#!/usr/bin/env python
# filter.py - shim to access different filter types and responses

import bessel

def prettyVal( value, key=None):
    """ Return prettified string for value, parse key for unit type """

    frmt = '%.4f %c'
    if value <= 1E-9: # Pico
        s = frmt % (value * 1E12, 'p')
    elif value < 1E-6: # Nano
        s = frmt % (value * 1E9, 'n')
    elif value < 1E-3: # Micro
        s = frmt % (value * 1E6, 'u')
    elif value < 1: # Milli
        s = frmt % (value * 1E3, 'm')
    else: # (whole units)
        s = frmt % (value, ' ')

    if key is not None: # Add unit suffix if given unit
        if key[0] == 'C':
            s += 'F' # Capacitors have units Farads
            if value < 1e-12 or value > 1e-3:
                s += ' BAD!' # outside of reasonable capacitors
        elif key[0] == 'L':
            s += 'H' # Inductors have units Henries
            if value < 1e-12 or value > 1e-3:
                s += ' BAD!' # outside of reasonable henries

    return s

def getValues( response='bessel', ftype='lowpass', order=1,
        frequency=1.0, bandwidth=None, load=50.0):
    """ Get component values for a specified response and type of filter

    response - Filter response type ['bessel']
    ftype - Filter type ['lowpass', 'highpass', 'bandpass']
    order - Filter order [1 through 10]
    frequency - design frequency (center for bandpass) <MHz>
    bandwidth - width of passband for bandpass filters <MHz>
    load - load resistance <Ohm>
    """
    # Pick module to call based on response first
    if response == 'bessel':
        return bessel.getValues(ftype=ftype, order=order, frequency=frequency,
                bandwidth=bandwidth, load=load)
    else:
        raise ValueError("Filter response type %s not supported" % response)

if __name__ == "__main__":  # if run as standalone script
    import argparse

    parser = argparse.ArgumentParser(
            description="Print component values for given filter")

    parser.add_argument("-r", "--response",     type=str,   required=True,
            help="Filter response", choices=['bessel'])
    parser.add_argument("-t", "--type",         type=str,
            help="Type of filter", choices=['lowpass', 'highpass', 'bandpass'])
    parser.add_argument("-o", "--order",        type=int,
            help="Filter order", choices=range(1,11))
    parser.add_argument("-f", "--frequency",    type=float,
            help="Cutoff frequency (MHz)")
    parser.add_argument("-b", "--bandwidth",    type=float,
            help="Bandwidth (MHz)")
    parser.add_argument("-l", "--load",         type=float, default=50.0,
            help="Output load resistance (Ohm)")

    args = parser.parse_args()

    params = getValues( response=args.response, ftype=args.type,
            order=args.order, frequency=args.frequency,
            bandwidth=args.bandwidth, load=args.load)

    for key, val in params.iteritems():
        print key, ':', prettyVal(val, key)
