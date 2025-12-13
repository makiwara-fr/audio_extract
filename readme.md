[![Testing commit](https://github.com/makiwara-fr/audio_extract/actions/workflows/makefile.yml/badge.svg?branch=main)](https://github.com/makiwara-fr/audio_extract/actions/workflows/makefile.yml)

# Audio extract 

Batch extract part of multiple audio files
It's a wrapper around FFMPEG.
Give these guys a thumbs up !
[https://www.ffmpeg.org/](https://www.ffmpeg.org/)

## Build

See [build.md](docs/build.md)

## installation 

### prerequisites

* ffmpeg installed
* python installed
* download and install the wheel file for CLI or gui-x.x.x. from here [https://github.com/makiwara-fr/extract_audio_exercept/releases/latest]

## How to - Graphical interface

* Download `audio_extract.exe` from here [https://github.com/makiwara-fr/extract_audio_exercept/releases/latest]
* Put it where ever you want
* click on the file to launch it

## How to - CLI 

### installation

```pip install batch-audio-extract```

After installing, the wheel.

In any working directory, create a file *parameters.yaml* (see example below). If undefined, default parameters will apply.

```
input_dir: input
output_dir: output
first_second: 0
last_second: 120
input_file_extension: [mp3, wav]
```

Then launch command in a terminal, in the directory of the *parameters.yaml* file

```
audio_extract
```

see more with

        audio_extract --help




### Parameters for *parameters.yaml*


| Parameter              | Description                                                                                              | Default Value        |
| ---------------------- | -------------------------------------------------------------------------------------------------------- | -------------------- |
| `input_dir`            | The directory containing the audio files you want to process.                                            | Current directory    |
| `output_dir`           | The directory where the extracted audio clips will be saved. The output format is `original_filename_extract.mp3`. | `./output/`          |
| `first_second`         | The start time (in seconds) for the audio extraction.                                                    | `0`                  |
| `last_second`          | The end time (in seconds) for the audio extraction.                                                      | `60`                 |
| `input_file_extension` | A list of file extensions to be considered for processing.                                               | `[mp3, wav]`         |
| `path_ffmpeg` (optional) | The path to the FFMPEG `bin` directory if it's not in your system's PATH.                                | Not set              |
| `debug` (optional)     | Enables debug mode for more verbose output.                                                              | `False`              |

### Parameters for CLI

All parameters from the `parameters.yaml` file can be overridden via command-line arguments.

| Argument          | Description                                  | Corresponding `yaml` parameter |
| ----------------- | -------------------------------------------- | ------------------------------ |
| `-d`, `--debug`   | Enable debug mode.                           | `debug`                        |
| `-i`, `--input`   | Input directory containing audio files.      | `input_dir`                    |
| `-o`, `--output`  | Output directory for extracted audio files.  | `output_dir`                   |
| `-s`, `--start`   | Starting second for the audio excerpt.       | `first_second`                 |
| `-e`, `--end`     | Ending second for the audio excerpt.         | `last_second`                  |
| `-f`, `--fade`    | Fade duration in seconds (0 for no fade).    | `fade_d`                       |

#### Examples

*   Extract the first 30 seconds of all audio files in the `my_audio` directory and save them to `my_extracts`:

    ```bash
    audio_extract --input my_audio --output my_extracts --start 0 --end 30
    ```

*   Extract audio from second 60 to 120 with a 3-second fade in/out:

    ```bash
    audio_extract --start 60 --end 120 --fade 3
    ```

*   Run in debug mode using a custom input directory:

    ```bash
    audio_extract --debug --input /path/to/your/audio
    ```
