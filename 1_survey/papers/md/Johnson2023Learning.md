---
citation_key: Johnson2023Learning
arxiv_id: 2306.00851
arxiv_url: "https://arxiv.org/abs/2306.00851"
title: "Learning Sampling Dictionaries for Efficient and Generalizable Robot Motion Planning with Transformers"
authors_short: "Jacob J Johnson et al."
year: 2023
direction_tag: J_homotopy_topology
source: mineru-vlm
converter: mineru-open-api
model: vlm
converted_at: 2026-06-25T09:28:09Z
origin: ai+web
reviewed: false
---

# Learning Sampling Dictionaries for Efficient and Generalizable Robot Motion Planning with Transformers

Jacob J. Johnson<sup>†</sup>, Ahmed H. Qureshi<sup>‡</sup>, and Michael C. Yip<sup>†</sup>

Abstract— Motion planning is integral to robotics applications such as autonomous driving, surgical robots, and industrial manipulators. Existing planning methods lack scalability to higher-dimensional spaces, while recent learning-based planners have shown promise in accelerating sampling-based motion planners (SMP) but lack generalizability to out-of-distribution environments. To address this, we present a novel approach, Vector Quantized-Motion Planning Transformers (VQ-MPT) that overcomes the key generalization and scaling drawbacks of previous learning-based methods. VQ-MPT consists of two stages. Stage 1 is a Vector Quantized-Variational AutoEncoder model that learns to represent the planning space using a finite number of sampling distributions, and stage 2 is an Auto-Regressive model that constructs a sampling region for SMPs by selecting from the learned sampling distribution sets. By splitting large planning spaces into discrete sets and selectively choosing the sampling regions, our planner pairs well with outof-the-box SMPs, generating near-optimal paths faster than without VQ-MPT’s aid. It is generalizable in that it can be applied to systems of varying complexities, from 2D planar to 14D bi-manual robots with diverse environment representations, including costmaps and point clouds. Trained VQ-MPT models generalize to environments unseen during training and achieve higher success rates than previous methods. Videos and code are available at https://sites.google.com/ucsd. edu/vq-mpt/home.

## I. INTRODUCTION

Sampling-based motion planning use randomly sampled points to generate a tree-based collision-free path between a start and goal locations [1], [2]. However, random sampling is inefficient [3] for goal-directed tasks, particularly when the search space spans a high number of dimensions. Since sampling-based motion planners (SMPs) are a fundamental component of numerous autonomous systems [4], [5], improving the efficiency and generalizability of the underlying planners enables these systems to handle more complex tasks that involve intricate sequences of planning, improves task execution, and reduces the need to retrain planners for different environments. While SMPs effectively generate a trajectory, they face several challenges in improving sampling efficiency. As the dimensionality of the configuration space increases, the ”curse of dimensionality” makes sampling more difficult and time-consuming. Efficiently exploring high-dimensional spaces to find feasible paths is a significant challenge. These planners must also be able to reliably solve for different environments without the need for reconfiguring planner parameters. Most of these planners are probabilistically complete, i.e., the planner will find a path if a trajectory exists, given enough time. But finding a trajectory that is optimal, like the shortest path, is also a challenge. Numerous works have been proposed that address some of these challenges.

![](Johnson2023Learning_figs/88dc42fdc63334b19aa35c84a5bb9b3d5650e7c7a3fd9fedc30f38a5b4723a88.jpg)

![](Johnson2023Learning_figs/887f72a5267dbffe8e6dd54e3602ddd0418f9e186375dbda76a323baa6cdfa45.jpg)  
Fig. 1. VQ-MPT can efficiently split high-dimensional planning spaces into discrete sets of distributions. Each distribution is represented using a latent variable called code or dictionary value. Given a planning problem, the model selects a subset of codes and samples from the associated distributions to construct the trajectory. By sampling efficiently, VQ-MPT reduces planning times by 2-6× compared to previous planners.

For efficient sampling, prior works have reduced the search spaces through hand-crafted heuristics or parametric functions, decreasing planning time. The current state-of-the-art motion planners leverage goal-directed heuristics; Informed-RRT<sup>∗</sup> (IRRT<sup>∗</sup>) [6] and Batch Informed Trees (BIT<sup>∗</sup>) [7] search for a path in an ellipsoidal region between the start and goal location. In [8], [9], Artificial Potential Fields (APF) guide random samples toward regions with an optimal solution. Sampling-based A<sup>∗</sup> [1] extends the A<sup>∗</sup> search algorithm to sampling-based planning and uses heuristics to sample from selected vertices. But for higher dimensional spaces, sampling with these heuristics still leaves many samples unused for constructing a trajectory.

On the other hand, learning-based methods leverage data from prior planned data to accelerate planning in similar environments [10], [11], [12], [13]. Motion Planning Networks (MPNet) [14] was the first neural planner to generate the full motion planning solution through a recurrent sampling of its networks, given the current and goal position of the robot as well as the environment representation. MPNet considerably reduces planning time for higher dimensions, but these models do not generalize to larger environment representations [15]. Other neural planners [16], [17] have also explored using neural networks for planning.

Transformer models are an ideal candidate for solving the planning problem because of their ability to make long-horizon connections [18]. Advances in large language models, such as BERT [19], and GPT [20], have inspired similar efforts in solving planning tasks using transformer models [21], [22]. These models make better control decisions in robotic quadrupedal walking tasks by attending to proprioceptive and visual sensor data [23]. Although these works support the possibility of using transformer models for decision-making, it is difficult to interpret the policy’s future control actions and provide any form of guarantee for the underlying planner. Other works [15], [24] only solve for planar manipulators and 2D mobile robots because, inherently, their network models follow those used in image understanding in 2D discrete spaces. Since these models have to discretize the entire planning space, extending these methods to higher dimensional, continuous planning spaces would exponentially increase training and memory costs. Furthermore, these planners require the space in which the path is constructed (planning space) to overlap with the space in which the environment is represented (task space). For example, for a 14-degree-of-freedom bi-manual robot arm setup, the environment is represented using point clouds which is $\mathbb { R } ^ { 3 }$ , while the planning space is $\mathbb { R } ^ { 1 4 }$ . How these methods apply to environments with disjoint planning and task space is unclear.

