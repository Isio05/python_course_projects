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


def get_currency_resource(resource, transform=(lambda x: x)):
    data = {
        'items':[
            {'code': 'usd', 'amount_to_usd': 1.00},
            {'code': 'eur', 'amount_to_usd': 1.07},
            {'code': 'gbp', 'amount_to_usd': 3.00},
            {'code': 'jpy', 'amount_to_usd': 0.05}
        ]
    }

    my_resource = data[resource]
    #return [transform(x) for x in my_resource]
    return list(map(transform, my_resource))


def get_codes():
    return get_currency_resource('items', transform=(lambda x: x['code'].upper()))


def get_currencies():
    return get_currency_resource('items', transform=(lambda x: Currency(x['code'], x['amount_to_usd'])))


def convert_all_to_usd(usd_amount):
    print("{} amount of USD converted to all currencies".format(usd_amount))
    list_of_currency_objects = get_currencies()
    for item in list_of_currency_objects:
        item.amount = 1000
        print("{} USD in {} is {:.2f}".format(usd_amount, item.code.upper(), item.in_usd()))


pounds = Currency('GBP', 1.40)
pounds.set_the_amount(1000)
euros = Currency('EUR', 1.07)
euros.set_the_amount(1000)

print(pounds <= euros)
print(get_codes())
convert_all_to_usd(1000)