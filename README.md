# Sketch Pad

Keeping Adobe awake at night, one terminal input at a time.

## Install

    git clone github.com/sbramin/sketch

## Requirements

- Python 3+
- *nix terminal (Available on Osx and even windows with gitbash etc)

## Run

	cd sketch/
	./sketch.py

## Usage

c/C - Creates a new Pad.  This must be smaller than your terminal size.
For example to create a Pad of size 25x25 issue the following command:

	c 25 25

l/L - Once your pad is created you can get drawing by inputing the x1, y1 and x2, y2 coordinates.
For example, to draw a line from (x1,y1) to (x2,y2) issue the following command:

	l 1 2 6 2

r/R - Draw a rectangle using similar positions to a line eg.
	
	r 1 5 10 20

b/B - Use the fill Bucket to fill empty lines with the colour of your choice.  For example filling 
the pad with blue can be done with:
	
	b 1 1 b

q/Q - Quit Sketch Pad, useful if you realy want to start again.




## TODO

* Fill function doesn't work as expected, likely a simple matrix operation from full functionality.
