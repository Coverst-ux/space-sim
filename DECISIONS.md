# Phase 2: Numerical Integrator Selection

## Options Considered
* Euler integration
* Leapfrog integration

## Chosen Architecture
**Leapfrog Integration** was selected for the core physics simulation loop.

## Technical Justification

## Algorithmic Mechanics
Euler Integration is a first-order numerical procedure which works by predicting the expected answer in a short period in the future by using the current velocity and position. This causes non-conservation of energy; it adds energy since a linear path is assumed across an entire step. 

On the other hand, Leapfrog Integration is a second-order numerical procedure which works by performing half a step, updating the velocity and position, then using the updated forces to predict the second half of the step. This prevents energy drift and greatly reduces the percentage of error.

## Performance Metrics (20-Year Horizon)

| Metric | Euler Integration | Leapfrog Integration | Performance Delta |
| :--- | :--- | :--- | :--- |
| **Energy Error %** | Over 60% error | 0.028% error | **2000x difference** |
| **Error Behavior** | Continuous drift (adds energy) | Bounded amplitude | Constant stability |

## Empirical Evidence
![Energy Drift Comparison](benchmarks/euler_vs_leapfrog_energy.png)

---

# Phase 3: Trail Optimization

## Options Considered
* Standard Python `list` with manual bounds checking (`list.pop(0)`)
* `collections.deque` with a fixed `maxlen`

## Chosen Architecture
A **`collections.deque(maxlen=500)`** was implemented to manage the historical coordinates of the celestial bodies.

## Technical Justification

## The Problem with Standard Lists
Using a normal list forces Python to drag every single old coordinate forward in memory every time the trail exceeds the specified length. When calling `list.pop(0)`, the item at index `0` is removed, meaning that Python must shift every remaining coordinate down a slot to keep the array continuous in memory. This introduces an $O(N)$ linear time penalty on every frame update, creating unnecessary strain on the CPU as the simulation continues.

## The Deque Advantage
A `deque` with a fixed `maxlen` removes this performance bottleneck entirely. It pushes memory management entirely down to the C-level, automatically dropping the oldest position point off the front of the queue the second a new point is appended to the back. Because a deque is a doubly-linked structure, these insertions and deletions happen in $O(1)$ constant time without disturbing or shifting the rest of the elements in memory.

## The Zoom Integration
Since the trail history is strictly capped at a maximum of 500 points per body, the computational efficiency per frame remains optimal. Instead of managing a complex pixel cache that would require a full recalculation every time the camera zoom changes, the engine safely converts raw coordinates (meters) to screen coordinates (pixels) on the fly. For a standard setup of 9 celestial bodies, this requires fewer than 4,500 basic calculations per frame—a negligible processing load that ensures the simulation display maintains a smooth, stable 60 FPS.

# Architectural Decisions Log

# Phase 4: N-body Complexity & Profiling

## The Question
What is the bottleneck in the simulation and what can be done about it?

## Options Considered
- Keep $O(N^2)$ but vectorize with NumPy (Complexity stays the same but constants are faster)
- Implement Barnes-Hut quadtree(Reduces the complexity to  $O(N \log N)$
- Do Both

## Chosen Option
Do both. Implementing a Barnes-Hut quadtree reduces the actual complexity to $O(N \log N)$ while NumPy improves the speed of the constant. The obvious choice here is to combine both worlds to produce the most optimal efficiency. 

## Why?
Using Barnes-Hut quadtree improves the complexity of the algorithms to be significantly more efficient. With the brute-force option of $O(N^2)$ when N = 100, ncalls were at 247,500 calls. N= 200, ncalls = 995,000, and finally at N = 500, ncalls were at an alarming 6,237,500 which took 33.07s to complete. Barnes-Hut would greatly reduce the computational load exerted. Gravitational_force is the real bottleneck which has all the calculations, force computation, and the operations. NumPy calculates the forces across all pairs in C, removing each pair's Python object creation and overhead that quickly piles up at high n.

## Empirical Evidence
| N | Time (s) | `gravitational_force` calls |
|---|---|---|
| 100 | 1.228 | 247,500 |
| 200 | 4.916 | 995,000 |
| 500 | 33.074 | 6,237,500 |

## Next steps
The next phase, phase 5, will address this bottleneck by deploying NumPy and Barnes-Hut algorithm to substantially streamline the operations.

# Phase 5: Barnes-Hut Algorithm and Bottleneck solution

## The Question
How can Barnes-Hut algorithm be applied to resolve the bottleneck that the current project is facing?

## Solution
Barnes-Hut algorithm uses a quadtree to traverse through all bodies. It traverses through all the nodes (bodies) until it finds a node that is far away enough from the target body for it to be considered as a single body. This increases accuracy as long as the theta is correctly set.

## Empirical Evidence
| N | O(N²) Time (s) | Barnes-Hut Time (s) | Ratio |
|---|---|---|---|
| 100 | 1.228 | 6.867 | 5.6x slower |
| 200 | 4.916 | 21.566 | 4.4x slower |
| 500 | 33.074 | 100.126 | 3.0x slower |

Counterintuitively, the initial benchmark data indicates the Barnes-Hut implementation ($O(N \log N)$) appears to be doing worse than the method of brute forcing the calculations ($O(N^2)$). This is a side effect of Barnes-Hut data structure at low `N`s. The tree overhead of building a quadtree from scratch, inserting all the bodies, and calling `update_mass` adds substantial overhead. In addition, pure python recursive calls are known to have expensive computational cost. However, as `N` grows, Barnes-Hut catches up to the brute force method. At a higher `N`, it will overtake the brute force method.

## Next steps
The next steps integrate NumPy vectorization with Barnes-Hut to further mitigate computational bottlenecks.