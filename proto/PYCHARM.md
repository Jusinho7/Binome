# Running Fly-in in PyCharm

This project ships with a ready-made `.idea/` configuration: three Run
Configurations and a module marking `fly_in/` as the sources root. You
should be able to open it and run it in about a minute.

## 1. Open the project

`File > Open...` and select the `fly-in` folder (the one containing
`Makefile`, `README.md`, `fly_in/`, etc.) — not a parent folder, not the
`fly_in/` package itself.

## 2. Configure the Python interpreter

PyCharm will likely show a banner saying no interpreter is configured
(the bundled config references an SDK named `Python 3.10 (fly-in)` that
only exists on the machine it was created on).

`File > Settings > Project: fly-in > Python Interpreter > Add Interpreter`

- Choose **Add Local Interpreter**.
- Pick **Virtualenv Environment > New**, base interpreter = any
  Python **3.10+** you have installed, then OK.
- Once created, open a PyCharm terminal (`Alt+F12` / bottom toolbar)
  and run:

  ```bash
  pip install -r requirements-dev.txt
  ```

  (this installs `flake8`, `mypy` and `pytest` — nothing else is
  required to run the simulator itself).

## 3. Run it

Open the **Run Configurations** dropdown (top-right toolbar) — you
should see three already defined:

- **Run Fly-in (subject example)** — runs `maps/example_subject.txt`.
- **Run Fly-in (hard maze)** — runs `maps/hard_maze.txt`.
- **Run all tests** — runs the full `pytest` suite.

Pick one and click the green ▶ button (or `Shift+F10`).

### Running a different map

Duplicate any of the two "Run Fly-in" configurations
(`Run > Edit Configurations... > select it > the copy icon`), then
change the **Parameters** field to e.g.:

```
maps/medium_loop.txt --quiet
```

### If the configurations don't show up

Create one yourself:

`Run > Edit Configurations... > + > Python`

- **Name**: anything, e.g. `Fly-in`
- **Module name** (not "Script path"!): `fly_in.main`
- **Parameters**: `maps/example_subject.txt`
- **Working directory**: the project root (should be filled automatically)

Apply, then run it.

## 4. Linting / type-checking from PyCharm

You can also just use the integrated terminal for the Makefile targets:

```bash
make lint          # flake8 + mypy (subject-mandated flags)
make lint-strict     # flake8 + mypy --strict
make test           # pytest
```

Optionally, enable PyCharm's built-in inspections for these tools under
`Settings > Tools > Python Integrated Tools` (set the default test
runner to `pytest`) and `Settings > Editor > Inspections > Python` if
you'd like inline warnings while you type, in addition to the
command-line checks above.
