up:
	@[ -d "user_db" ] || mkdir user_db
	@sudo docker compose up -d --build

down:
	@sudo docker compose down


clean:down
	@docker system prune -a -f
	docker volume prune -f
	docker network prune -f
	docker compose down --volumes --remove-orphans

re:clean up


.PHONY: all re down clean