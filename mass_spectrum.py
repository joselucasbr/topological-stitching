import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

def analyze_mass_spectrum():
    """
    Analyzes the Geometric Mass Spectrum of the Topological Stitch.
    
    Hypothesis: Mass ~ N * v_rot
    Where v_rot = sqrt(1 - m^2) (The internal rotational velocity)
    
    We search for the specific Harmonics (N) that match the known lepton mass ratios.
    """
    
    # 1. Physics Data (Standard Model)
    # Masses in MeV/c^2
    M_e = 0.510998
    M_mu = 105.658
    M_tau = 1776.86
    
    Target_Ratio_Mu = M_mu / M_e
    Target_Ratio_Tau = M_tau / M_e
    
    print(f"--- Standard Model Targets ---")
    print(f"Muon/Electron Ratio: {Target_Ratio_Mu:.4f}")
    print(f"Tau/Electron Ratio:  {Target_Ratio_Tau:.4f}")
    print("-" * 40)

    # 2. The Stability Equation Solver
    def solve_drift(N):
        # Solves: sqrt(1 - m^2) = m * (pi*N - arccos(-m))
        func = lambda m: np.sqrt(1 - m**2) - m * (np.pi * N - np.arccos(-m))
        guess = 1.0 / (np.pi * N)
        m_sol = fsolve(func, guess)[0]
        return m_sol

    # 3. Mass Proxy Calculator
    def get_mass_proxy(N):
        m = solve_drift(N)
        v_rot = np.sqrt(1 - m**2)
        # Mass Hypothesis: M ~ N * v_rot
        return N * v_rot

    # 4. Calculate Anchor (Electron)
    # We established Electron is the first stable matter state (N=3)
    N_e = 3
    mass_proxy_e = get_mass_proxy(N_e)
    
    # 5. Generate Spectrum
    # We calculate the mass curve for N=1 to 12,000
    n_values = np.arange(2, 12000)
    mass_ratios = []
    
    print("Generating Mass Spectrum...")
    for n in n_values:
        m_proxy = get_mass_proxy(n)
        mass_ratios.append(m_proxy / mass_proxy_e)
    
    mass_ratios = np.array(mass_ratios)
    
    # 6. Find Matches
    # Muon Match
    idx_mu = np.argmin(np.abs(mass_ratios - Target_Ratio_Mu))
    N_mu = n_values[idx_mu]
    ratio_mu = mass_ratios[idx_mu]
    
    # Tau Match
    idx_tau = np.argmin(np.abs(mass_ratios - Target_Ratio_Tau))
    N_tau = n_values[idx_tau]
    ratio_tau = mass_ratios[idx_tau]
    
    print(f"\n--- Geometric Predictions ---")
    print(f"Electron (Anchor): N = {N_e}")
    print(f"Muon Prediction:   N = {N_mu}  | Ratio = {ratio_mu:.4f} | Error = {abs(1 - ratio_mu/Target_Ratio_Mu)*100:.4f}%")
    print(f"Tau Prediction:    N = {N_tau} | Ratio = {ratio_tau:.4f} | Error = {abs(1 - ratio_tau/Target_Ratio_Tau)*100:.4f}%")

    # 7. Plotting
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Plot the Curve
    ax.plot(n_values, mass_ratios, color='gray', alpha=0.5, label='Geometric Mass Constraint')
    
    # Plot the Particles
    ax.scatter([N_e], [1], color='blue', s=100, label='Electron (N=3)', zorder=10)
    ax.scatter([N_mu], [ratio_mu], color='green', s=100, label=f'Muon (N={N_mu})', zorder=10)
    ax.scatter([N_tau], [ratio_tau], color='red', s=100, label=f'Tau (N={N_tau})', zorder=10)
    
    # Annotations
    ax.annotate(f"Muon\nErr: {abs(1 - ratio_mu/Target_Ratio_Mu)*100:.2f}%", 
                (N_mu, ratio_mu), xytext=(N_mu-200, ratio_mu+500), 
                arrowprops=dict(arrowstyle="->"))
    
    ax.annotate(f"Tau\nErr: {abs(1 - ratio_tau/Target_Ratio_Tau)*100:.3f}%", 
                (N_tau, ratio_tau), xytext=(N_tau-2000, ratio_tau-500), 
                arrowprops=dict(arrowstyle="->"))

    ax.set_title("The Lepton Mass Hierarchy: Derived from Topological Harmonics", fontsize=16)
    ax.set_xlabel("Harmonic Number (N)", fontsize=12)
    ax.set_ylabel("Mass Ratio (relative to Electron)", fontsize=12)
    ax.set_yscale('log')
    ax.set_xscale('log')
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(fontsize=12)
    
    plt.tight_layout()
    plt.savefig('mass_hierarchy.png', dpi=300)
    print("\nChart saved to mass_hierarchy.png")

if __name__ == "__main__":
    analyze_mass_spectrum()