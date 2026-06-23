---
citation_key: Philippe2024CollisionAware
arxiv_id: 2410.03370
arxiv_url: https://arxiv.org/abs/2410.03370
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-23T19:17:11Z
origin: ai+web
reviewed: false
---

# Introduction

The application of robotics in agriculture has experienced a significant increase in recent years, driven by advancements in autonomous systems and the pressing need to address challenges in the sector. As noted by @fountas_agricultural_2020, Unmanned Ground Vehicles (UGV) are being developed to mitigate the labor shortages in agriculture, while simultaneously reducing the physical demands of agricultural work. @lenain_agricultural_2021 have demonstrated the value of these robots for weeding tasks, replacing polluting chemical weedkillers with more environmentally-friendly mechanical methods.

However, the identification of traversable elements, i.e., those which do not present a lethal threat to navigation, is a challenging task. The main constraints in agricultural environments are the shape evolution that occur over the seasons and the presence of dense vegetation. Tall grass and branches may protrude in untrimmed areas, as illustrated in [1](#fig:UGV){reference-type="ref+label" reference="fig:UGV"}. This results in a considerable number of false detections by the perception systems, thus decreasing the UGV navigation performance and ultimately reducing the efficiency and resilience of the autonomous platform.

![Autonomous plateform navigating through an agricultural field. Tall grass, as well as crops, protrude into the path, forming potential obstacles the robot has to collide with. As such, any system working in such conditions must be able to assess the severity of each collision.](Philippe2024CollisionAware_figs/KIPP_Champ.jpg){#fig:UGV width="\\columnwidth"}

The necessity for a high level of safety in field deployment is paramount, both for the crops themselves and for pedestrians. A fundamental aspect of ensuring safe and resilient navigation is the development of a comprehensive understanding of the surrounding environment. It is imperative that UGVs are aware of any potential danger or lack of sufficient understanding of the surrounding unstructured environment. Furthermore, UGVs should not halt abruptly at every blade of grass seen by the sensors. As such, one must achieve a compromise between security and autonomy.

To address these constraints, it is crucial to identify elements with which the UGV can interact safely. Range measurements are crucial for understanding the environment's geometry. Additionally, while traditional color cameras can identify scene elements, emerging sensors such as multi-spectral cameras provide higher spectral resolution and more detailed scene information, especially in vegetal environments. The development of vegetation indices for detecting and monitoring plant health [@abderrazak_review_1996] offers valuable new data to improve traversability analysis.

In this paper, we propose a physics-based traversability analysis, able to determine whether an element can be traversed or must be avoided by a UGV in an agricultural environment. We propose a novel method that integrates depth and spectral modalities to create a mass density-augmented map by considering the semantic nature of objects within the UGV's path, aided by precise, non-data-driven vegetation detection. This map is then used to evaluate potential paths in terms of the resulting loss of velocity. The contributions presented in this article are

1.  the definition of a new traversability criterion and its physical interpretation for unstructured vegetal environments using emerging sensors; and

2.  a quantitative evaluation of vegetation segmentation methods.

# Related work {#sec:related_work}

The concept of traversability analysis has been extensively reviewed in the academic literature. @benrabah_review_2024 define the objectives of traversability analysis as determining whether a UGV can successfully navigate a path, or doing so while optimizing factors such as travel time or energy consumption. To achieve this goal, the surroundings are modeled during the environmental perception task. This model is used to assess navigation risks and provide crucial information for optimal and safe path planning. @beycimen_comprehensive_2023 classify traversability methods into three categories: vision-based, geometry-based, or hybrid, depending on the exteroceptive modality employed. The majority of methods rely on visual data. Furthermore, @borges_survey_2022 highlight the necessity for UGVs to have access to 6 Degrees of Freedom (DoF) pose information and large datasets to train data-driven solutions.

In a structured environment, @laghmara_25d_2019 proposed to generate a 2.5D map by fusing data from both a LiDAR and a camera. Through the application of belief theory, it not only represents the static surroundings but also identifies dynamic objects. In contrast, unstructured environments present greater challenges. @castro_how_2023 proposed fusing height and color data with the UGV velocity to generate an environmental cost grid for offroad application. This enables more nuanced and diverse navigation behaviors compared to traditional baselines, as vehicle velocity is integrated into the decision-making process. While most map-based approaches describe the environment with navigation costs or physical modeling (e.g., occupancy probability, slope, or ground roughness), @cai_risk-aware_2022 introduced a novel criterion based on UGV physics. To evaluate traversability, the environment is modeled in terms of the appropriate speeds for UGVs to navigate specific cells, employing an AI-driven solution. Both methods from @castro_how_2023 and @cai_risk-aware_2022 require a setup phase to train the AI model for risk estimation in navigating the environment. However, assessing the risk of traversing impassable areas---such as mud, which poses a sinking hazard, or crops that must be avoided---remains challenging without a highly realistic simulator. The proposed method does not need to be trained in-situ. Moreover, the success of data-driven segmentation methods strongly depends on the quality, quantity, and diversity of training data [@liu_computing_2021], making this approach unsuitable for security and environmental protection applications. To address AI's safety limitations, this paper proposes the use of a model-based semantic segmentation approach.

In unstructured environments, relying on a single criterion may be insufficient. @leininger_gaussian_2024 proposed a mapless method for traversability analysis. Geometric features (slope, step height, flatness) are extracted from a Gaussian Process before to be fused in a local traversability map. @fan_step_2021 also proposed a multi-criteria traversability approach. Factors such as slope, ground roughness, and steps are evaluated to create a multi-layered, risk-aware cost grid. The effectiveness of their approach has been demonstrated through field trials conducted in magma tubes and an abandoned metro line. However, one may wonder whether the criteria previously described are able to discern passable elements. In the proposed method, the impact of collisions is evaluated using semantic information.

Dense vegetation, common in agricultural environments during spring and summer, can obstruct traversability analysis by blocking visual features and introducing unnecessary geometric information. Detecting vegetation would enable the integration of its crossability into the analysis. While most UGVs rely on grayscale or color cameras, these sensors are limited by the narrow visible light spectrum and poor spectral resolution (up to 3 channels). Multispectral cameras enhance vision by providing higher spectral resolution and capturing data beyond the visible spectrum, thereby addressing this limitation. The use of spectral distances, as discussed by @richards_image_2006 for satellite image classification, has been widely studied, with applications in detecting crops, concrete, and water. These methods assess how closely spectral measurements align with a reference profile. Additionally, green vegetation absorbs red light while reflecting near-infrared (NIR) radiation [@gitelson_relationships_2003]. As noted by @abderrazak_review_1996, vegetation indices are employed to monitor these spectral bands, providing insights into plant health. Based on this assumption about the environment, the proposed traversability method incorporates vegetation detection using spectral images. In the work of @santos_segmentation_2021, vegetation indices were utilized for vegetation detection, specifically comparing indices based on visible light for segmentation tasks. The Modified Green Red Vegetation Index (MGRVI) demonstrated the best performance in segmenting green plants. Furthermore, Otsu and K-Means binarization algorithms were evaluated, with K-Means delivering superior results in most scenarios. Vegetation segmentation using data-driven methods has also been explored. @sa_weednet_2018 introduced WeedNet, a segmentation model that employs a CNN with visible and NIR inputs. The network classifies `weeds`, `crops`, and `background`, with applications in weed control. For navigation tasks, @kulic_deep_2017 developed a segmentation network to detect trails in unstructured environments using a multispectral camera to enhance navigation.

Few studies have been conducted on the application of spectral measurements for proximity detection. @zou_multi-spectrum_2017 proposed fusing vegetation indices with LiDAR depth data for obstacle detection. Superpixel generation on the Normalized Difference Vegetation Index (ndvi) image facilitates the detection of non-plant elements. A Support Vector Machine (SVM) classifier is then applied to categorize obstacles based on various geometric and visual features. However, this method is measurement-based. In a map-based approach, false detections could be filtered out by leveraging prior knowledge, due to most of the environment being static over time. To build an environmental model, @clamens_real-time_2021 combined multispectral and LiDAR measurements into a 3D map of the environment, augmented with the ndvi. These 3D maps are subsequently used to monitor the health of plantations, as well as for fruit detection and counting operations using data-driven methods. In the proposed method, a similar map is generated to conduct traversability analysis based on the semantic segmentation of vegetation within the environment. Plant detection is employed to estimate the crossability of map elements. [3](#sec:proposed_method){reference-type="ref+label" reference="sec:proposed_method"} introduces a traversability index that accounts for the semantic characteristics of scene elements to estimate their traversability. This method addresses the issue of false detections caused by dense vegetation in agricultural environments.

# Map-based Traversability Estimation {#sec:proposed_method}

![Traversability analysis flow: Multispectral images are fused with LiDAR data to produce an augmented point cloud, which serves as the basis for semantic segmentation. Mass density is calculated for each depth measurement, updating the 3D environmental map. This is then converted into a 2D traversability grid. Ultimately, potential paths are assessed, and the safest one is chosen.](Philippe2024CollisionAware_figs/traversability_analysis_flow.png){#fig:tta_flow width="\\textwidth"}

The objective of the proposed method is to estimate a path navigation cost by computing the potential loss of velocity that would be experienced by the UGV traversing it. [2](#fig:tta_flow){reference-type="ref+label" reference="fig:tta_flow"} illustrates the traversability analysis pipeline. Initially, the spectral measurements obtained from the camera are projected into the point cloud of the LiDAR. A semantic segmentation of the environment is conducted using spectral measurements. A mass density is estimated for each LiDAR point in the camera's field of view, on the basis of the probabilities of belonging to a given semantic class. The augmented point cloud is then filtered and stored within a 3D map, before being projected onto a 2D grid in order to estimate the traversability of the terrain. The loss of velocity for a given trajectory is estimated. Local paths leading to a larger velocity loss are rejected, and thus a safe trajectory is selected.

## Augmentation

The first step is to process the raw sensor data to derive a spectrally-enhanced depth measurement. After performing the necessary calibrations, the LiDAR data is projected onto the camera measurements. We refer to the outcome of this procedure as the *spectrally augmented point cloud*. In order to fuse spectral and spatial information on a 3D map, three calibrations are required:

#### Intrinsic calibration

estimates the distortion coefficients of the optics, the focal lengths and the optical center coordinates forming intrinsic matrix $\bm{K} \in \mathbb{R}^{3 \times 4}$ of each camera.

#### Extrinsic calibration

identifies the relative pose between each sensor and provides a transformation matrix defined by $\bm{T} \in SE(3)$.

#### Spectral calibration

@sattar_snapshot_2022 proposed a calibration procedure to establish a connection between reflectance, i.e., the physical material properties that determine how light is reflected, and the light intensity sensed by the camera. This step leads to *multispectral image* illustrated in [2](#fig:tta_flow){reference-type="ref+label" reference="fig:tta_flow"}. The conversion is achieved through the use of a linear system model. The spectral reflectance vector, denoted as $\bm{r} \in \mathbb{R}^{m}$, is estimated based on the corresponding spectral intensity vector $\bm{i} \in \mathbb{R}^{n}$, using the spectral calibration matrix $\bm{M}\in \mathbb{R}^{m\times n}$, for each pixel of the camera image. The reflectance vector is defined as $$\begin{equation}
   \bm{r} = \bm{M}\bm{i}.
   \label{equ:reflectance_estimation_function}
\end{equation}$$

From this, the lidar point cloud is projected on the image frame using $$\begin{equation}
    \bm{p}_\text{image} = \bm{K}\bm{T}\bm{p}_\text{lidar},
  \label{equ:spectral_projection}
\end{equation}$$ where $\bm{p}_\text{lidar} \in \mathbb{R}^{4}$ and $\bm{p}_\text{image} \in \mathbb{R}^{3}$ denotes the depth data measured by the LiDAR in their respective frames. As such, the LiDAR point cloud is augmented with spectral information from the camera, that will be used in the following to estimate a mass density map. This process is illustrated in [2](#fig:tta_flow){reference-type="ref+label" reference="fig:tta_flow"}, where it is denoted as *Augmentation*. The semantics are assessed using the spectrally augmented point cloud. This step is presented in [2](#fig:tta_flow){reference-type="ref+label" reference="fig:tta_flow"} as *Semantic segmentation*. It is both described and evaluated in the [4.2](#sec:semantic_seg){reference-type="ref+label" reference="sec:semantic_seg"}.

## Mass density map generation {#subsec:mass}

The aim of this section is to estimate the mass density of the environment. Therefore, we define the *mass density augmented point cloud* as a set of vectors of the form $[x,y,z,d_m]^T$, where $d_m\in\mathbb{R}_{\geq 0}$ denotes the associated mass density. This step is denoted as *Mass density computation* in [2](#fig:tta_flow){reference-type="ref+label" reference="fig:tta_flow"}. For this, we propose a data-driven approach: each of the $n$ semantic classes, $c_i$, is associated with a reference mass density $d_m(c_i)$. Furthermore, to address the inherent uncertainties, the mass density is modeled as a random variable. The mass density is computed as the expected value alongside the possible obstacles classes probabilities $p(c_i)$, as $$\begin{equation}
\begin{aligned}
    \mathbb{E}[d_m] &= \sum_{i=1}^{n}d_m(c_i) \cdot p(c_i | s) \\
                    % &=  \frac{\sum d_m(c_i)p(\bm{y}|c_i)p(c_i)}{p(\bm{y})} \\
                    &=\frac{\sum_i d_m(c_i)p(s|c_i)}{\sum_i p(s|c_i)}, 
\end{aligned}
   \label{equ:density_estimation_function}
\end{equation}$$ where $s$ is the semantic measurement, and $p(c_i | s)$ are the confidence on the measurements. Such values can be either input in the framework, or learned from an annotated dataset.

Once the 4D point cloud is processed, it is transformed into a 3D map to be used for traversability analysis. The 3D map is generated by aggregating the 4D measurements into a voxel grid, converting them into the world frame. The sensor poses is determined using the SLAM LiDAR solution from @koide_portable_2019. Next, the 3D map is converted into a 2D grid to assess navigation costs. This process is depicted in [2](#fig:tta_flow){reference-type="ref+label" reference="fig:tta_flow"} as *Map to grid*. This is done by flattening the map, where ground points are filtered using the RANSAC algorithm [@fischler_random_1981], along with points above the UGV's height. The mass density grid is initialized with the UGV mass value and is later filled with the maximum mass density value from the corresponding Z-axis column. As such, a 2D grid map with mass density information is generated, that is used in the next section to estimate the loss of velocity a robot would undergo given a path in the environment.

## Velocity loss evaluation

Using the mass density grid, we derive a physics-based formulation for traversability, relying on the loss of velocity due to navigation in nonempty space. This step is designated as *Navigation costs estimation* in [2](#fig:tta_flow){reference-type="ref+label" reference="fig:tta_flow"}. Assuming inelastic collisions, the final velocity $v_R^f$ of the UGV is computed as $$\begin{equation}
   v_R^f = \frac{m_R}{m_R+m_i} v_R \Leftrightarrow v_R^f = \alpha v_R,
   \label{equ:inelastic_collision}
\end{equation}$$ where $v_R$ is the initial velocity of the UGV, $m_R$ the mass of the robot, and $m_i$ the mass of the $i$th obstacle.

From this, we model the environment as a collection of infinitesimal particles of area $\Delta a\to 0$. Given a path $\mathcal{P}\subset\mathbb{R}^2$ crossing a total area $A$, the velocity coefficient $\alpha$ of the robot is given by $$\begin{equation}
   \alpha = \prod_{i=1}^N \frac{m_R}{m_R+d_m(i)\Delta a},
   \label{equ:velocity_lost_coeff}
\end{equation}$$ assuming colliding with $N$ particles of size $\Delta a$ such that $N\Delta a=A$. Note that free space is modeled as a particle of null mass density. From this, with the particle area $\Delta a$ tending towards zero, the equation becomes $$\begin{equation}
\begin{aligned}
   \alpha &= \lim\limits_{\Delta a \to 0} \prod_{i=1}^{A/\Delta a} \frac{m_R}{m_R+d_m(i)\Delta a} \\
          &= \exp{\left(- \frac{1}{m_R}\int_\mathcal{P} d_m(a)  da\right)},
   \end{aligned}
   \label{equ:velocity_lost_coeff_2}
\end{equation}$$ where $d_m(a)$ denoted the local mass density at the given position in the environment. As such, for infinitesimal particles, [\[equ:velocity_lost_coeff_3\]](#equ:velocity_lost_coeff_3){reference-type="ref+label" reference="equ:velocity_lost_coeff_3"} compute the ratio of lost velocity is undergoing the path $\mathcal{P}$. In the case of a grid map in which the mass density is constant inside each cell, the equation can be simplified to $$\begin{equation}
\begin{aligned}
   \alpha &= \exp{\left(- \frac{1}{m_R}\sum_{c_i\in\mathcal{P}} d_m(i) a_c\right)},
   \end{aligned}
   \label{equ:velocity_lost_coeff_3}
\end{equation}$$ where $a_c$ is the area of a grid cell. One can note that assuming infinitesimal collisions result in a lower bound on the loss of velocity, meaning that we will always overestimate the risk for one path.

To summarize, the environment is modeled through the multimodal fusion of LiDAR and cameras, as described in [\[equ:spectral_projection\]](#equ:spectral_projection){reference-type="ref+label" reference="equ:spectral_projection"}. As the UGV navigates, the grid is continuously updated to represent the mass density of surrounding elements using [\[equ:density_estimation_function\]](#equ:density_estimation_function){reference-type="ref+label" reference="equ:density_estimation_function"}. This grid is subsequently used to evaluate routes candidates using [\[equ:velocity_lost_coeff_3\]](#equ:velocity_lost_coeff_3){reference-type="ref+label" reference="equ:velocity_lost_coeff_3"}, allowing the selection of the safest path. This method enables the environment to be physically characterized by the expected loss of velocity by crossing a specific region. As such, the ratio of velocity $\alpha$ will be used as the navigation cost. In the following section, we will qualitatively assess this approach and quantitatively evaluate a non-data-driven vegetation semantic segmentation solution.

# Evaluations {#sec:evaluations}

In this section, we outline the setup employed for evaluating the proposed method. Next, we assess the performance of the semantic segmentation indices, followed by an offline test of our traversability analysis solution using recorded data.

## Experimental Setup

A teleoperated platform was equipped with a Hesai Pandar XT-32 LiDAR, a Silios CMS-V VNIR multispectral camera, and an Intel Realsense D415 stereoscopic camera. The VNIR camera provided 8 spectral measurements from 550 nm to 830 nm, in addition to a panchromatic (PAN) measurement. The stereoscopic camera provided 3 channels of RGB measurements. Data are collected using this mobile measurement bench, enabling us to evaluate our traversability analysis solution offline. As illustrated in [3](#fig:3d_map){reference-type="ref+label" reference="fig:3d_map"}, one of the environments explored was a park with tall grass, untrimmed trees and winding paths. Buildings and static pedestrians are present throughout the navigation. The weather was mild during the recordings.

## Semantic segmentation performance {#sec:semantic_seg}

In [3.2](#subsec:mass){reference-type="ref+label" reference="subsec:mass"}, we presented a generic way to estimate the mass density of the environment using semantic classes. As such, the quality of this estimate rely heavily on the level of accuracy on the segmentation. The following section presents a thorough quantitative evaluation of vegetation indices and spectral distance performances, highlighting their performance to differentiate vegetation from other objects. The evaluation is conducted using a manually annotated 3D dataset, where spectral information was fused with a 3d point cloud. Each point on the map is labeled with one of the following classes: `Grass, Track, Vegetation, Building, Pedestrian, Obstacle` or `Other`. An example of the annotation and spectral measurements is depicted in [3](#fig:3d_map){reference-type="ref+label" reference="fig:3d_map"}. In total, 6228592 points were annotated for a total covered area of 2515 m^2^, consisting of off-road environments.

![Augmented 3D maps of a park environment, consisting of tall grass, bushes, trees and a small shack. Top Left: Color camera's image from the scene; Top Right: ndvi colorized 3D map; Bottom Left: visible light colorized 3D map; Bottom Right: Manually annotated 3D map](Philippe2024CollisionAware_figs/feature_maps.png){#fig:3d_map width="\\columnwidth"}

The present study focuses on the vegetation detection: a macro-class designated `Plants` is defined, encompassing both the `Vegetation` and `Grass` classes, while all other classes are included under the $\neg \texttt{Plants}$ macro-class.

In the following, we evaluate the most popular metrics to detect and quantify the vegetation. Namely, the Modified Green-Red Vegetation Index (mgrv), Green Leaf Index (gli), Modified Photochemical Reflectance Index (mpr), Red-Green-Blue Vegetation Index (rgbvi), Excess of Green (exg), Excess of Red (exr), Vegetative (veg), Normalized Difference Vegetation Index (ndvi), and Enhanced Vegetation Index (evi) [@abderrazak_review_1996], are evaluated. Additionally, the spectral distances, such as Euclidean Distance (ed), Bray-Curtis Distance (bc), and Spectral Angle (sa) [@richards_image_2006; @kruse_spectral_1993] are also compared. The reference reflectance profiles used for the computation of spectral distances were extracted from the annotated spectral maps for each class by averaging the spectral measurements. These profiles consist of 29 wavelengths, ranging from 550 nm to 830 nm, and are presented in [4](#fig:ref_plot){reference-type="ref+label" reference="fig:ref_plot"}.

![Reflectance profiles of several elements of agricultural environment](Philippe2024CollisionAware_figs/reflectance_profile.png){#fig:ref_plot width="\\columnwidth"}

The segmentation procedure is described as follows: the vegetation index and spectral distance are applied to the spectral augmented maps. Subsequently, a binarization step is conducted using the Otsu algorithm [@otsu_threshold_1979] to segment vegetation with a dynamic threshold. The *Intersection over Union (IoU), Precision (Prec.), Accuracy (Acc.), Recall (Rec.), F1 score, Specificity (Spec.)* and *computation duration* $\Delta t$ are compared for each vegetation segmentation method in [1](#tab:vegetation_segmentation_performance){reference-type="ref+label" reference="tab:vegetation_segmentation_performance"}. An AMD Ryzen 7 5000 series CPU is used for the computational duration measures.

::: {#tab:vegetation_segmentation_performance}
   Index  IoU        Prec.      Rec.       Acc.       F1         Spec.       $\Delta t$ \[ms\]
  ------- ---------- ---------- ---------- ---------- ---------- ---------- -------------------
   mgrv   0.54       0.94       0.56       0.62       0.70       0.84              169.5
    gli   0.42       0.97       0.43       0.53       0.59       0.94              107.5
   mpri   0.49       0.94       0.51       0.58       0.66       0.88            **60.3**
   rgbvi  0.68       0.87       0.76       0.71       0.81       0.53              148.3
    exg   0.56       0.98       0.57       0.64       0.72       0.94              82.9
    exr   0.33       0.78       0.37       0.41       0.50       0.57              64.1
   exgr   0.64       0.89       0.70       0.69       0.78       0.63              138.8
    veg   0.80       0.84       **0.94**   0.81       0.89       0.27              194.8
    evi   0.56       0.99       0.56       0.64       0.72       **0.98**          104.0
   ndvi   **0.91**   **0.99**   0.92       **0.93**   **0.95**   0.94              67.8
    sa    0.69       0.79       0.84       0.69       0.81       0.05              883.7
    bc    0.66       0.95       0.69       0.72       0.80       0.85             1589.4
    ed    0.90       0.96       0.93       0.91       **0.95**   0.84              430.1

  : Benchmarking of model-based vegetation indices for vegetation segmentation.
:::

As such, the most reliable method for identifying vegetation in proximate detection applications is the ndvi. However, its response is dependent on the wavelength of only two specific frequencies, since the ndvi is computed as $$\begin{equation}
   \text{ndvi} = \frac{i_{810}-i_{650}}{i_{810}+i_{650}},
   \label{equ:ndvi}
\end{equation}$$ where the intensity of light at a specific wavelength $\lambda$ nm is denoted as $i_\lambda$. False positives are likely in the case of certain elements with similar reflectance in the red and NIR bands (e.g., plastics and textiles). Pedestrians represent a small portion of the dataset, so false detections related to their clothing have a negligible effect on the overall performance results presented. Spectral distance, such as the spectral angle, measures the consistency of a measurement with respect to a reference profile over a much higher resolution. At the expense of processing time, this allows for greater robustness to local similarities in the analyzed light spectrum. As such, when deadline with more complex environments where there is a thinner granularity than only differentiating between vegetation and non-vegetation, these metrics would prove themselves more robust. Such metrics will be investigated in future works.

Given the results in [1](#tab:vegetation_segmentation_performance){reference-type="ref+label" reference="tab:vegetation_segmentation_performance"}, the normalized ndvi index is used to generate belonging probabilities of `Plants` class in [\[equ:density_estimation_function\]](#equ:density_estimation_function){reference-type="ref+label" reference="equ:density_estimation_function"}.

## Navigation costs estimation analysis

In this section, we present an application of our method. For simplicity, we focus on only two classes that are `Plants` and $\neg \texttt{Plants}$, where future works will focus on using more classes for safe navigation. It is imperative that the $\neg \texttt{Plants}$ class is not navigable; therefore, the concrete mass density is set for this class [@noauthor_nf_2014]. In contrast, the `Plants` class permits navigation. The respective mass densities $d_m(\texttt{Plants})$ and $d_m(\neg \texttt{Plants})$ are set to 20 kg m^−2^ and 2400 kg m^−2^. The UGV mass is set to 250 kg. The cost grid is next extracted from the mass density-augmented map, as described in [3](#sec:proposed_method){reference-type="ref+label" reference="sec:proposed_method"}.

[5](#fig:path_costs){reference-type="ref+label" reference="fig:path_costs"} illustrates an example of navigation. In this scenario, a path-following solution presents the UGV with a series of potential local paths, each of which offers a different route to reach the desired objective. These routes are then evaluated using the navigation cost function, which is applied to the mass density grid. The environment is characterized by the presence of high grass, dense vegetation (e.g., bushes, trees) and buildings, as illustrated on the semantic grid. The UGV's local planner generates seven candidate paths (color pixels) over the cost grid (gray pixels).

The path p1 guides the vehicle through a grove of trees, with a navigation cost of ($\alpha_1=0.4$). This results in a significant reduction in speed due to the collision with the substantial vegetation. Path p7 directs the UGV to an uncharted region. The navigation cost is ($\alpha_7=0.7$) due to the grid initialization and the unknown nature of the objects it contains. Ultimately, path p4 traverses exclusively through regions with null density mass. As shown in the label grid, the path is comprised solely of grass, which is a component of the ground. The navigation cost of p4 is ($\alpha_4=0.9$), indicating that the UGV will experience a minor loss of speed when navigating this route. The local planner selected this path over the other candidates. In this context, a non-semantic-aware method, as described in @leininger_gaussian_2024, would treat vegetation as an impassable step for the vehicle.

This method is based on semantic understanding of the environment. It can be employed in diverse environments settings and extended with different semantic classes. Furthermore, it can be adapted to any UGV's size, from a lawnmower to a tractor, by setting the appropriate mass value $m_R$. Finally, the loss velocity coefficient $\alpha$ used to evaluate a candidate path can be derived to estimate more complex metrics, such as the loss of kinetic energy over a path.

The grid-based approach for mass density estimation is inherently highly parallelizable and the ndvi requires relatively low computation. This potentially makes the solution suitable for real-time applications.

![Local planning candidates evaluated based on the mass density grid. Semantic grid (top) and satellite view (middle) illustrate the environmental configuration during the run (middle). The local paths over the cost grid (bottom) illustrate navigation costs of each candidate. A coefficient of $1$ means no loss of velocity, thus a safe path, whereas a coefficient of $0$ means a collision resulting in the total stop of the robot.](Philippe2024CollisionAware_figs/nav_path_cost_estimation.png){#fig:path_costs width="\\columnwidth"}

# Conclusion {#seq:conclusion}

In this paper, we presented a novel traversability analysis method specifically designed for Unmanned Ground Vehicle (UGV) navigation in agricultural environments. The proposed approach constructs a representation of the environment that incorporates both impassable obstacles and crossable elements within the scene.

A quantitative evaluation of algorithms for vegetation segmentation was conducted, demonstrating that the use of the Normalized Difference Vegetation Index (ndvi) yields the most effective results in terms of detection accuracy and computational efficiency.

We provided an example of the use of our framework for traversability analysis, showing that the robot is able to differentiate between dangerous and safe collisions. The approach can be adapted to various UGV models, allowing for flexibility in how obstacles are defined based on specific vehicle requirements.

For future work, a quantitative evaluation of the collision-aware navigation method will be conducted, linking the proposed solution to robot control. Additional semantic classes could be explored for density map estimation, utilizing either the spectral angle distance, or a data-driven approach with appropriate safeguards. Furthermore, integrating the mass index into a multi-layer grid would be advantageous, as it would enable the inclusion of additional features to enhance the traversability estimation. These features could include ground slope, height map, and other relevant characteristics.

# Acknowledgment {#acknowledgment .unnumbered}

We gratefully acknowledge the financial support from the *Association Nationale de la Recherche et de la Technologie* (ANRT) and *Technology & Strategy Engineering SAS*, as well as the contribution of *GdR IASIS* towards interlaboratory mobility, which was essential for conducting this research.

[^1]: $^{1}$ Université de Haute-Alsace, IRIMAS, EA 7499, 68093, Mulhouse, France

[^2]: $^{2}$ Université Clermont Auvergne, INRAE, UR TSCF, 63000, Clermont-Ferrand, France

[^3]: $^{3}$ Technology & Strategy Engineering SAS, 67300, Schiltigheim, France
