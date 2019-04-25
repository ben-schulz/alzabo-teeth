PWD = `pwd`
SRC_FILES = teeth/*.py tests/*.py

ENTR = entr
ENTR_FLAGS = -c
NEED_ENTR = "'make watch' requires entr to be installed."

PYTEST = python -m pytest
PYTEST_FLAGS = -s

watch:

	which $(ENTR) || ( echo $(NEED_ENTR) && exit 1 )
	ls $(SRC_FILES) | $(ENTR) $(ENTR_FLAGS) $(PYTEST) $(PYTEST_FLAGS)

test:
	$(PYTEST) $(PYTEST_FLAGS)

.PHONY: watch test
