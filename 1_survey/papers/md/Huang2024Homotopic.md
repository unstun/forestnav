---
citation_key: Huang2024Homotopic
arxiv_id: 2406.02885
arxiv_url: "https://arxiv.org/abs/2406.02885"
title: "Homotopic Path Set Planning for Robot Manipulation and Navigation"
authors_short: "Jing Huang et al."
year: 2024
direction_tag: J_homotopy_topology
source: pymupdf4llm
converted_at: 2026-06-23T19:10:03Z
origin: ai+web
reviewed: false
---

This paper has been accepted for publication at Robotics: Science and Systems, 2024. Please cite the paper as: J. Huang, Y. Tang, and K. W. Samuel Au, 

“Homotopic path set planning for robot manipulation and navigation,” Robotics: Science and Systems, 2024. 

# Homotopic Path Set Planning for Robot Manipulation and Navigation 

Jing Huang[1] _[,]_[2] , Yunxi Tang[1] , and Kwok Wai Samuel Au[1] _[,]_[2] 

> 1Department of Mechanical and Automation Engineering, The Chinese University of Hong Kong 

> 2Multi-Scale Medical Robotics Center, Hong Kong SAR Email: _{_ huangjing, yxtang _}_ @mae.cuhk.edu.hk, samuelau@cuhk.edu.hk 

_**Abstract**_ **—This paper addresses path set planning that yields important applications in robot manipulation and navigation such as path generation for deformable object keypoints and swarms. A path set refers to the collection of finite agent paths to represent the overall spatial path of a group of keypoints or a swarm, whose collective properties meet spatial and topological constraints. As opposed to planning a single path, simultaneously planning multiple paths with constraints poses nontrivial challenges in complex environments. This paper presents a systematic planning pipeline for homotopic path sets, a widely applicable path set class in robotics. An extended visibility check condition is first proposed to attain a sparse passage distribution amidst dense obstacles. Passage-aware optimal path planning compatible with sampling-based planners is then designed for single path planning with adjustable costs. Large accessible free space for path set accommodation can be achieved by the planned path while having a sufficiently short path length. After specifying the homotopic properties of path sets, path set generation based on deformable path transfer is proposed in an efficient centralized manner. The effectiveness of these methods is validated by extensive simulated and experimental results.** 

## I. INTRODUCTION 

Simultaneously generating paths for multiple agents finds vast applications in robotics. For instance, planning multiple robots’ paths with certain collective properties has been extensively studied in multi-robot navigation tasks like surveillance, formation flight, and collaborative transport [1]-[4]. Manipulative tasks also demonstrate similar needs. Particularly, robotic deformable object manipulation (DOM) remains challenging today. One core reason is that widely populated constrained environments in reality make DOM far more complicated beyond pure control approaches [6], [7] and entail planning [8], [9]. The reliance on models or simulations renders deformation planning not easily applicable. An effective alternative is directly planning spatial paths for deformable objects (DOs). Considering DO keypoints provides a tractable way to depict the object states [5]. Analogous to multi-robot paths, keypoint paths should be specified coordinately. For consistency, a path set here refers to the collection of paths for a robot team or object keypoints. 

In comparison to path set planning, multi-trajectory planning is more commonly studied in multi-robot systems to impose time-dependent constraints. Usually cast to spatiotemporally constrained optimization problems, multi-trajectory planning poses high complexity. In contrast, path set planning decouples time to make a more basic and tractable problem. 


![](1_survey/papers/md/Huang2024Homotopic_figs/Huang2024Homotopic.pdf-0001-11.png)


Fig. 1. Block diagram illustrating the overall workflow and main modules in the proposed path set planning pipeline. Blocks in the bottom row are the key components of corresponding modules. 

Planned spatial paths can be converted to trajectories readily. This paper addresses path set planning, in particular a general class of homotopic path sets, and presents a systematic planning pipeline as shown in Fig. 1. In obstacle-dense environments, the obstacle distribution is first perceived by identifying valid passages that constrain agent motions. A novel passage identification criterion is proposed which drastically reduces the number of passages and subsequent computations over the original visibility condition. Then, passage-aware optimal path planning is utilized to find a single path trading off classical objectives, e.g., the path length, and free space along the path to accommodate multiple paths. After analyzing the feasible topological properties of path sets, a deformable path-transfer scheme is designed to efficiently generate coordinated path sets from a single agent path. 

A recently reported study on path set planning in [5] only adopts DOM setups. In navigation, the concept of virtual tube in [2], [3] shows similarity to path sets in that it contains homotopic swarm trajectories, but standard planners and heavy optimization are relied on to attain trajectories. This paper extends and completes path set planning via a systematic and thorough investigation of core modules of the pipeline. The key contributions can be summarized as 

- 1) A general passage check condition to detect sparse passage distributions in environments. It reduces the passage number dramatically over pure visibility check and helps save computations in planning stages. 

- 2) New cost forms in passage-aware optimal path planning for adjustable planning results. Planners are enabled to optimally trade off path’s accessible free space and length over conventional clearance-based methods. 

- 3) Further refined path transfer procedure to better guarantee 

transferred paths’ feasibility and coordination. Path sets can be generated much more efficiently than approaches of separately planning. 

Additionally, we demonstrate extensive simulation and experimental results as well as practical robotic applications to reveal the generality and applicability of our proposals. 

## II. RELATED WORK 

The related work draws equally from manipulation planning, mostly DOM planning, and multi-robot path planning literature. While DOs usually do not permit easily attainable state representations, a feasible path connecting the initial and target DO states can be planned with explicit deformation models. The DO state is usually characterized by extracted geometrical or topological properties. A survey on modelbased DOM planning can be found in [8]. Models include the elasticity model [10], the mass-spring model [11], minimalenergy curves for deformable linear objects (DLOs) [12], to determine valid intermediate states, namely samples. Standard planning algorithms, e.g., Probabilistic Roadmap (PRM) and Rapidly-exploring Random Tree (RRT), are utilized to attain a path to the target state. Most works are DO/task-specific, e.g., DLOs, planar DOs, and clothes [13], [14], or ad-hoc elemental action paradigms like folding and bending [15]. The reliance on models or simulations severely hinders the utility of modelbased planning in practice. 

More relevant to this work is spatial DO path planning for a feasible path connecting initial and target DO configurations in complex environments. Using sampling-based planners, a nominal feasible path can be achieved with models/simulations [16], [17]. For better practicality, DO state prediction, motion planning, and control are interleaved in [18]. An increasing number of approaches unleash the potential of learning methods in DOM planning. In [19], the reliability of planned stateaction pairs is enforced by learning a classifier of more reliably feasible state-pairs. The imagined plan, i.e., a sequence of images to the desired goal, is attained by learning a causal InfoGAN [20] of the deformation dynamics and planning in the latent space in [21]. More recently, path sets of feedback points are leveraged as DO motion references in DOM [5], but path set generation and passage processing are simplified, leading to restrictive generality. 

Multi-robot path planning is a basic problem when multiple robots are present and has received substantial research in the robotics and AI community, formally named the multi-agent path finding (MAPF) problem. It aims to find feasible paths for all agents while optimizing objectives of the makespan or the sum of individual path costs [22], [23]. Numerous MAPF algorithms are proposed on common abstractions like ignoring agents’ kinematics constraints and using discrete grid graphs. Despite the NP-hardness of MAPF [24], sub-optimal solvers, including search-based solvers like hierarchical cooperative A _[∗]_ and its variants [25], [26] as well as rule-based solvers [27], can quickly find all agent paths. Some optimal solvers reduce the problem to standard and more tractable ones, e.g., integer linear programming [28], answer set programming [29] and satisfiability solving [30]. M _[∗]_ dynamically changes the 

dimensionality and branching factors upon detected conflicts [31]. Conflict-based search adopts a two-level structure to enable fewer state examinations [32]. Other methods such as increasing cost tree search [33] also exist and a comprehensive survey on MAPF is available in [22]. 

In robotics, realistic conditions in ground and aerial swarms usually render the above methods less applicable. Trajectory planning, optimization, and local motion planning are often jointly considered [1]-[4]. Mix-integer quadratic optimization is formulated for multiple trajectories passing specified intermediate waypoints [34]. Discretized linear temporal logic is employed to depict robot groups’ desired behaviors and trajectories are solved as a problem of satisfiability modulo theories [35]. An important alternative for global path planning is sampling-based methods that define the path by a set of safe team configurations. For instance, PRM is used for team formation in [36], [37]. Sampling-based strategies in multirobot path planning usually need to compute cell decomposition of environments to recognize traversable areas [1], [38]. Recently in [2], [3], the virtual tube is proposed to generate infinite homotopic optimal trajectories efficiently via convex combinations of several optimal vertex trajectories. The tube’s topological properties are decided by vertex paths found by RRT _[∗]_ (optimal RRT) that minimize the path length, but tube’s accessible free space is not optimized. 

## III. PASSAGE DETECTION AND PASSAGE-AWARE OPTIMAL PATH PLANNING 

This section elaborates on prerequisites for path set planning. After a brief problem statement, the extended visibility check condition in passage detection is proposed. Passageaware optimal path planning is then presented. 

## _A. Homotopic Path Set Planning Problem_ 

Consider a team of _K_ agents _S_ = [ **s**[T] 1 _[, ...,]_ **[ s]**[T] _K_[]][T][ with] **[ s]** _[i][∈]_[R][3] denoting the _i_ -th agent’s position. In manipulation, the team can be the group of keypoints picked on DOs for deformation description. The _path set_ , i.e., the collection of agent paths, is employed as the path embodiment of the team. Given the initial _S_ 0 = [ **s**[T] 0 _,_ 1 _[, ...,]_ **[ s]**[T] 0 _,K_[]][T][and][target] _[S][d]_[=][[] **[s]**[T] _d,_ 1 _[, ...,]_ **[ s]**[T] _d,K_[]][T][,] the aim is to find the path set to encode the team’s spatial path in complex obstacle-dense environments. Apart from individual path’s properties, the path set needs to fulfill certain constraints as a whole. In particular, we target homotopic path sets in which all paths are homotopic. Denote _σi_ the path of **s** _i_ , then the path set Σ _S_ satisfies 


![](1_survey/papers/md/Huang2024Homotopic_figs/Huang2024Homotopic.pdf-0002-12.png)


where _H_ ( _·_ ) checks path homotopy. Meanwhile, Σ _S_ is required to occupy a large free space in complex environments for multiple path accommodation and have short paths as detailed later. Intuitively, homotopic path sets do not allow agents to be split apart by obstacles, a widely applicable homotopy path class in DOM [5] and robot navigation [1], [39], [40], and are also readily extendable to general cases by allowing multiple homotopic path sets [3], [41]. 


![](1_survey/papers/md/Huang2024Homotopic_figs/Huang2024Homotopic.pdf-0003-00.png)


Fig. 2. For simplicity, segments connecting obstacle side centers represent passages formed by two obstacles here. All passages pass the visibility check, but only black ones are useful in free space determination. 

## _B. Extended Visibility Check in Passage Detection_ 

