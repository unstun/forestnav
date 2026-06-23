---
citation_key: Liu2025MultiObjective
arxiv_id: 2507.17140
arxiv_url: "https://arxiv.org/abs/2507.17140"
title: "Multi-Objective Trajectory Planning for a Robotic Arm in Curtain Wall Installation"
authors_short: "Xiao Liu et al."
year: 2025
direction_tag: M_multi_objective_planning
source: pymupdf4llm
converted_at: 2026-06-23T18:20:40Z
origin: ai+web
reviewed: false
---

# **Multi-Objective Trajectory Planning for a Robotic Arm in Curtain Wall Installation** 

Xiao Liu[1] , Yunxiao Cheng[1] , Weijun Wang[1] , Tianlun Huang[1] , Zhiyong Wang[1] , Wei Feng[1] _[,]_[2] _[∗]_ 

_**Abstract**_ **— In the context of labor shortages and rising costs, construction robots are regarded as the key to revolutionizing traditional construction methods and improving efficiency and quality in the construction industry. In order to ensure that construction robots can perform tasks efficiently and accurately in complex construction environments, traditional single-objective trajectory optimization methods are difficult to meet the complex requirements of the changing construction environment. Therefore, we propose a multi-objective trajectory optimization for the robotic arm used in the curtain wall installation. First, we design a robotic arm for curtain wall installation, integrating serial, parallel, and folding arm elements, while considering its physical properties and motion characteristics. In addition, this paper proposes an NSGA-III-FO algorithm (NSGA-III with Focused Operator, NSGA-III-FO) that incorporates a focus operator screening mechanism to accelerate the convergence of the algorithm towards the Pareto front, thereby effectively balancing the multi-objective constraints of construction robots. The proposed algorithm is tested against NSGA-III, MOEA/D, and MSOPS-II in ten consecutive trials on the DTLZ3 and WFG3 test functions, showing significantly better convergence efficiency than the other algorithms. Finally, we conduct two sets of experiments on the designed robotic arm platform, which confirm the efficiency and practicality of the NSGAIII-FO algorithm in solving multi-objective trajectory planning problems for curtain wall installation tasks.** 

## I. INTRODUCTION 

In the current construction landscape, construction robots are an important way to improve construction efficiency and quality[1]-[2]. Trajectory planning can ensure that robots execute construction operations optimally, thereby minimizing construction time and energy consumption. Optimizing the motion trajectory of construction robots is crucial[3]–[4]. The optimization of motion trajectories primarily involves three aspects: time[5]–[7], energy consumption[8], and joint impact[9]–[10] during motion. 

Multi-objective trajectory planning typically involves more complex tasks and constraints, and requires consideration of the priorities and resolution of conflicts between different objectives. Solving this problem has always been a popular topic in academic research[11]–[14]. [15] proposes a multi-objective trajectory optimization method based on response surface methodology (RSM) and non-dominated sorting genetic algorithm III (NSGA-III). [5] proposes a 3- 5-3 polynomial interpolation trajectory planning algorithm 

> *corresponding author. e-mail: wei.feng@siat.ac.cn 

> 1 All authors are with Shenzhen Institute of Advanced Technology, Chinese Academy of Sciences, Shenzhen, 518055, China. Contact: xiao.liu1@siat.ac.cn 

> 2 All authors are with Shenzhen University of Advanced Technology and University of Chinese Academy of Sciences, Shenzhen, 518055, China. Contact: wei.feng@siat.ac.cn 

based on an improved cuckoo search algorithm (ICS) that functions under a velocity constraint. The proposed algorithm performed well and realized a better time-optimal trajectory. [16] efficiently addressed the trajectory-planning problem for kiwifruit harvesting manipulators using multi-objective trajectory planning based on NSGA-III. [17] proposed an improved elitist non-dominated sorting genetic algorithm (INSGA-II) by introducing three genetic operators: ranking group selection (RGS), direction-based crossover (DBX), and adaptive precision-controllable mutation (APCM), which was developed to optimize travelling time and torque fluctuation. 

