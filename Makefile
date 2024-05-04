.PHONY: run
run:
	python3.12 src/manage.py runserver


.PHONY: check
check:
	python3.12 -m ruff . && python3.12 -m black --check . && python3.12 -m isort --check .

.PHONY: fix
fix:
	python3.12 -m ruff --fix . && python3.12 -m black . && python3.12 -m isort .
    
.PHONY: database
database:
	docker compose up -d database

.PHONY: broker
broker:
	docker compose up -d broker

.PHONY: mailing
mailing:
	docker compose up -d mailing

.PHONY: down
down:
	docker compose down


.PHONY: worker
worker:
	celery -A config worker -l INFO