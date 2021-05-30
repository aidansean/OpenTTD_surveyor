# OpenTTD Surveyor
A tool for making map images from OpenTTD save games. This is not part of the main OpenTTD codebase, nor is it ever intended to be part of it. This project was written in python to parse save game files to make maps.

## Installation

Install pycairo
https://pycairo.readthedocs.io/en/latest/getting_started.html

On a mac you can do:
> brew install cairo pkg-config

Create a virtualenv and install the requirements:

```
> python3 -m venv venv
> source venv/bin/activate
> pip install --upgrade pip
> pip install -r requirements.txt
```

## Use

Then you should be able to use the tool to make some maps!

Make a png map of the tutorial map:
> python src/run.py -m png -v -i example_saves/Tutorial.sav

Make an svg map of the tutorial map in dark mode:
> python src/run.py -m svg -v -d -i example_saves/Tutorial.sav

## Questions

Will it work with this really cool extension I'm using?
Probably not.

I'm colour blind. Can you make it more colour blind friendly?
Maybe... Pretty much all the colours are specified in the config files, so you should be able to change the colours there to something more friendly.

It takes to generate a map for a very large save game.
Yes, it will do. You can use the -p option to show progress bars and -v option to give verbose output, and find out where it's taking a long time.

Can I use this on Window?
I don't have a Windows machine, so I can't help with that, I'm afraid. Anywhere you can use python and can install cairo should work.

This repo is poorly coded and the maps are buggy!
Probably. Help out by forking it and opening a PR :)
