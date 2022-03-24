import pprint
import random

from fireplace import cards
from fireplace.game import Game
from fireplace.player import Player
from fireplace.utils import random_draft
from hslog import LogParser

from hslog.export import EntityTreeExporter, FriendlyPlayerExporter
import platform

from pathlib import Path
from string import ascii_uppercase, ascii_lowercase

from hearthstone.enums import CardType, GameTag, Zone, CardClass

pp = pprint.PrettyPrinter(depth=6)
pp = pp.pprint

# for line in tailer.follow(open(
# '/home/dee/.PlayOnLinux/wineprefix/hs/drive_c/Program Files/Hearthstone/Logs/Power.log'), 0):
#     print(line)
global g, fplayer, eplayer
p = LogParser()
# system = platform.system()
# hs_path = None
# if system == 'Darwin':
#     hs_path = Path('/') / 'Applications' / 'Hearthstone' / 'Logs' / 'Power.log'
# elif system == 'Windows':
#     for Disk in ascii_uppercase:
#         hs_path = Path(f'{Disk}:\\') / 'Program Files (x86)' / 'Hearthstone' / 'Logs' / 'Power.log'
#         if hs_path.exists():
#             break
# elif system == 'Linux':
#     if 'Microsoft' in platform.release():
#         for Disk in ascii_lowercase:
#             hs_path = Path('/') / 'mnt' / Disk / 'Program Files (x86)' / 'Hearthstone' / 'Logs' / 'Power.log'
#             if hs_path.exists():
#                 break

hs_path = Path(r'C:\Users\PotatoHD\Documents\GitHub\hs-log-fireplace\Power.log')


def reload():
    global p, g, fplayer, eplayer
    # with open('/home/dee/.PlayOnLinux/wineprefix/hs/drive_c/Program Files/Hearthstone/Logs/Power.log') as f:
    with open(hs_path) as f:
        # print(f.read())
        p.read(f)
        p.flush()
        g = p.games[-1].export().game
        fplayer = g.players[0]
        eplayer = g.players[1]


def get_hand_events(player):
    for e in g.entities:
        # print(e.zone == Zone.HAND, str(e.controller))
        if e.zone == Zone.HAND and e.tags[GameTag.CONTROLLER] == player.player_id:
            ...
            # print(f"ACTION FROM HAND: {e} {e.__dict__.keys()} {e._initial_controller} {e.initial_creator} {e.tags}")


def get_amount_handcards(player):
    return len([e for e in g.entities if (e.zone == Zone.HAND and e.tags[GameTag.CONTROLLER] == player.player_id)])


def get_amount_minions(player):
    return len([e for e in g.entities if (e.zone == Zone.PLAY and
                                          e.type == CardType.MINION and e.tags[
                                              GameTag.CONTROLLER] == player.player_id)])


def get_heropower_active(player):
    for e in g.entities:
        if e.zone == Zone.PLAY and e.type == CardType.HERO_POWER and e.tags[GameTag.CONTROLLER] == player.player_id:
            # print(e.__dict__)
            ...
            # return True if e.tags[GameTag.EXHAUSTED] == 0 else False


class Decoder:
    def __init__(self):
        self.arr = []

    def push(self, el):
        self.arr.append(el)

    pass


def main():
    cards.db.initialize()

    c1 = CardClass(random.randint(2, 10))
    c2 = CardClass(random.randint(2, 10))
    deck1 = random_draft(c1)
    deck2 = random_draft(c2)

    players = []
    players.append(Player("Player1", deck1, c1.default_hero))
    players.append(Player("Player2", deck2, c2.default_hero))
    game1 = Game(players=players)
    game1.start()
    print(game1.tags)
    if hs_path is not None and hs_path.exists():
        reload()
        # print(fplayer.player_id)
        get_hand_events(fplayer)
        get_heropower_active(fplayer)
        get_amount_minions(fplayer)
        get_amount_minions(fplayer)
        # for key, value in p.games[-1].export().__dict__.items():
        #     print(key, value)
        # exporter = EntityTreeExporter(p.games[-1])
        # what = exporter.export()
        game = p.games[-1].export()
        print(game)
        # for packet in p.games[-1].packets:
        #     print(vars(packet))
        #     print()
        # print(vars(fplayer))
        # print(vars(what))
        # print(export)
        # for key, value in g.players[0].__dict__.items():
        #     print(key, value, sep=':')
        # print("HandCards {:<20}: {}".format("", get_amount_handcards()))
        # print(fplayer, get_amount_minions(fplayer))
        # for e in g.entities:
        #     print(e)
        # print(eplayer, get_amount_minions(eplayer))
        # print("Minios {:<20}: {}".format(fplayer, get_amount_minions(fplayer)))
        # print("Minios {:<20}: {}".format(eplayer, get_amount_minions(eplayer)))
        # print("HeroPower {:<20}: {}".format(fplayer, get_heropower_active(fplayer)))
        # print("HeroPower {:<20}: {}".format(eplayer, get_heropower_active(eplayer)))
    else:
        print('Log not found')


if __name__ == '__main__':
    main()
