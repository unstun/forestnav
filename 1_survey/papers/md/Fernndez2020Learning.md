---
citation_key: Fernndez2020Learning
arxiv_id: 2006.07746
arxiv_url: https://arxiv.org/abs/2006.07746
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-24T16:45:07Z
origin: ai+web
reviewed: false
---

# Introduction {#sec:introduction}

Many practical robotic applications require planning robot motions with constraints, such as maintaining an orientation or reaching a particular location. Planning becomes more complicated when the task consists of many subtasks that must be completed in sequence. In this case, task and motion planning frameworks [@kaelbling2013integrated; @dantam2016incremental; @konidaris2018skills; @toussaint2018differentiable; @dantam2018task; @barry2013hierarchical; @cambon2009hybrid] can be used to handle long planning horizons and a wide range of tasks. However, some constraints may be difficult to describe analytically, or it may be difficult to sample constraints that adhere to them. For example, if the task is to pour a liquid from a bottle into a cup, it is not immediately clear how to encode the motion constraints for a planning algorithm.

In this work, we focus on learning constraint manifolds for use in constrained motion planning algorithms [@englert2020sampling; @stilman2010global; @berenson2011task; @jaillet2013asymptotically; @kim2016tangent; @kingston2019ijrr; @csucan2012motion; @cortes2004sampling]. To this end, we investigate two different approaches: Variational autoencoders (VAE) following @kingma2013AutoEncodingVB, and Equality Constraint Manifold Neural Network (ECoMaNN), a method we propose which learns the implicit function value of equality constraints. We evaluate these techniques on six datasets of varying size and complexity, and we present preliminary resulting motion plans.

# Background on Sequential Manifold Planning {#sec:background}

We focus on learning manifolds that describe kinematic robot tasks. We aim to integrate these learned manifolds into the sequential manifold planning (SMP) framework proposed in @englert2020sampling. SMP considers kinematic motion planning problems in a configuration space $\mathcal{C}\subseteq \mathbb{R}^{d}$. A robot configuration $\mathbf{q}\in \mathcal{C}$ describes the state of one or more robots with $d$ degrees of freedom in total. A manifold $M$ is represented as an equality constraint ${h}_{M}(\mathbf{q}) = \boldsymbol{0}$ where ${h}_{M}: \mathbb{R}^{d} \rightarrow \mathbb{R}^{l}$ and $l$ is the dimensionality of the implicit manifold. The set of robot configurations that are on a manifold $M$ is given by ${\mathcal{C}}_{M}= \{ \mathbf{q}\in \mathcal{C}\mid {h}_{M}(\mathbf{q}) = \boldsymbol{0} \}~.$ SMP defines the planning problem as a sequence of $(n+1)$ such manifolds $\mathcal{M} = \{M_1, M_2, \dots, M_{n+1}\}$ and an initial configuration $\mathbf{q}_{\textrm{start}} \in \mathcal{C}_{{M}_1}$ that is on the first manifold. The goal is to find a path from $\mathbf{q}_{\textrm{start}}$ that traverses the manifold sequence $\mathcal{M}$ and reaches a configuration on the goal manifold $M_{n+1}$. A path on the $i$-th manifold is defined as $\tau_i : [0, 1] \to {{\mathcal{C}}_{M}}_{i}$ and $J(\tau_i)$ is the cost function of a path $\mathcal{J}: \mathcal{T}\to \mathbb{R}_{\geq 0}$ where $\mathcal{T}$ is the set of all non-trivial paths. The problem is formulated as an optimization over a set of paths $\boldsymbol{\tau}= (\tau_1, \dots, \tau_{n})$ that minimizes the sum of path costs under the constraints of traversing $\mathcal{M}$ and of being collision-free: $$\begin{align}
 %
	\begin{alignedat}{2} %	
	\label{eq:smp_problem}
	&\boldsymbol{\tau}^{\star} = \operatorname*{arg\:min}_{\boldsymbol{\tau}} \sum_{i=1}^{n} J(\tau_i) &&\\
	{\textrm{s.t.}}\quad &{\tau}_1 (0) = {\mathbf{q}}_{\textrm{start}} &\\
	&\tau_i(1) = \tau_{i+1}(0)  &&\forall_{i=1,\dots,n-1} \\ 
	&\mathcal{C}_{{\textrm{free}}, i+1} = \Upsilon(\mathcal{C}_{{\textrm{free}}, i}, \tau_{i})~~~~ &&\forall_{i=1,\dots,n}\\
	&\tau_i(s) \in {{\mathcal{C}}_{M}}_{i} \cap \mathcal{C}_{{\textrm{free}}, i} &&\forall_{i=1,\dots,n}~ \forall_{s \in [0, 1]}\\
	&\tau_{n}(1) \in {{\mathcal{C}}_{M}}_{n+1} \cap \mathcal{C}_{{\textrm{free}}, n+1} &&
	\end{alignedat} %
