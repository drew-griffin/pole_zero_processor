import itertools
import signal
import sys
from sympy import Symbol
from sympy import symbols
import sympy as sp
import matplotlib.pyplot as plt
import numpy as np


def timeout_handler(signum, frame):
    print(f"Sympy couldn't perform inverse laplace on transfer function")
    sys.exit(1)


class ExpressionClass:
    """"""

    def __init__(self, pz, limits, type, s_var, s_func):
        self.pz = pz
        self.limits = limits
        self.type = type
        self.s_var = s_var
        self.s_func = s_func
        self.t_func = None
        self.min = float("inf")
        self.max = 0
        self.indices = []

        self.t_var = Symbol("t")
        self.t_func = 0

        self.fs_processed = False
        self.labels_all_s = []
        self.fs_all_s = []

        self.ts_processed = True
        self.labels_all_t = []
        self.ts_all_t = []

    def process_bode(self):
        num_dimensions = len(self.limits)
        dimension_sizes = self.type  # [len(limits_list) for limits_list in self.limits]

        # Generate all possible combinations of self.indices
        self.indices = []
        for dimension in range(num_dimensions):
            self.indices.append(range(dimension_sizes[dimension]))

        # Iterate over the combinations of self.indices
        label = np.chararray(len(self.pz), itemsize=3)
        full_label = []
        fs_all = []
        labels_all = []
        for combination in itertools.product(*self.indices):
            values = [
                self.limits[dimension][index]
                for dimension, index in enumerate(combination)
            ]
            #print(values)
            mag_values = [abs(val) for val in values]
            if min(mag_values) < self.min:
                self.min = min(mag_values)
            if max(mag_values) > self.max:
                self.max = max(mag_values)
            for index in range(len(combination)):
                if self.type[index] == 1:
                    label[index] = "typ"
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
            #print(label)
            label = label.astype(str)
            full_label = [val for label_pair in zip(self.pz, label) for val in label_pair]  # type: ignore
            self.labels_all_s.append(full_label)

            substitutions_dict = {key: value for key, value in zip(self.pz, list(values))}  # type: ignore
            fs = self.s_func.subs(substitutions_dict)
            self.fs_all_s.append(fs)

        self.fs_processed = True

    def plot_bode(self):
        """"""
        if not self.fs_processed:
            print("Error, bode not processed. Process first")
            exit(1)

        w_min = int(np.log10(self.min)) - 10
        w_max = int(np.log10(self.max))
        w = np.logspace(-8, 8, 1000)
        #print(0, w_max)

        fig1, ax1 = plt.subplots(1, 1, figsize=(15, 8))
        fig2, ax2 = plt.subplots(1, 1, figsize=(15, 8))

        for tf, label in zip(self.fs_all_s, self.labels_all_s):  # type: ignore
            H_lambda = sp.lambdify(self.s_var, tf)
            # Evaluate the magnitude of the transfer function for each frequency
            magnitude = [
                20 * np.log10(abs(H_lambda(1j * wi))) for wi in w
            ]  # Convert to dB
            phase = [np.angle(H_lambda(1j * wi), deg=True) for wi in w]
            # Plot the magnitude response
            ax1.semilogx(w, magnitude, label=label)
            ax2.semilogx(w, phase, label=label)

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
        """"""
        signal.signal(signal.SIGALRM, timeout_handler)
        timeout = 10  # 10 seconds

        try:
            signal.alarm(timeout)
            self.t_func = sp.inverse_laplace_transform(
                self.s_func, self.s_var, self.t_var
            )
            signal.alarm(0)
        except TimeoutError:
            print("Timeout error")

      
        for combination in itertools.product(*self.indices):
            values = [
                self.limits[dimension][index]
                for dimension, index in enumerate(combination)
            ]
            #print(values)
            substitutions_dict = {key: value for key, value in zip(self.pz, list(values))}  # type: ignore
            full_label = [
                val for label_pair in zip(self.pz, values) for val in label_pair
            ]
            ts = self.t_func.subs(substitutions_dict)
            self.ts_all_t.append(ts)
            self.labels_all_t.append(full_label)

        self.ts_processed = True

    def plot_time_domain(self):
        if not self.ts_processed:
            print("Error, time domain not processed. Process first")
            exit(1)

        time = np.linspace(-1, 1e6, 1000)
        print(self.t_func)
        fig3, ax3 = plt.subplots(1, 1, figsize=(15, 8))
        for ts, label in zip(self.ts_all_t, self.labels_all_t):
            T_lambda = sp.lambdify(self.t_var, ts)
            #print(T_lambda)
            magnitude = [T_lambda(ti) * sp.Heaviside(ti) for ti in time]
            ax3.plot(time, magnitude, label=label)

        ax3.set_xlabel("Time(s)")
        ax3.set_ylabel("Magnitude")
        ax3.set_title(f"Time-domain unit-step response for {self.t_func}")
        ax3.grid(True)
        ax3.legend(loc="upper right")

        plt.tight_layout()

    def display_all_plots(self):
        plt.show()
