#!/usr/bin/env python

import sys
import math
import argparse
import pdb

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

parser = argparse.ArgumentParser()

parser.add_argument("-f", "--freq", help="Set the cutoff frequency (MHz)", type=float, required=True)
parser.add_argument("-bw", "--bandwidth", help="Set the bandwidth (MHz)", type=float)
parser.add_argument("-t", "--type", help="Set the type of filter. [HP, LP, BP]", type=str, required=True)
parser.add_argument("-o", "--order", help="Set the filter order", type=int, required=True)
parser.add_argument("-r", "--resistance", help="Set the port resistance", type=float, default = 50.00) 
args = parser.parse_args()

f = args.freq
bw = args.bandwidth
ftype = args.type
order = args.order
r = args.resistance

fl = f - bw/2
fh = f + bw/2

coef = COEFS[order-1]

# input the normalized values, output the denormalized values for L&C
def lpl(L, R, F):
    # Return the low pass inductor value
    return (L * R) / (2 * math.pi * F)

def lpc(C, R, F):
    # Return the low pass cap value
    return C / (2 * math.pi * F * R)

def hpl(C, R, F):
    # Return the high pass inductor value
    return R / (2 * math.pi * F * C)

def hpc(L, R, F):
    # Return the high pass cap value
    return 1 / (2 * math.pi * F * R * L)

def bpplc(Fh, Fl, R, L):
    # return the parallel L & C values
    Cp = (Fh - Fl)/(2 * math.pi * Fh * Fl * R * L)
    Lp = (R * L) / (2 * math.pi * (Fh - Fl))
    return (Cp,Lp)

def bpslc(Fh, Fl, R, C):
    # Return the series L & C values
    Cs = C / (2 * math.pi * (Fh - Fl) * R)
    Ls = ((Fh - Fl) * R) / (2 * math.pi * Fh * Fl * C)
    return (Cs,Ls)


def lp_filter(F, R, Cn, Ln):    
    inductors = []
    for l in Ln:
	inductors.append(lpl(l, R, F))
    capacitors = []
    for c in Cn:
	capacitors.append(lpc(c, R, F))

    return inductors, capacitors

def hp_filter(F, R, Cn, Ln):
    inductors = []
    for l in Ln:
	inductors.append(hpl(l, R, F))
    capacitors = []
    for c in Cn:
	capacitors.append(hpc(c, R, F))

    return inductors, capacitors

def bp_filter(Fh, Fl, R, Cn, Ln):
    parallel_LC = []
    series_LC = []
    for L in Ln:
	parallel_LC.append(bpplc(Fh, Fl, R, L))
    for C in Cn:
	series_LC.append(bpslc(Fh, Fl, R, C))



def denorm(cut, res, order, ftype, coeffs):
    Cn = coeffs[0:][::2]
    Ln = coeffs[1:][::2]
    
    ftype = ftype.lower()
    if 'lp' in ftype:
	print lp_filter(cut, res, Cn, Ln)
    elif 'hp' in ftype:
	hp_filter(cut, res, Cn, Ln)
    elif 'bp' in ftype:
	bp_filter(fh, fl, res, Cn, Ln)
    else:
	raise Exception("Unsuported Filter Type!!!")


denorm(f, r, order, ftype, coef)
