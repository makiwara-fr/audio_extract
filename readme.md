# Audio extract 

Batch extract part of multiple audio files


## Build

See [build.md](build.md)

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




### Parameters

#### input_dir

It should contain files you wish to extract audio excerpt from.

default is: current working directory.

#### output_dir

It will contain all extractions. New file will be mp3 format with format **original_file_name_extract.mp3**

default is: ./output/

#### first_second

Indicate what is the first second of the stream you wish to extract

default is: 0

#### last_second

Indicate what is the last second of the stream you wish to extract

default is: 60

#### input_file_extension: 
A list of file extension you want to consider 

default is: [mp3, wav]

### path_ffmpeg [optional]
directory where is located FFMPEG if not in PATH. Should end with ... ffmpeg/bin

### debug [optional]
enable debug. Default is False
