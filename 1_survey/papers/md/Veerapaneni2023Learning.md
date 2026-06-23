---
citation_key: Veerapaneni2023Learning
arxiv_id: 2303.09477
arxiv_url: "https://arxiv.org/abs/2303.09477"
title: "Learning Local Heuristics for Search-Based Navigation Planning"
authors_short: "Rishi Veerapaneni et al."
year: 2023
direction_tag: E_bounded_suboptimal_search
source: pymupdf4llm
converted_at: 2026-06-23T19:44:52Z
origin: ai+web
reviewed: false
---

## **Learning Local Heuristics for Search-Based Navigation Planning** 

## **Rishi Veerapaneni, Muhammad Suhail Saleem, Maxim Likhachev** 

Robotics Institute, Carnegie Mellon University _{_ rveerapa, msaleem2, mlikhach _}_ @andrew.cmu.edu 

## **Abstract** 

Graph search planning algorithms for navigation typically rely heavily on heuristics to efficiently plan paths. As a result, while such approaches require no training phase and can directly plan long horizon paths, they often require careful hand designing of informative heuristic functions. Recent works have started bypassing hand designed heuristics by using machine learning to learn heuristic functions that guide the search algorithm. While these methods can learn complex heuristic functions from raw input, they i) require a significant training phase and ii) do not generalize well to new maps and longer horizon paths. Our contribution is showing that instead of learning a global heuristic estimate, we can define and learn local heuristics which results in a significantly smaller learning problem and improves generalization. We show that using such local heuristics can reduce node expansions by 2-20x while maintaining bounded suboptimality, are easy to train, and generalize to new maps & long horizon plans. 

## **1 Introduction** 

Motion planning has many applications like autonomous car navigation, robotic arm manipulation, and multi-agent warehouse autonomy. Graph search is one popular class of motion planning methods which relies on typically handdesigned informative heuristics (cost-to-go estimates) for competitive performance (2008; 2014; 2015; 2019). 

The majority of graph search algorithms assume known environmental knowledge (i.e. the graph) to compute valid/invalid nodes and edges for the search algorithm. Given this transition information, heuristic search algorithms can directly work on maps without any computationally expensive pre-training phase. These methods can also solve long horizon tasks out-of-the-box without any algorithmic changes. Additionally heuristic search algorithms have strong theoretical guarantees of completeness and bounded suboptimality given enough computation time. 

Modern machine learning techniques, e.g. reinforcement or imitation learning, on the other hand utilize observational data from the environment to determine paths. These methods bypass needing hand-crafted heuristics by learning complex values and/or policies directly from raw input 

Copyright © 2022, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved. 


![](1_survey/papers/md/Veerapaneni2023Learning_figs/Veerapaneni2023Learning.pdf-0001-11.png)


**----- Start of picture text -----**<br>
Global Problem Local Problem<br>**----- End of picture text -----**<br>


Figure 1: Left: Estimating a _global_ cost-to-go heuristic from the red star state _s_ to the orange goal requires reasoning over a large region. Right: We define and learn a _local_ heuristic centered at _s_ which reasons about vehicle dynamics and obstacles in a local region, that we then combine with the global heuristic. This significantly smaller problem eases the learning progress, enables generalization, and provides significant improvements in some domains. 

and perform well on environments similar to those seen during training. Recent work have started to bridge the gap of heuristic search and machine learning, usually by learning a neural network which returns a heuristic or priority that is used in a search algorithm (typically weighted A*). These methods show improvements in reducing nodes expanded compared to heuristic search and improvements in increasing success rate compared to pure machine learning (2017; 2019; 2020; 2021; 2022). However, most methods require a significant training phase, lack guarantees on completeness or solution quality, and struggle to generalize to long horizon tasks or new maps. 

