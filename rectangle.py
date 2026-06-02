# Custom Classes in python

class Rectangle:
    def __init__(self, length, width):
        self.length = length
        self.width = width
    
    def __iter__(self):
        return iter(self.__dict__.items())

r = Rectangle(6, 4)

for i in r:
    print(*i)