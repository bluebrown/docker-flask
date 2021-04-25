run:
	docker-compose up --build

test:
	docker-compose -f test-compose.yml up --build
	docker-compose -f test-compose.yml down
