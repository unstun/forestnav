---
citation_key: Zhang2023MultiModal
arxiv_id: 2312.02328
arxiv_url: https://arxiv.org/abs/2312.02328
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-24T16:14:09Z
origin: ai+web
reviewed: false
---

Zhang *et al.*: Multi-Modal MPPI and Active Inference for Reactive Task and Motion Planning

::: IEEEkeywords
Task and Motion Planning, Manipulation Planning
:::

# Introduction {#sec:intro}

and Motion Planning (TAMP) is a powerful class of methods for solving complex long-term manipulation problems where logic and geometric variables influence each other. TAMP [@garrett2021integrated; @toussaint2015logic; @garrett2020pddlstream] has been successfully applied to domains such as table rearrangement, stacking blocks, or solving the Hanoi tower. [However, the plan is often executed in open-loop in static environments.]{style="color: blue"} Recent works [@toussaint2022sequence; @migimatsu2020object; @li2021reactive] recognized the importance of robustifying the execution of TAMP plans to be able to carry them out in the real world reliably. But they either rely only on the adaptation of the action sequence in a plan [@pezzato2022aipbt; @castaman2021receding; @Colledanchise2019; @li2021reactive] or only on the motion planning problem in a dynamic environment given a fixed plan [@toussaint2022sequence; @migimatsu2020object]. [Unlike typical TAMP planners that focus on solving static and complex tasks offline and then execute the solution, this paper aims to achieve reactive execution by simultaneously adapting high-level actions and low-level motions]{style="color: blue"}.

[Reactive TAMP faces the challenge of accommodating unforeseen geometric constraints during planning, such as the need to pull rather than push a block when it's in a corner, complicating high-level planning without complete scene knowledge. Additionally, scenarios like pick-and-place tasks with dynamic obstacles and human disturbances demand varied grasping poses for different objects and obstacles, requiring TAMP algorithms to adapt to such configurations dynamically.]{style="color: blue"}

We address these challenges by proposing a control scheme that jointly achieves reactive action selection and robust low-level motion planning during execution. We propose a high-level planner capable of providing alternative actions to achieve a goal. These actions are translated to different cost functions for our new Multi-Modal Model Predictive Path Integral controller for motion planning. [This]{style="color: black"} motion planner leverages a physics simulator to sample parallel motion plans that minimize the given costs and computes one coherent control input that effectively blends different strategies. To achieve this, we build upon two of our recent works: 1) an Active Inference planner (AIP) [@pezzato2022aipbt] for symbolic action selection, and 2) a Model Predictive Path Integral (MPPI) controller [@pezzato2023sampling] for motion planning. [The AIP computes a sequence of actions and state transitions through backchaining to achieve a sub-goal specified in a given Behavior Tree (BT). The BT guides the search and allows real-time high-level planning within the AIP framework [@pezzato2022aipbt]. In this work,]{style="color: blue"} we extend the previous AIP to plan possible alternative [action]{style="color: blue"} plans, and we propose a new Multi-Modal Model Predictive Path Integral controller (M3P2I) that can sample in parallel these alternatives and smoothly blend them [considering the geometric constraints of the problem]{style="color: blue"}.

## Related work

[To robustly operate in dynamic environments, reactive motion planners are necessary.]{style="color: black"} In [@toussaint2022sequence], the authors provided a reactive Model Predictive Control (MPC) strategy to execute a TAMP plan as a given linear sequence of constraints. The reactive nature of the approach allows coping with disturbances and dynamic collision avoidance during the execution of a TAMP plan. Authors in [@migimatsu2020object] formulated a TAMP plan in object-centric Cartesian coordinates, showing how this allows coping with perturbations such as moving a target location. However, both [@toussaint2022sequence; @migimatsu2020object] do not consider adaptation at the symbolic action level if a perturbation invalidates the current plan.

Several papers focused on adapting and repairing high-level action sequences during execution. In [@Paxton2019], robot task plans are represented as robust logical-dynamical systems to handle human disturbances. Similarly, [@harris2022fc] coordinates control chains for robust plan execution through plan switching and controller selection. A recent paper [@huang2022parallel] suggests employing Monte Carlo Tree Search with IsaacGym to accelerate task planning for multi-step object retrieval from clutter involving intricate physical interactions. While promising, [@huang2022parallel] only supports high-level reasoning with predefined motions in an open loop. Recent works [@zhou22; @li2021reactive] combined BTs and linear temporal logic to adapt the high-level plan to cope with cooperative or adversarial human operators, environmental changes, or failures. In our previous work [@pezzato2022aipbt], AIP and BT were combined to provide reactive action selection in long-term tasks in partially observable and dynamic environments. This method achieved hierarchical deliberation and continual online planning, making it particularly appealing for the problem of reactive TAMP at hand. In this paper, we extend [@pezzato2022aipbt] by bridging the gap to low-level reactive control by planning cost functions instead of symbolic actions.

At the lower level, MPC is a widely used approach [@bangura2014real; @scianca2020mpc; @spahn2021coupled]. However, manipulation tasks often involve discontinuous contacts that are hard to differentiate. Sampling-based MPCs, such as MPPI [@williams2017information; @bhardwaj2022storm], can handle non-linearities, non-convexities, or discontinuities of the dynamics and costs. MPPI relies on sampling control input sequences and forward system dynamics simulation. The resulting trajectories are weighted according to their cost to approximate an optimal control input. In [@abraham2020model], the authors proposed an ensemble MPPI to cope with model parameters uncertainty. Sampling-based MPCs are generally applied for single-skill execution, such as pushing or reaching a target point. As pointed out in the future work of [@howell2022predictive], one could use a high-level agent to set the cost functions for the sampling-based MPC for long-horizon cognitive tasks. We follow this line of thought and propose a method to reactively compose cost functions for long-horizon tasks. Moreover, classical MPPI approaches can only keep track of one cost function at a time. This means the task planner should propose a single plan to solve the task. However, some tasks might present geometric ambiguities for which multiple plans could be effective, and selecting what strategy to pursue can only be determined by the motion planner based on the geometry of the problem.

## Contributions

The main contribution of this work is a reactive task and motion planning algorithm based on the following:

- A new Multi-Modal MPPI (M3P2I) capable of sampling in parallel plan alternatives to achieve a goal, evaluating them against different costs. This enables the smooth blending of alternative solutions into a coherent behavior instead of switching based on heuristics.