Most of the existing research and methods have focused on industrial robotic arms. To address the challenges faced by construction robots, such as long working hours, high energy consumption, and complex tasks, we propose a multi-objective trajectory planning method for our designed robotic arm. This method introduces a focused operator selection mechanism and a new algorithm, NSGA-III-FO (NSGA-III with Focused Operator, NSGA-III-FO), to enhance the population selection process and accelerate convergence towards the Pareto front. The proposed algorithm demonstrates significant performance advantages in convergence efficiency, effectively balancing multiple objectives to achieve solution sets that meet task requirements. 


![](1_survey/papers/md/Liu2025MultiObjective_figs/Liu2025MultiObjective.pdf-0001-12.png)


Fig. 1. Structural Design of a Robotic Arm for Curtain Wall Installation 

## II. DESIGN OF A ROBOTIC ARM FOR CURTAIN WALL INSTALLATION 

Currently, serial robots struggle to meet the high load-toweight ratio requirements for construction tasks. Leveraging the high load-bearing capacity of parallel mechanisms with redundant actuation and the superior workspace characteristics of serial mechanisms, we design a robotic arm for curtain wall installation. The proposed arm includes a folding arm, a serial-parallel arm, and an end effector, as illustrated in Figure 1. The folding arm consists of a base platform, 

two support arms, three hydraulic cylinders, and an end platform. The serial-parallel arm comprises three 2-DOF parallel mechanisms connected in series, each containing three hydraulic cylinders(two active axes and one passive axis). All joints are driven by hydraulic cylinders. The entire robotic arm has six degrees of freedom and can perform compliant operations over a 150-degree range. The wrist motor enables ±360-degree rotation of the end effector. The end effector consists of four suction cups and a suction cup frame, controlled by a solenoid valve for overall air circuit switching, designed for glass handling. 

## III. TRAJECTORY PLANNING 

## _A. Sixth-Order B-Spline Interpolation Trajectory_ 

Mapping from Task Space to Joint Space: To execute predefined trajectory tasks, B-spline curves define the trajectory in task space. Key points _Pn_ are determined based on the velocity requirements, where _n_ denotes the sequence number of key points. Moving from the initial point _P_ 0 to the final point _Pn_ in task space, a series of key points in joint space can be obtained via inverse kinematics algorithms. 


![](1_survey/papers/md/Liu2025MultiObjective_figs/Liu2025MultiObjective.pdf-0002-04.png)


In the equations: _i_ denotes the joint of the robotic arm; _qin_ represents the joint angle at key point _n_ for joint _i_ , and _tn_ indicates the time at which the trajectory passes through key point _Pin_ . To construct a sixth-order B-spline curve based on the given key points, ensuring that each joint trajectory passes through these points _p_ ( _x_ ), B-spline interpolation is used to determine the control points that make the curve pass through these specified points. 

To ensure that the robotic arm’s joints pass through _n_ + 1 key points, we have: 


![](1_survey/papers/md/Liu2025MultiObjective_figs/Liu2025MultiObjective.pdf-0002-07.png)


Where: _d j_ denotes the control points; _x_ is the knot vector, where _xi_ +6 _∈_ [ _x_ 6 _, xi_ +6]; _j_ isthe parameter of the B-spline curve; _N j,_ 6( _x_ ) is the 6th-order normalized B-spline basis function, which depends on the vector _x_ and is constructed recursively. The constraint function can be expressed as: 


![](1_survey/papers/md/Liu2025MultiObjective_figs/Liu2025MultiObjective.pdf-0002-09.png)


In the equations: _vs_ and _ve_ represent the initial and final velocities of the joint; _as_ and _ve_ represent the initial and finaland finalaccelerationsjerk of theof joint.the joint; **P**[˙] ( _x_ ) _j_ , _s_ **P**[¨] and( _x_ ), _j_ and _e_ represent **P** ... ( _x_ ) denotethe initialthe first, second, and third derivatives of the B-spline curve, respectively. The velocity, acceleration, and jerk for each joint in a sixth-order B-spline can be expressed as: 


![](1_survey/papers/md/Liu2025MultiObjective_figs/Liu2025MultiObjective.pdf-0002-11.png)



![](1_survey/papers/md/Liu2025MultiObjective_figs/Liu2025MultiObjective.pdf-0002-12.png)


