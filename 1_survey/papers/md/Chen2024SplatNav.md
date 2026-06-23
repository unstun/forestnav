---
citation_key: Chen2024SplatNav
arxiv_id: 2403.02751
arxiv_url: "https://arxiv.org/abs/2403.02751"
title: "Splat-Nav: Safe Real-Time Robot Navigation in Gaussian Splatting Maps"
authors_short: "Timothy Chen et al."
year: 2024
direction_tag: I_corridor_planning
source: pymupdf4llm
converted_at: 2026-06-23T18:59:17Z
origin: ai+web
reviewed: false
---

1 

# Splat-Nav: Safe Real-Time Robot Navigation in Gaussian Splatting Maps 

Timothy Chen[1] _[⋆]_ , Ola Shorinwa[1] _[⋆]_ , Joseph Bruno[3] , Aiden Swann[1] , Javier Yu[1] , Weijia Zeng[2] , Keiko Nagami[1] , Philip Dames[3] , Mac Schwager[1] 

_**Abstract**_ **—We present Splat-Nav, a real-time robot navigation pipeline for Gaussian Splatting (GSplat) scenes, a powerful new 3D scene representation. Splat-Nav consists of two components: 1) Splat-Plan, a safe planning module, and 2) Splat-Loc, a robust vision-based pose estimation module. Splat-Plan builds a safeby-construction polytope corridor through the map based on mathematically rigorous collision constraints and then constructs a Bezier curve trajectory through this corridor. Splat-Loc provides´ real-time recursive state estimates given only an RGB feed from an on-board camera, leveraging the point-cloud representation inherent in GSplat scenes. Working together, these modules give robots the ability to recursively re-plan smooth and safe trajectories to goal locations. Goals can be specified with position coordinates, or with language commands by using a semantic GSplat. We demonstrate improved safety compared to point cloudbased methods in extensive simulation experiments. In a total of 126 hardware flights, we demonstrate equivalent safety and speed compared to motion capture and visual odometry, but without a manual frame alignment required by those methods. We show online re-planning at more than 2 Hz and pose estimation at about 25 Hz, an order of magnitude faster than Neural Radiance Field (NeRF)-based navigation methods, thereby enabling real-time navigation. We provide experiment videos on our project page at https://chengine.github.io/splatnav/. Our codebase and ROS nodes can be found at https://github.com/chengine/splatnav.** 

_**Index Terms**_ **—Vision-Based Navigation, Collision Avoidance, Localization.** 

## I. INTRODUCTION 

Autonomous robotic operation requires robots to localize themselves within an envrionment, plan safe paths to reach a desired goal location, and have closed-loop trajectorytracking. Traditionally, the fundamental problems of planning and localization have been performed in maps represented as occupancy grids [1], triangular meshes [2], point clouds [3], and Signed Distance Fields (SDFs) [4], all of which provide well-defined geometry. 

However, these explicit scene representations are generally constructed at limited resolutions (to enable real-time opera- 

- _⋆_ The co-first authors contributed equally. 

> _†_ This work was supported in part by ONR grant N00014-23-1-2354 and DARPA grant HR001120C0107 and NSF grant 2220866. Toyota Research Institute provided funds to support this work. T. Chen was supported by a NASA NSTGRO Fellowship and A. Swann was supported by NSF GRFP DGE-2146755. 

> 1 Stanford University, Stanford, CA 94305, USA _{_ chengine, shorinwa, swann, javieryu, knagami, schwager _}_ @stanford.edu 

> 2University of California San Diego, San Diego, CA 92093, USA, wez195@ucsd.edu 

> 3Temple University, Philadelphia, PA 19122, USA, _{_ brunoj6, pdames _}_ @temple.edu 

tion), leaving out potentially-important scene details that could be valuable in planning and localization problems. 

Neural Radiance Fields (NeRFs) [5] have recently been used to implicitly represent 3D scenes. NeRFs consist of a volumetric density field and a view-dependent color field parameterized by multilayer perceptrons (MLPs). NeRFs generate photorealistic scene reconstructions, addressing the fundamental limitations of explicit representations; however, NeRFs require running inference on a deep neural network to render the scene, making them impractical for real-time use in robotic path planning. More recently, Gaussian Splatting (GSplat) [6] has emerged as a viable scene representation compared to NeRFs, representing the environment with Gaussian (ellipsoidal) primitives. Compared to NeRFs, GSplats generate higher-fidelity maps at faster rendering rates, with shorter or comparable training times. More importantly for robotics, GSplats, unlike NeRFs, offer a geometrically consistent collision geometry, enabling us to use level sets of these Gaussians to generate an ellipsoidal representation of the scene. These interpretable geometric primitives facilitate the development of rigorous motion planning algorithms that are safe, robust, and real-time. 

In this paper, we introduce _Splat-Nav_ , a pipeline for drone navigation in GSplat maps with a _monocular_ camera. Splat-Nav comprises a lightweight pose estimation module, Splat-Loc, coupled with a planning module, Splat-Plan, to enable safe navigation from RGB-only (monocular) camera observations, as illustrated in Figure 1. Given an incoming RGB frame, Splat-Loc performs Perspective-n-Point (PnP)based localization, leveraging the GSplat map to estimate the RGB and depth values rendered at candidate poses, which are then used to estimate the drone’s pose. Next, Splat-Plan ingests the estimated pose computed by Splat-Loc to generate an initial trajectory, which is subsequently optimized to lie within safe flight corridors constructed from the ellipses that make up the GSplat map. The trajectory is parametrized by smooth, continuously safe Bezier´ splines that route the robot to a specified position or to a open-vocabulary languageconditioned goal location (i.e., “go to the microwave”). This feature enables the execution of Splat-Nav in a wide array of deployment conditions, such as in search missions where the precise location of targets is not known. 

Additionally, the proposed system enables both open-loop trajectory generation and closed-loop re-planning. The latter is important in long trajectories, where existing onboard localization may drift or be subject to noise, impacting the overall safety of the executed trajectory of the robot. In these scenarios, Splat-Loc estimates can either be fused with that 

2 


![](1_survey/papers/md/Chen2024SplatNav_figs/Chen2024SplatNav.pdf-0002-01.png)


Fig. 1: Splat-Nav, consists of a safe planning module, Splat-Plan, and robust localization module, Splat-Loc, both operating on a Gaussian Splatting environment representation. In Splat-Plan we develop a fast, new ellipsoid-ellipsoid collision test to find a safe flight corridor through the GSplat, and plan a spline through the corridor. In Splat-Loc we localize the robot using only RGB images through a PnP algorithm, using the GSplat to render a point cloud. We use a language-embedded GSplat to enable open-vocabulary specification of goal locations like “go to the microwave.” 

of the existing localization module or used as a correction mechanism to steer the current motion toward a safer one. Finally, closed-loop re-planning additionally enables changes in goal locations during execution, leading to more dynamic plans. 

In extensive simulations we compare Splat-Plan and SplatLoc with baseline alternatives for planning and localization, respectively. We show Splat-Plan is always safe with respect to the full collision geometry, while four variants of a pointcloud based planner sometimes lead to collisions, or fail to find trajectories. Splat plan achieves similar or better solutions in terms of path length compared to point cloud-based planner in all cases, with similar computation time. Splat-Plan runs at no less than 2 Hz; comparable to point cloud-based solutions for the same scenes, but faster than gradient-based NeRF planners [7] and sampling-based planners (greater than 1 Hz) for similar solution quality. Similarly, we find that Splat-Loc is more accurate, faster, and fails less often compared to baselines. We demonstrate online pose estimation at about 25 Hz on a desktop computer, enabling real-time navigation. 

Finally, in an experimental campaign with 124 hardware flights, we show that Splat-Nav (Splat-Plan and Splat-Loc running together) perform as well as motion capture or on board VIO, without the manual frame alignment required for those methods to align the MoCap or VIO frame with the GSplat (since both Splat-Plan and Splat-Loc operate natively in the same GSplat map). 

The key contributions of this paper are as follows: 

- We develop a fast polytope corridor generation algorithm to enable provably safe planning for drone navigation in GSplat maps. 

- We develop a fast camera localization module based on GSplat maps that does not require manual alignment of the pose estimation frame to the planning frame, improving the synergy between planning and pose estimation. 

- We demonstrate safe closed-loop re-planning with openvocabulary goal specification, across a series of 124 hardware experimental trials. 

## II. RELATED WORK 

We review the related literature in robot planning and localization with different map representations, categorized into three groups: traditional representations (e.g., occupancy grids, meshes, point clouds, and SDFs), NeRFs, and GSplat. 

**Planning.** We refer readers to [8] for an excellent explanation of planning algorithms in robotics. Most relevant for this work are the graph-based planners (e.g., A _[⋆]_ ), which compute a path over a grid representation of the environment; sampling-based planners (e.g., PRM [9], RRT and RRT _[⋆]_ [10]), which generate a path by sampling candidate states within the configuration space of the robot; and trajectory optimization-based planners (e.g., CHOMP [11] and Traj-Opt [12]), which take an optimizationbased approach to planning. Prior work in [13] utilizes an optimization-based approach in path planning, taking a point cloud representation of the environment and converting this into a set of safe polytopes. The resulting safe polytopes are 

3 

utilized in computing a safe trajectory, parameterized as a spline from a quadratic program (QP), which can be efficiently solved. 

There is also extensive literature on planning based on onboard sensing. Typically, these works present reactive control schemes [14, 15], using the sensed depth to perform collision checking in real time. These methods typically are myopic, reasoning only locally about the scene. Consequently, such methods often converge to local optima, preventing the robot from reaching its goal, especially in cluttered, complex environments. An alternate approach is to construct a map of the environment using depth measurements from Lidar or RGB-D sensors. Often, a Signed Distance Field (SDF) or its truncated variant (TSDF) is constructed from depth data [16, 17], which is encoded within a voxel representation. Such a representation is typical in dynamic robotic motion planning, providing fast collision checking and gradients in planning; however, voxel-based scene models do no provide visually rich or geometrically detailed scene representations compared to NeRFs or GSplats. Point cloud and voxel-based representations require a significant number of points or voxels for high-fidelity scene reconstruction, increasing the computational burden. Prior work [18, 19] introduced a Gaussian Mixture Model (GMM) as a more effective scene representation, which preserves the accuracy of point cloud-based map representations without the additional computational overhead, enabling fast exploration of unknown environments by multi-robot teams. Nevertheless, the aforementioned methods do not achieve photorealistic scene rendering. 

More recent research has developed planning methods for highly expressive neural representations, such as NeRFs, which represent the environment as a spatial density field (with color) [5]. Using a NeRF map, NeRF-Nav [7] plans trajectories that minimize the total collision cost for differentially flat robots, e.g., quadrotors. Further, CATNIPS [20] converts the NeRF into a probabilistic voxel grid and then uses this to generate trajectories parameterized as Bezier´ curves. The work in [21] uses the predicted depth map at sampled poses to enforce step-wise safety using a control barrier function. The above works are complementary, with [7, 20] serving as high-level planners that encourage non-myopic behavior, while [21] can be used as a safety filter for a myopic low-level controller. GSplats are faster to train and provide higher fidelity visual and geometric detail compared to NeRFs [6], making them a strong candidate for scene representations for robot planning. To the best of our knowledge, our work is the first to propose a planning algorithm suitable for GSplat scene representations. 

**Localization.** Prior work in robot localization typically utilizes filtering schemes, such as Extended Kalman Filters (EKFs) [22, 23], Particle Filters (PFs) [24, 25], and other related filters [26, 27], to solve the pose localization problem. These methods generally estimate the pose of the robot from lowdimensional observations (measurements), extracted from the high-dimensional observations collected by the robot’s onboard sensors, such as cameras. This approach often fails to leverage the entire information available in the raw, high-dimensional measurements. Learning-based filtering methods [28, 29] seek 

to address this limitation using deep learning to develop endto-end frameworks for localization, computing a pose estimate directly from raw camera images. Although learning-based approaches can be quite effective given sufficient training data, these methods are often limited to a single robot platform (dynamics model) and thus require separate filters for each robot or environment. 

There is some existing work on tracking the pose of a robot equipped with an on-board camera and IMU through a pre-trained NeRF map. For pose localization, these methods compute a pose that minimizes the photometric loss, given an initial guess of the camera’s pose. iNeRF [30] does this for single images, and NeRF-Nav [7] and Loc-NeRF [31] both track a trajectory using a sequence of images. Other works consider simultaneous localization and mapping (SLAM) using a NeRF map representation. Existing methods such as [30, 32] all simultaneously optimize the NeRF weights and the robot/camera poses. NeRF-SLAM [33] proposes a combination of an existing visual odometry pipeline for camera trajectory estimation together with online NeRF training for the 3D scene. Although applicable to localization in Gaussian Splatting, photometric loss-based localization methods generally have a small region of convergence and require multiple passes through the scene representation for gradient computation, leading to increased computation times. In this work, we introduce a localization algorithm based on the perspective-n-point problem, which addresses these challenges. 

There are a few recent works on SLAM using a GSplat representation of the environment [34, 35, 36]. These SLAM methods use the photometric loss to optimize the camera’s pose, suffering from the aforementioned challenges, which we address with our proposed method. Moreover, these SLAM methods do not consider safe trajectory planning and control, as is the focus of this paper. 

## III. 3D GAUSSIAN SPLATTING 

