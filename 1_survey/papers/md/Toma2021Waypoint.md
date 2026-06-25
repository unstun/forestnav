---
citation_key: Toma2021Waypoint
arxiv_id: 2105.00312
arxiv_url: https://arxiv.org/abs/2105.00312
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-24T16:32:20Z
origin: ai+web
reviewed: false
---

# Introduction

Nowadays, mobile autonomous systems are indispensable, used to automate tasks that cannot be performed at large scale or in a safe manner by a human being. Some example applications include search-and-rescue, large-scale manufacturing, and warehouse management. Path planning algorithms have essential applications in these mobile autonomous systems, motivating researchers to design efficient algorithms [@gonzalez2016review].

Currently, there are many classic solutions to the path planning problem. Popular algorithms include A\* [@choset2005principles; @duchovn2014path; @zhang2014multiple; @5937169], Rapidly-exploring Random Tree (RRT) family [@lavalle1998rapidly; @rodriguez2006obstacle; @lavalle2001randomized; @karaman2011sampling], and value iteration on Markovian decision processes (MDP) [@szepesvari2010algorithms; @satia1973markovian]. Furthermore, these algorithms are often offline, requiring complete knowledge of the environment beforehand. Advancements in learned path planning algorithms have been rapid; however, they are often unable to compete with the success rates of classic algorithms. [Search or graph-based algorithms such as A\* and Dijkstra produce optimal solutions but require to search a large portion of the configuration space. This becomes computationally expensive in large maps or motions with high degrees of freedom. Though sampling-based algorithms such as RRT reduce the space/time complexity, the results are often sub-optimal. The problem that we try to tackle in this paper is to reduce the search space, and therefore the time/space complexity, of the A\* algorithm by learning better heuristics.]{style="color: black"}

