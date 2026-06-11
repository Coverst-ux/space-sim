## Phase 2: Euler Integration Vs Leapfrog Integration
**The question:** Which numerical integrator should be used?
**Options considered**: Euler integration and Leapfrog integration
**What I chose:** Leapfrog Integration
**Why:** Euler Integration is a first order numerical procedure which works by predicting the expected answer in a short period in the future by using the current velocity and position. This causes non-conservation with energy, it adds energy since it assumes it's linear across an entire step. On the other hand, Leapfrog Integration is a second order numerical procedure which works by performing half a step, updating the velocity and position, then using the updated forces to predict the second half of the step. This prevents energy drift and greatly reduces the percentage of error. Euler's energy error reached over 60% over 20 years while Leapfrog's error stayed at 0.028% with constant amplitude, a 2000x difference.

**Evidence:**  ![Energy Drift Comparison](benchmarks/euler_vs_leapfrog_energy.png)