\end{align}$$ $\Upsilon$ is an operator that describes the change in the free configuration space (the space of all configurations that are not in collision with the environment) $\mathcal{C}_{\textrm{free}}$ when transitioning to the next manifold. The SMP algorithm is able to solve this problem for a certain class of problems. It iteratively applies RRT${}^\star$ to find a path that reaches the next manifold while staying on the current manifold. For further details of the SMP algorithm, we refer the reader to @englert2020sampling.

In this paper, we employ data-driven algorithms to learn manifolds $M$ from data with the goal to integrate them into the SMP framework.

# Manifold Learning {#sec:manifold_learning}

Learning constraint manifolds from data is attractive for multiple reasons. For example, it may be easier for a human to demonstrate a task rather than specifying constraints analytically, or we may want to reduce the amount of expert information needed.

We propose a novel neural network structure -- called *Equality Constraint Manifold Neural Network* (ECoMaNN) -- to become a learning representation that takes $\mathbf{q}$ as input and outputs the prediction of the implicit function ${h}_{M}(\mathbf{q})$. Moreover, we would like to train ECoMaNN in a supervised manner, from demonstrations. One of the challenges is that the supervised training dataset is collected *only* from demonstrations of data points which are on the equality constraint manifold ${\mathcal{C}}_{M}$, called the *on-manifold* dataset. This is a reasonable assumption, since collecting both the on-manifold ${\mathcal{C}}_{M}$ and off-manifold ${\mathcal{C}}_{\cancel{M}}= \{ \mathbf{q}\in \mathcal{C}\mid {h}_{M}(\mathbf{q}) \neq \boldsymbol{0} \}$ datasets for supervised training will be tedious because the implicit function ${h}_{M}$ values of points in ${\mathcal{C}}_{\cancel{M}}$ are typically unknown and hard to label. We will show that even though our approach is only provided with data on ${\mathcal{C}}_{M}$, it can still learn a useful representation of the manifold, sufficient for use in the SMP framework.

Our goal is to learn a single global representation of the constraint manifold in form of a neural network. A manifold can be defined as a collection of local neighborhoods which resemble Euclidean spaces (@Lee00_IntroToSmoothManifolds). Therefore, a global representation of the manifold can be developed by constructing characterizations for its Euclidean-like local neighborhoods.

Our approach leverages local information on the manifold in the form of the tangent and normal spaces (@Deutsch2015_TensorVotingGraph [@GStrangIntroLinearAlgebra]). With regard to ${h}_{M}$, the tangent and normal spaces are equivalent to the null and row space, respectively, of the matrix $\mathbf{J}_M= \left. \frac{\partial {h}_{M}({\mathbf{q}})}{\partial {\mathbf{q}}}\right|_{{\mathbf{q}} = \Bar{\mathbf{q}}}$, and valid in a small neighborhood around the point $\Bar{\mathbf{q}}$.

