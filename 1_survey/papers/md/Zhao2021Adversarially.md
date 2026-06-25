---
citation_key: Zhao2021Adversarially
arxiv_id: 2109.07627
arxiv_url: "https://arxiv.org/abs/2109.07627"
title: "Adversarially Regularized Policy Learning Guided by Trajectory Optimization"
authors_short: "Zhigen Zhao et al."
year: 2021
direction_tag: L_learning_path_optimization
source: mineru-vlm
converter: mineru-open-api
model: vlm
converted_at: 2026-06-25T09:43:05Z
origin: ai+web
reviewed: false
---

# Adversarially Regularized Policy Learning Guided by Trajectory Optimization

Zhigen Zhao<sup>\*</sup>, Simiao Zuo<sup>†</sup>, Tuo Zhao<sup>†‡</sup>, Ye Zhao<sup>\*‡</sup> <sup>{</sup>zhigen.zhao, simiaozuo, tourzhao, yzhao301<sup>}</sup>@gatech.edu

## Abstract

Recent advancement in combining trajectory optimization with function approximation (especially neural networks) shows promise in learning complex control policies for diverse tasks in robot systems. Despite their great flexibility, the large neural networks for parameterizing control policies impose significant challenges. The learned neural control policies are often overcomplex and non-smooth, which can easily cause unexpected or diverging robot motions. To address this issue, we propose adversarially regularized policy learning guided by trajectory optimization (VERONICA) for learning smooth control policies. Specifically, our proposed approach controls the smoothness (local Lipschitz continuity) of the neural control policies by stabilizing the output control with respect to the worst-case perturbation to the input state. Our experiments on robot manipulation show that our proposed approach not only improves the sample eficiency of neural policy learning but also enhances the robustness of the policy against various types of disturbances, including sensor noise, environmental uncertainty, and model mismatch.

## 1 Introduction

Robust and generalizable motion planning enables robotic systems to handle various uncertainties and accomplishes diverse tasks. However, learning a dynamically consistent neural control policy (i.e., a neural-network control policy) and executing it reliably remain challenging. First, the function approximators used to model the policy can be highly complex and non-smooth, causing poor generalization performance. Second, the dynamics models involved are often mismatched from the physical robot, leading to the need of learning a robust policy.

Trajectory optimization (TO) [2, 17, 38, 33] is a powerful model-based approach to generate optimal control sequences for complex robotic systems. However, existing methods for solving TO problems with full robot dynamics require solving large nonlinear programs, resulting in high computational cost. This dificulty prevents the use of TO methods in real-time robot control settings. As such, to alleviate the computational burden at run-time, it is preferable to have a parametric representation of a robot control policy. In comparison, model-free policy search, as in [8], aims to automatically learn the controller through random exploration. However, a majority of these methods fail to utilize the prior knowledge on the robot dynamics encoded in the physical model, which causes sample ineficiency.

To take advantage of both TO and policy search, [29] and [20] train a robot control policy supervised by optimized trajectory samples, and meanwhile adapting TO to the learned policy. The work in [29] observes that the derivatives of a neural control policy can behave irregularly even when the policy matches the optimal trajectory baseline. This is because neural networks have high complexity and flexibility, which makes them highly non-smooth — a small change in the networks’ input can cause a large variation in the output. To mitigate this limitation, existing works attempt to impose some smoothness constraints on the policy. For instance, [29] matches the gradient for policy and trajectory samples via tangent propagation. However, tangent propagation requires Jacobian computation on each trajectory point, which does not scale well to large datasets.

To alleviate these issues, we propose a new approach: adversarially regularized policy learning guided by trajectory optimization (VERONICA). Specifically, our approach improves the local Lipschitz continuity of the neural control policy via adversarial regularization, which improves generalization performance for inputs not seen during training. We focus on promoting smoothness in policy for non-hybrid robotics tasks that are often governed by diferential equations with high-order continuity. For hybrid systems where non-smooth dynamics might occur during physical contact, several works in TO [4, 40, 28] and physical simulation MuJoCo [41] propose to model contact with a smoothed model, where contact forces diminish gradually with contact distance. The work of [9] proposes a risk-sensitive cost function to represent a stochastic, smoothed variant of the original complementarity contact problem [5]. In this work, we show that the VERON-ICA framework also provides robustness benefits for a hybrid locomotion system with physical contacts.

The VERONICA framework is related to existing works [27, 46, 12, 43, 15, 37, 15, 51, 23]. These works consider similar regularization techniques, but target at other applications with different motivations, e.g., semi-supervised learning, unsupervised domain adaptation, harnessing adversarial examples, fine-tuning pre-trained models and reinforcement learning. [30] and [32] solve similar min-max problems to improve the robustness of reinforcement learning.

We further observe that besides promoting policy smoothness, adversarial regularization improves the robustness of the policy against modeling errors and perturbations in the environment. We verify that the VERONICA framework produces stable robot behaviors under sensor noise, environmental uncertainty, and model mismatch.

Conventionally, adversarial regularization involves a min-max game, which is solved by alternating gradient descent-ascent. During training, neither of the players can be advantageous, such that the generated perturbations can be over-strong and hinder model generalization. To resolve this issue, we employ Stackelberg adversarial regularization (SAR), as proposed in [50], which formulates adversarial regularization as a Stackelberg game [42]. In SAR, the policy (i.e., the leader) has a higher priority than the perturbation (i.e., the follower). The leader procures its advantage by considering how the follower will respond after observing the leader’s decision, such that the leader anticipates the predicted move of the follower when optimizing its strategy. We note that prioritizing the policy optimization is reasonable and beneficial because we target the performance of the learned policy, instead of the adversary.

Our contributions are: I) We propose VERONICA, an adversarial regularization method for learning smooth neural control policies guided by TO. This improves the generalization performance of the learned policy; II) We show that the learned policy achieves better robustness under disturbances such as sensor noise, environmental uncertainty, and model mismatch; III) We reformulate adversarial regularization as a Stackelberg game, which further improves generalization and robustness of the policy compared with the conventional formulation.

## 2 Related Works

Adversarial Training in Robot Learning: Adversarial training has previously been used to improve safety in robot visuomotor control scenarios [6]. The work in [19] argues that adversarial training induces unexplored error profiles in vision-based robot learning, which studies classification tasks that are not Lipschitz continuous. In contrast, our work focuses on adversarial regularization for neural control policy in dynamics-based robot learning, which are intrinsically smooth. Therefore, vision-based adversarial training studies fundamentally diferent problems than ours.

Imitation Learning: Behavioral cloning (BC) uses supervised learning to directly imitate expert trajectories without interacting with the environment [36]. However, BC is particularly vulnerable to error compounding [35]. In our work, we solve a BC problem for policy learning in each iteration of the Alternating Direction Method of Multipliers (ADMM) method, while the ADMM framework ofers a coupling mechanism to allow the trajectory optimizer (i.e., the teacher) to not only guide the learned policy (i.e., the student) towards better solutions but also adapt to the student. More importantly, we incorporate an adversarial regularizer to improve policy smoothness, which significantly eases the efect of error compounding.

Along another line of research, generative adversarial imitation learning [13, 49] uses generative adversarial networks (GAN) to directly generate policies that imitate expert demonstrations. In contrast, the adversaries in our work are the direct perturbations on the input (i.e., the robot state), rather than the discriminator network.

Trajectory-Optimization-Guided Policy Learning: Trajectory optimization has been used to aid and stabilize value function learning in the reinforcement learning (RL) context [25], while the authors of [18] use a bilevel optimization to learn the value function with adversarial samples. In this work, we focus on supervised learning approaches that train neural control policies from TO.

Guided policy search (GPS) [20, 22, 21] iteratively updates guiding sample using diferential dynamic programming (DDP) and trains policies on the distribution over the guiding samples. In contrast, the work of [29] seeks consensus between neural network policy and trajectory optimization using ADMM [3]. The authors in [10] similarly solve for ADMM consensus, but aim to learn a trajectory sequence rather than policy. The ADMM formulation in our work is closely related to [29], but we focus on adversarial regularization for policy learning.

## 3 Method

We introduce VERONICA, our proposed adversarially regularized approach which combines the strength of policy learning and trajectory optimization. First, we define an adversarial regularizer and explain how it improves smoothness and robustness of neural control policies; Second, we describe an ADMM-based algorithm that solves the full joint optimization problem; Third, we develop an extension to our proposed adversarial regularization approach — Stackelberg adversarial regularization. We consider the neural control policy learning process guided by N optimal trajectories $\{ \mathbf { X } , \mathbf { U } \} = \{ \mathbf { X } _ { i } , \mathbf { U } _ { i } \mid i = 1 , \cdots , N \}$ , and each optimal trajectory $\{ \mathbf { X } _ { i } , \mathbf { U } _ { i } \}$ consists of T state-control pairs $\{ \mathbf { x } _ { i } ^ { t } \in \mathbb { R } ^ { d _ { x } } , \mathbf { u } _ { i } ^ { t } \in \mathbb { R } ^ { d _ { u } } \ | \ t = 1 , \cdots , T \}$ <sup>}</sup>, where $\mathbf { x } _ { i } ^ { t }$ and $\mathbf { u } _ { i } ^ { t }$ denote the robot state and the control, respectively. In this study, the robot state corresponds to the joint positions, velocities and task parameters such as goal configurations, while the control corresponds to the joint torque. Moreover, let $\pi ( \cdot | \mathbf { W } )$ denotes the neural control policy, where W denotes the associated parameters.

