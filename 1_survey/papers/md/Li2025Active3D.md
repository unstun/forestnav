---
citation_key: Li2025Active3D
arxiv_id: 2511.20050
arxiv_url: "https://arxiv.org/abs/2511.20050"
title: "Active3D: Active High-Fidelity 3D Reconstruction via Hierarchical Uncertainty Quantification"
authors_short: "Yan Li et al."
year: 2025
direction_tag: L_learning_path_optimization
source: pymupdf4llm
converted_at: 2026-06-23T18:55:09Z
origin: ai+web
reviewed: false
---

# **Active3D: Active High-Fidelity 3D Reconstruction via Hierarchical Uncertainty Quantification** 

## **Yan Li**[1] **, Yingzhao Li**[2] **, Gim Hee Lee**[1] 

1National University of Singapore 2Harbin Institute of Technology 

## **Abstract** 

In this paper, we present an active exploration framework for high-fidelity 3D reconstruction that incrementally builds a multi-level uncertainty space and selects next-best-views through an uncertainty-driven motion planner. We introduce a _hybrid implicit–explicit representation_ that fuses neural fields with Gaussian primitives to jointly capture global structural priors and locally observed details. Based on this hybrid state, we derive a _hierarchical uncertainty volume_ that quantifies both implicit global structure quality and explicit local surface confidence. To focus optimization on the most informative regions, we propose an _uncertainty-driven keyframe selection_ strategy that anchors high-entropy viewpoints as sparse attention nodes, coupled with a _viewpoint-space sliding window_ for uncertainty-aware local refinement. The planning module formulates next-best-view selection as an _Expected Hybrid Information Gain_ problem and incorporates a risk-sensitive path planner to ensure efficient and safe exploration. Extensive experiments on challenging benchmarks demonstrate that our approach consistently achieves state-ofthe-art accuracy, completeness, and rendering quality, highlighting its effectiveness for real-world active reconstruction and robotic perception tasks. 

**Website** — https://yanyan-li.github.io/project/vlx/active3d 

## **1 Introduction** 

Visual-based 3D reconstruction (Newcombe et al. 2011; Whelan et al. 2015; Dai et al. 2017; Li et al. 2020) aims to infer the geometry and appearance of previously unseen scenes from 2D imagery, making it a fundamental problem in both computer vision and robotics. Depending on how the sensor moves, reconstruction methods can be clustered into two categories: passive and active. Passive systems process streams of RGB (Schonberger and Frahm 2016) or RGB-D (Li and Tombari 2022) frames to jointly estimate six-degree-of-freedom (6-DoF) camera motions and fuse the measurements into sparse or dense 3D models, under the assumption of a fixed, user-driven path. In contrast, active reconstruction frameworks (Aloimonos, Weiss, and Bandyopadhyay 1988; Chen, Li, and Kwok 2011) integrate 

Copyright © 2026, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved. 


![](1_survey/papers/md/Li2025Active3D_figs/Li2025Active3D.pdf-0001-10.png)


**----- Start of picture text -----**<br>
100 Mesh Gaussian Map Depth<br>NARUTO OURS<br>ANM-SANM ActiveSplatActiveGamber<br>90 CO-SLAM<br>LoopSplat<br>NICE-SLAM<br>80TSDF-Fusion<br>MonoGS<br>SplaTAM<br>0 10 20 30<br>PSNR<br>C.R.(%)<br>**----- End of picture text -----**<br>


Figure 1: Performance on the Replica dataset. Left: Comparison of rendering quality (PSNR) versus reconstruction completeness (C.R.) across state-of-the-art methods. Right: Qualitative outputs of our method including reconstructed mesh, Gaussian map, and estimated depth. 

next-best-view (NBV) planning (Peralta et al. 2020) to autonomously select subsequent viewpoints to maximize information gain (Isler et al. 2016; Kirsch, Van Amersfoort, and Gal 2019) and ensure comprehensive surface coverage. In addition to accurate geometry, next-generation intelligent robots demand dense 3D models with _high fidelity_ and photometric consistency for downstream tasks. 

The conventional active reconstruction problem (Isler et al. 2016; Huang et al. 2018) is typically cast as an exploration task: select the sequence of viewpoints that will most effectively reveal detailed scene geometry and appearance. Early approaches leverage occupancy-grid (Elfes 2013) or voxel-based (Wu et al. 2014) maps and frontierdriven exploration to push the boundary between known and unknown space, ensuring that new measurements continually reduce map uncertainty (Lee et al. 2022). However, since these approaches focus solely on geometric uncertainty, the resulting reconstructions are ill-suited for highquality novel-view rendering and often lack the photometrically consistent details required for downstream tasks. Recent advances in scene representation have revealed two complementary paradigms: _implicit neural fields_ (Mildenhall et al. 2021; Barron et al. 2022) and _explicit parameterizations_ such as 3D Gaussian Splatting (Kerbl et al. 2023; Li et al. 2024), both achieving impressive performance in novel-view synthesis and surface reconstruction. Implicit models encode continuous neural fields that excel at capturing global structure, while explicit Gaussians faithfully 

preserve observed geometry and fine details. However, existing active frameworks typically adopt only one of these paradigms. Implicit-based active methods (Yan, Yang, and Zha 2023; Kuang et al. 2024) leverage neural priors for view planning, but their continuous fields tend to hallucinate missing surfaces (e.g., transparent or mirrored areas), leading to persistent high uncertainty and planner oscillation. Conversely, GS-based active approaches (Li et al. 2025; Jin et al. 2025) directly reflect observations into the map, providing reliable local geometry but lacking the ability to reason about occluded or unseen regions, resulting in suboptimal exploration coverage. 

These complementary strengths and limitations motivate a hybrid implicit–explicit formulation for active reconstruction, unifying global priors and local textured surface within a single information-theoretic planning framework. First, given a posed RGB-D stream, Active3D constructs a **hybrid implicit–explicit scene state** and derives a **hierarchical uncertainty map** to jointly quantify global structural entropy and local surface uncertainty. Based on this hybrid uncertainty, the planner is further proposed to formulate _next-best-view selection_ as an Expected Hybrid Information Gain ( **EHIG** ) optimization and executes viewpointaware trajectory planning. Keyframes are promoted via a dual-uncertainty intersection criterion, selecting viewpoints that observe regions where both implicit and explicit uncertainties are high. This establishes a sparse attention mechanism over the hybrid scene state. A viewpoint-space sliding window then performs uncertainty-aware local refinement of Gaussian primitives with respect to implicit priors, maintaining global–local consistency throughout the reconstruction process. Our contributions are summarized as follows: 

- We propose a _hybrid implicit–explicit scene representation_ for active 3D reconstruction, unifying neural fields and Gaussian primitives into a joint entropy minimization framework and introducing the _Hybrid Scene State Entropy_ . 

- We design a _hierarchical uncertainty map_ that fuses global implicit variance, local depth residuals, local photometric residuals, and temporal SDF changes via Bayesian fusion, providing a principled multi-scale signal to drive exploration and refinement. 

- We formulate next-best-view planning as an _Expected Hybrid Information Gain (EHIG)_ problem, combining global structural exploration and local detail preservation with risk-aware path optimization. 

- We introduce a viewpoint-aware keyframe selection strategy driven by the intersection of implicit and explicit uncertainties, anchoring high-information regions as sparse attention nodes in the hybrid map. Integrated with a spatial (non-temporal) sliding window, this enables uncertaintyaware local refinement and consistent reconstruction of the hybrid scene state. 

## **2 Related Work** 

**Neural Implicit and Explicit Representation.** Traditionally, 3D reconstructed models have been represented us- 

ing various geometric formats, including meshes (Kazhdan, Bolitho, and Hoppe 2006; Li et al. 2021), surfels (Whelan et al. 2015; St¨uckler and Behnke 2014), and truncated signed distance fields (TSDF) (Osher, Fedkiw, and Piechor 2004; Izadi et al. 2011). With the advent of differentiable radiance fields, these representations have been significantly extended to support high-quality novel view synthesis. In particular, NeRF (Mildenhall et al. 2021) have emerged as a powerful paradigm for photorealistic rendering and scene understanding. Specifically, iMAP (Sucar et al. 2021) utilizes MLP as the only scene representation for both tracking and mapping. To address the over smoothed reconstruction problem of only-MLP representation in large-scale environments, NeuralRecon (Sun et al. 2021) integrates neural TSDF volumes with learned features to enhance 3D reconstruction quality in indoor scenes. Similarly, ConvONet (Peng et al. 2020) predicts occupancy probabilities in 3D space using 3D convolutional architectures (C¸ ic¸ek et al. 2016; Ronneberger, Fischer, and Brox 2015; Niemeyer et al. 2020), combining the strengths of spatially aware feature encoding and implicit shape modeling. 

