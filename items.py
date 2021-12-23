class Weapon:
    def __init__(self):
        raise NotImplementedError("Do not create Weapon objects.")

    def __str__(self):
        return self.name


class Ak47(Weapon):
    def __init__(self):
        self.name = "soldier with Ak47"
        self.description = "A fist-sized Ak47, suitable for kill the enenies."
        self.damage = 5
        self.value = 1


class battle_Tank(Weapon):
    def __init__(self):
        self.name = "battle Tank"
        self.description = "A small battle_Tank with some Rocket launcher. " \
                           "Somewhat more dangerous than a soldier."
        self.damage = 10
        self.value = 50


class RustySword(Weapon):
    def __init__(self):
        self.name = "Rusty sword"
        self.description = "This sword is showing its age, " \
                           "but still has some fight in it."
        self.damage = 20
        self.value = 100


class Consumable:
    def __init__(self):
        raise NotImplementedError("Do not create raw Consumable objects.")

    def __str__(self):
        return "{} (+{} soldier)".format(self.name, self.healing_value)


class health_kit(Consumable):
    def __init__(self):
        self.name = "health kit"
        self.healing_value = 10
        self.value = 12


class HealingPotion(Consumable):
    def __init__(self):
        self.name = "Healing Potion"
        self.healing_value = 50
        self.value = 60


