import argparse
import os
import re
import requests
from io import BytesIO
from PIL import Image

CARD_HEIGHT = 370
CARD_WIDTH = 265
CARD_MARGIN = 1
CANVAS_WIDTH = CARD_MARGIN * 4 + CARD_WIDTH * 3
CANVAS_HEIGHT = CARD_MARGIN * 4 + CARD_HEIGHT * 3
CARDS_PER_CANVAS = 9


def parse_general_form_cardname(general_form_cardname):
    splitted = general_form_cardname.split(' // ')
    if len(splitted) == 1:
        ja, en = splitted[0].replace('《', '').replace('》', '').split('/')
        return {'ja': ja, 'en': en}
    if len(splitted) == 2:
        ja0, en0 = splitted[0].replace('《', '').replace('》', '').split('/')
        ja1, en1 = splitted[1].replace('《', '').replace('》', '').split('/')
        return {'ja': '{}+{}'.format(ja0, ja1), 'en': '{} // {}'.format(en0, en1)}
    else:
        raise ValueError(general_form_cardname)


DATA_DIR = './data/'
CARD_URL_INFO = {}
for data_file in os.listdir(DATA_DIR):
    with open(os.path.join(DATA_DIR, data_file), 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            url, general_form_cardname = line.replace('\n', '').split('\t')
            cardname = parse_general_form_cardname(general_form_cardname)
            CARD_URL_INFO[cardname['en']] = url


DOUBLE_FACED_DICT = {
    "Legion's Landing": "Adanto, the First Fort",
    "Search for Azcanta": "Azcanta, the Sunken Ruin",
    "Arguel's Blood Fast": "Temple of Aclazotz",
    "Vance's Blasting Cannons": "Spitfire Bastion",
    "Growing Rites of Itlimoc": "Itlimoc, Cradle of the Sun",
    "Conqueror's Galleon": "Conqueror's Foothold",
    "Dowsing Dagger": "Lost Vale",
    "Primal Amulet": "Primal Wellspring",
    "Thaumatic Compass": "Spires of Orazca",
    "Treasure Map": "Treasure Cove",
    "Hadana's Climb": "Winged Temple of Orazca",
    "Journey to Eternity": "Atzal, Cave of Eternity",
    "Path of Mettle": "Metzali, Tower of Triumph",
    "Profane Procession": "Tomb of the Dusk Rose",
    "Storm the Vault": "Vault of Catlacan",
    "Azor's Gateway": "Sanctum of the Sun",
    "Golden Guardian": "Gold-Forge Garrison",
    "Nicol Bolas, the Ravager": "Nicol Bolas, the Arisen",
}


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('decklist_path')
    return parser.parse_args()


def get_decklist_lines(decklist_path: str) -> list:
    decklist_lines = []
    with open(decklist_path, 'r') as f:
        while True:
            line = f.readline()
            if re.match('^[0-9]+', line):
                decklist_lines.append(line.replace('\n', ''))
            if not line:
                break
    return decklist_lines


def get_cardnames_and_nums(decklist_lines: list) -> list:
    cardnames_and_nums = []
    for decklist_line in decklist_lines:
        splitted = decklist_line.split(' ')
        num = splitted[0]
        cardname = ' '.join(splitted[1:])
        cardnames_and_nums.append({'num': num, 'cardname': cardname})
    return cardnames_and_nums


def get_url_from_cardname(cardname: str) -> str:
    return CARD_URL_INFO[cardname]

def get_image_object_from_cardname(cardname: str) -> Image:
    url = get_url_from_cardname(cardname)
    response = requests.get(url)
    image = Image.open(BytesIO(response.content))

    # 分割カードの場合は90度左に回転したものを印刷リストに入れる
    if '//' in cardname:
        image = image.resize((image.width, image.width))
        image = image.rotate(90)

    return image.resize((CARD_WIDTH, CARD_HEIGHT))


def create_images(cardnames_and_nums: list) -> list:
    cards_list = []
    for item in cardnames_and_nums:
        num = int(item['num'])
        cardname = item['cardname']
        image = get_image_object_from_cardname(cardname)
        cards_list += [image] * num

        # 両面カードの場合は指定の名前をもつ2つの画像（表・裏）を印刷リストに入れる
        if cardname in DOUBLE_FACED_DICT.keys():
            image = get_image_object_from_cardname(DOUBLE_FACED_DICT[cardname])
            cards_list += [image] * num

    # cards_list を CARDS_PER_CANVAS の倍数に調節
    num_white_card_addition = CARDS_PER_CANVAS - len(cards_list) % CARDS_PER_CANVAS
    cards_list += [Image.new('RGB', (CARD_WIDTH, CARD_HEIGHT), (255, 255, 255))] * num_white_card_addition

    for canvas_number in range(len(cards_list) // CARDS_PER_CANVAS):
        canvas = Image.new('RGB', (CANVAS_WIDTH, CANVAS_HEIGHT), (255, 255, 255))
        for i in range(3):
            for j in range(3):
                image = cards_list[canvas_number * CARDS_PER_CANVAS + i * 3 + j]
                canvas.paste(image, (CARD_MARGIN * (j + 1) + CARD_WIDTH * j, CARD_MARGIN * (i + 1) + CARD_HEIGHT * i))
        canvas.save('output/o{}.jpg'.format(canvas_number), 'JPEG', quality=100, optimize=True)


if __name__ == '__main__':
    args = parse_args()
    decklist_lines = get_decklist_lines(args.decklist_path)
    cardnames_and_nums = get_cardnames_and_nums(decklist_lines)
    images = create_images(cardnames_and_nums)