Our goal is to combine the best of two worlds of heuristic search’s ability to solve long-horizon tasks and machine learning’s ability to incorporate environmental data. Concretely, we would like a method that 1. Uses environment data to speed up performance 2. Is easy to train 3. Generalizes to new maps and long horizon plans 4. Maintains solution completeness and suboptimality guarantees. Our main insight is that instead of learning a global cost-to-go heuristic which becomes exceedingly difficult to train for long horizon plans, we can instead define and learn a _local_ heuristic. Unlike all related literature (to the best of our knowledge) which attempt to directly predict the entire cost-togoal heuristic, we attempt to only predict the cost to escape a small region centered at the current robot state, enabling 


![](1_survey/papers/md/Veerapaneni2023Learning_figs/Veerapaneni2023Learning.pdf-0002-00.png)


**----- Start of picture text -----**<br>
Global Heuristic  Local Heuristic  Combined Heuristic<br>start goal<br>**----- End of picture text -----**<br>


Figure 2: We demonstrate the effect of computing a local heuristic and summing it to get a combined more informed heuristic. The global heuristic _hg_ is the Manhattan distance to the goal ignoring obstacles while the local heuristic reasons about obstacles within a window of _K_ = 3 and inflates heuristic values in the cul-de-sac. Running weighted A* from the start with _hg_ + _hk_ now skips the cul-de-sac compared to running with just _hg_ . 

easy learning for a neural network (see Figure 1). This local estimate is augmented with the global heuristic to provide a more accurate and informative cost-to-go estimate. We employ focal search (Pearl and Kim 1982), a variant of A*, to use the informed heuristic in a manner that provides bounded suboptimal guarantees. We call this framework Local Heuristic A*, LoHA*, and show how LoHA* can effectively generalize and improve performance. 

Succinctly, our main contributions are: 

1. Defining a _local_ heuristic _hk_ that is _independent_ of the full scale planning problem, and using a neural network to estimate its value efficiently. 

2. Combining the local and global heuristic, and using focal search to maintain bounded suboptimality. 

3. Experimentally demonstrating that a learned local 9x9 heuristic can result in 20x node reductions compared to regular weighted A* search on large 1024x1024 maps, and that LoHA* effectively generalizes to new maps. 

## **2 Related work** 

The majority of prior works incorporating machine learning with search-based planning do so by attempting to directly learn the cost-to-go heuristic to the goal state. Agostinelli et al. (2019, 2021) learn such functions on a Rubik Cube and other combinatorial tasks (e.g. 24-tile problem, Sokoban) using reinforcement learning. Kim and An (2020) tests and trains a global heuristic function on _one_ map. Li et al. (2022) impressively, but at the cost of extra machinery, learns an _admissible_ CNN heuristic function to find optimal solutions for tile and TopSpin problems. Jabbari Arfaee, Zilles, and Holte (2011) is an early work which uses curriculum learning and a small NN to learn global heuristics on different classical combinatorial problems (e.g. 3x3 Rubik Cube, 24-tile problem). For all these methods, it is unclear how their learnt heuristic would work on larger horizon problems or similar but different scenarios outside of their training distribution, e.g. a different goal Rubik Cube state, or similarly-generated but larger maps. Our work aims to speed-up search using machine learning in a way which generalizes to new maps. 

A few other works attempt to speed up search by learning different metrics. Bhardwaj, Choudhury, and Scherer (2017) learns a global priority value of features of the search state which determines their expansion policy. On the other hand 

we learn a local heuristic based on local features, which allows our method to be useable across different search instantiations (e.g. different weights). Kaur, Chatterjee, and Likhachev (2021) learns an expansion delay heuristic that speeds up search but must be retrained for new maps. 

We aim to generalize to different maps by limiting the learning problem to a “local” sub-problem. Our local subproblem is loosely related to lookahead in best-first search (Stern et al. 2010) which uses a fixed depth DFS lookahead to update the heuristic in a A* search, but our local heuristic definition is completely different as well as our use of a neural network. Our local definition dramatically eases the learning problem and substantially reduces the required training dataset size, training time, and model size of the neural network while simultaneously enabling it to effectively generalize to different maps. 

## **3 Method** 

