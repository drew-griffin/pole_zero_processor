"""
 file: main.py
 author: Drew Seidel (dseidel@pdx.edu)
 description: main function. Finds test function, 
 parses via processes via process_fs, and interfaces 
 with expression_class to produces results. 
 brief: 
    - Process the fs function when main is called 
    - test.py - update the fs expression you would like to evaluate here 
    - process.py - implements process_fs functionality. Interfaces with the expression_class
    - expression_class.py: 
        - class methods: 
            - timeout_handler - is invoked after trying to perform inverse laplace 
                for 20 seconds. If so exit program as it can't be done or is to 
                computationally intense
            - process_bode - processes all FS substitutions based on indexing 
                - utilizes itertools to calculate all dynamic looping needed
            - plot_bode - calculates frequency range and plots bode. 
                Pass in true for extra pole/zero annotations, false for not. 
                Too many pole/zero will get too clutter hence the option
            - process_time_domain - processes the inverse laplace given a unit step 
                (in frequency domain - 1/s)
            - settling calc - used to determine wether a function settles or not. Because
                function may settle for some poles/zeros and not others, and they are on the 
                same plot, the 5 unsettled spec is not used, and the settled versus unsettled 
                nature of the specific response is noted in the legend 
            - plot_time_domain - calculates time, settling, and plots time domain response 
            - display_all_plots - call to show all processed plots
         - note that process_bode must be processed before process_time_domain due to general flow
"""

import test

if __name__ == "__main__":
    test.test_func()
