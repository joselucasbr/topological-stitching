# Topological Time-Stitching — Simulation & Experimental Tools

This repository contains numerical tools and reference scripts used to explore and test the predictions of the **Topological Time-Stitching** framework, including relativistic dilation, drift-quantization, and proposed interferometric experiments.

The goal is to provide fully reproducible code for theorists and experimental groups evaluating the model's predictions.

---

## 🔧 **Repository Contents**

### **1. `helical_relativity.py`**

Numerical verification that the geometric helical cycle reproduces the Lorentz factor:
[
\gamma = \frac{1}{\sqrt{1 - (v/c)^2}}.
]

Produces:

* Overlaid γ plots (theory vs SR)
* Automatic numerical consistency check (assertion)
* Publication-quality PNG & PDF figures

---

### **2. `quantized_spectrum.py`**

Computes the discrete drift-velocity spectrum predicted by the model.

Features:

* Root-finding for the stability (closure) equation
* Reproduction of Appendix C spectrum table
* Adjustable precision and tolerance
* Export to CSV for comparison with experiment

---

### **3. `gravity_river.py`**

Generates the Gullstrand–Painlevé (GP) flow metric using the causal-flow interpretation of gravity.

Outputs:

* Flow profiles (v_{\text{flow}}(r))
* Effective metric components
* Sanity checks against Schwarzschild

---

### **4. `predict_phase_shift.py`**

Utility script for **Experimental Proposal A (Drift-Quantization Interferometry)**.

Computes:

* Expected interferometer phase shift
  [
  \Delta\phi = k_{\rm eff},\Delta v,T
  ]
* Required number of shots to achieve target detection significance
* Publication-ready CSV tables and PNG plots

Parameters:

* LMT factors (`N_LMT`)
* Interferometer times (`T`)
* Wavelength
* Per-shot phase noise
* Target sigma level

Usage example:

```bash
python predict_phase_shift.py --delta_v 1e-12 --k_factors 50 100 200 --T 1 5
```

Produces:

* `predict_phase_shift_table.csv`
* `phase_shifts.png`

---

## 🧪 **Reproducibility**

All scripts:

* Are deterministic
* Use fixed numerical tolerances
* Require only standard scientific Python packages (`numpy`, `matplotlib`, `pandas`)
* Can be run on any machine supporting Python ≥ 3.8

To ensure full reproducibility:

```bash
pip install numpy matplotlib pandas
```

---

## 📁 **Folder Structure**

```
/ (root)
  helical_relativity.py
  quantized_spectrum.py
  gravity_river.py
  predict_phase_shift.py
  README.md
  figures/
        helical_gamma.png
        phase_shifts.png
        distorted_stitch_diagram.svg
  data/
        drift_spectrum.csv
        predict_phase_shift_table.csv
```

---

## 📘 **Citation**

If you use this code in academic work, please cite the associated whitepaper:

> J. Lucas, *Topological Time-Stitching: A Process-Based Derivation of Relativity, Quantization, and Gravitation* (2025).
> DOI / arXiv link TBD.

---

## 🤝 **Contributions & Collaboration**

Pull requests, replication attempts, and experimental collaborations are welcome — especially from groups working in:

* LMT atom interferometry
* Ultra-stable optical clocks
* High-precision quantum metrology
* Experimental tests of Lorentz symmetry

---

## 📬 **Contact**

For questions or collaboration inquiries, please reach out:

* Author: **José Lucas**
* Email: *(replace with your preferred contact method)*

---
