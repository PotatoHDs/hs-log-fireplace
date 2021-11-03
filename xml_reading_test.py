from hsreplay.document import HSReplayDocument
import json
import os
from io import BytesIO
from hslog.export import EntityTreeExporter


def get_file_paths(path):
    for root, _, files in os.walk(path):
        for filename in files:
            yield os.path.join(root, filename)
    # for root, dirs, files in os.walk(path):
    #     for name in files:
    #         print
    #         os.path.join(root, name)


def get_games(games_dir):
    for filename in get_file_paths(games_dir):
        with open(filename) as f:
            game = json.load(f)
            game['game'] = HSReplayDocument.from_xml_file(BytesIO(game['xml'].encode("utf-8")))
            del game['xml']
            game['id'] = os.path.basename(filename).split('.')[0]
            yield game


def get_games_dict(games_dir):
    res = {}
    for game in get_games(games_dir):
        game_id = game['id']
        del game['id']
        res[game_id] = game
    return res


# def import_data():
#     res = list(get_data())


def main():
    game = next(get_games(r'D:\datasets and shit\hs_games'))
    # print(game['game'].nodes)
    # print('\n\n\n')

    # packet_tree = game['game'].to_packet_tree()
    # p = LogParser()
    game = game['game'].to_packet_tree()[0]
    # p.
    print(game.export())
    # for node in game['game'].nodes:
    #     print(vars(node))
    #     print()
    # print([vars(node) for node in game['game'].nodes])
    # print(game)
    # print(game)
    # games = list(get_games(r'C:\Users\kmv026\Documents\GitHub\hs-log-fireplace\example data'))
    # game = games[0]
    # print(vars(game['game']))
    # print(vars(game['game'].nodes[0].nodes[0]))


if __name__ == '__main__':
    main()
