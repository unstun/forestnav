---
citation_key: Caro2025Push
arxiv_id: 2512.10099
arxiv_url: https://arxiv.org/abs/2512.10099
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-23T18:56:05Z
origin: ai+web
reviewed: false
---

# Introduction {#sec:introduction}

Nonprehensile manipulation (manipulation without grasping) is a fundamental capability for general-purpose robots operating in cluttered or constrained environments. Compared to prehensile manipulators, such as gripper arms, nonprehensile manipulators can interact with multiple objects and are more accommodating of simple, low-cost hardware. While gripper arms offer some unique advantages, many real-world scenarios, such as area-clearing or transporting large or ungraspable objects, are better suited for nonprehensile strategies. Although humans intuitively learn these skills at a young age, the task remains highly complex in robotics due to the nonlinear and contact-rich dynamics of pushing [@stuber_lets_2020].

Reinforcement learning (RL) is well-suited for goal-directed tasks, as it optimizes behaviour through trial and error based on reward signals. In robotic settings, RL policies often operate over low-level control signals such as wheel velocities or discrete movement commands (e.g., move forward, turn left) [@aljalbout_role_2024]. As a result, these policies must simultaneously learn task-relevant strategies and develop an understanding of the robot's dynamics. This dual burden makes learning more challenging, especially in contact-rich tasks like nonprehensile manipulation. Hierarchical RL addresses this challenge by separating high-level decision-making from low-level control. Wu et al. demonstrated that using Spatial Action Maps (SAM) [@wu_spatial_2020], where an RL policy outputs spatial goals, combined with a separate controller for execution, improves performance in nonprehensile manipulation tasks.

Diffusion models are a branch of generative models originally developed for image generation tasks, but have recently shown promising applications in robotics due to their ability to produce diverse, high-dimensional, and temporally coherent trajectories [@janner_planning_2022; @chi_diffusion_2024]. Trained on human demonstrations, diffusion policies capture rich behavioural priors that reflect intuitive control strategies. In our case, these include stabilizing contact during object manipulation, anticipating future interactions, and avoiding disruptive collisions -- strategies which are intuitive for a human but are difficult to learn from reinforcement alone, especially in the presence of sparse or delayed rewards. While much promise is shown here, diffusion policies are limited by the quality and diversity of the demonstrations provided. To address this limitation, we offload high-level planning to an RL agent, allowing the diffusion policy to focus on trajectory generation, where high quality demonstrations are easier to collect at low cost.

