.POSIX:
.PHONY: all lint format clean

all: frames lint format

bad-apple.mp4:
	youtube-dl -o $@ -f 'best[ext=mp4]' https://youtu.be/FtutLA63Cp8

frames: bad-apple.mp4
	mkdir -p frames
	ffmpeg -i bad-apple.mp4 \
		-r $$(ffprobe -v 0 -of csv=p=0 -select_streams v:0 -show_entries stream=r_frame_rate bad-apple.mp4) \
		-s $$(ffprobe -v error -select_streams v -show_entries stream=width,height -of csv=p=0:s=x bad-apple.mp4) \
		-f image2 frames/frame-%04d.png
	python3 convert.py frames

# Flake8 Ignored Errors:
#   E203 - Conflicts with black.
#   E221 - Disabled for manual vertically-aligned code.
#   E241 - Disabled for manual vertically-aligned code.
#   W503 - Conflicts with black.
lint:
	python3 -m mypy *.py
	python3 -m flake8 *.py --ignore=E203,E221,E241,W503

format:
	python3 -m black *.py --line-length 79

clean:
	rm -rf frames
	rm -rf __pycache__
	rm -rf .mypy_cache

fresh: clean
	rm *.mp4