## _B. Multi-Objective Trajectory Planning_ 

In real-world construction scenarios, energy consumption optimization is crucial for robots powered by batteries or generators. Joint impact optimization can reduce wear and tear on mechanical joints, thereby extending the robot lifespan. A high efficiency is also essential for the construction process. Therefore, the optimization objectives are time, joint impact, and energy consumption. Define the time evaluation function _f_ 1, joint impact evaluation function _f_ 2, and energy consumption evaluation function _f_ 3 as follows: 


![](1_survey/papers/md/Liu2025MultiObjective_figs/Liu2025MultiObjective.pdf-0002-15.png)


In the equations: _K_ and _k_ represent the total number of sampling points and the number of sampling points, respectively; _ji_ is the angular jerk of joint _i_ ; _ωi_ is the angular velocity of joint _i_ ; _τi_ is the output torque of joint _i_ . The motion constraints for the robotic arm are defined as follows: 


![](1_survey/papers/md/Liu2025MultiObjective_figs/Liu2025MultiObjective.pdf-0002-17.png)


where: _τi_ max, _ji_ max, _ωi_ max, _vi_ max is the maximum torque, the maximum angular jerk, the maximum angular velocity, and the maximum linear velocity of joint _i_ . 

## IV. NSGA-III-FO MULTI-OBJECTIVE OPTIMIZATION ALGORITHM WITH FOCUS OPERATOR 

Researchers commonly employ heuristic multi-objective optimization algorithms to address robotic arm trajectory planning problems [18]–[19], aiming to find an optimal set of solutions that balance various performance metrics. NSGA-III is a multi-objective optimization algorithm [20] that utilizes a reference-point-based strategy to decompose the objective space, allowing each reference point to correspond with multiple solutions. However, NSGA-III overlooks the efficiency of converging towards the Pareto front. To enhance the convergence performance, we propose an enhanced version of NSGA-III named NSGA-III-FO(NSGA-III with Focused Operator, NSGA-III-FO). This algorithm introduces focused and non-focused operators to accelerate population screening, thereby improving the overall convergence efficiency. 

## _A. NSGA-III-FO Algorithm_ 

The fundamental idea of the NSGA-III-FO algorithm is to iteratively generate a set of non-dominated solutions, where each non-dominated solution approximates an optimal solution. In each iteration, the algorithm creates a new initial population based on the non-dominated solutions from the current solution set. The algorithm first selects individuals using focused operators for inclusion in the next generation, while directly excluding those selected by non-focused operators. The remaining individuals are then subjected to non-dominated sorting to form the next generation solution set. This process continuously optimizes multiple objective functions simultaneously, ultimately yielding an optimal set of target allocation schemes. The optimization flowchart is illustrated in Figure 2. 


![](1_survey/papers/md/Liu2025MultiObjective_figs/Liu2025MultiObjective.pdf-0003-02.png)


Fig. 2. Flowchart of NSGA-III-FO for Multi-objective Optimization) 

The specific solution steps of the NSGA-III-FO algorithm are as follows: 

(1) Randomly initialize an initial population _Pt_ of size N, construct a reference plane based on boundary crossover, for m objective optimization functions, divide into p on the m- dimensional standardized hyperplane, and uniformly generate H reference points. The calculation method is as follows: 


![](1_survey/papers/md/Liu2025MultiObjective_figs/Liu2025MultiObjective.pdf-0003-06.png)


(2) In the initial population _Pt_ , select the individual with the smallest Euclidean distance from the reference plane as the focused operator, which directly enters the offspring population, and select the individual with the largest Euclidean distance from the reference plane as the non-focused operator to be directly excluded. 

(3) The remaining individuals undergo non-dominated sorting, and the better individuals are selected from the sorting results to undergo crossover and mutation operations. The crossover probability and mutation probability are calculated as follows: 


![](1_survey/papers/md/Liu2025MultiObjective_figs/Liu2025MultiObjective.pdf-0003-09.png)


