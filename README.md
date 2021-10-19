# Braille Apple

[Bad Apple](https://www.youtube.com/watch?v=FtutLA63Cp8) rendered from the
terminal using [braille patterns](https://en.wikipedia.org/wiki/Braille_Patterns).

See a side by side comparison of Bad Apple and Braille Apple
[**-->here<--**](https://vimeo.com/636580388)!

## Dependencies
```sh
$ apt-get install python3 python3-pil black flake8 ffmpeg youtube-dl
```

## Usage
Running `make main` will download Bad Apple from YouTube using `youtube-dl`,
split the video into individual frames using `ffmpeg`, and then begin rendering
frames of the video converted to braille-art in real time at 30 FPS. Subsequent
runs of the `main` target will use the cached MP4 and frame PNGs if they were
successfully downloaded / produced.

```sh
$ make main
```
