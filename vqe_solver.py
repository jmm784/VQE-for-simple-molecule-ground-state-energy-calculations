
from qiskit_aer.noise import NoiseModel
from qiskit_aer import AerSimulator
from qiskit.algorithms.minimum_eigensolvers import VQE
from qiskit.primitives import Estimator
from qiskit_nature.second_q.algorithms import GroundStateEigensolver
from noisy_estimator_2 import noisy_estimator

class VQEGroundStateSolver:
    def __init__(self, problem, NoisyEstimator=False):
        """
        Initialize the solver with an electronic structure problem
        
        Args:
            problem: ElectronicStructureProblem to solve
        """
        self.problem = problem 
        self.convergence_data = {}  # Stores all convergence histories
        self.is_noisy = NoisyEstimator
        self.estimator = self._arrange_estimator()


    def _arrange_estimator(self):
        if self.is_noisy:
            from noisy_estimator_2 import noisy_estimator
            return noisy_estimator
        from qiskit.primitives import Estimator
        return Estimator()
        
        
    def _store_history(self, combo_name):
        """Callback factory that guarantees data storage"""
        def callback(eval_count, parameters, energy, std):
            if not hasattr(self, 'convergence_data'):  # Redundant safety
                self.convergence_data = {}
            if combo_name not in self.convergence_data:
                self.convergence_data[combo_name] = []
            self.convergence_data[combo_name].append(energy)
            return False
        return callback
        
    def run_vqe(self, mapper_name, ansatz_name, optimizer_name, maxiter=100):
        """
        Run VQE and return only the final ground state energy
        
        Args:
            mapper_name: Name of the qubit mapper ('jordan_wigner', 'parity', 'bravyi_kitaev')
            ansatz_name: Name of the ansatz ('uccsd', 'twolocal', 'su2')
            optimizer_name: Name of the optimizer ('cobyla', 'spsa', 'nft')
            maxiter: Maximum number of iterations
            
        Returns:
            float: Final ground state energy in Hartrees
        """
        # Import components here to avoid circular imports
        from mappers import get_mapper
        from ansatzes import get_ansatz
        from optimizers import get_optimizer
        
        # Get the specified components
        mapper = get_mapper(mapper_name, self.problem.num_particles)
        
        ansatz = get_ansatz(
            ansatz_name,
            self.problem.num_spatial_orbitals,
            self.problem.num_particles,
            mapper
        )
        optimizer = get_optimizer(optimizer_name, maxiter)
        
        # Initialize VQE without any callback

        combo_name = f"{mapper_name}_{ansatz_name}_{optimizer_name}"
        
        vqe = VQE(
            estimator=self.estimator,
            ansatz=ansatz,
            optimizer=optimizer,
            initial_point=[0.0] * ansatz.num_parameters,
            callback=self._store_history(combo_name)  # Add this line
        )

        # Create and run the ground state solver
        solver = GroundStateEigensolver(mapper, vqe)
        result = solver.solve(self.problem)

        
        # Return only the final ground state energy
        return result.groundenergy + self.problem.nuclear_repulsion_energy + self.problem.reference_energy