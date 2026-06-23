---
citation_key: Wan2024DiffTORI
arxiv_id: 2402.05421
arxiv_url: https://arxiv.org/abs/2402.05421
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-23T18:58:05Z
origin: ai+web
reviewed: false
---

# Introduction

Recent works have shown that the representation of a policy can have a substantial impact on the learning performance [@chi2023diffusion; @florence2022implicit; @amos2018differentiable; @seita2023toolflownet]. Prior works have explored the use of feed-forward neural networks [@seita2023toolflownet], energy-based models [@florence2022implicit], or diffusion [@chi2023diffusion; @wang2022diffusion] as the policy representation. In this paper, we propose to use differentiable trajectory optimization [@amos2018differentiable; @jin2020pontryagin; @xiao2022learning; @xu2023revisiting; @jin2021safe] as the policy representation to generate actions for deep reinforcement learning (RL) and imitation learning (IL) with high-dimensional sensory observations (images/point clouds).

Trajectory optimization is an effective and widely used algorithm in control, defined with a cost function and a dynamics function. It can be viewed as a policy [@amos2018differentiable; @jin2020pontryagin], where the parameters of the policy specify the cost function and the dynamics function. Given the learned cost and dynamics functions as well as the input state (e.g., images, point clouds, robot joint states), the policy then computes the actions by solving the trajectory optimization problem. Trajectory optimization can also be made to be differentiable, which allows back-propagating through the trajectory optimization process [@amos2018differentiable; @xu2023revisiting; @pineda2022theseus; @jin2020pontryagin; @jin2021safe; @gould2021deep; @landry2019differentiable; @jaxoptimization]. In prior work, differentiable trajectory optimization has been applied to system identification [@amos2018differentiable; @jin2020pontryagin; @jin2021safe], inverse optimal control [@jin2020pontryagin], imitation learning [@amos2018differentiable; @jin2020pontryagin; @xu2023revisiting; @shrestha2023end; @xiao2022learning] and control/planning for robotics problems with low-dimensional states [@amos2018differentiable; @jin2020pontryagin; @xu2023revisiting; @romero2023actor].

In this paper, we propose to combine differentiable trajectory optimization with deep model-based RL algorithms. Because we use differentiable trajectory optimization to generate actions [@pineda2022theseus], we are able to compute the policy gradient loss on the generated actions to learn the dynamics and cost functions to optimize the reward. This approach addresses the "objective mismatch" issue [@lambert2020objective; @eysenbach2022mismatched] of current model-based RL algorithms, i.e. models that achieve better training performance (e.g., lower MSE) in learning a dynamics model are not necessarily better for control. Our method addresses this issue, as the latent dynamics and reward models are both optimized to maximize the task performance by back-propagating the policy gradient loss through the trajectory optimization process. We show that our method outperforms prior state-of-the-art model-based RL algorithms on 15 tasks from the DeepMind Control Suite [@tassa2018deepmind] with high-dimensional image inputs.

We further benchmark our method for imitation learning on standard robotic manipulation task suites with high-dimensional sensory observations and compare our method to feed-forward policy classes as well as Energy-Based Models (EBM) [@florence2022implicit] and Diffusion [@chi2023diffusion], and term our method (**Diff**erentiable **T**rajectory **O**ptimization for **R**einforcement and **I**mitation Learning). We observe that our training procedure using differentiable trajectory optimization leads to better performance compared to the EBM approach used in prior work, which can suffer from training instability due to the requirement of sampling high-quality negative examples [@chi2023diffusion]. We also outperform diffusion-based approaches [@chi2023diffusion] due to our procedure of learning a cost function that we optimize at test time. We show achieves state-of-the-art performance across 35 different tasks: 5 tasks from Robomimic [@mandlekar2021matters] with image inputs, 9 tasks from Maniskill1 [@mu2021maniskill] and Maniskill2 [@gu2023maniskill2] with point cloud inputs, and 22 tasks from MetaWorld [@yu2020meta] with point cloud inputs.

Our work is closely related to prior work [@amos2018differentiable; @xu2023revisiting; @jin2020pontryagin] in employing differentiable trajectory optimization as a policy representation. Compared to these prior work, we are the first to show how differentiable trajectory optimization can be combined with deep model based RL algorithms, training dynamics, reward, Q function, and the policy end-to-end using task loss. In contrast, prior work either focuses on imitation learning [@amos2018differentiable; @xu2023revisiting], assumes known dynamics and reward structures and learns only a few parameters [@amos2018differentiable], or first learns the dynamics model with the dynamics prediction loss (instead of the task loss), and then uses the fixed learned dynamics for control [@xu2023revisiting]. We are also the first to show that the policy class represented by differentiable trajectory optimization can scale up to high-dimensional sensory observations like images and point clouds, achieving state-of-the-art performances in standard RL and imitation learning benchmarks. In contrast, prior works [@amos2018differentiable; @xu2023revisiting; @jin2020pontryagin] only test their methods in customized tasks with ground-truth low-level states, and do not report performance on standard benchmarks with more complex tasks and high-dimensional observations.

In summary, the contributions of our paper are as following:

- We introduce , which uses differentiable trajectory optimization as the policy representation for deep reinforcement learning and imitation learning.

- We conduct extensive experiments to compare against prior state-of-the-art methods on 15 tasks for model-based RL and 35 tasks for imitation learning in standard benchmarks with high-dimensional sensory observations, and show that achieves superior performances.

- We perform analysis and ablations of to provide insights into its performance gains.

# Related Works

**Differentiable optimization and implicit policy representation:** Our work follows the line of research on differentiable optimization, which embeds optimization problems as a layer in neural networks for end-to-end learning. Early works focus on differentiating through convex optimization problems [@amos2017optnet; @agrawal2019differentiable]. Recent works extend the range of optimization problems that can be made differentiable [@gould2021deep; @landry2019differentiable; @jin2020pontryagin; @xu2023revisiting; @jin2021safe; @pineda2022theseus]. The mostly related prior work to ours are Amos et al. [@amos2018differentiable] and Jin et al. [@jin2020pontryagin], which first proposed to treat trajectory optimization as an implicit policy and demonstrated its effectiveness in the setting of behavior cloning, system identification, and control for robotics problems with low-dimensional states. Another closely related recent work is Romero et al. [@romero2023actor], where they embed a differentiable quadratic program with learnable cost matrices and known dynamics into the last layer of the actor in PPO, with applications for quadcopter flying. Ours differ from this work as we learn non-linear costs parameterized by a full neural network, and we also learn the dynamics instead of assuming it is known. We also show our method work with high-dimensional sensory inputs such as images and point clouds. Cheng et al. [@cheng2024difftune; @cheng2023difftunehyperparameterfreeautotuningusing] proposes to learn the parameters of a PID controller by unrolling the controller and system dynamics into a computation graph and optimizing the controller parameters via gradient descent with respect to the task loss, assuming known dynamics. does not assume any prior knowledge on the dynamics or policy class; Instead of representing the policy as a predefined controller, our policy is represented as performing trajectory optimization with the learned dynamics, reward and Q functions represented as neural networks. Sacks et al. [@sacks2024deep] proposes to learn the update rule in MPPI, represented as a neural network, using reinforcement learning, with known dynamics and cost functions. Instead of learning the update rule, we learn the dynamics, reward, Q function used in trajectory optimization to generate the actions. We perform differentiable trajectory optimization instead of RL to optimize the parameters of these functions. Differentiable optimization has also been applied in other robotics domains such as autonomous driving [@shrestha2023end; @huang2023differentiable; @diehl2023energy], navigation [@xiao2022learning; @diehl2023connection], motion planning [@bhardwaj2020differentiable; @landry2019differentiable], and state estimation [@yi2021differentiable]. We are the first to show how differentiable trajectory optimization can be combined with deep model-based RL.