In the formula, _Pc.max_ and _Pc.min_ represent the maximum and minimum values of the set crossover probability, respectively, while _Pm.max_ and _Pm.min_ represent the maximum and minimum values of the set mutation probability, respectively. _f_ is the average fitness function value of the current solution, and _fmax_ and _fmin_ are the maximum and minimum values of the fitness function for the current solution, respectively. After crossover and mutation produce offspring populations _Qt_ , both populations are combined to form a new offspring population _Rt_ of size 2 _N_ . 

(4) Perform rapid non-domination sorting, retaining excellent and diverse individuals according to the non-domination relationship, forming a new parent population _Pt_ +1. 

(5) Generate a new offspring population _Qt_ +1 through basic operations of genetic algorithms, merge _Pt_ +1 with _Qt_ +1 to form a new population _R_ , repeat these operations until reaching the designated number of generations. 

## _B. Performance Testing of the NSGA-III-FO Algorithm_ 

The NSGA-III-FO algorithm is used to conduct ten comparative tests against the NSGA-III, MOEA/D, and MSOPS-II algorithms on the DTLZ3 and WFG3 test functions. DTLZ3 and WFG3, as classic benchmark functions in multiobjective optimization, are widely used to evaluate the algorithm performance. Their standardized status ensures fair assessment. Using these recognized benchmarks facilitates an effective comparison with the existing algorithms. An important performance evaluation metric in multi-objective optimization problems is the Inverse Generational Distance (IGD). This metric measures the distance between the nondominated solution set generated by the algorithm and the reference non-dominated solution set, thereby evaluating the performance of the algorithm. The smaller the IGD value, the closer the non-dominated solution set generated by the algorithm is to the reference non-dominated solution set, indicating better algorithm performance. The calculation method is: 


![](1_survey/papers/md/Liu2025MultiObjective_figs/Liu2025MultiObjective.pdf-0003-15.png)


In the formula, _P_ represents the non-dominated point set in the target space; _P[∗]_ represents the uniformly distributed points on the true Pareto frontier; _|P|_ represents the number of solutions in set _P_ ; _d_ ( _Pi, P[∗]_ ) represents the Euclidean distance 

TABLE I 

COMPARISON OF IGD VALUES AMONG NSGA-III-FO AND OTHER MULTI-OBJECTIVE ALGORITHMS 

|Test Function|NSGA-III|MSOPS-II|MOEA/D|NSGA-III-FO|
|---|---|---|---|---|
|DTLZ3<br>WFG3|343.9±24.9<br>0.6122±0.038|352.4±28.0<br>0.7547±0.048|387.1±23.8<br>0.6932±0.051|341.3±25.3<br>0.6087±0.028|



between the solution _Pi_ and _P[∗]_ in the target space. The calculation result is shown in the table below: 

The hypervolume(HV)is an important metric for evaluating the quality of Pareto solution sets in multi-objective optimization algorithms. It measures the volume enclosed by the Pareto front and a reference point. Hypervolume can simultaneously reflect the convergence and diversity of the solution set. The hypervolume convergence curves for the DTLZ3 and WFG3 test functions, using the origin as the reference point in the Pareto solution space, are shown in the following figure: From 


![](1_survey/papers/md/Liu2025MultiObjective_figs/Liu2025MultiObjective.pdf-0004-05.png)


Fig. 3. The HV Convergence Curves of Each Algorithm (Shaded Areas Indicate Standard Deviation Ranges) 

Figure 3 and Table 2, it can be observed that when the number of iterations is 20,000, the HV value of MSOPS-II for the DTLZ3 test function is only 63.6% of that of NSGA-III-FO, while other algorithms have not yet found effective solutions. When the number of iterations reaches 50,000, the HV values of NSGA-III-FO, NSGA-III, and MSOPS-II tend to converge and their results are close, while the curve of MOEA/D has not yet converged. By analyzing the calculation results of IGD values, it is evident that NSGA-III-FO exhibits better convergence and stability. 

In the WFG3 test function, at 10,000 iterations, the HV values of NSGA-III-FO, NSGA-III, and MSOPS-II have approached convergence, with NSGA-III-FO exhibiting the smallest standard deviation and stable convergence. In terms of IGD values, NSGA-III-FO outperforms the other three algorithms, with significantly lower average values. Although NSGA-III also performs well on WFG3, it still falls short compared to NSGA-III-FO. 