In this work, we propose VQ-MPT, a scalable transformerbased model that accelerates SMP by narrowing the sampling space. VQ-MPT uses a Vector Quantized (VQ) model to discretize the planning space. VQ models are generative models with an encoder-decoder architecture similar to Variational AutoEncoder (VAE) models but with the latent dimension represented as a collection of learnable vectors referred to as dictionaries. A transformer model selects a subset of these learned vectors to generate the search region for the given planning problem. We describe in this paper how the VQ approach can be used in the context of motion planning, leading to the following major advantages:

1) Reduces planning times by 2-6× compared to traditional planning algorithms such as BIT<sup>∗</sup> and by 3-6× compared to learned planners such as MPNet.

2) Scales to 14-dimensional planning spaces without compromising planning performance.

3) Learns efficient quantization of high dimensional planning space without increasing the dictionary size.

4) Generalizes to unseen in-distribution and out-ofdistribution environments more successfully than learned planners such as MPNet.

## II. BACKGROUND

## A. Problem Definition

Consider the planning space defined by $\mathcal { X } ~ \in ~ \mathbb { R } ^ { n }$ . We define a subspace $\chi _ { f r e e } \subset \mathcal { X } .$ , such that all states in $\mathcal { X } _ { f r e e }$ do not collide with any obstacle in the environment and are considered valid configuration. The objective of the motion planner is to generate a sequence of states: $\mathcal { Q } = \{ q _ { 1 } , q _ { 2 } , \dots , q _ { n _ { s } } \}$ for a given start state $( q _ { 1 } )$ and a goal region $( \mathcal { X } _ { g o a l } )$ such that $q _ { i } \in \mathscr { X } _ { f r e e } , \forall i \in \{ 1 , 2 , \ldots , n _ { s } \}$ the edge connecting $q _ { i }$ and $q _ { i + 1 }$ is also in $\lambda _ { f r e e } ,$ i.e., $( 1 - \alpha ) q _ { i } + \alpha q _ { i + 1 } \in \mathcal { X } _ { f r e e } , \forall \alpha \in [ 0 , 1 ] .$ , and $q _ { n _ { s } } \in \mathcal { X } _ { g o a l } .$ The sequence of states is often referred to as a trajectory or path. In this work, we are interested in a novel learning-based approach to promote efficient sampling in $\mathcal { X }$ for generating a valid, optimized trajectory.

## B. Vector Quantized Models

The VQ-VAE model has been shown to compress highdimensional spaces such as images and audio without posterior collapse observed in VAE models [25]. We utilize a VQ-VAE in a similar manner to compress the robot planning space $\mathcal { X } .$ The VQ model encodes input $q \in \mathbb { R } ^ { n }$ using a function $f$ to a latent space ${ \mathcal { Z } } ,$ and is quantized to a set of learned vectors $\mathcal { Z } _ { Q } = \{ \hat { z } _ { 1 } , \hat { z } _ { 2 } , . . . , \hat { z } _ { N } \}$ . The vectors in $\mathcal { Z } _ { Q }$ are often called codes or dictionary values in literature. The function $g$ decodes the closest vector in $\mathcal { Z } _ { Q }$ to $f ( q )$ back to the input space. The parameters of $f$ and $g$ and the set of vectors in $\mathcal { Z } _ { Q }$ are estimated using self-supervised learning by minimizing the following error,

$$
\mathcal {L} = \mathcal {L} _ {r e c o n} + \| \mathrm{sg} [ f (q) ] - \hat {z} \| + \beta \| f (q) - \mathrm{sg} [ \hat {z} ] \|,\tag{1}
$$

where $\hat { z }$ is the quantized vector and sg[ ] stands for the stop gradient operator [25], which has zero partial derivatives, i.e. $\nabla \mathrm { s g } ( x ) = 0 ,$ , preventing the operand from being updated during training. $\mathcal { L } _ { r e c o n }$ is the main AE reconstruction loss (we will derive this later). The second term is used to update the latent vectors in $\mathcal { Z } _ { Q }$ while keeping the encoder output constant, and the last term is called the commitment loss and updates the encoder function while keeping the latent vectors constant. This prevents the output of the encoder from drifting away from the current set of latent vectors. Yu et al. [26] proposed two further improvements in representing the codes to help improve the training stability, code usage, and reconstruction quality of VQ-VAE models for images.

1) Factorized Codes: The output from the encoder function is linearly projected to a lower dimensional space. For example, if the encoder output is a 1024-d vector, it is projected to an 8-d vector. The authors in [26] show that using a lower dimensional space improves code usage and reconstruction quality.

2) Normalized Codes: Each factorized codes, $\hat { z } _ { i } ,$ , are $l _ { 2 }$ normalized. Hence all the dictionary values are mapped onto a hypersphere. This improves the training stability and reconstruction quality of the model.

![](Johnson2023Learning_figs/918502a88320181c817393b472058387ce81241d00ea5fcec94ec77caf61cdde.jpg)  
Stage 1 : Learning sampling dictionary  
Stage 2 : Predicting Distributions  
Fig. 2. An outline of the model architecture of VQ-MPT. Stage 1 (Left) is a Vector Quantizer that learns a set of latent dictionary values that can be mapped to a distribution in the planning space. By encoding the planning space to discrete distributions, we can plan for high-dimensional robot systems. Stage 2 (Right) is the Auto-Regressive (AR) model that sequentially predicts the sampling regions for a given environment and a start and goal configuration. The cross-attention model transduces the start and goal embeddings given the environment embedding generated using a feature extractor. The output from the AR Transformer is mapped to a distribution in the planning space using the decoder model from Stage 1.

## C. Transformer Models

Transformer models are transduction models that consist of self-attention [27] and fully connected layers. They have been shown to efficiently model sequence data for language and image tasks [18], [28], hence an ideal encoder model. The self-attention layer is a Scaled Dot-product Attention [18] that takes three matrices - query $( Q \in \mathbb { R } ^ { n _ { s } \times d _ { q } } )$ , value $( V \in \mathbb { R } ^ { n _ { s } \times d _ { v } } )$ , and key $( K \in \mathbb { R } ^ { n _ { s } \times d _ { q } } )$ vectors to generate the attention output

