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
	rm -rf build/ dist/ *.egg-info .pytest_cache
	find . -type d -name __pycache__ -exec rm -rf {} +
