all: up

up:
	docker compose up --build

down:
	docker compose down

clean:
	docker compose down --rmi all --volumes --remove-orphans
