Base=tbutzer/etm_v3_python_base


base:
	docker build -t ${Base} -f Dockerfile.base .


Image=tbutzer/etm_v3

build:
	docker build -t ${Image} .



publish:
	cat ~/token.txt
	git add .
	git commit -m 'Auto git update December 2021 - tony'
	git push