Narrow space easily causes collisions in team motion and manipulation. Thus, sufficient free space along the path set represents a fundamental requirement. As paths are homotopic, it suffices to resort to one agent path for a large free space. An effective way to gauge accessible free space along a path is by checking traversed passages. Unlike passage detection based on computationally intensive bridge tests [42], [43], obstacle distribution is exploited for fast detection. Assume obstacles are separate polyhedrons _Ei_ ( _i_ = 1 _, ..., M_ ). Each ordered pair _Ei, Ej_ ( _i < j_ ) forms a generic passage denoted as ( _Ei, Ej_ ). A total of ( _[M]_ 2[)][such][passages][exist,][but][not][all][are][physically] valid. The pruning strategy of visibility check is used in [5]. ( _Ei, Ej_ ) is classified as valid only if the passage segment is collision-free with other obstacles. Though visually invalid passages are excluded, a significant downside is that it leaves a large fraction of passages invalid for free space determination in obstacle-dense environments, e.g., Fig. 2. Redundant passages will incur a large computational load in following passage-related procedures in path set planning. To address this, an extended visibility check condition is proposed here to enable a thorough passage check. The shortest segment between obstacles is leveraged as a compact representation of the passage, i.e., 


![](1_survey/papers/md/Huang2024Homotopic_figs/Huang2024Homotopic.pdf-0003-04.png)


where _l_ ( _·_ ) _⊂_ R[3] is the segment connecting two points. In pure visibility check, _V_ ( _Ei, Ej, Ek_ ) returns true if ( _Ei, Ej_ ) is not occluded by _Ek_ and false otherwise 


![](1_survey/papers/md/Huang2024Homotopic_figs/Huang2024Homotopic.pdf-0003-06.png)


( _Ei, Ej_ ) is evaluated as a passage if _V_ ( _Ei, Ej, Ek_ ) is true for all _Ek, k_ = _i, j_ . This condition, however, is overly restrictive to filter out invalid passages. For instance, ( _E_ 2 _, E_ 4) in Fig. 2 is marked as a passage under the visibility criterion. Nonetheless, suppose an agent with a certain volume is passing ( _E_ 2 _, E_ 4), its motion is more directly restricted by nearby obstacles _E_ 3 and _E_ 8 in passages ( _E_ 2 _, E_ 3) and ( _E_ 3 _, E_ 8). 

Taking the perspective of an agent with isotropic motion directions, ( _Ei, Ej_ ) constrains the agent in a circular area _Ri,j_ . 


![](1_survey/papers/md/Huang2024Homotopic_figs/Huang2024Homotopic.pdf-0003-09.png)


Fig. 3. ( _E_ 1 _, E_ 4) will pass the original visibility check, but cannot pass the extended variant because both _E_ 3 and _E_ 6 intersect _R_ 1 _,_ 3. 

The region center **o** _i,j_ coincides with the passage center and the diameter 2 _ri,j_ equals the passage width _∥_ ( _Ei, Ej_ ) _∥_ 2. If any other _Ek_ intersects _Ri,j_ , the free space shrinks as exemplified in Fig. 3 for a drone. ( _Ei, Ej_ ) should be classified as invalid since the agent is more directly confined by _Ek_ when it is in ( _Ei, Ej_ ). This criterion naturally involves the original visibility condition as an extended variant and can be expressed as 


![](1_survey/papers/md/Huang2024Homotopic_figs/Huang2024Homotopic.pdf-0003-12.png)


This infers that an agent in cluttered environments is more likely to be blocked by obstacles in its vicinity than obstacles forming the generic passage it is traversing. (4) can also be interpreted by Voronoi diagrams that partition the environment by clearance to obstacles [44], [45], [46]. Specifically, (4) imposes that ( _Ei, Ej_ ) is valid if it only goes through the Voronoi cells associated with _Ei_ and _Ej_ . In this way, redundant passages are thoroughly excluded, which helps save computations in following passage-related procedures. In 3D maps, passage detection can be performed in height intervals determined by obstacles to maintain a sparse passage structure. 

## _C. Passage-Aware Optimal Path Planning_ 

Passage determination preprocesses the environment before path planning. For each **s** _i ∈ S_ , the path from its start **s** 0 _,i_ to the target **s** _d,i_ optimizing a user-defined cost function is obtainable by optimal planers such as sampling-based methods [47]-[49]. Formally, a feasible path is a continuous function _σ_ : [0 _,_ 1] _�→Xfree_ where _Xfree_ is the obstacle-free configuration space. The path argument _τ ∈_ [0 _,_ 1] is given by path length parameterization by default. As aforementioned, apart from the typical criterion of path length, one core requirement for an agent path is to optimize the accessible free space for the path set. The passages passed by _σ_ from the start _σ_ (0) to _σ_ ( _τ_ ) are stored in an ordered list _Pσ_ ( _τ_ ) = _{_ ( _Ei, Ej_ ) _, ...,_ ( _Ep, Eq_ ) _}_ . _Pσ_ ( _τ, i_ ) indexes the _i_ -th passage in _Pσ_ ( _τ_ ). min _∥Pσ_ ( _τ_ ) _∥_ 2 returns the minimum passage width in _Pσ_ ( _τ_ ). 

Optimal planners asymptotically find the path that optimizes some properly defined cost. A well-formulated cost is therefore essential to depict the aforementioned planning requirements. However, it is not straightforward since these requirements may be inconsistent and conflicting. A path minimizing the path length need not have sufficient free space along it and vice versa. The cost to trade off them in [5] is 

_f_ ( _σ_ ) = Len( _σ_ ) _/fP_ ( _σ_ ) (5) 

**Algorithm 1:** Update Cost of **s** _new_ in A New Edge 

**Algorithm 2:** RRT _[∗]_ -Based Passage-Aware Optimal Path Planning 

|**1** Input **s**_near ∈Snear,_**s**_new, Pvalid, E_;<br>**2 foreach** (_Ei, Ej_)_∈Pvalid_ **do**<br>**3**<br>**if** _edge_(**s**_near,_**s**_new_) passes (_Ei, Ej_) **then**<br>**4**<br>_σ′ ←σ∗_<br>_near ∗edge_(**s**_near,_**s**_new_);<br>**5**<br>Compute _f_(_σ′_)_, fP_(_σ′_);<br>**if** _f_(_σtemp_)_< f_(_σ∗_<br>_new_) **then**<br>**6**<br>Update _f_(_σ∗_<br>_new_)_, fP_ (_σ∗_<br>_new_) as values of _σ′_;<br>**7**<br>Update _fcur_(**s**_new_) and parent of **s**_new_;<br>**8**<br>_E ←_(_E \ {edge_(**s**_parent,_**s**_new_)_}_) _∪_<br>_{edge_(**s**_near,_**s**_new_)_}_;<br>where Len(_σ_)is the path length._fP_(_σ_) = min_∥Pσ_(1)_∥_2is the<br>minimum passage width passed by_σ_. Proportional comparison<br>between Len(_σ_) and _fP_(_σ_) is adopted in (5). The composite<br>ttdtiiiththlthhiliiith|Path Planning|
|---|---|
||**1** _Pvalid ←_<br>ExtendedVisibilityCheck(_E_1_, ..., EM_);<br>**2** _V ←{_**s**_init}_; _E ←∅_;<br>**3 for** _i_= 1_,_2_, ..., N_ **do**<br>**4**<br>**s**_rand ←_SampleFree(_δ_);<br>**5**<br>**s**_nearest ←_Nearest(_G_= (_V, E_)_,_**s**_rand_);<br>**6**<br>**s**_new ←_Steer(**s**_nearest,_**s**_rand_);<br>**7**<br>**if** ObstacleFree(**s**_nearest,_**s**_new_) **then**<br>**8**<br>_Snear ←_Near(_G_= (_V, E_)_,_**s**_new, rnear_);<br>**9**<br>_V ←V ∪{_**s**_new}_;<br>**10**<br>**s**_min ←_GetParent(_Snear,_**s**_new, Pvalid_);<br>**11**<br>_E ←E ∪{edge_(**s**_min,_**s**_new_)_}_;<br>**12**<br>Rewire(_G_=<br>(_V, E_)_, Snear,_**s**_min,_**s**_new, Pvalid_);<br>**13 return** _G_= (_V, E_);|



where Len( _σ_ ) is the path length. _fP_ ( _σ_ ) = min _∥Pσ_ (1) _∥_ 2 is the minimum passage width passed by _σ_ . Proportional comparison between Len( _σ_ ) and _fP_ ( _σ_ ) is adopted in (5). The composite cost tends to minimize the path length while maximizing the minimum passage width the path passes. 

Terms’ priorities in (5) are fixed. Adjustable costs are more desirable to enable different path preferences considering the free space requirement varies with problem setups such as the team size and the obstacle density. A weighted cost structure is introduced herein as 

## _A. Feasibility Requirement for Path Sets in Homotopy_ 

For the feasibility of the path set Σ _S_ as a collection, paths’ homotopic interrelationships are analyzed. In general nonwinding scenarios where agents do not wrap around obstacles, the homotopy constraint is imposed on paths. _σ_ 1 _, σ_ 2 with identical initial and final positions are path homotopic if there exists a continuous function, i.e., the homotopy, _ψ_ ( _·_ ) : [0 _,_ 1] _�→_ Σ _free_ , where Σ _free_ is the set of paths in _Xfree_ , such that _ψ_ (0) = _σ_ 1 _, ψ_ (1) = _σ_ 2 and _ψ_ ( _x_ ) _∈_ Σ _free, ∀ x ∈_ [0 _,_ 1]. Homotopic paths essentially can continuously deform to one another in _Xfree_ but are not easily verifiable in general. For easy verifiability and good generality, straight-line homotopy is imposed on paths. If _σ_ 1 _, σ_ 2 are path homotopic, their straight-line homotopy is 


![](1_survey/papers/md/Huang2024Homotopic_figs/Huang2024Homotopic.pdf-0004-07.png)


where _kP >_ 0 acts as the weight of _fP_ ( _σ_ ) that determines the importance of _f_ ( _σ_ ). Intuitively, the passage width is converted into a generalized and weighted path length subtracted from the true path length in (6). By taking different _kP_ , the dominance between Len( _σ_ ) and _fP_ changes. _kP_ selection is problem-specific. In most scenarios, _∥Pσ_ (1) _∥_ 2 is significantly smaller than Len( _σ_ ), _kP_ should not be too small to bring out the effect of _fP_ ( _σ_ ) in the cost. 

