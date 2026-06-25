---
citation_key: Low2013InformationTheoretic
arxiv_id: 1305.6129
arxiv_url: "https://arxiv.org/abs/1305.6129"
title: "Information-Theoretic Approach to Efficient Adaptive Path Planning for Mobile Robotic Environmental Sensing"
authors_short: "Kian Hsiang Low et al."
year: 2013
direction_tag: Q_informed_sampling
source: pymupdf4llm
converted_at: 2026-06-24T17:20:43Z
origin: ai+web
reviewed: false
---

# **Information-Theoretic Approach to Efficient Adaptive Path Planning for Mobile Robotic Environmental Sensing** 

**Kian Hsiang Low** _[†]_ and **John M. Dolan** _[†§]_ and **Pradeep Khosla** _[†§]_ Department of Electrical and Computer Engineering _[†]_ , Robotics Institute _[§]_ Carnegie Mellon University 

5000 Forbes Avenue, Pittsburgh, PA 15213, USA _{_ bryanlow, jmd _}_ @cs.cmu.edu, pkk@ece.cmu.edu 

## **Abstract** 

Recent research in robot exploration and mapping has focused on sampling environmental hotspot fields. This exploration task is formalized by Low, Dolan, and Khosla (2008) in a sequential decision-theoretic planning under uncertainty framework called MASP. The time complexity of solving MASP approximately depends on the map resolution, which limits its use in large-scale, high-resolution exploration and mapping. To alleviate this computational difficulty, this paper presents an information-theoretic approach to MASP ( _i_ MASP) for efficient adaptive path planning; by reformulating the cost-minimizing _i_ MASP as a rewardmaximizing problem, its time complexity becomes independent of map resolution and is less sensitive to increasing robot team size as demonstrated both theoretically and empirically. Using the reward-maximizing dual, we derive a novel adaptive variant of maximum entropy sampling, thus improving the induced exploration policy performance. It also allows us to establish theoretical bounds quantifying the performance advantage of optimal adaptive over non-adaptive policies and the performance quality of approximately optimal vs. optimal adaptive policies. We show analytically and empirically the superior performance of _i_ MASPbased policies for sampling the log-Gaussian process to that of policies for the widely-used Gaussian process in mapping the hotspot field. Lastly, we provide sufficient conditions that, when met, guarantee adaptivity has no 

## **Introduction** 

Recent research in multi-robot exploration and mapping (Low, Dolan, and Khosla 2008; Singh et al. 2007) has focused on sampling environmental fields, some of which typically feature a few small _hotspots_ in a large region (Webster and Oliver 2007). Such a _hotspot field_ often arises in environmental and ecological sensing applications such as precision agriculture, mineral prospecting, monitoring of ocean phenomena, forest ecosystems, pollution, or contamination. In particular, the hotspot field (e.g., plankton density and mineral distribution in Fig. 2) is characterized by _continuous, positively skewed, spatially correlated_ measurements with the hotspots exhibiting extreme measurements 

Copyright _⃝_ c 2018, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved. 

and much higher spatial variability than the rest of the field. With limited (e.g., point-based) robot sensing range, a complete coverage becomes impractical in terms of resource costs (e.g., energy consumption). So, to accurately map the field, the hotspots have to be sampled at a higher resolution. 

The hotspot field discourages static sensor placement (Guestrin, Krause, and Singh 2005) because a large number of sensors has to be positioned to detect and refine the sampling of hotspots. If these static sensors are not placed in any hotspot initially, they cannot reposition by themselves to locate one. In contrast, a robot team is capable of performing high-resolution hotspot sampling due to its mobility. Hence, it is desirable to build a mobile robot team that can actively explore to map a hotspot field. 

To learn a hotspot field map, the _exploration strategy_ of the robot team has to plan resource-constrained observation paths that minimize the map uncertainty of the hotspot field. To achieve this, the recent work of Low, Dolan, and Khosla (2008) has proposed such a strategy that plans nonmyopic adaptive paths to minimize the uncertainty of a spatial model of the hotspot field. In particular, both (a) modeling and (b) planning components are designed to fully exploit the environmental structure in order to yield a highquality map: (a) The hotspot field is assumed to be realized from a non-parametric probabilistic model called the log-Gaussian process, which can provide a formal measure of map uncertainty and more importantly, characterize the abovementioned hotspot field measurements well; (b) The exploration task is formalized in a sequential decisiontheoretic planning under uncertainty framework, which we call the _multi-robot adaptive sampling problem_ (MASP). So, MASP can be viewed as a sequential, non-myopic version of active learning. In contrast to finite-state Markov decision problems, MASP adopts a more complex but realistic continuous-state, _non-Markovian_ problem structure so that its induced exploration policy can be informed by the complete history of continuous, spatially correlated observations for selecting paths. It is unique in unifying formulations of exploration problems along the entire adaptivity (see Def. 2) spectrum, thus subsuming existing non-adaptive formulations and allowing the performance advantage of a more adaptive policy to be theoretically realized. Through MASP, it is demonstrated that a more adaptive strategy can exploit clustering phenomena in a hotspot field to produce 

lower map uncertainty. 

However, MASP is besieged by a serious computational drawback due to its measure of map uncertainty using the mean-squared error criterion. Consequently, the time complexity of solving MASP (approximately) depends on the map resolution, which limits its practical use in large-scale, high-resolution exploration and mapping. 

The principal contribution of this paper is to alleviate this computational difficulty through an information-theoretic approach to MASP ( _i_ MASP) for efficient adaptive path planning, which measures map uncertainty based on the entropy criterion instead. Unlike MASP, reformulating the cost-minimizing _i_ MASP as a reward-maximizing problem causes its time complexity of being solved approximately to be independent of the map resolution and less sensitive to larger robot team size as demonstrated both theoretically and empirically in this paper. Additional contributions stemming from this reward-maximizing formulation include: 

- transforming the commonly-used non-adaptive maximum entropy sampling problem (Shewry and Wynn 1987) into a novel adaptive variant, thus improving the performance of the induced exploration policy; 

- establishing theoretical bounds to quantify the performance advantage of optimal adaptive over non-adaptive exploration policies, and the performance quality of approximately optimal vs. optimal adaptive policies; 

- given an assumed environment model (e.g., occupancy grid map), establishing sufficient conditions that, when met, guarantee adaptivity provides no benefit; and 

- showing analytically and empirically the superior performance of _i_ MASP-based policies for sampling the logGaussian process ( _ℓ_ GP) to that of policies for the widelyused Gaussian process (GP) (Guestrin, Krause, and Singh 2005; Shewry and Wynn 1987; Singh et al. 2007) in mapping the hotspot field. 

**Related Work.** Beyond its computational gain, _i_ MASP retains the beneficial properties of MASP: it is novel in the class of model-based exploration strategies to perform both wide-area coverage and hotspot sampling. The former considers sparsely sampled areas to be of high uncertainty and thus spreads the observations evenly across the environmental field. The latter expects areas of high uncertainty to contain highly-varying measurements and hence produces clustered observations. Like MASP, _i_ MASP also covers the entire adaptivity spectrum, thus subsuming the existing nonadaptive entropy-based problem formulation (Shewry and Wynn 1987). In contrast, all other model-based strategies (Meliou et al. 2007; Singh et al. 2007) are non-adaptive and achieve only wide-area coverage; they are observed to perform well only with smoothly-varying fields. Similar to MASP, _i_ MASP can plan non-myopic multi-robot paths, which are more desirable than greedy or single-robot paths (Meliou et al. 2007; Singh et al. 2007). 

## **Cost-Minimizing Problem Formulations** 

We formalize here the information-theoretic exploration problems at the two extremes of the adaptivity spectrum. Exploration problems residing within the spectrum can be 

formalized in a similar manner. Note that the use of the entropy criterion in non-myopic active learning is not new but is limited to the non-adaptive problem formulation (Shewry and Wynn 1987), which is presented here as a comparison to the novel adaptive problem formulation. It can be observed that the resulting cost-minimizing formulations differ from that of MASP by only the entropy criterion. However, as we shall see in a later section, their reward-maximizing dual formulations are significantly different from that of MASP in terms of interpretation and computational complexity. 

**Notation and Preliminaries** . Let _X_ be the domain of the hotspot field corresponding to a finite set of grid cell locations. An observation taken (e.g., by a single robot) at stage _i_ comprises a pair of location _xi ∈X_ and its measurement _zxi_ . More generally, _k_ observations taken (e.g., by _k_ robots or 1 robot taking _k_ observations) at stage _i_ can be represented by a pair of vectors **x** _i_ of _k_ locations and **zx** _i_ of the corresponding measurements. 

**Definition 1 (Posterior Data)** _The posterior data di at stage i >_ 0 _comprises_ 

- _the prior data d_ 0 = _⟨_ **x** 0 _,_ **zx** 0 _⟩ available at stage_ 0 _, and_ 