## 3.1 Adversarial Regularization for Neural Control Policy

To promote smoothness of the neural control policy, we consider the following adversarial discrepancy measure:

$$
r _ {\mathrm{adv}} (\mathbf {x}, \mathbf {W}) = \max _ {\| \delta \| \leq \epsilon} r (\mathbf {x}, \mathbf {W}, \boldsymbol {\delta}) = \max _ {\| \delta \| \leq \epsilon} \| \pi (\mathbf {x} | \mathbf {W}) - \pi (\mathbf {x} + \boldsymbol {\delta} | \mathbf {W}) \| ^ {2},
$$

where <sup>k</sup> <sup>·</sup> <sup>k</sup> denotes the $\ell _ { 2 }$ norm, $\pmb { \delta } \in \mathbb { R } ^ { d _ { x } }$ is the adversarial perturbation injected to the state vector $\mathbf { x } ,$ and $\epsilon > 0$ is the perturbation strength. Such an adversarial discrepancy measure $r _ { \mathrm { a d v } } ( \mathbf { x } , \mathbf { W } )$ essentially computes the maximal deviation of the neural control policy output at state x given an input perturbation δ whose $\ell _ { 2 }$ norm is bounded by .

We then apply the adversarial discrepancy measure to control the smoothness of the neural control policy. Specifically, we solve the following joint optimization problem:

$$
\begin{array}{l} \min _ {\mathbf {X}, \mathbf {U}, \mathbf {W}} \sum_ {i = 1} ^ {N} \mathcal {L} (\mathbf {X} _ {i}, \mathbf {U} _ {i}) + \mathcal {Q} _ {\mathrm{BC}} (\mathbf {X}, \mathbf {U}, \mathbf {W}) + \alpha \mathcal {R} _ {\mathrm{adv}} (\mathbf {X}, \mathbf {W}), \\ \text {s.t.} \quad \mathbf {x} ^ {t + 1} = f (\mathbf {x} ^ {t}, \mathbf {u} ^ {t}), \mathbf {x} ^ {0} = \mathbf {x} _ {\mathrm{init}}, \mathbf {X} \in \mathcal {X}, \mathbf {U} \in \mathcal {U}, \end{array}\tag{1}
$$

where $\mathcal { L } ( \mathbf { X } _ { i } , \mathbf { U } _ { i } )$ denotes the loss function of the trajectory optimization (TO) for the $i ^ { \mathrm { t h } }$ trajectory,

$\mathcal { Q } _ { \mathrm { B C } } ( \mathbf { X } , \mathbf { U } , \mathbf { W } )$ denotes the loss function for policy learning:

$$
\mathcal {Q} _ {\mathrm{BC}} (\mathbf {X}, \mathbf {U}, \mathbf {W}) = \frac {1}{N} \sum_ {i, t} \| \pi (\mathbf {x} _ {i} ^ {t} | \mathbf {W}) - \mathbf {u} _ {i} ^ {t} \| ^ {2},
$$

$\mathcal { R } _ { \mathrm { a d v } } ( \mathbf { X } , \mathbf { W } )$ is the adversarial regularizer for controlling the smoothness of the policy:

$$
\mathcal {R} _ {\mathrm{adv}} (\mathbf {X}, \mathbf {W}) = \frac {1}{N} \sum_ {i, t} r _ {\mathrm{adv}} (\mathbf {x} _ {i} ^ {t}, \mathbf {W}) = \frac {1}{N} \sum_ {i, t} \max _ {\| \boldsymbol {\delta} _ {i} ^ {t} \| \leq \epsilon} \| \pi (\mathbf {x} _ {i} ^ {t} | \mathbf {W}) - \pi (\mathbf {x} _ {i} ^ {t} + \boldsymbol {\delta} _ {i} ^ {t} | \mathbf {W}) \| ^ {2},
$$

and $\alpha$ is the regularization coeficient weighting between the $\mathcal { Q } _ { \mathrm { B C } } ( \mathbf { X } , \mathbf { U } , \mathbf { W } )$ and $\mathcal { R } _ { \mathrm { a d v } }$

Solving the optimization problem in Eq. (1) learns a neural control policy that not only minimizes the TO loss and the behavior cloning loss, but also encourages the adversarial discrepancy measure of the policy to be small at every state of the optimal trajectories.

(I) Adversarial Regularization Improves Generalization: Existing methods usually train neural control policies by only minimizing the trajectory optimization loss and behavior cloning loss. Due to the high capacity of deep neural networks, the learned neural control policies are often over-complex and highly non-smooth. This is inconsistent with observations that many optimal control policies for robots are smooth. Here we exclude the problem involving physical contact dynamics, which exhibits discontinuous and non-smooth phenomenon. Smoothness requires a small perturbation to the state vector x to only yield a small change to the policy output (Figure 1). Such a property is desirable in robotics tasks, since they often involve diferential equations with high-order continuity properties. Therefore, improving smoothness of the learned policy can improve its ability to generalize to states unseen during training.

VERONICA naturally promotes the desired smoothness by imposing a high penalty when the adversarial perturbation $\pmb { \delta }$ yields a large deviation to the policy output. More precisely, $r _ { \mathrm { a d v } } ( \mathbf { x } , \mathbf { W } )$ essentially upper bounds the deviation of the policy output due to the adversarial perturbation δ with respect to the state $\mathbf { x } ,$ and therefore can be viewed as a measure of the local Lipschitz constant within a small neighborhood of $\mathbf { x } ,$ i.e., $\begin{array} { r } { C _ { \mathbf { x } } = \mathbf { s u p } _ { \| \delta \| \leq \epsilon } \frac { \| \pi ( \mathbf { x } | \mathbf { W } ) - \pi ( \mathbf { x } + \delta | \mathbf { W } ) \| } { \| \delta \| } } \end{array}$ . Accordingly, our proposed adversarial regularizer penalizes the average discrepancy measures of the neural control policy at all trajectory points, which enforces its local Lipschitz continuity.

Remark 1. An alternative regularization technique is the so-called Jacobian regularization (JR), which penalizes the Frobenius norm of the Jacobian matrix of the policy with respect to the input state at all trajectory points $\begin{array} { r } { \mathcal { R } _ { \mathrm { J R } } ( \mathbf { X } , \mathbf { W } ) = \frac { 1 } { N } \sum _ { i , t } \| \nabla _ { \mathbf { x } } \pi ( \mathbf { x } _ { i } ^ { t } | \mathbf { W } ) \| _ { \mathrm { F } } ^ { 2 } } \end{array}$ . As shown in [45], such a Jacobian regularizer is not particularly efective in promoting the Lipschitz continuity of large neural networks. Moreover, when using the Jacobian regularizer for stochastic gradient type algorithms, one needs to further diferentiate through the Jacobian with respect to the parameter W, which is neither computationally eficient nor scalable in practice.

(II) Adversarial Regularization Gains Robustness: Robot systems measure their states from sensors, which are prone to stochastic or systematic sensor errors. VERONICA naturally gains robustness against such disturbances. Specifically, the adversarial perturbation in VERONICA can be viewed as a proxy to the errors. Therefore, our approach does not require prior knowledge of them. In comparison, existing methods for handling such errors usually assume specific forms, $\mathrm { e . g . }$ , independent Gaussian noise, which can be restrictive in practice.

![](Zhao2021Adversarially_figs/e9cb0aeb30d4b7f5a296d3b52adf14edeef3ec9eb99faaa501f251c9fa2bef3c.jpg)  
Figure 1: Illustration of policy smoothness at state x and control u. If the policy π(<sup>·|</sup>W ) is smooth around x, the perturbed state x will produce a control $\mathbf { u } ^ { \prime }$ similar to u. If the policy π(<sup>·|</sup>W) is non-smooth around x, the output control $\mathbf { u } ^ { \prime \prime }$ would deviate significantly from u.

Moreover, as suggested in [1], the Lipschitz continuity is essential to robustness, especially for control and reinforcement learning problems. This is because for policies without the Lipschitz continuity property, a small error in sensor measurement or state transition potentially leads to a drastic change to the policy output. Due to the dynamic nature of the control problem, it will further yield significant error compounding during policy roll-out. Moreover, when the models used to describe robot dynamics mismatch the real robot, such compounding system errors can be catastrophic. Quantitatively, the upper bound for policy robustness under state disturbance, measured by compounding value function discrepancy, is proportional to the Lipschitz constant of the neural control policy (Appendix F). As the VERONICA approach can efectively control the local Lipschitz continuity of the neural control policy, such an issue can be mitigated.

## 3.2 Combined Trajectory Optimization and Adversarially Regularized Policy Learning

We apply ADMM [47, 48] to solve the optimization problem in Eq. (1). Specifically, we reparameterize Eq. (1) into a decomposable form by introducing two auxiliary sets of state and control variables: $( { \bf X } ^ { \mathrm { T O } } , { \bf U } ^ { \mathrm { T O } } )$ represents the trajectory samples generated by trajectory optimization (TO), and $( \mathbf { X } ^ { \mathrm { P L } } , \mathbf { U } ^ { \mathrm { P L } } )$ are copies of $( { \bf X } ^ { \mathrm { T O } } , { \bf U } ^ { \mathrm { T O } } )$ for policy learning. Accordingly, the optimization problem in Eq. (1) is reformulated as:

$$
\begin{array}{r l} \underset {\mathbf {X} ^ {\mathrm{TO,PL}}, \mathbf {U} ^ {\mathrm{TO,PL}}, \mathbf {W}} {\min} & \sum_ {i = 1} ^ {N} \mathcal {L} (\mathbf {X} _ {i} ^ {\mathrm{TO}}, \mathbf {U} _ {i} ^ {\mathrm{TO}}) + \mathcal {Q} _ {\mathrm{BC}} (\mathbf {X} ^ {\mathrm{PL}}, \mathbf {U} ^ {\mathrm{PL}}, \mathbf {W}) + \alpha \mathcal {R} _ {\mathrm{adv}} (\mathbf {X} ^ {\mathrm{PL}}, \mathbf {W}) \\ & \text {s.t.} \mathbf {X} ^ {\mathrm{TO}} = \mathbf {X} ^ {\mathrm{PL}}, \mathbf {U} ^ {\mathrm{TO}} = \mathbf {U} ^ {\mathrm{PL}}. \end{array}\tag{2}
$$

ADMM splits the above optimization problem into N individual TO problems and a policy learning problem to be solved in an iterative manner. Let $\lambda _ { \mathbf { X } _ { i } } ^ { p } , \lambda _ { \mathbf { U } _ { i } } ^ { p }$ denote the dual variables at the $p ^ { \mathrm { t h } }$ iteration and $\rho _ { x } , \rho _ { u } > 0$ denote the penalty parameters. The ADMM primal and policy updates are:

$$
\mathbf {X} _ {i} ^ {\mathrm{TO}, p + 1}, \mathbf {U} _ {i} ^ {\mathrm{TO}, p + 1} = \underset {\mathbf {X} _ {i}, \mathbf {U} _ {i}} {\arg \min} \mathcal {L} (\mathbf {X} _ {i}, \mathbf {U} _ {i}) + \frac {\rho_ {x}}{2} \| \mathbf {X} _ {i} - \mathbf {X} _ {i} ^ {\mathrm{PL}, p} + \boldsymbol {\lambda} _ {\mathbf {X} _ {i}} ^ {p} \| ^ {2}
$$

$$
+ \frac {\rho_ {u}}{2} \| \mathbf {U} _ {i} - \mathbf {U} _ {i} ^ {\mathrm{PL}, p} + \boldsymbol {\lambda} _ {\mathbf {U} _ {i}} ^ {p} \| ^ {2}, \quad (\text { primal   TO   update })\tag{3}
$$

$$
\mathbf {W} ^ {p + 1} = \underset {\mathbf {W}} {\operatorname{argmin}} \mathcal {Q} _ {\mathrm{BC}} (\mathbf {X} ^ {\mathrm{PL}, p}, \mathbf {U} ^ {\mathrm{PL}, p}, \mathbf {W}) + \mathcal {R} _ {\mathrm{adv}} (\mathbf {X} ^ {\mathrm{PL}, p}, \mathbf {W}), \quad (\text {policy update})\tag{4}
$$

$$
\begin{array}{l} \mathbf {X} _ {i} ^ {\mathrm{PL}, p + 1}, \mathbf {U} _ {i} ^ {\mathrm{PL}, p + 1} = \underset {\mathbf {X} _ {i}, \mathbf {U} _ {i}} {\arg \min} \mathcal {Q} _ {\mathrm{BC}} (\mathbf {X} _ {i} ^ {\mathrm{PL}, p}, \mathbf {U} _ {i} ^ {\mathrm{PL}, p}, \mathbf {W} ^ {p + 1}) + \frac {\rho_ {x}}{2} \| \mathbf {X} _ {i} ^ {\mathrm{TO}, p + 1} - \mathbf {X} _ {i} + \boldsymbol {\lambda} _ {\mathbf {X} _ {i}} ^ {p} \| ^ {2} \\ \qquad + \frac {\rho_ {u}}{2} \| \mathbf {U} _ {i} ^ {\mathrm{TO}, p + 1} - \mathbf {U} _ {i} + \boldsymbol {\lambda} _ {\mathbf {U} _ {i}} ^ {p} \| ^ {2}. \quad (\textbf {p r i m a l P L u p d a t e}) \end{array}\tag{5}
$$

Primal TO update: The update in Eq. (3) involves TO and is solved by either direct optimization methods or indirect methods such as diferential dynamic programming (DDP) [38, 14]. We defer details of the DDP algorithm to Appendix A.

Policy update: Note that Eq. (4) is a min-max optimization problem. For notation simplicity, we omit the iteration index $p ,$ and we rewrite it as

$$
\mathbf {W} = \underset {\mathbf {W}} {\arg \min} \mathcal {Q} _ {\mathrm{BC}} (\mathbf {X} ^ {\mathrm{PL}}, \mathbf {U} ^ {\mathrm{PL}}, \mathbf {W}) + \frac {\alpha}{N} \sum_ {i, t} \max _ {\| \boldsymbol {\delta} _ {i} ^ {t} \| \leq \epsilon} r (\mathbf {x} _ {i} ^ {\mathrm{PL}, t}, \mathbf {W}, \boldsymbol {\delta} _ {i} ^ {t}).\tag{6}
$$

To solve Eq. (6), we apply an alternating gradient descent/ascent algorithm. Specifically, at the $s ^ { \mathrm { t h } }$ iteration, we first apply the projected gradient ascent algorithm to update $\delta _ { i } ^ { t }$ for K steps,

$$
\boldsymbol {\delta} _ {i} ^ {t, s} = \boldsymbol {\delta} _ {i} ^ {t, s, K}, \text {where} \boldsymbol {\delta} _ {i} ^ {t, s, k} = \Pi \left[ \boldsymbol {\delta} _ {i} ^ {t, s, k - 1} + \eta_ {\delta} \nabla_ {\delta} r (\mathbf {x} _ {i} ^ {\mathrm{PL}, t}, \mathbf {W} ^ {s}, \boldsymbol {\delta} _ {i} ^ {t, s, k - 1}) \right] \text {for} k = 2, \dots , K.
$$

Here, $\delta _ { i } ^ { t , s , 1 }$ is randomly sampled from ${ \mathcal { N } } ( 0 , \sigma ^ { 2 } \mathbb { I } )$ , Π denotes projection to the $\ell _ { 2 }$ ball with a radius $\epsilon ,$ and $\eta _ { \delta } > 0$ denotes the step size. Then we apply a gradient descent (or stochastic gradient descent) step to W,

$$
\mathbf {W} ^ {s} = \mathbf {W} ^ {s - 1} - \eta_ {W} [ \nabla_ {\mathbf {W}} \mathcal {Q} _ {\mathrm{BC}} (\mathbf {X} ^ {\mathrm{PL}}, \mathbf {U} ^ {\mathrm{PL}}, \mathbf {W} ^ {s}) + \frac {\alpha}{N} \sum_ {i, t} \nabla_ {\mathbf {W}} r (\mathbf {x} _ {i} ^ {\mathrm{PL}, t}, \mathbf {W} ^ {s}, \boldsymbol {\delta} _ {i} ^ {t, s}) ].\tag{7}
$$

Primal PL update: The update in Eq. (5) solves an unconstrained diferentiable optimization subproblem, which can be eficiently solved for each trajectory using stochastic gradient descent.

Dual update: After the above three updates, we perform the dual update as follows:

$$
\boldsymbol {\lambda} _ {\mathbf {X} _ {i}} ^ {p + 1} = \boldsymbol {\lambda} _ {\mathbf {X} _ {i}} ^ {p} + \mathbf {X} _ {i} ^ {\mathrm{TO}, p + 1} - \mathbf {X} _ {i} ^ {\mathrm{PL}, p + 1}, \quad \boldsymbol {\lambda} _ {\mathbf {U} _ {i}} ^ {p + 1} = \boldsymbol {\lambda} _ {\mathbf {U} _ {i}} ^ {p} + \mathbf {U} _ {i} ^ {\mathrm{TO}, p + 1} - \mathbf {U} _ {i} ^ {\mathrm{PL}, p + 1}.\tag{8}
$$

After a certain number of iterations of the above primal-dual policy updates, the joint optimization in Eq. (2) achieves a consensus and the primal and dual residuals meet the ADMM stopping criteria. The overall algorithm is summerized in Algorithm 2 in Appendix B.

## 3.3 Stackelberg Adversarial Regularization

One major limitation of the adversarial regularizer in Eq. (6) is that it solves a min-max-gamebased optimization, where neither of the players can be advantageous. This is problematic because the adversarial player may generate over-strong perturbations that hinder generalization. To mitigate this issue, we employ Stackelberg adversarial regularization [50] to solve the policy update in Eq. (6) through a Stackelberg game formulation. In a Stackelberg game, there are two players, a leader (the policy) and a follower (the perturbations). The leader acknowledges the strategy of the follower, such that it is always in an advantageous position. This efectively eliminates the over-strong perturbations.

```txt
Algorithm 1 Adversarially Regularized Policy Learning.

Input: {X,U}: trajectory samples; E: number of epochs; K: number of perturbation updates.

for epoch = 1,⋯,E do

for {x,u} ∈ {X,U} do

Initialize δ⁰ ∼ N(0,σ²Π)

for k = 1,⋯,K do

Compute dRadv/dδk−1

δk ← Optimizer(dRadv/dδk−1)

end for

Adv Reg:

Compute d(QBC + Radv)/dW

Update W using (7)

Stackelberg Adv Reg:

Compute dQSAR/dW using (10)

W ← Optimizer(dQSAR/dW)

end for

end for
```

To simplify the notation, we omit the indices on the trajectory sample points x. We solve

