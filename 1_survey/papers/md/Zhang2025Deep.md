---
citation_key: Zhang2025Deep
arxiv_id: 2508.20884
arxiv_url: https://arxiv.org/abs/2508.20884
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-23T18:22:00Z
origin: ai+web
reviewed: false
---

# Introduction

Motion planning is a fundamental problem in robotics and autonomous systems, particularly in high-dimensional continuous spaces [@zhang2024review]. Traditional graph-based algorithms, such as Dijkstra's algorithm [@dijkstra1959note] and A\* [@hart1968formal], rely on discretized search spaces, making them computationally expensive and resolution-dependent. In contrast, sampling-based methods, such as Rapidly-exploring Random Trees (RRT) [@LaValle1998RRT] and Probabilistic Roadmaps (PRM) [@Kavraki1996PRM], achieve more efficient exploration. The improved variants, PRM\* and RRT\*, further guarantee asymptotic optimality [@Karaman2011RRTstar]. Informed RRT\* [@gammell2014informed] refines RRT\* by restricting sampling to an ellipsoid derived from the initial solution cost, accelerating convergence.

Several algorithms have extended these approaches. Fast Marching Tree (FMT\*) [@fmt2015] leverages batch processing for computational efficiency. Batch Informed Trees (BIT\*) [@gammell2020batch] balances exploration and optimization through incremental batch processing. Effort Informed Trees (EIT\*) [@strub2022adaptively] prioritizes regions with higher potential for path improvement, while Adaptively Informed Trees (AIT\*) [@strub2022adaptively] refines computational efficiency through heuristics. These methods have advanced sampling-based motion planning [@zhang25ral], making them widely applicable in navigation and bio-robotics.

To further improve planning efficiency, researchers have explored learning-based approaches [@ZHANG2025git]. Motion Planning Networks (MPNet) [@Qureshi2020MPNet] eliminate explicit trajectory optimization by directly mapping sensory inputs to motion sequences. Neural Exploration-Exploitation Trees (NEXT) [@chen2020learningplanhighdimensions] and Neural Informed RRT\* [@NeuralInformedRRT] integrate neural networks to guide sampling, reducing unnecessary exploration. Deep fuzzy methodologies have also been introduced to enhance adaptability. Wu et al. [@DeepFuzzyRobotSpeed] proposed a deep fuzzy framework that refines velocity commands through defuzzification.