- _a complete history of observations_ **x** 1 _,_ **zx** 1 _, . . . ,_ **x** _i,_ **zx** _i induced by k observations per stage over stages_ 1 _to i._ 

Let **x** 0: _i_ and **zx** 0: _i_ denote vectors comprising the location and measurement components of the posterior data _di_ (i.e., concatenations of **x** 0 _,_ **x** 1 _, . . . ,_ **x** _i_ and **zx** 0 _,_ **zx** 1 _, . . . ,_ **zx** _i_ ), respectively. Let **x** 0: _i_ denote the vector comprising locations of domain _X_ not observed in _di_ , and **zx** 0: _i_[be the vector compris-] ing the corresponding measurements. Let _Zxi_ , **Zx** _i_ , **Zx** 0: _i_ , ~~**Z**~~ **x** 0: _i_[be the random measurements corresponding to the re-] spective realizations _zxi_ , **zx** _i_ , **zx** 0: _i_ , **zx** 0: _i_[.] 

**Definition 2 (Characterizing Adaptivity)** _Suppose prior data d_ 0 _are available and n new locations are to be explored. Then, an exploration strategy is_ 

- **adaptive** _if its policy to select each vector_ **x** _i_ +1 _of k new locations depends only on the previously sampled data di for i_ = 0 _, . . . , n/k −_ 1 _. So, this strategy selects k observations per stage over n/k stages. If k_ = 1 _, this strategy is strictly adaptive. Increasing k makes it partially adaptive;_ 

- **non-adaptive** _if its policy to select each new location xi_ +1 _for i_ = 0 _, . . . , n −_ 1 _is independent of the measurements zx_ 1 _, . . . , zxn. As a result, all n new locations x_ 1 _, . . . , xn can be selected prior to exploration. That is, this strategy selects all n observations in a single stage._ 

**Objective Function** . The exploration objective is to plan observation paths that minimize the uncertainty of mapping the hotspot field. To achieve this, we use the entropy criterion to measure map uncertainty. Given the posterior data _dn_ , the _posterior map entropy_ of domain _X_ can be represented by the posterior joint entropy of the measurements ~~**Z**~~ **x** 0: _n_[at the unobserved locations] **x** 0: _n_ : 


![](1_survey/papers/md/Low2013InformationTheoretic_figs/Low2013InformationTheoretic.pdf-0002-20.png)


**Value Function** . If only the prior data _d_ 0 are available, an exploration strategy has to produce a policy for selecting observation paths that minimize the _expected_ posterior 

map entropy instead. This policy must then collect the optimal observations **x** 1 _,_ **zx** 1 _, . . . ,_ **x** _n,_ **zx** _n_ during exploration to form posterior data _dn_ . The value under an exploration policy _π_ is defined to be the expected posterior map entropy (i.e., expectation of (1)) when starting in _d_ 0 and following _π_ thereafter: 


![](1_survey/papers/md/Low2013InformationTheoretic_figs/Low2013InformationTheoretic.pdf-0003-01.png)


The strategies of Guestrin, Krause, and Singh (2005) and Singh et al. (2007) have optimized a closely related _mutual information_ criterion that measures the expected entropy reduction of unobserved locations **x** 0: _n_ by observing **x** 1: _n_ (i.e., H[ ~~**Z**~~ **x** 0: _n[|][d]_ 0[]] _[−]_[E] _[{]_[H][[] ~~**[Z]**~~ **x** 0: _n[|][d] n_[]] _[|][d]_ 0 _[}]_[).] This is deficient for the exploration objective because mutual information may be maximized by a choice of **x** 1: _n_ inducing a very large prior entropy H[ ~~**Z**~~ **x** 0: _n[|][d]_ 0[]][but][not][necessarily][the][smallest] expected posterior map entropy E _{_ H[ ~~**Z**~~ **x** 0: _n[|][d] n_[]] _[|][d]_ 0 _[}]_[.] 

In the next two subsections, we will describe how the adaptive and non-adaptive exploration policies can be derived to minimize the expected posterior map entropy (2). 

**Adaptive Exploration** . The adaptive policy _π_ for directing a team of _k_ robots is structured to collect _k_ observations per stage over a finite planning horizon of _n_ stages. This implies each robot observes 1 location per stage and is thus constrained to explore at most _n_ new locations over 

_△ n_ stages. Formally, _π_ = _⟨π_ 0( _d_ 0) _, . . . , πn−_ 1( _dn−_ 1) _⟩_ where _πi_ : _di →_ **a** _i_ maps data _di_ to a vector of robots’ actions **a** _i ∈A_ ( **x** _i_ ) at stage _i_ , and _A_ ( **x** _i_ ) is the joint action space of the robots given their current locations **x** _i_ . We assume the transition function _τ_ : **x** _i ×_ **a** _i →_ **x** _i_ +1 _deterministically_ moves the robots to their next locations **x** _i_ +1 at stage _i_ + 1. Combining _πi_ and _τ_ gives **x** _i_ +1 _← τ_ ( **x** _i, πi_ ( _di_ )). We can observe from this assignment that the sequential (i.e., stagewise) selection of _k_ new locations **x** _i_ +1 to be included in the observation paths depends only on the previously sampled data _di_ along the paths for stage _i_ = 0 _, . . . , n −_ 1. Hence, policy _π_ is adaptive (Def. 2). 

Solving the adaptive exploration problem _i_ MASP(1) means choosing the adaptive policy _π_ to minimize _V_ 0 _[π]_[(] _[d]_[0][)] (2), which we call the _optimal adaptive policy π_[1] . That is, _V_ 0 _[π]_[1][(] _[d]_[0][)][=][min] _[π][V]_ 0 _[π]_[(] _[d]_[0][)][.][Plugging] _[π]_[1][into][(2)][gives][the] _n_ -stage dynamic programming equations: 


![](1_survey/papers/md/Low2013InformationTheoretic_figs/Low2013InformationTheoretic.pdf-0003-07.png)


Note that the optimal action _π_ 0[1][(] _[d]_[0][)][at][stage][0][can][be][de-] termined prior to exploration using prior data _d_ 0. However, each action rule _πi_[1][(] _[d][i]_[)][ at stage] _[ i]_[ = 1] _[, . . . , n][ −]_[1][ defines the] optimal action to take in response to _di_ , part of which (i.e., **x** 1 _,_ **zx** 1 _, . . . ,_ **x** _i,_ **zx** _i_ ) are only observed during exploration. **Non-Adaptive Exploration** . The non-adaptive policy _π_ is structured to collect, in 1 stage, _n_ observations per robot with a team of _k_ robots. So, each robot is also constrained to explore at most _n_ new locations, but they have 

_△_ to do this within 1 stage. Formally, _π_ = _π_ 0( _d_ 0) where _π_ 0 : _d_ 0 _→_ **a** 0: _n−_ 1 maps prior data _d_ 0 to a vector **a** 0: _n−_ 1 of action components concatenating a sequence of robots’ actions **a** 0 _, . . . ,_ **a** _n−_ 1. Combining _π_ 0 and _τ_ gives **x** 1: _n ← τ_ ( **x** 0: _n−_ 1 _, π_ 0( _d_ 0)). We can observe from this assignment that the selection of _k × n_ new locations **x** 1 _, . . . ,_ **x** _n_ to form the observation paths are independent of the measurements **zx** 1 _, . . . ,_ **zx** _n_ obtained along the paths during exploration. Hence, policy _π_ is non-adaptive (Def. 2) and all new locations can be selected in a single stage prior to exploration. Solving the non-adaptive exploration problem _i_ MASP( _n_ ) involves choosing _π_ to minimize _V_ 0 _[π]_[(] _[d]_[0][)][(2),][which][we] call the _optimal non-adaptive policy π[n]_ (i.e., _V_ 0 _[π][n]_ ( _d_ 0) = min _π V_ 0 _[π]_[(] _[d]_[0][)][).][Plugging] _[ π][n]_[ into (2) gives the 1-stage equa-] tion: _V_ 0 _[π][n]_ ( _d_ 0) = _f_ ( **zx** 1: _n|d_ 0 _, π_ 0 _[n]_[)][ H][[] ~~**[Z]**~~ **x** 0: _n[|][d] n_[]][ d] **[z] x** 1: _n_ � = _f_ ( **z** _τ_ ( **x** 0: _n−_ 1 _,π_ 0 _[n]_[(] _[d]_[0][))] _[|][d]_[0][)][ H][[] ~~**[Z]**~~ **x** 0: _n[|][d] n_[]][ d] **[z]** _τ_ ( **x** 0: _n−_ 1 _,π_ 0 _[n]_[(] _[d]_[0][))] � = **a** min0: _n−_ 1� _f_ ( **z** _τ_ ( **x** 0: _n−_ 1 _,_ **a** 0: _n−_ 1) _|d_ 0) H[ ~~**Z**~~ **x** 0: _n[|][d] n_[]][ d] **[z]** _τ_ ( **x** 0: _n−_ 1 _,_ **a** 0: _n−_ 1) _[.]_ (4) The second equality follows from **x** 1: _n ← τ_ ( **x** 0: _n−_ 1 _, π_ 0 _[n]_[(] _[d]_[0][))][described][above.][Policy] _[π][n]_[=] _[π]_ 0 _[n]_[(] _[d]_[0][)] can therefore be determined in a single stage by _π_ 0 _[n]_[(] _[d]_[0][) =] arg min _f_ ( **z** _τ_ ( **x** 0: _n−_ 1 _,_ **a** 0: _n−_ 1) _|d_ 0) H[ ~~**Z**~~ **x** 0: _n[|][d] n_[]][ d] **[z]** _τ_ ( **x** 0: _n−_ 1 _,_ **a** 0: _n−_ 1) _[.]_ **a** 0: _n−_ 1 � 

