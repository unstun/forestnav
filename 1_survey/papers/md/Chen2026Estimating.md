---
citation_key: Chen2026Estimating
arxiv_id: 2602.01085
arxiv_url: https://arxiv.org/abs/2602.01085
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-23T17:48:50Z
origin: ai+web
reviewed: false
---

# Introduction

Force feedback of robotic interaction with wires can be useful for trajectory planning or implementing safety conditions during collisions [@schlechter2001manipulating; @lee2015learning; @nakagawa2018real; @suberkrub2022feel; @zhong2023regressor]. In many such scenarios, the robot does not directly grasp or manipulate the wire -- for example, when a robotic arm nudges a wire into place. In other cases, wires serve merely as passive elements or environmental obstacles that the robot must navigate around. For the case of a robot arm, a common robotic manipulator for wires, force sensors are generally mounted on the end-effector. This allows for interaction forces of an end-effector gripper with a wire to be easily recorded. The problem arises when robot-wire interactions do not happen at the end-effector but instead at other locations along the robot arm. These interactions must be considered because they could lead to restricted or potentially dangerous movement of the robot. Too much tension in the wires could lead to breakages of the wires in the environment. Understanding these interaction forces will allow robots to plan their trajectory based on expectations of how a wire would react to its immediate movement.

For this reason, we introduce an algorithm which estimates the forces on a wire based on its shape. From here we will refer to the wire as an elastic rod. Our work derives consistency conditions, based on force torque balance equations, which determine if sections of an elastic rod in static equilibrium belong to the same undisturbed section where no external interaction forces are present between them. With the section classification and knowledge on the internal stiffness torques of the elastic rod based on the discrete elastic rods (DER) model [@bergou2008discrete], directions and magnitudes of external forces on the rod can be solved for. Due to the indeterminate nature of the problem, the algorithm proceeds by either assuming zero external torque and solving for the force positions, or by assuming that forces are applied at the midpoint of each section and solving for the resulting external torque. A solution to obtain both torques applied and force positions is by detecting collision points along the wire in the real image and identifying their positions visually, although this method will not be discussed in our work. We observe that our approach is closely related to existing proprioceptive sensor-based force and collision estimators [@wahrburg2017motor; @wang2023active; @shan2023fine]. However, prior work primarily applies these methods to robotic arms, where accurately localizing contact forces and estimating their magnitudes remains challenging. In contrast, our method transfers this idea to the wire, leveraging the internal torques of an elastic rod as a proxy for proprioceptive sensing within a similar estimation framework. The inherent discretization of the wire allows for more accurate force localization and estimation.

