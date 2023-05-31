"""
 file: main.py
 author: Drew Seidel (dseidel@pdx.edu)
 description: implements process_fs 
 brief: 
    - parses s_domain_func, s_var ('s' symbol), limits
    - ensures limits are in order (even complex) 
    - allows both tuple, and single value for typ
        - appends to a tuple for consistency 
    - split poles and zeros and limits to separate lists for ease of looping 
    - ensures matching between supplied poles/zeros, limits dict, and provided s function
    - instantiates expression class passing in
        - pole/zero symbol list 
        - limits list 
        - type (list containing type for limits at a given index)
            - 1 is single value or 'typ'
            - 2 is two value or 'min', 'max'
            - 3 is three values or 'min', 'typ', 'max'
        - s_var - symbol to substitute jw in (normally 's' by convention)
        - s_func - provided s_func
"""

import sys
from sympy import Symbol
from expression_class import ExpressionClass


def process_fs(s_domain_func, s_var, limits):
    """process_fs function implementation"""
    print(f"Processing function '{s_domain_func}'")
    print(f"Using '{s_var}' and the following limits:")
    print(limits)
    keys = list(limits.keys())  # split dict for ease of looping and using class later
    limit_values = list(limits.values())
    limit_values_type = [] # see type explanation in file header
    for index, value in enumerate(limit_values):
        if isinstance(value, tuple):  # if tuple, check ordering. min < typ < max
            temp_tuple = tuple(
                abs(val) for val in value
            )  # convert to magnitude to account for complex numbers
            if temp_tuple == tuple(sorted(temp_tuple)):  # check ascending order
                limit_values_type.append(len(value))
            else:
                print("tuple is not in ascending order")
                sys.exit(1)
        else:  # if single number, check its a number
            try:
                float(abs(value)) # can we do this operation?
            except:
                print("Error, number is not supplied.")
                sys.exit(1)
            limit_values_type.append(1)  # type is 1 for this index
            limit_values[index] = (value,)  # append as if it were a tuple

    for pz in keys:  # check all poles/zeros are represented in the passed function
        if Symbol(pz) not in s_domain_func.free_symbols:
            print("Discrepancy between s-domain-function and pole/zero's provided")
            sys.exit(1)

    fs = ExpressionClass(  # instantiate ExpressionClass with parsed values
        limits=limit_values,
        pz=keys,
        s_var=s_var,
        s_func=s_domain_func,
        type=limit_values_type,
    )

    fs.process_bode()
    fs.plot_bode(annotate_plot=True)
    fs.process_time_domain()
    fs.plot_time_domain()
    fs.display_all_plots()