Note that the optimal sequence of robots’ actions _π_ 0 _[n]_[(] _[d]_[0][)] (i.e., optimal observation paths) can be determined prior to exploration since the prior data _d_ 0 are available. 

## **Reward-Maximizing Dual Formulations** 

In this section, we transform the cost-minimizing _i_ MASP(1) (3) and _i_ MASP( _n_ ) (4) into reward-maximizing problems and show their equivalence. The reward-maximizing _i_ MASP( _n_ ) turns out to be the well-known _maximum entropy sampling_ (MES) problem (Shewry and Wynn 1987): 


![](1_survey/papers/md/Low2013InformationTheoretic_figs/Low2013InformationTheoretic.pdf-0003-13.png)


which is a single-staged problem of selecting _k×n_ new locations **x** 1 _, . . . ,_ **x** _n_ with maximum entropy to form the observation paths. This dual ensues from the equivalence result _V_ 0 _[π][n]_ ( _d_ 0) = H[ ~~**Z**~~ **x** 0 _[|][d]_ 0[]] _[ −][U]_ 0 _[ π][n]_[(] _[d]_[0][)][ relating cost-minimizing] and reward-maximizing _i_ MASP( _n_ )’s in the non-adaptive exploration setting, which follows from the chain rule of entropy. This result says the original objective of minimizing expected posterior map entropy (i.e., _V_ 0 _[π][n]_ ( _d_ 0) (4)) is equivalent to that of discharging from prior map entropy H[ ~~**Z**~~ **x** 0 _[|][d]_ 0[]] the largest entropy into the selected paths (i.e., _U_ 0 _[π][n]_[(] _[d]_[0][)][ (5)).] Hence, their optimal non-adaptive policies coincide. 

Our reward-maximizing _i_ MASP(1) is a novel adaptive variant of MES. Unlike the cost-minimizing _i_ MASP(1), it can be subject to convex analysis, which allows monotonebounding approximations to be developed as shown later. It comprises the following _n_ -stage dynamic programming equations: 


![](1_survey/papers/md/Low2013InformationTheoretic_figs/Low2013InformationTheoretic.pdf-0004-01.png)


for stage _i_ = 0 _, . . . , t −_ 1 where _t_ = _n −_ 1. Each stagewise reward reflects the entropy of _k_ new locations **x** _i_ +1 to be potentially selected into the paths. By maximizing the sum of expected rewards over _n_ stages in (6), the rewardmaximizing _i_ MASP(1) absorbs the largest expected entropy into the selected paths. In the adaptive exploration setting, the cost-minimizing and reward-maximizing _i_ MASP(1)’s are also equivalent (i.e., their optimal adaptive policies coincide): 

**Theorem 3** _Vi[π]_[1] ( _di_ ) = H[ ~~**Z**~~ **x** 0: _i[|][d] i_[]] _[−][U] i[ π]_[1][(] _[d][i]_[)] _[ for stage][ i]_[ =] 0 _, . . . , n −_ 1 _._ 

The work of Low, Dolan, and Khosla (2008) has also provided an equivalence result to relate the cost-minimizing and reward-maximizing MASPs through the use of the variance decomposition formula in its induction proof. In contrast, the induction proof to Theorem 3 uses the chain rule of entropy, which entails a computational complexity reduction (not available to MASP) as described next. 

In cost-minimizing _i_ MASP(1), the time complexity of evaluating the cost (i.e., posterior map entropy (1)) depends on the domain size _|X|_ for the environment models described in the next section. By transforming into the dual, the time complexity of evaluating each stagewise reward becomes independent of _|X|_ because it reflects only the uncertainty of the new locations to be potentially selected into the observation paths. As a result, the runtime of the approximation algorithm proposed in a later section does not depend on the map resolution, which is clearly advantageous in large-scale, high-resolution exploration and mapping. In contrast, the reward-maximizing MASP (Low, Dolan, and Khosla 2008) utilizing the mean-squared error criterion does not share this computational advantage, as the time needed to evaluate each stagewise reward still depends on _|X|_ . We will evaluate this computational advantage using time complexity analysis in a later section. 

## **Learning the Hotspot Field Map** 

Traditionally, a hotspot is defined as a location where its measurement exceeds a pre-defined extreme. But, hotspot locations do not usually occur in isolation but in clusters. So, it is useful to characterize hotspots with spatial properties. Accordingly, we define a hotspot field to vary as a realization of a spatial random field _{Yx >_ 0 _}x∈X_ such that putting together the observed measurements of a realization _{yx}x∈X_ gives a positively skewed 1D sample frequency distribution (e.g., Fig. 1b). In this section, we will highlight the problem with modeling the hotspot field directly using GP and explain how the _ℓ_ GP remedies this. We will also 

show analytically that the _i_ MASP-based policy for sampling _ℓ_ GP is adaptive and exploits clustering phenomena but that for sampling GP lacks these properties. 

**Gaussian Process** . A widely-used random field to model environmental phenomena is the GP (Guestrin, Krause, and Singh 2005; Meliou et al. 2007; Singh et al. 2007). The stationary assumption on the GP covariance structure is very sensitive to strong positive skewness of hotspot field measurements (e.g., Fig. 1b) and is easily violated by a few extreme ones (Webster and Oliver 2007). In practice, this can cause reconstructed fields to display large hotspots centered about a few extreme observations and prediction variances to be unrealistically small in hotspots, which are undesirable. So, if GP is used to model a hotspot field directly, it may not map well. To remedy this, a standard statistical practice is to take the log of the measurements (i.e., _Zx_ = log _Yx_ ) to remove skewness and extremity (e.g., Fig. 1c), and use GP to map the _log-measurements_ . As a result, the entropy criterion (1) has to be optimized in the transformed log-scale. 

We will apply _i_ MASP(1) to sampling GP and determine if _π_[1] exhibits adaptive and hotspot sampling properties. Let _{Zx}x∈X_ denote a GP, i.e., the joint distribution over any finite subset of _{Zx}x∈X_ is Gaussian (Rasmussen and Williams 2006). The GP can be completely specified by its 

_△ △_ mean _µZx_ = E[ _Zx_ ] and covariance _σZxZu_ = cov[ _Zx, Zu_ ] for _x, u ∈X_ . We adopt a common assumption that the GP is second-order stationary, i.e., it has a constant mean and a stationary covariance structure (i.e., _σZxZu_ is a function of _x − u_ for all _x, u ∈X_ ). In this paper, we assume that the mean and covariance structure of _Zx_ are known. Given _dn_ , the distribution of _Zx_ is Gaussian with posterior mean and covariance 

_µZx|dn_ = _µZx_ + Σ _x_ **x** 0: _n_ Σ _[−]_ **x** 0:[1] _n_ **x** 0: _n[{]_ **[z][x]** 0: _n[−]_ _**[µ]**_ **[Z] x** 0: _n[}][⊤]_[(7)] _σZxZu|dn_ = _σZxZu −_ Σ _x_ **x** 0: _n_ Σ _[−]_ **x** 0:[1] _n_ **x** 0: _n_[Σ] **[x]** 0: _n[u]_ (8) where, for every pair of locations _v, w_ of **x** 0: _n_ , _**µ**_ **Zx** 0: _n_ is a row vector with mean components _µZv_ , Σ _x_ **x** 0: _n_ is a row vector with covariance components _σZxZv_ , Σ **x** 0: _nu_ is a column vector with covariance components _σZvZu_ , and Σ **x** 0: _n_ **x** 0: _n_ is a covariance matrix with components _σZvZw_ . An important property of _σZxZu|dn_ is its independence of **zx** 1: _n_ . 

