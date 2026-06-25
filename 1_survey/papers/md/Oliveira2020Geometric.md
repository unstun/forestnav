---
citation_key: Oliveira2020Geometric
arxiv_id: 2010.07133
arxiv_url: "https://arxiv.org/abs/2010.07133"
title: "A Geometric Approach to On-road Motion Planning for Long and Multi-Body Heavy-Duty Vehicles"
authors_short: "Rui Oliveira et al."
year: 2020
direction_tag: O_dense_forest_narrow_passage
source: mineru-vlm
converter: mineru-open-api
model: vlm
converted_at: 2026-06-25T09:47:35Z
origin: ai+web
reviewed: false
---

# <sub>A</sub> <sub>G</sub>eometric <sub>A</sub>pproach to <sub>O</sub>n<sub>-</sub>road <sub>M</sub>otion <sub>P</sub>lanning for <sub>L</sub>ong and <sub>M</sub>ulti<sub>-B</sub>ody <sub>H</sub>eavy<sub>-D</sub>uty <sub>V</sub>ehicles

Rui Oliveira<sup>1 3</sup>, Oskar Ljungqvist<sup>2</sup>, Pedro F. Lima<sup>3</sup>, Jonas Mårtensson<sup>1</sup>, and Bo Wahlberg<sup>1</sup>

## <sub>A</sub>bstract

Driving heavy-duty vehicles, such as buses and tractor-trailer vehicles, is a dificult task in comparison to passenger cars. Most research on motion planning for autonomous vehicles has focused on passenger vehicles, and many unique challenges associated with heavy-duty vehicles remain open. However, recent works have started to tackle the particular dificulties related to on-road motion planning for buses and tractor-trailer vehicles using numerical optimization approaches. In this work, we propose a framework to design an optimization objective to be used in motion planners. Based on geometric derivations, the method finds the optimal trade-of between the conflicting objectives of centering diferent axles of the vehicle in the lane. For the buses, we consider the front and rear axles trade-of, whereas for articulated vehicles, we consider the tractor and trailer rear axles trade-of. Our results show that the proposed design strategy results in planned paths that considerably improve the behavior of heavy-duty vehicles by keeping the whole vehicle body in the center of the lane.

## <sub>1</sub> <sub>I</sub>ntroduction

Driving heavy-duty vehicles is a dificult task that requires expertise and special driver education. The additional dificulties experienced by drivers when controlling these vehicles translate into further challenges for autonomous driving systems to tackle. Even though motion planning for autonomous vehicles has been the subject of extensive research eforts, most of its focus has been on passenger cars [1, 2]. As a result, fundamental problems that afect buses and articulated vehicles, but not passenger cars, have been left unanswered.

The long dimensions of buses are a major challenge for traditional motion planning frameworks. To be able to plan for such vehicles the work in [3] introduces a new environment classification scheme, as well as the formulation of new optimization objectives. Nevertheless, the planned paths still result in the bus driving unnecessarily close to the road boundaries.

In the tractor-trailer case, the presence of multiple vehicle bodies requires that both bodies are centered simultaneously. This conflicting objective introduces a trade-of that weighs the importance of centering the tractor, against the importance of centering the trailer. To tune this parameter, the work in [4] requires ofline time-consuming computations that do not generalize for all vehicle and road combinations.

In this work, we extend the framework developed in [4] by deriving, via geometric arguments, the optimal weighting parameter, i.e., the optimal tradeof between tractor centering and trailer centering. The derived parameter can then be used in the numerical optimization formulation, resulting in planned solutions that are optimal according to performance metrics measuring the area swept by the vehicle. Analogously, we derive an optimal weighting parameter for the bus case, this time, corresponding to the optimal tradeof between rear axle centering and front axle centering. Using the derived optimal weighting parameter leads to improvements upon the results obtained in [3].

![](Oliveira2020Geometric_figs/cde507cb65b76c1c93589284fd1c856b3b4d99181408e176d4794800de3bda4d.jpg)

![](Oliveira2020Geometric_figs/e5e08ae7287b1f3bca204f5b2d4367cfe093b5f2bca9d859848a0bdd31ff7412.jpg)  
Figure 1: A bus (left), with a considerable vehicle length, and a tractor-trailer (right), consisting of two vehicle bodies, are examples of heavy-duty vehicles studied in this work. The long vehicle dimensions, or the presence of multiple vehicle bodies, introduce novel challenges covered in this work. (courtesy of Scania CV)

Summarizing, the contributions of this work are:

• Geometric derivation of optimal driving objectives, with respect to the area swept by the vehicles, suitable for online computation;

• Development of a unified framework targeting both long vehicles, such as buses, as well as multi-body vehicles, such as tractor-trailers;

• Comparison with recent works on the same topic [3,4], showing significant performance improvements.

The remainder of this paper is structured as follows: Section 2 sumarizes related work on the motion planning topic. Section 3 introduces the vehicle models of the bus and the tractor-trailer, and formulates the motion planning problem as a numerical optimization problem. Section 4 presents the geometrical derivation of the driving objectives to be used in the numerical optimization. Section 5 presents relevant simulation results and shows the benefits of the proposed approach when compared to previous methods. We give final remarks and propose directions for future work in Section 6.

## <sub>2</sub> <sub>R</sub>elated <sub>W</sub>ork

The motion planning problem has been the subject of intensive research in the field of robotics. In order to deal with complex vehicle dynamics [5] proposes Rapidly-exploring Random Trees. The work in [6] proposes instead a special discretization of the search space that is compliant with the vehicle motion capabilities. Despite good performance when considering unstructured driving environments, these algorithms require specific adaptations to make them suitable for on-road driving [7, 8].

In recent years, numerical optimization has emerged as a promising approach to motion planning and control [9–13], due to the broader availability of numerical solvers [14, 15], as well as increasing computational power available in automotive components. Numerical optimization approaches benefit from structured driving environments, such as on-road scenarios, and can outperform other existing methods in terms of smoothness and optimality [12].

Research in motion planning for heavy-duty vehicles have mostly considered of-road scenarios [16–18], semi-structured scenarios [19], or roads with low curvature [20], leaving the challenges of on-road driving opened. However, recently proposed works [3, 4] study the specific problems of heavy-duty vehicles driving on urban roads.