$$
\begin{array}{l} \min _ {\mathbf {W}} \mathcal {Q} _ {\mathrm{SAR}} (\mathbf {W}) = \mathcal {Q} _ {\mathrm{BC}} (\mathbf {X}, \mathbf {U}, \mathbf {W}) + \frac {\alpha}{N} \sum r (\mathbf {x}, \mathbf {W}, \boldsymbol {\delta} ^ {K}), \\ \text {s.t.} \boldsymbol {\delta} ^ {K} (\mathbf {W}) = U ^ {K} \circ U ^ {K - 1} \circ \dots \circ U ^ {1} (\boldsymbol {\delta} ^ {0}). \end{array}\tag{9}
$$

The policy parameter W in $\operatorname { E q . } \left( 9 \right)$ is the leader, and the perturbation $\delta ( \mathbf { W } )$ is the follower. Here, <sup>◦</sup> denotes operator composition, i.e., $f ( \cdot ) \circ g ( \cdot ) = f ( g ( \cdot ) )$ . Each $U ^ { k }$ for $k = 1 , \cdots , K$ represents the $k ^ { \mathrm { t h } }$ step update operator for the follower’s strategy. The operators are defined by pre-selected optimization algorithms such as stochastic gradient descent (SGD) or Adam [16].

In Stackelberg adversarial training, the leader acknowledges the strategy of the follower by treating the perturbations (the follower) as a function of the policy parameters (the leader). Correspondingly, we solve for the policy parameters using gradient descent, where the Stackelberg gradient is

$$
\frac {\mathrm{d} \mathcal {Q} _ {\mathrm{SAR}} (\mathbf {W})}{\mathrm{d} \mathbf {W}} = \underbrace {\frac {\mathrm{d} \mathcal {Q} _ {\mathrm{BC}} (\mathbf {X} , \mathbf {U} , \mathbf {W})}{\mathrm{d} \mathbf {W}} + \alpha \frac {\partial r (\mathbf {x} , \mathbf {W} , \boldsymbol {\delta} ^ {K})}{\partial \mathbf {W}}} _ {\text { leader }} + \underbrace {\alpha \frac {\partial r (\mathbf {x} , \mathbf {W} , \boldsymbol {\delta} ^ {K})}{\partial \boldsymbol {\delta} ^ {K}} \frac {\mathrm{d} \boldsymbol {\delta} ^ {K}}{\mathrm{d} \mathbf {W}}} _ {\text { leader - follower   interaction }}.\tag{10}
$$

In comparison, the conventional adversarial regularization in Eq. (6) uses only the leader term and does not consider the leader-follower interaction.

The most expensive term to compute in Eq. (10) is $\mathrm { d } \delta ^ { \mathrm { K } } / \mathrm { d } { \bf W }$ . Recall that we have $\delta ^ { k } = U ^ { k } ( \delta ^ { k - 1 } )$ where $U ^ { k }$ is an update operator, e.g., a one-step gradient ascent. As a short-hand, we write

$$
\boldsymbol {\delta} ^ {k} (\mathbf {W}) = \boldsymbol {\delta} ^ {k - 1} (\mathbf {W}) + \Delta (\mathbf {x}, \boldsymbol {\delta} ^ {k - 1} (\mathbf {W}), \mathbf {W}),
$$

where $\Delta ( \mathbf { x } , \delta ^ { k - 1 } ( \mathbf { W } ) , \mathbf { W } )$ signifies the update from $\delta ^ { k - 1 }$ to $\delta ^ { k }$ . Then we have

$$
\frac {\mathrm{d} \boldsymbol {\delta} ^ {k}}{\mathrm{d} \mathbf {W}} = \frac {\mathrm{d} \boldsymbol {\delta} ^ {k - 1}}{\mathrm{d} \mathbf {W}} + \frac {\partial \Delta (\mathbf {x} , \boldsymbol {\delta} ^ {k - 1} , \mathbf {W})}{\partial \mathbf {W}} + \frac {\partial \Delta (\mathbf {x} , \boldsymbol {\delta} ^ {k - 1} , \mathbf {W})}{\partial \boldsymbol {\delta} ^ {k - 1}} \frac {\mathrm{d} \boldsymbol {\delta} ^ {k - 1}}{\mathrm{d} \mathbf {W}}.
$$

This recursive diferentiation can be eficiently computed using deep learning libraries, such as PyTorch [31]. Please refer to [50] for more details. The overall adversarial regularization algorithm is shown in Algorithm 1.

## 4 Experiments

We evaluate VERONICA on cart-pole swing-up and Kuka arm manipulation tasks. The manipulation scenarios are shown in Figure 2. The experiments are shown in the video<sup>1</sup>. We compare smoothness, generalization, and robustness of policies trained with Gaussian perturbations, conventional adversarial regularization (VERONICA-AR), and SAR (VERONICA-SAR). We do not include tangent propagation due to the excessive computational requirements to compute the Jacobian. We also demonstrate that the neural control policy is able to handle simple multi-modal dynamics for the pick and place task.

For Kuka manipulation tasks, the simulation environment is implemented in PyBullet [7]. We solve for TO described in Eq. (3) using DDP implemented in Crocoddyl [26]. For hopper locomotion tasks, we implement both the simulation environment and a direct TO algorithm in Drake [39]. The adversarially regularized policy learning algorithm is implemented in Py-Torch [31] and Higher [11]. The implementation details can be found in Appendix C.

Policy Smoothness: We qualitatively examine the smoothness of our neural control policy by inspecting a typical policy roll-out for cart-pole swing-up and Kuka arm reaching tasks, as shown in Figure 3. Figure 3(a) shows the smoothness comparison during a cart-pole swing-up. VERON-ICA produced visually smoother force sequences comparing to Gaussian perturbation. Figure 3(b)

![](Zhao2021Adversarially_figs/ea43a1d5e10e012382589d244ccb7e9a8290942e3fef12192825db33e2e0cfc5.jpg)  
Figure 2: The Kuka arm manipulation scenarios in simulation. (a) Kuka IIWA arm reaching: the learned policy controls the arm to reach a predefined joint configuration. In 3-DOF reaching experiments, only joints 2, 4, and 6 are active degrees-of-freedom (DOFs), making the arm equivalent to a planar manipulator. In 5-DOF experiments, joints 1, 2, $4 , 5 ,$ and 6 are active DOFs; (b) The Kuka arm pick and place task: an additional object is grasped by the Kuka arm during this task.

displays the torque sequence of Kuka joint 2 during a reaching task. The policy trained by Gaussian perturbation generates a non-smooth torque profile around the initial position of the task, indicating that the Gaussian perturbation is not suficient to prevent overfitting at the initial phase of the trajectory, where the torque changes relatively quickly with respect to state. In comparison, the VERONICA-AR and VERONICA-SAR policies produce smoother control sequences that track the baseline closely. To inspect the smoothness of the neural control policies, we plot the torque output on Kuka joint 2 against the joint angle in Figure 3(c). VERONICA successfully penalize against the non-smooth peak that appeared in the torque profile of the Gaussian perturbed policy.

![](Zhao2021Adversarially_figs/ddf96d4aebd2b5348d25f10b17118a80b1b7ca602fc367c47bca401babbfefc4.jpg)

(b)  
![](Zhao2021Adversarially_figs/c52321c998374ffa126a907432652cee75b59d431e90613ec0d12a9df508e7a8.jpg)

(c)  
![](Zhao2021Adversarially_figs/cf2cc747229cc70dce99a8e50089e64b1ae9917a60e05a71585fc7848286dd81.jpg)  
Figure 3: Comparison of control output smoothness for cart-pole and Kuka arm reaching tasks. Trajectory optimization baseline is marked as a dashed line. (a) Time sequence of forces applied onto the cart during swing-up. (b-c) Torque output for Kuka joint 2 with respect to time and joint 2 angle.

Generalization Performance: To evaluate the generalization performances of VERONICA, we perform policy roll-outs with 100 diferent initializations in an undisturbed environment, as seen in Figure 4(a). The adversarially regularized policies produce lower costs because the policies trained with no perturbation or Gaussian perturbation are unable to generate stable robot motions under some initializations. Figure 5 displays an example of an arm reaching task that Gaussian perturbation cannot handle. Although a vast majority of roll-outs with the VERONICA-AR policy are stable, a small percentage (2%) produces unstable robot motions that fail to achieve the task. In comparison, the VERONICA-SAR policy leads to stable and near-optimal robot motions across all attempts, confirming our hypothesis that VERONICA-SAR helps enhance numerical stability comparing to VERONICA-AR.

![](Zhao2021Adversarially_figs/61e1319bb1dfb40b777c1487050ea33539196147f7a228bbfe7b342f62e0cf3e.jpg)

(b)  
![](Zhao2021Adversarially_figs/6a05a09cbdca2e1e743be0f9db735866df4008fa3d892ab3c9761b75d3b94794.jpg)  
(c)

![](Zhao2021Adversarially_figs/d00bac0119226c790d8bfd7fdda52ad216e32556e7ada62ba83e543fe2f88ef5.jpg)  
Figure 4: Cost percentile plot for 3-DOF arm reaching task with 100 diferent initializations and under diferent disturbances on sensor measurement. Disturbances are drawn from a uniform distribution bounded by ζ. Policies trained with no perturbation, Gaussian perturbation, VERONICA-AR, and VERONICA-SAR are compared against an undisturbed TO baseline. The plot is capped at 2 times the maximum baseline cost. A cost curve that exceeds the plotting cap indicates that a percentage of policy roll-outs lead to unstable robot motion.