**Background.** We present a brief introduction to 3D Gaussian Splatting [6], a radiance field method for deriving volumetric scene representations from a set of monocular images. Gaussian Splatting represents non-empty space in a scene using 3D Gaussian primitives, each of which is parameterized by a mean _µ ∈_ R[3] (defining its position), covariance matrix Σ _∈_ S++ (related to its spatial extent and orientation), opacity _α ∈_ [0 _,_ 1], and spherical harmonics (SH) coefficients (defining viewdependent colors). The scene is typically initialized using a sparse point cloud computed via structure-from-motion [37]. To render an image from a given camera pose, the 3 _D_ Gaussians are projected onto the image plane using an affine approximation of the projective transformation, given by Σ2 _D_ = _JW_ Σ _W[T] J[T]_ , with Jacobian _J_ and viewing transformation _W_ . The number of primitives, along with the coefficients for each primitive, is then learned via stochastic gradient descent with a loss function comprising of the photometric loss between the rendered and ground-truth images and the structural similarity (SSIM) index loss (the same as NeRF methods). 

For better numerical optimization, the anisotropic 3D covariance of each Gaussian is written as: Σ = _RSS[T] R[T]_ , where 

4 

_R ∈_ SO(3) is a rotation matrix (parameterized by a quaternion) and _S_ is a diagonal scaling matrix (parameterized by a 3D vector). This anisotropic covariance along with adaptive density control (i.e., splitting and merging Gaussians) enable the computation of compact high-quality representations, even in complex scenes, unlike many state-of-the-art point-based rendering methods. Further, 3D Gaussian Splatting obviates the need for volumetric ray-marching required in NeRF methods, enabling high-quality real-time rendering, even from novel views. 

**GSplats versus NeRFs.** Gaussian Splatting typically requires less training time than state-of-the-art NeRF methods, while achieving about the same or better photometric quality. The biggest difference is in the rendering speed, where Gaussian Splatting achieves real-time performance [6]. Moreover, 3D Gaussian Splatting enables relatively fast extraction of a mesh representation (Remark 1) of the scene from the Gaussian primitives, and instantaneous extraction of the primitives themselves. In contrast, slower meshing techniques [38] are needed for NeRFs, and the extraction of a point cloud requires slow volumetric rendering of many training viewpoints. In Fig. 2, we visualize the ground-truth mesh, the GSplat mesh, and the associated point cloud extracted from a NeRF of a simulated Stonehenge scene to showcase the collision geometry quality of GSplats over NeRFs. Quantitatively, the GSplat mesh has a smaller Chamfer distance (0.031 with 3M vertices) compared to the NeRF point cloud (0.081 with 4M points) despite having fewer points. We note that the NeRF does not necessarily yield a view-consistent geometry due to volumetric rendering, especially when the point cloud is not post-processed to remove outliers, leading to relatively poor collision geometry despite having good photometric quality. 

**Remark 1.** _The original work [6] only projects_ 3 _D Gaussians whose_ 99% _confidence interval intersects the view frustum of a camera, effectively restricting the scene representation to the_ 99% _confidence ellipsoid associated with each Gaussian. Consequently, the union of the_ 99% _confidence ellipsoids represents the entirety of the geometry of the scene learned during the training procedure. We find that this cutoff is too conservative, due to the fact that the color of the Gaussians toward the tails of the distribution are close to transparent. Instead, we find that renderings of the_ 1 _σ collision geometry closely matches that of the GSplat depth channel, so we elect to use_ 1 _σ-ellipsoid as the collision geometry for the remainder of this work. Future work will seek to explore the calibration of this cutoff._ 

**Semantic Gaussian Splatting.** To enable goal specifications for the navigation task in natural-language, we leverage semantic Gaussian Splatting [39, 40, 41], which distills 2D language semantics from vision-language models, e.g., CLIP [42], into 3D GSplat models. In general, these methods assign learnable semantic codes to each Gaussian, supervised by the robust semantic features extracted by 2D foundation models. The semantic GSplats are trained in the same way as non-semantic GSplat via gradient descent. Semantic Gaussian Splatting has been utilized in prior work to enable open-vocabulary robotics 


![](1_survey/papers/md/Chen2024SplatNav_figs/Chen2024SplatNav.pdf-0004-05.png)


Fig. 2: Visualization of a point cloud from a NeRF and a mesh from a Gaussian Splat in the synthetic scene Stonehenge. The Chamfer Distance between the NeRF and ground-truth is 0.081 (with 4M points). The Chamfer distance between the GSplat and ground-truth is 0.031 (with 3M vertices). The collision geometry (especially the foreground) of the GSplat is better and can be extracted instantaneously from the model parameters compared to the costly rendering procedure from many viewpoints to create a point cloud from the NeRF. 

## tasks, e.g., robotic manipulation [43, 44]. 

In the subsequent sections, we present the core contributions of our work in deriving an efficient navigation pipeline for robots, describing how we leverage 3D Gaussian Splatting as the underlying scene representation. Specifically, the quick extraction of simple convex primitives (whose union closely approximates the ground-truth scene geometry) promotes the development of guarantees on safety and solution quality of Splat-Plan and facilitates real-time deployment with low sim-toreal gap while navigating in Gaussian Splatting environments. Similarly, the fast and high-quality color and depth rendering from arbitrary viewpoints of the GSplat enables robust, fast camera localization in Splat-Loc. 

## IV. PLANNING WITH SAFE POLYTOPES 

Now, we present Splat-Plan, our planner for GSplat maps. Splat-Plan generates safe polytopic corridors (inspired by [13]) that represent the free space of a GSplat map between an initial configuration to a goal configuration. These corridors, and the resulting trajectories through them, are rigorously built on theory derived from tests for intersection between ellipsoids. The method is fast enough to provide real-time operation, provides safety guarantees extending to any scene with a pretrained GSplat representation, and is not overly-conservative. 

We stress that, as with any safety guarantee on a map, our ultimate safety rests on the completeness of the map. If the map does not reflect the presence of an obstacle, our method may collide with the obstacle—we cannot avoid what we cannot see. In practice, we observe that GSplat maps provide fast and efficient representations of the underlying ground-truth geometry, as validated in our hardware experiments. 

We would also like to motivate the use of the full collision geometry of GSplats for planning compared to conventional representations like point clouds in an RGB setting. It is common to extract the means of the GSplat to form a point cloud. However, in feature-less regions, we observe that the point cloud can be quite sparse. Meanwhile, the full collision geometry spanned by the ellipsoids covers the full surface. This phenomenon can be observed in Fig. 1, where the render of the ellipsoidal representation of the collision geometry closely 

5 

mimics the RGB render from the GSplat. However, the point cloud extracted from the means is very sparse. While usable for localization, such a sparse representation leaves a large simto-real gap when planning safe trajectories close to those areas. Another option is to sample the surface of these primitives for a point cloud, but even with this modification, point cloud-based planners are not as robust as Splat-Plan (Section VI). 

Before presenting the planning problem, we make the following assumptions on the representations of the robot _R_ and the map _G_ considered in this work. We assume that the robot is represented by a union of the ellipsoids in the nonempty set _{ER,i}[d] i_ =1[,][where] _[d]_[denotes][the][cardinality][of][the] set, i.e., _R ⊆∪[d] i_ =1 _[E][R][,i]_[. For simplicity, we consider a singleton] set _ER_ , noting that the subsequent discussion applies directly to the non-singleton case by running the collision check for all robot ellipsoids. One can also convert a mesh or point cloud of a robot to an ellipsoid by finding the minimal bounding ellipsoid (or sphere). 

We represent non-empty space in the environment with _γ_ % confidence ellipsoids obtained from the GSplat map, as discussed in Remark 1, given by: 


![](1_survey/papers/md/Chen2024SplatNav_figs/Chen2024SplatNav.pdf-0005-04.png)


where _µj ∈_ R[3] denotes the mean of Gaussian _j_ , Σ _j ∈_ S++ denotes its covariance matrix, and _χ_[2] 3[(] _[γ]_[)][denotes][the] _[γ]_[th] percentile of the chi-square distribution with three degrees of freedom. The union of these ellipsoids, given by _G_ = _{Ej}[N] j_ =1[,] defines the occupied space in the environment. To simplify notation, we express the ellipsoid in (1) in standard form: _Ej_ = _{x ∈_ R[3] _|_ ( _x − µj_ ) _[T]_ Σ _[−] j_[1][(] _[x][ −][µ][j]_[)] _[ ≤]_[1] _[}]_[,][where][we][over-] load notation with Σ _j_ := _χ_[2] 3[(] _[γ]_[)Σ] _[j][.]_[ Based on Remark 1, we set] _γ_ = 0 _._ 2 to be safe with respect to the entirety of the supervised scene. 

**Remark 2** (Online Gaussian Splatting) **.** _Our planning algorithm requires a GSplat map. While this map can be trained online using real-time SLAM methods for radiance fields [36, 35, 34], which is a very new and active area of research, we limit the scope of this work to only plan in pre-trained maps._ 

**Remark 3** (Handling Uncertainty of the Scene Representation) **.** _We can vary the value of γ (from that used during the training procedure) based on the quality of the GSplat map and uncertainty in different regions of the GSplat map. In general, larger values of γ inflate the volume of the confidence ellipsoids associated with each Gaussian, resulting in greater safety margins and more conservative planning. The converse holds if smaller values of γ are selected. Moreover, for simplicity, we utilized a uniform value of γ. However, the value of γ can vary among the ellipsoids, allowing the planner to account for varying levels of uncertainty in different regions of the GSplat map. Likewise, the volume of the ellipsoid representing the robot can be increased/decreased to account for uncertainty in the pose of the robot._ 

**Remark 4** (Dynamic Scenes) **.** _We limit our discussion to planning in static scenes. However, we note that our method readily applies to planning in dynamic scenes, under the assumption_ 

_that a dynamic Gaussian Splatting scene representation can be constructed. We discuss more about planning in dynamic scenes in Section VIII._ 

**Problem Statement.** Given a bounding ellipsoid _ER_ for the robot and a GSplat map _G_ , we seek to find a smooth, feasible path _x_ ( _t_ ) for a robot to navigate from an initial configuration _x_ (0) = _x_ 0 to a specified goal configuration _x_ ( _T_ ) = _xf_ , such that there are no collisions in the continuum, i.e., _ER_ ( _x_ ( _t_ )) _∩Ej_ = _∅, ∀Ej ∈G_ , _∀ t ∈_ [0 _, T_ ]. 

**Collision Detection.** We leverage the ellipsoidal representations of the robot and the environment to derive an efficient collision-checking algorithm, based on [45], where we take advantage of GPU parallelization for faster computation. We build upon [45] rather than on other existing ellipsoid-toellipsoid intersection tests, because of its amenability to significant GPU parallelization. We do not utilize the GJK algorithm [46], since we do not require knowledge of the distance between the two ellipsoids. For completeness, we restate the collision-checking method from [45, Proposition 2]. 

**Theorem 1.** _Given two ellipsoids Ea, Eb (with means µa, µb and covariances_ Σ _a,_ Σ _b) and the concave function K_ : (0 _,_ 1) _→_ R _,_ 


![](1_survey/papers/md/Chen2024SplatNav_figs/Chen2024SplatNav.pdf-0005-13.png)


_Ea ∩Eb_ = _∅ if and only if there exists s ∈_ (0 _,_ 1) _such that K_ ( _s_ ) _>_ 1 _._ 

We will let Σ _a,b_ ( _s_ ) = 1 _−_ 1 _s_[Σ] _[a]_[+][1] _s_[Σ] _[b]_[for][compactness] throughout the remainder of the work. Using this, we can rewrite _K_ ( _s_ ) = ( _µb − µa_ ) _[T]_ Σ _[−] a,b_[1][(] _[s]_[)(] _[µ][b][ −][µ][a]_[)][.] 

Note that _K_ ( _s_ ) is concave in _s_ and convex with respect to the means and variances. Theorem 1 is a complete test that will always indicate whether two ellipsoids are in collision or not. We note, however, that solving the feasibility problem in Theorem 1 can be challenging, particularly in large-scale problems, where the feasibility problem has to solved for many pairs of ellipsoids with an associated matrix inversion procedure in each problem. In general, GSplat environments consists of hundreds of thousands to millions of Gaussians [6]. Consequently, we eliminate the matrix inversion by operating in a shared basis for both Σ _A_ and Σ _B_ , for faster collisionchecking, detailed in the following Proposition. 

**Proposition 1.** _By solving the generalized eigenvalue problem for_ Σ _a and_ Σ _b, we obtain generalized eigenvalues λi and the corresponding matrix of generalized eigenvectors ϕ. Then_ 


![](1_survey/papers/md/Chen2024SplatNav_figs/Chen2024SplatNav.pdf-0005-18.png)


## _Proof._ We present the proof in Appendix A. 

**Corollary 1.** _Given a GSplat representation with_ Σ _j_ = _RSS[T] R[T] , let SS[T]_ = **diag** � _λ_[2] _i_ � _. If we choose to parameterize our robot body as a sphere with covariance_ Σ _R_ = _κ_[2] _I, then_ 


![](1_survey/papers/md/Chen2024SplatNav_figs/Chen2024SplatNav.pdf-0005-21.png)


From hereafter, we will treat Corollary 1 as the general formula expression of _K_ ( _s_ ) for both sphere and ellipsoid to 

6 