## V. MULTI-OBJECTIVE TRAJECTORY PLANNING SIMULATION BASED ON NSGA-III-FO ALGORITHM 

We use the number of iterations as a convergence metric, where convergence speed reflects algorithm efficiency rather than absolute runtime. In task space, trajectories are defined using B-spline curves, and key points in the sequence of 

poses are determined based on trajectory task requirements. We set seven key points during the motion process, as shown in Table 2. 

TABLE II 

SETTING KEY POINTS 

||Node|Joint 1|Joint 2|Joint 3|Joint 4|Joint 5|Joint 6|
|---|---|---|---|---|---|---|---|
||1<br>2<br>3|43.35<br>46.35<br>55.04|78.54<br>86.43<br>99.62|-90.05<br>-56.68<br>-39.25|0<br>1.68<br>4.71|0<br>1.31<br>3.65|0<br>0.68<br>2.71|
||4|62.67|104.06|-21.94|6.51|5.53|4.64|
||5<br>6<br>7|68.04<br>74.40<br>84.13|112.40<br>124.5<br>133.6|-9.04<br>1.68<br>12.81|8.14<br>12.8<br>16.14|6.99<br>8.18<br>10.15|6.53<br>7.31<br>9.21|



Based on the dynamic parameters of a foldable serialparallel robotic arm, we use the NSGA-III-FO algorithm to optimize the time function _f_ 1, impact function _f_ 2, and energy consumption function _f_ 3 through simulation. The multi-objective optimization trajectory Pareto solution set was obtained, as shown in Figure 4: 


![](1_survey/papers/md/Liu2025MultiObjective_figs/Liu2025MultiObjective.pdf-0004-16.png)


Fig. 4. Pareto Solution Set of Multi-objective Optimized Trajectories Based on NSGA-III-FO Algorithm 

As shown in Figure 4, A, B, and C represent the optimal solutions for _f_ 1, _f_ 2, and _f_ 3, respectively. It can be observed that _f_ 1 and _f_ 2 exhibit a negative correlation, while the relationship between _f_ 1 and _f_ 3 is more complex but generally also shows a negative correlation. The time vectors of the optimal solutions for the objective functions _f_ 1, _f_ 2, and _f_ 3, along with their corresponding function values, are shown in Table 3. The time vectors are the collection of time points corresponding to the seven key points in the motion process. 

The Pareto front of the solution set is observed to exhibit uniform distribution and good diversity. When applying the robotic arm to practical work requirements, different weights can be set for time, energy consumption, and joint impact metrics, allowing the selection of a multi-objective optimal solution that best meets the requirements. Additionally, the 

## TABLE III 

TIME VECTORS AND CORRESPONDING OBJECTIVE FUNCTION VALUES 

|Plan|Time Vector(s)|_f_1 (s)|_f_2 (N)|_f_3 (J)|
|---|---|---|---|---|
|A|[0, 2.01, 3.77, 5.79, 6.53, 8.85, 10.48]|10.48|900.87|45.89|
|B|[0, 3.51, 7.34, 10.91, 13.31, 15.32, 18.94]|18.94|362.25|10.95|
|C|[0, 1.51, 5.09, 10.23, 15.67, 18.98, 23.27]|23.27|443.33|6.40|



NSGA-III, MOEA/D, and NSGA-II algorithms are used for trajectory planning of the robotic arm with _f_ 1, _f_ 2, and _f_ 3 as the objective functions, and compared with the NSGA-III-FO algorithm in terms of the HV metric. The convergence curves are shown in Figure 5. 


![](1_survey/papers/md/Liu2025MultiObjective_figs/Liu2025MultiObjective.pdf-0005-04.png)


Fig. 5. HV Indicator of Multi-objective Trajectory Planning Solutions for the robotic arm 

The experimental results show that the NSGA-III-FO algorithm demonstrates a clear advantage in convergence rate, further validating its potential and effectiveness in exploring the solution space. 

## VI. EXPERIMENT ON MULTI-OBJECTIVE TRAJECTORY PLANNING 

## _A. Robotic Arm Experimental Platform_ 

