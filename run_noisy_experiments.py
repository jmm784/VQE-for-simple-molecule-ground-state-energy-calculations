
from molecules import get_molecule
from vqe_solver import VQEGroundStateSolver

ACTIVE_SPACES = {
    "h2": None,
    "lih": {"num_electrons": 2, "num_orbitals": 2},
    "beh2": {"num_electrons": 4, "num_orbitals": 3}
}

def run_all_noisy_combinations(molecule_name, maxiter=100):
    """Run all combinations for a given molecule"""
    mappers = ["jordan_wigner", "parity", "bravyi_kitaev"]
    ansatzes = ["uccsd", "twolocal", "su2"]
    optimizers = ["cobyla", "spsa", "nft"]
    
    problem = get_molecule(molecule_name, ACTIVE_SPACES.get(molecule_name))
    solver = VQEGroundStateSolver(problem, NoisyEstimator=True)
    
    results = {}
    
    for mapper in mappers:
        for ansatz in ansatzes:
            for optimizer in optimizers:
                print(f"Running {mapper} + {ansatz} + {optimizer}...")
                try:
                    energy = solver.run_vqe(
                        mapper_name=mapper,
                        ansatz_name=ansatz,
                        optimizer_name=optimizer,
                        maxiter=maxiter
                    )

                    results[f"{mapper}_{ansatz}_{optimizer}"] = energy
                    print(f"Final energy: {energy:.6f} Ha")
                except Exception as e:
                    print(f"Failed for {mapper}_{ansatz}_{optimizer}: {str(e)}")
                    results[f"{mapper}_{ansatz}_{optimizer}"] = {
                        "energy": None,
                        "error": str(e)
                    }
    
    return results
    