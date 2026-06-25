---
citation_key: Lee2024Performance
arxiv_id: 2404.07889
arxiv_url: https://arxiv.org/abs/2404.07889
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-24T15:40:31Z
origin: ai+web
reviewed: false
---

::: keywords
Time-Optimal Trajectory Planning, Jerk Constraints, Smooth Trajectory Generation, Industrial Robots
:::

# INTRODUCTION

In automation, time-optimal motion planning plays a crucial role in maximizing productivity while ensuring efficiency and safety. However, solving the complete trajectory-planning problem is often difficult to perform in real time [@chettibi2004minimum; @diehl2006fast; @schulman2013finding; @zhao2018efficient; @zhang2022time]. To obtain satisfactory results using reasonable computational resources, trajectory planning is often solved in two stages [@shin1985minimum; @shiller1989robot; @shiller1991computing]. As shown in Fig. [1](#fig:architecture){reference-type="ref" reference="fig:architecture"}, during the initial stage, the path generator creates a geometric path that incorporates task specifications and obstacle avoidance. In the subsequent stage, a time-optimal trajectory is calculated along the specified geometric path, enforcing constraints such as permissible joint velocity and torque.

:::: {#fig:architecture .figure latex-placement="t!"}
![](Lee2024Performance_figs/control_architecture.png){width="95%"}

::: caption
Two-Stage Motion Planning and Control Architecture: The path generator creates a collision-free path, which is fed into the time-optimal trajectory planner to compute the desired trajectory satisfying robot hardware limits. Subsequently, the predictive proportional-integral (PPI) controller generates high-frequency joint commands with feedback.
:::
::::

This paper focuses on solving the second-stage motion planning sub-problem, also known as time-optimal trajectory planning (TOTP) or path tracking (TOPT) [@bobrow1985time; @pfeiffer1987concept]. Although TOTP under first- and second-order constraints (such as velocity, acceleration, and torque limits) has been thoroughly explored, third-order constraints such as jerk or torque rate bounds are often overlooked. This is primarily because their inclusion lacks clear guidance (for instance, these bounds may not be specified in motor usage requirements), and they introduce non-convex terms into the formulation, making problem-solving much more challenging. However, without considering jerk limits, solution trajectories may include large acceleration jumps, resulting in various issues when applied to real robots [@eager2016beyond].

In this paper, we propose a new approach for TOTP with practical third-order constraints. By incorporating jerk limits into trajectory planning and control strategies, robotic systems can achieve higher reliability and effectiveness. Some well-known advantages include: 1) Enhanced path tracking: a smoother trajectory allows the robot's movements to more closely match the desired trajectory, minimizing jerk-induced vibrations. 2) Reduced wear and tear: Sudden changes in acceleration can subject mechanical components to higher stress levels. By constraining jerk, the robot's motor gears undergo gentler transitions, extending component lifespans. 3) Energy efficiency: Jerk-limited motions prevent unnecessary spikes in power consumption, leading to decreased energy usage and reduced operational costs.

