Base=tbutzer/etm_v3_python_base


base:
	docker build -t ${Base} -f Dockerfile.base .


Image=tbutzer/etm_v3

build:
	docker build -t ${Image} .


test_etasw:
	docker run -it ${Image} python3 api_etm.py -i ws-out/CONUS/Run03_11_2022/conus_r50t9/ -o ws-enduser/CONUS/r50.0_tile9/ -y monthly etasw dummy

test_etc:
	docker run -it ${Image} python3 api_etm.py -i ws-out/CONUS/Run03_11_2022/conus_r50t9/ -o ws-enduser/CONUS/r50.0_tile9/ -y monthly etc dummy

test_dd:
	docker run -it ${Image} python3 api_etm.py -i ws-out/CONUS/Run03_11_2022/conus_r50t9/ -o ws-enduser/CONUS/r50.0_tile9/ -y monthly dd dummy


run:
	docker run -it ${Image} bash


publish:
	cat ~/token.txt
	git add .
	git commit -m 'Auto git update December 2021 - tony'
	git push

