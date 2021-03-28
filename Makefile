### Pip package building
.PHONY: test-release
test-release: 	
			cleandist
			python3 setup.py sdist bdist_wheel
			python3 -m twine upload --repository testpypi dist/* 

.PHONY: cleandist
cleandist: 		
			rm -r dist

.PHONY: release
release: 		
			cleandist
			python3 setup.py sdist bdist_wheel
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