ellipsoid, substituting the appropriate variables for _R, κ,_ and _λ_ . For readers interested in visualizing the behavior of the aforementioned proposition and corollary, we direct readers to [47, Figure 2] to understand how the shape of _K_ ( _s_ ) changes as ellipsoids move through space. 

**Extension to Linear Motion.** Proposition 1 (and Corollary 1) can be extended to account for linear motion of ellipsoidal bodies. Consider a line segment starting at point _x_ 0 and ending at point _x_ 1, and let _δx_ = _x_ 1 _− x_ 0. Then the line segment can be parameterized as _ℓ_ ( _t_ ) = _x_ 0 + _tδx_ for _t ∈_ [0 _,_ 1]. In our case, we consider a moving ellipsoid _Ea_ , which starts at _x_ 0 = _µa_ . Let 


![](1_survey/papers/md/Chen2024SplatNav_figs/Chen2024SplatNav.pdf-0006-03.png)


The ellipsoid _Ea_ must satisfy Proposition 1 at all points along the line _ℓ_ ( _t_ ), so the safety test[1] is 


![](1_survey/papers/md/Chen2024SplatNav_figs/Chen2024SplatNav.pdf-0006-05.png)


We seek to solve a portion of Eq. (3) using Corollary 2. 

**Corollary 2.** _Note that K_ ( _s, t_ ) _is a convex scalar function in t because δx[T]_[Σ] _[−] a,b_[1][(] _[s]_[)] _[δ][x][>]_[0] _[for][all][δ][x]_[=][0] _[since][covariance] matrices are symmetric and positive definite. The t that minimizes K_ ( _s, t_ ) _is_ 


![](1_survey/papers/md/Chen2024SplatNav_figs/Chen2024SplatNav.pdf-0006-08.png)


_so the optimal value will be t[∗]_ ( _s_ ) = _clamp_ ( _t_[ˆ] ( _s_ ) _,_ 0 _,_ 1) _. Then we can write the safety check as_ 


![](1_survey/papers/md/Chen2024SplatNav_figs/Chen2024SplatNav.pdf-0006-10.png)


_Proof._ Sion’s minimax theorem states that switching the order of the minimum and maximum yields identical solutions when _K_ ( _s, t_ ) is concave in _s_ and convex in _t_ . Additionally, _s_ must lie in a convex set and _t_ in a compact, convex set, which Eq. (3) admits. Consequently, the max-min problem results is an inner minimization problem of a quadratic, which is solved in closed-form. The point-wise minimum of concave functions _K_ ( _s, t[∗]_ ( _s_ )) is concave, hence the outer maximization is still over a concave function. 

As a byproduct of concavity of _K_ ( _s_ ), we have the following corollary: 

**Corollary 3.** _By concavity of K_ ( _s_ ) _, any approximate solution s_ ˆ _in Theorem 1, Proposition 1, Corollary 1, or Corollary 2 results in K_ ( _s[∗]_ ) _≥ K_ (ˆ _s_ ) _. Hence, no approximate solution will yield false negatives (i.e., miss a collision)._ 

**Optimization.** While Corollary 3 is a nice blanket certificate, we can craft approximate solutions that exponentially converge to the optimal _s[∗]_ such that false _positives_ tend to 0 (i.e., a perfect approximation). Bisection searches (especially in 1D) are efficient, simple ways to guarantee exponential convergence for bounded variables in smooth convex/concave functions, 

> 1Note that the sliding of the ellipsoid along a line forms capsules, making Corollary 2 also a necessary and sufficient collision test between this type of geometry with an ellipsoid. 

ˆ i.e., _||si − s[∗] || ≤ ϵ_ for any desired _ϵ_ . We propose to solve max _s∈_ [0 _,_ 1] _K_ ( _s_ ) using Algorithm 1. 

**Algorithm 1:** _K_ ( _s_ ) Bisection Search 


![](1_survey/papers/md/Chen2024SplatNav_figs/Chen2024SplatNav.pdf-0006-18.png)


**Corollary 4.** _The distance of s to s[∗] converges at a rate of_ 1 _ϵ_ = 2 _[k]_[+1] _[through][k][iterations][using][Algorithm][1.]_ 

_Proof._ The bisection method guarantees convergence to a root of a continuous function _f_ ( _s_ ) in the interval [ _a, b_ ] if _f_ ( _a_ ) and _f_ ( _b_ ) have different signs. The method achieves a rate of 


![](1_survey/papers/md/Chen2024SplatNav_figs/Chen2024SplatNav.pdf-0006-21.png)


Note that _K_ ( _s_ ) evaluates to 0 at both _s_ = _{_ 0 _,_ 1 _}_ , and _K_ ( _s_ ) is concave and non-linear. Therefore, we know a unique global maxima occurs between 0 and 1 and that the gradient _f_ ( _s_ ) = _∇sK_ ( _sk, t[∗] k_[)][is][positive][at] _[s]_[ = 0][and][negative][at] _[s]_[ = 1][.] 

Additionally, note that Algorithm 1 is batchable across many queries to different ellipsoids and is more efficient than performing uniform sampling for the same tolerance. For all tests, we use _k_ = 10. 

**Computing Safe Polytopes.** We like to again emphasize that having convex primitives (ellipsoids) as an environment representation facilitates the development of interpretable algorithms for planning. This is especially true in the construction of safe trajectories within convex safe polytopes, which define obstaclefree regions of the robot’s configuration space. We build upon prior work on convex decomposition of configuration spaces such as [48, 13]. In this work, we leverage the ellipsoidal primitives to create polytopes that define the safe regions of space through the use of supporting hyperplanes. The ellipsoidal representation of the environment obtained from GSplat enables the direct computation of these convex obstaclefree regions without the need for a convex optimization procedure. Furthermore, our method is fast enough to run in real time. In the following proposition, we describe the generation of safe polytopes for a given robot. 

7 

**Proposition 2.** _Given a seed point x[∗] for a candidate robot position and a collision set G[∗]_ = _{Ej}, a supporting hyperplane for the ellipsoid robot can be derived from Proposition 1 or Corollary 1 for any desired buffer ϵ >_ 0 _:_ 


![](1_survey/papers/md/Chen2024SplatNav_figs/Chen2024SplatNav.pdf-0007-02.png)


_where_ ∆ _j_ = _x[∗] − µj,_ Σ _[−] x[∗]_[1] _,j_[(] _[s][∗]_[)] _[uses][the][robot][shape][and]_[Σ] _[j][,] and_ ( _kj[∗]_[)][2][=] _[ K]_[(] _[s][∗]_[) = ∆] _[T] j_[Σ] _[−] x[∗]_[1] _,j_[(] _[s][∗]_[)∆] _[j][>]_[ 0] _[,][for][s][∗][∈]_[(0] _[,]_[ 1)] _[.] By stacking the hyperplane constraints (aj, bj), we arrive at a polytope Ax ≥ b that is guaranteed to be safe._ 

_Proof._ We provide the proof in Appendix B. 

**Corollary 5.** _Proposition 2 can be extended for the K_ ( _s_ ) _in Corollary 2 by substituting x[∗]_ = _x_ 0 + _t[∗] δx, where t[∗] ∈_ [0 _,_ 1] _._ 

## _Proof._ We provide the proof in Appendix C. 

Proposition 2 and Corollary 5 guarantee manageability, coined by [49], which refers to the encapsulation of the seed object by the free-space partition. This property is important to guarantee connected-ness of each part of the safe flight corridor, which in turn admits a feasible trajectory that resides solely within the corridor. 

**Generating Safe Paths.** We present Splat-Plan, similar in spirit to the safe flight corridor method from [13]. There are four primary components: (1) feasible path seeding through graph-based search, (2) construction of a collision set around each part of the path, (3) generation of hyperplane constraints, and (4) smooth path planning posed as a spline optimization. For Splat-Plan, we leverage Corollary 2, Algorithm 1, and Corollary 5 to generate safe polytopes along the seed path. Within the polytopes, we plan Bezier´ curves, which can be formulated as a quadratic program. 

_1) Seed Path:_ There are two primary flavors of graph-based paths that are popular in the literature: those that use random trees (e.g. RRT) and those on uniform grids. We will detail how both can be used as an initialization. 

Methods like RRT primarily rely on a module for collision detection at test points as well as a module to test for collision along a line. The use of Corollary 2 serves both functions. Unfortunately, the probabilistic completeness of these algorithms make them undesirable for real-time execution. 

The use of a uniform grid to run algorithms like Dijkstra Search are optimal and typically faster than those of random trees **if** there exists a cheap subroutine that converts the scene representation into a uniform grid. Specifically, we would like to avoid expensive collision checking between each disjoint sub-region of 3 _D_ space with the environment. Conversion from point clouds to binary voxel grids circumvents this issue by binning every point and assigning it an ( _i, j, k_ ) index. 

While there are many ways one could convert the ellipsoidal representation into a conservative occupancy grid, we propose the following method that is parallelizable and efficient, and show in Section VI that it is not too conservative. Without loss of generality, we assume that the robot is a sphere, which can be done by applying the necessary rotation and stretching 

for all ellipsoids such that the robot ellipsoid is a sphere. For every ellipsoid, we calculate its axis-aligned bounding box. 

The Minkowski sum of the ellipsoid with a sphere does not present an ellipsoid. However, at the extremal points which represent intersections of the bounding box with the ellipsoid, the normal of the ellipsoid is in the principal directions. The bounding box is defined as the following 


![](1_survey/papers/md/Chen2024SplatNav_figs/Chen2024SplatNav.pdf-0007-15.png)


where _µ[i] j_[is][the] _[i][−]_[th][element][in][the][mean][for][ellipsoid] _[j]_[,] and Σ _ii_ represents the _i_ -th diagonal term of the associated covariance. 

For those _Bj_ whose side lengths are not within the resolution of each grid cell _vx,y,z_ , we subdivide them by their largest side length relative to _vx,y,z_ . We iterate on this process until all subdivisions of _Bj_ are smaller than _vx,y,z_ . At this point, we can calculate all 8 vertices for every subdivision of _Bj_ and bin them similar to the point cloud case. This procedure can leverage batch operations on GPU and ensures that we construct an over-approximation of the collision geometry. 

To account for the extent of the robot body, we convert the robot sphere into a kernel (similar to [20]) and perform a MaxPool3D operation. The resultant grid represents where the robot can be centered and be safe or unsafe. More sophisticated subdivision routines may be used to reduce the conservativism of the grid. Once the final grid is constructed, we run Dijkstra to find the seed path represented as an ordered set of connected line segments _L_ = _{ℓi}[L] i_ =1[.] 

_2) Collision Set:_ Along the seed path, rather than checking collisions between the robot and _every_ ellipsoid in the scene, we would like to quickly find a subset of these primitives in the local vicinity of the robot to check against for efficiency reasons. In fact, Proposition 1 or Corollary 1 can directly be used to define a ball or ellipsoid collision set centered around the seed path, but may contain unnecessary information at the cost of additional compute. 

Instead, following the paradigm of [13], we can rapidly define a bounding box oriented along _ℓi_ and pinpoint ellipsoids that live within it without incurring the additional cost of reasoning about the linear motion of the robot body. We define a radius _rs_ = 2 _va_ max[2] max[,][which][is][the][maximum][stopping][distance] (dependent on the maximum velocity and acceleration), such that the facets of the box are no less than _rs_ + _κ_ away from _ℓi_ . This bounding box will be denoted as _A[bb] i[x][ ≤][B] i[bb]_[.] 

To check all ellipsoids that are at least partially contained within the box, we check for the minimum signed distance between each hyperplane min _x∈Ej a[bb] i[x][≤][b][bb] i_ with every ellipsoid _Ej_ in the scene. Ellipsoids that have negative signed distance for every hyperplane in the box will be at least partially contained. To perform this check, the plane and ellipsoid undergo an affine transformation to produce a new plane and an origin-centered sphere. The signed distance of the new plane from the origin must be less than 1, namely 


![](1_survey/papers/md/Chen2024SplatNav_figs/Chen2024SplatNav.pdf-0007-22.png)


8 


![](1_survey/papers/md/Chen2024SplatNav_figs/Chen2024SplatNav.pdf-0008-01.png)


Fig. 3: Splat-Plan, as described by Algorithm 2. Given a GSplat and its corresponding ellipsoidal collision geometry, Splat-Plan generates a binary occupancy grid representing the collision-less free space. Next, a seed path is created using graph-based search. Corollary 5 synthesizes a set of connected polytopes forming a corridor around the feasible path. Finally, a quadratic program is solved for the control points of a sequence of Bezier´ curves that lives entirely within the corridor and hence is safe. 

_3) Polytope Generation:_ The creation of polytopes around the line segment _ℓi_ can be done through Corollary 5 and appending these constraints to the bounding box constraints _a[bb] i[x][ ≤][b][bb] i[−][κ][∥][a][bb] i[∥]_[2][. Note that if we were to create a halfspace] for every ellipsoid in the constraint set, we would overly constrain the free space, leading to a smaller-than-necessary polytope. This phenomenon arises from the fact that, given an existing set of halfspaces, ellipsoids that are outside of the set can still contribute non-redundant halfspaces to the existing set. Moreover, having more halfspaces than necessary in the polytope representation can significantly slow down the proceeding spline optimization. 

Therefore, we adopt a greedy algorithm like [13]. Every time we form a new halfspace, we use Eq. (6) to eliminate from our collision set all ellipsoids that violate this halfspace. Of the remaining ellipsoids, we create a new halfspace for the one that had the smallest _K_ ( _s[∗]_ ). We iterate this process until no ellipsoids remain in the collision set. 

