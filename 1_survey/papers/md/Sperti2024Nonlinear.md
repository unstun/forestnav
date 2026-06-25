---
citation_key: Sperti2024Nonlinear
arxiv_id: 2404.05343
arxiv_url: "https://arxiv.org/abs/2404.05343"
title: "Non-linear Model Predictive Control for Multi-task GPS-free Autonomous Navigation in Vineyards"
authors_short: "Matteo Sperti et al."
year: 2024
direction_tag: O_dense_forest_narrow_passage
source: mineru-vlm
converter: mineru-open-api
model: vlm
converted_at: 2026-06-25T09:23:20Z
origin: ai+web
reviewed: false
---

# NON-LINEAR MODEL PREDICTIVE CONTROL FOR MULTI-TASK GPS-FREE AUTONOMOUS NAVIGATION IN VINEYARDS

Matteo Sperti Department of Electronics and Telecommunications Politecnico di Torino Torino, TO, 10129 matteo.sperti@studenti.polito.it

Mauro Martini Department of Electronics and Telecommunications Politecnico di Torino Torino, TO, 10129 mauro.martini@polito.it

Andrea Ostuni Department of Electronics and Telecommunications Politecnico di Torino Torino, TO, 10129 andrea.ostuni@polito.it

Marco Ambrosio Department of Electronics and Telecommunications Politecnico di Torino Torino, TO, 10129 marco.ambrosio@polito.it

Alessandro Navone Department of Electronics and Telecommunications Politecnico di Torino Torino, TO, 10129 alessandro.navone@polito.it

Marcello Chiaberge Department of Electronics and Telecommunications Politecnico di Torino Torino, TO, 10129 marcello.chiaberge@polito.it

April 9, 2024

## ABSTRACT

Autonomous navigation is the foundation of agricultural robots. This paper focuses on develop ing an advanced autonomous navigation system for a rover operating within row-based crops. A position-agnostic system is proposed to address the challenging situation when standard localization methods, like GPS, fail due to unfavorable weather or obstructed signals. This breakthrough is especially vital in densely vegetated regions, including areas covered by thick tree canopies or pergola vineyards. This work proposed a novel system that leverages a single RGB-D camera and a Non-linear Model Predictive Control strategy to navigate through entire rows, adapting to various crop spacing. The presented solution demonstrates versatility in handling diverse crop densities, environmental factors, and multiple navigation tasks to support agricultural activities at an extremely cost-effective implementation. Experimental validation in simulated and real vineyards underscores the system’s robustness and competitiveness in both standard row traversal and target objects approach.

## 1 Introduction

In recent years, precision agriculture has advanced significantly, utilizing technology to optimize crop production and reduce waste [1]. Row-based crops, in particular, represent a pivotal scenario in precision agriculture applications. Research in this domain encompasses various aspects, such as plant health monitoring [2], harvesting [3], spraying [4], irrigation [5], and seeding [6].

This work contributes to the foundation problem of robust autonomous platforms in row-based crops [7, 8], to address all the aforementioned tasks. Standard localization technologies as the Global Navigation Satellite System (GNSS), can fail in this context due to adverse weather or dense vegetation. Moreover, GPS-based solutions are often enhanced by the corrections carried out by multiple costly Real-Time Kinematics (RTK) receivers.

![](Sperti2024Nonlinear_figs/e2645c199b5459004c702c0107e7a8279f76a13aafdb81c1f8ff5c66d89cd566.jpg)  
(a) Straight vineyard

![](Sperti2024Nonlinear_figs/f0dd11e300f5b9f755eaa6c31abcbfc3e9d803595a0acbc7d6e76be9c82130e7.jpg)  
(b) Pergola vineyard  
Figure 1: Vineyards used for testing the proposed navigation system in Agliè, Turin, Italy.

Alternative methods, such as Visual Odometry (VO), have been investigated to localize rovers using camera image streams [9]. However, challenges arise in row-crop fields due to the repetitiveness of environmental visual patterns. A versatile position-agnostic system is therefore proposed, excelling in scenarios where traditional methods fall short. The presented control system can address multiple navigation tasks, such as traversing entire rows, avoiding obstacles effectively, and approaching target objects in varying row spacing. Position-agnostic sensorimotor agents directly map sensor data to rover velocity commands without relying on fixed Reference Frames (RFs). For instance, [10, 11, 12] proposed to segment the input image to compute a set point in the camera frame and to use a proportional controller to align the rover towards the set point. These methods, however, fail in the case of pergola vineyards or high trees in which the sky is not visible [10, 12] or the crops are not uniform on both sides [11], see Fig. 1. Moreover, segmentation-based methods encounter difficulties in generalizing due to visual seasonal changes and in handling unexpected obstacles along the path.

