# Backend

This is a WSGI Flask server that serves a few basic endpoints for each Linkedin game. Currently, this is only Queens and Tango, but more will be added soon.

## Local dev

> Note: ensure you have python >= 3.10. Running in a virtual-env is recommended.

Assuming you have everything set up, begin by installing the right packages. From `/core`:

```bash
pip install -r requirements.txt
```

We need a `.env` file in `tango/core`. Create one and populate it with the following contents:

```
# .env
DEBUG=True
SECRET_KEY=super-secret-key
FLASK_RUN_HOST=localhost
FLASK_RUN_PORT=8000
```

Everything should be setup now. To expose this server at `http://localhost:8000`, first `cd` outside of `core` (`cd ..`). Then run:

```bash
python3 -m core.app.run
```

This local server will listen on port 8000 of your machine.

## Unit tests

If for whatever reason you want to run unit tests, you can do so by calling `pytest` in the `core` directory. To ensure the pytest is the one installed in the current python environment, we can run it as follows:

```bash
python3 -m pytest # Runs all tests
python3 -m pytest tests/tango # Runs tests in the tango/ folder
python3 -m pytest tests/tango/test_tango_solver.py::test_board_55 # Runs a specific test
```

If you get any module not found errors, you can typically resolve them by reinstalling the correct dependencies in your existing environment:

```bash
python3 -m pip install -r requirements.txt
python3 -m pytest # This should not run into module not found
```