In [3], the authors study the motion planning problem for buses and identify shortcomings in current motion planning frameworks. A new environment classification scheme together with a new formulation of optimization objectives, increase the maneuverability and safety of buses driving in urban scenarios. However, the approach only penalizes if the vehicle exits the road boundaries, and therefore planned paths often result in the bus driving on the border of the road boundaries.

The work in [4] focuses on articulated vehicles and on the problem of how to best drive multi-body vehicles, where centering both vehicle bodies at the same time is a conflicting objective. The authors propose an optimization objective that is a compromise between the minimization of the area swept by the vehicle, and the feasibility of online computations. However, the optimization objective includes a tuning parameter used to tradeof between centering the tractor and the trailer on the road. To achieve the best performance, this parameter has to be properly tuned which can be a time-consuming process.

This paper improves upon the works [3, 4] by introducing a unified framework targeted for buses and tractor-trailer vehicles. Our proposed framework improves the driving behavior of buses, by centering their whole body on the lane, thus avoiding the problem of driving too close to road boundaries, as seen in [3]. Moreover, the proposed framework provides a geometric way of computing the tuning parameter presented in [4], allowing it to be adapted online to the current road the vehicle is driving in.

## <sub>3</sub> <sub>M</sub>otion <sub>P</sub>lanning <sub>F</sub>ramework

This section presents the proposed on-road path planning framework. First, the vehicle models for the bus and the tractortrailer are introduced. We then formulate the on-road path planning problem as an optimal control problem.

![](Oliveira2020Geometric_figs/45c87594f64ba60c82385358fbd6460ec50e71987876afececae282e314c7ff6.jpg)  
Figure 2: An illustration of the bus in the road-aligned frame and definitions of relevant geometric lengths and vehicle states.

## 3.1 Road-aligned bus model

The vehicles are modeled in a road-aligned frame, which describes the evolution of the vehicles’ states in terms of deviation from, and progression along, a geometric reference path (·). The reference path is parametrized in s which corresponds <sup>γ</sup>to the distance traveled along the path, and the shape of the path is characterized by a bounded and continuous curvature $\kappa _ { \gamma } ( s )$ <sup>κγ</sup>In this work, the reference path (·) represents the center of the <sup>γ</sup>vehicle’s drive lane, but could also be computed by a global path planner.

The bus in the road-aligned coordinate frame is schematically illustrated in Fig. 2. The wheelbase of the bus is denoted by $L _ { 1 }$ and its width by W, whereas $L _ { 1 } ^ { r }$ and $L _ { 1 } ^ { f }$ denote the lengths of the bus rear and front overhangs. The vehicle state s represents the distance traveled by the rear axle of the bus along the reference path $\gamma ,$ whereas $e _ { y }$ is lateral displacement of the bus rear axle <sup>γ</sup>with respect to the reference path and $e _ { \psi }$ is the orientation error <sup>ψ</sup>of the bus with respect to the reference path’s tangent.

The vehicle model is given by [21]:

$$
\begin{array}{c} \dot {s} = v \frac {\cos (e _ {\psi})}{1 - e _ {y} \kappa_ {\gamma} (s)}, \\ \dot {e} _ {y} = v \sin (e _ {\psi}), \\ \dot {e} _ {\psi} = v \left(\kappa - \frac {\kappa_ {\gamma} (s) \cos (e _ {\psi})}{1 - e _ {y} \kappa_ {\gamma} (s)}\right), \end{array}\tag{1}
$$

where $\dot { ( \cdot ) } = \mathrm { d } ( \cdot ) / \mathrm { d }$ t and the control input is curvature of the bus. <sup>/ κ</sup>The relationship between the steering angle of the bus $\phi$ and its curvature is $\kappa = { \tan ( \phi ) } / { L }$ <sub>1</sub>.

By restricting the attention to forward motion $\nu > 0$ and employing time scaling with $\dot { s } > 0 .$ <sup>></sup>, the temporal model of Eq. (1) can be converted to an equivalent spatial model [21]:

$$
\begin{array}{l} {e _ {y} ^ {\prime} = (1 - e _ {y} \kappa_ {\gamma}) \tan (e _ {\psi}),} \\ {e _ {\psi} ^ {\prime} = \frac {1 - e _ {y} \kappa_ {\gamma}}{\cos (e _ {\psi})} \kappa - \kappa_ {\gamma},} \end{array}\tag{2}
$$

where $( \cdot ) ^ { \prime } = \mathbf { d } ( \cdot ) \big / \mathbf { d } s$

Equation (2) describes the behavior of the lateral and orientation error of the bus rear axle. However, it does not contain information of the lateral error of the bus front axle $e _ { v } ^ { b u s }$ with respect to the reference path $\gamma ( \cdot )$ . To center the whole vehicle <sup>γ</sup>body around the reference path, it is desired to represent this auxiliary state $e _ { y } ^ { b u s }$ as a function of $[ e _ { y } \ e _ { \psi } ] ^ { T }$ . Except for the case of a straight nominal path, this relationship cannot be written in a purely algebraic form, as it involves a line integral [22].

In order to be able to consider the lateral error of the bus front axle $e _ { y } ^ { b u s }$ , we introduce its approximation $\hat { e } _ { \mathrm { v } } ^ { b u s }$ . Similar to [4], it is possible to numerically compute an approximate relationship of $\hat { \mathbf { \rho } } _ { e _ { y } } ^ { b u s }$ which depends linearly on the states $[ e _ { y } \ e _ { \psi } ] ^ { T }$ . Given a linearization point $[ \bar { s } \bar { e } _ { y } \bar { e } _ { \psi } ] ^ { T }$ , using finite diferences and by <sup>ψ</sup>iteratively projecting the bus front axle to the reference path, it is possible to compute a linear model for the lateral error of the bus front axle $e _ { y } ^ { b u s }$ as a function of $[ e _ { y } \ e _ { \psi } ] ^ { T }$ that is given by

$$
\hat {e} _ {y} ^ {b u s} = \bar {e} _ {y} ^ {b u s} + \frac {\partial e _ {y} ^ {b u s}}{\partial e _ {y}} (e _ {y} - \bar {e} _ {y}) + \frac {\partial e _ {y} ^ {b u s}}{\partial e _ {\psi}} (e _ {\psi} - \bar {e} _ {\psi}),\tag{3}
$$

where the partial derivatives $\frac { \partial e _ { y } ^ { b u s } } { \partial e _ { v } }$ and $\frac { \partial e _ { y } ^ { b u s } } { \partial e _ { \psi } }$ are computed numerically (see [4] for details).

