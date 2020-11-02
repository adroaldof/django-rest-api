BLUE=\033[0;34m
RESET_COLOR=\033[0m
GREEN=\033[0;32m

DOCKER_RUN=docker-compose run --rm api
DOCKER_EXEC=docker-compose exec api
DOCKER_TEST=docker-compose -f docker-compose.test.yml run --rm


.PHONY: start stop bash shell migration migrate seed test coverage lint clean

start: stop
	@echo "$(BLUE)--> Running with Docker$(RESET_COLOR)"
	docker-compose up --build


stop:
	@echo "$(BLUE)--> Stopping containers$(RESET_COLOR)"
	docker stop $$(docker ps -q) || true && docker rm $$(docker ps -aq) || true


bash:
	@echo "$(BLUE)--> Bash container$(RESET_COLOR)"
	$(DOCKER_EXEC) sh


shell:
	@echo "$(BLUE)--> Shell container$(RESET_COLOR)"
	$(DOCKER_EXEC) python3 manage.py shell


migration:
	@echo "$(BLUE)--> Creating new migrations$(RESET_COLOR)"
	$(DOCKER_RUN) python3 manage.py makemigrations


migrate:
	@echo "$(BLUE)--> Running all migrations files$(RESET_COLOR)"
	$(DOCKER_RUN) python3 manage.py migrate


seed:
	@echo "$(BLUE)--> Loading seed data$(RESET_COLOR)"
	$(DOCKER_EXEC) python3 manage.py loaddata core


test:
	@echo "$(BLUE)--> Running tests$(RESET_COLOR)"
	$(DOCKER_TEST) test


coverage:
	@echo "$(BLUE)--> Running coverage$(RESET_COLOR)"
	$(DOCKER_TEST) coverage


lint:
	@echo "$(BLUE)--> Running pylint$(RESET_COLOR)"
	$(DOCKER_EXEC) pylint apps,api --load-plugins=pylint_django --msg-template="{path} {line} {msg_id} ({symbol}) {obj}: {msg}"


clean:
	@echo "$(BLUE)--> Removing .pyc and __pycache__$(RESET_COLOR)"
	find . | grep -E "__pycache__|.pyc$$" | xargs rm -rf
	@echo ""
	@echo "$(BLUE)--> Removing coverage data$(RESET_COLOR)"
	rm -rf .coverage .html-coverage
