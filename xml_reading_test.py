from hsreplay.document import HSReplayDocument
import json
import os
from io import StringIO, BytesIO


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
            game['game'] = HSReplayDocument.from_xml_file(BytesIO(game['xml'].encode("utf-8"))).games[0]
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
    for data in get_games(r'C:\Users\kmv026\Documents\GitHub\hs-log-fireplace\example data'):
        print(data)


if __name__ == '__main__':
    main()
