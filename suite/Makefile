URL='conda'

# docker run -ti --privileged -v `pwd`/../../:/code -v `pwd`/../secrets/:/secrets $(URL) --asset_root `pwd` --cmd 'python /code/docker/conda3/test.py'

bash:
#	docker run -ti  -v /sailhome/jimfan/vision:/home/jimfan/vision:rw $(URL) bash
	docker run -ti  -v /sailhome/jimfan/vision/temp1:/home/jimfan/vision/temp1:rw $(URL) bash
#	docker run -ti --privileged $(URL) bash

push:
	docker push $(URL):`cat VERSION`
	docker push $(URL):latest

build:
	# docker build -t $(URL):`cat VERSION` .
	docker build -t $(URL) .
	# docker tag $(URL):`cat VERSION` $(URL):latest
	docker tag $(URL) $(URL):latest

run: build
	docker run -ti --privileged -v /sailhome/jimfan/vision:/home/jimfan/vision $(URL) ls --color /home/jimfan/vision