Due to manageability, we can further reduce the complexity of our corridor representation by retrieving a smaller number _P_ of polytopes than line segments _L_ . For the current part of the seed path, we construct the minimal collision set and the polytope ( _Ap, bp_ ). Then, we check subsequent line segments, represented as the endpoints, with the current polytope. The first instance where the line segment is not fully contained in ( _Ap, bp_ ), we construct a new minimal collision set and polytope and repeat the process until the end of the seed path. Keeping more polytopes enables smoother paths (e.g. less opportunity for pinch points) at the expense of higher computation in the spline optimization phase. 

_4) Spline Optimization:_ Given the safe flight corridor represented as _P_ polytopes and initial and final configurations ( _x_ 0 _, xf_ ), we compute a set of _P_ Bezier´ curves (parametrized by _M_ + 1 control points _c[m] p_[and][Bernstein][basis] _[β][m]_[(] _[t]_[)][2][with] progress _t ∈_ [0 _,_ 1]) representing the trajectory of the robot 

using the path-length minimization problem: 


![](1_survey/papers/md/Chen2024SplatNav_figs/Chen2024SplatNav.pdf-0008-08.png)



![](1_survey/papers/md/Chen2024SplatNav_figs/Chen2024SplatNav.pdf-0008-09.png)



![](1_survey/papers/md/Chen2024SplatNav_figs/Chen2024SplatNav.pdf-0008-10.png)



![](1_survey/papers/md/Chen2024SplatNav_figs/Chen2024SplatNav.pdf-0008-11.png)



![](1_survey/papers/md/Chen2024SplatNav_figs/Chen2024SplatNav.pdf-0008-12.png)


Without the dynamics constraints (7f), the optimization problem reduces to a quadratic program that can be solved in real-time, producing a trajectory that can be tracked by differentially-flat robots. The quadratic program is solved natively using Clarabel [50]. 

Due to the convex hull property of Bezier´ curves, constraining the control points to lie in the polytopes ensures that all points along the curves will lie in the corridor and hence guarantees safety in the continuum. Additionally, Splat-Plan is sound and complete, summarized in the following corollary. 

**Corollary 6.** _Given that there exists a smooth, safe path in an arbitrarily complex GSplat environment, Splat-Plan (Algorithm 2) will always return a feasible, safe, and smooth path as the limit of the voxel occupancy grid used for path seeding goes to_ 0 _, the number of steps in Algorithm_ 1 _goes to ∞, and the number of control points parametrizing the spline also goes to ∞._ 

_Proof._ As the occupancy grid resolution grows increasingly small, the unoccupied grid converges toward the true collisionfree space of the scene. In the limit, Dijkstra will find an initial safe, feasible path toward the goal. Next, the constructed set of polytopes forming the corridor will (1) always be safe, (2) connected, and (3) contain the initial path assuming a 

> 2For notational simplicitiy, we refer to the variable as both the conventional basis and its time derivatives up to some specified order _D_ . 

9 

sufficient number of iterations of Algorithm 1 is performed due to Corollary 4 and manageability. Due to the Stone-Weierstrass theorem [51], given an arbitrary smooth curve, a Bezier curve of´ sufficient degree can exactly recover it. Under mild conditions, a smooth curve exists within the corridor, and given a sufficiently expressive parametrization and enough time, the quadratic program will find a solution. 

Certainly, without these conditions, Dijkstra could fail to find a path for finite resolutions. Similarly, Algorithm 1 and Corollary 5 could return a conservative estimate that does not contain the line segment if given an insufficient number of iterations. Finally, Eq. (7) could return infeasibility if the degree of the Bezier´ curve is not expressive enough. Failure of these three components will lead Splat-Plan to not return a solution. However, in our experimental results, we find that this is not the case in practical settings. 

**Querying Waypoints.** For simplicity of notation, we will refer to the output of Splat-Plan as _X_ ( _T_ ), which takes in metric time, finds the associated spline _Xp_ , and queries the spline for its position and derivatives at the local spline time ∆ _pT_ = _T − Tp,start_ . In our hardware demonstrations, we unnormalize the Bezier´ curves in order to approximately achieve the desired _v_ max. Specifically, by knowing the associated subset of the seed path (and the total length _Lp_ ) for each polytope, we can enforce in metric time the duration of the individual splines ∆ _Tp,_ 0 = _vmaxLp_[.][Our][local][B][ezier][´][curve][is][re-mapped][using][the] formula _Xp_ ( _T_ ) = _xp_ ( ∆[∆] _T[p] p,[T]_ 0[)][.][Eq.][(7)][can][again][be][used][to] constrain _Xp_ to lie within the safety corridor and enforce continuity in metric time. The entire Splat-Plan algorithm is visualized in Fig. 3. 

## V. MONOCULAR POSE ESTIMATION 

In this section, we present our pose estimation module, SplatLoc, for localizing a robot in a GSplat representation of its environment. This is essential to the overall functionality of the SplatNav pipeline as the safety guarantees of Splat-Plan only hold if the robot is able to consistently and accurately estimate its pose in the GSplat map. Splat-Loc only requires a monocular RGB camera, which enables it to work on a broad range of hardware platforms, including those beyond robots (such as mobile phones). Furthermore, Splat-Loc can be used either as a stand-alone pose estimation system or in conjunction with an independent pose estimation system (onboard VIO, external motion capture, etc). 

**Problem Formulation.** Formally, we wish to estimate the pose of a robot at a particular time _T_[ˆ] _t ∈_ SE(3) given a color image _It ∈_ R _[H][×][W][ ×]_[3] . The true camera pose _Tt_ is unknown. A pose in SE(3) is parameterized by a rotation matrix _R ∈_ SO(3) and a translation vector _τ ∈_ R[3] 


![](1_survey/papers/md/Chen2024SplatNav_figs/Chen2024SplatNav.pdf-0009-07.png)


In the case that the navigating robot has an independent pose estimation system, we would like to use those pose estimates as initializations for Splat-Loc’s optimization procedures, and also correct these poses using the estimates from Splat-Loc. 

## **Algorithm 2:** Splat-Plan 

|**Input:** _x_0, _xf_, grid resolution, lower, and upper bounds<br>(_d, uℓ, uh_), _vmax_, _amax_, _κ_, _G,_ num. iters. _k_;|
|---|
|**Output:** B´ezier spline _x_(_t_);|
|// Create the voxel grid|
|_V ←_GSplatVoxelGrid(_d, uℓ, uh, κ, G_);|
|// Path Seeding: creates safe but|
|non-smooth path|
|_{ℓ}L_<br>_i_=1 _←V_(_x_0_, xf_);<br>// Iterate through the line segments|
|**for** _i ←_1 **to** _L_ **do**|
|// Skip to next line segment if|
|contained|
|**if** _IsInPolytope_(_ℓi,_(_Acurr, Bcurr_)) **then**|
|continue;|
|// Create collision set|
|_Gi,_(_Abb_<br>_i , Bbb_<br>_i_ )_←_<br>GetCollisionSet(_ℓi, κ, G, vmax, amax_);<br>// Initialize polytope<br>_Ai, Bi ←Abb_<br>_i , Bbb_<br>_i_ ;<br>// Create polytope<br>**while** _|Gi| >_0 **do**<br>_{Kj} ←_Algorithm 1(_ℓi, Gi, k_);<br>_K ←_min(_{Kj}_);<br>// Create halfspace<br>(_A, B_)_←_Corollary 5(_ℓi, K_);<br>// Add halfspace to polytope<br>_Ai ←_append(_Ai, A_)_, Bi ←_append(_Bi, B_);|
|// Reject redundant ellipsoids|
|_Gi ←_Eq. (6) (_Gi,_(_A, B_));|
|**end**|
|// Set current polytope|
|_Acurr ←Ai, Bcurr ←Bi_;|
|**end**<br>// Optimize B´ezier splines<br>_x_(_t_)_←_Optimize(_x_0_, xf, {_(_Ap, Bp_)_}P_<br>_p_=1)|



We assume knowledge of the camera’s calibration including the intrinsic matrix and distortion coefficients for projective geometry. These are easily computable, and are often available from the camera manufacturer. 

**Lightweight Monocular Pose Estimator.** At its core, SplatLoc uses the fast rendering capabilities of GSplats and standard tools from camera tracking to formulate Perspective-n-Point (PnP) problems, which can be reliably solved using off-theshelf optimizers, and produces accurate estimates of the robot pose. As input for the pose estimation procedure, we have the color image and a coarse initial guess for the pose estimate, _T_[ˆ] _t,_ 0. This guess can either come from an independent localization module (e.g. VIO) or can simply be the previous time step’s estimate. We begin by rendering an RGB image using the GSplat map with the camera pose set to the initial guess and simultaneously generate a local point-cloud within the camera’s view, effectively using the GSplat as a monocular depth estimator. 

Next, a local feature extractor is used to compute visual 

10 

features (keypoints and descriptors) in both the camera image and the rendered image. Each keypoint has an associated pixel coordinate ( _u, v_ ) _∈_ R[2] , and let _m_ and _n_ respectively be the number of keypoints in the camera and rendered images. A feature matcher is used to determine correspondences between the visual features in the camera image and the rendered image. Let _ℓ ≤_ min _{m, n}_ be the number of successfully matched features. In our experiments we found that the feature extractor SuperPoint [52] used in conjunction with the transformer-based LightGlue [53] feature matcher had the best performance (see Section VI for more details). 

Using the rendered depth image and the camera intrinsics matrix, the keypoints from the rendered color image can be projected into the 3D to produce a point cloud. Let _p_ ˆ _j ∈_ R[3] be the position of the _j_ th projected keypoint where _j ∈_ 1 _, . . . , n_ . Finally, we seek to minimize the following reprojection error in order to find the relative pose transform that transforms _T_[ˆ] _t,_ 0 to _T_[ˆ] _t_ 


![](1_survey/papers/md/Chen2024SplatNav_figs/Chen2024SplatNav.pdf-0010-03.png)


where _ρk_ = [ _uk, vk,_ 1] _[⊤]_ and subsequently recover our estimated pose _T_[ˆ] _t_ = _T_[¯] _tT_[ˆ] _t,_ 0. Eq. (9) is the Perspective-n-Point problem, and is a nonlinear least-squares optimization problem that we solve using the Levenberg-Marquardt algorithm. In practice, we use Random Sample Consensus (RANSAC) to remove outliers from the set of matched features which results in more robust solutions of Eq. (9). We illustrate this procedure in Figure 1. In Section VI, we highlight the accuracy of incremental estimation in real-world experiments while a drone navigates a cluttered environment. 

**Global Initialization.** The above pose estimation procedure requires common overlap between _It_ and _I_[ˆ] _t_ , necessitating a reasonably accurate initial estimate of the robot’s pose _T_[ˆ] _t,_ 0, which may not be available in many practical settings. When a good initial guess of the robot’s pose is unavailable, we execute a global pose estimation procedure. Note that this only needs to be performed once, and then subsequent pose estimate steps can be performed using the solution from the previous iteration. 

One approach requires a monocular depth estimator, e.g., [54, 55], to augment the RGB image obtained by the robot with depth information, which is used to generate a point cloud (in the camera frame). Another is to randomly sample SE(3) for pose initializations and return the pose estimate from the P _n_ P run that has the lowest reprojection error. However, we instead generate a point cloud of the scene from the GSplat means _{µj}[N] j_ =1[, enabling the formulation of a point-cloud registration] problem: 


![](1_survey/papers/md/Chen2024SplatNav_figs/Chen2024SplatNav.pdf-0010-07.png)


where _C_ denotes the set of correspondences, associating the point _p_ in the map cloud to a point _q_ in the point cloud from the camera. If we are given a known set of correspondences, we can compute the optimal solution of (10) using Umeyama’s method [56]. 

In practice, we do not have prior knowledge of the set of correspondences _C_ between the two point clouds. To address this challenge, we apply standard techniques in feature-based global point-cloud registration. We begin by computing 33dimensional Fast Point Feature Histograms (FPFH) descriptors [57] for each point in the point-cloud, encoding the local geometric properties of each point. Prior work has shown that visual attributes can play an important role in improving the convergence speed of point-cloud registration algorithms [58], something that FPFH does not do. To solve this, we augment the FPFH feature descriptor of a given point with its RGB color. We then identify putative sets of correspondences using a nearest-neighbor query based on the augmented FPFH descriptors, before running RANSAC to iteratively identify and remove outliers in _C_ . The RANSAC convergence criterion is based on the distance between the aligned point clouds and the length of a pair of edges defined by the set of correspondences. **Non-invasive Pose Correction.** While fusing Splat-Loc poses with existing pose estimates like VIO is beyond the scope of this work, we will address challenges that arises when using SplatPlan to plan high-level plans in a GSplat while using existing pose estimates to stabilize (i.e., for control). Fundamentally, discrepancies between the one in which the GSplat is trained in _T_ gs and the running coordinate frame of the existing localization module _T_ (control _,t_ ) can vary with time, either due to noise or drift. Yet, poses from Splat-Loc are inherently tied to the GSplat coordinate frame, leading to potentially more informative state estimates of whether the robot is in collision or not. In turn, these estimates can be passed into Splat-Plan to create safer trajectories if necessary, as depicted in Fig. 1. However, the trajectory that Splat-Plan returns again lives in _T_ gs and not necessarily the running coordinate frame of the existing localization, which is crucially used for control. To overcome this mismatch, we necessarily need to transform the outputs of Splat-Plan into the control localization frame. Namely, there exists a transform[control] _[,t] T_ gs : _T_ gs _→T_ (control _,t_ ) that maps poses in the GSplat frame to ones in the control localization frame. Therefore, the waypoints that we send to the robot are (control _,t_ ) _T_ gs( _X_ ( _T_ )), which is depicted in Fig. 1 as the input to the robot. 

