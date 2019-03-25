import unittest

class Currency:
    def __init__(self, code, exchange_to_usd):
        self.amount = 0.00
        self.code = code
        self.exchange_to_usd = exchange_to_usd

    def __repr__(self):
        return '{} of {}'.format(self.amount, self.code)

    def in_currency(self):
        converted = self.amount / self.exchange_to_usd
        return '%.4f' % converted

    def in_usd(self, amount=None):
        to_convert = amount or self.amount
        return to_convert / (1 / self.exchange_to_usd)

    def set_the_amount(self, amount):
        self.amount = amount

    def __gt__(self, other):
        return self.in_usd() > other.in_usd()

    def __lt__(self, other):
        return self.in_usd() < other.in_usd()

    def __eq__(self, other):
        return self.in_usd() == other.in_usd()

    def __le__(self, other):
        return self.in_usd() <= other.in_usd()

    def __ge__(self, other):
        return self.in_usd() >= other.in_usd()


class CurrencyTest(unittest.TestCase):

    def test_create_currency(self):
        pound = Currency('GBP', 1.35)

        self.assertEqual(pound.code, 'GBP')
        self.assertEqual(pound.exchange_to_usd, 1.35)

    def test_set_amount(self):
        pound = Currency('GBP', 1.35)
        euro = Currency('EUR', 1.18)

        pound.set_the_amount(1000)
        euro.set_the_amount(100)

        self.assertEqual(pound.amount, 1000)
        self.assertEqual(euro.amount, 100)

    def test_comparisons(self):
        pound = Currency('GBP', 1.35)
        euro = Currency('EUR', 1.18)

        pound.set_the_amount(1000)
        euro.set_the_amount(100)

        self.assertTrue(pound > euro)
        self.assertFalse(pound < euro)
        self.assertFalse(pound == euro)

    def test_to_usd(self):
        pound = Currency('GBP', 1.35)
        self.assertEqual(pound.in_usd(1000), 1350)

    def test_comparison_with_exceptions(self):
        pound = Currency('GBP', 1.35)
        pound.set_the_amount(1000)

        with self.assertRaises(AttributeError):
            pound == 1000
