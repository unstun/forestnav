---
citation_key: Moore2023URA
arxiv_id: 2309.08814
arxiv_url: https://arxiv.org/abs/2309.08814
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-24T16:05:49Z
origin: ai+web
reviewed: false
---

# INTRODUCTION

A key step in navigating ground robots in unmapped, off-road environments is performing traversability estimation. The concept of traversability estimation refers to interpreting the geometry and appearance of the region of interest to determine whether a vehicle could drive through it safely depending on its capabilities [@borges2022] [@sharma2022]. In structured urban environments with clear road markings, local traversability estimation using sensors from a ground vehicle's perspective [@levi2015][@oliveira2016] is usually sufficient for navigation. Whereas in unstructured off-road environments such as dense forests or mountainous regions where the robot's field of view is limited, aerial-to-ground traversability estimation is advantageous to enable path planning from a global perspective [@chavez2018][@kim2019][@hudjakov2009].

Major advances in computer vision and deep neural networks (DNNs) have enabled work in traversability estimation from aerial images in the form of road segmentation [@bandara2021][@quan2021] or terrain segmentation [@hosseinpoor2021]. However, these works only consider the traversability prediction task without addressing the path planning task, which needs to account for errors and uncertainty in the perception model output. Another line of work has proposed ad-hoc modifications to conventional path planners such as Rapidly-exploring Random Trees (RRT) [@lavalle1998] and A\* [@hart1968] by adding terrain and slip penalization terms to make the planner more risk-aware [@ono2015][@candela2022]. However, in these studies, such penalization terms are usually hand-engineered from prior knowledge instead of using a traversability measure that can be directly obtained from sensor data. Thus, research gaps remain in consolidating robotic path planning algorithms with recent advances in learning-based traversability estimation techniques.

This research proposes an uncertainty-aware path planning algorithm using aerial traversability estimation for off-road environments. An ensemble convolutional neural network (CNN) model is first used to perform segmentation of aerial images and output a traversal probability value at the pixel level. Given the noisy traversal probability estimates, an uncertainty-aware path planning algorithm is proposed to predict the best global path for a ground robot to travel from its start location to the goal location. A probabilistic replanning technique that combines information from noisy aerial-to-ground traversability estimates with accurate ground-level traversability measurements is applied so that the ground robot is able to rapidly scan and re-plan suitable paths during physical operation. Code [^2] and datasets [^3] are made publicly-available.

In summary, the key contributions of this work are:

- Development of an uncertainty-aware global path planning algorithm that makes use of noisy aerial-to-ground traversability estimates, with a strong coupling between perception and planning.

- Introduction of a probabilistic replanning technique to enable online updates of the planned path.

- Demonstrated the feasibility of this path-planning approach through experiments with three different image datasets, including a challenging off-road environment.