::::: {#fig:physical .figure}
::: minipage
ıin 1,\...,5 ![image](Caro2025Push_figs/\i_comp.jpg){width="0.36\\columnwidth"}
:::

::: caption
The robot (highlighted in red) is tasked with pushing the boxes into the green receptacle. This sequence of images shows a robot using the proposed HeRD policy gathering three boxes and pushing them into the receptacle.
:::
:::::

We seek to improve the spatial action maps formulation in two ways: increasing success rate and lowering the distance required of the agent to complete the task. Our work makes the following contributions:

- We introduce a goal-conditioned diffusion policy framework capable of producing collision-free trajectories by enforcing feasibility constraints. We then train this policy using human demonstrations to generate trajectories to navigate to spatial goals.

- We propose **H**i**e**rarchical **R**einforcement Learning - **D**iffusion Policy (**HeRD**) that combines the high-level planning of spatially-aware RL with the context-aware trajectory generation of a diffusion policy, and outperforms the state-of-the-art SAM policy in [@wu_spatial_2020] in terms of success and distance in a range of environments. Key to our approach is a new reward function that encourages the RL agent to act more efficiently.

- Finally, in our physical implementation, we observe a substantial increase in success rate of the HeRD policy when compared to the current state-of-the-art policy.

# Related Work {#sec:related_work}

Nonprehensile manipulation is inherently challenging due to the underactuated nature of the system from the limited set of forces that can be transmitted to the object from an agent [@hogan_reactive_2020], and the highly non-linear dynamics of pushing [@stuber_lets_2020]. Prior work has addressed these challenges using model-based and feedback control approaches. For instance, reactive controllers adapt to contact uncertainties during pushing [@ozdamar_pushing_2024], while model predictive control methods reason over contact forces and future trajectories to maintain stable pushes [@tang_unwieldy_2023; @bauza_data-efficient_2018].

More recently, learning-based methods, particularly reinforcement learning, have become popular for developing closed-loop manipulation policies. Action space design plays a crucial role in these methods. Continuous-control policies typically operate directly in low-level action spaces such as linear and angular velocities [@sun_integrating_2023; @del_aguila_ferrandis_nonprehensile_2023]. While expressive, these actions combine low-level motion control with high-level planning, forcing the RL agent to learn both precise robot dynamics and long-horizon task structure simultaneously, making training inefficient. On the other hand, discretized motion primitive action spaces improve learning stability [@yuan_rearrangement_2018], but they introduce their own challenges: meaningful reward signals may arise only after executing long sequences of motion primitives, making exploration difficult in long-horizon tasks [@wu_spatial_2020].

Spatial Action Maps (SAMs) address this tradeoff by treating the action space as a dense grid of spatial goals. They decouple high-level decision-making from low-level motion control, improving sample efficiency and generalization. The discrete nature of SAMs lends them to be a useful action representation for Deep Q-Networks [@mnih_playing_2013]. In our work, we use the Double DQN variant [@hasselt_deep_2015]. SAMs have shown success in pushing [@wu_spatial_2020], blowing [@wu_learning_2022], and multi-agent manipulation [@wu_spatial_2021]. However, these works do not consider the state of the environment when generating paths from the output of the SAM; we address this by using a generative diffusion policy conditioned on the state of the environment to make context-aware paths.

The SAM framework can be viewed as a form of implicit hierarchy: the high-level agent chooses a spatial subgoal, and a low-level controller executes it. Hierarchical Reinforcement Learning (HRL) decomposes complex tasks into a hierarchy of subgoals or options [@sutton_between_1999; @vezhnevets_feudal_2017]. This reduces the effective planning horizon and improves sample efficiency, particularly in sparse-reward settings. Our method makes this hierarchy explicit by pairing a goal-predicting DDQN policy with a denoising diffusion probabilistic model (DDPM) [@sohl-dickstein_deep_2015; @ho_denoising_2020] for path generation. DDPMs are generative diffusion models with recent applications in robotics that sample structured action sequences via iterative denoising [@janner_planning_2022] and can be conditioned on observations [@chi_diffusion_2024].

A central challenge in diffusion-based control is guiding the generation process toward task-relevant outcomes. In our framework, we use goal inpainting [@janner_planning_2022], which conditions the trajectory endpoints by fixing them to specific targets, as well as FiLM [@perez_film_2018] layers to encode observations to ensure geometry-aware trajectory synthesis.

It is worth noting related works that use hierarchical diffusion policies. HDMI [@li_hierarchical_2023], Hierarchical Diffuser [@chen_simple_2024], and HDP [@ma_hierarchical_2024] all adopt a two-level diffusion architecture: a high-level model generates subgoals or intermediate keyframes, and a low-level diffusion model produces the full trajectory segments that reach them. Other approaches, such as [@wang_hierarchical_2025; @wu_diffusion-reinforcement_2025], combine high-level diffusion models for subgoal generation with low-level controllers trained via reinforcement learning, forming hybrid architectures that integrate generative planning with policy-based execution.

Our method adopts a complementary hierarchical structure: the high-level planner is a value-based reinforcement learning policy that selects spatial subgoals, while the low-level controller is a goal-conditioned diffusion model that synthesizes smooth, feasible trajectories to those targets.

# Problem Formulation and Spatial Action Map Overview {#sec:problemformulation}

In this section, we first formulate the task as a Markov decision process and specify the objectives we aim to optimize. We then provide an overview of spatial action maps, including details about the state and action spaces, and the reward function used in the original paper.

## Problem Formulation

We consider an environment $\mathcal{W} \subset \mathbb{R}^2$ containing $n$ fixed obstacles $\mathcal{O}_1, \ldots, \mathcal{O}_n \subset \mathcal{W}$, a receptacle $\mathcal{B} \subset \mathcal{W}$, $m$ movable boxes, and a mobile robot. At time $t \geq 0$, each box $j\in\{1,\ldots,m\}$ is described by a time-varying set $b_j(t) \subset \mathcal{W}$, defining the 2D space occupied by the box. Likewise, the robot is described by $\mathcal{R}(t) \subset \mathcal{W}$. The robot navigates within the free space $\mathcal{W}_{\text{free}} = \mathcal{W} \setminus \left( \cup_i \mathcal{O}_i \right)$. The task of the robot is to successfully push all boxes into the receptacle by a given time $T_{\max}$: That is, to reach a state at some time $t'\in[0,T_{\max}]$ where $b_j(t') \subset \mathcal{B}$ for all $j \in \{1, \ldots, m\}$.

**Objective.** Our objective is to compute a robot policy $\pi$ that optimizes a two-tiered objective, capturing both task success and the efficiency of robot behaviour. The *Primary Objective* is to maximize the expected number of boxes placed in the receptacle by time $T_{\max}$. Formally, the primary objective corresponds to maximizing the success indicator: $$\begin{equation*}
        \sum_{j=1}^m \mathbf{1}[b_j(T_{\max})\subset \mathcal{B}].
