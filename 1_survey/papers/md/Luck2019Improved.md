---
citation_key: Luck2019Improved
arxiv_id: 1911.06833
arxiv_url: https://arxiv.org/abs/1911.06833
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-24T16:58:56Z
origin: ai+web
reviewed: false
---

# Introduction

Reinforcement learning (RL) methods enabled the development of autonomous systems that can autonomously learn and master a task when provided with an objective function. RL has been successfully applied to a wide range of tasks including flying [@tedrake2009learning; @reddy2018glider], manipulation [@vevcerik2017leveraging; @li2019robot; @luck2017extracting; @colome2019exploiting; @chebotar2018closing], locomotion [@li2018using; @luck2017lab2desert], and even autonomous driving [@jaritz2018end; @kendall2018learning]. The vast majority of RL algorithms can be classified into the two categories of (a) inherently stochastic or (b) deterministic methods. While inherently stochastic methods have their exploration typically built-in [@haarnoja2018soft; @schulman2017proximal], their deterministic counterparts require an, often independent, exploration strategy for the acquisition of new experiences within the task domain [@lillicrap2015continuous; @kober2009policy]. In deep reinforcement learning, simple exploration strategies such as Gaussian noise or Ornstein-Uhlenbeck (OU) processes [@uhlenbeck1930theory], which model Brownian motion, are standard practice and have been found to be effective [@lillicrap2015continuous]. However, research has shown that advanced exploration strategies can lead to a higher sample-efficiency and performance of the underlying RL algorithm [@luck2014latent].