As in [3], the spatial model is discretized to make it suitable for numerical optimization purposes. Given a path sampling distance $\Delta s ,$ the reference path is discretized along its length resulting in $\stackrel { \cdot } { \{ s _ { i } \} } _ { i = 0 } ^ { N }$ and $\{ \kappa _ { \gamma } ( s _ { i } ) \} _ { i = 0 } ^ { N } ,$ , where $s _ { i } = i \Delta s$ . By defining the state vector for the bus as $z _ { b u s } = [ e _ { y } ~ e _ { \psi } ~ e _ { y } ^ { b u s } ] ^ { T }$ and using <sup>ψ</sup>Euler-forward discretization, a discrete-time nonlinear model of Eq. (2) and Eq. (3) is obtained which can be represented compactly as

$$
z _ {b u s, i + 1} = f _ {b u s} (z _ {b u s, i}, \kappa_ {i}).\tag{4}
$$

## 3.2 Road-aligned tractor-trailer model

The tractor-trailer vehicle in the road-aligned coordinate frame is illustrated in Fig. 3. The geometric lengths for the tractor are defined analogously to the bus case and its kinematics modeled accordingly. The length $L _ { 2 }$ is the distance between the trailer’s axle and the hitch connection at the tractor, $L _ { \gamma } ^ { r }$ is the trailer’s rear overhang, and $M _ { 1 }$ is the signed hitching ofset at the tractor. This hitching ofset is negative if the hitch connecting is in front of the tractor’s rear axle and positive otherwise. To model the tractor-trailer vehicle’s kinematics, one needs to additionally consider state $\beta _ { 1 }$ , the joint angle between the tractor and the trailer. Its temporal model is given by [16]:

$$
\dot {\beta_ {1}} = v \left(\kappa - \frac {\sin (\beta_ {1})}{L _ {2}} + \frac {M _ {1}}{L _ {2}} \cos (\beta_ {1}) \kappa\right),\tag{5}
$$

and as in Eq. (2), the equivalent spatial model is

$$
\beta_ {1} ^ {\prime} = \frac {1 - e _ {y} \kappa_ {\gamma}}{\cos (e _ {\psi})} \left(\kappa - \frac {\sin (\beta_ {1})}{L _ {2}} + \frac {M _ {1}}{L _ {2}} \cos (\beta_ {1}) \kappa\right).\tag{6}
$$

Similarly to the bus case,the models in Eq. (2) and Eq. (6) only provide information about the axle of the tractor, and as such, there is no explicit information regarding the axle of the trailer’s lateral error $\bar { e } _ { y } ^ { t t }$ with respect to the reference path $\gamma ( \cdot )$ . As no closed-form expression exists to express $e _ { y } ^ { t t }$ as a function of $[ e _ { y } \ e _ { \psi } \ \beta _ { 1 } ] ^ { T }$ for paths with nonzero curvature, we compute an <sup>ψ β</sup>approximation $\hat { e } _ { v } ^ { \bar { t } t }$ using the techniques presented in [4]. Given a working point [ ¯s $\overline { { e } } _ { y } \ \overline { { e } } _ { \psi } \ \bar { \beta } _ { 1 } ] ^ { T }$ , using finite diferences and by iteratively projecting the trailer’s axle to the reference path (·) a linear model of $e _ { v } ^ { t i }$ as a function of $[ e _ { y } \ e _ { \psi } \ \beta _ { 1 } ] ^ { T }$ <sup>γ</sup>is obtained

$$
\begin{array}{l} \hat {e} _ {y} ^ {t t} = \bar {e} _ {y} ^ {t t} + \frac {\partial e _ {y} ^ {t t}}{\partial e _ {y}} (e _ {y} - \bar {e} _ {y}) \\ \qquad + \frac {\partial e _ {y} ^ {t t}}{\partial e _ {\psi}} (e _ {\psi} - \bar {e} _ {\psi}) + \frac {\partial e _ {y} ^ {t t}}{\partial \beta_ {1}} (\beta_ {1} - \bar {\beta} _ {1}), \end{array}\tag{7}
$$

![](Oliveira2020Geometric_figs/f1759bbfd4665055e33ecc3bb4096ed215649dc51e6a7a343f5a036e1eff5f8b.jpg)  
Figure 3: An illustration of the tractor-trailer vehicle in the road-aligned frame and definitions of relevant geometric lengths and vehicle states.

where the partial derivatives $\frac { \partial e _ { y } ^ { t t } } { \partial e _ { y } } , \frac { \partial e _ { y } ^ { t t } } { \partial e _ { \psi } }$ and $\frac { \partial e _ { y } ^ { t t } } { \partial \beta _ { 1 } }$ are computed numerically (see [4] for details).

We define the state vector as $\boldsymbol { z } _ { t t } = [ e _ { y } \ e _ { \psi } \ \beta _ { 1 } \ e _ { v } ^ { t t } ] ^ { T }$ . As in the bus <sup>ψ β</sup>case, the reference path is discretized and by performing Euler forward discretization, a discrete-time nonlinear model of the tractor-trailer vehicle Eq. (2), Eq. (6), and Eq. (7) is obtained that is represented compactly as

$$
z _ {t t, i + 1} = f _ {t t} (z _ {t t, i}, \kappa_ {i}).\tag{8}
$$

## 3.3 Numerical Optimization Formulation

The on-road path planning problem for the bus $( j = b u s )$ and the tractor-trailer vehicle $( j = t t )$ are uniformly formulated as the following nonlinear programming (NLP) problem:

$$
\underset {\kappa} {\text { minimize }} \quad \omega_ {\kappa} J _ {\kappa} (\kappa) + J _ {j} (e _ {y}, e _ {y} ^ {j})\tag{9a}
$$

$$
\text { subject   to } z _ {j, i + 1} = f _ {j} (z _ {j, i}, \kappa_ {i}), i \in \{0,..., N - 1 \},\tag{9b}
$$

$$
z _ {j, 0} = z _ {\mathrm{start}}, \kappa_ {0} = \kappa_ {\mathrm{start}},\tag{9c}
$$

$$
p _ {e _ {y}} ^ {\text { obst,s }} \leq g _ {j} (z _ {j, i}), i \in \{1,..., N \},\tag{9d}
$$

