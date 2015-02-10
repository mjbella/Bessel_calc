#!/usr/bin/env python
# bessel.py - calculate bessel filter component values
import math, pdb, sys

# !!!!!! MAGIC NUMBERS !!!!!!
# Normalized for 1ohm and 1 rad/sec
COEFS = [[2.00],
         [0.5760,2.148],
         [0.3374,0.9705,2.2034],
         [0.2334,0.6725,1.0815,2.2404],
         [0.1743,0.5072,0.8040,1.1110,2.2582],
         [0.1365,0.4002,0.6392,0.8538,1.1126,2.2645],
         [0.1106,0.3259,0.5249,0.7020,0.8690,1.1052,2.2659],
         [0.0919,0.2719,0.4409,0.5936,0.7303,0.8695,1.0956,2.2656],
         [0.0780,0.2313,0.3770,0.5108,0.6306,0.7407,0.8639,1.0863,2.2649],
         [0.0672,0.1998,0.3270,0.4454,0.5528,0.6493,0.7420,0.8561,1.0781,2.2641]]

def orderCoefs(order):
    """ Return order coefficient lists in a tuple for (Cn, Ln) """
    coeffs = COEFS[order-1]
    Cn = coeffs[0:][::2]
    Ln = coeffs[1:][::2]
    return Cn, Ln

# input the normalized values, output the denormalized values for L&C
def lpl(L, R, F):
    ''' Lowpass inductors
        Return the low pass inductor value '''
    return (L * R) / (2 * math.pi * F)

def lpc(C, R, F):
    ''' Lowpass capacitors
        Return the low pass cap value '''
    return C / (2 * math.pi * F * R)

def hpl(C, R, F):
    ''' Highpass inductors
        Return the high pass inductor value '''
    return R / (2 * math.pi * F * C)

def hpc(L, R, F):
    ''' Highpass capacitors
         Return the high pass cap value '''
    return 1 / (2 * math.pi * F * R * L)

def bpplc(Fh, Fl, R, L):
    ''' Bandpass parallel LCs
        Return the parallel L & C values '''
    Cp = (Fh - Fl)/(2 * math.pi * Fh * Fl * R * L)
    Lp = (R * L) / (2 * math.pi * (Fh - Fl))
    return (Cp,Lp)

def bpslc(Fh, Fl, R, C):
    ''' Bandpass series LCs
        Return the series L & C values '''
    Cs = C / (2 * math.pi * (Fh - Fl) * R)
    Ls = ((Fh - Fl) * R) / (2 * math.pi * Fh * Fl * C)
    return (Cs,Ls)

# Calculate full sequences of component values (for a set of values from the table above) for a filter.
def lp_filter(F, R, Cn, Ln):
    ''' Calculate all the component values for a low pass filter '''
    parts = {}
    for i, l in enumerate(Ln):
        ref = "L%d"%(i+1)
        parts[ref] = lpl(l, R, F)

    for i, c in enumerate(Cn):
        ref = "C%d"%(i+1)
        parts[ref] = lpc(c, R, F)

    return parts

def hp_filter(F, R, Cn, Ln):
    ''' Calculate all the component values for a high pass filter '''
    parts = {}
    for i, l in enumerate(Ln):
        ref = "L%d"%(i+1)
        parts[ref] = hpl(l, R, F)

    for i, c in enumerate(Cn):
        ref = "C%d"%(i+1)
        parts[ref] = hpc(c, R, F)

    return parts

def bp_filter(F, Bw, R, Cn, Ln):
    ''' Calculate all the component values for a bandpass filter '''
    Fl = F - Bw/2.0 # Low frequency of passband
    Fh = F + Bw/2.0 # High frequency of passband
    parts = {}
    for i, L in enumerate(Ln):
        cref = "Cp%d" % (i+1)
        lref = "Lp%d" % (i+1)
        a, b, = bpplc(Fh, Fl, R, L)
        parts[cref] = a
        parts[lref] = b

    for i, C in enumerate(Cn):
        cref = "Cs%d" % (i+1)
        lref = "Ls%d" % (i+1)
        a, b = bpslc(Fh, Fl, R, C)
        parts[cref] = a
        parts[lref] = b

    return parts

