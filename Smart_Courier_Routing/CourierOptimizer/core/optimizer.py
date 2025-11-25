# core/optimizer.py
# Builds delivery route, computes totals, writes route and metrics, supports Pareto mode.

import csv
import os
from math import inf

from CourierOptimizer.core.haversine import haversine_distance
from CourierOptimizer.utils.logger import Logger
from CourierOptimizer.utils.decorators import timing_decorator
from CourierOptimizer.core.metrics_writer import write_metrics_csv

# Priority effect: lower weight = more important (High < Medium < Low)
PRIORITY_WEIGHTS = {
    "High": 0.6,
    "Medium": 1.0,
    "Low": 1.2,
}


@timing_decorator
def optimize(deliveries, depot, mode, objective, return_totals: bool = False):
    """
    Main optimisation function using a greedy, nearest-best approach.

    Supports objectives:
      - 'fastest'      : minimise travel time
      - 'lowest_cost'  : minimise monetary cost (with weight penalty)
      - 'lowest_co2'   : minimise emissions (with priority penalty)
      - 'pareto'       : simple multi-objective combination of time, cost, and CO2

    return_totals:
        False → return only route (pytest expects this)
        True  → return route + totals (CLI uses this)
    """
    logger = Logger("run.log")
    logger.log("=== Optimization Run Started ===")
    logger.log(f"Depot: {depot}")
    logger.log(f"Mode: {mode.name}")
    logger.log(f"Objective: {objective}")

    # Copy list to avoid modifying original
    unvisited = deliveries.copy()

    # Pre-compute a max weight for normalisation (avoid division by zero)
    weight_values = []
    for stop in deliveries:
        try:
            w = float(stop.get("weight", 0))
            if w > 0:
                weight_values.append(w)
        except (TypeError, ValueError):
            continue
    max_weight = max(weight_values) if weight_values else 1.0

    # Start at depot
    current_lat = depot["lat"]
    current_lon = depot["lon"]

    route = []
    metrics = []
    iteration = 1

    # Running totals
    total_distance = 0.0
    total_time = 0.0
    total_cost = 0.0
    total_co2 = 0.0

    # Weights used in Pareto scoring (can be tuned)
    w_time = 0.5
    w_cost = 0.3
    w_co2 = 0.2

    # --------------------------------------------------------------
    # MAIN LOOP
    # --------------------------------------------------------------
    while unvisited:

        best_stop = None
        best_score = inf
        best_distance = 0.0
        best_time = 0.0
        best_cost = 0.0
        best_co2 = 0.0

        for stop in unvisited:
            # Distance from current location to candidate stop
            dist = haversine_distance(
                current_lat,
                current_lon,
                stop["lat"],
                stop["lon"],
            )

            # Priority factor (defensive default = 1.0)
            priority_factor = PRIORITY_WEIGHTS.get(stop.get("priority", "Medium"), 1.0)

            # Weight in kilograms (defensive parsing)
            try:
                weight_kg = float(stop.get("weight", 0.0))
            except (TypeError, ValueError):
                weight_kg = 0.0

            # Normalised weight in [0, 1]
            weight_norm = weight_kg / max_weight if max_weight > 0 else 0.0

            # Base travel metrics for this segment
            time_hours = dist / mode.speed_kmh
            cost_units = dist * mode.cost_per_km
            co2_units = dist * mode.co2_per_km

            # Slightly different interpretations per objective so that
            # routes can actually change depending on the goal.
            if objective == "fastest":
                # Pure time, but still slightly influenced by priority
                score = time_hours * priority_factor

            elif objective == "lowest_cost":
                # Heavier parcels increase effective cost penalty
                cost_with_weight = cost_units * (1.0 + 0.4 * weight_norm)
                score = cost_with_weight * priority_factor

            elif objective == "lowest_co2":
                # Low-priority stops are penalised more for emissions
                co2_with_priority = co2_units * (1.0 + 0.3 * (priority_factor - 1.0))
                score = co2_with_priority

            elif objective == "pareto":
                # Simple multi-objective weighted sum
                # Time (hours), cost, and CO2 scaled into one score
                cost_with_weight = cost_units * (1.0 + 0.4 * weight_norm)
                co2_with_priority = co2_units * (1.0 + 0.3 * (priority_factor - 1.0))

                score = priority_factor * (
                    w_time * time_hours +
                    w_cost * cost_with_weight +
                    w_co2 * co2_with_priority
                )

            else:
                # Default fallback: fastest
                score = time_hours * priority_factor

            # Greedy choice: keep the best-scoring stop
            if score < best_score:
                best_score = score
                best_stop = stop
                best_distance = dist
                best_time = time_hours
                best_cost = cost_units
                best_co2 = co2_units

        # ------------- After choosing the best stop for this step -------------

        # Add chosen stop to route
        route.append({
            "customer": best_stop["customer"],
            "lat": best_stop["lat"],
            "lon": best_stop["lon"],
            "priority": best_stop.get("priority", "-"),
            "distance_from_prev": best_distance,
            "cumulative_distance": total_distance + best_distance,
            "eta_hours": best_time,
            "cost": best_cost,
            "co2": best_co2,
        })

        # Save metrics row
        metrics.append({
            "iteration": iteration,
            "selected_customer": best_stop["customer"],
            "raw_distance": best_distance,
            "weighted_score": best_score,
            "cumulative_distance": total_distance + best_distance,
            "cumulative_time": total_time + best_time,
            "cumulative_cost": total_cost + best_cost,
            "cumulative_co2": total_co2 + best_co2,
        })
        iteration += 1

        # Update totals
        total_distance += best_distance
        total_time += best_time
        total_cost += best_cost
        total_co2 += best_co2

        # Move to new location
        current_lat = best_stop["lat"]
        current_lon = best_stop["lon"]

        # Mark stop as visited
        unvisited.remove(best_stop)

    # --------------------------------------------------------------
    # RETURN TO DEPOT
    # --------------------------------------------------------------
    rdist = haversine_distance(current_lat, current_lon, depot["lat"], depot["lon"])
    rtime = rdist / mode.speed_kmh
    rcost = rdist * mode.cost_per_km
    rco2 = rdist * mode.co2_per_km

    route.append({
        "customer": "RETURN_TO_DEPOT",
        "lat": depot["lat"],
        "lon": depot["lon"],
        "priority": "-",
        "distance_from_prev": rdist,
        "cumulative_distance": total_distance + rdist,
        "eta_hours": rtime,
        "cost": rcost,
        "co2": rco2,
    })

    # Update totals
    total_distance += rdist
    total_time += rtime
    total_cost += rcost
    total_co2 += rco2

    # Log totals
    logger.log_totals(total_distance, total_time, total_cost, total_co2)

    # Write output files
    write_route_csv(route)
    write_metrics_csv(metrics)

    # Return format depends on caller
    if return_totals:
        return route, total_distance, total_time, total_cost, total_co2
    else:
        return route


# --------------------------------------------------------------
# ROUTE CSV WRITER
# --------------------------------------------------------------
def write_route_csv(route, filename: str = "route.csv"):
    """
    Write the final route (including RETURN_TO_DEPOT) to a CSV file.
    """
    output_dir = os.path.join(os.getcwd(), "output")
    os.makedirs(output_dir, exist_ok=True)

    full_path = os.path.join(output_dir, filename)
    keys = route[0].keys()

    with open(full_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(route)

    print(f"Route saved to: {full_path}")