## VI. EXPERIMENTS 

We demonstrate the effectiveness of our navigation pipeline for GSplat maps, examining its performance in real-world scenes on hardware and in simulation. In addition, we perform ablative studies comparing our algorithms against existing methods. 

## _A. Simulation Results_ 

_1) Test Environments:_ We benchmark Splat-Plan and SplatLoc independently on four different environments: **Stonehenge** , a fully-synthetic scene, and three real-world scenes **Statues** , **Flightroom** , and **Old Union** . For **Stonehenge** , we captured image-pose pairs by rendering the **Stonehenge** mesh in Blender. For the other scenes, we recorded a video from a mobile phone and processed the image frames through structure-from-motion (COLMAP [37]) to retrieve corresponding camera poses and intrinsics. 

11 

_2) Splat-Loc Evaluations:_ We compare Splat-Loc to existing pose estimation methods, including a baseline GS-Loc, based on the localization component of existing GSplat SLAM methods [34, 35]. We leverage finite differences to estimate the gradient of the photometric loss function utilized in the pose estimator, which might not be particularly fast or robust, especially for larger errors in the initial pose estimate. While these methods optimize over the re-rendering loss composed of the photometric loss, and in some cases, depth and semantic-related loss terms, in our baseline, we optimize only over the photometric loss, since we assume the robot in these evaluations does not have an RGB-D camera for depth measurements. As a result, our baseline essentially matches the GSplat SLAM method in [36]. In addition, we compare our pose estimator to the Point-to-plane Iterative Closest Point (ICP) [59] and Colored-ICP [58] algorithms, assuming these point-cloud methods have privileged 3D information that the incremental estimation of Splat-Loc does not have. Furthermore, we examine two variants of our pose estimator: Splat-Loc-Glue, which utilizes LightGlue for feature matching; and Splat-LocSIFT, which utilizes SIFT for feature matching. 

In each scene, we run 10 trials (of 100 frames each) of each pose estimation algorithm. We evaluate the rotation error (R.E.) and translation error (T.E.) with respect to the ground-truth pose, the computation time (C.T.) per frame, and the overall success rate (S.R.). Here, success indicates the generation of a solution regardless of its quality. The performance of pose estimation algorithms often depends on the error associated with the initial estimate of the pose. As such, we test our system across a range of different errors in the initial estimate of the pose. In this study, we assume an initial estimate of the pose is available. We generate the initial estimate by taking the ground truth pose then applying a rotation _δR_ about a random axis and the translation _δt_ in a random direction. 

We provide the summary statistics of the error in the pose estimates computed by each algorithm, in addition to the computation time on a trial with 100 frames in the **Statues** scene in Table I. We note that all methods had a perfect success rate in this problem. The GS-Loc algorithm achieves the lowest accuracy and requires the greatest computation time, unlike Colored-ICP, Splat-Loc-SIFT, and Splat-Loc-Glue, which achieve much-higher accuracy with a rotation error less than a degree and a translation error less than 15cm. GS-Loc requires a computation time of about 36.15 s per frame, which is about two orders of magnitude slower than the next-slowest method ICP, which requires a computation time of about 110 ms. Colored-ICP, Splat-Loc-SIFT, and Splat-Loc-Glue require less than 100 ms of computation time. Compared to all methods, Splat-Loc-Glue yields pose estimates with the lowest mean rotation and translation error, less than 0 _._ 06 _[◦]_ and 4 mm, respectively, and achieves the fastest mean computation time, less than 42 ms. The computation time of Splat-Loc may be about a standard deviation greater during the first call, which may be due to the time spent loading the models and initializing the GPU kernels. 

Lastly, we examine the performance of the pose estimation algorithms in problems with a larger error in the initial estimate of the pose, with _δR_ = 30 _[◦]_ and _δt_ = 0 _._ 5 m in the 

TABLE I: Comparison of baseline pose estimation algorithms in simulation in the **Statues** scene with _δR_ = 20 _[◦]_ and _δt_ = 0 _._ 1 m. 

||Algorithm|R.E. (deg.)|T.E. (cm)|C.T. (msec.)|S.R. (%)|
|---|---|---|---|---|---|
||ICP [59]|73_._1_±_45_._9|129_±_75|107_±_19_._2|100|
||Colored-ICP [58]<br>Splat-Loc-SIFT (ours)<br>Splat-Loc-Glue (ours)|0_._83_±_0_._37<br>0_._09_±_0_._06<br>**0****_._05****_±_ 0****_._03**|1_._31_±_0_._60<br>0_._56_±_0_._75<br>**0****_._33****_±_ 0****_._27**|43_._3_±_9_._70<br>63_._3_±_2_._39<br>**41****_._2****_±_ 73****_._2**|100<br>100<br>100|
||GS-Loc [34, 35, 36]|122_±_33_._8|245_±_91_._2|36200_±_5440|100|



synthetic **Stonehenge** scene. We present the performance of each algorithm on each metric in Table II, where we note that ICP and Colored-ICP do not provide accurate estimates of the robot’s pose. Moreover, the pose estimation errors achieved by ICP and Colored-ICP have a significant variance. In contrast, Splat-Loc-SIFT and Splat-Loc-Glue yield pose estimates of high accuracy with average rotation and translation errors less than 0 _._ 5 deg. and 5mm, respectively. However, Splat-Loc-SIFT achieves a lower success rate, compared to Splat-Loc-Glue, which achieves a perfect success rate. 

TABLE II: Comparison of baseline pose estimation algorithms in the **Stonehenge** scene with _δR_ = 30 _[◦]_ and _δt_ = 0 _._ 5 m. 

||Algorithm<br>ICP [59]<br>Colored-ICP [58]|R.E. (deg.)<br>131_±_22_._6<br>94_._9_±_51_._3|T.E. (cm)<br>370_±_554<br>57_._4_±_28_._8|C.T. (msec.)<br>122_±_153<br>488_±_104|S.R. (%)<br>100<br>20|
|---|---|---|---|---|---|
||Splat-Loc-SIFT (ours)<br>Splat-Loc-Glue (ours)|**0****_._217****_±_ 0****_._0369**<br>0_._220_±_0_._203|0_._334_±_0_._0563<br>**0****_._315****_±_ 0****_._210**|139_±_3_._15<br>**45****_._1****_±_ 0****_._611**|70<br>100|



_3) Splat-Plan Evaluations:_ Splat-Plan is benchmarked against three different methods: a point-cloud planner [13], a sampling-based planner (RRT* using Proposition 1), and a NeRF-based planner (NeRF-Nav [7]). Furthermore, we perform ablations against variations of the point-cloud planner in order to expose flaws when planning against point clouds compared to the full scene geometry. For each simulation scene, we train a dense and sparse GSplat, totaling 8 scenes. In every scene, we run 100 start and goal locations distributed in a circle around the boundary of the scene. 

In the simulated tests, we represent the robot using balls of various sizes in order to generate interesting trajectories due to the fact that the simulated scenes are not trained in metric scale.[3] . Additional parameters, such as the number of Gaussians, can be found in Table III. 

TABLE III: Parameters across scenes for experiments. Number of Gaussians is reported for both dense and sparse variants of the same scene. 

||Radius|_Vmax_|_Amax_|Resolution|N. Gauss (K)|
|---|---|---|---|---|---|
|Stonehenge|0.01|0.1|0.1|1503|116_/_12|
|Statues|0.03|0.1|0.1|1003|201_/_18|
|Flight|0.02|0.1|0.1|1003|281_/_4|
|Old Union|0.01|0.1|0.1|1003|525_/_87|
|Maze|0.25|0.5|1.0|803|100|
|Maze (fast)|0.25|1.5|1.0|803|100|



While point cloud-based planners are ubiquitously used, they can sometimes fall short when the scene geometry is not dense 

> 3Nerfstudio adopts the NeRF conventions in scaling the scene to fit within the confines of a two-unit-length cube centered at the origin, with the poses of the camera residing within a [ _−_ 1 _,_ 1][3] -bounding box. We disable this feature for the hardware **Maze** scene. 

12 

or if the scene is very cluttered. To this end, we developed four variants of the Safe Flight Corridor (SFC) [13]. SFC-1 ingests the GSplat means as a point cloud, runs Dijkstra to retrieve a feasible initial path seed, creates collision sets with respect to the point cloud, synthesizes a polytope corridor that marginally intersects with the point cloud, and finally deflates the polytopes by the robot radius. These polytopes are fed to the same spline optimizer (7) that Splat-Plan uses. SFC-2 executes the same pipeline as SFC-1, but the point cloud representation is sampled from the surface of the ellipsoids. We sample 20 points from each ellipsoid in the scene to simulate a typical amount of points a Lidar or depth image would produce (approximately 2-5 million points). SFC-3 uses the Splat-Plan occupancy grid to retrieve a feasible path seed, while the means are still used to create polytopes. Finally, SFC-4 uses the SplatPlan occupancy grid, synthesizes polytopes using the means, but deflates the polytope by the robot radius and the maximum eigenvalue of the ellipsoid whose mean was used to create a particular halfspace in the polytope. These variants are all potential solutions to apply SFC to GSplat environments. We summarize the tradeoffs of all methods in Table IV. 

TABLE IV: Splat-Plan strikes a favorable tradeoff compared to existing methods in terms of safety, non-conservativeness (NC), smoothness, solution feasibility, and real-time execution. 

||Safe|NC|Smooth|Feasible|RT|Env.|
|---|---|---|---|---|---|---|
|NeRF-Nav|×|N/A|×|✓|×|NeRF|
|RRT*|×|×|×|✓|×|GS|
|SFC-1|×|✓|✓|×|✓|GS|
|SFC-2|×|✓|✓|×|✓|GS|
|SFC-3|×|✓|✓|×|✓|GS|
|SFC-4|×|×|✓|×|✓|GS|
|**Splat-Plan**|✓|✓|✓|✓|✓|GS|



Visually, the paths generated by Splat-Plan are smooth, safe, and non-conservative (Fig. 4). This fact is validated in Fig. 6, where Splat-Plan’s trajectories in blue are safe (minimum distances greater than 0 with respect to the GSplat collision geometry). Unfortunately, because many of these scenes were captured in the real-world, no ground-truth mesh exists. Moreover, we inspect the point cloud and mesh created by COLMAP and notice poor overall reconstruction of the collision geometry. Therefore, we elected to use the GSplat ellipsoidal geometry in place of the ground-truth geometry due to its high-quality approximation. 

Notice that these trajectories are non-conservative compared to the SFC methods (low path lengths and high polytope volume in Figs. 5 and 6). More importantly, we see that Splat-Plan never fails to return a trajectory, highlighted by the 0 failure rate. All other methods have failures, other than NeRF-Nav by virtue of it being an end-to-end optimization method. Finally, Splat-Plan has comparable execution times to SFC. Note that as SFC does not use GPU, we rewrote the codebase in Pytorch to yield comparable times to Splat-Plan. 

Finally, in terms of memory, we observe that in the scene with the most Gaussians ( **Old Union** ), GPU memory usage hovered around 3.1 GB, with the GSplat itself requiring 1.6 GB and the binary occupancy grid, 1.5GB. 

## _B. Hardware Results_ 

_1) Test Environment:_ We test Splat-Nav in the **Maze** scene using a drone. Images to train **Maze** were captured using the RGB camera onboard the drone. We utilize Nerfstudio [60] to train the Semantic GSplat, using its default parameters (which includes estimating the camera poses for each image frame from structure-from-motion via COLMAP [37]). In Figure 8, we show the true training images captured by the drone, the rendered RGB image from the GSplat at the same camera pose, and the semantic relevancy for the associated language query. First, we note that the rendered image is photorealistic, highlighting the remarkable visual quality of the trained Gaussian Splat. Second, the semantic relevancy spatially agrees with the expected location of the queried object, making the semantic field suitable for open-vocabulary goal querying. 

_2) Hardware:_ We test our pipeline on the Modal AI development drone platform measuring 29 cm x 20 cm x 10 cm (diagonal length of 36 _._ 6 cm). In the hardware tests, we approximate the robot using a sphere with diameter 0 _._ 5 m. Readers can find our test parameters in Table III. An OptiTrack motion capture system is solely used for evaluation purposes. Any other markers, such as ArUco tags, in the scene are purely cosmetic. 

_3) Implementation:_ We run the pose estimator and the planner ROS2 nodes on a desktop computer with an Nvidia RTX 4090 GPU and an Intel i9 13900K CPU, which communicates with the drone via WiFi. We emphasize that both modules are running asynchronously. At a frequency of about 3 Hz, the drone transmits images from its cameras and associated VIO poses to the desktop computer. Splat-Loc ingests the VIO _T_ ˆ _t_ ofposethe _T_ drone[ˆ] _t,_ 0 andbodythe imageafter applying _It_ to computerigid thebodyposetransformsestimate to transform the camera pose to the body frame. We run the estimator continuously, synchronized with the stream of images published from the drone via ROS2. 