Our main motivation is straightforward; simplify the learning problem. Learning a heuristic which estimates the _global_ cost-to-go requires complex reasoning about the entire map. Our main insight is that instead of solving the entire shortest path problem, we define a _local_ problem which is significantly easier to solve, and that solving this local problem can result in a large overall reduction of nodes expanded when used in heuristic search. 

## **Defining the Local Heuristic** 

Heuristic search methods like A* conduct a best first search over states, with their priority _f_ ( _s_ ) equal to the sum of costto-come _g_ ( _s_ ) and cost-to-go estimate _hg_ ( _s_ ). Crucially, _hg_ ( _s_ ) (under)estimates the total cost-to-go, i.e. the best cost to reach the goal state _sg_ from _s_ . We call this a _global_ heuristic _hg_ ( _s_ ), distinct from our local heuristic _hk_ ( _s_ ). This means that as the planning problem gets longer/larger, obtaining accurate _hg_ ( _s_ ) estimates becomes harder. 

We instead propose to learn a local heuristic _hk_ ( _s_ ) that takes full consideration of the robot dynamics and environmental obstacles in a local region of size _K_ around _s_ . Conceptually, _hk_ tries to predict the additional cost required to escape the local region. We can then use _hgk_ ( _s_ ) = _hg_ ( _s_ ) + _hk_ ( _s_ ) during search (see Figure 2). 

Mathematically, given a state _s_ = ( _x, y,_ Ω) with position _x, y_ and other state parameters Ω (e.g. heading, velocity), we define a local region _LR_ ( _s_ ) to contain the states within a window of _K_ , i.e. _LR_ ( _s_ ) = _{s[′] | K ≥|s.x − s[′] .x|, K ≥ |s.y − s[′] .y|}_ . Let _LRB_ ( _s_ ) be the border of this region, i.e. _{s[′] | K_ = _|s.x − s[′] .x| ∨ K_ = _|s.y − s[′] .y|}_ . Conceptually, assuming unit length actions, any path from _s_ to _sg_ must contain a state in _LRB_ ( _s_ ), or directly reach the goal in the local region _LR_ ( _s_ ). If neither are possible from _s_ , then _s_ cannot leave _LR_ ( _s_ ), is in a dead end, and should have an infinite heuristic value. Thus our objective value _hgk_ ( _s_ ) is 


![](1_survey/papers/md/Veerapaneni2023Learning_figs/Veerapaneni2023Learning.pdf-0002-18.png)


Notice how computing _c_ ( _s, s[′]_ ), the minimum cost of a path from _s_ to _s[′]_ , requires incorporating the robot’s dynamics/kinematic constraints as well as local obstacle/environmental data in _LR_ ( _s_ ). We can compute _hgk_ ( _s_ ) at a given state _s_ by running A* following Equation 1, however this becomes slow as the size of _LR_ ( _s_ ) increases. We can instead approximate this value by training a neural network (NN). We can input _s_ , the environment’s data in _LR_ ( _s_ ), and the heuristic data in _LR_ ( _s_ ), and predict _hgk_ ( _s_ ). 

A key problem with this approach is that even though our problem is local, our input _s_ and _hg_ ( _s[′]_ ) are not scaleinvariant. For example, if we trained on small maps, but then evaluated on larger maps, our neural network would be unable to generalize to larger encountered _s_ and _hg_ values. A key observation is that we can make our inputs invariant to any such changes. The state _s_ = ( _x, y,_ Ω) can become just Ω as the local region _LR_ ( _s_ ) is centered at _x, y_ . We remove global dependence on _hg_ ( _s[′]_ ) for _s[′] ∈ LR_ ( _s_ ) by subtracting _hg_ ( _s_ ). Our local invariant heuristic thus becomes 


![](1_survey/papers/md/Veerapaneni2023Learning_figs/Veerapaneni2023Learning.pdf-0003-02.png)


Therefore instead of passing _hg_ into the NN, we only need the relative information _hg_ ( _s[′]_ ) _− hg_ ( _s_ ) _∈ LR_ ( _s_ ). 

