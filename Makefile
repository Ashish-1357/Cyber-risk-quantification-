.PHONY: install start test docker-build docker-up docker-down clean

# Local Development
install:
	cd server && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt

start:
	./scripts/start.sh

test:
	./scripts/test.sh

# Docker
docker-build:
	docker-compose build

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

# Cleanup
clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name .pytest_cache -exec rm -rf {} +
	find . -type d -name venv -exec rm -rf {} +