Decision algorithms provide another avenue, with Deep Reinforcement Learning agents trained by [13] for decisionmaking or Convolutional Neural Network (CNN) used by [14] to output actions from a discrete set. Additionally, [15] introduced a path-following Non-linear Model Predictive Control (NMPC) approach, leveraging a Point Cloud Data (PCD) from four cameras to generate the reference path.

The primary contribution of this research lies in developing a new robust controller tailored for row crop geometry, avoiding the need for precise and costly localization systems such as GPS receivers. Notably, a single RGB-D camera represents a cost-effective option compared to other sensors like 3D LIDARs.

Furthermore, the navigation system has been conceived to support task-oriented behavior. This enables the system not only to navigate the agricultural space efficiently but also to engage in auxiliary tasks: approaching target objects in the field, such as boxes or specific plants, or avoiding obstacles, and seamlessly resuming the row traversal process. This flexibility enhances the overall utility of the system and broadens its applicability for diverse agricultural tasks beyond navigation, from object transport to plant harvesting.

![](Sperti2024Nonlinear_figs/639bcc9456e5ef629082966c958fe8162f694fdd4542e711938609815d72d248.jpg)  
Figure 2: Computation Graph of the ROS 2 overall application system. A Behavior Tree manages and coordinates the NMPC controller for row traversal, target object approach, and recovery behaviors for robust multi-task navigation.

The next sections are organized as follows: Section 2 describes the proposed control system for multi-task positionagnostic autonomous navigation in row-based crops. Section 3 illustrates the experiments conducted both in simulated and real vineyards, discussing the obtained results. Finally, Section 4 wraps up all the considerations on the study and suggests future directions.

## 2 Methodology

The proposed methodology adopts a position-agnostic controller approach to guide the robot in row-based crops without relying on a localization signal. Costly GPS sensorization of the platform may lead to unreliable performances in case of thick vegetation. Taking a PCD as input, the controller computes in real-time linear velocity $v _ { x }$ and angular velocity $\omega _ { z }$

## 2.1 Navigation System Architecture

The computation graph, shown in Fig. 2, illustrates the system’s structure. The overall system is orchestrated by a Behavior Tree, overseeing high-level logic, mission switches, start and stop commands, failure detection, and initiating fallback procedures.

The RGB-D camera data is analyzed by two parallel operation flows that carry out standard row traversal and check the presence of potential objects of interest in the mission to be approached. The Point Cloud Analysis process computes two lines that delimit the intra-row space from the PCD, necessary for the main navigation purpose. The NMPC controller uses a Non-linear Model Predictive Control strategy to compute the control sequence given the estimated geometrical constraint of the row. A generic Object Detection visual algorithm could be adopted to estimate the position of potential target objects from the camera image. If any, the Target approach process is triggered to smoothly guide the robot to a desired position near the target. A Fallback Controller manages recovery from fault behaviors: a simple proportional controller is used to re-align the rover with the plants’ row.

## 2.2 Point Cloud processing pipeline

The PCD of the camera is processed to perceive potential obstacles and the boundaries of the crop row. The output of this pipeline includes the array of obstacle points and two straight lines, which represent the geometrical sides of the row.

The first part of the procedure consists of mapping the input PCD to the 2D horizontal plane. Hence, as a first thing, the PCD is transformed into the rover RF. A down-sampling, performing a voxelization operation with a resolution $r _ { v } ,$ , and filtering using a classical k-NN algorithm to exclude the noise points, are applied. Then, the PCD is cropped to eliminate outliers and misleading points in the sky and on the ground. Therefore, minimum and maximum height thresholds, $z _ { t h , m i n } , z _ { t h , m a x }$ on the z-axis are set to ensure the removal of ground points. This operation is necessary in cases where the rover is not perfectly parallel to the ground plane due to bumpy or rough terrain. If, after this preprocessing, the fraction of remaining points, in relation to the original amount, falls below a specified threshold, $f _ { p o i n t s } ,$ the field of view is deemed empty. Consequently, no row is detected. On the other hand, if the fraction exceeds the threshold, the points are projected onto a 2D plane by considering only their coordinates on the x-y plane generating a grid map.

