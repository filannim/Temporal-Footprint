Temporal-Footprint
==================

Temporal footprint is a Python based piece of software, which predicts the temporal footprint of a concept by analysing the textual content of its encyclopeadiac description.

![ScreenShot](http://www.cs.man.ac.uk/~filannim/projects/temporal_footprints/gfx/temporal_footprints_git.png)

##How to use it

Run the temporal_footprint.py script with a Wikipedia URL as parameter.

    $ python temporal_footprint.py --help

For example:

    $ python temporal_footprint.py http://en.wikipedia.org/wiki/Galileo_Galilei --start 1564 --end 1642
    Prediction: 1556-1654
    $ 

##Online DEMO

[Click here for the online DEMO](http://www.cs.man.ac.uk/~filannim/projects/temporal_footprints/).

##Requirements

You should have installed the following Python libraries:

* Numpy ([web page](http://www.numpy.org/))
* Matplotlib ([web page](http://matplotlib.org/))
* Scipy ([web page](http://www.scipy.org/))

and the following external softwares:

* HeidelTime ([web page](https://code.google.com/p/heideltime/))
* wikipedia2text ([web page](https://github.com/chrisbra/wikipedia2text))

##Contact
- Email: filannim@cs.man.ac.uk
- Web: http://www.cs.man.ac.uk/~filannim/