We can generalize this definition for non-unit length actions by predicting the additional cost required to _escape LR_ ( _s_ ). We omit the mathematical definitions for brevity but note that our experiments uses this more general version. 

## **Computing Ground Truth hk** 

Equation 2 defines a multi-goal search problem within _LR_ ( _s_ ) where we want to minimize _c_ ( _s, s[′]_ )+ _hg_ ( _s[′]_ ) _−hg_ ( _s_ ). We directly run an A* search starting at _s_ until either of the first two conditions are met, or until it returns no solution found which results in the third _∞_ value. In high dimensional state spaces where the number of states within _LR_ ( _s_ ) is large, it can take prohibitively long for the local search to terminate. We can ease this by conducting a maximum number of expansions and then returning the top _g_ ( _s[′]_ )+ _h_ ( _s[′]_ ) in the queue as this is an underestimate of _hk_ ( _s_ ). 

## **Training Procedure** 

**Neural network inputs:** As described earlier, we want to feed in a locally invariant version of _s_ and _LR_ ( _s_ ) into the neural network. _LR_ ( _s_ ) contains both the obstacle and invariant heuristic values of window _K_ centered at _s_ . 

**Collecting data:** We utilize supervised learning to train a model to learn _hk_ . A naive approach to collect training data is to randomly sample states _s_ . However, this may over sample regions in the state space that are not relevant during runtime and hurt performance. We thus collect training data by running weighted A* with ground truth local heuristic and storing the inputs _s, LR_ ( _s_ ) and corresponding true value _hk_ ( _s_ ) of states _s_ we encounter during search. 

**Neural network output:** Local heuristic value _hk_ ( _s_ ). 

**Loss function:** One issue we discovered when training our neural network is that regressing directly to _hk_ causes 

issue as the mean square error objective prioritizes samples with larger values, reducing the prediction quality for many lower range values. An effective alternate we found was regressing to log( _hk_ + 1) which is a measure of relative error but has better statistical properties than relative error or other alternatives (Tofallis 2015). The +1 is numerically required as _hk_ can equal 0. Additionally we chose to regress to _hk_ = 2 _K_ for dead-ends where _hk_ = _∞_ , which we found to be sufficiently large. 

## **Using the Local Heuristic in Search** 

We use _hgk_ ( _s_ ) = _hg_ ( _s_ ) + _hk_ ( _s_ ) as our heuristic. Conceptually, _hk_ augments _hg_ with local dynamics and obstacle information. If _hk_ ( _s_ ) is computed accurately (e.g. by a local search), _hgk_ ( _s_ ) is guaranteed to be admissible and can be used in A* while guaranteeing optimality. However, if _hk_ is learnt, it can be arbitrarily suboptimal. We therefore employ focal search, using _hg_ as a consistent heuristic in OPEN and _hgk_ ( _s_ ) as an inadmissible heuristic in FOCAL, guaranteeing that our solution is bounded suboptimal. We call this framework of learning a local heuristic, combining it with the global heuristic, and using it in focal search, Local Heuristic A*, or LoHA* for short. 

## **4 Local Heuristic Experiments** 

We experiment using custom random obstacle maps and 6 city maps from (Sturtevant 2012), minimizing travel time between start-goal pairs. We simulate a non-holonomic car with state ( _x, y, θ, v_ ) with positions _x, y_ discretized by 0.5, heading _θ_ discretized by 30 degrees, and velocity _v ∈ {−_ 1 _,_ 0 _,_ 1 _,_ 2 _,_ 3 _}_ . The car follows Ackermann dynamic constraints and every state has unit-cost actions of ∆ _v ∈ {−_ 1 _,_ 0 _,_ 1 _}_ and steering angle _∈ {−_ 60 _, −_ 30 _,_ 0 _,_ 30 _,_ 60 _}_ . Since the max velocity is 3, our _hg_ heuristic is _L_ 2( _s, sgoal_ ) _/_ 3. Our objective with this set-up is to show how a local heuristic can help in complex state and action spaces as opposed to many existing works combining search and machine learning on 4/8-connected grids. We report results for a small local heuristic size of _K_ = 4. Experiments were run on an Ubuntu 20.04 machine with 32-GB Ram and a 11th Gen Intel Core i7-11800H@2.30GHzx16. 