The cost formulations (6) are monotonic under path concatenation (Len( _·_ ) is monotonically increasing, _fP_ ( _·_ ) is monotonically non-increasing) and bounded. Therefore, samplingbased optimal planners are guaranteed to find the optimal path asymptotically [48] and RRT _[∗]_ is taken in our implementation. Denote _σnew[∗]_[the][optimal][path][from][the][start] **[s]** _[init]_[to][the][new] sample **s** _new_ . **s** _new_ carries attributes of _f_ ( _σnew[∗]_[)][,] _[f][P]_[(] _[σ] new[∗]_[)] and _fcur_ ( **s** _new_ ), the passage width passed by the edge from the parent node to **s** _new_ . _fP_ ( _σnew[∗]_[)][and] _[f][cur]_[(] **[s]** _[new]_[)][are][initialized] as large values to indicate no passing of passages. To iteratively find _σnew[∗]_[,][passage][passing][is][checked][in][every][attempt] to add the edge between **s** _new_ and a near node **s** _near_ . Attributes are updated accordingly (see Algorithm 1). This procedure is invoked when finding the parent node and rewiring the tree, i.e., GetParent() and Rewire(). See Algorithm 2 for passage-aware optimal path planning for a single path that integrates the extended visibility check for passage detection and the new cost formulation. 


![](1_survey/papers/md/Huang2024Homotopic_figs/Huang2024Homotopic.pdf-0004-10.png)


_σ_ 1 _, σ_ 2 are said to be strong path homotopic if _ψ_ 1 _,_ 2( _x, τ_ ) _∈ Xfree_ always holds, indicating that the hypersurface swept by _ψ_ 1 _,_ 2( _x, τ_ ) lies in _Xfree_ . We do not construct strictly homotopic paths with the same endpoints as in [50]. _σi, σj ∈_ Σ _S_ are said to be strong path homotopic-like if their straight-line homotopy in (7) remains in Σ _free_ . 

Any pair of paths in Σ _S_ are required to be strong path homotopic-like as in [5], equivalent to the uniform visibility condition for quadrotor paths [39], [40], line of sight [50], and visibility deformation of roadmaps [41]. Since agents are not separated by obstacles, paths are homotopic to transform into each other, which is hard to check in high-dimensional spaces. The strong homotopic-like condition is easy to check, although it can be overly constrained in 3D space to exclude feasible situations where paths round obstacles like Fig. 4. This can be further checked by examining if the straight-line homotopy passes the entire obstacle top part. 

## IV. PATH SET HOMOTOPY AND PATH TRANSFER 

This section first discusses the feasibility requirements for path sets regarding paths’ homotopic properties. Path transfer is then introduced as the basic primitive for path set generation. 

## _B. Path Transfer_ 

Generating Σ _S_ by planning each agent path in a decentralized fashion is complex due to the homotopy constraint. 


![](1_survey/papers/md/Huang2024Homotopic_figs/Huang2024Homotopic.pdf-0005-00.png)


Fig. 4. In the left 2D case, DO point path 1 and 2 are not homotopic and thus infeasible. In the right 3D case, though path 1 and 2 are not strong path homotopic-like, the shown DO pose is feasible. 

Coordination among paths is also hard to achieve. Paths in a homotopic path set share an identical passage passing list in 2D, i.e., _Pσi_ = _Pσj , ∀ σi, σj ∈_ Σ _S_ , or have limited differences in 3D. Therefore, if one path in Σ _S_ is planned, other paths can be generated by transferring from it. This flow fulfills homotopy by construction and is computationally efficient. _S_ 0 and _Sd_ are essentially two clusters with different agent distributions. A path set from _S_ 0 to _Sd_ connects the two clusters while meeting the above constraints. Suppose **s** _p ∈ S_ has a planned path _σp_ from **s** 0 _,p_ to **s** _d,p_ , then for each point **s** _i ∈ S_ , the path transferred from _σp_ is 


![](1_survey/papers/md/Huang2024Homotopic_figs/Huang2024Homotopic.pdf-0005-03.png)


where a general path transfer form is utilized compared to [5]. It permits different path arguments in _σp_ , _σt,i_ , and a varying transfer vector to enable more flexible transfer. 

The planned path _σp_ in path transfer is conceptually similar to the generator curve in [3]. The corresponding agent, termed _pivot_ , can be picked arbitrarily since following transfer procedures are invariant to pivot. Designate _p_ the chosen pivot index. The pivot path _σp_ is found by the passage-aware optimal path planner. When transferring _σp_ to other agents, forward and backward transfer are proposed in [5] by assigning **v** _p→i_ as **v** 0 _,p→i_ = **s** 0 _,i −_ **s** 0 _,p_ and **v** _d,p→i_ = **s** _d,i −_ **s** _d,p_ , respectively, where extra postprocessing of path concatenation is required. To resolve this, these two transfer paradigms are combined in (8) to be 


![](1_survey/papers/md/Huang2024Homotopic_figs/Huang2024Homotopic.pdf-0005-06.png)


where _τi_ = _τp_ = _τ_ , **v** 0 _,p→i_ and **v** _d,p→i_ are linearly interpolated to compose a varying transfer vector along _σt,i_ . In this way, _σt,i_ (0) = **s** 0 _,i_ , _σt,i_ (1) = **s** _d,i_ with no need for path postprocessing. Performing (9) for each agent in _S_ leads to a transferred path set Σ _t_ ( _S_ 0 _, Sd, σp_ ). Σ _t_ is strong homotopiclike if the hyperplane swept by the varying transfer vector **v** _p→i_ keeps collision-free. As constrained environments are present, such an assumption usually fails, which entails refined processing to reach the final path set. 


![](1_survey/papers/md/Huang2024Homotopic_figs/Huang2024Homotopic.pdf-0005-08.png)


In this section, a path set generation scheme for constrained environments is proposed incorporating two refined steps on [5]: 1) pivot path planning and repositioning, and 2) coordinated deformable path transfer. 

_A. Pivot Path Planning and Repositioning_ 

_1) Repositioning Reference Points Determination:_ Before planning the pivot path _σp_ , a pivot selection criterion minimizing the transfer vector magnitude is introduced as 


![](1_survey/papers/md/Huang2024Homotopic_figs/Huang2024Homotopic.pdf-0005-12.png)


which limits path transfer to a tunnel centered at _σp_ with a radius as small as possible. In Σ _t_ , transferred paths can percolate obstacles easily since _σp_ is often close to obstacles to reduce its length in (5) or (6). _σp_ thus needs to be repositioned to a more reasonable configuration while preserving _Pσp_ (1). After planning _σp_ , Σ _t_ is obtained for checking passage intersections. Usually, it is sufficient to consider obstacles in _Pσp_ (1), but this may miss some nearby obstacles. For completeness, a distance filter is first applied to register obstacles near _σp_ . Denote the distance between _σp_ and _Ei_ as 


![](1_survey/papers/md/Huang2024Homotopic_figs/Huang2024Homotopic.pdf-0005-14.png)


A threshold _λ_ = max1 _≤i≤K_ max( _∥_ **s** 0 _,i−_ **s** 0 _,p∥_ 2 _, ∥_ **s** _d,i−_ **s** _d,p∥_ 2) is set to rule out obstacles not in _σp_ ’s vicinity. The remaining obstacles are divided into two categories: obstacles in passages traversed by _σp_ , termed passage obstacles, and isolated obstacles otherwise. Formally, define _Enear_ = _{Ei | d_ ( _σp, Ei_ ) _≤ λ}_ , _EP_ = _{Ei |_ ( _Ei, Ej_ ) _∈ Pσp_ (1) or ( _Ej, Ei_ ) _∈ Pσp_ (1) _∃Ej}_ . Passage obstacles are _EP[near]_ = _Enear ∩EP_ . Isolated obstacles are _Eiso_ = _Enear \ EP[near]_ . 

The relative position of _σp_ to nearby obstacles determines how _σp_ should be locally repositioned. The passage list _Pσp_ (1) is updated to only contain passages with obstacles in _Enear_ . _Pσp_ (1 _, i_ ) = ( _Ej, Ek_ ) is discarded if both _Ej_ and _Ek_ are not in _Enear_ . The intersection segment between Σ _t_ and _Pσp_ (1 _, i_ ) is characterized by the chord, denoted as Σ _t ∩ Pσ[′] p_[(1] _[, i]_[)][,][with][its] length being 


![](1_survey/papers/md/Huang2024Homotopic_figs/Huang2024Homotopic.pdf-0005-17.png)


where _Pσ[′] p_[(1] _[, i]_[)][signifies][the][entire][straight][line][on][which] _Pσp_ (1 _, i_ ) lies. _σt,k_ ( _ηk,i_ ) is the intersection point between _σt,k_ and _Pσ[′] p_[(1] _[, i]_[)][.][The][ordered][intersection][points][between] _σp_ and _Pσp_ (1), _{σp_ ( _ηp,_ 1) _, σp_ ( _ηp,_ 2) _, ..., σp_ ( _ηp,n_ ) _}_ , constitute reference points of _σp_ . Two overlapping possibilities between Σ _t ∩Pσ[′] p_[(1] _[, i]_[)][ and] _[ P][σ] p_[(1] _[, i]_[)][ exist:][ Σ] _[t][∩][P] σ[ ′] p_[(1] _[, i]_[)][ is completely] contained in _Pσp_ (1 _, i_ ) or otherwise. If Σ _t ∩ Pσ[′] p_[(1] _[, i]_[)][falls] inside _Pσp_ (1 _, i_ ), the intersection point _σp_ ( _ηp,i_ ) just remains unchanged for anchoring. In situations otherwise, the chord is in collision and _σp_ should be modified locally. If _∥_ Σ _t ∩ Pσ[′] p_[(1] _[, i]_[)] _[∥]_[2] _[≤∥][P][σ] p_[(1] _[, i]_[)] _[∥]_[2][,] _[P][σ]_[(1] _[, i]_[)][is][sufficiently][wide.] _[σ][p]_ can be simply translated along _Pσp_ (1 _, i_ ) to move the chord into _Pσp_ (1 _, i_ ). Denote _σp[∗]_[(] _[η][p,i]_[)][the adjusted][reference point,][it] can be given as 


![](1_survey/papers/md/Huang2024Homotopic_figs/Huang2024Homotopic.pdf-0005-19.png)


where **d** _δ,i_[is the translation along] _[ P] σp_[(1] _[, i]_[)][. Note that there is] one chord end outside _Pσp_ (1 _, i_ ), be it _σq_ ( _ηq,i_ ). After translation, the end is moved to a point **p** _δ,i_[on] _[ P] σp_[(1] _[, i]_[)][ with a preset] clearance _δ_ to obstacles. The shift is **d** _δ,i_[=] **[p]** _δ,i[−][σ] q_[(] _[η] q,i_[)][as] illustrated in Fig. 5 and Fig. 6. 


![](1_survey/papers/md/Huang2024Homotopic_figs/Huang2024Homotopic.pdf-0006-00.png)


Fig. 5. In the shown passage, _σ_ 2 is the pivot path. _σt,_ 1 _, σt,_ 3 are transferred from _σ_ 2 and both collide with obstacles. To tackle this, _σ_ 2 is repositioned first. _σt,_ 1 _, σt,_ 3 are then locally deformed. 

