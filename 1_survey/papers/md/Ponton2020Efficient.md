---
citation_key: Ponton2020Efficient
arxiv_id: 2010.01215
arxiv_url: https://arxiv.org/abs/2010.01215
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-24T16:48:54Z
origin: ai+web
reviewed: false
---

# Introduction

The computation of multi-contact motions remains a difficult yet important challenge for legged locomotion and manipulation in order to afford more versatile behaviors in complex environments. Of particular interest are methods that can compute such motions in real-time without making restrictive assumptions on the solution set. Indeed, they can provide the necessary adaptive behavior required in uncertain environments without trading-off motion versatility.

Very successful walking pattern generators often rely on simplified linear models of the dynamics [@Kajita:2003gj] as they offer important computational advantages that make them suitable for receding horizon control [@DBLP:conf/iros/Wieber08; @journals/corr/KuindersmaPT13; @journals/trob/EnglsbergerOA15]. Unfortunately, these models are fundamentally restricted to locomotion patterns with predefined gaits on quasi-flat grounds. While extensions of such models can enable the use of hands to maintain balance [@mason_mpc_2018], they make substantial assumptions on the admissible gaits and are thus limited by the range of gaits they can generate.

Complete rigid body dynamics models including interaction dynamics, in principle, afford the synthesis of a wider range of behaviors for more complex motion tasks. Despite the inherent computational challenges, very impressive motions can be computed [@journals/tog/MordatchTP12; @DBLP:conf/iros/TassaET12; @DBLP:conf/iros/ErezT12; @DBLP:conf/iros/KoenemannPTTSBM15; @TimeSwitchedJonas; @Neunert2017TrajectoryOT; @DBLP:journals/corr/abs-1711-11006; @DBLP:conf/wafr/PosaT12; @Manchester09stabledynamic; @MombaurSomersault; @DBLP:conf/syroco/KochMS12]. However such approaches are often limited for receding horizon control as they require the resolution of non-convex, high dimensional optimization problems, often with complex nonlinear constraints such as complementarity constraints for contact dynamics.

Middle-complexity options that decouple the pattern generation problem into simpler sub-problems have also been studied. They typically assume that a sequence of contact configuration be provided first, typically using an efficient search algorithms for contact sequences [@Tonneau:2018dm; @escande2013planning; @lin2017; @DBLP:conf/humanoids/DeitsT14; @NishiS14]. Of special interests are methods based on the centroidal dynamics of the robot [@OrinCentroidalMomentum; @Kajita:2003gj; @DynamicsAnalysis] which have become very popular recently [@Wensing:2013fm; @DBLP:conf/humanoids/DaiVT14; @Herzog-2016b]. Indeed, under mild assumptions on the kinematic and actuation feasibility, this model provides sufficient conditions to plan dynamically consistent full-body motions with multiple contacts. This model is simple enough to be amenable to online resolution and at the same time expressive to plan complex behaviors [@JustinMomentumOptimization; @TROCarpentier; @winkler18; @Audren:2014gl; @AlexHumanoidsPaper]. It is then possible to combine momentum dynamics with a full kinematic model to plan highly dynamic motions [@DBLP:conf/humanoids/DaiVT14]. This decomposition between centroidal dynamics and kinematics models was, for example, leveraged to create an alternating algorithm that efficiently computes full-body motions in multi-contact by iteratively solving two separate optimization problems until they reach consensus [@Herzog-2016b; @AlexHumanoidsPaper]. This connection has then been further explored in [@budhiraja2018dynamics], which proposed a method to optimize both centroidal and full-body motions using an Alternating Direction Method of Multipliers formulation.

While promising, approaches based on the centroidal momentum dynamics are inherently non-convex and thus still challenging to solve efficiently. This led researchers to focus on the mathematical structure of the problem to derive more efficient methods. For example, convex bounds on the angular momentum rate (that maximizes the contact wrench cone margin) are used to minimize a worst-case bound on the $l_1$ angular momentum norm via convex optimization [@Dai:2016hz]. In [@JustinMomentumOptimization; @TROCarpentier], the bilinear terms of the momentum dynamics and timings are handled by a dedicated multiple-shooting solver and, proxy constraints are used for handling whole-body limits based on an offline learning method. [@Audren:2014gl] exploits a linear approximation of the momentum dynamics based on a lower dimensional space projection and an adaptive method for timing optimization to control a robot in multi-contact scenarios in a receding horizon fashion. In [@TOPP; @Caron:2016wt], the interpretation of friction cones as dual twists allows to compute online cones of feasible CoM accelerations. The resulting bilinear constraints are decoupled into linear pairs via a conservative trajectory-wide contact-stability criterion for online motion generation. Timings between contact switches are optimized online by solving an easy-to-solve nonlinear problem.

In [@Herzog-2016b], we further studied the problem structure and proposed an analytic decomposition of positive and negative definite terms of the problem Lagrangian based on the decomposition of angular momentum non-convex terms. This led to a solver with improved convergence properties. In our previous work [@ConvexModelMomentumDynamics], we proposed a convex relaxation of the problem that suggested the use of a proxy function to minimize angular momentum, namely the sum of the squares of the terms composing the non convex part of the dynamics. While computationally very efficient, this approach was limited as it did not allow the inclusion of an explicit target angular momentum in the cost function, therefore severely limiting the space of solutions. Moreover, the approach could not be used with the alternating full-body motion optimization method discussed above.

In this paper, extending our preliminary work [@TimeOptimization], we study a general convex relaxation of the problem that allows the explicit inclusion of angular momentum objectives and naturally extends to the optimization of timing, a feature missing in most contributions on centroidal dynamics optimization. The main contributions of the paper are[^4]

- Exploiting the structure of the centroidal dynamics optimization problem, we propose two computationally efficient algorithms formulated as a sequence of convex second order cone programs to compute physically consistent center of mass, angular momentum and contact force trajectories and demonstrate how timing optimization can be efficiently included.

- We show how our approach can be efficiently used with the kino-dynamic optimization method proposed in [@AlexHumanoidsPaper] to generate full-body physically-consistent movements. We further extend the approach to also include actuation limit constraints.

- We extend the approach in a mixed-integer program to find dynamically consistent contact sequences and locations.

- Finally, we evaluate the capabilities and limitations of our approach in simulation on several multi-contact scenarios for a biped and a quadruped robot, we study the benefits of timing optimization to extend the range of possible behaviors and demonstrate the execution of these movements on a real quadruped robot.