$$
| \kappa_ {i} | \leq \kappa_ {\max}, i \in \{1, \dots , N - 1 \},\tag{9e}
$$

$$
\left| \kappa_ {i} - \kappa_ {i - 1} \right| \leq \kappa_ {\max} ^ {\prime}, i \in \{1, \dots , N - 1 \},\tag{9f}
$$

where $\pmb { e } _ { y } = [ e _ { y , 1 } \ . . . \ e _ { y , N } ] ^ { T } \in \mathbb { R } ^ { N }$ is the sequence of predicted lateral errors, $\dot { \pmb { e } } _ { y } ^ { j } = [ { \pmb e } _ { y , 0 } ^ { j } \ \dots \ e _ { v , N } ^ { j } ] ^ { T } \in \mathbb { R } ^ { N }$ is the sequence of predicted auxiliary lateral errors and $\pmb { \kappa } = [ \kappa _ { 0 } \kappa _ { 1 } \dots \kappa _ { N - 1 } ] ^ { T } \in \mathbb { R } ^ { N }$ is <sup>κ κ κ .</sup> <sup>.</sup> <sup>.</sup> <sup>κ</sup>the sequence of vehicle curvatures, corresponding to the commanded control inputs. The equality constraint in Eq. (9b) corresponds to the vehicle model, where j = bus implies that the bus model Eq. (4) is used and $j ~ = ~ t t$ that the tractor-trailer model Eq. (8) is used. The constraints in Eq. (9c) are the initial constraints on vehicle’s state and curvature. The planned paths ensure collision avoidance and keep the vehicle inside of the road limits through constraint Eq. (9d), where the techniques presented in [3] are used. The curvature limitations on the tractor and the bus are modeled in Eq. (9e) and Eq. (9f), where $K _ { \mathrm { m a x } }$ and $K _ { \mathrm { m a x } } ^ { \prime }$ are the maximum curvature and curvature rate, <sup>κ κ</sup>respectively.

The optimization objective Eq. (9a) is composed of two terms. The term $J _ { \kappa }$ penalizes curvature control inputs and is in this work selected as $\begin{array} { r } { J _ { \kappa } ( \kappa ) = \sum _ { i = 1 } ^ { N - 1 } ( \kappa _ { i } - \kappa _ { i - 1 } ) ^ { 2 } } \end{array}$ to promote a smooth <sup>κ κ</sup>curvature profile. That is, $\bar { J _ { \kappa } ( \kappa ) } = 0$ if and only if the curva-<sup>κ κ</sup>ture profile is constant along the entire prediction horizon. The weight $\omega _ { \kappa }$ determines the importance of driving in a smooth <sup>ωκ</sup>and comfortable manner.

The term $J _ { j }$ penalizes quantities related to the vehicle’s lateral errors and is defined as

$$
J _ {j} (\pmb {e} _ {y}, \pmb {e} _ {y} ^ {j}) = \sum_ {i = 1} ^ {N} (K _ {j, i} e _ {y, i} + e _ {y, i} ^ {j}) ^ {2},\tag{10}
$$

where $K _ { j , i } ~ > ~ 0$ is a design parameter. Recall that $e _ { y }$ and $e _ { \nu } ^ { j }$ <sup>, ></sup>are signed lateral errors, which implies that it is possible that $J _ { j } = 0$ even though $e _ { y }$ and $\pmb { e } _ { \nu } ^ { j }$ are nonzero. This property will be exploited in the next section, where geometric techniques are employed to select $K _ { j , i }$ optimally to promote a certain driving behavior.

To solve the NLP problem Eq. (9), the Sequential Quadratic Programming (SQP) approach presented in [3] is used. At each SQP iteration a Quadratic Programming (QP) problem is constructed, where the vehicle model Eq. (9b) and the collision avoidance constraint Eq. (9d) are linearized around the solution of the previous iteration using a first order Taylor-series expansion. Moreover, around the previous solution, the linear model for the sequence of auxiliary lateral error $e _ { y } ^ { j }$ is obtained using the approximation Eq. (3) for the bus $( e _ { y } ^ { j } = e _ { y } ^ { b u s } )$ and Eq. (7) for the tractor-trailer vehicle $( e _ { y } ^ { j } = e _ { y } ^ { t t } )$

## <sub>4</sub> <sub>O</sub>ptimal <sub>D</sub>riving <sub>B</sub>ehavior

In this section, a desired driving behavior is proposed that accounts for the challenges related to long and multi-body vehicles. Based on the desired driving behavior, the optimization objective related to the signed lateral errors (10) is tuned using geometric conditions. With the proposed optimization objective and design strategy, the result is that the optimal stationary solution to (9) on roads with constant curvature yields exactly the desired driving behavior.

## 4.1 Desired driving behavior

As presented in [4], the formulation of optimization objectives for long and multi-body vehicle is non-trivial. In fact, due to limited computation time, the optimization objective used in motion planners is often a combination of simple mathematical expressions that favor motion plans making the vehicle behave well according to a desired performance metric.

When driving vehicles with large dimensions, such as buses or tractor-trailer vehicles, centering one of the vehicle’s axles on the center of the road does not sufice to center the whole vehicle on the road. Instead, one needs to take particular attention to the whole vehicle body to ensure that all of it is kept as close as possible to the center of the road.

As a vehicle progresses along the road, it leaves a trail of its swept area. This area corresponds to the total covered area that the vehicle’s body (or bodies) has occupied while driving along the road. We define that the whole vehicle body is centered if the maximum extent to which its swept area extends to the left and to right of the center of the road are equal. The desired driving behavior is shown in Fig. 4.

In this figure, the red vehicle is driving with its rear axle on the center of the road. As a result, the area swept by its body, as it progresses along the road, does not have an equal distance to the left and right boundaries of the road. On the contrary, the green vehicle has a more desirable driving behavior. Even though its rear axle is not centered on the road, the spread of its swept area is at equal distances to the left and the right boundaries of the road.

![](Oliveira2020Geometric_figs/5aca7caec721f045e2b982983ce64a4797a2e33d5e1687207d49f0855a4cc6c3.jpg)

0 28 m  
![](Oliveira2020Geometric_figs/3292d3d48147afbf308e3d88df492552e8d1186f1b3e359f4b7236554ee7ff36.jpg)  
Figure 4: The desired behavior is defined as that which achieves the best centering of the vehicle swept area. Top: The vehicle has a rear axle that follows the center of the road, shown as a dotted line. Its swept area, shown in red, tends to the right side of the road. Bottom: The vehicle in has a swept area, shown in green, that is equally distant to both the left and right limits of the road. This desired driving behavior is possible because the rear axle does not follow the center of the road.

