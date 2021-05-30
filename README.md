# OpenTTD_surveyor
A tool for making map images from OpenTTD save games

Install pycairo
https://pycairo.readthedocs.io/en/latest/getting_started.html

On a mac you can do:
> brew install cairo pkg-config

Create a virtualenv and install the requirements:

> python3 -m venv venv
> source venv/bin/activate
> pip install --upgrade pip
> pip install -r requirements.txt

Then you should be able to use the tool to make some maps!

Make a png map of the tutorial map:
> python src/run.py -m png -v -i example_saves/Tutorial.sav

Make an svg map of the tutorial map in dark mode:
> python src/run.py -m svg -v -d -i example_saves/Tutorial.sav

