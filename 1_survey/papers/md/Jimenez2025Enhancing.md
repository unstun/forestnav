---
citation_key: Jimenez2025Enhancing
arxiv_id: 2501.06639
arxiv_url: "https://arxiv.org/abs/2501.06639"
title: "Enhancing Path Planning Performance through Image Representation Learning of High-Dimensional Configuration Spaces"
authors_short: "Jorge Ocampo Jimenez et al."
year: 2025
direction_tag: G_subgoal_optimization
source: mineru-vlm
converter: mineru-open-api
model: vlm
converted_at: 2026-06-25T09:17:14Z
origin: ai+web
reviewed: false
---

# Enhancing Path Planning Performance through Image Representation Learning of High-Dimensional Configuration Spaces

Jorge Ocampo Jimenez and Wael Suleiman

Abstract—This paper presents a novel method for accelerating path-planning tasks in unknown scenes with obstacles by utilizing Wasserstein Generative Adversarial Networks (WGANs) with Gradient Penalty (GP) to approximate the distribution of waypoints for a collision-free path using the Rapidly-exploring Random Tree algorithm. Our approach involves conditioning the WGAN-GP with a forward diffusion process in a continuous latent space to handle multimodal datasets effectively. We also propose encoding the waypoints of a collision-free path as a matrix, where the multidimensional ordering of the waypoints is naturally preserved. This method not only improves model learning but also enhances training convergence. Furthermore, we propose a method to assess whether the trained model fails to accurately capture the true waypoints. In such cases, we revert to uniform sampling to ensure the algorithm’s probabilistic completeness; a process that traditionally involves manually determining an optimal ratio for each scenario in other machine learning-based methods. Our experiments demonstrate promising results in accelerating path-planning tasks under critical time constraints. The source code is openly available at https://bitbucket.org/joro3001/imagewgangpplanning/src/master/.

Index Terms—Sampling-based path planning, Generative Adversarial Networks, Image-conditioned generative model, Diffusion.

## I. INTRODUCTION

Machine learning techniques, such as neural network generative models like Variational Autoencoders (VAEs) [1] and Generative Adversarial Networks (GANs) [2], have been used to improve the efficiency of random sampling algorithms. These models bias the sample distribution towards collisionfree states, conditioned on the robot’s current workspace configuration. While previous research has successfully applied GANs [2], [3], [4] to tasks such as generating inverse and forward kinematics, there has been limited exploration of using GANs with gradient penalties in high-dimensional problems. This is largely due to the increased complexity and computational cost associated with such approaches.

Moreover, it has been demonstrated that Wasserstein GANs (WGANs) are highly sensitive to hyperparameter tuning. This sensitivity arises because the transport cost between the image and waypoints of a collision-free path derived from a training dataset is often represented by discontinuous functions [5].

Another challenge in employing machine learning algorithms for waypoint sampling is the inherent inaccuracy of the learned model. Since the model’s predictions are not perfectly accurate, the sampling process uses a predefined ratio to balance between using the uniform distribution and the learned distribution to ensure probabilistic completeness [6]. However, determining the optimal ratio requires careful tuning, which can pose additional difficulties.

## II. PROPOSED METHOD

To address challenges such as unstable training processes, extended training times, and the potential for unexpected outcomes when encountering unseen conditions during path planning, we propose to:

• Select a forward diffusion process from an SDE model to train the input condition of the workspace. Unlike using an encoder from a VAE, the SDE approach does not require joint training with the generative model, simplifying the training process while maintaining effective performance.

• Reduce the number of images in the input of the trained network by using affinity propagation. This process reduces the number of samples per epoch during training by representing the whole waypoint set as a matrix.

• Exploit in the cases of bounded configuration spaces, the fact that the samples clustered by the affinity points are bounded too; thus, we could reject samples too far from their means in the bounded sets; removing the need of finding an optimal sampling ratio between the uniform distribution and the learned one.

Our model is trained using forward kinematics simulations with the Baxter manipulator robot. We create multiple scenarios by placing random human models around the robot and using RGB-D representations of the robot’s obstacles to train our model to estimate the waypoints of a collision-free path.

We evaluate the performance of our model using metrics such as planning time, path length, and success rate. This evaluation enables us to assess the impact of changes in the conditions and encoding of configuration states on the model’s ability to generate new waypoints. To establish a baseline for comparison, we employed paths generated by RRT and RRT\*. Our experiments demonstrated that our model is capable of finding shorter and faster paths in time-constrained scenarios.

## III. ORIGINAL CONTRIBUTIONS

This paper offers several novel contributions, including:

1) Introducing a new architecture that enhances WGAN-GP training by embedding the condition as an additional channel in the RGB-D representation of the working space (WS).

2) Reducing the number of queries by generating all the waypoints in one query.

3) Introducing a new methodology that discards samples from the trained model during deployment of the planner when a probability threshold is met in bounded configuration spaces, thus preserving probabilistic completeness.

4) Enhancing path planning performance in terms of time, success rate, and path length compared to algorithms like RRT and RRT\* under time constraints.

Compared to other similar works where the planner’s sampling is biased, our method offers several advantages, including:

• By utilizing both GANs and forward diffusion, our model can handle noisy or previously untrained scenarios while generating high-quality WGAN samples.

• Our image-to-image model has the potential to extend to the prediction of higher-dimensional waypoints for robotic tasks using image processing algorithms, thereby reducing the number of connections between networks by employing pattern-based deep neural network models.

• Unlike other machine-learning methods [1], [6] that depend on finding an appropriate ratio between uniform or biased distributions for RRT-based planners, our approach is established an error bound to reject the sampling of the trained model.

## IV. RELATED WORK