\end{equation*}$$ The *Secondary Objective* is to minimize the time to complete the task. Formally, we seek to minimize: $$\begin{equation*}
        \min \big\{t \in[0,T_{\max}] \; | \; b_j(t) \subset \mathcal{B} \text{ $\forall \; j\in\{1,\ldots,m\}$}\big\},
\end{equation*}$$ where the completion time is $T_{\max}$ if not all boxes are in the receptacle by time $T_{\max}$.

This tiered formulation encourages the agent to reliably complete the task while favouring efficient policies.

**MDP Model.** We model the problem as a Markov decision process (MDP), defined by the tuple $(\mathcal{S}, \mathcal{A}, \mathbb{P}, R, \gamma)$, where $\mathcal{S}$ is the state space consisting of the robot position and environment configuration and $\mathcal{A}$ is the action space. At each time step, the robot observes a state $s \in \mathcal{S}$ and chooses an action $a \in \mathcal{A}$ according to a policy $\pi:\mathcal{S}\to \mathcal{A}$. The environment transitions to a new state $s' \sim \mathbb{P}(s'|s, a)$ and emits a scalar reward $r = R(s, a)$, where the scalar reward acts as a proxy for the multi-objective optimization stated above. The constant $\gamma \in (0,1)$ is the discount factor.

## Spatial Action Maps {#sec:sam_details}

In this section, we review the spatial action map (SAM) policy as proposed in [@wu_spatial_2020]. To motivate the use of SAMs, we first formulate the task as a reinforcement learning problem. To solve the above MDP, we adopt a value-based RL approach using a Double Deep Q-Network (DDQN) [@hasselt_deep_2015]. The goal is to learn an action-value function $Q_\theta:\mathcal{S} \times \mathcal{A} \rightarrow \mathbb{R}$, parameterized by $\theta$, that estimates the expected cumulative discounted reward when taking action $a$ in state $s$ and following an optimal policy thereafter.

