---
citation_key: Raorane2025SBAMP
arxiv_id: 2511.12022
arxiv_url: https://arxiv.org/abs/2511.12022
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-23T18:50:06Z
origin: ai+web
reviewed: false
---

::: IEEEkeywords
Motion Planning, Dynamical Systems, Lyapunov Stability, Real-Time Adaptation
:::

# Introduction

Autonomous robots must navigate geometrically complex and dynamically changing environments, including dodging pedestrians, rerouting around debris, and recovering from sudden collisions, demanding two competing capabilities: *global path quality* (near-optimal, collision-free trajectories over long horizons) and *local reactivity* (instantaneous adaptation to new obstacles or perturbations).

Sampling-based planners like RRT\* [@karaman2011sampling] guarantee asymptotic optimality in static scenes but incur significant overhead when replanning under change. Reactive controllers such as SEDS [@khansari2011learning] and LPV-DS [@figueroa2018physically] offer smooth, real-time adaptation but rely on offline demonstrations.

We present *Sampling-Based Adaptive Motion Planning* (SBAMP), a hybrid framework that fits a Lyapunov-stable vector field online to each RRT\* waypoint segment, requiring no pre-collected data, and interleaves high-rate local control with lower-frequency global replanning to avoid expensive full replanning. Our main contributions are:

- *A bi-level SBAMP architecture* combining RRT\* global planning with an online, Lyapunov-stable SEDS-inspired controller that rescues RRT\* under severe perturbations.

- *An efficient interleaving scheme* minimizing global replanning while preserving provable local stability.

- *Extensive evaluation on RoboRacer [@okelly2020f1tenth]* hardware and simulation, showcasing rapid disturbance recovery and robust obstacle resilience.

# Related Work

Sampling-Based Motion Planning (SBMP) algorithms such as RRT\* enable efficient, collision-free path planning in high-dimensional spaces and converge asymptotically to optimal solutions [@lavalle2006planning; @karaman2011anytime; @arxiv2023sampling]. Variants including bi-directional RRT\* and heuristic-enhanced methods further accelerate convergence [@akgun2011sampling]. However, classical SBMP methods are inherently static: once a path is generated, they lack mechanisms for real-time adaptation to environmental changes, and extensions handling kinodynamic or dynamic constraints often sacrifice online practicality.

Learning-based Dynamical Systems (DS) address adaptability by modeling robot motion as stable attractor systems. SEDS fits a Gaussian mixture model to demonstration data under Lyapunov constraints, ensuring global asymptotic stability [@khansari2011learning], while LPV-DS generalizes this via state-dependent linear models with stability certificates across operating regimes [@figueroa2018physically]. GP-MDS enables online refinement through Gaussian Process Regression without batch training, though it requires careful kernel tuning and sparse-data management [@kronander2015incremental]. All three paradigms share a core limitation: dependence on offline demonstrations, extensive dataset collection, or nontrivial model tuning, which hinders integration with global planners in real-time, unstructured environments.

Hybrid frameworks attempt to combine global exploration with local adaptability. Recent work couples RRT\* with Lyapunov-certified, demonstration-driven controllers to funnel around nominal waypoints [@arxiv2023sampling], but relies on pre-collected data and lacks a unified global stability guarantee. Robust samplers incorporating forward reachability analysis [@wu2022robustrrt] similarly omit Lyapunov-style proofs, while chance-constrained RRT variants using tube-based LPV-MPC [@nezami2022robust] and LPV-embedded nonlinear MPC [@karachalios2025efficient] achieve probabilistic robustness but incur significant per-step optimization overhead. None of these methods simultaneously eliminate demonstration dependence, guarantee unified stability, and maintain real-time tractability.

SBAMP addresses all three gaps by fitting its SEDS-style Gaussian mixture model on-the-fly from each newly planned RRT\* segment---requiring no offline data---and synthesizing every local controller under a common Lyapunov-style local stability constraint. By decoupling RRT\* planning from vector-field evaluation (a weighted sum of linear maps at control rate), SBAMP sustains real-time performance without per-step optimization solves.

# Sampling Based Adaptive Motion Planning {#sec:SBAMP-theory}

