# utils/plotter.py
# Fixed version: correct depot handling + correct route connections

import os
import matplotlib.pyplot as plt

def plot_route(route):

    if not route:
        print("No route to plot.")
        return

    # ------------------------------------------
    # Extract route order as-is from optimizer
    # route[-1] = RETURN_TO_DEPOT
    # ------------------------------------------

    lats = [stop["lat"] for stop in route]
    lons = [stop["lon"] for stop in route]
    names = [stop["customer"] for stop in route]

    # Identify depot (last point)
    depot_lat = lats[-1]
    depot_lon = lons[-1]

    # Delivery stops only
    delivery_lats = lats[:-1]
    delivery_lons = lons[:-1]
    delivery_names = names[:-1]

    # ------------------------------------------
    # FIX: Draw a CLOSED LOOP
    # Connect depot → first stop → ... → last stop → depot
    # ------------------------------------------
    closed_lats = [depot_lat] + lats
    closed_lons = [depot_lon] + lons

    # Output folder
    output_dir = os.path.join(os.getcwd(), "output")
    os.makedirs(output_dir, exist_ok=True)
    save_path = os.path.join(output_dir, "route_plot.png")

    plt.figure(figsize=(8, 6))

    # Route lines (closed loop)
    plt.plot(closed_lons, closed_lats, color="gray", linestyle="-", linewidth=1)

    # Delivery markers
    plt.scatter(delivery_lons, delivery_lats, color="blue", label="Delivery stops")

    # Depot marker
    plt.scatter([depot_lon], [depot_lat], color="red", marker="s", s=90, label="Depot (start/stop)")

    # Labels for delivery stops
    for lon, lat, name in zip(delivery_lons, delivery_lats, delivery_names):
        plt.text(lon, lat, name, fontsize=8, ha="left", va="bottom")

    # Label depot
    plt.text(depot_lon, depot_lat, "DEPOT", fontsize=9, weight="bold", ha="left", va="bottom")

    plt.title("Courier Route (Longitude vs Latitude)")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.grid(True)
    plt.legend(loc="upper left")

    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"Route plot saved to: {save_path}")
