class TripRequest:
    def __init__(self, city, days, budget):
        self.city = city
        self.days = days
        self.budget = budget


trip = TripRequest(
    "成都",
    5,
    5000
)

print(trip.city)
print(trip.days)
print(trip.budget)