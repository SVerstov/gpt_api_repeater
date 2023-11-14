.PHONY: init migrate migrations downgrade run parse update

init:
	poetry install
	poetry shell

run:
	poetry run python app.py bot


update:
	git pull
	poetry install
	sudo systemctl restart gpt_repeater.service