The curtain wall installation robotic arm we developed primarily consists of a folding arm, a serial-parallel manipulator, and an end effector. The folding arm is configured with three joints: Joint 1, Joint 2, and Joint 3. The serial-parallel manipulator is restricted to three degrees of freedom in the vertical plane, designated as Joint 4, Joint 5, and Joint 6. The experimental platform for the curtain wall installation robotic arm.is shown in Figure 6. 

## _B. Experiment_ 

We designed two construction tasks based on real-world scenarios to perform trajectory planning for the robotic arm. Utilizing the NSGA-III-FO algorithm, we successfully obtained solution sets that best met the task requirements. The feasibility of these solution sets was verified through experiments. 


![](1_survey/papers/md/Liu2025MultiObjective_figs/Liu2025MultiObjective.pdf-0005-12.png)


Fig. 6. Robotic Arm Experimental Platform for Curtain Wall Installation Trajectory Planning 

(1)Construction Task 1—Vertical Surface Installation: The task space is obstacle-free. Starting from the home position, the robotic arm picks up the steel plate and then transports it to the target position on a vertical surface directly in front of the arm. The steel plate weighs 10 kg and is picked up using four suction cups in 2 seconds. The task requirements are that _f_ 1 must be less than 40, _f_ 2 must be less than 1000, and _f_ 3 is not specified. Key points are detailed in Table 4. 

TABLE IV 

JOINT ANGLES FOR KEY POINTS IN TASK 1 (°) 

||**Key Point**|**Joint 1**|**Joint 2**|**Joint 3**|**Joint 4**|**Joint 5**|**Joint 6**|
|---|---|---|---|---|---|---|---|
||Key Point 1|30.0|130.0|-60.0|0|0|0|
||Key Point 2<br>Key Point 3|37.2<br>73.2|126.4<br>119.2|-16.8<br>19.2|6.8<br>14.7|8.8<br>15.8|10.4<br>16.0|
||Key Point 4|80.0|104.0|19.0|16.0|18.0|18.0|
||Key Point 5<br>Key Point 6<br>Key Point 7|80.0<br>61.2<br>57.2|104.0<br>108.4<br>103.6|19.0<br>-1.6<br>-12.8|16.0<br>12.8<br>10.0|18.0<br>11.8<br>10.0|18.0<br>10.8<br>10.0|



The robotic arm’s poses at key points during the experiment are shown in Figure 7. 

According to the key point requirements of Task 1, we first set the robotic arm to pass through key points 4 and 5 in 2 seconds. Next, we used the NSGA-III-FO algorithm to obtain the Pareto solution set. Finally, the trajectory was executed on the robotic arm platform. The time-optimal solution vector obtained from the NSGA-III-FO algorithm is [0, 7.744, 15.307, 22.863, 30.976, 38.720]. 

During Task 1 experiments, the changes in joint angles of 


![](1_survey/papers/md/Liu2025MultiObjective_figs/Liu2025MultiObjective.pdf-0006-00.png)


than or equal to 50, _f_ 2 must be less than 300, and _f_ 3 must be less than 65,000. Key points are detailed in Table 5. 

TABLE V 

JOINT ANGLES FOR KEY POINTS IN TASK 2 (°) 

|**Key Point**|**Joint 1**|**Joint 2**|**Joint 3**|**Joint 4**|**Joint 5**|**Joint 6**|
|---|---|---|---|---|---|---|
|Key Point 1|30.0|130.0|-60.0|0|0|0|
|Key Point 2|44.4|122.8|-20.4|15.0|14.4|10.8|
|Key Point 3|80.0|104.0|19.0|16.0|18.0|18.0|
|Key Point 4|80.0|104.0|19.0|16.0|18.0|18.0|
|Key Point 5|51.6|108.4|-24.0|14.0|13.4|10.4|
|Key Point 6|65.6|86.8|-45.6|11.4|7.2|6.8|
|Key Point 7|73.0|57.8|-47.2|0|0|0|



During the Task 2 experiment, the poses of the robotic arm at each key point are shown in Figure 9. 

Fig. 7. Robotic arm poses at key points during Task 1. 

the robotic arm and the measured joint angles are compared in Figure 8. 


![](1_survey/papers/md/Liu2025MultiObjective_figs/Liu2025MultiObjective.pdf-0006-08.png)


