class Ration:
    def __init__(self):
        self.list = []  # [{},]

    def append(self, field: dict):
        self.list.append(field)

def field(item, quantity, period):
    return {'item': item, 'quantity': quantity,
            'period': period, 'intake': 0}