We thus define the desired driving behavior as that resulting in the swept area being equally distant to the left and right boundaries of the road. With this desired behavior defined, we turn to the problem of designing $K _ { j , i }$ in (10) such that this behavior is <sup>,</sup>obtained for the bus and tractor-trailer vehicles.

## 4.2 Derivation for the bus case

Fig. 5 illustrates the scenario of a bus driving along a road with a constant radius $R _ { r o a d }$ and achieving the desired driving behavior. The bus is assumed to drive at a constant curvature $\kappa > 0$ which renders in a constant, but unknown, turning ra-<sup>κ</sup> <sup>></sup>dius $R _ { 1 } = 1 / \kappa$ . Since $| \kappa | \leq \kappa _ { m a x } .$ , the bus turning radius satisfies $| R _ { 1 } | \ge 1 / \kappa _ { m a x }$ <sup>κ κ κ</sup>. Without loss of generality, it is further assumed <sup>/κ</sup>that the bus is driving in a left turn, giving that $R _ { 1 } ~ > ~ 0$ . The <sup>></sup>derivations for a right turn is done similarly. In a left turn, the swept area is delimited by the radius $R _ { b u s , l }$ corresponding to the <sup>,</sup>path traveled by the bus rear left wheel, and by the radius $R _ { b u s , r }$ <sup>,</sup>corresponding to the path traveled by the front right corner of the bus body. To achieve that the swept area by the vehicle’s body is equally spread to the right and to the left of the road center, the following relationship must hold:

$$
R _ {r o a d} = \frac {R _ {b u s , l} + R _ {b u s , r}}{2}.\tag{11}
$$

As the turning radius of the bus $R _ { 1 }$ is constant, basic trigonometry gives that the inner and outer radii $R _ { b u s , l }$ and $R _ { b u s , r }$ can be

represent as:

$$
\begin{array}{l} R _ {b u s, r} ^ {2} = \left(R _ {1} + \frac {W}{2}\right) ^ {2} + \left(L _ {1} + L _ {1} ^ {f}\right) ^ {2}, \\ R _ {b u s, l} = R _ {1} - \frac {W}{2}, \end{array}\tag{12}
$$

where it is assumed that $R _ { 1 } > W / 2$ . Note that this assumption <sup>> /</sup>does not pose any practical restrictions as the minimum turning radius of a bus is typically much larger than half the vehicle’s width. Since $R _ { b u s , r } > 0$ in a left turn, inserting (12) in (11) yields:

$$
R _ {r o a d} = \frac {\sqrt {\left(R _ {1} + \frac {W}{2}\right) ^ {2} + \left(L _ {1} + L _ {1} ^ {f}\right) ^ {2}} + R _ {1} - \frac {W}{2}}{2},\tag{13}
$$

which is a nonlinear equation in the unknown variable $R _ { 1 }$ . For roads with radius $R _ { r o a d }$ such that $R _ { 1 } ~ > ~ W / 2$ , the unique and positive solution to (13) is

$$
R _ {1} = \frac {- (L _ {1} + L _ {1} ^ {f}) ^ {2} + 4 R _ {r o a d} ^ {2} + 2 W R _ {r o a d}}{4 R _ {r o a d} + 2 W}.\tag{14}
$$

Equation (14) gives the optimal turning radius of the bus $R _ { 1 }$ as a function of the road curvature $R _ { r o a d }$ , which is optimal in the sense that the bus left swept width $( R _ { r o a d } - R _ { b u s , l } )$ and right swept width $( R _ { b u s , r } - R _ { r o a d } )$ <sup>,</sup> are equal. This is deemed as the <sup>,</sup>desired behavior as it perfectly centers the area swept by the vehicle around the road center.

From the derived turning radius of the bus $R _ { 1 }$ it is now possible to obtain the constant sign lateral errors $e _ { y } ^ { b u s }$ and $e _ { y } ,$ , corresponding to the bus front and rear axle distances to the road center are given by:

$$
\begin{array}{r} e _ {y} ^ {b u s} = R _ {r o a d} - \sqrt {L _ {1} ^ {2} + R _ {1} ^ {2}}, \\ e _ {y} = R _ {r o a d} - R _ {1}, \end{array}\tag{15}
$$

where $e _ { \mathrm { v } } ^ { b u s } < 0$ and $e _ { y } > 0$ . To make the optimization objective $J _ { b u s } = \mathrm { \acute { 0 } }$ <sup>< ></sup> at this stationary configuration, we get from (10) that $K _ { b u s } e _ { y } + e _ { v } ^ { b u s } = 0$ must hold. This condition together with (15) gives the optimal tuning strategy

$$
K _ {b u s} (R _ {r o a d}) = \frac {\sqrt {L _ {1} ^ {2} + R _ {1} ^ {2}} - R _ {r o a d}}{R _ {r o a d} - R _ {1}}.\tag{16}
$$

For the case of a clockwise turn with equal radius, the same geometrically derived tuning of $K _ { b u s }$ can be used. With the proposed tuning of $K _ { b u s } .$ , and under the assumption of no obstacles or other additional vehicle constraints, the optimization objectives $J _ { b u s }$ and $J _ { \kappa }$ will obtain their minimum value of zero <sup>κ</sup>when the vehicle moves along the road with a constant curvature $\begin{array} { r } { \kappa = 1 / R _ { 1 } . } \end{array}$ , where $R _ { 1 }$ is given by (14). Using this tuning <sup>κ /</sup>strategy, the optimization-based path planner is guided towards finding a solution with the desired behavior of having a balanced swept width to the left and to the right of the road center.

## 4.3 Derivation for the tractor-trailer case

Figure 6 illustrates the tractor-trailer vehicle driving along a road with a constant radius $R _ { r o a d }$ and achieving the desired driving behavior. The tractor-trailer vehicle is posed in a stationary circular equilibrium configuration (17) where a constant curvature of the tractor corresponds to $\beta _ { 1 } ^ { \prime } = 0$ and

$$
\beta_ {1} = \left(\arctan \left(\frac {M _ {1}}{R _ {1}}\right) + \arctan \left(\frac {L _ {2}}{R _ {2}}\right)\right),\tag{17}
$$

