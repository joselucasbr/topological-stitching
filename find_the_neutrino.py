import numpy as np
from scipy.optimize import fsolve

# Constants
MASS_ELECTRON_MEV = 0.51099895000  # CODATA
N_ELECTRON = 3  # Our established anchor

def solve_for_mass_proxy(N):
    """
    Solves Jose's Stability Equation and applies Scaling Hypothesis:
    Mass ~ N * sqrt(1 - m^2)
    """
    def equation(m):
        if abs(m) > 1: return 100 
        return np.sqrt(1 - m**2) - m * (np.pi * N - np.arccos(-m))

    guess = 1.0 / (np.pi * N)
    root = fsolve(equation, guess)
    m = root[0]
    
    # The Scaling Hypothesis
    return N * np.sqrt(1 - m**2)

# --- 1. Establish the Scale (The "Ruler") ---
mass_proxy_e = solve_for_mass_proxy(N_ELECTRON)
print(f"ANCHOR (Electron N=3): Mass Proxy = {mass_proxy_e:.6f}")
print("-" * 60)

# --- 2. Calculate N=2 ---
print("Calculating N=2 Candidate...")
mass_proxy_2 = solve_for_mass_proxy(2)
ratio_2 = mass_proxy_2 / mass_proxy_e
predicted_mass_2_mev = ratio_2 * MASS_ELECTRON_MEV

print(f"N=2 Mass Proxy: {mass_proxy_2:.6f}")
print(f"Ratio (N=2 / Electron): {ratio_2:.6f}")
print(f"PREDICTED MASS (MeV): {predicted_mass_2_mev:.6f} MeV")
print(f"PREDICTED MASS (eV):  {predicted_mass_2_mev * 1e6:.6f} eV")

# --- 3. Calculate N=1 (Just to check, should be near zero) ---
print("-" * 60)
print("Calculating N=1 (Photon check)...")
mass_proxy_1 = solve_for_mass_proxy(1)
ratio_1 = mass_proxy_1 / mass_proxy_e
predicted_mass_1_mev = ratio_1 * MASS_ELECTRON_MEV

print(f"N=1 Mass Proxy: {mass_proxy_1:.6f}")
print(f"PREDICTED MASS (MeV): {predicted_mass_1_mev:.9f} MeV")

# --- Contextual Comparison ---
print("-" * 60)
print("COMPARISON DATA:")
print(f"Neutrino Upper Bound: < 0.00000012 MeV (0.12 eV)")
print(f"Electron Mass:        0.510999 MeV")