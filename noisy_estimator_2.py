
from qiskit_aer.noise import NoiseModel, depolarizing_error
from qiskit_aer.primitives import Estimator

# 1. Create noise model
noise_model = NoiseModel()
error = depolarizing_error(0.01, 1)  # 1-qubit error
noise_model.add_all_qubit_quantum_error(error, ['u', 'rx', 'ry', 'rz'])

# 2. Initialize noisy estimator
noisy_estimator = Estimator(
    backend_options={
        "method": "density_matrix",  # Required for noise
        "noise_model": noise_model
    },
    run_options={"seed": 42}  # Optional for reproducibility
)

