# ECE 508 Transfer Function Evaluation
## Drew Seidel (dseidel@pdx.edu)
## ECE 508 Python Workshop Assignment #2
# Brief
Takes in symbolic s-domain expression, poles and zeros, applies limits to them, produces bode plots, and plots time domain response given a unit step. 

# Repository organization 
- src: contains all python src code 
    - main.py - invokes program and provides documentation
    - test.py - change function to evaluate here. For example: 
    ``` python
     p1 = Symbol("p1")
     z1 = Symbol("z1")
     sp = 1 * z1 / (s * p1 + 1)
     limits = {"p1": (1/1e6, 1/1e3, 1/1e1), "z1": 1}
    ```
    - process.py - parses input information and processes using ExpressionClass in expression_class.py
    - expression_class.py - implements ExpressionClass
- seidel_report.pdf - contains supplemental plots, and documentation for program


# To run program (in terminal): 
To run this program, navigate to the src directory of this repository and run main.py
``` bash
cd 'your_path_to_this_repository'/src
```
To run program
```
python3 main.py
```