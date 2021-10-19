#!/usr/bin/env python3

from pathlib import Path
import argparse
import time

from PIL import Image

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
    ESC = chr(27)  # ANSI ESC
    s = f"{ESC}[H{ESC}[2J"  # HOME; CLEAR SCREEN
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
    return s


def main():
    parser = argparse.ArgumentParser(
        description="Transform PNGs in DIRECTORY from RGB into black & white."
    )
    parser.add_argument("directory", metavar="DIRECTORY", type=str)
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()

    # Bad Apple is 30 FPS. To make this script work with any arbitrary video
    # the FPS of the video would need to be explicitly passed as a program
    # argument. For the purposes of this mini-project this is a WONTFIX.
    FPS = 30
    SPF = 1 / FPS
    # Time accumulator. For each frame rendered, 1 / FPS is subtracted from the
    # accumulator and the time to execute the frame-rendering logic is added to
    # the accumulator. Draw calls are only permitting once every 1 / FPS
    # seconds, and any excess time is captured in the new value of the
    # accumulator. This systems leads to a semi-stable frame rate without
    # having to worry about de-sync.
    accumulator = 0

    def next_frame(frame, accumulator):
        start = time.time()
        braille = image_to_braille(frame)
        # Wait until 1 / FPS seconds have elapsed since the last frame render.
        while accumulator + (time.time() - start) < SPF:
            time.sleep(0.001)
        # Perform draw calls.
        print(braille, end="")
        if args.debug:
            print(f"Current Frame: {frame}")
            print(f"Accumulator: {accumulator:.5f}")
        # Return the new value of the accumulator.
        return accumulator + (time.time() - start) - SPF

    for frame in sorted(Path(args.directory).glob("*.png")):
        accumulator = next_frame(frame, accumulator)


if __name__ == "__main__":
    main()
