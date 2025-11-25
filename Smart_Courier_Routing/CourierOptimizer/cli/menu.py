# cli/menu.py
# Command-line menu for CourierOptimizer with Pareto, plotting, and console totals.

from CourierOptimizer.core.reader import read_deliveries
from CourierOptimizer.core.optimizer import optimize
from CourierOptimizer.core.transport import MODES
from CourierOptimizer.utils.logger import Logger
from CourierOptimizer.utils.plotter import plot_route


def run_cli():
    print("=== CourierOptimizer CLI ===\n")

    # -----------------------------
    # CSV INPUT
    # -----------------------------
    csv_path = input("Enter path to CSV file (e.g., C:/Users/.../sample.csv): ").strip()

    print("\nReading and validating deliveries...")
    valid_rows, rejected_rows = read_deliveries(csv_path)
    print(f"Valid rows: {len(valid_rows)}")
    print(f"Rejected rows: {len(rejected_rows)}")

    logger = Logger("run.log")
    logger.log_rejected(rejected_rows)

    # -----------------------------
    # DEPOT INPUT
    # -----------------------------
    print("\nEnter depot coordinates:")
    try:
        depot_lat = float(input("Depot latitude: ").strip())
        depot_lon = float(input("Depot longitude: ").strip())
    except:
        print("Invalid depot coordinates. Exiting.")
        return

    depot = {"lat": depot_lat, "lon": depot_lon}

    # -----------------------------
    # TRANSPORT MODE
    # -----------------------------
    print("\nSelect transport mode:")
    print("1. Car")
    print("2. Bicycle")
    print("3. Walking")

    mode_choice = input("Enter choice (1-3): ").strip()

    if mode_choice == "1":
        mode = MODES["car"]
    elif mode_choice == "2":
        mode = MODES["bicycle"]
    elif mode_choice == "3":
        mode = MODES["walk"]
    else:
        print("Invalid mode. Exiting.")
        return

    # -----------------------------
    # OBJECTIVE
    # -----------------------------
    print("\nSelect optimization objective:")
    print("1. Fastest")
    print("2. Lowest Cost")
    print("3. Lowest CO2")
    print("4. Pareto (multi-objective)")

    obj_choice = input("Enter choice (1–4): ").strip()

    if obj_choice == "1":
        objective = "fastest"
    elif obj_choice == "2":
        objective = "lowest_cost"
    elif obj_choice == "3":
        objective = "lowest_co2"
    elif obj_choice == "4":
        objective = "pareto"
    else:
        print("Invalid objective. Exiting.")
        return

    print("\nRunning optimization...\n")

    # -----------------------------
    # RUN OPTIMIZER (ask for totals)
    # -----------------------------
    route, total_dist, total_time, total_cost, total_co2 = optimize(
        valid_rows, depot, mode, objective, return_totals=True
    )

    # -----------------------------
    # PLOT ROUTE
    # -----------------------------
    plot_route(route)

    # -----------------------------
    # PRINT TOTALS
    # -----------------------------
    print("\n=== Optimization Complete ===")
    print("Summary of totals:")
    print(f"Total distance: {total_dist:.2f} km")
    print(f"Total time: {total_time:.2f} hours")
    print(f"Total cost: {total_cost:.2f} NOK")
    print(f"Total CO2: {total_co2:.2f} g\n")

    print("Files saved in /output/:")
    print(" - route.csv")
    print(" - metrics.csv")
    print(" - rejected.csv")
    print(" - run.log")
    print(" - route_plot.png")

    # -----------------------------
    # PRINT ROUTE
    # -----------------------------
    print("\nOptimized route:")
    for stop in route:
        print(f"- {stop['customer']} (lat={stop['lat']}, lon={stop['lon']})")

    print("\nDone.")
