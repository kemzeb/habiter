### Pip package building
.PHONY: setup
setup: clean
	python3 setup.py sdist bdist_wheel

.PHONY: test-release
test-release: clean setup
	python3 -m twine upload --repository testpypi dist/*
			

.PHONY: clean
clean: 			
	if [ -d "dist" ]; then \
		rm -r "dist"; \
	fi

	if [ -d "build" ]; then \
		rm -r "build/"; \
	fi

.PHONY: release
release: clean setup
	python3 -m twine upload dist/*


### Development-related
.PHONY: dev-mode
dev-mode:
	pip install -e .

.PHONY: dev-clean
dev-clean:
	pip uninstall habiter

.PHONY: dev-run # Runs linting and testing commands that are almost equivalent to what is ran in the CI pipeline
dev-run: lint-check test


## Linting
.PHONY: lint-check
lint-check:
	@echo '[habiter]  Linting for Python syntax errors or undefined names...'
	flake8 --count --select=E9,F63,F7,F82 --show-source --statistics --exclude=venv,dist,build .
	@echo '[habiter]  Linting with the default error codes...'
	flake8 --count --max-complexity=10 --max-line-length=100 --statistics --exclude=venv,dist,build .


### Testing
.PHONY: test
test:
	@echo '[habiter]  Running tests...'
	pytest -v


### Virtual environment
.PHONY: virt
virt:
		python3 -m venv venv/
