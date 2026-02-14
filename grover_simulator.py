from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram, array_to_latex
from qiskit.result import marginal_distribution
from qiskit.circuit.library import UGate, PhaseOracleGate
from numpy import pi, random
from qiskit.circuit.library import QFT, CDKMRippleCarryAdder
from qiskit_aer.noise import NoiseModel, depolarizing_error

from sympy import symbols
from sympy.logic.boolalg import SOPform
import math


class GroverSimulator:
    def __init__(self, qubits, solutions, iterations, error_rate):
        self.qubit_count = qubits
        self.solution_count = solutions
        self.iterations = iterations
        self.error_rate = error_rate


        self.solution_list = []

        self.circuit = QuantumCircuit(self.qubit_count, self.qubit_count)
        self.grover_operator = self.iteration()

        self.circuit.h(range(self.qubit_count))
        for x in range(iterations):
            self.circuit = self.circuit.compose(self.grover_operator)
        
        for x in range(self.qubit_count):
            self.circuit.measure(x, x)
        
        #display(self.circuit.draw(output="mpl"))
        
        #noise
        noise = NoiseModel()
        noise.add_all_qubit_quantum_error(depolarizing_error(error_rate, 1), ['h'])

        self.sim = AerSimulator(noise_model=noise)
        self.t_q = transpile(self.circuit, self.sim)


    def int_to_bit_tuple(self, n, width):
        self.solution_list.append(str(format(n, f"0{width}b")))
        return tuple(int(b) for b in format(n, f"0{width}b"))

    def iteration(self):
        iter = QuantumCircuit(self.qubit_count)

        #generate solutions
        solutions = []
        for x in range(self.solution_count):
            print(f"{x}, {self.qubit_count}")
            solutions.append(self.int_to_bit_tuple(x, self.qubit_count))
        
        vars = symbols(f'a0:{self.qubit_count}')
        
        expression = SOPform(vars, solutions)

        print(f"{vars} {solutions} {expression}")

        var_order = [str(v) for v in vars]
        g = PhaseOracleGate(str(expression), var_order=var_order)
        iter = iter.compose(g)
        
        #reflection around the mean
        iter.h(range(self.qubit_count))
        iter.x(range(self.qubit_count))

        iter.h(self.qubit_count-1)
        iter.mcx(list(range(self.qubit_count-1)), self.qubit_count-1)
        iter.h(self.qubit_count-1)
        
        iter.x(range(self.qubit_count))
        iter.h(range(self.qubit_count))
        
        #display(iter.draw(output="mpl"))

        print(self.solution_list)

        return iter.to_gate()
    
    def run(self):
        job = self.sim.run(self.t_q, shots=1)
        result = job.result()

        return result.get_counts()

    def simulate(self, runs):
        for x in range(runs):
            print("Running")
    
    def get_theta(self):
        return math.asin(math.sqrt(self.solution_count*1.0/math.pow(2, self.qubit_count)))
    
    def get_angle(self):
        if (self.error_rate == 0):
            return 2 * self.get_theta() * self.iterations + self.get_theta()
        else:
            error = self.error_rate * 2 * self.qubit_count
            theta = self.get_theta()
            p = math.pow(math.e, -error*self.iterations) \
                * math.pow(math.sin((2*self.iterations + 1)*theta), 2) \
                + (1 - math.pow(math.e, -error*self.iterations)) * self.solution_count*1.0 / math.pow(2, self.qubit_count)
            return math.asin(math.sqrt(p))

#g = GroverSimulator(3, 2, 2)

#print(g.get_angle())
