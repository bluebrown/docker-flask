run:
	docker-compose up --build

test:
	docker-compose -f test-compose.yml up
	sleep 5
	docker-compose -f test-compose.yml down