During training, transitions $(s,a,r,s')$ are uniformly sampled from an experience replay buffer [@lin_self-improving_1992], and the online network parameters $\theta$ are updated to minimize the following temporal difference loss: $$\begin{equation*}
    \mathcal{L}(\theta) = \left| r + \gamma Q_{\theta'}\left( s', \arg\max_{a'} Q_\theta(s', a') \right) - Q_\theta(s, a) \right|,
\end{equation*}$$ where $Q_{\theta'}$ is the target network with frozen parameters $\theta'$ periodically updated from $\theta$.

The resulting policy is derived greedily from the learned Q-function: $$\begin{equation*}
    \pi_{\theta}(s) = \arg\max_a Q_\theta(s, a).
\end{equation*}$$

SAMs define a dense, pixel-aligned action space where each action corresponds to a goal coordinate in the robot's environment. The Q-network $Q_\theta(s, a)$ outputs a heatmap over all spatial locations, representing the value of navigating to each coordinate. The policy $\pi_{\theta}(s)$ selects the pixel with the highest Q-value, which becomes the high-level goal for the robot. A path is then generated to this goal point using the Shortest Path Faster Algorithm (SPFA) [@fanding_spfa_1994], and a low-level controller is used to traverse the path. This process is summarized in Algorithm [\[alg:orig\]](#alg:orig){reference-type="ref" reference="alg:orig"}. The rest of this section details the state space, action space, and reward function, which are central to this formulation.

::::: algorithm
:::: small
::: algorithmic
policy $\pi_{\theta}$, robot position $p_{\mathcal{R}}$, controller $c$ Observe state $s$ Select action $a = \pi_{\theta}$ $\texttt{path} \leftarrow \texttt{SPFA}(p_{\mathcal{R}}, a)$ Initialize controller $c_{\text{active}} \gets c(\texttt{path})$ Execute $c_{active}$ until goal $a$ is reached
:::
::::
:::::

Each state $s \in \mathcal{S}$ is encoded as a 4-channel image aligned to the robot's local coordinate frame, with spatial resolution $(H, W)$. The channels include: (1) A semantic segmentation map encoding object classes (e.g., obstacles, floor, boxes, robot, receptacle); (2) A binary mask representing the robot's footprint and location; (3) A shortest-path distance map from the robot's current position to each pixel; and (4) A shortest-path distance map from each pixel to the receptacle. This yields a structured state space $\mathcal{S} = [0,1]^{H \times W \times 4}$. An example visualization is shown in Fig. [6](#fig:sam_state){reference-type="ref" reference="fig:sam_state"}.

:::: {#fig:sam_state .figure latex-placement="tbp"}
![Overhead Map](Caro2025Push_figs/channel_0_Overhead_Map.png){#fig:obs_0 width="\\linewidth"}

![Robot Footprint](Caro2025Push_figs/channel_1_Robot_Footprint.png){#fig:obs_1 width="\\linewidth"}

![Shortest path from robot](Caro2025Push_figs/channel_2_Shortest_Path_to_Robot.png){#fig:obs_2 width="\\linewidth"}

![Shortest path to receptacle](Caro2025Push_figs/channel_3_Shortest_Path_to_Receptacle.png){#fig:obs_3 width="\\linewidth"}

::: caption
Visualization of the four-channel state representation in the *LargeDivider* environment (colors shown for clarity only).
:::
::::

Each action $a \in \mathcal{A}$ represents a pixel location $(u, v)$ in the spatial map: $\mathcal{A} =\{1, \dots, W\} \times \{1, \dots, H\}$. The selected coordinate becomes the high-level goal, and the robot uses a low-level controller to navigate to it.

The total reward at a given step $k$ is composed of three components: $$\begin{equation}
    r(k) = r_{\text{goal}}(k) + r_{\text{progress}}(k) + r_{\text{penalty}}(k),
\end{equation}$$ where: $$\begin{alignat}
{3}
&r_{\text{goal}}(k)     &=\;& +1      \; \text{for each box placed in receptacle}, \\
&r_{\text{progress}}(k) &=\;& \alpha \sum_j \Delta d_{b_j}(k), \label{eqn:cum_rew} \\
&r_{\text{penalty}}(k)  &=\;& -0.25   \; \text{for a collision or nonmovement}.
\end{alignat}$$

Here, $\Delta d_{b_j}(k)$ denotes the signed change in shortest-path distance from box $b_j$ to the receptacle at step $k$, and $\alpha$ is a scaling coefficient that ensures the progress reward is on a comparable scale to the other reward terms. The value of $\alpha$ is chosen empirically based on the environment size, such that progress rewards do not dominate the reward signal and overwhelm goal completion or penalty terms.

# Approach Overview {#sec:approach}

:::: {#fig:overview .figure latex-placement="t"}
::: caption
HeRD architecture. The high‑level RL policy encodes observations into a spatial action map and selects a spatial goal, which is converted to a path using SPFA. If the path intersects boxes, it is executed by a proportional controller that first rotates then translates the robot; otherwise, a diffusion policy generates a goal‑conditioned trajectory through denoising and feasibility conditioning.
:::
::::

We design a hierarchical control framework, **HeRD**, that separates high-level semantic decision-making from low-level path planning. The high-level policy selects spatial goals using reinforcement learning with a SAM action representation [@wu_spatial_2020], while a low-level controller determines how to move the robot toward that goal.

Our key contribution lies in adapting the trajectory generation strategy depending on whether the path to the spatial goal requires interacting with movable objects (i.e., boxes):

1.  If the SPFA-computed path to the spatial goal intersects a boxes, we retain the original path to exploit pushing behaviour.

2.  Otherwise, we generate a new trajectory using a learned diffusion policy $\pi_d$, trained on human demonstrations, which captures human-like strategies for positioning, navigation, and setup in scenarios where no immediate box interaction is required.

Our decision to use the diffusion policy only when no boxes are intersected stems from an asymmetry in the learning signal provided by the reward function. There is strong, immediate reward feedback when the robot pushes a box ($r_{\text{progress}}$), but when just navigating, the only available reward signal is the occasional penalty for colliding with an obstacle or not moving, and a distance-based penalty (See Eqn. [\[eqn:sdp\]](#eqn:sdp){reference-type="ref" reference="eqn:sdp"} in Sect. [5.1](#sec:RLP){reference-type="ref" reference="sec:RLP"}). We hypothesize that the strong feedback when pushing enables the policy to specialize in this task. In contrast, there are complex and subtle concepts involved in efficiently navigating the robot that are difficult to encode into a reward function. Strategically repositioning or avoiding boxes en route to a spatial goal are tasks that are easy for a human to carry out, but very hard to encode into a reward function. By deferring to the diffusion policy in these situations, we leverage the intuition of the human demonstrator to generate effective trajectories for the robot.

The overall architecture is visualized in Fig. [7](#fig:overview){reference-type="ref" reference="fig:overview"}. Further details on the policy and training are provided in Section [5](#sec:implementation){reference-type="ref" reference="sec:implementation"}.

# Implementation Details {#sec:implementation}

## Reinforcement Learning Policy {#sec:RLP}

We formulate the high-level RL policy as a DDQN with a SAM action representation, following the architecture described in Section [3.2](#sec:sam_details){reference-type="ref" reference="sec:sam_details"}, with two notable modifications to the reward function. Qualitatively, we observe that the current policy often engages in inefficient behaviour: rather than directly pushing boxes to the receptacle, the robot tends to gather them into a corner before attempting group pushes along walls. It frequently performs backward movements or pushes boxes away from the receptacle in hopes of later combining them. This strategy leads to excessive travel and coordination failures, particularly in larger or more constrained environments. To address this behaviour we (1) modify the $r_{\text{progress}}$ reward term and (2) add a new $r_{\text{motion}}$ term.

**Progress-based reward.** In the original SAM formulation, the robot received a reward based on the total signed progress of all boxes toward the receptacle (Eqn. [\[eqn:cum_rew\]](#eqn:cum_rew){reference-type="ref" reference="eqn:cum_rew"}), which heavily incentivized the agent to push multiple boxes at once. While this inherently is not a negative quality, it often leads to unnecessarily long and inefficient paths in order to gather boxes to push them together.

To align with our objective of minimizing time to task completion, we redefine the reward to consider only the signed progress of the single most-advancing box per step: $$\begin{equation}
\label{eqn:max_rew} r_{\text{progress}}(k) = \alpha \cdot \Delta d_{b_j^*}(k), \quad \text{where} \; j^* = \arg \max_j |\Delta d_{b_j}(k)|,
\end{equation}$$ and $\Delta d_{b_j}(k)$ represents the distance box $j$ travels towards the receptacle at step $k$. This preserves the directional component of progress while avoiding reward inflation from simultaneous multi-box pushes. As a result, the agent tends to act more efficiently, choosing to push nearby boxes individually rather than engaging in complex, inefficient maneuvers to gather and push multiple boxes at once. Nevertheless, the agent can still exploit favourable multi-box pushes if they arise naturally.

We use $\alpha = 0.2$, consistent with [@wu_spatial_2020], to normalize progress rewards and prevent them from dominating other terms.

**Distance-based penalty.** To further encourage efficient trajectories, we introduce a penalty based on the robot's displacement at each step. The penalty is scaled to be smaller than the reward for a correct box push, ensuring that the agent is not heavily penalized for non-pushing actions, giving it the $$\begin{equation}
\label{eqn:sdp}
r_{\text{motion}}(k) = -\frac{\alpha}{\beta} \cdot \Delta d_{\mathcal{R}}(k).
\end{equation}$$ Here, $\Delta d_{\mathcal{R}}(k)$ denotes the distance the robot travels at step $k$. We use $\beta=8$, but found that values in $[2,16]$ work with similar effectiveness.

We adopt the hyperparameters used in [@wu_spatial_2020], summarized as follows: *Replay Buffer* of 10,000 transitions; *Optimizer* is SGD with learning rate 0.01, momentum 0.9, and weight decay 0.0001; *Loss Function* is Smooth L1 loss with gradients clipped at 10; *Batch Size* is 32; *Discount Factor* is $\gamma = 0.99^{0.25 \cdot d_{\mathcal{R}(t)}}$, to reflect distance travelled per step (see [@wu_spatial_2020] for more details); *Exploration* via $\epsilon$-greedy with $\epsilon$ linearly annealed from 1.0 to 0.01 over 6,000 steps; *Training Duration* is 60,000 steps; *Random Warm-up* is 1,000 random exploration steps before training begins.

While [@wu_spatial_2020] trains four specialized policies, one per environment type, due to our more efficient reward design we are able to train one generalized policy with minimal performance loss due to the generalization. To do this, we randomly select between the *LargeColumns* or *LargeDivider* environments every episode (see Fig. [12](#fig:env){reference-type="ref" reference="fig:env"} for the environment types), which forces the policy to adapt to various obstacle configurations. We define an episode as terminated when either all of the boxes are pushed into the receptacle or if the robot has not pushed any boxes into the receptacle for 100 steps. We assume access to ground-truth state observations in simulation to eliminate partial observability and better isolate the impact of our reward and architecture modifications. Training takes about 8 hours on an NVIDIA L40S GPU.

:::: {#fig:env .figure latex-placement="htbp"}
![*SmallEmpty*](Caro2025Push_figs/small_empty.png){#fig:a width="\\linewidth"}

![*SmallColumns*](Caro2025Push_figs/small_columns.png){#fig:b width="\\linewidth"}

![*LargeColumns*](Caro2025Push_figs/large_columns.png){#fig:c width="\\linewidth"}

![*LargeDivider*](Caro2025Push_figs/large_divider.png){#fig:d width="\\linewidth"}

::: caption
Evaluation environments used in HeRD. We use four environments varying in size and obstacle layout. The *Small* environments measure 10m$\times$`<!-- -->`{=html}5m and contain 10 boxes; the *Large* environments are 10m$\times$`<!-- -->`{=html}10m with 20 boxes. At each episode reset, the positions of the robot, boxes, and static obstacles are randomized. The number of columns ranges from 0--2 in the *Small* environments and 0--8 in the *Large* ones.
:::
::::

## Diffusion Policy

::::: {#fig:action .figure}
::: minipage
ıin 2,\...,5 ![image](Caro2025Push_figs/\i.png){width="0.36\\columnwidth"}
:::

::: caption
Denoising process of a generated path. The high-level RL policy selects a spatial goal (the black dot in the figure), and the low-level diffusion policy generates a context-aware trajectory from the robot to the spatial goal.
:::
:::::

:::: {#fig:denoise .figure latex-placement="t"}
::: caption
Diffusion-based trajectory generation pipeline. At each difusion timestep $i$, the trajectory $\tau^i$ is denoised using a 1D U-Net conditioned on observation features. The trajectory's endpoints are fixed via goal inpainting: the first point is the robot's position, and the last is the spatial goal. If $i > 0$, the intermediate points are further denoised. Once denoising completes ($i = 0$), the trajectory undergoes a feasibility pipeline: each waypoint is projected to free space if necessary, redundant waypoints are pruned, and path segments crossing obstacles are repaired via SPFA. The final output is a smooth trajectory that respects geometric constraints.
:::
::::

Our diffusion-based controller generates trajectories from demonstration data to guide the robot toward a spatial goal in non-pushing scenarios. It is queried during execution when the SAM-selected goal is reachable without box interaction. Fig. [13](#fig:action){reference-type="ref" reference="fig:action"} shows one such diffused path.

Following [@chi_diffusion_2024], we implement a conditional diffusion model using a 1D U-Net for denoising, conditioned via FiLM layers [@perez_film_2018] on low-dimensional observation features. Unlike the receding-horizon approach used in [@chi_diffusion_2024], we generate the entire trajectory in a single forward pass. This is necessary to support goal conditioning via inpainting [@janner_planning_2022], where at every denoising step we fix the first point of the trajectory to the robot's current position and the last point to the spatial goal. This guides the waypoints into a coherent trajectory. Receding-horizon rollouts are incompatible here, as they lack a consistent final waypoint.

The denoising process is defined iteratively as $$\begin{equation}
    \tau_t^{i-1} = a\left( \tau_t^i - \lambda \, \epsilon_\theta(\mathbf{O}_t, \tau_t^i, i) + \mathcal{N}(0, \sigma^2 I) \right),
    \label{eqn:condDDPM}
\end{equation}$$ where $\tau^i$ is the noisy trajectory at timestep $i$, $\mathbf{O}_t$ is the observation vector, $\epsilon_\theta$ is the noise prediction network, $a(\cdot)$ enforces the goal conditioning, and $\lambda\in(0,1)$ is the discount factor in the diffusion process. The model is trained to minimize the standard denoising loss: $\mathcal{L} = \text{MSE} \left( \epsilon^i, \epsilon_\theta(\mathbf{O}_t, \tau^0 + \epsilon^i, i) \right)$, and generates 32-point trajectories using DDIM sampling at inference time.

To collect expert demonstrations for training the diffusion policy, we deployed a pretrained high-level policy in a large, obstacle-free environment (*LargeEmpty*) to generate spatial goals. For each episode, a human demonstrator teleoperated the robot to navigate toward the SAM-selected goal while strategically considering the most effective path to the goal. These considerations included grouping boxes against walls, avoiding interactions with boxes that would be easier to push later, and pushing multiple boxes at once.

Each demonstration episode begins at the robot's initial position and ends at the SAM-specified goal location. Trajectories are recorded by logging the robot's $(x, y)$ position at fixed intervals of 0.3 meters of travel, producing a sequence of sparse, evenly spaced waypoints. To improve smoothness and standardize input dimensions for the diffusion policy, we then apply linear interpolation between these waypoints to generate a dense 32-point trajectory per episode.

Approximately 1,000 episodes were collected. To augment the dataset, we generate additional demonstrations by selecting any non-interpolated waypoint from an existing trajectory as the new starting position, and padding the end of the trajectory with the spatial goal to maintain the fixed length. This yields $\sim$`<!-- -->`{=html}13,500 valid demonstrations for training.

Each demonstration is paired with a state observation composed of: (1) the 4-corner vertices of the robot and receptacle, (2) the $(x, y)$ positions of the four closest boxes to the robot, and (3) the spatial goal. If fewer than four boxes remain in the environment, placeholder boxes centered within the receptacle are used to preserve a fixed input size. All state inputs are normalized following the protocol from [@chi_diffusion_2024]. We made the design decision to include only the four closest boxes based on our empirical hypothesis that human demonstrators struggled to consider more than four boxes when teleoperating the robot. In addition, we found that the orientation of the boxes was not essential to include in the state, allowing us to further reduce the state space by only including the box positions.

The diffusion model was trained for 3,500 epochs using a batch size of 256, with a validation split of $2\%$. Optimization was performed using AdamW ($\beta_1 = 0.95$, $\beta_2 = 0.999$, $\epsilon = 10^{-8}$, weight decay $= 10^{-6}$, learning rate $= 10^{-4}$). Validation was performed every 10 epochs. Although full training took approximately 1 hour on a single NVIDIA L40S GPU, we selected the checkpoint with the lowest validation loss, which occurred at epoch 350. This corresponds to roughly 6 minutes of training time in practice. We trained with 100 denoising steps but use 15-step DDIM sampling at inference to improve efficiency.

To ensure the diffusion path is feasible, we use the following postprocessing procedure:

1.  *Goal Conditioning:* All sampled trajectories should start at the robot and end at the spatial goal. We use conditioning-by-inpainting to replace the first and last sampled points in the trajectory with the robot's position and spatial goal.

2.  *Waypoint Feasibility:* Each waypoint is checked for collision; if it lies within an obstacle, it is projected to the nearest valid point in $\mathcal{W}_{free}$.

3.  *Pruning:* Waypoints are sparsified via a distance threshold. This results in a more efficient trajectory without compromising fidelity.

4.  *Trajectory Feasibility:* Even if all waypoints lie in free space, sequential points may straddle obstacles. Line segments crossing obstacles are repaired using SPFA.

The complete denoising process is shown in Fig. [14](#fig:denoise){reference-type="ref" reference="fig:denoise"}.

# Results

::: table*
:::

We evaluate the performance of HeRD on the *Box-Delivery* task from Bench-NPIN [@zhong_bench-npin_2025], where the objective is to push scattered boxes into a receptacle while navigating through randomized environments with varying levels of fixed obstacles. We test across four environments of increasing difficulty, as illustrated in Fig. [12](#fig:env){reference-type="ref" reference="fig:env"}. Each trial initializes the robot, boxes, and obstacles at random positions. For fair comparison, all models are evaluated on the same random seed, with 20 trials per environment.

We report two primary metrics: (1) the number of boxes successfully delivered to the receptacle, and (2) the total distance travelled by the robot within the episode.

**Comparison to baseline.** We first compare HeRD to the state-of-the-art spatial action maps (SAM) formulation presented in [@wu_spatial_2020]. As in the original implementation, we train a separate SAM model per environment. In contrast, we train a single generalized HeRD policy.

Evaluation results in Table [\[tab:baseline\]](#tab:baseline){reference-type="ref" reference="tab:baseline"} show that HeRD achieves both higher success rates and significantly shorter paths than the SAM baseline. As we discuss in further detail below, the reward modifications improve the behaviour of HeRD by deterring the inefficient box-grouping actions seen in the baseline, shown in Fig. [17](#fig:behaviour){reference-type="ref" reference="fig:behaviour"}. This combined with the generative paths account for the increased success of HeRD. For instance, in *LargeDivider*, the baseline travels an average of $705$ meters, representing a $104\%$ increase in distance travelled compared to HeRD. Despite being trained as a single generalized policy, HeRD consistently outperforms these specialized baselines in both efficiency and success.

:::: {#fig:behaviour .figure latex-placement="tbp"}
![HeRD](Caro2025Push_figs/ours.png){#fig:ours width="\\linewidth"}

![Baseline](Caro2025Push_figs/baseline.png){#fig:base width="\\linewidth"}

::: caption
The difference in behaviour of HeRD compared to the baseline. The figure shows the first few actions of each policy in the same environment. HeRD immediately seeks out boxes to push into the receptacle while the baseline focuses on gathering multiple boxes together, even pushing them backwards to do so.
:::
::::

**Effect of separating pushing and non-pushing actions.** We hypothesize that the high-level policy specializes in pushing actions but struggles to plan efficient navigation actions, which is why we utilize diffusion for these scenarios. To validate this design, we compare HeRD to two ablations: one trained *without* a diffusion policy, and one that uses the diffusion policy *exclusively* for all trajectories. See Table [\[tab:ablation\]](#tab:ablation){reference-type="ref" reference="tab:ablation"}.

The "No diffusion trajectories" variant outperforms the "Only diffusion trajectories" variant in both success rate and efficiency. This supports our claim that the high-level policy excels at pushing, and also highlights the limitations of relying entirely on diffusion-generated paths. Diffusion trajectories lack the fine-grained precision required for effective pushing, especially in cluttered or multi-box scenarios. A much larger demonstration dataset would be required to overcome this.

HeRD outperforms both ablations, indicating that combining high-level policy competence with selectively deployed diffusion trajectories offers the best of both worlds. We observe improved sample efficiency as well: Fig. [18](#fig:training_curve){reference-type="ref" reference="fig:training_curve"} shows that HeRD converges roughly 16,000 samples earlier than the no-diffusion variant. This suggests that delegating low-reward decision-making to the diffusion model helps smooth the learning signal and accelerates training.

:::: {#fig:training_curve .figure}
::: caption
Training curves for the high-level policy. HeRD converges substantially earlier than the no-diffusion variant, reflecting improved learning efficiency.
:::
::::

**Effect of reward structure.** We perform two ablations to evaluate how the reward function components contribute to performance. The first reverts our maximum-based progress reward (Eqn. [\[eqn:max_rew\]](#eqn:max_rew){reference-type="ref" reference="eqn:max_rew"}) back to the cumulative formulation (Eqn. [\[eqn:cum_rew\]](#eqn:cum_rew){reference-type="ref" reference="eqn:cum_rew"}). The second removes the step distance penalty (Eqn. [\[eqn:sdp\]](#eqn:sdp){reference-type="ref" reference="eqn:sdp"}) to assess its impact on efficiency and task success.

The results under the "Cumulative progress reward" column in Table [\[tab:ablation\]](#tab:ablation){reference-type="ref" reference="tab:ablation"} show a noticeable decline in efficiency and, in some environments, task success. This formulation encourages the robot to gather multiple boxes before pushing to maximize per-step reward. While this behaviour can be effective in isolated cases, it often leads to complex setup actions, including backward movement and detours. In constrained environments like *LargeDivider*, this results in longer paths and reduced robustness. By contrast, our maximum-based formulation reduces this bias and encourages steady, directed progress toward the goal, even when pushing a single box. This leads to more robust and efficient behaviour.

The results of the "No step distance penalty" experiment yield the most competitive metrics compared to ours. However, removing the penalty causes the success rate to suffer in the more complex environments. While the changes are subtle, the penalty appears to help discourage inefficient motion while retaining exploration.

## Real-World Experiments

We evaluate HeRD and a baseline model in a real-world setup to test the effectiveness of the policies in a physical environment. For the experiments, we used a TurtleBot3 Burger with a 3D printed bumper fixed to the front, and recreated the *SmallEmpty* environment in a lab. Using an overhead camera and visual markers, we obtain accurate pose estimations of the robot, boxes, receptacle, and environment boundaries, which we then use to construct the observations for the robot. Our setup is shown in Fig [1](#fig:physical){reference-type="ref" reference="fig:physical"}. From this, we test the policies trained in simulation. Given the generated observations, the policy generates a spatial goal that is then carried out on the robot using a low-level controller.

Each trial is run for $T_{\max} = 25$ minutes. We consider the number of boxes pushed into the receptacle in this time period as a proxy for our two-tiered objective of maximizing completed boxes and minimizing distance. We tested HeRD and the baseline for 5 trials each. Using the HeRD policy, the robot was able to push 8.0 out of 10 boxes on average into the receptacle in the given time limit, and only 3.2 boxes using the baseline policy.

A sim-to-real gap we noticed was the friction between the boxes and the environment walls. The robot struggled to overcome this force when many boxes were on the wall at once. This was very detrimental to the baseline policy, which relies heavily on gathering many boxes in a corner (sometimes up to seven) and pushing all of them against the wall towards the receptacle. In contrast, the HeRD policy acts more efficiently, opting to push one or two boxes in at a time if they are in accessible positions rather than pushing them backwards into a far corner.

# Conclusion

We introduce HeRD, a hierarchical architecture pairing high-level spatial goal selection with low-level diffusion trajectory generation. This decoupling enables efficient pushing in clutter, consistently outperforming the baseline [@wu_spatial_2020] in success and efficiency, particularly in constrained settings. By leveraging human priors for smooth navigation within a hierarchical framework, HeRD achieves robust generalization across diverse environments.

While currently limited to static 2D environments, HeRD's modular design naturally extends to dynamic settings. Future work will explore richer state representations, such as visual observations or expanded object contexts beyond the four nearest boxes, to better capture human priors and improve generalization in complex scenes.

[^1]: Resources used in preparing this research were provided, in part, by the Province of Ontario, the Government of Canada through CIFAR, and companies sponsoring the Vector Institute.

[^2]: The authors are with the Department of Electrical and Computer Engineering, University of Waterloo, Waterloo, ON N2L 3G1, Canada (e-mails:[{steven.caro, stephen.smith}@uwaterloo.ca]({steven.caro, stephen.smith}@uwaterloo.ca){.uri})
