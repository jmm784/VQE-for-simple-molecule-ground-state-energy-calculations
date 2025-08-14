
import matplotlib.pyplot as plt

def plot_convergence(solver, mapper, ansatz, optimizer, problem, exact_energy=None):
    """
    Plot convergence for a specific combination
    
    Args:
        solver: Your VQEGroundStateSolver instance
        mapper: Mapper name (e.g. "jordan_wigner")
        ansatz: Ansatz name (e.g. "uccsd")
        optimizer: Optimizer name (e.g. "cobyla")
        exact_energy: Optional reference energy
    """
    combo_name = f"{mapper}_{ansatz}_{optimizer}"
    history = solver.convergence_data.get(combo_name, [])
    
    
    if not history:
        print(f"No data found for {combo_name}")
        return

    plot_data = history + problem.nuclear_repulsion_energy
    
    plt.figure(figsize=(10, 5))
    plt.plot(plot_data, 'b-o', markersize=4, linewidth=1)
    
    if exact_energy is not None:
        plt.axhline(y=exact_energy, color='r', linestyle='--', 
                   label=f"Exact: {exact_energy:.6f} Ha")
    
    plt.xlabel("Iteration", fontsize=12)
    plt.ylabel("Energy (Ha)", fontsize=12)
    plt.title(f"Convergence: {mapper} + {ansatz} + {optimizer}", fontsize=14)
    plt.grid(alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()