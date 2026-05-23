test:
	mypy
	pytest

clean:
	find -regex '.*\.pyc' -exec rm {} \;
	find -regex '.*~' -exec rm {} \;
	rm -rf MANIFEST dist build *.egg-info

install:
	pip install -e ".[web]"

uninstall:
	pip uninstall -y ibflex

.PHONY:	test clean install uninstall
