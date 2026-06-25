---
citation_key: Stache2021Adaptive
arxiv_id: 2108.01884
arxiv_url: https://arxiv.org/abs/2108.01884
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-24T16:38:16Z
origin: ai+web
reviewed: false
---

# Introduction {#sec:intro}

Unmanned aerial vehicles (UAVs) are experiencing a rapid uptake in a variety of aerial monitoring applications, including search and rescue [@Meera19], wildlife conservation [@Manfreda2018], and precision agriculture [@popovic2017icra; @popovic2017iros; @Vivaldini2019]. They offer a flexible and easy to execute a way to monitor areas from a top-down perspective. Recently, the advent of deep learning has unlocked their potential for image-based remote sensing, enabling flexible, low-cost data collection and processing [@Carrio2017]. However, a key challenge is planning paths to efficiently gather the most useful data in large environments, while accounting for the constraints of physical platforms, e.g. on fuel/energy, as well as the on-board sensor properties.

This paper examines the problem of deep learning-based semantic segmentation using UAVs and the exploitation of this information in path planning. Our goal is to adaptively select the next sensing locations above a 2D terrain to maximize the classification accuracy of objects or areas of interest seen in images, e.g. animals on grassland or crops on a field. This enables us to perform targeted high-resolution classification only where necessary and thus maximize the value of data gathered during a mission.

Most data acquisition campaigns rely on coverage-based planning to generate UAV paths at a fixed flight altitude [@Cabreira2019]. Although easily implemented, the main drawback of such methods is that they assume an even distribution of features in the target environment; mapping the entire area at a constant image spatial resolution governed by the altitude. Recent work has explored *informative planning* for terrain mapping, whereby the aim is to maximize an information-theoretic mapping objective subject to platform constraints. However, these studies either consider 2D planning at a fixed altitude or apply simple heuristic predictive sensor models [@popovic2017icra; @popovic2017iros; @Meera19], which limits the applicability of future plans. A key challenge is reliably characterizing how the accuracy of segmented images varies with the altitude and relative scales of the objects in registered images.