Using on-manifold data, the local information of the manifold can be analyzed using Local Principal Component Analysis (Local PCA) (@Kambhatla_LocalPCA). Essentially, for each data point $\mathbf{q}$ in the on-manifold dataset, we establish a local neighborhood using $K$-nearest neighbors ($K$NN) $\hat{\mathcal{K}}= \{\hat{\mathbf{q}}_1, \hat{\mathbf{q}}_2, \dots \hat{\mathbf{q}}_K\}$, with $K\geq d$. After a change of coordinates, $\mathbf{q}$ becomes the origin of a new local coordinate frame $\mathcal{F}$, and the $K$NN becomes $\tilde{\mathcal{K}}= \{\tilde{\mathbf{q}}_1, \tilde{\mathbf{q}}_2, \dots \tilde{\mathbf{q}}_K\}$ with $\tilde{\mathbf{q}}_k= \hat{\mathbf{q}}_k- \mathbf{q}$ for all values of $k$. Defining the matrix $\mathbf{X}= 
\begin{bmatrix} 
\tilde{\mathbf{q}}_1 & \tilde{\mathbf{q}}_2 & \hdots & \tilde{\mathbf{q}}_K\\
\end{bmatrix}^{\textrm T}\in \mathbb{R}^{K\times d}$, we can compute the covariance matrix $\mathbf{S}= \frac{1}{K-1} \mathbf{X}^{\textrm T}\mathbf{X}\in \mathbb{R}^{d\times d}$. The eigendecomposition of $\mathbf{S}= \mathbf{V}\mathbf{\Sigma}\mathbf{V}^{\textrm T}$ gives us the Local PCA. The matrix $\mathbf{V}$ contains the eigenvectors of $\mathbf{S}$ as its columns in decreasing order w.r.t. the corresponding eigenvalues in the diagonal matrix $\mathbf{\Sigma}$. These eigenvectors form the basis of $\mathcal{F}$.

This local coordinate frame $\mathcal{F}$ is tightly related to the tangent and normal spaces of the manifold at $\mathbf{q}$. That is, the $(d- l)$ eigenvectors corresponding to the $(d- l)$ biggest eigenvalues of $\mathbf{\Sigma}$ form a basis of the tangent space, while the remaining $l$ eigenvectors form the basis of the normal space. Furthermore, due to the characteristics of the manifold from which the dataset was collected, the $l$ smallest eigenvalues of $\mathbf{\Sigma}$ will be close to zero, resulting in the $l$ eigenvectors associated with them forming the basis of the null space of $\mathbf{S}$. On the other hand, the remaining $(d- l)$ eigenvectors form the basis of the row space of $\mathbf{S}$.

To this end, we present several methods to define and train ECoMaNN, as follows:

## Local Tangent and Normal Spaces Alignment

ECoMaNN aims to align the following:

(a) the null space of $\mathbf{J}_M$ and the row space of $\mathbf{S}$, which both must be equivalent to the tangent space, and

(b) the row space of $\mathbf{J}_M$ and the null space of $\mathbf{S}$, which both must be equivalent to the normal space

for each local neighborhood of each point $\mathbf{q}$ in the on-manifold dataset. Suppose the eigenvectors of $\mathbf{S}$ are $\{\boldsymbol{v}_1, \boldsymbol{v}_2, \dots, \boldsymbol{v}_d\}$ and the singular vectors of $\mathbf{J}_M$ are $\{\boldsymbol{e}_1, \boldsymbol{e}_2, \dots, \boldsymbol{e}_d\}$, where the indices indicate the decreasing order w.r.t. the eigenvalue/singular value magnitude. The null spaces of $\mathbf{S}$ and $\mathbf{J}_M$ are spanned by $\{\boldsymbol{v}_{d-l+1}, \dots, \boldsymbol{v}_d\}$ and $\{\boldsymbol{e}_{l+1}, \dots, \boldsymbol{e}_d\}$, respectively. The two conditions above imply that the projection of the null space eigenvectors of $\mathbf{J}_M$ into the null space of $\mathbf{S}$ should be $\boldsymbol{0}$, and similarly for the row spaces. Hence, we achieve this by training ECoMaNN to minimize projection errors $\@ifstar{\norm}{\norm*}{\mathbf{V}_{\text{N}}\mathbf{V}_{\text{N}}^{\textrm T}\mathbf{E}_{\text{N}}}_2^2$ and $\@ifstar{\norm}{\norm*}{ \mathbf{E}_{\text{N}}\mathbf{E}_{\text{N}}^{\textrm T}\mathbf{V}_{\text{N}}}_2^2$ with $\mathbf{V}_{\text{N}}= 
\begin{bmatrix}
    \boldsymbol{v}_{d-l+1} & \dots & \boldsymbol{v}_d
\end{bmatrix}$ and $\mathbf{E}_{\text{N}}=  
\begin{bmatrix}
    \boldsymbol{e}_{l+1} & \dots & \boldsymbol{e}_d
\end{bmatrix}$.