## **Training** 

**Local state input:** We input _LR_ ( _s_ ) as a 2 channel 2 _K_ +1 by 2 _K_ + 1 image centered at (floor( _x_ ) _,_ floor( _y_ )). The first channel is the binary obstacle map, the second the local invariant heuristic _hg_ ( _s[′]_ ) _−hg_ ( _s_ ). We additionally input the local invariant state containing ( _x−_ floor( _x_ ) _, y−_ floor( _y_ ) _, θ, v_ ). 

**Training data:** We run weighted A* with the local heuristic on random start-goal locations on a set of training maps, and collect data on states we have seen. We use a local heuristic expansion limit of 100 to enable faster data collection. Overall the procedure is fast; with unoptimized C++ code we collect on the order of 5000 examples a second. We train on 200,000 states (which can be collected in minutes). We highlight that this contrasts learning a global heuristic where data collection takes longer as each training example requires solving the entire planning problem. 

|Map Type|Split|Method|Reduction in nodes expanded<br><br><br><br>|Reduction in nodes expanded<br><br><br><br>|Reduction in nodes expanded<br><br><br><br>|Reduction in nodes expanded<br><br><br><br>|
|---|---|---|---|---|---|---|
||||_w_2|_w_8|_w_32|_w_128|
|random20|Train|A* w/TL<br>LoHA*|6.76<br>3.53|10.88<br>7.92|12.78<br>10.33|14.7<br>11.6|
||Test|A* w/TL<br>LoHA*|6.6<br>3.57|10.42<br>6.94|14.45<br>10.46|15.75<br>12.67|
|random30|Train|A* w/TL<br>LoHA*<br>|12.21<br>2.16<br>|26.3<br>12.07<br>|40.38<br>18.08<br>|44.02<br>20.51<br>|
||Test|A* w/TL<br>LoHA*|10.36<br>1.68|28.58<br>7.71|43.57<br>13.59|44.3<br>16.55|
|Denver<br>256|Train|A* w/TL<br>LoHA*<br>|2.43<br>1.22<br>|6.45<br>5.15<br>|5.92<br>3.98<br>|7.13<br>6.37<br>|
||Test|A* w/TL<br>LoHA*|4.54<br>1.43|16.37<br>8.43|30.73<br>28.16|29.21<br>30.73|



Table 1: **LoHA* Results —** We report the median multiplicative reduction in nodes compared to weighted A*. We see that LoHA* is able to get larger reductions as the weight _w_ increases, and that we are able to effectively able to generalize to different maps. 

**NN architecture:** We apply a convolutional layer to _LR_ ( _s_ ), flatten out latent vector, append our local invariant state _s_ , and apply two intermediate size 100 MLP layers. 

**Training time:** We train on 200,000 examples for 100 epochs with a batchsize of 32 on CPU, which takes roughly 20-30 minutes. We did not optimize training speed but again we iterate our local problem enables a smaller model and correspondingly smaller compute requirements (i.e. using a CPU and not a GPU, training in minutes and not hours). After training, our squared relative loss saturates around 0.03, corresponding to about 18% absolute relative error. 

## **Results** 

Table 1 reports the median speed-up across several weighted runs of using A* with _hgk_ using the ground Truth Local heuristic (A* w/TL) and LoHA* using a neural network approximation on both the training and testing maps. The “randomN” maps are 1024x1024 maps with N% randomly generated obstacles, split into 7 training and 3 testing maps. The Denver maps are 256x256 split into 2 training maps and 1 testing map. Overall, each training/testing set has about 40/20 individual start-goal pairs correspondingly, with 3 seeds run per configuration. We report the median reduction in nodes expanded compared to the corresponding weighted A* baseline, e.g. a value of 6.76 means the method expands 6.76 times less nodes than weighted A*. 

