# Tango Solver

Tango is my favorite game by far, and thus the first bot that we decided to work on end-to-end.

## Tango Backend

Hooray! You want to run the Tango backend locally. There's only one endpoint right now, but this should be sufficient for our use cases.

> Note: ensure you have python >= 3.10. Running in a virtual-env is recommended.

Assuming you have everything set up, begin by installing the right packages. From `tango/core`:

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

Everything should be setup now. To expose this server at `http://localhost:8000`, run:

```bash
cd .. && python3 -m core.app.run
```

Running the app (i.e. the `python3` script) should occur from the `tango` directory rather than `tango/core`, which is why we added a `cd`.

## Tango Frontend

We use a React/Typescript frontend with vite for building the project. Before starting, make sure your npm and node versions are supported. The dependencies will generally require:
- `node -v` >= 16.18
- `npm -v` >= 8.3

If you don't have node or npm installed, get them installed with versions satisfying the above constraints. Once done, install the required dependencies:

```bash
npm install
```

Start the dev server:

```bash
npm run dev
```

And open the app locally in a browser:

```
http://localhost:5173
```

**Note: this requires starting the backend server first. See `../core` for details.**

### Frontend: Troubleshooting

Either npm sucks or I'm bad at using it, but I routinely face issues with `vite` and `node_modules`. If this is you, I've found that re-installing everything typically works.

```bash
rm -rf node_modules package-lock.json
npm install
```

Once in a while, `vite` will suddenly be not found -- I have no clue why. Whenever this happens, I use the above commands, similar to how back in the day, IT support primarily consisted of turning the machine off and on again.

## Backend unit tests

If for whatever reason you want to run unit tests, you can do so by calling `pytest` in the `tango/core` directory. To ensure the pytest is the one installed in the current python environment, we can run it as follows:

```bash
python3 -m pytest # Runs all tests
python3 -m pytest tests/test_api.py # Runs tests in test_api.py
python3 -m pytest tests/test_api.py::test_tango_api # Runs a specific test
```

If you get any module not found errors, you can typically resolve them by reinstalling the correct dependencies in your existing environment:

```bash
python3 -m pip install -r requirements.txt
python3 -m pytest # This should not run into module not found
```
