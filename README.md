# bessel_calc

This python script uses precomputed normalized values from http://www.rfcafe.com/references/electrical/bessel-proto-values.htm to calculate the required component values to make an LC lowpass, highpass, or bandpass filter.

This script may produce component values that are either too low or too high to be usable depending on the input requirements.

bessel.py accepts the following options:
Flag	| Description
--------|-------------------------------------
  -f	| Set the cutoff frequency (MHz)
  -bw	| Set the bandwidth (MHz)
  -t	| Set the type of filter. [HP, LP, BP]
  -o	| Set the filter order
  -r	| Set the port resistance