The “A* w/TL” results reveal the usefulness of the local heuristic in reducing the total number of nodes expanded, ranging from 2-40x depending on the map and heuristic weight _w_ . We see that _hgk_ is more effective when _w_ is larger; this occurs as node expansions for larger _w_ are more likely to occur in local optimas while _hgk_ penalizes these regions more. Additionally, our ability to run A* w/TL informs us of the estimated upper-bound that LoHA* can obtain, and determine regimes where LoHA* would not be effective. This capability is useful for practitioners as they can easily determine beforehand if LoHA* will be useful for their domains. 

LoHA* is able to roughly match the order of magnitude of performance of the true local heuristic. We note that some degradation in performance is expected as LoHA*’s neural 


![](1_survey/papers/md/Veerapaneni2023Learning_figs/Veerapaneni2023Learning.pdf-0004-08.png)


**----- Start of picture text -----**<br>
0.30 NN losses on random30 maps<br>0.25<br>0.20 K=4: Train<br>K=4: Test<br>K=8: Train<br>0.15<br>K=8: Test<br>K=12: Train<br>0.10 K=12: Test<br>0.05<br>0.00<br>0 20 40 60 80 100<br>Training epoch<br>Loss<br>**----- End of picture text -----**<br>


Figure 3: The y-axis is the log relative loss objective; a loss of 0.2 roughly translates to _≥_ 50% absolute relative error, 0.1 to _≥_ 35%. As _K_ increases, the neural network struggles to generalize to the test maps. This supports our motivation that learning a local heuristic eases the learning problem and improves generalization. 

network is a noisy approximation of the true local heuristic, but see that the noisy approximation is still effective in reducing node expansions. Importantly, LoHA* is able to effectively generalize to the test maps not seen in during training. Figure 3 shows how increasing _K_ makes it harder for the neural network to generalize to testing maps, justifying our motivation for using a local and not global heuristic to enable generalization. 

One key limitation with LoHA* is that although it can significantly reduce node expansions, its overall runtime is longer than baseline A*. This occurs as running the neural network in the search is slow; LoHA* expands roughly 4,500 nodes a second (with neural network inference time dominating) while A* with _hg_ expands roughly 140,000 nodes a second. We imagine LoHA* will provide runtime benefits in scenarios where node expansions are more expensive, or by utilizing batch expansions in focal search or GPU optimization (Greco et al. 2022; Li et al. 2022; Veerapaneni and Likhachev 2022). This is independent of our core contribution and is left for the future. 

## **5 Future Work and Conclusion** 

Our key assumption is that we could define a local region around the physical region of the state _s_ of the agent, which works in navigation. Expanding this for other domains, e.g. manipulation, would be interesting future work where defining _LR_ ( _s_ ) could be non-trivial. As mentioned in the previous section, future work could also address the runtime issues of using a neural network in a heuristic search loop. 

We present a framework for extracting, learning, and using local heuristics in heuristic search in navigation planning. Using the local heuristic in a focal A* search results in a significant reduction in nodes expanded compared to regular A*, while maintaining bounded suboptimality gaurantees. We show that learning a local heuristic enables significantly easier data collection, learning, and generalization while decreasing expansions by 2-20x. **Acknowledgements** This material is partially supported by the National Science Foundation Graduate Research Fellowship under Grant No. DGE1745016 and DGE2140739. 

## **References** 

Agostinelli, F.; McAleer, S.; Shmakov, A.; and Baldi, P. 2019. Solving the Rubik’s cube with deep reinforcement learning and search. _Nature Machine Intelligence_ , 1–8. 

Agostinelli, F.; Shmakov, A.; McAleer, S.; Fox, R.; and Baldi, P. 2021. A* Search Without Expansions: Learning Heuristic Functions with Deep Q-Networks. _CoRR_ , abs/2102.04518. 