![](Sperti2024Nonlinear_figs/286d46a5caac05222d2122b76b56a53851ef44fa339ac496dbb1d10ad68d4547.jpg)  
Figure 3: The black points represent the input PCD, filtered and flattened on a 2D map (obstacles), the green area is the free space in front of the rover, while the two straight lanes represent the lane borders. Finally, the dotted green line is the expected trajectory as computed by the NMPC controller.

After the generation of the obstacle occupation map, the areas behind them are also considered occupied. This allows us to identify the inner edge of the plants in the row. Then, a heuristic approach is used to gather the occupied zones on the available borders.

Since the two internal row borders are considered two straight lines, a least square fit is applied to evaluate the angular and bias coefficients, $a _ { i } , b _ { i } \in$ <sup>R</sup> of the equation $y = a _ { i } x + b _ { i } , i \in [ l , r ]$ ]. Two lines are generated, one for the left side l and one for the right one r.

Finally, a safety distance margin R is added to the row’s two borders to consider the robot’s occupancy and account for possible errors. Moreover, suppose the rover is required to travel only in half of the available row space, for example in a scenario where multiple robots are expected to move in opposite directions. In that case, the middle line is computed and used to separate the two motion lanes. An error is raised if one of the two lines is (given a predefined maximum angle) perpendicular to the $x { \mathrm { - a x i s , i . e . } }$ , the direction of motion of the rover. Hence, the fallback recovery procedure is initiated to prevent the rover crash and realign it with the row direction.

## 2.3 NMPC formulation

A customized model and cost function were meticulously tailored to address the specific requirements and characteristics of the rover’s navigation scenario. This involved carefully calibrating the model parameters and formulating the cost function terms, as well as the problem constraints. The inputs of the NMPC controller are the points representing the obstacles and the two first-order polynomials representing the two straight lines delimiting the lane, expressed in the robot’s RF (as presented in Section 2.2).

The NMPC approach requires a plant model to predict future states. For this purpose, a modified version of the Unicycle Model was selected. In particular, quaternions are used for the representation of orientation angle. Summarizing, the kinematic model of the unicycle has been modified to:

$$
\left[ \begin{array}{c} \dot {x _ {1}} \\ \dot {x _ {2}} \\ \dot {x _ {3}} \\ \dot {x _ {4}} \end{array} \right] = \left[ \begin{array}{c} v (x _ {3} ^ {2} - x _ {4} ^ {2}) \\ v (2 x _ {3} x _ {4}) \\ - \omega \frac {x _ {4}}{2} \\ \omega \frac {x _ {3}}{2} \end{array} \right]\tag{1}
$$

where $\begin{array} { r } { x _ { 1 } = x , x _ { 2 } = y , x _ { 3 } = \cos \frac { \theta } { 2 } , x _ { 4 } = \sin \frac { \theta } { 2 } . } \end{array}$

Moreover, input saturation constraints were incorporated into the NMPC minimization problem, allowing for the specification of maximum linear and angular velocities, namely $v _ { x , m a x }$ and $\omega _ { z , m a x }$ , as parameters before the system’s initiation.

In addition, non-linear constraints were integrated to ensure obstacle avoidance, according to the following formula:

$$
- (x _ {1} - o _ {1} ^ {i}) ^ {2} - (x _ {2} - o _ {2} ^ {i}) ^ {2} + R ^ {2} \leq 0\tag{2}
$$

where the two negative terms represent the square of the Euclidean distance between the rover pose x and the i-th obstacle $\mathbf { o } ^ { i }$ , and the parameter R represents a predetermined safe distance between the rover and an obstacle point. This constraint must hold for each time step $t _ { k } = 1 , \dots , T _ { H }$ and for every obstacle point, providing a robust mechanism for obstacle avoidance throughout the prediction horizon.

The core of the NMPC formulation lies in defining an objective function, which needs to be optimized, represented as follows:

