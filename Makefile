.PHONY: install run lint build up down logs
install:
	pip install -r requirements.txt
run:
	streamlit run app.py
lint:
	pip install ruff && ruff check app.py
build:
	docker compose build
up:
	docker compose up -d
down:
	docker compose down
logs:
	docker compose logs -f