The use of learning by demonstration has proven to be an effective approach in numerous studies aimed at enhancing the performance of sampling-based random planners [7]. A common technique involves employing an auto-generative model that learns a mapping between a robot’s configuration space (C) and the image-based scenario, using a reduced number of samples from the full distribution. In recent years, deep neural network (DNN) models have gained significant traction in this field due to their ability to process large volumes of input data, such as image or point cloud representations of the robot’s environment, and to generalize across a wide range of examples, including potential robot configurations and the number and location of obstacles in the workspace.

While DNNs allow conditioning in high-dimensional spaces; they are trained as unimodal models, which fail to capture the inherent diversity and multiple modes in the data. In contrast, Deep Generative models have demonstrated their ability of capturing high-dimensional multimodal data in contexts like text and image generation [8].

Generative models are widely used in the context of Rapidly-exploring Random Trees-based algorithms [9] for two main purposes: to introduce a bias in the sampling process or to serve as a heuristic for the cost function. These models guide the algorithm towards lower-cost paths by taking into account the specific conditions of the scenario.

The application of neural networks for learning the sampling distributions to bias-sampled based planners was first introduced in [6]. The study utilized a conditional variational autoencoder to identify areas in C that held promise based on the initial and goal states, as well as the obstacles present in the scenario. This enabled the sampler of random path algorithms to be biased, resulting in more efficient path planning.

In another study [1], an encoder was used to capture environmental information, with the sampler conditioned on raw sensor data or voxelized output embedded in the latent space. The encoded information was then utilized by a planning network, in conjunction with the current and goal states, to generate the next state. This model can bias the sampler of RRT\* [10] and has been tested on high-dimensional configuration spaces.

The research presented in [3] utilizes 2D working spaces as inputs for a conditional GAN. The GAN is conditioned on the RGB representation of both the initial and final points of the path, as well as the map of the working space. The generator is trained with two discriminators: one for the obstacle map and another for the initial and final goal states represented in the working space. The resulting algorithm achieves an impressive success rate of approximately 90% in generating connected configurations.

The study presented in [11] utilizes inverse reinforcement learning to determine the weights of the RRT\* cost function based on the expected behavior of a robot in environments previously occupied by humans. This approach helps guide the planner towards the desired path. However, it may be less suitable for dynamic environments where the weights cannot be adjusted without compromising the asymptotic optimality of the algorithm.

The authors of [4] present an approach where GANs are used to bias an RRT-based planner by incorporating Encoders and Decoders directly as hidden layers in the generator. The initial state, map, and latent vector are provided as inputs to the encoder, while the decoders output a 2D representation of the path. The generator thus produces the path as an output image, treating the task as an image-to-image model. Although the authors do not provide specific information on running times, it is reported that the algorithm requires fewer iterations to achieve a lower cost compared to RRT\*.

The research presented in [2] explores the use of a GAN to learn the inverse kinematics of high-dimensional robots. The model is conditioned on the target working space position of the end effectors, enabling the generation of samples in highdimensional Cs, which was previously infeasible. However, it is important to note that the conditioning is not directly based on sensor data or the current state of the scenario.

Lately, significant advances in generative neural network models have been made, such as the diffusion generation approach in path planning [12], their application in random sampling-based planners remains limited, particularly in scenarios with strict time constraints for obtaining a collisionfree path. A common challenge with diffusion-based methods is their computational cost; repeatedly sampling from the diffusion generator during the backward pass can be timeconsuming. For a more comprehensive discussion on the use of generative DNN models, we refer to the work of [8].

## V. PROBLEM FORMULATION

The objective of this research is to develop a method for approximating waypoints of a collision-free path by leveraging information from its obstacles, represented as an imagescenario. The ultimate goal is to enhance the performance of a path planner. This is achieved by training a model to learn the mapping from the image-scenario to ${ \mathcal { C } } ,$ which allows for more efficient sampling and accelerates the planning process. The proposed method has the potential to significantly improve robotic systems’ performance by reducing the computational cost of planning while still producing low cost paths.

![](Jimenez2025Enhancing_figs/86cd107c2c5c0432f5314115284f4fc64e800af2702ee646d72d7f110d33edb3.jpg)  
Fig. 1: Proposed architecture to learn the waypoints of a collision-free path from the robot’s WS.

Mathematically speaking, a path planning problem is defined by a configuration space $\mathcal { C } = ~ [ 0 , 1 ] ^ { d }$ with dimension $d \in \mathbb { N } , d \geq 2 ; \mathrm { ~ a ~ } \mathcal { C } _ { o b s }$ that is defined as the set of C that corresponds to the collision states; and a free configuration space $\mathcal { C } _ { f r e e } = \mathcal { C } \backslash \mathcal { C } _ { o b s }$ , with initial configuration $q _ { 0 } \in \mathcal { X } _ { f r e e }$ and a set of goal configuration $\mathcal { C } _ { g o a l } \subset \mathcal { C } _ { f r e e } .$ A path is a continuous function $s : [ 0 , 1 ] \to \bar { \mathbb { R } ^ { d } }$ , and it is collision-free if $s ( \tau ) \in \mathcal { C } _ { f r e e }$ for all $\tau \in \ [ 0 , 1 ]$ and feasible when it is collision-free and $s ( 0 ) = q _ { 0 }$ and $s ( 1 ) \in \mathcal { C } _ { g o a l }$

Finding a feasible path in the C of a robot is known to be PSPACE-complete [13], which makes it computationally intractable for most practical applications. Consequently, researchers have developed sampling-based motion planning algorithms to address this challenge in high-dimensional Cs. These algorithms work by randomly sampling configurations and connecting them to form a path to the goal states. Completeness, or finding a solution if one exists, requires drawing a sufficient number of uniformly distributed random samples. Asymptotic optimality, where the path cost converges to the optimal solution, can be achieved by systematically connecting the nodes of the search tree [6].