In contrast to implicit and hybrid approaches, explicit representations directly encode scene geometry and appearance in structured forms such as voxel grids (M¨uller et al. 2022) or Gaussian primitives (Kerbl et al. 2023), enabling efficient rendering and fast optimization. Plenoxels (FridovichKeil et al. 2022) replace MLPs with a sparse voxel grid that stores density and spherical harmonics coefficients. TensoRF (Chen et al. 2022) further improves scalability and memory efficiency by applying low-rank tensor decomposition. More recently, 3D Gaussian Splatting (Kerbl et al. 2023; Li et al. 2024) introduces a point-based explicit method where each Gaussian encodes position, orientation, scale, and radiance attributes, supporting high-fidelity rendering with real-time performance and continuous surfaces. 

**Active High-quality 3D Modeling.** Active reconstruction methods (Yan, Yang, and Zha 2023; Kuang et al. 2024; Pan et al. 2022; Li et al. 2025; Jin et al. 2024; Feng et al. 2024; Chen et al. 2025) autonomously select viewpoints during iterative mapping to maximize coverage and reconstruction quality. NeRF-based NBV strategies (Lee et al. 2022; Pan et al. 2022) use pixel-wise rendering variance as uncertainty cues, while FisherRF (Jiang, Lei, and Daniilidis 2024) introduces Fisher information for view planning. ANM (Yan, Yang, and Zha 2023) maintains weight-space uncertainty in a continually learned neural field, and NARUTO (Feng et al. 2024) extends this paradigm to 6-DoF exploration in largescale scenes. 

Recently, Gaussian primitives have been adopted for active scene modeling. ActiveGAMER (Chen et al. 2025) incorporates rendering quality into the information gain metric. GS-Planner (Jin et al. 2024) detects unobserved regions in the Gaussian map and employs a sampling-based NBV policy. HGS (Xu et al. 2024) proposes an adaptive hierarchical planning strategy balancing global and local refinement. ActiveSplat (Li et al. 2025) extends Gaussian-based SLAM to active mapping with decoupled viewpoint orientation. 

Uncertainty estimation plays a central role in NBV selec- 

tion. NeRF-based methods typically derive voxel or pixelwise variance from density fields (Pan et al. 2022; Lee et al. 2022), while Gaussian-based methods rely on observation completeness or visibility priors (Jin et al. 2024; Li et al. 2025). In contrast, we fuse _global implicit variance_ , _local surface residuals_ , and _temporal SDF variation_ , constructing a hierarchical uncertainty map that simultaneously guides global exploration and local refinement. 

**Hybrid State Quantification.** At state _k_ , the key objective is to quantify the **current scene knowledge** and guide the next-best-view selection. This hybrid formulation bridges _global structural exploration_ driven by _Fθ_ and _local highfidelity surface_ enabled by _Gk_ . Casting NBV planning as an _expected hybrid information gain_ optimization, we formalize active reconstruction in a probabilistic informationtheoretic context. 

We define the voxel-wise hybrid entropy as: 

## **3 Methodology** 

In the active reconstruction task, the core of the problem is to decide the position and orientation of the _i[th]_ viewpoint based on the information captured by the previous posed RGB-D stream _Si−_ 1 = _{_ **S** _k},_ **S** _k_ = [ _Ik, Dk,_ **T** _ck,w,_ **K** ] _, k ∈_ [0 _,_ 1 _, . . . , i −_ 1]. Therefore, the problem can be defined as determining how to leverage the previously posed RGB-D stream to guide the selection of the current viewpoint in order to achieve high-quality reconstruction. This process first involves the data organization of the previous RGB-D stream, followed by quantifying the historical information to evaluate the current reconstruction state and predicting potential information gain. By modeling the scene coverage, uncertainty distribution, and geometric consistency from _Si−_ 1, the system can actively plan the next viewpoint that maximizes scene completeness and reconstruction fidelity. Fig. 2 depicts the algorithm’s workflow. 

## **Hybrid Implicit-explicit Space** 

To simultaneously capture continuous global priors and high-quality local surface, we construct a **hybrid implicit–explicit space** that integrates implicit neural fields with explicit Gaussian primitives. Given a posed RGB-D observation **S** _k_ = [ _Ik, Dk,_ **T** _ck,w,_ **K** ], this hybrid space provides a unified state representation for incremental active reconstruction. 

**Definition of Hybrid Scene State.** We introduce a state formulation for the incremental active reconstruction task, where the state _Mk_ at step _k_ is designed to represent the currently reconstructed portion of the scene: 


![](1_survey/papers/md/Li2025Active3D_figs/Li2025Active3D.pdf-0003-08.png)


where _Fθ_ : R[3] _→_ SDF is the implicit neural field, and _Gk_ = _{Gi}[N] i_ =1 _[k]_[is the set of 3D Gaussian primitives. Each primitive] _Gi_ is parameterized as _Gi_ = ( _µi,_ Σ _i, αi, ci_ ), where _µi ∈_ R[3] is the mean position, Σ _i ∈_ R[3] _[×]_[3] the covariance, _αi ∈_ [0 _,_ 1] the opacity, and _ci ∈_ R[3] the color vector. And for the implicit neural field, we employ a One-blob encoder (Wang, Wang, and Agapito 2023; M¨uller et al. 2019) to extract deep features from input point clouds. The implicit representation subsequently maps world coordinates **x** _∈_ R[3] to SDF values and color attributes via the MLP: 


![](1_survey/papers/md/Li2025Active3D_figs/Li2025Active3D.pdf-0003-10.png)


where _γ_ ( **x** ) denotes tri-plane decomposition of spatial coordinates, and _Vα_ ( **x** ) represents position feature vectors obtained through volumetric trilinear interpolation. The function _fτ_ ( _·_ ) corresponds to the geometry decoder. 

_H_ hybrid( _v_ ) = _λ_ imp _H_ [ _pFθ_ ( _v_ )] + _λ_ exp _H_ [ _pGk_ ( _v_ )] _,_ (3) where _H_ [ _p_ ] denotes Shannon entropy and _λ_ imp _, λ_ exp balance global priors and local observations. 

The NBV reward for **c** is accumulated over all visible voxels: 


![](1_survey/papers/md/Li2025Active3D_figs/Li2025Active3D.pdf-0003-14.png)


where _V_ **c** is the set of voxels visible from **c** , and _O_ ( _v_ ) is the occupancy probability used to discount free-space ambiguity. 

## **Hierarchical Uncertainty Map Construction** 

To drive the hybrid NBV objective in Eq. 3, we construct a hierarchical uncertainty volume _Vu ∈_ R _[L][×][W][ ×][H]_ that fuses **global implicit priors** , **local view-dependent surface** , and **temporal consistency cues** . Each voxel _v_ stores a scalar _u_ ( _v_ ) _∈_ R[+] representing the hybrid reconstruction confidence. 

**Global Structure Uncertainty.** The implicit branch _Fθ_ encodes a continuous SDF-based representation that provides _global structural entropy_ . We approximate per-voxel variance using an uncertainty head _fδ_ ( _·_ ): 


![](1_survey/papers/md/Li2025Active3D_figs/Li2025Active3D.pdf-0003-19.png)


where **x** _v_ denotes the voxel center, _γ_ ( _·_ ) is the tri-plane encoder, and _ϕ_ ( _·_ ) applies a softplus normalization. Upon receiving new observations, the structural uncertainty is updated, encouraging coverage-driven exploration and mitigating local greedy behavior during the early stages of mapping. 

**View-dependent Local Uncertainty.** The explicit Gaussian map _Gk_ provides _local observation entropy_ through photometric and geometric residuals. At each step, we select top- _K_ high-uncertainty candidate viewpoints _C_ high and compute depth and color errors: 


