
from qiskit_nature.second_q.drivers import PySCFDriver
from qiskit_nature.second_q.problems import ElectronicStructureProblem
from qiskit_nature.second_q.transformers import ActiveSpaceTransformer


def get_molecule(molecule_name, active_space=None):
    """Returns properly initialized ElectronicStructureProblem"""
    # Define molecules
    if molecule_name.lower() == "h2":
        driver = PySCFDriver(atom="H 0 0 0; H 0 0 0.735", basis="sto3g")
    elif molecule_name.lower() == "lih":
        driver = PySCFDriver(atom="Li 0 0 0; H 0 0 1.6", basis="sto3g")
    elif molecule_name.lower() == "beh2":
        driver = PySCFDriver(atom="Be 0 0 0; H 0 0 1.3; H 0 0 -1.3", basis="sto3g")
    else:
        raise ValueError(f"Unknown molecule: {molecule_name}")
    
    # Run driver to get electronic structure data
    es_problem = driver.run()
    
    # Apply active space transformation if specified
    if active_space is not None:
        transformer = ActiveSpaceTransformer(
            num_electrons=active_space["num_electrons"],
            num_spatial_orbitals=active_space["num_orbitals"]
        )
        es_problem = transformer.transform(es_problem)
        
    
    # Get the second quantized operators
    second_q_ops = es_problem.second_q_ops()
    
    # Create the electronic structure problem
    problem = ElectronicStructureProblem(es_problem.hamiltonian)
    problem.num_particles = es_problem.num_particles
    problem.num_spatial_orbitals = es_problem.num_spatial_orbitals

    hamiltonian: ElectronicEnergy = es_problem.hamiltonian
    nuclear_repulsion = hamiltonian.nuclear_repulsion_energy  # Directly accessible

    if active_space is not None:
        frozen_core_energy = hamiltonian.constants["ActiveSpaceTransformer"]  # Frozen core contribution
        reference_energy = frozen_core_energy
        problem.reference_energy = reference_energy
    else:
        problem.reference_energy = 0
    
    return problem