To improve the efficiency of sampling-based motion planners, researchers have proposed various methods to bias the path towards the goal. One such method involves learning a probability distribution over the waypoints in s(·) based on the robot’s scenario, which guides the sampling process to explore regions of C more likely to lead to the goal. This approach reduces the time spent exploring regions of C that are less likely to yield a viable path, thereby accelerating the planning process. As a result, it has the potential to substantially enhance the efficiency of sampling-based motion planning algorithms, making them more practical for realworld applications.

## VI. METHODOLOGY

We propose a novel approach for accelerating samplingbased motion planning algorithms by generating waypoints of a path in $\mathcal { C } _ { f r e e }$ with additional properties such as feasibility and connectivity with the current path. Our approach utilizes a WGAN to sample from a learned distribution over $\mathcal { C } _ { f r e e } ,$ which biases the sampling process towards regions of C more likely to yield waypoints. Specifically, we employ a WGAN-GP to generate high-quality collision-free configurations without the need to determine a suitable clipping interval. This method replaces the uniform distribution typically used for sampling C and results in faster query times. The proposed architecture is illustrated in Fig. 1. In this architecture, we simplify the original number of waypoints-states by learning the centroid of clusters when the number of waypoints is higher than the matrix representation; then, the clusters follow an already multidimensional sort given the order of the waypoints in a path; this increases the chances of having smooth gradients during training. New waypoint clusters are generated by applying positional encoding to the initial and final states of the desired path to an RGB-D image representation of the current WS of the robot. The RGB-D is then diffused through a continuous stochastic process, which serves as the latent space of a generative neural network capable of predicting the sorted multidimensional waypoints. To recover any potential missing states of a collision-free path within these clusters, sampling is performed around the predicted centroids.

## A. Generative Model

Deep generative models are based on estimating the probability distribution of a dataset X where the probability distribution $P _ { X }$ is unknown. In particular, the assumption is made that the unknown distribution $P _ { X }$ can be approximated by a parametric distribution $P _ { \omega } ;$ ; where $\omega \in \Omega$ with Ω defined as a parametric space. $P _ { \omega }$ should be marginalized over a latent variable Z f

$$
p _ {\omega} (\pmb {x}) = \int_ {Z} p (\pmb {x} | \pmb {z}) p (\pmb {z}) d \pmb {z}\tag{1}
$$

There are mainly two well-known methodologies that utilize such approach for deep generative models, one is GAN [14], where the density $p _ { \omega }$ does not have an explicit analytical form. Instead, a random variable Z is sampled from a specified random distribution, and a deterministic function

$G _ { \omega } : Z \to X$ aims to approximate the target distribution $P _ { X }$ This is achieved by optimizing the Jensen-Shannon divergence [15]. The second approach, Variational Auto-Encoders (VAE) requires learning an approximation of the posterior distribution $P _ { Z | X }$ and the marginal distribution $P _ { X }$ . The distribution $q _ { \omega } ( z | x ) = \mathcal { N } ( \mu _ { \omega } ( x ) , \Sigma _ { \omega } ( x ) )$ is used to approximate the conditional distribution with the Kullback–Leibler divergence loss between marginal distributions. While the VAE and GAN have been studied thoroughly in the literature, empirically GAN has been found to generate better quality results compared with the VAE’s approach.

In order to improve the training stability of GAN models, a method was proposed in [16] which employs the Earth-Mover distance to measure the similarity between distributions, called WGAN. This approach offers the benefit of providing smooth measures even in scenarios where the distributions are completely overlapping or disjoint.

Initially, in [16], weight clipping was proposed as a method to stabilize the training of a WGAN model. However, choosing the right clipping parameters can be challenging, and setting them to values that are too large or too small can result in slow convergence or vanishing gradients. To address this issue, the authors in [17] introduced a gradient penalty approach that penalizes the model gradients if the Lipschitz constraint is violated. Specifically, if the critic function $f$ has a gradient norm greater than 1, a penalty term is added to the loss function to encourage the model to stay within the Lipschitz constraint as follows:

$$
\begin{array}{c} L = \underbrace {\mathbb {E} _ {x \sim p _ {r} (x)} [ f _ {\omega} (\boldsymbol {x}) ] - \mathbb {E} _ {z \sim p _ {r} (z)} [ f _ {\omega} (g _ {\rho} (\boldsymbol {z})) ]} _ {\text { Original   critic   loss }} \\ + \underbrace {\lambda \mathbb {E} _ {\hat {x} \sim p _ {\hat {x}}} [ (\| \nabla_ {\hat {x}} f _ {\omega} (\hat {\boldsymbol {x}}) \| _ {2} - 1) ^ {2} ]} _ {\text { Gradient   penalty }} \end{array}\tag{2}
$$

where $p _ { r } ( x )$ and $p _ { r } ( z )$ represent respectively the distributions over the real multidimensional data x and the noise input vector z. λ is a penalty coefficient to weight the gradient penalty, xˆ sampled from the generator $g _ { \rho } , \rho \in \Omega$ and x within a t uniformly sampled between 0 and 1.

However, from the Optimal Transport theory [5]; the Wasserstein distance is the transport ground cost $c ( { \pmb x } , { \pmb y } ) =$ $\| \ b { x } - \ b { y } \|$ and it can be shown that GANs are sensitive to hyper-parameters and difficult to train given that the transport map is discontinuous and DNNs can represent only continuous maps. A proposed solution to this problem is to compute the optimal transport map between a continuous set and a latent distribution, as outlined in [18].

In our case, we propose to use a forward diffusion process as input to train the WGAN; defined as follows:

$$
\pmb {x} _ {t} = \sqrt {\alpha_ {t}} \pmb {x} _ {t - 1} + \sqrt {(1 - \alpha_ {t})} \pmb {\epsilon} _ {t - 1}\tag{3}
$$

where $\epsilon _ { t - 1 } , \epsilon _ { t - 2 } , . . . \sim \mathcal { N } ( \mathbf { 0 } , I ) , \alpha _ { t } \in \mathbb { R }$ , this process creates a continuous map between the training input data and the latent distribution. Using latent distributions to train GANs is not a new concept, other works in the field of computer vision have used VAEs to represent the latent distribution of GANs with the objective of encoding the conditioning of the model;

however this methodology requires training both VAE and WGAN at the same time, which could be challenging to find the perfect ratio between the approximation of the continuous latent function and the desired output. The SDE approach adds the benefit of establishing a continuous map from the input space to the latent space without the need to train the encoder and the GAN at the same time and without the search of the optimal radius between encoding and reconstruction. Also, our approach has the advantage that the latent variable $x _ { t }$ can be estimated in a single step using the reparameterization trick by a simple function in Eq. (4), with $\hat { \beta } _ { t } \in \mathbb { R } \colon$

$$
\pmb {x} _ {t} = \sqrt {\hat {\beta} _ {t}} \pmb {x} _ {0} + \sqrt {(1 - \hat {\beta}) _ {t}} \pmb {\epsilon} _ {t}\tag{4}
$$

This method does not require training and querying an additional DNN, which reduces sampling time. Additionally, this continuous function accounts for cases where previously unseen samples from the input space are covered by the path followed by a new input $\scriptstyle { \mathbf { { \mathit { x } } } } _ { 0 }$ at time t.

## B. Clustering

We aim to simplify the training of the model given the number of data samples. Typically, other approaches that use DNNs involve tuples of image inputs and vector outputs to represent different samples from $\mathcal { C } _ { f r e e }$ used to train the approximation. However, approximating each image/sample of $\mathcal { C } _ { f r e e }$ in a large dataset requires processing a significant number of images per batch, which can slow down performance when the dataset is relatively large.

In our approach, we propose to estimate the entire list of waypoints in a single step. However, this is impractical due to the infinite number of samples in a continuous $\mathcal { C } _ { f r e e }$ . Instead, we aim to learn parameters that can generate an approximation of the total number of waypoints. One possible method is to use clustering techniques, which only require learning the parameters of the distribution to reconstruct the original space.

However, methods like Gaussian Mixture Models (GMMs) pose challenges during training. The random selection of initial centroids and the problem of solving the approximation using Expectation-Maximization often lead to different models even with the same parameters. This variability in cluster assignment means that the DNN may struggle to find a continuous map. In addition; when GMMs parameters are learned in the context of sampling based path planners; it can be challenging to condition the model [11] [7].

As an alternative, we propose using affinity propagation [19]. Unlike GMMs, which require specifying the number of clusters, affinity propagation identifies exemplars directly from the dataset. It does not require defining the number of clusters in advance.

Affinity propagation operates by exchanging two types of messages between data points: the responsibility function, which measures how well a proposed data point represents its neighbors, and the availability function, which accumulates the responsibilities from other data points. This iterative process continues until convergence or a fixed number of iterations is reached. This method reduces the variance in cluster locations derived from the training dataset of waypoints in $\mathcal { C } _ { f r e e }$ , as the exemplars are estimated using the entire dataset without relying on random sampling to form clusters. To approximate the set of waypoints, we use each exemplar as the mean of a Gaussian distribution and generate points around each exemplar with an initial standard deviation $\sigma _ { 0 } = 0$ . If we are unable to capture values in $\mathcal { C } _ { f r e e : }$ , we increase the standard deviation by following a vector of values $\sigma = \{ \sigma _ { 0 } , \ldots , \sigma _ { k } \} ; k \in$ $\mathbb { N } ; \sigma _ { k } ~ > ~ \sigma _ { k - 1 } ; \sigma ~ \in ~ \mathbb { R } ^ { + }$ , instead of directly obtaining the sampled $\mathcal { C } _ { f r e e }$ configurations from $f _ { \omega }$

While the exemplars are not necessarily the means of Gaussian mixtures, we know in advance that their neighborhoods contain the original configurations in $\mathcal { C } _ { f r e e }$ . Furthermore, there exists a $\delta > 0$ such that the ball $B _ { \delta } ( \bar { q } )$ , centered at the exemplar q¯, includes its affinity points. The goal is to bias the sampler as close as possible to the original $\mathcal { C } _ { f r e e } ,$ thereby reducing the number of queries in $\mathcal { C } _ { o b s }$ . This process is illustrated in Fig. 2.

![](Jimenez2025Enhancing_figs/cba5be605e8108632a01c8e0a9a5ce0c2eb04539fde2cc80d8bfa9967534b772.jpg)  
(a)

![](Jimenez2025Enhancing_figs/b1c6d3f3e73458506ad2c48bccc8237c30fa6ded96b239d166eeef020dbadaf4.jpg)  
(b)  
Fig. 2: Projection of the first two joints of the Baxter manipulator’s arm and its affinity points q¯. The circle represents the standard deviation σ. A fixed σ could miss the original points around the exemplars, as shown in Fig. 2a. However, if we increase $\sigma ,$ we eventually also increase the probability of sampling the missing $\mathcal { C } _ { f r e e }$ -configurations, as shown in Fig. 2b

## C. Image Representation and Conditioning

