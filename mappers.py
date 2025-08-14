
from qiskit_nature.second_q.mappers import (
    JordanWignerMapper,
    ParityMapper,
    BravyiKitaevMapper
)

def get_mapper(mapper_name, num_particles=None):
    """Returns configured qubit mapper"""
    if mapper_name.lower() == "jordan_wigner":
        return JordanWignerMapper()
    elif mapper_name.lower() == "parity":
        return ParityMapper()
    elif mapper_name.lower() == "bravyi_kitaev":
        return BravyiKitaevMapper()
    else:
        raise ValueError(f"Unknown mapper: {mapper_name}")