$$
C = \sum_ {k = 0} ^ {n - 1} (\underbrace {l \left(\mathbf {x} _ {k} , \mathbf {u} _ {k} , p\right)} _ {\text { Lagrange   term }} + \underbrace {\Delta \mathbf {u} _ {k} ^ {T} \mathbf {R} \Delta \mathbf {u} _ {k}} _ {\text { r - term }}) + \underbrace {m \left(\mathbf {x} _ {n}\right)} _ {\text { meyer   term }}\tag{3}
$$

In this equation, three contributions can be identified, respectively the Lagrange term, the meyer term, and the r-term. The Lagrange term, $l \left( \mathbf { x } _ { k } , \mathbf { u } _ { k } , p \right)$ , evaluated and summed at each time step until the prediction horizon, is composed of two contributions as in the following equation:

$$
l \left(\mathbf {x} _ {k}, \mathbf {u} _ {k}, p\right) = K _ {l a n e} C _ {l a n e} \left(\mathbf {x} _ {k}, \mathbf {u} _ {k}, p\right) + K _ {o r i e n t} C _ {a l i g n} \left(\mathbf {x} _ {k}, \mathbf {u} _ {k}, p\right)\tag{4}
$$

The first term, $C _ { l a n e } \left( \mathbf { x } _ { k } , \mathbf { u } _ { k } , p \right)$ , aims at maintaining a central trajectory with respect to the lane while, the second term, $C _ { a l i g n } \left( \mathbf { x } _ { k } , \mathbf { u } _ { k } , p \right)$ , aims at minimizing misalignment from the row direction. The constants $K _ { l a n e }$ and $K _ { o r i e n t }$ are the weights of the corresponding contributions.

Given a position $\mathbf { x } = [ x _ { 1 } , x _ { 2 } , x _ { 3 } , x _ { 4 } ]$ , and the two lines delimiting the row $y _ { l } = a _ { l } x _ { 1 } + b _ { l }$ (on the left), and $y _ { r } =$ $a _ { r } x _ { 1 } + b _ { \eta }$ <sub>r</sub> (on the right), the cost term regarding the lane centrality is described by the following equation:

$$
C _ {l a n e} = \frac {4}{(y _ {l} - y _ {r}) ^ {2}} x _ {2} ^ {2} - 4 \frac {(y _ {l} + y _ {r})}{(y _ {l} - y _ {r}) ^ {2}} x _ {2} + \frac {(y _ {l} + y _ {r}) ^ {2}}{(y _ {l} - y _ {r}) ^ {2}}\tag{5}
$$

Essentially, it consists of a paraboloid with its minimum coinciding with the middle of the row. For each depth value $x _ { 1 }$ a convex-upward parabola is constructed along the axis $x _ { 2 }$ with a minimum in the middle of the lane. Therefore, the minimum cost trajectory ideally aligns perfectly with it.

The cost term for the alignment is computed considering the difference between the angular coefficient of the middle line $a _ { a v g } = ( a _ { l } + a _ { r } ) / 2$ and the angular coefficient of a straight line oriented as the rover $a _ { r o v e r }$ as in the following equation:

$$
a _ {r o v e r} = \tan \theta = \frac {\sin \theta}{\cos \theta} = \frac {2 x _ {3} x _ {4}}{x _ {3} ^ {2} - x _ {4} ^ {2}}\tag{6}
$$

$$
C _ {a l i g n} = (a _ {a v g} - a _ {r o v e r}) ^ {2}\tag{7}
$$

The r-term is the quadratic penalty on changes for control inputs, which can be utilized to smooth the obtained optimal solution and serve as a crucial tuning parameter.

![](Sperti2024Nonlinear_figs/ab4cfae5a012fe3b7e62e087cbeb85226b5a597a6e46484c7747d30e8af08a61.jpg)  
Figure 4: Aerial view of vineyards in Gazebo used for testing in simulation.

The terminal (or meyer) term of the objective function is designed to maximize the distance traveled by the rover in the prediction horizon time interval. So, recalling that max $f = \operatorname* { m i n } - f ,$ the terminal (or meyer) term is set as follows:

$$
m (\mathbf {x}) = - K _ {t r a v e l} \frac {x _ {1} + a _ {a v g} \cdot x _ {2}}{\sqrt {1 + a _ {a v g} ^ {2}}}\tag{8}
$$

here $K _ { t r a v e l }$ represents the parameter for weighting this term, $a _ { a v g } = ( a _ { l } + a _ { r } ) / 2$ is the angular coefficient of the line in the middle of the row, and $x _ { 1 } , x _ { 2 }$ are the coordinates of the rover in plane at the horizon $t _ { k } = T _ { H }$ . The distance traveled by the rover is projected onto the middle line to weigh only the distance traveled in the direction of the row.

