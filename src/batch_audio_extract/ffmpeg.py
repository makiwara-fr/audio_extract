from pathlib import Path
import subprocess
import sys


def get_ffmpeg_path(path_ffmpeg: str, debug: bool = False) -> Path:
    """
    Constructs the platform-specific path to the FFmpeg executable.

    Args:
        path_ffmpeg: The directory path where the FFmpeg executable is located.
                     If empty, it assumes FFmpeg is in the system's PATH.
        debug: If True, prints the constructed path.

    Returns:
        A Path object representing the full path to the FFmpeg executable.
    """
    ffmpeg_exec = "ffmpeg.exe" if sys.platform == "win32" else "ffmpeg"
    if path_ffmpeg:
        ffmpeg_path = Path(path_ffmpeg) / ffmpeg_exec
    else:
        ffmpeg_path = Path(ffmpeg_exec)

    if debug:
        print(f"Path to ffmpeg is : {ffmpeg_path}")
        print()

    return ffmpeg_path


def check_ffmpeg(ffmpeg_path: Path) -> bool:
    """
    Check if ffmpeg is available at the given path or in the system's PATH.

    Args:
        path_ffmpeg: The path to the directory containing the ffmpeg executable.
                     If empty, it will check for ffmpeg in the system's PATH.

    Returns:
        True if ffmpeg is found and executable, False otherwise.
    """


    try:
        # On Windows, use CREATE_NO_WINDOW to prevent a console from popping up
        creation_flags = 0
        if sys.platform == "win32":
            creation_flags = subprocess.CREATE_NO_WINDOW

        subprocess.run(
            [str(ffmpeg_path), "-version"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=creation_flags,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False