:::: {#fig:motivation .figure latex-placement="t"}
![image](Stache2021Adaptive_figs/teaser_adaptive.png){width="48%"} ![image](Stache2021Adaptive_figs/teaser_high.png){width="48%"}

![](Stache2021Adaptive_figs/teaser_sim.jpg){width="95%"}

::: caption
A comparison of our proposed adaptive path planning strategy (top-left) against lawn-mower coverage planning (top-right) for UAV-based field segmentation, evaluated on the application of precision agriculture using real field data (bottom). By allowing the paths to change online, our approach enables selecting high-resolution (low-altitude) imagery in areas with more semantic detail, enabling higher-accuracy, fine-grained segmentation in these regions.
:::
::::

To address this, we propose a new adaptive planning algorithm that directly tackles the altitude dependency of the deep learning semantic segmentation model using UAV-based imagery. First, our approach leverages prior labeled terrain data to empirically determine how classification accuracy varies with altitude; we train a deep neural network with images obtained at different altitudes that we use to initialize our planning strategy. Based on this analysis, we develop a *decision function* using Gaussian Process (GP) regression that is first initialized on a training field and then updated online on a separate testing field during a mission as new images are received. For replanning, the UAV path is chosen according to the decision function and segmented images to obtain higher classification accuracy in more semantically detailed or interesting areas. This allows us to gather more accurate data in targeted areas without relying on a heuristic sensor model for informative planning.

The contributions of this work are: (i) an online planning algorithm for UAVs that uses the semantic content of new images to adaptively map areas of finer detail with higher accuracy. (ii) A variable-altitude accuracy model for deep learning-based semantic segmentation architectures and its integration in our planning algorithm. (iii) The evaluation of our approach against state-of-the-art methods using real-world data from an agricultural field to demonstrate its performance. We note that, while this work targets the application of precision agriculture, our algorithm can be used in any other UAV-based semantic segmentation scenario, e.g., search and rescue [@Meera19], urban scene analysis, wetland assessment, etc.

# Related Work {#sec:related}

There is an emerging body of literature addressing mission planning for UAV-based remote sensing. This section briefly reviews the sub-topics most related to our work.

**UAV-based Semantic Segmentation:** The goal of semantic segmentation is to assign a predetermined class label to each pixel of an image. State-of-the-art approaches are predominantly based on convolutional neural networks (CNNs) and have been successfully applied to aerial datasets in various scenarios [@Sa2018; @Carrio2017; @Nguyen2019; @Lyu2020; @Sa2018b]. In the past few years, technological advancements have enabled efficient segmentation on board small UAVs with limited computing power. Nguyen et al.. [@Nguyen2019] introduced MAVNet, a light-weight network designed for real-time aerial surveillance and inspection. Sa et al.. [@Sa2018] and Deng et al.. [@Deng2020] proposed CNN methods to segment vegetation for smart farming using similar platforms. Our work shares the motivation of these studies; we adopt ERFNet [@romera17] to perform efficient aerial crop/weed classification in agricultural fields. However, rather than flying predetermined paths for monitoring, as in previous studies, we focus on planning: we aim to exploit modern data processing capabilities to localize areas of interest and finer detail (e.g. high vegetation cover) online and steer the robot for adaptive, high-accuracy mapping in these regions.

**Adaptive Path Planning:** Adaptive algorithms for active sensing allow an agent to replan online as measurements are collected during a mission to focus on application-specific interests. Several works have successfully incorporated adaptivity requirements within informative path planning problems. Here, the objective is to minimize uncertainty in target areas as quickly as possible, e.g. for exploration [@stachniss2005rss], underwater surface inspection [@Hollinger2013], target search [@Meera19; @Sadat15; @Singh2009], and environmental sensing [@Singh2009]. These problem setups differ from ours in several ways. First, they consider a probabilistic map to represent the entire environment, using a sensor model to update the map with new uncertain measurements. In contrast, our approach directly exploits the accuracy in semantic segmentation to drive adaptive planning. Second, they consider a predefined, i.e. non-adaptive, sensor model, whereas ours is adapted online according to the behavior of the semantic segmentation model.

Very few works have considered planning based on semantic information. Bartolomei et al.. [@Bartolomei20] introduced a perception-aware planner for UAV pose tracking. Although like us, they exploit semantics to guide next UAV actions, their goal is to triangulate high-quality landmarks whereas we aim to obtain accurate semantic segmentation in dense images. Dang et al.. [@Dang2018] and Meera et al.. [@Meera19] study informative planning for target search using object detection networks. Most similar to our approach is that of Popović et al.. [@Popovic2020AURO], which adaptively plans the 3D path of a UAV for terrain monitoring based on an empirical performance analysis of a SegNet-based architecture at different altitudes [@Sa2018]. A key difference is that our decision function, representing the network accuracy, is not static. Instead, we allow it to change online and thus adapt to new unseen environments.

:::: {#fig:workflow .figure latex-placement="t"}
![](Stache2021Adaptive_figs/overview_small.png){width="99%"}

::: caption
Each time the UAV segments one region of the field, we decide if the UAV should follow its predefined path (right side) or if it should scout the same region with a lower altitude, i.e. obtaining images with high resolution (left side). In the second case, we update the decision strategy by comparing the segmentation results of the same regions at different altitudes.
:::
::::

**Multi-Resolution:** An important trade-off in aerial imaging arises from the fact that spatial resolution degrades with increasing coverage, e.g. Peña et al.. [@Pena2015] show that there are optimal altitudes for monitoring plants based on their size. Relatively limited research has tackled this challenge in the contexts of semantic segmentation and planning. For mapping, Dang et al.. [@Dang2018] employ an interesting method for weighting distance measurements according to their resolution. Sadat et al.. [@Sadat15] propose an adaptive coverage-based strategy that assumes sensor accuracy increases with altitude. Other studies [@Vivaldini2019; @Sa2018b] only consider fixed-altitude mission planning. We follow previous approaches that empirically assess the effects of multi-resolution observations for trained models [@Meera19; @Popovic2020AURO; @Qingqing2020]. Specifically, our contribution is a new decision function that supports online updates for more reliable predictive planning.

# Our Approach {#sec:main}

The goal of this work is to maximize the accuracy in the semantic segmentation of RGB images taken by a camera on-board a UAV with a limited flight time. We propose a data-driven approach that uses information from incoming images to adapt an initial predefined UAV flight path online. The main idea behind our approach is to guide the UAV to take high-resolution images for fine-grained segmentation at lower altitudes (higher resolutions) only where necessary.

As a motivating application, our problem setup considers a UAV monitoring an agricultural field to identify crops and weeds for precision treatment. We first divide the target field into non-overlapping regions and, for each, associate a waypoint in the 3D space above the field from which the camera footprint of the UAV camera covers the entire area. From these waypoints, we then define a lawn-mower coverage path that we use to bootstrap the adaptive strategy. Our strategy consists of two steps. First, at each waypoint along the lawnmower path, we use a deep neural network to assign a semantic label to each pixel in the observed region (soil, crop, and weed in our selected use-case). Second, based on the segmented output, we decide whether the current region requires more detailed re-observation at a higher image resolution, i.e.., lower UAV altitude; otherwise, the UAV continues its pre-determined coverage path.

A key aspect of our approach is a new data-driven decision function that enables the UAV to select a new altitude for higher-resolution images if they are needed. This decision function is updated adaptively during the mission by comparing the segmentation results of the current region at the different altitudes. This enables us to precisely capture the relationship between image resolution (altitude) and segmentation accuracy when planning new paths. Fig. [2](#fig:workflow){reference-type="ref" reference="fig:workflow"} shows an overview of our planning strategy. In the following sub-sections, we describe the CNN for semantic segmentation and the path planning strategy, which consists of offline planning and online path adaptation.

## Semantic Segmentation {#subsec:segmentation}

In this work, we consider the semantic segmentation of RGB images not only as of the final goal but also as a tool to define adaptive paths for re-observing given regions of the field. Each time the UAV reaches a waypoint, we perform a pixel-wise semantic segmentation to assign a label (crop, weed or soil in our case) to each pixel in the current view. We use the ERFNet [@romera17] architecture provided by the Bonnetal framework [@milioto2019ieee] that allows for real-time inference. We train this neural network on RGB images collected at different altitudes to allow it to generalize across possible altitudes without the need for retraining. If the same region is observed by the camera from different altitudes, we preserve the results obtained with the highest resolution, assuming that higher-resolution images yield greater segmentation accuracy.

## Path Planning: Basic Strategy {#subsec:planning}

The initial flight path is calculated based on the standard lawn-mower strategy [@Galceran2013]. Such a path enables covering the region of interest efficiently without any prior knowledge. We aim to adapt this path according to the non-uniform distribution of features in the field to improve semantic segmentation performance.

For a desired region of interest, we define a lawn-mower path based on a series of waypoints. A waypoint is defined as a position ${\mbox{\boldmath$w$}_i}$ in the 3D UAV workspace where: (i) the UAV camera footprint does not overlap the footprints of any other waypoint; (ii) the UAV performs the semantic segmentation of its current field of view; (iii) the UAV decides to revise its path or to execute the path as previously determined; and (iv) we impose zero velocity and zero acceleration.

The initial flight path is calculated in form of fixed waypoints at the highest altitude ${\mbox{\boldmath$W$}}^{h_\text{max}} = \{ {\mbox{\boldmath$w$}_0}, {\mbox{\boldmath$w$}_1},\ldots, {\mbox{\boldmath$w$}_n} \}$. If necessary, we modify this coarse plan by inserting further waypoints based on the new imagery as it arrives. At each waypoint ${\mbox{\boldmath$w$}_i}$, UAV decides either to follow the pre-determined path, i.e.. moving to ${\mbox{\boldmath$w$}_{i+1}}$, or to inspect the current region more closely at a lower altitude. In the second case, we define a second series of waypoints, ${\mbox{\boldmath$W$}}^{h^\prime} = \{ {\mbox{\boldmath$w$}_0}, {\mbox{\boldmath$w$}_1}, \ldots, {\mbox{\boldmath$w$}_n} \}$, at the desired altitude, $h^\prime$, that will be inserted before ${\mbox{\boldmath$w$}_{i+1}} \in {\mbox{\boldmath$W$}}^{h_\text{max}}$ so that the resulting path, at the desired altitude, is a lawn-mower strategy covering the camera footprint from ${\mbox{\boldmath$w$}_{i}} \in {\mbox{\boldmath$W$}}^{h_\text{max}}$.

## Planning Strategy: Offline Initialization {#subsec:init}

We develop a decision function that takes a given waypoint as input and outputs the next waypoint, either ${\mbox{\boldmath$w$}_{i+1}} \in {\mbox{\boldmath$W$}}^{h_\text{max}}$ or ${\mbox{\boldmath$w$}_{0}} \in {\mbox{\boldmath$W$}}^{h^\prime}$, given the segmentation result. In the case of an altitude change, our decision function outputs also the value of the desired altitude $h^\prime$. To do this, we start by defining a vegetation ratio providing the number of pixels classified as vegetation (crop and weed) as a fraction of the total number of pixels in the image:

$$\begin{equation}
\label{eq:vr} 
v = \frac{\sum_{c \in \{ \text{crop, weed} \} } p_c }{p_{\text{tot}}},
\end{equation}$$ where $p_{tot}$ is the total number of pixel and $p_c$ is the total number of pixels classified as $c$. This vegetation ratio gives us a way to infer how valuable it is to spend time on the current region of the field. It captures the intuition that higher values of this ratio indicate more possible misclassifications between the crop and weed classes. To quantify such a relationship, we let the UAV run on a separate field, where we have access to ground truth data, segmenting regions of the fields with different altitudes. Segmenting the same region of the field with different altitudes provides two pieces of information that we use to shape the decision function. On one hand, we have the difference between the altitudes from which we segment the field, $\Delta h = h_\text{max} - h^\prime$. On the other hand, we have the the difference between the vegetation ratio in the predicted segmentation, $\Delta v = v_{h_\text{max}} - v_{h^\prime}$. At the same time, we can compare the vegetation ratio to the accuracy of the predicted segmentation by computing the mean intersection over union (mIoU). Where the mIoU is defined as the average over the classes $C=\{ \text{crop, weed, soil} \}$ of the ratio between the intersection of ground truth and predicted segmentation and the union of the same quantities:

:::: {#fig:dataset_split .figure latex-placement="t"}
![](Stache2021Adaptive_figs/dataset.png){width="99%"}

::: caption
We use three different fields from the WeedMap dataset [@Sa2018b] to train a CNN for semantic segmentation and one field to initialize the planning strategy. The remaining field is used for evaluation. For an extensive evaluation of our approach, we swap the roles of the fields so that we test our algorithm on each field once.
:::
::::

$$\begin{equation}
\label{eq:iou}
\text{mIoU} = \frac{1}{|C|} \sum_{c \in C}  \frac{\text{gt}_\text{c} \cap \text{prediction}_\text{c}}{\text{gt}_\text{c} \cup \text{prediction}_\text{c}}.
\end{equation}$$ Again, we define the difference between mIoUs at different altitudes as, $\Delta \text{mIoU} = \text{mIoU}_{h_\text{max}} - \text{mIoU}_{h^\prime}$ .

Our method thus considers two sets of observations, representing the relationships between the vegetation ratio and UAV altitude ($\mathcal{O}$) and between vegetation ratio and mIoU ($\mathcal{I}$) as follows:

::: multicols
2 $$\begin{equation*}
\label{eq:veg2h}
  \mathcal{O} = \begin{bmatrix}
   \Delta v_0 & \Delta h_0\\ 
   \Delta v_1 & \Delta h_1\\ 
   \multicolumn{2}{c}{\vdots}\\
   \Delta v_n & \Delta h_n\\ 
  \end{bmatrix},
\end{equation*}$$

$$\begin{equation*}
\label{eq:veg2h}
  \mathcal{I} = \begin{bmatrix}
   \Delta v_0 & \Delta \text{mIoU}_0\\ 
   \Delta v_1 & \Delta \text{mIoU}_1\\ 
   \multicolumn{2}{c}{\vdots}\\
   \Delta v_n & \Delta \text{mIoU}_n\\ 
  \end{bmatrix}.
\end{equation*}$$
:::

While both sets are initialized offline, we only update $\mathcal{O}$ online given that $\mathcal{I}$ requires access to ground truth that is clearly not available on testing fields. We fit both sets of observations using GP regression [@Rasmussen2006]. A GP for a function $f(x)$ is defined by a mean function $m(x)$ and a covariance function $k(x_i,\,x_j)$:

$$\begin{equation}
\label{eq:prior}
f(x) \thicksim GP(m(x),k(x_i,x_j)).
\end{equation}$$

A common choice is to set the mean function $m(x) = 0$ and to use the squared exponential covariance function: $$\begin{eqnarray}
\label{eq:sqexp}
  k(x_i,x_j) &=& \varsigma_{f}^2 \mathrm{exp}\left(-\frac{1}{2}\frac{|x_i-x_j|^2}{\ell^2}\right) +\varsigma_{n}^2,
\end{eqnarray}$$ where $\mathbf{\theta} =\{\ell,\,\varsigma_{f}^2,\,\varsigma_{n}^2\}$ are the model hyperparameters and represent respectively the length scale $\ell$, the variance of the output $\varsigma_{f}^2$ and of the noise $\varsigma_{n}^2$. Typically, the hyperparameters are learned from the training data by maximizing the log marginal likelihood. Given a set of observations $y$ of $f$ for the inputs ${\mbox{\boldmath$X$}}$ (i.e.. our sets $\mathcal{O}$, $\mathcal{I}$), GP regression allows for learning a predictive model of $f$ at the query inputs ${\mbox{\boldmath$X$}}_{*}$ by assuming a joint Gaussian distribution over the samples. The predictions at ${\mbox{\boldmath$X$}}_{*}$ are represented by the predictive mean $\mu_{*}$ and variance $\sigma_{*}^2$ defined as:

$$\begin{eqnarray}
  \begin{aligned}
    \mu_{*} =&~{\mbox{\boldmath$K$}}({\mbox{\boldmath$X$}}_{*},{\mbox{\boldmath$X$}})\,{\mbox{\boldmath$K$}}_{\mathrm{XX}}^{-1}\,y, \\
    \sigma_{*}^2 =&~{\mbox{\boldmath$K$}}({\mbox{\boldmath$X$}}_{*},{\mbox{\boldmath$X$}}_{*})\,-{\mbox{\boldmath$K$}}({\mbox{\boldmath$X$}}_{*},{\mbox{\boldmath$X$}})\,{{\mbox{\boldmath$K$}}_{\mathrm{XX}}}^{-1}\,{\mbox{\boldmath$K$}}({\mbox{\boldmath$X$}},{\mbox{\boldmath$X$}}_{*}),
  \end{aligned}
  \label{eq:gp}
\end{eqnarray}$$

where ${\mbox{\boldmath$K$}}_{\mathrm{XX}} = {\mbox{\boldmath$K$}}({\mbox{\boldmath$X$}},{\mbox{\boldmath$X$}})+\varsigma_{n}^2\,{\mbox{\boldmath$I$}}$, and ${\mbox{\boldmath$K$}}(\cdot,\,\cdot)$ are matrices constructed using the covariance function $k(\cdot,\cdot)$ evaluated at the training and test inputs, ${\mbox{\boldmath$X$}}$ and ${\mbox{\boldmath$X$}}_{*}$. In the following, we will use the ground sampling distance (GSD) to identify the image resolution (thus the UAV altitude) from which the UAV performs the semantic segmentation. The GSD is defined as: $\text{GSD} = \frac{h \* S_w}{f \* I_w }$, where $h$ is the UAV altitude, $S_w$ the sensor width of the camera in mm, $f$ the focal length of the camera in mm and $I_w$ the image width in pixels.

## Planning Strategy: Online Adaptation {#subsec:online}

To adapt the UAV behavior online to fit the differences between the testing and training fields, we update the GP defined by the set $\mathcal{O}$ in the following way. In the testing field, each time the UAV decides to change altitude to a lower one, we compute a new pair $\Delta v' , \Delta h'$ and re-compute the GP output as defined in Eq. ([\[eq:prior\]](#eq:prior){reference-type="ref" reference="eq:prior"}).

:::: {#fig:results .figure latex-placement="t"}
![](Stache2021Adaptive_figs/iouvstime.png){width="90%"}

::: caption
The averaged results for the testing fields from the WeedMap dataset. The blue square lies to the left of all performances with a linear decision function, indicating some performance improvement.
:::
::::

:::: {#fig:waypoints .figure latex-placement="t"}
![image](Stache2021Adaptive_figs/traj_high_low.png){width="30%"} ![image](Stache2021Adaptive_figs/traj_linear.png){width="30%"} ![image](Stache2021Adaptive_figs/traj_adaptive.png){width="30%"}

::: caption
Visual comparison of trajectories traveled by the UAV over a field using different planning strategies. The coverage paths (left) are restricted to fixed heights and cannot map targeted areas of interest. The linear decision function (middle) enables adaptive planning, but it is continuous with respect to altitude and leads to sudden jumps. Our adaptive approach overcomes this issue, leaving the path less often and more purposefully at selected heights for more efficient mapping. The black spheres indicate measurement points.
:::
::::

# Experimental Results {#sec:experimental}

We validate our proposed algorithm for online adaptive path planning on the application of UAV-based crop/weed semantic segmentation. The goal of our experiments is to demonstrate the benefits of using our adaptive strategy to maximize segmentation accuracy in missions while keeping a low execution time. Specifically, we show results to support two key claims: our online adaptive algorithm can (i) map high-interest regions with higher accuracy and (ii) improve segmentation accuracy while keeping a low execution time with respect to the baselines described in Sec. [4.2](#subsec:baselines){reference-type="ref" reference="subsec:baselines"}.

## Dataset

To evaluate our approach, we use the WeedMap dataset [@Sa2018b]. It consists of 8 different fields collected with two different having different channels, it also provides pixel-wise semantic segmentation labels for each of the 8 fields. In this study, we focus only on the 5 fields having RGB information. We split the 5 fields into training and testing sets (Fig. [3](#fig:dataset_split){reference-type="ref" reference="fig:dataset_split"}). One of the training fields is used to initialize the decision function that shapes altitude selection in the adaptive strategy, as described in Sec. [3.4](#subsec:online){reference-type="ref" reference="subsec:online"}. For each experiment in the following sub-sections, we test our approach and the baselines, see Sec. [4.2](#subsec:baselines){reference-type="ref" reference="subsec:baselines"}, on each field once, and then report the average among each run.

## Baselines {#subsec:baselines}

To evaluate our proposed approach, we compare it against two main baselines. The first one is the standard lawn-mower strategy where a UAV covers the entire field at the same altitude, for this strategy we use consider five different altitudes resulting in GSD $\in \{ 1.0, 1.5, 2.0, 2.5, 3.0 \} \frac{\text{cm}}{\text{px}}$. The lawnmower strategy with a fixed GSD of $3.0 \frac{\text{cm}}{\text{px}}$ corresponds to the initial plan for our strategy described in Sec. [3.2](#subsec:planning){reference-type="ref" reference="subsec:planning"}. The second baseline is defined by *only* initializing the UAV behavior as described in Sec. [3.3](#subsec:init){reference-type="ref" reference="subsec:init"} and without adapting the strategy online using the decision function as new segmentations arrive. We refer to this strategy as "Non Adaptive". This benchmark allows us to study the benefit of adaptivity obtained by using our proposed approach ("Adaptive").

## Metrics {#subsec:metrics}

Our evaluation consists of two main criteria: segmentation accuracy and mission execution time. For execution time, we compute the total time taken by the UAV to survey the whole field, including the time needed to move between waypoints, segment a new image, and plan the next path. To assess the quality of the semantic segmentation we use the mIoU metric defined in Eq. ([\[eq:iou\]](#eq:iou){reference-type="ref" reference="eq:iou"}).

## Field Segmentation Accuracy vs Execution Time {#sec:semseg_acc}

The first experiment is designed to show that our proposed strategy obtains higher accuracy while keeping low execution time. We show such results in Fig. [4](#fig:results){reference-type="ref" reference="fig:results"}. For each strategy, we compute the mIoU (over the entire field) and the execution time needed by the UAV to complete its path. The adaptive strategy crosses the line defined by the lawnmower strategies at different altitudes, meaning that it can achieve better segmentation accuracy while keeping a lower execution time. The non-adaptive strategy instead lies under the curve, failing to overtake the lawn-mower strategy. We plot exemplary paths results from the different strategies in Fig. [5](#fig:waypoints){reference-type="ref" reference="fig:waypoints"}; on the left, we show the lawn-mower strategy with altitudes corresponding to GSDs of $1.0\frac{\text{cm}}{\text{px}}$ and $3.0\frac{\text{cm}}{\text{px}}$, while the middle and right plots show the paths resulting from non-adaptive and adaptive strategy, respectively.

## Per-Image Segmentation Accuracy vs Altitude {#sec:semseg_acc}

The second experiment shows the ability of our approach to achieve targeted semantic segmentation when compared to the non-adaptive strategy. At this stage, we compute mIoU for each image that contributes to the final segmentation of the whole field. This will give us a way to evaluate the efficiency of our adaptation strategy. We then visualize the mean and standard deviation. As can be seen in Fig. [6](#fig:acc_vs_gsd){reference-type="ref" reference="fig:acc_vs_gsd"}, our adaptive strategy provides higher per-image accuracies when the UAV is scouting the field at low altitudes. This entails that, with our strategy, the UAV invests time resources in a more proficuous manner. We show a qualitative comparison of the per-image semantic masks in Fig. [7](#fig:results2){reference-type="ref" reference="fig:results2"}.

:::: {#fig:acc_vs_gsd .figure latex-placement="t"}
![](Stache2021Adaptive_figs/miouvsh.png){width="90%"}

::: caption
Mean and standard deviation of the per-image statistics for semantic segmentation. Our adaptive strategy leads to better performance when scouting the field at low altitudes.
:::
::::

# Conclusion {#sec:conclusion}

In this paper, we presented a new approach for efficient multi-resolution mapping using UAVs for semantic segmentation. We exploit prior knowledge and the new incoming segmentations in a way, that we get a decision function with a shape that produces a flight path, leading to a performance gain in terms of segmentation accuracy while keeping comparatively short execution time. The resulting map is mapped with different resolutions, depending on the information content of a corresponding area. We believe that our approach opens a direction for efficient UAV mapping purposes, especially in precision agriculture. Further investigations on less homogeneous field structures are to be carried out to refine the approach.

:::: {#fig:results2 .figure latex-placement="t"}
![](Stache2021Adaptive_figs/qualitative.png){width="90%"}

::: caption
Qualitative field segmentation results using the non-adaptive strategy (left) and the proposed adaptive strategy using our decision function (right) for path planning. The circled details demonstrate that our adaptive planning approach enables targeted high-resolution segmentation to better capture finer plant details.
:::
::::

[^1]: $^*$: authors with equal contribution.

[^2]: All authors are with the University of Bonn, Germany.

[^3]: This work has been funded by the Deutsche Forschungsgemeinschaft (DFG, German Research Foundation) under Germany's Excellence Strategy, EXC-2070 -- 390732324 (PhenoRob).
