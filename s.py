class Test:
    def __init__(self):
        self.x =5
        self.change_x()
    def change_x(self):
        self.x = 10

test = Test()
print(test.x)