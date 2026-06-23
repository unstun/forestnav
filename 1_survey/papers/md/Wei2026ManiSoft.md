---
citation_key: Wei2026ManiSoft
arxiv_id: 2605.18617
arxiv_url: https://arxiv.org/abs/2605.18617
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-23T17:54:54Z
origin: ai+web
reviewed: false
---

:::: strip
::: center
![image](Wei2026ManiSoft_figs/fig1.png){width="\\textwidth"} []{#fig:fig1 label="fig:fig1"}
:::
::::

# Introduction {#sec:intro}

Vision-language manipulation [@shao2025large] is a central capability of embodied AI, enabling language-conditioned interaction with the physical world. To date, most benchmarks [@liu2023liberobenchmarkingknowledgetransfer; @yu2021metaworldbenchmarkevaluationmultitask; @mees2022calvin; @li24simpler; @srivastava2021behavior] and methods [@chi2025diffusion; @liu2024rdt; @kim2024openvlaopensourcevisionlanguageactionmodel; @kim2025fine] focus on rigid robotic arms, where accurate proprioception and low-dimensional kinematics enable straightforward perception-to-control pipelines. However, rigid morphologies impose fundamental limitations in cluttered or confined environments [@chen2025survey]. As illustrated in [\[fig:fig1\]](#fig:fig1){reference-type="ref+Label" reference="fig:fig1"} (a), when obstacles require significant shape adaptation, a rigid arm may fail to reach the target due to its joint constraints.

Soft robotic arms [@e_soam; @armanini2023soft; @majidi2014soft; @hughes2016soft; @zhao2024exploring], built from elastic materials, offer an appealing alternative. Through continuous deformation, soft arms can adapt their geometry to execute policies infeasible for rigid arms. However, these advantages come with major challenges for vision-language manipulation. Unlike rigid arms with reliable joint sensing, soft arms often lack accurate proprioception [@pagliarani2025softtex], leading to highly complex kinematic control. Therefore, soft arms are typically actuated via low-level commands (e.g., pressures [@liu2025data], tendon tensions [@walker2024modular], or torques [@caasenbrood2022energy]) rather than intuitive kinematic targets. Moreover, distributed actuation along the body yields a higher-dimensional and more coupled action space than rigid arms. Together, these factors complicate the generation of stable and coordinated behaviors.

In this work, we introduce *ManiSoft*, a benchmark designed to catalyze vision-language manipulation research for soft arms. *ManiSoft* provides (i) a simulation and rendering stack for soft-arm manipulation, (ii) a suite of language-conditioned tasks with diverse scenes, and (iii) expert demonstration trajectories to support imitation and offline reinforcement learning. This design allows for evaluating existing policy models with minimal modifications, exposing failure modes unique to deformable embodiments.

A central technical challenge lies in simulation. While many soft-body simulators [@huang2021plasticinelab; @faure2012sofa] accurately capture elastic dynamics, they offer limited support for environmental interactions (e.g., contact and friction). In contrast, rigid-body simulators [@geng2025roboverseunifiedplatformdataset; @Xiang_2020_SAPIEN; @szot2021habitat] excel at modeling interactions but struggle with continuous deformation. To bridge this gap, we integrate a soft-body dynamics simulator [@elastica] with a rigid-body interaction simulator [@todorov2012mujoco] through an elastic force constraint, facilitating contact-rich manipulation with a soft arm. We further provide a Blender-based[^1] renderer for generating the visual observations used by policy models.

Built on this stack, *ManiSoft* defines four tasks as illustrated in [\[fig:fig1\]](#fig:fig1){reference-type="ref+Label" reference="fig:fig1"} (b). For each task, we follow the automated pipeline in [\[fig:fig1\]](#fig:fig1){reference-type="ref+Label" reference="fig:fig1"} (c) to generate tabletop scenes and expert trajectories. The asset library contains $263$ 3D objects, annotated with candidate manipulation poses. We first construct clean (uncluttered) scenes by sampling target objects from the asset library and then create randomized variants by adding obstacles and varying object placements and textures, enabling systematic evaluation under increasing visual and physical complexity.

For each scenario, we generate expert trajectories using a hierarchical mechanism. A high-level planner produces a sequence of waypoints, where each waypoint specifies a 6-DoF end-effector pose. A low-level controller outputs torque commands to drive the soft arm between successive waypoints. In our implementation, the high-level planner uses task-specific rules, and the low-level controller is a reinforcement learning (RL) [@sutton1988learning] policy. This decomposition mitigates the difficulty of directly producing torque sequences and yields stable trajectories for training.

Finally, we benchmark representative policy models on *ManiSoft*. As summarized in [\[fig:fig1\]](#fig:fig1){reference-type="ref+Label" reference="fig:fig1"} (d), existing models can solve a subset of tasks in clean scenes. However, performance drops substantially in randomized settings. Our visualizations and failure-case analysis suggest two bottlenecks: (i) estimating the soft arm's proprioceptive states from visual observations, and (ii) exploiting deformability to plan obstacle-avoiding interaction strategies. We hope *ManiSoft* will serve as a testbed for developing methods that address these challenges.

**Conflict of Interest Disclosure**. We declare that we have no relevant or material financial interests that relate to the research described in this paper.

# Related Works {#sec:related}

#### Robotic Manipulation Benchmarks.

Progress in vision-language manipulation has been accelerated by benchmarks that standardize tasks, observations, and evaluation protocols for comparing policy models [@shridhar2020alfred; @ahmed2020causalworld; @qi2020reverie]. RLBench [@james2020rlbench] provides a suite of $100$ vision-based manipulation tasks for evaluating both learning-based and traditional policy models. The ManiSkill series [@mu2021maniskill; @gu2023maniskill2; @taomaniskill3] emphasizes generalizable manipulation over diverse objects in a full-physics simulator. CALVIN [@mees2022calvin] targets long-horizon, language-conditioned manipulation, while LIBERO [@liu2023liberobenchmarkingknowledgetransfer] studies cross-task transfer in lifelong learning. RoboVerse [@geng2025roboverseunifiedplatformdataset] supports evaluation across multiple simulators and robot embodiments. RoboTwin [@mu2024robotwin; @chen2025robotwin] proposes an automated pipeline for generating diverse dual-arm manipulation scenarios at scale. Despite their breadth, these benchmarks predominantly target rigid arms with low-dimensional kinematics and reliable proprioception, leaving vision-language manipulation for deformable embodiments relatively underexplored. We fill this void by introducing a benchmark tailored to vision-language manipulation with soft arms.

#### Vision-Language-Action Models.

Vision-Language-Action (VLA) models have advanced rapidly in recent years. RT-1 [@brohan2023rt1roboticstransformerrealworld] and RT-2 [@brohan2023rt2visionlanguageactionmodelstransfer] demonstrate the effectiveness of large-scale training by leveraging multi-robot datasets. DexVLA [@wen2025dexvlavisionlanguagemodelplugin] extends this paradigm to enhance efficiency and generalization in long-horizon manipulation. RDT-1B [@liu2024rdt] introduces a diffusion-based foundation model for bimanual manipulation. OpenVLA [@kim2024openvlaopensourcevisionlanguageactionmodel] presents an open-source framework built upon large language models and pretrained visual encoders, while CogACT [@li2024cogactfoundationalvisionlanguageactionmodel] proposes an action module conditioned on VLM outputs to improve action prediction. More recently, the $\pi$ series [@black2024pi0visionlanguageactionflowmodel; @intelligence2025pi_; @intelligence2025pi] has demonstrated strong performance via large-scale pretraining followed by reinforcement learning. Despite this progress, prior VLA methods have been predominantly developed and evaluated on rigid arms. Our work provides a comprehensive benchmark and systematic evaluation of representative policy models on soft arms, highlighting unique challenges absent in rigid arms.

#### Soft Robotic Arms.

Over the past decade, soft arms have been widely studied and applied in domains such as biomedical engineering [@cianchetti2018biomedical; @rogatinsky2023multifunctional], aerospace [@ruiz2024thermally; @szasz2022modeling], and underwater exploration [@gong2021soft; @li2023bioinspired]. To address the challenges of modeling and control, learning-based approaches have been extensively explored. @thuruthel2017learning  applies trajectory optimization for open-loop predictive control, while @thuruthel2018model  extends this framework using model-based reinforcement learning for closed-loop control. @centurelli2022closed  develops a controller based on LSTM and TPRO for dynamic trajectory tracking, both with and without payloads. Soft DAgger [@nazeer2023soft] enables sample-efficient imitation learning for soft control. While these efforts advance low-level control of soft arms, high-level vision-language reasoning for manipulation remains largely unaddressed. Our work studies vision-language manipulation with soft arms, which requires jointly reasoning about visual perception, language understanding, environmental interaction, and deformable control.

# The *ManiSoft* Benchmark

We introduce the *ManiSoft* benchmark, designed to support vision-language manipulation with soft robotic arms. It comprises a soft-arm simulator, a collection of diverse tabletop scenes paired with language instructions, and expert demonstration trajectories. To enable scalable data collection, we propose an automated data generation pipeline that integrates procedural scene construction with a hierarchical expert trajectory generation mechanism.

## Simulator {#sec:SoftSim}

:::: {#fig:robot_sim .figure latex-placement="t"}
::: caption
**Overview of the soft arm modeling in our Simulator.** The soft body is modeled as a Cosserat rod that moves under the influence of an external torque $\boldsymbol{\tau}_e$. Interaction between soft body and EEF is represented via an an elastic force constraint. Relative displacement $\Delta \mathbf{x}$ or relative rotation $\Delta{\mathbf{\theta}}$ between them induces corresponding restoring forces and torques.
:::
::::

While existing soft-body simulators faithfully capture elastic deformation, they often provide limited support for interactions with rigid environments. Conversely, rigid-body simulators excel in modeling contacts and friction but lack native continuous deformation. To bridge this gap for soft robotic manipulation, we develop a hybrid simulator that combines accurate deformable dynamics with robust environmental interactions.

As illustrated in [1](#fig:robot_sim){reference-type="ref+Label" reference="fig:robot_sim"}, we model the soft arm as two coupled components: a deformable soft body and an end-effector. These components are linked via an elastic force constraint to ensure coordinated yet compliant motion.

The soft body is simulated using Elastica [@elastica], which discretizes the arm into $N$ segments following the Cosserat rod theory [@cosserat1909theorie]. External actuation torques $\boldsymbol{\tau}_e \in \mathbb{R}^{N \times 3}$ induce axial, shear, bending, and torsional strains along the rod, producing internal forces $\mathbf{f}_i \in \mathbb{R}^{N \times 3}$ and moments $\boldsymbol{\tau}_i \in \mathbb{R}^{N \times 3}$. These forces and torques govern the deformation together. [5](#sec:cosserat){reference-type="ref+Label" reference="sec:cosserat"} provides further details on Cosserat rod theory.

The end-effector and its interactions with the environment are handled by MuJoCo [@todorov2012mujoco], enabling efficient and stable simulation of contact-rich scenarios.

To couple the soft body and the end-effector, we impose an elastic force constraint. The two components are connected by a stretchable and twistable virtual spring with zero rest length. Relative translations $\Delta \mathbf{x} \in \mathbb{R}^3$ and rotations $\Delta \boldsymbol{\theta} \in \mathbb{R}^3$ between the attachment points generate restoring force $\mathbf{F} \in \mathbb{R}^3$ and torque $\mathbf{M} \in \mathbb{R}^3$, computed according to Hooke's law: $$\begin{equation}
  \mathbf{F} = -k_F \Delta \mathbf{x}, \quad \mathbf{M} = -k_M \Delta \boldsymbol{\theta},
\end{equation}$$ where $k_F, k_M \in \mathbb{R}$ are the translational and rotational stiffness coefficients, respectively. These restoring terms penalize relative motion between the soft body and the end-effector, driving the system toward coordinated motion.

We employ Blender to render the visual observations. Based on the simulated states, Blender produces RGB images of the tabletop scenes from fixed camera viewpoints, including the soft arm, target objects, and surrounding obstacles. Rendering parameters are detailed in [6](#sec:bench detail){reference-type="ref+Label" reference="sec:bench detail"}.

## Task Definition

As shown in [\[fig:fig1\]](#fig:fig1){reference-type="ref+Label" reference="fig:fig1"} (b), *ManiSoft* defines four manipulation tasks, each designed to highlight distinct challenges in vision-language manipulation for soft arms. Collecting (**COLL**) involves guiding the soft arm to gather a designated object and deposit it into a container, thereby evaluating fundamental trajectory control and basic end-effector coordination in policy models. Building on this foundation, Alignment (**ALN**) demands precise positioning of the target object to a specified 6-DoF pose, testing the model's capability for fine-grained orientation adjustments. Stacking (**STK**) escalates the challenge by requiring the arm to assemble tableware items from largest to smallest in a stable vertical pile, which assesses precision control during elevated, contact-rich interactions. Finally, Arrangement (**ARR**) requires placing objects according to a specified spatial configuration, thereby demanding integrated visual perception, spatial reasoning, and obstacle avoidance.

Formally, at each time step $t \in \mathbb{N}^+$, given an instruction $\mathbf{L}$ and the current visual observation $\mathbf{V}_t$, the policy model predicts the next action $\mathbf{A}_t = (\boldsymbol{\tau}_e, S)$. Here, $\boldsymbol{\tau}_e$ is the external torques and $S \in \{0, 1\}$ indicates the end-effector state. Upon execution, a new observation $\mathbf{V}_{t+1}$ is rendered, and the policy model proceeds autoregressively until task completion or the maximum horizon $T$ is reached.

Unlike rigid-arm benchmarks, which typically provide proprioceptive state (e.g., joint angles), *ManiSoft* deliberately excludes internal soft-body states to reflect real-world sensing limitations. Policy models must therefore infer the arm's configuration and deformation solely from visual observations, introducing significant challenges in proprioceptive state estimation and deformable strategy planning.

Two evaluation metrics are used: (i) success rate, determined by task-specific criteria, and (ii) efficiency, measured as the number of steps required for completion.

## Scene Generation

:::: {#fig:scene_gen .figure latex-placement="t"}
::: caption
**Scene generation in *ManiSoft*.** Objects are sampled from the asset library to create a clean scene, and randomized scenes are generated by injecting objects as obstacles and varying surface textures. Instructions are produced with the descriptions of relevant objects. In the randomized setting, diverse descriptions are leveraged to enhance the linguistic richness.
:::
::::

:::: {#fig:traj_gen .figure latex-placement="h!"}
::: caption
**Trajectory generation pipeline in *ManiSoft*.** (a) An executor is trained via RL policy to transform waypoint (6-DoF pose) into torques. (b) RL rewards are designed to balance accuracy and stability, consisting of a pose difference reward $R_d$ negatively correlated with the pose difference, and a stability reward $R_s$ that penalizes or rewards changes in pose difference. (c) Task-specific rules are predefined to produce high-level planning (trajectory waypoints) for each case, which are then converted into low-level actions (torque commands) by the executor to generate complete trajectories.
:::
::::

As depicted in [2](#fig:scene_gen){reference-type="ref+Label" reference="fig:scene_gen"}, *ManiSoft* adopts a tabletop environment as its core setting. The soft arm is fixed behind the table and centered relative to the workspace, allowing full access to objects distributed across the table surface. We build our object library by leveraging assets from RoboTwin-OD [@chen2025robotwin]. For each object, we pre-annotate a set of suitable 6-DoF end-effector poses for interaction with the soft arm (e.g., approach, grasp, and lift candidates). These annotations guide the high-level planner during expert trajectory generation. Scenes are procedurally generated by randomly sampling objects from this library and placing them within the workspace.

To support systematic evaluation, each task includes two difficulty levels: clean and randomized. In the clean setting, scenes contain only the task-relevant target objects in fixed layouts and appearances. In the randomized setting, we introduce additional irrelevant objects as obstacles to enhance spatial complexity, and apply scene randomization by sampling diverse textures along with variations in lighting intensity and brightness. This yields diverse spatial arrangements and visual appearances across episodes, stressing generalization in perception and planning.

Language instructions are generated in a controlled manner to ensure diversity, semantic accuracy, and consistency. Direct LLM sampling often produces variable phrasing or minor hallucinations; therefore, we first generate candidate instructions via GPT, manually curate and refine them into a template library, then instantiate templates by filling in object attributes (e.g., color, shape, material). In clean scenes, each object receives a single canonical description. In randomized scenes, objects are paired with multiple attribute-aware descriptions to reflect visual variability (e.g., a bottle may be referred to as "yellow bottle", "bottle with green cap", or "tall plastic bottle").

## Trajectory Generation. {#subsec: traj_gen}

:::: {#fig:data_statistic .figure latex-placement="t"}
::: caption
**Statistical analysis of the *ManiSoft* Benchmark.** (a) Distribution of trajectory lengths. Tasks in *ManiSoft* generally involve long trajectories, with the STK task exhibiting notably longer trajectories than the others. (b) Frequency distribution of target object categories, highlighting the diversity of manipulable objects in *ManiSoft*. (c) Spatial distribution of initial target object positions on the tabletop, showing that graspable targets are broadly and evenly distributed across the workspace.
:::
::::

Given the procedurally generated scenes for each task, we produce expert trajectories using a hierarchical mechanism, as illustrated in [3](#fig:traj_gen){reference-type="ref+Label" reference="fig:traj_gen"}. At the high level, a task-specific rule-based planner generates a sequence of waypoints, where each waypoint defines a desired 6-DoF end-effector pose in $SE(3)$. These waypoints encode semantically intermediate configurations (e.g., approach, grasp, retract) tailored to the task, avoiding the need for direct torque-sequence planning over long horizons.

At the low level, an RL-trained executor drives the soft arm from its current configuration to each successive waypoint using torque actuation. At each timestep $t$, the executor receives the following inputs: (i) the target end-effector pose $\hat{P} \in \mathrm{SE}(3)$, (ii) proprioceptive states including positions and velocities of selected segments along the arm, and (iii) the current end-effector pose $P \in \mathrm{SE}(3)$, and outputs torque commands.

The executor is trained with a dense reward function that encourages precise reaching of the target waypoint while promoting stable convergence and penalizing excessive deformation or oscillation. We measure the pose discrepancy using the standard $\mathrm{SE}(3)$ logarithm map: $$\begin{align}
    [\mathbf{d}_p, \mathbf{d}_r] = \log(P^{-1} \hat{P}), \quad d = \|\mathbf{d}_p\|_2 + \alpha \|\mathbf{d}_r\|_2,
\end{align}$$ where $\mathbf{d}_p, \mathbf{d}_r \in \mathbb{R}^3$ represent the position and axis-angle rotation differences, respectively. The scalar $\alpha > 0$ is tuned to balance the contributions of translation and rotation.

We define the total reward $R$ as the sum of two terms: a pose difference term $R_d$ and a stability term $R_s$. The pose difference reward $R_d$ is adapted from Elastica-RL-Control [@elastica], using the pose distance $d$ instead of Euclidean distance: $$\begin{equation}
    R_d = -d + k_1 \mathbbm{1}_{\{d < d_1\}} + k_2 \mathbbm{1}_{\{d < d_2\}}.
\end{equation}$$ The stability reward $R_s$ provides a signal based on the rate of change of $d$ when the end-effector is close to the target pose, encouraging smooth and stable convergence: $$\begin{equation}
    R_s =
    \begin{cases}
        -\operatorname{sgn}\!\left(\dfrac{\partial d}{\partial t}\right) \cdot \beta, & d \leq D, \\
        0, & d > D,
    \end{cases}
\end{equation}$$ where $\beta > 0$ is a scaling factor that controls the strength of the stability incentive.

Once trained, the executor is used to roll out complete trajectories by sequentially tracking the high-level waypoints. This hierarchical decomposition produces stable, collision-free demonstrations across a wide range of scenes. It significantly simplifies downstream policy learning compared to training directly on raw torque actions.

:::: {#fig:dicturbe .figure latex-placement="t"}
::: caption
**Visualization of executor trained w/ and w/o the stability reward $\mathbf{R_s}$.** (Left) The pose difference between the end-effector and the target pose over time. (Right) The soft robotic arm's trajectory shadows during the final $1000$ simulation steps. The red line represents the soft body, and the blue circle indicates the end-effector.
:::
::::

:::: {#fig:data_viusal .figure latex-placement="t"}
::: caption
**Visualization of the *ManiSoft*.** The left example is a clean scene, while the right is a randomized scene.
:::
::::

Empirically, the executor reaches a success rate of $54\%$ on $100$ random samples. We further investigate the effect of the stability reward $R_s$ on control stability. As shown in [5](#fig:dicturbe){reference-type="ref+Label" reference="fig:dicturbe"}, the model trained with $R_s$ exhibits noticeably smaller fluctuations in pose difference compared to the model trained without $R_s$. We also perform an ablation study on different parameter settings of $R_s$. The variance of the pose difference between the end-effector and the target is used to quantify control stability. Based on this metric, we select the best-performing set of parameters, $\beta=1,\ D=0.3$, as reported in [1](#tab:stable_reward){reference-type="ref+Label" reference="tab:stable_reward"}. Additional ablation studies are provided in [7](#sec:executor training){reference-type="ref+Label" reference="sec:executor training"}.

::: {#tab:stable_reward}
               0      0.5        1        1.5
  --------- ------- ------- ----------- -------
    0.05     0.176   0.157     0.074     0.121
     0.1     0.176   0.149     0.153     0.071
     0.2     0.176   0.070     0.135     0.064
     0.3     0.176   0.145   **0.053**   0.091
   Average   0.176   0.130     0.104     0.087

  : Control stability under different parameters of $R_s$. Specifically, $\beta = 0$ indicates the absence of $R_s$.
:::

## Data Statistic

*ManiSoft* contains 6,300 scene--trajectory pairs, comprising 2,100 clean scenes and 4,200 randomized scenes, with an average of 40 language instructions per scene. The dataset is split into training and testing sets with a ratio of $4:1$.

Owing to the high precision of torque-based control, trajectories in *ManiSoft* are relatively long, with an average length of 1,272 steps; the distribution of trajectory lengths is shown in [4](#fig:data_statistic){reference-type="ref+Label" reference="fig:data_statistic"} (a). *ManiSoft* features a rich variety of objects, including 109 manipulable objects across 17 categories, as illustrated in [4](#fig:data_statistic){reference-type="ref+Label" reference="fig:data_statistic"} (b), and 154 obstacles spanning 35 categories. [4](#fig:data_statistic){reference-type="ref+Label" reference="fig:data_statistic"} (c) visualizes the initial positions of target objects (i.e. grasp poses) across all scenes as a heatmap over the tabletop, demonstrating a wide distribution of grasp positions across the entire table.

Examples of the generated data are shown in [6](#fig:data_viusal){reference-type="ref+Label" reference="fig:data_viusal"}. More visualizations are provided in [10](#sec:more visualize){reference-type="ref+Label" reference="sec:more visualize"}.

::: table*
:::

# Experiments

We evaluate three representative models on *ManiSoft*: Diffusion Policy (DP) [@chi2025diffusion], RDT [@liu2024rdt], and OpenVLA-OFT [@kim2025fine]. DP and RDT are trained from scratch, while OpenVLA-OFT is fine-tuned with LoRA. Implementation details are provided in [8](#sec:implement details){reference-type="ref+Label" reference="sec:implement details"}.

## Main Results {#subsec: main res}

::: table*
:::

[\[tab:main\]](#tab:main){reference-type="ref+Label" reference="tab:main"} shows the performance of different models on each task under clean and randomized settings. Overall, DP and OpenVLA-OFT achieve substantially better performance than RDT. Specifically, DP attains an average success rate of $31.6\%$ with a mean execution length of $520$ steps, while OpenVLA-OFT achieves a comparable success rate of $30.4\%$ with an average of $527$ steps. In contrast, RDT performs significantly worse, with an average success rate of only $9.2\%$ despite requiring $496$ steps on average. This performance gap is likely attributable to differences in model capacity. RDT contains approximately $1$B parameters, whereas DP and OpenVLA-OFT each have around $400$M parameters. As a result, RDT is more prone to overfitting the training data, leading to inferior generalization on the testing set. Across all three models, the best performance is consistently observed on the COLL task, which requires less precise orientation perception and spatial reasoning compared to the other tasks.

Under the clean setting, DP achieves higher accuracy than OpenVLA-OFT on the COLL task, exceeding it by $17.6\%$. However, OpenVLA-OFT outperforms DP on all remaining tasks. Specifically, it achieves improvements of $6.7\%$, $5.0\%$, and $1.3\%$ on the ALN, STK, and ARR tasks, respectively. These results suggest that DP is more effective for simpler tasks, whereas OpenVLA-OFT exhibits stronger reasoning and generalization capabilities in more complex scenarios, likely benefiting from its pretrained weights.

Under the randomized setting, all models experience a decrease in success rate. Specifically, DP exhibits the largest performance drop, with its success rate decreasing by $29.4\%$, while RDT and OpenVLA-OFT show more moderate declines of $7.6\%$ and $3.4\%$, respectively. This indicates that the introduction of obstacles, together with variations in language instructions and scene configurations, substantially increases task difficulty. Notably, unlike in the clean setting, OpenVLA-OFT consistently outperforms DP under randomization, achieving an average improvement of $13.1\%$. This suggests that OpenVLA-OFT maintains stronger generalization performance in the presence of environmental and instruction-level variations.

[\[tab:arr\]](#tab:arr){reference-type="ref+Label" reference="tab:arr"} illustrates the performance across different object categories. The Rubik's Cube consistently yields the highest success rates among all objects. In the clean setting, its success rate exceeds that of the other categories by $5\%$-$30\%$ across methods. Notably, under the randomized setting, OpenVLA-OFT achieves a $15.0\%$ success rate on the Rubik's Cube, which is twice that of others. In contrast, the shoe is the most challenging object. In the clean setting, its success rate is $5\%$--$30\%$ lower than other categories across models. This gap becomes more pronounced under randomization, where success rates drop below $10\%$ for all methods. These results indicate that while object geometry strongly affects absolute task difficulty, different models exhibit consistent relative performance trends across object categories. More results are provided in [9](#sec:category results){reference-type="ref+Label" reference="sec:category results"}.

## Analysis {#subsec: findings}

[]{#sec: fingings label="sec: fingings"}

:::: {#fig:failure_case .figure latex-placement="t"}
::: caption
Visualization of typical failure cases of OpenVLA-OFT in *ManiSoft*. (a) The robot exhibits unexpected torsion and internal forces, resulting in inaccurate action prediction. (b) The robot fails to reach behind the obstacle.
:::
::::

:::: {#fig:dp_oft .figure latex-placement="t"}
::: caption
Comparison of DP and OpenVLA-OFT on the same task: (a) DP successfully completes the task; (b) OpenVLA-OFT exhibits the "stop-moving" behavior.
:::
::::

By visualizing rollouts from the evaluated policy models, we identify three failure modes.

#### Proprioceptive state ambiguity.

Reliable torque control depends on precise proprioceptive state estimation. Soft-arm deformation induces internal torques that must be actively compensated. Only the residual torque can drive the arm toward a desired pose. When the compensation term dominates, small state-estimation errors can overwhelm this residual, yielding unreliable control. As shown in [7](#fig:failure_case){reference-type="ref+Label" reference="fig:failure_case"} (a), the target object lies close to the arm base, requiring a large bend to reach it. This deformation induces substantial internal torques. The policy model fails to compensate for these loads, leaving insufficient residual control to stabilize the motion. Consequently, the end-effector drifts laterally and ultimately fails to reach the target object.

#### Challenges in leveraging soft arm compliance.

Compared to rigid arms, soft arms offer advantages in flexibility, allowing them to adapt their shape to the environment and reach behind obstacles. However, as illustrated in [7](#fig:failure_case){reference-type="ref+Label" reference="fig:failure_case"} (b), rather than adapting its shape to reach behind the obstacle, the policy model extends the soft arm directly toward the target object, resulting in collisions with the obstacle. This suggests that the policy model has not effectively utilized the soft-specific capabilities, such as shape adaptation and passive compliance. Increasing the proportion of obstacle-specific expert data or incorporating physical priors during training may help to mitigate this limitation.

#### Stop-Moving Behavior.

When comparing DP and OpenVLA-OFT, we observe that OpenVLA-OFT can exhibit a "stop-moving" behavior after grasp completion, where the robot remains stationary and fails to initiate subsequent actions. This behavior is likely caused by subtle visual changes during grasping, which induce a feedback loop that suppresses further action generation. As shown in [8](#fig:dp_oft){reference-type="ref+Label" reference="fig:dp_oft"}, OpenVLA-OFT often stops moving after a successful grasp, whereas DP rarely encounters this issue. This helps explain why OpenVLA-OFT achieves a lower success rate than DP on the simpler COLL task (45.4% vs. 63.0%) and requires longer execution lengths (565 vs. 547 steps, [\[tab:main\]](#tab:main){reference-type="ref+Label" reference="tab:main"}). Overall, this highlights a key distinction between diffusion-based and deterministic policies: the stochasticity in diffusion-based policies enables escaping such feedback loops, while deterministic policies are more prone to repetitive behavior.

# Conclusion {#conclusion .unnumbered}

We introduced *ManiSoft*, a benchmark for vision-language manipulation with soft arms. *ManiSoft* features a tailored simulator that couples soft-body dynamics with interactions via an elastic force constraint. Four tasks are designed to highlight distinct challenges in deformable control. An automated pipeline generates $6{,}300$ diverse scenes and corresponding expert trajectories. Quality of the trajectories is ensured through a hierarchical mechanism that combines waypoint decomposition with RL-based torque control. Benchmarking representative policy models shows relatively promising performance in clean scenes but marked degradation under randomization. Failures are primarily attributed to inaccurate visual estimation of proprioceptive state and under-exploitation of deformability.

# Limitations {#limitations .unnumbered}

This work represents an initial step toward benchmarking vision-language manipulation for soft robots. The current setup mainly focuses on a subset of actuation mechanisms and relatively simple tabletop scenarios, and does not yet cover more diverse actuation types or more dynamic, long-horizon tasks. In addition, sim-to-real consistency and physical validation could be further strengthened. These aspects leave room for future improvements in terms of coverage, realism, and evaluation diversity.

# Impact Statement {#impact-statement .unnumbered}

This work can support the development of safer and more human-friendly robotic systems. By providing a benchmark for vision-language manipulation with soft robots, ManiSoft may facilitate research on compliant interaction, with potential applications in service robotics and assistive or medical settings. Overall, it contributes toward more adaptable and accessible robotic technologies.

# Acknowledgements {#acknowledgements .unnumbered}

This research is supported in part by the Key Research Program of Hangzhou (No. 2025SZD1A56), the National Natural Science Foundation of China (No. 62461160308, U23B2010, 62576024), the Beijing Natural Science Foundation (No. L231011), the Fundamental Research Funds for the Central Universities (No. 501RCQD2025141003), BeiHang GanWei Project (No. 502GWXM2024141001), the National Science Foundation Support Projects (No. 62425303), and the National Key R&D Program of China (No. 2024YFb4707300).

# Supplementary Material {#supplementary-material .unnumbered}

# Cosserat Rod Theory {#sec:cosserat}

In Cosserat Rod Theory [@cosserat1909theorie], the elastic rod with $L_0$ and radius $r_0$ is presented as a Cosserat rod composed of $N$ discrete element rods, each of length $L_0/N$ and radius $r_0$. For each element rod, we describe its position in the global frame by $\bar {\mathbf{x}}(s,t) \in \mathbb{R}^3$, and its rotation in the global frame is represented by the rotation matrix $\mathbf{Q}(s,t) = \left\{\bar {\mathbf{d}}_1, \bar {\mathbf{d}}_2, \bar {\mathbf{d}}_3\right\}^{-1}$, where $\mathbf{Q}(s,t)$ also defines the transformation between the global and local frames. Specifically, for any vector $\mathbf{v}$ in the local frame and $\bar {\mathbf{v}}$ in the global frame, we have $\mathbf{v} = \mathbf{Q}\bar {\mathbf{v}}$ and $\bar {\mathbf{v}} = \mathbf{Q}^T\mathbf{v}$. Here, $s = L \cdot i / N$ denotes the position of the $i$-th element rod in the material coordinate, $t$ represents time, and $\delta s = L / N$ is the length of each element rod. As $N \to \infty$, $s$ becomes continuous, and $\delta s \to ds$. Subsequent derivations will be carried out in the continuous case.

The normal strain of the rod is described by the stretch factor $e = ds / d\hat s$, where $d \hat s = L_0 / N$, and $N \to \infty$ represents the original length of the element rod. The shear strain of the rod is described by the shear vector in the local frame, $\mathbf{\sigma} = \mathbf{Q}(\bar {\mathbf{x}}_s - \bar {\mathbf{d}}_3)$, where $\bar {\mathbf{x}}_s = \partial_s \bar {\mathbf{x}}$ is the centerline tangent in the global frame. At this point, we have the translational velocity $\bar {\mathbf{x}} = \partial_t \bar {\mathbf{x}}$ and the curvature vector $\mathbf{\kappa}$ satisfies $\partial_s \mathbf{d}_j = \mathbf{\kappa} \times \mathbf{d}_j$, which describes the rate of change of rotation along the material coordinate. The angular velocity $\mathbf{\omega}$ satisfies $\mathbf{\omega} = \partial_t \mathbf{d}_j = \mathbf{\omega} \times \mathbf{d}_j$, which describes the rate of change of rotation over time.

Given the bending $\mathbf{B}$ and shearing $\mathbf{S}$ stiffness matrices, the second area moment of inertia $\mathbf{I}$, the cross-sectional area $A$, and the mass per unit length $\rho$, the dynamics of the Cosserat rod can then be written based on the momentum and angular momentum theorems as follows: $$\begin{align}
    \rho A \cdot \partial_t \bar {\mathbf{v}} &= \partial_s \left(\frac{\mathbf{Q}^T\mathbf{S}\mathbf{\sigma}}{e}\right) + e \bar {\mathbf{f }}, \\
    \frac{\rho \mathbf{I}}{e}\cdot  \partial_t \mathbf{\omega} &= \partial_s \left(\frac{\mathbf{B} \mathbf{\kappa}}{e^3}\right) + \frac{\mathbf{\kappa} \times \mathbf{B}\mathbf{\kappa}}{e^3} + \left(\mathbf{Q} \frac{\bar {\mathbf{x}}_s}{e} \times \mathbf{S}\mathbf{\sigma}\right) \nonumber \\
    &+ \left(\rho \mathbf{I} \cdot  \frac{\mathbf{\omega}}{e}\right) \times \mathbf{\omega} + \frac{\rho \mathbf{I }\mathbf{\omega}}{e^2}\cdot \partial_t e+ e\boldsymbol{\tau}.
\end{align}$$ Where $\bar {\mathbf{f}}$ is the force density in the global frame for the Cosserat rod, and $\boldsymbol{\tau}$ is the torque density. In the discrete case, they represent the force and torque acting on each element rod. We propose a simulation framework for soft robotic arms that captures both their deformable dynamics and interactions with the environment. As shown in [1](#fig:robot_sim){reference-type="ref+Label" reference="fig:robot_sim"}, the arm is modeled as two coupled components: a deformable soft body and an end-effector, connected to allow coordinated motion.

::: {#tab:parameters}
  Parameter                      Value
  --------------------- -----------------------
  ***Simulator***       
  $k_F$                       $0.1\ N/m$
  $k_M$                   $10\ N\cdot m/rad$
  Simulation timestep         $0.0002\ s$
  Control Frequency            $714\ Hz$
  ***Soft Arm***        
  Length                        $1\ m$
  Radius                       $0.05\ m$
  Density                   $1000\ kg/m^3$
  Poisson's ratio                $0.5$
  Young's modulus        $1.0\ \times 10^7 Pa$
  ***Render***          
  Resolution               $514 \times 514$
  Camera Position           $(0,1.6,1.6)m$
  Camera FOV                     $60$

  : Key Parameters in the *ManiSoft* Simulator
:::

# Details for *ManiSoft* Benchmark {#sec:bench detail}

In the simulation, choosing appropriate values for $k_F$ and $k_M$ is crucial for maintaining both numerical stability and physical realism. If the coefficients are too small, positional and orientational discrepancies may persist, leading to separation between the components. On the other hand, excessively large coefficients can result in overcorrection, causing oscillations or even numerical instability. By carefully tuning the evolution of the elastic constraint, *ManiSoft*-Sim ensures stable, physically consistent coupling between the soft body and the EEF, enabling a coherent simulation of soft robotic manipulation.

Specifically, the parameters of the simulator used in our experiments are listed in the [2](#tab:parameters){reference-type="ref+Label" reference="tab:parameters"}.

In the *ManiSoft* benchmark, we set the maximum execution horizon to $T = 1500$ steps.

# Details for Executor Training {#sec:executor training}

For training the executor, we adopt an MLP-based policy network and employ SAC [@haarnoja2018soft], for reinforcement learning. We use a learning rate of $3 \times 10^{-4}$ and a batch size of $256$. The model is trained using a total of $160$M samples.

We perform training and evaluation with different parameters in the reward function.

First, we examine the success rate using a reward that includes only $R_d$ ($\beta = 0$) across various parameter settings. A case is deemed successful once the pose difference between the end-effector and the target drops below a predefined threshold. In Elastica-RL-Control [@elastica], the parameters are set as $k_1 = 0.5$, $k_2 = 1.5$, $d_1 = 0.1$, and $d_2 = 0.05$. We adopt the same values for $k_1$ and $k_2$. For $d_1$ and $d_2$, since we replace the original Euclidean distance with pose difference, the scale of $d$ changes. To maintain the original ratio between $d_1$ and $d_2$, we scale them proportionally, setting $d_1 = 0.1/\lambda$ and $d_2 = 0.05/\lambda$. The model is trained under different $\lambda$ and $\alpha$ configurations. For each setting, we train on $20$M samples. During evaluation, a case is considered successful if $d_p < 0.03$ and $d_r < 0.3$. We randomly sample 100 cases to evaluate the success rate, as summarized in Tab. [4](#tab: R_d){reference-type="ref" reference="tab: R_d"}. We found that despite changing $d$ from Euclidean distance to pose difference, the best performance was still achieved when $d_1$ and $d_2$ remained unchanged, *i.e.*, when $\lambda = 1$. With $\lambda$ fixed at $1$, we trained on $80$M samples with different $\alpha$ values, as shown in [\[tab:percentage_results_lambda1\]](#tab:percentage_results_lambda1){reference-type="ref+Label" reference="tab:percentage_results_lambda1"}. The best performance was achieved with $\alpha = 0.2$.

Based on the model with the highest success rate, we add $R_s$ and perform post-training on $80$M samples. We then compare the stability performance under different parameter settings, as shown in [1](#tab:stable_reward){reference-type="ref+Label" reference="tab:stable_reward"} of the main text.

Fig. [9](#fig: execute){reference-type="ref" reference="fig: execute"} shows the visualization of the trained executor controlling the soft robotic arm to move to the target pose.

# Implement Details for Baselines {#sec:implement details}

We train and evaluate the three baselines separately on each of the four tasks. All models are trained on 8 RTX 4090 GPUs.

## Clean Setting.

For the cleaning setting, we adopt the following training configuration.

#### DP [@chi2025diffusion].

We set the batch size to $64$ and the learning rate to $1\times10^{-4}$. The model is trained for $120,000$ iterations on the COLL task and $60,000$ iterations on each of the other three tasks, using a linear learning rate decay schedule. Since DP does not inherently support language understanding, we employ BERT as the text encoder. The resulting text embeddings are combined with image embeddings to guide action generation.

::: {#tab: R_d}
          0.4   0.6    0.8      1.0      1.2    1.4
  ------ ----- ------ ------ ---------- ------ ------
  0.02    6.0   6.0    3.0      6.0      5.0    5.0
  0.04    6.0   6.0    16.0     19.0     0.0    2.0
  0.05    2.0   2.0    11.0     8.0      11.0   4.0
  0.10    2.0   11.0   16.0     17.0     13.0   20.0
  0.15    3.0   4.0    8.0      19.0     9.0    16.0
  0.20    7.0   15.0   20.0     6.0      6.0    3.0
  Avg.    4.7   7.3    12.3   **12.5**   7.0    8.3

  : Success rate (%) on 100 samples under different parameters of $R_d$.
:::

[]{#tab: R_d label="tab: R_d"}

::: {#tab: R_d}
       $\alpha$       0.04   0.15     0.20     0.40     
  ------------------ ------ ------ ---------- ------ -- --
   Success Rate (%)   16.0   31.0   **33.0**   23.0     

  : Success rate on 100 samples under difference values of $\alpha$ with $\lambda=1$.
:::

[]{#tab: R_d label="tab: R_d"}

#### RDT [@liu2024rdt]

We use a batch size of $32$ and a learning rate of $1\times10^{-4}$, while keeping the text encoder and vision encoder frozen. The model is trained for $60,000$ iterations on the COLL task and $30,000$ iterations on the remaining tasks, with a cosine learning rate decay schedule.

#### OpenVLA-OFT [@kim2025fine].

We finetune the model using LoRA based on the official pretrained weights, with a batch size of $4$ and a learning rate of $5\times10^{-4}$. The model is trained for $60,000$ iterations on the COLL task and $30,000$ iterations on the other three tasks, following a cosine learning rate decay schedule.

## Randomized Setting.

For the randomized setting, we finetune the model initialized from the clean setting checkpoint, training for $20,000$ iterations on COLL and $10,000$ iterations on each of the other three tasks, while keeping all other training configurations unchanged.

# Results on Each Category {#sec:category results}

In COLL, ALN, and ARR, multiple categories of manipulable objects are included. Tab. [\[tab: coll\]](#tab: coll){reference-type="ref" reference="tab: coll"} and Tab. [\[tab: aln\]](#tab: aln){reference-type="ref" reference="tab: aln"} present the results for different categories of manipulable objects in COLL and ALN, respectively.

For the COLL task, DP outperforms both RDT and OpenVLA-OFT (by $17.6\%$ and $49.2\%$ respectively) in the clean setting, while in the randomized setting, OpenVLA-OFT performs better than DP by $28.9\%$. Regarding the number of inference steps, DP performs better than OpenVLA-OFT in both settings (by $18$ on clean and $80$ on randomized). This is due to the stop-moving phenomenon in OpenVLA-OFT, which leads to an increase in inference steps. Although RDT requires fewer inference steps, it completes fewer tasks overall, and the tasks it does complete are simpler, requiring fewer execution steps. This does not accurately reflect its overall performance.

The comparison of success rates across different objects reveals that, compared to the candle stick ($100\%$ success rate on DP) and the can ($85\%$), the shoe ($35\%$) and the sand clock ($35\%$) are more difficult to grasp. This is because they require a fixed grasping direction or have relatively large volumes.

A similar trend is observed in the ALN task, where OpenVLA-OFT achieves a higher success rate than DP (by $6.7\%$ on clean and $25\%$ on randomized), but requires more inference steps (by $30$ on clean and $65$ on randomized). In the clean setting, for the same object such as bottle, the success rate in the COLL task is higher than in the ALN task, indicating that the ALN task is relatively more challenging.

# More Visualizations {#sec:more visualize}

In Figure [10](#fig: COLL){reference-type="ref" reference="fig: COLL"}, Figure [11](#fig: ALN){reference-type="ref" reference="fig: ALN"}, Figure [12](#fig: STK){reference-type="ref" reference="fig: STK"} and Figure [13](#fig: ARR){reference-type="ref" reference="fig: ARR"}, we present more visualizations of the four tasks.

::: table*
[]{#tab: coll label="tab: coll"}
:::

::: table*
+------------------------------+----------------------------+--------------------+--------------------+--------------------+--------------------+
| Setting                      | Method                     | Bottle             | Shoe               | Candle Stick       | Average            |
+:=============================+:===========================+:========:+:=======:+:========:+:=======:+:========:+:=======:+:========:+:=======:+
| 3-4 (lr)5-6 (lr)7-8 (lr)9-10 |                            | ACC(%)   | #Steps  | ACC(%)   | #Steps  | ACC(%)   | #Steps  | ACC(%)   | #Steps  |
+------------------------------+----------------------------+----------+---------+----------+---------+----------+---------+----------+---------+
| Clean                        | DP [@chi2025diffusion]     | 5.0      | 391     | 5.0      | **519** | **45.0** | 417     | 18.3     | **442** |
|                              +----------------------------+----------+---------+----------+---------+----------+---------+----------+---------+
|                              | RDT [@liu2024rdt]          | 5.0      | 538     | 20.0     | 535     | 10.0     | **316** | 11.7     | 463     |
|                              +----------------------------+----------+---------+----------+---------+----------+---------+----------+---------+
|                              | OpenVLA-OFT [@kim2025fine] | **15.0** | **370** | **25.0** | 597     | 35.0     | 449     | **25.0** | 472     |
+------------------------------+----------------------------+----------+---------+----------+---------+----------+---------+----------+---------+
| Randomized                   | DP [@chi2025diffusion]     | 2.5      | **371** | 2.5      | **278** | 0.0      | \-      | 1.7      | **324** |
|                              +----------------------------+----------+---------+----------+---------+----------+---------+----------+---------+
|                              | RDT [@liu2024rdt]          | 0.0      | \-      | 7.5      | 498     | 5.0      | **260** | 4.2      | 379     |
|                              +----------------------------+----------+---------+----------+---------+----------+---------+----------+---------+
|                              | OpenVLA-OFT [@kim2025fine] | **5.0**  | 559     | **20.0** | 430     | **55.0** | 480     | **26.7** | 489     |
+------------------------------+----------------------------+----------+---------+----------+---------+----------+---------+----------+---------+

[]{#tab: aln label="tab: aln"}
:::

:::: {#fig: execute .figure latex-placement="h"}
::: caption
Visualization of the trained executor controlling the soft robotic arm to move to the target pose.
:::
::::

:::: {#fig: COLL .figure latex-placement="t"}
::: caption
**Visualization of COLL Task.** The first two are for the clean setting, and the last two are for the randomized setting.
:::
::::

:::: {#fig: ALN .figure latex-placement="t"}
::: caption
**Visualization of ALN Task.** The first two are for the clean setting, and the last two are for the randomized setting.
:::
::::

:::: {#fig: STK .figure latex-placement="t"}
::: caption
**Visualization of STK Task.** The first one is for the clean setting, and the last one is for the randomized setting.
:::
::::

:::: {#fig: ARR .figure latex-placement="t"}
::: caption
**Visualization of ARR Task.** The first two are for the clean setting, and the last two are for the randomized setting.
:::
::::

[^1]: <https://www.blender.org/>
