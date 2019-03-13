migrate:
	docker-compose exec venv_house_project /bin/bash -c "python app/manage.py db init"
	docker-compose exec venv_house_project /bin/bash -c "python app/manage.py db migrate"
	docker-compose exec venv_house_project /bin/bash -c "python app/manage.py db upgrade"