Following the universal approximation theorem, DNNs are able to approximate any continuous function given an arbitrary number of activation functions. Thus, it is to our advantage to represent the training data problem as a continuous function. In our case, given that we have $C _ { f r e e } \subseteq \mathbb { R } ^ { n } , n \geq 2$ , a nonconstrained approximation of $C _ { f r e e }$ represented as an image will rarely be continuous pixel-wise. However, the waypoints in $C _ { f r e e }$ that are part of a constrained path have a hierarchical ordering. Particularly, in the case of the shortest path; the affinity points of the set of waypoints can be represented an image with an almost continuous gradient; as shown in Fig. 3.

The matrix representation effectively reduces the paired training data between the RGB-D and each of the waypoints in $\mathcal { C } _ { f r e e }$ . Thus, we transform the problem to an image-to-image function, where each image represents the whole path in $\mathcal { C } _ { f r e e } .$ This process is exemplified in Fig. 4.

Next, to overcome the challenges of the adversarial training of WGAN, we used the forward diffusion process on the input RGB-D images as explained previously.

![](Jimenez2025Enhancing_figs/d0e8deaa3ddfdd46ac14f4b39e9015ff14dc11a64b31b4ab591daa4ebaeff614.jpg)  
Fig. 3: In the case of a constrained path, such as the shortest path, there is already an inherent ordering relationship between the configurations. In this example, we observe an almost continuous gradient between the different states in the matrix representation of a collision-free path, each entry of the waypoints are scaled.

![](Jimenez2025Enhancing_figs/79f05865cc93c425245d776df0f347663f7004f757e3b0353fec8d6cd76c9803.jpg)  
(b) Proposed representation dataset for training waypoints in $\mathcal { C } _ { f r e e }$ generative models. The cardinality of the input working spaces is lower than the conventional representation  
Fig. 4: Conventional and proposed datasets for waypoints in $\mathcal { C } _ { f r e e }$ generative model training. In Fig. 4a, we show how the dataset during training would repeat the same working space RGB-D for every waypoint sampled from $\mathcal { C } _ { f r e e } ;$ thus requiring to increase the number of samples to be processed in the same epoch. In Fig. 4b, the representation only requires a paired matrix of centroids to represent all the waypoints, which decreases the total number of samples per epoch and decreases the time of learning.

Using a forward diffusion process as a latent variable for a GAN in the context of sampling-based planners is not a novel concept. In the work of [20], a WGAN is conditioned by the forward diffusion process of the RGB-D workspace (WS); however, the path conditioning can only be represented as a mask of the RGB-D, which limits the constraints that can be effectively captured. Similarly, the work of [21] uses the forward diffusion process as a latent variable for the GAN’s generator, but it requires a more structured approach to train the model in 3D workspaces. Other approaches necessitate discretizing the $\mathcal { C } _ { f r e e }$ of the robot [22], which compromises the precision of the model.

```txt
0 2 4 6 8 10 12
Sequence index 0 2 4 6 8 10 12
Value encoding
```  
Fig. 5: Extra channel to add conditioning to the generator. For instance, when training the model to generate waypoints for the shortest path, we include the start and end states of the path in this extra channel; the condition consists of 14 entries, where 7 corresponding to the start state and 7 to the end state. Each row represents different encoding.

To be able to represent diverse conditions outside of a mask of the original RGB-D; we also added an extra channel to represent the start state and the goal state of the path, which we refer to as RGB-D+. Given that the start and goal states can be represented by a vector of 14 entries, we propose to fill the rest of the condition channel with the positional encoding proposed in [23], which has been shown to improve gradient propagation [24]. This representation gives us the chance of not only represent information encoded as an image in the WS like the one presented in [20]; any other numerical information can be represented as such given that it can be fit in the same dimension as the resolution of the input image.

Our proposed representation helps us to encode the information directly into the image input $\mathbf { { \boldsymbol { \psi } } } _ { 0 }$ , which would be used as the latent for $\mathbf { \nabla } _ { \mathbf { \boldsymbol { y } } _ { t } . }$ This change will help reduce the complexity of the DNN, given that the condition is already inside the $\mathrm { R G B - D + }$ , and we can exploit image processing techniques like convolutions to avoid the need for fully connected layers between all entries of the condition’s vector. An example of the condition channel is presented in Fig. 5.

## D. Planner

To guide the path towards the desired region in $\mathcal { C } _ { f r e e } ,$ we utilize a technique inspired by [25]; where a 2D $\mathcal { C }$ is represented as an image for the DNN to be learned by convolution layers. Our approach involves using a DNN’s model generator trained by an adversarial loss function as a sampler for the RRT path planning algorithm. However, we made a modification in our implementation to reject the sampling from the training model given the probability of the data around an estimated waypoint being in the complement of $\mathcal { C } _ { f r e e } .$

One advantage of our proposal compared with other approaches in the field of path planning using random trees and DNNs is that we can estimate when our approximation has most likely failed. Given that the probability of selecting a sample on the tail of the Gaussian distributions of each exemplar decays exponentially, we have an upper bound to our trained model to know when the generator $f _ { \omega }$ most likely failed to approximate a bounded $\mathcal { C } _ { f r e e } .$

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 1: RRT with WGAN-GP cluster bias

Data:  $q_{init}, q_{goal}, \epsilon = [\epsilon_0, \epsilon_1, ..., \epsilon_t], t \in N, \epsilon_j \in \mathcal{N}(0, I)$ ,  $y_0 \in RGB-D + : [0, 1]^{5 \times 32 \times 32}$ ,

 $\sigma = [\sigma_0, \sigma_1, ..., \sigma_k], k \in N, \sigma_i \in R^+$  and

 $\sigma_i &gt; \sigma_{i-1}$  is an increasing amount of perturbation for the exemplars  $\bar{q}$ , generator

 $f_\omega(\cdot)$ . m is the number of samples taken from each  $\mathcal{N}(\bar{q}, \sigma_i I)$ 

Result: G

1  $s \leftarrow 0;$ 

2  $V \leftarrow q_{init}, E \leftarrow \emptyset;$ 

