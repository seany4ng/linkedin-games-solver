# Tango Solver

Tango is my favorite game by far, and thus the first bot that we decided to work on end-to-end.

## Tango Backend

Hooray! You want to run the Tango backend locally. There's only one endpoint right now, but this should be sufficient for our use cases.

> Note: ensure you have python >= 3.10. Running in a virtual-env is recommended.

Assuming you have everything set up, begin by installing the right packages. From `tango/core`:

```bash
pip install -r requirements.txt
```

Everything should be setup now. To expose this server at `http://localhost:8000`, run:

```bash
cd .. && python3 -m core.app.run
```

Running the app (i.e. the `python3` script) should occur from the `tango` directory rather than `tango/core`, which is why we added a `cd`.

## Backend unit tests

If for whatever reason, you want to run the backend unit tests, you can do so by running each individual file. From the `tango` directory:

```bash
python3 -m core.tests.test_services
python3 -m core.tests.test_solver
```

Setting up pytest probably takes less time than it takes to write this README but sometimes you just don't feel like doing that