- An enhanced Active Inference planner (AIP) capable of generating alternative cost functions for M3P2I.

We demonstrate the method in several scenarios in simulations and real robots for pushing, pulling, picking, and placing objects under disturbances.

# Background {#sec:background}

In this section, we present the background knowledge about the Active Inference planner and Model Predictive Path Integral Control to understand the contributions of this paper. We refer the interested reader to the original articles [@pezzato2022aipbt; @williams_model_2017; @williams_information-theoretic_2018] for a more in-depth understanding of the techniques.

## Active Inference Planner (AIP)

AIP is a high-level decision-making algorithm that relies on symbolic states, observations, and actions [@pezzato2022aipbt]. Each independent set of states in AIP is a factor, and the planner contains a total of $n_f$ factors. For a generic factor $f_j$ where $j\in\mathcal{J} = \{1,...,n_f\}$, it holds: $$\begin{gather}
    \nonumber
    s^{(f_j)} = \left[s^{(f_j,1)}, s^{(f_j,2)},...,s^{(f_j,m^{(f_j)})}\right]^\top,\\ 
    \mathcal{S} = \big\{ s^{(f_j)}|j\in\mathcal{J}\big\}
\end{gather}$$ where $m^{(f_j)}$ is the number of mutually exclusive symbolic values a state factor can have, each entry of $s^{(f_j)}$ is a real value between 0 and 1, and the sum of the entries is 1. This represents the current belief state.

The continuous state of the world $x\in\mathcal{X}$ is discretized through a symbolic observer such that the AIP can use it. Discretized observations $o$ are used to build a probabilistic belief about the symbolic current state. Assuming one set of observations per state factor with $r^{(f_j)}$ possible values: $$\begin{gather}
    \nonumber
    o^{(f_j)} = \left[o^{(f_j,1)}, o^{(f_j,2)},...,o^{(f_j,r^{(f_j)})}\right]^\top,\\ 
    \mathcal{O} = \big\{ o^{(f_j)}|j\in\mathcal{J}\big\}
\end{gather}$$

The robot has a set of symbolic actions that can act then their corresponding state factor: $$\begin{gather}
    \nonumber
    a_\tau \in \alpha^{(f_j)} = \big\{a^{(f_j,1)}, a^{(f_j,2)},...,a^{(f_j,k^{(f_j)})}\big\},\\ 
    \mathcal{A} = \big\{ \alpha^{(f_j)}|j\in\mathcal{J}\big\}
\end{gather}$$ where $k^{(f_j)}$ is the number of actions that can affect a specific state factor $f_j$. Each generic action $a^{(f_j,\cdot)}$ has associated a symbolic name, *parameters*, *pre-* and *postconditions*:

  ------------------------------ ---------------------------- ----------------------------
  **Action** $a^{(f_j,\cdot)}$        **Preconditions**            **Postconditions**
  `action_name(`$par$`)`          `prec`$_{a^{(f_j,\cdot)}}$   `post`$_{a^{(f_j,\cdot)}}$
  ------------------------------ ---------------------------- ----------------------------

where `prec`$_{a^{(f_j,\cdot)}}$ and `post`$_{a^{(f_j,\cdot)}}$ are *first-order logic predicates* that can be evaluated at run-time. A logical predicate is a boolean-valued function $\mathcal{B}:\mathcal{X}\rightarrow\{$`true`, `false`$\}$. Finally, we define the logical state $l^{(f_j)}$ as a one-hot encoding of $s^{(f_j)}$. The AIP computes the posterior distribution over $p$ plans $\bm \pi$ through free-energy minimization [@pezzato2022aipbt]. The symbolic action to be executed by a robot in the next time step is the first action of the most likely plan, denoted with $\pi_{\zeta, 0}$: $$\begin{eqnarray}
\label{eq:a_t}
    \zeta = \max(\underbrace{[\bm\pi_{1}, \bm\pi_{2},...,\bm\pi_{p}]}_{\bm \pi^\top}),\ 
    a_{\tau=0} = \pi_{\zeta, 0}.
\end{eqnarray}$$

## Model Predictive Path Integral Control (MPPI)

MPPI is a method for solving optimal stochastic problems in a sampling-based fashion [@williams_model_2017; @williams_information-theoretic_2018]. Let us consider the following discrete-time systems: $$\begin{equation}
    x_{t+1} = f(x_t, v_t),\ \ \ v_t \sim \mathcal{N}(u_t, \Sigma),
\end{equation}$$ where $f$, a nonlinear state-transition function, describes how the state $x$ evolves over time $t$ with a control input $v_t$. $u_t$ and $\Sigma$ are the commanded input and the variance, respectively. $K$ noisy input sequences ${V}_k$ are sampled and then applied to the system to forward simulate $K$ state trajectories $Q_k$, $k \in [0,K-1]$, over a time horizon $T$. Given the state trajectories $Q_k$ and a designed cost function $C$ to be minimized, the total state-cost $S_k$ of an input sequence $V_k$ is computed by evaluating $S_k = C(Q_k)$. Finally, each rollout is weighted by the importance sampling weights $w_k$. These are computed through an inverse exponential of the cost $S_k$ with tuning parameter $\beta$ and normalized by $\eta$. For numerical stability, the minimum sampled cost $\rho = \min_k S_k$ is subtracted, leading to: $$\begin{equation}
    \label{eq:weights}
    w_k = \frac{1}{\eta}\exp\left(-\frac{1}{\beta}(S_k - \rho)\right), \ \ \ \sum_{k=1}^K w_k=1
\end{equation}$$

The parameter $\beta$ is called *inverse temperature*. The importance sampling weights are finally used to approximate the optimal control input sequence $U^*$: $$\begin{equation}
    \label{eq:approx_U}
    U^* = \sum_{k=1}^K w_k {V}_k
\end{equation}$$

The first input $u_0^*$ of the sequence $U^*$ is applied to the system, and the process is repeated. At the next iteration, $U^*$ is used as a warm-start, time-shifted backward of one timestep. Specifically, the second last input in the shifted sequence is also propagated to the last input. In this work, we build upon our previous MPPI approaches [@pezzato2023sampling; @trevisan2024biased], where we employed IsaacGym as a dynamic model to forward simulate trajectory rollouts [and allow for arbitrary sampling distributions]{style="color: blue"}.

