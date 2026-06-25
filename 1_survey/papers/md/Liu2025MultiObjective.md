---
citation_key: Liu2025MultiObjective
arxiv_id: 2507.17140
arxiv_url: "https://arxiv.org/abs/2507.17140"
title: "Multi-Objective Trajectory Planning for a Robotic Arm in Curtain Wall Installation"
authors_short: "Xiao Liu et al."
year: 2025
direction_tag: M_multi_objective_planning
source: mineru-vlm
converter: mineru-open-api
model: vlm
converted_at: 2026-06-25T08:14:08Z
origin: ai+web
reviewed: false
---

# Multi-Objective Trajectory Planning for a Robotic Arm in Curtain Wall Installation

Xiao Liu<sup>1</sup>, Yunxiao Cheng<sup>1</sup>, Weijun Wang<sup>1</sup>, Tianlun Huang<sup>1</sup>, Zhiyong Wang<sup>1</sup>, Wei Feng <sup>1,2∗</sup>

Abstract— In the context of labor shortages and rising costs, construction robots are regarded as the key to revolutionizing traditional construction methods and improving efficiency and quality in the construction industry. In order to ensure that construction robots can perform tasks efficiently and accurately in complex construction environments, traditional single-objective trajectory optimization methods are difficult to meet the complex requirements of the changing construction environment. Therefore, we propose a multi-objective trajectory optimization for the robotic arm used in the curtain wall installation. First, we design a robotic arm for curtain wall installation, integrating serial, parallel, and folding arm elements, while considering its physical properties and motion characteristics. In addition, this paper proposes an NSGA-III-FO algorithm (NSGA-III with Focused Operator, NSGA-III-FO) that incorporates a focus operator screening mechanism to accelerate the convergence of the algorithm towards the Pareto front, thereby effectively balancing the multi-objective constraints of construction robots. The proposed algorithm is tested against NSGA-III, MOEA/D, and MSOPS-II in ten consecutive trials on the DTLZ3 and WFG3 test functions, showing significantly better convergence efficiency than the other algorithms. Finally, we conduct two sets of experiments on the designed robotic arm platform, which confirm the efficiency and practicality of the NSGA-III-FO algorithm in solving multi-objective trajectory planning problems for curtain wall installation tasks.

## I. INTRODUCTION

In the current construction landscape, construction robots are an important way to improve construction efficiency and quality[1]-[2]. Trajectory planning can ensure that robots execute construction operations optimally, thereby minimizing construction time and energy consumption. Optimizing the motion trajectory of construction robots is crucial[3]–[4]. The optimization of motion trajectories primarily involves three aspects: time[5]–[7], energy consumption[8], and joint impact[9]–[10] during motion.

Multi-objective trajectory planning typically involves more complex tasks and constraints, and requires consideration of the priorities and resolution of conflicts between different objectives. Solving this problem has always been a popular topic in academic research[11]–[14]. [15] proposes a multi-objective trajectory optimization method based on response surface methodology (RSM) and non-dominated sorting genetic algorithm III (NSGA-III). [5] proposes a 3- 5-3 polynomial interpolation trajectory planning algorithm based on an improved cuckoo search algorithm (ICS) that functions under a velocity constraint. The proposed algorithm performed well and realized a better time-optimal trajectory. [16] efficiently addressed the trajectory-planning problem for kiwifruit harvesting manipulators using multi-objective trajectory planning based on NSGA-III. [17] proposed an improved elitist non-dominated sorting genetic algorithm (INSGA-II) by introducing three genetic operators: ranking group selection (RGS), direction-based crossover (DBX), and adaptive precision-controllable mutation (APCM), which was developed to optimize travelling time and torque fluctuation.

Most of the existing research and methods have focused on industrial robotic arms. To address the challenges faced by construction robots, such as long working hours, high energy consumption, and complex tasks, we propose a multi-objective trajectory planning method for our designed robotic arm. This method introduces a focused operator selection mechanism and a new algorithm, NSGA-III-FO (NSGA-III with Focused Operator, NSGA-III-FO), to enhance the population selection process and accelerate convergence towards the Pareto front. The proposed algorithm demonstrates significant performance advantages in convergence efficiency, effectively balancing multiple objectives to achieve solution sets that meet task requirements.

![](Liu2025MultiObjective_figs/a3e2c89030960c3f010009bc511c769315c9680e7246bb8b3367e6607164ae1c.jpg)  
Fig. 1. Structural Design of a Robotic Arm for Curtain Wall Installation

## II. DESIGN OF A ROBOTIC ARM FOR CURTAIN WALL INSTALLATION

Currently, serial robots struggle to meet the high load-toweight ratio requirements for construction tasks. Leveraging the high load-bearing capacity of parallel mechanisms with redundant actuation and the superior workspace characteristics of serial mechanisms, we design a robotic arm for curtain wall installation. The proposed arm includes a folding arm, a serial-parallel arm, and an end effector, as illustrated in Figure 1. The folding arm consists of a base platform, two support arms, three hydraulic cylinders, and an end platform. The serial-parallel arm comprises three 2-DOF parallel mechanisms connected in series, each containing three hydraulic cylinders(two active axes and one passive axis). All joints are driven by hydraulic cylinders. The entire robotic arm has six degrees of freedom and can perform compliant operations over a 150-degree range. The wrist motor enables ±360-degree rotation of the end effector. The end effector consists of four suction cups and a suction cup frame, controlled by a solenoid valve for overall air circuit switching, designed for glass handling.

