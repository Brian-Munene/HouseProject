migrate:
	docker-compose exec house_project /bin/bash -c "python app/manage.py db init"
	docker-compose exec house_project /bin/bash -c "python app/manage.py db migrate"
	docker-compose exec house_project /bin/bash -c "python app/manage.py db upgrade"