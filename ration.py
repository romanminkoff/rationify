class Periods:
    Week = 'Week'

class Ration:
    def __init__(self):
        self.list = []  # [{},]

    def append(self, field: dict):
        self.list.append(field)

def field(item, quantity, period):
    return {'item': item, 'quantity': quantity,
            'period': period, 'intake': 0}

def reset_intake(items:list):
    for item in items:
        item['intake'] = "0"
    return items