# Methodology {#sec:algorithm}

The proposed method is depicted in [1](#fig:scheme){reference-type="ref+Label" reference="fig:scheme"}. After a general overview, we discuss the three main parts of the scheme: *action planner*, *motion planner*, and *plan interface*.

:::: {#fig:scheme .figure latex-placement="!b"}
![](Zhang2023MultiModal_figs/general_scheme.png){width="42%"}

::: caption
Proposed scheme. Given symbolic observations $o$ of the environment, the action planner computes $N$ different plan alternatives linked to individual cost functions $C_i$. M3P2I samples control input sequences and uses an importance sampling scheme to approximate the optimal control $u_0^*$.
:::
::::

## Overview

The proposed scheme works as follows. First, the *symbolic observers* translates continuous states $x$ into discretized symbolic observations $o$[, which are then passed to the action planner. The current desired state $s_d$ for Active Inference can be manually set or be encoded as the skeleton solution of a BT as previous work [@pezzato2022aipbt]]{style="color: blue"}. The [AIP]{style="color: blue"} computes $N$ alternative symbolic plans based on the current symbolic state and the available symbolic actions. The symbolic actions are encoded as action templates with pre-post conditions that Active Inference uses to construct action sequences to achieve the desired state. After the plans are generated, the plan interface links the first action $a_{0,i},\ i=0...N-1$ of each plan to a cost function $C_i$. The cost functions are sent to M3P2I, which samples $N\cdot K$ different control input sequences. The input sequences are forward simulated using IsaacGym, which encodes the dynamics of the problem [@pezzato2023sampling]. The resulting trajectories are evaluated against their respective costs. Finally, an importance sampling scheme calculates the approximate optimal control $u_0^*$. All processes are running continuously during execution at different frequencies. The action planner runs, for instance, at $1Hz$ while the motion planner runs at $25Hz$. An overview can be found in [\[alg:whole scheme\]](#alg:whole scheme){reference-type="ref+Label" reference="alg:whole scheme"}.

:::: algorithm
::: algorithmic
[**Input:** action templates and inputs from [\[alg:alternative plans\]](#alg:alternative plans){reference-type="ref+Label" reference="alg:alternative plans"} to [\[alg:m3p2i\]](#alg:m3p2i){reference-type="ref" reference="alg:m3p2i"}]{style="color: blue"} [$AIP.task = AIP.agent(ActionTemplates)$ ]{style="color: blue"} $o \leftarrow GetSymbolicObservation(x)$ /\* *Get current desired state* \*/ $AIP.s_d \leftarrow BT(o)$ [or be manually set]{style="color: blue"}$\triangleright$ from [@pezzato2022aipbt] /\* *Get current action plans from Active Inference* \*/ $\mathcal{P} \leftarrow AIP.par\textcolor{blue}{a}ll\_act\_sel(o)$ $\triangleright$ [\[alg:alternative plans\]](#alg:alternative plans){reference-type="ref+Label" reference="alg:alternative plans"} /\* *Translate action plan to cost function* \*/ $C \leftarrow Interface(\mathcal{P})$ /\* *Compute motion commands* \*/ $M3P2I.command(C)$ $\triangleright$ [\[alg:m3p2i\]](#alg:m3p2i){reference-type="ref+Label" reference="alg:m3p2i"}
:::
::::

## Action planner - Active Inference Planner (AIP)

In contrast to our previous work [@pezzato2022aipbt] where only one action $a_\tau$ for the next time step is computed, we modify the AIP to generate action alternatives. In particular, instead of stopping the search for a plan when a valid executable action $a_\tau$ is found, we repeat the search while removing that same $a_\tau$ from the available action set $\mathcal{A}$. This simple change is effective because we are looking for alternative actions to be applied at the next step, and the AIP builds plans backward from the desired state [@pezzato2022aipbt]. The pseudocode is reported in [\[alg:alternative plans\]](#alg:alternative plans){reference-type="ref+Label" reference="alg:alternative plans"}. The algorithm will cease when no new actions are found, returning a list of possible plans $\mathcal{P}$. This planner is later integrated with M3P2I to evaluate different alternatives in real-time. This increases the [robustness at run-time and,]{style="color: blue"} at the same time, reduces the number of heuristics to be encoded in the action planner. [Specifically, one does not need to encode when to prefer a symbolic action over another based on the geometry of the problem]{style="color: blue"}.

:::: algorithm
::: algorithmic
[**Input:** available action set: $\mathcal{A}$ ]{style="color: blue"} $a_\tau \leftarrow AIP.act\_sel(o)$ $\triangleright$ from [@pezzato2022aipbt] Set $\mathcal{P} \leftarrow \emptyset$ $\mathcal{P}.append(a_\tau)$ $\mathcal{A} = \mathcal{A} \symbol{92} \{a_\tau\}$ $a_\tau \leftarrow AIP.act\_sel(o)$ $\triangleright$ from [@pezzato2022aipbt] **Return** $\mathcal{P}$
:::
::::

## Motion planner - Multi-Modal MPPI (M3P2I)

We propose a Multi-Modal MPPI capable of sampling different plan alternatives from the AIP. Traditional MPPI approaches consider *one* cost function and *one* sampling distribution. In this work, we propose keeping track of $N$ separate control input sequences corresponding to $N$ different plan alternatives/costs. This is advantageous because it offers a general approach to exploring different strategies in parallel. We perform $N$ separate sets of importance weights, one for each alternative, and only ultimately, we combine the weighted control inputs in one coherent control. This allows the smooth blending of different strategies. Assume we consider $N$ alternative plans, a total of $N\cdot K$ samples. Assume the cost of plan $i, i \in [0, N)$ to be formulated as: $$\begin{equation}
    \label{eq: cost function 1}
    %S_i(V_k) = \gamma^{T-1}\phi_i(x_{T-1, k}, v_{T-1, k})+\sum_{t=0}^{T-2}\gamma^t C_i(x_{t, k}, v_{t, k})
    S_i(V_k) = \sum_{t=0}^{T-1}\gamma^t C_i(x_{t, k}, v_{t, k})
\end{equation}$$ $\forall k \in \kappa(i)$ where $\kappa(i)$ is the integer set of indexes ranging from $i \cdot K$ to $(i+1)\cdot K-1$. State $x_{t, k}$ and control input $v_{t, k}$ are indexed based on the time $t$ and trajectory $k$. The random control sequence $V_k = [v_{0, k}, v_{1, k}, \dots, v_{T-1, k}]$ defines the control inputs for trajectory $k$ over a time horizon $T$. The trajectory $Q_i(V_k) = [x_{0, k}, x_{1, k}, \dots, x_{T-1, k}]$ is determined by the control sequence $V_k$ and the initial state $x_{0,k}$. $C_i$ is the cost function for plan $i$. Finally, $\gamma \in [0, 1]$ is a discount factor [that evaluates the importance of accumulated future costs]{style="color: black"}. As in classical MPPI approaches, given the costs $S_i(V_k)$, we can compute the importance sampling weights associated with each alternative as: $$\begin{align}
    \label{eq: weight 1}
    \omega_i(V_k) &= \frac{1}{\eta_i} \exp \left(
    -\frac{1}{\beta_i} 
    \left( S_i(V_k) - \rho_i \right)
    \right), \forall k \in \kappa(i)\\
    \label{eq:eta1}
    \eta_i &=  \sum_{k \in \kappa(i)} \exp \left(-\frac{1}{\beta_i}
    \left( S_i(V_k) - \rho_i \right)
    \right)\\
    \label{eq:ro1}
    \rho_i &= \min_{k \in \kappa(i)} S_i(V_k)
\end{align}$$

We use the insight in [@pezzato2023sampling] to 1) sample Halton splines instead of Gaussian noise for smoother behavior, 2) automatically tune the inverse temperature $\beta_i$ to maintain the normalization factor $\eta_i$ within certain bounds. The latter is helpful since $\eta_i$ indicates the number of samples to which significant weights are assigned. If $\eta_i$ is close to the number of samples $K$, an unweighted average of sampled trajectories will be taken. If $\eta_i$ is close to 1, then the best trajectory sample will be taken. We observed that setting $\eta_i$ [between 5% and 10% of ]{style="color: black"}$K$ generates smooth trajectories. As opposed to [@pezzato2023sampling], we update $\eta$ *within a rollout* to stay within bounds instead of updating it once per iteration, see [\[alg:update temperature\]](#alg:update temperature){reference-type="ref+Label" reference="alg:update temperature"}.

:::: algorithm
::: algorithmic
[**Input:** parameters: $\eta_{l}, \eta_{u}$]{style="color: blue"} $\rho_i \leftarrow \min_{k \in \kappa(i)} S_i(V_k)$ $\triangleright$ [\[eq:ro1\]](#eq:ro1){reference-type="ref+label" reference="eq:ro1"} $\eta_i \leftarrow \sum_{k\in \kappa(i)} \exp (-\frac{S_i(V_k)-\rho_i}{\beta_i})$ $\triangleright$ [\[eq:eta1\]](#eq:eta1){reference-type="ref+label" reference="eq:eta1"} $\triangleright$ [greater]{style="color: blue"} than upper bound $\beta_i = 0.9 * \beta_i$ $\triangleright$ smaller than lower bound $\beta_i = 1.2 * \beta_i$ **Return** $\rho_i, \eta_i, \beta_i$
:::
::::

We use $\mu_i$ to denote the action sequence of plan $i$ over a time horizon $\mu_i = [\mu_{i, 0}, \mu_{i, 1}, \dots, \mu_{i, T-1}]$. Each sequence is weighted by the corresponding weights leading to: $$\begin{align}
    \label{eq:mean action i}
    \mu_i = \sum_{k \in \kappa(i)} \omega_i(V_k) V_k
\end{align}$$

At every iteration, we add to $\mu_i$ the sampled noise from *Halton splines* [@bhardwaj2022storm]. Then, we forward simulate the state trajectories $Q_i(V_k)$ using IsaacGym as in [@pezzato2023sampling]. Finally, given the state trajectories corresponding to the plan alternatives, we need to compute the weights and mean for the overall control sequence. To do so, we concatenate the $N$ state-costs $S_i(V_k), i \in [0, N)$ and represent it as $\tilde{S}(V)$. Therefore, we calculate the weights for the whole control sequence as [@bhardwaj2022storm]: $$\begin{equation}
    \label{eq: weight all}
    \tilde{\omega}(V) = \frac{1}{\eta} \exp \left(
    -\frac{1}{\beta} 
    \left( \tilde{S}(V) - \rho \right)
    \right)
\end{equation}$$

Similarly, $\eta, \rho$ are computed as in [\[eq:eta1,eq:ro1\]](#eq:eta1,eq:ro1){reference-type="ref+Label" reference="eq:eta1,eq:ro1"} but considering $\tilde{S}(V)$ instead. The overall mean action over time horizon $T$ is denoted as $u = [u_0, u_1, \dots, u_{T-1}]$. For each timestep $t$: $$\begin{align}
    \label{eq:mean action all}
    u_t = (1-\alpha_u)u_{t-1} + \alpha_u\sum_{k = 0}^{N\cdot K-1} \tilde{\omega}_k(V) v_{t,k}
\end{align}$$ where $\alpha_u$ is the step size that regularizes the current solution to be close to the previous $u_{t-1}$. The optimal control is set to $u_0^* = u_0$. Note that through [\[eq: weight all\]](#eq: weight all){reference-type="ref+Label" reference="eq: weight all"}, we can smoothly fuse different strategies to achieve a goal in a general way.

:::: algorithm
::: algorithmic
[**Input:** cost functions: $C_i, \forall i \in [0, N)$]{style="color: blue"} Parameters: $N, K, T$ [Initial sequence:]{style="color: blue"} $\mu_i = \bm 0, u= \bm 0, \in \mathbb{R}^T\ \forall i \in [0, N)$ $x \leftarrow GetStateEstimate()$ $InitIsaacGym(x)$ /\* *Begin parallel sampling of alternatives* \*/ []{#line:plan label="line:plan"} []{#line:control label="line:control"} $S_i(V_k) \leftarrow 0$ Sample noise $\mathcal{E}_k \leftarrow SampleHaltonSplines()$ $\mu_i \leftarrow BackShift(\mu_i)$ []{#line:time label="line:time"} $Q_i(V_k) \leftarrow ComputeTrajIsaacGym(\mu_i+\mathcal{E}_k)$ $S_i(V_k) \leftarrow UpdateCost(C_i, Q_i(V_k))$ $\triangleright$ [\[eq: cost function 1\]](#eq: cost function 1){reference-type="ref+label" reference="eq: cost function 1"} []{#line:end_plan label="line:end_plan"} /\* *Begin computing trajectory weights* \*/ []{#line:weights 0 label="line:weights 0"} $\rho_i, \eta_i, \beta_i \leftarrow UpdateInvTemp(i)$ $\triangleright$ [\[alg:update temperature\]](#alg:update temperature){reference-type="ref+Label" reference="alg:update temperature"} $\omega_i(k) \leftarrow \frac{1}{\eta_i} \exp (-\frac{1}{\beta_i}(S_i(V_k)-\rho_i)), \forall k$ $\triangleright$ [\[eq: weight 1\]](#eq: weight 1){reference-type="ref+label" reference="eq: weight 1"} $\mu_i = \sum_{k \in \kappa(i)} \omega_i(V_k) V_k$ $\triangleright$ [\[eq:mean action i\]](#eq:mean action i){reference-type="ref+label" reference="eq:mean action i"} []{#line:weights 1 label="line:weights 1"} /\* *Begin control update* \*/ $\tilde{\omega}(V) = \frac{1}{\eta} \exp \left(
    -\frac{1}{\beta} 
    \left( \tilde{S}(V) - \rho \right)
    \right)$ $\triangleright$ [\[eq: weight all\]](#eq: weight all){reference-type="ref+label" reference="eq: weight all"} $u_t = (1-\alpha_u)u_{t-1} + \alpha_u\sum_{j = 0}^{N\cdot K-1} \tilde{\omega}_k v_{t, k}$ $\triangleright$ [\[eq:mean action all\]](#eq:mean action all){reference-type="ref+label" reference="eq:mean action all"}[]{#line:mean label="line:mean"} $ExecuteCommand(u_0^* = u_0)$ []{#line:execute label="line:execute"} $u =  BackShift(u)$
:::
::::

The pseudocode is summarized in Algorithm [\[alg:m3p2i\]](#alg:m3p2i){reference-type="ref" reference="alg:m3p2i"}. After the initialization, we sample Halton splines and forward simulate the plan alternatives using IsaacGym to compute the costs (Lines [\[line:plan\]](#line:plan){reference-type="ref" reference="line:plan"}-[\[line:end_plan\]](#line:end_plan){reference-type="ref" reference="line:end_plan"}). The costs are then used to update the weights for each plan and update their means (Lines [\[line:weights 0\]](#line:weights 0){reference-type="ref" reference="line:weights 0"}-[\[line:weights 1\]](#line:weights 1){reference-type="ref" reference="line:weights 1"}). Finally, the mean of the overall action sequence is updated (Line [\[line:mean\]](#line:mean){reference-type="ref" reference="line:mean"}), and the first action from the mean is executed.

## Plan interface

The plan interface is a component that takes the possible alternative symbolic actions in $\mathcal{P}$ and links them to their corresponding cost functions, forwarding the latter to M3P2I. For every symbolic action a robot can perform, we store a cost function in a database that we can query at runtime, bridging the output of the action planner to the motion planner.

# Experiments {#sec:experiments}

We evaluate the performance of our method in two different scenarios. The first is a *push-pull scenario* for non-prehensile manipulation of an object with an omnidirectional robot. The second is a *object stacking scenario* with a 7-DOF manipulator with dynamic obstacles and external disturbances at runtime.

## Push-pull scenario

:::: {#fig:push-pull_scenario .figure latex-placement="htb!"}
![](Zhang2023MultiModal_figs/push-pull_scenario.png){width="24%"}

::: caption
Push-pull scenario. The dark purple object has to be placed on the green area. The robot can pull or push the object while avoiding dynamic and fixed obstacles. The objects and goals can have different initial positions.
:::
::::

This scenario is depicted in [2](#fig:push-pull_scenario){reference-type="ref+Label" reference="fig:push-pull_scenario"}. One object has to be placed to a goal, situated in one of the corners of an arena. The object can have different initial locations, for instance, in the middle of the arena or on one of the corners. There are also static and dynamic obstacles, and the robot can push or pull the object. We define the following action templates for AIP and the cost functions for M3P2I.

### Action templates for AIP

The AIP for this task requires one state $s^{(goal)}$ and a relative symbolic observation $o^{(goal)}$ that indicates when an object is at the goal. This is defined as: $$\begin{align}
    % {s^{(goal)}} = \begin{bmatrix} \texttt{isAt(goal)}\\ \texttt{!isAt(goal)}\end{bmatrix},
    o^{(goal))} = \left\{
    \begin{aligned}
        & 0, ||{p}_{G} - {p}_{O}||\leq \delta \\
        & 1, ||{p}_{G} - {p}_{O}|| > \delta
    \end{aligned} 
    \right.
\end{align}$$ [where ${p}_{G}, {p}_{O}$ represent the positions of the goal and the object in a 3D coordinate system.]{style="color: black"} $\delta$ is a constant threshold determined by the user. The mobile robot can either push, pull, or move. These skills are encoded in the action planner as follows:

  ------------------ ------------------- ------------------------------
  **Actions**        **Preconditions**   **Postconditions**
  `push(obj,goal)`   `-`                 ${l^{(goal)}} = [1\ 0]^\top$
  `pull(obj,goal)`   `-`                 ${l^{(goal)}} = [1\ 0]^\top$
  ------------------ ------------------- ------------------------------

The postcondition of the action `push(obj, goal)` is that the object is at the goal, similarly for the pull action. Note that we do not add complex heuristics to encode the geometric relations in the task planner to determine when to push or pull; instead, we will exploit parallel sampling in the motion planner later. [The desired state $s_d$ of]{style="color: blue"} this task is set as a preference for $l^{(goal)} = [1\ 0]^\top$. The BT would contain more desired states for pushing or pulling several blocks. Our approach can be extended to multiple objects in different locations, for instance, and accommodate more involved pre-post conditions and fallbacks since it has the same properties as in [@pezzato2022aipbt].

### Cost functions for M3P2I

We need to specify a cost for each symbolic action. The cost function for pushing object $O$ to the goal $G$ is defined as: $$\begin{equation}
\begin{split}
\label{eq: constraint push}
    C_{push}(R, O, G) &= C_{dist}(R, O)+C_{dist}(O, G)+C_{ori}(O, G) \\
     & +C_{align\_push}(R, O, G)
\end{split}
\end{equation}$$ where minimizing $C_{dist}(O, G) = \omega_{dist} \cdot ||{p}_{G} - {p}_{O}||$ makes the object $O$ close to the goal $G$. $C_{ori}(O, G) = \omega_{ori} \cdot  \phi(\Sigma_{O}, \Sigma_{G})$ defines the orientation cost between the object $O$ and goal $G$. We define $\phi$ for symmetric objects as: $$\begin{equation}
\label{eq: ori_metric}
    \phi(\Sigma_u, \Sigma_v) = \min_{i, j \in \{1, 2, 3\}} \left(2 - ||\Vec{u}_1 \cdot \Vec{v}_i|| - ||\Vec{u}_2 \cdot \Vec{v}_j|| \right)
\end{equation}$$ where $\Sigma_u = \{\Vec{u}_1, \Vec{u}_2, \Vec{u}_3 \}, \Sigma_v = \{\Vec{v}_1, \Vec{v}_2, \Vec{v}_3 \}$ form the orthogonal bases of two coordinates systems. Minimizing this cost makes two axes in the coordinate systems of the object and goal coincide. [The orientation cost for asymmetric objects can be extended from [\[eq: ori_metric\]](#eq: ori_metric){reference-type="ref+Label" reference="eq: ori_metric"} by aligning the corresponding axes.]{style="color: blue"}

The align cost $C_{align\_push}(R, O, G)$ is defined as: $$\begin{align}
\label{eq: constraint align push}
    C_{align\_push}(R, O, G) &= \omega_{align\_push} \cdot h(cos(\theta)),\\
    cos(\theta) &= \frac{({p}_R-{p}_{O}) \cdot ({p}_G-{p}_{O})}{||{p}_R-{p}_{O}|| \cdot ||{p}_G-{p}_{O})||}, \\
    h(cos(\theta)) &= \left\{
    \begin{aligned}
        & 0,\ cos(\theta)\leq0 \\
        & cos(\theta),\ cos(\theta) > 0
    \end{aligned} 
    \right.
\end{align}$$

This makes the object $O$ lie at the center of robot $R$ and goal $G$ so that the robot can push it, as illustrated in [3](#fig:pull_illus){reference-type="ref+Label" reference="fig:pull_illus"}.

:::: {#fig:pull_illus .figure latex-placement="htb!"}
![](Zhang2023MultiModal_figs/push-pull_angle.png){width="24%"}

::: caption
Push and pull ideal configurations. The robot $R$ has to push or pull the object $O$ to the goal $G$.
:::
::::

Similarly, the cost function of making the robot $R$ pull object $O$ to the goal $G$ can be formulated as:

$$\begin{equation}
\begin{split}
\label{eq: constraint pull}
    & C_{pull}(R, O, G) = C_{dist}(R, O)+C_{dist}(O, G)+C_{ori}(O, G) \\
     & +C_{align\_pull}(R, O, G) + C_{act\_pull}(R, O, G)
\end{split}
\end{equation}$$ where the align cost $C_{align\_pull}(R, O, G)$ makes the robot $R$ lie between the object $O$ and goal $G$, see [3](#fig:pull_illus){reference-type="ref+Label" reference="fig:pull_illus"}. While pulling, we simulate a suction force in IsaacGym, and we are only allowed to sample control inputs that move away from the object through $C_{act\_pull}(R, O, G)$. Mathematically: $$\begin{align}
    \label{eq: constraint align pull}
    C_{align\_pull}(R, O, G) &= \omega_{align\_pull}\ \cdot h(-cos(\theta)) \\
    C_{act\_pull}(R, O, G) &= \omega_{act\_pull}\ \cdot h(\frac{({p}_O-{p}_R)\cdot \Vec{u}}{||{p}_O-{p}_R|| \cdot ||\Vec{u}||})
\end{align}$$

An example can be seen in [4](#fig:example_push_pull){reference-type="ref+Label" reference="fig:example_push_pull"}. [We also consider an additional cost $C_{dyn\_obs}(R, D)$ to avoid collisions with (dynamic) obstacles while operating. [The dynamic obstacle is assumed to move in a certain direction with constant velocity.]{style="color: blue"} We use a constant velocity model to predict the position of the dynamic obstacle $D$ in the coming horizon and try to maximize the distance between the latter and the robot:]{style="color: black"} $$\begin{align}
    C_{dyn\_obs}(R, D) = \omega_{dyn\_obs} \cdot e ^{-|| {p}_R - {p}_{D_{pred}}||}
\end{align}$$ where ${p}_{D_{pred}}$ is the predicted position of dynamic obstacle.

:::: {#fig:example_push_pull .figure latex-placement="!htb"}
![](Zhang2023MultiModal_figs/push-pull_examples.png){width="40%"}

::: caption
Illustrative example of pulling and pushing a block to a goal. The strategy differs according to the object, goal location, and dynamic obstacle position. What action to perform is decided at runtime through multi-modal sampling.
:::
::::

### Results

We test the performance of our approach in two configurations: a) the object is in the middle of the arena, and the goal is to one corner, and b) both the object and the goals are in different corners. For each arena configuration, we test three cases: the robot can either only push, only pull, or combine the two through our M3P2I. The AIP plans for the two alternatives, pushing and pulling, and forwards the solution to the plan interface. Then, M3P2I starts minimizing the costs until the AIP observes the completion of the task. We performed 20 trials per case, per arena configuration, for a total of 120 simulations. By only pulling an object, the robot cannot tightly place it on top of the goal in the corner; on the other hand, by only pushing, the robot cannot retrieve the object from the corner. Using multi-modal motion, we can complete the task in every tested configuration. [1](#tab:results_push_pull){reference-type="ref+Label" reference="tab:results_push_pull"} shows that the multi-modal case outperforms push and pull in both arena configurations. It presents lower position and orientation errors and a shorter [planning and execution]{style="color: blue"} time.

::: {#tab:results_push_pull}
  --------------- ----------- -- -- --
     **Case**      **Skill**        
   **pos error**                    
   **ori error**                    
   **time (s)**                     
                     Push           
     (0.0212)                       
     (0.0217)                       
     (6.8084)                       
                                    
      corner         Pull           
     (0.0836)                       
     (0.1294)                       
     (13.7952)                      
                                    
       modal                        
     (0.0310)                       
     (0.0045)                       
     (0.8239)                       
                     Push           
     (3.2987)                       
     (0.0929)                       
                                    
      corner         Pull           
     (0.1778)                       
     (0.2050)                       
     (7.9240)                       
                                    
       modal                        
     (0.0091)                       
     (0.0227)                       
     (3.4591)                       
  --------------- ----------- -- -- --

  : Simulation Results of Push and Pull
:::

## Object stacking scenario

We address the challenge of stacking objects with external task disruptions, necessitating adaptive actions like re-grasping with different pick configurations (e.g., top or side picking in [5](#fig:pick_scenario){reference-type="ref+Label" reference="fig:pick_scenario"}). We showcase the robot's ability to rectify plans by repeating actions or compensating for unplanned occurrences, such as unexpected obstacles obstructing the path. We benchmark against the cube-stacking task outlined in [@makoviychuk2021isaac].

:::: {#fig:pick_scenario .figure latex-placement="htb!"}
![](Zhang2023MultiModal_figs/pick_scenarios.png){width="40%"}

::: caption
Pick-place scenarios. The red cube has to be placed on top of the green cube. The red cube can be either on the table or a constrained shelf, requiring different pick strategies from the top or the side, respectively.
:::
::::

### Action templates for AIP

For this task, we define the following states $s^{(reach)}$, $s^{(hold)}$, $s^{(preplace)}$, $s^{(placed)}$, and their corresponding symbolic observations. The robot has four symbolic actions, summarized [below:]{style="color: blue"}

[]{#tab::prepost label="tab::prepost"}

::: {#tab::prepost}
  ----------------- ------------------- ----------------------------------
  **Actions**       **Preconditions**   **Postconditions**
  `reach(obj)`      `-`                 ${l^{(reach)}} = [1\ 0]^\top$
  `pick(obj)`       `reachable(obj)`    ${l^{(hold)}} = [1\ 0]^\top$
  `prePlace(obj)`   `holding(obj)`      ${l^{(preplace)}} = [1\ 0]^\top$
  `place(obj)`      `atPreplace(obj)`   ${l^{(placed)}} = [1\ 0]^\top$
  ----------------- ------------------- ----------------------------------
:::

The symbolic observers to estimate the states are defined as follows. To estimate whether the gripper is close enough to the cube, we define the relative observation $o^{(reach)}$. We set $o^{(reach)} = 0$ if $\delta_r \leq \textcolor{blue}{\delta}$, where $\delta_r = ||{p}_{ee} - {p}_{O}||$ measures the distance between the end effector $ee$ and the object $O$. $o^{(reach)} = 1$ otherwise. To estimate whether the robot is holding the cube [of size 0.06m]{style="color: blue"}, we define: $$\begin{align}
    & o^{(hold)} = \left\{
    \begin{aligned}
        & 0, \delta_f < \textcolor{blue}{0.06+\delta} \text{ and } \delta_f \geq \textcolor{blue}{0.06-\delta}\\
        & 1, \delta_f \geq \textcolor{blue}{0.06+\delta} \text{ or } \delta_f \leq \textcolor{blue}{0.06-\delta}
    \end{aligned} 
    \right.
\end{align}$$ where $\delta_f = ||{p}_{ee\_l} - {p}_{ee\_r}||$ measures the distance between the two gripper's fingers. To estimate whether the cube reaches the pre-place location, we define: $$\begin{align}
\label{eq:preplace_obs}
    & o^{(preplace)} = \left\{
    \begin{aligned}
        & 0, C_{dist}(O, P) < \textcolor{blue}{\delta} \text{ and } C_{ori}(O, P) < \textcolor{blue}{\delta} \\
        & 1, C_{dist}(O, P) \geq \textcolor{blue}{\delta} \text{ or } C_{ori}(O, P) \geq \textcolor{blue}{\delta}
    \end{aligned} 
    \right.
\end{align}$$ where $C_{dist}(O, P)$ and $C_{ori}(O, P)$ measure the distance and the orientation between the object $O$ and the pre-place location $P$ as in [\[eq: constraint push\]](#eq: constraint push){reference-type="ref+Label" reference="eq: constraint push"}. The pre-place location is a few centimeters higher than the target cube location, directly on top of the green cube. We use the same logic as [\[eq:preplace_obs\]](#eq:preplace_obs){reference-type="ref+Label" reference="eq:preplace_obs"} for $o^{(placed)}$ where the place location is directly on top of the cube location. [The desired state for this task is set to be $l^{(placed)} = [1\ 0]^T$]{style="color: blue"}, meaning the cube is correctly placed on top of the other. Note that in more complex scenarios, such as rearranging many cubes, the BT can guide the AIP as demonstrated in [@pezzato2022aipbt].

### Cost functions for M3P2I

At the motion planning level, the cost functions for the four actions are formulated as: $$\begin{equation}
    \label{eq: constraint reach}
    \begin{aligned}
        C_{reach}(ee, O, \psi) &= \omega_{reach} \cdot ||{p}_{ee}-{p}_{O}|| \\
        &+ \omega_{tilt} \cdot \left(\frac{||\Vec{z}_{ee} \cdot \Vec{z}_{O}||}{||\Vec{z}_{ee}|| \cdot ||\Vec{z}_{O}||} - \psi \right)
    \end{aligned}
\end{equation}$$ $$\begin{align}
    &
    \begin{aligned}
        C_{pick}(ee) &= \omega_{gripper} \cdot l_{gripper} 
    \end{aligned}\\
    &
    \begin{aligned}
        C_{preplace}(O, P) &= C_{dist}(O, P) + C_{ori}(O, P)
    \end{aligned}\\
    &
    \begin{aligned}
        C_{place}(O, P) &= \omega_{gripper} \cdot (1-l_{gripper})
    \end{aligned}
\end{align}$$ $C_{reach}(ee, O, \psi)$ moves the end effector close to the object with a grasping tilt constraint $\psi$. As $\psi$ approaches 1, the gripper becomes perpendicular to the object; as it nears 0, the gripper aligns parallel to the object's supporting plane.

### Results - reactive pick and place

We first consider the pick-and-place under disturbances. We model disturbances by changing the position of the cubes at any time. We compare the performance of our method with the off-the-shelf RL method [@makoviychuk2021isaac]. This is a readily available Actor-Critic RL example from IsaacGym, which considers the same tabletop configuration and robot arm. We compare the methods in a *vanilla* task without disturbances and a *reactive* task with disturbances. It should be noticed that the cube-stacking task in [@makoviychuk2021isaac] only considers moving the cube on top of the other cube while neglecting the action of opening the gripper and releasing the cube. In contrast, our method exhibits fluent transitions between pick and place and shows robustness to interferences [such as repick ]{style="color: blue"}during the long-horizon task execution. Results are available in [3](#tab: results reactive pick place){reference-type="ref+Label" reference="tab: results reactive pick place"}, with 50 trials per case. While the RL agent shows a slightly lower position error in the vanilla case, our method outperforms it in the reactive task. [Planning and execution time for smooth pick-and-place with our method is approximately 5 to 10s.]{style="color: blue"}

::: {#tab: results reactive pick place}
+:-------------------------------:+:----------:+:----:+:----------------------:+
| **Task**                        | **Method** |      |                        |
+---------------------------------+------------+------+------------------------+
| **epochs**                      |            |      |                        |
+---------------------------------+------------+------+------------------------+
| **pos error**                   |            |      |                        |
+---------------------------------+------------+------+------------------------+
| [Vanilla]{style="color: black"} | Ours       | 0    | 0.0075 (0.0036)        |
|                                 +------------+------+------------------------+
|                                 | RL         | 1500 | **0.0042** (0.0019)    |
+---------------------------------+------------+------+------------------------+
| Reactive                        | Ours       | 0    | **0.0117** (0.0166)    |
|                                 +------------+------+------------------------+
|                                 | RL         | 1500 | 0.0246 (0.0960)        |
+---------------------------------+------------+------+------------------------+

: Simulation Results of Reactive Pick and Place
:::

[]{#tab: results reactive pick place label="tab: results reactive pick place"}

### Results - multi-modal grasping

In this case, we consider grasping the object with different grasping poses by sampling two alternatives in parallel. That is, pick from the top or the side to cover the cases when the object is on the table or the constrained shelf with an obstacle above. To do so, we use the proposed M3P2I and incorporate the cost functions of $C_{reach}(ee, O, \psi=0)$ and $C_{reach}(ee, O, \psi=1)$ as shown in [\[eq: constraint reach\]](#eq: constraint reach){reference-type="ref+Label" reference="eq: constraint reach"}. This allows for a smooth transition between top and side grasp according to the geometry of the problem, see [6](#fig: generalizing pick){reference-type="ref+Label" reference="fig: generalizing pick"}.

:::: {#fig: generalizing pick .figure latex-placement="htb!"}
![](Zhang2023MultiModal_figs/pick_examples.png){width="40%"}

::: caption
Example of different picking strategies computed by our multi-modal MPPI. The obstacle on top of the shelf can be moved, simulating a dynamic obstacle.
:::
::::

### Results - real-world experiments

[Our real-world validation of reactive pick-and-place, depicted in [7](#fig: real-world pick){reference-type="ref+Label" reference="fig: real-world pick"}, involves avoiding a moving stick and disturbances such as movement and theft of the cube. M3P2I enables smooth execution and recovery while using different grasp configurations.]{style="color: black"}

:::: {#fig: real-world pick .figure latex-placement="htb"}
![](Zhang2023MultiModal_figs/pick_real.png){width="40%"}

::: caption
Real-world experiments of picking a cube from the table or the shelf while avoiding dynamic obstacles and recovering from task disturbances.
:::
::::

# Discussion

[In this section, we discuss key aspects of our solution and potential future work. The main strength of M3P2I is its ability to reason over discrete alternative actions at the motion planning level. This is enabled by sampling different control sequences for each alternative symbolic action and then blending them through importance sampling. We thus alleviate the task planning burden by eliminating logic heuristics to switch between these actions. Sampling alternatives at the motion planning level increases robustness during execution, at the price of slightly degrading the performance since the control distribution is also slightly biased towards less effective strategies, as shown in [@trevisan2024biased]. The performance of M3P2I also depends on the weight tuning of the cost functions. In this case, implementing auto-tuning techniques can reduce manual effort [@spahn2023autotuning]. The cost functions also need to capture the essence of the skills.]{style="color: blue"} [ The AIP requires manually defined symbolic action templates and a set of discrete states. The discrete desired states need to be encoded in a sequence in a BT or can be as simple as encoding the end state for a task, as in our examples.]{style="color: blue"} [To transfer from simulation to the real world, we considered randomization of object properties in the rollouts [@pezzato2023sampling]. Online system identification could be added to achieve better performance with uncertain model parameters [@abraham2020model].]{style="color: blue"}

# Conclusion {#sec:conclusions}

In this paper, [to address the runtime geometric uncertainties and disturbances]{style="color: black"}, we proposed a method to combine the adaptability of an Active Inference planner (AIP) for high-level action selection with a novel Multi-Modal Model Predictive Path Integral Controller (M3P2I) for low-level control. We modified the AIP to generate plan alternatives that are linked to costs for M3P2I. The motion planner can sample the plan alternatives in parallel, and it computes the control input for the robot by smoothly blending different strategies. In a push-pull task, we demonstrated how our proposed framework can blend both push and pull actions, allowing it to deal with corner cases where approaches only using a single plan fail. With a simulated manipulator, we showed our method outperforming a reinforcement learning baseline when the environment is disturbed while requiring no training. Simulated and real-world experiments demonstrated how our approach solves reactive object stacking tasks with a manipulator subject to severe disturbances and various scene configurations that require different grasp strategies.

[^1]: This research was supported in part by Ahold Delhaize; by the Netherlands Organization for Scientific Research (NWO), domain Science (ENW), TRILOGY project; and by the European Union through ERC, under Grant 101041863 (INTERACT). *(Corresponding author: Yuezhe Zhang.)*

[^2]: The authors are with Cognitive Robotics Department, TU Delft, The Netherlands `yuezhezhang_bit@163.com``, {corrado.pezzato, salmi.chadi}@gmail.com, {e.trevisan, c.h.corbato, j.alonsomora}@tudelft.nl`