![](Oliveira2020Geometric_figs/b5b2cbdad99521d98f9c4a81d21d246158f4b683c1fd14e24c2fc4ee119e1a52.jpg)  
Figure 5: Geometric illustration of optimal road centering for a bus on a counter-clockwise turn with constant radius $R _ { r o a d } .$

where the signed radii $R _ { 1 } = 1 / \kappa$ and $R _ { 2 } ^ { 2 } = R _ { 1 } ^ { 2 } + M _ { 1 } ^ { 2 } - L _ { 2 } ^ { 2 }$ . The <sup>/κ</sup>swept area by the vehicle’s bodies is characterized by radius $R _ { t t , l }$ corresponding to the path traveled by the rear left wheel <sup>,</sup>of the trailer, and by the radius $R _ { t t , r }$ corresponding to the path <sup>,</sup>traveled by the front right corner of the tractor’s body. In analogous to the bus case, to achieve the desired driving behavior, the following relationship must hold:

$$
R _ {r o a d} = \frac {R _ {L} + R _ {R}}{2}.\tag{18}
$$

As the turning radius of of the tractor $R _ { 1 } = 1 / \kappa$ and the joint angle $\beta _ { 1 }$ <sup>/κ</sup>are both constant, basic trigonometry gives that the radii $R _ { t t , l }$ and $R _ { t t , r }$ are given by:

$$
\begin{array}{l} R _ {t t, r} ^ {2} = (R _ {1} + W / 2) ^ {2} + \left(L _ {1} + L _ {1} ^ {f}\right) ^ {2}, \\ R _ {t t, l} = R _ {2} - W / 2, \end{array}\tag{19}
$$

where it is assumed that the turning radius of the trailer’s axle $R _ { 2 } ~ > ~ W / 2$ , which is typically true for standard roads. Since $R _ { t t , r } > 0$ <sup>/</sup>, inserting (19) in (18) gives

$$
\begin{array}{l} 2 R _ {r o a d} = \sqrt {R _ {1} ^ {2} + M _ {1} ^ {2} - L _ {2} ^ {2}} - W / 2 \\ \qquad + \sqrt {(R _ {1} + W / 2) ^ {2} + (L _ {1} + L _ {1} ^ {f}) ^ {2}}, \end{array}\tag{20}
$$

which is a nonlinear equation in the variable $R _ { 1 }$ . The positive solution to (20) can compactly be represented as

$$
R _ {1} = g (R _ {r o a d}, W, L _ {1}, L _ {2}, M _ {1}, L _ {1} ^ {f}).\tag{21}
$$

Function $g$ is found using MATLAB’s symbolic toolbox, however, due to its extensive length, it is not presented in the paper. It is now possible to compute $R _ { 2 }$ and also the joint angle $\beta _ { 1 }$ using (17). From the derived radii $R _ { 1 }$ and $R _ { 2 } ,$ <sup>β</sup>, the constant signed lateral errors $e _ { v } ^ { t t }$ and $e _ { y } ,$ corresponding to the trailer’s axle and the tractor’s rear axle distances to the road center are given by:

$$
\begin{array}{l} \boldsymbol {e} _ {y} = R _ {\text {road}} - R _ {1}, \\ \boldsymbol {e} _ {y} ^ {t t} = R _ {\text {road}} - \sqrt {R _ {1} ^ {2} + M _ {1} ^ {2} - L _ {2} ^ {2}}, \end{array}\tag{22}
$$

where $e _ { \mathrm { y } } \ < \ 0$ and $e _ { v } ^ { t t } \ > \ 0$ . In analogous to the bus case, to <sup>< ></sup>make the optimization objective $J _ { t t } = \bar { 0 }$ at this stationary configuration, we get from (10) that $K _ { t t } e _ { y } + e _ { v } ^ { t t } = 0$ most hold. This together with (22) gives the optimal tuning

$$
K _ {t t} (R _ {r o a d}) = \frac {R _ {1} - R _ {r o a d}}{R _ {r o a d} - \sqrt {R _ {1} ^ {2} + M _ {1} ^ {2} - L _ {2} ^ {2}}},\tag{23}
$$

![](Oliveira2020Geometric_figs/3e313a3d502bf90f9f2882233f67433b12e153c409babb6c14907b488d4c8cff.jpg)  
Figure 6: Geometric illustration of the stationary and optimal road centering of a tractor-trailer vehicle around a counterclockwise turn with constant radius $R _ { r o a d }$

where $R _ { 1 }$ is given in (21). When considering a clockwise turn with equal radius, the same geometrically derived tuning of $K _ { t t }$ can be used. With the proposed tuning of $K _ { t t } .$ , and under the assumption of no obstacles or other additional vehicle constraints, the optimization objectives $J _ { t t }$ and $J _ { \kappa }$ will be zero when <sup>κ</sup>the tractor-trailer vehicle moves along the road with a constant joint angle (17) and a constant curvature of the tractor $\kappa = 1 / R _ { 1 }$ where $R _ { 1 }$ <sup>κ /</sup>is given by (21). Thus, using this tuning strategy the optimization-based path planner is guided towards finding a solution that achieves the desired behavior of having a balanced swept area of the tractor-trailer bodies to the left and the right of the road center.

## 4.4 Roads with varying curvature

The geometrically derived tuning of $K _ { b u s }$ and $K _ { t t }$ can now be used in the path planner’s optimization objective (10). If the road has a constant curvature, one can simply define $K _ { j , i }$ in (10) to be equal to the derived $K _ { j }$ <sup>,</sup>in Section 4.2 and Section 4.3. For the generic driving situation in which the road has a varying curvature, one needs to update $K _ { j , i }$ along the planning horizon. <sup>,</sup>In this work, this is done by updating $K _ { j , i }$ at each point along the sampled reference path $\{ \gamma ( s _ { i } ) \} _ { i = 0 } ^ { N }$ based on its curvature $\kappa _ { \gamma } ( s _ { i } )$ <sup>γ κγ</sup>We note that the geometric derivations in Section 4.2 and Section 4.3 assume a road with constant curvature. However, as is shown in the next section, using a varying $K _ { j , i }$ based on the road <sup>,</sup>curvature results in a behavior that is close to the one expected based on constant curvature assumptions.

## <sub>5</sub> <sub>R</sub>esults