![](1_survey/papers/md/Li2025Active3D_figs/Li2025Active3D.pdf-0003-22.png)


where _Mt_ masks valid pixels. The 2D errors are backprojected into the 3D voxel space to estimate the uncertainty of the local surface using the following formulation: 


![](1_survey/papers/md/Li2025Active3D_figs/Li2025Active3D.pdf-0003-24.png)


where _P_ ( _·_ ) denotes voxel-wise backprojection with bilinear interpolation. 


![](1_survey/papers/md/Li2025Active3D_figs/Li2025Active3D.pdf-0004-00.png)


Figure 2: Our method processes the RGB-D stream through dual explicit and implicit reconstruction branches. The explicit branch projects data into a 3D Gaussian model, while the implicit branch employs an encoder-decoder architecture to regress RGB values and SDF. Subsequently, the discrepancy between the rendered RGB-D and the GT RGB-D is computed. Another mlp predicts global uncertainty, while temporal variations on the SDF surface are characterized to derive uncertainty for the hybrid explicit-implicit representation. This representation then drives NBV selection and path planning. Finally, keyframes are selected within a sliding window for joint optimization of the explicit and implicit maps. 

**Temporal Variation Uncertainty.** To detect emerging surfaces and inconsistencies, we evaluate SDF changes between consecutive keyframes: ∆ _St_ = _St − St−_ 1. According to the varying states of surfaces, define masks for new surfaces, geometry changes, and novel free space: 


![](1_survey/papers/md/Li2025Active3D_figs/Li2025Active3D.pdf-0004-03.png)


The temporal uncertainty term is: 


![](1_survey/papers/md/Li2025Active3D_figs/Li2025Active3D.pdf-0004-05.png)



![](1_survey/papers/md/Li2025Active3D_figs/Li2025Active3D.pdf-0004-06.png)


Then, the final hierarchical uncertainty is fused as: 


![](1_survey/papers/md/Li2025Active3D_figs/Li2025Active3D.pdf-0004-08.png)


where _αi_ are weights estimated via evidence maximization, interpreted as a fusion of global priors, local observations, and temporal consistency. This **hierarchical map** directly links to the NBV reward in Eq. 4, providing a multi-scale uncertainty signal that balances exploration coverage and model fidelity. 

## **Next-Best-View Searching** 

With the hybrid scene state _Mk_ = _{Fθ, Gk}_ and hierarchical uncertainty map _u_ final( _v_ ) defined in Eq. 11, the goal of active planning is to select the next viewpoint **c** _i_ that maximizes the expected _hybrid information gain_ . 

**EHIG Objective.** Based on the final hierarchical uncertainty, we cast NBV selection as: 


![](1_survey/papers/md/Li2025Active3D_figs/Li2025Active3D.pdf-0004-13.png)


where _C_ is the candidate viewpoint set, and ∆ _I_ hybrid measures the reduction of hybrid entropy: 


![](1_survey/papers/md/Li2025Active3D_figs/Li2025Active3D.pdf-0004-15.png)


corresponding to global implicit and local explicit uncertainty reduction, respectively. 

**Voxel-wise Information Weighting.** For a voxel _v_ visible from candidate **c** , we define its contribution as: 


![](1_survey/papers/md/Li2025Active3D_figs/Li2025Active3D.pdf-0004-18.png)


where _U_ ( _v_ ) is the hierarchical uncertainty estimate from Eq. 11 and _H_ hybrid( _v_ ) is the hybrid entropy in Eq. 3. _α_ and _β_ are weights. This formulation unifies multi-scale uncertainty into a single information-theoretic weight. 

**NBV Reward.** Given the information weight of the voxel, the expected reward of candidate **c** is obtained via Eq. 4. **Risk-Aware Path Planning.** After obtaining the next goal, we employs an enhanced RRT* algorithm (LaValle and Kuffner 2001) for active path planning. To generate physically feasible trajectories, we integrate the NBV reward into a risk-aware cost function: 


![](1_survey/papers/md/Li2025Active3D_figs/Li2025Active3D.pdf-0004-21.png)


where **p** is the planned path, _C_ travel the navigation cost, _C_ risk the collision probability, and _R_ ( **c** _x_ ) the NBV reward at pose _x_ . 

This proposed NBV searching bridges hybrid scene representation, multi-scale uncertainty, and active trajectory optimization into a single expected information gain framework. By combining global implicit entropy reduction and local explicit observation gain, the planner achieves coverageaware and detail-preserving exploration. 

## **Uncertainty-driven Keyframe Selection** 

Unlike conventional keyframe strategies that are tightly coupled with temporal ordering, we propose a **Uncertaintydriven** selection criterion that anchors high-information observations in the hybrid scene state _Mk_ . Rather than merely ensuring temporal coverage, the proposed keyframes act as a _sparse attention mechanism_ , focusing optimization on regions where the hybrid uncertainty is maximized. 

**Viewpoint-Based Keyframe Selection.** By decoupling keyframe selection from temporal sampling and binding it to viewpoint-space information gain, our method avoids redundant observations and focuses optimization capacity on spatially complementary views, which is crucial for active reconstruction. For a newly acquired RGB-D frame **S** _c_ with camera pose **T** _c,w_ , we compute its viewpoint divergence relative to the active keyframe set _S_ KF: 


![](1_survey/papers/md/Li2025Active3D_figs/Li2025Active3D.pdf-0005-05.png)


where _d_ view measures the viewpoint baseline in SE(3) space, combining angular separation and projected frustum overlap. 

Aggressive active motion planning may cause an agent to overskip salient textural structures, we introduce a dual-uncertainty intersection criterion. Define the _highuncertainty intersection set_ as: 


![](1_survey/papers/md/Li2025Active3D_figs/Li2025Active3D.pdf-0005-08.png)


For frame **S** _c_ , we compute its _uncertainty coverage ratio ρc_ as the fraction of _V_ high visible in its frustum: 


![](1_survey/papers/md/Li2025Active3D_figs/Li2025Active3D.pdf-0005-10.png)


with _V_ vis being the visible voxel set. A frame is promoted to keyframe if: 


![](1_survey/papers/md/Li2025Active3D_figs/Li2025Active3D.pdf-0005-12.png)


where _τ_ view, _τ_ info, _τρ_ are viewpoint, information-gain and coverage threshold, respectively. The uncertainty-driven keyframe selection scheme actually establishes a sparse attention mechanism toward scene structures. This ensures selection of frames observing regions where both geometric and neural uncertainties are high. 

**Viewpoint-Space Sliding Window.** Employing all keyframes for joint optimization still incurs excessive computational burden, prior approaches maintained a sliding window over continuous time. However, this strategy exhibits significant viewpoint redundancy as agent approaches 

the target, while failing to establish sufficient covisibility constraints upon revisiting similar locations. We maintain a local optimization window _Wk_ = _{_ **S** _c_ 1 _, . . . ,_ **S** _cm}_ indexed by spatially selected keyframes, not constrained by temporal adjacency. The hybrid state _Mk_ is jointly refined via: 


![](1_survey/papers/md/Li2025Active3D_figs/Li2025Active3D.pdf-0005-16.png)


where _E_ photo enforces multi-view photometric consistency on _Gk_ , _E_ geo aligns Gaussian primitives with the implicit SDF _Fθ_ , and _E_ reg prevents overfitting across non-overlapping viewpoints. 

## **4 Experiments** 

## **Implementation and Simulator** 

We implement the proposed method within the Habitat simulator (Savva et al. 2019) as an active exploration system. The agent captures posed RGB-D observations along planned viewpoints. The camera field-of-view is set to 60 _[◦]_ vertically and 90 _[◦]_ horizontally, and the system processes sequences online with on-policy planning and incremental reconstruction. Further implementation details are presented in the supplementary material. 

## **Datasets, Metrics, and Baselines** 

Following prior active mapping benchmarks (Yan, Yang, and Zha 2023), we evaluate on two widely used datasets:(i) **Replica** (Straub et al. 2019) with 8 indoor scenes, and (ii) **Matterport3D (MP3D)** (Chang et al. 2017) with 5 large-scale scenes exhibiting significant occlusion and spatial complexity. All methods are run for 2000 exploration steps on Replica and MP3D. 