The software implementation of the algorithms presented in this paper is open-source and freely available [@opensourcelink]. We state the problem and present background material in Section [2](#sec:problem_formulation){reference-type="ref" reference="sec:problem_formulation"}. In Section [3](#sec:opt_movement){reference-type="ref" reference="sec:opt_movement"}, we detail the motion optimization approach and in Section [4](#sec:contacts_planning){reference-type="ref" reference="sec:contacts_planning"} the contacts planning approach using mixed integer programming. We present simulation and real robot results in Section [5](#sec:experiments){reference-type="ref" reference="sec:experiments"} and discuss the features and limitations of our proposed framework in Section [6](#sec:discussion){reference-type="ref" reference="sec:discussion"}. Finally, we conclude in Section [7](#sec:conclusion){reference-type="ref" reference="sec:conclusion"}.

# Preliminaries and Problem Formulation {#sec:problem_formulation}

![Our architecture maps a high-level task description into functional motions. The initial state $\mathbf{r}            _{0},  \mathbf{l}            _{0},  \mathbf{k}            _{0}$ of the robotic platform (simulated humanoid or a real quadruped robot), a desired CoM motion $\Delta \mathbf{r}$, a description of the $\mathrm{R}$ surfaces that compose the terrain and a set of costs $\indexed{ \phi                  }[cnt][ \mathrm{t}            ](\cdot), \indexed{ \phi                  }[kin][ \mathrm{t}            ](\cdot), \indexed{ \phi                  }[dyn][ \mathrm{t}            ](\cdot), \indexed{ \phi                  }[fb][ \mathrm{t}            ](\cdot)$ are used to select a set of surfaces $\indexed{ \pazocal{S}           }[][\{  \mathfrak{r}          \}]$ that support a dynamic motion, optimize a kino-dynamic motion over a discrete time horizon $N$, and synthesize a set of feedback gains $\mathbf{K}_{ \mathbf{h}            }, \mathbf{K}_{ \mathbf{q}            }, \mathbf{K}_{ \lambda              _{ \mathrm{e}            }}$ that define closed-loop behaviors to be realized by an inverse dynamics controller as in [@AlexAuroPaper; @compliant_terrain_adaptation; @robust_biped_walking]. ](figures/ctrlarch/ControlArchitecture.pdf){#fig:ExecutionArchitecture width="98%"}

In this section, we introduce the centroidal dynamics optimization problem for multi-contact locomotion in the larger context of full-body optimization. First, we provide an overview of the larger kino-dynamic optimization problem, present the structured approach used in our architecture to tackle it and outline the centroidal dynamics optimization problem, which is the core focus of this paper. Our overall approach is summarized in Figure [1](#fig:ExecutionArchitecture){reference-type="ref" reference="fig:ExecutionArchitecture"}. From a task description we first select a sequence on physically-feasible contact sequences using mixed integer programming (Sec. [4](#sec:contacts_planning){reference-type="ref" reference="sec:contacts_planning"}). This sequence is used to optimize a time-optimal full-body movements using our kino-dynamic solver (Fig. [3](#fig:KinDynStructure){reference-type="ref" reference="fig:KinDynStructure"}). These movements are then tracked with an instantaneous whole-body feedback controller.

## Kino-dynamic optimization of multi-contact behaviors

To synthesize full-body multi-contact behaviors, we seek to efficiently solve an optimal control problem of the form $$\begin{align}
        %
        % General objective function
        %
        \min_{ \mathbf{q}            ( \mathrm{t}            ),  \Lambda              ( \mathrm{t}            ), \indexed{ \lambda              }[][ \mathrm{e}            ]( \mathrm{t}            )} & \indexed{ \phi                  }[][end] \left( \mathbf{q}            ,  \mathbf{\dot{q}}      ,  \mathbf{\ddot{q}}     ,  \Lambda              , {\indexed{ \lambda              }[][ \mathrm{e}            ]} \right) + \int\limits_{0}^{ \pazocal{T}           } \indexed{ \phi                  }[][ \mathrm{t}            ]\left( \mathbf{q}            ,  \mathbf{\dot{q}}      ,  \mathbf{\ddot{q}}     ,  \Lambda              , {\indexed{ \lambda              }[][ \mathrm{e}            ]} \right) \mathrm{d} \mathrm{t}            \label{eq_problem_cost} \\
        %
        % Equations of motion
        %
        \textrm{subject to}\;\; &  \indexed{ \mathbf{M}           }( \mathbf{q}            ) \mathbf{\ddot{q}}     + \indexed{ \mathbf{h}           }( \mathbf{q}            , \mathbf{\dot{q}}      ) =  \mathbf{S}           ^{T}  \Lambda              + \hspace{-0.1cm} \sum_{ \mathrm{e}            \in   \mathrm{e}            _{\mathrm{cnt}} } \hspace{-0.1cm} \indexed{ \mathbf{J}           }[][ \mathrm{e}            ]( \mathbf{q}            )^{T} \indexed{ \lambda              }[][ \mathrm{e}            ] \label{eq_of_motion} \\
        %
        % Joint limits
        %
        & \;  \mathbf{q}_{\textrm{jnt}}\in [ \indexed[min]{ \mathbf{q}_{\textrm{jnt}}}, \indexed[max]{ \mathbf{q}_{\textrm{jnt}}} ]  \label{eq_joint_limits} \\
        %
        % Torque limits
        %
        & \;  \Lambda              \in [\indexed[min]{ \Lambda              }, \indexed[max]{ \Lambda              }] \label{eq_torque_limits}\\
        %
        % Contact forces, velocity and acceleration limits
        %
        & \; (\indexed{ \lambda              }[][ \mathrm{e}            ],  \mathbf{\dot{q}}      ,  \mathbf{\ddot{q}}     ) \in \Omega \label{eq:force_vel_constraints}
    \end{align}
    \label{eqns_general_problem}$$ which minimizes a performance cost $\phi                  (\cdot)$, composed of a terminal cost $\indexed{ \phi                  }[][end]$ and the integral of a running cost $\indexed{ \phi                  }[][ \mathrm{t}            ]$, over a finite time horizon $\pazocal{T}$ under a set of physical constraints. It enforces the equations of motion for a floating-base rigid-body system (Eq. $\eqref{eq_of_motion}$), joint and torque limits (Eqs. [\[eq_joint_limits\]](#eq_joint_limits){reference-type="eqref" reference="eq_joint_limits"}-[\[eq_torque_limits\]](#eq_torque_limits){reference-type="eqref" reference="eq_torque_limits"}), as well as contact forces, velocity and acceleration constraints (Eq. [\[eq:force_vel_constraints\]](#eq:force_vel_constraints){reference-type="eqref" reference="eq:force_vel_constraints"}). Here, $\mathbf{q}            = \begin{bmatrix}  \mathbf{x}            ^{T} \;  \mathbf{q}_{\textrm{jnt}}^{T} \end{bmatrix}^{T}$ denotes the robot posture composed of $\mathbf{x}            \in SE(3)$, the pose of the floating-base relative to an inertial frame, and $\mathbf{q}_{\textrm{jnt}}\in  \mathbb{R}            ^ \mathrm{n}$, the joint positions, where $\mathrm{n}$ is the number of joints. $\Lambda              ( \mathrm{t}            ) \in  \mathbb{R}            ^ \mathrm{n}$ are joint torques and $\indexed{ \lambda              }[][ \mathrm{e}            ]( \mathrm{t}            ) \in  \mathbb{R}            ^{6}$ is the contact wrench of endeffector $\mathrm{e}            \in   \mathrm{e}            _{\mathrm{cnt}}$ (where $\mathrm{e}            _{\mathrm{cnt}}$ is the set of endeffectors in contact with the environment at the time in question). $\indexed{ \mathbf{M}           }( \mathbf{q}            ) \in  \mathbb{R}            ^{( \mathrm{n}            +6) \times ( \mathrm{n}            +6)}$ is the inertia matrix; $\indexed{ \mathbf{h}           }( \mathbf{q}            , \mathbf{\dot{q}}      ) \in  \mathbb{R}            ^{ \mathrm{n}            +6}$ a vector of generalized forces including Coriolis, centrifugal, gravity and joint friction forces. $\mathbf{S}           = \begin{bmatrix} \mathbf{0}^{ \mathrm{n}            \times 6} \; \mathbf{I}^{ \mathrm{n}            \times  \mathrm{n}            } \end{bmatrix}$ is a selection matrix reflecting the system under-actuation and $\indexed{ \mathbf{J}           }[][ \mathrm{e}            ]( \mathbf{q}            ) \in  \mathbb{R}            ^{6 \times ( \mathrm{n}            +6)}$ is the contact Jacobian of endeffector $\mathrm{e}$. The pre-superscripts $\mathrm{min}$ and $\mathrm{max}$ for joint positions $\mathbf{q}_{\textrm{jnt}}$ and joint torques $\Lambda$ denote their minimum and maximum limits. The set $\Omega$ denotes constraints such as friction or non-sliding contacts, that will be explicitly defined within the next subsection. Note that additional kinematic constraints could also be added to the problem without changing the reasoning below.

The problem described in Eq. [\[eqns_general_problem\]](#eqns_general_problem){reference-type="eqref" reference="eqns_general_problem"} is nonlinear, non-convex and computationally intensive and we seek to formulate a more tractable approximation without sacrificing the versatility of motion synthesis. The equations of motion can be decomposed into actuated (superscript $\mathrm{a}$) and unactuated parts (superscript $\mathrm{u}$) $$\begin{align}
    %
    % Unactuated part EoM
    %
    \indexed{ \mathbf{M}           }[u]( \mathbf{q}            ) \mathbf{\ddot{q}}     + \indexed{ \mathbf{h}           }[u]( \mathbf{q}            , \mathbf{\dot{q}}      ) &= \sum_{ \mathrm{e}            \in   \mathrm{e}            _{\mathrm{cnt}} } \indexed{ \mathbf{J}           }[u][ \mathrm{e}            ]( \mathbf{q}            )^{T} \indexed{ \lambda              }[][ \mathrm{e}            ] \label{eq_unactuated_part} \\
    %
    % Actuated part EoM
    %
    \indexed{ \mathbf{M}           }[a]( \mathbf{q}            ) \mathbf{\ddot{q}}     + \indexed{ \mathbf{h}           }[a]( \mathbf{q}            , \mathbf{\dot{q}}      ) &= \sum_{ \mathrm{e}            \in   \mathrm{e}            _{\mathrm{cnt}} } \indexed{ \mathbf{J}           }[a][ \mathrm{e}            ]( \mathbf{q}            )^{T} \indexed{ \lambda              }[][ \mathrm{e}            ] +  \Lambda              \label{eq_actuated_part}
    \end{align}$$ As shown in [@AlexAuroPaper], the actuated part of the dynamics provides the necessary actuation torques needed to achieve any combination of desired acceleration $\mathbf{\ddot{q}}$ and contact forces $\indexed{ \lambda              }[][ \mathrm{e}            ]$. Thus, assuming sufficient actuation $\Lambda$, it is possible to ignore the actuated part of the equations of motion (Eq. [\[eq_actuated_part\]](#eq_actuated_part){reference-type="eqref" reference="eq_actuated_part"}) and base the synthesis of multi-contact behaviors only on the unactuated part (Eq. [\[eq_unactuated_part\]](#eq_unactuated_part){reference-type="eqref" reference="eq_unactuated_part"}). As we will later in the paper, it is nevertheless possible to add torque limits in the decoupled optimization problems. In [@robust_biped_walking; @WieberNonholonomy], it has been shown that the right-hand side of the unactuated part and the gravitational effects of the vector of nonlinear terms $\indexed{ \mathbf{h}           }[u]( \mathbf{q}            , \mathbf{\dot{q}}      )$ that relate the acceleration of the floating-base to external contact forces, are equivalent to the robot centroidal momentum dynamics $$\begin{equation}
    %
    % Robot momenta
    %
    \begin{bmatrix}
         \mathbf{\dot{l}}      \\[0.5em]
         \mathbf{\dot{k}}      \\[0.5em]
    \end{bmatrix} =
    %
    % Definition in terms of force and torques
    %
    \underbrace{
        \begin{bmatrix}
             m                      \mathbf{g}            + \sum\limits_{ \mathrm{e}            \in   \mathrm{e}            _{\mathrm{cnt}} } \indexed{ \mathbf{f}            }[][ \mathrm{e}            ] \\[0.0em]
            \sum\limits_{ \mathrm{e}            \in   \mathrm{e}            _{\mathrm{cnt}} } ( (\indexed{ \mathbf{p}            }[][ \mathrm{e}            ] + \indexed{ \mathbf{R}            }[ \mathrm{x}            , \mathrm{y}            ][ \mathrm{e}            ] \indexed{ \mathbf{\mathfrak{z}} }[][ \mathrm{e}            ] -  \mathbf{r}            ) \times \indexed{ \mathbf{f}            }[][ \mathrm{e}            ] + \indexed{ \mathbf{R}            }[ \mathrm{z}            ][ \mathrm{e}            ] \indexed{ \tau                  }[][ \mathrm{e}            ] ) \\[0.0em]
        \end{bmatrix}
    }_{\textrm{From {\color{black} Newton-Euler} dynamics}}\label{eqns_momentum_dynamics}
\end{equation}$$

![The figure illustrates the representation used in the paper. ](Ponton2020Efficient_figs/RobotNotation.png){#fig1:schematic width="68%"}

![Schematic of the kino-dynamic optimization approach that iteratively computes contact force $\indexed{ \lambda              }[][ \mathrm{e}            ]$ and whole-body trajectories $\mathbf{q}            ,  \mathbf{\dot{q}}      ,  \mathbf{\ddot{q}}$ until convergence of the common set of variables: CoM $\indexed{ \mathbf{r}            }[][ \mathrm{t}            ]$, robot momenta $\indexed{ \mathbf{l}            }[][ \mathrm{t}            ], \indexed{ \mathbf{k}            }[][ \mathrm{t}            ]$ and endeffector poses $\indexed{ \mathbf{p}            }[][ \mathrm{e}            , \mathrm{t}            ]$. The vector $\indexed{ \mathbf{h}            }[][ \mathrm{t}            ]$ is built by vertically stacking CoM and robot momenta. The pre superscripts $\mathrm{kin}$ and $\mathrm{dyn}$ relate the variables to the problem they are a solution for. The optimization objective $\phi$ is assumed to be separable and composed by $\indexed{ \phi                  }[dyn][ \mathrm{t}            ] + \indexed{ \phi                  }[kin][ \mathrm{t}            ]$. Finally, the cost penalties $\indexed{ \Phi                  }[dyn][ \mathrm{t}            ], \indexed{ \Phi                  }[kin][ \mathrm{t}            ]$ ensure the consensus of the solutions at convergence.](figures/kinodyn/KinoDynStructure.pdf){#fig:KinDynStructure width="36%"}

The center of mass position is denoted $\mathbf{r}$ and the linear and angular momentum expressed at the CoM are written as $\mathbf{l}$ and $\mathbf{k}$. $m$ is the robot mass and $\mathbf{g}$ the gravity vector. The endeffector frame is located at the endeffector position $\indexed{ \mathbf{p}            }[][ \mathrm{e}            ]$, and it is oriented so that $\indexed{ \mathbf{R}            }[ \mathrm{z}            ][ \mathrm{e}            ] \in  \mathbb{R}            ^{3 \times 1}$ is normal to the contact surface, and $\indexed{ \mathbf{R}            }[ \mathrm{x}            ][ \mathrm{e}            ],\indexed{ \mathbf{R}            }[ \mathrm{y}            ][ \mathrm{e}            ] \in  \mathbb{R}            ^{3 \times 1}$ are aligned with the rectangular shape of the endeffector support surface in the desired motion direction. The rotation matrix $\indexed{ \mathbf{R}            }[][ \mathrm{e}            ] = \begin{bmatrix} \indexed{ \mathbf{R}            }[ \mathrm{x}            ][ \mathrm{e}            ] & \hspace{-0.2cm} \indexed{ \mathbf{R}            }[ \mathrm{y}            ][ \mathrm{e}            ] & \hspace{-0.2cm} \indexed{ \mathbf{R}            }[ \mathrm{z}            ][ \mathrm{e}            ] \end{bmatrix}   \in  \mathbb{R}            ^{3 \times 3}$ rotates quantities from endeffector to inertial frame. For instance, the endeffector force $\indexed{ \mathbf{f}            }[][ \mathrm{e}            ]$, expressed in the inertial frame, is equivalent in local endeffector coordinates to $\indexed{ \mathbf{\mathfrak{f}} }[][ \mathrm{e}            ] = {\indexed{ \mathbf{R}            }[][ \mathrm{e}            ]}^{T} \indexed{ \mathbf{f}            }[][ \mathrm{e}            ]$. The center of pressure (CoP) $\indexed{ \mathbf{\mathfrak{z}} }[][ \mathrm{e}            ] \in  \mathbb{R}            ^{2}$ expressed in local endeffector frame and scalar torque $\indexed{ \tau                  }[][ \mathrm{e}            ]$ at the CoP complete the description of the endeffector wrench. They can be equivalently described by a torque at $\indexed{ \mathbf{p}            }[][ \mathrm{e}            ]$ as $\indexed{ \gamma                }[][ \mathrm{e}            ] = (\indexed{ \mathbf{R}            }[ \mathrm{x}            , \mathrm{y}            ][ \mathrm{e}            ] \indexed{ \mathbf{\mathfrak{z}} }[][ \mathrm{e}            ]) \times \indexed{ \mathbf{f}            }[][ \mathrm{e}            ] + \indexed{ \mathbf{R}            }[ \mathrm{z}            ][ \mathrm{e}            ] \indexed{ \tau                  }[][ \mathrm{e}            ]$. The endeffector wrench can now be defined as $\indexed{ \lambda              }[][ \mathrm{e}            ] = \begin{bmatrix} { \mathbf{f}            }^{T}_{ \mathrm{e}            } & \hspace{-0.2cm} { \gamma                }^{T}_{ \mathrm{e}            } \end{bmatrix}^{T}$. Figure [2](#fig1:schematic){reference-type="ref" reference="fig1:schematic"} depicts coordinate frames and the notation.

It has been shown [@OrinCentroidalMomentum] that the left-hand side of the unactuated part in Eq. [\[eq_unactuated_part\]](#eq_unactuated_part){reference-type="eqref" reference="eq_unactuated_part"}, under an appropriate coordinate transformation from the floating base to the robot's CoM, relates the robot rate of momenta expressed at the robot's center of mass ($\mathbf{\dot{l}}      ,  \mathbf{\dot{k}}$) to the robot velocity $\mathbf{\dot{q}}$ and acceleration $\mathbf{\ddot{q}}$ via the centroidal momentum matrix $\indexed{ \mathbf{M}           }[u][CoM]( \mathbf{q}            ) \in  \mathbb{R}            ^{6 \times ( \mathrm{n}            +6)}$.

$$\begin{equation}
%
% Definition in terms of kinematics
%
\underbrace{
    \frac{d}{d \mathrm{t}            } \left[ {\indexed{ \mathbf{M}           }[u][CoM]( \mathbf{q}            )  \mathbf{\dot{q}}      } \right]
}_{\textrm{From {\color{black} full-body} kinematics}} =
%
\indexed{ \mathbf{M}           }[u][CoM]( \mathbf{q}            )  \mathbf{\ddot{q}}     + \indexed{\dot{ \mathbf{M}           }}[u][CoM]( \mathbf{q}            )  \mathbf{\dot{q}}      =
%
% Robot momenta
%
\begin{bmatrix}
     \mathbf{\dot{l}}      \\[0.2em]
     \mathbf{\dot{k}}      \\[0.2em]
\end{bmatrix}
\label{eqns_kindyn_momentum_dynamics}
\end{equation}$$

At this point, it becomes clear that the problem of finding feasible multi-contact motions can be reduced to the optimization of centroidal dynamics (Eq. [\[eqns_momentum_dynamics\]](#eqns_momentum_dynamics){reference-type="eqref" reference="eqns_momentum_dynamics"}) and the optimization of full-body kinematics (Eq. [\[eqns_kindyn_momentum_dynamics\]](#eqns_kindyn_momentum_dynamics){reference-type="eqref" reference="eqns_kindyn_momentum_dynamics"}) as long as the motion-induced momentum agrees with the dynamic optimization. In [@AlexHumanoidsPaper], an alternating algorithm to solve the optimal control problem [\[eqns_general_problem\]](#eqns_general_problem){reference-type="eqref" reference="eqns_general_problem"} using this idea was proposed (see Fig. [3](#fig:KinDynStructure){reference-type="ref" reference="fig:KinDynStructure"}). It optimized centroidal dynamic motions and full-body kinematics separately, but ensured through added cost penalties that both optimization problems come to an agreement on their common variables: CoM, momentum and contact locations.

In this paper, we use the complete architecture shown in Figure [1](#fig:ExecutionArchitecture){reference-type="ref" reference="fig:ExecutionArchitecture"} to evaluate our contributions, but our work mostly focuses on the centroidal dynamics optimization problem, which is sufficient to synthesize physically consistent motion behaviors.

## Dynamic optimization with the centroidal dynamics

We now present in detail the centroidal dynamics optimization problem we are interested in, that synthesizes a motion plan (timing, contact wrenches and momentum trajectories) under the momentum dynamics (Eq. [\[eqns_momentum_dynamics\]](#eqns_momentum_dynamics){reference-type="eqref" reference="eqns_momentum_dynamics"}) and is optimal in terms of a desired quadratic performance objective. First, we discretize the dynamics equations using Euler's methods and then seek a local solution for the following problem: $$\begin{align}
        \phantom{abcdefghi}
        &\begin{aligned}
            %
            % Objective function
            %
            \mathllap{\min_{\substack{\indexed{ \mathbf{h}            }[][ \mathrm{t}            ], \indexed{ \Delta                }[][ \mathrm{t}            ], \indexed{ \mathbf{p}            }[][ \mathrm{e}            , \mathrm{t}            ] \\ \indexed{ \mathbf{f}            }[][ \mathrm{e}            , \mathrm{t}            ], \indexed{ \mathbf{\mathfrak{z}} }[][ \mathrm{e}            , \mathrm{t}            ], \indexed{ \tau                  }[][ \mathrm{e}            , \mathrm{t}            ]}}}
            %
            &\sum\limits_{ \mathrm{t}            =1}^{ N                     } \hspace{-0.075cm}
            %
            % Dynamics part of the cost
            %
            \left[ \hspace{-0.05cm}\indexed{ \phi                  }[dyn][ \mathrm{t}            ] \hspace{-0.1cm}\left(
            \begin{matrix}
                \indexed{ \mathbf{h}            }[][ \mathrm{t}            ], \indexed{ \Delta                }[][ \mathrm{t}            ], \indexed{ \mathbf{p}            }[][ \mathrm{e}            , \mathrm{t}            ],\\
                \indexed{ \mathbf{\mathfrak{z}} }[][ \mathrm{e}            , \mathrm{t}            ], \indexed{ \mathbf{f}            }[][ \mathrm{e}            , \mathrm{t}            ], \indexed{ \tau                  }[][ \mathrm{e}            , \mathrm{t}            ]
            \end{matrix} \right) \hspace{-0.05cm}+\hspace{-0.025cm}
            %
            % Consensus part of the cost
            %
            \indexed{ \Phi                  }[dyn][ \mathrm{t}            ] \hspace{-0.1cm} \left(
            \begin{matrix}
                \indexed{ \mathbf{h}            }[][ \mathrm{t}            ] - \indexed[kin]{ \mathbf{h}            }[][ \mathrm{t}            ] \\
                \indexed{ \mathbf{p}            }[][ \mathrm{e}            , \mathrm{t}            ] - \indexed[kin]{ \mathbf{p}            }[][ \mathrm{e}            , \mathrm{t}            ]
            \end{matrix} \right) \hspace{-0.05cm} \right]
        \end{aligned} \hspace{-0.5cm} \label{eq_dynopt_cost} \\[0.0cm]
        &\begin{aligned}
            %
            % Centroidal dynamics
            %
            \mathllap{\textrm{subject to}}\;
            & \;  \mathbf{h}            _{ \mathrm{t}            } =
            \begin{bmatrix}
                \indexed{ \mathbf{r}            }[][ \mathrm{t}            ]  \\[0.5em]
                \indexed{ \mathbf{k}            }[][ \mathrm{t}            ] \\[0.5em]
                \indexed{ \mathbf{l}            }[][ \mathrm{t}            ] \\[0.5em]
            \end{bmatrix} = 
            \begin{bmatrix}
                \indexed{ \mathbf{r}            }[][ \mathrm{t}            -1] + \frac{1}{ m                     } \indexed{ \mathbf{l}            }[][ \mathrm{t}            ] \indexed{ \Delta                }[][ \mathrm{t}            ] \\[0.3em]
                \indexed{ \mathbf{k}            }[][ \mathrm{t}            -1] + \sum\limits_{ \mathrm{e}            \in   \mathrm{e}            _{\mathrm{cnt}} } \indexed{ \kappa                }[][ \mathrm{e}            , \mathrm{t}            ] \indexed{ \Delta                }[][ \mathrm{t}            ] \\[0.6em]
                \indexed{ \mathbf{l}            }[][ \mathrm{t}            -1] +  m                      \mathbf{g}            \indexed{ \Delta                }[][ \mathrm{t}            ] + \sum\limits_{ \mathrm{e}            \in   \mathrm{e}            _{\mathrm{cnt}} } \indexed{ \mathbf{f}            }[][ \mathrm{e}            , \mathrm{t}            ] \indexed{ \Delta                }[][ \mathrm{t}            ] \\[0.0em]
            \end{bmatrix}
        \end{aligned} \hspace{-0.5cm} \label{eq_dynopt_momentum} \\
        &\begin{aligned}
            %
            % Torque at endeffector position
            %
            \mathllap{}
            &\; \indexed{ \kappa                }[][ \mathrm{e}            , \mathrm{t}            ] = (\indexed{ \mathbf{p}            }[][ \mathrm{e}            , \mathrm{t}            ] - \indexed{ \mathbf{r}            }[][ \mathrm{t}            ]) \times \indexed{ \mathbf{f}            }[][ \mathrm{e}            , \mathrm{t}            ] + \indexed{ \gamma                }[][ \mathrm{e}            , \mathrm{t}            ]
        \end{aligned}  \label{eq_dynopt_kappa} \\
        &\begin{aligned}
            %
            % Torque at center of pressure
            %
            \mathllap{}
            &\; \indexed{ \gamma                }[][ \mathrm{e}            , \mathrm{t}            ] = ( \indexed{ \mathbf{R}            }[ \mathrm{x}            , \mathrm{y}            ][ \mathrm{e}            , \mathrm{t}            ] \indexed{ \mathbf{\mathfrak{z}} }[][ \mathrm{e}            , \mathrm{t}            ] )  \times \indexed{ \mathbf{f}            }[][ \mathrm{e}            , \mathrm{t}            ] + \indexed{ \mathbf{R}            }[ \mathrm{z}            ][ \mathrm{e}            , \mathrm{t}            ] \indexed{ \tau                  }[][ \mathrm{e}            , \mathrm{t}            ]
        \end{aligned} \label{eq_dynopt_gamma} \\
        &\begin{aligned}
            %
            % Membership to contact surfaces
            %
            \mathllap{}
            &\; \indexed{ \mathbf{p}            }[][ \mathrm{e}            , \mathrm{t}            ] \in  \pazocal{U}           (\indexed{ \pazocal{S}           }[][ \mathfrak{r}          =  \varphi               ( \mathrm{e}            , \mathrm{t}            )])
        \end{aligned} \label{eq_dynopt_effpos} \\[0.0em]
        &\begin{aligned}
            %
            % Constraints on time discretization variable
            %
            \mathllap{}
            &\; \indexed{ \Delta                }[][ \mathrm{t}            ] \in [ \indexed[min]{ \Delta                }[][ \mathrm{t}            ], \indexed[max]{ \Delta                }[][ \mathrm{t}            ] ]
        \end{aligned} \label{eq_dynopt_time}\\[0.0em]
        &\begin{aligned}
            %
            % Constraints on center of pressure limits
            %
            \mathllap{}
            &\; \indexed{ \mathbf{\mathfrak{z}} }[ \mathrm{x}            , \mathrm{y}            ][ \mathrm{e}            , \mathrm{t}            ] \in [ \indexed[min]{ \mathbf{\mathfrak{z}} }[ \mathrm{x}            , \mathrm{y}            ], \indexed[max]{ \mathbf{\mathfrak{z}} }[ \mathrm{x}            , \mathrm{y}            ] ]
        \end{aligned} \label{eq_dynopt_cop} \\[0.0em]
        &\begin{aligned}
            %
            % Friction cone constraints
            %
            \mathllap{}
            &\; \left\lVert \indexed{ \mathbf{\mathfrak{f}} }[ \mathrm{x}            , \mathrm{y}            ][ \mathrm{e}            , \mathrm{t}            ] \right\rVert_{2} \le  \mu                   \indexed{ \mathbf{\mathfrak{f}} }[ \mathrm{z}            ][ \mathrm{e}            , \mathrm{t}            ], \hspace{0.25cm} \indexed{ \mathbf{\mathfrak{f}} }[ \mathrm{z}            ][ \mathrm{e}            , \mathrm{t}            ] > 0
        \end{aligned} \label{eq_dynopt_frccone} \\
        &\begin{aligned}
            %
            % Heuristic on distance between center of mass and contacts
            %
            \mathllap{}
            &\; \left\lVert\indexed{ \mathbf{p}            }[][ \mathrm{e}            , \mathrm{t}            ] -  \mathbf{r}            _{ \mathrm{t}            }\right\rVert_{2} \le \indexed[max]{\pazocal{L}}[][ \mathrm{e}            ]
        \end{aligned} \label{eq_dynopt_eff_length} \\[0.0em]
        &\begin{aligned}
            %
            % Contraint on torque limits
            %
            \mathllap{}
            &\; \indexed{ \Lambda              }[][ \mathrm{t}            ] = \big( \indexed{ \mathbf{M}           }[a](\indexed[*]{ \mathbf{q}            }) \indexed[*]{ \mathbf{\ddot{q}}     } + \indexed{ \mathbf{h}           }[a](\indexed[*]{ \mathbf{q}            },\indexed[*]{ \mathbf{\dot{q}}      })  \big. \\[0.1cm]
            & \big. \hspace{1.1cm} - \sum_{ \mathrm{e}            \in   \mathrm{e}            _{\mathrm{cnt}} } \indexed{ \mathbf{J}           }[a][ \mathrm{e}            ](\indexed[*]{ \mathbf{q}            })^{T} \indexed{ \lambda              }[][ \mathrm{e}            , \mathrm{t}            ] \big) \; \in [{\indexed[min]{ \Lambda              }},{\indexed[max]{ \Lambda              }}]  \label{eq_dynopt_joint_torques}
        \end{aligned}
    \end{align}
    \label{dynopt_problem}$$

We minimize a quadratic cost [\[eq_dynopt_cost\]](#eq_dynopt_cost){reference-type="eqref" reference="eq_dynopt_cost"} that includes a running cost $\indexed{ \phi                  }[dyn][ \mathrm{t}            ]$ composed by user-defined task costs (such as reaching a CoM position or moving through a way-point) and regularization of control variables (such as contact wrenches or Euler discretization of time $\indexed{ \Delta                }[][ \mathrm{t}            ]$). When the problem is solved in the context of the alternating kino-dynamic optimization procedure, it also includes a consensus cost $\indexed{ \Phi                  }[dyn][ \mathrm{t}            ]$ penalizing momentum trajectories and contact locations deviating from the solution of the kinematic optimization step. The problem is optimized over a discrete time horizon $N                     \approx  \pazocal{T}           / \indexed[0]{ \Delta                }[][ \mathrm{t}            ]$ computed using the initial guess for the timestep variable $\indexed{ \Delta                }[][ \mathrm{t}            ]$, that corresponds to the difference between time at step $\mathrm{t}$ and $\mathrm{t}            -1$.

The constraints (defined for all active endeffectors $\mathrm{e}            \in   \mathrm{e}            _{\mathrm{cnt}}$ and timesteps $\mathrm{t}$) include consistency with the centroidal dynamics [\[eq_dynopt_momentum\]](#eq_dynopt_momentum){reference-type="eqref" reference="eq_dynopt_momentum"}-[\[eq_dynopt_gamma\]](#eq_dynopt_gamma){reference-type="eqref" reference="eq_dynopt_gamma"}. Here, we have formulated the dynamics using torques at each contact's center of pressure and added an extra variable $\indexed{ \kappa                }[][ \mathrm{e}            , \mathrm{t}            ]$ which will facilitate the formulation of the time optimization algorithm. Other constraints include: constraints on the endeffector locations to remain on the assigned contact surface [\[eq_dynopt_effpos\]](#eq_dynopt_effpos){reference-type="eqref" reference="eq_dynopt_effpos"} modeled as linear inequality constraints (cf. Section [4.1](#sec:contact_membership){reference-type="ref" reference="sec:contact_membership"} for a detailed explanation of $\indexed{ \mathbf{p}            }[][ \mathrm{e}            , \mathrm{t}            ] \in  \pazocal{U}           (\indexed{ \pazocal{S}           }[][ \mathfrak{r}          =  \varphi               ( \mathrm{e}            , \mathrm{t}            )])$), box constraints to restrict the timestep variable [\[eq_dynopt_time\]](#eq_dynopt_time){reference-type="eqref" reference="eq_dynopt_time"} between a lower $\indexed[min]{ \Delta                }[][ \mathrm{t}            ]$ and upper $\indexed[max]{ \Delta                }[][ \mathrm{t}            ]$ limits, constraints to maintain the CoP of the endeffectors (assumed to be rectangular) within the support region [\[eq_dynopt_cop\]](#eq_dynopt_cop){reference-type="eqref" reference="eq_dynopt_cop"} defined by the lower $\indexed[min]{ \mathbf{\mathfrak{z}} }[ \mathrm{x}            , \mathrm{y}            ]$ and $\indexed[max]{ \mathbf{\mathfrak{z}} }[ \mathrm{x}            , \mathrm{y}            ]$ upper limits, friction cone constraints [\[eq_dynopt_frccone\]](#eq_dynopt_frccone){reference-type="eqref" reference="eq_dynopt_frccone"} (with friction coefficient $\mu$) and a heuristic constraint to ensure that the contact locations remain reachable expressed as a distance from the CoM [\[eq_dynopt_eff_length\]](#eq_dynopt_eff_length){reference-type="eqref" reference="eq_dynopt_eff_length"} that cannot exceed a predefined value $\indexed[max]{\pazocal{L}}[][ \mathrm{e}            ]$. A linear time-varying approximation of the torque limits constraint [\[eq_dynopt_joint_torques\]](#eq_dynopt_joint_torques){reference-type="eqref" reference="eq_dynopt_joint_torques"} along the motion trajectory $\indexed[*]{ \mathbf{q}            }, \indexed[*]{ \mathbf{\dot{q}}      }, \indexed[*]{ \mathbf{\ddot{q}}     }$ optimized in the previous kinematics optimization problem can also be considered and provides the ability to adapt contact wrenches to satisfy torque limits.

In its general form, the optimization problem defined in Eq. [\[dynopt_problem\]](#dynopt_problem){reference-type="eqref" reference="dynopt_problem"} is non-convex. Its non-convexities are due to the cross products from the angular momentum dynamics and the bilinear terms from the timestep variable. In the next section, we leverage the structure of the problem and propose two algorithms based on convex relaxations to efficiently solve it. We then extend the approach to also optimally select contact surfaces that support a dynamic motion by embedding the dynamics model within a custom mixed-integer solver.

::: remark
**Remark 1**. *In general, we can write down the relation between the contact forces and the CoM motion in two ways, 1) using the contact wrench sum (CWS) at the CoM and imposing contact wrench cone (CWC) constraints [@Caron:2016wt; @Dai:2016hz; @AdiosZMP; @compliant_terrain_adaptation] 2) using the contact forces (or wrench) at each end-effector and imposing directly contact force constraints [@Herzog-2016b; @JustinMomentumOptimization; @winkler18; @TimeOptimization]. In this paper, we use the second approach. The main advantage of this approach is the capability of adapting contact location of the end-effectors. The main caveat is that for more than one end-effector in contact (i.e. $\mathrm{e}            \geq 2$), the number of decision variables (i.e. $6 \times  \mathrm{e}$) is more than the minimal representation of the centroidal wrench (i.e. 6). However, the cross product term between decision variables is inherent in the centroidal dynamics and our approach to dealing with the cross-product (and bilinear terms in general) is also applicable to a CWC formulation.*
:::

# Centroidal Momentum Dynamics Optimization {#sec:opt_movement}

This section presents our approach to solve the centroidal dynamics optimization based on an analytical decomposition of non-convex bilinear expressions as a difference of quadratic functions, whose known curvature is exploited to design efficient iterative convex approximations. In the following, we analyze the nature of nonconvexities of problem [\[dynopt_problem\]](#dynopt_problem){reference-type="eqref" reference="dynopt_problem"}, propose two convex relaxations to approximate them and, detail the optimization procedures and their convergence criteria.

## Bilinear terms as difference of quadratic functions

Some constraints in problem [\[dynopt_problem\]](#dynopt_problem){reference-type="eqref" reference="dynopt_problem"} are affine [\[eq_dynopt_effpos\]](#eq_dynopt_effpos){reference-type="eqref" reference="eq_dynopt_effpos"}-[\[eq_dynopt_cop\]](#eq_dynopt_cop){reference-type="eqref" reference="eq_dynopt_cop"}, [\[eq_dynopt_joint_torques\]](#eq_dynopt_joint_torques){reference-type="eqref" reference="eq_dynopt_joint_torques"} or second-order cones (SOC) [\[eq_dynopt_frccone\]](#eq_dynopt_frccone){reference-type="eqref" reference="eq_dynopt_frccone"}-[\[eq_dynopt_eff_length\]](#eq_dynopt_eff_length){reference-type="eqref" reference="eq_dynopt_eff_length"} and thus convex; others however describe nonconvex constraints such as the momentum dynamics evolution when considering the timestep variable $\indexed{ \Delta                }[][ \mathrm{t}            ]$ as an optimization variable [\[eq_dynopt_momentum\]](#eq_dynopt_momentum){reference-type="eqref" reference="eq_dynopt_momentum"} or torque cross products [\[eq_dynopt_kappa\]](#eq_dynopt_kappa){reference-type="eqref" reference="eq_dynopt_kappa"}-[\[eq_dynopt_gamma\]](#eq_dynopt_gamma){reference-type="eqref" reference="eq_dynopt_gamma"}. Next, we show the common nature of all the nonlinearities and reformulate them in a way amenable to efficient approximations using iterative convex models.

The torque cross product $\ell                  \times  \mathbf{f}$ between a length ($\indexed{ \mathbf{p}            }[][ \mathrm{e}            ] -  \mathbf{r}            )$ in [\[eq_dynopt_kappa\]](#eq_dynopt_kappa){reference-type="eqref" reference="eq_dynopt_kappa"} or $\indexed{ \mathbf{R}            }[ \mathrm{x}            , \mathrm{y}            ][ \mathrm{e}            ] \indexed{ \mathbf{\mathfrak{z}} }[][ \mathrm{e}            ]$ in [\[eq_dynopt_gamma\]](#eq_dynopt_gamma){reference-type="eqref" reference="eq_dynopt_gamma"}) and the force $\indexed{ \mathbf{f}            }[][ \mathrm{e}            , \mathrm{t}            ]$ can be written as $$\begin{align}
    %
    % General product
    %
     \ell                  \times  \mathbf{f}            & =\hspace{-0.1cm}
    %
    \begin{bmatrix}
        \begin{array}{lll}
            \phantom{-}0                          & -\indexed{ \ell                  }[ \mathrm{z}            ]           & \phantom{-}\indexed{ \ell                  }[ \mathrm{y}            ] \\
            \phantom{-}\indexed{ \ell                  }[ \mathrm{z}            ] & \phantom{-}0                          & -\indexed{ \ell                  }[ \mathrm{x}            ]           \\
            -\indexed{ \ell                  }[ \mathrm{y}            ]           & \phantom{-}\indexed{ \ell                  }[ \mathrm{x}            ] & \phantom{-}0
        \end{array}
    \end{bmatrix}
    \begin{bmatrix}
        \indexed{ \mathbf{f}            }[ \mathrm{x}            ] \\ \indexed{ \mathbf{f}            }[ \mathrm{y}            ] \\ \indexed{ \mathbf{f}            }[ \mathrm{z}            ]
    \end{bmatrix} \label{eq_len_cross_force_1} \\
    %
    % Decomposed product
    %
    & =\hspace{-0.1cm} \Bigg[ {
        % ax
        \overbrace{
            \begin{bmatrix}
                -\indexed{ \ell                  }[ \mathrm{z}            ] &\hspace{-0.18cm}  \indexed{ \ell                  }[ \mathrm{y}            ]
            \end{bmatrix}}^{ \indexed{ \mathbf{a}            }[ \mathrm{x}            ] }
        % bx
        \overbrace{
            \begin{bmatrix}
                 \indexed{ \mathbf{f}            }[ \mathrm{y}            ] \\ \indexed{ \mathbf{f}            }[ \mathrm{z}            ]
            \end{bmatrix}}^{ \indexed{ \mathbf{b}            }[ \mathrm{x}            ] },
        % ay
        \overbrace{
            \begin{bmatrix}
                 \indexed{ \ell                  }[ \mathrm{z}            ] &\hspace{-0.18cm} -\indexed{ \ell                  }[ \mathrm{x}            ]
            \end{bmatrix}}^{ \indexed{ \mathbf{a}            }[ \mathrm{y}            ] }
        % by
        \overbrace{
            \begin{bmatrix}
                 \indexed{ \mathbf{f}            }[ \mathrm{x}            ] \\ \indexed{ \mathbf{f}            }[ \mathrm{z}            ]
            \end{bmatrix}}^{ \indexed{ \mathbf{b}            }[ \mathrm{y}            ] },
        % az
        \overbrace{
            \begin{bmatrix}
                -\indexed{ \ell                  }[ \mathrm{y}            ] &\hspace{-0.18cm}  \indexed{ \ell                  }[ \mathrm{x}            ]
            \end{bmatrix}}^{ \indexed{ \mathbf{a}            }[ \mathrm{z}            ] }
        % bz
        \overbrace{
            \begin{bmatrix}
                 \indexed{ \mathbf{f}            }[ \mathrm{x}            ] \\ \indexed{ \mathbf{f}            }[ \mathrm{y}            ]
            \end{bmatrix}}^{ \indexed{ \mathbf{b}            }[ \mathrm{z}            ] }
    } \Bigg] \label{eq_len_cross_force_2}
\end{align}$$ where the superscripts $\mathrm{x}            ,  \mathrm{y}            ,  \mathrm{z}$ reference to the components of the vectors $\ell                  ,  \mathbf{f}            \in  \mathbb{R}            ^{3\times1}$, but then they also identify the vectors $\indexed{ \mathbf{a}            }[ \mathrm{i}            ], \indexed{ \mathbf{b}            }[ \mathrm{i}            ] \in  \mathbb{R}            ^{2\times1}$ for $\mathrm{i}            \in \{  \mathrm{x}            ,  \mathrm{y}            ,  \mathrm{z}            \}$, whose scalar product $\indexed{ \mathbf{a}            }[ \mathrm{i}            ] \cdot \indexed{ \mathbf{b}            }[ \mathrm{i}            ]$ is equivalent to the corresponding element of the cross product vector $( \ell                  \times  \mathbf{f}            )^{ \mathrm{i}            }$. Similarly, we notice that the nonconvexity in [\[eq_dynopt_momentum\]](#eq_dynopt_momentum){reference-type="eqref" reference="eq_dynopt_momentum"} can be written as a scalar product between the timestep variable $\indexed{ \Delta                }[][ \mathrm{t}            ]$ and linear momentum $\indexed{ \mathbf{l}            }[][ \mathrm{t}            ]$, contact forces $\indexed{ \mathbf{f}            }[][ \mathrm{e}            , \mathrm{t}            ]$ and torque $\indexed{ \kappa                }[][ \mathrm{e}            , \mathrm{t}            ]$ variables. It means that all nonconvex constraints solely include equality constraints with bilinear terms.

Noticing that $\indexed{ \mathbf{a}            }[ \mathrm{i}            ] \cdot \indexed{ \mathbf{b}            }[ \mathrm{i}            ] = \frac{1}{4}\left\lVert\indexed{ \mathbf{a}            }[ \mathrm{i}            ] + \indexed{ \mathbf{b}            }[ \mathrm{i}            ]\right\rVert^{2}_{2} - \frac{1}{4}\left\lVert\indexed{ \mathbf{a}            }[ \mathrm{i}            ] - \indexed{ \mathbf{b}            }[ \mathrm{i}            ]\right\rVert^{2}_{2}$, we reformulate all the bilinear expressions as differences of convex quadratic functions with known positive curvature, as was done in [@Herzog-2016b] and in the spirit of [@DBLP:conf/cdc/ShenDGB16]. In other words, we can now decompose a bilinear expression with an indefinite curvature into quadratic terms with known curvature, which is key for the efficiency of our algorithm. To simplify the subsequent presentation, we define the following sets

::: definition
**Definition 1**. *Given a real vector space $V$, we define $\pazocal{Q}^{+}$ as the set of quadratic functions $V                     \rightarrow  \mathbb{R}$ with a positive semi-definite Hessian matrix.*
:::

::: {#def:decomposition .definition}
**Definition 2**. *Given a real vector space $V$, the set $\pazocal{Q}^{\pm}$ is $$\begin{align}
        & \pazocal{Q}^{\pm}     \hspace{-0.025cm}=\hspace{-0.025cm} \bigg\{ \hspace{-0.025cm} \mathfrak{B}          {\cdot} :  V                     \hspace{-0.025cm}\rightarrow\hspace{-0.025cm}  \mathbb{R}            \; | \;  \mathfrak{B}          (\hspace{-0.025cm} \mathbf{u}            \hspace{-0.025cm}) \hspace{-0.025cm}=\hspace{-0.025cm}  \chi                  (\hspace{-0.025cm} \mathbf{u}            \hspace{-0.025cm}) \hspace{-0.025cm}-\hspace{-0.025cm}  \zeta                 (\hspace{-0.025cm} \mathbf{u}            \hspace{-0.025cm}) \textrm{ for }  \chi                  ,  \zeta                 \hspace{-0.025cm}\in\hspace{-0.025cm}  \pazocal{Q}^{+}       \hspace{-0.025cm} \bigg\}
\end{align}$$*
:::

where Figure [4](#fig2:dc_picture){reference-type="ref" reference="fig2:dc_picture"} graphically illustrates this decomposition.

::::: {#fig2:dc_picture .figure}
::: minipage
![](Ponton2020Efficient_figs/Decomp.png){width="100%"}
:::

::: {.caption short-caption=""}
Decomposition (as shown in *Definition* [2](#def:decomposition){reference-type="ref" reference="def:decomposition"}) of the bilinear form $\mathfrak{B}          ( \mathbf{u}            ) =  \mathfrak{B}          ([{\indexed{ \mathbf{u}            }[][1]}^{T},{\indexed{ \mathbf{u}            }[][2]}^{T}]^{T}) = \indexed{ \mathbf{u}            }[][1] \cdot \indexed{ \mathbf{u}            }[][2]$ into a difference of quadratic expressions $\mathfrak{B}          ( \mathbf{u}            ) =  \chi                  ( \mathbf{u}            ) -  \zeta                 ( \mathbf{u}            )$ with $\chi                  ( \mathbf{u}            ) = \frac{1}{4}  \mathfrak{Q}          (\indexed{ \mathbf{u}            }[][1]+\indexed{ \mathbf{u}            }[][2])$ and $\zeta                 ( \mathbf{u}            ) = \frac{1}{4} \mathfrak{Q}          (\indexed{ \mathbf{u}            }[][1]-\indexed{ \mathbf{u}            }[][2])$, where $\mathfrak{Q}          (\cdot)$ is the quadratic function $\left\lVert\cdot\right\rVert^{2}_{2}$.
:::
:::::

In particular, the set $\pazocal{Q}^{\pm}$ is closed under scalar multiplication, addition and composition with affine functions, $$\begin{align}
    \alpha (\mathbf{\bar{v}} \circ \mathbf{v}) + \beta (\mathbf{\bar{w}} \circ \mathbf{w}) \in  \pazocal{Q}^{\pm}     \quad
%   \begin{matrix} \ctxt{\forall \mathbf{\bar{v}}(\cdot), \mathbf{\bar{w}}(\cdot)} \in \setpm;\\
%   \mathbf{v}(\cdot), \mathbf{w}(\cdot) \in \pazocal{A}; \quad \ctxt{\alpha}, \beta \in \setreals \end{matrix}
\end{align}$$ for any $\alpha, \beta \in  \mathbb{R}$, affine functions $\mathbf{v}(\cdot),\mathbf{w}(\cdot)$ and $\mathbf{\bar{v}}(\cdot), \mathbf{\bar{w}}(\cdot) \in  \pazocal{Q}^{\pm}$. Consider for example Equation [\[eq_dynopt_gamma\]](#eq_dynopt_gamma){reference-type="eqref" reference="eq_dynopt_gamma"} and assume for simplicity that $(\indexed{ \mathbf{R}            }[ \mathrm{x}            , \mathrm{y}            ][ \mathrm{e}            , \mathrm{t}            ]   \indexed{ \mathbf{\mathfrak{z}} }[][ \mathrm{e}            , \mathrm{t}            ]) \times \indexed{ \mathbf{f}            }[][ \mathrm{e}            , \mathrm{t}            ]$ is represented by the decomposition $\ell                  \times  \mathbf{f}$, then each endeffector torque component becomes $\indexed{ \gamma                }[ \mathrm{i}            ][ \mathrm{e}            , \mathrm{t}            ] = \indexed{ \mathbf{a}            }[ \mathrm{i}            ] \cdot \indexed{ \mathbf{b}            }[ \mathrm{i}            ] + ( \indexed{ \mathbf{R}            }[ \mathrm{z}            ][ \mathrm{e}            , \mathrm{t}            ] \indexed{ \tau                  }[][ \mathrm{e}            , \mathrm{t}            ] )^{ \mathrm{i}            }$. The torque component $\indexed{ \tau                  }[][ \mathrm{e}            , \mathrm{t}            ]$ could also be formulated as a difference of positive components $\indexed{ \tau                  } = \indexed[+]{ \tau                  } - \indexed[-]{ \tau                  }, \textrm{ where } \indexed[+]{ \tau                  },\indexed[-]{ \tau                  } \ge 0$, as in [@DBLP:conf/wafr/PosaT12] to embed them into the decomposition; however, this is not required. Then $$\begin{equation}
\indexed{ \gamma                }[ \mathrm{i}            ][ \mathrm{e}            , \mathrm{t}            ] =
\overbrace{
    %
    % Positive term of endeffector torque decomposition
    %
    \underbrace{\left[
        \frac{1}{4} \left\lVert\indexed{ \mathbf{a}            }[ \mathrm{i}            ] + \indexed{ \mathbf{b}            }[ \mathrm{i}            ]\right\rVert^{2}_{2}
        \right]}_{\in  \pazocal{Q}^{+}       }
    -
    %
    % Negative term of endeffector torque decomposition
    %
    \underbrace{ \left[
        \frac{1}{4} \left\lVert\indexed{ \mathbf{a}            }[ \mathrm{i}            ] - \indexed{ \mathbf{b}            }[ \mathrm{i}            ]\right\rVert^{2}_{2}
        \right] }_{\in  \pazocal{Q}^{+}       }
}^{\in  \pazocal{Q}^{\pm}     }
    %
    % Rotational part
    %
    + (\indexed{ \mathbf{R}            }[ \mathrm{z}            ][ \mathrm{e}            , \mathrm{t}            ])^{ \mathrm{i}            } \indexed[]{ \tau                  }[][ \mathrm{e}            , \mathrm{t}            ]
\label{eq_gamma_decomposition}
\end{equation}$$ In a similar manner, each endeffector torque component $\indexed{ \kappa                }[ \mathrm{i}            ][ \mathrm{e}            , \mathrm{t}            ]$ [\[eq_dynopt_kappa\]](#eq_dynopt_kappa){reference-type="eqref" reference="eq_dynopt_kappa"}, can be decomposed parameterizing its cross product $(\indexed{ \mathbf{p}            }[][ \mathrm{e}            ] -  \mathbf{r}            ) \times \indexed{ \mathbf{f}            }[][ \mathrm{e}            ]$ with vectors $\indexed{ \mathbf{c}            }[ \mathrm{i}            ]$ and $\indexed{ \mathbf{d}            }[ \mathrm{i}            ]$ as $\indexed{ \kappa                }[ \mathrm{i}            ][ \mathrm{e}            , \mathrm{t}            ] = \indexed{ \mathbf{c}            }[ \mathrm{i}            ] \cdot \indexed{ \mathbf{d}            }[ \mathrm{i}            ] + \indexed{ \gamma                }[ \mathrm{i}            ][ \mathrm{e}            , \mathrm{t}            ]$. $$\begin{equation}
\indexed{ \kappa                }[ \mathrm{i}            ][ \mathrm{e}            , \mathrm{t}            ] =
\overbrace{
    \overbrace{
        %
        % Positive term of endeffector torque decomposition
        %
        \underbrace{\left[
            \frac{1}{4} \left\lVert\indexed{ \mathbf{c}            }[ \mathrm{i}            ] + \indexed{ \mathbf{d}            }[ \mathrm{i}            ]\right\rVert^{2}_{2}
            \right]}_{\in  \pazocal{Q}^{+}       }
        -
        %
        % Negative term of endeffector torque decomposition
        %
        \underbrace{ \left[
            \frac{1}{4} \left\lVert\indexed{ \mathbf{c}            }[ \mathrm{i}            ] - \indexed{ \mathbf{d}            }[ \mathrm{i}            ]\right\rVert^{2}_{2}
            \right] }_{\in  \pazocal{Q}^{+}       }
    }^{\in  \pazocal{Q}^{\pm}     } +
    \overbrace{ \indexed{ \gamma                }[ \mathrm{i}            ][ \mathrm{e}            , \mathrm{t}            ] }^{\in  \pazocal{Q}^{\pm}     }
}^{\in  \pazocal{Q}^{\pm}     }
\label{eq_kappa_decomposition}
\end{equation}$$ where the vectors $\indexed{ \mathbf{c}            }[ \mathrm{i}            ], \indexed{ \mathbf{d}            }[ \mathrm{i}            ] \in  \mathbb{R}            ^{2\times1}$ for $\mathrm{i}            \in \{  \mathrm{x}            ,  \mathrm{y}            ,  \mathrm{z}            \}$ have been introduced in a similar fashion to Eq. [\[eq_len_cross_force_2\]](#eq_len_cross_force_2){reference-type="eqref" reference="eq_len_cross_force_2"} to refer to the vectors whose scalar product $\indexed{ \mathbf{c}            }[ \mathrm{i}            ] \cdot \indexed{ \mathbf{d}            }[ \mathrm{i}            ]$ is equivalent to the corresponding component of the cross product $((\indexed{ \mathbf{p}            }[][ \mathrm{e}            ] -  \mathbf{r}            ) \times \indexed{ \mathbf{f}            }[][ \mathrm{e}            ])^{ \mathrm{i}            }$. A similar analysis holds for each of the Cartesian components of the bilinear expressions within the dynamic constraints [\[eq_dynopt_momentum\]](#eq_dynopt_momentum){reference-type="eqref" reference="eq_dynopt_momentum"}, which can be decomposed into elements of $\pazocal{Q}^{\pm}$ as given by $$\begin{align}
        %
        % linear momentum
        %
        \indexed{ \mathbf{l}            }[ \mathrm{i}            ][ \mathrm{t}            ] \indexed{ \Delta                }[][ \mathrm{t}            ] =&
         \frac{1}{4} \left\lVert\indexed{ \mathbf{l}            }[ \mathrm{i}            ][ \mathrm{t}            ] + \indexed{ \Delta                }[][ \mathrm{t}            ]\right\rVert^{2}_{2}
        -\frac{1}{4} \left\lVert\indexed{ \mathbf{l}            }[ \mathrm{i}            ][ \mathrm{t}            ] - \indexed{ \Delta                }[][ \mathrm{t}            ]\right\rVert^{2}_{2} \\
        %
        % wrenches
        %
        \sum_{ \mathrm{e}            \in   \mathrm{e}            _{\mathrm{cnt}} } \hspace{-0.15cm}\indexed{ \kappa                }[ \mathrm{i}            ][ \mathrm{e}            , \mathrm{t}            ] \indexed{ \Delta                }[][ \mathrm{t}            ] =&
        \frac{1}{4} \left\lVert \sum_{ \mathrm{e}            \in   \mathrm{e}            _{\mathrm{cnt}} } \hspace{-0.15cm}\indexed{ \kappa                }[ \mathrm{i}            ][ \mathrm{e}            , \mathrm{t}            ] + \indexed{ \Delta                }[][ \mathrm{t}            ]\right\rVert^{2}_{2}
        -\frac{1}{4} \left\lVert \sum_{ \mathrm{e}            \in   \mathrm{e}            _{\mathrm{cnt}} } \hspace{-0.15cm}\indexed{ \kappa                }[ \mathrm{i}            ][ \mathrm{e}            , \mathrm{t}            ] - \indexed{ \Delta                }[][ \mathrm{t}            ]\right\rVert^{2}_{2} \\
        %
        % forces
        %
        \sum_{ \mathrm{e}            \in   \mathrm{e}            _{\mathrm{cnt}} } \hspace{-0.15cm}\indexed{ \mathbf{f}            }[ \mathrm{i}            ][ \mathrm{e}            , \mathrm{t}            ] \indexed{ \Delta                }[][ \mathrm{t}            ] =&
        \frac{1}{4} \left\lVert \sum_{ \mathrm{e}            \in   \mathrm{e}            _{\mathrm{cnt}} } \hspace{-0.15cm}\indexed{ \mathbf{f}            }[ \mathrm{i}            ][ \mathrm{e}            , \mathrm{t}            ] + \indexed{ \Delta                }[][ \mathrm{t}            ]\right\rVert^{2}_{2}
        -\frac{1}{4} \left\lVert \sum_{ \mathrm{e}            \in   \mathrm{e}            _{\mathrm{cnt}} } \hspace{-0.15cm}\indexed{ \mathbf{f}            }[ \mathrm{i}            ][ \mathrm{e}            , \mathrm{t}            ] - \indexed{ \Delta                }[][ \mathrm{t}            ]\right\rVert^{2}_{2}
    \end{align}
    \label{eq_dc_dynamics}$$ In the next section, we show how we can use this structure to approximate the problem using iterative convex relaxations.

## Optimization with iterative convex relaxations {#subsubsec:iterative_methods}

We now use the known curvature of the quadratic terms $\pazocal{Q}^{+}$ to build a convex approximation. We start by isolating the quadratic expressions into quadratic constraints by introducing scalar variables $\indexed{ \bar{a}               }[ \mathrm{i}            ], \indexed{ \bar{b}               }[ \mathrm{i}            ] \in  \mathbb{R}$. For example, Eq. [\[eq_gamma_decomposition\]](#eq_gamma_decomposition){reference-type="eqref" reference="eq_gamma_decomposition"} would become $$\begin{align}
        %
        % Quadratic equalities
        %
        &\indexed{ \bar{a}               }[ \mathrm{i}            ] = \left\lVert\indexed{ \mathbf{a}            }[ \mathrm{i}            ] + \indexed{ \mathbf{b}            }[ \mathrm{i}            ]\right\rVert^{2}_{2} \; ,  \quad \indexed{ \bar{b}               }[ \mathrm{i}            ] = \left\lVert\indexed{ \mathbf{a}            }[ \mathrm{i}            ] - \indexed{ \mathbf{b}            }[ \mathrm{i}            ]\right\rVert^{2}_{2} \label{eq_chg_variables} \\
        %
        % Additional linear constraints
        %
        &\quad\indexed{ \gamma                }[ \mathrm{i}            ][ \mathrm{e}            , \mathrm{t}            ] =
            \frac{1}{4} \left(
             \indexed{ \bar{a}               }[ \mathrm{i}            ] - \indexed{ \bar{b}               }[ \mathrm{i}            ]
            \right)
            + (\indexed{ \mathbf{R}            }[ \mathrm{z}            ][ \mathrm{e}            , \mathrm{t}            ])^{ \mathrm{i}            } \indexed[]{ \tau                  }[][ \mathrm{e}            , \mathrm{t}            ]
            \label{eq_linear_part}
    \end{align}$$ where the introduction of the additional scalar variables $\indexed{ \bar{a}               }[ \mathrm{i}            ], \indexed{ \bar{b}               }[ \mathrm{i}            ]$ renders the original equation [\[eq_linear_part\]](#eq_linear_part){reference-type="eqref" reference="eq_linear_part"} linear and isolates the quadratic nonconvex expressions with known curvature into a pair of additional quadratic constraints [\[eq_chg_variables\]](#eq_chg_variables){reference-type="eqref" reference="eq_chg_variables"}, whose very simple form will benefit the search of efficient convex approximations.

:::: {#fig3:quadractic_equality_constraint .figure}
:::: {#fig3:soft_constraint_approx .figure}
![](Ponton2020Efficient_figs/DecompositionPica.png){width="90%"}

![](Ponton2020Efficient_figs/DecompositionPicb.png){width="90%"}

![](Ponton2020Efficient_figs/DecompositionPicc.png){width="90%"}

::: {.caption short-caption=""}
Soft-constraint method: We first find a solution within the convex space $\mathfrak{Q}          ( \mathfrak{p}          ) \leq \indexed{ \bar{a}               }[ \mathrm{i}            ]$ and based on this solution, we iteratively build a function underestimator, that allows us to include a cost that rewards selecting values close to it and thus close to the constraint boundary. Parameter $\eta$ controls the desirability of selecting solutions close to the underestimator of the convex quadratic inequality constraint.
:::
::::

::: {.caption short-caption=""}
Sequential approximation of quadratic expressions $\pazocal{Q}^{+}$ within its convex space using iterative convex relaxation methods.
:::
::::

Figure [\[fig3:intersection_approx\]](#fig3:intersection_approx){reference-type="ref" reference="fig3:intersection_approx"} sketches the hyperplane defined by the nonconvex constraint [\[eq_chg_variables\]](#eq_chg_variables){reference-type="eqref" reference="eq_chg_variables"}, conceived as the intersection of two inequalities, a convex $\indexed{ \bar{a}               }[ \mathrm{i}            ] \geq \left\lVert\indexed{ \mathbf{a}            }[ \mathrm{i}            ] + \indexed{ \mathbf{b}            }[ \mathrm{i}            ]\right\rVert^{2}_{2}$ and a concave one $\indexed{ \bar{a}               }[ \mathrm{i}            ] \leq \left\lVert\indexed{ \mathbf{a}            }[ \mathrm{i}            ] + \indexed{ \mathbf{b}            }[ \mathrm{i}            ]\right\rVert^{2}_{2}$. While it is difficult to search a solution in a high dimensional nonconvex space, it is easier to search within the space defined by the convex inequality and guide the optimization towards the constraint boundary, approaching in this way towards solutions with practical feasibility for the original nonconvex quadratic equality constraint.

To summarize, we systematically isolate all the quadratic expressions present in the optimization problem and replace them with new scalar optimization variables in order to render the original constraints linear. We then add simple equality constraints between the new variables and the quadratic terms. This allows us to move all the nonconvex elements of the problem into simpler terms in the form of quadratic equality constraints. We now propose two iterative methods based on SOC programs to deal with each of the quadratic equalities.

### Trust-region method

In this approach the main idea is to use a primal constraint to limit the convex search space to values close to the boundaries. In mathematical terms, the trust-region should constrain the problem to values of $\indexed{ \bar{a}               }[ \mathrm{i}            ]$ near $\mathfrak{Q}          ( \mathfrak{p}          )$ (for simplicity of notation, we define $\mathfrak{p}          = \indexed{ \mathbf{a}            }[ \mathrm{i}            ] + \indexed{ \mathbf{b}            }[ \mathrm{i}            ]$ and $\mathfrak{Q}          (\cdot) = \left\lVert\cdot\right\rVert^{2}_{2}$). During the first iteration, an initial guess of the optimal problem values is obtained by searching over the entire relaxed convex search space. From there on, the trust-region is built based on the optimal problem values from the previous iteration $\indexed[*]{ \mathfrak{p}          }$ and by reducing the desired allowed amount of constraint violation $\sigma$, as shown in Figure [\[fig3:trust_region_approx\]](#fig3:trust_region_approx){reference-type="ref" reference="fig3:trust_region_approx"}.

::: mytheorem1*
In the case of $\pazocal{Q}^{+}$ expressions, thanks to the positive curvature of the constraint's hessian, a linear inequality constraint suffices to constrain the problem as desired. $$\begin{equation}
        \hspace{-0.05cm} \mathfrak{Q}          ( \mathfrak{p}          ) \hspace{-0.05cm}=\hspace{-0.05cm} \indexed{ \bar{a}               }[ \mathrm{i}            ] \hspace{-0.05cm}\rightarrow\hspace{-0.075cm}
        \begin{cases}
            \hspace{-0.025cm} \mathfrak{Q}          (\indexed[*]{ \mathfrak{p}          }\hspace{-0.025cm}) \hspace{-0.025cm}+\hspace{-0.05cm} \nabla  \mathfrak{Q}          (\hspace{-0.025cm} \mathfrak{p}          \hspace{-0.025cm}) |_{\indexed[*]{ \mathfrak{p}          }} \hspace{-0.025cm}\cdot\hspace{-0.025cm} ( \mathfrak{p}          \hspace{-0.025cm}-\hspace{-0.05cm} \indexed[*]{ \mathfrak{p}          } \hspace{-0.025cm}) \hspace{-0.025cm}+\hspace{-0.05cm}  \sigma                \hspace{-0.05cm}\geq\hspace{-0.025cm} \indexed{ \bar{a}               }[ \mathrm{i}            ]
        \end{cases}
\end{equation}$$ The linear constraint is built based on the optimal values of $\mathfrak{p}$ found in the previous iteration $\indexed[*]{ \mathfrak{p}          }$ and $\sigma$ is a positive threshold, big enough to provide a feasible interior to the intersection of the constraints, but also small enough so as to achieve the desired precision at convergence.
:::

The benefits of constraining the problem in this way are twofold: firstly, we can easily refine the solution with values of $\mathfrak{p}$ around $\indexed[*]{ \mathfrak{p}          }$ that satisfy the amount of desired constraint violation $\sigma$, and secondly, it provides a method to iteratively increase the approximation accuracy by reducing the value of $\sigma$, as required by convergence tolerances. We further note that if the hessian of this constraint were an indefinite matrix, this trust-region would lead to unbounded regions instead of constraining the problem as desired.

### Soft-constraint method

Alternatively, a hard restriction of the search space could be replaced with a cost that biases the optimizer towards finding solutions close to the boundary of the constraint by pulling optimization variables towards a function underestimator, as shown in Figure [5](#fig3:soft_constraint_approx){reference-type="ref" reference="fig3:soft_constraint_approx"}.

::: mytheorem2*
A cost heuristic is used to reward the selection of values for the variable $\indexed{ \bar{a}               }[ \mathrm{i}            ]$ close to the function underestimator ($\mathfrak{Q}          (\indexed[*]{ \mathfrak{p}          }) + \nabla  \mathfrak{Q}          ( \mathfrak{p}          ) |_{\indexed[*]{ \mathfrak{p}          }} \cdot ( \mathfrak{p}          - \indexed[*]{ \mathfrak{p}          })$), hyperplane that supports the function and was built based the optimal values of $\mathfrak{p}$ found in the previous iteration $\indexed[*]{ \mathfrak{p}          }$. $$\begin{equation}
         \mathfrak{Q}          ( \mathfrak{p}          ) \hspace{-0.05cm}=\hspace{-0.05cm} \indexed{ \bar{a}               }[ \mathrm{i}            ] \hspace{-0.05cm}\rightarrow\hspace{-0.05cm}
        \begin{cases}
             \mathfrak{Q}          ( \mathfrak{p}          ) \leq \indexed{ \bar{a}               }[ \mathrm{i}            ] \\
             \eta                  \hspace{-0.025cm}\left\lVert 
                 \mathfrak{Q}          (\hspace{-0.025cm}\indexed[*]{ \mathfrak{p}          }\hspace{-0.025cm}) \hspace{-0.05cm}+\hspace{-0.05cm} \nabla \hspace{-0.025cm}  \mathfrak{Q}          (\hspace{-0.025cm} \mathfrak{p}          \hspace{-0.025cm}) \hspace{-0.025cm}|\hspace{-0.025cm}_{\indexed[*]{ \mathfrak{p}          }} \hspace{-0.05cm}\cdot\hspace{-0.05cm} ( \mathfrak{p}          \hspace{-0.05cm}-\hspace{-0.075cm} \indexed[*]{ \mathfrak{p}          }\hspace{-0.025cm}) \hspace{-0.05cm}-\hspace{-0.05cm} \indexed{ \bar{a}               }[ \mathrm{i}            ] \hspace{-0.025cm}
            \right\rVert^{2}_{2}
        \end{cases}
\end{equation}$$ $\eta$ defines the desirability of selecting optimization values close to the underestimator, and thus enjoy practical feasibility for the nonconvex constraint.
:::

::: remark
**Remark 2**. *As shown in Fig. [6](#fig3:quadractic_equality_constraint){reference-type="ref" reference="fig3:quadractic_equality_constraint"}, both methods iteratively approximate the problem as SOC programs, efficiently solvable with polynomial-time methods. In section sec. [6.2](#exp:approximation_limitations){reference-type="ref" reference="exp:approximation_limitations"}, we will further discuss and compare the described methods.*
:::

## Numerical optimization

In this section, we describe numerical aspects such as convergence criteria and algorithmic implementation details for both optimization problems.

### Convergence criteria

The amount of constraint violation $\epsilon$ is used as the measure to decide upon convergence. It is defined as the supremum among the average errors of the state trajectory variables [\[eq_error\]](#eq_error){reference-type="eqref" reference="eq_error"}, which are computed by comparing the values of the optimization variables ($\indexed{ \mathbf{r}            }[][ \mathrm{t}            ]$, $\indexed{ \mathbf{l}            }[][ \mathrm{t}            ]$, $\indexed{ \mathbf{k}            }[][ \mathrm{t}            ]$) that solve the approximate problem and the values obtained by integrating endeffector wrenches ($\indexed[seq]{ \mathbf{r}            }[][ \mathrm{t}            ]$, $\indexed[seq]{ \mathbf{l}            }[][ \mathrm{t}            ]$, $\indexed[seq]{ \mathbf{k}            }[][ \mathrm{t}            ]$) that satisfy exactly all of the nonconvex constraints, as follows $$\begin{align}
    %
    % Linear momentum in sequential form
    %
    & \indexed[seq]{ \mathbf{l}            }[][ \mathrm{t}            ] \hspace{-0.05cm}=\hspace{-0.05cm} \indexed{ \mathbf{l}            }[][0] \hspace{-0.025cm}+\hspace{-0.025cm} \sum_{\mathrm{ \mathrm{i}            =1}}^{ \mathrm{t}            }\hspace{-0.05cm} \left[  m                      \mathbf{g}            + \sum\limits_{ \mathrm{e}            \in   \mathrm{e}            _{\mathrm{cnt}} }\hspace{-0.075cm} \indexed{ \mathbf{f}            }[][ \mathrm{e}            , \mathrm{i}            ] \right] \indexed{ \Delta                }[][ \mathrm{i}            ] \\
    %
    % Center of mass in sequential form
    %
    & \indexed[seq]{ \mathbf{r}            }[][ \mathrm{t}            ] \hspace{-0.05cm}=\hspace{-0.05cm} \indexed{ \mathbf{r}            }[][0] \hspace{-0.025cm}+\hspace{-0.025cm} \frac{1}{ m                     } \sum_{\mathrm{ \mathrm{j}            =1}}^{ \mathrm{t}            }\hspace{-0.05cm} \left[ \indexed{ \mathbf{l}            }[][0] + \sum_{\mathrm{ \mathrm{i}            =1}}^{ \mathrm{j}            }\hspace{-0.05cm} \left(  m                      \mathbf{g}            + \sum\limits_{ \mathrm{e}            \in   \mathrm{e}            _{\mathrm{cnt}} }\hspace{-0.075cm} \indexed{ \mathbf{f}            }[][ \mathrm{e}            , \mathrm{i}            ] \right) \indexed{ \Delta                }[][ \mathrm{i}            ] \right] \indexed{ \Delta                }[][ \mathrm{j}            ] \\
    %
    % Angular momentum in sequential form
    %
    & \indexed[seq]{ \mathbf{k}            }[][ \mathrm{t}            ] \hspace{-0.05cm}=\hspace{-0.075cm} \indexed{ \mathbf{k}            }[][0] \hspace{-0.05cm}+\hspace{-0.075cm} \sum_{\mathrm{ \mathrm{i}            =1}}^{ \mathrm{t}            }\hspace{-0.1cm} \left[ \hspace{-0.05cm} \sum\limits_{ \mathrm{e}            \in   \mathrm{e}            _{\mathrm{cnt}} }\hspace{-0.175cm} (\indexed{ \mathbf{p}            }[][ \mathrm{e}            , \mathrm{i}            ] \hspace{-0.05cm}+\hspace{-0.05cm} \indexed{ \mathbf{R}            }[ \mathrm{x}            , \mathrm{y}            ][ \mathrm{e}            , \mathrm{i}            ] \hspace{-0.025cm}\indexed{ \mathbf{\mathfrak{z}} }[][ \mathrm{e}            , \mathrm{i}            ] \hspace{-0.075cm}-\hspace{-0.1cm} \indexed[seq]{ \mathbf{r}            }[][ \mathrm{i}            ]) \hspace{-0.075cm}\times\hspace{-0.075cm} \indexed{ \mathbf{f}            }[][ \mathrm{e}            , \mathrm{i}            ] \hspace{-0.05cm}+\hspace{-0.05cm} \indexed{ \mathbf{R}            }[ \mathrm{z}            ][ \mathrm{e}            , \mathrm{i}            ] \hspace{-0.025cm} \indexed{ \tau                  }[][ \mathrm{e}            , \mathrm{i}            ] \hspace{-0.05cm}\right] \hspace{-0.1cm}\indexed{ \Delta                }[][ \mathrm{i}            ] \\
    %
    % Maximum convergence error
    %
    &  \epsilon              \hspace{-0.05cm}=\hspace{-0.05cm} \sup \Bigg\{
    \underbrace{\sum_{ \mathrm{t}            =1}^{ N                     } \frac{\left\lVert  \mathbf{r}            _{ \mathrm{t}            }  - \indexed[seq]{ \mathbf{r}            }[][ \mathrm{t}            ] \right\rVert^{2}_{2}}{ N                     }}_{\indexed{ \epsilon              }[][ \mathbf{r}            ]},
    \underbrace{\sum_{ \mathrm{t}            =1}^{ N                     } \frac{\left\lVert  \mathbf{l}            _{ \mathrm{t}            } - \indexed[seq]{ \mathbf{l}            }[][ \mathrm{t}            ] \right\rVert^{2}_{2}}{ N                     }}_{\indexed{ \epsilon              }[][ \mathbf{l}            ]},
    \underbrace{\sum_{ \mathrm{t}            =1}^{ N                     } \frac{\left\lVert  \mathbf{k}            _{ \mathrm{t}            } - \indexed[seq]{ \mathbf{k}            }[][ \mathrm{t}            ] \right\rVert^{2}_{2}}{ N                     }}_{\indexed{ \epsilon              }[][ \mathbf{k}            ]} \Bigg\} \label{eq_error}
    %
\end{align}$$

When the errors $\epsilon$ fall below a certain threshold for the constraint violation to be considered negligible for practical purposes, we consider that the algorithm has converged.

### Algorithmic implementation details

To approximate the solution of problem [\[dynopt_problem\]](#dynopt_problem){reference-type="eqref" reference="dynopt_problem"}, we iteratively solve an approximate problem (using an interior point solver for SOC programs based on [@Domahidi2013ecos]), where each nonconvex constraint [\[eq_dynopt_momentum\]](#eq_dynopt_momentum){reference-type="eqref" reference="eq_dynopt_momentum"}-[\[eq_dynopt_gamma\]](#eq_dynopt_gamma){reference-type="eqref" reference="eq_dynopt_gamma"} has been replaced by a convex approximation. At each iteration, we update the approximation (based on the optimal values of the previous iteration) and its parameters to reduce the constraint violation amount. The procedure is then repeated until convergence. For the trust-region method, the parameter $\sigma$ is decreased using iteratively increasing powers of a value less than one, i.e. $\sigma                \propto {{\nu}^k}$, where ${\nu}<1.0$ and ${k}$ denotes the iteration number. In a similar fashion, for the soft-constraint method, a value for the penalty parameter $\eta$ is selected according to the desired precision to be achieved (typically within the range $[1e4, 1e6]$) and higher relative to other objectives, so that it is prioritized.

We also highlight that the formulation of torques $\indexed{ \gamma                }[][ \mathrm{e}            , \mathrm{t}            ]$ in Eq. [\[eq_dynopt_gamma\]](#eq_dynopt_gamma){reference-type="eqref" reference="eq_dynopt_gamma"} separately of $\indexed{ \kappa                }[][ \mathrm{e}            , \mathrm{t}            ]$ in Eq. [\[eq_dynopt_kappa\]](#eq_dynopt_kappa){reference-type="eqref" reference="eq_dynopt_kappa"} is required only when the torque limits constraint [\[eq_dynopt_joint_torques\]](#eq_dynopt_joint_torques){reference-type="eqref" reference="eq_dynopt_joint_torques"} is used, as it depends on the contact wrench $\indexed{ \lambda              }[][ \mathrm{e}            , \mathrm{t}            ] = \begin{bmatrix} { \mathbf{f}            }^{T}_{ \mathrm{e}            , \mathrm{t}            } & \hspace{-0.2cm} { \gamma                }^{T}_{ \mathrm{e}            , \mathrm{t}            } \end{bmatrix}^{T}$. Otherwise, the torques $\indexed{ \gamma                }[][ \mathrm{e}            , \mathrm{t}            ]$ in Eq. [\[eq_dynopt_gamma\]](#eq_dynopt_gamma){reference-type="eqref" reference="eq_dynopt_gamma"} can be directly embedded within the torque $\indexed{ \kappa                }[][ \mathrm{e}            , \mathrm{t}            ]$ in Eq. [\[eq_dynopt_kappa\]](#eq_dynopt_kappa){reference-type="eqref" reference="eq_dynopt_kappa"}, thus generating a problem of smaller size.

# Optimization of contact plans {#sec:contacts_planning}

In this section, we explain how contact locations can be optimized within problem [\[dynopt_problem\]](#dynopt_problem){reference-type="eqref" reference="dynopt_problem"} when they are considered optimization variables that belong to a given contact surface. We also describe an algorithm based on mixed-integer programming to efficiently select a sequence of terrain surfaces and contact locations consistent with the centroidal dynamics.

## Membership of contact locations to terrain surfaces {#sec:contact_membership}

![The description of a terrain surface ${\indexed{ \pazocal{S}           }[][ \mathfrak{r}          ]}$ comprises a set of coplanar corners ${\indexed{ \omega                }[ \mathrm{i}            ][ \mathfrak{r}          ] \in  \mathbb{R}            ^{3\times1}}$, where in this case $\mathrm{i}            \in [1,4]$. Out of them the following quantities can be computed: surface normal ${\indexed{ \mathfrak{N}          }[][ \mathfrak{r}          ] \in  \mathbb{R}            ^{3\times1}}$, surface rotation $\mathfrak{R}          (\indexed{ \pazocal{S}           }[][ \mathfrak{r}          ]) \in  \mathbb{R}            ^{3\times3}$ (whose third column points in the direction of the surface normal), any surface point ${\indexed[surf]{ \omega                }[][ \mathfrak{r}          ] = \indexed{ \omega                }[ \mathrm{i}            ][ \mathfrak{r}          ]}$ and a membership constraint ${\bar{ \omega                } \in  \pazocal{U}           (\indexed{ \pazocal{S}           }[][ \mathfrak{r}          ]), \forall \bar{ \omega                } \in \indexed{ \pazocal{S}           }[][ \mathfrak{r}          ]}$, that simply defines the set of points ${\bar{ \omega                } \in  \mathbb{R}            ^{3\times1}}$ that lie on the terrain surface.](figures/surfnotation/CntSurfNotation.pdf){#fig4:contact_surface width="22%"}

Given a description of the terrain surface $\indexed{ \pazocal{S}           }[][ \mathfrak{r}          ]$ (over which it is safe to make contact), a contact location can be optimized by including its membership constraint to surface $\indexed{ \pazocal{S}           }[][ \mathfrak{r}          ]$ to the optimization problem. A terrain surface $\indexed{ \pazocal{S}           }[][ \mathfrak{r}          ]$ (as defined in Fig. [7](#fig4:contact_surface){reference-type="ref" reference="fig4:contact_surface"}) is such that any contact point $\indexed{ \mathbf{p}            }[][ \mathrm{e}            ]$, selected from its interior, guarantees that the entire endeffector is in contact. The expression $\indexed{ \mathbf{p}            }[][ \mathrm{e}            ] \in { \pazocal{U}           (\indexed{ \pazocal{S}           }[][ \mathfrak{r}          ])}$ that constrains an endeffector position $\indexed{ \mathbf{p}            }[][ \mathrm{e}            ]$ to belong to surface $\indexed{ \pazocal{S}           }[][ \mathfrak{r}          ]$ is defined as follows $$\begin{equation}
    \indexed{ \mathbf{p}            }[][ \mathrm{e}            ] \in { \pazocal{U}           (\indexed{ \pazocal{S}           }[][ \mathfrak{r}          ])} {\hspace{0.2cm}\stackrel{\mathclap{\normalfont\mbox{def}}}{=}\hspace{0.2cm}}
    %
    % Left hand side membership constraint
    %
    \begin{bmatrix}
        \begin{array}{r}
            {\indexed{ \Xi                   }[][ \mathfrak{r}          ]} \\
            {\indexed{ \mathfrak{N}          }[][ \mathfrak{r}          ]} \\
            -{\indexed{ \mathfrak{N}          }[][ \mathfrak{r}          ]}
        \end{array}
    \end{bmatrix} \indexed{ \mathbf{p}            }[][ \mathrm{e}            ] \leq
    %
    % Right hand side membership constraint
    %
    \begin{bmatrix}
        \begin{array}{r}
            {\indexed{ \xi                   }[][ \mathfrak{r}          ]} \\
            {\indexed{ \mathfrak{N}          }[][ \mathfrak{r}          ] \cdot \indexed[surf]{ \omega                }[][ \mathfrak{r}          ]} \\
            -{\indexed{ \mathfrak{N}          }[][ \mathfrak{r}          ] \cdot \indexed[surf]{ \omega                }[][ \mathfrak{r}          ]}
        \end{array}
    \end{bmatrix}
    \label{eq_belonging_to_surface}
\end{equation}$$ Equation [\[eq_belonging_to_surface\]](#eq_belonging_to_surface){reference-type="eqref" reference="eq_belonging_to_surface"} defines a set of halfspaces, whose intersection constrains a contact point $\indexed{ \mathbf{p}            }[][ \mathrm{e}            ]$ to lie on a safe contact surface. For instance, ${\indexed{ \Xi                   }[][ \mathfrak{r}          ]} \indexed{ \mathbf{p}            }[][ \mathrm{e}            ] \leq {\indexed{ \xi                   }[][ \mathfrak{r}          ]}$ denote the halfspaces that define lateral limits of the terrain surface, while ${\indexed{ \mathfrak{N}          }[][ \mathfrak{r}          ]} \cdot \indexed{ \mathbf{p}            }[][ \mathrm{e}            ] = {\indexed{ \mathfrak{N}          }[][ \mathfrak{r}          ] \cdot \indexed[surf]{ \omega                }[][ \mathfrak{r}          ]}$ implies that the normal distance from the plane should be zero, i.e. the contact point has to lie on the terrain surface. Note that the row-size of the matrix $\indexed{ \Xi                   }[][ \mathfrak{r}          ]$ and vector $\indexed{ \xi                   }[][ \mathfrak{r}          ]$ depends on the number of halfspaces required to define the terrain region $\indexed{ \pazocal{S}           }[][ \mathfrak{r}          ]$, while the column size of the matrix $\indexed{ \Xi                   }[][ \mathfrak{r}          ]$ is as $\indexed{ \mathbf{p}            }[][ \mathrm{e}            ]$, namely 3.

## Dynamics-based contacts planning

Thus far, we have assumed that to solve problem [\[dynopt_problem\]](#dynopt_problem){reference-type="eqref" reference="dynopt_problem"} a set of terrain surfaces, from where contacts are selected, was given. Alternatively, a contact sequence could also be given by for example a contact planner such as [@Tonneau:2018dm; @lin_efficient_2019]. In the following, we propose a mixed-integer formulation that enables the selection of terrain surfaces and contact sequences based on a measure of dynamical robustness.

### Terrain description and contact model

We now describe how a terrain is modeled and how contacts are selected within this description of the terrain using the notation of [@DBLP:conf/humanoids/DeitsT14].

The terrain consists of a set of $\mathrm{R}$ convex, obstacle free regions $\indexed{ \pazocal{S}           }[][ \mathfrak{r}          ]$ where $\mathfrak{r}          \in \left\{ 1,\cdots, \mathrm{R}            \right\}$ and we consider the selection of a sequence of $\mathrm{M}$ contact locations $\indexed{ \mathbf{p}            }[][ \mathrm{m}            ]$ where $\mathrm{m}            \in \left\{ 1,\cdots, \mathrm{M}            \right\}$. We note that the mapping between index ${ \mathrm{m}            }$ of the selected contact location ${\indexed{ \mathbf{p}            }[][ \mathrm{m}            ]}$ and, endeffector $\mathrm{e}$ and the range of timesteps $\mathrm{t}$, in which endeffector location $\indexed{ \mathbf{p}            }[][ \mathrm{e}            , \mathrm{t}            ]$ is active, is predefined. For instance, we could optimize $\mathrm{M}            =4$ contacts with $\mathrm{M}            /2$ contacts for each foot in a locomotion task, or we could optimize a larger number of contacts $\mathrm{M}            =6$, where the 2 additional contacts are free slots to select hand contacts. Note that stance and flight timings can later be changed within the dynamics problem. Also $\mathfrak{r}          =  \varphi               ( \mathrm{e}            , \mathrm{t}            )$ maps $\mathrm{e}            , \mathrm{t}$ to surface $\mathfrak{r}$ chosen for contact $\mathrm{m}$.

The matrix of binary variables ${ \pazocal{H}           \in \{0,1\}^{( \mathrm{M}            -\indexed{ \mathrm{M}            }[][0])\times \mathrm{R}            }}$ (indexed by contact $\mathrm{m}            \in \{1,\cdots, \mathrm{M}            -\indexed{ \mathrm{M}            }[][0]\}$ and terrain surface $\mathfrak{r}          \in \{1,\cdots, \mathrm{R}            \}$) defines the terrain surface ${\indexed{ \pazocal{S}           }[][ \mathfrak{r}          ]}$, whose domain contains the contact location $\indexed{ \mathbf{p}            }[][ \mathrm{m}            ]$ ($\indexed{ \mathrm{M}            }[][0]$ are contacts initially active and thus with a predefined pose). The model is defined as follows $$\begin{align}
        %
        % surface selection matrix
        %
        &{\indexed{ \pazocal{H}           }[][ \mathrm{m}            , \mathfrak{r}          ] \implies \indexed{ \mathbf{p}            }[][ \mathrm{m}            ] \in  \pazocal{U}           (\indexed{ \pazocal{S}           }[][ \mathfrak{r}          ])} \label{eq_cntopt_cntassign} \\
        %
        % Fixed or not according to endeffector type
        %
        &{\sum_{ \mathfrak{r}          } \indexed{ \pazocal{H}           }[][ \mathrm{m}            , \mathfrak{r}          ]}
        \begin{cases}
        = 1, \quad \textrm{for feet contacts} \\
        \leq 1, \quad \textrm{for hands contacts}
        \end{cases} \label{eq_cntopt_integrality} \\
        %
        % Force zeroing for non-active hand contacts
        %
        &1 - {\sum_{ \mathfrak{r}          } \indexed{ \pazocal{H}           }[][ \mathrm{m}            , \mathfrak{r}          ]} \implies (\indexed{ \mathbf{f}            }[][ \mathrm{e}            , \mathrm{t}            ] = 0), \quad \textrm{for hands} \label{eq_cntopt_nonactivefrcs}  \\[0.2em]
        %
        % Friction cones for active forces
        %
        &{\indexed{ \pazocal{H}           }[][ \mathrm{m}            , \mathfrak{r}          ]} \implies {\indexed[cone]{ \pazocal{F}           }[][ \mu                   ]} { \mathfrak{R}          (\indexed{ \pazocal{S}           }[][ \mathfrak{r}          ])} \indexed{ \mathbf{f}            }[][ \mathrm{e}            , \mathrm{t}            ] \leq 0, \quad \textrm{friction cone} \label{eq:frccone_cntopt}
        %       
    \end{align}$$ Thus, $\indexed{ \pazocal{H}           }[][ \mathrm{m}            , \mathfrak{r}          ]$ decides upon the terrain region from where a contact location can be selected. Integrality constraints [\[eq_cntopt_integrality\]](#eq_cntopt_integrality){reference-type="eqref" reference="eq_cntopt_integrality"} enforce membership of a contact location to at most one terrain surface. When no contact region is selected (e.g. no hand contact), control variables such as contact forces should be inactive (Eq. [\[eq_cntopt_nonactivefrcs\]](#eq_cntopt_nonactivefrcs){reference-type="eqref" reference="eq_cntopt_nonactivefrcs"}). When a contact region is selected, local endeffector forces ${ \mathfrak{R}          ( \pazocal{S}           )^{T}} \indexed{ \mathbf{f}            }[][ \mathrm{e}            , \mathrm{t}            ]$ must satisfy friction cone constraints, as in [\[eq:frccone_cntopt\]](#eq:frccone_cntopt){reference-type="eqref" reference="eq:frccone_cntopt"}. ${\indexed[cone]{ \pazocal{F}           }[][ \mu                   ]}$ is a matrix function of $\mu$ such that its product with the local force, returns a vector of negative values.

### Reachability constraints

Reachability constraints between footstep locations are selected based on kinematic reachability using linear inequalities such as in [@khadiv:humanoids2016] for forward or lateral motions or, based on the intersection of SOC constraints [@DBLP:conf/humanoids/DeitsT14] for more general settings. They can be described in a convex form using linear inequalities based on kinematic reachability such as in $$\begin{align}
    &\indexed[min]{\Delta \mathbf{p}            } \leq {|} {\indexed{ \mathbf{p}            }[][ \mathrm{m}            ]} - {\indexed{ \mathbf{p}            }[][ \mathrm{m}            -1]} {|} \leq \indexed[max]{\Delta \mathbf{p}            }
\end{align}$$ . Reachability constraints can also be described as in [@DBLP:conf/humanoids/DeitsT14] using an intersection of SOC constraints $$\begin{align}
        %
        % Only one active approximation
        %
        &{\sum\limits_{ \mathfrak{h}          \in  \mathrm{H}            } \indexed[sec]{ \mathfrak{S}          }[][ \mathfrak{h}          , \mathrm{m}            ] = \sum\limits_{ \mathfrak{h}          \in  \mathrm{H}            } \indexed[sec]{ \mathfrak{C}          }[][ \mathfrak{h}          , \mathrm{m}            ]} = 1 \label{eq_surf_integrality} \\ 
        %
        % Sine matrix binary variable
        %
        &{\indexed[sec]{ \mathfrak{S}          }[][ \mathfrak{h}          , \mathrm{m}            ] \implies
            \begin{cases}
                \indexed[sin]{ \Theta                }[][ \mathfrak{h}          ] \leq \indexed{ \theta                }[][ \mathrm{m}            ] \leq \indexed[sin]{ \Theta                }[][ \mathfrak{h}          +1] \\
                \indexed[sin]{ \mathfrak{s}          }[][ \mathrm{m}            ] = \indexed[sin]{ \mathfrak{u}          }[][ \mathfrak{h}          ] \indexed{ \theta                }[][ \mathrm{m}            ] + \indexed[sin]{ \mathfrak{v}          }[][ \mathfrak{h}          ]
            \end{cases}} \label{eq_surf_sinmat} \\
        %
        % Cosine matrix binary variable
        %
        &{\indexed[sec]{ \mathfrak{C}          }[][ \mathfrak{h}          , \mathrm{m}            ] \implies
            \begin{cases}
                \indexed[cos]{ \Theta                }[][ \mathfrak{h}          ] \leq \indexed{ \theta                }[][ \mathrm{m}            ] \leq \indexed[cos]{ \Theta                }[][ \mathfrak{h}          +1] \\
                \indexed[cos]{ \mathfrak{c}          }[][ \mathrm{m}            ] = \indexed[cos]{ \mathfrak{u}          }[][ \mathfrak{h}          ] \indexed{ \theta                }[][ \mathrm{m}            ] + \indexed[cos]{ \mathfrak{v}          }[][ \mathfrak{h}          ]
            \end{cases}} \label{eq_surf_cosmat} \\
        %
        % Heuristic separation among endeffector locations
        %
        &\left\lVert {
            \begin{bmatrix}
                \indexed{ \mathbf{p}            }[ \mathrm{x}            ][ \mathrm{m}            ] \\
                \indexed{ \mathbf{p}            }[ \mathrm{y}            ][ \mathrm{m}            ]
            \end{bmatrix}} \hspace{-0.05cm}-\hspace{-0.05cm}
            \left( {
                \begin{bmatrix}
                    \indexed{ \mathbf{p}            }[ \mathrm{x}            ][ \mathrm{m}            -1] \\
                    \indexed{ \mathbf{p}            }[ \mathrm{y}            ][ \mathrm{m}            -1]
                \end{bmatrix}} \hspace{-0.05cm}+\hspace{-0.05cm}
            {
                \begin{bmatrix}
                    \indexed[cos]{ \mathfrak{c}          }[][ \mathrm{m}            ] & \hspace{-0.15cm} -\indexed[sin]{ \mathfrak{s}          }[][ \mathrm{m}            ] \\
                    \indexed[sin]{ \mathfrak{s}          }[][ \mathrm{m}            ] & \hspace{-0.15cm} \phantom{-} \indexed[cos]{ \mathfrak{c}          }[][ \mathrm{m}            ]
                \end{bmatrix} \indexed{ \pazocal{P}           }[][1,2]}
            \right) \right\rVert \leq {\indexed{ \pazocal{D}           }[][1,2]} \label{eq_surf_separation}
    \end{align}$$

In the latter case e.g., a piecewise affine approximation of sine and cosine functions is used to model footsteps rotation ${ \theta                _{ \mathrm{m}            } \in  \mathbb{R}            }$ in a convex form. The matrices of binary variables ${\indexed[sec]{ \mathfrak{S}          }, \indexed[sec]{ \mathfrak{C}          } \in \{0,1\}^{ \mathrm{H}            \times \indexed{ \mathrm{M}            }[][f]}}$ (indexed by affine approximation $\mathfrak{h}          \in [1, \mathrm{H}            ]$ and contact $\mathrm{m}            \in [1, \indexed{ \mathrm{M}            }[][f]]$ ) are used to select the active affine approximation of sine or cosine ${ \mathfrak{h}          }$ for each footstep ${ \mathrm{m}            }$. $\mathrm{H}$ denotes the number of affine functions used to approximate sine and cosine, and $\indexed{ \mathrm{M}            }[][f]$ the number of footstep contacts to be selected out of the total number of contacts $\mathrm{M}$. As shown before, integrality constraints (Eq. [\[eq_surf_integrality\]](#eq_surf_integrality){reference-type="eqref" reference="eq_surf_integrality"}) guarantee that only one approximation is active at each footstep ${ \mathrm{m}            }$.

An element $\indexed[sec]{ \mathfrak{S}          }[][ \mathfrak{h}          , \mathrm{m}            ], \indexed[sec]{ \mathfrak{C}          }[][ \mathfrak{h}          , \mathrm{m}            ]$ being one implies the activation of a single affine approximation for sine and cosine functions, as shown in [\[eq_surf_sinmat\]](#eq_surf_sinmat){reference-type="eqref" reference="eq_surf_sinmat"}-[\[eq_surf_cosmat\]](#eq_surf_cosmat){reference-type="eqref" reference="eq_surf_cosmat"}. Each affine approximation is defined by a region of validity of the footstep rotation angle ${\indexed{ \theta                }[][ \mathrm{m}            ] \in [\indexed[sin]{ \Theta                }[][ \mathfrak{h}          ], \indexed[sin]{ \Theta                }[][ \mathfrak{h}          +1]]}$ (for sine) or ${\indexed{ \theta                }[][ \mathrm{m}            ] \in [\indexed[cos]{ \Theta                }[][ \mathfrak{h}          ], \indexed[cos]{ \Theta                }[][ \mathfrak{h}          +1]]}$ (for cosine) and, the corresponding affine approximation ${\indexed[sin]{ \mathfrak{s}          }[][ \mathrm{m}            ] = \indexed[sin]{ \mathfrak{u}          }[][ \mathfrak{h}          ] \indexed{ \theta                }[][ \mathrm{m}            ] + \indexed[sin]{ \mathfrak{v}          }[][ \mathfrak{h}          ]}$ (for sine) or ${\indexed[cos]{ \mathfrak{c}          }[][ \mathrm{m}            ] = \indexed[cos]{ \mathfrak{u}          }[][ \mathfrak{h}          ] \indexed{ \theta                }[][ \mathrm{m}            ] + \indexed[cos]{ \mathfrak{v}          }[][ \mathfrak{h}          ]}$ (for cosine), where $\indexed[sin]{ \mathfrak{u}          }[][ \mathfrak{h}          ], \indexed[sin]{ \mathfrak{v}          }[][ \mathfrak{h}          ], \indexed[cos]{ \mathfrak{u}          }[][ \mathfrak{h}          ], \indexed[cos]{ \mathfrak{v}          }[][ \mathfrak{h}          ] \in  \mathbb{R}$ are parameters that define slope and intercept values of each affine approximation. The footstep rotation angle $\indexed{ \theta                }[][ \mathrm{m}            ]$, sine $\indexed[sin]{ \mathfrak{s}          }[][ \mathrm{m}            ]$ and cosine $\indexed[cos]{ \mathfrak{s}          }[][ \mathrm{m}            ]$ of this angle constitute optimization variables.

Finally, these variables are used to model the range of available positions for the next footstep (Eq. [\[eq_surf_separation\]](#eq_surf_separation){reference-type="eqref" reference="eq_surf_separation"}) based on the current footstep position and yaw angle as the intersection of two SOC constraints, parameterized by a pair of points $\indexed{ \pazocal{P}           }[][1,2] \in  \mathbb{R}            ^{2\times1}$ (located sideways of the footstep position $\mathrm{m}            -1$ and rotated by the yaw angle), and a pair of distances $\indexed{ \pazocal{D}           }[][1,2] \in  \mathbb{R}$.

### Dynamics model and objective function

To keep computational complexity low, in the mixed-integer approach to select contact sequences, we use a light version of problem [\[dynopt_problem\]](#dynopt_problem){reference-type="eqref" reference="dynopt_problem"}, where we do not consider the endeffector torques $\indexed{ \gamma                }[][ \mathrm{e}            , \mathrm{t}            ]$ (in other words, a point contact model is assumed), we use a linear approximation of the friction cones and, either a centroidal momentum dynamics model with fixed or non-fixed timings. The objective function $\indexed{ \phi                  }[cnt][ \mathrm{t}            ]$ similarly to [\[eq_dynopt_cost\]](#eq_dynopt_cost){reference-type="eqref" reference="eq_dynopt_cost"} regularizes states and controls and also incorporates user-defined objectives.

### Numerical optimization

To evaluate the performance of our method at synthesizing contact plans and selecting contact surfaces, we implement a custom mixed-integer solver able to solve a sequence of SOC programs. It relies on two functions to bound the optimal value of a given search space. The lower bound comes from a relaxation of the search space binary variables and the upper bound by any solution where the binary variables are actually binary. The rest of the constraints are treated using the iterative models previously described. The feasible search space is partitioned into convex sets and each partition bounded. The algorithm converges once global lower and upper bounds are close enough, otherwise the partitions are refined and the search process is repeated. The implementation of the custom mixed-integer solver is based on a branch and bound method for global nonconvex optimization, as detailed in [@mixed_integer_solver]. In simple scenarios, we use linear reachability constraints, and SOC constraints in more complex ones, as will be shown in Section [5](#sec:experiments){reference-type="ref" reference="sec:experiments"}.

# Experimental Results {#sec:experiments}

In this section, we show experimental results about the optimization of contact and movement plans using the algorithms previously described. We have tested them in several challenging multi-contact scenarios using simulated humanoid and quadruped robots and a real quadruped robot (Fig. [8](#fig:humanoid_robot){reference-type="ref" reference="fig:humanoid_robot"}). The resulting motions are visible in the accompanying video.

:::: {#fig:robotic_platforms .figure}
![Simulated humanoid robot](Ponton2020Efficient_figs/scenario10.jpg){#fig:humanoid_robot height="3cm"}

![Real quadruped robot](Ponton2020Efficient_figs/jump_1_crop.jpg){#fig:quadruped_robot height="3cm"}

::: {.caption short-caption=""}
Robotic platforms used throughout the experimental section. Left, a simulated humanoid robot with 32 torque-controlled degrees of freedom is used in the SL simulation environment [@SLSimLab]. It has 7 degrees of freedom in each limb and 3 in the torso. Right, we show the quadruped robot 'Solo' with 8 torque-controlled joints [@grimminger2019open].
:::
::::

## On the optimization of movement plans {#exp:dynamics_planning}

In this section, we analyze solutions of problem [\[dynopt_problem\]](#dynopt_problem){reference-type="eqref" reference="dynopt_problem"} in terms of convergence to feasibility (measured by the amount of constraint violation ${ \epsilon              }$ of the solution) and time complexity to converge to the desired feasibility threshold. We also present results regarding the qualitative improvement of motions that include time and/or contact locations in the optimization. Finally, we will show how full-body motions can be optimized using a kino-dynamic approach, how actuation limits can be included in the dynamics optimization, and tracking performance of time-optimized movement plans.

### Convergence to feasibility and time complexity {#exp:feasibility_convergence}

To analyze convergence properties and computational complexity of the algorithm, we use a set of 8 optimized motions (shown in Fig. [19](#fig5:movement_planning){reference-type="ref" reference="fig5:movement_planning"}) to gather statistics about its performance. Table [\[tab:costfunction\]](#tab:costfunction){reference-type="ref" reference="tab:costfunction"} shows a typical cost function and the relative importance of the weighted costs used to optimize a motion.

:::: {#fig5:movement_planning .figure}
![Rough terrain](Ponton2020Efficient_figs/scenario01.jpg){#fig:motion01 width="100%"}

![Down-Up](Ponton2020Efficient_figs/scenario02.jpg){#fig:motion02 width="100%"}

![Walking stairs](Ponton2020Efficient_figs/scenario03.jpg){#fig:motion03 width="100%"}

![Up stairs](Ponton2020Efficient_figs/scenario04.jpg){#fig:motion04 width="100%"}

![Using hands](Ponton2020Efficient_figs/scenario05.jpg){#fig:motion05 width="100%"}

![Up with hands](Ponton2020Efficient_figs/scenario06.jpg){#fig:motion06 width="100%"}

![Tilted terrain](Ponton2020Efficient_figs/scenario07.jpg){#fig:motion07 width="100%"}

![Narrow path](Ponton2020Efficient_figs/scenario08.jpg){#fig:motion08 width="100%"}

::: {.caption short-caption=""}
Examples of time-optimized dynamic movement plans.
:::
::::

::: tabular
\|@ L3.6cm@ \| @ L2.5cm@ \| @ C2.0cm@ \| **Cost** & $\;\;$**Functional Form** & **Scaling Order**\
$\;\quad$ CoM terminal cost & ${\quad \mathfrak{Q}          ( \mathbf{r}            _{ N                     } - ( \mathbf{r}            _{0}+\Delta \mathbf{r}            ))}$ & ${1e+4}$\
$\;\quad$ Time regularization & ${\quad\sum_{ \mathrm{t}            } \mathfrak{Q}          ( \Delta                _{ \mathrm{t}            }-\indexed[0]{ \Delta                }[][ \mathrm{t}            ])}$ & ${1e+3}$\
$\;\quad$ Momenta terminal cost & ${\quad \mathfrak{Q}          ( \mathbf{h}            _{ N                     })}$ & ${1e+2}$\
$\;\quad$ Endeffector consensus cost & ${\quad\sum_{ \mathrm{t}            } \mathfrak{Q}          (\indexed{ \mathbf{p}            }[][ \mathrm{e}            , \mathrm{t}            ] - \indexed[kin]{ \mathbf{p}            }[][ \mathrm{e}            , \mathrm{t}            ])}$ & ${1e+0}$\
$\;\quad$ Momenta consensus cost & ${\quad\sum_{ \mathrm{t}            } \mathfrak{Q}          (\indexed{ \mathbf{h}            }[][ \mathrm{t}            ] - \indexed[kin]{ \mathbf{h}            }[][ \mathrm{t}            ])}$ & ${1e+0}$\
$\;\quad$ Momenta rate cost & ${\quad\sum_{ \mathrm{t}            } \mathfrak{Q}          (\dot{ \mathbf{h}            }_{ \mathrm{t}            })}$ & ${1e-1}$\
$\;\quad$ Momenta running cost & ${\quad\sum_{ \mathrm{t}            } \mathfrak{Q}          ( \mathbf{h}            _{ \mathrm{t}            })}$ & ${1e-2}$\
$\;\quad$ Force running cost & ${\quad\sum_{ \mathrm{t}            } \mathfrak{Q}          ( \mathbf{f}            _{ \mathrm{e}            , \mathrm{t}            })}$ & ${1e-3}$\
$\;\quad$ Torque running cost & ${\quad\sum_{ \mathrm{t}            } \mathfrak{Q}          ( \tau                  _{ \mathrm{e}            , \mathrm{t}            })}$ & ${1e-3}$\
:::

In Fig. [20](#fig:conv_per_num_timesteps){reference-type="ref" reference="fig:conv_per_num_timesteps"}, we present statistics about time complexity, convergence to feasibility and relative cost reduction when using the same objective function but different number of discretization timesteps and algorithmic settings. In particular, we look at what happens when the optimization includes or not time as an optimization variable $Time \textrm{ vs. } Mom$, includes or not optimization of contact locations $Cnt$, uses the soft-constraint or trust-region relaxation approaches $Sc \textrm{ vs. } Tr$. As an example, $MomSc$ refers to a motion optimized with fixed timings, fixed contacts and using the soft-constraint heuristic, while $TimeTrCnt$ refers to a motion optimized including timings, contact locations and using the trust-region heuristic.

![*Top:* Roughly linear-time complexity of movement plans within the shown range of timesteps $N$: with or without time optimization $Time-Mom$, using soft-constraint or trust-region heuristics $Sc-Tr$, and with or without optimization of contact locations $Cnt$. *Center:* Corresponding normalized convergence errors or amount of constraint violation ${ \epsilon              }$ as given by [\[eq_error\]](#eq_error){reference-type="eqref" reference="eq_error"} and *Bottom:* numerical relative cost reduction of motions optimized including time and/or contact locations with respect to motions using fixed contacts and timings. Each datapoint averages information from 8 experiments (shown in Fig. [19](#fig5:movement_planning){reference-type="ref" reference="fig5:movement_planning"}) optimized using the same objective function but different number of timesteps $N$ and heuristics.](figures/timestatistics/TimingResults.pdf){#fig:conv_per_num_timesteps width="100%"}

First of all, in the center plot we show the amount of constraint violation ${ \epsilon              }$ of the optimized solutions, as measured by [\[eq_error\]](#eq_error){reference-type="eqref" reference="eq_error"}. We note that the algorithm converges when ${ \epsilon              }$ or its reduction from one iteration to another ${\indexed{ \epsilon              }[][ \pazocal{I}           ]-\indexed{ \epsilon              }[][ \pazocal{I}           -1]}$ fall below a desired threshold (typically in the order of $1e-4$) and, as visible on the plot, our method converges in all experiments to the desired feasibility thresholds in all settings.

On the top, we show statistics about the time-complexity of the algorithm for convergence to the desired feasibility thresholds; in particular, this shows evidence of linear complexity in the number of timesteps for momentum and time optimization problems. We notice that for fixed-time optimization problems, neither heuristics nor the optimization of contact locations affect the solving time performance. A similar behavior can be seen for time optimization problems with the difference that the trust-regions are slightly faster than the soft-constraints.

Finally, on the bottom plot we show numerically the relative reduction of the cost when optimizing time and contact locations. In orange tones, we see the reference normalized costs of momentum optimization problems using fixed contact locations and timings for trust-region and soft-constraint heuristics, namely $MomSc$ and $TimeSc$. As expected both achieve a similar minimum and have thus the same normalized cost of one. As shown above, considering contact locations as optimization variables (in the form of linear constraints and over a given terrain surface) has minimum impact on solving time performance, yet it significantly reduces the objective value (between 35 and 40 percent) because this degree of freedom allows the optimizer to select motions with lower momentum values, e.g. motions with less lateral sway of the CoM (see $MomScCnt$ and $MomTrCnt$ in red tones).

![Average number of iterations required to solve an optimization problem with or without time optimization for different number of discretization timesteps and, average time to solve each iteration. Each datapoint is based on 32 experiments, with different heuristic $Sc-Tr$ and with our without optimization of contacts $Cnt$.](Ponton2020Efficient_figs/AverageTimings.png){#fig:average_timings width="48%"}

The effect of time optimization on the objective value is dependent on the problem time horizon (or number of timesteps $N$). For simplicity, we can assume that the value of one timestep is 0.1 seconds (which is the discretization time we use for fixed time optimization) and thus the horizontal axis spans between 2 and 20 seconds. For instance, in problems with short-time horizons such as those at the leftmost side, the cost difference between motions that consider or not time as an optimization variable is modest, but as the look-ahead horizon increases (right side) time optimization becomes a powerful way of shaping the motion to achieve lower costs. We notice that in this case the soft-constraint heuristic ($timeSc$ and $timeScCnt$) finds in average slightly lower local minima than the trust-region heuristic ($timeTr$ and $timeTrCnt$).

In Fig. [21](#fig:average_timings){reference-type="ref" reference="fig:average_timings"}, we show the average number of iterations required to solve a momentum or time optimization problem for varying number of timesteps, as well as the average time required to solve each of these iterations. For instance, momentum optimization problems require 2-3 iterations, while time optimization problems 7-10. However, the difference in solving times of one iteration is small, e.g. for a time horizon of 2 seconds ($N                     = 20$) the solving times are 80 and 100 \[ms\] for momentum and time optimization problems respectively. This suggests that the approach could be used in a receding horizon setting. In such setting, the optimizer could be warm-started from the previous solution to significantly increase resolution time (typically one would only need to solve one iteration of the problem for a short look-ahead horizon).

### Qualitative improvement of solutions {#exp:qualitative_results}

Here, we discuss qualitative results that cannot be described from the statistical analysis above. We therefore restrict our analysis to specific instances of the problem. In Fig. [22](#fig:lowfriction_comparison){reference-type="ref" reference="fig:lowfriction_comparison"} we show time optimal results for a walking up tilted stairs motion traversed with two different values of the friction coefficient $\mu$. In the first case ($\mu                   = 0.35$), the tendency is to increase the value of timestep variables $\Delta                _{ \mathrm{t}            }$ during double supports to have enough time to slowly accelerate the CoM while respecting physical constraints, resembling statically stable motions. In an environment with flat surfaces, the same approach would be valid even if the friction coefficient is further reduced (e.g. $\mu                   = 0.25$). However, in a terrain with tilted surfaces such a strategy is not viable. In such a setting, even the fixed-time version of our algorithm cannot find a dynamically feasible solution. Yet, our time optimization approach is able to find a solution, whose main strategy is to quickly traverse the tilted surfaces to get to the uppermost flat contact surfaces. During this phase, lateral contact forces are exploited to the limit, and then a similar strategy to the previous case is found.

:::: {#fig:lowfriction_comparison .figure}
\
![image](Ponton2020Efficient_figs/LowFrictionComparison.png){width="49%"}

::: {.caption short-caption=""}
Comparison of optimal normalized endeffector forces and timing results for two different values of friction coefficient $\mu$. Timings ${\indexed[0]{ \Delta                }[][ \mathrm{t}            ]}$ are the initial ones and ${\indexed[*]{ \Delta                }[][ \mathrm{t}            ]}$ the final optimized ones.
:::
::::

In Fig. [23](#fig:walking_up_with_hands){reference-type="ref" reference="fig:walking_up_with_hands"}, we show a walking up stairs motion using hand contacts. In our experiments, in such multi-contact scenarios time optimization does not significantly change motion timings, as can be seen in the bottom plot (that graphically illustrates endeffector activations $\mathrm{e}            _{\mathrm{cnt}}$) by comparing the timings of a fixed-time optimization problem (Mom) and those of a time optimization problem (Time). However, optimizing contact locations allows us to find motions with less CoM sway. This is visible, for example, in the CoM trajectories for a momentum optimization without optimization of contact locations $MomSc$ or even a time optimization without optimization of contacts $TimeSc$ and a momentum or time optimization that includes optimization of contact locations such as $MomScCnt$ and $TimeScCnt$ respectively. These motions are more energetically efficient and arguably easier to control with only a small additional computational cost in the optimization. Note that the top plot in Fig. [23](#fig:walking_up_with_hands){reference-type="ref" reference="fig:walking_up_with_hands"} is a top view of the walking up stairs movement using hands, not to be confused with a planar motion.

:::: {#fig:walking_up_with_hands .figure}
\
![image](Ponton2020Efficient_figs/HandingMotion.png){width="49%"}

::: {.caption short-caption=""}
Comparison between CoM and normalized linear momentum in the lateral direction for a walking up stairs motion using hands. The squares, circles, diamonds and stars show the endeffector locations $\indexed{ \mathbf{p}            }[][ \mathrm{e}            , \mathrm{t}            ]$ optimized under different settings, as shown in the legend. Bottom plot shows the contact activation of endeffectors over the time horizon for momentum (Mom) and time (Time) optimization problems (low value is inactive and high value is active).
:::
::::

### Kino-dynamic full-body optimization

In this section, we show how our algorithm can be used in the kino-dynamic approach described in Section [2](#sec:problem_formulation){reference-type="ref" reference="sec:problem_formulation"}, and illustrated in Figure [3](#fig:KinDynStructure){reference-type="ref" reference="fig:KinDynStructure"}, to generate whole-body time-optimal motions.

First, we use the climbing uneven stairs motion depicted in Fig. [14](#fig:motion04){reference-type="ref" reference="fig:motion04"} to illustrate algorithmic convergence of our method to kino-dynamic consistency. In Fig. [24](#fig:kinodynamic_approach){reference-type="ref" reference="fig:kinodynamic_approach"}, we graphically compare (on the top 3 plots) kinematic $\indexed[kin]{ \mathbf{h}            }$ and dynamic momentum trajectories $\indexed[dyn]{ \mathbf{h}            }$ at the end of each dynamics optimization. We use dark colors to show dynamic trajectories $\indexed[dyn]{ \mathbf{h}            }$, and the same, but light color, for kinematic ones $\indexed[kin]{ \mathbf{h}            }$. Solid lines correspond to motions optimized using soft-constraints, and dashed lines to motions optimized using trust-regions. It can be seen from the plots that they qualitatively converge to similar solutions, as it is difficult to distinguish them from each other.

![This figure shows convergence to feasibility of each dynamics optimization along three kino-dynamic iterations. We compare desired kinematic momentum trajectories $Kin$ and dynamic momentum trajectories $Dyn$ (computed out of optimal controls) at the end of each dynamic optimization. Bottom plots (left for linear momentum and right for angular momentum) show how errors $\indexed{ \epsilon              }[][ \mathbf{l}            ]$ and $\indexed{ \epsilon              }[][ \mathbf{k}            ]$ decrease until convergence along each kino-dynamic iteration. Momentum values are normalized by robot mass. Vertical colored bars show the activation of each endeffector over time.](figures/kditers/KinoDynIters.pdf){#fig:kinodynamic_approach width="49%"}

On the bottom plot, we show how quantitatively the norms $\indexed{ \epsilon              }[][ \mathbf{l}            ]$ and $\indexed{ \epsilon              }[][ \mathbf{k}            ]$, that compare momentum trajectories obtained from optimal controls and the momentum trajectory variables that track desired kinematic momentum trajectories, decrease until convergence at each kino-dynamic iteration. Note that the first dynamics optimization (shown in red) takes the longest to converge and that trajectories optimized in subsequent iterations without using any information from previous ones converge faster (see e.g. how solid and dashed lines from the first iteration compare to those at subsequent iterations). In practice however, by warm-starting the heuristics of dynamic optimizations with the results and information of previous iterations, the optimization problems can be solved much faster and with fewer iterations, as shown in dotted trajectories. Despite that at each iteration kinematic and dynamic momentum trajectories match, in practice we use at least two iterations to converge to a motion easily executable on a physical simulator.

Note as well how linear momentum converges fast and to high levels of precision, while angular momentum does it only to modest levels. See for example, how solid and dashed lines achieve in 4 iterations the required precision for linear momentum errors $\indexed{ \epsilon              }[][ \mathbf{l}            ]$, while it takes around 8 for angular momentum errors $\indexed{ \epsilon              }[][ \mathbf{k}            ]$. This is due to the fact that on the one hand angular momentum depends on the CoM and can only achieve a higher precision once this variable has converged, and on the other hand due to the fact that given a CoM trajectory, angular momentum can be further optimized along it by exploiting the control degrees of freedom left.

Finally, we present results on a simulated quadruped robot, where we show in Fig. [25](#fig:motion_with_flight_phases){reference-type="ref" reference="fig:motion_with_flight_phases"} the kino-dynamic trajectories of a galloping motion, very difficult to optimize due to the presence of simultaneous flight phases for all endeffectors, where only gravity is acting on the system. Despite this challenge, kino-dynamic trajectories converge qualitatively well thanks to the exploitation of optimal timing for all available endeffector forces.

:::: {#fig:motion_with_flight_phases .figure}
\
![image](Ponton2020Efficient_figs/GallopTracking.png){width="49%"}

::: {.caption short-caption=""}
Kino-dynamic results for the optimization of a galloping motion that includes simultaneous flight phases for all endeffectors.
:::
::::

### Execution of movement plans {#exp:motion_execution}

In this section, we show that optimal motion plans optimized in the previous section using a kino-dynamic approach can be executed in a physical simulator using the architecture described in Fig. [1](#fig:ExecutionArchitecture){reference-type="ref" reference="fig:ExecutionArchitecture"}.

In Fig. [26](#fig:tracking_stepping_motion){reference-type="ref" reference="fig:tracking_stepping_motion"}, we first show tracking of an optimized movement plan for a robot climbing uneven stairs using inverse dynamics controllers [@AlexAuroPaper] that realize closed-loop behaviors based on risk-sensitive feedback design [@FarbodRiskSensitive] that explicitly considers process and measurement noise [@MeasurementUncertainty] to compute time-varying feedback gains. In our experience, such a controller leads to overall lower impedance gains in comparison to typical LQR design, which is beneficial to increase compliance at contact with an environment that differs from the ideal scenario used for planning. Note that such a feedback controller is important in this case, as the kino-dynamic optimizer is not used in a receding horizon fashion. The top three plots show the optimized momentum trajectories ($\indexed[dyn]{ \mathbf{l}            }, \indexed[dyn]{ \mathbf{k}            }$ in blue) as well as their tracking ($\indexed[exe]{ \mathbf{l}            }, \indexed[exe]{ \mathbf{k}            }$ in red). At the bottom left corner, endeffectors activation over time $\mathrm{e}            _{\mathrm{cnt}}$ are shown, as given by the optimal timings $\indexed[*]{ \Delta                }[][ \mathrm{t}            ]$ at the bottom right corner.

:::: {#fig:tracking_stepping_motion .figure}
\
![image](Ponton2020Efficient_figs/WalkingExecution.png){width="49%"}

::: {.caption short-caption=""}
Tracking of desired momentum trajectories for the climbing up stairs motion (shown in Fig. [14](#fig:motion04){reference-type="ref" reference="fig:motion04"}) using time optimization.
:::
::::

In Fig. [\[fig:torques_limits\]](#fig:torques_limits){reference-type="ref" reference="fig:torques_limits"}, we show that actuation limits are not always satisfied, if they are not explicitly considered. For instance, on the left column, we analyze torques in the climbing up stairs motion (Fig. [14](#fig:motion04){reference-type="ref" reference="fig:motion04"}). Here, the knee flexion-extension (KFE) joint torque exceeds its limit by 30 Nm (bottom-left in blue). To enforce torque limits, the solution of the kinematics problem ($\indexed[*]{ \mathbf{q}            }, \indexed[*]{ \mathbf{\dot{q}}      }, \indexed[*]{ \mathbf{\ddot{q}}     }$) is used to build a linear approximation of Eq. [\[eq_actuated_part\]](#eq_actuated_part){reference-type="eqref" reference="eq_actuated_part"} along the motion trajectory (used to build the constraint of Eq. [\[eq_dynopt_joint_torques\]](#eq_dynopt_joint_torques){reference-type="eqref" reference="eq_dynopt_joint_torques"}). This constraint relates contact wrenches $\indexed{ \lambda              }[][ \mathrm{e}            ]( \mathrm{t}            ) = \begin{bmatrix} \indexed{ \gamma                }[][ \mathrm{e}            , \mathrm{t}            ] & \indexed{ \mathbf{f}            }[][ \mathrm{e}            , \mathrm{t}            ] \end{bmatrix} \forall  \mathrm{e}            \in   \mathrm{e}            _{\mathrm{cnt}}$ and torques $\Lambda              ( \mathrm{t}            )$, making it possible to adapt contact wrenches to satisfy torque limits. The top three left plots show how the right foot's wrench can be adapted from a motion that does not satisfy torque limits (NoTrqLimPlan in blue) to one that does (TrqLimPlan in orange). Further, in green the torque limit being satisfied during execution is shown. Another way to satisfy torque limits is by redistribution of contact forces among the available endefectors (Fig. [\[fig:torques_limits\]](#fig:torques_limits){reference-type="ref" reference="fig:torques_limits"} right). In this case, timesteps were kept constant, and the optimizer distributed contact forces in such a way that the left leg is supported by the left hand in order to synthesize a motion within the leg actuation limits. Joint torques plotted correspond to those degrees of freedom of left limbs that control the endeffector position. Furthermore, Fig. [27](#fig:movement_generation_statistics){reference-type="ref" reference="fig:movement_generation_statistics"} shows the effect of torque limits on solve time performance.

::: remark
**Remark 3**. *While we only demonstrated the ability of our approach to include joint actuation limits in the dynamic optimization problem, it would also be straightforward to add such limits in the kinematic optimization problem. Indeed, it would be possible to add linear joint acceleration constraints using Eq. [\[eq_actuated_part\]](#eq_actuated_part){reference-type="eqref" reference="eq_actuated_part"} and the solution of the dynamic optimization problem to approximate the contact forces.*
:::

:::: {#fig:movement_generation_statistics .figure}
![](Ponton2020Efficient_figs/TorqueLimits.png){width="49%"}

![](Ponton2020Efficient_figs/TrqOptTiming.png){width="49%"}

::: {.caption short-caption=""}
Effect of actuation limit constraints on solving time of fixed-time optimization problems for different number of discretization timesteps. Results shown correspond to a walking down and up motion (Fig. [12](#fig:motion02){reference-type="ref" reference="fig:motion02"}) using soft-constraints for torque limits.
:::
::::

Finally, Fig. [28](#fig:capture_regions){reference-type="ref" reference="fig:capture_regions"} compares the ability of the algorithm at synthesizing a dynamically feasible solution under different initial and final conditions. Initial conditions include varying CoM velocities in the horizontal plane and distinct contact supports (one or two feet), while the final condition is a contact configuration as the initial one (single or double support). A solution is colored in orange if after one step, a motion trajectory with momentum values under a small threshold has not been found. The experiment suggests that optimal timings can significantly extend the regions where a feasible dynamical solution is attainable, under given physical conditions and objective function, as well as that timing adaptation is important beyond known results for flat ground walking [@majidJournal].

![Comparison of the regions where a dynamically feasible solution is attainable for single and double support experiments using fixed and optimal timings.](Ponton2020Efficient_figs/CaptureRegions.png){#fig:capture_regions width="49%"}

## On the optimization of contact plans {#exp:contacts_planning}

This subsection discusses results on the surface selection and contacts planning algorithm using a mixed-integer program that makes use of a dynamics model to measure the quality of the motion induced by the selected contacts plan.

Figure [29](#fig:contacts_planner){reference-type="ref" reference="fig:contacts_planner"} shows a schematic of the experiment setup, average timing results, and a comparison between cost decrease and solving time increase for each iteration of the problem internally solved. In the experiment a robot traverses an uneven terrain from the initial stepping stone (in orange) to a desired position forward using a desired number of contacts $\mathrm{M}$. Further, the number of the terrain stepping stones is adapted as shown in the statistics table on the number of regions axis. On the figure's top, mean and one standard deviation of solving times are shown for several configurations of surfaces and number of contacts to optimize. Note how short contact plans can be quickly solved, while longer ones require more computational effort. In those cases, more efficient techniques for contact planning can be used [@Tonneau:2018dm]. For example, a predictive neural network could be used to speed up the evaluation of dynamically feasible contact sequences as in [@yuchi].

![Statistics about solving time for a contacts planning problem under different number of stepping regions and horizon of the number of contacts. It further compares the cost improvement and increment in solving time for different number of iterations $\pazocal{I}$.](Ponton2020Efficient_figs/CntTimings.png){#fig:contacts_planner width="49%"}

:::: {#fig:experiments_1 .figure}
![image](Ponton2020Efficient_figs/trot_1.jpg){height="9%"} ![image](Ponton2020Efficient_figs/trot_2.jpg){height="9%"} ![image](Ponton2020Efficient_figs/trot_3.jpg){height="9%"} ![image](Ponton2020Efficient_figs/trot_4.jpg){height="9%"} ![image](Ponton2020Efficient_figs/trot_5.jpg){height="9%"}

![image](Ponton2020Efficient_figs/dist_trot_1.jpg){height="9%"} ![image](Ponton2020Efficient_figs/dist_trot_2.jpg){height="9%"} ![image](Ponton2020Efficient_figs/dist_trot_3.jpg){height="9%"} ![image](Ponton2020Efficient_figs/dist_trot_4.jpg){height="9%"} ![image](Ponton2020Efficient_figs/dist_trot_5.jpg){height="9%"}

::: {.caption short-caption=""}
Snapshots of the experiments in scenario 1; top) trot on flat surface, bottom) trot on seesaw
:::
::::

:::: {#fig:experiments_2 .figure}
![image](Ponton2020Efficient_figs/jump_1.jpg){height="9.2%"} ![image](Ponton2020Efficient_figs/jump_2.jpg){height="9.2%"} ![image](Ponton2020Efficient_figs/jump_3.jpg){height="9.2%"} ![image](Ponton2020Efficient_figs/jump_4.jpg){height="9.2%"} ![image](Ponton2020Efficient_figs/jump_5.jpg){height="9.2%"}

![image](Ponton2020Efficient_figs/box_jump_1.jpg){height="9.2%"} ![image](Ponton2020Efficient_figs/box_jump_2.jpg){height="9.2%"} ![image](Ponton2020Efficient_figs/box_jump_3.jpg){height="9.2%"} ![image](Ponton2020Efficient_figs/box_jump_4.jpg){height="9.2%"} ![image](Ponton2020Efficient_figs/box_jump_5.jpg){height="9.2%"}

::: {.caption short-caption=""}
Snapshots of the experiments in scenario 2; top) jump in place, bottom) jump on a box
:::
::::

:::: {#fig:experiments_3 .figure}
![image](Ponton2020Efficient_figs/step_jump_1.jpg){height="9.6%"} ![image](Ponton2020Efficient_figs/step_jump_2.jpg){height="9.6%"} ![image](Ponton2020Efficient_figs/step_jump_3.jpg){height="9.6%"} ![image](Ponton2020Efficient_figs/step_jump_4.jpg){height="9.6%"} ![image](Ponton2020Efficient_figs/step_jump_5.jpg){height="9.6%"}

![image](Ponton2020Efficient_figs/step_jump_6.jpg){height="9.5%"} ![image](Ponton2020Efficient_figs/step_jump_7.jpg){height="9.5%"} ![image](Ponton2020Efficient_figs/step_jump_8.jpg){height="9.5%"} ![image](Ponton2020Efficient_figs/step_jump_9.jpg){height="9.6%"} ![image](Ponton2020Efficient_figs/step_jump_10.jpg){height="9.6%"}

::: {.caption short-caption=""}
Snapshots of the experiments in scenario 3; step and jump on an obstacle
:::
::::

Finally, Fig. [29](#fig:contacts_planner){reference-type="ref" reference="fig:contacts_planner"} (bottom-left) shows the cost evolution of a contacts optimization problem ($\sum_{ \mathrm{t}            }{\indexed{ \phi                  }[cnt][ \mathrm{t}            ]}$ in blue) as well as the time required to solved it (in red) as a function of the number of iterations $\pazocal{I}$ used to approximate the dynamic constraints. These values have been normalized by the values corresponding to $\pazocal{I}           =1$, such that both curves depict the cost decrease and time increase factors relative to those that use only one iteration. Notice how initially two additional iterations ($\pazocal{I}           =3$) reduce the cost by $\sim$`<!-- -->`{=html}15% while increasing the solving time by a factor 4. Towards the end, however, an additional iteration increases the solving time linearly, but reduces the cost only minimally. This suggests that solving the problem to high-precision optimality (e.g. $\pazocal{I}           =10$) is impractical because of the large required solving time; however, a sub-optimal solution (e.g. $\pazocal{I}           =1$) is reasonable and can provide a good initialization contact plan for the motion optimization. The functional form of the cost function $\indexed{ \phi                  }[cnt][ \mathrm{t}            ]$ and importance weights are defined similarly to Table [\[tab:costfunction\]](#tab:costfunction){reference-type="ref" reference="tab:costfunction"}.

## Real robot experiments {#exp:robot_experiment}

This section presents the execution of kino-dynamic motion plans on our quadruped Solo [@grimminger2019open]. Our main goal is to demonstrate that these plans are of sufficient quality to be executed on a real robot using only an instantaneous feedback controller and no re-planning. We use a passivity based controller to track the optimized motions. The controller tracks desired CoM, angular momentum, base orientation, feet trajectories and also uses the desired feedforward centroidal wrench from the planner. This controller is described in detail in [@grimminger2019open].

We consider three different scenarios to show the capability of the planner to generate feasible motions. In the first scenario, we provide the kino-dynamic planner with a periodic sequence of contact points to generate a trotting motion. In the second scenario, we consider a jumping motion with a flight phase. Finally, in the third scenario, we present a motion that combines a non trivial sequence of contacts and a jumping motion. In all scenarios, we use the approach presented in Section [2](#sec:problem_formulation){reference-type="ref" reference="sec:problem_formulation"} and [3](#sec:opt_movement){reference-type="ref" reference="sec:opt_movement"} to generate kino-dynamically feasible motions. Note that for all the experiments we iterated only once between kinematic and dynamic optimizers. Note also that some of the motions presented here are the same motions used in [@grimminger2019open] to evaluate the control law. We reproduce them here for completeness and focus our analysis on the motion plans not discussed in [@grimminger2019open].

### Scenario 1, trot {#exp:trot}

In the first scenario, we give a periodic contact sequence to the planner, where diagonal feet move forward as much as a step length in a specified time (Fig. [30](#fig:experiments_1){reference-type="ref" reference="fig:experiments_1"}, top row). Since the robot does not have the abduction/adduction hip joint, it is very important that the planner generates stable motions taking into account the robot full dynamics and that can be tracked by the controller without step adjustment. In our experiments, we noticed the importance of having fully consistent motion plans (and not solely centroidal dynamic motions), especially during contact transitions. Furthermore, it was also important to have a feedback controller explicitly tracking desired centroidal wrench and feet trajectories. We were able to successfully execute trotting motions at various speeds. Moreover, in order to test the sensitivity of the motion plans to moderate environmental uncertainty, we planned a flat ground trot and successfully executed it on a seesaw. This result suggests that the optimized motions are neither sensitive to model mismatch nor to small environmental changes. It is particularly interesting to note that we were able to execute rather long motions of around 10 \[s\] without re-planning.

### Scenario 2, jump {#exp:jump}

To show the capability of the planner to generate highly dynamic motions, in this scenario we provide the planner with contact sequences with a flight phase. First, we implemented a jump in place (Fig. [31](#fig:experiments_2){reference-type="ref" reference="fig:experiments_2"}, top row), where the robot only needed to generate vertical thrust. In this scenario the robot was able to jump 65 cm, while the robot height in its natural standing phase is 24 cm. The generated plan is good enough such that the feedback controller is able to track desired linear momentum in the vertical direction and realize the desired jump in place. We then implemented a forward jump on an 18 cm box (Fig. [31](#fig:experiments_2){reference-type="ref" reference="fig:experiments_2"}, bottom row). In this case the planner needs to generate linear momentum in both vertical and horizontal directions to jump 60 cm forward and around 30 cm upward at the apex of the flight phase while ensuring that the generated angular momentum at take-off enables landing with the proper orientation.

### Scenario 3, step and jump on obstacle {#exp:step_jump}

In this scenario, we present a motion that is a combination of transition between different multi-contact sequences, and a flight phase for jumping on an obstacle (Fig. [32](#fig:experiments_3){reference-type="ref" reference="fig:experiments_3"}). Here, our main goal is to showcase the capability of the planner in generating highly constrained multi-contact motion together with a highly dynamic motion. To step on the obstacle, the planner exploits the high range of motion of the robot hip joint and step on the obstacle without the need to change the base orientation to avoid collision of the front legs with the obstacle. Then, through generating enough thrust on a non-coplanar set of contact points and in a non-trivial end-effectors configuration, the robot jumps on top of the obstacle. Finally, through another multi-contact set of change in contact configuration, it brings back the joint configuration to the default one. This experiment scenario further illustrates the versatility of our optimizer to generate motions in complex environments.

# Discussion {#sec:discussion}

## Time and computational complexity {#exp:time_complexity}

In general, finding a solution to the dense version of any of the convex approximations we solve, requires a polynomial time algorithm (of order ${\pazocal{O}( \nu                   ^{\frac{1}{2}}[ \nu                   + \iota                 ] \iota                 ^{2}) \approx \pazocal{O}( \nu                   ^{\frac{3}{2}})}$, $\nu$ being the number of quadratic constraints and $\iota$ its size) [@InteriorPointPTM]. However, within the problem size ranges of interest to us and thanks to the exploited problem sparsity patterns (e.g. due to time indexing), we observe (Fig. [20](#fig:conv_per_num_timesteps){reference-type="ref" reference="fig:conv_per_num_timesteps"}) that the problem has approximately linear time complexity. It is possible to note this linear tendency for both momentum and time optimization problems, despite their different rates of growth due to distinct problem sizes and even problems that consider actuation limits show this linear tendency (Fig. [27](#fig:movement_generation_statistics){reference-type="ref" reference="fig:movement_generation_statistics"}).

When considering torque limits the doubled computational effort due to the addition of ${2  \mathrm{n}             N                     }$ inequality constraints for a problem with ${ N                     }$ timesteps and robot with ${ \mathrm{n}            }$ joints ($\approx 32$ in our case) can be reduced by considering only the weakest joints or only those involved in the motion. All in all, computation times are still lower than the planned horizon, making it possible to run the algorithm online (for example the next plan can be computed, while the current one is being executed).

## On limitations and comparison of the approximations {#exp:approximation_limitations}

Problem [\[dynopt_problem\]](#dynopt_problem){reference-type="eqref" reference="dynopt_problem"} is nonconvex and thus hard to solve. The proposed heuristics lighten to some extent the effort required to find a solution by searching for an approximate one within the convex space of the problem. This however comes with certain limitations. For instance, when using trust-regions, they might be inappropriately built leading to non-optimal solutions, or even unsuitably initialized which could render the interior of the convex cone empty leading to primal infeasibility. For the soft-constraint method, the difficulty lies in finding an appropriate trade-off between two competing objectives: amount of constraint violation and problem conditioning. An adaptive solution that iteratively reduces the value of the allowed amount of constraint violation $\sigma$ works well for the trust-region heuristic, though care is required to slowly converge from the relaxed to the approximate problem without rendering the problem infeasible due to excessive reduction of $\sigma$. For the soft-constraint method, a value high enough to prioritize the soft-constraint over the rest of the cost terms works well.

We have used both methods to synthesize a relatively high number of motions, so as to be able to successfully train a neural network [@yuchi]. From this experience, we highlight that both methods work equally well. However, we would like to remark two cases where on would be more appropriate than the other. First case would be when a certificate of optimality or infeasibility matters, e.g. to compute a viable set to be used as a terminal set constraint. In this case, the trust-region method is more appropriate as the slack or degree of constraint violation is controlled using a primal constraint and the certificate is valid for the given precision. The second case would be when the solver is to be warm-started not from information from previous iterations, but using a predictive model (e.g. a neural network). In this case, the soft-constraint method would not run into the risk of infeasibility due to an invalid initialization, making it a more appropriate approach to handle this case.

Notice that a single timeline was used to parameterize and optimize motions in eq. [\[dynopt_problem\]](#dynopt_problem){reference-type="eqref" reference="dynopt_problem"}. However, this might be a limitation for more general and complex motions that require an independent timeline for each endeffector. Finally, notice that while the method is very general in nature and works well to solve problem [\[dynopt_problem\]](#dynopt_problem){reference-type="eqref" reference="dynopt_problem"}, it is the case, as with any other nonlinear optimization method such as sequential quadratic programming [@SnoptPaper], that it might not be appropriate or fail with other problem instances.

## Stability of the computed motions {#exp:stability}

Our method generates dynamically feasible motions that satisfy general contact stability criteria such as [@AdiosZMP]. If the final position of the robot has zero velocity, then we are guaranteed that the motion (if perfectly executed) will lead to a stable behavior, i.e. a behavior that will lead to the robot to stop and remain stabilized. Additionally, the construction of the feedback controllers ensures that the controlled motion will be locally stable, i.e. it will reject small perturbations. While we do not have any guarantees on the size of the region of stability, our experimental evaluations demonstrate that the motions are good enough to be executed in a simulator or on a real robot with substantially different dynamics. We noticed in our real-robot experiments that the synergy between the feedback controller and the motion plan is important and that none of them is solely responsible for a success execution of the motions, especially when executing a 10s long multi-contact motion.

Ideally, it would be desirable to use the optimizer in a receding horizon manner, raising the issue of closed-loop stability of the optimizer. Several methods have been proposed to ensure stability of model predictive control problems such as the use of a terminal equality constraint [@ocp_terminal_constraint], terminal cost [@ocp_terminal_cost], terminal constraint set [@ocp_terminal_constraint_set] or terminal cost and constraint set [@ocp_terminal_cost_and_constraint_set]. In this work, we use a terminal cost that keeps the terminal state within a viable set to generate balanced motions (see table [\[tab:costfunction\]](#tab:costfunction){reference-type="ref" reference="tab:costfunction"}). This should thus lead to closed-loop stable behaviors.

Moreover, our approach exploits sequential convex approximations (cf. section [3](#sec:opt_movement){reference-type="ref" reference="sec:opt_movement"}) to achieve polynomial-time convergence and provide a certificate of optimality or infeasibility for the motion to the desired precision. We highlight that these features do not come for free in any off-the-shelf solver. For instance, an off-the-shelf interior point method for general nonlinear problems will not take advantage of the structure of the problem as we do. This will result in a poor approximation of the non-convex constraints unable to capture the global convex part of the problem, thus leading to slower convergence. Lastly, the certificate of optimality certifies that problem constraints are satisfied to the desired precision.

## Cost definition and importance weights {#exp:cost_definition}

As pointed out throughout this work, efficiency is a key concern. Consequently, the cost function (used to synthesize motions) is composed using convex quadratic expressions, as shown in Table [\[tab:costfunction\]](#tab:costfunction){reference-type="ref" reference="tab:costfunction"}. The set of importance weights for these costs is, however, expected as an input (see Fig. [1](#fig:ExecutionArchitecture){reference-type="ref" reference="fig:ExecutionArchitecture"}), as it gives the user the flexibility to shape solutions using the knowledge about the particular robot and application. For instance, it allows to express different preferences of endeffector force distributions in humanoid and quadruped robots. Similarly, a preference for highly dynamic and aggressive motions such as jumping (Fig. [25](#fig:motion_with_flight_phases){reference-type="ref" reference="fig:motion_with_flight_phases"}) over more conservative and slow motions (Fig. [19](#fig5:movement_planning){reference-type="ref" reference="fig5:movement_planning"}) can be expressed by lower penalties over control variables. However, automatically computing appropriate cost weights to generate desired behaviors remains an open research problem.

## Comparison to other approaches {#exp:approaches_comparison}

In [@JustinMomentumOptimization], the motion and timings for a walking on stairs using a handrail scenario, given a sequence of contacts, are optimized in less than 5.5s. However, the multiple shooting solver used in this approach is closed-source to the best of our knowledge. In our approach, such a motion can be optimized in around 4.8s. In [@DBLP:conf/iros/KoenemannPTTSBM15], one iteration of a multi-contact motion of 0.5s duration can be optimized within 0.05s. Thus, extrapolating, one iteration for a 7s motion could be optimized within 0.7s. This approach, however, does not take into account hard constraints. In our approach, the cost of such an iteration is around 0.61s. In [@winkler18], a bipedal motion of 4.4s is optimized within 4.1s together with the contact sequence but uses a simplified dynamics model, assuming for example a constant locked inertia tensor at the CoM. Our method would achieve a comparable time by optimizing 4 contacts within a time horizon of 5s. Our contacts planning approach based on mixed-integer programming is competitive only for small problems that optimize a few contacts, due to the combinatorial complexity of mixed-integer programs. For longer contact sequences, other state of the art approaches are more competitive, but typically use simplified dynamics to test for contact transition feasibility [@Tonneau:2018dm; @fernbach2018croc; @lin2016using]. Note however, that the kino-dynamic optimizer can be used to generate data and learn how to predict dynamic contact feasibility and significantly speed up contact search [@yuchi].

These few examples highlight the competitiveness of the presented method while enabling the resolution of the problem without simplifications. However, we are not yet capable to compute solutions for model predictive control (e.g. at 50Hz rate or above) and thus we require a feedback controller to stabilize the motion in between plan computations. Bringing such approaches to real-time rates while enabling full-body optimization remains an open problem, likely to require the design of dedicated numerical solvers and smart warm-start procedures. Lastly, we note that the receding horizon control of whole-body motions ensuring stability, robustness and recursive feasibility, remains an open and exciting research problem.

# Conclusion {#sec:conclusion}

We have presented a structured and efficient algorithm for generating time-optimal motion plans for robots with arms and legs, as well as an approach to select a set of contact surfaces from a terrain description that supports such a motion. Finally, we have shown experimental evidence on a physical simulator and on a real quadruped robot that the algorithm is capable of efficiently generating dynamically feasible motion plans. Future work will include the extension of the algorithm to receding horizon control. The open source repository [@opensourcelink] offers fully functional kino-dynamic demos, examples of tasks descriptions and implementation details.

::: IEEEbiography
Brahayam Ponton received the B.Sc. degree in electronics and control engineering from the National Polytechnic University (EPN), Quito, Ecuador in 2011, the M.Sc degree in robotics from the Swiss Federal Institute of Technology Zürich (ETHZ), Zürich, Switzerland, in 2014 and Ph.D. degree in computer science from the Eberhard Karls Universität Tübingen, Tübingen, Germany, in 2019.
:::

::: IEEEbiography
Majid Khadiv received the B.Sc. degree in mechan- ical engineering from the Isfahan University of Tech- nology (IUT), Isfahan, Iran, in 2010, and the M.Sc. and Ph.D. degrees in mechanical engineering from the K.N. Toosi University of Technology, Tehran, Iran, in 2012 and 2017, respectively.\
He is a Postdoctoral researcher with the Movement Generation and Control Group, Max-Planck Institute for Intelligent Systems, Tübingen, Germany. He joined the Iranian National Humanoid Project, Surena III, and worked as the Head of Dynamics and Control Group from 2012 to 2015. He also spent a one-year visiting scholarship under the supervision of Prof. L. Righetti at the Autonomous Motion Laboratory, Max-Planck Institute for Intelligent Systems. His main research interest is control of legged robots.
:::

::: IEEEbiography
Avadesh Meduri received his B.E (hons) in Manufacturing Engineering from Birla Institute of Technology and Science Pilani (BITS Pilani), India in 2019. He is currently a PhD student in the Mechanical and Aerospace Engineering Department at Tandon School of Engineering, New York University, USA.\
He visited Movement Generation and Control Group at the Max-Planck Institute for Intelligent Systems to pursue his undergraduate thesis under the supervision of Prof. L. Righetti. His main research interests are contact and motion planning for legged robots.
:::

::: IEEEbiography
Ludovic Righetti (Senior Member, IEEE) received an engineering diploma in computer science and a doctorate in science from the Ecole Polytechnique Federale de Lausanne, Switzerland, in 2004 and 2008, respectively.\
He is an Associate Professor in the Electrical and Computer Engineering Department, the Mechanical and Aerospace Engineering Department and the Center for Urban Science And Progress at the Tandon School of Engineering, New York University. He is also a Senior Researcher at the Max-Planck Institute for Intelligent Systems in Germany. His research focuses on the planning and control of movements for autonomous robots, with a special emphasis on legged locomotion and manipulation.
:::

[^1]: This research was supported by New York University, the Max-Planck Society, the European Union's Horizon 2020 research and innovation programme (grant agreement No 780684 and European Research Council's grant No 637935), and the US National Science Foundation grant CMMI-1825993.

[^2]: $^{1}$ Max Planck Institute for Intelligent Systems, Tübingen - Germany

[^3]: $^{2}$ New York University, New York - USA

[^4]: Part of the material was presented at the 2018 IEEE-RAS International Conference on Robotics and Automation [@TimeOptimization]. Contribution 1 is an extension of this work, Contributions 2 and 3 are novel, Contribution 4 extends simulation results to Contribution 2 and 3 and presents real robot experiments.
