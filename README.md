Temporal-Footprint
==================

Temporal footprint is a Python based piece of software, which predicts the temporal footprint of a concept by analysing the textual content of its encyclopeadiac description.

![ScreenShot](http://www.cs.man.ac.uk/~filannim/projects/temporal_footprints/gfx/temporal_footprints_git.png)

##Online DEMO

[Click here for the online DEMO](http://www.cs.man.ac.uk/~filannim/projects/temporal_footprints/).



##How to use it (from command line)

Run the temporal_footprint.py script with a Wikipedia URL as parameter.

    $ python temporal_footprint.py --help

For example:

    $ python temporal_footprint.py http://en.wikipedia.org/wiki/Galileo_Galilei --start 1564 --end 1642
    Prediction: 1556-1654



## How to install it

	$ python setup.py install



##Requirements

Python libraries:

* Numpy ([web page](http://www.numpy.org/))
* Matplotlib ([web page](http://matplotlib.org/))
* Scipy ([web page](http://www.scipy.org/))

Non-Python resources:

* HeidelTime ([web page](https://code.google.com/p/heideltime/))
* wikipedia2text ([web page](https://github.com/chrisbra/wikipedia2text))

please update the `temporal_footprint/properties.py` file with the right paths.

##Contact
- Email: filannim@cs.man.ac.uk
- Web: http://www.cs.man.ac.uk/~filannim/