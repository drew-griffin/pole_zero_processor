"""
 file: expression_class.py
 author: Drew Seidel (dseidel@pdx.edu)
 description: implements ExpressionClass 
 brief (also highlighted in main.py and throughout document):
    - class containing fs information including parsed given information (poles/zeros, 
            limits, s symbol, and s_func)
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

import itertools
import signal
import sys
from sympy import Symbol
import sympy as sp
import matplotlib.pyplot as plt
import numpy as np

# pylint: disable=locally-disabled, multiple-statements, fixme, invalid-name
# pylint: disable=locally-disabled, multiple-statements, fixme, pointless-string-statement


class ExpressionClass:
    """implementation of ExpressionClass
    See main.py, the README, and further comments in methods for specifics
    """

    def __init__(self, pz, limits, type, s_var, s_func):
        """class initialized variables"""
        self.pz = pz
        self.limits = limits
        self.type = type
        self.s_var = s_var
        self.s_func = s_func

        """general processing variables"""
        self.max = 0  # max pole/zero
        self.indices = []  # list described in process_bode

        """time-domain symbol, and function to be generated"""
        self.t_var = Symbol("t")  # type: ignore
        self.t_func = None  # to be determined in process_time_domain() method

        """frequency domain processing, labeling, and substitution variables"""
        self.fs_processed = False
        self.labels_all_s = []
        self.annotate_labels_all_s = []
        self.fs_all_s = []

        """time domain processing, labeling, and substitution variables"""
        self.ts_processed = True
        self.labels_all_t = []
        self.ts_all_t = []

    def timeout_handler(self, signum, frame):
        """callback handler for inability to process inverse laplace in 20 seconds"""
        print(f"Sympy couldn't perform inverse laplace on transfer function")
        sys.exit(1)

    def process_bode(self):
        """implement class method for processing bode"""
        num_dimensions = len(self.limits)
        dimension_sizes = self.type

        """
            Generate all possible combinations of self.indices
            for example, if limits = {"p1" : (1,2,3), "p2" : (1,2,3)}
            self.indices gets [range(0,3), range(0,3)] 
            this allows for dynamic number of for loops 
            which is required for varying number of poles/zeros
        """
        self.indices = []
        for dimension in range(num_dimensions):
            self.indices.append(range(dimension_sizes[dimension]))

        """
            itertools.product calculates all combinations unpacked self_indices
            for example: 
            limits = {"p1" : (1,2,3), "p2" : (1,2,3)}
            self.indices = [range(0,3), range(0,3)] 
            combination will be: 
            0, 0
            0, 1
            0, 2
            1, 0 
            1, 1
            1, 2
            2, 0
            2, 1
            2, 2
            where the last poles/zeros in limits loop the
            quickest as they are the last range indexes supplied
            values is a list for the current substitutions that need to be made 
            at the index of the pole/zero
            In the example above: 
            values = [1, 1]
            values = [1, 2]
            ...
            values = [3, 3]
            iterating through the last poles/zeros the quickest as specified. 
        """
        label = np.chararray(len(self.pz), itemsize=3)
        full_label = []
        for combination in itertools.product(*self.indices):
            values = [
                self.limits[dimension][index]
                for dimension, index in enumerate(combination)
            ]
            mag_values = [abs(val) for val in values]
            if max(mag_values) > self.max:  # calculate maximum pole/zero magnitude
                self.max = max(mag_values)
            for index in range(
                len(combination)
            ):  # create label based on combination length
                if self.type[index] == 1:  # and self.type[index] containing 1,2,3
                    label[
                        index
                    ] = "typ"  # representation type for limits (typ, min-max, etc.)
                elif self.type[index] == 2:
                    label[index] = "min" if combination[index] == 0 else "max"
                elif self.type[index] == 3:
                    label[index] = (
                        "min"
                        if combination[index] == 0
                        else "typ"
                        if combination[index] == 1
                        else "max"
                    )

            # create both legend labels 'p1 = typ, p2 = min' etc.
            # and annotate labels 'p1 = 1, p2 = 1' etc.
            label = label.astype(str)
            full_label = [val for label_pair in zip(self.pz, label) for val in label_pair]  # type: ignore
            annotate_label = [val for label_pair in zip(self.pz, values) for val in label_pair]  # type: ignore

            # append to list of lists for all substitutions
            self.labels_all_s.append(full_label)
            self.annotate_labels_all_s.append(annotate_label)

            # make all necessary substitutions and append to list self.fs_all_s
            substitutions_dict = {key: value for key, value in zip(self.pz, list(values))}  # type: ignore
            fs = self.s_func.subs(substitutions_dict)
            self.fs_all_s.append(fs)

        self.fs_processed = True

    def plot_bode(self, annotate_plot=False):
        """implement plot bode class method"""
        if not self.fs_processed:
            print("Error, bode not processed. Process first")
            sys.exit(1)

        # range needed for proper display
        w_max = int(np.log10(self.max))
        w = np.logspace(0, abs(w_max) + 10, 1000)

        # declare plot
        fig1, ax1 = plt.subplots(1, 1, figsize=(15, 8))
        fig2, ax2 = plt.subplots(1, 1, figsize=(15, 8))

        for tf, label, annotate in zip(self.fs_all_s, self.labels_all_s, self.annotate_labels_all_s):  # type: ignore
            h_lambda = sp.lambdify(
                self.s_var, tf
            )  # lambdify for quick processing of jw for s
            # Evaluate the magnitude of the transfer function for each frequency
            magnitude = [
                20 * np.log10(abs(h_lambda(1j * wi))) for wi in w
            ]  # Convert to dB
            phase = [np.angle(h_lambda(1j * wi), deg=True) for wi in w]
            # Plot the magnitude response
            ax1.semilogx(w, magnitude, label=label)
            ax2.semilogx(w, phase, label=label)

            # annotations, can be turned on and off by user in argument in call to method
            # best for lower number of poles/zeros and limits
            if annotate_plot == True:
                x_list = []
                for index in range(0, len(annotate), 2):  # parse annotation label
                    x_shift = 0  # used to shift if multiple values in same place
                    str = f"{annotate[index]} = {annotate[index + 1]}"
                    if annotate[index][0] == "p":  # if pole, x value is reciprocal
                        x = 1 / annotate[index + 1]
                    else:
                        x = annotate[index + 1]
                    if x in x_list:  # if pole/zero is repeated shift the arrow
                        x_shift = 10
                    x_list.append(x)
                    y_coord = np.argmin(
                        np.abs(w - x)
                    )  # find index closes to frequency of pole/zero

                    # annotate the plot with pole/zero using and arrow
                    ax1.annotate(
                        str,
                        xy=(x, magnitude[y_coord]),
                        xytext=(x + x_shift, magnitude[y_coord] - 20),
                        arrowprops=dict(facecolor="black", shrink=0.05),
                    )

        ax1.set_xlabel("Frequency [rad/s]")
        ax1.set_ylabel("Magnitude [dB]")
        ax1.set_title(f"Frequency Magnitude (Bode) Plot for {self.s_func}")
        ax1.grid(True)
        ax1.legend(loc="upper right")

        ax2.set_xlabel("Frequency [rad/s]")
        ax2.set_ylabel("Phase [degrees]")
        ax2.set_title(f"Frequency Phase (Bode) Plot for {self.s_func}")
        ax2.grid(True)
        ax2.legend(loc="upper right")

        plt.tight_layout()

    def process_time_domain(self):
        """implement method for processing time domain"""

        # setup timeout handler for inverse laplace timeout and set callback handler
        signal.signal(signal.SIGALRM, self.timeout_handler)
        timeout = 20  # 20 seconds
        step = (
            1 / self.s_var
        )  # 1/s is unit step. apply in s-domain for normal evaluation

        try:  # try to perform the inverse laplace transform in 20 seconds or less
            signal.alarm(timeout)
            self.t_func = sp.inverse_laplace_transform(
                (self.s_func * step), self.s_var, self.t_var
            )
            signal.alarm(0)
        except TimeoutError:  # if not signal cannot be processed
            print("Timeout error")

        # iterate through combinations (as described in process_bode)
        # in order to perform time domain substitutions
        for combination in itertools.product(*self.indices):
            values = [
                self.limits[dimension][index]
                for dimension, index in enumerate(combination)
            ]
            substitutions_dict = {key: value for key, value in zip(self.pz, list(values))}  # type: ignore
            full_label = [
                val for label_pair in zip(self.pz, values) for val in label_pair
            ]
            ts_current = self.t_func.subs(
                substitutions_dict
            )  # perform for given values
            self.ts_all_t.append(ts_current)  # append evaluated expression to list
            self.labels_all_t.append(full_label)  # append label to full label list

        self.ts_processed = True

    def settling_calc(self, magnitude):
        """determine settling calc for a given magnitude - pass in the last 10-30%
        of the magnitude for good settled response calculation
        """
        mag_min = np.min(magnitude)
        mag_max = np.max(magnitude)
        # the percentage change between the max and min is less than
        # 20% the response has settled, else, it has not
        if (mag_max - mag_min) / mag_min < 0.20:
            return True
        else:
            return False

    def plot_time_domain(self):
        """class method for plotting time domain response when given a unit step function (in freq domain - 1/s)"""
        if not self.ts_processed:
            print("Error, time domain not processed. Process first")
            sys.exit(1)

        time = np.linspace(0, self.max * 10, 1000)  # time range using max pole/zero

        fig3, ax3 = plt.subplots(1, 1, figsize=(15, 8))  # pylint: disable=invalid-name
        for ts_current, label in zip(self.ts_all_t, self.labels_all_t):
            t_lambda = sp.lambdify(
                self.t_var, ts_current
            )  # lambdify for quick substitution of time for t
            magnitude = [t_lambda(ti) for ti in time]
            label.append("settled")
            settled = self.settling_calc(
                magnitude[-100:]
            )  # pass in last 100 values of magnitude (10% as 100/1000 = 10%)
            if settled:
                label.append("True")
            else:
                print(f"Time domain function for {ts_current} does not settle")
                label.append("False")
            ax3.plot(time, magnitude, label=label)

        ax3.set_xlabel("Time(s)")
        ax3.set_ylabel("Magnitude")
        ax3.set_title(f"Time-domain unit-step response for {self.t_func}")
        ax3.grid(True)
        ax3.legend(loc="upper right")

        plt.tight_layout()

    def display_all_plots(self):
        """display all the plots processed"""
        plt.show()
