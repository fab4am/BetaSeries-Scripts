ifndef TEST_FLAGS
	TEST_FLAGS:=
endif

venv:
	python2.6 tools/make-bootstrap.py
	python2.6 bootstrap.py --no-site-packages venv
	rm bootstrap.py

clean:
	rm -Rf venv/ bs.egg-info/
	rm bs.db

app:
	python2.6 bs/ui.py