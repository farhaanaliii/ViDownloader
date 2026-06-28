.PHONY: format lint test resources build clean

format:
	isort .
	black .

lint:
	flake8 .
	isort --check-only .
	black --check .

test:
	pytest

resources:
	pyrcc5 vidownloader/resources.qrc -o vidownloader/ui/resources_rc.py

build: resources
	pyinstaller --onefile --windowed --name="ViDownloader" --icon=vidownloader/icons/icon.ico --distpath=dist vidownloader/main.py

clean:
	python -c "import shutil, pathlib; [shutil.rmtree(p, ignore_errors=True) for p in list(pathlib.Path('.').rglob('__pycache__')) + list(pathlib.Path('.').glob('*.egg-info')) + [pathlib.Path('build'), pathlib.Path('dist'), pathlib.Path('.pytest_cache')]]"
