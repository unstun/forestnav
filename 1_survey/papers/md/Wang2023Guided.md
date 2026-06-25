---
citation_key: Wang2023Guided
arxiv_id: 2309.13508
arxiv_url: https://arxiv.org/abs/2309.13508
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-24T16:07:38Z
origin: ai+web
reviewed: false
---

# Introduction

Hierarchical reinforcement learning (HRL) has made significant contributions toward solving complex and long-horizon tasks with sparse rewards. Among HRL frameworks, goal-conditioned HRL is an especially promising paradigm for goal-directed learning in a divide-and-conquer manner[@vezhnevets2017feudal]. In goal-conditioned HRL, multiple goal-conditioned policies are stacked hierarchically, where the higher-level policy assigns a directional subgoal to the lower-level policy, and the lower strives toward it. Recently, related advances [@zhang2020generating; @zhang2022adjacency; @li2021learning; @leed2022hrl; @guo2021state; @huang2019mapping; @eysenbach2019search; @zhang2021world] have made significant progress in improving exploration efficiency via reachable subgoal generation with adjacency constraint [@zhang2020generating; @zhang2022adjacency] and graph-based planning [@csimcsek2005identifying; @huang2019mapping; @eysenbach2019search; @zhang2021world]. Yet, integrating these strategies with an off-policy learning method still struggles with being sample efficient. Previous research handles this issue by relabeling experiences with more faithful goals [@nachum2018data; @levy2019learning; @zhu2021mapgo], in which the relabeling aims to explore how to match the higher-level intent and the actual outcome of the lower-level subroutine. The HER-style approaches [@andrychowicz2017hindsight; @levy2019learning; @zhu2021mapgo] overwrite the former with the latter, while the HIRO [@nachum2018data] modifies the past instruction to adapt to the current behavioral policy, thereby improving the data-efficiency.

inter-level cooperation and communication, addressing the following questions is essential: 1) how does the lower level comprehend and synchronize with the higher level? 2) how does the lower level errors from the higher level? 3) how does the lower level directly understand the overall task without relying on higher-level proxies? the gap between the intent and outcome, leading to robust policy improvement.

In this paper, we propose a novel goal-conditioned HRL framework to systematically facilitate inter-level cooperation, which mainly consists of three crucial components: 1) the goal-relabelling for synchronizing, 2) the gradient penalty for enhancing robustness against high-level errors, and 3) the one-step rollout-based planning for . The key insight in the proposed framework is to modularly integrate a forward dynamics prediction model into HRL framework for improving the data efficiency and enhancing learning efficiency. Specifically, our framework, named **G**uided **C**ooperation via **M**odel-based **R**ollout (GCMR), brings together three crucial ingredients:

- off-policy correction. Additionally, we .

- We propose a gradient penalty to suppress sharp lower-level Q-function gradients, which clamps the Q-function gradient by means of an inferred upper bound. .

- Meanwhile, we designed a one-step rollout-based planning method to prevent the lower-level policy from getting stuck in local optima

To justify the superiority of the proposed , we integrate with a strong baseline: ACLG, a disentangled variant of HIGL [@kim2021landmark]. Experimental results show that incorporating the proposed framework in complex and sparse reward environments.

- 
- 
- 

# Preliminaries {#sec:Preliminaries}

Consider a finite-horizon, goal-conditioned Markov decision process (MDP) represented by a tuple $\left(\mathcal{S}, \mathcal{G}, \mathcal{A}, \mathcal{P}, \mathcal{R} \right)$, where $\mathcal{S}$, $\mathcal{G}$, and $\mathcal{A}$ denote the state space, goal space, and action space, respectively. The transition function $\mathcal{P}: \mathcal{S} \times \mathcal{A} \rightarrow \mathcal{S}$ defines the transition dynamics of environment, and the $\mathcal{R}: \mathcal{S} \times \mathcal{A} \times \mathcal{G} \rightarrow \mathbb{R}$ is the reward function. Specifically, the environment will transition from $s_t \in \mathcal{S}$ to a new state $s_{t+1} \in \mathcal{S}$ while yielding a reward $R_t \in \mathcal{R}$ once it takes an action $a_t \in \mathcal{A}$, where $s_{t+1} \sim \mathcal{P}\left(s_{t+1}|a_{t+1}, a_{t}\right)$ and $R_t$ is conditioned on a final goal $g \in \mathcal{G}$. In most real-world scenarios, complex tasks can often be decomposed into a sequence of simpler movements and interactions. Therefore, we formulate a hierarchical reinforcement learning framework, which typically has two : higher- and lower-level policies, to deal with these challenging tasks. The higher-level policy observes the state $s_{t}$ of environment and produces a high-level action $sg_t$, i.e., a subgoal indicating a desired change of state or absolute location to reach every $c$ time steps. The lower-level policy attempts to reach these assigned subgoals within a $c$ time interval. Suppose that the higher-level policy and lower-level policy are parameterized by neural networks with parameters $\theta_{hi}$ and $\theta_{lo}$, respectively. The above procedure of the higher-level controller can be formulated: $sg_t \sim \pi \left(sg|s_t, g;\theta_{hi}\right) \in \mathcal{G}$ when $t \equiv 0$ (mod $c$). The lower-level policy observes the state $s_t$ as well as subgoal $sg_t$ and then yields a low-level atomic action to interact directly with the environment: $a_t \sim \pi \left(a|s_t,sg_t;\theta_{lo}\right) \in \mathcal{A}$. Notably, for the relative subgoal scheme, subgoals evolve following a pre-defined subgoal transition process $sg_t = h\left(sg_{t-1},s_{t-1},s_t\right) = sg_{t-1} + \varphi(s_{t-1} - s_t)$ when $t \not\equiv 0$ (mod $c$), where $\varphi: \mathcal{S} \rightarrow \mathcal{G}$ is a known mapping function that transforms a state into the goal space. The pre-defined transition makes the lower-level agent seem completely self-contained and like an autonomous dynamical system.

## Parameterized Rewards

During interaction with the environment, the higher-level agent makes a plan using subgoals and receives entire feedback by accumulating all external rewards within the planning horizon: $$\begin{equation}
r^{hi}_t=\sum_{i=t}^{t+c-1} R_i \left(s_i,a_i,g\right)
\end{equation}$$ The lower-level agent is intrinsically motivated in the form of internal reward that evaluates subgoal-reaching performance: $$\begin{equation}
r^{lo}_t=-\Vert sg_{t+1} -  \eta \varphi \left( s_{t+1} \right)\Vert_2
\label{intrinsic_reward}
\end{equation}$$ Where $\eta$ denotes a Boolean hyper-parameter whose value is 0/1 for the relative/absolute subgoal scheme.

## Experience Replay for Off-Policy Learning

Experience replay has been the fundamental component for off-policy RL algorithms, which greatly improves the sample efficiency by reusing previously collected experiences. Here, there is no dispute that the lower-level agent can collect the experience $\tau_{lo} = \left( \left \langle s_t, sg_t \right \rangle, a_t, r^{lo}_t, \left \langle s_{t+1}, sg_{t+1} \right \rangle \right)$ by using the behavioral policy to directly interact with the environment. The higher-level agent interacts indirectly with it through the lower-level proxy and then stores a series of state-action transitions as well as a cumulative reward, i.e., $\tau_{hi} = \left( \left \langle s_{t:t+c-1}, g \right \rangle, sg_{t:t+c-1}, r^{hi}_t, \left \langle s_{t+c}, g \right \rangle \right)$, into the high-level replay buffer. The lower- and higher-level policies can be trained by sampling transitions stored in these experience replay buffers $\mathcal{D}_{lo}$, $\mathcal{D}_{hi}$. The aim of optimization is to maximize the expected discounted reward $\mathbb{E}_{L\in \left \{ lo, hi\right \} } \left[ \sum^{\infty}_{t=0} \gamma^i r^L_t\right]$, where $\gamma \in \left[0, 1 \right]$ is the discount factor. In practice, we instantiate lower- and higher-level agents based on the TD3 algorithm [@fujimoto2018addressing], each having a pair of online critic networks with parameters $\phi_1$ and $\phi_2$, along with a pair of target critic networks with parameters $\phi^{\prime}_1$ and $\phi^{\prime}_2$. Additionally, TD3 has a single online actor parameterized by $\theta$ and a target actor parameterized by $\theta^{\prime}$. All target networks are updated using a soft update approach. Then, the Q-network can be updated by minimizing the mean squared temporal-difference (TD) error over all sampled transitions. To simplify notation, we adopt unified symbols $o^{L}_t$ and $a^L_t$ to indicate the observation and performed action, where $\left \langle o^{L}_t, a^L_t\big|_{L=lo}\right \rangle=\left \langle \left \langle s_t, sg_t \right \rangle, a_t \right \rangle$ for lower-level while $\left \langle o^{L}_t, a^L_t\big|_{L=hi}\right \rangle=\left \langle \left \langle s_t, g \right \rangle, sg_t \right \rangle$ for higher-level. Hence, the Q-learning loss can be written as follows: $$\begin{equation}
\mathcal{L}(\phi_{i, L}) = \mathbb{E}_{\tau_{L} \sim \mathcal{D}_{L}} \left[Q \left(o^{L}_t, a^L_t; \phi_{i, L} \right) - y^{L}_t \right]^2 \Big|_{\substack{L\in \left \{ lo, hi\right \} \\ i\in \left \{1, 2\right \}}}
\label{critic_loss}
\end{equation}$$ Where $y^{L}_t$, i.e., $y^{lo}_t$ or $y^{hi}_t$, is dependent on $\theta_{lo}$ or $\theta_{hi}$ correspondingly because target policies map states to the \"optimal\" actions in an almost deterministic manner: $$\begin{equation}
\begin{aligned}
y^{L}_t=r^{L}_t + \gamma \min_{i=1,2} &Q \left(o^{L}_{t^{\prime}}, \pi \left(o^{L}_{t^{\prime}};\theta^{\prime}_{L} \right)+\varepsilon; \phi^{\prime}_{i,L} \right) \Big|_{L\in \left \{ lo, hi\right \}}\\
{\rm with} \quad \varepsilon & \sim {\rm clip}(\mathcal{N}(0,\sigma), -a_c, a_c)
\label{critic_loss_q}
\end{aligned}
\end{equation}$$ Where $\sigma$ is the s.d. of the Gaussian noise, $a_c$ defines the range of the auxiliary noise, and $o^{L}_{t^{\prime}}$ refers to the next obtained observation after taking an action. It is noteworthy that $t^{\prime}=t+c$ with respect to the higher-level while $t^{\prime}=t+1$ for the lower-level. Drawing support from Q-network, the policy can be optimized by minimizing the following loss: $$\begin{equation}
\mathcal{L}(\theta_{L}) = -\mathbb{E}_{\tau_{L} \sim \mathcal{D}_{L}}\left[ Q \left(o^{L}_{t}, \pi \left(o^{L}_{t};\theta_{L} \right); \phi_{1,L} \right) \right] \Big|_{L\in \left \{ lo, hi\right \}}
\label{actor_loss}
\end{equation}$$ As mentioned above, we outline the common actor-critic approach with the deterministic policy algorithms [@timothy2016continuous; @fujimoto2018addressing]. For more details, please refer to [@fujimoto2018addressing].

