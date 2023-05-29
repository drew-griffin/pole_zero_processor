

"""Example setup code for assignment 2"""
from sympy import Symbol
from expression import ExpressionClass
import sys
import numpy as np


def process_fs(s_domain_func, s_var, limits):
    """You need to write this function"""
    print(f"Processing function '{s_domain_func}'")
    print(f"Using '{s_var}' and the following limits:")
    print(limits)
    keys = list(limits.keys())
    limit_values = list(limits.values())
    #print(len(limit_values))
    #print(keys)
    limit_values_type = [] #list to be filled with 0, 1, 2, 3 for singular number, tuple with 1, 2, 3 items respectively
    for index, value in enumerate(limit_values):
        if isinstance(value, tuple): 
            temp_tuple = tuple(abs(val) for val in value) #convert to magnitude to account for complex numbers
            if temp_tuple == tuple(sorted(temp_tuple)): #check ascending order
                limit_values_type.append(len(value))
            else: 
                print("tuple is not in ascending order")
                sys.exit(1)
        else: 
            try: 
                temp_val = float(abs(value))
            except: 
                print("Error, number is not supplied.")
                sys.exit(1)
            #print(limit_values)
            limit_values_type.append(1)
            limit_values[index] = (value,)
        
    for pz in keys: 
        if Symbol(pz) not in s_domain_func.free_symbols:
            print("Discrepancy between s-domain-function and pole/zero's provided")
            sys.exit(1)
    
    fs = ExpressionClass(limits=limit_values, pz=keys, s_var=s_var, s_func=s_domain_func, type=limit_values_type)
    fs.process_bode()
    fs.plot_bode()
    fs.process_time_domain()
    fs.plot_time_domain()
    fs.display_all_plots()
    



def test_func():
    """Test code setup"""
    s = Symbol("s")         # pylint: disable=invalid-name
    """
    p1 = Symbol("p1")       # pylint: disable=invalid-name
    p2 = Symbol("p2")       # pylint: disable=invalid-name
    p3 = Symbol("p3")       # pylint: disable=invalid-name
    p4 = Symbol("p4")       # pylint: disable=invalid-name
    sp = 1 / ((p1* (s**4)) + (p2*(s**3)) + (p3*(s**2)) + (p4*s))  # pylint: disable=invalid-name
    limits = {"p1": 10e3, "p2": (1,10e3+1j,20e3+2j), "p3": (1,2,3), "p4": (1,2,3)}
    """
    
    p1 = Symbol("p1")
    sp = 1/p1 / (s + 1/p1)
    limits = {"p1" : 1e6}
    
    process_fs(sp, s, limits)


# Run the example_code when this file is executed
if __name__ == "__main__":
    test_func()