We report metrics targeting the critical objectives of active reconstruction: _accuracy_ (Acc, cm), _completion_ (Com, cm), and _completion ratio_ (C.R., %), where Acc/Com are computed with a 5 _cm_ threshold. To evaluate rendering quality, we report PSNR, SSIM, and LPIPS on held-out viewpoints. For additional geometric consistency analysis, we compute the Mean Absolute Distance (MAD) between the reconstructed SDF and ground-truth surfaces. 

We compare our method against state-of-the-art active reconstruction frameworks: ActiveNR (Yan, Yang, and Zha 2023), ANM-S (Kuang et al. 2024), NARUTO (Feng et al. 2024), and ActiveSplat (Li et al. 2025). We further compare passive baselines in the supplemental material. All baselines are re-trained and evaluated locally for fair comparison. 

## **Evaluation on Replica** 

Table 1 reports 3D reconstruction and view synthesis metrics on the Replica dataset. Our method consistently achieves the best or second-best performance across all metrics. For reconstruction, it yields the highest completion ratio (C.R.) and lowest Acc/Com error, reaching 98.09% C.R. on R1 and 98.18% on R2. For view synthesis, it achieves the highest PSNR (up to 40.51) and SSIM (0.980) while maintaining the lowest LPIPS, demonstrating sharp textures and photometric consistency. 


![](1_survey/papers/md/Li2025Active3D_figs/Li2025Active3D.pdf-0006-00.png)


**----- Start of picture text -----**<br>
HxpK<br>pLe4<br>gZ6f<br>ANM-S NARUTO ActiveSplat OURS GT<br>**----- End of picture text -----**<br>


Figure 3: Qualitative comparison of 3D reconstruction results on representative MP3D sequences. Additional results and detailed comparisons for all Replica and MP3D sequences are provided in the supplementary material. 

|Method|Metric|Off0|Off1|Off2|Off3|Off4|R0|R1|R2|
|---|---|---|---|---|---|---|---|---|---|
||Acc (cm)_↓_|1.44|1.03|1.60|1.80|1.50|1.47|1.29|1.28|
|ANM-S|Com. (cm)_↓_|1.98|1.55|6.65|1.13|1.08|0.91|1.02|0.85|
||C.R. (%)_↑_|95.43|92.66|79.20|94.98|95.35|96.71|95.66|96.79|
||Acc (cm)_↓_|1.26|1.04|_×_|34.84|1.67|1.75|_×_|1.50|
||Com. (cm)_↓_|1.41|1.30|_×_|2.96|2.01|1.56|_×_|1.49|
|NARUTO|C.R. (%)_↑_<br>PSNR_↑_|97.63<br>31.01|96.88<br>31.43|_×_<br>_×_|91.27<br>26.63|95.14<br>28.57|94.58<br>26.55|_×_<br>_×_|97.56<br>25.56|
||SSIM_↑_|0.892|0.897|_×_|0.831|0.882|0.782|_×_|0.818|
||LPIPS_↓_|0.299|0.283|_×_|0.283|0.284|0.354|_×_|0.367|
||Acc (cm)_↓_|1.16|1.11|1.47|1.70|1.50|1.67|1.43|1.36|
||Com. (cm)_↓_|0.63|0.94|5.59|1.83|1.06|0.84|0.74|1.04|
|ActiveSplat|C.R. (%)_↑_<br>PSNR_↑_|97.54<br>24.487|94.54<br>26.955|80.69<br>22.728|91.49<br>20.965|95.34<br>27.887|97.04<br>26.163|96.84<br>29.005|95.65<br>28.865|
||SSIM_↑_|0.857|0.871|0.888|0.804|0.878|0.823|0.877|0.894|
||LPIPS_↓_|0.145|0.130|0.113|0.232|0.147|0.199|0.136|0.113|
||Acc (cm)_↓_|1.12|1.02|1.34|1.56|1.38|1.59|1.13|1.26|
||Com. (cm)_↓_|1.34|1.17|1.66|1.97|1.87|1.75|1.32|1.52|
|OURS|C.R. (%)_↑_<br>PSNR_↑_|97.76<br>40.51|98.21<br>40.54|96.86<br>33.72|94.70<br>34.14|96.80<br>37.37|97.28<br>33.80|98.09<br>34.63|98.18<br>36.00|
||SSIM_↑_|0.980|0.979|0.951|0.949|0.964|0.948|0.954|0.962|
||LPIPS_↓_|0.030|0.034|0.067|0.075|0.054|0.072|0.056|0.053|



Table 1: Quantitative comparison of 3D reconstruction and view synthesis quality between the proposed method and state-of-the-art approaches on the Replica dataset. The symbol _×_ indicates that the method fails to complete exploration within five trials. 

|Method|Metric|Gdvg|gZ6f|HxpK|pLe4|YmJk|Avg.|
|---|---|---|---|---|---|---|---|
||Acc (cm)_↓_|5.09|4.15|15.60|5.56|8.61|7.80|
|ActiveINR|Com. (cm)_↓_|5.69|7.43|15.96|8.03|8.46|9.11|
||C.R. (%)_↑_|80.99|80.68|48.34|76.41|79.35|73.15|
||Acc (cm)_↓_|5.52|1.62|2.13|4.54|4.50|3.66|
|ANM-S|Com. (cm)_↓_|3.95|2.01|12.49|2.51|3.53|4.90|
||C.R. (%)_↑_|91.00|94.58|60.39|95.02|88.65|85.93|
||Acc (cm)_↓_|2.34|3.57|7.29|4.46|9.52|5.44|
||Com. (cm)_↓_|4.93|2.47|2.84|3.14|5.68|3.81|
||C.R. (%)_↑_|84.88|93.26|92.15|82.67|78.99|86.39|
|NARUTO|PSNR_↑_|23.42|23.84|23.32|27.15|23.64|24.27|
||SSIM_↑_|0.742|0.719|0.734|0.767|0.735|0.739|
||LPIPS_↓_|0.416|0.523|0.492|0.554|0.517|0.500|
||Acc (cm)_↓_|2.39|1.74|2.53|4.09|9.52|4.05|
||Com. (cm)_↓_|3.76|1.34|24.28|1.07|2.84|6.66|
||C.R. (%)_↑_|92.11|97.61|44.45|99.10|90.78|84.81|
|ActiveSplat|PSNR_↑_|22.77|16.40|18.33|23.49|24.57|21.12|
||SSIM_↑_|0.700|0.601|0.776|0.667|0.852|0.719|
||LPIPS_↓_|0.264|0.342|0.236|0.345|0.156|0.269|
||Acc (cm)_↓_|1.68|1.90|1.61|2.68|2.66|2.11|
||Com. (cm)_↓_|1.59|1.96|2.09|2.38|2.81|2.27|
||C.R. (%)_↑_|98.23|97.94|98.12|94.55|91.73|96.11|
|OURS|PSNR_↑_|31.12|32.43|29.53|33.14|30.93|31.43|
||SSIM_↑_|0.912|0.939|0.905|0.920|0.923|0.920|
||LPIPS_↓_|0.160|0.168|0.176|0.222|0.179|0.181|



## **Evaluation on MP3D** 

Table 2 evaluates our method on the MP3D dataset. Compared to ActiveSplat, our approach significantly improves both geometry and rendering fidelity. We achieve the highest combined reconstruction score in nearly all scenes, exceeding 98% on three out of five sequences. For photometric metrics, our method delivers the best PSNR and SSIM in four out of five cases, while maintaining the lowest LPIPS, reflecting perceptually consistent rendering. 

Table 2: Quantitative comparison on the MP3D dataset for 3D reconstruction and novel view synthesis. 

Figure 3 visualizes reconstructions on MP3D. Compared to NARUTO and ActiveSplat, our method produces sharper edges, fewer ghosting artifacts, and consistent textures under dynamic occlusion. 


![](1_survey/papers/md/Li2025Active3D_figs/Li2025Active3D.pdf-0007-00.png)


**----- Start of picture text -----**<br>
(a) Cavity Region (b) MLP Uncertainty (c) Depth Uncertainty (d) Photometric Uncertainty (e) SDF Variation Uncertainty Rotation<br>(f) Clean Mesh (g) SDF Surface (h) Combined Uncertainties (i) Uncertainty with SDF (g) Total Uncertainty Heatmap (k) Occlusion<br>**----- End of picture text -----**<br>


