run:
	docker-compose up --build

test:
	docker-compose -p test -f test-compose.yml up --build
	docker-compose -p test -f test-compose.yml down

dev:
	docker-compose -p dev -f dev-compose.yml up --build