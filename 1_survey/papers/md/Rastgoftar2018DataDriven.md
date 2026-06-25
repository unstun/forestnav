---
citation_key: Rastgoftar2018DataDriven
arxiv_id: 1805.09951
arxiv_url: https://arxiv.org/abs/1805.09951
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-24T17:00:11Z
origin: ai+web
reviewed: false
---

# Introduction

Success in autonomous off-road driving will be assured in part through the use of diverse static and real-time data sources in planning and control decisions. A vehicle traversing complex terrain over a long distance must define a route that balances efficiency with safety. Off-road driving requires including both global and local metrics in path planning. Algorithms such as A\* and D\* [@duchovn2014path] for waypoint definition and sequencing can be combined with local path planning strategies [@latombe2012robot] to guarantee obstacle avoidance given system motion constraints and terrain properties such as slope and surface composition.

Off-road navigation studies to-date have primarily focused on avoiding obstacles and improving local driving paths. A\* [@gaw1986minimum] and dynamic programming [@zhao2014optimizing] support globally-optimal planning over a discrete grid or pre-defined waypoint set. In Ref. [@karumanchi2010non], the surface slope is considered during A\* search over a grid-based mobility map. Slope is used to assign feasible traversal velocity constraints that maintain acceptable risk of loss-of-control (e.g., spin-out) or roll-over. In Ref. [@chu2012local], local driving path optimization is studied, while Ref. [@chu2015real] applies a Pythagorean Hodograph (PH) [@farouki1990pythagorean] cubic curve to provide a smooth path that avoids obstacles by generating a kinematic graph data structure. Vehicle models that consider continuously-variable (rough) terrain are introduced in Refs. [@howard2007optimal], [@shiller1990optimal], [@shiller1991dynamic], [@amar1993modeling] and [@bonnafous2001motion].

This paper proposes a data-driven approach to autonomous vehicle motion planning and control for off-road driving scenarios. The decision-making architecture consists of three layers: (i) Global Route Planning (GRP), (ii) Local Path Planning (LPP), and (iii) Feedback Control (FC). The GRP planning layer assigns optimal waypoints using dynamic programming (DP) [@bertsekas1995dynamic; @zolfpour2014modeling]. The GRP must rely on cloud and stored database information to define and sequence waypoints beyond onboard sensor range (line-of-sight). In this paper, DP cost is defined based on realistic weather and geographic data provided by the National Center for Environmental Information in the National Oceanographic and Atmospheric Administration (NOAA) along with geographical information system (GIS) data. The LPP computes a continuous-time trajectory between optimal waypoints assigned by the GRP. The FC applies a nonlinear controller to asymptotically track desired vehicle trajectory. To our knowledge, this is the first publication in which NOAA weather and GIS data provide input into autonomous off-road driving decision-making.

Autonomous off-road driving has been proposed for multiple applications. The DARPA Grand Challenge series and PerceptOR program have led to numerous advances in perception and autonomous driving decision-making. For example, Ref. [@kelly2006toward] proposes a three-tier deliberative, perception, reaction architecture to navigate an off-road cluttered environment with limited GPS availability and changing lighting conditions. A review of navigation or perception systems relevant to agricultural applications is provided in Ref. [@mousazadeh2013technical]. Because agriculture equipment normally operates in open fields with minimal slope, precision driving and maneuvering tends to be more important than evaluating field traversability. Ref. [@reina2016lidar] describes how LIDAR and stereo video data can be fused to support off-road vehicle navigation, providing critical real-time traversability information for the area within range of sensors. To augment LIDAR and vision with information on soil conditions, Ref. [@gonzalez2017thermal] proposes use of a thermal camera to provide real-time measurements of soil moisture content, which in turn can be used to assess local traversability. Our paper provides complementary work that incorporates GIS and cloud-based (NOAA) data sources to enable an off-road vehicle planner to build a traversable and efficient route through complex off-road terrain. Onboard sensors would then provide essential feedback to confirm the planned route is safe and update database-indicated traversability conditions as needed.

A second contribution of this paper is a feedback linearization controller for trajectory tracking over nonlinear surfaces. Most literature on vehicle control and trajectory tracking usually assumes that the car moves on a flat surface [@hwan2013optimal; @kong2015kinematic; @ryu2004integrating; @brown2017safe]. In Ref. [@brown2017safe], model predictive controller (MPC) is deployed for trajectory tracking and motion control on flat surfaces. Ref. [@howard2007optimal] introduces a vehicle body frame for motion over a nonlinear surface and realizes velocity with respect to the local coordinate frame. Bases of the body and ground (world) coordinate system are related through Euler angles $\phi$, $\theta$, $\psi$. A first-order kinematic model for motion over a nonlinear surface is presented in Ref. [@howard2007optimal].

In this paper, we extend the kinematic car model given in Refs. [@paden2016survey; @kwatny2000nonlinear] by including both position and velocity as control states. The car is modeled by two wheels connected by a rigid bar. Side-slip of the rear car wheel (axle) is presumed zero. Car tangent acceleration (drive torque) and steering rate control inputs are chosen such that the desired trajectory on a nonlinear motion surface is asymptotically tracked.