## Data Augmentation with Off-Manifold Data

The training dataset is on-manifold, i.e., each point $\mathbf{q}$ in the dataset satisfies ${h}_{M}(\mathbf{q}) = \boldsymbol{0}$. Through Local PCA on each of these points, we know the data-driven approximation of the normal space of the manifold at $\mathbf{q}$. Hence, we know the directions where the violation of the equality constraint increases, i.e., the same or opposite direction of any vector from the approximate normal space. Since our future use of the learned constraint manifold on motion planning does not require the acquisition of the near-ground-truth value of ${h}_{M}(\mathbf{q}) \neq \boldsymbol{0}$, we can set this off-manifold valuation of ${h}_{M}$ arbitrarily, as long as it does not interfere with the utility for projecting an off-manifold point onto the manifold. Therefore, we can augment our dataset with additional off-manifold data to achieve a more robust learning of ECoMaNN. For each point $\mathbf{q}$ in the on-manifold dataset, and for each eigenvector $\boldsymbol{v}$ that forms the basis of the normal space at $\mathbf{q}$, we can add an off-manifold point $\check{\mathbf{q}}= \mathbf{q}+ i\epsilon\boldsymbol{v}$ with a non-zero signed integer $i$ and a small positive scalar $\epsilon$. For such an augmented data point $\check{\mathbf{q}}$, we set the label satisfying $\@ifstar{\norm}{\norm*}{{h}_{M}(\check{\mathbf{q}})}_2 = \@ifstar{\abs}{\abs*}{i} \epsilon$. During training, we minimize the prediction error $\@ifstar{\norm}{\norm*}{(\@ifstar{\norm}{\norm*}{{h}_{M}(\check{\mathbf{q}})}_2 - \@ifstar{\abs}{\abs*}{i} \epsilon)}_2^2$ for each augmented point $\check{\mathbf{q}}$.

# Datasets {#sec:datasets}

We use a robot simulator (@todorov2012mujoco) to generate various datasets. For each dataset, we define ${h}_{M}(\mathbf{q})$ by hand and randomly sample points in the configuration space and project them onto the manifold. We use six datasets:

- **Nav**: 2D point that has to stay close to a reference point. Defined as an inequality constraint. $N=15000$.

- **Sphere**: 3D point that has to stay on the surface of a sphere. $N=10000$.

- **Plane**: Robot arm with 3 rotational DOFs where the end effector has to be on a plane. $N=999$.

- **Orient**: Robot arm with 6 rotational DOFs that has to keep its orientation upright (e.g., transporting a cup). $N=21153$.

- **Tilt**: Same as Orient, but here the orientation constraint is relaxed to an inequality constraint. $N=2000$.

- **Handover**: Robot arm with 6 rotational DOFs and a mobile base with 2 translational DOFs. The manifold is defined as an equality constraint that describes the handover of an object between the two robots. $N=2002$.

# Experiments {#sec:experiments}

We compare the proposed ECoMaNN method to a Variational Autoencoder (VAE), which is a popular method for learning a generative model of a set of data (@chen2016dynamic [@kingma2013AutoEncodingVB; @park2018multimodal]). Importantly, because they embed data points as a distribution in the latent space, new latent vectors can be sampled and decoded into unseen examples which fit the distribution of the training data. VAEs make use of two neural networks in a neural autoencoder structure during training, and they only use the decoder during generation. The key idea that makes VAEs computationally tractable is that the distribution in the latent space is assumed to be Gaussian. The loss function is a combination of the reconstruction error of the input and the KL divergence of the latent space distribution, weighted by a parameter $\beta$.

We use the following network structures and parameters: For the Nav dataset, the VAE has two hidden layers with 6 and 4 units. The input size is 2 and the embedding size is 2. For the Plane dataset, the VAE has three hidden layers with 12, 9, and 6 units. The input size is 3 and the embedding size is 2. For the Sphere, Orient, Tilt, and Handover datasets, the VAEs have the same structure: Four hidden layers with 8, 6, 6, and 4 units. The input sizes to the networks are 3, 6, 6, and 8, and the embedding sizes are 2, 5, 3, and 7, respectively. All VAE models have $\beta$ = 0.25 and use batch normalization. We train for 500 epochs for Handover, and 200 otherwise.