Figure 4: Visualization of uncertainties and their spatial relationship to real scene. Our proposed hybrid strategy not only endows the agent with global optimization capabilities, but also enables it to perceive intricate structures and textures while handling occlusions. 

## **Ablation Study** 

As summarized in Table 3, ablation studies are conducted on the challenging MP3D YmJk scene—characterized by significant occlusion and complex geometry. 

**Uncertainty Setting.** Removing multi-resolution tri-plane encoding causes system failure due to complete loss of spatial perception. Eliminating the MLP-predicted uncertainty volume severely degrades reconstruction completeness (Com: 4.37 cm vs. 2.81 cm) by impeding global scene understanding. Exclusion of depth uncertainty induces erratic reconstruction (Acc: 4.75 cm vs. 2.66 cm) due to compromised surface fidelity estimation, which destabilizes optimization. Omission of RGB uncertainty substantially deteriorates rendering metrics (PSNR: 28.35 dB vs. 30.93 dB), attributable to degraded color/texture perception. Disabling the time-varying SDF representation markedly decreases reconstruction completeness. 

**Searching and Planning.** Replacing the risk-aware path planner with naive uncertainty-volume aggregation degrades reconstruction coverage (C.R.: 89.23% vs. 91.73%), as this suboptimal strategy prompts excessive surface proximity, reducing global observability while increasing collision risk. Finally, disabling keyframe management guided by spatial co-visibility and uncertainty underutilizes historical observations upon revisit, leading to rendering degradation. 

**Advantages of Hierarchical Uncertainties.** Fig. 4 visualizes the Hierarchical Uncertainty Map. The fully implicit uncertainty (b, e) provides the agent with global optimization capability. However, as the MLP-predicted SDF tends to generate redundant structures (f, g), it induces excessively high uncertainty in void regions (a) and redundant structure areas (g). This results in the agent allocating excessive attention to non-existent uncertainties (h). Conversely, the fully explicit uncertainty (c, d) aids the agent in identifying complex structures and textures. Nevertheless, due to its inability 

|Method|PSNR_↑_|SSIM_↑_|LPIPS_↓_|MAD_↓_|Acc_↓_|Com_↓_|C.R._↑_|
|---|---|---|---|---|---|---|---|
|fnal|30.93|0.923|0.179|1.53|2.66|2.81|91.73|
|w.o. Tri-plane Encoder|_×_|_×_|_×_|_×_|_×_|_×_|_×_|
|w.o. MLP Uncert|30.89|0.917|0.191|1.80|2.65|4.37|84.84|
|w.o. Depth Uncert|29.28|0.907|0.218|1.88|4.75|5.12|83.97|
|w.o. RGB Uncert|28.35|0.901|0.201|1.78|2.69|4.02|86.18|
|w.o. SDF Temp|31.23|0.921|0.187|1.58|2.71|3.11|90.83|
|w.o. Risk Planning|30.78|0.916|0.179|1.61|2.67|3.40|89.23|
|w.o. Uncert Keyframe|29.43|0.917|0.182|1.54|2.77|2.88|88.91|
|w. Temporal Sliding Window|28.69|0.910|0.186|1.62|2.69|3.72|87.02|



Table 3: Ablation study on MP3D dataset. The best results are highlighted in the table. 

to perceive occluded regions (k) via _α_ -blending, it leads the agent to prematurely conclude optimization completeness and initiate subsequent planning. Our hybrid approach synergistically combines the strengths of both explicit and implicit representations. By adaptively weighting the explicit and implicit uncertainties, it enhances the agent’s perceptual awareness across all local and global regions (g). 

## **5 Conclusion** 

We have introduced Active3D, an active 3D reconstruction framework that unifies implicit neural fields and explicit Gaussian primitives into a hybrid information-theoretic formulation. By deriving a hierarchical uncertainty volume from this hybrid scene state, our method simultaneously captures global structural priors and local observation confidence, enabling principled next-best-view selection. An uncertainty-driven keyframe selection strategy anchors high-entropy viewpoints as sparse attention nodes, while a viewpoint-space sliding window performs uncertaintyaware local refinement to maintain global–local consistency. Formulating NBV planning as an Expected Hybrid Information Gain problem with a risk-aware path planner further ensures efficient and safe exploration. 


![](1_survey/papers/md/Li2025Active3D_figs/Li2025Active3D.pdf-0008-00.png)


**----- Start of picture text -----**<br>
NARUTO: 19.33 NARUTO: 21.44 NARUTO: 21.30 NARUTO: 19.25 NARUTO: 20.52<br>OURS: 23.38 OURS: 24.68 OURS: 26.73 OURS: 23.88 OURS: 23.57<br>GT GT GT GT GT<br>Gdvg gZ6f HxpK pLe4 YmJK<br>**----- End of picture text -----**<br>


Figure 5: Novel view synthesis results on the MP3D dataset. The tested viewpoints were not present in any training trajectories of the evaluated methods. PSNR values are indicated in the top-left corner. Challenging regions are highlighted with red boxes. 

|Method|PSNR_↑_|SSIM_↑_|LPIPS_↓_|MAD_↓_|Acc_↓_|Com_↓_|C.R._↑_|
|---|---|---|---|---|---|---|---|
|Hybrid|32.43|0.939|0.168|1.22|1.90|1.96|97.94|
|Implicit-only|30.64|0.922|0.187|1.25|1.91|2.34|96.24|
|Explicit-only|32.29|0.932|0.171|1.28|1.92|3.85|94.87|



Table 4: Numerical Results of Hybrid Representation on MP3D dataset. The best results are highlighted in the table. 

## **Acknowledgments** 

This research was supported by the Tier 2 Grant (MOET2EP20124-0015) from the Singapore Ministry of Education. 

## **A Supplementary Details** 

This section elaborates on algorithmic details and experimental results omitted from the main text. We begin by introducing loss functions for both explicit and implicit reconstruction. Subsequently, we present computational efficiency metrics for each submodule and analyze the convergence point of reconstruction completeness during iterative refinement. Finally, extensive comparative evaluations against SOTA methods are provided, assessing reconstruction performance and rendering quality. 

## **Hybrid-map Optimization** 

Within BA optimization, we compute gradients of the loss function with respect to both Gaussian parameters ( _Gi_ = ( _µi,_ Σ _i, αi, ci_ )) and the implicit weights of the MLP. **Explicit Loss.** In the explicit branch, each Gaussian primitive’s parameters are optimized by minimizing photometric ( _L_ pho) and geometric ( _L_ geo) residuals between rendered and observed data: 


![](1_survey/papers/md/Li2025Active3D_figs/Li2025Active3D.pdf-0008-10.png)



![](1_survey/papers/md/Li2025Active3D_figs/Li2025Active3D.pdf-0008-11.png)


Figure 6: Convergence curves of completeness vs. iterations on the MP3D dataset. Our method achieves a faster convergence rate and higher final reconstruction completeness compared to other SOTA approaches. 

where _I_[¯] and _D_[¯] represent the observed RGB image and depth map, while _I_ ( _·_ ) and _D_ ( _·_ ) denote the rendered images synthesized from the static Gaussian map _**M**_ , camera pose **T** _c,w ∈_ SE(3), and intrinsic matrix **K** _∈_ R[3] _[×]_[3] . 

In the implicit branch, we employ four core loss functions to jointly optimize geometry, appearance, and uncertainty: **RGB Loss.** For ray _i_ with rendered color _C_[ˆ] _i_ and ground truth _C_[¯] _i_ , we compute: 


![](1_survey/papers/md/Li2025Active3D_figs/Li2025Active3D.pdf-0008-15.png)


where _N_ is the total ray count, and _ωi_ weights rays based on 

||Implicit Branch<br>Ray Samping<br>MLP Inference<br>MLP Backward|Gaussian Splatting<br>Rendering<br>Mapping|Uncertainty Construction<br>Depth Uncert<br>Photometric Uncert<br>SDF Uncert|Planning<br>Uncert Aggre<br>NBV<br>Risk Field<br>RRT Planning|
|---|---|---|---|---|
|Time (ms)|6.56<br>7.38<br>14.46|7.03<br>35.42|6.34<br>7.55<br>2.55|16.34<br>1.98<br>2.12<br>3.07|



