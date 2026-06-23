---
citation_key: Min2025Advancing
arxiv_id: 2510.16500
arxiv_url: https://arxiv.org/abs/2510.16500
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-23T18:37:12Z
origin: ai+web
reviewed: false
---

# Introduction

Off-road autonomous driving has attracted increasing attention in recent years due to its potential in enabling intelligent transportation and robotic systems to operate in unstructured and complex environments [@min2024autonomous]. As illustrated in Fig. [1](#difference){reference-type="ref" reference="difference"}, unlike urban or highway settings---where well-marked lanes, standardized traffic rules, and high-quality maps provide strong priors---off-road scenarios are characterized by irregular terrains, sparse or absent road markings, unpredictable obstacles, and rapidly changing environmental conditions [@shu2025overview]. These factors pose significant challenges for perception, planning, and control systems, necessitating robust algorithms capable of handling extreme variability in both appearance and geometry [@chen2025scene].

::::: {#difference .figure}
::: minipage
![](Min2025Advancing_figs/compare.png){width="8cm"}
:::

::: caption
On-road environments are characterized by well-structured infrastructure---such as lane markings, traffic signs, and clearly delineated roadways---that provide consistent and reliable navigational cues. In stark contrast, off-road environments lack paved surfaces and structured guidance, instead featuring irregular, heterogeneous, and often ambiguous terrain. This absence of formal infrastructure greatly amplifies the complexity of perception and navigation tasks.
:::
:::::

Despite the growing interest in this domain, progress in off-road autonomous driving research has been hindered by the scarcity of large-scale, high-quality datasets. Existing datasets for autonomous driving predominantly focus on structured, on-road environments, limiting the generalization and robustness of models when deployed off-road. Moreover, the few publicly available off-road datasets are often constrained in size, diversity, or sensing modalities, leaving a gap in supporting comprehensive research on perception and planning under diverse off-road conditions.

To address this gap, we present ORAD-3D---to the best of our knowledge, the largest and most diverse dataset dedicated to off-road autonomous driving. The dataset was collected across a broad spectrum of terrains, including woodlands, farmlands, grasslands, riversides, gravel roads, cement roads, and rural areas. It encompasses a rich set of environmental conditions, covering multiple weather scenarios (sunny, rainy, foggy, and snowy) and illumination states (bright daylight, daytime, twilight, and nighttime). The data are captured using multi-sensor configurations, enabling both 2D and 3D perception tasks.

In addition to releasing ORAD-3D, we establish a comprehensive set of benchmark evaluations to enable fair and reproducible comparisons in off-road autonomous driving research. Specifically, we evaluate five core tasks: (1) 2D free-space detection, (2) 3D occupancy prediction, (3) rough GPS-guided path planning, (4) VLM-based autonomous driving, and (5) world model for off-road autonomous driving. Determining traversable areas is essential for safe off-road navigation; thus, we first construct a benchmark for 2D free-space detection based on large-scale off-road imagery. Recognizing the critical role of 3D terrain geometry, we further provide 3D occupancy annotations for predicting terrain structure in 3D space. Given that GPS signals in off-road environments are often noisy or inaccurate---making precise localization challenging---we design a benchmark for rough GPS-guided path planning to evaluate navigation under such uncertainty. Inspired by the rapid progress and strong generalization capability of Vision--Language Models (VLMs), we introduce a benchmark for VLM-based scene understanding and path planning in diverse off-road scenarios. Finally, we construct an off-road world model capable of controllably generating diverse future off-road scenarios. Together, these benchmarks span a representative spectrum of perception and decision-making challenges encountered in real-world off-road environments.

By providing both a large-scale, diverse dataset and well-defined benchmarks, ORAD-3D aims to serve as a foundational resource for the off-road autonomous driving community. We anticipate that it will accelerate the development of algorithms that are robust to terrain variability, adverse weather, and low-visibility conditions---ultimately pushing the frontier of safe and reliable off-road autonomous driving.

The highlights of our work are as follows:

- **ORAD-3D dataset** -- We release the largest and most diverse off-road autonomous driving dataset to date, covering multiple terrains, weather conditions, and illumination levels with synchronized multi-sensor data.

- **Environmental diversity** -- The dataset includes challenging and underrepresented scenarios such as woodlands, farmlands, grasslands, riversides, and rural roads, with extensive weather and lighting variations.

- **Benchmark suite** -- We establish standardized benchmarks for 2D free-space detection, 3D occupancy prediction, rough GPS-guided path planning, VLM-based autonomous driving, and off-road world model.

- **Research resource** -- ORAD-3D serves as a comprehensive platform for developing and evaluating robust perception and planning algorithms in unstructured off-road environments.

# Related Work

## Off-Road Autonomous Driving

Off-road perception research primarily targets road segmentation and traversability estimation in unstructured, complex terrains. Recent works enhance passable area detection using advanced CNNs and Transformer architectures [@sun2023passable; @chung2024pixel], while others integrate RGB imagery with point clouds to achieve more robust terrain mapping and navigation [@guan2021tns; @guan2023vinet]. Multi-modal fusion techniques combining RGB, depth, and LiDAR data have been employed to improve free-space detection and obstacle classification [@bae2023self; @feng2023adaptive; @m2f2; @kim2024ufo]. Noise-robust networks and Transformer-based models further refine segmentation accuracy in challenging conditions [@lv2024noise; @yan2024fsn]. Contrastive and self-supervised learning approaches reduce dependence on dense labels, enabling fine-grained terrain understanding from limited annotations [@gao2021fine; @seo2023learning; @jung2023v]. Off-road semantic segmentation methods such as OFFSEG [@offseg] and OffRoadTranSeg [@singh2021offroadtranseg] tackle class imbalance and domain adaptation issues via semi-supervised strategies. Fusion-based frameworks leverage uncertainty modeling and attention mechanisms to enhance mapping and perception in unstructured environments [@lian2023research; @feng2024multi; @kim2024uncertainty]. Xu et al. [@xu2022trajectory] propose an end-to-end Transformer-based framework for map-less autonomous driving, which takes raw LiDAR data and a noisy topometric map as inputs and generates precise local trajectories for navigation. While these approaches demonstrate promising results, most are trained and evaluated on small-scale datasets. To address this limitation, we introduce a large-scale off-road dataset with comprehensive benchmark results.

## Datasets for Off-Road Autonomous Driving

::: center
:::

Existing off-road autonomous driving datasets predominantly target perception-oriented tasks, such as traversability estimation and semantic segmentation. Identifying traversable areas is particularly critical for autonomous vehicles. TrailNet[@hoveidar2018autonomous] is among the first datasets to examine road surface types using publicly available camera data. ORFD[@orfd] provides high-resolution imagery and annotations for detecting navigable regions across diverse off-road conditions. Verti-Wheelers[@datar2023toward] addresses wheeled mobility on steep terrain, while M3-GMN[@m3gmn] advances grid map--based navigation. For semantic segmentation in off-road environments, several datasets have been introduced. YCOR[@maturana2018real] offers multi-season imagery, whereas BotanicGarden[@liu2024botanicgarden] contains annotated images for robot navigation in botanical gardens. RUGD[@rugd] provides multimodal sensor data to support perception in outdoor scenes. More recently, RELLIS-3D[@rellis-3d], GOOSE[@mortimer2023goose], and WildScenes[@wildscenes] have released multimodal datasets for robust perception in complex natural environments. UnScenes3D [@chen2025scene] focuses on 3D semantic occupancy as a central representation for off-road understanding. While these datasets have significantly contributed to the field, most remain limited in scale and primarily emphasize perception tasks. In contrast, this work introduces a large-scale off-road dataset that not only supports perception tasks but also includes planning tasks and vision--language model--driven autonomy, thereby providing a more comprehensive resource for advancing off-road autonomous driving research.

:::: {#type .figure latex-placement="t"}
![](Min2025Advancing_figs/scene.png){width="6.8in"}

::: caption
ORAD-3D dataset contains a variety of off-road scenes.
:::
::::

:::: {#weather .figure latex-placement="t"}
![](Min2025Advancing_figs/weather.png){width="3.4in"}

::: caption
Different weather conditions are considered in ORAD-3D.
:::
::::

:::: {#day .figure latex-placement="t"}
![](Min2025Advancing_figs/light.png){width="3.4in" height="2.2in"}

::: caption
Different light conditions are considered in ORAD-3D.
:::
::::

:::: {#turn .figure latex-placement="t"}
![](Min2025Advancing_figs/type.png){width="3.4in" height="2.2in"}

::: caption
Different road types are considered in ORAD-3D.
:::
::::

# ORAD-3D Dataset

We present ORAD-3D, a comprehensive off-road autonomous driving dataset curated from multi-season recordings spanning winter to summer. It covers diverse terrains, weather, lighting, and road types, providing rich data essential for robust perception and accurate future forecasting. ORAD-3D includes data such as images, LiDAR, pose, and depth. The provided annotations include 2D free-space segmentation, 3D occupancy, driving trajectories, and scene text descriptions.

:::: table*
::: center
   Split   Grassland   Field    Wilderness   Forest   Riverside   Gravel   Rural    Asphalt   Cement    Mud    Total      \%
  ------- ----------- -------- ------------ -------- ----------- -------- -------- --------- -------- ------- -------- --------
   Train     3,921     5,610      2,146      7,005      1,770     4,424    5,734     1,467    7,481     369    39,927   69.07%
    Val       345       960        343        478        334       642      860       336     1,086     333    5,717    9.89%
   Test      1,092     1,900      1,047      1,785       393      1,233    1,719      528     1,999     468    12,164   21.04%
   Total     9.27%     14.65%     6.12%      16.03%     4.32%     10.90%   14.38%    4.03%    18.28%   2.02%   57,808    100%

[]{#scene label="scene"}
:::
::::

::: center
:::

:::: {#sensor .figure latex-placement="t"}
![](Min2025Advancing_figs/sensor.png){width="3.4in"}

::: caption
Detail information of vehicle and sensor to collect LiDAR and camera data.
:::
::::

::: center
:::

## Data Curation and Statistics {#data-description}

### Diverse Scenes

Unlike the uniformity of structured on-road environments, off-road scenarios are characterized by diverse types, such as grasslands, forests, deserts, farmlands, and mountainous terrain, as shown in Fig. [2](#type){reference-type="ref" reference="type"}. Furthermore, off-road environments contain numerous elements that are irregular in shape, with blurred boundaries and semantically ambiguous categories. The heterogeneity and spatial disorder of open off-road scenes significantly exceed the cognitive limits of structured roadways. Structurally, the absence of lane markings and traffic signs removes clear guidance, while natural features like trees and deep ravines contribute to feature sparsity in models. To address these challenges, we have collected off-road data from a variety of environments, including grasslands, forests, deserts, and farmlands, laying the foundation for off-road autonomous driving. The data distribution across various scenes is shown in Table [\[scene\]](#scene){reference-type="ref" reference="scene"}.

### Weather Conditions

Off-road scenarios often encounter sudden weather changes, such as shifts from sunny to rainy, foggy to snowy conditions, and so on, as shown in Fig. [3](#weather){reference-type="ref" reference="weather"}. Typically, there is a larger volume of autonomous driving data available for sunny weather. However, obtaining corner case data for rare and extreme weather scenarios, such as rain, fog, and snow, is crucial for enhancing the accuracy of off-road autonomous driving models. To address this, we have specifically collected off-road scene data under various extreme weather conditions, including rain, snow, fog, and sunny days. The data distribution across weather conditions is shown in Table [\[weather_con\]](#weather_con){reference-type="ref" reference="weather_con"}.

### Lighting Variations

Lighting variations have a significant impact on autonomous driving performance. To address this, we have collected off-road scene data under various lighting conditions, including bright light, daylight, twilight, and darkness, as shown in Fig. [4](#day){reference-type="ref" reference="day"}. Data collection during the evening and nighttime is particularly challenging due to reduced visibility and the complexity of environmental factors. To overcome these challenges, we specifically focused on gathering data during twilight and nighttime, allowing the model to learn the unique distribution of off-road data under low-light conditions. By incorporating these varying lighting conditions into the training process, we aim to improve the robustness and accuracy of off-road autonomous driving models in challenging lighting situations. The data distribution across lighting variations is shown in Table [\[light\]](#light){reference-type="ref" reference="light"}.

### Road Type

Autonomous vehicles are required to perform a variety of driving maneuvers, such as traveling in a straight line, turning, and navigating complex terrain. Generating video representations of future scenes based on these driving actions is highly valuable, as it allows the vehicle to anticipate and adapt to its surroundings. In off-road environments, the terrain is often rugged and uneven, with frequent uphill and downhill maneuvers that present significant challenges to both vehicle control and data collection. This makes it difficult to obtain comprehensive and diverse datasets that capture the full range of possible off-road driving scenarios. To address this challenge, we have collected a diverse set of video data corresponding to various driving actions, with a particular focus on off-road scenarios, as illustrated in Fig. [5](#turn){reference-type="ref" reference="turn"}.

### Data collection

The vehicle used for collecting the ORAD-3D dataset is the Mazda Ruiyi 6 Coupe, manufactured by FAW. Its body dimensions are 4,755 mm $\times$ 1,795 mm $\times$ 1,440 mm, with a wheelbase of 2,725 mm and a track width of 1,560 mm (both front and rear). A sensor fusion kit, Pandora, developed by Hesai Technology, is mounted on the vehicle's roof to capture LiDAR point cloud and RGB image data. The system is equipped with five cameras positioned around the lower part of the vehicle, including one color camera and four wide-angle black-and-white cameras. Detailed specifications of the vehicle and sensors are shown in Fig. [6](#sensor){reference-type="ref" reference="sensor"}. We collected 145 sequences from various off-road environments across China, spanning from spring to winter. Each sequence covers a distance of approximately 100 meters, and the size of the RGB images is 1280 $\times$ 720 pixels.

# ORAD-3D Benchmarks

Building on the large-scale off-road autonomous driving dataset ORAD-3D, we evaluate five core tasks: (1) 2D free-space detection, (2) 3D occupancy prediction, (3) rough GPS-guided path planning, (4) VLM-based autonomous driving, and (5) off-road world model.

## 2D Free-Space Detection {#tasks}

:::: {#orfd .figure latex-placement="h"}
![](Min2025Advancing_figs/label.png){width="3.4in"}

::: caption
The annotation 2D off-road free-space detection.
:::
::::

### Label Generation

Unlike the ORFD [@orfd] dataset, which adopts a binary road/non-road labeling scheme, our annotation protocol (Fig. [7](#orfd){reference-type="ref" reference="orfd"}) captures the complexity of off-road environments by including fine-grained classes such as safe road, boundary transition zones, puddles, rocks, vehicles, and pedestrians. This detailed semantic representation enables more nuanced terrain understanding and supports safer autonomous navigation.

### Benchmark Method

Building on existing off-road free-space detection methods, we conduct experiments on the ORAD-3D dataset using both multimodal and vision-only approaches. Detailed comparative analyses are presented in the experimental results section.

## 3D Occupancy Prediction

:::: {#occ .figure latex-placement="h"}
![](Min2025Advancing_figs/occ.png){width="3.4in"}

::: caption
The Annotation 3D occupancy prediction.
:::
::::

### Label Generation

Relying solely on 2D off-road free-space detection results is insufficient for accurately modeling complex 3D terrains. To address this limitation, we further construct 3D occupancy annotations for off-road environments. Specifically, we first apply the LiDAR odometry method KISS-ICP [@vizzo2023ral] to register the collected LiDAR point clouds and obtain precise pose estimates. Multiple frames are then accumulated to generate dense point clouds, from which the 3D occupancy labels are subsequently derived (Fig. [8](#occ){reference-type="ref" reference="occ"}).

Existing off-road 3D occupancy prediction benchmarks, such as Wild-Occ [@zhai2024wildocc], are collected from small-scale platforms with limited coverage and relatively simple terrain.

### Benchmark Method

We conduct extensive experiments on ORAD-3D using a range of 3D occupancy prediction methods, encompassing both general-purpose approaches and algorithms tailored for off-road environments.

## Rough GPS-guided Path Planning

:::: {#model .figure latex-placement="h"}
![](Min2025Advancing_figs/rough.png){width="3.4in"}

::: caption
The flowchart for rough GPS-guided local path planning.
:::
::::

### Label Generation

In off-road environments, GPS signals are often unreliable, preventing autonomous vehicles from obtaining accurate localization. To address this, we construct a rough GPS-guided path planning benchmark dataset. Specifically, we use the previously estimated poses as ground-truth driving trajectories and apply B-spline interpolation to generate waypoints. We then introduce controlled perturbations to these trajectories to simulate the effects of inaccurate GPS localization.

### Benchmark Method

We adopt the method proposed by Xu et al. [@xu2022trajectory] as our benchmark for rough GPS-guided path planning (Fig. [9](#model){reference-type="ref" reference="model"}). This approach takes LiDAR BEV maps and rough routes as inputs, employing a Transformer-based backbone to predict waypoints. Building upon this, we further incorporate an uncertainty module to enhance the accuracy and reliability of the path planning.

## VLM-based Autonomous Driving {#tass2}

:::: {#dis .figure latex-placement="h"}
![](Min2025Advancing_figs/dis.png){width="3.4in"}

::: caption
Textual description annotation of off-road scenes.
:::
::::

### Label Generation

Recent advances in VLMs have demonstrated their ability to analyze complex scenes through chain-of-thought reasoning, enabling end-to-end autonomous driving. However, research on applying VLMs to off-road autonomous driving remains limited. In this work, we first leverage the multimodal large model Qwen2.5-VL [@Qwen2.5-VL] to annotate images from the ORAD-3D dataset, generating detailed scene descriptions as illustrated in Fig. [10](#dis){reference-type="ref" reference="dis"}. Subsequently, using pose data as ground-truth trajectories, we prompt the VLM to predict future paths, enabling end-to-end path planning in off-road scenarios.

### Benchmark Method

:::: {#vlm .figure latex-placement="h"}
![](Min2025Advancing_figs/flowchart.png){width="3.4in"}

::: caption
The flowchart for VLM-based off-road autonomous driving.
:::
::::

We construct an off-road VLM-based autonomous driving benchmark on OpenEMMA [@xing2025openemma], integrating a chain-of-thought (CoT) reasoning mechanism to handle the complexity of unstructured environments. As shown in Fig. [11](#vlm){reference-type="ref" reference="vlm"}, the model takes RGB images and prompt as inputs, performs step-by-step analysis of terrain, obstacles, and navigable areas, and outputs future trajectory waypoints for end-to-end path planning, leveraging VLM generalization while adapting reasoning to off-road challenges.

## Off-road World Model

In contrast to the abundance of large-scale datasets readily available for urban autonomous driving, research on off-road autonomous driving remains significantly constrained by the scarcity of suitable data. This paper seeks to address this critical limitation by investigating off-road scene data generation through the development of a world model capable of producing diverse and controllable off-road scenarios [@zhu2024sora]. Specifically, the proposed approach enables the synthesis of off-road data under extreme weather and illumination conditions, from multiple viewpoints, and across heterogeneous road environments, thereby substantially enhancing both the scale and diversity of off-road datasets.

### Benchmark Method

:::: {#wm .figure latex-placement="h"}
![](Min2025Advancing_figs/wm.png){width="3.4in"}

::: caption
The flowchart for off-road world model.
:::
::::

We introduce an off-road world model framework (Fig. [12](#wm){reference-type="ref" reference="wm"}) that redefines the architecture of Stable Video Diffusion (SVD) [@svd] for off-road autonomous driving applications. Diverging from conventional image-to-video generation paradigms, our approach introduces a dual-stream conditioning mechanism that simultaneously processes visual observations and vehicular control signals [@wang2024drivingdojo]. These features are then spatially aligned with the encoded visual features from the initial observation frame using cross-attention layers in the modified U-Net backbone [@ronneberger2015u]. This synergistic integration enables the diffusion model to generate temporally coherent video predictions that strictly adhere to specified conditions while maintaining visual consistency with the environmental context.

# Experimental Results

In this section, experiments are conducted to validate the performance of the proposed dataset and baseline method.

## 2D Free-Space Detection {#d-free-space-detection}

:::: {#road_re .figure latex-placement="h"}
![](Min2025Advancing_figs/road_pred.png){width="3.4in"}

::: caption
Visualization of 2D free-space detection.
:::
::::

::: center
:::

As shown in Fig. [13](#road_re){reference-type="ref" reference="road_re"}, the proposed off-road free-space detection algorithm (ROD [@sun2025rod]) effectively delineates off-road boundaries, median grass strips, and safe regions, thereby providing fine-grained road information that facilitates off-road autonomous driving. Quantitative results are presented in Table [\[results_road\]](#results_road){reference-type="ref" reference="results_road"}. Compared to multimodal baselines such as M2F2-Net [@m2f2] and OFF-Net [@orfd], the vision-only ROD [@sun2025rod], built upon a ViT backbone, demonstrates superior accuracy in predicting detailed road information.

## 3D Occupancy Prediction

:::: {#occ_re .figure latex-placement="h"}
![](Min2025Advancing_figs/occ_pred.png){width="3.4in"}

::: caption
Visualization of 3D occupancy prediction.
:::
::::

::: {#tab:comparisons}
                Method                IoU$\uparrow$   mIoU$\uparrow$
  ---------------------------------- --------------- ----------------
          OpenOcc[@openocc]               9.54             5.83
   OccFormer[@Zhang2023OccFormerDT]       12.24            7.45
      SurroundOcc [@surroundocc]          11.87            7.60

  : 3D Semantic Occupancy Prediction Results on ORAD-3D test set.
:::

[]{#tab:comparisons label="tab:comparisons"}

Accurate 3D terrain modeling is crucial for off-road autonomous driving. As shown in Fig. [14](#occ_re){reference-type="ref" reference="occ_re"}, the predicted 3D occupancy results demonstrate that the model can capture the 3D structure of complex off-road environments. Quantitative results are reported in Table [1](#tab:comparisons){reference-type="ref" reference="tab:comparisons"}, where the fusion of LiDAR and vision yields higher prediction accuracy for 3D occupancy estimation.

## Rough GPS-guided Path Planning

:::: {#traj_re .figure latex-placement="h"}
![](Min2025Advancing_figs/traj.png){width="3.4in"}

::: caption
Visualization of local path planning under the guidance of rough GPS. Blue: local route. Red: ground truth trajectory. Green: predicted trajectory.
:::
::::

::: center
:::

As shown in Fig. [15](#traj_re){reference-type="ref" reference="traj_re"}, although GPS localization is imprecise, the model can effectively plan trajectories along the safe road centerline under the guidance of rough GPS, particularly in turning regions. This capability is crucial for off-road autonomous driving, where localization is often unreliable. Table [\[gps_re\]](#gps_re){reference-type="ref" reference="gps_re"} provides the quantitative comparison of trajectory planning performance.

## VLM-based Autonomous Driving {#vlm-based-autonomous-driving}

:::: {#vla_vlm .figure latex-placement="h"}
![](Min2025Advancing_figs/vla_vlm.png){width="3.4in"}

::: caption
Visualization of the predicted trajectories via VLM.
:::
::::

::: tabular
c\|cccc\|c \*Method & &\*Failure\
&1s &2s &3s &Avg. &Rate(%)$\downarrow$\
Qwen2.5-VL [@Qwen2.5-VL] &1.95&2.21&2.90&2.35&82.55\
OpenEMMA [@xing2025openemma] &1.73 &1.92 &2.75 &2.13 &57.56\
LightEMMA [@qiao2025lightemma] &1.72 &1.88 &2.63 &2.08 &55.63\
:::

[]{#vla label="vla"}

[]{#tab:planning label="tab:planning"}

As illustrated in Fig. [16](#vla_vlm){reference-type="ref" reference="vla_vlm"}, VLMs can perform fine-grained analysis of off-road scenes conditioned on prompts, such as recognizing objects, weather, and road conditions, and subsequently generating a planned trajectory. Quantitative results in Table [\[vla\]](#vla){reference-type="ref" reference="vla"} demonstrate that OpenEMMA [@xing2025openemma] and LightEMMA [@qiao2025lightemma] outperform the zero-shot Qwen2.5-VL [@Qwen2.5-VL] in path planning tasks.

## Off-road World Model

:::: {#result1 .figure latex-placement="h"}
![](Min2025Advancing_figs/results.png){width="3.3in"}

::: caption
Future driving video generation will involve the interaction of driving actions with various conditions, enabling the creation of driving videos that correspond to different scenarios and driving behaviors.
:::
::::

:::: center
::: {#wm_re}
     Method     Dataset   FID$\downarrow$   FVD$\downarrow$
  ------------ --------- ----------------- -----------------
   SVD [@svd]     \-           79.5              534.2
    Baseline    ORAD-3D        70.2              486.6

  : Quantitative results of off-road world model.
:::

[]{#wm_re label="wm_re"}
::::

The results in Table [2](#wm_re){reference-type="ref" reference="wm_re"} demonstrate that models trained on our dataset deliver superior visual quality. As shown in Fig. [17](#result1){reference-type="ref" reference="result1"}, the world model trained on the ORAD-3D dataset is capable of accurately generating future scene videos. Notably, the model can generate the required future scenarios based on specific conditions, greatly reducing the cost of collecting off-road scene data and advancing research in off-road autonomous driving.

# Conclusion

In this work, we introduced ORAD-3D, the largest and most diverse dataset for off-road autonomous driving to date. Collected across a wide variety of terrains, weather conditions, and illumination scenarios, ORAD-3D provides multi-sensor data to support both 2D and 3D perception tasks. Beyond data collection, we established four representative benchmarks---2D free-space detection, 3D occupancy prediction, rough GPS-guided path planning, VLM-based autonomous driving, and off-road world model---covering essential challenges in perception and decision-making for unstructured environments. We believe ORAD-3D will serve as a key resource to advance research on robust off-road autonomy, facilitating the development of algorithms capable of operating reliably under diverse and adverse conditions.

**Limitations and Future Work.** Off-road environments are highly complex, yet current datasets remain limited in scale and obstacle diversity. Future work will expand terrain coverage and capture more challenging scenarios with diverse obstacles to better evaluate algorithm robustness in real-world conditions.

[^1]: $^{1}$Research Center for Intelligent Computing Systems, SKLP, Institute of Computing Technology, Chinese Academy of Sciences, Beijing, China, 100190.

[^2]: $^{2}$Tongji University, Shanghai, China, 200092.

[^3]: $^{3}$Xi'an Jiaotong University, Shaanxi, China, 710049.

[^4]: $^{4}$Nanchang University, Jiangxi, China, 330047.

[^5]: $^{5}$Defense Innovation Institute, Beijing, China, 100073.

[^6]: $^{*}$ Corresponding author Dawei Zhao and Yu Hu. Email: `adamzdw@163.com and huyu@ict.ac.cn`
