import pprint

from hslog import LogParser

from hslog.export import EntityTreeExporter, FriendlyPlayerExporter
import platform

from pathlib import Path
from string import ascii_uppercase, ascii_lowercase

from hearthstone.enums import CardType, GameTag, Zone

pp = pprint.PrettyPrinter(depth=6)
pp = pp.pprint

# for line in tailer.follow(open(
# '/home/dee/.PlayOnLinux/wineprefix/hs/drive_c/Program Files/Hearthstone/Logs/Power.log'), 0):
#     print(line)
global g, fplayer, eplayer
p = LogParser()
system = platform.system()
hs_path = None
if system == 'Darwin':
    hs_path = Path('/') / 'Applications' / 'Hearthstone' / 'Logs' / 'Power.log'
elif system == 'Windows':
    for Disk in ascii_uppercase:
        hs_path = Path(f'{Disk}:\\') / 'Program Files (x86)' / 'Hearthstone' / 'Logs' / 'Power.log'
        if hs_path.exists():
            break
elif system == 'Linux':
    if 'Microsoft' in platform.release():
        for Disk in ascii_lowercase:
            hs_path = Path('/') / 'mnt' / Disk / 'Program Files (x86)' / 'Hearthstone' / 'Logs' / 'Power.log'
            if hs_path.exists():
                break


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
            print()
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
            print(e.__dict__)
            # return True if e.tags[GameTag.EXHAUSTED] == 0 else False


def main():
    if hs_path is not None and hs_path.exists():
        reload()
        # print(fplayer.player_id)
        get_hand_events(fplayer)
        get_heropower_active(fplayer)
        get_amount_minions(fplayer)
        get_amount_minions(fplayer)
        # for key, value in p.games[-1].export().__dict__.items():
        #     print(key, value)
        exporter = EntityTreeExporter(p.games[-1])
        what = exporter.export()

        # print(p.games[-1].__dict__)
        print(fplayer.__dict__)
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