## 3 Tests and Results

For testing and validation, extensive experiments were conducted on both simulated and real vineyards to illustrate the competitive advantages of the proposed solution.

## 3.1 Experimental Setting

All the code was developed in a ROS 2 framework and has been tested on Ubuntu 22.04 LTS using the ROS 2 Humble distro. This research employed two distinct mobile robots: the Clearpath Robotics Jackal and Husky<sup>1</sup>. The first is a compact robot designed for indoor and outdoor robotics applications, while the second is a much bigger and more powerful platform. For simulated tests, the Gazebo platform, the Jackal model and description, and the PIC4rl\_gym [16] evaluation tool were utilized. The world chosen, shown in Fig. 4, contains a straight and curved vineyard, with an intra-row space of around 1.5 m.

Instead, tests in a real vineyard utilized the Jackal to verify the target approach feature and the Husky to evaluate the path metrics, an Intel Realsense D455 RGB-D camera, and a Velodyne VLP16 3D LIDAR for comparison. The tests were conducted on a straight vineyard with an intra-row space of around 2.5 m and on a pergola vineyard with an intra-row space of around 4 $m ,$ both shown in Fig. 1.

An accurate robot localization in the row was necessary for comparing its position to a ground truth path. However, the odometry system of the IMU of the rover failed to localize the rover due to significant drifts; SLAM techniques based on scan matching algorithms such as KISS-ICP [17], also failed to correctly localize the system due to the repetitiveness of the environment. ${ \mathrm { S o } } ,$ the GPS position provided by the SwiftNav Duro GNSS receiver was used as a reference to compute the metrics, along with a precise geo-localization of the row in the vineyards (Fig. 5). However, GPS positioning is prone to errors in environments where leaves obstruct GPS visibility, leading to signal failures and inaccuracies in position tracking. Moreover, costs must also be considered: the GNSS receiver chosen to obtain a sufficiently precise localization is much more expensive than an RGB-D camera. These facts highlight the difficulties in localizing a ground rover in this environment and suggest the advantages of adopting a position-agnostic controller such as the one developed in this project. RGB-D cameras are also a cost-effective choice to get a limited FOV PCD, compared to a multi-range 3D LIDAR.

For the tests, $v _ { x , m a x } = 0 . 4 ~ m / s$ or $v _ { x , m a x } = 0 . 5 ~ m / s$ s and $\omega _ { z , m a x } = 0 . 5$ rad/s has been set. The control period has been fixed to 0.7 s. In the PCD processing pipeline, the resolution of the voxel has been set to $r _ { v } = 0 . 0 5 m$ , the minimum and maximum height threshold have been set to $z _ { t h , m i n } = 0 . 1 5$ m and $z _ { t h , m a x } = 2$ m and the minimum point threshold has been set to $f _ { p o i n t s } = 0 . 2$ . The safety margins, for the Jackal and the Husky robots, were respectively set to $R _ { J a c k a l } = 0 . 3$ m and $R _ { H u s k y } = 0 . 4 m$

![](Sperti2024Nonlinear_figs/4b74c85d5ae193b7cea8bb24a9f5d813eb7a7f0f584c0b3e0b122f7f0fdaa90c.jpg)  
Figure 5: Satellite view of the vineyard. In red the trajectory followed by the Husky rover during a test session.

To implement the NMPC controller, the DO-MPC library [18] was chosen for its versatility. The hyper-parameters of the NMPC controller have been set by a trial and error procedure.

## 3.2 Evaluation Metrics

The metrics used to evaluate the performances of the control system include:

• Clearance Time [s] and Mean linear velocity $v _ { a v g } [ \mathrm { m } / \mathrm { s } ] ;$ gauging the effectiveness of the proposed solution.

• Cumulative heading average $C u m . \gamma _ { a v g }$ or standard deviation of the heading $\gamma _ { s t d }$ [rad], and the standard deviation of the angular velocity $\omega _ { s t d }$ [rad/s]: measuring the oscillation around the trajectory.

• Trajectory Mean Absolute Error (MAE) [m] and trajectory Mean Squared Error $\left( M S E \right) [ \mathrm { m } ^ { 2 } ]$ : measuring the error of the rover trajectory concerning a predefined ground truth, such as the center of the row or the center of the lane.

