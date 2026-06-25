---
citation_key: Shu2023Federated
arxiv_id: 2308.04077
arxiv_url: https://arxiv.org/abs/2308.04077
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-24T16:02:42Z
origin: ai+web
reviewed: false
---

# Introduction

Due to the growing computational power of edge devices and increasing privacy concerns, recent years have witnessed a surging interest in *federated optimization*, which finds real-world applications such as federated learning [@federated]. Federated optimization allows the agents to retain their local datasets and hence only share their gradients. However, in many important applications of federated optimization such as federated black-box adversarial attack [@fedzo], the gradient information is not available. This consequently gives rise to the paradigm of federated *zeroth-order* *optimization* (ZOO), in which the global function to be optimized is an aggregation of the local functions that are distributed on edge devices (i.e., clients) and are only accessible via function queries [@fedzo]. To tackle federated ZOO, existing algorithms [@fedzo] follow the framework of using *finite difference* (FD) for local gradient estimation and hence resorting to federated *first-order optimization* (FOO) algorithms (e.g., FedAvg [@fedavg]) for optimization.[^1] Nevertheless, these algorithms usually suffer from both query and communication inefficiency, especially in heterogeneous settings characterized by significant disparities between local and global functions. This thus impedes their practical applicability, especially in scenarios with restricted query and communication resources. To the best of our knowledge, little attention has been dedicated to achieving query- and communication-efficient federated ZOO algorithms.