_∥_ Σ _t ∩ Pσ[′] p_[(1] _[, i]_[)] _[∥]_[2] _[>][∥][P][σ] p_[(1] _[, i]_[)] _[∥]_[2][is][more][constrained.] The chord cannot be placed within the passage segment by translation. Repositioning _σp_ now aims for a coordinated distribution of all transferred paths. The strategy to overlap centers of Σ _t ∩ Pσ[′] p_[(1] _[, i]_[)][and] _[P][σ] p_[(1] _[, i]_[)][is][utilized][in][[][5][].] Its problem is that it may cause extremely unbalanced path distributions. To avoid this, proportionally placing intersection points on _Pσp_ (1 _, i_ ) according to the relative distribution of _{σt,_ 1( _η_ 1 _,i_ ) _, σt,_ 2( _η_ 2 _,i_ ) _, ..., σt,K_ ( _ηK,i_ ) _}_ provides more reasonable reference points. _σp[∗]_[(] _[η][p,i]_[)][now][is] 


![](1_survey/papers/md/Huang2024Homotopic_figs/Huang2024Homotopic.pdf-0006-03.png)


where _ri_ = ( _∥Pσp_ (1 _, i_ ) _∥_ 2 _−_ 2 _δ_ ) _/∥_ Σ _t ∩ Pσ[′] p_[(1] _[, i]_[)] _[∥]_[2][is][the] scaling ratio. **p** _δ,i_[is the new chord end. As] _[ ∥]_[Σ] _t[∩][P][ ′] σp_[(1] _[, i]_[)] _[∥]_[2] _[>] ∥Pσp_ (1 _, i_ ) _∥_ 2, at least one chord end is outside of _Pσp_ (1 _, i_ ) to be taken as _σq_ ( _ηq,i_ ). For isolated obstacles, we only consider the case in which they collide with some path or lie between paths. As such, _σp_ ( _τEi_ ) is translated along the direction of _σp_ ( _τEi_ ) _−_ **p** _[∗] i_[,][where] _[σ][p]_[(] _[τ][E] i_[)][is][the][minimum] distance projection of _Ei_ on _σp_ in (11). **p** _[∗] i_[is][the][optimal] point on _Ei_ . This is analogous to (13) by replacing _Pσ[′] p_[(1] _[, i]_[)] with the line of _σp_ ( _τEi_ ) _−_ **p** _[∗] i_[.] 

_2) Repositioning Pivot Path:_ A series of reference points have been obtained along _σp_ . _σp_ is repositioned iteratively between every two consecutive reference points in a linear interpolation manner. For _ηp,i ≤ τ ≤ ηp,i_ +1, the new path position _σp[∗]_[(] _[τ]_[)][is][given][as] 


![](1_survey/papers/md/Huang2024Homotopic_figs/Huang2024Homotopic.pdf-0006-06.png)


_σp[∗]_[is][the][repositioned] _[σ][p]_[.][The][start][and][final][points][of] _[σ][p]_ need to be inserted to establish an augmented list of reference points _{σp_ (0) _, σp[∗]_[(] _[η][p,]_[1][)] _[, ..., σ] p[∗]_[(] _[η][p,n]_[)] _[, σ][p]_[(1)] _[}]_[.][Since][the][shift] magnitude on a passage segment is small compared to the total path length, the path segment in (15) is feasible in general. As for the repositioning procedure in 3D space, the chord evolves into the convex hull formed by intersection points with the passage plane. Without considering floating obstacles, the shift of _σp_ ( _ηp,i_ ) is restricted in the direction parallel to the ground and rules are set similarly to (13) and (14). One 


![](1_survey/papers/md/Huang2024Homotopic_figs/Huang2024Homotopic.pdf-0006-08.png)


Fig. 6. Different situations when attaining reference points for the pivot path _σp_ . 1. No need for repositioning. 2. Translate _σp_ along the passage segment. 3. Reposition _σp_ to proportionally compress the chord. 4. Push _σp_ away from an isolated obstacle. 

inherent problem of chords is that they may poorly represent how the entire path set passes through the passage and lead to nonsmooth path segments, e.g., when the passage is nearly parallel to the local path. Inspired by the virtual tube [2], [3], we propose a geometrical approach for chord determination, which uses the normal direction of the pivot path to get the chord and then rotates it back to the passage segment. Details are given in Appendix A. 

## _B. Coordinated Deformable Path Transfer_ 

After attaining _σp[∗]_[,][the][next][step][generates][rest][agent][paths.] Although _σp[∗]_[gets][further][optimized][based][on] _[σ][p]_[,][directly] transferred paths from _σp[∗]_[via][(][9][)][may][still][be][infeasible] in constrained environments. To effectively convert a locally infeasible path into a feasible one, a path-deforming scheme similar to the path-guided optimization avenue in [39], [40] is leveraged. The core idea is to use proper reference points to tailor infeasible path parts to feasible paths through path deformation. Firstly, a new path set Σ _[∗] t_[is][regenerated][by] transferring _σp[∗]_[to rest agents as (][9][). Passage intersection check] is conducted as before. If adjustment is needed, the reference point for each transferred path is given as 


![](1_survey/papers/md/Huang2024Homotopic_figs/Huang2024Homotopic.pdf-0006-13.png)


where _σ[∗]_[is][the][fixed][reference][point.][The][intersection] _t,j_[(] _[η][j,i]_[)] point of the repositioned _σp[∗]_[is][fixed][as][the][reference][point.] This follows the proportional distribution in (14) to compress the chord. With all these reference points, each transferred path is deformed in the same manner as (15). 

The deformed transferred path _σt,j[∗]_[need][not][be][collision-] free because obstacle sizes may not be negligible in practice. The key to addressing this is providing more reference points near narrow passages than those on the passage segments. This can be achieved by introducing translated passage segments on obstacle vertices as shown in Fig. 16 and more details are provided in Appendix B. The overall path set generation pipeline is outlined in Algorithm 3. The completeness of the entire scheme is ensured by the completeness of the optimal planner backbone for pivot path planning. Only linear time complexity w.r.t. the discrete path node number exists to obtain a transferred path and the resulting paths are strong path homotopic by construction. 


![](1_survey/papers/md/Huang2024Homotopic_figs/Huang2024Homotopic.pdf-0007-00.png)


**----- Start of picture text -----**<br>
30 30 30<br>25 25 25 18 11 10 20<br>20 20 20 2 6 5<br>15 15 15 15 7 14<br>10 10 10 1 4 8<br>5 5 5 19 12 9 3<br>17 16 13<br>0 0 0<br>0 10 20 30 40 50 0 10 20 30 40 50 0 10 20 30 40 50<br>x x x<br>(a) (b) (c)<br>y y y<br>**----- End of picture text -----**<br>


Fig. 7. Examples of passage detection results with different obstacle distributions. Dashed blue segments are passages after the visibility check. Solid black segments are passages after the extended visibility check. (a) and (b) have the same obstacle side length of one with 20 and 100 obstacles respectively. Dense dashed segments are not plotted in (b) for clarity. (c) 20 obstacles with an obstacle side length of four. 

## VI. EXPERIMENTAL RESULTS 

The proposed path set planning pipeline together with core modules is implemented and tested in various conditions. This section presents comprehensive evaluation results. Core code is updated at _https://github.com/HuangJingGitHub/HPSP_ . 

## _A. Passage Detection by Extended Visibility Check_ 

As a key upstream module, passage detection determines passages for the following path set planning. The experiment aims to investigate how the visibility condition and the extended variant affect the resulting passages. Different setups of obstacle shapes, sizes, and densities are tested to enrich passage variations. For each obstacle number equally spaced from 10 to 100, the passage number is averaged over 10 random obstacle distributions (map size: 50 _×_ 30) of random shapes (squares, regular triangles, and rectangles with an aspect ratio of 2:1) and poses. The obstacle size is controlled by the side length which is set as one here to accommodate more obstacles (see Fig. 7). The statistical results in Fig. 8(a) show that the combinatorial quadratic increase of the passage number w.r.t. the obstacle number is reduced to significant linear relations by two visibility conditions, which dramatically brings down the valid passage number. Both conditions have coefficients of determination larger than 0 _._ 99 after linear regression. The extended visibility condition, however, has a much smaller passage number increase rate ( _∼_ 2 _._ 1 vs. 15 _._ 0). The ratios of the passage number using the visibility condition to that using the extended version has a mean of 0 _._ 158, suggesting that only a small fraction of passages remain after further checking the extended visibility. 

Next, the obstacle number is fixed as 20, and side lengths are equally spaced from 0 _._ 5 to 5 to change obstacle sizes. Obstacle distributions are still randomly generated in 10 tests for each side length. Unlike the pure visibility check, Fig. 8(b) indicates that the extended visibility check is not sensitive to obstacle size changes. The passage number via the visibility check decreases significantly and nearly linearly as obstacles expand, but passage numbers after the extended visibility check present small variations. The passage number increases slightly rather than decreases as obstacles get larger. This counterintuitive phenomenon can be attributed to the fact that when obstacle sizes grow, the passage segment length _l_ ( **p** _[∗] i[,]_ **[ p]** _[∗] j_[)][ shrinks twice] 

as fast as the third obstacle _Ek_ ’s distance to the passage center **o** _i,j_ , making _Ek ∩Ri,j_ = _∅_ easier to meet in (4), leading to insignificant passage number rises in Fig. 8(b). Predictably, the two conditions’ differences will be unnoticeable if obstacle sizes are sufficiently large. Finally, Fig. 9 shows an example of passage detection in a 3D map. The passage distribution varies in height intervals divided by obstacle heights to get a sparse result. The passage distribution can be retrieved efficiently by indexing height as the key. 

## _B. Passage-Aware Optimal Path Planning Results_ 

This part showcases passage-aware optimal path planning (PAOPP) results. We aim to investigate two major aspects: the influence of cost formulations on planned paths and computational performance differences brought by two visibility checks in path planning. Despite many available efficient planner implementations such as the open motion planning library [51] and the navigation toolbox in MATLAB, it is not straightforward to incorporate passage-related functions and customized costs into existing frameworks due to the lack of related interfaces. RRT _[∗]_ planner is thus implemented separately with all subroutines in C++. Obstacle-related functionalities, including two types of visibility check for passage detection, passage segment positioning, and passage passing check for path segments, are packaged to be invoked readily. These make cost forms and parameters easily configurable when instantiating a planner. 

As depicted in Fig. 10, different cost formulations are tested in path planning: the ratio cost in (5) and the weighted cost in (6) with different weights ( _kP_ = 1 _,_ 10, and 100 respectively to change the preference). Various numbers of obstacles are randomly distributed. Passage detection is conducted using the extended visibility check and environment boundaries are treated as extra obstacles. The planning problem is constant across tests to find an optimal path from the top left to the bottom right corner as in Fig. (10). It is observed that paths can vary with cost choices. For the weighted cost, the path length Len( _σ_ ) dominates the cost when _kP_ = 1. Thus, the resulting paths (green paths) prioritize minimizing Len( _σ_ ), similar to the most typical setup in optimal path planning. In comparison, when _kP_ = 100, the minimum traversed passage width _fP_ ( _σ_ ) largely determines the cost. Planned paths (red paths) try to 


![](1_survey/papers/md/Huang2024Homotopic_figs/Huang2024Homotopic.pdf-0008-00.png)


