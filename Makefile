ifeq ($(OS),Windows_NT)
    SEPARATOR = ;
else
    SEPARATOR = :
endif

.PHONY: format lint test build clean

format:
	isort .
	black .

lint:
	flake8 .
	isort --check-only .
	black --check .

test:
	pytest

build:
	pyinstaller --onefile --windowed --name="ViDownloader" \
		--icon=vidownloader/icons/icon.ico \
		--add-data="vidownloader/icons$(SEPARATOR)icons" \
		--distpath=dist vidownloader/main.py

clean:
	python -c "import shutil, pathlib; [shutil.rmtree(p, ignore_errors=True) for p in list(pathlib.Path('.').rglob('__pycache__')) + list(pathlib.Path('.').glob('*.egg-info')) + [pathlib.Path('build'), pathlib.Path('dist'), pathlib.Path('.pytest_cache')]]"
