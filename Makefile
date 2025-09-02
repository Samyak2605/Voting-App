SHELL := /bin/sh

.PHONY: up down logs ps vote result health

up:
	docker-compose up -d --build

down:
	docker-compose down -v

logs:
	docker-compose logs --tail=200 -f

ps:
	docker ps

vote:
	@echo http://localhost:5050
	@curl -sf http://localhost:5050 | head -n 3 || true

result:
	@echo http://localhost:5051
	@curl -sf http://localhost:5051 | head -n 3 || true

health: vote result
	@echo OK
