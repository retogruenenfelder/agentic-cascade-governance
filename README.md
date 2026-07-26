# agentic-cascade-governance

[![SSRN Part One](https://img.shields.io/badge/SSRN-Part%20One%3A%20The%20Single%20Layer-blue)](https://ssrn.com/abstract=7184938)
[![SSRN Part Two](https://img.shields.io/badge/SSRN-Part%20Two%3A%20The%20Cascade-blue)](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7184979)

Code and figures for **The Double-Slit Correspondence: A Five-Parameter Structural Framework for AI Governance** by Reto Gruenenfelder.

## Papers

| Part | Title | SSRN |
|------|-------|------|
| One | The Single Layer | [Abstract 7184938](https://ssrn.com/abstract=7184938) |
| Two | The Cascade | [Abstract 7184979](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7184979) |

## Contents

- **`gen_setup_figs.py`** — Python script that generates all figures in both papers (fig1–fig14). Requires `matplotlib`, `numpy`, `scipy`.

## Usage

```bash
pip install matplotlib numpy scipy
python gen_setup_figs.py
```

Figures are written to the working directory as PDF files.

## Abstract

The Double-Slit Correspondence maps the five structural parameters of a quantum double-slit experiment — slit separation *d*, slit width *a*, wavelength *λ*, screen distance *L*, and observation position *x* — onto the five governance parameters of an AI production system: model heterogeneity, data specificity, update frequency, deployment scale, and performance threshold. The correspondence is exact, not metaphorical: every pathology of the physical setup (collapsed fringes, diffraction wash-out, near-field distortion) has a direct governance analogue that manifests as systematic, not random, model failure.

Part Two extends the single-layer result to multi-agent cascade architectures using random affine recurrences and the Brandt–Bougerol theorem, establishing a second-moment stability condition and a tail-threshold obligation for CRO sign-off on agentic pipelines.

## Citation

If you use this code, please cite the papers and this repository. See [`CITATION.cff`](CITATION.cff) for machine-readable citation metadata.

## Author

Reto Gruenenfelder — [gruenenfelder.co](https://gruenenfelder.co)

## Licence

Code: MIT. Paper text: © 2026 Reto Gruenenfelder. All rights reserved.
