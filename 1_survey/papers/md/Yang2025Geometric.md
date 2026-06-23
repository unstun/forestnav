---
citation_key: Yang2025Geometric
arxiv_id: 2504.19072
arxiv_url: https://arxiv.org/abs/2504.19072
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-23T18:13:36Z
origin: ai+web
reviewed: false
---

# Introduction

:::: {#fig:intro .figure latex-placement="!t"}
![](Yang2025Geometric_figs/fig002.png){width="\\linewidth"}

::: caption
Execution of the comprehensive motion plan computed using the proposed method on the roller racer robot. The green curve depicts the robot's position trajectory, and the composite figure illustrates the robot's configuration at different times. The roller racer has only one actuated degree of freedom: the steering angle between the front and rear wheels, with all wheels being passive and driven by anti-slip constraints and steering angle changes. The motion plan incorporates multiple gaits and transitions, enabling the robot to: a) start from rest and nominal shape into the gait cycle, b) accelerate to the optimal steady-state motion, c) smoothly switch to the steady-state gait that maintains maximum speed, d) execute a turn with minimal energy loss and return to steady-state motion, and e) end the gait cycle and return to the nominal shape. Throughout the execution, the motion plan maintains the desired heading angle and meets the average power consumption constraints.
:::
::::

Animals use a diverse set of gaits---such as horses' trotting and galloping, snakes' slithering and sidewinding, and body-caudal fin swimming in fish---to locomote effectively in various environments. By switching or transitioning between different gaits, animals demonstrate remarkable efficiency and adaptability, even in unstructured terrains [@alexander2006principles].

In both biology and robotics, significant research has been conducted on various forms of locomotion. Beyond systems whose dynamics are either fully determined by nonholonomic constraints or solely governed by conservation of momentum [@shammas2007geometric], there exist classes of locomoting systems that exhibit both kinematic and dynamic effects. These systems, referred to in this paper as kinodynamic systems, have garnered considerable attention due to their time-varying nonlinear dynamics and high degree of underactuation.

A representative example of kinodynamic systems is aquatic animals swimming at intermediate Reynolds numbers. The swimming of these aquatic animals is modeled as a system with drift (the ability to glide) due to the mixed inertial and fluid drag effects [@mason2003fluid; @kelly2012geometric]. This system is distinct from swimming at very high or low Reynolds numbers, where the dynamics are respectively dominated by conservation of momentum [@kanso2009swimming; @hatton2022geometry] or quasistatic drag equilibrium [@mason2003fluid; @xiong2007geometric; @ramasamy2019geometry], both of which produce driftless (or "kinematic") locomotion behavior. There is existing work that applies perturbation analysis to kinodynamic swimming locomotion to approximate the average motion over a gait cycle, enabling the design of sinusoidal gaits and image-based feedback control [@mcisaac2003motion]. Subsequent study models robotic fish by incorporating fluid-added mass, lift, and drag forces, deriving oscillatory control strategies through controllability analysis [@morgansen2007geometric]. Other works extend Lighthill's large-amplitude elongated body theory by introducing resistive forces [@boyer2008fast; @boyer2010poincare], resulting in a kinodynamic swimming model, which was later used in [@porez2014improved] for modeling swimming robots and performing gait search. Additionally, simplified swimming robot systems, such as Chaplygin's sleigh and its variants, have been studied for their control and motion planning [@kelly2012proportional; @fedonyuk2020path; @knizhnik2021thrust].

Interestingly, some wheeled robots are also kinodynamic systems, characterized by their dynamics governed by a combination of nonholonomic constraints and nonholonomic momentum evolution. The snakeboard [@ostrowski1995mechanics; @ostrowski1998reduced] and roller racer [@krishnaprasad2001oscillations; @halvani2022nonholonomic] are two representative examples. These systems have inspired extensive research on kinodynamic locomotion, including controllability analysis and gait design using sinusoidal waves [@murray1993nonholonomic; @ostrowski1994nonholonomic; @krishnaprasad2001oscillations], gait selection via optimal control theory [@ostrowski2000optimal], and motion planning formulated as a nonlinear inversion problem [@bullo2001kinematic; @bullo2003kinematic]. Other studies have explored gait design using area rules [@shammas2007unified], analytical solutions for trajectory tracking [@shammas2012motion; @dear2013snakeboard], and the integration of kinodynamic systems with bipedal riders [@anglingdarma2021motion]. Additionally, efforts have been made to enhance the fidelity of kinodynamic models based on the snakeboard and roller racer. For instance, some studies incorporate dissipative forces or viscous friction [@kelly1996geometry; @ostrowski1998reduced; @krishnaprasad2001oscillations], account for skidding effects [@dear2015snakeboard], or introduce improved friction modeling [@pengcheng2006motion; @salman2016physical]. Variants of these systems have also been studied, with research focusing on their modeling and control [@chitta2005robotrikke; @shammas2007unified].

Given that the positions of kinodynamic systems relative to the world are described by elements of Lie groups, numerical methods that exploit this group structure and preserve its symmetries offer significant advantages in terms of accuracy and efficiency [@marsden2001discrete; @hairer2006geometric; @celledoni2014introduction]. These methods have demonstrated superior performance across various domains, including simulation [@jonghoonpark2005geometric; @bruls2010use], control [@kobilarov2009lie; @wu2015safetycritical], and estimation [@barrau2017invariant; @barrau2018invariant]. Moreover, variational integrators and discretization techniques that preserve group structures can be combined with optimal control to enhance both accuracy and stability [@leok2007overview; @bloch2008optimal; @kobilarov2011discrete; @jimenez2013discrete; @saccon2013optimal]. This idea has been applied to a variety of robotic systems, including ground vehicles [@kobilarov2009lie], quadrotors [@kobilarov2014discrete], and legged robots [@teng2022errorstate; @csomay-shanklin2023nonlinear]. These advancements highlight the potential of Lie group integrators as a powerful tool for gait optimization in kinodynamic systems.

A common baseline for gait optimization is to use standard optimal control techniques---such as direct collocation [@chang2018optimal] or indirect methods [@wiezel2023geometric]---without exploiting Lie group theory. However, direct collocation suffers from discretization errors, in which quadrature-based integral approximations may violate dynamic constraints and accumulate errors, allowing the optimizer to "cheat" in highly nonlinear systems. While indirect methods offer better forward rollout accuracy, their backward pass is more complex and they struggle to incorporate additional state or input constraints. In contrast, gait optimization methods that leverage Lie group theory enable full-fidelity simulations and allow for the direct imposition of constraints on both control inputs and trajectories, with gradients obtained via the chain rule.

One line of related work uses Lie group theory for geometric gait optimization via constraint curvature and the generalized Stokes' theorem [@ramasamy2019geometry; @hatton2022geometry], but these methods mainly apply to principally kinematic systems. Geometric insights into the dynamic phase in kinodynamic systems have been developed to better understand their structure, though the approach relies on trial-and-error selection of gaits that couple the geometric and dynamic phases [@shammas2007unified]. Furthermore, other studies employing Lie group theory or integrators for motion planning in kinodynamic systems have predominantly focused on waypoint tracking or trajectory optimization [@leok2007overview; @bloch2008optimal; @kobilarov2011discrete; @jimenez2013discrete; @saccon2013optimal]. These methods can suffer from discretization errors over long trajectories and require recalculation for each new waypoint or trajectory. In contrast, this work focuses on gait optimization to avoid long trajectory discretization and to generate reusable motion primitives that enable comprehensive motion planning.

The main contribution of this paper is a gait optimization and motion planning framework for kinodynamic systems. This framework comprises:

- A general kinodynamic model incorporating kinematic and dynamics effects, based on Lagrangian reduction and differential geometry, applicable to a broad range of kinodynamic systems, including wheeled robots with nonholonomic constraints and swimming robots with anisotropic fluid-added inertia and hydrodynamic drag.

- A variational gait optimization method for kinodynamic systems, leveraging Lie group integrators and group symmetries.

- A methodology for constructing comprehensive motion plans that integrate multiple gaits and their transitions, enabling diverse motion capabilities for kinodynamic systems.

