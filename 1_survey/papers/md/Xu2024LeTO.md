---
citation_key: Xu2024LeTO
arxiv_id: 2401.17500
arxiv_url: https://arxiv.org/abs/2401.17500
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-24T15:35:37Z
origin: ai+web
reviewed: false
---

::: IEEEkeywords
Robotic manipulation, imitation learning, differentiable optimization.
:::

# Introduction {#sec:intro}

Imitation learning [@pomerleau1988alvinn] focuses on the derivation of robot policies from demonstrations. This process can be formulated as a supervised learning task, with the aim of learning the mapping between observations and robot actions. Through imitation learning, robots can perform highly complex and diverse tasks [@chi2024universal; @xu2024unit; @fu2024mobile; @zhu2022viola; @wang2024poco; @xu2023gan; @pignat2021generative]. Moreover, recent studies have shown the feasibility of conducting imitation learning directly from manipulation videos [@bahl2022human; @wang2023mimicplay; @qian2023robot].

However, ensuring the safety of robots is very important due to the interaction between robots and the real world. In contrast to optimization-based trajectory generation methods, imitation learning often exhibits greater uncertainty, which can lead to system instability, reduced robustness, and safety concerns. Hence, compared to other supervised learning problems, this poses novel and exceptional challenges in safety for imitation learning.

Existing research focus on different aspects and challenges of imitation learning, such as improving action accuracy by addressing compounding errors [@zhao2023learning] and representing multi-modal distributions by implicit policy [@jarrett2020strictly; @florence2022implicit; @chi2023diffusionpolicy]. However, these methods overlook critical aspects of safety and smoothness of the generated trajectories. For robotic systems, their behaviors must meet specific constraints to ensure the safety of the system. Moreover, for certain tasks, robot actions also need to meet specific constraints to ensure their successful completion. In addition, adding explainable constraints for neural network-based algorithms, often called "black boxes\", is much harder than for traditional model-based methods.

::::: {#fig:firstPage .figure latex-placement="t"}
::: overpic
images/first_page_v3.png
:::

::: caption
In LeTO, we enable the model to end-to-end generate actions in a safe and constraint-controlled fashion without extra modules. To the best of our knowledge, LeTO is the first visuomotor imitation learning framework that not only utilizes differentiable optimization but also demonstrates its efficacy in real-world robotic manipulation tasks.
:::
:::::

In this paper, we propose LeTO, learning constrained visuomotor policy with differentiable trajectory optimization. The strengths and novelties of our method are as follows.

1\) **Differentiable optimization layer:** We integrate a differentiable optimization layer into the neural network and formulate it as a trajectory optimization problem. We demonstrate that the proposed differentiable optimization layer is feasible for optimization during training and capable of effective model representation. To the best of our knowledge, our work is the first visuomotor imitation learning framework that not only utilizes differentiable optimization but also demonstrates its efficacy in both simulation and real-world robotic manipulation tasks.

2\) **Safe and constrained action generation:** In our approach, we formulate the optimization layer as a trajectory optimization problem. Through this approach, the policy generates constrained trajectories, enhancing the overall safety and smoothness of robot actions. Since the model incorporates position, velocity, and acceleration constraints during end-to-end training, it ensures robot safety without compromising performance when deploying the model as a real-time policy. Compared to the "black box\" characteristics of neural networks, our approach can be described as a "gray box\" that combines the safety and interpretability of optimization-based trajectory generation with the powerful representational capabilities of neural networks. LeTO balances the objectives of skill learning and trajectory optimization with constraint guarantees.

