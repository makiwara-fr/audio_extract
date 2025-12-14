import sys
import re
import os
from pathlib import Path
import yaml
from yaml.loader import SafeLoader

from batch_audio_extract.welcome import message
from batch_audio_extract.ffmpeg import get_ffmpeg_path, check_ffmpeg



def set_regexp(suffix_list):
    """set the regex to look for audio files"""
    regexp = ""
    for suf in suffix_list:
        if regexp == "":
            regexp += f"({suf}"
        else:
            regexp += f"|{suf}"
    # finalize the string if not empty
    if regexp != "":
        regexp += f")"
        return re.compile(regexp)
    else:
        return None


def scan_folder(wd: Path, regexp):
    """scan folder for files mathcing regexp"""

    if type(wd) == str:
        wd = Path(wd)

    if not wd.exists():
        print(wd, "doesn't exist")
        return []


    files_list = []

    # Scanning folder
    print(f"Scanning folder : {wd}")

    

    # if wd == ".":
    #     wd = os.getcwd()

    # scanning all the files  #for entry in os.scandir(wd):
    for entry in wd.iterdir():
        if entry.is_file():
            # recognize if audio
            if regexp.search(entry.name):
                # print(entry.name)
                files_list.append(entry)
        else:
            # don't go into subdirectories
            pass

    return files_list


def extract(file: Path, output_dir: Path, beg: int, end: int, ffmpeg_path: Path)->int:
    """extract except from given file and put results in output dir taking audio only for beg to end
    
        returns:
            - status of FFMpeg extraction
            - 1 if error
    """
    
    
    # infile = Path.cwd().joinpath(file)
    print(f"Processing {file}")
    print()
    # outfile = Path.cwd().joinpath(output_dir, file.stem + "_extract.mp3")
    outfile = output_dir.joinpath(file.stem + "_extract.mp3")

    infile = file

    try:
        # reencode if not MP3 file
        if infile.suffix != ".mp3":
            print("not mp3", infile.suffix)
            reencode = " -codec:a libmp3lame "
        else:
            reencode = ""

        # command = f"ffmpeg -i \"{infile}\" -ss {beg} -to {end}  -af \"afade=t=out:st={end-5}:d=5\" {reencode} -y \"{outfile}\""
        command = f'{ffmpeg_path} -i "{infile}" -ss {beg} -to {end}  -af "afade=t=out:st={end-5}:d=5" {reencode} -y "{outfile}"'

        status = os.system(command)
        return status

    except Exception as e:
        print(e)
        return 1


def process(input_params=None):
    
    # Welcome messages
    message()

    # print(input_params)

    if input_params != None:  # input parameters are given probably from Gui
        params = {}
        for k, v in input_params.items():
            params[k] = v

    else:  # Open the config file and load the file
        try:
            with open("parameters.yaml") as f:
                params = yaml.load(f, Loader=SafeLoader)
        except:
            # not file found
            params = {}

    # print(params)

    # list of default parameters
    default_params = {
        "input_dir": Path("./"),
        "output_dir": Path("./output"),
        "first_second": 0,
        "last_second": 60,
        "input_file_extension": ["wav", "mp3"],
        "path_ffmpeg": "",
        "debug": False,
        "fade_d": 8,
    }

    # check quality of parameters
    for k, v in default_params.items():
        if k not in params:
            print(f"{k} is defaulted")
            params[k] = default_params[k]

    debug = params["debug"]

    print(params)

    # read input files
    # ----------------
    if debug:
        print(f"Working directory is {Path.cwd()}")

    regex = set_regexp(
        params["input_file_extension"]
    )  # list of extension to look for in directory

    files_list = scan_folder(params["input_dir"], regex)  # scanning the input directory
    if debug:
        if len(files_list) > 0:
            print(f"found {len(files_list)} files")
            print()
        else:
            print()
            print("Exiting: no file has been found")
            print("")
            sys.exit(0)

    end = params["last_second"]
    beg = params["first_second"]
    if not isinstance(params["output_dir"], Path):
        output_dir = Path(params["output_dir"] + "/")
    else:
        output_dir = params["output_dir"]
    


    # --------------------------
    # launch ffmpeg on file list
    # --------------------------
    status = 0
    error_files = []

    # check if output directory exists. Otherwise create it
    # -----------------------------------------------------
    if not Path(params["output_dir"]).exists():
        print("Output directory doesn't exist. Creating it")
        Path(params["output_dir"]).mkdir(parents=True, exist_ok=True)

    # path to FFMPEG
    # --------------

    ffmpeg_path = get_ffmpeg_path(params["path_ffmpeg"], debug=debug)

    if not check_ffmpeg(ffmpeg_path):
        print("Could not find FFMPEG. Please install it or review PATH configuration")
        return 1

    # real processing of files
    # -------------------------

    for f in files_list:
        if extract(f, output_dir, beg, end, ffmpeg_path) == 0:
            status += 1
        else:
            error_files.append(f)

    # --------------
    # report results
    # --------------

    # check if all files have been processed
    if len(files_list) > 0:
        results = status / len(files_list)
    else:
        results = 1.0
    print(f"Processing done at {results*100:.0f}%")
    print()

    if len(error_files) > 0:
        print("Something went wrong with these files")
        for ef in error_files:
            print("-", ef.name)
    print("")

    return 0