:::: {#fig:framework .figure latex-placement="t!"}
::: caption
Overview of the deep-fuzzy motion planning framework. The environmental information in configuration space is encoded by global, local invalid ratio and Lebesgue measure of the informed set. A learning-based fuzzy rule is applied, followed by a defuzzification to get crisp batchsize $\mathcal{B}$ and the number of neighbors $\mathcal{K}$.
:::
::::

Recent work has focused on optimizing sampling strategies [@zhang2025TASE] and nearest neighbor optimization [@zhang2025apt]. Flexible Informed Trees (FIT\*) [@Zhang2024adaptive] dynamically adjust batch size to improve convergence, while Adaptive Prolated Trees (APT\*) [@zhang2025apt] employ prolated elliptical r-nearest neighbors to accelerate path search. However, these methods lack dynamic adaptation of batch size and neighbor selection [@Zhang2024Elliptical], potentially reducing accuracy and increasing search complexity. Moreover, reliance only on Coulomb's law limits their applicability.

Inspired by neural behavior, where the networks perceive a broader field of view in obstacle-sparse environments and navigate more directly, this work introduces Learning-Based Informed Trees (LIT\*). LIT\* integrates a deep fuzzy framework to address these challenges by leveraging invalid sampled states to encode environmental complexity and dynamically adjusting both sampling density and neighbor selection. By determining the number of sampled points and selected neighbors based on real-time conditions, LIT\* enhances both planning efficiency and path quality.

The main contributions of this work are:

- *A Fuzzy Reinforcement Learning Framework*: Encodes environmental complexity through *global invalid rate*, *local invalid rate*, and *the Lebesgue measure* of the informed set, enabling adaptive motion planning.

- *Learning-based batch size selection*: Dynamically adjusts batch size to balance exploration and exploitation.

- *Learning-based neighbor selection*: Replaces the fixed $k$-nearest neighbor approach (Fig. [2](#fig:compare){reference-type="ref" reference="fig:compare"}) with an adaptive strategy, improving sampling efficiency in both obstacle-dense and obstacle-sparse regions.

:::: {#fig:compare .figure latex-placement="t!"}
::: caption
Compare between with and without learning-based neighbor selection. These circles represent the minimum enclosing regions of selected neighbors at each step. Choosing $\mathcal{K}$ with a leaning-based method facilitates a more direct and cost-efficient path.
:::
::::

# Preliminaries and Problem formulation

This section introduces the background of neighbor search and deep fuzzy systems as preliminaries. It then formulates the problem in the deep fuzzy framework, explaining how it improves motion planning efficiency and solution quality.

## Preliminaries

### $R$-Nearest $\&$ K-Nearest Neighbors Search

The $r$-nearest neighbors search defines connectivity based on a fixed radius around each state. A state $q$ is connected to all other states within a radius $r(q)$, The $k$-nearest neighbors search method connects each state $q$ to its $k$ closest states regarding Euclidean distance. Their can be formulated as: $$\begin{equation}
\label{eqn: radius RNN}
    r(q) := \eta \left(2\left(1 + \frac{1}{n}\right){\left(\frac{\lambda(X_{\text{free}})}{\lambda\left(B_{1, n}\right)}\right) \left( \frac{\log(q)}{q}\right)}\right)^{\frac{1}{n}},
\end{equation}$$ where $\eta$ is a normalization constant, $n$ is the dimensionality of the space, $\lambda(\cdot)$ denotes the Lebesgue measure, $X_{\text{free}}$ is the free space, $B_{1,n}$ is the unit ball in $n$-dimensional space [@strub2022adaptively]. $$\begin{equation}
\label{eq: knn}
    k(q) := \eta e \left( 1 + \frac{1}{n} \right) \log(q),
\end{equation}$$ where $\eta$ is a tuning parameter, $e$ is the base of the natural logarithm, and $n$ denotes dimension [@andoni2009nearest].

### Deep Fuzzy Systems

Deep fuzzy systems combine fuzzy logic with learning methods. [@FuzzyMachineLearning]. A general deep fuzzy framework consists of three key components: *Fuzzification*: transforming raw input data into fuzzy membership values; *Fuzzy rules*: defines the relationships between fuzzy variables through a set of rules; and *Defuzzification*: applies fuzzy logic to derive crisp conclusions based on fuzzy rules.

::: algorithm
[]{#alg: g3t label="alg: g3t"}

$\textit{X}_{\textnormal{valid}} \gets \{\mathbf{x}_\textnormal{start}, \textit{}{X}_\textnormal{goal}\}$, $\mathbf{x}_{\textnormal{center,k}} \leftarrow \mathbf{x}_\textnormal{start}$, $\textit{X}_{\textnormal{invalid}} \gets \emptyset$, $E \mathcal \gets \emptyset$\
$\textit{X}_{\textnormal{valid}}, \textit{X}_{\textnormal{invalid}} \xleftarrow{+} \sample(\mathcal{B}_{\textnormal{init}} )$\
$\xi^{*}$
:::

::: algorithm
$X_{\smash{\textnormal{valid,r}}} \mathcal \gets \emptyset, X_{\smash{\textnormal{invalid,r}}} \mathcal \gets \emptyset, X_{\smash{\textnormal{center,b}}} \mathcal \gets \emptyset$\
$X_{\smash{\textnormal{center,b}}} \leftarrow \getStatesOnPath(\xi_{\textnormal{current}})$\
$r \leftarrow \caucLocalRadius()$\
$\rho_{\textnormal{local,B}} \leftarrow \rho_{\textnormal{local,B}} / |X_{\smash{\textnormal{center,b}}}|$\
$X_{\smash{\textnormal{valid,r}}}, X_{\smash{\textnormal{invalid,r}}} \leftarrow \getValidInvalid(\mathbf{x}_{\smash{\textnormal{center,k}}}, r)$\
$\rho_{\textnormal{local,K}} \leftarrow \ratioCalc(\textit{X}_{\textnormal{invalid,r}}, \textit{X}_{\textnormal{valid,r}})$\
$\rho_{\textnormal{local,B}}, \rho_{\textnormal{local,K}}$
:::

This work replaces the fuzzy rule component with a reinforcement learning algorithm, *Deterministic Policy Gradient (DDPG)* architecture, as illustrated in Fig. [1](#fig:framework){reference-type="ref" reference="fig:framework"}. It generates a deterministic policy as the fuzzy rule and facilitates seamless integration into subsequent planning stages.

## Problem Formulations

### Problem Formulation 1 (Optimal Planning)

We define the motion planning problem within the framework of sampling-based methods [@karaman2011sampling]. The state space is denoted as $X \subseteq \mathbb{R}^n$, where obstacle regions occupy $X_{\text{invalid}}$, the set of valid, collision-free states is defined as $X_{\text{valid}}$, and the goal states is $X_{\text{goal}} \subset X_{\text{valid}}$. The motion planning problem is defined to compute a path $\xi : [0,1] \to X_{\text{valid}}$ such that $\xi(0) = \mathbf{x}_{\text{init}}$ and $\xi(1) \in X_{\text{goal}}$. The optimal path denoted as $\xi^{*}$; $\Xi$ denotes the set of all nontrivial paths. The path planning problem can be described as: $$\begin{align*}
    & \xi^* = \arg \min_{\xi \in \Xi} c(\xi) \\
    \text{s.t.} \quad 
    & \xi(0) = \mathbf{x}_{\text{init}}, \xi(T) \in X_{\text{goal}}, \xi(t) \in X_{\text{valid}}(t), \forall t \in [0,1],
\end{align*}$$ where $c(\xi): \Xi \mapsto \mathbb{R}_{\geq 0}$ is the cost function of each feasible path, and the optimal cost is $c^*$.

### Problem Formulation 2 (Fuzzy-DDPG)

Beyond solving the motion planning problem, this work aims to improve the solution quality using the deep fuzzy framework, where reward functions $\mathcal{R}$ are designed to guide learning. During training, the objective is to maximize reward, ensuring efficient learning of key parameters.

The reinforcement learning observation $\textbf{s}_t$ is fuzzified global, local ratio and Lebesgue measure. Each state $\textbf{s}_t$ is associated with an action $\textbf{a}_t \in \mathbb{R}^3$. After defuzzification , a crisp number of batchsize $\mathcal{B} \in \mathbb{N}^{+} \cap [20, 200]$ and a factor of neighbor selection $\psi_{\mathcal{K}} \in \mathbb{R}^+ \cap [3.0, 15.0]$ will be applied in the following algorithm. The limits of batchsize are based on SOTA algorithms' upper and lower limits, while the factor's limits consider the connectivity.

The $\textit{Fuzzy-DDPG}$'s task is to determine an optimal policy $\bm{\pi}: \mathbb{S} \to \mathbb{A}$, where $\mathbb{S}$ is the state space, and $\mathbb{A}$ is the action space. The learned policy $\bm{\pi}$ aims to accelerate convergence and reduce solution cost, which are valued by the reward function $\mathcal{R}$. Formally, the problem can be described as: $$\begin{align*}
    & \mathop{\mathrm{arg\,max}}_{\bm{\pi}} \mathcal{R}  \\
    \text{s.t.} \quad 
    & \tilde{\mathcal{B}} = \bm{\pi}_{B}(\mathbf{s}_t ; \bm{W}_{B}), \tilde{\psi_{\mathcal{K}}} = \bm{\pi}_{K}(\mathbf{s}_t; \bm{W}_{K}),
\end{align*}$$ where $\bm{W}_{B}$ and $\bm{W}_{K}$ represent the parameters of the neural network trained via reinforcement learning.

:::: {#fig:actorcritic .figure latex-placement="t"}
::: caption
Illustration of the $\textit{Fuzzy-DDPG}$ architecture. The Actor and Critic net have the same structure of convolutional layers, flattened layers, and fully connected layers. The essential difference is the output generated by defuzzification.
:::
::::

# Learning-Based Informed Trees (LIT\*)

*Notation:* In the Fuzzy-DDPG framework, observation $\textbf{s}_t$ encodes the map information through a fuzzification process; action $\textbf{a}_t$ represents the membership values in the defuzzification phase; $\mathcal{E}$ denotes the set of factors involved in reward calculation. Each step of reward $r_t$ is calculated based on $\mathcal{E}$. The policy network (Actor) and the value network (Critic) are denoted as $\pi_{\theta}$ and $Q_{\phi}$, their loss is $\mathcal{L}_{\theta}$ and $\mathcal{L}_{\phi}$. To encode the map information, this work else takes invalid states $X_\textnormal{invalid}$ into account and defines the invalid ratio as: $$\begin{equation}
    \rho = \frac{|X_\textnormal{invalid}|}{|X_\textnormal{valid}| + |X_\textnormal{invalid}|},
    \label{eq:ratioDefinition}
\end{equation}$$ where the $|\cdot|$ denotes the size of corresponded set.

::: algorithm
Initialize $\pi_{\theta}$ , $Q_{\phi}$ , and $\mathcal{D}$\
$\pi_{\theta}$
:::

## Architecture of *Fuzzy-DDPG*

LIT\* deconstructs the solving process from a microscopic algorithmic perspective, simulating a network's field of view and autonomously selects optimal actions based on the current environment. Fig. [3](#fig:actorcritic){reference-type="ref" reference="fig:actorcritic"} illustrates the architecture of *Fuzzy-DDPG*. The process begins with fuzzifying three inputs, *Fuzzy-DDPG* then iteratively trains the Actor and Critic. Finally, leveraging the trained Actor, the system computes membership degrees and applies defuzzification to generate a continuous action based on the learned policy. Specificlly, for B-Net the defuzzied $z^*$ is batchsize $\mathcal{B}$ and for K-net the $z^*$ is $\psi_{\mathcal{K}}$, and $\mathcal{K}$ is calculated as: $$\begin{equation}
\label{eq:newknn}
    k(q) := \eta e \cdot \psi_\mathcal{K} \cdot \left( 1 + \frac{1}{n} \right) \log(q),
\end{equation}$$

:::: {#fig: simulation .figure latex-placement="t!"}
::: caption
Illustrates the narrow passage (a) and random rectangles (b) tests in Planner Developer Tools (PDT) [@gammell2022planner]. Fig. (c) and (d) illustrate the dual-Barrett Whole-Arm Manipulator-$\mathbb{R}^{14}$ in the Open Robotics Automation Virtual Environment (OpenRAVE) [@Diankov2008OpenRAVEAP]. (c) shows the start configuration as it picks up objects from the bottom, (d) illustrates the goal configuration where the object is placed on the top shelf.
:::
::::

:::: {#fig:tensor .figure latex-placement="t!"}
:::: {#fig:compare1 .figure}
::: caption
Trained Tensor of $\mathcal{K}$
:::
::::

:::: {#fig:compare2 .figure}
::: caption
Trained Tensor of $\mathcal{B}$
:::
::::

::: caption
Visulization of the $\mathcal{K}$-tensor and $\mathcal{B}$-tensor The three axes of the tensor represent the global invalid ratio, the local invalid ratio, and the Lebesgue measure of the informed set. Each pair of these coordinates uniquely determines a specific value of $\mathcal{K}$ or $\mathcal{B}$.
:::
::::

### Inputs Fuzzification

This work extracts three key parameters to encode the map: $\rho_{\textnormal{global}}$, $\rho_{\textnormal{local}}$, and $\lambda(X_{\hat{f}})$. To further enhance the expressiveness of the input representation, this work fuzzifies these inputs into the *DDPG* neural network to improve its feature representation capability.

This work selects three fuzzy sets and Gaussian membership functions to balance expressiveness and computational complexity. For each input in $\mathcal{O} = \{ \rho_{\text{global}}, \rho_{\text{local}}, \lambda(X_{\hat{f}}) \}$, this study employs fuzzy sets for modeling and designs three fuzzy sets to describe their characteristics: *S* (sparse), *M* (medium), and *D* (dense).

$$\begin{equation}
    \mu_{\mathcal{O},i}(\rho_{\text{global}}) = \exp\left(-\frac{(\rho_{\text{global}} - \vartheta_{\text{global},i})^2}{2\sigma_{\text{global},i}^2}\right),
\end{equation}$$

Correspondingly, each element in $\mathcal{O}$ has three membership functions ($i, j, k \in \{1,2,3\}$), corresponding to different levels of its fuzzy feature. The parameters $\vartheta_{|\cdot|}$ and $\sigma_{|\cdot|}$ control the shape and position of each membership function. Then, the final fuzzy mapping can be represented as a $9 \times 1$ vector: $$\begin{equation}
\bm{i} = [\mu_{\mathcal{O}_{1},1}(x_{1}), \mu_{\mathcal{O}_{1},2}(x_{1}), ... , \mu_{\mathcal{O}_{3},3}(x_{3})]^T,
\label{input}
\end{equation}$$ where $x_1, x_2, x_3$ correspond to the three components of the input $\mathcal{O}$. This fuzzy logic mapping transforms the original input data into a continuously fuzzy representation, making it more effectively processable by the neural network.

### Actor and Critic

In *Fuzzy-DDPG*, there are two primary networks: the Actor $A_{\theta}(\mathbf{s})$ and the Critic $Q_{\phi}(\mathbf{s, a})$. The Actor network takes a 9-dimensional input and passes it through a convolutional layer with kernel sizes 3, 5 and 7, and outputs 9 channels, followed by a fully connected multi-layer perceptron (MLP). The MLP consists of five hidden layers with neuron sizes (64, 128, 128, 64, 32) activated by ReLU. The final output layer has 3 neurons, corresponding to the number of defuzzification-membership functions, and applies a TSK defuzzification [@softmaxNeuralNetwork] for discrete and continuous actions. The Critic network follows a similar architecture but takes the concatenation of state $\textbf{s}$ and defuzed-result as input. The output layer is a single neuron representing the estimated Q-value of current ($\textbf{s}$, $\textbf{a}$) pair.

### Defuzzification

This work select the Takagi-Sugeno-Kang (TSK) defuzzification [@TSKDefuzzy] method due to its effectiveness in modeling complex nonlinear systems and its widespread use in control and decision-making applications. It employs a weighted sum approach, allowing a smooth transition between rules and enabling more adaptive decision-making. Specifically, the defuzzified output is computed as:

$$\begin{equation}
    z^* = \frac{\sum_{i=1}^{N} w_i f_i}{\sum_{i=1}^{N} w_i},
\end{equation}$$

where $w_i$ represents the weight of the $i$-th fuzzy rule, and $f_i$ is a constant functions to control the output range.

## Training of Fuzzy-DDPG

Deep Deterministic Policy Gradient (DDPG) is an actor-critic reinforcement learning algorithm designed for continuous control problems. The key feature of DDPG is its ability to optimize policies over a continuous action space by leveraging an off-policy training framework with target networks and soft updates.

The Bellman equation for the critic network is defined as: $$\begin{equation}
    Q_{\phi}(\mathbf{s}_t, \mathbf{a}_t) = r_t + \gamma Q_{\phi'}(\mathbf{s}_{t+1}, A_{\theta'}(\mathbf{s}_{t+1})),
\end{equation}$$ where: $r_t$ is the reward at time step $t$, $Q_{\phi'}$ and $A_{\theta'}$ are the target networks for the critic and actor, respectively, $\gamma \in [0,1]$ is the discount factor.

:::: {#fig: result .figure latex-placement="t!"}
::: caption
Detailed experimental results from Section [4](#sec:experi){reference-type="ref" reference="sec:experi"} are presented above. Fig. (a), (b), and (c) depict test benchmark random rectangle outcomes in $\mathbb{R}^4$, $\mathbb{R}^8$ and $\mathbb{R}^{16}$, respectively. Panel (d) showcases ten narrow passage experiments in $\mathbb{R}^4$, while panels (e) and (f) demonstrate in $\mathbb{R}^8$ and $\mathbb{R}^{16}$. In the cost plots, boxes represent solution cost and time, with lines showing cost progression for planners (unsuccessful runs have infinite costs). Error bars provide nonparametric 99% confidence intervals for solution cost and time.
:::
::::

### Reward Definition

This work defines different reward functions for two sub-networks: BatchSize-Net (B-Net) and NearestK-Net (K-Net) as in Fig. [1](#fig:framework){reference-type="ref" reference="fig:framework"}. Processing more information each step in an obstacle-free space can lead to more direct solutions and increase computational effort. Therefore, the reward function must account for key parameters to balance efficiency and solution quality.

#### BatchSize-Net Reward

The reward function for B-Net is defined as: $$\begin{equation}
\mathcal{R}_{B} = \alpha_B \cdot \frac{\kappa}{t} + \beta_B \cdot \frac{\kappa}{c(\xi)} -\gamma_B \cdot n_{\text{update}},
\label{rewardB}
\end{equation}$$ where: $\alpha_B$, $\beta_B$, and $\gamma_B$ are scaling factors to ensure that the corresponding terms remain within a reasonable range, preventing them from becoming excessively large or small; t denoted the time cost for each solution update; $n_{\text{update}}$ represents the number of solution updates, $\gamma_B$ is a scale parameter for $n_{\text{update}}$, $\kappa$ is a decay function about $n_{\text{update}}$, which is given by: $$\kappa(n_{\text{update}}) = \max \left( \nu_{\min}, \nu \cdot \log_2 (6.8 - n_{\text{update}}) \right).$$

This reward function encourages rapid convergence by assigning high rewards in early updates if a solution is found quickly and high rewards in later updates if a more stable, faster-converging solution is achieved.

#### K-Net Reward

The reward function for NearestK-Net is defined as: $$\begin{equation}
\mathcal{R}_{K} = \alpha_K \cdot \frac{1}{t} + \beta_K \cdot \frac{1}{c(\xi)} +\gamma_K \cdot \#\xi,
\label{rewardK}
\end{equation}$$ specially, $\#\xi$ denotes the number of states in a solution path. Since neighbor selection influences path efficiency, this function encourages more direct paths with fewer intermediate states, leading to higher efficiency and better trajectory planning. This work also incorporates Prioritized Experience Replay (PER) [@schaul2016prioritizedexperiencereplay] to address the sparse rewards problem.

### Actor and Critic Network Training

The objective of the actor network is to maximize the expected Q-value: $$\begin{equation}
\bm{W}_{\theta}^{*} =\mathop{\mathrm{arg\,max}}_{\bm{W}_{\theta}} \mathbb{E} \left[ Q_{\phi}(\mathbf{s}, A_{\theta}(\mathbf{s})) \right].
\label{actor_loss_expectation}
\end{equation}$$ This is transformed into a loss function for training: $$\begin{equation}
\mathcal{L}(\bm{W}_{\theta}) = -\frac{1}{m} \sum_{t} Q_{\phi}(\mathbf{s}, A_{\theta}(\mathbf{s}; \bm{W}_{\theta})).
\label{actorloss}
\end{equation}$$ where: $\bm{W}_{\theta}$ represents the actor network parameters, $m$ is the batch size used during training.

For the critic network, the goal is to minimize the Temporal Difference (TD) error: $$\begin{equation}
\mathcal{L}(\bm{W}_{\phi}^{*}) = \mathop{\mathrm{arg\,min}}_{\bm{W}_{\phi}} \mathbb{E} \left[ \delta^2 \right] 
\label{Critic_loss}
\end{equation}$$ where $\delta = Q_{\phi'}(\mathbf{s}, \mathbf{a}) - Q_{\phi}(\mathbf{s}, \mathbf{a})$ is the TD error.

For mini-batch training, the loss function becomes: $$\begin{equation}
\mathcal{L}(\bm{W}_{\theta}) = -\frac{1}{m} \sum_{t} Q_{\phi}(s_t, A_{\theta}(s_t; \bm{W}_{\theta})).
\label{criticloss}
\end{equation}$$

### Network Update

To stabilize training, soft updates are applied to the target networks: $$\begin{align}
    \bm{W}_{\phi}^{'} &\gets \tau \bm{W}_{\theta} + (1 - \tau) \bm{W}_{\phi}^{'}, \\
    \bm{W}_{\phi}^{'} &\gets \tau \bm{W}_{\phi} + (1 - \tau) \bm{W}_{\phi}^{'},
\end{align}$$ where $\bm{W}_{\theta}^{'}$ and $\bm{W}_{\phi}^{'}$ are target network parameters, $\tau \ll 1$ is a small update factor ensuring stability.

This gradual update strategy prevents sudden oscillations in policy updates and improves learning efficiency.

Given that the *Fuzzy-DDPG*'s output is deterministic, this study pre-maps the neural network outputs into a tensor (Fig. [7](#fig:tensor){reference-type="ref" reference="fig:tensor"}), where the three tensor dimensions correspond to the three input variables. Each unique three-dimensional coordinate directly determines a specific output value. In C++, querying this tensor has a time complexity of $\bm{O}(1)$, achieving microsecond-level access speed.

The overall process is as follows: during sampling and neighbor node expansion, the current map information is retrieved; based on this information, a lookup is performed in the tensor; the corresponding action is obtained, and the path planning algorithm continues execution.

# Experimental Results {#sec:experi}

LIT\* was evaluated against several existing algorithms, including different versions of RRT-Connect, Informed RRT\*, BIT\*, AIT\*, EIT\*, and FIT\* from the Open Motion Planning Library (OMPL) [@sucan2012open]. Tests were conducted in simulated environments ranging from $\mathbb{R}^4$ to $\mathbb{R}^{16}$ and simulation manipulation scenarios using an Intel i7 3.90 GHz processor with 32GB of LPDDR3 4800 MHz memory. The main goal was to minimize the median initial path length ($c^\textit{med}_\textit{init}$) over 100 runs. For all planners, the RGG constant $\eta$ was set to 1.1, and the rewire factor to 1.001. RRT-based algorithms used a 5% goal bias, with maximum edge lengths adjusted for space dimensionality. This work also tests the algorithm in the Open Robotics Automation Virtual Environment (OpenRAVE [@Diankov2008OpenRAVEAP], Fig. [4](#fig: simulation){reference-type="ref" reference="fig: simulation"} (c) and (d)) by a dual-Barrett Whole-Arm Manipulator (dual-WAM-$\mathbb{R}^{14}$). The learning-based mechanism optimizes the convergence speed and solution quality.

[]{#tab:benchmark label="tab:benchmark"}

As observed in Table [\[tab:benchmark\]](#tab:benchmark){reference-type="ref" reference="tab:benchmark"}, there's a median cost improvement across varied benchmark scenarios, correlating with dimensionality. In the case of the NP-$\mathbb{R}^{16}$ scenario, the initial median solution cost exhibits a reduction of up to 31.59%.

# Discussion & Conclusion

This paper introduces Learning-based Informed Trees (LIT\*), a planner using *Fuzzy-DDPG* to determine batchsize and nearest neighbors. It also encodes the invalid states as input of the *Fuzzy-DDPG* framework, thereby self-adjusting according to the valid/invalid ratio. Since multiple neighbor expansion steps occur in each epoch, and the motion planning algorithm is implemented in C++ while Fuzzy-DDPG runs in Python, the communication between the two can be significant. This work facilitates data exchange by a shared file, which may introduce latency. Future work could focus on improving communication efficiency to reduce training time. LIT\* demonstrated its adaptability by achieving short path lengths and quickly generating solutions.

In conclusion, LIT\* leverages valid and invalid states to dynamically determine batchsize and the number of neighbors, ensuring adaptive and efficient motion planning.

[^1]: $^{1}$L. Zhang, Q. Zong, Y, Zhang, Z. Bing, and A. Knoll are with the School of Computation, Information and Technology (CIT), Technical University of Munich, 80333 Munich, Germany. `liding.zhang@tum.de`

[^2]: $^{2}$Z. Bing is also with the State Key Laboratory for Novel Software Technology and the School of Science and Technology, Nanjing University (Suzhou Campus), China. *(Corresponding author: Zhenshan Bing.)*

[^3]: $^{\dagger}$The authors acknowledge the financial support by the Bavarian State Ministry for Economic Affairs, Regional Development and Energy (StMWi) for the Lighthouse Initiative KI.FABRIK (Phase 1: Infrastructure and the research and development program under grant no. DIK0249).
