class Decimal:
    def __init__(self, number, places):
        self.number = number
        self.places = places

    def __repr__(self):
        return '%.{}f'.format(self.places) % self.number


class Currency(Decimal):
    def __init__(self, number, places, symbol):
        super().__init__(number, places)
        self.symbol = symbol

    def __repr__(self):
        return "{} {}".format(self.symbol, super().__repr__())


print(Decimal(3.26257366, 3))
print(Currency(3.26257366, 3, "EUR"))
