# This is a sample Python script.
import json
import os.path
import time
import urllib
import requests

# iron_maiden_songs_clean = []
headers = {'User-Agent': 'my-app/0.0.1'}
# with open('iron_maiden_songs.csv', newline='') as f:
#     reader = csv.reader(f)
#     iron_maiden_songs = list(reader)
# iron_maiden_songs = sum(iron_maiden_songs, [])
# for song in iron_maiden_songs:
#     if song.startswith('The'):
#         song = ''.join(song.split()[1:])
#     iron_maiden_songs_clean.append(song.split('(')[0])
#
# print(f"{iron_maiden_songs_clean=}")


def run_search(search_text_list: list):
    url_search_text = [urllib.parse.quote(search_text, safe='/', encoding=None, errors=None) + '+' for search_text in search_text_list]
    url_search_text = ''.join(url_search_text)
    url_search_text = url_search_text[:len(url_search_text)-1]
    print(url_search_text)

    x = requests.get(f'https://api.scryfall.com/cards/search?q={url_search_text}', headers=headers)
    x_dict = json.loads(x.text)
    if 'code' in x_dict and x_dict['code'] == 'not_found':
        print('No card found')
        return

    try:
        x_dict['data']
    except KeyError:
        print('No card found')
        print(f"{x_dict=}")

    for card in x_dict['data']:
        print(card['name'], card['scryfall_uri'])


def run_search_ark_export(card_list: list):
    all_data = []

    for card in card_list:
        print(f"Finding card: {card}")
        card_info = card.split()
        print(f"{card_info=}")
        if any("^Have" in info for info in card_info):
            print("I already own this card! Skipping... ")
            continue

        for ind in range(len(card_info)):
            if '(' in card_info[ind] and ')' in card_info[ind]:
                set_ind = ind
        card_name = '!\"' + ''.join([card_info[i] + ' ' for i in range(1, set_ind)])[:-1] + "\""
        card_set = 'set:' + card_info[set_ind][1:-1]
        card_number = 'number:' + "\"" + card_info[set_ind+1] + "\""

        search_text_list = [card_name, card_set, card_number]

        url_search_text = [urllib.parse.quote(search_text, safe='/', encoding=None, errors=None) + '+' for search_text in search_text_list]
        url_search_text = ''.join(url_search_text)
        url_search_text = url_search_text[:len(url_search_text)-1]

        x = requests.get(f'https://api.scryfall.com/cards/search?q={url_search_text}', headers=headers)
        x_dict = json.loads(x.text)
        if 'code' in x_dict and x_dict['code'] == 'not_found':
            print('No card found')
            return

        try:
            x_dict['data']
        except KeyError:
            print('No card found')
            print(f"{x_dict=}")

        all_data.append(x_dict['data'])
        time.sleep(1)  # Due to API request rate

    return all_data


def load_card_data(file_name):
    with open(file_name, 'r') as file:
        data = file.read().splitlines()
    print(f"{data=}")
    return data


def save_to_png(card_data_scryfall, save_path):
    save_file_name = os.path.join(save_path, card_data_scryfall['name'] + '.png')
    with open(save_file_name, 'wb') as file:
        pic = requests.get(card_data_scryfall['image_uris']['png'], stream=True, headers=headers)

        for block in pic.iter_content(1024):
            file.write(block)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # for song in iron_maiden_songs_clean:
    #     print(song)
    #     run_search([song, 'id<=grixis'])
    cards = load_card_data(r'C:\Users\ddb29996\Downloads\thin_line_between_love_and_hate.txt')
    card_data_scryfall = run_search_ark_export(cards)
    print(f"{card_data_scryfall=}")
    for card_data in card_data_scryfall:
        print(f"{card_data[0]=}")
        save_to_png(card_data[0], r'C:\Users\ddb29996\scryfall_python\card_output\\')