$$
\operatorname{Atten} (Q, K, V) = \operatorname{softmax} \left(\gamma^ {- 1} Q K ^ {T}\right) V,\tag{2}
$$

where $n _ { s }$ is the sequence length, $d _ { q }$ is the dimension of the query space, $d _ { v }$ is the dimension of key and value space, and $\gamma = \sqrt { d _ { v } }$ is a scaling factor. Rather than doing a single attention function, these models linearly project the query, key, and value vectors multiple times using different learned weights and is called the multi-headed attention model. This enables the model to attend to different features present in the data. The final output is a linear combination of individual attention values evaluated on each projected set. The pooled output is passed through deep residual multilayer perceptron (MLP) networks. In [29], the authors introduce Prenorm-Transformer where the inputs to the attention and MLP layers are normalized as this makes training the model more stable.

## III. VECTOR QUANTIZED-MOTION PLANNING TRANSFORMERS

The VQ pipelines in image generation [30], [26] consist of a quantization stage and a prediction stage. We adapt this pipeline for sequence generation and represent the planning space as a collection of distributions (Fig. 2). Below, we describe the two stages and objectives used for training.

## A. Stage 1: Vector Quantizer

The first stage learns to represent the planning space using a set of distributions. It does not take any sensor data such as costmap or pointcloud. We use a VQ model similar to VQ-VAE [25] with a transformer network as the encoder and propose a maximum likelihood-based reconstruction loss to learn the set of distributions. The encoder network takes in a trajectory, ${ \mathcal { Q } } = \{ q _ { 1 } , q _ { 2 } , . . . , q _ { n _ { s } } \}$ , and outputs a set of latent vectors, $\mathcal { Z } ~ = ~ \{ z _ { 1 } , z _ { 2 } , . ~ . ~ . ~ , z _ { n _ { s } } \}$ The decoder model, an MLP model, maps the quantized encoder output to a sequence of parameterized distributions, $\{ P ( \cdot ; \theta _ { 1 } ) , P ( \cdot ; \theta _ { 2 } ) , \ldots , P ( \cdot ; \theta _ { n _ { s } } ) \}$ , in the planning space. We define our reconstruction loss as follows:

$$
\begin{array}{c} \mathcal {L} _ {r e c o n} = - \sum_ {j = 1} ^ {n _ {s}} \log (P (q _ {j}; \theta_ {j})) \\ - \lambda \sum_ {j = 1} ^ {n _ {s}} \mathbb {E} _ {q \sim \mathcal {X}} [ - \log (P (q; \theta_ {j})) ] \end{array}\tag{3}
$$

where λ is a scaling constant. The first term maximizes the likelihood of observing the input trajectory, while the second term maximizes the differential entropy. The entropy term prevents the distribution from overfitting to each batch of data because a small batch size does not cover the entire planning space. In the following paragraphs, we provide further details of our models.

The encoder model transforms each state in the trajectory into an efficient representation by learning patterns in the sequence. Each input state, $q _ { j } .$ , to the encoder is linearly projected to a latent space $\mathbb { R } ^ { d }$ , and fixed position embedding [18] is added to the projected output. The resulting vector is passed through multiple blocks of Prenorm-Transformer described in Section II-C to obtain the set $\mathcal { Z } .$ Each latent vector $z _ { j } \in { \mathcal { Z } }$ is quantized to a vector from the set $\mathcal { Z } _ { Q } =$ $\{ \hat { z } _ { 1 } , \hat { z } _ { 2 } , \dots , \hat { z } _ { N } \}$ using the function $z _ { q } ( \cdot )$ defined by:

$$
z _ {q} (z) = \hat {z} _ {i} \quad \text { where } \quad i = \underset {k \in \{1, \ldots , N \}} {\operatorname{argmin}} \| z - \hat {z} _ {k} \|\tag{4}
$$

where $\hat { z } _ { i }$ is the quantized vector corresponding to $q _ { i } .$ . We prepend and append the transduced set with static encodings $z _ { s }$ and $z _ { g }$ to indicate the start and end of the sequence, respectively. Hence the robot trajectory Q is transduced to $\hat { \mathcal { Z } } = \{ z _ { s } , z _ { q } ( z _ { 1 } ) , z _ { q } ( z _ { 2 } ) , \ldots z _ { q } ( z _ { n _ { s } } ) , z _ { g } \}$

The decoder model maps each quantized vector, $z _ { q } ( z _ { i } )$ to the parameterized distribution $P ( \cdot ; \theta _ { i } )$ . We choose the output distribution as Gaussian, but any parametric distribution, such as Gaussian Mixture Models, Exponential distributions, or Uniform distributions, can be chosen. The decoder model outputs the mean and the covariance matrix of the Gaussian distribution $( { \mathcal { N } } ( \mu , \Sigma ) )$ ; hence it is a function of the dictionary value $z _ { q } ( z _ { j } ) , \forall j \ \in \ \{ 1 , \ldots , n _ { s } \}$ , and is represented by $\mu ( z _ { q } ( z _ { j } ) )$ and $\Sigma ( z _ { q } ( z _ { j } ) )$ respectively. We will refer to these variables as $\mu _ { j }$ and $\Sigma _ { j }$ for simplicity.

To ensure that the covariance matrix always remains positive definite during training, we decompose $\Sigma _ { j }$ using Cholesky decomposition as in previous works [31], [32]:

$$
\Sigma_ {j} = L _ {j} D _ {j} L _ {j} ^ {T}\tag{5}
$$

where $L _ { j }$ is a lower triangle matrix with ones along the diagonal, and $D _ { j }$ is a diagonal matrix with positive values. The output from the penultimate MLP layer is passed through separate linear layers to obtain $\mu _ { j }$ and $L _ { j }$ , while for $D _ { j } ,$ , it is passed through a linear and soft-plus layer [33] to ensure values are positive. Using the soft-plus layer improves the stability of training the model.

## B. Stage 2: Auto-Regressive (AR) Prediction

The second stage generates sampling regions by predicting indexes from the dictionary set $\mathcal { Z } _ { Q }$ for a given planning problem and sensor data. It comprises two models - a cross-attention model to embed start and goal pairs and the environment embedding into latent vectors $( M )$ , and a Transformer-based Auto-Regressive (AR) model to predict the dictionaries indexes, $\mathcal { H } = \{ h _ { 1 } , h _ { 2 } , . . . h _ { n _ { h } } \}$ . Both models are trained end-to-end by reducing the cross entropy loss using trajectories from an $\mathrm { { R R T ^ { * } } }$ planner:

$$
\mathcal {L} _ {C E} = \mathbb {E} [ - \sum_ {j = 1} ^ {n _ {h}} \sum_ {i = 1} ^ {N + 1} \delta_ {i} (h _ {j}) \log (\pi (h _ {j} = i | \hat {z} _ {h _ {1}}, \dots , \hat {z} _ {h _ {j - 1}}, M)) ]\tag{6}
$$

where $\delta _ { i } ( \cdot )$ is the Kronecker delta function, $\pi ( \cdot )$ is the output of the AR model, and $\hat { z } _ { h _ { i } }$ corresponds to the latent dictionary vector associated with the ground truth index $h _ { i } ,$ , and the expectation is over multiple trajectories. We provide more details of the models in the following section.

The environment representation $( \mathrm { i . e . }$ , costmap or point cloud data) is passed through a feature extractor to construct the environment encodings $\mathcal { E } = \{ e _ { 1 } , e _ { 2 } , \ldots , e _ { n _ { e } } \}$ where $e _ { i } \in$ $\mathbb { R } ^ { d }$ . The feature extractor reduces the dimensionality of the environment representation and captures local environment structures as latent variables using convolutional layers for costmaps and set-abstraction layers for point clouds. The start and goal states $( q _ { s }$ and $q _ { g } )$ are projected to the start and goal embedding $( \mathcal { E } _ { s } ~ \in ~ \mathbb { R } ^ { d }$ and $\mathcal { E } _ { g } ~ \in ~ \mathbb { R } ^ { d } )$ using a MLP network. The cross-attention model is a Prenorm-Transformer model that uses the environment embedding, $\mathcal { E } ,$ and the start and goal embedding, $\{ \mathcal { E } _ { s } , \mathcal { E } _ { g } \}$ to generate latent vectors M. The cross-attention model learns a feature embedding that fuses the given start and goal pair with the given planning environment. It uses the vector in $\mathcal { E }$ as keyvalue pairs, and ${ \mathcal { E } } _ { s }$ and $\mathcal { E } _ { g }$ as query vectors to generate $M$

We use an AR Transformer model, $\pi ( \cdot )$ , to predict the dictionary indexes H. A Transformer-based AR model was chosen because of their ability to make long-horizon connections. For each index $h _ { j }$ , the model outputs a probability distribution over $\mathcal { Z } _ { Q } \cup \{ z _ { g } \}$ given dictionary values of previous predictions $\{ \hat { z } _ { h _ { 1 } } , \hat { z } _ { h _ { 2 } } , \dots , \hat { z } _ { h _ { j - 1 } } \}$ and the planning context M:

$$
\pi (h _ {j} = i | \hat {z} _ {h _ {1}}, \dots , \hat {z} _ {h _ {j - 1}}, M) = p _ {i} \quad \text { where } \sum_ {i = 1} ^ {N + 1} p _ {i} = 1\tag{7}
$$

Using the learned decoder from Stage 1, we can convert each of the predicted dictionary values, $\hat { z } _ { h _ { j } }$ , into a Gaussian distribution $( \mathcal { N } ( \mu _ { h _ { j } } , \Sigma _ { h _ { j } } ) )$ in the planning space.

## C. Generating Distributions for Sampling

With stage 1, we have efficiently split the planning space into a discrete set of distributions represented using a set of latent vectors, and with stage 2, we have provided a means to select a subset of distributions from the dictionary. Given a new planning problem, we use the trained Stage 2 models to generate a sequence of dictionary indexes H = $\{ h _ { 1 } , \ldots h _ { n _ { h } } \}$ . Since each index can take N values, we pick the sequence H that maximizes the following probability:

$$
P (h _ {1}, \dots , h _ {n _ {h}} | M) = \prod_ {i = 1} ^ {n _ {h}} \pi (h _ {i} | h _ {1}, \dots , h _ {i - 1}, M)\tag{8}
$$

where $h _ { n _ { h } }$ is the goal index and π is the probability from Eqn. 7. We apply a beam-search algorithm to optimize for Eqn. 8 as done before in language model tasks [19].

The decoder model from Stage 1 is used to generate a set of distributions, P, from the dictionary values, $\left\{ \hat { z } _ { h _ { 1 } } , \hat { z } _ { h _ { 2 } } , \dots , \hat { z } _ { h _ { n _ { h } - 1 } } \right\}$ , corresponding to the predicted indexes $\{ h _ { 1 } , h _ { 2 } , . . . , \ddot { h } _ { n _ { h } - 1 } \}$ }. We define this set as a Gaussian Mixture Model (GMM) with uniform mixing coefficients:

$$
\mathcal {P} (q) = \sum_ {i = 1} ^ {n _ {h} - 1} \frac {1}{n _ {h} - 1} \mathcal {N} (\mu (\hat {z} _ {h _ {i}}), \Sigma (\hat {z} _ {h _ {i}}))\tag{9}
$$

An example of this distribution is in Fig. 3 for a 2D robot.

![](Johnson2023Learning_figs/52af05ea8515bef149664bc17b37a261a8a5156c50322cbc0861cbc10cb6bc94.jpg)  
Fig. 3. A trajectory (black) planned using VQ-MPT for the 2D robot and the corresponding GMM used for sampling. Each ellipse represents the distribution encoded by the dictionary values. The shaded region represents the 2 standard deviation confidence interval region. The dictionary values can encode the planning space using a finite number of vectors.

TABLE I  
MODEL AND ENVIRONMENT PARAMETERS FOR EACH ROBOT

<table><tr><td>Robot</td><td>Environment Representation</td><td>d</td><td>Dictionary Keys</td><td> $d_k$ </td><td> $d_v$ </td></tr><tr><td>2D</td><td>Costmap</td><td>512</td><td>1024</td><td>512</td><td>256</td></tr><tr><td>7D</td><td>Point Cloud</td><td>512</td><td>2048</td><td>512</td><td>256</td></tr><tr><td>14D</td><td>Point Cloud</td><td>512</td><td>2048</td><td>512</td><td>256</td></tr></table>