Table 5: Computational Time Breakdown for System Components. The data represent the mean values derived from 2000 test frames in the MP3D dataset. 


![](1_survey/papers/md/Li2025Active3D_figs/Li2025Active3D.pdf-0009-02.png)


**----- Start of picture text -----**<br>
NARUTO: 31.36 NARUTO: 31.31 NARUTO: 26.40 NARUTO: 25.49 NARUTO: 24.31 NARUTO: 26.86<br>OURS: 41.73 OURS: 40.04 OURS: 34.14 OURS: 31.21 OURS: 30.53 OURS: 35.41<br>GT GT GT GT GT GT<br>office0  office1  office3  office4  room0 room2<br>**----- End of picture text -----**<br>


Figure 7: Novel view synthesis results on the Replica dataset. The tested viewpoints were not present in any training trajectories of the evaluated methods. PSNR values are indicated in the top-left corner. Challenging regions are highlighted with red boxes. The office2 and room1 sequences are not exhibited due to NARUTO’s complete failure. 

depth validity. 

where _λk_ are balancing weights for each loss term. 

**Depth Loss.** For valid depth rays ( _D_[¯] _j ≤ D_ trunc): 


![](1_survey/papers/md/Li2025Active3D_figs/Li2025Active3D.pdf-0009-07.png)


where _Nv_ is the count of valid depth measurements, and _D_[ˆ] _j_ is the rendered depth for ray _j_ . 

**SDF Loss.** Given sampled depths **z** = _{zi}[N] i_ =1 _[s]_[along a ray] with _Ns_ samples, ground truth depth _d[∗]_ , and predicted SDF values **s** = _{si}[N] i_ =1 _[s]_[:] 


![](1_survey/papers/md/Li2025Active3D_figs/Li2025Active3D.pdf-0009-10.png)


where _M_ = _{i_ : _|zi −d[∗] | < τ }_ defines the truncation region with threshold _τ_ . 

**Uncertainty Loss.** For valid depth rays: 


![](1_survey/papers/md/Li2025Active3D_figs/Li2025Active3D.pdf-0009-13.png)


where _σj_[2][is the variance from the uncertainty grid for ray] _[ j]_[.] The Uncertainty Loss incorporates two regularization terms. The first term reflects depth prediction uncertainty, promoting uncertainty amplification when depth estimates deviate significantly from ground truth to enhance agent attentiveness, while attenuating uncertainty under accurate predictions. The second term serves to curb excessive uncertainty expansion. 

**Total Loss.** The unified objective combines all loss components: 


![](1_survey/papers/md/Li2025Active3D_figs/Li2025Active3D.pdf-0009-16.png)


## **Computational Efficiency and Convergence** 

Owing to our dual-branch framework comprising both implicit and explicit reconstructions, we demonstrate the realtime capability by separately measuring the forward inference and backward optimization latency per RGB-D frame, further analyzing the computational cost of four key uncertainty components, and presenting the efficiency of path planning. 

**Time Analysis.** Table 5 presents the average computation time for key modules. For the implicit branch, the primary computational cost lies in coordinate point sampling, model forward inference, and back-propagation. Our MLP is lightweight due to its shallow depth and minimal number of hidden neurons. Within the Gaussian reconstruction branch, significant time is consumed by _α_ -blending and Gaussian map optimization, which is performed only on keyframes within the sliding window to enhance computational efficiency. For the uncertainty voxels, implicit uncertainty voxels are directly obtained via MLP inference, while the construction of other uncertainty voxels completes within milliseconds. Finally, the path planning module aggregates uncertainty voxels, identifies the NBV, constructs a risk field, and performs RRT planning. Note that planning is triggered only when the agent reaches its target position and initiates the next planning cycle; the system primarily operates in motion execution, thereby enhancing overall efficiency. **C.R. Convergence.** Fig. 6 illustrates the reconstruction completeness curve versus iteration count. In challenging scenario _YmJk_ , ActiveSplat (Li et al. 2025) fails to plan effective trajectories, significantly hindering its per- 


![](1_survey/papers/md/Li2025Active3D_figs/Li2025Active3D.pdf-0010-00.png)


**----- Start of picture text -----**<br>
Gdvg<br>gZ6f<br>HxpK<br>pLe4<br>YmJK<br>ANM-S NARUTO ActiveSplat OURS GT<br>**----- End of picture text -----**<br>


Figure 8: Reconstruction results on all 5 sequences of the MP3D dataset. The first row of each group illustrates local details, while the second row demonstrates global completeness. Our method achieves reconstructions with higher-fidelity local geometric details and superior completeness, while maintaining robustness across diverse scenarios. Scene appearance may exhibit variations due to method-specific simulator lighting configurations. 


![](1_survey/papers/md/Li2025Active3D_figs/Li2025Active3D.pdf-0011-00.png)


**----- Start of picture text -----**<br>
MonoGS<br>LoopSplat<br>ANM-S<br>NARUTO<br>ActiveSplat<br>OURS<br>GT<br>office0 office1 office2 office3<br>**----- End of picture text -----**<br>


Figure 9: Reconstruction results on the first 4 sequences of the Replica dataset. While MonoGS and LoopSplat are passive reconstruction approaches, the others represent active reconstruction schemes. Our method reconstructs more complete scene structures and demonstrates robustness across all sequences. Scene appearance may exhibit variations due to method-specific simulator lighting configurations. 


![](1_survey/papers/md/Li2025Active3D_figs/Li2025Active3D.pdf-0012-00.png)


**----- Start of picture text -----**<br>
MonoGS<br>LoopSplat<br>ANM-S<br>NARUTO<br>ActiveSplat<br>OURS<br>GT<br>office4 room0 room1 room2<br>**----- End of picture text -----**<br>


Figure 10: Reconstruction results on the last 4 sequences of the Replica dataset. While MonoGS and LoopSplat are passive reconstruction approaches, the others represent active reconstruction schemes. Our method reconstructs more complete scene structures and demonstrates robustness across all sequences. Scene appearance may exhibit variations due to method-specific simulator lighting configurations. 

formance. While Active-INR (Yan, Yang, and Zha 2023) and ANM-S (Kuang et al. 2024) exhibit rapid initial exploration, they ultimately converge to low completeness levels. NARUTO (Feng et al. 2024) demonstrates superior convergence and completeness, yet it frequently predicts large-scale redundant structures in invalid regions (refer to reconstruction results in the main text). In contrast, our method robustly plans trajectories and reconstructs highfidelity meshes. 

## **Rendering Performance** 

Compared to NeRF, Gaussian Splatting exhibits superior novel view synthesis. Quantitative evaluations in the main text confirm our approach outperforms SOTA methods across all metrics. This subsection provides qualitative comparisons on all MP3D and Replica sequences. Fig. 5 and Fig. 7 show results for MP3D and Replica, respectively. Notably, test viewpoints were excluded from all training trajectories. Our method renders sharp boundaries and clear textures. 

## **Reconstruction Results** 

Mesh reconstructions for three MP3D sequences are compared with SOTA in the main text. Fig. 8-10 show full qualitative comparisons across five MP3D and eight Replica sequences. MonoGS (Matsuki et al. 2023) and LoopSplat (Zhu et al. 2024) (passive schemes) exhibit extensive fragmentation due to incomplete scene observation. Neural methods ANM-S (Kuang et al. 2024) and NARUTO (Feng et al. 2024) partially fill holes but generate superfluous structures, causing agent over-focus as shown in the text. ActiveSplat (Li et al. 2025) produces only sparse point clouds. In contrast, our approach ensures superior global integrity and enhanced local geometric accuracy. 

## **B Hybrid Representation Analysis** 

To validate the hybrid implicit-explicit formulation, we compare against two variants: (i) _implicit-only_ , using only _Fθ_ , and (ii) _explicit-only_ , using only _Gk_ . 

## **Implicit-only** 

For the implicit-only evaluation, we utilize the MLPpredicted SDF and uncertainty for active exploration. We simultaneously capture RGB-D images along the planned trajectory, perform Gaussian projection, and optimize the Gaussian branch using the loss defined in Eq. 20. However, the explicit and implicit branches remain entirely independent, yielding no mutual enhancement or interference. 

## **Explicit-only** 

