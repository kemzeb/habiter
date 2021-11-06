### Pip package building
.PHONY: setup clean
setup:		
		python3 setup.py sdist bdist_wheel

.PHONY: test-release
test-release: 	clean setup
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
release: 		clean setup
			python3 -m twine upload dist/*
## END OF Pip package building


### Developer mode 
.PHONY: devmode
devmode: 			
			pip install -e .

.PHONY: devclean
devclean:			
			pip uninstall habiter
## END OF Developer mode


### Testing
.PHONY: test
test:			
			@echo "Recipe not yet supported."
## END OF Testing


### Virtual Environment
.PHONY: virt
virt:
		python3 -m venv venv/