In Section [3](#sec:app){reference-type="ref" reference="sec:app"}, we will introduce the specific methodologies of LeTO, followed by the presentation of experimental results from simulations and real-world scenarios in Sections [4](#sec:simu){reference-type="ref" reference="sec:simu"} and [5](#sec:real){reference-type="ref" reference="sec:real"}, respectively. Section [6](#sec:diss){reference-type="ref" reference="sec:diss"} will be the discussion section and will also propose future research questions that are promising and intriguing in our opinion.

# Related work

## Trajectory Optimization

Trajectory optimization is pivotal in generating safe and smooth trajectories for robots and remains an active area of research. CHOMP [@zucker2013chomp] approaches trajectory optimization by gradient techniques, focusing on optimizing the trade-off between safety and smoothness. TrajOpt [@schulman2014motion] uses sequential convex optimization to generate smooth and collision-free trajecotries and can use naive straight-line initializations that might be in collision. The minimum-snap trajectory optimization [@mellinger2011minimum] uses piecewise polynomials to represent the trajectory and is optimized by quadratic programs. The work in [@zhang2020optimization] proposes a method for reformulating nondifferentiable collision avoidance constraints into smooth, differentiable constraints and enables real-time optimization-based trajectory planning.

In LeTO, we innovatively combine trajectory optimization with imitation learning by differentiable optimization, to generate smooth and constraint-compliant trajectories during policy rollout. Our model is trained end-to-end. During the training process, LeTO not only learns the policy from human demonstrations but also learns the appropriate trajectory optimization parameters suitable for the policy. Moreover, we would like to clarify that our paper does not introduce a new trajectory generation algorithm. Rather, it focuses on presenting an imitation learning algorithm. The entire discussion within our paper is centered on this aspect of imitation learning.

## Imitation Learning

The basic way of imitation learning explicitly maps observations to actions [@pomerleau1988alvinn; @zhang2018deep; @florence2019self; @bojarski2016end; @ross2011reduction; @rahmatizadeh2018vision]. It can be trained using regression loss. However, these policies are not ideal for capturing multi-modal distributions [@florence2022implicit].

Previous works have aimed to represent multi-modal distributions by converting the regression into classification [@wu2020spatial; @zeng2021transporter; @avigal2022speedfolding], using action discretization coupled with a multi-task action correction [@shafiullah2022behavior], using MDNs [@mandlekar2022matters], and using implicit modeling that including energy-based model [@florence2022implicit; @jarrett2020strictly] and diffusion model [@chi2023diffusionpolicy]. However, these methods overlook critical aspects of safety for robotic systems. For robotic systems, their behaviors must meet specific constraints to ensure the safety of the system and the successful completion of tasks.

LeTO focuses on combining explainable and model-based trajectory optimization with imitation learning. In this way, LeTO can be end-to-end trained and generate action in a safe and constraint-controlled fashion without extra modules.

## Differentiable Optimization in Robot Learning

Previous works utilize differentiable optimization to model discontinuous functions and dynamics [@Pfrommer2020; @Bianchini2022]. Furthermore, some works focus on combining model-based methods with neural networks through differentiable optimization, such as using differentiable MPC [@amos2018differentiable] and koopman operator [@retchin2023koopman]. However, these methods are not suitable for tasks with high-dimensional observations, such as using camera images from multiple viewpoints.

The work in [@xu2024letac] proposes a tactile-reactive grasping controller that combines image encoder and differentiable MPC. However, it cannot be used for more general policy learning.

For robot navigation and obstacle avoidance, various end-to-end learning frameworks are proposed that are embedded with differentiable optimization, such as the use of the control barrier function [@xiao2021barriernet], gradient-based correction [@diehl2022differentiable], and stack prediction, planning, and control in a differentiable way [@karkus2023diffstack]. However, all of these methods are not suitable for performing manipulation tasks.

DiffTOP [@wan2024difftop] is a method that integrates differentiable trajectory optimization as the policy representation to generate actions. In integrating imitation learning, DiffTOP focuses on capturing multi-modal distributions. However, it cannot generate safe and constrained trajectories. In contrast, LeTO focuses on how the integration of differentiable trajectory optimization into the imitation learning framework enables the generation of trajectories that not only perform tasks effectively but also satisfy constraints.

Another category of methods closely related to LeTO is riemannian motion policy (RMP) [@ratliff2018riemannian] and its extensions [@li2021rmp2; @cheng2020rmp]. Specifically, the works in [@li2021rmp2; @cheng2020rmp] enhance RMP's integration into end-to-end robot learning by incorporating automatic differentiation. This enables end-to-end training and inference for policies with RMP structures. Methods based on RMP are particularly focused on generating motion in spaces with high degrees of freedom and nonlinear dynamics. In contrast, LeTO offers a capable form of generating constrained motion at the task space trajectory level with differentiable optimization. This advantage makes it better suited for adaptation to visuomotor policies and demonstrates superior performance in real tasks. To the best of our knowledge, our work is the first visuomotor imitation learning framework that not only utilizes differentiable optimization but also demonstrates its efficacy in both simulation and real-world robotic manipulation tasks.

# Approach {#sec:app}

In this paper, we assume access to an offline trajectories dataset of the task we want to perform. The goal is to learn a policy from this dataset offline and can successfully carry out the task by running the policy online. The overview of LeTO is shown in Fig. [2](#fig:leto_model){reference-type="ref" reference="fig:leto_model"}. In this section, we will detail the design of the model.

::::: {#fig:leto_model .figure latex-placement="t"}
::: overpic
images/leto_model.png
:::

::: caption
Overview of LeTO. We enable the model to end-to-end generate actions in a safe and constraint-controlled fashion by integrating a differentiable trajectory optimization layer.
:::
:::::

::::: {#fig:sampling .figure latex-placement="t"}
::: overpic
images/sampling.pdf
:::

::: caption
Illustration of training data sampling.
:::
:::::

## Training Data Sampling

In this paper, we categorize actions into two types: one is discrete actions, such as grasping and releasing; the other is continuous actions, such as the motion of the robot. For continuous actions, we consider the velocity/increment of the end-effector as the action [@mandlekar2022matters; @mandlekar2020learning; @mandlekar2020iris; @shafiullah2022behavior; @zhang2018deep; @florence2019self]. Denote the dataset as $$\mathcal{D}=\left\{\left(o_0^i, y_0^i, o_1^i,y_1^i, \ldots, o_{T^i_d}^i,y_{T^i_d}^i\right)\right\}_{i=1}^{N_d},$$ where $o$ represents the observations of the robot, such as images of the cameras with different views and robot states and $y\in\mathbb{R}^{D_y}$ represents the demonstrated action aligned with the observation $o$. $N_d$ is the total number of demonstrated trajectories, $T_d$ is the total length of a trajectory, and $D_y$ is the dimension of action $y$.

Inspired by model predictive control and diffusion policy [@chi2023diffusionpolicy], in LeTO, we predict an action sequence at each time step. Moreover, we care about how to predict trajectories that satisfy constraints rather than action sequences simply fitting the human demonstration. Therefore, before training, we first sample many fixed-length sequences in following format from the dataset $$\left(o_{t_0}, \mathbf{y}_{t_0},o_{{t_0}+1}, \mathbf{y}_{{t_0}+1}, \ldots, o_{t_0+T_s-1}, \mathbf{y}_{t_0+T_s-1}\right)
,$$ where $\mathbf{y}_t = \left[
{y}_t^{\mathrm{T}},{y}_{t+1}^{\mathrm{T}},\ldots,{y}_{t+T_p-1}^{\mathrm{T}}
\right]^{\mathrm{T}}\in \mathbb{R}^{T_pD_y}$. $T_s$ is the length of each data sampling and $T_p$ is the length of the predicted action sequence, as shown in Fig. [3](#fig:sampling){reference-type="ref" reference="fig:sampling"}. The learning objective is to minimize errors between the predicted $\hat{\mathbf{y}}^*_t$ and $\mathbf{y}_t$ (e.g. using MSE loss to assess the distance between them), as shown in Fig. [2](#fig:leto_model){reference-type="ref" reference="fig:leto_model"}. During policy rollout, the robot will execute the first $T_a$-step actions of $\hat{\mathbf{y}}^*_t$, and then repeat the same process based on new observations. This process is typically called receding horizon planning/control.

Continuous actions need to be constrained to ensure actions' safety and smoothness, while discrete actions do not. Therefore, we define a selection matrix $S$ to pick the continuous action vector $v$ that must be constrained. $$\begin{align}
\label{eq:select}
v = Sy\in\mathbb{R}^{D_v}.
\end{align}$$ As mentioned earlier, we focus on a velocity-based action space, so here $v$ refers to the velocity at which the robot is being controlled and $D_v$ is the dimension of $v$.

## Observation Encoder

The observation encoder maps observations, such as raw RGB images and robot states, to a latent embedding $e$ and is trained end-to-end with LeTO. To capture the sequential correlation of the task, we use a recurrent neural network (RNN) architecture, $E_{\theta}$, where the right subscript $\theta$ represents the parameters of the network. We choose long short-term memory (LSTM) as our RNN model. At each time step, $e_t, h_{t+1}=E_\theta\left(o_t, h_t\right),$ where $h$ is the hidden state. We define $e_t \in \mathbb{R}^{T_pD_y}$. More detailed reasons of setting the dimension as $T_pD_y$ can be seen in Section [3.3](#subsec:dto){reference-type="ref" reference="subsec:dto"}.

## Differentiable Trajectory Optimization Layer {#subsec:dto}

The differentiable trajectory optimization (DTO) layer maps the embedding $e_t$ to a predicted action sequence $\hat{\mathbf{y}}_t = \left[
\hat{y}_t^{\mathrm{T}},\hat{y}_{t+1}^{\mathrm{T}},\ldots,\hat{y}_{t+T_p-1}^{\mathrm{T}}
\right]^{\mathrm{T}}\in \mathbb{R}^{T_pD_y}$. In this section, we will show how to design this layer based on trajectory optimization, learn this layer during training, and integrate it with the entire neural network.

By equation [\[eq:select\]](#eq:select){reference-type="eqref" reference="eq:select"}, the predicted velocity command sequence

$$\begin{align}
\hat{\mathbf{v}}_t = \mathbf{S}\hat{\mathbf{y}}_t = \left[
\hat{v}_t^{\mathrm{T}},\hat{v}_{t+1}^{\mathrm{T}},\ldots,\hat{v}_{t+T_p-1}^{\mathrm{T}}
\right]^{\mathrm{T}} \in \mathbb{R}^{T_pD_v},\label{eq:select2}
\end{align}$$ where $\mathbf{S} = \text{blkdiag}\left(S,\dots,S \right)
    \in \mathbb{R}^{T_pD_v \times T_pD_y}$. Then the predicted acceleration sequence and position sequence are

$$\begin{align}
\hat{\mathbf{a}}_t &= \left[\hat{a}_t^{\mathrm{T}},\hat{a}_{t+1}^{\mathrm{T}},\ldots,\hat{a}_{t+T_p-2}^{\mathrm{T}}\right]^{\mathrm{T}} \notag\\
 & = \frac{1}{\Delta t}\left[\hat{v}_{t+1}^{\mathrm{T}}-\hat{v}_{t}^{\mathrm{T}},\ldots,\hat{v}_{t+T_p-1}^{\mathrm{T}} - \hat{v}_{t+T_p-2}^{\mathrm{T}}\right]^{\mathrm{T}}\notag\\
 & =  \frac{1}{\Delta t}\left[ \begin{matrix}
-1 & 1 &  &  &  \\
 & -1 & 1 &  &  \\
 &  & \ddots & \ddots &  \\
 &  &  & -1 & 1 
\end{matrix}  \right]\hat{\mathbf{v}}_t\notag\\
 & = \mathbf{A}_{\text{diff}} \hat{\mathbf{v}}_t \in \mathbb{R}^{T_pD_v-D_v},\label{eq:acc}\\
\hat{\mathbf{p}}_t &= \left[\hat{p}_{t+1},\ldots,\hat{p}_{t+T_p-1}\right]^{\mathrm{T}}\notag\\
                    & = 
\left[ 
\begin{matrix}
p_t   \\
p_t   \\
\vdots  \\
p_t 
\end{matrix}  
\right] + 
\left[ 
\begin{matrix}
\Delta t &  &  &    \\
\Delta t& \Delta t &    \\
 \vdots& \vdots & \ddots &  \\
\Delta t & \Delta t & \ldots &  \Delta t 
\end{matrix}  
\right]\hat{\mathbf{v}}_t\notag\\
&= \mathbf{p}_{t,0} + \mathbf{A}_{\text{inte}} \hat{\mathbf{v}}_t\in \mathbb{R}^{T_pD_v-D_v},
\label{eq:posi}
\end{align}$$ where $\hat{p}_{t+i} = {p}_{t} + \hat{v}_{t}\Delta t+\dots+\hat{v}_{t+i-1}\Delta t, i = 1,\ldots,T_p-1$, and $p_t$ is the robot end-effector position at time step $t$.

The sequence $\hat{\mathbf{p}}_t, \hat{\mathbf{v}}_t, \text{and}~\hat{\mathbf{a}}_t$ together constitutes the trajectory generated by the policy. To optimize the trajectory, we must consider the relationship between $\hat{\mathbf{p}}_t, \hat{\mathbf{v}}_t, \text{and}~\hat{\mathbf{a}}_t$ and human demonstration, as well as the constraints of $\hat{\mathbf{p}}_t, \hat{\mathbf{v}}_t, \text{and}~\hat{\mathbf{a}}_t$. Based on this, the forward pass of the DTO layer is the following optimization problem:

$$\begin{align}
\hat{\mathbf{y}}^{\star}_t&=\underset{\hat{\mathbf{y}}_t}{\operatorname{argmin}} \frac{1}{2} \hat{\mathbf{y}}_t^{\mathrm{T}} \mathbf{Q} \hat{\mathbf{y}}_t+e_t^{\mathrm{T}} \hat{\mathbf{y}}_t +\frac{\alpha}{2} \hat{\mathbf{a}}_t^{\mathrm{T}} \hat{\mathbf{a}}_t, \label{eq:opt1}\\
\text { subject to }~&b_{\text{min}} \leq A_{\text{pos}} \hat{p}_{t+i} \leq b_{\text{max}},i = 1,\ldots,T_p-1,\notag\\
&v_{\text{min}}\leq \hat{v}_{t+j} \leq {v}_{\text{max}},j = 0,\ldots,T_p-1,\notag\\
 &a_{\text{min}} \leq \hat{a}_{t+k} \leq a_{\text{max}}, k = 0, \ldots T_p-2.\notag
\end{align}$$ Rewrite the optimization problem [\[eq:opt1\]](#eq:opt1){reference-type="eqref" reference="eq:opt1"} by equations [\[eq:select2\]](#eq:select2){reference-type="eqref" reference="eq:select2"}, [\[eq:acc\]](#eq:acc){reference-type="eqref" reference="eq:acc"}, and [\[eq:posi\]](#eq:posi){reference-type="eqref" reference="eq:posi"}, then we have $$\begin{align}
\hat{\mathbf{y}}^{\star}_t&=\underset{\hat{\mathbf{y}}_t}{\operatorname{argmin}} \frac{1}{2} \hat{\mathbf{y}}_t^{\mathrm{T}} \bar{\mathbf{Q}} \hat{\mathbf{y}}_t+e_t^{\mathrm{T}} \hat{\mathbf{y}}_t,\label{eq:opt2}\\
\text { subject}&~\text{to}\notag\\
&\mathbf{b}_{\text{min}} \leq \mathbf{A}_{\text{pos}} (\mathbf{p}_{t,0} + \mathbf{A}_{\text{inte}} \mathbf{S}\hat{\mathbf{y}}_t) \leq \mathbf{b}_{\text{max}},\label{eq:posi_con}\\
&\mathbf{v}_{\text{min}}\leq \mathbf{S}\hat{\mathbf{y}}_{t} \leq \mathbf{v}_{\text{max}},\label{eq:vel_con}\\
 &\mathbf{a}_{\text{min}} \leq \mathbf{A}_{\text{diff}}\mathbf{S}\hat{\mathbf{y}}_t \leq \mathbf{a}_{\text{max}},\label{eq:acc_con}\\
 \text{where}&~\bar{\mathbf{Q}} = (\mathbf{Q}+\alpha \mathbf{S}^\mathrm{T}\mathbf{A}_{\text{diff}}^\mathrm{T}\mathbf{A}_{\text{diff}} \mathbf{S}), \notag\\
 &~\mathbf{A}_{\text{pos}} = \text{blkdiag}\left(A_{\text{pos}} ,\dots,A_{\text{pos}}  \right) \notag\\
    &~~~~~~~~\in \mathbb{R}^{(T_pD_v-D_v) \times (T_pD_v-D_v)}. \notag
\end{align}$$

The coefficient $\alpha$ controls the smoothness of the trajectory. It can be observed in [\[eq:opt1\]](#eq:opt1){reference-type="eqref" reference="eq:opt1"} that the larger the value of $\alpha$, the higher the cost associated with the sum of accelerations, leading the optimization problem to generate trajectories with a smaller sum of accelerations. $A_{\text{pos}}$ and $b_{\text{max,min}}$ define the convex constraints that the position must satisfy. $v_{\text{max,min}}$ and $a_{\text{max,min}}$ define the constraints for the velocity and acceleration of the trajectory. $\alpha,A_{\text{pos}},b_{\text{max,min}},v_{\text{max,min}}$ and $a_{\text{max,min}}$ are interpretable and model-based, so we do not need to learn these parameters during training. Instead, it is advisable to specify them according to the requirements of the task. In contrast, $\mathbf{Q}\in \mathbb{R}^{T_pD_y}$ is a parameter that we need to learn during training. Next, we will demonstrate how to learn $\mathbf{Q}$ and its specific meaning in our trajectory optimization problem.

Optimization problem [\[eq:opt2\]](#eq:opt2){reference-type="eqref" reference="eq:opt2"} is a quadratic program (QP). Therefore, the layer [\[eq:opt2\]](#eq:opt2){reference-type="eqref" reference="eq:opt2"} can perform forward pass and backpropagation in batch form as long as it is always feasible in the training process [@amos2017optnet]. The feasibility of [\[eq:opt2\]](#eq:opt2){reference-type="eqref" reference="eq:opt2"} can be guaranteed by ensuring $\mathbf{Q}$ symmetric positive definite [@boyd2004convex]. To achieve that, we use a Cholesky factorization $$\mathbf{Q}=\mathbf{L} \mathbf{L}^{\mathrm{T}} + \epsilon \mathbf{I},$$ and directly learn $\mathbf{L}$ , where $\mathbf{L}$ is a lower triangular matrix and $\epsilon$ is a very small scalar (e.g. $1\times10^{-4}$). By observing optimization problem [\[eq:opt2\]](#eq:opt2){reference-type="eqref" reference="eq:opt2"}, Remark [1](#rm:1){reference-type="ref" reference="rm:1"} can be derived.

::: {#rm:1 .remark}
**Remark 1** (feasibility of the differentiable optimization layer). *If the constraint $\mathbf{b}_{\rm{min}} \leq \mathbf{A}_{\rm{pos}} \mathbf{p}_{t,0} \leq \mathbf{b}_{\rm{max}}$ is satisfied at each time step $t$, the optimization problem is always feasible, regardless of how $\mathbf{L}$ and $e_t$ change. This means that the optimization problem remains consistently feasible, which ensures a stable training process. $\mathbf{b}_{\rm{min}} \leq \mathbf{A}_{\rm{pos}} \mathbf{p}_{t,0} \leq \mathbf{b}_{\rm{max}}$ represents that the human demonstrations should satisfy the position constraints. Additionally, human demonstrations do not need to satisfy the velocity and acceleration constraints strictly, because they have nothing to do with the feasibility of the optimization problem. Further more, for human demonstration, satisfying position constraints is much easier than satisfying velocity and acceleration constraints.*
:::

Based on the fact that $\mathbf{Q}$ is symmetric positive definite, the optimization problem [\[eq:opt2\]](#eq:opt2){reference-type="eqref" reference="eq:opt2"} can be converted to the following least squares problem:

$$\begin{align}
 &\hat{\mathbf{y}}^{\star}_t=\underset{\hat{\mathbf{v}}_t}{\operatorname{argmin}} \frac{1}{2}\|\bar{\mathbf{L}}^{\mathrm{T}} \hat{\mathbf{y}}_t-{\bar{e}_t}\|^2,\label{eq:opt3}\\
&\text { subject to }~\eqref{eq:posi_con}, \eqref{eq:vel_con}, \text{and}~ \eqref{eq:acc_con},\notag\\
&\text { where }~\bar{\mathbf{Q}}=\bar{\mathbf{L}} \bar{\mathbf{L}}^{\mathrm{T}},\notag \\
&~~~~~~~~~~{e_t}=-\bar{\mathbf{L}} {\bar{e}_t}.\notag
\end{align}$$ Based on Cholesky factorization, $\bar{\mathbf{L}}$ is a lower triangular matrix with real and positive diagonal entries. By observing optimization problem [\[eq:opt3\]](#eq:opt3){reference-type="eqref" reference="eq:opt3"}, Remark [2](#rm:2){reference-type="ref" reference="rm:2"} can be derived.

::: {#rm:2 .remark}
**Remark 2** (representational power). *DTO layer actually optimizes a linear transformation under motion constraints. Since $\bar{\mathbf{L}}$ is a lower triangular matrix and it is fully ranked, the linear transformation here is $$\hat{\mathbf{y}}^{\star}_t = -({\bar{\mathbf{L}}^{\mathrm{T}}})^{-1}\bar{\mathbf{L}}^{-1}e_t.$$ Since the observation encoder is just a normal LSTM architecture, it is already has the power of representing the policy. Therefore, the whole model including the DTO layer has the power to fit the human demonstration.*
:::

## Policy Deployment

When the policy is deployed on the robot, the RNN is unrolled one-step at a time, $e_t, h_{t+1}=E_\theta\left(o_t, h_t\right)$. The hidden state $h$ is refreshed every $T_s$ steps. In addition, the training is done on discrete trajectory clips while the robot trajectory is continuous in reality. Therefore, the forward pass of the DTO layer need to add a new constraint during test time to fully constrain the motion generation.

$$\begin{align*}
\hat{\mathbf{y}}^{\star}_t=\underset{\hat{\mathbf{y}}_t}{\operatorname{argmin}} &\frac{1}{2} \hat{\mathbf{y}}_t^{\mathrm{T}} \bar{Q} \hat{\mathbf{y}}_t+e_t^{\mathrm{T}} \hat{\mathbf{y}}_t,\\
\quad \text { subject to }&~\eqref{eq:posi_con}, \eqref{eq:vel_con}, \text{and}~\eqref{eq:acc_con},\\
 a_{\text{min}}\Delta t &\leq \hat{v}_{t} - \hat{v}_{t-1} \leq  a_{\text{max}}\Delta t
\end{align*}$$ where $\hat{v}_{t-1}$ represents the last executed action for the robot at time step $t$ (executed at time step $t-1$). Adding this new constraint is to transfer the model trained on a discrete set of trajectories to continuous online trajectory optimization.

::: table*
          **Task**          **Initial States**   **Objective**   **PH**   **MH**   **Act. Dim.**   **HiPrec**   **Multi-Steps**   **Num. of Cam.**
  ------------------------ -------------------- --------------- -------- -------- --------------- ------------ ----------------- ------------------
          **Can**                 Random             Fixed        200      300           7             No             No                 2
         **Square**               Random             Fixed        200      300           7            Yes             No                 2
     **Move-the-stack**           Random            Random        100       \-           3            Yes             No                 1
   **Arrange-chopsticks**         Random             Fixed        120       \-           4             No             Yes                2

[]{#tb:task_config label="tb:task_config"}
:::

::: table*
   **Velocity Constraints** \[${v}_{\text{min}},{v}_{\text{max}}$\]   **Acceleration Constraints** \[${a}_{\text{min}},{a}_{\text{max}}$\]   **Smoothing Weight** $\alpha$   **Sampling Length** $T_s$   **Predicted Length** $T_p$
  ------------------------------------------------------------------ ---------------------------------------------------------------------- ------------------------------- --------------------------- ----------------------------
                     \[-1,1\] (normalized values)                                       \[-0.1,0.1\] (normalized values)                                   1                            12                           6

[]{#tb:train_config label="tb:train_config"}
:::

::: table*
+-------------------------------------------+---------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|                                           | Can                                                                 | Square                                                                                                                                                                                                                      |
+:=========================================:+:================================:+:================================:+:============================================================================================================:+:============================================================================================================:+
|                                           | $\mathrm{ph}$                    | $\mathrm{mh}$                    | $\mathrm{ph}$                                                                                                | $\mathrm{mh}$                                                                                                |
+-------------------------------------------+----------------------------------+----------------------------------+--------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------+
| IBC [@florence2022implicit]               | 8                                | 0                                | 3                                                                                                            | 0                                                                                                            |
+-------------------------------------------+----------------------------------+----------------------------------+--------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------+
| LSTM-GMM [@mandlekar2022matters]          | $94.6\pm2.3$                     | $94.6\pm2.3$                     | $78.7\pm6.1$                                                                                                 | $77.3\pm8.3$                                                                                                 |
+-------------------------------------------+----------------------------------+----------------------------------+--------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------+
| LSTM-GMM clipping                         | $90.7\pm4.6$                     | $89.3\pm2.3$                     | $73.3\pm8.3$                                                                                                 | $70.7\pm2.3$                                                                                                 |
+-------------------------------------------+----------------------------------+----------------------------------+--------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------+
| DiffusionPolicy [@chi2023diffusionpolicy] | $\textbf{100.0}\pm\textbf{0.0}$  | $\textbf{100.0}\pm \textbf{0.0}$ | $\textbf{98.7}\pm \textbf{2.3}$                                                                              | $\textbf{90.7}\pm\textbf{4.6}$                                                                               |
+-------------------------------------------+----------------------------------+----------------------------------+--------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------+
| DiffusionPolicy clipping                  | $98.7\pm2.3$                     | $93.3\pm4.6$                     | $92.0\pm4.0$                                                                                                 | $82.7\pm2.3$                                                                                                 |
+-------------------------------------------+----------------------------------+----------------------------------+--------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------+
| LeTO                                      | $\textbf{100.0}\pm\textbf{ 0.0}$ | $\textbf{100.0}\pm \textbf{0.0}$ | $\textbf{\textcolor[rgb]{0,0.5,0}{94.7}}\textcolor[rgb]{0,0.5,0}{\pm}\textbf{\textcolor[rgb]{0,0.5,0}{4.6}}$ | $\textbf{\textcolor[rgb]{0,0.5,0}{88.0}}\textcolor[rgb]{0,0.5,0}{\pm}\textbf{\textcolor[rgb]{0,0.5,0}{4.0}}$ |
+-------------------------------------------+----------------------------------+----------------------------------+--------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------+

[]{#tb:succ_rate_sim label="tb:succ_rate_sim"}
:::

::::: {#fig:sim_env .figure latex-placement="t"}
::: overpic
images/simulation_envs.pdf
:::

::: caption
Simulation benchmarks: pick and place the can (can task) and grasping and assembling the square nut (square task).
:::
:::::

# Simulation Evaluation {#sec:simu}

## Experimental Setup

We employed two simulation tasks used in [@mandlekar2022matters] for our simulation evaluation: pick and place the can (can task) and grasping and assembling the square nut (square task), as shown in Fig. [4](#fig:sim_env){reference-type="ref" reference="fig:sim_env"}. More details of the task configurations can be seen in Table [\[tb:task_config\]](#tb:task_config){reference-type="ref" reference="tb:task_config"}. The results demonstrate that within these two simulation tasks, LeTO not only achieves success rates comparable to diffusion policy [@chi2023diffusionpolicy], but also significantly surpasses IBC [@florence2022implicit] and LSTM+GMM [@mandlekar2022matters]. Furthermore, owing to the presence of constraints and differentiable trajectory optimization, our method exhibits superior performance in terms of generated trajectory quality compared to other methods, which is very important for robot systems.

For training parameters of diffusion policy and LSTM-GMM, we use the default configurations provided in their released code. We also do the same for our realworld evaluation. We have released our code, training data, and checkpoints for reproducing our results.

The can and square tasks are from the RoboMimic benchmark [@mandlekar2022matters]. Apart from the most basic lifting task, we opted not to include the tool hanging and transport tasks. As highlighted in [@amos2017optnet], solving optimization problems precisely, as we are doing here, exhibits cubic complexity concerning the number of variables and/or constraints. Consequently, our method's training speed for tasks like tool hanging and transport, which involve larger datasets or high-dimensional output, is sluggish, and under limited GPU computational resources, obtaining results within a short time is unfeasible. Nevertheless, as we have already demonstrated the capability of our approach to achieve high successful rates and generate high-quality trajectories through the outcomes of the two tasks mentioned above, we decided against further training on the tool hanging and transport tasks.

We train policies on 3 seeds (42, 142, 242) with batch size 64, and test in 25 different initial environments for each seed (totaling 75 conditions). For each task, we train policies on two different types of datasets: Proficient-Human (ph), and Multi-Human (mh) datasets [@mandlekar2022matters]. We report the success rate (see Table [\[tb:succ_rate_sim\]](#tb:succ_rate_sim){reference-type="ref" reference="tb:succ_rate_sim"}) of all these experiments. We also report metrics to evaluate the quality of the generated trajectories (see Tables [\[tb:can_ph\]](#tb:can_ph){reference-type="ref" reference="tb:can_ph"}, [\[tb:can_mh\]](#tb:can_mh){reference-type="ref" reference="tb:can_mh"}, [\[tb:square_ph\]](#tb:square_ph){reference-type="ref" reference="tb:square_ph"}, and [\[tb:square_mh\]](#tb:square_mh){reference-type="ref" reference="tb:square_mh"}).

::: table*
                                                         avg-mean-lin                        avg-max-lin                        avg-std-lin                        avg-mean-rot                       avg-max-rot                        avg-std-rot              num-of-opt
  ------------------------------------------- ---------------------------------- ----------------------------------- ---------------------------------- ---------------------------------- ---------------------------------- ---------------------------------- ------------
   DiffusionPolicy [@chi2023diffusionpolicy]            $8.23\pm 0.70$                     $69.78\pm 2.67$                     $8.39\pm 0.58$            $\textbf{1.03}\pm\textbf{ 0.12}$           $12.73\pm 0.78$            $\textbf{1.29}\pm \textbf{0.12}$       2
       LSTM-GMM [@mandlekar2022matters]                 $9.78\pm 3.54$                    $77.49\pm 15.16$                    $10.61\pm 3.48$            $\textbf{1.04}\pm \textbf{0.27}$           $24.58\pm 9.73$                     $2.71\pm 0.26$                1
           DiffusionPolicy clipping                     $7.73\pm 0.10$            $\textbf{10.00}\pm \textbf{0.00}$   $\textbf{3.21}\pm\textbf{ 0.06}$            $3.61\pm 0.47$            $\textbf{9.94}\pm \textbf{0.07}$            $2.45\pm 0.08$                3
               LSTM-GMM clipping                        $5.61\pm 1.03$            $\textbf{10.00}\pm \textbf{0.00}$            $3.68\pm 0.10$                     $1.16\pm 0.13$            $\textbf{9.59}\pm \textbf{0.14}$   $\textbf{1.37}\pm \textbf{0.05}$       3
                     LeTO                      $\textbf{4.36}\pm \textbf{0.10}$   $\textbf{10.00}\pm \textbf{0.00}$   $\textbf{3.47}\pm \textbf{0.03}$            $1.50\pm 0.21$            $\textbf{9.78}\pm \textbf{0.37}$            $1.73\pm 0.30$              **4**

[]{#tb:can_ph label="tb:can_ph"}
:::

::: table*
                                                         avg-mean-lin                        avg-max-lin                        avg-std-lin                        avg-mean-rot                       avg-max-rot                        avg-std-rot              num-of-opt
  ------------------------------------------- ---------------------------------- ----------------------------------- ---------------------------------- ---------------------------------- ---------------------------------- ---------------------------------- ------------
   DiffusionPolicy [@chi2023diffusionpolicy]            $5.97\pm 0.93$                     $64.85\pm 9.04$                     $7.32\pm 0.85$            $\textbf{0.60}\pm \textbf{0.06}$           $10.95\pm 1.16$            $\textbf{0.96}\pm \textbf{0.09}$       2
       LSTM-GMM [@mandlekar2022matters]                 $6.02\pm 0.78$                     $72.16\pm 1.94$                     $7.41\pm 0.36$                     $0.75\pm 0.08$                    $21.48\pm 9.64$                     $1.57\pm 0.50$                0
           DiffusionPolicy clipping                     $7.35\pm 0.14$            $\textbf{10.00}\pm \textbf{0.00}$            $3.30\pm 0.03$                     $2.74\pm 0.19$                     $9.80\pm 0.07$                     $2.26\pm 0.12$                1
               LSTM-GMM clipping                        $4.74\pm 0.46$            $\textbf{10.00}\pm \textbf{0.00}$            $3.45\pm 0.10$                     $0.79\pm 0.10$                     $9.16\pm 0.87$                     $1.19\pm 0.43$                1
                     LeTO                      $\textbf{2.66}\pm \textbf{0.68}$   $\textbf{10.00}\pm \textbf{0.00}$   $\textbf{2.60}\pm \textbf{0.31}$          ${0.74}\pm {0.22}$          $\textbf{8.28}\pm \textbf{1.04}$   $\textbf{0.98}\pm \textbf{0.24}$     **5**

[]{#tb:can_mh label="tb:can_mh"}
:::

::: table*
                                                         avg-mean-lin                        avg-max-lin                        avg-std-lin                        avg-mean-rot                       avg-max-rot                        avg-std-rot              num-of-opt
  ------------------------------------------- ---------------------------------- ----------------------------------- ---------------------------------- ---------------------------------- ---------------------------------- ---------------------------------- ------------
   DiffusionPolicy [@chi2023diffusionpolicy]            $8.17\pm 0.78$                     $70.66\pm 4.49$                     $8.65\pm 0.40$            $\textbf{0.95}\pm \textbf{0.11}$           $13.22\pm 0.80$            $\textbf{1.32}\pm \textbf{0.11}$       2
       LSTM-GMM [@mandlekar2022matters]                 $8.19\pm 2.49$                     $68.75\pm 6.52$                     $8.76\pm 1.82$            $\textbf{0.91}\pm \textbf{0.08}$           $13.81\pm 3.51$            $\textbf{1.30}\pm \textbf{0.24}$       2
           DiffusionPolicy clipping                     $6.90\pm 0.75$            $\textbf{10.00}\pm \textbf{0.00}$   $\textbf{3.36}\pm \textbf{0.06}$            $2.09\pm 0.88$            $\textbf{9.09}\pm \textbf{0.82}$            $1.75\pm 0.59$                3
               LSTM-GMM clipping               $\textbf{5.11}\pm \textbf{1.46}$   $\textbf{10.00}\pm \textbf{0.00}$   $\textbf{3.36}\pm \textbf{0.20}$   $\textbf{0.98}\pm \textbf{0.22}$   $\textbf{9.04}\pm \textbf{0.54}$   $\textbf{1.27}\pm \textbf{0.29}$     **6**
                     LeTO                      $\textbf{5.08}\pm \textbf{0.33}$   $\textbf{10.00}\pm \textbf{0.00}$   $\textbf{3.35}\pm \textbf{0.03}$            $1.28\pm 0.17$            $\textbf{9.24}\pm \textbf{0.15}$   $\textbf{1.37}\pm \textbf{0.08}$       5

[]{#tb:square_ph label="tb:square_ph"}
:::

::: table*
                                                         avg-mean-lin                        avg-max-lin                        avg-std-lin                        avg-mean-rot                       avg-max-rot                        avg-std-rot              num-of-opt
  ------------------------------------------- ---------------------------------- ----------------------------------- ---------------------------------- ---------------------------------- ---------------------------------- ---------------------------------- ------------
   DiffusionPolicy [@chi2023diffusionpolicy]            $5.42\pm 0.30$                     $60.97\pm 4.38$                     $6.61\pm 0.44$            $\textbf{0.57}\pm \textbf{0.08}$           $13.41\pm 3.45$                     $1.11\pm 0.26$                1
       LSTM-GMM [@mandlekar2022matters]                 $5.37\pm 0.66$                     $54.43\pm 6.99$                     $6.28\pm 1.00$                     $0.64\pm 0.08$                    $13.31\pm 2.66$                     $1.04\pm 0.22$                0
           DiffusionPolicy clipping                     $7.04\pm 0.42$            $\textbf{10.00}\pm \textbf{0.00}$            $3.35\pm 0.06$                     $2.41\pm 0.50$                     $9.46\pm 0.34$                     $2.04\pm 0.36$                1
               LSTM-GMM clipping                        $3.81\pm 0.44$            $\textbf{10.00}\pm \textbf{0.00}$            $3.07\pm 0.13$            $\textbf{0.63}\pm \textbf{0.04}$   $\textbf{7.80}\pm \textbf{0.23}$   $\textbf{0.85}\pm \textbf{0.04}$     **4**
                     LeTO                      $\textbf{3.08}\pm \textbf{0.04}$   $\textbf{10.00}\pm \textbf{0.00}$   $\textbf{2.70}\pm \textbf{0.01}$            $0.91\pm 0.06$            $\textbf{8.18}\pm \textbf{0.07}$            $1.09\pm 0.07$              **4**

[]{#tb:square_mh label="tb:square_mh"}
:::

::: {#tb:cons_ablation}
                              **0.05**                             **0.1**                               **0.2**                               **0.5**                                **1**
  -------------- ---------------------------------- ------------------------------------- ------------------------------------- ------------------------------------- -------------------------------------
    succ-rate                   0.88                   **[0.96]{style="color: red"}**        **[0.96]{style="color: red"}**      **[0.92]{style="color: 0,0.5,0"}**                   0.88
   avg-mean-lin   **[0.033]{style="color: red"}**    **[0.049]{style="color: 0,0.5,0"}**                  0.061                                 0.071                                 0.067
   avg-max-lin     **[0.05]{style="color: red"}**    **[0.10]{style="color: 0,0.5,0"}**                   0.20                                  0.46                                  0.58
   avg-std-lin    **[0.017]{style="color: red"}**    **[0.033]{style="color: 0,0.5,0"}**                  0.051                                 0.071                                 0.072
   avg-mean-rot   **[0.012]{style="color: red"}**    **[0.013]{style="color: 0,0.5,0"}**     **[0.012]{style="color: red"}**     **[0.013]{style="color: 0,0.5,0"}**   **[0.013]{style="color: 0,0.5,0"}**
   avg-max-rot    **[ 0.050]{style="color: red"}**   **[0.090]{style="color: 0,0.5,0"}**                  0.121                                 0.145                                 0.134
   avg-std-rot    **[0.011]{style="color: red"}**    **[0.014]{style="color: 0,0.5,0"}**   **[0.014]{style="color: 0,0.5,0"}**                  0.015                                 0.015

  : The results of LeTO on square-ph with varying acceleration constraints. To enhance readability, we have highlighted the optimal values in each metric in bold red and the second-optimal values in bold green. The acceleration results employ the same normalization as outlined in Tables [\[tb:can_ph\]](#tb:can_ph){reference-type="ref" reference="tb:can_ph"}, [\[tb:can_mh\]](#tb:can_mh){reference-type="ref" reference="tb:can_mh"}, [\[tb:square_ph\]](#tb:square_ph){reference-type="ref" reference="tb:square_ph"}, and [\[tb:square_mh\]](#tb:square_mh){reference-type="ref" reference="tb:square_mh"}
:::

[]{#tb:cons_ablation label="tb:cons_ablation"}

For the CNN+LSTM backbone of LeTO, we employ the hyperparameters selected in [@mandlekar2022matters]. The other hyperparameters for training LeTO are detailed in Table [\[tb:train_config\]](#tb:train_config){reference-type="ref" reference="tb:train_config"}. To improve learning efficiency, actions processed through LeTO are first normalized to a range between -1 and 1 [@mandlekar2022matters]. Consequently, the velocity and acceleration constraints applied here pertain to the normalized actions. See the codebase[^3] for more information of action unnormalization.

Setting velocity constraints within the range of \[-1, 1\] ensure that the trajectories generated by LeTO during both training and inference do not exceed the maximum velocity in the human demonstration data. This is a logical approach since we can assume that the maximum velocity in a high-quality human demonstration dataset is reasonable and does not lead to dangerous or unstable behavior in the robot.

The acceleration constraint of \[-0.1, 0.1\] effectively imposes additional smoothness on the trajectories. As acceleration is not directly controlled, the trajectories in the human demonstration may not be sufficiently smooth. In LeTO, imposing hard acceleration constraints optimizes the generation of higher-quality, smoother trajectories while ensuring manipulation performance.

For the simulation tests, we do not apply any position constraints, as our aim is to solely compare the success rates and the smoothness of the trajectories generated by different methods.

For the assessment of trajectory quality, we calculate the maximum acceleration, average acceleration, and acceleration standard deviation for each dimension (x,y,z, roll, pitch, and yaw) and for each environment condition (25 environments for each seed). Then we calculate the average among dimensions and environments. For example $$\text{avg-max-lin} = \frac{1}{25}\sum_{i =1}^{25}\frac{a_{x,max}^i+a_{y,max}^i+a_{z,max}^i}{3},$$ where $i$ represents the $i$-th environment and $a$ represents acceleration. "lin\" here represents linear motion and "rot\" represents rotational motion. The remaining matrices can be computed by analogy. Additionally, it is worth noting that the acceleration values here are obtained by computing the difference of the normalized velocity. It is directly proportional to the actual acceleration, and this proportionality constant is a fixed value for all experiments. We mark the values within the range of 100% to 110% of the minimum value in each metric as the optimal indicators (bolded), and denote the number of optimal indicators for each method as "num-of-opt\".

In order to investigate the impact of direct action clipping on success rate and trajectory smoothness for baselines, we implement a clipping method. It involves evaluating the difference between the generated action and the previously executed action to determine whether it falls within the range of -0.1 to 0.1, which are the same constraints that we implement for LeTO. If it exceeds this range, we apply clipping to bring it within this range. This approach restricts acceleration.

## Results and Analysis

As shown in Tables [\[tb:can_ph\]](#tb:can_ph){reference-type="ref" reference="tb:can_ph"}, [\[tb:can_mh\]](#tb:can_mh){reference-type="ref" reference="tb:can_mh"}, [\[tb:square_ph\]](#tb:square_ph){reference-type="ref" reference="tb:square_ph"}, and [\[tb:square_mh\]](#tb:square_mh){reference-type="ref" reference="tb:square_mh"}, it can be observed that LeTO significantly enhances trajectory smoothness by trajectory optimization. For example, if we unnormalize the values to true values for comparison, in Table [\[tb:can_ph\]](#tb:can_ph){reference-type="ref" reference="tb:can_ph"}, the maximum linear acceleration for LSTM-GMM is $10^{-2} \times 77.49 \times 20~\text{m}/\text{s}^2 = 15.50~\text{m}/\text{s}^2$ (which exceeds the gravitational acceleration), while for LeTO it is only 2 $\text{m}/\text{s}^2$. The average acceleration of LSTM-GMM is also about twice that of LeTO. These metrics indicate that the trajectories generated by LSTM-GMM are significantly jerkier than those produced by LeTO. The same analysis applies to diffusion policy, and we can obtain similar results.

Moreover, LeTO achieves a success rate comparable to that of diffusion policy and surpasses LSTM-GMM and IBC in these tasks. Interestingly, when clipping is applied to constrain the actions generated by the diffusion policy and LSTM-GMM, although this method sometimes increases the smoothness of the trajectory, it results in a reduction in their task success rates.

An intuitive explanation for this phenomenon is that both methods do not consider constraints during their training process; they merely fitted human demonstrations. When constraints are imposed on the actions generated by the trained models during deployment, it introduces additional factors that inevitably affect their performance. In contrast, our proposed LeTO, due to its ability to achieve end-to-end trajectory optimization while fitting demonstration data, balances the training objectives of satisfying constraints, smoothing the trajectories, and minimizing errors with demonstrations.

While all the policies we benchmark might successfully complete these tasks in simulation, constraint guarantees are crucial metrics for robotic systems. People aim for robotic systems to operate safely and reliably over the long term, not just to complete a task once. Violating constraints and producing jerky trajectories could lead to unsafe situations because neural networks are inherently uninterpretable black boxes. Moreover, if a robot consistently executes jerky trajectories to complete tasks, it places a greater burden on the hardware. Over time, these factors undermine the robustness and stability of the entire system.

Historically, trajectory optimization for robots has focused on meeting constraints to enhance system robustness. In our paper, LeTO can be seen as a \"gray box\" that offers a certain level of interpretability and can perform end-to-end trajectory optimization with hard constraints. This represents our attempt to connect trajectory optimization with robot learning. Moreover, we demonstrated that simply constraining the policy through clipping results in a decrease in performance. Therefore, we believe it is meaningful to explore how to integrate constraints into the policy to balance the objectives of skill learning and trajectory optimization with constraint guarantees. LeTO provides a practical example of how to achieve this integration.

To investigate the impact of acceleration constraints on the results of LeTO, we have conducted an ablation study on acceleration constraints (see Table [1](#tb:cons_ablation){reference-type="ref" reference="tb:cons_ablation"} for details). Through this ablation study, we can the following observations.

1. Different acceleration constraints affect the success rate of the policy. Both overly restrictive and overly lenient constraints can reduce the success rate, resulting in a trend where the success rate initially increases with the constraint values before decreasing.

2. Table [1](#tb:cons_ablation){reference-type="ref" reference="tb:cons_ablation"} demonstrates that LeTO, when implementing tight acceleration constraints, yields trajectories with notably superior smoothness based on differentiable optimization. The acceleration constraints determines the smoothness of the resulting trajectories. Tighter acceleration constraints result in smoother trajectories. As the maximum acceleration in the constraints approaches the maximum acceleration in the dataset, The trajectories generated by LeTO progressively approximate the original trajectories in the dataset.

3. Specifically, Tables  [\[tb:square_ph\]](#tb:square_ph){reference-type="ref" reference="tb:square_ph"} and [1](#tb:cons_ablation){reference-type="ref" reference="tb:cons_ablation"} show that both the unconstrained LSTM-GMM and diffusion policy, and the loosely constrained LeTO ultimately generate a maximum linear acceleration of around 0.6 and a maximum rotational acceleration of about 0.14. Under relaxed or no constraints, the trajectories generated by the learned policies resemble those in the dataset across various metrics. This indicates that the dataset trajectories' linear and rotational accelerations are approximately around 0.6 and 0.14, respectively (all values are normalized). As the constraints in LeTO transition from 1 to 0.05, the maximum linear acceleration of the trajectories it generates also transitions from 0.58 to 0.05, and the rotational acceleration transitions from 0.134 to 0.05.

4. This ablation study highlights LeTO's superiority in terms of interpretability and controllability. When adjusting constraints, the metrics of the trajectories it generates remain consistent with the design of the differentiable trajectory optimization layer. Due to the black-box nature of neural networks, they lack the capability to "control\" the final outputs, being limited only to fitting datasets. LeTO's adjustable influence on trajectories stems from the theoretical fulfillment of constraints. This ensures that regardless of the input observations, the trajectories output by LeTO will always satisfy the given constraints by trajectory optimization. Such theoretical assurances enhance the interpretability of the entire model and are crucial for long-term safety and robustness.

# Realworld Evaluation {#sec:real}

For real robot experiments, we tackled constraints-critical tasks that demand smooth and safe trajectories, which are Move-the-stack (Fig. [5](#fig:stack_overview){reference-type="ref" reference="fig:stack_overview"}) and Arrange-chopsticks (Fig. [7](#fig:chop_overview){reference-type="ref" reference="fig:chop_overview"}). We use SpaceMouse[^4] teleoperating the end-effector of the robot manipulator to collect human demonstration data. SpaceMouse is widely used for data collection in imitation learning-related research [@chi2023diffusionpolicy; @mandlekar2022matters; @zhu2022viola; @liu2022robot]. By manipulating the SpaceMouse, we can control the six degrees of freedom in the robot's end-effector velocity, as well as the gripper's grasping and releasing actions, thereby enabling the collection of data for various manipulation tasks. During the data collection process, the robot state information and images from the cameras are recorded simultaneously. More details of the task configurations can be seen in Table [\[tb:task_config\]](#tb:task_config){reference-type="ref" reference="tb:task_config"}. More details of experiments and results can be seen in the attached video.

## Move-the-stack

::::: {#fig:stack_overview .figure latex-placement="t"}
::: overpic
images/stack_overview.pdf
:::

::: caption
Move-the-stack task. The robot grasps a set of stacked objects, smoothly transport them, and ultimately place them onto a black board, ensuring none of the stacked objects fall off. The black tape is for marking a consistent grasping position.
:::
:::::

::::: {#fig:ood .figure latex-placement="t"}
::: overpic
images/ood.pdf
:::

::: caption
When chopsticks fall, which is a type of OOD data, both the diffusion policy and LeTO can still move the stacked cups and place them on the black board. In contrast, LSTM-GMM often exhibits erroneous behaviors, such as moving to incorrect locations or acting erratically.
:::
:::::

::::: {#fig:chop_overview .figure latex-placement="t"}
::: overpic
images/bowl_overview.pdf
:::

::: caption
Arrange-chopsticks task. The robot picks up randomly placed two chopsticks and arrange them neatly on a bowl.
:::
:::::

The objective of the "Move-the-stack\" task is that the robot grasps a set of stacked objects, smoothly transports them, and ultimately places them onto a black board, ensuring none of the stacked objects fall off. The initial positions of the robot and the black board are randomized. The policy inputs end-effector positions and images from a third-person perspective camera and controls the end-effector position. We introduce the velocity constraint \[-1,1\] and the acceleration constraint \[-0.25,0.25\] for LeTO. In particular, while we did not place chopsticks on top during human demonstration collection, a chopstick was added to the stacked cups during policy rollout.

For imitation learning algorithms, the task is challenging because: 1) The policy needs to generate very smooth trajectories. Any roughness in the trajectory can lead to vibrations at the robot's end-effector, causing the cups to shake. This vibration can accumulate and cause the chopstick to drop. 2) Since a chopstick is introduced during policy rollout, this out-of-distribution (OOD) observation adds greater uncertainty to the network input. This uncertainty may make the network's output jerkier, resulting in a poorer quality trajectory.

::: {#tb:move}
                     avg-acc-mean/max/std    succ-rate   acc-peak
  ----------------- ----------------------- ----------- -----------
      LSTM-GMM         0.053/0.480/0.081       4/20        0.647
   DiffusionPolicy   **0.037**/0.336/0.055     4/20        0.721
        LeTO         **0.037/0.219/0.042**   **13/20**   **0.250**

  : Metrics for evaluating the Move-the-stack task. "acc-peak\" represents the highest acceleration achieved in any of the test trials while "avg-acc-mean/max/std\" are the average of mean/max/std values across all test trials.
:::

[]{#tb:move label="tb:move"}

::: {#tb:arrange}
                     avg-contact-max   contact-peak   succ-rate
  ----------------- ----------------- -------------- -----------
      LSTM-GMM           13.2 N           27.3 N        0/20
   DiffusionPolicy       13.9 N           24.8 N      **18/20**
        LeTO           **11.7 N**       **16.1 N**    **17/20**

  : Metrics for evaluating the Arrange-chopsticks task. "contact-peak\" represents the highest contact force achieved in any of the test trials while "avg-contact-max\" is the average of max contact forces across all test trials.
:::

[]{#tb:arrange label="tb:arrange"}

The results are shown in Table [2](#tb:move){reference-type="ref" reference="tb:move"}. From the results, LeTO excels in terms of trajectory smoothness and, correspondingly, also boasts the highest success rate. This shows that due to the presence of end-to-end trajectory optimization, LeTO can robustly maintain its effectiveness even when facing OOD data. Another point worth noting is that when chopsticks fall (which is also a type of OOD data), both the diffusion policy and LeTO can still move the stacked cups and place them on the black board. In contrast, LSTM-GMM often exhibits erroneous behaviors, such as moving to incorrect locations or acting erratically (see Fig. [6](#fig:ood){reference-type="ref" reference="fig:ood"} and the attached video).

The Move-the-stack task highlights the importance of trajectory optimization. For methods solely based on neural networks, there is a lack of control over the generated trajectories, resulting in trajectories that are less smooth and more uncertain. The inherent uninterpretability of neural networks introduces greater uncertainty.

## Arrange-chopsticks

The objective of the "Arrange-chopsticks\" task is to pick up two randomly placed chopsticks and arrange them neatly on a bowl. The policy inputs end-effector poses and images from two cameras, a third-person perspective camera and a wrist-mounted camera, and controls the end-effector position, yaw angle, and grasping.

The challenges of this task include: 1. It is a relatively long-range task that requires the policy to have the capability to represent complex tasks. 2. Due to the slender nature of chopsticks, there is a high risk of the robot making forceful contact with the table when attempting to grasp them. For the sake of hardware safety, such collisions should be minimized as much as possible.

We introduce both position, velocity, and acceleration constraints for LeTO. During the demonstration, the lowest position of the robot's end-effector on the z-axis was recorded at 0.0501 m. We have opted for 0.0475 m as the z-axis positional constraint within the LeTO framework. This choice is made with the task's completion in mind, where the goal is not to prevent any contact between the robot's end-effector and the table surface, but rather to allow for the slightest possible contact that still enables the picking up of slender chopsticks.

The results are shown in Table [3](#tb:arrange){reference-type="ref" reference="tb:arrange"}. Both LeTO and diffusion policy have high success rate, but the contact forces in LeTO tests are significantly smaller. Collisions with the environment are quite common for manipulation tasks like picking up very fine chopsticks from the tabletop. One can imagine that if the table were made of glass, such collisions could be very hazardous. Moreover, consider a scenario in which a robot frequently collides with its environment without constraints. Even if this does not affect performance in the short term, it could significantly reduce the robot's lifespan over time.

The reduction in contact force with the tabletop is a result of the implementation of the LeTO differentiable optimization layer, which incorporates position constraints that allow for trajectory optimization. In contrast, existing \"black box\" approaches, which are solely based on neural networks, do not ensure outputs that consistently meet these constraints, leading to unpredictable and potentially large impact forces with the tabletop.

Given that robots physically interact with their environment and humans, factors like safety, interpretability, stability, and robustness are crucial. Fully neural network-based approaches pose challenges for real-world deployment due to their lack of interpretability. For instance, even if the algorithm performs well under most conditions, the absence of constraints means that significant deviations in a few edge cases can lead to severe problems due to the physical nature of robots.

# Discussion and Future Work {#sec:diss}

In this paper, we present LeTO, a framework for learning constrained visuomotor policy with differentiable trajectory optimization. By balancing the objective of minimizing errors with the need to satisfy trajectory constraints, LeTO allows for deployment in tasks where safety and reliability are paramount.

## Training Time and Training Stability

::: {#tb:time}
  -- -- -- --
           
  -- -- -- --

  : The training time for 20 epochs on the square ph task with a batch size of 64, conducted on a single GeForce RTX 3080. The hyperparameters for diffusion policy and LSTM-GMM are adopted from the default parameters reported in [@mandlekar2022matters; @chi2023diffusionpolicy], respectively.
:::

[]{#tb:time label="tb:time"}

As shown in Remark [1](#rm:1){reference-type="ref" reference="rm:1"}, the optimization problem of the DTO layer is always feasible during training, given that the positions (and orientations) in the dataset meet the set position constraints. The consistent feasibility of the DTO layer ensures training stability, which is evident from the training logs of LeTO available in our open-source code.

Table [4](#tb:time){reference-type="ref" reference="tb:time"} compares the training times of LSTM-GMM, diffusion policy, and LeTO. We acknowledge that one limitation of LeTO is the computational overhead introduced by the differentiable optimization layer. Future work could look into improving the computational efficiency of the differentiable optimization process, potentially through the use of more efficient solvers or by learning approximations of the optimization layer.

## LeTO in Low-data and High-data Regimes

We would like to highlight that networks with the training objective of minimizing errors to fit human demonstrated actions can easily incorporate our proposed DTO layer at the head. This suggests that for scalability, one could consider designing a LeTO variant with transformer, enhancing the model's capability to scale to large datasets. However, the time and cost involved in training could still be a limiting factor. As shown in Table [4](#tb:time){reference-type="ref" reference="tb:time"}, LeTO exhibits a significantly slower training compared to other methods. As highlighted in [@amos2017optnet], solving optimization problems with precision, as done in this case, demonstrates cubic complexity relative to the number of variables and/or constraints. Therefore, future research focused on accelerating differentiable optimization is pivotal for scalability.

Furthermore, exploring policies that excel in low-data regimes based on differentiable optimization layers is an intriguing research direction. By constructing differentiable optimization layers using prior knowledge of the model, policy may reduce reliance on data.

## LeTO in Reinforcement Learning

Due to the differentiability, the DTO layer can be designed to integrate into the robot learning pipelines, enabling end-to-end optimization and inference. This opens up the possibility of extending LeTO to reinforcement learning, offering a promising future research direction. By integrating differentiable trajectory optimization with reinforcement learning, it is possible to ensure that the generated actions comply with the designed constraints, thus significantly improving the safety and interpretability of the policy.

## LeTO in High-safety Scenarios

The safe and constraint-controlled output form of LeTO holds significant potential in robot learning scenarios where safety is of utmost importance, such as in human-robot interaction and surgical robotics. Investigating the application of LeTO, or more broadly, robot policies that integrate differentiable optimization in these settings, represents a highly interesting and promising research direction.

Additionally, since imitation learning provides a high-level controller responsible for decision-making and high-level action generation, LeTO's trajectory optimization capabilities enable it to generate reference motions that are dynamically feasible for a low-level controller. In scenarios requiring high dynamics or heavy loads for manipulation, LeTO may have certain advantages and safety assurances when combined with more specialized lower-level controllers to accomplish these tasks.

## Complex Obstacle Avoidance and Nonconvex Optimization

As stated in our paper, LeTO's constraints must be convex. In complex environments filled with obstacles, these constraints become highly complicated and nonconvex. Therefore, LeTO does not have the ability to generate collision-free actions in confined environments filled with diverse and complex obstacles. We believe that developing an imitation learning algorithm capable of achieving collision-free performance in complex environments while executing dexterous manipulation tasks will be a very promising and important research direction.

# acknowledgements

This work was partially supported by the United States Department of Agriculture (USDA; No. 2023-67021-39072 and 2024-67021-42878) as well as National Science Foundation (NSF; No. 2423068). This article solely reflects the opinions and conclusions of its authors and not USDA or NSF.

::: IEEEbiography
Zhengtong Xu received his Bachelor of Engineering degree in mechanical engineering from Huazhong University of Science and Technology, China in 2020. He is currently pursuing his Ph.D. at Purdue University.

His research focuses on robot learning.
:::

plus -1fil

::: IEEEbiography
Yu She is an assistant professor at Purdue University Edwardson School of Industrial Engineering. Prior to that, he was a postdoctoral researcher in the Computer Science and Artificial Intelligence Laboratory at MIT from 2018 to 2021. He earned his Ph.D. degree in the Department of Mechanical Engineering at the Ohio State University in 2018. His research, at the intersection of mechanical design, sensory perception, and dynamic control, explores human-safe collaborative robots, soft robotics, and robotic manipulation.
:::

[^1]: $^{*}$Address all correspondence to this author.

[^2]: Zhengtong Xu and Yu She are with the Edwardson School of Industrial Engineering, Purdue University, West Lafayette, USA (E-mail: {xu1703, shey}@purdue.edu).

[^3]: https://github.com/ARISE-Initiative/robosuite

[^4]: https://3dconnexion.com/dk/product/spacemouse-compact/