![A Baxter robot learning a visuo-motor policy for an insertion task using efficient exploration in latent spaces. The peg is suspended from a string. ](Luck2019Improved_figs/front_pic_scaled_darker.JPG){#Fig::teaser width="42%"}

In practice, there are two ways to incorporate advanced exploration strategies into deterministic policy search methods. Where possible, one can reformulate the deterministic approach within a stochastic framework, such as by modeling the actions to be sampled as a distribution. Parameters of the distribution can then be trained and are tightly interconnected with the learning framework. One example for this methodology, is the transformation of Policy Search with Weighted Returns (PoWER) [@kober2009policy] into Policy Search with Probabilistic Principal Component Exploration (PePPEr) [@luck2014latent]. Instead of using a fixed Gaussian distribution for exploration, the noise generating process in PePPEr is based on Probabilistic Principal Component Analysis (PPCA) and generates samples along the latent space of high-reward actions. Generating explorative noise from PPCA and sampling along the latent space was shown to outperform the previously fixed Gaussian exploration. Alternatively, one can choose to optimize the exploration strategy itself. Examples of this methodology are count-based exploration strategies [@tang2017exploration], novelty search [@stadie2015incentivizing] or curiosity-driven approaches [@pathak2017curiosity] which can be transferred with ease to other algorithms or frameworks. Typically, when incorporating these techniques into reinforcement learning, they are limited to local exploration cues based on the current state. This paper aims to combine the model-free deep deterministic policy gradient method with a model-based exploration technique for increased sample-efficiency in real world task domains. The proposed method generates exploratory noise by optimizing a (latent) trajectory from the current state to ideal future states, based on value functions learned by an RL algorithm. This experience is, in turn, used by the RL algorithm to optimize policy and value functions in an off-policy fashion, providing an improved objective function for the trajectory optimizer. We investigate whether this strategy of formulating exploration as a latent trajectory optimization problem leads to an improved learning process both in simulation, as well as in a robotic insertion task executed solely in the real world. In particular, we apply our approach to a challenging, flexible insertion task as seen in Fig. [1](#Fig::teaser){reference-type="ref" reference="Fig::teaser"}.

:::: {#Fig::baxter::setup .figure}
![Rand. initial position](Luck2019Improved_figs/robot_task_cut_init.png){width="95%"}

![Insertion started](Luck2019Improved_figs/robot_task_cut_new.png){width="95%"}

::: caption
The experimental setup in which a Baxter robot has to insert a blue cylinder into a white tube (b). The cylinder is with a string attached to the end-effector of the robot. Camera images are recorded with the integrated end-effector camera. The sensor detecting the state of insertion is integrated into the white tube. Experiments on this platform were run fully autonomously without human intervention or simulations.
:::
::::

# Related Work

The advancement of deep reinforcement learning in recent years has lead to the development of a number of methods combining model-free and model-based learning techniques, in particular to improve the sample complexity of deep reinforcement learning methods. Nagabandi et al. [@nagabandi2018neural] present a model-based deep reinforcement learning approach which learns a deep dynamic function mapping a state and action pair $(\ensuremath{\mathbf{s}}_t, \ensuremath{\mathbf{a}}_t)$ to the next state $\ensuremath{\mathbf{s}}_{t+1}$. The dynamics function is used to unroll a trajectory and to create an objective function based on the cumulative reward along the trajectory. This objective function is, then, used to optimize the actions along the trajectory and thereafter the first action is executed. The procedure is repeated whenever the next state is reached. After a dataset of executed trajectories is collected by the planning process, the policy of a model-free reinforcement learning algorithm is initialized in a supervised fashion by training it to match the actions produced by the planner. This technique is different to our approach in that we do not force the actor to match the executed action, but rather see it as an exploration from which we generate off-policy updates. Furthermore, it is implicitly assumed in [@nagabandi2018neural] that a reward function is available for each state during the planning process. This can be a rather strong assumption, especially when learning in the real world without access to a simulation of the task and only providing minimal human supervision. Using executions in the environment during the planning process would be too costly since each change in state would require a re-execution of the whole trajectory. Since our insertion task provides only sparse rewards during execution, the trajectory planning algorithm would fail when relying only on rewards due to flat regions with zero reward and require additional reward engineering. This leaves a large and mostly flat region in the state space with a reward of zero.

In [@chua2018deep], Chua et al. introduce the model-based *probabilistic ensembles with trajectory sampling* method. This work builds upon [@nagabandi2018neural], but also makes use of a reward function. It makes use of a probabilistic formulation of the deep dynamics function by using an ensemble of bootstrapped models encoding distributions to improve the sample complexity and improves the properties of the trajectory planner. Both approaches do not explicitly train an actor or a critic network.

Similarly to us, Universal planning networks [@srinivas2018universal] introduced by Srinivas et al. use a latent, gradient-based trajectory optimization method. However, the planner requires a goal state for the trajectory optimization. In certain tasks such as walking or running, it might be hard to acquire such a goal state to use in place of a velocity-based reward function. It is mentioned in [@srinivas2018universal] that to achieve walking, it was necessary to re-render images or reformulate the objective function by including an accessible dense reward function.

In contrast to previous work, we focus explicitly on the impact of using trajectory optimization as an additional technique for exploration and its impact on the learning process when used by a deep reinforcement learning algorithm such as Deep Deterministic Policy Gradient. Furthermore, using an actor-critic architecture is a key element in our work to allow off-policy updates in a fast manner during the training process and to inform the trajectory optimization process initially.

# Method

The following sections introduce the different components used to generate explorative actions via trajectory optimization. We first describe the image embedding used, then the training process of the dynamics function and Deep Deterministic Policy Gradient (DDPG) [@lillicrap2015continuous], as well as its extension for the use of a value function. The section ends with a description of our trajectory optimization based exploration for DDPG.

## Image Embedding

All tasks used throughout this paper are setup such that they use only images as observations, which have to be projected into a latent image embedding. This serves two main purposes: First, the number of parameters is greatly reduced since the actor, critic, and the dynamics network can be trained directly in the low dimensional latent space. Second, it is desirable to enforce temporal constraints within the latent image embedding, namely that subsequent images are close to each other after being projected into the latent space. Therefore, we make use of the recently introduced approach of time-contrastive networks [@sermanet2017time]: the loss function enforces that the distance between latent representations of two subsequent images are small but the distance between two randomly chosen images is above a chosen threshold $\alpha$. Enforcing a temporal constraint in the latent space improves the learning process of a consistent deep dynamics function in the latent space [@sermanet2017time]. Time-contrastive networks make use of two losses. The first is defined on the output of the decoder network and the input image as found in most autoencoder implementations. The second loss, the triplet loss, takes the latent representation $\mathbf{z}_t$ and $\mathbf{z}_{t+1}$ of two temporally close images and the latent representation $\mathbf{z}_r$ of a randomly chosen image.

Thus, given two temporal images $\ensuremath{\mathbf{\text{Im}}}_t$ and $\ensuremath{\mathbf{\text{Im}}}_{t+1}$ and a randomly chosen image $\ensuremath{\mathbf{\text{Im}}}_{r}$, the loss functions for each element in the batch is given by $$\begin{equation}
    L(\ensuremath{\mathbf{\text{Im}}}_t, \ensuremath{\mathbf{\text{Im}}}_{t+1}, \ensuremath{\mathbf{\text{Im}}}_r) = L_{\text{ae}}(\ensuremath{\mathbf{\text{Im}}}_t) + L_{\text{contr}}(\ensuremath{\mathbf{\text{Im}}}_t, \ensuremath{\mathbf{\text{Im}}}_{t+1}, \ensuremath{\mathbf{\text{Im}}}_r).
\end{equation}$$ The classical autoencoder loss $L_{\text{ae}}$ and the contrastive loss $L_{\text{contr}}$ are here defined as $$\begin{equation}
    \begin{split}
        &L_{\text{ae}} = \parallel \ensuremath{\mathbf{\text{Im}}}_t - \ensuremath{\text{D}}(\ensuremath{E}(\ensuremath{\mathbf{\text{Im}}}_t)) \parallel, \\
        &L_{\text{contr}} \left( \ensuremath{\mathbf{\text{Im}}}_t, \ensuremath{\mathbf{\text{Im}}}_{t+1}, \ensuremath{\mathbf{\text{Im}}}_r \right) = \parallel \ensuremath{E}(\ensuremath{\mathbf{\text{Im}}}_{t}) - \ensuremath{E}(\ensuremath{\mathbf{\text{Im}}}_{t+1})\parallel \\
         & \hspace{3ex}+ \max(\alpha - \parallel\ensuremath{E}(\ensuremath{\mathbf{\text{Im}}}_{t}) - \ensuremath{E}(\ensuremath{\mathbf{\text{Im}}}_r)\parallel, 0),
    \end{split}
\end{equation}$$ with $\ensuremath{E}$ being the encoder and $\ensuremath{\text{D}}$ being the decoder network. The scalar value $\alpha$ defines the desired minimum distance between two random images in the latent embedding. Thus the classic autoencoder loss $L_{\text{ae}}$ trains both the encoder and decoder network to learn a reconstructable image embedding. The contrastive loss $L_{\text{contr}}$, on the other hand, generates only a learning signal for the encoder network and places a temporal constraint on the image embedding. The encoder and decoder consist of three convolutional networks with a kernel shape of $(3,3)$ and a stride of $(2,2)$, followed by a linear layer of size 20 and an l2-normalized embedding which projects the states on a unit sphere [@sermanet2017time]. All activation functions are rectified linear units (ReLU).

## Latent Dynamics

Using a trajectory optimization algorithm in latent space requires a dynamics function which maps a latent state $\ensuremath{\mathbf{z}}_t$ and an action $\ensuremath{\mathbf{a}}_t$ to a subsequent latent state $\ensuremath{\mathbf{z}}_{t+1}$. This allows us to unroll trajectories into the future. In the case of a single image with $\ensuremath{\mathbf{z}}_t=\ensuremath{E}(\ensuremath{\mathbf{\text{Im}}}_t)$, we learn a dynamics mapping of $\ensuremath{\Psi}(\ensuremath{\mathbf{z}}_t, \ensuremath{\mathbf{a}}_t)=\tilde{\ensuremath{\mathbf{z}}}_{t+1}$. In the other case, when our latent state is derived from several stacked images, then we project each image into the latent space, for example by $$\begin{equation}
    \begin{bmatrix}
        \ensuremath{E}(\ensuremath{\mathbf{\text{Im}}}_{t-2}) \\
        \ensuremath{E}(\ensuremath{\mathbf{\text{Im}}}_{t-1}) \\
        \ensuremath{E}(\ensuremath{\mathbf{\text{Im}}}_{t}) \\
    \end{bmatrix}
    =
    \begin{bmatrix}
        \ensuremath{\mathbf{z}}_{t}^{t-2} \\
        \ensuremath{\mathbf{z}}_{t}^{t-1} \\
        \ensuremath{\mathbf{z}}_{t}^{t} \\
    \end{bmatrix}
    = \ensuremath{\mathbf{z}}_t.
\end{equation}$$ To predict the next latent state, the dynamics function simply has to rotate the state and only predict the third latent sub-state. This function can be described with $$\begin{equation}
    \ensuremath{\mathbf{z}}_t = 
    \begin{bmatrix}
        \ensuremath{\mathbf{z}}_{t}^{t-2} \\
        \ensuremath{\mathbf{z}}_{t}^{t-1} \\
        \ensuremath{\mathbf{z}}_{t}^{t} \\
    \end{bmatrix}
    \mapsto 
    \begin{bmatrix}
        \ensuremath{\mathbf{z}}_{t}^{t-1} \\
        \ensuremath{\mathbf{z}}_{t}^{t} \\
        \overline{\ensuremath{\Psi}}(\ensuremath{\mathbf{z}}_t, \ensuremath{\mathbf{a}}_t) \\
    \end{bmatrix}
    = \tilde{\ensuremath{\mathbf{z}}}_{t+1},
\end{equation}$$ where $\overline{\ensuremath{\Psi}}$ is the output of the neural network while we will use the notation $\ensuremath{\Psi}(\ensuremath{\mathbf{z}}_t, \ensuremath{\mathbf{a}}_t)=\tilde{\ensuremath{\mathbf{z}}}_{t+1}$ for the whole operation, and $\tilde{\ensuremath{\mathbf{z}}}_{i+1}$ is the predicted next latent state. The loss function for the dynamics network is then simply the difference between the predicted latent state and the actual latent state. Therefore, the loss is given as $$\begin{equation}
    \begin{split}
    L_{\text{dyn}}(\ensuremath{\mathbf{\text{Im}}}_{t-2:t}, \ensuremath{\mathbf{a}}_t, \ensuremath{\mathbf{\text{Im}}}_{t+1}) =~\parallel
    &\overline{\ensuremath{\Psi}}(\ensuremath{\mathbf{z}}_{t}, \ensuremath{\mathbf{a}}_t) - \ensuremath{E}(\ensuremath{\mathbf{\text{Im}}}_{t+1}) \parallel,
    \end{split}
\end{equation}$$ for each state-action-state triple $(\ensuremath{\mathbf{\text{Im}}}_{t-2:t}, \ensuremath{\mathbf{a}}_t, \ensuremath{\mathbf{\text{Im}}}_{t-1:t+1})$ observed during execution. The dynamics networks is constructed out of 3 fully connected layers of size 400, 400 and 20 with ReLUs as nonlinear activation functions.

## Deep Reinforcement Learning

We make use of the Deep Deterministic Policy Gradient (DDPG) algorithm since action and state/latent space are continuous. DDPG is based on the actor-critic model which is characterized by the idea to generate a training signal for the actor (network) from the critic (network). In turn, the critic utilizes the actor to achieve an off-policy update and models usually a Q-value function. In DDPG, the actor is a network mapping (latent) states to an action with the goal of choosing optimal actions under a reward function. Hence, the loss function for the actor is given by $$\begin{equation}
    \begin{split}
        L_{\text{actor}}(\ensuremath{\mathbf{z}}_t) = -\ensuremath{\text{Q}}(\ensuremath{\mathbf{z}}_t, \ensuremath{\pi}(\ensuremath{\mathbf{z}}_t)),
    \end{split}
\end{equation}$$ where only the parameters of the actor $\ensuremath{\pi}(\ensuremath{\mathbf{z}}_t)$ are optimized (see Eq. 6 in [@lillicrap2015continuous]). In the case of classical DDPG, the critic is a Q-function network, which maps state and action pairs to a Q-value: $Q(\ensuremath{\mathbf{z}}_t, \ensuremath{\mathbf{a}}_t) = r(\ensuremath{\mathbf{z}}_t, \ensuremath{\mathbf{a}}_t) + \gamma Q(\ensuremath{\mathbf{z}}_{t+1}, \ensuremath{\pi}(\ensuremath{\mathbf{z}}_{t+1}))$. The scalar $gamma$ is a discount factor and $r(\ensuremath{\mathbf{z}}_t, \ensuremath{\mathbf{a}}_t)$ is the reward. The loss function of the critic network is based on the Bellman equation: $$\begin{equation}
    \begin{split}
         L_{\text{critic}}(\ensuremath{\mathbf{z}}_t, \ensuremath{\mathbf{a}}_t, r_{t+1}, \ensuremath{\mathbf{z}}_{t+1}) = &\parallel \ensuremath{\text{Q}}(\ensuremath{\mathbf{z}}_t, \ensuremath{\mathbf{a}}_t) - \\
        &~(r_{t+1} + \gamma \ensuremath{\text{Q}}^\prime(\ensuremath{\mathbf{z}}_{t+1}, \ensuremath{\pi}^\prime(\ensuremath{\mathbf{z}}_{t+1}))) \parallel,
    \end{split}
\end{equation}$$ where $\ensuremath{\text{Q}}^\prime$ and $\ensuremath{\pi}^\prime$ are target networks. For more details on DDPG we refer the interested reader to [@lillicrap2015continuous].

:::: {#Fig::ddpg:q_and_v .figure}
![Q-Value based actor update](Luck2019Improved_figs/ddpg_q.png){height="4.5cm"}

![Value based actor update](Luck2019Improved_figs/ddpg_v.png){width="95%"}

::: caption
The original DDPG algorithm (a) can be reformulated such that a value function (b) is used. In the case of a value function the policy gradient (red arrow) is computed via a neural dynamics function.
:::
::::

It is worth noting that DDPG can be reformulated such that the critic resembles a value function instead of a Q-value function (Fig. [3](#Fig::ddpg:q_and_v){reference-type="ref" reference="Fig::ddpg:q_and_v"}, see also [@heess2015learning]). A naive reformulation of the loss function given above is $$\begin{equation}
    \begin{split}
        L_{\text{critic}}(\ensuremath{\mathbf{z}}_t, \ensuremath{\mathbf{a}}_t, r_t, \ensuremath{\mathbf{z}}_{t+1}) = &\parallel \ensuremath{\text{V}}(\ensuremath{\mathbf{z}}_t) - (r_{t+1} + \gamma\ensuremath{\text{V}}^\prime(\ensuremath{\mathbf{z}}_{t+1})) \parallel,
    \end{split}
\end{equation}$$ given an experience $(\ensuremath{\mathbf{z}}_t, \ensuremath{\mathbf{a}}_t, r_{t+1}, \ensuremath{\mathbf{z}}_{t+1})$. But this reformulation updates only on-policy and lacks the off-policy update ability of classical DDPG. Even worse, we would fail to use such a critic to update the actor since no action gradient can be computed due to the sole dependency on the state. However, since we have access to a dynamics function we reformulate for our extension of DDPG the loss function and incorporate off-policy updates with $$\begin{equation}
    \begin{split}
        L_{\text{critic}}(\ensuremath{\mathbf{z}}_t, \ensuremath{\mathbf{a}}_t, r_t, \ensuremath{\mathbf{z}}_{t+1}) = &\parallel \ensuremath{\text{V}}(\ensuremath{\mathbf{z}}_t)\\&- (r_t + \gamma \ensuremath{\text{V}}^\prime(\ensuremath{\Psi}({\ensuremath{\mathbf{z}}}_{t}, \ensuremath{\pi}^\prime(\ensuremath{\mathbf{z}}_t ))) \parallel.\\
    \end{split}
\end{equation}$$ This formulation allows for off-policy updates given the experience $(\ensuremath{\mathbf{z}}_t, \ensuremath{\mathbf{a}}_t, r_{t}, \ensuremath{\mathbf{z}}_{t+1})$, for which we assume that the reward $r(\ensuremath{\mathbf{z}})$ is only state-dependent. While this might appear to be a strong assumption at first, it holds true for most tasks in robotics. The insertion task presented in the remainder of this paper is such a case in which the reward is fully described by the current position of both end-effector and the object to be inserted.

The loss function for the actor is then given with $$\begin{equation}
    \begin{split}
        L_{\text{actor}}(\ensuremath{\mathbf{z}}_t) = -\ensuremath{\text{V}}(\ensuremath{\Psi}(\ensuremath{\mathbf{z}}_t, \ensuremath{\pi}(\ensuremath{\mathbf{z}}_t))),
    \end{split}
\end{equation}$$ which is fully differentiable and, again, only used to optimize the parameters of the actor network. We use for both actor and critic two fully connected hidden layers of size 400 and 300 with ReLUs as nonlinear activation functions.

## Optimized Exploration

![The proposed exploration strategy unrolls the trajectory in the latent space and uses the Value/Q-Value to optimize the actions of the trajectory. Dotted connections might not be used when using a Value function as critic. ](Luck2019Improved_figs/dyna.png){#Fig::traj_opt width="45%"}

Due to the deterministic nature of the actor network in DDPG and similar algorithms, the standard approach for exploration is to add random noise to actions. Random noise is usually generated from an Ornstein-Uhlenbeck process or a Gaussian distribution with fixed parameters. Such parameters, like the variance for a Gaussian distribution, are usually chosen by intuition or have to be optimized as hyper-parameter, for example with grid-search. In preliminary experiments we found Ornstein-Uhlenbeck processes with $\sigma=0.5$ and $\theta=0.15$ most effective on the chosen simulated task. In the presented approach we make use of the fact that we can access a dynamics function and therefore unroll trajectories throughout the latent space. The basic idea is to first unroll a trajectory using the actor network a number of steps into the future from the current point in time. We then optimize the actions $\ensuremath{\mathbf{a}}_t, \cdots, \ensuremath{\mathbf{a}}_{t+n}$ such that we maximize the Q-values/rewards along the latent trajectory. We characterize a latent trajectory, given a start state $\ensuremath{\mathbf{z}}_t = \ensuremath{E}(\ensuremath{\mathbf{\text{Im}}}_t)$, as a sequence of state-action pairs $(\ensuremath{\mathbf{z}}_t, \ensuremath{\mathbf{a}}_t, \cdots, \ensuremath{\mathbf{z}}_{t+H}, \ensuremath{\mathbf{a}}_{t+H}, \ensuremath{\mathbf{z}}_{t+H+1})$. We can then formulate a scalar function to be maximized by the trajectory optimizer based on the Q-value or reward-functions available. This process is visualized in Fig. [4](#Fig::traj_opt){reference-type="ref" reference="Fig::traj_opt"}. The Q-function in the following equations can be substituted with a learned value function. An intuitive objective function to optimize is to simply sum up all Q-values for each state-action pair of the trajectory $$\begin{equation}
    \begin{split}
        f_{Q}(\ensuremath{\mathbf{a}}_{t:t+H}, \ensuremath{\mathbf{z}}_t) = w_{0} Q(\ensuremath{\mathbf{z}}_{t}, \ensuremath{\mathbf{a}}_t) + \sum_{j=1}^{H} w_{j} Q(\ensuremath{\mathbf{z}}_{t+j}, \ensuremath{\mathbf{a}}_{t+j}),
    \end{split}
    \label{Eq::Q}
\end{equation}$$ with $\ensuremath{\mathbf{z}}_{t+j} = \ensuremath{\Psi}(\ensuremath{\mathbf{z}}_{t+j-1}, \ensuremath{\mathbf{a}}_{t+j-1})$ and $\ensuremath{\mathbf{z}}_t$ being the current state from which we start unrolling the trajectory. The time-dependent weight $w_i$ determines how much actions are going to be impacted by future states and their values and can be uniform, linearly increasing or exponential. We consider in our experiments the special case of $w_i=\frac{1}{H}$. Alternatively, if one has access to a rewards function or learns a state-to-reward mapping simultaneously, then an objective function can be used which accumulates all rewards along the latent trajectory and adds only the final q-value: $$\begin{equation}
    \begin{split}
     f_{r+Q}(\ensuremath{\mathbf{a}}_{t:t+H}, \ensuremath{\mathbf{z}}_t) =& \sum_{j=1}^{H-1} w_j r(\ensuremath{\mathbf{z}}_{t+j})  + w_{H}Q(\ensuremath{\mathbf{z}}_{t+H}, \ensuremath{\mathbf{a}}_{t+H}).
    \end{split}
    \label{Eq::QR}
\end{equation}$$ Clearly, this objective function is especially useful in the context of tasks with dense rewards. Both objective functions will be evaluated on the simulated cheetah task, which provides such dense rewards. While executing policies in the real world, we unroll a planning trajectory from the current state for $n$ steps into the future. Then, the actions $\ensuremath{\mathbf{a}}_{t:t+H}$ are optimized under one of the introduced objectives from above with a gradient-based optimization method such as L-BFGS [@zhu1997algorithm]. After a number of iterations of trajectory optimization, here 20, the first action of the trajectory, namely $\ensuremath{\mathbf{a}}_t$, is executed in the real world (Alg. [\[alg1\]](#alg1){reference-type="ref" reference="alg1"}).

:::: algorithm
::: algorithmic
Horizon $H$, Encoder network
:::
::::

# Experiments

We compare in our experiments the classical approach of exploration in DDPG with an optimized Ornstein-Uhlenbeck process against the introduced approach of exploration through optimization. First, an experiment in simulation was conducted using the DeepMind Control Suite [@tassa2018deepmind]. The cheetah task, in which a two-dimensional bipedal agent has to learn to walk, is especially interesting because it involves contacts with the environment that makes the dynamics hard to model. In the second experiment, we evaluate the algorithms directly on a robot and aim to solve an insertion task in the real world.

## Evaluation in Simulation on the Cheetah Task

The cheetah environment of the DeepMind control suite [@tassa2018deepmind] has six degrees-of-freedom in its joints and we only use camera images as state information. The actions are limited to the range of $[-1,1]$ and camera images are of the size $320\times240~px$ in RGB and were resized to $64\times64~px$. Each episode consists of 420 time steps and actions are repeated two times per time step. First, a dataset of 50 representative episodes was collected through the use of DDPG on the original state space of joint positions, joint velocities, relative body pose and body velocity of cheetah. This dataset was used to train the time-contrastive autoencoder as described above. The same parameters for the neural encoder were use for all exploration strategies. This was done to allow the sole evaluation of the exploration strategies independently of the used embedding. Since cheetah is a quite dynamic task and rewards depend on the forward velocity, this velocity must be inferable from each state. Hence, we project three subsequent images $(\ensuremath{\mathbf{\text{Im}}}_{t-2}, \ensuremath{\mathbf{\text{Im}}}_{t-1}, \ensuremath{\mathbf{\text{Im}}}_t)$ down by using the encoder network and define the current state $\ensuremath{\mathbf{z}}_t$ as the three stacked latent states $\ensuremath{\mathbf{z}}_t=[\ensuremath{\mathbf{z}}_{t-2}, \ensuremath{\mathbf{z}}_{t-1}, \ensuremath{\mathbf{z}}_{t}]^T$. For each of the presented evaluations 25 experiments were executed and the mean and standard deviations of the episodic cumulative rewards are shown in Figures [5](#Fig::cheetah::basic){reference-type="ref" reference="Fig::cheetah::basic"}-[8](#Fig::objectives){reference-type="ref" reference="Fig::objectives"}.

:::: {#Fig::cheetah::basic .figure}
![Deterministic Policy (Q-Value)](Luck2019Improved_figs/fig_5_test.png){width="\\textwidth"}

![Exploration (Q-Value)](Luck2019Improved_figs/fig_5_training.png){width="\\textwidth"}

![Deterministic Policy (Value)](Luck2019Improved_figs/fig_2_test_recolored.png){width="\\textwidth"}

![Exploration (Value)](Luck2019Improved_figs/fig_2_training_recolored.png){width="\\textwidth"}

::: caption
Comparison between DDPG using exploration with optimization (orange) and classical exploration using an Ornstein-Uhlenbeck process (blue) on the simulated cheetah task. The exploitation graph shows the evaluation of actions produced by the deterministic actor while exploration strategies are applied during training.
:::
::::

![Comparison between DDPG using exploration with optimization (orange) and classical exploration using an Ornstein-Uhlenbeck process (blue) on the simulated cheetah task while using a value function as critic. The number of training iterations per episode were raised from 1000 (Fig. [5](#Fig::cheetah::basic){reference-type="ref" reference="Fig::cheetah::basic"}-d) to 3000 for this evaluation. ](images/fig_1_training.png){#Fig::cheetah:3000 width="40%"}

### Comparison between Ornstein-Uhlenbeck and optimized exploration

As a first step we optimized the hyperparameter $\sigma$ of DDPG and found that an Ornstein-Uhlenbeck process with $\sigma=0.5$ and $\theta=0.15$ achieve a better result for DDPG on this task than the variance of $\sigma=0.2$ proposed in [@lillicrap2015continuous], especially in the early stages of the training process. A planning horizon of ten steps was used to generate the optimized noise. We make comparisons between the training process, in which we use the exploration strategies, and the test case, in which we execute the deterministic actions produced by the actor without noise. Throughout the training process we evaluate the current policy of the actor after each episode. The results are presented in Fig. [5](#Fig::cheetah::basic){reference-type="ref" reference="Fig::cheetah::basic"}.

### Comparison between different planning horizons

The main hyperparameter for optimized noise is the length of the planning horizon. If it is too short, actions are optimized greedily for immediate or apparent short-term success; if it is too long, the planning error becomes too large. Figure [7](#Fig::cheetah::steps){reference-type="ref" reference="Fig::cheetah::steps"} shows the optimized exploration strategy with three different step-sizes: one step, ten steps and 20 steps into the future from the current state.

:::: {#Fig::cheetah::steps .figure}
![](Luck2019Improved_figs/fig_6_training.png){width="\\textwidth"}

::: caption
Exploration through optimization evaluated with different horizons for the planning trajectory on the simulated cheetah task.
:::
::::

### Comparison between different objectives

We introduced two potential objective functions, based on Q-values (Eq. [\[Eq::Q\]](#Eq::Q){reference-type="ref" reference="Eq::Q"}) and a mix of reward- and Q-function (Eq. [\[Eq::QR\]](#Eq::QR){reference-type="ref" reference="Eq::QR"}). We compare both of these against another objective where we only optimize for the q-value of the very last state-action pair of the unrolled trajectory (Fig. [8](#Fig::objectives){reference-type="ref" reference="Fig::objectives"}).

![Comparison between three different objective functions for optimized exploration on the simulated cheetah task. ](Luck2019Improved_figs/fig_7_training.png){#Fig::objectives width="40%"}

:::: {#Fig::baxter::basic .figure}
![Deterministic Policy](Luck2019Improved_figs/baxter_sb_test_rect_type1.png){width="\\textwidth"}

![Exploration](Luck2019Improved_figs/baxter_sb_training_rect_type1.png){width="\\textwidth"}

::: caption
Comparison between exploration with an Ornstein-Uhlenbeck (blue) and exploration through optimization (red) on the insertion task in the real world. The planning horizon is three steps. The figures show the cumulative rewards averaged over five experiments in light colours and in bold colours, for better interpretability due to the sparse reward, the mean smoothed with a Savitzky-Golay filter with window size 21 and 1st order polynomials.
:::
::::

::: {#Tabel::Horizons}
  Method                            Avg. Success rate $(\pm std)$
  -------------------------------- --------------------------------
  Ornstein-Uhlenbeck Exploration        $75.2\% ~(\pm 11.7\%)$
  1 Step Planning Horizon           $\mathbf{93.2}\% ~(\pm 5.2\%)$
  3 Steps Planning Horizon          $91.6\% ~(\pm \mathbf{1.5}\%)$
  5 Steps Planning Horizon              $84.0\% ~(\pm 14.1\%)$
  15 Steps Planning Horizon              $84.4\% ~(\pm 9\%)$

  : The average success rate of insertion for policies trained by DDPG with standard Ornstein-Uhlenbeck exploration or trajectory optimization with varying planning horizons. The individual success rates for each experiment were computed over a window of 50 subsequent episodes of 500 executions total. The average success rates and standard deviations were then computed with the highest success rate achieved in each experiment. A total of five experiments were executed for each method.
:::

## Insertion in the real world

Fast exploration is especially important when tasks have to be solved in a real world environment and training needs to be executed on the real robot. An insertion task was set up in which a Baxter robot had to insert a cylinder into a tube where both training and testing were performed in the real world environment, without the use of simulation (Fig. [2](#Fig::baxter::setup){reference-type="ref" reference="Fig::baxter::setup"}) [^3]. Cylinder and tube were 3D-printed. The cylinder was attached to the right end-effector of the robot with a string. The position control mode was used because there is a variable delay in the observations. Image observation were acquired from the end-effector camera of the Baxter robot via ethernet. The six dimensional actions are in the range of $[-0.05, 0.05]$ radians and represent the deviation for each joint of the arm at a point in time. This restriction ensures a strong correlation between subsequent camera images throughout the execution and allows the task to be solved in 20 steps. The initial position (radians) of the robot arm was randomized by sampling from a normal distribution with mean $\mu_{1:6}=(0.48, -1.23, -0.15,  1.42,  0.025, 1.35)$ and variances $\sigma_{1:6}=(0.05, 0.05, 0.05, 0.05, 0.05, 0.1)$, ensuring that the tube is in the image. As a simplification of the task, we excluded the last rotational wrist joint of the robot arm. Because of the adynamic nature of this task and the necessity to use position control mode it is sufficient to use the latent representation of the current image versus a stack of images as in simulation. Larger movements of the cylinder appear as blur in the images. Each episode consists of 20 time steps and a sparse reward is used: For safety reasons, if the end-effector left the designated workspace area, the episode ended and a reward of $-1$ is assigned. When the cylinder is inserted into the tube, the extent of insertion is transformed into a reward from $[0, 1.0]$ and an episode stops if a reward of $0.9$ or higher is assigned. The state of insertion is measured with a laser-based time-of-flight sensor (VL6180). The reward for all other possible states is zero. Five experiments were conducted on the robot: DDPG with a value function as critic and Ornstein-Uhlenbeck exploration, DDPG with exploration using trajectory optimization and a varying planning horizon (1, 3, 5 and 15 steps). We use a reduced planning horizon in this task due to the low number of time steps per episode. The comparison between Ornstein-Uhlenbeck exploration and optimized exploration with a horizon of three is shown in Fig. [9](#Fig::baxter::basic){reference-type="ref" reference="Fig::baxter::basic"}. Every episode which ends with a negative cumulative reward violated the workspace boundaries and episodes reaching a reward of 0.9 or more were successful insertions. Table [1](#Tabel::Horizons){reference-type="ref" reference="Tabel::Horizons"} shows the comparison between exploration with Ornstein-Uhlenbeck noise and using planning horizons of different lengths in terms of successful insertions. Each experiment was repeated five times and the cumulative reward for each episode is used to compute the mean shown in Figure [9](#Fig::baxter::basic){reference-type="ref" reference="Fig::baxter::basic"}. For better interpretability, the figures show, in bold lines, additionally a smoothed version of the mean where a Savitzky-Golay filter was applied with a window size of 21 and polynomials of order one. The autoencoder network as well as the dynamics network were trained with a demonstration dataset of 50 trajectories. Of these, 19 were positive demonstrations, in which the cylinder was successfully inserted. At the beginning of each training process, 5 of these 19 trajectories were added to the replay buffer to ensure convergence of the training process due to the difficulty of the task caused by using sparse reward.

# Discussion

We start with a discussion of the results from the simulated bipedal cheetah task which uses a dense reward function: The first insight is that both actors seem to perform equally well after 20 episodes, with the actor trained with optimized noise outperforming classical DDPG throughout the first 20 episodes (Fig. [5](#Fig::cheetah::basic){reference-type="ref" reference="Fig::cheetah::basic"} (a)). However, during training the optimized exploration does not only perform better than exploration with an Ornstein-Uhlenbeck process (Fig. [5](#Fig::cheetah::basic){reference-type="ref" reference="Fig::cheetah::basic"} (b)) but also performs better than the actions produced by both actors during test time (Fig. [5](#Fig::cheetah::basic){reference-type="ref" reference="Fig::cheetah::basic"} (a)).

We found that using a critic network modelling the Q-function (Fig. [5](#Fig::cheetah::basic){reference-type="ref" reference="Fig::cheetah::basic"} (b)) outperformed the formulation of DDPG using a value network when using optimized exploration (Fig. [5](#Fig::cheetah::basic){reference-type="ref" reference="Fig::cheetah::basic"} (d)), while DDPG with Ornstein-Uhlenbeck noise performs slightly better with a Value network (Fig. [5](#Fig::cheetah::basic){reference-type="ref" reference="Fig::cheetah::basic"} (a,d)). One could argue, that the effects of using optimized noise could vanish when increasing the number of trainings per episode, giving DDPG more time to find an optimal actor given the current training set. Following this line of thought we increased the number of training iterations per episode three times to 3000 (Fig. [6](#Fig::cheetah:3000){reference-type="ref" reference="Fig::cheetah:3000"}). The evaluation shows that while DDPG with OU noise improves in the later stages of the learning process, the trajectory optimization uncovers valuable training experience now much faster early on. This strongly indicates that the data distribution generated by the exploration strategy has an impact on the performance of DDPG. Evaluating the step-lengths we could find that trajectory optimization improved up to a planning horizon of 20 steps, although we opted for our experiments with a conservative planning horizon of 10 steps to reduce the overall training time. The evaluation of the three introduced objective functions show that the summation of Q-values along the planning trajectory yields better performance in the early training stages, up to episode 25, for the dense reward task (Fig. [8](#Fig::objectives){reference-type="ref" reference="Fig::objectives"}). This is an interesting result given that many other trajectory optimization approaches use a Bellman-inspired sum of weighted rewards [@nagabandi2018neural; @chua2018deep]. It is also worth to notice that the Q-Value is the more suitable objective function for optimizing actions in the presented real-world insertion task due to the reward function being zero for the majority of time steps.

The results showing the learning progress on the insertion task in the real world draw a clearer picture of the benefit of exploration through optimization (Fig. [9](#Fig::baxter::basic){reference-type="ref" reference="Fig::baxter::basic"}, Table [1](#Tabel::Horizons){reference-type="ref" reference="Tabel::Horizons"}). Generally, after roughly 50 training episodes, the networks trained with optimized exploration outperformed DDPG with OU and also achieved higher rewards in later stages of the learning process (Fig. [9](#Fig::baxter::basic){reference-type="ref" reference="Fig::baxter::basic"}). An evaluation of the length of the planning horizon shows, as expected, that longer planning horizons lead to a decreases performance (Table [1](#Tabel::Horizons){reference-type="ref" reference="Tabel::Horizons"}). This is very likely due to the accumulating error of predicted future states from the dynamics network. However, even with longer planning horizons the presented approach outperformed exploration using OU noise.

# Conclusion

This work investigated the possibility of combining an actor-critic reinforcement learning method with a model-based trajectory optimization method for exploration. By using trajectory optimization only to gain new experience, the ability of DDPG to learn an optimal policy is not affected and we can furthermore make use of DDPG's off-policy training ability. We were able to show that by using this strategy, a performance gain can be achieved, especially in the presented real world insertion task learned from images. It is worth noting that this performance gain can be mainly attributed to the change in exploration strategy since a fixed image embedding was used, reducing the possibility of performance differences caused by using different image embeddings. This work only considered using reward, Q-Value or value functions as objective functions for optimizing the latent trajectory. In future work we plan to investigate the possibility of using additional cost terms, eg. safety and state-novelty. Furthermore, another natural next step would be to use probabilistic dynamics networks and advanced trajectory optimization algorithms to evaluate their impact on deep reinforcement learning algorithms when used for exploration in this setup.

[^1]: $^{1}$Interactive Robotics Lab, Arizona State University, Tempe, AZ, USA\
    $\lbrace \text{ksluck},~\text{sstepput},~\text{hbenamor}\rbrace$` ät asu.edu`

[^2]: $^{2}$Google DeepMind, London, UK.\
    $\lbrace \text{vec},~\text{jscholz} \rbrace$` ät google.com`

[^3]: A video of the experiment can be found here: <https://youtu.be/rfZcUWnut5I>
