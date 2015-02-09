#!/usr/bin/env python
# filter.py - shim to access different filter types and responses

if __name__ == "__main__":  # if run as standalone script
    import argparse

    parser = argparse.ArgumentParser(
            description="Print component values for given filter")

    parser.add_argument("-r", "--response",     type=str,   required=True,
            help="Filter response", choices=['bessel'])
    parser.add_argument("-t", "--type",         type=str,   required=True,
            help="Type of filter", choices=['lowpass', 'highpass', 'bandpass'])
    parser.add_argument("-o", "--order",        type=int,   required=True,
            help="Filter order", choices=range(1,11))
    parser.add_argument("-f", "--frequency",    type=float, required=True,
            help="Cutoff frequency (MHz)")
    parser.add_argument("-b", "--bandwidth",    type=float,
            help="Bandwidth (MHz)")
    parser.add_argument("-l", "--load",         type=float, default=50.0,
            help="Output load resistance (Ohm)")

    args = parser.parse_args()

    response    = args.response
    ftype       = args.type
    order       = args.order
    frequency   = args.frequency
    bandwidth   = args.bandwidth
    load        = args.load
