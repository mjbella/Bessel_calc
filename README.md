# bessel_calc

Calculate component values to make an LC lowpass, highpass, or bandpass filter,
using precomputed normalized values from
[rfcafe] [rfcafe] .

This script may produce component values that are either too low or too high
to be usable depending on the input requirements.

_bessel.py_ accepts the following options:
```
-f	Set the cutoff frequency (MHz)
-bw	Set the bandwidth (MHz)
-t	Set the type of filter. [HP, LP, BP]
-o	Set the filter order
-r	Set the port resistance
```

[rfcafe]: http://www.rfcafe.com/references/electrical/bessel-proto-values.htm
