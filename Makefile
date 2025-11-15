install_ci:
	poetry install
	poetry run pre-commit install

install_dev:
	make install_ci
	poetry shell
	invoke --list

install_poetry:
	pip install poetry==2.2.1
	poetry self add poetry-plugin-shell
	pip install --upgrade pip