## III. TRAJECTORY PLANNING

## A. Sixth-Order B-Spline Interpolation Trajectory

Mapping from Task Space to Joint Space: To execute predefined trajectory tasks, B-spline curves define the trajectory in task space. Key points $P _ { n }$ are determined based on the velocity requirements, where n denotes the sequence number of key points. Moving from the initial point $P _ { 0 }$ to the final point $P _ { n }$ in task space, a series of key points in joint space can be obtained via inverse kinematics algorithms.

$$
P _ {i n} = (q _ {i n}, t _ {n}),\tag{1}
$$

In the equations: i denotes the joint of the robotic arm; $q _ { i n }$ represents the joint angle at key point n for joint $i ,$ and $t _ { n }$ indicates the time at which the trajectory passes through key point $P _ { i n }$ . To construct a sixth-order B-spline curve based on the given key points, ensuring that each joint trajectory passes through these points $p ( x )$ , B-spline interpolation is used to determine the control points that make the curve pass through these specified points.

To ensure that the robotic arm’s joints pass through $n + 1$ key points, we have:

$$
P \left(x _ {i + 6}\right) = \sum_ {j = i} ^ {i + 6} d _ {j} N _ {j, 6} \left(x _ {i + 6}\right)\tag{2}
$$

Where: $d _ { j }$ denotes the control points; $x$ is the knot vector, where $x _ { i + 6 } \in [ x _ { 6 } , x _ { i + 6 } ] ;$ ; jisthe parameter of the B-spline curve; $N _ { j , 6 } ( x )$ is the 6th-order normalized B-spline basis function, which depends on the vector x and is constructed recursively. The constraint function can be expressed as:

$$
\left\{ \begin{array}{l} \dot {P} (x) | _ {x _ {6}} = v _ {s}, \dot {P} (x) | _ {x _ {6}} = v _ {e} \\ \ddot {P} (x) | _ {x _ {6}} = a _ {s}, \ddot {P} (x) | _ {x _ {6}} = a _ {e} \\ \dddot {P} (x) | _ {x _ {6}} = j _ {s}, \dddot {P} (x) | _ {x _ {6}} = j _ {e} \end{array} \right.\tag{3}
$$

In the equations: $\nu _ { s }$ and $\nu _ { e }$ represent the initial and final velocities of the joint; $a _ { s }$ and $\nu _ { e }$ represent the initial and final accelerations of the joint; $j _ { s }$ and $j _ { e }$ represent the initial and final jerk of the joint. $\dot { \mathbf { P } } ( x ) , \ddot { \mathbf { P } } ( x )$ , and $\dddot { \mathbf { P } } ( x )$ denote the first, second, and third derivatives of the B-spline curve, respectively. The velocity, acceleration, and jerk for each joint in a sixth-order B-spline can be expressed as:

$$
\left\{ \begin{array}{l} v (t) = \dot {P} (x) = \sum_ {j = i - 5} ^ {i} d _ {j} ^ {1} N _ {j, 5} (x) \\ a (t) = \ddot {P} (x) = \sum_ {j = i - 4} ^ {i} d _ {j} ^ {2} N _ {j, 4} (x) \\ j (t) = \overset {...} {P} (x) = \sum_ {j = i - 3} ^ {i} d _ {j} ^ {3} N _ {j, 3} (x) \end{array} \right.\tag{4}
$$

In the equations: $\mathbf { d } _ { j } ^ { r } = \left[ d _ { 1 _ { j } } ^ { r } , d _ { 2 _ { j } } ^ { r } , \ldots , d _ { N _ { j } } ^ { r } \right] ^ { \mathrm { T } }$ is the control point vector, and the derivative order r is 1, 2, or 3.

## B. Multi-Objective Trajectory Planning

In real-world construction scenarios, energy consumption optimization is crucial for robots powered by batteries or generators. Joint impact optimization can reduce wear and tear on mechanical joints, thereby extending the robot lifespan. A high efficiency is also essential for the construction process. Therefore, the optimization objectives are time, joint impact, and energy consumption. Define the time evaluation function $f _ { 1 }$ , joint impact evaluation function $f _ { 2 }$ , and energy consumption evaluation function $f _ { 3 }$ as follows:

$$
\begin{array}{l} \mathrm{f} = \sum_ {i = 0} ^ {n - 1} (t _ {i + 1} - t _ {i}) \\ f _ {2} = \sum_ {k = 1} ^ {K} \sqrt {\frac {1}{T} \int_ {0} ^ {T} (j _ {i}) ^ {2} d t} \\ f _ {3} = \sum_ {k = 1} ^ {K} \sqrt {\frac {1}{T} \int_ {0} ^ {T} (\omega_ {i} \tau_ {i}) ^ {2} d t} \end{array}\tag{5}
$$

In the equations: K and k represent the total number of sampling points and the number of sampling points, respectively; $j _ { i }$ is the angular jerk of joint $i ; \omega _ { i }$ is the angular velocity of joint $i ; \tau _ { i }$ is the output torque of joint $i .$ The motion constraints for the robotic arm are defined as follows:

$$
\begin{array}{l} | \tau_ {i} (t) | \leq \tau_ {i \max} \\ | j _ {i} (t) | \leq j _ {i \max} \\ | \omega_ {i} (t) | \leq \omega_ {i \max} \\ | v _ {i} (t) | \leq v _ {i \max} \end{array}\tag{6}
$$

where: $\tau _ { i \operatorname* { m a x } } , j _ { i \operatorname* { m a x } } , \omega _ { i \operatorname* { m a x } } , \nu _ { i \operatorname* { m a x } }$ is the maximum torque, the maximum angular jerk, the maximum angular velocity, and the maximum linear velocity of joint i.

## IV. NSGA-III-FO MULTI-OBJECTIVEOPTIMIZATION ALGORITHM WITH FOCUSOPERATOR

Researchers commonly employ heuristic multi-objective optimization algorithms to address robotic arm trajectory planning problems [18]–[19], aiming to find an optimal set of solutions that balance various performance metrics. NSGA-III is a multi-objective optimization algorithm [20] that utilizes a reference-point-based strategy to decompose the objective space, allowing each reference point to correspond with multiple solutions. However, NSGA-III overlooks the efficiency of converging towards the Pareto front. To enhance the convergence performance, we propose an enhanced version of NSGA-III named NSGA-III-FO(NSGA-III with Focused Operator, NSGA-III-FO). This algorithm introduces focused and non-focused operators to accelerate population screening, thereby improving the overall convergence efficiency.

## A. NSGA-III-FO Algorithm

The fundamental idea of the NSGA-III-FO algorithm is to iteratively generate a set of non-dominated solutions, where each non-dominated solution approximates an optimal solution. In each iteration, the algorithm creates a new initial population based on the non-dominated solutions from the current solution set. The algorithm first selects individuals using focused operators for inclusion in the next generation, while directly excluding those selected by non-focused operators. The remaining individuals are then subjected to non-dominated sorting to form the next generation solution set. This process continuously optimizes multiple objective functions simultaneously, ultimately yielding an optimal set of target allocation schemes. The optimization flowchart is illustrated in Figure 2.

![](Liu2025MultiObjective_figs/8d1db0034cf1c567b4e8384378c8caa477b26a8cbdc7f89200e6a1baa9f7ad63.jpg)  
Fig. 2. Flowchart of NSGA-III-FO for Multi-objective Optimization)

The specific solution steps of the NSGA-III-FO algorithm are as follows:

(1) Randomly initialize an initial population $P _ { t }$ of size $\mathrm { N , }$ construct a reference plane based on boundary crossover, for m objective optimization functions, divide into p on the mdimensional standardized hyperplane, and uniformly generate H reference points. The calculation method is as follows:

$$
H = \frac {(m + p - 1) !}{p ! (m - 1) !}\tag{7}
$$

(2) In the initial population $P _ { t }$ , select the individual with the smallest Euclidean distance from the reference plane as the focused operator, which directly enters the offspring population, and select the individual with the largest Euclidean distance from the reference plane as the non-focused operator to be directly excluded.

(3) The remaining individuals undergo non-dominated sorting, and the better individuals are selected from the sorting results to undergo crossover and mutation operations. The crossover probability and mutation probability are calculated as follows:

$$
P _ {c} = \left\{ \begin{array}{l l} P _ {c, \max} - \frac {P _ {c , \max} - P _ {c , \min}}{1 + e ^ {\cos \left[ \left(\frac {\bar {f} - f _ {\max}}{\bar {f} - f _ {\min}}\right) \pi \right]}}, & f _ {\max} \leq \bar {f} \\ P _ {c, \max}, & f _ {\max} > \bar {f} \end{array} \right.\tag{8}
$$

$$
P _ {m} = \left\{ \begin{array}{l l} P _ {m, \max} - \frac {P _ {m , \max} - P _ {m , \min}}{1 + e ^ {\cos \left[ \left(\frac {\bar {f} - f _ {\max}}{\bar {f} - f _ {\min}}\right) \pi \right]}}, & f _ {\max} \leq \bar {f} \\ P _ {m, \max}, & f _ {\max} > \bar {f} \end{array} \right.\tag{9}
$$

In the formula, $P _ { c . m a x }$ and $P _ { c . m i n }$ represent the maximum and minimum values of the set crossover probability, respectively, while $P _ { m a x }$ and $P _ { m , m i n }$ represent the maximum and minimum values of the set mutation probability, respectively. $\overline { { f } }$ is the average fitness function value of the current solution, and $f _ { m a x }$ and $f _ { m i n }$ are the maximum and minimum values of the fitness function for the current solution, respectively. After crossover and mutation produce offspring populations $Q _ { t }$ , both populations are combined to form a new offspring population $R _ { t }$ of size 2N.

(4) Perform rapid non-domination sorting, retaining excellent and diverse individuals according to the non-domination relationship, forming a new parent population $P _ { t + 1 }$

(5) Generate a new offspring population $\boldsymbol { Q } _ { t + 1 }$ through basic operations of genetic algorithms, merge $P _ { t + 1 }$ with $\boldsymbol { Q } _ { t + 1 }$ to form a new population R, repeat these operations until reaching the designated number of generations.

## B. Performance Testing of the NSGA-III-FO Algorithm

The NSGA-III-FO algorithm is used to conduct ten comparative tests against the NSGA-III, MOEA/D, and MSOPS-II algorithms on the DTLZ3 and WFG3 test functions. DTLZ3 and WFG3, as classic benchmark functions in multiobjective optimization, are widely used to evaluate the algorithm performance. Their standardized status ensures fair assessment. Using these recognized benchmarks facilitates an effective comparison with the existing algorithms. An important performance evaluation metric in multi-objective optimization problems is the Inverse Generational Distance (IGD). This metric measures the distance between the nondominated solution set generated by the algorithm and the reference non-dominated solution set, thereby evaluating the performance of the algorithm. The smaller the IGD value, the closer the non-dominated solution set generated by the algorithm is to the reference non-dominated solution set, indicating better algorithm performance. The calculation method is:

$$
I G D \left(P, P ^ {*}\right) = \frac {\sum_ {i = 1} ^ {| P |} d \left(P _ {i} , P ^ {*}\right)}{| P ^ {*} |}\tag{10}
$$

In the formula, $P$ represents the non-dominated point set in the target space; $P ^ { * }$ represents the uniformly distributed points on the true Pareto frontier; $| P |$ represents the number of solutions in set $P ; d \left( P _ { i } , P ^ { * } \right)$ represents the Euclidean distance between the solution $P _ { i }$ and $P ^ { * }$ in the target space. The calculation result is shown in the table below:

TABLE I  
COMPARISON OF IGD VALUES AMONG NSGA-III-FO AND OTHER MULTI-OBJECTIVE ALGORITHMS

<table><tr><td>Test Function</td><td>NSGA-III</td><td>MSOPS-II</td><td>MOEA/D</td><td>NSGA-III-FO</td></tr><tr><td>DTLZ3</td><td> $343.9 \pm 24.9$ </td><td> $352.4 \pm 28.0$ </td><td> $387.1 \pm 23.8$ </td><td> $341.3 \pm 25.3$ </td></tr><tr><td>WFG3</td><td> $0.6122 \pm 0.038$ </td><td> $0.7547 \pm 0.048$ </td><td> $0.6932 \pm 0.051$ </td><td> $0.6087 \pm 0.028$ </td></tr></table>

The hypervolume(HV)is an important metric for evaluating the quality of Pareto solution sets in multi-objective optimization algorithms. It measures the volume enclosed by the Pareto front and a reference point. Hypervolume can simultaneously reflect the convergence and diversity of the solution set. The hypervolume convergence curves for the DTLZ3 and WFG3 test functions, using the origin as the reference point in the Pareto solution space, are shown in the following figure: From

![](Liu2025MultiObjective_figs/d2317a9f7eac0474133a7df0070e710a1fe6ae322d9c6b5a644b47aacf5c99fb.jpg)

![](Liu2025MultiObjective_figs/323dc969939ecc882e78ae23e9f2fb737e361065f28291330b17a567ea44f1f1.jpg)  
Fig. 3. The HV Convergence Curves of Each Algorithm (Shaded Areas Indicate Standard Deviation Ranges)

Figure 3 and Table 2, it can be observed that when the number of iterations is 20,000, the HV value of MSOPS-II for the DTLZ3 test function is only 63.6% of that of NSGA-III-FO, while other algorithms have not yet found effective solutions. When the number of iterations reaches 50,000, the HV values of NSGA-III-FO, NSGA-III, and MSOPS-II tend to converge and their results are close, while the curve of MOEA/D has not yet converged. By analyzing the calculation results of IGD values, it is evident that NSGA-III-FO exhibits better convergence and stability.

In the WFG3 test function, at 10,000 iterations, the HV values of NSGA-III-FO, NSGA-III, and MSOPS-II have approached convergence, with NSGA-III-FO exhibiting the smallest standard deviation and stable convergence. In terms of IGD values, NSGA-III-FO outperforms the other three algorithms, with significantly lower average values. Although NSGA-III also performs well on WFG3, it still falls short compared to NSGA-III-FO.

## V. MULTI-OBJECTIVE TRAJECTORY PLANNING SIMULATION BASED ON NSGA-III-FO ALGORITHM

We use the number of iterations as a convergence metric, where convergence speed reflects algorithm efficiency rather than absolute runtime. In task space, trajectories are defined using B-spline curves, and key points in the sequence of poses are determined based on trajectory task requirements. We set seven key points during the motion process, as shown in Table 2.

TABLE II  
SETTING KEY POINTS

<table><tr><td>Node</td><td>Joint 1</td><td>Joint 2</td><td>Joint 3</td><td>Joint 4</td><td>Joint 5</td><td>Joint 6</td></tr><tr><td>1</td><td>43.35</td><td>78.54</td><td>-90.05</td><td>0</td><td>0</td><td>0</td></tr><tr><td>2</td><td>46.35</td><td>86.43</td><td>-56.68</td><td>1.68</td><td>1.31</td><td>0.68</td></tr><tr><td>3</td><td>55.04</td><td>99.62</td><td>-39.25</td><td>4.71</td><td>3.65</td><td>2.71</td></tr><tr><td>4</td><td>62.67</td><td>104.06</td><td>-21.94</td><td>6.51</td><td>5.53</td><td>4.64</td></tr><tr><td>5</td><td>68.04</td><td>112.40</td><td>-9.04</td><td>8.14</td><td>6.99</td><td>6.53</td></tr><tr><td>6</td><td>74.40</td><td>124.5</td><td>1.68</td><td>12.8</td><td>8.18</td><td>7.31</td></tr><tr><td>7</td><td>84.13</td><td>133.6</td><td>12.81</td><td>16.14</td><td>10.15</td><td>9.21</td></tr></table>

Based on the dynamic parameters of a foldable serialparallel robotic arm, we use the NSGA-III-FO algorithm to optimize the time function $f _ { 1 }$ , impact function $f _ { 2 }$ , and energy consumption function $f _ { 3 }$ through simulation. The multi-objective optimization trajectory Pareto solution set was obtained, as shown in Figure 4:

![](Liu2025MultiObjective_figs/77270ebb008280d4a423977b1c09c6086241a38623c32343d483ea07f4a148fb.jpg)  
Fig. 4. Pareto Solution Set of Multi-objective Optimized Trajectories Based on NSGA-III-FO Algorithm

As shown in Figure 4, A, B, and C represent the optimal solutions for $f _ { 1 } , f _ { 2 } ,$ , and $f _ { 3 } ,$ , respectively. It can be observed that $f _ { 1 }$ and $f _ { 2 }$ exhibit a negative correlation, while the relationship between $f _ { 1 }$ and $f _ { 3 }$ is more complex but generally also shows a negative correlation. The time vectors of the optimal solutions for the objective functions $f _ { 1 } , f _ { 2 }$ , and $f _ { 3 } ,$ along with their corresponding function values, are shown in Table 3. The time vectors are the collection of time points corresponding to the seven key points in the motion process.

The Pareto front of the solution set is observed to exhibit uniform distribution and good diversity. When applying the robotic arm to practical work requirements, different weights can be set for time, energy consumption, and joint impact metrics, allowing the selection of a multi-objective optimal solution that best meets the requirements. Additionally, the

TABLE III  
TIME VECTORS AND CORRESPONDING OBJECTIVE FUNCTION VALUES

<table><tr><td>Plan</td><td>Time Vector(s)</td><td> $f_1$  (s)</td><td> $f_2$  (N)</td><td> $f_3$  (J)</td></tr><tr><td>A</td><td>[0, 2.01, 3.77, 5.79, 6.53, 8.85, 10.48]</td><td>10.48</td><td>900.87</td><td>45.89</td></tr><tr><td>B</td><td>[0, 3.51, 7.34, 10.91, 13.31, 15.32, 18.94]</td><td>18.94</td><td>362.25</td><td>10.95</td></tr><tr><td>C</td><td>[0, 1.51, 5.09, 10.23, 15.67, 18.98, 23.27]</td><td>23.27</td><td>443.33</td><td>6.40</td></tr></table>

NSGA-III, MOEA/D, and NSGA-II algorithms are used for trajectory planning of the robotic arm with $f _ { 1 } , f _ { 2 } ,$ , and $f _ { 3 }$ as the objective functions, and compared with the NSGA-III-FO algorithm in terms of the HV metric. The convergence curves are shown in Figure 5.

![](Liu2025MultiObjective_figs/57ed54a1397c5a297a09f7aa911b1f293ffadf1f4713899f0ae433b2c4c2489c.jpg)  
Fig. 5. HV Indicator of Multi-objective Trajectory Planning Solutions for the robotic arm

The experimental results show that the NSGA-III-FO algorithm demonstrates a clear advantage in convergence rate, further validating its potential and effectiveness in exploring the solution space.

## VI. EXPERIMENT ON MULTI-OBJECTIVE TRAJECTORY PLANNING

## A. Robotic Arm Experimental Platform

The curtain wall installation robotic arm we developed primarily consists of a folding arm, a serial-parallel manipulator, and an end effector. The folding arm is configured with three joints: Joint 1, Joint 2, and Joint 3. The serial-parallel manipulator is restricted to three degrees of freedom in the vertical plane, designated as Joint $^ { 4 , }$ Joint 5, and Joint 6. The experimental platform for the curtain wall installation robotic arm.is shown in Figure 6.

## B. Experiment

We designed two construction tasks based on real-world scenarios to perform trajectory planning for the robotic arm. Utilizing the NSGA-III-FO algorithm, we successfully obtained solution sets that best met the task requirements. The feasibility of these solution sets was verified through experiments.

![](Liu2025MultiObjective_figs/40a2b53149c298f24c40198d13ef8a04844e179797348a7b464aa9bcdd3c7268.jpg)  
Fig. 6. Robotic Arm Experimental Platform for Curtain Wall Installation Trajectory Planning

(1)Construction Task 1—Vertical Surface Installation: The task space is obstacle-free. Starting from the home position, the robotic arm picks up the steel plate and then transports it to the target position on a vertical surface directly in front of the arm. The steel plate weighs 10 kg and is picked up using four suction cups in 2 seconds. The task requirements are that $f _ { 1 }$ must be less than $4 0 , f _ { 2 }$ must be less than 1000, and $f _ { 3 }$ is not specified. Key points are detailed in Table 4.

TABLE IV  
JOINT ANGLES FOR KEY POINTS IN TASK 1 (°)

<table><tr><td>Key Point</td><td>Joint 1</td><td>Joint 2</td><td>Joint 3</td><td>Joint 4</td><td>Joint 5</td><td>Joint 6</td></tr><tr><td>Key Point 1</td><td>30.0</td><td>130.0</td><td>-60.0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>Key Point 2</td><td>37.2</td><td>126.4</td><td>-16.8</td><td>6.8</td><td>8.8</td><td>10.4</td></tr><tr><td>Key Point 3</td><td>73.2</td><td>119.2</td><td>19.2</td><td>14.7</td><td>15.8</td><td>16.0</td></tr><tr><td>Key Point 4</td><td>80.0</td><td>104.0</td><td>19.0</td><td>16.0</td><td>18.0</td><td>18.0</td></tr><tr><td>Key Point 5</td><td>80.0</td><td>104.0</td><td>19.0</td><td>16.0</td><td>18.0</td><td>18.0</td></tr><tr><td>Key Point 6</td><td>61.2</td><td>108.4</td><td>-1.6</td><td>12.8</td><td>11.8</td><td>10.8</td></tr><tr><td>Key Point 7</td><td>57.2</td><td>103.6</td><td>-12.8</td><td>10.0</td><td>10.0</td><td>10.0</td></tr></table>

The robotic arm’s poses at key points during the experiment are shown in Figure 7.

According to the key point requirements of Task 1, we first set the robotic arm to pass through key points 4 and 5 in 2 seconds. Next, we used the NSGA-III-FO algorithm to obtain the Pareto solution set. Finally, the trajectory was executed on the robotic arm platform. The time-optimal solution vector obtained from the NSGA-III-FO algorithm is [0, 7.744, 15.307, 22.863, 30.976, 38.720].

During Task 1 experiments, the changes in joint angles of the robotic arm and the measured joint angles are compared in Figure 8.

![](Liu2025MultiObjective_figs/87cce7279e0b08aedd51d26f10fcd7b0ddc7c9326e96863154144c85f968780b.jpg)  
(a) Key Point 1

![](Liu2025MultiObjective_figs/752657393915568fd23837b0d6396e3fa56410137991f3a9f81d047515e83fde.jpg)

![](Liu2025MultiObjective_figs/3099298d3061e49ab6c9eef3f637a07da49457c9b9b90e8eb6aeba442f0964d7.jpg)

(b) Key Point 2  
![](Liu2025MultiObjective_figs/f1dad2c4c18768c510142da3f548ee0c8e92d0cad4b6fa2dd5b2ff6cebdc0668.jpg)  
(d) Key Point 4 and 5

(c) Key Point 3  
![](Liu2025MultiObjective_figs/343f83b18d0936f5638f7d30885ace46cbf42a50f467a409955ec58ba79e2ab5.jpg)  
(e) Key Point 6

![](Liu2025MultiObjective_figs/ab15a1e855a4208f4d54fab7b715cfe7e5f4c02bfedac6886e6e9647c4cec8a6.jpg)  
(f) Key Point 7  
Fig. 7. Robotic arm poses at key points during Task 1.

![](Liu2025MultiObjective_figs/87139c95166bc8e8342696cd60e14e9eb28313285746fab9f0ba4f4c9b94e436.jpg)

![](Liu2025MultiObjective_figs/ae216714cc962bc88848d115dbf2b5fad957925d75bde84eb3491a58cccedfd1.jpg)

![](Liu2025MultiObjective_figs/433301e8121da24dd9bcfd21f735d0f8bd1a6012676b989e0e0193bce50399ac.jpg)

![](Liu2025MultiObjective_figs/883ca013360b74d044be5f7dcb4b21c220f93cc6e353c8c73836383baad417c7.jpg)

![](Liu2025MultiObjective_figs/69a2748237151cbbb2a4741d87a9256fb82d99185ffb2dd548bcbc92d0c49d41.jpg)

![](Liu2025MultiObjective_figs/052d54f4260247ef42ba882b57514173875764bad5cc14fcf0a0521c75e5d01a.jpg)  
Fig. 8. Joint Angle Variations of Robotic Arm for Task 1

In trajectory planning experiments, significant errors occurred during joint transitions from static to dynamic states, primarily due to hydraulic actuator precision limits and assembly inaccuracies. The current control algorithm does not effectively compensate for these errors. However, the robotic arm maintains stability, successfully passes through predefined key points, and completes trajectory tasks. Despite limitations in handling transition errors, the overall performance meets the basic requirements of trajectory planning.

(2) Construction Task 2—Overhead Panel Installation: In an obstacle-free space, the Starting from the home position, the robotic arm picks up a 10 kg steel plate and installs it overhead. The suction cup takes 2 seconds to pick up the steel plate. The task requirements are that f<sub>1</sub> must be less than or equal to 50, $f _ { 2 }$ must be less than 300, and $f _ { 3 }$ must be less than 65,000. Key points are detailed in Table 5.

TABLE V  
JOINT ANGLES FOR KEY POINTS IN TASK 2 (°)

<table><tr><td>Key Point</td><td>Joint 1</td><td>Joint 2</td><td>Joint 3</td><td>Joint 4</td><td>Joint 5</td><td>Joint 6</td></tr><tr><td>Key Point 1</td><td>30.0</td><td>130.0</td><td>-60.0</td><td>0</td><td>0</td><td>0</td></tr><tr><td>Key Point 2</td><td>44.4</td><td>122.8</td><td>-20.4</td><td>15.0</td><td>14.4</td><td>10.8</td></tr><tr><td>Key Point 3</td><td>80.0</td><td>104.0</td><td>19.0</td><td>16.0</td><td>18.0</td><td>18.0</td></tr><tr><td>Key Point 4</td><td>80.0</td><td>104.0</td><td>19.0</td><td>16.0</td><td>18.0</td><td>18.0</td></tr><tr><td>Key Point 5</td><td>51.6</td><td>108.4</td><td>-24.0</td><td>14.0</td><td>13.4</td><td>10.4</td></tr><tr><td>Key Point 6</td><td>65.6</td><td>86.8</td><td>-45.6</td><td>11.4</td><td>7.2</td><td>6.8</td></tr><tr><td>Key Point 7</td><td>73.0</td><td>57.8</td><td>-47.2</td><td>0</td><td>0</td><td>0</td></tr></table>

During the Task 2 experiment, the poses of the robotic arm at each key point are shown in Figure 9.

![](Liu2025MultiObjective_figs/9232ef5ddde0468e8a5599a3e993484d0f7658e0d998760dbee0652c6f6caf4f.jpg)

![](Liu2025MultiObjective_figs/932c5464582adc1584da6ba272d5ada5196b10e12822fb204aeebb9066986f3b.jpg)  
(a) Key Point 1  
(b) Key Point 2

![](Liu2025MultiObjective_figs/eacf92badc527ca7d663273622012d609c2cecfa6784d7ee457f395388fdb4b8.jpg)

![](Liu2025MultiObjective_figs/83062e5a02e77242f49a8d0f701a4d0861af8125ab3195014d3d41d81589c605.jpg)

(c) Key Point 3 and 4  
![](Liu2025MultiObjective_figs/9bd11d47294fed7f834d26e15b2f58feb9df21d48b7460a6da3ff6e67fc9bdf9.jpg)  
(d) Key Point 5

![](Liu2025MultiObjective_figs/f9013c0b7a5c6316f12b91e6e72042d82539ebd5d14812b03ad46eba6df8e487.jpg)  
(e) Key Point 6  
(f) Key Point 7  
Fig. 9. Robotic arm poses at key points during Task 2

According to the key point requirements of Task 2, we first set the robotic arm to pass through key points 3 and 4 in 2 seconds. We then used the NSGA-III-FO algorithm to obtain the Pareto solution set. Finally, the trajectory was executed on the robotic arm experimental platform. The multiobjective optimal time vector obtained from the NSGA-III-FO algorithm is [0, 9.431, 19.334, 21.456, 34.660, 39.140, 49.043].

During Task 2, the robotic arm required more time to complete the task, resulting in reduced joint angular velocities compared to previous tasks. This adjustment significantly decreased the observed errors during transitions from static to dynamic states. The robotic arm maintained accurate adherence to the predefined trajectory, successfully passing through all key points and completing the trajectory planning task.

In Task 2 experiments, the changes in joint angles of the robotic arm and the measured angles are shown in Figure 10.

Combining the results of the two task experiments, the robotic arm’s end-effector actual trajectory closely matched the pre-simulated trajectory while satisfying all joint torque constraints. Additionally, the joint angle curves during actual motion were smooth, with no noticeable oscillations observed.

![](Liu2025MultiObjective_figs/5601827069f42097bbf1f8a14d535bb974149a46afddb62307760fd9d16e9517.jpg)

![](Liu2025MultiObjective_figs/42689a9a0c30e18cc6a41e971ab2346aad84c67765d2ff3f2b72af0bf35f16c9.jpg)

![](Liu2025MultiObjective_figs/a640327c9fa5b2ab96a377d88d440837632a065a43d4c31c99cccb34fcc0c02a.jpg)

![](Liu2025MultiObjective_figs/1538371c5d49bd5ecfe07fa5f8f03c94ef04f5d84ff56495b644b50534844c98.jpg)

![](Liu2025MultiObjective_figs/6c8f91ce5efa30f1ff7d137f61aab0651e8f62a173fb8aa75881b8cbaebce87d.jpg)

![](Liu2025MultiObjective_figs/123c0483171e71ac6f195fad6d169393d8cd4bfdf22038c08e51956f214b82ae.jpg)  
Fig. 10. Joint Angle Variations of Robotic Arm for Task 2

Smooth transitions were achieved at all key points. This verifies the effectiveness and practicality of the NSGA-III-FO algorithm in multi-objective trajectory planning.

## VII. CONCLUSIONS

In this study, we developed a robotic arm for curtain wall installation by employing a sixth-order B-spline interpolation to ensure continuous motion trajectories. Secondly, We improved the NSGA-III algorithm by introducing a focused operator, resulting in an NSGA-III-FO algorithm. Through multiple comparative experiments on the DTLZ3 and WFG3 test functions, we verified that the NSGA-III-FO algorithm significantly enhances the convergence efficiency in multiobjective optimization problems. In a real-world curtain wall installation scenario, we designed two practical tasks and used the NSGA-III-FO algorithm to solve robotic arm trajectories that satisfy multi-objective constraints. Trajectory tracking experiments confirmed high consistency between the actual and pre-simulated trajectories. The experimental results demonstrate that the NSGA-III-FO algorithm is both efficient and practical in addressing multi-objective trajectory planning for curtain wall installation robots, providing new technical pathways and support for the development of construction robotics.

## ACKNOWLEDGMENT

This work was supported in part by the National Key R&D Program of China (No.2023YFB4705002), in part by the National Natural Science Foundation of China(U20A20283), in part by the Guangdong Provincial Key Laboratory of Construction Robotics and Intelligent Construction (2022KSYS 013), in part by the CAS Science and Technology Service Network Plan (STS) - Dongguan Special Project (Grant No. 20211600200062), in part by the Science and Technology

Cooperation Project of Chinese Academy of Sciences in Hubei Province Construction 2023.

## REFERENCES

[1] N. Melenbrink, J. Werfel, and A. Menges, “On-site autonomous construction robots: Towards unsupervised building,” Automation in Construction, vol. 119, p. 103312, 2020.

[2] M. Gharbia, A. Chang-Richards, and Y. Lu, “Robotic technologies for on-site building construction: A systematic review,” Journal of Building Engineering, vol. 32, p. 101584, 2020.

[3] S. Kim, M. Peavy, and P. C. Huang, “Development of BIM-integrated construction robot task planning and simulation system,” Automation in Construction, vol. 127, p. 103720, 2021.

[4] Z. Dong, X. Zhang, and W. Yang, “Ant colony optimization-based method for energy-efficient cutting trajectory planning in axial robotic roadheader,” Applied Soft Computing, vol. 163, p. 111965, 2024.

[5] W. Wang, Q. Tao, and Y. Cao, “Robot time-optimal trajectory planning based on improved cuckoo search algorithm,” IEEE Access, vol. 8, pp. 86923–86933, 2020.

[6] J. Huang, P. Hu, and K. Wu, “Optimal time-jerk trajectory planning for industrial robots,” Mechanism and Machine Theory, vol. 121, pp. 530–544, 2018.

[7] X. Hu, H. Wu, and Q. Sun, “Robot time optimal trajectory planning based on improved simplified particle swarm optimization algorithm,” IEEE Access, vol. 11, pp. 44496–44508, 2023.

[8] X. Liu, D. Jiang, and B. Tao, “Genetic algorithm-based trajectory optimization for digital twin robots,” Frontiers in Bioengineering and Biotechnology, vol. 9, p. 793782, 2022.

[9] T. Osa, “Multimodal trajectory optimization for motion planning,” The International Journal of Robotics Research, vol. 39, no. 8, pp. 983–1001, 2020.

[10] G. Wang, W. Li, and C. Jiang, “Trajectory planning and optimization for robotic machining based on measured point cloud,” IEEE Transactions on Robotics, vol. 38, no. 3, pp. 1621–1637, 2021.

[11] J. Lee, D. Yi, and S. S. Srinivasa, “Sampling of pareto-optimal trajectories using progressive objective evaluation in multi-objective motion planning,” in 2018 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), pp. 1–9, Oct. 2018.

[12] A. Jain et al., “Anticipatory human-robot collaboration via multiobjective trajectory optimization,” in 2020 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), pp. 11052–11057, Oct. 2020.

[13] M. Brandao, M. Fallon, and I. Havoutis, “Multi-controller multiobjective locomotion planning for legged robots,” in 2019 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), pp. 4714–4721, Nov. 2019.

