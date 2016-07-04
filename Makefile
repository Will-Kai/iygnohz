static:
	./python3 manage.py collectstatic

start:
	fab start

stop:
	fab stop

restart:
	fab restart


build:
	fab build

deploy:
	fab deploy
