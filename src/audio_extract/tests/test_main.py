from src.audio_extract import main
import pytest
import re

def test_regexp():
    assert type(main.set_regexp(["mp3"])) == re.Pattern
    assert type(main.set_regexp(["mp3","wav"])) is not None

def test_scan():
    scan_cwd = main.scan_folder(".", main.set_regexp(["mp3"]))
    assert type(scan_cwd) == list

def test_main():
    pass