Finally, we perform real robot experiments to confirm the benefits of including jerk limits. We analyze factors such as peak power and torque, which affect the performance, durability, and maintainability of the robot. The proposed motion planning and control framework is depicted in Fig. [1](#fig:architecture){reference-type="ref" reference="fig:architecture"}.

## Related Works

Traditionally, there are two widely adopted approaches for addressing time-optimal trajectory planning (TOTP): numerical integration (NI), and convex optimization (CO). NI-based approaches [@bobrow1985time; @pfeiffer1987concept; @pham2014general] solve the problem based on the insight that one can obtain a time-optimal trajectory through bang-bang control. However, this method requires identifying switch points where acceleration changes, and it is prone to failure in certain cases. Conversely, optimization provides a general and robust means to formulate and solve the problem [@verscheure2009time; @hauser2014fast]. However, it increases the problem's complexity by at least an order of magnitude, resulting in longer computation times. Other works solve the problem using dynamic programming [@shin1986dynamic; @singh1987optimality] or by leveraging specific conditions which may be too constraining, such as imposing constant first- or second-order limits in the path parameter space [@haschke2008line; @berscheid2021jerk], which may not map to desired (e.g., constant) limits in the joint space.

Recently, there have been efforts to simplify TOTP algorithms through methods based in reachability analysis (RA) [@pham2018new; @consolini2019optimal]. These methods, instead of solving a high-dimensional optimization problem (with $n$ optimization variables, one for each timestep), can achieve the optimal solution by solving a series of 2$n$ 2-D sub-problems. However, it's worth noting that these reachability-based algorithms are restricted to second-order constraints, since they cannot handle situations where second-order constraints violate the third-order constraints, known as third-order singularity [@pham2017structure].

Many works have attempted to incorporate third-order constraints into time-optimal trajectory planning (TOTP). Many of them rely on the NI-based approaches [@pham2017structure; @ma2021new; @mattmuller2009calculating; @wang2021third]. In [@ma2021new], however, this formulation is limited to bounding the third-order derivative of the path parameter ($\dddot{s}$) rather than directly limiting the robot jerk or torque rate, and the third-order singularity issue is not addressed. Instead, one can carefully bridge the maximum and minimum jerk profile to avoid failure from singularity [@pham2017structure]. However, this approach requires handling numerous exceptional cases, making the algorithm overly complex when adding first and second-order constraints, which are often more critical [@wang2021third].

Our approach provides a more general formulation within a convex optimization framework. A key challenge is enforcing nonlinear third-order inequality constraints, as approximating them without careful consideration can lead to solutions that violate real constraints. An alternative is to minimize both jerk and time [@lu2017solving], but this requires careful tuning of the relative weight for jerk and time in the cost function. Since the solutions of the optimization problem are often very sensitive to the weight, the solution can frequently sacrifice motion time or smoothness excessively depending on the input path given, even under the same weight. In this paper, we formulate the problem as an SLP using conservative linearization of the nonlinear constraints at each iteration to ensure solution feasibility. The work in [@zhang2013practical] also used conservative approximation for third-order constraints, based on the fact that torque obtained without third-order constraints is always bigger than the one with third-order constraints. Thus, their approach is limited to a one-time approximation, which can lead to suboptimal solutions, with stricter limits often widening the optimality gap.

## Contribution

- We formulate a unique TOTP with third-order constraints as a Sequential Linear Program (SLP), exceeding the performance of existing methods.

- We introduce a method for approximating general third-order constraints, enabling iterative optimization to converge to the optimal solution.

- We demonstrate that imposing jerk limits significantly reduces peak power, enhances energy efficiency, and improves tracking performance.

## Organization

The paper is organized as follows. Section [2](#sec:preliminaries){reference-type="ref" reference="sec:preliminaries"} revisits the concepts of TOTP and the corresponding parameterization methods. Section [3](#sec:jerktotp){reference-type="ref" reference="sec:jerktotp"} formulates the jerk constraints for TOTP and outlines the overall optimization process with the approximated jerk constraints. In Section [4](#sec:experiment){reference-type="ref" reference="sec:experiment"}, we discuss the numerical and experimental results of the proposed jerk-bounded time-optimal trajectory planning. Finally, in Section [5](#sec:conclusion){reference-type="ref" reference="sec:conclusion"} we discuss conclusions and future work.

# PRELIMINARIES {#sec:preliminaries}

## Problem Formulation

We formulate time-optimal trajectory planning (TOTP) as follows: Given a path $\mathbf{q}(s)$ as a function of a scalar path coordinate $s\in[0,1]$, find a monotonically increasing time scaling $s(t) :[0,T] \rightarrow [0,1]$ that

- satisfies an initial state $(s_0,\dot{s}_0)=(0,0)$ and a final state $(s_\textrm{end},\dot{s}_\textrm{end})=(1,0)$,

- minimizes the total travel time $T$ along the path,

- enforces kinematics and dynamics constraints imposed by robot hardware limitations.

## Time-Optimal Trajectory Planning (TOTP) 

For the purpose of solving the TOTP problem to track the prescribed path $\mathbf{q}(s)$ for a robot manipulator, we express the first- and second-order time derivatives of $\mathbf{q}(s)$ as $$\begin{eqnarray}
\dot{\mathbf{q}}(s) = \mathbf{q}'(s)\dot{s}, \quad \ddot{\mathbf{q}}(s)=\mathbf{q}''(s)\dot{s}^2+\mathbf{q}'(s)\ddot{s}.
\end{eqnarray}$$ We also transform the dynamics of the manipulator into $$\begin{align}
\boldsymbol{\tau}&~= M(\mathbf{q})\ddot{\mathbf{q}} + C(\mathbf{q}, \dot{\mathbf{q}})\dot{\mathbf{q}} + g(\mathbf{q})  \nonumber \\
 &~= M(\mathbf{q})(\mathbf{q}''\dot{s}^2+\mathbf{q}'\ddot{s}) + C(\mathbf{q}, \mathbf{q}')\mathbf{q}' \dot{s}^2 + g(\mathbf{q})  \nonumber \\
&:= \mathbf{m}(s)\ddot{s} + \mathbf{c}(s)\dot{s}^2 + \mathbf{g}(s) \label{eqn:parameterized_dyn}.
\end{align}$$ Note that from the linear nature of the Coriolis matrix, we have $C(\mathbf{q}, \mathbf{q}'\dot{s})\mathbf{q}' \dot{s} = C(\mathbf{q}, \mathbf{q}')\mathbf{q}' \dot{s}^2$ above.

Furthermore, it is known that a second-order time differential equation can be transformed into a first-order differential equation in $(\dot{s}^2, s)$ based on the relation introduced in [@pfeiffer1987concept], $$\begin{eqnarray}
\ddot{s} = \frac{d\dot{s}}{dt} =  \frac{d\dot{s}}{ds}\frac{ds}{dt} = \dot{s}'\dot{s}=\frac{1}{2}(\dot{s}^2)'.
\label{eqn:uandx}
\end{eqnarray}$$ This is beneficial for solving TOTP problems, as it allows writing all the equations in linear form by setting ($\dot{s}^2, \ddot{s}$) as optimization variables [@pham2018new; @verscheure2009time].

## TOTP Constraints in the Discretized System

We now show that we can express all constraints up to second-order as linear in $x=\dot{s}^2$ for the discretized system. By dividing the path interval $[0,1]$ into $N$ segments, we have $$\begin{eqnarray*}
0=:s_0, s_1,...,s_{N-1},s_N:=1.
\end{eqnarray*}$$ Then from the relation in [\[eqn:uandx\]](#eqn:uandx){reference-type="eqref" reference="eqn:uandx"}, $\dot{s}_k, \ddot{s}_k$ can be represented as: $$\begin{equation}
\dot{s}_k^2 := x_k, \quad \ddot{s}_k = \frac{x_{k+1}-x_k}{2\triangle_k} \quad\textrm{or}\quad \frac{x_{k}-x_{k-1}}{2\triangle_{k-1}} \label{eqn:def_sdot_sddot},
\end{equation}$$ where $\triangle_k :=s_{k+1}-s_k$ and $\triangle_{k-1} :=s_{k}-s_{k-1}$.

For representational convenience, we simplify the notation of each quantity at $s_k$ as $(\cdot)(s_k)=(\cdot)_k$. Instead of introducing another optimization variable $u=\ddot{s}$ like other works [@pham2018new], we express all quantities as linear in $x$, which is sufficient. Finally, we formulate the following constraints:

- **Velocity limits (1st-order constraints)** First, the joint velocity limit can be represented as $$\begin{eqnarray}
       \dot{\mathbf{q}}_k \circ \dot{\mathbf{q}}_k  = (\mathbf{q}_k' \circ \mathbf{q}_k') x_k &\leq& \dot{\mathbf{q}}_{k}^{max} \circ \dot{\mathbf{q}}_{k}^{max}, \label{eqn:1stvel}
  \end{eqnarray}$$ where $\mathbf{a} \circ \mathbf{b}$ represents the Hadamard product (i.e., the element-wise product) of two vectors.

- **Acceleration limits (2nd-order constraints)** Similarly, from the parameterized expression of acceleration $$\ddot{\mathbf{q}}_k  = \mathbf{q}''_k\dot{s_k}^2 + \mathbf{q}'_k\ddot{s}_k =  \mathbf{q}''_k x_k + \mathbf{q}'_k\left(\frac{x_{k+1}-x_k}{2\triangle_k}\right),$$ we can constrain two consecutive $x_k$ by $$\begin{align}
    \left|  \frac{\mathbf{q}'_k}{2\triangle_k} x_{k+1} + \left(\mathbf{q}''_k - \frac{\mathbf{q}'_k}{2\triangle_k}\right) x_k \right| \leq \ddot{\mathbf{q}}_k^{max} & \nonumber \\ 
  \textrm{or}\quad \left|  \left(\mathbf{q}''_k + \frac{\mathbf{q}'_k}{2\triangle_{k-1}}\right) x_k - \frac{\mathbf{q}'_k}{2\triangle_{k-1}} x_{k-1} \right| \leq \ddot{\mathbf{q}}_k^{max}. &
   \label{eqn:2ndacc}
  \end{align}$$

- **Torque limits (2nd-order constraints)** The parameterized dynamics can also be rewritten with respect to $x$ by substituting [\[eqn:def_sdot_sddot\]](#eqn:def_sdot_sddot){reference-type="eqref" reference="eqn:def_sdot_sddot"} into [\[eqn:parameterized_dyn\]](#eqn:parameterized_dyn){reference-type="eqref" reference="eqn:parameterized_dyn"}: $$\begin{align}
  % \left| \mathbf{m}_k\ddot{s}_k + \mathbf{c}_k\dot{s}_k^2 + \mathbf{g}_k \right| &\leq \btau_k^{max} \nonumber \\
   \left| \frac{\mathbf{m}_k}{2\triangle_k}x_{k+1}  + \left(\mathbf{c}_k-\frac{\mathbf{m}_k}{2\triangle_k}\right) x_k + \mathbf{g}_k \right| &\leq \boldsymbol{\tau}_k^{max}  \label{eqn:2ndtrq}  \nonumber  \\
   \textrm{or}~ \left| \left(\mathbf{c}_k+\frac{\mathbf{m}_k}{2\triangle_{k-1}}\right)x_{k}  - \frac{\mathbf{m}_k}{2\triangle_{k-1}} x_{k-1} + \mathbf{g}_k \right| &\leq \boldsymbol{\tau}_k^{max}.
  \end{align}$$

By stacking up all the constraints derived above, we can simply express first-order constraints as $\boldsymbol{\omega}_k x_k \leq \boldsymbol{\nu}_k$, where $\boldsymbol{\omega}_k =  \mathbf{q}_k' \circ \mathbf{q}_k'$ and $\boldsymbol{\nu}_k = \dot{\mathbf{q}}_{k}^{max} \circ \dot{\mathbf{q}}_{k}^{max}$. Similarly, second-order constraints can be represented in the form of $\boldsymbol{\alpha}_k^0 x_k + \boldsymbol{\alpha}_k^1 x_{k+1} \leq \boldsymbol{\beta}_k$.

# Jerk-Constrained Time-Optimal Trajectory Planning {#sec:jerktotp}

## Jerk Constraint Formulation

Suppose we want to enforce joint-level jerk bounds $$\begin{equation}
 \label{eqn:jerkbound}
-\dddot{\mathbf{q}}_\textrm{max} \leq \dddot{\mathbf{q}} \leq \dddot{\mathbf{q}}_\textrm{max} .
\end{equation}$$ In this paper, we define jerk as change in acceleration between adjacent trajectory points. While this formula is more forgiving than an instantaneous rate, it is still effective in preventing abrupt changes in acceleration and simplifies the formulation. Additional details can be found in Section [5](#sec:conclusion){reference-type="ref" reference="sec:conclusion"}. Then joint jerk given the discretized system can be formulated as: $$\begin{align}
\dddot{\mathbf{q}}_k = \frac{\Delta \ddot{\mathbf{q}}}{\Delta t} (s_k)  &= \frac{\left(\ddot{\mathbf{q}}_{k+1}-\ddot{\mathbf{q}}_k\right)}{\frac{1}{2}(\triangle t_{k+1} + \triangle t_k)} \nonumber \\
 &= \frac{\mathbf{j}_k^2x_{k+2} + \mathbf{j}_k^1x_{k+1} + \mathbf{j}_k^0x_{k}}{h_k(\mathbf{x}_{k:k+2})} \label{eqn:jerk},
\shortintertext{where}
 \mathbf{x}_{k:k+2} &= [x_k ~ x_{k+1} ~ x_{k+2}]^\top \nonumber \\
h_k(\mathbf{x}_{k:k+2}) &=  {\dfrac{\triangle_{k+1}}{\sqrt{x_{k+2}}+\sqrt{x_{k+1}}}
 +\dfrac{\triangle_{k}}{\sqrt{x_{k+1}}+\sqrt{x_{k}}}} \nonumber
\end{align}$$ $$\begin{align*}
\mathbf{j}_k^2 =\frac{\mathbf{q}'_{k+1}}{2\triangle_{k+1}}&, \quad \mathbf{j}_k^1 = \mathbf{q}''_{k+1}-\frac{\mathbf{q}'_{k+1}}{2\triangle_{k+1}}-\frac{\mathbf{q}'_{k}}{2\triangle_{k}},  
 \mathbf{j}_k^0 &=  - \mathbf{q}_k''+\frac{\mathbf{q}_k'}{2\triangle_k} \nonumber.
\end{align*}$$

Unfortunately, unlike second- or lower-order constraints, a nonlinear term such as $h_k(\mathbf{x}_{k:k+2})$ in Eqn. [\[eqn:jerk\]](#eqn:jerk){reference-type="eqref" reference="eqn:jerk"} always remains when expressing jerk in the TOTP problem. We address this issue by linearizing the nonlinear term $h_k(\mathbf{x}_{k:k+2})$ and leveraging its convexity to ensure the solution always satisfies the original constraints, i.e.,

$$\begin{align*}
h_k(\mathbf{x}_{k:k+2}) &\geq h_k(\bar{\mathbf{x}}_{k:k+2}) + \nabla h_k(\bar{\mathbf{x}}_{k:k+2})({\mathbf{x}}_{k:k+2} - \bar{\mathbf{x}}_{k:k+2}) \\
&:= \bar{h}_k + \bar{h}_k^2x_{k+2} + \bar{h}_k^1x_{k+1} + \bar{h}_k^0x_{k},
\end{align*}$$ where $$\begin{align*}
\bar{h}_k^i&=\frac{\partial h_k(\mathbf{x}_{k:k+2})}{\partial x_{k+i}}\bigg|_{\mathbf{x}=\mathbf{\bar{x}}}, \quad  i \in \{0,1,2\},\\
\bar{h}_k &=h_k(\bar{\mathbf{x}}_{k:k+2}) - \bar{h}_k^2 \bar{x}_{k+2}-\bar{h}_k^1 \bar{x}_{k+1}-\bar{h}_k^0 \bar{x}_{k}.
\end{align*}$$ We show the convexity of this function in the Appendix. From this, we can reformulate the joint jerk constraints as $$\begin{align*}
\big|~ \mathbf{j}_k^2x_{k+2} &+ \mathbf{j}_k^1x_{k+1} + \mathbf{j}_k^0x_{k} ~\big| \\
&\leq  \dddot{\mathbf{q}}_\textrm{max} \left( \bar{h}_k + \bar{h}_k^2x_{k+2} + \bar{h}_k^1x_{k+1} + \bar{h}_k^0x_{k} \right) \\
&\leq \dddot{\mathbf{q}}_\textrm{max} h_k(\mathbf{x}_{k:k+2}) ,
\end{align*}$$ which finally leads to the linear form of 3rd-order constraints: $$\boldsymbol{\gamma}_k^0 x_k + \boldsymbol{\gamma}_k^1 x_{k+1} + \boldsymbol{\gamma}_k^2 x_{k+2} \leq \boldsymbol{\eta}_k.$$ We can now combine all first- to third-order constraints as a linear matrix inequality:

::: numcases
[1st order constraints:]{.roman}&$\boldsymbol{\omega}_k x_k \leq \boldsymbol{\nu}_k$\
[2nd order constraints:]{.roman}&$\boldsymbol{\alpha}_k^0 x_k + \boldsymbol{\alpha}_k^1 x_{k+1} \leq \boldsymbol{\beta}_k$ []{#eqn:1and2and3 label="eqn:1and2and3"}\
[3rd order constraints:]{.roman}&$\boldsymbol{\gamma}_k^0 x_k + \boldsymbol{\gamma}_k^1 x_{k+1} + \boldsymbol{\gamma}_k^2 x_{k+2} \leq \boldsymbol{\eta}_k$
:::

:::: {#fig:snapshot .figure latex-placement="t!"}
![](Lee2024Performance_figs/snapshots_all.png){width="\\linewidth"}

::: caption
Test motion snapshots. A: Front place motion to move boxes from a conveyor to the top of a virtual stack of packages. B: Pre-pick motion preparing to pick a box from a conveyor: C. Bottom place motion to place boxes onto the bottom of the truck. D: Post-place motion to return to the ready pose after placing boxes. E and F show box unloading motions, which return the box from a stack of packages to the conveyor with and without jerk constraints. Without jerk constraints, the robot's suction gripper is also more likely to lose grasp of the box.
:::
::::

## Trajectory Optimization

The cost function for minimizing the total time required to follow the given path can be expressed as $$\begin{equation}
    f(\mathbf{x}) = \sum_{i=0}^{N-1} \frac{s_{i+1}-s_{i}}{\sqrt{x_i}+\sqrt{x_{i+1}}},
\end{equation}$$ which can be linearized along the nominal trajectory $\bar{\mathbf{x}}$.

Now we formulate the trajectory optimization problem as a Sequential Linear Program (SLP), where the optimization variables are $\mathbf{x} = [x_1, \cdots, x_{N-1}]^\top$ as follows: $$\begin{align}
& \min_{\mathbf{x}} \quad \mathbf{c}^\top\mathbf{x}  \label{eqn:opt} \\
& \textrm{subject to}\quad A \mathbf{x} \leq b, \nonumber
\end{align}$$ where $$\begin{equation}
\mathbf{c} = \frac{\partial f}{\partial \mathbf{x}}\bigg\vert_{\mathbf{x}=\mathbf{\bar{x}}} \label{eqn:constraints}, \; A = \begin{bmatrix}  A^1 \\ A^2 \\ A^3  \end{bmatrix},\; b = \begin{bmatrix}  b^1 \\ b^2 \\ b^3 \end{bmatrix} \nonumber
\end{equation}$$ $$\begin{align}
A^1 &= \begin{bmatrix}
\boldsymbol{\omega}_1 & 0 & \cdots & 0 \\
\vdots & &  & \vdots \\
 0 & \cdots & 0 & \boldsymbol{\omega}_{N-1} 
\end{bmatrix}, %
\quad\;\; b^1 = \begin{bmatrix}
\boldsymbol{\nu}_1 \\ \vdots \\ \boldsymbol{\nu}_{N-1} 
\end{bmatrix}, \nonumber \\
A^2 &= \begin{bmatrix}
\boldsymbol{\alpha}^1_{0} & 0 & \cdots & 0 \\
\boldsymbol{\alpha}^0_{1} & \boldsymbol{\alpha}^1_{1} & \cdots & 0 \\
\vdots & & & \vdots \\
0 & \cdots & \boldsymbol{\alpha}^0_{N-2} & \boldsymbol{\alpha}^1_{N-2}   \\
0 & \cdots & \cdots & \boldsymbol{\alpha}^0_{N-1}   
\end{bmatrix}, %
b^2 = \begin{bmatrix}
\boldsymbol{\beta}_{0}-\boldsymbol{\alpha}_0^0x_0 \\
\boldsymbol{\beta}_{1} \\ \vdots \\ \boldsymbol{\beta}_{N-2} \\ 
\boldsymbol{\beta}_{N-1} - \boldsymbol{\alpha}_{N-1}^1x_N
\end{bmatrix}, \nonumber \\
A^3 &= \begin{bmatrix}
\boldsymbol{\gamma}^2_0 & 0 & 0 & 0 & \cdots & 0 \\
\boldsymbol{\gamma}^1_1 & \boldsymbol{\gamma}^2_1 & 0 & 0 & \cdots & 0 \\
\boldsymbol{\gamma}^0_2 & \boldsymbol{\gamma}^1_2 & \boldsymbol{\gamma}^2_2 & 0 & \cdots & 0 \\
\vdots & & \vdots & \ddots & \ddots & \vdots \\
0 & \cdots & 0 & \boldsymbol{\gamma}^0_{N-3} & \boldsymbol{\gamma}^1_{N-3} & \boldsymbol{\gamma}^2_{N-3}\\
0 & \cdots & 0 & 0 & \boldsymbol{\gamma}^0_{N-2} & \boldsymbol{\gamma}^1_{N-2}
\end{bmatrix}, \label{eqn:A3} \\
b^3 &= \begin{bmatrix}  \boldsymbol{\eta}_0 - \boldsymbol{\gamma}^0_0 x_0 -\boldsymbol{\gamma}^1_0 x_1 \\
 \boldsymbol{\eta}_{1} - \boldsymbol{\gamma}^0_{1}x_1 \\
 \boldsymbol{\eta}_{2} \\ \vdots \\ \boldsymbol{\eta}_{N-3} \\ \boldsymbol{\eta}_{N-2} - \boldsymbol{\gamma}^2_{N-2} x_N
\end{bmatrix}.
\label{eqn:b3}
\end{align}$$

Note that due to the linearization, we need to iteratively update the nominal trajectory to reformulate the coefficients for cost function and 3rd-order constraints. The steps of the resulting algorithm are shown in Algorithm [\[alg:cap\]](#alg:cap){reference-type="ref" reference="alg:cap"}.

:::: algorithm
::: algorithmic
Nominal variables $\bar{\mathbf{x}}_{1:N}$ Update $\mathbf{c}, A^3, b^3$ $\mathbf{x}_{1:N}$ = solve LP break Update $\bar{\mathbf{x}}_{1:N}$
:::
::::

:::: {#fig:s_sdot .figure latex-placement="b!"}
![](Lee2024Performance_figs/s_sdot_plot_revised.png){width="85%"}

::: caption
Comparison of the velocity curve for the pre-pick motion (Fig. [2](#fig:snapshot){reference-type="ref" reference="fig:snapshot"}B) computed from TOPP-RA [@pham2018new] without jerk limits (black), [@zhang2013practical] with pseudo jerk limits (blue) and the proposed approach with jerk limits (red).
:::
::::

# EXPERIMENT RESULTS {#sec:experiment}

In this section, we provide experimental results to validate the effectiveness of the proposed approach.

:::: {#fig:performance .figure latex-placement="ht!"}
![](Lee2024Performance_figs/robotperformance_revised.png){width="\\linewidth"}

::: caption
Algorithm performance comparison on real-robot for the front place motion (Fig. [2](#fig:snapshot){reference-type="ref" reference="fig:snapshot"}A): **A** shows tracking performance of the algorithms with and without jerk limits by comparing the desired, commanded, and actual joint position and velocity. **B** shows the corresponding estimated torque and power.
:::
::::

:::: {#fig:jerkplot .figure latex-placement="ht!"}
![](Lee2024Performance_figs/jerkplot_revised.png){width="\\linewidth"}

::: caption
Time-optimal trajectory generated for the front place motion (Fig. [2](#fig:snapshot){reference-type="ref" reference="fig:snapshot"}A) without jerk limits (blue) and with jerk limits (red).
:::
::::

## Experiment Setup

For practical evaluation, we used an example motion from a real-world box-loading application. We performed the test motions depicted and described in Fig. [2](#fig:snapshot){reference-type="ref" reference="fig:snapshot"} with and without the jerk limit. We used the output from TOPP-RA [@pham2018new] as the initial nominal trajectory for our algorithm and as a comparison target for the optimal trajectory without the jerk limit. Finally, the jerk limits were heuristically chosen to be $100 \sim 1000 
 \textnormal{ rad}/\textnormal{s}^3$, balancing the trade-off between motion duration and overall performance metrics such as energy efficiency and tracking (note that some applications may require more specific strict limitations on jerk). Lastly, we used 7-DOF robotic system composed of a 6-DOF RS020N Kawasaki arm mounted on an additional revolute joint for our experiment.

## Comparison With TOPP-RA 

### Simulation Results

We compare the TOTP outcomes obtained by three different methods in the phase plane. These methods include TOPP-RA [@pham2018new] without jerk limits, TOTP3 [@zhang2013practical] with pseudo jerk limits, and our proposed approach with jerk limits. While the original work in [@zhang2013practical] focused on torque rate constraints, we adapted it for our experiment by introducing jerk limits. We employed a similar methodology to the one used for pseudo-torque rate to establish the pseudo-jerk limit. Fig. [3](#fig:s_sdot){reference-type="ref" reference="fig:s_sdot"} shows that the curve tends to have a smoother shape when jerk limits are enforced. Note that since we formulate jerk limits in joint space and then map them to the space of the path parameter $s$, the smoothness of the joint-space curves along the path may vary at different path points. The result shows that the proposed approach yields faster motion than the pseudo-torque rate method under the same limits. To highlight the optimality gap, we applied a very stringent jerk limit of $100 \textnormal{ rad}/\textnormal{s}^3$.

Fig. [5](#fig:jerkplot){reference-type="ref" reference="fig:jerkplot"} illustrates the computed velocity, acceleration, and jerk with the corresponding limits for the significant axes of the robot. It demonstrates that by enforcing a jerk limit, rapid changes in acceleration are mitigated, leading to a smoother velocity profile.

### Robot Implementation Results

While we can observe jerk limits producing a smoother trajectory in simulation, we must still establish their tangible benefits on a real robot. We performed a comparative test on the real Kawasaki robot system described above, running the same path with and without jerk limits. The results are shown in Fig. [4](#fig:performance){reference-type="ref" reference="fig:performance"}.

Fig. [4](#fig:performance){reference-type="ref" reference="fig:performance"}A shows that the robot deviated from its desired path during rapid acceleration changes, leading to overshooting and increased fluctuations in the velocity plots. However, applying jerk limits significantly smoothed the motions, resulting in differences in the generated torque and power, as illustrated in Fig. [4](#fig:performance){reference-type="ref" reference="fig:performance"}B. The jerk-limited motions prevented aggressive velocity spikes, lowering peak power and torque usage, with significant reductions for some joints.

We measured peak power and RMS torque and the results are presented in Table [3](#tab:energy){reference-type="ref" reference="tab:energy"}, showing that peak power was reduced by about 25%, and RMS torque was reduced to half of its original value by limiting jerk.

::: {#tab:energy}
+---------------------------------------------------------+---------------------------------------------------+-----+
| 3-9                                                     | Axis                                              |     |
+:=======================================================:+:=======:+:====:+:====:+:====:+:====:+:====:+:====:+:===:+
| 3-9                                                     | 0       | 1    | 2    | 3    | 4    | 5    | 6    |     |
+---------------------------------------------------------+---------+------+------+------+------+------+------+-----+
| ::: {#tab:energy}                                       | TOPP-RA | 3624 | 965  | 32   | 73   | 795  | 100  | 28  |
|   ---------                                             |         |      |      |      |      |      |      |     |
|    RMS Trq                                              |         |      |      |      |      |      |      |     |
|     \[Nm\]                                              |         |      |      |      |      |      |      |     |
|   ---------                                             |         |      |      |      |      |      |      |     |
|                                                         |         |      |      |      |      |      |      |     |
|   : RMS torque and peak power during front place motion |         |      |      |      |      |      |      |     |
| :::                                                     |         |      |      |      |      |      |      |     |
|                                                         +---------+------+------+------+------+------+------+-----+
|                                                         | TOTP3   | 1504 | 377  | 14   | 77   | 267  | 35   | 6.4 |
+---------------------------------------------------------+---------+------+------+------+------+------+------+-----+
| ::: {#tab:energy}                                       | TOPP-RA | 1119 | 113  | 57   | 40   | 102  | 18   | 8.5 |
|   ----------------------------                          |         |      |      |      |      |      |      |     |
|             Peak Pwr                                    |         |      |      |      |      |      |      |     |
|     \[$\textnormal{Nm}^2$/s\]                           |         |      |      |      |      |      |      |     |
|   ----------------------------                          |         |      |      |      |      |      |      |     |
|                                                         |         |      |      |      |      |      |      |     |
|   : RMS torque and peak power during front place motion |         |      |      |      |      |      |      |     |
| :::                                                     |         |      |      |      |      |      |      |     |
|                                                         +---------+------+------+------+------+------+------+-----+
|                                                         | TOTP3   | 612  | 67   | 27   | 38   | 34   | 6.6  | 1.2 |
+---------------------------------------------------------+---------+------+------+------+------+------+------+-----+

: RMS torque and peak power during front place motion
:::

[]{#tab:energy label="tab:energy"}

### Algorithm Efficiency

We ran experiments via a C++ implementation running on a 64-bit system with a 2.35 GHz AMD EPYC 7452 32-core processor. To show the algorithm's efficiency, we measured the computation time of TOTP3 and TOPP-RA by averaging 20 trials of box-place motions. Each trial involved 20-30 path points beginning from slightly different initial box lift poses. TOTP3 (w/ jerk limit) took $7.533 \pm 5.848$ ms while TOPP-RA (w/o jerk limit) took $0.273 \pm 0.089$ ms to obtain the solution. The TOPT3 algorithm's runtime was longer than TOPP-RA due to the additional complexity of enforcing third-order constraints. However, it could still be executed within 10 ms, very reasonable for real-time applications. We were able to accelerate our computation times by warm-starting our algorithm with the non-jerk-limited TOPP-RA result and recomputing the only changed portion at each iteration.

:::: {#fig:motion_duration .figure latex-placement="t!"}
![](Lee2024Performance_figs/motion_duration.png){width="90%"}

::: caption
Motion duration for several motions computed with and without jerk limit.
:::
::::

Lastly, we measured the motion time generated by each algorithm for several different motions. Notably, imposing a jerk limit of $1000 \textnormal{ rad}/\textnormal{s}^3$ increased overall motion duration by just 3-5%. For the "Post-Place\" motion, we observed lower motion time with jerk limit, but this is just due to a known case of suboptimality in TOPP-RA, which guarantees optimality only if path points exclude zero-inertia point (see [@pham2018new] for details), which requires denser path segmentation. On the other hand, the proposed algorithm's SLP formulation allows it to converge to the optimal solution.

# DISCUSSION & CONCLUSIONS {#sec:conclusion}

In summary, we introduced a novel approach to solve the time-optimal trajectory planning problem while enforcing third-order constraints. In particular, we constrained the acceleration change between path points to produce smoother and more trackable trajectories. Using the proposed formulation, we removed the need for high-order dynamics variables which are computationally difficult to handle. For instance, the jerk formulation in [@pham2018new] requires $\mathbf{q}'''$, and the torque rate formulation in [@zhang2013practical] requires $\mathbf{M}'$ and $\mathbf{C}'$. These quantities can be challenging to compute from standard robot dynamics libraries. Though this paper tested only jerk limits, the provided formulation is versatile and can be extended to other useful third-order constraints such as torque rate.

Furthermore, our study has shown a significant reduction in peak power and torque efficiency from these jerk limits. This comes at the expense of some increased computation time, though it remains well within real-time limits. Additionally, this trade-off can be managed by computing the next step while the robot is executing the preceding path and using warm-starting to recompute solutions as needed. Additionally, although jerk limits result in slightly longer motion durations, this can be compensated by reduced time required for the robot to stabilize and come to a stop, due to reduced tracking fluctuation and overshoot.

During this study, we also observed that the results were quite sensitive to path parameter function discretization and splining. Splines can interpolate the discretized solution to generate robot commands at the desired high control frequency, but some spline types may induce jerk discontinuities between spline segments. This can be mitigated by constraining acceleration changes in transitions between spline segments, which can be formulated as additional third-order constraints. Furthermore, it is crucial to ensure sufficient discretization resolution to avoid high jerk between knot points where jerk is not directly constrained. In the future, we should explore more optimal and constrained parameterization methods for TOTP's path parameter function and refine the overall optimization process to accommodate corresponding changes effectively.

# APPENDIX {#appendix .unnumbered}

## Proof of convexity

**Proposition 1.** $f(x) = \dfrac{a}{\sqrt{x_1}+\sqrt{x_2}}+\dfrac{b}{\sqrt{x_2}+\sqrt{x_3}}$ *is convex in $x=(x_1,x_2,x_3)\in \mathbb{R}_+^3$.*

*Proof.* To show a twice-differentiable function $f$ is convex on a convex set, it is sufficient to show that its Hessian matrix of second partial derivatives is positive semi-definite in the interior of the set [@boyd2004convex]. The Hessian matrix is $$\begin{align*}
    H &= \frac{\partial^2 f}{\partial x^2} = 
    \begin{bmatrix} s_{11} & s_{12} & 0 \\
        s_{12} & s_{22} & s_{23} \\
        0 & s_{23} & s_{33}
    \end{bmatrix} ,
\end{align*}$$ where $$\begin{align*}
    s_{11} =& \frac{a}{2x_1(\sqrt{x_1}+\sqrt{x_2})^2}\left(\frac{1}{2\sqrt{x_1}}+\frac{1}{\sqrt{x_1}+\sqrt{x_2}}\right) \\    
    s_{22} =& \frac{a}{2x_2(\sqrt{x_1}+\sqrt{x_2})^2}\left(\frac{1}{\sqrt{x_1}+\sqrt{x_2}}+\frac{1}{2\sqrt{x_2}}\right) \\
    &+ \frac{b}{2x_2(\sqrt{x_2}+\sqrt{x_3})^2}\left(\frac{1}{2\sqrt{x_2}}+\frac{1}{\sqrt{x_2}+\sqrt{x_3}}\right) \\
    s_{33} =& \frac{b}{2x_3(\sqrt{x_2}+\sqrt{x_3})^2}\left(\frac{1}{\sqrt{x_2}+\sqrt{x_3}}+\frac{1}{2\sqrt{x_3}}\right) \\
    s_{12} =& \frac{a}{2\sqrt{x_1}\sqrt{x_2}(\sqrt{x_1}+\sqrt{x_2})^3} , \;
    s_{23} = \frac{b}{2\sqrt{x_2}\sqrt{x_3}(\sqrt{x_2}+\sqrt{x_3})^3}.
\end{align*}$$

As $H$ is a real symmetric matrix, $\lambda$s (eigenvalues of $H$) are real, which can be obtained from the characteristic equation: $$\begin{align*}
    \lambda^3 - \text{Tr}(H)\lambda^2 + \Bigg(\sum_{i \neq  j}s_{ii}s_{jj} - s_{12}^2 -s_{23}^2\Bigg)\lambda - |H| = 0.
\end{align*}$$ First, given the domain of $x_i>0$, it is clear that $\text{Tr}(H)>0$ and $\sum_{i \neq j}s_{ii}s_{jj} - s_{12}^2 -s_{23}^2 >0$. The determinant of $H$ is also positive in the given domain:

$$\begin{align*}
    |H| = \dfrac{3ab(a(4\sqrt{x_2}\sqrt{x_3}+x_2+3x_3)+b(4\sqrt{x_1}\sqrt{x_2}+3x_1+x_2))}{64\sqrt{x_1^3 x_2^3 x_3^3}(\sqrt{x_1}+\sqrt{x_2})^4(\sqrt{x_2}+\sqrt{x_3})^4  } > 0.
\end{align*}$$ When considering the relationship between the roots and coefficients of a cubic equation, it is known that if all coefficients above are positive, then all $\lambda$s satisfying the equation are also positive. Thus we have shown that $H$ is positive semi-definite, which implies that $f$ is convex.

# ACKNOWLEDGMENTS {#acknowledgments .unnumbered}

We thank Dexterity and the HCRL personnel for their support of this project. Jee-eun Lee was a robotics intern for Dexterity, Inc. during the summer of 2023, and Luis Sentis was a consultant for Dexterity, Inc. during the summer of 2022.

[^1]: This work was supported by Dexterity, Inc.

[^2]: \* Corresponding authors contributed equally.

[^3]: $^{1}$ J. Lee and L. Sentis are with The University of Texas at Austin, Austin, TX, USA, `{jelee, lsentis}@utexas.edu`

[^4]: $^{2}$ A. Bylard, and R. Sun are with Dexterity, Inc., Redwood City, CA, USA, `{andrew.bylard, robert}@dexterity.ai `
