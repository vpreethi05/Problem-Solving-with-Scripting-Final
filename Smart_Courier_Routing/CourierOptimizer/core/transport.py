# core/transport.py

class TransportMode:
    """
    A simple class to hold transport properties.
    Each mode has:
      - speed in km/h
      - cost per km
      - CO2 emissions per km
    """

    def __init__(self, name, speed_kmh, cost_per_km, co2_per_km):
        self.name = name
        self.speed_kmh = speed_kmh
        self.cost_per_km = cost_per_km
        self.co2_per_km = co2_per_km


# Transport modes as described in the assignment
MODES = {
    "car": TransportMode("Car", speed_kmh=50, cost_per_km=4, co2_per_km=120),
    "bicycle": TransportMode("Bicycle", speed_kmh=15, cost_per_km=0, co2_per_km=0),
    "walk": TransportMode("Walking", speed_kmh=5, cost_per_km=0, co2_per_km=0),
}
