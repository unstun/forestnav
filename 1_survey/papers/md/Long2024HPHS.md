---
citation_key: Long2024HPHS
arxiv_id: 2407.10660
arxiv_url: https://arxiv.org/abs/2407.10660
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-23T19:15:07Z
origin: ai+web
reviewed: false
---

# Introduction

As the autonomous ability of robots has been constantly improved, increasing robots are being used for rescue, mapping, exploration, 3-D reconstruction, and other tasks. However, for various reasons, human operators are not always able to control the robot's movement and complete tasks in real time. Such a situation requires the robot to have higher autonomy and be able to independently decide where to go and complete the mapping of the environment. Therefore, more researches [@yamauchi1997frontier; @perkasa2020improved; @image; @sensor_reading; @huang2023fael] aim at developing autonomous exploration techniques to improve the exploration efficiency of robots in unknown environments.

The mainstream framework of exploration technology mainly includes frontier-based and sampling-based methods. Both methods essentially search the potentially unknown areas of the environment and select the high-revenue one to explore. The boundary of the unknown area is expanded continuously until the whole environment is completely modeled. However, these methods still have some limitations:

- Expensive computation. Most methods need to search the boundary of the unknown environment in a large area or perform a large number of frontier sampling, which is a huge burden for edge computing devices and causes the failure of the robot to respond quickly [@huang2023fael]. When the exploration range increases, the efficiency of sampling becomes lower, resulting in the inability to generate new frontiers in real time.

- Greedy strategy. Common revenue evaluation methods either minimize the distance from the robot to the frontier [@yamauchi1997frontier], or maximize the information gain [@gao2018improved]. However, they all ignore efficient global path coverage, resulting in myopic behaviors of the robot. This leads to backtracking exploration and low efficiency.

:::: {#effect .figure latex-placement="!t"}
![](Long2024HPHS_figs/fig_0.png){width="7.2cm"}

::: caption
A robot performs autonomous exploration in an unknown environment using the proposed method. The yellow points represent the frontier points, the purple point is the next target point, and the black curve is the trajectory of the robot. The green grids are divided subregions.
:::
::::

:::: {#framework .figure latex-placement="!t"}
::: caption
The overall framework diagram of the exploration system.
:::
::::

In this paper, we present a hierarchical planning exploration system based on hybrid frontier sampling. Firstly, the hybrid frontier sampling method is proposed to quickly extract the frontier points by directly using LiDAR data and local map information. Then, the hierarchical planning strategy divides the updated environment into multiple subregions, reorders the exploring sequence of subregions, and evaluates the benefits of frontier points within the currently accessed subregion. This two-level planning strategy enables the robot to explore regions in a sequence determined by both global and local information. Finally, the goal frontier point selected from the subregion is taken as the next target to guide the robot for further exploration. The whole process is repeated until the environment is fully modeled.

We evaluate the proposed method in both simulation and real environments. The results show that the proposed method has an excellent performance in terms of exploration efficiency and completion. The main contributions of this paper are as follows:

1\) A fast and efficient hybrid frontier sampling method is proposed to extract frontier points, ensuring that the sampling efficiency is not affected by the scale of the whole environment map.

2\) The hierarchical planning strategy is adopted to provide global information for the robot and reduce the complexity of the optimization problem.

3\) Extensive experiments are conducted to verify the theoretical and practical feasibility of the proposed method, and our method shows more advantages compared with other methods in terms of traveling length and exploration time.

# Related Works

Environmental exploration methods are mainly divided into frontier-based and sampling-based methods. With the development of deep learning, there are also methods to use these learning-based technologies to enable autonomous exploration [@deep1; @deep2; @deep3; @deep4; @deep5].

The frontier-based method is first proposed by Yamauchi et al. [@yamauchi1997frontier], by extracting the boundary between known and unknown regions as the frontier, and selecting the frontier closest to the robot as the next exploration target area. This approach can easily promote the exploration task into a local optimal situation, causing the robot to move to the next area before it has explored one, or repeatedly explore the environment. Although there are subsequent works to introduce information gain into the evaluation function [@perkasa2020improved], the above problem cannot be well solved by simply adding an evaluation indicator. Different from conventional methods to obtain frontiers, [@image] uses image processing technology to extract frontiers in the environment map, but with the expansion of exploration scope, processing this map will consume more and more computing resources. To reduce the resource consumption of generating frontiers, [@sensor_reading] uses laser reading to detect the frontiers, which speeds up the generation of frontiers. The approach in [@holz2010evaluating] uses the map segmentation method to divide each indoor room and corridor into subregions to reduce the problem of multiple visits to the environment. Meanwhile, repeated inspection technology is used to improve the efficiency of the robot in the exploration process.