This section presents results showing the advantages of the proposed framework. The results consider both the bus and tractortrailer cases and compare them with previous works. Furthermore, we test the performance of the motion planner in data gathered from real roads.

The results presented are obtained using a laptop computer with an Intel Core i7-6820 HQ@2.7GHz CPU, with the code implemented in MATLAB. We use OSQP [14] to solve the SQP iterations of the motion planning problem. For the vehicle dimensions we use the bus described in [3] and the tractor-trailer described in [4].

![](Oliveira2020Geometric_figs/a246034e35d883db7b609e76827338e2eab1a700ac11b4e5e5920165b7e5914e.jpg)  
Figure 7: In previous work [3], the bus drives close to the border of the road (blue). However, using the proposed method, the bus is able to center itself on the road (yellow).

## 5.1 Bus in a U-turn

It is noticeable that in previous work [3], driving the bus on a turn results in the vehicle being excessively close to the outer road limits. This is due to that the optimization objective only considers the lateral position of the rear axle. Using an optimization objective that considers both the rear and the front axle, and using the derived optimal $K _ { j , i }$ results in that the bus <sup>,</sup>drives centered on the road. Fig. 7 replicates the results presented in [3], where the bus drives on the border of the road, and compares them to the results obtained by our proposed method, where the bus drives centered on the road.

## 5.2 Tractor-trailer in a roundabout

We now consider the tractor-trailer driving in a roundabout scenario as presented in [4]. Using the proposed geometric method to obtain the optimal weighting parameter, the planned solution is able to center the vehicle precisely, as shown in Fig. 8. The maximum envelope widths to the left and right of the road center difer only by 0 04 m as presented in Fig. 9, and are both <sup>.</sup>very close to the optimally derived envelope width. A transient behavior can be observed at the entrance and exit of the roundabout, however, for a considerable length of the maneuver, the vehicle is driving according to the geometrically derived optimal stationary behavior.

To further validate our geometrical approach, Fig. 10 compares the derived optimal vehicle curvature, obtained at each road distance s, with the planned vehicle curvature found by the motion planner. It can be seen that the planned curvature follows the optimal curvature quite closely, with the exception of transients at the entrance and exit of the roundabout. Fig. 10 also compares the planned and optimal articulation angles $\beta .$ In contrast <sup>β</sup>to the curvature, the articulation angle has a slower response time, as can be seen by the significantly longer transient behavior.

![](Oliveira2020Geometric_figs/77aad113798fbd1ec598e57e09aee2760169b97396f2e53042017dcf97ae89ec.jpg)  
Figure 8: The tractor-trailer vehicle is able to center its whole body as it drives along the roundabout.

![](Oliveira2020Geometric_figs/0424fe4d30dd0a570665d7f8fa4978ae4dfb330a829c31954838eb419ed8e7d2.jpg)  
Figure 9: The proposed motion planner achieves a balanced tractor and trailer centering, where the maximum left and right widths correspond to 2 30 m and 2 26 m respectively. These widths are both fairly close to the expected width of 2 27 m derived geometrically.

![](Oliveira2020Geometric_figs/b29b8a0e40229f92dbed9aa96e2e7cb2e8c0e4c7291fb3949e8755b7664a8867.jpg)

![](Oliveira2020Geometric_figs/06f2c198eb94fc0738372dc628d2a788544d960ce7374de4727255b857f5e0f5.jpg)  
Figure 10: Top: The solution path curvature of the proposed motion planner closely follows the optimal curvature derived using stationarity principles. Bottom: The same is true with respect to the articulation angle .

The optimal $K _ { t t , j }$ values used in this experiment are computed <sup>,</sup>online using (23). In previous work [4], $K _ { t t , j }$ would have to <sup>,</sup>be computed ofline, either by manual tuning, or automatically found by trying out diferent values and choosing the best. Both options are quite time consuming, and the results cannot be generalized for diferent vehicle configurations or road scenarios. With the proposed method, we are able to compute the optimal $K _ { t t , j }$ values online, allowing them to dynamically adapt <sup>,</sup>to the current road characteristics. This represents a significant improvement over the work [4].

## 5.3 Computational times on real road data

We run tests on road data obtained from Scania’s test facilities in Sodert ¨ alje, Sweden, and measure the computational times¨ of the proposed methods for the bus and tractor-trailer cases. For both vehicles, we assuming a planning horizon of 100 m, and a discretization of the reference path of 0 5 m. The motion <sup>.</sup>planner is implemented in a receding horizon fashion, where every planned path is executed for the first 5 m and then a new plan is computed over a shifted horizon.

Problem 9 is solved using an SQP approach [3]. The SQP algorithm can run until convergence of the solution, i.e., until the solution of a given QP is arbitrarily close to the linearization point. Alternatively, it can run in an Real-Time Iteration (RTI) fashion [11], where only one QP iteration is performed at each planning step. This is particularly suited for motion planners that operate in a receding horizon, since the linearization of the QP step, will correspond to the previous motion planner solution, therefore resembling an SQP that runs until convergence of the solution.

The computational results for both methods are shown in Table 1. It has been observed in our experiments that both the SQP and RTI schemes results in almost identical vehicle performances. With respect to computational times, the RTI scheme is on average twice as fast as the SQP, however its biggest advantage comes from the worst-case planning time, where it is an order of magnitude faster.

Table 1: Computational times of the proposed method.

<table><tr><td rowspan="2">Vehicle</td><td colspan="2">SQP time</td><td colspan="2">RTI time</td></tr><tr><td>mean</td><td>max</td><td>mean</td><td>max</td></tr><tr><td>Bus</td><td>0.079 s</td><td>0.742 s</td><td>0.030 s</td><td>0.048 s</td></tr><tr><td>Tractor-trailer</td><td>0.137 s</td><td>1.248 s</td><td>0.050 s</td><td>0.137 s</td></tr></table>

## <sub>6</sub> <sub>C</sub>onclusions

We have introduced a framework for designing optimization objectives of motion planners. The developed approach targets both buses and tractor-trailers, resulting in a unified framework for a large number of possible heavy-duty vehicle configurations. To design the optimization objective, we define the desired driving behavior to be that resulting in the whole vehicle body driving as centered on the road as possible. We then use a computationally eficient optimization objective to achieve this complex driving behavior. The optimization objective formulation is obtained via geometric arguments, being suitable for online computation, allowing for a continuous adaptation of the optimization objective to the current road characteristics. Our results show significant improvements upon previous works targeting buses and tractor-trailers. Tests using real road data highlight the capability of the method to tackle real-world scenarios and indicate its computational tractability.