**Model-based reinforcement learning:** Compared to model-free RL, model-based RL usually has higher sample efficiency as it is solving a simpler supervised learning problem when learning the dynamics model. Recently, researchers have identified a fundamental problem for model-based RL, known as "objective mismatch" [@lambert2020objective]. Recent works have proposed a single objective which is a lower bound on the true return of the policy, for joint model and policy learning in model-based RL [@eysenbach2022mismatched; @ghugare2022simplifying]. Our approach also addresses the objective mismatch problem. In contrast to these two prior work which only optimizes a lower bound on the true return, our approach directly optimizes the task reward. Further, these approaches are only demonstrated using low-dimensional state-based observations whereas our approach is able to handle high-dimensional image or point cloud observations. In contrast to these works, we use Theseus [@pineda2022theseus] to analytically compute the gradient of the true objective for updating the model. Another related work, Nikishin et al. [@nikishin2022control] proposes to learn a dynamics and reward model in model-based RL, and derive an implicit policy as the softmax policy associated with the optimal Q function under the learned dynamics and reward, learned by back-propagating the RL loss via implicit function theorem. In contrast, we derive the implicit policy as the optimal solution from performing trajectory optimization with the learned dynamics, reward and Q function.

**Policy architecture for deep imitation learning:** Imitation learning can be formulated as the supervised regression task of learning to map observations to actions from demonstrations. Some recent work explores different policy architectures (e.g., explicit policy, implicit policy [@florence2022implicit], diffusion policy [@chi2023diffusion]) and different action representations (e.g., mixtures of Gaussian [@bishop1994mixture; @mandlekar2021matters], spatial action maps [@wu2020spatial], action flow [@seita2023toolflownet], or parameterized action spaces [@hausknecht2015deep]) to achieve more accurate learning from demonstrations, to model the multimodal distributions of demonstrations, and to capture sequential correlation. Our method outperforms explicit or diffusion policy approaches due to our procedure of learning a cost function that we optimize at test time. In comparison with the implicit policy, which also employs test-time optimization with a learned obective, we use a different and more stable training procedure via differentiable trajectory optimization.

# Background

## Differentiable Trajectory Optimization

In robotics and control, trajectory optimization solves the following type of problems: $$\begin{equation}
\small
\begin{split}
    \min_{a_0, ..., a_T} &\sum_{t=0}^{T-1} c(s_t, a_t) + C(s_T) \\
    s.t. ~~~~& s_{t+1} = d(s_t, a_t)
\end{split}
    \label{eq:traj_opt}
\end{equation}$$ where $c(s_t, a_t)$ and $C(s_T)$ are the cost functions, and $s_{t+1} = d(s_t, a_t)$ is the dynamics function. In this paper, we consider the case where the cost function and the dynamics functions are neural networks parameterized by $\theta$: $c_\theta(s_t, a_t)$, $C_\theta(s_T)$, and $d_\theta(s_t, a_t)$.

Let $a_0(\theta), ..., a_T(\theta)$ be the optimal solution to the trajectory optimization problem, which is a function of the model parameters $\theta$. Differentiable trajectory optimization is a class of method that enables computation of the gradient of the actions with respect to the model parameters $\mypartial{a_t(\theta)}{\theta}$. Specifically, in this paper we use Theseus [@pineda2022theseus], which is an efficient application-agnostic open source library for differentiable nonlinear least squares optimization. Theseus works well with high-dimensional states, e.g., images or point clouds, along with using neural networks as the cost and dynamics functions.

## Model-Based RL preliminaries {#sec:Model-Based RL preliminaries}

We use the standard MDP formulation: $\langle \mathcal{S}, \mathcal{A}, \mathcal{R}, \mathcal{T}, \gamma \rangle$ where $\mathcal{S}$ is the state space, $\mathcal{A}$ is the action space, $\mathcal{R}(s,a)$ is the reward function, $\mathcal{T}(\cdot|s,a)$ is the transition dynamics function, and $\gamma \in [0, 1)$ is the is the discount factor. The goal is to learn a policy $\pi$ to maximize the expected return: $\mathbb{E}_{s_t, a_t \sim \pi} [\sum_{t=1}^{\infty} \gamma^t R(s_t, a_t)]$. In this paper we work on problems where the state space $S$ are high-dimensional sensory observations, e.g., images or point clouds. Model-based RL algorithms first learn a dynamics model, and then use it for learning a policy. When applied to model-based RL, our method builds upon TD-MPC [@hansen2022temporal], a recently proposed model-based RL algorithm which we review briefly here. We choose TD-MPC for its simplicity and state-of-the-art performance. However, our method is compatible with any model-based RL algorithm that learns a dynamics model and a reward function. TD-MPC consists of the following components: first, an encoder $h_\theta$, which encodes the high-dimensional sensory observations, e.g., images, into a low-dimensional state $z_t = h_\theta(s_t)$. In the latent space, a latent dynamics model $d_\theta$ is also learned: $z_{t+1} = d_\theta(z_t, a_t)$. A latent reward predictor $R_\theta$ is learned which predicts the task reward $r$: $\hat{r} = R_\theta(z_t, a_t)$. Finally, a value predictor $Q_\theta$ learns to predict the Q value: $\hat{Q} = Q_\theta(z_t, a_t)$. Note that we use $\theta$ to denote all learnable parameters including the encoder, the latent dynamics model, the reward predictor, and the Q value predictor. These models are trained jointly using the following objective: $$\begin{equation}
\scriptsize
\label{eq:objective}
    \mathcal{L}_{\text{TD-MPC}}(\theta; \tau) = \sum_{i=t}^{t+H} \lambda^{i-t} \mathcal{L}_{\text{TD-MPC}}(\theta; \tau_{i}),
\end{equation}$$ where $\tau \sim \mathcal{B}$ is a trajectory $(s_{t}, a_{t}, r_{t}, s_{t+1})_{t:t+H}$ sampled from a replay buffer $\mathcal{B}$, $\lambda \in \mathbb{R}_{+}$ is a constant that weights near-term predictions higher, and the single-step loss is: $$\begin{equation}
\scriptsize
\begin{split}
      \mathcal{L}_{\text{TD-MPC}}(\theta; \tau_{i}) = & c_{1} {\underbrace{{\color{black} \| R_{\theta}(\mathbf{z}_{i}, \mathbf{a}_{i}) - r_{i} \|^{2}_{2}}}_\text{reward}} 
      + c_{2} {\underbrace{{\color{black} \| Q_{\theta}(\mathbf{z}_{i}, \mathbf{a}_{i}) - \left( r_{i} + \gamma Q_{\theta^{-}}(\mathbf{z}_{i+1}, \pi_{\theta}(\mathbf{z}_{i+1})) \right) \|^{2}_{2}}}_\text{value}} \\
     & + c_{3} {\underbrace{{\color{black}\| d_{\theta}(\mathbf{z}_{i}, \mathbf{a}_{i}) - h_{\theta^{-}}(\mathbf{s}_{i+1}) \|^{2}_{2}}}_{\text{latent state consistency}}}
     \label{eq:td-mpc-loss}
