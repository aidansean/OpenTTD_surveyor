# OpenTTD Surveyor
A tool for making map images from OpenTTD save games. This is not part of the main OpenTTD codebase, nor is it ever intended to be part of it. This project was written in python to parse save game files to make maps. At the time of writing, it only supports save files up to version 34.

## Installation

Install pycairo
https://pycairo.readthedocs.io/en/latest/getting_started.html

On a mac you can do:

```
> brew install cairo pkg-config
```

Create a virtualenv and install the requirements:

```
> python3 -m venv venv
> source venv/bin/activate
> pip install --upgrade pip
> pip install -r requirements.txt
```

Then clone the repo and change dir:

```
> git clone git@github.com:aidansean/OpenTTD_surveyor.git
> cd OpenTTD_surveyor
```

## Use

Then you should be able to use the tool to make some maps!

Make a png map of the tutorial map:
```
> python src/run.py -m png -v -i example_saves/Tutorial.sav
```

Make an svg map of the tutorial map in dark mode:
```
> python src/run.py -m svg -v -d -i example_saves/Tutorial.sav
```

## Docker

You can also use docker to run the tool to avoid installing dependencies on your
host PC (instead you need to "only" install docker).

Follow the relevant instructions to install docker on your system:
https://docs.docker.com/engine/install/

Clone the repo and change dir as mentioned above.

Build the docker image:
```
docker build . -t openttd_surveyor
```

And run the tool:
```
docker run --rm -v "${PWD}/example_saves":/save -v "${PWD}/example_images":/image openttd_surveyor -m png -v -o /image -i "/save/tiny.sav"
```

Change `${PWD}/example_saves` to the location of your savegames and
`${PWD}/example_images` to the location you want to output the images.

## Questions

*It takes ages to generate a map for a very large save game.*

Yes, it will do. You can use the -p option to show progress bars and -v option to give verbose output, and find out where it's taking a long time.

*Can I use this on Windows?*

I don't have a Windows machine, so I can't help with that, I'm afraid. Anywhere you can use python and can install cairo should work.

*Will it work with this really cool extension I'm using?*

Yes. No. Maybe. I don't know. Can you repeat the question? Try it and find out!

*I'm colour blind. Can you make it more colour blind friendly?*

Maybe... Pretty much all the colours are specified in the config files, so you should be able to change the colours there to something more friendly.


*This repo is poorly coded and the maps are buggy!*

Probably. Help out by forking it and opening a PR :)

## Screenshots

Here's the sort of thing it can do:

![Normal mode example](/example_images/martin_250.png)

![Normal mode example](/example_images/tiny_normal_mode.png)

![Dark mode example](/example_images/tiny_dark_mode.png)