(a)  
![](Zhao2021Adversarially_figs/e7c8aedd23551c3f5fe68f82b695c76cffef0ecae0fbf01036b98e93d02032a9.jpg)

(b)  
![](Zhao2021Adversarially_figs/172005023bc5fce3244ccd63861a0f1feee8030f71f1574b62dd318df99ddecd.jpg)

![](Zhao2021Adversarially_figs/63f7aebfef38d2c44dc44db58f4db29166d7d995cdc8a33ba209cdbe9682a10c.jpg)  
Figure 5: Example of an undisturbed policy roll-out for a 3-DOF manipulator reaching task where Gaussian perturbation fails. The undisturbed TO result is provided as a baseline. (a) Cumulative cost for policy roll-out (b-c) Torque outputs on joints 2 and 4.

Policy Robustness: We evaluate our policies’ robustness against three diferent kinds of disturbances. For sensor noise and environmental uncertainty, we add a uniform noise bounded by an $\ell _ { \infty } { - } \mathrm { n o r m }$ ball with radius ζ onto the sensor measurement and state transition, respectively. As for model mismatch, we modify the URDF file used in policy roll-out by decreasing the mass of each robot link by 0.25 kg.

We first compare the policies’ robustness against diferent magnitudes of sensor noise, as shown in Figure 4(b-c). While Gaussian perturbation does provide some robustness comparing to the unregularized policy, VERONICA-AR and VERONICA-SAR consistently outperforms the Gaussian perturbation. Furthermore, VERONICA-AR deviates significantly from the undisturbed TO baseline under a strong sensor noise $( \zeta = 0 . 0 5 )$ , while VERONICA-SAR remains able to produce stable robot motion and closely track the TO baseline.

Table 1 shows the average task errors - the distance between the goal and the actual final positions for the robot arm’s end-efector - and their standard deviation for 100 manipulator reaching tasks under diferent types of disturbances. VERONICA provides significantly lower task errors across all clean and disturbed experiments. Furthermore, VERONICA-SAR leads to a lower standard deviation than VERONICA-AR, indicating that the policy learned by VERONICA-SAR is less prone to outliers comparing to VERONICA-AR.

Table 1: Task Error for 3-DOF Manipulator Reaching Task $( \zeta = 0 . 0 1$ , Unit: m)

<table><tr><td></td><td>Gaussian</td><td>VERONICA-AR</td><td>VERONICA-SAR</td></tr><tr><td>Undisturbed</td><td> $1.62e-1 \pm 5.05e-2$ </td><td> $6.26e-2 \pm 3.96e-2$ </td><td> $6.39e-2 \pm 2.70e-2$ </td></tr><tr><td>Sensor Error</td><td> $1.75e-1 \pm 7.85e-2$ </td><td> $7.11e-2 \pm 7.57e-2$ </td><td> $6.61e-2 \pm 2.42e-2$ </td></tr><tr><td>Environment Uncertainty</td><td> $1.73e-1 \pm 7.59e-2$ </td><td> $8.66e-2 \pm 1.03e-1$ </td><td> $7.75e-2 \pm 3.99e-2$ </td></tr><tr><td>Model Mismatch</td><td> $2.14e-1 \pm 8.26e-2$ </td><td> $5.24e-2 \pm 3.27e-2$ </td><td> $1.23e-1 \pm 2.16e-2$ </td></tr></table>

Table 2: Median Task Errors for M-DOF Manipulator (Unit: m)

<table><tr><td>M=3</td><td>M=5</td><td>M=7</td></tr><tr><td>6.39e-2</td><td>1.23e-1</td><td>1.32e-1</td></tr></table>

Extension to Higher-DOF Manipulators: We investigate how the performance of VERONICA-SAR scales to higher state and control dimensions by evaluating the task errors of manipulator reaching tasks for 3, 5, and 7-DOF Kuka arms (Table 2). The task error increases with the dimen sionality of the problem, but not significantly. Note that the 5 and 7-DOF experiments involve manipulation in the 3-D space, which lead to much higher problem complexity than the planar 3-DOF Kuka arm configuration, and require larger neural control policies. Figure 6 indicates that similar to the 3-DOF cases, the proposed Stackelberg adversarial regularization benefits both generalization and robustness performance compared to Gaussian regularization in the 7-DOF Kuka arm reaching tasks.

![](Zhao2021Adversarially_figs/129f97166ae0c2d307af2b1bc50e0864ec9cf1d8b223a100f21e137f5a912e66.jpg)

![](Zhao2021Adversarially_figs/85eabb7eabcb7b9a042eff762c462a3ed190a7584a3c4f8468b7b9378b4b028d.jpg)

![](Zhao2021Adversarially_figs/50a03805dec590770dd8737a548107550d85d10d277cf48960bfa31a923e9649.jpg)  
Figure 6: Cost percentile plot for 7-DOF arm reaching task with 100 diferent initializations and under diferent disturbances on sensor measurements. The plot is capped at 3 times the maximum baseline cost.

Preliminary Study of Learning Multimodal Dynamics: In the pick and place task, we train a network policy to handle the control of the Kuka arm for both free-moving or object-holding scenarios. In order to train the policy applicable for both cases simultaneously, we include a discrete variable in the network input to signify the grasping state of the object. Figure 7 shows the arm’s torque output for the same initialization, with or without an object. For simplicity, this experiment assumes that only one object with a known mass, and the object is fixed to a pre-specified position in the gripper when grasped by the arm. In the future, the adaptability of the network policy can be improved by augmenting the input with more information such as the weight of the object and the relative position between the object and the gripper.

![](Zhao2021Adversarially_figs/e1a0baeb37a5a9deb6e84eb17264de1cb01f40ea385344430c4098fe08f661c6.jpg)  
Figure 7: Comparison for the control policy outputs with or without grasping a 5kg object.

![](Zhao2021Adversarially_figs/2930c6fee47974d49b03480b0e1f86155d9b9439aa02000c72a978a982e1edd7.jpg)  
Figure 8: Cost percentile plot for hopper locomotion task with 100 diferent initializations.

Application to Hybrid Locomotion Systems: We apply VERONICA in hopper locomotion tasks to evaluate the performance of VERONICA in a single leg 5-DOF hopper system, where the hybrid locomotion trajectories involve intermittent contacts with the terrain. We compare the cost percentile plot between the TO baseline and VERONICA-SAR, as displayed in Figure 8. Note that the open-loop rollout of trajectories generated by TO baseline performs poorly in simulation due to the model mismatch between TO and simulation environments. In contrast, the policy trained with VERONICA-SAR generates a lower cost hopper motions due to the robustness against model mismatch provided by adversarial perturbation. A visual comparison can be found in the video.

## 5 Conclusion

We present VERONICA, an adversarial regularization framework for combined trajectory optimization and policy learning. We show that the proposed regularizer improves generalization and robustness by enforcing Lipschitz continuity of the policy. Additionally, we propose to further stabilize training by formulating the adversarial regularization as a Stackelberg game. The experiment results in robot manipulation scenarios show that our approach helps to improve the smoothness of the learned policy, which results in a more stable robot motions and lower policy execution costs. Additionally, we demonstrate that policies trained with VERONICA are able to robustly handle various types of disturbances. Our future work will include various extensions to the proposed framework. For example, we will extend VERONICA to solve more complex manipulation problems involving physical contact and enhance robustness to contact uncertainties. We will employ our method in conjunction with a smoothed contact solver similar to the one in [28] to circumvent the discontinuity due to contact phenomena while leveraging the smoothness merit induced by the adversarial regularization. Additionally, adaptive adversarial training, where perturbations are generated by an additional network, can be incorporated to generate variable perturbation radius around contact points.

Our future work will (i) evaluate the performance of VERONICA in the presence of more types of perturbations and uncertainties, such as varying link moment of inertia and kinematic parameters; (ii) extend VERONICA to solve more complex manipulation and locomotion problems involving physical contact and enhance robustness to contact uncertainties. Adaptive adversarial training, where perturbations are generated by an additional network, can be incorporated to generate variable perturbation radius around contact points.

## References

[1] Kavosh Asadi, Dipendra Misra, and Michael Littman. “Lipschitz continuity in model-based reinforcement learning”. In: International Conference on Machine Learning. PMLR. 2018, pp. 264–273.

[2] John T Betts. “Survey of numerical methods for trajectory optimization”. In: Journal of guidance, control, and dynamics 21.2 (1998), pp. 193–207.

[3] Stephen Boyd, Neal Parikh, and Eric Chu. Distributed optimization and statistical learning via the alternating direction method of multipliers. Now Publishers Inc, 2011.

[4] Marcus A Brubaker, Leonid Sigal, and David J Fleet. “Estimating contact dynamics”. In: 2009 IEEE 12th International Conference on Computer Vision. IEEE. 2009, pp. 2389–2396.

[5] Chunhui Chen and Olvi L Mangasarian. “A class of smoothing functions for nonlinear and mixed complementarity problems”. In: Computational Optimization and Applications 5.2 (1996), pp. 97–138.

[6] Xi Chen et al. “Adversarial feature training for generalizable robotic visuomotor control”. In: 2020 IEEE International Conference on Robotics and Automation (ICRA). IEEE. 2020, pp. 1142– 1148.

[7] Erwin Coumans and Yunfei Bai. PyBullet, a Python module for physics simulation for games, robotics and machine learning. http://pybullet.org. 2016–2021.

[8] Marc Peter Deisenroth, Gerhard Neumann, Jan Peters, et al. “A survey on policy search for robotics”. In: Foundations and trends in Robotics 2.1-2 (2013), pp. 388–403.