For the explicit-only evaluation, we employ both Depth Uncertainty and Photometric Uncertainty to construct an uncertainty voxel map, computing the discrepancy between the ground-truth depth and the observed depth as the SDF map, which is updated in real-time during subsequent tracking. During incremental updates, voxel grids are projected into camera coordinates and validated against depth bounds and 

image constraints. Valid voxels sample depth values via bilinear interpolation, enforcing local depth continuity to reject outliers. The SDF observations are truncated to a narrow band around surfaces. Each voxel update includes depth adaptation and consistency weight between images, which is maintained by an exponential weighted moving average. 

Although uncertainty predicted by the implicit MLP is not utilized, we retain its presence while optimizing the MLP for convergence analysis. 

## **Complementarity Analysis** 

**Completeness Analysis.** Fusing implicit and explicit branches yields a statistically significant acceleration in reconstruction convergence speed and elevates final reconstruction completeness. This synergistic integration facilitates mutual enhancement between the two map representation paradigms. Table 4 shows the quantitative comparison of different representation modes. 

## **Risking Filed and Planning** 

Conventional path planners rely on explicit representations (e.g., occupancy grids, octrees), yet suffer from degraded navigation accuracy in complex environments due to erroneous occupancy estimation. SDF fields conversely exhibit initial exploration instability, frequently guiding paths into obstacles and causing collisions. To address these limitations, we propose a hybrid implicit-explicit planner. Our framework constructs an occupancy field via Gaussian processes, integrates it with an SDF to generate a risk field, enabling efficient global exploration and planning. 

Fig. 12 visualizes cross-sections of the occupancy field, SDF field, and risk field on MP3D sequence gZ6f. Initial exploration shows the Gaussian-based occupancy map is incomplete, misleading planners into boundary violations. The SDF map generates redundant structures. Our risk field synergistically preserves distinct object boundaries while eliminating redundant structures. 

**Uncertainty Convergence Analysis.** For the three schemes (Hybrid, Implicit-only, Explicit-only), we statistically analyzed the temporal evolution of the MLP-predicted uncertainty throughout the tracking and reconstruction pipeline. Fig. 11 juxtaposes these trends against the convergence/divergence of reconstruction accuracy (Comp) and completeness rate (C.R.). The uncertainty convergence curves reveal that the Implicit-only scheme culminates in persistently elevated uncertainty values. This stems from its tendency to over-prioritize redundant structures (as analyzed in the main text), thereby diminishing exploratory coverage in structurally rich regions and degrading reconstruction quality and completeness. Furthermore, gradient optimization of the uncertainty MLP exhibits direct correlation with depth prediction fidelity. Suboptimal reconstruction accuracy consequently amplifies uncertainty, establishing a detrimental bidirectional feedback loop. 

**Reconstruction Accuracy Analysis.** The Explicit-only scheme demonstrates consistently inferior accuracy across all iterations. This limitation arises from its fundamental inability to address occlusions, causing premature abandonment of under-optimized regions. In contrast, the integration 


![](1_survey/papers/md/Li2025Active3D_figs/Li2025Active3D.pdf-0014-00.png)


Figure 11: Convergence-divergence analysis of hybrid representation on MP3D dataset. The left figure depicts the evolution of predictive uncertainty from the MLP during the iterative process. The center figure plots the reconstruction accuracy against iteration count. The right figure illustrates the progression of reconstruction completeness throughout the iterations. 


![](1_survey/papers/md/Li2025Active3D_figs/Li2025Active3D.pdf-0014-02.png)


Figure 12: Visualization of occupancy field, sdf field, and risk field for MP3D gZ6f. The risk field completes the gaps within the occupancy field and eliminates the inherent redundant structures in the SDF field. 

of implicit uncertainty imbues the agent with heightened attentional focus on occluded areas, thereby enhancing reconstruction precision. 

## **References** 

Aloimonos, J.; Weiss, I.; and Bandyopadhyay, A. 1988. Active vision. _International journal of computer vision_ , 1: 333– 356. 

Barron, J. T.; Mildenhall, B.; Verbin, D.; Srinivasan, P. P.; and Hedman, P. 2022. Mip-nerf 360: Unbounded antialiased neural radiance fields. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 5470–5479. 

Chang, A.; Dai, A.; Funkhouser, T.; Halber, M.; Niessner, M.; Savva, M.; Song, S.; Zeng, A.; and Zhang, Y. 2017. Matterport3d: Learning from rgb-d data in indoor environments. _arXiv preprint arXiv:1709.06158_ . 

Chen, A.; Xu, Z.; Geiger, A.; Yu, J.; and Su, H. 2022. Ten- 

sorf: Tensorial radiance fields. In _European conference on computer vision_ , 333–350. Springer. 

Chen, L.; Zhan, H.; Chen, K.; Xu, X.; Yan, Q.; Cai, C.; and Xu, Y. 2025. ActiveGAMER: Active GAussian Mapping through Efficient Rendering. _arXiv preprint arXiv:2501.06897_ . 

Chen, S.; Li, Y.; and Kwok, N. M. 2011. Active vision in robotic systems: A survey of recent developments. _The International Journal of Robotics Research_ , 30(11): 1343– 1377. 

C¸ ic¸ek, O.;[¨] Abdulkadir, A.; Lienkamp, S. S.; Brox, T.; and Ronneberger, O. 2016. 3D U-Net: learning dense volumetric segmentation from sparse annotation. In _Medical Image Computing and Computer-Assisted Intervention–MICCAI 2016: 19th International Conference, Athens, Greece, October 17-21, 2016, Proceedings, Part II 19_ , 424–432. Springer. Dai, A.; Nießner, M.; Zollh¨ofer, M.; Izadi, S.; and Theobalt, C. 2017. Bundlefusion: Real-time globally consistent 3d reconstruction using on-the-fly surface reintegration. _ACM Transactions on Graphics (ToG)_ , 36(4): 1. 

Elfes, A. 2013. Occupancy grids: A stochastic spatial representation for active robot perception. _arXiv preprint arXiv:1304.1098_ . 

Feng, Z.; Zhan, H.; Chen, Z.; Yan, Q.; Xu, X.; Cai, C.; Li, B.; Zhu, Q.; and Xu, Y. 2024. Naruto: Neural active reconstruction from uncertain target observations. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 21572–21583. 

Fridovich-Keil, S.; Yu, A.; Tancik, M.; Chen, Q.; Recht, B.; and Kanazawa, A. 2022. Plenoxels: Radiance fields without neural networks. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 5501– 5510. 

Huang, R.; Zou, D.; Vaughan, R.; and Tan, P. 2018. Active image-based modeling with a toy drone. In _2018 IEEE International Conference on Robotics and Automation (ICRA)_ , 6124–6131. IEEE. 

Isler, S.; Sabzevari, R.; Delmerico, J.; and Scaramuzza, D. 2016. An information gain formulation for active volumetric 3D reconstruction. In _2016 IEEE International Conference on Robotics and Automation (ICRA)_ , 3477–3484. IEEE. 

Izadi, S.; Kim, D.; Hilliges, O.; Molyneaux, D.; Newcombe, R.; Kohli, P.; Shotton, J.; Hodges, S.; Freeman, D.; Davison, A.; et al. 2011. Kinectfusion: real-time 3d reconstruction and interaction using a moving depth camera. In _Proceedings of the 24th annual ACM symposium on User interface software and technology_ , 559–568. 

Jiang, W.; Lei, B.; and Daniilidis, K. 2024. Fisherrf: Active view selection and mapping with radiance fields using fisher information. In _European Conference on Computer Vision_ , 422–440. Springer. 

Jin, L.; Zhong, X.; Pan, Y.; Behley, J.; Stachniss, C.; and Popovi´c, M. 2025. Activegs: Active scene reconstruction using gaussian splatting. _IEEE Robotics and Automation Letters_ . 

Jin, R.; Gao, Y.; Wang, Y.; Wu, Y.; Lu, H.; Xu, C.; and Gao, F. 2024. Gs-planner: A gaussian-splatting-based planning framework for active high-fidelity reconstruction. In _2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , 11202–11209. IEEE. 

Kazhdan, M.; Bolitho, M.; and Hoppe, H. 2006. Poisson surface reconstruction. In _Proceedings of the fourth Eurographics symposium on Geometry processing_ , volume 7. 

