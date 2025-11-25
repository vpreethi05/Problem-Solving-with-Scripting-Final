# tests/test_basic.py
# Beginner-friendly pytest tests for CourierOptimizer

import os
import math
from CourierOptimizer.core.validator import (
    is_valid_name, is_valid_lat, is_valid_lon,
    is_valid_priority, is_valid_weight
)
from CourierOptimizer.core.haversine import haversine_distance
from CourierOptimizer.core.reader import read_deliveries
from CourierOptimizer.core.transport import MODES
from CourierOptimizer.core.optimizer import optimize


# -----------------------------------------------------------------------------
# VALIDATOR TESTS
# -----------------------------------------------------------------------------
def test_validators():
    assert is_valid_name("John Doe")
    assert not is_valid_name("")                # empty name invalid

    assert is_valid_lat("59.91")
    assert not is_valid_lat("200")              # invalid latitude

    assert is_valid_lon("10.75")
    assert not is_valid_lon("300")              # invalid longitude

    assert is_valid_priority("High")
    assert not is_valid_priority("Urgent")      # invalid

    assert is_valid_weight("4")
    assert not is_valid_weight("-3")            # negative invalid


# -----------------------------------------------------------------------------
# HAVERSINE TEST
# -----------------------------------------------------------------------------
def test_haversine_distance():
    # Distance between same point = 0
    d = haversine_distance(59.91, 10.75, 59.91, 10.75)
    assert math.isclose(d, 0.0, rel_tol=1e-6)


# -----------------------------------------------------------------------------
# READER TEST
# -----------------------------------------------------------------------------
def test_reader_reads_valid_rows(tmp_path):
    sample = tmp_path / "sample.csv"
    sample.write_text(
        "customer,latitude,longitude,priority,weight_kg\n"
        "John,59.91,10.75,High,2\n"
        "BadRow,200,10,High,1\n"
    )

    valid, rejected = read_deliveries(str(sample))
    assert len(valid) == 1
    assert len(rejected) == 1


# -----------------------------------------------------------------------------
# OPTIMIZER TEST
# -----------------------------------------------------------------------------
def test_optimizer_creates_route():
    deliveries = [
        {"customer": "A", "lat": 59.91, "lon": 10.75, "priority": "High", "weight": 1},
        {"customer": "B", "lat": 59.92, "lon": 10.70, "priority": "Medium", "weight": 1}
    ]

    depot = {"lat": 59.90, "lon": 10.70}
    mode = MODES["car"]

    route = optimize(deliveries, depot, mode, "fastest")

    # Must include both customers + RETURN_TO_DEPOT (total 3 stops)
    assert len(route) == 3

    # Last entry must be the depot
    assert route[-1]["customer"] == "RETURN_TO_DEPOT"


# -----------------------------------------------------------------------------
# OPTIMIZER TEST FOR ALL OBJECTIVES
# -----------------------------------------------------------------------------
def test_optimizer_objectives():
    deliveries = [
        {"customer": "A", "lat": 59.91, "lon": 10.75, "priority": "High", "weight": 1},
        {"customer": "B", "lat": 59.92, "lon": 10.70, "priority": "Medium", "weight": 1}
    ]

    depot = {"lat": 59.90, "lon": 10.70}
    mode = MODES["car"]

    objectives = ["fastest", "lowest_cost", "lowest_co2", "pareto"]

    for obj in objectives:
        route = optimize(deliveries.copy(), depot, mode, obj)
        assert route[-1]["customer"] == "RETURN_TO_DEPOT"
