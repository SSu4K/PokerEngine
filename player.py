class Player:
    def __init__(self, name, money) -> None:
        self.name = name
        self.money = money
    
    def __repr__(self):
        return str(vars(self))
        