Fig. 8. Joint Angle Variations of Robotic Arm for Task 1 

In trajectory planning experiments, significant errors occurred during joint transitions from static to dynamic states, primarily due to hydraulic actuator precision limits and assembly inaccuracies. The current control algorithm does not effectively compensate for these errors. However, the robotic arm maintains stability, successfully passes through predefined key points, and completes trajectory tasks. Despite limitations in handling transition errors, the overall performance meets the basic requirements of trajectory planning. 

(2) Construction Task 2—Overhead Panel Installation: In an obstacle-free space, the Starting from the home position, the robotic arm picks up a 10 kg steel plate and installs it overhead. The suction cup takes 2 seconds to pick up the steel plate. The task requirements are that _f_ 1 must be less 


![](1_survey/papers/md/Liu2025MultiObjective_figs/Liu2025MultiObjective.pdf-0006-12.png)


Fig. 9. Robotic arm poses at key points during Task 2 

According to the key point requirements of Task 2, we first set the robotic arm to pass through key points 3 and 4 in 2 seconds. We then used the NSGA-III-FO algorithm to obtain the Pareto solution set. Finally, the trajectory was executed on the robotic arm experimental platform. The multiobjective optimal time vector obtained from the NSGA-IIIFO algorithm is [0, 9.431, 19.334, 21.456, 34.660, 39.140, 49.043]. 

During Task 2, the robotic arm required more time to complete the task, resulting in reduced joint angular velocities compared to previous tasks. This adjustment significantly decreased the observed errors during transitions from static to dynamic states. The robotic arm maintained accurate adherence to the predefined trajectory, successfully passing through all key points and completing the trajectory planning task. 

In Task 2 experiments, the changes in joint angles of the robotic arm and the measured angles are shown in Figure 10. 

Combining the results of the two task experiments, the robotic arm’s end-effector actual trajectory closely matched the pre-simulated trajectory while satisfying all joint torque constraints. Additionally, the joint angle curves during actual motion were smooth, with no noticeable oscillations observed. 


![](1_survey/papers/md/Liu2025MultiObjective_figs/Liu2025MultiObjective.pdf-0007-00.png)


Fig. 10. Joint Angle Variations of Robotic Arm for Task 2 

Smooth transitions were achieved at all key points. This verifies the effectiveness and practicality of the NSGA-III-FO algorithm in multi-objective trajectory planning. 

## VII. CONCLUSIONS 

In this study, we developed a robotic arm for curtain wall installation by employing a sixth-order B-spline interpolation to ensure continuous motion trajectories. Secondly, We improved the NSGA-III algorithm by introducing a focused operator, resulting in an NSGA-III-FO algorithm. Through multiple comparative experiments on the DTLZ3 and WFG3 test functions, we verified that the NSGA-III-FO algorithm significantly enhances the convergence efficiency in multiobjective optimization problems. In a real-world curtain wall installation scenario, we designed two practical tasks and used the NSGA-III-FO algorithm to solve robotic arm trajectories that satisfy multi-objective constraints. Trajectory tracking experiments confirmed high consistency between the actual and pre-simulated trajectories. The experimental results demonstrate that the NSGA-III-FO algorithm is both efficient and practical in addressing multi-objective trajectory planning for curtain wall installation robots, providing new technical pathways and support for the development of construction robotics. 

## ACKNOWLEDGMENT 

This work was supported in part by the National Key R&D Program of China (No.2023YFB4705002), in part by the National Natural Science Foundation of China(U20A20283), in part by the Guangdong Provincial Key Laboratory of Construction Robotics and Intelligent Construction (2022KSYS 013), in part by the CAS Science and Technology Service Network Plan (STS) - Dongguan Special Project (Grant No. 20211600200062), in part by the Science and Technology 

Cooperation Project of Chinese Academy of Sciences in Hubei Province Construction 2023. 

## REFERENCES 

- [1] N. Melenbrink, J. Werfel, and A. Menges, “On-site autonomous construction robots: Towards unsupervised building,” Automation in Construction, vol. 119, p. 103312, 2020. 