## 3.3 Tests in simulated environment

The extensive simulations conducted in simulated vineyard environments have demonstrated the reliability and robustness of the proposed navigation system. As illustrated in Fig. 6, the rover’s trajectory closely aligns with the desired central path, exhibiting minimal oscillations in both straight and curved vineyards.

Detailed results are provided in Tab. 1, revealing several key performance indicators. In both straight and curved vineyards, the rover consistently achieves speeds close to the maximum limit $( v _ { a v g } \simeq 0 . 3 9 m / s$ for $v _ { x , m a x } = 0 . 4 m / s )$ resulting in effective clearance times. The rover’s trajectory shows minimal oscillations, as indicated by a small standard deviation of angular velocity $( \omega _ { s t d } \simeq 0 . 0 5 r a d / s )$ , reflecting stable and smooth behavior. Path metrics, including MAE and MSE, are minimal, on the order of centimeters. This demonstrates the rover’s precise adherence to the center of its lane. In the curved vineyard, a slightly larger path error is observed (MAE up to 0.2 m in the worst case), attributed to the controller’s inclination to cut curves. This behavior can be mitigated through parameter tuning. The algorithm’s consistent performance across input sensors, including RGB-D cameras, highlights its reliability and versatility. This robustness, even compared to more expensive technologies such as LIDAR, underscores the algorithm’s adaptability to various sensor configurations. The ability to achieve comparable results with RGB-D cameras suggests a cost-effective alternative for applications where LIDAR may be cost-prohibitive. Overall, these findings underscore the effectiveness and versatility of the proposed navigation system across diverse vineyard scenarios.

![](Sperti2024Nonlinear_figs/d29a66359bf837bc39f7a1c314e21dae5bf2362c7cff3591703a2932fd572928.jpg)

![](Sperti2024Nonlinear_figs/c04a361593ccdc025c390fbafb9088307d9c2c7dd258eb40a9a66598870aba1a.jpg)  
Figure 6: Tests in a simulated vineyard using the PCD of the camera as input in two different scenarios.

Table 1: Results of conducted experiments in simulated straight and curved vineyards.

<table><tr><td>Field</td><td>Sensor</td><td>Clearance time [s]</td><td>Cum.  $\gamma_{avg}$  [rad]</td><td> $v_{avg}$  [m/s]</td><td> $\omega_{std}$  [rad/s]</td><td>MAE [m]</td><td>MSE [m2]</td></tr><tr><td rowspan="3">Straight</td><td>LIDAR</td><td>49.528±0.167</td><td>0.036±0.001</td><td>0.395±0.002</td><td>0.034±0.001</td><td>0.034±0.001</td><td>0.001±0.000</td></tr><tr><td>PCD cam</td><td>52.586±4.130</td><td>0.045±0.001</td><td>0.377±0.019</td><td>0.038±0.001</td><td>0.048±0.005</td><td>0.003±0.001</td></tr><tr><td>RGB-D cam</td><td>49.321±0.356</td><td>0.011±0.005</td><td>0.395±0.001</td><td>0.046±0.004</td><td>0.104±0.011</td><td>0.018±0.004</td></tr><tr><td rowspan="3">Curved</td><td>LIDAR</td><td>52.080±0.220</td><td>-0.024±0.001</td><td>0.397±0.001</td><td>0.036±0.001</td><td>0.102±0.001</td><td>0.015±0.000</td></tr><tr><td>PCD cam</td><td>52.157±0.673</td><td>0.002±0.002</td><td>0.393±0.002</td><td>0.041±0.003</td><td>0.068±0.004</td><td>0.007±0.001</td></tr><tr><td>RGB-D cam</td><td>51.763±0.228</td><td>-0.011±0.002</td><td>0.394±0.001</td><td>0.056±0.007</td><td>0.188±0.005</td><td>0.051±0.003</td></tr></table>

## 3.4 Tests in real scenario

