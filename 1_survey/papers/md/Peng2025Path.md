---
citation_key: Peng2025Path
arxiv_id: 2502.03540
arxiv_url: "https://arxiv.org/abs/2502.03540"
title: "Path Planning for Masked Diffusion Model Sampling"
authors_short: "Fred Zhangzhi Peng et al."
year: 2025
direction_tag: L_learning_path_optimization
source: mineru-vlm
converter: mineru-open-api
model: vlm
converted_at: 2026-06-25T09:18:35Z
origin: ai+web
reviewed: false
---

# Path Planning for Difusion Language Model Sampling

Fred Zhangzhi Peng<sup>1,∗,‡</sup>, Zachary Bezemek<sup>1,∗</sup>, Sawan Patel<sup>2</sup>, Jarrid Rector-Brooks<sup>3,4</sup>, Sherwood Yao<sup>2</sup>, Avishek Joey Bose<sup>3,5</sup>, Alexander Tong<sup>3,4,6,†,‡</sup>, Pranam Chatterjee<sup>7,†,‡</sup>

<sup>1</sup>Duke University, <sup>2</sup>Atom Bioworks, <sup>3</sup>Mila – Québec AI Institute,

<sup>4</sup>Université de Montréal, <sup>5</sup>The University of Oxford, <sup>6</sup>Aithyra, <sup>7</sup>University of Pennsylvania <sup>∗</sup>Equal contribution, <sup>†</sup>Equal co-supervision

<sup>‡</sup>Corresponding authors: zp70@duke.edu, atong@aithyra.at, pranam@seas.upenn.edu

## Abstract

Any order generation of discrete data using masked difusion language models (MDMs) ofers a compelling alternative to traditional autoregressive models, especially in domains that lack a natural causal ordering of data. However, current popular MDMs depart from their successful continuous difusion model counterparts with simplified masked inference wherein unmasked tokens cannot be iteratively refined—even if there is a mistake. In this paper, we extract the full power of MDMs by introducing a novel inference sampling strategy termed Path Planning (P2) that decomposes each generation step into two sub-stages: planning and denoising. Under P2, the planner at every step selects appropriate tokens that are marked to be updated, which can then be sampled using the denoiser. We demonstrate that P2 generalizes all existing sampling strategies for MDMs and critically enhances generative quality through the new capability of refining and updating existing unmasked tokens. We theoretically prove that P2 establishes a (new) expanded evidence lower bound (ELBO) on the log marginal likelihood of data. We instantiate P2 with a family of planners including: 1.) Self-Planning, 2.) BERT-Planning, and 3.) Trained-Planning with a learned planner leading to SOTA generative performance for MDMs on a suite of domains. Specifically, solely using P2 inference, we observe relative improvements of 22% in protein sequence foldability, 8% in RNA sequence pLDDT, 4% in math reasoning, 68% in story generation (ROUGE score), and 33% in code generation for the challenging pass@1 metric.

## 1 Introduction

Difusion models in continuous domains are currently the most popular generative modeling family, with state-of-the-art sample quality across the entire AI spectrum of applications (Watson et al., 2023; Rombach et al., 2022). The success of the difusion framework in continuous spaces, comparatively, raises the possibility of having similarly expressive models that can also operate on discrete data domains. Despite the appeal of discrete difusion models, which are arguably a more natural for certain discrete domains—e.g., biological sequences—that do not have a causal ordering, the most successful discrete generative models are autoregressive models (Achiam et al., 2023). One key reason that drives this gap is that, despite the generality of accommodating a multitude of noising processes, most successful discrete difusion approaches have converged to absorbing state difusion (Austin et al., 2021; Lou et al., 2023) (MDMs). Moreover, while considerable efort has focused on improving training for MDMs (Sahoo et al., 2024; Shi et al., 2024; Gat et al., 2024; Shi et al., 2024), resulting in new, simple, and scalable training recipes, considerably less attention has been devoted to unlocking their full potential at inference—which is limited to simple uniform denoising. This raises a question: Can we design new inference strategies for MDMs to improve generative quality?

Current work. In this paper, we answer the above research question afirmatively by investigating how the order in which tokens are unmasked during MDM inference afects generative quality. We motivate our investigation by making the critical observation that, while the MDM reverse process requires that each token is uniformly likely to be unmasked at a given step, this correctly reconstructs the true data distribution only under a perfect denoiser. However, since any trained MDM is inherently imperfect due to the nature of training and convergence in non-convex optimization, it has been empirically observed that a uniformly random unmasking order is suboptimal in many settings (Ou et al., 2024; Shih et al., 2022; Li et al., 2021). Moreover, in current MDM inference it is not possible to course-correct incorrectly denoised tokens at future steps during inference, which leads to error propagation and overall suboptimal generative quality.

We begin our study by reexamining the typical MDM ELBO and show that, for a fixed denoiser, we can expand the ELBO to include two additional terms, both involving a “planner” whose role is to select which tokens should be unmasked at a given inference step as well as optionally choosing already unmasked tokens to be resampled (see Figure 1). Our ELBO shows that while the optimal planner for the optimal denoiser is indeed uniform unmasking, the strategy prescribed by the reverse process, one can obtain better generative quality for an imperfect denoiser through the use of a non-uniform planner.

Main contributions. These observations lead to our proposed method, Path Planning (P2), which makes use of the expanded ELBO to introduce a family of planners for use at inference time.

Crucially, by noting the similarity between the planner ELBO terms and the typical MLM objective, we show that in practice we can obtain efective planners by employing either pre-trained BERT-type models, training a light-weight planner ofline, or simply using the already trained denoiser. Moreover, we show that P2 generalizes all known existing sampling strategies in the MDM literature (see Table 1). We validate our P2 framework across a diverse set of experimental settings, showing that by using P2, a 1B parameter MDM model can outperform a 7B Llama model in math reasoning while far outpacing state-of-the-art ARMs for code generation on the same-sized models. At the same time, for biological sequence design, we show that the combination of P2 and DPLM (Wang et al., 2024) leads to state-of-the-art generation quality for proteins. Finally, for RNA design,

![](Peng2025Path_figs/77d7b64e07ea2d40ad5c74d09cef2e2d8a228e1de15872fe787d5190da2ed14d.jpg)  
Figure 1: Illustration of P2 sampling (Algorithm 1). At each step, the denoiser D<sub>θ</sub> predicts z, and the planner $G _ { \phi }$ selects positions to unmask (green) and remask (red).

we outperform all prior models and observe that our sequences lead to higher structural plausibility than even true, naturally occurring sequences.

## 2 Background and preliminaries

Notation. Let $\mathcal { V } = \{ 1 , \ldots , d \}$ be a finite vocabulary set. We designate the final element of this set to a specialized mask token $d = \mathbf { m }$ , whereas the remaining d−1 elements in V form the categories found in a typical vocabulary set. We are interested in generating sequences of length L from V. A discrete data sample x is then a realization of a category in $\mathcal { V } ^ { L }$ . Let $\Delta ^ { d } : = \{ \bar { v } \in \mathbb { R } ^ { d } : v ^ { i } \geq 0 , i = 1 , \ldots , d , \sum _ { i = 1 } ^ { d } v ^ { i } = 1 \}$ represent the d-dimensional probability simplex. Each point on $u \in \Delta ^ { d }$ corresponds to a categorical distribution $\mathrm { C a t } ( j ; u ) = u ^ { j } { \mathrm { ~ f o r ~ } } j \in \mathcal { V }$ We write a discrete sequence of length L as $\mathbf { x } = ( \bar { x } ^ { 1 } , \dots , x ^ { L } ) \in \mathcal { V } ^ { \bar { L } }$ . The data distribution p<sub>data</sub> is provided as an empirical distribution on n sequences in the form of a training set $\mathcal { D } = \{ \mathbf { x } \} ^ { n } \subset \mathcal { V } ^ { L }$ . We further use boldface x to denote the entire sequence and normal script to indicate an individual token. We denote for $x \in \mathcal { V } , \delta ( x ) \in \Delta ^ { d }$ given by $\operatorname { C a t } ( j ; \delta ( x ) ) = 1 { \mathrm { ~ i f ~ } } j = x$ and 0 otherwise. Finally, we reserve superscripts for set indexing purposes, $\mathrm { e . g . ~ } x ^ { i } , i \in [ d ]$ , while subscripts are used to represent positions in time of a discrete sample $x _ { t } , t \in [ 0 , 1 ]$

## 2.1 Masked Discrete Difusion Models

We can define difusion models on discrete spaces by constructing a forward noising process that progressively converts the data distribution $\mathbf { p } _ { \mathrm { d a t a } }$ to a structureless prior. Without loss of generality, let $\mathbf { p } _ { 0 } ( \mathbf { x } ) : = \mathbf { p } _ { \mathrm { d a t a } } ( \mathbf { x } )$ be the data distribution at time $t = 0$ and let $\mathbf { p } _ { 1 } : = [ \delta ( \mathbf { m } ) ] ^ { n }$ the prior which consists of a fully masked sequence. For simplicity of exposition, we consider a discretization of time into $T$ sub-intervals, i.e. $t ( i ) = i / T$ . This enables the specification of the forward corruption process using a noising kernel $\mathbf { p } _ { t } ( \mathbf { x } _ { t } | \mathbf { x } _ { 0 } )$ . One of the most popular forward-noising processes (Sahoo et al., 2024; Gat et al., 2024; Shi et al., 2024; Zhao et al., 2024a) is the socalled “simplified masked" process, which corrupts each unmasked token $x _ { t } ^ { i } \neq \mathbf { m }$ in a sequence independently:

$$
\mathbf {p} _ {t} (\mathbf {x} _ {t} | \mathbf {x} _ {0}) = \prod_ {i = 1} ^ {L} p _ {t} (x _ {t} ^ {i} | x _ {0} ^ {i}) = \prod_ {i = 1} ^ {L} \mathrm{Cat} (x _ {t} ^ {i}; \alpha_ {t} \delta (x _ {0} ^ {i}) + (1 - \alpha_ {t}) \delta (\mathbf {m})).\tag{1}
$$

Here, $\alpha _ { t }$ plays the role of a noise schedule and is an decreasing reparametrization of time such that $\alpha _ { 0 } = 1$ and $\alpha _ { 1 } = 0 \quad$ . A key detail of the simplified masking process is that once a token is masked, it remains masked for the remainder of the process. Similar to conventional difusion models in continuous space, the specification of the forward process also allows us to write a time-reversed process that iteratively denoises a sample from $t  t - 1$ until a clean, fully unmasked sample is procured at time $t = 0$ . For the simplified masking process, the time reversal also factorizes across tokens within the sequence. More precisely, the reverse transition kernel for a token $\boldsymbol { x } _ { t } ^ { i }$ conditioned on $x _ { 0 } ^ { i }$ is given by:

$$
q _ {t} (x _ {t - 1} ^ {i} | x _ {t} ^ {i}, x _ {0} ^ {i}) = \left\{ \begin{array}{l l} \operatorname{Cat} (x _ {t - 1} ^ {i}; \delta (x _ {t} ^ {i})) & x _ {t} ^ {i} \neq \mathbf {m} \\ \operatorname{Cat} \left(x _ {t - 1} ^ {i}; \frac {(1 - \alpha_ {t - 1}) \delta (\mathbf {m}) + (\alpha_ {t - 1} - \alpha_ {t}) \delta (x _ {0} ^ {i})}{1 - \alpha_ {t}}\right) & x _ {t} ^ {i} = \mathbf {m}. \end{array} \right.\tag{2}
$$

It is important to highlight that once a token is unmasked and realized as one of the remaining $d - 1$ categories, it remains fixed for the rest of the denoising steps. The form of Equation (2) suggests a natural parameterization to learn the reverse process using a time-independent denoiser network $D _ { \theta } : \mathcal { V } ^ { L } \to ( \Delta ^ { d } ) ^ { L }$ that predicts the probabilities of a clean sample $\mathbf { z } \sim D _ { \theta } ( x _ { t } )$ at $t = 0 \colon$

$$
q _ {t, \theta} (x _ {t - 1} ^ {i} | x _ {t} ^ {i}, D _ {\theta} ^ {i} (\mathbf {x} _ {t})) = \left\{ \begin{array}{l l} \operatorname{Cat} (x _ {t - 1} ^ {i}; \delta (x _ {t} ^ {i})) & x _ {t} ^ {i} \neq \mathbf {m} \\ \operatorname{Cat} \left(x _ {t - 1} ^ {i}; \frac {(1 - \alpha_ {t - 1}) \delta (\mathbf {m}) + (\alpha_ {t - 1} - \alpha_ {t}) D _ {\theta} ^ {i} (\mathbf {x} _ {t})}{1 - \alpha_ {t}}\right) & x _ {t} ^ {i} = \mathbf {m}. \end{array} \right.\tag{3}
$$

where $D _ { \theta } ^ { i }$ refers to selecting the i-th index of the output of the denoiser $D _ { \theta } ( \mathbf { x } _ { t } ) { \mathrm { - } } \mathrm { i . e }$ . the approximate distribution of $x _ { 0 } ^ { i }$ given the conditional information from $\mathbf { x } _ { t } .$ . Using the reverse parametrization and taking an infinitesimal time discretization $T \to \infty ,$ , it is possible to construct an evidence lower bound (ELBO) to the log marginal likelihood on the data distribution of the approximate data distribution from iteratively sampling via Eq. 3, $\mathbf { p } _ { \theta } ( \mathbf { x } _ { 0 } )$ , which also yields a natural optimization objective for learning the denoiser $D _ { \theta }$

$$
\log \mathbf {p} _ {\theta} (\mathbf {x} _ {0}) \geq - \int_ {0} ^ {1} \frac {d \alpha_ {t}}{d t} \cdot \frac {1}{1 - \alpha_ {t}} \mathbb {E} _ {\mathbf {x} _ {t} \sim \mathbf {p} _ {t} (\cdot | \mathbf {x} _ {0})} \left[ \sum_ {i = 1, x _ {t} ^ {i} = \mathbf {m}} ^ {L} \delta (x _ {0} ^ {i}) ^ {T} \log D _ {\theta} ^ {i} (\mathbf {x} _ {t}) \right] d t.\tag{4}
$$

This efectively renders training a masked discrete difusion model as optimizing a weighted cross-entropy loss (Eijkelboom et al., 2024).

A major limitation of vanilla MDMs is that, in the continuous-time limit $T \to \infty$ , the probability of denoising multiple tokens simultaneously vanishes due to independent updates via Eq. 3. In this regime, an analytic Gillespie-style sampler (Gillespie, 1977; 1976) reveals that denoising proceeds by uniformly sampling a masked position (see §D.3), ofering no control over the generation order. Next, we consider a new, more complex inference scheme that principally allows for changing unmasked tokens to any other token in V, allowing for the index of the next token to be resampled.

## 3 Discrete Difusion with Path Planning

We now aim to improve the generation capability of MDMs by modifying the reverse denoising process by introducing a planning component in a novel inference strategy termed P2. In Table 1 we contrast P2 with the extensive existing literature in planning for MDMs. In particular, P2 is the only model with remasking, planning, and stochasticity control. In what follows, we further explore novel forms of planners as we find that the optimal planner depends on the application.

Table 1: Generalization of existing sampling Methods within the P2 Framework. Masked Planner $( G _ { M } ^ { j } )$ gives the probability that a mask token should be unmasked. Unmasked Planner $( G _ { U } ^ { j } )$ gives the probability that an unmasked token should be kept. $D _ { \theta } ^ { j }$ gives the prediction probability of the denoiser at position j. TopKMargin $( D _ { \theta } ^ { j } ( { \bf x } _ { t } ) )$ denotes selection based on the probability margin between the top-2 predictions.

<table><tr><td>Method</td><td>Remasking</td><td>Planning</td><td>Stochasticity Control</td><td>Mask Planner ( $G_{M}^{j}(\mathbf{z},\mathbf{x}_{t})$ )</td><td>Unmask Planner ( $G_{U}^{j}(\mathbf{z},\mathbf{x}_{t})$ )</td></tr><tr><td>Ancestral (Shi et al., 2024; Sahoo et al., 2024)</td><td>✘</td><td>✘</td><td>✘</td><td> $\mathcal{U}(0,1)$ </td><td>1</td></tr><tr><td>MaskGIT (Chang et al., 2022b)</td><td>✘</td><td>✓</td><td>✘</td><td> $\text{Cat}(z^{j};D_{\theta}^{j}(\mathbf{x}_{t}))$ </td><td>1</td></tr><tr><td>Greedy Ancestral (Gong et al., 2025)</td><td>✘</td><td>✓</td><td>✘</td><td> $\text{Cat}(z^{j};D_{\theta}^{j}(\mathbf{x}_{t}))$ </td><td>1</td></tr><tr><td>TopK-Marginal (Kim et al., 2025)</td><td>✘</td><td>✓</td><td>✘</td><td> $\text{TopKMargin}(D_{\theta}^{j}(\mathbf{x}_{t}))$ </td><td>1</td></tr><tr><td>DFM Sampling (Campbell et al., 2024)</td><td>✘</td><td>✘</td><td>✓</td><td> $\mathcal{U}(0,1)$ </td><td> $\mathcal{U}(0,1)$ </td></tr><tr><td>RDM Sampling (Zheng et al., 2023)</td><td>✓</td><td>✓</td><td>✘</td><td> $\text{Cat}(z^{j};D_{\theta}^{j}(\mathbf{x}_{t}))$ </td><td> $\text{Cat}(z^{j};D_{\theta}^{j}(\mathbf{x}_{t}))$ </td></tr><tr><td>DDPD (Liu et al., 2024)</td><td>✓</td><td>✓</td><td>✘</td><td> $G_{\phi}^{j}(\mathbf{z})$ </td><td> $G_{\phi}^{j}(\mathbf{z})$ </td></tr><tr><td>P2 (Self-Planning)</td><td>✓</td><td>✓</td><td>✓</td><td> $\text{Cat}(z^{j};D_{\theta}^{j}(\mathbf{x}_{t}))$ </td><td> $\text{Cat}(z^{j};D_{\theta}^{j}(\mathbf{x}_{t}))$ </td></tr><tr><td>P2 (BERT Planner)</td><td>✓</td><td>✓</td><td>✓</td><td> $\text{Cat}(z^{j};D_{\theta}^{j}(\mathbf{x}_{t}))$ </td><td> $\text{Cat}(z^{j};B_{\phi}^{j}(\mathbf{z}))$ </td></tr><tr><td>P2 (Trained Planner)</td><td>✓</td><td>✓</td><td>✓</td><td> $\text{Cat}(z^{j};D_{\theta}^{j}(\mathbf{x}_{t}))$ </td><td> $T_{\phi}^{j}(\mathbf{x}_{t},\mathbf{z})$ </td></tr></table>

## 3.1 The P2 Sampling Strategy

In order to formulate P2, we begin by modifying the approximate backwards process $\left( \operatorname { E q . 3 } \right)$ , introducing a new function $G _ { \phi } : \mathcal { V } ^ { L } \times \mathcal { V } ^ { L } \to [ 0 , 1 ] ^ { L }$ , with parameters $\phi ,$ which we refer to as the planner. Intuitively, $G _ { \phi } ^ { j } ( { \bf z } , { \bf x } _ { t } )$ approximates the probability that the $j ^ { \cdot } \mathrm { t h }$ token in a partially denoised sequence should be (re)sampled conditioned on the rest of the sequence $\mathbf { x } _ { t } \in \mathcal { V } ^ { L }$ and predicted clean data z.

P2 departs from the vanilla MDM inference procedure, where the backward transition $q _ { t , \theta } \big ( x _ { t - 1 } ^ { i } | x _ { t } ^ { i } , D _ { \theta } ^ { i } \big ( \mathbf { x } _ { t } \big ) \big )$ in Equation (3) is denoised independently for each coordinate in the sequence by instead assigning the likelihood of denoising at $\boldsymbol { x } _ { t } ^ { i }$ as a function of the planner $G _ { \phi }$ . Succinctly, the P2 strategy is used to update a partially noised sequence $\mathbf { x } _ { t }$ by first sampling a denoised sequence given a partially noised sequence $x _ { t }$ , i.e., $\mathbf { z } \sim D _ { \theta } ( \mathbf { x } _ { t } )$ after which we can leverage our planner $G _ { \phi } ( \mathbf { z } , \mathbf { x } _ { t } )$ to determine which positions in the sequence to update. If $x _ { t } ^ { i } = { \mathbf { m } }$ , we unmask to the sample $z ^ { i }$ with probability $G _ { \phi } ^ { i } ( { \bf z } , { \bf x } _ { t } )$ . Conversely, if $x _ { t } ^ { i } \neq \mathbf { m }$ , with probability $G _ { \phi } ^ { i } ( { \bf z } , { \bf x } _ { t } )$ , we construct $\bar { \mathbf { x } } _ { t }$ from $\mathbf { x } _ { t }$ via setting $\ v x _ { t } ^ { i }$ to m (remasking), and then we resample $x _ { t - 1 } ^ { i } \sim D _ { \theta } ^ { i } ( \bar { \mathbf { x } } _ { t } )$ so that $x _ { t - 1 } ^ { i } \neq x _ { t } ^ { i }$ . The conditionally independent coordinate-wise reverse transitions are then, for $x _ { t - 1 } ^ { i } \neq x _ { t } ^ { i }$

$$
q _ {t, \theta} (x _ {t - 1} ^ {i} | \mathbf {x} _ {t}, \mathbf {z}) = \left\{ \begin{array}{l l} \mathrm{Cat} \left(x _ {t - 1} ^ {i}; \frac {\alpha_ {t - 1} - \alpha_ {t}}{1 - \alpha_ {t}} G _ {\phi} ^ {i} (\mathbf {z}, \mathbf {x} _ {t}) \delta (z ^ {i})\right) & x _ {t} ^ {i} = \mathbf {m} \\ \mathrm{Cat} \left(x _ {t - 1} ^ {i}; \frac {(\alpha_ {t - 1} - \alpha_ {t}) G _ {\phi} ^ {i} (\mathbf {z} , \mathbf {x} _ {t})}{(1 - \alpha_ {t}) (1 - \mathrm{Cat} (x _ {t} ^ {i} , D _ {\theta} ^ {i} (\bar {\mathbf {x}} _ {t})))} D _ {\theta} ^ {i} (\bar {\mathbf {x}} _ {t})\right) & x _ {t} ^ {i} \neq \mathbf {m}, \end{array} \right.\tag{5}
$$

and the case $x _ { t - 1 } ^ { i } = x _ { t } ^ { i }$ is obtained by ensuring these sum to 1.

We highlight the masked case in Equation (5) proceeds in the same manner as the classical MDM inference setup outside of the key diference that the index to be denoised is selected by the planner $G _ { \phi }$ . Furthermore, P2 updates a masked token by an intermediate step of remasking and then denoising to a diferent token by resampling from $D _ { \theta } ( \bar { \bf x } _ { t } )$ , using the newly constructed $\bar { \mathbf { x } } _ { t }$ . Critically, we see that P2 allows for the planner $G _ { \phi }$ to guide the denoising process towards a more optimal path of denoising orders using the information from both the partially noised sequence $\mathbf { x } _ { t }$ and the predicted clean sequence z from the denoiser—including resampling incorrect denoised tokens. We outline the full top-k instantiation of the P2 algorithm in pseudocode in Algorithm 1 and include a computationally viable Gillespie sampler method (Gillespie, 1977; 1976) for P2 in Algorithm 5.

## 3.2 Designing the Planner

The P2 sampling strategy requires the design of a planner $G _ { \phi }$ whose role is to select tokens to update by exploiting information about the current $\mathbf { x } _ { t }$ and z. To construct the planner, such that we can guarantee convergence to a fully unmasked sequence at t = 1 we first decompose $G _ { \phi }$ into two components:

$$
G _ {\phi} ^ {j} (\mathbf {z}, \mathbf {x} _ {t}) = \left\{ \begin{array}{l l} G _ {M} ^ {j} (\mathbf {z}, \mathbf {x} _ {t}) & x _ {t} ^ {j} = \mathbf {m} \\ 1 - G _ {U} ^ {j} (\mathbf {z}, \mathbf {x} _ {t}) & x _ {t} ^ {j} \neq \mathbf {m}. \end{array} \right.\tag{6}
$$

where $G _ { M } ^ { j } ( \mathbf { z } , \mathbf { x } _ { t } )$ is the masked token planner that predicts the likelihood that a masked token at the $j ^ { \flat }$ th position should be unmasked, and an unmasked token planner $G _ { U } ^ { j } ( { \bf z } , { \bf x } _ { t } )$ which predicts the probability that an unmasked token should be kept. We then employ a modified $^ { \mathrm { 6 6 } } \mathrm { t o p ~ k } ^ { \mathrm { 9 } }$ sampling strategy, which introduces the possibility of changing multiple tokens per iteration and better exploits the information provided by a monotone non-decreasing scheduler function $\kappa : \{ 1 , \ldots , L \}  \{ 1 , \ldots , L \}$ , with $\kappa ( L ) = L$ . The purpose of the scheduler is to determine the number of tokens, $\kappa ( t )$ , that are guaranteed to be unmasked at the reverse step t.

The final component of P2 is a stochasticity parameter η, which controls the frequency of remasking as in DFM (Campbell et al., 2024). This parameter allows a practitioner to control the trade-of between eficiency and additional self-correction and is standard in continuous difusion models. This defines a family of probability path measures for our planner:

$$
\tilde {G} _ {\eta} ^ {j} (\mathbf {z}, \mathbf {x}) \propto \eta \mathrm{Cat} (x ^ {j}; \delta (\mathbf {m})) G _ {M} ^ {j} (\mathbf {z}, \mathbf {x}) + (1 - \mathrm{Cat} (x ^ {j}; \delta (\mathbf {m}))) G _ {U} ^ {j} (\mathbf {z}, \mathbf {x}), \quad \eta \geq 0.\tag{7}
$$

## 3.3 A Family of Planners: Instantiations of P2

We next propose three practical instantiations of the planner $G _ { \phi }$ employed in our P2 framework.

Self-Planning. We propose a self-planning mechanism by leveraging the denoiser’s own predicted probabilities to guide updating decisions. Concretely, we set $G _ { U } ^ { j } ( { \mathbf { z } } , { \mathbf { x } } ) = G _ { M } ^ { j } ( { \mathbf { z } } , { \mathbf { x } } ) = { \mathrm { C a t } } ( z ^ { j } ; D _ { \theta } ^ { j } ( { \mathbf { x } } ) )$ , and as a result the denoiser itself serves as the planner. For masked positions, the denoiser is trained to predict tokens given the surrounding context, and the predicted probabilities serve as confidence estimates for the correctness of token predictions. This methodology aligns with established practices in the literature (Gong et al., 2025; Chang et al., 2022a; Zheng et al., 2023; Wang et al., 2024; 2025b) as outlined in Table 1. We further highlight that instantiations of the self-planner recover the methodology of established results. Fo instance, both MaskGIT (Chang et al., 2022b) and Greedy Ancestral (Gong et al., 2025) are special cases of self-planning without stochasticity control and when the unmask planner $G _ { U } ( \mathbf { z } , \mathbf { x } ) = 1 { \mathrm { - d i s a b l i n g } }$ the remasking technique from self-planning (see e.g. Table 1). Surprisingly, for unmasked tokens probabilities, the denoiser—despite only being trained solely on masked positions—still has access to robust representations of unmasked positions, and as a result is still informative for resampling, and thus sequence generation.

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 1 P2 Sampling (simplified)
1: Input:  $x_{0} \leftarrow (\mathbf{m}, \ldots, \mathbf{m})$ ,  $G_{\phi}$ ,  $D_{\theta}$ , Schedule  $\kappa$ 
2: for t = 1 : L do
3: Plan:
4:  $z \sim D_{\theta}(x_{t})$ 
5: UpdatePos  $\leftarrow \text{Top}_{\kappa(t)} \left( \tilde{G}_{\eta}(z, x_{t}) \right)$ 
6: Denoise:
7:  $x_{t}^{j} \leftarrow \begin{cases} z^{j} &amp; \text{if } j \in \text{UpdatePos} \wedge x_{t}^{j} = m \\ m &amp; \text{if } j \notin \text{UpdatePos} \end{cases}$ 

8: end for
9: return  $x_{L}$ 

Algorithm 2 P2 Planner Training (Frozen  $D_{\theta}$ )

1: Input:  $x_{0} \sim p_{0}$ ,  $D_{\theta}$ ,  $G_{\phi}$ 
2: Sample  $t \sim U(0, 1)$ 
3: Sample  $x_{t} \sim p_{t}(\cdot | x_{0})$ 
4:  $z \sim D_{\theta}(x_{t})$ 
5: logits $^{j} \leftarrow G_{M}^{j}(z, x_{t})$  for j such that  $x_{t}^{j} = m$  and  $G_{U}^{j}(z, x_{t})$  otherwise
6: label $^{j} \leftarrow 1[z^{j} = x_{0}^{j}]$ 
7:  $\mathcal{L}(\phi) \leftarrow \frac{d\alpha_{t}}{dt} \cdot \frac{1}{1 - \alpha_{t}} \cdot \text{CE}(\text{label}, \text{logits})$ 
8: Update:  $\phi \leftarrow \phi - \nabla_{\phi}\mathcal{L}(\phi)$
</div>

BERT-planning. In BERT-planning, we introduce a class of planners based on a pre-trained BERT model (Devlin et al., 2019), which is trained to denoise from a 12% masking rate at training and 1.5% random flipping rate. Despite such a simple training objective, BERT learns to estimates the naturalness of an unmasked token with the predicted probabilities which demonstrates wide application in zero-shot mutation prediction (Hie et al., 2024), suggesting that BERT may serve as an efective choice for $G _ { U }$ . Compared to training a dedicated planner that is equal-size to denoiser as in DDPD (Liu et al., 2024), BERT is more versatile, flexible in sizes, and often available in common tasks such as text (Devlin et al., 2019; Liu et al., 2019; Lan et al., 2020), protein (Lin et al., 2023; Hayes et al., 2025; Wang et al., 2024; 2025b) and RNA (Penić et al., 2024). Mathematically, we formulate BERT planning using a BERT model $B _ { \phi } : \dot { \mathcal { V } } ^ { L } \to ( \Delta ^ { d } ) ^ { L }$ , such that $\mathrm { C a t } ( z ^ { j } ; B _ { \phi } ^ { j } ( { \bf z } ) )$ assigns the probability that the j-th token in the sequence z is clean. In BERT planning we set the unmask planner to be the BERT $G _ { U } ^ { j } ( { \bf z } , { \bf x } ) = \mathrm { C a t } ( z ^ { j } ; B _ { \phi } ^ { j } ( { \bf z } ) )$ ) and mask planner to be the denoiser $G _ { M } ^ { j } ( { \bf z } , { \bf x } ) = \mathrm { C a t } ( z ^ { j } ; D _ { \theta } ^ { j } ( { \bf x } ) )$ .

Trained-Planner. We can also employ a trained planner that operates on the denoiser’s prediction and the current masked input. Specifically, we freeze the denoiser during training and fine-tune the BERT planner by taking $G _ { M } ^ { j } ( { \mathbf { z } } , { \mathbf { x } } ) = G _ { U } ^ { j } ( { \mathbf { z } } , { \mathbf { x } } ) = { \mathrm { C a t } } ( z ^ { j } ; B _ { \phi } ^ { j } ( { \mathbf { z } } ) )$ using a cross-entropy loss derived from the planner ELBO objective. In this case, the planner learns to predict whether each token should be selected based on whether the denoiser’s output matches the ground-truth token. As detailed in Algorithm 2, the planner is supervised to match the optimal decoding trajectory—i.e., one that prioritizes correct positions.

During sampling for experiments using P2 Train - see Table 5 - we use the same parameterization as with P2 BERT for constructing $\tilde { G } _ { \eta } ^ { j }$ of $\mathrm { E q . ~ } 7$ in Algorithm 1. That is, we set the unmask planner to be the fine-tuned BERT $G _ { U } ^ { j } ( { \bf z } , { \bf x } ) = \mathrm { C a t } ( z ^ { j } ; B _ { \phi } ^ { j } ( { \bf z } ) )$ and mask planner to be the denoiser $G _ { M } ^ { j } ( { \bf z } , { \bf x } ) = \mathrm { C a t } ( z ^ { j } ; D _ { \theta } ^ { j } ( { \bf x } ) )$

We emphasize that, although we only use the fine-tuned BERT model as $G _ { U }$ for sampling, it is trained on both masked and unmasked positions in Algorithm 2. This allows for the model to have a meaningful training signal in that it gets to see both 0 and 1 as the label. We note that without training on masked positions, this would not be the case, since the label is always 1 in unmasked positions.

The training of the planner in Algorithm 2 is theoretically supported by the following propositions. Note that indeed in Proposition $2$ we make the assumption that the same network backbone is used as both $G _ { M }$ and $G _ { U }$ in training, and this should always be done in practice, even if one intends to use $T$ only as $G _ { U }$ or $G _ { M }$ during sampling.

Proposition 1. Define $P _ { 0 } ^ { \theta , \phi } \in \Delta ^ { d ^ { L } }$ by $P _ { 0 } ^ { \theta , \phi } ( \mathbf { x } ) = \mathbb { P } ( X _ { 0 } ^ { \theta , \phi } = \mathbf { x } )$ , where $X ^ { \theta , \phi }$ is the continuous time Markov chain resulting from sending $T \to \infty$ in the discrete-time P2 formulation $E q .$ 5. Then we have an “Evidence Based Lower Bound” $" \mathcal { E } ( \mathbf { x } _ { 0 } ) \leq \log ( P _ { 0 } ^ { \theta , \phi } ( \mathbf { x } _ { 0 } ) )$ for each fixed ${ \bf x } _ { 0 } \in \mathcal { V } ^ { L }$ given by $\mathcal { E } ( \mathbf { x } _ { 0 } ) =$ $\mathcal { E } _ { M P } ( \mathbf { x } _ { 0 } ) + \mathcal { E } _ { U P } ( \mathbf { x } _ { 0 } ) + \mathcal { E } _ { D } ( \mathbf { x } _ { 0 } )$ , where:

$$
\mathcal {E} _ {M P} (\mathbf {x} _ {0}) = - \int_ {0} ^ {1} \frac {d \alpha_ {t}}{d t} \cdot \frac {1}{1 - \alpha_ {t}} \mathbb {E} _ {\mathbf {x} _ {t} \sim \mathbf {p} _ {t} (\cdot ; \mathbf {x} _ {0})} \left[ \sum_ {i = 1, \mathbf {x} _ {t} ^ {i} = \mathbf {m}} ^ {L} \mathbb {E} _ {\mathbf {z} \sim D _ {\theta} (\mathbf {x} _ {t})} \left[ C E \left(C a t (z ^ {i}; \delta (x _ {0} ^ {i})), G _ {M} ^ {i} (\mathbf {z}, \mathbf {x} _ {t})\right) \right] \right] d t
$$

$$
\mathcal {E} _ {U P} (\mathbf {x} _ {0}) = - \int_ {0} ^ {1} \frac {d \alpha_ {t}}{d t} \cdot \frac {1}{1 - \alpha_ {t}} \mathbb {E} _ {\mathbf {x} _ {t} \sim \mathbf {p} _ {t} (\cdot ; \mathbf {x} _ {0})} \left[ \sum_ {i = 1, \mathbf {x} _ {t} ^ {i} \neq \mathbf {m}} ^ {L} \mathbb {E} _ {\mathbf {z} \sim D _ {\theta} (\mathbf {x} _ {t})} \left[ C E \left(C a t (z ^ {i}; \delta (x _ {0} ^ {i})), G _ {U} ^ {i} (\mathbf {z}, \mathbf {x} _ {t})\right) \right] \right] d t
$$

$$
\mathcal {E} _ {D} (\mathbf {x} _ {0}) = - \int_ {0} ^ {1} \frac {d \alpha_ {t}}{d t} \cdot \frac {1}{1 - \alpha_ {t}} \mathbb {E} _ {\mathbf {x} _ {t} \sim \mathbf {p} _ {t} (\cdot ; \mathbf {x} _ {0})} \left[ \sum_ {i = 1, \mathbf {x} _ {t} ^ {i} = \mathbf {m}} ^ {L} \delta (\mathbf {x} _ {0} ^ {i}) ^ {\top} \log (D _ {\theta} ^ {i} (\mathbf {x} _ {t})) \right] d t.
$$

Here $\mathbf { p } _ { t }$ is defined per Eq. 1 and $C E ( a , b ) = a \log ( b ) + ( 1 - a ) \log ( 1 - b ) \ f o r \ a , b \in [ 0 , 1 ]$ , with 0 log $0 = 0$

Here $ { \mathcal { E } _ { \mathrm { D } } }$ is the ELBO of the denoiser in a standard MDM, $\mathcal { E } _ { \mathrm { U P } }$ is the ELBO of the unmasking planner, and $\mathcal { E } _ { \mathrm { M P } }$ is the ELBO of the masking planner. See §B for a proof via taking limits of the time-discritized ELBO for the dynamics Eq. 5 and §D for a proof and more fine-grained theoretical analysis from a continuous-time point of view. This proposition establishes the validity of using P2 and presents a novel, finer-grained ELBO for planner-based masked language models. The explicit inclusion of a non-trivial $G _ { \phi }$ in our ELBO allows both for training a planner and for evaluating the eficacy of an “of-the-shelf” planner. Table S6, we show that planners ranging from 8M to 3B parameters have similar ELBOs and thus have similar generation performance (Figure S3), which corroborates the efectiveness of training on this bound. We also remark that, while we use the default stochasticity parameter of $\eta = 1$ to evaluate the ELBO and for the loss in P2 train and find this to be indicative of planner performance, one could also use the ELBO of Proposition 1 to evaluate varied stochasticity levels. We include the form of the ELBO for general η in §B.3 for reference.

We note that the loss ${ \mathcal { L } } ( \phi )$ used in Algorithm 2 operates on a frozen denoiser $D _ { \theta }$ , and ${ \mathcal { L } } ( \phi ) ~ =$ $- \mathbb { E } _ { { \mathbf { x } } _ { 0 } \sim { \mathbf { p } } _ { 0 } } \left[ \mathcal { E } _ { \mathrm { M P } } ( { \mathbf { x } } _ { 0 } ) + \mathcal { E } _ { \mathrm { U P } } ( { \mathbf { x } } _ { 0 } ) \right]$ . Moreover, $\mathcal { E } _ { \mathrm { M P } }$ optimizes the role of the masked planner as a mechanism for selecting the viable masked position to insert a “clean” token as suggested by $D _ { \theta }$ . E acts as a mechanism for selecting an unmasked token to resample via remasking and inserting back into $D _ { \theta }$ . Indeed, these roles are verified via finding the optimal form of the trained planner as per Proposition 2.

Proposition 2. Let $T _ { \phi } : \mathcal { V } ^ { L } \times \mathcal { V } ^ { L } \to [ 0 , 1 ]$ be trained via $\mathcal { L } ( \phi ) = - \mathbb { E } _ { { \bf x } _ { 0 } \sim { \bf p } _ { 0 } } \left[ \mathcal { E } _ { M P } ( { \bf x } _ { 0 } ) + \mathcal { E } _ { U P } ( { \bf x } _ { 0 } ) \right]$ , taking $G _ { U } = G _ { M } = T _ { \phi }$ in $\mathcal { E } _ { M P }$ and E<sub>UP</sub> from Proposition 1. Define, for ${ \mathbf z } , { \mathbf x } _ { \mathbf t } \in \mathcal V ^ { \mathbf L }$ with z a sequence of unmasked tokens satisfying $\mathbf { z } ^ { i } = \mathbf { x } _ { t } ^ { i }$ for all i such that $\mathbf { x } _ { t } ^ { i } \neq$ m:

$$
\bar {T} ^ {i} (\mathbf {z}, \mathbf {x} _ {t}) = \left\{ \begin{array}{l l} \mathbf {p} _ {0} \left(x _ {0} ^ {i} = z ^ {i} | x _ {0} ^ {j} = x _ {t} ^ {j}, \forall j \neq i \text {such that} x _ {t} ^ {j} \neq \mathbf {m}\right), & x _ {t} ^ {i} \neq \mathbf {m} \\ \mathbf {p} _ {0} \left(x _ {0} ^ {i} = z ^ {i} | x _ {0} ^ {j} = x _ {t} ^ {j}, \forall j \text {such that} x _ {t} ^ {j} \neq \mathbf {m}\right), & x _ {t} ^ {i} = \mathbf {m} \end{array} \right..
$$

Then, for any $D _ { \theta }$ , L(ϕ) is uniquely minimized over $T _ { \phi } ^ { i }$ when $T _ { \phi } ^ { i } ( \mathbf { z } , \mathbf { x } _ { t } ) = \bar { T } ^ { i } ( \mathbf { z } , \mathbf { x } _ { t } )$

Observe that this means, for any denoiser, the optimal $T _ { \phi } ^ { i }$ is aiming to steer towards planned paths which are representative of the data distribution in both its roles as $G _ { U } ^ { i }$ and $G _ { M } ^ { i }$ . In unmasked positions, a token in position i is kept with probability proportional to to the probability the token is in the data distribution conditionally upon the information from the partially denoised sequence $x _ { t }$ in positions other than i. In masked positions, a suggested token $z ^ { i }$ for position i from the denoiser is selected with probability proportional to the probability $z ^ { i }$ is in position i under the data distribution conditionally upon the information from the current $x _ { t }$ . For further discussion of the form of the optimal planner and a proof of Proposition 2, see §B.2.

## 4 Experiments

We empirically evaluate our Path Planning (P2) inference framework for MDMs across three distinct discrete generative modeling tasks: protein sequence generation, natural language generation, and RNA sequence generation. Our main experiments Section 4.1-Section 4.3 aim to investigate the empirical benefit P2 by evaluating the generated sequences for their functional quality, sample diversity, and task completion at various model scales. We also conduct comprehensive ablations to investigate the impact of planner choice in §4.4 and finally turn to inference-time scaling experiments in §4.5.

![](Peng2025Path_figs/a5faac7b929ba0acec4c12c2611b6a815c26f9eebfa87ba6b27eabecbbf2066a.jpg)  
Figure 2: Visualizing the predicted structures of generated protein (top) and RNA (bottom) sequences. Additional structures depicted in Figure S7.

## 4.1 Protein Sequence Generation

We consider the task of protein sequence generation and measure the foldability, structural quality (pLDDT, $\mathrm { { p T M } , \mathrm { { p A E } ) } }$ , and diversity (diversity & entropy) of generated proteins and benchmark against state-of-the-art autoregressive and MDMs. Through this experiment we assess whether P2 improves structural metrics while preserving entropy and diversity of generated sequences. For each model we generate 100 sequences at lengths in {200, 300, . . . , 800} using its default decoding strategy. Structural quality is assessed using ESMFold (Lin et al., 2023). We define a sequence as foldable if it satisfies: $\mathrm { \ p L D D T > 8 0 , \ p T M > 0 . 7 , }$ and $\mathrm { p A E } < 1 0$ Entropy and diversity metrics are also computed to assess mode collapse see Section F.1 for further details.

Table 2: Protein sequence generation benchmark. We evaluate structure quality via pLDDT, pTM, and pAE, and diversity via token entropy and sequence uniqueness. Foldability is the percentage of sequences satisfying pLDDT > 80, pTM > 0.7, and ${ \mathrm { p A E } } < 1 0 .$ See Section F.1 for setup and Table S4 for model size ablations.

<table><tr><td>Model</td><td>pLDDT↑</td><td>pTM↑</td><td>pAE↓</td><td>Foldability (%)↑</td><td>Entropy↑</td><td>Diversity (%)↑</td></tr><tr><td>EvoDiff</td><td>31.84</td><td>0.21</td><td>24.76</td><td>0.43</td><td>4.05</td><td>93.19</td></tr><tr><td>ESM3</td><td>34.13</td><td>0.23</td><td>24.65</td><td>1.50</td><td>3.99</td><td>93.44</td></tr><tr><td>ProGen2</td><td>49.38</td><td>0.28</td><td>23.38</td><td>4.48</td><td>2.55</td><td>89.31</td></tr><tr><td>DPLM</td><td>80.23</td><td>0.65</td><td>12.07</td><td>48.14</td><td>3.14</td><td>92.80</td></tr><tr><td>DPLM + P2-train (ours)</td><td>83.45</td><td>0.72</td><td>10.15</td><td>58.86</td><td>3.35</td><td>92.69</td></tr></table>

Table 3: Language generation benchmarks. Accuracy (%) is reported for TriviaQA, LAMBADA, and GSM8K; ROUGE-1/2/L for ROCStories; and pass@1 for HumanEval.

<table><tr><td>Model</td><td>TriviaQA</td><td>LAMBADA</td><td>GSM8K</td><td>ROUGE-1/2/L</td><td>Code</td></tr><tr><td>GPT2-S (127M)</td><td>4.0</td><td>25.9</td><td>44.8</td><td>7.8 / 0.8 / 7.4</td><td>1.6</td></tr><tr><td>DiffuGPT-S (127M)</td><td>2.0</td><td>45.0</td><td>50.2</td><td>13.7 / 1.4 / 12.6</td><td>0.3</td></tr><tr><td>SEDD-S (170M)</td><td>1.5</td><td>12.4</td><td>45.3</td><td>11.9 / 0.7 / 10.9</td><td>0.7</td></tr><tr><td>GPT2-M (355M)</td><td>6.7</td><td>37.7</td><td>50.7</td><td>8.6 / 0.9 / 8.2</td><td>2.6</td></tr><tr><td>DiffuGPT-M (355M)</td><td>3.8</td><td>60.5</td><td>52.6</td><td>18.7 / 2.7 / 17.0</td><td>2.9</td></tr><tr><td>SEDD-M (424M)</td><td>1.8</td><td>23.1</td><td>53.5</td><td>13.1 / 1.4 / 12.2</td><td>0.5</td></tr><tr><td>Plaid1B (1.3B)</td><td>1.2</td><td>8.6</td><td>32.6</td><td>12.1 / 1.1 / 11.2</td><td>0.1</td></tr><tr><td>TinyLlama (1.1B)</td><td>-</td><td>43.2</td><td>-</td><td>-</td><td>-</td></tr><tr><td>GPT-2 (1.5B)</td><td>-</td><td>44.6</td><td>-</td><td>-</td><td>-</td></tr><tr><td>MDM (1.1B)</td><td>-</td><td>52.7</td><td>58.5</td><td>-</td><td>-</td></tr><tr><td>MDM + P2-self (ours)</td><td>-</td><td>52.9</td><td>60.9</td><td>-</td><td>-</td></tr><tr><td>LLaMA2 (7B)</td><td>45.4</td><td>68.8</td><td>58.6</td><td>11.6 / 2.1 / 10.5</td><td>1.7</td></tr><tr><td>DiffuLLaMA (7B)</td><td>18.5</td><td>53.7</td><td>-</td><td>20.3 / 2.8 / 18.2</td><td>13.2</td></tr><tr><td>DiffuLLaMA + P2-self (ours)</td><td>18.8</td><td>54.8</td><td>-</td><td>25.4 / 7.1 / 23.4</td><td>17.6</td></tr></table>

Results. As shown in Table 2, applying P2 to DPLM significantly improves all folding metrics. Compared to DPLM with RDM sampling, P2 boosts pLDDT from 80.23 to 83.45 and foldability from 48.14% to 58.86%, while maintaining comparable entropy and diversity. These results confirm that P2 enhances generation quality without sacrificing diversity. Notably, DPLM + P2 outperforms all baselines—including EvoDif, ESM3, and the 2.7B parameter ProGen2—with fewer parameters and better foldability. In Figure 2 we visualize the predicted 3D structures of generated proteins, showing visually coherent and plausible folds. Additional lengthwise breakdowns and scaling ablations are included the appendix, and in particular in Table S4 and Figure S1.

## 4.2 Language Generation

We next investigate the ability of P2 inference in language modeling tasks and evaluate on a suite of diverse including reading comprehension (TriviaQA (Joshi et al., 2017)), paragraph completion (LAMBADA (Paperno et al., 2016)), math reasoning (GSM8K (Cobbe et al., 2021)), story infilling (ROCStories (Mostafazadeh et al., 2016)), and code generation (HumanEval (Bavarian et al., 2022))—adopted from SMDM (Gong et al., 2025) and DifuLLaMA (Nie et al., 2025). Additional experiments on modeling bidirectional relations, i.e. reverse curse behavior, are included in Section G.1.1. We apply P2 to two strong difusion models: 1.) MDM (1.1B) and 2.) DifuLLaMA (7B), and compare them to ancestral sampling. For P2, we sweep the stochasticity strength $\eta \in [ 0 , 2 . 0 ]$ with step size 0.2, and report the best result per task in Table 3, with full experimental setup provided in Section F.2.

Results. We observe that P2 consistently improves generation quality across all five benchmarks, indicating improved global reasoning, fewer intermediate errors, and more coherent generations. On GSM8K, P2 lifts MDM performance from 58.5% to 60.9%, surpassing the 7B autoregressive baseline LLaMA2 (58.6%). Finally, on code generation, DifuLLaMA with P2 achieves a 17.6% pass@1, significantly outperforming both ancestral sampling (13.2%) and LLaMA2 (1.7%). On ROCStories, P2 boosts ROUGE-1/2/L scores by more than 5 absolute points.

Table 4: RNA sequence generation results. pLDDT and MFE measure structural quality, Entropy measures diversity, and GC content reflects biophysical realism.

<table><tr><td>Source</td><td>pLDDT (↑)</td><td>MFE (↓)</td><td>Entropy (↑)</td><td>GC% (↑)</td></tr><tr><td>Native</td><td>48.26</td><td>-35.83</td><td>1.96</td><td>49.64</td></tr><tr><td>RiNALMo-150M</td><td>59.01</td><td>-30.12</td><td>1.29</td><td>29.50</td></tr><tr><td>RiNALMo-650M</td><td>46.99</td><td>-31.90</td><td>1.33</td><td>28.06</td></tr><tr><td>MDM</td><td>68.12</td><td>-48.46</td><td>1.93</td><td>60.84</td></tr><tr><td>MDM + P2-BERT (ours)</td><td>73.28</td><td>-51.91</td><td>1.86</td><td>65.47</td></tr></table>

## 4.3 RNA Sequence Generation

We evaluate P2 in the context of RNA generation, where biophysical plausibility is critical (see Section F.4 for training and evaluation details). A 150M-parameter MDM is trained on 27M sequences from RNACentral (Petrov, 2021). For evaluation, we follow the protein protocol and predict RNA structures using an external folding model (Shen et al., 2024), measuring pLDDT, minimum free energy (MFE), sequence entropy, and GC content. We generate 100 sequences of 100 base pairs each. As shown in Table 4, the MDM already surpasses RiNALMo baselines in structural quality and energy. Applying P2 with BERT-Planning (from RiNALMo-150M) further improves pLDDT (68.1 → 73.3), lowers MFE (−48.5 → −51.9), and increases GC content (60.8% → 65.5%)—key indicators of biophysically plausible RNA. These gains come with only a small reduction in entropy.

## 4.4 Ablation Studies

We conduct ablation studies to evaluate whether P2 improves performance across diferent domains and to understand how its variants compare to existing sampling strategies. We focus each ablation experiment on a specific domain and seek to answer the following key experimental questions:

Q1: Does P2 outperform prior sampling strategies for protein sequence generation? We compare P2 against common decoding strategies using a 150M MDM on protein generation ( Table 5). P2-Train (ours) achieves the highest pLDDT (83.45) and foldability (58.86%), outperforming RDM (Zheng et al., 2023) and Greedy Ancestral, MaskGIT (Chang et al., 2022b) and Top-K Marginal (Kim et al., 2025) by large margins. The performance gap further highlights that the design choices made in P2 which diferentiate it from the related baselines, such as MaskGIT (Chang et al., 2022b) and Top-K Marginal (Kim et al., 2025), play a crucial role in real-world applications. P2-Self and P2-Bert also yield consistent gains, while P2-Train with an additionally post-trained planner exhibits the best performance, validating that planner-based sampling significantly enhances structural quality.

## Q2: Can P2 improve generative fluency and accuracy in code and story infilling tasks?

Using a 7B DifuLLaMA model, we assess generation quality in HumanEval and ROCStories benchmarks (Table 6). We find our P2-Self model achieves the highest pass@1 and ROUGE scores, outperforming both ancestral decoding and RDM.

## Q3: Does P2 improve structural quality in RNA generation while maintaining diversity?

Table 7 shows that P2-Bert (ours) improves pLDDT and MFE while preserving GC content and entropy. This indicates that P2 remains efective across biomolecular domains, even when transferring planners pretrained on diferent modalities.

Table 5: Protein sequence generation: comparison of sampling strategies.

<table><tr><td>Method</td><td>pLDDT (↑)</td><td>pTM (↑)</td><td>pAE (↓)</td><td>Foldability (%) (↑)</td><td>Entropy (↑)</td><td>Diversity (%) (↑)</td></tr><tr><td>Vanilla Ancestral</td><td>54.11</td><td>0.43</td><td>19.96</td><td>6.29</td><td>3.90</td><td>93.28</td></tr><tr><td>Greedy Ancestral</td><td>63.69</td><td>0.51</td><td>17.50</td><td>13.00</td><td>3.83</td><td>93.03</td></tr><tr><td>DFM Sampling</td><td>63.20</td><td>0.41</td><td>19.90</td><td>17.00</td><td>2.85</td><td>91.36</td></tr><tr><td>RDM Sampling</td><td>78.79</td><td>0.65</td><td>12.13</td><td>48.57</td><td>3.11</td><td>92.70</td></tr><tr><td>TopK-Marginal</td><td>55.46</td><td>0.32</td><td>22.03</td><td>10.86</td><td>2.10</td><td>92.45</td></tr><tr><td>P2-Self (ours)</td><td>80.98</td><td>0.68</td><td>11.43</td><td>49.86</td><td>3.25</td><td>92.63</td></tr><tr><td>P2-Bert (ours)</td><td>70.80</td><td>0.51</td><td>16.09</td><td>35.43</td><td>2.36</td><td>90.66</td></tr><tr><td>P2-Train (ours)</td><td>83.45</td><td>0.72</td><td>10.15</td><td>58.86</td><td>3.35</td><td>92.69</td></tr></table>

Table 6: Language generation ablation: code generation (HumanEval) and story infilling (ROCStories).

<table><tr><td>Method</td><td>pass@1↑</td><td>ROUGE-1↑</td><td>ROUGE-2↑</td><td>ROUGE-L↑</td></tr><tr><td>Vanilla Ancestral</td><td>0.121</td><td>17.18</td><td>2.72</td><td>15.57</td></tr><tr><td>Greedy Ancestral</td><td>0.161</td><td>24.68</td><td>7.12</td><td>22.85</td></tr><tr><td>DFM Sampling</td><td>0.116</td><td>16.62</td><td>2.42</td><td>15.23</td></tr><tr><td>RDM Sampling</td><td>0.132</td><td>20.31</td><td>2.83</td><td>18.16</td></tr><tr><td>P2-Self (ours)</td><td>0.180</td><td>25.27</td><td>7.36</td><td>23.25</td></tr></table>

Summary. P2 generalizes and improves upon all major masked difusion sampling strategies. With its flexible decoding design, P2 can subsume Vanilla, Greedy, RDM, and DFM via appropriate planner configurations. Its variants—P2-Self, P2-Bert, and P2-Train—not only retain diversity but also unlock substantial gains in structural and functional accuracy across domains.

Table 7: RNA sequence generation ablation.

<table><tr><td>Method</td><td>pLDDT↑</td><td>MFE↓</td><td>Entropy↑</td><td>GC (%)↑</td></tr><tr><td>Vanilla Ancestral</td><td>68.12</td><td>-48.46</td><td>1.93</td><td>60.84</td></tr><tr><td>Greedy Ancestral</td><td>37.41</td><td>-32.32</td><td>1.66</td><td>49.27</td></tr><tr><td>DFM Sampling</td><td>33.17</td><td>-26.32</td><td>1.93</td><td>49.23</td></tr><tr><td>RDM Sampling</td><td>67.35</td><td>-47.54</td><td>1.89</td><td>59.42</td></tr><tr><td>P2-Self (ours)</td><td>69.41</td><td>-48.21</td><td>1.89</td><td>59.84</td></tr><tr><td>P2-Bert (ours)</td><td>73.28</td><td>-51.91</td><td>1.86</td><td>65.47</td></tr></table>

Additional ablations, including the efects of stochasticity η (Figure S2, Figure S5) and planner scale (Figure S3, Figure S6, Table S5), are provided in §G.2.3. In Table S6, we compare ELBO values between $G _ { \phi }$ and show that self-planning often outperforms BERT-based planning due to a better fit with the underlying denoiser. Further appendix results include analysis on short protein sequences ( Table S8), comparisons with baseline ESM2 ( Table S9), a comparison with Top-K Marginal (Kim et al., 2025) ( Table S10), and a robustness study reporting variance across runs ( Table S11).

## 4.5 Inference-Time Scaling and Computational Complexity

![](Peng2025Path_figs/8b730951c1440e60f5d151a32a0a5f8168216e5ca7455a69e1a17409b56fc9f2.jpg)  
Figure 3: Inference-time scaling: Foldability vs. Sampling steps.

![](Peng2025Path_figs/c403ff7f49563da6b86ba4ec645aec2f295d757f21640bb22508c793bcd49c5e.jpg)  
Figure 4: Runtime (bar) and throughput (line) for different planner sizes (150M denoiser on an A100).

A key strength of Path Planning (P2) is its resampling-based decoding mechanism, which allows flexible control over generation fidelity by varying the number of sampling steps. We evaluate P2 (Trained Planner,

8M) on protein sequence generation with varying sampling steps: {50, 100, 150, 200, 250, 300}, generating 300 sequences of length 200 for each setting. As shown in Figure 3, P2 consistently improves foldability with increased sampling steps and maintains its advantage beyond 200 steps, where other methods plateau.

Computational complexity. P2 ofers a tunable tradeof between sampling quality and runtime, depending on planner size. In Figure 4, we compare sampling speed across various planner models using a 150M denoiser on a single NVIDIA A100 GPU. All baseline strategies—including Vanilla, Greedy, DFM, RDM, and P2-Self—share a common “No Planner” runtime profile, yielding the highest throughput of 673.16 tokens/sec. Introducing an external planner naturally incurs additional cost. However, the 8M P2 planner—used in all protein experiments—maintains a strong balance, achieving 509.55 tokens/sec with only a 24% overhead.

## 5 Related Work

Masked difusion language models (MDMs) have emerged as promising alternatives to autoregressive models for discrete generation (Sahoo et al., 2024; Shi et al., 2024; Nie et al., 2025; Gong et al., 2025). To improve sampling, several heuristic methods—greedy unmasking (Gong et al., 2025), remasking (Zheng et al., 2023; Wang et al., 2024), and informed correctors (Zhao et al., 2024b)—have been proposed, though they lack structured guidance. Order-based strategies from Any-Order Autoregressive Models (AOARMs) (Li et al., 2021; Shih et al., 2022) enable greater flexibility but often require costly planners or fixed schedules. DDPD (Liu et al., 2024) separates planning and denoising, but operates on uniform difusion without mask-awareness. In contrast, our P2 sampler introduces a lightweight, modular mechanism for dynamic, mask-aware planning compatible with frozen denoisers. A detailed comparison with DDPD is provided in §D.4.

Recent work has sought to improve generation order in MDMs. ReMDM-conf (Wang et al., 2025a) schedules the temperature of the Gibbs distribution used in confidence-based informed correctors, while Kim et al. (2025) propose a Top-K heuristic based on local confidence gaps. Our path planning framework generalizes such strategies within a unified, optimizable, and principled formulation. Closest to our approach is LO-ARM (Wang et al., 2025c), which treats generation order as a latent variable and learns it via REINFORCE. However, its reliance on high-variance policy gradients limits scalability. Our method instead ofers a simple, diferentiable ELBO objective, enabling eficient and scalable learning of generation policies.

## 6 Conclusion

We demonstrate that unmasking order significantly impacts the generative performance of masked difusion language models (MDMs). By expanding the ELBO formulation, we introduce a planner that optimizes token selection during inference. We propose Path Planning (P2), a sampling framework that generalizes all existing MDM sampling strategies. P2 delivers state-of-the-art improvements across diverse tasks, including language generation and biological sequence design, enabling MDMs to outperform larger autoregressive models. Our findings highlight the importance of inference strategies in discrete difusion models, paving the way for more eficient and efective sequence generation.

## Ethics Statement

This work investigates improvements to discrete difusion models for generative modeling across text, code, and biological sequences. While our method, Path Planning (P2), demonstrates significant gains in generative quality, we recognize the potential for both positive and negative downstream impacts.

On the positive side, more efective discrete generative models can advance research in reasoning, programming, and biomolecular design. In particular, applications in protein and RNA sequence modeling may accelerate scientific discovery and therapeutic design. However, these same capabilities could also be misused, for instance in generating harmful or dual-use biological sequences. To mitigate this, all biological experiments in this work are purely computational and evaluated against standard, publicly available benchmarks; no wet-lab synthesis or functional validation was performed. We explicitly discourage and do not support the malicious application of our methods.

All datasets used are publicly available and widely adopted in the community. We have not introduced new data that could expose private or sensitive information. Our models are trained and released in accordance with open-science practices, but with careful documentation of intended use and limitations to discourage misuse.

## Reproducibility Statement

We provide the PyTorch implementation in Section E. For the experiments, we integrate our approach into the SMDM (Gong et al., 2025) GitHub codebase<sup>1</sup> to obtain the results for "MDM (1.1B) + P2" reported in Table 3. Similarly, the results for "DifuLLaMA (7B) + P2" in Table 3 are derived using the DifuLLaMA (Nie et al., 2025) GitHub codebase<sup>2</sup>. For the protein sequence generation experiments, we utilize the DPLM (Wang et al., 2024) open-source codebase<sup>3</sup>. The RNA sequence generation results are obtained by adapting the DPLM codebase for MDM training, combined with the RiNALMo (Penić et al., 2024) language model architecture.

## 7 Acknowledgments

Fred extends sincere gratitude to Jiaxin Shi, Xinyou Wang, Zaixiang Zheng, Chengtong Wang, and Bowen Jing, Kaiwen Zheng for their invaluable insights on DPLM. Fred devotes his special thank you to Tian Wang for playing ping-pong with him during the project and Divya Srijay, for reminding him what a factorial is. Zack extends his gratitude to Jim Nolen for his support and insightful discussions.

The authors acknowledge funding from UNIQUE, CIFAR, NSERC, Intel, Samsung, as well as the Hartwell Foundation and CHDI Foundation. The research was enabled in part by computational resources provided by the Digital Research Alliance of Canada (https://alliancecan.ca), Mila (https://mila.quebec), and NVIDIA. This research is partially supported by the EPSRC Turing AI World-Leading Research Fellowship No. EP/X040062/1 and EPSRC AI Hub No. EP/Y028872/1. Z.B. is partially supported by NSF-DMS award 2038056.

## 8 Author Contributions

F.Z.P. proposed the initial idea and conducted the experiments on language and protein modeling. Z.B. formulated the mathematical framework. S.P. carried out the experiments on RNA. F.Z.P. and Z.B. jointly wrote the manuscript, with all other authors contributing revisions and refinements. A.T., S.Y., and P.C. supervised the project.

## References

Josh Abramson, Jonas Adler, Jack Dunger, Richard Evans, Tim Green, Alexander Pritzel, Olaf Ronneberger, Lindsay Willmore, Andrew J Ballard, Joshua Bambrick, et al. Accurate structure prediction of biomolecular interactions with alphafold 3. Nature, pp. 1–3, 2024.

Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Florencia Leoni Aleman, Diogo Almeida, Janko Altenschmidt, Sam Altman, Shyamal Anadkat, et al. Gpt-4 technical report. arXiv, 2023.

Sarah Alamdari, Nitya Thakkar, Rianne van den Berg, Alex X. Lu, Nicolo Fusi, Ava P. Amini, and Kevin Kaichuang Yang. Protein generation with evolutionary difusion: sequence is all you need. bioRxiv, 2024.

Alan N. Amin, Nate Gruver, and Andrew Gordon Wilson. Why masking difusion works: Condition on the jump schedule for improved discrete difusion, 2025. URL https://arxiv.org/abs/2506.08316.

Jacob Austin, Daniel D. Johnson, Jonathan Ho, Daniel Tarlow, and Rianne van den Berg. Structured denoising difusion models in discrete state-spaces. arXiv, 2021.

Mohammad Bavarian, Heewoo Jun, Nikolas A. Tezak, John Schulman, Christine McLeavey, Jerry Tworek, and Mark Chen. Eficient training of language models to fill in the middle. arXiv, 2022.

Joe Benton, Yuyang Shi, Valentin De Bortoli, George Deligiannidis, and Arnaud Doucet. From denoising difusions to denoising markov models. Journal of the Royal Statistical Society Series B: Statistical Methodology, 86(2):286–301, 2024.

Lukas Berglund, Meg Tong, Max Kaufmann, Mikita Balesni, Asa Cooper Stickland, Tomasz Korbak, and Owain Evans. The reversal curse: Llms trained on "a is b" fail to learn "b is a". arXiv, 2023.

Stella Biderman, Hailey Schoelkopf, Lintang Sutawika, Leo Gao, Jonathan Tow, Baber Abbasi, Alham Fikri Aji, Pawan Sasanka Ammanamanchi, Sid Black, Jordan Clive, Anthony DiPofi, Julen Etxaniz, Benjamin Fattori, Jessica Zosa Forde, Charles Foster, Mimansa Jaiswal, Wilson Y. Lee, Haonan Li, Charles Lovering, Niklas Muennighof, Ellie Pavlick, Jason Phang, Aviya Skowron, Samson Tan, Xiangru Tang, Kevin A. Wang, Genta Indra Winata, Franccois Yvon, and Andy Zou. Lessons from the trenches on reproducible evaluation of language models. arXiv, 2024.

Amarjit Budhiraja and Paul Dupuis. Analysis and Approximation of Rare Events: Representations and Weak Convergence Methods, volume 94 of Probability Theory and Stochastic Modelling. Springer US, New York, NY, 2019. ISBN 978-1-4939-9577-6 978-1-4939-9579-0.

Andrew Campbell, Joe Benton, Valentin De Bortoli, Tom Rainforth, George Deligiannidis, and Arnaud Doucet. A continuous time framework for discrete denoising models, 2022.

Andrew Campbell, Jason Yim, Regina Barzilay, Tom Rainforth, and T. Jaakkola. Generative flows on discrete state-spaces: Enabling multimodal flows with applications to protein co-design. International Conference on Learning Representations, 2024

Huiwen Chang, Han Zhang, Lu Jiang, Ce Liu, and William T. Freeman. Maskgit: Masked generative image transformer. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), pp. 11315–11325, 2022a.

Huiwen Chang, Han Zhang, Lu Jiang, Ce Liu, and William T. Freeman. Maskgit: Masked generative image transformer, 2022b. URL https://arxiv.org/abs/2202.04200.

Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian, Mark Chen, Heewoo Jun, Lukasz Kaiser, Matthias Plappert, Jerry Tworek, Jacob Hilton, Reiichiro Nakano, Christopher Hesse, and John Schulman. Training verifiers to solve math word problems. arXiv, 2021.

Jacob Devlin, Ming-Wei Chang, Kenton Lee, and Kristina Toutanova. Bert: Pre-training of deep bidirectional transformers for language understanding. In North American Chapter of the Association for Computational Linguistics, 2019.

Floor Eijkelboom, Grigory Bartosh, Christian Andersson Naesseth, Max Welling, and Jan-Willem van de Meent. Variational flow matching for graph generation. Neural Information Processing Systems, 2024.

Itai Gat, Tal Remez, Neta Shaul, Felix Kreuk, Ricky T. Q. Chen, Gabriel Synnaeve, Yossi Adi, and Yaron Lipman. Discrete flow matching. Neural Information Processing Systems, 2024.

Daniel T Gillespie. A general method for numerically simulating the stochastic time evolution of coupled chemical reactions. Journal of Computational Physics, 22(4):403–434, 1976. ISSN 0021-9991.

Daniel T. Gillespie. Exact stochastic simulation of coupled chemical reactions. The Journal of Physical Chemistry, 81(25):2340–2361, 1977. ISSN 0022-3654.

Shansan Gong, Shivam Agarwal, Yizhe Zhang, Jiacheng Ye, Lin Zheng, Mukai Li, Chenxin An, Peilin Zhao, Wei Bi, Jiawei Han, Hao Peng, and Lingpeng Kong. Scaling difusion language models via adaptation from autoregressive models. International Conference on Learning Representations, 2025.

Ishaan Gulrajani and Tatsunori Hashimoto. Likelihood-based difusion language models. Neural Information Processing Systems, 2023.

Thomas Hayes, Roshan Rao, Halil Akin, Nicholas J. Sofroniew, Deniz Oktay, Zeming Lin, Robert Verkuil, Vincent Q. Tran, Jonathan Deaton, Marius Wiggert, Rohil Badkundri, Irhum Shafkat, Jun Gong, Alexander Derry, Raul S. Molina, Neil Thomas, Yousuf A. Khan, Chetan Mishra, Carolyn Kim, Liam J. Bartie, Matthew Nemeth, Patrick D. Hsu, Tom Sercu, Salvatore Candido, and Alexander Rives. Simulating 500 million years of evolution with a language model. Science, 2025.

Brian L. Hie, Duo Xu, Varun R. Shanker, Theodora U. J. Bruun, Payton A.-B. Weidenbacher, Shaogeng Tang, and Peter S. Kim. Eficient evolution of human antibodies from general protein language models and sequence information alone. Nature Biotechnology, 2024.

Emiel Hoogeboom, Alexey A. Gritsenko, Jasmijn Bastings, Ben Poole, Rianne van den Berg, and Tim Salimans. Autoregressive difusion models. In 10th International Conference on Learning Representations, 2022.

Jean Jacod and Albert Shiryaev. Limit theorems for stochastic processes, volume 288. Springer Science & Business Media, 2013.

Mandar Joshi, Eunsol Choi, Daniel Weld, and Luke Zettlemoyer. TriviaQA: A large scale distantly supervised challenge dataset for reading comprehension. In Proceedings of the 55th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), 2017.

Peter Kerpedjiev, Stefan Hammer, and Ivo L Hofacker. Forna (force-directed rna): Simple and efective online rna secondary structure diagrams. Bioinformatics, 31(20):3377–3379, 2015.

Jaeyeon Kim, Kulin Shah, Vasilis Kontonis, Sham Kakade, and Sitan Chen. Train for the worst, plan for the best: Understanding token ordering in masked difusions. arXiv, 2025.

Zhenzhong Lan, Mingda Chen, Sebastian Goodman, Kevin Gimpel, Piyush Sharma, and Radu Soricut. Albert: A lite bert for self-supervised learning of language representations. International Conference on Learning Representations, 2020.

Xuanlin Li, Brandon Trabucco, Dong Huk Park, Michael Luo, Sheng Shen, Trevor Darrell, and Yang Gao. Discovering non-monotonic autoregressive orderings with variational inference. International Conference on Learning Representations, 2021.

Chin-Yew Lin. ROUGE: A package for automatic evaluation of summaries. In Text Summarization Branches Out, pp. 74–81, Barcelona, Spain, July 2004. Association for Computational Linguistics.

Zeming Lin, Halil Akin, Roshan Rao, Brian Hie, Zhongkai Zhu, Wenting Lu, Nikita Smetanin, Robert Verkuil, Ori Kabeli, Yaniv Shmueli, Allan dos Santos Costa, Maryam Fazel-Zarandi, Tom Sercu, Salvatore Candido, and Alexander Rives. Evolutionary-scale prediction of atomic-level protein structure with a language model. Science, 379(6637):1123–1130, 2023.

Sulin Liu, Juno Nam, Andrew Campbell, Hannes Stärk, Yilun Xu, T. Jaakkola, and Rafael G’omez-Bombarelli. Think while you generate: Discrete difusion with planned denoising. International Conference on Learning Representations, 2024.

Yinhan Liu, Myle Ott, Naman Goyal, Jingfei Du, Mandar Joshi, Danqi Chen, Omer Levy, Mike Lewis, Luke Zettlemoyer, and Veselin Stoyanov. Roberta: A robustly optimized bert pretraining approach. arXiv, 2019.

Ronny Lorenz, Stephan H Bernhart, Christian Höner zu Siederdissen, Hakim Tafer, Christoph Flamm, Peter F Stadler, and Ivo L Hofacker. Viennarna package 2.0. Algorithms for molecular biology, 6:1–14, 2011.

Aaron Lou, Chenlin Meng, and Stefano Ermon. Discrete difusion modeling by estimating the ratios of the data distribution. In International Conference on Machine Learning, 2023.

Ang Lv, Kaiyi Zhang, Shufang Xie, Quan Tu, Yuhan Chen, Ji-Rong Wen, and Rui Yan. Are we falling in a middle-intelligence trap? an analysis and mitigation of the reversal curse. arXiv preprint arXiv:2311.07468, 2023.

N. Mostafazadeh, Nathanael Chambers, Xiaodong He, Devi Parikh, Dhruv Batra, Lucy Vanderwende, Pushmeet Kohli, and James F. Allen. A corpus and cloze evaluation for deeper understanding of commonsense stories. arXiv, 2016.

Shen Nie, Fengqi Zhu, Chao Du, Tianyu Pang, Qian Liu, Guangtao Zeng, Min Lin, and Chongxuan Li. Scaling up masked difusion models on text. International Conference on Learning Representations, 2025.

Erik Nijkamp, Jefrey A. Rufolo, Eli N. Weinstein, Nikhil Vijay Naik, and Ali Madani. Progen2: Exploring the boundaries of protein language models. Cell systems, 2022.

Jingyang Ou, Shen Nie, Kaiwen Xue, Fengqi Zhu, Jiacheng Sun, Zhenguo Li, and Chongxuan Li. Your absorbing discrete difusion secretly models the conditional distributions of clean data. arXiv, 2024.

Denis Paperno, Germán Kruszewski, Angeliki Lazaridou, Quan Ngoc Pham, Rafaella Bernardi, Sandro Pezzelle, Marco Baroni, Gemma Boleda, and R. Fernández. The lambada dataset: Word prediction requiring a broad discourse context. arXiv, 2016.

Kishore Papineni, Salim Roukos, Todd Ward, and Wei-Jing Zhu. Bleu: a method for automatic evaluation of machine translation. In Proceedings of the 40th annual meeting of the Association for Computational Linguistics, pp. 311–318, 2002.

Rafael Josip Penić, Tin Vlašić, Roland G Huber, Yue Wan, and Mile Šikić. Rinalmo: General-purpose rna language models can generalize well on structure prediction tasks. arXiv, 2024.

Anton I. Petrov. Rnacentral 2021: secondary structure integration, improved sequence search and new member databases. Nucleic acids research, 49(D1):D212–D220, 2021.

Yinuo Ren, Haoxuan Chen, Grant M. Rotskof, and Lexing Ying. How discrete and continuous difusion meet: Comprehensive analysis of discrete difusion models via a stochastic integral framework. arXiv, 2024.

Robin Rombach, Andreas Blattmann, Dominik Lorenz, Patrick Esser, and Björn Ommer. High-resolution image synthesis with latent difusion models. In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, pp. 10684–10695, 2022.

Subham Sekhar Sahoo, Marianne Arriola, Aaron Gokaslan, Edgar Mariano Marroquin, Alexander M Rush, Yair Schif, Justin T Chiu, and Volodymyr Kuleshov. Simple and efective masked difusion language models. In The Thirty-eighth Annual Conference on Neural Information Processing Systems, 2024.

Yair Schif, Subham Sekhar Sahoo, Hao Phung, Guanghan Wang, Sam Boshar, Hugo Dalla-torre, Bernardo P. de Almeida, Alexander Rush, Thomas Pierrot, and Volodymyr Kuleshov. Simple guidance mechanisms for discrete difusion models. International Conference on Learning Representations, 2025.

Tao Shen, Zhihang Hu, Siqi Sun, Di Liu, Felix Wong, Jiuming Wang, Jiayang Chen, Yixuan Wang, Liang Hong, Jin Xiao, et al. Accurate rna 3d structure prediction using a language model-based deep learning approach. Nature Methods, pp. 1–12, 2024.

Jiaxin Shi, Kehang Han, Zhe Wang, Arnaud Doucet, and Michalis K Titsias. Simplified and generalized masked difusion for discrete data. arXiv, 2024.

Andy Shih, Dorsa Sadigh, and Stefano Ermon. Training and inference on any-order autoregressive models the right way. Neural Information Processing Systems, 2022.

Jascha Sohl-Dickstein, Eric Weiss, Niru Maheswaranathan, and Surya Ganguli. Deep unsupervised learning using nonequilibrium thermodynamics. In Francis Bach and David Blei (eds.), Proceedings of the 32nd International Conference on Machine Learning, volume 37 of Proceedings of Machine Learning Research, pp. 2256–2265, Lille, France, 07–09 Jul 2015. PMLR. URL https://proceedings.mlr.press/v37/ sohl-dickstein15.html.

Haoran Sun, Lijun Yu, Bo Dai, Dale Schuurmans, and Hanjun Dai. Score-based continuous-time discrete difusion models. International Conference on Learning Representations, 2023.

Hugo Touvron, Louis Martin, Kevin R. Stone, Peter Albert, Amjad Almahairi, Yasmine Babaei, Nikolay Bashlykov, Soumya Batra, Prajjwal Bhargava, Shruti Bhosale, Daniel M. Bikel, Lukas Blecher, Cristian Cantón Ferrer, Moya Chen, Guillem Cucurull, David Esiobu, Jude Fernandes, Jeremy Fu, Wenyin Fu, Brian Fuller, Cynthia Gao, Vedanuj Goswami, Naman Goyal, Anthony S. Hartshorn, Saghar Hosseini, Rui Hou, Hakan Inan, Marcin Kardas, Viktor Kerkez, Madian Khabsa, Isabel M. Kloumann, A. V. Korenev, Punit Singh Koura, Marie-Anne Lachaux, Thibaut Lavril, Jenya Lee, Diana Liskovich, Yinghai Lu, Yuning Mao, Xavier Martinet, Todor Mihaylov, Pushkar Mishra, Igor Molybog, Yixin Nie, Andrew Poulton, Jeremy Reizenstein, Rashi Rungta, Kalyan Saladi, Alan Schelten, Ruan Silva, Eric Michael Smith, R. Subramanian, Xia Tan, Binh Tang, Ross Taylor, Adina Williams, Jian Xiang Kuan, Puxin Xu, Zhengxu Yan, Iliyan Zarov, Yuchen Zhang, Angela Fan, Melissa Hall Melanie Kambadur, Sharan Narang, Aurélien Rodriguez, Robert Stojnic, Sergey Edunov, and Thomas Scialom. Llama 2: Open foundation and fine-tuned chat models. arXiv, 2023.

Benigno Uria, Iain Murray, and Hugo Larochelle. A deep and tractable density estimator. In Proceedings of the 31th International Conference on Machine Learning, 2014.

Guanghan Wang, Yair Schif, Subham Sekhar Sahoo, and Volodymyr Kuleshov. Remasking discrete difusion models with inference-time scaling. arXiv, 2025a.

Xinyou Wang, Zaixiang Zheng, Fei Ye, Dongyu Xue, Shujian Huang, and Quanquan Gu. Difusion language models are versatile protein learners. International Conference on Machine Learning, 2024.

Xinyou Wang, Zaixiang Zheng, Fei Ye, Dongyu Xue, Shujian Huang, and Quanquan Gu. Dplm-2: A multimodal difusion protein language model. International Conference on Learning Representations, 2025b.

Zhe Wang, Jiaxin Shi, Nicolas Heess, Arthur Gretton, and Michalis K. Titsias. Learning-order autoregressive models with application to molecular graph generation. arXiv, 2025c.

Joseph L Watson, David Juergens, Nathaniel R Bennett, Brian L Trippe, Jason Yim, Helen E Eisenach, Woody Ahern, Andrew J Borst, Robert J Ragotte, Lukas F Milles, et al. De novo design of protein structure and function with rfdifusion. Nature, 620(7976):1089–1100, 2023.

G. George Yin and Qing Zhang. Continuous-Time Markov Chains and Applications, volume 37 of Stochastic Modelling and Applied Probability. Springer, New York, NY, 2013.

Lingxiao Zhao, Xueying Ding, Lijun Yu, and Leman Akoglu. Unified discrete difusion for categorical data. arXiv, 2024a.

Yixiu Zhao, Jiaxin Shi, Lester Mackey, and Scott Linderman. Informed correctors for discrete difusion models. arXiv, 2024b.

Kaiwen Zheng, Yongxin Chen, Hanzi Mao, Mingying Liu, Jun Zhu, and Qinsheng Zhang. Masked difusion models are secretly time-agnostic masked models and exploit inaccurate categorical sampling, 2025.

Lin Zheng, Jianbo Yuan, Lei Yu, and Lingpeng Kong. A reparameterized discrete difusion model for text generation. arXiv, 2023.

## Appendices

A Related Works: Extended Discussion 19   
B Proofs of Propositions 1 and 2 19   
B.1 Proof of Proposition 1: Time Discretization Approach . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . B.2 Finding the Optimal Planner Under the ELBO-informed Loss: Proposition 2 24   
B.3 Form of the ELBO for Varying $\eta$ 26   
B.4 Proof of Lemma 1 26   
B.5 Deriving the Discrete Time ELBO Eq. 10 27   
C Additional Background: Continuous Time Perspective 28   
C.1 Discrete Diffusion/Flow Models: Continuous Time Problem Setup 28   
C.2 Time-Inhomogeneous Continuous Time Markov Chains (CTMC) 29   
C.3 The Role of the Denoiser and the Approximate Backwards Process 29   
C.4 The Conditional Backwards Process 30   
C.5 Masked Diffusion Model: Continuous Time Formulation 30   
C.6 Role of the ELBO 31   
D Mathematical Details: P2 from a CTMC Point of View 32   
D.1 P2 Continuous Time Formulation 32   
D.2 Proof of the ELBO Proposition 1: CTMC Version 33   
D.3 Equivalence of MDMs with AOARMs 34   
D.4 Comparison with Other Sampling Methods 36   
D.5 Deriving the P2 Gillespie Scheme Algorithm 5 38   
E Implementation Details 40   
F Experimental Details 42   
F.1 Protein Generation Evaluation Details 42   
F.2 Language Generation Evaluation Details 44   
F.3 RNA Generation Details 44   
F.4 RNA Evaluation Details 44   
G Additional Results 46   
G.1 Language Generation 46   
G.2 Protein Generation 47   
G.3 RNA Generation 58

## A Related Works: Extended Discussion

Masked difusion language models (MDMs) represent a promising alternative to autoregressive models for discrete data generation, particularly in language modeling. Recent advancements have focused on simplifying and generalizing the MDM framework to improve performance and training eficiency (Shi et al., 2024; Sahoo et al., 2024). These studies introduced a continuous-time variational objective for MDMs, expressed as a weighted integral of cross-entropy losses, facilitating the training of models with state-dependent masking schedules. At the GPT-2 scale, these MDMs outperformed prior difusion-based language models and demonstrated superior capabilities in zero-shot language modeling tasks (Nie et al., 2025; Gong et al., 2025).

MDMs generate sequences starting from a fully masked input and progressively unmasking positions until a clean sequence is reached. Once a token is unmasked, it will stay unchanged. However, there is not guarantee that the state is correct, considering the approximation errors arise from the imperfect fit to real-world data distributions. Additionally, time discretization (Zhao et al., 2024b) and numerical errors (Zheng et al., 2025) may further the error incurred during sampling processes.

To address these challenges, several solutions have been proposed. These include methods allowing models to revise prior predictions and guiding sampling trajectories using internal or external knowledge. Examples include informed correctors (Zhao et al., 2024b), greedy ancestral methods (Gong et al., 2025), and RDM sampling techniques (Zheng et al., 2023; Wang et al., 2024), which leverage model scores to replace random masking with targeted corrections. None of these works, however, allow for the use of an external planner, and (Zheng et al., 2023; Wang et al., 2024) are simply using a top-k sampling strategy without any concern for the theoretical underpinnings of the sampling strategies viability.

In terms of theoretically-backed methods for selecting the denoising order during a generative model’s sampling process, the current literature is quite sparse. Shih et al. (2022); Li et al. (2021) discuss this task from the perspective of Any-Order Autoregressive models, with Li et al. (2021) requiring a specially-trained external planner model using a specially designed architecture and Shih et al. (2022) taking the perspective that a fixed family of possible generation orders should be chosen a priori to eliminate redundancy.

The most closely related work to ours is likely the recent DDPD (Liu et al., 2024) introduced a generative process divided into a planner, which identifies corrupted positions, and a denoiser, which refines these positions. Though they discuss the ability to employ a MDM denoiser within their framework, their analysis and sampling is through the lens of uniform discrete difusion models. In particular, as with Li et al. (2021), the success of their strategy is contingent upon training a large specialized planner model of comparable size to the denoiser itself. Moreover, in their framework, since they are based on uniform difusion models, the partially de-noised sequence never contains any masked states, and there is no way for the planner to be separated into masked and unmasked components to design a sampling strategy with guaranteed finite-time along the lines of our Algorithm 1. Given the possible perceived similarity of this work with ours, we provide a thorough comparison of DDPD with P2 in Algorithm 4, highlighting the greater flexibility and diference in role of P2s’ planners.

## B Proofs of Propositions 1 and 2

## B.1 Proof of Proposition 1: Time Discretization Approach

In this section we provide a self-contained proof of Proposition 1, using directly a lower bound for the time-discretized, coordinate-wise conditionally independent dynamics Eq. 5. We refer the reader interested in a direct and more concise proof of Proposition 1 using the theory of continuous time Markov chains (see Section C for the definition and basic theory thereof) to Section D.

Proposition 1. Define $P _ { 0 } ^ { \theta , \phi } \in \Delta ^ { d ^ { L } }$ by $P _ { 0 } ^ { \theta , \phi } ( \mathbf { x } ) = \mathbb { P } ( X _ { 0 } ^ { \theta , \phi } = \mathbf { x } )$ , where $X ^ { \theta , \phi }$ is the continuous time Markov chain resulting from sending $T $ ∞ in the discrete-time P2 formulation Eq. 5. Then we have an “Evidence Based Lower Bound” $" \mathcal { E } ( \mathbf { x } _ { 0 } ) \leq \log ( P _ { 0 } ^ { \theta , \phi } ( \mathbf { x } _ { 0 } ) )$ ) for each fixed $\mathbf { x } _ { 0 } \in \mathcal { V } ^ { L }$ given by $\mathcal { E } ( \mathbf { x } _ { 0 } ) = \mathcal { E } _ { M P } ( \mathbf { x } _ { 0 } ) + \mathcal { E } _ { U P } ( \mathbf { x } _ { 0 } ) +$

$\mathcal { E } _ { D } ( \mathbf { x } _ { 0 } )$ , where:

$$
\begin{array}{l} \mathcal {E} _ {M P} (\mathbf {x} _ {0}) = - \int_ {0} ^ {1} \frac {d \alpha_ {t}}{d t} \cdot \frac {1}{1 - \alpha_ {t}} \mathbb {E} _ {\mathbf {x} _ {t} \sim \mathbf {p} _ {t} (\cdot ; \mathbf {x} _ {0})} \left[ \sum_ {i = 1, \mathbf {x} _ {t} ^ {i} = \mathbf {m}} ^ {L} \mathbb {E} _ {\mathbf {z} \sim D _ {\theta} (\mathbf {x} _ {t})} \left[ C E \left(C a t (z ^ {i}; \delta (x _ {0} ^ {i})), G _ {M} ^ {i} (\mathbf {z}, \mathbf {x} _ {t})\right) \right] \right] d t \\ \mathcal {E} _ {U P} (\mathbf {x} _ {0}) = - \int_ {0} ^ {1} \frac {d \alpha_ {t}}{d t} \cdot \frac {1}{1 - \alpha_ {t}} \mathbb {E} _ {\mathbf {x} _ {t} \sim \mathbf {p} _ {t} (\cdot ; \mathbf {x} _ {0})} \left[ {\sum_ {i = 1, \mathbf {x} _ {t} ^ {i} \neq \mathbf {m}} ^ {L}} \mathbb {E} _ {\mathbf {z} \sim D _ {\theta} (\mathbf {x} _ {t})} \left[ C E \left(C a t (z ^ {i}; \delta (x _ {0} ^ {i})), G _ {U} ^ {i} (\mathbf {z}, \mathbf {x} _ {t})\right) \right] \right] d t \\ \mathcal {E} _ {D} (\mathbf {x} _ {0}) = - \int_ {0} ^ {1} \frac {d \alpha_ {t}}{d t} \cdot \frac {1}{1 - \alpha_ {t}} \mathbb {E} _ {\mathbf {x} _ {t} \sim \mathbf {p} _ {t} (\cdot ; \mathbf {x} _ {0})} \left[ \underset {i = 1, \mathbf {x} _ {t} ^ {i} = \mathbf {m}} {\sum_ {i = 1, \mathbf {x} _ {t} ^ {i} = \mathbf {m}} ^ {L}} \delta (\mathbf {x} _ {0} ^ {i}) ^ {\top} \log (D _ {\theta} ^ {i} (\mathbf {x} _ {t})) \right] d t. \end{array}
$$

Here $\mathbf { p } _ { t }$ is defined per $E q .$ 1 and $C E ( a , b ) = a \log ( b ) + ( 1 - a ) \log ( 1 - b ) \ f o r \ a , b \in [ 0 , 1 ]$ , with 0 log $0 = 0$

Consider $\mathbf { q } _ { \theta } ^ { T }$ the distribution on $\mathcal { V } ^ { L }$ resulting from iteratively sampling independently in each coordinate according to Eq. 5, with initial data $( \mathbf { m } , \ldots , \mathbf { m } )$ . Our starting point is the standard standard ELBO in discrete time used for difusion models Sohl-Dickstein et al. (2015). That is, fixing $\mathbf { x } _ { T } = ( \mathbf { m } , \ldots , \mathbf { m } )$ , we let $\mathbf { q } _ { t , \theta } ^ { T } ( \mathbf { x } _ { t - 1 } | \mathbf { x } _ { t } )$ be the one-step transition probabilities describing our time-discretized sampling scheme on $\mathcal { V } ^ { L }$

$$
\begin{array}{r} \mathbf {q} _ {t, \theta} ^ {T} (\mathbf {x} _ {t - 1} | \mathbf {x} _ {t}) = \mathbb {E} _ {\mathbf {z} \sim D _ {\theta} (\mathbf {x} _ {t})} \left[ \mathbf {q} _ {t, \theta} ^ {T} (\mathbf {x} _ {t - 1} | \mathbf {x} _ {t}, \mathbf {z}) \right] \\ \mathbf {q} _ {t, \theta} ^ {T} (\mathbf {x} _ {t - 1} | \mathbf {x} _ {t}, \mathbf {z}) = \prod_ {i = 1} ^ {L} q _ {t, \theta} (x _ {t - 1} ^ {i} | \mathbf {x} _ {t}, \mathbf {z}), \end{array}\tag{8}
$$

with $q _ { t , \theta } \big ( x _ { t - 1 } ^ { i } \big | \mathbf { x } _ { t } , \mathbf { z } \big )$ as in Eq. 5. Note that this follows immediately from the assumed conditional independence and marginalizing over the independent samples z. We also let $\mathbf { q } _ { t } ^ { T } ( \mathbf { x } _ { t - 1 } | \mathbf { x } _ { t } , \mathbf { x } _ { 0 } )$ be the one-step transitions for the reference reverse process on $\mathcal { V } ^ { L }$ given by

$$
\mathbf {q} _ {t} ^ {T} (\mathbf {x} _ {t - 1} | \mathbf {x} _ {t}, \mathbf {x} _ {0}) = \prod_ {i = 1} ^ {L} q _ {t} (x _ {t - 1} ^ {i} | x _ {t} ^ {i}, x _ {0} ^ {i}).\tag{9}
$$

for $q ( x _ { t - 1 } ^ { i } | x _ { t } ^ { i } , x _ { 0 } ^ { i } )$ as in Eq. 2.

Then the discrete time ELBO reads:

$$
\begin{array}{r l} & {\log (\mathbf {q} _ {\theta} ^ {T} (\mathbf {x} _ {0}) \geq - \sum_ {t = T} ^ {2} \sum_ {\mathbf {x} _ {t} \in \mathcal {V} ^ {L}} \hat {\mathbf {q}} _ {t} ^ {T} (\mathbf {x} _ {t} | \mathbf {x} _ {0}) \sum_ {\mathbf {x} _ {t - 1} \in \mathcal {V} ^ {L}} \mathbf {q} _ {t} ^ {T} (\mathbf {x} _ {t - 1} | \mathbf {x} _ {t}, \mathbf {x} _ {0}) \log \left(\frac {\mathbf {q} _ {t} ^ {T} (\mathbf {x} _ {t - 1} | \mathbf {x} _ {t} , \mathbf {x} _ {0})}{\mathbf {q} _ {t , \theta} ^ {T} (\mathbf {x} _ {t - 1} | \mathbf {x} _ {t})}\right)} \\ & {\quad + \sum_ {\mathbf {x} _ {1} \in \mathcal {V} ^ {L}} \hat {\mathbf {q}} _ {1} ^ {T} (\mathbf {x} _ {1} | \mathbf {x} _ {0}) \log (\mathbf {q} _ {1, \theta} ^ {T} (\mathbf {x} _ {0} | \mathbf {x} _ {1})),} \end{array}\tag{10}
$$

where $\hat { \mathbf { q } } _ { t } ^ { T } ( \mathbf x _ { t } | \mathbf x _ { 0 } )$ is the distribution at timestep t of the backward dynamics with transition probabilities Eq. 9 with initial data $\mathbf { x } _ { T } = ( \mathbf { m } , \ldots , \mathbf { m } )$ . For reference, we include a derivation of this result in the following subsection B.5.

We will use Eq. 10 to show lim $_ { T  \infty } \log ( \mathbf { q } _ { \theta } ^ { T } ( \mathbf { x } _ { 0 } ) \geq \mathcal { E } ( \mathbf { x } _ { 0 } )$ from Proposition 1.

In the proof, we will make use of the following Lemma, the proof of which is delayed to subsection B.4.

Lemma 1. For $\mathbf { x } \neq \mathbf { y } \in \mathcal { V } ^ { L } , \mathbf { x } _ { 0 } \in \mathcal { V } ^ { L }$ , and setting $t = \lfloor s T \rfloor$ for fixed $s \in ( 0 , 1 )$ , we have the following limits:

$$
\lim _ {T \to \infty} \hat {\mathbf {q}} _ {t} ^ {T} (\mathbf {x} | \mathbf {x} _ {0}) = \mathbf {p} _ {1 - s} (\mathbf {x} | \mathbf {x} _ {0}),\tag{11}
$$

$$
\lim _ {T \to \infty} \hat {\mathbf {q}} _ {1} ^ {T} (\mathbf {x} _ {0} | \mathbf {x} _ {0}) = 1\tag{12}
$$

$$
\lim _ {T \to \infty} T \mathbf {q} _ {t} ^ {T} (\mathbf {y} | \mathbf {x}, \mathbf {x} _ {0})\tag{13}
$$

$$
= \left\{ \begin{array}{l l} - \frac {\alpha_ {1 - s} ^ {\prime}}{1 - \alpha_ {1 - s}}   C a t \bigg (y ^ {i}; \delta (x _ {0} ^ {i}) \bigg)   C a t \bigg (x ^ {i}; \delta (\mathbf {m}) \bigg) & , d _ {H A M} (\mathbf {x}, \mathbf {y}) = 1, x ^ {i} \neq y ^ {i} \\ 0 & , o t h e r w i s e \end{array} \right.
$$

$$
\lim _ {T \to \infty} T \mathbf {q} _ {t, \theta} ^ {T} (\mathbf {y} | \mathbf {x})\tag{14}
$$

$$
= - \frac {\alpha_ {1 - s} ^ {\prime}}{1 - \alpha_ {1 - s}} \left\{ \begin{array}{l l} C a t (y ^ {i}; D _ {\theta} ^ {i} (\mathbf {x})) \mathbb {E} _ {\mathbf {z} \sim D _ {\theta} (\mathbf {x})} \left[ G _ {\phi} ^ {i} (\mathbf {z} ^ {- i, y ^ {i}}, \mathbf {x}) \right] & , d _ {H A M} (\mathbf {x}, \mathbf {y}) = 1, x ^ {i} \neq y ^ {i}, x ^ {i} = \mathbf {m} \\ \frac {\mathbb {E} _ {\mathbf {z} \sim D _ {\theta} (\mathbf {x})} \left[ G _ {\phi} ^ {i} (\mathbf {z} , \mathbf {x}) \right]}{1 - C a t (x ^ {i} ; D _ {\theta} ^ {i} (\bar {\mathbf {x}})} C a t (y ^ {i}; D _ {\theta} ^ {i} (\bar {\mathbf {x}})) & , d _ {H A M} (\mathbf {x}, \mathbf {y}) = 1, x ^ {i} \neq y ^ {i}, x ^ {i} \neq \mathbf {m} \\ 0, & o t h e r w i s e \end{array} \right.,
$$

where here we recall $d _ { H A M }$ refers to the Hamming distance, and the notation $\mathbf { z } ^ { - i , y ^ { i } }$ means replacing the i’th coordinate of z with $y ^ { i }$

We now proceed with the proof of Proposition 1.

Proof. First we observe that, from Eq. 12, in the limit as $T \to \infty$ , the reconstruction loss - i.e. the second term in Eq. 10 - vanishes. We thus turn our attention to bounding the first term.

We observe first that we are seeking to find

$$
\lim _ {T \to \infty} \sum_ {t = T} ^ {2} f ^ {T} (t) = \lim _ {T \to \infty} \frac {1}{T} \sum_ {t = T} ^ {2} T f ^ {T} (t)
$$

for a sequence of functions $f ^ { T } : \{ 2 , \dots , T \}  \mathbb { R }$ , with $f ^ { T } ( t ) = g ^ { T } ( t / T )$ for $g ^ { T } : [ 0 , 1 ] \to \mathbb { R }$ . With the uniform integrability of $T g ^ { T }$ , this converges to the Riemann integral

$$
\int_ {0} ^ {1} \lim _ {T \to \infty} T f ^ {T} (\lfloor T s \rfloor) d s.\tag{15}
$$

We identified the limit of $\hat { \mathbf { q } }$ for the outermost sum in $\operatorname { E q }$ . 10 in $\operatorname { E q }$ . 11. Now we turn to finding:

$$
\lim _ {T \to \infty} - T \sum_ {\mathbf {x} _ {t - 1} \in \mathcal {V} ^ {L}} \mathbf {q} _ {t} ^ {T} (\mathbf {x} _ {t - 1} | \mathbf {x} _ {t}, \mathbf {x} _ {0}) \log \left(\frac {\mathbf {q} _ {t} ^ {T} (\mathbf {x} _ {t - 1} | \mathbf {x} _ {t} , \mathbf {x} _ {0})}{\mathbf {q} _ {t , \theta} ^ {T} (\mathbf {x} _ {t - 1} | \mathbf {x} _ {t})}\right), t = \lfloor s T \rfloor ,
$$

after which we will use $\operatorname { E q . }$ 15 and Eq. 11 to replace the outermost sum over times in $\operatorname { E q } .$ 9 with an integral, the sum over $\mathbf { x } _ { t }$ with the expected value against $\mathbf { p } _ { 1 - s }$ , and the terms in the integrand with the above limit.

We treat this as two terms:

$$
E _ {1} ^ {\infty} (\mathbf {x} _ {0}, \mathbf {x}, s) = \sum_ {\mathbf {y} \in \mathcal {V} ^ {L}, \mathbf {y} \neq \mathbf {x}} \lim _ {T \to \infty} - T \mathbf {q} _ {t} ^ {T} (\mathbf {y} | \mathbf {x}, \mathbf {x} _ {0}) \log \left(\frac {\mathbf {q} _ {t} ^ {T} (\mathbf {y} | \mathbf {x} , \mathbf {x} _ {0})}{\mathbf {q} _ {t , \theta} ^ {T} (\mathbf {y} | \mathbf {x})}\right), \quad t = \lfloor s T \rfloor\tag{16}
$$

and

$$
E _ {2} ^ {\infty} (\mathbf {x} _ {0}, \mathbf {x}, s) = \lim _ {T \to \infty} - T \mathbf {q} _ {t} ^ {T} (\mathbf {x} | \mathbf {x}, \mathbf {x} _ {0}) \log \left(\frac {\mathbf {q} _ {t} ^ {T} (\mathbf {x} | \mathbf {x} , \mathbf {x} _ {0})}{\mathbf {q} _ {t , \theta} ^ {T} (\mathbf {x} | \mathbf {x})}\right), \quad t = \lfloor s T \rfloor .\tag{17}
$$

We begin with Eq. 16. Using for $\mathbf x \neq \mathbf y \in \mathcal V ^ { L } , t = \lfloor s T \rfloor$

$$
\begin{array}{l} \lim _ {T \to \infty} - T \mathbf {q} _ {t} ^ {T} (\mathbf {y} | \mathbf {x}, \mathbf {x} _ {0}) \log \left(\frac {\mathbf {q} _ {t} ^ {T} (\mathbf {y} | \mathbf {x} , \mathbf {x} _ {0})}{\mathbf {q} _ {t , \theta} ^ {T} (\mathbf {y} | \mathbf {x})}\right) \\ = \lim _ {T \to \infty} - T \mathbf {q} _ {t} ^ {T} (\mathbf {y} | \mathbf {x}, \mathbf {x} _ {0}) \log \left(\frac {\lim _ {T \to \infty} T \mathbf {q} _ {t} ^ {T} (\mathbf {y} | \mathbf {x} , \mathbf {x} _ {0})}{\lim _ {T \to \infty} T \mathbf {q} _ {t , \theta} ^ {T} (\mathbf {y} | \mathbf {x})}\right), \end{array}
$$

where we interpret 0 log $0 = 0$ , and Eq. 13, Eq. 14, every term in the sum becomes 0 when $d _ { \mathrm { H A M } } ( \mathbf { x } , \mathbf { y } ) > 1$ 2 $y ^ { i } \neq x _ { 0 } ^ { i }$ , or $x ^ { i } \neq \mathbf { m }$ , and we arrive at:

$$
\begin{array}{r l} & E _ {1} ^ {\infty} (\mathbf {x} _ {0}, \mathbf {x}, s) = \frac {\alpha_ {1 - s} ^ {\prime}}{1 - \alpha_ {1 - s}} \sum_ {i = 1, x ^ {i} = \mathbf {m}} ^ {L} \log \left(\frac {1}{\mathrm{Cat} (x _ {0} ^ {i} ; D _ {\theta} ^ {i} (\mathbf {x})) \mathbb {E} _ {\mathbf {z} \sim D _ {\theta} (\mathbf {x})} [ G _ {\phi} ^ {i} (\mathbf {z} ^ {- i , x _ {0} ^ {i}} , \mathbf {x}) ]}\right) \\ & \qquad = - \frac {\alpha_ {1 - s} ^ {\prime}}{1 - \alpha_ {1 - s}} \sum_ {i = 1, x ^ {i} = \mathbf {m}} ^ {L} \log \left(\mathrm{Cat} (x _ {0} ^ {i}; D _ {\theta} ^ {i} (\mathbf {x}))\right) \\ & \qquad - \frac {\alpha_ {1 - s} ^ {\prime}}{1 - \alpha_ {1 - s}} \sum_ {i = 1, x ^ {i} = \mathbf {m}} ^ {L} \log \left(\mathbb {E} _ {\mathbf {z} \sim D _ {\theta} (\mathbf {x})} [ G _ {\phi} ^ {i} (\mathbf {z} ^ {- i, x _ {0} ^ {i}}, \mathbf {x}) ]\right). \end{array}\tag{18}
$$

We now turn our attention to the limit Eq. 17. We first observe that, from $\operatorname { E q . 2 } $ for $x ^ { i } \in \mathcal { V } , t = \lfloor T s \rfloor$ ， lim $1 _ { T  \infty } q _ { t } ( x ^ { i } | x ^ { i } , x _ { 0 } ^ { i } ) = 1$ , so by definition of $\mathbf { q } _ { t } ^ { T }$ from Eq. 9, li $\begin{array} { r } { \mathbf { \eta } \mathrm { n } _ { T  \infty } \mathbf { q } _ { t } ^ { T } ( \mathbf { x } | \mathbf { x } , \mathbf { x } _ { 0 } ) = 1 } \end{array}$ . Then:

$$
\begin{array}{r l} & E _ {2} ^ {\infty} (\mathbf {x} _ {0}, \mathbf {x}, s) = \lim _ {T \to \infty} - T \log \left(\frac {\mathbf {q} _ {t} ^ {T} (\mathbf {x} | \mathbf {x} , \mathbf {x} _ {0})}{\mathbf {q} _ {t , \theta} ^ {T} (\mathbf {x} | \mathbf {x})}\right) \\ & \qquad = \lim _ {T \to \infty} - T \log \left(1 - \sum_ {\mathbf {y} \neq \mathbf {x}} \mathbf {q} _ {t} ^ {T} (\mathbf {y} | \mathbf {x}, \mathbf {x} _ {0})\right) + \lim _ {T \to \infty} T \log \left(1 - \sum_ {\mathbf {y} \neq \mathbf {x}} \mathbf {q} _ {t, \theta} ^ {T} (\mathbf {y} | \mathbf {x})\right) \\ & \qquad = \sum_ {\mathbf {y} \neq \mathbf {x}} \lim _ {T \to \infty} T \mathbf {q} _ {t} ^ {T} (\mathbf {y} | \mathbf {x}, \mathbf {x} _ {0}) - \sum_ {\mathbf {y} \neq \mathbf {x}} \lim _ {T \to \infty} T \mathbf {q} _ {t, \theta} ^ {T} (\mathbf {y} | \mathbf {x}), t = \lfloor T s \rfloor \end{array}
$$

where we used standard log asymptotics.

Inserting now Eq. 13 and Eq. 14, once again any terms in the sum so that $d _ { \mathrm { H A M } } ( \mathbf { x } , \mathbf { y } ) > 1$ vanish, and we arrive at

$$
\begin{array}{l} E _ {2} ^ {\infty} (\mathbf {x} _ {0}, \mathbf {x}, s) = - \frac {\alpha_ {1 - s} ^ {\prime}}{1 - \alpha_ {1 - s}} \sum_ {i = 1, x ^ {i} = m} ^ {L} \sum_ {y ^ {i} \in \mathcal {V}, y ^ {i} \neq \mathbf {m}} \mathrm{Cat} (y ^ {i}; \delta (x _ {0} ^ {i}) \\ \quad + \frac {\alpha_ {1 - s} ^ {\prime}}{1 - \alpha_ {1 - s}} \sum_ {i = 1, x ^ {i} = m} ^ {L} \sum_ {y ^ {i} \in \mathcal {V}, y ^ {i} \neq \mathbf {m}} \mathrm{Cat} (y ^ {i}; D _ {\theta} ^ {i} (\mathbf {x})) \mathbb {E} _ {\mathbf {z} \sim D _ {\theta} (\mathbf {x})} \left[ G _ {\phi} ^ {i} (\mathbf {z} ^ {- i, y ^ {i}}, \mathbf {x}) \right] \\ \quad + \frac {\alpha_ {1 - s} ^ {\prime}}{1 - \alpha_ {1 - s}} \sum_ {i = 1, x ^ {i} \neq m} ^ {L} \sum_ {y ^ {i} \in \mathcal {V}, y ^ {i} \neq x ^ {i}} \frac {\mathbb {E} _ {\mathbf {z} \sim D _ {\theta} (\mathbf {x})} \left[ G _ {\phi} ^ {i} (\mathbf {z} , \mathbf {x}) \right]}{1 - \mathrm{Cat} (x ^ {i} ; D _ {\theta} ^ {i} (\bar {\mathbf {x}})} \mathrm{Cat} (y ^ {i}; D _ {\theta} ^ {i} (\bar {\mathbf {x}})) \\ \quad = - \frac {\alpha_ {1 - s} ^ {\prime}}{1 - \alpha_ {1 - s}} \sum_ {i = 1, x ^ {i} = m} ^ {L} \left(1 - \mathbb {E} _ {\mathbf {z} \sim D _ {\theta} (\mathbf {x})} \left[ G _ {\phi} ^ {i} (\mathbf {z}, \mathbf {x}) \right]\right) \\ \quad - \frac {\alpha_ {1 - s} ^ {\prime}}{1 - \alpha_ {1 - s}} \sum_ {i = 1, x ^ {i} \neq m} ^ {L} - \mathbb {E} _ {\mathbf {z} \sim D _ {\theta} (\mathbf {x})} \left[ G _ {\phi} ^ {i} (\mathbf {z}, \mathbf {x}) \right], \end{array}\tag{19}
$$

where in the second step we recall $\mathbf { z } ^ { - i , y ^ { i } }$ is denoting replacing the i’th coordinate of z with $y ^ { i }$ , so the sum in the second term is just taking the expected value in the missing coordinate, and the law of total probability applied to $D _ { \theta } ^ { i } ( { \mathbf { x } } )$ cancels the denominator in the third term.

Recalling we are finding the limit as $T \to \infty$ of the right hand side of Eq. 10, using the limits Eq. 11, Eq. 18, Eq. 19 with the observation Eq. 15, we arrive at:

$$
\begin{array}{l} \lim _ {T \to \infty} \log (\mathbf {q} _ {\theta} ^ {T} (\mathbf {x} _ {0}) \geq \int_ {0} ^ {1} \mathbb {E} _ {\mathbf {x} _ {s} \sim \mathbf {p} _ {1 - s} (\cdot | \mathbf {x} _ {0})} \left[ E _ {1} ^ {\infty} (\mathbf {x} _ {0}, \mathbf {x} _ {s}, s) + E _ {2} ^ {\infty} (\mathbf {x} _ {0}, \mathbf {x} _ {s}, s) \right] d s \\ = - \int_ {0} ^ {1} \frac {\alpha_ {1 - s} ^ {\prime}}{1 - \alpha_ {1 - s}} \mathbb {E} _ {\mathbf {x} _ {s} \sim \mathbf {p} _ {1 - s} (\cdot | \mathbf {x} _ {0})} \bigg [ \sum_ {i = 1, x _ {s} ^ {i} = \mathbf {m}} ^ {L} \log \left(\mathrm{Cat} (x _ {0} ^ {i}; D _ {\theta} ^ {i} (\mathbf {x} _ {s}))\right) \\ \quad + \sum_ {i = 1, x _ {s} ^ {i} = \mathbf {m}} ^ {L} \log \left(\mathbb {E} _ {\mathbf {z} \sim D _ {\theta} (\mathbf {x} _ {s})} \left[ G _ {\phi} ^ {i} (\mathbf {z} ^ {- i, x _ {0} ^ {i}}, \mathbf {x} _ {s}) \right]\right) \\ \quad + \sum_ {i = 1, x _ {s} ^ {i} = \mathbf {m}} ^ {L} \left(1 - \mathbb {E} _ {\mathbf {z} \sim D _ {\theta} (\mathbf {x})} \left[ G _ {\phi} ^ {i} (\mathbf {z}, \mathbf {x} _ {s}) \right]\right) \\ \quad + \sum_ {i = 1, x _ {s} ^ {i} \neq m} ^ {L} - \mathbb {E} _ {\mathbf {z} \sim D _ {\theta} (\mathbf {x} _ {s})} \left[ G _ {\phi} ^ {i} (\mathbf {z}, \mathbf {x} _ {s}) \right] \bigg ] d s. \end{array}\tag{20}
$$

We handle the 4 terms in Eq. 20 separately. For the first, we observe that making the time change $t = 1 - s ,$ this is $\mathcal { E } _ { D } ( \mathbf { x } _ { 0 } )$ from Proposition 1.

For the second, we recall α is decreasing, so the time-dependent term in front is positive. Thus, by Jensen’s inequality:

$$
\begin{array}{l} - \int_ {0} ^ {1} \frac {\alpha_ {1 - s} ^ {\prime}}{1 - \alpha_ {1 - s}} \mathbb {E} _ {\mathbf {x} _ {s} \sim \mathbf {p} _ {1 - s} (\cdot | \mathbf {x} _ {0})} \left[ \sum_ {i = 1, x _ {s} ^ {i} = \mathbf {m}} ^ {L} \log \left(\mathbb {E} _ {\mathbf {z} \sim D _ {\theta} (\mathbf {x} _ {s})} \left[ G _ {\phi} ^ {i} (\mathbf {z} ^ {- i, x _ {0} ^ {i}}, \mathbf {x} _ {s}) \right]\right) \right] d s \\ \geq - \int_ {0} ^ {1} \frac {\alpha_ {1 - s} ^ {\prime}}{1 - \alpha_ {1 - s}} \mathbb {E} _ {\mathbf {x} _ {s} \sim \mathbf {p} _ {1 - s} (\cdot | \mathbf {x} _ {0})} \left[ \sum_ {i = 1, x _ {s} ^ {\prime} = \mathbf {m}} ^ {L} \mathbb {E} _ {\mathbf {z} \sim D _ {\theta} (\mathbf {x} _ {s})} \left[ \log \left(G _ {\phi} ^ {i} (\mathbf {z} ^ {- i, x _ {0} ^ {i}}, \mathbf {x} _ {s})\right) \right] \right] d s \\ = - \int_ {0} ^ {1} \frac {\alpha_ {1 - s} ^ {\prime}}{1 - \alpha_ {1 - s}} \mathbb {E} _ {\mathbf {x} _ {s} \sim \mathbf {p} _ {1 - s} (\cdot | \mathbf {x} _ {0})} \left[ \sum_ {i = 1, x _ {s} ^ {{i}} = \mathbf {m}} ^ {L} \mathbb {E} _ {\mathbf {z} \sim D _ {\theta} (\mathbf {x} _ {s})} \left[ \mathrm{Cat} (z ^ {{i}}; \delta (x _ {0} ^ {{i}})) \log \left(G _ {\phi} ^ {{i}} (\mathbf {z}, \mathbf {x} _ {s})\right) \right] \right] d s \\ \geq - \int_ {0} ^ {1} \frac {\alpha_ {1 - s} ^ {\prime}}{1 - \alpha_ {1 - s}} \mathbb {E} _ {\mathbf {x} _ {s} \sim \mathbf {p} _ {1 - s} (\cdot | \mathbf {x} _ {0})} \left[ \sum_ {i = {1, x _ {s} ^ {{i}} = \mathbf {m}}} ^ {L} \mathbb {E} _ {\mathbf {z} \sim D _ {\theta} (\mathbf {x} _ {s})} \left[ \mathrm{CE} \left(\mathrm{Cat} (z ^ {{i}}; \delta (x _ {0} ^ {{i}})), G _ {\phi} ^ {{i}} (\mathbf {z}, \mathbf {x} _ {s})\right) \right] \right] d s \\ = \mathcal {E} _ {{M P}} (\mathbf {x} _ {0}) \end{array}
$$

where $\mathcal { E } _ { M P } ( \mathbf { x } _ { 0 } )$ is as in Proposition 1. The second inequality comes from the fact that $a \log ( b ) \geq \mathrm { C E } ( a , b ) =$ $a \log ( b ) + ( 1 - a ) \log ( 1 - b )$ for $a , b \in [ 0 , 1 ]$ . To see this final equality, we again make the time change $t = 1 - s$ and recall that we define $G _ { M } ^ { i } ( { \bf z } , { \bf x } ) = G _ { \phi } ^ { i } ( { \bf z } , { \bf x } )$ when $x ^ { i } = \mathbf { m }$

For the third term, the second term is already training the planner in masked positions, so we simply use that $G _ { \phi } ^ { i } \in [ 0 , 1 ]$ to bound this below by 0.

Finally, for the last term, we use that $- a \geq \log ( 1 - a )$ for any $a \in [ 0 , 1 )$ , so:

$$
\begin{array}{r l} & {- \int_ {0} ^ {1} \frac {\alpha_ {1 - s} ^ {\prime}}{1 - \alpha_ {1 - s}} \mathbb {E} _ {\mathbf {x} _ {s} \sim \mathbf {p} _ {1 - s} (\cdot | \mathbf {x} _ {0})} \bigg [ \sum_ {i = 1, x _ {s} ^ {i} \neq \mathbf {m}} ^ {L} - \mathbb {E} _ {\mathbf {z} \sim D _ {\theta} (\mathbf {x} _ {s})} \left[ G _ {\phi} ^ {i} (\mathbf {z}, \mathbf {x} _ {s}) \right] \bigg ] d s} \\ & {\geq - \int_ {0} ^ {1} \frac {\alpha_ {1 - s} ^ {\prime}}{1 - \alpha_ {1 - s}} \mathbb {E} _ {\mathbf {x} _ {s} \sim \mathbf {p} _ {1 - s} (\cdot | \mathbf {x} _ {0})} \bigg [ \sum_ {i = 1, x _ {s} ^ {\prime} \neq \mathbf {m}} ^ {L} \log \left(\mathbb {E} _ {\mathbf {z} \sim D _ {\theta} (\mathbf {x} _ {s})} \left[ 1 - G _ {\phi} ^ {i} (\mathbf {z}, \mathbf {x} _ {s}) \right]\right) \bigg ] d s} \\ & {\geq - \int_ {0} ^ {1} \frac {\alpha_ {1 - s} ^ {\prime}}{1 - \alpha_ {1 - s}} \mathbb {E} _ {\mathbf {x} _ {s} \sim \mathbf {p} _ {1 - s} (\cdot | \mathbf {x} _ {0})} \bigg [ \sumop_ {i = 1, x _ {s} ^ {i} \neq \mathbf {m}} ^ {L} \mathbb {E} _ {\mathbf {z} \sim D _ {\theta} (\mathbf {x} _ {s})} \left[ \log \left(1 - G _ {\phi} ^ {i} (\mathbf {z}, \mathbf {x} _ {s})\right) \right] \bigg ] d s} \end{array}
$$

$$
\begin{array}{l} = - \int_ {0} ^ {1} \frac {\alpha_ {1 - s} ^ {\prime}}{1 - \alpha_ {1 - s}} \mathbb {E} _ {\mathbf {x} _ {s} \sim \mathbf {p} _ {1 - s} (\cdot | \mathbf {x} _ {0})} \bigg [ \sum_ {i = 1, x _ {s} ^ {i} \neq \mathbf {m}} ^ {L} \mathbb {E} _ {\mathbf {z} \sim D _ {\theta} (\mathbf {x} _ {s})} \left[ \mathrm{CE} \left(\mathrm{Cat} (z ^ {i}; \delta (x _ {0} ^ {i})), 1 - G _ {\phi} ^ {i} (\mathbf {z}, \mathbf {x} _ {s})\right) \right] \bigg ] d s \\ = \mathcal {E} _ {U P} (\mathbf {x} _ {0}), \end{array}
$$

where for the second inequality we applied Jensen $\therefore \mathrm { s } ,$ for the second-to-last equality we use $\mathrm { C a t } ( z ^ { i } ; \delta ( x _ { 0 } ^ { i } ) ) = 1$ for $z ^ { i } \sim D _ { \theta } ^ { i } ( x _ { s } )$ with $x _ { s } ^ { i } \neq \mathbf { m }$ by assumption, and for the last equality yet again we make the time change $t = 1 - s$ , and observe that we defined $G _ { U } ^ { i } ( { \bf z } , { \bf x } ) = 1 - G _ { \phi } ^ { i } ( { \bf z } , { \bf x } )$ when $x ^ { i } \neq \mathbf { m }$

The proof of the proposition is now complete.

## B.2 Finding the Optimal Planner Under the ELBO-informed Loss: Proposition 2

Here we derive the form of the optimal $G _ { U }$ and $G _ { M }$ using the training loss associated to the ELBO proved in Proposition 1 for a fixed MDM denoiser $D _ { \theta }$ . Recall, as discussed in Subsection 3.2 that we train via $\mathcal { L } ( \phi ) \doteq - \mathbb { E } _ { \mathbf { x } _ { 0 } \sim \mathbf { p } _ { 0 } } \left[ \mathcal { E } _ { \mathrm { M P } } ( \mathbf { x } _ { 0 } ) + \mathcal { E } _ { \mathrm { U P } } ( \mathbf { x } _ { 0 } ) \right]$ . In practice, we train a single network $T _ { \phi } ( \mathbf { z } , \mathbf { x } )$ to play the role of both $G _ { U }$ and $G _ { M }$ in E<sub>UP</sub> and ${ \mathcal { E } } _ { \mathrm { M } }$ respectively. Making ${ \mathcal { L } } ( \phi )$ with this insertion explicit for reference:

$$
\mathcal {L} (\phi) = \int_ {0} ^ {1} \frac {d \alpha_ {t}}{d t} \cdot \frac {1}{1 - \alpha_ {t}} \mathbb {E} _ {\mathbf {x} _ {0} \sim \mathbf {p} _ {0}} \left[ \mathbb {E} _ {\mathbf {x} _ {t} \sim \mathbf {p} _ {t} (\cdot ; \mathbf {x} _ {0})} \left[ \sum_ {i = 1} ^ {L} \mathbb {E} _ {\mathbf {z} \sim D _ {\theta} (\mathbf {x} _ {t})} \left[ \mathrm{CE} \left(\operatorname{Cat} (z ^ {i}; \delta (x _ {0} ^ {i})), T _ {\phi} ^ {i} (\mathbf {z}, \mathbf {x} _ {t})\right) \right] \right] \right] d t\tag{21}
$$

where $\mathbf { p } _ { t }$ is defined per Eq. 1 and $\mathrm { C E } ( a , b ) = a \log ( b ) + ( 1 - a ) \log ( 1 - b )$

We have the following proposition:

Proposition 2. Let $T _ { \phi } : \mathcal { V } ^ { L } \times \mathcal { V } ^ { L } \to [ 0 , 1 ]$ be trained via $\mathcal { L } ( \phi ) = - \mathbb { E } _ { { \bf x } _ { 0 } \sim { \bf p } _ { 0 } } \left[ \mathcal { E } _ { M P } ( { \bf x } _ { 0 } ) + \mathcal { E } _ { U P } ( { \bf x } _ { 0 } ) \right]$ ], taking $G _ { U } = G _ { M } = T _ { \phi }$ in $\mathcal { E } _ { M P }$ and $\mathcal { E } _ { U P }$ from Proposition 1. Define, $f o r \ { \mathbf { z } } , { \mathbf { x _ { t } } } \in \mathcal { V } ^ { \mathbf { L } }$ with z a sequence of unmasked tokens satisfying $\mathbf { z } ^ { i } = \mathbf { x } _ { t } ^ { i }$ for all i such that $\mathbf { x } _ { t } ^ { i } \neq $ m:

$$
\bar {T} ^ {i} (\mathbf {z}, \mathbf {x} _ {t}) = \left\{ \begin{array}{l l} \mathbf {p} _ {0} \left(x _ {0} ^ {i} = z ^ {i} | x _ {0} ^ {j} = x _ {t} ^ {j}, \forall j \neq i \text {such that} x _ {t} ^ {j} \neq \mathbf {m}\right), & x _ {t} ^ {i} \neq \mathbf {m} \\ \mathbf {p} _ {0} \left(x _ {0} ^ {i} = z ^ {i} | x _ {0} ^ {j} = x _ {t} ^ {j}, \forall j \text {such that} x _ {t} ^ {j} \neq \mathbf {m}\right), & x _ {t} ^ {i} = \mathbf {m} \end{array} \right..
$$

Then, for any $D _ { \theta } , { \mathcal { L } } ( \phi )$ is uniquely minimized over $T _ { \phi } ^ { i }$ when $T _ { \phi } ^ { i } ( \mathbf { z } , \mathbf { x } _ { t } ) = \bar { T } ^ { i } ( \mathbf { z } , \mathbf { x } _ { t } )$

Note that in practice z which is inserted into $G _ { M }$ and $G _ { U }$ is always sampled from $D _ { \theta } ^ { i } ( \mathbf { x } _ { t } )$ , which is taken to be $\delta ( x _ { t } ^ { i } )$ in positions where $x _ { t } ^ { i } \neq \mathbf { m }$ . Thus the proposition considers exactly the form of sequences that $T _ { \phi }$ will see during sampling. Also observe that this minimizer is doing exactly what we would desire from $\hat { T } ^ { i }$ in both its roles as $G _ { U } ^ { i }$ and $G _ { M } ^ { i }$ :

• For $\bar { T } ^ { i } ( { \bf z } , { \bf x } _ { t } )$ as $G _ { U } ^ { i } ( { \bf z } , { \bf x } _ { t } )$ , we keep a previously unmasked position $z ^ { i } = x _ { t } ^ { i }$ with probability proportional to the probability that, conditionally upon the information about the currently unmasked positions of $x _ { t }$ other than $i , z ^ { i } = x _ { t } ^ { i }$ is found in the i’th position of a sequence under the data distribution $\mathbf { p } _ { 0 } .$

• Similarly, for $\bar { T } ^ { i } ( { \bf z } , { \bf x } _ { t } )$ as $G _ { M } ^ { i } ( { \bf z } , { \bf x } _ { t } )$ , we unmask a token in position i to $z ^ { i }$ suggested by the denoiser with probability proportional to the conditional probability that $z ^ { i }$ is found in the i’th position of a sequence under the data distribution $\mathbf { p } _ { 0 }$

Thus, for any denoiser, the optimal $T _ { \phi } ^ { i }$ is aiming to steer towards planned paths which are representative of the data distribution in both its roles as $G _ { U } ^ { i }$ and $G _ { M } ^ { i }$ . We emphasize once again that even if one wishes to train only for the role of $G _ { U }$ or $G _ { M }$ respectively, to gain a meaningful training signal for both correctly and incorrectly denoised $\mathbf { z } ,$ one should use $G _ { U } = G _ { M } = T _ { \phi }$ in Algorithm 2.

We now proceed with the proof of Proposition 2.

Proof. We begin by defining

$$
\mathbf {r} _ {t} (\mathbf {x} _ {0}; \mathbf {x} _ {t}) := \frac {\mathbf {p} _ {0} (\mathbf {x} _ {0}) \mathbf {p} _ {t} (\mathbf {x} _ {t} ; \mathbf {x} _ {0})}{\mathbf {p} _ {t} (\mathbf {x} _ {t} ; \mathbf {x} _ {0} \sim \mathbf {p} _ {0})},
$$

where by ${ \bf p } _ { t } ( { \bf x } _ { t } ; { \bf x } _ { 0 } \sim { \bf p } _ { 0 } )$ we mean, as usual, $\begin{array} { r } { \mathbf { p } _ { t } ( \mathbf { x } _ { t } ; \mathbf { x } _ { 0 } \sim \mathbf { p } _ { 0 } ) = \sum _ { \mathbf { x } _ { 0 } \in \mathcal { V } ^ { L } } \mathbf { p } _ { t } ( \mathbf { x } _ { t } ; \mathbf { x } _ { 0 } ) \mathbf { p } _ { 0 } ( \mathbf { x } _ { 0 } ) } \end{array}$ , and where $\mathbf { p } _ { t } ( \mathbf { x } _ { t } ; \mathbf { x } _ { 0 } )$ is as in Eq. 1. We then observe:

$$
\mathcal {L} (\phi) = \int_ {0} ^ {1} \beta_ {t} \mathbb {E} _ {\mathbf {x} _ {t} \sim \mathbf {p} _ {t} (\cdot ; \mathbf {x} _ {0} \sim \mathbf {p} _ {0})} \left[ \mathbb {E} _ {\mathbf {z} \sim D _ {\theta} (\mathbf {x} _ {t})} \left[ \mathbb {E} _ {\mathbf {x} _ {0} \sim \mathbf {r} _ {t} (\cdot ; \mathbf {x} _ {t})} \left[ \sum_ {i = 1} ^ {L} \mathrm{CE} \left(\mathrm{Cat} (z ^ {i}; \delta (x _ {0} ^ {i})), T _ {\phi} ^ {i} (\mathbf {z}, \mathbf {x} _ {t})\right) \right] \right] \right] d t,
$$

where $\begin{array} { r } { \beta _ { t } = \frac { d \alpha _ { t } } { d t } \cdot \frac { 1 } { 1 - \alpha _ { t } } } \end{array}$ . Next, we observe that there is no relationship enforced between $T _ { \phi } ^ { i } ( { \bf z } , { \bf x } _ { t } )$ and $T _ { \phi } ^ { i } ( \bar { \bf z } , \bar { \bf x } _ { t } )$ for $( { \bf z } , { \bf x } _ { t } ) \neq ( \bar { \bf z } , \bar { \bf x } _ { t } ) \in \mathcal { V } ^ { L }$ . So, as $\beta _ { t }$ is negative, minimizing ${ \mathcal { L } } _ { \mathrm { U P } } ( \phi )$ amounts to maximizing

$$
L (\mathbf {z}, \mathbf {x} _ {t}) = \mathbb {E} _ {\mathbf {x} _ {0} \sim \mathbf {r} _ {t} (\cdot ; \mathbf {x} _ {t})} \left[ \sum_ {i = 1} ^ {L} \mathrm{CE} \left(\mathrm{Cat} (z ^ {i}; \delta (x _ {0} ^ {i})), T _ {\phi} ^ {i} (\mathbf {z}, \mathbf {x} _ {t})\right) \right]
$$

for each z and $\mathbf { x } _ { t }$ . Using that each i’th term in the sum only depends on $\mathbf { x } _ { \mathrm { 0 } }$ through $\mathbf { x } _ { 0 } ^ { i }$ , we have:

$$
L (\mathbf {z}, \mathbf {x} _ {t}) = \sum_ {i = 1} ^ {L} \mathrm{CE} \left(r _ {t} ^ {i} (z ^ {i}; \mathbf {x} _ {t}), G _ {U} ^ {i} (\mathbf {z}, \mathbf {x} _ {t})\right),
$$

where

$$
r _ {t} ^ {i} (z ^ {i}; \mathbf {x} _ {t}) = \sum_ {\mathbf {x} _ {0} \in \mathcal {V} ^ {L}} \mathbf {r} _ {t} (\mathbf {x} _ {0} ^ {- i, z ^ {i}}; \mathbf {x} _ {t}),
$$

where $\mathbf { x } _ { 0 } ^ { - i , z ^ { i } }$ denotes that we remove the i’th coordinate of $\mathbf { x } _ { \mathrm { 0 } }$ and replace it with $z ^ { i } .$ . It now follows from the fact that for fixed $a , \operatorname { C E } ( a , b ) = a \log ( b ) + ( 1 - a ) \log ( 1 - b )$ is uniquely maximized at $b = a$ that the optimal $G _ { U } ^ { i } ( \mathbf { z } , \mathbf { x } _ { t } ) { \mathrm { ~ i s ~ } } r _ { t } ^ { i } ( z ^ { i } ; \mathbf { x } _ { t } )$ . It remains to show, that thanks to the simple form of $\mathbf { p } _ { t }$ from $\operatorname { E q . 1 }$ , indeed $r _ { t } ^ { i } ( z ^ { i } ; { \bf x } _ { t } )$ does not depend on time and is equal to $\bar { T } ^ { i } ( { \bf z } , { \bf x } _ { t } )$ .

First, we note that, as p<sub>0</sub> does not contain any sequences with the token m in its support by definition:

$$
\begin{array}{r l} & {\mathbf {p} _ {t} (\mathbf {x} _ {t}; \mathbf {x} _ {0} \sim \mathbf {p} _ {0}) = \sum_ {\mathbf {x} _ {0} \in \mathcal {V} ^ {L}} \mathbf {p} _ {0} (\mathbf {x} _ {0}) \prod_ {i = 1} ^ {L} \mathrm{Cat} (x _ {t} ^ {i}; \alpha_ {t} \delta (x _ {0} ^ {i}) + (1 - \alpha_ {t}) \delta (\mathbf {m}))} \\ & {\qquad = \alpha_ {t} ^ {L - N _ {M} (\mathbf {x} _ {t})} (1 - \alpha_ {t}) ^ {N _ {M} (\mathbf {x} _ {t})} \mathbf {p} _ {0} (x _ {0} ^ {j} = x _ {t} ^ {j}, \forall j \text {such that} x _ {t} ^ {j} \neq \mathbf {m}),} \end{array}\tag{22}
$$

where $N _ { M } ( { \bf x } _ { t } )$ is the number of positions of $\mathbf { x } _ { t }$ which are equal to m. Indeed, this computation is the result of Ou et al. (2024) Proposition 1.

Then we observe that, similarly, for fixed i:

$$
\begin{array}{l} \sum_ {\mathbf {x} _ {0} \in \mathcal {V} ^ {L}} \mathbf {p} _ {0} (\mathbf {x} _ {0} ^ {- i, z ^ {i}}) \mathbf {p} _ {t} (\mathbf {x} _ {t}; \mathbf {x} _ {0} ^ {- i, z ^ {i}}) \\ = \operatorname{Cat} (x _ {t} ^ {i}; \alpha_ {t} \delta (z ^ {i}) + (1 - \alpha_ {t}) \delta (\mathbf {m})) \sum_ {\mathbf {x} _ {0} \in \mathcal {V} ^ {L}} \mathbf {p} _ {0} (\mathbf {x} _ {0} ^ {- i, z ^ {i}}) \prod_ {j = 1, j \neq i} ^ {L} \operatorname{Cat} (x _ {t} ^ {j}; \alpha_ {t} \delta (x _ {0} ^ {j}) + (1 - \alpha_ {t}) \delta (\mathbf {m})) \\ = \operatorname{Cat} (x _ {t} ^ {i}; \alpha_ {t} \delta (z ^ {i}) + (1 - \alpha_ {t}) \delta (\mathbf {m})) \alpha_ {t} ^ {L - 1 - N _ {M} (\mathbf {x} _ {t} ^ {- i})} (1 - \alpha_ {t}) ^ {N _ {M} (\mathbf {x} _ {t} ^ {- i})} \\ \quad \times \mathbf {p} _ {0} (x _ {0} ^ {i} = z ^ {i} \text {and} x _ {0} ^ {j} = x _ {t} ^ {j}, \forall j \text {such that} x _ {t} ^ {j} \neq \mathbf {m}), \end{array}
$$

where $\mathbf { x } _ { t } ^ { - i } \in \mathcal { V } ^ { L - 1 }$ is obtained from $\mathbf { x } _ { t }$ by removing its i’th coordinate. $r _ { t } ^ { i } \big ( z ^ { i } ; { \mathbf { x } } _ { t } \big )$ is precisely this term divided by ${ \bf p } _ { t } ( { \bf x } _ { t } ; { \bf x } _ { 0 } \sim { \bf p } _ { 0 } )$

There are two cases to consider. The first is when $x _ { t } ^ { i } = { \mathbf { m } }$ . Then ${ \cal N } _ { M } ( { \bf x } _ { t } ^ { - i } ) = { \cal N } _ { M } ( { \bf x } _ { t } ) - 1 \mathrm { a n d } { \mathrm { C a t } } ( x _ { t } ^ { i } ; \alpha _ { t } \delta ( z ^ { i } ) +$ $( 1 - \alpha _ { t } ) \delta ( \mathbf { m } ) ) = 1 - \alpha _ { t } ,$ , so

$$
\begin{array}{l} \sum_ {\mathbf {x} _ {0} \in \mathcal {V} ^ {L}} \mathbf {p} _ {0} (\mathbf {x} _ {0} ^ {- i, z ^ {i}}) \mathbf {p} _ {t} (\mathbf {x} _ {t}; \mathbf {x} _ {0} ^ {- i, z ^ {i}}) \\ = \alpha_ {t} ^ {L - N _ {M} (\mathbf {x} _ {t})} (1 - \alpha_ {t}) ^ {N _ {M} (\mathbf {x} _ {t})} \mathbf {p} _ {0} (x _ {0} ^ {i} = z ^ {i} \text {and} x _ {0} ^ {j} = x _ {t} ^ {j}, \forall j \text {such that} x _ {t} ^ {j} \neq \mathbf {m}), \end{array}
$$

and dividing by Eq. 22, the time-dependent terms cancel, yielding the desired result. The second is when $x _ { t } ^ { i } \neq \mathbf { m }$ . Then $N _ { M } ( \mathbf { x } _ { t } ^ { - i } ) = N _ { M } ( \mathbf { x } _ { t } )$ ) and $\mathrm { C a t } ( x _ { t } ^ { i } ; \alpha _ { t } \delta ( z ^ { i } ) + ( 1 - \alpha _ { t } ) \delta ( \mathbf { m } ) ) = \alpha _ { t } \mathrm { C a t } ( z ^ { i } ; \delta ( x _ { t } ^ { i } ) )$ , so

$$
\begin{array}{l} \sum_ {\mathbf {x} _ {0} \in \mathcal {V} ^ {L}} \mathbf {p} _ {0} (\mathbf {x} _ {0} ^ {- i, z ^ {i}}) \mathbf {p} _ {t} (\mathbf {x} _ {t}; \mathbf {x} _ {0} ^ {- i, z ^ {i}}) \\ = \alpha_ {t} ^ {L - N _ {M} (\mathbf {x} _ {t})} (1 - \alpha_ {t}) ^ {N _ {M} (\mathbf {x} _ {t})} \mathrm{Cat} (z ^ {i}; \delta (x _ {t} ^ {i})) \mathbf {p} _ {0} (x _ {0} ^ {i} = z ^ {i} \text {and} x _ {0} ^ {j} = x _ {t} ^ {j}, \forall j \text {such that} x _ {t} ^ {j} \neq \mathbf {m}). \end{array}
$$

Using that $\mathrm { C a t } ( z ^ { i } ; \delta ( x _ { t } ^ { i } ) ) = 1$ by assumption and again dividing by $\mathrm { E q . 2 2 }$ , the time-dependent terms cancel, yielding the desired result. □

## B.3 Form of the ELBO for Varying η

Here we show how to find the form of the ELBO from Proposition 1 for arbitrary stochasticity $\eta \geq 0$ in the definition of ${ \tilde { G } } _ { \eta }$ from Eq. 7.

We observe that taking $\eta \neq 1$ corresponds to modifying $G _ { M }$ and $G _ { U }$ to $G _ { \eta , M }$ and $G _ { \eta , U }$ respectively, where:

$$
\begin{array}{l} {G _ {\eta , M} ^ {j} (\mathbf {z}, \mathbf {x}) = \frac {\eta G _ {M} ^ {j} (\mathbf {z} , \mathbf {x})}{C _ {\eta} (\mathbf {z} , \mathbf {x})}} \\ {G _ {\eta , U} ^ {j} (\mathbf {z}, \mathbf {x}) = \frac {G _ {U} ^ {j} (\mathbf {z} , \mathbf {x})}{C _ {\eta} (\mathbf {z} , \mathbf {x})}} \\ {C _ {\eta} (\mathbf {z}, \mathbf {x}) = \sum_ {i = 1, \mathbf {x} ^ {i} \neq \mathbf {m}} ^ {L} G _ {U} ^ {j} (\mathbf {z}, \mathbf {x}) + \eta \sum_ {i = 1, \mathbf {x} ^ {i} = \mathbf {m}} ^ {L} G _ {M} ^ {j} (\mathbf {z}, \mathbf {x})} \end{array}
$$

(see Alg. 5 for reference). Inserting this choice into E from Proposition 1 yields $\mathcal { E } _ { \eta } ( \mathbf { x } _ { 0 } ) \leq \log ( P _ { 0 } ^ { \theta , \phi , \eta } ( \mathbf { x } _ { 0 } ) )$ ) for each fixed $\mathbf { x } _ { 0 } \in \mathcal { V } ^ { L }$ given by $\mathcal { E } _ { \eta } ( \mathbf { x } _ { 0 } ) = \mathcal { E } _ { \eta , \mathrm { M P } } ( \mathbf { x } _ { 0 } ) + \mathcal { E } _ { \eta , \mathrm { U P } } ( \mathbf { x } _ { 0 } ) + \mathcal { E } _ { \mathrm { D } } ( \mathbf { x } _ { 0 } )$ , where:

$$
\begin{array}{l} \mathcal {E} _ {\eta , \mathrm{MP}} (\mathbf {x} _ {0}) = - \int_ {0} ^ {1} \beta_ {t} \mathbb {E} _ {\mathbf {x} _ {t} \sim \mathbf {p} _ {t} (\cdot ; \mathbf {x} _ {0})} \left[ \sum_ {i = 1, \mathbf {x} _ {t} ^ {i} = \mathbf {m}} ^ {L} \mathbb {E} _ {\mathbf {z} \sim D _ {\theta} (\mathbf {x} _ {t})} \left[ \mathrm{CE} \left(\mathrm{Cat} (z ^ {i}; \delta (x _ {0} ^ {i})), \eta G _ {M} ^ {i} (\mathbf {z}, \mathbf {x} _ {t}) / C _ {\eta} (\mathbf {z}, \mathbf {x} _ {t})\right) \right] \right] d t \\ \mathcal {E} _ {\eta , \mathrm{UP}} (\mathbf {x} _ {0}) = - \int_ {0} ^ {1} \beta_ {t} \mathbb {E} _ {\mathbf {x} _ {t} \sim \mathbf {p} _ {t} (\cdot ; \mathbf {x} _ {0})} \left[ \sum_ {i = 1, \mathbf {x} _ {t} ^ {i} \neq \mathbf {m}} ^ {L} \mathbb {E} _ {\mathbf {z} \sim D _ {\theta} (\mathbf {x} _ {t})} \left[ \mathrm{CE} \left(\mathrm{Cat} (z ^ {i}; \delta (x _ {0} ^ {i})), G _ {U} ^ {i} (\mathbf {z}, \mathbf {x} _ {t}) / C _ {\eta} (\mathbf {z}, \mathbf {x} _ {t})\right) \right] \right] d t \\ \mathcal {E} _ {\mathrm{D}} (\mathbf {x} _ {0}) = - \int_ {0} ^ {1} \beta_ {t} \mathbb {E} _ {\mathbf {x} _ {t} \sim \mathbf {p} _ {t} (\cdot ; \mathbf {x} _ {0})} \left[ \sum_ {i = 1, \mathbf {x} _ {t} ^ {i} = {\mathbf m}} ^ {L} \delta (\mathbf {x} _ {0} ^ {i}) ^ {\top} \log (D _ {\theta} ^ {i} (\mathbf {x} _ {t})) \right] d t, \end{array}
$$

where, as before, p is defined per Eq. $\begin{array} { r } { 1 , \beta _ { t } = \frac { d \alpha _ { t } } { d t } \cdot \frac { 1 } { 1 - \alpha _ { t } } } \end{array}$ , and $\mathrm { C E } ( a , b ) = a \log ( b ) + ( 1 - a ) \log ( 1 - b )$ for $a , b \in$ $[ 0 , 1 ]$ , with 0 log $0 = 0$ . Note that the efect of increasing η will be to place more weight on the role of the masked planner, since $\begin{array} { r } { \frac { \partial } { \partial \eta } G _ { \eta , M } ^ { j } ( \mathbf { z } , \mathbf { x } ) = \frac { G _ { M } ^ { j } ( \mathbf { z } , \mathbf { x } ) \displaystyle \sum _ { i = 1 , x ^ { i } \neq \mathbf { m } } G _ { U } ^ { i } ( \mathbf { z } , \mathbf { x } ) } { C _ { \eta } ^ { 2 } ( \mathbf { z } , \mathbf { x } ) } \geq 0 } \end{array}$ , and hence $\mathrm { C E } ( 1 , G _ { \eta , M } ^ { j } ( \mathbf { z } , \mathbf { x } ) )$ is increasing in η and $\mathrm { C E } ( 0 , G _ { \eta , M } ^ { j } ( \mathbf { z } , \mathbf { x } ) )$ is decreasing in η. Conversely, $\begin{array} { r } { \frac { \partial } { \partial \eta } G _ { \eta , U } ^ { j } ( \mathbf { z } , \mathbf { x } ) = - \frac { G _ { U } ^ { j } ( \mathbf { z } , \mathbf { x } ) \sum _ { i = 1 , { x ^ { i } } = \mathbf { m } } G _ { M } ^ { i } ( \mathbf { z } , \mathbf { x } ) } { C _ { n } ^ { 2 } ( \mathbf { z } , \mathbf { x } ) } \leq 0 . } \end{array}$ , so $\mathrm { C E } ( 1 , G _ { n , U } ^ { j } ( \mathbf { z } , \mathbf { x } ) )$ is decreasing in η and $\mathrm { C E } ( 0 , G _ { n , U } ^ { j } ( \mathbf { z } , \mathbf { x } ) )$ is increasing in $\eta .$ Recalling the loss for the planner is given by $\begin{array} { r } { \mathcal { L } _ { \eta } ( \phi ) = - \mathbb { E } _ { \mathbf { x } _ { 0 } \sim \mathbf { p } _ { 0 } } \left[ \mathcal { E } _ { \eta , \mathrm { U P } } ( \mathbf { x } _ { 0 } ) + \mathcal { E } _ { \eta , \mathrm { M P } } ( \mathbf { x } _ { 0 } ) \right] } \end{array}$ and that $\beta _ { t } \le 0$ , indeed we see that increasing η puts more weight on $G _ { M } ^ { i }$ and less on $G _ { U } ^ { i }$ matching the label $\mathrm { C a t } ( z ^ { i } ; \delta ( x _ { 0 } ^ { i } ) )$ .

## B.4 Proof of Lemma 1

We consider each limit one at a time.

For Eq. 11, we have:

$$
\hat {\mathbf {q}} _ {\lfloor s T \rfloor} ^ {T} (\mathbf {x} | \mathbf {x} _ {0}) = \prod_ {i = 1} ^ {L} \hat {q} _ {\lfloor s T \rfloor} ^ {T} (x ^ {i} | x _ {0} ^ {i})
$$

where $\hat { q } _ { | s T | } ^ { T } ( \cdot | x _ { 0 } ^ { i } )$ is the distribution after $\lfloor s T \rfloor$ jumps of a single independent coordinate evolving according to $\operatorname { E q . 2 }$ and

$$
\begin{array}{l} \hat {q} _ {\lfloor s T \rfloor} ^ {T} (x ^ {i} | x _ {0} ^ {i}) = 0, x ^ {i} \not \in \{x _ {0} ^ {i}, \mathbf {m} \}, \\ \hat {q} _ {\lfloor s T \rfloor} ^ {T} (\mathbf {m} | x _ {0} ^ {i}) = \prod_ {t = T - 1} ^ {T - 1 - \lfloor s T \rfloor} \frac {1 - \alpha_ {(t - 1) / T}}{1 - \alpha_ {t / T}} = \frac {1 - \alpha_ {1 - 1 / T - \lfloor s T \rfloor / T}}{1 - \alpha_ {1 - 1 / T}} \to 1 - \alpha_ {1 - s} \text {as} T \to \infty . \end{array}
$$

Similarly for Eq. 12, $\begin{array} { r } { \hat { q } _ { 1 } ^ { T } ( x _ { 0 } ^ { i } | \mathbf { x } _ { 0 } ) = 1 - \hat { q } _ { 1 } ^ { T } ( \mathbf { m } | x _ { 0 } ^ { i } ) = 1 - \frac { 1 - \alpha _ { 1 / T } } { 1 - \alpha _ { 1 - 1 / T } } \to 1 \ \mathrm { a s } \ T \to \infty . } \end{array}$

For Eq. 13, observe from Eq. 2 that, for $y ^ { i } \neq x ^ { i } , t = \lfloor T s \rfloor ;$

$$
\begin{array}{c} \lim _ {T \to \infty} q _ {t} (y ^ {i} | x ^ {i}, x _ {0} ^ {i}) = 0 \\ \lim _ {T \to \infty} T q _ {t} (y ^ {i} | x ^ {i}, x _ {0} ^ {i}) = - \frac {\alpha_ {1 - s} ^ {\prime}}{1 - \alpha_ {1 - s}} \mathrm{Cat} \bigg (y ^ {i}; \delta (x _ {0} ^ {i}) \bigg) \mathrm{Cat} \bigg (x ^ {i}; \delta (\mathbf {m}) \bigg), \end{array}
$$

where the second limit follows from the definition of the derivative. Thus we have, recalling the definition of $\mathbf { q } _ { t } ^ { T }$ from Eq. 9, if y and x difer in two or more coordinates, the entire product vanishes, and if they difer in exactly 1, the limit is given by the above. This yields precisely Eq. 13.

Finally, for Eq. 14, observe from Eq. 5 that for $\mathbf { x } , \mathbf { z } \in \mathcal { V } ^ { L }$ and $y ^ { i } \neq x ^ { i } \in \mathcal { V } , t = \lfloor T s \rfloor$

$$
\begin{array}{r l} & {\underset {T \to \infty} {\lim} q _ {t, \theta} (y ^ {i} | \mathbf {x}, \mathbf {z}) = 0} \\ & {\underset {T \to \infty} {\lim} T q _ {t, \theta} (y ^ {i} | \mathbf {x}, \mathbf {z}) = - \frac {\alpha_ {1 - s} ^ {\prime}}{1 - \alpha_ {1 - s}} G _ {\phi} ^ {i} (\mathbf {z}, \mathbf {x}) \mathrm{Cat} (y ^ {i}; \delta (z ^ {i})), x ^ {i} = \mathbf {m}} \\ & {\underset {T \to \infty} {\lim} T q _ {t, \theta} (y ^ {i} | \mathbf {x}, \mathbf {z}) = - \frac {\alpha_ {1 - s} ^ {\prime}}{1 - \alpha_ {1 - s}} \frac {G _ {\phi} ^ {i} (\mathbf {z} , \mathbf {x})}{1 - \mathrm{Cat} (x ^ {i} ; D _ {\theta} ^ {i} (\bar {\mathbf {x}})} \mathrm{Cat} (y ^ {i}; D _ {\theta} ^ {i} (\bar {\mathbf {x}})), x ^ {i} \neq \mathbf {m},} \end{array}
$$

where here, as before, x¯ is shorthand for removing the i’th coordinate of x and replacing with m.

Then, recalling the definition of $\mathbf { q } _ { t , \theta } ^ { T }$ from Eq. 8, we pass the limit inside the expected value to obtain, for $\mathbf { y } \neq \mathbf { x } \in \mathcal { V } ^ { L } , t = \lfloor s T \rfloor$ :

$$
\begin{array}{l} \lim _ {T \to \infty} T \mathbf {q} _ {t, \theta} ^ {T} (\mathbf {y} | \mathbf {x}) \\ = - \frac {\alpha_ {1 - s} ^ {\prime}}{1 - \alpha_ {1 - s}} \left\{ \begin{array}{l l} \mathbb {E} _ {\mathbf {z} \sim D _ {\theta} (\mathbf {x})} \left[ G _ {\phi} ^ {i} (\mathbf {z}, \mathbf {x}) \mathrm{Cat} (y ^ {i}; \delta (z ^ {i})) \right] & , d _ {\mathrm{HAM}} (\mathbf {x}, \mathbf {y}) = 1, y ^ {i} \neq y ^ {i}, x ^ {i} = \mathbf {m} \\ \frac {\mathbb {E} _ {\mathbf {z} \sim D _ {\theta} (\mathbf {x})} \left[ G _ {\phi} ^ {i} (\mathbf {z} , \mathbf {x}) \right]}{1 - \mathrm{Cat} (x ^ {i} ; D _ {\theta} ^ {i} (\bar {\mathbf {x}})} \mathrm{Cat} (y ^ {i}; D _ {\theta} ^ {i} (\bar {\mathbf {x}})) & , d _ {\mathrm{HAM}} (\mathbf {x}, \mathbf {y}) = 1, y ^ {i} \neq y ^ {i}, x ^ {i} \neq \mathbf {m}. \\ 0, & \text {otherwise} \end{array} \right. \end{array}
$$

For the first term above, we recall that $\mathbf { z } \sim D _ { \theta } ( \mathbf { x } )$ means each coordinate $z ^ { i }$ is sampled independently from $D _ { \theta } ^ { i } ( { \mathbf { x } } )$ . Thus:

$$
\begin{array}{r l} & {\mathbb {E} _ {\mathbf {z} \sim D _ {\theta} (\mathbf {x})} \left[ G _ {\phi} ^ {i} (\mathbf {z}, \mathbf {x}) \mathrm{Cat} (y ^ {i}; \delta (z ^ {i})) \right] = \sum_ {\mathbf {z} \in \mathcal {V} ^ {L}, z ^ {i} = y ^ {i}} \prod_ {j = 1} ^ {L} \mathrm{Cat} (z ^ {j}; D _ {\theta} ^ {j} (\mathbf {x})) G _ {\phi} ^ {i} (\mathbf {z}, \mathbf {x})} \\ & {\qquad = \mathrm{Cat} (y ^ {i}; D _ {\theta} ^ {i} (\mathbf {x})) \mathbb {E} _ {\mathbf {z} \sim D _ {\theta} (\mathbf {x})} \left[ G _ {\phi} ^ {i} (\mathbf {z} ^ {- i, y ^ {i}}, \mathbf {x}) \right],} \end{array}
$$

where $\mathbf { z } ^ { - i , y ^ { i } }$ denotes replacing the i’th coordinate of z with $y ^ { i }$ . This yields precisely Eq. 14.

## B.5 Deriving the Discrete Time ELBO Eq. 10

This computation is standard, but we include it here for the sake of completeness. We begin by observing:

$$
\mathbf {q} _ {\theta} ^ {T} (\mathbf {x} _ {0}) = \sum_ {\mathbf {x} _ {T - 1}, \ldots , \mathbf {x} _ {1} \in \mathcal {V} ^ {L}} \prod_ {t = T} ^ {1} \mathbf {q} _ {t, \theta} ^ {T} (\mathbf {x} _ {t - 1} | \mathbf {x} _ {t}),
$$

where $\mathbf { q } _ { t , \theta } ^ { T } ( \mathbf { x } _ { t - 1 } | \mathbf { x } _ { t } )$ are as in Eq. 8, and we recall here that we fix $\mathbf { x } _ { T } = ( \mathbf { m } , \ldots , \mathbf { m } )$ . So, letting $\bar { q } ^ { T }$ be the distribution of the reference path up to time 1:

$$
\bar {\mathbf {q}} ^ {T} (\mathbf {x} _ {1}, \mathbf {x} _ {2}, \dots , \mathbf {x} _ {T - 1} | \mathbf {x} _ {0}) = \prod_ {t = T} ^ {2} \mathbf {q} _ {t} ^ {T} (\mathbf {x} _ {t - 1} | \mathbf {x} _ {t}, \mathbf {x} _ {0}),
$$

where $\mathbf { q } _ { t } ^ { T }$ are as in Eq. 9 we have:

$$
\mathbf {q} _ {\theta} ^ {T} (\mathbf {x} _ {0}) = \sum_ {\mathbf {x} _ {T - 1}, \ldots , \mathbf {x} _ {1} \in \mathcal {V} ^ {L}} \bar {\mathbf {q}} _ {1} ^ {T} (\mathbf {x} _ {1}, \ldots , \mathbf {x} _ {T - 1} | \mathbf {x} _ {0}) \frac {\prod_ {t = T} ^ {1} \mathbf {q} _ {t , \theta} ^ {T} (\mathbf {x} _ {t - 1} | \mathbf {x} _ {t})}{\bar {\mathbf {q}} _ {1} ^ {T} (\mathbf {x} _ {1} , \ldots , \mathbf {x} _ {T - 1} | \mathbf {x} _ {0})}.
$$

Then, by Jensen’s inequalty:

$$
\log (\mathbf {q} _ {\theta} ^ {T} (\mathbf {x} _ {0}) \geq \sum_ {\mathbf {x} _ {T - 1}, \ldots , \mathbf {x} _ {1} \in \mathcal {V} ^ {L}} \bar {\mathbf {q}} _ {1} ^ {T} (\mathbf {x} _ {1}, \ldots , \mathbf {x} _ {T - 1} | \mathbf {x} _ {0}) \sum_ {t = T} ^ {1} \log \left(\frac {\mathbf {q} _ {t , \theta} ^ {T} (\mathbf {x} _ {t - 1} | \mathbf {x} _ {t})}{\bar {\mathbf {q}} _ {1} ^ {T} (\mathbf {x} _ {1} , \ldots , \mathbf {x} _ {T - 1} | \mathbf {x} _ {0})}\right),
$$

and inserting the definition of $\bar { q } _ { 1 } ^ { T }$ inside the log:

$$
\begin{array}{l} \log (\mathbf {q} _ {\theta} ^ {T} (\mathbf {x} _ {0}) \\ \geq \sum_ {\mathbf {x} _ {T - 1}, \ldots , \mathbf {x} _ {1} \in \mathcal {V} ^ {L}} \bar {\mathbf {q}} _ {1} ^ {T} (\mathbf {x} _ {1}, \ldots , \mathbf {x} _ {T - 1} | \mathbf {x} _ {0}) \left[ \sum_ {t = T} ^ {2} \log \left(\frac {\mathbf {q} _ {t , \theta} ^ {T} (\mathbf {x} _ {t - 1} | \mathbf {x} _ {t})}{\mathbf {q} _ {t} ^ {T} (\mathbf {x} _ {t - 1} | \mathbf {x} _ {t} , \mathbf {x} _ {0})}\right) + \log (q _ {1, \theta} ^ {T} (\mathbf {x} _ {0} | \mathbf {x} _ {1})) \right] \\ = \sum_ {t = T} ^ {2} \sum_ {\mathbf {x} _ {T - 1}, \ldots , \mathbf {x} _ {1} \in \mathcal {V} ^ {L}} \bar {\mathbf {q}} _ {1} ^ {T} (\mathbf {x} _ {1}, \ldots , \mathbf {x} _ {T - 1} | \mathbf {x} _ {0}) \log \left(\frac {\mathbf {q} _ {t , \theta} ^ {T} (\mathbf {x} _ {t - 1} | \mathbf {x} _ {t})}{\mathbf {q} _ {t} ^ {T} (\mathbf {x} _ {t - 1} | \mathbf {x} _ {t} , \mathbf {x} _ {0})}\right). \\ + \sum_ {\mathbf {x} _ {T - 1}, \ldots , \mathbf {x} _ {1} \in \mathcal {V} ^ {L}} \bar {\mathbf {q}} _ {1} ^ {T} (\mathbf {x} _ {1}, \ldots , \mathbf {x} _ {T - 1} | \mathbf {x} _ {0}) \log (\mathbf {q} _ {1, \theta} ^ {T} (\mathbf {x} _ {0} | \mathbf {x} _ {1})). \end{array}
$$

Marginalizing out the variables not appearing in each term in the sum, we have, denoting by $\hat { \mathbf { q } } _ { t } ^ { T } ( \cdot | \mathbf { x } _ { 0 } )$ the marginal distribution at time t of the chain with one step transitions $\mathbf { q } _ { t } ^ { T }$ :

$$
\begin{array}{r l} & {\log (\mathbf {q} _ {\theta} ^ {T} (\mathbf {x} _ {0}) \geq \sum_ {t = T} ^ {2} \sum_ {\mathbf {x} _ {t} \in \mathcal {V} ^ {L}} \hat {\mathbf {q}} _ {t} ^ {T} (\mathbf {x} _ {t} | \mathbf {x} _ {0}) \sum_ {\mathbf {x} _ {t - 1} \in \mathcal {V} ^ {L}} \mathbf {q} _ {t} ^ {T} (\mathbf {x} _ {t - 1} | \mathbf {x} _ {t}, \mathbf {x} _ {0}) \log \left(\frac {\mathbf {q} _ {t , \theta} ^ {T} (\mathbf {x} _ {t - 1} | \mathbf {x} _ {t})}{\mathbf {q} _ {t} ^ {T} (\mathbf {x} _ {t - 1} | \mathbf {x} _ {t} , \mathbf {x} _ {0})}\right)} \\ & {\quad + \sum_ {\mathbf {x} _ {1} \in \mathcal {V} ^ {L}} \hat {\mathbf {q}} _ {1} ^ {T} (\mathbf {x} _ {1} | \mathbf {x} _ {0}) \log (\mathbf {q} _ {1, \theta} ^ {T} (\mathbf {x} _ {0} | \mathbf {x} _ {1})),} \end{array}
$$

which is precisely Eq. 10.

## C Additional Background: Continuous Time Perspective

This section contains additional background information for contextualizing P2 in the greater “discrete difusion model” landscape, and providing necessary mathematical background to understand the continuous time Markov chain setup and proof in Section Eq. D. A reader already familiar with the general discrete difusion framework and theory of continuous time Markov chains may skip this section.

## C.1 Discrete Difusion/Flow Models: Continuous Time Problem Setup

Here we discuss the general formulation of the problem setup and motivation behind discrete difusion Austin et al. (2021); Lou et al. (2023); Sun et al. (2023); Campbell et al. (2022) and discrete flow models Campbell et al. (2024); Gat et al. (2024). This helps contextualize this manuscript in the broader landscape of the generative modeling framework, as well as introduce some additional notation that will be useful for the mathematical derivations in Section D.

Suppose we have a set of N tokens, $S = \{ 1 , \ldots , N \}$ , and samples of sequences of length L comprised of elements of S from some distribution $\mathbf { p } _ { d a t a } \in \Delta ^ { N ^ { L } }$ . We seek to generate new samples from $\mathbf { p } _ { d a t a }$ via learning a “denoising” function $D _ { \theta }$ which allows one to sample from p<sub>θ</sub> ≈ p<sub>data</sub>.

To find such a function, we choose a family of probability measures $\{ P _ { t } ( \cdot ; \mu ) \} _ { t \in [ 0 , 1 ] , \mu \in \Delta ^ { N ^ { L } } }$ such that $P _ { 0 } ( \cdot ; \mu ) = \mu$ and $P _ { 1 } = \pi$ , where $\pi \in \Delta ^ { N ^ { L } }$ is some easily-sampled from reference distribution. Then we find $\{ \stackrel {  } { X } _ { t } \} _ { t \in [ 0 , 1 ] }$ a continuous-time Markov chain with $\mathbb { P } ( \overleftarrow { X } _ { t } = { \mathbf { x } } ) = \overleftarrow { P } _ { t } ( { \mathbf { x } } ; { \mathbf { p } } _ { d a t a } ) : = P _ { 1 - t } ( { \mathbf { x } } ; { \mathbf { p } } _ { d a t a } )$ , and seek to use the “denoising function” $D _ { \theta }$ to simulate a continuous time Markov chain $\{ X _ { t } ^ { \theta } \} _ { t \in [ 0 , 1 ] }$ which is close in distribution to $_ { X . } ^ {  }$ . In the end, we will have that taking $X _ { 0 } ^ { \theta } \sim \pi$ and simulating the chain to time 1, $X _ { 1 } ^ { \theta } \overset { d } { \approx } \overset  { X } _ { 1 } \sim \mathbf { p } _ { d a t a }$ . To understand what this process $X ^ { \theta }$ is and why the use of this intermediary Markov chain is useful for finding a choice of $D _ { \theta }$ , we first briefly review the theory of continuous time Markov chains in Section C.2.

## C.2 Time-Inhomogeneous Continuous Time Markov Chains (CTMC)

A (time-inhomogenous) continuous-time Markov chain $\{ X _ { t } \} _ { t \ge 0 }$ on a finite set X is a stochastic process satisfying the Markov property, which can be formally summarized $\mathbb { P } ( X _ { t } = y | X _ { s _ { 1 } } = x _ { 1 } , \ldots , X _ { s _ { k } } = x _ { k } , X _ { s } =$ $x ) = \mathbb { P } ( X _ { t } = y | X _ { s } = x ) , \forall y , x _ { 1 } , . . . , x _ { k } , x \in \mathcal { X } , 0 \leq s _ { 1 } < s _ { 2 } < . . . < s _ { k } < s < t \leq 1$ . One can construct such a process by specifying a "rate matrix" $Q _ { t } \in \mathbb { R } ^ { | \mathcal { X } | \times | \mathcal { X } | }$ with $Q _ { t } ( y , x ) > 0$ and $\begin{array} { r } { Q _ { t } ( x , x ) = - \sum _ { y \neq x } Q _ { t } ( y , x ) } \end{array}$ for all $x \neq y \in \mathcal { X }$ and $t \geq 0$ . Along with an initial distribution $\mu \in \Delta ^ { | X | }$ , Q determines the 1-dimensional time marginals $\mathbb { P } ( X _ { t } = \cdot ) \in \Delta ^ { | X | }$ via the Kolmogorov equation:

$$
\begin{array}{c} \frac {d}{d t} \mathbb {P} (X _ {t} = \cdot) = Q _ {t} \mathbb {P} (X _ {t} = \cdot), \qquad t \geq 0 \\ \mathbb {P} (X _ {0} = x) = \mu (x), \qquad x \in \mathcal {X}. \end{array}\tag{23}
$$

When the above holds, we will say $Q$ “generates” X. Note that one can see necessarily that if $Q$ generates $X$ ,

$$
Q _ {t} (y, x) := \lim _ {s \downarrow t} \frac {d}{d s} \mathbb {P} (X _ {s} = y | X _ {t} = x), \quad x \neq y \in \mathcal {X}\tag{24}
$$

Knowing the entries of $Q$ also provides a means of generating samples from $X _ { t }$ at any given time, since paths of $\{ X _ { t } \} _ { t \ge 0 }$ can be realized via a sequence of jump times $\{ \tau _ { n } \} _ { n \in \mathbb { N } }$ , with $\tau _ { i } = \operatorname* { i n f } \{ t > \tau _ { i - 1 } : X _ { t } \neq X _ { \tau _ { i - 1 } } \}$ and the efective discrete-time jump process $\{ X _ { \tau _ { i } } \} _ { i \in \mathbb { N } }$ . Then

$$
\mathbb {P} (X _ {\tau_ {i + 1}} = y | X _ {\tau_ {i}} = x, \tau_ {i + 1} = t) = - \frac {Q _ {t} (y , x)}{Q _ {t} (x , x)},\tag{25}
$$

and

$$
\log (\mathbb {P} (\tau_ {i + 1} > t | X _ {\tau_ {i}} = x, \tau_ {i} = s)) = \int_ {s} ^ {t} Q _ {p} (x, x) d p.
$$

For more background on time-inhomogenous continuous-time Markov chains, see e.g. Chapter 2 of Yin & Zhang (2013) or the appendix of Ren et al. (2024).

## C.3 The Role of the Denoiser and the Approximate Backwards Process

In the “discrete difusion model” framework, one in fact starts with specifying a rate matrix $Q _ { t }$ generating some Markov chain $\{ X _ { t } \} _ { t \in [ 0 , 1 ] }$ with $X _ { 0 } \sim \mathbf { p } _ { d a t a }$ and $X _ { 1 } \sim \pi$ and defines $P _ { t } ( \mathbf { x } ; \mathbf { p } _ { d a t a } ) : = \mathbb { P } ( X _ { t } = \mathbf { x } ) . \stackrel {  } { X } _ { t }$ is then simply defined as $X _ { 1 - t } ,$ , and a rate matrix $\left. \sum _ { Q _ { t } } \right.$ which generates $\overleftarrow { X }$ can be found from $Q _ { t }$ via an application of Bayes’ rule (see Prop. 3.2 in Sun et al. (2023)). In the “Discrete Flow Model” framework, one instead starts with a desired interpolation (often linear) $P _ { t } ( \cdot ; \mu )$ between arbitrary $\mu \in \Delta ^ { N ^ { L } }$ and π, and constructs a rate matrix $\stackrel {  } { Q } _ { t }$ generating a $\stackrel {  } { X } _ { t }$ with one-dimensional time marginals $ _ { P d a t a } )$ a posteriori.

As explained above, in order to generate samples of $\stackrel {  } { X } _ { t }$ at a given time (and in particular of $\stackrel {  } { X } _ { 1 } \sim \mathbf { p } _ { d a t a } )$ , it is suficient to have access to the entries of $\stackrel {  } { Q } _ { t }$ . In both settings, however, the entries of $\stackrel {  } { Q } _ { t }$ will naturally depend on the unknown distribution $\mathbf { p } _ { d a t a }$ , and hence, using the form of this dependence, a denoiser function $D _ { \theta }$ is constructed in an attempt to approximate these unknown quantities. This results in a rate matrix $Q _ { t } ^ { \theta } \approx \stackrel {  } { Q } _ { t } .$ , which generates the approximate backwards Markov chain $\{ X _ { t } ^ { \theta } \} _ { t \in [ 0 , 1 ] }$ . The distribution of the output of the resulting sampling scheme is then

$$
\mathbf {p} _ {\theta} = P _ {1} ^ {\theta} = \mathbb {P} (X _ {1} ^ {\theta} = \cdot).
$$

The form of the denoiser, as well as the choice of $P _ { t } , \stackrel {  } { Q } .$ , and $Q ^ { \theta }$ in our particular setup are introduced in Sections 2.1, C.5, and D.1.

## C.4 The Conditional Backwards Process

A pervasive assumption made in the literature is that for any fixed $\mathbf { x } _ { 0 } \in S ^ { L }$

$$
P _ {t} (y; \delta (\mathbf {x} _ {0})) = \prod_ {i = 1} ^ {L} p _ {t} (y ^ {i} | x _ {0} ^ {i})\tag{26}
$$

for a family of probability measures $\{ p _ { t } ( \cdot | x _ { 0 } ^ { i } ) \} _ { t \in [ 0 , 1 ] } \subset \Delta ^ { N }$ . We denote by $\overleftarrow { X } ^ { \mathbf { x } _ { 0 } }$ the “conditional backwards process,” on the point $\mathbf { x } _ { 0 } ,$ , defined as the Markov chain with distribution $\mathbb { P } ( \overset {  } { X } _ { t } ^ { \mathbf { x } _ { 0 } } = \mathbf { y } ) = \overset  { P } ( \mathbf { y } ; \delta ( \mathbf { x } _ { 0 } ) )$ , and by $\dot { Q }$ ←x its rate matrix. The coordinates $( \overleftarrow { X } _ { 1 } ^ { \mathbf { x } _ { 0 } } , \ldots , \overleftarrow { X } _ { L } ^ { \mathbf { x } _ { 0 } } )$ of $\overleftarrow { X } ^ { \mathbf { x } _ { 0 } }$ are thus assumed independent, and each described by a continuous-time Markov chain $\{ \stackrel {  } { x } _ { t } ^ { i } \} _ { t \in [ 0 , 1 ] }$ with rate matrix $\hat { \boldsymbol { Q } } _ { t } ^ { x _ { 0 } ^ { \imath } } \in \mathbb { R } ^ { N \times N }$ for $i = 1 , \ldots , L .$ $t \in [ 0 , 1 ]$ that yields $\mathbb { P } ( \stackrel {  } { x } _ { t } ^ { i } = y ^ { i } ) = \stackrel {  } { p } _ { t } ( y ^ { i } | x _ { 0 } ^ { i } )$ for all $t \in [ 0 , 1 ]$ and $y ^ { i } \in S$ . The hope in making this assumption is that each coordinate of $X _ { t } ^ { \theta } \approx \stackrel {  } { X } _ { t }$ will be able to be simulated independently in parallel without introducing significant error Sun et al. (2023).

$P _ { t } ( y ; \mu )$ is taken to be linear in $\mu ,$ so we have $\begin{array} { r } { P _ { t } ( \mathbf { y } ; \mathbf { p } _ { d a t a } ) = \sum _ { \mathbf { x } \in S ^ { L } } P _ { t } ( \mathbf { y } ; \delta ( \mathbf { x } ) ) \mathbf { p } _ { d a t a } ( \mathbf { x } ) } \end{array}$ , and hence specifying $p _ { t } ( j | i ) , i , j \in S$ is what ultimately what determines the form of $\stackrel {  } { Q } _ { t }$ and hence the functions needed to be approximated by $D _ { \theta }$ in order to construct $Q ^ { \theta }$ . The most common choices explored this far in the literature are the “uniform difusion,” Lou et al. (2023); Schif et al. (2025) which sets

$$
p _ {t} (j | i) = \alpha_ {t} \mathrm{Cat} (j; \delta (i)) + \frac {1 - \alpha_ {t}}{S}\tag{27}
$$

for $\alpha : [ 0 , 1 ]  [ 0 , 1 ]$ with $\alpha _ { 0 } = 1 , \alpha _ { 1 } = 0$ and the “masked difusion,” which is out subject of focus.

Note that in the Discrete Difusion Model framework, $p _ { t } ( j | i )$ is not always defined explicitly, and is often implicitly prescribed by asserting the “forward noising” process is the independent evolution of a CTMC on S with rate matrix $\hat { Q _ { t } } \in \mathbb R ^ { N \times N }$ on each coordinate (see e.g. Equations (15) and (16) in Lou et al. (2023)). $p _ { t } ( j | i )$ is then found by solving Eq. 23 with $Q = \hat { Q }$ and $\mu = \delta ( i )$

## C.5 Masked Difusion Model: Continuous Time Formulation

In the case of a “masked difusion model,” one extends S to ${ \bar { S } } = S \cup \{ \mathbf { m } \}$ for m some “masked state” outside the dictionary of tokens S, and takes $p _ { t } ( j | i ) = \alpha _ { t } \mathrm { C a t } ( j ; \delta ( i ) ) + ( 1 - \alpha _ { t } ) \mathrm { C a t } ( j ; \delta ( \mathbf { m } ) )$ ). From here on we will refer to $\bar { S }$ as V as in the body of the manuscript. This choice of forward/noising process has been seen to outperform the uniform difusion process Schif et al. (2025) as well as other choices of $p _ { t }$ Austin et al. (2021) consistently among applications. It corresponds to the coordinate-wise forward matrix given by, for $i \neq j \in \mathcal { V } ;$

$$
\hat {Q} _ {t} (j, i) = \left\{ \begin{array}{l l} \sigma (t) & , \quad j = \mathbf {m}, i \neq \mathbf {m} \\ 0 & , \quad \text { otherwise } \end{array} \right.
$$

with $\begin{array} { r } { \sigma ( t ) = - \frac { d } { d t } \log ( \alpha _ { t } ) } \end{array}$ , and through Eq. 26 yields Eq. 1.

In the masked-difusion setting, both the Discrete Flow Model and Discrete Difusion Model framework use the rate matrices for the conditional reversed process’ coordinates (Campbell et al. (2024) Appendix F.1.) for $i \neq j \in \mathcal { V } ;$

$$
\stackrel {\wedge} {Q} _ {t} ^ {x _ {0} ^ {i}} (j, i) = \left\{ \begin{array}{l l} - \frac {\frac {d \alpha_ {1 - t}}{d t}}{1 - \alpha_ {1 - t}} & , i = \mathbf {m}, j = x _ {0} ^ {i} \\ 0 & , \text {otherwise} \end{array} \right..
$$

The resulting conditional rate matrix generating $\overleftarrow { X } _ { t } ^ { \mathbf { x } _ { 0 } }$ is then, for $\mathbf x \neq \mathbf y \in \mathcal V ^ { L }$

$$
\stackrel {{\leftarrow}} {Q} _ {t} ^ {\mathbf {x} _ {0}} (\mathbf {y}, \mathbf {x}) = \left\{ \begin{array}{l l} - \frac {\frac {d \alpha_ {1 - t}}{d t}}{1 - \alpha_ {1 - t}}, & d _ {H A M} (\mathbf {x}, \mathbf {y}) = 1, x ^ {i} \neq y ^ {i}, x ^ {i} = \mathbf {m}, y ^ {i} = x _ {0} ^ {i} \\ 0, & \text { otherwise } \end{array} \right.\tag{28}
$$

with $\begin{array} { r } { \overleftarrow { Q } _ { t } ^ { - \mathbf { x } _ { 0 } } ( \mathbf { x } , \mathbf { x } ) = \frac { \frac { d \alpha _ { 1 - t } } { d t } } { 1 - \alpha _ { 1 - t } } \sum _ { i = 1 } ^ { L } \mathrm { C a t } ( x ^ { i } ; \delta ( \mathbf { m } ) ) } \end{array}$ , and the a rate matrix generating $\stackrel {  } { X } _ { t }$ is given for $\mathbf x \neq \mathbf y \in \mathcal V ^ { L }$ ， by:

$$
\stackrel {{\leftarrow}} {Q} (\mathbf {y}, \mathbf {x}) = \left\{ \begin{array}{l l} - \frac {\frac {d \alpha_ {1 - t}}{d t}}{1 - \alpha_ {1 - t}} p _ {d a t a} ^ {i} (y ^ {i} | \mathbf {x} \neq \mathbf {m}), & d _ {H A M} (\mathbf {x}, \mathbf {y}) = 1, x ^ {i} \neq y ^ {i}, x ^ {i} = \mathbf {m} \\ 0, & \text { otherwise } \end{array} \right.
$$

and $\begin{array} { r } { \overleftarrow { Q } ( \mathbf { x } , \mathbf { x } ) = \frac { \frac { d \alpha _ { 1 - t } } { d t } } { 1 - \alpha _ { 1 - t } } \sum _ { i = 1 } ^ { L } \mathrm { C a t } ( x ^ { i } ; \delta ( \mathbf { m } ) ) } \end{array}$ (see e.g. Ou et al. (2024) Theorem 1 and Equation (3.1)). Here for $i \in \{ 1 , \ldots , L \}$ , and $j \in \mathcal V ;$

$$
p _ {d a t a} ^ {i} (j | \mathbf {z} _ {\neq \mathbf {m}}) := \mathbf {p} _ {d a t a} (\{\mathbf {x}: x ^ {i} = j \} | \mathbf {z} _ {\neq \mathbf {m}}),
$$

where for $\mathbf { z } \in \mathcal { V } ^ { L } , \mathbf { z } _ { \neq \mathbf { m } }$ denotes the coordinates of z which are not equal to m, and $d _ { H A M }$ is Hamming distance.

Note that reversing time to 1 − t and approximating $\frac { d \alpha _ { t } } { d t }$ via $T [ \alpha _ { t + 1 / T } \ - \ \alpha _ { t } ]$ and $\frac { d \mathbb { P } ( \overleftarrow { X } _ { t } = \mathbf { x } | \overleftarrow { X } _ { s } = \mathbf { y } ) } { d t }$ via $T [ \mathbb { P } ( \overleftarrow { X } _ { t + 1 / T } = { \mathbf { x } } | \overleftarrow { X } _ { s } = { \mathbf { y } } ) - \mathbb { P } ( \overleftarrow { X } _ { t + 1 / T } = { \mathbf { x } } | \overleftarrow { X } _ { s } = { \mathbf { y } } ) ]$ yields the discrete-time approximation scheme Eq. 2 by way of Eq. 24. The is precisely the limit taken in Eq. 13.

One then parameterizes the approximate backwards process $X ^ { \theta , \mathrm { { m a s k } } }$ via the denoiser $D _ { \theta }$ by taking it to be the CTMC with rate matrix $\mathbf { x } \neq \mathbf { y } \in \mathcal { V } ^ { L }$ :

$$
Q ^ {\theta , \text { mask }} (\mathbf {y}, \mathbf {x}) = \left\{ \begin{array}{l l} - \frac {\frac {d \alpha_ {1 - t}}{d t}}{1 - \alpha_ {1 - t}} \text { Cat } (y ^ {i}; D _ {\theta} ^ {i} (\mathbf {x})), & d _ {H A M} (\mathbf {x}, \mathbf {y}) = 1, x ^ {i} \neq y ^ {i}, x ^ {i} = \mathbf {m} \\ 0, & \text { otherwise } \end{array} \right.\tag{29}
$$

In the same way as with $\overleftarrow { X } _ { t } .$ , the discrete time approximation scheme for $X ^ { \theta , \mathrm { { m a s k } } }$ is $\operatorname { E q . 3 }$

## C.6 Role of the ELBO

The training objective in general is obtained via the same methodology in both the Discrete Flow and Discrete Difusion Model framework—in fact, this methodology can also be used for continuous difusion models and denoising processes described by more general Markovian dynamics Benton et al. (2024).

We seek to minimize the KL divergence:

$$
\begin{array}{r l} & D _ {K L} (\mathbf {p} _ {d a t a} | | P _ {1} ^ {\theta}) = \sum_ {\mathbf {x} \in S ^ {L}} \mathbf {p} _ {d a t a} (\mathbf {x}) \log \left(\frac {\mathbf {p} _ {d a t a} (\mathbf {x})}{P _ {1} ^ {\theta} (\mathbf {x})}\right) \\ & \qquad = \sum_ {\mathbf {x} \in S ^ {L}} \mathbf {p} _ {d a t a} (\mathbf {x}) \log \mathbf {p} _ {d a t a} (\mathbf {x}) - \sum_ {\mathbf {x} \in S ^ {L}} \mathbf {p} _ {d a t a} (\mathbf {x}) \log (P _ {1} ^ {\theta} (\mathbf {x})) \\ & \qquad = - H (\mathbf {p} _ {d a t a}) - \sum_ {\mathbf {x} \in S ^ {L}} \mathbf {p} _ {d a t a} (\mathbf {x}) \log (P _ {1} ^ {\theta} (\mathbf {x})). \end{array}
$$

The first term - that is, the Shannon entropy of $\mathbf { p } _ { d a t a } , \ H ( \mathbf { p } _ { d a t a } )$ - is constant in $\theta ,$ and so we turn our attention to finding an “Evidence Based Lower Bound”

$$
E (\mathbf {x} _ {0}) \leq \log (P _ {1} ^ {\theta} (\mathbf {x} _ {0}))
$$

for each fixed $\mathbf { x } _ { 0 } \in S ^ { L }$ . The loss that we seek to minimize is then defined as:

$$
\mathcal {L} _ {E} ^ {\theta} := - \sum_ {\mathbf {x} \in S ^ {L}} \mathbf {p} _ {d a t a} (\mathbf {x}) E (\mathbf {x}),\tag{30}
$$

since $D _ { K L } ( { \bf p } _ { d a t a } | | P _ { 1 } ^ { \theta } ) \leq - H ( { \bf p } _ { d a t a } ) + \mathcal { L } _ { E } ^ { \theta }$

Letting $\mathbb { P } ^ { \mathbf { x } _ { 0 } } \in \mathcal { P } ( D ( [ 0 , 1 ] ; S ^ { L } ) )$ denote the Law (on the Skorokhod space of all cádlág paths from [0, 1] to $S ^ { L } )$ of $_ { X } ^ {  \mathbf { x } _ { 0 } }$ and $\mathbb { P } ^ { \theta } \in \mathcal { P } ( D ( [ 0 , 1 ] ; S ^ { L } ) )$ ) the same but for $X ^ { \theta }$ , we have, by the data-processing inequality (see, e.g. Budhiraja & Dupuis (2019) Lemma 2.4 (f)):

$$
\log (P _ {1} ^ {\theta} (\mathbf {x} _ {0})) = - D _ {K L} (\delta (\mathbf {x} _ {0}) | | P _ {1} ^ {\theta}) \geq - D _ {K L} (\mathbb {P} ^ {\mathbf {x} _ {0}} | | \mathbb {P} ^ {\theta}) := E (\mathbf {x} _ {0}),\tag{31}
$$

That is, in order to make sure the approximate reverse process has the desired terminal distribution, by minimizing $\mathcal { L } _ { E }$ we attempt to make it so that the entire path of the approximate reverse process matches that of the exact one. Eq. 31 is efectively the same as the first step in the proof of the discrete time ELBO - see B.5.

$E ( \mathbf { x } _ { \mathrm { 0 } } )$ can be found via an application of Girsanov’s Theorem for Markov Jump processes (see $\mathrm { e . g . }$ Theorem III.5.34 in Jacod & Shiryaev (2013) for a general result or Ren et al. (2024) Theorem 3.3 for the specific x Markov Chain setting), and is expressed solely in terms of $\overleftarrow { Q } ^ { \mathrm { ~ \tiny ~ , ~ } } D _ { \theta } ,$ and $P _ { t } ( \cdot ; \delta ( { \bf x } _ { 0 } ) )$ ). This yields an expression analogous to the discrete time ELBO Eq. 10 but for continuous time Markov chains -see the first line in the proof in Subsection D.2.

In the masked difusion setting, where $Q ^ { \theta }$ is given by $Q ^ { \theta , \mathrm { m a s k } }$ from Eq. 29 and $\stackrel {  } { Q } ^ { \mathbf { x } _ { 0 } }$ is given by Eq. 28, this expression is given by Eq. 4 (see Sahoo et al. (2024) Equation (10)). This is exactly $\mathcal { E } _ { D }$ from Proposition 1.

## D Mathematical Details: P2 from a CTMC Point of View

In this Section we continue to use the notation established in Section C.

## D.1 P2 Continuous Time Formulation

In order to formulate P2 we begin by modifying the jump matrix for the approximate backwards process Eq. 29, recall the planner function $\check { G _ { \phi } } : \mathcal { V } ^ { L } \times \mathcal { V } ^ { \bar { L } } \to [ \bar { 0 } , 1 ] ^ { \bar { L } } . \ G _ { \phi } ^ { j } ( \mathbf { z } , \mathbf { x } )$ approximates the probability that the j’th token in a partially denoised sequence $\mathbf { x } \in \mathcal { V } ^ { L }$ should be (re)sampled given the conditional information about the rest of the sequence x and of the clean data z as predicted by $D _ { \theta }$

We define $F _ { \theta , \phi } : \mathcal { V } ^ { L } \times \mathcal { V } ^ { L } \to [ 0 , 1 ] ^ { L }$ by

$$
\begin{array}{r l} & F _ {\theta , \phi} ^ {j} (\mathbf {y}, \mathbf {x}) := \mathrm{Cat} (x ^ {j}; \delta (\mathbf {m})) \mathbb {E} _ {Z \sim D _ {\theta} (\mathbf {x})} [ G _ {\phi} ^ {j} (Z ^ {- j, y ^ {j}}, \mathbf {x}) ] \\ & \qquad + (1 - \mathrm{Cat} (x ^ {j}; \delta (\mathbf {m}))) \mathbb {E} _ {Z \sim D _ {\theta} (\mathbf {x})} [ G _ {\phi} ^ {j} (Z, \mathbf {x}) ] \end{array}
$$

where here we use the shorthand $Z \sim D _ { \theta } ( \mathbf { x } )$ to mean $Z \sim \otimes _ { i = 1 } ^ { L } D _ { \theta } ^ { i } ( { \bf x } )$ , and introduce the notation $\mathbf { z } ^ { - i , j }$ for $\mathbf { z } \in \mathcal { V } ^ { L } , i \in [ L ]$ , and $j \in \mathcal V$ to mean the element of $\mathcal { V } ^ { L }$ resulting from replacing the i’th coordinate of z with $j$ Via our interpretation of the role of $G _ { \theta } , F _ { \theta } ^ { j } ( \mathbf { y } , \mathbf { x } )$ gives the probability that the j’th position of x should be (re)sampled given the information about the rest of the sequence x and the data’s j’th token via averaging out the information provided about the rest of the data’s tokens from $D _ { \theta }$

Finally, we define

$$
\hat {D} _ {\theta} ^ {i} (\mathbf {x}) = D _ {\theta} ^ {i} (\mathbf {x}) \mathrm{Cat} (x ^ {i}; \delta (\mathbf {m})) + \frac {D _ {\theta} ^ {i} (x ^ {- i , \mathbf {m}})}{1 - \mathrm{Cat} (x ^ {i} ; D _ {\theta} ^ {i} (\mathbf {x} ^ {- i , \mathbf {m}}))} (1 - \mathrm{Cat} (x ^ {i}; \delta (\mathbf {m}))).
$$

That is, when $x ^ { i }$ is masked $\mathrm { C a t } ( y ^ { i } ; \hat { D } _ { \theta } ^ { i } ( { \bf x } ) )$ approximates the probability that the i’th token of x should be unmasked to $y ^ { i }$ given the conditional information about the unmasked tokens in $\mathbf { x } ,$ and when $x ^ { i }$ is not masked, $\hat { D } _ { \theta } ^ { i } ( { \bf x } )$ approximates the probability that i’th token of x should be resampled to a value other than $x ^ { i }$ , given the conditional information about the unmasked tokens in x other than $x ^ { i }$

We now seek to modify $Q ^ { \theta , \mathrm { m a s k } }$ from $\operatorname { E q }$ . 29 in a way so that F<sub>θ,ϕ</sub> - by way of the planner $G _ { \phi } \mathrm { ~ - ~ } \mathrm { p l a y s }$ the role of selecting which position should be unmasked/resampled and $\hat { D } _ { \theta }$ plays the role of choosing what it should be (re)sampled to.

For x $\neq y \in \mathcal { V } ^ { L }$ , we thus set:

$$
Q _ {t} ^ {\theta , \phi} (\mathbf {y}, \mathbf {x}) := \left\{ \begin{array}{l l} - \frac {\frac {d \alpha_ {1 - t}}{d t}}{1 - \alpha_ {1 - t}} F _ {\theta , \phi} ^ {i} (\mathbf {y}, \mathbf {x}) \mathrm{Cat} (y ^ {i}; \hat {D} _ {\theta} ^ {i} (\mathbf {x})) & , d _ {H A M} (\mathbf {x}, \mathbf {y}) = 1, x ^ {i} \neq y ^ {i} \\ 0 & , \text {otherwise} \end{array} \right..\tag{32}
$$

Note that, via the same formal discrete time approximation discussed above $\operatorname { E q } .$ . 29, the discrete time sampling scheme outlined in Section 3.1 approximates the distribution of the CTMC $X ^ { \theta , \phi }$ with rate matrix $Q ^ { \theta , \phi }$ . This is precisely the limit taken in Eq. 14.

## D.2 Proof of the ELBO Proposition 1: CTMC Version

As per Eq. 31, it sufices to find a lower bound on $- D _ { K L } ( \mathbb { P } ^ { \mathbf { x } _ { 0 } } | | \mathbb { P } ^ { \theta , \phi } )$ , where $\mathbb { P } ^ { \mathbf { x } _ { 0 } }$ is the Law of the continuous time Markov chain $\overleftarrow { X } ^ { \cdots }$ with rate matrix $\dot { Q }$ ←x<sub>0</sub> given by Eq. 28, $\mathbb { P } ^ { \theta , \phi }$ is the Law of the continuous time Markov chain $X ^ { \theta , \phi }$ with rate matrix $Q ^ { \theta , \phi }$ given by Eq. 32, and $\overleftarrow { \boldsymbol { X } } _ { 0 } ^ { \alpha _ { 0 } } = X _ { 0 } ^ { \theta } = ( \mathbf { m } , \ldots , \mathbf { m } )$ . Via an application of Girsanov’s Theorem for CTMCs (see e.g. Theorem III.5.34 in Jacod & Shiryaev (2013) for a general result or Ren et al. (2024) Theorem 3.3 for the specific CTMC setting):

$$
\begin{array}{l} - D _ {K L} (\mathbb {P} ^ {\mathbf {x} _ {0}} | | \mathbb {P} ^ {\theta}) \\ = - \int_ {0} ^ {1} \mathbb {E} _ {\mathbf {x} _ {t} \sim \mathbf {p} _ {1 - t} (\cdot ; \mathbf {x} _ {0})} \bigg [ - Q _ {t} ^ {\theta , \phi} (\mathbf {x} _ {t}, \mathbf {x} _ {t}) + \stackrel {{\leftarrow \mathbf {x} _ {0}}} {{Q}} (\mathbf {x} _ {t}, \mathbf {x} _ {t}) \\ \quad + \sum_ {\mathbf {y} \neq \mathbf {x} _ {t}} \stackrel {{\leftarrow \mathbf {x} _ {0}}} {{Q}} (\mathbf {y}, \mathbf {x} _ {t}) \log \left(\frac {\stackrel {{\leftarrow \mathbf {x} _ {0}}} {{Q}} (\mathbf {y} , \mathbf {x} _ {t})}{Q _ {t} ^ {\theta , \phi} (\mathbf {y} , \mathbf {x} _ {t})}\right) \bigg ] d t \\ = - \int_ {0} ^ {1} \frac {\frac {d \alpha_ {t}}{d t}}{1 - \alpha_ {t}} \mathbb {E} _ {\mathbf {x} _ {t} \sim \mathbf {p} _ {t} (\cdot ; \mathbf {x} _ {0})} \bigg [ \sum_ {i = 1} ^ {L} \Biggl \{\mathrm{Cat} (x _ {t} ^ {i}; \delta (\mathbf {m})) (1 - \mathbb {E} _ {Z \sim D _ {\theta} (\mathbf {x} _ {t})} [ G _ {\phi} ^ {i} (Z, \mathbf {x} _ {t}) ]) \\ \quad - (1 - \mathrm{Cat} (x _ {t} ^ {i}; \delta (\mathbf {m}))) \mathbb {E} _ {Z \sim D _ {\theta} (\mathbf {x} _ {t})} [ G _ {\phi} ^ {i} (Z, \mathbf {x} _ {t}) ] \\ \quad + \mathrm{Cat} (x _ {t} ^ {i}; \delta (\mathbf {m})) \log (F _ {\theta , \phi} ^ {i} (\mathbf {x} _ {0}, \mathbf {x} _ {t}) \mathrm{Cat} (x _ {0} ^ {i}; \hat {D} _ {\theta} ^ {i} (\mathbf {x} _ {t}))) \Biggr \} \bigg ] d t, \end{array}
$$

where in the third equality we have inserted the definitions of $\stackrel {  } { Q } ^ { \mathbf { x } _ { 0 } }$ and $Q ^ { \theta , \phi }$ and reversed the role of the time parameter $t \mapsto 1 - t ,$ , and ${ \mathbf { } } p _ { t }$ is as in Eq. 1.

We consider this as 4 parts:

$$
\begin{array}{l} E _ {1} (\mathbf {x} _ {0}) := - \int_ {0} ^ {1} \frac {\frac {d \alpha_ {t}}{d t}}{1 - \alpha_ {t}} \mathbb {E} _ {\mathbf {x} _ {t} \sim \mathbf {p} _ {t} (\cdot ; \mathbf {x} _ {0})} \bigg [ \sum_ {i = 1, x _ {t} ^ {i} = \mathbf {m}} ^ {L} \big (1 - \mathbb {E} _ {Z \sim D _ {\theta} (\mathbf {x} _ {t})} [ G _ {\phi} ^ {i} (Z, \mathbf {x} _ {t}) ] \big) \bigg ] d t \\ E _ {2} (\mathbf {x} _ {0}) := - \int_ {0} ^ {1} \frac {\frac {d \alpha_ {t}}{d t}}{1 - \alpha_ {t}} \mathbb {E} _ {\mathbf {x} _ {t} \sim \mathbf {p} _ {t} (\cdot ; \mathbf {x} _ {0})} \bigg [ \sum_ {j = 1, x _ {t} ^ {i} \neq \mathbf {m}} ^ {L} \big (- \mathbb {E} _ {Z \sim D _ {\theta} (\mathbf {x} _ {t})} [ G _ {\phi} ^ {i} (Z, \mathbf {x} _ {t}) ] \big) \bigg ] d t \\ E _ {3} (\mathbf {x} _ {0}) := - \int_ {0} ^ {1} \frac {\frac {d \alpha_ {t}}{d t}}{1 - \alpha_ {t}} \mathbb {E} _ {\mathbf {x} _ {t} \sim \mathbf {p} _ {t} (\cdot ; \mathbf {x} _ {0})} \bigg [ \sum_ {l = 1, x _ {t} ^ {i} = \mathbf {m}} ^ {L} \log (F _ {\theta , \phi} ^ {i} (\mathbf {x} _ {0}, \mathbf {x} _ {t})) \bigg ] d t \\ E _ {4} (\mathbf {x} _ {0}) := - \int_ {0} ^ {1} \frac {\frac {d \alpha_ {t}}{d t}}{1 - \alpha_ {t}} \mathbb {E} _ {\mathbf {x} _ {t} \sim \mathbf {p} _ {t} (\cdot ; \mathbf {x} _ {0})} \bigg [ \sum_ {k = 1, x _ {t} ^ {i} = \mathbf {m}} ^ {L} \log (\mathrm{Cat} (x _ {0} ^ {i}; \hat {D} _ {\theta} ^ {i} (\mathbf {x} _ {t}))) \bigg ] d t \end{array}
$$

Recalling that $\begin{array} { r } { \frac { d \alpha _ { t } } { d t } \leq 0 } \end{array}$ for all $t \in [ 0 , 1 ]$ and $G _ { \phi } ^ { i } ( Z , \mathbf { x } ) \in [ 0 , 1 ]$ for all $i \in \{ 1 , \ldots , L \} , \mathbf { x } \in \mathcal { V } ^ { L }$ , we see $E _ { 1 } ( \mathbf { x } _ { 0 } )$ is positive for all $\mathbf { x } _ { 0 } \in \mathcal { V } ^ { L }$ , and artificially attempting to ensure that the rates of the original CTMC and our modified one do not difer too much out of masked positions (see the discussion of the “Rate Forcing Term” in Appendix C.2 of Campbell et al. (2024)). Hence we simply bound it below by zero:

$$
E _ {1} (\mathbf {x} _ {0}) \geq 0,
$$

because we are only interested in $P _ { 1 } ^ { \theta }$ being close to $\mathbf { p } _ { d a t a } .$ , not the entire trajectory of the chains $X ^ { \theta . \phi }$ and $\overleftarrow { X }$ being close.

For $E _ { 3 } ( \mathbf { x } _ { 0 } )$ we note that, by definition, when $x _ { t } ^ { i } = \mathbf { m } , F _ { \theta , \phi } ^ { i } ( \mathbf { x } _ { 0 } , \mathbf { x } _ { t } ) = \mathbb { E } _ { Z \sim D _ { \theta } ( \mathbf { x } _ { t } ) } [ G _ { \phi } ^ { i } ( Z , \mathbf { x } _ { t } ) ]$ . Upon inserting this equality, we observe that, up to the time change $s = 1 - t ,$ these are the same 4 terms from Eq. 20 which we bound below by $\mathcal { E } ( \mathbf { x } _ { 0 } )$ in the time discritization version of the proof found in Section B, The rest of the proof thus proceeds identically.

## D.3 Equivalence of MDMs with AOARMs

Here, for completeness, we recall the connection between masked difusion language models and Any-Order Autoregressive Models Uria et al. (2014); Hoogeboom et al. (2022) as described in Zheng et al. (2025); Ou et al. (2024). We start by providing a simplified derivation of the equivalence of the two types of models’ sampling schemes.

We begin by obtaining the diagonals for the matrix Eq. 29. Recalling $D _ { \theta } ^ { i } ( { \bf x } ) \ = \ \delta ( x ^ { i } ) \ \mathrm { i f } x ^ { i } \neq { \bf m }$ , and $\begin{array} { r } { \sum _ { y ^ { i } = 1 } ^ { d - 1 } \operatorname { C a t } ( y ^ { i } ; D _ { \theta } ^ { i } ( { \bf x } ) ) = 1 ~ \mathrm { i f ~ } x ^ { i } = { \bf m } } \end{array}$ :

$$
\begin{array}{l} - \sum_ {y \neq x} Q _ {t} ^ {\theta , \text {mask}} (\mathbf {y}, \mathbf {x}) = \frac {\frac {d \alpha_ {1 - t}}{d t}}{1 - \alpha_ {1 - t}} \sum_ {i = 1} ^ {L} \text {Cat} (x ^ {i}; \delta (\mathbf {m})) \sum_ {y ^ {i} \neq x ^ {i}} \text {Cat} (y ^ {i}; D _ {\theta} ^ {i} (\mathbf {x})) \\ = \frac {\frac {d \alpha_ {1 - t}}{d t}}{1 - \alpha_ {1 - t}} \sum_ {i = 1} ^ {L} \text {Cat} (x ^ {i}; \delta (\mathbf {m})) \sum_ {y ^ {i} = 1} ^ {d - 1} \text {Cat} (y ^ {i}; D _ {\theta} ^ {i} (\mathbf {x})) \\ = \frac {\frac {d \alpha_ {1 - t}}{d t}}{1 - \alpha_ {1 - t}} \sum_ {i = 1} ^ {L} \text {Cat} (x ^ {i}; \delta (\mathbf {m})). \end{array}
$$

Then, if one considers the efective jump chain’s transition probabilities as described in Eq. 25, we have, for $\mathbf { x } \neq \mathbf { y } \colon$

$$
\begin{array}{c} \mathbb {P} (X _ {\tau_ {k + 1}} ^ {\theta , \text {mask}} = \mathbf {y} | X _ {\tau_ {k}} ^ {\theta , \text {mask}} = \mathbf {x}, \tau_ {k + 1} = t) = \mathbb {P} (X _ {\tau_ {k + 1}} ^ {\theta , \text {mask}} = \mathbf {y} | X _ {\tau_ {k}} ^ {\theta , \text {mask}} = \mathbf {x}) \\ = \frac {\operatorname{Cat} (x ^ {i} ; \delta (\mathbf {m})) \operatorname{Cat} (y ^ {i} ; D _ {\theta} ^ {i} (\mathbf {x}))}{\sum_ {i = 1} ^ {L} \operatorname{Cat} (x ^ {i} ; \delta (\mathbf {m}))}, \end{array}
$$

when $d _ { H A M } ( \mathbf { x } , \mathbf { y } ) = 1$ and $x ^ { i } \neq y ^ { i }$ , and 0 when $d _ { H A M } ( \mathbf { x } , \mathbf { y } ) \neq 1$

Then, for any $j \in \{ 1 , \ldots , L \}$

$$
\begin{array}{l} \mathbb {P} ([ X _ {\tau_ {k + 1}} ^ {\theta , \text {mask}} ] ^ {j} \neq [ X _ {\tau_ {k}} ^ {\theta , \text {mask}} ] ^ {j} | X _ {\tau_ {k}} ^ {\theta , \text {mask}} = \mathbf {x}, \tau_ {k + 1} = t) = \sum_ {y ^ {j} \neq x ^ {j}} \mathbb {P} ([ X _ {\tau_ {k + 1}} ^ {\theta , \text {mask}} ] ^ {j} = y ^ {j} | X _ {\tau_ {k}} ^ {\theta , \text {mask}} = \mathbf {x}) \\ \qquad = \sum_ {y ^ {j} \neq x ^ {j}} \frac {\text {Cat} (x ^ {j} ; \delta (\mathbf {m}) \text {Cat} (y ^ {j} ; D _ {\theta} ^ {j} (\mathbf {x}))}{\sum_ {i = 1} ^ {L} \text {Cat} (x ^ {i} ; \delta (\mathbf {m}))} \\ \qquad = \frac {\text {Cat} (x ^ {j} ; \delta (\mathbf {m})) \sum_ {y ^ {j} = 1} ^ {d - 1} \text {Cat} (y ^ {j} ; D _ {\theta} ^ {j} (\mathbf {x}))}{\sum_ {i = 1} ^ {L} \text {Cat} (x ^ {i} ; \delta (\mathbf {m}))} \\ \qquad = \frac {\text {Cat} (x ^ {j} ; \delta (\mathbf {m}))}{\sum_ {i = 1} ^ {L} \text {Cat} (x ^ {i} ; \delta (\mathbf {m}))} \end{array}
$$

and, for x such that $x ^ { j } = \mathbf { m }$

$$
\begin{array}{l} \mathbb {P} ([ X _ {\tau_ {k + 1}} ^ {\theta , \mathrm{mask}} ] ^ {j} = y ^ {j} | X _ {\tau_ {k}} ^ {\theta , \mathrm{mask}} = \mathbf {x}, \tau_ {k + 1} = t, [ X _ {\tau_ {k + 1}} ^ {\theta , \mathrm{mask}} ] ^ {j} \neq [ X _ {\tau_ {k}} ^ {\theta , \mathrm{mask}} ] ^ {j}) \\ = \frac {\mathbb {P} ([ X _ {\tau_ {k + 1}} ^ {\theta , \mathrm{mask}} ] ^ {j} = y ^ {j} , [ X _ {\tau_ {k + 1}} ^ {\theta , \mathrm{mask}} ] ^ {j} \neq [ X _ {\tau_ {k}} ^ {\theta , \mathrm{mask}} ] ^ {j} | X _ {\tau_ {k}} ^ {\theta , \mathrm{mask}} = \mathbf {x} , \tau_ {k + 1} = t)}{\mathbb {P} ([ X _ {\tau_ {k + 1}} ^ {\theta , \mathrm{mask}} ] ^ {j} \neq [ X _ {\tau_ {k}} ^ {\theta , \mathrm{mask}} ] ^ {j} | X _ {\tau_ {k}} ^ {\theta , \mathrm{mask}} = \mathbf {x} , \tau_ {k + 1} = t)} \\ = \frac {\sum_ {i = 1} ^ {L} \operatorname{Cat} (x ^ {i} ; \delta (\mathbf {m})}{\operatorname{Cat} (x ^ {j} ; \delta (\mathbf {m})} \sum_ {\mathbf {y} ^ {\prime} \in \mathcal {V} ^ {L}: [ y ^ {\prime} ] ^ {j} = y ^ {j} \neq x ^ {j}} \mathbb {P} (X _ {\tau_ {k + 1}} ^ {\theta , \mathrm{mask}} = \mathbf {y} ^ {\prime} | X _ {\tau_ {k}} ^ {\theta , \mathrm{mask}} = \mathbf {x}) \\ = \operatorname{Cat} (x ^ {j}; \delta (\mathbf {m})) \operatorname{Cat} (y ^ {j}; D _ {\theta} ^ {j} (\mathbf {x})) \\ = \operatorname{Cat} (y ^ {j}; D _ {\theta} ^ {j} (\mathbf {x})). \end{array}
$$

Defining for $\mathbf { x } \in \mathcal { V } ^ { L } , M ( \mathbf { x } ) : = \{ j \in \{ 1 , \dots , L \} : x ^ { j } = \mathbf { m } \}$ , the corresponding Gillespie sampling scheme Gillespie (1977; 1976) for a standard masked difusion model is thus as follows:

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 3 Gillespie Sampler for masked diffusion language models
1: Initialize: $x_0 \leftarrow (\mathbf{m}, \mathbf{m}, \ldots, \mathbf{m})$, denoiser $D_\theta$
2: for $t = 1 : L$ do
3: Choose Random Coordinate for Unmasking:
4: Sample dimension $i \sim \text{Unif } (M(x_t))$
5: Denoise:
6: Sample $z^i \sim D_\theta^i(x_t)$
7: $x_{t+1}^i \leftarrow z^i$
8: end for
9: return $x_L$
</div>

Letting $\mathbb { S } _ { L }$ be the set of all permutations of $\{ 1 , \ldots , L \}$ , we then have:

$$
\begin{array}{c} \mathbb {P} (X _ {1} ^ {\theta , \mathrm{mask}} = \mathbf {x}) = \frac {1}{L !} \sum_ {\sigma \in \mathbb {S} _ {L}} \prod_ {i = 1} ^ {L} \mathrm{Cat} (x ^ {\sigma (i)}; D _ {\theta} ^ {\sigma (i)} (\mathbf {x} ^ {- \sigma (\geq i), \mathbf {m}})) \\ = \mathbb {E} _ {\sigma \sim \mathrm{Unif} (\mathbb {S} _ {L})} \left[ \mathbb {P} (X _ {1} ^ {\theta , \mathrm{mask}} = \mathbf {x} | \sigma) \right] \end{array}
$$

where $\mathbf { x } ^ { - \sigma ( \geq i ) , \mathbf { m } } \in \mathcal { V } ^ { L }$ is x but with $x ^ { \sigma ( j ) } = { \bf m } , \forall j \ge i .$ . Here $\sigma ( i )$ represents the coordinate which is unmasked at time $\tau _ { i } .$ . From this it is clear that with each unmasking, $D _ { \theta }$ is gaining additional conditional information about the sequence it is denoising, and could potentially benefit from backtracking and remasking previously unmasked tokens.

Moreover, in Ou et al. (2024), it is proved that the loss that $D _ { \theta }$ is trained on (see Eq. 30 and $\operatorname { E q . 4 } )$ is equivalent to:

$$
\begin{array}{r l} & {\mathcal {L} _ {\mathrm{mask}} (\theta) = - \mathbb {E} _ {\mathbf {x} \sim \mathbf {p} _ {d a t a}} \left[ \mathbb {E} _ {\sigma \sim \mathrm{Unif} (\mathbb {S} _ {L})} \left[ \log \left(\mathbb {P} (X _ {1} ^ {\theta , \mathrm{mask}} = \mathbf {x} | \sigma)\right) \right] \right]} \\ & {\qquad = \mathbb {E} _ {\sigma \sim \mathrm{Unif} (\mathbb {S} _ {L})} \left[ D _ {K L} (\mathbf {p} _ {d a t a} | | \mathbb {P} (X _ {1} ^ {\theta , \mathrm{mask}} = \cdot | \sigma)) \right] + H (\mathbf {p} _ {d a t a}),} \end{array}
$$

where H is the Shannon Entropy of $\mathbf { p } _ { d a t a } .$ This is minimized with value $H ( \mathbf { p } _ { d a t a } )$ if and only if $\begin{array} { r } { \mathbb { P } ( X _ { 1 } ^ { \theta , \mathrm { m a s k } } = \cdot | \sigma ) = { \bf p } _ { d a t a } , \forall \sigma \in \mathbb { S } _ { L } ; } \end{array}$ that is, if every choice of unmasking order exactly recovers the data distribution.

It becomes clear that if the training objective used for a Masked Difusion Model was made uniformly 0, every choice of unmasking order would exactly recover the data distribution (the KL divergence is 0 if and only if the distributions are equal - see e.g. Budhiraja & Dupuis $( 2 0 1 9 )$ Lemma 2.1). In practice, however, $D _ { \theta }$ is far from perfect (and even if it were, it is trained using samples form $\mathbf { p } _ { d a t a } ,$ so would just recover those samples). As such, not all such orders will be created equal - that is there will be denoising orders $\sigma , \hat { \sigma } \in \mathbb S _ { L }$ such that

$$
D _ {K L} (\mathbf {p} _ {d a t a} | | \mathbb {P} (X _ {1} ^ {\theta , \mathrm{mask}} = \cdot | \sigma)) > > D _ {K L} (\mathbf {p} _ {d a t a} | | \mathbb {P} (X _ {1} ^ {\theta , \mathrm{mask}} = \cdot | \hat {\sigma})).
$$

This was observed empirically in Ou et al. (2024) Appendix J.4, Shih et al. (2022), and Li et al. (2021) Section 6.

## D.4 Comparison with Other Sampling Methods

Here we discuss how existing sampling methods fall under the P2 framework as outlined in Table 1.

Ancestral sampling disables the remasking by setting the Unmasked Planner $\left( G _ { U } \right)$ to always output 1, i.e., the probability that an unmask token should be kept is always 1, and the mask planner $G _ { M }$ functions as a uniform sampler as it randomly selects mask positions. Greedy ancestral sampling improves open this by using the denoiser $\mathrm { C a t } ( z ^ { j } ; D _ { \theta } ^ { j } ( { \bf x } ) )$ ) as the mask planner $G _ { M } ^ { j } ( { \bf z } , { \bf x } )$ . DFM sampling randomly selects positions, and enables remasking by introducing a tunable stochasticity strength η. RDM functions identically to our self-planning by using the denoiser for both mask and unmask planning but it omits the stochasticity control with the default stochasticity strength $\eta = 1$ DDPD introduces external planners and purely relies on the planner for both mask and unmask position planning with default stochasticity strength $\eta = 1$ . Crucially, it disallows for the possibility of mask-informed planning and the decomposition of $G _ { \phi }$ into $G _ { U }$ and $G _ { M }$ . As it is the most similar work to ours in the existing literature, here we provide a thorough comparison with DDPD Liu et al. (2024).

Given that our objective is to plan a denoising order assuming access to a Masked Difusion Model for our denoiser (as with DDPD-MaskD) and not to train a uniform difusion-based denoiser from scratch (as with DDPD-DFM-Uni), we focus on their framework in the former setting.

Even with DDPD-MaskD, the framework uses a “uniform discrete difusion” Eq. 27 as the starting-point for their token-wise forward noising process, as opposed to the “masked difusion” forward noising process Eq. 1 used in our work. They modify the state space $S ^ { L } = \{ 1 , \dots , d - 1 \} ^ { L }$ to $\tilde { S } ^ { L }$ , where $\tilde { S } = S \times \{ N , D \}$ . For $( \mathbf { y } , \mathbf { z } ) \in \tilde { S } ^ { L } , ( y ^ { i } , z ^ { i } )$ denotes the pair describing the state $y ^ { i } \in S$ in of i’th token and $z ^ { i } \in \{ N , D \}$ denotes whether that token is noise (N ) or data (D). They then modify the forward noising process to:

$$
p _ {t} ((j, \zeta) | i) = \alpha_ {t} \mathrm{Cat} ((j, \zeta); \delta (i, D)) + \frac {1 - \alpha_ {t}}{d - 1} \mathrm{Cat} (\zeta ; \delta (N)), \quad i, j \in S, \quad \zeta \in \{N, D \},
$$

see Equation (17) therein.

Thus, their reference distribution $\pi \in \Delta ^ { ( d + 1 ) ^ { L } }$ is given by $\pi = \operatorname { U n i f } ( S ^ { L } ) \otimes \delta _ { N ^ { L } }$ , where $N ^ { L } \in \{ N , D \} ^ { L }$ consists of all $N \mathrm { \bar { s } } .$ and the corresponding backwards processes’ $S ^ { L }$ marginal is initialized at the reference distribution $\mathrm { U n i f } ( S ^ { L } )$ as opposed to $[ \delta _ { \bf m } ] ^ { L }$ as in our setting.

They approximate a resulting true backward process on $S ^ { L } { } ^ { , } \mathrm { s }$ rate matrix $\mathsf { \Pi } _ { \boldsymbol { Q } _ { t } } ^ {  }$ (given by Proposition 3.1 therein) with $Q _ { t } ^ { \theta , \breve { \phi } , \mathrm { D D P D } }$ given by, for $\mathbf { x } \neq \mathbf { y } \colon$

$$
Q _ {t} ^ {\theta , \phi , \mathrm{DDPD}} (\mathbf {y}, \mathbf {x}) = \left\{ \begin{array}{l l} - \frac {\frac {d \alpha_ {1 - t}}{d t}}{1 - \alpha_ {1 - t}} \sum_ {i = 1} ^ {L} \Bigg \{\operatorname{Cat} (N; G _ {\phi , \mathrm{DDPD}} ^ {i} (\mathbf {x})) \\ \qquad \times \mathbb {E} _ {Z \sim G _ {\phi} (\mathbf {x})} [ \operatorname{Cat} (y ^ {i}; D _ {\theta} ^ {i} (\mathbf {x} ^ {Z, - i, \mathbf {m}}) ] \Bigg \} & , d _ {H A M} (\mathbf {x}, \mathbf {y}) = 1, x ^ {i} \neq y ^ {i} \\ 0 & , \text {otherwise} \end{array} \right.
$$

where $D _ { \theta } : \mathcal { V } ^ { L } \to ( \Delta ^ { d } ) ^ { L }$ is a denoiser for a masked difusion model trained via the ELBO Eq. 4. Here for $\mathbf { x } \in S ^ { L }$ $\mathbf { z } \in \{ N , D \} ^ { L } , \mathbf { x } ^ { \mathbf { z } , - i , \mathbf { m } } \in \mathcal { V } ^ { L }$ is obtained from x via:

$$
[ \mathbf {x} ^ {\mathbf {z}, - i, \mathbf {m}} ] ^ {j} = \left\{ \begin{array}{l l} \mathbf {m}, & z ^ {j} = N \\ x ^ {j}, & z ^ {j} = D, j \neq i \\ \mathbf {m}, & j = i \end{array} \right..
$$

$G _ { \phi , \mathrm { D D P D } } : S ^ { L } \to ( \Delta ^ { 2 } ) ^ { L }$ is another neural network with $\mathrm { C a t } ( N ; G _ { \phi , \mathrm { D D P D } } ^ { i } ( \mathbf { x } ) )$ approximating the probability that the i’th coordinate of $\mathbf { x } \in S ^ { L }$ is noise, and is trained via $\operatorname { E q } .$ . 30 with $\begin{array} { r } { \dot { E } ( \mathbf { x } _ { 0 } ) = E ^ { \mathrm { D D P D } } ( \mathbf { x } _ { 0 } ) } \end{array}$ given by:

$$
E ^ {\mathrm{DDPD}} (\mathbf {x} _ {0}) = E _ {P} ^ {\mathrm{DDPD}} (\mathbf {x} _ {0}) + E _ {D} ^ {\mathrm{DDPD}} (\mathbf {x} _ {0})
$$

$$
\begin{array}{l} E _ {P} ^ {\mathrm{DDPD}} (\mathbf {x} _ {0}) = - \int_ {0} ^ {1} \frac {\frac {d \alpha_ {t}}{d t}}{1 - \alpha_ {t}} \mathbb {E} _ {(\tilde {X} _ {t}, Z _ {t}) \sim P _ {t} ^ {\mathrm{DDPD}} (\cdot | \delta ((\mathbf {x} _ {0}, D ^ {L})))} \bigg [ \sum_ {i = 1} ^ {L} \log \operatorname{Cat} (Z _ {t} ^ {i}; G _ {\phi , \mathrm{DDPD}} ^ {i} (\tilde {X} _ {t}) \bigg ] d t \\ E _ {D} ^ {\mathrm{DDPD}} (\mathbf {x} _ {0}) = - \int_ {0} ^ {1} \frac {\frac {d \alpha_ {t}}{d t}}{1 - \alpha_ {t}} \mathbb {E} _ {(\tilde {X} _ {t}, Z _ {t}) \sim P _ {t} ^ {\mathrm{DDPD}} (\cdot | \delta ((\textbf {x} _ {0}, D ^ {L})))} \bigg [ \\ \sum_ {i = 1, Z _ {t} ^ {i} = N} ^ {L} \mathbb {E} _ {\hat {Z} \sim G _ {\phi , \mathrm{DDPD}} (\tilde {X} _ {t})} \left[ \log \operatorname{Cat} (\mathbf {x} _ {0} ^ {i}; D _ {\theta} ^ {i} (\tilde {X} _ {t} ^ {\hat {Z}, - i, \mathbf {m}})) \right] \bigg ] d t, \end{array}
$$

where for $\mathbf { y } \in S ^ { L } , \mathbf { z } \in \{ N , D \} ^ { L }$

$$
P _ {t} ((\mathbf {y}, \mathbf {z}) | \delta ((\mathbf {x} _ {0}, D ^ {L}))) := \alpha_ {t} \prod_ {i = 1} ^ {L} \mathrm{Cat} ((y ^ {i}, z ^ {i}); \delta ((x _ {0} ^ {i}, D))) + \frac {(1 - \alpha_ {t})}{(d - 1) ^ {L}} \prod_ {i = 1} ^ {L} \mathrm{Cat} (z ^ {i}; \delta (N)).
$$

Note that in the above ELBO, $E _ { D } ^ { \mathrm { { D D P D } } }$ is slightly modified from what which they present in Theorem 4.1. As written, they would take the expected value with respect to $G _ { \phi , \mathrm { D D P D } }$ inside the second log, which requires $2 ^ { L - 1 }$ function evaluations of $D _ { \theta }$ . When the denoiser $D _ { \theta }$ is given by that of a masked difusion, one should instead use the above, which can be readily arrived at the same proof with an extra application of Jensen’s inequality.

Comparing this with our Proposition Eq. 1, the comparison between DDPD and P2 becomes evident: $E _ { P } ^ { \mathrm { D D P D } } ( \mathbf { x } _ { 0 } )$ is playing the role of $E _ { U P } ( \mathbf { x } _ { 0 } ) + E _ { M P } ( \mathbf { x } _ { 0 } )$ (that is, it yields the training objective for the Planner) and $E _ { D } ^ { \mathrm { { \tiny { D D P D } } } } ( { \bf { x } } _ { 0 } ) ^ { ' }$ is playing the role of $E _ { D } ( \mathbf { x } _ { 0 } )$ (that is, it yields the training objective for the denoiser). However, we note the following key distinguishing factors:

1. In P2, $\mathcal { E } _ { D }$ is the same as the ELBO originally used to train the denoiser $D _ { \theta } \colon$ that is, $D _ { \theta }$ has already be trained to maximize $\mathbb { E } _ { x _ { 0 } \sim \mathbf { p } _ { \mathrm { d a t a } } } [ \mathcal { E } _ { D } ( \mathbf { x } _ { 0 } ) ]$ . Meanwhile, $E _ { D } ^ { \mathrm { { D D P D } } }$ depends on the output of $G _ { \phi }$ <sub>,DDPD</sub>, increasing the importance of the role of planner in the quality of the generations output. For this reason, DDPD must train an external Planner whose model size is comparable to that of the denoiser - they are essentially asking the planner to play a role akin to the denoiser in a uniform difusion model. Meanwhile, due to the “flipped” importance of the roles of the planner and denoiser in P2, we show that we can use lightweight BERT models or even the denoiser itself as an efective Planner. See Table S5, where we confirm DDPD’s inability to make use of such lightweight models.

2. In P2, we separate the Planner’s training objective into two components. This is natural because our planner may use information both from the partially masked data $X _ { t }$ and the output of the denoiser. Meanwhile, in DDPD, the Planner only has access to $\tilde { X } _ { t }$ -unmasked data perturbed by random flips of its tokens. Because DDPD’s generation process is grounded in a uniform difusion process, there is no ability to separate the Planner into unmasked and masked components as we do in Section $\operatorname { E q . }$ 3.2. In particular, their framework does not allow for a general enough planner to introduce our stochasticity strength parameter η and design an algorithm analogous to the P2 Sampler Algorithm 1.

The practical diferences between DDPD and P2 are further elucidated by comparing their Gillespie sampling strategy (Algorithm 1 therein) with ours (see Algorithm 5). For convenience, we reproduce it here.

Letting $\hat { G } _ { \phi , \mathrm { D D P D } } : S ^ { L } \to \Delta ^ { L }$ be given by $\hat { G } _ { \phi , \mathrm { D D P D } } ^ { j } ( \mathbf { x } ) = \frac { \mathrm { C a t } ( N ; G _ { \phi , \mathrm { D D P D } } ^ { j } ( \mathbf { x } ) ) } { \sum _ { j = 1 } ^ { L } \mathrm { C a t } ( N ; G _ { \phi , \mathrm { D D P D } } ^ { j } ( \mathbf { x } ) ) }$ , DDPD’s Gillespie sampling algorithm is given by Algorithm 4.

As is clear from Algorithm 4, in DDPD, the input to the Planner only depends on some unmasked, randomly flipped sequence of tokens, and does not depend on the output of the denoiser, and the input to the denoiser is entirely dependent on the output of the planner. Meanwhile, in P2, the Planner may use the both the information about the partially unmasked sequence (whose unmasked tokens all result from samples from the denoiser) and the output of the denoiser, and the input to the denoiser only depends on the output of the planner insofar as it may choose to remask a single token. We note that dificulty of the precise task performed by DDPD’s planner was recently shown to be the reason for MDMs performance over uniform difusion models in Amin et al. (2025). In Proposition 5.1 they essentially show that if one conditions on whether each position in a sequence of unmasked tokens is clean or noise, uniform difusion models reverse to masked difusion. So the ability of the model to make this distinction is the bottleneck preventing uniform difusion models from performing comparably to MDMs, and likely the same reason for P2-BERT, P2-train, and P2-self’s superior performance to DDPD as evidenced in Table S5. For ease of comparison, we derive the corresponding Gillespie sampling scheme for P2 in the forthcoming §D.5.

```csv
Algorithm 4 DDPD Sampler
1: init i ← 0, x₀ ~ Unif(S^L), planner G_φ,DDPD, denoiser D_θ, maximum steps T
2: for t = 1 : T do
3: Plan Sample dimension i ~ G_φ,DDPD(x_t)
4: Denoise Sample z ~ G_φ,DDPD
5: Sample y^i ~ D^i_θ(x^z,-i,m)
6: Update: x^i_{t+1} ← y^i
7: end for
8: return x_T
```

## D.5 Deriving the P2 Gillespie Scheme Algorithm 5

Here, for ease of comparison with the works discussed in Subsection D.4 and to motivate the connection between the sampling scheme described in Eq. 5 and the practical top-k sampling scheme Alg. 1, we derive the Gillespie sampler for the continuous time limit of P2.

Let $\{ \tau _ { k } \} _ { k \in \mathbb { N } }$ be the jump times for the CTMC $X ^ { \theta , \phi }$ with rate matrix $Q ^ { \theta , \phi }$ as described in Equation $\operatorname { E q } .$ . 32 (see Section C.2). To derive a Gillespie sampling scheme, we need to find the transition probabilities for the efective jump chain as described in Eq. 25. We first need to obtain the diagonal entries for the jump matrix $Q ^ { \theta , \phi }$ . We have for $\mathbf { x } \in \mathcal { V } ^ { L }$ :

$$
\begin{array}{r l} & {- \sum_ {\mathbf {y} \neq \mathbf {x}} Q _ {t} ^ {\theta , \phi} (\mathbf {y}, \mathbf {x})} \\ & {= \frac {\frac {d \alpha_ {1 - t}}{d t}}{1 - \alpha_ {1 - t}} \sum_ {i = 1} ^ {L} \sum_ {y ^ {i} = 1, y ^ {i} \neq x ^ {i}} ^ {d - 1} F _ {\theta , \phi} ^ {i} (\mathbf {x} ^ {- i, y ^ {i}}, \mathbf {x}) \mathrm{Cat} (y ^ {i}; \hat {D} _ {\theta} ^ {i} (\mathbf {x}))} \\ & {= \frac {\frac {d \alpha_ {1 - t}}{d t}}{1 - \alpha_ {1 - t}} \sum_ {i = 1} ^ {L} \bigg [ \mathrm{Cat} (x ^ {i}; \delta (\mathbf {m})) \sum_ {y ^ {i} = 1, y ^ {i} \neq x ^ {i}} ^ {d - 1} \mathbb {E} _ {Z \sim D _ {\theta} (\mathbf {x})} [ G _ {\phi} ^ {i} (Z ^ {- i, y ^ {i}}) ] \mathrm{Cat} (y ^ {i}; D _ {\theta} ^ {i} (\mathbf {x}))} \\ & {\quad + \frac {(1 - \mathrm{Cat} (x ^ {i} ; \delta (\mathbf {m})))}{1 - \mathrm{Cat} (x ^ {i} ; D _ {\theta} ^ {i} (\mathbf {x} ^ {- i , \mathbf {m}}))} \sum_ {y ^ {i} = 1, y ^ {i} \neq x ^ {i}} ^ {d - 1} \mathbb {E} _ {Z \sim D _ {\theta} (\mathbf {x})} [ G _ {\phi} ^ {i} (Z, x) ] \mathrm{Cat} (y ^ {i}; D _ {\theta} ^ {i} (\mathbf {x} ^ {- i, \mathbf {m}})) \bigg ]} \\ & {= \frac {\frac {d \alpha_ {1 - t}}{d t}}{1 - \alpha_ {1 - t}} \sum_ {i = 1} ^ {L} \bigg \{\mathrm{Cat} (x ^ {i}; \delta (\mathbf {m})) \mathbb {E} _ {Z \sim D _ {\theta} (\mathbf {x})} [ G _ {\phi} ^ {i} (Z, \mathbf {x}) ] + (1 - \mathrm{Cat} (x ^ {i}; \delta (\mathbf {m}))) \mathbb {E} _ {Z \sim D _ {\theta} (\mathbf {x})} [ G _ {\phi} ^ {i} (Z, \mathbf {x}) ] \bigg \}} \\ & {= \frac {\frac {d \alpha_ {1 - t}}{d t}}{1 - \alpha_ {1 - t}} \sum_ {i = 1} ^ {L} \mathbb {E} _ {Z \sim D _ {\theta} (\mathbf {x})} [ G _ {\phi} ^ {i} (Z, \mathbf {x}) ]} \\ & {= Q _ {t} ^ {\theta , \phi} (\mathbf {x}, \mathbf {x}).} \end{array}
$$

Then for $\mathbf { x } \neq \mathbf { y } \in \mathcal { V } ^ { L } , k \in \mathbb { N } ,$ and $t \in [ 0 , 1 ]$ :

$$
\mathbb {P} (X _ {\tau_ {k + 1}} ^ {\theta , \phi} = \mathbf {y} | X _ {\tau_ {k}} ^ {\theta , \phi} = \mathbf {x}, \tau_ {k + 1} = t) = \frac {F _ {\theta , \phi} ^ {i} (\mathbf {y} , \mathbf {x}) \mathrm{Cat} (y ^ {i} ; \hat {D} _ {\theta} ^ {i} (\mathbf {x})}{\sum_ {i = 1} ^ {L} \mathbb {E} _ {Z \sim D _ {\theta} (\mathbf {x})} [ G _ {\phi} ^ {i} (Z , x) ]},
$$

when $d _ { H A M } ( \mathbf { x } , \mathbf { y } ) = 1$ and $x ^ { i } \neq y ^ { i }$ and 0 when the Hamming distance $d _ { H A M } ( \mathbf { x } , \mathbf { y } ) \neq 1$ . We note that this is and independent of t and k.

Then, for $j \in [ L ] = \{ 1 , \dots , L \}$ and $\mathbf { x } , \mathbf { y } , k , t$ as before:

$$
\begin{array}{l} \mathbb {P} ([ X _ {\tau_ {k + 1}} ^ {\theta , \phi} ] ^ {j} \neq [ X _ {\tau_ {k}} ^ {\theta , \phi} ] ^ {j} | X _ {\tau_ {k}} ^ {\theta , \phi} = \mathbf {x}, \tau_ {k + 1} = t) \\ = \sum_ {\mathbf {y} \in \mathcal {V} ^ {L}: y ^ {j} \neq x ^ {j}} \mathbb {P} (X _ {\tau_ {k + 1}} ^ {\theta , \phi} = \mathbf {y} | X _ {\tau_ {k}} ^ {\theta , \phi} = \mathbf {x}) \\ = \sum_ {y ^ {j} = 1, y ^ {j} \neq x ^ {j}} ^ {d - 1} F _ {\theta , \phi} ^ {j} (\mathbf {x} ^ {- j, y ^ {j}}, \mathbf {x}) \mathrm{Cat} (y ^ {j}; \hat {D} _ {\theta} ^ {j} (\mathbf {x})) / \biggl (\sum_ {i = 1} ^ {L} \mathbb {E} _ {Z \sim D _ {\theta} (\mathbf {x})} [ G _ {\phi} ^ {i} (Z, x) ] \biggr) \\ = \frac {\mathbb {E} _ {Z \sim D _ {\theta} (\mathbf {x})} [ G _ {\phi} ^ {j} (Z , \mathbf {x}) ]}{\sum_ {i = 1} ^ {L} \mathbb {E} _ {Z \sim D _ {\theta} (\mathbf {x})} [ G _ {\phi} ^ {i} (Z , \mathbf {x}) ]} \\ =: P (j, \mathbf {x}) \end{array}
$$

and for $y ^ { j } \in \mathcal { V }$ with $y ^ { j } \neq x ^ { j } ;$

$$
\begin{array}{l} \mathbb {P} ([ X _ {\tau_ {k + 1}} ^ {\theta , \phi} ] ^ {j} = y ^ {j} | X _ {\tau_ {k}} ^ {\theta , \phi} = \mathbf {x}, \tau_ {k + 1} = t, [ X _ {\tau_ {k + 1}} ^ {\theta , \phi} ] ^ {j} \neq [ X _ {\tau_ {k}} ^ {\theta , \phi} ] ^ {j}) \\ = \frac {\mathbb {P} ([ X _ {\tau_ {k + 1}} ^ {\theta , \phi} ] ^ {j} = y ^ {j} , [ X _ {\tau_ {k + 1}} ^ {\theta , \phi} ] ^ {j} \neq [ X _ {\tau_ {k}} ^ {\theta , \phi} ] ^ {j} | X _ {\tau_ {k}} ^ {\theta , \phi} = \mathbf {x} , \tau_ {k + 1} = t)}{\mathbb {P} ([ X _ {\tau_ {k + 1}} ^ {\theta , \phi} ] ^ {j} \neq [ X _ {\tau_ {k}} ^ {\theta , \phi} ] ^ {j} | X _ {\tau_ {k}} ^ {\theta , \phi} = \mathbf {x} , \tau_ {k + 1} = t)} \\ = \sum_ {\boldsymbol {y} ^ {\prime} \in \mathcal {V} ^ {L}: [ y ^ {\prime} ] ^ {j} = y ^ {j} \neq x ^ {j}} \frac {\mathbb {P} (X _ {\tau_ {k + 1}} ^ {\theta , \phi} = \boldsymbol {y} ^ {\prime} | X _ {\tau_ {k}} ^ {\theta , \phi} = \mathbf {x})}{\mathbb {P} ([ X _ {\tau_ {k + 1}} ^ {\theta , \phi} ] ^ {j} \neq [ X _ {\tau_ {k}} ^ {\theta , \phi} ] ^ {j} | X _ {\tau_ {k}} ^ {\theta , \phi} = \mathbf {x} , \tau_ {k + 1} = t)} \\ = \frac {F _ {\theta , \phi} ^ {j} (\mathbf {x} ^ {- j , y ^ {j}} , \mathbf {x}) \mathrm{Cat} (y ^ {j} ; \hat {D} _ {\theta} ^ {j} (\mathbf {x})}{\mathbb {E} _ {Z \sim D _ {\theta} (\mathbf {x})} [ G _ {\phi} ^ {j} (Z , x) ]} \\ = \left(\mathrm{Cat} (x ^ {j}; \delta (\mathbf {m})) \mathbb {E} _ {Z \sim D _ {\theta} (\mathbf {x})} [ G _ {\phi} ^ {j} (Z ^ {- j, y ^ {j}}, x) ] \mathrm{Cat} (y ^ {j}; D _ {\theta} ^ {j} (\mathbf {x})) + (1 - \mathrm{Cat} (x ^ {j}; \delta (\mathbf {m}))) \mathbb {E} _ {Z \sim D _ {\theta} (\mathbf {x})} [ G _ {\phi} ^ {j} (Z, x) ] \frac {\mathrm{Cat} (y ^ {j} ; D _ {\theta} ^ {j} (\mathbf {x} ^ {- i , \mathbf {m}}))}{1 - \mathrm{Cat} (x ^ {j} ; D _ {\theta} ^ {j} (\mathbf {x} ^ {- j , \mathbf {m}}))}\right) \\ / \mathbb {E} _ {Z \sim D _ {\theta} (\mathbf {x})} [ G _ {\phi} ^ {j} (Z, x) ] \\ = \mathrm{Cat} (x ^ {j}; \delta (\mathbf {m})) \frac {\mathbb {E} _ {Z \sim D _ {\theta} (\mathbf {x})} [ G _ {\phi} ^ {j} (Z ^ {- j , y ^ {j}} , x) ]}{\mathbb {E} _ {Z \sim D _ {\theta} (\mathbf {x})} [ G _ {\phi} ^ {j} (Z , x) ]} \mathrm{Cat} (y ^ {j}; D _ {\theta} ^ {j} (\mathbf {x})) \\ + (1 - \mathrm{Cat} (x ^ {j}; \delta (\mathbf {m}))) \frac {\mathrm{Cat} (y ^ {j} ; D _ {\theta} ^ {j} (\mathbf {x} ^ {- j , \mathbf {m}}))}{1 - \mathrm{Cat} (x ^ {j} ; D _ {\theta} ^ {j} (\mathbf {x} ^ {- j , \mathbf {m}})} \\ =: \tilde {P} (j, x, y ^ {j}). \end{array}
$$

Thus, an exact Gillespie sampling scheme would be given by Gillespie (1977; 1976):

When the chain is in state $x \in \mathcal { V } ^ { L }$ , sample a dimension $i \sim \hat { P } ( \cdot , x )$ to change, then sample a value $y ^ { j } \sim { \tilde { P } } ( i , x , \cdot )$ to change it to.

In practice it is impractical to approximate these expected values with respect to $Z \sim D _ { \theta } ( \mathbf { x } )$ , as this would require many function evaluations of the denoiser. However, assuming that the token space is large, conditioning on the value of one coordinate should have little impact on the expected output of the Planner over the entire sequence (see e.g. the discussion under Proposition 3.5. and Appendix E.4 in Liu et al. (2024)). Given that Algorithm 5 is provided for the purpose of exposition and in practice we make use of Algorithm 1 in sampling, we use this intuition to formally approximate:

$$
\tilde {P} (j, \mathbf {x}, y ^ {j}) \approx \operatorname{Cat} (x ^ {j}; \delta (\mathbf {m})) \operatorname{Cat} (y ^ {j}; D _ {\theta} ^ {j} (\mathbf {x}) + (1 - \operatorname{Cat} (x ^ {j}; \delta (\mathbf {m}))) \frac {\operatorname{Cat} (y ^ {j} ; D _ {\theta} ^ {j} (\mathbf {x} ^ {- j , \mathbf {m}})}{1 - \operatorname{Cat} (x ^ {j} ; D _ {\theta} ^ {j} (\mathbf {x} ^ {- j , \mathbf {m}})}
$$

and

$$
P (j, \mathbf {x}) \approx \frac {\mathbb {E} _ {Z \sim D _ {\theta} (\mathbf {x})} [ G _ {\phi} ^ {j} (Z , \mathbf {x}) ]}{\sum_ {i = 1} ^ {L} \mathbb {E} _ {Z \sim D _ {\theta} (\mathbf {x})} [ G _ {\phi} ^ {i} (Z , \mathbf {x}) ]} \approx \mathbb {E} _ {Z \sim D _ {\theta} (\mathbf {x})} [ \hat {G} ^ {j} (Z, \mathbf {x}) ],
$$

where : $\hat { G } _ { \phi } : \mathcal { V } ^ { L } \times \mathcal { V } ^ { L } \to \Delta ^ { L }$ is given by:

$$
\hat {G} _ {\phi} ^ {j} (\mathbf {z}, \mathbf {x}) := \frac {G _ {\phi} ^ {j} (\mathbf {z} , \mathbf {x})}{\sum_ {j = 1} ^ {L} G _ {\phi} ^ {j} (\mathbf {z} , \mathbf {x})}.
$$

We then arrive at Algorithm 5.

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 5 Our Gillespie Sampler
1: Initialize:  $t \leftarrow 0, x_{0} \leftarrow (m, \ldots, m)$ , planner  $G_{\phi}$ , denoiser  $D_{\theta}$ , maximum steps T
2: for t = 1 : T do
3: Plan Sample  $z \sim D_{\theta}(x_{t})$ 
4: Sample dimension  $i \sim \hat{G}_{\phi}(z, x_{t})$ 
5: Denoise
6: if  $x_{t}^{i} \neq m$  then
7:  $x_{t}^{i} \leftarrow m$ 
8: Resample  $z^{i} \sim D_{\theta}^{i}(x_{t})$ 
9:  $x_{t+1}^{i} \leftarrow z^{i}$ 
10: else
11:  $x_{t+1}^{i} \leftarrow z^{i}$ 
12: end if
13: end for
14: return  $x_{T}$
</div>

Observe that Algorithm 1 is simply the result of modifying Algorithm 5 so that $\hat { G }$ is replaced by ${ \tilde { G } } _ { \eta }$ (allowing for $\eta \neq 1 )$ , dropping the requirement that a token is denoised immediately after remasking, and replacing faithful sampling from ${ \tilde { G } } _ { \eta }$ with top-k sampling.

## E Implementation Details

In Listing 1, we provide a self-contained PyTorch implementation of our Path-Planning Sampling procedure. The code consists of three core components, each addressing a distinct step in the sampling process:

1) topk\_lowest\_masking: Given a matrix of scalar scores, this function returns a boolean mask that flags the “lowest-scoring” positions per row. The user can specify how many positions should be re-masked by providing a cutoff\_len tensor. Internally, the function sorts the score matrix and determines the threshold score for each row before comparing every score to this cutof.

2) stochastic\_sample\_from\_categorical: This function draws samples from a categorical distribution using Gumbel noise. It first applies Gumbel noise to the input logits (if a non-zero temperature is specified), then computes the log-softmax to obtain token probabilities. The sampled tokens and their corresponding log probabilities are returned.

3) path\_planning\_sampling: Positions initially set to the mask\_token\_id are iteratively predicted and updated. At each iteration, we:

1. Compute model logits and identify positions that remain masked.

2. Sample from the model outputs via stochastic\_sample\_from\_categorical.

```python
import torch

def topk_lowest_masking(scores, cutoff_len):
    sorted_scores, _ = scores.sort(dim=-1)
    threshold = sorted_scores.gather(dim=-1, index=cutoff_len)
    return scores < threshold

def stochastic_sample_from_categorical(logits, temperature=1.0, noise_scale=1.0):
    logits = logits.double()
    if temperature != 0.0:
    gumbel = -torch.log(-torch.log(torch.rand_like(logits) + 1e-8) + 1e-8)
    logits = logits / temperature + noise_scale * gumbel
    scores, tokens = logits.log_softmax(dim=-1).max(dim=-1)
    return tokens, scores

@torch.inference_mode()
@torch.cuda.amp.autocast()

def path_planning_sampling(
    xt,
    model,
    tokenizer,
    num_steps,
    tau=1.0,
    kappa_fn=lambda t: t,
    eta=1.0,
    planner=None,
    score_type='confidence'
```

3. Integrate a planner (if provided) to re-score predictions for currently unmasked positions, giving users the flexibility to incorporate any additional guidance or constraints.

4. Construct a score and re-mask positions with the lowest scores. Fixed positions are ignored by assigning them infinite scores so that they cannot be re-masked.

5. Scale the scores of unmasked positions by the factor η, which adjusts how aggressively new tokens are updated.

The function continues for num\_steps, revealing high-confidence predictions and re-masking uncertain positions. Finally, any remaining masks are replaced with the last sampled tokens. The key parameters are:

• xt: The initial token matrix of shape [B, L], containing masked tokens.

• model: A callable mapping tokens to logits.

• tokenizer: Provides the special mask\_token\_id.

• num\_steps: Number of refinement iterations.

• tau: Temperature for controlling sampling noise.

• kappa\_fn: A schedule function in [0, 1] that dictates how many positions remain masked vs. unmasked over time.

• eta: A multiplier for scores in unmasked positions.

• planner: An optional model for additional re-scoring.

• score\_type: Either ’confidence’ (uses log probabilities) or ’random’ (random re-masking).

## Listing 1: Path-Planning Sampling procedure in PyTorch

```python
):
    fix_mask = (xt != tokenizer.mask_token_id)
    dt = 1.0 / num_steps

    for step in range(1, num_steps + 1):
    t = step * dt
    kappa_t = kappa_fn(t)
    logits = model(xt).double()

    last_mask = (xt == tokenizer.mask_token_id)
    unmask_candidates = ~last_mask & ~fix_mask

    x0, logp = stochastic_sample_from_categorical(logits, temperature=tau)

    if planner is not None:
    planner_logits = planner(x0).double()
    planner_logp = planner_logits.log_softmax(dim=-1).gather(-1, x0.unsqueeze(-1)).squeeze(-1)
    logits[unmask_candidates] = planner_logits[unmask_candidates]
    logp[unmask_candidates] = planner_logp[unmask_candidates]

    if score_type == 'confidence':
    score = logp
    elif score_type == 'random':
    score = torch.rand_like(logp).log()
    else:
    raise ValueError("Invalid score_type.")

    score = score.masked_fill(fix_mask, float('inf'))
    score[unmask_candidates] *= eta

    num_to_mask = ((~fix_mask).sum(dim=1, keepdim=True).float() * (1 - kappa_t)).long()
    mask = topk_lowest_masking(score, num_to_mask)
    xt[mask] = tokenizer.mask_token_id

    mask_to_x0 = last_mask & ~mask
    xt[mask_to_x0] = x0[mask_to_x0]

    remaining_mask = (xt == tokenizer.mask_token_id)
    xt[remaining_mask] = x0[remaining_mask]

    return xt
```

## F Experimental Details

## F.1 Protein Generation Evaluation Details

Setup We compare our method with state-of-the-art protein sequence generation models, including three discrete difusion models—DPLM (Wang et al., 2024), EvoDif (Alamdari et al., 2024), and ESM3 (Hayes et al., 2025)—and an autoregressive model, ProGen2 (Nijkamp et al., 2022), across three model sizes: small, medium, and large. Additionally, we benchmark masked language models, ESM2 (Lin et al., 2023), at three scales: 150M, 650M, and 3B parameters.

For our path-planning algorithm (P2), we vary the stochasticity strength from 1.0 to 2.0 in increments of 0.1 and report optimal results. Baselines are evaluated with default sampling strategies. Since ESM2 lacks a masked difusion loss, it uses ancestral sampling. Each model generates 100 sequences for sequence lengths in [200, 300, . . . , 800]. DPLM employs a sequence length matching the number of sampling steps and a temperature of 0.9, with rejection-resampling disabled for fairness. ESM3 is sampled with a temperature of 1, a cosine schedule, top-p = 1, and 500 steps. Special tokens are removed to ensure valid amino acid sequences.

Evaluation. Protein sequence generation quality is evaluated via protein folding models, using ESMFold (Lin et al., 2023) as a proxy for structural stability. We extract three folding metrics:

• pLDDT (predicted Local Distance Diference Test): Measures local structural accuracy.

• pTM (predicted Template Modeling): Assesses global structural plausibility.

• pAE (predicted Alignment Error): Evaluates overall compactness.

A sequence can achieve high pLDDT while exhibiting poor global compactness (high pAE). To ensure robust evaluation, we define foldability as the proportion of sequences satisfying pLDDT > 80, pTM > 0.7, and $\mathrm { p A E } < 1 0$ . This metric efectively identifies low-quality sequences, such as repetitive patterns (e.g., “ABABABAB”), which tend to have high pAE.

Beyond folding scores, we compute:

• Token entropy, excluding tokens not present in generated sequences.

• Sequence diversity, defined as 1− pairwise sequence identity within a batch. Since all sequences in a batch share equal length, no sequence alignment is needed.

These metrics detect mode collapse, where models generate highly repetitive sequences.

## F.1.1 Training Details of the 150M MDM.

We train a 150M mask difusion model on protein sequences for the ablation of self-planning. The 150M MDM is trained using the open-sourced DPLM code<sup>4</sup>. We use the same transformer architecture as DPLM-150M as well as ESM2-150M. We train our MDM from scratch for 500k steps with a total of 320K tokens in each iteration, which is achieved by multi-GPU and multi-node training with gradient accumulation. The training data is Uniref50, consisting of around 40M protein sequences with 50% sequence-identity cutof, namely, the sequences in uniref50 are at least higher than 50% dissimilar. Uniref50 is widely used for training protein language models.

## F.1.2 Training Details for P2 Train

For results on P2 train, we fine-tune $T _ { \phi } ^ { i } ( \mathbf { z } , \mathbf { x } )$ where $T _ { \phi } ^ { i } ( { \bf z } , { \bf x } ) = \mathrm { C a t } ( z ^ { i } ; B ^ { i } ( { \bf z } ) )$ for B given by ESM-8M for 100k steps using $G _ { U } = G _ { M } = T _ { \phi }$ in Alg. 2 with the same data and hyperparameter setup as for the 150M MDM. During sampling for P2 train, we take $G _ { U } ^ { i } ( { \bf z } , { \bf x } ) = T _ { \phi } ^ { i } ( { \bf z } , { \bf x } )$ and $G _ { M } ^ { i } ( { \bf { z } } , { \bf { x } } ) = \mathrm { { C a t } } ( z ^ { i } ; D _ { \theta } ^ { i } ( { \bf { x } } ) )$ in Alg. 1.

## F.1.3 Computing the ELBO

The Evidence Lower Bound (ELBO) serves as the training objective of mask difusion models and can be used to assess how well the model fits the data. The ELBO experiments are conducted on protein sequence generation tasks. We compute the negative ELBO for five planners, namely ESM-8M, ESM-35M, ESM-150M, ESM-650M, and ESM-3B, alongside the self-planning ELBO, using a weighted cross-entropy loss function to quantify reconstruction accuracy.

Dataset Preparation. We utilize sequences from the UniRef50 dataset, filtering to include only test sequences with lengths shorter than 300 residues to align with the experiments in Figure S3 and mitigate memory constraints. The dataset is loaded into a PyTorch DataLoader using a sequence length of 1022 tokens and a maximum token budget of 60,000. For consistent evaluation, we run the ELBO calculation over 20 independent simulations and report the average across these runs.

Masking Strategy. For each sequence, we randomly generate a mask ratio uniformly sampled from the range [1/500, 1 − 1/500]. Positions are masked based on this ratio, but masking is constrained to avoid altering non-maskable tokens (e.g., special symbols). The masked tokens are replaced with a designated mask token provided by the denoiser model.

Loss Calculation. To compute the ELBO, the denoiser and planner models predict the original tokens for both masked and unmasked positions. The cross-entropy loss is calculated separately for these categories. Both masked and unmasked loss values are weighted inversely by the mask ratio to ensure probabilistic consistency in the evaluation. Each model is evaluated across 20 independent simulations, and the average ELBO is reported to capture the robustness of the planners under stochastic settings.

## F.2 Language Generation Evaluation Details

Tasks and Metrics.

• TriviaQA (Joshi et al., 2017): reading comprehension (exact match).

• LAMBADA (Paperno et al., 2016): last-token prediction (accuracy).

• GSM8K (Cobbe et al., 2021): math reasoning (accuracy).

• ROCStories (Mostafazadeh et al., 2016): story infilling, evaluated by ROUGE-1/2/L (Lin, 2004).

• HumanEval (Bavarian et al., 2022): code completion, measured by pass@1.

Example of Language generation Task We provide Table S1 consisting of examples for the five language generation tasks.

Setup. We follow SMDM (Gong et al., 2025) and DifuLLaMA (Nie et al., 2025) protocols. MDM (1.1B) and DifuLLaMA (7B) are used as base models. We apply P2 with η ∈ [0, 2.0] and report best-performing settings. Decoding follows standard ancestral sampling unless otherwise noted. For AR baselines lacking native infilling support, we use oracle length truncation. Evaluation is done using the LM Harness (Biderman et al., 2024).

Baselines. We report published results from GPT2-S/M, DifuGPT, SEDD (Lou et al., 2023), Plaid1B (Gulrajani & Hashimoto, 2023), and LLaMA2 (Touvron et al., 2023). TinyLlama is also included as an open-source AR baseline.

Implementation Notes. For P2, stochasticity is critical to quality. For each model-task pair, we tune η using a grid sweep and hold evaluation set fixed. We do not use instruction tuning or CoT prompting.

## F.3 RNA Generation Details

## F.4 RNA Evaluation Details

Training. We train a 150M-parameter MDM on 27M RNA sequences from RNACentral (Petrov, 2021) using a batch size of 320K tokens for 100K steps. The tokenizer and vocabulary follow RiNALMo (Penić et al., 2024).

Evaluation. We generate 100 RNA sequences of 100 base pairs. Predicted structures are obtained using the RNA folding model from Shen et al. (2024). Evaluation metrics include:

• pLDDT (↑): predicted local structure confidence.

• MFE (↓): minimum free energy of folded structure.

• Entropy (↑): mean token entropy across positions.

• GC Content (↑): proportion of guanine-cytosine nucleotides.

Table S1: Examples from language understanding benchmarks.

<table><tr><td>Metric</td><td>Question</td><td>Answer</td></tr><tr><td>LAMBADA</td><td>&quot;Again, he left that up to you. However, he was adamant in his desire that it remain a private ceremony. He asked me to make sure, for instance, that no information be given to the newspaper regarding his death, not even an obituary. I got the sense that he didn&#x27;t want anyone, aside from the three of us, to know that he&#x27;d even _. &quot;</td><td>died</td></tr><tr><td>GSM8K</td><td>Weng earns $12 an hour for babysitting. Yesterday, she just did 50 minutes of babysitting. How much did she earn?</td><td>10</td></tr><tr><td>TriQA</td><td>The Dodecanese Campaign of WWII that was an attempt by the Allied forces to capture islands in the Aegean Sea was the inspiration for which acclaimed 1961 commando film?</td><td>The Guns of Navarone</td></tr><tr><td>ROCStories</td><td>Morgan and her family lived in Florida. They heard a hurricane was coming. (Story infills here...) They arrived and learned from the news that it was a terrible storm. They felt lucky they had evacuated when they did.</td><td>They decided to evacuate to a relative&#x27;s house.</td></tr><tr><td>Code</td><td></td><td></td></tr></table>

Baselines. We compare against RiNALMo-150M and RiNALMo-650M (Penić et al., 2024), two masked language models pretrained on RNA. We also include a reference set of 100 natural RNA sequences of matching length. For P2, we use BERT-Planning derived from RiNALMo-150M, sweeping η ∈ [0, 2] with step size 0.02 and reporting the best-performing configuration.

Findings. P2 improves MDM’s structural quality beyond native baselines and pretrained models, while keeping sequence diversity nearly unchanged. Structure visualizations are provided in Section G.3.2.

RNA MDM Training Implementation. The RNA MDM follows the same discrete difusion described in (Zheng et al., 2023). The MDM was trained using a machine mounted with 4 A100 GPUs, each with 40GB memory. The training implementation is otherwise identical to the second-stage fine-tuning described in (Wang et al., 2024), where we continued from a RiNALMo (Penić et al., 2024) checkpoint instead of ESM-2 (Lin et al., 2023).

Table S2: Results on breaking the reverse curse: Performance comparison of models on DescriptionToName and NameToDescription tasks. Metrics include accuracy (Acc.) and BLEU scores (BLEU) for both same and reverse directions.

<table><tr><td rowspan="2"></td><td colspan="3">DescriptionToName</td><td colspan="3">NameToDescription</td></tr><tr><td>Same direction Acc. ↑</td><td>Reverse direction Acc. ↑</td><td>Same direction Acc. ↑</td><td>BLEU ↑ BLEU ↑</td><td>Reverse direction Acc. ↑</td><td>BLEU ↑ BLEU ↑</td></tr><tr><td>GPT3 (175B)</td><td>97</td><td>0</td><td>50</td><td>-</td><td>0</td><td>-</td></tr><tr><td>Llama-2 (13B)</td><td>99</td><td>0</td><td>-</td><td>74</td><td>-</td><td>19</td></tr><tr><td>T5 (3B)</td><td>100</td><td>0</td><td>47</td><td>87</td><td>0</td><td>20</td></tr><tr><td>MDM (1.1B)</td><td>97</td><td>92</td><td>49</td><td>76</td><td>37</td><td>67</td></tr><tr><td>MDM (1.1B) + Path Planning (P2)</td><td>96</td><td>93</td><td>48</td><td>78</td><td>36</td><td>68</td></tr></table>

## G Additional Results

## G.1 Language Generation

## G.1.1 Breaking the Reverse Curse

Benchmark. Berglund et al. (2023) introduced the concept of the reverse curse, which refers to the dificulty of ARMs in generalizing bidirectional relationships. Specifically, this occurs when a model is trained on information in the form “A is B” but fails to infer the reverse relationship “B is A.” For example, a model trained on the fact “Valentina Tereshkova was the first woman to travel to space” may not correctly answer the reverse question “Who was the first woman to travel to space?” This limitation raises concerns about whether large language models genuinely possess logical reasoning capabilities.

Baselines. We compare with the leading AR models including GPT3 (175B), Llama-2 (13B), and the T5 consisting of both bidirectional encoder and unidirectional decoder, finetuned on the reverse curse dataset. For the MDM baseline, We use the existing MDM (1.1B) from Gong et al. (2025) with its default greedy ancestral sampling strategy.

Setup. It is observed in SMDM (Gong et al., 2025) that MDMs easily break the reverse curse, displaying near-perfect reverse accuracy where ARs achieve 0 accuracy. We follow SMDM and evaluate MDMs on the same reverse curse dataset used by Berglund et al. (2023), which consists of fictitious statements in the format “〈name〉 is 〈description〉” and the reversals. We use the pretrained MDMs and baseline results from SMDM which on these statements and assess their performance using questions not seen during training. Following the same protocol as (Berglund et al., 2023), we generate responses and report the exact match accuracy and use the BLEU metric (Papineni et al., 2002) to evaluate the quality of name-to-description generation (Lv et al., 2023).

Results. As shown in Table S2, both the T5 model and ARMs achieve zero accuracy and low BLEU scores with reverse queries. Equipping with P2, we successfully improve the accuracy of MDMs in Reverse direction of task Description To Name and the BLEU metric of Name To Description in both directions.

## G.1.2 Additional Comparison Among Sampling Methods

We provide an expanded ablation over sampling strategies for difusion code generation in Table S3, complementing the results in Table 6. We evaluate on two families of benchmarks. HumanEval and MBPP measure standard left-to-right code completion, while HumanEval+ and MBPP+ use strengthened unit tests to probe functional correctness under more adversarial cases. To stress the non-causal advantages of difusion models, we additionally report infilling performance on HumanEval-Infill and SantaCoder-FIM, where models must complete missing spans given both left and right context. All methods share the same Open-dCoder base model and inference budget; only the sampling rule for choosing which masked positions to update difers. The compared samplers span common baselines and recent state-of-the-art. Vanilla Ancestral follows the standard stochastic reverse difusion procedure, unmasking positions uniformly at each step. Greedy Ancestral replaces stochastic updates with always taking the argmax token, which typically improves short-horizon correctness but can cause premature commitment. Entropy-based Confidence prioritizes positions with low predictive entropy (high confidence), akin to confidence-ordered decoding used in MaskGIT-style samplers (Chang et al.,

2022b). TopK-Margin (Kim et al., 2025) selects positions by the logit margin between the top two candidates, a stronger confidence proxy that has shown gains in recent dLLM work. Finally, P2-self-plan is our planner that jointly decides unmasking and selective remasking based on a lookahead objective, explicitly optimizing the global denoising path instead of applying a local heuristic. Across all six tasks and both Pass@1 and Pass@10, P2-self-plan consistently achieves the best performance. Relative to Vanilla Ancestral, P2 yields large gains on standard completion (e.g., +17.5 Pass@1 on HumanEval and +14.9 on MBPP) and also improves infilling and FIM, indicating that its path-level planning benefits both causal and non-causal settings. Greedy Ancestral and Entropy-based Confidence provide clear improvements over Vanilla, confirming that informed, confidence-driven ordering is important for dLLM sampling; however, their gains saturate because they remain purely myopic and cannot revise earlier low-quality decisions. TopK-Margin is competitiv among heuristic baselines but still trails P2, suggesting that better confidence estimates alone are insuficient without explicit planning over future denoising dynamics. Overall, these results reinforce that the sampling algorithm is a first-order determinant of dLLM performance, and that P2 ofers a robust, consistently superior default for both code completion and infilling.

Table S3: Performance comparison across coding benchmarks for diferent sampling methods.

<table><tr><td rowspan="2">Method</td><td colspan="2">HumanEval</td><td colspan="2">HumanEval+</td><td colspan="2">MBPP</td><td colspan="2">MBPP+</td><td colspan="2">HumanEval Infill</td><td>SantaCoder</td></tr><tr><td>P@1</td><td>P@10</td><td>P@1</td><td>P@10</td><td>P@1</td><td>P@10</td><td>P@1</td><td>P@10</td><td>P@1</td><td>P@1</td><td>P@1</td></tr><tr><td>P2-self-plan</td><td>20.8</td><td>38.4</td><td>17.6</td><td>35.2</td><td>16.7</td><td>38.4</td><td>23.9</td><td>53.6</td><td></td><td>77.4</td><td>56.4</td></tr><tr><td>Vanilla Ancestral</td><td>3.3</td><td>18.3</td><td>3.2</td><td>15.2</td><td>1.8</td><td>13.2</td><td>2.9</td><td>21.8</td><td></td><td>72.7</td><td>53.8</td></tr><tr><td>Greedy Ancestral</td><td>9.3</td><td>31.1</td><td>8.1</td><td>28.7</td><td>5.3</td><td>29.0</td><td>8.7</td><td>41.5</td><td></td><td>75.1</td><td>53.7</td></tr><tr><td>Entropy-based Confidence</td><td>12.6</td><td>35.4</td><td>10.9</td><td>29.9</td><td>9.2</td><td>36.8</td><td>15.2</td><td>50.7</td><td></td><td>75.1</td><td>53.2</td></tr><tr><td>TopK-Margin</td><td>7.6</td><td>27.4</td><td>6.5</td><td>26.2</td><td>3.9</td><td>24.0</td><td>6.2</td><td>33.5</td><td></td><td>75.0</td><td>54.4</td></tr></table>

## G.2 Protein Generation

## G.2.1 Performance Across Length Categories.

We analyze the performance of protein generation models across various sequence lengths, ranging from 200 to 800 base pairs. Certain models, such as ProGen, do not generate proteins of fixed lengths; therefore, we group results into length categories to facilitate meaningful comparisons. As shown in Figure S1, the performance of these models varies with length, highlighting their capabilities and limitations across diverse length categories.

![](Peng2025Path_figs/514dda33f76bfc479b76ff48a7838dec9b1d1920a71d7ef952bfb4bffad23d92.jpg)  
Figure S1: Protein Sequence Generation Benchmark: Performance across length categories (200–800).

Table S4: Ablation on model scale for ProGen2 and DPLM. P2 (Trained Planner, 8M) consistently improves DPLM variants. Scaling alone does not ensure better performance.

<table><tr><td>Model Variant</td><td>pLDDT↑</td><td>pTM↑</td><td>pAE↓</td><td>Foldability (%)↑</td><td>Entropy↑</td><td>Diversity (%)↑</td></tr><tr><td>ProGen2-small</td><td>49.38</td><td>0.28</td><td>23.38</td><td>4.48</td><td>2.55</td><td>89.31</td></tr><tr><td>ProGen2-medium</td><td>57.94</td><td>0.38</td><td>20.81</td><td>12.75</td><td>2.91</td><td>91.45</td></tr><tr><td>ProGen2-large</td><td>55.07</td><td>0.35</td><td>22.00</td><td>11.87</td><td>2.73</td><td>91.48</td></tr><tr><td>DPLM-150M</td><td>80.23</td><td>0.65</td><td>12.07</td><td>48.14</td><td>3.14</td><td>92.80</td></tr><tr><td>+ P2-Train</td><td>83.45</td><td>0.72</td><td>10.15</td><td>58.86</td><td>3.35</td><td>92.69</td></tr><tr><td>DPLM-650M</td><td>79.53</td><td>0.66</td><td>11.85</td><td>49.14</td><td>3.18</td><td>92.22</td></tr><tr><td>+ P2-Train</td><td>81.69</td><td>0.69</td><td>11.05</td><td>54.08</td><td>3.25</td><td>91.25</td></tr></table>

![](Peng2025Path_figs/9e09f0a944c4a9ed623da3bc1b39ad3cd9ca1f527f0b12cb38249b046690c750.jpg)  
Figure S2: The Design Space of P2 (See Figure S5 for more). P2 Generalizes existing sampling algorithms with specific stochasticity strength and planner choice.

## G.2.2 Ablation over model scale for ProGen2 and DPLM.

## G.2.3 Ablation of Path Planning

The Design Space of Path Planning. Our Path Planning (P2) framework generalizes existing sampling strategies, including vanilla ancestral sampling, greedy ancestral sampling, RDM sampling, and DFM sampling, by incorporating specific parameterizations. In Figure S2, we instantiate these sampling algorithms and evaluate their performance on protein sequence generation, focusing on foldability (additional metric results are provided in Figure S5).

Vanilla and greedy ancestral sampling employ a stochasticity strength of 0, efectively disabling remasking, which results in poor performance. DFM sampling introduces tunable stochasticity, leading to improved performance over ancestral sampling; however, it lacks trajectory planning, which limits its efectiveness.

![](Peng2025Path_figs/322ece447357f2c7907de392f94be18144c249acf016f1c8006bb16be6c50c15.jpg)  
Figure S3: Ablation of the Planner Size: an 8M BERT planner functions similarly to a 3B BERT. Self-planning performs better in a default temperature of 1. We sweep the temperature from 0.1 to 2.0 and plot the scaling between the resultant sequence entropy and the foldability. For more see Figure S6.

RDM sampling, by contrast, enables remasking with a default stochasticity strength of 1 and utilizes the denoiser’s confidence for self-planning, yielding better sampling quality.

P2 combines the advantages of these existing algorithms, ofering both controllable stochasticity strength and planning guidance. By tuning stochasticity strength, P2 can enhance RDM sampling and optionally leverage an external BERT planner to further steer the sampling trajectory toward generating high-quality sequences.

Table S5: Ablation of Sampling Strategies. Path planning (P2) outperforms existing sampling strategies, including DDPD. The arrows indicate whether higher (↑) or lower (↓) values are better.

<table><tr><td>Sampling Algorithm</td><td>pLDDT (↑)</td><td>pTM (↑)</td><td>pAE (↓)</td><td>Foldability (%) (↑)</td><td>Entropy (↑)</td><td>Diversity (%) (↑)</td></tr><tr><td>Vanilla Ancestral</td><td>44.08</td><td>0.34</td><td>20.61</td><td>2.00</td><td>4.03</td><td>93.63</td></tr><tr><td>RDM Sampling</td><td>74.67</td><td>0.71</td><td>10.33</td><td>43.00</td><td>3.85</td><td>93.12</td></tr><tr><td>P2 + 8M BERT Planner</td><td>78.24</td><td>0.74</td><td>9.11</td><td>44.50</td><td>3.80</td><td>92.77</td></tr><tr><td>DDPD + 8M BERT Planner</td><td>46.51</td><td>0.24</td><td>23.20</td><td>0.25</td><td>0.31</td><td>51.69</td></tr><tr><td>Ancestral</td><td>52.67</td><td>0.46</td><td>17.64</td><td>7.75</td><td>3.98</td><td>93.42</td></tr></table>

In this section, we utilize the protein sequence generation task as an ablation benchmark to analyze the implications of our Path Planning (P2) design choices. We experiment with the ESM2 (Lin et al., 2023) family of protein language models, including versions with 8M, 35M, 150M, 650M, and 3B parameters, for variants incorporating a BERT planner. For the denoiser, we train a 150M MDM from scratch, using the same architecture as ESM2-150M and DPLM-150M, for 500k steps with approximately 320k tokens per step. Training details are provided in Section F.1.1.

Table S6: Comparison of negative ELBOs for Path Planning Planners and self-planning, averaged on 20 runs. Lower values (↓) indicate better ELBO. The ELBO is computed at default temperature 1, corresponding to the star-annotation results in Figure S3.

<table><tr><td>Method</td><td>Unmasked pos.-ELBO (↓)</td><td>Masked pos.-ELBO (↓)</td></tr><tr><td>P2 + Planner ESM2-8M</td><td>22.5</td><td>13.4</td></tr><tr><td>P2 + Planner ESM2-35M</td><td>22.0</td><td>13.4</td></tr><tr><td>P2 + Planner ESM2-150M</td><td>21.8</td><td>13.4</td></tr><tr><td>P2 + Planner ESM2-650M</td><td>21.7</td><td>13.4</td></tr><tr><td>P2 + Planner ESM2-3B</td><td>21.6</td><td>13.4</td></tr><tr><td>P2 (self-planning)</td><td>15.7</td><td>13.4</td></tr></table>

Table S7: Ablation study of self-planning. We compare self-planning using denoiser-predicted probabilities with a uniformly sampled probability baseline. finetuned MDM refers to MDM fine-tuned from BERT (DPLM-150M (Wang et al., 2024)), while tfs-MDM refers to MDM trained from scratch.

<table><tr><td>Configuration</td><td>pLDDT (↑)</td><td>pTM (↑)</td><td>pAE (↓)</td><td>Foldability (↑)</td><td>Entropy (↑)</td><td>Diversity (↑)</td></tr><tr><td>finetuned MDM</td><td>82.62</td><td>0.72</td><td>9.15</td><td>63.00</td><td>3.40</td><td>93.05</td></tr><tr><td>finetuned MDM + Uniform</td><td>72.61</td><td>0.66</td><td>11.82</td><td>39.00</td><td>4.01</td><td>93.62</td></tr><tr><td>tfs-MDM</td><td>74.67</td><td>0.71</td><td>10.33</td><td>43.00</td><td>3.85</td><td>93.12</td></tr><tr><td>tfs-MDM + Uniform</td><td>59.88</td><td>0.52</td><td>15.57</td><td>20.00</td><td>4.00</td><td>93.57</td></tr></table>

Results. Table S5 demonstrates that our P2 approach consistently outperforms existing sampling strategies across all folding metrics, while maintaining strong token entropy and sequence diversity. Notably, results are further enhanced when an external BERT planner is utilized. To provide a comparative perspective, we perform an apple-to-orange evaluation against a planner-based sampling algorithm, DDPD, equipped with the same BERT planner. DDPD is prone to generating low-entropy, repetitive sequences with poor foldability, as it relies exclusively on the planner to dictate both unmasking and remasking. In contrast, P2 separates these responsibilities: remasking is delegated to the BERT planner, while unmasking is guided by the denoiser itself. This decomposition mitigates the planner’s bias and leverages the denoiser’s planning capabilities efectively.

In Figure S3, we ablate the size of the planner and evaluate foldability under varying temperatures (entropy). Additional metric results are shown in Figure S6. Our findings reveal that an 8M BERT planner is suficient to guide a 150M MDM, achieving competitive performance relative to its 3B counterpart across a broad range of entropy values. Furthermore, the BERT planner demonstrates superior scalability compared to the self-planning variant, preserving foldability under extreme high and low temperature conditions.

Self-Planning Analysis. In our self-planning approach, we leverage the predicted probabilities from unmasked positions to guide unmasking decisions. This raises a key question: Are the predicted probabilities from unmasked tokens meaningful? We conducted an ablation study where we replaced predicted probabilities for unmasked tokens with uniformly random values and performed the experiments on two MDM variants: one trained from scratch and another fine-tuned from a BERT-based model (DPLM-150M (Wang et al., 2024)). The DPLM-150M was fine-tuned from ESM2, which was pretrained to predict both masked and randomly mutated tokens, making it more likely to inherit meaningful logits for unmasked positions. As shown in Table S7, randomizing unmasked token probabilities leads to a substantial decline in performance across both variants. This finding confirms that unmasked token logits are informative, despite the lack of direct supervision. It is also evidenced by the ELBO from Proposition 1 in Table S6 where self-planning displays an even better ELBO compared with BERT planners, further validating its efectiveness.

![](Peng2025Path_figs/162e296cbeb7c6a317abadc92039472b66ab0595a72b3efaa8f9858d6d32375a.jpg)

![](Peng2025Path_figs/ce5e9df49aae8bf2a0fbc48f3516c63e245cc8290faa9bd1be6693250415f891.jpg)

![](Peng2025Path_figs/c85d32475ee213797bd0854f52bbee6e4f7f380991908a89c32b211761d3f63c.jpg)  
Figure S4: Top: Performance vs. Sampling Time (steps). Bottom: Running Time (left) and Speed (right) vs. Sequence Length.

## G.2.4 Sampling Eficiency

Increasing the number of sampling steps generally enhances generative quality, albeit with increased computational time. To evaluate the scaling eficiency, we benchmark three sampling algorithms—ancestral sampling, P2 (self-planning), and P2 augmented with an 8M BERT planner—on the task of protein sequence generation. We measure the foldability across increasing sampling steps in terms of elapsed time (benchmarked on NVIDIA A100 GPUs). In Figure S4 top, P2 achieves superior foldability compared to ancestral sampling, while the inclusion of the external BERT planner demonstrates exceptional scalability, particularly at higher sampling steps. In Figure S4 bottom, we further analyze inference eficiency by examining elapsed time and speed (tokens per second) as a function of sequence length. P2 with self-planning maintains the same inference cost as ancestral sampling, as it does not rely on an external model. Conversely, P2 with the BERT planner doubles the number of sampling steps due to one additional BERT evaluation. However, since the planner is a lightweight 8M model compared to the 150M MDM, the overhead is negligible. This is eviden in the figure, where the performance gap between P2 (self-planning) and P2 with the 8M BERT planner becomes indistinguishable at higher sampling scales.

## G.2.5 Design Space of P2.

We explore the design space of our proposed P2 framework using key metrics, including pLDDT, pAE, pTM, entropy, and diversity. As illustrated in Figure S5, P2 demonstrates a strong ability to balance structural accuracy and diversity, underscoring its versatility and robustness in protein generation tasks.

![](Peng2025Path_figs/35b0edda9a5cca19112dfc2b3de2fe66dff7f079686c7c08a0859b8d103381bb.jpg)  
Figure S5: Design space of P2, characterized by pLDDT, pAE, pTM, entropy, and diversity metrics.

## G.2.6 Ablation Study on the Planner.

We investigate the impact of planner size on model performance through an ablation study. Figure S6 shows how varying the planner size afects key metrics such as pLDDT and diversity. These results emphasize the importance of planner size in optimizing the quality and consistency of generated sequences.

![](Peng2025Path_figs/2515912edff74d35e48d83c1a55b7474152f3dee0d59d2dd8b1d34b8112c87e0.jpg)

![](Peng2025Path_figs/084c6130079d19ec7534fe15fa95731469d66e10f0cf4296fc63ec52fa5b6a1f.jpg)

![](Peng2025Path_figs/caf389d67974f89cb5810ce4e8f10c0e1a0218a0a39de3d29dcf204c49a47182.jpg)

![](Peng2025Path_figs/3fb9f1a1cc3b143222986dee48f164783cae071f1ed3e5d81fe2959877bdcdfb.jpg)  
Figure S6: Ablation study of planner size and its impact on protein generation performance.

## G.2.7 Inference-Time Scaling: Performance vs. Sampling Time.

To evaluate the trade-of between inference time and performance, we investigate how sampling time scales with model performance. These results will be detailed in future work, but they highlight the scalability of our approach for eficient protein generation.

## G.2.8 Performance on Short Protein Sequences (<200 residues).

While our main results focus on proteins of length 200–800, we also examined performance on shorter proteins. As shown in Table S8, P2 provides substantial improvements even for shorter sequences (64–200 residues). The gains are less pronounced than for longer sequences due to two factors: (1) shorter sequences are underrepresented in the UniRef50 training corpus, limiting model learning; and (2) ESMFold, used for evaluation, is less accurate on shorter sequences. Nevertheless, P2 consistently improves pLDDT and pTM while reducing pAE.

## G.2.9 Comparison with Additional Baselines (ESM2).

We further tested P2 in combination with alternative protein language models to assess generalizability. Although ESM2 is not designed as a generative model, adding P2 yields measurable improvements. For reference, we also include ESM3, ProGen2, and EvoDif baselines. As shown in Table S9, P2 enhances generation quality across models, with particularly large gains when combined with DPLM.

Table S8: Performance on short proteins of diferent lengths. P2 substantially improves generation quality.

<table><tr><td>Length</td><td>pLDDT Anc</td><td>pLDDTP2</td><td>pTM Anc</td><td>pTMP2</td><td>pAE Anc</td><td>pAEP2</td><td>Entropy Anc</td><td>Entropy P2</td></tr><tr><td>64</td><td>49.62</td><td>70.67</td><td>0.26</td><td>0.48</td><td>16.03</td><td>10.13</td><td>3.74</td><td>2.27</td></tr><tr><td>100</td><td>43.92</td><td>70.08</td><td>0.25</td><td>0.48</td><td>18.50</td><td>11.91</td><td>3.80</td><td>2.17</td></tr><tr><td>150</td><td>46.32</td><td>71.17</td><td>0.29</td><td>0.54</td><td>19.24</td><td>11.94</td><td>3.79</td><td>2.41</td></tr><tr><td>200</td><td>56.94</td><td>80.11</td><td>0.38</td><td>0.68</td><td>17.96</td><td>9.43</td><td>3.67</td><td>2.80</td></tr></table>

Table S9: Comparison with additional protein language model baselines.

<table><tr><td>Model</td><td>pLDDT↑</td><td>pTM↑</td><td>pAE↓</td><td>Entropy↑</td></tr><tr><td>EvoDiff</td><td>31.84</td><td>0.21</td><td>24.76</td><td>4.05</td></tr><tr><td>ESM3</td><td>34.13</td><td>0.23</td><td>24.65</td><td>3.99</td></tr><tr><td>ProGen2</td><td>49.38</td><td>0.28</td><td>23.38</td><td>2.55</td></tr><tr><td>DPLM</td><td>80.23</td><td>0.65</td><td>12.07</td><td>3.14</td></tr><tr><td>DPLM + P2</td><td>83.45</td><td>0.72</td><td>10.15</td><td>3.35</td></tr><tr><td>ESM2-150M + P2</td><td>40.99</td><td>0.16</td><td>27.08</td><td>1.51</td></tr></table>

## G.2.10 Comparison with Top-K Marginal.

Recent work by Kim et al. (2025) introduced the Top-K Marginal method for masked difusion models. We directly compare Top-K Marginal with our P2 framework in the protein generation setting. As shown in Table S10, P2 substantially outperforms Top-K Marginal, achieving large improvements in all structural quality metrics (pLDDT, pTM, pAE) as well as entropy. These results demonstrate that P2 not only subsumes Top-K Marginal as a special case, but also provides a significant empirical advantage.

Table S10: Comparison with Top-K Marginal (Kim et al., 2025).

<table><tr><td>Model</td><td>pLDDT↑</td><td>pTM↑</td><td>pAE↓</td><td>Entropy↑</td></tr><tr><td>DPLM</td><td>80.23</td><td>0.65</td><td>12.07</td><td>3.14</td></tr><tr><td>DPLM + Top-K Marginal</td><td>53.89</td><td>0.31</td><td>22.49</td><td>2.03</td></tr><tr><td>DPLM + P2 (ours)</td><td>83.45</td><td>0.72</td><td>10.15</td><td>3.35</td></tr></table>

## G.2.11 Variance Analysis of P2.

To assess robustness, we computed variance statistics over 20 independent runs of DPLM+P2. As shown in Table S11, while variance is non-negligible—particularly for pLDDT due to local fluctuations in poorly generated residues—P2 consistently maintains strong mean performance.

## G.2.12 Generated Protein Sequences and Their Predicted Structures.

We fold the protein sequences generated by our model using ESMFold and visualize their predicted structures in Figures S7–S10. For each length category—200, 300, 400, 500, 600, 700, and 800—we display 15 representative proteins. These visualizations highlight the structural diversity and consistency of the generated sequences, providing evidence of the model’s ability to predict biologically plausible structures across diverse lengths.

![](Peng2025Path_figs/041269ce398294edb2f89d90c284cc1e416e6237702acf667a249da442c9a3db.jpg)  
Figure S7: Predicted structures of generated protein sequences (Group 1). Each panel represents structures generated for specific length categories.

![](Peng2025Path_figs/7b00e8a81969975d18f95895e540827bd2e182b6d704b714078239dad38fd603.jpg)  
Figure S8: Predicted structures of generated protein sequences (Group 2). Each panel corresponds to diferent length categories.

![](Peng2025Path_figs/e0bacad0b9626edcc49b83f67112d8df73944ff5e2fb63535a688d230ae6a020.jpg)  
Figure S9: Predicted structures of generated protein sequences (Group 3). These structures illustrate the diversity and robustness of the generation process.

Table S11: Variance of DPLM+P2 performance over 20 runs.

<table><tr><td>Metric</td><td>pLDDT↑</td><td>pTM↑</td><td>pAE↓</td><td>Entropy↑</td></tr><tr><td>Mean</td><td>77.39</td><td>0.62</td><td>11.62</td><td>2.91</td></tr><tr><td>Std. Dev.</td><td>18.52</td><td>0.27</td><td>7.89</td><td>1.20</td></tr></table>

![](Peng2025Path_figs/0b9317f1a55d640fe81e2b61251d58e72dd9850f7ffc214b20c442f7fb6d28fc.jpg)  
Figure S10: Predicted structures of generated protein sequences (Group 4). This group emphasizes structures for the longest generated sequences.

## G.3 RNA Generation

## G.3.1 RNA MDM Training Implementation.

The RNA MDM follows the same discrete difusion described in (Zheng et al., 2023). The MDM was trained using a machine mounted with 4 A100 GPUs, each with 40GB memory. The training implementation is otherwise identical to the second-stage fine-tuning described in (Wang et al., 2024), where we continued from a RiNALMo (Penić et al., 2024) checkpoint instead of ESM-2 (Lin et al., 2023).

## G.3.2 Visualizing the Predicted Structures of Generated RNA Sequences.

We extend our analysis to RNA sequence generation by folding RNA sequences of 200 base pairs using AlphaFold3 (Abramson et al., 2024). The predicted folding structures, visualized in Figures S11 and S12, highlight the diversity and consistency of the RNA structures generated by the model. Particularly, predicted structures exhibit greater diversity as sequence length increases, as is observed in nature, while their pLDDT’s mirroring those computed for natural sequences. We also include the predicted secondary structures of generated RNAs in Figure S13. These results demonstrate the model’s ability to generate biologically plausible RNA sequences suitable for downstream applications.

![](Peng2025Path_figs/966ccccbfc9434105b6d01f898a88626da5d6d0f6da745d1c9d1e6e04c3813ce.jpg)  
Figure S11: Predicted structures of additional generated RNA sequences (100 bps).

![](Peng2025Path_figs/a2626e6cd14fbd69830defafa11dfa2e51d308674615adff5c9d7f6a5c8d1f8e.jpg)  
Figure S12: Predicted structures of generated RNA sequences (200 bps). This figure showcases the structural diversity of RNA sequences generated by the model as sequence length increases, which is observed in nature.

![](Peng2025Path_figs/813abb6a71684df4d6bb5440aabaa4eafad80d6297034af015a12e14d92a9b82.jpg)  
Figure S13: Predicted secondary structures of generated RNA sequences of length 100 (top) and 200 bp (bottom). Predictions were made using ViennaRNA (Lorenz et al., 2011) and visualized with forna (Kerpedjiev et al., 2015).