## Adjacency Constraint

For the high-level subgoal generation, reachability within $c$ steps is a sufficient condition for facilitating reasonable exploration. Zhang et al. [@zhang2020generating; @zhang2022adjacency] mined the adjacency information from trajectories gathered by the changing behavioral policy over time. In that study, a $c$-step adjacency matrix was constructed to memorize $c$-step adjacent state-pairs appearing in these trajectories. To ensure this procedure is differentiable and can be generalized to newly-visited states, the adjacency information stored in such matrix was further distilled into an adjacency network $\psi$ parameterized by $\Phi$. Specifically, the adjacency network approximates a mapping from a goal space into an adjacency space. Subsequently, the resulting embeddings can be utilized to measure whether two states are $c$-step adjacent using the Euclidean distance. For example, the $c$-step adjacent estimation (or shortest transition distance) of two states $s_i$ and $s_j$ can be calculated as: $d_{st}(s_i, s_j; \Phi) \approx \frac{c}{\zeta_c}||\psi_{\Phi}(\varphi(s_i))-\psi_{\Phi}(\varphi(s_j))||_2$, where $\zeta_c$ is a scaling factor and the $\varphi$ function maps states into the goal space. Such an adjacency network can be learned by minimizing the following contrastive-like loss: $\mathcal{L}_{{\rm adj}}(\Phi)=\mathbb{E}_{s_i,s_j\in\mathcal{S}}[l\cdot \max(||\psi_{\Phi}(\varphi(s_i))-\psi_{\Phi}(\varphi(s_j))||_2-\zeta_c, 0)+(1-l)\cdot \max(\zeta_c+\delta_{\rm adj}-||\psi_{\Phi}(\varphi(s_i))-\psi_{\Phi}(\varphi(s_j))||_2, 0)]$, where $\delta_{\rm adj} > 0$ is a hyper-parameter indicating a margin between embeddings and $l \in \{0,1\}$ is the label indicating whether $s_i$ and $s_j$ are -step adjacent.

## Landmark-based Planning

Graph-based navigation has become a popular technique for solving complex and sparse reward tasks by providing a long-term horizon. The relevant frameworks [@savinov2018semi; @huang2019mapping; @eysenbach2019search; @emmons2020sparse; @yang2020plan2vec; @kim2021landmark; @zhang2021world; @leed2022hrl; @kim2022imitating] commonly contain two components: (a) a graph built by sampling landmarks and (b) a graph planner to select waypoints. In a graph, each node corresponds to an observation state, while edges between nodes are weighted using a distance estimation. Specifically, a set of observations randomly subsampling from the replay buffer are organized as nodes, where high-dimensional samples (e.g., images) may be embedded into low-dimensional representations [@savinov2018semi; @eysenbach2019search; @liu2020hallucinative; @yang2020plan2vec; @zhang2021world]. However, operations over the direct subsampling of the replay buffer will be costly. The state aggregation [@emmons2020sparse] and landmark sampling based on farthest point sampling (FPS) were proposed for further sparsification [@huang2019mapping; @kim2021landmark; @leed2022hrl; @kim2022imitating]. Our study follows prior works of Kim et al. [@kim2021landmark; @kim2022imitating], in which FPS was employed to select a collection of landmarks, i.e., *coverage-based landmarks ${LM}^{\rm cov}$*, from the replay buffer. In addition to this, HIGL [@kim2021landmark] used random network distillation [@burda2019exploration] to explicitly sample novel landmarks, i.e., *novelty-based landmarks ${LM}^{\rm nov}$*, a set of states rarely visited in the past. Hence, the final collection of landmarks was ${LM}={LM}^{\rm cov} \cup {LM}^{\rm nov}$. Once landmarks are added to the graph, the edge weight between any two vertices can be estimated by a lower-level value function [@huang2019mapping; @eysenbach2019search; @kim2021landmark; @leed2022hrl; @kim2022imitating] or the (Euclidean-based or contrastive-loss-based) distance between low-dimensional embeddings of states [@savinov2018semi; @yang2020plan2vec; @liu2020hallucinative; @zhang2020generating]. Following prior works [@huang2019mapping; @kim2021landmark; @kim2022imitating], in this study, we estimated the edge weight via the lower-level value function, i.e., $-V_{lo}(s_i, \varphi(s_j)) \approx -Q(s_i, \varphi(s_j), \pi \left(a|s_i,\varphi(s_j);\theta_{lo}\right); \phi_{lo}), \forall s_i, s_j \in LM$. After that, unreachable edges were clipped by a preset threshold [@huang2019mapping]. In the end, the shortest path planning algorithm was run to plan the next subgoal, the very first landmark in the shortest path from the current state $s_t$ to the goal $g$: $$\begin{equation}
sg_{t}^{\rm plan}=\arg\min_{\varphi(s_i)}-[V_{lo}(s_t, \varphi(s_i))+V_{lo}(s_i, g)], \qquad\text{s.t.} \quad \forall s_i \in {LM}^{\rm cov} \cup {LM}^{\rm nov}
\label{HIGL_landmarks}
\end{equation}$$

## 

