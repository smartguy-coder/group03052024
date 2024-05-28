from abc import ABC, abstractmethod


class BaseWeapon(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def fire(self):
        pass

    def __len__(self):
        return len(self.name)


class Tank(BaseWeapon):
    def __init__(self, name, bullets: int):
        super().__init__(name)
        self.bullets = bullets

    def fire(self):
        print(f'Tank {self} fire')

    def __str__(self):
        return f'-- Tank: {id(self)} --'


class Submarine(BaseWeapon):
    def __str__(self):
        return f'-- Submarine: {id(self)} --'

    def fire(self):
        raise NotImplementedError


class Artillery(BaseWeapon):
    def __str__(self):
        return f'-- Artillery: {id(self)} --'

    def fire(self):
        print(f'{self} fire unique bullet')


tank = Tank('abrams', 45)
tank1 = Tank('T-64-2', 40)
tank.fire()
arta = Artillery('M777')
arta.fire()
tank.fire()
tank.fire()
tank.fire()

submarine = Submarine('K-18')


print(len('5757567'))
print(len(submarine))
print(len(tank1))