## D. Planning

To generate a trajectory, any SMP can be used to generate the trajectory by sampling from the distribution given in Eqn. 9. We use Algorithm 1, to generate a path using samples from the distribution in Eqn. 9. The VQMPTPlanner function takes the start and goal state $( q _ { s }$ and $q _ { g } )$ , the number of samples to generate (K), and a threshold value (b) to sample the goal state and returns a valid trajectory. This function is a modified RRT algorithm, where instead of CONNECT extending the current node by a small range, it checks if a valid path exists between the current and sampled node.

## IV. EXPERIMENTS

We evaluated our framework on three environments - a 2D point robot, a 7D Franka Panda Arm, and a 14D Bimanual Setup. Our experiments compare the use of VQ-MPT coupled with RRT (Algorithm 1) with traditional and learningbased planners on a diverse set of planning problems. All planners were implemented using the Open Motion Planning Library (OMPL) [34].

## A. Setup

We trained a separate VQ-MPT model for each robot system and chose feature extractors based on environment representations. For costmaps, we used the Fully Convolutional Network (FCN) as in [15], while for point cloud data, we used two layers of set-abstraction proposed in PointNet++ [35]. We chose these architectures because they are agnostic to the environment size and can generate latent embeddings for larger-sized costmaps or point clouds. The same transformer model architecture was used for the Stage 1 encoder, the cross-attention network, and the AR model. Each transformer model consisted of 3 attention layers with 3 attention heads each. Table I details the latent vector dimensions and the dictionary size used for each robot. A larger key size was used for the 7D and 14D robots because of the larger planning space. We observed that increasing the dictionary size further did not reduce the reconstruction loss.

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 1: VQMPTPlanner(qs, qg, P, K, b)
1  $\tau \leftarrow \{q_s\}$ ;
2 for k  $\leftarrow 0$  to K do
3    $q_{rand} \leftarrow \text{SAMPLE}(\mathcal{P})$ ;
4    $q_{near} \leftarrow \text{NEAREST}(q_{rand}, \tau)$ ;
5    if CONNECT(qrand, qnear) then
6    $\tau \leftarrow \tau \cup \{q_{rand}\}$ ;
7    end
8    if rand() &gt; b then
9    $q_{gn} \leftarrow \text{NEAREST}(q_g, \tau)$ ;
10    if CONNECT(qgn, qg) then
11    $\tau \leftarrow \tau \cup \{q_g\}$ ;
12    break;
13    end
14    end
15    SIMPLIFY( $\tau$ );
16    return  $\tau$ 
17 end
</div>

All models were trained using data collected from simulation. We collected two sets of trajectories.

1) Trajectories without obstacles: This set consisted of trajectories in an environment without obstacles and was used to train Stage 1 of the model. These trajectories were free from any form of self-collision and covered the whole planning space of the planner. For each robot, we collected 2000 trajectories of this type.

2) Trajectories with obstacles: This set consisted of valid trajectories collected from environments where obstacles were placed randomly in the scene. It was used to train Stage 2 of the model. For each robot, we collected 10 trajectories for 2000 randomly generated environments.

We trained Stages 1 and 2 using the Adam optimizer [36] with $\beta _ { 1 } = 0 . 9 , \beta = 0 . 9 8$ and $\epsilon = 1 0 ^ { - 9 }$ and a scheduled learning rate from [18].

## B. Results - Unseen In-Distribution Environments

We compared our framework against traditional and learning-based SMP algorithms for each robot system on a trajectory from 500 different environments. To quantify planning performance, we measured three metrics: planning time - the time it takes for the planner to generate a valid trajectory; vertices - the number of collision-free vertices required to find the trajectory and accuracy - the percentage of planning problems solved before a given cutoff time. We chose to measure vertices because checking the validity of a vertex imposes a significant cost on most SMPs [37]. Since optimal planners do not have termination conditions, for fair comparisons, we stopped planning when the constructed trajectory, $\{ q _ { 1 } , q _ { 2 } , \ldots , q _ { n } \}$ , satisfied the following condition:

![](Johnson2023Learning_figs/f4633ccd9651b57963ccd1c1f73ccefd4fe99087cca02a67f0027bf74e9143ed.jpg)

![](Johnson2023Learning_figs/c62312bd0d4194c22b13281023d8612ad56e6bfcb8831a2c94991b09cbe9ca27.jpg)

![](Johnson2023Learning_figs/3478b8ccaa75acd853e91eb0343bd52c89343adceb9126bf47b4147175c34406.jpg)  
Fig. 4. Plots of planning time and percentage of paths successfully planned on in-distribution environments for the 2D (Left), 7D (Center), and 14D (Right) robots. VQ-MPT can solve problems faster than other SMP planners by reducing the planning space and scales to higher dimensional problems.

TABLE II  
COMPARING ACCURACY AND MEAN PLANNING TIME AND VERTICES IN IN-DISTRIBUTION ENVIRONMENTS

<table><tr><td>Robot</td><td></td><td>RRT*</td><td>RRT* (50%)</td><td>IRRT*</td><td>IRRT* (50%)</td><td>BIT*</td><td>BIT* (50%)</td><td>MPNet</td><td>VQ-MPT</td></tr><tr><td rowspan="3">2D</td><td>Accuracy</td><td>94.8%</td><td>·</td><td>97.4%</td><td>·</td><td>96.0 %</td><td>·</td><td>92.35%</td><td>97.6%</td></tr><tr><td>Time (sec)</td><td>1.588</td><td>·</td><td>0.244</td><td>·</td><td>0.297</td><td>·</td><td>0.296</td><td>0.147</td></tr><tr><td>Vertices</td><td>1195</td><td>·</td><td>195</td><td>·</td><td>457</td><td>·</td><td>63</td><td>306</td></tr><tr><td rowspan="3">7D</td><td>Accuracy</td><td>52.80%</td><td>95.20%</td><td>89.0%</td><td>94.80%</td><td>72.20%</td><td>97.40%</td><td>94.2%</td><td>97.4%</td></tr><tr><td>Time (sec)</td><td>49.35</td><td>10.51</td><td>54</td><td>15.03</td><td>7.58</td><td>5.26</td><td>5.18</td><td>0.929</td></tr><tr><td>Vertices</td><td>683</td><td>149</td><td>63</td><td>71</td><td>826</td><td>640</td><td>147</td><td>45</td></tr><tr><td rowspan="3">14D</td><td>Accuracy</td><td>11.80%</td><td>32.00%</td><td>21.80%</td><td>40.40%</td><td>30.80%</td><td>43.40%</td><td>92.20%</td><td>99.20%</td></tr><tr><td>Time (sec)</td><td>1.80</td><td>15.03</td><td>52.84</td><td>29.16</td><td>9.56</td><td>39.09</td><td>17.46</td><td>2.62</td></tr><tr><td>Vertices</td><td>9</td><td>94</td><td>45</td><td>77</td><td>384</td><td>2021</td><td>117</td><td>18</td></tr></table>