:::: {#Fig:s2f_overallpipeline .figure latex-placement="t"}
::: {.caption short-caption="Overall Force Estimation Process"}
Overall Force Estimation Process. Rowwise from top left to bottom right: Real image of experiment, depth information, segmentation mask of wire, and final smoothed wire shape with actual and estimated forces (arrows: red - estimated end-clamp force, black - actual force, green - estimated external force).
:::
::::

## Contribution and organization of the paper {#contribution-and-organization-of-the-paper .unnumbered}

The contributions of this paper are twofold. First, we formulate a set of novel consistency conditions to estimate the positions of external interactions along an elastic rod in static equilibrium ([4.1](#Section:estimatingpos){reference-type="ref+Label" reference="Section:estimatingpos"}). Prerequisite assumptions are also stated to ensure the problem is not underdetermined.

Second, using the positions of interactions, parameters of the force and torque can be solved for using a system of linear equations derived from the force-torque balance in each discretized rod piece ([4.2](#Section:estimatingdisturb){reference-type="ref+Label" reference="Section:estimatingdisturb"}). Due to the nature of the problem, one can either solve for the external torque applied or the exact positions of force application, the former requiring an assumption of force application being at the center of mass of the discrete piece, and the latter with the assumption that there is no external torque applied at that discrete piece.

# Related Works

Robotic manipulation of Deformable Linear Objects (DLOs) increasingly emphasizes force sensing and control to overcome limitations such as unknown object properties and visual occlusions. Robots operating in complex or unstructured environments require sophisticated capabilities to safely interact with their surroundings, particularly concerning detecting physical contact and understanding interaction forces.

## Force Control for DLO Manipulation

Foundational work investigated characteristics in force signals for detecting contact state transitions between a DLO and rigid obstacles [@schlechter2001manipulating]. Research reveals that the set of all static equilibrium configurations for a Kirchhoff elastic rod constitutes a smooth manifold of finite dimension that can be explicitly parameterized by moments and forces at the elastic rod base [@bretl2014quasi], and its free configuration space is path-connected [@borum2015free]. This significantly simplifies and enables the construction of gripper paths for manipulation planning of DLOs. Complementary methods focus on estimating DLO shape or contact information primarily from force/torque sensing, achieving real-time 3D shape estimation of elastic rods via a discretized Kirchhoff elastic rod model with gravity compensation [@takano2017real; @nakagawa2018real], or by keeping the DLO under tension for contact inference and primitive execution [@suberkrub2022feel]. Another method is to learn force-based manipulation skills from demonstrations for variable-impedance control, enabling tasks like knot-tightening despite challenges in capturing accurate force profiles [@lee2015learning]. Furthermore, regressor-based model adaptation offers an online adaptation law for unknown DLO deformation parameters, facilitating model-based force control without vision feedback for open-loop shape control in quasi-static scenarios [@zhong2023regressor].

## Contact Detection and Force Estimation

One direct solution for force sensing involves using external sensors, such as distributed tactile 'robot skin' sensors, to detect contact intensity and location across the robot's body and drive it through obstacles [@novak1991capacitance; @albini2021exploiting]. However, integrating such extensive and accurate sensing equipment is often expensive [@nuelle2017force]. To that end, it was found that proprioceptive sensors of the robot can be used for contact detection [@de2005sensorless; @haddadin2008collision; @cho2012collision]. Two main issues faced when using proprioceptive sensors to detect collisions are the system dynamic modeling inaccuracies and the noise from proprioceptive sensors [@haddadin2017robot]. These problems affect the accuracy of the estimated external joint torques and could lead to false positives in contact detection.

Simpler robot models are generally successful in force estimation [@6224977], some integrating visual information as a tool [@lee2018interaction]. Difficulties in modeling the non-linear dynamics of the whole robot arm has led to the utilization of a model-based Kalman filters with motor signals [@wahrburg2017motor], an Extended Kalman Filter torque fusion method [@wang2023active], and a model-free leaning-based neural network approach [@shan2023fine]. Such methods require accurate calibration in the event of modifications to the robot structure which affect its dynamics [@gaz2017payload; @shan2024fast]. Although these works showed some success in estimating the direction, magnitude, and position of external forces, they require additional assumptions such as having only one external contact point [@han2019collision], or that the contacts are applied sequentially [@manuelli2016localizing], due to the underdetermined nature of the problem. The handling of numerous contacts is still a problem that demands attention. This idea of contact detectability has been discussed in-depth [@pang2021identifying], in which small motions that most effectively falsify spurious contact positions has been found. Vision and depth sensing has been utilized in a GPU parallel processing algorithm to effectively determine contact points on a robot arm and react accordingly [@magrini2017human].

# Problem Definition {#Section:ws}

In the following, we use the terms 'elastic rod' and 'wire' interchangeably. We define a rod piece as a discrete section between consecutive nodes of a discretized rod. A section is then defined as a set of consecutive rod pieces that share one or more properties. We categorize pieces of a discretized elastic rod into two section types (s-types): Undisturbed (UD) and Disturbed (D). A UD section is defined as a set of consecutive discretized rod pieces to which no external disturbances are applied. A D section is defined as a set that has at least one disturbance applied to one or more of its pieces. An elastic rod is discretized into $n = n_{\text{UD}} + n_{\text{D}}$ pieces where $n_{\text{s-type}}$ is the total number of s-type pieces (s-type being either UD or D). $N = N_{\text{UD}} + N_{\text{D}}$ is the total number of sections and $N_{\text{s-type}}$ is the number of s-type sections. Each edge in the discretized rod is defined as $\mathbf{e}^{i}=\mathbf{x}_{i+1}-\mathbf{x}_{i}$ where $\mathbf{x}_{i}$ is the Cartesian position of the $i-\text{th}$ piece. Each D section has a set of external force-torque, $\{\mathbf{f}^j, \boldsymbol{\tau}^j\}$, where $0 \leq j < N_{\text{D}}$. Theoretically, our method should be able to detect all force disturbances on an elastic rod provided it fulfills the following condition:

- Elastic rod is in static equilibrium or in sufficiently quasistatic motion. This forms the basis of our method and allows us to derive the equations required.

- Rod must be sufficiently discretized such that there are at least 3 discrete undisturbed pieces between consecutive sections of external disturbances. This ensures that a necessary and sufficient condition can be formed to categorize pieces.

- The 3 undisturbed pieces identified must not be parallel to ensure the problem is not underdetermined. To understand this intuitively, shape of a completely taut wire does not visibly change in response to variations in external force, making it difficult or even impossible to visually infer the force distribution.

- Rod is behavior closely follows the elastic rod theory used. This ensure that the categorization and estimation of forces is accurate.

## Elastic Rod Theory

Before the estimation of external forces and torques can occur, one would have to provide an accurate elastic rod model to compute the internal torques within the system. For our work, we have chosen to use the discrete elastic rods (DER) theory [@bergou2008discrete], which has been implemented as a plugin in MuJoCo [@todorov2012mujoco]. Additionally, we estimate the material properties of the wire with a simple parameter identification pipeline [@chen2025accuratesimulationparameteridentification].

# Formulation {#Section:forms2f}

The total torque on piece $i$ of the discretized rod is $$\begin{equation}
    \boldsymbol{\tau}_{total} - c\boldsymbol{\omega} = \mathbf{I} \boldsymbol{\alpha}
\end{equation}$$ where $\mathbf{I}$ is the second area moment of inertia, $\boldsymbol{\alpha}$ is the angular acceleration vector, $c\boldsymbol{\omega}$ is the damping torque and $\boldsymbol{\tau}_{total}$ is the overall torque on the system. When the rod is in static equilibrium, $\boldsymbol{\alpha} = 0$, $c\boldsymbol{\omega} = 0$. $$\begin{equation}
    \boldsymbol{\tau}_{total} = \left(\mathbf{e}^{i} \times \mathbf{F}^i\right) + \left(\mathbf{a}^i \times \mathbf{f_{c}}^i\right) + \boldsymbol{\tau_c}^i + \mathbf{c}^i = 0,
\end{equation}$$ where $\mathbf{F}^i = \sum_{j\in G_i} \mathbf{f}^j$ such that $G_i$ is the set of all external forces belonging to D sections after piece $i$ (i.e., D sections containing pieces with index $> i$). This means that $\mathbf{F}^k = \mathbf{F}^l$ if $k$ and $l$ belong to the same UD section. $\mathbf{f_{c}}^i$ and $\boldsymbol{\tau_{c}}^i$ are respectively the external force and torque on piece $i$ and are equal to $0$ if $i$ belongs to an UD section. $\mathbf{a}^i = \mathbf{p}_i - \mathbf{x}_i = r\mathbf{e}^i$ where $\mathbf{p}_i$ is the point of application of $\mathbf{f_{c}}^i$, and $r \in [0, 1] \subset \mathbb{R}$. $\mathbf{c}^i$ is the stiffness torque applied on piece $i$ by its adjacent pieces (not to be confused with unbold $c$). Note that the effects of gravity is easily included by adding the torque effects of gravity from the side which $\mathbf{F}_R$ is acting (i.e., adding $\left(\left(n-i-0.5\right)\mathbf{e}^i \right) \times \mathbf{wpp}$ to $\mathbf{c}^i$ where $\mathbf{wpp}$ is a 3-vector describing the weight per piece of the discretized wire).

## Identifying Positions of Disturbances {#Section:estimatingpos}

Suppose two pieces $i$ and $i+1$ belong to the same UD section, the following equations must be consistent. $$\begin{align}
\label{eq:consist2}
    &\mathbf{e}^{i} \times \mathbf{F}^i = -\mathbf{c}^i \\
    &\mathbf{e}^{i+1} \times \mathbf{F}^{i+1} = -\mathbf{c}^{i+1}
\end{align}$$ Knowing $\mathbf{F}^i = \mathbf{F}^{i+1}$, we arrive at the first consistency condition (condition A) which states that $\mathbf{e}^i\cdot\mathbf{c}^{i+1} + \mathbf{e}^{i+1}\cdot\mathbf{c}^{i} = 0$. This is a necessary condition to conclude that these adjacent pieces belong in the same UD section. To check for sufficiency, we investigate the case of piece $i$ belonging to an adjacent D section. $$\begin{align}
\label{eq:necctest}
    &\mathbf{e}^{i} \times \mathbf{F}^i + \mathbf{a}^i \times \mathbf{f_{c}}^i + \boldsymbol{\tau_c}^i = -\mathbf{c}^i \\
    &\mathbf{e}^{i+1} \times \mathbf{F}^{i+1} = -\mathbf{c}^{i+1}
\end{align}$$ Using triple vector product rule, we get $$\begin{equation}
    \mathbf{f_{c}}^i \cdot \left(\mathbf{e}^{i+1} \times \mathbf{a}^i \right) + \mathbf{e}^{i+1}\cdot\boldsymbol{\tau_c}^i = -\left(\mathbf{e}^i\cdot\mathbf{c}^{i+1} + \mathbf{e}^{i+1}\cdot\mathbf{c}^{i}\right).
\end{equation}$$ Knowing that $\text{RHS} = 0$ and $\mathbf{e}^{i+1} \times \mathbf{a}^i \neq 0$ (linear independence condition), we find that the consistency condition can be fulfilled in two cases. The first is when $\mathbf{f_{c}}^i = 0$, which confirms that pieces $i$ and $i+1$ belong to the same UD section. The second is when $\mathbf{f_{c}}^i \cdot \left(\mathbf{e}^{i+1} \times \mathbf{a}^i \right) = 0$. Since $\mathbf{a}^i \parallel \mathbf{e}^i$, this means that condition A can be fulfilled even when the two pieces belong to different sections as long as $\mathbf{f_{c}}^i$ lies in the plane spanned by $\mathbf{e}^{i}$ and $\mathbf{e}^{i+1}$, and $\boldsymbol{\tau_c}^i \perp \mathbf{e}^{i+1}$. Therefore, condition A is not a sufficient condition.

To establish a sufficient condition for pieces to belong to the same UD section, we must check the consistency of 3 adjacent pieces. $$\begin{align}
    \text{Given } &\mathbf{A}_i = \left[\left[\mathbf{e}^i\right]_\times \quad \left[\mathbf{e}^{i+1}\right]_\times \quad \left[\mathbf{e}^{i+2}\right]_\times\right]^T \quad 
    \\ \text{and} \quad &\mathbf{C}_i = -\left[\mathbf{c}^{i} \quad \mathbf{c}^{i+1} \quad \mathbf{c}^{i+2}\right]^T\text{,}
    \\ \text{ where } &\left[\mathbf{e}\right]_\times \text{ is the skew symmetric of 3-vector } \mathbf{e}. \notag
\end{align}$$ The consistency of the above equation according to a manually designed threshold is the second consistency condition we term as condition B -- a necessary and sufficient condition to conclude that the pieces belong to the same UD section. We solve for $\mathbf{F}^{*} = \underset{\mathbf{F}}{\operatorname{argmin}} \norm{\mathbf{A}\mathbf{F} - \mathbf{C}}_2^2$ using least squares. $$\begin{equation}
    \mathbf{F}^{*} = \mathbf{A}^{\!\!+}\mathbf{C}
\end{equation}$$ where $\mathbf{A}^{\!\!+} = \mathbf{V}\boldsymbol{\Sigma}^{\!+}\mathbf{U}^T$ is the pseudoinverse of $\mathbf{A}$ arrived at from the singular value decomposition (SVD) of $\mathbf{A} = \mathbf{U}\boldsymbol{\Sigma}\mathbf{V}^T$.

## Estimating External Disturbances {#Section:estimatingdisturb}

After we have classified the discretized wire pieces into their D and UD sections, we solve for external disturbances.

### Estimating External Forces

It is interesting to note that it is not possible to solve for forces with only one UD piece $\mathbf{e}^{i} \times \mathbf{F}^i = \left[\mathbf{e}^i\right]_\times \cdot \mathbf{F}^i = -\mathbf{c}^i$, as the skew-symmetric of a 3-vector is maximally rank 2, resulting in an underdetermined problem. As such a minimum of 2 pieces are required. The solving and classification processes are combined, and $\mathbf{F}_R$ is calculated as the average of all the $\mathbf{F}^{*}$ for that UD section.

As the wire consists of alternating D and UD sections, the force on section $D_j$ can be calculated as $$\begin{equation}
    \mathbf{f}^j = \mathbf{F}_R^k - \mathbf{F}_R^l + \mathbf{f}_g
\end{equation}$$ such that $k$ and $l$ belong to consecutive UD sections separated by $\text{D}_j$, $k<l$, and $\mathbf{f}_g^j = n_{\text{D}_j} \times \mathbf{wpp}$ is the force contribution due to gravity.

### Estimating External Torques or Force Positions

There are three possible solutions following this. First, we either use a known position of force application for the given D section to compute torque on it. $$\begin{equation}
    \boldsymbol{\tau}_{\text{D}_j} = \left(\mathbf{e}^j_\text{D} \times \mathbf{F}^j_\text{D}\right) + \left(\mathbf{a}^j_\text{D} \times \mathbf{f}^j\right) + \mathbf{c}^j_\text{D} + \boldsymbol{\tau}^j,
\end{equation}$$ such that $\mathbf{e}^j_\text{D} = \mathbf{x}_k - \mathbf{x}_l$ where $k$ and $l$ are the pieces on the two ends of section $\text{D}_j$ and $k>l$. $\mathbf{a}^j_\text{D} = \mathbf{p}_j - \mathbf{x}_l$ where $\mathbf{p}_j$ is the point of application of the external force $\mathbf{f}^j$. $\mathbf{c}^j_\text{D}$ is the stiffness torque applied on $\text{D}_j$ by the UD pieces just adjacent to section $\text{D}_j$ (gravity contributions can be added to this term). Assuming static equilibrium $\boldsymbol{\tau}_{\text{D}_j} = 0$, we can now solve for $\boldsymbol{\tau}^j$.

Second, we can assume that torque acting on the D section is 0 ($\boldsymbol{\tau}^j = 0$) and compute the exact point of external force application on the D section ($\mathbf{p}_j$) under the assumption of static equilibrium.

Third, force is assume to be applied at the mass center of the D section. No torque is computed. The results from our real-world experiments utilize this final solution, as the scope of our work is limited to force prediction. Estimating torque would require capturing internal twist from RGB-D data -- a problem that remains an open challenge in the field.

# Simulation Experiments

A wire was clamped at two points $\SI{50}{cm}$ apart along the wire length. The clamps were held $\SI{30}{cm}$ apart horizontally and the excess wire length was left to dangle. Perfect knowledge on wire stiffness values was assumed. The environment used an adapted DER model [@chen2025accuratesimulationparameteridentification] to simulate bending and twisting behaviors and compute internal stiffness torques. The algorithm used only the wire's pose from the simulation as input and predicted the resulting external interactions. The wire twist could be captured through a call to the API, a capability which is lacking for real experiments. Because the force estimation from shape was relatively fast, it could be run in real time. Forces were input by the user through an interactive simulation viewer. A video of the simulation experiments can be found at <https://youtu.be/_jDbKWxA19w>. Results are plotted in [2](#Fig:s2f_simexp){reference-type="ref+Label" reference="Fig:s2f_simexp"}. As expected from the assumption of quasistatic equilibrium, force estimation performed better when there was less wire movement. Theoretically, force estimation becomes infeasible when the wire undergoes large motions (effectively becoming an underdetermined problem when too many perceived external forces must be predicted). In spite of this, we visually observed that force estimation was able to perform well even in the presence of significant wire motion.

:::: {#Fig:s2f_simexp .figure latex-placement="!htbp"}
::: {.caption short-caption="Force Estimation Simulation Experiments"}
Simulation experiments for force estimation. The top image shows a screen capture of the wire with a force applied through the interactive user visualization window. The actual (black) and estimated (green) forces are shown (overlapping). Two simulation experiments were carried out: **P1** shows the force estimation for varying force magnitude and direction on disturbances at the center of the wire length. **P2** shows the estimation of force position when the point of force application was varied. The solid and dotted lines are the actual and estimated data, respectively. Video of the experiments found here: <https://youtu.be/_jDbKWxA19w>.
:::
::::

# Physical Experiments

## Experimental Set-up

The set-up followed the simulation experiments. A Denso VS-060 robot arm was fitted with a force-torque sensor at its end-effector along with a custom wire clamp attachment. The robot arm was used to manipulate the wire first at its midpoint and then at a $\SI{7}{cm}$ offset along the wire length from its center. Actual force readings were recorded with the force-torque sensor and filtered using a Chebyshev filter. Due to the limitation of capturing internal twist from visual and depth information, our results assumed a zero-twist configuration of the rod, focusing solely on force prediction and not torque estimation. Although gripper movement would introduce external torque on the wire, this did not affect force prediction, as the force prediction and torque estimation parts of the pipeline were separate. The result was still a prediction of the external force from the gripper on the wire.

The wire shape was obtained through the pipeline presented in [@zhaole2023robust], leveraging GROUNDED-SAM, a zero-shot image segmentation framework, which we found to be both easy to implement and accurate, with the drawback of longer computational times (overall detection pipeline takes $\SI{8}{s}$ per 720p frame on an NVIDIA GeForce RTX 3060 Ti GPU). The wire was discretized into 60 pieces after smoothing and interpolated into 30 discrete pieces for further processing. For DLO smoothing, we used a trade-off between the error from node displacement due to smoothing ($p_{\text{smooth}}$) and the decrease in elastic potential energy in the rod ($E_{\text{decrease}}$). As long as $J_{i} > J_{i-1}$ where $i$ is the time step and $J = E_{\text{decrease}} - m_p*p_{\text{smooth}}$, smoothing continued. In this work, we applied time stepping through the DER model implemented in MuJoCo and included a plugin state which provides the potential energy in the rod. The same model was used to compute internal torques in the rod.

## Results

The experiments were split into two main parts. Coordinate frame of the experiment was defined as shown in plots of [3](#Fig:s2fexpA_vis){reference-type="ref+Label" reference="Fig:s2fexpA_vis"}. For the first part (**A**), the wire was clamped to the robot end-effector at its center ($\SI{25}{cm}$ along its length from the left end) in its equilibrium position and moved into 6 different positions with pure translational motion (orientation remains constant). Position displacement from the neutral positions are shown in [3](#Fig:s2fexpA_vis){reference-type="ref+Label" reference="Fig:s2fexpA_vis"}. These positions were selected for variety and the distance was chosen to ensure the condition of non-parallel discrete pieces was fulfilled as much as possible (to avoid an underdetermined problem). The actual and estimated force vectors for experiment **A** are shown in [3](#Fig:s2fexpA_vis){reference-type="ref+Label" reference="Fig:s2fexpA_vis"}. Vectors within each plot are shown to scale relative to each other, but their scales are not consistent across different plots.

For the second part (**B**), the wire was clamped to the robot end-effector at a $\SI{7}{cm}$ offset along the wire length from its center ($\SI{18}{cm}$ along its length from the left end) in its equilibrium position and moved into 4 different positions with pure translational motion. The actual and estimated force vectors for experiment **B** are shown in [4](#Fig:s2fexpB_vis){reference-type="ref+Label" reference="Fig:s2fexpB_vis"}. Overall quantitative results for both experiments (**A** and **B**) comparing the actual ($\mathbf{F}_{\text{act}}$) and estimated ($\mathbf{F}_{\text{est}}$) forces are shown in [\[Table:s2f_force_data\]](#Table:s2f_force_data){reference-type="ref+Label" reference="Table:s2f_force_data"}. To evaluate the accuracy of the estimated force $\mathbf{F}_{\text{est}}$ compared to the actual force $\mathbf{F}_{\text{act}}$, we computed several error metrics. To assess directional accuracy, we computed the *angle difference* between the vectors. The *relative L2 error* normalizes the L2 error by the magnitude of the actual force, yielding $\frac{ \left\| \mathbf{F}_{\text{est}} - \mathbf{F}_{\text{act}} \right\|_2 }{ \left\| \mathbf{F}_{\text{act}} \right\|_2 + \varepsilon },$ where $\varepsilon$ is a small constant added to avoid division by zero. Lastly, to evaluate the spatial accuracy of the estimated point of application, we computed the *position difference* between the estimated and actual contact points as $\left\| \mathbf{p}_{\text{est}} - \mathbf{p}_{\text{act}} \right\|_2,$ where $\mathbf{p}$ is the position at which the force acts.

:::: {#Fig:s2fexpA_vis .figure latex-placement="!htbp"}
::: {.caption short-caption="Visual Results of Force Estimation for Centered Displacement"}
Visual results of force estimation for experiment **A** where the wire was clamped at both ends and attached to the robot end-effector at its center. The robot end-effector was fitted with a force-torque sensor and moved into 6 different positions. The left column shows the real experiment images (coordinates axes shown in first image) with Cartesian displacement of the grasped point (below), and the right column shows the smoothed wire shape along with the actual and estimated force vector (arrows: red - estimated end-clamp force, black - actual force, green - estimated external force). Note that the accuracy of end-clamp forces are not analyzed.
:::
::::

:::: {#Fig:s2fexpB_vis .figure latex-placement="!htbp"}
::: {.caption short-caption="Visual Results of Force Estimation for Off-centered Displacement"}
Visual results of force estimation for experiment **B** where the wire was clamped at both ends and attached to the robot end-effector at a $\SI{7}{cm}$ offset along the wire length from its center.
:::
::::

[]{#Table:s2f_force_data label="Table:s2f_force_data"}

::: center
:::

## Discussion

In scenarios **A4**, **A5**, **B1**, and **B4**, additional erroneous forces were detected. For our analysis, we only compared the largest magnitude force with the actual force sensed. The *relative L2 error* and *angle difference* were generally lower for single direction wire displacements, with the exception of **B1**. Along with **A4**, **A6**, and **B4**, we found that displacement and forces in the $x$-direction were not easily detected with our method and caused relatively large relative L2 errors and angle differences. For the cases of **A4** and **B4**, the algorithm seemed to dissect the forces and identify additional force disturbances (other green arrows) which have an $x$-direction contribution, but these were not considered in our analysis.

Interestingly, these forces which were difficult to detect were those that act nearly tangentially to the wire. That could be a hint that the algorithm in its current state is not suited to accurately determine tangential forces due to the sensitivity of calculated tangential forces to the error in positions and orientations of the discretized wire pieces, and wire physical properties. We speculate that these errors likely result from two main causes: the wire not having purely elastic deformation properties and imperfect determination of wire position using the depth camera. The latter of which can be solved with improved detection capabilities. The former proves to be a more complex issue and could directly affect our results as the algorithm might recognize internal torque in the wire where it is not actually present, requiring further intense investigations into modeling of plastic deformations in DLOs.

Estimations on the position of force application were all below $\SI{40}{mm}$ and experienced better results for experiment **A** than **B**. This could be due to a displacement at the midpoint of the wire **A** producing more deformation in the wire which the algorithm is sensitive to.

# Conclusion

In this work, we introduced an algorithm to estimate external forces acting on an elastic rod based on its observed shape. By deriving consistency conditions from static force-torque balance equations, we identified undisturbed sections of the rod where no external interactions occur. Leveraging this classification and internal stiffness torque models from the DER formulation, we solved for the direction and magnitude of external forces. Experimental results validated the method's effectiveness by comparing the estimated forces against ground truth readings from physical sensors during robot-wire interactions.

## Limitations and Future Work

Through our experiments, we assume the wire behaves in a purely elastic way which is not an accurate model for its true behavior. The real wire experiences plastic deformation as can be seen from the undisturbed kinks sometimes found in the wire when recovering from large deformation. Although this property is partially hidden when smoothing the visually detected DLO, it definitely affects the accuracy of our results. Past works aimed at manipulating wires with such properties use learning techniques [@laezza2021learning; @matl2021deformable] or model the plasticity directly with known physical properties [@terzopoulos1988deformable].

Wire detection using the Azure Kinect's time-of-flight infrared depth sensor is prone to significant noise, particularly in regions where the wire is in contact with or occluded by other objects. This noise adversely affects the accuracy of shape and force estimation. The proposed method would benefit significantly from a higher-resolution, lower-noise wire detection approach. This remains an active area of research within the field of deformable linear object perception [@caporali2023rt; @xiang2023trackdlo; @lv2022learning; @zhaole2023robust].

[^1]: \*Github repo: <https://github.com/qj25/ds2f> (Videos: <https://youtu.be/_jDbKWxA19w>)

[^2]: $^{1}$Nanyang Technological University, School of Mechanical and Aerospace Engineering, $^{2}$University of Illinois Urbana-Champaign, $^{3}$Eureka Robotics, Singapore
