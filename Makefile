all: init test doc

init:
	pip install -r requirements.txt
test:
	py.test --cov-report term-missing --cov=mavconn tests
coverage:
	py.test --cov-report html --cov=mavconn tests
doc:
	$(MAKE) -C docs html
clean:
	$(MAKE) -C docs clean

.PHONY: all init test doc