![Proposed pipeline for uncertainty-aware perception and planning from aerial observations](Moore2023URA_figs/PathPlanningDiagram1.png){#Fig:pipeline_diag}

# LITERATURE REVIEW

Classical path planning algorithms in robotics mostly rely on static maps, which assume that information about which areas are traversable and which areas are not traversable are available in advance in the form of pre-built maps and do not change over time. Classical path planning may be further classified into sampling-based algorithms [@sadat2020perceive] and search-based algorithms [@ajanovic2018search]. Search-based algorithms include the popular Dijkstra's algorithm [@dijkstra1959note], A\* algorithm [@hart1968], and state lattice algorithms [@mcnaughton2011motion]. Variants of search-based path planning include the weighted A\* approach [@pohl1970first], which is faster and uses less memory, but is not optimal. Alternatively, the Anytime Repairing A\* (ARA\*) algorithm [@likhachev2003ara] provides a sub-optimal solution in a short period of time and continues to try to find an optimal solution within a specified time period. More recent approaches have also used deep reinforcement learning [@bhatia2022tuning] or Bayesian optimization [@cano2018] to tune the hyperparameters of the planner. On the other hand, sampling-based approaches such as RRT use random samples drawn from traversable areas of the search space, which allow planning to be carried out in non-convex and high-dimensional spaces [@lavalle1998][@van2021curvature]. Overall, classical path planning algorithms may work well in structured environments but fail to address the problem of unstructured off-road environments with complex terrain and uncertain traversability [@hua2022].

To make an informed decision regarding the desired path during autonomous navigation, it is essential to make use of real-time semantic information derived from sensors that are observing the surrounding environment [@Cui_2021_ICCV]. Recent advances in computer vision [@ranft2016] and the release of big datasets [@liao2022kitti][@cordts2016cityscapes] have facilitated research into path planning methods that can reason directly from sensor inputs [@hu2023planning][@Cui_2022_WACV]. In the domain of ground images, [@Can_2022_CVPR] proposes a neural network for predicting lane geometry and estimating a topology-preserving road network using a forward-looking camera. Similarly, [@yuan2020segfix] uses neural networks to improve the boundary quality for road segmentation. In the domain of aerial images, road semantic segmentation can also be carried out using convolutional neural networks (CNNs) [@quan2021][@yang2022sdunet], or graph neural networks [@Bahl_2022_CVPR][@mei2021coanet] on UAV images or satellite images to provide traversability information to a ground vehicle. Most of these existing works only focus on improving the traversability prediction task without implementing a path-planning solution, which can account for errors and uncertainty in the perception model output.

Another key research gap that we plan to address in this paper is path planning in off-road environments. Urban roads are characterized by features such as curbs, buildings, traffic signs, road markings, and guardrails that can simplify the perception and planning problem[@Volpi_2022_CVPR; @li2022deep], whereas rural roads lack clear boundaries and intersections are complex and heterogeneous [@yadav2018rural; @kearney2020maintaining]. The vast majority of autonomous driving systems have been trained using either urban or suburban datasets (e.g. KITTI [@liao2022kitti] and Cityscapes [@cordts2016cityscapes]) without consideration for rural environments. Some datasets such as Robot Unstructured Ground Driving (RUGD) [@wigness2019rugd], OFF-Road Freespace Detection (ORFD) [@min2022orfd], DeepScene [@valada2016deep], Center for Advanced Vehicular Systems Traversability (CaT) [@sharma2022; @carruth2022challenges], do involve off-road environments but only evaluate perception tasks such as semantic segmentation and free-space detection and not planning tasks. In contrast, this paper will introduce a new aerial image dataset for off-road environments and use it as a benchmark for path planning.

# METHODOLOGY

## Problem definition

Given an aerial image, **I** of a region of interest, a start position, **s**, and goal position, **g**, in image coordinates: compute the *best* path for a ground robot to travel from **s** to **g** using only information in **I**. The *best* path is evaluated based on (i) quality, i.e. how short the total path length is for the computed path, and (ii) feasibility, i.e. how much of the computed path is actually traversable. **I** is assumed to be captured with an image plane parallel to the ground plane so that pixel-wise distances are roughly proportional to real-world physical distances.

## Traversable area segmentation from aerial images

The segmentation step aims to take an aerial observation of a scene, pass it through a semantic information extractor in the form of a DNN, and finally predict the traversability of different regions in the scene at the individual pixel level [@zhang2018road]. The output of the segmentation network for a given aerial image will be the traversal probability distribution matrix for that particular image. For image segmentation, we utilize an ensemble of DNN methods to predict the traversal probabilities. Initially, the neural networks were pre-trained on the classification task using the ImageNet[@deng2009imagenet] dataset containing over 14 million images. Next, we fine-tuned the networks on the semantic segmentation task using specific aerial image datasets to enable the networks to perform traversability estimation from aerial images.

### Network architecture

In this research, we developed an ensemble model utilizing output segmentation heads from U-Net [@ronneberger2015u] and DeepLabV3+ [@chen2018encoder] built on a ResNet-50 [@he2016deep] encoder and pre-trained on ImageNet  [@deng2009imagenet]. Upsampling layers from U-Net and atrous convolution layers from DeepLabV3 are both common strategies in image semantic segmentation to process multi-scale contextual information in image data. The segmentation heads are trained to predict binary traversability (either traversable or not-traversable for each pixel) using the Dice loss function [@sudre2017generalised]. During inference, the output of the final softmax layer is used to extract a traversability map over the entire image. The middle dotted-line block in Figure [1](#Fig:pipeline_diag){reference-type="ref" reference="Fig:pipeline_diag"} shows the proposed network architecture for traversable areas from aerial images.

In our empirical studies, we found that having a high recall rate for traversable terrain is important for successfully generating paths from the start position to the goal position. This is because if the ratio of regions predicted to be traversable compared to the regions predicted to be non-traversable is too low, the path planner may terminate prematurely before finding a traversable connection between the start position and the goal position. Thus, the proposed network architecture uses a max-pooling layer to combine predictions from an ensemble of segmentation heads. The output of the pooling layer has the highest probability of traversability among the input model predictions for each pixel. In our experiments, we found that the pooling function is effective in achieving generally higher recall rates for traversable terrain (refer to Table [\[table:segmentation_results\]](#table:segmentation_results){reference-type="ref" reference="table:segmentation_results"} in the Results section). Theoretically, the outputs of more than two segmentation networks may be pooled together in the ensemble model; however, in our experiments, we found that pooling together two segmentation networks gave adequate performance.

### Aerial image datasets

In this research, we make use of the Massachusetts Road Dataset (MRD) [@MnihThesis] and the DeepGlobe dataset (DGD) [@DeepGlobe18], which are both datasets of satellite images with a mix of urban and off-road environments. MRD contained 1108 training, 49 testing, and 14 validation images, all of 1500 x1500 in resolution and with corresponding ground truth labels. DGD contained 6226 training, 1101 testing, and 1243 validation images, all of 1024 x1024 in resolution but with only the training set having ground truth labels. We resized MRD and DGD images to a standard resolution of 1536 x1536 pixels to maintain consistency. Although these datasets are not directly applicable to the targeted domain of off-road environments, we used them for testing and comparison since these datasets are publicly released and have a large number of annotations readily available. For validation of the approach in the domain of off-road environments, we collected and annotated our own dataset of off-road aerial images obtained from the Center for Advanced Vehicular Systems (CAVS) proving grounds at Mississippi State University [@trail_map] (hereafter referred to as the CAVS dataset). The proving grounds is a 55-acre test facility featuring 12 rugged off-road trails filled with naturally occurring obstacles and terrain features such as rocks, tall grasses, wet lowlands, and wooded or obscured trails. For our CAVS dataset, we manually labeled a total of 403 images and split them into training, test, and validation sets of 332, 38, and 33 images respectively.

In addition, we applied data augmentation to generate sufficiently diverse samples for training. We pre-processed the images with random crop, horizontal flip, vertical flip, and random rotation at 0.75 probability for all the datasets.

### Hyperparameters

The networks were trained for a total of 15 epochs with a batch size of 16. The Adam [@kingma2014adam] optimizer was used due to its faster convergence and fewer hyperparameter requirements. Softmax was used as the activation function for the segmentation prediction layer. These hyperparameter settings follow widely used standard training procedures and have been previously applied on the MRD [@unet_massachuests] and DeepGlobe datasets [@deeplab_deepglobe]. Note that separate models were trained for each dataset.

## Uncertainty-aware path planning

In this subsection, we introduce an Uncertainty-aware A\* (URA\*) approach to generate suitable paths with respect to uncertainty in unknown environments. In traditional A\*-based approaches [@hart1968][@likhachev2003ara][@ren2022], the environment is first discretized into states, and searches over the state-space are carried out based on the edge costs as the optimality criteria. However, this is assuming a perfect environment where the traversability and cost of every state are known in advance. In this research, we take anytime-replanning techniques from ARA\* [@likhachev2003ara] and extend it to uncertain environments by incorporating predictions from a semantic segmentation network to generate robust paths that take into account the traversal probability of each state. We utilize this URA\* algorithm, in conjunction with D\*-lite [@Koenig2002Dlite] to extend to the replanning problem, with an algorithm we call Uncertainty-aware D\*-lite (URD\*) (described in the next subsection).

The traversability matrix obtained from the segmentation network is divided into a grid where each grid cell stores the traversal probability of that region. In this study, we resample the traversability matrix to a grid of 600x600 cells to speed up the computation. The path-planning algorithm will generate a sequence of cells to traverse from the start cell to the goal cell. A denser grid can be used to generate finer paths, at the cost of incurring higher computational time.

::: algorithm
return $g(s) + \epsilon * ( dist(s, goal) - (\alpha * M(s)) )$
:::

::: algorithm
$g(s_{start}) = \infty$; $g(s_{goal}) = 0$\
$OPEN = CLOSED = INCONS = \varnothing$\
Insert $s_{start}$ into $OPEN$ with URA_f_value($s_{start}$)\
ImprovePath()\
:::

Algorithm [\[alg:urafvalue\]](#alg:urafvalue){reference-type="ref" reference="alg:urafvalue"} shows the f-value calculation of URA\*, which determines the priority of which state to expand next. Similar to weighted-A\* and ARA\*, an $\epsilon$ parameter is used to weight the heuristic vs. the g-value. The heuristic value for a state consists of the distance from the current state to the goal state subtracted by the traversal probability times a constant multiplier $\alpha$. This places a higher preference on nodes that have a higher probability of being free space and are also closer to the goal.

Algorithm [\[alg:ura\]](#alg:ura){reference-type="ref" reference="alg:ura"} shows the main loop of URA\*. Similar to ARA\*, this involves running weighted A\* multiple times with $\epsilon$ gradually lowering each time. The $ImprovePath()$ function is borrowed from ARA\* and recomputes the shortest path within a given $\epsilon$ while reusing search efforts from the previous executions. In $ImprovePath()$, the cost of visiting a node is calculated as $1-M(s)$; the higher the predicted traversability probability, the lower the cost of a state.

## Uncertainty-aware path replanning

In this section, we introduce URD\*, a probabilistic replanning technique that combines information from noisy aerial-to-ground traversability estimates with accurate ground-level traversability measurements. This algorithm is applied so that the ground robot is able to rapidly scan and re-plan suitable paths during physical operation. In order to effectively update the environment of the surrounding agent during traversal, we simulate LiDAR scans by using Bresenham's algorithm [@bresenham1965] to simulate the field of view of the robot as it moves through the environment and updates its internal representation of the traversable areas.

::: algorithm
[]{#alg:urd label="alg:urd"}

InitializeEnvironment()\
Initialize Tree with URA\*\
$s_{current} = s_{last} = s_{start}$\
:::

### Tree Initialization

Using Algorithm [\[alg:ura\]](#alg:ura){reference-type="ref" reference="alg:ura"}, the search tree initialization step is performed with URA\*. Since URA\* uses traversability prediction values as pseudo-costs, the initial search process is guaranteed to always find a path from the start state to the goal state.

::: algorithm
[]{#alg:urdheuristic label="alg:urdheuristic"}

$d_{x} = || x_{start}-x_{current} ||$\
$d_{y} = || y_{start}-y_{current} ||$\
$u(s) = dist(s_{start}, s) / dist(s_{start}, s_{goal})$\
$H = u(s) * (\gamma * min(d_x, d_y) + || d_x – d_y ||)$\
return $min(H, dist(s_{start}, s_{current}))$\
:::

### Replanning

In Algorithm [\[alg:urd\]](#alg:urd){reference-type="ref" reference="alg:urd"}, we adopt similar procedures to D\*-lite [@Koenig2002Dlite] to replan paths to the goal, starting from the initial URA\* search tree. Each time the simulated robot moves to a new state, $s_{current}$, the traversability costs of the environment is updated by scanning a fixed radius around the robot and assigning the true traversability (i.e. the ground truth labels in the MRD, DeepGlobe, and CAVS datasets). This is implemented in the function $UpdateEnvironment()$. Then, if the edge costs have changed, the vertices are updated according to the D\*-lite procedure in combination with our new URD\* heuristic.

### Improved Heuristic

In Algorithm [\[alg:urdheuristic\]](#alg:urdheuristic){reference-type="ref" reference="alg:urdheuristic"}, we determine the best node to expand during the replanning process by establishing a custom heuristic. We place higher importance on nodes that have a high traversal probability score as generated from the segmentation model and are closer to the goal. This heuristic is similar to the heuristic presented in [@9327404], and we utilize a similar calculation method with a $u(s)$ value term in the heuristic $H$, where $\gamma$ is the constant multiplier. We place a weight on the first equation to bias the algorithm away from the customized heuristic toward a simpler Euclidean distance heuristic as the number of replans increases as this indicates overestimation.

### Tree Resetting and Heuristic Scaling

In order to prevent the algorithm from being trapped in deadlock situations, we reset the search tree and plan a new path to the goal whenever $s_{current}$ did not update after a few iterations. We also scale the $\gamma$ term after each replan, to resort to the Euclidean distance term in the event that the segmentation model is highly inaccurate.

# RESULTS

## Performance analysis of traversability segmentation

:::: {#Fig:prediction_diag .figure latex-placement="h"}
![](Moore2023URA_figs/PathPlanningDiagram2.png)

::: caption
Traversability segmentation results for aerial images from different datasets. From top to bottom, the rows represent images from the Massachusetts Road Dataset, DeepGlobe dataset, and CAVS dataset. From left to right, the columns represent the (i) original image, (ii) predicted segmentation mask PSM from U-Net (iii) PSM from DeepLabV3+ (iv) PSM from our ensemble model, and (v) ground truth segmentation mask
:::
::::

:::: {#Fig:path_diag .figure latex-placement="h"}
![](Moore2023URA_figs/path_diagram.png)

::: caption
Path planning results for aerial images from different datasets. From top to bottom, the rows represent images from the Massachusetts Road Dataset, DeepGlobe dataset, and CAVS dataset. From left to right, the columns represent the (i) input aerial image, (ii) A\* path (iii) RRT\* path (iv) proposed URA\* path and (v) proposed URD\* replanned path. Red/blue dots indicate start/goal points whereas green lines indicate planned path. A path is not plotted if the algorithm fails to find a path between the start and goal points.
:::
::::

Table [\[table:segmentation_results\]](#table:segmentation_results){reference-type="ref" reference="table:segmentation_results"} shows the segmentation performance analysis of UNet, DeepLabV3+, and our ensemble model on the MRD, DeepGlobe, and CAVS datasets. The traversability predictions were compared pixel-by-pixel to the ground truth annotations. The evaluation metrics used are Dice Loss, standard deviation (SD) of Dice Loss, Intersection-over-Union (IoU), and recall rate, averaged over all images for each dataset. Bold numbers indicate the best-performing model for each metric.

Results show that the proposed ensemble model for traversability segmentation achieved the lowest standard deviation in Dice Loss and the highest IoU for two out of the three datasets. More importantly, the proposed model achieved the highest recall rate for all datasets, demonstrating the benefit of an ensemble approach for maximizing the rate of finding traversable regions from aerial images. Still, the recall rates remain low at 50-60% across the three datasets. In the next section, we will present our results of uncertainty-aware reasoning and path planning to overcome these noisy segmentation results.

## Performance analysis of path planning

To evaluate the performance of URA\* for calculation of the initial path, we opted to compare the algorithm with RRT\* and A\*, which are popular algorithms for path planning. For A\* and RRT\*, a confidence threshold of 50% was used as the cutoff threshold for converting the segmentation network predictions to a binary traversability map. We also considered an alternate version of A\*, which we term as A\*\*, where we lower the confidence threshold from 50% to 30% to give it a better chance of obtaining an initial solution. RRT\* uses a step size of 5, search radius of 50, and 10000 iterations. In the path planning experiments, we manually fix the start and end points for each aerial image.

The results of path planning for generating the initial path are shown in Table [\[table:initial_planning\]](#table:initial_planning){reference-type="ref" reference="table:initial_planning"}. These results are obtained from 49 images in the MRD test set, 29 images in the DeepGlobe validation set (since ground truth labels for the DeepGlobe test set has not been released), and 38 images in the CAVS test set. We use the normalized path length, average path accuracy, and success rate as evaluation metrics. The path length reflects the *quality* of the planned path whereas the path accuracy reflects the *feasibility* of the planned path. The normalized path length is calculated by dividing the computed path length in pixels with the straight line distance from start to goal in pixels. The path accuracy is calculated by comparing the pixels of the computed path with the ground truth traversability labels to determine the percentage of the computed path that lie in traversable regions. That is, the higher the path accuracy, the more likely the initial path is to be feasible for a robot. Finally, the success rate is calculated as the percentage of aerial images for which the path planning algorithm is able to generate an initial path without returning failure. Note that in cases where an algorithm is not successful in producing a complete path from the start to goal (given an input image), we use the maximum cost computed among all algorithms as a nominal value to penalize these failure cases.

Results in Table [\[table:initial_planning\]](#table:initial_planning){reference-type="ref" reference="table:initial_planning"} show that the proposed URA\* algorithm significantly outperforms baseline algorithms on normalized path length, path accuracy and success rate but expands significantly more nodes than A\* to find a feasible solution. By integrating the traversability probabilities into the planning process, URA\* is able to generate higher quality and more feasible paths. In addition, URA\* is always successful in returning a solution. In contrast to A\* or RRT\*, which treats the input map as having binary traversability and may terminate prematurely if there are insufficient areas predicted to be traversable, URA\* is designed to always be able to obtain a path from the start to goal by treating traversability as a continuous value.

The results of path planning for generating replanned paths for online operations are shown in Table [1](#table:replanning){reference-type="ref" reference="table:replanning"}. Rapidly-replanning A\* (RRA\*) [@ganganath2016] and D\*-lite [@Koenig2002Dlite] are used as baseline algorithms. Results show that the proposed URD\* algorithm performs the best in terms of shortest path length and fewest nodes expanded in two out of three datasets considered. For the CAVS dataset, URD\* performs slightly worse compared to RRA\* because the dataset contains scenes with fewer twists and intersections and thus, the advantage of uncertainty-aware replanning was not as significant compared to the MRD and DeepGlobe datasets.

Figure [3](#Fig:path_diag){reference-type="ref" reference="Fig:path_diag"} shows a visual comparison of the paths generated by the proposed algorithm overlaid on the predicted traversability maps. Results show that A\* and RRT\* mostly fail or take suboptimal paths due to the noisy traversability maps whereas URA\* is able to generate reasonable paths and URD\* can improve those paths after replanning.

::: {#table:replanning}
  ----------- ---------- ---------- ---------
    Dataset     Method              
    Length                          
   Expanded                         
      MRD       RRA\*       2.32       346
               D\*-lite     2.01       472
                URD\*     **1.36**   **300**
   DeepGlobe    RRA\*       2.33       505
               D\*-lite     2.16       664
                URD\*     **1.50**   **490**
     CAVS       RRA\*     **1.21**   **161**
               D\*-lite     1.40       359
                URD\*       1.24       262
  ----------- ---------- ---------- ---------

  : Performance comparison of replanned path
:::

# CONCLUSIONS

In conclusion, this research demonstrated an uncertainty-aware path planning algorithm to compute the best path through a region with unknown traversability where only aerial images are available. In future work, we will investigate the possibility of using real-time traversability observations to update the segmentation network model to generate more accurate traversability estimations for replanning purposes. We will also conduct experiments with off-road vehicles to benchmark the effectiveness of this form of aerial-to-ground traversability estimation and planning in real-world conditions.

# ACKNOWLEDGMENT {#acknowledgment .unnumbered}

The work reported herein was supported by by the National Science Foundation (NSF) (Award #IIS-2153101). Any opinions, findings, and conclusions or recommendations expressed in this material are those of the authors and do not necessarily reflect the views of the NSF.

[^1]: $^{1}$ Computer Science and Engineering, Mississippi State University, Mississippi State, MS 39762, USA. Email: cam1271@msstate.edu, sm3843@msstate.edu, pillai@cse.msstate.edu, mnm419@msstate.edu, mittal@cse.msstate.edu, cbethel@cse.msstate.edu, chenjingdao@cse.msstate.edu

[^2]: [github.com/shaswata09/Offroad-Path-Planning/](github.com/shaswata09/Offroad-Path-Planning/){.uri}

[^3]: [kaggle.com/datasets/mitrashaswata/msstate-cavs-off-road-aerial-images](kaggle.com/datasets/mitrashaswata/msstate-cavs-off-road-aerial-images){.uri}
