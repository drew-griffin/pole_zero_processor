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
    """
    p1 = Symbol("p1")  
    p2 = Symbol("p2")  
    p3 = Symbol("p3")  
    p4 = Symbol("p4")  
    sp = 1 / (
        (p1 * (s**4)) + (p2 * (s**3)) + (p3 * (s**2)) + (p4 * s)
    )  
    limits = {"p1": 1 / 10e3, "p2": 1 / 1e3, "p3": (1, 2, 3), "p4": (1, 2, 3)}
    """

    """
    p1 = Symbol("p1")  
    p2 = Symbol("p2")  
    sp = 1/(p1 * p2 * s)
    limits = {"p1" : (1,2,3), "p2" : (1,2,3)}
    """

    p1 = Symbol("p1")
    z1 = Symbol("z1")
    sp = 1 * z1 / (s * p1 + 1)
    limits = {"p1": (1 / 1e6, 1 / 1e3, 1 / 1e1), "z1": 1}

    process.process_fs(sp, s, limits)
