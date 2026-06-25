---
citation_key: Cao2013MultiRobot
arxiv_id: 1302.0723
arxiv_url: https://arxiv.org/abs/1302.0723
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-24T17:17:02Z
origin: ai+web
reviewed: false
---

# Introduction {#sect:intro}

Research in environmental sensing and monitoring has recently gained significant attention and practical interest, especially in supporting environmental sustainability efforts worldwide. A key direction of this research aims at sensing, modeling, and predicting the various types of environmental phenomena spatially distributed over our natural and built-up habitats so as to improve our knowledge and understanding of their economic, environmental, and health impacts and implications. This is non-trivial to achieve due to a trade-off between the quantity of sensing resources (e.g., number of deployed sensors, energy consumption, mission time) and the uncertainty in predictive modeling. In the case of deploying a limited number of mobile robotic sensing assets, such a trade-off motivates the need to plan the most informative resource-constrained observation paths to minimize the uncertainty in modeling and predicting a spatially varying environmental phenomenon, which constitutes the active sensing problem to be addressed in this paper.

A wide multitude of natural and urban environmental phenomena is characterized by *spatially correlated* field measurements, which raises the following fundamental issue faced by the active sensing problem:

> How can the spatial correlation structure of an environmental phenomenon be exploited to improve the active sensing performance and computational efficiency of robotic path planning?

The works of [@LowAAMAS12; @LowAAMAS08; @LowICAPS09] have tackled this issue specifically in the context of an environmental hotspot field by studying how its spatial correlation structure affects the performance advantage of adaptivity in path planning: If the field is large with a few small hotspots exhibiting extreme measurements and much higher spatial variability than the rest of the field, then adaptivity can provide better active sensing performance. On the other hand, non-adaptive sampling techniques [@LowUAI12; @Guestrin08; @LowAAMAS11] suffice for smoothly-varying fields.

In this paper, we will investigate the above issue for another important broad class of environmental phenomena called *anisotropic* fields that exhibit a (often much) higher spatial correlation along one direction than along its perpendicular direction. Such fields occur widely in natural and built-up environments and some of them include (a) ocean and freshwater phenomena like plankton density [@Kitsiou01], fish abundance, temperature and salinity [@Sokolov99]; (b) soil and atmospheric phenomena like peat thickness [@Webster01], surface soil moisture, rainfall; (c) mineral deposits like radioactive ore; (d) pollutant and contaminant concentration like air [@Boisvert11], heavy metals; and (e) ecological abundance like vegetation density.

The geostatistics community has examined a related issue of how the spatial correlation structure of an anisotropic field can be exploited to improve the predictive performance of a sampling design for a static sensor network. To resolve this, the following heuristic design [@Webster01] is commonly used for sampling the anisotropic fields described above: Arrange and place the static sensors in a rectangular grid such that one axis of the grid is aligned along the direction of lowest spatial correlation (i.e., highest spatial variability) and the grid spacing along this axis as compared to that along its perpendicular axis is proportional to the ratio of their respective spatial correlations. In the case of path planning for $k$ robots, one may consider the sampling locations of the rectangular grid as cities to be visited in a $k$-traveling salesman problem so as to minimize the total distance traveled or mission time [@LowICRA07]. However, since the resulting observation paths are constrained by the heuristic sampling design, they are suboptimal in solving the active sensing problem (i.e., minimizing the predictive uncertainty). This drawback is exacerbated when the robots are capable of sampling at a higher resolution along their paths (e.g., due to high sensor sampling rate) than that of the grid, hence gathering suboptimal observations while traversing between grid locations.