The real-world tests conducted in vineyards have validated the results obtained in the simulated environment. Detailed results are presented in Tab. 2, highlighting the robust performance of the controller in real scenarios. As in simulation, the rover consistently achieves speeds close to the maximum limit $( v _ { a v g } \simeq 0 . 3 9 9 m / s$ for $v _ { x , m a x } = 0 . 4 \ : m / s$ and $v _ { a v g } \simeq 0 . 4 9 m / s$ for $v _ { x , m a x } = 0 . 5 m / s )$ . The achieved trajectory shows minimal oscillations, as indicated by a small standard deviation of angular velocity $( \omega _ { s t d } \simeq 0 . 0 5 r a d / s )$ , reflecting stable and smooth behavior. The exception is the narrow straight vineyard in the right lane configuration, where this metric is slightly larger $( \omega _ { s t d } \simeq 0 . 1 8 \ : r a d / s ) \colon$ the rover displays a more oscillatory behavior, likely due to the proximity of the right lane to the crops. This behavior is less prominent in the pergola vineyard test (Fig. 7) with a larger intra-row distance (4 m), where the rover shows a smooth convergence to the right lane without significant oscillations. Path metrics, including MAE and MSE, are minimal, on the order of centimeters (up to 20 cm for the narrow vineyard and up to 30 cm for the larger pergola vineyard). However, it’s important to consider the error in the reference trajectory, as well as the error of localization, affected by the intrinsic accuracy of the sensor used when interpreting these results.

![](Sperti2024Nonlinear_figs/bf4ac573c09f8027d0677902eb3c715c4bf90fffaf4bea7ab1d3454501210a59.jpg)  
Figure 7: Test in a real pergola vineyard using the PCD of the camera as input. The desired position is in the middle of the right lane (so at 3/4 of the entire intra-row space). The rover starts in the middle of the row and then converges smoothly to the desired position.

Table 2: Results of a series of experiments in real vineyards.

<table><tr><td>Field</td><td>Sensor</td><td>Position</td><td> $v_{x,max}$  [m/s]</td><td> $\gamma_{std}$  [rad]</td><td> $v_{avg}$  [m/s]</td><td> $\omega_{std}$  [rad/s]</td><td>MAE [m]</td><td>MSE [m2]</td></tr><tr><td rowspan="3">Straight</td><td rowspan="2">PCD camera</td><td>Centered</td><td>0.4</td><td>0.031±0.007</td><td>0.399±0.000</td><td>0.042±0.002</td><td>0.165±0.007</td><td>0.035±0.000</td></tr><tr><td>Right lane</td><td>0.5</td><td>0.388±0.395</td><td>0.488±0.007</td><td>0.184±0.108</td><td>0.204±0.098</td><td>0.070±0.044</td></tr><tr><td>LIDAR</td><td>Right lane</td><td>0.5</td><td>0.0153</td><td>0.4989</td><td>0.0271</td><td>0.1519</td><td>0.0294</td></tr><tr><td rowspan="2">Pergola</td><td rowspan="2">PCD camera</td><td>Centered</td><td>0.4</td><td>0.122</td><td>0.399</td><td>0.063</td><td>0.313</td><td>0.129</td></tr><tr><td>Right lane</td><td>0.4</td><td>0.047</td><td>0.399</td><td>0.04</td><td>0.092</td><td>0.011</td></tr></table>

Moreover, using a simple recognition system for fruit boxes, the smaller robot achieved to approach the desired object of interest without any collision.

## 4 Conclusions

The position-agnostic NMPC controller proposed in this paper has demonstrated robustness in effectively handling the diverse challenges presented in traversing row-based fields with different characteristics without accessing any localization information. Its resilient navigation on rough terrains underscores its adaptability to real-world agricultural conditions with a lower platform cost. This research significantly contributes to the continuous advancement of precision agriculture and the evolution of autonomous navigation systems tailored for row-based crop environments.

## Acknowledgements

This work has been developed with the contribution of Politecnico di Torino Interdepartmental Center for Service Robotics PIC4SeR <sup>2</sup>.

## References

[1] Zhaoyu Zhai, José Fernán Martínez, Victoria Beltran, and Néstor Lucas Martínez. Decision support systems for agriculture 4.0: Survey and challenges. Computers and Electronics in Agriculture, 170:105256, 2020.

[2] Nicolas Virlet, Kasra Sabermanesh, Pouria Sadeghi-Tehran, and Malcolm J Hawkesford. Field scanalyzer: an automated robotic field phenotyping platform for detailed crop monitoring. Functional Plant Biology, 44(1):143– 153, 2017.

