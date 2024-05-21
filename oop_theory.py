import datetime
import datetime as dt


class Person:
    def __init__(self, name: str, weight: float):
        self.first_name = name
        self.weight = weight
        # self.birthday = dt.datetime.now(datetime.UTC) - dt.timedelta(days=365*11)
        self.birthday = dt.datetime(year=2013, month=11, day=22)

    # def age(self):
    #     return (dt.datetime.now(datetime.UTC) - self.birthday).days // 365


alex = Person(name='Alex', weight=3.6)
print(alex)
print(alex.__dict__)
print(alex.birthday)
print(alex.first_name)
# print(alex.age())
