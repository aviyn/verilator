#!/usr/bin/env python3

# DESCRIPTION: Verilator: Verilog example python module
#
# This file ONLY is placed into the Public Domain, for any use,
# without warranty, 2017 by Wilson Snyder.
#======================================================================

import os
import sys
# Search the build directory
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "obj_dir"))

import Vtop


def main():
    # See a similar example walkthrough in the verilator manpage.
    Vtop.Verilated.parse_arguments(sys.argv[1:])

    # This is intended to be a minimal example.  Before copying this to start a
    # real project, it is better to start with a more complete example,
    # e.g. examples/c_tracing.

    # Create logs/ directory in case we have traces to put under it
    #Vtop.Verilated.mkdir("logs")
    Vtop.Verilated.traceEverOn(True)
    # Construct the Verilated model
    top = Vtop.Vtop()

    top.reset_l = 1
    top.clk = 0
    top.in_small = 1
    top.in_quad = 0x1234
    top.in_wide = 0x32222222211111111

    #time = 0
    # Simulate until $finish
    while not Vtop.Verilated.finished:
        top.clk = 0 if top.clk else 1
        Vtop.Verilated.timeInc(1)
        if top.clk:

            if Vtop.Verilated.time < 10:
                top.reset_l = 0
            else:
                top.reset_l = 1

            top.in_quad += 0x12

        top.eval()

        # Read outputs
        print("[ {} ] clk={} rstl={} iquad=0x{:x} -> oquad=0x{:x} owide=0x{:x}".format(
              Vtop.Verilated.time, top.clk, top.reset_l, top.in_quad, top.out_quad, top.out_wide))

    # Final model cleanup
    top.final()

    # Destroy model
    del top

    # Fin
    sys.exit(0);


if __name__ == "__main__":
    print("args:", sys.argv[1:])
    main()