To address this problem, it is imperative to firstly identify the challenges faced by federated ZOO algorithms which are responsible for their query and communication inefficiency (Sec. [3](#sec:framework&challenge){reference-type="ref" reference="sec:framework&challenge"}). Federated ZOO requires multiple *communication* rounds for central server aggregation; between consecutive communication rounds, every client performs several iterations of local optimization using their estimated gradients which are usually approximated via additional function *queries* (e.g., based on FD). Firstly, we show (Sec. [3](#sec:framework&challenge){reference-type="ref" reference="sec:framework&challenge"}) that the *query inefficiency* of existing federated ZOO algorithms arises from their employment of FD for local gradient estimation, which often requires an excessive number of additional function queries. Therefore, addressing the challenge of query efficiency in federated ZOO calls for a gradient estimation method that requires minimal (ideally zero) additional function queries. Secondly, we show (Sec. [3](#sec:framework&challenge){reference-type="ref" reference="sec:framework&challenge"}) that the *communication inefficiency* of these existing algorithms results from the disparity between their realized local updates and the intended global updates, which is typically caused by client heterogeneity. Hence, resolving the challenge of communication efficiency requires developing a high-quality gradient correction technique to mitigate such a disparity.

To this end, we propose the *[f]{.underline}ederated [z]{.underline}eroth-[o]{.underline}rder [o]{.underline}ptimization using trajectory-informed [s]{.underline}urrogate gradients* (FZooS) algorithm to address the aforementioned challenges, and hence to achieve query- and communication-efficient federated ZOO. Firstly, we introduce the recent *derived Gaussian process* [@zord], which only requires the optimization trajectory (i.e., the history of function queries during optimization) for gradient estimation, as the local gradient surrogates for the clients, thereby realizing query-efficient gradient estimation in federated ZOO (Sec. [4.1](#sec:local-surrogates){reference-type="ref" reference="sec:local-surrogates"}). Secondly, based on these local gradient surrogates, we use *random Fourier features* (RFF) approximation [@rahimi2007random] to produce a transferable global gradient surrogate (without transferring raw observations), which is an accurate estimate of the gradient of the global function (Sec. [4.2.1](#sec:global-surrogates){reference-type="ref" reference="sec:global-surrogates"}). Using these surrogates, we develop the technique of *adaptive gradient correction* using adaptive gradient correction vector and length to mitigate the disparity between our local updates and the intended global updates, and consequently to improve the communication efficiency of federated ZOO (Sec. [4.2.2](#sec:adaptive-est){reference-type="ref" reference="sec:adaptive-est"}).

We verify that our FZooS has addressed the aforementioned challenges via both theoretical analysis and empirical experiments. We firstly theoretically bound the disparity between our realized local updates in FZooS and the intended global updates in the federated ZOO problems with heterogeneous clients. It shows that our local update is superior to those employed by the previous works because it achieves both a better query efficiency and smaller disparity error (Sec. [5.1](#sec:est-analysis){reference-type="ref" reference="sec:est-analysis"}). Based on this, we then prove the convergence of our FZooS and show that FZooS also enjoys an improved communication efficiency over the existing algorithms (Sec. [5.2](#sec:conv-analysis){reference-type="ref" reference="sec:conv-analysis"}). Lastly, we use extensive experiments, such as synthetic experiments, federated black-box adversarial attack and federated non-differentiable metric optimization, to show that our FZooS consistently outperforms the existing federated ZOO algorithms in terms of both query efficiency and communication efficiency (Sec. [6](#sec:exps){reference-type="ref" reference="sec:exps"}).

# Problem Setup and Notations {#sec:setting}

In the federated *zeroth-order optimization* (ZOO) setting [@fedzo], we aim to minimize a global function $F$ defined on the domain ${\mathcal{X}}\triangleq [0,1]^d$, which is the arithmetic average of $N$ local functions $\{f_1, \cdots, f_N\}$ distributed on $N$ different clients with $\left|f_i({\bm{x}})\right| \leq 1$ for any ${\bm{x}}\in {\mathcal{X}}$ and $i \in [N]$, [^2] without sharing these local functions: $$\begin{equation}
    \min_{{\bm{x}}\in {\mathcal{X}}} F({\bm{x}}) \triangleq \frac{1}{N}{\textstyle\sum}_{i \in [N]} f_i({\bm{x}}). \label{eq:obj}
\end{equation}$$ A central server is typically introduced to periodically aggregate the updated inputs sent from the distributed clients after their several iterations of local optimization. Of note, in this federated ZOO setting, the gradients of the local functions are either not accessible or too computationally expensive to obtain. Consequently, the gradients can not be directly employed for optimization, which is our main difference from the standard federated *first-order optimization* (FOO) setting [@beyond; @wang2021field; @adap-fed]. Instead, given an input ${\bm{x}}\in {\mathcal{X}}$, agent $i$ is only allowed to observe a noisy output $y_i({\bm{x}}) \triangleq f_i({\bm{x}}) + \zeta$ of the local function $f_i$, in which $\zeta \sim {\mathcal{N}}(0, \sigma^2)$. Moreover, we focus on federated ZOO with heterogeneous clients, i.e., the local functions $\{f_i\}_{i=1}^N$ differ from the global function $F$. Besides, we adopt a common assumption on $\{f_i\}_{i=1}^N$: We assume that every local function $f_i$ is sampled from a *Gaussian process* (GP), i.e., $f_i \sim \mathcal{GP}(\mu(\cdot), k(\cdot, \cdot))$ [@zord], in which $k$ is a shift-invariant kernel and is assumed to have $\left\|\partial_{{\bm{z}}}\partial_{{\bm{z}}'} k({\bm{z}},{\bm{z}}')|_{{\bm{z}}={\bm{z}}'={\bm{x}}}\right\|\leq \kappa, \left\|\partial_{{\bm{z}}} k({\bm{z}},{\bm{x}}')|_{{\bm{z}}={\bm{x}}}\right\|\leq L \, (\forall{{\bm{x}}, {\bm{x}}'} \in {\mathcal{X}})$ for some $\kappa > 0$ and $L>0$. This encompasses commonly used kernels such as the squared exponential kernel [@RasmussenW06]. Unless specified otherwise, we use $\|\cdot\|$ to denote the norm $\|\cdot\|_2$, $[Z]$ to denote the set $\{1,\cdots, Z\}$, and $[Z)$ to denote the set $\{0,\cdots, Z-1\}$ where $Z$ is an integer. We will use $i \in [N]$ to denote the formulas related to client $i$ throughout this paper.

# Framework and Challenges for Federated ZOO {#sec:framework&challenge}

Here we firstly summarize the framework to solve the federated ZOO problem (Sec. [3.1](#sec:framework){reference-type="ref" reference="sec:framework"}), and then identify the challenges which existing algorithms following this framework fail to address (Sec. [3.2](#sec:challenges){reference-type="ref" reference="sec:challenges"}).

## Optimization Framework {#sec:framework}

To solve [\[eq:obj\]](#eq:obj){reference-type="eqref" reference="eq:obj"}, a general optimization framework is to estimate the gradients of $\{f_i\}_{i=1}^N$ using only function queries and then employ the standard federated FOO algorithms for the optimization, as in Algo. [\[alg:fedzoo\]](#alg:fedzoo){reference-type="ref" reference="alg:fedzoo"}. Specifically, in round $r$, every client performs $T$ iterations of local gradient decent updates in parallel (line 2-5 of Algo. [\[alg:fedzoo\]](#alg:fedzoo){reference-type="ref" reference="alg:fedzoo"}), in which $\widehat{{\bm{g}}}_{r,t-1}^{\smash{(i)}} \in {\mathbb{R}}^d$ denotes the estimated gradient by client $i$ for the local update in iteration $t$ of round $r$. After that, each client sends its locally updated input ${\bm{x}}_{r,T}^{\smash{(i)}}$ to server (line 6 of Algo. [\[alg:fedzoo\]](#alg:fedzoo){reference-type="ref" reference="alg:fedzoo"}). After receiving the updated inputs from all clients (i.e., $\{{\bm{x}}_{r,T}^{\smash{(i)}}\}_{i=1}^N$), the server aggregates them (e.g., via arithmetic average) to produce a globally updated input ${\bm{x}}_{r}$, and then sends it back to the clients for the optimization in the next round (line 7-8 of Algo. [\[alg:fedzoo\]](#alg:fedzoo){reference-type="ref" reference="alg:fedzoo"}).

The aforementioned $\widehat{{\bm{g}}}_{r,t-1}^{\smash{(i)}}$ used in the literature can be summarized into the following general form: $$\begin{equation}
    \widehat{{\bm{g}}}_{r,t-1}^{(i)} \triangleq {\bm{g}}_{r,t-1}^{(i)} + \gamma_{r,t-1}^{(i)} \Big({\bm{g}}_{r-1}({\bm{x}}') - {\bm{g}}_{r-1}^{(i)}({\bm{x}}'')\Big) \label{eq:general-grad-est}
\end{equation}$$ where ${\bm{g}}_{r,t-1}^{\smash{(i)}} \in {\mathbb{R}}^d$ is an estimate of $\nabla f_i({\bm{x}}_{r,t-1}^{\smash{(i)}})$ and is usually obtained using the *finite difference* (FD) methods (refer to Sec. [3.2](#sec:challenges){reference-type="ref" reference="sec:challenges"}). In addition, the *gradient correction vector* ${\bm{g}}_{r-1}({\bm{x}}') - {\bm{g}}_{r-1}^{\smash{(i)}}({\bm{x}}'') \in {\mathbb{R}}^d$ is usually obtained from the previous round $r-1$. This aims to make the resulting $\widehat{{\bm{g}}}_{r,t-1}^{\smash{(i)}}$ better aligned with $\nabla F({\bm{x}}_{r,t-1}^{\smash{(i)}})$, such that the local update on each client (i.e., line 5 of Algo. [\[alg:fedzoo\]](#alg:fedzoo){reference-type="ref" reference="alg:fedzoo"}) can better approximate the intended global update along the direction of $\nabla F({\bm{x}}_{r,t-1}^{\smash{(i)}})$. It is especially important in the presence of client heterogeneity, i.e., $\{\nabla f_i\}_{i=1}^N$ differ from $\nabla F$. Intuitively, to accomplish this alignment, ${\bm{g}}_{r-1}({\bm{x}}')$ and ${\bm{g}}_{r-1}^{\smash{(i)}}({\bm{x}}'')$ should be good estimates of $\nabla F({\bm{x}}_{r,t-1}^{\smash{(i)}})$ and $\nabla f_i({\bm{x}}_{r,t-1}^{\smash{(i)}})$, respectively, which we theoretically justify in Sec. [3.2](#sec:challenges){reference-type="ref" reference="sec:challenges"}. Of note, the form of ${\bm{g}}_{r-1}({\bm{x}}') - {\bm{g}}_{r-1}^{\smash{(i)}}({\bm{x}}'')$ for gradient correction usually aims to ensure that the estimation biases from ${\bm{g}}_{r-1}({\bm{x}}')$ and ${\bm{g}}_{r-1}^{\smash{(i)}}({\bm{x}}'')$ could cancel out [@svrg-first]. Finally, $\gamma_{r,t-1}^{\smash{(i)}} \in [0,1]$ denotes the *gradient correction length*, which can be adjusted to trade off the utilization of the gradient correction vector (Sec. [3.2](#sec:challenges){reference-type="ref" reference="sec:challenges"}).

Remarkably, [\[eq:general-grad-est\]](#eq:general-grad-est){reference-type="eqref" reference="eq:general-grad-est"} subsumes the forms of gradient updates employed in many existing federated ZOO algorithms, and hence Algo. [\[alg:fedzoo\]](#alg:fedzoo){reference-type="ref" reference="alg:fedzoo"} can reduce to the corresponding optimization algorithms (more details in Appx. [11](#app-sec:existing){reference-type="ref" reference="app-sec:existing"}). E.g., when $\gamma_{r,t-1}^{\smash{(i)}}=0$ and ${\bm{g}}_{r,t-1}^{\smash{(i)}}$ is obtained using FD, Algo. [\[alg:fedzoo\]](#alg:fedzoo){reference-type="ref" reference="alg:fedzoo"} becomes the FedZO algorithm [@fedzo]; when $\gamma_{r,t-1}^{\smash{(i)}}{=}1$, ${\bm{g}}_{r-1}({\bm{x}}'){=}\frac{1}{NT}\sum_{i,t=1}^{N,T} {\bm{g}}_{r-1,t-1}^{\smash{(i)}}$, and ${\bm{g}}_{r-1}^{\smash{(i)}}({\bm{x}}'')=\frac{1}{T}\sum_{t=1}^T {\bm{g}}_{r-1,t-1}^{\smash{(i)}}$, [\[eq:general-grad-est\]](#eq:general-grad-est){reference-type="eqref" reference="eq:general-grad-est"} reduces to the gradient update in [@scaffold] and hence Algo. [\[alg:fedzoo\]](#alg:fedzoo){reference-type="ref" reference="alg:fedzoo"} becomes the SCAFFOLD (Type ) algorithm in the federated ZOO setting; let the gradient correction vector ${\bm{g}}_{r-1}({\bm{x}}') - {\bm{g}}_{r-1}^{\smash{(i)}}({\bm{x}}'')$ in [\[eq:general-grad-est\]](#eq:general-grad-est){reference-type="eqref" reference="eq:general-grad-est"} be ${\bm{x}}_{r,t-1}^{\smash{(i)}} - {\bm{x}}_r$, Algo. [\[alg:fedzoo\]](#alg:fedzoo){reference-type="ref" reference="alg:fedzoo"} is then equivalent to FedProx [@fedprox] in the federated ZOO setting.

## Existing Challenges {#sec:challenges}

:::::::: {#alg:fzoos .figure}
:::: minipage
::: algorithm
:::
::::

:::: minipage
::: algorithm
:::
::::

::: caption
FZooS
:::
::::::::

Existing federated ZOO algorithms aiming to solve the problem in Sec. [2](#sec:setting){reference-type="ref" reference="sec:setting"} typically fail to address the challenges of query efficiency and communication efficiency, which we discuss in more detail below.

#### Challenge of Query Efficiency.

Similar to standard ZOO algorithms [@Nesterov2017; @prgf], existing federated ZOO algorithms (e.g., [@fedzo]) also commonly apply the FD methods [@approx-error] for gradient estimation. Specifically, given a parameter $\lambda>0$ and directions $\{{\bm{u}}_q\}_{q=1}^{\smash{Q}}$, the gradient of the function $f_i$ on client $i$ at ${\bm{x}}$ can be estimated as $$\begin{equation}
\nabla f_i({\bm{x}}) \approx {\bm{\Delta}}^{(i)}({\bm{x}}) \triangleq \frac{1}{Q}\sum_{q \in [Q]}
\frac{y_i({\bm{x}}+ \lambda {\bm{u}}_q) - y_i({\bm{x}})}{\lambda} {\bm{u}}_q \ . \label{eq:grad-est-fd}
\end{equation}$$ That is, for existing federated ZOO algorithms, ${\bm{g}}^{\smash{(i)}}_{r,t-1} = {\bm{\Delta}}^{(i)}({\bm{x}}^{\smash{(i)}}_{r,t-1})$ in [\[eq:general-grad-est\]](#eq:general-grad-est){reference-type="eqref" reference="eq:general-grad-est"}. As implied in [\[eq:grad-est-fd\]](#eq:grad-est-fd){reference-type="eqref" reference="eq:grad-est-fd"}, $Q$ additional function queries are required for the gradient estimation at every local updated input ${\bm{x}}^{\smash{(i)}}_{r,t-1}$. This therefore results in $NTQ \times$ more function queries than the standard federated FOO algorithms [@fedprox; @scaffold] in every communication round, which is unsatisfying in practice especially when $\{f_i\}_{i=1}^N$ are prohibitively costly to evaluate. So, tackling the challenge of query efficiency in federated ZOO requires designing query-efficient gradient estimators.

#### Challenge of Communication Efficiency.

When $\widehat{{\bm{g}}}_{r,t-1}^{\smash{(i)}} = \nabla F({\bm{x}}_{r,t-1}^{\smash{(i)}})$ in [\[eq:general-grad-est\]](#eq:general-grad-est){reference-type="eqref" reference="eq:general-grad-est"}, Algo. [\[alg:fedzoo\]](#alg:fedzoo){reference-type="ref" reference="alg:fedzoo"} is then able to attain the convergence of centralized FOO algorithms, which is known to be better than the one in the federated setting [@scaffold]. Therefore, intuitively, the convergence or the communication efficiency (i.e., the number of communication rounds $R$ required to achieve an ${\epsilon}$ convergence error) of Algo. [\[alg:fedzoo\]](#alg:fedzoo){reference-type="ref" reference="alg:fedzoo"} depends on the disparity between [\[eq:general-grad-est\]](#eq:general-grad-est){reference-type="eqref" reference="eq:general-grad-est"} and $\nabla F({\bm{x}}_{r,t-1}^{\smash{(i)}})$. Define the gradient disparity $\Xi^{\smash{(i)}}_{r,t} \triangleq \|\widehat{{\bm{g}}}_{r,t-1}^{\smash{(i)}} - \nabla F({\bm{x}}_{r,t-1}^{\smash{(i)}})\|^2$, we propose the following Prop. [1](#prop:opt-correction){reference-type="ref" reference="prop:opt-correction"} (proof in Appx. [10.1](#app-sec:proof:prop:opt-correction){reference-type="ref" reference="app-sec:proof:prop:opt-correction"}) to show the condition for the best-performing [\[eq:general-grad-est\]](#eq:general-grad-est){reference-type="eqref" reference="eq:general-grad-est"} and thus to justify the challenge in communication efficiency that existing federated ZOO algorithms typically fail to address well.

::: {#prop:opt-correction .proposition}
**Proposition 1**. *Let ${\bm{g}}_{r-1}^{\smash{(i)}}({\bm{x}}'') \neq {\bm{g}}_{r-1}({\bm{x}}')$, the minimum of $\Xi^{\smash{(i)}}_{r,t}$ w.r.t $\gamma_{r,t-1}^{\smash{(i)}}$ is achieved when $$\begin{equation*}
    \gamma_{r,t-1}^{\smash{(i)}} = \gamma_{r,t-1}^{(i)*} \triangleq \left(\nabla F({\bm{x}}^{(i)}_{r,t-1}) - {\bm{g}}_{r,t-1}^{(i)}\right)^{\top}\left({\bm{g}}_{r-1}({\bm{x}}') - {\bm{g}}_{r-1}^{(i)}({\bm{x}}'')\right) \left\|{\bm{g}}_{r-1}({\bm{x}}') - {\bm{g}}_{r-1}^{(i)}({\bm{x}}'')\right\|^{-2}.
\end{equation*}$$ When $\gamma_{r,t-1}^{\smash{(i)*}}=1$, $\Xi^{\smash{(i)}}_{r,t}=0$ iff we have ${\bm{g}}_{r-1}({\bm{x}}') - {\bm{g}}_{r-1}^{\smash{(i)}}({\bm{x}}'') = \nabla F({\bm{x}}^{\smash{(i)}}_{r,t-1}) - {\bm{g}}_{r,t-1}^{\smash{(i)}}$.*
:::

Prop. [1](#prop:opt-correction){reference-type="ref" reference="prop:opt-correction"} shows that to achieve a small gradient disparity, $\gamma_{r,t-1}^{\smash{(i)}}$ should be adaptive w.r.t. the alignment between the *gradient correction vector* ${\bm{g}}_{r-1}({\bm{x}}') - {\bm{g}}_{r-1}^{\smash{(i)}}({\bm{x}}'')$ and the *drift* $\nabla F({\bm{x}}^{\smash{(i)}}_{r,t-1}) - {\bm{g}}_{r,t-1}^{\smash{(i)}}$. We have shown (Appx. [10.1](#app-sec:proof:prop:opt-correction){reference-type="ref" reference="app-sec:proof:prop:opt-correction"}) that a better alignment between the gradient correction vector and the drift leads to a smaller gradient disparity, Prop. [1](#prop:opt-correction){reference-type="ref" reference="prop:opt-correction"} further shows that a zero gradient disparity (i.e., $\Xi^{\smash{(i)}}_{r,t}=0$ for any $r\in[R],t\in[T]$) can be reached when these two are perfectly aligned. To achieve such an alignment, i.e., to make ${\bm{g}}_{r-1}({\bm{x}}')=\nabla F({\bm{x}}^{\smash{(i)}}_{r,t-1})$ and ${\bm{g}}_{r-1}^{\smash{(i)}}({\bm{x}}'')={\bm{g}}_{r,t-1}^{\smash{(i)}}$ hold more likely, it requires not only *(a)* accurate gradient surrogates ${\bm{g}}_{r-1}$ and ${\bm{g}}_{r-1}^{\smash{(i)}}$ to accurately represent $\nabla F$ and $\nabla f_i$, respectively, but also *(b)* adaptive ${\bm{x}}',{\bm{x}}''$ to avoid the discrepancy between ${\bm{x}}^{\smash{(i)}}_{r,t-1}$ and ${\bm{x}}',{\bm{x}}''$.

Consequently, resolving the challenge of communication efficiency in federated ZOO mainly requires phantomsection []{#com:1 label="com:1"} []{#com:1 label="com:1"} ***(A)***

*accurate* local and global surrogates (i.e., ${\bm{g}}_{r-1}^{\smash{(i)}}$ and ${\bm{g}}_{r-1}$) for the gradient correction in [\[eq:general-grad-est\]](#eq:general-grad-est){reference-type="eqref" reference="eq:general-grad-est"}, and phantomsection []{#com:2 label="com:2"} []{#com:2 label="com:2"} ***(B)*** *adaptive* gradient correction in [\[eq:general-grad-est\]](#eq:general-grad-est){reference-type="eqref" reference="eq:general-grad-est"} with both adaptive ${\bm{x}}',{\bm{x}}''$ and adaptive $\gamma_{r,t-1}^{\smash{(i)}}$. However, existing federated ZOO algorithms usually fail to address them well: Firstly, these algorithms rely on the FD methods for gradient estimation, which usually lead to poor estimation quality and consequently inaccurate gradient correction vectors in [\[eq:general-grad-est\]](#eq:general-grad-est){reference-type="eqref" reference="eq:general-grad-est"} when the query budget is very limited. Secondly, although ${\bm{x}}_{r,t-1}^{\smash{(i)}}$ changes during local updates, existing algorithms typically rely on ${\bm{g}}_{r-1}, {\bm{g}}_{r-1}^{\smash{(i)}}$ evaluated at a fixed input ${\bm{x}}_{r-1}={\bm{x}}'={\bm{x}}''$ to estimate $\nabla F$ or $\nabla f_i$ (e.g., [@fedprox; @scaffold]), leading to large discrepancies between ${\bm{x}}^{\smash{(i)}}_{r,t-1}$ and ${\bm{x}}',{\bm{x}}''$. Thirdly, existing algorithms use a fixed gradient correction length (e.g., $\gamma_{r,t-1}^{\smash{(i)}}=0$ in [@fedzo] and $\gamma_{r,t-1}^{\smash{(i)}}=1$ in [@scaffold]), which is likely to result in misspecified gradient correction length during optimization.

# FZooS Algorithm {#sec:fzoos}

To address the aforementioned challenges, we propose our *[f]{.underline}ederated [z]{.underline}eroth-[o]{.underline}rder [o]{.underline}ptimization using trajectory-informed [s]{.underline}urrogate gradients* (FZooS) algorithm in Algo. [1](#alg:fzoos){reference-type="ref" reference="alg:fzoos"}, which improves the query and communication efficiency of existing algorithms thanks to our two major contributions, correspondingly. Firstly, we introduce the *trajectory-informed derived Gaussian Process* in [@zord] as local gradient surrogates for query-efficient gradient estimations (Sec. [4.1](#sec:local-surrogates){reference-type="ref" reference="sec:local-surrogates"}). Secondly, we use *random Fourier features* (RFF) approximation [@rahimi2007random] to attain a transferable global gradient surrogate that can accurately estimate the gradient of the global function (Sec. [4.2.1](#sec:global-surrogates){reference-type="ref" reference="sec:global-surrogates"}); based on these surrogates, we then develop the technique of *adaptive gradient correction* with both adaptive gradient correction vector and length to mitigate the disparity between our local updates and the intended global updates (Sec. [4.2.2](#sec:adaptive-est){reference-type="ref" reference="sec:adaptive-est"}), which thus lead to communication-efficient federated ZOO.

## Trajectory-Informed Gradient Estimation for Query Efficiency {#sec:local-surrogates}

Of note, we assumed that $f_i \sim \mathcal{GP}(\mu(\cdot), k(\cdot, \cdot)),\forall i \in [N]$ (Sec. [2](#sec:setting){reference-type="ref" reference="sec:setting"}). Then, in iteration $t$ of communication round $r$ (Algo. [1](#alg:fzoos){reference-type="ref" reference="alg:fzoos"}), conditioned on the optimization trajectory ${\mathcal{D}}^{\smash{(i)}}_{r, t-1} \triangleq \{({\bm{x}}^{\smash{(i)}}_{\tau}, y^{\smash{(i)}}_{\tau})\}_{\tau=1}^{T(r-1)+t-1}$ of client $i$,[^3] $\nabla f_i$ follows a *derived posterior Gaussian Process* [@zord]: $$\begin{equation}
\nabla f_i \sim \mathcal{GP}\Big(\nabla\mu^{(i)}_{r, t-1}(\cdot), \partial \left(\sigma^{(i)}_{r, t-1}\right)^2(\cdot, \cdot)\Big)
\label{eq:derived-gp}
\end{equation}$$ where the mean function $\nabla \mu^{\smash{(i)}}_{r, t-1}({\bm{x}})$ and the covariance function $\partial (\sigma^{\smash{(i)}}_{r, t-1})^2({\bm{x}}, {\bm{x}}')$ are defined as $$\begin{equation}
\begin{aligned}
    \nabla \mu^{(i)}_{r, t-1}({\bm{x}}) &\triangleq \partial_{{\bm{x}}} {\bm{k}}^{(i)}_{r, t-1}({\bm{x}})^{\top}\left({\mathbf{K}}^{(i)}_{r, t-1}+\sigma^2{\mathbf{I}}\right)^{-1}{\bm{y}}^{(i)}_{r, t-1} \ , \\
    \partial \left(\sigma^{(i)}_{r, t-1}\right)^2({\bm{x}}, {\bm{x}}') &\triangleq  \partial_{{\bm{x}}}\partial_{{\bm{x}}'} k({\bm{x}}, {\bm{x}}') - \partial_{{\bm{x}}} {\bm{k}}^{(i)}_{r, t-1}({\bm{x}})^{\top}\left({\mathbf{K}}^{(i)}_{r, t-1}+\sigma^{2} {\mathbf{I}}\right)^{-1} \partial_{{\bm{x}}'} {\bm{k}}^{(i)}_{r, t-1}({\bm{x}}') \ . \label{eq:posterior-derived}
\end{aligned}
\end{equation}$$ Both ${\bm{k}}^{\smash{(i)}}_{r, t-1}({\bm{x}})^{\top} \triangleq [k({\bm{x}}, {\bm{x}}^{\smash{(i)}}_{\tau})]_{\tau=1}^{\smash{T(r-1)+t-1}}$ and $({\bm{y}}^{\smash{(i)}}_{r, t-1})^{\top} \triangleq [y^{\smash{(i)}}_{\tau}]_{\tau=1}^{\smash{T(r-1)+t-1}}$ are $[T(r-1)+t-1]$-dimensional row vectors, and $\displaystyle {\mathbf{K}}^{\smash{(i)}}_{r, t-1} \triangleq [k({\bm{x}}^{\smash{(i)}}_{\tau}, {\bm{x}}^{\smash{(i)}}_{\tau'})]_{\tau,\tau'=1}^{T(r-1)+t-1}$ is a $[T(r-1)+t-1]\times [T(r-1)+t-1]$-dimensional matrix.

We propose to use the posterior mean $\nabla \mu^{\smash{(i)}}_{r, t-1}({\bm{x}})$ [\[eq:posterior-derived\]](#eq:posterior-derived){reference-type="eqref" reference="eq:posterior-derived"} as the local gradient surrogate for client $i$ since it is a prediction of the gradient $\nabla f_i({\bm{x}})$, and $\partial (\sigma^{\smash{(i)}}_{r, t-1})^2({\bm{x}})\triangleq \partial (\sigma^{\smash{(i)}}_{r, t-1})^2({\bm{x}}, {\bm{x}})$ provides a principled uncertainty measure for this gradient surrogate [@zord]. Of note, our gradient surrogate only requires the optimization trajectory (i.e., the history of function queries ${\mathcal{D}}^{\smash{(i)}}_{r, t-1}$ till iteration $t-1$ of round $r$) and thus *eliminates the need for additional queries* required by the FD methods adopted by existing federated ZOO (Sec. [3.2](#sec:challenges){reference-type="ref" reference="sec:challenges"}). This therefore leads to more query-efficient gradient estimations in federated ZOO. Moreover, the aforementioned uncertainty measure can theoretically guarantee the quality of our gradient estimation, and provide theoretical support for our technique of using active queries to further improve the local gradient estimations (Sec. [5.1](#sec:est-analysis){reference-type="ref" reference="sec:est-analysis"}).

## High-Quality Gradient Correction for Communication Efficiency

### Transferable Global Gradient Surrogate {#sec:global-surrogates}

Of note, our local gradient surrogates from Sec. [4.1](#sec:local-surrogates){reference-type="ref" reference="sec:local-surrogates"} can produce not only query-efficient but also accurate gradient estimations [@zord]. So, these local surrogates can be used to construct an accurate global gradient surrogate, which then satisfies requirement [\[com:1\]](#com:1){reference-type="ref" reference="com:1"} for communication-efficient federated ZOO from Sec. [3.2](#sec:challenges){reference-type="ref" reference="sec:challenges"}: accurate local and global gradient surrogates. Unfortunately, due to the non-parametric nature of Gaussian processes, [\[eq:derived-gp\]](#eq:derived-gp){reference-type="eqref" reference="eq:derived-gp"} cannot be transferred to the server without sending the raw observations. To this end, we introduce the idea of *random Fourier features* (RFF) approximation from [@rahimi2007random] to approximate the mean of [\[eq:derived-gp\]](#eq:derived-gp){reference-type="eqref" reference="eq:derived-gp"} and then transfer this approximated mean to server for the construction of high-quality global gradient surrogate.

We firstly approximate the mean of [\[eq:derived-gp\]](#eq:derived-gp){reference-type="eqref" reference="eq:derived-gp"} on each client $i \in [N]$ to ease its transfer between the clients and the server. Since $k(\cdot,\cdot)$ is assumed to be shift-invariant, it can be approximated by a finite number of random features [@rahimi2007random]. That is, we have that $k({\bm{x}},{\bm{x}}') \approx \phi({\bm{x}})^{\top}\phi({\bm{x}}')$ where $\phi({\bm{x}}) \in {\mathbb{R}}^{M}$ contains $M$ random features defined before optimization and is shared across all clients and the server (Appx. [9](#app-sec:rff){reference-type="ref" reference="app-sec:rff"}). By incorporating this approximation into [\[eq:posterior-derived\]](#eq:posterior-derived){reference-type="eqref" reference="eq:posterior-derived"}, the local gradient surrogates on each client $i$ at the end of every round $r$ (i.e., $\nabla \mu^{\smash{(i)}}_{r, T}({\bm{x}})$) can then be approximated as $$\begin{equation}
    \nabla \widehat{\mu}^{(i)}_{r, T}({\bm{x}}) \triangleq \nabla \phi({\bm{x}})^{\top} {\bm{\Phi}}^{(i)}_{r, T}\left(\widehat{{\mathbf{K}}}^{(i)}_{r, T}+\sigma^2{\mathbf{I}}\right)^{-1}{\bm{y}}^{(i)}_{r, T} \label{eq:local-surrogate-approx}
\end{equation}$$ where $\nabla \phi({\bm{x}})$ is an $M \times d$-dimensional matrix, ${\bm{\Phi}}^{\smash{(i)}}_{r, T} \triangleq [\phi({\bm{x}}^{\smash{(i)}}_{\tau})]_{\tau=1}^{rT}$ is an $M \times rT$-dimensional matrix, and $\displaystyle \widehat{{\mathbf{K}}}^{\smash{(i)}}_{r, T} \triangleq [\phi({\bm{x}}^{\smash{(i)}}_{\tau})^{\top} \phi({\bm{x}}^{\smash{(i)}}_{\tau'})]_{\tau,\tau'=1}^{rT}$ is an $rT \times rT$-dimensional matrix. Define an $M$-dimensional column vector ${\bm{w}}_{r,T}^{\smash{(i)}} \triangleq {\bm{\Phi}}^{\smash{(i)}}_{r, T}(\widehat{{\mathbf{K}}}^{\smash{(i)}}_{r, T}+\sigma^2{\mathbf{I}})^{-1}{\bm{y}}^{\smash{(i)}}_{r, T}$, [\[eq:local-surrogate-approx\]](#eq:local-surrogate-approx){reference-type="eqref" reference="eq:local-surrogate-approx"} can be rewritten as $\nabla \widehat{\mu}^{\smash{(i)}}_{r, t-1}({\bm{x}}) = \nabla \phi({\bm{x}})^{\top} {\bm{w}}_{r,T}^{\smash{(i)}}$ (line 8 of Algo. [1](#alg:fzoos){reference-type="ref" reference="alg:fzoos"}). So, each client only needs to calculate and send the $M$-dimensional vector ${\bm{w}}_{r,T}^{\smash{(i)}}$ to the server for constructing the global gradient surrogate (line 9 of Algo. [1](#alg:fzoos){reference-type="ref" reference="alg:fzoos"}).

After receiving $\{{\bm{w}}_{r,T}^{\smash{(i)}}\}_{i=1}^N$ from all clients, the server can construct the global gradient surrogate at the end of every round $r$ by averaging the local gradient surrogates [\[eq:local-surrogate-approx\]](#eq:local-surrogate-approx){reference-type="eqref" reference="eq:local-surrogate-approx"} from all clients, i.e., $$\begin{equation}
    \nabla \widehat{\mu}_r({\bm{x}}) \triangleq \frac{1}{N} {\textstyle\sum}_{i\in[N]} \widehat{\mu}^{(i)}_{r, T}({\bm{x}}) = \nabla \phi({\bm{x}})^{\top}\Big(\frac{1}{N} {\textstyle\sum}_{i\in[N]}{\bm{w}}_{r,T}^{(i)}\Big) \ . \label{eq:global-surrogate}
\end{equation}$$ To transfer this global gradient surrogate to clients, we only need to send the $M$-dimensional vector ${\bm{w}}_r \triangleq \frac{1}{N} \sum_{i=1}^N {\bm{w}}_{r,T}^{\smash{(i)}}$ back (lines 10-11 of Algo. [1](#alg:fzoos){reference-type="ref" reference="alg:fzoos"}). Importantly, after receiving ${\bm{w}}_r$ from the server, each client can calculate the global gradient surrogate *at any input in the domain*. Although this global gradient surrogate incurs an additional transmission of $M$-dimensional vectors compared with existing federated ZOO algorithms (Algo. [\[alg:fedzoo\]](#alg:fedzoo){reference-type="ref" reference="alg:fedzoo"}), it enjoys the advantage of achieving an improved gradient correction with theoretical guarantees (Sec. [5.1](#sec:est-analysis){reference-type="ref" reference="sec:est-analysis"}), which is known to be essential for addressing federated ZOO with heterogeneous clients (Sec. [3.2](#sec:challenges){reference-type="ref" reference="sec:challenges"}) and is thus able to outweigh its drawback of increased transmission burden in practice. To further improve the quality of this surrogate, we can actively query in the neighbourhood of the updated input ${\bm{x}}_{r}$ on every client (line 7 of Algo. [1](#alg:fzoos){reference-type="ref" reference="alg:fzoos"}) as supported in Sec. [5.1](#sec:est-analysis){reference-type="ref" reference="sec:est-analysis"}. This incurs an additional server-clients transmission because the transmission of the gradient surrogates via ${\bm{w}}^{\smash{(i)}}_{r, T}$ needs to happen after the active queries (i.e., after the gradient surrogates are improved), which is consistent with SCAFFOLD (Type ) [@scaffold]. Without active queries, only one transmission is needed because lines 7 and 9 in Algo. [1](#alg:fzoos){reference-type="ref" reference="alg:fzoos"} can be executed simultaneously.

### Adaptive Gradient Correction {#sec:adaptive-est}

By exploiting our aforementioned high-quality local and global gradient surrogates, we then develop the technique of adaptive gradient correction to meet requirement [\[com:2\]](#com:2){reference-type="ref" reference="com:2"} for communication-efficient federated ZOO from Sec. [3.2](#sec:challenges){reference-type="ref" reference="sec:challenges"}. Specifically, thanks to the ability of our gradient surrogates to *estimate the gradient at any input in the domain*, we can let ${\bm{x}}'={\bm{x}}''={\bm{x}}^{\smash{(i)}}_{r,t-1}$ in [\[eq:general-grad-est\]](#eq:general-grad-est){reference-type="eqref" reference="eq:general-grad-est"} to realize a more accurate gradient correction vector during optimization. Moreover, we propose to employ an adaptive gradient correction length $\gamma_{r, t-1}$ (shared across all clients) to better trade off the utilization of our gradient correction vector during optimization.

That is, for every iteration $t$ of round $r$, we propose to use the following $\widehat{{\bm{g}}}^{\smash{(i)}}_{r,t-1}$ on each client $i \in [N]$ (i.e., line 6 of Algo. [1](#alg:fzoos){reference-type="ref" reference="alg:fzoos"}): $$\begin{equation}
    \widehat{{\bm{g}}}^{(i)}_{r,t-1} = \nabla \mu_{r,t-1}^{(i)}({\bm{x}}^{(i)}_{r,t-1}) + \gamma_{r, t-1} \left(\nabla \widehat{\mu}_{r-1}({\bm{x}}^{(i)}_{r,t-1}) - \nabla \widehat{\mu}_{r-1, T}^{(i)}({\bm{x}}^{(i)}_{r,t-1})\right)  \ , \label{eq:fzoos-grad-est}
\end{equation}$$ in which $\nabla \widehat{\mu}_{r-1, T}^{(i)}$ is the local gradient surrogate of client $i$ with RFF approximation at the end of round $r-1$ from [\[eq:local-surrogate-approx\]](#eq:local-surrogate-approx){reference-type="eqref" reference="eq:local-surrogate-approx"}, $\nabla \widehat{\mu}_{r-1}$ is our global gradient surrogate from [\[eq:global-surrogate\]](#eq:global-surrogate){reference-type="eqref" reference="eq:global-surrogate"}, and $\gamma_{r, t-1}$ is a theoretically inspired adaptive gradient correction length which we will discuss in Sec. [5.1](#sec:est-analysis){reference-type="ref" reference="sec:est-analysis"}. Of note, the advantage of this adaptive gradient correction can be theoretically justified (Sec. [5.1](#sec:est-analysis){reference-type="ref" reference="sec:est-analysis"}).

# Theoretical Analysis {#sec:analysis}

In this section, we present our theoretical analysis on the gradient disparity of our local gradient update [\[eq:fzoos-grad-est\]](#eq:fzoos-grad-est){reference-type="eqref" reference="eq:fzoos-grad-est"} in Sec. [5.1](#sec:est-analysis){reference-type="ref" reference="sec:est-analysis"} and the convergence of our FZooS (Algo. [1](#alg:fzoos){reference-type="ref" reference="alg:fzoos"}) in Sec. [5.2](#sec:conv-analysis){reference-type="ref" reference="sec:conv-analysis"}.

## Gradient Disparity Analysis {#sec:est-analysis}

We assume that $\frac{1}{N}\sum_{i=1}^N \left\|\nabla f_i({\bm{x}}) - \nabla F({\bm{x}})\right\|^2 \leq G$ for any ${\bm{x}}\in {\mathcal{X}}$, which is a common assumption in the analysis of federated optimization [@adap-fed]. Here a larger $G$ indicates a larger degree of client heterogeneity. By making use of the uncertainty measure from [\[eq:posterior-derived\]](#eq:posterior-derived){reference-type="eqref" reference="eq:posterior-derived"}, we derive an upper bound on the gradient disparity of our [\[eq:fzoos-grad-est\]](#eq:fzoos-grad-est){reference-type="eqref" reference="eq:fzoos-grad-est"} in Thm. [1](#th:grad-error){reference-type="ref" reference="th:grad-error"} below (proof in Appx. [10.2](#app-sec:proof:grad-error){reference-type="ref" reference="app-sec:proof:grad-error"}).

::: {#th:grad-error .theorem}
**Theorem 1**. *Define $\rho_i \triangleq \max_{{\bm{x}}\in {\mathcal{X}}, r\geq 1, t\geq 1} \big\|\partial (\sigma^{\smash{(i)}}_{r,t})^2({\bm{x}})\big\| / \big\|\partial \left(\sigma^{\smash{(i)}}_{r,t-1}\right)^2({\bm{x}})\big\|$ and $\rho \triangleq \frac{1}{N}\sum_{i=1}^N \rho_i$,*

*$\rho, \rho_i {\in} [\frac{1}{1+1/\sigma^2}, 1]$. Given constant $\omega{>}0$ and ${\epsilon}={\mathcal{O}}(\frac{1}{M})$, the following holds with constant probability $$\begin{equation*}
    \frac{1}{N} \sum_{i\in[N]} \Xi_{r,t}^{(i)} \leq \underbrace{4\omega\kappa \rho^{(r-1)T+t-1}}_{\normalfont \tikz[baseline=(char.base)]{\node[shape=circle,draw,inner sep=0.2pt] (char) {1};}} + \gamma^2_{r, t-1}\underbrace{(8\omega\kappa \rho^{(r-1)T}  + 8N{\epsilon})}_{\normalfont \tikz[baseline=(char.base)]{\node[shape=circle,draw,inner sep=0.2pt] (char) {2};}} + (1 - \gamma_{r, t-1})^2\underbrace{4G}_{\normalfont \tikz[baseline=(char.base)]{\node[shape=circle,draw,inner sep=0.2pt] (char) {3};}} \ . \label{eq:trade-off}
\end{equation*}$$*
:::

::: {#co:better-gamma .corollary}
**Corollary 1**. *Thm. [1](#th:grad-error){reference-type="ref" reference="th:grad-error"} implies a better-performing choice of $\gamma_{r,t-1}$, i.e., $\gamma_{r,t-1} = \frac{G}{G + 2\omega\kappa\rho^{(r-1)T} + 2N{\epsilon}}$.*
:::

In the upper bound of Thm. [1](#th:grad-error){reference-type="ref" reference="th:grad-error"}, term $\tikz[baseline=(char.base)]{\node[shape=circle,draw,inner sep=0.2pt] (char) {1};}$ represents the error of estimating $\{\nabla f_i(\cdot)\}_{i=1}^N$ using our local gradient surrogates in Sec. [4.1](#sec:local-surrogates){reference-type="ref" reference="sec:local-surrogates"}, and term $\tikz[baseline=(char.base)]{\node[shape=circle,draw,inner sep=0.2pt] (char) {2};}$ characterizes the disparity between our gradient correction vector in [\[eq:fzoos-grad-est\]](#eq:fzoos-grad-est){reference-type="eqref" reference="eq:fzoos-grad-est"} and its corresponding ground truth $\{\nabla F(\cdot) - \nabla f_i(\cdot)\}_{i=1}^N$. The ${\epsilon}$ within term $\tikz[baseline=(char.base)]{\node[shape=circle,draw,inner sep=0.2pt] (char) {2};}$ denotes the RFF approximation error for our global gradient surrogate in Sec. [4.2.1](#sec:global-surrogates){reference-type="ref" reference="sec:global-surrogates"} and ${\epsilon}$ decreases with a larger number $M$ of random features. Term $\tikz[baseline=(char.base)]{\node[shape=circle,draw,inner sep=0.2pt] (char) {3};}$ results from the client heterogeneity in federated ZOO. Compared with the gradient disparity of existing algorithms (provided in Appx. [11](#app-sec:existing){reference-type="ref" reference="app-sec:existing"}), Thm. [1](#th:grad-error){reference-type="ref" reference="th:grad-error"} shows that our [\[eq:fzoos-grad-est\]](#eq:fzoos-grad-est){reference-type="eqref" reference="eq:fzoos-grad-est"} enjoys a number of major advantages: ***(a)*** Our [\[eq:fzoos-grad-est\]](#eq:fzoos-grad-est){reference-type="eqref" reference="eq:fzoos-grad-est"} is more query-efficient since it does not require any additional function query for gradient estimation, in contrast to existing algorithms which incur ${\mathcal{O}}(NQ)$ additional function queries in every iteration. ***(b)*** The estimation error in our [\[eq:fzoos-grad-est\]](#eq:fzoos-grad-est){reference-type="eqref" reference="eq:fzoos-grad-est"} (i.e., terms $\tikz[baseline=(char.base)]{\node[shape=circle,draw,inner sep=0.2pt] (char) {1};}$ and $\tikz[baseline=(char.base)]{\node[shape=circle,draw,inner sep=0.2pt] (char) {2};}$) can be exponentially decreasing when $\rho<1$ and ${\epsilon}$ is small, whereas other existing algorithms only achieve a reduction rate of ${\mathcal{O}}(1/Q)$, which implies that our gradient estimation is significantly more accurate. Of note, $\rho_i<1$ is likely to be satisfied as justified in [@zord] and more importantly, $\rho<1$ is even easier to be realized as it only needs one of the clients to satisfy $\rho_i<1$. ***(c)*** Our [\[eq:fzoos-grad-est\]](#eq:fzoos-grad-est){reference-type="eqref" reference="eq:fzoos-grad-est"} mitigates the disparity caused by the fixed gradient correction vector adopted by existing works, i.e., in contrast to FedProx and SCAFFOLD, our Thm. [1](#th:grad-error){reference-type="ref" reference="th:grad-error"} does not contain an additional disparity term of $\sum_{i=1}^{\smash{N}} \|{\bm{x}}_{r,t-1}^{\smash{(i)}} - {\bm{x}}_{r-1}\|^2$. ***(d)*** Our [\[eq:fzoos-grad-est\]](#eq:fzoos-grad-est){reference-type="eqref" reference="eq:fzoos-grad-est"} can trade off between the impacts of our gradient correction vector and client heterogeneity, and can consequently urther improve the gradient estimation when $\gamma_{r,t-1}$ is chosen intelligently while accounting for this trade-off. Specifically, the upper bound in Thm. [1](#th:grad-error){reference-type="ref" reference="th:grad-error"} has characterized such a trade-off: When the estimation error of our gradient correction vector (i.e., term $\tikz[baseline=(char.base)]{\node[shape=circle,draw,inner sep=0.2pt] (char) {2};}$) is relatively small compared with the client heterogeneity (i.e., term $\tikz[baseline=(char.base)]{\node[shape=circle,draw,inner sep=0.2pt] (char) {3};}$), a large $\gamma_{t-1}$ is preferred to reduce the impact of client heterogeneity and hence to achieve a small gradient disparity. Furthermore, this also implies a theoretically better choice of $\gamma_{r,t-1}$ in our Cor. [1](#co:better-gamma){reference-type="ref" reference="co:better-gamma"} (refer to Appx. [10.3](#app-sec:prac-gamma){reference-type="ref" reference="app-sec:prac-gamma"} for a more practical choice of $\gamma_{r,t-1}$).

In addition to the theoretical insights above, Thm. [1](#th:grad-error){reference-type="ref" reference="th:grad-error"} also offers valuable insights to enhance the practical efficacy of our [\[eq:fzoos-grad-est\]](#eq:fzoos-grad-est){reference-type="eqref" reference="eq:fzoos-grad-est"}. Firstly, during local updates, we can actively query more function values on each client to further decrease the uncertainty (i.e., $\big\|\partial (\sigma^{\smash{(i)}}_{r,t})^2({\bm{x}})\big\|$) of our local gradient surrogates, which improves our [\[eq:fzoos-grad-est\]](#eq:fzoos-grad-est){reference-type="eqref" reference="eq:fzoos-grad-est"} by decreasing term $\tikz[baseline=(char.base)]{\node[shape=circle,draw,inner sep=0.2pt] (char) {1};}$ in Thm. [1](#th:grad-error){reference-type="ref" reference="th:grad-error"} with a larger exponent. Secondly, after receiving ${\bm{x}}_r$ from the server (i.e., at the end of every round $r$ of our Algo. [1](#alg:fzoos){reference-type="ref" reference="alg:fzoos"}), we can actively query in the neighborhood of ${\bm{x}}_r$ on every client, in order to decrease term $\tikz[baseline=(char.base)]{\node[shape=circle,draw,inner sep=0.2pt] (char) {2};}$ in Thm. [1](#th:grad-error){reference-type="ref" reference="th:grad-error"} using a larger exponent and thus to improve the quality of gradient correction in our [\[eq:fzoos-grad-est\]](#eq:fzoos-grad-est){reference-type="eqref" reference="eq:fzoos-grad-est"}. Thirdly, we can use a large number $M$ of random features to achieve a small RFF approximation error ${\epsilon}$ in term $\tikz[baseline=(char.base)]{\node[shape=circle,draw,inner sep=0.2pt] (char) {2};}$ of Thm. [1](#th:grad-error){reference-type="ref" reference="th:grad-error"}. Fourthly, we can choose an adaptive gradient correction length $\gamma_{r,t-1}$ (e.g., the $\gamma_{r,t-1}$ in Cor. [1](#co:better-gamma){reference-type="ref" reference="co:better-gamma"}) to better trade off the impacts of the gradient correction and client heterogeneity.

## Convergence Analysis {#sec:conv-analysis}

We prove the convergence of our FZooS (measured by the number of communication rounds to achieve ${\epsilon}$ convergence error) under different assumptions, in addition to assuming that $F$ is $\beta$-smooth.

::: {#th:convergence-fzoos .theorem}
**Theorem 2**. *Define $D_0 \triangleq \left\|{\bm{x}}_0 - {\bm{x}}^*\right\|^2$ and $D_1 \triangleq F({\bm{x}}_0) - F({\bm{x}}^*)$, to achieve an ${\epsilon}$ convergence error for our FZooS (Algo. [1](#alg:fzoos){reference-type="ref" reference="alg:fzoos"}) with a constant probability when $\rho<1$, the number $M$ of random features and the number $R$ of communication rounds need to satisfy the following,*

1.  *If $F$ is strongly convex and $\eta \leq\frac{1}{10 \beta T}$, $M = {\mathcal{O}}\left(\frac{NG}{{\epsilon}^2}\right)$ and $R = {\mathcal{O}}\left(\frac{1}{\eta T}\ln\frac{D_0}{{\epsilon}} + \ln\frac{\sqrt{G}}{{\epsilon}}\right)$.*

2.  *If $F$ is convex and $\eta \leq \frac{1}{10 \beta T}$, $M = {\mathcal{O}}\left(\frac{NG}{{\epsilon}^2} + \frac{d^2NG}{{\epsilon}^4}\right)$ and $R = {\mathcal{O}}\left(\frac{D_0}{\eta T{\epsilon}} + \frac{\sqrt{G} + \sqrt[4]{d^2G}}{{\epsilon}}\right)$.*

3.  *If $F$ is non-convex and $\eta \leq \frac{7}{100 \beta T}$, $M = {\mathcal{O}}\left(\frac{NG}{{\epsilon}^2}\right)$ and $R = {\mathcal{O}}\left(\frac{D_1}{\eta T {\epsilon}} + \frac{\sqrt{G}}{{\epsilon}}\right)$.*
:::

The proof is in Appx. [10.5](#app-sec:proof:conv-fzoos){reference-type="ref" reference="app-sec:proof:conv-fzoos"}.[^4] Thm. [2](#th:convergence-fzoos){reference-type="ref" reference="th:convergence-fzoos"} suggests that the learning rate $\eta$ in FZooS should be proportionally reduced w.r.t. the number $T$ of local updates, which is in fact consistent with the results in federated FOO [@scaffold]. Thm. [2](#th:convergence-fzoos){reference-type="ref" reference="th:convergence-fzoos"} also shows that when client heterogeneity (i.e., measured by $G$) increases, both the number $M$ of random features and the number $R$ of communication rounds in our FZooS should be increased in order to achieve the same convergence error, which is also empirically verified in our Sec. [6](#sec:exps){reference-type="ref" reference="sec:exps"} and Appx. [13](#app-sec:more){reference-type="ref" reference="app-sec:more"}. Moreover, Thm. [2](#th:convergence-fzoos){reference-type="ref" reference="th:convergence-fzoos"} has revealed that given a constant learning rate $\eta$ that satisfies the conditions in Thm. [2](#th:convergence-fzoos){reference-type="ref" reference="th:convergence-fzoos"} under various $T$, a larger $T$ usually improves the communication efficiency (i.e., $R$) of our FZooS (see Appx. [13](#app-sec:more){reference-type="ref" reference="app-sec:more"}). More importantly, compared with the convergence of other existing algorithms (provided in Appx. [11](#app-sec:existing){reference-type="ref" reference="app-sec:existing"}), FZooS enjoys an improved communication efficiency in a number of major aspects, which can be attributed to the advantages of our [\[eq:fzoos-grad-est\]](#eq:fzoos-grad-est){reference-type="eqref" reference="eq:fzoos-grad-est"} as discussed in Sec. [5.1](#sec:est-analysis){reference-type="ref" reference="sec:est-analysis"} (see Appx. [11](#app-sec:existing){reference-type="ref" reference="app-sec:existing"} for a detailed comparison).

# Experiments {#sec:exps}

In this section, we demonstrate that our FZooS outperforms existing federated ZOO algorithms using synthetic experiments (Sec. [6.1](#sec:syn){reference-type="ref" reference="sec:syn"}), as well as real-world experiments on federated black-box adversarial attack (Sec. [6.2](#sec:attack){reference-type="ref" reference="sec:attack"}) and federated non-differentiable metric optimization ([6.3](#sec:metric){reference-type="ref" reference="sec:metric"}).

## Synthetic Experiments {#sec:syn}

We firstly employ federated synthetic functions to illustrate the superiority of our proposed FZooS over a number of existing federated ZOO baselines such as FedZO, FedProx, and SCAFFOLD in the federated ZOO setting (see Appx. [11](#app-sec:existing){reference-type="ref" reference="app-sec:existing"} for their specific forms). We refer to Appx. [12.1](#app-sec:setting-syn){reference-type="ref" reference="app-sec:setting-syn"} for the details of these synthetic functions and the experimental setting applied here. Fig. [2](#fig:quadratic){reference-type="ref" reference="fig:quadratic"} provides the results with $d=300$, $N=5$, and varying $C$ to control the client heterogeneity (more results in Appx. [13.1](#app-sec:syn){reference-type="ref" reference="app-sec:syn"}). It shows that our FZooS considerably outperforms the other baselines in terms of both communication and query efficiency, which can be attributed to the superiority of our [\[eq:fzoos-grad-est\]](#eq:fzoos-grad-est){reference-type="eqref" reference="eq:fzoos-grad-est"}. When $C$ is increased, a larger number of communication rounds and total queries is required to achieve the same convergence error, which empirically verifies our Thm. [2](#th:convergence-fzoos){reference-type="ref" reference="th:convergence-fzoos"}. Interestingly, SCAFFOLD (Type ) consistently outperforms SCAFFOLD (Type ) while Type in fact is an approximation of Type in [@scaffold]. This is likely because SCAFFOLD (Type ) achieves improved gradient correction by implicitly increasing the number of additional function queries for a smaller approximation error of $\nabla F$ (refer to Appx. [11](#app-sec:existing){reference-type="ref" reference="app-sec:existing"}). This thus indicates the necessity of achieving an accurate approximation of $\nabla F$ for federated ZOO with heterogeneous clients, which is achieved by our FZooS. Meanwhile, when client heterogeneity is small (i.e., $C\leq5.0$), both FedProx and SCAFFOLD (Type ) perform worse than FedZO which does not apply any gradient correction. This is likely because the impact of the inaccurate gradient correction applied in these two algorithms outweighs that of client heterogeneity as justified in our Appx. [11](#app-sec:existing){reference-type="ref" reference="app-sec:existing"}. This corroborates the importance of developing improved gradient correction for federated ZOO of varying client heterogeneity, which is realized by our FZooS.

:::: {#fig:quadratic .figure latex-placement="t"}
  --------------------------------------------------------------------------------------------------------- ---------------------------------------------------------------------------------------------------------
   ![image](Shu2023Federated_figs/convergence-Quadratic-300,10,div-round.png){width="0.5\\columnwidth"}   ![image](Shu2023Federated_figs/convergence-Quadratic-300,10,div-query.png){width="0.5\\columnwidth"}
  --------------------------------------------------------------------------------------------------------- ---------------------------------------------------------------------------------------------------------

![](Shu2023Federated_figs/legend.png){width="0.57\\columnwidth"}

::: caption
Comparison of the communication and query efficiency between our FZooS and other existing baselines on the federated synthetic functions with varying client heterogeneity (controlled by $C\geq0$), where a larger $C$ implies larger client heterogeneity. The $x$-axes of the first and last three plots are the number of rounds and total queries required by these algorithms. SCAFFOLD (1) and (2) stand for SCAFFOLD (Type ) and SCAFFOLD (Type ) algorithms, respectively.
:::
::::

## Federated Black-Box Adversarial Attack {#sec:attack}

Following the practice of [@fedzo], we then examine the advantages of our FZooS in the task of federated black-box adversarial attack. Here we aim to find a small perturbation ${\bm{x}}$ to be added to an input image ${\bm{z}}$ such that the perturbed image ${\bm{z}}+ {\bm{x}}$ will be wrongly classified by the *majority* of the private ML models on various clients through only the function queries of these models. Specifically, we randomly select 15 images from CIFAR-10 [@cifar] and then attempt to find one single perturbation ( $d=32 \times 32$ ) for every image to make the averaged output of $N=10$ deep neural networks trained using private datasets on different clients misclassify the image using federated ZOO algorithms (refer to Appx. [12.2](#app-sec:setting-attack){reference-type="ref" reference="app-sec:setting-attack"} for more details). Fig. [3](#fig:attack){reference-type="ref" reference="fig:attack"} illustrates the success rates on these 15 images achieved by various federated ZOO algorithms during optimization (more results in Appx. [13.2](#app-sec:attack){reference-type="ref" reference="app-sec:attack"}). Remarkably, our FZooS again achieves consistently improved communication efficiency over the other baselines under varying client heterogeneity. Thanks to this improved communication efficiency and the ability of our [\[eq:fzoos-grad-est\]](#eq:fzoos-grad-est){reference-type="eqref" reference="eq:fzoos-grad-est"} to avoid a large number of additional function queries in every communication round, our FZooS also achieves a substantial improvement in query efficiency. Overall, these results support the superiority of our FZooS over the other existing approaches in real-world federated ZOO problems in terms of both communication and query efficiency.

:::: {#fig:attack .figure latex-placement="t"}
  ------------------------------------------------------------------------------------------------------ ------------------------------------------------------------------------------------------------------
   ![image](Shu2023Federated_figs/convergence-CIFAR10_Attack-div-round-0.png){width="0.5\\columnwidth"}   ![image](Shu2023Federated_figs/convergence-CIFAR10_Attack-div-query-0.png){width="0.5\\columnwidth"}
  ------------------------------------------------------------------------------------------------------ ------------------------------------------------------------------------------------------------------

![](Shu2023Federated_figs/legend.png){width="0.57\\columnwidth"}

::: caption
Comparison of the success rate in federated black-box adversarial attack achieved by FZooS and other existing federated ZOO algorithms on CIFAR-10 under varying client heterogeneity (controlled by $P \in [0,1]$, a larger $P$ implies smaller client heterogeneity). The $x$ and $y$-axis are the number of rounds/queries and the corresponding success rate (higher is better).
:::
::::

## Federated Non-Differentiable Metric Optimization {#sec:metric}

Inspired by [@zord], we lastly demonstrate the superior performance of our FZooS in the task of federated non-differentiable metric optimization, which has received a surging interest recently [@HiranandaniMNFK21; @HuangZGS21]. Specifically, we employ federated ZOO algorithms to fine-tune a fully trained MLP model ($d=2189$) to optimize a non-differentiable metric such as precision and recall, using the Covertype dataset [@Dua19] distributed on $N=7$ clients (refer to Appx. [12.3](#app-sec:setting-metric){reference-type="ref" reference="app-sec:setting-metric"} for more details). This is similar to the widely applied federated learning setting [@federated] whereas the gradient information here is unavailable due to the non-differentiability of these metrics. Fig. [4](#fig:metricopt){reference-type="ref" reference="fig:metricopt"} reports the comparison among various federated ZOO algorithms under varying client heterogeneity (more results in Appx. [13.3](#app-sec:metric){reference-type="ref" reference="app-sec:metric"}). The results show that in the task of federated non-differentiable metric optimization with varying client heterogeneity, our FZooS is still able to consistently outperform the other existing federated ZOO algorithms in terms of both communication and query efficiency, which therefore further substantiates the superiority of our FZooS in optimizing high-dimensional non-differentiable functions in the federated setting.

:::: {#fig:metricopt .figure latex-placement="t"}
  ------------------------------------------------------------------------------------------------------------------- -------------------------------------------------------------------------------------------------------------------
   ![image](Shu2023Federated_figs/convergence-MetricOpt-precision_score-div-round.png){width="0.5\\columnwidth"}   ![image](Shu2023Federated_figs/convergence-MetricOpt-precision_score-div-query.png){width="0.5\\columnwidth"}
  ------------------------------------------------------------------------------------------------------------------- -------------------------------------------------------------------------------------------------------------------

![](Shu2023Federated_figs/legend.png){width="0.57\\columnwidth"}

::: caption
Comparison of the non-differentiable metric optimization between FZooS and other existing federated ZOO algorithms under varying client heterogeneity (controlled by $P \in [0,1]$, a larger $P$ implies smaller client heterogeneity). The $y$-axis is $(1-\text{precision})\times 100\%$ and each curve is the mean $\pm$ standard error from five independent runs.
:::
::::

# Conclusion and Discussion

In this paper, we first identify the non-trivial challenges of query and communication inefficiency faced by federated ZOO algorithms in the presence of client heterogeneity (Sec. [3](#sec:framework&challenge){reference-type="ref" reference="sec:framework&challenge"}) and then introduce our FZooS algorithm to address these challenges (Sec. [4](#sec:fzoos){reference-type="ref" reference="sec:fzoos"}). We employ both theoretical justifications (Sec. [5](#sec:analysis){reference-type="ref" reference="sec:analysis"}) and empirical demonstrations (Sec. [6](#sec:exps){reference-type="ref" reference="sec:exps"}) to show that FZooS is indeed able to address these challenges and consequently to achieve considerably improved query and communication efficiency over the existing federated ZOO algorithms. Of note, the limitation of our FZooS lies in two major aspects. Firstly, as discussed in Sec. [4.2.1](#sec:global-surrogates){reference-type="ref" reference="sec:global-surrogates"}, FZooS incurs an additional transmission of $M$-dimensional vectors for every communication round compared with existing algorithms, which is acceptable given a high-speed transmission between clients and server. Secondly, it will be hard for FZooS to solve extremely high-dimensional federated ZOO problems (e.g., the model training of neural networks with millions/billions of parameters) due to the restrictive modeling capacity of GP where a promising solution is to use neural networks as the GPs of compelling representation power [@sto-bnts; @fed-neural-bandit].

:::::::::::::::::::::::::::::::::::::::::::::: appendices
# Related Work

#### Federated Learning and Federated First-Order Optimization.

Federated learning (FL) has become a paradigm of applying multiple edge devices (i.e., clients) to collaboratively train a global model without sharing the private data on these edge devices [@federated]. We refer to the surveys [@fl-chanllenges; @fl-advance] for more comprehensive reviews of FL. Such a paradigm then gives rise to recent interest in federated optimization or more precisely federated first-order optimization (FOO) [@wang2021field] to broaden its real-world application. Since the first federated FOO algorithm FedAvg proposed in [@fedavg], a number of techniques have been developed to further improve its performance in different aspects, e.g., federated FOO with momentum [@mom-fed] and adaptive learning rates [@adap-fed; @acce-fed; @deco-fed] for convergence speedup, federated FOO with local posterior sampling for de-biased client updates [@fedpa], and federated FOO with regularized functions [@fedprox; @feddane] and control variates [@scaffold; @mime] for the challenge of heterogeneous clients, in which the global function to be optimized differs from the local functions on clients.

#### Federated Zeroth-Order Optimization.

Despite the success of federated FOO algorithms, some important applications, e.g., federated black-box adversarial attack in [@fedzo], suggests the development of federated zeroth-order (ZOO) algorithms for the federated optimization where gradient information is not available. Nevertheless, very limited efforts have been devoted to the development of federated zeroth-order (ZOO) algorithms especially when the clients are heterogeneous. To the best of our knowledge, @fedzo are the first to consider federated ZOO, in which they simply combine FedAvg with existing FD methods as their FedZO algorithm. Similar to the FedAvg algorithm in federated FOO, the FedZO algorithm also likely performs poorly in the heterogeneous setting. This thus encourages the design of federated ZOO algorithms for heterogeneous federated ZOO problems. Following the practice of FedZO, existing federated FOO algorithms for heterogeneous clients, e.g., [@fedprox; @scaffold], can be simply adapted to the corresponding federated ZOO algorithms for this kind of problem. However, these algorithms shall be query- and communication-inefficient in practice, which therefore raises the question of how to improve query efficiency and the communication efficiency of these algorithms. To answer this question, we first identify the challenges of such an improvement and then develop a federated ZOO algorithm to overcome these challenges in this paper.

# Random Fourier Features {#app-sec:rff}

According to [@rahimi2007random], the random Fourier features can usually be represented as a $M$-dimensional row vector $\phi({\bm{x}})^{\top} = \left[\frac{2}{\sqrt{M}} \cos({\bm{v}}_j {\bm{x}}+ b_j)\right]_{j=1}^M$ where every ${\bm{v}}_j$ is independently randomly sampled from a distribution $p({\bm{v}})$ and every $b_j$ is independently randomly sampled from the uniform distribution over $[0,2\pi]$. Particularly, for the squared exponential kernel $k({\bm{x}},{\bm{x}}') = \exp\left(-\left\|{\bm{x}}- {\bm{x}}'\right\|^2 / (2l^2)\right)$ in which $l$ is the length scale, $p({\bm{v}}) = {\mathcal{N}}(0, \frac{1}{l^2}{\mathbf{I}})$. In FZooS, we typically adopt the squared exponential kernel for the optimization. Importantly, before the start of our FZooS, $\{{\bm{v}}_j\}_{j=1}^M$ and $\{b_j\}_{j=1}^M$ need to be sampled and shared across all clients as well as server (as mentioned in Sec. [4.2.1](#sec:global-surrogates){reference-type="ref" reference="sec:global-surrogates"}), which however will only happen once for whole optimization process.

# Theoretical Analyses

## Proof of Proposition [1](#prop:opt-correction){reference-type="ref" reference="prop:opt-correction"} {#app-sec:proof:prop:opt-correction}

Based on the definition of $\Xi^{\smash{(i)}}_{r,t}$ in Sec. [3.2](#sec:challenges){reference-type="ref" reference="sec:challenges"}, we have that $$\begin{equation}
\begin{aligned}
    \Xi^{\smash{(i)}}_{r,t} &= \left\|\widehat{{\bm{g}}}^{(i)}_{r,t-1} - \nabla F({\bm{x}}^{(i)}_{r,t-1})\right\|^2 \\
    &= \left\|{\bm{g}}_{r,t-1}^{(i)} + \gamma_{r,t-1}^{(i)} \left({\bm{g}}_{r-1}({\bm{x}}') - {\bm{g}}_{r-1}^{(i)}({\bm{x}}'')\right) - \nabla F({\bm{x}}^{(i)}_{r,t-1})\right\|^2\\
    &= \left\|{\bm{g}}_{r,t-1}^{(i)} - \nabla F({\bm{x}}^{(i)}_{r,t-1})\right\|^2 - 2\gamma_{r,t-1}^{(i)}\left(\nabla F({\bm{x}}^{(i)}_{r,t-1}) - {\bm{g}}_{r,t-1}^{(i)}\right)^{\top}\left({\bm{g}}_{r-1}({\bm{x}}') - {\bm{g}}_{r-1}^{(i)}({\bm{x}}'')\right) + \\
    &\qquad\qquad \left(\gamma_{r,t-1}^{(i)}\right)^2\left\|{\bm{g}}_{r-1}({\bm{x}}') - {\bm{g}}_{r-1}^{(i)}({\bm{x}}'')\right\|^2 \ ,
\end{aligned}
\end{equation}$$ which is a quadratic function w.r.t. $\gamma_{r,t-1}^{(i)}$. It is easy to show that when $$\begin{equation}
    \gamma_{r,t-1}^{(i)} = \gamma_{r,t-1}^{(i)*} \triangleq \frac{\left(\nabla F({\bm{x}}^{(i)}_{r,t-1}) - {\bm{g}}_{r,t-1}^{(i)}\right)^{\top}\left({\bm{g}}_{r-1}({\bm{x}}') - {\bm{g}}_{r-1}^{(i)}({\bm{x}}'')\right)}{\left\|{\bm{g}}_{r-1}({\bm{x}}') - {\bm{g}}_{r-1}^{(i)}({\bm{x}}'')\right\|} \ , \label{eq:temp-savx}
\end{equation}$$ $\Xi^{(i)}_{r,t}$ can achieve its global minimum w.r.t. $\gamma_{r,t-1}^{(i)}$ as $$\begin{equation}
    \Xi^{\smash{(i)}}_{r,t} = \left\|{\bm{g}}_{r,t-1}^{(i)} - \nabla F({\bm{x}}^{(i)}_{r,t-1})\right\|^2 - \frac{\left\|\left(\nabla F({\bm{x}}^{(i)}_{r,t-1}) - {\bm{g}}_{r,t-1}^{(i)}\right)^{\top}\left({\bm{g}}_{r-1}({\bm{x}}') - {\bm{g}}_{r-1}^{(i)}({\bm{x}}'')\right)\right\|^2}{\left\|{\bm{g}}_{r-1}({\bm{x}}') - {\bm{g}}_{r-1}^{(i)}({\bm{x}}'')\right\|^2} \ . \label{eq:temp-bvud}
\end{equation}$$ This therefore finishes the proof of the fist-part result in Prop. [1](#prop:opt-correction){reference-type="ref" reference="prop:opt-correction"}. Interestingly, [\[eq:temp-bvud\]](#eq:temp-bvud){reference-type="eqref" reference="eq:temp-bvud"} implies that given the $\gamma_{r,t-1}^{(i)}$ in [\[eq:temp-savx\]](#eq:temp-savx){reference-type="eqref" reference="eq:temp-savx"}, a better alignment between the gradient correction vector ${\bm{g}}_{r-1}({\bm{x}}') - {\bm{g}}_{r-1}^{(i)}({\bm{x}}'')$ and the shift $\nabla F({\bm{x}}^{(i)}_{r,t-1}) - {\bm{g}}_{r,t-1}^{(i)}$ leads to a smaller gradient disparity $\Xi^{(i)}_{r,t}$.

Given the $\gamma_{r,t-1}^{(i)*}=1$ in [\[eq:temp-savx\]](#eq:temp-savx){reference-type="eqref" reference="eq:temp-savx"}, when ${\bm{g}}_{r-1}({\bm{x}}') - {\bm{g}}_{r-1}^{(i)}({\bm{x}}'') = \nabla F({\bm{x}}^{(i)}_{r,t-1}) - {\bm{g}}_{r,t-1}^{(i)}$, we can easily verify that $\Xi^{(i)}_{r,t}$ in [\[eq:temp-savx\]](#eq:temp-savx){reference-type="eqref" reference="eq:temp-savx"} has $\Xi^{(i)}_{r,t}=0$. On the contrary, when $\Xi^{(i)}_{r,t}=0$, we have that $$\begin{equation}
    \left\|{\bm{g}}_{r,t-1}^{(i)} - \nabla F({\bm{x}}^{(i)}_{r,t-1})\right\| = \frac{\left\|\left(\nabla F({\bm{x}}^{(i)}_{r,t-1}) - {\bm{g}}_{r,t-1}^{(i)}\right)^{\top}\left({\bm{g}}_{r-1}({\bm{x}}') - {\bm{g}}_{r-1}^{(i)}({\bm{x}}'')\right)\right\|}{\left\|{\bm{g}}_{r-1}({\bm{x}}') - {\bm{g}}_{r-1}^{(i)}({\bm{x}}'')\right\|} \ , \label{eq:tem-ceiv}
\end{equation}$$ which implies that $\nabla F({\bm{x}}^{(i)}_{r,t-1}) - {\bm{g}}_{r,t-1}^{(i)}$ and ${\bm{g}}_{r-1}({\bm{x}}') - {\bm{g}}_{r-1}^{(i)}({\bm{x}}'')$ are linear dependent according to the Cauchy-Schwarz inequality. Since $\gamma_{r,t-1}^{(i)*}=1$, we further have $$\begin{equation}
    \left\|\nabla F({\bm{x}}^{(i)}_{r,t-1}) - {\bm{g}}_{r,t-1}^{(i)}\right\| = \left\|{\bm{g}}_{r-1}({\bm{x}}') - {\bm{g}}_{r-1}^{(i)}({\bm{x}}'')\right\| \ . \label{eq:temp-fiewn}
\end{equation}$$ These two results, i.e., [\[eq:tem-ceiv\]](#eq:tem-ceiv){reference-type="eqref" reference="eq:tem-ceiv"} and [\[eq:temp-fiewn\]](#eq:temp-fiewn){reference-type="eqref" reference="eq:temp-fiewn"} thus imply that $\nabla F({\bm{x}}^{(i)}_{r,t-1}) - {\bm{g}}_{r,t-1}^{(i)} = {\bm{g}}_{r-1}({\bm{x}}') - {\bm{g}}_{r-1}^{(i)}({\bm{x}}'')$, which therefore concludes our proof.

## Proof of Theorem [1](#th:grad-error){reference-type="ref" reference="th:grad-error"} {#app-sec:proof:grad-error}

### Gradient Estimation Error Using Uncertainty

We introduce the following lemma that is adapted from [@zord] to bound the estimation error of our local gradient surrogates using the uncertainty measure in our [\[eq:posterior-derived\]](#eq:posterior-derived){reference-type="eqref" reference="eq:posterior-derived"}.

::: {#le:confidence-bound .lemma}
**Lemma 1**. *Let $\delta \in (0,1)$ and $\omega \triangleq d + 2(\sqrt{d}+1)\ln(1/\delta)$. For any ${\bm{x}}\in {\mathcal{X}}$, $i \in [N]$, $r\geq1$ and $t\geq 1$, the following holds with probability of at least $1-\delta$, $$\begin{equation*}
\vspace{-0.5mm}
\begin{aligned}
\left\|\nabla \mu^{(i)}_{r,t}({\bm{x}}) - \nabla f_i({\bm{x}})\right\|^2 \leq 
\omega \left\|\partial \left(\sigma^{(i)}_{r,t}\right)^2({\bm{x}})\right\| \ .
\end{aligned}
\end{equation*}$$*
:::

### RFF Approximation Error for Global Gradient Surrogate

::: {#le:chi-square .lemma}
**Lemma 2** (@laurent2000adaptive). *If ${\textnormal{x}}_1,\cdots,{\textnormal{x}}_k$ are independent standard normal random variables, for ${\textnormal{y}}=\sum_{i=1}^k {\textnormal{x}}_i^2$ and any ${\epsilon}$, $$\begin{equation*}
         {\mathbb{P}}({\textnormal{y}}- k \geq 2\sqrt{k{\epsilon}} + 2{\epsilon}) \leq \exp(-{\epsilon}) \ .
\end{equation*}$$*
:::

Following the general idea in [@rahimi2007random], we present the following Lemma [3](#le:kenerl-derivative-error){reference-type="ref" reference="le:kenerl-derivative-error"} to bound the difference of our approximated kernel using random features and the ground truth kernel $k$, as well as the difference between their partial derivatives first. To ease our presentation, we let the kernel $k$ be defined by an infinite dimensional vector $\psi({\bm{x}})$, which is defined by the corresponding infinite number of features for $k$, throughout this section. That is, $k({\bm{x}}, {\bm{x}}') = \psi({\bm{x}})^{\top}\psi({\bm{x}}')$ for any ${\bm{x}}, {\bm{x}}' \in {\mathcal{X}}$.

::: {#le:kenerl-derivative-error .lemma}
**Lemma 3**. *Let $\delta \in (0,1)$. Assume that $\mathbb{E}\left[\left\|{\bm{v}}\right\|^2\right] \leq V$, for any ${\bm{x}},{\bm{x}}' \in {\mathcal{X}}$, the following holds with probability of at least $1-\delta$, $$\begin{equation*}
\begin{aligned}
    \left|{\bm{\phi}}({\bm{x}})^{\top}{\bm{\phi}}({\bm{x}}') - {\bm{\psi}}({\bm{x}})^{\top}{\bm{\psi}}({\bm{x}}')\right| &\leq \sqrt{8\ln(2/\delta) / M} \ , \\    
    \left\|\nabla{\bm{\phi}}({\bm{x}})^{\top}{\bm{\phi}}({\bm{x}}') - \nabla{\bm{\psi}}({\bm{x}})^{\top}{\bm{\psi}}({\bm{x}}')\right\| &\leq \sqrt{4V / (M\delta)} 
\end{aligned}
\end{equation*}$$ where $M$ is the number of random Fourier features.*
:::

::: proof
*Proof.* Recall that ${\bm{\phi}}({\bm{x}})^{\top}{\bm{\phi}}({\bm{x}}') = 1 / M \sum_{j=1}^M 2\cos({\bm{v}}_j^{\top}{\bm{x}}+ b_j)\cos({\bm{v}}_j^{\top}{\bm{x}}' + b_j)$ as shown in Appx. [9](#app-sec:rff){reference-type="ref" reference="app-sec:rff"}. Then, according to [@rahimi2007random], for any $j\in[M]$, $$\begin{equation}
\begin{aligned}
    \mathbb{E}\left[2\cos({\bm{v}}_j^{\top}{\bm{x}}+ b_j)\cos({\bm{v}}_j^{\top}{\bm{x}}' + b_j)\right] &= {\bm{\psi}}({\bm{x}})^{\top}{\bm{\psi}}({\bm{x}}') \ , \\
    \mathbb{E}\left[{\bm{\phi}}({\bm{x}})^{\top}{\bm{\phi}}({\bm{x}}')\right] &= {\bm{\psi}}({\bm{x}})^{\top}{\bm{\psi}}({\bm{x}}') \ . \label{eq:temp-vnsvns}
\end{aligned}
\end{equation}$$ Since $2\cos({\bm{v}}_j^{\top}{\bm{x}}+ b_j)\cos({\bm{v}}_j^{\top}{\bm{x}}' + b_j) \in [-2,2]$ and both $\{{\bm{v}}_1, \cdots, {\bm{v}}_M\}$ and $\{b_1, \cdots, b_M\}$ are randomly independently sampled, according to Hoeffding's inequality, the following inequality holds for any ${\epsilon}> 0$ $$\begin{equation}
\begin{aligned}
    {\mathbb{P}}\left(\left|{\bm{\phi}}({\bm{x}})^{\top}{\bm{\phi}}({\bm{x}}') - {\bm{\psi}}({\bm{x}})^{\top}{\bm{\psi}}({\bm{x}}')\right| \geq {\epsilon}\right) \leq 2\exp\left(- \frac{M{\epsilon}^2}{8}\right) \ .
\end{aligned}
\end{equation}$$ Choose $\delta = 2\exp(M{\epsilon}^2)$, the following holds with a probability of at least $1-\delta$, $$\begin{equation}
\begin{aligned}
    \left|{\bm{\phi}}({\bm{x}})^{\top}{\bm{\phi}}({\bm{x}}') - {\bm{\psi}}({\bm{x}})^{\top}{\bm{\psi}}({\bm{x}}')\right| \leq \sqrt{\frac{8\ln(2/\delta)}{M}} \ .
\end{aligned}
\end{equation}$$

Moreover, based on the interchangeability of derivative and expectation, we then have the following results derived from [\[eq:temp-vnsvns\]](#eq:temp-vnsvns){reference-type="eqref" reference="eq:temp-vnsvns"} $$\begin{equation}
\begin{aligned}
    \mathbb{E}\left[-2\sin({\bm{v}}_j^{\top}{\bm{x}}+ b_j)\cos({\bm{v}}_j^{\top}{\bm{x}}' + b_j){\bm{v}}_j^{\top}\right] &= \nabla{\bm{\psi}}({\bm{x}})^{\top}{\bm{\psi}}({\bm{x}}')  \ , \\
    \mathbb{E}\left[\nabla{\bm{\phi}}({\bm{x}})^{\top}{\bm{\phi}}({\bm{x}}')\right] &= \nabla{\bm{\psi}}({\bm{x}})^{\top}{\bm{\psi}}({\bm{x}}') \ .
\end{aligned}
\end{equation}$$

Since both $\{{\bm{v}}_1, \cdots, {\bm{v}}_M\}$ and $\{b_1, \cdots, b_M\}$ are randomly independently sampled, we then can bound the variance $\mathbb{E}\left[\left\|\nabla{\bm{\phi}}({\bm{x}})^{\top}{\bm{\phi}}({\bm{x}}') - \nabla{\bm{\psi}}({\bm{x}})^{\top}{\bm{\psi}}({\bm{x}}')\right\|^2\right]$ as below $$\begin{equation}
\label{equ:phi-t-phi-norm}
\begin{aligned}
    &\mathbb{E}\left[\left\|\nabla{\bm{\phi}}({\bm{x}})^{\top}{\bm{\phi}}({\bm{x}}') - \nabla{\bm{\psi}}({\bm{x}})^{\top}{\bm{\psi}}({\bm{x}}')\right\|^2\right] \\
    \stackrel{(a)}{=}& \mathbb{E}\left[\left\|\frac{1}{M}\sum_{j=1}^M \left(-2\sin({\bm{v}}_j^{\top}{\bm{x}}+ b_j)  \cos({\bm{v}}_j^{\top}{\bm{x}}' + b_j) {\bm{v}}_j - \nabla{\bm{\psi}}({\bm{x}})^{\top}{\bm{\psi}}({\bm{x}}')\right)\right\|^2\right] \\
    \stackrel{(b)}{=}& \frac{1}{M^2}\mathbb{E}\left[\sum_{j=1}^M \left\|-2\sin({\bm{v}}_j^{\top}{\bm{x}}+ b_j)  \cos({\bm{v}}_j^{\top}{\bm{x}}' + b_j) {\bm{v}}_j - \nabla{\bm{\psi}}({\bm{x}})^{\top}{\bm{\psi}}({\bm{x}}')\right\|^2\right] \\
    \stackrel{(c)}{=}& \frac{1}{M^2}\sum_{j=1}^M \left(\mathbb{E}\left[\left\|-2\sin({\bm{v}}_j^{\top}{\bm{x}}+ b_j)  \cos({\bm{v}}_j^{\top}{\bm{x}}' + b_j) {\bm{v}}_j\right\|^2\right] - \mathbb{E}\left[\left\|\nabla{\bm{\psi}}({\bm{x}})^{\top}{\bm{\psi}}({\bm{x}}')\right\|^2\right]\right) \\
    \stackrel{(d)}{\leq}& \frac{1}{M^2}\sum_{j=1}^M \mathbb{E}\left[\left\|-2\sin({\bm{v}}_j^{\top}{\bm{x}}+ b_j)  \cos({\bm{v}}_j^{\top}{\bm{x}}' + b_j) {\bm{v}}_j\right\|^2\right] \\
    \stackrel{(e)}{\leq}& \frac{4}{M^2} \sum_{j=1}^M \mathbb{E}\left[\left\|{\bm{v}}_j\right\|^2\right] \\
    \stackrel{(f)}{\leq}& \frac{4V}{M}
\end{aligned}
\end{equation}$$ where $(b)$ is from the independence among $\{{\bm{v}}_1, \cdots, {\bm{v}}_M\}$ and $\{b_1, \cdots, b_M\}$ for variance derivation and $(c)$ is based on the definition of variance. In addition, $(e)$ is due to the fact that $\sin({\bm{v}}_j^{\top}{\bm{x}}+ b_j), \cos({\bm{v}}_j^{\top}{\bm{x}}' + b_j) \in [-1,1]$ and $(f)$ is because of the assumption that $\mathbb{E}\left[\left\|{\bm{v}}\right\|^2\right] \leq V$.

Therefore, according to Chebyshev's inequality, we have the following inequalities for any ${\epsilon}>0$ $$\begin{equation}
\begin{aligned}
    {\mathbb{P}}\left(\left\|\nabla{\bm{\phi}}({\bm{x}})^{\top}{\bm{\phi}}({\bm{x}}') - \nabla{\bm{\psi}}({\bm{x}})^{\top}{\bm{\psi}}({\bm{x}}')\right\| > {\epsilon}\right) &\leq \frac{\mathbb{E}\left[\left\|\nabla{\bm{\phi}}({\bm{x}})^{\top}{\bm{\phi}}({\bm{x}}') - \nabla{\bm{\psi}}({\bm{x}})^{\top}{\bm{\psi}}({\bm{x}}')\right\|^2\right]}{{\epsilon}^2} \\
    &\leq \frac{4V}{M {\epsilon}^2} \ .
\end{aligned}
\end{equation}$$

Choose ${\epsilon}= \sqrt{4V / (M\delta)}$, the following holds for a probability of at least $1-\delta$, $$\begin{equation}
\begin{aligned}
    \left\|\nabla{\bm{\phi}}({\bm{x}})^{\top}{\bm{\phi}}({\bm{x}}') - \nabla{\bm{\psi}}({\bm{x}})^{\top}{\bm{\psi}}({\bm{x}}')\right\| \leq \sqrt{\frac{4V}{M\delta}} \ ,
\end{aligned}
\end{equation}$$ which finally completes the proof. ◻
:::

::: {#th:approximation-error-mean-derivative-gp .lemma}
**Lemma 4**. *For any ${\bm{x}}, {\bm{x}}' \in {\mathcal{X}}$ and $i \in [N]$, assume that $\mathbb{E}\left[\left\|{\bm{v}}\right\|^2\right] \leq V$, $\left\|\nabla {\bm{\psi}}({\bm{x}})^{\top}{\bm{\psi}}({\bm{x}}') \right\| \leq L$ and $\left|f_i({\bm{x}})\right| \leq 1$, then the following holds with a constant probability for all $r \in [R]$, $$\begin{equation*}
    \left\|\nabla\widehat{\mu}_{r,T}^{(i)}({\bm{x}}) - \nabla \mu^{(i)}_{r,T}({\bm{x}})\right\|^2 \le {\mathcal{O}}\left(\frac{1}{M}\right) \ .
\end{equation*}$$*
:::

::: proof
*Proof.* Based on the definition in [\[eq:posterior-derived\]](#eq:posterior-derived){reference-type="eqref" reference="eq:posterior-derived"} and [\[eq:local-surrogate-approx\]](#eq:local-surrogate-approx){reference-type="eqref" reference="eq:local-surrogate-approx"}, we have that: $$\begin{equation}
\begin{aligned}
    &\left\|\nabla\widehat{\mu}^{(i)}_{r, T}({\bm{x}}) - \nabla \mu^{(i)}_{r, T}({\bm{x}})\right\| \\
    \stackrel{(a)}{=}& \left\|\nabla {\bm{\phi}}({\bm{x}})^{\top}{\bm{\Phi}}^{(i)}_{r, t-1}\left(\widehat{{\mathbf{K}}}^{(i)}_{r, T}+\sigma^2{\mathbf{I}}\right)^{-1}{\bm{y}}^{(i)}_{r, T} - \nabla{\bm{\psi}}({\bm{x}})^{\top}{\bm{\Psi}}^{(i)}_{r, T}\left({\mathbf{K}}^{(i)}_{r, T}+\sigma^2{\mathbf{I}}\right)^{-1}{\bm{y}}^{(i)}_{r, T}\right\| \\
    \stackrel{(b)}{\leq}& \left\|\nabla {\bm{\phi}}({\bm{x}})^{\top}{\bm{\Phi}}^{(i)}_{r, T}\left(\widehat{{\mathbf{K}}}^{(i)}_{r, T}+\sigma^2{\mathbf{I}}\right)^{-1} - \nabla{\bm{\psi}}({\bm{x}})^{\top}{\bm{\Psi}}^{(i)}_{r, T}\left({\mathbf{K}}^{(i)}_{r, T}+\sigma^2{\mathbf{I}}\right)^{-1}\right\|\left\|{\bm{y}}^{(i)}_{r, T}\right\| \\
    \stackrel{(c)}{=}& \underbrace{\left\|\nabla {\bm{\phi}}({\bm{x}})^{\top}{\bm{\Phi}}^{(i)}_{r, T}\left(\widehat{{\mathbf{K}}}^{(i)}_{r, T}+\sigma^2{\mathbf{I}}\right)^{-1} - \nabla{\bm{\psi}}({\bm{x}})^{\top}{\bm{\Psi}}^{(i)}_{r, T}\left(\widehat{{\mathbf{K}}}^{(i)}_{r, T}+\sigma^2{\mathbf{I}}\right)^{-1}\right\|}_{\tikz[baseline=(char.base)]{\node[shape=circle,draw,inner sep=0.2pt] (char) {1};}}\left\|{\bm{y}}^{(i)}_{r, T}\right\| + \\ 
    &\qquad \underbrace{\left\|\nabla{\bm{\psi}}({\bm{x}})^{\top}{\bm{\Psi}}^{(i)}_{r, T}\left(\widehat{{\mathbf{K}}}^{(i)}_{r,T}+\sigma^2{\mathbf{I}}\right)^{-1} - \nabla{\bm{\psi}}({\bm{x}})^{\top}{\bm{\Psi}}^{(i)}_{r,T}\left({\mathbf{K}}^{(i)}_{r,T}+\sigma^2{\mathbf{I}}\right)^{-1}\right\|}_{\tikz[baseline=(char.base)]{\node[shape=circle,draw,inner sep=0.2pt] (char) {2};}}\left\|{\bm{y}}^{(i)}_{r,T}\right\| \label{eq:temp-2uvnu}
\end{aligned}
\end{equation}$$ where $(b)$ and $(c)$ are from the Cauchy--Schwarz inequality and the triangle inequality, respectively.

We bound term $\tikz[baseline=(char.base)]{\node[shape=circle,draw,inner sep=0.2pt] (char) {1};}$, term $\tikz[baseline=(char.base)]{\node[shape=circle,draw,inner sep=0.2pt] (char) {2};}$ and $\left\|{\bm{y}}^{(i)}_{r,T}\right\|$ above separately. Firstly, the following holds with probability of at least $1-rT\delta'$ $$\begin{equation}
\begin{aligned}
\tikz[baseline=(char.base)]{\node[shape=circle,draw,inner sep=0.2pt] (char) {1};} &\stackrel{(a)}{=} \left\|\nabla {\bm{\phi}}({\bm{x}})^{\top}{\bm{\Phi}}^{(i)}_{r,T}\left(\widehat{{\mathbf{K}}}^{(i)}_{r,T}+\sigma^2{\mathbf{I}}\right)^{-1} - \nabla{\bm{\psi}}({\bm{x}})^{\top}{\bm{\Psi}}^{(i)}_{r,T}\left(\widehat{{\mathbf{K}}}^{(i)}_{r,T}+\sigma^2{\mathbf{I}}\right)^{-1}\right\| \\
&\stackrel{(b)}{\leq} \left\|\nabla {\bm{\phi}}({\bm{x}})^{\top}{\bm{\Phi}}^{(i)}_{r,T} - \nabla{\bm{\psi}}({\bm{x}})^{\top}{\bm{\Psi}}^{(i)}_{r,T}\right\|\left\|\left(\widehat{{\mathbf{K}}}^{(i)}_{r,T}+\sigma^2{\mathbf{I}}\right)^{-1}\right\| \\
&\stackrel{(c)}{\leq} \sqrt{\sum_{\tau=1}^{rT}\left\|\nabla {\bm{\phi}}({\bm{x}})^{\top}{\bm{\phi}}({\bm{x}}^{(i)}_{\tau}) - \nabla {\bm{\psi}}({\bm{x}})^{\top}{\bm{\psi}}({\bm{x}}^{(i)}_{\tau})\right\|^2}\left\|\left(\widehat{{\mathbf{K}}}^{(i)}_{r,T}+\sigma^2{\mathbf{I}}\right)^{-1}\right\| \\
&\stackrel{(d)}{\leq} \frac{1}{\sigma^2} \sqrt{\frac{4rTV}{M\delta'}} \label{eq:temp-quf3}
\end{aligned}
\end{equation}$$ Where $(b)$ comes from the Cauchy--Schwarz inequality and $(c)$ follows from the fact that for any matrix $A$ with $n$ rows and each row identified as $\bm{a}_i$ we have $\|A\| \le \|A\|_{\text{F}} \triangleq \sqrt{\sum_{i=1}^n \|\bm{a}_i\|^2}$. Finally, $(d)$ is due to the fact that $\widehat{{\mathbf{K}}}^{(i)}_{r,T}$ is positive semi-definite and therefore $\widehat{{\mathbf{K}}}^{(i)}_{r,T}+\sigma^2{\mathbf{I}}\succcurlyeq \sigma^2{\mathbf{I}}$ as well as the results in Lemma [3](#le:kenerl-derivative-error){reference-type="ref" reference="le:kenerl-derivative-error"}.

Secondly, the following holds with probability of at least $1-r^2T^2\delta''$, $$\begin{equation}
\begin{aligned}
\tikz[baseline=(char.base)]{\node[shape=circle,draw,inner sep=0.2pt] (char) {2};} &\stackrel{(a)}{=} \left\|\nabla {\bm{\psi}}({\bm{x}})^{\top}{\bm{\Psi}}^{(i)}_{r,T}\left(\widehat{{\mathbf{K}}}^{(i)}_{r,T}+\sigma^2{\mathbf{I}}\right)^{-1} - \nabla {\bm{\psi}}({\bm{x}})^{\top}{\bm{\Psi}}^{(i)}_{r,T}\left({\mathbf{K}}^{(i)}_{r,T}+\sigma^2{\mathbf{I}}\right)^{-1}\right\| \\
&\stackrel{(b)}{\leq} \left\|\nabla {\bm{\psi}}({\bm{x}})^{\top}{\bm{\Psi}}^{(i)}_{r, t-1}\right\|\left\|\left(\widehat{{\mathbf{K}}}^{(i)}_{r,T}+\sigma^2{\mathbf{I}}\right)^{-1} - \left({\mathbf{K}}^{(i)}_{r,T}+\sigma^2{\mathbf{I}}\right)^{-1}\right\| \\
&\stackrel{(c)}{=} \left\|\nabla {\bm{\psi}}({\bm{x}})^{\top}{\bm{\Psi}}^{(i)}_{r,T}\right\|\left\|\left({\mathbf{K}}^{(i)}_{r,T} - \widehat{{\mathbf{K}}}^{(i)}_{r,T}\right)\left(\widehat{{\mathbf{K}}}^{(i)}_{r,T}+\sigma^2{\mathbf{I}}\right)^{-1}\left({\mathbf{K}}^{(i)}_{r,T}+\sigma^2{\mathbf{I}}\right)^{-1}\right\| \\
&\stackrel{(d)}{\leq} \sqrt{\sum_{\tau=1}^{rT} \left\|\nabla {\bm{\psi}}({\bm{x}})^{\top}{\bm{\psi}}({\bm{x}}^{(i)}_{\tau}) \right\|^2}\left\|{\mathbf{K}}^{(i)}_{r,T} - \widehat{{\mathbf{K}}}^{(i)}_{r,T}\right\|\left\|\left(\widehat{{\mathbf{K}}}^{(i)}_{r,T}+\sigma^2{\mathbf{I}}\right)^{-1}\right\|\left\|\left({\mathbf{K}}^{(i)}_{r,T}+\sigma^2{\mathbf{I}}\right)^{-1}\right\| \\
&\stackrel{(e)}{\leq} \frac{L}{\sigma^4} \sqrt{rT}\sqrt{\sum_{\tau,\tau'=1}^{rT} \left\|{\bm{\psi}}({\bm{x}}^{(i)}_{\tau})^{\top}{\bm{\psi}}({\bm{x}}^{(i)}_{\tau'}) - {\bm{\phi}}({\bm{x}}^{(i)}_{\tau})^{\top}{\bm{\phi}}({\bm{x}}^{(i)}_{\tau'})\right\|^2} \\
&\stackrel{(f)}{\leq} \frac{L \left(rT\right)^{3/2}}{\sigma^4}\sqrt{\frac{8\ln(2/\delta'')}{M}} \label{eq:temp-scj82}
\end{aligned}
\end{equation}$$ where $(b)$ is from the Cauchy--Schwarz inequality. Besides, $(c)$ and $(e)$ come from the aforementioned inequality $\|A\| \le \|A\|_{\text{F}}$. In addition, $(f)$ is based on the assumption that $\left\|\nabla {\bm{\psi}}({\bm{x}})^{\top}{\bm{\psi}}({\bm{x}}') \right\| \leq L$, $\|A\| \le \|A\|_{\text{F}}$, $\widehat{{\mathbf{K}}}^{(i)}_{r,T}+\sigma^2{\mathbf{I}}\succcurlyeq \sigma^2{\mathbf{I}}$ and ${\mathbf{K}}^{(i)}_{r,T}+\sigma^2{\mathbf{I}}\succcurlyeq \sigma^2{\mathbf{I}}$.

Thirdly, the following holds with probability of at least $1-rT\delta'''$, $$\begin{equation}
\begin{aligned}
    \left\|{\bm{y}}_{r,T}^{(i)}\right\| &\stackrel{(a)}{=} \sqrt{\sum_{\tau=1}^{rT} \left(f_i({\bm{x}}_{\tau}) + \zeta_{\tau}\right)^2} \\
    &\stackrel{(b)}{\leq} \sqrt{\sum_{\tau=1}^{rT} 2f^2_i({\bm{x}}_{\tau}) + 2\zeta^2_{\tau} } \\
    &\stackrel{(c)}{\leq} \sqrt{2rT + 2\sigma^2 \sum_{\tau=1}^{rT} \left(\frac{\zeta_{\tau}}{\sigma}\right)^2} \\
    &\stackrel{(d)}{\leq} \sqrt{2rT + 2\sigma^2\left(rT + 2\sqrt{rT\ln(1/\delta''')} + 2\ln(1/\delta''')\right)} \label{eq:temp-fwnsl}
\end{aligned}
\end{equation}$$ where $\zeta_{\tau}$ denote the observation noise associated with the input ${\bm{x}}_{\tau}$. Besides, $(c)$ is from the assumption that $\zeta_{\tau} \sim {\mathcal{N}}(0, \sigma^2)$ for any $\tau$ in Sec. [2](#sec:setting){reference-type="ref" reference="sec:setting"} and $\left|f_i({\bm{x}})\right| \leq 1$ for any ${\bm{x}}\in {\mathcal{X}}$. Finally, $(d)$ comes from our Lemma [2](#le:chi-square){reference-type="ref" reference="le:chi-square"}.

By introducing [\[eq:temp-quf3\]](#eq:temp-quf3){reference-type="eqref" reference="eq:temp-quf3"}, [\[eq:temp-scj82\]](#eq:temp-scj82){reference-type="eqref" reference="eq:temp-scj82"} and [\[eq:temp-fwnsl\]](#eq:temp-fwnsl){reference-type="eqref" reference="eq:temp-fwnsl"} with $\delta' = \frac{\delta}{3rT}$, $\delta'' = \frac{\delta}{3r^2T^2}$ and $\delta''' = \frac{\delta}{3rT}$ into [\[eq:temp-2uvnu\]](#eq:temp-2uvnu){reference-type="eqref" reference="eq:temp-2uvnu"}, the following then holds with probability of at least $1-\delta$, $$\begin{equation}
\begin{aligned}
    &\left\|\nabla\widehat{\mu}^{(i)}_{r, T}({\bm{x}}) - \nabla \mu^{(i)}_{r, T}({\bm{x}})\right\| \\
    \leq& \left(\frac{rT}{\sigma^2} \sqrt{\frac{12V}{M\delta}} + \frac{4L \left(rT\right)^{3/2}}{\sigma^4}\sqrt{\frac{\ln(6rT/\delta)}{M}}\right)  \sqrt{2rT + 2\sigma^2\left(rT + 2\sqrt{rT\ln(3rT/\delta)} + 2\ln(3rT/\delta)\right)} \\
    =& {\mathcal{O}}\left(\frac{rT\sqrt{rT}}{\sqrt{M}} + \frac{r^2T^2\sqrt{\ln(rT)}}{\sqrt{M}}\right) \ . \label{eq:temp-2ivnw}
\end{aligned}
\end{equation}$$

Of note, it is easy to show that when [\[eq:temp-2ivnw\]](#eq:temp-2ivnw){reference-type="eqref" reference="eq:temp-2ivnw"} holds for $r=R$, it must hold for any $r \leq R$. Therefore, the following finally holds with a constant probability for all $r \in [R]$, $$\begin{equation}
    \left\|\nabla\widehat{\mu}^{(i)}_{r, T}({\bm{x}}) - \nabla \mu^{(i)}_{r, T}({\bm{x}})\right\|^2 \leq {\mathcal{O}}\left(\frac{1}{M}\right) \ ,
\end{equation}$$ which concludes our proof. ◻
:::

::: remark
**Remark 1**. *Note that the assumption $\mathbb{E}\left[\left\|{\bm{v}}\right\|^2\right] \leq V$ implies that the distribution $p({\bm{v}})$ in Appx. [9](#app-sec:rff){reference-type="ref" reference="app-sec:rff"} has a bounded mean and covariance since $\mathbb{E}\left[\left\|{\bm{v}}\right\|^2\right] = \left\|\mathbb{E}\left[{\bm{v}}\right]\right\|^2 + \mathbb{E}\left[\left\|{\bm{v}}- \mathbb{E}\left[{\bm{v}}\right]\right\|^2\right]$. This is usually valid for the widely applied kernels (e.g., the squared exponential kernel in Appx. [9](#app-sec:rff){reference-type="ref" reference="app-sec:rff"}) in practice.*

*Remarkably, [\[eq:temp-2ivnw\]](#eq:temp-2ivnw){reference-type="eqref" reference="eq:temp-2ivnw"} with $r=R$ has demonstrated that a larger number $M$ of random features is preferred to maintain the approximation quality of $\nabla\widehat{\mu}^{(i)}_{R, T}({\bm{x}}) \approx \nabla \mu^{(i)}_{R, T}$ when the number $R$ of communication rounds and the number $T$ of local iterations increase. This in fact aligns with the intuition that a larger hypothesis space (defined by the $M$ random features) should be used when the target function (defined by the existing $RT$ function queries) becomes more complex. However, for any communication round $r+1 \in [R]$ in our FZooS, the approximation of $\nabla \mu^{(i)}_{r, T}$ using $\nabla\widehat{\mu}^{(i)}_{r, T}({\bm{x}})$ needs to be accurate only at the local updated inputs $\{{\bm{x}}^{(i)}_{r+1, t-1}\}_{t \in [T], i \in [N]}$ with a relatively small $T$ (i.e., $T \leq 20$), which consequently usually does not requires an extremely large $M$ to realize a good approximation quality in practice. This has actually been supported by the empirical results in our Sec. [6](#sec:exps){reference-type="ref" reference="sec:exps"} and Appx. [13](#app-sec:more){reference-type="ref" reference="app-sec:more"}.*
:::

### Final Gradient Disparity Analysis Using Uncertainty

We introduce the following Lemma [5](#le:triangle){reference-type="ref" reference="le:triangle"} and Lemma [6](#le:uncertainty-error){reference-type="ref" reference="le:uncertainty-error"} from [@zord] to ease our proof of Thm. [1](#th:grad-error){reference-type="ref" reference="th:grad-error"}:

::: {#le:triangle .lemma}
**Lemma 5**. *Let $\left\{{\bm{v}}_{1}, \ldots, {\bm{v}}_{\tau}\right\}$ be any $\tau$ vectors in $\mathbb{R}^{d}$. Then the following holds for any $a>0$: $$\begin{align}
    \left\|{\bm{v}}_i\right\|\left\|{\bm{v}}_j\right\| &\leq \frac{a}{2}\left\|{\bm{v}}_i\right\|^2 + \frac{1}{2a}\left\|{\bm{v}}_j\right\|^2 \ , \label{eq:triangle-1} \\
    \left\|{\bm{v}}_{i}+{\bm{v}}_{j}\right\|^{2} &\leq (1+a)\left\|{\bm{v}}_{i}\right\|^{2}+\left(1+\frac{1}{a}\right)\left\|{\bm{v}}_{j}\right\|^{2} \ , \label{eq:triangle-2} \\
    \left\|\sum_{i=1}^{\tau} {\bm{v}}_{i}\right\|^{2} &\leq \tau \sum_{i=1}^{\tau}\left\|{\bm{v}}_{i}\right\|^{2} \ . \label{eq:triangle-3}
\end{align}$$*
:::

::: proof
*Proof.* For [\[eq:triangle-1\]](#eq:triangle-1){reference-type="eqref" reference="eq:triangle-1"}, we have that $$\begin{equation}
\begin{aligned}
    \frac{a}{2}\left\|{\bm{v}}_i\right\|^2 + \frac{1}{2a}\left\|{\bm{v}}_j\right\|^2 \geq 2\sqrt{\frac{a}{2}\left\|{\bm{v}}_i\right\|^2 \cdot \frac{1}{2a}\left\|{\bm{v}}_j\right\|^2} = \left\|{\bm{v}}_i\right\|\left\|{\bm{v}}_j\right\| \ .
\end{aligned}
\end{equation}$$

For [\[eq:triangle-2\]](#eq:triangle-2){reference-type="eqref" reference="eq:triangle-2"}, we have that $$\begin{equation}
\begin{aligned}
    (1+a)\left\|{\bm{v}}_{i}\right\|^{2}+\left(1+\frac{1}{a}\right)\left\|{\bm{v}}_{j}\right\|^{2} &= \left\|{\bm{v}}_{i}\right\|^2 + \left\|{\bm{v}}_{j}\right\|^2 + \left(a\left\|{\bm{v}}_{i}\right\|^2 + \frac{1}{a} \left\|{\bm{v}}_{j}\right\|^2\right) \\
    &\geq \left\|{\bm{v}}_{i}\right\|^2 + \left\|{\bm{v}}_{j}\right\|^2 + 2\sqrt{a\left\|{\bm{v}}_{i}\right\|^2  \cdot \frac{1}{a} \left\|{\bm{v}}_{j}\right\|^2} \\
    % &= \left\|\vv_{i}\right\|^2 + \left\|\vv_{j}\right\|^2 + 2\left\|\vv_i\right\|\left\|\vv_j\right\| \\
    &= \left\|{\bm{v}}_{i}+{\bm{v}}_{j}\right\|^{2} \ .
\end{aligned}
\end{equation}$$

For [\[eq:triangle-3\]](#eq:triangle-3){reference-type="eqref" reference="eq:triangle-3"}, we can directly employ the convexity of function $h({\bm{x}})=\left\|{\bm{x}}\right\|^2$ and Jensen's inequality: $$\begin{equation}
\begin{aligned}
    \left\|\frac{1}{\tau}\sum_{i=1}^{\tau} {\bm{v}}_{i}\right\|^{2} \leq \frac{1}{\tau}\sum_{i=1}^{\tau}\left\|{\bm{v}}_{i}\right\|^{2} \ .
\end{aligned}
\end{equation}$$ By multiplying the inequality above with $\tau^2$, we conclude the proof. ◻
:::

::: {#le:uncertainty-error .lemma}
**Lemma 6**. *Define $\rho_i \triangleq \max_{{\bm{x}}\in {\mathcal{X}}, r\geq 1, t\geq 1} \left\|\partial \left(\sigma^{(i)}_{r,t}\right)^2({\bm{x}})\right\| \bigg/ \left\|\partial \left(\sigma^{(i)}_{r,t-1}\right)^2({\bm{x}})\right\|$, we have that $\rho_i \in \left[1 / (1+1/\sigma^2), 1\right]$, and that for any ${\bm{x}}\in{\mathcal{X}}, r\geq 1,t\geq1$ the following holds, $$\begin{equation*}
\begin{aligned}
    \left\|\partial \left(\sigma^{(i)}_{r,t}\right)^2({\bm{x}})\right\| \leq \kappa \rho_i^{(r-1)T+t} \ .
\end{aligned}
\end{equation*}$$*
:::

Let $\delta \in (0, 1)$, ${\epsilon}= {\mathcal{O}}(\frac{1}{M})$ and $\omega = d + 2(\sqrt{d}+1)\ln(2NRT/\delta)$, the following inequalities then hold with a probability of at least $1 - \delta$: $$\begin{equation}
\begin{aligned}
    &\left\|\frac{1}{N}\sum_{j=1,j\neq i}^N \left(\nabla \widehat{\mu}^{(j)}_{r-1, T}({\bm{x}}_{r,t-1}^{(i)}) - \nabla f_j({\bm{x}}_{r,t-1}^{(i)})\right)\right\|^2 \\
    \stackrel{(a)}{\leq}& \frac{N-1}{N^2} \sum_{j=1,j\neq i}^N \left\|\nabla \widehat{\mu}^{(j)}_{r-1, T}({\bm{x}}_{r,t-1}^{(i)}) - \nabla f_j({\bm{x}}_{r,t-1}^{(i)})\right\|^2 \\
    \stackrel{(b)}{=}& \frac{N-1}{N^2} \sum_{j=1,j\neq i}^N  \left\|\nabla \widehat{\mu}^{(j)}_{r-1, T}({\bm{x}}_{r,t-1}^{(i)}) - \nabla \mu^{(j)}_{r-1, T}({\bm{x}}_{r,t-1}^{(i)}) + \nabla \mu^{(j)}_{r-1, T}({\bm{x}}_{r,t-1}^{(i)}) - \nabla f_j({\bm{x}}_{r,t-1}^{(i)})\right\|^2 \\
    \stackrel{(c)}{\leq}& \frac{N-1}{N^2} \sum_{j=1,j\neq i}^N \left(\frac{N}{N-1}\left\|\nabla \mu^{(j)}_{r-1, T}({\bm{x}}_{r,t-1}^{(i)}) - \nabla f_j({\bm{x}}_{r,t-1}^{(i)})\right\|^2 + N\left\|\nabla \widehat{\mu}^{(j)}_{r-1, T}({\bm{x}}_{r,t-1}^{(i)}) - \nabla \mu^{(j)}_{r-1, T}({\bm{x}}_{r,t-1}^{(i)})\right\|^2\right) \\
    \stackrel{(d)}{\leq}& \frac{\omega}{N} \sum_{j=1,j\neq i}^N \left\|\partial \left(\sigma^{(j)}_{r-1,T}\right)^2({\bm{x}}_{r,t-1}^{(i)})\right\| + \frac{(N-1)^2}{N} {\epsilon}\ , \label{eq:temp-hvwj}
\end{aligned}
\end{equation}$$ in which $(a)$ is from [\[eq:triangle-3\]](#eq:triangle-3){reference-type="eqref" reference="eq:triangle-3"} and $(c)$ is from [\[eq:triangle-2\]](#eq:triangle-2){reference-type="eqref" reference="eq:triangle-2"} with $a=\frac{1}{N-1}$. In addition, $(d)$ comes from Lemma [1](#le:confidence-bound){reference-type="ref" reference="le:confidence-bound"} and Lemma [4](#th:approximation-error-mean-derivative-gp){reference-type="ref" reference="th:approximation-error-mean-derivative-gp"}.

$$\begin{equation}
\begin{aligned}
    &\frac{(N-1)^2}{N^2} \left\|\nabla f_i({\bm{x}}_{r,t-1}^{(i)}) - \nabla \widehat{\mu}_{r-1,T}^{(i)}({\bm{x}}_{r,t-1}^{(i)})\right\|^2 \\
    \stackrel{(a)}{=}&\frac{(N-1)^2}{N^2} \left\|\nabla f_i({\bm{x}}_{r,t-1}^{(i)}) - \nabla \mu_{r-1,T}^{(i)}({\bm{x}}_{r,t-1}^{(i)}) + \nabla \mu_{r-1,T}^{(i)}({\bm{x}}_{r,t-1}^{(i)}) - \nabla \widehat{\mu}_{r-1,T}^{(i)}({\bm{x}}_{r,t-1}^{(i)})\right\|^2 \\
    \stackrel{(b)}{\leq}& \frac{(N-1)^2}{N^2}\left(\frac{N}{N-1}\left\|\nabla f_i({\bm{x}}_{r,t-1}^{(i)}) - \nabla \mu_{r-1,T}^{(i)}({\bm{x}}_{r,t-1}^{(i)})\right\|^2 + N\left\|\nabla \mu_{r-1,T}^{(i)}({\bm{x}}_{r,t-1}^{(i)}) \nabla \widehat{\mu}_{r-1,T}^{(i)}({\bm{x}}_{r,t-1}^{(i)})\right\|^2\right) \\
    \stackrel{(c)}{\leq}& \left(\frac{\omega(N-1)}{N}\left\|\partial \left(\sigma^{(i)}_{r-1,T}\right)^2({\bm{x}}_{r, t-1}^{(i)})\right\| + \frac{(N-1)^2}{N} {\epsilon}\right) \ , \label{eq:temp-vcbewi}
\end{aligned}
\end{equation}$$ in which $(c)$ is from [\[eq:triangle-2\]](#eq:triangle-2){reference-type="eqref" reference="eq:triangle-2"} with $a=\frac{1}{N-1}$. In addition, $(d)$ comes from Lemma [1](#le:confidence-bound){reference-type="ref" reference="le:confidence-bound"} and Lemma [4](#th:approximation-error-mean-derivative-gp){reference-type="ref" reference="th:approximation-error-mean-derivative-gp"}.

By exploiting the inequalities above, we have $$\begin{equation}
\begin{aligned}
    &\frac{1}{N} \sum_{i=1}^N \Xi_{r,t}^{(i)} \\
    % =& \frac{1}{N} \sum_{i=1}^N \left\|\widehat{\vg}^{(i)}_{r,t-1} - \nabla F(\vx_{r,t-1}^{(i)})\right\|^2 \\
    \stackrel{(a)}{=}& \frac{1}{N} \sum_{i=1}^N \left\|\nabla \mu_{r,t-1}^{(i)}({\bm{x}}_{r,t-1}^{(i)}) + \gamma_{r, t-1}\left(\nabla \widehat{\mu}_{r-1}({\bm{x}}_{r,t-1}^{(i)}) - \nabla \widehat{\mu}_{r-1,T}^{(i)}({\bm{x}}_{r,t-1}^{(i)})\right) - \nabla F({\bm{x}}_{r,t-1}^{(i)})\right\|^2 \\
    \stackrel{(b)}{=}& \frac{1}{N} \sum_{i=1}^N \left\|\nabla \mu_{r,t-1}^{(i)}({\bm{x}}_{r,t-1}^{(i)}) - \nabla f_i({\bm{x}}_{r,t-1}^{(i)}) + \gamma_{r, t-1}\left(\frac{1}{N}\sum_{j=1,j\neq i}^N \left(\nabla \widehat{\mu}^{(j)}_{r-1, T}({\bm{x}}_{r,t-1}^{(i)}) - \nabla f_j({\bm{x}}_{r,t-1}^{(i)})\right)\right) + \right. \\
    &\qquad \left. \frac{\gamma_{r, t-1}(N-1)}{N} \left(\nabla f_i({\bm{x}}_{r,t-1}^{(i)}) - \nabla \widehat{\mu}_{r-1,T}^{(i)}({\bm{x}}_{r,t-1}^{(i)})\right) + (1 - \gamma_{r, t-1}) \left(\nabla f_i({\bm{x}}_{r,t-1}^{(i)}) - \nabla F({\bm{x}}_{r,t-1}^{(i)})\right)\right\|^2 \\
    \stackrel{(c)}{\leq}& \frac{1}{N} \sum_{i=1}^N \left(4\left\|\nabla \mu_{r,t-1}^{(i)}({\bm{x}}_{r,t-1}^{(i)}) - \nabla f_i({\bm{x}}_{r,t-1}^{(i)})\right\|^2 + 4\gamma^2_{r, t-1}\left\|\frac{1}{N}\sum_{j=1,j\neq i}^N \left(\nabla \widehat{\mu}^{(j)}_{r-1, T}({\bm{x}}_{r,t-1}^{(i)}) - \nabla f_j({\bm{x}}_{r,t-1}^{(i)})\right)\right\|^2 + \right. \\
    &\qquad \left. \frac{4\gamma_{r, t-1}^2(N-1)^2}{N^2} \left\|\nabla f_i({\bm{x}}_{r,t-1}^{(i)}) - \nabla \widehat{\mu}_{r-1,T}^{(i)}({\bm{x}}_{r,t-1}^{(i)})\right\|^2 + 4(1 - \gamma_{r, t-1})^2 \left\|\nabla f_i({\bm{x}}_{r,t-1}^{(i)}) - \nabla F({\bm{x}}_{r,t-1}^{(i)})\right\|^2\right) \\
    \stackrel{(d)}{\leq}& \frac{4\omega}{N} \sum_{i=1}^N \left\|\partial \left(\sigma^{(i)}_{r,t-1}\right)({\bm{x}}_{r,t-1}^{(i)})\right\| + 4\gamma^2_{r, t-1} \left(\frac{\omega}{N^2}\sum_{i=1}^N\sum_{j=1,j\neq i}^N \left\|\partial \left(\sigma^{(j)}_{r-1,T}\right)^2({\bm{x}}_{r,t-1}^{(i)})\right\| +  \frac{(N-1)^2}{N} {\epsilon}\right) + \\
    &\qquad 4\gamma_{r, t-1}^2\left(\frac{\omega(N-1)}{N^2}\sum_{i=1}^N \left\|\partial \left(\sigma^{(i)}_{r-1,T}\right)^2({\bm{x}}_{r, t-1}^{(i)})\right\| + \frac{(N-1)^2}{N} {\epsilon}\right) + 4(1 - \gamma_{r, t-1})^2G \label{eq:temp-vbej}
\end{aligned}
\end{equation}$$ where $(c)$ is from the [\[eq:triangle-3\]](#eq:triangle-3){reference-type="eqref" reference="eq:triangle-3"}. In addition, $(d)$ is from Lemma [1](#le:confidence-bound){reference-type="ref" reference="le:confidence-bound"}, [\[eq:temp-hvwj\]](#eq:temp-hvwj){reference-type="eqref" reference="eq:temp-hvwj"} and [\[eq:temp-vcbewi\]](#eq:temp-vcbewi){reference-type="eqref" reference="eq:temp-vcbewi"}.

By introducing the results in Lemma [6](#le:uncertainty-error){reference-type="ref" reference="le:uncertainty-error"} into [\[eq:temp-vbej\]](#eq:temp-vbej){reference-type="eqref" reference="eq:temp-vbej"}, we have $$\begin{equation}
\begin{aligned}
    \frac{1}{N} \sum_{i=1}^N \Xi_{r,t}^{(i)}
    &\stackrel{(a)}{\leq} \frac{4\omega}{N}\sum_{i=1}^N \kappa \rho_i^{(r-1)T+t-1} + 4\gamma^2_{r, t-1}\left(\frac{2\omega(N-1)}{N^2} \sum_{i=1}^N \kappa \rho_i^{(r-1)T}  + \frac{2(N-1)^2}{N}{\epsilon}\right) \\
    &\qquad\qquad + 4(1 - \gamma_{r, t-1})^2G \\
    &\stackrel{(b)}{\leq} \frac{4\omega}{N}\sum_{i=1}^N \kappa \rho_i^{(r-1)T+t-1} + 4\gamma^2_{r, t-1}\left(\frac{2\omega}{N} \sum_{i=1}^N \kappa \rho_i^{(r-1)T}  + 2N{\epsilon}\right) + 4(1 - \gamma_{r, t-1})^2G \\
    &\stackrel{(c)}{\leq} 4\omega\kappa \rho^{(r-1)T+t-1} + 4\gamma^2_{r, t-1}\left(2\omega\kappa \rho^{(r-1)T}  + 2N{\epsilon}\right) + 4(1 - \gamma_{r, t-1})^2G \label{eq:temp-amvsw}
\end{aligned}
\end{equation}$$ where $(c)$ is from Jansen's inequality with $\rho \triangleq \frac{1}{N} \sum_{i=1}^N\rho_i$. This finally concludes our proof.

::: remark
**Remark 2**. *Of note, the upper bound in our Thm. [1](#th:grad-error){reference-type="ref" reference="th:grad-error"} is a quadratic function w.r.t. the gradient correction length $\gamma_{r, t-1}$. As a consequence, it is easy to verify that in order to minimize the upper bound in our Thm. [1](#th:grad-error){reference-type="ref" reference="th:grad-error"} (i.e., to achieve a better-performing [\[eq:fzoos-grad-est\]](#eq:fzoos-grad-est){reference-type="eqref" reference="eq:fzoos-grad-est"}) w.r.t. $\gamma_{r, t-1}$, $\gamma_{r, t-1}$ needs to be chosen as $$\begin{equation}
    \gamma_{r, t-1} = \frac{G}{G + 2\omega\rho^{(r-1)T} + 2N{\epsilon}} \ ,
\end{equation}$$ as shown in our Cor. [1](#co:better-gamma){reference-type="ref" reference="co:better-gamma"}. This better-performing $\gamma_{r, t-1}$ therefore implies that ***(a)*** an adaptive $\gamma_{r, t-1}$ is indeed able to theoretically reduce the gradient disparity, which therefore aligns with the conclusion from our Prop. [1](#prop:opt-correction){reference-type="ref" reference="prop:opt-correction"} and ***(b)*** when the estimation error of our gradient correction vector (characterized by $2\omega\rho^{rT} + 2N{\epsilon}$) in [\[eq:fzoos-grad-est\]](#eq:fzoos-grad-est){reference-type="eqref" reference="eq:fzoos-grad-est"} is smaller than the client heterogeneity (characterized by $G$), a large $\gamma_{t-1}$ is suggested to be applied in order to minimize the gradient disparity $\frac{1}{N} \sum_{i=1}^N \Xi_{r,t}^{(i)}$, as shown in our Sec. [5.1](#sec:est-analysis){reference-type="ref" reference="sec:est-analysis"}.*

*By introducing this $\gamma_{r,t-1}$ into the upper bound in Thm. [1](#th:grad-error){reference-type="ref" reference="th:grad-error"}, we have $$\begin{equation}
\begin{aligned}
    \frac{1}{N} \sum_{i=1}^N \Xi_{r,t}^{(i)} &\stackrel{(a)}{\leq} 4\omega\kappa \rho^{(r-1)T+t-1} + 4\gamma^2_{r, t-1}\left(2\omega\kappa \rho^{(r-1)T}  + 2N{\epsilon}\right) + 4(1 - \gamma_{r, t-1})^2G \\[-6pt]
    &\stackrel{(b)}{=} 4\omega\kappa \rho^{(r-1)T+t-1} + \frac{4G\left(2\omega\kappa \rho^{(r-1)T}  + 2N{\epsilon}\right)}{G + \left(2\omega\rho^{(r-1)T} + 2N{\epsilon}\right)} \\
    &\stackrel{(c)}{\leq} 4\omega\kappa \rho^{(r-1)T+t-1} + 2\sqrt{2G(\omega\kappa \rho^{(r-1)T}  + N{\epsilon})} \\
    &\stackrel{(d)}{\leq} 4\omega\kappa \rho^{(r-1)T+t-1} + 2\sqrt{2\omega\kappa\rho^{(r-1)T}G}  + 2\sqrt{2NG{\epsilon}} \label{eq:temp-cbskv}
\end{aligned}
\end{equation}$$ where $(c)$ is from the inequality of $G + 2\omega\rho^{(r-1)T} + 2N{\epsilon}\geq 2\sqrt{G(2\omega\rho^{(r-1)T} + 2N{\epsilon})}$ (i.e., the relationship between the geometric mean and arithmetic mean of $G$ and $2\omega\rho^{(r-1)T} + 2N{\epsilon}$) and $(d)$ is from the fact that $(\sqrt{2\omega\kappa\rho^{(r-1)T}G} + \sqrt{2NG{\epsilon}})^2 > 2\omega\kappa\rho^{(r-1)T}G + 2NG{\epsilon}$. Interestingly, [\[eq:temp-cbskv\]](#eq:temp-cbskv){reference-type="eqref" reference="eq:temp-cbskv"} enjoys two major aspects. ***(a)*** In contrast to the algorithm where $\gamma_{r,t-1}=0$ (e.g., FedZO), the impact of client heterogeneity (i.e., $G$) is able to be reduced in our FZooS through decreasing the estimation error of our gradient surrogates (i.e., $\omega\kappa\rho^{(r-1)T}$) and the RFF approximation error (i.e., ${\epsilon}$) for our global gradient surrogates. ***(b)*** In contrast to the federated ZOO algorithms where $\gamma_{r,t-1}=1$ (e.g., SCAFFOLD), the impact of the large estimation error of our gradient surrogates (i.e., $\omega\kappa\rho^{(r-1)T}$) is also able to be mitigated in our FZooS through a small client heterogeneity (i.e., $G$) in practice. As a result, these advantages will intuitively make our FZooS produce more robust optimization performance under different scenarios in practice, as supported by our Sec. [6](#sec:exps){reference-type="ref" reference="sec:exps"} and Appx. [13](#app-sec:more){reference-type="ref" reference="app-sec:more"}.*
:::

## Gradient Estimation Analysis Based on Euclidean Distance {#app-sec:prac-gamma}

Of note, for every iteration $t$ of round $r$, our global gradient surrogate in Sec. [4.2.1](#sec:global-surrogates){reference-type="ref" reference="sec:global-surrogates"} is obtained based on the optimization trajectory ${\mathcal{D}}^{(i)}_{r-1, T} = \{({\bm{x}}^{(i)}_{\tau}, y^{(i)}_{\tau})\}_{\tau=1}^{T(r-1)}$ and is not capable of being updated immediately although $t-1$ new function queries are given at this time. This is because the update of our global gradient surrogate only occurs when clients and server can communicate with each other, i.e., at the end of each round. Intuitively, this will result in the phenomenon that the quality of our global gradient surrogate and hence the quality of our [\[eq:fzoos-grad-est\]](#eq:fzoos-grad-est){reference-type="eqref" reference="eq:fzoos-grad-est"} decays w.r.t. the iterations of local updates, as empirically supported in Appx. [13.1](#app-sec:syn){reference-type="ref" reference="app-sec:syn"}. This is likely because the Euclidean distance between the input to be evaluated in our global gradient surrogate and the queried inputs from the optimization trajectory becomes larger and consequently the optimization trajectory becomes less informative. Unfortunately, such a quality decay within the local updates fails to be captured in Thm. [1](#th:grad-error){reference-type="ref" reference="th:grad-error"} and hence may result in an impractical choice of $\gamma_{r,t-1}$ in Cor. [1](#co:better-gamma){reference-type="ref" reference="co:better-gamma"}. To this end, we develop another uncertainty analysis of our global gradient surrogate that is based on Euclidean distance to capture such a phenomenon in this section, which finally gives us a more practical choice of gradient correction length.

We first introduce the following lemma to ease our proof in this section.

::: {#le:same-eigenvalues .lemma}
**Lemma 7**. *For any matrix ${\mathbf{A}}$, ${\mathbf{A}}^{\top}{\mathbf{A}}$ and ${\mathbf{A}}{\mathbf{A}}^{\top}$ share the same non-zero eigenvalues.*
:::

::: proof
*Proof.* Let $\lambda$ be any non-zero eigenvalue of ${\mathbf{A}}^{\top}{\mathbf{A}}$, for some ${\bm{x}}\neq {\bm{0}}$, we have $$\begin{equation}
\begin{aligned}
    {\mathbf{A}}^{\top}{\mathbf{A}}{\bm{x}}= \lambda {\bm{x}}\ .
\end{aligned}
\end{equation}$$ By multiplying ${\mathbf{A}}$ on both sides above, we have $$\begin{equation}
\begin{aligned}
    {\mathbf{A}}{\mathbf{A}}^{\top}\left({\mathbf{A}}{\bm{x}}\right) = \lambda \left({\mathbf{A}}{\bm{x}}\right) \ ,
\end{aligned}
\end{equation}$$ which implies that $\lambda$ is also the eigenvalue of ${\mathbf{A}}{\mathbf{A}}^{\top}$ with ${\mathbf{A}}{\bm{x}}$ being the eigenvector. Following the same proof, it is easy to show that any non-zero eigenvalue of ${\mathbf{A}}{\mathbf{A}}^{\top}$ remains the eigenvalue of ${\mathbf{A}}^{\top}{\mathbf{A}}$, which therefore concludes the proof. ◻
:::

We then introduce another estimation error analysis (different from the one presented in Appx. [10.2](#app-sec:proof:grad-error){reference-type="ref" reference="app-sec:proof:grad-error"}) of our global gradient surrogate as follows where we slightly abuse the notation and use ${\bm{x}}^{(i)}_{\tau} \in {\mathcal{D}}^{(i)}_{r, T}$ to denote that ${\bm{x}}^{(i)}_{\tau}$ is from the optimization trajectory ${\mathcal{D}}^{(i)}_{r, T}$.

::: {#prop:error-to-dist .proposition}
**Proposition 2**. *Let the shift-invariant kernel $k({\bm{x}}, {\bm{x}}') = k(\left\|{\bm{x}}- {\bm{x}}'\right\|^2)$ where $k(\cdot)$ is assumed to be non-increasing and function $h(\iota) = \iota \nabla k(\iota)^2$ is assumed to be convex, the following then holds with a probability of at least $1-\delta$ for any ${\bm{x}}\in {\mathcal{X}}$, $$\begin{equation*}
    \left\|\nabla \mu_{r}({\bm{x}}) - \nabla F({\bm{x}})\right\|^2 \leq \omega\kappa - \frac{4\omega\iota_r^2 \nabla k(\iota_r)^2}{k(0) d  + \sigma^2 d / (rT)}
\end{equation*}$$ where $\omega = d + 2(\sqrt{d}+1)\ln(1/\delta)$, $\iota_r \triangleq \frac{1}{rNT}\sum_{i=1}^N\sum_{{\bm{x}}^{(i)}_{\tau} \in {\mathcal{D}}^{(i)}_{r, T}} \left\|{\bm{x}}- {\bm{x}}^{(i)}_{\tau}\right\|^2$, and $k(0) = k({\bm{x}},{\bm{x}})$.*
:::

::: proof
*Proof.* Recall that the uncertainty measure function (see [\[eq:posterior-derived\]](#eq:posterior-derived){reference-type="eqref" reference="eq:posterior-derived"}) of our local gradient surrogate on client $i$ for iteration $T$ of round $r$ will be $$\begin{equation}
\begin{aligned}
    \partial \left(\sigma_{r,T}^{(i)}\right)^2({\bm{x}}) &= \partial_{{\bm{z}}}\partial_{{\bm{z}}'} k({\bm{z}}, {\bm{z}}') - \partial_{{\bm{z}}} {\bm{k}}^{(i)}_{r,T}({\bm{z}})^{\top}\left({\mathbf{K}}^{(i)}_{r,T}+\sigma^{2} {\mathbf{I}}\right)^{-1} \partial_{{\bm{z}}'} {\bm{k}}^{(i)}_{r,T}({\bm{z}}') \Big|_{{\bm{z}}={\bm{z}}'={\bm{x}}} \\
    &\stackrel{(a)}{\preccurlyeq} \kappa {\mathbf{I}}- \left(\lambda_{\max}({\mathbf{K}}^{(i)}_{r,T}) + \sigma^2 \right)^{-1}\partial_{{\bm{z}}} {\bm{k}}^{(i)}_{r,T}({\bm{z}})^{\top}\partial_{{\bm{z}}'} {\bm{k}}^{(i)}_{r,T}({\bm{z}}') \Big|_{{\bm{z}}={\bm{z}}'={\bm{x}}} \\
    &\stackrel{(b)}{\preccurlyeq} \kappa{\mathbf{I}}- \frac{\partial_{{\bm{z}}} {\bm{k}}^{(i)}_{r,T}({\bm{z}})^{\top}\partial_{{\bm{z}}'} {\bm{k}}^{(i)}_{r,T}({\bm{z}}')\big|_{{\bm{z}}={\bm{z}}'={\bm{x}}}}{rT \max_{{\bm{x}},{\bm{x}}' \in {\mathcal{D}}_{r,T}^{(i)}} k({\bm{x}},{\bm{x}}') + \sigma^2} \label{eq:temp-cemv}
\end{aligned}
\end{equation}$$ where $(a)$ is based on the assumption on $\partial_{{\bm{z}}}\partial_{{\bm{z}}'} k({\bm{z}}, {\bm{z}}')$ in our Sec. [2](#sec:setting){reference-type="ref" reference="sec:setting"} and the definition of maximum eigenvalue. In addition, $(b)$ comes from $\lambda_{\max}({\mathbf{K}}^{(i)}_{r,T}) \leq rT \max_{{\bm{x}},{\bm{x}}' \in {\mathcal{D}}_{r,T}^{(i)}} k({\bm{x}},{\bm{x}}')$ (i.e., the Gershgorin theorem).

Based on the assumption that $k({\bm{x}}, {\bm{x}}') = k(\left\|{\bm{x}}- {\bm{x}}'\right\|^2)$ and $k(\cdot)$ is non-increasing, we have $$\begin{equation}
\begin{aligned}
    \max_{{\bm{x}},{\bm{x}}' \in {\mathcal{D}}_{r,T}^{(i)}} k({\bm{x}},{\bm{x}}') \leq k({\bm{x}},{\bm{x}}) = k(0) \ . \label{eq:temp-3rgx}
\end{aligned}
\end{equation}$$ Moreover, define $\iota \triangleq \left\|{\bm{z}}- {\bm{z}}'\right\|^2$, the partial derivative of kernel $k(\cdot, \cdot)$ will be $$\begin{equation}
\begin{aligned}
    \partial_{{\bm{z}}}k({\bm{z}}, {\bm{z}}') &= 2\left({\bm{z}}- {\bm{z}}'\right) \nabla k(\iota) \\
    \partial_{{\bm{z}}'}k({\bm{z}}, {\bm{z}}') &= 2\left({\bm{z}}' - {\bm{z}}\right) \nabla k(\iota) \ .
\end{aligned}
\end{equation}$$

Therefore, the each element in the $rT \times rT$ matrix $\partial_{{\bm{z}}} {\bm{k}}^{(i)}_{r,T}({\bm{z}})\partial_{{\bm{z}}'} {\bm{k}}^{(i)}_{r,T}({\bm{z}}')^{\top}\big|_{{\bm{z}}={\bm{z}}'={\bm{x}}}$ that is induced by the input pair $({\bm{x}}^{(i)}_{\tau}, {\bm{x}}^{(i)}_{\tau'})$ with ${\bm{x}}^{(i)}_{\tau}, {\bm{x}}^{(i)}_{\tau'} \in {\mathcal{D}}_{r,T}^{(i)}$ and $\tau,\tau' \in [rT]$ will be: $$\begin{equation}
\begin{aligned}
    4\left({\bm{x}}- {\bm{x}}^{(i)}_{\tau}\right)^{\top}\left({\bm{x}}- {\bm{x}}^{(i)}_{\tau'}\right) \nabla k(\iota^{(i)}_{\tau})\nabla k(\iota^{(i)}_{\tau'})
\end{aligned}
\end{equation}$$ where $\iota^{(i)}_{\tau} \triangleq \left\|{\bm{x}}- {\bm{x}}^{(i)}_{\tau}\right\|^2, \iota^{(i)}_{\tau'} \triangleq \left\|{\bm{x}}- {\bm{x}}^{(i)}_{\tau'}\right\|^2$. Based on these results, the trace norm $\left\| \cdot \right\|_{\text{tr}}$ of $\partial_{{\bm{z}}} {\bm{k}}^{(i)}_{r,T}({\bm{z}})\partial_{{\bm{z}}'} {\bm{k}}^{(i)}_{r,T}({\bm{z}}')^{\top}\big|_{{\bm{z}}={\bm{z}}'={\bm{x}}}$ will be $$\begin{equation}
\begin{aligned}
    \left\|\partial_{{\bm{z}}} {\bm{k}}^{(i)}_{r,T}({\bm{z}})\partial_{{\bm{z}}'} {\bm{k}}^{(i)}_{r,T}({\bm{z}}')^{\top}\big|_{{\bm{z}}={\bm{z}}'={\bm{x}}}\right\|_{\text{tr}} &= \sum_{\tau=1}^{rT} 4\left\|{\bm{x}}- {\bm{x}}_{\tau}\right\|^2 \nabla k(\iota_{\tau})^2 \\
    &= \sum_{\tau=1}^{rT} 4\iota_{\tau} \nabla k(\iota_{\tau})^2 \ . \label{eq:temp-csnvs}
\end{aligned}
\end{equation}$$

By further assuming that the function $h(\iota) = \iota \nabla k(\iota)^2$ is convex, we then have $$\begin{equation}
\begin{aligned}
    \left\|\partial_{{\bm{z}}} {\bm{k}}^{(i)}_{r,T}({\bm{z}})^{\top}\partial_{{\bm{z}}'} {\bm{k}}^{(i)}_{r,T}({\bm{z}}')\big|_{{\bm{z}}={\bm{z}}'={\bm{x}}}\right\| &\stackrel{(a)}{\geq} \frac{1}{d} \left\|\partial_{{\bm{z}}} {\bm{k}}^{(i)}_{r,T}({\bm{z}})^{\top}\partial_{{\bm{z}}'} {\bm{k}}^{(i)}_{r,T}({\bm{z}}')\big|_{{\bm{z}}={\bm{z}}'={\bm{x}}}\right\|_{\text{tr}} \\[7.5pt]
    &\stackrel{(b)}{=} \frac{1}{d} \left\|\partial_{{\bm{z}}} {\bm{k}}^{(i)}_{r,T}({\bm{z}}) \partial_{{\bm{z}}'} {\bm{k}}^{(i)}_{r,T}({\bm{z}}')^{\top} \big|_{{\bm{z}}={\bm{z}}'={\bm{x}}}\right\|_{\text{tr}} \\
    % &= \frac{1}{d} \sum_{\tau=1}^{rT} 4\left\|\vx-\vx^{(i)}_{\tau}\right\|^2 \nabla k(\iota^{(i)}_{\tau})^2 \\
    &\stackrel{(c)}{=} \frac{1}{d} \sum_{\tau=1}^{rT} 4\iota^{(i)}_{\tau} \nabla k(\iota^{(i)}_{\tau})^2 \\
    &\stackrel{(d)}{\geq} \frac{4rT}{d} \iota_r^{(i)} \nabla k(\iota_r^{(i)})^2 \label{eq:temp-3hufe}
\end{aligned}
\end{equation}$$ where $(a)$ comes from the fact the maximum eigenvalue of a matrix is always larger or equal to its averaged eigenvalues and $(b)$ is based on Lemma [7](#le:same-eigenvalues){reference-type="ref" reference="le:same-eigenvalues"}. In addition, $(c)$ is obtained from [\[eq:temp-csnvs\]](#eq:temp-csnvs){reference-type="eqref" reference="eq:temp-csnvs"} while $(d)$ results from the definition of $\iota_r^{(i)} \triangleq \frac{1}{rT}\sum_{{\bm{x}}^{(i)}_{\tau} \in {\mathcal{D}}^{(i)}_{r, T}} \left\|{\bm{x}}- {\bm{x}}^{(i)}_{\tau}\right\|^2$ as well as the Jansen's inequality for the convex function $h(\cdot)$.

Finally, by introducing the results above, i.e., [\[eq:temp-3rgx\]](#eq:temp-3rgx){reference-type="eqref" reference="eq:temp-3rgx"} and [\[eq:temp-3hufe\]](#eq:temp-3hufe){reference-type="eqref" reference="eq:temp-3hufe"}, into [\[eq:temp-cemv\]](#eq:temp-cemv){reference-type="eqref" reference="eq:temp-cemv"}, we have $$\begin{equation}
\begin{aligned}
    \left\|\partial \left(\sigma_{r,T}^{(i)}\right)^2({\bm{x}}) \right\| \leq \kappa - \frac{4 \iota_r^{(i)} \nabla k(\iota_r^{(i)})^2}{k(0) d + \sigma^2 d/(rT)} \ .
\end{aligned}
\end{equation}$$

Define $\iota_r \triangleq \frac{1}{N}\sum_{i=1}^N \overline{\iota}_{r}^{(i)}$, we then have $$\begin{equation}
\begin{aligned}
    \left\|\nabla \mu_r({\bm{x}}) - \nabla F({\bm{x}})\right\|^2 &\stackrel{(a)}{=} \left\|\frac{1}{N}\sum_{i=1}^N \left(\nabla \mu^{(i)}_{r,T}({\bm{x}}) - \nabla f_i({\bm{x}})\right)\right\|^2 \\
    &\stackrel{(b)}{\leq} \frac{1}{N} \sum_{i=1}^N \left\|\nabla \mu^{(i)}_{r,T}({\bm{x}}) - \nabla f_i({\bm{x}})\right\|^2 \\
    &\stackrel{(c)}{\leq} \frac{1}{N} \sum_{i=1}^N \omega\kappa - \frac{4\omega\iota_r^{(i)} \nabla k(\iota_r^{(i)})^2}{k(0) d  + \sigma^2 d / (rT)} \\
    &\stackrel{(d)}{\leq} \omega\kappa - \frac{4\omega\iota_r \nabla k(\iota_r)^2}{k(0) d  + \sigma^2 d / (rT)}
\end{aligned}
\end{equation}$$ where $(b)$ is from the Cauchy-Schwarz inequality, $(c)$ derives from Lemma [2](#prop:error-to-dist){reference-type="ref" reference="prop:error-to-dist"}, and $(d)$ results from the Jansen's inequality for convex function $h(\cdot)$. which finally concludes the proof. ◻
:::

::: remark
**Remark 3**. *Of note, the assumption that $k({\bm{x}}, {\bm{x}}') = k(\left\|{\bm{x}}- {\bm{x}}'\right\|^2)$ where $k(\cdot)$ is non-increasing and function $h(\iota) = \iota \nabla k(\iota)^2$ is convex can be satisfied by the widely applied squared exponential kernel $k({\bm{x}},{\bm{x}}') = \exp\left(-\left\|{\bm{x}}- {\bm{x}}'\right\|^2 / (2l^2)\right)$, which has also been applied in our FZooS. To justify the validity of these assumptions on the squared exponential kernel, we first show that this kernel can be represented as $k(\iota) = \exp\left(-\iota / (2l^2)\right)$, which is non-increasing w.r.t. its input $\iota$, and $h(\iota) = \iota \exp\left(-\iota / l^2\right) / (4l^4)$ is convex when $\iota \geq 2l^2$.*

*Remarkably, Prop. [2](#prop:error-to-dist){reference-type="ref" reference="prop:error-to-dist"} reveals that the quality of the gradient estimation at an input ${\bm{x}}\in {\mathcal{X}}$ when using our global gradient surrogate without RFF approximation is highly related to the averaged Euclidean distance between ${\bm{x}}$ and ${\bm{x}}_{\tau} \in \bigcup_{i=1}^N{\mathcal{D}}_{r,T}^{(i)}$ (i.e., $\iota_r$ in Prop. [2](#prop:error-to-dist){reference-type="ref" reference="prop:error-to-dist"}). Specifically, when the input ${\bm{x}}$ to be evaluated in our global gradient surrogate leads to a larger value of $\iota_r \nabla k(\iota_r)^2$, the upper bound in our Prop. [2](#prop:error-to-dist){reference-type="ref" reference="prop:error-to-dist"} demonstrates that the gradient estimation error of our global gradient surrogate tends to be more accurate. Note that when the kernel is the squared exponential kernel, we have that $h(\iota) = \iota \nabla k(\iota)^2 = \iota \exp\left(-\iota / l^2\right) / (4l^4)$ decreases w.r.t. $\iota$ and that a smaller averaged Euclidean distance between ${\bm{x}}$ and ${\bm{x}}_{\tau} \in \bigcup_{i=1}^N{\mathcal{D}}_{r,T}^{(i)}$ likely enjoys a smaller gradient estimation error. This is intuitively aligned with the common practice that ${\bm{x}}_{\tau} \in \bigcup_{i=1}^N{\mathcal{D}}_{r,T}^{(i)}$ is more informative when it achieves a smaller averaged Euclidean distance with ${\bm{x}}$. Intuitively, when the iteration $t$ of local updates is increased, the input ${\bm{x}}_{r,t-1}$ to be evaluated in our global gradient surrogate likely achieves a larger distance with the history of function queries $\bigcup_{i=1}^N{\mathcal{D}}_{r,T}^{(i)}$ and consequently the quality of our global gradient surrogate likely decays, which finally aligns with the phenomenon that we have mentioned at the beginning of this section.*
:::

#### More Practical Choice of $\gamma_{r,t-1}$.

Finally, by introducing Prop. [2](#prop:error-to-dist){reference-type="ref" reference="prop:error-to-dist"} into the analysis in Appx. [10.2](#app-sec:proof:grad-error){reference-type="ref" reference="app-sec:proof:grad-error"}, we achieve the following better-performing choice of gradient correction length $\gamma_{r,t-1}$:

::: {#co:prac-gamma .corollary}
**Corollary 2**. *Based on our Prop. [2](#prop:error-to-dist){reference-type="ref" reference="prop:error-to-dist"}, a better-performing choice choice of $\gamma_{r,t-1}$ should be $$\begin{equation*}
    \gamma_{r,t-1} = \frac{G}{G + 2\left(\omega\kappa - \frac{4\omega\iota_r \nabla k(\iota_r)^2}{k(0) d  + \sigma^2 d / (rT)} + N{\epsilon}\right)} \ .
\end{equation*}$$*
:::

Cor. [2](#co:prac-gamma){reference-type="ref" reference="co:prac-gamma"} implies that $\gamma_{r,t-1}$ should decay w.r.t the iteration $t$ of local updates if $\iota_r \nabla k(\iota_r)^2$ decreases w.r.t. $t$. Particularly, when $k({\bm{x}},{\bm{x}}') = \exp\left(-\left\|{\bm{x}}- {\bm{x}}'\right\|^2 / (2l^2)\right)$ and $\iota_r \nabla k(\iota_r)^2$ decreases at a rate of ${\mathcal{O}}(\frac{1}{t})$ for the iteration $t$ of local updates, we then have that better-performing choice of $\gamma_{r,t-1}$ in Prop. [2](#prop:error-to-dist){reference-type="ref" reference="prop:error-to-dist"} has the form of $\gamma_{r,t-1} = \frac{G}{G + C_0 - C_1/t}$ for some constant $C_0 \geq C_1>0$. Since we usually have no prior knowledge of client heterogeneity $G$ as well as the constants $C_0, C_1$, we commonly apply the approximated form of $\gamma_{r,t-1} = 1/t$, which will be widely applied in our experiments as shown in our Appx. [12](#app-sec:exp-settings){reference-type="ref" reference="app-sec:exp-settings"}.

## Convergence of Algo. [\[alg:fedzoo\]](#alg:fedzoo){reference-type="ref" reference="alg:fedzoo"} {#app-sec:conv-general}

We first introduce the following lemmas that are inspired by the results in [@scaffold].

::: {#le:smooth&convex .lemma}
**Lemma 8**. *For any $\alpha$-strongly convex and $\beta$-smooth function $f$, and any ${\bm{x}}, {\bm{y}}, {\bm{z}}$ in the domain of $f$, we have $$\begin{equation*}
\begin{aligned}
    \nabla f({\bm{x}})^{\top}\left({\bm{y}}- {\bm{z}}\right) \leq f({\bm{y}})-f({\bm{z}}) - \alpha\|{\bm{y}}-{\bm{z}}\|^{2} / 4 + \beta\|{\bm{z}}-{\bm{x}}\|^{2}
\end{aligned}
\end{equation*}$$*
:::

::: proof
*Proof.* Since $f$ is both $\alpha$-strongly convex and $\beta$-smooth, we have that $$\begin{equation}
\begin{aligned}
    f({\bm{z}}) - f({\bm{x}}) &\leq \nabla f({\bm{x}})^{\top}\left({\bm{z}}- {\bm{x}}\right) + \frac{\beta}{2}\left\|{\bm{z}}- {\bm{x}}\right\|^2 \\
    f({\bm{y}}) - f({\bm{x}}) &\geq \nabla f({\bm{x}})^{\top}\left({\bm{y}}- {\bm{x}}\right) + \frac{\alpha}{2}\left\|{\bm{y}}- {\bm{x}}\right\|^2 \ .
\end{aligned}
\end{equation}$$ Note that when $\alpha = 0$, the inequalities above still hold. By aggregating the results above, we have $$\begin{equation}
\begin{aligned}
    f({\bm{z}}) - f({\bm{y}}) &= f({\bm{z}}) - f({\bm{x}}) + f({\bm{x}}) - f({\bm{y}}) \\
    &\leq \nabla f({\bm{x}})^{\top}\left({\bm{z}}- {\bm{x}}\right) + \nabla f({\bm{x}})^{\top}\left({\bm{x}}- {\bm{y}}\right) + \frac{\beta}{2}\left\|{\bm{z}}- {\bm{x}}\right\|^2 - \frac{\alpha}{2}\left\|{\bm{y}}- {\bm{x}}\right\|^2 \\
    &\leq \nabla f({\bm{x}})^{\top}\left({\bm{z}}- {\bm{y}}\right) + \frac{\beta}{2}\left\|{\bm{z}}- {\bm{x}}\right\|^2 - \frac{\alpha}{4}\left\|{\bm{y}}- {\bm{z}}\right\|^2 + \frac{\alpha}{2}\left\|{\bm{x}}- {\bm{z}}\right\|^2 \\
    &= \nabla f({\bm{x}})^{\top}\left({\bm{z}}- {\bm{y}}\right) + \frac{\beta + \alpha}{2}\left\|{\bm{z}}- {\bm{x}}\right\|^2 - \frac{\alpha}{4}\left\|{\bm{y}}- {\bm{z}}\right\|^2 
\end{aligned}
\end{equation}$$ where the second inequality comes from $\alpha\left\|{\bm{y}}- {\bm{x}}\right\|^2/2 \geq \alpha\left\|{\bm{y}}- {\bm{z}}\right\|^2/4 - \alpha\left\|{\bm{x}}- {\bm{z}}\right\|^2/2$ (triangle inequality). When $\alpha>0$, since $\beta > \alpha$, we have $$\begin{align}
    f({\bm{z}}) - f({\bm{y}}) \leq \nabla f({\bm{x}})^{\top}\left({\bm{z}}- {\bm{y}}\right) + \beta\left\|{\bm{z}}- {\bm{x}}\right\|^2 - \frac{\alpha}{4}\left\|{\bm{y}}- {\bm{z}}\right\|^2 \ .
\end{align}$$ By rearranging the inequality above, we can directly derive the result in Lemma [8](#le:smooth&convex){reference-type="ref" reference="le:smooth&convex"} with $\alpha >0$. Even when $\alpha=0$, since $\left\|{\bm{z}}- {\bm{x}}\right\|^2 \geq 0$, we have $$\begin{equation}
\begin{aligned}
    f({\bm{z}}) - f({\bm{y}}) &\leq \nabla f({\bm{x}})^{\top}\left({\bm{z}}- {\bm{y}}\right) + \frac{\beta}{2}\left\|{\bm{z}}- {\bm{x}}\right\|^2 \\
    &\leq \nabla f({\bm{x}})^{\top}\left({\bm{z}}- {\bm{y}}\right) + \beta \left\|{\bm{z}}- {\bm{x}}\right\|^2 \ .
\end{aligned}
\end{equation}$$ By rearranging the inequality above, we show that the result in Lemma [8](#le:smooth&convex){reference-type="ref" reference="le:smooth&convex"} also holds for $\alpha = 0$. ◻
:::

::: {#le:contractive .lemma}
**Lemma 9**. *For any $\beta$-smooth function $f$, inputs ${\bm{x}}, {\bm{y}}$ in the domain of $f$, the following holds for any $\eta>0$ $$\begin{equation*}
\|{\bm{x}}-\eta \nabla f({\bm{x}})-{\bm{y}}+\eta \nabla f({\bm{y}})\|^{2} \leq (1+\eta\beta)^2\|{\bm{x}}-{\bm{y}}\|^{2} \ . \label{eq:contractive-1}
\end{equation*}$$*
:::

::: proof
*Proof.* Since $f$ is $\beta$-smooth, we have $$\begin{equation}
\begin{aligned}
    \left\|{\bm{x}}-\eta \nabla f({\bm{x}})-{\bm{y}}+\eta \nabla f({\bm{y}})\right\|^{2} &\leq \left(1 + \frac{1}{a}\right)\left\|{\bm{x}}- {\bm{y}}\right\|^2 + \left(1 + a\right)\eta^2\left\|\nabla f({\bm{x}}) - \nabla f({\bm{y}})\right\|^2 \\
    &\leq \left(1 + \frac{1}{a} + \left(1+a\right)\eta^2\beta^2\right)\left\|{\bm{x}}- {\bm{y}}\right\|^2
\end{aligned}
\end{equation}$$ where the first inequality derives from Lemma [5](#le:triangle){reference-type="ref" reference="le:triangle"} and the second inequality comes from the smoothness of $f$. By choosing $a=1/(\eta\beta)$, we conclude our proof. ◻
:::

:::: remark
**Remark 4**. *Lemma [9](#le:contractive){reference-type="ref" reference="le:contractive"} only requires the smoothness of function $f$. When $f$ is both $\beta$-smooth and $\alpha$-strongly convex ($\alpha > 0$), we will have a tighter bound as below when $\eta < \alpha / \beta^2$ (see proof below), $$\begin{align}
    \|{\bm{x}}-\eta \nabla f({\bm{x}})-{\bm{y}}+\eta \nabla f({\bm{y}})\|^{2} \leq (1-\eta\alpha)\|{\bm{x}}-{\bm{y}}\|^{2} \ , \label{eq:contractive-2}
\end{align}$$ which can lead to a better convergence (by achieving a smaller constant term) compared with the inequality [\[eq:inter-3\]](#eq:inter-3){reference-type="eqref" reference="eq:inter-3"} we will prove later. However, for simplicity and consistency under various assumptions on the function to be optimized, we only use Lemma [9](#le:contractive){reference-type="ref" reference="le:contractive"} for the convergence analysis of our Thm. [2](#th:convergence-fzoos){reference-type="ref" reference="th:convergence-fzoos"} in the main paper.*

::: proof
**Proof.* Based on the strong convexity of $f$, for any inputs ${\bm{x}}, {\bm{y}}$ in the domain of $f$, we have $$\begin{equation}
\begin{aligned}
    f({\bm{y}}) - f({\bm{x}}) \geq \nabla f({\bm{x}})^{\top}({\bm{y}}- {\bm{x}}) + \frac{\alpha}{2}\left\|{\bm{y}}- {\bm{x}}\right\|^2 \ , \\
    f({\bm{x}}) - f({\bm{y}}) \geq \nabla f({\bm{y}})^{\top}({\bm{x}}- {\bm{y}}) + \frac{\alpha}{2}\left\|{\bm{y}}- {\bm{x}}\right\|^2 \ .
\end{aligned}
\end{equation}$$ By summing up these inequalities, we have $$\begin{equation}
\begin{aligned}
    \left(\nabla f({\bm{y}}) - \nabla f({\bm{x}})\right)^{\top}({\bm{y}}- {\bm{x}}) \geq \alpha \left\|{\bm{y}}- {\bm{x}}\right\|^2 \ . \label{eq:strong-conv-contractive}
\end{aligned}
\end{equation}$$ Finally, we have $$\begin{equation}
\begin{aligned}
     &\left\|{\bm{x}}-\eta \nabla f({\bm{x}})-{\bm{y}}+\eta \nabla f({\bm{y}})\right\|^{2} \\
     \stackrel{(a)}{=}&\left\|{\bm{x}}-{\bm{y}}\right\|^2 + \eta^2\left\|\nabla f({\bm{x}})-\nabla f({\bm{y}})\right\|^2 -2\eta\left(\nabla f({\bm{x}})-\nabla f({\bm{y}})\right)^{\top}\left({\bm{x}}- {\bm{y}}\right) \\
     \stackrel{(b)}{\leq}& \left\|{\bm{x}}-{\bm{y}}\right\|^2 + \eta^2\beta^2\left\|{\bm{x}}-{\bm{y}}\right\|^2 -2\eta\alpha\left\|{\bm{x}}-{\bm{y}}\right\|^2 \\
     \stackrel{(c)}{=}&\left(1 + \eta^2\beta^2 - 2\eta\alpha\right)\left\|{\bm{x}}-{\bm{y}}\right\|^2 \label{eq:inter-2}
     % \stackrel{(d)}{\leq}&\left(1 - \eta\alpha\right)\left\|\vx-\vy\right\|^2
\end{aligned}
\end{equation}$$ where $(b)$ comes from the smoothness of $f$ and [\[eq:strong-conv-contractive\]](#eq:strong-conv-contractive){reference-type="eqref" reference="eq:strong-conv-contractive"}. Since $\alpha>0$, by introducing $\eta\leq \alpha / \beta^2$ into [\[eq:inter-2\]](#eq:inter-2){reference-type="eqref" reference="eq:inter-2"}, we can complete our proof. ◻*
:::
::::

::: {#le:bound-grad .lemma}
**Lemma 10**. *Let $f$ be $\beta$-smooth and ${\bm{x}}^* = \mathop{\mathrm{arg\,min}}f({\bm{x}})$, then for any input ${\bm{x}}$ in the domain of $f$, the following holds $$\begin{equation*}
\left\|\nabla f({\bm{x}})\right\|^2 \leq 2\beta\left(f({\bm{x}}) - f({\bm{x}}^*)\right)
\end{equation*}$$*
:::

::: proof
*Proof.* Since $f$ is $\beta$-smooth, we have the following inequality for any $x,y$ in the domain of $f$ $$\begin{equation}
\begin{aligned}
    f({\bm{y}}) \leq f({\bm{x}}) + \nabla f({\bm{x}})^{\top}({\bm{y}}- {\bm{x}}) + \frac{\beta}{2}\left\|{\bm{y}}- {\bm{x}}\right\|^2 \ .
\end{aligned}
\end{equation}$$ By setting ${\bm{y}}= {\bm{x}}- \nabla f({\bm{x}}) / \beta$, we have $$\begin{equation}
\begin{aligned}
    f({\bm{x}}^*) &\leq f({\bm{x}}- \frac{1}{\beta}\nabla f({\bm{x}})) \\
    &\leq f({\bm{x}}) + \nabla f({\bm{x}})^{\top}\left({\bm{x}}- \frac{1}{\beta}\nabla f({\bm{x}}) - {\bm{x}}\right) + \frac{\beta}{2}\left\|{\bm{x}}- \frac{1}{\beta}\nabla f({\bm{x}}) - {\bm{x}}\right\|^2 \\
    &= f({\bm{x}}) - \frac{1}{2\beta} \left\|\nabla f({\bm{x}})\right\|^2 \ .
\end{aligned}
\end{equation}$$ We finally conclude our proof by rearranging the inequality above. ◻
:::

We then bound the drift between ${\bm{x}}^{(i)}_{r,t}$ and ${\bm{x}}_r$ for every iteration $t$ of any round $r$ as below, which is the key difference between the convergence of general federated ZOO and centralized optimization.

::: {#le:drift .lemma}
**Lemma 11**. *Assume that $F$ is $\beta$-smooth. Then the updated input ${\bm{x}}^{(i)}_{r,t}$ at any iteration $t\geq1$ of round $r\geq1$ on client $i$ in Algo. [\[alg:fedzoo\]](#alg:fedzoo){reference-type="ref" reference="alg:fedzoo"} has the following bounded drift with $\eta \leq \frac{1}{\beta T}$ $$\begin{equation*}
\begin{aligned}
    \left\|{\bm{x}}^{(i)}_{r+1,t} - {\bm{x}}_r\right\|^2 \leq 2\eta^2 T \sum_{\tau=1}^{t} S^{t-\tau}\Xi_{r+1,\tau}^{(i)} + 22\eta^2 T^2\left\|\nabla F({\bm{x}}_r)\right\|^2
    % 22\eta^2 T^2 \left(\Xi^{(i)}_r + \left\|\nabla F(\vx_r)\right\|^2\right) \ .
\end{aligned}
\end{equation*}$$ where $S \triangleq (T+1)^2/(T(T-1))$.*
:::

::: proof
*Proof.* Since ${\bm{x}}^{(i)}_{r+1,t} = {\bm{x}}^{(i)}_{r+1,t-1} - \eta \widehat{{\bm{g}}}^{(i)}_{r+1,t-1}$, we have the following inequalities when $T>1$ $$\begin{equation}
\begin{aligned}
    &\left\|{\bm{x}}^{(i)}_{r+1,t} - {\bm{x}}_r\right\|^2 \\
    \stackrel{(a)}{=}& \left\|{\bm{x}}^{(i)}_{r+1,t-1} - \eta \widehat{{\bm{g}}}^{(i)}_{r+1,t-1} - {\bm{x}}_r\right\|^2 \\
    \stackrel{(b)}{=}&\left\|{\bm{x}}^{(i)}_{r+1,t-1} - \eta\nabla F({\bm{x}}^{(i)}_{r+1,t-1}) + \eta\nabla F({\bm{x}}_r) - {\bm{x}}_r + \eta\left(\nabla F({\bm{x}}^{(i)}_{r+1,t-1}) - \widehat{{\bm{g}}}^{(i)}_{r+1,t-1} - \nabla F({\bm{x}}_r)\right)\right\|^2 \\
    \stackrel{(c)}{\leq}& \frac{T}{T-1}\left\|{\bm{x}}^{(i)}_{r+1,t-1} - \eta\nabla F({\bm{x}}^{(i)}_{r+1,t-1}) + \eta\nabla F({\bm{x}}_r) - {\bm{x}}_r\right\|^2 \\
    &\qquad\qquad + \eta^2 T\left\|\nabla F({\bm{x}}^{(i)}_{r+1,t-1}) - \widehat{{\bm{g}}}^{(i)}_{r+1,t-1} - \nabla F({\bm{x}}_r)\right\|^2 \\
    \stackrel{(d)}{\leq}& \frac{T}{T-1}\left\|{\bm{x}}^{(i)}_{r+1,t-1} - \eta\nabla F({\bm{x}}^{(i)}_{r+1,t-1}) + \eta\nabla F({\bm{x}}_r) - {\bm{x}}_r\right\|^2 \\
    &\qquad\qquad + 2\eta^2 T\left[\left\|\nabla F({\bm{x}}^{(i)}_{r+1,t-1}) - \widehat{{\bm{g}}}^{(i)}_{r+1,t-1}\right\|^2 + \left\|\nabla F({\bm{x}}_r)\right\|^2\right] \label{eq:inter-1}
\end{aligned}
\end{equation}$$ where $(c)$ and $(d)$ come from the [\[eq:triangle-2\]](#eq:triangle-2){reference-type="eqref" reference="eq:triangle-2"} in Lemma [5](#le:triangle){reference-type="ref" reference="le:triangle"} by setting $a=1/(T-1)$ and $a=1$, respectively. Since $F$ is $\beta$-smooth, we can introduce Lemma [9](#le:contractive){reference-type="ref" reference="le:contractive"} into [\[eq:inter-1\]](#eq:inter-1){reference-type="eqref" reference="eq:inter-1"} to obtain the following result given the constant $S \triangleq (T+1)^2/(T(T-1))$ $$\begin{equation}
\begin{aligned}
    &\left\|{\bm{x}}^{(i)}_{r+1,t} - {\bm{x}}_r\right\|^2 \\
    \stackrel{(a)}{\leq}& \frac{T(1+\eta\beta)^2}{T-1} \left\|{\bm{x}}^{(i)}_{r+1,t-1} - {\bm{x}}_r\right\|^2 + 2\eta^2 T\left[\left\|\nabla F({\bm{x}}^{(i)}_{r+1,t-1}) - \widehat{{\bm{g}}}^{(i)}_{r+1,t-1}\right\|^2 + \left\|\nabla F({\bm{x}}_r)\right\|^2\right] \\
    \stackrel{(b)}{=}& 2\eta^2 T \sum_{\tau=0}^{t-1} \left(\frac{T(1+\eta\beta)^2}{T-1}\right)^{t-\tau-1} \left\|\nabla F({\bm{x}}^{(i)}_{r+1,\tau}) - \widehat{{\bm{g}}}^{(i)}_{r+1,\tau}\right\|^2 + 2\eta^2 T \left\|\nabla F({\bm{x}}_r)\right\|^2 \sum_{\tau=0}^{t-1} \left(\frac{(1+\eta\beta)^2T}{T-1}\right)^{\tau} \\
    \stackrel{(c)}{\leq}& 2\eta^2 T \sum_{\tau=0}^{t-1} \left(\frac{(T+1)^2}{T(T-1)}\right)^{t-\tau-1} \left\|\nabla F({\bm{x}}^{(i)}_{r+1,\tau}) - \widehat{{\bm{g}}}^{(i)}_{r+1,\tau}\right\|^2 + 2\eta^2 T \left\|\nabla F({\bm{x}}_r)\right\|^2 \sum_{\tau=0}^{t-1} \left(\frac{(T+1)^2}{T(T-1)}\right)^{\tau} \\
    \stackrel{(d)}{\leq}& 2\eta^2 T \sum_{\tau=0}^{t-1} S^{t-\tau-1}\left\|\nabla F({\bm{x}}^{(i)}_{r+1,\tau}) - \widehat{{\bm{g}}}^{(i)}_{r+1,\tau}\right\|^2 + 22\eta^2 T^2\left\|\nabla F({\bm{x}}_r)\right\|^2  \\
    \stackrel{(e)}{=}& 2\eta^2 T \sum_{\tau=1}^{t} S^{t-\tau}\Xi_{r+1,\tau}^{(i)} + 22\eta^2 T^2\left\|\nabla F({\bm{x}}_r)\right\|^2 % \\[8pt]
\end{aligned}
\end{equation}$$ where $(b)$ comes from the summation of geometric series and $(c)$ is from the fact that $\eta \leq 1/(\beta T)$. In addition, $(d)$ results from the definition of $S$ as well as the following results $$\begin{equation}
\begin{aligned}
    \sum_{\tau=0}^{t-1} \left(\frac{(T+1)^2}{T(T-1)}\right)^{\tau} &\leq \sum_{\tau=0}^{T-1} \left(\frac{(T+1)^2}{T(T-1)}\right)^{\tau} \\
    &= \frac{\left((T+1)^2/[T(T-1)]\right)^T - 1}{(T+1)^2/[T(T-1)] - 1} \\
    &= \frac{T(T-1)}{3T+1}\left(\left(1 + \frac{3T+1}{T(T-1)}\right)^T - 1\right) \\
    &< \frac{T(T-1)}{3T+1}\left(\exp\left(\frac{3T+1}{T}\right) - 1\right) \\
    &< \frac{T}{3}\left(\exp\left(\frac{7}{2}\right) - 1\right) \\[7pt]
    &< 11T \ . \label{eq:inter-3}
\end{aligned}
\end{equation}$$ Finally, $(e)$ results from the definition of $\Xi^{(i)}_{r+1,t} \triangleq \left\|\widehat{{\bm{g}}}_{r+1,t-1} - \nabla F({\bm{x}}_{r+1,t-1}^{(i)})\right\|^2$ in our Sec. [3.2](#sec:challenges){reference-type="ref" reference="sec:challenges"}. ◻
:::

We finally present the convergence of Algo. [\[alg:fedzoo\]](#alg:fedzoo){reference-type="ref" reference="alg:fedzoo"} in the following theorem for the general federated ZOO framework, which then can be easily applied to prove the convergence of our FZooS in Appx. [10.5](#app-sec:proof:conv-fzoos){reference-type="ref" reference="app-sec:proof:conv-fzoos"} and the convergence of existing federated ZOO algorithms in Appx. [11](#app-sec:existing){reference-type="ref" reference="app-sec:existing"}.

::: {#th:conv-general .theorem}
**Theorem 3**. *Define $\Xi^{(i)}_{r,t} \triangleq \sum_{t=1}^T \left\|\widehat{{\bm{g}}}^{(i)}_{r,t-1} - \nabla F({\bm{x}}^{(i)}_{r,t-1})\right\|^2$, $S \triangleq (T+1)^2/(T(T-1))$, and ${\bm{x}}^* \triangleq \mathop{\mathrm{arg\,min}}F({\bm{x}})$. Algo. [\[alg:fedzoo\]](#alg:fedzoo){reference-type="ref" reference="alg:fedzoo"} then has the following convergence when $F$ is under different assumptions:*

1.  *When $F$ is $\beta$-smooth and $\alpha$-strongly convex, by defining $p_r \triangleq \frac{(1 - \alpha \eta T / 4)^{R-r}}{\sum_{r=0}^R \left(1-\alpha\eta T / 4\right)^{R-r}}$ and choosing a constant learning rate $\eta \leq \frac{1}{10\beta T}$, $$\begin{equation*}
    \begin{aligned}
        \min_{r \in [R+1)} F({\bm{x}}_r) - F({\bm{x}}^*) &\leq 2 \alpha \exp\left(-\frac{\alpha\eta TR}{4}\right)\left\|{\bm{x}}_0 - {\bm{x}}^*\right\|^2 \\
        &\qquad + \sum_{r=0}^{R}\sum_{i=1}^N\sum_{t=1}^T p_r\left(\frac{\eta}{NT}\sum_{\tau=1}^{t} S^{t-\tau}\Xi_{r+1,\tau}^{(i)} + \frac{8(\eta T + 1/\alpha)}{\alpha NT}\Xi_{r+1,t}^{(i)}\right) \ .
    \end{aligned}
    \end{equation*}$$*

2.  *When $F$ is $\beta$-smooth and convex, by choosing a constant learning rate $\eta \leq \frac{1}{10\beta T}$, $$\begin{equation*}
    \begin{aligned}
        \min_{r \in [R+1)} F({\bm{x}}_r) - F({\bm{x}}^*) &\leq \frac{2\left\|{\bm{x}}_0 - {\bm{x}}^*\right\|^2}{\eta RT} + \frac{1}{R}\sum_{r=0}^{R}\sum_{i=1}^N\sum_{t=1}^T \left(\frac{\eta}{NT}\sum_{\tau=1}^{t} S^{t-\tau}\Xi_{r+1,\tau}^{(i)}\right. \\
        &\qquad \left. + \frac{8\eta}{N}\Xi_{r+1,t}^{(i)} + \frac{4\sqrt{d}}{NT}\sqrt{\Xi_{r+1,t}^{(i)}}\right) \ .
    \end{aligned}
    \end{equation*}$$*

3.  *When $F$ is only $\beta$-smooth, by choosing a constant learning rate $\eta \leq \frac{7}{100\beta T}$, $$\begin{equation*}
    \begin{aligned}
        \min_{r \in [R+1)} \left\|\nabla F({\bm{x}}_r)\right\|^2 &\leq \frac{13(F({\bm{x}}_0) - F({\bm{x}}^*))}{\eta RT} + \frac{13}{\eta RT}\sum_{r=0}^R\sum_{i=1}^N\sum_{t=1}^T \left(\frac{\left(0.14 \eta + 1/(2\beta T)\right)}{N}\Xi_{r+1,t}^{(i)} \right. \\
        &\qquad \left. + \frac{1.02\eta^2 \beta}{N}\sum_{\tau=1}^{t} S^{t-\tau}\Xi_{r+1,\tau}^{(i)} \right) \ .
    \end{aligned}
    \end{equation*}$$*
:::

::: proof
*Proof.* Recall that the global update on server in Algo. [\[alg:fedzoo\]](#alg:fedzoo){reference-type="ref" reference="alg:fedzoo"} is given as $$\begin{equation}
\begin{aligned}
    {\bm{x}}_{r+1} &= \frac{1}{N} \sum_{i=1}^N {\bm{x}}_{r+1}^{(i)} = \frac{1}{N} \sum_{i=1}^N \left({\bm{x}}_{r}^{(i)} - \eta \sum_{t=1}^T \widehat{{\bm{g}}}^{(i)}_{r+1,t-1}\right) = {\bm{x}}_{r} - \frac{\eta}{N} \sum_{i=1}^N \sum_{t=1}^T \widehat{{\bm{g}}}^{(i)}_{r+1,t-1} \ . \label{eq:temp-vbbv}
\end{aligned}
\end{equation}$$ Therefore, we have $$\begin{equation}
\begin{aligned}
    \left\|{\bm{x}}_{r+1} - {\bm{x}}^* \right\|^2 &= \left\|{\bm{x}}_{r} -  \frac{\eta}{N} \sum_{i=1}^N \sum_{t=1}^T \widehat{{\bm{g}}}^{(i)}_{r+1,t-1} - {\bm{x}}^*\right\|^2 \\
    &= \left\|{\bm{x}}_{r} - {\bm{x}}^*\right\|^2 \underbrace{- 2\left({\bm{x}}_r - {\bm{x}}^*\right)^{\top} \frac{\eta}{N}\sum_{i=1}^{N} \sum_{t=1}^T \widehat{{\bm{g}}}^{(i)}_{r+1,t-1}}_{\tikz[baseline=(char.base)]{\node[shape=circle,draw,inner sep=0.2pt] (char) {1};}} + \underbrace{\left\|\frac{\eta}{N} \sum_{i=1}^{N} \sum_{t=1}^T \widehat{{\bm{g}}}^{(i)}_{r+1,t-1}\right\|^2}_{\tikz[baseline=(char.base)]{\node[shape=circle,draw,inner sep=0.2pt] (char) {2};}}  \ . \label{eq:temp-vgjern}
\end{aligned}
\end{equation}$$ We then bound $\tikz[baseline=(char.base)]{\node[shape=circle,draw,inner sep=0.2pt] (char) {1};}$ and $\tikz[baseline=(char.base)]{\node[shape=circle,draw,inner sep=0.2pt] (char) {2};}$ based on the different assumptions on $F$ separately.

#### Strongly Convex $F$.

Since $F$ is $\beta$-smooth and $\alpha$-strongly convex, we have $$\begin{equation}
\begin{aligned}
    \tikz[baseline=(char.base)]{\node[shape=circle,draw,inner sep=0.2pt] (char) {1};} &\stackrel{(a)}{=} 2\left({\bm{x}}^* - {\bm{x}}_r\right)^{\top} \frac{\eta}{N}\sum_{i=1}^{N} \sum_{t=1}^T \left(\widehat{{\bm{g}}}^{(i)}_{r+1,t-1} - \nabla F({\bm{x}}^{(i)}_{r+1,t-1}) \right) + 2\left({\bm{x}}^* - {\bm{x}}_r\right)^{\top}\frac{\eta}{N}\sum_{i=1}^{N}\sum_{t=1}^T \nabla F({\bm{x}}^{(i)}_{r+1,t-1}) \\
    &\stackrel{(b)}{\leq} 2\left\|{\bm{x}}^* - {\bm{x}}_r\right\| \frac{\eta}{N}\sum_{i=1}^{N}\sum_{t=1}^T \left\|\widehat{{\bm{g}}}^{(i)}_{r+1,t-1} - \nabla F({\bm{x}}^{(i)}_{r+1,t-1}) \right\| \\
    &\qquad\qquad + \frac{2\eta}{N} \sum_{i=1}^{N}\sum_{t=1}^T \left[F({\bm{x}}^*) - F({\bm{x}}_r) - \frac{\alpha}{4}\left\|{\bm{x}}_r - {\bm{x}}^*\right\|^2 + \beta \left\|{\bm{x}}^{(i)}_{r,t-1} - {\bm{x}}_r\right\|^2\right] \\
    &\stackrel{(c)}{\leq} \frac{2\eta}{N}\left\|{\bm{x}}^* - {\bm{x}}_r\right\| \sum_{i=1}^{N}\sum_{t=1}^T \sqrt{\Xi_{r+1,t}^{(i)}} + 2\eta T \big[F({\bm{x}}^*) - F({\bm{x}}_r)\big] - \frac{\alpha\eta T}{2}\left\|{\bm{x}}_r - {\bm{x}}^*\right\|^2 \\
    &\qquad\qquad + \frac{4\eta^3T\beta}{N}\sum_{i=1}^N\sum_{t=1}^T \sum_{\tau=1}^{t} S^{t-\tau}\Xi_{r+1,\tau}^{(i)} + 44\eta^3T^3\beta\left\|\nabla F({\bm{x}}_r)\right\|^2 \\
    &\stackrel{(d)}{\leq} - \frac{\alpha\eta T}{4} \left\|{\bm{x}}^* - {\bm{x}}_r\right\|^2 + 2\eta T \big[F({\bm{x}}^*) - F({\bm{x}}_r)\big] + 44\eta^3T^3\beta \left\|\nabla F({\bm{x}}_r)\right\|^2 + \\
    &\qquad\qquad \sum_{i=1}^N\sum_{t=1}^T \left(\frac{4\eta^3 T\beta}{N}\sum_{\tau=1}^{t} S^{t-\tau}\Xi_{r+1,\tau}^{(i)} + \frac{4\eta}{\alpha N}\Xi_{r+1,t}^{(i)}\right) \ . \label{eq:inter-6}
\end{aligned}
\end{equation}$$ where $(b)$ is from Lemma [8](#le:smooth&convex){reference-type="ref" reference="le:smooth&convex"} by setting ${\bm{y}}={\bm{x}}^*$, ${\bm{z}}={\bm{x}}_r$ and ${\bm{x}}={\bm{x}}_{r,t-1}^{(i)}$ in Lemma [8](#le:smooth&convex){reference-type="ref" reference="le:smooth&convex"}. In addition, $(c)$ comes from the definition of $\Xi^{(i)}_{r+1,t} \triangleq \left\|\widehat{{\bm{g}}}_{r+1,t-1} - \nabla F({\bm{x}}_{r+1,t-1}^{(i)})\right\|^2$ in our Sec. [3.2](#sec:challenges){reference-type="ref" reference="sec:challenges"} and Lemma [11](#le:drift){reference-type="ref" reference="le:drift"}. Finally, $(d)$ comes from the following results $$\begin{equation}
\begin{aligned}
    \frac{2\eta}{N}\left\|{\bm{x}}^* - {\bm{x}}_r\right\| \sum_{i=1}^{N}\sum_{t=1}^T \sqrt{\Xi_{r+1,t}^{(i)}} &= \frac{2\eta}{N} \sum_{i=1}^{N} \sum_{t=1}^T \left\|{\bm{x}}^* - {\bm{x}}_r\right\|\sqrt{\Xi_{r+1,t}^{(i)}} \\
    &\leq \frac{\eta}{N}\sum_{i=1}^{N} \sum_{t=1}^T \left(\frac{\alpha}{4}\left\|{\bm{x}}^* - {\bm{x}}_r\right\|^2 + \frac{4}{\alpha}\Xi_{r+1,t}^{(i)}\right) \\
    &= \frac{\alpha\eta T}{4} \left\|{\bm{x}}^* - {\bm{x}}_r\right\|^2 + \frac{4\eta}{\alpha N} \sum_{i=1}^{N}\sum_{t=1}^T \Xi_{r+1,t}^{(i)} \ . \label{eq:temp-cjwnc}
\end{aligned}
\end{equation}$$

We then bound term $\tikz[baseline=(char.base)]{\node[shape=circle,draw,inner sep=0.2pt] (char) {2};}$ in [\[eq:temp-vgjern\]](#eq:temp-vgjern){reference-type="eqref" reference="eq:temp-vgjern"} as below $$\begin{equation}
\begin{aligned}
    \tikz[baseline=(char.base)]{\node[shape=circle,draw,inner sep=0.2pt] (char) {2};} &\stackrel{(a)}{=} \left\|\frac{\eta}{N} \sum_{i=1}^{N} \sum_{t=1}^T \widehat{{\bm{g}}}^{(i)}_{r+1,t-1}\right\|^2 \\
    &\stackrel{(b)}{=}\left\|\frac{\eta}{N} \sum_{i=1}^{N} \sum_{t=1}^T \left(\widehat{{\bm{g}}}^{(i)}_{r+1,t-1} - \nabla F({\bm{x}}^{(i)}_{r+1,t-1}) + \nabla F({\bm{x}}^{(i)}_{r+1,t-1}) - \nabla F({\bm{x}}_r)\right) + \eta T \nabla F({\bm{x}}_r)\right\|^2 \\
    &\stackrel{(c)}{\leq} \frac{2\eta^2 T}{N} \sum_{i=1}^{N} \sum_{t=1}^T \left(2\left\|\widehat{{\bm{g}}}^{(i)}_{r+1,t-1} - \nabla F({\bm{x}}^{(i)}_{r+1,t-1})\right\|^2 + 2\left\|\nabla F({\bm{x}}^{(i)}_{r+1,t-1}) - \nabla F({\bm{x}}_r)\right\|^2\right) + \\
    &\qquad\qquad 2\eta^2T^2 \left\|\nabla F({\bm{x}}_r)\right\|^2 \\
    &\stackrel{(d)}{\leq} \frac{4\eta^2 T}{N} \sum_{i=1}^{N}\sum_{t=1}^T \Xi_{r+1,t}^{(i)} + \frac{4\eta^2 T\beta^2}{N} \sum_{i=1}^{N} \sum_{t=1}^T \left\|{\bm{x}}^{(i)}_{r+1,t-1} - {\bm{x}}_r\right\|^2 + 2\eta^2T^2 \left\|\nabla F({\bm{x}}_r)\right\|^2 \\
    &\stackrel{(e)}{\leq} \sum_{i=1}^N\sum_{t=1}^T \left(\frac{8\eta^4 T^2 \beta^2}{N}\sum_{\tau=1}^{t} S^{t-\tau}\Xi_{r+1,\tau}^{(i)} + \frac{4\eta^2 T}{N}\Xi_{r+1,t}^{(i)}\right) + \left(88\eta^4T^4\beta^2 + 2\eta^2 T^2\right) \left\|\nabla F({\bm{x}}_r)\right\|^2 \label{eq:temp-sivbnw}
\end{aligned}
\end{equation}$$ where $(c)$ is obtained by applying Lemma [5](#le:triangle){reference-type="ref" reference="le:triangle"} multiple times and $(d)$ is from the smoothness of $F$. Besides, $(e)$ comes from our Lemma [11](#le:drift){reference-type="ref" reference="le:drift"} and the fact that $\eta \leq 1/(\beta T)$.

By combining [\[eq:inter-6\]](#eq:inter-6){reference-type="eqref" reference="eq:inter-6"} and [\[eq:temp-sivbnw\]](#eq:temp-sivbnw){reference-type="eqref" reference="eq:temp-sivbnw"}, we have $$\begin{equation}
\begin{aligned}
    &\left\|{\bm{x}}_{R+1} - {\bm{x}}^* \right\|^2  \\
    \stackrel{(a)}{\leq}& \left(1-\frac{\alpha\eta T}{4}\right)\left\|{\bm{x}}_R - {\bm{x}}^*\right\|^2 + 2\eta T\big[F({\bm{x}}^*) - F({\bm{x}}_R)\big] \\
    &\qquad + 2\eta^2 T^2\left(44\eta^2T^2\beta^2 + 22\eta T \beta + 1\right)\left\|\nabla F({\bm{x}}_R)\right\|^2 \\
    &\qquad\qquad + \sum_{i=1}^N\sum_{t=1}^T \left(\frac{4\eta^3 T\beta(2\eta T \beta + 1)}{N}\sum_{\tau=1}^{t} S^{t-\tau}\Xi_{R+1,\tau}^{(i)} + \frac{4\eta(\eta T + 1/\alpha)}{\alpha N}\Xi_{R+1,t}^{(i)}\right) \\
    \stackrel{(b)}{\leq}&  \left(1-\frac{\alpha\eta T}{4}\right)\left\|{\bm{x}}_R - {\bm{x}}^*\right\|^2 + 2\eta T\left(1 - 2\eta T\beta \left(44\eta^2T^2\beta^2 + 22\eta T \beta + 1\right)\right)\big[F({\bm{x}}^*) - F({\bm{x}}_R)\big] \\
    &\qquad + \sum_{i=1}^N\sum_{t=1}^T \left(\frac{4\eta^3 T\beta(2\eta T \beta + 1)}{N}\sum_{\tau=1}^{t} S^{t-\tau}\Xi_{r+1,\tau}^{(i)} + \frac{4\eta(\eta T + 1/\alpha)}{\alpha N}\Xi_{r+1,t}^{(i)}\right) \\
    \stackrel{(c)}{=}& \left(1-\frac{\alpha\eta T}{4}\right)^{R+1}\left\|{\bm{x}}_0 - {\bm{x}}^*\right\|^2 + \sum_{r=0}^{R}\left(1-\frac{\alpha\eta T}{4}\right)^{R-r} H \big[F({\bm{x}}^*) - F({\bm{x}}_r)\big]  \\
    & \qquad + \sum_{r=0}^{R}\left(1-\frac{\alpha\eta T}{4}\right)^{R-r} \sum_{i=1}^N\sum_{t=1}^T \left(\frac{4\eta^3 T\beta(2\eta T \beta + 1)}{N}\sum_{\tau=1}^{t} S^{t-\tau}\Xi_{r+1,\tau}^{(i)} + \frac{4\eta(\eta T + 1/\alpha)}{\alpha N}\Xi_{r+1,t}^{(i)}\right) \label{eq:temp-dtwj}
\end{aligned}
\end{equation}$$ where $(b)$ is from Lemma [10](#le:bound-grad){reference-type="ref" reference="le:bound-grad"} and $(c)$ is from $H \triangleq 2\eta T\left(1 - 2\eta T\beta \left(44\eta^2T^2\beta^2 + 22\eta T \beta + 1\right)\right)$ as well as the repeated application of $(b)$.

Define $p_r \triangleq \frac{(1 - \alpha \eta T / 4)^{R-r}}{\sum_{r=0}^R \left(1-\alpha\eta T / 4\right)^{R-r}}$. Note that when choose the learning rate $\eta$ that satisfies $\eta \leq \frac{1}{10\beta T}$, we have $H \geq 0.544\,\eta T$. Based on this and $\left\|{\bm{x}}_{R+1} - {\bm{x}}^* \right\|^2 \geq 0$ for [\[eq:temp-dtwj\]](#eq:temp-dtwj){reference-type="eqref" reference="eq:temp-dtwj"}, we further have $$\begin{equation}
\begin{aligned}
    \min_{r \in [R+1)} F({\bm{x}}_r) - F({\bm{x}}^*) &\stackrel{(a)}{\leq} \sum_{r=0}^R p_r \big[F({\bm{x}}_r) - F({\bm{x}}^*)\big] \\
    &\stackrel{(b)}{\leq} \frac{\left(1-\alpha\eta T/4\right)^{R+1}\left\|{\bm{x}}_0 - {\bm{x}}^*\right\|^2}{H \sum_{r=0}^R \left(1-\alpha\eta T / 4\right)^r} \\
    &\qquad + \frac{1}{H}\sum_{r=0}^{R}\sum_{i=1}^N\sum_{t=1}^T p_r\left(\frac{\eta^2}{2N}\sum_{\tau=1}^{t} S^{t-\tau}\Xi_{r+1,\tau}^{(i)} + \frac{4\eta(\eta T + 1/\alpha)}{\alpha N}\Xi_{r+1,t}^{(i)}\right) \\
    &\stackrel{(c)}{\leq} \frac{\alpha \eta T}{H}\exp\left(-\frac{\alpha\eta TR}{4}\right)\left\|{\bm{x}}_0 - {\bm{x}}^*\right\|^2 \\
    &\qquad + \frac{1}{H}\sum_{r=0}^{R}\sum_{i=1}^N\sum_{t=1}^T p_r\left(\frac{\eta^2}{2N}\sum_{\tau=1}^{t} S^{t-\tau}\Xi_{r+1,\tau}^{(i)} + \frac{4\eta(\eta T + 1/\alpha)}{\alpha N}\Xi_{r+1,t}^{(i)}\right) \\
    &\stackrel{(d)}{\leq} 2 \alpha \exp\left(-\frac{\alpha\eta TR}{4}\right)\left\|{\bm{x}}_0 - {\bm{x}}^*\right\|^2 \\
    &\qquad + \sum_{r=0}^{R}\sum_{i=1}^N\sum_{t=1}^T p_r\left(\frac{\eta}{NT}\sum_{\tau=1}^{t} S^{t-\tau}\Xi_{r+1,\tau}^{(i)} + \frac{8(\eta T + 1/\alpha)}{\alpha NT}\Xi_{r+1,t}^{(i)}\right) \label{eq:temp-cwbuw}
\end{aligned}
\end{equation}$$ where $(b)$ is from the rearrangement of [\[eq:temp-dtwj\]](#eq:temp-dtwj){reference-type="eqref" reference="eq:temp-dtwj"} and the fact that $\eta \leq \frac{1}{10\beta T}$. Besides, $(c)$ comes from the inequality $1-x \leq \exp(-x)$ as well as the following results when $R+1 \geq 4\ln(3/4)/(\alpha\eta T)$ $$\begin{equation}
\begin{aligned}
    \sum_{r=0}^R \left(1-\frac{\alpha\eta T}{4}\right)^r &= \frac{1 - \left(1 - \alpha\eta T / 4\right)^{R+1}}{1 - \left(1 - \alpha\eta T / 4\right)} \\
    &\geq \frac{4\left[1 - \exp(-\alpha\eta T(R+1)/4)\right]}{\alpha\eta T} \\
    &\geq \frac{1}{\alpha\eta T} \ . \label{eq:temp-cvjen}
\end{aligned}
\end{equation}$$ Finally, $(d)$ is due to the fact that $H \geq 0.544\,\eta T$.

#### Convex $F$.

When $\alpha=0$, following the derivation in [\[eq:inter-6\]](#eq:inter-6){reference-type="eqref" reference="eq:inter-6"}, we have $$\begin{equation}
\begin{aligned}
    \tikz[baseline=(char.base)]{\node[shape=circle,draw,inner sep=0.2pt] (char) {1};} &\stackrel{(a)}{\leq} \frac{2\eta}{N}\left\|{\bm{x}}^* - {\bm{x}}_r\right\| \sum_{i=1}^{N}\sum_{t=1}^T \sqrt{\Xi_{r+1,t}^{(i)}} + 2\eta T \big[F({\bm{x}}^*) - F({\bm{x}}_r)\big] + 44\eta^3T^3\beta\left\|\nabla F({\bm{x}}_r)\right\|^2 \\
    &\qquad\qquad + \frac{4\eta^3T\beta}{N}\sum_{i=1}^N\sum_{t=1}^T \sum_{\tau=1}^{t} S^{t-\tau}\Xi_{r+1,\tau}^{(i)} \\
    &\stackrel{(b)}{\leq} \frac{2\eta\sqrt{d}}{N}\sum_{i=1}^{N}\sum_{t=1}^T \sqrt{\Xi_{r+1,t}^{(i)}} + 2\eta T \big[F({\bm{x}}^*) - F({\bm{x}}_r)\big] + 44\eta^3T^3\beta\left\|\nabla F({\bm{x}}_r)\right\|^2 \\
    &\qquad\qquad + \frac{4\eta^3T\beta}{N}\sum_{i=1}^N\sum_{t=1}^T \sum_{\tau=1}^{t} S^{t-\tau}\Xi_{r+1,\tau}^{(i)} \\
    &\stackrel{(c)}{=} 2\eta T \big[F({\bm{x}}^*) - F({\bm{x}}_r)\big] + 44\eta^3T^3\beta\left\|\nabla F({\bm{x}}_r)\right\|^2 \\
    &\qquad\qquad + \sum_{i=1}^N\sum_{t=1}^T \left(\frac{4\eta^3T\beta}{N}\sum_{\tau=1}^{t} S^{t-\tau}\Xi_{r+1,\tau}^{(i)} + \frac{2\eta\sqrt{d}}{N}\sqrt{\Xi_{r+1,t}^{(i)}}\right)  \label{eq:inter-7}
\end{aligned}
\end{equation}$$ where the $(b)$ comes from the diameter of ${\mathcal{X}}$, i.e., $\left\|{\bm{x}}-{\bm{x}}'\right\| \leq \sqrt{d}$ for any ${\bm{x}},{\bm{x}}' \in {\mathcal{X}}= [0,1]^d$.

For term $\tikz[baseline=(char.base)]{\node[shape=circle,draw,inner sep=0.2pt] (char) {2};}$ in [\[eq:temp-vgjern\]](#eq:temp-vgjern){reference-type="eqref" reference="eq:temp-vgjern"}, similar to [\[eq:temp-sivbnw\]](#eq:temp-sivbnw){reference-type="eqref" reference="eq:temp-sivbnw"}, we also have $$\begin{equation}
\begin{aligned}
    \tikz[baseline=(char.base)]{\node[shape=circle,draw,inner sep=0.2pt] (char) {2};} \leq  \sum_{i=1}^N\sum_{t=1}^T \left(\frac{8\eta^4 T^2 \beta^2}{N}\sum_{\tau=1}^{t} S^{t-\tau}\Xi_{r+1,\tau}^{(i)} + \frac{4\eta^2 T}{N}\Xi_{r+1,t}^{(i)}\right) + \left(88\eta^4T^4\beta^2 + 2\eta^2 T^2\right) \left\|\nabla F({\bm{x}}_r)\right\|^2  \ . \label{eq:temp-cbvk}
\end{aligned}
\end{equation}$$

By combining [\[eq:inter-7\]](#eq:inter-7){reference-type="eqref" reference="eq:inter-7"} and [\[eq:temp-cbvk\]](#eq:temp-cbvk){reference-type="eqref" reference="eq:temp-cbvk"}, we have $$\begin{equation}
\begin{aligned}
    & \left\|{\bm{x}}_{R+1} - {\bm{x}}^* \right\|^2 \\ 
    \stackrel{(a)}{\leq}& \left\|{\bm{x}}_R - {\bm{x}}^*\right\|^2 + 2\eta T\left(1 - 2\eta T\beta \left(44\eta^2T^2\beta^2 + 22\eta T \beta + 1\right)\right)\big[F({\bm{x}}^*) - F({\bm{x}}_R)\big] \\
    &\qquad\qquad + \sum_{i=1}^N\sum_{t=1}^T \left(\frac{4\eta^3 T\beta(2\eta T \beta + 1)}{N}\sum_{\tau=1}^{t} S^{t-\tau}\Xi_{R+1,\tau}^{(i)} + \frac{4\eta^2 T}{N}\Xi_{R+1,t}^{(i)} + \frac{2\eta\sqrt{d}}{N}\sqrt{\Xi_{R+1,t}^{(i)}} \right) \\
    \stackrel{(b)}{\leq}& \left\|{\bm{x}}_0 - {\bm{x}}^*\right\|^2 + \sum_{r=0}^R H \big[F({\bm{x}}^*) - F({\bm{x}}_r)\big] \\
    &\qquad\qquad + \sum_{i=1}^N\sum_{t=1}^T \left(\frac{4\eta^3 T\beta(2\eta T \beta + 1)}{N}\sum_{\tau=1}^{t} S^{t-\tau}\Xi_{r+1,\tau}^{(i)} + \frac{4\eta^2 T}{N}\Xi_{r+1,t}^{(i)} + \frac{2\eta\sqrt{d}}{N}\sqrt{\Xi_{r+1,t}^{(i)}}\right) \label{eq:temp-qkvn}
\end{aligned}
\end{equation}$$ where $(a)$ is from Lemma [10](#le:bound-grad){reference-type="ref" reference="le:bound-grad"} and $(b)$ is from $H \triangleq 2\eta T\left(1 - 2\eta T\beta \left(44\eta^2T^2\beta^2 + 22\eta T \beta + 1\right)\right)$ as well as the repeated application of $(a)$.

Note that when choose the learning rate $\eta$ that satisfies $\eta \leq \frac{1}{10\beta T}$, we have $H \geq 0.544\,\eta T$. Based on this and $\left\|{\bm{x}}_{R+1} - {\bm{x}}^* \right\|^2 \geq 0$ for [\[eq:temp-qkvn\]](#eq:temp-qkvn){reference-type="eqref" reference="eq:temp-qkvn"}, we further have $$\begin{equation}
\begin{aligned}
    \min_{r \in [R+1)} F({\bm{x}}_r) - F({\bm{x}}^*) &\stackrel{(a)}{\leq} \frac{1}{R} \sum_{r=0}^R \big[F({\bm{x}}_r) - F({\bm{x}}^*)\big] \\
    &\stackrel{(b)}{\leq} \frac{\left\|{\bm{x}}_0 - {\bm{x}}^*\right\|^2}{RH} + \frac{1}{RH}\sum_{r=0}^{R}\sum_{i=1}^N\sum_{t=1}^T \left(\frac{\eta^2}{2N}\sum_{\tau=1}^{t} S^{t-\tau}\Xi_{r+1,\tau}^{(i)}\right. \\
    &\qquad\qquad \left. + \frac{4\eta^2 T}{N}\Xi_{r+1,t}^{(i)} + \frac{2\eta\sqrt{d}}{N}\sqrt{\Xi_{r+1,t}^{(i)}}\right) \\
    &\stackrel{(c)}{\leq} \frac{2\left\|{\bm{x}}_0 - {\bm{x}}^*\right\|^2}{\eta R} + \frac{1}{R}\sum_{r=0}^{R}\sum_{i=1}^N\sum_{t=1}^T \left(\frac{\eta}{NT}\sum_{\tau=1}^{t} S^{t-\tau}\Xi_{r+1,\tau}^{(i)}\right. \\
    &\qquad\qquad \left. + \frac{8\eta}{N}\Xi_{r+1,t}^{(i)} + \frac{4\sqrt{d}}{NT}\sqrt{\Xi_{r+1,t}^{(i)}}\right)
\end{aligned}
\end{equation}$$ where $(c)$ is due to the fact that $H \geq 0.544\,\eta T$.

#### Non-Convex $F$.

When $F$ is only $\beta$-smooth, we have $$\begin{equation}
\begin{aligned}
    &F({\bm{x}}_{r+1}) - F({\bm{x}}_r) \\
    \stackrel{(a)}{\leq}& \nabla F({\bm{x}}_r)^{\top}\left({\bm{x}}_{r+1} - {\bm{x}}_r\right) + \frac{\beta}{2}\left\|{\bm{x}}_{r+1} - {\bm{x}}_r\right\|^2 \\
    \stackrel{(b)}{=}& -\frac{\eta}{N} \nabla F({\bm{x}}_r)^{\top} \sum_{i=1}^N \sum_{t=1}^T \widehat{{\bm{g}}}^{(i)}_{r+1,t-1} + \frac{\beta}{2}\left\|\frac{\eta}{N}\sum_{i=1}^N \sum_{t=1}^T \widehat{{\bm{g}}}^{(i)}_{r+1,t-1}\right\|^2 \\
    \stackrel{(c)}{\leq}& -\frac{\eta}{N} \nabla F({\bm{x}}_r)^{\top} \sum_{i=1}^N \sum_{t=1}^T \left(\widehat{{\bm{g}}}^{(i)}_{r+1,t-1} - \nabla F({\bm{x}}^{(i)}_{r+1,t-1}) + \nabla F({\bm{x}}^{(i)}_{r+1,t-1}) - \nabla F({\bm{x}}_r) + \nabla F({\bm{x}}_r) \right) \\
    &\qquad + \frac{\beta}{2}\left[\sum_{i=1}^N\sum_{t=1}^T \left(\frac{8\eta^4 T^2 \beta^2}{N}\sum_{\tau=1}^{t} S^{t-\tau}\Xi_{r+1,\tau}^{(i)} + \frac{4\eta^2 T}{N}\Xi_{r+1,t}^{(i)}\right) + \left(88\eta^4T^4\beta^2 + 2\eta^2 T^2\right) \left\|\nabla F({\bm{x}}_r)\right\|^2\right] \\
    \stackrel{(d)}{\leq}& \frac{\eta}{N} \sum_{i=1}^N \sum_{t=1}^T \left\|\nabla F({\bm{x}}_r)\right\|\left(\left\|\widehat{{\bm{g}}}^{(i)}_{r+1,t-1} - \nabla F({\bm{x}}^{(i)}_{r+1,t-1})\right\| + \left\|\nabla F({\bm{x}}^{(i)}_{r+1,t-1}) - \nabla F({\bm{x}}_r)\right\|\right)\\
    &\qquad + \sum_{i=1}^N\sum_{t=1}^T \left(\frac{4\eta^4 T^2 \beta^3}{N}\sum_{\tau=1}^{t} S^{t-\tau}\Xi_{r+1,\tau}^{(i)} + \frac{2\eta^2\beta T}{N}\Xi_{r+1,t}^{(i)}\right) + \left(44\eta^4T^4\beta^3 + \eta^2 T^2 \beta - \eta T\right) \left\|\nabla F({\bm{x}}_r)\right\|^2 \\
    \stackrel{(e)}{\leq}&\frac{\eta}{N} \sum_{i=1}^N \sum_{t=1}^T \left(\eta\beta T\left\|\nabla F({\bm{x}}_r)\right\|^2 + \frac{1}{2\eta\beta T}\left\|\widehat{{\bm{g}}}^{(i)}_{r+1,t-1} - \nabla F({\bm{x}}^{(i)}_{r+1,t-1})\right\|^2 + \frac{\beta}{2\eta T}\left\|{\bm{x}}^{(i)}_{r+1,t-1} - {\bm{x}}_r \right\|^2\right) + \\
    &\qquad + \sum_{i=1}^N\sum_{t=1}^T \left(\frac{4\eta^4 T^2 \beta^3}{N}\sum_{\tau=1}^{t} S^{t-\tau}\Xi_{r+1,\tau}^{(i)} + \frac{2\eta^2\beta T}{N}\Xi_{r+1,t}^{(i)}\right) + \left(44\eta^4T^4\beta^3 + \eta^2 T^2 \beta - \eta T\right) \left\|\nabla F({\bm{x}}_r)\right\|^2 \\
    \stackrel{(f)}{\leq}& \left(44\eta^4T^4\beta^3 + 13\eta^2 T^2 \beta - \eta T\right) \left\|\nabla F({\bm{x}}_r)\right\|^2 + \sum_{i=1}^N\sum_{t=1}^T \left(\frac{\left(4\eta^4 T^2 \beta^3 + \eta^2 \beta\right)}{N}\sum_{\tau=1}^{t} S^{t-\tau}\Xi_{r+1,\tau}^{(i)} \right. \\
    &\qquad \left.+ \frac{\left(2\eta^2\beta T + 1/(2\beta T)\right)}{N}\Xi_{r+1,t}^{(i)}\right)
\end{aligned}
\end{equation}$$ where $(a)$ comes from the smoothness of $F$ and $(b)$ is from the one-round update [\[eq:temp-vbbv\]](#eq:temp-vbbv){reference-type="eqref" reference="eq:temp-vbbv"} for input ${\bm{x}}$. In addition, $(c)$ derives from [\[eq:temp-sivbnw\]](#eq:temp-sivbnw){reference-type="eqref" reference="eq:temp-sivbnw"} and $(e)$ results from [\[eq:triangle-1\]](#eq:triangle-1){reference-type="eqref" reference="eq:triangle-1"} in Lemma [5](#le:triangle){reference-type="ref" reference="le:triangle"} by setting $a=\eta\beta T$ in [\[eq:triangle-1\]](#eq:triangle-1){reference-type="eqref" reference="eq:triangle-1"}. Finally, $(f)$ comes from Lemma [11](#le:drift){reference-type="ref" reference="le:drift"}.

Define $H \triangleq \eta T - 44\eta^4T^4\beta^3 - 13\eta^2 T^2 \beta$ and choose $\eta \leq \frac{7}{100\beta T}$, we have that $H > 0.08 \eta T$. Based on this, we further have $$\begin{equation}
\begin{aligned}
    \min_{r \in [R+1)} \left\|\nabla F({\bm{x}}_r)\right\|^2 &\stackrel{(a)}{\leq} \frac{1}{R} \sum_{r=0}^{R} \left\|\nabla F({\bm{x}}_r)\right\|^2 \\
    &\stackrel{(b)}{\leq} \frac{1}{RH} \sum_{r=0}^{R} \big[F({\bm{x}}_r) - F({\bm{x}}_{r+1})\big] + \frac{1}{RH}\sum_{r=0}^R\sum_{i=1}^N\sum_{t=1}^T \left(\frac{\left(2\eta^2\beta T + 1/(2\beta T)\right)}{N}\Xi_{r+1,t}^{(i)} \right. \\
    &\qquad\qquad \left. + \frac{\left(4\eta^4 T^2 \beta^3 + \eta^2 \beta\right)}{N}\sum_{\tau=1}^{t} S^{t-\tau}\Xi_{r+1,\tau}^{(i)} \right) \\
    &\stackrel{(c)}{\leq} \frac{13(F({\bm{x}}_0) - F({\bm{x}}^*))}{\eta RT} + \frac{13}{\eta RT}\sum_{r=0}^R\sum_{i=1}^N\sum_{t=1}^T \left(\frac{\left(0.14 \eta + 1/(2\beta T)\right)}{N}\Xi_{r+1,t}^{(i)} \right. \\
    &\qquad\qquad \left. + \frac{1.02\eta^2 \beta}{N}\sum_{\tau=1}^{t} S^{t-\tau}\Xi_{r+1,\tau}^{(i)} \right)
\end{aligned}
\end{equation}$$ where $(c)$ is due to the fact that $H \geq 0.08\,\eta T$. ◻
:::

::: remark
**Remark 5**. *Of note, Thm. [3](#th:conv-general){reference-type="ref" reference="th:conv-general"} has presented the convergence of the general optimization framework for federated ZOO problems (i.e., Algo. [\[alg:fedzoo\]](#alg:fedzoo){reference-type="ref" reference="alg:fedzoo"}). So, it can be easily adapted to provide the convergence for those algorithms that follow this optimization framework (e.g., our Thm. [2](#th:convergence-fzoos){reference-type="ref" reference="th:convergence-fzoos"} and the results in Appx. [11](#app-sec:existing){reference-type="ref" reference="app-sec:existing"}). This advancement demonstrates superiority over existing federated optimization approaches, such as FedZO, FedProx, and SCAFFOLD, in terms of universality. Notably, these prior works primarily focus on providing convergence guarantees exclusively for their specific algorithmic designs.*
:::

## Proof of Theorem [2](#th:convergence-fzoos){reference-type="ref" reference="th:convergence-fzoos"} {#app-sec:proof:conv-fzoos}

To establish the proof for Thm. [2](#th:convergence-fzoos){reference-type="ref" reference="th:convergence-fzoos"}, we introduce the upper bound of gradient disparity $\frac{1}{N}\sum_{i=1}^N \Xi^{(i)}_{r,t}$ derived from our Thm. [1](#th:grad-error){reference-type="ref" reference="th:grad-error"}, into Thm. [3](#th:conv-general){reference-type="ref" reference="th:conv-general"}. This is in fact facilitated by leveraging the gradient correction length in our Cor. [1](#co:better-gamma){reference-type="ref" reference="co:better-gamma"} to improve the bound in our Thm. [1](#th:grad-error){reference-type="ref" reference="th:grad-error"} (refer to the remark of Appx. [10.2](#app-sec:proof:grad-error){reference-type="ref" reference="app-sec:proof:grad-error"}). To begin with, we first derive a set of inequalities below based on our [\[eq:temp-cbskv\]](#eq:temp-cbskv){reference-type="eqref" reference="eq:temp-cbskv"} since they are frequently required in the results of Thm. [3](#th:conv-general){reference-type="ref" reference="th:conv-general"}. It is important to note that for the sake of simplicity in our proof, we present the validity of these inequalities with a constant probability, without explicitly providing the exact form of this probability. $$\begin{equation}
\begin{aligned}
    &\frac{1}{NR} \sum_{r=0}^{R}\sum_{t=1}^T\sum_{i=1}^N \sum_{\tau=1}^{t} S^{t-\tau}\Xi_{r+1,\tau}^{(i)} \\
    \stackrel{(a)}{=}&\frac{1}{R} \sum_{r=0}^R\sum_{t=1}^T \sum_{\tau=1}^{t} S^{t-\tau}\left(4\omega\kappa \rho^{rT+\tau-1} + 2\sqrt{2\omega\kappa\rho^{rT}G} + 2\sqrt{2NG{\epsilon}}\right) \\
    \stackrel{(b)}{=}& \sum_{t=1}^T \frac{1}{R} \sum_{r=0}^R \left(\frac{4\omega\kappa\rho^{rT}\left(S^{t} - \rho^t\right)}{S - \rho} + \left(2\sqrt{2\omega\kappa\rho^{rT}G} + 2\sqrt{2NG{\epsilon}}\right)\frac{S^t-1}{S-1}\right) \\
    \stackrel{(c)}{=}& \sum_{t=1}^T\left[\frac{4\omega\kappa\left(S^{t} - \rho^t\right)(1 - \rho^{(R+1)T})}{R(S-\rho)(1-\rho^T)} + \left(\frac{2\sqrt{2\omega\kappa G}(1 - \rho^{(R+1)T/2})}{R(1 - \rho^{T/2})(S-1)} + \frac{2\sqrt{2NG{\epsilon}}}{S-1}\right)(S^t-1)\right] \\
    \stackrel{(d)}{=}& \frac{4\omega\kappa(1 - \rho^{(R+1)T})}{R(S-\rho)(1-\rho^T)}\left(\frac{S(S^T-1)}{S-1} - \frac{\rho(1-\rho^T)}{1-\rho}\right) + \left(\frac{2\sqrt{2\omega\kappa G}(1 - \rho^{(R+1)T/2})}{R(1 - \rho^{T/2})(S-1)} \right. \\
    &\qquad\qquad \left. + \frac{2\sqrt{2NG{\epsilon}}}{S-1}\right)\left(\frac{S(S^T-1)}{S-1} - 1\right) \\
    \stackrel{(e)}{=}& {\mathcal{O}}\left(\frac{T^2(\sqrt{G}+1)}{R} + T^2\sqrt{\frac{NG}{M}} \right) \label{eq:temp-qkhv}
\end{aligned}
\end{equation}$$ where $(b),(c),(d)$ are from the summation of geometric series. In addition, $(e)$ comes from the fact that $S \triangleq \frac{(T+1)^2}{T(T-1)}$ (i.e., $S \leq 4.5$), $\frac{S^T-1}{S-1} \leq 11T$ in [\[eq:inter-3\]](#eq:inter-3){reference-type="eqref" reference="eq:inter-3"}, $\frac{S}{S-1}=\frac{(T+1)^2}{3T+1} = {\mathcal{O}}\left(T\right)$ and ${\epsilon}= {\mathcal{O}}\left(\frac{1}{M}\right)$.

$$\begin{equation}
\begin{aligned}
    \frac{1}{NR}\sum_{r=0}^R\sum_{t=1}^T \sum_{i=1}^N \Xi_{r+1,t}^{(i)} &\stackrel{(a)}{=} \frac{1}{R}\sum_{r=0}^R\sum_{t=1}^T \left(4\omega\kappa \rho^{rT+t-1} + 2\sqrt{2\omega\kappa\rho^{rT}G} + 2\sqrt{2NG{\epsilon}}\right) \\
    &\stackrel{(b)}{=} \frac{1}{R}\sum_{r=0}^R \left(\frac{4\omega\kappa\rho^{rT}(1 - \rho^T)}{1 - \rho} + 2T\sqrt{2\omega\kappa\rho^{rT}G} + 2T\sqrt{2NG{\epsilon}}\right) \\
    &\stackrel{(c)}{=} \frac{4\omega\kappa(1 - \rho^{(R+1)T})}{R(1-\rho)} + \frac{2T\sqrt{2\omega\kappa G}(1 - \rho^{(R+1)T/2})}{R(1 - \rho^{T/2})} + 2T\sqrt{2NG{\epsilon}} \\
    % &\leq \gO\left(\frac{1}{R} + \frac{T\sqrt{G}}{R} + T\sqrt{NG\eps}\right) \\
    &\stackrel{(d)}{=} {\mathcal{O}}\left(\frac{T\sqrt{G} + 1}{R} + T\sqrt{NG{\epsilon}}\right) \label{eq:temp-q73b}
\end{aligned}
\end{equation}$$ where $(c),(d)$ are from the summation of geometric series.

$$\begin{equation}
\begin{aligned}
    \frac{1}{NR} \sum_{r=0}^R \sum_{t=1}^T \sum_{i=1}^N \sqrt{\Xi_{r+1,t}^{(i)}} 
    &\stackrel{(a)}{\leq} \frac{1}{R}\sum_{r=0}^R\sum_{t=1}^T \sqrt{\frac{1}{N} \sum_{i=1}^N \Xi_{r+1,t}^{(i)}} \\
    % &= \sum_{t=1}^T \sqrt{4\omega\kappa \rho^{(r-1)T+t-1} + 2\sqrt{2\omega\kappa\rho^{(r-1)T}G} + 2\sqrt{2NG\eps}} \\
    &\stackrel{(b)}{\leq} \frac{1}{R}\sum_{r=1}^R\sum_{t=1}^T \left(\sqrt{4\omega\kappa \rho^{rT+t-1}} + \sqrt{2\sqrt{2\omega\kappa\rho^{rT}G}} + \sqrt{2\sqrt{2NG{\epsilon}}}\right) \\
    &\stackrel{(c)}{=} \frac{1}{R}\sum_{r=0}^R \left(\frac{\sqrt{4\omega\kappa \rho^{rT}}(1 - \rho^{T/2})}{1 - \rho^{1/2}} + T\sqrt{2\sqrt{2\omega\kappa\rho^{rT}G}} + T\sqrt{2\sqrt{2NG{\epsilon}}}\right) \\
    &\stackrel{(d)}{=} \frac{\sqrt{4\omega\kappa}(1 - \rho^{T/2})(1 - \rho^{(R+1)T/2})}{R(1 - \rho^{1/2})(1-\rho^{T/2})} + \frac{T\sqrt[4]{8\omega\kappa G}(1 - \rho^{(R+1)T/4})}{R(1-\rho^{T/4})} + T\sqrt[4]{8NG{\epsilon}} \\
    &\stackrel{(e)}{=} {\mathcal{O}}\left(\frac{T\sqrt[4]{G}+1}{R} + T\sqrt[4]{\frac{NG}{M}}\right) \label{eq:temp-vviw3}
\end{aligned}
\end{equation}$$ where $(a)$ is from Cauchy--Schwarz inequality and $(b)$ is from the inequality of $\sum_j c_j \leq \left(\sum_{j} \sqrt{c_j}\right)^2$ for any $c_j>0$. Besides, $(c),(d)$ are from the summation of geometric series.

Subsequently, we proceed to establish the proof for the results in Thm. [2](#th:convergence-fzoos){reference-type="ref" reference="th:convergence-fzoos"} that are conditioned on different assumptions of $F$ by systematically demonstrating each case individually as follows.

#### Strongly Convex $F$.

Define $c \triangleq 1 - \alpha\eta T / 4$. [^5] When $R+1 \geq 4\ln(3/4)/(\alpha \eta T)$, we then have that $p_r \leq \alpha \eta T c^{R-r}$ according to [\[eq:temp-cvjen\]](#eq:temp-cvjen){reference-type="eqref" reference="eq:temp-cvjen"}, which finally yields the following result $$\begin{equation}
\begin{aligned}
    &\frac{1}{N} \sum_{r=1}^R p_r\sum_{t=1}^T\sum_{i=1}^N \sum_{\tau=1}^{t} S^{t-\tau}\Xi_{r,\tau}^{(i)}\\
    \stackrel{(a)}{=}& \sum_{r=1}^R \frac{4p_r\omega\kappa\rho^{rT}}{S-\rho}\left(\frac{S(S^T-1)}{S-1} - \frac{\rho(1-\rho^T)}{1-\rho}\right) + \sum_{r=1}^R\frac{2p_r\sqrt{2\omega\kappa G}\rho^{rT/2}}{S-1}\left(\frac{S(S^T-1)}{S-1} - 1\right) \\
    &\qquad\qquad + \frac{2\sqrt{2NG{\epsilon}}}{S-1}\left(\frac{S(S^T-1)}{S-1} - 1\right) \\
    \stackrel{(b)}{\leq}& \frac{4\alpha\eta T\omega\kappa (c^{R+1} - \rho^{(R+1)T})}{(S-\rho)(c - \rho^T)}\left(\frac{S(S^T-1)}{S-1} - \frac{\rho(1-\rho^T)}{1-\rho}\right) \\
    &\qquad\qquad + \frac{2\alpha\eta T\sqrt{2\omega\kappa G}(c^{R+1} - \rho^{(R+1)T/2})}{(S-1)(c - \rho^{T/2})}\left(\frac{S(S^T-1)}{S-1} - 1\right) + \frac{2\sqrt{2NG{\epsilon}}}{S-1}\left(\frac{S(S^T-1)}{S-1} - 1\right) \\
    \stackrel{(c)}{\leq}&{\mathcal{O}}\left(\alpha\eta T^3 c^{R}(\sqrt{G}+1) + T^2\sqrt{\frac{NG}{M}}\right) \\
    \stackrel{(d)}{=}&{\mathcal{O}}\left(\frac{\alpha T^2 c^{R}}{\beta}(\sqrt{G}+1) + T^2\sqrt{\frac{NG}{M}}\right) \label{eq:temp-cuqwuy}
\end{aligned}
\end{equation}$$ where $(a)$ follows from the derivation in [\[eq:temp-qkhv\]](#eq:temp-qkhv){reference-type="eqref" reference="eq:temp-qkhv"} and $(b)$ is due to the fact that $p_r \leq \alpha \eta T c^{R-r}$ as well as the summation of geometric series. Besides, $(c)$ comes from $c^{R+1} > \rho^{(R+1)T/2} > \rho^{(R+1)T}$ and $c > \rho^{T/2} > \rho^{T}$ when we choose $c$ properly in the proof of [\[eq:temp-cwbuw\]](#eq:temp-cwbuw){reference-type="eqref" reference="eq:temp-cwbuw"} as well as ${\epsilon}= {\mathcal{O}}\left(\frac{1}{M}\right)$. Finally, $(d)$ results from the fact that $\eta \leq \frac{1}{10\beta T}$ and $\alpha < \beta$.

Following from the derivation above, we also have $$\begin{equation}
\begin{aligned}
    &\frac{1}{N}\sum_{r=0}^R p_r\sum_{t=1}^T \sum_{i=1}^N \Xi_{r+1,t}^{(i)} \\
    =& \sum_{r=0}^R p_r \left(\frac{4\omega\kappa\rho^{rT}(1 - \rho^T)}{1 - \rho} + 2T\sqrt{2\omega\kappa\rho^{rT}G} + 2T\sqrt{2NG{\epsilon}}\right) \\
    \leq& \frac{4\alpha\eta T\omega\kappa(1 - \rho^{T})(c^{R+1} - \rho^{(R+1)T})}{(1-\rho)(c - \rho^T)} + \frac{2\alpha\eta T^2\sqrt{2\omega\kappa G}(c^{R+1} - \rho^{(R+1)T/2})}{(c - \rho^{T/2})} + 2T\sqrt{2NG{\epsilon}} \\
    =& {\mathcal{O}}\left(\frac{\alpha c^{R}}{\beta}(T\sqrt{G}+1) + T\sqrt{\frac{NG}{M}}\right) \ . \label{eq:temp-bvkw}
\end{aligned}
\end{equation}$$

Finally, by introducing [\[eq:temp-cuqwuy\]](#eq:temp-cuqwuy){reference-type="eqref" reference="eq:temp-cuqwuy"} and [\[eq:temp-bvkw\]](#eq:temp-bvkw){reference-type="eqref" reference="eq:temp-bvkw"} into Thm. [3](#th:conv-general){reference-type="ref" reference="th:conv-general"}, we have $$\begin{equation}
\begin{aligned}
    &\min_{r \in [R+1)} F({\bm{x}}_r) - F({\bm{x}}^*) \\
    \stackrel{(a)}{\leq}& 2 \alpha \exp\left(-\frac{\alpha\eta TR}{4}\right)\left\|{\bm{x}}_0 - {\bm{x}}^*\right\|^2  + \sum_{r=0}^{R}\sum_{i=1}^N\sum_{t=1}^T p_r\left(\frac{\eta}{NT}\sum_{\tau=1}^{t} S^{t-\tau}\Xi_{r+1,\tau}^{(i)} + \frac{8(\eta T + 1/\alpha)}{\alpha NT}\Xi_{r+1,t}^{(i)}\right) \\
    \stackrel{(b)}{\leq}& {\mathcal{O}}\left(\alpha \exp\left(-\frac{\alpha \eta T R}{4}\right)D_0 + \frac{1}{\beta T^2}\left(\frac{\alpha c^{R} T^2}{\beta}(\sqrt{G}+1) + T^2\sqrt{\frac{NG}{M}}\right) \right. \\
    &\qquad\qquad \left. + \frac{1/\beta + 1/\alpha}{\alpha T}\left(\frac{\alpha c^{R}}{\beta}(T\sqrt{G}+1) + T\sqrt{\frac{NG}{M}}\right) \right) \\
    \stackrel{(c)}{=}& {\mathcal{O}}\left(\exp(-\eta RT) D_0 + c^{R} \sqrt{G} + \sqrt{\frac{NG}{M}}\right)
\end{aligned}
\end{equation}$$ where $(b)$ is due to the fact that $\eta \leq \frac{1}{10\beta T}$. Let each item above achieve an ${\epsilon}/4$ error, we then realize the result in our Thm. [2](#th:convergence-fzoos){reference-type="ref" reference="th:convergence-fzoos"} when $F$ is $\alpha$-strongly convex and $\beta$-smooth.

#### Convex $F$.

By introducing [\[eq:temp-qkhv\]](#eq:temp-qkhv){reference-type="eqref" reference="eq:temp-qkhv"}, [\[eq:temp-q73b\]](#eq:temp-q73b){reference-type="eqref" reference="eq:temp-q73b"} and [\[eq:temp-vviw3\]](#eq:temp-vviw3){reference-type="eqref" reference="eq:temp-vviw3"} into Thm. [3](#th:conv-general){reference-type="ref" reference="th:conv-general"}, we have

$$\begin{equation}
\begin{aligned}
    &\min_{r \in [R+1)} F({\bm{x}}_r) - F({\bm{x}}^*) \\
    \stackrel{(a)}{\leq}& \frac{2\left\|{\bm{x}}_0 - {\bm{x}}^*\right\|^2}{\eta RT} + \frac{1}{R}\sum_{r=0}^{R}\sum_{i=1}^N\sum_{t=1}^T \left(\frac{\eta}{NT}\sum_{\tau=1}^{t} S^{t-\tau}\Xi_{r+1,\tau}^{(i)} + \frac{8\eta}{N}\Xi_{r+1,t}^{(i)} + \frac{4\sqrt{d}}{NT}\sqrt{\Xi_{r+1,t}^{(i)}}\right)\\
    \stackrel{(b)}{\leq}& {\mathcal{O}}\left(\frac{D_0}{\eta RT} + \frac{1}{\beta T^2}\left(\frac{T^2(\sqrt{G}+1)}{R} + T^2 \sqrt{\frac{NG}{M}}\right) + \frac{1}{\beta T}\left(\frac{T\sqrt{G}+1}{R} + T \sqrt{\frac{NG}{M}}\right) \right. \\
    &\qquad\qquad \left. + \frac{\sqrt{d}}{T} \left(\frac{T\sqrt[4]{G}+1}{R} + T\sqrt[4]{\frac{NG}{M}}\right)\right) \\
    \stackrel{(c)}{=}& {\mathcal{O}}\left(\frac{D_0}{\eta RT} + \frac{\sqrt{G} + \sqrt[4]{d^2 G}}{R} + \sqrt{\frac{NG}{M}} + \sqrt[4]{\frac{NG}{M}}\right)
\end{aligned}
\end{equation}$$ where $(b)$ is due to the fact that $\eta \leq \frac{1}{10\beta T}$. Let each item above achieve an ${\epsilon}/4$ error, we then realize the result in our Thm. [2](#th:convergence-fzoos){reference-type="ref" reference="th:convergence-fzoos"} when $F$ is convex and $\beta$-smooth.

#### Non-Convex $F$.

By introducing [\[eq:temp-qkhv\]](#eq:temp-qkhv){reference-type="eqref" reference="eq:temp-qkhv"} and [\[eq:temp-q73b\]](#eq:temp-q73b){reference-type="eqref" reference="eq:temp-q73b"} into Thm. [3](#th:conv-general){reference-type="ref" reference="th:conv-general"}, we have $$\begin{equation}
\begin{aligned}
    &\min_{r \in [R+1)} \left\|\nabla F({\bm{x}}_r)\right\|^2 \\
    \stackrel{(a)}{\leq}& \frac{13(F({\bm{x}}_0) - F({\bm{x}}^*))}{\eta RT} + \frac{13}{\eta RT}\sum_{r=0}^R\sum_{i=1}^N\sum_{t=1}^T \left(\frac{\left(0.14 \eta + 1/(2\beta T)\right)}{N}\Xi_{r+1,t}^{(i)} \right. \\
    &\qquad\qquad \left. + \frac{1.02\eta^2 \beta}{N}\sum_{\tau=1}^{t} S^{t-\tau}\Xi_{r+1,\tau}^{(i)} \right) \\
    \stackrel{(b)}{\leq}& {\mathcal{O}}\left(\frac{D_1}{\eta RT} + \frac{1}{T}\left(\frac{T\sqrt{G}+1}{R} + T \sqrt{\frac{NG}{M}}\right) + \frac{1}{\beta T^2}\left(\frac{T^2(\sqrt{G}+1)}{R} + T^2 \sqrt{\frac{NG}{M}}\right)\right) \\
    \stackrel{(c)}{=}& {\mathcal{O}}\left(\frac{D_1}{\eta RT} + \frac{\sqrt{G}}{R} + \sqrt{\frac{NG}{M}}\right)
\end{aligned}
\end{equation}$$ where $(b)$ is due to the fact that $\eta \leq \frac{7}{100\beta T}$. Let each item above achieve an ${\epsilon}/3$ error, we then realize the result in our Thm. [2](#th:convergence-fzoos){reference-type="ref" reference="th:convergence-fzoos"} when $F$ is non-convex and $\beta$-smooth. This hence finally concludes our proof of Thm. [2](#th:convergence-fzoos){reference-type="ref" reference="th:convergence-fzoos"}.

# Theoretical Results for Existing Federated ZOO Algorithms {#app-sec:existing}

## Gradient Estimation in Existing Federated ZOO Algorithms {#app-sec:existing-disparity}

We first introduce the following lemma from the Thm. 2.6 in [@approx-error] to bound the gradient estimation error of the standard FD method, which usually serves as the foundation of existing federated ZOO baselines, e.g., [@fedzo].

::: {#le:fd-grad-error .lemma}
**Lemma 12**. *Let $\delta \in (0,1)$. Assume that function $f$ is $\beta$-smooth in its domain and ${\bm{u}}_q \sim {\mathcal{N}}({\bm{0}}, {\mathbf{I}})$ in [\[eq:grad-est-fd\]](#eq:grad-est-fd){reference-type="eqref" reference="eq:grad-est-fd"}, then the following holds with a probability of at least $1-\delta$, $$\begin{equation*}
    \left\|{\bm{\Delta}}({\bm{x}}) - \nabla f({\bm{x}})\right\| \leq \beta\lambda\sqrt{d} + \frac{{\epsilon}\sqrt{d}}{\lambda} + \sqrt{\frac{3n}{\delta Q}\left(3 \left\|\nabla f({\bm{x}})\right\|^2 + \frac{\beta^2\lambda^2}{4}(d+2)(d+4)+\frac{4{\epsilon}^2}{\lambda^2}\right)}
\end{equation*}$$ where $\sup_{{\bm{x}}\in {\mathcal{X}}} \left|y({\bm{x}}) - f({\bm{x}})\right| \leq {\epsilon}$.*
:::

::: remark
**Remark 6**. *In our setting (see Sec. [2](#sec:setting){reference-type="ref" reference="sec:setting"}), we in fact have the following result with a probability of at least $1-\delta$ by applying the Chernoff bound on the Gaussian observation noise $\zeta$: $$\begin{equation}
    {\epsilon}= \sqrt{2\ln(2/\delta)} \sigma \ ,
\end{equation}$$ which is regarded as a constant in our following proofs. By additionally assuming that the gradient of $f$ be bounded (i.e., $\left\|\nabla f({\bm{x}})\right\| \leq c$ for any ${\bm{x}}$ in the domain of $f$ and some $c>0$), we have $$\begin{equation}
    \left\|{\bm{\Delta}}({\bm{x}}) - \nabla f({\bm{x}})\right\| \leq \Uplambda + {\mathcal{O}}\left(\frac{1}{\sqrt{Q}}\right) \label{eq:temp-b83bc}
\end{equation}$$ where the constant $\Uplambda$ is defined as $\Uplambda \triangleq \beta\lambda\sqrt{d} + \frac{{\epsilon}\sqrt{d}}{\lambda}$. Note that this additional constant term in [\[eq:temp-b83bc\]](#eq:temp-b83bc){reference-type="eqref" reference="eq:temp-b83bc"} can not be avoided, which thus is another pitfall of the FD method in addition to its query inefficiency as discussed in our Sec. [3.2](#sec:challenges){reference-type="ref" reference="sec:challenges"}.*
:::

Based on the results above, we can get the following upper bounds for the gradient estimation methods in the existing federated ZOO algorithms. Note that, we usually keep the constant before ${\mathcal{O}}\left(\frac{1}{Q}\right)$ to deliver a more detailed comparison among different federated ZOO algorithms throughout this section.

#### FedZO Algorithm.

For FedZO [@fedzo], it applies the following gradient estimation for every local update in Algo. [\[alg:fedzoo\]](#alg:fedzoo){reference-type="ref" reference="alg:fedzoo"}: $$\begin{equation}
\begin{aligned}
    \widehat{{\bm{g}}}_{r,t-1}^{(i)} = {\bm{\Delta}}^{(i)}({\bm{x}}_{r,t-1}^{(i)}) \ . \label{eq:fedzo-grad-est}
\end{aligned}
\end{equation}$$ That is, $\gamma_{r,t-1}^{(i)}=0$ and ${\bm{g}}_{r,t-1}^{(i)} = {\bm{\Delta}}^{(i)}({\bm{x}}_{r,t-1}^{(i)})$ in [\[eq:general-grad-est\]](#eq:general-grad-est){reference-type="eqref" reference="eq:general-grad-est"}. We provide the following gradient disparity bound for such a gradient estimation method when it is applied in Algo. [\[alg:fedzoo\]](#alg:fedzoo){reference-type="ref" reference="alg:fedzoo"}.

::: {#prop:fedzo .proposition}
**Proposition 3**. *Assume that $\frac{1}{N}\sum_{i=1}^N \left\|\nabla f_i({\bm{x}}) - \nabla F({\bm{x}})\right\|^2 \leq G$ for any ${\bm{x}}\in {\mathcal{X}}$ and $f_i$ is $\beta$-smooth with bounded gradient for any $i \in [N]$. When applying [\[eq:fedzo-grad-est\]](#eq:fedzo-grad-est){reference-type="eqref" reference="eq:fedzo-grad-est"} in Algo. [\[alg:fedzoo\]](#alg:fedzoo){reference-type="ref" reference="alg:fedzoo"}, the following then holds with a constant probability for some $\Uplambda > 0$, $$\begin{equation*}
    \frac{1}{N} \sum_{i=1}^N \Xi_{r,t}^{(i)} \leq 4\Uplambda^2 + 2G + 4{\mathcal{O}}\left(\frac{1}{Q}\right) \ .
\end{equation*}$$*
:::

::: proof
*Proof.* $$\begin{equation}
\begin{aligned}
    \frac{1}{N} \sum_{i=1}^N \Xi_{r,t}^{(i)} &\stackrel{(a)}{=} \frac{1}{N} \sum_{i=1}^N \left\|{\bm{\Delta}}^{(i)}({\bm{x}}_{r,t-1}^{(i)})  - \nabla F({\bm{x}}_{r,t-1}^{(i)})\right\|^2 \\
     &\stackrel{(b)}{=} \frac{1}{N} \sum_{i=1}^N \left\|{\bm{\Delta}}^{(i)}({\bm{x}}_{r,t-1}^{(i)})  - \nabla f_i({\bm{x}}_{r,t-1}^{(i)}) + \nabla f_i({\bm{x}}_{r,t-1}^{(i)}) - \nabla F({\bm{x}}_{r,t-1}^{(i)})\right\|^2 \\
     &\stackrel{(c)}{\leq} \frac{1}{N} \sum_{i=1}^N 2\left(\left\|{\bm{\Delta}}^{(i)}({\bm{x}}_{r,t-1}^{(i)})  - \nabla f_i({\bm{x}}_{r,t-1}^{(i)})\right\|^2 + \left\|\nabla f_i({\bm{x}}_{r,t-1}^{(i)}) - \nabla F({\bm{x}}_{r,t-1}^{(i)})\right\|^2\right) \\
     &\stackrel{(d)}{\leq} 4\Uplambda^2 + 2G + 4{\mathcal{O}}\left(\frac{1}{Q}\right)
\end{aligned}
\end{equation}$$ where $(c)$ comes from Lemma [5](#le:triangle){reference-type="ref" reference="le:triangle"} and $(d)$ is based on Lemma [5](#le:triangle){reference-type="ref" reference="le:triangle"} as well as the result in [\[eq:temp-b83bc\]](#eq:temp-b83bc){reference-type="eqref" reference="eq:temp-b83bc"}. ◻
:::

#### FedProx Algorithm.

For FedProx in the federated ZOO setting (i.e., by simply combining FedProx from [@fedprox] with the standard FD method in [\[eq:grad-est-fd\]](#eq:grad-est-fd){reference-type="eqref" reference="eq:grad-est-fd"}), it has the gradient estimation form as follows: $$\begin{equation}
\begin{aligned}
    \widehat{{\bm{g}}}_{r,t-1}^{(i)} = {\bm{\Delta}}^{(i)}({\bm{x}}_{r,t-1}^{(i)}) + \gamma({\bm{x}}_{r,t-1}^{(i)} - {\bm{x}}_{r-1}) \label{eq:fedprox-grad-est}
\end{aligned}
\end{equation}$$ where $\gamma$ is a constant. That is, $\gamma_{r,t-1}^{(i)}=\gamma$, ${\bm{g}}_{r,t-1}^{(i)} = {\bm{\Delta}}^{(i)}({\bm{x}}_{r,t-1}^{(i)})$ and ${\bm{g}}_{r-1}({\bm{x}}') - {\bm{g}}_{r-1}^{(i)}({\bm{x}}'')={\bm{x}}_{r,t-1}^{(i)} - {\bm{x}}_{r-1}$ in [\[eq:general-grad-est\]](#eq:general-grad-est){reference-type="eqref" reference="eq:general-grad-est"}. We provide the following gradient disparity bound for such a gradient estimation method when it is applied in Algo. [\[alg:fedzoo\]](#alg:fedzoo){reference-type="ref" reference="alg:fedzoo"}.

::: {#prop:fedprox .proposition}
**Proposition 4**. *Assume that $\frac{1}{N}\sum_{i=1}^N \left\|\nabla f_i({\bm{x}}) - \nabla F({\bm{x}})\right\|^2 \leq G$ for any ${\bm{x}}\in {\mathcal{X}}$ and $f_i$ is $\beta$-smooth with bounded gradient for any $i \in [N]$. When applying [\[eq:fedprox-grad-est\]](#eq:fedprox-grad-est){reference-type="eqref" reference="eq:fedprox-grad-est"} in Algo. [\[alg:fedzoo\]](#alg:fedzoo){reference-type="ref" reference="alg:fedzoo"}, the following then holds with a constant probability for some $\Uplambda > 0$, $$\begin{equation*}
    \frac{1}{N} \sum_{i=1}^N \Xi_{r,t}^{(i)} \leq 6\Uplambda^2 + 3G + \frac{3\gamma^2}{N}\sum_{i=1}^N \left\|{\bm{x}}_{r,t-1}^{(i)} - {\bm{x}}_{r-1}\right\|^2 + 6{\mathcal{O}}\left(\frac{1}{Q}\right) \ .
\end{equation*}$$*
:::

::: proof
*Proof.* $$\begin{equation}
\begin{aligned}
     \frac{1}{N} \sum_{i=1}^N \Xi_{r,t}^{(i)} &\stackrel{(a)}{=} \frac{1}{N} \sum_{i=1}^N \left\|{\bm{\Delta}}^{(i)}({\bm{x}}_{r,t-1}^{(i)}) + \gamma\left({\bm{x}}_{r,t-1}^{(i)} - {\bm{x}}_{r-1}\right)  - \nabla F({\bm{x}}_{r,t-1}^{(i)})\right\|^2 \\
     &\stackrel{(b)}{=} \frac{1}{N} \sum_{i=1}^N \left\|{\bm{\Delta}}^{(i)}({\bm{x}}_{r,t-1}^{(i)})  - \nabla f_i({\bm{x}}_{r,t-1}^{(i)}) + \nabla f_i({\bm{x}}_{r,t-1}^{(i)}) - \nabla F({\bm{x}}_{r,t-1}^{(i)}) + \gamma\left({\bm{x}}_{r,t-1}^{(i)} - {\bm{x}}_{r-1}\right)\right\|^2 \\
     &\stackrel{(c)}{\leq} \frac{1}{N} \sum_{i=1}^N 3\left(\left\|{\bm{\Delta}}^{(i)}({\bm{x}}_{r,t-1}^{(i)})  - \nabla f_i({\bm{x}}_{r,t-1}^{(i)})\right\|^2 + \left\|\nabla f_i({\bm{x}}_{r,t-1}^{(i)}) - \nabla F({\bm{x}}_{r,t-1}^{(i)})\right\|^2 \right)  \\
     &\qquad\qquad + \frac{3\gamma^2}{N}\sum_{i=1}^N \left\|{\bm{x}}_{r,t-1}^{(i)} - {\bm{x}}_{r-1}\right\|^2 \\
     &\stackrel{(d)}{\leq} 6\Uplambda^2 + 3G + \frac{3\gamma^2}{N}\sum_{i=1}^N \left\|{\bm{x}}_{r,t-1}^{(i)} - {\bm{x}}_{r-1}\right\|^2 + 6{\mathcal{O}}\left(\frac{1}{Q}\right) \ . 
\end{aligned}
\end{equation}$$ Similarly, $(c)$ is from Lemma [5](#le:triangle){reference-type="ref" reference="le:triangle"} and $(d)$ is based on Lemma [5](#le:triangle){reference-type="ref" reference="le:triangle"} as well as the result in [\[eq:temp-b83bc\]](#eq:temp-b83bc){reference-type="eqref" reference="eq:temp-b83bc"}. ◻
:::

#### SCAFFOLD (Type ) Algorithm.

For SCAFFOLD using its Type gradient correction in the federated ZOO setting (i.e., by simply combining SCAFFOLD (Type ) from [@scaffold] with the standard FD method in [\[eq:grad-est-fd\]](#eq:grad-est-fd){reference-type="eqref" reference="eq:grad-est-fd"}), it has the gradient estimation form as follows: $$\begin{equation}
\begin{aligned}
    \widehat{{\bm{g}}}_{r,t-1}^{(i)} = {\bm{\Delta}}^{(i)}({\bm{x}}_{r,t-1}^{(i)}) + \frac{1}{N}\sum_{j=1}^N {\bm{\Delta}}^{(j)}({\bm{x}}_{r-1}) - {\bm{\Delta}}^{(i)}({\bm{x}}_{r-1}) \ . \label{eq:scaff-grad-est-1}
\end{aligned}
\end{equation}$$ That is, $\gamma_{r,t-1}^{(i)}=1$, ${\bm{g}}_{r,t-1}^{(i)} = {\bm{\Delta}}^{(i)}({\bm{x}}_{r,t-1}^{(i)})$ and ${\bm{g}}_{r-1}({\bm{x}}') - {\bm{g}}_{r-1}^{(i)}({\bm{x}}'')=\frac{1}{N}\sum_{j=1}^N {\bm{\Delta}}^{(j)}({\bm{x}}_{r-1}) - {\bm{\Delta}}^{(i)}({\bm{x}}_{r-1})$ in [\[eq:general-grad-est\]](#eq:general-grad-est){reference-type="eqref" reference="eq:general-grad-est"}. Of note, similar to our FZooS where an additional transmission is required when we actively query in the neighborhood of ${\bm{x}}_r$ in line 7 of Algo. [1](#alg:fzoos){reference-type="ref" reference="alg:fzoos"}, SCAFFOLD (Type ) also needs another server-client transmission of $\frac{1}{N}\sum_{j=1}^N {\bm{\Delta}}^{(j)}({\bm{x}}_{r-1})$ for gradient correction. We provide the following gradient disparity bound for such a gradient estimation method when it is applied in Algo. [\[alg:fedzoo\]](#alg:fedzoo){reference-type="ref" reference="alg:fedzoo"}.

::: {#prop:scaffold-1 .proposition}
**Proposition 5**. *Assume that $f_i$ is $\beta$-smooth with bounded gradient for any $i \in [N]$. When applying [\[eq:scaff-grad-est-1\]](#eq:scaff-grad-est-1){reference-type="eqref" reference="eq:scaff-grad-est-1"} in Algo. [\[alg:fedzoo\]](#alg:fedzoo){reference-type="ref" reference="alg:fedzoo"}, the following then holds with a constant probability for some $\Uplambda > 0$, $$\begin{equation*}
    \frac{1}{N} \sum_{i=1}^N \Xi_{r,t}^{(i)} \leq 18\Uplambda^2  + \frac{6\beta^2}{N}\sum_{i=1}^N \left\|{\bm{x}}_{r,t-1}^{(i)} - {\bm{x}}_{r-1}\right\|^2 + 18{\mathcal{O}}\left(\frac{1}{Q}\right) \ .
\end{equation*}$$*
:::

::: proof
*Proof.* $$\begin{equation}
\begin{aligned}
     \frac{1}{N} \sum_{i=1}^N \Xi_{r,t}^{(i)}
     &\stackrel{(a)}{=} \frac{1}{N} \sum_{i=1}^N \left\|{\bm{\Delta}}^{(i)}({\bm{x}}_{r,t-1}^{(i)}) + \left(\frac{1}{N}\sum_{j=1}^N {\bm{\Delta}}^{(j)}({\bm{x}}_{r-1}) - {\bm{\Delta}}^{(i)}({\bm{x}}_{r-1})\right)  - \nabla F({\bm{x}}_{r,t-1}^{(i)})\right\|^2 \\
     &\stackrel{(b)}{=} \frac{1}{N} \sum_{i=1}^N \left\|{\bm{\Delta}}^{(i)}({\bm{x}}_{r,t-1}^{(i)}) - \nabla f_i({\bm{x}}_{r,t-1}^{(i)}) + \frac{1}{N}\sum_{j=1,j \neq i}^N \left({\bm{\Delta}}^{(j)}({\bm{x}}_{r-1}) - \nabla f_j({\bm{x}}_{r,t-1}^{(i)})\right)\right. \\
     &\qquad\qquad + \left. \frac{N-1}{N} \left(\nabla f_i({\bm{x}}_{r,t-1}^{(i)}) - {\bm{\Delta}}^{(i)}({\bm{x}}_{r-1})\right) \right\|^2 \\
     &\stackrel{(c)}{\leq} \frac{3}{N} \sum_{i=1}^N \left\|{\bm{\Delta}}^{(i)}({\bm{x}}_{r,t-1}^{(i)}) - \nabla f_i({\bm{x}}_{r,t-1}^{(i)})\right\|^2 + \frac{3}{N^3} \sum_{i=1}^N \left\|\sum_{j=1,j \neq i}^N \left({\bm{\Delta}}^{(j)}({\bm{x}}_{r-1}) - \nabla f_j({\bm{x}}_{r,t-1}^{(i)})\right)\right\|^2 \\
     &\qquad\qquad + \frac{3(N-1)^2}{N^3} \sum_{i=1}^N \left\|\nabla f_i({\bm{x}}_{r,t-1}^{(i)}) - {\bm{\Delta}}^{(i)}({\bm{x}}_{r-1})\right\|^2 \\
     &\stackrel{(d)}{\leq} \frac{3}{N} \sum_{i=1}^N \left\|{\bm{\Delta}}^{(i)}({\bm{x}}_{r,t-1}^{(i)}) - \nabla f_i({\bm{x}}_{r,t-1}^{(i)})\right\|^2 + \frac{3(N-1)}{N^3}\sum_{i=1}^N\sum_{j=1,j\neq i}^N \left\|{\bm{\Delta}}^{(j)}({\bm{x}}_{r-1}) - \nabla f_j({\bm{x}}_{r,t-1}^{(i)})\right\|^2 \\
     &\qquad\qquad + \frac{3(N-1)^2}{N^3} \sum_{i=1}^N\left\|\nabla f_i({\bm{x}}_{r,t-1}^{(i)}) - {\bm{\Delta}}^{(i)}({\bm{x}}_{r-1})\right\|^2 \\
     &\stackrel{(e)}{\leq} \frac{3}{N} \sum_{i=1}^N \left\|{\bm{\Delta}}^{(i)}({\bm{x}}_{r,t-1}^{(i)}) - \nabla f_i({\bm{x}}_{r,t-1}^{(i)})\right\|^2 + \frac{6(N-1)}{N^2}\sum_{j=1}^N \left\|{\bm{\Delta}}^{(j)}({\bm{x}}_{r,t-1}^{(i)}) - \nabla f_j({\bm{x}}_{r,t-1}^{(i)})\right\|^2 \\
     &\qquad\qquad + \frac{6\beta^2(N-1)^2}{N^2}\sum_{j=1}^N\left\|{\bm{x}}_{r,t-1}^{(i)} - {\bm{x}}_{r-1}\right\|^2\\
     &\stackrel{(f)}{\leq} \frac{9}{N} \sum_{i=1}^N \left\|{\bm{\Delta}}^{(i)}({\bm{x}}_{r,t-1}^{(i)}) - \nabla f_i({\bm{x}}_{r,t-1}^{(i)})\right\|^2 + 6\beta^2\sum_{i=1}^N\left\|{\bm{x}}_{r,t-1}^{(i)} - {\bm{x}}_{r-1}\right\|^2 \\
     &\stackrel{(g)}{\leq} 18\Uplambda^2  +  6\beta^2\sum_{i=1}^N\left\|{\bm{x}}_{r,t-1}^{(i)} - {\bm{x}}_{r-1}\right\|^2 + 18{\mathcal{O}}\left(\frac{1}{Q}\right)
\end{aligned}
\end{equation}$$ Similarly, $(c),(d)$ are from Lemma [5](#le:triangle){reference-type="ref" reference="le:triangle"} and $(e)$ is because of the smoothness of $F$ as well as [\[eq:triangle-2\]](#eq:triangle-2){reference-type="eqref" reference="eq:triangle-2"} with $a=\frac{1}{N-1}$. Finally, $(g)$ follows from the results in [\[eq:temp-b83bc\]](#eq:temp-b83bc){reference-type="eqref" reference="eq:temp-b83bc"} as well as the result in Lemma [5](#le:triangle){reference-type="ref" reference="le:triangle"}. ◻
:::

#### SCAFFOLD (Type ) Algorithm.

For SCAFFOLD using its Type gradient correction in the federated ZOO setting (i.e., by simply combining SCAFFOLD (Type ) from [@scaffold] with the standard FD method in [\[eq:grad-est-fd\]](#eq:grad-est-fd){reference-type="eqref" reference="eq:grad-est-fd"}), it has the gradient estimation form as follows: $$\begin{equation}
\begin{aligned}
    \widehat{{\bm{g}}}_{r,t-1}^{(i)} = {\bm{\Delta}}^{(i)}({\bm{x}}_{r,t-1}^{(i)}) + \frac{1}{NT}\sum_{j=1}^N \sum_{\tau=1}^{T}{\bm{\Delta}}^{(j)}({\bm{x}}_{r-1,\tau-1}^{(j)}) - \frac{1}{T}\sum_{\tau=1}^{T}{\bm{\Delta}}^{(i)}({\bm{x}}_{r-1,\tau-1}^{(i)}) \ . \label{eq:scaff-grad-est-2}
\end{aligned}
\end{equation}$$ That is, ${\bm{g}}_{r-1}({\bm{x}}') - {\bm{g}}_{r-1}^{(i)}({\bm{x}}'')=\frac{1}{NT}\sum_{j=1}^N \sum_{\tau=1}^{T}{\bm{\Delta}}^{(j)}({\bm{x}}_{r-1,\tau-1}^{(j)}) - \frac{1}{T}\sum_{\tau=1}^{T}{\bm{\Delta}}^{(i)}({\bm{x}}_{r-1,\tau-1}^{(i)})$, ${\bm{g}}_{r,t-1}^{(i)} = {\bm{\Delta}}^{(i)}({\bm{x}}_{r,t-1}^{(i)})$ and $\gamma_{r,t-1}^{(i)}=1$ in [\[eq:general-grad-est\]](#eq:general-grad-est){reference-type="eqref" reference="eq:general-grad-est"}. Interestingly, SCAFFOLD (Type ) servers as an approximation of SCAFFOLD (Type ), which in fact does not require another server-client transmission for gradient correction as discussed in [@scaffold]. This is because $\frac{1}{NT}\sum_{j=1}^N \sum_{\tau=1}^{T}{\bm{\Delta}}^{(j)}({\bm{x}}_{r-1,\tau-1}^{(j)})$ can be computed before the aggregation of $\{{\bm{x}}_{r-1,T}^{(i)}\}_{i=1}^N$ on server. We provide the following gradient disparity bound for such a gradient estimation method when it is applied in Algo. [\[alg:fedzoo\]](#alg:fedzoo){reference-type="ref" reference="alg:fedzoo"}.

::: {#prop:scaffold-2 .proposition}
**Proposition 6**. *Assume that $f_i$ is $c$-continuous and $\beta$-smooth for any $i \in [N]$ and the randomly sampled $\{{\bm{u}}_q\}_{q=1}^Q$ in [\[eq:grad-est-fd\]](#eq:grad-est-fd){reference-type="eqref" reference="eq:grad-est-fd"} are shared across all iterations and rounds. When applying [\[eq:scaff-grad-est-2\]](#eq:scaff-grad-est-2){reference-type="eqref" reference="eq:scaff-grad-est-2"} in Algo. [\[alg:fedzoo\]](#alg:fedzoo){reference-type="ref" reference="alg:fedzoo"}, the following then holds with a constant probability for some $\Uplambda, a> 0$, $$\begin{equation*}
\begin{aligned}
    \frac{1}{N} \sum_{i=1}^N \Xi_{r,t}^{(i)} &\leq 18\Uplambda^2 + \frac{24ac^2}{\lambda^2 T}\sum_{i=1}^N\sum_{\tau=1}^T \left\|{\bm{x}}_{r,t-1}^{(i)} - {\bm{x}}_{r-1,\tau-1}^{(i)}\right\|^2 + 6 {\mathcal{O}}\left(\frac{1}{Q}\right) + 12 {\mathcal{O}}\left(\frac{1}{TQ}\right) \ .
\end{aligned}
\end{equation*}$$*
:::

::: proof
*Proof.* We slightly abuse notation and use ${\bm{\Delta}}_T^{(i)}({\bm{x}}_{r,t-1}^{(i)})$ to denote the FD method in [\[eq:grad-est-fd\]](#eq:grad-est-fd){reference-type="eqref" reference="eq:grad-est-fd"} using $TQ$ function queries for the gradient estimation at input ${\bm{x}}_{r,t-1}^{(i)}$ on client $i$. Based on this notation, we then have $$\begin{equation}
\begin{aligned}
     &\frac{1}{N} \sum_{i=1}^N \Xi_{r,t}^{(i)} \\
     % =& \frac{1}{N} \sum_{i=1}^N \left\|\widehat{\vg}^{(i)}_{r,t-1} - \nabla F(\vx_{r,t-1}^{(i)})\right\|^2 \\
     \stackrel{(a)}{=}& \frac{1}{N} \sum_{i=1}^N \left\|{\bm{\Delta}}^{(i)}({\bm{x}}_{r,t-1}^{(i)}) + \left(\frac{1}{NT}\sum_{j=1}^N \sum_{\tau=1}^{T}{\bm{\Delta}}^{(j)}({\bm{x}}_{r-1,\tau-1}^{(j)}) - \frac{1}{T}\sum_{\tau=1}^{T}{\bm{\Delta}}^{(i)}({\bm{x}}_{r-1,\tau-1}^{(i)})\right)  - \nabla F({\bm{x}}_{r,t-1}^{(i)})\right\|^2 \\
     \stackrel{(b)}{=}& \frac{1}{N} \sum_{i=1}^N \left\|{\bm{\Delta}}^{(i)}({\bm{x}}_{r,t-1}^{(i)}) - \nabla f_i({\bm{x}}_{r,t-1}^{(i)}) + \frac{N-1}{N}\left(\nabla f_i({\bm{x}}_{r,t-1}^{(i)}) - \frac{1}{T}\sum_{\tau=1}^{T}{\bm{\Delta}}^{(i)}({\bm{x}}_{r-1,\tau-1}^{(i)})\right)\right. \\
     &\qquad + \left.\frac{1}{NT}\sum_{j=1,j\neq i}^N \sum_{\tau=1}^{T}\left({\bm{\Delta}}^{(j)}({\bm{x}}_{r-1,\tau-1}^{(j)}) - \nabla f_j({\bm{x}}_{r,t-1}^{(j)})\right)\right\|^2 \\
     \stackrel{(c)}{\leq}& \frac{3}{N} \sum_{i=1}^N \left\|{\bm{\Delta}}^{(i)}({\bm{x}}_{r,t-1}^{(i)}) - \nabla f_i({\bm{x}}_{r,t-1}^{(i)})\right\|^2 \\
     &\qquad + \frac{3(N-1)^2}{N^3} \sum_{i=1}^N \left\| \left(\nabla f_i({\bm{x}}_{r,t-1}^{(i)} - {\bm{\Delta}}_T^{(i)}({\bm{x}}_{r,t-1}^{(i)})\right) + \left({\bm{\Delta}}_T^{(i)}({\bm{x}}_{r,t-1}^{(i)}) - \frac{1}{T}\sum_{\tau=1}^T {\bm{\Delta}}^{(i)}({\bm{x}}_{r-1,\tau-1}^{(i)})\right)\right\|^2 \\
     &\qquad + \frac{3}{N^3}\sum_{i=1}^N\left\|\sum_{j=1,j\neq 1}^N \left[\left(\nabla f_j({\bm{x}}_{r,t-1}^{(j)}) - {\bm{\Delta}}_T^{(j)}({\bm{x}}_{r,t-1}^{(j)})\right) + \left({\bm{\Delta}}_T^{(j)}({\bm{x}}_{r,t-1}^{(j)}) - \frac{1}{T}\sum_{\tau=1}^T{\bm{\Delta}}^{(j)}({\bm{x}}_{r-1,\tau-1}^{(j)})\right)\right]\right\|^2 \\
     \stackrel{(d)}{\leq}& \frac{3}{N} \sum_{i=1}^N \left\|{\bm{\Delta}}^{(i)}({\bm{x}}_{r,t-1}^{(i)}) - \nabla f_i({\bm{x}}_{r,t-1}^{(i)})\right\|^2 \\
     &\qquad + \frac{3(N-1)^2}{N^3} \sum_{i=1}^N \Biggr(\left(1 + \frac{1}{N-1}\right)\left\| \nabla f_i({\bm{x}}_{r,t-1}^{(i)} - {\bm{\Delta}}_T^{(i)}({\bm{x}}_{r,t-1}^{(i)})\right\|^2 \Biggr. \\
     &\qquad\qquad\qquad \Biggr.+ N\left\|{\bm{\Delta}}_T^{(i)}({\bm{x}}_{r,t-1}^{(i)}) - \frac{1}{T}\sum_{\tau=1}^T {\bm{\Delta}}^{(i)}({\bm{x}}_{r-1,\tau-1}^{(i)})\right\|^2\Biggr) \\
     &\qquad + \frac{3(N-1)}{N^3}\sum_{i=1}^N\sum_{j=1,j\neq 1}^N\Biggl(\left(1 + \frac{1}{N-1}\right)\left\|\nabla f_j({\bm{x}}_{r,t-1}^{(j)}) - {\bm{\Delta}}_T^{(j)}({\bm{x}}_{r,t-1}^{(j)})\right\|^2 \Biggr. \\
     &\qquad\qquad\qquad + \Biggl. N\left\|{\bm{\Delta}}_T^{(j)}({\bm{x}}_{r,t-1}^{(j)}) - \frac{1}{T}\sum_{\tau=1}^T{\bm{\Delta}}^{(j)}({\bm{x}}_{r-1,\tau-1}^{(j)})\right\|^2 \Biggr) \label{eq:temp-ghkv}
     % + \gO\left(\frac{1}{N}\sum_{i=1}^N\eps^2\right)
\end{aligned}
\end{equation}$$ Similarly, $(c)$ are from [\[eq:triangle-3\]](#eq:triangle-3){reference-type="eqref" reference="eq:triangle-3"} in Lemma [5](#le:triangle){reference-type="ref" reference="le:triangle"} and $(d)$ is because of [\[eq:triangle-2\]](#eq:triangle-2){reference-type="eqref" reference="eq:triangle-2"} in Lemma [5](#le:triangle){reference-type="ref" reference="le:triangle"} with $a=\frac{N}{N-1}$.

We then bound $\left\|{\bm{\Delta}}_T^{(i)}({\bm{x}}_{r,t-1}^{(i)}) - \frac{1}{T}\sum_{\tau=1}^T {\bm{\Delta}}^{(i)}({\bm{x}}_{r-1,\tau-1}^{(i)})\right\|^2$ as below $$\begin{equation}
\begin{aligned}
    &\left\|{\bm{\Delta}}_T^{(i)}({\bm{x}}_{r,t-1}^{(i)}) - \frac{1}{T}\sum_{\tau=1}^T {\bm{\Delta}}^{(i)}({\bm{x}}_{r-1,\tau-1}^{(i)})\right\|^2 \\
    \stackrel{(a)}{\leq}&\frac{1}{T}\sum_{\tau=1}^T\left\|{\bm{\Delta}}^{(i)}({\bm{x}}_{r,t-1}^{(i)}) - {\bm{\Delta}}^{(i)}({\bm{x}}_{r-1,\tau-1}^{(i)})\right\|^2 \\
    \stackrel{(b)}{=}& \frac{1}{T}\sum_{\tau=1}^T\left\|\frac{1}{Q}\sum_{q=1}^Q\left(y_i({\bm{x}}_{r-1,\tau-1}^{(i)}+ \lambda {\bm{u}}_q) - y_i({\bm{x}}_{r,t-1}^{(i)}+ \lambda {\bm{u}}_q) + y_i({\bm{x}}_{r,t-1}^{(i)}) - y_i({\bm{x}}_{r-1,\tau-1}^{(i)})\right)\frac{{\bm{u}}_q}{\lambda}\right\|^2 \\
    \stackrel{(c)}{\leq}&\frac{1}{\lambda^2 TQ}\sum_{\tau=1}^T\sum_{q=1}^Q\left|y_i({\bm{x}}_{r-1,\tau-1}^{(i)}+ \lambda {\bm{u}}_q) - y_i({\bm{x}}_{r,t-1}^{(i)}+ \lambda {\bm{u}}_q) + y_i({\bm{x}}_{r,t-1}^{(i)}) - y_i({\bm{x}}_{r-1,\tau-1}^{(i)})\right\|^2\left\|{\bm{u}}_q\right|^2 \\
    \stackrel{(d)}{=}& \frac{1}{\lambda^2 TQ}\sum_{\tau=1}^T\sum_{q=1}^Q 2\left|f_i({\bm{x}}_{r-1,\tau-1}^{(i)}+ \lambda {\bm{u}}_q) - f_i({\bm{x}}_{r,t-1}^{(i)}+ \lambda {\bm{u}}_q) + f_i({\bm{x}}_{r,t-1}^{(i)}) - f_i({\bm{x}}_{r-1,\tau-1}^{(i)})\right|^2\left\|{\bm{u}}_q\right\|^2 \\
    &\qquad + \frac{1}{\lambda^2 TQ}\sum_{q=1}^Q 2 \left| \zeta^{(i)}_{r-1,\tau-1} - \zeta_{r,t-1}^{(i)} + \zeta^{(i)'}_{r-1,\tau-1} - \zeta_{r,t-1}^{(i)'} \right|^2 \left\|{\bm{u}}_q\right\|^2 \\
    \stackrel{(e)}{\leq}& \frac{1}{\lambda^2 TQ}\sum_{\tau=1}^T\sum_{q=1}^Q 4\left(\left|f_i({\bm{x}}_{r-1,\tau-1}^{(i)}+ \lambda {\bm{u}}_q) - f_i({\bm{x}}_{r,t-1}^{(i)}+ \lambda {\bm{u}}_q)\right|^2 + \left|f_i({\bm{x}}_{r,t-1}^{(i)}) - f_i({\bm{x}}_{r-1,\tau-1}^{(i)})\right|^2\right)\left\|{\bm{u}}_q\right\|^2 \\
    &\qquad + \frac{1}{\lambda^2 TQ}\sum_{q=1}^Q 8{\epsilon}^2\left\|{\bm{u}}_q\right\|^2 \\
    \stackrel{(f)}{\leq}& \frac{8}{\lambda^2 T} \sum_{\tau=1}^T \left(c^2 \left\|{\bm{x}}_{r,t-1}^{(i)} - {\bm{x}}_{r-1,\tau-1}^{(i)}\right\|^2 + {\epsilon}^2 \right) \left(\frac{1}{Q}\sum_{q=1}^Q\left\|{\bm{u}}_q\right\|^2\right) \\
    \stackrel{(g)}{\leq}& \frac{8a}{\lambda^2 T}\sum_{\tau=1}^T\left(c^2 \left\|{\bm{x}}_{r,t-1}^{(i)} - {\bm{x}}_{r-1,\tau-1}^{(i)}\right\|^2 + {\epsilon}^2\right) \label{eq:temp-bvkw8}
\end{aligned}
\end{equation}$$ where $(a),(d),(e)$ are due to [\[eq:triangle-3\]](#eq:triangle-3){reference-type="eqref" reference="eq:triangle-3"} in Lemma [5](#le:triangle){reference-type="ref" reference="le:triangle"}. Note that $(d)$ is valid because $\{{\bm{u}}_q\}_{q=1}^Q$ in [\[eq:grad-est-fd\]](#eq:grad-est-fd){reference-type="eqref" reference="eq:grad-est-fd"} is assumed to be shared across all iterations and rounds. In addition, $(c)$ is from the Cauchy--Schwarz inequality and $(f)$ is based on the continuity of $F$, i.e., $\left\|F({\bm{x}}) - F({\bm{x}}')\right\| \leq c$ for any ${\bm{x}},{\bm{x}}' \in {\mathcal{X}}$. Finally, $(g)$ is from Lemma [2](#le:chi-square){reference-type="ref" reference="le:chi-square"} and $a \triangleq d + 2\sqrt{dQ^{-1}\ln(1/\delta)}+2Q^{-1}\ln(1/\delta)$.

Finally, by introducing [\[eq:temp-bvkw8\]](#eq:temp-bvkw8){reference-type="eqref" reference="eq:temp-bvkw8"} into [\[eq:temp-ghkv\]](#eq:temp-ghkv){reference-type="eqref" reference="eq:temp-ghkv"}, we have $$\begin{equation}
\begin{aligned}
    \frac{1}{N}\sum_{i=1}^N \Xi_{r,t}^{(i)} \stackrel{(a)}{\leq}& \frac{3}{N} \sum_{i=1}^N \left\|{\bm{\Delta}}^{(i)}({\bm{x}}_{r,t-1}^{(i)}) - \nabla f_i({\bm{x}}_{r,t-1}^{(i)})\right\|^2 + \frac{6(N-1)}{N^2} \sum_{i=1}^N \left\|\nabla f_i({\bm{x}}_{r,t-1}^{(i)}) - {\bm{\Delta}}_T^{(i)}({\bm{x}}_{r,\tau-1}^{(i)})\right\|^2\\
    &\qquad + \frac{24a(N-1)^2}{\lambda^2 TN^2}\sum_{i=1}^N \sum_{\tau=1}^T\left(c^2 \left\|{\bm{x}}_{r,t-1}^{(i)} - {\bm{x}}_{r-1,\tau-1}^{(i)}\right\|^2 + {\epsilon}^2\right) \\
    &\qquad + \frac{24a(N-1)}{\lambda^2 TN^2} \sum_{j=1,j\neq 1}^N\sum_{\tau=1}^T\left(c^2 \left\|{\bm{x}}_{r,t-1}^{(j)} - {\bm{x}}_{r-1,\tau-1}^{(j)}\right\|^2 + {\epsilon}^2\right) \\
    \stackrel{(b)}{\leq}& 18\Uplambda^2 + \frac{24ac^2}{\lambda^2 T}\sum_{i=1}^N\sum_{\tau=1}^T \left\|{\bm{x}}_{r,t-1}^{(i)} - {\bm{x}}_{r-1,\tau-1}^{(i)}\right\|^2 + 6 {\mathcal{O}}\left(\frac{1}{Q}\right) + 12 {\mathcal{O}}\left(\frac{1}{TQ}\right)
\end{aligned}
\end{equation}$$ Finally, $(b)$ follows from the results in [\[eq:temp-b83bc\]](#eq:temp-b83bc){reference-type="eqref" reference="eq:temp-b83bc"} as well as the result in Lemma [5](#le:triangle){reference-type="ref" reference="le:triangle"}, which finally concludes our proof. ◻
:::

#### Comparison and Discussion.

By comparing the upper bounds in Prop. [3](#prop:fedzo){reference-type="ref" reference="prop:fedzo"}, [4](#prop:fedprox){reference-type="ref" reference="prop:fedprox"}, [5](#prop:scaffold-1){reference-type="ref" reference="prop:scaffold-1"}, and [6](#prop:scaffold-2){reference-type="ref" reference="prop:scaffold-2"} above with the one in our Thm. [1](#th:grad-error){reference-type="ref" reference="th:grad-error"}, we can summarize certain interesting insights as follows, which, to the best of our knowledge, has never been formally presented in the literature of federated ZOO.

1.  The gradient disparity of existing federated ZOO algorithms consistently has an additional constant error term (i.e., $\Uplambda^2$) that can not be avoided. Remarkably, no additional constant error term occurs in the gradient disparity bound of our [\[eq:fzoos-grad-est\]](#eq:fzoos-grad-est){reference-type="eqref" reference="eq:fzoos-grad-est"}.

2.  The gradient disparity of existing federated ZOO algorithms typically can only be reduced at a polynomial rate of $Q$ whereas our [\[eq:fzoos-grad-est\]](#eq:fzoos-grad-est){reference-type="eqref" reference="eq:fzoos-grad-est"} is able to achieve an exponential rate of reduction for its gradient disparity.

3.  FedProx achieves an even worse gradient disparity when compared with FedZO by introducing an additional error term $\frac{3\gamma^2}{N}\sum_{i=1}^N \left\|{\bm{x}}_{r,t-1}^{(i)} - {\bm{x}}_{r-1}\right\|^2$. This may explain its worst convergence in Sec. [6](#sec:exps){reference-type="ref" reference="sec:exps"}.

4.  SCAFFOLD (Type ) and SCAFFOLD (Type ) are typically able to mitigate the impact of client heterogeneity (i.e., $G$) by enlarging the impact of the gradient estimation error that is resulting from the FD method applied in these two algorithms. This may lead to worse practical performance when the gradient estimation error outweighs the client heterogeneity, as shown in our Sec. [6](#sec:exps){reference-type="ref" reference="sec:exps"}.

5.  Although SCAFFOLD (Type ) is proposed to approximate SCAFFOLD (Type ) in the original paper [@scaffold], SCAFFOLD (Type ) in fact has the advantage of achieving a smaller gradient estimation error for gradient correction by increasing the number of additional function queries (i.e., the term ${\mathcal{O}}\left(\frac{1}{TQ}\right)$ in Prop. [6](#prop:scaffold-2){reference-type="ref" reference="prop:scaffold-2"}), which is however at the cost of a likely increased input disparity (i.e., the term $\frac{24ac^2}{\lambda^2 T}\sum_{i=1}^N\sum_{\tau=1}^T \left\|{\bm{x}}_{r,t-1}^{(i)} - {\bm{x}}_{r-1,\tau-1}^{(i)}\right\|^2$ in Prop. [6](#prop:scaffold-2){reference-type="ref" reference="prop:scaffold-2"}). Interestingly, federated ZOO usually prefers gradient correction of smaller gradient estimation errors, as suggested by the empirical results in our Sec. [6](#sec:exps){reference-type="ref" reference="sec:exps"}. This explains the reason why SCAFFOLD (Type ) usually outperforms SCAFFOLD (Type ) in federated ZOO, which differs from the scenario of federated FOO and therefore highlights the importance of an accurate gradient correction in federated ZOO.

## Convergence of Existing Federated ZOO Algorithms {#app-sec:conv-existing}

To establish the proof for the convergence of existing federated ZOO algorithms, we introduce the upper bound of gradient disparity $\frac{1}{N}\sum_{i=1}^N \Xi^{(i)}_{r,t}$ derived from our Prop. [3](#prop:fedzo){reference-type="ref" reference="prop:fedzo"}, [4](#prop:fedprox){reference-type="ref" reference="prop:fedprox"}, [5](#prop:scaffold-1){reference-type="ref" reference="prop:scaffold-1"}, and [6](#prop:scaffold-2){reference-type="ref" reference="prop:scaffold-2"}, into Thm. [3](#th:conv-general){reference-type="ref" reference="th:conv-general"}. Particularly, to ease our proof, we mainly prove the convergence of existing federated ZOO algorithms when $F$ is non-convex and $\beta$-smooth. Similar to our Thm. [2](#th:convergence-fzoos){reference-type="ref" reference="th:convergence-fzoos"}, we define $D_0 \triangleq \left\|{\bm{x}}_0 - {\bm{x}}^*\right\|^2$ and $D_1 \triangleq F({\bm{x}}_0) - F({\bm{x}}^*)$, and assume that $\frac{1}{N}\sum_{i=1}^N \left\|\nabla f_i({\bm{x}}) - \nabla F({\bm{x}})\right\|^2 \leq G$ for any ${\bm{x}}\in {\mathcal{X}}$.

::: {#th:fedzo .theorem}
**Theorem 4**. *FedZO enjoys the following convergence with a constant probability for some $\Uplambda > 0$ when $\eta \leq \frac{7}{100 \beta T}$, $$\begin{equation*}
    \min_{r \in [R+1)} \left\|\nabla F({\bm{x}}_r)\right\|^2 \leq {\mathcal{O}}\left(\frac{D_1}{\eta RT} + \Uplambda^2 + G + \frac{1}{Q}\right) \ .
\end{equation*}$$*
:::

::: proof
*Proof.* Following the proof in our Appx. [10.5](#app-sec:proof:conv-fzoos){reference-type="ref" reference="app-sec:proof:conv-fzoos"}, we have $$\begin{equation}
\begin{aligned}
    \min_{r \in [R+1)} \left\|\nabla F({\bm{x}}_r)\right\|^2 &\leq \frac{13(F({\bm{x}}_0) - F({\bm{x}}^*))}{\eta RT} + \frac{13}{\eta RT}\sum_{r=0}^R\sum_{i=1}^N\sum_{t=1}^T \left(\frac{\left(0.14 \eta + 1/(2\beta T)\right)}{N}\Xi_{r+1,t}^{(i)} \right. \\
    &\qquad \left. + \frac{1.02\eta^2 \beta}{N}\sum_{\tau=1}^{t} S^{t-\tau}\Xi_{r+1,\tau}^{(i)} \right) \\
    &\leq {\mathcal{O}}\left(\frac{D_1}{\eta RT} + \left(\Uplambda^2 + G + \frac{1}{Q}\right) + \frac{1}{\beta}\left(\Uplambda^2 + G + \frac{1}{Q}\right)\right) \\
    &= {\mathcal{O}}\left(\frac{D_1}{\eta RT} + \Uplambda^2 + G + \frac{1}{Q}\right) \ ,
\end{aligned}
\end{equation}$$ which concludes our proof. ◻
:::

::: remark
**Remark 7**. *Of note, this convergence aligns with one provided in [@fedzo], which hence supports the validity of our Thm. [3](#th:conv-general){reference-type="ref" reference="th:conv-general"} and Prop. [3](#prop:fedzo){reference-type="ref" reference="prop:fedzo"}.*
:::

#### Discussion.

Of note, the key to proving the convergence of other existing federated ZOO algorithms (i.e., FedProx and SCAFFOLD) lies in the bounded client drift (i.e., Lemma [11](#le:drift){reference-type="ref" reference="le:drift"}) when additional input disparity is introduced in these algorithms. This in fact takes up a lot of space as shown in their original paper and is also out of the scope of this paper. As a consequence, we leave out the proof of the convergence of FedProx and SCAFFOLD in federated ZOO. Fortunately, the convergence (i.e., Thm. [3](#th:conv-general){reference-type="ref" reference="th:conv-general"}) for the general optimization framework Algo. [\[alg:fedzoo\]](#alg:fedzoo){reference-type="ref" reference="alg:fedzoo"} implies that the key difference among the convergence of various federated ZOO algorithms in fact lies in their difference of gradient disparity. In light of this, based on our theoretical insights about the gradient disparity in different federated ZOO algorithms (Sec. [11.1](#app-sec:existing-disparity){reference-type="ref" reference="app-sec:existing-disparity"}), we are still able to present the following insights into the advantages of our FZooS intuitively from the perspective of convergence:

1.  In general, the convergence of our FZooS in Appx. [10.5](#app-sec:proof:conv-fzoos){reference-type="ref" reference="app-sec:proof:conv-fzoos"} avoids the constant error term that can not be omitted in existing federated ZOO algorithms. Note that even the error term caused by RFF approximation (see Thm. [2](#th:convergence-fzoos){reference-type="ref" reference="th:convergence-fzoos"}) is in fact able to be mitigated by using a large number $M$ of random features.

2.  Compared with the convergence of FedZO in Thm. [4](#th:fedzo){reference-type="ref" reference="th:fedzo"}, the convergence of FZooS in Appx. [10.5](#app-sec:proof:conv-fzoos){reference-type="ref" reference="app-sec:proof:conv-fzoos"} demonstrates that the client heterogeneity can be effectively mitigated in FZooS and the gradient estimation term enjoys a better reduction rate (i.e., exponential rate vs. polynomial rate).

3.  The bounded client drift in Lemma [11](#le:drift){reference-type="ref" reference="le:drift"} for the framework Algo. [\[alg:fedzoo\]](#alg:fedzoo){reference-type="ref" reference="alg:fedzoo"} implies that the additional input disparity from the FedProx in Prop. [4](#prop:fedprox){reference-type="ref" reference="prop:fedprox"}, the SCAFFOLD (Type ) in Prop. [5](#prop:scaffold-1){reference-type="ref" reference="prop:scaffold-1"} and the SCAFFOLD (Type ) in Prop. [6](#prop:scaffold-2){reference-type="ref" reference="prop:scaffold-2"} likely leads to a larger client drift and consequently results in worse convergence compared with our FZooS, which has been empirically supported by the results in our Sec. [6](#sec:exps){reference-type="ref" reference="sec:exps"} and Appx. [13](#app-sec:more){reference-type="ref" reference="app-sec:more"}.

# Experimental Settings {#app-sec:exp-settings}

#### General Settings.

The gradient correction length is set to be $\gamma_{r,t-1}^{(i)} = 1/t$ such that it decays with the iteration of local updates $t$. We set the learning rate $\eta = 0.01$ and use Adam as the optimizer. As we described in line 7-8 of Algo. [1](#alg:fzoos){reference-type="ref" reference="alg:fzoos"} and in Sec. [4.2.1](#sec:global-surrogates){reference-type="ref" reference="sec:global-surrogates"}, at each local update iteration, we actively query in the neighborhood of the input ${\bm{x}}^{\smash{(i)}}_{r,t}$ on each client. Each time we generate $100$ values of ${\bm{x}}^{\smash{(i)}}_{r,t} + \boldsymbol{\delta}$ where each dimension of $\boldsymbol{\delta}'$ is uniformly sampled from $[-0.01, 0.01]$. We select the top $5$ values with the highest uncertainty $\big\|\partial (\sigma^{\smash{(i)}}_{r,t})^2({\bm{x}}^{\smash{(i)}}_{r,t} + \boldsymbol{\delta})\big\|$. We set the number of random features $M=10000$ for the squared exponential kernel with a length scale of $1$. Each dimension of the function input is normalized to be within $[0,1]$ using the min-max normalization. The number of clients $N$, the number of local updates $T$, and the number of rounds $R$ vary for different experiments.

## Synthetic Experiments {#app-sec:setting-syn}

Let input ${\bm{x}}= [x_j]_{j=1}^d \in [-10,10]^d$, ${\bm{a}}^{(i)} = [a^{(i)}_j]_{j=1}^d$, and ${\bm{b}}^{(i)} = [b^{(i)}_j]_{j=1}^d$, then the quadratic functions on each client $i$ that has been applied in our Sec. [6.1](#sec:syn){reference-type="ref" reference="sec:syn"} is in the form of $$\begin{equation}
\begin{aligned}
    f_i({\bm{x}}) = \frac{1}{10 d} \left(\sum_{j \in [d]} \left[\left(1 + C \left(a^{(i)}_j - \frac{1}{N}\right)\right)x_j^2 +\left(1 + C \left(b^{(i)}_j - \frac{1}{N}\right)\right)x_j\right] + 1\right)
\end{aligned}
\end{equation}$$ where every $[a^{(i)}_j]_{i=1}^N$ and $[b^{(i)}_j]_{i=1}^N$ are independently randomly sampled from the same Dirichlet distribution $\text{Dir}({\bm{\alpha}})$ where ${\bm{\alpha}}= \frac{1}{N} \cdot {\bm{1}}$. So, given any $C>0$, the final objective function remains $$\begin{equation}
    F({\bm{x}}) = \frac{1}{10 d}\left(\sum_{j \in [d]} \left[x_j^2 + x_j\right] + 1 \right) \ .
\end{equation}$$ Of note, $C$ is the constant that controls the client shift in our federated setting. Specifically, a larger $C$ typically leads to larger client shifts whereas a smaller $C$ usually enjoys smaller client shifts. We set the number of clients to be $N=5$. We set $C \in \{0.5, 5, 50\}$ to vary the degree of heterogeneity (i.e., client shifts) among the local functions. The dimension of the function input is set to be $d=300$. We set the number of local updates to be $T=10$ and the number of rounds to be $R=50$.

## Federated Black-Box Adversarial Attack {#app-sec:setting-attack}

We set the number of clients $N=10$ in this experiment. Before we conduct the adversarial attack, we need to train $N=10$ models on different datasets to get the heterogeneous local model functions. To control the degree of heterogeneity among these functions, each time we sample $P \times 10$ classes among the $10$ classes of the dataset (i.e., MNIST or CIFAR-10) and construct a dataset that only contains data points from these $P \times 10$ classes where $P \in [0,1]$. Repeat the above procedures for $10$ times to get $10$ different datasets. Consequently, a higher $P$ means that the degree of heterogeneity among the local model functions is lower. As an example, when $P=1$, all the local models of these clients will be exactly the same since they are all trained on the dataset with all $10$ classes data points. For MNIST, we train a convolutional neural network (CNN) with two convolution layers followed by two fully connected layers on each dataset. For CIFAR-10, we train a ResNet18 on each dataset.

After obtaining these $10$ local model functions for the clients, we proceed to select $15$ data points from the test dataset. Specifically, we choose these data points among the ones that have been correctly classified by all of the $10$ local models. These selected data points will be used as the targets for our attack. The goal is to find a perturbation ${\bm{x}}$, such that the modified image ${\bm{z}}+ {\bm{x}}$ will be classified incorrectly by the model of each client. The local function takes the perturbed image ${\bm{z}}+ {\bm{x}}$ as input and outputs the difference between the logit of the true class and the highest logit among all other classes except the true class. The condition for the attack to be successful is that the averaged output of $N=10$ models misclassify the image ${\bm{z}}+ {\bm{x}}$. The success rate is the portion of images that are successfully attacked among the selected $15$ images. We set the number of local updates $T=10$ and the number of rounds to be $R=100$.

## Federated Non-Differentiable Metric Optimization {#app-sec:setting-metric}

Following the practice in [@zord], we first train a 3-layer MLP model on the training dataset of Covertype [@Dua19] using the Cross-Entropy loss to obtain its fully converged parameters ${\bm{\theta}}^*$. This is to simulate the federated learning (i.e., fine-tuning) of a pre-trained model with other non-differentiable metrics. Similar to the setting in Appx. [12.2](#app-sec:setting-attack){reference-type="ref" reference="app-sec:setting-attack"}, we construct $N=7$ datasets by sampling $P \times 7$ ($P \in [0,1]$) classes from the test dataset each time. Again, the degree of heterogeneity among the local functions of the clients is controlled by $P$. The higher the value of $P$, the more heterogeneous local functions will be. In this experiment, we aim to find a perturbation ${\bm{x}}$ to the model parameters ${\bm{\theta}}^*$, such that ${\bm{\theta}}^* + {\bm{x}}$ will yield better performance for other non-differentiable metrics, e.g., precision and recall, by using the distributed datasets on clients. Specifically, the local function takes the perturbed model parameter as input and outputs the result of a non-differentiable metric (e.g., $1-\text{precision}$) that evaluates the performance of the model on the corresponding constructed dataset. We set $T=10$ and $R=50$. As in [@zord], we conduct experiments on four non-differentiable metrics, namely precision, recall, Jaccard score, and F1 score.

# More Results {#app-sec:more}

## Synthetic Experiments {#app-sec:syn}

In this section, we first compare the gradient disparity of existing federated ZOO algorithms and our FZooS algorithm using the quadratic functions (see Appx. [12.1](#app-sec:setting-syn){reference-type="ref" reference="app-sec:setting-syn"}) with $d=300$, $N=5$, and $C=5$. The results are in Fig. [5](#fig:error){reference-type="ref" reference="fig:error"}, showing that our proposed adaptive gradient estimation is indeed able to realize significantly improved estimation quality than other existing methods while requiring fewer function queries. This consequently verified the theoretical insights of Thm. [1](#th:grad-error){reference-type="ref" reference="th:grad-error"}. Interestingly, we notice that the quality of our [\[eq:fzoos-grad-est\]](#eq:fzoos-grad-est){reference-type="eqref" reference="eq:fzoos-grad-est"} decreases when the number of iterations for local updates is increased, which is likely because the performance of our gradient surrogates suffers when the input ${\bm{x}}$ for gradient estimation is far away from the historical function queries (i.e., few function information at ${\bm{x}}$ can be used for predictions), as theoretically supported in our Appx. [10.3](#app-sec:prac-gamma){reference-type="ref" reference="app-sec:prac-gamma"}. This also indicates the importance of active queries in our FZooS for consistently high-quality [\[eq:fzoos-grad-est\]](#eq:fzoos-grad-est){reference-type="eqref" reference="eq:fzoos-grad-est"} by collecting more function information in the neighborhood of the potential updated inputs within the local updates.

:::: {#fig:error .figure latex-placement="t"}
![](Shu2023Federated_figs/grad-error.png){width="0.95\\columnwidth"}

::: caption
Comparison of the cosine similarity between $\widehat{{\bm{g}}}_{r,t-1}^{(i)}$ and $\nabla F({\bm{x}}_{r,t-1})$ within one round (with local iterations $T=20$) among different federated ZOO algorithms, where the $y$-axis denotes the cumulatively averaged similarity w.r.t. the $x$-axis (i.e., the iterations of local updates). Of note, for every iteration, our [\[eq:fzoos-grad-est\]](#eq:fzoos-grad-est){reference-type="eqref" reference="eq:fzoos-grad-est"} will actively query only 5 additional function values, which is much fewer than the 20 additional queries in other existing algorithms based on FD methods.
:::
::::

:::: {#fig:quadratic-varying-t .figure latex-placement="t"}
  ----------------------------------------------------------------------------------------------------------- -----------------------------------------------------------------------------------------------------------
   ![image](Shu2023Federated_figs/convergence-Quadratic-300,iter,5.0-round.png){width="0.5\\columnwidth"}   ![image](Shu2023Federated_figs/convergence-Quadratic-300,iter,5.0-query.png){width="0.5\\columnwidth"}
  ----------------------------------------------------------------------------------------------------------- -----------------------------------------------------------------------------------------------------------

![](Shu2023Federated_figs/legend.png){width="0.57\\columnwidth"}

::: caption
Comparison of the communication and query efficiency between our FZooS and other existing baselines on the federated synthetic functions with a varying number $T$ of local updates.
:::
::::

In addition to the comparison using a quadratic function that is under varying heterogeneity through different $C$ in our Fig. [2](#fig:quadratic){reference-type="ref" reference="fig:quadratic"}, we present the comparison using a quadratic function that is under a varying number $T$ of local updates in Fig. [6](#fig:quadratic-varying-t){reference-type="ref" reference="fig:quadratic-varying-t"}. Remarkably, our FZooS still considerably outperforms other baselines in terms of both communication efficiency and query efficiency. Interestingly, Fig. [6](#fig:quadratic-varying-t){reference-type="ref" reference="fig:quadratic-varying-t"} shows that a larger $T$ usually improves the communication efficiency of both our FZooS, as theoretically supported in our Thm. [2](#th:convergence-fzoos){reference-type="ref" reference="th:convergence-fzoos"}. However, such an improvement is usually smaller than the increasing scale of $T$. This also aligns with our Thm. [2](#th:convergence-fzoos){reference-type="ref" reference="th:convergence-fzoos"} since our Thm. [2](#th:convergence-fzoos){reference-type="ref" reference="th:convergence-fzoos"} demonstrates that the increasing $T$ fails to mitigate the impact of client heterogeneity. That is, term $G$ in Thm. [2](#th:convergence-fzoos){reference-type="ref" reference="th:convergence-fzoos"} can not be reduced when $T$ is increased.

:::: {#fig:quadratic-ablation .figure latex-placement="t"}
  ------------------------------------------------------------------------------------------------ --------------------------------------------------------------------------------------------------
   ![image](Shu2023Federated_figs/ablation-Levy-round-features.png){width="0.50\\columnwidth"}   ![image](Shu2023Federated_figs/ablation-Levy-round-components.png){width="0.50\\columnwidth"}
                                                (a)                                                                                               (b)
  ------------------------------------------------------------------------------------------------ --------------------------------------------------------------------------------------------------

::: caption
Comparison of the communication efficiency of our FZooS (a) with a varying number $M$ of random features and (b) without adaptive gradient correction. Of note, $\gamma_{r,t-1}=1$ means a fixed gradient correction length and ${\bm{x}}'={\bm{x}}''={\bm{x}}_{r-1}$ stands for a fixed gradient correction vector as in SCAFFOLD.
:::
::::

We finally present the comparison of the communication efficiency of our FZooS (a) with a varying number $M$ of random features and (b) without adaptive gradient correction under varying client heterogeneity in Fig. [7](#fig:quadratic-ablation){reference-type="ref" reference="fig:quadratic-ablation"}. Of note, in Fig. [7](#fig:quadratic-ablation){reference-type="ref" reference="fig:quadratic-ablation"}, we only apply $M=1000$ random features to facilitate a clear and direct comparison. Interestingly, Fig. [7](#fig:quadratic-ablation){reference-type="ref" reference="fig:quadratic-ablation"}(a) demonstrates that our FZooS of a larger number $M$ of random features generally is preferred for an improved communication efficiency when the client heterogeneity (i.e., $C$) is increased, which thus aligns with the theoretical insights from our Thm. [2](#th:convergence-fzoos){reference-type="ref" reference="th:convergence-fzoos"} in Sec. [5.2](#sec:conv-analysis){reference-type="ref" reference="sec:conv-analysis"}. Nevertheless, when client heterogeneity is small (e.g., $C \leq 5.0$), a moderate number of random features can already produce compelling and competitive convergence. Meanwhile, Fig. [7](#fig:quadratic-ablation){reference-type="ref" reference="fig:quadratic-ablation"}(b) illustrates that, in general, both our adaptive gradient correction vector and adaptive gradient correction length are essential for our FZooS to achieve remarkable convergence in practice. Surprisingly, our FZooS with fixed gradient correction outperforms its counterpart with adaptive gradient correction when client heterogeneity is large (i.e., $C=50$). This is likely because a small number of random features (i.e., $M=1000$) are applied when $C=50$, making adaptive gradient correction generally inaccurate for a long horizon of local updates since the quality of our gradient surrogates decays w.r.t. the horizon (i.e., iterations) as shown in Fig. [5](#fig:error){reference-type="ref" reference="fig:error"}. This can also be verified from Fig. [7](#fig:quadratic-ablation){reference-type="ref" reference="fig:quadratic-ablation"}(a). On the contrary, the fixed gradient correction is already of reasonably good quality due to the smoothness of the global function $F$ (i.e., its gradients are continuous), which consequently can provide consistently good gradient correction along a long horizon of local updates when client heterogeneity is large (i.e., $C=50$).

## Federated Black-Box Adversarial Attack {#app-sec:attack}

:::: {#fig:attack-cifar10-varying-t .figure latex-placement="t"}
  ------------------------------------------------------------------------------------------------------- -------------------------------------------------------------------------------------------------------
   ![image](Shu2023Federated_figs/convergence-CIFAR10_Attack-iter-round-0.png){width="0.5\\columnwidth"}   ![image](Shu2023Federated_figs/convergence-CIFAR10_Attack-iter-query-0.png){width="0.5\\columnwidth"}
  ------------------------------------------------------------------------------------------------------- -------------------------------------------------------------------------------------------------------

![](Shu2023Federated_figs/legend.png){width="0.57\\columnwidth"}

::: caption
Comparison of the success rate achieved by FZooS and other existing federated ZOO algorithms on CIFAR-10 under a varying number $T$ of local updates.
:::
::::

:::: {#fig:attack-mnist .figure latex-placement="t"}
  ----------------------------------------------------------------------------------------------------- -----------------------------------------------------------------------------------------------------
   ![image](Shu2023Federated_figs/convergence-MNIST_Attack-div-round-0.png){width="0.5\\columnwidth"}    ![image](Shu2023Federated_figs/convergence-MNIST_Attack-div-query-0.png){width="0.5\\columnwidth"}
   ![image](Shu2023Federated_figs/convergence-MNIST_Attack-iter-round-0.png){width="0.5\\columnwidth"}   ![image](Shu2023Federated_figs/convergence-MNIST_Attack-iter-query-0.png){width="0.5\\columnwidth"}
  ----------------------------------------------------------------------------------------------------- -----------------------------------------------------------------------------------------------------

![](Shu2023Federated_figs/legend.png){width="0.57\\columnwidth"}

::: caption
Comparison of the success rate in federated black-box adversarial attack achieved by FZooS and other existing federated ZOO algorithms on MNIST under varying client heterogeneity (controlled by $P \in [0,1]$, a larger $P$ implies smaller client heterogeneity) and a varying number $T$ of local updates. The $x$ and $y$-axis are the number of rounds/queries and the corresponding success rate (higher is better).
:::
::::

In addition to depicting the success rate of attacks on CIFAR-10 in Fig.[3](#fig:attack){reference-type="ref" reference="fig:attack"}, which accounts for varying client heterogeneity, we also present the success rate of attacks on CIFAR-10 considering a variable number of local updates, as showcased in Fig.[8](#fig:attack-cifar10-varying-t){reference-type="ref" reference="fig:attack-cifar10-varying-t"}. Furthermore, we provide an illustration of the attack success rate on MNIST, considering both varying client heterogeneity and a variable number of local updates, as presented in Fig. [9](#fig:attack-mnist){reference-type="ref" reference="fig:attack-mnist"}. Notably, our proposed algorithm consistently demonstrates enhanced efficiency in terms of communication when compared to other baselines, across different levels of client heterogeneity and varying numbers of local updates.

## Federated Non-Differentiable Metric Optimization {#app-sec:metric}

:::: {#fig:metricopt-vary-t .figure latex-placement="t"}
  -------------------------------------------------------------------------------------------------------------------- --------------------------------------------------------------------------------------------------------------------
   ![image](Shu2023Federated_figs/convergence-MetricOpt-precision_score-iter-round.png){width="0.5\\columnwidth"}   ![image](Shu2023Federated_figs/convergence-MetricOpt-precision_score-iter-query.png){width="0.5\\columnwidth"}
  -------------------------------------------------------------------------------------------------------------------- --------------------------------------------------------------------------------------------------------------------

![](Shu2023Federated_figs/legend.png){width="0.57\\columnwidth"}

::: caption
Comparison of the non-differentiable metric optimization between FZooS and other existing federated ZOO algorithms under a varying number $T$ of local updates. Note that the $y$-axis is $(1-\text{precision})\times 100\%$ and each curve is the mean $\pm$ standard error from five independent runs.
:::
::::

Besides the non-differentiable metric optimization result for the precision score that is under a varying heterogeneity through different $P$ in Fig. [4](#fig:metricopt){reference-type="ref" reference="fig:metricopt"}, we also report the corresponding result under a varying number $T$ of local updates in Fig. [10](#fig:metricopt-vary-t){reference-type="ref" reference="fig:metricopt-vary-t"}. Moreover, we provide results for recall, F1 score, and Jaccard as the non-differentiable metric in Fig. [11](#fig:metricopt-recall){reference-type="ref" reference="fig:metricopt-recall"}, Fig. [12](#fig:metricopt-f1){reference-type="ref" reference="fig:metricopt-f1"}, and Fig. [13](#fig:metricopt-jaccard){reference-type="ref" reference="fig:metricopt-jaccard"} respectively. Notably, our FZooS still consistently outperforms other baselines in terms of both communication efficiency and query efficiency when under the comparison of varying client heterogeneity and a varying number of local updates with different non-differentiable metrics.

:::: {#fig:metricopt-recall .figure latex-placement="ht"}
  ------------------------------------------------------------------------------------------------------------------- -------------------------------------------------------------------------------------------------------------------
    ![image](Shu2023Federated_figs/convergence-MetricOpt-recall_score-div-round.png){width="0.5\\columnwidth"}      ![image](Shu2023Federated_figs/convergence-MetricOpt-recall_score-div-query.png){width="0.5\\columnwidth"}
   ![image](Shu2023Federated_figs/convergence-MetricOpt-recall_score-iter-round.png){width="0.503\\columnwidth"}   ![image](Shu2023Federated_figs/convergence-MetricOpt-recall_score-iter-query.png){width="0.503\\columnwidth"}
  ------------------------------------------------------------------------------------------------------------------- -------------------------------------------------------------------------------------------------------------------

![](Shu2023Federated_figs/legend.png){width="0.57\\columnwidth"}

::: caption
Comparison of the non-differentiable metric optimization between FZooS and other existing federated ZOO algorithms under varying client heterogeneity (controlled by $P \in [0,1]$, a larger $P$ implies smaller client heterogeneity) and a varying number $T$ of local updates. Note that the $y$-axis is $(1-\text{recall})\times 100\%$ and each curve is the mean $\pm$ standard error from five independent runs.
:::
::::

:::: {#fig:metricopt-f1 .figure latex-placement="ht"}
  --------------------------------------------------------------------------------------------------------------- ---------------------------------------------------------------------------------------------------------------
    ![image](Shu2023Federated_figs/convergence-MetricOpt-f1_score-div-round.png){width="0.5\\columnwidth"}      ![image](Shu2023Federated_figs/convergence-MetricOpt-f1_score-div-query.png){width="0.5\\columnwidth"}
   ![image](Shu2023Federated_figs/convergence-MetricOpt-f1_score-iter-round.png){width="0.503\\columnwidth"}   ![image](Shu2023Federated_figs/convergence-MetricOpt-f1_score-iter-query.png){width="0.503\\columnwidth"}
  --------------------------------------------------------------------------------------------------------------- ---------------------------------------------------------------------------------------------------------------

![](Shu2023Federated_figs/legend.png){width="0.57\\columnwidth"}

::: caption
Comparison of the non-differentiable metric optimization between FZooS and other existing federated ZOO algorithms under varying client heterogeneity (controlled by $P \in [0,1]$, a larger $P$ implies smaller client heterogeneity) and a varying number $T$ of local updates. Note that the $y$-axis is $(1-\text{F1 score})\times 100\%$ and each curve is the mean $\pm$ standard error from five independent runs.
:::
::::

:::: {#fig:metricopt-jaccard .figure latex-placement="ht"}
  -------------------------------------------------------------------------------------------------------------------- --------------------------------------------------------------------------------------------------------------------
    ![image](Shu2023Federated_figs/convergence-MetricOpt-jaccard_score-div-query.png){width="0.5\\columnwidth"}      ![image](Shu2023Federated_figs/convergence-MetricOpt-jaccard_score-div-query.png){width="0.5\\columnwidth"}
   ![image](Shu2023Federated_figs/convergence-MetricOpt-jaccard_score-iter-round.png){width="0.503\\columnwidth"}   ![image](Shu2023Federated_figs/convergence-MetricOpt-jaccard_score-iter-query.png){width="0.503\\columnwidth"}
  -------------------------------------------------------------------------------------------------------------------- --------------------------------------------------------------------------------------------------------------------

![](Shu2023Federated_figs/legend.png){width="0.57\\columnwidth"}

::: caption
Comparison of the non-differentiable metric optimization between FZooS and other existing federated ZOO algorithms under varying client heterogeneity (controlled by $P \in [0,1]$, a larger $P$ implies smaller client heterogeneity) and a varying number $T$ of local updates. The $y$-axis is $(1-\text{Jaccard score})\times 100\%$ and each curve is the mean $\pm$ standard error from five independent runs.
:::
::::
::::::::::::::::::::::::::::::::::::::::::::::

[^1]: So, existing federated FOO algorithms (e.g., FedProx [@fedprox], SCAFFOLD [@scaffold] and etc.) can be easily adapted to this framework (refer to Sec. [3](#sec:framework&challenge){reference-type="ref" reference="sec:framework&challenge"}). We refer to this simple integration of FD methods and federated FOO algorithms as the *existing federated ZOO algorithms* throughout this paper.

[^2]: Of note, our proposed algorithm and theoretical analyses can be easily extended to the setting where the global function has the more general form of $F({\bm{x}})=\sum_{i=1}^N w_i f_i({\bm{x}})$ with $\sum_{i=1}^N w_i=1$ and $w_i\geq 0$.

[^3]: We slightly abuse notation and use $({\bm{x}}^{\smash{(i)}}_{\tau}, y^{\smash{(i)}}_{\tau})$ to denote a historical query till iteration $t-1$ of round $r$.

[^4]: The poor convergence of our FZooS under convex $F$ (vs. the one under non-convex $F$) results from the drawback of the commonly applied proof technique for convex $F$ rather than the algorithm itself. This has been widely recognized in the literature of stochastic gradient descent [@harvey2019tight; @liu2023high].

[^5]: Note that according to [\[eq:temp-cjwnc\]](#eq:temp-cjwnc){reference-type="eqref" reference="eq:temp-cjwnc"}, we can always find a $\sqrt{\rho} < c < 1$ such that [\[eq:temp-cwbuw\]](#eq:temp-cwbuw){reference-type="eqref" reference="eq:temp-cwbuw"} still holds with only different constant terms. As a result, $c^{R+1} > \rho^{(R+1)T/2} > \rho^{(R+1)T}$ and $c > \rho^{T/2} > \rho^{T}$.
