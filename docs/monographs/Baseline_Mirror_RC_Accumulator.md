# Monograph: The Baseline Mirror and the RC Accumulator — A Physical Framework for Balanced Ternary Information Processing

* **Author:** Justin D. Grimm ([ORCID: 0009-0000-5299-0243](https://orcid.org/0009-0000-5299-0243))
* **Affiliation:** Independent Dandelion Substrate Research Group
* **Workspace Source:** [Monograph - The Baseline Mirror and the RC Accumulator](https://docs.google.com/document/d/1Lk218haXDhepaWpgLwAzjKXiwNR4b9zYrvy2B27e8Bw/edit?usp=drivesdk&ouid=108041868247398199219)

## 1. The Incompressible Baseline and the Illusion of Subtraction

1. **The Active Baseline ($0$):** Systems operate against an incompressible metabolic baseline ($V_0 = 1650\text{ mV}$ on a $3300\text{ mV}$ rail, $\Delta S > 0$).
2. **Phase Reflections over Deletion:** What classical systems label as subtraction or deletion is a conjugate phase reflection across the active baseline mirror: $\mathcal{R}_{V_0}(V_{\text{rc}}) = (V_0 \ll 1) - V_{\text{rc}} = 3300 - V_{\text{rc}}$.
3. **Pure Addition & Wave Interference:** Every state transition is an addition relative to the baseline, satisfying $V_{\text{rc}}[t] + \mathcal{R}_{V_0}(V_{\text{rc}}[t]) \equiv 3300\text{ mV}$.

## 2. Dipole Frustration & Hardware Realization ($\tau = RC$)

At $N = 3$, bilateral symmetry breaks into dynamic metabolic flow ($\Delta S > 0$). Replacing digital bit-flipping with integer-shifted RC integration ($V_{\text{rc}}[t] = V_{\text{rc}}[t-1] - ((V_{\text{rc}}[t-1] - V_0) \gg 3) + \Delta V_{\text{in}} + (M_{\text{epig}} \gg 2)$) and dual-rail Schmitt window comparators ([Op-Amp Positive Feedback Schmitt Trigger & Window Comparator With Hysteresis](https://industrialmonitordirect.com/blogs/knowledgebase/op-amp-virtual-short-assumption-in-positive-feedback-loops)) locks physical memory into a single 64-byte L1D cache line (`ArgonMethylatedFrame64B`).