![](Johnson2023Learning_figs/f41e1547d148ac710675ecad68de3848c9807c620c8f7df711b2cbfcd29070d8.jpg)

![](Johnson2023Learning_figs/42c582df0e85d4f5bd29399cd2f2c2495a562f14499e660e60054cb8ef20a91a.jpg)

![](Johnson2023Learning_figs/d1faa797deb0ea94bd9deb761f616a055d247a2d71820be8c2821cce118c231c.jpg)  
Fig. 5. Sample paths planned by the VQ-MPT planner for different robot systems (Left) 2D robot, (Center) 7D robot, and (Right) 14D robot on indistribution environments. The red and green color represents the start and goal states of the robot, respectively. Given an environment with crowded obstacles, VQ-MPT can sample efficiently from learned distributions to find a trajectory.

![](Johnson2023Learning_figs/b1003f76904eb92a9c071066e41398ddd1e4ca4c7e5a122ddc460e69f9df01f4.jpg)  
Fig. 6. Snapshots of a trajectory planning using VQ-MPT for physical panda robot arm for a given start and goal pose on a shelf environment. On the top-right of each image, we show the point cloud data captured using Azure Kinect cameras. We used markerless camera-to-robot pose estimation to localize the captured point cloud in the robot’s reference frame. VQ-MPT can generalize to real-world sensor data without additional training or fine-tuning.

$$
\sum_ {i = 0} ^ {n - 1} \| q _ {i + 1} - q _ {i} \| _ {2} \leq (1 + \epsilon) \sum_ {j = 0} ^ {m - 1} \| q _ {j + 1} ^ {*} - q _ {j} ^ {*} \| _ {2}\tag{10}
$$

where $\mathcal { Q } ^ { * } = \{ q _ { 1 } ^ { * } , \ldots , q _ { n } ^ { * } \}$ is the path planned by VQ-MPT and $\epsilon \geq 0$ is a user-defined threshold. If VQ-MPT could not generate a path for the trajectory, we used a path from RRT<sup>∗</sup> running for 300 seconds (s) to generate Q<sup>∗</sup>. For optimal planners like RRT<sup>∗</sup>, IRRT<sup>∗</sup>, and BIT<sup>∗</sup>, we used $\epsilon \ : = \ : 0 . 1$ and $\epsilon = 0 . 5$ . In our tables, planners that used $\epsilon = 0 . 5$ are reported by ‘X (50%)’, where X is the planner. The planning time reported for VQ-MPT also includes the time taken for model inference. All results are summarized in Table II and the percentage of planning problems solved vs planning time is shown in Figure 4.

We first tested our framework on a simple 2D robot. An example of the path planned by the VQ-MPT framework is shown in Fig. 5 (Left). The cutoff time set was 20 seconds. VQ-MPT showed efficient sampling of points in the planning space and found trajectories faster than traditional planners.

TABLE III  
COMPARING ACCURACY AND MEAN PLANNING TIME AND VERTICES IN OUT-OF-DISTRIBUTION ENVIRONMENTS

<table><tr><td>Robot</td><td></td><td>RRT*</td><td>RRT* (50%)</td><td>IRRT*</td><td>IRRT* (50%)</td><td>BIT*</td><td>BIT* (50%)</td><td>RRT</td><td>MPNet</td><td>VQ-MPT</td></tr><tr><td rowspan="3">7D</td><td>Accuracy</td><td>8.60%</td><td>66.60%</td><td>44.60%</td><td>59.20%</td><td>37.80%</td><td>88.60%</td><td>84.20%</td><td>53.20%</td><td>92.20%</td></tr><tr><td>Time (sec)</td><td>107.75</td><td>22.75</td><td>55.12</td><td>23.94</td><td>75.32</td><td>11.86</td><td>8.88</td><td>10.14</td><td>3.24</td></tr><tr><td>Vertices</td><td>1338</td><td>279</td><td>215</td><td>72</td><td>5147</td><td>896</td><td>477</td><td>310</td><td>306</td></tr><tr><td rowspan="3">14D</td><td>Accuracy</td><td>6.00%</td><td>18.60%</td><td>10.60%</td><td>17.80%</td><td>12.20%</td><td>30.00%</td><td>75.00%</td><td>80.40%</td><td>98.60%</td></tr><tr><td>Time (sec)</td><td>4.92</td><td>7.61</td><td>20.72</td><td>10.57</td><td>30.07</td><td>40.58</td><td>19.75</td><td>23.91</td><td>6.21</td></tr><tr><td>Vertices</td><td>39</td><td>67</td><td>20</td><td>34</td><td>1673</td><td>2889</td><td>179</td><td>104</td><td>70</td></tr><tr><td rowspan="3">7D (Real)</td><td>Accuracy</td><td>·</td><td>·</td><td>100%</td><td>·</td><td>100%</td><td>·</td><td>100%</td><td>30%</td><td>100%</td></tr><tr><td>Time (sec)</td><td>·</td><td>·</td><td>30.68</td><td>·</td><td>26.42</td><td>·</td><td>1.69</td><td>2.23</td><td>1.17</td></tr><tr><td>Vertices</td><td>·</td><td>·</td><td>607</td><td>·</td><td>2852</td><td>·</td><td>21</td><td>7</td><td>34</td></tr></table>