Aine, S.; Swaminathan, S.; Narayanan, V.; Hwang, V.; and Likhachev, M. 2014. Multi-Heuristic A. In Fox, D.; Kavraki, L. E.; and Kurniawati, H., eds., _Robotics: Science and Systems X, University of California, Berkeley, USA, July 12-16, 2014_ . 

Bhardwaj, M.; Choudhury, S.; and Scherer, S. A. 2017. Learning Heuristic Search via Imitation. _CoRR_ , abs/1707.03034. 

Pearl, J.; and Kim, J. H. 1982. Studies in Semi-Admissible Heuristics. _IEEE Transactions on Pattern Analysis and Machine Intelligence_ , PAMI-4(4): 392–399. 

Stern, R.; Kulberis, T.; Felner, A.; and Holte, R. 2010. Using Lookaheads with Optimal Best-First Search. In Fox, M.; and Poole, D., eds., _Proceedings of the Twenty-Fourth AAAI Conference on Artificial Intelligence, AAAI 2010, Atlanta, Georgia, USA, July 11-15, 2010_ . AAAI Press. 

Sturtevant, N. 2012. Benchmarks for Grid-Based Pathfinding. _Transactions on Computational Intelligence and AI in Games_ , 4(2): 144 – 148. 

Tofallis, C. 2015. A better measure of relative prediction accuracy for model selection and model estimation. _J. Oper. Res. Soc._ , 66(3): 524. 

Veerapaneni, R.; and Likhachev, M. 2022. Non-Blocking Batch A* (Technical Report). 

Ferguson, D.; Howard, T. M.; and Likhachev, M. 2008. Motion planning in urban environments: Part II. In _2008 IEEE/RSJ International Conference on Intelligent Robots and Systems, September 22-26, 2008, Acropolis Convention Center, Nice, France_ , 1070–1076. IEEE. 

Greco, M.; Toro, J.; Ulloa, C. H.; and Baier, J. A. 2022. K-Focal Search for Slow Learned Heuristics (Extended Abstract). In Chrpa, L.; and Saetti, A., eds., _Proceedings of the Fifteenth International Symposium on Combinatorial Search, SOCS 2022, Vienna, Austria, July 21-23, 2022_ , 279– 281. AAAI Press. 

Jabbari Arfaee, S.; Zilles, S.; and Holte, R. C. 2011. Learning heuristic functions for large state spaces. _Artificial Intelligence_ , 175(16): 2075–2098. 

Kaur, J.; Chatterjee, I.; and Likhachev, M. 2021. Speeding Up Search-Based Motion Planning using Expansion Delay Heuristics. _Proceedings of the International Conference on Automated Planning and Scheduling_ , 31(1): 528–532. 

Kim, S.; and An, B. 2020. Learning Heuristic A: Efficient Graph Search using Neural Network. In _2020 IEEE International Conference on Robotics and Automation (ICRA)_ , 9542–9547. 

Li, J.; Felner, A.; Boyarski, E.; Ma, H.; and Koenig, S. 2019. Improved Heuristics for Multi-Agent Path Finding with Conflict-Based Search. In Kraus, S., ed., _Proceedings of the Twenty-Eighth International Joint Conference on Artificial Intelligence, IJCAI 2019, Macao, China, August 1016, 2019_ , 442–449. ijcai.org. 

Li, T.; Chen, R.; Mavrin, B.; Sturtevant, N. R.; Nadav, D.; and Felner, A. 2022. Optimal Search with Neural Networks: Challenges and Approaches. In Chrpa, L.; and Saetti, A., eds., _Proceedings of the Fifteenth International Symposium on Combinatorial Search, SOCS 2022, Vienna, Austria, July 21-23, 2022_ , 109–117. AAAI Press. 

Narayanan, V.; Aine, S.; and Likhachev, M. 2015. Improved Multi-Heuristic A* for Searching with Uncalibrated Heuristics. In Lelis, L.; and Stern, R., eds., _Proceedings of the Eighth Annual Symposium on Combinatorial Search, SOCS 2015, 11-13 June 2015, Ein Gedi, the Dead Sea, Israel_ , 78– 86. AAAI Press. 

