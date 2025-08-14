
from qiskit.algorithms.optimizers import COBYLA, SPSA, NFT

def get_optimizer(optimizer_name, maxiter):
    """Returns configured optimizer"""
    if optimizer_name.lower() == "cobyla":
        return COBYLA(maxiter=maxiter)
    elif optimizer_name.lower() == "spsa":
        return SPSA(maxiter=maxiter)
    elif optimizer_name.lower() == "nft":
        return NFT(maxiter=maxiter)
    else:
        raise ValueError(f"Unknown optimizer: {optimizer_name}")