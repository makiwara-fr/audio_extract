from pathlib import Path

def get_ffmpeg_path(path_ffmpeg:str, debug:bool=False)->Path:
    if len(path_ffmpeg) > 0:
        ffmpeg_path = Path(path_ffmpeg).joinpath("ffmpeg")
    else:
        ffmpeg_path = "ffmpeg"

    if debug:
        print(f"Path to ffmpeg is : {ffmpeg_path}")
        print()

    return ffmpeg_path