#!/usr/bin/env python3
"""predict_phase_shift.py

Predict interferometer phase shifts for a given Δv, k_eff, and T.
Also computes required number of shots to reach a target significance
for a given per-shot phase noise.
Outputs a CSV table and a plot (PNG).

Usage (basic):
    python predict_phase_shift.py

You can also import functions from this module in other scripts:
    from predict_phase_shift import build_table, plot_phase_shifts
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import argparse
import sys
import os

def delta_phi(k_eff, delta_v, T):
    """Compute interferometer phase shift: Delta phi = k_eff * delta_v * T"""
    return k_eff * delta_v * T

def required_shots_for_detection(delta_phi_signal, phase_noise_per_shot, sigma=5.0):
    """Compute required number of shots to reach detection at 'sigma' significance.
    Assumes independent, identically distributed per-shot phase noise (Gaussian).
    N = (sigma * sigma_phi / delta_phi)^2
    """
    if delta_phi_signal == 0:
        return np.inf
    return (sigma * phase_noise_per_shot / abs(delta_phi_signal))**2

def build_table(delta_v=1e-12, k_eff_factors=[50,100,200], T_values=[0.5,1.0,5.0],
                wavelength=780e-9, per_shot_noise=1e-3, target_sigma=5.0):
    """Build a pandas DataFrame summarizing Delta phi and required shots for detection.
    k_eff_factors: multiples of single-photon k (i.e., N_LMT)
    wavelength: laser wavelength [m]
    """
    k_single = 2 * np.pi / wavelength
    rows = []
    for N in k_eff_factors:
        k_eff = N * k_single
        for T in T_values:
            dphi = delta_phi(k_eff, delta_v, T)
            req_shots = required_shots_for_detection(dphi, per_shot_noise, sigma=target_sigma)
            rows.append({
                "N_LMT": N,
                "k_eff [1/m]": f"{k_eff:.3e}",
                "T [s]": T,
                "delta_v [m/s]": f"{delta_v:.3e}",
                "Delta_phi [rad]": f"{dphi:.3e}",
                "per_shot_noise [rad]": per_shot_noise,
                f"shots_for_{target_sigma}sigma": int(np.ceil(req_shots)) if np.isfinite(req_shots) else np.inf
            })
    df = pd.DataFrame(rows)
    return df

def plot_phase_shifts(df, outfile_png="phase_shifts.png"):
    """Plot Delta_phi vs T for different k_eff factors."""
    plt.figure(figsize=(8,5))
    df_plot = df.copy()
    df_plot["k_eff_factor"] = df_plot["N_LMT"].astype(int)
    df_plot["T"] = df_plot["T [s]"].astype(float)
    df_plot["Delta_phi"] = df_plot["Delta_phi [rad]"].apply(lambda s: float(s))
    for N, group in df_plot.groupby("k_eff_factor"):
        plt.plot(group["T"], group["Delta_phi"], marker='o', label=f"N_LMT={N}")
    plt.xlabel("Interferometer time T [s]")
    plt.ylabel("Delta phi [rad]")
    plt.yscale("log")
    plt.title("Predicted interferometer phase shift for Δv = baseline")
    plt.grid(True, which="both", ls="--", alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.savefig(outfile_png, dpi=300)
    plt.close()

def parse_args():
    p = argparse.ArgumentParser(description="Predict interferometer phase shifts and required shots.")
    p.add_argument('--delta_v', type=float, default=1e-12, help='Velocity step Δv in m/s (default 1e-12)')
    p.add_argument('--k_factors', type=float, nargs='+', default=[50,100,200], help='LMT factors (default 50 100 200)')
    p.add_argument('--T', type=float, nargs='+', default=[0.5,1.0,5.0], help='Interferometer times in s (default 0.5 1.0 5.0)')
    p.add_argument('--wavelength', type=float, default=780e-9, help='Laser wavelength in meters (default 780e-9)')
    p.add_argument('--per_shot_noise', type=float, default=1e-3, help='Per-shot phase noise in radians (default 1e-3)')
    p.add_argument('--sigma', type=float, default=5.0, help='Detection significance in sigma (default 5)')
    p.add_argument('--out_csv', type=str, default='predict_phase_shift_table.csv', help='Output CSV filename')
    p.add_argument('--out_png', type=str, default='phase_shifts.png', help='Output PNG filename')
    return p.parse_args()

def main():
    args = parse_args()
    df = build_table(delta_v=args.delta_v, k_eff_factors=args.k_factors, T_values=args.T,
                     wavelength=args.wavelength, per_shot_noise=args.per_shot_noise,
                     target_sigma=args.sigma)
    df.to_csv(args.out_csv, index=False)
    plot_phase_shifts(df, args.out_png)
    print(f"Saved CSV to {args.out_csv} and plot to {args.out_png}")

if __name__ == '__main__':
    main()
