test:
	coverage erase
	nosetests -dsv --with-yanc --with-coverage --cover-package ibflex tests/*.py

clean:
	find -regex '.*\.pyc' -exec rm {} \;
	find -regex '.*~' -exec rm {} \;
	rm -rf reg-settings.py
	rm -rf MANIFEST dist build *.egg-info
	rm -rf test.db

install:
	make clean
	make uninstall
	python setup.py install

uninstall:
	pip uninstall -y ibflex

lint:
	pylint ibflex/*.py

lint-tests:
	pylint tests/*.py

.PHONY:	test clean lint lint-tests install uninstall