The Next Best View Planner [@nbvp] is a representative approach of the sampling-based method, which uses RRT to expand the entire exploration space, selecting the branches of the tree with the most revenue for the robot to advance. Since the exploration work itself lacks information on the global environment, the robot cannot predict the future environmental space, so the planned path is difficult to be globally optimal. To provide the robot with a global perspective, [@tdle] divides the environmental map into different areas and makes global path planning for these areas to provide global guidance for the exploration system. [@tare] employs a hierarchical framework to simultaneously process online update environment representations and search for continuous traversable paths, significantly enhancing exploration efficiency in large-scale environments. To speed up the sampling process, [@dsvp] utilizes the dynamic expansion of a two-stage planning method, rather than rebuilding the tree, only part of the tree nodes are generated in each iteration process, which greatly improves the computational efficiency.

Some of the above methods use RRT to sample frontier points or viewpoints. However, due to the randomness of the RRT algorithm, the generated nodes may not be uniform. As the tree grows, the generation of new nodes becomes slower, and some small areas and passages are difficult to sample, resulting in incomplete exploration. Several methods [@fuel; @huang2023fael] adopt the incremental detection to extract frontiers, but require maintaining a state voxel map at the underlying level to search frontiers. This consumes computation memory when the scale of the map becomes larger.

In our work, we quickly obtain the frontier points of the surrounding environment, the frontier points are extracted directly from the LiDAR point cloud and the local map, which avoids traversing and maintaining a large-scale voxel map. We also adopt the hierarchical planning strategy to provide comprehensive information for the exploration system, this can make efficient decisions while further reducing the computing consumption.

# Proposed Method

