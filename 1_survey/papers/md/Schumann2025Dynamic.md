---
citation_key: Schumann2025Dynamic
arxiv_id: 2504.03280
arxiv_url: https://arxiv.org/abs/2504.03280
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-24T15:28:58Z
origin: ai+web
reviewed: false
---

# Introduction {#sec:intro}

:::: {#fig:overview .figure latex-placement="t"}
::: caption
Overview of the proposed methods. 1. Precise positioning at switching points by dynamic weight allocation while being able to smooth the rest of the trajectory; 2. Seamless and safe planning to goal poses by dynamic objective allocation while respecting corridor constraints.
:::
::::

Automated guided vehicles and other logistics robots are increasingly used in warehouses and similar environments [@warehouseReport]. In these scenarios, the robots are faced with the task of finding, transporting, and dropping off different goods or containers in narrow and unstructured environments. Further, they regularity need to dock automatically to their charging station. In this work, we focus on the motion planning part of these use cases. There already exist industry-level solutions, many of them using the motion planning algorithms of the Nav2 stack of Open Navigation LLC [@macenski2020marathon2; @macenski2023survey]. These algorithms provide methods for motion planning in ROS2 [@macenski2022ros] and contain a docking mechanism for connecting robots and vehicles with charging stations or similar objects. Generally, these approaches are often divided into two phases. A rough positioning to a so-called staging pose followed by the detection of, for example, the charging station and the navigation towards it. This workflow has two main disadvantages. The robot stops at the staging pose to allow for a safe switch to another planning algorithm, which is often necessary. This intermediate stop takes time, and it is unlikely that the staging pose is part of the optimal trajectory to the goal pose. In addition to that, the controller used in the Nav2 stack to reach the final goal pose in the second phase is not able to handle non-holonomic vehicle dynamics. Hence, if the goal pose is at an inconvenient position that cannot be reached physically from the staging pose, the controller will fail to reach it, which will trigger a retrial of the procedure starting at a new staging pose.

In this work, we mitigate these disadvantages by proposing a unified MPC-based approach that does not require switching between two algorithms but seamlessly completes the docking scenario. The main contributions of this work are visualized in Fig. [1](#fig:overview){reference-type="ref" reference="fig:overview"}, which are:

1.  Dynamic weight allocation to precisely reach direction changes and path ends. This serves as the base for the last contribution, which is called

2.  Dynamic objective allocation: An MPCC that inherently changes its objective to transition to a pure cartesian MPC to reach specific goal poses.

The source code of this paper will be published on the final submission at[^3]. The paper is structured in the following way: First, related work is summarized in Sec. [2](#sec:related-work){reference-type="ref" reference="sec:related-work"}, followed by the foundations in Sec. [3](#sec:foundations){reference-type="ref" reference="sec:foundations"}, after which the identified problem is further analyzed in Sec. [4](#sec:problem_formulation){reference-type="ref" reference="sec:problem_formulation"}. Then, the proposed methods are explained in Sec. [5](#sec:method){reference-type="ref" reference="sec:method"} followed by the evaluation in Sec. [6](#sec:eval){reference-type="ref" reference="sec:eval"}. Finally, the paper is concluded in Sec. [7](#sec:conclusion){reference-type="ref" reference="sec:conclusion"}.

# Related Work {#sec:related-work}

The first topic that is handled in this work is the problem of path-following. Hence, we assume that a global kinematically feasible path has already been planned. Possible methods to follow this path are the Stanley controller [@thrun2006stanley] and pure pursuit [@coulter1992pure] or regulated pure pursuit [@macenski2023regulated] controller. These provide a control law that stabilizes the robot along the path. Other approaches are sampling-based, like the dynamic window approach (DWA) [@fox1997dwa] or model predictive path integral (MPPI) [@williams2016mppi] method. At last, model predictive control (MPC) [@ziegler2014bertha] and especially model predictive contouring control (MPCC) [@liniger2015; @romero2022] can be used in which the path following problem is solved using numerical optimization. Especially, [@romero2022] proposes a method to dynamically change the weights of an MPC-based controller, which is used to fly a drone precisely through a number of goals.

The next topic is the task of navigating to a specific pose. At first, this goal can be achieved by planning a path to this pose followed by a path-following controller. However, if the goal pose is derived from noisy measurements, this method is not suitable as it would trigger a frequent replanning of a new path, which is resource-intensive and could lead to varying paths caused by discretization errors in the path planning algorithm, which reduces the robustness. Therefore, methods to plan directly to a goal pose are necessary. They are the graceful controller [@park2011graceful], which is unable to handle non-holonomic system dynamics, flatness-based controllers [@fuchshumer2005flatness], (iterative) linear quadratic regulators [@chen2019ilqr], and also MPC-based methods [@zhang2018opt]. The latter ones are able to handle non-holonomic system dynamics as present in normal vehicles.

However, there are scenarios in which both methods should be applied shortly after each other. This is the case, e.g., in robot docking maneuvers to their charging stations or if they must navigate to pick up a package. Usually, the path-following step is completely separated from the step to plan to a pose, like in the docking server of the Nav2 stack [@macenski2020marathon2; @macenski2023survey], which is used in the industry by different robot manufacturers like Dexory [@dexory]. The Nav2 stack uses the graceful controller mentioned above, which has the disadvantage of being incapable of handling non-holonomic vehicle dynamics. Due to this limitation and the possibility of first navigating to a staging pose, this planning framework can generate suboptimal trajectories. Hence, it would be advantageous to address this topic with a unified approach. To the best of our knowledge, no motion planning algorithm yet exists that solves the two problems of path following and moving to a pose in one go. As stated above, MPC-based methods can solve both problems. Therefore, this paper proposes an approach using a variant of MPC that can solve both problems inherently.

# Foundations {#sec:foundations}

This section gives a brief overview of the concept of MPC and MPCC. The fundamental algorithm in this work is an MPCC similar to the ones in [@liniger2015] and [@romero2022]. Hence, the reader is referred to [@romero2022] for further details.

The core of MPC is an optimal control problem (OCP). This section will define the terms of an OCP partly discretely and continuously to allow easier comparison with its implementation. The OCP is solved for a certain time horizon $T$, which is divided into $N$ steps. The sub-index $k\in N$ specifies variables at a single discretized time step. Its goal is to find a sequence of inputs $\boldsymbol{u}_k$ that minimizes a given cost function $J(\boldsymbol{x})$ depending on the state and input vectors $\boldsymbol{x} \in \mathcal{X}$ and $\boldsymbol{u} \in \mathcal{U}$ with respect to the dynamic function of a given system $f: \mathcal{X} \times \mathcal{U} \mapsto \mathcal{X}$. $$\begin{align}
\begin{split}
    \mathop{\mathrm{argmin}}_u\quad &J(\boldsymbol{x}) \\
    \text{subject to} \quad &\boldsymbol{x}_0 = \boldsymbol{x} \\&\boldsymbol{x}_{k+1} = f(\boldsymbol{x}_k, \boldsymbol{u}_k) \\
    \end{split}
\end{align}$$ The standard cost function minimizes the quadratic differences of the states and inputs to a given reference $\boldsymbol{x}_k^\text{r}$, $\boldsymbol{u}_k^\text{r}$. These differences are denoted by $\Delta\boldsymbol{x}_k$, $\Delta\boldsymbol{u}_k$ and $\Delta\boldsymbol{x}_N$. Thus, the cost function is defined by $$\begin{align}
    J(\boldsymbol{x}) = 
        \Vert \Delta\boldsymbol{x}_N \Vert^2_{\boldsymbol{Q}_N} +  
        \sum_{k=0}^{N-1}
        \Vert \Delta\boldsymbol{x}_k \Vert^2_{\boldsymbol{Q}} + 
        \Vert \Delta\boldsymbol{u}_k \Vert^2_{\boldsymbol{R}}\,. \label{eq:mpc}
\end{align}$$ The matrices $\boldsymbol{Q}_N=\operatorname{diag}(\boldsymbol{q_N})$, $\boldsymbol{Q}=\operatorname{diag}(\boldsymbol{q})$, $\boldsymbol{R}=\operatorname{diag}(\boldsymbol{r})$ are the weight matrices for the weighted Euclidian product denoted by $\Vert \boldsymbol{x}\Vert^2_Q = \boldsymbol{x}^T\cdot \boldsymbol{Q} \cdot \boldsymbol{x}$. This summarizes the structure of a standard MPC.

The MPCC approach comprises some additional changes. The state vector $\boldsymbol{x}$ is extended by an additional state $\theta$ that specifies the arc length along a given reference path that should be followed. This reference path is a parameterized path denoted by $\boldsymbol{p}^\text{r}(\theta) = (x^\text{r}(\theta), y^\text{r}(\theta), \phi^\text{r}(\theta))$. In addition, the input vector $\boldsymbol{u}$ is extended by the derivative of the arc length $\dot\theta$. Hence, each state has a corresponding reference pose $\boldsymbol{p}_k^r=(x_k^\text{r}, y_k^\text{r}, \phi_k^\text{r})$ whose location can be controlled by the virtual input $\dot\theta$. This input is penalized with the parameter $\gamma$, which is a negative penalty, hence a reward, that causes the MPCC to maximize the value of $\dot\theta$, leading to a progression of the reference poses along the reference path. The particularity of the MPCC is that it contains a vector of additional Frenet coordinates $\boldsymbol{x}^\text{F}$ with their corresponding weight matrix $\boldsymbol{Q}^\text{F}=\operatorname{diag}(\boldsymbol{q}^\text{F})$. The frenet coordinates and the corresponding weight vector are defined by $$\begin{align}
        \boldsymbol{x}^\text{F} = \begin{pmatrix} 
        e^\text{l} \\ 
        e^\text{c} \\ 
        % e^{\phi}
        \end{pmatrix}\,,\quad 
    \boldsymbol{q}^\text{F} = 
    \begin{pmatrix} 
    q^\text{l} \\
    q^\text{c} \\ 
    % q^{\phi}
    \end{pmatrix} \,. \label{eq:frenet_state_and_weight}
\end{align}$$ The Frenet coordinates can be approximated by the following equation, which denotes a rotation of the coordinate differences around the reference pose. $$\begin{align}
        \begin{pmatrix} 
        e^\text{l} \\ 
        e^\text{c} \\ 
        % e^{\phi}
        \end{pmatrix}=
        \begin{pmatrix}
        (x\!-\!x^\text{r})\!\cdot\!\cos(\phi^r)\!+\!(y\!-\!y^\text{r})\!\cdot\!\sin(\phi^\text{r})\\ 
        -(x\!-\!x^\text{r})\!\cdot\!\sin(\phi^r)\!+\!(y\!-\!y^\text{r})\!\cdot\!\cos(\phi^\text{r})\\ 
        % \phi\!-\!\phi^r
        \end{pmatrix}\,.
        \label{eq:contouring}
\end{align}$$ However, this approximation is only valid if $\boldsymbol{x}^\text{F}$ if $q^\text{l} \gg q^\text{c}$. Only in this case is $e^\text{c}$ equal to the lateral deviation to the reference pose $\boldsymbol{p^\text{r}}$ and $e^\text{l}$ to the longitudinal deviation. Hence, the MPCC maximizes its progress $\dot\theta$ while minimizing the longitudinal deviation to the reference pose, which provides a valid lateral distance to the reference path encoded in the Frenet coordinate $e^\text{c}$. Usually, there is no final position to reach. Hence, the term $\Vert\Delta\boldsymbol{x}_N\Vert^2_{\boldsymbol{Q}_N}$ is often omitted as no reference for the final state exists. The overall cost function of the MPCC is then denoted by $$\begin{align}
\begin{split}
    J(\boldsymbol{x}) = 
        % \Vert\boldsymbol{x}_N\Vert^2_{\boldsymbol{Q}_N} +  
        \sum_{k=0}^{N-1}
        &\Vert \Delta\boldsymbol{x}_k \Vert^2_{\boldsymbol{Q}} + 
        \Vert \Delta\boldsymbol{x}^\text{F}_k \Vert^2_{\boldsymbol{Q^\text{F}}} + \\
        &\Vert \Delta\boldsymbol{u}_k \Vert^2_{\boldsymbol{R}} +
        \dot\theta_k \gamma \,. \label{eq:mpcc}
\end{split}
\end{align}$$

# Problem Formulation {#sec:problem_formulation}

:::: {#fig:problem .figure latex-placement="t"}
::: caption
Visualization of the stated problem. Each trajectory state $\boldsymbol{x}_k$ has a reference pose $p_k^\text{r}$ perfectly orthogonally at the reference path. This provides valid frenet coordinates. However, with standard MPCC, the goal pose behind the corridor cannot be reached without switching to another motion planning algorithm, as there is no valid pairing of a state and a reference pose for $\theta > \theta^\text{e}$.
:::
::::

The automated vehicle controlled in this work can be approximated by a bicycle mode. Thus, the state vector $\boldsymbol{x}$ and the input vector $\boldsymbol{u}$, including their extensions by MPCC, are defined by $$\begin{align}
    \boldsymbol{x} = \begin{pmatrix} 
    x\\ y\\ \phi \\ v\\ \delta \\ \theta \\ 
    \end{pmatrix}, 
        \quad
    \boldsymbol{u} = \begin{pmatrix} 
    a\\ 
    \dot{\delta} \\
    \dot{\theta} %
    \end{pmatrix}\,.  %, \quad 
    %     \boldsymbol{x}^\text{F} &= 
    % \begin{pmatrix} 
    % e^\text{l} \\ 
    % e^\text{c} \\ 
    % e^\phi
    % \end{pmatrix}\,.
\end{align}$$ Further, the problem solved in this work is visualized in Fig. [2](#fig:problem){reference-type="ref" reference="fig:problem"}. The goal of the trajectory planning algorithm is to follow a path under certain state and input constraints. They are, among others, the so-called corridor constraints. They define the extent of obstacles in Frenet coordinates and constrain the contouring error by $\underline{e}^\text{c}(\theta) < e^\text{c}(\theta) < \overline{e}^\text{c}(\theta)$. However, goal poses extracted from noisy measurements change over time, leading to goal poses that are different from the pose that the underlying path was previously planned to. The motion planning algorithm should be able to plan to these poses without having to repeat the path planning approach. This should also be possible for poses that lie behind the path end denoted by $\theta^\text{e}$. Thus, the trajectory must be able to have states with $\theta > \theta^\text{e}$.

# Method {#sec:method}

This section explains the methods of our contributions.

## Dynamic Weight Allocation {#sec:method:dyn_weight}

In path-following problems, the path ends must be reached precisely if they are the goal of the overall motion plan. Further, the cusp points, at which direction switches are necessary, should also be reached precisely to ensure that the path can be followed with respect to the vehicle's system dynamics. Therefore, we introduce a dynamic weight allocation technique similar to the one used by [@romero2022] to precisely reach the mentioned points.

The first part of the method is setting weight $q^\text{c}$ for the contouring error $e^\text{c}$ to the path depending on the proximity to the end of the path. This distance is calculated by the longitudinal position of the trajectory given by $\theta$ to the longitudinal position of the path end or switching point, which is denoted by $\theta^\text{e}$. The resulting distance is denoted by $\epsilon(\theta)$. Now an effective $q^\text{c,eff}$ is calculated by blending the original contouring weight $q^\text{c}$ with an increased one, denoted by $q^\text{c,e}$, by means of a sigmoid function $\sigma(\theta)$: $$\begin{align}
\begin{split}
    \epsilon(\theta) &= \theta^\text{e} - \theta \\
    \sigma(\theta) &= \frac{1}{1+e^{\,\alpha\cdot(\epsilon(\theta) - \beta)}} \\
    q^\text{c,eff}(\theta) &= \sigma(\theta) \cdot q^\text{c,e} + (1-\sigma(\theta)) \cdot q^\text{c}.\label{eq:qceff}
    \end{split}
\end{align}$$ Here, $\alpha$ and $\beta$ serve as tuning parameters to set the steepness and the offset of the sigmoid function, which defines the proximity in which the cost starts to blend, leading to the vehicle staying closer to the reference path. Hence, the effective contouring weight vector is changed from the fundamental version in Eq. [\[eq:frenet_state_and_weight\]](#eq:frenet_state_and_weight){reference-type="ref" reference="eq:frenet_state_and_weight"} to $$\begin{align}
    \boldsymbol{q}^\text{F}(\theta) = 
    \begin{pmatrix} 
    q^\text{l} \\
    q^\text{c,eff}(\theta) \\ 
    % q^{\phi}
    \end{pmatrix}\,.
\end{align}$$ Fig. [3](#fig:dyn_weight){reference-type="ref" reference="fig:dyn_weight"} visualizes the key aspects of this method schematically. The figure visualizes the rise of $q^\text{c,eff}$ by the dynamic weight allocation for trajectory states near the path end $\theta^e$. This causes the trajectory to minimize the contouring error $e^\text{c}$ towards the path end.

:::: {#fig:dyn_weight .figure latex-placement="t"}
::: caption
Schematic visualization of the dynamic weight allocation method to precisely reach the path end at $\theta^\text{e}$: The sigmoid function $\sigma(\theta)$ blends the weights $q^\text{c}$ into $q^\text{c,e}$ for trajectory states approaching the path end at $\theta=30$. This causes an increasing penalty of $e^\text{c}$, which leads to the blue trajectory in Frenet coordinates with minimized $e^\text{c}$ towards the path end.
:::
::::

This method can now be applied to another use case. If the goal of the motion plan is a pose $\boldsymbol{p}^\text{g}$ that lies not on the path but in its proximity, the weights can be adapted similarly. At first, the goal pose must be projected to the path, which yields its longitudinal position $\theta^\text{g}$. The weight $q^\text{c}$, which was increased before, must now be deactivated on approach to allow the vehicle to deviate from the path. Further, also the negative weight of the reward $\gamma$ to increase the progress along the reference path must be blended out because otherwise, the MPC would try to reach the path end. Hence, also an effective $\gamma^\text{eff}$ is calculated. This dynamic weight allocation is then calculated similarly as in Eq. [\[eq:qceff\]](#eq:qceff){reference-type="eqref" reference="eq:qceff"} by $$\begin{align}
\begin{split}
    \epsilon(\theta) &= \theta^\text{g} - \theta \\
    % \sigma(\theta) &= \frac{1}{1+e^{\,\alpha\cdot(\epsilon(\theta) - \beta)}}\\
    q^\text{c,eff}(\theta) &= (1-\sigma(\theta)) \cdot q^\text{c} \\
    \gamma^\text{eff}(\theta) &= (1-\sigma(\theta)) \cdot \gamma \, .\label{eq:qceff_inside_goal}
    \end{split}
\end{align}$$ In addition to that, we now reinsert the cost term belonging of the last trajectory state $\Delta\boldsymbol{x}_N$ to reach a specific reference position $\boldsymbol{x}_N^\text{r}$ which is set by the mentioned goal pose $\boldsymbol{p}^\text{g}$. Hence, the weight vector $\boldsymbol{q}_\text{N}$ must be changed as well into an effective $\boldsymbol{q}_N^\text{eff}$. Here, this weight is blended similarly as before, but in this case, it depends on the longitudinal position of the goal along the path $\theta^\text{g}$ to the longitudinal position of the base of the robot, which is denoted by $\theta_0$, and not of the trajectory states. An equal approach is not possible, as increasing the costs to reach the final goal causes an intermediate rise in the overall costs, which forces the trajectory to avoid the proximity of the goal completely. Consequently, the weights to reach the goal are calculated by $$\begin{align}
\begin{split}
    \epsilon_0 &= \theta^\text{e} - \theta_0 \\
    \sigma &= \frac{1}{1+e^{\,\alpha\cdot(\epsilon_0 - \beta)}} \\
    \boldsymbol{q}_N^{\text{eff}} &= \sigma \cdot \boldsymbol{q}_N^\text{e} + (1-\sigma)\cdot \boldsymbol{q}_N \, .
        \end{split}
\end{align}$$ With this formulation, the MPCC is able to reach goal poses that are longitudinally within the corridor. The dynamic weight allocation approach to reach the goal pose is also visualized schematically in Fig. [4](#fig:method:dyn_weight_goal){reference-type="ref" reference="fig:method:dyn_weight_goal"}.

:::: {#fig:method:dyn_weight_goal .figure latex-placement="t"}
::: caption
Schematic visualization of the dynamic weight allocation to reach a goal pose inside the corridor: The weights $\gamma^\text{eff}$ and $q^\text{c,eff}$ of states close to the projected longitudinal goal position $\theta^\text{g}$ are blended to zero. Now, the penalty $\boldsymbol{q}_N^\text{eff}$ to reach the goal pose dominates the behavior of the MPC. Hence, the algorithm plans precisely to the goal pose while being able to deviate from the reference path which is shown by the blue trajectory in Cartesian coordinates.
:::
::::

## Dynamic Objective Allocation {#sec:method:dyn_cost_type}

The method just proposed cannot be applied directly to scenarios in which the goal pose $\boldsymbol{p}^\text{g}$ lies longitudinally behind the corridor. In these cases, the MPCC cannot reach the pose, as the high penalty by $q^\text{l}$ prevents it from leaving the corridor longitudinally. Hence, we apply the dynamic weight allocation method to the weight of the longitudinal error $q^\text{l}$ and set it to zero for trajectory states that lie behind the path end ($\theta > \theta^\text{e}$). If the states lie within the corridor, we keep the default value $q^\text{l}$ to guarantee a valid Frenet state $\boldsymbol{x}^\text{F}$ at each stage. This leads to the following behavior: Behind the corridor, the contouring aspect of the MPCC is deactivated, and only the Cartesian penalty $\boldsymbol{q}_N$ of the final state $\boldsymbol{x}_N$ determines the behavior of the MPCC, which tries to reach the goal pose. This case distinction can be defined by $$\begin{align}
    q^\text{l,eff} = \begin{cases} q^\text{l} \quad &\text{for} \quad \theta < \theta^\text{e} \\
    0 \quad &\text{for} \quad \theta \ge \theta^\text{e}\end{cases} \,. \label{eq:case_dist}
\end{align}$$ Further, all possible penalties or constraints related to Frenet coordinates must be deactivated as well because there are no valid Frenet coordinates behind the path end.

:::: {#fig:dyn_cost_type .figure latex-placement="b"}
::: caption
Schematic visualization of the dynamic objective allocation: The purple curve at the top visualizes the drop of $q^\text{l, eff}$ caused by the case distinction from Eq. [\[eq:case_dist\]](#eq:case_dist){reference-type="eqref" reference="eq:case_dist"}. The other weights are equally blended as in Fig.[4](#fig:method:dyn_weight_goal){reference-type="ref" reference="fig:method:dyn_weight_goal"} In the lower part, the trajectory of a vehicle maneuvering to a goal pose is shown. For every state $\boldsymbol{x}$ with a $\theta \le \theta^\text{e}$, a corresponding reference exists on the reference path. For states behind the corridor with $\theta < \theta^\text{e}$, $q^\text{l, eff}$ is set to zero, which allows them to have no valid reference.
:::
::::

To summarize, a valid reference exists only for states inside the corridor. But for $\theta > \theta^e$, this pairing is no longer enforced, and the states are penalized as if they were part of a pure Cartesian MPC. Because this dynamic weight allocation not only increases or decreases the magnitude of weights but also completely changes the main objective of a trajectory state, we call this method dynamic objective allocation. The complete approach is visualized schematically in Fig. [5](#fig:dyn_cost_type){reference-type="ref" reference="fig:dyn_cost_type"}.

# Evaluation {#sec:eval}

This section comprises the evaluation of the two proposed methods. First, the evaluation of the dynamic weight allocation applied to path ends and direction switches, as well as goal poses, is shown, followed by the evaluation of the dynamic objective allocation approach. All following evaluations are executed using the same parameters, which are shown in Table [1](#tab:params){reference-type="ref" reference="tab:params"}. The MPC was created by using the Python API of acados [@acados2021]. The runtimes are $\approx \qty{1.7}{\milli\second}$ for a standard MPC run, $\approx \qty{3}{\milli\second}$ if new references are inserted, which is done every 100 ms, and $\approx \qty{7}{\milli\second}$ if the MPC is reset and reinitialized completely. These runtimes were determined on an AMD Ryzen 9 7950X with a base clock of 4.5 GHz.

[]{#tab:params label="tab:params"}

:::: center
::: {#tab:params}
            Parameter                         Description                           Value
  ----------------------------- ---------------------------------------- ----------------------------
               $T$                            time horizon                           7 s
               $N$                          number of stages                          70
        $\boldsymbol{q}$                     state weights                   $[0, 0, 0, 0, 0, 0]$
       $\boldsymbol{q}_N$                  goal pose weights                 $[0, 0, 0, 0, 0, 0]$
   $\boldsymbol{q}_N^\text{e}$   goal pose weights at $\theta^\text{g}$   $[1e4, 1e4, 1e4, 0, 0, 0]$
        $\boldsymbol{r}$                     input weights                     $[1e3, 100, 0]$
    $\boldsymbol{q}^\text{F}$                Frenet weights                   $[1e3, 1.0, 0.0]$
         $q^\text{c,e}$           lateral weight at $\theta^\text{e}$               $100$
            $\gamma$                penalty of progress $\dot\theta$                 -100
            $\alpha$                     steepness of sigmoids                      $1.0$
             $\beta$                       center of sigmoids                        10 m

  : MPC Parameters
:::
::::

## Dynamic Weight Allocation {#sec:eval:dyn_weigth}

:::: {#fig:eval:dyn_weight .figure latex-placement="t"}
::: caption
Driven trajectories for different constant lateral weights $q^\text{c}$ and our approach using the dynamic weight allocation method. Its effect can be observed when approaching the direction switch and the path end, which should be reached precisely. Our approach is able to reach both with high precision while smoothing out the other parts of the reference path.
:::
::::

In this section, the dynamic weight allocation is evaluated. This is done with a path-following scenario that contains one direction switch. At first, we compare our approach to the same MPC algorithm but with three different, fixed values of $q^\text{c}$. This comparison is shown in Fig. [6](#fig:eval:dyn_weight){reference-type="ref" reference="fig:eval:dyn_weight"}. It can be observed that with low values of $q^\text{c}$, the trajectory may vary from the reference path, leading to a smoother driven trajectory. Usually, this is the intended behavior to generate a smooth and comfortable trajectory. However, with low values of $q^\text{c}$, the trajectory does not reach the direction switches and the end of the path precisely. In contrast to that, our approach can generate smooth trajectories along the reference path while reaching the direction changes and the path end precisely by adapting the weight $q^\text{c,eff}$ depending on the proximity of the state to these regions. Hence, it inherently combines the advantages of low and high lateral penalties.

In addition to that, the dynamic weight allocation can be applied to reach goal poses inside a corridor. This objective is called Scenario 1 in the following. The effect of our method is compared to two other methods. All are MPC-based methods that only differ in the approach used to reach the final pose.

1\. The MPCC plans to the path end or a certain distance in front of the goal while already using the dynamic weight allocation. After reaching the specified position, the MPCC is exchanged by a pure Cartesian MPC, which plans to the final pose. This method is called *separated* in the following. Its separated architecture is similar to the docking approach used in the Nav2 stack.

2\. The MPCC plans along the corridor. If the vehicle is close enough to the goal pose, a Cartesian MPC replaces the MPCC during runtime to reach it. This method is called *switched* in the following.

The driven trajectories of all three methods are visualized in Fig. [7](#fig:eval:dyn_weight_goal){reference-type="ref" reference="fig:eval:dyn_weight_goal"}.

:::: {#fig:eval:dyn_weight_goal .figure latex-placement="t"}
::: caption
Scenario 1: Visualization of the second part of the corridor of Fig. [6](#fig:eval:dyn_weight){reference-type="ref" reference="fig:eval:dyn_weight"} after the switching point. Here, the goal pose lies within the corridor. *Our* approach reaches this pose smoothly without excessive steering angles. The *separated* baseline does not smooth the reference path and needs larger steering angles to reach the goal. Finally, the *switched* baseline requires the vehicle to make an additional direction change.
:::
::::

The *separated* method reaches the goal without direction in contrast to the *switched* approach, which does need an additional direction switch. In contrast to that, our approach begins to plan to the goal pose early enough and reaches it smoothly.

This behavior can be further analyzed in Fig. [8](#fig:eval:dyn_weight_velocity){reference-type="ref" reference="fig:eval:dyn_weight_velocity"}. Here, it can be seen that our method reaches the goal earlier in a fluent movement without stopping or direction changes. Further, the maximum applied steering angle is smaller. These trajectory details are further evaluated in Table [2](#tab:traj_comparison_1){reference-type="ref" reference="tab:traj_comparison_1"}. Here, the trajectories are compared quantitatively with different metrics adapted from the CommonRoad benchmarks [@althoff2017]. We evaluate the scenarios by calculating the Root Mean Square (RMS) values of various states and inputs of the trajectory. We compare the RMS values of the steering angle $\delta_\text{RMS}$, the change of the steering angle $\dot\delta_\text{RMS}$, the longitudinal acceleration $a^\perp_\text{RMS}$, and lateral acceleration $a^\parallel_\text{RMS}$. Low values indicate a smooth trajectory without excessive input changes or high acceleration values that can decrease passenger comfort. Further, steering angles smaller than the maximum possible angle are also important to allow the underlying low-level controller to follow the trajectory, which increases the overall system's robustness. Our approach outperforms the baseline approaches in all metrics except for the *separated* approach in which they share the same RMS of the change of the steering angle $\dot\delta_\text{RMS}$. Further, all trajectories reach the goal pose without collision.

[]{#tab:traj_comparison_1 label="tab:traj_comparison_1"}

:::: center
::: {#tab:traj_comparison_1}
    method         T       $\delta_\text{RMS}$   $\dot\delta_\text{RMS}$   $a^\parallel_\text{RMS}$   $a^\perp_\text{RMS}$    safe
  ----------- ----------- --------------------- ------------------------- -------------------------- ---------------------- ---------
     ours      **27.39**        **0.018**              **0.00021**               **0.00038**               **0.0012**        **yes**
   separated     41.68            0.037                **0.00021**                 0.00063                   0.0015          **yes**
   switched      49.29            0.059                  0.00095                   0.00051                   0.0024          **yes**

  : Scenario 1: Goal within the corridor
:::
::::

In addition to that, the times at which the goal pose was reached can be observed. Our approach reached the goal pose much earlier, with $T_\text{ours}\approx\qty{27}{\second}$, compared to $T_\text{sep.}\approx\qty{41}{\second}$ and $T_\text{switch}\approx\qty{49}{\second}$. These evaluations and all the following ones can also be observed in the video[^4] provided with this paper.

:::: {#fig:eval:dyn_weight_velocity .figure latex-placement="t"}
::: caption
Scenario 1: Driven velocities and steering angles of the scene in Fig. [7](#fig:eval:dyn_weight_goal){reference-type="ref" reference="fig:eval:dyn_weight_goal"}, in which the goal pose lies within the corridor. *Our* approach reaches the goal pose in about half the time compared to the *separated* and *switched* approaches while actuating lower steering angles $\delta$ and lower changes of the steering angle $\delta$, which can be estimated by the slope of the function.
:::
::::

## Dynamic Objective Allocation {#sec:eval:dyn_cost_type}

This section evaluates the dynamic objective allocation, which becomes relevant if a goal pose must be reached that is not longitudinally inside the corridor. This is called Scenario 2 in the following. In this case, the corridor boundaries were also modified to emulate a narrow environment close to the goal pose. Fig. [9](#fig:eval:dyn_cost){reference-type="ref" reference="fig:eval:dyn_cost"} visualizes the driven trajectories of the three different methods. Here, our method reaches the goal pose outside of the corridor smoothly while keeping its distance to the boundaries of the corridor. The *separated* method also reaches the goal pose with a comparable driven trajectory. However, it needs an additional direction change because the path end was not in an optimal position to plan to the goal pose. In contrast to these methods, the method using the *switched* baseline even collides with the corridor boundary near the end of the path. This is because if the MPCC is completely switched to a Cartesian MPC, the Frenet coordinates are no longer valid. Hence, all costs and constraints that are based on the Frenet coordinates are not calculated correctly, leading to the collision.

:::: {#fig:eval:dyn_cost .figure latex-placement="H"}
::: caption
Scenario 2: The goal pose lies behind the corridor end. Further, the corridor is narrowed by objects near the end. Our approach reaches the goal successfully while keeping distance to the corridor bounds, whereas the *switched* approach collides with the boundary marked by the orange circle. The *separated* approach also reaches the goal but needs an additional direction change.
:::
::::

To summarize, the problem is to define when it is safe to switch to the Cartesian MPC. Our proposed approach solves this problem inherently as the objective of each trajectory state is changed separately. The advantages of our approach can also be observed in Fig. [10](#fig:eval:dyn_cost_velocity){reference-type="ref" reference="fig:eval:dyn_cost_velocity"}. Here, the impact of the forced stop at the path end and the needed direction switches can be observed, leading to the *separated* baseline needing approximately double of the time.

:::: {#fig:eval:dyn_cost_velocity .figure latex-placement="t"}
::: caption
Scenario 2: Driven velocities and steering angles of the scene in Fig. [9](#fig:eval:dyn_cost){reference-type="ref" reference="fig:eval:dyn_cost"}, in which the goal pose lies outside of the corridor. The *separated* approach takes the longest time, in contrast to our method. The *switched* baseline is not shown as it collided and thus is not a valid baseline.
:::
::::

The three approaches are also compared quantitatively in Table [3](#tab:traj_comparison_2){reference-type="ref" reference="tab:traj_comparison_2"}. Our approach has the lowest $\delta_\text{RMS}$ and $\dot\delta_\text{RMS}$, while the *separated* baseline has the lowest $a^\perp_\text{RMS}$ and $a^\parallel_\text{RMS}$. In our approach, increasing the respective weights of the MPC could further lower the RMS values of both accelerations. Because our approach reaches the goal way earlier than the *separated* approach with $T_\text{ours}\approx\qty{30}{\second}$, compared to $T_\text{sep.}\approx\qty{63}{\second}$, the accelerations could thus be penalized more. However, as already mentioned, the parameters are equal for all methods to allow for a fair comparison. To summarize, our approach profits from the benefits of both baseline methods. It stays safe inside the corridor by keeping valid Frenet coordinates and plans inherently to the goal pose by switching the objective of all states behind the corridor to a pure cartesian one. This allows for the generation of a smooth and feasible trajectory.

[]{#tab:traj_comparison_2 label="tab:traj_comparison_2"}

:::: center
::: {#tab:traj_comparison_2}
    method         T       $\delta_\text{RMS}$   $\dot\delta_\text{RMS}$   $a^\parallel_\text{RMS}$   $a^\perp_\text{RMS}$             safe
  ----------- ----------- --------------------- ------------------------- -------------------------- ---------------------- --------------------------
     ours      **30.66**        **0.035**              **0.00045**                 0.00072                   0.0087                  **yes**
   separated     63.55            0.043                  0.0012                  **0.00024**               **0.0010**                **yes**
   switched    ~~31.38~~        ~~0.011~~              ~~0.00020~~               ~~0.00075~~               ~~0.0045~~        [no]{style="color: red"}

  : Scenario 2: Goal outside the corridor
:::
::::

## Evaluation of a docking maneuver in CARLA

This section evaluates the proposed approach on the docking maneuver of the U-Shift II concept vehicle [@ushift2]. It is an automated vehicle that can connect to different kinds of capsules, such as cargo capsules and public transport capsules. This was done to separate the vehicle platform from its use case, which increases the flexibility of the mobility concept. The vehicle can, for example, serve as a support vehicle for local bus fleets during rush hours and transport goods during the night, when few public transport vehicles are necessary. For capsule swapping, the vehicle must detect these capsules and dock to them. This is done by the pose estimation of so-called ChArUco boards [@garrido2014charuco]. More details about the automation of this vehicle can be found in  [@buchholz2025ushift].

Hence, this section evaluates our proposed approach on the docking maneuver to a capsule. The evaluation was done within the CARLA simulator [@carla2017] with a reduced set of sensors. In this case, only three cameras facing to the rear and two lidars were simulated. Fig. [11](#fig:eval:carla_scene){reference-type="ref" reference="fig:eval:carla_scene"} shows the initial scene.

:::: {#fig:eval:carla_scene .figure latex-placement="t"}
::: caption
Illustration of our software-in-the-loop test in CARLA. a) U-Shift vehicle on the left with two capsules on the right. The goal is to pickup the larger right one. b) The planned path and its corresponding trajectory on top of a grid map in Rviz [@macenski2022ros]. The driving corridor is denoted in black. The path planning algorithm plans to the estimated docking position of the capsule because the capsule's actual pose has not been measured yet. As soon as the capsule is detected, the estimated pose is passed to the dynamic objective MPC.
:::
::::

The goal pose for the proposed planning approach, is derived from the detected ChArUco board. The vehicle must reach this pose, being perfectly aligned right in front of the capsule to allow for successful docking. Then, the chassis of the vehicle is lowered for capsule pick-up, leading to very limited steering capabilities. Thus, almost only straight driving is possible. Because this process is difficult to visualize by figures only, the docking maneuver is also visualized under the already referenced link^[2](#fn:video){reference-type="ref" reference="fn:video"}^. The driven velocities and steering angles of the vehicle are shown in Fig. [12](#fig:eval:carla){reference-type="ref" reference="fig:eval:carla"}.

:::: {#fig:eval:carla .figure latex-placement="t"}
::: caption
Trajectory details of the docking maneuver in CARLA. Our approach generates a smooth trajectory to the goal pose at which the vehicle is lowered at $T_\text{goal}$. This takes some time, after which the vehicle reverses and connects with the capsule.
:::
::::

It can be observed that the vehicle drives forward and stops at the direction switch. Here, the cameras begin to detect the ChArUco board, which generates a dedicated goal pose for the planning algorithm. Hence, the vehicle continues to follow the path and seamlessly reaches the goal pose. At $T_\text{goal}\approx\qty{50}{\second}$, it stops to lower its chassis, which takes $\approx \qty{10}{\second}$, reverses slowly to its final position and attaches the capsule.

# Conclusion {#sec:conclusion}

In this paper, we introduced a new MPC-based planning approach called dynamic objective MPC for precise and seamless motion planning to different kinds of goals in narrow environments.

At first, we proposed an adapted dynamic weight allocation method to plan precisely to direction switches and path ends. This was the fundamental approach for the main contribution, called dynamic objective allocation. This novel method transforms an MPCC into a pure Cartesian MPC by state-dependent weight changes, allowing precise, safe, and seamless motion planning to specific goal poses in the proximity of a path without the need to change the planning algorithms. Our approach provides shorter times to reach the goal pose and smoother trajectories compared to the baseline approaches. Further, this approach can be used for seamless docking maneuvers, as shown in a software-in-the-loop simulation in CARLA in which a docking maneuver of the U-Shift concept vehicle to a capsule was shown.

In future work, we want to investigate how the dynamic weight allocation and dynamic objective allocation methods affect the stability of the MPC and under what circumstances the stability of the approach can be assured. At last, we want to apply this algorithm in real-world scenarios of the U-Shift concept vehicle, in which it will be used for normal trajectory planning and docking maneuvers.

[^1]: This work was supported by the State Ministry of Economic Affairs, Labour and Tourism Baden-Württemberg (project U-Shift II, AZ 3-433.62-DLR/60).

[^2]: All authors are with the Institute of Measurement, Control and Microtechnology, Ulm University, Albert-Einstein-Allee 41, 89081 Ulm, Germany `{firstname}.{lastname}@uni-ulm.de`

[^3]: [github.com/uulm-mrm/dynamic_objective_mpc](https://github.com/uulm-mrm/dynamic_objective_mpc)

[^4]: []{#fn:video label="fn:video"}<https://youtu.be/28X5zaHW6bs>
