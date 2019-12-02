.PHONY: run test
run:
	docker-compose up -d
	docker-compose exec python ./manage.py makemigrations
	docker-compose exec python ./manage.py migrate
test:
	docker-compose exec python ./manage.py test game.tests