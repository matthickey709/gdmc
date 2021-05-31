# GDMC 2021 Submission
This project was forked from [gdmc_http_client_python](https://github.com/nilsgawlik/gdmc_http_client_python) to use the library functions as a starting point for communicating with the HTTP API.

# Final Submission
* [Trailer Video](https://youtu.be/kdEqbZuHSmE)
* [Presentation and Demo](https://www.youtube.com/watch?v=TipwEZGCl84)

There are instructions below for how to get this up and running. Before running the script ensure that the chunks
that are in your build area are loaded. Otherwise, the parser won't recognize the NBT and you'll have to try again.

## Get up and running
Using python >= 3.7, create a virtual environment. Then inside that virtual environment, run pip install using the requirements.txt as input. Then you're ready to go.
Run the following while inside the gdmc_http_client_python directory:

```
<path to correct python> -m gdmc_env
source gdmc_env/bin/activate
python -m pip install -r requirements.txt
```

If there are any issues getting this running, please don't hesitate to contact either of us. 

You need to have Minecraft running, the necessary mods (version 36.0.43 of Forge, version 0.4.1 of GDMC HTTP interface mod) installed and a world open for this to work!

Scripts:

**`GDMCSettlemetGenerator.py`**: Run this file while a minecraft world is open with a build area set to generate a settlement. Build area is set in Minecraft using setBuildArea command.

Example: setbuildarea 0 3 0 200 3 200

Creates a build area from 0,0 to 200,200.
When the build area is set (and virtual environment activated):

```
python GDMCSettlementGenerator.py
```
When prompted, set a timeout in minutes. Hitting enter with no timeout will default to 10 minutes (GDMC limit). For builds
greater than 256x256, more time may be needed to generate the settlement (needed 15 for 400x400).



### Acknowledgements
* Some structures: https://www.youtube.com/watch?v=d7dp6pHzKJU