Policy _π_[1] can be reduced to be _non-adaptive_ : observe that each stagewise reward is independent of the measurements H[ **Z** _τ_ ( **x** _i,_ **a** _i_ ) _|di_ ] = log ~~�~~ (2 _πe_ ) _[k] |_ Σ **Z** _τ_ ( **x** _i,_ **a** _i_ ) _|di|_ (9) where Σ **Z** _τ_ ( **x** _i,_ **a** _i_ ) _|di_ is a covariance matrix with components _σZxZu|di_ , _x, u_ of _τ_ ( **x** _i,_ **a** _i_ ), that are independent of **zx** 1: _n_ . As a result, it follows from (6) that _Ui[π]_[1][(] _[d][i]_[)][and] _[π] i_[1][(] _[d][i]_[)][are][independent][of] **[z][x]** 1: _n_[for] _[i]_ = 0 _, . . . , n −_ 1. The expectations in _i_ MASP(1) (6) can then be integrated out. As a result, _i_ MASP(1) for sampling GP can be reduced to a 1-stage deterministic problem _U_ 0 _[π]_[1][(] _[d]_[0][)][=][�] _[n] i_ =0 _[−]_[1][max] **a** _i_[H][[] **[Z]** _[τ]_[(] **[x]** _[i][,]_ **[a]** _[i]_[)] _[|][d][i]_[]][=] **a** 0 _,...,_ max **a** _n−_ 1 _n−_ 1 � _i_ =0[H][[] **[Z]** _[τ]_[(] **[x]** _i[,]_ **[a]** _i_[)] _[|][d][i]_[]][=] **a**[max] 0: _n−_ 1[H][[] **[Z]** _[τ]_[(] **[x]**[0:] _[n][−]_[1] _[,]_ **[a]**[0:] _[n][−]_[1][)] _[|][d]_[0][]][=] _U_ 0 _[π][n]_[(] _[d]_[0][)][.][This][indicates][the][induced][optimal][values][from] solving _i_ MASP(1) and _i_ MASP( _n_ ) are equal. So, _π_[1] offers no performance advantage over _π[n]_ . 


![](1_survey/papers/md/Low2013InformationTheoretic_figs/Low2013InformationTheoretic.pdf-0005-00.png)


**----- Start of picture text -----**<br>
9 14 )<br>12<br>87 2 1086 (b) (' *+%<br>6 1.5 42 & *<br>5 00 0.5 1Measurement1.5 2 2.5 3 %<br>4 !% $<br>3 1 !"( (c) # !*+%<br>2 ' "<br>11 2 3 4 5 6 7 8 9 0.5 &% !! " # $ % & ' ( ) !!<br>Figure 1: Hotspot field simulation:(a) " !! !"#$)*+!,-./01-,-23" "#$(a)!  ℓ GP and (d) GP real-(d)<br>izations with their 1D sample frequency distributions shown,<br>respectively, in (b) and (c).<br>Sample frequency<br>4.,56-781-90-2:;<br>**----- End of picture text -----**<br>


Based on the above analysis, the following sufficient conditions, when met, guarantee that adaptivity has no benefit under an assumed environmental model: 

**Theorem 4** _If_ H[ **Z** _τ_ ( **x** _i,_ **a** _i_ ) _|di_ ] _is independent of_ **zx** 1: _n for stage i_ = 0 _, . . . , n −_ 1 _, iMASP(_ 1 _) and π_[1] _can be reduced to be single-staged and non-adaptive, respectively._ 

For example, Theorem 4 also holds for the simple case of an _occupancy grid map_ modeling an obstacle-ridden environment, which typically assumes _zx_ for _x ∈X_ to be independent. As a result, H[ **Z** _τ_ ( **x** _i,_ **a** _i_ ) _|di_ ] can be reduced to a sum of prior entropies over the unobserved locations _τ_ ( **x** _i,_ **a** _i_ ), which are independent of **zx** 1: _n_ . 

Policy _π_[1] performs _wide-area coverage_ only: to maximize stagewise rewards (9), _π_[1] selects new locations with large posterior variance for observation. If we assume isotropic covariance structure (i.e., the covariance _σZxZu_ decreases monotonically with _||x − u||_ ) (Rasmussen and Williams 2006), the posterior data _di_ provide the least amount of information on unobserved locations that are far away from all observed locations. As a result, the posterior variance of unobserved locations in sparsely sampled regions are still largely unreduced by the posterior data _di_ from the observed locations. Hence, by exploring the sparsely sampled areas, a large expected entropy can be absorbed into the selected observation paths. Using the observations selected from wide-area coverage, the field of _original_ measurements may not be mapped well because the under-sampled hotspots with extreme, highly-varying measurements contribute considerably to map entropy in the original scale, as discussed below. 

**Log-Gaussian Process** . To map the original, rather than the log-, measurements directly, it is a conventional practice in geostatistics to use the _ℓ_ GP. Consequently, the entropy criterion (1) is optimized in the original scale. To do this, let _{Yx}x∈X_ denote a _ℓ_ GP: if _Zx_ = log _Yx_ , _{Zx}x∈X_ is a GP. So, the positive-valued _Yx_ = exp _{Zx}_ denotes the original random measurement at location _x_ . It is straightforward to derive the predictive properties of _ℓ_ GP from that of GP as shown in (Low, Dolan, and Khosla 2008). 

A _ℓ_ GP can model a field with hotspots that exhibit much higher spatial variability than the rest of the field: Figs. 1a and 1d compare the realizations of _ℓ_ GP and GP; the GP realization results from taking the log of the _ℓ_ GP measurements. This does not just dampen the extreme measurements, but also dampens and amplifies the difference between extreme and small measurements respectively, thus removing the 

positive skew (compare Figs. 1b and 1c). Compared to the GP realization, the _ℓ_ GP one thus exhibits higher spatial variability within hotspots but lower variability in the rest of the field. This intuitively explains why wide-area coverage suffices for GP but hotspot sampling is further needed for _ℓ_ GP. 

Policy _π_[1] is _adaptive_ : observe that each stagewise reward depends on the previously sampled data _di_ : 

H[ **Y** _τ_ ( **x** _i,_ **a** _i_ ) _|di_ ] = log ~~�~~ (2 _πe_ ) _[k] |_ Σ **Z** _τ_ ( **x** _i,_ **a** _i_ ) _|di|_ + _**µ**_ **Z** _τ_ ( **x** _i,_ **a** _i_ ) _|di_ **1** _[⊤]_ (10) where _**µ**_ **Z** _τ_ ( **x** _i,_ **a** _i_ ) _|di_ is a mean vector with components _µZx|di_ for _x_ of _τ_ ( **x** _i,_ **a** _i_ ). Since _µZx|di_ depends on _di_ by (7), H[ **Y** _τ_ ( **x** _i,_ **a** _i_ ) _|di_ ] depends on _di_ . Consequently, it follows from (6) that _Ui[π]_[1][(] _[d][i]_[)][and] _[π] i_[1][(] _[d][i]_[)][depend][on] _[d][i]_[for] _[i]_[=] 0 _, . . . , n −_ 1. Hence, _π_[1] is _adaptive_ . 

Policy _π_[1] performs both _hotspot sampling_ and _wide-area coverage_ : to maximize stagewise rewards (10), _π_[1] selects new locations with large Gaussian posterior variance and mean for observation. So, it directs exploration towards sparsely sampled areas and hotspots. 

## **Value-Function Approximations** 

**Strictly Adaptive Exploration** . With a team of _k >_ 1 robots, _π_[1] collects _k >_ 1 observations per stage, thus becoming _partially adaptive_ . We will now derive the optimal _strictly adaptive_ policy (in particular, for sampling _ℓ_ GP), which, among policies of all adaptivity, selects paths with the largest expected entropy. By Def. 2, a strictly adaptive policy has to be structured to collect only 1 observation per stage. To achieve strict adaptivity, _i_ MASP(1) (6) can be revised as follows: (a) The space _A_ ( **x** _i_ ) of simultaneous joint actions is reduced to a constrained set _A[′]_ ( **x** _i_ ) of joint actions that allows one robot to move to observe a new location and the other robots stay put. This tradeoff for strict adaptivity allows _A[′]_ ( **x** _i_ ) to grow linearly, rather than exponentially, with the number of robots; (b) We constrain each robot to explore a path of at most _n_ new adjacent locations; this can be viewed as an energy consumption constraint on each robot. The horizon then spans _k × n_ , rather than _n_ , stages, which reflects the additional time of exploration incurred by strict adaptivity; (c) If **a** _i ∈A[′]_ ( **x** _i_ ), the assignment **x** _i_ +1 _← τ_ ( **x** _i,_ **a** _i_ ) moves one chosen robot to a new location _xi_ +1 while the other unselected robots stay put at their current locations. Then, only one component of **x** _i_ is changed to _xi_ +1 to form **x** _i_ +1; the other components of **x** _i_ +1 are unchanged from **x** _i_ . Hence, there is only one unobserved component _Yxi_ +1 in **Yx** _i_ +1; the other components of **Yx** _i_ +1 are already observed in the previous stages and can be found in _di_ . As a result, the probability distribution of **Yx** _i_ +1 can be simplified to a univariate _Yxi_ +1. 

These revisions of _i_ MASP(1) yield the strictly adaptive exploration problem called _i_ MASP( _k_[1][):] 


![](1_survey/papers/md/Low2013InformationTheoretic_figs/Low2013InformationTheoretic.pdf-0005-14.png)


adaptive policy) from the optimal value functions above. 

