run:
	docker-compose up --build

test:
	docker-compose -p test -f test-compose.yml up
	docker-compose -p test -f test-compose.yml down
