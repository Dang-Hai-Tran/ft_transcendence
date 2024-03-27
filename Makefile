all: up

up:
	docker compose up -d --build

down:
	docker compose down

start:
	docker compose start

stop:
	docker compose stop

logs:
	docker compose logs

status:
	docker compose ps

clean:
	docker compose down --rmi all --volumes --remove-orphans
	docker system prune -f -a --volumes

.PHONY: all up down start stop logs status clean
