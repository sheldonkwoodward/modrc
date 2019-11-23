docker build -f test.Dockerfile -t modrc_tests:latest .
docker run --name modrc_tests -v $(pwd)/modrc/:/modrc/modrc -v $(pwd)/tests/:/modrc/tests modrc_tests:latest python -m unittest discover
docker rm modrc_tests
