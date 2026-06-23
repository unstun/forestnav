---
citation_key: Mower2023OpTaS
arxiv_id: 2301.13512
arxiv_url: https://arxiv.org/abs/2301.13512
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-23T19:33:26Z
origin: ai+web
reviewed: false
---

# Introduction {#sec:intro}

High-dimensional motion planners and controllers are integrated in many of the approaches for solving complex manipulation tasks. Consider, for example, a robot operating in an unstructured and dynamic environment that, e.g. places an object onto a shelf, or drilling during pedicle screw fixation in surgery (see Fig. [3](#fig:examples){reference-type="ref" reference="fig:examples"}). In such cases, a planner and controller must account for objectives/constraints like bi-manual coordination, contact constraints between robot-object and object-environment, and be robust to disturbances. Efficient motion planning and fast controllers are an effective way of enabling robots to perform these tasks subject to motion constraints, system dynamics, and changing task objectives.

Sampling-based planners [@lavalle2006planning] are effective, however, they typically require considerable post-processing (e.g. trajectory smoothing). Optimal planners (i.e. that are provably asymptotically optimal, e.g. RRT$^*$) are promising but inefficient (in terms of computation duration) for solving high-dimensional problems [@karaman2011sampling].

Gradient-based trajectory optimization (TO) is a key approach in optimal control, and has also been utilized for motion planning. This approach underpins many recent works in robotics for planning and control, e.g. [@Ratliff2009; @Schulman2014; @Posa2014; @Kuindersma2016; @stouraitis2020online; @mower2021skill; @moura2022non; @Toussaint2022]. Given an initialization, optimization finds a locally optimal trajectory, comprised of a stream of state and control commands subject to motion constraints and system dynamics (i.e. equations of motion).

Several reliable open-source and commercial optimization solvers exist for solving TO problems, e.g. IPOPT [@Wachter2006], KNITRO [@byrd2006k], and SNOPT [@Gill2005SNOPT]. However, despite the success of the optimization approaches proposed in the literature and motion planning frameworks such as MoveIt [@coleman2014reducing], there is a lack of libraries enabling fast development/prototyping of optimization-based approaches for multi-robot setups that easily interfaces with these efficient solvers.

:::: {#fig:examples .figure}
![](Mower2023OpTaS_figs/shelf2.jpg){#fig:shelf height="2.7cm"}

 

![](Mower2023OpTaS_figs/faros.jpg){#fig:suturing height="2.7cm"}

::: caption
Examples of contact-rich manipulation showing (a) a robot placing an item on a shelf, (b) a human interacting with a robot performing a drilling task during pedicle screw fixation. Image credit: University Hospital Balgrist, Daniel Hager Photography & Film GmbH.
:::
::::

To fill this gap, this paper proposes OpTaS, a user-friendly task-specification library for rapid development and deployment of nonlinear optimization-based planning and control approaches such as Model Predictive Control (MPC). The library leverages the symbolic framework of CasADi [@Andersson2019], enabling function derivatives to arbitrary order via automatic differentiation. This is important since some solvers (e.g. SNOPT) utilize the Jacobian and Hessian.

:::: {#fig:sys-overview .figure latex-placement="t"}
![](Mower2023OpTaS_figs/system_overview.png){width="1.8\\columnwidth"}

::: caption
System overview for the proposed OpTaS library. **Red** highlights the main features of the proposed library. **Green** shows configuration parameter input. **Grey** shows third-party frameworks/libraries. Finally, the image in the top-right corner shows integration with the ROS-PyBullet Interface [@Mower2022].
:::
::::

## Related work {#sec:related-work}

In this section, we review popular optimization solvers and their interfaces. Next, we describe works similar (in formulation) to our proposed library. Finally, we summarize the key differences and highlight our contributions. Table [1](#tab:compare){reference-type="ref" reference="tab:compare"} summarizes alternatives and how they compare to OpTaS.

There are several capable open-source and commercial optimization solvers. First considering quadratic programming, the OSQP method provides a general purpose solver based on the alternating direction method of multipliers [@osqp]. Alternatively, CVXOPT implements a custom interior-point solver [@andersen2020cvxopt]. IPOPT implements an interior-point solver for constrained nonlinear optimization. SNOPT provides an interface to an SQP algorithm [@Gill2005SNOPT]. KNITRO also solves general mixed-integer programs [@byrd2006k]. Please note that SNOPT and KNITRO are proprietary.

These solvers are often implemented in low-level programming languages such as C, C++, or FORTRAN. However, there are also many interfaces to these methods via higher level languages, such as Python, to make implementation and adoption easier. The SciPy library contains the `optimize` module [@2020SciPy-NMeth] to interface with low-level routines, e.g. conjugate gradient and BFGS algorithm [@nocedal1999numerical], the Simplex method [@nelder1965simplex], COBYLA [@Powell1994], and SLSQP [@Kraft1988]. A requirement when using optimization-based methods is the need for function gradients. Several popular software packages implement automatic differentiation [@jax2018github; @Andersson2019; @NEURIPS2019_9015]. We leverage the CasADi framework [@Andersson2019] for deriving gradients. Our choice for CasADI is based on the fact that it comes readily integrated with common solvers for optimal control. To the best of our knowledge, JAX and PyTorch are not currently integrated with constrained nonlinear optimization solvers.

Similar to our proposed library are the following packages. The MoveIt package provides the user with specific IK/planning formulations and provides interfaces to solvers for the particular problem [@coleman2014reducing]. The eTaSL library [@Aertbelien2014etasl] allows the user to specify custom tasks specifications, but only supports problems formulated as quadratic programs. The CASCLIK library uses CasADi and provides support for constraint-based inverse kinematic controllers [@Arbo2019], to the best of our knowledge they allow optimization in the joint space. We provide joint space, task space optimization and also the ability to simultaneously optimize in the joint/task space. Furthermore, our framework supports optimization of several robots in a single formulation. The EXOTica library allows the user to specify a problem formulation from an XML file [@exotica]. The package, however, requires the user to supply analytic gradients for additional sub-task models.

::: {#tab:compare}
              Languages    End-pose   Traj.   MPC   Solver   AutoDiff   ROS   Re-form
  ----------- ------------ ---------- ------- ----- -------- ---------- ----- ---------
  **OpTaS**   Python                                QP/NLP                    
  EXOTica     Python/C++                            QP/NLP                    
  MoveIt      Python/C++                            QP                        
  TracIK      Python/C++                            QP                        
  RBDL        Python/C++                            QP                        
  eTaSL       C++                                   QP                        
  OpenRAVE    Python                                QP                        

  : Comparison between OpTaS and common alternatives in literature.
:::

## Contributions

This paper makes the following contributions:

- A task-specification library, in Python, for rapid development/deployment of TO approaches for multi-robot setups.

- Modeling of the robot kinematics (forward kinematics, geometric Jacobian, etc.), to arbitrary derivative order, given a URDF specification.

- An interface that allows a user to easily reformulate an optimal control problem, and define parameterized constraints for online modification of the optimization problem.

- Analysis comparing the performance of the library (i.e. solver convergence, solution quality) versus existing software packages. Further demonstrations highlight the ease in which nonlinear constrained optimization problems can be set up and deployed in realistic settings.

# Problem Formulation {#sec:problem-formulation}

We can write an optimal control formulation of a TO or planning problems as $$\begin{equation}
  \label{eq:trajopt}
  \underset{x, u}{\min}~\text{cost}(x, u; T)\quad\text{subject to}\quad
  \begin{cases}
    \dot{x} = f(x, u)\\x\in\mathbb{X}\\u\in\mathbb{U}
  \end{cases}
\end{equation}$$ where $t$ denotes time, and $x = x(t)\in\mathbb{R}^{n_x}$ and $u = u(t)\in\mathbb{R}^{n_u}$ denote the states and controls, with $T$ being the time-horizon for the planned trajectory. The scalar function $\text{cost}: \mathbb{R}^{n_x}\times \mathbb{R}^{n_u}\rightarrow\mathbb{R}$ represents the cost function (typically a weighted sum of terms each modeling a certain sub-task), the dot notation denotes a derivative with respect to time (i.e. $\dot{x}\equiv\tfrac{dx}{dt}$), $f$ represents the system dynamics (equations of motion), and $\mathbb{X}\subseteq\mathbb{R}^{n_x}$ and $\mathbb{U}\subseteq\mathbb{R}^{n_u}$ are feasible regions for the states and controls respectively (modeled by a set of equality and inequality constraints). Direct optimal control, optimizes for the controls $u$ for a discrete set of time instances, using numerical methods (e.g. Euler or Runge-Kutta), to integrate the system dynamics over the time horizon $T$ [@kelly2017introduction]. Given an initialization $x^{\textrm{init}}, u^{\textrm{init}}$, a locally optimal trajectory $x^*, u^*$ is found by solving [\[eq:trajopt\]](#eq:trajopt){reference-type="eqref" reference="eq:trajopt"}.

As discussed in Sec. [1](#sec:intro){reference-type="ref" reference="sec:intro"}, many works propose optimization-based approaches for planning and control. These can all be formulated under the same framework, i.e. a TO problem as in [\[eq:trajopt\]](#eq:trajopt){reference-type="eqref" reference="eq:trajopt"}. The goal of our work is to deliver a library that allows a user to quickly develop and prototype constrained nonlinear TO for multi-robot problems, and deploy them for motion generation. The library includes two types of problems, IK and task-sace TO, and indeed both simultaneously. Common steps, such as transcription that transforms the problem's task-level description into a form accepted by numerical optimization solver routines, should be automated and thus not burden the user. Furthermore, many works in practice require the ability to adapt constraints dynamically to handle changes in the environment (e.g. MPC). This motivates a constraint parameterization feature.

# Proposed Framework {#sec:proposed-framework}

In this section, we describe the main features of the proposed library shown in Fig. [4](#fig:sys-overview){reference-type="ref" reference="fig:sys-overview"}. The library is completely implemented in the Python programming language. We chose Python because it is simple for beginners but also versatile with many well-developed libraries, and it easily facilitates fast prototyping.

## Robot model {#sec:robot-model}

The robot model (`RobotModel`) provides the kinematic modeling and specifies the time derivative orders required for the optimization problem. The only requirement is a URDF to instantiate the object[^5]. A key feature is that we can include several robots in the TO, which is useful for dual arm and whole-body optimization. Additional base frames and end-effector links can be added programatically (for example, when several robots are included the optimization their base frames should be registered within a global coordinate frame).

The `RobotModel` class allows access to data such as: the number of degrees of freedom, the names of the actuated joints, the upper and lower actuated joint limits, and the kinematics model. Furthermore, we provide methods to compute the forward kinematics and geometric Jacobian in any given reference frame. Several methods modeling the kinematics are supplied, given a specification from the user for the base frame and end-effector frame. These methods include: the $4\times 4$ homogeneous transformation matrix, translation position, rotational representations (e.g. Euler angles, quaternions), the geometric and analytical Jacobian. Each of the methods above depend on a joint state (supplied as either a Python list, NumPy array, or CasADi symbolic array).

## Task model

Several works optimize robot motion in the task space and then compute the IK as a secondary step, e.g. [@mower2021skill; @moura2022non]. The task model (`TaskModel`) provides a representation for any arbitrary trajectory. For example, the three dimensional position trajectory of an end-effector. In the same way as the robot model, the time derivatives can be specified in the interface an arbitrary order.

## Optimization builder

This section introduces and describes the optimization builder class (`OptimizationBuilder`). The purpose of this class is to aid the user to easily setup a TO problem, and then automatically build an optimization problem model (Sec. [3.4](#sec:optimization-problem-model){reference-type="ref" reference="sec:optimization-problem-model"}) that interfaces with a solver interface (Sec. [3.5](#sec:solver-interface){reference-type="ref" reference="sec:solver-interface"}). The development cycle consists in specifying the task (i.e. decision variables, parameters, cost function, and constraints) using intuitive syntax and symbolic variables. Then, the builder creates an optimization problem class, which interfaces with several solvers.

## Optimization problem model {#sec:optimization-problem-model}

The standard TO is stated in [\[eq:trajopt\]](#eq:trajopt){reference-type="eqref" reference="eq:trajopt"}. This task/problem is specified by the optimization builder class in intuitive syntax for the user. Transcribing the problem to a form that can be solved by off-the-shelf solvers is non-trivial. The output of the optimization builder method `build` is an optimization problem model that allows us to interface with several solvers.

The most general optimization problem that is modeled by OpTaS is given by $$\label{eq:optimization-problem}
  \begin{align}
    X^* & = \underset{X}{\text{arg}\min}~f(X; P)\\
        & \text{subject to}\nonumber\\
        & k(X; P) = M(P)X + c(P) \geq 0\label{eq:lin-ineq-con}\\
        & a(X; P) = A(P)X + b(P) = 0\label{eq:lin-eq-con}\\
        & g(X; P) \geq 0\label{eq:nlin-ineq-con}\\
        & h(X; P) = 0\label{eq:nlin-eq-con}
  \end{align}$$ where $X = [vec(x)^T, vec(u)^T]^T\in\mathbb{R}^{n_X}$ is the decision variable array such that $x, u$ are as defined in [\[eq:trajopt\]](#eq:trajopt){reference-type="eqref" reference="eq:trajopt"} and $vec(\cdot)$ is a function that returns its input as a 1-dimensional vector, $P\in\mathbb{R}^{n_P}$ is the vectorized parameters, $f: \mathbb{R}^{n_X}\rightarrow\mathbb{R}$ denotes the objective function, $k: \mathbb{R}^{n_X}\rightarrow\mathbb{R}^{n_k}$ denotes the linear inequality constraints, $a: \mathbb{R}^{n_X}\rightarrow\mathbb{R}^{n_a}$ denotes the linear equality constraints, $g: \mathbb{R}^{n_X}\rightarrow\mathbb{R}^{n_g}$ denotes the nonlinear inequality constraints, and $h: \mathbb{R}^{n_X}\rightarrow\mathbb{R}^{n_h}$ denotes the nonlinear equality constraints. The decision variables $X$ are all the joint states and other variables specified by the user stacked into a single vector. Similarly for the parameters, cost terms, and constraints. Vectorization is made possible by the `SXContainer` data structure implemented in the `sx_container` module. This data structure enables automatic transcription of the TO problem specified in [\[eq:trajopt\]](#eq:trajopt){reference-type="eqref" reference="eq:trajopt"} into the form [\[eq:optimization-problem\]](#eq:optimization-problem){reference-type="eqref" reference="eq:optimization-problem"}.

Of course, not all task specifications will require definitions for each of the functions in [\[eq:optimization-problem\]](#eq:optimization-problem){reference-type="eqref" reference="eq:optimization-problem"}. Depending on the structure of the objective function and constraints, the required time budget, and accuracy, some solvers will be more appropriate for solving [\[eq:optimization-problem\]](#eq:optimization-problem){reference-type="eqref" reference="eq:optimization-problem"}. For example, a quadratic programming solver that only handles linear constraints (e.g. OSQP [@osqp]) is unsuitable for solving a problem with nonlinear objective function and nonlinear constraints. The build process automatically identifies the optimization problem type, exposing only the relevant solvers. Several problem types are available to the user: unconstrained quadratic cost, linearly constrained with quadratic cost, nonlinear constrained with quadratic cost, unconstrained with nonlinear cost, linearly constrained with nonlinear cost, nonlinear cost and constraints.

### Initialization

Upon initialization of the optimization builder class we can specify **(i)** the number of time steps in the trajectory, **(ii)** several robot and task models (given a unique name for each), **(iii)** the joint states (positions and required time-derivatives) that integrate the decision variable array, **(iv)** task space labels, dimensions, and derivatives to also integrate the decision variable array, **(v)** a Boolean describing the alignment of the derivatives (Fig. [5](#fig:time-deriv){reference-type="ref" reference="fig:time-deriv"}), and **(vi)** a Boolean indicating whether to optimize time steps.

:::: {#fig:time-deriv .figure latex-placement="t"}
![](Mower2023OpTaS_figs/time-deriv.png){width="0.8\\columnwidth"}

::: caption
Joint state alignment with time. User supplies `derivs_align` that specifies how joint state time derivatives should be aligned.
:::
::::

The alignment of time-derivatives can be specified in two ways. Each derivative is aligned with its corresponding state (alignement), or otherwise. This is specified by the `derivs_align` flag in the optimization builder interface and shown diagramatically in Fig. [5](#fig:time-deriv){reference-type="ref" reference="fig:time-deriv"}.

In addition, the user can also optimize the time-steps between each state. The time derivatives can be integrated over time, e.g. $q_{t+1} = q_t + \delta\tau_t\dot{q}_t$, where $\delta\tau_t$ is an increment in time. When `optimize_time=True`, then each $\delta\tau_t$ is included as decision variables in the optimal control problem.

### Decision variables and parameters

Decision variables are specified in the optimization builder class interface for the joint space, task space, and time steps. Each group of variables is given a unique label and can be retrieved using the `get_model_state` method. States are retrieved by specifying a robot name or task name, the required time index, and the time derivative order required. Additional decision variables can be included in the problem by using the `add_decision_variables` method given a unique name and dimension.

Parameters for the problem (e.g. safe distances) can be specified using the `add_parameter` method. To specify a new parameter, a unique name and dimension is required.

### Cost and constraint functions

The cost function in [\[eq:trajopt\]](#eq:trajopt){reference-type="eqref" reference="eq:trajopt"} is assumed to be made up of several cost terms, i.e. $$\begin{equation}
  \label{eq:cost-function}
  \text{cost}(x, u; T) = \sum_{i}~c_i(x, u; T)
\end{equation}$$ where $c_i: \mathbb{R}^{n_x}\times\mathbb{R}^{n_u}\rightarrow\mathbb{R}$ is an individual cost term modeling a specific sub-task. For example, let us define the cost terms $c_0 = \|\psi(x_T) - \psi^*\|^2$ and $c_1 = \lambda\int_0^T~\|u\|^2~dt$ (note, discretization is implicit in this formulation) where $\psi:\mathbb{R}^{n_x}\rightarrow\mathbb{R}^3$ is a function for the forward kinematics position (note, this can be provided by the robot model class as described in Sec. [3.1](#sec:robot-model){reference-type="ref" reference="sec:robot-model"}), $\psi^*\in\mathbb{R}^3$ is a goal task space position, and $0<\lambda\in\mathbb{R}$ is a scaling term used to weight the relative importance of one constraint against the other. Thus, $c_0$ describes an ideal state for the final state, and $c_1$ encourages trajectories with minimal control signals (e.g. minimize joint velocities). Each cost term is added to the problem using the `add_cost_term` method; the `build` sequence ensures each term is added to the objective function.

Several constraints can be added to the optimization problem by using the `add_equality_constraint` and `add_leq_inequality_constraint` methods that add equality and inequality constraints respectively. When the constraints are added to the problem, they are first checked to see if they are linear constraints with respect to the decision variables. This functionality allows the library to differentiate between linear and nonlinear constraints.

Additionally, OpTaS offers several methods that provide an implementation for common constraints, as, for example, joint position/velocity limits and time-integration for the system dynamics $f$ (e.g joint velocities can be integrated to positions).

## Solver interface {#sec:solver-interface}

OpTaS provides interfaces to solvers (open-source and commercial) that interface with CasADi [@Andersson2019] (such as IPOPT [@Wachter2006]), SNOPT [@Gill2005SNOPT], KNITRO [@byrd2006k], and Gurobi [@gurobi]), the Scipy `minimize` method [@2020SciPy-NMeth], OSQP [@osqp], and CVXOPT [@andersen2020cvxopt].

### Initialization of solver

When the solver is initialized, several variables are setup and the optimization problem object is set as a class attribute. The user must then call the `setup` method - that itself is an interface to the solver initialization that the user has chosen. The requirement of this method is to setup the interface for the specific solver; relevant solver parameters are passed to the interface at this stage.

### Resetting the interface

When using the solver as a controller, it is expected that the solver should be called more than once. In the case for feedback controllers or controllers with parameterized constraints (e.g. obstacles), this requires a way to reset the problem parameters. Furthermore, the initial seed for the optimizer is often required to be reset at each control loop cycle. To reset the initial seed and problem parameters the user calls `reset_initial_seed`, and `reset_parameters`, respectively. Both the initial seed and parameters are initialized by giving the name of the variables. The required vectorization is internally performed by the solver utilizing features of the `SXContainer` data structure. Note, if any decision variables or parameters are not specified in the reset methods then they automatically default to zero. This enables warm-starting the optimization routine, e.g. with the solution of the previous time-step problem.

### Solving an optimization problem

The optimization problem is solved by calling the `solve` method. This method passes the optimization problem to the desired solver. The resulting data from the solver is collected and transformed back into the state trajectory for each robot. A method is provided, named `interpolate`, is used to interpolate the computed trajectories across time. Additionally, the method `stats` retrieves available optimization statistics (e.g. number of iterations).

### Extensible solver interface

The solver interface has been implemented to allow for extensibility, i.e. additional optimization solvers can be easily integrated into the framework. When a user would like to include a new solver interface, they must create a new class that inherits from the `Solver` class. In their sub-class definition they must implement three methods: (i) `setup` which (as described above) initializes the solver interface, (ii) `_solve` that calls the solver and returns the optimized variable $X^*$, and (iii) `stats` that returns any statistics from the solver.

:::: {#fig:code-example .figure latex-placement="t"}
``` {fontsize="\\footnotesize" commandchars="\\\\\\{\\}"}
\PYG{k+kn}{import} \PYG{n+nn}{optas}

    \PYG{c+c1}{\PYGZsh{} Setup robot and optimization builder}
    \PYG{n}{T} \PYG{o}{=} \PYG{l+m+mi}{100} \PYG{c+c1}{\PYGZsh{} number of time steps in trajectory}
    \PYG{n}{urdf} \PYG{o}{=} \PYG{l+s+s1}{\PYGZsq{}/path/to/robot.urdf\PYGZsq{}}
    \PYG{n}{r} \PYG{o}{=} \PYG{n}{optas}\PYG{o}{.}\PYG{n}{RobotModel}\PYG{p}{(}\PYG{n}{urdf}\PYG{p}{,} \PYG{n}{time\PYGZus{}deriv}\PYG{o}{=}\PYG{p}{[}\PYG{l+m+mi}{0}\PYG{p}{,} \PYG{l+m+mi}{1}\PYG{p}{])}
    \PYG{n}{n} \PYG{o}{=} \PYG{n}{r}\PYG{o}{.}\PYG{n}{get\PYGZus{}name}\PYG{p}{()}
    \PYG{n}{b} \PYG{o}{=} \PYG{n}{optas}\PYG{o}{.}\PYG{n}{OptimizationBuilder}\PYG{p}{(}\PYG{n}{T}\PYG{o}{=}\PYG{n}{T}\PYG{p}{,} \PYG{n}{robots}\PYG{o}{=}\PYG{p}{[}\PYG{n}{r}\PYG{p}{])}

    \PYG{c+c1}{\PYGZsh{} Retrieve variables and setup parameters}
    \PYG{n}{q0} \PYG{o}{=} \PYG{n}{b}\PYG{o}{.}\PYG{n}{get\PYGZus{}model\PYGZus{}state}\PYG{p}{(}\PYG{n}{n}\PYG{p}{,} \PYG{n}{t}\PYG{o}{=}\PYG{l+m+mi}{0}\PYG{p}{)}
    \PYG{n}{qT} \PYG{o}{=} \PYG{n}{b}\PYG{o}{.}\PYG{n}{get\PYGZus{}model\PYGZus{}state}\PYG{p}{(}\PYG{n}{n}\PYG{p}{,} \PYG{n}{t}\PYG{o}{=\PYGZhy{}}\PYG{l+m+mi}{1}\PYG{p}{)} \PYG{c+c1}{\PYGZsh{} final state}
    \PYG{n}{pg} \PYG{o}{=} \PYG{n}{b}\PYG{o}{.}\PYG{n}{add\PYGZus{}parameter}\PYG{p}{(}\PYG{l+s+s1}{\PYGZsq{}pg\PYGZsq{}}\PYG{p}{,} \PYG{l+m+mi}{3}\PYG{p}{)} \PYG{c+c1}{\PYGZsh{} goal pos.}
    \PYG{n}{qc} \PYG{o}{=} \PYG{n}{b}\PYG{o}{.}\PYG{n}{add\PYGZus{}parameter}\PYG{p}{(}\PYG{l+s+s1}{\PYGZsq{}qc\PYGZsq{}}\PYG{p}{,} \PYG{n}{r}\PYG{o}{.}\PYG{n}{ndof}\PYG{p}{)} \PYG{c+c1}{\PYGZsh{} init q}
    \PYG{n}{o} \PYG{o}{=} \PYG{n}{b}\PYG{o}{.}\PYG{n}{add\PYGZus{}parameter}\PYG{p}{(}\PYG{l+s+s1}{\PYGZsq{}o\PYGZsq{}}\PYG{p}{,} \PYG{l+m+mi}{3}\PYG{p}{)} \PYG{c+c1}{\PYGZsh{} obstacle pos.}
    \PYG{n}{r} \PYG{o}{=} \PYG{n}{b}\PYG{o}{.}\PYG{n}{add\PYGZus{}parameter}\PYG{p}{(}\PYG{l+s+s1}{\PYGZsq{}r\PYGZsq{}}\PYG{p}{)}  \PYG{c+c1}{\PYGZsh{} obstacle radius}
    \PYG{n}{dt} \PYG{o}{=} \PYG{n}{b}\PYG{o}{.}\PYG{n}{add\PYGZus{}parameter}\PYG{p}{(}\PYG{l+s+s1}{\PYGZsq{}dt\PYGZsq{}}\PYG{p}{)} \PYG{c+c1}{\PYGZsh{} time step}

    \PYG{c+c1}{\PYGZsh{} Forward kinematics}
    \PYG{n}{p} \PYG{o}{=} \PYG{n}{r}\PYG{o}{.}\PYG{n}{get\PYGZus{}global\PYGZus{}link\PYGZus{}position}\PYG{p}{(}\PYG{n}{tip}\PYG{p}{,} \PYG{n}{qT}\PYG{p}{)}

    \PYG{c+c1}{\PYGZsh{} Cost and constraints}
    \PYG{n}{b}\PYG{o}{.}\PYG{n}{add\PYGZus{}cost\PYGZus{}term}\PYG{p}{(}\PYG{l+s+s1}{\PYGZsq{}c\PYGZsq{}}\PYG{p}{,} \PYG{n}{optas}\PYG{o}{.}\PYG{n}{sumsqr}\PYG{p}{(}\PYG{n}{p} \PYG{o}{\PYGZhy{}} \PYG{n}{pg}\PYG{p}{))}
    \PYG{n}{b}\PYG{o}{.}\PYG{n}{integrate\PYGZus{}model\PYGZus{}states}\PYG{p}{(}
        \PYG{n}{n}\PYG{p}{,} \PYG{n}{time\PYGZus{}deriv}\PYG{o}{=}\PYG{l+m+mi}{1}\PYG{p}{,} \PYG{n}{dt}\PYG{o}{=}\PYG{n}{dt}\PYG{p}{)}
    \PYG{n}{b}\PYG{o}{.}\PYG{n}{add\PYGZus{}equality\PYGZus{}constraint}\PYG{p}{(}\PYG{l+s+s1}{\PYGZsq{}init\PYGZsq{}}\PYG{p}{,} \PYG{n}{q0}\PYG{p}{,} \PYG{n}{qc}\PYG{p}{)}
    \PYG{k}{for} \PYG{n}{t} \PYG{o+ow}{in} \PYG{n+nb}{range}\PYG{p}{(}\PYG{n}{T}\PYG{p}{):}
        \PYG{n}{b}\PYG{o}{.}\PYG{n}{add\PYGZus{}leq\PYGZus{}inequality\PYGZus{}constraint}\PYG{p}{(}
            \PYG{n}{optas}\PYG{o}{.}\PYG{n}{sumsqr}\PYG{p}{(}\PYG{n}{p} \PYG{o}{\PYGZhy{}} \PYG{n}{o}\PYG{p}{),} \PYG{n}{r}\PYG{o}{**}\PYG{l+m+mi}{2}\PYG{p}{)}

    \PYG{c+c1}{\PYGZsh{} Build optimization problem and setup solver}
    \PYG{n}{solver} \PYG{o}{=} \PYG{n}{optas}\PYG{o}{.}\PYG{n}{CasADiSolver}\PYG{p}{(}
        \PYG{n}{b}\PYG{o}{.}\PYG{n}{build}\PYG{p}{())}\PYG{o}{.}\PYG{n}{setup}\PYG{p}{(}\PYG{l+s+s1}{\PYGZsq{}ipopt\PYGZsq{}}\PYG{p}{)}
```

::: caption
Example code for TO described in Section [4](#sec:code-example){reference-type="ref" reference="sec:code-example"}.
:::
::::

## Additional features

Support for integration with ROS [@Quigley09] is provided out-of-the-box. The ROS node provided is integrated with the ROS-PyBullet Interface [@Mower2022] so the publishers/subscribers can connect a robot in the optimization problem with a robot simulated in PyBullet.

In addition, we provide a port of the `spatialmath` library by Corke [@Corke17a] that supports CasADi variables. This library defines methods for manipulating homogeneous transformation matrices, quaternions, Euler angles, etc. using CasADi symbolic variables.

# Code Example {#sec:code-example}

In this section, we describe a common TO problem and give the code that models the problem. We aim to highlight how straightforward it is to setup a problem.

Consider a serial link manipulator, and goal to find a collision-free plan over time horizon $T$ to a goal end-effector position $p_g$ given a starting configuration $q_c$. A single spherical collision is represented by a position $o$ and radius $r$. The robot configuration $q_t$ represent states, and the velocities $\dot{q}_t$ are controls.

The cost function is given by $\|p(q_T) - p_g\|^2$ where $p$ is the position of the end-effector given by the forward kinematics. We solve the problem by minimizing the cost function subject to the constraints: (i) initial configuration, $q_0 = q_c$, (ii) joint limits $q^-\leq q_t\leq q^+$, and (iii) obstacle avoidance, $\|p(q_t) - o\|^2\geq r^2$. The system dynamics is represented by several equality constraints $q_{t+1} = q_t + \delta t\dot{q}_t$ that can be specified by methods already in-built into OpTaS. The code for the TO problem above, is shown in Fig. [6](#fig:code-example){reference-type="ref" reference="fig:code-example"}.

# Experiments {#sec:experiments}

:::: {#fig:pos-traj .figure}
![](Mower2023OpTaS_figs/kuka_views.png){#fig:kuka-start width="0.6\\columnwidth"}

\

![](Mower2023OpTaS_figs/plot_position_trajectory.png){#fig:plt-trajppos width="0.9\\columnwidth"}

::: caption
Comparison of end-effector task space trajectories computed using two different formulations. (a) Shows the start (left), and final configurations (right) for the robot under each approach. (b) Plots the end-effector position trajectory two dimensions.
:::
::::

## Optimization along custom dimensions

Popular solvers, such as TracIK [@Beeson2015], require the user to provide a 6D pose as the task space goal. Whilst this is applicable to several robotics problems (e.g. pick-and-place) it may not be necessary to optimize each task space dimension (e.g. spraying applications does not require optimization in the roll angular direction). Furthermore, optimizing in more dimensions than necessary may be disadvantageous.

OpTaS can optimize or neglect any desired task space dimension. This can have certain advantages, for example increasing the robot workspace. Consider a non-prehensile pushing task along the plane, optimizing the full 6D pose may not be ideal since the task is two dimensional. By optimizing in the two dimensional plane and specifying boundary constraints on the third linear spatial dimension, increases the robots workspace.

We setup a tracking experiment in OpTaS using a simulated Kuka LWR robot arm to compare the two cases: (i) optimize the full 6D pose, and (ii) optimize 2D linear position. The robot is given an initial configuration (Fig. [7](#fig:kuka-start){reference-type="ref" reference="fig:kuka-start"} left) and the task is to move the end-effector with velocity of constant magnitude and direction in the 2D plane. The end configuration for each approach is shown in Fig. [7](#fig:kuka-start){reference-type="ref" reference="fig:kuka-start"} right and the end-effector trajectories are shown in Fig. [8](#fig:plt-trajppos){reference-type="ref" reference="fig:plt-trajppos"}. We see that the 2D optimization problem is able to reach a greater distance, highlighting that the robot workspace is increased.

## Performance comparison

In this section, we demonstrate that OpTaS can formulate similar problems and compare its performance to alternatives. First, we model, with OpTaS, the same problem as used in TracIK [@Beeson2015] and in addition we also model the problem using EXOTica [@exotica]. The Scipy SLSQP solver [@Kraft1988] was used for OpTaS and EXOTica. With same Kuka LWR robot arm in the previous experiment, we setup a task where the robot must track a figure-of-eight motion in task space (Fig. [10](#fig:kuka-fig8){reference-type="ref" reference="fig:kuka-fig8"}) and record the CPU time for the solver duration at each control loop cycle. The results are shown in Fig. [11](#fig:time-comparison){reference-type="ref" reference="fig:time-comparison"}. TracIK is the fastest ($0.049\pm 0.035$ms), which is expected since it is optimized for a specific problem formulation. We see that OpTaS ($2.608\pm 0.239$ms) is faster than EXOTica ($3.694\pm 0.300$ms)

A second experiment, using the same setup as before, was performed comparing the performance of OpTaS against EXOTica with an additional cost term to maximize manipulability [@Yoshikawa85]. The results are shown in Fig. [12](#fig:err-comparison){reference-type="ref" reference="fig:err-comparison"}. Despite using the same formulation and solver, OpTaS ($2.650\pm 0.270$ms) achieved better performance than EXOTica ($7.640\pm 1.404$ms). Without extensive profiling it is difficult to precisely explain this difference. However, EXOTica requires the user to supply analytical gradients for sub-tasks (called *task maps* in the EXOTica documentation). EXOTica does not provide the gradients for the manipulability task, and thus falls-back to using the finite difference method to estimate the gradient - this can can be slow to compute.

![Figure-of-eight trajectory tracked by the Kuka LWR.](Mower2023OpTaS_figs/kuka_fig8.png){#fig:kuka-fig8 width="0.3\\columnwidth"}

:::: {#fig:comparisons .figure latex-placement="t"}
![](Mower2023OpTaS_figs/optas_cmp_crop.png){#fig:time-comparison width="\\columnwidth"}

 

![](Mower2023OpTaS_figs/optas_cmp_manip_crop.png){#fig:err-comparison width="\\columnwidth"}

::: caption
Solver duration comparisons for figure of eight motion. (a) Compares an IK tracking approach described in Section [5](#sec:experiments){reference-type="ref" reference="sec:experiments"}, (b) is a similar comparison that includes a maximization term for manipulability. Green is OpTaS, red is TracIK, and blue is EXOTica.
:::
::::

# Conclusions {#sec:conclusions}

In this paper, we have proposed OpTaS: an optimization-based task tpecification Python library for TO and MPC. OpTaS allows a user to setup a constrained nonlinear programs for custom problem formulations and has been shown to perform well against alternatives. Parameterization enables programs to act as feedback controllers, motion planners, and benchmark problem formulations and solvers.

We hope OpTaS will be used by researchers, students, and industry to facilitate the development of control and motion planning algorithms. The code base is easily installed via `pip` and has been made open-source under the Apache 2 license: <https://github.com/cmower/optas>.

[^1]: C. E. Mower, C. Bergeles and T. Vercauteren are with the School of Biomedical Engineering & Imaging Sciences, King's College London, UK. J. Moura and S. Vijaykumar are with School of Informatics, University of Edinburgh, UK. Correspondence: [christopher.mower@kcl.ac.uk](mailto:chris.mower@kcl.ac.uk).

[^2]: This research received funding from the European Union's Horizon 2020 research and innovation program under grant agreement No. 101016985 (FAROS). Further, this work was supported by core funding from the Wellcome/EPSRC \[WT203148/Z/16/Z; NS/A000049/1\]. T.  Vercauteren is supported by a Medtronic / RAEng Research Chair \[RCSRF1819\7\34\], and C. Bergeles by an ERC Starting Grant \[714562\]. This work has received funding from the European Union's Horizon 2020 research and innovation programme under grant agreement No 101017008, Enhancing Healthcare with Assistive Robotic Mobile Manipulation (HARMONY). This work was supported by core funding from the Wellcome/EPSRC \[WT203148/Z/16/Z; NS/A000049/1\]. This research is supported by Kawada Robotics Corporation, Japan and the Alan Turing Institute, UK.

[^3]: $^{*}$C. Bergeles and T. Vercauteren equally contributed to the work.

[^4]: For the purpose of open access, the authors have applied a CC BY public copyright license to any Author Accepted Manuscript version arising from this submission.

[^5]: <http://wiki.ros.org/urdf>