Kerbl, B.; Kopanas, G.; Leimk¨uhler, T.; and Drettakis, G. 2023. 3D Gaussian Splatting for Real-Time Radiance Field Rendering. _ACM Trans. Graph._ , 42(4): 139–1. 

Kirsch, A.; Van Amersfoort, J.; and Gal, Y. 2019. Batchbald: Efficient and diverse batch acquisition for deep bayesian active learning. _Advances in neural information processing systems_ , 32. 

Kuang, Z.; Yan, Z.; Zhao, H.; Zhou, G.; and Zha, H. 2024. Active neural mapping at scale. In _2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , 7152–7159. IEEE. 

LaValle, S. M.; and Kuffner, J. J. 2001. Rapidly-exploring random trees: Progress and prospects: Steven m. lavalle, iowa state university, a james j. kuffner, jr., university of tokyo, tokyo, japan. _Algorithmic and computational robotics_ , 303–307. 

Lee, S.; Chen, L.; Wang, J.; Liniger, A.; Kumar, S.; and Yu, F. 2022. Uncertainty guided policy for active robotic 3d reconstruction using neural radiance fields. _IEEE Robotics and Automation Letters_ , 7(4): 12070–12077. 

Li, Y.; Brasch, N.; Wang, Y.; Navab, N.; and Tombari, F. 2020. Structure-slam: Low-drift monocular slam in indoor environments. _IEEE Robotics and Automation Letters_ , 5(4): 6583–6590. 

Li, Y.; Kuang, Z.; Li, T.; Hao, Q.; Yan, Z.; Zhou, G.; and Zhang, S. 2025. ActiveSplat: High-Fidelity Scene Reconstruction Through Active Gaussian Splatting. _IEEE Robotics and Automation Letters_ , 10(8): 8099–8106. Li, Y.; Lyu, C.; Di, Y.; Zhai, G.; Lee, G. H.; and Tombari, F. 2024. Geogaussian: Geometry-aware gaussian splatting for scene rendering. In _European Conference on Computer Vision_ , 441–457. Springer. 

Li, Y.; and Tombari, F. 2022. E-graph: Minimal solution for rigid rotation with extensibility graphs. In _European Conference on Computer Vision_ , 306–322. Springer. 

Li, Y.; Yunus, R.; Brasch, N.; Navab, N.; and Tombari, F. 2021. RGB-D SLAM with structural regularities. In _2021 IEEE international conference on Robotics and automation (ICRA)_ , 11581–11587. IEEE. 

Matsuki, H.; Murai, R.; Kelly, P. H.; and Davison, A. J. 2023. Gaussian splatting slam. _arXiv preprint arXiv:2312.06741_ . 

Mildenhall, B.; Srinivasan, P. P.; Tancik, M.; Barron, J. T.; Ramamoorthi, R.; and Ng, R. 2021. Nerf: Representing scenes as neural radiance fields for view synthesis. _Communications of the ACM_ , 65(1): 99–106. 

M¨uller, T.; Evans, A.; Schied, C.; and Keller, A. 2022. Instant neural graphics primitives with a multiresolution hash encoding. _ACM transactions on graphics (TOG)_ , 41(4): 1– 15. 

M¨uller, T.; McWilliams, B.; Rousselle, F.; Gross, M.; and Nov´ak, J. 2019. Neural importance sampling. _ACM Transactions on Graphics (ToG)_ , 38(5): 1–19. 

Newcombe, R. A.; Izadi, S.; Hilliges, O.; Molyneaux, D.; Kim, D.; Davison, A. J.; Kohi, P.; Shotton, J.; Hodges, S.; and Fitzgibbon, A. 2011. Kinectfusion: Real-time dense surface mapping and tracking. In _2011 10th IEEE international symposium on mixed and augmented reality_ , 127–136. Ieee. 

Niemeyer, M.; Mescheder, L.; Oechsle, M.; and Geiger, A. 2020. Differentiable volumetric rendering: Learning implicit 3d representations without 3d supervision. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , 3504–3515. Osher, S.; Fedkiw, R.; and Piechor, K. 2004. Level set methods and dynamic implicit surfaces. _Appl. Mech. Rev._ , 57(3): B15–B15. 

Pan, X.; Lai, Z.; Song, S.; and Huang, G. 2022. Activenerf: Learning where to see with uncertainty estimation. In _European Conference on Computer Vision_ , 230–246. Springer. 

Peng, S.; Niemeyer, M.; Mescheder, L.; Pollefeys, M.; and Geiger, A. 2020. Convolutional occupancy networks. In _Computer Vision–ECCV 2020: 16th European Conference, Glasgow, UK, August 23–28, 2020, Proceedings, Part III 16_ , 523–540. Springer. 

Peralta, D.; Casimiro, J.; Nilles, A. M.; Aguilar, J. A.; Atienza, R.; and Cajote, R. 2020. Next-best view policy for 3d reconstruction. In _Computer Vision–ECCV 2020 Workshops: Glasgow, UK, August 23–28, 2020, Proceedings, Part IV 16_ , 558–573. Springer. 

Ronneberger, O.; Fischer, P.; and Brox, T. 2015. U-net: Convolutional networks for biomedical image segmentation. In _Medical image computing and computer-assisted intervention–MICCAI 2015: 18th international conference, Munich, Germany, October 5-9, 2015, proceedings, part III 18_ , 234–241. Springer. 

Savva, M.; Kadian, A.; Maksymets, O.; Zhao, Y.; Wijmans, E.; Jain, B.; Straub, J.; Liu, J.; Koltun, V.; Malik, J.; et al. 2019. Habitat: A platform for embodied ai research. In _Proceedings of the IEEE/CVF international conference on computer vision_ , 9339–9347. 

Schonberger, J. L.; and Frahm, J.-M. 2016. Structure-frommotion revisited. In _Proceedings of the IEEE conference on computer vision and pattern recognition_ , 4104–4113. 

Straub, J.; Whelan, T.; Ma, L.; Chen, Y.; Wijmans, E.; Green, S.; Engel, J. J.; Mur-Artal, R.; Ren, C.; Verma, S.; et al. 2019. The Replica dataset: A digital replica of indoor spaces. _arXiv preprint arXiv:1906.05797_ . 

St¨uckler, J.; and Behnke, S. 2014. Multi-resolution surfel maps for efficient dense 3D modeling and tracking. _Journal of Visual Communication and Image Representation_ , 25(1): 137–147. 

Sucar, E.; Liu, S.; Ortiz, J.; and Davison, A. J. 2021. imap: Implicit mapping and positioning in real-time. In _Proceedings of the IEEE/CVF international conference on computer vision_ , 6229–6238. 

Sun, J.; Xie, Y.; Chen, L.; Zhou, X.; and Bao, H. 2021. Neuralrecon: Real-time coherent 3d reconstruction from monocular video. In _Proceedings of the IEEE/CVF conference on computer vision and pattern recognition_ , 15598–15607. 

Wang, H.; Wang, J.; and Agapito, L. 2023. Co-slam: Joint coordinate and sparse parametric encodings for neural realtime slam. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 13293–13302. 

Whelan, T.; Leutenegger, S.; Salas-Moreno, R. F.; Glocker, B.; and Davison, A. J. 2015. ElasticFusion: Dense SLAM without a pose graph. In _Robotics: science and systems_ , volume 11, 3. Rome, Italy. 

Wu, S.; Sun, W.; Long, P.; Huang, H.; Cohen-Or, D.; Gong, M.; Deussen, O.; and Chen, B. 2014. Quality-driven poisson-guided autoscanning. _ACM Trans. Graph._ , 33(6): 203–1. 

Xu, Z.; Jin, R.; Wu, K.; Zhao, Y.; Zhang, Z.; Zhao, J.; Gao, F.; Gan, Z.; and Ding, W. 2024. Hgs-planner: Hierarchical planning framework for active scene reconstruction using 3d gaussian splatting. _arXiv preprint arXiv:2409.17624_ . 

Yan, Z.; Yang, H.; and Zha, H. 2023. Active neural mapping. In _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , 10981–10992. 

Zhu, L.; Li, Y.; Sandstr¨om, E.; Huang, S.; Schindler, K.; and Armeni, I. 2024. Loopsplat: Loop closure by registering 3d gaussian splats. _arXiv preprint arXiv:2408.10154_ . 