3  $y_t \leftarrow \sqrt{\hat{\beta}_t} y_0 + \sqrt{(1 - \hat{\beta}_t)} \epsilon_t;$ 

4  $\bar{q} \leftarrow f_\omega(y_t);$ 

5 for  $h = 1, ..., l$  do

6 if h mod m == 0 then

7  $s \leftarrow s + 1$ 

8 if s &lt;= k then

9 if  $\mathcal{N}(\bar{q}, \sigma_s I) \cap C_{free} \neq \emptyset$  then

10  $q_{rand} \leftarrow SampleFree(\mathcal{N}(\bar{q}, \sigma_s I));$ 

11 else

12  $q_{rand} \leftarrow SampleFree(\mathcal{U}(\mathcal{C}));$ 

13 else

14  $q_{rand} \leftarrow SampleFree(\mathcal{U}(\mathcal{C}));$ 

15  $q_{nearest} \leftarrow Nearest(G = (V, E), q_{rand});$ 

16  $q_{new} \leftarrow Steer(q_{nearest}, q_{rand});$ 

17 if ObstacleFree( $q_{nearest}, q_{new}$ ) then

18  $V \leftarrow V \cup \{q_{new}\};$ 

19  $E \leftarrow E \cup \{(q_{nearest}, q_{new})\};$ 

20 if  $q_{new} == q_{goal}$  then

21 return G = (V, E);

22 return G = (V, E);
</div>

Given that we only have an approximation of the affinity points and lack information about their neighboring waypoints, we aim to recover some of the missing waypoints by sampling around q¯. Although we cannot guarantee that the process will recover all the original waypoints by sampling from $\mathcal { N } ( \overline { { \pmb { q } } } , \sigma _ { i } \pmb { I } )$ , we increase the value of $\sigma _ { i }$ with the goal of identifying as many missing neighboring waypoints as possible within an unknown neighborhood.

We know that $P ( | q - \bar { q } _ { i } | > \sigma ) \sim 0 . 3 1 7 3$ and that sampling from $\mathcal { N } ( \bar { \pmb q } , \sigma _ { i } { \pmb I } ) \cap \mathcal { C } _ { f r e e } \neq \emptyset$ should hold for sufficiently large m, provided that the affinity points were well-approximated during training. If this condition does not hold, it is likely that the trained model failed to capture the true waypoints for $\sigma _ { i }$ with sufficiently large $m .$

By increasing $\sigma _ { i }$ until the boundary of the configuration space is reached, we can evaluate whether the learned model is inadequate for generating points in $\mathcal { C } _ { f r e e } .$ . If this condition is met, we switch to sampling from the uniform distribution. This proves that our algorithm is probabilistic complete following [26], when the total number of samples $l \in \mathbb N$ goes to infinity. The proposed algorithm is described in Algorithm 1. Where U is the uniform distribution, and $S a m p l e F r e e ( \cdot )$ is a function that samples the input distribution until it finds a configuration in $\mathcal { C } _ { f r e e }$

## VII. EXPERIMENTAL RESULTS

All the models are trained on a system with 2 x Intel Gold 6148 Skylake, 16 GB of RAM and 2 x Nvidia V100SXM2. For deployment, we use Ubuntu 20.04 running on a 3.60 GHz × 8 Intel Core i9-9900KF processor, 16GB RAM on Nvidia RTX 2070.

We propose a set of experiments to examine the effectiveness of learning the waypoints of a constrained path. These waypoints are used to bias the sampling of $C _ { f r e e }$ states to find a collision-free path, as described in Section VI. The constrained approximation illustrates how well the conditioning of $\mathcal { C } _ { f r e e }$ is encoded in the RGB-D+ input and also provides insight into how the implementation might work in real-world problems.

We use a combination of 100 ${ \sf W S s } / { \mathcal { C } } _ { f r e e } { \bf s }$ with 100 different starting and goal configurations. All WSs and waypoints are derived from a simulated Baxter’s 7-DOF right arm. All input images of the scenarios were resized to $3 2 \texttt { X } 3 2$ pixels. We utilized the PyTorch Lightning framework with Adam optimizer parameters derived from [17] for training. Our experimental hyperparameters consisted of a learning rate of $4 \mathrm { e } { - } 5 ,$ , a batch size of 128, a regularization coefficient λ of 10 for the gradient penalty, and $n _ { \mathrm { c r i t i c } } = 5$ training iterations per generator iteration. All Cs are scaled between [0,1] in their matrix encoding. Our code is available on Bitbucket<sup>1</sup>.

We employ a simulated RealSense RGB-D sensor to represent the conditioning factor in our experiment. This image captures the obstacles’ representation within the robot’s operational space. In cases of constrained paths by path length, we add the initial and final states of the shortest path as an extra channel. To streamline the experimentation process, we opted for a human model spawning in a random position and orientation within Baxter’s working space. The initial and final configurations of the arm are chosen randomly.

For the test, we train the generator using waypoints of the shortest path between random goal and start configurations. The shortest path depends on the initial and goal configurations; thus, the goal and start states condition the generation of the waypoints to generate the RGB-D+ training data. The original waypoints of the shortest path were obtained by running RRT\* for 30 seconds. We used $\mathrm { R R T ^ { * } }$ paths as training data, which provided a more stable distribution that did not fluctuate significantly when the configuration space was changed. We used path length as the minimization objective for the generator training, as it provides a reliable measure of the quality of the generated paths.

To implement the trained sampler, we utilized the Open Motion Planning Library (OMPL) [27] implementations of RRT and RRT\*. To compare how well the constraints were maintained by the trained model, we ran 3500 different, previously unseen scenarios with random goals and states, similar to the previous section. Each algorithm was run for