\end{split}
\end{equation}$$ where $\theta^-$ are parameters of target networks that are periodically updated using the parameters of the learning networks. As shown in [\[eq:td-mpc-loss\]](#eq:td-mpc-loss){reference-type="eqref" reference="eq:td-mpc-loss"}, the parameters $\theta$ is optimized with a set of surrogate losses (reward prediction, value prediction, and latent consistency), rather than directly optimizing the task performance, known as the objective mismatch issue  [@lambert2020objective]. At test time, model predictive path integral (MPPI) [@williams2016aggressive] is used for planning actions that maximize the predicted rewards and Q functions in the latent space. A policy $\pi_\psi$ is further learned in the latent space using the latent Q-value function, which is used to generate action samples in the MPPI process.

:::: {#fig:method-rl .figure latex-placement="t"}
![](Wan2024DiffTORI_figs/method_rl_neurips.png){width=".9\\linewidth"}

::: caption
**Overview of for model-based RL**. In contrast to prior work in model-based RL [@hansen2022temporal] that uses non-differentiable MPPI (left), we utilize differentiable trajectory optimization to generate actions (right). computes the policy gradient loss on the generated actions and back-propagates it through the optimization process, to optimize the encoder as well as other latent space models (latent reward predictor and latent dynamics function) to maximize task performance.
:::
::::

# Method

## Overview

The core idea of is to use trajectory optimization as the policy $\pi_\theta$, where $\theta$ parameterizes the dynamics and cost functions. Given a state $s$, generates the actions $a(\theta)$ by solving the trajectory optimization problem in [\[eq:traj_opt\]](#eq:traj_opt){reference-type="eqref" reference="eq:traj_opt"} with $s_0 = s$. To optimize the policy parameters $\theta$, we use differentiable trajectory optimization to compute the gradients of the loss $\mathcal{L}(a(\theta))$ with respect to the policy parameters: $\mypartial{\mathcal{L}(a(\theta))}{\theta}$, where the exact form of the loss depends on the problem setting.

An overview of applying to model-based RL is shown in Figure [1](#fig:method-rl){reference-type="ref" reference="fig:method-rl"}. Existing model-based RL algorithms such as TD-MPC suffer from the objective mismatch issue: the latent dynamics and reward (cost) functions are learned to optimize a set of surrogate losses (as in [\[eq:td-mpc-loss\]](#eq:td-mpc-loss){reference-type="eqref" reference="eq:td-mpc-loss"}), instead of optimizing the task performance directly. addresses this issue: by computing the policy gradient loss on the optimized actions from trajectory optimization and differentiating through the trajectory optimization process, the dynamics and cost functions are optimized directly to maximize the task performance. We describe for model-based RL in Section [4.2](#sec:model-based-RL){reference-type="ref" reference="sec:model-based-RL"}.

We also apply to imitation learning; an overview is shown in Figure [2](#fig:method-il){reference-type="ref" reference="fig:method-il"}. In contrast to explicit policies that generate actions at test-time by forward passes of the policy network, generates the actions via test-time trajectory optimization with a learned cost function. This is in the same spirit of implicit behaviour cloning [@florence2022implicit] which learns an energy function and optimizes with respect to it to generate actions at test-time. However, we observe that our training procedure using differentiable trajectory optimization leads to better performance compared to the EBM approach used in prior work, which can suffer from training instability due to the requirement of sampling high-quality negative examples [@chi2023diffusion]. We describe for imitation learning in detail in Section [4.3](#sec:method-il){reference-type="ref" reference="sec:method-il"}.

## Differentiable trajectory optimization applied to model-based RL {#sec:model-based-RL}

We build on top of TD-MPC for model-based RL. Similar to TD-MPC, consists of an encoder $h_\theta$, a latent dynamics model $d_\theta$, a reward predictor $R_\theta$, and a Q-value predictor $Q_\theta$ (see Sec. [3.2](#sec:Model-Based RL preliminaries){reference-type="ref" reference="sec:Model-Based RL preliminaries"}). We use $\theta$ to denote all learnable parameters to be optimized in . As shown in Figure [1](#fig:method-rl){reference-type="ref" reference="fig:method-rl"}, the key to is to change the non-differentiable MPPI planning algorithm in TD-MPC to a differentiable trajectory optimization, and include the policy gradient loss on the generated actions to optimize the model parameters $\theta$ directly for task performance.

Formally, given a state $s_t$, we use the encoder $h_\theta$ to encode it to the latent state $z_t$, and then construct the following trajectory optimization problem in the latent space: $$\begin{equation}
\small
\begin{split}
    a(\theta) = \argmax_{a_t, ..., a_{t+H}} & \sum_{l=t}^{H-1}\gamma^{l-t} R_\theta(z_t, a_t) + \gamma^H Q_\theta(z_H, a_H)  \\
    s. t. & ~~ z_{t+1} = d_\theta(z_t, a_t)
\end{split}
\label{eq:RL-traj-opt-def}
\end{equation}$$ where $H$ is the planning horizon. In this paper we leverage Theseus [@pineda2022theseus] to solve [\[eq:RL-traj-opt-def\]](#eq:RL-traj-opt-def){reference-type="eqref" reference="eq:RL-traj-opt-def"} in a differentiable way. Since Theseus only supports solving non-linear least-square optimization problems without constraints, we remove the dynamics constraints in the above optimization problem by manually rolling out the dynamics into the objective function. For example, with a planning horizon of $H=2$, we turn the above optimization problem into the following one: $$\begin{equation}
\small
\begin{split}
    a(\theta) = \argmax_{a_t, a_{t+1}, a_{t+2}}  &R_\theta(z_t, a_t) 
    +R_\theta(d_\theta(z_t, a_t), a_{t+1}) +Q_\theta(d_\theta(d_\theta(z_t, a_t), a_{t+1}), a_{t+2})
\end{split}
\end{equation}$$ We set the values of $H$ following the schedule as in TD-MPC, and we use the Levenberg--Marquardt algorithm in Theseus to solve the optimization problem. Following TD-MPC, we also learn a policy $\pi_\psi$ in the latent space using the learned Q-value predictor $Q_\theta$, and the output from the policy is used as the action initialization for solving [\[eq:RL-traj-opt-def\]](#eq:RL-traj-opt-def){reference-type="eqref" reference="eq:RL-traj-opt-def"}.

Let $a(\theta)$ be the solution of the above trajectory optimization problem, obtained using Theseus as described above. is learned with the following objective, which jointly optimizes the encoder, latent dynamics model, latent reward model, and the Q-value predictor: $$\begin{equation}
\small
\begin{split}
    \mathcal{L}^{RL}_{\model{}}(\theta; \tau) &= \sum_{i=t}^{t+H} \lambda^{i-t} \left(\mathcal{L}_{TD-MPC}(\theta; \tau_{i}) + c_0 \mathcal{L}_{PG}(\theta; \tau_i)\right) \\
    \mathcal{L}_{PG}(\theta; \tau_i) &= - \tilde{Q}_\phi(s_i, a(\theta))
\end{split}
\label{eq:RL_loss}
\end{equation}$$ where $\tilde{Q}_\phi$ is the Q function learned via Bellman updates [@watkins1992q] which is used to compute the deteministic policy gradient [@lillicrap2015continuous], and $c_0$ is the weight for this loss term. $\tilde{Q}_\phi$ is learned in the original state space $\mathcal{S}$ instead of the latent space to provide accurate policy gradients. The key idea here is that we can backpropagate through the policy gradient loss $\mathcal{L}_{PG}$, which backpropagates through $a(\theta)$ and then through the differentiable trajectory optimization procedure of Equation [\[eq:RL-traj-opt-def\]](#eq:RL-traj-opt-def){reference-type="ref" reference="eq:RL-traj-opt-def"} to update $\theta$.

## Differentiable Trajectory Optimization applied to imitation learning {#sec:method-il}

:::: {#fig:method-il .figure latex-placement="t"}
![](Wan2024DiffTORI_figs/method_il_neurips.png){width="55%"}

::: caption
**Overview of our method on Imitation Learning.** (right) learns a cost function via differentiable trajectory optimization and performs test-time optimization with it, which is different from prior work (left) that uses an explicit policy or diffusion without test-time optimization. Although implicit policy shares the same spirit as , we observe that the training procedure of using differentiable trajectory optimization leads to better performance compared to the EBM approach used in prior work [@florence2022implicit], which can suffer from training instability.
:::
::::

We also use for model-based imitation learning. A comparison of to other types of policy classes used in prior work is shown in Figure [2](#fig:method-il){reference-type="ref" reference="fig:method-il"}. In this approach, consists of an encoder $h_\theta$ and a latent dynamics function $d_\theta$, as before. However, in the setting of imitation learning, we do not assume access to a reward function $\mathcal{R}(s,a)$. Instead, we generate actions by solving the following trajectory optimization problem: $$\begin{equation}
\small
    \begin{split}
    a(\theta) = \argmax_{a_t, ..., a_{t+H}} & \sum_{l=t}^{H}\gamma^{l-t} f_\theta(z_t, a_t)  \\
    s. t. & ~~ z_{t+1} = d_\theta(z_t, a_t),
\end{split}
\label{eq:IL-traj-opt-def}
\end{equation}$$ in which $f_\theta(z_t, a_t)$ is a function over the latent state $z_t$ and actions $a_t$ that we will optimize using the imitation learning loss, as described below. Similarly, We use $\theta$ to denote all learnable parameters to be optimized in , including the parameters of the encoder $h_\theta$, the latent dynamics model $d_\theta$, and the function $f_\theta$ in the imitation learning setting.

In imitation learning, we assume access to an expert dataset $D = \{(s_i, a^*_i)\}^N_{i=1}$ of state-action pairs $(s_i, a^*_i)$. In the most basic form, the loss $\mathcal{L}$ for can be the mean square error between the the expert actions $a^*_i$ and the actions $a(\theta)$ returned from solving [\[eq:IL-traj-opt-def\]](#eq:IL-traj-opt-def){reference-type="eqref" reference="eq:IL-traj-opt-def"}: $$\begin{equation}
\small
    \mathcal{L}_{BC}(\theta) = \sum_{i=1}^N ||a(\theta) - a^*_i||
    \label{eq:bc}
\end{equation}$$ The key idea here is that we can backpropagate through the imitation loss $\mathcal{L}_{BC}$, which backpropagates through $a(\theta)$ and then through the differentiable trajectory optimization procedure of Equation [\[eq:IL-traj-opt-def\]](#eq:IL-traj-opt-def){reference-type="ref" reference="eq:IL-traj-opt-def"} to update $\theta$. This enables us to learn the function $f_\theta(z_t, a_t)$ used in the optimization Equation [\[eq:IL-traj-opt-def\]](#eq:IL-traj-opt-def){reference-type="ref" reference="eq:IL-traj-opt-def"} directly by optimizing the imitation loss $\mathcal{L}_{BC}(\theta)$. Because this loss is optimized through the trajectory optimization procedure (Equation [\[eq:IL-traj-opt-def\]](#eq:IL-traj-opt-def){reference-type="ref" reference="eq:IL-traj-opt-def"}), we will learn a function $f_\theta(z_t, a_t)$ such that optimizing Equation [\[eq:IL-traj-opt-def\]](#eq:IL-traj-opt-def){reference-type="ref" reference="eq:IL-traj-opt-def"} returns actions that match the expert actions.

**Multimodal :** The loss in Equation [\[eq:bc\]](#eq:bc){reference-type="ref" reference="eq:bc"} will not be able to capture multi-modal action distributions in the expert demonstrations. To address this, we use a Conditional Variational Auto-Encoder (CVAE) [@sohn2015learning] as the policy architecture, which has the ability to capture a multi-modal action distribution [@zhao2023learning]. The CVAE encoder encodes the state $s_i$ and the expert action $a_i^*$ into a latent state vector $z_i$. The key idea in our approach is that the decoder in CVAE takes the form of a trajectory optimization algorithm, given by Equation [\[eq:IL-traj-opt-def\]](#eq:IL-traj-opt-def){reference-type="ref" reference="eq:IL-traj-opt-def"}. It takes as input the sampled latent $\tilde{z}$ from the Gaussian Prior, and the state $s_i$ and uses differentiable trajectory optimization to decode the action $a(\theta)$. Because this trajectory optimization is differentiable, we can backpropagate through it to learn the parameters $\theta$ for the encoder, dynamics $d_\theta$, and the function $f_\theta$ used in Equation [\[eq:IL-traj-opt-def\]](#eq:IL-traj-opt-def){reference-type="ref" reference="eq:IL-traj-opt-def"}. See Appendix [10](#sec:CVAE){reference-type="ref" reference="sec:CVAE"} for further details.

**Action refinement:** We note that provides a natural way to perform action refinement on top of a base policy. Given an action from any base policy, we can use this action as the initialization of the action variables for solving the trajectory optimization problem; the trajectory optimizer will iteratively refine this action initialization with respect to the optimization objective of Equation [\[eq:IL-traj-opt-def\]](#eq:IL-traj-opt-def){reference-type="ref" reference="eq:IL-traj-opt-def"}. In our experiments, we find always outperforms the base policies when using their actions as the initialization and other ways of performing action refinement, such as residual learning.

# Experiments

## Model-based Reinforcement Learning

::::: {#fig:RL_results .figure latex-placement="t"}
::: center
![](Wan2024DiffTORI_figs/RL_results_new_higher_1.png){width="100%"}
:::

::: caption
Performance of , in comparison to 4 prior state-of-the-art model-based and model-free RL algorithms, on 15 tasks from DeepMind control suite. achieves the best performance when averaged across all tasks. Results are averaged with 4 seeds, and the shaded regions represent the $95\%$ confidence interval.
:::
:::::

We conduct experiments on 15 DeepMind Control suite tasks, which involve simulated locomotion and manipulation tasks, such as making a cheetah run or swinging a ball into a cup. All tasks use image observations and the control policy does not have direct access to the underlying states.

We compare to the following baselines: **SAC** [@haarnoja2018soft], a commonly used off-policy model-free RL algorithm. **DrQ-v2** [@yarats2021mastering], a state-of-the-art model-free RL algorithm for image observations that adds data augmentation on top of SAC . **TD-MPC** [@hansen2022temporal], a state-of-the-art model-based RL algorithm, which builds on. All training details such as hyper-parameters, and pysudo-code can be found in Appendix [8](#app:implementation){reference-type="ref" reference="app:implementation"}. All experiments use NVIDIA 2080 Ti GPUs.

Figure [3](#fig:RL_results){reference-type="ref" reference="fig:RL_results"} shows the learning curves for all methods on all tasks. The top-left subplot shows the normalized performance averaged across all 15 tasks, which is computed as the achieved return divided by the max return from any algorithm. As shown, (red curve) outperforms all compared baselines by a noticeable margin. On 14 out of the 15 tasks (except Quadruped-walk), achieves the highest performance among compared algorithms. We especially note that the performance of is much higher than TD-MPC, which builds on, showing the benefit of adding the policy gradient loss and directly differentiating through it to optimize the learned latent spaces. Although achieves higher sample efficiency, one limitation of is that it requires more wall-clock time for training, due to the need for solving and differentiating through the trajectory optimization process. We show detailed results on computational efficiency (return vs wall-clock time) of in Appendix [7.1.2](#app:rl-wall-clock){reference-type="ref" reference="app:rl-wall-clock"}. We also perform ablation studies to examine how each loss term in [\[eq:RL_loss\]](#eq:RL_loss){reference-type="eqref" reference="eq:RL_loss"} contributes to the final performance of in Figure [6](#fig:rl-ablation){reference-type="ref" reference="fig:rl-ablation"} in Appendix [7.1.3](#app:rl-ablation){reference-type="ref" reference="app:rl-ablation"}.

:::: table*
[]{#table:IL on MetaWorld label="table:IL on MetaWorld"}

::: flushleft
:::
::::

::: table*
+-------------+------+--------+--------------+---------------+-----------+------------------+------------------+------------------+
|             | IBC  | BC-RNN |   ---------- |   ----------- | Diffusion |   -------------- |   -------------- |   -------------- |
|             |      |        |   Residual   |   (Ours)      |           |   IBC            |   Residual       |   (Ours)         |
|             |      |        |   +BC-RNN    |   \+ BC-RNN   |           |   \+ Diffusion   |   \+ Diffusion   |   \+ Diffusion   |
|             |      |        |   ---------- |   ----------- |           |   -------------- |   -------------- |   -------------- |
+:===========:+:====:+:======:+:============:+:=============:+:=========:+:================:+:================:+:================:+
| Square      |      |        |              |               |           |                  |                  |                  |
+-------------+------+--------+--------------+---------------+-----------+------------------+------------------+------------------+
| Transport   |      |        |              |               |           |                  |                  |                  |
+-------------+------+--------+--------------+---------------+-----------+------------------+------------------+------------------+
| ToolHang    |      |        |              |               |           |                  |                  |                  |
+-------------+------+--------+--------------+---------------+-----------+------------------+------------------+------------------+
| Push-T      |      |        |              |               |           |                  |                  |                  |
+-------------+------+--------+--------------+---------------+-----------+------------------+------------------+------------------+
| **Average** | 0.96 | 0.27   | 0.25         | 0.18          | 0.10      | 0.78             | 0.10             | **0.07**         |
+-------------+------+--------+--------------+---------------+-----------+------------------+------------------+------------------+

[]{#imitation_results1 label="imitation_results1"}
:::

::: table*
[]{#imitation_results_2 label="imitation_results_2"}
:::

## Imitation Learning

Below we show results of on 3 commonly used imitaiton learning benchmarks: MetaWorld [@yu2020meta], RoboMimic [@mandlekar2021matters], ManiSkill [@mu2021maniskill], and the comparison to state-of-the-art methods on these three benchmarks. We also compare to one closely related prior work [@amos2018differentiable] on one of their customized tasks in Appendix [7.3](#app:amos){reference-type="ref" reference="app:amos"}.

### MetaWorld

MetaWorld [@yu2020meta] is a large-scale benchmark that includes 100 robotic manipulation tasks, and has been recently used for evaluating different imitation learning algorithms [@ze20243d]. The policy observation is point clouds of the scene, and the action is the 3d translation of the robot end-effector. We test on 22 tasks with different levels of difficulties: Medium, Hard, and Very Hard (See Table [\[table:IL on MetaWorld\]](#table:IL on MetaWorld){reference-type="ref" reference="table:IL on MetaWorld"} for all the tasks). 10 demonstrations are used for all tasks [@ze20243d]. We compare with the following baselines: **DP3** [@ze20243d], a 3D version of diffusion policy that achieves state-of-the-art performances on this benchmark, outperforming other algorithms such as the original diffusion policy [@chi2023diffusion] with 2d image inputs. **Residual + DP3**: Since refines the actions from a base pre-trained DP3 policy, we additionally compare to this baseline that also leverages the actions from a base pre-trained DP3 policy. Specifically, we learn a residual policy on top of the base pre-trained policy, which takes as input the action from the base policy, and outputs a delta action that is added to the base action. This is the most standard and simple way of doing residual learning. All training details such as hyper-parameters and pseudo-code can be found in Appendix [8](#app:implementation){reference-type="ref" reference="app:implementation"}.

Table [\[table:IL on MetaWorld\]](#table:IL on MetaWorld){reference-type="ref" reference="table:IL on MetaWorld"} presents the task success rates, averaged over 50 evaluation episodes, of all compared algorithms. As shown, consistently achieves higher (or on par) success rates than the other 2 compared baselines. The improvement in success rates is larger on tasks where the original DP3 policy struggles, e.g., a 15% improvement on the task of Shelf Place and Sweep Into; and as expected, when the base DP3 policy is already doing well on the task, there is not much room of improvement left for , e.g., on Basketball and Stick Push. The simple way of learning a residual policy on top of the DP3 policy does not always improve the performance of the base policy, and even leads to lower success rates. This demonstrates that is a more effective way to leverage a pre-trained policy. On average, the success rates of is $7.7\%$ higher than that of DP3, a substantial improvement with only 10 demonstrations.

### Robomimic

Robomimic [@mandlekar2021matters] is another commonly used benchmark designed to study imitation learning for robot manipulation. The benchmark encompasses a total of 5 tasks with two types of demonstrations: collected from proficient humans (PH) or a mixture of proficient and non-proficient humans. We use the PH demonstrations, and evaluate on three of the most challenging tasks: Square, Transport, and ToolHang. We use image-based observations and the default velocity controller for all the tasks. In addition to Robomimic, we compare to another task, Push-T from the diffusion policy [@chi2023diffusion] task set, to demonstrate that we can learn multimodal cost functions by using the CVAE training loss.

We compare to the following baselines: **IBC** [@florence2022implicit]: An implicit policy that learns an energy function conditioned on both action and observation using the InfoNCE loss [@oord2018representation]. **BC-RNN** [@mandlekar2021matters]: A variant of BC that uses a Recurrent Neural Network (RNN) as the policy network to encode a history of observations. This is the best-performing baseline in the original Robomimic [@mandlekar2021matters] paper. **Residual + BC-RNN**: We use a pretrained BC-RNN as the base policy, and learn a residual policy on top of it. The residual policy takes as input the action from the base policy, and outputs a delta action which is added to the base action. **Diffusion Policy** [@chi2023diffusion]: A policy that uses the diffusion model as the policy class. It refines noise into actions via a learned gradient field. **IBC + Diffusion**: A version of IBC that uses the action from a pre-trained Diffusion Policy as the action initialization in the test-time optimization process. **Residual + Diffusion**: Similar to Residual + BC-RNN, but using a pre-trained Diffusion Policy as the base policy. For , we compare two variants of it: + BC-RNN and + Diffusion Policy, which uses a pre-trained BC-RNN or a pre-trained diffusion policy as the base policy to generate the initialization action for solving the trajectory optimization problem. In Appendix [7.2](#app:imitation-learning-results){reference-type="ref" reference="app:imitation-learning-results"}, we also present results of with zero initialization or random initialization, instead of initializing the action from a base policy.

The results are shown in Table [\[imitation_results1\]](#imitation_results1){reference-type="ref" reference="imitation_results1"}. We find that +Diffusion Policy achieves the lowest failure rates consistently across all tasks. Even though Diffusion Policy has almost saturated on these tasks with very low failure rates, can still further reduces it. Furthermore, irrespective of the base policy used --- whether BC-RNN or Diffusion Policy --- always brings noticeable improvement in the performance over the base policy. While learning a residual policy does lead to improvements upon the base policy, shows a significantly greater performance boost. In addition, by comparing +Diffusion Policy with IBC+Diffusion Policy, we find that using the same action initialization for IBC is considerably less effective than using the same action initialization in . In many tasks, even when the base Diffusion Policy already exhibits low failure rates, IBC+Diffusion Policy still results in poor performances, indicating the training objective used in IBC actually deteriorates the base actions.

We also show the benefit of using a CVAE architecture for , which enables to capture multimodal action distributions. With different latent samples from CVAE, we get different objective functions $f_{\theta}(z,a)$ and dynamics functions $d_{\theta}(z,a)$, allowing to generate different actions from the same state. Figure [4](#fig:rew_landscape){reference-type="ref" reference="fig:rew_landscape"} illustrates the multimodal objective function learned by (right), and the resulting multimodal actions (left). The left subplot shows that when starting from the same action initialization $a_{init}$, with two different latent samples, optimizes $a_{init}$ into two different actions, $\hat{a}_1$ and $\hat{a}_2$ that move in distinct directions. The trajectory optimization procedure that iteratively updates the action is represented by dashed lines transitioning from faint to solid. From these two actions, two distinct trajectories are subsequently generated to push the T-shape object towards its goal. The middle and right subplots show the objective function landscapes for the 2 different samples, as well as the initial action $a_{init}$, and the final optimized action $\hat{a_1}$ and $\hat{a_2}$. We note the two landscapes are distinct from each other with different optimal solutions, showing that can generate multimodal objective functions and thus capture multimodal action distributions. We note that the learned objective function $f$ is not necessarily a "reward" function as those learned via inverse RL [@ng2000algorithms]. It is just a learned "objective function", such that optimizing it with trajectory optimization would yield actions that minimize the imitation learning loss with respect to the expert actions in the demonstration. We leave exploring the connections with inverse RL for future work.

### ManiSkill

ManiSkill [@mu2021maniskill; @gu2023maniskill2] is a benchmark for learning generalizable robotic manipulation skills with 2D & 3D visual input. It includes a series of rigid body tasks and soft body tasks. We choose 9 tasks (4 soft body tasks and 5 rigid body tasks) from ManiSkill1 [@mu2021maniskill] and ManiSkill2 [@gu2023maniskill2] and use 3D point cloud input for all the tasks. We use the end-effector frame as the observation frame [@liu2022frame] and use the PD controller with the end-effector delta pose as the action.

We build our method on top of the strongest imitation learning baseline in ManiSkill2 released by the authors, which is a Behavior Cloning (BC) policy with PointNet [@qi2017pointnet] as the encoder. Again, we also compare to BC+residual, which learns a residual policy that takes as input the action from the BC policy and outputs a delta correction. The results are shown in Table [\[imitation_results_2\]](#imitation_results_2){reference-type="ref" reference="imitation_results_2"}. As shown, + BC consistently achieves higher success rates than both baselines on all tasks, demonstrating the strong effectiveness of using differentiable trajectory optimization as the policy class.

:::: {#fig:rew_landscape .figure latex-placement="t"}
![](Wan2024DiffTORI_figs/rew_landscape.png){width="75%"}

::: caption
By using a CVAE, can learn multimodal objectives functions via sampling different latent vectors from CVAE (right). By performing trajectory optimization with these two different objective functions, can generate multimodal actions (left).
:::
::::

# Conclusion and Discussion

We introduce that uses differentiable trajectory optimization to generate the policy actions for deep reinforcement learning and imitation learning. The key is to utilize the recent progress in differentiable trajectory optimization to compute the gradients of the loss with respect to the parameters of the cost and dynamics function of trajectory optimization, and learn them end-to-end. When applied to model-based reinforcement learning, addresses the "objective mismatch" issue of prior methods. We also test for imitation learning on standard robotic manipulation task suites with high-dimensional sensory observations and compare it to feed-forward policy classes as well as Energy-Based Models (EBM) and Diffusion. Across 15 model-based RL tasks and 35 imitation learning tasks with high-dimensional image and point cloud inputs, outperforms prior state-of-the-art methods.

# Additional results

## Model-based Reinforcement Learning {#app:model-based-rl-results}

###  without policy gradient loss

In model-based reinforcement learning, the key distinctions between and TD-MPC [@hansen2022temporal] are: 1) TD-MPC employs the Model Predictive Path Integral (MPPI [@williams2015model]) in the planning stage, whereas we utilize trajectory optimization. 2) In addition to the original loss used in TD-MPC, we use an additional policy gradient loss and back-propagate it through the differentiable trajectory optimization process to update the model parameters. Figure [5](#fig:RL_results_forward){reference-type="ref" reference="fig:RL_results_forward"} shows that the improvement of over TD-MPC comes from the addition of the policy gradient loss, instead of purely changing MPPI to trajectory optimization. To be more specific, we compare TD-MPC with  (w/o backward), a variant of that removes the policy gradient loss for updating the model parameters. The results indicate that TD-MPC and the  (w/o backward) variant perform comparably, suggesting that using MPPI or trajectory optimization at test-time for action generation have similar performances. With the inclusion of the policy gradient loss, significantly outperforms both TD-MPC and the  (w/o backward) variant, demonstrating the efficacy of adding the policy gradient loss in .

::::: {#fig:RL_results_forward .figure latex-placement="h"}
::: center
![](Wan2024DiffTORI_figs/RL_results_forward.png){width="100%"}
:::

::: caption
Performance of , in comparison to TD-MPC and  (w/o backward) on 15 tasks from DeepMind control suite.
:::
:::::

### Computational efficiency of  {#app:rl-wall-clock}

In addition to comparing the sample efficiency of to prior methods, we also compare the computational efficiency of versus TD-MPC on some of the environments. This is shown in Figure [7](#fig:rebuttal_wall_clock_time){reference-type="ref" reference="fig:rebuttal_wall_clock_time"}, where the y-axis is the return, and the x-axis is the wall-clock time (tested on a NVIDIA RTX 2080 Ti GPU) used to train and TD-MPC for 1M environment steps. As shown, it takes more wall-clock time for to finish the training. In terms of computational efficiency, the results are environment-dependent. achieves better computational efficiency on reacher-hard and cup-catch. On pendum-swingup, TD-MPC converges to a sub-optimal value in the early training stage and outperforms it within 24 hours of training time. has similar computational efficiency on cartpole-swingup-sparse, reacher-easy, and finger-spin, and slightly worse computational efficiency on cheetah-run and walker-stand compared to TD-MPC. The gap is larger on hopper-stand. The major reason for to take longer time for training is that solving and back-propagating through the trajectory optimization problem in [\[eq:RL-traj-opt-def\]](#eq:RL-traj-opt-def){reference-type="eqref" reference="eq:RL-traj-opt-def"} is slower than doing MPPI as used in TD-MPC. As a reference, to infer the action at one time step, it takes $0.052$ second to use Theseus to solve and differentiate through the trajectory optimization problem in [\[eq:RL-traj-opt-def\]](#eq:RL-traj-opt-def){reference-type="eqref" reference="eq:RL-traj-opt-def"}, and $0.0092$ second for using MPPI in TD-MPC. However, we also want to note that the community is actively developing better and faster algorithms/software libraries for differentiable trajectory optimization, which could improve the computation efficiency of . For example, in all our experiments, we used the default CPU-based solver in Theseus. Theseus also provides a more advanced solver named BaSpaCho, which is a batched sparse Cholesky solver with GPU support. When we switch from the default CPU-based solver to BaSpaCho, the time cost of solving the trajectory optimization problem in [\[eq:RL-traj-opt-def\]](#eq:RL-traj-opt-def){reference-type="eqref" reference="eq:RL-traj-opt-def"} is reduced by 22% from $0.052$ second to $0.041$ second. With better libraries/algorithms in the future for differentiable trajectory optimization, we believe the computational efficiency of would further improve.

:::: {#fig:rl-ablation .figure latex-placement="h"}
![](Wan2024DiffTORI_figs/RL_ablation.png){width="100%"}

::: caption
Ablation study of to examine the contribution of each loss terms towards the final performance, on a subset of 4 tasks. We find the reward prediction loss, action initialization, and dynamics prediction loss are all essential for to achieve good performance.
:::
::::

### Ablation study on the loss terms {#app:rl-ablation}

We also perform ablation studies to examine how each loss term in [\[eq:RL_loss\]](#eq:RL_loss){reference-type="eqref" reference="eq:RL_loss"} contributes to the final performance of , as shown in Figure [6](#fig:rl-ablation){reference-type="ref" reference="fig:rl-ablation"}. We find that removing the reward prediction loss causes to completely fail. Removing the dynamics loss, or not using the action initialization from the learned policy $\pi_\psi$ for solving the trajectory optimization, both lead to a decrease in the performance. These shows the necessity of using all the loss terms in for learning a good latent space to achieve strong performance.

::::: {#fig:rebuttal_wall_clock_time .figure}
::: center
![](Wan2024DiffTORI_figs/RL_time_results.png){width="100%"}
:::

::: caption
Return vs wall-clock time of and TD-MPC on some of the RL environments. The x-axis is the training time in days (24 hours), and the y-axis is the return. Both methods are trained for 1M environments steps. The training takes a long time (a few days on some environments) because the policy observation is high-dimensional images.
:::
:::::

## Imitation Learning {#app:imitation-learning-results}

###  with zero and random action initialization

We also present results of with zero initialization or random initialization, where instead of initializing the action from a base policy, the action is initialized to be 0, or randomly sampled from $\mathcal{N}(0, 1)$, on RoboMimic and Maniskill.

The results on RoboMimic is shown in Table [8](#imitation_results1_full){reference-type="ref" reference="imitation_results1_full"}. We notice a drop in performance of with zero or randomly-initialized actions, possibly due to the convergence to bad local minima during nonlinear trajectory optimization without a good action initialization. We note this would not be a drawback of applying in practice for imitation learning: one could always first learn a base policy using any behavior cloning algorithm, and then use to further refine the actions.

The results on Maniskill is shown in Table [13](#imitation_results_2_full){reference-type="ref" reference="imitation_results_2_full"}. Again, if we use zero or random action initialization with , the performance drops to be similar to or slightly worse than vanilla BC. Therefore, we think a good practice of using for imitation learning would be to always try to provide it with a good action initialization, e.g., by first training a BC policy and use its action as the initialization in .

::: {#imitation_results1_full}
[TABLE]

: Failure rates ($\downarrow$) of and all other mehtods on the Robomimic tasks. achieves the best performances on all tasks when using diffusion policy as the base policy. If zero or random initialization are used in , the performance drops, possibly due to the convergence to bad local minima during nonlinear trajectory optimization without a good action initialization.
:::

[]{#imitation_results1_full label="imitation_results1_full"}

::: {#imitation_results_2_full}
[TABLE]

: Success rates ($\uparrow$) of all methods on the Maniskill benchmark. consistently outperforms both baselines on all tasks with action initialization from the BC policy. If zero or random initialization are used in , the performance drops, possibly due to the convergence to bad local minima during nonlinear trajectory optimization without a good action initialization.
:::

[]{#imitation_results_2_full label="imitation_results_2_full"}

### Results of positional controller on RoboMimic

Note that for the three tasks in Table [\[imitation_results1\]](#imitation_results1){reference-type="ref" reference="imitation_results1"} from Robomimic, we use the default velocity controller from Robomimic. We note the use of the velocity controller leads to a small decline in the performance of the Diffusion Policy compared to its performance in the original paper where a positional controller is used. The Push-T task still uses the default position controller as in the diffusion policy paper. Below we evaluate the performance of and Diffusion Policy with the positional controller.

In the original Diffusion Policy [@chi2023diffusion] paper, it was observed that the use of positional controllers yielded superior results for Diffusion Policy compared to the default velocity controller on Robomimic [@mandlekar2021matters] tasks. We evaluate Diffusion Policy, which is the strongest baseline, and on the most difficult three tasks with ph (proficient-human demonstration) and mh (multi-human demonstration) demonstrations using positional controller. The results with the positional controller are presented in Table [14](#imitation_additional_results){reference-type="ref" reference="imitation_additional_results"}. Diffusion Policy already achieves nearly the maximal possible performance on most tasks with the positional controller. , however, is able to achieve similar or even higher performances on most of these tasks.

::: {#imitation_additional_results}
                 Square (ph)                          Square (mh)                          Transport (ph)                       Transport (mh)                       ToolHang (ph)
  -------------- ------------------------------------ ------------------------------------ ------------------------------------ ------------------------------------ ------------------------------------
  Diffusion      **0.02**$\pm$`<!-- -->`{=html}0.01   **0.03**$\pm$`<!-- -->`{=html}0.02   **0.00**$\pm$`<!-- -->`{=html}0.00   0.12$\pm$`<!-- -->`{=html}0.02       0.05$\pm$`<!-- -->`{=html}0.02
  \+ Diffusion   **0.02**$\pm$`<!-- -->`{=html}0.01   0.04$\pm$`<!-- -->`{=html}0.02       **0.00**$\pm$`<!-- -->`{=html}0.00   **0.09**$\pm$`<!-- -->`{=html}0.01   **0.04**$\pm$`<!-- -->`{=html}0.01

  : Failure rates ($\downarrow$) of and Diffusion Policy using Positional Controllers on Robomimic Tasks.
:::

[]{#imitation_additional_results label="imitation_additional_results"}

### Ablation on planning horizon $H$

Additionally, we do ablation experiments on the planning horizon $H$ for imitation learning, with the results presented in Table [15](#imitation_horizon){reference-type="ref" reference="imitation_horizon"}. We observe that simply increasing the planning horizon $H$ in imitation learning does not necessarily enhance performance. As the horizon increases from $H = 1$ to $H = 3$, the performance remains nearly the same; however, when $H$ is increase to $5$, we observe a slight decline in the performance.

::: {#imitation_horizon}
            Square (ph)                          Transport (ph)                       ToolHang (ph)                        Push-T
  --------- ------------------------------------ ------------------------------------ ------------------------------------ ------------------------------------
  $H = 1$   **0.08**$\pm$`<!-- -->`{=html}0.01   **0.04**$\pm$`<!-- -->`{=html}0.01   **0.08**$\pm$`<!-- -->`{=html}0.01   **0.09**$\pm$`<!-- -->`{=html}0.01
  $H = 3$   **0.08**$\pm$`<!-- -->`{=html}0.01   0.06$\pm$`<!-- -->`{=html}0.02       **0.08**$\pm$`<!-- -->`{=html}0.00   0.12$\pm$`<!-- -->`{=html}0.02
  $H = 5$   0.09$\pm$`<!-- -->`{=html}0.01       0.06$\pm$`<!-- -->`{=html}0.01       0.10$\pm$`<!-- -->`{=html}0.00       0.12$\pm$`<!-- -->`{=html}0.01

  : Failure rates ($\downarrow$) of different planning horizon $H$ for on RoboMimic tasks.
:::

[]{#imitation_horizon label="imitation_horizon"}

::: {#tab:amos}
                            Expert Policy      Amos et al.          LSTM policy             (ours)
  ------------------------ --------------- -------------------- -------------------- --------------------
    Pendulum w/o damping       13.126       13.576 $\pm$ 0.012   15.962 $\pm$ 0.164   14.603 $\pm$ 0.190
   Pendulum with dampling      10.132       14.874 $\pm$ 0.600   12.098 $\pm$ 0.031   10.644 $\pm$ 0.029

  : Cost of different algorithms on the Pendulum swingup tasks from Amos et al. As in Amos et al., we test in two settings, pendulum without damping and with damping. Lower cost means the better performance. performs slightly worse in the no damping case but noticeably better in the damping case.
:::

[]{#tab:amos label="tab:amos"}

## Comparison to prior work Amos et al. [@amos2018differentiable] {#app:amos}

In our main paper, we did not compare to [@amos2018differentiable; @jin2020pontryagin; @xu2023revisiting] because we target different experiments. These related works all conduct experiments on customized tasks with ground-truth low-level states. In contrast, we test our method on standard RL and robotic imitation learning benchmarks, with high-dimensional sensory observations like images and point clouds. As these prior works have not been demonstrated on high-dimensional observations or more complex tasks, we originally compared to more recent state-of-the-art methods on these benchmarks, e.g., 3D Diffusion Policy [@ze20243d].

We have now included a comparison with Amos et al. [@amos2018differentiable] in one of their tasks (pendulum swing-up with ground-truth low-level states) under imitation learning settings. Unlike Amos et al. [@amos2018differentiable], who assumes known dynamics and reward structures and only learns 10 parameters, our method uses neural networks to represent both dynamics and reward functions without such assumptions. The metric is the cost of the learned policy. As in Amos et al., we test in two settings, pendulum without damping and with damping. Following Amos et al., their method does not model the damping effect in the assumed dynamics, so the ground-truth dynamics model is not realizable in the damping case. We also compared to an additional baseline in Amos et al., which uses a LSTM to predict the expert action. The results in Table [16](#tab:amos){reference-type="ref" reference="tab:amos"} show our method performs slightly worse in the no damping case but noticeably better in the damping case. This is because Amos et al. assumes correct dynamics in the no damping case and learns only 10 unknown parameters, whereas the assumed dynamics structure is incorrect in the damping case; we use fully-connected neural networks to represent the dynamics function, avoiding such assumptions. It is generally difficult to know the exact correct dynamics function structure, especially for tasks with complex dynamics (e.g., with contacts) and high-dimensional observations (images and point clouds).

# Implementation Details {#app:implementation}

In this section, we describe the implementation details of for the model-based RL experiments. For the imitation learning part, the code structure is very similar to this model-based RL implementation. For more detailed information, please refer to the code we will release upon acceptance of the paper. We implement on top of the open-source implementation of TD-MPC [@hansen2022temporal] from the authors. Below we show the pseudo-code of the training function in .

    def train():
        """
        Training code
        """
        for step in range(total_steps):
            obs = env.reset()
            # Differentiable trajectory optimization and update model
            action, info = agent.plan_theseus_update(obs)
            # Env step
            obs, reward, done, _ = env.step(action.cpu().numpy())
            # collect data in buffer and update model (TD-MPC loss)
    	replay_buffer += (obs, action, reward, done)
            agent.update(replay_buffer)

Then, we demonstrate how the policy gradient loss is computed by differentiable trajectory optimization in with PyTorch-like pseudocode:

    def plan_theseus_update(obs):
        """
        Differentiable trajectory optimization and update model using policy 
        gradient loss.
        h, R, Q, d: model components.
        c0: loss coefficients.
        """
        import theseus as th
        
        # Encode first observation
        z = self.model.h(obs)
        
        # Get initialization action from pi
        init_actions = self.model.pi(z)
        
        # Theseus variable
        actions = th.Vector(tensor=actions, name="actions")
        obs = th.Variable(obs, name="obs")
        
        # Cost Function and Objective
        cost_function = th.AutoDiffCostFunction([obs], [action]
            ,value_cost_fn)
        objective = th.Objective().add(cost_function)
        
        # Trajectory optimization optimizer
        theseus_optim = th.TheseusLayer(th_optimizer)
        
        # Theseus layer forward
        theseus_inputs = {"actions": init_actions, "obs": obs}
        updated_inputs, info = theseus_optim.forward(theseus_inputs)
        updated_actions = updated_inputs['actions']
        
        # Update model using policy gradient losss
        a_loss = - torch.min(*self.model.Q_s(obs, updated_actions[0]))*c0
        a_loss.backward()
        optim_a.step()

-For model-based reinforcement learning, We provide the network details for the added networks we used upon TD-MPC, which are the twin Q networks $\tilde{Q}_\phi$ learned in the original state space for computing the deterministic policy gradient.

    (Q_s1): Sequential(
        (0): Linear(in_features=S, out_features=256)
        (1): ELU(alpha=1.0)
        (2): Linear(in_features=256, out_features=Z))
        (3): Linear(in_features=Z+A, out_features=512)
        (4): LayerNorm((512,), elementwise_affine=True)
        (5): Tanh()
        (6): Linear(in_features=512, out_features=512)
        (7): ELU(alpha=1.0)
        (8): Linear(in_features=512, out_features=1))
    (Q_s2): Sequential(
        (0): Linear(in_features=S, out_features=256)
        (1): ELU(alpha=1.0)
        (2): Linear(in_features=256, out_features=Z))
        (3): Linear(in_features=Z+A, out_features=512)
        (4): LayerNorm((512,), elementwise_affine=True)
        (5): Tanh()
        (6): Linear(in_features=512, out_features=512)
        (7): ELU(alpha=1.0)
        (8): Linear(in_features=512, out_features=1))

For Imitation Learning, The default network details are as follows. Note that for Robomimic [@mandlekar2021matters] and Push-T tasks, we use the RNN-encoder from Robomimic; for ManiSkill [@mu2021maniskill; @gu2023maniskill2] tasks, we use the PointNet encoder from ManiSkill2 [@gu2023maniskill2].

    (ho): Sequential(
        (0): Linear(in_features=S, out_features=256)
        (1): ELU(alpha=1.0)
        (2): Linear(in_features=256, out_features=256)
        (3): ELU(alpha=1.0)
        (4): Linear(in_features=256, out_features=Zs))
    (ha): Identity
    (hl): Sequential(
        (0): Linear(in_features=Zs+A, out_features=256)
        (1): ELU(alpha=1.0)
        (2): Linear(in_features=256, out_features=256)
        (3): ELU(alpha=1.0)
        (4): Linear(in_features=256, out_features=128))
    (R): Sequential(
        (0): Linear(in_features=Zs+A+64, out_features=512)
        (1): ELU(alpha=1.0)
        (2): Linear(in_features=512, out_features=512)
        (3): ELU(alpha=1.0)
        (4): Linear(in_features=512, out_features=1))
    (d): Sequential(
        (0): Linear(in_features=Zs+A+64, out_features=512)
        (1): ELU(alpha=1.0)
        (2): Linear(in_features=512, out_features=512)
        (3): ELU(alpha=1.0)
        (4): Linear(in_features=512, out_features=Zs+64))

Hyperparameters used for for both model-based RL and imitation learning are shown in Tab [17](#tab:hyperparam){reference-type="ref" reference="tab:hyperparam"}. In model-based RL, we use the same parameters with TD-MPC [@hansen2022temporal] whenever possible.

::: {#tab:hyperparam}
  Hyperparameter                                             Value                    
  ---------------------------------------- ------------------------------------------ --
  Model-based RL                                                                      
  Max planning iterations                                   100 (50)                  
  Planning step size                                      1e-4 (5e-3)                 
  Discount factor                                             0.99                    
  Action loss coefficient (c0)                                 1                      
  optimizer                                 Adam($\beta_1 = 0.9$, $\beta_2 = 0.999$)  
  Gradient Norm                                                10                     
  Planning horizon schedule                          1 $\to$ 5 (25k steps)            
  Batch size                                                  256                     
  Latent dimension                                             50                     
  Sampling technique                           PER($\alpha = 0.6$, $\beta = 0.4$)     
  Learning rate                                               1e-3                    
  Imitation Learning                                                                  
  Max planning iterations                                     100                     
  Planning step size                                          1e-4                    
  Planning horizon schedule                                    1                      
  Latent dimension                                             50                     
  Posterior Gaussian dimension                                 64                     
  KL coefficien                                                1                      
  Learning rate                                               3e-4                    
  Learning rate (MetaWorld)                                   3e-3                    
  GMM Num Modes                                                5                      
  RNN Seq Len                                                  16                     
  RNN Hidden Dim                                              1000                    
  Point Cloud Sampled Points (ManiSkill)                      1200                    
  Point Cloud Sampled Points (MetaWorld)                      512                     

  : Hyperparameters used in .
:::

[]{#tab:hyperparam label="tab:hyperparam"}

# Environment Details

For model-based reinforcement learning evaluation, we use 15 visual continuous control tasks from Deepmind Control Suite (DMC). For imitation learning, we use 13 tasks (detailed information can be found in Table [\[tab:task_sum\]](#tab:task_sum){reference-type="ref" reference="tab:task_sum"}) from Robomimic [@mandlekar2021matters], IBC [@florence2022implicit], ManiSkillp [@mu2021maniskill], and ManiSkill2 [@gu2023maniskill2].

[]{#tab:task_sum label="tab:task_sum"}

We visualize the keyframes of the imitation learning tasks in Fig [8](#fig:task_vis){reference-type="ref" reference="fig:task_vis"} and Fig [9](#fig:metaworld_task_vis){reference-type="ref" reference="fig:metaworld_task_vis"}.

::::: {#fig:task_vis .figure latex-placement="h"}
::: center
![](Wan2024DiffTORI_figs/task_vis.png){width="72%"}
:::

::: caption
Visualization of the tasks for imitation learning in RoboMimic and ManiSkill.
:::
:::::

::::: {#fig:metaworld_task_vis .figure latex-placement="h"}
::: center
![](Wan2024DiffTORI_figs/Metaworld_tasks.png){width="99%"}
:::

::: caption
Visualization of the tasks for imitation learning in Metaworld.
:::
:::::

# More implementation details on using CVAE for imitation learning {#sec:CVAE}

We provide more details on how we instantiate with CVAE in imitation learning, in which the goal is to reconstruct the expert actions conditioned on the state. The CVAE encoder is composed of three networks: the first network is a state encoder $h^o_\theta$ that encodes the state into a latent feature vector $z^s = h^o_\theta(s_i)$, which is the conditional information in our case. The second is an action encoder $h^a_\theta$ that encodes the expert action into a latent feature vector $z^a = h^a_\theta(a^*_i)$. The last is a fusing encoder $h^l_\theta(z^s, z^a)$ that takes as input the concatenation of the state and action latent features, and outputs the mean $\mu$ and variance $\sigma^2$ of the posterior Gaussian distribution $\mathcal{N}(\cdot|\mu,\sigma^2)$. During training, the final latent state $z$ for state $s_i$ used in [\[eq:IL-traj-opt-def\]](#eq:IL-traj-opt-def){reference-type="eqref" reference="eq:IL-traj-opt-def"} is the concatenation of a sampled vector $\tilde{z}$ from the posterior Gaussian distribution $\mathcal{N}(\cdot|\mu,\sigma^2)$, and the latent state feature vector $z^s$: $z = [\tilde{z}, z^s], \tilde{z}\sim \mathcal{N}(\cdot|\mu,\sigma^2)$.

The latent state $z$ will then be used as input for the decoder, which consists of the reward function $R_\theta$, and the dynamics function $d_\theta$. Trajectory optimization is performed with the reward and dynamics function in the decoder to solve [\[eq:IL-traj-opt-def\]](#eq:IL-traj-opt-def){reference-type="eqref" reference="eq:IL-traj-opt-def"} to generate the reconstructed action $a^*(\theta; s_i)$. The loss for training the CVAE is the evidence lower bound (ELBO) on the demonstration data: $$\begin{equation}
        \mathcal{L}^{IL}_{\model{}}(\theta) = \sum_{i=1}^N ||a(\theta; s_i) - a^*_i||_2^2 - \beta \cdot \text{KL}(\mathcal{N}(\cdot|\mu,\sigma^2)|\mathcal{N}(0, I)),
\end{equation}$$ where $\text{KL}(P || Q)$ denotes the KL divergence between distributions $P$ and $Q$. At test time, only the decoder of the CVAE is used for generating the actions. Given a state $s$, the latent state $z$ is the concatenation of the encoded latent state feature $z^s$, and a sampled vector $\tilde{z}$ from the prior distribution $\mathcal{N}(0, 1)$.

[^1]: Equal contribution. This work was performed when Weikang Wan and Ziyu Wang were interning at CMU.

[^2]: Equal Advising.