[9] Luke Drnach and Ye Zhao. “Robust trajectory optimization over uncertain terrain with stochastic complementarity”. In: IEEE Robotics and Automation Letters 6.2 (2021), pp. 1168– 1175.

[10] Alexis Duburcq et al. “Online trajectory planning through combined trajectory optimization and function approximation: Application to the exoskeleton Atalante”. In: IEEE International Conference on Robotics and Automation. 2020.

[11] Edward Grefenstette et al. “Generalized Inner Loop Meta-Learning”. In: arXiv preprint arXiv:1910.01727 (2019).

[12] Dan Hendrycks et al. “Using Self-Supervised Learning Can Improve Model Robustness and Uncertainty”. In: arXiv preprint arXiv:1906.12340 (2019).

[13] Jonathan Ho and Stefano Ermon. “Generative adversarial imitation learning”. In: Proceedings of the 30th International Conference on Neural Information Processing Systems. 2016, pp. 4572–4580.

[14] David H Jacobson and David Q Mayne. “Diferential dynamic programming”. In: (1970).

[15] Haoming Jiang et al. “SMART: Robust and Eficient Fine-Tuning for Pre-trained Natural Language Models through Principled Regularized Optimization”. In: arXiv preprint arXiv:1911.03437 (2019).

[16] Diederik P Kingma and Jimmy Ba. “Adam: A method for stochastic optimization”. In: arXiv preprint arXiv:1412.6980 (2014).

[17] Scott Kuindersma et al. “Optimization-based locomotion planning, estimation, and control design for the atlas humanoid robot”. In: Autonomous robots 40.3 (2016), pp. 429–455.

[18] Benoit Landry, Hongkai Dai, and Marco Pavone. “SEAGuL: Sample Eficient Adversarially Guided Learning of Value Functions”. In: Learning for Dynamics and Control. PMLR. 2021, pp. 1–13.

[19] Mathias Lechner et al. “Adversarial Training is Not Ready for Robot Learning”. In: arXiv preprint arXiv:2103.08187 (2021).

[20] Sergey Levine and Vladlen Koltun. “Guided policy search”. In: International conference on machine learning. PMLR. 2013, pp. 1–9.

[21] Sergey Levine and Vladlen Koltun. “Learning complex neural network policies with trajectory optimization”. In: International Conference on Machine Learning. PMLR. 2014, pp. 829– 837.

[22] Sergey Levine and Vladlen Koltun. “Variational policy search via trajectory optimization”. In: Advances in neural information processing systems 26 (2013), pp. 207–215.

[23] Yan Li et al. “Implicit bias of gradient descent based adversarial training on separable data”. In: (2020).

[24] Ilya Loshchilov and Frank Hutter. “Decoupled weight decay regularization”. In: arXiv preprint arXiv:1711.05101 (2017).

[25] Kendall Lowrey et al. “Plan online, learn ofline: Eficient learning and exploration via model-based control”. In: arXiv preprint arXiv:1811.01848 (2018).

[26] Carlos Mastalli et al. “Crocoddyl: An Eficient and Versatile Framework for Multi-Contact Optimal Control”. In: IEEE International Conference on Robotics and Automation (ICRA). 2020.

[27] Takeru Miyato et al. “Virtual adversarial training: a regularization method for supervised and semi-supervised learning”. In: IEEE transactions on pattern analysis and machine intelligence 41.8 (2018), pp. 1979–1993.

[28] Igor Mordatch, Emanuel Todorov, and Zoran Popovic. “Discovery of complex behaviors´ through contact-invariant optimization”. In: ACM Transactions on Graphics (TOG) 31.4 (2012), pp. 1–8.

[29] Igor Mordatch and Emo Todorov. “Combining the benefits of function approximation and trajectory optimization.” In: Robotics: Science and Systems. Vol. 4. 2014.

[30] Jun Morimoto and Kenji Doya. “Robust reinforcement learning”. In: NIPS. Citeseer. 2000, pp. 1061–1067.

[31] Adam Paszke et al. “PyTorch: An Imperative Style, High-Performance Deep Learning Library”. In: Advances in Neural Information Processing Systems 32. Ed. by H. Wallach et al. Curran Associates, Inc., 2019, pp. 8024–8035. <sup>url</sup>: http://papers.neurips.cc/paper/9015- pytorch-an-imperative-style-high-performance-deep-learning-library.pdf.

[32] Lerrel Pinto et al. “Robust adversarial reinforcement learning”. In: Proceedings of the 34th International Conference on Machine Learning-Volume 70. JMLR. org. 2017, pp. 2817–2826.

[33] Michael Posa, Cecilia Cantu, and Russ Tedrake. “A direct method for trajectory optimiza tion of rigid bodies through contact”. In: The International Journal of Robotics Research 33.1 (2014), pp. 69–81.

[34] Antonin Rafin et al. Stable Baselines3. https://github.com/DLR-RM/stable-baselines3. 2019.

[35] Stephane Ross, Geo ´ frey Gordon, and Drew Bagnell. “A reduction of imitation learning and structured prediction to no-regret online learning”. In: Proceedings of the fourteenth international conference on artificial intelligence and statistics. JMLR Workshop and Conference Proceedings. 2011, pp. 627–635.

[36] Stefan Schaal et al. “Learning from demonstration”. In: Advances in neural information processing systems (1997), pp. 1040–1046.

[37] Qianli Shen et al. “Deep Reinforcement Learning with Robust and Smooth Policy”. In: International Conference on Machine Learning. PMLR. 2020, pp. 8707–8718.

[38] Yuval Tassa, Nicolas Mansard, and Emo Todorov. “Control-limited diferential dynamic programming”. In: 2014 IEEE International Conference on Robotics and Automation (ICRA). IEEE. 2014, pp. 1168–1175.

[39] Russ Tedrake and the Drake Development Team. Drake: Model-based design and verification for robotics. 2019. <sup>url</sup>: https://drake.mit.edu.

[40] Emanuel Todorov. “A convex, smooth and invertible contact model for trajectory optimization”. In: 2011 IEEE International Conference on Robotics and Automation. IEEE. 2011, pp. 1071–1076.

[41] Emanuel Todorov, Tom Erez, and Yuval Tassa. “Mujoco: A physics engine for model-based control”. In: 2012 IEEE/RSJ International Conference on Intelligent Robots and Systems. IEEE. 2012, pp. 5026–5033.

[42] Heinrich Von Stackelberg. Market structure and equilibrium. Springer Science & Business Media, 2010.

[43] Qizhe Xie et al. “Unsupervised data augmentation”. In: arXiv preprint arXiv:1904.12848 (2019).

[44] Tian Xu, Ziniu Li, and Yang Yu. “On Value Discrepancy of Imitation Learning”. In: arXiv preprint arXiv:1911.07027 (2019).

[45] Yao-Yuan Yang et al. “Adversarial robustness through local lipschitzness”. In: arXiv preprint arXiv:2003.02460 (2020).

[46] Hongyang Zhang et al. “Theoretically principled trade-of between robustness and accuracy”. In: arXiv preprint arXiv:1901.08573 (2019).

[47] Zhigen Zhao et al. “SyDeBO: Symbolic-Decision-Embedded Bilevel Optimization for Long-Horizon Manipulation in Dynamic Environments”. In: arXiv preprint arXiv:2010.11078 (2020).

[48] Ziyi Zhou and Ye Zhao. “Accelerated ADMM based Trajectory Optimization for Legged Locomotion with Coupled Rigid Body Dynamics”. In: American Control Conference. 2020, pp. 5082–5089.

[49] Konrad Zolna et al. “Task-relevant adversarial imitation learning”. In: arXiv preprint arXiv:1910.01077 (2019).

[50] Simiao Zuo et al. “Adversarial Training as Stackelberg Game: An Unrolled Optimization Approach”. In: arXiv preprint arXiv:2104.04886 (2021).

[51] Simiao Zuo et al. “ARCH: Eficient Adversarial Regularized Training with Caching”. In: arXiv preprint arXiv:2109.07048 (2021).

## Supplemental Materials

## A Diferential Dynamic Programming

In order to generate each individual trajectory sample satisfying robot rigid body dynamics, we solve the following trajectory optimization (TO) problem formulated as:

$$
\min _ {\mathbf {X}, \mathbf {U}} \quad \mathcal {L} (\mathbf {X}, \mathbf {U}) = \sum_ {t = 1} ^ {T - 1} \ell (\mathbf {x} ^ {t}, \mathbf {u} ^ {t}) + \ell_ {f} (\mathbf {x} ^ {T}, \mathbf {u} ^ {T})\tag{11a}
$$

$$
\mathrm{s.t.} \quad \mathbf {x} ^ {t + 1} = f (\mathbf {x} ^ {t}, \mathbf {u} ^ {t}), \mathbf {x} ^ {0} = \mathbf {x} _ {\mathrm{init}},\tag{11b}
$$

$$
\mathbf {X} \in \mathcal {X}, \mathbf {U} \in \mathcal {U},\tag{11c}
$$

where $\ell ( \mathbf { x } ^ { t } , \mathbf { u } ^ { t } )$ is the cost function at time-step $t , \ell _ { f } ( \mathbf { x } ^ { T } , \mathbf { u } ^ { T } )$ represents the terminal trajectory cost at time-step $T , \mathbf { x } ^ { t + 1 } = f ( \mathbf { x } ^ { t } , \mathbf { u } ^ { t } )$ is the discretized system dynamics, and $x , u$ represents additional path constraints on state and control. The running trajectory cost $\ell ( \mathbf { x } , \mathbf { u } )$ is composed of the a goal tracking term, a control regularization term, and the ADMM residual terms:

$$
\ell (\mathbf {x}, \mathbf {u}) = \widehat {\mathbf {x}} ^ {\top} \mathbf {Q} \widehat {\mathbf {x}} + \mathbf {u} ^ {\top} \mathbf {R u} + \frac {\rho_ {x}}{2} \| \mathbf {x} - \mathbf {x} ^ {\mathrm{PL}} + \boldsymbol {\lambda} _ {\mathbf {x}} \| ^ {2} + \frac {\rho_ {u}}{2} \| \mathbf {u} - \mathbf {u} ^ {\mathrm{PL}} + \boldsymbol {\lambda} _ {\mathbf {u}} \| ^ {2},
$$

where $\widehat { \mathbf { x } } = \mathbf { x } - \mathbf { x } _ { \mathrm { g o a l } }$ represents the deviation between the trajectory state x and goal state $\mathbf { x } _ { \mathrm { g o a l } }$ and $\mathbf { Q } , \mathbf { R } \succeq 0$ are the weighting matrices for the strength of the regularization. The ADMM residual terms $\frac { \rho _ { x } } { 2 } \| \mathbf { x } - \mathbf { x } ^ { \mathrm { P L } } + \lambda _ { \mathbf { x } } \| ^ { 2 }$ and $\frac { \rho _ { u } } { 2 } \| \mathbf { u } - \mathbf { u } ^ { \mathrm { P L } } + \lambda _ { \mathbf { u } } \| ^ { 2 }$ are initialized to be 0 at the first iteration, but eventually have the efect of regularizing the trajectory optimization to be closer to the policy output.

In the following we briefly describe the formulation of DDP, which is used in this work to compute trajectory samples. [14] provides a detailed representation of DDP in the historical context, and [38] presents a control-constrained version of DDP that is widely used in robotics.

DDP solves the optimization described in Eq. (11) using a backward pass of Bellman’s equation,

$$
V (\mathbf {x} ^ {t}) = \min _ {\mathbf {u}} [ \ell (\mathbf {x} ^ {t}, \mathbf {u} ^ {t}) + V (\mathbf {x} ^ {t + 1}) ].\tag{12}
$$

Let $Q ( \delta \mathbf { x } ^ { t } , \delta \mathbf { u } ^ { t } )$ be the change in local cost function given a perturbation around the tth time-step:

$$
Q (\delta \mathbf {x}, \delta \mathbf {u}) = \ell (\mathbf {x} + \delta \mathbf {x}, \mathbf {u} + \delta \mathbf {u}) - \ell (\mathbf {x}, \mathbf {u}) + V (\mathbf {x} + \delta \mathbf {x}) - V (\mathbf {x})\tag{13}
$$

The DDP backward pass computes the second order Taylor expansion of Q and the optimal local perturbation $\delta \mathbf { u } ^ { * }$ is given by the local feedback control policy:

$$
\delta \mathbf {u} ^ {*} = \mathbf {k} + \mathbf {K} \delta \mathbf {x},\tag{14}
$$

where ${ \mathbf k } = - Q _ { u u } ^ { - 1 } Q _ { u }$ and ${ \bf K } = - Q _ { u u } ^ { - 1 } Q _ { u x }$ . After the backward pass is completed, the DDP forward pass simulates the system by rolling out the system dynamics $\mathbf { x } ^ { t + 1 } = f ( \mathbf { x } ^ { t } , \mathbf { u } ^ { t } )$ . The backwardforward passes are iterated until convergence.

# B Algorithm Overview of the Proposed Trajectory Optimization Guided by Adversarially Regularized Policy Learning

Algorithm 2 shows the complete procedure of jointly solving TO and policy learning using ADMM.

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 2 TO-Guided Policy Learning Using ADMM
Input: P: total number of ADMM iterations; N: number of sample trajectories.
 $X_{init} \leftarrow N$ trajectory initial conditions
 $\lambda_{X}^{0}, \lambda_{U}^{0} \leftarrow 0$ 
for  $p = 1, \cdots, P$ do
 $X^{TO,p}, U^{TO,p} \leftarrow$ compute N trajectories using Eq. (3) (primal TO update)
 $W^{p} \leftarrow$ solve min-max optimization in Eq. (4) using Algorithm 1 (policy update)
 $X^{PL,p}, U^{PL,p} \leftarrow$ optimize using Eq. (5) (primal PL update)
 $\lambda_{X}^{p}, \lambda_{U}^{p} \leftarrow$ update using Eq. (8) (dual update)
end for
return  $W^{P}$
</div>

## C Implementation Details

We use a fully connected neural network with 2 hidden layers and 8 units per layer for the cartpole example. The 3-DOF Kuka arm uses 2 hidden layers and 64 units each, the 5-DOF manipulator uses 3 hidden layers and 64 units each, while the 7-DOF manipulator uses a residual network with 3 hidden layers and 256 units. The hopper example, as shown in Figure 9, uses a fully connected network with 3 hidden layers and 24 units each.

In all experiments, we train the networks using AdamW [24] for policy optimization and stochastic gradient descent (SGD) for adversarial perturbation. The regularization coeficient α is set to 1. The learning rate for the policy learning $\mathbf { l r } _ { p }$ is chosen between <sup>{</sup>1e-3, 5e-4<sup>}</sup>, and the learning rate for adversarial perturbation $\mathrm { l r } _ { \mathrm { a d v } }$ is chosen between <sup>{</sup>5e-4, 1e-4<sup>}</sup>. The number of adversarial update steps K is selected from <sup>{</sup>1, 3<sup>}</sup>, and the adversarial bound  is chosen from <sup>{</sup>1e-2, 5e-3<sup>}</sup>. The policy is trained for at most 300 epochs, with model averaging in the last $1 / 4$ of total epochs. Also, we apply gradient norm clipping of <sup>{∞</sup>, 1<sup>}</sup>.

In ADMM, we apply a trajectory state penalty coeficient $\rho _ { x }$ of <sup>{</sup>1, 10, 50<sup>}</sup> and a trajectory control penalty coeficient $\rho _ { u }$ of 1. We find that the behavioral cloning loss $\mathcal { Q } _ { \mathrm { B C } }$ decreases over ADMM iterations, but the loss deduction is not significant after 5-10 iterations. Therefore, the ADMM is run until $\mathcal { Q } _ { \mathrm { B C } }$ stops decreasing, which results in between 5-15 iterations in our experiments. The result for $\mathcal { Q } _ { \mathrm { B C } }$ plotted with respect to ADMM iterations can be found in Appendix D.

![](Zhao2021Adversarially_figs/6f0484b9b487c7a939a10cd026d71bccb4a17007fc07d211849ccdaea7d4bcb5.jpg)  
Figure 9: The hopper locomotion tasks in simulation. The single leg hopper has 5 degree-of-freedom, with two contact points with the ground located at the heel and the toe of the hopper.

## C.1 3-DOF Kuka Experiments

We use a fully connected network with 2 hidden layers and 64 units in each layer. The policy input for the reaching task is 9-dimensional, which consists of a 6-dimensional robot state and a 3-dimensional goal configuration. The policy input for the pick and place task is 10-dimensional, with 1 additional input dimension encoding the grasp state. The learning rate for policy parameters $\mathbf { l r } _ { p }$ is set to 1e-3, and the learning rate for adversarial perturbation $\mathrm { l r } _ { \mathrm { a d v } }$ is set to 5e-3. The number of adversarial update step K is selected to be 1, and the adversarial bound  is 5e-3. We use N = 5000 trajectory samples with 300 timesteps each. The policy is trained for 300 epochs, with model averaging in the last 75 epochs.

The PPO algorithm as compared in Figure ?? is implemented using Stable Baseline 3 [34].

## C.2 7-DOF Kuka Experiment

We use a residual network with 3 hidden layers (Figure 10) to learn the neural control policy for the 7-DOF Kuka experiment. The policy input is 21-dimensional, which consists of a 14- dimensional robot state and a 7-dimensional target joint angles. The learning rate for policy parameters $\mathbf { l r } _ { p }$ is set to 1e-3, and the learning rate for adversarial perturbation $\mathrm { l r } _ { \mathrm { a d v } }$ is set to 1e-4. The number of adversarial update step K is selected to be 1, and the adversarial bound  is 5e-3. We apply a gradient norm clipping of 1. We use N = 25000 trajectory samples with 200 timesteps each. The policy is trained for 100 epochs, with model averaging in the last 25 epochs.

## D Policy Behavioral Cloning Loss Over ADMM Iterations

Figure 11 shows the behavioral cloning loss $\mathcal { Q } _ { \mathrm { B C } }$ plotted against ADMM iterations. In the cartpole experiment shown in Figure 11(a), $\mathcal { Q } _ { \mathrm { B C } }$ decreases in the first 15 iterations, and gradually increases afterwards. In Kuka experiment (Figure 11(b)), $\mathcal { Q } _ { \mathrm { B C } }$ is improved significantly in the first

![](Zhao2021Adversarially_figs/13dce4acc0a25baf9de90aabb32a03d95d0e48bcdc7decda26fa9ad471b8592c.jpg)  
Figure 10: Illustration of the residual network used for 7-DOF Kuka manipulator experiments. The network consists of 3 hidden layers with 256 units each. A skip connection is included from the output of the $1 ^ { \mathrm { s t } }$ hidden layer to the output of the $3 ^ { \mathrm { r d } }$ hidden layer.

