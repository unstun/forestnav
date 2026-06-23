---
citation_key: Deflesselle2026ManeuverNet
arxiv_id: 2602.14726
arxiv_url: https://arxiv.org/abs/2602.14726
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-23T17:49:46Z
origin: ai+web
reviewed: false
---

# Introduction

Recent advances in deep reinforcement learning (DRL) for robotics have mainly focused on navigation and locomotion tasks for holonomic robots such as omni-wheeled [@Mehmood2021ITC], quadruped [@Zhang2024AS], or biped robots [@GaspardIROS2024]. By holonomic robots, we refer to the ones that can move freely in all directions [@Moreno2016Sensors]. In contrast, Ackermann-steering robots, like cars, represent a restrictive type of non-holonomic robots [@Zhao2013AC]. These robots cannot rotate without moving forward or backward, which reduces their number of degrees of freedom (DOF) [@Siegwart2005]. Such constraints significantly limit their maneuverability and impose additional challenges for control [@SamsonTRO]. In this work, we specifically focus on controlling a mobile platform with four-wheel steering (4WS), and a double-Ackermann-steering mechanism (see Fig. [1](#fig:eye-catch){reference-type="ref" reference="fig:eye-catch"}). Controlling such robots presents even more complex challenges compared to single-Ackermann-steering systems. The need to coordinate both front and rear steering introduces additional non-holonomic constraints, making precise maneuvering, such as reversing or parallel alignment, even more difficult [@Hulttinen2020]. Despite these challenges, double-Ackermann-steering mobile robots (DASMRs) offer several advantages: improved maneuverability, stability, and energy efficiency [@Yu2010TRO]. These characteristics make them particularly suitable for applications in agriculture, autonomous navigation, and uneven terrain, where robustness and cost-effectiveness are essential [@Deremetz2017ECMR; @Thuilot2009]. Enabling these robots to perform precise maneuvers significantly enhances their practical use and autonomy in real-world environments, such as parking in tight spaces, or positioning within recharging areas.

:::: {#fig:eye-catch .figure latex-placement="t"}
![](Deflesselle2026ManeuverNet_figs/eyecatcher.jpg){width="\\linewidth"}

::: caption
Maneuver handling (left figure) with 4WS robots in DRL is challenging because it requires current reward loss (circled in red in the right figure), making classical approaches sub-optimal.
:::
::::

Classical trajectory optimization and control methods, such as the widely used Timed Elastic Band (TEB) planner [@TEBref], have been applied to Ackermann and double-Ackermann robots. While these methods can be effective in principle, they require tuning multiple parameters, making them highly sensitive to small variations in robot dynamics (e.g., tire pressure, load distribution). In practice, this limits their robustness and complicates deployment in real-world agricultural environments [@TEB_parameters_limitation]. Therefore, DRL approaches represent a promising alternative. However, the maneuvering constraints of double-Ackermann-steering robots pose a major challenge for DRL agents [@Lazzaroni2022APPLEPIES]. In many scenarios, reaching a desired position requires the robot to perform a complex maneuver, such as initially moving away from the goal to later approach it with the correct orientation. Unfortunately, classic DRL approaches based on reward functions such as the Euclidean distance fail in such scenarios because they penalize the robot for increasing its distance from the desired position, resulting in a reward loss (cf. Fig. [1](#fig:eye-catch){reference-type="ref" reference="fig:eye-catch"}). As a result, the maneuvers needed to achieve successful positioning are often discouraged. This can lead to sub-optimal policies [@Mihir2021], where the agent becomes stuck near the goal in an incorrect orientation, unable to complete the task without temporarily sacrificing reward. Achieving such maneuvers can also be challenging when controlled through teleoperation, as even human operators often struggle with precise navigation [@Datar2024IROS]. Therefore, designing specific DRL frameworks that accommodate such constraints is essential for successful learning in DASMRs.

In this paper, we address the control of DASMRs using DRL in a fully model-free setting without relying on expert demonstrations or handcrafted guidance. Our goal is to develop a DRL framework that enables robust and generalizable maneuver learning despite the inherent kinematic constraints of DASMRs. To that end, we propose ManeuverNet, a novel Soft Actor-Critic (SAC) framework for DASMR with optimized reward functions designed specifically to perform precise maneuvers. The contributions of this article can be summarized as follows.

**- End-to-End DRL Framework:** We propose a fully model-free, end-to-end DRL framework designed to teach DASMRs precise maneuvering without relying on expert data, predefined trajectories, or handcrafted guidance. ManeuverNet ensures robust learning across a variety of environments, and leverages the SAC [@Haarnoja2018SAC] algorithm enhanced with CrossQ [@Bhatt2024CrossQ] for improved sample efficiency and stability during training.

**- Comprehensive Study of Reward Functions:** We conduct an in-depth study of reward functions for DASMRs, reviewing state-of-the-art reward functions and presenting four novel reward functions for enabling precise maneuvers in non-holonomic robots.

**- Experimental Validation:** We conduct extensive validation of ManeuverNet against a range of DRL and analytical baselines, demonstrating its superior efficiency and robustness. Furthermore, we demonstrate zero-shot transfer capabilities, with the robot consistently performing well in real-world environments across diverse terrains, without any fine-tuning or domain-specific adaptation.

# Related Work

The control of non-holonomic mobile robots, including those with double-Ackermann-steering mechanisms, has traditionally been tackled using classical control techniques [@Thuilot2009; @Hulttinen2020; @double-ackermann-2]. Among these, the TEB planner [@TEBref] is widely used to generate smooth trajectories and perform local obstacle avoidance. However, TEB is highly sensitive to parameter tuning, and small changes in robot dynamics, payload, or tire pressure often necessitate full recalibration [@TEB_parameters_limitation]. Its local obstacle handling, based on RANSAC polygon approximations, can also be overly conservative, sometimes causing the robot to halt or oscillate between forward and backward movements rather than progressing toward the goal.

In recent years, DRL has shown promise for robotic control tasks, but its application has predominantly targeted holonomic systems [@Mehmood2021ITC]. These approaches typically use reward functions $\mathcal{R}_{\text{Euclid}}$ based on Euclidean distance to the goal. While such rewards perform well in holonomic systems, they are not well suited for non-holonomic systems [@Siegwart2005].

Among non-holonomic platforms, differential-drive robots have been the most studied in DRL research [@ZhangWTYWS25; @SOUALHI2025RAS]. Although these robots are non-holonomic, they can rotate in place [@Siegwart2005], which helps reduce some of the challenges of maneuvering. To guide these robots more effectively, the exponential reward function $\mathcal{R}_\text{Exp}$ was introduced, combining both the Euclidean distance and heading error [@SOUALHI2025RAS]. However, this reward function is less effective for Ackermann-steering robots, as they cannot rotate in place and often need to move away from the goal temporarily in order to align correctly [@Yu2010TRO]. Classic reward functions penalize such maneuvers, resulting in sub-optimal policies. Furthermore, small heading misalignments when near the target can cause significant reward losses, which further contributes to the learned policy being sub-optimal.

Some works have proposed DRL solutions specifically for single-Ackermann-steering robots. A notable example is the FastRLap framework [@Stachowicz2023CoRL], which trains an agent to follow a predefined racing trajectory. Its reward function $\mathcal{R}_{\text{FastRLap}}$ encourages fast forward motion along the track and handles complex situations using a finite-state machine and expert demonstrations. While effective for high-speed path-following, FastRLap does not directly address the challenge of maneuvering in constrained environments. Furthermore, its reliance on handcrafted guidance and expert input limits its adaptability and generalization across tasks and robot platforms [@DanielRAL2024; @Stachowicz2023CoRL]. Other studies have addressed Ackermann-steering car parking scenarios using reward functions that combine distance and angle error terms [@Lazzaroni2022APPLEPIES; @Junzuo2021IOP]. While these reward functions $\mathcal{R}_{\text{Car}}$ effectively address alignment maneuvers when the car is initially perpendicular to the desired position, they fall short when dealing with more complex maneuvers. Specifically, they do not account for situations in which the robot must rotate and move along different axes to reach the goal.

To overcome local reward minima and sub-optimal policy convergence in DRL more broadly, two major strategies have been explored. The first is curriculum learning, which gradually increases task complexity to facilitate learning [@Honghu2022AS]. This often involves breaking down a complex goal into intermediate waypoints to help guide the agent. However, all methods that rely on guided training, whether via curriculum learning, imitation learning, or supervised learning, tend to be highly task and environment-specific [@DanielRAL2024; @Stachowicz2023CoRL]. The second is Hindsight Experience Replay (HER) [@Andrychowicz2017HER], which reframes failed trajectories as successful by redefining the goal retroactively. HER uses sparse reward functions $\mathcal{R}_{\text{HER}}$, avoiding penalizing exploratory behaviors that are essential for reaching the goal. HER has proven to be a powerful general-purpose strategy, but it is not tailored to the specific challenges of double-Ackermann-steering control.

Despite growing interest, to the best of our knowledge, no end-to-end DRL framework has been proposed specifically for DASMR, which are more difficult to maneuver. This highlights a critical gap that our work aims to address.

# Problem Statement {#PS}

We consider a DASMR, controlled to make a maneuver to reach a desired 2D position $\boldsymbol{X_d} = (x_d,y_d)$. The DASMR is a non-holonomic platform. Its configuration includes $(\boldsymbol{X_c}, \theta_c)$, where $\boldsymbol{X_c}=(x_c,y_c)$ denotes the center position and $\theta_c$ the orientation of its longitudinal axis (cf. Fig. [2](#fig:ackermann-geom){reference-type="ref" reference="fig:ackermann-geom"}). However, only two DOF (forward motion and change of orientation) can be directly controlled, and the DASMR cannot rotate without moving forward or backward. In this paper, the double-Ackermann configuration is used in a symmetric, negative 4WS setup, where the front and rear wheel steering angles are mirrored, i.e., they are equal in magnitude but opposite in direction relative to the chassis-fixed frame as shown in Fig. [2](#fig:ackermann-geom){reference-type="ref" reference="fig:ackermann-geom"}. Although ManeuverNet can be applied to any kind of DASMR, in this study, we consider large and heavy ($>$ 50 kg) robots, which are generally used in agricultural settings. The robot is initially positioned at the center of a 8-meter side square workspace and can move freely in this environment. The objective is to control the spinning velocity $\omega$ and steering angle $\phi$ of the four robot wheels to reach $\boldsymbol{X_d}$.

:::: {#fig:ackermann-geom .figure latex-placement="!t"}
![](Deflesselle2026ManeuverNet_figs/ackermann_geom.jpg){width="70%"}

::: caption
DASMR rotating around an instantaneous center of rotation (ICR).
:::
::::

A key challenge is enabling the robot to generate feasible maneuvers without relying on prior expert knowledge or pre-defined trajectories. In addition, we assume a model-free setting in which the robot's dynamics are unknown. The robot's wheel spinning acceleration and steering speeds are limited and empirically determined to ensure stability during motion. We train a DRL agent to generate control commands that respect these physical constraints while achieving the desired behavior. This agent interacts with a simulated environment to learn a policy $\pi$ that maximizes cumulative rewards over time. The agent is designed according to the Markov Decision Process (MDP) formalism [@SuttonMIT2018]. An MDP is defined as the tuple $(\mathcal{S}, \mathcal{A}, \mathcal{P}, \mathcal{R})$, where $\mathcal{S}$ is the state space, $\mathcal{A}$ is the action space, $\mathcal{P}$ is the state transition function, and $\mathcal{R}$ is the reward function. At each discrete time step $t$, the agent observes a state $s_t \in \mathcal{S}$, selects an action $a_t \in \mathcal{A}$ according to its current policy, and transitions to a new state $s_{t+1}$ based on $\mathcal{P}$. It then receives a reward $r_t = R(s_t, a_t)$ as feedback. The policy $\pi : \mathcal{S} \rightarrow \mathcal{A}$ is deterministic and maps each state to a specific action. While the distance between the robot and the target point is defined by $d$, the success of reaching $\boldsymbol{X_d}$ is determined by a distance threshold $d_{th}$. Similar to many DRL frameworks [@Zhao2020SimtoReal], ManeuverNet is trained in a simulator.

# Method

In our framework, a DRL agent controls $\omega$ and $\phi$. At the beginning of each training episode, the robot is initialized in the center of a square obstacle-free workspace, and must reach $\boldsymbol{X_d}$.

## RL Background

In robotics, actor-critic algorithms have been successfully used in several control tasks [@DanielRAL2024; @GaspardICRA2024; @GaspardIROS2024]. Actor-critic algorithms rely on the interaction between two dense neural networks (DNNs): an actor and a critic [@DanielRAL2024]. The actor $\mu$, also called the policy network, selects an action $a_t$ based on the current state $s_t$, following $a_t = \mu(s_t)$. The critic $Q$, also called the Q-network, estimates the expected return of the state-action pair $(s_t, a_t)$ by computing the Q-value $Q^\pi (s_t, a_t)$. The critic is updated using the temporal difference learning and the Bellman equation [@SuttonMIT2018], with $Q^\pi_t (s_t, a_t) = r_t + \gamma \mathbb{E} [Q^\pi_{t+1} (s_{t+1}, a_{t+1})]$. The actor is updated by maximizing the expected Q-value.

:::: {#fig:reward-shapes .figure latex-placement="!ht"}
![$\mathcal{R}_\text{ES}$ shape with $c = 4.0$](Deflesselle2026ManeuverNet_figs/ellipse_shape_1_4.png){#sub:ellipse-shape width="\\textwidth"}

![$\mathcal{R}_\text{Ch}$ shape](Deflesselle2026ManeuverNet_figs/tcheby_shape.png){#sub:tcheby-shape width="\\textwidth"}

![$\mathcal{R}_\text{HS}$ shape with $c = 2.0$](Deflesselle2026ManeuverNet_figs/hourglass_shape.png){#sub:hour-shape width="\\textwidth"}

![$\mathcal{R}_\text{Cl}$ shape with $c = 3.0$](Deflesselle2026ManeuverNet_figs/clover_shape.png){#sub:clover-shape width="\\textwidth"}

\

![$\mathcal{R}_\text{Euclid}$ shape](Deflesselle2026ManeuverNet_figs/euclidean_shape.png){#sub:euclid-shape width="\\textwidth"}

![$\mathcal{R}_\text{Exp}$ shape with $K = 0.5$, $\lambda_d = 0.8$ and $\lambda_{\theta} = 0.2$ [@SOUALHI2025RAS] ](figures/dnh_shape.png){#sub:dnh-shape width="\\textwidth"}

![$\mathcal{R}_\text{FastRLap}$ shape with $V$ fixed at $[10, 0]$ m/s [@Stachowicz2023CoRL]](figures/fastrlap_shape.png){#sub:fast-shape width="\\textwidth"}

![$\mathcal{R}_\text{Car}$ shape with $c_1 = 0.01$ and $c_2 = 1.5$ [@Lazzaroni2022APPLEPIES]](figures/rcar_shape.png){#sub:sparse-shape width="\\textwidth"}

::: caption
Comparison between the shape of our reward functions (top) vs. classic state-of-the-art reward functions (bottom). X is the longitudinal axis, Y is the lateral axis, and the robot's center position is at the origin. Each point on the heatmaps represents the reward for a $\boldsymbol{X_d}$ in the same position. Thus, the robot reaches $\boldsymbol{X_d}$ when $\|\boldsymbol{X_d} \| < d_\text{th}$.
:::
::::

## DRL Algorithms

SAC, introduced in [@Haarnoja2018SAC], optimizes both cumulative rewards and policy entropy to encourage exploration and improve stability. Additionally, it uses two critic networks, a technique from Twin Delayed Deep Deterministic Policy Gradient (TD3) [@Fujimoto2018TD3], to mitigate Q-value overestimation bias.

Despite these improvements, SAC is still computationally expensive. To improve learning efficiency, the CrossQ algorithm [@Bhatt2024CrossQ] has been recently proposed as an SAC overlay that eliminates target networks [@Lillicrap2015DDPG]. CrossQ introduces batch normalization layers in the DNN of the actor and the critic, and employs wider critic layers. Experimental results in [@GaspardICRA2024; @Bhatt2024CrossQ] showed that CrossQ outperforms existing actor-critic algorithms while significantly reducing computational times and increasing sample efficiency, making it an interesting solution for robotics applications. Therefore, our DRL agent leverages the SAC algorithm, enhanced with the CrossQ overlay.

## State Space

As described in Section [3](#PS){reference-type="ref" reference="PS"}, the robot's center position is denoted by $\boldsymbol{X_c}$ and its orientation by the yaw angle $\theta_c$. The spinning velocities of the left and right wheels are $\omega_l$ and $\omega_r$. The steering angles of the left and right wheels are $\phi_l$ and $\phi_r$, and the corresponding steering velocities $\dot{\phi}_l$ and $\dot{\phi}_r$. The robot's center linear velocity is $\boldsymbol{V_c} = (\dot x_c, \dot y_c)$, and its angular velocity is $\dot{\theta_c}$. At the time step $t$, we define the DRL agent's current state $\boldsymbol{s_t} \in \mathcal{S}$ as ($\boldsymbol{X_c}$, $\boldsymbol{X_d}$, $\theta_c$, $\omega_l$, $\omega_r$, $\phi_l$, $\phi_r$, $\dot\phi_l$, $\dot\phi_r$, $\boldsymbol{V_c}$, $\dot\theta_c$) $\in \mathbb{R}^{14}$.

## Action Space

When neglecting steering dynamics and assuming ideal Ackermann-steering, the kinematics of the platform can be approximated by a simplistic bicycle model, reducing front and rear pairs of wheels to a single pair of virtual central wheels [@Hulttinen2020]. Since we consider a negative symmetric 4WS configuration, the rear steering angles mirror the front steering angles. Let us define the spinning velocity and the steering angle of the virtual central wheels as $\omega_{c}$ and $\phi_{c}$, respectively. At each time step $t$, the DRL agent outputs an action $\boldsymbol{a_t} = (\omega_c, \phi_c) \in [-1, 1]$, representing normalized commands for the wheel spinning velocity and the steering angle. These values are then scaled by the vehicle's respective actuation limits to obtain the actual control inputs. Following the double-Ackermann-steering geometry, the spinning velocities and steering angles of the left and right wheels can be calculated from $\omega_{c}$ and $\phi_{c}$. For this, we compute the steering angles of the inner and outer wheels $\phi_{i}$ and $\phi_{o}$, relative to the robot's current instantaneous center of rotation (ICR) shown in Fig. [2](#fig:ackermann-geom){reference-type="ref" reference="fig:ackermann-geom"}, as: $$\begin{align}
    \phi_i = \tan^{-1}\frac{2 L \cdot \sin{\phi_{c}}} {2 L \cdot \cos{\phi_{c}} - W \cdot \sin{\phi_{c}}}
\end{align}$$ $$\begin{align}
   \text{and }  \phi_o = \tan^{-1}\frac{2 L \cdot \sin{\phi_{c}}} {2 L \cdot \cos{\phi_{c}} + W \cdot \sin{\phi_{c}}},
\end{align}$$ where $L$ is the wheelbase of the vehicle and $W$ is the track of the vehicle. Similarly, we can compute the spinning velocities of the inner and outer wheels $\omega_{i}$ and $\omega_{o}$ relative to the ICR as: $$\begin{align}
    \omega_{i} = \omega_{c} \frac{ \sqrt{[L \cdot \tan (\frac{\pi}{2} - |\phi_{i}|)]^2 + L^2 } }{ \sqrt{[L \cdot \tan (\frac{\pi}{2} - |\phi_{i}|) + \frac{W}{2}]^2 + L^2} }
\end{align}$$ $$\begin{align}
    \text{ and } \omega_{o} = \omega_{c} \frac{ \sqrt{[L \cdot \tan(\frac{\pi}{2} - |\phi_{i}|) + W]^2 + L^2 } }{ \sqrt{[L \cdot \tan(\frac{\pi}{2} - |\phi_{i}|) + \frac{W}{2}]^2 + L^2} }.
\end{align}$$

These inner and outer wheel spinning velocities and steering angles can then be applied to the left and right wheels based on the sign of $\phi_{c}$. If $\phi_c \geq 0$, the left wheel is the inner wheel, so that $\omega_l = \omega_i$ and $\phi_l = \phi_i$, while the right wheel becomes the outer wheel with $\omega_r = \omega_o$ and $\phi_r = \phi_o$. If $\phi_c < 0$, the roles are reversed, with the right wheel becoming the inner wheel.

## Reward Functions {#reward_new_section}

To address the issue of sub-optimal policies for DASMRs, we introduce the reward $\mathcal{R}_\text{HS}$ (cf. Table [1](#table:rewards){reference-type="ref" reference="table:rewards"}). This reward is designed to handle scenarios where the robot must temporarily deviate from the target to execute a successful maneuver. By prioritizing lateral ($Y$-axis) error over longitudinal ($X$-axis) error, $\mathcal{R}_\text{HS}$ minimizes reward penalties when the robot temporarily moves away from the goal. As shown in Fig. [5](#sub:hour-shape){reference-type="ref" reference="sub:hour-shape"}, this reward is shaped as an hourglass, which reduces penalization during maneuvers.

With the same objective, we also investigate alternative reward functions: $\mathcal{R}_\text{ES}$, $\mathcal{R}_\text{Ch}$, and $\mathcal{R}_\text{Cl}$, each defined in Table [1](#table:rewards){reference-type="ref" reference="table:rewards"}. The reward $\mathcal{R}_\text{ES}$ is a variation of the Euclidean distance that scales the error components asymmetrically, forming an ellipse. The reward $\mathcal{R}_\text{Ch}$ is based on the Chebychev distance focusing on the maximum deviation along either axis, while $\mathcal{R}_\text{Cl}$ extends the exponential reward, proposed in [@SOUALHI2025RAS], by incorporating a directional weighting term specifically tuned for DASMR dynamics. This reward penalizes large lateral deviations and misalignments only when the robot is close to the target $\boldsymbol{X_d}$. A comparative visualization of these reward functions alongside conventional formulations is provided in Fig. [11](#fig:reward-shapes){reference-type="ref" reference="fig:reward-shapes"}.

[]{#table:rewards label="table:rewards"}

:::: center
::: {#table:rewards}
  **Rewards**                                                                    **Formulation**
  ------------------------- -------------------------------------------------------------------------------------------------------------------------
                            
  $\mathcal{R}_\text{HS}$        $-\sqrt{(\Delta x)^2 + \left(c \cdot (\Delta y \pm \max \left\{0, |\Delta y| - |\Delta x| \right\})\right)^2}$
                            
  $\mathcal{R}_\text{ES}$                                            $-\sqrt{(\Delta x)^2 + (c\Delta y)^2}$
                            
  $\mathcal{R}_\text{Ch}$                                        $-\max \left\{ |\Delta x|, |\Delta y| \right\}$
                            
  $\mathcal{R}_\text{Cl}$                                                        $\begin{cases} 
                             \tan^{-1} \left( \frac{\Delta y}{\Delta x} \right) \times c e^{d_\text{th}- d} &\text{ if  $\Delta y > d_\text{th}$ }\\
                                                                             -d &\text{otherwise} \\
                                                                                  \end{cases}$

  : DASMR reward functions where $\Delta x$ and $\Delta y$ are the X and Y components of $\left(\boldsymbol{X_d} -\boldsymbol{X_c}\right)$ and $c$ a weighting parameter.
:::
::::

# Experimental Results {#sec:result}

## Environment Setup

We considered the Shadow Runner RR100 EDU rover as our mobile robot platform. The RR100 weighs approximately 100 kg and is 65 cm wide, 90 cm long, and 80 cm high. The DRL agent controlling the robot was trained using the PyBullet simulator, in an environment defined as follows: the robot is placed at coordinates $(0,0)$, and its movements are limited to an $8\times8\text{ m}^2$ square workspace. When the environment is reset, the robot is reset to initial configuration, and a new $\boldsymbol{X_d} = (x_d, y_d)$ is sampled from a $4 \times 4$ m^2^ goal space. All values, including spaces and goal coordinates, are expressed in the robot's frame at reset. The rationale for using a small goal space is to maximize the number of $\boldsymbol{X_d}$ requiring complex maneuvers. In real-world settings, the robot's workspace and goal space are constrained to the same $4.2 \times 4.2$ m^2^ square, resulting in a more restrictive setup that better reflects practical operating conditions. Fig. [12](#fig:env_spaces){reference-type="ref" reference="fig:env_spaces"} presents the environment setup used in both simulation and real-world experiments.

A training episode is considered successfully terminated when the DRL agent reaches $\boldsymbol{X_d}$ within $d_\text{th}$, regardless of orientation. If the robot fails to reach $\boldsymbol{X_d}$ within a time step limit or drives outside the bounds of its workspace, the episode is truncated, and the environment is consequently reset. We released the code at <https://github.com/MelodieDANIEL/4ws_actor_critic_maneuvering>.

[]{#table:hyperparams label="table:hyperparams"}

::: center
:::

:::: {#fig:env_spaces .figure latex-placement="!h"}
![](Deflesselle2026ManeuverNet_figs/ws_bullet.jpg){width="\\linewidth"}

![](Deflesselle2026ManeuverNet_figs/ws_real.jpg){width="\\linewidth"}

::: caption
Environment setup in simulation and real-world settings. The red square denotes the goal space. The blue square represents the robot's workspace. In real-world settings, both spaces coincide to impose stricter constraints on navigation and positioning.
:::
::::

## Training Setup

The DRL agent was trained in a single, non-vectorized simulation environment for 600,000 time steps, where each episode was limited to 800 time steps before truncation. The agent interacted with its environment at a frequency of 40 Hz, resulting in 40 time steps per second. The training progress was monitored by logging the average episode reward and success rate (SR) every 10 episodes, both computed using a sliding window of 100 episodes. The full training process took approximately 1.5 hours. The training was carried out on a desktop computer equipped with an AMD Ryzen Threadripper PRO 7985WX 64-Cores (AMD Zen 4) CPU, 128 GB of memory, along with an Nvidia RTX 4090 GPU. The DRL algorithms were implemented using the Stable Baselines JAX (SBX) library, leveraging its CrossQ implementation built upon the SAC algorithm. Hyperparameters and network architecture details for both SAC and CrossQ are provided in Table [\[table:hyperparams\]](#table:hyperparams){reference-type="ref" reference="table:hyperparams"}, and were kept consistent in all experiments unless otherwise specified. To ensure reproducibility, detailed network architecture and algorithm parameters are available in our GitHub repository.

## Benchmarking Against Baseline Approaches in Gazebo

To evaluate the effectiveness and generalizability of ManeuverNet, we conducted experiments in the Gazebo simulator, which offers a more realistic physics engine than PyBullet, thereby helping to assess robustness across different simulators (sim-to-sim gap). ManeuverNet combines the SAC framework with CrossQ, together with the reward $\mathcal{R}_\text{HS}$ specifically designed to encourage maneuvers. We compared ManeuverNet with two representative DRL baselines: (i) a standard DRL agent trained with the SAC framework using a Euclidean distance-based reward commonly used for mobile robot navigation [@DRLStandard], and (ii) the single-Ackermann framework FastRLap [@Stachowicz2023CoRL] implemented with the SAC parameters reported in the original publication. To the best of our knowledge, FastRLap is the only available DRL framework for Ackermann mobile robots. In addition to these DRL-based methods, we benchmarked against the analytical TEB planner [@TEBref]. This closed-loop online local planner relies on several inputs, including the robot's current velocity, a local occupancy map, and its global pose estimation, to generate feasible trajectories in real time.

All evaluations were conducted using a different random seed than during training, ensuring exposure to 20 unseen goals. Furthermore, unlike the training setup, the robot was not reset to its initial position after each episode. This forced the agent to handle successive tasks continually, without relying on episodic resets to simplify maneuvering. These evaluation conditions were designed to reflect real-world deployment scenarios and rigorously test the robustness of each method under dynamic and non-ideal circumstances.

Each approach was quantitatively evaluated with the success rate (SR), and the average distance error (AE) and the standard deviation to $\boldsymbol{X_d}$. We also evaluated the average Success weighted by (normalized inverse) Path Length (SPL) [@AndersonSPL]. High SPL values indicate trajectories that are not only successful but also closely aligned with the shortest possible path. Achieving a high SPL is particularly challenging for DASMRs, as reaching the target position often requires complex maneuvers deviating from the optimal path.

As shown in Table [\[table:sim-to-sim\]](#table:sim-to-sim){reference-type="ref" reference="table:sim-to-sim"}, although ManeuverNet does not reach the SR of the TEB planner, it consistently surpasses other DRL baselines. It demonstrates superior maneuvering proficiency while achieving shorter, more efficient trajectories, as evidenced by the average SPL metric. Interestingly, if we only focus on the successfully reached targets, ManeuverNet has a better SPL than TEB (0.89). The AE metric reveals that the standard DRL method gets relatively close to the target but it fails to attain precisely the desired position, primarily due to its limited maneuverability. Differently, FastRLap tends to drift away from the target and not maintain proximity, due to its emphasis on forward motion.

## Comparative Study of the Reward Functions

:::: {#fig:bullet-vs-real .figure latex-placement="!h"}
![](Deflesselle2026ManeuverNet_figs/bullet_traj1.png){width="\\textwidth"}

![](Deflesselle2026ManeuverNet_figs/bullet_traj2.png){width="\\textwidth"}

![](Deflesselle2026ManeuverNet_figs/bullet_traj3.png){width="\\textwidth"}

![](Deflesselle2026ManeuverNet_figs/bullet_traj4.png){width="\\textwidth"}

![](Deflesselle2026ManeuverNet_figs/bullet_traj5.png){width="\\textwidth"}

![](Deflesselle2026ManeuverNet_figs/real_traj1.png){width="\\textwidth"}

![](Deflesselle2026ManeuverNet_figs/real_traj2.png){width="\\textwidth"}

![](Deflesselle2026ManeuverNet_figs/real_traj3.png){width="\\textwidth"}

![](Deflesselle2026ManeuverNet_figs/real_traj4.png){width="\\textwidth"}

![](Deflesselle2026ManeuverNet_figs/real_traj5.png){width="\\textwidth"}

![](Deflesselle2026ManeuverNet_figs/carpet_traj1.png){width="\\textwidth"}

![](Deflesselle2026ManeuverNet_figs/carpet_traj2.png){width="\\textwidth"}

![](Deflesselle2026ManeuverNet_figs/carpet_traj3.png){width="\\textwidth"}

![](Deflesselle2026ManeuverNet_figs/carpet_traj4.png){width="\\textwidth"}

![](Deflesselle2026ManeuverNet_figs/carpet_traj5.png){width="\\textwidth"}

::: caption
An example of a maneuver executed by ManeuverNet in both simulation and real-world settings is shown in the first two rows. Another example, showcasing multi-terrain performance, is presented in the final row of figures. The red dot represents $\boldsymbol{X}_d$.
:::
::::

To assess the effectiveness of our specially designed reward functions for DASMRs (see Section [4.5](#reward_new_section){reference-type="ref" reference="reward_new_section"}), we performed a comparative study under different testing conditions. This study emphasizes the reward functions that best support precise and robust maneuver learning. Additionally we evaluated three reward functions adapted from the literature: 1) $\mathcal{R}_{\text{Exp}}$ [@SOUALHI2025RAS] based on the direction and distance to the target goal; 2) $\mathcal{R}_{\text{HER}}$ [@Andrychowicz2017HER] based on a sparse binary reward function; 3) $\mathcal{R}_{\text{Car}}$  [@Lazzaroni2022APPLEPIES] combining the direction and distance to the target goal for a parking task. In this case, we omitted the collision term as it was unnecessary in our setup.

In this study, the agents were tested in simulation using PyBullet under progressively challenging generalization settings, including: (i) using the same training seed and distance threshold $d_\text{th}$, (ii) using two unseen random seeds with $d_\text{th}= 15$ cm, (iii) evaluating all seeds with $d_\text{th}= 10$ cm. Setting (i) evaluated the agent under familiar conditions. In setting (ii), the sampled goal $\boldsymbol{X_d}$ is altered, which typically requires the robot to perform different maneuvers, thereby testing its ability to generalize to unseen spatial configurations. Setting (iii) evaluated the precision of the learned policy, demanding finer control near the goal.

The corresponding results are summarized in Table [2](#table:simulation_tests){reference-type="ref" reference="table:simulation_tests"}. The results were generated over 100,000 time steps, with a new $\boldsymbol{X_d}$ sampled either when the agent reached the goal or when the episode was truncated after 300 time steps. As shown in Table [2](#table:simulation_tests){reference-type="ref" reference="table:simulation_tests"}, all state-of-the-art reward functions either failed entirely or converged to sub-optimal policies when applied to DASMRs. For example, $\mathcal{R}_\text{Car}$ and $\mathcal{R}_\text{Exp}$ performed poorly, suggesting that they are ill-suited to the maneuvering constraints inherent to DASMRs. Similarly, $\mathcal{R}_\text{HER}$ did not exceed a 55% SR, indicating limited effectiveness. While $\mathcal{R}_\text{Cl}$ achieved moderately better results (72% and 62% of SR), it struggled to generalize to unseen environments, highlighting its lack of robustness.

In contrast, the rewards $\mathcal{R}_\text{HS}$, $\mathcal{R}_\text{ES}$ and $\mathcal{R}_\text{Ch}$ demonstrated greater adaptability to complex maneuvering tasks. Among these, the reward $\mathcal{R}_\text{HS}$ performed the best overall, achieving at least 96% of SR across all test scenarios with $d_\text{th} = 15$ cm and also superior performance in terms of the SPL metric, highlighting its efficiency and reliability. This improvement stems from the stronger weighting of the lateral ($y$) displacement in these rewards, which better captures the sideward maneuvering requirements inherent to DASMR.

Additional results under challenging conditions, specifically continuous goal targeting without pose reinitialization, are available in our GitHub repository. These findings align with the main results and further showcase the flexibility and robustness of our reward functions.

[]{#table:sim-to-sim label="table:sim-to-sim"}

:::: center
::: tabular
l\|l\|\*3c **Approach** & &\
**Type**& & **SR $\uparrow$** & **AE($\boldsymbol{\sigma}$) $\downarrow$** & **SPL $\uparrow$**\
**Analytical** & TEB [@TEBref] & **100** & **0.05** (0.05) & **0.79\
**DRL**&Standard DRL [@DRLStandard] & 45 & 0.25 (0.17) & 0.35\
&FastRLap [@Stachowicz2023CoRL] & 00 & 3.79 (2.11) & 0.00\**

&ManeuverNet (ours) & **85** & **0.15 (0.04)** & **0.70**\
:::
::::

[]{#table:simulation_tests label="table:simulation_tests"}

:::: center
::: {#table:simulation_tests}
+----------------------------+----------------------------+----------------------------------------------------------------------------------+----------------------------------------------------------------------------------+----------------------------------------------------------------------------------+
| **Rew.**                   | $\boldsymbol{d_\text{th}}$ | **Seen**                                                                         | **Unseen 1**                                                                     | **Unseen 2**                                                                     |
+:===========================+:==========================:+:================:+:=========================================:+:=================:+:================:+:=========================================:+:=================:+:================:+:=========================================:+:=================:+
| 3-11                       | \(cm\)                     | **SR$\uparrow$** | **AE($\boldsymbol{\sigma}$)$\downarrow$** | **SPL$\uparrow$** | **SR$\uparrow$** | **AE($\boldsymbol{\sigma}$)$\downarrow$** | **SPL$\uparrow$** | **SR$\uparrow$** | **AE($\boldsymbol{\sigma}$)$\downarrow$** | **SPL$\uparrow$** |
+----------------------------+----------------------------+------------------+-------------------------------------------+-------------------+------------------+-------------------------------------------+-------------------+------------------+-------------------------------------------+-------------------+
| $\mathcal{R}_{\text{Car}}$ | 15                         | 02               | 0.19(0.62)                                | 0.00              | 02               | 0.17(0.75)                                | 0.02              | 02               | 0.17(0.62)                                | 0.02              |
|                            +----------------------------+------------------+-------------------------------------------+-------------------+------------------+-------------------------------------------+-------------------+------------------+-------------------------------------------+-------------------+
|                            | 10                         | 02               | 0.19(0.63)                                | 0.00              | 02               | 0.18(0.76)                                | 0.02              | 02               | 0.17(0.63)                                | 0.02              |
+----------------------------+----------------------------+------------------+-------------------------------------------+-------------------+------------------+-------------------------------------------+-------------------+------------------+-------------------------------------------+-------------------+
| $\mathcal{R}_{\text{Exp}}$ | 15                         | 04               | 0.53(0.20)                                | 0.03              | 04               | 0.55(0.25)                                | 0.03              | 06               | 0.55(0.26)                                | 0.04              |
|                            +----------------------------+------------------+-------------------------------------------+-------------------+------------------+-------------------------------------------+-------------------+------------------+-------------------------------------------+-------------------+
|                            | 10                         | 02               | 0.53(0.24)                                | 0.01              | 02               | 0.56(0.24)                                | 0.01              | 00               | 0.57(0.24)                                | 0.00              |
+----------------------------+----------------------------+------------------+-------------------------------------------+-------------------+------------------+-------------------------------------------+-------------------+------------------+-------------------------------------------+-------------------+
| $\mathcal{R}_{\text{HER}}$ | 15                         | 55               | 0.25(0.21)                                | 0.47              | 50               | 0.28(0.25)                                | 0.40              | 55               | 0.30(0.26)                                | 0.45              |
|                            +----------------------------+------------------+-------------------------------------------+-------------------+------------------+-------------------------------------------+-------------------+------------------+-------------------------------------------+-------------------+
|                            | 10                         | 48               | 0.21(0.19)                                | 0.39              | 45               | 0.22(0.19)                                | 0.35              | 47               | 0.28(0.28)                                | 0.39              |
+----------------------------+----------------------------+------------------+-------------------------------------------+-------------------+------------------+-------------------------------------------+-------------------+------------------+-------------------------------------------+-------------------+
| $\mathcal{R}_{\text{Cl}}$  | 15                         | 72               | 0.27(0.25)                                | 0.64              | 58               | 0.38(0.34)                                | 0.50              | 60               | 0.34(0.29)                                | 0.54              |
|                            +----------------------------+------------------+-------------------------------------------+-------------------+------------------+-------------------------------------------+-------------------+------------------+-------------------------------------------+-------------------+
|                            | 10                         | 62               | 0.26(0.28)                                | 0.53              | 45               | 0.40(0.36)                                | 0.39              | 47               | 0.36(0.32)                                | 0.41              |
+----------------------------+----------------------------+------------------+-------------------------------------------+-------------------+------------------+-------------------------------------------+-------------------+------------------+-------------------------------------------+-------------------+
| $\mathcal{R}_{\text{Ch}}$  | 15                         | 92               | **0.15**(0.03)                            | 0.79              | 82               | **0.16**(0.06)                            | 0.70              | 88               | 0.17(0.12)                                | 0.77              |
|                            +----------------------------+------------------+-------------------------------------------+-------------------+------------------+-------------------------------------------+-------------------+------------------+-------------------------------------------+-------------------+
|                            | 10                         | 81               | 0.13(0.06)                                | 0.66              | 74               | 0.13(0.07)                                | 0.62              | 79               | 0.13(0.13)                                | 0.65              |
+----------------------------+----------------------------+------------------+-------------------------------------------+-------------------+------------------+-------------------------------------------+-------------------+------------------+-------------------------------------------+-------------------+
| $\mathcal{R}_{\text{ES}}$  | 15                         | **97**           | 0.16(0.07)                                | 0.81              | 96               | 0.17(0.16)                                | **0.82**          | 93               | 0.16(0.08)                                | 0.80              |
|                            +----------------------------+------------------+-------------------------------------------+-------------------+------------------+-------------------------------------------+-------------------+------------------+-------------------------------------------+-------------------+
|                            | 10                         | 88               | **0.12**(0.10)                            | 0.71              | **88**           | 0.12(0.11)                                | 0.71              | **85**           | **0.12**(0.09)                            | **0.70**          |
+----------------------------+----------------------------+------------------+-------------------------------------------+-------------------+------------------+-------------------------------------------+-------------------+------------------+-------------------------------------------+-------------------+
| $\mathcal{R}_{\text{HS}}$  | 15                         | **97**           | 0.16(0.22)                                | **0.82**          | **97**           | **0.16**(0.17)                            | **0.82**          | **96**           | **0.15**(0.03)                            | **0.84**          |
|                            +----------------------------+------------------+-------------------------------------------+-------------------+------------------+-------------------------------------------+-------------------+------------------+-------------------------------------------+-------------------+
|                            | 10                         | **89**           | 0.13(0.24)                                | **0.73**          | **88**           | **0.11**(0.04)                            | **0.72**          | **85**           | **0.12**(0.07)                            | 0.69              |
+----------------------------+----------------------------+------------------+-------------------------------------------+-------------------+------------------+-------------------------------------------+-------------------+------------------+-------------------------------------------+-------------------+

: ManeuverNet simulation results for different reward functions on seen, unseen 1, and unseen 2 seeds, with the success rate (SR) in %, the average error (AE) (the standard deviation $\sigma$) in m, and the average SPL.
:::
::::

## Real-World Results {#TEB_exp}

We deployed ManeuverNet with $\mathcal{R}_\text{HS}$ on a real robot using zero-shot transfer, without any fine-tuning. The current state was estimated using the robot's sensors, which include an UM7 IMU, wheel encoders, and an RS-LiDAR-16 3D LiDAR. The robot was controlled via ROS within a real-world, square workspace measuring 4.2 meters per side, bounded by tables. Goal positions were randomly sampled within this area, and all evaluations were conducted using a fixed $d_\text{th} = 15$ cm. As illustrated in Fig. [13](#fig:bullet-vs-real){reference-type="ref" reference="fig:bullet-vs-real"}, the DRL agent successfully controlled the robot with high precision in real-world conditions, despite the absence of any adaptation.

To further assess the generalization capabilities of ManeuverNet, we tested it on a variety of surface types, including vinyl, artificial grass, and carpet. An example is shown in Fig. [13](#fig:bullet-vs-real){reference-type="ref" reference="fig:bullet-vs-real"}. Despite significant differences in ground friction and contact dynamics, the policy maintained consistent and robust performance, underscoring its independence from specific physical parameters of the simulation. Moreover, the robot was not always initialized at the center of the workspace, yet the agent reliably handled arbitrary initial positions and orientations. This demonstrates ManeuverNet's capacity to function effectively in unstructured and non-resettable environments.

To evaluate the effectiveness of ManeuverNet, we performed a comparative study with the TEB planner [@TEBref]. TEB was configured to generate smooth trajectories toward the target positions. To ensure a fair comparison, we sampled the same six successful target positions for both ManeuverNet and the TEB planner. To ensure consistency in evaluation, the desired robot orientation for the TEB planner was matched to the final pose attained by the DRL agent. The comparison in Table [\[table:TEB_vs_DRL\]](#table:TEB_vs_DRL){reference-type="ref" reference="table:TEB_vs_DRL"} demonstrates that, in all targets tested, ManeuverNet consistently produced shorter paths, achieving up to a 90% improvement in the SPL metric. On average, ManeuverNet outperforms TEB by 40% in SPL and reduces navigation time by 28%. Notably, similar trends have been observed in prior work [@Arce2023], which reported superior performance of DRL over TEB in the context of differential-drive robots.

Although both approaches successfully reached the six target positions, several practical limitations help explain the performance differences reported in Table [\[table:TEB_vs_DRL\]](#table:TEB_vs_DRL){reference-type="ref" reference="table:TEB_vs_DRL"}. First, the TEB planner exhibits high sensitivity to the robot's physical state: variations in dynamics, payload, or tire pressure often require fine-tuning and recalibration, which is impractical for real-world deployment. Second, the TEB planner includes a RANSAC-based algorithm for obstacle avoidance, which occasionally causes the robot to halt or oscillate between forward and backward motions, thereby impeding progress toward the goal. This behavior results in inefficient trajectories. Finally, the reliance of the TEB planner on a sequential planning/control loop introduces latency, reducing robot responsiveness during navigation.

[]{#table:TEB_vs_DRL label="table:TEB_vs_DRL"}

## Limitations

Despite the strong performance of ManeuverNet, we have identified a few limitations. First, the current DRL approach does not account for obstacles. The agent is trained and evaluated in obstacle-free environments, which limits its applicability in cluttered or dynamic real-world scenarios where path planning and collision avoidance are critical. A promising solution to address this limitation is to integrate a higher-level planner such as A\*, which could generate a global collision-free path to the target. This was successfully tested, as shown in the video: <https://youtu.be/3-aarbuEOSY>. Alternatively, we can incorporate obstacle avoidance in the learning process by extending the state space and adapting the reward function, as explored in our preliminary work [@Daniel2025ManeuverNetWithObstacles].

Second, ManeuverNet focuses solely on reaching a desired position and does not explicitly handle the robot's final 2D pose. Nevertheless, our framework could be extended to handle precise final poses when needed by adapting the reward function to incorporate orientation constraints, similar to strategies used in goal-conditioned RL [@LiuGCRL].

# Conclusion {#sec:conclusion}

In this work, we proposed ManeuverNet, a DRL framework leveraging SAC and CrossQ, specifically tailored for the control of DASMRs. By designing novel reward functions that better take into account the maneuvering constraints of such robots, we addressed the limitations of existing state-of-the-art methods, which often fail to generalize or converge to sub-optimal policies in this scenario. ManeuverNet was evaluated extensively in simulation under various generalization settings. These included unseen goal distributions, stricter success thresholds, and non-reset scenarios. Across all settings, ManeuverNet consistently outperformed baseline approaches, improving success rate by at least 40% while maintaining efficient trajectories. Furthermore, we demonstrated the framework's zero-shot transfer capabilities in real-world experiments, validating its robustness across diverse terrains and settings without requiring fine-tuning or expert demonstrations. Moreover, when compared to the widely used TEB planner, ManeuverNet improved the maneuvering trajectory efficiency by up to 90%. For future work, we plan to extend our framework by integrating obstacle-aware planning and orientation control, further broadening the versatility and applicability in real-world scenarios.

# Acknowledgment {#acknowledgment .unnumbered}

This work was supported by the French Government under the France 2030 program through the National Research Agency (ANR) grant reference ANR-24-PEAE-0002. It was also funded by the Nouvelle-Aquitaine Region through the MIRAE project. Author M. Aranda was supported through grant RYC2024-051408-I, funded by MICIU/AEI/10.13039/501100011033 and by ESF+.

[^1]: \*These authors contributed equally.

[^2]: $^{1}$Univ. Bordeaux, CNRS, Bordeaux INP, LaBRI, UMR 5800, F-33400 Talence, France. $^{2}$School of Computer Science, University of Nottingham, UK. $^{3}$Instituto de Investigación en Ingeniería de Aragón (I3A), Universidad de Zaragoza, 50018 Zaragoza, Spain. Author's Accepted Manuscript. Released under the Creative Commons license: Attribution 4.0 International (CC BY 4.0). Corresponding author: Mélodie Daniel, e-mail: `melodie.daniel@u-bordeaux.fr.`