As future work, we will generalize the developed framework to more complex vehicles, such as vehicles with multiple actuated steering axles, and articulated vehicles composed of a tractor, a dolly, and a trailer. The framework can be readily extended to consider alternative desired driving behaviors besides that of centering the vehicle on the road. Based on the current traffic situation, it might be beneficial to plan paths that maximize the distance between the vehicle swept area and oncoming traffic. To further validate the approach, we plan to implement the proposed methods on real world tests using autonomous heavyduty vehicles.

## <sub>R</sub>eferences

[1] C. Katrakazas, M. Quddus, W. Chen, and L. Deka, “Realtime motion planning methods for autonomous on-road driving: State-of-the-art and future research directions,” Transportation Research Part C: Emerging Technologies, vol. 60, pp. 416 – 442, 2015.

[2] B. Paden, M. C<sup>ˇ</sup> ap, S. Z. Yong, D. Yershov, and E. Frazzoli,´ “A survey of motion planning and control techniques for selfdriving urban vehicles,” IEEE Transactions on Intelligent Vehicles, vol. 1, no. 1, pp. 33–55, March 2016.

[3] R. Oliveira, P. F. Lima, G. Collares Pereira, J. Mårtensson, and B. Wahlberg, “Path planning for autonomous bus driving in highly constrained environments,” in 2019 IEEE Intelligent Transportation Systems Conference (ITSC), Oct 2019.

[4] R. Oliveira, O. Ljungqvist, P. F. Lima, and B. Wahlberg, “Optimization-based on-road path planning for articulated vehicles,” arXiv e-prints, p. arXiv:2001.06827, 2020.

[5] S. M. LaValle and J. James J. Kufner, “Randomized kinodynamic planning,” The International Journal of Robotics Research, vol. 20, no. 5, pp. 378–400, 2001.

[6] M. Pivtoraiko, R. A. Knepper, and A. Kelly, “Diferentially constrained mobile robot motion planning in state lattices,” Journal of Field Robotics, vol. 26, no. 3, pp. 308–333, 2009.

[7] Y. Kuwata, G. A. Fiore, J. Teo, E. Frazzoli, and J. P. How, “Motion planning for urban driving using RRT,” in International

Conference on Intelligent Robots and Systems, Sept 2008, pp. 1681–1686.

[8] M. McNaughton, C. Urmson, J. M. Dolan, and J. W. Lee, “Motion planning for autonomous driving with a conformal spatiotemporal lattice,” in International Conference on Robotics and Automation, May 2011, pp. 4889–4895.

[9] C. Gotte, M. Keller, C. R¨ osmann, T. Nattermann, C. Haß, K. H.¨ Glander, A. Seewald, and T. Bertram, “A real-time capable model predictive approach to lateral vehicle guidance,” in International Conference on Intelligent Transportation Systems, Nov 2016.

[10] T. Tram, I. Batkovic, M. Ali, and J. Sjoberg, “Learning when to¨ drive in intersections by combining reinforcement learning and model predictive control,” in 2019 IEEE Intelligent Transportation Systems Conference (ITSC), Oct 2019, pp. 3263–3268.

[11] L. Svensson, M. Bujarbaruah, N. Kapania, and M. Torngren,¨ “Adaptive Trajectory Planning and Optimization at Limits of Handling,” arXiv e-prints, p. arXiv:1903.04240, Mar 2019.

[12] J. Ziegler, P. Bender, T. Dang, and C. Stiller, “Trajectory planning for bertha — a local, continuous method,” in 2014 IEEE Intelligent Vehicles Symposium Proceedings, June 2014, pp. 450– 457.

[13] P. F. Lima, G. C. Pereira, J. Mårtensson, and B. Wahlberg, “Experimental validation of model predictive control stability for autonomous driving,” Control Engineering Practice, vol. 81, pp. 244 – 255, 2018.

[14] B. Stellato, G. Banjac, P. Goulart, A. Bemporad, and S. Boyd, “OSQP: An operator splitting solver for quadratic programs,” ArXiv e-prints, Nov. 2017.

[15] H. Ferreau, C. Kirches, A. Potschka, H. Bock, and M. Diehl, “qpOASES: A parametric active-set algorithm for quadratic programming,” Mathematical Programming Computation, vol. 6, no. 4, pp. 327–363, 2014.

[16] O. Ljungqvist, N. Evestedt, D. Axehill, M. Cirillo, and H. Pettersson, “A path planning and path-following control framework for a general 2-trailer with a car-like tractor,” Journal of Field Robotics, vol. 36, no. 8, pp. 1345–1377, 2019.

[17] N. Evestedt, O. Ljungqvist, and D. Axehill, “Motion planning for a reversing general 2-trailer configuration using Closed-Loop RRT,” in Proceedings of the 2016 IEEE/RSJ International Conference on Intelligent Robots and Systems, 2016, pp. 3690–3697.

[18] B. Li, Y. Zhang, T. Acarma, Q. Kong, and Y. Zhang, “Trajectory planning for a tractor with multiple trailers in extremely narrow environments: A unified approach,” in Proceeding of the 2019 International Conference on Robotics and Automation, 2019, pp. 8557–8562.

[19] F. Lamiraux, J. . Laumond, C. Van Geem, D. Boutonnet, and G. Raust, “Trailer truck trajectory optimization: the transportation of components for the airbus a380,” IEEE Robotics Automation Magazine, vol. 12, no. 1, pp. 14–21, March 2005.

[20] N. van Duijkeren, T. Keviczky, P. Nilsson, and L. Laine, “Realtime nmpc for semi-automated highway driving of long heavy vehicle combinations,” IFAC-PapersOnLine, vol. 48, no. 23, pp. 39–46, 2015.

[21] Y. Gao, A. Gray, J. V. Frasch, T. Lin, E. Tseng, J. K. Hedrick, and F. Borrelli, “Spatial predictive control for agile semi-autonomous ground vehicles,” in Proceedings of the 11th international symposium on advanced vehicle control, 2012.

[22] C. Altafini, “Path following with reduced of-tracking for multibody wheeled vehicles,” IEEE Transactions on Control Systems Technology, vol. 11, no. 4, pp. 598–605, 2003.