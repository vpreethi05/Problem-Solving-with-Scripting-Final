# core/reader.py

import csv
from CourierOptimizer.core.validator import (
    is_valid_name,
    is_valid_lat,
    is_valid_lon,
    is_valid_priority,
    is_valid_weight,
)


def read_deliveries(filepath):
    """
    Reads a CSV file and validates each row.

    Returns:
        valid_rows (list of dict)
        rejected_rows (list of dict)
    """

    valid_rows = []
    rejected_rows = []

    try:
        with open(filepath, newline='', encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                customer = row.get("customer", "").strip()
                lat = row.get("latitude", "").strip()
                lon = row.get("longitude", "").strip()
                priority = row.get("priority", "").strip()
                weight = row.get("weight_kg", "").strip()

                valid = (
                    is_valid_name(customer)
                    and is_valid_lat(lat)
                    and is_valid_lon(lon)
                    and is_valid_priority(priority)
                    and is_valid_weight(weight)
                )

                if valid:
                    valid_rows.append({
                        "customer": customer,
                        "lat": float(lat),
                        "lon": float(lon),
                        "priority": priority,
                        "weight": float(weight),
                    })
                else:
                    rejected_rows.append(row)

    except FileNotFoundError:
        print("File not found. Please check your CSV path.")
        return [], []

    return valid_rows, rejected_rows