**----- Start of picture text -----**<br>
1800<br>Extended visibility condition<br>1600 Pure visibility condition<br>1400<br>1200<br>1000<br>800<br>600<br>400<br>200<br>0<br>10 20 30 40 50 60 70 80 90 100<br>Obstacle number<br>(a)<br>180<br>Extended visibility condition<br>160 Pure visibility condition<br>140<br>120<br>100<br>80<br>60<br>40<br>20<br>0<br>0.5 1 1.5 2 2.5 3 3.5 4 4.5 5<br>Obstacle side length (20 obstacles)<br>(b)<br>Passage number<br>Passage number<br>**----- End of picture text -----**<br>



![](1_survey/papers/md/Huang2024Homotopic_figs/Huang2024Homotopic.pdf-0008-01.png)



![](1_survey/papers/md/Huang2024Homotopic_figs/Huang2024Homotopic.pdf-0008-02.png)


**----- Start of picture text -----**<br>
(a)<br>200 200<br>9 z < 21 m 9 55 < z < 65 m<br>150 150<br>8 8<br>100 7 100 7<br>1 10 1<br>6<br>50 2 3 50 2<br>5 4 5 4<br>0 0<br>0 50 100 150 200 0 50 100 150 200<br>x (m) x (m)<br>(b)<br>y (m) y (m)<br>**----- End of picture text -----**<br>


Fig. 9. 3D passage detection example. (a) Valid passages are transparent red planes. (b) Height-varying passage distributions in two height intervals. 

TABLE I 

Fig. 8. Statistical results of passage numbers detected by two check conditions in different setups. (a) Passage numbers with different numbers of obstacles (obstacle side length is one). (b) Passage numbers with the same number of obstacles but different obstacle sizes. 

avoid going through narrow passages. In between, _kP_ = 10 balances the two items shown by cyan paths. The value range of _kP_ to effectively alter two factors’ precedence is problemrelated as _kP_ varies to make Len( _σ_ ) and _kP fP_ ( _σ_ ) comparable. Overall, the ratio cost (paths are in blue) behaves similarly to adopting a moderate _kP_ in the weighted cost, making it a balanced cost in most cases. 

To quantitatively measure how the extended visibility check improves planning efficiency, passages are identified by two check conditions respectively for PAOPP, i.e., PAOPP-pure and PAOPP-ext. Planning efficiency is gauged by the planning time with a maximum valid sample number _N_ = 10k. The path cost is weighted ( _kP_ = 10) and the start and goal remain unchanged. All computations are run on a PC with Ubuntu 18.04, Intel Core i9-7980XE CPU@2 _._ 60 GHz _×_ 36, and 64 GB of RAM, with no specifications for acceleration. For the same problem, paths found with two passage check results have the same passage traversal list and similar path costs. Thus, they can be regarded as equivalently optimal paths. See Appendix D for theoretical analyses of two checks’ equivalence in PAOPP. The planning time differs much in Table I. For each obstacle number (the side length is three), 10 different planning tests are run. The planning time is shown to reduce 58 _._ 7 % on average. Roughly, the extended visibility check helps save more than 

AVERAGE TIME OF PASSAGE-AWARE OPTIMAL PATH PLANNING AND MAX-CLEARANCE PATH PLANNING TESTS (ms) 

||Obstacle Num.|10|20|30|40|50|60|
|---|---|---|---|---|---|---|---|
||MC-time|327_×_<br>9_._0|619_×_<br>9_._0|740_×_<br>9_._0|916_×_<br>9_._0|1361_×_<br>8_._9|1345_×_<br>8_._7|
||MC-sample|868|1440|2087|2594|3627|4223|
||PAOPP-pure<br>PAOPP-ext|1995<br>**882**|4172<br>**1640**|6342<br>**2401**|8312<br>**3331**|10161<br>**4212**|11405<br>**5119**|



half the planning time. Note that despite the significant time saving, its reduction is not as dramatic as the passage number reduction in Fig. 8(a) because passage-related operations only take a fraction of planning computations. 

Next, PAOPP is further compared to the conventional maxclearance path planning (MCPP) method. MCPP finds the shortest path with the maximum clearance (MC) to all obstacles and represents a classical avenue to balance path’s accessible free space and length. To get the MC, a binary search for MC in planning is performed as in Algorithm 4. The lower and upper bounds are half the minimum and maximum passage width respectively. For completeness, passage widths are detected by the pure visibility check. Two failure criteria for an MC value exist: return false if the planner fails to find a path after a given time (MCPP-time) or a given sample number (MCPP-sample). In Table I, MCPP-time reports the one-round planning time when MC is found within an error of 0 _._ 5 _×_ the total planning trail number. MCPP-sample reports the total planning time and the max sample number is _NMC_ = 20k. 


![](1_survey/papers/md/Huang2024Homotopic_figs/Huang2024Homotopic.pdf-0009-00.png)



![](1_survey/papers/md/Huang2024Homotopic_figs/Huang2024Homotopic.pdf-0009-01.png)



![](1_survey/papers/md/Huang2024Homotopic_figs/Huang2024Homotopic.pdf-0009-02.png)



![](1_survey/papers/md/Huang2024Homotopic_figs/Huang2024Homotopic.pdf-0009-03.png)


**----- Start of picture text -----**<br>
(a) M = 10 (b) M = 20 (c) M = 30<br>(d) M = 40 (e) M = 50 (f) M = 60<br>**----- End of picture text -----**<br>


Fig. 10. Path planning results using different cost formulations. The obstacle number in the environment ranges from 10 to 60. Blue paths correspond to the cost in (5). Green, cyan, and red paths correspond to the cost in (6) with _kP_ = 1 _,_ 10, and 100, respectively. 

MCPP-time turns out to be the slowest. Due to the fast planning failure check, MCPP-sample is faster than PAOPP with sparse passages by 13 _._ 4 % on average. However, its inherent drawbacks are that the planned result is not adjustable and its performance deteriorates if _NMC_ is large. See Appendix C for more implementation details and results. 

## _C. Path Set Generation Results_ 

Built on the modules above, the set generation scheme is implemented and tested. Given the initial _S_ 0 and final _Sd_ , a pivot path is first planned via PAOPP. _kP_ = 10 is utilized in pivot path planning for a balanced cost. The top row in Fig. 11 illustrates the directly transferred path set Σ _t_ (in blue) and the repositioned pivot path _σp[∗]_[(in][green).][Though] the planned pivot path _σp_ goes through passages associated with large free space, directly transferred paths collide with obstacles easily. This is because the passage passing positions of _σp_ , namely intersections with passages, are obtained to minimize the path length, which commonly makes _σp_ located in obstacles’ vicinity. Thereby, repositioning _σp_ is required while preserving its passed passages to better accommodate transferred paths. In experiments, the geometrical approach for chord determination is utilized. Reference points on passage segments are given from chords’ locations and _σp_ is deformed piecewise to _σp[∗]_[as][(][15][).] 

It is reinforced that filtering out invalid passages is not only for computational efficiency but also necessary. Dense passages after pure visibility check make path set intersections overly redundant. The extended variant attains a sparse distribution of passages more suitable for repositioning _σp_ and deformable path transfer. The repositioned _σp[∗]_[is][in][a] configuration more likely to lead to feasible transferred paths. In less restrictive cases with fewer obstacles like Fig. 11(a) and Fig. 11(d), paths directly transferred from _σp[∗]_[are][feasible.][In] 

TABLE II 

AVERAGE PATH SET PLANNING TIME USING PATH SET TRANSFER AND SEPARATELY PLANNING METHOD (ms) 

||Path Number|3|6|9|12|15|18|
|---|---|---|---|---|---|---|---|
||SP (_M_ = 10)|4442|9501|14653|20083|25393|31105|
||PT (_M_ = 10)|**840**|**882**|**845**|**879**|**863**|**867**|
||SP (_M_ = 20)|5809|11972|17743|24630|28956|33411|
||PT (_M_ = 20)|**1660**|**1681**|**1653**|**1665**|**1661**|**1658**|
||SP (_M_ = 30)|7242|13259|21332|28087|34020|40727|
||PT (_M_ = 30)|**2480**|**2433**|**2498**|**2450**|**2452**|**2272**|



general, transferred paths from _σp[∗]_[may][collide][with][obstacles,] and coordinated deformable path transfer is required. As in Fig. 11(f), there exist narrow passages that cannot accommodate all directly transferred paths. Coordinated reference points are given for each path to guide path deformation, making the path set go through narrow passages freely. In scenarios where obstacles are dense and of significant sizes, translated passage segments can be introduced to density reference points for feasible deformed paths. See Appendix B for more examples with translated passages. 

For efficiency evaluation, the benchmark method of separately planning (SP) each path is compared with the proposed scheme based on path transfer (PT). In the SP method, _σp_ is also first planned using PAOPP. Then the rest paths are planned separately with the homotopy constraint to _σp_ . Specifically, samples are restricted to be close to _σp_ and are obstaclefree to _σp_ in the neighborhood. Table II outlines the average path set planning time when obstacle number and path number vary in 10 random setups. As is observed, the SP method has a significantly larger time cost that increases nearly linearly with the path number. Conversely, the PT method time is not sensitive to the path number at all. Its dominant cost solely comes from _σp_ planning in PAOPP. Other operations in PT 


![](1_survey/papers/md/Huang2024Homotopic_figs/Huang2024Homotopic.pdf-0010-00.png)



![](1_survey/papers/md/Huang2024Homotopic_figs/Huang2024Homotopic.pdf-0010-01.png)



![](1_survey/papers/md/Huang2024Homotopic_figs/Huang2024Homotopic.pdf-0010-02.png)



![](1_survey/papers/md/Huang2024Homotopic_figs/Huang2024Homotopic.pdf-0010-03.png)


**----- Start of picture text -----**<br>
(a) (b) (c)<br>(d) (e) (f)<br>**----- End of picture text -----**<br>


Fig. 11. Path set generation results. Black dashed lines are passages after the extended visibility check. Light blue dashed lines are passages after the pure visibility check. (a)-(c) show the directly transferred path sets in blue and the repositioned pivot paths in green. (d)-(f) show corresponding path sets obtained via deformable path transfer from repositioned pivot paths. Red segments depict the chords of Σ _[∗] t_[transferred][from][the][repositioned] _[σ] p[∗]_[.] 

(e.g., pivot path reposition, path transfer) are linear to the path resolution, i.e., path node number, which is almost negligible compared to the cost of invoking the planner once. Moreover, coordination constraints are hard to impose in SP. Thus, the PT method is much more advantageous in homotopic path set planning. See Appendix C for more results. 

## _D. Application Case Study_ 

The last part showcases some common applications of path set planning in robot manipulation and navigation. The first kind of task is DO path planning in complex environments, similar to [5], but in much more cluttered setups. As shown in Fig. 12, a manipulation site is emulated with various objects randomly placed on the table. The robot needs to move a deformable grip glove on this table while avoiding collisions. Due to the restriction of tall objects like vertically placed boxes and bottles, manipulation is confined near the table surface, for which a path reference of the glove is required. To do this, several keypoints are picked on the glove to depict the glove state. In Fig. 12, these points are mainly distributed on fingers and the middle one acts as the pivot by (10). The target _Sd_ is vertically aligned. Obstacles are segmented as bounding quadrangles and path set planning is conducted in the image space. Fig. 12 demonstrates different test results. As can be seen, the planned path sets have wide free space along them with sufficiently short lengths, making them good path references for glove movement. With planned path sets, subsequent manipulation can be conducted as a constrained path set tracking problem as in [5]. 