:::: {#higl_aclg_vis .figure latex-placement="htbp"}
![](Wang2023Guided_figs/ac_ld_higl_aclg.png){width="90%"}

::: caption
:::
::::

In HIGL, after finding a landmark through landmark-based planning (see Equation [\[HIGL_landmarks\]](#HIGL_landmarks){reference-type="ref" reference="HIGL_landmarks"}), the raw selected landmark was shifted towards the current state $s_t$ for reachability: $sg_{t}^{\rm pseudo}= sg_{t}^{\rm plan} + \delta_{\rm pseudo} \cdot \frac{sg_{t}^{\rm plan}-\varphi(s_t)}{||sg_{t}^{\rm plan}-\varphi(s_t)||_2}$, where $\delta_{\rm pseudo}$ denotes the shift magnitude. Then, the higher-level policy was guided to generate subgoals adjacent to the planned landmarks and the landmark loss of HIGL was formulated as: $$\begin{equation}
\mathcal{L}^{\rm HIGL}_{\rm landmark}(\theta_{hi}) = \lambda^{\rm HIGL}_{\rm landmark} \cdot \max(||\psi_{\Phi}(sg_{t}^{\rm pseudo}) -\psi_{\Phi}(\pi(s_t, g;\theta_{hi}))||\chadded{_{2}} - \zeta_c, 0)
\label{higl_loss}
\end{equation}$$ Here, Kim et al. employed the adjacency constraint to encourage the generated subgoals to be in the $c$-step adjacent region to the planned landmark. However, the entanglement between the adjacency constraint and landmark-based planning limited the performance of HIGL.

Inspired by PIG [@kim2022imitating], we proposed a disentangled variant of HIGL. We only made minor modifications to the landmark loss (see Equation [\[higl_loss\]](#higl_loss){reference-type="ref" reference="higl_loss"}) of HIGL: $$\begin{equation}
\begin{aligned}
\mathcal{L}^{\rm ACLG}&(\theta_{hi}) \\= & \lambda_{\rm adj} \cdot \max(||\psi_{\Phi}(\varphi(s_t))-\psi_{\Phi}(\pi(s_t, g;\theta_{hi}))||\chadded{_{2}} - \zeta_c, 0) \\ \qquad &\qquad+ \lambda^{\rm ACLG}_{\rm landmark} \cdot ||sg_{t}^{\rm pseudo} - \pi(s_t, g;\theta_{hi}) ||^2_2
\end{aligned}
\end{equation}$$ The former term is the adjacency constraint and the latter is the landmark-guided loss, so the proposed method was called ACLG. The hyper-parameters $\lambda_{\rm adj}$ and $\lambda^{\rm ACLG}_{\rm landmark}$ were introduced to better balance the adjacency constraint and landmark-based planning.

# Related work {#related_work}

## Transition Relabeling

Training a hierarchy using an off-policy algorithm remains a prominent challenge due to the non-stationary state transitions [@nachum2018data; @levy2019learning; @zhu2021mapgo]. Specifically, the higher-level policy takes the same action under the same state but could receive markedly different outcomes because of the low-level policy changing, so the previously collected transition tuple is no longer valid. To address the issues, HIRO [@nachum2018data] deployed an off-policy correction to maintain the validity of past experiences, which relabeled collected transitions with appropriate high-level actions chosen to maximize the probability of the past lower-level actions. Alternative approaches, HAC [@andrychowicz2017hindsight; @levy2019learning], replaced the original high-level action with the achieved state (projected to the goal space) in the form of hindsight. However, HAC-style relabeled subgoals are compatible with the past low-level policy rather than the current one, deteriorating the non-stationarity issue.

Our work is related to HIRO [@nachum2018data], and the majority of modification is that we roll out the off-policy correction using learned transition dynamics to suppress the accumulative error. The closest work is the MapGo [@zhu2021mapgo], a model-based HAC-style framework in which the original goal was replaced with a foresight goal by reasoning using an ensemble transition model. Our work differs in that we screen out a faithful subgoal that induces rollout-based action sequence similar to the past transitions, while the MapGo overwrites the subgoal with a foresight goal based on the model-based rollout. Meanwhile, our framework proposes a gradient penalty with model-inferred upper bound to prohibit the disturbance caused by relabeling to the behavioral policy.

## Model Exploitation in Goal-conditioned HRL

The promises of model-based RL (MBRL) have been extensively discussed in past research [@moerland2023model]. The well-known model-based RL algorithm, Dyna [@sutton1991dyna], leveraged a dynamics model to generate one-step transitions and then update the value function using these imagined data, thus accelerating the learning. Recently, instantiating environment dynamics using an ensemble of probabilistic networks has become quite popular because of its ability to model both aleatory uncertainty and epistemic uncertainty [@chua2018deep]. Hence, a handful of Dyna-style methods proposed to simulate multi-step rollouts by using ensemble models, such as SLBO [@luo2019algorithmic] and MBPO [@janner2019trust]. Alternatively, the model-based value expansion methods performed multi-step simulation and estimated the future transitions using the Q-function, which helped to reduce the value estimation error. The representative algorithms include MVE [@feinberg2018model] and STEVE [@buckman2018sample]. Besides, in fact, the estimated value of states can directly provide gradients to the policy when the learned dynamic models are differentiable, like Guided Policy Search [@levine2013guided] and Imagined Value Gradients [@byravan2020imagined]. Our work differs from these works since we use the higher-level Q-function to estimate the value of future lower-level transitions. As stated in a recent survey [@a2023luo], there have been only a few works [@nair2020hierarchical; @zhu2021mapgo] involving the model exploitation in the goal-conditioned RL. To our knowledge, there is no prior work studying such inter-level planning.

# Methods

This section explains how our framework with Guided Cooperation via Model-based Rollout (GCMR) promotes inter-level cooperation. The GCMR involves three critical components: 1) the off-policy correction via model-based rollouts, 2) gradient penalty with a model-inferred upper bound, and 3) one-step rollout-based planning. Below, we detail the architecture of the dynamics model and such three critical components.

## Forward Dynamics Modeling

A bootstrapped ensemble of dynamics models is constructed to approximate the true transition dynamics of environment: $f(s_{t+1}|s_t,a_t)$, which has been demonstrated in several studies [@chua2018deep; @kurutach2018model; @janner2019trust; @shen2020model; @yu2020mopo; @yu2021combo]. We denote the dynamics approximators as $\Gamma_{\xi} = \{\hat{f}^1_{\xi}, \dots, \hat{f}^B_{\xi}\}$, where $B$ is the ensemble size and $\xi$ denotes the parameters of models. Each model of the ensemble projects the state $s_t$ conditioned on the action $a_t$ to a Gaussian distribution of the next state, i.e., $\hat{f}^b_{\xi}(s_{t+1}|s_t,a_t)=\mathcal{N}(\mu^b_{\xi}(s_t,a_t),\Sigma^b_{\xi}(s_t,a_t))$, with $b \in \{1,\dots,B\}$. In usage, a model is picked out uniformly at random to predict the next state. Note that, here, we do not learn the reward function because the compounding error from multi-step rollouts makes it infeasible for higher-level to infer the future cumulative rewards. As for the lower-level agent, the reward can be computed through the intrinsic reward function (see Equation [\[intrinsic_reward\]](#intrinsic_reward){reference-type="ref" reference="intrinsic_reward"}) on the fly. Finally, such dynamics models are trained via maximum likelihood and are incorporated to encourage inter-level cooperation and stabilize the policy optimization process.

## Off-Policy Correction via Model-based Rollouts

With well-trained dynamics models, we expand the vanilla off-policy correction in HIRO [@nachum2018data] by using the model-generated state transitions to bridge the gap between the past and current behavioral policies. Recall a stored high-level transition $\tau_{hi} = \left( \left \langle s_{t:t+c-1}, g \right \rangle, sg_{t:t+c-1}, r^{hi}_t, \left \langle s_{t+1:t+c}, g \right \rangle \right)$ in the replay buffer, which is converted into a state-action-reward transition: $\tau_{hi} = \left( \left \langle s_t, g \right \rangle, sg_t, r^{hi}_t, \left \langle s_{t+c}, g \right \rangle \right)$ during training. Relabeling either the cumulative rewards or the final state via $c$-step rollouts, resembling the FGI in MapGo [@zhu2021mapgo], substantially suffers from the high variance of long-horizon prediction. In essence, both the final state $s_{t+c}$ and the reward sequence $R_{t:t+c-1}$ are explicitly affected by the action sequence $a_{t:t+c-1}$. Hence, relabeling the $sg_t$, instead of the $s_{t+c}$ or $r^{hi}_t$, with an action sequence-based maximum likelihood is a promising way to improve sample efficiency. Following prior work [@nachum2018data], we consider the maximum likelihood-based action relabeling: $$\begin{equation}
\log \pi(a_{t:t+c-1}|s_{t:t+c-1},\tilde{sg}_{t:t+c-1};\theta_{lo}) \propto -\frac{1}{2} \sum^{i+c-1}_{i=t} \Vert a_i - \pi(s_i,\tilde{sg}_i;\theta_{lo}) \Vert^2_2+\rm{const}
\label{opc_hiro}
\end{equation}$$ Where $\tilde{sg}_t$ indicates the candidate subgoals sampled randomly from a Gaussian centered at $\varphi(s_{t+c})$. Meanwhile, the original goal $sg_t$ and the achieved state (in goal space) $\varphi(s_{t+c})$ are also taken into consideration. Specifically, according to Equation [\[opc_hiro\]](#opc_hiro){reference-type="ref" reference="opc_hiro"}, the current low-level policy performed $c$-step rollouts conditioned on these candidate subgoals. These sub-goals maximizing the similarity between original and rollout-based action sequences will be selected as optimal. Yet, we find that the current behavioral policy cannot produce the same action as in the past, so the $s_{t+1}$Therefore, the vanilla off-policy correction still suffers from the cumulative error due to the gap between the $s_{t+1:t+c}$ and the unknown transitions $\hat{s}_{t+1:t+c}$. In view of this fact, we roll out these transitions using the learned dynamics models $\Gamma_{\xi}$ to mitigate the issue. Besides, we employ an exponential weighting function along the time axis to highlight shorter rollouts and Then Equation [\[opc_hiro\]](#opc_hiro){reference-type="ref" reference="opc_hiro"} is rewritten as: $$\begin{equation}
\begin{aligned}
 &\log\pi(a_{t:t+c-1}|s_{t},\tilde{sg}_{t};\theta_{lo}) \propto -\mathbb{E}_{\hat{a}_{i}} \chdeleted{\rho^{i-t} }\cdot \Vert a_i-\hat{a}_i \Vert^2_2 +\rm{const} \\
 &\quad\text{s.t.} \quad \hat{a}_{i} \sim \pi(\hat{s}_{i}, \tilde{sg}_i;\theta_{lo}) ;\\ \chdeleted{\text{ and }} &\quad\quad\quad\hat{s}_{i+1} \sim \chadded{(1-\rho^{i-t})\cdot}\Gamma_{\xi}(\hat{s}_{i}, \hat{a}_{i}) \chadded{+ \rho^{i-t}\cdot{s}_{i+1}}
%&\text{s.t.} \left \{\begin{array}{lr} 
%\hat{a}_{i} \sim \pi(\hat{s}_{i}, \tilde{sg}_i;\theta_{lo}) \\
%\hat{s}_{i+1} \sim \Gamma_{\xi}(\hat{s}_{i}, \hat{a}_{i}) 
%\end{array} \right.
\end{aligned}
\end{equation}$$ Where $t \leq i \le t+c-1$ and $\hat{s}_{i}\big|_{i=t} = s_t$. $\rho \in \mathbb{R}$. $\rho \in \mathbb{R}$ is a hyper-parameter indicating the base of the exponential function, where in practice, we set $\rho$ to 0.95.

***Soft-Relabeling:*** Inspired by the pseudo-landmark shift of HIGL [@kim2021landmark], instead of an immediate overwrite, we use a soft mechanism to smoothly update subgoals: $$\begin{equation}
 sg_{t}\leftarrow  sg_{t} + \chreplaced{\delta_{sg}}{\delta_{g}}\frac{\Delta sg_{t}}{\Vert \Delta sg_{t} \Vert_2}; \qquad
%%%% \chreplaced{\delta_{sg}}{\delta_{g}} &\leftarrow \epsilon\chreplaced{\delta_{sg}}{\delta_{g}} + (1-\epsilon) \Vert \Delta sg_{t} \Vert_2 \\ 
\Delta sg_{t} := \tilde{sg}_t - sg_{t}
\end{equation}$$ Where $\chreplaced{\delta_{sg}}{\delta_{g}}$ represents the shift magnitude. The soft update is expected to be robust to outliers.

## Gradient Penalty with a Model-Inferred Upper Bound

Apparently, from the perspective of the lower-level policy, the subgoal relabeling implicitly brings in a distributional shift of observation. Specifically, these relabeled subgoals are sampled from the goal space but are not executed in practice. The behavioral policy is prone to produce unreliable actions under such an unseen or faraway goal, resulting in ineffective exploration. Motivated by , we pose the Lipschitz constraint on the Q-function gradients to stabilize the Q-learning of behavioral policy. To understand the effect of the gradient penalty, we highlight the property of the learned Q-function.

::: {#gradient_penalty .prop}
**Proposition 1**. *Let $\pi^*(a_t|s_t)$ and $r^*(s_t,a_t)$ be the policy and the reward function in an MDP. Suppose there are the upper bounds of Frobenius norm of the policy and reward gradients w.r.t. input actions, i.e., $\Vert \frac{\partial \pi^*(a_{t+1}|s_{t+1})}{\partial a_t}\Vert_F \leq L_{\pi} < 1$ and $\Vert \frac{\partial r^*(\chreplaced{s_{t}, a_{t}}{s_{t+1}, a_{t+1}})}{\partial a_t}\Vert_F \leq L_{r}$. Then the gradient of the learned Q-function w.r.t. action can be upper-bounded as: $$\begin{equation}
\Vert \nabla_{a_t}Q_{\pi^*}(s_t,a_t) \Vert_F \leq \frac{\sqrt{N}L_r}{1-\gamma L_{\pi}}
\end{equation}$$ Where $N$ denotes the dimension of the action and $\gamma$ is the discount factor.*
:::

::: proof
*Proof.* See the . ◻
:::

::: remark
**Remark 1**. *Proposition [1](#gradient_penalty){reference-type="ref" reference="gradient_penalty"} proposes a tight upper bound. A more conservative upper bound can be obtained by employing the inequality pertaining to $L_{\pi}$: $$\begin{equation}
\Vert \nabla_{a_t}Q_{\pi^*}(s_t,a_t) \Vert_F < (1-\gamma)^{-1} \sqrt{N} L_r
\end{equation}$$ Hence, a core challenge in the applications is how to estimate the upper bound of reward gradients w.r.t. input actions.*
:::

Now, we propose an approximate upper-bound approach grounded on the learned dynamics $\Gamma_{\xi}$. Fortunately, the lower-level reward function is specified in the form of L2 distance and is immune to environment stochasticity. Naturally, the upper bound of reward gradients w.r.t. input actions can be estimated as: $$\begin{equation}
\begin{aligned}
\hat{L}_r =& \sup \left \{ \Vert \nabla_{a_t} \Vert sg_{t+1} -  \eta \varphi ( s_{t+1} )\Vert_2 \Vert_F \right \}  \\
 &\text{s.t.}\quad s_{t+1} \in \mathcal{S}, sg_t \in \mathcal{G}, a_t \in \mathcal{A}
 \end{aligned}
\end{equation}$$ In practice, we approximate the upper bound using a mini-batch of lower-level observations independently sampled from the replay buffer $\mathcal{D}_{lo}$, yielding a tighter upper bound and, in turn, more forcefully penalizing the gradient: $$\begin{equation}
\begin{aligned}
\hat{L}_r \simeq& \max \left \{ \Vert \nabla_{a_t} \Vert sg_t+ \varphi(s_t-\Gamma_{\xi}(s_t,a_{t})) \right. \left. -  \eta \varphi (\Gamma_{\xi}(s_t,a_{t}) )\Vert_2 \Vert_F \right \} \\
 &\text{s.t.} \quad s_t, sg_t \sim \mathcal{D}_{lo} \text{ and } a_{t} \sim \pi(s_{t}, sg_t;\theta_{lo})
 \end{aligned}
\end{equation}$$ Then, following prior works [@gao2022robust], we plug the gradient penalty term into the lower-level Q-learning loss (see Equation [\[critic_loss\]](#critic_loss){reference-type="ref" reference="critic_loss"}), which can be formulated as: $$\begin{equation}
\begin{aligned}
\mathcal{L}_{gp}(\phi_{lo}) &= \lambda_{gp} \cdot \mathbb{E}_{s_t, sg_t}[{\rm ReLU}(\Vert \nabla_{a_t}Q_{\pi}(s_t, sg_t,a_t; \phi_{lo}) \Vert_F - (1-\gamma)^{-1}\sqrt{N} \cdot \hat{L}_r)]^2 \\
&\text{s.t.} \quad s_t, sg_t \sim \mathcal{D}_{lo} \text{ and } a_{t} \sim \pi(s_{t}, sg_t;\theta_{lo})
\end{aligned}
\end{equation}$$ Where $\lambda_{gp}$ is a hyper-parameter controlling the effect of the gradient penalty term. Because the gradient penalty enforces the Lipschitz constraint on the critic, limiting its update, we had to increase the number of critic training iterations to 5, a recommended value in WGAN-GP [@gulrajani2017improved], per actor iteration. Considering the computational efficiency, we apply the gradient penalty every 5 training steps.

## One-Step Rollout-based Planning

::: wrapfigure
r0.5 ![image](Wang2023Guided_figs/osrp_workflow.png){width="50%"}
:::

In a flat model-based RL framework, model-based value expansion-style methods [@feinberg2018model; @buckman2018sample] use dynamics models to simulate short rollouts and evaluate future transitions using the Q-function. Here, we steer the behavioral policy towards globally valuable states, i.e., having a higher higher-level Q-value. Specifically, we perform a one-step rollout and evaluate the next transition using the higher-level critics. The objective is to minimize the following loss: $$\begin{equation}
\begin{aligned}
\mathcal{L}_{osrp} =& -\lambda_{osrp}\cdot\\ 
&\mathbb{E}_{s_t, g, sg_t}\left[Q(\Gamma_{\xi}(s_t, a_t),g,sg_{t+1};\phi_{hi}) \right]\\
&\text{s.t.} \qquad s_t \in \mathcal{S} \\
&\text{\quad} \qquad g, sg_t \in \mathcal{G}  \\ 
&\text{\quad}\qquad a_{t} \sim \pi(s_{t}, sg_t;\theta_{lo}))
\end{aligned}
\label{osrp_1}
\end{equation}$$ Where $\lambda_{osrp}$ is a hyper-parameter to weigh the planning loss. Note that the $sg_t$ is not determined by higher-level policy solely. Meanwhile, considering that the higher-level policy is also changing over time, the $sg_t$ is sampled randomly from a Gaussian distribution centered at $\pi(s_{t}, g;\theta_{hi})$. In practice, a pool of $s_t$ and $g$ is sampled from the buffer $\mathcal{D}_{hi}$, and then they are repeated ten times with shuffling the $g$. Next, these samples are duplicated again to accommodate the variance of $sg_t$. On the other hand, the next step's subgoal $sg_{t+1}$ is also produced by the fixed goal transition function or by the higher-level policy conditioning on the observation. But, from the perspective of lower-level policy, the probability of such two events is equal because of the property of Markov decision process, i.e., $$\begin{equation}
Pr\{sg_{t+1}=h\left(sg_{t},s_{t},s_{t+1}\right)|s_t, sg_t, a_t\} = Pr\{sg_{t+1}=\pi(s_t,g;\theta_{hi})|s_t, sg_t, a_t\} = 0.5
\end{equation}$$ Hence, the Equation [\[osrp_1\]](#osrp_1){reference-type="ref" reference="osrp_1"} is instantiated: $$\begin{equation}
\begin{aligned}
&\mathcal{L}_{osrp} \\
&= -\lambda_{osrp} \cdot \mathbb{E}_{s_t, g, sg_t \atop sg_{t+1} \in \{h, \pi(\theta_{hi})\}} Q(\Gamma_{\xi}(s_t, a_t),g,sg_{t+1};\phi_{hi}) \\
&= -\frac{1}{2}\lambda_{osrp} \cdot \mathbb{E}_{s_t, g, sg_t} \left[Q(\Gamma_{\xi}(s_t, a_t),g,h;\phi_{hi}) \right.+ \underbrace{\left. Q(\Gamma_{\xi}(s_t, a_t),g,\pi(\theta_{hi});\phi_{hi}) \right] }_{\textcircled{a}} \\
 &\text{s.t.} \quad s_t, g, sg_t \sim \mathcal{D}_{hi} \text{ and } a_{t} \sim \pi(s_{t}, sg_t;\theta_{lo})
 \end{aligned}
\end{equation}$$

Obviously, the second term $\textcircled{a}$ is too dependent on current higher-level policy. The TD3 [@fujimoto2018addressing] seeks to smoothen the value estimate by bootstrapping off of nearby state-action pairs. Similarly, we add clipped noise to keep the value estimate robust. This makes our modified term $\textcircled{a}$: $$\begin{equation}
\begin{aligned}
\textcircled{a} := Q(&\Gamma_{\xi}(s_t, a_t),g,\pi(\theta_{hi})+\varepsilon;\phi_{hi}) \\
{\rm with} \quad \varepsilon & \sim {\rm clip}(\mathcal{N}(0,\sigma), -a_c, a_c)
 \end{aligned}
\end{equation}$$ Where the hyper-parameters $\sigma$ and $a_c$ are common in the TD3 algorithm (see Equation [\[critic_loss_q\]](#critic_loss_q){reference-type="ref" reference="critic_loss_q"}). In the end, $\mathcal{L}_{osrp}$ is incorporated into lower-level actor loss (see Equation [\[actor_loss\]](#actor_loss){reference-type="ref" reference="actor_loss"}) to guide the lower-level policy towards valuable highlands with respect to the overall task. Here, in the same way, we employ the one-step rollout-based planning every 10 training steps.

# Experiments

We evaluated the proposed GCMR on challenging continuous control tasks, as shown in Fig. [2](#environments){reference-type="ref" reference="environments"}. Specifically, the following simulated robotics environments are considered:

- Point Maze [@kim2021landmark]: In this environment, a simulated ball starts at the bottom left corner and navigates to the top left corner in a '$\sqsupset$'-shaped corridor.

- Ant Maze (W-shape) [@kim2021landmark]: In a '$\exists$'-shaped corridor, a simulated ant starts from a random position and must navigate to the target location at the middle left corner.

- Ant Maze (U-shape) [@nachum2018data; @kim2021landmark], Stochastic Ant Maze (U-shape) [@zhang2020generating; @zhang2022adjacency], and Large Ant Maze (U-shape): A simulated ant starts at the bottom left corner in a '$\sqsupset$'-shaped corridor and seeks to reach the top left corner. As for the randomized variation, *Stochastic* Ant Maze (U-shape) introduces environmental stochasticity by replacing the agent's action at each step with a random action (with a probability of 0.25).

- Ant Maze-Bottleneck [@leed2022hrl]: The environment is almost the same as the Ant Maze (U-shape). Yet, in the middle of the maze, there is a very narrow bottleneck so that the ant can barely pass through it.

- Pusher [@kim2021landmark]: A 7-DOF robotic arm is manipulated into pushing a (puck-shaped) object on a plane to a target position.

- Reacher [@kim2021landmark]:

:::: {#environments .figure latex-placement="htbp"}
\

::: caption
Environments used in our experiments. In the maze-related tasks, the goal in each task is marked with a red arrow, and the black line represents a possible trajectory from the current state to the goal.
:::
::::

These general '$\sqsupset$'-shaped mazes have the same size of $12 \times 12$ while $20 \times 20$ is for the '$\exists$'-shaped maze. Besides, the size of the *Large* Ant Maze (U-shape) is twice as large as that of the general Ant Maze (U-shape), i.e., 24 × 24.

- 
- 

Further environment details are available in the \"Supplementary Materials\".

## Hyper-parameters in *ACLG* {#sec:hyperparams_aclg}

First, we conduct experiments on Ant Maze (U-shape) to explore the effect of hyper-parameters in ACLG: (1) the number of landmarks and (2) the balancing coefficient $\lambda^{\rm ACLG}_{\rm landmark}$.

:::: {.figure latex-placement="htbp"}
::: caption
Ablation studies on landmark-related components. We measure the performance of ACLG by (a) varying number of landmarks and (b) varying balancing coefficient $\lambda^{\rm ACLG}_{\rm landmark}$ in Ant Maze (U-shape).
:::
::::

#### Landmark Number Selection

Since the number of landmarks plays an important role in the graph-related method, we explored the effects of different numbers of landmarks on performance. Here, we sample the same number of landmarks for each criterion, i.e., the same number for novelty-based and novelty-based landmarks ${LM}^{\rm \chreplaced{cov}{nov}}={LM}^{\rm nov}$. As shown in Fig. , overall, the ACLG significantly outperforms the HIGL since the disentanglement between the adjacency constraint and landmark-based planning further highlights the advantages of landmarks. Finally, the setting ${LM}^{\rm \chreplaced{cov}{nov}}={LM}^{\rm nov}=60$ was adopted for further analysis.

#### Balancing Coefficient $\lambda^{\rm ACLG}_{\rm landmark}$

In Fig. , we investigate the effectiveness of the balancing coefficient $\lambda^{\rm ACLG}_{\rm landmark}$, which determines the effect of the landmark-based planning term in ACLG on performance. We find that ACLG with $\lambda^{\rm ACLG}_{\rm landmark}=1.0$ outperforms others. Moreover, ACLG with $\lambda^{\rm ACLG}_{\rm landmark}\in\{1.0, 10\}$ outperforms that with $\lambda^{\rm ACLG}_{\rm landmark}=0.1$, which shows a large value of $\lambda^{\rm ACLG}_{\rm landmark}$ helps unleash the guiding role of landmarks.

##  {#sec:hyperparams_gcmr}

####  {#section-1}

:::: {#goal_shift .figure latex-placement="htbp"}
\

::: caption
:::
::::

####  {#section-2}

:::: {#mgp_lambda .figure latex-placement="htbp"}
::: caption
:::
::::

:::: {#osrp_lambda .figure latex-placement="htbp"}
::: caption
:::
::::

####  {#section-3}

## Comparative Experiments

To validate the effectiveness of the GCMR, we plugged it into the ACLG, the disentangled variant of HIGL, and then compared the performance of the integrated framework with that of ACLG, HIGL [@kim2021landmark], HRAC [@zhang2020generating], DHRL [@leed2022hrl], as well as the PIG [@kim2022imitating]. Note that the numbers of landmarks used in these methods are different. In most tasks, HIGL employed 40 landmarks, ACLG used landmarks, DHRL utilized 300 landmarks, and PIG employed 400 landmarks (see Table 3 in the \"Supplementary Materials\" for details). This is in line with prior works. Also, consistent with prior research, our experiments were performed on the above-mentioned environments with *sparse* reward settings, where the agent will obtain no reward until it reaches the target area.

::: wrapfigure
r0.5 ![image](Wang2023Guided_figs/AntMaze-v1_dense.png){width="50%"} []{#landmark_num label="landmark_num"}
:::

But we also present a discussion about dense experiments based on AntMaze (U-shape), as shown in Fig. [\[dense_compare\]](#dense_compare){reference-type="ref" reference="dense_compare"}. Note that the comparison on dense reward setting did not involve DHRL and PIG due to the scope and limitations of their applicability. In the implementation, we did not use the learned dynamics model until we had sufficient transitions for sampling, which would avoid a catastrophic performance drop arising from inaccurate planning. It means that our method was enabled only if the step number of interactions was over a pre-set value. Here, the time step limit was set to $20K$ for maze-related tasks and $10K$ for robotic arm manipulation. After that, the dynamics model was trained at a frequency of $D$ steps. In the end, we evaluate their performance over 5 random seeds , conducting 10 test episodes every $5K^{\rm th}$ time step. All of the experiments were carried out on a computer with the configuration of Intel(R) Xeon(R) Gold 5220 CPU @ 2.20GHz, 8-core, 64 GB RAM. And each experiment was processed using a single GPU (Tesla V100 SXM2 32 GB). We provide more detailed experimental configurations in the \"Supplementary Materials\".

####  {#section-4}

:::: {#subgoal_generate .figure latex-placement="htbp"}
\

::: caption
:::
::::

#### Comparison results

As shown in Fig. [7](#compare_results){reference-type="ref" reference="compare_results"}, GCMR contributes to achieving better performance and shows resistance to performance degradation. By integrating the GCMR with ACLG, we find that the proposed method outperforms the prior SOTA methods in almost all tasks. Especially in complicated tasks requiring meticulous operation (e.g., Ant Maze-Bottleneck, *Stochastic* Ant Maze, and *Large* Ant Maze), our method steadily improved the policy without getting stuck in local optima. , as shown in Fig. , , , , , [\[maze_point\]](#maze_point){reference-type="ref" reference="maze_point"}, , our method achieved a faster asymptotic convergence rate than others. There was no catastrophic failure. ur method slightly trailed behind the PIG, it still achieved the second-best performance. Moreover, in Fig. [\[dense_compare\]](#dense_compare){reference-type="ref" reference="dense_compare"}, we investigated the performance of the proposed method in the *Dense*-reward environment, i.e., Ant Maze (*Dense*, U-shape). The results demonstrate the GCMR is also effective and significantly improves the performance of ACLG. To verify whether GCMR can be solely applied to goal-reaching tasks, we conducted experiments in the Point Maze and Ant Maze (U-shape) tasks. From the experimental results depicted in Fig. 1 in the \"Supplementary Materials\", it can be observed that the GCMR can be used independently and achieve similar results to HIGL.

:::: {#compare_results .figure latex-placement="!ht"}
\
\

::: caption
The average success rate of multiple comparison methods on a set of *Sparse*-reward environments. The solid lines represent the mean across five runs.
:::
::::

#### Comparison to existing goal-relabeling

To justify the superiority of over the others. We compared it with various goal-relabeling technologies: (a) vanilla off-policy correction in HIRO [@nachum2018data], (b) hindsight-based goal-relabeling in HAC [@levy2019learning], and (c) foresight goal inference in MapGo [@zhu2021mapgo], which is a model-based variant of vanilla hindsight-based goal-relabeling.

:::: {#relabel .figure latex-placement="!ht"}
![](Wang2023Guided_figs/AntMaze-v1_sparse_relabel.png){width="70%"}

::: caption
Figure compares the performance of different relabeling technologies on Ant Maze (U-shape). .
:::
::::

## Ablation study

####  {#section-5}

Considering that the number of lower-level critic training iterations was increased to alleviate the impact of the gradient penalty, we additionally provide a comprehensive analysis concerning the effects of increased iterations on various alternative methods. As depicted in Fig. [9](#crit5){reference-type="ref" reference="crit5"}, increasing the number of critic training iterations led to improved performance when compared to the original approach. Moreover, even without increasing the training iterations, ACLG+GCMR consistently outperformed other methods and overtook the ACLG with increased training iterations after several timesteps. The results demonstrate that the can enhance the robustness of HRL frameworks and prevent falling into local pitfalls.

:::: {#crit5 .figure latex-placement="htbp"}
![](Wang2023Guided_figs/AntMazeComplex-v1_sparse_crit5.png){width="62%"}

::: caption
We investigate the impact of increased training iterations for critic on various HRL methods in the Ant Maze (U-shape) environment, where \"5-train\" indicates that the number of training iterations of lower-level critic network is increase to 5.
:::
::::

####  {#section-6}

:::: {#weights_actor_gp .figure latex-placement="htbp"}
\

::: caption
:::
::::

:::: {#mgp_abs .figure latex-placement="!htbp"}
\

::: caption
:::
::::

####  {#section-7}

:::: {#osrp_abs .figure latex-placement="htbp"}
\

::: caption
:::
::::

:::: {#osrp_abs_traj .figure latex-placement="htbp"}
\

::: caption
:::
::::

# Discussion {#Discussion}

##  {#section-8}

##  {#section-9}

##  {#section-10}

This study has certain limitations. First, our experiments show that the GCMR achieved significant performance improvement, and such improvement came at the expense of more computational cost (see Table 4 in the \"Supplementary Materials\" for a quantitative analysis of computational cost). However, the time-consuming issue only occurs during the training stage and will not affect the execution response time in the applications. Second, we need to clarify that the scope of applicability is off-policy goal-conditioned HRL. The effectiveness in general RL tasks or online tasks . Third, the experimental environments used in this study have 7 or 30 dimensions. Our network architecture of transition dynamics models is relatively simple, leading to limited regression capability. Applications in complex environments that closely resemble real-world scenarios with high-dimensional observation, like the large-scale point cloud environments encountered in autonomous driving, might face limitations. This issue will be investigated in our future work.

# Conclusion {#Conclusion}

This study proposes a new goal-conditioned HRL framework with Guided Cooperation via Model-based Rollout (GCMR), which uses the learned dynamics as a bridge for inter-level cooperation. Experimentally we instantiated several cooperation and communication mechanisms to improve the stability of hierarchy, achieving both data efficiency and learning efficiency. To our knowledge, very few prior works have discussed the model exploitation problem in goal-conditioned HRL. This research not only provides a SOTA HRL algorithm but also demonstrates the potential of integrating the learned dynamics model into goal-conditioned HRL, which is expected to draw the attention of researchers to such a direction.

# Lipschitz Property of the Q-function w.r.t. action {#sec:mgp_proof}

In this appendix, we provide a brief proof for **Proposition 1**. More detailed proof can be found in . We start out with a lemma that helps with subsequent derivation.

::: {#lemma:1 .lemma}
**Lemma 1**. *Assume policy gradients w.r.t. input actions in an MDP admit a bound at any time $t$: $\Vert \frac{\partial \pi^*(a_{t+1}|s_{t+1})}{\partial a_t}\Vert_F \leq L_{\pi}$. Then the following holds for any non-negative integer $c$ and $t$: $$\begin{equation}
\begin{aligned}
\big\vert \nabla_{a_t} &\mathbb{E}_{s_{t+c}|s_t}[r^*(s_{t+c}, a_{t+c})]\big\vert \\
&\leq L_{\pi} \mathbb{E}_{s_{t+c}|s_t} \big\vert \nabla_{a_{t+1}} \mathbb{E}_{s_{t+c}|s_{t+1}}[r^*(s_{t+c}, a_{t+c})]\big\vert
\end{aligned}
\end{equation}$$*
:::

::: proof
*Proof.* $$\begin{equation}
\begin{aligned}
&\big\vert \nabla_{a_t} \mathbb{E}_{s_{t+c}|s_t}[r^*(s_{t+c}, a_{t+c})] \\ & \quad= \big\vert \nabla_{a_t} \mathbb{E}_{s_{t+1}|s_t} \mathbb{E}_{s_{t+c}|s_{t+1}}[r^*(s_{t+c}, a_{t+c})]\cdot \frac{\partial a_{t+1}}{\partial a_{t}} \big\vert \\
&\quad\leq \big\vert \nabla_{a_t} \mathbb{E}_{s_{t+1}|s_t} \mathbb{E}_{s_{t+c}|s_{t+1}}[r^*(s_{t+c}, a_{t+c})] \big\vert \cdot \big\vert \frac{\partial a_{t+1}}{\partial a_{t}} \big\vert \\
&\quad\leq \big\vert \nabla_{a_t} \mathbb{E}_{s_{t+1}|s_t} \mathbb{E}_{s_{t+c}|s_{t+1}}[r^*(s_{t+c}, a_{t+c})] \big\vert \cdot L_{\pi} \\
&\quad= \mathbb{E}_{s_{t+1}|s_t} \big\vert \nabla_{a_t} \mathbb{E}_{s_{t+c}|s_{t+1}}[r^*(s_{t+c}, a_{t+c})] \big\vert \cdot L_{\pi}
\end{aligned}
\end{equation}$$ ◻
:::

::: {#remark:1 .remark}
**Remark 2**. *Lemma [1](#lemma:1){reference-type="ref" reference="lemma:1"} gives the discrepancy of reward gradients starting from adjacent states. We can apply this lemma sequentially and infer the upper bound of reward gradients: $$\begin{equation}
\begin{aligned}
&\big\vert \nabla_{a_t} \mathbb{E}_{s_{t+c}|s_t}[r^*(s_{t+c}, a_{t+c})]\big\vert \\
&= \big\vert \nabla_{a_t} \mathbb{E}_{s_{t+1}|s_t} \mathbb{E}_{s_{t+c}|s_{t+1}}[r^*(s_{t+c}, a_{t+c})]\cdot \frac{\partial a_{t+1}}{\partial a_{t}} \big\vert \\
&\leq \mathbb{E}_{s_{t+1}|s_t} \big\vert \nabla_{a_t} \mathbb{E}_{s_{t+c}|s_{t+1}}[r^*(s_{t+c}, a_{t+c})] \big\vert \cdot L_{\pi} \\
&\leq \mathbb{E}_{s_{t+1}|s_t} \mathbb{E}_{s_{t+2}|s_{t+1}} \dots \mathbb{E}_{s_{t+c}|s_{t+c-1}} \\
&\qquad\qquad\qquad \big\vert \nabla_{a_t} \mathbb{E}_{s_{t+c}|s_{t+c}}[r^*(s_{t+c}, a_{t+c})] \big\vert \cdot (L_{\pi})^c \\
&= \mathbb{E}_{s_{t+c}|s_t} \big\vert \nabla_{a_t} r^*(s_{t+c}, a_{t+c}) \big\vert \cdot (L_{\pi})^c
\end{aligned}
\end{equation}$$*
:::

::: prop
**Proposition 2**. *Let $\pi^*(a_t|s_t)$ and $r^*(s_t,a_t)$ be the policy and the reward function in an MDP. Suppose there are the upper bounds of Frobenius norm of the policy and reward gradients w.r.t. input actions, i.e., $\Vert \frac{\partial \pi^*(a_{t+1}|s_{t+1})}{\partial a_t}\Vert_F \leq L_{\pi} < 1$ and $\Vert \frac{\partial r^*(\chreplaced{s_{t}, a_{t}}{s_{t+1}, a_{t+1}})}{\partial a_t}\Vert_F \leq L_{r}$. Then the gradient of the learned Q-function w.r.t. action can be upper-bounded as: $$\begin{equation}
\Vert \nabla_{a_t}Q_{\pi^*}(s_t,a_t) \Vert_F \leq \frac{\sqrt{N}L_r}{1-\gamma L_{\pi}}
\end{equation}$$ Where $N$ denotes the dimension of the action and $\gamma$ is the discount factor.*
:::

::: proof
*Proof.* $$\begin{equation}
\begin{aligned}
\Vert \nabla_{a_t}&Q_{\pi^*}(s_t,a_t) \Vert^2_F \\
&= \sum_{i=0}^N\left(\nabla_{a^i_t}Q_{\pi^*}(s_t,a_t)\right)^2 \\
&=\sum_{i=0}^N\left(\sum_{c=0}^{\infty}\gamma^c \nabla_{a^i_t} \mathbb{E}_{s_{t+c}|s_t}[r^*(s_{t+c}, a_{t+c})]\right)^2 \\
&\leq \sum_{i=0}^N\left(\sum_{c=0}^{\infty}\gamma^c \big\vert \nabla_{a^i_t} \mathbb{E}_{s_{t+c}|s_t}[r^*(s_{t+c}, a_{t+c})]\big\vert\right)^2
\end{aligned}
\label{proof:2}
\end{equation}$$ Meanwhile according to Remark [2](#remark:1){reference-type="ref" reference="remark:1"}, we have: $$\begin{equation}
\begin{aligned}
\big\vert \nabla_{a_t}& \mathbb{E}_{s_{t+c}|s_t}[r^*(s_{t+c}, a_{t+c})]\big\vert \\
&\leq \mathbb{E}_{s_{t+c}|s_t} \big\vert \nabla_{a^i_t} r^*(s_{t+c}, a_{t+c}) \big\vert \cdot (L_{\pi})^c \\
&\leq \mathbb{E}_{s_{t+c}|s_t} L_r \cdot (L_{\pi})^c\\
&=L_r \cdot (L_{\pi})^c
\end{aligned}
\end{equation}$$ Replacing the above gradient term, then the formula ([\[proof:2\]](#proof:2){reference-type="ref" reference="proof:2"}) can be rewritten as: $$\begin{equation}
\begin{aligned}
\Vert \nabla_{a_t}&Q_{\pi^*}(s_t,a_t) \Vert^2_F \\
&\leq \sum_{i=0}^N\left(\sum_{c=0}^{\infty}\gamma^c \big\vert \nabla_{\chreplaced{a_t^i}{a_t}} \mathbb{E}_{s_{t+c}|s_t}[r^*(s_{t+c}, a_{t+c})]\big\vert\right)^2 \\
&\leq \sum_{i=0}^N\left(\sum_{c=0}^{\infty}\gamma^c \cdot L_r \cdot L_{\pi}^c\right)^2 = 
N \left(L_r\sum_{c=0}^{\infty}(\gamma \cdot L_{\pi})^c\right)^2 \\
&= N \left(\frac{L_r}{1-\gamma L_{\pi}} \right)^2
\end{aligned}
\end{equation}$$ The above inequality on the sqrt function then implies: $$\begin{equation}
\begin{split}
\Vert \nabla_{a_t}Q_{\pi^*}(s_t,a_t) \Vert_F \leq \frac{\sqrt{N}L_r}{1-\gamma L_{\pi}}
\end{split}
\end{equation}$$ Which completes the proof. ◻
:::

# Algorithm table

We provide the pseudo code below for this algorithm. Python-based implementation is available at <https://github.com/HaoranWang-TJ/GCMR_ACLG_official>.

:::: algorithm
::: algorithmic
**Input:**\

- **Key hyper-parameters**: the number of candidate goals $k$, gradient penalty loss coefficient $\lambda_{gp}$, one-step planning term coefficient$\lambda_{osrp}$, soft update rate of the shift magnitude within relabeling $\epsilon$.

- **General hyper-parameters**: the subgoal scheme $\eta$ (set to 0/1 for the relative/absolute scheme), training batch number $BN$, higher-level update frequency $H_c$, learning frequency of dynamics models $D_c$, initial steps without using dynamics models $t_{dm}$, usage frequencies of gradient penalty and planning term $GP_c$, $OP_c$.

Initialize all actor and critic networks with random parameters $\theta_{lo}$, $\theta_{hi}$, $\phi_{lo}$, $\phi_{hi}$. Initialize the dynamics models $\Gamma_{\xi}$. $\mathcal{D}_{lo} \gets \emptyset$, $\mathcal{D}_{hi} \gets \emptyset$ $t \gets 0$ Reset the environment and get the state $s_t$ and episode terminal signal $done$. Generate subgoal $sg_t \sim \pi \left(sg|s_t, g;\theta_{hi}\right)$. Obtain through the transition function $sg_t = sg_{t-1} + (\neg\eta) \cdot \varphi(s_{t-1} - s_t)$. $a_t \sim \pi \left(a|s_t,sg_t;\theta_{lo}\right)$ $s_{t+1}$, $r_t$ $\gets {\rm env.step}(a_t)$\
$\mathcal{D}_{lo} \gets \mathcal{D}_{lo} \cup\{\tau_{lo}\}$, $\mathcal{D}_{hi} \gets \mathcal{D}_{hi} \cup\{\tau_{hi}\}$\
$t \gets t + 1$

Train the dynamics models $\Gamma_{\xi}$.

Randomly sample experiences from replay buffers. Relabel subgoals via the rollout-based off-policy correction.

$\mathcal{L}(\phi_{lo}) \gets \mathcal{L}_{gp}(\phi_{lo}) + \mathcal{L}(\phi_{lo})$\
$\mathcal{L}(\theta_{lo})  \gets \mathcal{L}_{osrp} + \mathcal{L}(\theta_{lo})$\
:::
::::

# Environment Details {#sec:environment_setting}

Most experiments were conducted under the same environments as that in [@kim2021landmark], including ***Point Maze***, ***Ant Maze (W-shape)***, ***Ant Maze (U-shape)***, ***Pusher***, and ***Reacher***. Further detail is available in public repositories [^3] [^4]. Besides, we introduced a more challenging locomotion environment, i.e., Ant Maze-Bottleneck, to validate the stability and robustness of the proposed GCMR in long-horizon and complicated tasks requiring delicate controls.

#### Ant Maze-Bottleneck

The Ant Maze-Bottleneck environment was first introduced in [@leed2022hrl], which provided implementation details in public repositories in [^5]. In this study, we resized it to be the same as the other mazes. Specifically, the size of the environment is $12 \times 12$. At training time, a goal point was selected randomly from a two-dimensional planar where both $x$- and $y$-axes range from -2 to 10. At evaluation time, the goal was placed at (0, 8) (i.e., the top left corner). A minimum threshold of competence was set to an L2 distance of 2.5 from the goal. Each episode would be terminated after 600 steps.

# Experimental Configurations

## Network Structure

For a fair comparison, we adopted the same architecture as [@zhang2020generating; @kim2021landmark]. In detail, all actor and critic networks had two hidden layers composed of a fully connected layer with 300 units and a ReLU nonlinearity function. The output layer in actor networks had the same number of cells as the dimension of the action space and normalized the output to $[-1, 1]$ using the $tanh$ function. After that, the output was rescaled to the range of action space.

For the dynamics model, the ensemble size $B$ was set to 5, a recommended value in [@chua2018deep]. Each of the ensembles was instantiated with three layers, similar to the above actor network. Yet, each hidden layer had 256 units and was followed by the Swish activation [@ramachandran2018searching]. Note that units of the output layer were twice as much as the actor because the action distribution was represented with the mean and covariance of a Gaussian.

The Adam optimizer was utilized for all networks.

## Hyper-Parameter Settings {#sec:params_setting}

In Table [1](#table:1){reference-type="ref" reference="table:1"}, we list common hyper-parameters used across all environments. Hyper-parameters that differ across the environments are presented in Table [2](#table:2){reference-type="ref" reference="table:2"}. These hyper-parameters involving HIGL remained the same as proposed by [@kim2021landmark]. Besides, the update speed of the shift magnitude of goals was set at 0.01.

::::: threeparttable
::: {#table:1}
+-------------------------------------+------------------------------------------------------------+
| Hyper-parameters                    | Value                                                      |
+:===================================:+:===========================:+:============================:+
| 2-3                                 | Higher-level                | Lower-level                  |
+-------------------------------------+-----------------------------+------------------------------+
| Actor learning rate                 | 0.0001                      | 0.0001                       |
+-------------------------------------+-----------------------------+------------------------------+
| Critic learning rate                | 0.001                       | 0.001                        |
+-------------------------------------+-----------------------------+------------------------------+
| Soft update rate                    | 0.005                       | 0.005                        |
+-------------------------------------+-----------------------------+------------------------------+
| $\gamma$                            | 0.99                        | 0.95                         |
+-------------------------------------+-----------------------------+------------------------------+
| Reward scaling                      | 0.1                         | 1.0                          |
+-------------------------------------+-----------------------------+------------------------------+
| Training frequency $H_c$            | 10                          | 1                            |
+-------------------------------------+-----------------------------+------------------------------+
| Batch size                          | 128                         | 128                          |
+-------------------------------------+-----------------------------+------------------------------+
| Candidates' number                  | 10                          |                              |
+-------------------------------------+-----------------------------+------------------------------+
| $\lambda^{\rm ACLG}_{\rm landmark}$ | 1.0                         |                              |
+-------------------------------------+-----------------------------+------------------------------+
| Shift Magnitude $\delta_{sg}$       | 20$\sim$`<!-- -->`{=html}30 |                              |
+-------------------------------------+-----------------------------+------------------------------+
| $\lambda_{gp}$                      |                             | 1.0$\sim$`<!-- -->`{=html}10 |
+-------------------------------------+-----------------------------+------------------------------+
| $\lambda_{osrp}$                    |                             | 0.0005 $\sim$ 0.00005        |
+-------------------------------------+-----------------------------+------------------------------+
|                                     |                             |                              |
+-------------------------------------+-----------------------------+------------------------------+
| $GP_c$                              |                             | 5                            |
+-------------------------------------+-----------------------------+------------------------------+
|                                     |                             |                              |
+-------------------------------------+-----------------------------+------------------------------+
| $OP_c$                              |                             | 10                           |
+-------------------------------------+-----------------------------+------------------------------+
|                                     | Dynamics model                                             |
+-------------------------------------+------------------------------------------------------------+
| Ensemble number                     | 5                                                          |
+-------------------------------------+------------------------------------------------------------+
| Learning rate                       | 0.005                                                      |
+-------------------------------------+------------------------------------------------------------+
| Batch size                          | 256                                                        |
+-------------------------------------+------------------------------------------------------------+
| Training epochs                     | 20 $\sim$ 50                                               |
+-------------------------------------+------------------------------------------------------------+

: Hyper-parameters across all environments.
:::

::: tablenotes
$\delta_{sg}$ is set to 20 for small mazes, such as Ant Maze (U-shape, W-shape), and 30 for larger mazes, such as the Large Ant Maze (U-shape).

Only $\lambda_{gp}=10$ for the Ant Maze-Bottleneck, while $\lambda_{gp}$ are set to 1.0 for others.

Only $\lambda_{osrp}=0.00005$ for the FetchPush and FetchPickAndPlace, while $\lambda_{osrp}$ are set to 0.0005 for others.
:::
:::::

::::: threeparttable
::: {#table:2}
+----------------------------------+------------+-----------+
| Hyper-parameters                 | Maze-based | Arm-based |
+:================================:+:==========:+:=========:+
| 2-3                              | Higher-level           |
+----------------------------------+------------+-----------+
| High-level action frequency      | 10         | 5         |
+----------------------------------+------------+-----------+
| Exploration strategy             |            |           |
+----------------------------------+------------+-----------+
| ($\sigma=1.0$)                   |            |           |
+----------------------------------+------------+-----------+
| ($\sigma=0.2$)                   |            |           |
+----------------------------------+------------+-----------+
|                                  | Lower-level            |
+----------------------------------+------------+-----------+
| Exploration strategy             |            |           |
+----------------------------------+------------+-----------+
| ($\sigma=1.0$)                   |            |           |
+----------------------------------+------------+-----------+
| ($\sigma=0.1$)                   |            |           |
+----------------------------------+------------+-----------+
| $\lambda_{\rm adj}$              | 20.0       | 0         |
+----------------------------------+------------+-----------+
|                                  | Dynamics model         |
+----------------------------------+------------+-----------+
| Training frequency $D_c$         | 2000       | 500       |
+----------------------------------+------------+-----------+
| Initial steps w/o model $t_{dm}$ | 20000      | 10000     |
+----------------------------------+------------+-----------+

: Hyper-parameters that differ across the environments.
:::

::: tablenotes
Maze-based environments include the Point Maze, Ant Maze (U/W-shape), and Ant Maze-Bottleneck.

Arm-based environments are the Pusher, Reacher, FetchPush, and FetchPickAndPlace.
:::
:::::

::::: threeparttable
::: {#table:landmark_num}
+--------------------+--------------+--------------+--------------------------+------+-----+
| Environments       | GCMR$+$ACLG  | ACLG         | HIGL                     | DHRL | PIG |
+:==================:+:============:+:============:+:========================:+:====:+:===:+
| Ant Maze (U-shape) | 60$+$`<!-- -->`{=html}60    | 20$+$`<!-- -->`{=html}20 | 300  | 400 |
+--------------------+-----------------------------+--------------------------+------+-----+
| Ant Maze (W-shape) | 60$+$`<!-- -->`{=html}60    | 60$+$`<!-- -->`{=html}60 | 300  | 400 |
+--------------------+-----------------------------+--------------------------+------+-----+
| Point Maze         | 60$+$`<!-- -->`{=html}60    | 20$+$`<!-- -->`{=html}20 | 300  | 200 |
+--------------------+-----------------------------+--------------------------+------+-----+
| Pusher and Reacher | 20$+$`<!-- -->`{=html}20    | 20$+$`<!-- -->`{=html}20 | 300  | 80  |
+--------------------+--------------+--------------+--------------------------+------+-----+
|                    |              |              |                          |      |     |
+--------------------+--------------+--------------+--------------------------+------+-----+
| FetchPickAndPlace  | 60$+$`<!-- -->`{=html}60    | 20$+$`<!-- -->`{=html}20 | 300  | 80  |
+--------------------+-----------------------------+--------------------------+------+-----+

: Number of Landmarks
:::

::: tablenotes
Where $+$ connects the numbers of coverage-based landmarks and novelty-based landmarks.
:::
:::::

# Additional Experiments

## GCMR Solely Employed for Goal-Reaching Tasks {#sec:gcmr_sole}

In our experiments, the proposed GCMR was used as an additional plugin. Of course, GCMR can be solely applicable to goal-reaching tasks. We conducted experiments in the Point Maze and Ant Maze (U-shape) tasks. As shown in Figure [14](#gcmr_sole){reference-type="ref" reference="gcmr_sole"}, the results indicate that GCMR can be used independently and achieve similar results to HIGL. Meanwhile, in Figure [15](#gcmr_sole_params){reference-type="ref" reference="gcmr_sole_params"}, we investigate how the gradient penalty term and the one-step planning term impact the final performance when solely using the GCMR method in Ant Maze (U-shape). Figure [15](#gcmr_sole_params){reference-type="ref" reference="gcmr_sole_params"} illustrates similar conclusions as those of Figure 2 in the \"***Main Paper***\".

:::: {#gcmr_sole .figure latex-placement="htbp"}
::: caption
Performance when solely using the GCMR method in environments (a) Point Maze and (b) Ant Maze (U-shape). The solid lines represent the mean across five runs. The transparent areas represent the standard deviation.
:::
::::

:::: {#gcmr_sole_params .figure latex-placement="H"}
\

::: caption
Impact of varying (a) $\lambda_{gp}$ and (b) $\lambda_{osrp}$ in the Ant Maze (U-shape) environment, when solely using the GCMR method.
:::
::::

## Quantification of Extra Computational Cost {#sec:quan_comp_cost}

The extra computational cost is primarily composed of three aspects:

- \(1\) **dynamic model training**,

- \(2\) model-based gradient penalty and one-step rollout planning in **low-level policy training**,

- \(3\) goal-relabeling in **high-level policy training**.

Therefore, we ran both methods ACLG+GCMR and ACLG on Ant Maze (U-shape) for $0.7 \times 10^5$ steps to compare their runtime in these aspects.

::: {#table:quan_comp_cost}
   Training time (s)    Total    Dynamic model   Low-level policy   High-level policy
  ------------------- --------- --------------- ------------------ -------------------
       ACLG+GCMR       5065.18       16.51           3603.01             854.64
         ACLG          1845.63         0              632.97             614.01

  : Quantification of Extra Computational Cost
:::

[^1]: Code is available at <https://github.com/HaoranWang-TJ/GCMR_ACLG_official> []{#link_us label="link_us"}

[^2]: Corresponding author: Yaoru Sun.

[^3]: Our code is available at <https://github.com/HaoranWang-TJ/GCMR_ACLG_official>[]{#link_us label="link_us"}

[^4]: <https://github.com/junsu-kim97/HIGL.git>

[^5]: <https://github.com/jayLEE0301/dhrl_official.git>