def siprint(refdes, value):
    frmt = '%.4f'
    print refdes, ' ',
    if 'c' in refdes[0].lower():
        if value <= 1E-9:
            print frmt%(value*1E12), 'pF'
        elif value < 1E-6:
            print frmt%(value*1E9), 'nF'
        elif value < 1E-3:
            print frmt%(value*1E6), 'uF'
        elif value < 1:
            print frmt%(value*1E3), 'mF'
        else:
            print frmt%(value), 'F'

    if 'l' in refdes[0].lower():
        if value <= 1E-9:
            print frmt%(value*1E12), 'pH'
        elif value < 1E-6:
            print frmt%(value*1E9), 'nH'
        elif value < 1E-3:
            print frmt%(value*1E6), 'uH'
        elif value < 1:
            print frmt%(value*1E3), 'mH'
        else:
            print frmt%(value), 'H'


def printLCs(parts):
    assert isinstance(parts, dict), "The parts list needs to be a dictionary!!"
    print
    for refdes, value in sorted(parts.items()):
        siprint(refdes, value)

# Run the denormalization process for high pass, low pass, or band pass.
def denorm(cut, res, order, ftype, bw=None):
    Cn, Ln = orderCoefs(order)

    ftype = ftype.lower()
    if 'lp' in ftype:
        result =  lp_filter(cut, res, Cn, Ln)
        filter_type = 'Low Pass Filter'
    elif 'hp' in ftype:
        result = hp_filter(cut, res, Cn, Ln)
        filter_type = 'High Pass Filter'
    elif 'bp' in ftype:
        result = bp_filter(cut, bw, res, Cn, Ln)
        filter_type = 'Band Pass Filter'
    else:
        raise ValueError("Unsuported Filter Type!!!")

    print filter_type+':'
    printLCs(result)

def lowpassValues(order=1, frequency=1.0, load=50.0):
    """ Return component values for given lowpass filter as dict.
    frequency is given in MHz, load is given in Ohms
    """
    Cn, Ln = orderCoefs(order)
    cutoff = frequency * 1e6 # convert MHz to Hz
    return lp_filter(cutoff, load, Cn, Ln)

def highpassValues(order=1, frequency=1.0, load=50.0):
    """ Return component values for given highpass filter as dict.
    frequency is given in MHz, load is given in Ohms
    """
    Cn, Ln = orderCoefs(order)
    cutoff = frequency * 1e6 # convert MHz to Hz
    return lp_filter(cutoff, load, Cn, Ln)

def bandpassValues(order=1, frequency=1.0, bandwidth=1.0, load=50.0):
    """ Return component values for given bandpass filter as dict.
    frequency and bandwidth is given in MHz, load is given in Ohms
    """
    Cn, Ln = orderCoefs(order)
    center = frequency * 1e6 # convert MHz to Hz
    bw     = bandwidth * 1e6 # convert MHz to Hz
    return bp_filter(center, bw, load, Cn, Ln)

def getValues(ftype='lowpass', order=1, frequency=1.0,
        bandwidth=None, load=50.0):
    """ Return component values for given bessel filter as dictionary.

    ftype - Filter type ['lowpass', 'highpass', 'bandpass']
    order - Filter order [1 through 10]
    frequency - design frequency (center for bandpass) <MHz>
    bandwidth - width of passband for bandpass filters <MHz>
    load - load resistance <Ohm>
    """
    if ftype == 'lowpass':
        return lowpassValues(order=order, frequency=frequency, load=load)
    elif ftype == 'highpass':
        return highpassValues(order=order, frequency=frequency, load=load)
    elif ftype == 'bandpass':
        return bandpassValues(order=order, frequency=frequency,
                bandwidth=bandwidth, load=load)
    else:
        raise ValueError("Unsuported filter type: %s" % ftype)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("-f", "--freq", help="Set the cutoff frequency (MHz)", type=float, required=True)
    parser.add_argument("-bw", "--bandwidth", help="Set the bandwidth (MHz)", type=float)
    parser.add_argument("-t", "--type", help="Set the type of filter. [HP, LP, BP]", type=str, required=True)
    parser.add_argument("-o", "--order", help="Set the filter order", type=int, required=True)
    parser.add_argument("-r", "--resistance", help="Set the port resistance", type=float, default = 50.00)
    args = parser.parse_args()

    f = args.freq * 1e6 # convert MHz to Hz
    bw = args.bandwidth * 1e6 # convert MHz to Hz
    ftype = args.type
    order = args.order
    r = args.resistance

    if bw: # bandwidth is set
        denorm(f, r, order, ftype, bw=bw)
    else:
        denorm(f, r, order, ftype)