The second task is swarm navigation in 3D maps. In Fig. 13, aerial robot swarms ( _K_ = 5 _,_ 10) move as a team in city environments where buildings of various sizes and heights are populated. To reach the target, the swarm needs to fly through 

narrow spaces among buildings. Robots are not allowed to fly subsequently as a queue or vertically aligned when passing narrow space and they are initially aligned horizontally in a line. The target is a different and distant formation. Robots’ positions change in 3D, including the flight height. Passage detection is first performed to establish the passage distribution in height intervals formed by buildings. The pivot can be selected arbitrarily and its planned path selects wide passages in Fig. 13(a) and Fig. 13(c). Then pivot path repositioning and coordinated deformable path set transfer are performed to generate the final path set in Fig. 13(b) and Fig. 13(d). Path deformation on passages is restricted in the _x_ - _y_ plane. Since robots’ initial and target positions are vertices of convex hulls, methods in [3] will have to plan paths for each robot with no optimization of accessible free space along paths. 

## VII. CONCLUSION 

This paper presented a systematic pipeline of homotopic path set planning for substantial robotics applications. The extended visibility check was first proposed to attain sparse passage distributions over pure visibility check. Passage-aware optimal path planning compatible with sampling-based optimal planners was designed with adjustable path costs. It could balance the path length and accessible free space more flexibly over clearance-based planning methods. Path set generation based on path transfer was then proposed. Techniques such as proportional reference point distribution, geometrical chord determination, and translated passage segments provided a better guarantee of the resulting paths’ feasibility and coordination. The scheme’s effectiveness was validated in different experiments. Future work includes more detailed passage descriptions as an area or space. Considering dynamic environments and imposing constraints among agents such as reducing path intersections are also important directions. 


![](1_survey/papers/md/Huang2024Homotopic_figs/Huang2024Homotopic.pdf-0011-00.png)



![](1_survey/papers/md/Huang2024Homotopic_figs/Huang2024Homotopic.pdf-0011-01.png)



![](1_survey/papers/md/Huang2024Homotopic_figs/Huang2024Homotopic.pdf-0011-02.png)



![](1_survey/papers/md/Huang2024Homotopic_figs/Huang2024Homotopic.pdf-0011-03.png)



![](1_survey/papers/md/Huang2024Homotopic_figs/Huang2024Homotopic.pdf-0011-04.png)


**----- Start of picture text -----**<br>
(a) (b) (c) (d)<br>**----- End of picture text -----**<br>


Fig. 12. Path set planning in DO manipulation site with random daily objects (bottles, boxes, tapes, etc.). There are eight objects in (a) and (b), ten in (c) and (d). Black dashed lines are detected passages. Planned path sets for the glove comprise yellow and green paths (pivot paths). 


![](1_survey/papers/md/Huang2024Homotopic_figs/Huang2024Homotopic.pdf-0011-06.png)



![](1_survey/papers/md/Huang2024Homotopic_figs/Huang2024Homotopic.pdf-0011-07.png)



![](1_survey/papers/md/Huang2024Homotopic_figs/Huang2024Homotopic.pdf-0011-08.png)



![](1_survey/papers/md/Huang2024Homotopic_figs/Huang2024Homotopic.pdf-0011-09.png)



![](1_survey/papers/md/Huang2024Homotopic_figs/Huang2024Homotopic.pdf-0011-10.png)


**----- Start of picture text -----**<br>
(a) (b) (c) (d)<br>**----- End of picture text -----**<br>


Fig. 13. Path set planning examples for swarms ( _K_ = 5 _,_ 10) in 3D maps. (a), (c) Passage-aware optimal path planning returns pivot paths with large accessible free space. (b), (d) Corresponding final path sets after pivot path repositioning and coordinated deformable path transfer. 

## REFERENCES 

- [1] J. Alonso-Mora, S. Baker, and D. Rus, “Multi-robot formation control and object transport in dynamic environments via constrained optimization,” _The International Journal of Robotics Research_ , vol. 36, no. 9, pp. 1000–1021, 2017. 

- [2] P. Mao and Q. Quan, “Making robotics swarm flow more smoothly: A regular virtual tube model,” in _Proc. IEEE/RSJ International Conference on Intelligent Robots and Systems_ , 2022, pp. 4498-4504. 

- [3] P. Mao, R. Fu, and Q. Quan, “Optimal virtual tube planning and control for swarm robotics,” _The International Journal of Robotics Research_ , 2023. 

- [4] W. H¨onig, J. A. Preiss, T. K. S. Kumar, G. S. Sukhatme and N. Ayanian, “Trajectory Planning for Quadrotor Swarms,” _IEEE Transactions on Robotics_ , vol. 34, no. 4, pp. 856-869, 2018. 

- [5] J. Huang, X. Chu, X. Ma, and K. W. Samuel Au “Deformable object manipulation with constraints using path set planning and tracking,” _IEEE Transactions on Robotics_ , vol. 39, no. 6, pp. 4671-4690, 2023. 

- [6] J. Sanchez, J.-A. Corrales, B.-C. Bouzgarrou, and Y. Mezouar, “Robotic manipulation and sensing of deformable objects in domestic and industrial applications: A survey,” _The International Journal of Robotics Research_ , vol. 37, no. 7, pp. 688–716, 2018. 

- [7] V. E. Arriola-Rios et al., ”Modeling of deformable objects for robotic manipulation: A tutorial and Review,” _Frontiers in Robotics and AI_ , vol. 7, 2020. 

- [8] P. Jim´enez, “Survey on model-based manipulation planning of deformable objects,” _Robotics and Computer-Integrated Manufacturing_ , vol. 28, no. 2, pp. 154–163, 2012. 

- [9] H. Yin, A. Varava, and D. Kragic, “Modeling, learning, perception, and control methods for deformable object manipulation,” _Science Robotics_ , vol. 6, no. 54, 2021. 

- [10] F. Lamiraux and L. E. Kavraki, “Planning paths for elastic objects under manipulation constraints,” _The International Journal of Robotics Research_ , vol. 20, no. 3, pp. 188–208, 2001. 

- [11] R. Gayle, W. Segars, M. Lin, and D. Manocha, “Path planning for deformable robots in complex environments,” in _Proc. Robotics: Science and Systems_ , 2005. 

- [12] M. Moll and L. E. Kavraki, “Path planning for deformable linear objects,” _IEEE Transactions on Robotics_ , vol. 22, no. 4, pp. 625–636, 2006. 

- [13] M. Saha and P. Isto, “Manipulation planning for deformable linear objects,” _IEEE Transactions on Robotics_ , vol. 23, no. 6, pp. 1141–1150, 2007. 

- [14] A. Doumanoglou _et al._ , “Folding clothes autonomously: A complete pipeline,” _IEEE Transactions on Robotics_ , vol. 32, no. 6, pp. 1461–1478, 2016. 

- [15] L. Lu and S. Akella, “Folding cartons with fixtures: A motion planning approach,” _IEEE Transactions on Robotics and Automation_ , vol. 16, no. 4, pp. 346–356, 2000. 

- [16] O. Burchan Bayazit, Jyh-Ming Lien, and N. M. Amato, “Probabilistic roadmap motion planning for deformable objects,” in _Proc. IEEE International Conference on Robotics and Automation_ , 2002, pp. 2126-2133. 

- [17] R. Gayle, M. C. Lin, and D. Manocha, “Constraint-based motion planning of deformable robots,” in _Proc. IEEE International Conference on Robotics and Automation_ , 2005, pp. 1046-1053. 

- [18] D. Mcconachie, A. Dobson, M. Ruan, and D. Berenson, “Manipulating deformable objects by interleaving prediction, planning, and control,” _The International Journal of Robotics Research_ , vol. 39, no. 8, pp. 957–982, 2020. 

- [19] D. Mcconachie, T. Power, P. Mitrano, and D. Berenson, “Learning when to trust a dynamics model for planning in reduced state spaces,” _IEEE Robotics and Automation Letters_ , vol. 5, no. 2, pp. 3540–3547, 2020. 

- [20] X. Chen, Y. Duan, R. Houthooft, J. Schulman, I. Sutskever, and P. Abbeel, “Infogan: Interpretable representation learning by information maximizing generative adversarial nets,” in _Proc. Conference on Neural Information Processing Systems_ , 2016. 

- [21] A. Wang, T. Kurutach, K. Liu, P. Abbeel, and A. Tamar, “Learning robotic manipulation through visual planning and acting,” in _Proc. Robotics: Science and Systems_ , 2019. 

- [22] A. Felner et al., “Search-based optimal solvers for the multiagent pathfinding problem: Summary and challenges,” in _Proc. International Symposium on Combinatorial Search_ , 2017, pp. 29–37. 

- [23] R. Stern et al., “Multi-agent pathfinding: Definitions, variants, and benchmarks,” in _Proc. International Symposium on Combinatorial Search_ , 2019, pp. 151–158. 

- [24] J. Yu and S. LaValle, “Structure and intractability of optimal multi-robot path planning on graphs,” in _Proc. AAAI Conference on Artificial Intelligence_ , 2013, pp. 1443–1449. 

- [25] D. Silver, “Cooperative pathfinding,” in _Proc. AAAI Conference on Artificial Intelligence and Interactive Digital Entertainment_ , 2005, pp. 117–122. 

- [26] Z. Bnaya and A. Felner, “Conflict-oriented windowed hierarchical cooperative A _[∗]_ ”, in _Proc. IEEE International Conference on Robotics and Automation_ , 2014, pp. 3743-3748. 

- [27] M. Khorshid, R. Holte, and N. Sturtevant, “A polynomial-time algorithm for non-optimal multi-agent pathfinding,” in _Proc. International Symposium on Combinatorial Search_ , 2011, pp. 76–83. 

- [28] J. Yu and S. M. LaValle, “Planning optimal paths for multiple robots on graphs”, in _Proc. IEEE International Conference on Robotics and Automation_ , 2013, pp. 3612-3617. 

- [29] E. Erdem, D. G. Kisa, U. Oztok and P. Sch¨uller, “A general formal framework for pathfinding problems with multiple agents,” in _Proc. AAAI Conference on Artificial Intelligence_ , 2013, pp. 290-296. 

- [30] P. Surynek, “Towards optimal cooperative path planning in hard setups through satisfiability solving,” in _Proc. The Pacific Rim International Conference on Artificial Intelligence_ , 2012, pp. 564-576. 

- [31] G. Wagner and H. Choset, “M _[∗]_ : A complete multirobot path planning algorithm with performance bounds,” in _Proc. IEEE/RSJ International Conference on Intelligent Robots and Systems_ , 2011, pp. 3260-3267. 