2 iterations, then only slowly decreases from the $3 ^ { \mathrm { r d } }$ iteration onward.

## E Efects of Adversarial Perturbation Bound Value

We evaluate the efect of adversarial perturbation bound  by comparing the 3-DOF Kuka arm policies trained by VERONICA-SAR with a set of perturbation values $\epsilon \in \{ 0 , 0 . 0 0 5 , 0 . 0 1 , 0 . 0 2 5 , 0 . 0 5 \}$ As seen in Figure 12, $\epsilon \in \lbrace 0 . 0 0 5 , 0 . 0 1 \rbrace$ provides the best performances and closely track the TO baseline. $\epsilon = 0$ is equivalent to the policy trained without perturbation, which does not enjoy the generalization and robustness gains provided by VERONICA. In contrast, the policy performance decreases significantly when $\epsilon > 0 . 0 2 5$ , indicating that the adversarial perturbation is too strong and causes underfitting.

## F Theoretical Analysis on Policy Smoothness and Robustness

In this section, we provide a theoretical analysis on how the Lipschitz continuity improves a neural control policy’s robustness. We evaluate the policy’s robustness against state disturbances via value discrepancy propagation analysis [44], where the policy robustness is analyzed by studying how the error caused by state disturbance propagates in the value functions of the policy. As shown in Appendix F.3, the upper bound of the policy robustness (measured by value function discrepancy) is proportional to the Lipschitz constant of the policy. Therefore, controlling the Lipschitz continuity of the policy helps to improve its robustness.

We make the assumption that the poilcy π, the cost function $\ell ( \mathbf { x } , \mathbf { u } )$ , and the system dynamics $f ( \mathbf { x } , \mathbf { u } )$ are globally Lipschitz continuous. Although these assumptions might not hold in all practical cases, the following discussion provides some insight and intuition about why controlling the smoothness of the policy enhances its robustness against various disturbances.

![](Zhao2021Adversarially_figs/b3bdb62d8e1568f16c3fedcd92907b8083a52ff8dd1bbb06fa1b5634b6076ef7.jpg)  
(a)

![](Zhao2021Adversarially_figs/7fe6ef90ca52375e4c13385aebfa531d86a2c2906d8fddd3be4ad0031c94441c.jpg)  
(b)  
Figure 11: The behavioral cloning losses <sup>Q</sup> with respect to ADMM iterations. The policies are trained with VERONICA-SAR for (a) cart-pole and (b) 3-DOF Kuka manipulator.

## F.1 Definitions

$\pi ( \cdot | \mathbf { W } )$ denotes a neural control policy with network parameters W. For notation simplicity, W are omitted in the following discussion. Let $\ell _ { \pi } ( \mathbf { x } ^ { ( t ) } ) = \ell ( \mathbf { x } ^ { ( t ) } , \pi ( \mathbf { x } ^ { ( t ) } ) )$ denote the cost for policy π at state $\mathbf { x } ^ { ( t ) }$ on time-step t. Similarly, $f _ { \pi } ( \mathbf { x } ^ { ( t ) } ) = f ( \mathbf { x } ^ { ( t ) } , \pi ( \mathbf { x } ^ { ( t ) } ) )$ represents the system dynamics under policy π at state $\mathbf { x } ^ { ( t ) }$ . We define the value function $J _ { \pi }$ of policy $\pi ( \mathbf { x } )$ to be the infinite horizon cost with a discount factor $\gamma \in ( 0 , 1 )$ ,

$$
J _ {\pi} (\mathbf {x} ^ {(0)}) = \sum_ {t = 0} ^ {\infty} \gamma^ {t} \ell_ {\pi} (\mathbf {x} ^ {(t)}).
$$

We consider the discount factor for convenience of analysis. The results can be extended to the average cost setting, but will be more involved.

The Lipschitz constant of $\pi , \ell _ { \pi } , f _ { \pi } ,$ , and $J _ { \pi }$ are denoted as $C _ { \pi } , C _ { \ell _ { \pi } } , C _ { f _ { \pi } }$ , and $C _ { J _ { \pi } }$ respectively. $C _ { \ell } ^ { \mathbf { u } }$ and $C _ { f } ^ { \mathbf { u } }$ represents the Lipschitz constant of $\ell ( \mathbf { x } , \mathbf { u } )$ and $f ( \mathbf { x } , \mathbf { u } )$ with respect to u.

## F.2 Lipschitz Continuity of Value Function

Lemma 1: Given a neural control policy π with Lipschitz continuous cost function $\ell _ { \pi }$ and dynamics $f _ { \pi }$ , and let $\gamma C _ { f _ { \pi } } < 1$ . The value function $J _ { \pi }$ is Lipschitz continuous and the Lipschitz constant is $C _ { J _ { \pi } } =$ $\frac { C _ { \ell _ { \pi } } } { 1 - ( \gamma C _ { f _ { \pi } } ) ^ { t } }$

![](Zhao2021Adversarially_figs/2a1d19a568bdcc9428059bca2be882bec9cdf40952321afb8d1fe94e76fc69eb.jpg)  
Figure 12: Cost percentile plot for 3-DOF arm policy rollout with 100 diferent initializations. The policies are trained with diferent adversarial perturbation bounds 

Proof:

$$
\begin{array}{r l} & {\| J _ {\pi} (\mathbf {x} ^ {(0)}) - J _ {\pi} (\mathbf {y} ^ {(0)}) \|} \\ & {= \sum_ {t = 0} ^ {\infty} \gamma^ {t} \| \ell_ {\pi} (f _ {\pi} (\mathbf {x} ^ {(t)})) - \ell_ {\pi} (f _ {\pi} (\mathbf {y} ^ {(t)})) \|} \\ & {\leq \sum_ {t = 0} ^ {\infty} C _ {\ell_ {\pi}} \gamma^ {t} \| f _ {\pi} (\mathbf {x} ^ {(0)}) - f _ {\pi} (\mathbf {y} ^ {(0)}) \|} \\ & {\leq (\sum_ {t = 0} ^ {\infty} (\gamma C _ {f _ {\pi}}) ^ {t}) C _ {\ell_ {\pi}} \| \mathbf {x} ^ {(0)} - \mathbf {y} ^ {(0)} \|} \\ & {= \frac {C _ {\ell_ {\pi}}}{1 - (\gamma C _ {f _ {\pi}}) ^ {t}} \| \mathbf {x} ^ {(0)} - \mathbf {y} ^ {(0)} \|} \end{array}
$$

## F.3 Value Discrepancy Under State Disturbances

Lemma 2 below shows that the value discrepancy for a policy π caused by a norm bounded perturbation is proportional to the Lipschitz constant of the policy.

Lemma 2: Given a neural control policy π and let $\pmb { \delta } ^ { ( t ) }$ be the state disturbance at time-step t norm bounded by $\| \delta ^ { ( t ) } \| \le \zeta$ . Let $\pi ^ { \prime } ( \mathbf { x } ^ { ( t ) } ) = \pi ( \mathbf { x } ^ { ( t ) } + \pmb { \delta } ^ { ( t ) } )$ denote the disturbed neural control policy. The discrepancy between value functions $J _ { \pi ^ { \prime } }$ and $J _ { \pi }$ has an upper bound of $C _ { \pi } ( \frac { C _ { \ell } ^ { u } + \gamma C _ { J _ { \pi } } C _ { f } ^ { u } } { 1 - \gamma } ) \zeta$

Proof:

The value function $J _ { \pi }$ satisfies:

$$
J _ {\pi} (\mathbf {x}) = \ell_ {\pi} (\mathbf {x}) + \gamma J _ {\pi} (f _ {\pi} (\mathbf {x})).
$$

Therefore, the value discrepancy due to disturbances $\pmb { \delta }$ can be written as the following:

$$
\begin{array}{l} J _ {\pi^ {\prime}} (\mathbf {x}) - J _ {\pi} (\mathbf {x}) \\ = \ell_ {\pi^ {\prime}} (\mathbf {x}) - \ell_ {\pi} (\mathbf {x}) + \gamma (J _ {\pi^ {\prime}} (f _ {\pi^ {\prime}} (\mathbf {x})) - J _ {\pi} (f _ {\pi} (\mathbf {x}))) \\ \leq C _ {\ell} ^ {\mathbf {u}} \| \pi^ {\prime} (\mathbf {x}) - \pi (\mathbf {x}) \| + \gamma (J _ {\pi} (f _ {\pi^ {\prime}} (\mathbf {x})) - J _ {\pi} (f _ {\pi} (\mathbf {x}))) + \gamma (J _ {\pi^ {\prime}} (f _ {\pi^ {\prime}} (\mathbf {x})) - J _ {\pi} (f _ {\pi^ {\prime}} (\mathbf {x}))) \\ \leq C _ {\ell} ^ {\mathbf {u}} C _ {\pi} \zeta + \gamma C _ {J _ {\pi}} C _ {f} ^ {\mathbf {u}} C _ {\pi} \zeta + \gamma (J _ {\pi^ {\prime}} (f _ {\pi^ {\prime}} (\mathbf {x})) - J _ {\pi} (f _ {\pi^ {\prime}} (\mathbf {x}))) \qquad \text {(by Lemma 1)} \\ \leq C _ {\pi} (\frac {C _ {\ell} ^ {\mathbf {u}} + \gamma C _ {J _ {\pi}} C _ {f} ^ {\mathbf {u}}}{1 - \gamma}) \zeta . \end{array}
$$