[14] J. Sun, X. Han, and Y. Zuo, “Trajectory planning in joint space for a pointing mechanism based on a novel hybrid interpolation algorithm and NSGA-II algorithm,” IEEE Access, vol. 8, pp. 228628–228638, 2020.

[15] Q. Shi, Z. Wang, and X. Ke, “Trajectory optimization of wall-building robots using response surface and non-dominated sorting genetic algorithm III,” Automation in Construction, vol. 155, p. 105035, 2023.

[16] X. Li, H. Lv, D. Zeng et al., “An improved multi-objective trajectory planning algorithm for kiwifruit harvesting manipulator,” IEEE Access, vol. 11, pp. 65689–65699, 2023.

[17] Z. Wang, Y. Li, K. Shuai et al., “Multi-objective trajectory planning method based on the improved elitist non-dominated sorting genetic algorithm,” Chinese Journal of Mechanical Engineering, vol. 35, no. 1, p. 7, 2022.

[18] W. Serralheiro, N. Maruyama, and F. Saggin, “Self-tuning time-energy optimization for the trajectory planning of a wheeled mobile robot,” Journal of Intelligent & Robotic Systems, vol. 95, pp. 987–997, 2019.

[19] G. Carabin and L. Scalera, “On the trajectory planning for energy efficiency in industrial robotic systems,” Robotics, vol. 9, no. 4, p. 89, 2020.

[20] K. Deb, C. L. do Val Lopes, F. V. C. Martins et al., “Identifying Pareto Fronts Reliably Using a Multistage Reference-Vector-Based Framework,” IEEE Transactions on Evolutionary Computation, vol. 28, no. 1, pp. 252–266, 2023.