The planning module ingests _T_[ˆ] _t_ as _x_ 0 and computes a safe trajectory for the drone to follow toward the languageconditioned goal _xf_ . The re-plan node, which runs Splat-Plan based on _x_ 0, updates the spline(s) _X_ ( _T_ ) as frequently as possible. The waypoint node, which operates asynchronously from the re-plan node, measures the running time since the _X_ ( _T_ ) was last updated and returns positions, velocities, acceleration, and jerk at this running time. The waypoint node runs at 10 Hz. This architecture allows the drone to continue following a smooth spline even when Splat-Plan is still computing the next plan. However, we find that simply sending position waypoints can cause the drone to jerk when _X_ ( _T_ ) is updated, as successive splines need not be close to one another. To rectify this issue, we forward integrate the waypoint velocities to get positions. Finally, these positions undergo[(][control] _[,t]_[)] _T_ gs( _X_ ( _T_ )) before being sent to the drone. Additionally, we run a Kalman Filter to smooth[(][control] _[,t]_[)] _T_ gs, as both the Splat-Loc and VIO pose estimates can be somewhat noisy. 

_4) Goal Specification:_ In the **Maze** , we specify the goal locations for the drone via natural language, comprising of the following objects: a keyboard, beachball, phonebook, and microwave (depicted in Figure 8). We query the semantic 

13 


![](1_survey/papers/md/Chen2024SplatNav_figs/Chen2024SplatNav.pdf-0013-01.png)


Fig. 4: Qualitative results of 100 safe trajectories using Splat-Plan with start (blue) and goal (red) states spread over a circle. We see that the trajectories are safe, but not conservative. 

Gaussian Splat for the location of these objects using the following text prompts: “keyboard,” “beachball,” “phonebook” and “microwave,” corresponding to these objects, without negative prompts. These objects are placed in locations that require dynamic motions, such as hard turns and elevation maneuvers, to reach. Moreover, all tests begin at the same position at hover, and the objects are positioned relative to this position so that they are not immediately visible when the drone first begins flight. 

_5) Control Schemes:_ Our hardware tests consist of three different control schemes, coined Open-loop, Closed-loop VIO, and Splat-Loc. Open-loop tests do not not re-plan, and therefore does not use Splat-Loc estimates. One trajectory is created at the start _T_ = 0, and the control node returns the corresponding waypoint at that point in time. No forward integration of the velocities is necessary since only one trajectory is ever created. Closed-loop VIO and Splat-Loc are re-planning control schemes where the re-plan node updates the trajectory _X_ ( _T_ ) as frequently as possible. Closed-loop VIO uses the VIO estimate as _x_ 0 and no additional transform is applied to the waypoint. Conversely, Splat-Loc uses the Splat-Loc pose estimate as _x_ 0, and the smoothed[(][control] _[,t]_[)] _T_ gs is applied to the Splat-Plan trajectories to transform them into the VIO control frame. Our hardware tests consist of all combinations of goal locations and control schemes. In addition, we run these combinations 10 times for statistical significance, yielding a total of 120 flights. 

_6) Splat-Loc Evaluations:_ We validate the performance of Splat-Loc in hardware experiments in the **Maze** scene, showing that Splat-Loc achieves relatively the same level of accuracy as the onboard VIO in estimating the drone’s pose, without 

requiring any special calibration or re-initialization procedures for frame alignment, which the onboard VIO requires. In Table V, we provide the rotation and translation errors of the Splat-Loc estimates, with the MOCAP poses as the groundtruth estimates. We note that Splat-Loc achieves rotation errors of about 3 deg and translation errors of about 4 cm, which is comparable to the accuracy of the VIO estimates, shown in Table VI. However, Splat-Loc failed in one of the closedloop trials with the “keyboard” goal location. As a result, the rotation and translation errors for this goal location is higher compared to the those of the other goal locations. The failure case is visualized in Figure 9, where the drone goes past the keyboard. We note that the failure likely occurred because the drone’s camera was pointing towards an area of the scene which was not really covered in the video used in training the GSplat. We discuss strategies for addressing such failure cases in Section VIII. In Figure 8, we show the estimated trajectories of the drone using MOCAP, the onboard VIO, and Splat-Loc, demonstrating the effectiveness of SplatLoc. Essentially, all the pose estimators achieve comparable estimation accuracy. However, unlike the MOCAP system, Splat-Loc does not require a specialized hardware system and is amenable to any monocular camera. Moreover, Splat-Loc runs at about 25 Hz on average, which is fast-enough for realtime operation. The bulk of the computation time is utilized in computing the feature matches and in solving the PnP problem, which requires about 10 milliseconds. 

_7) Splat-Plan Evaluations:_ Visualizations of 120 trajectories across four goal locations and three control schemes can be found in Fig. 9. Note that all flights were collision-free with 

14 


![](1_survey/papers/md/Chen2024SplatNav_figs/Chen2024SplatNav.pdf-0014-01.png)


Fig. 5: A comparison of trajectories generated by Splat-Plan and four variants of SFC [13] for the same 100 start and end locations for each scene (Stonehenge, Statues, Flightroom, and Old Union). Bars on the left represent trajectories planned using the dense scene, while the sparse scene is on the right. We evaluate the safety (Distance to GSplat and failure rate), conservativeness (path length and polytope volume), and computation time. We also show the distance of the polytope vertices to the GSplat to illustrate that Splat-Plan is sound. Violin plots showcase the spread of the minimum distance, path length, and polytope volume across all 100 trajectories, with markings indicating the mean. Splat-Plan displays competitive non-conservativeness and computation time, while exhibiting superior safety and success rates. 

TABLE V: Rotation Error (R.E.), Translation Error (T.E.), and the Success Rate (S.R.) of Splat-Loc with MOCAP as the ground-truth reference. 

|Goal|R.E.|(deg.)|T.E. (cm)|S.R.(%)|
|---|---|---|---|---|
|Beachball|2_._82|_±_0_._12|3_._93_±_0_._86|100|
|Keyboard<br>Microwave|5_._61 <br>2_._82|_±_3_._50<br>_±_0_._23|8_._14_±_0_._35<br>3_._59_±_0_._42|90<br>100|
|Phonebook|2_._83|_±_0_._25|3_._37_±_0_._95|100|



respect to the true scene except for one flight using Splat-Loc to navigate to the keyboard. The drone was oriented toward the edge of the scene, where features were few and the GSplat quality was poor. The poor quality can be attributed to the lack of training images pointing toward the edges of the scene, as we wanted to reconstruct the foreground in the highest quality. These qualitative results indicate that, within the confines of our controlled setting, all control schemes work equally well. 


![](1_survey/papers/md/Chen2024SplatNav_figs/Chen2024SplatNav.pdf-0014-06.png)


Fig. 6: A comparison of trajectories generated by Splat-Plan, SFC [13], RRT*, and NeRF-Nav [7]) for the same 100 start and end locations for each scene (Stonehenge, Statues, Flightroom, and Old Union). Bars on the left represent trajectories planned using the dense scene, while the sparse scene is on the right. We evaluate the safety (Distance to GSplat and failure rate), conservativeness (path length), and computation time. Violin plots showcase the spread of the minimum distance and path length across all 100 trajectories, with markings indicating the mean. Splat-Plan is safer than competing methods, relatively fast, non-conservative, and never fails across all 8 problem settings. 

TABLE VI: Rotation Error (R.E.), Translation Error (T.E.), and the Success Rate (S.R.) of VIO pose estimates with MOCAP as the ground-truth reference. 

||Goal|R.E.|(deg.)|T.E. (cm)|S.R.(%)|
|---|---|---|---|---|---|
||Beachball|2_._42|_±_0_._13|3_._87_±_0_._89|100|
||Keyboard|2_._36|_±_0_._27|3_._28_±_1_._20|100|
||Microwave|2_._36|_±_0_._14|4_._29_±_1_._30|100|
||Phonebook|2_._40|_±_0_._23|3_._63_±_1_._23|100|



These results are promising for Splat-Loc from a convenience point of view. We noticed that the VIO of the drone would drift in subsequent runs, necessitating the reinitialization of the VIO at the start of every run. In addition, as the VIO is not calibrated to be in the GSplat frame, we manually aligned the frames by zero-ing the VIO of the drone at the same position for all flights and for collection of training data. Meanwhile, Splat-Loc needed no such alignment, and was kept running continuously throughout all experiments without zero-ing (even 

15 


![](1_survey/papers/md/Chen2024SplatNav_figs/Chen2024SplatNav.pdf-0015-01.png)


Fig. 7: Natural language-specified goal locations in the **Maze** scene. The rendered RGB image from the GSplat demonstrate good reconstruction of the ground-truth. Additionally, the semantic relevancy spatially agrees with the provided language query. 

in control schemes that do not use Splat-Loc). 

Qualitatively, we see similar trends in Fig. 10. All control schemes are unsafe at different times, but in similar amounts. Note that some curves dip below 0, yet are verifiably safe in real-life. This is due to a variety of reasons, the most of prominent of which are: the difference in the set robot radius (0 _._ 25 cm) versus the true radius (0 _._ 18 cm), errors in aligning the motion capture frame into the frame of the GSplat (because the GSplat was not trained using motion capture), and the tracking capabilities of the drone. Note that the safety violation of all control schemes is relatively small compared to the size of the drone, which allows error in low-level tracking to obfuscate advantages of one method over another, especially in cluttered environments. 

_8) Fast Control:_ We stress test Splat-Plan by increasing _v_ max until the onboard VIO could no longer track the desired waypoint with enough accuracy to avoid collision, which was 1 _._ 5 m _/_ s. These speeds, coupled with the clutter in the environment, allowed for dynamic flight, which is visualized in the right column of Fig. 9. We point readers toward the associated videos hosted on our website (https://chengine.github. io/splatnav/) to better visualize the trajectories. 

_9) Closed-loop Endurance:_ Finally, we stress test the Splat-Loc re-planning pipeline through endurance flights. The 


![](1_survey/papers/md/Chen2024SplatNav_figs/Chen2024SplatNav.pdf-0015-07.png)


Fig. 8: Pose estimates of Splat-Nav using motion capture (green), onboard VIO (red), and Splat-Loc (blue). Splat-Loc gives comparable performance without requiring a manual frame alignment between the GSplat and a separate localization frame. 