Figure [1](#fig:SBAMP-theory){reference-type="ref" reference="fig:SBAMP-theory"} depicts the overall SBAMP control loop. At its core, SBAMP runs two modules in parallel: a global RRT$^*$ planner and a local SEDS controller, with a lightweight decision logic that refits the dynamical system whenever the planner produces a new path.

:::: {#fig:SBAMP-theory .figure latex-placement="H"}
![](Raorane2025SBAMP_figs/SBAMP_NODE.png){width="1\\columnwidth"}

::: caption
Flowchart of the SBAMP theoretical framework. When *New Path Available?* is true, the SEDS generator refits the dynamical system to the latest RRT$^*$ segment; otherwise, the existing SEDS velocity command is executed.
:::
::::

SBAMP is structured as a bi-level optimization framework comprising three interacting components.

## Global Path Planning via RRT$^*$

We incrementally grow and rewire a tree $\mathcal{T}\subset\mathcal{C}_{\rm free}$ using a lightweight RRT$^*$-inspired planner [@karaman2011anytime], yielding a waypoint sequence $$\tau = \{\,x_0,\,x_1,\,\dots,\,x_g\}\subset\mathbb R^n.$$ Every planner cycle (period $\Delta t_G$) samples $x_{\rm rand}\sim\mathcal{U}(\mathcal{C}_{\rm free})$, extends toward it, and performs local rewiring over nearby nodes to improve path optimality.

## Local Trajectory Adaptation via SEDS

At control rate ($\Delta t_C \ll \Delta t_G$), the robot state $\xi(t)$ is driven by a convex mixture of $K$ linear subsystems [@khansari2011learning]: $$\begin{equation}
\label{eq:seds-theory}
  \dot{\xi}
  = f(\xi)
  = \sum_{k=1}^K \gamma_k(\xi)\bigl(A_k\,\xi + b_k\bigr),
  \quad
  \sum_{k=1}^K\gamma_k(\xi)=1,\;\gamma_k(\xi)\ge0,
\end{equation}$$ where each $A_k\!+\!A_k^\top\prec0$ (ensuring $V(\xi)=\xi^\top\xi$ decays) and $$b_k = -A_k\,x_i \quad\Longrightarrow\quad f(x_i)=0$$ at the active waypoint $x_i$. We pose local controller synthesis as a real-time constrained optimization problem: given waypoints $\{x_i, x_{i+1}\}$, find a $K$-component mixture of linear systems that (1) produces smooth vector fields via GMM fitting, and (2) guarantees local asymptotic stability via Hurwitz projection. Formally, for each component $k$: $$\min_{A_k}\;\|A_k - \hat{A}_k\|_F \quad \text{s.t.} \quad A_k + A_k^\top \prec 0,$$ This per-cycle fit requires no stored dataset and completes within the replanning loop. The attractor is then recentered at $x_{i+1}$ by updating $\{b_k\}$ accordingly.

## Real-Time Integration and Stability

Upon receiving a new path, the SEDS generator refits $\{b_k\}$ and updates $\dot{\xi}$; otherwise, the current model is used, with attractor shifts preserving velocity continuity. Under the average dwell-time theorem [@hespanha1999stability], if the SEDS update period $\Delta t_C$ and RRT$^*$ planning period $\Delta t_G$ satisfy $$\Delta t_C \;\ll\;\tau_D\;\le\;\Delta t_G,$$ then each fitted subsystem remains locally stable to its active waypoint, with empirically observed recovery to the final goal $x_g$. Together, these three modules realize a real-time adaptive planner with Lyapunov-stable local subsystems and no offline training data required. Full implementation details on the RoboRacer [@okelly2020f1tenth] hardware are provided in Appendix [6](#sec:appendix-impl){reference-type="ref" reference="sec:appendix-impl"}.

# Experiments

We evaluate SBAMP against standard RRT\* across three complementary studies designed to stress-test the two core claims of the framework: that the DS attractor preserves control authority during replanning gaps, and that Lyapunov-stable local control enables recovery from disturbances that exceed RRT\*'s planning capacity.

## Computational Efficiency Under Disturbance {#sec:exp1}

A fundamental vulnerability of purely sampling-based planners is that replanning latency grows with perturbation magnitude: as the vehicle is displaced farther from its prior tree, RRT\* must explore a larger region of $\mathcal{C}_{\rm free}$ before recovering a feasible path, and if that latency exceeds the time to exhaust the current waypoint buffer, the controller loses its reference entirely. We quantify this degradation by teleporting the vehicle laterally by $\Delta d \in [2.25, 2.75]$ m at a fixed straightaway immediately before each planning cycle, repeating $N=20$ trials per displacement in the ROS2 simulator at $v = 1$ m/s.

Figure [2](#fig:replan_freq_vs_perturbation){reference-type="ref" reference="fig:replan_freq_vs_perturbation"} reports replanning frequency $f_{\rm plan}$ as a function of $\Delta d$. RRT\* degrades sharply across this range, falling below the 2 Hz minimum required to ensure the vehicle advances no more than 0.5 m between updates at nominal speed. SBAMP, by contrast, sustains approximately 60 Hz throughout, because the DS attractor provides a well-defined velocity command toward the last known waypoint irrespective of planner latency, and transitions to each new RRT\* solution without discontinuity in the control signal. This 30$\times$ margin over the stability threshold directly validates the dwell-time argument of Section [3](#sec:SBAMP-theory){reference-type="ref" reference="sec:SBAMP-theory"}.

:::: {#fig:replan_freq_vs_perturbation .figure latex-placement="H"}
![](Raorane2025SBAMP_figs/pertubation_dist_vs_hz.png){width="0.75\\columnwidth"}

::: caption
Replanning frequency vs. lateral perturbation. RRT\* falls below the 2 Hz stability threshold as $\Delta d$ grows; SBAMP maintains approximately 60 Hz throughout.
:::
::::

## Recovery from Extreme Planner Failures {#sec:exp2}

To characterize the boundary of RRT\*'s recovery envelope and demonstrate SBAMP's behavior beyond it, we subjected both planners to three qualitatively distinct failure modes in a $5\,\text{m} \times 2\,\text{m}$ corridor: large translational jumps, rotational offsets up to $90^\circ$, and corner entrapment. In each case we increased disturbance magnitude until the planner either collided or failed to produce a feasible path within the planning budget.

Under large lateral displacement (Figure [5](#fig:pair_large_trans){reference-type="ref" reference="fig:pair_large_trans"}), RRT\* exhausts its planning budget before reconnecting to the corridor, leaving the vehicle with no valid reference. SBAMP's attractor immediately redirects the vehicle toward the last RRT\* waypoint, maintaining bounded tracking error until the planner recovers and a new path is handed off without discontinuity.

:::: {#fig:pair_large_trans .figure latex-placement="H"}
![RRT\* under large translation](Raorane2025SBAMP_figs/RRT_large_trans.png){#fig:RRT_large_trans width="\\linewidth"}

![SBAMP under large translation](Raorane2025SBAMP_figs/SBAMP_large_trans.png){#fig:SBAMP_large_trans width="\\linewidth"}

::: caption
Planner recovery under large translational perturbation. RRT\* loses its reference; SBAMP maintains a stable attractor throughout.
:::
::::

Rotational offsets exceeding $60^\circ$ expose a second failure mode: RRT\* either times out or produces paths that, when executed, direct the vehicle into obstacles before a corrective replan can arrive (Figure [8](#fig:pair_large_rotate){reference-type="ref" reference="fig:pair_large_rotate"}). SBAMP is unaffected because the DS controller operates on the error to the current waypoint in Cartesian space, not on heading, and continues issuing stable commands regardless of orientation.

In tight-corner scenarios (Figure [11](#fig:pair_tight_corners){reference-type="ref" reference="fig:pair_tight_corners"}), RRT\*'s sparse sampling produces waypoints that, under execution, bring the vehicle within collision range of opposing walls. SBAMP resolves this by committing only to the immediately reachable waypoint via the SEDS vector field and withholding progression until the next global plan is available, yielding smooth, collision-free negotiation of the corner.

:::: {#fig:pair_large_rotate .figure latex-placement="H"}
![RRT\* under large rotation](Raorane2025SBAMP_figs/RRT_large_rotate.png){#fig:RRT_large_rotate width="\\linewidth"}

![SBAMP under large rotation](Raorane2025SBAMP_figs/SBAMP_large_rotate.png){#fig:SBAMP_large_rotate width="\\linewidth"}

::: caption
Planner recovery under large rotational perturbation. RRT\* produces unsafe paths; SBAMP maintains stable convergence to the last waypoint.
:::
::::

:::: {#fig:pair_tight_corners .figure latex-placement="H"}
![RRT\* in tight corners](Raorane2025SBAMP_figs/RRT_tight_corners.png){#fig:RRT_tight_corners width="\\linewidth"}

![SBAMP in tight corners](Raorane2025SBAMP_figs/SBAMP_tight_corners.png){#fig:SBAMP_tight_corners width="\\linewidth"}

::: caption
Performance in tight-corner scenarios. RRT\* produces unsafe waypoints; SBAMP commits only to the immediately reachable target.
:::
::::

:::: {#fig:SBAMP_large_recovery .figure latex-placement="H"}
![Pre-recovery state](Raorane2025SBAMP_figs/SBAMP_large_recovery_before.png){#fig:SBAMP_recovery_before width="\\linewidth"}

![Post-recovery state](Raorane2025SBAMP_figs/SBAMP_large_recovery_after.png){#fig:SBAMP_recovery_after width="\\linewidth"}

::: caption
SBAMP recovery under combined large translational and rotational displacement.
:::
::::

SBAMP's recovery is not limited to small perturbations: even under large translational and rotational displacements (Figure [14](#fig:SBAMP_large_recovery){reference-type="ref" reference="fig:SBAMP_large_recovery"}), the SEDS attractor guides the vehicle back into the connected free-space corridor, at which point a new global trajectory is computed and followed without discontinuity.

## Real-Time Performance Validation on Hardware {#sec:exp3}

Simulation results establish SBAMP's theoretical properties; hardware trials establish that these properties transfer to a physical platform subject to sensor noise, actuation lag, and unmodeled dynamics. We operated the vehicle on an indoor loop course featuring straightaways, tight turns, and cluttered corridors, and manually applied 20 randomized translational and rotational disturbances during closed-loop operation.

In all trials, the vehicle deviated from its nominal path immediately following the disturbance, after which the SEDS attractor generated commands that returned it to the vicinity of the last RRT\* waypoint before transitioning seamlessly to the newly computed global plan (Figures [17](#fig:pair_human_rotate){reference-type="ref" reference="fig:pair_human_rotate"}--[20](#fig:pair_human_translate){reference-type="ref" reference="fig:pair_human_translate"}). SBAMP achieved a near-100% recovery rate across all 20 perturbations; the isolated failures arose only under extreme rotational displacements sufficient to cause waypoint misidentification, and even in these cases the vehicle converged to the most recently valid waypoint rather than diverging.

:::: {#fig:pair_human_rotate .figure latex-placement="H"}
![Post-disturbance deviation](Raorane2025SBAMP_figs/SBAMP_human_rotate_1.png){#fig:SBAMP_human_rotate_before width="\\linewidth"}

![Post-recovery trajectory](Raorane2025SBAMP_figs/SBAMP_human_rotate_2.png){#fig:SBAMP_human_rotate_after width="\\linewidth"}

::: caption
SBAMP response to human-applied rotational disturbance on hardware.
:::
::::

:::: {#fig:pair_human_translate .figure latex-placement="H"}
![Post-disturbance deviation](Raorane2025SBAMP_figs/SBAMP_human_translate_1.png){#fig:SBAMP_human_translate_before width="\\linewidth"}

![Post-recovery trajectory](Raorane2025SBAMP_figs/SBAMP_human_translate_2.png){#fig:SBAMP_human_translate_after width="\\linewidth"}

::: caption
SBAMP response to human-applied translational disturbance on hardware.
:::
::::

Finally, Figures [23](#fig:pair_obsAvoid_A){reference-type="ref" reference="fig:pair_obsAvoid_A"}--[26](#fig:pair_obsAvoid_B){reference-type="ref" reference="fig:pair_obsAvoid_B"} demonstrate real-world obstacle avoidance under two drift scenarios. In each case SBAMP generated a collision-free avoidance trajectory around an unexpected object and rejoined the nominal corridor, without any modification to the underlying RRT\* planner. This non-invasive augmentation is a key property of the framework: when RRT\* operates correctly, SBAMP defers to it; when the planner falters, the DS attractor intervenes autonomously.

:::: {#fig:pair_obsAvoid_A .figure latex-placement="H"}
![Approaching obstacle (A)](Raorane2025SBAMP_figs/SBAMP_ObsAvoidance_11.png){#fig:SBAMP_obsAvoid_A_before width="\\linewidth"}

![Left-side avoidance (A)](Raorane2025SBAMP_figs/SBAMP_ObsAvoidance_12.png){#fig:SBAMP_obsAvoid_A_after width="\\linewidth"}

::: caption
Obstacle avoidance scenario A.
:::
::::

:::: {#fig:pair_obsAvoid_B .figure latex-placement="H"}
![Approaching obstacle (B)](Raorane2025SBAMP_figs/SBAMP_ObsAvoidance_21.png){#fig:SBAMP_obsAvoid_B_before width="\\linewidth"}

![Right-side avoidance (B)](Raorane2025SBAMP_figs/SBAMP_ObsAvoidance_22.png){#fig:SBAMP_obsAvoid_B_after width="\\linewidth"}

::: caption
Obstacle avoidance scenario B.
:::
::::

# Conclusion

We have introduced SBAMP, a bi-level motion-planning framework that non-invasively augments RRT\* with a Lyapunov-stable dynamical-systems controller, achieving on-the-fly adaptation with no prior training data. By converting each RRT\* waypoint into a locally stable attractor on-the-fly, SBAMP ensures a valid control reference even when global replanning lags. Our threefold evaluation demonstrates that SBAMP sustains high replanning frequencies, reliably recovers from large translational and rotational disturbances, and executes safe obstacle avoidance, all without any offline learning or demonstration dataset.

Future work includes integrating SBAMP with receding-horizon optimizers such as MPC or MPPI, embedding obstacle-repulsive modulation directly into the dynamical-systems layer to reduce reliance on occupancy-grid update rates, and extending the framework to high-dimensional manipulators to broaden its applicability across autonomous robotics tasks.

# SBAMP Implementation on RoboRacer {#sec:appendix-impl}

SBAMP is deployed on the RoboRacer [@okelly2020f1tenth] platform using ROS2 Humble. Laser scans and odometry feed into a local occupancy grid; the planner produces a waypoint sequence $\tau$; the SEDS controller issues velocity commands; and an optional visualization node renders the state in RViz2.

Five ROS2 nodes form the backbone of SBAMP: an *Occupancy Grid Node* fusing LIDAR and odometry; a *Next Waypoint Node* extracting the next feasible goal; an *RRT\* Node* continuously replanning collision-free paths; an optional *Visualization Node* for RViz2 debugging; and the *SBAMP Node* fitting the SEDS model and publishing Ackermann drive commands at high frequency. The five core nodes are listed in Table [1](#tab:ros2-packages){reference-type="ref" reference="tab:ros2-packages"}.

:::: {#fig:SBAMP-ROS-RoboRacer .figure latex-placement="H"}
![](Raorane2025SBAMP_figs/SBAMP_ROS.png){width="0.9\\columnwidth"}

::: caption
ROS2 node graph for SBAMP on RoboRacer.
:::
::::

::: {#tab:ros2-packages}
  **Node**                **Functionality**
  ----------------------- --------------------------------
  `occupancy_grid_node`   LIDAR/odometry fusion
  `rrt_node`              Online path planning
  `next_waypoint_node`    Feasible goal extraction
  `sbamp_node`            SEDS fit and Ackermann control
  `visualization_node`    RViz2 rendering (optional)

  : Core ROS2 Nodes in the `sbamp` Package
:::

All experiments were performed on the RoboRacer F1/10 platform, whose kinematics obey $$\dot{x} = v\cos\theta,\quad
\dot{y} = v\sin\theta,\quad
\dot{\theta} = \frac{v}{L}\tan\delta.$$ Perception is provided by an 812-beam SICK TIM781 LIDAR, and actuation uses ROS2 Ackermann steering commands.

[^1]: The authors are with the General Robotics, Automation, Sensing and Perception (GRASP) Laboratory, University of Pennsylvania, Philadelphia, PA, 19104, USA.

[^2]: ${^*}$ Equal contribution.

[^3]: ${^\dagger}$ Corresponding author: <quanpham@seas.upenn.edu>.

[^4]: Code & videos available at: <https://github.com/anhquanpham/SBAMP>.
