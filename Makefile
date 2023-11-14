.PHONY: init migrate migrations downgrade run parse update

init:
	poetry install
	poetry shell

run:
	poetry run python app.py bot


update:
	git pull origin master
	poetry install
	make migrate
	sudo systemctl restart wild_bot.service
	sudo systemctl restart wild_bot_api.service