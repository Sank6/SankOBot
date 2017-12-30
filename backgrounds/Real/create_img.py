from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import requests
from io import BytesIO


def get_picture(name, level, messages, credits, time, choice, xp, url):
    font_name = "./main.ttf"
    title_font = "./title.ttf"
    foreground = Image.open("./bg.png").convert("RGBA")
    background = Image.open("/" + str(choice) + ".png").convert("RGBA")

    together = Image.new('RGBA', (500, 500), (0, 0, 0, 0))
    together.paste(background, (0, 0))
    together.paste(foreground, (0, 0), mask=foreground)
    together.save("./together.png", format="png")

    # xp
    if int(xp) == 0:
        x = 45
    else:
        x = 45 + (420/(100/int(xp)))
    rectangle = Image.new('RGBA', (500, 500), (0, 0, 0, 0))
    rectangle_ = ImageDraw.Draw(rectangle)
    rectangle_.rectangle([86, 225, x, 287], fill=(100, 100, 100, 255), outline=None)
    rectangle.save("./rect.png", format="png")

    foreground = Image.open("./rect.png").convert("RGBA")
    background = Image.open("./together.png").convert("RGBA")

    together2 = Image.new('RGBA', (500, 500), (0, 0, 0, 0))
    together2.paste(background, (0, 0))
    together2.paste(foreground, (0, 0), mask=foreground)
    together2.save("./together2.png", format="png")

    # add level background

    foreground = Image.open("./level.png").convert("RGBA")
    background = Image.open("./together2.png").convert("RGBA")

    together3 = Image.new('RGBA', (500, 500), (0, 0, 0, 0))
    together3.paste(background, (0, 0))
    together3.paste(foreground, (0, 0), mask=foreground)
    together3.save("./together3.png", format="png")

    # ADD LOGO
    response = requests.get(url)
    foreground = Image.open(BytesIO(response.content))
    foreground.thumbnail((80, 80))
    old_size = foreground.size

    new_size = (90, 90)
    new_im = Image.new("RGB", new_size)
    new_im.paste(foreground, (int((new_size[0] - old_size[0]) / 2), int((new_size[1] - old_size[1]) / 2)))

    bg = Image.open("./together3.png").convert("RGBA")

    bg.paste(new_im , (40, 40))
    bg.save("./together3.png")

    #
    # add text
    result = Image.open("./together3.png")
    draw = ImageDraw.Draw(result)
    text = name
    if len(text) < 15:
        size = 50
    else:
        size = 50 - (len(text) - 15)
    font = ImageFont.truetype(title_font, size)
    draw.text((120, 220), text, (255, 255, 255), font=font)

    if level == 10 or level == '10':
        font = ImageFont.truetype(title_font, 50)
        draw.text((30, 220), str(level), (255, 255, 255), font=font)
    else:
        font = ImageFont.truetype(title_font, 50)
        draw.text((40, 220), str(level), (255, 255, 255), font=font)

    font_size = 30

    text = "Credits:   $" + str(credits)
    font = ImageFont.truetype(font_name, font_size)
    draw.text((40, 340), text, (0, 0, 0), font=font)

    text = str(time)
    font = ImageFont.truetype(font_name, font_size - 10)
    draw.text((250, 340), text, (0, 0, 0), font=font)

    text = "Total XP: " + str(messages)
    font = ImageFont.truetype(font_name, font_size)
    draw.text((40, 380), text, (0, 0, 0), font=font)

    text = "Level:        " + str(level)
    font = ImageFont.truetype(font_name, font_size)
    draw.text((40, 420), text, (0, 0, 0), font=font)

    result.save("./result.png", format="png")
