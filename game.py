from collections import OrderedDict
from player import Player
import world


def play():
    print("Escape from Cave Terror!")
    world.parse_world_dsl()
    player = Player()
    while player.is_alive() and not player.victory:
        room = world.tile_at(player.x, player.y)
        print(room.intro_text())
        room.modify_player(player)
        if player.is_alive() and not player.victory:
            choose_action(room, player)
        elif not player.is_alive():
            print("ohh sorry you can not save your army better luck next time!")


def choose_action(room, player):
    action = None
    while not action:
        available_actions = get_available_actions(room, player)
        action_input = input("Action: ")
        action = available_actions.get(action_input)
        if action:
            action()
        else:
            print("Invalid action!")


def get_available_actions(room, player):
    actions = OrderedDict()
    print("Take Action: ")
    if player.inventory:
        action_adder(actions, 'i', player.print_inventory, "show my army and weapons")
    if isinstance(room, world.Armybase):
        action_adder(actions, 'c', player.trade, "collect")
    if isinstance(room, world.EnemyTile) and room.enemy.is_alive():
        action_adder(actions, 'a', player.attack, "Attack")
    else:
        if world.tile_at(room.x, room.y - 1):
            action_adder(actions, 'n', player.move_north, "Narvik Islands")
        if world.tile_at(room.x, room.y + 1):
            action_adder(actions, 's', player.move_south, "Solomon Islands")
        if world.tile_at(room.x + 1, room.y):
            action_adder(actions, 'e', player.move_east, "Erodrome Islands")
        if world.tile_at(room.x - 1, room.y):
            action_adder(actions, 'w', player.move_west, "Wake Island")
    if player.soldier < 100:
        action_adder(actions, 'h', player.heal, "Heal")

    return actions


def action_adder(action_dict, hotkey, action, name):
    action_dict[hotkey.lower()] = action
    action_dict[hotkey.upper()] = action
    print("{}: {}".format(hotkey, name))


play()
