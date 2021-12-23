import enemies
import Heal
import random


class MapTile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def intro_text(self):
        raise NotImplementedError("Create a subclass instead!")

    def modify_player(self, player):
        pass


class StartTile(MapTile):
    def intro_text(self):
        return """
        Welcome to " The Battleship" you are The Army Chief and, you have 100 Soldiers to win the battle on different Islands. 
        You can use your power to increase and make your kingdom safe!
        """


class EnemyTile(MapTile):
    def __init__(self, x, y):
        r = random.random()
        if r < 0.20:
            self.enemy = enemies.Yellow_army()
            self.alive_text = "Yellow army start batlle against you " \
                              "Now its time to win the Island!"
            self.dead_text = "You see the Yellow_army dead," \
                             "All Dead soldiers on the ground."
        elif r < 0.40:
            self.enemy = enemies.Blue_army()
            self.alive_text = "You are in Islands and batlle is started!"
            self.dead_text = "You alrady win the Islands!"
        elif r < 0.60:
            self.enemy = enemies.Red_army()
            self.alive_text = "Red army has almost same soldier which we have so be careful" \
                              "...suddenly the attack started, you should attack!"
            self.dead_text = "Dozens of dead soldiers' on the ground."
        else:
            self.enemy = enemies.Black_army()
            self.alive_text = "Black army is the strongest army ever! Play carefully. :) " \
                              "put your all power to win the battle. Best of luck!"
            self.dead_text = "Island is yours, now look forward to other areas.." \
                             "Increase your army and lest go!"

        super().__init__(x, y)

    def intro_text(self):
        text = self.alive_text if self.enemy.is_alive() else self.dead_text
        return text

    def modify_player(self, player):
        if self.enemy.is_alive():
            player.soldier = player.soldier - self.enemy.damage
            print("Enemy does kill {} soldier. You have {} soldier remaining.".
                  format(self.enemy.damage, player.soldier))


class VictoryTile(MapTile):
    def modify_player(self, player):
        player.victory = True

    def intro_text(self):
        return """
        You see a bright light in the distance...
        ... it grows as you get closer! It's sunlight!


        Victory is yours!
        """


class FindHealing_potionTile(MapTile):
    def __init__(self, x, y):
        self.Healing_potion = random.randint(1, 50)
        self.Healing_potion_claimed = False
        super().__init__(x, y)

    def modify_player(self, player):
        if not self.Healing_potion_claimed:
            self.Healing_potion_claimed = True
            player.Healing_potion = player.Healing_potion + self.Healing_potion
            print("+{} Healing potion added.".format(self.Healing_potion))

    def intro_text(self):
        if self.Healing_potion_claimed:
            return """
            you already collected the healing potion ON this Island
            """
        else:
            return """
            You got some healing potion which help you to increase army and health kit.
            """


class Armybase(MapTile):
    def __init__(self, x, y):
        self.trader = Heal.Trader()
        super().__init__(x, y)

    def check_if_Exchange(self, player):
        while True:
            print("Would you like to (j)oin, (r)emove, or (Q)uit?")
            user_input = input()
            if user_input in ['Q', 'q']:
                return
            elif user_input in ['J', 'j']:
                print("Here's how many soldier join you: ")
                self.trade(buyer=player, seller=self.trader)
            elif user_input in ['R', 'r']:
                print("Here's how many soldier leve you: ")
                self.trade(buyer=self.trader, seller=player)
            else:
                print("Invalid choice!")

    def trade(self, buyer, seller):
        for i, item in enumerate(seller.inventory, 1):
            print("{}. {} - {} Healing_potion".format(i, item.name, item.value))
        while True:
            user_input = input("Choose an item or press Q to exit: ")
            if user_input in ['Q', 'q']:
                return
            else:
                try:
                    choice = int(user_input)
                    to_swap = seller.inventory[choice - 1]
                    self.swap(seller, buyer, to_swap)
                except ValueError:
                    print("Invalid choice!")

    def swap(self, seller, buyer, item):
        if item.value > buyer.Healing_potion:
            print("That's too expensive")
            return
        seller.inventory.remove(item)
        buyer.inventory.append(item)
        seller.Healing_potion = seller.Healing_potion + item.value
        buyer.Healing_potion = buyer.Healing_potion - item.value
        print("Exchange complete!")

    def intro_text(self):
        return """
        This is your base and you can exchange the soldier or you can take Healing posion with you!
        Its time rest soldier and heal your army...
        """

world_dsl = """
|EN|EN|VT|EN|EN|
|EN|  |  |  |EN|
|EN|HP|EN|  |AB|
|AB|  |ST|HP|EN|
|HP|  |EN|  |HP|
"""


def is_dsl_valid(dsl):
    if dsl.count("|ST|") != 1:
        return False
    if dsl.count("|VT|") == 0:
        return False
    lines = dsl.splitlines()
    lines = [l for l in lines if l]
    pipe_counts = [line.count("|") for line in lines]
    for count in pipe_counts:
        if count != pipe_counts[0]:
            return False

    return True

tile_type_dict = {"VT": VictoryTile,
                  "EN": EnemyTile,
                  "ST": StartTile,
                  "HP": FindHealing_potionTile,
                  "AB": Armybase,
                  "  ": None}


world_map = []

start_tile_location = None


def parse_world_dsl():
    if not is_dsl_valid(world_dsl):
        raise SyntaxError("DSL is invalid!")

    dsl_lines = world_dsl.splitlines()
    dsl_lines = [x for x in dsl_lines if x]

    for y, dsl_row in enumerate(dsl_lines):
        row = []
        dsl_cells = dsl_row.split("|")
        dsl_cells = [c for c in dsl_cells if c]
        for x, dsl_cell in enumerate(dsl_cells):
            tile_type = tile_type_dict[dsl_cell]
            if tile_type == StartTile:
                global start_tile_location
                start_tile_location = x, y
            row.append(tile_type(x, y) if tile_type else None)

        world_map.append(row)


def tile_at(x, y):
    if x < 0 or y < 0:
        return None
    try:
        return world_map[y][x]
    except IndexError:
        return None