pipeline is left to continually execute. Once the drone reaches a goal location, another goal location is set. We demonstrate collision-free flight over the order of minutes, which can again be visualized on our website (https://chengine.github. io/splatnav/). 

## VII. CONCLUSION 

We introduce an efficient navigation pipeline termed _Splat-Nav_ for robots operating in GSplat environments. Splat-Nav consists of a guaranteed-safe planning module _Splat-Plan_ , which allows for real-time planning ( _>_ 2 Hz) by leveraging the ellipsoidal representation inherent in GSplats for efficient collision-checking and safe corridor generation, facilitating real-time online replanning. Splat-Plan demonstrates superior performance in terms of conservativeness, safety, success rate and comparable computation times compared to point-cloud and NeRF methods on the same scene. Moreover, our proposed pose estimation module _Splat-Loc_ computes high-accuracy pose estimates faster (25 Hz) and more reliably compared to existing pose estimation algorithms for radiance fields, such as NeRFs. We present extensive hardware and simulation results, highlighting the effectiveness of Splat-Nav. 

## VIII. LIMITATIONS AND FUTURE WORK 

We only tested Splat-Nav in pre-constructed scenes. Existing GSplat SLAM algorithms do not run in real-time [36, 35], limiting the application of our method in online mapping. In future work, we seek to examine the derivation of real-time GSplat mapping methods, integrated with the planning and pose estimation algorithms proposed in this work. Additionally, the results from Section VI-A2 suggest that we can incorporate Splat-Loc as a localization module within online GSplat SLAM 

16 


![](1_survey/papers/md/Chen2024SplatNav_figs/Chen2024SplatNav.pdf-0016-01.png)


Fig. 9: Ground-truth trajectories of the drone navigating, projected onto the **Maze** GSplat. The drone is subjected to different goal locations and control schemes. The recorded flight trajectories are best viewed on our website https://chengine.github.io/splatnav/. 

algorithms to improve localization accuracy and the resulting map quality. 

We assumed that the pre-constructed scenes were correct. Safety of the planned trajectories depends on the quality of the underlying GSplat map. As noted in Remark 3, we can use different confidence levels of the ellipsoids to account for uncertainty in an object in the GSplat map. Splat-Plan cannot do anything if an obstacle is completely missing from the scene, which is a fundamental limitation of the GSplat map representation. Likewise, Splat-Plan could fail if the initialization graph-search procedure which utilizes Dijkstra fails to find a path to the goal, which could occur in maps with a coarse resolution. Future work will examine uncertainty quantification of different regions within a GSplat scene to aid the design of active-planning algorithms that enable a robot to collect additional observations in low-quality regions, such as areas with missing/non-existent geometry, while updating the GSplat scene representation via online mapping. 

We only tested Splat-Nav in a static scene. This could be a limitation in many practical problems. Using NeRFs and GSplat for dynamic environments remains an open area of research, especially in scenes without prerecorded motion [61, 62, 63]. Splat-Plan is fast enough to be extended easily to problems with dynamic scenes so long as the underlying dynamic GSplat representation is available. 

The performance of Splat-Loc depends on the presence of informative features in the scene. We can address this in two ways: through planning and by incorporating additional sensor data. Future work will explore the design of planning algorithms that bias the path towards feature-rich regions, improving localization accuracy during path execution. Future work will also incorporate IMU data to improve the robustness 

of the pose estimator, particularly in featureless regions of the scene where the PnP-RANSAC procedure might fail. 

Splat-Plan and Splat-Nav require loading the GSplat model onto the GPU, which takes up about 10 GB of GPU memory. Many drone platforms do not have the onboard compute resources to load the GSplat model, hindering onboard computation. Future work will seek to reduce the memory-usage demands of GSplat models, e.g., using sparse GSplat models. 


![](1_survey/papers/md/Chen2024SplatNav_figs/Chen2024SplatNav.pdf-0016-09.png)


This proposition was stated by [64] without proof. We provide the proof here. The goal is to diagonalize both Σ _a_ and Σ _b_ in such a way that they share the same eigenbasis. In this way, the matrix inversion amounts to a reciprocal of the eigenvalues. We can find such an eigenbasis through the generalized eigenvalue problem, which solves the following system of equations Σ _aϕi_ = _λi_ Σ _bϕi._ These generalized eigenvalues and eigenvectors satisfy the identity Σ _aϕ_ = Σ _bϕ_ Λ _._ 

To solve the generalized eigenvalue problem, we utilize the fact that Σ _a_ and Σ _b_ are symmetric, positive-definite, so the Cholesky decomposition of Σ _b_ = _LL[T]_ , where _L_ is lower triangular. This also means that we can represent Σ _a_ by construction as: Σ _a_ = _LCL[T]_ = _LV_ Λ _V[T] L[T] ,_ where _C_ is also symmetric, positive-definite, so its eigen-decomposition is _C_ = _V_ Λ _V[T]_ , where the eigenvectors _V_ are orthonormal _V[T] V_ = _I_ . To retrieve the original eigenbasis _ϕ_ , we solve the triangular system _L[T] ϕ_ = _V_ . A consequence of this solution is that: _V[T] V_ = _ϕ[T] LL[T] ϕ_ = _ϕ[T]_ Σ _bϕ_ = _I._ Moreover, this means that Σ _b_ = _ϕ[−][T] ϕ[−]_[1] . We can show that Λ and _ϕ_ indeed solve 

17 


![](1_survey/papers/md/Chen2024SplatNav_figs/Chen2024SplatNav.pdf-0017-01.png)


**----- Start of picture text -----**<br>
Open-loop Closed-loop VIO Splat-Loc<br>Keyboard Beachball<br>0.4 0.4<br>0.3 0.3<br>0.2<br>0.2<br>0.1<br>0.1<br>0.0<br>0.0<br>0.1<br>0 5 10 0 5 10 15<br>Phonebook Microwave<br>0.5<br>0.4<br>0.4<br>0.3 0.3<br>0.2 0.2<br>0.1 0.1<br>0.0 0.0<br>0.0 2.5 5.0 7.5 10.0 12.5 0 5 10 15<br>**----- End of picture text -----**<br>


Fig. 10: Distances (meters) of goal-conditioned trajectories to the Gaussian Splat as measured by the motion capture poses across three different control schemes. The abscissa represents time in seconds. The spread and the individual trajectories are visualized. 

the generalized eigenvalue problem through the following substitution: 


![](1_survey/papers/md/Chen2024SplatNav_figs/Chen2024SplatNav.pdf-0017-04.png)


where Λ = **diag** ( _λi_ ) is the diagonal matrix of eigenvalues. As a result, we can write the matrix inversion in Theorem 1 as the following: 


![](1_survey/papers/md/Chen2024SplatNav_figs/Chen2024SplatNav.pdf-0017-06.png)



![](1_survey/papers/md/Chen2024SplatNav_figs/Chen2024SplatNav.pdf-0017-07.png)


From Proposition 2, we know that we must find an _x_ such that _K_ ( _s_ ) _>_ 1 for all ellipsoids in the test set _G[∗]_ . We will approximate this safe set as a polytope. Given a test point _x[∗]_ and the _j_ th ellipsoid in the collision test set _G[∗]_ , we can use our collision test (Corollary 2) to derive these polytopes. Notice that _Ea_ represents the position of the robot (i.e., the mean is test point _µa_ = _x[∗]_ ). For any value of _s_ ¯ _∈_ (0 _,_ 1), the safety test is a quadratic constraint of the test point _x[∗]_ , namely ∆ _[T] j_[Σ] _[−] x[∗]_[1] _,j_[∆] _[j][>]_[1][,][where][we][omit][the][dependence][of][Σ][on] _[s]_ for brevity. 

To derive the supporting hyperplane for the safety check, we will first find the point on the ellipsoid and then linearize our test about this point. Let _fj_ ( _x_ ) = ( _x − µj_ ) _[T]_ Σ _[−] x[∗]_[1] _,j_[(] _[x][ −][µ][j]_[)] for any arbitrary _x_ . Note that _fj_ ( _x[∗]_ ) = ∆ _[T] j_[Σ] _x[−][∗]_[1] _,j_[∆] _[j]_[=] _[k] j_[2][.] We can immediately see that point _x_ 0 = _µj_ +[1+] _kj[ϵ]_[∆] _[j]_[will][be] outside of the ellipsoid for any _ϵ >_ 0 since: 


![](1_survey/papers/md/Chen2024SplatNav_figs/Chen2024SplatNav.pdf-0017-10.png)


Note that this point _x_ 0 lies on the ray starting from the center of the ellipsoid _µj_ and passing through the center of the robot at _x[∗]_ . We then linearize the constraint _fj_ ( _x_ ) about _x_ 0. Taking the derivative yields _[d] dx[f][j]_[(] _[x]_[)][=][2(] _[x][ −][µ][j]_[)] _[T]_[ Σ] _[−] x[∗]_[1] _,j_[.][The][linear] approximation of the constraint is then: 


![](1_survey/papers/md/Chen2024SplatNav_figs/Chen2024SplatNav.pdf-0017-12.png)


Plugging in _x_ 0 = _µj_ +[1+] _kj[ϵ]_[∆] _[j]_[and simplifying yields the given] expression ∆ _[T] j_[Σ] _[−] x[∗]_[1] _,j[x][ ≥]_[(1 +] _[ ϵ]_[)] _[k][j]_[+ ∆] _[T] j_[Σ] _[−] x[∗]_[1] _,j[µ][j]_[.] We need to also prove that the above constraint is a supporting hyperplane by showing that all feasible points when the constraint is equality is necessarily outside of the ellipsoid parametrized by Σ _[−] x[∗]_[1] _,j_[.][Recall][that] _[x]_[0][=] _[µ][j]_[+][∆] _kj[j]_ is a point both on the surface of the ellipsoid and on the hyperplane. Therefore, all feasible points on the hyperplane can be expressed as _x_ = _x_ 0 + _δ_ , where ∆ _[T] j_[Σ] _[−] x[∗]_[1] _,j[δ]_[=][0][.][If] the hyperplane supports the ellipsoid parametrized by Σ _[−] x[∗]_[1] _,j_[,] then necessarily _f_ ( _x_ ) = ( _x − µj_ ) _[T]_ Σ _[−] x[∗]_[1] _,j_[(] _[x][ −][µ][j]_[)] _[ ≥]_[1][.][For][all] points on the hyperplane, the ellipsoid constraint evaluates to 


![](1_survey/papers/md/Chen2024SplatNav_figs/Chen2024SplatNav.pdf-0017-14.png)


Hence, the constraint in Proposition 2 is a supporting hyperplane. 


![](1_survey/papers/md/Chen2024SplatNav_figs/Chen2024SplatNav.pdf-0017-16.png)


Our objective in this section is to show that the hyperplane created by Corollary 5 always contains the line segment _ℓ_ ( _t_ ) = _x_ 0 + _tδx_ for _t ∈_ [0 _,_ 1]. When the minimum unconstrained _t[∗]_ occurs outside _t ∈_ [0 _,_ 1], then necessarily the constrained minimum occurs at either of the two endpoints due to convexity of _K_ with respect to _t_ . Therefore, we consider the case where _t[∗] ∈_ (0 _,_ 1) and the case where _t[∗] ∈{_ 0 _,_ 1 _}_ . Let _x[∗]_ = _x_ 0 + _t[∗] δx_ . 

## _A. Optimum in the Interior_ 

Note that _t[∗]_ occurs when the normal of this ellipsoid Σ _[−]_[1] _x[∗] ,b_[(] _[x]_[0][+] _[t][∗][δ][x][−][µ]_[)][ is perpendicular to the direction of motion] 

18 

_δx_ . Given that _K_ ( _s[∗]_ ) _≥_ 1 (Corollary 2), Section B states that the point _x[∗]_ is safe and satisfies the hyperplane constraint 


![](1_survey/papers/md/Chen2024SplatNav_figs/Chen2024SplatNav.pdf-0018-02.png)


All points _x_ along the line can be parameterized as _x[∗]_ + _tδ_[˜] _x_ for _t_[˜] = _t − t[∗]_ , which due to orthogonality of _δx_ to the ellipsoid normal, yields 


![](1_survey/papers/md/Chen2024SplatNav_figs/Chen2024SplatNav.pdf-0018-04.png)


Therefore, the entire line segment is contained in the hyperplane and is not in collision. 

## _B. Optimum on the Boundary_ 

Boundary optima will not necessarily yield orthogonality of _δx_ with the normal of the ellipsoid Σ _[−] x[∗]_[1] _,j_[.][Without][loss] of generality, define _x[∗]_ = _x_ 0, which is the closest point on the line segment to the ellipsoid _Ej_ since the direction of the line segment can always be flipped to achieve this result. The unconstrainedˆ optima will occur at some point _x_ 0 + _tδ_[ˆ] _x_ , where _t <_ 0. Therefore, 


![](1_survey/papers/md/Chen2024SplatNav_figs/Chen2024SplatNav.pdf-0018-08.png)


Following the reasoning of Eq. (14), for all points on the line _x_ = _x[∗]_ + _tδx ∀ t ∈_ [0 _,_ 1], we have ( _x[∗] − µj_ ) _[T]_ Σ _[−] x[∗]_[1] _,j_[(] _[s][∗]_[)(] _[x][ −] µj_ ) _≥ kj[∗]_[.][Again,][in][this][case,][the][line][segment][still][remains] within the polytope. Hence, we have proven Corollary 5. 

## APPENDIX D 

## GLOBAL POSE INITIALIZATION OF SPLAT-LOC 

We evaluate the global point-cloud alignment initialization procedure from Section V when utilized by Splat-Loc-Glue, in the real-world scene Statues and synthetic scene Stonehenge, with the results in Table VII. We see that the success rate is 80% in both scenes, and it runs at approximately 20-30 Hz. When it does succeed, the pose errors are on the order of 0.3 deg and 1 cm. Although these estimates are relatively good, we note that these are less accurate than the recursive pose estimates discussed above. 

TABLE VII: Performance of the pose initialization module in Splat-Loc. 

|Scene|R.E.|(deg.)|T.E. (cm)|C.T. (msec.)|S.R. (%)|
|---|---|---|---|---|---|
|Statues|0_._37|_±_0_._72|1_._34_±_2_._33|33_._9_±_0_._57|80|
|Stonehenge|0_._21|_±_0_._21|0_._30_±_0_._23|45_._8_±_1_._70|80|



## REFERENCES 

- [1] A. Elfes, “Using occupancy grids for mobile robot perception and navigation,” _Computer_ , vol. 22, no. 6, pp. 46–57, Jun. 1989. 

- [2] H. Edelsbrunner, “Surface Reconstruction by Wrapping Finite Sets in Space,” in _Discrete and Computational Geometry: The Goodman-Pollack Festschrift_ , ser. Algorithms and Combinatorics, B. Aronov, S. Basu, J. Pach, and M. Sharir, Eds. Berlin, Heidelberg: Springer, 2003, pp. 379–404. 

- [3] P. Kim, J. Chen, and Y. K. Cho, “Slam-driven robotic mapping and registration of 3d point clouds,” _Automation in Construction_ , vol. 89, pp. 38–48, 2018. 

- [4] S. Osher and R. P. Fedkiw, _Level Set Methods and Dynamic Implicit Surfaces_ . New York: Springer, 2003. 

- [5] B. Mildenhall, P. P. Srinivasan, M. Tancik, J. T. Barron, R. Ramamoorthi, and R. Ng, “Nerf: Representing scenes as neural radiance fields for view synthesis,” in _European Conference on Computer Vision (ECCV)_ , 2020. 

- [6] B. Kerbl, G. Kopanas, T. Leimkuhler,¨ and G. Drettakis, “3D Gaussian splatting for real-time radiance field rendering,” _ACM Transactions on Graphics_ , vol. 42, no. 4, July 2023. [Online]. Available: https://repo-sam. inria.fr/fungraph/3d-gaussian-splatting/ 

- [7] M. Adamkiewicz, T. Chen, A. Caccavale, R. Gardner, P. Culbertson, J. Bohg, and M. Schwager, “Vision-only robot navigation in a neural radiance world,” _IEEE Robotics and Automation Letters (RA-L)_ , vol. 7, no. 2, pp. 4606–4613, 2022. 

- [8] S. LaValle, “Planning algorithms,” _Cambridge University Press google schola_ , vol. 2, pp. 3671–3678, 2006. 

- [9] L. E. Kavraki, P. Svestka, J.-C. Latombe, and M. H. Overmars, “Probabilistic roadmaps for path planning in high-dimensional configuration spaces,” _IEEE transactions on Robotics and Automation_ , vol. 12, no. 4, pp. 566–580, 1996. 

- [10] S. Karaman, M. R. Walter, A. Perez, E. Frazzoli, and S. Teller, “Anytime motion planning using the rrt,” in _2011 IEEE international conference on robotics and automation_ . IEEE, 2011, pp. 1478–1483. 

- [11] N. Ratliff, M. Zucker, J. A. Bagnell, and S. Srinivasa, “Chomp: Gradient optimization techniques for efficient motion planning,” in _2009 IEEE international conference on robotics and automation_ . IEEE, 2009, pp. 489–494. 

- [12] J. Schulman, Y. Duan, J. Ho, A. Lee, I. Awwal, H. Bradlow, J. Pan, S. Patil, K. Goldberg, and P. Abbeel, “Motion planning with sequential convex optimization and convex collision checking,” _The International Journal of Robotics Research_ , vol. 33, no. 9, pp. 1251–1270, 2014. 

- [13] S. Liu, M. Watterson, K. Mohta, K. Sun, S. Bhattacharya, C. J. Taylor, and V. Kumar, “Planning dynamically feasible trajectories for quadrotors using safe flight corridors in 3D complex environments,” _IEEE Robotics and Automation Letters (RA-L)_ , vol. 2, no. 3, pp. 1688– 1695, 2017. 

- [14] J. Van den Berg, M. Lin, and D. Manocha, “Reciprocal velocity obstacles for real-time multi-agent navigation,” 

19 

in _2008 IEEE international conference on robotics and automation_ . Ieee, 2008, pp. 1928–1935. 

- [15] X. Wu, S. Chen, K. Sreenath, and M. W. Mueller, “Perception-aware receding horizon trajectory planning for multicopters with visual-inertial odometry,” _IEEE Access_ , vol. 10, pp. 87 911–87 922, 2022. 

- [16] H. Oleynikova, Z. Taylor, M. Fehr, R. Siegwart, and J. Nieto, “Voxblox: Incremental 3D Euclidean signed distance fields for on-board MAV planning,” in _IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , 2017. 

- [17] L. Han, F. Gao, B. Zhou, and S. Shen, “Fiesta: Fast incremental euclidean distance fields for online motion planning of aerial robots,” _IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , pp. 4423–4430, 2019. 

- [18] K. Goel, W. Tabib, and N. Michael, “Rapid and highfidelity subsurface exploration with multiple aerial robots,” in _Experimental Robotics: The 17th International Symposium_ . Springer, 2021, pp. 436–448. 

- [19] K. Goel and W. Tabib, “Incremental multimodal surface mapping via self-organizing gaussian mixture models,” _IEEE Robotics and Automation Letters_ , vol. 8, no. 12, pp. 8358–8365, 2023. 

- [20] T. Chen, P. Culbertson, and M. Schwager, “Catnips: Collision avoidance through neural implicit probabilistic scenes,” _arXiv preprint arXiv:2302.12931_ , 2023. 

- [21] M. Tong, C. Dawson, and C. Fan, “Enforcing safety for vision-based controllers via control barrier functions and neural radiance fields,” in _IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2023, pp. 10 511–10 517. 

- [22] L. J. Guibas, R. Motwani, and P. Raghavan, “The robot localization problem,” _SIAM Journal on Computing_ , vol. 26, no. 4, pp. 1120–1138, 1997. 

- [23] A. Eman and H. Ramdane, “Mobile robot localization using extended kalman filter,” in _2020 3rd International Conference on Computer Applications & Information Security (ICCAIS)_ . IEEE, 2020, pp. 1–5. 

- [24] D. Fox, S. Thrun, W. Burgard, and F. Dellaert, “Particle filters for mobile robot localization,” in _Sequential Monte Carlo methods in practice_ . Springer, 2001, pp. 401–428. 

- [25] Q.-b. Zhang, P. Wang, and Z.-h. Chen, “An improved particle filter for mobile robot localization based on particle swarm optimization,” _Expert Systems with Applications_ , vol. 135, pp. 181–193, 2019. 

- [26] I. Ullah, Y. Shen, X. Su, C. Esposito, and C. Choi, “A localization based on unscented kalman filter and particle filter localization algorithms,” _IEEE Access_ , vol. 8, pp. 2233–2246, 2019. 

- [27] J. Biswas and M. Veloso, “Depth camera based indoor mobile robot localization and navigation,” in _2012 IEEE International Conference on Robotics and Automation_ . IEEE, 2012, pp. 1697–1702. 

- [28] P. Karkus, D. Hsu, and W. S. Lee, “Particle filter networks with application to visual localization,” in _Conference on robot learning_ . PMLR, 2018, pp. 169–178. 

- [29] R. Jonschkowski, D. Rastogi, and O. Brock, “Differen- 

tiable particle filters: End-to-end learning with algorithmic priors,” _arXiv preprint arXiv:1805.11122_ , 2018. 

- [30] L. Yen-Chen, P. Florence, J. T. Barron, A. Rodriguez, P. Isola, and T.-Y. Lin, “Inerf: Inverting neural radiance fields for pose estimation,” in _2021 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ . IEEE, 2021, pp. 1323–1330. 

- [31] D. Maggio, M. Abate, J. Shi, C. Mario, and L. Carlone, “Loc-nerf: Monte carlo localization using neural radiance fields,” in _IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 2023, pp. 4018–4025. 

- [32] Z. Zhu, S. Peng, V. Larsson, W. Xu, H. Bao, Z. Cui, M. R. Oswald, and M. Pollefeys, “Nice-SLAM: Neural implicit scalable encoding for SLAM,” in _IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)_ , June 2022. 