## Evaluate Implicit Functions on Datasets {#sec:experiment1}

We compare the performance of the models using the implicit function value ${h}_{M}$. In the case of the VAE models, we take the reprojected data $\hat{X}$ and evaluate each configuration with ${h}_{M}$. In the case of the ECoMaNN, the output of the network is the estimated implicit function value of the input, so we can directly use it. We report the mean and standard deviation of ${h}_{M}$ for each dataset in Table [\[table:experiment1\]](#table:experiment1){reference-type="ref" reference="table:experiment1"}. Note that for Nav and Tilt datasets, $h_M$ does not need to be 0 for a configuration to be valid, since these are inequality constraints. Values less than 1 for Nav and less than 0.1 for Tilt adhere to the constraints.

In Fig. [1](#sfig:levelset_contour_and_jac_vector_field){reference-type="ref" reference="sfig:levelset_contour_and_jac_vector_field"}, we plot the level set contour as well as the normal space eigenvector field of an ECoMaNN after training on a 3D unit sphere constraint dataset. We see that at both cross-sections $y=0$ (left) and $z=0$ (right), the contours are close to circular, which is expected for a unit sphere constraint manifold.

:::: {#sfig:hourglass_learned .figure}
![Level set contour plot and the learned ECoMaNN's normal space eigenvector field, after training on a 3D unit sphere constraint dataset.](Fernndez2020Learning_figs/contourplot_ltsann_epoch_25.png){#sfig:levelset_contour_and_jac_vector_field width="\\columnwidth"}

![Visualization of a planned path on a learned manifold (sphere).](Fernndez2020Learning_figs/hourglass_learned.png){#sfig:hourglass_learned width="\\columnwidth"}

::: caption
Visualization of a planned path on a learned manifold (sphere).
:::
::::

## Evaluate Implicit Functions on Generated Configurations {#sec:experiment2}

We use the trained VAE models from Sec. [5.1](#sec:experiment1){reference-type="ref" reference="sec:experiment1"} to generate 100,000 new, on-manifold configurations for each constraint. We then evaluate these configurations with the implicit function $h_M$ and report the mean and standard deviation in Table [\[table:experiment2\]](#table:experiment2){reference-type="ref" reference="table:experiment2"}.

## Sequential Motion Planning on Learned Manifolds {#sec:experiment3}

In this experiment, we incorporate a learned manifold into the planning framework developed and introduced in @englert2020sampling. The Sphere dataset (see Section [4](#sec:datasets){reference-type="ref" reference="sec:datasets"}) is used to learn a manifold representation with ECoMaNN. This learned manifold is combined with two analytical manifolds representing paraboloids. A motion planning problem is defined on these three manifolds where a 3D point has to find a path from a start configuration on one of the paraboloids to a goal configuration on the other. See Figure [3](#sfig:hourglass_learned){reference-type="ref" reference="sfig:hourglass_learned"} for a visualization of the manifolds and a found path with SMP.

# Discussion and Future Work {#sec:discussion}

In this paper, we presented ways of learning constraint manifolds for sequential manifold planning. One of them is the novel Equality Constraint Manifold Neural Network (ECoMaNN). ECoMaNN is a method for learning representation for implicit functions, with an emphasis on representing equality constraints, while VAEs can also learn inequality constraints. We showed that ECoMaNN has successfully learned equality constraint manifolds and that these manifolds can be used in a sequential motion planning method.

There are several interesting improvements and future directions to pursue. First, there are still limitations with the current approach; in particular, our approach does not address the sign/polarity assignments of the implicit function value output, which we plan to address. Second, we plan to do more comprehensive testing on higher-dimensional manifolds, and incorporate multiple learned constraints into a single motion plan with more subtasks. Further, we also plan to integrate manifolds learned with VAE into motion planning algorithms.

[^1]: equal contribution

[^2]: All authors are with the Robotic Embedded Systems Laboratory, University of Southern California, Los Angeles, CA, USA.

[^3]: This material is based upon work supported by the National Science Foundation Graduate Research Fellowship Program under Grant No. DGE-1842487. Any opinions, findings, and conclusions or recommendations expressed in this material are those of the author(s) and do not necessarily reflect the views of the National Science Foundation. This work was supported in part by the Office of Naval Research (ONR) under grant N000141512550.