To solve these issues, we propose *waypoint planning networks (WPN)*, a hybrid algorithm using a local kernel, typically a classic algorithm such as A\*, and a global kernel using a learned algorithm. In this paper, the scope of the design and experimentation is limited to 2D planning, i.e. floorplan-like environments, which is suitable for many indoor mobile robotic applications. We show that WPN produces a more computationally efficient and robust solution. It is able to work with partial knowledge of the environment. To evaluate WPN, we generate maps with a benchmarking platform, PathBench [@pathbench], and compare it against A\*, as well as related works including value iteration networks (VIN) [@tamar2016value] and motion planning networks (MPNet) [@qureshi2019motion]. Experimental results outline the benefits of WPN, both in efficiency and generalization. WPN generates near-optimal solutions but with reduced search space, compared with A\*. [A reduced search-space, which directly translates to reduced memory utilization, is particularly important in robotics and embedded devices with limited resources.]{style="color: black"} Fig. [1](#fig: intro_show){reference-type="ref" reference="fig: intro_show"} shows an example run of the algorithm compared with A\*. In this case, the search space, i.e. the visited cells, by both algorithms are shown in gray.

:::: {#fig: intro_show .figure latex-placement="t!"}
![(a) waypoint planning networks (WPN)](Toma2021Waypoint_figs/Figure1_wpn-map.png){width="\\linewidth"}

![(b) A\* algorithm](Toma2021Waypoint_figs/Figure1_AStar.png){width="\\linewidth"}

::: caption
Evaluation of waypoint planning networks and A\* paths on a real map, from the red start point to the goal. Gray cells show the search space. Cyan disks show the waypoints. WPN's search space is significantly smaller than A\*.
:::
::::

:::: {#fig:my_label .figure latex-placement="ht!"}
![](Toma2021Waypoint_figs/WPN.png){width=".95\\textwidth"}

::: caption
Overview of the waypoint planning networks (WPN) architecture. [The start point, goal point, and a compact representation of the map are used to generate waypoints between start and goal points. A\*, as a local kernel, is used to plan paths between the waypoints.]{style="color: black"}
:::
::::

# Related Work

**Classic planning** methods can be broadly categorized into four groups: graph search, sampling-based, interpolating curve, and numerical optimization [@gonzalez2016review]. Graph search performs its search in a state space that is generally represented as an occupancy grid or lattice, and encompasses prominent algorithms such as A\* [@choset2005principles; @duchovn2014path; @zhang2014multiple; @5937169], Dijkstra [@choset2005principles; @zhang2014multiple], wavefront [@choset2005principles; @luo2014effective], and bug algorithms [@choset2005principles; @rajko2001pursuit], to name a few. Unlike graph search, sampling-based planners, e.g. Rapidly-exploring Random Tree (RRT) [@lavalle1998rapidly] and Probabilistic Roadmap (PRM) [@kavraki1994probabilistic], can operate in high dimensional spaces more efficiently by randomly sampling in either the configuration or state space, but these methods come at a cost of sub-optimal solutions. Where the previous two methods plan on the global scale, interpolating curve planners [@reeds1990optimal; @funke2012up; @xu2012real] use local planning; given a set of waypoints, these methods generate a local path whilst optionally considering a set of constraints. Finally, numerical optimization methods, aim to optimize an objective function, often with a set of constraints. Previously, these methods were often used to smooth prior computed trajectories [@dolgov2010path] or used to compute trajectories from kinematic constraints [@ziegler2014making]; however, with the advent of deep learning, these optimization methods have become very diverse, to which we now discuss.

**Learning-based planning algorithms** have increasingly become more common [@Chen2016Humanoids], [@gupta2017cognitive], [@inoue2019robot], [@NeuralRRT]. In most learning-based path planning algorithms, imitation learning [@ross2011reduction] plays a key role [@TDPPNet]. Neural networks have been used to improve the classic algorithms, for instance by adaptively sampling a particular region of a configuration space in sampling-based algorithms [@qureshi2018deeply]. A similar concept was used by Chamzas et al. [@chamzas2019using]. In both works the computational complexity has been reduced compared to classic methods. Other methods use neural networks to generate a complete path. For instance, motion planning networks (MPNet) encodes the point cloud measurements of the workspace to generate a path from start to goal [@qureshi2019motion], [@qureshi2020motion]. MPNet works 3$\times$ faster than BIT\* [@{Bit*}]. Qureshi et al. formulate constraints into MPNet, and present CoMPNet, which encompasses kinematic constraints [@CoMPNet]. A similar work is done in [@Johnson_IROS_2020]. Bency et al. present OracleNet, a recurrent neural network (RNN)-based approach to generate fast near-optimal paths for robotic arms [@bency2019neural]. OracleNet needs training on each new environment which makes the algorithm suitable for static environments.

**Reinforcement Learning** (RL) approaches such as value iteration networks (VINs) [@tamar2016value], [@Levine2013], learning-from-demonstration (LfD) [@Abbeel2010], guided policy search (GPS) [@Levine2013], and universal planning networks (UPN) [@srinivas2018universal] have also been used for path planning. Wu et al. present three-dimensional path planning network (TDPP-Net) [@TDPPNet], which is an end-to-end network that predicts 3D actions via 2D CNNs. TDPP-Net learns a policy via supervised imitation learning from the Dijkstra's algorithm. These methods often use differentiable models of neural networks and are able to learn to plan. We compare WPN with VINs, as well as MPNet [@qureshi2019motion] and two other RNN-based algorithms [@nicola2018lstm] and [@inoue2019robot]. The comparisons are preformed on synthetic maps of different sizes [@pathbench], real-world maps [@first_map], [@second_map], [@third_map], and HouseExpo maps [@houseexpo].

# Network Architecture {#sec:wpn}

Fig. [2](#fig:my_label){reference-type="ref" reference="fig:my_label"} demonstrates the architecture of the waypoint planning networks. The inputs of the network are the current (partial) 2D map, the start point, and goal point. Given the start point, WPN finds a waypoint and repeats the process from the waypoint as the next start point, until it achieves the goal. The algorithm has a global kernel and a local kernel. The global kernel is responsible for finding a set of waypoints towards the goal. The local kernel uses a classic algorithm to find a path between the waypoints. The global kernel has four modules: *View Module*, *Map Module*, *Bagging Module*, and *Waypoint Module*.

The view module utilizes the current information provided by the sensor, in this case a typical measurement from a scanning laser ranger. The map module utilizes the current (partial) map of the environment, in this case a grid map. The bagging and waypoint modules together find the best waypoints. These modules are explained next.

## View Module {#sec:view_module}

The *view module* uses an LSTM network [@hochreiter1997long] to retrieve the next action that the agent should take given the current location data (pose and local surroundings information). This module is based on [@nicola2018lstm], with some architectural and logic changes. The concept behind having this module is to allow the network to learn a path towards a goal in simple environments. The LSTM architecture takes four inputs: (1) the normalized distance between the agent to obstacles on all eight directions of the Moore neighborhood, [an 8D vector]{style="color: black"}, (2) the normalized direction to the goal, [a 2D vector,]{style="color: black"} (3) the angle defined by the direction to the goal (not required to be normalized as it is already bounded by definition), and (4) the normalized distance to the goal. The model contains a hidden state and cell state which are initialized at each new batch with a zero-tensor of size $2 \times lstm\_layers \times batch\_size \times lstm\_output\_size$. The architecture has the following structure: one batch normalization layer, two LSTM layers, one batch normalization layer, and one linear layer. The network uses the cross entropy loss function. This module exhibits a greedy behaviour. It has a good success rate when there are direct routes, but fails when the path is complex, such as u-turns.

## Map Module {#sec:map_module}

The *map module* has both Convolutional Auto-encoder (CAE) [ [@inoue2019robot], similar to [@Everett_IROS_2019],]{style="color: black"} and LSTM components and attempts to fix some issues, e.g. greediness, that are present in the *view module* (i.e. the algorithm does not know how to navigate between complex obstacles and long corridors). This is done by augmenting the input from the LSTM network with the compressed global image snapshot. When we are dealing with partially known environments, we still use the global image snapshot, but we include the unknown environment as well. The global snapshot is compressed using a CAE (See Fig. [2](#fig:my_label){reference-type="ref" reference="fig:my_label"}, top left, [$M$ is the map, $\hat{M}$ is the reconstructed map, and $z$ is the learned latent variable]{style="color: black"}). The CAE encoder contains four convolutional layers and one linear layer. Each convolution layer is composed of multiple layers placed in the following order: convolutional layer, batch normalization layer, max pool, and leaky ReLU as the activation function. The final layer of the encoder is a linear layer with another batch normalization layer. The CAE decoder contains one linear layer and four de-convolutional layers. Each de-convolutional layer is composed of multiple layers placed in the following order: de-convolutional layer, batch normalization layer, and ReLU activation function. The last de-convolutional layer has Tanh activation function as the input is normalized in the range \[-1, 1\] and the output of Tanh matches it. The CAE is trained on the map training datasets, which is a collection of synthetically generated maps.

## Bagging Module {#sec:bagging}

The *view* and *map modules* behave differently depending on the map layout. Moreover, the same behaviour variability exists when training the models on uncorrelated datasets. The *bagging module* is a solution inspired by ML ensemble methods which combines the previous two modules into a unique best-of-all kind of algorithm [@dietterich2000ensemble]. The bagging planner attempts to boost the performance of the previous modules by picking the best solution depending on the layout of the environment.

Ensemble ML methods use multiple weak learners and output a majority voting consensus. Ensemble ML is split into two categories: sequential and parallel. Sequential ensemble ML (e.g. AdaBoost) trains the weak learners sequentially on the same dataset. We focus on the parallel ensemble methods which train all weak learners at the same time in parallel, but on different training datasets sampled from the original dataset. Thus, the weak learners are not correlated, and each one of them learns different features. Lastly, by having multiple uncorrelated weak learners, the voting procedure increases the accuracy of the predictions.

We use the *view* and *map* modules as weak learners. Since the models can be trained on different training datasets, weak learners learns how to behave in different environments and are uncorrelated. In run time, weak learners are executed in parallel on the map. If any/multiple kernels have found the goal, we pick the one which has lower traversed length. Otherwise, we pick the kernel which has made the furthest progress. Using the *bagging* module, the success rate of finding the goal is significantly increased compared to the *view* and *map* modules.

## Waypoint Module

The previous three modules, *view*, *map*, and *bagging* are able to generate paths from start to goal points sequentially. However, the success rates of these modules, as shown in the experiments, are still not comparable to the success rate of A\*. This is particularly more evident in long sequences. The *waypoint* module has been designed to fix this problem and increase the success rate.

The *waypoint* module is responsible for suggesting a series of waypoints which will guide the agent through the environment. To generate waypoints, any of the previous three modules may be use, but the *bagging* module performs the best. The algorithms used for waypoint generation is referred to as a global algorithm (kernel), GK, for simplicity. The waypoint generation is achieved by bounding the number of iterations of the global kernel, e.g. the bagging module.

Once the waypoints are known, a local kernel, LK, is responsible for planning a path for actual manoeuvring between the waypoints. Any classic solution can be used as the local planner, but we have decided to use A\* as it represents the base algorithmic frame of reference against all other proposed solutions. [The waypoint module is essential in the achieved success rates of WPN. This is demonstrated in experiments.]{style="color: black"}

# Experimental Results {#sec:result}

:::: {#fig: Way runs comp .figure}
:::: figure
::: caption
:::
::::

:::: figure
::: caption
Uniform Random-fill
:::
::::

:::: figure
::: caption
Block
:::
::::

:::: figure
::: caption
House-style
:::
::::

:::: figure
::: caption
:::
::::

![57.36 (m), **185** (cell)](Toma2021Waypoint_figs/way-point_nav_1.png){width="\\linewidth"}

![95.11 (m), **387** (cell)](Toma2021Waypoint_figs/way-point_nav_2.png){width="\\linewidth"}

![99.30 (m), **618** (cell)](Toma2021Waypoint_figs/way-point_nav_3.png){width="\\linewidth"}

:::: figure
::: caption
:::
::::

![**54.04** (m), 467 (cell)](Toma2021Waypoint_figs/a_star_1_map.png){width="\\linewidth"}

![**68.38** (m), 1054 (cell)](Toma2021Waypoint_figs/a_star_2_map.png){width="\\linewidth"}

![**87.74** (m), 1381 (cell)](Toma2021Waypoint_figs/a_star_3_map.png){width="\\linewidth"}

::: caption
WPN (first row) vs A\* (second row) in random, block, and house maps. Gray cells show the search space. Numbers indicate *path length (m) and search space (cell)*.
:::
::::

::: table*
[]{#tab:specific label="tab:specific"}
:::

In this section, several experiments are presented, under three subsections, briefly outlined below. The first two experiments compare WPN against bagging module, view module [@nicola2018lstm], map module [@inoue2019robot], VIN [@tamar2016value], and MPNet [@qureshi2019motion].

***  1) Generalized Benchmarking***: This benchmarking uses the models trained on a variety of synthetic maps, generated in PathBench [@pathbench]. They are trained on 30,000 64$\times$`<!-- -->`{=html}64 size maps, split equally between uniform random-fill, block, and house-style maps (See Fig. [3](#fig: Way runs comp){reference-type="ref" reference="fig: Way runs comp"}). They are then tested on a test-set of 3000 maps, equally divided by size and type (house and uniform random-fill). This highlights the ability of the algorithm to generalize on map sizes it has not been trained on.

***  2) HouseExpo Benchmarking***: This benchmarking involves the generalized models running on maps from the HouseExpo dataset [@houseexpo], modified to a 100$\times$`<!-- -->`{=html}100 size.

***  3) Real-world***: We run WPN on a robot in real-world and also demonstrate WPN vs A\* on a few real-world maps and a Gazebo world.

***  4) Large maps***: Finally, we test WPN, A\*, View and Map modules on larger environments (512$\times$`<!-- -->`{=html}512). This outlines the importance of the waypoint module.

## Generalized Benchmarking: Synthetic Maps {#sec:Generalized}

For training of WPN, View Module [@nicola2018lstm], Map Module [@inoue2019robot] and Bagging module, three types of synthetic maps of size 64$\times$`<!-- -->`{=html}64 pixels were procedurally generated: uniform random-fill map, block map, and house-style map (see Fig. [3](#fig: Way runs comp){reference-type="ref" reference="fig: Way runs comp"} for samples). In these maps, start and goal points are chosen randomly. Evaluations are done over maps that have never been seen by the algorithms. The algorithms were trained on 30,000 64$\times$`<!-- -->`{=html}64 maps, equally divided between the three map types. They were then tested on 3000 of each sized map, 8$\times$`<!-- -->`{=html}8 maps, 16$\times$`<!-- -->`{=html}16, and 28$\times$`<!-- -->`{=html}28 maps, split between uniform random-fill and house maps. They were also tested on 1500 64$\times$`<!-- -->`{=html}64 maps, of the same format. [Training parameters are as follows: view module was trained with 100 epochs, batch size of 50, input size of 12, and output size of 8 Map module was trained with 50 epochs, batch size of 50, input size of 112, and output size of 8. Training logs can be found in the GitHub repo.]{style="color: black"}

To demonstrate why such an architecture was chosen for WPN, we present the performance of its individual modules, i.e. *view*, *map*, *bagging* modules. Note that these do not produce any waypoints, rather they plan a path in one go, cell by cell. As discussed in the previous section, the bagging module is the best of map and view modules and that is why it outperforms the other two.

In addition to the WPN algorithm, we will include two other variation of WPN. These are different only in their global kernels, GK. *WPN* uses the bagging module as GK, while *WPN-view* uses the view module and *WPN-map* uses the map module as GKs.

We compare WPN and all its variants with VIN [@tamar2016value]. VIN was trained four times to produce four different models. One model for each size, 8$\times$`<!-- -->`{=html}8 maps, 16$\times$`<!-- -->`{=html}16 maps, and 28$\times$`<!-- -->`{=html}28 maps are trained on 60,000 maps. The 64$\times$`<!-- -->`{=html}64 model was trained on 30,000 maps due to computational limitations. The testing uses the corresponding trained model. This approach of training gives VIN a competitive advantage; each models is tuned for a specific size. In addition to the standard implementation of VIN based on [@tamar2016value], we also compare the results with VIN64. VIN64 was only trained on 30,000 64$\times$`<!-- -->`{=html}64, like WPNs, then tested on all sizes, similar to WPNs.

MPNet was trained in the same manner as VIN64. MPNet uses two neural models for planning, with the first being an encoder network that embeds obstacle point clouds into latent space and the second network being the planning network that learns to plan a path with the map embedding [@qureshi2019motion]. MPNet's encoder and planning networks were trained similar to the approach taken for the training of the WPN variations.

To evaluate the results maps, five metrics are used:

1.  **Succ. R**: success rate, defined as the percentage of the successful trajectories created from the entire test. Note that in VIN, the maps with no paths between the start and goal points were discarded, leading to 100% success rate. We define the success rate differently, by not discarding the maps when no paths exist, to calculate the *distance left* metric below.

2.  **Dev.**: deviation from the optimal classic path, i.e. A\*.

3.  **Comp.**: computation time in seconds.

4.  **Dist. Left**: distance left to goal when failed, either because there is no path or the algorithm was not successful in finding a path.

5.  **Search**: session search space, which is cells visited divided by total cells in a given map.

We report the averaged metrics for each test set. Another metric, map occupancy, was used to estimate the extent to which maps are occupied by obstacles. Table [1](#tab:mapoccupancy){reference-type="ref" reference="tab:mapoccupancy"} shows the occupancy rate of each map size. Results was computed using an Intel i7-6500u w/4 cores, 12GB, and an Nvidia GeForce 940M. Table [\[tab:specific\]](#tab:specific){reference-type="ref" reference="tab:specific"} presents detailed comparative results. Based on the results, WPN, WPN-map, WPN-view, and A\* are able to find a path if available. Note that the reason even A\* does not have 100% success rate is that for some of the start/goal points, no path exists. According to Table [1](#tab:mapoccupancy){reference-type="ref" reference="tab:mapoccupancy"}, 8$\times$`<!-- -->`{=html}8 maps have the highest occupancy percentage, which means for randomly selected start/goal points, it is more likely that a path does not exist. This is why the success rate of 8$\times$`<!-- -->`{=html}8 is less than the other maps, even for A\*. On small maps, i.e. 8$\times$`<!-- -->`{=html}8 and 16$\times$`<!-- -->`{=html}16, the deviation of WPN from the optimal path is the least. On large maps, the deviation of WPN-map is less than the deviation of WPN. Additionally, when these algorithms fail, for the start/goal pairs with no paths, almost in all cases, WPN's *Dist. Left* metric is the smallest.

In terms of the computation time, none of the WPN variations are comparable to A\*; however, all WPNs have smaller search space; which makes WPNs suitable for devices with low capabilities for search space, e.g. low memory. [Additionally, it is important to note, that while A\* runs on CPU memory, WPN will run the global kernel on GPU memory. Combining this with the reduced search space allows for decreased load on the system's CPU and memory.]{style="color: black"} In summary, compared with A\*, WPNs have smaller search space at the cost of being near-optimal. All models are available on the website of the project.

Compared with VIN and VIN64, WPN is consistently superior in success rate and deviation. Moreover; the performance of VIN degrades significantly as the size of the maps grow. Note that VIN and VIN64 are based on reinforcement learning and the search space for them is not applicable.

Finally, MPNet has better computation time on the benchmark maps compared with WPN, but is unable to achieve high success rates. To have a fair comparison, MPNet was retrained with the benchmark maps like other algorithms.

![Results from HouseExpo [@houseexpo]. WPN, A\*, View Module, Bagging Module, MPNet, and VIN were run on three different HouseExpo maps. The search space of the WPN and A\* algorithms can be seen in gray.](HouseExpo/houseexpo_results2_reordered.pdf){#fig:he_maps width="\\textwidth"}

## Ablation Study {#sec:ablation}

[To justify WPN's architecture and its high success rate, we compare WPN against it's own components: view module, map module and bagging module. These individual modules of WPN were also trained and benchmarked the same way that WPN was trained. This is as an ablation study, and the results show that the individual modules are not able to achieve the performance of WPN, particularly in terms of the success rate. Note that the deviation from the optimal path is computed for the successful cases only, and this explains the better deviation percentage for those modules. The results can be seen in Table [\[tab:specific\]](#tab:specific){reference-type="ref" reference="tab:specific"}. Without the waypoint module the success rates are not competitive to A\*, as they are with WPN when including waypoint module. This is predicted, as the local kernel planner is more successful in the smaller, known environments. Whereas the actual generation of the waypoints is done through the learned global kernel. The ability to generate learned waypoints and have a local kernel plan between them is what accounts for WPN's high success rates. ]{style="color: black"}

## HouseExpo Benchmarking: Simulated Real-world Maps

:::::::::::: {#fig:realmaps .figure}
::: minipage
:::

::: minipage
![](Toma2021Waypoint_figs/screenshot_147.png){width=".95\\columnwidth"}
:::

::: minipage
![](Toma2021Waypoint_figs/screenshot_149.png){width=".95\\columnwidth"}
:::

::: minipage
![](Toma2021Waypoint_figs/screenshot_134.png){width="\\columnwidth"}
:::

\

::: minipage
:::

::: minipage
![](Toma2021Waypoint_figs/screenshot_146.png){width=".95\\columnwidth"}
:::

::: minipage
![](Toma2021Waypoint_figs/screenshot_126.png){width=".95\\columnwidth"}
:::

::: minipage
![](Toma2021Waypoint_figs/screenshot_107.png){width="\\columnwidth"}
:::

::: caption
WPN (first row) vs A\* (second row) in real-world maps, [@first_map], [@second_map], [@third_map]. Gray cells show the search space.
:::
::::::::::::

This experiment is designed to demonstrate the transferablity of the learned algorithm from synthetic maps to real-world maps. Here we use HouseExpo dataset [@houseexpo], which is a large-scale 2D floor plan dataset built on SUNCG [@suncg] dataset. We also test WPN on occupancy grid maps produced by SLAM. The maps that have been used are the following works: [@first_map], [@second_map] and [@third_map].

From the HouseExpo dataset, 30 random maps were downsized to 100$\times$`<!-- -->`{=html}100 sizes. The maps were zero padded to make them square, then they were converted to PathBench acceptable format using the PathBench generator. All algorithms have higher success rates in HouseExpo, since these maps, based on Table [1](#tab:mapoccupancy){reference-type="ref" reference="tab:mapoccupancy"}, have low occupancy, and therefore it is more likely to find a path.

The algorithms used the same training models as Section [4.1](#sec:Generalized){reference-type="ref" reference="sec:Generalized"}. Results can be seen in Table [2](#tab:houseexpo){reference-type="ref" reference="tab:houseexpo"}. [Results were computed on Intel Silver 4216 Cascade Lake, 32 cores w/ 128GB RAM and an Nvidia V100 Volta GPU]{style="color: black"} We can see the results of WPN over all the other algorithms, where it surpasses in success rate and search space. WPN-map which uses the map module as its global kernel has the least deviation metric in indoor maps. Three HouseExpo maps with their paths are shown in Fig. [4](#fig:he_maps){reference-type="ref" reference="fig:he_maps"}. All algorithms were not shown due to space limitation.

::: {#tab:mapoccupancy}
          **Map**           **8$\times$`<!-- -->`{=html}8**   **16$\times$`<!-- -->`{=html}16**   **28$\times$`<!-- -->`{=html}28**   **64$\times$`<!-- -->`{=html}64**   **HouseExpo**
  ------------------------ --------------------------------- ----------------------------------- ----------------------------------- ----------------------------------- ---------------
   **Map Occupancy (%)**                 23.6                               17.6                                16.1                                13.9                      3.58

  : Percentage occupied by obstacles for the maps.
:::

[]{#tab:mapoccupancy label="tab:mapoccupancy"}

::: {#tab:houseexpo}
  ------------------------------- --------- ------------ ------------ ------ ----------
            **Planner**                                                      
           **Rate (%)**                                                      
                (%)                                                          
               (sec)                                                         
           (when failed)                                                     
              **(%)**                                                        
                WPN                **100**     -29.6        8.235       0       1.12
             WPN-view              **100**     -38.5        1.5476      0     **1.07**
              WPN-map              **100**   **-13.96**     1.4708      0       1.28
                A\*                **100**       0        **0.2414**    0       6.12
          Bagging module            90.0       -1.89        4.364      1.06      NA
   View module [@nicola2018lstm]    76.60      -1.99        0.3948     5.72      NA
   Map module [@inoue2019robot]      80        -3.54        0.2932     5.85      NA
       VIN [@tamar2016value]        51.72      -50.2        0.349      50.8      NA
    MPNet [@qureshi2019motion]      83.33      -42.3        0.658      64.8      NA
  ------------------------------- --------- ------------ ------------ ------ ----------

  : Generalization results of the algorithms on 30 100$\times$`<!-- -->`{=html}100 HouseExpo [@houseexpo].
:::

[]{#tab:houseexpo label="tab:houseexpo"}

WPN was trained only on synthetic images. Fig. [5](#fig:realmaps){reference-type="ref" reference="fig:realmaps"} highlights the performance of the WPN against A\* on the real-world occupancy grid maps. The gray cells demonstrate the search space of both algorithms. We can notice that the algorithm maintains the same behaviour across different environments which confirms the robustness to unknown environments. This is intuitively correct, as we have used machine learning methods to find the path, and thus, we inherit the generalization properties.

:::::::::::: {#fig: robot_run .figure}
::: minipage
![](Toma2021Waypoint_figs/start_2.JPG){width="\\linewidth"}
:::

::: minipage
![](Toma2021Waypoint_figs/2.JPG){width="\\linewidth"}
:::

 

::: minipage
![](Toma2021Waypoint_figs/4.JPG){width="\\linewidth"}
:::

::: minipage
![](Toma2021Waypoint_figs/final.JPG){width="\\linewidth"}
:::

::: minipage
![](Toma2021Waypoint_figs/start_2.png){width="\\linewidth"}
:::

::: minipage
![](Toma2021Waypoint_figs/2_2.png){width="\\linewidth"}
:::

::: minipage
![](Toma2021Waypoint_figs/4_2.png){width="\\linewidth"}
:::

::: minipage
![](Toma2021Waypoint_figs/final_2.png){width="\\linewidth"}
:::

::: caption
Real-world robot navigation using WPN via ROS. The robot is asked to move to a target in the adjacent room, while there is no global map available. Top row represents real-world view of the robot, the second row represents the live map, as being updated (left to right shows the progress through time). The true dimension of the grid is 128$\times$`<!-- -->`{=html}128.
:::
::::::::::::

:::::: {#fig:ros-exploration .figure}
::: minipage
![](Toma2021Waypoint_figs/WPN.png){width="\\linewidth"}
:::

::: minipage
![](Toma2021Waypoint_figs/Astar.png){width="\\linewidth"}
:::

::: caption
WPN-map vs A\* on the live exploration experiment in an unknown Gazebo world. A\* uses the frontier exploration algorithm and subsequently plan to the goal. WPN-map is able to plan and explore simultaneously. The map size is 128$\times$`<!-- -->`{=html}128 and Turtlebot3 with a scanning laser ranger is used.
:::
::::::

:::: {#fig:largemaps .figure latex-placement="t"}
![image](Toma2021Waypoint_figs/astar.png){width=".45\\columnwidth"} ![image](Toma2021Waypoint_figs/wpn-view.png){width=".49\\columnwidth"}

::: caption
City maps (512$\times$`<!-- -->`{=html}512) used for large map experimentation. A\* path on the left, and WPN-view on the right
:::
::::

## Real-world and Gazebo Experiments

Several real-world experiment were done with a differential drive robot, one of which reported here, the rest are in the video. The robot has a YDLidar sensor, a 360-degree two-dimensional scanning laser ranger, used to generate a 2D map using the GMapping algorithm [@gmapping]. The motherboard of the robot is a Raspberry Pi board which is running Raspbian, and makes use of ROS. The robot is asked to move from one room to another, without having a global map. This is a task that A\* is not able to find a path for. Using WPN, the algorithm suggests a waypoint and a path to it, then the robot navigates to the waypoint. While the map gets updated, WPN updates the waypoints to guide the robot to the final goal. Fig. [6](#fig: robot_run){reference-type="ref" reference="fig: robot_run"} showcases the robot.

We also run another experiment in Gazebo to further demonstrate the benefit of WPN over A\*. In this experiment, the frontier exploration algoritm [@Yamauchi] has been added to the A\* algorithm. A simple world was generated in Gazebo, with a start and goal point chosen. The map is unknown and planning was done with WPN-map and A\* with frontier exploration, on a Turtlebot3 robot with a scanning laser ranger. A\* must explore and subsequently plan. WPN is able to simultaneously plan and explore, which leads to a lower overall path length compared to A\* with exploration. This can be seen in Figure [7](#fig:ros-exploration){reference-type="ref" reference="fig:ros-exploration"}. The start point is on the left side, the goal is on the right side.

## Large Maps

[To demonstrate the performance of WPN in larger map environments, we test the algorithm on 30 large 2D environments, and compare them to A\*.]{style="color: black"} Real world city maps [@sturtevant2012benchmarks] are used for testing. These maps are 512$\times$`<!-- -->`{=html}512. WPN was trained on 45,000 64$\times$`<!-- -->`{=html}64 maps, split between types uniform random fill, block map, and house maps. Computation was done on an Intel Silver 4216 Cascade Lake CPU (16 cores) with 64GB memory, and an Nvidia V100 GPU. Results can be seen in Table [\[tab:largemaps\]](#tab:largemaps){reference-type="ref" reference="tab:largemaps"}. Sample runs can be seen in Figure [8](#fig:largemaps){reference-type="ref" reference="fig:largemaps"}. [It can be seen that WPN and it's variants are able to compete with A\* in terms of success rate, while maintaining a significantly lower search space. We also compare other ML approaches, all of which perform rather poorly on these large scale environments. We can see that WPN performs very well on large scale maps. The success rate can be attributed to the waypoint module, as discussed in Section [4.2](#sec:ablation){reference-type="ref" reference="sec:ablation"}]{style="color: black"}

[]{#tab:largemaps label="tab:largemaps"}

# Conclusion {#sec:conclusion}

In this paper a novel learning-based path planning algorithm was proposed. The algorithm, waypoint planning networks (WPN), was trained with synthetic maps and tested on various types of maps and a real robot. WPN presents a significant advantage over A\* in terms of search space, while achieving the success rate of A\*. WPN has the benefit of working with partial maps, while also maintaining a high efficiency and low deviation from A\*. It also provides a significant advantage over other learning-based algorithms in terms of success rate and deviation from optimal paths. WPN also generalizes more successfully than other learned algorithms and is easily trained. [It is able to compete with A\* on large scale environments, where other learned approaches perform poorly.]{style="color: black"} It takes advantage of the benefits of both learned algorithms and classic algorithms.

In the future, WPN will be optimized to use a different global kernel, such as generative adversarial networks. WPN will be trained on different real-world datasets, to generate better results. We also plan to improve multiprocessing on WPN, which will significantly improve computation time. Moreover, we plan to extend WPN to 3D maps and higher dimensions to perform path planning for higher degrees-of-freedom and complex robotic systems such as manipulators. [Also, we will include kinematics constraints in the architecture to account for real-world physical constraints.]{style="color: black"}

# Acknowledgment {#acknowledgment .unnumbered}

This work was partially funded by DRDC-IDEaS (CPCA-0126). We gratefully acknowledge the support of NVIDIA Corporation with the donation of the Titan Xp GPU used for conducting experiments.

[^1]: [https://sites.google.com/view/waypoint-planning-networks](https://sites.google.com/view/waypoint-planning-networks/home)

[^2]: $^{\dagger}$Imperial College London$^{\star}$Ryerson University
