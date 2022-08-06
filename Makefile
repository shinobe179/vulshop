list:
	@cat Makefile

run:
	@docker-compose up -d

build-run:
	@docker-compose up --build -d

reset:
	@docker-compose down
	@yes | docker system prune
	@docker volume rm vulshop_mysql
	@make build-run