- [32] G. Sharon, R. Stern, A. Felner and N. R. Sturtevant, “Conflictbased search for optimal multi-agent pathfinding,” _Artificial Intelligence_ , vol. 219, pp. 40-66, 2015. 

- [33] G. Sharon, R. Stern, M. Goldenberg and A. Felner, “The increasing cost tree search for optimal multi-agent pathfinding,” _Artificial Intelligence_ , vol. 195, pp. 470-495, 2013. 

   - [41] L. Jaillet and T. Simeon, “Path deformation roadmaps: Compact graphs with useful cycles for motion planning,” _The International Journal of Robotics Research_ , vol. 27, no. 11–12, pp. 1175–1188, 2008 

   - [42] Z. Sun, D. Hsu, T. Jiang, H. Kurniawati and J. H. Reif, “Narrow passage sampling for probabilistic roadmap planning,” _IEEE Transactions on Robotics_ , vol. 21, no. 6, pp. 1105-1115, 2005. 

   - [43] P. Guo, C. Sun and Q. Li, “Obstacle avoidance path planning in unstructured environment with narrow passages,” _IEEE Transactions on Intelligent Vehicles_ , vol. 8, no. 11, pp. 4632-4643, 2023. 

   - [44] P. Bhattacharya and M. L. Gavrilova, “Voronoi diagram in optimal path planning,” in _Proc. IEEE International Symposium on Voronoi Diagrams in Science and Engineering_ , 2007, pp. 38–47. 

   - [45] H. Niu, A. Savvaris, A. Tsourdos, and Z. Ji, “Voronoi-visibility roadmap-based path planning algorithm for unmanned surface vehicles,” _The Journal of Navigation_ , vol. 72, no. 04, pp. 850–874, 2019. 

   - [46] J. Hu, H. Niu, J. Carrasco, B. Lennox, and F. Arvin, “Voronoibased multi-robot autonomous exploration in unknown environments via deep reinforcement learning,” _IEEE Transactions on Vehicular Technology_ , vol. 69, no. 12, pp. 14413–14423, 2020. 

   - [47] S. Karaman, M.R. Walter, A. Perez, E. Frazzoli, and S. Teller, “Anytime motion planning using the RRT _[∗]_ ,” in _Proc. IEEE International Conference on Robotics and Automation_ , 2011, pp. 1478-1483. 

   - [48] S. Karaman and E. Frazzoli, “Sampling-based algorithms for optimal motion planning,” _The International Journal of Robotics Research_ , vol. 30, no. 7, pp. 846-894, 2011. 

   - [49] J. D. Gammell, S. S. Srinivasa, and T. D. Barfoot, “Informed RRT*: Optimal sampling-based path planning focused via direct sampling of an admissible ellipsoidal heuristic,” in _Proc. IEEE/RSJ International Conference on Intelligent Robots and Systems_ , 2014, pp. 2997-3004. 

   - [50] J. M. Esposito and T. W. Dunbar, “Maintaining wireless connectivity constraints for swarms in the presence of obstacles,” in _Proc. IEEE International Conference on Robotics and Automation_ , 2006, pp. 946-951. 

   - [51] I. A. Sucan, M. Moll, and L. E. Kavraki, “The open motion planning library,” _IEEE Robotics and Automation Magazine_ , vol. 19, no. 4, pp. 72–82, 2012. 

- [34] A. Kushleyev, D. Mellinger, C. Powers, and V. Kumar, “Towards a swarm of agile micro quadrotors,” _Autonomous Robots_ , vol. 35, no. 4, pp. 287–300, 2013. 

- [35] I. Saha, R. Ramaithitima, V. Kumar, G. J. Pappas, and S. A. Seshia, “Automated composition of motion primitives for multirobot systems from safe LTL specifications,” in _Proc. IEEE/RSJ International Conference on Intelligent Robots and Systems_ , 2014, pp. 1525-1532. 

- [36] T. D. Barfoot and C. M. Clark, “Motion planning for formations of mobile robots,” _Robotics and Autonomous Systems_ , vol. 46, no. 2, pp. 65–78, 2004. 

- [37] A. Krontiris, S. Louis, and K. E. Bekris, “Multi-level formation roadmaps for collision-free dynamic shape changes with nonholonomic teams,” in _Proc. IEEE International Conference on Robotics and Automation_ , 2012, pp. 1570-1575. 

- [38] N. Ayanian, V. Kallem, and V. Kumar, “Synthesis of feedback controllers for multiple aerial robots with geometric constraints,” in _Proc. IEEE/RSJ International Conference on Intelligent Robots and Systems_ , 2011, pp. 3126-3131. 

- [39] B. Zhou, F. Gao, J. Pan, and S. Shen, “Robust real-time UAV replanning using guided gradient-based optimization and topological paths,” in _Proc. IEEE International Conference on Robotics and Automation_ , 2020, pp. 1208–1214. 

- [40] B. Zhou, J. Pan, F. Gao, and S. Shen, “Raptor: Robust and perception-aware trajectory replanning for quadrotor fast flight,” _IEEE Transactions on Robotics_ , vol. 37, no. 6, pp. 1992–2009, 2021. 

## APPENDIX A CHORD DETERMINATION VIA PATH SET’S LOCAL GEOMETRY 

The chord obtained via the intersection check of the passage line and the path set is not always informative for repositioning the path set. Regarding the path set as a tube, a chord makes a good reference when it aligns well with the cross-section of the tube as exemplified in Fig. 14. To better describe how the path set passes a passage, instead of intersections with the passage line, the cross-section nearby can be utilized. Specifically, the intersection between the pivot path _σp_ and passage _Pσp_ (1 _, i_ ) is _σp_ ( _ηp,i_ ). The intersection Σ _t ∩N_ ( _σp, ηp,i_ ) is first found, where _N_ ( _σp, ηp,i_ ) represents the pivot path’s normal line at _σp_ ( _ηp,i_ ) available by the local path’s geometrical properties. Similarly to (12), the chord on _N_ ( _σp, ηp,i_ ) has the following length form 


![](1_survey/papers/md/Huang2024Homotopic_figs/Huang2024Homotopic.pdf-0013-02.png)


where _σ[N]_[is][the][intersection][point][between] _[N]_[(] _[σ][p][, η][p,i]_[)] _t,k_[(] _[η][k,i]_[)] and the transferred path _σt,k_ . Since paths’ shifts are on the passage. Then Σ _t∩N_ ( _σp, ηp,i_ ) is reflected on _Pσp_ (1 _, i_ ), which can be done by rotating Σ _t ∩N_ ( _σp, ηp,i_ ) about the point _σp_ ( _ηp,i_ ) to _Pσp_ (1 _, i_ ). The rotation direction is the acute angle between _Pσp_ (1 _, i_ ) and _N_ ( _σp, ηp,i_ ) to preserve the relative distribution of intersection points. Roughly speaking, looking in the pivot path’s forward direction at _σp_ ( _ηp,i_ ), if an intersection point _σ[N] t,k_[(] _[η][k,i]_[)][ is on the left (right) side of] _[ σ][p]_[(] _[η][p,i]_[)][ on] _[ N]_[(] _[σ][p][, η][p,i]_[)][.] It should be on the left (right) side of _σp_ ( _ηp,i_ ) after rotation on _Pσp_ (1 _, i_ ). The chord obtained by rotation now depicts the intersection point distribution on the passage and the following steps keep the same. 


![](1_survey/papers/md/Huang2024Homotopic_figs/Huang2024Homotopic.pdf-0013-04.png)


Adding translated passage segments aims to provide more references for path collision avoidance in obstacle-dense setups. For example, _σt,_ 3 in Fig. 5 is deformed to shift left. If the only reference point on _Pσ_ 2(1 _, i_ ) is placed too close to the right obstacle, the repositioned path is still in collision and this is not explicitly addressed in [5]. To handle this, the passed passage segment by the pivot path is translated to obstacle vertices to make _translated passage segments_ . As illustrated in Fig. 16, _Pσp_ (1 _, i_ ) is translated to vertices constructing this passage. _Pσp_ (1 _, i_ ) = ( _Ej, Ek_ ) with **p** _[∗] j[∈E][j][,]_ **[ p]** _[∗] k[∈E][k]_[minimizing] the distance in (2). There exists a translated passage segment starting at a vertex **v** _j[E][∈E][j]_[if] 


![](1_survey/papers/md/Huang2024Homotopic_figs/Huang2024Homotopic.pdf-0013-06.png)


for some small _δ >_ 0. **p** _[∗] k[−]_ **[p]** _[∗] j_[characterizes the direction from] _Ej_ to _Ek_ along _Pσp_ (1 _, i_ ). For vertices on _Ek_ , the direction reverses. (A2) essentially defines a ray starting at **v** _j[E]_[.][The] other end of the ray is assigned by detecting its collision with other obstacles or boundaries. Next, reference points of 


![](1_survey/papers/md/Huang2024Homotopic_figs/Huang2024Homotopic.pdf-0013-08.png)


Fig. 14. In this example, the chord on the passage line poorly characterizes how paths should be moved. Paths’ intersections on the normal line of the pivot path better describe the path set’s local geometry. 

## **Algorithm 3:** Path Set Generation 


![](1_survey/papers/md/Huang2024Homotopic_figs/Huang2024Homotopic.pdf-0013-11.png)



![](1_survey/papers/md/Huang2024Homotopic_figs/Huang2024Homotopic.pdf-0013-12.png)



![](1_survey/papers/md/Huang2024Homotopic_figs/Huang2024Homotopic.pdf-0013-13.png)



![](1_survey/papers/md/Huang2024Homotopic_figs/Huang2024Homotopic.pdf-0013-14.png)



![](1_survey/papers/md/Huang2024Homotopic_figs/Huang2024Homotopic.pdf-0013-15.png)


_σt,i_ on translated passage segments are found where the same procedure as in Section V is adopted. 

In practice, there may be multiple passage segments associated with an obstacle. For an obstacle vertex not contained in a passage, its nearest passage can be selected. Moreover, to avoid too dense passage segments, _Pσp_ (1 _, i_ ) can be translated to only one obstacle in _Ej_ and _Ek_ . Lastly, a translated passage can be filtered away by considering its distance to existing passages on the obstacle. Specifically, _d[∗]_ ( **v** _j[E][,]_ **[ v]** _near[E]_[)][is][the] distance of **v** _j[E]_[to][an][existing][passage][end] **[v]** _near[E]_[on] _[E][j]_[in][the] orthogonal direction of **p** _[∗] k[−]_ **[p]** _[∗] j_[,][i.e.,] 


![](1_survey/papers/md/Huang2024Homotopic_figs/Huang2024Homotopic.pdf-0013-18.png)



![](1_survey/papers/md/Huang2024Homotopic_figs/Huang2024Homotopic.pdf-0014-00.png)



![](1_survey/papers/md/Huang2024Homotopic_figs/Huang2024Homotopic.pdf-0014-01.png)



![](1_survey/papers/md/Huang2024Homotopic_figs/Huang2024Homotopic.pdf-0014-02.png)



