---
citation_key: Viswanath2024OffRoad
arxiv_id: 2401.01439
arxiv_url: https://arxiv.org/abs/2401.01439
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-23T18:56:31Z
origin: ai+web
reviewed: false
---

# Introduction

Off-road autonomous driving has recently received much attention with multimodal datasets, improved semantic segmentation frameworks and robust planners. Multiple sensors are employed to perceive and navigate unstructured terrain. The Light Detection and Ranging (LiDAR) sensor provides 3D information that helps to extract geometric data about a scene, while a camera captures visual data. However, cameras can lose information at different lighting conditions, which can affect navigation algorithms. To solve this problem, we used the backscattered LiDAR intensity value, which is not affected by lighting conditions, to classify objects in an off-road environment.

Traditional LiDAR Semantic Segmentation models [@10.1007/978-3-030-64559-5_16] [@9010002] have focused primarily on leveraging the geometric properties of objects, which has proven effective for urban scenes characterized by well-defined boundaries. However, off-road scenes present unique challenges, as they contain diverse objects/classes with varying colors, textures, and undefined boundaries. In such scenarios, the aforementioned models may not perform optimally.

The use of LiDAR intensity as an auxiliary input in conjunction with geometry information has been previously explored for segmentation purposes [@salsanet2020]. However, the values of the LiDAR intensity are influenced by factors such as range, angle of incidence, and surface reflectivity. In this paper, we explore the use of surface reflectivity information for efficiently segmenting different classes for off-road scenes by calibrating intensity values for range and angle of incidence.