![](Johnson2023Learning_figs/33980f5f7d7b0f1cb42aa8766778186d59fbd8bd350dcceb3e8a9d724e272de3.jpg)  
Fig. 7. Plots of planning time and percentage of paths successfully planned for the 7D (Left) and 14D (Right) robots on environments different from ones used for training. VQ-MPT can reduce the planning space in unseen environments, enabling efficient planning in challenging environments.

VQ-MPT can also use 3D environment representations such as point clouds to generate sampling regions. We evaluated the framework on a 7D panda robot arm with a point cloud environment representation. The dictionary encodings can capture diverse sets of valid configurations in 7D space (Fig. 2). An example of the trajectory planned by the VQ-MPT framework is shown in Fig. 5 (Center). The cutoff time set was 100 s. VQ-MPT planner generates a trajectory nearly 5× faster with fewer vertices than the next best accurate planner. MPNet performs poorly compared to VQ-MPT. The rigid feature encoding of MPNet potentially prevents it from generalizing to larger point cloud data environments. VQ-MPT, in contrast, learns to identify suitable regions to sample in the joint space using point cloud data of different sizes.

We also tested the framework in a bi-manual panda arm setup with 14D. An example of a VQ-MPT trajectory is shown in Fig. 5 (Right). Stage 1 captures the planning space with the same 2048 dictionary values used in the 7D panda experiment. The cutoff time was 250 s. While BIT\* performed relatively well compared to traditional planners for the 2D and 7D problems, performance and accuracy decreased due to the high-dimensional planning space. Since Stage 1 of the VQ-MPT framework encodes self-collisionfree regions, it’s easier for the planner to generate feasible trajectories in Stage 2, resulting in faster trajectory generation with fewer vertices.

## C. Results - Out-of-Distribution Environments

Our next set of experiments evaluated VQ-MPT’s performance for the 7D and 14D robots in environments very different from the training environments. We test our framework on different planning scenes resembling real-world scenarios (Fig. 1). We test the model for each robot on 500 and 10 start and goal locations for simulation and real-world environments, respectively. The cutoff time for each planner was set at 100 s. The results of the experiments are summarized in Table III, and the plot of the percentage of paths solved across planning time is given in Fig. 7. Higher dimensional 7D and 14D spaces are challenging. The environment is even more challenging because of the goal location inside the shelf since it reduces the number of feasible trajectories in the same way a narrow passage eliminates feasible trajectories in mobile robots [38]. Even non-optimal planners like RRT solve only 75-91% of trajectories. Existing optimal SMP planners cannot achieve the same accuracy as VQ-MPT even after relaxing path length constraints.

To evaluate the performance of VQ-MPT on physical sensor data, we tested a trained model in a real-world environment (Fig. 6). The environment was represented using point cloud data from Azure Kinect sensors, and collision checking was done using the octomap collision checker from Moveit <sup>1</sup>. Camera to robot base transform was estimated using markerless pose estimation technique [39]. Our results show that the model can plan trajectories faster than RRT with the same accuracy. We observed that VQ-MPT trajectories are also shorter than RRT trajectories, which can be clearly seen in some of the attached videos. This experiment shows that VQ-MPT models can also generalize well to physical sensor data without further training or finetuning. Such generalization will benefit the larger robotics community since other researchers can use trained models in diverse settings without collecting new data or fine-tuning the model.

## V. CONCLUSION

VQ-MPT can plan near-optimal paths in a fraction of the time required by traditional planners, scales to higher dimension planning space, and achieves better generalizability than previous learning-based planners. Our approach will be beneficial for planning multi-arm robot systems like the ABB Yumi and Intuitive’s da Vinci®Surgical System. It is also helpful for applications where generating nodes and edges for SMPs is computationally expensive, such as for constrained motion planning [40]. Future works will extend VQ-MPT to these applications.

## REFERENCES

[1] S. M. LaValle and J. James J. Kuffner, “Randomized kinodynamic planning,” The International Journal of Robotics Research, 2001.

[2] L. Kavraki, P. Svestka, J.-C. Latombe, and M. Overmars, “Probabilistic roadmaps for path planning in high-dimensional configuration spaces,” IEEE Trans. on Robotics and Auto., 1996.

[3] D. Hsu, T. Jiang, J. Reif, and Z. Sun, “The bridge test for sampling narrow passages with probabilistic roadmap planners,” in IEEE Int. Conf. on Robotics and Auto., 2003.

[4] Z.-Y. Chiu, F. Richter, E. K. Funk, R. K. Orosco, and M. C. Yip, “Bimanual regrasping for suture needles using reinforcement learning for rapid motion planning,” in IEEE Int. Conf. on Robotics and Auto., 2021.

[5] R. Alterovitz, K. Goldberg, and A. Okamura, “Planning for steerable bevel-tip needle insertion through 2d soft tissue with obstacles,” in Proceedings of the IEEE Int. Conf. on Robotics and Auto., 2005.

[6] J. D. Gammell, S. S. Srinivasa, and T. D. Barfoot, “Informed RRT\*: Optimal sampling-based path planning focused via direct sampling of an admissible ellipsoidal heuristic,” in Int. Conf. on Intelligent Robots and Systems, 2014.

[7] ——, “Batch informed trees (BIT\*): Sampling-based optimal planning via the heuristically guided search of implicit random geometric graphs,” in 2015 IEEE Int. Conf. Robot. Autom., 2015.

[8] A. H. Qureshi and Y. Ayaz, “Potential functions based sampling heuristic for optimal path planning,” Autonomous Robots, 2016.

[9] Z. Tahir, A. H. Qureshi, Y. Ayaz, and R. Nawaz, “Potentially guided bidirectionalized rrt\* for fast optimal path planning in cluttered environments,” Robotics and Autonomous Systems, 2018.

[10] P. Lehner and A. Albu-Schaffer, “The repetition roadmap for repetitive¨ constrained motion planning,” IEEE Robot. and Autom. Letters, 2018.

[11] C. Chamzas, Z. Kingston, C. Quintero-Pena, A. Shrivastava, and L. E.˜ Kavraki, “Learning sampling distributions using local 3d workspace decompositions for motion planning in high dimensions,” in IEEE Int. Conf. on Robot. and Autom., 2021.

[12] B. Ichter and M. Pavone, “Robot motion planning in learned latent spaces,” IEEE Robotics and Auto. Letters, 2019.