![](1_survey/papers/md/Huang2024Homotopic_figs/Huang2024Homotopic.pdf-0014-03.png)


**----- Start of picture text -----**<br>
(a) M = 10 (b) M = 20 (c) M = 30<br>(d) M = 40 (e) M = 50 (f) M = 60<br>**----- End of picture text -----**<br>


Fig. 15. Path planning results using different planners. The obstacle number ranges from 10 to 60. Blue paths are found by PAOPP-pure. Green paths are found by PAOPP-ext. _kP_ = 50 in two PAOPP planners. Red paths are found by MCPP. 


![](1_survey/papers/md/Huang2024Homotopic_figs/Huang2024Homotopic.pdf-0014-05.png)


Fig. 16. Transferred paths from the repositioned _σp[∗]_[may][be][infeasible.][The] shown paths shifted left from the setup in Fig. 5 as _σp_ is shifted left to _σp[∗]_[,] but infeasible paths exist. Blue dashed lines are translated passage segments starting from obstacle vertices. 


![](1_survey/papers/md/Huang2024Homotopic_figs/Huang2024Homotopic.pdf-0014-07.png)


Fig. 17. Example of adding translated passages. Translated passage segments (blue segments) are only on obstacles on one side of the pivot path to avoid overly dense passage segments. 

**n** _[⊥] k,j_[is the unit vector orthogonal to] **[ p]** _[∗] k[−]_ **[p]** _[∗] j_[. If] _[ d][∗]_[(] **[v]** _j[E][,]_ **[ v]** _near[E]_[)] is too small, _Pσp_ (1 _, i_ ) is not translated to the vertex **v** _j[E]_[.][An] example of added passage segments is shown in Fig. 17. 

## APPENDIX C EXTENDED EXPERIMENTAL RESULTS 

More comparative results between PAOPP and MCPP, path set generation using SP and PT methods are reported here. Fig. 10 shows examples of path planning results using MCPP and PAOPP with two passage detection strategies ( _kp_ = 50). PAOPP-pure (using passages detected by the pure visibility check) and PAOPP-ext (using passages detected by the extended visibility check) find similar paths passing the same passages. Thus, paths have similar path costs and can be regarded as equivalently optimal paths. This empirically validates that the sparse passage distribution after the extended visibility check in PAOPP-ext will generally have the same optimal path as PAOPP-pure. The equivalence of PAOPP-ext and PAOPP-pure on an easy condition is analyzed in Appendix 

D. Paths found by MCPP may or may not be homotopic to those in PAOPP. Due to the clearance constraint, the planned path keeps the MC from obstacles. For better feasibility, the clearance to map boundaries is not included in MCPP. MCPP implementation is outlined in Algorithm 4. 

The comparisons between path set generation results using SP and PT are demonstrated in Fig. 19. In addition to the significant runtime differences reported in Table II, Fig. 19 provides intuitive comparisons of planned path sets. The main difference is that though the homotopy constraint is enforced in the SP method, coordination among paths is hard to achieve and paths overlap in most cases. To address this, explicit rules need to be specified to coordinate paths or postprocessing will be required to refine paths. In contrast, path sets generated by the PT method usually occupy wider spaces in narrow passages to place paths, which makes it more suitable for multiple path generation in obstacle-dense environments. In addition, the PT method allows for specifications of coordination requirements by adjusting reference point distributions in passages, making it quite flexible. 

**Algorithm 4:** Max-Clearance Path Planning (MCPP) 

**1** Input **s** 0 _,_ **s** _d_ ; 

**2** _Pvalid ←_ PureVisibilityCheck( _E_ 1 _, ..., EM_ ); 

**3** _MClower ←_ min _∥Pvalid∥_ 2 _/_ 2; **4** _MCupper ←_ max _∥Pvalid∥_ 2 _/_ 2; **5** _σMC ←∅_ ; 


![](1_survey/papers/md/Huang2024Homotopic_figs/Huang2024Homotopic.pdf-0015-04.png)


## APPENDIX D CONDITION OF EQUIVALENCE BETWEEN PAOPP-PURE AND PAOPP-EXT 

One fundamental problem of the extended visibility check is whether it guarantees the optimality of planned paths in PAOPP problems. In other words, the problem is if paths planned by PAOPP-ext are guaranteed to be the same as those planned by PAOPP-pure. Here we show that the equivalence between PAOPP-ext and PAOPP-pure can be achieved via simple processing. For simplicity, only the 2D case is discussed here, but the derivation extends to 3D space readily. The elementary case is illustrated in Fig. 18. The passage ( _E_ 1 _, E_ 2) passes the pure visibility check but will be discarded in the extended visibility check due to _E_ 3. ( _E_ 1 _, E_ 3) and ( _E_ 2 _, E_ 3) are valid. Considering the region _A_ 123 enclosed by obstacles and passage segments, any non-winding path _σ_ can be categorized into one of the following four types: 

1) _σ_ does not pass _A_ 123. 

2) _σ_ is entirely inside _A_ 123. 

3) _σ_ passes through _A_ 123. 

4) One endpoint of _σ_ is inside _A_ 123 and the other is not. 

Our discussion is restricted to PAOPP problems in which _fP_ ( _σ_ ), the minimum passage width passed by _σ_ , is used in the path cost like (5) and (6). For type 1 and 2, _fP_ ( _σ_ ) is intact. For type 3, the discarding of ( _E_ 1 _, E_ 2) will not affect the update of _fP_ ( _σ_ ) before and after passing _A_ 123. Specifically, note that _∥_ ( _E_ 1 _, E_ 2) _∥_ 2 _> ∥_ ( _E_ 1 _, E_ 3) _∥_ 2, _∥_ ( _E_ 1 _, E_ 2) _∥_ 2 _> ∥_ ( _E_ 2 _, E_ 3) _∥_ 2. Then if _σ_ passes ( _E_ 1 _, E_ 2) and ( _E_ 1 _, E_ 3) (the passing order does not matter), the update rule of _fP_ ( _σ_ ) is 


![](1_survey/papers/md/Huang2024Homotopic_figs/Huang2024Homotopic.pdf-0015-12.png)


Fig. 18. Only type 3 and 4 are illustrated here. ( _E_ 1 _, E_ 2) can pass the visibility check but cannot pass the extended variant. Green paths pass through _A_ 123 across different passages. The blue path has one endpoint inside _A_ 123. 

In all cases, _fP_ ( _σ_[2] ) is independent from ( _E_ 1 _, E_ 2). Therefore, discarding ( _E_ 1 _, E_ 2) will not affect the update of the path cost _f_ ( _σ_ ). This result holds iteratively for the entire environment. As a result, optimal planners return the path with the optimal cost, namely the optimal path. 

For type 4, however, PAOPP-ext and PAOPP-pure may return different results. The fundamental reason is that in PAOPP-ext, path costs of paths passing ( _E_ 1 _, E_ 2) may not be updated in type 4. Assume the target position _σ_ (1) is within _A_ 123, in PAOPP-pure, _fP_ ( _σ_ 1[2] _,_ 2[)][after] _[σ]_[passes][(] _[E]_[1] _[,][ E]_[2][)][is] 


![](1_survey/papers/md/Huang2024Homotopic_figs/Huang2024Homotopic.pdf-0015-16.png)


where the subscript of _σ_ signifies which passage _σ_ passes. In PAOPP-ext, however, _fP_ ( _σ_ 1[2] _,_ 2[)][=] _[f][P]_[(] _[σ]_ 1[1] _,_ 2[)][is][not][updated.][If] _fP_ ( _σ_ 1[1] _,_ 2[)] _[>][∥]_[(] _[E]_[1] _[,][E]_[2][)] _[∥]_[2][happens,] _[f][P]_[(] _[σ]_ 1[2] _,_ 2[)][=] _[∥]_[(] _[E]_[1] _[,][E]_[2][)] _[∥]_[2][is] correctly updated in PAOPP-pure, but _fP_ ( _σ_ 1[2] _,_ 2[)][=] _[f][P]_[(] _[σ]_ 1[1] _,_ 2[)] in PAOPP-ext and a smaller cost is wrongly adopted (suppose other conditions except _fP_ ( _σ_ ) are the same). This may further lead to a different choice of the optimal path among _σ_ 1[2] _,_ 2 _[, σ]_ 1[2] _,_ 3 and _σ_ 2[2] _,_ 3[.][The][same][also][applies][to][situations][where][the][start] of _σ_ is in _A_ 123. Note that such a situation is rare and only locally affects the path’s beginning or ending parts. A simple way to address this is to preserve passages enclosing the start and target positions in PAOPP-ext. To sum up, PAOPP-ext and PAOPP-pure are equivalent in finding the optimal path in type 1 to 3. In type 4, the equivalence can be ensured by preserving passages enclosing the start and target positions. 


![](1_survey/papers/md/Huang2024Homotopic_figs/Huang2024Homotopic.pdf-0015-18.png)


where _σ_[1] _, σ_[2] represent _σ_ before entering _A_ 123 and after leaving _A_ 123, respectively. If _σ_ passes ( _E_ 1 _, E_ 2) and ( _E_ 2 _, E_ 3), _fP_ ( _σ_ ) is updated as 


![](1_survey/papers/md/Huang2024Homotopic_figs/Huang2024Homotopic.pdf-0015-20.png)


Finally, if _σ_ passes ( _E_ 1 _, E_ 3) and ( _E_ 2 _, E_ 3), _fP_ ( _σ_[2] ) is 


![](1_survey/papers/md/Huang2024Homotopic_figs/Huang2024Homotopic.pdf-0015-22.png)



![](1_survey/papers/md/Huang2024Homotopic_figs/Huang2024Homotopic.pdf-0016-00.png)



![](1_survey/papers/md/Huang2024Homotopic_figs/Huang2024Homotopic.pdf-0016-01.png)



![](1_survey/papers/md/Huang2024Homotopic_figs/Huang2024Homotopic.pdf-0016-02.png)



![](1_survey/papers/md/Huang2024Homotopic_figs/Huang2024Homotopic.pdf-0016-03.png)


**----- Start of picture text -----**<br>
(a) SP ( M = 10 , K = 3) (b) SP ( M = 10 , K = 9) (c) SP ( M = 10 , K = 15)<br>(d) PT ( M = 10 , K = 3) (e) PT ( M = 10 , K = 9) (f) PT ( M = 10 , K = 15)<br>(g) SP ( M = 20 , K = 3) (h) SP ( M = 20 , K = 9) (i) SP ( M = 20 , K = 15)<br>(j) PT ( M = 20 , K = 3) (k) PT ( M = 20 , K = 9) (l) PT ( M = 20 , K = 15)<br>(m) SP ( M = 30 , K = 3) (n) SP ( M = 30 , K = 9) (o) SP ( M = 30 , K = 15)<br>(p) PT ( M = 30 , K = 3) (q) PT ( M = 30 , K = 9) (r) PT ( M = 30 , K = 15)<br>**----- End of picture text -----**<br>


Fig. 19. Path set generation results in different setups using SP and PT methods. Red paths are pivot paths in SP and repositioned pivot paths in PT. Other agent paths are in blue. 

