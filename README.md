# GDMC 2021 Submission
Developed by [Matthew Hickey](https://github.com/matthickey709) and [Alex Porter](https://github.com/abporter).

Result: 7th overall and 2nd in aesthetics.

This project was forked from [gdmc_http_client_python](https://github.com/nilsgawlik/gdmc_http_client_python) to use the library functions as a starting point for communicating with the HTTP API.

# Final Submission
* [Trailer Video](https://youtu.be/kdEqbZuHSmE)
* [Presentation and Demo](https://www.youtube.com/watch?v=TipwEZGCl84)

There are instructions below for how to get this up and running. Before running the script ensure that the chunks
that are in your build area are loaded. Otherwise, the parser won't recognize the NBT and you'll have to try again.

## Get up and running
Using Python 3.9 or newer, create a virtual environment and install the requirements into it. Run the following from the root of this repository:

```bash
python3 -m venv gdmc_env
source gdmc_env/bin/activate
python -m pip install -r requirements.txt
```

If there are any issues getting this running, please don't hesitate to contact either of us.

You need to have Minecraft running, the necessary mods (version 36.0.43 of Forge, version 0.4.1 of GDMC HTTP interface mod) installed and a world open for this to work!

## Scripts

**`gdmc_2021/GDMCSettlementGenerator.py`**: Run this file while a minecraft world is open with a build area set to generate a settlement. Build area is set in Minecraft using the setbuildarea command.

Example: `/setbuildarea 0 3 0 200 3 200`

Creates a build area from 0,0 to 200,200.
When the build area is set (and virtual environment activated):

```bash
cd gdmc_2021
python GDMCSettlementGenerator.py
```

When prompted, set a timeout in minutes. Hitting enter with no timeout will default to 10 minutes (GDMC limit). For builds
greater than 256x256, more time may be needed to generate the settlement.

## Tests

Run the tests from the `gdmc_2021` directory:

```bash
cd gdmc_2021
python -m unittest discover -s tests -t .
```

The tests in `tests/minecraft` need Minecraft running with a build area set, and place blocks inside that build area.
They are skipped when Minecraft isn't reachable.

### Acknowledgements
* Some structures: https://www.youtube.com/watch?v=d7dp6pHzKJU