- [2] M. Gharbia, A. Chang-Richards, and Y. Lu, “Robotic technologies for on-site building construction: A systematic review,” Journal of Building Engineering, vol. 32, p. 101584, 2020. 

- [3] S. Kim, M. Peavy, and P. C. Huang, “Development of BIM-integrated construction robot task planning and simulation system,” Automation in Construction, vol. 127, p. 103720, 2021. 

- [4] Z. Dong, X. Zhang, and W. Yang, “Ant colony optimization-based method for energy-efficient cutting trajectory planning in axial robotic roadheader,” Applied Soft Computing, vol. 163, p. 111965, 2024. 

- [5] W. Wang, Q. Tao, and Y. Cao, “Robot time-optimal trajectory planning based on improved cuckoo search algorithm,” IEEE Access, vol. 8, pp. 86923–86933, 2020. 

- [6] J. Huang, P. Hu, and K. Wu, “Optimal time-jerk trajectory planning for industrial robots,” Mechanism and Machine Theory, vol. 121, pp. 530–544, 2018. 

- [7] X. Hu, H. Wu, and Q. Sun, “Robot time optimal trajectory planning based on improved simplified particle swarm optimization algorithm,” IEEE Access, vol. 11, pp. 44496–44508, 2023. 

- [8] X. Liu, D. Jiang, and B. Tao, “Genetic algorithm-based trajectory optimization for digital twin robots,” Frontiers in Bioengineering and Biotechnology, vol. 9, p. 793782, 2022. 

- [9] T. Osa, “Multimodal trajectory optimization for motion planning,” The International Journal of Robotics Research, vol. 39, no. 8, pp. 983–1001, 2020. 

- [10] G. Wang, W. Li, and C. Jiang, “Trajectory planning and optimization for robotic machining based on measured point cloud,” IEEE Transactions on Robotics, vol. 38, no. 3, pp. 1621–1637, 2021. 

- [11] J. Lee, D. Yi, and S. S. Srinivasa, “Sampling of pareto-optimal trajectories using progressive objective evaluation in multi-objective motion planning,” in 2018 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), pp. 1–9, Oct. 2018. 

- [12] A. Jain et al., “Anticipatory human-robot collaboration via multiobjective trajectory optimization,” in 2020 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), pp. 11052–11057, Oct. 2020. 

- [13] M. Brandao, M. Fallon, and I. Havoutis, “Multi-controller multiobjective locomotion planning for legged robots,” in 2019 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), pp. 4714–4721, Nov. 2019. 

- [14] J. Sun, X. Han, and Y. Zuo, “Trajectory planning in joint space for a pointing mechanism based on a novel hybrid interpolation algorithm and NSGA-II algorithm,” IEEE Access, vol. 8, pp. 228628–228638, 2020. 

- [15] Q. Shi, Z. Wang, and X. Ke, “Trajectory optimization of wall-building robots using response surface and non-dominated sorting genetic algorithm III,” Automation in Construction, vol. 155, p. 105035, 2023. 

- [16] X. Li, H. Lv, D. Zeng et al., “An improved multi-objective trajectory planning algorithm for kiwifruit harvesting manipulator,” IEEE Access, vol. 11, pp. 65689–65699, 2023. 

- [17] Z. Wang, Y. Li, K. Shuai et al., “Multi-objective trajectory planning method based on the improved elitist non-dominated sorting genetic algorithm,” Chinese Journal of Mechanical Engineering, vol. 35, no. 1, p. 7, 2022. 

- [18] W. Serralheiro, N. Maruyama, and F. Saggin, “Self-tuning time-energy optimization for the trajectory planning of a wheeled mobile robot,” Journal of Intelligent & Robotic Systems, vol. 95, pp. 987–997, 2019. 

- [19] G. Carabin and L. Scalera, “On the trajectory planning for energy efficiency in industrial robotic systems,” Robotics, vol. 9, no. 4, p. 89, 2020. 

- [20] K. Deb, C. L. do Val Lopes, F. V. C. Martins et al., “Identifying Pareto Fronts Reliably Using a Multistage Reference-Vector-Based Framework,” IEEE Transactions on Evolutionary Computation, vol. 28, no. 1, pp. 252–266, 2023. 

