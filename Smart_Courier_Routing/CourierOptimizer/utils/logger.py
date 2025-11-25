# utils/logger.py
# Simple logger for writing messages, totals, and rejected rows.

import os
import csv
from datetime import datetime


class Logger:
    def __init__(self, filename="run.log"):
        """
        Initialize the logger.
        Creates /output folder automatically.
        """

        output_dir = os.path.join(os.getcwd(), "output")
        os.makedirs(output_dir, exist_ok=True)

        # File where logs will be written
        self.filepath = os.path.join(output_dir, filename)

    def log(self, message):
        """
        Write a single log message with timestamp.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(self.filepath, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {message}\n")

    def log_totals(self, total_distance, total_time, total_cost, total_co2):
        """
        Write summary of totals at the end of optimization.
        """
        self.log(f"Total distance: {total_distance:.3f} km")
        self.log(f"Total time: {total_time:.3f} hours")
        self.log(f"Total cost: {total_cost:.3f} NOK")
        self.log(f"Total CO2: {total_co2:.3f} g")

    def log_rejected(self, rejected_rows, filename="rejected.csv"):
        """
        Save rejected rows to output/rejected.csv.
        """

        if not rejected_rows:
            return

        output_dir = os.path.join(os.getcwd(), "output")
        os.makedirs(output_dir, exist_ok=True)

        full_path = os.path.join(output_dir, filename)

        keys = rejected_rows[0].keys()

        with open(full_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(rejected_rows)

        self.log(f"{len(rejected_rows)} rejected rows saved to {filename}")
