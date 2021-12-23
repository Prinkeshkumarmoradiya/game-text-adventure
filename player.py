import items
import world


class Player:
    def __init__(self):
        self.inventory = [items.Ak47(),
                          items.battle_Tank(),
                          items.health_kit()]
        self.x = world.start_tile_location[0]
        self.y = world.start_tile_location[1]
        self.soldier = 100
        self.Healing_potion = 5
        self.victory = False

    def is_alive(self):
        return self.soldier > 0

    def print_inventory(self):
        print("army and weapons:")
        for item in self.inventory:
            print('* ' + str(item))
        print("  Healing potion: {}".format(self.Healing_potion))

    def heal(self):
        consumables = [item for item in self.inventory
                       if isinstance(item, items.Consumable)]
        if not consumables:
            print("You don't have any items to heal you!")
            return

        for i, item in enumerate(consumables, 1):
            print("Choose an item to use to heal: ")
            print("{}. {}".format(i, item))

        valid = False
        while not valid:
            choice = input("")
            try:
                to_eat = consumables[int(choice) - 1]
                self.soldier = min(100, self.soldier + to_eat.healing_value)
                self.inventory.remove(to_eat)
                print("Current soldier: {}".format(self.soldier))
                valid = True
            except (ValueError, IndexError):
                print("Invalid choice, try again.")

    def most_powerful_weapon(self):
        max_damage = 0
        best_weapon = None
        for item in self.inventory:
            try:
                if item.damage > max_damage:
                    best_weapon = item
                    max_damage = item.damage
            except AttributeError:
                pass

        return best_weapon

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def move_north(self):
        self.move(dx=0, dy=-1)

    def move_south(self):
        self.move(dx=0, dy=1)

    def move_east(self):
        self.move(dx=1, dy=0)

    def move_west(self):
        self.move(dx=-1, dy=0)

    def attack(self):
        best_weapon = self.most_powerful_weapon()
        room = world.tile_at(self.x, self.y)
        enemy = room.enemy
        print("You use {} against {}!".format(best_weapon.name, enemy.name))
        enemy.soldier -= best_weapon.damage
        if not enemy.is_alive():
            print("You killed {}!".format(enemy.name))
        else:
            print("{} soldier is {}.".format(enemy.name, enemy.soldier))

    def trade(self):
        room = world.tile_at(self.x, self.y)
        room.check_if_exchange(self)
