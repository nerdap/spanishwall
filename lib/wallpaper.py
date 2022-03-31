import os
import random
from PIL import Image, ImageDraw, ImageFont
from . import config

def _get_filepath(dictionary_entry):
    rand = random.randint(0, 1000000000)
    return f'{config.WALLS_DIR}/{dictionary_entry.word}_{rand}.jpg'

def _draw_column(draw, font_normal, font_bold, x, y, col):
    for i, val in enumerate(col):
        if i == 0:
            font = font_bold
        else:
            font = font_normal
        draw.text((x, y + i*100), val, font=font, fill='black')

def _draw_conjugations(draw, font_normal, font_bold, start_x, start_y, conjs):
    if len(conjs) == 0:
        return

    _draw_column(
        draw=draw,
        font_normal=font_bold,
        font_bold=font_bold,
        x=start_x,
        y=start_y,
        col=['Form', 'Yo', 'Tú', 'El', 'Nosotros', 'Ellos'],
    )
    offset = 0
    for conj_name, conj in conjs:
        _draw_column(
            draw=draw,
            font_normal=font_normal,
            font_bold=font_bold,
            x=start_x + 300 + offset*500,
            y=start_y,
            col=[
                conj_name,
                conj.yo,
                conj.tu,
                conj.el,
                conj.nosotros,
                conj.ellos,
            ],
        )
        offset += 1

def _draw_text(img, dictionary_entry):
    d = ImageDraw.Draw(img)
    font_big = ImageFont.truetype(config.FONT_PATH_NORMAL, size=150)
    font_mid = ImageFont.truetype(config.FONT_PATH_NORMAL, size=100)
    font_small = ImageFont.truetype(config.FONT_PATH_NORMAL, size=50)
    font_small_bold = ImageFont.truetype(config.FONT_PATH_BOLD, size=50)
    d.text((250,250), dictionary_entry.word, font=font_big, fill='black')
    d.text((250,500), dictionary_entry.definition, font=font_mid, fill='black')
    d.text((1500, 350), 'Example: ', font=font_small_bold, fill='black')
    if dictionary_entry.example is not None:
        d.text(
            (1500, 450),
            dictionary_entry.example[0],
            font=font_small,
            fill='black',
        )
        d.text(
            (1500, 550),
            dictionary_entry.example[1],
            font=font_small,
            fill='black',
        )
    _draw_conjugations(
        draw=d,
        font_normal=font_small,
        font_bold=font_small_bold,
        start_x=250, 
        start_y=750,
        conjs=dictionary_entry.conjugations,
    )

def create_text_wallpaper(dictionary_entry):
    img = Image.new(
        'RGB',
        (config.WALL_WIDTH, config.WALL_HEIGHT),
        color='white',
    )
    _draw_text(img, dictionary_entry)
    img.save(_get_filepath(dictionary_entry))