This paper presents two principled approaches to efficient information-theoretic path planning based on entropy and mutual information (respectively, Sections [3](#se:mepp){reference-type="ref" reference="se:mepp"} and [4](#se:m2ipp){reference-type="ref" reference="se:m2ipp"}) criteria for *in situ* active sensing of environmental phenomena. In contrast to the existing methods described above, our proposed path planning algorithms are novel in addressing a trade-off between active sensing performance and computational efficiency. An important practical consequence is that our algorithms can exploit the spatial correlation structure of anisotropic fields to improve time efficiency while preserving near-optimal active sensing performance. The specific contributions of our work in this paper include:

::: list
$\bullet$

Analyzing the time complexity of our proposed algorithms and proving analytically that they scale better than state-of-the-art information-theoretic path planning algorithms [@Guestrin08; @LowICAPS09] with increasing length of planning horizon (Sections [\[mepp:ta\]](#mepp:ta){reference-type="ref" reference="mepp:ta"} and [\[mipp:ta\]](#mipp:ta){reference-type="ref" reference="mipp:ta"});

Providing theoretical guarantees on the active sensing performance of our proposed algorithms (Sections [\[mepp:pg\]](#mepp:pg){reference-type="ref" reference="mepp:pg"} and [\[mipp:pg\]](#mipp:pg){reference-type="ref" reference="mipp:pg"}) for a class of exploration tasks called the transect sampling task (Section [2.1](#back:tran){reference-type="ref" reference="back:tran"}), which, in particular, can be improved with longer planning time and/or lower spatial correlation along the transect;

Empirically evaluating the time efficiency and active sensing performance of our proposed algorithms on real-world temperature and plankton density field data (Section [5](#se:exp){reference-type="ref" reference="se:exp"}).
:::

# Background

## Transect Sampling Task {#back:tran}

In a transect sampling task [@LowAAMAS11; @Thompson08], a team of $k$ robots is tasked to explore and sample an environmental phenomenon spatially distributed over a transect (Fig. [1](#figtst){reference-type="ref" reference="figtst"}) that is discretized into a $r\times n$ grid of sampling locations where the number $n$ of columns is assumed to be much larger than the number $r$ of sampling locations in each column, $r$ is expected to be small in a transect, and $k\leq r$. The columns are indexed in an increasing order from left to right. The $k$ robots are constrained to simultaneously explore forward one column at a time from the leftmost column '$1$' to the rightmost column '$n$' such that each robot samples one location per column for a total of $n$ locations. Hence, each robot, given its current location, can move to any of the $r$ locations in the adjacent column on its right.

![Transect sampling task with $2$ robots on a temperature field (measured in$\,^{\circ}\mathrm{C}$) spatially distributed over a $25$ m $\times$ $150$ m transect that is discretized into a $5 \times 30$ grid of sampling locations (white dots) (Image courtesy of \[$14$\]).](tempgrid.pdf){#figtst}

In practice, the transect sampling task is especially appropriate for and widely performed by mobile robots with limited maneuverability (e.g., unmanned aerial vehicles, autonomous surface and underwater vehicles (AUVs) [@Davis04]) because it involves less complex path maneuvers that can be achieved more reliably using less sophisticated on-board control algorithms. In terms of practical applicability, transect sampling is a particularly useful exploration task to be performed during the transit from the robot's current location to a distant planned waypoint [@Leonard07; @Thompson08] to collect the most informative observations. For active sensing of ocean and freshwater phenomena, the transect can span a spatial feature of interest such as a harmful algal bloom or pollutant plume to be explored and sampled by a fleet of AUVs being deployed off a ship vessel.

## Gaussian Process-Based Anisotropic Field {#back:gp}

An environmental phenomenon is defined to vary as a realization of a rich class of Bayesian non-parametric models called the *Gaussian process* (GP) [@Rasmussen06] that can formally characterize its spatial correlation structure and be refined with increasing number of observations. More importantly, GP can provide formal measures of predictive uncertainty (e.g., based on an entropy or mutual information criterion) for directing the robots to explore the highly uncertain areas of the phenomenon.

Let ${\mathcal D}$ be a set of sampling locations representing the domain of the environmental phenomenon such that each location $x\in{\mathcal D}$ is associated with a realized (random) measurement $z_x$ ($Z_x$) if $x$ is sampled/observed (unobserved). Let $\{Z_x\}_{x \in {\mathcal D}}$ denote a GP, that is, every finite subset of $\{Z_x\}_{x \in {\mathcal D}}$ has a multivariate Gaussian distribution [@Rasmussen06]. The GP is fully specified by its prior mean $\mu_{x} \triangleq \mathbb{E}[Z_x]$ and covariance $\sigma_{x x'} \triangleq \mbox{cov}[Z_x, Z_{x'}]$ for all $x, x' \in {\mathcal D}$. In the experiments (Section [5](#se:exp){reference-type="ref" reference="se:exp"}), we assume that the GP is second-order stationary, i.e., it has a constant *prior* mean and a stationary *prior* covariance structure (i.e., $\sigma_{x x'}$ is a function of $x -x'$ for all $x,x' \in{\mathcal D}$), both of which are assumed to be known. In particular, its covariance structure is defined by the widely-used squared exponential covariance function $$\begin{equation}
    \label{kf} \sigma_{x x'} \triangleq \sigma^2_s \exp \left\{ -\frac{1}{2}(x-x')^T M^{-2} (x-x') \right\} + \sigma_n^2\delta_{xx'}
\end{equation}$$ where $\sigma^2_s$ and $\sigma_n^2$ are, respectively, the signal and noise variances controlling the intensity and noise of the measurements, $M$ is a diagonal matrix with length-scale components $\ell_1$ and $\ell_2$ controlling the degree of spatial correlation or "similarity" between measurements along (i.e., horizontal direction) and perpendicular to (i.e., vertical direction) the transect, respectively, and $\delta_{xx'}$ is a Kronecker delta of value $1$ if $x=x'$, and $0$ otherwise. For anisotropic fields, $\ell_1 \neq\ell_2$.

An advantage of using GP to model the environmental phenomenon is its probabilistic regression capability: Given a vector $s$ of sampled locations and a column vector $z_s$ of corresponding measurements, the joint distribution of the measurements at any vector $u$ of $\kappa$ unobserved locations remains Gaussian with the following *posterior* mean vector and covariance matrix $$\begin{equation}
    \label{gpmm}  \mu_{u|s}  =   \mu_{u} + \Sigma_{us}\Sigma^{-1}_{ss}(z_s - \mu_s)\vspace{-2.2mm}
\end{equation}$$ $$\begin{equation}
    \label{gpmv}  \Sigma_{uu|s} =  \Sigma_{uu} - \Sigma_{us}\Sigma^{-1}_{ss}\Sigma_{su}\vspace{-1mm}
\end{equation}$$ where ${\mu}_u$ (${\mu}_s$) is a column vector with mean components $\mu_{x}$ for every location $x$ of $u$ ($s$), $\Sigma_{us}$ ($\Sigma_{ss}$) is a covariance matrix with covariance components $\sigma_{x x'}$ for every pair of locations $x$ of $u$ ($s$) and $x'$ of $s$, and $\Sigma_{su}$ is the transpose of $\Sigma_{us}$. The posterior mean vector $\mu_{u|s}$ ([\[gpmm\]](#gpmm){reference-type="ref" reference="gpmm"}) is used to predict the measurements at vector $u$ of $\kappa$ unobserved locations. The uncertainty of these predictions can be quantified using the posterior covariance matrix $\Sigma_{uu|s}$ ([\[gpmv\]](#gpmv){reference-type="ref" reference="gpmv"}), which is independent of the measurements $z_s$, in two ways: (a) the trace of $\Sigma_{uu|s}$ yields the sum of posterior variances $\Sigma_{xx|s}$ over every location $x$ of $u$; (b) the determinant of $\Sigma_{uu|s}$ is used in calculating the Gaussian posterior joint entropy $$\begin{equation}
  H(Z_u|Z_s)\triangleq
  \frac{1}{2}\log\hspace{-0.5mm}\left(2\pi e\right)^{\kappa}\left|\Sigma_{uu|s}\right| \ .
  \label{mepp:pw06}\vspace{-0.5mm}
  %\vspace{-2.5mm}
\end{equation}$$ Unlike the first measure of predictive uncertainty which assumes conditional independence between measurements at vector $u$ of unobserved locations, the entropy-based measure ([\[mepp:pw06\]](#mepp:pw06){reference-type="ref" reference="mepp:pw06"}) accounts for their correlation, thereby not overestimating their uncertainty. Hence, we will focus on using the entropy-based measure of uncertainty in this paper.

# Entropy-Based Path Planning {#se:mepp}

**Notations.** Each planning stage $i$ is associated with column $i$ of the transect for $i=1,\ldots,n$. In each stage $i$, the team of $k$ robots samples from column $i$ a total of $k$ observations (each of which comprises a pair of a location and its measurement) that are denoted by a pair of vectors $x_i$ of $k$ locations and $Z_{x_i}$ of the corresponding random measurements. Let ${\mathcal X}_i$ denote the set of all possible robots' sampling locations $x_i$ in stage $i$. It can be observed that $\chi\triangleq |{\mathcal X}_1| =\ldots =|{\mathcal X}_n|=$ $^r\mathrm{C}_k$. We assume that the robots can deterministically (i.e., no stochasticity in motion) move from their current locations $x_{i-1}$ in column $i-1$ to the next locations $x_i$ in column $i$. Let $x_{i:j}$ and $Z_{x_{i:j}}$ denote vectors concatenating robots' sampling locations $x_i, \ldots, x_j$ and concatenating corresponding random measurements $Z_{x_i}, \ldots, Z_{x_j}$ over stages $i$ to $j$, respectively, and ${\mathcal X}_{i:j}$ denote the set of all possible $x_{i:j}$.

**Maximum Entropy Path Planning (MEPP).** The work of [@LowICAPS09] has proposed planning non-myopic observation paths $x^{\ast}_{1:n}$ with maximum entropy (i.e., highest uncertainty): $$\begin{equation}
    x^{\ast}_{1:n}= \mathop{\arg\max}_{x_{1:n} \in \mathcal{X}_{1:n}} H(Z_{x_{1:n}})
    \label{mepp:pw03} \vspace{-1mm}
\end{equation}$$ that, as proven in an equivalence result, minimize the posterior entropy/uncertainty remaining in the unobserved locations of the transect. Computing the maximum entropy paths $x^{\ast}_{1:n}$ incurs ${\mathcal O}\hspace{-0.7mm}\left(\chi^n(kn)^3\right)$, which is exponential in the length $n$ of planning horizon. To mitigate this computational difficulty, an anytime heuristic search algorithm [@Korf90] is used to compute ([\[mepp:pw03\]](#mepp:pw03){reference-type="ref" reference="mepp:pw03"}) approximately. However, its performance cannot be guaranteed. Furthermore, as reported in [@LowAAMAS11], when $\chi$ or $n$ is large, its computed paths perform poorly even after incurring a huge amount of search time and space.

**Approximate MEPP$(m)$.**[]{#mepp:ta label="mepp:ta"}[]{#mepp:pg label="mepp:pg"} To establish a trade-off between active sensing performance and computational efficiency, the key idea is to exploit a property of the covariance function ([\[kf\]](#kf){reference-type="ref" reference="kf"}) that the spatial correlation of measurements between any two locations decreases exponentially with increasing distance between them. Intuitively, such a property makes the measurements $Z_{x_i}$ to be observed next in column $i$ near-independent of the past distant measurements $Z_{x_{1:i-m-1}}$ observed from columns $1$ to $i-m-1$ (i.e., far from column $i$) for a sufficiently large $m$ by conditioning on the closer measurements $Z_{x_{i-m:i-1}}$ observed in columns $i-m$ to $i-1$ (i.e., closer to column $i$). Consequently, $H(Z_{x_i}| Z_{x_{1:i-1}})$ can still be closely approximated by $H(Z_{x_i}|Z_{x_{i-m:i-1}})$ after assuming a $m$-th order Markov property, thus yielding the following approximation of the joint entropy $H(Z_{x_{1:n}})$ in ([\[mepp:pw03\]](#mepp:pw03){reference-type="ref" reference="mepp:pw03"}): $$\begin{equation}
\hspace{-1.04mm}
\begin{array}{rl}
    H(Z_{x_{1:n}}) =& \hspace{-2mm} H(Z_{x_{1:m}}) +\sum_{i=m+1}^{n} H(Z_{x_{i}} |
    Z_{x_{1:i-1}})\vspace{1mm}\\ 
    \approx & \hspace{-2mm} H(Z_{x_{1:m}}) + \sum_{i=m+1}^{n} H(Z_{x_{i}} |
    Z_{x_{i-m:i-1}}) \ .
\end{array} 
    \label{mef1}
\end{equation}$$ The first equality is due to the chain rule for entropy [@Cover91]. Using ([\[mef1\]](#mef1){reference-type="ref" reference="mef1"}), MEPP ([\[mepp:pw03\]](#mepp:pw03){reference-type="ref" reference="mepp:pw03"}) can be approximated by the following stage-wise dynamic programming equations, which we call MEPP$(m)$: $$\begin{equation}
\hspace{-1.5mm}
    \begin{array}{rl}
        V_{i}(x_{i-m:i-1}) =& \hspace{-2mm}\displaystyle \max_{x_i \in \mathcal{X}_{i}}H(Z_{x_i} |Z_{x_{i-m:i-1}}) + V_{i+1}(x_{i-m+1:i})\\
        V_{n}(x_{n-m:n-1}) =& \hspace{-2mm}\displaystyle \max_{x_n \in \mathcal{X}_{n}} H(Z_{x_n} | Z_{x_{n-m:n-1}})\vspace{-2.5mm} 
     \end{array}
\label{mlme2}
\end{equation}$$ for stage $i = m+1,\ldots,n-1$, each of which induces a corresponding optimal vector $x^{{\mbox{\tiny{$\mathbb{E}$}}}}_{i}$ of $k$ locations given the optimal vector $x^{{\mbox{\tiny{$\mathbb{E}$}}}}_{i-m:i-1}$ obtained from previous stages $i-m$ to $i-1$[^1]. Let the optimal observation paths of MEPP$(m)$ be denoted by $x^{{\mbox{\tiny{$\mathbb{E}$}}}}_{1:n}$ that concatenates $$\begin{equation}
    x^{{\mbox{\tiny{$\mathbb{E}$}}}}_{1:m} = \underset{x_{1:m} \in \mathcal{X}_{1:m}}{\operatorname{\arg\max}} H(Z_{x_{1:m}})+V_{m+1}(x_{1:m}) \label{mlmax}\vspace{-0.5mm}
    %\displaystyle \max_{x_{1:m} \in \mathcal{X}_{1:m}}
\end{equation}$$ for the first $m$ stages and $x^{{\mbox{\tiny{$\mathbb{E}$}}}}_{m+1}, \ldots, x^{{\mbox{\tiny{$\mathbb{E}$}}}}_{n}$ derived using ([\[mlme2\]](#mlme2){reference-type="ref" reference="mlme2"}) for the subsequent stages $m+1$ to $n$. Our proposed MEPP$(m)$ algorithm generalizes that of [@LowAAMAS11] which is essentially MEPP$(1)$.

::: {#timeme .theorem}
**Theorem 1** (Time Complexity). * Deriving  $x^{{\mbox{\tiny{$\mathbb{E}$}}}}_{1:n}$  of\
*MEPP*$(m)$ requires ${\mathcal O}\hspace{-0.7mm}\left(\chi^{m+1}[n+(km)^3]\right)$ time.*
:::

Its proof is given in [@LowArxiv13]. Unlike MEPP which scales exponentially in the planning horizon length $n$, our MEPP$(m)$ algorithm scales linearly in $n$.

Let $\omega_1$ and $\omega_2$ be the horizontal and vertical separation widths between adjacent grid locations, respectively, $\ell^\prime_1 \triangleq \ell_1 / \omega_1$ and $\ell^\prime_2 \triangleq \ell_2 / \omega_2$ denote the normalized horizontal and vertical length-scale components, respectively, and $\eta\triangleq\sigma^2_n / \sigma^2_s$. The following result bounds the loss in active sensing performance of the MEPP$(m)$ algorithm (i.e., ([\[mlme2\]](#mlme2){reference-type="ref" reference="mlme2"}) and ([\[mlmax\]](#mlmax){reference-type="ref" reference="mlmax"})) relative to that of MEPP ([\[mepp:pw03\]](#mepp:pw03){reference-type="ref" reference="mepp:pw03"}):

::: {#theoEd .theorem}
**Theorem 2** (Performance Guarantee). *The paths $x^{{\mbox{\tiny{$\mathbb{E}$}}}}_{1:n}$ are $\epsilon$-optimal in achieving the maximum entropy criterion, i.e., $H(Z_{x^{\ast}_{1:n}}) - H(Z_{x^{{\mbox{\tiny{$\mathbb{E}$}}}}_{1:n}})\leq\epsilon$ where $$\epsilon\triangleq \left[k(n-m)\right]^2\log\hspace{-0.7mm}\left\{1+\frac{\exp\hspace{-0.7mm}\left\{-(m+1)^2/(2\ell'^{2}_1) \right\}^2}{\eta(1+\eta)} \right\}.$$*
:::

Its proof is given in [@LowArxiv13]. Theorem [2](#theoEd){reference-type="ref" reference="theoEd"} reveals that the active sensing performance of MEPP$(m)$ can be improved by decreasing $\epsilon$, which is achieved using higher noise-to-signal ratio $\eta$ (i.e., noisy, less intense fields), smaller number $k$ of robots, shorter planning horizon length $n$, larger $m$, and/or lower spatial correlation $\ell'_1$ along the transect. Two important implications result: (a) Increasing $m$ trades off computational efficiency (Theorem [1](#timeme){reference-type="ref" reference="timeme"}) for better active sensing performance, and (b) if the spatial correlation of the anisotropic field along the transect is sufficiently low to maintain a relatively tight bound $\epsilon$ such that only a small $m$ is needed, then MEPP$(m)$ can exploit this spatial correlation structure to gain time efficiency while preserving near-optimal active sensing performance. In practice, it is often possible to obtain prior knowledge on a direction of low spatial correlation (refer to ocean and freshwater phenomena in Section [1](#sect:intro){reference-type="ref" reference="sect:intro"} for examples) and align it with the horizontal axis of the transect.

# Mutual Information-Based Path Planning {#se:m2ipp}

**Notations.** Recall that the team of $k$ robots selects $k$ locations $x_i$ to be sampled from column $i$ of the transect for $i =1,\ldots,n$. Let $u_i$ denote a vector of remaining $r-k$ unobserved locations in column $i$ and $Z_{u_{i}}$ denote a vector of the corresponding random measurements. Let $u_{i:j}$ and $Z_{u_{i:j}}$ denote vectors concatenating remaining unobserved locations $u_i, \ldots, u_j$ and concatenating corresponding random measurements $Z_{u_i}, \ldots, Z_{u_j}$ over stages $i$ to $j$, respectively.

**Maximum Mutual Information Path Planning (M$^2$IPP).** An alternative to MEPP is to plan non-myopic observation paths $x_{1:n}^{\star}$ that share the maximum mutual information with the remaining unobserved locations $u_{1:n}^{\star}$ of the transect: $$\begin{equation}
\begin{array}{rl}
    x^{\star}_{1:n}=&\hspace{-2mm}\displaystyle \mathop{\arg\max}_{x_{1:n} \in \mathcal{X}_{1:n}} I(Z_{x_{1:n}}; Z_{u_{1:n}})\\
    I(Z_{x_{1:n}}; Z_{u_{1:n}}) \triangleq &\hspace{-2mm} H(Z_{u_{1:n}}) - H(Z_{u_{1:n}} | Z_{x_{1:n}}) \ .\vspace{-0.5mm}
\end{array}
    \label{mipp1}
\end{equation}$$ From ([\[mipp1\]](#mipp1){reference-type="ref" reference="mipp1"}), $I(Z_{x_{1:n}}; Z_{u_{1:n}})$ measures the reduction in entropy/ uncertainty of the measurements $Z_{u_{1:n}}$ at the remaining unobserved locations $u_{1:n}$ of the transect by observing the measurements $Z_{x_{1:n}}$ to be sampled along the paths $x_{1:n}$. So, the path planning of M$^2$IPP ([\[mipp1\]](#mipp1){reference-type="ref" reference="mipp1"}) is equivalent to the selection of remaining unobserved locations with the largest entropy reduction (i.e., determining $u_{1:n}^{\star}$). This may be mistakenly perceived as the selection of remaining unobserved locations with the lowest uncertainty (i.e., minimizing posterior entropy term $H(Z_{u_{1:n}} | Z_{x_{1:n}})$ in ([\[mipp1\]](#mipp1){reference-type="ref" reference="mipp1"})), which is exactly what the path planning of MEPP ([\[mepp:pw03\]](#mepp:pw03){reference-type="ref" reference="mepp:pw03"}) can achieve, as mentioned in Section [3](#se:mepp){reference-type="ref" reference="se:mepp"}. Note, however, that the maximum mutual information paths ([\[mipp1\]](#mipp1){reference-type="ref" reference="mipp1"}) planned by M$^2$IPP can in fact induce a very large prior entropy $H(Z_{u_{1:n}})$ but not necessarily the smallest posterior entropy $H(Z_{u_{1:n}} | Z_{x_{1:n}})$. Consequently, MEPP and M$^2$IPP exhibit different path planning behaviors and resulting active sensing performances, as shown empirically in Section [5](#se:exp){reference-type="ref" reference="se:exp"}.

Similar to MEPP, M$^2$IPP incurs exponential time in the length of planning horizon. To relieve this computational burden, we will describe an approximation algorithm for planning maximum mutual information paths next.

**Approximate M$^2$IPP$(m)$.** We will exploit the same property of the covariance function ([\[kf\]](#kf){reference-type="ref" reference="kf"}) as that used by MEPP$(m)$ (Section [3](#se:mepp){reference-type="ref" reference="se:mepp"}) to establish a trade-off between active sensing performance and computational efficiency for our M$^2$IPP$(m)$ algorithm. However, this is not as straightforward to achieve as that to derive MEPP$(m)$ where a $m$-th order Markov property can simply be imposed on each posterior entropy term in ([\[mef1\]](#mef1){reference-type="ref" reference="mef1"}). To illustrate this, using the chain rule for mutual information [@Cover91], $$\begin{equation*}
\hspace{-1.5mm}
\begin{array}{rl}
      I(Z_{x_{1:n}};Z_{u_{1:n}}) = &\hspace{-2mm} I(Z_{x_{1:m}};Z_{u_{1:n}}) +
      \hspace{-1mm}\displaystyle\sum_{i=m+1}^{n-m-1} \hspace{-1mm}I(Z_{x_i};Z_{u_{1:n}}| Z_{x_{1:i-1}})\\
       &\hspace{-2mm} +\
 I(Z_{x_{n-m:n}}; Z_{u_{1:n}}|Z_{x_{1:n-m-1}})\ ,\vspace{-0.5mm}
     \end{array}
%\label{mipp2}
\end{equation*}$$ after which a $m$-th order Markov property is assumed to yield the following approximation: $$\begin{equation}
\hspace{-1.5mm}
\begin{array}{rl}
     I(Z_{x_{1:n}};Z_{u_{1:n}})\approx & \hspace{-2mm} I(Z_{x_{1:m}};Z_{u_{1:n}}) +\hspace{-1mm} 
      \displaystyle\sum_{i=m+1}^{n-m-1}\hspace{-1mm} I(Z_{x_i}; Z_{u_{1:n}}|Z_{x_{i-m:i-1}})\\ 
      &\hspace{-2mm}  +\
          I(Z_{x_{n-m:n}}; Z_{u_{1:n}}|Z_{x_{n-2m:n-m-1}})\ .\vspace{-1mm}
\end{array}
\label{mipp2}
\end{equation}$$ From ([\[mipp2\]](#mipp2){reference-type="ref" reference="mipp2"}), note that each conditional mutual information term $I(Z_{x_i}; Z_{u_{1:n}}|Z_{x_{i-m:i-1}})$ cannot be evaluated individually because the remaining unobserved locations $u_{1:n}$ of the transect (specifically, $u_{1:i-m-1}$ and $u_{i+1:n}$ in the respective columns $1$ to $i-m-1$ and $i+1$ to $n$) cannot be determined simply by knowing the robots' past and current sampling locations $x_{i-m:i-1}$ and $x_i$ in columns $i-m$ to $i$.

To resolve this, we exploit the same property of the covariance function ([\[kf\]](#kf){reference-type="ref" reference="kf"}) as that used by MEPP$(m)$ (Section [3](#se:mepp){reference-type="ref" reference="se:mepp"}) again: It makes the measurements $Z_{x_i}$ to be observed next in column $i$ near-independent of the distant unobserved measurements $Z_{u_{1:i-m-1}}$ and $Z_{u_{i+m+1:n}}$ in the respective columns $1$ to $i-m-1$ and $i+m+1$ to $n$ (i.e., far from column $i$) for a sufficiently large $m$ by conditioning on the closer measurements $Z_{x_{i-m:i-1}}$ and $Z_{u_{i-m:i+m}}$ in columns $i-m$ to $i+m$ (i.e., closer to column $i$). As a result, each term $I(Z_{x_i}; Z_{u_{1:n}}|Z_{x_{i-m:i-1}})$ in ([\[mipp2\]](#mipp2){reference-type="ref" reference="mipp2"}) can be closely approximated by $I(Z_{x_i}; Z_{u_{i-m:i+m}}|Z_{x_{i-m:i-1}})$ for $i=m+1,\ldots,n-m-1$: $$\begin{array}{l}
I(Z_{x_i}; Z_{u_{1:n}}|Z_{x_{i-m:i-1}})\vspace{0.5mm}\\
= H(Z_{x_i}|Z_{x_{i-m:i-1}}) - H(Z_{x_i}|Z_{x_{i-m:i-1}}, Z_{u_{1:n}})\vspace{0.5mm}\\
\approx H(Z_{x_i}|Z_{x_{i-m:i-1}}) - H(Z_{x_i}|Z_{x_{i-m:i-1}}, Z_{u_{i-m:i+m}})\vspace{0.5mm}\\
= I(Z_{x_i}; Z_{u_{i-m:i+m}}|Z_{x_{i-m:i-1}})%\vspace{-0.5mm}
\end{array}$$ where the approximation follows from the above-mentioned conditional independence assumption and the equalities are due to the definition of conditional mutual information [@Cover91]. Similarly, $I(Z_{x_{1:m}};Z_{u_{1:n}})$ and $I(Z_{x_{n-m:n}}; Z_{u_{1:n}}|Z_{x_{n-2m:n-m-1}})$ in ([\[mipp2\]](#mipp2){reference-type="ref" reference="mipp2"}) are, respectively, approximated by $I(Z_{x_{1:m}};Z_{u_{1:2m}})$ and $I(Z_{x_{n-m:n}}; Z_{u_{n-2m:n}}|Z_{x_{n-2m:n-m-1}})$. Then, $$\begin{equation}
\hspace{-1.5mm}
\begin{array}{l}
I(Z_{x_{1:n}};Z_{u_{1:n}}) \approx \hspace{0mm}I(Z_{x_{1:m}};Z_{u_{1:2m}}) \\
\hspace{25.0mm} + \displaystyle\sum_{i=m+1}^{n-m-1} I(Z_{x_{i}};Z_{u_{i-m:i+m}}| Z_{x_{i-m:i-1}})\\
\hspace{25.0mm}+\ I(Z_{x_{n-m:n}}; Z_{u_{n-2m:n}}|Z_{x_{n-2m:n-m-1}})\\
= I(Z_{x_{1:m}};Z_{u_{1:2m}}) +\hspace{-1mm} \displaystyle\sum_{i=2m+1}^{n-1}\hspace{-1mm} I(Z_{x_{i-m}};Z_{u_{i-2m:i}}| Z_{x_{i-2m:i-m-1}})\\
\hspace{3.4mm} +\ I(Z_{x_{n-m:n}}; Z_{u_{n-2m:n}}|Z_{x_{n-2m:n-m-1}})\ .\vspace{-1mm}
\end{array}
\label{mipp05}
\end{equation}$$ Using ([\[mipp05\]](#mipp05){reference-type="ref" reference="mipp05"}), M$^2$IPP ([\[mipp1\]](#mipp1){reference-type="ref" reference="mipp1"}) can be approximated by the following stage-wise dynamic programming equations, which we call M$^2$IPP$(m)$: $$\begin{equation}
\hspace{-1.5mm}
\begin{array}{rl}
    U_{i}(x_{i-2m:i-1}) =&  \hspace{-2mm}\displaystyle \max_{x_i \in \mathcal{X}_i} I( Z_{x_{i-m}} ; Z_{u_{i-2m:i}} |
    Z_{x_{i-2m:i-m-1}}) \\
&   \hspace{6mm}+ \ U_{i+1}(x_{i-2m+1:i}) \\
U_{n}(x_{n-2m:n-1}) =&  \hspace{-2.6mm}\displaystyle \max_{x_n \in \mathcal{X}_n} I(Z_{x_{n-m:n}}; Z_{u_{n-2m:n}}|Z_{x_{n-2m:n-m-1}})\vspace{-1mm}
\end{array} 
\label{maxmi2}
\end{equation}$$ for stage $i = 2m+1,\ldots,n-1$, each of which induces a corresponding optimal vector $x^{{\mbox{\tiny{$\mathbb{M}$}}}}_i$ of $k$ locations given the optimal vector $x^{{\mbox{\tiny{$\mathbb{M}$}}}}_{i-2m:i-1}$ obtained from previous stages $i-2m$ to $i-1$[^2]. Note that the term $I( Z_{x_{i-m}} ; Z_{u_{i-2m:i}} |Z_{x_{i-2m:i-m-1}})$ in each stage $i$ can be evaluated now because the remaining unobserved locations $u_{i-2m:i}$ in columns $i-2m$ to $i$ can be determined since the robots' past and current sampling locations $x_{i-2m:i-1}$ and $x_i$ in the same columns are given (i.e., as input to $U_i$ and under the max operator, respectively). Let the optimal observation paths of M$^2$IPP$(m)$ be denoted by $x^{{\mbox{\tiny{$\mathbb{M}$}}}}_{1:n}$ that concatenates $$\begin{equation}
    %x^{\mathtt{mi}}_{1:2m} =  \displaystyle \max_{x_{1:2m} \in \mathcal{X}_{1:2m}}
    x^{{\mbox{\tiny{$\mathbb{M}$}}}}_{1:2m} =\underset{x_{1:2m} \in \mathcal{X}_{1:2m}}{\operatorname{\arg\max}} I(Z_{x_{1:m}},
    Z_{u_{1:2m}}) + U_{2m+1}(x_{1:2m}) \vspace{-0.5mm}
    \label{maxmis}
\end{equation}$$ for the first $2m$ stages and $x^{{\mbox{\tiny{$\mathbb{M}$}}}}_{2m+1}, \ldots, x^{{\mbox{\tiny{$\mathbb{M}$}}}}_{n}$ derived using ([\[maxmi2\]](#maxmi2){reference-type="ref" reference="maxmi2"}) for the subsequent stages $2m+1$ to $n$. []{#mipp:ta label="mipp:ta"}

::: {#timemi .theorem}
**Theorem 3** (Time Complexity). * Deriving  $x^{{\mbox{\tiny{$\mathbb{M}$}}}}_{1:n}$  of\
*M$^2$IPP*$(m)$ requires $\mathcal{O}\hspace{-0.7mm}\left(\chi^{2m+1}[n+ 2(r(2m+1))^3]\right)$ time.*
:::

Its proof is given in [@LowArxiv13]. Unlike M$^2$IPP that scales exponentially in the planning horizon length $n$, our M$^2$IPP$(m)$ algorithm scales linearly in $n$.

[]{#mipp:pg label="mipp:pg"} The following result bounds the loss in active sensing performance of the M$^2$IPP$(m)$ algorithm (i.e., ([\[maxmi2\]](#maxmi2){reference-type="ref" reference="maxmi2"}) and ([\[maxmis\]](#maxmis){reference-type="ref" reference="maxmis"})) relative to that of M$^2$IPP ([\[mipp1\]](#mipp1){reference-type="ref" reference="mipp1"}):

::: {#theomi .theorem}
**Theorem 4** (Performance Guarantee). *The paths $x^{{\mbox{\tiny{$\mathbb{M}$}}}}_{1:n}$ are $\varepsilon$-optimal in achieving the maximum mutual information criterion, i.e., $I(Z_{x^\star_{1:n}}; Z_{u^\star_{1:n}}) - I(Z_{x^{{\mbox{\tiny{$\mathbb{M}$}}}}_{1:n}};Z_{u^{{\mbox{\tiny{$\mathbb{M}$}}}}_{1:n}})\leq\varepsilon$ where $$\varepsilon\triangleq k(n-2m)\hspace{-1mm}\left[rn + \frac{1}{2}k(n-2m) \right] \log\hspace{-0.7mm}\left\{\hspace{-0.5mm}1\hspace{-0.5mm}+\hspace{-0.5mm}\frac{\exp\hspace{-0.7mm}\left\{-\frac{(m+1)^2}{2\ell'^{2}_1} \right\}^2}{\eta(1+\eta)}\hspace{-0.5mm}\right\}\hspace{-0.5mm}.$$*
:::

Its proof is given in [@LowArxiv13]. As shown in Theorem [4](#theomi){reference-type="ref" reference="theomi"}, decreasing $\varepsilon$ improves the active sensing performance of M$^2$IPP$(m)$; this can be achieved in a similar manner to that for decreasing the loss bound $\epsilon$ of MEPP$(m)$ (see paragraph after Theorem [2](#theoEd){reference-type="ref" reference="theoEd"}) since the two loss bounds $\varepsilon$ and $\epsilon$ are similar. In addition, smaller number $r$ of sampling locations in each column decreases $\varepsilon$. M$^2$IPP$(m)$ shares the same implications as that of MEPP$(m)$: (a) Increasing $m$ trades off time efficiency (Theorem [3](#timemi){reference-type="ref" reference="timemi"}) for improved active sensing performance, and (b) M$^2$IPP$(m)$ can exploit a low spatial correlation $\ell'_1$ of the anisotropic field along the transect to improve time efficiency (i.e., only requiring a small $m$) while preserving near-optimal active sensing performance (i.e., still maintaining a relatively tight bound $\varepsilon$).

# Experiments and Discussion {#se:exp}

This section evaluates the active sensing performance and computational efficiency of the MEPP$(m)$ (i.e., ([\[mlme2\]](#mlme2){reference-type="ref" reference="mlme2"}) and ([\[mlmax\]](#mlmax){reference-type="ref" reference="mlmax"})) and M$^2$IPP$(m)$ (i.e., ([\[maxmi2\]](#maxmi2){reference-type="ref" reference="maxmi2"}) and ([\[maxmis\]](#maxmis){reference-type="ref" reference="maxmis"})) algorithms empirically on two real-world datasets: (a) May $2009$ temperature field data of Panther Hollow Lake in Pittsburgh, PA spatially distributed over a $25$ m by $150$ m transect that is discretized into a $5 \times 30$ grid [@LowAeroconf10], and (b) June $2009$ plankton density field data of Chesapeake Bay spatially distributed over a $314$ m by $1765$ m transect that is discretized into a $8 \times 45$ grid [@LowSPIE09]. These environmental phenomena are modeled by GPs with hyperparameters (i.e., horizontal and vertical length-scales, signal and noise variances) (Section [2.2](#back:gp){reference-type="ref" reference="back:gp"}) learned using maximum likelihood estimation (MLE) [@Rasmussen06]: (a) $\ell_1 =40.45$ m, $\ell_2 = 16.00$ m, $\sigma^2_s =0.1542$, and $\sigma^2_n = 0.0036$ for the temperature field, and (b) $\ell_1 = 27.53$ m, $\ell_2 = 134.64$ m, $\sigma^2_s =2.152$, and $\sigma^2_n = 0.041$ for the plankton density field. It can be observed that the temperature and plankton density fields have low noise-to-signal ratios $\eta$ of $0.023$ and $0.019$, respectively. Also, though both fields are observed to be highly anisotropic, the spatial correlation of the temperature field is much higher along the transect than perpendicular to it. According to Theorems [2](#theoEd){reference-type="ref" reference="theoEd"} and [4](#theomi){reference-type="ref" reference="theomi"}, such field conditions lead to loose performance loss bounds for both algorithms, which does not necessarily imply their poor performance. So, the empirical evaluation here complements our theoretical results by assessing their performance-efficiency trade-off (i.e., by varying $m$) under these less favorable field conditions. To further investigate our algorithms' trade-off behaviors under different horizontal and vertical spatial correlations, the corresponding length-scales $\ell_1$ and $\ell_2$ of the original temperature field (Fig. [2](#figtfda){reference-type="ref" reference="figtfda"}d) are reduced and fixed to produce three other modified fields (Figs. [2](#figtfda){reference-type="ref" reference="figtfda"}a, [2](#figtfda){reference-type="ref" reference="figtfda"}b, [2](#figtfda){reference-type="ref" reference="figtfda"}c) with the signal and noise variances $\sigma^2_s$ and $\sigma^2_n$ learned using MLE.

:::: {#figtfda .figure}
  ------------------------------------------ -------------------------------------------
             ![image](Cao2013MultiRobot_figs/tfda7.png)                         ![image](Cao2013MultiRobot_figs/tfda6.png)
     \(a\) $\ell_1 = 5$ m, $\ell_2=5$ m.        \(b\) $\ell_1 = 5$ m, $\ell_2=16$ m.
             ![image](Cao2013MultiRobot_figs/tfda5.png)                         ![image](Cao2013MultiRobot_figs/tfda1.png)
   \(c\) $\ell_1 = 40.45$ m, $\ell_2= 5$ m.   \(d\) $\ell_1 = 40.45$ m, $\ell_2= 16$ m.
  ------------------------------------------ -------------------------------------------

::: caption
Temperature fields (measured in$\,^{\circ}\mathrm{C}$) discretized into $5 \times 30$ grids with varying horizontal and vertical length-scales.
:::
::::

**Comparison with Active Sensing Algorithms.** The performance of our proposed algorithms is compared to that of state-of-the-art information-theoretic path planning algorithms for active sensing: The work of [@LowICAPS09] has proposed the following *greedy maximum entropy path planning* (gMEPP) algorithm: $$\begin{equation}
    {V}^{\mbox{\tiny{g}}}_i(x_{1:i-1}) =  \displaystyle \max_{x_{i} \in \mathcal{X}_{i}} H(Z_{x_{i}}| Z_{x_{1:i-1}})\vspace{-1mm}
    \label{erge1}
\end{equation}$$ for stage $i = 1, \ldots, n$, each of which induces a corresponding optimal vector $x^{\mbox{\tiny{${\mathcal E}$}}}_{i}$ of $k$ locations given the optimal vector $x^{\mbox{\tiny{${\mathcal E}$}}}_{1:i-1}$ obtained from previous stages $1$ to $i-1$. A *greedy maximum mutual information path planning* (gM$^2$IPP) algorithm is devised by [@Guestrin08] as follows: $$\begin{equation}
    {U}^{\mbox{\tiny{g}}}_i(x_{1:i-1}) = \displaystyle \max_{x_{i} \in \mathcal{X}_{i}} I(Z_{x_{1:i}};Z_{\overline{x}_{1:i}})\vspace{-1mm}
    \label{ergm1}
\end{equation}$$ for stage $i = 1, \ldots, n$, each of which induces a corresponding optimal vector $x^{\mbox{\tiny{${\mathcal M}$}}}_{i}$ of $k$ locations given the optimal vector $x^{\mbox{\tiny{${\mathcal M}$}}}_{1:i-1}$ obtained from previous stages $1$ to $i-1$, and $\overline{x}_{1:i}$ denotes a vector of all sampling locations in the domain ${\mathcal D}$ excluding those of $x_{1:i}$. As mentioned earlier in Section [3](#se:mepp){reference-type="ref" reference="se:mepp"}, the work of [@LowAAMAS11] has developed MEPP$(1)$, which is a special case of our MEPP$(m)$ algorithm.

In contrast to our MEPP$(m)$ and M$^2$IPP$(m)$ algorithms that scale linearly in the length $n$ of planning horizon (Theorems [1](#timeme){reference-type="ref" reference="timeme"} and [3](#timemi){reference-type="ref" reference="timemi"}), deriving $x^{\mbox{\tiny{${\mathcal E}$}}}_{1:n}$ of gMEPP and $x^{\mbox{\tiny{${\mathcal M}$}}}_{1:n}$ of gM$^2$IPP incurs quartic time in $n$. Hence, if the required value of $m$ is sufficiently small, then MEPP$(m)$ and M$^2$IPP$(m)$ can be more efficient than the greedy algorithms, as shown below.

:::: table*
::: tiny
+:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| +------------------------------------------------------------------+--------------------------------------------------+-------------------------------------------+-----------------------------------------------+ |
| |                                                                  | EN$(x_{1:n})$                                    | MI$(x_{1:n})$                             | ER$(x_{1:n})$                                 | |
| +:================================================================:+:=========:+:==========:+:==========:+:==========:+:========:+:========:+:========:+:========:+:=========:+:=========:+:=========:+:=========:+ |
| | 1 robot                                                          | Field                                            | Field                                     | Field                                         | |
| +------------------------------------------------------------------+-----------+------------+------------+------------+----------+----------+----------+----------+-----------+-----------+-----------+-----------+ |
| | Algorithm                                                        | a         | b          | c          | d          | a        | b        | c        | d        | a         | b         | c         | d         | |
| +------------------------------------------------------------------+-----------+------------+------------+------------+----------+----------+----------+----------+-----------+-----------+-----------+-----------+ |
| | gM$^2$IPP: $x^{\mbox{\tiny{${\mathcal M}$}}}_{1:n}$[@Guestrin08] | -64.4     | -123.9     | -173.3     | -182.2     | 27.9     | 48.4     | 46.0     | 39.5     | 1.764     | 0.581     | 0.088     | 0.042     | |
| +------------------------------------------------------------------+-----------+------------+------------+------------+----------+----------+----------+----------+-----------+-----------+-----------+-----------+ |
| | gMEPP: $x^{\mbox{\tiny{${\mathcal E}$}}}_{1:n}$[@LowICAPS09]     | -64.8     | -128.4     | -173.3     | -182.4     | 26.5     | 44.7     | 46.0     | 39.5     | 2.792     | 0.572     | 0.077     | 0.037     | |
| +------------------------------------------------------------------+-----------+------------+------------+------------+----------+----------+----------+----------+-----------+-----------+-----------+-----------+ |
| | **M$^2$IPP**$(m)$: $x^{{\mbox{\tiny{$\mathbb{M}$}}}}_{1:n}$      | (1) -64.5 | (1) -123.9 | (1) -167.2 | (1) -182.0 | (1) 27.9 | (1) 48.4 | (1) 39.6 | (1) 39.4 | (1) 1.764 | (1) 0.581 | (1) 0.488 | (1) 0.049 | |
| +------------------------------------------------------------------+-----------+------------+------------+------------+----------+----------+----------+----------+-----------+-----------+-----------+-----------+ |
| |                                                                  |           |            | (2) -173.2 |            |          |          | (2) 45.8 |          |           |           | (2) 0.110 | (2) 0.042 | |
| +------------------------------------------------------------------+-----------+------------+------------+------------+----------+----------+----------+----------+-----------+-----------+-----------+-----------+ |
| |                                                                  |           |            |            |            |          |          |          |          |           |           |           | (3) 0.034 | |
| +------------------------------------------------------------------+-----------+------------+------------+------------+----------+----------+----------+----------+-----------+-----------+-----------+-----------+ |
| | **MEPP**$(m)$: $x^{{\mbox{\tiny{$\mathbb{E}$}}}}_{1:n}$          | (1) -64.8 | (1) -128.4 | (1) -161.2 | (1) -180.4 | (1) 23.9 | (1) 44.7 | (1) 33.2 | (1) 36.9 | (1) 5.115 | (1) 0.572 | (1) 3.765 | (1) 0.757 | |
| +------------------------------------------------------------------+-----------+------------+------------+------------+----------+----------+----------+----------+-----------+-----------+-----------+-----------+ |
| |                                                                  | (2) -64.9 |            | (2) -167.2 | (2) -182.4 | (2) 26.3 |          | (2) 39.6 | (2) 39.5 | (2) 2.315 |           | (2) 0.501 | (2) 0.026 | |
| +------------------------------------------------------------------+-----------+------------+------------+------------+----------+----------+----------+----------+-----------+-----------+-----------+-----------+ |
| |                                                                  |           |            | (3) -171.6 |            |          |          | (3) 44.2 |          | (3) 2.080 |           | (3) 0.241 |           | |
| +------------------------------------------------------------------+-----------+------------+------------+------------+----------+----------+----------+----------+-----------+-----------+-----------+-----------+ |
| |                                                                  |           |            | (4) -173.4 |            |          |          | (4) 46.1 |          |           |           | (4) 0.068 |           | |
| +------------------------------------------------------------------+-----------+------------+------------+------------+----------+----------+----------+----------+-----------+-----------+-----------+-----------+ |
+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| +------------------------------------------------------------------+--------------------------------------------------+-------------------------------------------+-----------------------------------------------+ |
| | 2 robots                                                         | Field                                            | Field                                     | Field                                         | |
| +:================================================================:+:=========:+:==========:+:==========:+:==========:+:========:+:========:+:========:+:========:+:=========:+:=========:+:=========:+:=========:+ |
| | Algorithm                                                        | a         | b          | c          | d          | a        | b        | c        | d        | a         | b         | c         | d         | |
| +------------------------------------------------------------------+-----------+------------+------------+------------+----------+----------+----------+----------+-----------+-----------+-----------+-----------+ |
| | gM$^2$IPP: $x^{\mbox{\tiny{${\mathcal M}$}}}_{1:n}$[@Guestrin08] | -57.8     | -100.5     | -132.9     | -138.0     | 41.7     | 62.0     | 45.8     | 36.9     | 1.153     | 0.265     | 0.019     | 0.016     | |
| +------------------------------------------------------------------+-----------+------------+------------+------------+----------+----------+----------+----------+-----------+-----------+-----------+-----------+ |
| | gMEPP: $x^{\mbox{\tiny{${\mathcal E}$}}}_{1:n}$[@LowICAPS09]     | -59.8     | -112.2     | -132.9     | -138.8     | 41.2     | 55.8     | 45.9     | 36.2     | 0.521     | 0.439     | 0.033     | 0.018     | |
| +------------------------------------------------------------------+-----------+------------+------------+------------+----------+----------+----------+----------+-----------+-----------+-----------+-----------+ |
| | **M$^2$IPP**$(m)$: $x^{{\mbox{\tiny{$\mathbb{M}$}}}}_{1:n}$      | (1) -57.8 | (1) -100.5 | (1) -132.9 | (1) -138.2 | (1) 41.2 | (1) 62.0 | (1) 45.9 | (1) 36.9 | (1) 0.605 | (1) 0.265 | (1) 0.020 | (1) 0.018 | |
| +------------------------------------------------------------------+-----------+------------+------------+------------+----------+----------+----------+----------+-----------+-----------+-----------+-----------+ |
| |                                                                  |           |            |            |            | (2) 41.8 |          |          |          |           |           |           | (2) 0.014 | |
| +------------------------------------------------------------------+-----------+------------+------------+------------+----------+----------+----------+----------+-----------+-----------+-----------+-----------+ |
| | **MEPP$(m)$**: $x^{{\mbox{\tiny{$\mathbb{E}$}}}}_{1:n}$          | (1) -59.8 | (1) -113.0 | (1) -129.3 | (1) -138.4 | (1) 41.6 | (1) 56.4 | (1) 41.8 | (1) 36.9 | (1) 0.662 | (1) 0.378 | (1) 0.286 | (1) 0.012 | |
| +------------------------------------------------------------------+-----------+------------+------------+------------+----------+----------+----------+----------+-----------+-----------+-----------+-----------+ |
| |                                                                  | (2) -60.0 |            | (2) -132.9 |            |          |          | (2) 45.9 |          |           |           | (2) 0.018 |           | |
| +------------------------------------------------------------------+-----------+------------+------------+------------+----------+----------+----------+----------+-----------+-----------+-----------+-----------+ |
+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| +------------------------------------------------------------------+-----------------------------------------------+-------------------------------------------+-----------------------------------------------+    |
| | 3 robots                                                         | Field                                         | Field                                     | Field                                         |    |
| +:================================================================:+:=========:+:=========:+:=========:+:=========:+:========:+:========:+:========:+:========:+:=========:+:=========:+:=========:+:=========:+    |
| | Algorithm                                                        | a         | b         | c         | d         | a        | b        | c        | d        | a         | b         | c         | d         |    |
| +------------------------------------------------------------------+-----------+-----------+-----------+-----------+----------+----------+----------+----------+-----------+-----------+-----------+-----------+    |
| | gM$^2$IPP: $x^{\mbox{\tiny{${\mathcal M}$}}}_{1:n}$[@Guestrin08] | -46.5     | -80.5     | -89.5     | -92.8     | 40.8     | 61.3     | 41.4     | 31.6     | 0.272     | 0.012     | 0.018     | 0.008     |    |
| +------------------------------------------------------------------+-----------+-----------+-----------+-----------+----------+----------+----------+----------+-----------+-----------+-----------+-----------+    |
| | gMEPP: $x^{\mbox{\tiny{${\mathcal E}$}}}_{1:n}$[@LowICAPS09]     | -46.3     | -80.6     | -89.5     | -93.2     | 40.5     | 60.6     | 41.3     | 28.6     | 0.257     | 0.024     | 0.017     | 0.009     |    |
| +------------------------------------------------------------------+-----------+-----------+-----------+-----------+----------+----------+----------+----------+-----------+-----------+-----------+-----------+    |
| | **M$^2$IPP**$(m)$: $x^{{\mbox{\tiny{$\mathbb{M}$}}}}_{1:n}$      | (1) -46.5 | (1) -72.0 | (1) -89.4 | (1) -92.1 | (1) 40.8 | (1) 60.0 | (1) 38.8 | (1) 32.0 | (1) 0.272 | (1) 0.123 | (1) 0.016 | (1) 0.008 |    |
| +------------------------------------------------------------------+-----------+-----------+-----------+-----------+----------+----------+----------+----------+-----------+-----------+-----------+-----------+    |
| |                                                                  |           |           | (2) -89.5 |           |          |          | (2) 41.3 |          | (2) 0.229 |           | (2) 0.014 |           |    |
| +------------------------------------------------------------------+-----------+-----------+-----------+-----------+----------+----------+----------+----------+-----------+-----------+-----------+-----------+    |
| | **MEPP$(m)$**: $x^{{\mbox{\tiny{$\mathbb{E}$}}}}_{1:n}$          | (1) -45.9 | (1) -81.3 | (1) -89.4 | (1) -93.5 | (1) 40.2 | (1) 61.6 | (1) 38.7 | (1) 28.2 | (1) 0.231 | (1) 0.014 | (1) 0.013 | (1) 0.007 |    |
| +------------------------------------------------------------------+-----------+-----------+-----------+-----------+----------+----------+----------+----------+-----------+-----------+-----------+-----------+    |
| |                                                                  | (2) -46.5 |           |           |           | (2) 40.8 |          | (4) 41.1 | (3) 28.6 |           |           |           |           |    |
| +------------------------------------------------------------------+-----------+-----------+-----------+-----------+----------+----------+----------+----------+-----------+-----------+-----------+-----------+    |
| |                                                                  |           |           |           |           |          |          |          | (4) 29.0 |           |           |           |           |    |
| +------------------------------------------------------------------+-----------+-----------+-----------+-----------+----------+----------+----------+----------+-----------+-----------+-----------+-----------+    |
+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
:::
::::

**Performance Metrics.** The tested algorithms are evaluated using three different metrics: The (a) entropy metric EN$(x_{1:n}) \triangleq H(Z_{u_{1:n}}|Z_{x_{1:n}})$ and (b) mutual information metric MI$(x_{1:n}) \triangleq I(Z_{x_{1:n}}; Z_{u_{1:n}})$ measure, respectively, the posterior entropy/uncertainty and the reduction in entropy/ uncertainty at the remaining unobserved locations $u_{1:n}$ of the transect given the observation paths $x_{1:n}$. The difference between the entropy and mutual information metrics has been explained in the paragraph after ([\[mipp1\]](#mipp1){reference-type="ref" reference="mipp1"}) in Section [4](#se:m2ipp){reference-type="ref" reference="se:m2ipp"}.

The (c) ER$(x_{1:n}) \triangleq ||z_{u_{1:n}} - \mu_{u_{1:n} |x_{1:n}}||^2_2\slash\{\overline{\mu}^2 n(r-k)\}$ metric measures the mean-squared relative prediction error resulting from using the posterior mean $\mu_{u |x_{1:n}}$ ([\[gpmm\]](#gpmm){reference-type="ref" reference="gpmm"}) to predict the measurements at the remaining $n(r-k)$ unobserved locations $u_{1:n}$ of the transect given the measurements sampled along the observation paths $x_{1:n}$ where $\overline{\mu} = 1^{\top} z_{u_{1:n}} \slash \{n(r-k)\}$. It has an advantage over the two information-theoretic metrics of using ground truth measurements to evaluate if the phenomenon is being predicted accurately. However, unlike the EN$(x_{1:n})$ and MI$(x_{1:n})$ metrics that account for the spatial correlation between measurements at the unobserved locations $u_{1:n}$, the ER$(x_{1:n})$ metric assumes conditional independence between them. In contrast to the ER$(x_{1:n})$ metric, the EN$(x_{1:n})$ and MI$(x_{1:n})$ metrics consequently do not overestimate their uncertainty.

## Temperature Field Data {#er:tdr}

Table [\[tab:entcompare\]](#tab:entcompare){reference-type="ref" reference="tab:entcompare"} shows the results of EN$(x_{1:n})$, MI$(x_{1:n})$, and ER$(x_{1:n})$ performance of tested algorithms for temperature fields with different horizontal and vertical length-scales (Fig. [2](#figtfda){reference-type="ref" reference="figtfda"}) and with varying number of robots. For our proposed M$^2$IPP$(m)$ and MEPP$(m)$ algorithms, the results are reported in an increasing order of $m$ until the performance has stabilized. It can be observed from Table [\[tab:entcompare\]](#tab:entcompare){reference-type="ref" reference="tab:entcompare"} that MEPP$(m)$ with $m>1$ or M$^2$IPP$(m)$ often outperforms MEPP$(1)$ [@LowAAMAS11] in the three metrics, as discussed and explained later. Note that every increment of $m$ increases the length of history of sampling locations considered in each stage by two for M$^2$IPP$(m)$ instead of by one for MEPP$(m)$; this can be seen from the inputs to $U_i$ ([\[maxmi2\]](#maxmi2){reference-type="ref" reference="maxmi2"}) and $V_i$ ([\[mlme2\]](#mlme2){reference-type="ref" reference="mlme2"}), respectively. The observations of the results are detailed in the rest of this subsection.

### Entropy Metric *EN*$(x_{1:n})$ {#er:tdr:em}

As expected, the entropy-based MEPP$(m)$ and gMEPP algorithms generally perform better than or at least as well as the mutual information-based M$^2$IPP$(m)$ and gM$^2$IPP algorithms in this metric.

For fields a, b, and d (i.e., of small $\ell_1$ or large $\ell_2$) with any number of robots, MEPP$(m)$ can produce EN$(x^{{\mbox{\tiny{$\mathbb{E}$}}}}_{1:n})$ values lower than or comparable to that achieved by gMEPP and gM$^2$IPP using small values of $m$ (i.e., $m=1$ or $2$), hence incurring $1$ to $4$ orders of magnitude less computational time, as shown in Fig. [3](#figtemptime){reference-type="ref" reference="figtemptime"}. This can be explained by one of the following reasons: (a) A low spatial correlation along the transect cannot be exploited by gMEPP and gM$^2$IPP, which consider the entire history of past measurements for improving active sensing performance; (b) a high correlation perpendicular to the transect can be exploited by MEPP$(m)$ for better active sensing performance; and (c) unlike the greedy gMEPP and gM$^2$IPP algorithms, MEPP$(m)$ is capable of non-myopic planning to improve active sensing performance.

:::: {#figtemptime .figure}
  --------------------------------------------- --------------------------------------------- ---------------------------------------------
   ![image](Cao2013MultiRobot_figs/temp_time1m7.png){height="22.4mm"}   ![image](Cao2013MultiRobot_figs/temp_time2m5.png){height="22.4mm"}   ![image](Cao2013MultiRobot_figs/temp_time3m5.png){height="22.4mm"}
                                                                                              
  --------------------------------------------- --------------------------------------------- ---------------------------------------------

::: caption
Graphs of incurred time by different active sensing algorithms vs. $m$ for temperature fields with varying number of robots.
:::
::::

For field c (i.e., of large $\ell_1$ and small $\ell_2$) with $1$ robot, MEPP$(m)$ cannot exploit the low spatial correlation perpendicular to the transect for improving active sensing performance. Therefore, it needs to raise the value of $m$ up to $4$ in order to better exploit the high spatial correlation along the transect. Consequently, MEPP$(m)$ can achieve EN$(x^{{\mbox{\tiny{$\mathbb{E}$}}}}_{1:n})$ performance comparable to that achieved by gMEPP and gM$^2$IPP while incurring similar computational time as gMEPP and about $2$ orders of magnitude less time than gM$^2$IPP. Increasing the number of robots allows MEPP$(m)$ to achieve EN$(x^{{\mbox{\tiny{$\mathbb{E}$}}}}_{1:n})$ performance comparable to that of gMEPP and gM$^2$IPP using smaller values of $m$ (i.e., $m=1$ or $2$), hence incurring $1$ to $4$ orders of magnitude less time.

### Mutual Information Metric *MI*$(x_{1:n})$ {#er:tdr:mm}

The mutual information-based M$^2$IPP$(m)$ and gM$^2$IPP algorithms often perform better than or at least as well as the entropy-based MEPP$(m)$ and gMEPP in this metric.

For fields a, b, and d (i.e., of small $\ell_1$ or large $\ell_2$) with any number of robots, M$^2$IPP$(m)$ can generally yield MI$(x^{{\mbox{\tiny{$\mathbb{M}$}}}}_{1:n})$ values higher than or comparable to that achieved by gM$^2$IPP and gMEPP using a small $m$ value of $1$, hence incurring less computational time (in particular, about $2$ orders of magnitude less time than gM$^2$IPP), as shown in Fig. [3](#figtemptime){reference-type="ref" reference="figtemptime"}. This can be explained by the same reasons as that discussed previously in Section [5.1.1](#er:tdr:em){reference-type="ref" reference="er:tdr:em"}.

![Plankton density (chl-a) field (measured in $\mathrm{mg\ m}^{-3}$) discretized into a $8 \times 45$ grid.](Cao2013MultiRobot_figs/chla-task2.png){#figchla}

For field c (i.e., of large $\ell_1$ and small $\ell_2$) with $1$ or $3$ robots, M$^2$IPP$(m)$ cannot exploit the low spatial correlation perpendicular to the transect for improving active sensing performance. So, it has to increase the value of $m$ to $2$ in order to better exploit the high correlation along the transect. As a result, M$^2$IPP$(m)$ can achieve MI$(x^{{\mbox{\tiny{$\mathbb{M}$}}}}_{1:n})$ performance comparable to that achieved by gM$^2$IPP and gMEPP while incurring less time with $1$ robot and slightly more time with $3$ robots than gM$^2$IPP. With $2$ robots, $m=1$ suffices for M$^2$IPP$(m)$ to achieve MI$(x^{{\mbox{\tiny{$\mathbb{M}$}}}}_{1:n})$ performance comparable to that achieved by gM$^2$IPP and gMEPP while incurring less time (Fig. [3](#figtemptime){reference-type="ref" reference="figtemptime"}). A computationally cheaper alternative for active sensing of field c is to consider using MEPP$(m)$ with larger $m$: When the values of $m$ are raised to $4$, $2$, and $4$ for the respective $1$-, $2$-, and $3$-robot cases, it can produce MI$(x^{{\mbox{\tiny{$\mathbb{E}$}}}}_{1:n})$ performance comparable to that achieved by gM$^2$IPP and gMEPP while incurring similar or less time.

### Prediction Error Metric *ER*$(x_{1:n})$ {#er:tdr:pm}

For field c (i.e., of large $\ell_1$ and small $\ell_2$) with any number of robots, MEPP$(m)$ and M$^2$IPP$(m)$ cannot exploit the low spatial correlation perpendicular to the transect for improving active sensing performance. Hence, their values of $m$ need to be raised in order to exploit the high correlation along the transect. Compared to M$^2$IPP$(m)$, it is computationally cheaper (Fig. [3](#figtemptime){reference-type="ref" reference="figtemptime"}) and offers greater performance improvement (Table [\[tab:entcompare\]](#tab:entcompare){reference-type="ref" reference="tab:entcompare"}) to increase the value of $m$ of MEPP$(m)$, which can then produce ER$(x^{{\mbox{\tiny{$\mathbb{E}$}}}}_{1:n})$ values lower than that achieved by gMEPP and gM$^2$IPP while incurring similar computational time to gMEPP and about $2$ orders of magnitude less time than gM$^2$IPP with $1$ robot and $1$ to $4$ orders of magnitude less time than both with $2$ or $3$ robots. For field d (i.e., of large $\ell_1$ and large $\ell_2$) with any number of robots, MEPP$(m)$ can now exploit the high spatial correlation perpendicular to the transect for better active sensing performance. As a result, MEPP$(m)$ can yield better ER$(x^{{\mbox{\tiny{$\mathbb{E}$}}}}_{1:n})$ performance than gMEPP and gM$^2$IPP using smaller values of $m$ (i.e., $m=1$ or $2$), hence incurring $1$ to $4$ orders of magnitude less time.

For fields a and b (i.e., of small $\ell_1$) with $1$ or $2$ robots, M$^2$IPP$(m)$ can produce ER$(x^{{\mbox{\tiny{$\mathbb{M}$}}}}_{1:n})$ values lower than or comparable to that achieved by gM$^2$IPP and gMEPP using a small $m$ value of $1$, hence incurring less time (in particular, about $2$ orders of magnitude less time than gM$^2$IPP), as shown in Fig. [3](#figtemptime){reference-type="ref" reference="figtemptime"}. Increasing to $3$ robots allows MEPP$(m)$ to achieve ER$(x^{{\mbox{\tiny{$\mathbb{E}$}}}}_{1:n})$ performance better than or comparable to that of gMEPP and gM$^2$IPP using a small $m$ value of $1$, hence incurring $3$ to $4$ orders of magnitude less time (Fig. [3](#figtemptime){reference-type="ref" reference="figtemptime"}). These can be explained by the same reasons as that discussed previously in Section [5.1.1](#er:tdr:em){reference-type="ref" reference="er:tdr:em"}.

## Plankton Density Field Data

Table [1](#tab:cl){reference-type="ref" reference="tab:cl"} shows the results of EN$(x_{1:n})$, MI$(x_{1:n})$, and ER$(x_{1:n})$ performance of tested algorithms for the plankton density field (Fig. [4](#figchla){reference-type="ref" reference="figchla"}) with varying number of robots. For our proposed M$^2$IPP$(m)$ and MEPP$(m)$ algorithms, the results are only reported for $m=1$, at which their performance has already stabilized. As mentioned earlier in the first paragraph of Section [5](#se:exp){reference-type="ref" reference="se:exp"}, the plankton density field exhibits low and high spatial correlations, respectively, along and perpendicular to the transect, which resemble that of temperature field b.

:::: tiny
::: {#tab:cl}
+------------------------------------------------------------------+-----------------------------+-----------------------------+-----------------------------+
|                                                                  | EN$(x_{1:n})$               | MI$(x_{1:n})$               | ER$(x_{1:n})$               |
+:================================================================:+:=======:+:=======:+:=======:+:=======:+:=======:+:=======:+:=======:+:=======:+:=======:+
|                                                                  | No. of robots $k$           | No. of robots $k$           | No. of robots $k$           |
+------------------------------------------------------------------+---------+---------+---------+---------+---------+---------+---------+---------+---------+
| Algorithm                                                        | 1       | 2       | 3       | 1       | 2       | 3       | 1       | 2       | 3       |
+------------------------------------------------------------------+---------+---------+---------+---------+---------+---------+---------+---------+---------+
| gM$^2$IPP: $x^{\mbox{\tiny{${\mathcal M}$}}}_{1:n}$[@Guestrin08] | 124     | 55      | 28      | 83      | 162     | 201     | 0.65    | 0.09    | 0.01    |
+------------------------------------------------------------------+---------+---------+---------+---------+---------+---------+---------+---------+---------+
| gMEPP: $x^{\mbox{\tiny{${\mathcal E}$}}}_{1:n}$[@LowICAPS09]     | 117     | 42      | -6      | 65      | 126     | 184     | 1.35    | 0.44    | 0.04    |
+------------------------------------------------------------------+---------+---------+---------+---------+---------+---------+---------+---------+---------+
| **M$^2$IPP**$(m)$: $x^{{\mbox{\tiny{$\mathbb{M}$}}}}_{1:n}$      | 124     | 55      | 28      | 83      | 162     | 201     | 0.65    | 0.09    | 0.01    |
+------------------------------------------------------------------+---------+---------+---------+---------+---------+---------+---------+---------+---------+
| **MEPP$(m)$**: $x^{{\mbox{\tiny{$\mathbb{E}$}}}}_{1:n}$          | 117     | 41      | -8      | 65      | 128     | 187     | 1.35    | 0.41    | 0.01    |
+------------------------------------------------------------------+---------+---------+---------+---------+---------+---------+---------+---------+---------+

: Comparison of EN$(x_{1:n})$, MI$(x_{1:n})$, and ER$(x_{1:n})$ ($\times 10^{-2}$) performance for plankton density field shown in Fig. [4](#figchla){reference-type="ref" reference="figchla"} with varying number of robots.
:::
::::

The observations are as follows: With any number of robots, MEPP$(1)$ can produce EN$(x^{{\mbox{\tiny{$\mathbb{E}$}}}}_{1:n})$ values lower than that achieved by gMEPP and gM$^2$IPP while incurring $2$ to $5$ orders of magnitude less time, as shown in Fig. [5](#figplanktime){reference-type="ref" reference="figplanktime"}. On the other hand, M$^2$IPP$(1)$ can yield MI$(x^{{\mbox{\tiny{$\mathbb{M}$}}}}_{1:n})$ and ER$(x^{{\mbox{\tiny{$\mathbb{M}$}}}}_{1:n})$ performance better than or comparable to that achieved by gM$^2$IPP and gMEPP while incurring less time (in particular, about $2$ orders of magnitude less time than gM$^2$IPP) (Fig. [5](#figplanktime){reference-type="ref" reference="figplanktime"}). These can be explained by the same reasons as that discussed previously in Section [5.1.1](#er:tdr:em){reference-type="ref" reference="er:tdr:em"}.

## Summary of Test Results

The observations of the above results are summarized below: For anisotropic fields with low spatial correlation along the transect (e.g., temperature fields a and b and plankton density field), MEPP$(m)$ can perform better or at least as well as gMEPP and gM$^2$IPP in the prediction error (i.e., with $3$ robots) and entropy metrics using small $m$ values of $1$ or $2$, hence incurring $1$ to $4$ orders of magnitude less time. M$^2$IPP$(m)$ can generally perform likewise in the prediction error (i.e., with $1$ or $2$ robots) and mutual information metrics using a small $m$ value of $1$, hence incurring less time as well (in particular, $2$ orders of magnitude less time than gM$^2$IPP). These observations are previously explained in Section [5.1.1](#er:tdr:em){reference-type="ref" reference="er:tdr:em"}. Note that they corroborate the second implications of Theorems [2](#theoEd){reference-type="ref" reference="theoEd"} and [4](#theomi){reference-type="ref" reference="theomi"} on the performance guarantees of MEPP$(m)$ and M$^2$IPP$(m)$.

For anisotropic fields with high spatial correlation along the transect (e.g., temperature fields c and d), a larger $m$ value is needed in order for MEPP$(m)$ and M$^2$IPP$(m)$ to exploit it if the correlation perpendicular to the transect is low (i.e., field c). Compared to M$^2$IPP$(m)$, it is computationally cheaper to increase the value of $m$ of MEPP$(m)$ such that it performs better or at least as well as gMEPP and gM$^2$IPP in all three metrics while incurring similar time to gMEPP and about $2$ orders of magnitude less time than gM$^2$IPP with $1$ robot and often $1$ to $4$ orders of magnitude less time than both with $2$ or $3$ robots. If the correlation perpendicular to the transect is high (i.e., field d) instead, it can be exploited by MEPP$(m)$ and M$^2$IPP$(m)$ to improve active sensing performance and consequently allow $m$ to be reduced to small values of $1$ or $2$: MEPP$(m)$ can perform better or, if not, at least as well as gMEPP and gM$^2$IPP in the prediction error and entropy metrics while incurring $1$ to $4$ orders of magnitude less time. M$^2$IPP$(m)$ can perform likewise in the mutual information metric while incurring less time (in particular, $2$ orders of magnitude less time than gM$^2$IPP).

:::: {#figplanktime .figure}
  -------------------------------------------- -------------------------------------------- --------------------------------------------
   ![image](Cao2013MultiRobot_figs/plank_time1.png){height="22.4mm"}   ![image](Cao2013MultiRobot_figs/plank_time2.png){height="22.4mm"}   ![image](Cao2013MultiRobot_figs/plank_time3.png){height="22.4mm"}
                                                                                            
  -------------------------------------------- -------------------------------------------- --------------------------------------------

::: caption
Graphs of incurred time by different active sensing algorithms vs. $m$ for plankton density field with varying number of robots.
:::
::::

# Conclusion

This paper describes two principled information-theoretic path planning algorithms based on entropy and mutual information criteria (respectively, MEPP$(m)$ and M$^2$IPP$(m)$) for active sensing of GP-based anisotropic fields. Two important practical implications result from the theoretical guarantees on the active sensing performance of our algorithms (Theorems [2](#theoEd){reference-type="ref" reference="theoEd"} and [4](#theomi){reference-type="ref" reference="theomi"}): Increasing $m$ trades off computational efficiency (Theorems [1](#timeme){reference-type="ref" reference="timeme"} and [3](#timemi){reference-type="ref" reference="timemi"}) for better active sensing performance, and our algorithms can exploit a low spatial correlation along the transect to improve time efficiency (i.e., only needing a small $m$) while preserving near-optimal active sensing performance. This motivates the use of prior knowledge, if available, on a direction of low spatial correlation in order to align it with the horizontal axis of the transect. Empirical evaluation of real-world anisotropic temperature and plankton density field data reveals that our algorithms can perform better or at least as well as gMEPP and gM$^2$IPP while often incurring a few orders of magnitude less time. In particular, it can be observed that anisotropic fields with low spatial correlation along the transect or high correlation perpendicular to the transect allow our algorithms to perform well using small values of $m$, thus yielding significant computational gain over gMEPP and gM$^2$IPP. To perform well in a field with high correlation along the transect and low correlation perpendicular to the transect (i.e., less favorable conditions), our algorithms have to increase the value of $m$ or the number of robots but can still achieve comparable or better time efficiency than gMEPP and gM$^2$IPP.

[^1]: In fact, solving MEPP$(m)$ ([\[mlme2\]](#mlme2){reference-type="ref" reference="mlme2"}) yields a policy that, in each stage $i$, induces an optimal vector for every possible vector $x_{i-m:i-1}$ (including possible diverged paths from $x^{{\mbox{\tiny{$\mathbb{E}$}}}}_{i-m:i-1}$ due to external forces) obtained from previous $m$ stages.

[^2]: Similar to MEPP$(m)$, solving M$^2$IPP$(m)$ ([\[maxmi2\]](#maxmi2){reference-type="ref" reference="maxmi2"}) yields a policy that, in each stage $i$, induces an optimal vector for every possible vector $x_{i-2m:i-1}$ (including possible diverged paths from $x^{{\mbox{\tiny{$\mathbb{E}$}}}}_{i-2m:i-1}$) obtained from previous $2m$ stages.