We evaluate our approach on three representative systems: the roller racer, the snakeboard, and a swimmer at an intermediate Reynolds number. All systems are evaluated in simulation, and the roller racer is additionally tested in hardware experiments. These evaluations demonstrate the ability of our framework to achieve a wide range of motions, including acceleration, steady-state maintenance, gait transitions, and turning, as shown in Fig. [1](#fig:intro){reference-type="ref" reference="fig:intro"} that illustrates the experiment conducted on the roller racer robot. The results underscore the effectiveness of the proposed approach and its potential for generalization to other biological and robotic locomotion systems.

# Kinodynamic System Modeling

:::: {#fig:systems .figure latex-placement="!t"}
![](Yang2025Geometric_figs/fig008.png){width="\\linewidth"}

::: caption
Illustration and key characteristics of the three kinodynamic systems considered in this paper. The roller racer has four degrees of freedom (DOF): three DOFs for position, describing its pose in the world, and one DOF for shape (the heading angle between the two carts). The system includes two nonholonomic constraints, corresponding to the non-lateral slip constraints of the wheelsets on the two carts, resulting in one DOF of nonholonomic momentum. Linear viscous friction occurs in the driving direction of each wheelset. Similarly, the snakeboard has five DOFs: three DOFs for position and two DOFs for shape. The shape is defined by the rotor angle and the cart angle, with the assumption that the two carts rotate together in opposite directions. The two nonholonomic constraints, corresponding to the non-lateral slip constraints of the wheelsets, also result in one DOF of nonholonomic momentum. Linear viscous friction also acts in the driving direction of each wheelset. Finally, the intermediate Reynolds number swimmer has five DOFs: three DOFs for position and two DOFs for shape, defined by the joint angles between its three links. Unlike the other systems, it has no direct nonholonomic constraints, so its momentum corresponds to the three DOFs for position. Instead, fluid dynamics manifest as anisotropic fluid-added mass and hydrodynamic drag acting on each link.
:::
::::

Kinodynamic systems are characterized by the interplay of kinematic and dynamic effects. Kinematic effects include the relationship between inertia, velocity, and momentum, as well as nonholonomic constraints. Based on the kinematics, one can derive the reconstruction equation that relates the system's body velocity to its shape velocity and nonholonomic momentum. Dynamic effects are governed by the Euler-Lagrange equations, incorporating dissipative or frictional forces and constrained forces. Through the application of Lagrangian reduction, these dynamics can be simplified into nonholonomic momentum evolution equations [@bloch1996nonholonomic].

## Reconstruction Equation

For a general locomoting system, the Lagrangian, $L$, is defined as

L(r, , g, ) &= [ke]{.smallcaps}(r, , ) - [pe]{.smallcaps}(r)\
[ke]{.smallcaps}(r, , ) &= \_i \^ \_i\_i \_i\
&=

::: bmatrix
\
:::

\^

::: bmatrix
M\_gg & M\_gr\
M\_rg & M\_rr
:::

::: bmatrix
\
:::

,

where $\textsc{ke}$ and $\textsc{pe}$ represent the kinetic and potential energy, respectively.[^3] The terms ${r}$ and $\dot{{r}}$ correspond to the system's shape and shape velocity, while $g$ and $%
	\mathchoice{\accentset{\scriptstyle\circ}{g}}
	{\accentset{\scriptstyle\circ}{g}}
	{\accentset{\scriptscriptstyle\circ}{g}}
	{\accentset{\scriptscriptstyle\circ}{g}}$ denote the system's position in $SE(2)$ and its body velocity in $\mathfrak{se}(2)$, respectively.[^4] $M$ represents the inertia matrix, with the subscripts representing the entries corresponding to the coordinates. $%
	\mathchoice{\accentset{\scriptstyle\circ}{g}}
	{\accentset{\scriptstyle\circ}{g}}
	{\accentset{\scriptscriptstyle\circ}{g}}
	{\accentset{\scriptscriptstyle\circ}{g}}
	_{i}$ and $\mu_{i}$ indicating the body velocity and inertia matrix of the $i$-th component of the system in its body frame.

Based on the Lagrangian, we can define the body momentum, $\underaccent{\scriptstyle\circ}{p}_{g}$, and the momentum in the generalized coordinates of the system shape, $p_{{r}}$, as[^5]

::: bmatrix
\_g& p\_r
:::

&=

::: bmatrix
&
:::

\
&=

::: bmatrix
\^ & \^
:::

::: bmatrix
M\_gg & M\_gr\
M\_rg & M\_rr
:::

.

If any nonholonomic constraints exist, they can be encoded by a linear operator $\omega$ which maps permitted combinations of body and shape velocity to zero $$\begin{equation}
\delimitershortfall=0pt\begin{aligned}
    \omega({r})\begin{bmatrix}
        %
	\mathchoice{\accentset{\scriptstyle\circ}{g}}
	{\accentset{\scriptstyle\circ}{g}}
	{\accentset{\scriptscriptstyle\circ}{g}}
	{\accentset{\scriptscriptstyle\circ}{g}}
	\\ \dot{{r}}
    \end{bmatrix}_{\text{permitted}} = 0.
\end{aligned}
\end{equation}$$ Then, the total nonholonomic momentum, $\bar{p}$, is defined as the projection of the system's momentum onto the allowable motion space, determined by the kernel of the constraint map $\bar{\Omega}$

\| &= ()\
\|p &=

::: bmatrix
\_g& p\_r
:::

; \|.

If no nonholonomic constraints exist in the system, we can simply skip this step and define $\omega= \emptyset$ and $\bar{\Omega} = \mathrm{Id}$.

By the definition of nonholonomic momentum and nonholonomic constraints, we can derive the system kinematics, which relates the system's body and shape velocities to the current nonholonomic momentum and nonholonomic constraints: $$\begin{equation}
\delimitershortfall=0pt\begin{aligned}
    \begin{bmatrix}
        %
	\mathchoice{\accentset{\scriptstyle\circ}{g}}
	{\accentset{\scriptstyle\circ}{g}}
	{\accentset{\scriptscriptstyle\circ}{g}}
	{\accentset{\scriptscriptstyle\circ}{g}}
	\\ \dot{{r}}
    \end{bmatrix} = \begin{bmatrix}
        \bar{\Omega}^{%
  {\mathpalette\@transposeintercal{}}%
}\begin{bmatrix}
            M_{gg} & M_{g{r}} \\ M_{{r}g} & M_{{r}{r}}
        \end{bmatrix} \\
        \omega
    \end{bmatrix}^{\hspace{.1ex}\text{-}\hspace{-.2ex}1}\begin{bmatrix}
        \bar{p}^{%
  {\mathpalette\@transposeintercal{}}%
} \\
        0
    \end{bmatrix}.
\end{aligned}
\end{equation}$$ In this paper, we assume direct control of the system shape, meaning that unit vectors corresponding to shape control lie in the kernel of the nonholonomic constraint map. Consequently, the total nonholonomic momentum can be decomposed into the coupled nonholonomic momentum, $p$,[^6] and the shape momentum, $p_{{r}}$,

\| &=

::: bmatrix
& 0\
&
:::

\
\|p &=

::: bmatrix
p& p\_r
:::

\
p&=

::: bmatrix
\_g& p\_r
:::

; .

By substituting the decomposition, the kinematics is rearranged into the reconstruction equation, which expresses the system's body velocity as a function of the current nonholonomic momentum and the shape velocity control:

&=

:::: bmatrix
\^

::: bmatrix
M\_gg\
M\_rg
:::

\
\_g
::::

\^1

:::: bmatrix
p\^  - \^

::: bmatrix
M\_gr\
M\_rr
:::

\
-\_r
::::

\
&= (r)+ (r)p\^ , []{#eq:reconstruction label="eq:reconstruction"}

where $\mathbf{A}$ is commonly referred to as the system's local connection, representing kinematic effects, while $\mathbf{\Gamma}$ denotes the connection associated with nonholonomic momentum, incorporating dynamic effects.

Note that systems with sufficiently many nonholonomic constraints to fully determine the body velocity from the controlled shape will have no nonholonomic momentum, i.e., $$\label{eq:primarily_kinematic}
\begin{align}
    %
	\mathchoice{\accentset{\scriptstyle\circ}{g}}
	{\accentset{\scriptstyle\circ}{g}}
	{\accentset{\scriptscriptstyle\circ}{g}}
	{\accentset{\scriptscriptstyle\circ}{g}}
	&= \mathbf{A}({r})\dot{{r}}\\
    p&\text{ is not defined}.
\end{align}$$ Additionally, systems whose dynamics are fully governed by momentum conservation, starting from rest, will take the form: $$\label{eq:purely_mechanical}
\begin{align}
    %
	\mathchoice{\accentset{\scriptstyle\circ}{g}}
	{\accentset{\scriptstyle\circ}{g}}
	{\accentset{\scriptscriptstyle\circ}{g}}
	{\accentset{\scriptscriptstyle\circ}{g}}
	&= \mathbf{A}({r})\dot{{r}}\\
    p&= \dot{p} = 0.
\end{align}$$ In these two cases, the system reduces to a principally kinematic system and a purely mechanical system, respectively [@shammas2007geometric]. Extensions to purely mechanical systems starting from nonzero momentum are discussed in [@yang2023geometric].

## Momentum Evolution

The momentum evolution can be derived from constrained Lagrangian mechanics: $$\begin{equation}
\begin{aligned}
    \begin{bmatrix}
        \underaccent{\scriptstyle\circ}{\dot{p}}_{g}& \dot{p}_{{r}}
    \end{bmatrix} = \lambda\omega+ \begin{bmatrix}
        -\operatorname{ad}^{\text{-}*}_{%
	\mathchoice{\accentset{\scriptstyle\circ}{g}}
	{\accentset{\scriptstyle\circ}{g}}
	{\accentset{\scriptscriptstyle\circ}{g}}
	{\accentset{\scriptscriptstyle\circ}{g}}
	}\underaccent{\scriptstyle\circ}{p}_{g}+ \underaccent{\scriptstyle\circ}{f}\\[0.75em]
        \frac{\partial L}{\partial {r}} + \tau
    \end{bmatrix}, \label{eq:lagrangemechanics}
\end{aligned}
\end{equation}$$ where $\lambda$ represents the constraint force due to the nonholonomic constraints, $\operatorname{ad}^{\text{-}*}_{%
	\mathchoice{\accentset{\scriptstyle\circ}{g}}
	{\accentset{\scriptstyle\circ}{g}}
	{\accentset{\scriptscriptstyle\circ}{g}}
	{\accentset{\scriptscriptstyle\circ}{g}}
	}\underaccent{\scriptstyle\circ}{p}_{g}$ denotes the rate of change of a constant momentum expressed in a moving body frame relative to a fixed observer in space, and $\underaccent{\scriptstyle\circ}{f}$ is the body force acting on the system's body frame. This body force includes viscous friction on the wheels of the roller racer and snakeboard, as well as nonlinear fluid drag forces on the swimmer at intermediate Reynolds numbers, as considered in this paper.[^7] The viscous friction is modeled as being linear in the wheel velocity, whereas the fluid drag force increases quadratically with the flow velocity: $$\begin{equation}
\begin{aligned}
    \underaccent{\scriptstyle\circ}{f}=
    \begin{cases}
        -\sum_{i}\operatorname{Ad}^{*}_{g^{\hspace{.1ex}\text{-}\hspace{-.2ex}1}_{i}}%
	\mathchoice{\accentset{\scriptstyle\circ}{g}}
	{\accentset{\scriptstyle\circ}{g}}
	{\accentset{\scriptscriptstyle\circ}{g}}
	{\accentset{\scriptscriptstyle\circ}{g}}
	^{%
  {\mathpalette\@transposeintercal{}}%
}_{i}d_{\text{friction}, i} & \text{for viscous friction} \\
        -\sum_{i}\operatorname{Ad}^{*}_{g^{\hspace{.1ex}\text{-}\hspace{-.2ex}1}_{i}}(\lvert%
	\mathchoice{\accentset{\scriptstyle\circ}{g}}
	{\accentset{\scriptstyle\circ}{g}}
	{\accentset{\scriptscriptstyle\circ}{g}}
	{\accentset{\scriptscriptstyle\circ}{g}}
	_{i}\rvert\odot%
	\mathchoice{\accentset{\scriptstyle\circ}{g}}
	{\accentset{\scriptstyle\circ}{g}}
	{\accentset{\scriptscriptstyle\circ}{g}}
	{\accentset{\scriptscriptstyle\circ}{g}}
	_{i})^{%
  {\mathpalette\@transposeintercal{}}%
}d_{\text{drag}, i}  & \text{for fluid drag},
    \end{cases}
\end{aligned}
\end{equation}$$ where $\odot$ denotes the element-wise product, $\lvert\bullet\rvert$ represents the element-wise absolute value, $g_{i}$ is the position of the $i$-th component relative to the system's body frame, $d_{\text{friction}, i}$ and $d_{\text{drag}, i}$ are the viscous friction and fluid drag coefficients of the $i$-th component, expressed in its body frame, and $\operatorname{Ad}^{*}_{\bullet}$ denotes the dual adjoint matrix corresponding to the transformation.[^8]

Similarly, $\tau$ represents the torque acting on the joints, which includes contributions from viscous friction or quadratic fluid drag forces, as well as actuator-applied torques for shape control:

$$\begin{equation}
\begin{aligned}
    \tau_{j} =
    \begin{cases}
        \bar{\tau}_{j} - \sum_{i}\operatorname{Ad}^{*\theta}_{g_{ij}}%
	\mathchoice{\accentset{\scriptstyle\circ}{g}}
	{\accentset{\scriptstyle\circ}{g}}
	{\accentset{\scriptscriptstyle\circ}{g}}
	{\accentset{\scriptscriptstyle\circ}{g}}
	^{%
  {\mathpalette\@transposeintercal{}}%
}_{i}d_{\text{friction}, i} & \text{for viscous friction} \\
        \bar{\tau}_{j} - \sum_{i}\operatorname{Ad}^{*\theta}_{g_{ij}}(\lvert%
	\mathchoice{\accentset{\scriptstyle\circ}{g}}
	{\accentset{\scriptstyle\circ}{g}}
	{\accentset{\scriptscriptstyle\circ}{g}}
	{\accentset{\scriptscriptstyle\circ}{g}}
	_{i}\rvert\odot%
	\mathchoice{\accentset{\scriptstyle\circ}{g}}
	{\accentset{\scriptstyle\circ}{g}}
	{\accentset{\scriptscriptstyle\circ}{g}}
	{\accentset{\scriptscriptstyle\circ}{g}}
	_{i})^{%
  {\mathpalette\@transposeintercal{}}%
}d_{\text{drag}, i}  & \text{for fluid drag},
    \end{cases}
\end{aligned}
\end{equation}$$ where $g_{ij}$ is the transformation matrix from the $i$-th link to the $j$-th joint, $\operatorname{Ad}^{*\theta}_{\bullet}$ denotes the row corresponding to rotation in the dual adjoint matrix, and $\bar{\tau}_{j}$ represents the actuator torque.

The time derivative of the nonholonomic momentum can be computed by differentiating its definition: $$\begin{equation}
\begin{aligned}
    \dot{p}&= \left\langle\begin{bmatrix}
        \underaccent{\scriptstyle\circ}{\dot{p}}_{g}& \dot{p}_{{r}}
    \end{bmatrix}; \Omega\right\rangle + \left\langle\begin{bmatrix}
        \underaccent{\scriptstyle\circ}{p}_{g}& p_{{r}}
    \end{bmatrix}; \dot{\Omega}\right\rangle. \label{eq:momevo}
\end{aligned}
\end{equation}$$ Because $\Omega$ lies in the kernel of the nonholonomic constraint map, the inner product eliminates the constraint forces in [\[eq:lagrangemechanics\]](#eq:lagrangemechanics){reference-type="eqref" reference="eq:lagrangemechanics"}.

Finally, substituting the time derivative of the nonholonomic momentum along with the controlled position, velocity, and acceleration of the shape into [\[eq:lagrangemechanics\]](#eq:lagrangemechanics){reference-type="eqref" reference="eq:lagrangemechanics"} allows for the calculation of the joint actuator torque $\tau$.

## Examples

The key features of the three examples of kinodynamic systems considered in this paper are summarized in Fig. [2](#fig:systems){reference-type="ref" reference="fig:systems"}. Both the roller racer and the snakeboard are kinodynamic systems with one degree of freedom (DOF) of nonholonomic momentum, resulting from nonholonomic constraints and dynamic effects caused by internal relative motion between multiple bodies. For these systems, wheel friction is modeled as linear viscous friction [@ostrowski1998reduced; @krishnaprasad2001oscillations].

The primary difference between the roller racer and the snakeboard lies in their actuation. The roller racer has a single actuated DOF---the steering angle---where the inertia rearrangement and constraint directions are coupled to the steering control. In contrast, the snakeboard features two actuated DOFs: one for the rotor and the other for the trucks' steering (with the trucks assumed to steer together in opposite directions). This configuration decouples the inertia rearrangement from the constraint directions.

Unlike the roller racer and the snakeboard, the swimmer at intermediate Reynolds numbers does not involve direct nonholonomic constraints. Instead, its dynamics are modeled by Morison's equation, incorporating anisotropic fluid-added mass and hydrodynamic drag forces acting on each body [@brennen2006internet; @boyer2010poincare; @porez2014improved]. Consequently, the swimmer possesses three DOFs of nonholonomic momentum, corresponding to the position dimensions. In this case, the kinematic and dynamic effects are strongly coupled, with the fluid-added mass and drag forces being shape-dependent and directly acting on the joints.

# Variational Gait Optimization Based on Lie Group Integrator

In this section, we introduce the variational gait optimization method for kinodynamic systems. The Lie group integrator provides an efficient and accurate method to compute the gradients and Jacobians of the gait-induced displacement with respect to the gait parameters, enabling effective variational gait optimization. We begin by defining the displacement, nonholonomic momentum, and power consumption corresponding to a gait cycle. These terms are fundamental concepts in the gait optimization problem, as most objective and constraint functions rely on them. Once the gradients of these terms are computed, the chain rule can be applied to derive the gradients of the optimization objective and constraint functions, thereby achieving variational gait optimization.

Without loss of generality, consider a gait $\phi$ in the shape space, parameterized by the gait parameters $\chi$. The displacement induced by this gait is given by $$\begin{equation}
\begin{aligned}
    g_{\phi}= \Prodi_{0}^{T}\left(\mathrm{Id}+%
	\mathchoice{\accentset{\scriptstyle\circ}{g}}
	{\accentset{\scriptstyle\circ}{g}}
	{\accentset{\scriptscriptstyle\circ}{g}}
	{\accentset{\scriptscriptstyle\circ}{g}}
	(t) dt\right) \label{eq:fwdeuler},
\end{aligned}
\end{equation}$$ where $T$ represents the gait period, and $\prodi$ is the product integral. This formulation essentially is a Lie group integrator.

Additionally, as shown in [\[eq:momevo\]](#eq:momevo){reference-type="eqref" reference="eq:momevo"}, the nonholonomic momentum over the gait period is given by the solution to the ordinary differential equation for momentum evolution: $$\begin{equation}
\begin{aligned}
    p(t) = p(0) + \int_{0}^{t}\dot{p}\bigl(({r}(\tau), \dot{{r}}(\tau), p(\tau)\bigr)d\tau, \label{eq:momevoint}
\end{aligned}
\end{equation}$$ where $p(0)$ is the initial nonholonomic momentum at the start of the gait execution.

Finally, the power consumption of executing the gait is defined as the integral of the squared actuator torque $\|\tau(t)\|^{2}_{2}$ over the gait period: $$\begin{equation}
\begin{aligned}
    E= \int^{T}_{0}\|\tau(t)\|^{2}_{2} dt. \label{eq:energy}
\end{aligned}
\end{equation}$$

## Gradient of Gait-Induced Displacement

:::: {#fig:gradient .figure latex-placement="!t"}
![](Yang2025Geometric_figs/fig003.png){width="90%"}

::: caption
Demonstration of gradient computation for variational gait optimization based on Lie group integrator. For a principally kinematic system, $%
	\mathchoice{\accentset{\scriptstyle\circ}{g}}
	{\accentset{\scriptstyle\circ}{g}}
	{\accentset{\scriptscriptstyle\circ}{g}}
	{\accentset{\scriptscriptstyle\circ}{g}}
	= \begin{bmatrix} 1 & 0 & u \end{bmatrix}^{\intercal}$, the position trajectory $g\vert_{u=u_0}$ is represented by the solid line. The variation in the trajectory due to a control change $\Delta u$ is computed by summing the gradient contributions from the control change at each segment along the trajectory. The contribution of each segment is depicted as the dashed trajectory. Due to group symmetries, a control change at any segment does not affect the shape of the remaining trajectory, similar to rotating the joints of a robotic arm.
:::
::::

By differentiating the Lie group integral with respect to the gait parameters $\chi$, we obtain

&= \_0\^T g(t)( + )g\^1(t)g_dt\
&= \_0\^T \_g(t)( + )g_dt, []{#eq:disgrad label="eq:disgrad"}

The second term in the sum inside the parentheses arises because the period $T$ is treated as a function of the gait parameters $\chi$, requiring consideration of the integration bounds during differentiation.

Using the reconstruction equation in [\[eq:reconstruction\]](#eq:reconstruction){reference-type="eqref" reference="eq:reconstruction"}, the derivative of the system's body velocity can be expressed as $$\begin{equation}
\begin{aligned}
    \frac{\partial %
	\mathchoice{\accentset{\scriptstyle\circ}{g}}
	{\accentset{\scriptstyle\circ}{g}}
	{\accentset{\scriptscriptstyle\circ}{g}}
	{\accentset{\scriptscriptstyle\circ}{g}}
	(t)}{\partial \chi} = \frac{\partial %
	\mathchoice{\accentset{\scriptstyle\circ}{g}}
	{\accentset{\scriptstyle\circ}{g}}
	{\accentset{\scriptscriptstyle\circ}{g}}
	{\accentset{\scriptscriptstyle\circ}{g}}
	_{t}}{\partial {r}_{t}}\frac{\partial {r}_{t}}{\partial \chi} + \frac{\partial %
	\mathchoice{\accentset{\scriptstyle\circ}{g}}
	{\accentset{\scriptstyle\circ}{g}}
	{\accentset{\scriptscriptstyle\circ}{g}}
	{\accentset{\scriptscriptstyle\circ}{g}}
	_{t}}{\partial \dot{{r}}_{t}}\frac{\partial \dot{{r}}_{t}}{\partial \chi} + \frac{\partial %
	\mathchoice{\accentset{\scriptstyle\circ}{g}}
	{\accentset{\scriptstyle\circ}{g}}
	{\accentset{\scriptscriptstyle\circ}{g}}
	{\accentset{\scriptscriptstyle\circ}{g}}
	_{t}}{\partial p_{t}}\frac{\partial p_{t}}{\partial \chi},
\end{aligned}
\end{equation}$$ where time-varying variables $[\bullet](t)$ are denoted as $[\bullet]_{t}$ for clarity in the equations. Because the gait in the shape space is parameterized by $\chi$, the derivatives of the shape position and velocity can be directly obtained from the parameterization function. In contrast, the derivative of the momentum is more complex, because it involves the momentum evolution, which will be addressed in the next section.

## Gradient of Nonholonomic Momentum

Based on the nonholonomic momentum solution in [\[eq:momevoint\]](#eq:momevoint){reference-type="eqref" reference="eq:momevoint"}, the chain rule can be applied to compute the derivative of the nonholonomic momentum: $$\begin{equation}
\begin{aligned}\label{eq:linear_system}
    \frac{\partial p(t)}{\partial \chi} &= \int^{t}_{0}\left(\frac{\partial \dot{p}_{\tau}}{\partial {r}_{\tau}}\frac{\partial {r}_{\tau}}{\partial \chi} + \frac{\partial \dot{p}_{\tau}}{\partial \dot{{r}}_{\tau}}\frac{\partial \dot{{r}}_{\tau}}{\partial \chi} + \frac{\partial \dot{p}_{\tau}}{\partial p_{\tau}}\frac{\partial p_{\tau}}{\partial \chi}\right)d\tau\\
    &\quad+\frac{p(t) - p(0)}{T}\frac{\partial T}{\partial \chi},
\end{aligned}
\end{equation}$$ where, as before, time-varying variables $[\bullet](\tau)$ are denoted as $[\bullet]_{\tau}$ for clarity in the equations. The last term arises because the period $T$ depends on the gait parameters $\chi$, requiring consideration of the integration bounds during differentiation.

Similarly, the gradient of the energy consumption in [\[eq:energy\]](#eq:energy){reference-type="eqref" reference="eq:energy"} for executing the gait can be derived in the same manner, as it follows a similar sum-integral structure.

A key difference between the gradient of momentum and that of displacement or energy consumption is the temporal autocorrelation of momentum. Specifically, the momentum at time $t$ depends on the time series of momentum preceding $t$, because $\dot{p}$ is a function of $p$ itself. This temporal dependence transforms the gradient computation into solving a linear system after discretization. Consequently, this distinction affects the computational accuracy of the gradients post-discretization, which we will discuss in the next section.

## Invariance and Gradient Error Analysis

For principally kinematic and purely mechanical systems described by [\[eq:primarily_kinematic\]](#eq:primarily_kinematic){reference-type="eqref" reference="eq:primarily_kinematic"} and [\[eq:purely_mechanical\]](#eq:purely_mechanical){reference-type="eqref" reference="eq:purely_mechanical"}, which do not involve nonholonomic momentum, the gradients of gait-induced displacement are invariant. Specifically, as illustrated in Fig. [3](#fig:gradient){reference-type="ref" reference="fig:gradient"}, the body velocities are trajectory-independent, meaning any variation in the body velocity at a point on the trajectory applies only a left group action to the subsequent trajectory. Integrating this variation along the trajectory, as in [\[eq:disgrad\]](#eq:disgrad){reference-type="eqref" reference="eq:disgrad"}, yields the corresponding variation in the final displacement. Consequently, once the trajectory is simulated, the displacement gradient along it can be directly computed, with accuracy linearly proportional to the discretization density. These characteristics allow for an efficient and accurate gradient-based variational gait optimization across a wide range of principally kinematic and purely mechanical systems.

In contrast, for the kinodynamic systems considered in this paper, the presence of nonholonomic momentum breaks this invariance. The momentum evolution is a self-dependent ordinary differential equation, causing momentum gradient errors to scale quadratically with discretization density. Because the displacement gradient depends on the momentum gradient, these errors propagate into the displacement gradient as well. In this case, optimizing gaits or trajectories over long horizons becomes impractical, because discretization errors or model mismatches accumulate. Instead, we focus on optimizing periodic gaits and short-term transitions between them. These motion primitives are subsequently combined to construct complete motion plans, as detailed in the motion planning section below.

# Geometric Motion Planning

Motion planning for kinodynamic systems is inherently more complex than for principally kinematic or purely mechanical systems due to their time-dependent dynamics. In kinematic systems, where dynamics are quasi-static, motion planning can often be achieved using simple gaits to locomote directly in the desired direction. However, in kinodynamic systems, the presence of nonholonomic momentum requires accounting for the evolution of momentum, adding additional complexity to the planning process. Efficient locomotion involves first accumulating momentum and then directing it to drive towards the desired direction. This principle appears in many real-world examples, such as roller racer or snakeboard riders swinging to accelerate before steering towards their target, or fish stroking to generate thrust and then gliding towards the desired direction using their streamlined bodies. In this paper, we leverage the gradient computations based on the Lie group integrator discussed earlier to identify gaits and transitions, enabling the construction of comprehensive motion plans for kinodynamic systems.

We begin by considering the following optimization problem, which maximizes the linear displacement over a time horizon $T_{\infty}$, significantly longer than a single gait period $T$ (i.e., $T_{\infty} \gg T$), subject to joint position limits and energy consumption constraints:

&g̍\^\[x, y\](T\_)̍\_2\
s.t. &(t) , t\
&̍(t)̍\^2\_2 \< \_c\^2, t,

where $g^{[x, y]}(T_{\infty})$ denotes the linear displacement over the horizon $T_{\infty}$, $\mathcal{R}$ represents the range of motion of the robot joints, and $\tau_{c}^2$ defines the power consumption limit. Due to energy dissipation from velocity-dependent friction or fluid drag, as well as constraints on energy consumption and the range of motion of the joints, the robot will eventually converge to a steady state with periodic motion and state. This allows us to decompose the original problem into four sub-problems, solving for multiple gaits and their transitions to construct a comprehensive motion plan, as illustrated in Fig. [4](#fig:roller_racer_gait){reference-type="ref" reference="fig:roller_racer_gait"}:

1.  Steady-state gait optimization: Finding the optimal gait $\phi_{\mathrm{S}}$ and periodic nonholonomic momentum state $p_{\mathrm{S}}$ that maximize the steady-state speed.

2.  Acceleration gait optimization: Identifying the acceleration gait $\phi_{\mathrm{A}}$ that optimally accelerates the robot to the steady state.

3.  Transition gait optimization: Determining the transition gaits $\phi_{\mathrm{TS}}$ for:

    1.  Starting from rest at the nominal shape and transitioning to the acceleration gait,

    2.  Transitioning from the acceleration gait to the steady-state gait,

    3.  Returning from the steady-state gait to the nominal shape.

4.  Turning gait optimization: Finding the turning gait $\phi_{\mathrm{T}}$ to redirect the steady-state robot to a new direction.

## Steady-State Gait Optimization

We first address steady-state gait optimization, which involves maintaining periodic motion and state while maximizing velocity and satisfying specific constraints. This gait optimization can be formulated as:

\_\_, p\_ &g̍\_\_\^\[x, y\]̍\_2\
s.t. &p\_(0) = p\_(T\_) []{#eq:momconstr label="eq:momconstr"}\
&g\_\_\^ = 0 []{#eq:orientconstr label="eq:orientconstr"}\
&\_(t) , t[]{#eq:jointconstr label="eq:jointconstr"}\
& \< \_c\^2[]{#eq:energyconstr label="eq:energyconstr"}\
&\_, p\_ . []{#eq:feasibility label="eq:feasibility"}

In this formulation, the objective function seeks to maximize the average translational velocity of the gait. Constraint [\[eq:momconstr\]](#eq:momconstr){reference-type="eqref" reference="eq:momconstr"} ensures that the nonholonomic momentum $p_{\mathrm{S}}$ is periodic throughout the gait cycle. Constraint [\[eq:orientconstr\]](#eq:orientconstr){reference-type="eqref" reference="eq:orientconstr"} requires the robot to maintain its orientation before and after the gait cycle. Constraint [\[eq:jointconstr\]](#eq:jointconstr){reference-type="eqref" reference="eq:jointconstr"} enforces that joint positions remain within their prescribed limits. Constraint [\[eq:energyconstr\]](#eq:energyconstr){reference-type="eqref" reference="eq:energyconstr"} requires that the average energy consumption stays within the allowable range. Finally, [\[eq:feasibility\]](#eq:feasibility){reference-type="eqref" reference="eq:feasibility"} serves as an auxiliary feasibility condition, ensuring that the steady state can be reached from rest via an acceleration gait while adhering to the power consumption constraint. This avoids potential energy barriers that could render the steady state inaccessible. Details on this auxiliary feasibility problem, as well as the design of the acceleration gait, will be discussed in the next section.

## Acceleration Gait Optimization

:::: {#fig:roller_racer_gait .figure latex-placement="!t"}
![](Yang2025Geometric_figs/fig004.png){width="\\linewidth"}

::: caption
Illustration of the optimal gaits and transitions for the roller racer (top) and their demonstration on the robot (middle: acceleration-transition-steady-state gait; bottom: steady-state-left-turn-steady-state and steady-state-right-turn-steady-state gaits). In the demonstration, the dashed line represents the robot's position trajectory, with its color indicating the corresponding gait being executed at each point.
:::
::::

Due to the time-varying dynamics of kinodynamic systems, naively executing the steady-state gait for acceleration is impractical, because it may violate power constraints, drift in direction, or require excessive convergence time. To address this, we explore effective acceleration gaits to reach the steady state in this section.

We begin by introducing the feasibility problem formulated in [\[eq:feasibility\]](#eq:feasibility){reference-type="eqref" reference="eq:feasibility"}. The objective is to find an acceleration gait that accelerates the system from rest to a steady state, achieving the average kinetic energy level similar to that of the optimal steady-state gait without violating joint or power constraints:

&\
s.t. &p\_(0) = p\_(T\_)\
&g\_\_\^ = 0\
&\_(t) , t\
& \< \_c\^2, \< \_c\^2\
&\_ \> \_,

where $E_{\mathrm{F}, 0}$ represents the power consumption during the first gait cycle starting from rest (i.e., zero nonholonomic momentum),[^9] and $\overline{\textsc{ke}}_{\mathrm{S}}$ and $\overline{\textsc{ke}}_{\mathrm{F}}$ denote the average kinetic energy of the steady-state gait and that of the feasible acceleration gait in its steady state, respectively. This feasibility problem ensures that an acceleration gait exists to bring the system from rest to the kinetic energy level of the steady-state gait while respecting all constraints, thereby enabling a further transition to the steady-state gait. In the steady-state gait optimization, this feasibility problem is solved as an auxiliary problem alongside to ensure the feasibility of the steady-state gait.

For the actual acceleration gait optimization, simply ensuring the existence of feasible gaits is insufficient, because we also want to maximize efficiency and maintain the heading angle. To this end, we propose an approach for optimizing acceleration gaits. A key characteristic of the acceleration behavior in the kinodynamic systems studied in this paper is that, during the transition from a stationary state to a steady state, the average translational velocity of each gait cycle, $\bar{\dot{g}}^{[x, y]}$, converges to the steady-state velocity, $\bar{\dot{g}}^{[x, y]}_{\mathrm{S}}$, in a manner analogous to a linear mass-damper system: $$\begin{equation}
\begin{aligned}
    \bar{\dot{g}}^{[x, y]}(t) \approx (1 - e^{-kt})\bar{\dot{g}}^{[x, y]}_{\mathrm{S}},  
\end{aligned}
\end{equation}$$ where $k$ represents the convergence rate or equivalent damping coefficient. This behavior emerges naturally from the dynamic model: executing repeated acceleration gaits continuously adds energy to the system, while energy dissipation due to viscous friction is proportional to velocity.

For systems like the roller racer and snakeboard, which assume linear viscous friction, this analogy is particularly appropriate, as their wheels consistently generate friction through continuous rolling. For intermediate Reynolds number swimmers, despite the fluid-added mass being acceleration-dependent and the fluid drag quadratically velocity-dependent, they are anisotropic and shape-dependent. Consequently, an efficient acceleration gait minimizes the equivalent total fluid drag during acceleration. Thus, the linear mass-damper model remains a valid approximation for these systems, as illustrated in the following figure.

Using the linear mass-damper approximation model for the acceleration period, we can reformulate the feasibility problem as an acceleration gait optimization problem:

\_\_, p\_ &\|̍\^\[x, y\]\_T̍\_ - g\_\
s.t. &p\_(0) = p\_(T\_)\
&g\_\_, 0\^ = 0 ,g\_\_\^ = 0\
& \< \_c\^2, \< \_c\^2\
&\_(t) , t\
&\_ \> \_,

where the subscript $[\bullet]_{\mathrm{R}}$ denotes the total transient period, which we define as the rise time required to reach 90% of the steady-state velocity, calculated based on the linear mass-damper model. The objective function seeks to determine the optimal acceleration gait that minimizes the deviation from the steady-state velocity during the transition. The term $g_{\phi_{\mathrm{A}}, 0}^{\theta}$ represents the orientation difference before and after the first gait cycle starting from rest. Constraints on this term, combined with constraints on the orientation difference at the steady state, ensure a consistent heading angle throughout the acceleration period.[^10]

## Transition Gait Optimization

With the optimal gaits derived in the previous section, a complete motion plan can be constructed by combining these gaits. The remaining challenge is to enable smooth transitions between these gaits without loss of generality. In this section, we propose a method for gait transitions using polynomials.

To ensure a smooth transition while respecting power consumption constraints, we employ a fifth-order polynomial to connect between the two gaits. This polynomial guarantees continuity up to the shape acceleration at both ends. Because the initial and final shape positions, velocities, and accelerations are fully determined by the gaits at either end of the transition, all polynomial coefficients can be computed directly. The transition gait optimization problem for determining the transition gait $\phi_{\mathrm{TS}}(t_{0}, t_{1}, T_{\mathrm{TS}})$ for transitioning from gait $(\phi_{0}, p_{0})$ to gait $(\phi_{1}, p_{1})$ is formulated as:

\_t\_0, t\_1, T\_ &̍(g\_\_\^ + g\_\_0\^(t\_0) - (g\_\_0\^y, g\_\_0\^x)).\
&- .(g\_\_1\^(t\_1) - (g\_\_1\^y, g\_\_1\^x))̍\_2\
s.t. &\_\^(n)(0) = \_0\^(n)(t_0), n = 0, 1, 2 []{#eq:polyconstr1 label="eq:polyconstr1"}\
&\_\^(n)(T\_) = \_1\^(n)(t_1), n = 0, 1, 2 []{#eq:polyconstr2 label="eq:polyconstr2"}\
&p\_0(t_0) + p\_(T\_) = p\_1(t_1) []{#eq:polymomconstr label="eq:polymomconstr"}\
&\_(t) , t[]{#eq:polyjointconstr label="eq:polyjointconstr"}\
& \< \_c\^2, []{#eq:polyenergyconstr label="eq:polyenergyconstr"}

where $t_{0}$ and $t_{1}$ are the phases of the two gaits connected by the polynomial, $T_{\mathrm{TS}}$ represents the transition duration, and $p_{\mathrm{TS}}$ is the change in momentum relative to the initial momentum at the beginning of the transition. The objective function minimizes orientation drift during the transition, ensuring consistency in the translational motion direction between the two gaits while accounting for orientation oscillations within each gait. Constraints [\[eq:polyconstr1\]](#eq:polyconstr1){reference-type="eqref" reference="eq:polyconstr1"} and [\[eq:polyconstr2\]](#eq:polyconstr2){reference-type="eqref" reference="eq:polyconstr2"} define the 5th-order polynomial coefficients based on the shape position, velocity, and acceleration of the gaits before and after the transition. Constraint [\[eq:polymomconstr\]](#eq:polymomconstr){reference-type="eqref" reference="eq:polymomconstr"} enforces momentum continuity between the two gaits. Constraints [\[eq:polyjointconstr\]](#eq:polyjointconstr){reference-type="eqref" reference="eq:polyjointconstr"} and [\[eq:polyenergyconstr\]](#eq:polyenergyconstr){reference-type="eqref" reference="eq:polyenergyconstr"} address joint limits and power consumption. During execution, the transition is triggered once the acceleration gait reaches the energy level of the steady-state gait.

The same approach can be adapted for transitions at the start or end of motion. To initiate acceleration from rest at the nominal shape, we fix $\phi_{0}(t_{0})$ and $p_{0}$ to the initial state. Conversely, to transition from a steady-state gait to gliding, $\phi_{1}(t_{1})$ is fixed to the gliding shape, and the momentum constraint is relaxed.

:::: {#fig:snakeboard_gait .figure latex-placement="!t"}
![](Yang2025Geometric_figs/fig006.png){width="\\linewidth"}

::: caption
Illustration of the optimal gaits and transitions for the snakeboard (top) and their demonstration on the robot (middle: acceleration-transition-steady-state gait; bottom: steady-state-left-turn-steady-state and steady-state-right-turn-steady-state gaits). The thickness of the gait cycles indicates the pacing of the gait, with thick lines representing slower shape changes and thin lines representing faster changes. Black arcs with arrows denote the direction of the gait. In the demonstration, the dashed line represents the robot's position trajectory, with its color indicating the corresponding gait being executed at each point.
:::
::::

## Turning Gait Optimization

In the previous section, we discussed gait optimization and motion planning for maximizing translational velocity in a single direction, but did not address motion in other directions. As demonstrated in [@ostrowski1995mechanics; @krishnaprasad2001oscillations; @morgansen2007geometric], these kinodynamic systems exhibit small-time local controllability in all three directions, enabling the design of gaits and motion plans for lateral motion or rotation using the same approach.

However, in practice, roller racer and snakeboard riders rarely move sideways or rotate on the spot, and similarly, fish seldom swim sideways. Instead, they typically accelerate to accumulate momentum and then use this momentum to turn toward the desired direction. Therefore, in this section, we extend the transition gait optimization to turning motions, thereby extending the motion planning capabilities.

Turning gait optimization is introduced as an extension of transition gait optimization, where the turning gait, $\phi_{\mathrm{T}}(t_{0}, t_{1}, T_{\mathrm{T}})$, is preceded and followed by the same steady-state gait and satisfies the requirement that the orientation change equals the desired turning angle:

\_t\_0, t\_1, T\_ &̍ \_\_(t_1)- \_\_(T\_)̍\_M\_gg(t\_1)\
s.t. &\_\^(n)(0) = \_\^(n)(t_0), n = 0, 1, 2\
&\_\^(n)(T\_) = \_\^(n)(t_1), n = 0, 1, 2\
&g\_\_\^ + g\_\_\^(t\_0) - g\_\_\^(t\_1) =\
&\_(t) , t\
& \< \_c\^2,

where $\Delta\theta$ represents the desired turning angle, and the third constraint ensures that the directional change across the turning gait equals the turning angle. $\left\|\bullet\right\|_{M_{gg}(t_{1})}$ denotes the inner product weighted by the inertia matrix, evaluated at the steady-state gait shape at $t_1$. Because turning by gliding inevitably leads to energy loss, momentum continuity before and after the turn cannot be enforced. Instead, the objective function minimizes the difference in body velocity between the steady state and the post-turn state, weighted by the inertia matrix, effectively measuring the kinetic energy loss.

It is also possible to formulate a steering gait by enforcing zero energy loss and nonzero rotational displacement. A straightforward approach involves modifying the steady-state gait using the same transition formula---adding a segment to introduce rotational displacement without energy loss. However, this approach does not always yield feasible solutions, and the achievable steering angle is inherently limited.

## Implementation Details

We solve the optimization using `fmincon` in MATLAB with the interior-point method, providing the cost and gradient from our method and approximating the Hessian via the Broyden-Fletcher-Goldfarb-Shanno (BFGS) algorithm. Our approach is also compatible with other nonlinear programming solvers.

As with any nonlinear optimization, the solution depends on the initial guess and may converge to a local minimum. For steady-state gait optimization, we choose a gait in which the shape variables oscillate sinusoidally out of phase and with an offset (tracing a circle in the shape space centered on the mean joint values) and its corresponding steady-state momentum as the initial guess to maintain the heading angle and respect joint limits. Then we seed the acceleration gait with the optimal steady-state gait. For transition, turning, start, and end gaits---parameterized by polynomials with fewer decision variables---we perform a grid search for initial guesses of the gait percentiles and initialize the period with the average of the adjacent gaits.

The computational complexity scales with the system dimension and discretization density. For high-dimensional systems, the main cost per iteration is solving the linear system in [\[eq:linear_system\]](#eq:linear_system){reference-type="eqref" reference="eq:linear_system"}, which scales as $O(n^2)$. In our implementation, discretizing the gait cycle into 100 segments allows each gait's optimization to complete in less than one minute. Because gait optimization is performed offline and online execution only requires retrieving solutions from a pre-computed library, our method scales well to higher-dimensional systems.

# Simulation Results

To evaluate the proposed approach, we apply it to all the three representative example systems to calculate a comprehensive motion plan involving start from the rest, accelerating to the steady-state energy level, transition between the acceleration and the steady-state gait, turning left and right, and smoothly end the run by resting at a nominal shape. For gait optimization, the steady-state and acceleration gaits are parameterized as fourth-order Fourier series.

## Roller Racer

The roller racer is modeled based on the physical robot. The robot has a total weight of approximately 2.5 kg, with the rear cart weighing 1.7 kg and the front cart 0.8 kg. The distances from the joints to the center of mass are about 0.13 meters for the front cart and 0.05 meters for the rear cart. The wheels are spaced 0.07 meters apart laterally. The viscous friction coefficient was calculated based on the experimental data. The actuator force limit is set according to the hardware datasheet. The actuator range limits are set to avoid the center of mass extending beyond the supporting polygon.

Fig. [4](#fig:roller_racer_gait){reference-type="ref" reference="fig:roller_racer_gait"} illustrates the optimal gaits and transitions for the roller racer and their demonstration. Because the system has only one actuated degree of freedom, most of the gaits resemble sinusoidal waves, except for the start and acceleration gaits, which feature different pacing on the rising and falling edges. These gaits are specifically designed to accelerate as quickly as possible while maintaining the heading angle under increasing momentum. The turning gait exhibits the largest wave magnitude to steer the front cart effectively, utilizing the accumulated momentum to achieve turns with minimal energy loss. Notably, the two turning gaits show symmetry in shape space. For all other gaits, the wave amplitude gradually decreases as momentum increases. This reflects a design principle where higher drive amplitudes are required for acceleration, while more compliant control is necessary to sustain high speeds in the steady state. The start, transition, and end gaits, ensure smooth transitions between the nominal zero shape and the cyclic gaits. These transitions are achieved using a half-period wave with a shape similar to the cyclic gaits being connected and an appropriate magnitude, facilitating heading angle maintenance and momentum matching.

The first row of Fig. [7](#fig:simulation){reference-type="ref" reference="fig:simulation"} illustrates the position trajectory and momentum history of the simulation results of a roller racer executing the comprehensive motion plan starting from rest. Because the motion plan was also designed for experimental implementation, the acceleration phase was reduced by one cycle from the duration required to reach 90% of the steady-state velocity to accommodate environmental size constraints. Despite this adjustment, the resulting trajectory demonstrates promising performance, including starting the robot from the nominal zero shape, accelerating to the desired energy level, smoothly transitioning to the steady-state gait, performing left and right turns for a quarter corner, and finally gliding at the nominal zero shape. The momentum trajectory highlights key differences between the acceleration and steady-state cycles and illustrates the minimal energy loss during the turning phases.

## Snakeboard

The snakeboard physics model is based on [@ostrowski1996mechanics], with a total mass of 6 kg and inertias of 0.06, 0.167, and $\text{0.00167 kg}\cdot \text{m}^\text{2}$ for the body, rotor, and wheelsets, respectively. The board has a total length of 0.6 m, and the viscous friction coefficient is assumed to be 0.15. The range of rotor rotation is constrained to one cycle, and the range of wheel rotation mimics that of ankle joints.

Fig. [5](#fig:snakeboard_gait){reference-type="ref" reference="fig:snakeboard_gait"} illustrates the optimal gaits and transitions for the snakeboard in the shape space, along with their demonstration on the robot. Due to the limited range of both shapes, the gaits resemble circular cycles with varying radii and localized deformations. Unlike the roller racer, the acceleration and steady-state gaits for the snakeboard are distinct. This difference arises because the relative arrangement of the multi-rigid bodies and the direction of the constraints are decoupled into two degrees of freedom: the rotor and the wheel truck joints. This decoupling has two key implications. First, the efficiency of acceleration can be enhanced by alternating the rotation of the rotor and wheels to pump energy with the help of constraint forces. Second, in the steady state, energy savings can be achieved by applying compliant control to the rotor, allowing it to oscillate passively in tandem with the wheel oscillations. Similar to the roller racer, the magnitude of oscillation decreases as momentum increases. The two turning gaits, like those of the roller racer, are symmetrical to each other, and involve an additional cycle and a half added to the steady-state gaits to direct momentum for turning with minimal energy loss. In the demonstration, the turning motion occurs in two stages. The first stage serves as a preparatory motion, where the wheel and rotor are turned to one side. In the second stage, the actual large-angle turn is executed by turning both the wheel and rotor to the opposite side. Other gait transitions, including the start, transition, and end gaits, converge to the corresponding cyclic gaits using half cycles of appropriate amplitudes to maintain heading angles and match momentum.

The second row of Fig. [7](#fig:simulation){reference-type="ref" reference="fig:simulation"} presents the position trajectory and momentum history of the simulation results of a snakeboard executing the comprehensive motion plan starting from rest. During the acceleration phase, significantly larger oscillations are observed in both position and momentum compared to the steady-state phase, corresponding to the distinction between energy pumping and compliant control. The decoupled inertial manipulation and constraint direction control enable the snakeboard to achieve higher efficiency than the roller racer, but it also requires a longer acceleration time. Overall, these results demonstrate that the proposed method performs effectively in planning complex motions for the snakeboard.

## Intermediate Reynolds Number Swimmer

:::: {#fig:swimmer_gait .figure latex-placement="!t"}
![](Yang2025Geometric_figs/fig007.png){width="\\linewidth"}

::: caption
Illustration of the optimal gaits and transitions for the intermediate Rynolds number swimmer (top) and their demonstration on the robot (middle: acceleration-transition-steady-state gait; bottom: steady-state-left-turn-steady-state and steady-state-right-turn-steady-state gaits). The thickness of the gait cycles indicates the pacing of the gait, with thick lines representing slower shape changes and thin lines representing faster changes. Black arcs with arrows denote the direction of the gait. In the demonstration, the dashed line represents the robot's position trajectory, with its color indicating the corresponding gait being executed at each point. For clearer visualization, the swimmer's dimensions are scaled down from actual size.
:::
::::

:::: {#fig:simulation .figure latex-placement="!t"}
![](Yang2025Geometric_figs/fig005.png){width="\\linewidth"}

::: caption
Overall position trajectories and momentum-time curves from the execution of the integrated motion plan for three representative systems. The motion plan begins from rest, accelerates to the steady-state energy level, transitions to a steady state, performs a right turn, continues forward in the steady state, executes a left turn, continues forward in the steady state again, and finally returns to the nominal shape. For the turning gait, the swimmer turns 15 degrees per cycle, requiring six cycles to complete a quarter-angle turn.
:::
::::

The intermediate Reynolds number swimmer is modeled as a three-link swimmer neutrally buoyant in the fluid with a total length of 0.6 meters. Each link is modeled as a cylindrical shape with a slenderness ratio of 1:5. Together with the actuator limits, this configuration results in swimming at a Reynolds number approximately between $2 \times 10^4$ and $3 \times 10^5$. Hydrodynamics are modeled using Morison's equation, with quadratic drag coefficients of 1.2 in the lateral direction and 0.008 in the axial direction [@orcina2025orcaflex]. Fluid-added mass is calculated based on the cylinder's cross-sectional geometry.

Fig. [6](#fig:swimmer_gait){reference-type="ref" reference="fig:swimmer_gait"} illustrates the optimal gaits and transitions for the swimmer in shape space and their demonstration on the robot. Similar to the snakeboard, the swimmer uses a larger-radius cycle for efficient acceleration and transitions to a streamlined steady-state gait to minimize drag. Notably, both the acceleration and steady-state gaits exhibit a larger amplitude for the tail joint (${r}_1$) compared to the head joint (${r}_2$). This difference likely arises from the need to maintain the heading angle by stabilizing the head while propelling forward with larger tail swings. Such behavior aligns with physical observations and analyses of fish propulsion, where wave amplitude increases toward the tail [@wu1961swimming]. As shown in the demonstration, turning is achieved by bending the body toward the desired direction, allowing drag forces to redirect momentum. Unlike the roller racer and snakeboard, which utilize constraint forces for turning, the swimmer actively drives its joints to generate turning forces through drag. This reliance on active actuation makes large-angle turning in a single cycle infeasible due to joint torque limits. Consequently, the desired turning angle is set to 15 degrees, requiring six cycles to complete a quarter turn.

The last row of Fig. [7](#fig:simulation){reference-type="ref" reference="fig:simulation"} shows the position trajectory and momentum history of the swimmer during the execution of the comprehensive motion plan starting from rest. Due to the six-cycle quarter-turn maneuver, the turning trajectory is less sharp compared to the roller racer and snakeboard. Additionally, the momentum and energy losses during turning are significantly higher than in the other systems. This difference stems from the swimmer's reliance on large lateral drag forces for turning, which inherently dissipate substantial energy. Furthermore, as previously mentioned, although drag is quadratic with respect to the local body velocity, an efficient gait that alternates shapes correctly can minimize drag during swimming. This optimization results in an acceleration process that resembles the behavior of a linear mass-damper system, as shown in the momentum trajectory. Overall, the simulation results highlight the effectiveness of the proposed method in generating motion plans for the swimmer.

# Experiment Results

We conducted experiments on the roller racer robot. The hardware consists of two pairs of passive skateboard wheels, each with a diameter of 0.8 m, attached to the front and rear carts. A Dynamixel XL430-W250-T actuator was used to control the joint between the two carts, with a bearing isolating the linear force. The battery, actuator, and bearing are all mounted on the rear cart, giving it greater inertia compared to the front cart. To evaluate pure feed‑forward performance, the motion plan was loaded onto a Raspberry Pi and executed in an open-loop manner, with the actuator solely tracking the desired shape. The viscous friction coefficient of the wheels was determined experimentally by pushing the robot and observing its deceleration until it came to a stop due to friction. The robot's position trajectory was tracked using Aruco markers attached to the robot and the environment.

Fig. [1](#fig:intro){reference-type="ref" reference="fig:intro"} illustrates the robot's movement and behavior when executing the motion plan from rest. The composite plots show that the robot successfully reproduces the planned behaviors, including starting from rest, accelerating, transitioning between gaits, maintaining steady-state motion, turning, and returning to the zero shape to glide. These results align closely with the simulation outcomes. Given that the gaits were executed in an open-loop manner, this performance demonstrates the validity and robustness of our approach.

Fig. [8](#fig:experiment){reference-type="ref" reference="fig:experiment"} presents the position trajectories of three experimental trials for quantitative analysis. The results show that the robot effectively reproduces the overall motion and gait behaviors, despite exhibiting approximately 10 degrees of orientation drift at the beginning of the acceleration and 2 meters of additional displacement compared to the simulation. The primary sources of error are likely due to model mismatches, including friction not being purely viscous but potentially involving Coulomb friction, imperfect shape tracking, inaccuracies in the robot's inertia computation, and possible wheel sliding at high speeds. Because the experiments were conducted in an open-loop setup, these errors accumulated and scaled up over time. Despite these errors, the experimental results demonstrate that the feed-forward motion plan and gaits computed using the proposed approach can be successfully executed on the robot hardware, achieving the desired movements with promising performance---even in open-loop control. Furthermore, the consistency across the three experimental trials highlights the robustness of our approach.

# Limitations

While our work demonstrates effectiveness and robustness in both simulations and experiments across three example systems, several limitations remain and provide opportunities for future work. First, the framework currently generates only feed‑forward gaits and motion plans; it does not incorporate closed-loop control. In practice, mitigating real-world errors requires feedback. For example, the feedback controller based on averaging theory in [@vela2002second; @vela2003averaging] can complement our feedforward gait, as both are derived from Lie group theory. In addition, implementing feedback would involve online state estimation, for instance via the invariant Kalman filter [@barrau2018invariant], using IMUs and wheel encoders.

Second, as evidenced by the experimental results, the current model based on viscous friction lacks the fidelity to fully capture real robot behavior. Addressing this limitation requires adopting higher-fidelity models for both wheeled robots and swimmers. Potential approaches include improved friction models [@salman2016physical], boundary element methods for coupled fluid-added mass computations [@kanso2005locomotion], or system identification techniques [@justus2024geometry].

In addition, the limited turning angle achievable within a single cycle for the swimmer highlights a constraint in the current gait design. Potential solutions include developing turning gaits independent of the steady-state gait to improve efficiency. Alternatively, addressing the fundamental limitation---that swimmers cannot leverage constraint forces for turning, unlike the roller racer or snakeboard---could involve designing mechanisms such as fins or rudders to utilize constraint forces for energy-efficient turning [@morgansen2007geometric]. Additionally, transitioning from articulated designs to continuum swimmers with soft actuators could enable more efficient bending and propulsion [@yang2025geometric].

Moreover, the current approach assumes a single gait is used throughout the acceleration process. While this simplifies implementation, it sacrifices some efficiency. A potential direction for future work is to dynamically adjust the acceleration gait during the process based on momentum changes. This could be achieved by tracking the solution of the time-varying acceleration gait optimization problem using an online algorithm, such as those described in [@simonetto2017predictioncorrection; @choi2022optimal].

Finally, the Lie group integrator discretization used in this paper employs a method analogous to the forward Euler method on the tangent space, which may be less accurate compared to higher-order methods, such as the Cayley mapping proposed in [@marsden2001discrete; @kobilarov2011discrete]. Future work will focus on extending the discretization of Lie group integrators to higher-order methods to enhance accuracy and performance.

:::: {#fig:experiment .figure latex-placement="!t"}
![](Yang2025Geometric_figs/fig001.png){width="\\linewidth"}

::: caption
Comparison of experimental and simulated position trajectories for the roller racer robot. Three open-loop experiments were conducted to execute the comprehensive motion plan derived using the proposed method. The experimental trajectories were obtained using Aruco markers on the roller racer and within the environment. A low-pass filter was applied to the experimental results to reduce noise.
:::
::::

# Conclusion

In this paper, we propose a gait optimization and motion planning framework for kinodynamic systems. The framework begins with a general kinodynamic model that captures both kinematic and dynamic effects using Lagrangian reduction and differential geometry. Building on this model, we introduce a variational gait optimization approach based on Lie group integrators and group symmetries. Finally, we construct motion plans by combining diverse gaits and transitions to achieve various motions, including acceleration, maximizing steady-state speed, turning, and transitions. The proposed framework was evaluated on wheeled robots with nonholonomic constraints and swimming robots with anisotropic fluid-added inertia and hydrodynamic drag, demonstrating consistent performance and robustness across both simulations and hardware experiments. These results underscore the validity and effectiveness of our approach.

[^1]: This work was supported in part by NSF Grants No. 1653220, 1826446, and 1935324, and by ONR Grant No. N00014-23-1-2171.

[^2]: Y. Yang and R. L. Hatton are with the Collaborative Robotics and Intelligent Systems (CoRIS) Institute at Oregon State University, Corvallis, OR USA. `{yangyanh, Ross.Hatton}@oregonstate.edu`

[^3]: For simplicity, this paper focuses on changes in kinetic energy during locomotion, assuming constant potential energy. This assumption is based on gravity being counteracted by the ground reaction force in wheeled robots or by neutral buoyancy in swimmers. However, the proposed approach is generalizable to systems with variable potential energy, such as those influenced by gravity or joint stiffness.

[^4]: The "open circle" notation we use here is similar to the "dot" notation, but denotes derivatives taken in the body frame. Formally, these are derivatives with respect to right-group actions (locally with respect to the current configuration) rather than coordinate values, producing left-invariant representations of velocity and force. The "open circle" superscripts represent tangent vectors, such as velocity, and the subscripts are for covectors such as force or momentum. By convention, velocity is represented as the time derivative of the configuration, and momentum and force are given their own symbols.

    For example, the full reading of the notation of the body velocity $%
    	\mathchoice{\accentset{\scriptstyle\circ}{g}}
    	{\accentset{\scriptstyle\circ}{g}}
    	{\accentset{\scriptscriptstyle\circ}{g}}
    	{\accentset{\scriptscriptstyle\circ}{g}}$ is "the velocity constructed by taking the derivative of position with respect to right group actions", and the full reading of the notation of body force $\underaccent{\scriptstyle\circ}{f}$ is "the force constructed by taking the derivative of dissipated energy with respect to right (body) velocities".

[^5]: Momentum is a covector, so we represent it as a row vector here.

[^6]: For simplicity, we refer to it as nonholonomic momentum in the rest of this paper.

[^7]: For force-controlled systems---such as those using jet thrusters attached to the body---this model can be generalized to include the controlled force in $\underaccent{\scriptstyle\circ}{f}$.

[^8]: In colloquial terms, $\operatorname{Ad}_{\bullet}$ and $\operatorname{Ad}^{*}_{\bullet}$ refer to the adjoint and dual adjoint operators that combine the cross-product operation---which converts linear and angular velocities or forces/momenta between different frames---with the rotation operation that expresses velocities or forces/momenta in body-aligned coordinates.

[^9]: Technically, the average power consumption is not a convex function of the nonholonomic momentum, which implies that enforcing constraints only at zero momentum and steady-state momentum does not guarantee compliance with the power limit at intermediate points. However, for the kinodynamic systems studied in this paper, the power consumption peak typically occurs either at the start or in the steady state. In practice, one can validate the power consumption limits after optimizing the gait. Addressing the power consumption constraints more rigorously during acceleration remains an open challenge, which we leave for future work.

[^10]: Unlike the non-convex power consumption discussed earlier, the orientation displacement before and after each gait cycle is a linear function of the momentum change. This relationship arises because the body velocity is computed by applying the linear mapping $\mathbf{\Gamma}$ to the momentum, as shown in [\[eq:reconstruction\]](#eq:reconstruction){reference-type="eqref" reference="eq:reconstruction"}. Because $\mathbf{\Gamma}$ is shape-dependent and the shape remains consistent across each cycle for shape-controlled gaits, the orientation change produced during each gait cycle is linearly related to the nonholonomic momentum. Consequently, by enforcing zero orientation displacement at the beginning and at the steady state, the orientation remains unchanged throughout the acceleration period.