0.1, 0.2, and 0.5 seconds. The results are presented in Table I.

As shown in Table I, our algorithm improves the success rate, planning time, and average length compared to the implementations of RRT and RRT\* when the time constraint is between 0.1 and 0.2 seconds. When the planning time increases, RRT is able to improve its success rate because the uniform sampler starts the process earlier when the scenario is more challenging for the trained generator and too far of a good approximation of the original waypoints. Without timing constraints, $\mathrm { R R T ^ { * } }$ begins to converge to the optimal path cost; however, in scenarios where query time is critical, our approach generates a collision-free path that improves the cost compared to $\mathrm { R R T ^ { * } }$ at query times similar to RRT, as seen in the 0.5 seconds case. Additionally, for cost constrained paths, we see that our algorithm increases the success rate of the planning task, as it spends less time reaching the boundary set by $\sigma _ { k } .$ , given that most of the time constrained waypoints is a subset of $\mathcal { C } _ { f r e e }$ . This clearly demonstrates that our approach effectively increases the success rate, reflecting the probabilistic completeness of our algorithm given that the success rate increases as the maximum planning time increases.

## VIII. CONCLUSION AND FUTURE WORK

In this work, we have presented a novel approach for training WGAN-GP models conditioned by continuous latent matrices, which can be utilized for tasks related to waypoints prediction and path planning. We also proposed using the parametric learned model to evaluate whether the approximation has failed in predicting the waypoints in $\mathcal { C } _ { f r e e }$ . Additionally, we explored incorporating extra channels from the RGB-D working space to constrain the path to a specific cost function.

The experiments indicated that using images as a representation of waypoints in $\mathcal { C } _ { f r e e }$ stabilizes training and simplifies the deep neural network (DNN) models by utilizing convolutional networks instead of fully connected DNNs. The inclusion of high-dimensional ordering contributes to creating almost continuous training data in the image space. However, it is important to note that poor approximations of the waypoints could increase the planning time to be in par with the original sampler of the path planner, as regions not part of the collisionfree path will be explored first.

The results of our experiments demonstrate that our proposed model is capable of generating collision-free paths in unknown scenarios with an improved success rate and reduced running time compared to conventional path planning algorithms such as RRT and RRT\*. This is particularly useful when these algorithms are constrained by a specific running time, making our approach valuable for real-world scenarios.

In the case of having a bad approximation of the waypoints, our proposed approach is capable of rejecting such samples and revert to a uniform sampler without input from the user about the ratio between samplers, a capability non-previously seen in other works.

We have also shown the effectiveness of our method in planning paths in a 7-dimensional space for a humanoidmanipulator robot. To establish the broader applicability of our method, it is necessary to extend it to higher-dimensional spaces and non-stationary robots. This is critical for demonstrating its usefulness in solving diverse problems in realworld applications and scenarios. Future work will focus on exploring the feasibility of this extension and evaluating the performance of our method on more complex tasks and scenarios.

<table><tr><td>Algorithm</td><td>Max Planning Time (s)</td><td>Percentage of success</td><td>Average planning time (s)</td><td>Average Length rad</td></tr><tr><td>RRT</td><td>0.1</td><td>35%</td><td> $0.07 \pm 0.02$ </td><td> $10.12 \pm 3.18$ </td></tr><tr><td>RRT*</td><td>0.1</td><td>30%</td><td> $0.1 \pm 0.0$ </td><td> $10.04 \pm 3.11$ </td></tr><tr><td>RRT-WGAN</td><td>0.1</td><td>63%</td><td> $0.06 \pm 0.01$ </td><td> $9.91 \pm 2.86$ </td></tr><tr><td>RRT</td><td>0.2</td><td>60%</td><td> $0.11 \pm 0.04$ </td><td> $10.65 \pm 3.25$ </td></tr><tr><td>RRT*</td><td>0.2</td><td>58%</td><td> $0.2 \pm 0.0$ </td><td> $10.57 \pm 3.20$ </td></tr><tr><td>RRT-WGAN</td><td>0.2</td><td>75%</td><td> $0.08 \pm 0.04$ </td><td> $10.4 \pm 3.15$ </td></tr><tr><td>RRT</td><td>0.5</td><td>94%</td><td> $0.15 \pm 0.1$ </td><td> $10.91 \pm 3.33$ </td></tr><tr><td>RRT*</td><td>0.5</td><td>87%</td><td> $0.5 \pm 0.0$ </td><td> $10.73 \pm 3.15$ </td></tr><tr><td>RRT-WGAN</td><td>0.5</td><td>87%</td><td> $0.11 \pm 0.1$ </td><td> $10.81 \pm 3.32$ </td></tr></table>

TABLE I: Results of constrained planning of a collision-free path using a Baxter robot and a human inside its working space in previously unseen scenarios. The constraint is finding the shortest path. The red rectangles represent the best result in each metric given different maximum planning times.

The convergence of affinity propagation could potentially generate more exemplars than the matrix can accommodate. Therefore, further research is needed to explore methods for reducing the amount of data required to represent the waypoints in $\mathcal { C } _ { f r e e }$ as a matrix representation.

## IX. ACKNOWLEDGEMENT

We acknowledge the computing resources provided by Calcul Quebec and the Digital Research Alliance of Canada.´

## REFERENCES

[1] A. H. Qureshi, Y. Miao, A. Simeonov, and M. C. Yip, “Motion Planning Networks: Bridging the Gap Between Learning-based and Classical Motion Planners,” IEEE Transactions on Robotics, pp. 1–9, 2020.

[2] T. S. Lembono, E. Pignat, J. Jankowski, and S. Calinon, “Learning Constrained Distributions of Robot Configurations With Generative Adversarial Network,” IEEE Robotics and Automation Letters,, vol. 6, no. 2, pp. 4233–4240, 2021.

