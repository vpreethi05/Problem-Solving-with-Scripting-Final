# core/metrics_writer.py
# Writes per-iteration optimization metrics.

import os
import csv


def write_metrics_csv(metrics, filename="metrics.csv"):
    """
    Saves the optimization metrics to output/metrics.csv.
    Creates the output folder if it does not exist.
    """

    # Make sure output folder exists
    output_dir = os.path.join(os.getcwd(), "output")
    os.makedirs(output_dir, exist_ok=True)

    # Full path to metrics.csv
    full_path = os.path.join(output_dir, filename)

    # If metrics list is empty, nothing to write
    if not metrics:
        print("No metrics to write.")
        return

    keys = metrics[0].keys()

    # Write CSV
    with open(full_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(metrics)

    print(f"Metrics saved to: {full_path}")
