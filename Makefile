install:
	python -m pip install --upgrade pip &&\
		python -m pip install -r src/audio_extract/requirements.txt

test:
	python -m pytest -v src/audio_extract/tests/test_main.py
lint:

format:
	black src/audio_extract/*.py

all:
	make install lint test