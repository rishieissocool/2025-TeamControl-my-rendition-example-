VENV = . 
PIP = ./bin/pip3
PYTHON = ./bin/python3

all: $(VENV)/bin/activate

$(VENV)/bin/activate: pyproject.toml
	virtualenv .
	$(PIP) install -e . 

clean:
	rm -rfv bin/ lib/ share/ pyvenv.cfg

.PHONY: venv clean