The exploration system consists of four modules: the hybrid frontier point sampling module, the filter module, the subregion segmentation and selection module, and the frontier selection module. The hybrid frontier point sampling module is used to quickly sample potential frontier points from the environment. The filter module removes some invalid frontier points. The subregion segmentation and selection module is proposed to divide the region of the map into several subregions and arrange their access order, then the appropriate subregion is assigned to the next module. According to the assigned subregion, the frontier selection module sorts the candidate frontier points in the subregion using the heuristic evaluation criteria. The point with the highest gain is chosen as the next marching target. The overall framework diagram of the exploration system is shown in Fig. [2](#framework){reference-type="ref" reference="framework"}.

:::: {#frontier_sensor .figure latex-placement="!t"}
![](Long2024HPHS_figs/fig2.png){width="6cm"}

::: caption
Frontier points sampling directly from the LiDAR data. The red dots represent the point cloud. The purple and green dots represent the inserted frontier points when condition 1 or 2 is satisfied respectively. The radius and polar angle of the point in the polar coordinate system are expressed by $r$ and $\theta$.
:::
::::

## Hybrid Frontier Point Sampling Module

Fast extraction of frontier points from the environment is essential to improve exploration efficiency. We adopt a hybrid frontier sampling method. Specifically, we first determine the potential frontier points directly from the LiDAR point cloud, and further screen them to obtain the final available frontier points $\mathcal{F}_{sensor}$. With the movement of the robot in the environment and updating of the LiDAR data, new frontier points will be generated to help expand the boundary. Due to the presence of environmental noise, some frontier points may not be detected. To obtain frontier points stably, we also introduce the image processing-based frontier detector to acquire frontier points $\mathcal{F}_{image}$ within a radius of $d_s$ around the robot. Finally, the frontier points $\mathcal{F}_{all}$ obtained by two frontier detection methods are gathered together.

*1) Sampling frontier points based on LiDAR sensor*

We are inspired by the method in [@gdae] for its several advantages such as fast detection speed and long detection distance. In the frontier point sampling stage, the point cloud of the current frame is converted to the cylindrical coordinate system. Then, the point cloud is selected based on a specific height $z$, and sorted according to the polar angle from $0^{\circ}$-$360^{\circ}$ to construct a collection of point cloud $\mathcal{L}^z=\left\{l_{\theta_0}^z,l_{\theta_1}^z,...,l_{\theta_n}^z\right\}$. For any two consecutive points $l_{\theta_i}^z$, $l_{\theta_{i+1}}^z$ in the collection, a frontier point is inserted between them if satisfy one of the following conditions in the Eq. ([\[condition1\]](#condition1){reference-type="ref" reference="condition1"})-([\[condition2\]](#condition2){reference-type="ref" reference="condition2"}).

$$\begin{equation}
\vert r_{i+1}-r_i \vert \geq r_{gap} \;\;or \label{condition1}
\end{equation}$$

$$\begin{equation}
\theta_{i+1}-\theta_i \geq \theta_{inf} \label{condition2}
\end{equation}$$ where $r$ and $\theta$ represent the radius and polar angle of the point cloud in the polar coordinate system respectively. The condition ([\[condition1\]](#condition1){reference-type="ref" reference="condition1"}) is satisfied when the radius of two consecutive points differs by a certain distance, which means that there may be a corridor passage or slightly larger occlusions between them. Due to these occlusions, the robot is not able to complete the mapping in this area. The condition ([\[condition2\]](#condition2){reference-type="ref" reference="condition2"}) states that there is no scanning point in the region between $\theta_{i}$ and $\theta_{i+1}$, which reveals that the region has not been mapped either. Furthermore, setting a frontier point in this region can help the robot detect and expand the boundary, especially in exploring a large environment.

The presence of frontiers in the map is usually a result of obstructing or exceeding the maximum detection distance of the sensor. Therefore, points that meet these conditions are considered to exist within unexplored areas. Compared with searching the whole map or random sampling to obtain the frontier point, the direct use of LiDAR data can insert the frontier point more accurately and quickly without traversing the whole map, so the calculation speed is not affected by the scale of the map. Fig. [3](#frontier_sensor){reference-type="ref" reference="frontier_sensor"} intuitively represents the above two approaches to sampling frontier points.

*2) Sampling frontier points based on image processing*

Not all frontier points can be found using sensor information only, thus we complement the frontiers with an image processing-based frontier detector [@image]. This detector leverages edge and contour detection methods to process the map data in order to capture the intersection of known and unknown areas. Image-based detection algorithms consume more computing resources with the increase in the image size. Our method aims to reduce the computation burden and improve the time efficiency when extracting frontier points. Thus, we restrict the scale of the local map for detecting frontier points within a radius of $d_s$.

## Filter Module

The filter module accepts all sampled frontier points $\mathcal{F}_{all}$ for filtering to obtain available points. A sampled frontier point will be deleted if it is located near obstacles or other frontier points already exist within its field of view. Besides, this filter also rejects points that belong to the known region. The final filtered frontier points ${\mathcal{F}_{filt}}$ are used for the further exploration.

Additionally, the filter module also deletes frontier points that the robot has visited or unreachable frontier points in real time.

:::: {#subregion .figure latex-placement="htbp"}
![](Long2024HPHS_figs/subregion.png){width="16cm"}

::: caption
Subregion segmentation and selection during the exploration. The green grids represent the remaining subregions after being filtered, and the dark blue grid in each map refers to the subregion that should be visited at the current moment. The other unfilled grids represent subregions that are filtered out, as there are no frontiers in the interior. As the size of the map changes, subregions should grow dynamically.
:::
::::

## Subregion Segmentation and Selection Module

This module processes the whole map region $\mathcal{M}$ according to the pipeline of dividing subregions, filtering, and arranging the access order of subregions. The boundary $\mathcal{B}$ of the current map is first detected to determine the maximal rectangular bounding box $\mathcal{R}$. Then, the entire rectangle $\mathcal{R}$ with the size of $\mathcal{R}_w\times \mathcal{R}_h$ is split into several subregions uniformly in both height and width. Thus, the map is divided into $n$ subregions $\mathcal{SR}=\left\{sr_0,sr_1,...,sr_n\right\},n\leq {n_wn_h}$. The filtered frontier points $\mathcal{F}_{filt}$ are divided into their respective subregion $sr\in\left\{sr_0,sr_1,...,sr_n\right\}$, according to their positions. Those subregions without any frontier point are filtered out. Noting that the map boundary $\mathcal{B}$ is constantly updated as the map area $\mathcal{M}$ expands during the exploration process, the size and center position of each subregion will also dynamically change as the map is extending. Fig. [4](#subregion){reference-type="ref" reference="subregion"} explains the dynamic division of subregions throughout the exploration.

In each of the remaining subregions $\mathcal{SR}^{filt}=\left\{sr_0^{filt},sr_1^{filt},...,sr_m^{filt}\right\},m\leq n$, there exists at least one frontier point. When entering any of these subregions, the new environmental information can be obtained. In order to arrange the sequence of the exploration for the remaining subregions, that is, to find a global path covering the exploration space, we present a revenue function for the global path that simultaneously considers the global coverage and the traveling distance. The optimal subregion arrangement is found by optimizing the sequence combination of subregions by maximizing the revenue function: $$\begin{equation}
    \begin{aligned}
        \mathbf{G}^* &= \max Rev\left(\mathbf{G}\right) \\
                     &=\max e^{-\lambda_2\cdot DTW(\mathbf{G})} \cdot\sum_{i=0}^m e^{-\lambda_1\cdot
\mathbf{D}\left(\mathcal{P}_{rob},\mathcal{P}_i\right)}
    \end{aligned}
    \label{revenue}
\end{equation}$$

$$\begin{equation}
    \begin{aligned}
    & \mathbf{D}\left(\mathcal{P}_{rob},\mathcal{P}_i\right) = \lambda_3 \cdot \mathbf{E}\left(\mathcal{P}_{rob},\mathcal{P}_0\right) + \mathbf{E}\left(\mathcal{P}_{0},\mathcal{P}_1\right) +\cdots \\
    & +\mathbf{E}\left(\mathcal{P}_{i-1},\mathcal{P}_i\right)
    \end{aligned}
    \label{dist}
\end{equation}$$ where $\mathbf{G}=[sr_0^{filt},sr_1^{filt},...,sr_m^{filt}]$ is the access sequence of the remaining subregions, $\mathbf{D}\left(\mathcal{P}_{rob},\mathcal{P}_i\right)$ is the cumulative distance from the robot position $\mathcal{P}_{rob}$ to the subregion center position $\mathcal{P}_i$, and $\lambda$ is the turning factor. The revenue function $Rev(\mathbf{G})$ in Eq. [\[revenue\]](#revenue){reference-type="ref" reference="revenue"} considers the path coverage length when passing through centers of these subregions, and introduces the Dynamic Time Warping (DTW) method [@dtw] to calculate the similarity between the global path $\mathbf{G}$ and the path sequence selected in the last iteration. In Eq. [\[dist\]](#dist){reference-type="ref" reference="dist"}, $\mathbf{E}\left(\mathcal{P}_{i-1},\mathcal{P}_i\right)$ represents the Euclidean distance between centers of two subregions, and the factor $\lambda_3$ is introduced to allow the exploration to start in the subregion that close to the robot. This prevents the robot from starting exploration from a distant region, reducing unnecessary backtracking.

Eq. [\[revenue\]](#revenue){reference-type="ref" reference="revenue"} is proposed to solve a combinatorial optimization problem, which essentially finds an optimal sequence from all possible permutation combinations. Additionally, Eq. [\[revenue\]](#revenue){reference-type="ref" reference="revenue"} ignores the amount of information gain, since all the remaining subregions are worth exploring and only the coverage distance of the global path needs to be considered. After arranging the sequence, the subregion that should be visited currently is selected according to the access sequence.

## Frontier Selection Module

This module receives the assigned subregion and selects the target point $target\in \left\{ \mathcal{F}^{sub}\right\}$ in the assigned subregion using the heuristic function. Then we assign the target point to the planning module to drive the robot to explore. Fig. [5](#gain){reference-type="ref" reference="gain"} illustrates the calculation of the heuristic gain. The frontier selection module selects the best point by considering:

**Traveling gain:** The distance between the robot position $\mathcal{P}_{rob}$ and the frontier point $\mathcal{F}_j^{sub}$ in the assigned subregion reflects the travel cost that the robot needs to pay to reach the frontier point. To reduce the computational cost, we calculate this gain $G^{D}$ using the Euclidean distance: $$\begin{equation}
G^{D}_j=\mathbf{E}\left(\mathcal{P}_{rob},\mathcal{F}_j^{sub}\right)
\end{equation}$$

:::: {#gain .figure latex-placement="!t"}
![](Long2024HPHS_figs/fig5.png){width="6cm"}

::: caption
The illustration of calculating the heuristic gain. The total gain of a frontier point is composed of the traveling gain, the orientation gain, and the information gain. The information gain uses a $k\times k$ information kernel for the comprehensive evaluation.
:::
::::

**Orientation gain:** It is defined as the angle $\theta_{ori}$ between the current motion orientation of the robot and the vector between the robot and the frontier point $\mathcal{F}_j^{sub}$. The point with a small angle is beneficial to maintain the consistency of the robot's motion, avoiding taking a zigzag path or turning back to explore the point behind it. The orientation gain $G^{O}$ is defined as follows: $$\begin{equation}
G^{O}_j=e^{2 \cdot \left(\frac{2 \theta_{o r i}}{\pi}-1\right)}
\end{equation}$$ where larger $\theta_{ori}$ values are more penalized, this can avoid unnecessary routes. It also prevents small values of $\theta_{ori}$ from becoming the decisive factor, since it is reasonable to explore within a range of angles.

**Information gain:** The information gain refers to the revenue calculated from the search space $\mathbb{R}$ around the frontier point. Each grid in the map has three possible states: free $\mathbb{R}_f$, unknown $\mathbb{R}_u$, and occupied $\mathbb{R}_o$, i.e, $\mathbb{R}=\mathbb{R}_f\cup\mathbb{R}_u\cup\mathbb{R}_o$. The unknown state indicates that the area has not been explored, the free state means that the region has been explored and not occupied, and the occupied state represents that there exist obstacles that affect the safety of the robot. The integrated information gain $G^{I}$ for this region is calculated using a $k\times k$ information kernel: $$\begin{equation}
G^{I}_j=e^{\frac{\sum_{w=-\frac{k}{2}}^{\frac{k}{2}} \sum_{h=-\frac{k}{2}}^{\frac{k}{2}} S_{w,h}}{k^2}}
\end{equation}$$ where $s$ is assigned according to the state of the grid in the map and should satisfy: $$\begin{equation}
0\leq s_o\leq s_f\leq s_u
\end{equation}$$

Unlike the conventional information calculation method [@perkasa2020improved], Eq. (5) also imposes penalties on other states, especially areas with obstacles. It is similar to the heuristic used in [@informed]. Our goal is to enable the robot to explore the entire environment as safely as possible.

**Total gain:** For any frontier point $\mathcal{F}_j^{sub}$ in the assigned subregion, the total heuristic gain $Gain$ can be calculated as: $$\begin{equation}
Gain=\tau_3\cdot\Vert G^{I}_j \Vert - \tau_1\cdot\Vert G^{D}_j \Vert - \tau_2\cdot \Vert G^{O}_j \Vert
\end{equation}$$ where $\tau$ denotes the weight factor, and the min-max normalization is used to normalize indicators. The point with the largest score is selected as the next target to explore: $$\begin{equation}
target=\arg\max _{\mathcal{F}^{sub}_j} Gain
\end{equation}$$

## Advantages of Hierarchical Strategy

*Improving decision speed.* A significant amount of computing resources will be consumed if evaluating all these frontier points in the map, resulting in a slow decision speed. By dividing the environment into several subregions, the large-scale exploration challenge can be decomposed into multiple smaller-scale problems, which reduces the complexity of the task.

*Avoiding local minimum trap.* It is difficult to get a globally optimal solution by evaluating the frontier points distributed in different regions only by several evaluation metrics. This leads to unnecessary reentry and repeated exploration. The hierarchical planning strategy enables the robot to make decisions on a larger scale initially than just based on the current local information. Such operation helps prevent the robot from falling into a local minimum while striking a balance between the information acquisition and the exploration efficiency.

*Quickly responding to environmental changes.* Hierarchical planning allows for a more convenient response to environmental changes and enables real-time updates to the exploration strategy. By managing and optimizing the exploration process through the division of regions, the exploration system becomes adaptable to various types and scales of environments.

::: algorithm
$Flag \gets True$\
$BestGain \gets 0$\
:::

# Simulation And Experiment

The proposed method is validated in both simulation and real-world experiments. Fig. [6](#platform){reference-type="ref" reference="platform"} shows our real-world ground platform with an Intel Core i5-11500T@1.5 GHz CPU and 16 GB RAM using Ubuntu 18.04 LTS. The platform is topped with the RoboSense RS-Hellos-16P LiDAR sensor.

:::: {#platform .figure latex-placement="!b"}
![](Long2024HPHS_figs/fig6.jpg){width="5cm"}

::: caption
The real-world ground platform.
:::
::::

## Simulation Experiment

We build four environments for simulation experiments, namely, maze, office, indoor 1, and indoor 2. The four scenarios have different structural arrangements to evaluate the exploration performance of the algorithm in each of them. In particular, two indoor environments are composed of a series of corridors and rooms, and there exist many dead corners that are not easy to explore. The robot is easy to miss some places during the exploration process, resulting in the formation of a backtracking path. All the scenes are built in the Gazebo simulator.

We evaluate the performance of our method by comparing it with three previous methods in these metrics: exploration time, exploration distance, exploration rate (the ratio of explored area to traveling distance), and exploration completion.

- *Efficient Dense Frontier Detection* [@frontier]: A frontier-based method that exploits the submap structure of the SLAM to quickly perform frontier updates and achieve responsive exploration goal planning.

- *TDLE* [@tdle]: An improved method based on RRT-exploration [@rrt_exploration]. It employs the regional division and arrangement to efficiently obtain a global view for exploration.

- *TARE* [@tare]: One of the state-of-the-art exploration methods that uses a hierarchical framework to represent the environment space, which can efficiently deal with large-scale complex environments and achieve faster exploration.

All the tests use the exploration algorithm as the top-level decision-making module, while the planning and obstacle avoidance module as the middle layer uses the open source framework [@cao2022autonomous] of the Robotics Institute from Carnegie Mellon University and obtains the metric data during the exploration process. In each scenario, simulation experiments are conducted 10 times with each method.

:::: {#scenes .figure latex-placement="!t"}
\

::: caption
The four simulation environments.
:::
::::

The best trajectories for each method and their exploration results are depicted in Fig. [8](#result map){reference-type="ref" reference="result map"}. From a purely path-based perspective, our approach exhibits minimal redundant paths and completes the entire exploration process seamlessly without any backtracking. Even in two indoor scenarios, our method sequentially passes through each room along the exploration path, ensuring comprehensive coverage with minimal details missed. On the other hand, the TARE exhibits several instances of backtracking as some rooms in the start and middle of the scene are left unexplored, necessitating a return to complete the exploration, and resulting in missed areas. Both the frontier-based method and the TDLE experience varying degrees of backtracking in all scenarios, leading to decreased exploration efficiency.

:::: {#result map .figure latex-placement="!t"}
\
\
\

::: caption
The result maps of our method and trajectories of all methods in four simulation scenes. The red end of the trajectory represents the start point, and the purple end of the trajectory represents the end point.
:::
::::

::: center
:::

Table 1 shows the specific experimental results and statistics. The results show that our method is able to explore more environmental information while consuming less traveling time and path length. Compared with the TARE, our method reduces the travel path by 7.0% -29.1% and the exploration time by 4.1%-27.2%, and improves the overall efficiency by 10.4%-42.7%. The hybrid frontier sampling method allows for the rapid extraction of potential frontiers from the environment while reducing the computation memory. Thus, the robot can immediately obtain effective frontier information when passing through unknown areas, ensuring timely exploration and planning. This is important because the small unexplored area has a huge impact on the whole exploration process, leading to a significant reduction in its later exploration efficiency.

Fig. [9](#area/time){reference-type="ref" reference="area/time"} visually shows the progress curves of each method during the exploration, and our method finishes the exploration first in all scenarios. Compared with the TDLE and frontier-based method, the exploration efficiency of our method is significantly higher. In two indoor scenes, the TARE makes fast exploration progress in the initial stage. After several experiments, the TARE exhibits a tendency to initially explore along the corridor, significantly accelerating progress in the earlier stages of the exploration. Then it proceeds to explore the smaller rooms, wherein the process of the accumulating exploration progress is relatively slower. In Fig. [9](#area/time){reference-type="ref" reference="area/time"} (c) and (d), the progress curves of the TARE initially grow rapidly, while the growth rate of curves slows down when returning to explore those rooms at the later stage. Our approach arranges the entry sequence of each subregion. The Eq. [\[revenue\]](#revenue){reference-type="ref" reference="revenue"}, encourages the robot to cover the whole exploration space with a short total path to avoid subsequent retrace, without the consideration of the information gain. As can be seen from the trajectories in Fig. [8](#result map){reference-type="ref" reference="result map"} (c) and (d), our method can sequentially pass through each cell and region when exploring. Thus, our exploration progress initially grows at a relatively slow pace, but this approach helps us avoid the issue of unnecessary back-and-forth motion. Therefore, our method ends up traveling with a shorter path than TARE, and in the final stage of curves, it surpasses the TARE and completes the exploration earlier.

:::: {#area/time .figure latex-placement="!t"}
\

::: caption
Comparison of the four methods in the exploration process.
:::
::::

::: center
:::

The average exploration completion (the ratio of the explored area to the total area) of each method is presented in Table 2. Our method achieves a higher degree of exploration completeness compared to the TARE, from 2.2% to 3.0%, while the TARE leaves some areas unexplored. The TDLE can detect the small unexplored corners, but it does not optimize the sampling method of the RRT tree, which leads to the subsequent turning back when some recent frontier points are not detected in time. Since our method also detects frontiers in the local map, it is able to quickly detect some small regions and corners that have not been explored and incorporate them into the planning process for the subsequent exploration.

## Real-World Experiment

The real-world experiment is conducted in two human-made maze scenes and an indoor corridor scene. The maze scenes in Fig. [10](#real word){reference-type="ref" reference="real word"} (a) and (b) are with the size of 10 m × 10 m, and different numbers of obstacles are set inside. Fig. [10](#real word){reference-type="ref" reference="real word"} (c) is the corridor scene, with corridors criss-crossing each other. The Direct LiDAR Odometry [@dlo] is used as the SLAM module, and only relies on the LiDAR sensor for the localization. The maximum speed of the robot is set to 0.6 m/s.

Fig. [10](#real word){reference-type="ref" reference="real word"} also shows the environments explored using the grid map created by Gmapping [@gmapping], where the blue lines are the trajectories of the robot. The trajectories demonstrate the robot's efficient exploration strategy without a redundant path. Even in the corridor with a more complex layout, the robot also visits each area in sequence, achieving an effective exploration in unknown environments.

# Conclusion

We propose an efficient method to explore the unknown environment. Our method adopts the hybrid frontier sampling approach to rapidly extract frontier points by directly using the LiDAR data and the local map information. The hierarchical planning strategy is incorporated to drive the robot to explore the environment according to a path sequence determined by both global and local information. The simulation experiments demonstrate that the proposed method encompasses all regions while exhibiting significant advantages in terms of the traveling distance and the exploration time. The real-world experiments also further prove the effectiveness of our approach in realistic unknown environments.

:::: {#real word .figure latex-placement="!t"}
\

::: caption
The real-world environments and exploration results. The red dot is the starting position and the green dot represents the end position.
:::
::::

[^1]: This work was supported in part by the National Natural Science Foundation of China under Grant 52102449, in part by the China Postdoctoral Science Foundation under Grant 2021M690394, and in part by the Beijing Institute of Technology Research Fund Program for Young Scholars and S&T Program of Hebei under Grant 21567606H.

[^2]: $^{1}$S. Long, Y. Li, B. Xu, and F. Wei are with the School of Mechanical Engineering, Beijing Institute of Technology, Beijing, China. `{sj_long, ying.li, bitxubin, fanweixx}@bit.edu.cn`

[^3]: $^{2}$C. Wu is with RAL, Baidu Research. `wuchenming@baidu.com`

[^4]: $^{1}$Available at `https://github.com/bit-lsj/HPHS.git`