[3] Weikuan Jia, Yan Zhang, Jian Lian, Yuanjie Zheng, Dean Zhao, and Chengjiang Li. Apple harvesting robot under information technology: A review. International Journal of Advanced Robotic Systems, 17(3):1729881420925310, 2020.

[4] Ron Berenstein, Ohad Ben Shahar, Amir Shapiro, and Yael Edan. Grape clusters and foliage detection algorithms for autonomous selective vineyard sprayer. Intelligent Service Robotics, 3(4):233–243, 2010.

[5] David Kohanbash, Abhinav Valada, and George Kantor. Irrigation control methods for wireless sensor network. In 2012 Dallas, Texas, July 29-August 1, 2012, page 1. American Society of Agricultural and Biological Engineers, 2012.

[6] Jayantha Katupitiya, Ray Eaton, and Tahir Yaqub. Systems engineering approach to agricultural automation: new developments. In 2007 1st Annual IEEE Systems Conference, pages 1–7. IEEE, 2007.

[7] Simone Cerrato, Vittorio Mazzia, Francesco Salvetti, and Marcello Chiaberge. A deep learning driven algorithmic pipeline for autonomous navigation in row-based crops. arXiv preprint arXiv:2112.03816, 2021.

[8] Francesco Salvetti, Simone Angarano, Mauro Martini, Simone Cerrato, and Marcello Chiaberge. Waypoint generation in row-based crops with deep learning and contrastive clustering. In Joint European Conference on Machine Learning and Knowledge Discovery in Databases, pages 203–218. Springer, 2022.

[9] Shahzad Zaman, Lorenzo Comba, Alessandro Biglia, Davide Ricauda Aimonino, Paolo Barge, and Paolo Gay. Cost-effective visual odometry system for vehicle motion control in agricultural environments. Computers and Electronics in Agriculture, 162:82–94, 2019.

[10] Diego Aghi, Simone Cerrato, Vittorio Mazzia, and Marcello Chiaberge. Deep Semantic Segmentation at the Edge for Autonomous Navigation in Vineyard Rows. In 2021 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS). IEEE, September 2021.

[11] Alessandro Navone, Mauro Martini, Andrea Ostuni, Simone Angarano, and Marcello Chiaberge. Autonomous navigation in rows of trees and high crops with deep semantic segmentation. In 2023 European Conference on Mobile Robots (ECMR), pages 1–6, 2023.

[12] Josiah Radcliffe, Julie Cox, and Duke M. Bulanon. Machine vision for orchard navigation. Computers in Industry, 98:165–171, 2018.

[13] Mauro Martini, Simone Cerrato, Francesco Salvetti, Simone Angarano, and Marcello Chiaberge. Position- Agnostic Autonomous Navigation in Vineyards with Deep Reinforcement Learning. In 2022 IEEE 18th International Conference on Automation Science and Engineering (CASE). IEEE, 08 2022.

[14] Peichen Huang, Lixue Zhu, Zhigang Zhang, and Chenyu Yang. An End-to-End Learning-Based Row- Following System for an Agricultural Robot in Structured Apple Orchards. Mathe- matical Problems in Engineering, 2021:1–14, 09 2021.

[15] A Villemazet, A Durand-Petiteville, and V Cadenat. Multi-Camera GPS-Free Nonlinear Model Predictive Control Strategy to Traverse Orchards. In 2023 European Conference on Mobile Robots (ECMR), pages 1–7. IEEE, 2023.

[16] Mauro Martini, Andrea Eirale, Simone Cerrato, and Marcello Chiaberge. Pic4rl-gym: a ros2 modular framework for robots autonomous navigation with deep reinforcement learning. In 2023 3rd International Conference on Computer, Control and Robotics (ICCCR), pages 198–202, 2023.

[17] Ignacio Vizzo, Tiziano Guadagnino, Benedikt Mersch, Louis Wiesmann, Jens Behley, and Cyrill Stachniss. KISS-ICP: In Defense of Point-to-Point ICP – Simple, Accurate, and Robust Registration If Done the Right Way. IEEE Robotics and Automation Letters, 8(2):1029–1036, 2023.

[18] Felix Fiedler, Benjamin Karg, Lukas Lüken, Dean Brandner, Moritz Heinlein, Felix Brabender, and Sergio Lucia. do-mpc: Towards FAIR nonlinear and robust model predictive control. Control Engineering Practice, 140:105676, 2023.