Since _Yxi_ +1 is continuous, it entails infinite state transitions. So, E[ _Ui_ +1( _di, xi_ +1 _, Yxi_ +1) _|di_ ] has to be evaluated in closed form for _i_ MASP( _k_[1][) to be solved exactly.][This can be] performed for _t_ = 1. When _t >_ 1, the expectation of the optimal value function results in an integral that is too complex to be evaluated. Hence, we will resort to approximating _i_ MASP( _k_[1][)][as][described][below.][For][ease][of][exposition,][we] will revert to using _Zxi_ +1 = log _Yxi_ +1 for _ℓ_ GP from now on. **Approximately Optimal Exploration** . To approximate _i_ MASP( _k_[1][),][we][will][first][approximate][the][expectation][in] (11) from below and above using the _ν_ -fold generalized Jensen and Edmundson-Madansky (EM) bounds respectively (Huang, Ziemba, and Ben-Tal 1977). To do this, we need the following convexity result for _i_ MASP( _k_[1][) (11):] 

**Lemma 5** _Ui_ ( _di_ ) _is convex in_ **zx** 0: _i for i_ = 0 _, . . . , t._ 

Let the support of _Zxi_ +1 given _di_ be _Zx[ν] i_ +1[that][is][parti-] tioned into _ν_ disjoint intervals _Zx_[[] _[j] i_[]] +1[=][[] _z_ ~~[[]~~ _x[j] i[−]_ +1[1]] _[,] z_ ~~[[]~~ _x[j] i_[]] +1[]][for] _j_ = 1 _, . . . , ν_ . Then, 


![](1_survey/papers/md/Low2013InformationTheoretic_figs/Low2013InformationTheoretic.pdf-0006-04.png)


The upper approximate problem _i_ MASP( _k_[1][)][can][be][con-] structed from _i_ MASP( _k_[1][)][(11)][by][replacing][the][expecta-] tion with the upper EM bound (12) to yield the optimal value functions _U_ ~~_ν_~~ _i_[(] _[d][i]_[)][for] _[i]_[=][0] _[, . . . , t]_[.] Similarly, the lower approximate problem _i_ MASP( _k_[1][)][can][be][constructed] from _i_ MASP( _k_[1][) (11) by replacing the expectation with the] lower Jensen bound (12) to yield the optimal value functions _U ν_ ~~_i_~~[(] _[d][i]_[)][ for] _[ i]_[ = 0] _[, . . . , t]_[ and optimal policy] _[π] k_ 1 . 

The next result uses the induced optimal values from solving the lower and upper approximate problems to monotonically bound the maximum expected entropy achieved by the 1 optimal strictly adaptive policy _π k_ : 

**Theorem 6** _If Zx[ν] i_[+1] +1 _[is][obtained][by][splitting][one][of][the] intervals in Zx[ν] i_ +1 _[,][U] ν_ ~~_i_~~[(] _[d][i]_[)] _[≤][U] ν_ ~~_i_~~ +1( _di_ ) _≤ Ui_ ( _di_ ) _≤_ ~~_ν_~~ +1 _ν U i_ ( _di_ ) _≤ U i_[(] _[d][i]_[)] _[ for][ i]_[ = 0] _[, . . . , t][.]_ A previous result of Low, Dolan, and Khosla (2008) has 1 guaranteed that _π k_ can achieve an expected entropy not worse than _U ν_ 0[(] _[d]_[0][)][.][But,][that][result][does][not][account][for] how much it differs from the maximum expected entropy 1 achieved by _π k_ . With the upper bound of Theorem 6, this error difference can be bounded: 

1 **Corollary 7** _π k is guaranteed to achieve an expected entropy that is not more than U ν_ 0[(] _[d]_[0][)] _[ −][U] ν_ ~~0~~[(] _[d]_[0][)] _[ from the max-]_ 1 _imum expected entropy U_ 0( _d_ 0) _achieved by π k ._ **Bounds on Performance Advantage of Adaptive Exploration** . A previous result of Low, Dolan, and Khosla (2008) has established the performance advantage of optimal adaptive over non-adaptive policies. Realizing the extent of such an advantage is important if adaptivity incurs a cost. In particular, we are interested in quantifying the performance 1 difference between the strictly adaptive _π k_ and the non1 adaptive _π[n]_ . This performance advantage of _π k_ over _π[n]_ is defined as the difference of their achieved maximum expected entropies _U_ 0( _d_ 0) _− U_ 0 _[π][n]_[(] _[d]_[0][)][.][Using the induced op-] timal values from solving the approximate problems (Theorem 6), the advantage _U_ 0( _d_ 0) _− U_ 0 _[π][n]_[(] _[d]_[0][)][ can be bounded] between _U ν_ 0[(] _[d]_[0][)] _[−][U]_ 0 _[ π][n]_[(] _[d]_[0][)][ and] _U_ ~~_ν_~~ 0[(] _[d]_[0][)] _[−][U]_ 0 _[ π][n]_[(] _[d]_[0][)][. A large] lower bound _U ν_ ~~0~~[(] _[d]_[0][)] _[−][U]_ 0 _[ π][n]_[(] _[d]_[0][)][implies] _[π] k_ 1 is to be preferred. A small upper bound _U ν_ 0[(] _[d]_[0][)] _[ −][U]_ 0 _[ π][n]_[(] _[d]_[0][)][ implies] _[ π][n]_ 1 performs close to that of _π k_ and should be preferred if it is 1 more costly to deploy _π k_ . For GP, this advantage is zero as 1 _π k_ can be reduced to be non-adaptive as shown previously. **Real-Time Dynamic Programming** . For our bounding approximation scheme, the state size grows exponentially with the number of stages. This is due to the nature of dynamic programming problems (e.g., _i_ MASP( _k_[1][)), which takes into] account all possible states. To alleviate this computational difficulty, we modify the anytime algorithm URTDP of Low, Dolan, and Khosla (2008) based on _i_ MASP( _k_[1][),][which][can] guarantee its policy performance in real time. It simulates greedy exploration paths through a large state space, resulting in desirable properties of focused search and good anytime behavior. The greedy exploration is guided by computationally efficient, informed initial heuristic bounds independent of state size. 

In URTDP (Algorithm 1), each simulated path involves an alternating selection of actions and their corresponding outcomes till the last stage. Each action is selected based on the upper bound (line 3). For each encountered state, the algorithm maintains both lower and upper bounds, which are used to derive the uncertainty of its corresponding optimal value function. It exploits them to guide future searches in an informed manner; it explores the next state/outcome with the greatest amount of uncertainty (lines 4-5). Then, the algorithm backtracks up the path to update the upper heuristic bounds using max **a** _i Qi_ ( **a** _i, di_ ) (line 11) where 


![](1_survey/papers/md/Low2013InformationTheoretic_figs/Low2013InformationTheoretic.pdf-0006-10.png)


We will show that the time complexity of SIMULATEDPATH( _d_ 0 _, t_ ) is independent of map resolution but the same 

procedure in (Low, Dolan, and Khosla 2008) is not. It is also less sensitive to increasing robot team size. Assuming no prior data and _|A[′]_ ( **x** _i_ ) _|_ = ∆, the time needed to evaluate the stagewise rewards H[ _Yxi_ +1 _|di_ ] for all ∆ new locations _xi_ +1 (i.e., using Cholesky factorization) is _O_ ( _t_[3] + ∆ _t_[2] ), which is independent of _|X|_ and results in _O_ ( _t_ ( _t_[3] + ∆( _t_[2] + _ν_ ))) time to run SIMULATED-PATH( _d_ 0 _, t_ ). In contrast, the time needed to evaluate the stagewise rewards in (Low, Dolan, and Khosla 2008) is _O_ ( _t_[3] +∆( _t_[2] + _|X|t_ )+ _|X|t_[2] ), which depends on _|X|_ and entails _O_ ( _t_ ( _t_[3] +∆( _t_[2] + _|X|t_ + _ν_ )+ _|X|t_[2] )) time to run the same procedure. When the joint action set size ∆ increases with larger robot team size, the time to run the procedure in (Low, Dolan, and Khosla 2008) increases faster than that of ours due to the gradient factor _|X|t_ involving large domain size. In the next section, we will report the time taken to run this procedure empirically. 

