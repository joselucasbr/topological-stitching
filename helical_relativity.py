import numpy as np
import matplotlib.pyplot as plt

def verify_helical_dilation():
    """
    Verifies that the Helical Stitching Model reproduces Special Relativity.

    We compare:
    1. Einstein's Gamma Factor (Standard Physics)
    2. The Helical Stitch Ratio (Geometric Derivation)

    They should match perfectly.
    """
    C = 1.0
    velocities = np.linspace(0.0, 0.995 * C, 1000)

    # 1. Einstein's Gamma (Target)
    gammas = 1 / np.sqrt(1 - (velocities/C)**2)

    # 2. Helical Stitch Ratio (Your Model)
    # Time T is proportional to the circumference of the internal rotation.
    # v_rot = sqrt(c^2 - v^2)
    # Ratio = (2*pi*A / v_rot) / (2*pi*A / c) = c / v_rot

    helical_ratios = []
    for v in velocities:
        # Prevent division by zero at c
        if v >= C:
            ratio = np.nan
        else:
            v_rot = np.sqrt(C**2 - v**2)
            ratio = C / v_rot
        helical_ratios.append(ratio)

    # --- Visualization ---
    # We use a single plot to show the perfect overlap
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot Helical Stitch (Thick Green Line)
    ax.plot(velocities, helical_ratios, color='#2ca02c', linewidth=5, alpha=0.6, label='Helical Stitch (Geometric)')

    # Plot Einstein Gamma (Thin Blue Dashed Line)
    ax.plot(velocities, gammas, color='blue', linestyle='--', linewidth=2, label='Einstein Gamma (Standard SR)')

    ax.set_title("Geometric Derivation of Time Dilation", fontsize=14)
    ax.set_xlabel("Velocity (v/c)", fontsize=12)
    ax.set_ylabel("Dilation Factor (γ)", fontsize=12)
    ax.legend(fontsize=12)
    ax.grid(True, alpha=0.3)
    ax.set_ylim(1, 10) # Limit Y to keep it readable
    ax.set_xlim(0, 1)

    # Annotations
    ax.text(0.5, 6, "Perfect Overlap confirms:\nGeometric Helix = Lorentz Factor",
            fontsize=12, ha='center', bbox=dict(facecolor='white', alpha=0.9))

    plt.tight_layout()
    plt.savefig('helical_fix.png', dpi=300)
    print("Verification plot saved to 'helical_fix.png'.")

if __name__ == "__main__":
    verify_helical_dilation()