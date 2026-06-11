## Phase 2: Numerical Integrator Selection

### Options Considered
* Euler integration
* Leapfrog integration

### Chosen Architecture
**Leapfrog Integration** was selected for the core physics simulation loop.

### Technical Justification

#### Algorithmic Mechanics
Euler Integration is a first-order numerical procedure which works by predicting the expected answer in a short period in the future by using the current velocity and position. This causes non-conservation of energy; it adds energy since a linear path is assumed across an entire step. 

On the other hand, Leapfrog Integration is a second-order numerical procedure which works by performing half a step, updating the velocity and position, then using the updated forces to predict the second half of the step. This prevents energy drift and greatly reduces the percentage of error.

#### Quantitative Performance Metrics (20-Year Horizon)

| Metric | Euler Integration | Leapfrog Integration | Performance Delta |
| :--- | :--- | :--- | :--- |
| **Energy Error %** | Over 60% error | 0.028% error | **2000x difference** |
| **Error Behavior** | Continuous drift (adds energy) | Bounded amplitude | Constant stability |

### Empirical Evidence
![Energy Drift Comparison](benchmarks/euler_vs_leapfrog_energy.png)

---

## Phase 3: Trail Optimization

### Options Considered
* Standard Python `list` with manual bounds checking (`list.pop(0)`)
* `collections.deque` with a fixed `maxlen`

### Chosen Architecture
A **`collections.deque(maxlen=500)`** was implemented to manage the historical coordinates of the celestial bodies.

### Technical Justification

#### The Problem with Standard Lists
Using a normal list forces Python to drag every single old coordinate forward in memory every time the trail exceeds the specified length. When calling `list.pop(0)`, the item at index `0` is removed, meaning that Python must shift every remaining coordinate down a slot to keep the array continuous in memory. This introduces an $O(N)$ linear time penalty on every frame update, creating unnecessary strain on the CPU as the simulation continues.

#### The Deque Advantage
A `deque` with a fixed `maxlen` eliminates this performance bottleneck entirely. It pushes memory management entirely down to the C-level, automatically dropping the oldest position point off the front of the queue the second a new point is appended to the back. Because a deque is a doubly-linked structure, these insertions and deletions happen in $O(1)$ constant time without disturbing or shifting the rest of the elements in memory.

#### The Zoom Integration
Since the trail history is strictly capped at a maximum of 500 points per body, the computational efficiency per frame remains optimal. Instead of managing a complex pixel cache that would require a full recalculation every time the camera zoom changes, the engine safely converts raw coordinates (meters) to screen coordinates (pixels) on the fly. For a standard setup of 9 celestial bodies, this requires fewer than 4,500 basic calculations per frame—a negligible processing load that ensures the simulation display maintains a smooth, stable 60 FPS.