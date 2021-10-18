#!/usr/bin/env python3

from pathlib import Path
import argparse
import time

from PIL import Image  # type: ignore

# Unicode Braille Patterns
# ========================
# https://en.wikipedia.org/wiki/Braille_Patterns
# https://www.unicode.org/charts/PDF/U2800.pdf
#
#
#        | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | A | B | C | D | E | F
# U+280x | ⠀ | ⠁ | ⠂ | ⠃ | ⠄ | ⠅ | ⠆ | ⠇ | ⠈ | ⠉ | ⠊ | ⠋ | ⠌ | ⠍ | ⠎ | ⠏
# U+281x | ⠐ | ⠑ | ⠒ | ⠓ | ⠔ | ⠕ | ⠖ | ⠗ | ⠘ | ⠙ | ⠚ | ⠛ | ⠜ | ⠝ | ⠞ | ⠟
# U+282x | ⠠ | ⠡ | ⠢ | ⠣ | ⠤ | ⠥ | ⠦ | ⠧ | ⠨ | ⠩ | ⠪ | ⠫ | ⠬ | ⠭ | ⠮ | ⠯
# U+283x | ⠰ | ⠱ | ⠲ | ⠳ | ⠴ | ⠵ | ⠶ | ⠷ | ⠸ | ⠹ | ⠺ | ⠻ | ⠼ | ⠽ | ⠾ | ⠿
# U+284x | ⡀ | ⡁ | ⡂ | ⡃ | ⡄ | ⡅ | ⡆ | ⡇ | ⡈ | ⡉ | ⡊ | ⡋ | ⡌ | ⡍ | ⡎ | ⡏
# U+285x | ⡐ | ⡑ | ⡒ | ⡓ | ⡔ | ⡕ | ⡖ | ⡗ | ⡘ | ⡙ | ⡚ | ⡛ | ⡜ | ⡝ | ⡞ | ⡟
# U+286x | ⡠ | ⡡ | ⡢ | ⡣ | ⡤ | ⡥ | ⡦ | ⡧ | ⡨ | ⡩ | ⡪ | ⡫ | ⡬ | ⡭ | ⡮ | ⡯
# U+287x | ⡰ | ⡱ | ⡲ | ⡳ | ⡴ | ⡵ | ⡶ | ⡷ | ⡸ | ⡹ | ⡺ | ⡻ | ⡼ | ⡽ | ⡾ | ⡿
# U+288x | ⢀ | ⢁ | ⢂ | ⢃ | ⢄ | ⢅ | ⢆ | ⢇ | ⢈ | ⢉ | ⢊ | ⢋ | ⢌ | ⢍ | ⢎ | ⢏
# U+289x | ⢐ | ⢑ | ⢒ | ⢓ | ⢔ | ⢕ | ⢖ | ⢗ | ⢘ | ⢙ | ⢚ | ⢛ | ⢜ | ⢝ | ⢞ | ⢟
# U+28Ax | ⢠ | ⢡ | ⢢ | ⢣ | ⢤ | ⢥ | ⢦ | ⢧ | ⢨ | ⢩ | ⢪ | ⢫ | ⢬ | ⢭ | ⢮ | ⢯
# U+28Bx | ⢰ | ⢱ | ⢲ | ⢳ | ⢴ | ⢵ | ⢶ | ⢷ | ⢸ | ⢹ | ⢺ | ⢻ | ⢼ | ⢽ | ⢾ | ⢿
# U+28Cx | ⣀ | ⣁ | ⣂ | ⣃ | ⣄ | ⣅ | ⣆ | ⣇ | ⣈ | ⣉ | ⣊ | ⣋ | ⣌ | ⣍ | ⣎ | ⣏
# U+28Dx | ⣐ | ⣑ | ⣒ | ⣓ | ⣔ | ⣕ | ⣖ | ⣗ | ⣘ | ⣙ | ⣚ | ⣛ | ⣜ | ⣝ | ⣞ | ⣟
# U+28Ex | ⣠ | ⣡ | ⣢ | ⣣ | ⣤ | ⣥ | ⣦ | ⣧ | ⣨ | ⣩ | ⣪ | ⣫ | ⣬ | ⣭ | ⣮ | ⣯
# U+28Fx | ⣰ | ⣱ | ⣲ | ⣳ | ⣴ | ⣵ | ⣶ | ⣷ | ⣸ | ⣹ | ⣺ | ⣻ | ⣼ | ⣽ | ⣾ | ⣿
#
#
# Dot Numbering:
#  1 4
#  2 3
#  3 6
#  7 8
#
#
# Dots | 87654321 | Hex
# -----+----------+----
#  x x | 00000000 | 00
#  x x |          |
#  x x |          |
#  x x |          |
# -----+----------+----
#  1 1 | 00001001 | 09
#  x x |          |
#  x x |          |
#  x x |          |
# -----+----------+----
#  1 1 | 11001001 | C9
#  x x |          |
#  x x |          |
#  1 1 |          |
# -----+----------+----
#  1 x | 10010101 | 95
#  x 1 |          |
#  1 x |          |
#  x 1 |          |


def image_to_braille(path, width=160, height=120):
    img = Image.open(path)
    img = img.convert("1")  # 1-bit color (a.k.a black & white)
    img = img.resize((width, height))
    #img.save("out.png")

    s = chr(27) + "[2J"
    for y in range(0, img.height, 4):
        for x in range(0, img.width, 2):
            bits = 0b00000000
            if img.getpixel((x + 0, y + 0)) != 0:
                bits |= 0b00000001
            if img.getpixel((x + 0, y + 1)) != 0:
                bits |= 0b00000010
            if img.getpixel((x + 0, y + 2)) != 0:
                bits |= 0b00000100
            if img.getpixel((x + 1, y + 0)) != 0:
                bits |= 0b00001000
            if img.getpixel((x + 1, y + 1)) != 0:
                bits |= 0b00010000
            if img.getpixel((x + 1, y + 2)) != 0:
                bits |= 0b00100000
            if img.getpixel((x + 0, y + 3)) != 0:
                bits |= 0b01000000
            if img.getpixel((x + 1, y + 3)) != 0:
                bits |= 0b10000000
            s += chr(0x2800 | bits)
        s += "\n"
    print(s, end="\n")



def main():
    parser = argparse.ArgumentParser(
        description="Transform PNGs in DIRECTORY from RGB into black & white."
    )
    parser.add_argument("directory", metavar="DIRECTORY", type=str)
    args = parser.parse_args()
    #image_to_braille(sorted(Path(args.directory).glob("*.png"))[5770])

    FPS=30
    accum = 0
    time.sleep(0.15) # for demo
    def next_frame():
        nonlocal accum
        start = time.time()
        while (time.time() - start) + accum < 1/FPS:
            time.sleep(0.001)
        #print(frame, f"ACCUM: {accum}")
        image_to_braille(frame)
        accum += time.time() - start - 1/FPS

    frames = sorted(Path(args.directory).glob("*.png"))
    for frame in frames:
        next_frame()


if __name__ == "__main__":
    main()