:::: {#fig:puddle .figure latex-placement="!ht"}
![](Viswanath2024OffRoad_figs/intens_puddle.png){width="\\textwidth" height="4 cm"}

::: caption
Segmentation Results on RELLIS-3D dataset.
:::
::::

# LiDAR Intensity Calibration

The intensity value in a LiDAR denotes the returned backscattered signal ebergy. Intensity is dependent on multiple factors such as range ($R$), reflectivity of the object ($\rho$), angle of incidence ($\alpha$), surface roughness, atmospheric humidity, etc.[@weitkamp_lidar_2006]. Among these factors, the surface's reflectivity is predominantly tied to the object's properties, making it our focal parameter. To ensure a reliable LiDAR intensity-based classification, it is crucial to calibrate the intensity values for the dependencies on the range and angle of incidence.

## Range Dependence

LiDAR sensor's principle works on the difference between the emitted and received laser power, given by: $$\begin{equation}
    \centering
    P_r = \frac{P_e\rho Cos(\alpha)}{R^2}
    \label{lq}
\end{equation}$$ where $P_e$ is the emitted laser power, $\rho$ is reflectance of an object. Eq. ([\[lq\]](#lq){reference-type="ref" reference="lq"}) represents an ideal model in which the intensity is inversely proportional to the square of the range.

:::: {.figure latex-placement="t"}
::: caption
\(a\) Raw Intensity vs Range of Grass (b) Intensity calibrated for $\alpha$ vs Range.
:::
::::

However, in reality, the range-intensity relationship at proximate distances is non ideal. In a shorter range, the Range-Intensity exhibits an exponential relationship, Eq. ([\[ir\]](#ir){reference-type="ref" reference="ir"}) until reaching a certain threshold [@Biavati:11] as given by: $$\begin{equation}
    \centering
    I(R,\alpha,\rho) \propto P_r(R,\alpha,\rho) = \eta(R)\frac{I_e\rho Cos(\alpha)}{R^2}
    \label{ir}
\end{equation}$$ Fig. [\[r_int\]](#r_int){reference-type="ref" reference="r_int"} shows the range vs. intensity scatter plot for grass, including the incidence angle. Due to the near-range effect[@rs14174393], our analysis focuses on points within the range of 6 to 60 m.

### Intensity Correction for Large Range

To correct the LiDAR intensities that depend solely on an object's reflectance, we follow Eq.[\[pred_eq\]](#pred_eq){reference-type="ref" reference="pred_eq"} and focus on LiDAR points outside of the near-range effect ($R>6 \text{ meter}$, where $\eta(R) = 1$). $$\begin{equation}
    I(\rho) = \frac{I(R,\alpha,\rho)  R^2}{Cos(\alpha)}
    \label{pred_eq}
\end{equation}$$ The above computation provides the emitted intensity (originating from the object) adjusted for both range and angle of incidence. Correction for the range is made through Eq ([\[eq:range_cor\]](#eq:range_cor){reference-type="ref" reference="eq:range_cor"}): $$\begin{equation}
    \centering
    I_e = I(R,\rho)  R^2\qquad\{R > 6 m\}
    \label{eq:range_cor}
\end{equation}$$

## Angle of Incidence Dependence

The intensity is intrinsically linked to angle of incidence ($\alpha$). Fig.[\[fig:alphavsI\]](#fig:alphavsI){reference-type="ref" reference="fig:alphavsI"} and Fig. [\[fig:avic\]](#fig:avic){reference-type="ref" reference="fig:avic"} elucidate the relationship between the angle of incidence ($\alpha$) and the Intensity ($I$). The graphs show that the highest intensity is observed when $\alpha$ is close to 0, and the lowest when it is close to $\pi/2$, which is in agreement with the relationship expressed in Eq. ([\[ir\]](#ir){reference-type="ref" reference="ir"}).

Based on Eq. ([\[pred_eq\]](#pred_eq){reference-type="ref" reference="pred_eq"}), the effect of the incidence angle $\alpha$ can be eliminated by dividing the intensity $I(R,\alpha,\rho)$ by $\cos(\alpha)$, resulting in $I(R,\rho)$, which depends only on the range and reflectance of the surface. The corrected intensity versus range plot is illustrated in Fig. [\[c_int\]](#c_int){reference-type="ref" reference="c_int"}.

:::: {#fig:alpha_surf .figure latex-placement="t"}
![](Viswanath2024OffRoad_figs/Angleofincidence.png){width="80%" height="3 cm"}

::: caption
Interaction of laser beam with surface at different angle of incidence
:::
::::

:::: {.figure latex-placement="!ht"}
::: caption
\(a\) Raw Intensity vs $\alpha$ of Grass at different ranges (b) Raw intensity vs $\alpha$ for different classes at 10 meters range. The segregation of intensity values for different classes is observed.
:::
::::

The angle $\alpha$ is determined by the vector of the incident laser beam$(\overrightarrow{l})$ and the normal of the surface $(\overrightarrow{n})$ as shown in Fig. [2](#fig:alpha_surf){reference-type="ref" reference="fig:alpha_surf"}. It can be calculated as $\alpha = arccos(\overrightarrow{l} \cdot \overrightarrow{n})$. Traditionally, the surface normal can be determined by Ball query sampling [@6287634], which takes into account points in the vicinity within a certain radius to calculate the normal vector by fitting a plane with Principal Component Analysis (PCA) [@doi:10.1080/14786440109462720]. However, the angle of incidence calculated with the estimated normal has an MSE error of 0.44 (38 degrees), which is inaccurate. Therefore, to accurately estimate the angle of incidence, we fit the surface normal-point vector data to the ground truth angle of incidence using Fully Connected Layers(FCN).

For FCN, we need the ground truth that is determined in the following way. The ground truth $\alpha$ is obtained by segregating the point cloud data according to annotated classes and then associating them with their corresponding range information, as shown for the \"grass\" class in Figure [\[r_int\]](#r_int){reference-type="ref" reference="r_int"}. Since $\alpha$ has a $cosine$ relationship with intensity, the maximum intensity in every range in Figure [\[r_int\]](#r_int){reference-type="ref" reference="r_int"} will have ($\cos \alpha$) = 1. This allows us to calculate $\alpha$ for a given LiDAR point class using the following equation: $$\begin{equation}
\alpha = arccos(\frac{Intensity(R)}{MaxIntensity(R)} \label{gt_alpha}).
\end{equation}$$ The generated ground truth $\alpha$ along with their corresponding surface normal point vector is used to train the FCN. The FCN takes the surface normal point vector (6 element array) as input and predicts $\alpha'$. The mean absolute error (MAE) between $\alpha$ and $\alpha'$ is calculated and the loss is backpropagated for the FCN to learn.

# Experiments and Results

The proposed approach to using surface reflectivity for segmentation is evaluated in the Rellis-3D off-road data set[@9561251]. Rellis-3D is a multimodal dataset consisting of 4 sequences of annotated LiDAR point cloud from off-road environments. The dataset consists of 20 classes that include grasses, bushes, puddles, trees, etc., providing heterogeneity. The point cloud data are collected using Ouster OS1 with 64 channels. For initial experimentation, we only consider the major classes such as grass, bushes, trees, puddle, and person for semantic labeling.

:::: {#fig:int_ranges .figure latex-placement="t"}
![](Viswanath2024OffRoad_figs/distri.png){width="80%" height="4 cm"}

::: caption
Calibrated Intensity ranges of different classes.
:::
::::

Ouster OS1 intensity data is purely raw, i.e; the values are not pre-calibrated but are scaled to 64-bit integers. The calibrated intensity ranges for different classes were generated from the 0000 sequence of Ouster data. $\alpha$ for each LiDAR point is extracted using Eq.([\[gt_alpha\]](#gt_alpha){reference-type="ref" reference="gt_alpha"}). With the $\alpha$ values and range known, we calibrate the raw LiDAR intensity using Eq.([\[pred_eq\]](#pred_eq){reference-type="ref" reference="pred_eq"}). The calibrated intensity values are segregated based on the annotated labels and we find that the intensity values are distributed in specific ranges for different classes, as shown in Figure [3](#fig:int_ranges){reference-type="ref" reference="fig:int_ranges"}. This proves our hypothesis of reflectivity-based class segregation.

To predict a LiDAR point cloud, the intensity values are calibrated using the Eq. ([\[pred_eq\]](#pred_eq){reference-type="ref" reference="pred_eq"}) where $\alpha$ is predicted using the FCN. A neighborhood prediction policy is employed, whereby calibrated intensity values are assigned classes based on their proximity to the closest class mode values. The predictions were performed on sequences 0001 and 0002 of the RELLIS-3D dataset, with classes limited to grass, bush, trees, person, and puddle. The framework gave an average mIoU of $47\%$, and the respective class IoU is given in Table [1](#tab:results){reference-type="ref" reference="tab:results"}.

::: {#tab:results}
     Framework       Tree        Grass      Puddle      Bushes      Person       mean
  --------------- ----------- ----------- ----------- ----------- ----------- -----------
       Ours          74.68     **66.44**   **47.83**     13.65       33.52       47.17
   SalsaNext$^*$   **79.04**     64.74       23.20     **72.90**   **83.17**   **64.61**
    KPConv$^*$       49.25       56.41        0.0        58.45       81.20       49.06

  : mIoU of experiment results. SalsaNext[@10.1007/978-3-030-64559-5_16] and KPConv[@9010002] are benchmarks of RELLIS-3D dataset.
:::

## Pre-Processing Velodyne Intensity data.

The Velodyne LiDARs generate point cloud data comprising three-dimensional coordinate points and a preprocessed intensity dataset, which differs from the raw intensity data produced by Ouster LiDARs. The Velodyne Intensity data are adjusted to an 8-bit integer scale and are calibrated with respect to range and laser power, as detailed in the data sheet. Figure [4](#fig:raw_osvs){reference-type="ref" reference="fig:raw_osvs"} illustrates a comparison between the intensity data from Velodyne and Ouster LiDARs across various classes. As depicted in the figure, the Velodyne intensity data do not align with the LiDAR equation [\[ir\]](#ir){reference-type="ref" reference="ir"}. In this context, we introduce a method for converting the Velodyne intensity data back to the raw intensity format used by Ouster, essentially reversing the inherent intensity processing employed by Velodyne.

:::: {#fig:raw_osvs .figure latex-placement="!ht"}
![](Viswanath2024OffRoad_figs/raw_osvs.png){width="80%"}

::: caption
Raw intensity plots from Ouster and Velodyne LiDAR for grass(green) and tree(brown).
:::
::::

The RELLIS-3D dataset contains LiDAR scans that are annotated, and these scans are obtained using the 32-channel Velodyne Ultra Puck for the same scenes as those scanned by Ouster LiDARs. In Figure [5](#fig:max_osvs){reference-type="ref" reference="fig:max_osvs"}, we illustrate the extraction of the most intense values that correspond to specific ranges for each class, and this is done using 1000 scans from both Velodyne and Ouster. It is worth noting that Velodyne LiDARs, as per the datasheet, lack calibration for the angle of incidence, denoted by \[$\alpha$\]. This lack of calibration means that the maximum intensity value remains independent of the angle of incidence, which is an important point to consider.

![Maximum intensity vs range for classes Grass, Tree and Person from Ouster and Velodyne LiDAR scans.](Viswanath2024OffRoad_figs/max_osvs.png){#fig:max_osvs width="\\textwidth" height="4 cm"}

In Figure [6](#fig:q){reference-type="ref" reference="fig:q"}, we can see the division of the maximum intensity values of Ouster by the maximum intensity values of Velodyne, resulting in a ratio denoted \[$Q$\]. It is noticeable that the trends or slopes for the three classes(grass, tree, and person) are strikingly similar. To explore further characteristics, we multiply \[$Q$\] by the range \[$R$\] and \[$R^2$\].

:::: {#fig:q .figure latex-placement="!h"}
![](Viswanath2024OffRoad_figs/qs.png){width="\\textwidth" height="6 cm"}

::: caption
$Q$, $Q*R, Q*R^2$ function for class Grass, Tree and Person.
:::
::::

To further validate the independence of the calibration function from objects, we performed a comparison by dividing the \[$Q$\] values of different classes with each other. Figure [7](#fig:q_r){reference-type="ref" reference="fig:q_r"} presents the deviations in the \[$Q$\] values, resulting in an average value of 1. This outcome provides strong confirmation that \[$Q$\] remains unchanged by variations in the reflectivity parameter, underscoring its object-independent nature.

![Comparing \[Q\] values between different classes to confirm object-independence of calibration function](images/q_ratio.png){#fig:q_r width="\\textwidth" height="4.5 cm"}

We apply a polynomial fitting procedure to the function $Q(r)$. This allows us to transform Velodyne intensity data into the Ouster format by utilizing the following equation: $$\begin{equation}
\centering
\text{Raw Intensity} = Q(r) \times \text{Velodyne}(r)
\end{equation}$$ This method facilitates a seamless conversion of classification ranges from Ouster to Velodyne, enabling a direct translation between the two.

![(a)Velodyne Intensity data of class tree after pre-processing (b) Ouster intensity data of class Tree.](Viswanath2024OffRoad_figs/processed.png){#fig:enter-label width="\\textwidth"}

# Experimental Insights

The decreased mIoU score for the \"bush\" class can be attributed to the considerable overlap in the calibrated intensity range with the \"tree\" class. This is likely due to the similar texture of leaves, stems, and trunks shared by both bushes and trees within the dataset.

During testing, we have observed that the class \"puddle\" is predicted with significantly more accurate distinct boundaries compared to the ground truth, as shown in Fig.[1](#fig:puddle){reference-type="ref" reference="fig:puddle"}. This improvement is achieved by using a mode-based prediction approach that effectively removes the major outliers from the segmentation distribution.

LiDAR scans with higher point density (more channels) yield more accurate surface normal estimations than scans with lower point density. This finding was also observed in [@10.1117/12.2663098]. We noticed that the approach yields better predictions for ranges beyond 10 meters. This improvement can be attributed to the more accurate estimation of $\alpha$ at larger distances, leading to precise estimates of calibrated intensity.

# Conclusions

In this paper we presented analysis of the potential utilization of LiDAR intensity for semantic segmentation of terrestrial LiDAR scans. Our proposed pipeline has demonstrated superior performance compared to the RELLIS-3D benchmarks, particularly in the prediction of the \"puddle\" and \"grass\" classes. It is worth noting that, while our approach may exhibit a lower prediction accuracy compared to other learning-based segmentation frameworks, it is important to emphasize that this study serves as an initial exploration into harnessing the LiDAR intensity parameter for this specific task. We also introduce a preprocessing methodology tailored for Velodyne LiDARs, aiming to enhance cross-platform compatibility. We acknowledge that the current methodology's accuracy can potentially be enhanced by incorporating geometric information derived from LiDAR points or by integrating sparse semantic data from camera images, thereby addressing the challenge of calibrated range overlap. Further investigations can be conducted to test the efficacy of the methods for different climatic conditions as the vegetation and texture of an off-road scene change significantly compared to urban environments.

[^1]: https://github.com/MOONLABIISERB/lidar-intensity-predictor/tree/main

[^2]: The work is supported by **TIH iHUB Drishti-IIT Jodhpur** under project number **23** and accepted for publication at International Symposium on Experimental Robotics 2023.
