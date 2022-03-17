cat:
	cat Makefile


rn:
	docker system prune
	python3 etm-class-orchestration-V4.py


mn:
	docker system prune
	python3 orchestrate-monthly-etm.py


kill:
	docker kill `docker ps -q`
