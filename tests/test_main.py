from src.batch_audio_extract import main
from src.batch_audio_extract import process
import pytest
import re
from pathlib import Path

def test_regexp():
    assert type(process.set_regexp(["mp3"])) == re.Pattern
    assert type(process.set_regexp(["mp3","wav"])) is not None

def test_scan():
    scan_cwd = process.scan_folder(".", process.set_regexp(["mp3"]))
    assert type(scan_cwd) == list

def test_main():
    p_status = process.process(input_params={"debug":True, "input_dir":"tests/input_test", "output_dir":"tests/output_test", "first_second":0, "last_second":5})
    assert p_status == 0
    assert Path("tests/output_test/test_extract.mp3").exists()