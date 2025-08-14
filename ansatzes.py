from qiskit_nature.second_q.circuit.library import HartreeFock, UCCSD
from qiskit.circuit.library import TwoLocal, EfficientSU2

def get_ansatz(ansatz_name, num_spatial_orbitals, num_particles, mapper):
    """Returns ansatz circuit with HF initial state"""
    # Create Hartree-Fock initial state
    hf_state = HartreeFock(num_spatial_orbitals, num_particles, mapper)
    
    if ansatz_name.lower() == "uccsd":

        return UCCSD(
            num_spatial_orbitals,
            num_particles,
            mapper,
            initial_state=hf_state
        )
        
    elif ansatz_name.lower() == "twolocal":
        return TwoLocal(hf_state.num_qubits, rotation_blocks=["ry"], entanglement_blocks="cx", entanglement="linear", reps=3)

    elif ansatz_name.lower() == "su2":

        su2 = EfficientSU2(
            num_qubits=hf_state.num_qubits,
            reps=3,  
            entanglement="linear",  
            skip_final_rotation_layer=True,  
            insert_barriers=True  
            )
        full_circuit = hf_state.compose(su2)
        
        return full_circuit
    else:
        raise ValueError(f"Unknown ansatz: {ansatz_name}")