- [33] A. Rosinol, J. J. Leonard, and L. Carlone, “NeRFSLAM: Real-Time Dense Monocular SLAM with Neural Radiance Fields,” _arXiv preprint arXiv:2210.13641_ , 2022. 

- [34] C. Yan, D. Qu, D. Wang, D. Xu, Z. Wang, B. Zhao, and X. Li, “GS-SLAM: Dense visual slam with 3d gaussian splatting,” _arXiv preprint arXiv:2311.11700_ , 2023. 

- [35] V. Yugay, Y. Li, T. Gevers, and M. R. Oswald, “GaussianSLAM: Photo-realistic dense slam with gaussian splatting,” _arXiv preprint arXiv:2312.10070_ , 2023. 

- [36] H. Matsuki, R. Murai, P. H. Kelly, and A. J. Davison, “Gaussian splatting slam,” _arXiv preprint arXiv:2312.06741_ , 2023. 

- [37] J. L. Schonberger¨ and J.-M. Frahm, “Structure-frommotion revisited,” in _Conference on Computer Vision and Pattern Recognition (CVPR)_ , 2016. 

- [38] W. E. Lorensen and H. E. Cline, “Marching cubes: A high resolution 3d surface construction algorithm,” in _Seminal graphics: pioneering efforts that shaped the field_ , 1998, pp. 347–353. 

- [39] M. Qin, W. Li, J. Zhou, H. Wang, and H. Pfister, “Langsplat: 3d language gaussian splatting,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2024, pp. 20 051–20 060. 

- [40] S. Zhou, H. Chang, S. Jiang, Z. Fan, Z. Zhu, D. Xu, P. Chari, S. You, Z. Wang, and A. Kadambi, “Feature 3dgs: Supercharging 3d gaussian splatting to enable distilled feature fields,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2024, pp. 21 676–21 685. 

- [41] O. Shorinwa, J. Sun, and M. Schwager, “Fast-splat: Fast, ambiguity-free semantics transfer in gaussian splatting,” _arXiv preprint arXiv:2411.13753_ , 2024. 

- [42] A. Radford, J. W. Kim, C. Hallacy, A. Ramesh, G. Goh, S. Agarwal, G. Sastry, A. Askell, P. Mishkin, J. Clark _et al._ , “Learning transferable visual models from natural language supervision,” in _International Conference on Machine Learning (ICML)_ . PMLR, 2021, pp. 8748– 8763. 

- [43] M. Ji, R.-Z. Qiu, X. Zou, and X. Wang, “Graspsplats: Efficient manipulation with 3d feature splatting,” _arXiv preprint arXiv:2409.02084_ , 2024. 

- [44] O. Shorinwa, J. Tucker, A. Smith, A. Swann, T. Chen, 

20 

R. Firoozi, M. D. Kennedy, and M. Schwager, “Splatmover: Multi-stage, open-vocabulary robotic manipulation via editable gaussian splatting,” in _8th Annual Conference on Robot Learning_ , 2024. 

- [45] I. Gilitschenski and U. D. Hanebeck, “A robust computational test for overlap of two arbitrary-dimensional ellipsoids in fault-detection of kalman filters,” in _2012 15th International Conference on Information Fusion_ , 2012, pp. 396–401. 

- [46] E. G. Gilbert, D. W. Johnson, and S. S. Keerthi, “A fast procedure for computing the distance between complex objects in three-dimensional space,” _IEEE Journal on Robotics and Automation_ , vol. 4, no. 2, pp. 193–203, 1988. 

- [47] I. Gilitschenski and U. D. Hanebeck, “A robust computational test for overlap of two arbitrary-dimensional ellipsoids in fault-detection of kalman filters,” in _2012 15th International Conference on Information Fusion_ . IEEE, 2012, pp. 396–401. 

- [48] S. Ruan, K. L. Poblete, H. Wu, Q. Ma, and G. S. Chirikjian, “Efficient path planning in narrow passages for robots with ellipsoidal components,” _IEEE Transactions on Robotics_ , vol. 39, no. 1, pp. 110–127, 2022. 

- [49] Q. Wang, Z. Wang, M. Wang, J. Ji, Z. Han, T. Wu, R. Jin, Y. Gao, C. Xu, and F. Gao, “Fast iterative region inflation for computing large 2-d/3-d convex regions of obstacle-free space,” 2024. [Online]. Available: https://arxiv.org/abs/2403.02977 

- [50] P. J. Goulart and Y. Chen, “Clarabel: An interior-point solver for conic programs with quadratic objectives,” 2024. 

   - [58] J. Park, Q.-Y. Zhou, and V. Koltun, “Colored point cloud registration revisited,” in _Proceedings of the IEEE international conference on computer vision_ , 2017, pp. 143–152. 

   - [59] Y. Chen and G. Medioni, “Object modelling by registration of multiple range images,” _Image and vision computing_ , vol. 10, no. 3, pp. 145–155, 1992. 

   - [60] M. Tancik, E. Weber, R. Li, B. Yi, T. Wang, A. Kristoffersen, J. Austin, K. Salahi, A. Ahuja, D. McAllister, A. Kanazawa, and E. Ng, “Nerfstudio: A framework for neural radiance field development,” in _SIGGRAPH_ , 2023. 

   - [61] G. Wu, T. Yi, J. Fang, L. Xie, X. Zhang, W. Wei, W. Liu, Q. Tian, and X. Wang, “4d gaussian splatting for real-time dynamic scene rendering,” _arXiv preprint arXiv:2310.08528_ , 2023. 

   - [62] A. Pumarola, E. Corona, G. Pons-Moll, and F. MorenoNoguer, “D-nerf: Neural radiance fields for dynamic scenes,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2021, pp. 10 318–10 327. 

   - [63] C. Gao, A. Saraf, J. Kopf, and J.-B. Huang, “Dynamic view synthesis from dynamic monocular video,” in _Proceedings of the IEEE/CVF International Conference on Computer Vision_ , 2021, pp. 5712–5721. 

   - [64] N. A. (https://math.stackexchange.com/users/3060/nick alger), “Detect if two ellipses intersect,” Mathematics Stack Exchange, 2020, uRL:https://math.stackexchange.com/q/3678498 (version: 2021-05-09). [Online]. Available: https: //math.stackexchange.com/q/3678498 

- [51] L. De Branges, “The stone-weierstrass theorem,” _Proceedings of the American Mathematical Society_ , vol. 10, no. 5, pp. 822–824, 1959. 

- [52] D. DeTone, T. Malisiewicz, and A. Rabinovich, “Superpoint: Self-supervised interest point detection and description,” in _Proceedings of the IEEE conference on computer vision and pattern recognition workshops_ , 2018, pp. 224–236. 

- [53] P. Lindenberger, P. Sarlin, and M. Pollefeys, “Lightglue: Local feature matching at light speed. arxiv 2023,” _arXiv preprint arXiv:2306.13643_ , 2023. 

- [54] S. F. Bhat, R. Birkl, D. Wofk, P. Wonka, and M. Muller,¨ “Zoedepth: Zero-shot transfer by combining relative and metric depth,” _arXiv preprint arXiv:2302.12288_ , 2023. 

- [55] L. Yang, B. Kang, Z. Huang, X. Xu, J. Feng, and H. Zhao, “Depth anything: Unleashing the power of largescale unlabeled data,” in _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_ , 2024, pp. 10 371–10 381. 

- [56] S. Umeyama, “Least-squares estimation of transformation parameters between two point patterns,” _IEEE Transactions on Pattern Analysis & Machine Intelligence_ , vol. 13, no. 04, pp. 376–380, 1991. 

- [57] R. B. Rusu, N. Blodow, and M. Beetz, “Fast point feature histograms (fpfh) for 3d registration,” in _2009 IEEE international conference on robotics and automation_ . IEEE, 2009, pp. 3212–3217. 