|URTDP(_d_0_, t_):|||||||
|---|---|---|---|---|---|---|
|**while**<br>_U_0(_d_0)_−U_<br>~~0~~(_d_0) _> α_**do**SIMULATED-PATH(_d_0_, t_)<br>SIMULATED-PATH(_d_0_, t_):|||||||
|1: _i ←_0<br>2: **while**_i < t_**do**<br>3:<br>**a**_∗_<br>_i ←_arg max**a**_i_<br>_Qi_(**a**_i, di_)|||||||
|4:<br>_∀j,_<br>Ξ_j_<br>_←_<br>_U_<br>~~_i_~~+1(_di, x∗_<br>_i_+1_,z_<br>[_j_]<br>~~_x_~~_∗_<br>_i_+1)_}_<br>5:<br>_z ←_sample from distribution at|_p_<br>[_j_]<br>~~_x_~~_∗_<br>_i_+1_{_<br>_U i_+1(_di, x∗_<br>_i_+1_,z_<br>[_j_]<br>~~_x_~~_∗_<br>_i_+1)<br>points _z_<br>[_j_]<br>_x∗_<br>_i_+1 of probabilityΞ_j/_�<br>_k_|||||_−_<br> Ξ_k_|
|6:<br>_di_+1 _←di, x∗_<br>_i_+1_, z_<br>7:<br>_i ←i_+ 1<br>8:<br>_U i_(_di_) _←_max**a**_i_ H[_Yxi_+1_|di_]_, _<br>9: **while**_i >_ 0**do**<br>10:<br>_i ←i −_1|_U_<br>~~_i_~~(_di_) _←_<br>_U i_(_di_)||||||
|11:<br>_U i_(_di_)_←_max**a**_i_<br>_Qi_(**a**_i, di_)<br>12:<br>_U_<br>~~_i_~~(_di_)_←_max**a**_i Q_<br>~~_i_~~(**a**_i, di_)|||||||



**Algorithm 1:** URTDP ( _α_ is user-specified bound). 

## **Experiments and Discussion** 

This section evaluates, empirically, the approximately opti1 mal strictly adaptive policy _π k_ on 2 real-world datasets exhibiting positive skew: (a) June 2006 plankton density data (Fig. 2a) of Chesapeake Bay bounded within lat. 38 _._ 481 _−_ 38 _._ 591N and lon. 76 _._ 487 _−_ 76 _._ 335W, and (b) potassium distribution data (Fig. 2d) of Broom’s Barn farm spanning 520m by 440m. Each region is discretized into a 14 _×_ 12 grid of sampling units. Each unit _x_ is, respectively, associated with (a) plankton density _yx_ (chl-a) in mg m _[−]_[3] , and (b) potassium level _yx_ (K) in mg l _[−]_[1] . Each region comprises, respectively, (a) _|X|_ = 148 and (b) _|X|_ = 156 such units. Using a team of 2 robots, each robot is tasked to explore 9 adjacent units in its path including its starting unit. If only 1 robot is used, it is placed, respectively, in (a) top and (b) bottom starting unit, and samples all 18 units. Each robot’s actions are restricted to move to the front, left, or right unit. We use the data of 20 randomly selected units to learn the hyperparameters (i.e., mean and covariance structure) of GP and _ℓ_ GP through maximum likelihood estimation (Rasmussen and Williams 2006). So, prior data _d_ 0 comprise the randomly selected and robot starting units. 

1 The performance of _π k_ is compared to the policies pro- 


![](1_survey/papers/md/Low2013InformationTheoretic_figs/Low2013InformationTheoretic.pdf-0007-06.png)


**----- Start of picture text -----**<br>
1 1<br>2 180 2 45<br>3 160 3 40<br>4 140 4 35<br>5 120 5 30<br>6 100 6 25<br>7 7<br>8 80 8 20<br>9 60 9 15<br>10 40 10 10<br>11 20 11 5<br>121 2 3 4 5 6 7 8 9 10 11 12 13 14 121 2 3 4 5 6 7 8 9 10 11 12 13 14 0<br>(a) (d)<br>2 2.22 2 2.22 2 0.550.5 2 0.550.5<br>4 1.81.6 4 1.81.6 4 0.450.4 4 0.450.4<br>6 1.41.2 6 1.41.2 6 0.350.3 6 0.350.3<br>8 10.8 8 10.8 8 0.250.2 8 0.250.2<br>10 0.60.4 10 0.60.4 10 0.150.1 10 0.150.1<br>0.2 0.2 0.05 0.05<br>12 2 4 6 (b)8 10 12 14 12 2 4 6 (c)8 10 12 14 12 2 4 6 (e)8 10 12 14 12 2 4 6 (f)8 10 12 14<br>**----- End of picture text -----**<br>


Figure 2: (a) chl-a field with prediction error maps for (b) strictly adaptive _π_ 1 _/k_ and (c) non-adaptive _πn_ : 20 units (white circles) are randomly selected as prior data. The robots start at locations marked by ‘ _×_ ’s. The black and gray robot paths are produced by _π_ 1 _/k_ and _πn_ respectively. (d-f) K field with error maps for _π_ 1 _/k_ and _πn_ . 

duced by four state-of-the-art exploration strategies: The _optimal non-adaptive policy π[n] for GP_ (Shewry and Wynn 1987) is produced by solving _i_ MASP( _n_ ) (5). Similar to Theorem 4, it can be shown to be equivalent to the strictly adap1 tive _π k_ for GP. Although _i_ MASP( _k_[1][)][and] _[i]_[MASP(] _[n]_[)][can] be solved exactly, their state size grows exponentially with the number of stages. To alleviate this computational difficulty, we use anytime heuristic search algorithms URTDP (Algorithm 1) and Learning Real-Time A _[∗]_ to, respectively, solve _i_ MASP( _k_[1][) and] _[ i]_[MASP(] _[n]_[) approximately.][The] _[ adap-] tive greedy policy for ℓGP_ repeatedly chooses a rewardmaximizing action (i.e., by repeatedly solving _i_ MASP( _k_[1][)] with _t_ = 0 in (11)) to form the paths. The _non-adaptive greedy policy for GP_ performs likewise but does it in the log-scale. In contrast to the above policies that optimize the entropy criterion (1), a non-adaptive greedy policy is proposed by Guestrin, Krause, and Singh (2005) to approximately maximize the mutual information (MI) criterion for GP; it repeatedly selects a new sampling location that maximizes the increase in MI. We call this the _MI-based policy_ . 

**Performance metrics** . Two metrics are used to evaluate the above policies: (a) _Posterior map entropy_ (ENT) H[ **Yx** 0: _t[|][d] t_[]][ of domain] _[ X]_[is the optimized criterion (1) mea-] suring the posterior joint entropy of the original measurements **Yx** 0: _t_[at the unobserved locations] **x** 0: _t_ where _t_ = 16 (17) for the case of 2 (1) robots. A smaller ENT implies lower map uncertainty; (b) _Mean-squared relative error_ (ERR) _|X|[−]_[1][ �] _x∈X[{]_[(] _[y][x][−][µ][Y] x[|][d] t_[)] _[/][µ]_[¯] _[}]_[2][ measures the poste-] rior map error from using the best unbiased predictor _µYx|dt_ (i.e., _ℓ_ GP posterior mean) (Low, Dolan, and Khosla 2008) of the measurement _yx_ to predict the hotspot field where _µ_ ¯ = _|X|[−]_[1][ �] _x∈X[y][x]_[.][Although this criterion is not the one] being optimized, it allows the use of ground truth measurements to evaluate if the field is being mapped accurately. A smaller ERR implies lower map prediction error. 

Table 1 shows the results of various policies with different 

Table 1: Performance comparison of information-theoretic policies for chl-a and K fields: 1R (2R) denotes 1 (2) robots. 

|Plankton density(chl-a) feld|Plankton density(chl-a) feld|ENT|ENT|ERR|ERR|
|---|---|---|---|---|---|
|Explorationpolicy|Model|1R|2R|1R|2R|
|Adaptive _π_<br>1_/k_<br>Adaptive greedy<br>Non-adaptive_πn_<br>Non-adaptive greedy<br>MI-based|_ℓ_GP<br>_ℓ_GP<br>GP<br>GP<br>GP|381.37<br>382.97<br>390.62<br>392.35<br>395.37|376.19<br>383.55<br>399.63<br>392.51<br>397.02|0.1827<br>0.2919<br>0.4145<br>0.2994<br>0.2764|0.2319<br>0.2579<br>0.3194<br>0.3356<br>0.2706|
|Potassium (K) feld||ENT||ERR||
|Explorationpolicy|Model|1R|2R|1R|2R|
|Adaptive _π_<br>1_/k_<br>Adaptive greedy<br>Non-adaptive_πn_<br>Non-adaptive greedy<br>MI-based|_ℓ_GP<br>_ℓ_GP<br>GP<br>GP<br>GP|47.330<br>61.080<br>67.084<br>58.704<br>59.058|48.287<br>56.181<br>59.318<br>64.186<br>67.390|0.0299<br>0.0457<br>0.0434<br>0.0431<br>0.0435|0.0213<br>0.0302<br>0.0358<br>0.0335<br>0.0343|



assumed models and robot team sizes for chl-a and K fields. For _i_ MASP( _k_[1][) and] _[ i]_[MASP(] _[n]_[),][the results are obtained us-] ing the policies provided by the anytime algorithms after running 120000 simulated paths. The differences in results between policies have been verified using _t_ -tests ( _α_ = 0 _._ 1) to be statistically significant. 

**Plankton density data** . The results show that the strictly 1 adaptive _π k_ achieves lowest ENT and ERR as compared 1 to the tested policies. From Fig. 2a, _π k_ moves the robots to sample the hotspots showing higher spatial variability whereas _π[n]_ moves them to sparsely sampled areas. Figs. 2b and 2c show, respectively, the prediction error maps result1 ing from _π k_ and _π[n]_ ; the prediction error at each location ¯ _x_ is measured using _|yx − µYx|dt|/µ_ . Locations with large errors are mostly concentrated in the left region where the field is highly-varying and contains higher measurements. 1 Compared to _π k_ , _π[n]_ incurs large errors at more locations in or close to hotspots, thus resulting in higher ERR. 

We also compare the time needed to run the first 10000 SIMULATED-PATH( _d_ 0 _, t_ )’s of our URTDP algorithm to that of Low, Dolan, and Khosla (2008), which are 115s and 10340s respectively for 2 robots (i.e., 90 _×_ faster). They, respectively, take 66s and 2835s for 1 robot (i.e., 43 _×_ faster). So, scaling to 2 robots incurs 1 _._ 73 _×_ and 3 _._ 65 _×_ more time 1 for the respective algorithms. Policy _π k_ can already achieve the performance reported in Table 1 for 2 robots, and ENT of 389 _._ 23 and ERR of 0 _._ 231 for 1 robot. In contrast, the policy of Low, Dolan, and Khosla (2008) only improves to ENT of 377 _._ 82 (391 _._ 85) and ERR of 0 _._ 233 (0 _._ 252) for 2 (1) robots, which are slightly worse off. 

**Potassium distribution data** . The results show again that 1 1 _π k_ achieves lowest ENT and ERR. From Fig. 2d, _π k_ again moves the robots to sample the hotspots showing higher spatial variability whereas _π[n]_ moves them to sparsely sampled 1 areas. Compared to _π k_ , _π[n]_ incurs large errors at a greater number of locations in or close to hotspots as shown in Figs. 2e and 2f, thus resulting in higher ERR. 

To run 10000 SIMULATED-PATH( _d_ 0 _, t_ )’s, our URTDP algorithm is 84 _×_ (48 _×_ ) faster than that of Low, Dolan, and Khosla (2008) for 2 (1) robots. Scaling to 2 robots incurs 1 _._ 93 _×_ and 3 _._ 37 _×_ more time for the respective algorithms. 

1 Policy _π k_ can already achieve the performance reported in Table 1 for 1 and 2 robots. In contrast, the policy of Low, Dolan, and Khosla (2008) achieves worse ENT of 67 _._ 132 (55 _._ 015) for 2 (1) robots. It achieves worse ERR of 0 _._ 032 for 2 robots but better ERR of 0 _._ 025 for 1 robot. 

**Summary of test results** . The above results show that the 1 strictly adaptive _π k_ can learn the highest-quality hotspot field map (i.e., lowest ENT and ERR) among the tested stateof-the-art strategies. After evaluating whether MASP- vs. _i_ MASP-based planners are time-efficient for real-time de1 ployment, we observe that _π k_ can achieve mapping performance comparable to the policy of Low, Dolan, and Khosla (2008) using significantly less time, and the incurred planning time is also less sensitive to larger robot team size. 1 Lastly, we see in Fig. 2 that the strictly adaptive _π k_ has exploited clustering phenomena (i.e., hotspots) to achieve lower ENT and ERR than that of the non-adaptive _π[n]_ . 

## **Conclusion** 

This paper describes an information-theoretic approach to efficient adaptive path planning for active exploration and mapping of hotspot fields. We have shown that, like MASP, _i_ MASP is capable of exploiting clustering phenomena to produce lower map uncertainty. In contrast to MASP, the time complexity of solving (reward-maximizing) _i_ MASP approximately is independent of map resolution and is also less sensitive to increasing robot team size as demonstrated theoretically and empirically. This is clearly advantageous in large-scale, high-resolution exploration and mapping. The proposed approximation techniques can be generalized to solve _i_ MASPs that utilize the full joint action space of the robot team, thus allowing the robots to move simultaneously at every stage and the mission time to be constrained. 

**Acknowledgments.** We would like to thank Dr R. Webster from Rothamsted Research for providing the Broom’s Barn Farm data. 

## **References** 

- [2005] Guestrin, C.; Krause, A.; and Singh, A. P. 2005. Nearoptimal sensor placements in Gaussian processes. In _Proc. ICML_ . 

- [1977] Huang, C. C.; Ziemba, W. T.; and Ben-Tal, A. 1977. Bounds on the expectation of a convex function of a random variable: With applications to stochastic programming. _Oper. Res._ 25:315–325. 

- [2008] Low, K. H.; Dolan, J. M.; and Khosla, P. 2008. Adaptive multi-robot wide-area exploration and mapping. In _Proc. AAMAS_ , 23–30. 

- [2007] Meliou, A.; Krause, A.; Guestrin, C.; Kaiser, W.; and Hellerstein, J. M. 2007. Nonmyopic informative path planning in spatio-temporal models. In _Proc. AAAI_ , 602–607. 

- [2006] Rasmussen, C. E., and Williams, C. K. I. 2006. _Gaussian Processes for Machine Learning_ . Cambridge, MA: MIT Press. 

- [1987] Shewry, M. C., and Wynn, H. P. 1987. Maximum entropy sampling. _J. Applied Stat._ 14(2):165–170. 

- [2007] Singh, A.; Krause, A.; Guestrin, C.; Kaiser, W.; and Batalin, M. 2007. Efficient planning of informative paths for multiple robots. In _Proc. IJCAI_ , 2204–2211. 

[2007] Webster, R., and Oliver, M. 2007. _Geostatistics for Environmental Scientists_ . John Wiley & Sons, 2nd edition. 

## **Proofs** 

## **Theorem 3** 

_Proof by induction_ on _i_ that _Vi[π]_[1] ( _di_ ) = H[ ~~**Z**~~ **x** 0: _i[|][d] i_[]] _[−] Ui[π]_[1][(] _[d][i]_[)][ for] _[ i]_[ =] _[ n][ −]_[1] _[, . . . ,]_[ 0][.] 

_Base case_ ( _i_ = _n −_ 1): 


![](1_survey/papers/md/Low2013InformationTheoretic_figs/Low2013InformationTheoretic.pdf-0009-05.png)


The first and second equalities follow from (3). The third equality is due to the chain rule for entropy (Cover and Thomas 1991). The last equality is due to (6). Hence, the base case is true. 

_Inductive case_ : Suppose that 


![](1_survey/papers/md/Low2013InformationTheoretic_figs/Low2013InformationTheoretic.pdf-0009-08.png)


is true. We have to prove that _Vi[π] −_[1] 1[(] _[d][i][−]_[1][)] = H[ ~~**Z**~~ **x** 0: _i−_ 1 _[|][d] i−_ 1[]] _[ −][U] i[ π] −_[1] 1[(] _[d][i][−]_[1][)][ is true.] 


![](1_survey/papers/md/Low2013InformationTheoretic_figs/Low2013InformationTheoretic.pdf-0009-10.png)


The first equality follows from (3). The second equality follows from (13). The third equality follows from linearity of expectation and the chain rule for entropy (Cover and Thomas 1991). The last equality is due to (6). Hence, the inductive case is true. 

It is clear from above that the induced optimal adaptive policies from solving the cost-minimizing and rewardmaximizing _i_ MASP(1)’s coincide. 

## **Equation 9** 

Since _f_ ( **Zx** _i_ +1 = **zx** _i_ +1 _|di_ ) = 


![](1_survey/papers/md/Low2013InformationTheoretic_figs/Low2013InformationTheoretic.pdf-0009-15.png)



![](1_survey/papers/md/Low2013InformationTheoretic_figs/Low2013InformationTheoretic.pdf-0009-16.png)


The fourth equality is due to the trace property tr( _AB_ ) = tr( _BA_ ). 

## **Equation 10** 

Using the Jacobian method of variable transformation, 


![](1_survey/papers/md/Low2013InformationTheoretic_figs/Low2013InformationTheoretic.pdf-0009-20.png)


where _X[′]_ = _{x | x_ is a location component in **x** _i_ +1 _}_ . So, 


![](1_survey/papers/md/Low2013InformationTheoretic_figs/Low2013InformationTheoretic.pdf-0009-22.png)


The fourth equality is due to the transformation _Zx_ = log _Yx_ and linearity of expectation. The fifth equality follows from (9). 

## **Lemma 5** 

We first show that H[ _Yxi_ +1 _|di_ ] is convex in **zx** 0: _i_ for _i_ = 0 _, . . . , t_ . From (10), we know that 


![](1_survey/papers/md/Low2013InformationTheoretic_figs/Low2013InformationTheoretic.pdf-0010-02.png)


From (7), the posterior mean _µZxi_ +1 _|di_ is an affine function of **zx** 0: _i_ . Hence, it is convex in **zx** 0: _i_ ((Boyd and Vandenberghe 2004), pp. 71). From (8), the posterior variance _σ_[2][independent][of] **[z][x]**[0:] _[i]_[.][So,][log] 2 _πeσ_[2] _Zxi_ +1 _|di_[is] ~~�~~ _Zxi_ +1 _|di_ is a constant term. Therefore, H[ _Yxi_ +1 _|di_ ] is convex in **zx** 0: _i_ . We will revert to using _Zxi_ +1 in _i_ MASP( _k_[1][) (11) for] _[ ℓ]_[GP] (i.e., by transforming _Zxi_ +1 = log _Yxi_ +1). 

_Proof by induction_ on _i_ that _Ui_ ( _di_ ) is convex in **zx** 0: _i_ for _i_ = _t, . . . ,_ 0. 

_Base case_ ( _i_ = _t_ ): As proven above, H[ _Yxt_ +1 _|dt_ ] is convex in **zx** 0: _t_ . Then, the pointwise maximum of H[ _Yxt_ +1 _|dt_ ] (i.e., max **a** _t∈A′_ ( **x** _t_ ) H[ _Yxt_ +1 _|dt_ ]) is convex in **zx** 0: _t_ ((Boyd and Vandenberghe 2004), pp. 81). Therefore, _Ut_ ( _dt_ ) is convex in **zx** 0: _t_ . The base case is true. 

_Inductive case_ : Suppose that _Ui_ +1( _di_ +1) is convex in **zx** 0: _i_ +1. We have to prove that _Ui_ ( _di_ ) is convex in **zx** 0: _i_ . 

From (11), the expectation under the normal variable _Zxi_ +1 with posterior mean _µZxi_ +1 _|di_ and variance _σZ_[2] _xi_ +1 _|di_ can be expressed in terms of the standard normal variable _Z_ = ( _Zxi_ +1 _− µZxi_ +1 _|di_ ) _/σZ_[2] _xi_ +1 _|di_[:] 


![](1_survey/papers/md/Low2013InformationTheoretic_figs/Low2013InformationTheoretic.pdf-0010-08.png)


Since _di_ and _µZxi_ +1 _|di_ + _σZ_[2] _xi_ +1 _|di[z]_[are][affine][in] **zx** 0: _i_ and _Ui_ +1( _di_ +1) is convex in **zx** 0: _i_ +1 by assumption, _Ui_ +1( _di, xi_ +1 _, µZxi_ +1 _|di_ + _σZ_[2] _xi_ +1 _|di[z]_[)][is][convex] in **zx** 0: _i_ because vector composition operation preserves convexity[1] ((Boyd and Vandenberghe 2004), pp. 86). Since _Ui_ +1( _di, xi_ +1 _, µZxi_ +1 _|di_ + _σZ_[2] _xi_ +1 _|di[z]_[)][is][convex] in **zx** 0: _i_ for each _z_ , _f_ ( _z_ ) _Ui_ +1( _di, xi_ +1 _, µZxi_ +1 _|di_ + � _σZ_[2] _xi_ +1 _|di[z]_[)][d] _[z]_[is][convex][in] **[z][x]** 0: _i_[because][integration][pre-] serves convexity ((Boyd and Vandenberghe 2004), pp. 79). So, _f_ ( _zxi_ +1 _|di_ ) _Ui_ +1( _di, xi_ +1 _, zxi_ +1) d _zxi_ +1 is � convex in **zx** 0: _i_ . From above, H[ _Yxi_ +1 _|di_ ] is convex in **zx** 0: _i_ . Then, the pointwise maximum of H[ _Yxi_ +1 _|di_ ] + _f_ ( _zxi_ +1 _|di_ ) _Ui_ +1( _di, xi_ +1 _, zxi_ +1) d _zxi_ +1 is convex in � **zx** 0: _i_ . Therefore, _Ui_ ( _di_ ) is convex in **zx** 0: _i_ . The inductive case is true. 

> 1Note that _Ui_ +1( _di_ +1) does not have to be non-decreasing in each argument because _di_ and _µZxi_ +1 _|di_ + _σZ_[2] _xi_ +1 _|di[z]_[are affine] in **zx** 0: _i_ . 

## **Theorem 6** 

_Proof by induction_ on _i_ that _U νi_[(] _[d][i]_[)] _[≤][U] νi_ +1( _di_ ) _≤ Ui_ ( _di_ ) for _i_ = _t, . . . ,_ 0. 

_Base case_ ( _i_ = _t_ ): _U ν_ ~~_t_~~[(] _[d][t]_[)][=] _[U] ν_ ~~_t_~~ +1( _dt_ ) = _Ut_ ( _dt_ ) = max[Hence, the base case is true.] **a** _t∈A[′]_ ( **x** _t_ )[H][[] _[Y][x][t]_[+1] _[|][d][t]_[]][.] _ν ν_ +1 _Inductive case_ : Suppose that _U_ ~~_i_~~ +1[(] _[d][i]_[+1][)] _[ ≤][U]_ ~~_i_~~ +1[(] _[d][i]_[+1][)] _[ ≤] Ui_ +1( _di_ +1) is true. We have to prove that _U ν_ ~~_i_~~[(] _[d][i]_[)] _[≤] U ν_ ~~_i_~~ +1( _di_ ) _≤ Ui_ ( _di_ ) is true. We will first show that _U ν_ ~~_i_~~ +1( _di_ ) _≤ Ui_ ( _di_ ). _U νi_ +1( _di_ ) 


![](1_survey/papers/md/Low2013InformationTheoretic_figs/Low2013InformationTheoretic.pdf-0010-14.png)


The first inequality follows from assumption (i.e., _ν_ +1 [ _j_ ] [ _j_ ] _U_ ~~_i_~~ +1[(] _[d][i][, x][i]_[+1] _[,][ z] xi_ +1[)] _≤ Ui_ +1( _di, xi_ +1 _, zxi_ +1[)][).] The second inequality follows from Lemma 5 that _Ui_ +1( _di, xi_ +1 _, zxi_ +1) is convex in _zxi_ +1 for _ℓ_ GP, and the generalized Jensen bound (12). 


![](1_survey/papers/md/Low2013InformationTheoretic_figs/Low2013InformationTheoretic.pdf-0010-16.png)



![](1_survey/papers/md/Low2013InformationTheoretic_figs/Low2013InformationTheoretic.pdf-0010-17.png)


The first inequality follows from assumption (i.e., _ν_ [ _j_ ] _ν_ +1 [ _j_ ] _U_ ~~_i_~~ +1[(] _[d][i][, x][i]_[+1] _[,][ z] xi_ +1[)] _≤ U_ ~~_i_~~ +1[(] _[d][i][, x][i]_[+1] _[,][ z] xi_ +1[)][).] We need the result that _U ν_ ~~_i_~~ +1( _di_ ) is convex in **zx** 0: _i_ for _i_ = 0 _, . . . , t_ for the second inequality to hold. The proof[2] is similar to that of Lemma 5. Consequently, since _U ν_ ~~_i_~~ +1+1[(] _[d][i][, x][i]_[+1] _[, z][x] i_ +1[)][is][convex][in] _[z][x] i_ +1[and] _[Z] x[ν] i_[+1] +1[is] obtained by splitting one of the intervals in _Zx[ν] i_ +1[,][the] second inequality results. The inductive case is thus true. 

_ν_ +1 ~~_ν_~~ The proof of _Ui_ ( _di_ ) _≤ U i_ ( _di_ ) _≤ U i_[(] _[d][i]_[)][for] _[i]_[=] _t, . . . ,_ 0 is similar to the above except that the inequalities are reversed. 

## **References for Proofs** 

Boyd, S., and Vandenberghe L. 2004. _Convex Optimization_ . Cambridge Univ. Press. 

> 2The approximate problems _i_ MASP( _k_[1][)][and] _i_ MASP( _k_[1][)][differ] from _i_ MASP( _k_[1][)][(11)][by][the][non-negative][weighted][sum][(instead] of the expectation), which also preserves convexity. 

Cover T., and Thomas J. 1991. _Elements of Information Theory_ . John Wiley & Sons. 