This paper is organized as follows. Section [2](#Preliminaries){reference-type="ref" reference="Preliminaries"} presents background on dynamic programming, deterministic state machines, and ground vehicle (car) kinematics. Section [3](#Methodology){reference-type="ref" reference="Methodology"} describes the paper's methodology, followed by off-road driving simulation results in Section [4](#Simulation Results){reference-type="ref" reference="Simulation Results"}. Section [5](#Conclusion){reference-type="ref" reference="Conclusion"} concludes the paper.

# Preliminaries {#Preliminaries}

Three motion planning and control layers are integrated to enable off-road autonomous driving. The top layer is \"global route planning\" (GRP) using dynamic programming (DP) as reviewed in Section [2.1](#Dynamic Programming){reference-type="ref" reference="Dynamic Programming"}. The second layer, local path planning (LPP), assigning a continuous-time vehicle trajectory to waypoints sequenced by the GRP via path and speed planning computations. The paper defines a deterministic finite state machine (DFSM) [@hopcroft2006automata] to specify desired speed along the desired path. Elements of a DFSM are defined in Section [2.2](#Deterministic Finite State Machine){reference-type="ref" reference="Deterministic Finite State Machine"}. The paper presents a nonlinear feedback control approach for trajectory tracking over an arbitrary motion surface as the inner-loop (third) layer. Motion of the car is expressed in coordinate frames defined in Section [2.3](#Local and Ground Coordinate Systems){reference-type="ref" reference="Local and Ground Coordinate Systems"} using driving dynamics given in Section [2.4](#Ego Car Dynamics){reference-type="ref" reference="Ego Car Dynamics"}.

## Dynamic Programming {#Dynamic Programming}

A dynamic programming (DP) problem [@bertsekas1995dynamic] can be defined by the tuple $$\left(\mathcal{S}, \mathcal{A}, \mathcal T, \mathcal C\right)$$ where $\mathcal{S}$ is a set of discrete states with cardinality $N$, and $\mathcal{A}$ is the set of discrete actions with cardinality $n_a$. Furthermore, $\mathcal{C}:\mathcal{S}\times \mathcal{A}\rightarrow \mathbb{R}$ is the cost function and $\mathcal{T}:\mathcal{S}\times \mathcal{A}\rightarrow \mathcal{S}$ is a deterministic transition function.

The Bellman Equation defines optimality with respect to action $a^*(s)\in \mathcal{A}$ selected for each state $s$: $$\begin{equation}
    \mathcal{V}(s)=\min\limits_{\forall a\in \mathcal{A},\forall s'\in \mathcal{S}}\{C(s,a)+\mathcal{T}(s,a,s')V(s')\}
\end{equation}$$ where $\mathcal{V}:\mathcal{S}\rightarrow \mathbb{R}$ is the utility or value function. Therefore, $$\begin{equation}
    a^*(s)=\mathop{\mathrm{\arg\!\min}}\limits_{\forall a\in \mathcal{A},\forall s'\in \mathcal{S}}\{C(s,a)+\mathcal{T}(s,a,s')V(s')\}
\end{equation}$$ assigns the optimal action for each state $s\in \mathcal{S}$. Case study simulations in this paper use a traditional value iteration algorithm [@puterman2014markov] to solve the Bellman equation.

## Deterministic Finite State Machine {#Deterministic Finite State Machine}

The behavior of a discrete system can be represented by a directed graph formulated as a *finite state machine* (FSM). In a FSM, nodes represent discrete states of the system and edges assign transitions between states. A FSM is *deterministic* if a unique input signal always returns the same result. A deterministic finite state machine (DFSM) [@hopcroft2006automata] is mathematically defined by the tuple $$\left(\Sigma,\mathcal P, \mathcal F, \Delta, p_0\right)$$ where $\Sigma$ is a finite set of inputs, $\mathcal P$ is the finite set of states, $\mathcal F$ is the set of terminal states, $\Delta:\mathcal P\times \Sigma \rightarrow \mathcal P$ defines transitions over the DFSM states, and $p_0$ is the initial state.

![Off-road driving coordinate frames.](Rastgoftar2018DataDriven_figs/carbodyframeeee.jpg){#carbodyframe width="3 in"}

## Motion Kinematics {#Local and Ground Coordinate Systems}

### Ground Coordinate System

Bases of a ground-fixed or inertial coordinate system are denoted $\hat{\mathbf{i}}_G$, $\hat{\mathbf{j}}_G$, and $\hat{\mathbf{k}}_G$, where $\hat{\mathbf{i}}_G$ and $\hat{\mathbf{j}}_G$ locally point East and North, respectively. Position of the vehicle can be expressed with respect to ground coordinate system $G$ by $$\begin{equation}
    \mathbf{r}=x\hat{\mathbf{i}}_G+y\hat{\mathbf{j}}_G+z\hat{\mathbf{k}}_G
\end{equation}$$ Because the ground coordinate system is stationary, $\dot{\mathbf{i}}_G=\mathbf{0}$, $\dot{\mathbf{j}}_G=\mathbf{0}$, and $\dot{\mathbf{k}}_G=\mathbf{0}$. Velocity and accelration are assigned by $$\begin{equation}
\label{VELACC}
\begin{split}
    \dot{\mathbf{r}}=&\dot{x}\hat{\mathbf{i}}_G+\dot{y}\hat{\mathbf{j}}_G+\dot{z}\hat{\mathbf{k}}_G\\
    \ddot{\mathbf{r}}=&\ddot{x}\hat{\mathbf{i}}_G+\ddot{y}\hat{\mathbf{j}}_G+\ddot{z}\hat{\mathbf{k}}_G\\
\end{split}
\end{equation}$$

It is assumed that the vehicle (car) moves on a surface $$\begin{equation}
\label{zfxy}
\Phi_p=z-f(x,y)=0.
\end{equation}$$

### Local Coordinate System

Bases of a local *terrain* coordinate system $T$ are denoted $\hat{\mathbf{i}}_T$, $\hat{\mathbf{j}}_T$, and $\hat{\mathbf{k}}_T$, where $\hat{\mathbf{k}}_T$ is normal to surface $\Phi_p$. Therefore, $$\begin{equation}
\label{kbxy}
\begin{split}
   \hat{\mathbf{k}}_T(x,y)=k_{T,x}(x,y)\hat{\mathbf{i}}_G+k_{T,y}(x,y)\hat{\mathbf{j}}_G+k_{T,z}(x,y)\hat{\mathbf{k}}_G=\dfrac{\bigtriangledown \Phi_p}{\|\bigtriangledown \Phi_p\|}
\end{split}
.
\end{equation}$$ Bases of the local coordinate system are related to the bases of the ground frame by $$\begin{equation}
\label{ibjbkb2ijk}
\begin{split}
    \begin{bmatrix}
    \hat{\mathbf{i}}_T\\
    \hat{\mathbf{j}}_T\\
    \hat{\mathbf{k}}_T\\
    \end{bmatrix}
    =
    \mathcal{R}_{\phi-\theta}
    \begin{bmatrix}
    \hat{\mathbf{i}}_G\\
    \hat{\mathbf{j}}_G\\
    \hat{\mathbf{k}}_G\\
    \end{bmatrix}
\end{split}
,
\end{equation}$$ where $$\begin{split}
\mathcal{R}_{\phi-\theta}=&\mathcal{R}_\phi\mathcal{R}_\theta=\begin{bmatrix}
    \cos\theta&0&-\sin\theta\\
    \sin\phi \sin\theta&\cos\phi&\sin\phi \cos\theta\\
    \cos\phi \sin \theta&-\sin\phi&\cos\phi \cos\theta\\
    \end{bmatrix}
\\
\mathcal{R}_{\phi}=&
\begin{bmatrix}
1&0&0\\
0&\cos\phi&\sin\theta\\
0&-\sin\phi&\cos\phi
\end{bmatrix}
\\
\mathcal{R}_{\theta}=&
\begin{bmatrix}
\cos\theta&0&-\sin\theta\\
0&1&0\\
\sin\theta&0&\cos\theta
\end{bmatrix}
\end{split}
.$$

Equating the right hand sides of Eq. [\[kbxy\]](#kbxy){reference-type="eqref" reference="kbxy"} and the third row of [\[ibjbkb2ijk\]](#ibjbkb2ijk){reference-type="eqref" reference="ibjbkb2ijk"}, the roll angle $\phi$ and the pitch angle $\theta$ are obtained as follows: $$\begin{equation}
\label{phitheta}
\begin{split}
   \phi=&\sin^{-1}\left(-k_{T,y}\right) \\
   \theta=&\tan^{-1}\left(\dfrac{k_{T,x}}{k_{T,z}}\right) \\
\end{split}
.
\end{equation}$$ $\dot{\phi}$ and $\dot{\theta}$ can be related to $\dot{x}$ and $\dot{y}$ by taking the derivative of Eq. [\[phitheta\]](#phitheta){reference-type="eqref" reference="phitheta"}: $$\begin{equation}
\label{DPHDTH}
    \begin{bmatrix}
    \dot{\phi}\\
    \dot{\theta}
    \end{bmatrix}
    =\begin{bmatrix}
    \dfrac{1}{C\phi}&0\\
    0&{C\theta}^2
    \end{bmatrix}
   \begin{bmatrix}
\dfrac{-\partial k_{T,y}}{\partial x}&\dfrac{-\partial k_{T,y}}{\partial y}\\
\dfrac{\dfrac{\partial k_{T,x}}{\partial x}-\dfrac{\partial k_{T,z}}{\partial x}}{k_{T,z}^2}&\dfrac{\dfrac{\partial k_{T,x}}{\partial y}-\dfrac{\partial k_{T,z}}{\partial y}}{k_{T,z}^2}
\end{bmatrix}
    \begin{bmatrix}
    \dot{x}\\
    \dot{y}
    \end{bmatrix}
    .
\end{equation}$$ Note that $C\phi$ and $C\theta$ abbreviate $\cos\phi$ and $\cos\theta$, respectively.

### Body Coordinate System

The bases of the vehicle body coordinate system $B$, denoted $\hat{\mathbf{i}}_B$, $\hat{\mathbf{j}}_B$, and $\hat{\mathbf{k}}_B$, can be related to $\hat{\mathbf{i}}_T$, $\hat{\mathbf{j}}_T$ and $\hat{\mathbf{k}}_T$ by $$\begin{equation}
    \begin{bmatrix}
    \hat{\mathbf{i}}_B\\
    \hat{\mathbf{j}}_B\\
    \hat{\mathbf{k}}_B\\
    \end{bmatrix}
    =
    \mathcal{R}_{\psi}
    \begin{bmatrix}
    \hat{\mathbf{i}}_T\\
    \hat{\mathbf{j}}_T\\
    \hat{\mathbf{k}}_T\\
    \end{bmatrix}
=
    \begin{bmatrix}
    \cos\psi&\sin\psi&0\\
    -\sin\psi&\cos\psi&0\\
    0&0&1
    \end{bmatrix}
    \begin{bmatrix}
    \hat{\mathbf{i}}_T\\
    \hat{\mathbf{j}}_T\\
    \hat{\mathbf{k}}_T\\
    \end{bmatrix},
\end{equation}$$ where $\psi$ is the yaw or approximate heading angle. Car angular velocity can be expressed by $$\begin{equation}
    \vec{\omega}_B=\vec{\omega}_T+\dot{\psi}\hat{\mathbf{k}}_T,
\end{equation}$$ where $$\begin{equation}
\label{AngVel}
\begin{split}
    \vec{\omega}_T=&p_T\hat{\mathbf{i}}_T+q_T\hat{\mathbf{j}}_T+r_T\hat{\mathbf{k}}_T\\=&\dot{\phi}\hat{\mathbf{i}}_T+\dot{\theta}\cos\phi\hat{\mathbf{j}}_T-\dot{\theta}\sin\phi\hat{\mathbf{k}}_T
\end{split}
.
\end{equation}$$

## Vehicle Dynamics {#Ego Car Dynamics}

Fig. [1](#carbodyframe){reference-type="ref" reference="carbodyframe"} shows a schematic of vehicle/car configuration in motion plane $\Omega_p$; we assume $\Omega_p$ is tangent to the terrain surface. The car is modeled by two wheels connected by a rigid bar with length $l$. In the figure, $o_1$ and $o_2$ are the centers of the front and rear tires, respectively. Given steering angle $\delta$ and car speed $v_T$, motion dynamics can be expressed by [@paden2016survey; @kwatny2000nonlinear] $$\begin{equation}
\label{EGOCARDYN}
\begin{split}
\dot{\mathbf{r}}=&v_T\left(\cos\delta\hat{\mathbf{i}}_B+\sin\delta\hat{\mathbf{j}}_B\right)\\
\end{split}
.
\end{equation}$$

**Motion Constraint**: This work assumes side slip of the rear tire is zero. This assumption can be mathematically expressed by $$\begin{equation}
    \mathbf{v}_{{\mathrm{rel}}_{o_2}}\cdot\hat{\mathbf{j}}_B=\mathbf{0},
\end{equation}$$ where $$\begin{equation}
\mathbf{v}_{{\mathrm{rel}}_{o_2}}=\dot{\mathbf{r}}-\vec{\omega}_B\times (-l\hat{\mathbf{i}}_B)
\end{equation}$$ is the rear tire relative velocity with respect to the local body frame. Therefore $$\begin{equation}
    \dot{\psi}=-\dfrac{1}{l}\left(\dot{{\mathbf{r}}}-l\vec{\omega}_T\times\hat{\mathbf{i}}_B\right)\cdot\hat{\mathbf{j}}_B.
\end{equation}$$

By taking the time derivative of Eq. [\[EGOCARDYN\]](#EGOCARDYN){reference-type="eqref" reference="EGOCARDYN"}, acceleration of the car is computed as $$\begin{equation}
\begin{split}
\ddot{\mathbf{r}}=&a_T\left(\cos\delta\hat{\mathbf{i}}_B+\sin\delta\hat{\mathbf{j}}_B\right)+v_T\gamma\left(-\sin\delta\hat{\mathbf{i}}_B+\cos\delta\hat{\mathbf{j}}_B\right)\\
+&\vec{\omega}_B\times v_T\left(\cos\delta\hat{\mathbf{i}}_B+\sin\delta\hat{\mathbf{j}}_B\right)    
\end{split}
,
\end{equation}$$ where $a_T=\dot{v}_T$ and $\gamma=\dot{\delta}$ are the car tangential acceleration and steering rate, respectively. $a_T$ and $\gamma$ are determined by $$\begin{equation}
\label{atgamma}
\begin{split}
&  \begin{bmatrix}
    a_T&
    \gamma
    \end{bmatrix}
    ^T
    =
    \\
    &
    \begin{bmatrix}
    \cos\delta&\sin\delta\\
    \dfrac{-\sin\delta}{v_T}&\dfrac{\cos\delta}{v_T}
    \end{bmatrix}
    \begin{bmatrix}
    \hat{\mathbf{i}}_B\cdot\big[ \ddot{\mathbf{r}}-\vec{\omega}_B\times v_T\left(\cos\delta\hat{\mathbf{i}}_B+\sin\delta\hat{\mathbf{j}}_B\right)\big]\\
    \hat{\mathbf{j}}_B\cdot\big[ \ddot{\mathbf{r}}-\vec{\omega}_B\times v_T\left(\cos\delta\hat{\mathbf{i}}_B+\sin\delta\hat{\mathbf{j}}_B\right)\big]\\
    \end{bmatrix}
    .
\end{split}
\end{equation}$$

The magnitude of vehicle normal force, $$\begin{equation}
\label{FN}
    {F}_N=\hat{\mathbf{k}}_B\cdot\left(mg\mathbf{k}_G+m\ddot{\mathbf{r}}\right)
\end{equation}$$ must be always positive, e.g. $F_N>0,\forall t$. This guarantees that the car never leaves the motion surface.

**Remark**: In Eqs. [\[EGOCARDYN\]](#EGOCARDYN){reference-type="eqref" reference="EGOCARDYN"}, [\[atgamma\]](#atgamma){reference-type="eqref" reference="atgamma"} and [\[FN\]](#FN){reference-type="eqref" reference="FN"}, $\dot{\mathbf{r}}$ and $\ddot{\mathbf{r}}$ are the car velocity and acceleration expressed with respect to the ground coordinate system (see Eq. [\[VELACC\]](#VELACC){reference-type="eqref" reference="VELACC"}).

# Methodology {#Methodology}

This section presents the proposed three-layer planning strategy comprised of Global Route Planning (GRP), Local path planning (LPP), and feedback control (FC). GRP applies DP to assign optimal driving waypoints given terrain navigability (traversability), weather conditions, and driving motion constraints. LPP is responsible for computing a trajectory between consecutive waypoints assigned by DP. Local obstacle information obtained during LPP is applied by FC to track the desired trajectory.

## Global Route Planning {#Global Route Planning}

**DP state set $\mathcal S$**: A uniform grid is overlaid onto a local terrain of the United States. Grid nodes are defined by the set $\mathcal{V}$; the node $i\in \mathcal{V}$ is considered as an obstacle if:

1.  There exists water at node location $i\in \mathcal{V}$,

2.  Node $i\in \mathcal{V}$ contains foliage (trees) or buildings, or

3.  There is a considerable elevation difference (steep slope) at node location $i\in \mathcal{V}$.

Let the set $\mathcal{V}_o$ define obstacle index numbers. Then, $$\begin{equation}
    \mathcal S=\mathcal{V}\setminus \mathcal{V}_o
\end{equation}$$ defines the DP states. We assume that $\mathcal S$ has cardinality $N$, e.g. $\mathcal{S}=\{1,\cdots,N\}$.

Transition from node $s\in \mathcal S$ to node $s'\in \mathcal S$ is defined by a directed graph. In-neighbor nodes of node $s\in \mathcal{S}$ are defined by the set $$\begin{equation}
    \mathcal N_s=\{s_1,\cdots,s_{n_s}\},
\end{equation}$$ where $n_s\leq 8$ is the cardinality of the set $\mathcal N_s$.

**DP Actions**: DP actions are defined by the set $$\begin{equation}
\mathcal{A}=\{1,\cdots, 9\},
\end{equation}$$ where actions $1$ through $8$ command the vehicle to drive to an adjacent node directly East, Northeast, North, Northwest, West, Southwest, South, and Southeast, respectively. Action $9\in \mathcal{A}$ is the \"Stay\" command. As shown in Fig. [2](#DPdiagram){reference-type="ref" reference="DPdiagram"}, all directions defined by the set $\mathcal{S}$ may not necessarily be reached from every node $s\in \mathcal{S}$. Therefore, actions available at node $s\in \mathcal{S}$ are defined by $\mathcal{A}_s\subset \mathcal{A}$.

**Transition Function**: Let $(x_s,y_s)$ and $(x_{s'},y_{s'})$ denote planar positions of nodes $s\in \mathcal{S}$ and $s'\in \mathcal{N}_s$; land slope $m_{s,s'}$ over the straight path connecting $s$ and $s'$ is considered as the criterion for land navigability in this paper. We define $M_{d,max}$ and $M_{w,max}$ as upper bounds for land slope $m_{s,s'}$ for dry and hazardous (wet) surface conditions, respectively, leading to the following constraints:

- In a dry weather condition, $s'\in \mathcal{N}_s$ can be reached from $s\in \mathcal{S}$ only when $m_{s,s'}\leq M_{d,max}$.

- In a wet weather condition, $s'\in \mathcal{N}_s$ can be reached from $s\in \mathcal{S}$ only when $m_{s,s'}\leq M_{w,max}$.

Suppose that $s_a\in \mathcal{S}$ is the expected outcome state when executing action $a\in \mathcal{A}$ in $s\in \mathcal{S}$. Then, transition function $\mathcal{T}\left(s,a,s'\right)$ is defined as follows: $$\begin{equation}
\begin{split}
     &\mathcal{T}\left(s,a,s'\right)=\\
     &
    \begin{cases}
    1&\left(s'=s_a\right)\wedge\left(m_{s,s_a}\leq M_{d,max}\vee m_{s,s_a}\leq M_{w,max}\right)\\
    0&\mathrm{else}.
    \end{cases}
\end{split}
\end{equation}$$

**DP cost**: The DP cost at node $s\in \mathcal{S}$ under DP action $a\in \mathcal{A}_s$ is defined by $$\begin{equation}
    C(s,s_a)=\alpha_m\bar{m}_{s,s_a}+\alpha_dd_{s,s_a},
\label{DPequation}
\end{equation}$$ where $\bar{m}_{s,s_a}$ is the average slope (elevation difference) along the path segment connecting $s\in \mathcal{S}$ and $s_a\in \mathcal{N}_s$. Also, $d_{s,s_a}$ is the distance between nodes $s\in \mathcal{S}$ and $s_a\in \mathcal{N}_s$. Note that scaling factors $\alpha_m$ and $\alpha_d$ are assigned by $$\begin{equation}
\begin{bmatrix}
 \bar{m}&\bar{d}\\
 1&1
\end{bmatrix}
\begin{bmatrix}
\alpha_m\\
\alpha_d
\end{bmatrix}
=
\begin{bmatrix}
1\\
1
\end{bmatrix}
,
\end{equation}$$ where $$\begin{equation}
\begin{split}
    \bar{m}=&\mathrm{\mathbf{Average}}\big\{m(s,a)\big|s\in \mathcal{S},a\in \mathcal{A}_s\big\}\\
    \bar{d}=&\mathrm{\mathbf{Average}}\big\{d(s,a)\big|s\in \mathcal{S},a\in \mathcal{A}_s\big\}\\
\end{split}
.
\end{equation}$$

![Adjacent nodes with minimum cost-to-go are preferred. If there is non-zero elevation difference between two adjacent points choose only actions respecting weather-dependent constraints $M_{d,max}$ or $M_w,max$.](Rastgoftar2018DataDriven_figs/DPdiagram.jpg){#DPdiagram width="3.3 in"}

## Local Path Planning

The main responsibility of the local path planner (LPP) is to define a desired trajectory between consecutive waypoints assigned by the DP-based GRP. The LPP also might interact with the GRP to share information about dynamically-changing obstacle and environment properties (in future work). LPP trajectory computation is discussed below.

![Trajectory planning state machine.](Rastgoftar2018DataDriven_figs/TPSMUPDATE.jpg){#TPSM width="2.5 in"}

### Trajectory Planning

Suppose $(x_{k-1},y_{k-1})$, $(x_{k},y_{k})$, and $(x_{k+1},y_{k+1})$ are $x$ and $y$ components of three consecutive way points, where the path segments connecting these three waypoints are navigable, e.g. the path connecting these three waypoints are obstacle-free. Let $$\begin{equation}
\begin{split}
  \mu_{k-1,k}=&\dfrac{y_{k}-y_{k-1}}{x_{k}-x_{k-1}}\\
  \mu_{k,k+1}=&\dfrac{y_{k+1}-y_k}{x_{k+1}-x_k}\\
\end{split}
,
\end{equation}$$ then the path segments connecting $(x_{k-1},y_{k-1})$, $(x_{k},y_{k})$, and $(x_{k+1},y_{k+1})$ intersect if $\mu_{k-1,k}\neq \mu_{k,k+1}$.

:::: {#EgoCarPAth .figure}
::: caption
Desired vehicle paths given $\mu_{k-1,k}$ and $\mu_{k,k+1}$.
:::
::::

**Remark**: We define a nominal speed $v_0$ for traversal along the desired path. If $\mu_{k-1,k}\neq \mu_{k,k+1}$, then $v_0$ should satisfy the following inequality: $$\begin{equation}
    \dfrac{{v_0}^2}{\rho}\leq \dot{\psi}_{\mathrm{max}},
\end{equation}$$ where $\dot{\psi}_{\mathrm{max}}$ is the maximum yaw rate.

Given $\mu_{k-1,k}$ and $\mu_{k,k+1}$, one of the following two conditions holds:

- If $\mu_{k-1,k}= \mu_{k,k+1}$, then the projection of the desired path onto the $x-y$ plane is a single line segment connecting $(x_{k-1},y_{k-1})$ and $(x_{k+1},y_{k+1})$ (see Fig. [4](#EgoCarPAth){reference-type="ref" reference="EgoCarPAth"}(a)).

- If $\mu_{k-1,k}\neq \mu_{k,k+1}$, then the projection of the desired path onto the $x-y$ plane consists of two separate crossing line segments connected by a circular path with radius $\rho$. (See Fig. [4](#EgoCarPAth){reference-type="ref" reference="EgoCarPAth"}(b).).

### Trajectory Planning State Machine (TPSM)

A trajectory planning state machine (TPSM), shown in Fig. [3](#TPSM){reference-type="ref" reference="TPSM"}, describes how the desired trajectory can be planned given vehicle (i) actual speed $v_T$, (ii) nominal speed $v_0$, (iii) turning radius $\rho$, (iv) maximum yaw rate $\dot{\psi}_{\mathrm{max}}$, and (v) consecutive path segment parameters $\mu_{{k-1},k}$ and $\mu_{{k},{k+1}}$. TPSM inputs are defined by the set $$\Sigma=\{v_T, \mu_{{k-1},{k}}, \mu_{{k},{k+1}}\}.$$ TPSM states are defined by $$\begin{equation}
\mathcal{P}=\{p_0,p_1,p_2,p_3,p_4\},
\end{equation}$$ where atomic propositions $p_0$, $p_1$ and $p_2$ are assigned as follows: $$\begin{split}
    p_0:&{F}_N=\hat{\mathbf{k}}_B\cdot\left(mg\mathbf{k}_G+m\ddot{\mathbf{r}}\right)>0\\
    p_1:&~\mu_{{k},{k+1}}=\mu_{{k-1},{k}}\\
    p_2:&~v_T< v_0\\
     p_3:&~v_T= v_0\\
    p_4:&~\dfrac{v_0}{\rho}\leq \dot{\psi}_{\mathrm{max}}\\
\end{split}
.$$ Note that $p_0$ is the initial TPSM state. TPSM terminal states are defined by the set $$\mathcal{F}=\{\mathrm{ACC},\mathrm{DEC},\mathrm{CV}\}$$ where $\mathrm{ACC}$ and $\mathrm{DEC}$ command the car to accelerate and decelerate, respectively, and $\mathrm{CV}$ commands the car to move at constant speed.

Transitions over TPSM states are shown by solid and dashed arrows. If $p_k$ ($k=0,1,2,3,4$) is satisfied, transition to the next state is shown by a solid arrow; otherwise, state transition is shown by a dashed vector.

## Motion Control {#Feedback Control}

Suppose $$\begin{equation}
\begin{split}
    \mathbf{r}_d=&x_{d}\hat{\mathbf{i}}_G+y_{d}\hat{\mathbf{j}}_G+f(x_d,y_d)\hat{\mathbf{k}}_T\\
\end{split}
\end{equation}$$ defines the desired trajectory of the car over the surface $\phi_p=z-f(x,y)=0$. Let $x$ and $y$ components of the car acceleration be chosen as follows: $$\begin{equation}
\label{ddxddy}
\begin{split}
    \begin{bmatrix}
    \ddot{x}\\
    \ddot{y}
    \end{bmatrix}
    =
    \begin{bmatrix}
    \ddot{x}_{d}\\
    \ddot{y}_{d}
    \end{bmatrix}
    +k_1
    \left(\begin{bmatrix}
    \dot{x}_{d}\\
    \dot{y}_{d}
    \end{bmatrix}
    -
    \begin{bmatrix}
    \dot{x}\\
    \dot{y}
    \end{bmatrix}\right)
    +k_2
    \left(\begin{bmatrix}
    {x}_{d}\\
    {y}_{d}
    \end{bmatrix}
    -
    \begin{bmatrix}
    {x}\\
    {y}
    \end{bmatrix}\right)
\end{split}
.
\end{equation}$$ The error signal $\mathbf{E}=\left(
\begin{bmatrix}
{x}\\
{y}
\end{bmatrix}
-
\begin{bmatrix}
{x}_{d}\\
{y}_{d}
\end{bmatrix}\right)$ is then updated by the following second order dynamics: $$\begin{equation}
\label{ERRRDYN}
    \ddot{\mathbf{E}}+k_1\dot{\mathbf{E}}+k_2\mathbf{E}=\mathbf{0}.
\end{equation}$$ The error dynamics is asymptotically stable and $\mathbf{E}$ asymptotically converges to $\mathbf{0}$ if $k_1>0$ and $k_2>0$. Given $\ddot{x}$ and $\ddot{y}$ assigned by Eq. [\[ddxddy\]](#ddxddy){reference-type="eqref" reference="ddxddy"}, $\ddot{z}$ is specified by $$\begin{equation}
\label{GeomConst}
    \ddot{z}=\left(\dfrac{\partial f}{\partial x}\ddot{x}+\dfrac{\partial^2 f}{\partial x^2}\dot{x}^2+\dfrac{\partial^2 f}{\partial y^2}\dot{y}^2+\dfrac{\partial f}{\partial y}\ddot{y}+2\dfrac{\partial^2 f}{\partial x\partial y}\dot{x}\dot{y}\right).
\end{equation}$$ By knowing $\ddot{\mathbf{r}}$, the car control inputs $a_T=\dot{v}_T$ and $\gamma=\dot{\delta}$ are assigned by Eq. [\[atgamma\]](#atgamma){reference-type="eqref" reference="atgamma"}.

# Case Study Results {#Simulation Results}

This section describes processing and infusion of map and weather data into our off-road multi-layer planner. In Section [3.1](#Global Route Planning){reference-type="ref" reference="Global Route Planning"}, data training and global route planning using dynamic programming are described. A local path planning example is provided in Section [4.2](#Local Path Planning){reference-type="ref" reference="Local Path Planning"}, and trajectory tracking results are presented in Section [4.3](#Trajectory Tracking){reference-type="ref" reference="Trajectory Tracking"}.

## Global Route Planning {#global-route-planning}

### Data Training

The elevation data used for generating the grid-based map is downloaded from the United States Geographic Survey (USGS) TNM download [@USGSTNM], Elevation Source Data (3DEP). The USGS elevation data is in \".las\" format and needed to be transformed into a $1000\times 1000$ grid map. An online tool is used to transform the data into \".csv\" format (see Ref. [@LidarTool]). After data processing, we can obtain a map with raw elevation data for input to planning.

Two different locations are chosen for this study. One is a mountainous area near the Ochoco National Forest, Oregon. The center location coordinate is $(44.2062527, -119.5812443)$ [@Mountain]. The second locale is in Indiana, near Lake Michigan, which is a relatively flat terrain area. The center location coordinate for the Indiana region is $(41.1003777, -86.4307332)$ [@Land].

The $3-D$ surface maps and contour plots of both areas are shown in Fig. [5](#SimulationMaps){reference-type="ref" reference="SimulationMaps"}. The first Mountain area (Oregon Forest) has an average altitude of $4800$ feet and is covered by trees. The left lower area of the map has higher elevation and is covered with fewer trees.

The second land area (Indiana) is flat with only several trees and roads as notable features. This area offers easier traversability in all weather conditions than the mountainous region.

:::: {#SimulationMaps .figure latex-placement="!ht"}
::: caption
Elevation data for mountain (Oregon) and midwest (Indiana) case study terrains, with 3-D plots and contour plots: (a) Mountain Elevation Map (Oregon, coordinate (44.2062527, -119.5812443)). (b) Land Elevation Map (Indiana, coordinate (41.1003777, -86.4307332)). (c) Mountain Elevation Contour Map (Oregon, coordinate (44.2062527, -119.5812443)). (d) Land Elevation Contour Map (Indiana, coordinate (41.1003777, -86.4307332)).
:::
::::

The weather data are downloaded from a National Center for Environmental Information (NOAA) website. Thee database contains temperature, weather type, and wind speed information. The weather is almost the same across each regions being traversed but it varies over time. If the weather is severe, such as snowy and rainy, the weather is called harsh or *wet*. The constraint (threshold) on driving slope is decreased to $M_{w,max}$ under a wet weather condition. If the weather is dry, the slope constraint is set to $M_{d,max}$.

By using the two typical land type elevation maps, global route planning simulation results are generated using DP. A $1000\times 1000$ grid map is obtained by spatial discretization of the study areas. A DP state $s\in \mathcal{S}$ represents a node in the grid map. As mentioned in Section [3.1](#Global Route Planning){reference-type="ref" reference="Global Route Planning"}, $9$ dicrete actions assign motion direction at a node $s\in \mathcal{S}$. Given $s\in \mathcal{S}$, the next waypoint $s_a\in \mathcal{S}$ given $a\in\mathcal{A}$ is considered unreachable if elevation change along the connecting path exceeds applicable upper-bound limit $M_{d,\mathrm{max}}$ or $M_{w,\mathrm{max}}$. GRP case study results for Oregon and Indiana Maps are shown in Fig. [6](#MapPathPlan){reference-type="ref" reference="MapPathPlan"}. Three different destinations are defined in different GRP executions given the same initial location for each. Optimal paths connecting initial and final locations are obtained under nominal and harsh weather conditions as shown by blue, red and green in Fig. [6](#MapPathPlan){reference-type="ref" reference="MapPathPlan"}.

### Results For Nominal Weather Condition

For nominal weather condition, we choose $M_{d,\mathrm{max}}=\tan (6.90^o)$ as the upper-limit (threshold) slope. Figs. [6](#MapPathPlan){reference-type="ref" reference="MapPathPlan"} (b) and (e) show corresponding optimal paths. Blue, red and green paths are reachable in both figures. The heavily-forested Oregon area shown in Fig. [6](#MapPathPlan){reference-type="ref" reference="MapPathPlan"} impacts traversals. Except for the blue path starting from the edge of the forest, initial traversals are flat in the remaining paths.

### Results For Harsh (Wet) Weather Conditions

For harsh or wet weather conditions, we choose $M_{d,\mathrm{max}}=\tan (2.77^o)$ as the terrain slope constraint. We consider the same start and target destinations to compute driving paths under harsh weather condition as in the previous cases. Figs. [6](#MapPathPlan){reference-type="ref" reference="MapPathPlan"} (c) and (f) show optimal driving paths under harsh (wet) weather conditions. Note that in Fig. [6](#MapPathPlan){reference-type="ref" reference="MapPathPlan"} (c), the blue path destination is unreachable because the endpoint region is not connected to the center (start state) region due to terrain slope constraints. The red and green paths are reachable but differ nontrivially compared to paths obtained for nominal weather conditions. As shown in Fig. [6](#MapPathPlan){reference-type="ref" reference="MapPathPlan"} (f), GRP chooses a safer but longer path to avoid a low elevation region in the depicted bottom right region given bad (wet) weather. Path planning results under wet and nominal weather conditions are quantitatively compared in Table [1](#table_example){reference-type="ref" reference="table_example"}.

:::: {#MapPathPlan .figure latex-placement="!ht"}
::: caption
Three path plans are generated given the same start point with different constraint sets for the Oregon map and land map. (a) The chosen traversal area for the Oregon map. (b) Nominal weather conditions for the Oregon map; the planned path has slope constraint $6.90^o$, representing $12.10\%$ slope. All paths are reachable. (c) Harsh (wet) weather for the Oregon map; the planned path has slope constraint $2.77^o$, representing $4.84\%$ slope. The blue path is unreachable while the other two paths are reachable given this constraint. (d) The chosen traversal area for the Indiana Map. (e) Nominal weather conditions for the Indiana map; the planned path has slope constraint $6.90^o$, representing $12.10\%$ slope. All paths are reachable. (f) Harsh (wet) weather for the Indiana map; the planned path has slope constraint $2.77^o$, representing $4.84\%$ slope. All paths are reachable.
:::
::::

::: {#table_example}
+-----------------+-------------------------------------------------------+-------------------------------------------------------+
|                 | Appropriate                                           | Harsh                                                 |
+:=======:+:=====:+:==================:+:=========:+:====================:+:==================:+:=========:+:====================:+
| State   | Path  | $D_{\mathrm{max}}$ | $\bar{s}$ | ${s}_{\mathrm{max}}$ | $D_{\mathrm{max}}$ | $\bar{s}$ | ${s}_{\mathrm{max}}$ |
+---------+-------+--------------------+-----------+----------------------+--------------------+-----------+----------------------+
| Oregon  | Red   | $325.05$           | $1.96$    | $2.87$               | $340.9$            | $1.75$    | $2.70$               |
|         +-------+--------------------+-----------+----------------------+--------------------+-----------+----------------------+
|         | Green | $158.05$           | $1.14$    | $3.29$               | $158.15$           | $1.16$    | $2.53$               |
|         +-------+--------------------+-----------+----------------------+--------------------+-----------+----------------------+
|         | Blue  | $282.65$           | $2.11$    | $6.64$               | $N/A$              | $N/A$     | $N/A$                |
+---------+-------+--------------------+-----------+----------------------+--------------------+-----------+----------------------+
| Indiana | Red   | $680.1$            | $0.92$    | $5.54$               | $728.4$            | $0.75$    | $2.67$               |
|         +-------+--------------------+-----------+----------------------+--------------------+-----------+----------------------+
|         | Green | $439.75$           | $0.57$    | $2.30$               | $439.75$           | $0.57$    | $2.30$               |
|         +-------+--------------------+-----------+----------------------+--------------------+-----------+----------------------+
|         | Blue  | $637.4$            | $1.11$    | $6.33$               | $780.5$            | $0.73$    | $2.63$               |
+---------+-------+--------------------+-----------+----------------------+--------------------+-----------+----------------------+

: Distances $D_{\mathrm{max}}(m)$, maximum and average slopes $\bar{s}( ^o )$ and $s(^o)$ of planned paths under nominal and harsh (wet) weather conditions.
:::

:::: {#LPPPic .figure latex-placement="!ht"}
![](Rastgoftar2018DataDriven_figs/LPPPA.jpg){width="3 in"}

::: caption
Smooth turns computed during local path planning (LPP) given a turn-back defined by three consecutive waypoints.
:::
::::

## Local Path Planning {#Local Path Planning}

Given three consecutive desired waypoints $(x_k,y_k)=(885,418.5)$ meters ($m$), $(x_k,y_k)=(892.5,411)$ m, and $(x_k,y_k)=(885,403.5)m$ , $\mu_{k-1,k}\neq \mu_{k,k+1}$. The desired path therefore consists of two straight path segments connected by a circular-arc turn (see Fig. [7](#LPPPic){reference-type="ref" reference="LPPPic"}). Note that the radius of the circular path is $\rho=4m$ in our case study. Selecting $\dot{\psi}_{\mathrm{max}}=1~\mathrm{rad}/s$ as the upper-bound for yaw rate, atomic proposition $p_4$ is satisfied if $v_T=v_0=2~m/s$. Because the desired speed is constant, the desired trajectory $\mathbf{r}_d(t)=x_d(t)\hat{\mathbf{i}}+y_d(t)\hat{\mathbf{j}}$ is given by $$\begin{equation}
\label{Des1}
\begin{split}
    \mathbf{r}_d=&v_T\mathbf{\hat{n}}_d=2\mathbf{\hat{n}}_d\\
\end{split}
\end{equation}$$ where the tangent vector $$\begin{equation}
\label{Des2}
    \mathbf{\hat{n}}_d=\dfrac{d\mathbf{r}_d}{ds}
\end{equation}$$ is as follows: $$\begin{equation}
\label{Des3}
    \mathbf{\hat{n}}_d=
    \begin{cases}
   {\frac{\sqrt{2}}{2}}\hat{\mathbf{i}}+{-\frac{\sqrt{2}}{2}}\hat{\mathbf{j}}&s\leq  4.6066\\
    2\cos\left(-s+{\frac{\pi}{4}}\right)& 4.6066<s\leq 14.0314\\
    {-\frac{\sqrt{2}}{2}}\hat{\mathbf{i}}+{-\frac{\sqrt{2}}{2}}\hat{\mathbf{j}}&14.0314<s\leq 18.6380\\
    \end{cases}
    .
\end{equation}$$ Note that $0\leq s\leq 18.6380$ is the desired path arc length, where $v_T=\dot{s}=2{~m/s}$ ($\forall s$).

## Trajectory Tracking {#Trajectory Tracking}

By applying the proposed feedback controller design from Section [3.3](#Feedback Control){reference-type="ref" reference="Feedback Control"}, the desired LPP vehicle trajectory assigned by Eqs. [\[Des1\]](#Des1){reference-type="eqref" reference="Des1"} and [\[Des2\]](#Des2){reference-type="eqref" reference="Des2"} can be asymptotically tracked. The FC is assigned controller gains $k_1=10$ and $k_2=20$ for this example. Fig. [8](#Coefficients){reference-type="ref" reference="Coefficients"} shows the $x$ and $y$ components of vehicle desired and actual positions. Error $\|\mathbf{E}\|$, the deviation between actual and desired position, is shown versus time in Fig. [9](#EERROORR){reference-type="ref" reference="EERROORR"}. Notice that error never exceeds $0.1101$. This deviation error occurs due to (i) surface non-linearities and (ii) sudden acceleration changes along the desired path. While acceleration along the linear segments of the path is zero, acceleration rapidly changes when the car enters or exits a circular arc (turning) path.

![Actual and desired trajectory of the car over the motion surface](Rastgoftar2018DataDriven_figs/ControlFigure.jpg){#Coefficients width="2.8 in"}

:::: {#EERROORR .figure latex-placement="!ht"}
![](Rastgoftar2018DataDriven_figs/ErrorFigure.png){width="3 in"}

::: caption
Deviation between actual and desired position of the car as a function of time
:::
::::

# Conclusion {#Conclusion}

This paper presents a novel data-driven approach for off-road motion planning and control. A dynamic programming module defines optimal waypoints using available GIS terrain and recent weather data. A path planning layer assigns a feasible desired trajectory connecting planned waypoints. A feedback linearization controller successfully tracks the desired trajectory over a nonlinear surface. In future work, we will relax assumptions related to sideslip and incorporate more sophisticated models of terrain interactions to improve decisions across all three decision layers.

#  Acknowledgement

This work was supported in part under Office of Naval Research grant N000141410596.

::: thebibliography
10 url@samestyle

F. Duchoň, A. Babinec, M. Kajan, P. Beňo, M. Florek, T. Fico, and L. Jurišica, "Path planning with modified a star algorithm for a mobile robot," *Procedia Engineering*, vol. 96, pp. 59--69, 2014.

J.-C. Latombe, *Robot motion planning*.Springer Science & Business Media, 2012, vol. 124.

D. Gaw and A. Meystel, "Minimum-time navigation of an unmanned mobile robot in a 2-1/2d world with obstacles," in *Robotics and Automation. Proceedings. 1986 IEEE International Conference on*, vol. 3.IEEE, 1986, pp. 1670--1677.

X. Zhao, W. Zhang, Y. Feng, and Y. Yang, "Optimizing gear shifting strategy for off-road vehicle with dynamic programming," *Mathematical Problems in Engineering*, vol. 2014, 2014.

S. Karumanchi, T. Allen, T. Bailey, and S. Scheding, "Non-parametric learning to aid path planning over slopes," *The International Journal of Robotics Research*, vol. 29, no. 8, pp. 997--1018, 2010.

K. Chu, M. Lee, and M. Sunwoo, "Local path planning for off-road autonomous driving with avoidance of static obstacles," *IEEE Transactions on Intelligent Transportation Systems*, vol. 13, no. 4, pp. 1599--1616, 2012.

K. Chu, J. Kim, K. Jo, and M. Sunwoo, "Real-time path planning of autonomous vehicles for unstructured road navigation," *International Journal of Automotive Technology*, vol. 16, no. 4, pp. 653--668, 2015.

R. T. Farouki and T. Sakkalis, "Pythagorean hodographs," *IBM Journal of Research and Development*, vol. 34, no. 5, pp. 736--752, 1990.

T. M. Howard and A. Kelly, "Optimal rough terrain trajectory generation for wheeled mobile robots," *The International Journal of Robotics Research*, vol. 26, no. 2, pp. 141--166, 2007.

Z. Shiller and J. Chen, "Optimal motion planning of autonomous vehicles in three dimensional terrains," in *Robotics and Automation, 1990. Proceedings., 1990 IEEE International Conference on*.IEEE, 1990, pp. 198--203.

Z. Shiller and Y.-R. Gwo, "Dynamic motion planning of autonomous vehicles," *IEEE Transactions on Robotics and Automation*, vol. 7, no. 2, pp. 241--249, 1991.

F. B. Amar, P. Bidaud, and F. B. Ouezdou, "On modeling and motion planning of planetary vehicles," in *Intelligent Robots and Systems' 93, IROS'93. Proceedings of the 1993 IEEE/RSJ International Conference on*, vol. 2.IEEE, 1993, pp. 1381--1386.

D. Bonnafous, S. Lacroix, and T. Siméon, "Motion generation for a rover on rough terrains," in *Intelligent Robots and Systems, 2001. Proceedings. 2001 IEEE/RSJ International Conference on*, vol. 2.IEEE, 2001, pp. 784--789.

D. P. Bertsekas, D. P. Bertsekas, D. P. Bertsekas, and D. P. Bertsekas, *Dynamic programming and optimal control*.Athena scientific Belmont, MA, 1995, vol. 1, no. 2.

M. Zolfpour-Arokhlo, A. Selamat, S. Z. M. Hashim, and H. Afkhami, "Modeling of route planning system based on q value-based dynamic programming with multi-agent reinforcement learning algorithms," *Engineering Applications of Artificial Intelligence*, vol. 29, pp. 163--177, 2014.

A. Kelly, A. Stentz, O. Amidi, M. Bode, D. Bradley, A. Diaz-Calderon, M. Happold, H. Herman, R. Mandelbaum, T. Pilarski *et al.*, "Toward reliable off road autonomous vehicles operating in challenging environments," *The International Journal of Robotics Research*, vol. 25, no. 5-6, pp. 449--483, 2006.

H. Mousazadeh, "A technical review on navigation systems of agricultural autonomous off-road vehicles," *Journal of Terramechanics*, vol. 50, no. 3, pp. 211--232, 2013.

G. Reina, A. Milella, and R. Worst, "Lidar and stereo combination for traversability assessment of off-road robotic vehicles," *Robotica*, vol. 34, no. 12, pp. 2823--2841, 2016.

R. González, A. López, and K. Iagnemma, "Thermal vision, moisture content, and vegetation in the context of off-road mobile robots," *Journal of Terramechanics*, vol. 70, pp. 35--48, 2017.

J. hwan Jeon, R. V. Cowlagi, S. C. Peters, S. Karaman, E. Frazzoli, P. Tsiotras, and K. Iagnemma, "Optimal motion planning with the half-car dynamical model for autonomous high-speed driving," in *American Control Conference (ACC), 2013*.IEEE, 2013, pp. 188--193.

J. Kong, M. Pfeiffer, G. Schildbach, and F. Borrelli, "Kinematic and dynamic vehicle models for autonomous driving control design," in *Intelligent Vehicles Symposium (IV), 2015 IEEE*. IEEE, 2015, pp. 1094--1099.

J. Ryu and J. C. Gerdes, "Integrating inertial sensors with global positioning system (gps) for vehicle dynamics control," *TRANSACTIONS-AMERICAN SOCIETY OF MECHANICAL ENGINEERS JOURNAL OF DYNAMIC SYSTEMS MEASUREMENT AND CONTROL*, vol. 126, no. 2, pp. 243--254, 2004.

M. Brown, J. Funke, S. Erlien, and J. C. Gerdes, "Safe driving envelopes for path tracking in autonomous vehicles," *Control Engineering Practice*, vol. 61, pp. 307--316, 2017.

B. Paden, M. Čáp, S. Z. Yong, D. Yershov, and E. Frazzoli, "A survey of motion planning and control techniques for self-driving urban vehicles," *IEEE Transactions on Intelligent Vehicles*, vol. 1, no. 1, pp. 33--55, 2016.

H. G. Kwatny and G. Blankenship, *Nonlinear Control and Analytical Mechanics: a computational approach*. Springer Science & Business Media, 2000.

J. E. Hopcroft, R. Motwani, and J. D. Ullman, "Automata theory, languages, and computation," *International Edition*, vol. 24, 2006.

M. L. Puterman, *Markov decision processes: discrete stochastic dynamic programming*.John Wiley & Sons, 2014.

=plus 4minus U. G. Survey. (2017) USGS TNM Download (V1.0). \[Online\]. Available: https://viewer.nationalmap.gov/basic

=plus 4minus P. Donato. (2017) USGS Lidar Data tool. \[Online\]. Available: https://bitbucket.org/umich_a2sys/usgs_lidar

=plus 4minus U. G. Survey. (2017) USGS Lidar Point Cloud (LPC) OR_OLC-Ochoco_2011_000034 2014-09-18 LAS. \[Online\]. Available: https://www.sciencebase.gov/catalog/item/58275640e4b01fad86fccc0d

=plus 4minus ------. (2017) USGS Lidar Point Cloud (LPC) IN_Statewide-FultonCo_2011_000049 2014-09-06 LAS. \[Online\]. Available: https://www.sciencebase.gov/catalog/item/5827579de4b01fad86fceef5
:::