[3] M. Q.-H. M. Tianyi Zhang, Jiankun Wang, “Generative Adversarial Network Based Heuristics for Sampling-Based Path Planning,” IEEE/CAA Journal of Automatica Sinica, vol. 9, no. JAS-2021-0110, p. 64, 2022.

[4] Z. Li, J. Wang, and M. Q. Meng, “Efficient Heuristic Generation for Robot Path Planning with Recurrent Generative Model,” IEEE International Conference on Robotics and Automation, pp. 7386–7392, 2021.

[5] L. Rout, A. Korotin, and E. Burnaev, “Generative Modeling with Optimal Transport Maps,” in International Conference on Learning Representations, 2022.

[6] B. Ichter, J. Harrison, and M. Pavone, “Learning Sampling Distributions for Robot Motion Planning,” in 2018 IEEE International Conference on Robotics and Automation, 2018, pp. 7087–7094.

[7] J. Wang, T. Li, B. Li, and M. Q.-H. Meng, “GMR-RRT\*: Sampling-Based Path Planning Using Gaussian Mixture Regression,” IEEE Transactions on Intelligent Vehicles, vol. 7, no. 3, pp. 690–700, 2022.

[8] J. Urain, A. Mandlekar, Y. Du, M. Shafiullah, D. Xu, K. Fragkiadaki, G. Chalvatzaki, and J. Peters, “Deep Generative Models in Robotics: A Survey on Learning from Multimodal Demonstrations,” 2024, arXiv.

[9] J. Kuffner and S. LaValle, “RRT-Connect: An Efficient Approach to Single-Query Path Planning.” in Proceedings - IEEE International Conference on Robotics and Automation, vol. 2, 01 2000, pp. 995–1001.

[10] S. Karaman and E. Frazzoli, “Sampling-based Algorithms for Optimal Motion Planning,” International Journal of Robotic Research, vol. 30, pp. 846–894, 06 2011.

[11] N. Perez Higueras, F. Caballero, and L. Merino, “Teaching Robot´ Navigation Behaviors to Optimal RRT Planners,” International Journal of Social Robotics, vol. 10, 04 2018.

[12] S. Huang, Z. Wang, P. Li, B. Jia, T. Liu, Y. Zhu, W. Liang, and S.-C. Zhu, “Diffusion-based Generation, Optimization, and Planning in 3D Scenes,” in Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, 2023.

[13] S. M. LaValle, Planning Algorithms. USA: Cambridge University Press, 2006.

[14] I. J. Goodfellow, J. Pouget-Abadie, M. Mirza, B. Xu, D. Warde-Farley, S. Ozair, A. Courville, and Y. Bengio, “Generative Adversarial Nets,” in Proceedings of the 27th International Conference on Neural Information Processing Systems, vol. 2, 2014, pp. 2672–2680.

[15] V. Huynh and D. Phung, “Optimal transport for deep generative models: state of the art and research challenges,” in Proceedings of the Thirtieth International Joint Conference on Artificial Intelligence, 2021, pp. 4450– 4457.

[16] M. Arjovsky, S. Chintala, and L. Bottou, “Wasserstein Generative Adversarial Networks,” in Proceedings of the 34th International Conference on Machine Learning, vol. 70, 2017, pp. 214–223.

[17] I. Gulrajani, F. Ahmed, M. Arjovsky, V. Dumoulin, and A. Courville, “Improved Training of Wasserstein GANs,” in Proceedings of the 31st International Conference on Neural Information Processing Systems, 2017, pp. 5769–5779.

[18] X. Gu, N. Lei, and S.-T. Yau, Optimal Transport for Generative Models. Springer International Publishing, 2021.

[19] B. J. Frey and D. Dueck, “Clustering by Passing Messages Between Data Points,” Science, vol. 315, no. 5814, pp. 972–976, 2007.

[20] J. Ortiz-Haro, J.-S. Ha, D. Driess, and M. Toussaint, “Structured deep generative models for sampling on constraint manifolds in sequential manipulation,” in Proceedings of the 5th Conference on Robot Learning, vol. 164, 08–11 Nov 2022, pp. 213–223.

[21] T. Lai and F. Ramos, “Plannerflows: Learning motion samplers with normalising flows,” in IEEE/RSJ International Conference on Intelligent Robots and Systems, 2021, pp. 2542–2548.

[22] T. Lai, W. Zhi, T. Hermans, and F. Ramos, “Parallelised Diffeomorphic Sampling-based Motion Planning,” in Proceedings of the 5th Conference on Robot Learning, vol. 164, 08–11 Nov 2022, pp. 81–90.

[23] A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A. N. Gomez, L. u. Kaiser, and I. Polosukhin, “Attention is all you need,” in Advances in Neural Information Processing Systems, vol. 30, 2017.

[24] J. Gehring, M. Auli, D. Grangier, D. Yarats, and Y. N. Dauphin, “Convolutional sequence to sequence learning,” in Proceedings of the 34th International Conference on Machine Learning - Volume 70, 2017, pp. 1243–1252.

[25] J. Wang, W. Chi, C. Li, C. Wang, and M. Q. Meng, “Neural RRT\*: Learning-Based Optimal Path Planning,” IEEE Transactions on Automation Science and Engineering, vol. 17, pp. 1748–1758, 2020.

[26] S. LaValle and J. Kuffner, “Randomized kinodynamic planning,” in IEEE International Conference on Robotics and Automation, vol. 1, 1998, pp. 473–479.

[27] Z. Kingston, M. Moll, and L. E. Kavraki, “Exploring implicit spaces for constrained sampling-based planning,” International Journal of Robotics Research, vol. 38, no. 10–11, pp. 1151–1178, 2019.