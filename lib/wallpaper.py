import os
import random
from PIL import Image, ImageDraw, ImageFont

WALL_WIDTH = 2736
WALL_HEIGHT = 1834
WALLS_DIR =  os.path.realpath('walls/')
FONT_PATH = 'C:\\Windows\\Fonts\\Arial.ttf'

def _get_filepath(dictionary_entry):
    rand = random.randint(0, 1000000000)
    return f'{WALLS_DIR}/{dictionary_entry.word}_{rand}.jpg'

def _make_conjugations_table(conjugations):
    table = []
    for conjugation in conjugations:
        row = []
        for verb in conjugation:
            row.append(verb)
        table.append(row)
    return table

def _draw_text(img, dictionary_entry):
    d = ImageDraw.Draw(img)
    font_big = ImageFont.truetype(FONT_PATH, size =150)
    font_mid = ImageFont.truetype(FONT_PATH, size=100)
    font_small = ImageFont.truetype(FONT_PATH, size=50)
    d.text((250,250), dictionary_entry.word, font=font_big, fill='black')
    d.text((250,500), dictionary_entry.definition, font=font_mid, fill='black')
    d.text(
        (250,800),
        str(dictionary_entry.conjugations),
        font=font_small,
        fill='black',
    )

def create_text_wallpaper(dictionary_entry):
    img = Image.new('RGB', (WALL_WIDTH, WALL_HEIGHT), color='white')
    _draw_text(img, dictionary_entry)
    img.save(_get_filepath(dictionary_entry))