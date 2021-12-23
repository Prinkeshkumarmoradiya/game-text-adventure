class Enemy:
    def __init__(self):
        raise NotImplementedError("Do not create raw Enemy objects.")

    def __str__(self):
        return self.name

    def is_alive(self):
        return self.soldier > 0


class Yellow_army(Enemy):
    def __init__(self):
        self.name = "Yellow army"
        self.soldier = 10
        self.damage = 2


class Blue_army(Enemy):
    def __init__(self):
        self.name = "Blue army"
        self.soldier = 30
        self.damage = 10


class Red_army(Enemy):
    def __init__(self):
        self.name = "Red army"
        self.soldier = 70
        self.damage = 4


class Black_army(Enemy):
    def __init__(self):
        self.name = "Black army"
        self.soldier = 80
        self.damage = 15
