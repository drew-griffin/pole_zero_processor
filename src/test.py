"""
 file: test.py
 author: Drew Seidel (dseidel@pdx.edu)
 description: implements test_func
 brief:       change fs function to evaluate and limits here
"""
from sympy import Symbol
import process

# pylint: disable=locally-disabled, multiple-statements, fixme, invalid-name
# pylint: disable=locally-disabled, multiple-statements, fixme, pointless-string-statement


def test_func():
    """Test functions"""
    s = Symbol("s")

    # random/unknown response, expression, test complex input
    """
    p1 = Symbol("p1")  
    p2 = Symbol("p2")  
    p3 = Symbol("p3")  
    p4 = Symbol("p4")  
    sp = 1 / (
        (p1 * (s**3)) + (p2 * (s**2)) + (p3 * s) + p4
    )  
    limits = {"p1": 1/10e3+1j, "p2": (1/1e6, 1/1e3, 1/1e1), "p3": (1+1j, 2, 3), "p4": (1, 2, 3)}
    """

    # single pole low pass 1k rad/s
    """
    p1 = Symbol("p1")
    sp = 1 / (s * p1 + 1)
    limits = {"p1": 1/1e3}
    """

    # band-pass filter with wc (p1) = 1k rad/s, Q(p2) = 10, Gain(z1) = (1,1000)
    # sympy cannot process inverse laplace of unit-step driven function
    # to look at bode plots, uncomment lines 70,71 of process.py
    """
    p1 = Symbol("p1")
    p2 = Symbol("p2")
    z1 = Symbol("z1")
    sp = z1 * ((p1/p2) * s) / (s ** 2 + ((p1 * s) / p2) + p1 ** 2)
    limits = {"p1": (1e3,), "p2": 10, "z1": (1, 1000)}
    """

    # single pole low pass 1M rad/s, 1k rad/s , 10 rad/s
    # gain of 1, 2, 3
    p1 = Symbol("p1")
    z1 = Symbol("z1")
    sp = 1 * z1 / (s * p1 + 1)
    limits = {"p1": (1 / 1e6, 1 / 1e3, 1 / 1e1), "z1": (1, 2, 3)}

    # add your test here

    process.process_fs(sp, s, limits)