[13] R. Kumar, A. Mandalika, S. Choudhury, and S. Srinivasa, “Lego: Leveraging experience in roadmap generation for sampling-based planning,” in Int. Conf. on Intelligent Robots and Systems, 2019.

[14] A. H. Qureshi, Y. Miao, A. Simeonov, and M. C. Yip, “Motion planning networks: Bridging the gap between learning-based and classical motion planners,” IEEE Trans. on Robotics, 2020.

[15] J. J. Johnson, U. S. Kalra, A. Bhatia, L. Li, A. H. Qureshi, and M. C. Yip, “Motion planning transformers: A motion planning framework for mobile robots,” 2021.

[16] B. Chen, B. Dai, Q. Lin, G. Ye, H. Liu, and L. Song, “Learning to plan in high dimensions via neural exploration-exploitation trees,” in Int. Conf. on Learning Representations, ICLR, 2020.

[17] C. Yu and S. Gao, “Reducing collision checking for sampling-based motion planning using graph neural networks,” in Advances in Neural Information Processing Systems, 2021.

[18] A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A. N. Gomez, L. u. Kaiser, and I. Polosukhin, “Attention is all you need,” in Advances in Neural Information Processing Systems, 2017.

[19] J. Devlin, M. Chang, K. Lee, and K. Toutanova, “BERT: pre-training of deep bidirectional transformers for language understanding,” in Proceedings of the Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, 2019.

[20] T. Brown, B. Mann, N. Ryder, M. Subbiah, J. D. Kaplan, P. Dhariwal, A. Neelakantan, P. Shyam, G. Sastry, A. Askell, S. Agarwal, A. Herbert-Voss, G. Krueger, T. Henighan, R. Child, A. Ramesh, D. Ziegler, J. Wu, C. Winter, C. Hesse, M. Chen, E. Sigler, M. Litwin, S. Gray, B. Chess, J. Clark, C. Berner, S. McCandlish, A. Radford, I. Sutskever, and D. Amodei, “Language models are few-shot learners,” in Advances in Neural Information Processing Systems, 2020.

[21] L. Chen, K. Lu, A. Rajeswaran, K. Lee, A. Grover, M. Laskin, P. Abbeel, A. Srinivas, and I. Mordatch, “Decision transformer: Reinforcement learning via sequence modeling,” in Advances in Neural Information Processing Systems, 2021.

[22] M. Janner, Q. Li, and S. Levine, “Offline reinforcement learning as one big sequence modeling problem,” in Advances in Neural Information Processing Systems, 2021.

[23] R. Yang, M. Zhang, N. Hansen, H. Xu, and X. Wang, “Learning vision-guided quadrupedal locomotion end-to-end with cross-modal transformers,” in Int. Conf. on Learning Representations, 2022.

[24] D. S. Chaplot, D. Pathak, and J. Malik, “Differentiable spatial planning using transformers,” in ICML, 2021.

[25] A. van den Oord, O. Vinyals, and k. kavukcuoglu, “Neural discrete representation learning,” in Advances in Neural Information Processing Systems, 2017.

[26] J. Yu, X. Li, J. Y. Koh, H. Zhang, R. Pang, J. Qin, A. Ku, Y. Xu, J. Baldridge, and Y. Wu, “Vector-quantized image modeling with improved VQGAN,” in Int. Conf. on Learning Representations, 2022.

[27] Z. Lin, M. Feng, C. N. dos Santos, M. Yu, B. Xiang, B. Zhou, and Y. Bengio, “A structured self-attentive sentence embedding,” in Int. Conf. on Learning Representations, 2017.

[28] A. Dosovitskiy, L. Beyer, A. Kolesnikov, D. Weissenborn, X. Zhai, T. Unterthiner, M. Dehghani, M. Minderer, G. Heigold, S. Gelly, J. Uszkoreit, and N. Houlsby, “An image is worth 16x16 words: Transformers for image recognition at scale,” in Int. Conf. on Learning Representations, 2021.

[29] R. Xiong, Y. Yang, D. He, K. Zheng, S. Zheng, C. Xing, H. Zhang, Y. Lan, L. Wang, and T. Liu, “On layer normalization in the transformer architecture,” in Int. Conf. on Machine Learning, 2020.

[30] A. Razavi, A. van den Oord, and O. Vinyals, “Generating diverse highfidelity images with vq-vae-2,” in Advances in Neural Information Processing Systems. Curran Associates, Inc., 2019.

[31] H. Hu and G. Kantor, “Parametric covariance prediction for heteroscedastic noise,” in Int. Conf. on Intelligent Robots and Systems (IROS), 2015.

[32] K. Liu, K. Ok, W. Vega-Brown, and N. Roy, “Deep inference for covariance estimation: Learning gaussian noise models for state estimation,” in 2018 IEEE Int. Conf. on Robotics and Auto. (ICRA), 2018, pp. 1436–1443.

[33] C. Dugas, Y. Bengio, F. Belisle, C. Nadeau, and R. Garcia, “Incorpo- ´ rating second-order functional knowledge for better option pricing,” in Advances in Neural Information Processing Systems, 2000.

[34] I. A. S¸ ucan, M. Moll, and L. E. Kavraki, “The Open Motion Planning Library,” IEEE Robotics & Auto. Magazine, 2012.

[35] C. R. Qi, L. Yi, H. Su, and L. J. Guibas, “Pointnet++: Deep hierarchical feature learning on point sets in a metric space,” in Advances in Neural Information Processing Systems, 2017.

[36] D. P. Kingma and J. Ba, “Adam: A method for stochastic optimization,” in Int. Conf. on Learning Representations, 2015.

[37] N. Das and M. Yip, “Learning-based proxy collision detection for robot motion planning applications,” IEEE Trans. on Robotics, 2020.

[38] J. Borenstein and Y. Koren, “The vector field histogram-fast obstacle avoidance for mobile robots,” IEEE Trans. on Robotics and Auto., 1991.

[39] J. Lu, F. Richter, and M. C. Yip, “Markerless camera-to-robot pose estimation via self-supervised sim-to-real transfer,” 2023.

[40] J. J. Johnson and M. C. Yip, “Chance-constrained motion planning using modeled distance- to-collision functions,” in Int. Conf. on Auto. Science and Engineering (CASE), 2021.