### Pip package building
.PHONY: setup
setup: clean
	python3 setup.py sdist bdist_wheel

.PHONY: test-release
test-release: setup
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
	@echo '[habiter]  Linting with flake8...'
	flake8 --count --show-source --statistics --exclude=venv,dist,build .


### Testing
.PHONY: test
test:
	@echo '[habiter]  Running tests...'
	pytest -v


### Virtual environment
.PHONY: virt
virt:
		python3 -m venv venv/
