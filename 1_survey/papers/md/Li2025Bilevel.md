---
citation_key: Li2025Bilevel
arxiv_id: 2502.08697
arxiv_url: https://arxiv.org/abs/2502.08697
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-23T18:08:25Z
origin: ai+web
reviewed: false
---

# Introduction

Imitation learning has made significant recent strides [@mandlekar2023mimicgen; @chi2023diffusionpolicy; @zhao2023learning; @wang2024equivariant; @yang2024equibot], but generalization remains an open challenge, especially when new tasks require recomposing high-level concepts that are only implicit in the training data [@mao2024planning; @li2024logicity]. In Figure [\[fig:teaser\]](#fig:teaser){reference-type="ref" reference="fig:teaser"}, a robot has seen demonstrations of stepping onto a platform to grasp an object, and other demonstrations of dropping the object into a container. Now, faced with a new task where the container is also elevated, the robot should first move the two platforms appropriately, step onto one of them to grasp the object, and finally step onto the other to drop the object. Note that the platform arrangements must be completed before grasping the target, since the robot cannot move platforms with its hand full. This kind of learning and reasoning requires compositional generalization (new objects); sequential generalization (new and longer action sequences); and long-horizon planning with continuous state and action spaces with sparse feedback (goals). In sum, the robot should not just *imitate* demonstrations, but also *understand and leverage* the high-level concepts within the low-level states that are being demonstrated.

One promising direction to address these challenges is to learn and plan with *abstractions* [@li2006towards; @abel2018state; @konidaris2018symbols; @wonglearning; @curtis2022discovering; @yang2024guidinglonghorizontaskmotion; @shah2024reals]. In this work, we continue a line of recent inquiry on learning abstractions for *bilevel planning* [@silver2021operator; @silver2022skills; @silver2023predicateinvent; @chitnis2021glib; @kumar2024practice; @kumar2023predict; @liang2024visualpredicator]. In bilevel planning, continuous low-level states are mapped into a symbolic relational state space defined by *predicates* such as `Viewable(?robot,?target)` or `On(?robot,?platform)`. Planning proceeds jointly in the symbolic high-level space and the continuous low-level space. The key idea is that this hybrid planning can be more efficient and effective than reasoning solely in the low-level space.

The performance of bilevel planning depends substantially on the predicates used to define the abstract state space [@silver2023predicateinvent]. To avoid the need for a human engineer to manually define predicates for every new domain, recent work has considered *learning predicates* from data [@kulick2013active; @konidaris2018skills; @silver2023predicateinvent; @li2023embodied; @han2024interpret; @liang2024visualpredicator]. Broadly, three approaches have emerged. The most direct one relies on human feedback (labels or guidance) during the predicate learning process [@li2023embodied; @migimatsu2022grounding; @han2024interpret], which is labor-intensive and does not guarantee useful abstractions for planning [@silver2023predicateinvent]. The second approach *invents* predicates with surrogate objectives that are easy to optimize, *e.g.*, reconstruction loss [@asai2018latplan_prop; @asai2019latplan_fol; @asai2021latplanpddl] or bisimulation [@curtis2022discovering; @hansen2022bisimulation]. While these methods simplify learning, they complicate planning due to the mismatch between the surrogate objectives and the actual planning goals [@silver2023predicateinvent]. The third approach directly invents predicates for efficient planning, making planning "easy\" but learning "hard,\" as objectives like *total-planning-time* and *expected-planning-success* are difficult to optimize [@silver2023predicateinvent]. To address this, previous works have used program synthesis with classical grammars [@silver2023predicateinvent] and foundation model-based techniques [@liang2024visualpredicator; @athalye2024predicate]. However, in both cases, the predicates are invented from programmatic and pre-defined classifiers, which are limited in flexibility and scalability.

Our main contribution is b**I**le**V**el lear**N**ing from **TR**ansitions (IVNTR), the first approach capable of learning *neural* predicates that are optimized for efficient and effective bilevel planning. Since directly incorporating the planning objective into network training is challenging, our IVNTR instead constructs a candidate neural predicate pool, which is later subselected [@silver2023predicateinvent]. The key insight behind our approach is to center learning around the *effects* of predicates, which provide two major benefits: (1) they enable the derivation of supervision labels for *transition* pairs, yielding a well-structured learning objective for training the neural network; and (2) the inherent sparsity of predicate effects, combined with neural learning signals, facilitates efficient symbolic learning of their structure. To this end, IVNTR presents a novel bilevel learning framework, inspired by the structure of bilevel planning itself. Similar to the alternation between high-level symbolic search and low-level neural sampling in bilevel planning, IVNTR interleaves symbolic effect learning and neural classifier learning in an iterative process. In each iteration, the symbolic learning proposes a candidate predicate effect across different actions, which provides labels for neural learning on transition pairs. Once the neural classifier converges, its validation loss guides the symbolic learning to propose the next candidate that could minimize the loss in the new iteration. This iterative bilevel learning ultimately yields a compact set of neural predicates, which are then selected to optimize the planning objective [@silver2023predicateinvent]. The final set of invented predicates seamlessly integrates into operator and sampler learning frameworks [@chitnis2021nsrt; @silver2023predicateinvent], ultimately forming a fully functional bilevel planner.

To evaluate the effectiveness of IVNTR, we conduct extensive experiments across six diverse robot planning domains. These domains feature a wide range of low-level state representations, from SE(2) and SE(3) poses to high-dimensional point clouds. Furthermore, as shown in Figure [\[fig:teaser\]](#fig:teaser){reference-type="ref" reference="fig:teaser"}, by leveraging relational predicates and AI planning, IVNTR zero-shot generalizes to tasks with unseen entity compositions. Finally, we deploy IVNTR on a quadruped mobile manipulator (Boston Dynamics Spot) for two long-horizon mobile manipulation tasks. The learned predicates successfully abstract complex continuous states into representations compatible with the AI planner, while also providing actionable guidance for the samplers. We believe IVNTR represents a pivotal step towards learning high-level abstractions from sophisticated low-level states.

# Problem Formulation {#sec:problem}

We propose a method that uses an offline demonstration dataset to learn planning *abstractions* that generalize to test tasks with unseen objects and action compositions. In this section, we describe the formal problem setting. We follow the notation system introduced in previous work [@silver2023predicateinvent]; see Appendix [7.1](#app:notation){reference-type="ref" reference="app:notation"} for a complete notation glossary.

Planning problems are defined within a certain *planning domain* $\langle \Lambda, \mathcal{C}, f, \Psi_{\mathrm{g}}, \Psi_\mathrm{sta} \rangle$ with a task distribution $\mathcal{T}$, where we can sample a *planning task* $T\sim\mathcal{T}=\langle \mathcal{O}, \mathbf{x}_0, g\rangle$.

$\Lambda$ is a finite set of object *types* $\lambda\in\Lambda$. For example, the Climb-Transport domain depicted in Figure [1](#fig:running_example){reference-type="ref" reference="fig:running_example"} has three object types: $\Lambda=\{\mathrm{robot} (\mathtt{r}), \mathrm{platform}(\mathtt{p}), \mathrm{target}(\mathtt{t})\}$. Each type is associated with a set of *features* that characterize the state of an object of that type.[^2] For example, $\mathrm{robot}$ has features "BasePose", "HandPose", and "GripperOpenPercent", among others. A specific *task* $T$ is characterized by objects $\mathcal{O}=\{\mathtt{o}_1,\mathtt{o}_2,\cdots,\mathtt{o}_N\}$, each associated with one type in $\Lambda$. Objects are fixed within tasks but vary between tasks. The state of a task $\mathbf{x}\in\mathcal{X}$ is defined by an assignment of feature values to all objects in the task. For simplicity of exposition, we assume that a state with $N$ objects can be represented as a matrix $\mathbf{x} \in \mathbb{R}^{N\times K}$ for some domain-specific constant $K$; however, we show in experiments that our approach can be applied to more sophisticated object-centric state representations as well.

The action space for a domain is characterized by a set of $M$ *parametrized controllers* $\mathcal{C} = \{\mathtt{C}_1, \mathtt{C}_2, \cdots, \mathtt{C}_M\}$, each of which has an object type signature $(\lambda_1, \lambda_2, \cdots, \lambda_{v})$ and a continuous parameter space $\Omega$. For example, in Figure [1](#fig:running_example){reference-type="ref" reference="fig:running_example"}, `MoveToReach` has type signature $(\mathrm{robot}, \mathrm{platform})$, and continuous parameters $\Omega = \text{SE}(2)$ defining an offset 2D pose for the robot relative to the platform. A *ground action* is a controller with fully specified parameters, e.g., $\texttt{MoveToReach}(\mathtt{r}_1, \mathtt{p}_1, \omega)$ for a certain $\omega \in \Omega$. We use underline notation to represent grounding: $\underline{\mathtt{C}}$ is a certain ground action. A *lifted action* is controller with object parameter placeholders, which are typically prefixed with ?, e.g., $\texttt{MoveToReach}(\mathrm{?r}, \mathrm{?p}, \cdot)$. States and actions are related through a known transition function $f(\mathbf{x}, \underline{\mathtt{C}}) \mapsto \mathbf{x}'$, which the robot can use to plan.

A *predicate* $\psi$ is defined by an object type signature $(\lambda_1, \lambda_2, \ldots, \lambda_{u})$ and a classifier $\theta_{\psi}: \mathcal{X}\times\mathcal{O} \to \{\mathrm{True}, \mathrm{False}\}$, where $\theta_{\psi}(\mathbf{x}, (\mathtt{o}_1, \ldots, \mathtt{o}_{u}))$ evaluates the truth value of a ground predicate based on the continuous features of the input objects. For example, the predicate `In` has type signature $(\mathrm{target}, \mathrm{target})$ and a classifier that uses the poses and shapes of two targets to determine whether one is "in" the other. A *ground predicate* $\underline{\psi}$ has fully specified objects. For simplicity, we denote $\theta_{\underline{\psi}}(\mathbf{x}) \triangleq \theta_{\psi}\left(\mathbf{x}, \left(\mathtt{o}_1, \ldots, \mathtt{o}_{u}\right)\right).$ A *lifted predicate* has placeholders for objects, e.g., $\texttt{In}(\texttt{?t}, \texttt{?t})$.

Following previous work [@silver2023predicateinvent], we assume that a small set of *goal predicates* $\Psi_G$ is known and used to characterize task goals. In particular, a goal $g$ is defined by a set of ground predicates that must evaluate to True in a state for the goal to be satisfied. For example, the goal in Figure [1](#fig:running_example){reference-type="ref" reference="fig:running_example"} has only one ground predicate, $\texttt{In}(\texttt{t}_1,\texttt{t}_2)$. In this work, we make an additional assumption that any relevant *static predicates* $\Psi_\mathrm{sta}$ are known. A predicate is static if its evaluation never changes within a task (see Appendix [7.5](#app:domain_details){reference-type="ref" reference="app:domain_details"} for examples). Conversely, a predicate is *dynamic* if its evaluation could change within a task; examples are provided later in Definition [1](#def:op){reference-type="ref" reference="def:op"}.

A solution to a task is a plan $\pi=[\underline{\mathtt{C}}_1, \underline{\mathtt{C}}_2, \cdots, \underline{\mathtt{C}}_H]$, that is, a sequence of $H$ ground actions such that successive application of the transition model $\mathbf{x}_i=f\left(\mathbf{x}_{i-1}, \underline{\mathtt{C}}_i\right)$ on each $\underline{\mathtt{C}}_i \in \pi$, starting from $\mathbf{x}_0$, results in a final state $\mathbf{x}_H$ where $g$ holds. For instance, the plan depicted in Figure [\[fig:teaser\]](#fig:teaser){reference-type="ref" reference="fig:teaser"} bottom right finally leads to the state where $\texttt{In}(\texttt{t}_1,\texttt{t}_2)$ holds. In sum, to generate the plan $\pi$ for a task, in each state, the robot needs to predict: (1) the action class $\mathtt{C}\in\mathcal{C}$, (2) the objects as the discrete parameters, and (3) the continuous parameter $\omega\in\Omega$.

During training, the robot has access to an offline demonstration dataset $\mathcal{D} =\{({T}_i, \pi_i)\}_{i=1}^B$, which consists of $B$ task and solution pairs sampled from the task distribution $\mathcal{T}^\mathrm{train}$. Note that since the transition function $f$ is known and deterministic, we can also recover the intermediate states from $\mathbf{x}_0$. During test time, the robot is required to solve held-out tasks sampled from a different *test* distribution $\mathcal{T}^\mathrm{test}$. In practice, for the sake of evaluating generalization, test tasks typically contain new and more objects than training tasks. For example, as shown in Figure [1](#fig:running_example){reference-type="ref" reference="fig:running_example"}, all training tasks only have $1$ platform, but during test, there are $2$ platforms. The difference in object compositions could result in different lengths of plans with a different action order, requiring the method to *generalize* by understanding the implicit concepts present in the training demonstrations.

# Bilevel Planning {#sec:bilevel_planning}

:::: {#fig:running_example .figure latex-placement="!t"}
![](Li2025Bilevel_figs/fig2.png){width="1\\columnwidth"}

::: caption
The Climb-Transport domain is presented as a running example. We have displayed one typical training and one test task on the top. The types, actions, and provided predicates are shown at the bottom.
:::
::::

:::: {#fig:overview .figure latex-placement="!t"}
![](Li2025Bilevel_figs/fig3.png){width="2\\columnwidth"}

::: caption
\(a\) Overview of IVNTR during training. Given transition pairs in the continuous space, IVNTR invents neural predicates with different arguments parallelly, resulting in a candidate set. A subset that minimizes the planning objective $J(\cdot)$ is selected from the candidates, which serves as the final $\Psi_{\mathrm{dyn}}$. With the complete predicate set, sampler and operator learning can be achieved. (b) Bilevel planning with operators and samplers during test. Compositional ground predicates serve as inputs to the AI planner and provide guidance to the samplers.
:::
::::

In this work, we propose a method for learning predicates that can be used for *bilevel planning*. We now provide a brief review of bilevel planning and refer to other references for a more in-depth discussion [@chitnis2021nsrt; @liang2024visualpredicator; @silver2023predicateinvent; @silver2022skills; @li2023embodied; @kumar2023predict; @kumar2024practice; @silver2021operator; @garrett2021integrated].

Bilevel planning uses relational abstractions to achieve sequential and compositional generalization. The two principal abstractions are *predicates* (state abstractions) and *operators* (action abstractions). Bilevel planning also uses relational *samplers* to generate possible ground actions from operators. The key idea is that planning jointly in the abstract transition system and the low-level transition system can be much more efficient than planning in the low-level transition space only.

::: {#def:op .definition}
**Definition 1** (Operator). The *operator* for a parametrized controller $\mathtt{C}$ is a tuple, $\mathtt{Op}^\mathtt{C} = \langle \mathtt{Var}, \mathtt{Pre}, \mathtt{Eff}^+, \mathtt{Eff}^- \rangle$, where $\mathtt{Var}$ is a tuple of object placeholders matching the type signature of $\mathtt{C}$, and $\mathtt{Pre},\,\mathtt{Eff}^+,\,\mathtt{Eff}^- \subseteq \Psi$, respectively *preconditions*, *add effects*, and *delete effects*, are each a set of lifted predicates defined with variables in $\mathtt{Var}$. $\Psi$ is a predicate set.
:::

For example, the operator for $\mathtt{Grasp(?r,?t)}$ could be: $$\begin{align*}
& \mathtt{Pre}=\{\mathtt{HandEmpty(?r)},\mathtt{HandSees(?r,?t)}\},\\
& \mathtt{Eff}^+=\{\mathtt{Holding(?r,?t)}\},\\
& \mathtt{Eff}^-=\{\mathtt{HandEmpty(?r)},\mathtt{HandSees(?r,?t)}\}.
\end{align*}$$ Given a task $T = \langle \mathcal{O}, \mathbf{x}_0, g\rangle$, bilevel planning (Figure [2](#fig:overview){reference-type="ref" reference="fig:overview"}b) starts by using predicates to generate an *abstract state* consisting of all ground predicates with objects $\mathcal{O}$ whose classifiers evaluate to True in $\mathbf{x}_0$. The initial ground predicates, together with the operator set and goal $g$, can then be input to an AI planner [@helmert2006fast] to generate a plan *skeleton*, $\bar{\pi}$ with partially grounded actions with unspecified continuous parameters, $\underline{\bar{\mathtt{C}}}$. To refine the actions in this skeleton $\underline{\bar{\mathtt{C}}}\in\bar{\pi}$ into fully grounded $\underline{{\mathtt{C}}}$ with the continuous parameters $\omega$, bilevel planning leverages *samplers*.

::: definition
**Definition 2** (Sampler). The *sampler* $\eta^\mathtt{C}$ for a planning operator $\mathtt{Op}^\mathtt{C}$ with $v$ object placeholders is a conditional distribution $\omega \sim \eta^\mathtt{C}(\cdot \mid \mathbf{x}, (\mathtt{o}_1, \ldots, \mathtt{o}_{v}))$ that proposes continuous action parameters for $\mathtt{C}((\mathtt{o}_1, \ldots, \mathtt{o}_{v}), \cdot)$ given a state $\mathbf{x}$.
:::

Note that unlike the deterministic operators, samplers are usually stochastic and may fail in certain steps. Thus, bilevel planning alternates between the AI planner and samplers, using the predicate classifiers $\theta_\Psi$ as "guidance\" in each step to compensate for potential sampling failures.

Assuming we have a complete predicate set, previous work has studied the problem of learning *operators* [@chitnis2021nsrt] and *samplers* [@kumar2024practice; @silver2022skills] from the demonstration dataset $\mathcal{D}$. Since the predicates, learned operators, and samplers are *relational*, they can be generally applied to held-out test tasks sampled from $\mathcal{T}^\mathrm{test}$. However, with an insufficient predicate set---for example, with only $\Psi_\mathrm{G}$ and $\Psi_\mathrm{sta}$---bilevel planning can be intractably slow [@silver2023predicateinvent]. We next introduce the IVNTR framework, which closes this gap by automatically inventing dynamic predicates for efficient bilevel planning.

# Methodology {#sec:ivntr}

The problem of inventing dynamic predicates $\Psi_\mathrm{dyn}$ can be decomposed into *symbolic learning*---how many predicates should be invented, and with what type signatures---and *classifier learning*, determining $\theta_\psi$ for each invented predicate $\psi \in \Psi_\mathrm{dyn}$. Previous approaches [@liang2024visualpredicator; @silver2023predicateinvent] address these problems via a "define-then-select\" two-stage pipeline. In the first stage, for each predicate candidate $\hat{\psi}$ with known variable types, its classifer is pre-defined via program synthesis [@silver2023predicateinvent] or pre-trained foundation models [@liang2024visualpredicator]. These candidates form a large predicate pool $\hat{\Psi}_\mathrm{dyn}$. In the second stage, to subselect predicates from the pool, each candidate predicate set $\tilde{\Psi}_\mathrm{dyn}\subseteq\hat{\Psi}_\mathrm{dyn}$ is scored with a function $J(\tilde{\Psi}_\mathrm{dyn})$ that measures both planning *efficiency* and *effectiveness*. A key limitation of this "define-then-select" pipeline is that the classifiers within $\hat{\Psi}_\mathrm{dyn}$ are restricted to a relatively simple set. Scaling to more general classifiers, e.g., neural networks, is nontrivial, since $J(\tilde{\Psi}_\mathrm{dyn})$ is highly non-differentiable. To address this, we propose IVNTR, a "learn-then-select" approach that leverages *bilevel learning*.

As depicted in Figure [2](#fig:overview){reference-type="ref" reference="fig:overview"} (a), given the domain types $\Lambda$, IVNTR enumerates all possible typed variable compositions (with maximum input arity). Since the input features for the predicate classifier depend on its argument types, IVNTR invents predicates with different arguments group by group parallelly. For the invention of each group, IVNTR draws inspiration from bilevel planning itself, where planning alternates between the symbolic level and the low level. Similarly, IVNTR interleaves *symbolic learning* and *neural learning*, with each providing guidance for the other. Specifically, symbolic learning proposes *effect vectors* that represent the add and delete effects for candidate predicates across all operators. Neural learning uses these effect vectors to provide supervision for classifier learning. The validation loss in neural learning feeds back into symbolic learning, and the process repeats. In this section, we describe these steps in detail via the exemplar predicate group $\psi\in\Psi^{\mathtt{Var}}$, with the typed variables $\mathtt{Var}=\mathtt{(?r,?t)}$.

## Effect Vectors as Supervision for Neural Learning {#sec:neural_learning}

Suppose we had access to the symbolic components of a predicate $\psi$, but did not yet know its classifier $\theta_\psi$. Suppose further that we had knowledge of all appearances of $\psi$ in the effect sets ($\mathtt{Eff}^+, \mathtt{Eff}^-$) for each operator $\mathtt{Op}^\mathtt{C}$. We now describe how this knowledge---which we do not actually have, but which will be suggested by symbolic learning---can be used for supervised learning of the classifier $\theta_\psi$.

Recall that we have access to demonstrations $\mathcal{D}$, and for each demonstrated task $T$, we can recover the solution trajectory, $[\mathbf{x}_0,\underline{\mathtt{C}}_0,\mathbf{x}_1,\underline{\mathtt{C}}_1,\cdots,\underline{\mathtt{C}}_{H-1},\mathbf{x}_H]$. If we knew the initial state ground predicates $\underline{\psi}$ in $\mathbf{x}_0$, then we could immediately recover all ground predicates for all the states in the trajectories by chaining together the operator effects. Then, a simple binary classification framework could easily address our neural learning problem. However, we do not have access to the initial state ground predicates---we only have access to operator effects---so we do not have direct knowledge of the abstract states in the demonstration. Nonetheless, we can still provide supervision for neural learning by leveraging the ground predicates that are added, deleted, or stay unchanged in each *transition pair*. We provide this supervision by way of *predicate effect vectors*, including the *lifted effect vector* for a domain, and the *ground effect vector* for a transition.

:::: {#fig:method_1 .figure latex-placement="!t"}
![](Li2025Bilevel_figs/fig4_1.png){width="1.01\\columnwidth"}

::: caption
Detailed neural learning process for predicate $\mathtt{P2_1(?r,?t)}$. From the demonstration dataset, we display two transition pairs (one for each action, in total four states) on the left. The neural network takes object centric features as input, predicting ground predicates (in total eight values). At the bottom, we display an example lifted effect vector for action Grasp, Gaze as $\Delta^\psi_t=[+1,+1]$. With the ground effect vector, supervisions can be derived on the predicted values. Due to the unreasonable effect supervisions, the intermediate state is labeled as both `True` and `False`, resulting in high validation loss.
:::
::::

::: {#def:effect_vec .definition}
**Definition 3** (Lifted Effect Vector). The *lifted effect vector* for predicate $\psi$ is $\Delta^{\psi} = [\delta^{\psi}_{1}, \cdots, \delta^{\psi}_{M}] \in \{-1, 0, 1\}^M$ where: $$\delta^{\psi}_{i} = \begin{cases} 
      1 & \psi \in \mathtt{Eff}^+ \text{ for } \mathtt{C}_i \\
      -1 & \psi \in \mathtt{Eff}^- \text{ for } \mathtt{C}_i \\
      0 & \text{otherwise.} 
   \end{cases}$$ For example, in Figure [3](#fig:method_1){reference-type="ref" reference="fig:method_1"}, the effect vector $[+1,+1]$ specifies that predicate $\psi=\mathtt{P2_1(?r,?t)}$ is the add effect for both $\mathtt{Gaze(?r,?t)}$ and $\mathtt{Grasp(?r,?t)}$[^3].
:::

The lifted effect vector is a favorable symbolic representation of a lifted predicate, since its shape doesn't depend on task object compositions and can thus be learned more efficiently, as we will see. However, to train the neural classifier on the transition pairs, we will need to derive supervision on *ground predicates*, which is achieved by the *ground effect vector*.

::: {#def:ground_effect_vec .definition}
**Definition 4** (Ground Effect Vector). Let $\mathcal{O}$ be the object set in a task $T$, $\underline{\mathtt{C}}_i$ be a ground action with objects $\mathcal{O}_{\underline{\mathtt{C}}_i}\subseteq\mathcal{O}$, then the ground effect vector $\bm{t}^{\psi, \underline{\mathtt{C}}_i} = [t_1, \cdots, t_P] \in \{-1, 0, 1\}^P$ for predicate $\psi$ grounded on $\mathcal{O}$ is defined as: $$t_p
    \;=\;
    \begin{cases}
    \delta^{\psi}_i, 
    & \text{if } \mathcal{O}_{\underline{\psi}_p} \subseteq \mathcal{O}_{\underline{\mathtt{C}}_i}, \\
    0,     
    & \text{otherwise},
    \end{cases}$$ where $\underline{\psi}_p$ denotes the $p$-th atom with objects $\mathcal{O}_{\underline{\psi}_p}$, among the total of $P$ ground predicates. For example, in Figure [3](#fig:method_1){reference-type="ref" reference="fig:method_1"}, ground effects for $\mathtt{P2_1(r_1,t_1)}$ will be $+1$ for both ground actions $\mathtt{Gaze(r_1,t_1)}$ and $\mathtt{Grasp(r_1,t_1)}$, while ground effects for $\mathtt{P2_1(r_1,t_2)}$ will be $0$, as $\mathtt{(r_1,t_2)} \not\subseteq \mathtt{(r_1,t_1)}$.
:::

Importantly, this implies that the "value\" of the (potentially) non-zero entry of all ground effects from the action class $\mathtt{C}_i$ equals $\delta^{\psi}_i$, while the "position\" of the non-zero entry is decided by the object set $\mathcal{O}_{\underline{\mathtt{C}}}$ and the predicate grounding (see Appendix [7.2](#app:assumption){reference-type="ref" reference="app:assumption"} and Appendix [7.3](#app:same_type){reference-type="ref" reference="app:same_type"} for more explanations).

Now, we are able to train the neural classifier $\theta_\psi$ on the transition pairs with supervisions from $\Delta^\psi$. Specifically, consider a transition pair: $(\mathbf{x}, \underline{\mathtt{C}}_i, \mathbf{x}')$, we first construct the ground effect vector $\bm{t}^{\psi,\underline{\mathtt{C}}_i}$ using $\delta^\psi_i\in\Delta^\psi$. Then, the following supervised learning objective can be established for $\theta_\psi$: $$\begin{equation}
    \label{eqn:loss}
    \begin{aligned}
    \mathcal{L}(\mathbf{x}, \mathbf{x}', \theta_\psi) 
    = \mathcal{L}_\mathrm{zero} + \mathcal{L}_\mathrm{one}
    \end{aligned}
\end{equation}$$ $$\begin{equation}
    \begin{aligned}
        \hat{\mathbf{v}}, \hat{\mathbf{v}}' &= \mathrm{Ground}(\mathbf{x},\theta_\psi), \mathrm{Ground}(\mathbf{x}',\theta_\psi), 
    \end{aligned}
\end{equation}$$ $$\begin{equation}
    \label{eqn:zero-loss}
    \begin{aligned}
    \mathcal{L}_\mathrm{zero}
    = & \mathrm{Div}_\mathrm{JS}\!\Big(\hat{\mathbf{v}} \odot \mathbb{I}\big(\bm{t}^{\psi, \underline{\mathtt{C}}_i} = 0\big) \,\Big\|\, \hat{\mathbf{v}}' \odot \mathbb{I}\big(\bm{t}^{\psi, \underline{\mathtt{C}}_i}= 0\big)\Big),
    \end{aligned}
\end{equation}$$ $$\begin{equation}
    \label{eqn:non-zero-loss}
    \begin{aligned}
    \mathcal{L}_\mathrm{one}
    =  &
    \Big(\mathrm{BCE}\big([\hat{{v}}_p, \hat{{v}}'_p], [\tfrac{1 - \delta^{\psi}_{i}}{2}, \tfrac{1 + \delta^{\psi}_{i}}{2}]\Big) * \mathrm{abs}(\delta^{\psi}_{i}),
    \end{aligned}
\end{equation}$$ where $\hat{\mathbf{v}}, \hat{\mathbf{v}}'\in[0,1]^P$ are the predicted ground predicates by applying $\theta_\psi$ on all possible object sets from $\mathcal{O}$. $\mathrm{Div}_\mathrm{JS}(\cdot | \cdot)$ denotes the Jensen--Shannon divergence [@lin1991divergence] and Eq.[\[eqn:zero-loss\]](#eqn:zero-loss){reference-type="eqref" reference="eqn:zero-loss"} tries to minimize the distance between $\hat{\mathbf{v}}$ and $\hat{\mathbf{v}}'$ if the indices with zero values in $\bm{t}^{\psi, \underline{\mathtt{C}}}$. $\hat{{v}}_p,\hat{{v}}_p'$ denotes $p$-th ground predicate, where $\mathcal{O}_{\underline{\psi}_p} \subseteq \mathcal{O}_{\underline{\mathtt{C}}_i}$. $\mathrm{BCE}(\cdot,\cdot)$ represents the Binary Cross-Entropy, which tries to directly supervise $\hat{\mathbf{v}}$ and $\hat{\mathbf{v}}'$ if $\delta^{\psi}_{i}\neq 0$. Intuitively, $\mathcal{L}_\mathrm{zero}$ supervises the ground predicates whose values should stay unchanged in a transition (but we don't know their values). $\mathcal{L}_\mathrm{one}$, on the other hand, supervises the ground predicates whose values can be derived based on the effect vectors. Since we have $\Delta^\psi$ for all lifted actions, the pipeline can be applied to all ground transition pairs in $\mathcal{D}$, resulting in the global loss, $$\begin{equation}
\label{eqn:global_loss}
    \mathcal{L}^{\mathcal{D}}(\theta_\psi)
    = \sum_{\mathtt{C}\in\mathcal{C}} \mathbb{E}_{(\mathbf{x},\underline{\mathtt{C}},\mathbf{x'})\sim\mathcal{D}_\mathtt{C}}\mathcal{L}(\mathbf{x}, \mathbf{x}', \theta_\psi),
\end{equation}$$ where $\mathcal{D}_\mathtt{C}$ denotes the distribution of the grounded transition for action $\mathtt{C}$ in the dataset $\mathcal{D}$ (See Figure [3](#fig:method_1){reference-type="ref" reference="fig:method_1"} for the examples of two transitions from different actions). Since $\mathcal{L}$ is fully differentiable with respect to $\theta$, given a effector $\Delta^{\psi}$ and the demonstration dataset, we could leverage the general and standard deep learning frameworks [@kingma2014adam; @rumelhart1986sgd] to train a neural classifier $\theta$ that minimizes the loss $\mathcal{L}$ for any state representation.

## Neural Loss as Guidance for Symbolic Learning

To obtain all the classifiers $\theta_{\Psi^{\mathtt{Var}}}$ for all the typed predicates $\psi\in\Psi^{\mathtt{Var}}$, the problem now becomes finding all the lifted effect vectors $\Delta^\psi\in\Delta^{\Psi^{\mathtt{Var}}}$. As defined in Definition [3](#def:effect_vec){reference-type="ref" reference="def:effect_vec"}, the lifted effect vectors live in the discrete world with a finite shape, which motivates us to establish some discrete optimization strategies for it. One insight here is that, despite the large space, only a few effect vectors provide reasonable supervision, with unreasonable ones resulting in high classification error on the validation set after the training converges.

A motivating example is depicted in Figure [3](#fig:method_1){reference-type="ref" reference="fig:method_1"}, where the proposed effect vector assumes the predicate to be the add effects for both $\mathtt{Gaze}$ and $\mathtt{Grasp}$. In the demonstration, $\mathtt{Grasp}$ closely follows $\mathtt{Gaze}$, making the intermediate state shared in the two transition pairs but with one being the next state and the other being the current state. Then, the intermediate state will be labeled as both $\mathtt{True}$ and $\mathtt{False}$, which is unreasonable and results in high classification error. Thus, our symbolic learning aims to efficiently find all "reasonable\" effect vectors,

::: definition
**Definition 5** (Symbolic Learning Objective). Let the demonstrations be split into non-overlapping training and validation sets $\mathcal{D} = \mathcal{D}^\text{train} \cup \mathcal{D}^\text{val}$, the objective of our symbolic learning is to find a subset of effect vectors $\Delta^{*,\Psi^{\mathtt{Var}}} \subset \Delta^{\Psi^{\mathtt{Var}}}$, $$\begin{equation}
\label{eqn:search_obj}
        \Delta^{*,\Psi^{\mathtt{Var}}} = \left\{ \Delta^\psi \in \Delta^{\Psi^{\mathtt{Var}}} \mid \mathcal{L}^{\mathcal{D}^\text{val}}(\theta_\psi) \leq \tau \right\},
\end{equation}$$ where $\theta^\psi$ is learned from $\mathcal{D}^\text{train}$ with supervision derived from $\Delta^\psi$ using Eq. [\[eqn:global_loss\]](#eqn:global_loss){reference-type="eqref" reference="eqn:global_loss"}, and $\mathcal{L}^{\mathcal{D}^\text{val}}$ denotes the validation loss of classifier $\theta^\psi$ calculated from Eq. [\[eqn:global_loss\]](#eqn:global_loss){reference-type="eqref" reference="eqn:global_loss"}, and $\tau$ is a given threshold.
:::

Inspired by the fact that a predicate's effects are usually sparse among actions, we propose a tree expansion algorithm for efficiently learning $\Delta^{*,\Psi^{\mathtt{Var}}}$. Specifically, as shown in Figure [4](#fig:method_2){reference-type="ref" reference="fig:method_2"} (with $M=4$ actions), the complete effect vector set, $\Delta^{\Psi^{\mathtt{Var}}}$, is formulated into a tree-like structure, with each node $\Delta^{\psi_n}\in\Delta^{\Psi^{\mathtt{Var}}}, n>0$ representing an effect vector. The root $\Delta^{0}$ of the tree is an "all-zero\" effect vector, which is not associated with any potential *dynamic* predicate. The nodes in the $l-$th level represent a vector with $l$ non-zero entries. For each non-leaf node in the $l-$th level, its "children\" in the $l+1$-th level have the same non-zero entries with one more non-zero entry. A naive exploration in this tree is to enumerate its nodes and train neural classifiers with supervisions from each of them, which is extremely time-consuming due to the large space. To explore the effect tree more efficiently, IVNTR tries to balance the trade-off between *exploration* and *exploitation* [@coulom2006mcts; @silver2017alphago].

:::: {#fig:method_2 .figure latex-placement="!t"}
![](Li2025Bilevel_figs/fig4_2.png){width="0.9\\columnwidth"}

::: caption
Detailed symbolic learning process for predicate group $\texttt{P2(?r,?t)}$. With the neural validation loss from the previous iteration, symbolic learning starts by merging the loss into the global value vector (See Eq. (7)). After the node values in the effect tree are updated, we conduct parent node selection and expansion. Among the children nodes, we evaluate the child with the current highest value, via the neural classifer training process described in Figure [3](#fig:method_1){reference-type="ref" reference="fig:method_1"}.
:::
::::

Specifically, each node $\Delta^{\psi_n}$ in the tree is additionally associated with a scalar $r^n_t$, indicating its value for finding $\Delta^\psi \in\Delta^{*,\Psi^{\mathtt{Var}}}$ if we expand it at the current $t$-th iteration. In the $t$-th iteration, we start by selecting a parent node $\mathrm{Par}(\Delta^{\psi}_t)$ with the highest current Upper Confidence bounds applied to Trees (UCT) score [@silver2017alphago]. Its child, $\Delta^{\psi}_t$ that has the current highest value $r_t$ among all the children is proposed for evaluation (index is neglected for simplicity). The evaluation process is defined as the supervised neural learning process in Section [4.1](#sec:neural_learning){reference-type="ref" reference="sec:neural_learning"}. After the classifier $\theta^{\psi}$ converges, we collect its *action-wise* validation loss $\mathbf{L}_t\in\mathbb{R}^M$ by decomposing Eq. [\[eqn:global_loss\]](#eqn:global_loss){reference-type="eqref" reference="eqn:global_loss"} for each action $\mathtt{C}\in\mathcal{C}, |\mathcal{C}|= M$. The loss information is then used to update the values of all the nodes in the tree, which helps us select and expand the parent node in the $t+1$-th iteration. The tree expansion terminates if all of the existing nodes are fully expanded, or, if the max iteration has been reached.

:::: {#fig:domains .figure latex-placement="!t"}
![](Li2025Bilevel_figs/fig5.png){width="1.8\\columnwidth"}

::: caption
Visualization of the five domains (excluding Climb-Transport) we have studied in this work. These domains feature various state representations (including the high-dimensional point clouds in the Engrave domain) where our IVNTR can be generally applied.
:::
::::

::: table*
+:------------------------------------:+:----------------------------:+:---------------------------:+:----------------------:+:----------------------------:+:---------------------------:+:----------------------:+:----------------------------:+:---------------------------:+:----------------------:+:----------------------------:+:---------------------------:+:----------------------:+:----------------------------:+:---------------------------:+:----------------------:+:----------------------------:+:---------------------------:+:----------------------:+
| Domain                               | Satellites [@kumar2023predict]                                                      | Blocks [@chitnis2021nsrt]                                                           | Measure-Mul                                                                         | Climb-Measure                                                                       | Climb-Transport                                                                     | Engrave                                                                             |
+--------------------------------------+-------------------------------------------------------------------------------------+-------------------------------------------------------------------------------------+-------------------------------------------------------------------------------------+-------------------------------------------------------------------------------------+-------------------------------------------------------------------------------------+-------------------------------------------------------------------------------------+
| State Space                          | SE2 ($\mathbb{R}^{3\times5}$)                                                       | Vec3 ($\mathbb{R}^{3\times8}$)                                                      | SE3 ($\mathbb{R}^{7\times5}$)                                                       | SE3 ($\mathbb{R}^{7\times5}$)                                                       | SE3 ($\mathbb{R}^{7\times5}$)                                                       | PCD ($\mathbb{R}^{1024\times3\times6}$)                                             |
+--------------------------------------+------------------------------+-----------------------------+------------------------+------------------------------+-----------------------------+------------------------+------------------------------+-----------------------------+------------------------+------------------------------+-----------------------------+------------------------+------------------------------+-----------------------------+------------------------+------------------------------+-----------------------------+------------------------+
| Test Dist                            | $\mathcal{T}^\mathrm{train}$ | $\mathcal{T}^\mathrm{test}$ | $\downarrow$           | $\mathcal{T}^\mathrm{train}$ | $\mathcal{T}^\mathrm{test}$ | $\downarrow$           | $\mathcal{T}^\mathrm{train}$ | $\mathcal{T}^\mathrm{test}$ | $\downarrow$           | $\mathcal{T}^\mathrm{train}$ | $\mathcal{T}^\mathrm{test}$ | $\downarrow$           | $\mathcal{T}^\mathrm{train}$ | $\mathcal{T}^\mathrm{test}$ | $\downarrow$           | $\mathcal{T}^\mathrm{train}$ | $\mathcal{T}^\mathrm{test}$ | $\downarrow$           |
+--------------------------------------+------------------------------+-----------------------------+------------------------+------------------------------+-----------------------------+------------------------+------------------------------+-----------------------------+------------------------+------------------------------+-----------------------------+------------------------+------------------------------+-----------------------------+------------------------+------------------------------+-----------------------------+------------------------+
| Oracle                               | 100.0                        | 100.0                       | 0.00                   | 100.0                        | 100.0                       | 0.00                   | 100.0                        | 100.0                       | 0.00                   | 90.0                         | 81.6                        | 0.09                   | 91.2                         | 82.0                        | 0.10                   | 100.0                        | 100.0                       | 0.00                   |
+--------------------------------------+------------------------------+-----------------------------+------------------------+------------------------------+-----------------------------+------------------------+------------------------------+-----------------------------+------------------------+------------------------------+-----------------------------+------------------------+------------------------------+-----------------------------+------------------------+------------------------------+-----------------------------+------------------------+
| **IVNTR (Ours)**                     | [**99.2**]{.underline}       | [**93.2**]{.underline}      | [**0.06**]{.underline} | [**100.0**]{.underline}      | [**82.0**]{.underline}      | [**0.18**]{.underline} | [**90.0**]{.underline}       | [**88.4**]{.underline}      | [**0.02**]{.underline} | [**91.6**]{.underline}       | [**65.6**]{.underline}      | [**0.28**]{.underline} | [**79.2**]{.underline}       | [**53.2**]{.underline}      | [**0.33**]{.underline} | [**98.4**]{.underline}       | [**79.2**]{.underline}      | [**0.20**]{.underline} |
+--------------------------------------+------------------------------+-----------------------------+------------------------+------------------------------+-----------------------------+------------------------+------------------------------+-----------------------------+------------------------+------------------------------+-----------------------------+------------------------+------------------------------+-----------------------------+------------------------+------------------------------+-----------------------------+------------------------+
| GNN [@battaglia2018gnn]              | 74.0                         | 6.0                         | 0.92                   | 82.4                         | 24.0                        | 0.71                   | 2.4                          | 1.2                         | 0.50                   | 20.8                         | 0.7                         | 0.97                   | 48.0                         | 2.0                         | 0.96                   | 0.0                          | 0.0                         | 1.00                   |
+--------------------------------------+------------------------------+-----------------------------+------------------------+------------------------------+-----------------------------+------------------------+------------------------------+-----------------------------+------------------------+------------------------------+-----------------------------+------------------------+------------------------------+-----------------------------+------------------------+------------------------------+-----------------------------+------------------------+
| Transformer [@vaswani2017tf]         | 46.8                         | 1.2                         | 0.97                   | 24.4                         | 7.6                         | 0.69                   | 10.0                         | 2.4                         | 0.76                   | 29.2                         | 0.0                         | 1.00                   | 10.4                         | 0.8                         | 0.92                   | 0.0                          | 0.0                         | 1.00                   |
+--------------------------------------+------------------------------+-----------------------------+------------------------+------------------------------+-----------------------------+------------------------+------------------------------+-----------------------------+------------------------+------------------------------+-----------------------------+------------------------+------------------------------+-----------------------------+------------------------+------------------------------+-----------------------------+------------------------+
| FOSAE [@asai2019latplan_fol]         | 100.0                        | 34.8                        | 0.65                   | 2.4                          | 0.4                         | 0.83                   | 3.6                          | 1.2                         | 0.67                   | 21.2                         | 0.0                         | 1.00                   | 45.6                         | 0.8                         | 0.98                   | 0.0                          | 0.0                         | 1.00                   |
+--------------------------------------+------------------------------+-----------------------------+------------------------+------------------------------+-----------------------------+------------------------+------------------------------+-----------------------------+------------------------+------------------------------+-----------------------------+------------------------+------------------------------+-----------------------------+------------------------+------------------------------+-----------------------------+------------------------+
| Grammar [@silver2023predicateinvent] | 0.0                          | 0.0                         | 1.00                   | 0.0                          | 0.0                         | 1.00                   | 0.0                          | 0.0                         | 1.00                   | 0.0                          | 0.0                         | 1.00                   | 0.0                          | 0.0                         | 1.00                   | N/A                          | N/A                         | N/A                    |
+--------------------------------------+------------------------------+-----------------------------+------------------------+------------------------------+-----------------------------+------------------------+------------------------------+-----------------------------+------------------------+------------------------------+-----------------------------+------------------------+------------------------------+-----------------------------+------------------------+------------------------------+-----------------------------+------------------------+
| Random                               | 0.0                          | 0.0                         | 1.00                   | 10.6                         | 1.2                         | 0.89                   | 0.0                          | 0.0                         | 1.00                   | 0.0                          | 0.0                         | 1.00                   | 0.0                          | 0.0                         | 1.00                   | 0.0                          | 0.0                         | 1.00                   |
+--------------------------------------+------------------------------+-----------------------------+------------------------+------------------------------+-----------------------------+------------------------+------------------------------+-----------------------------+------------------------+------------------------------+-----------------------------+------------------------+------------------------------+-----------------------------+------------------------+------------------------------+-----------------------------+------------------------+
:::

Clearly, the key to more efficient learning lies in the definition and updating strategy of the node values $r^n_t$. As the sparsity of predicate effects among actions is indicated by the sparsity of non-zero entries in the effect vector, we try to efficiently explore the entries in the effect vectors that **should not** be zero to optimize Eq. [\[eqn:search_obj\]](#eqn:search_obj){reference-type="eqref" reference="eqn:search_obj"}. To achieve this, we try to leverage the guidance from the "zero-parts\" (Eq. [\[eqn:zero-loss\]](#eqn:zero-loss){reference-type="eqref" reference="eqn:zero-loss"}) of $\mathbf{L}_t$. Specifically, after the evaluation of the node $\Delta^{\psi}_t$ in the $t-$th iteration with $\mathbf{L}_t$, we use the following equations to update and compute $r^n_{t+1}$ for all the nodes in the tree, $$\begin{equation}
\label{eqn:update}
    \begin{aligned}
    \mathbf{R}_{t+1} &= 
    \mathbf{R}_{t} \odot \mathbb{I}(\Delta^{\psi}_t \neq 0) 
    + \frac{(\mathbf{R}_{t} + \mathbf{L}_t)}{2} \odot \mathbb{I}(\Delta^{\psi}_t = 0). \\
        r^n_{t+1} &= \mathrm{Mean}\big(\mathbf{R}_{t+1} \odot \mathbb{I}(\Delta^{\psi_n} = 0)\big),
    \end{aligned}
\end{equation}$$ where $\mathbf{R}_{t}\in\mathbb{R}^M, \mathbf{R}_0=\mathbf{0}^M$ is a global value vector that stores the information from historical evaluations. $\mathbb{I}(\Delta^{\psi}_t = 0)$ is a binary vector indicating if an entry in the evaluated node $\Delta^{\psi}_t$ equals to zero. Here, we only update $\mathbf{R}_{t}$ with the "zero-parts\" of the loss information $\mathbf{L}_t$, which then helps update the node values. The node values intuitively indicate how likely the loss will decrease in its children where there are fewer zeros in the effect vectors. From Eq. [\[eqn:update\]](#eqn:update){reference-type="eqref" reference="eqn:update"}, we see that the higher loss in the zero entry indexes of $\Delta^{\psi_n}$ contributes to its higher value, encouraging the evaluation to prioritize its children, which are likely to decrease the loss. In Appendix [7.4](#app:pruning){reference-type="ref" reference="app:pruning"}, we additionally introduce some pruning strategy for more efficient expansion.

Finally, we collect all the effect vectors $\Delta^{\psi_n}\in\Delta^{*,\Psi^{\mathtt{Var}}}$ with the associated neural classifier $\theta_{\psi_n}$ as the outcomes from the bilevel learning of typed predicates $\Psi^{\mathtt{Var}}$. As shown in Figure [2](#fig:overview){reference-type="ref" reference="fig:overview"} (a), there could exist multiple different vector-classifier pairs for the same typed predicate $\Psi^{\mathtt{Var}}$, which are treated as different predicates in the following predicate selection stage.[^4]

## Predicate Selection

With all possible typed predicates, IVNTR is able to construct the predicate pool $\hat{\Psi}_{\mathrm{dyn}}$ without any classifier pre-definition. This strength has made bilevel planning applicable to complicated and high-dimensional state spaces. Meanwhile, as the predicate classifiers are *relational* and can be seamlessly integrated into an AI planner [@helmert2006fast], our approach can naturally achieve compositional generalization.

Yet, not all of the predicates in $\hat{\Psi}_{\mathrm{dyn}}$ are favorable for planning. Therefore, we next try to select a subset $\tilde{\Psi}_{\mathrm{dyn}}\subset\hat{\Psi}_{\mathrm{dyn}}$ that minimizes the score function $J(\tilde{\Psi}_{\mathrm{dyn}},
\mathcal{D})$ [@silver2023predicateinvent]. Specifically, with a set of candidate predicates $\tilde{\Psi} = \{\Psi_\mathrm{G},\Psi_\mathrm{sta}, \tilde{\Psi}_{\mathrm{dyn}}\}$, we start by grounding all the states $\mathbf{x}$ in the demonstration $\mathcal{D}$, which forms a ground atom dataset. Since we already have the effect vector for each of the predicates in $\tilde{\Psi}_{\mathrm{dyn}}$, the effect sets ($\tilde{\mathtt{Eff}}^+, \tilde{\mathtt{Eff}}^-\subset \tilde{\Psi}_{\mathrm{dyn}}$) for each operator $\tilde{\mathtt{Op}}^\mathtt{C}$ can be easily obtained. Then, the precondition set for each operator can be calculated using an intersection strategy [@chitnis2021nsrt]. The learned operator set $\tilde{\mathtt{Op}}$ is then applied to the ground atom dataset to generate plan *skeletons* $\tilde{\pi}$ for each task, which are compared with the demonstration plan *skeletons* $\bar{\pi}$ for objective calculation [@silver2023predicateinvent]. The objective is finally minimized by running a hill-climbing search over $\hat{\Psi}_{\mathrm{dyn}}$, resulting in the desired predicate set ${\Psi}_{\mathrm{dyn}}$. With the complete set, we are now able to learn the planning *abstractions* (operators and samplers) using standard pipelines [@chitnis2021nsrt; @kumar2023predict; @liang2024visualpredicator] as shown in Figure [2](#fig:overview){reference-type="ref" reference="fig:overview"} (a). For a more detailed explanation to operator and sampler learning, please see Appendix Appendix [7.11](#app:op_sam_learning){reference-type="ref" reference="app:op_sam_learning"}.

Note that before the predicate selection stage, all of the predicates' neural classifiers have been pre-trained using our IVNTR framework, which has avoided the challenge of using the planning objective for learning but still achieved a powerful and adaptive model optimized for planning.

# Experiments

::: table*
+:-------------------:+:---------:+:------:+:------:+:------:+:------:+:------:+:------:+:------:+:------:+:----:+:----:+:----:+:----:+:---:+:----:+:-----:+:-----:+
|                     |           | Climb-Measure                                                         | Climb-Transport                                |       |
+---------------------+-----------+--------+--------+--------+--------+--------+--------+--------+--------+------+------+------+------+-----+------+-------+-------+
| Planner             | Seed/Task | T0     | T1     | T2     | T3     | T4     | T5     | Mean   | Avg.   | T0   | T1   | T2   | T3   | T4  | T5   | Mean  | Avg.  |
+---------------------+-----------+--------+--------+--------+--------+--------+--------+--------+--------+------+------+------+------+-----+------+-------+-------+
| Oracle (Human)      | S0        | 0.0    | 1.0    | 1.0    | 1.0    | 0.5    | 1.0    | 0.750  | 0.833  | 0.5  | 0.0  | 1.0  | 1.0  | 1.0 | 1.0  | 0.750 | 0.592 |
|                     +-----------+--------+--------+--------+--------+--------+--------+--------+        +------+------+------+------+-----+------+-------+       |
|                     | S1        | 1.0    | 1.0    | 1.0    | 0.5    | 1.0    | 0.5    | 0.833  |        | 1.0  | 1.0  | 0.33 | 0.5  | 0.5 | 0.5  | 0.638 |       |
|                     +-----------+--------+--------+--------+--------+--------+--------+--------+        +------+------+------+------+-----+------+-------+       |
|                     | S2        | 1.0    | 1.0    | 1.0    | 1.0    | 1.0    | 0.5    | 0.917  |        | 0.5  | 0.33 | 0.5  | 0    | 0.5 | 0.5  | 0.388 |       |
+---------------------+-----------+--------+--------+--------+--------+--------+--------+--------+--------+------+------+------+------+-----+------+-------+-------+
| **IVNTR (Learned)** | S0        | 1.0    | 1.0    | 0.5    | 0.0    | 1.0    | 1.0    | 0.750  | 0.778  | 0.5  | 1.0  | 0    | 0.5  | 1.0 | 0.33 | 0.555 | 0.546 |
|                     +-----------+--------+--------+--------+--------+--------+--------+--------+        +------+------+------+------+-----+------+-------+       |
|                     | S1        | 1.0    | 1.0    | 1.0    | 1.0    | 1.0    | 0.0    | 0.833  |        | 0.33 | 0.5  | 1.0  | 0.33 | 0   | 0.5  | 0.443 |       |
|                     +-----------+--------+--------+--------+--------+--------+--------+--------+        +------+------+------+------+-----+------+-------+       |
|                     | S2        | 0.5    | 1.0    | 1.0    | 1.0    | 0.0    | 1.0    | 0.750  |        | 0.5  | 0.5  | 1.0  | 1.0  | 0.5 | 0.33 | 0.638 |       |
+---------------------+-----------+--------+--------+--------+--------+--------+--------+--------+--------+------+------+------+------+-----+------+-------+-------+
:::

::: {#tab:abla_gt_vec}
+:----------:+:----------------------------:+:---------------------------:+:-------------------------:+:----------------------------:+:---------------------------:+:-------------------------:+
| Domains    | Blocks                                                                                 | Climb-Measure                                                                          |
+------------+------------------------------+-----------------------------+---------------------------+------------------------------+-----------------------------+---------------------------+
| Metric     | $\mathcal{T}^\mathrm{train}$ | $\mathcal{T}^\mathrm{test}$ | $J(\cdot)$ ($\times10^5$) | $\mathcal{T}^\mathrm{train}$ | $\mathcal{T}^\mathrm{test}$ | $J(\cdot)$ ($\times10^5$) |
+------------+------------------------------+-----------------------------+---------------------------+------------------------------+-----------------------------+---------------------------+
| GT-Vectors | 80.0                         | 62.8                        | 121.59                    | 90.4                         | 61.2                        | 2.718                     |
+------------+------------------------------+-----------------------------+---------------------------+------------------------------+-----------------------------+---------------------------+
| **IVNTR**  | **100.0**                    | **82.0**                    | **56.77**                 | **91.6**                     | **65.6**                    | **2.481**                 |
+------------+------------------------------+-----------------------------+---------------------------+------------------------------+-----------------------------+---------------------------+

: Comparison between the predicates learned with ground-truth (GT)-vectors and using our IVNTR framework. We report the task success rate and the final planning objective.
:::

## Implementation Details

**System and Hardware:**  All methods are evaluated on a single NVIDIA A100 GPU and an AMD EPYC 7543 32-Core CPU to ensure fairness. Training is conducted on the same hardware as evaluation, with domain-specific details provided in Appendix [7.5](#app:domain_details){reference-type="ref" reference="app:domain_details"}. Real-robot experiments are performed using the Boston Dynamics Spot robot equipped with an arm.

**Baselines:**  Since we do not assume access to the complete predicate set, most existing bilevel planning approaches [@chitnis2021nsrt; @kumar2023predict; @kumar2024practice] are inapplicable. We attempted the grammar-based approach [@silver2023predicateinvent], but it failed to optimize the planning objective in most domains (see Appendix [7.10](#app:objective){reference-type="ref" reference="app:objective"}). Thus, IVNTR is primarily compared to relational neural policy learning methods [@battaglia2018gnn; @vaswani2017tf; @asai2019latplan_fol]. Following prior works [@kumar2023predict; @chitnis2021nsrt; @silver2023predicateinvent; @silver2022skills], baselines are trained using standard behavior cloning pipelines and evaluated with a shooting strategy; see Appendix [7.6](#app:baseline_details){reference-type="ref" reference="app:baseline_details"} for details.

**Domains:**  We evaluate the methods across six diverse robot planning domains with varying state representations, as visualized in Figure [5](#fig:domains){reference-type="ref" reference="fig:domains"} and summarized in Table [\[tab:sim_emp\]](#tab:sim_emp){reference-type="ref" reference="tab:sim_emp"}. Below, we provide a high-level overview of these domains. For more implementation details, please refer to Appendix [7.5](#app:domain_details){reference-type="ref" reference="app:domain_details"}:

- *Satellites* comes from prior work [@kumar2023predict], which involves a group of satellites collaborating to capture sensor readings from targets. States comprise SE2 poses and object attributes. Training scenarios ($\mathcal{T}^\mathrm{train}$) include 2 satellites and 2 targets, while test scenarios ($\mathcal{T}^\mathrm{test}$) have 3 of each.

- *Blocks:* Inspired by [@chitnis2021nsrt], this domain tasks a robot with manipulating 3D blocks to form goal towers. Unlike vanilla Blocks World, the goals here involve "packing\" pairs of blocks into two-level towers. $\mathcal{T}^\mathrm{train}$ includes 4--5 blocks, while $\mathcal{T}^\mathrm{test}$ features 6--7 blocks.

- *Measure-Mul:* In this new domain inspired by Satellites, a Spot robot calibrates a thermal camera by aligning it with a calibrator before measuring body temperatures of multiple human targets. States include 6D poses of the robot and the targets. Training distributions ($\mathcal{T}^\mathrm{train}$) have 2--3 humans, while test distributions ($\mathcal{T}^\mathrm{test}$) include 4.

- *Climb-Measure* is similar to Measure-Mul but with added complexity: calibrators and human targets may be placed at high, initially unreachable locations. The Spot robot must arrange platforms and climb onto them to reach targets. Training ($\mathcal{T}^\mathrm{train}$) includes 0--1 platforms, while testing ($\mathcal{T}^\mathrm{test}$) requires planning with 2 platforms.

- *Climb-Transport:* Introduced in Figure [1](#fig:running_example){reference-type="ref" reference="fig:running_example"}, this domain requires the Spot robot to arrange platforms to grasp a high-placed target, then transport it into a container. Training setups ($\mathcal{T}^\mathrm{train}$) feature 0--1 platforms, while testing ($\mathcal{T}^\mathrm{test}$) involves 2 platforms.

- *Engrave* features high-dimensional state spaces represented as object-centric point clouds. Similar to Blocks, the goal is to "pack\" blocks. However, blocks start with one irregular Gaussian surface that must be "engraved\" and "rotated\" to create a matching fit. Training distributions ($\mathcal{T}^\mathrm{train}$) include 3--4 blocks, while testing ($\mathcal{T}^\mathrm{test}$) has 5--6.

**Experiment Setup:**  For each domain, we manually designed an oracle bilevel planner (Oracle) to collect training demonstrations. We report averaged results over five random seeds for all six domains. For each seed in Satellites, Blocks, Measure-Mul, and Engrave, we have collected $500$ demonstrations. For Climb-Measure and Climb-Transport, $2000$ demonstrations were collected per seed. During test, each seed in each domain includes $50$ in-domain tasks ($T\sim\mathcal{T}^\mathrm{train}$) and $50$ generalization tasks ($T\sim\mathcal{T}^\mathrm{test}$). We report the success rate within the same maximum planning time for all the methods. For real-world Climb-Measure and Climb-Transport, a shared map was recorded using Spot's default graph_nav service for simulation and localization. Each domain was tested on $3$ random seeds, each with $6$ generalized tasks. For manipulation-based actions, we have utilized an off-the-shelf segment anything model (SAM) [@lang_sam; @ravi2024sam] for computing the grasping pixel.

::: {#tab:abla_highlevel}
+:----------------------------:+:--------:+:----:+:------------:+:--------:+:-----:+:------------:+
| Domains                      | Satellites                     | Measure-Mul                     |
+------------------------------+----------+------+--------------+----------+-------+--------------+
| Sampling with $\theta^\psi$  |          |      | $\downarrow$ |          |       | $\downarrow$ |
+------------------------------+----------+------+--------------+----------+-------+--------------+
| $\mathcal{T}^\mathrm{train}$ | **99.2** | 74.0 | 0.254        | **90.0** | 2.8   | 0.969        |
+------------------------------+----------+------+--------------+----------+-------+--------------+
| $\mathcal{T}^\mathrm{test}$  | **93.2** | 16.8 | 0.820        | **88.4** | 1.4   | 0.984        |
+------------------------------+----------+------+--------------+----------+-------+--------------+

: Comparison between sampling with and without the invented predicate classifiers. Without using the predicates as step-wise success indicator, the performance drops significantly.
:::

## Empirical Results

**Simulated Planning Domains:**  The empirical comparison across the six simulated domains is presented in Table [\[tab:sim_emp\]](#tab:sim_emp){reference-type="ref" reference="tab:sim_emp"}. Alongside the averaged success rates, we report the performance drop percentage during generalization. IVNTR consistently outperforms all baselines in both $\mathcal{T}^\mathrm{train}$ and $\mathcal{T}^\mathrm{test}$ across all domains. For complex state representations such as SE3 and PointClouds (PCD), none of the baselines achieve a success rate above $5\%$ on generalized tasks, while IVNTR stably solves over $50\%$ by virtue of its relational structure. In Appendix [7.12](#app:blocks_img){reference-type="ref" reference="app:blocks_img"}, we further demonstrate the potential of IVNTR to abstract high-dimensional RGB image states into symbolic predicates.

**Real Robot Planning Tasks:**  All real robot tasks are sampled from $\mathcal{T}^\mathrm{test}$, making IVNTR the only applicable approach. To benchmark performance, a human expert has exhaustively engineered oracle planners for the real robot in the two domains. Each approach attempts each task up to three times, with the average success rate reported in Table [\[tab:real_emp\]](#tab:real_emp){reference-type="ref" reference="tab:real_emp"}. Despite the simulation-to-reality gap, IVNTR successfully generalizes to held-out tasks, achieving results comparable to the oracle planner. Most real-world deployment failures stem from perception and localization errors, with examples shown in Appendix [7.7](#app:failures){reference-type="ref" reference="app:failures"}.

## Ablation Studies

**Comparison to Ground-Truth Effect Vectors:**  A notable strength of IVNTR is its ability to discover non-ground-truth (GT) predicates. In Table [1](#tab:abla_gt_vec){reference-type="ref" reference="tab:abla_gt_vec"}, we replaced our tree expansion with oracle-derived GT effect vectors, where the performance on the Blocks and Climb-Measure domains are reported. Interestingly, IVNTR minimizes the planning objective more effectively than GT vectors, resulting in its higher accuracy. This outcome highlights the advantage of exploring better high-level abstractions beyond human-engineered ones.

**Comparison to Other Search Algorithms:**  To evaluate the efficiency of our neural-informed tree expansion algorithm, we compared it with alternative search strategies: a greedy approach (Greedy) that flips the zero entry with the highest current loss, breadth-first (BFS) and depth-first (DFS) searches. For the Engrave domain, Figure [6](#fig:abla_search){reference-type="ref" reference="fig:abla_search"} shows the number of iterations required to find each reasonable effect vector using these methods. Compared to uninformed methods, our IVNTR framework is at least $2\times$ more efficient. The greedy approach exhibits high variance and is generally less reliable. We present comparisons in more domains in Appendix [7.13](#app:more_search){reference-type="ref" reference="app:more_search"}.

:::: {#fig:abla_search .figure latex-placement="!t"}
![](Li2025Bilevel_figs/fig6.png){width="1.01\\columnwidth"}

::: caption
Comparison between IVNTR with other search strategies in the Engrave domain. We report the number of iterations for each of the algorithm to find the reasonable effect vectors (different predicate could have different maximum search space $M_{\mathrm{max}}$). IVNTR has demonstrated the highest efficiency in finding the desired vectors.
:::
::::

**Comparison to Pure High-level Planning:** []{#sec:abla_pure_high_level label="sec:abla_pure_high_level"} As discussed in Section [3](#sec:bilevel_planning){reference-type="ref" reference="sec:bilevel_planning"}, predicates not only enable compositional generalization through planning operators but also serve as indicators of sampler failures in low-level states. To assess the importance of our invented predicates for reliable low-level sampling, we disabled bilevel planning and followed the high-level plan greedily, ignoring predicate-based checks for sampler success. As shown in Table [2](#tab:abla_highlevel){reference-type="ref" reference="tab:abla_highlevel"}, this approach results in performance drops of up to $98.4\%$, underscoring the critical role of predicates as indicators of low-level state validity.

## Interpreting Invented Predicates

Predicates play a key role in defining the preconditions and effects of operators, specifying the order of ground actions to complete a task. In Table [3](#tab:interprete){reference-type="ref" reference="tab:interprete"}, we display part of the precondition and effect sets for high-level actions in the Climb-Transport domain, where invented predicates capture logical relationships among actions. For example, the $\mathtt{Drop}$ action requires $\mathtt{P2_1}$ and $\mathtt{P2_2}$, which are the add effects of $\mathtt{Gaze}$, $\mathtt{MTGaze}$, and $\mathtt{WalkOn}$. Similarly, the $\mathtt{Pick}$ action depends on $\mathtt{P1_1}$, the delete effect of $\mathtt{Grasp}$, enforcing all $\mathtt{Pick}$ actions to precede $\mathtt{Grasp}$. These relational constraints over objects enable the generation of long-horizon plans that generalize to unseen object compositions. The complete operators are detailed in Appendix [7.8](#app:complete_op){reference-type="ref" reference="app:complete_op"}. We also provide visualizations of how predicates act as success indicators to filter out sampler failures in Appendix [7.9](#app:sampler_vis){reference-type="ref" reference="app:sampler_vis"}.

# Related Works

## Learning Abstractions for Planning

Learning abstractions is essential for reducing the complexity of long-horizon planning in high-dimensional domains. Traditional approaches, such as hierarchical task networks (HTN) [@kaelbling2011htn], heavily rely on hand-designed abstractions. Recent advances have shifted towards data-driven approaches that automatically discover useful abstractions from interactions [@gupta2020relay; @Soroush2022maple; @hansen2022bisimulation; @dong2019nlm; @chitnis2021glib] or demonstrations [@sharmadirected; @kipf2019compile; @chitnis2021nsrt; @mao2022pdsketch]. However, these methods struggle to generalize beyond the training environments [@liang2024visualpredicator]. Foundation models, such as large language models (LLMs) and vision-language models (VLMs), have been explored for high-level planning with minimal or no demonstrations [@liu2024BLADE; @fang2024keypoint; @liang2024visualpredicator; @silver2024generalized; @wei2022cot; @han2024interpret; @huang2023voxposer; @hu2023look; @kumar2024openworld]. While these models leverage commonsense knowledge for efficient plan generation, two challenges remain: (1) High-level plans from LLMs [@silver2024generalized; @han2024interpret; @wei2022cot; @huang2023voxposer] are difficult to reliably refine in the low-level space [@liang2024visualpredicator]. (2) VLM-based methods [@liang2024visualpredicator; @fang2024keypoint; @kumar2024openworld; @yang2024guidinglonghorizontaskmotion] struggle in domains where images cannot fully capture the state space.

## Task and Motion Planning

To address these challenges, task and motion planning (TAMP) integrates high-level symbolic planning with low-level motion generation. Traditional TAMP methods [@garrett2021integrated; @garrett2020pddlstream] rely on manually designed planners [@McDermott1998PDDL; @karaman2011anytime]. These frameworks inherently support compositional generalization due to their relational structure. In addition, the coupling between high-level and low-level planning can handle failures at either level effectively. However, traditional TAMP requires substantial human effort. Recent advances integrate learning into TAMP [@chitnis2021nsrt; @bougie2020skill; @kumar2023predict; @silver2023predicateinvent; @liang2024visualpredicator; @kumar2024openworld; @yang2024guidinglonghorizontaskmotion], forming bilevel planning frameworks. These approaches combine the strengths of TAMP with the scalability of machine learning models. However, most bilevel planners rely on manually engineered state abstractions (predicates), limiting their scalability and flexibility.

::: {#tab:interprete}
   Predicates          $\mathtt{P1_1(?r)}$           $\mathtt{P2_1(?r,?t)}$   $\mathtt{P2_2(?r,?t)}$   $\mathtt{In(?t,?t)}$  
  ------------ ------------------------------------ ------------------------ ------------------------ ---------------------- --
    `Grasp`     $\mathtt{Pre} \mid \mathtt{Eff}^-$       $\mathtt{Pre}$           $\mathtt{Pre}$                             
     `Gaze`                                              $\mathtt{Pre}$          $\mathtt{Eff}^+$                            
    `MAOff`               $\mathtt{Pre}$                                                                                     
     `MAOn`                                              $\mathtt{Pre}$           $\mathtt{Pre}$                             
    `MTGaze`                                            $\mathtt{Eff}^+$                                                     
    `WalkOn`                                            $\mathtt{Eff}^+$                                                     
   `MTPlace`              $\mathtt{Pre}$                                                                                     
   `MTReach`                                                                                                                 
     `Pick`               $\mathtt{Pre}$                                                                                     
     `Drop`                                              $\mathtt{Pre}$           $\mathtt{Pre}$         $\mathtt{Eff}^+$    

  : The preconditions, add effects, and delete effects for each of the actions (the variables are neglected for simplicity) with (part of) the invented predicates in the Climb-Transport Domain. $\mathtt{MA}$ is for $\mathtt{MoveAway}$ and $\mathtt{MT}$ for $\mathtt{MoveTo}$. The invented predicates have specified some logical constrains over the order of actions.
:::

## Predicate Invention for Planning

To automate predicate generation for planning, various approaches have been proposed [@liang2024visualpredicator; @li2023embodied; @han2024interpret; @silver2023predicateinvent; @asai2019latplan_fol; @asai2021latplanpddl; @asai2018latplan_prop; @hansen2022bisimulation; @shah2024reals]. The most direct approaches [@li2023embodied; @han2024interpret] rely on domain knowledge, such as human-provided labels [@li2023embodied] or LLM-based oracles [@han2024interpret]. To *invent* predicates, earlier approaches derive \"easy\" step-wise objectives, such as reconstruction [@asai2018latplan_prop; @asai2019latplan_fol; @asai2021latplanpddl] or bisimulation [@hansen2022bisimulation]. Among these, LatPlan (FOSAE) [@asai2019latplan_fol] learns relational neural abstractions for images by reconstructing states and identifying action spaces for planning, which is the closest work to IVNTR. However, its implicit predicates are not optimized for efficient planning, limiting its applicability to domains with only nullary actions. Recent approaches [@silver2023predicateinvent; @liang2024visualpredicator] address this by learning abstractions tailored to fast planners [@helmert2006fast]. However, these methods struggle to *learn* predicate classifiers due to non-differentiable objectives. Consequently, they often rely on pre-defined predicate candidates from program synthesis [@silver2023predicateinvent] or foundation models [@liang2024visualpredicator], which constrains their applicability in more sophisticated and high-dimensional state spaces. Our approach is motivated by the bilevel planning framework [@silver2023predicateinvent] but eliminates the need for pre-defining the candidates. Instead, we can learn adaptive neural classifiers for different domains, enabling more flexible and scalable learning based planning.

# Limitations and Future Works

In this work, we introduced IVNTR, a bilevel learning framework that invents neural classifiers as relational planning predicates. These predicates enable the learning of relational bilevel planners capable of generating long-horizon plans for unseen object compositions. At the neural level, IVNTR leverages the high-level effects of predicates across actions to provide step-wise supervisions on transition pairs. At the symbolic level, IVNTR captures the sparsity of effects through an informed tree expansion algorithm. By adopting neural classifiers, IVNTR adapts to diverse robot planning domains with continuous and high-dimensional state representations. Additionally, we deployed IVNTR on a mobile manipulator, demonstrating its ability to achieve compositional generalization over objects and actions in long-horizon mobile manipulation tasks.

IVNTR has several limitations that we leave for future work: (1) IVNTR can only invent *dynamic* predicates. *Static* predicates are still assumed as domain-level prior knowledge. (2) Following previous works [@kumar2024practice], we have assumed the sparsity of effects; discussions about the general cases can be found in Appendix [7.2](#app:assumption){reference-type="ref" reference="app:assumption"}. (3) Since IVNTR trains different neural networks in each iteration, the learning time could be prolonged in domains with extreme complexity. Currently, we parallelize the invention of different predicate groups on multiple GPUs for efficiency (see Appendix [7.5](#app:domain_details){reference-type="ref" reference="app:domain_details"}). (4) Neural predicates with quantifiers are less reliable due to the prediction errors in the classifiers. Future work could explore probabilistic symbolic planners [@younes2004ppddl1] or hybrid declarative-imperative representations [@mao2024hybrid] to plan with an inaccurate model. (5) Since the predicates are neural networks, it is hard to interpret their physical meanings. It would also be intriguing for future approaches to make them directly human readable.

# Acknowledgment {#acknowledgment .unnumbered}

We acknowledge the support of the Air Force Research Laboratory (AFRL), DARPA, under agreement number FA8750-23-2-1015. We also acknowledge Defence Science and Technology Agency (DSTA) under contract #DST000EC124000205. This work used Bridges-2 at PSC through allocation cis220039p from the Advanced Cyberinfrastructure Coordination Ecosystem: Services & Support (ACCESS) program which is supported by NSF grants #2138259, #2138286, #2138307, #2137603, and #213296. We express sincere gratitude to Qinglin Feng for her valuable time in supporting our real-robot experiments and for her intelligence in motivating our Climb-Transport domain. The authors would also like to express sincere gratitude to Jiayuan Mao (MIT), Nishanth Kumar (MIT), Prof. Katia Sycara (CMU), and Prof. Pradeep Ravikumar (CMU) for their valuable feedback, discussions, and suggestions on the early stages of this work. Finally, the authors wish to thank our Spot robot, Spotless, for being reliable throughout our real-world experiments.

## Complete Notation Table {#app:notation}

We have presented the complete notation definition in Table [4](#tab:notation){reference-type="ref" reference="tab:notation"} for reference.

## Discussion on the Sparsity Assumption {#app:assumption}

Formally, we define the sparsity assumption required as:

::: assumption
**Assumption 1** (Effect Sparsity). Let $\underline{\mathtt{C}}$ be a ground action with object sets $\mathcal{O}_{\underline{\mathtt{C}}}$, $\underline{\psi}$ be a ground predicate with object sets $\mathcal{O}_{\underline{\psi}}$, and $(\mathbf{x}, \underline{\mathtt{C}}, \mathbf{x}')$ be a transition pair. If $\mathcal{O}_{\underline{\psi}} \not\subset\mathcal{O}_{\underline{\mathtt{C}}}$, then $\theta_{\underline{\psi}}(\mathbf{x})=\theta_{\underline{\psi}}(\mathbf{x}')$.
:::

Generally, this assumption holds if the following two conditions are both satisfied:

- Each of the actions $\mathtt{C}\in\mathcal{C}$ in the domain has only one unique planning operator $\mathtt{Op}^{\mathtt{C}}$.

- The variable set in actions $\mathtt{C}$ is the same as the variable set in the operator $\mathtt{Op}^{\mathtt{C}}$.

In other words, if the options [@chitnis2021nsrt] in a domain equal to the potential operators, then the assumption holds. Though this is true in many domains, including those from previous work [@kumar2024practice], there exist domains where this assumption breaks [@silver2023predicateinvent; @chitnis2021nsrt]. If the assumption no longer holds, more entries will become non-zero in $\bm{t}^{\psi, \underline{\mathtt{C}}}(\mathbf{x}, \mathbf{x}')$ and it would be very hard to identify their locations. One future work that could potentially address this issue is by alternating between the predicate learning framework proposed in Section [4](#sec:ivntr){reference-type="ref" reference="sec:ivntr"} and the clustering mechanism proposed in previous work [@chitnis2021nsrt].

::: {#tab:notation}
                 **Symbol**                                            **Meaning**                              **Space**
  ----------------------------------------- ----------------------------------------------------------------- --------------
                  $\Lambda$                                     The type set in a domain                           Set
                  $\lambda$                                        A type in a domain                             Symbol
             $\mathtt{?\lambda}$                                    A typed variable                              Symbol
                     $T$                                           A task in a domain                             Tuple
                $\mathcal{T}$                                       Task Distribution                          Distribution
                     $K$                                   Domain specific feature dimensions                     Scalar
                     $N$                                       Number of objects in a task                        Scalar
               $\mathbf{x}_i$                                       The $i$-th state                              Matrix
                $\mathcal{O}$                                     Object set in a task                             Set
                $\mathcal{C}$                                  The action set in a domain                          Set
                $\mathtt{C}$                                A parametrized action in a domain                     Symbol
                     $M$                                      Number of actions in a domain                       Scalar
                  $\Omega$                              Space of the continuous action parameter                   Set
                  $\omega$                              The specific continuous action parameter                  Vector
          $\underline{\mathtt{C}}$                            A grounded and refined action                       Symbol
       $\underline{\bar{\mathtt{C}}}$                       A grounded but not refined action                     Symbol
                     $f$                                     Transition function for a task                      Function
                   $\psi$                                           Lifted predicate                              Symbol
             $\underline{\psi}$                                    Grounded predicate                             Symbol
                $\theta_\psi$                                Classifier for predicate $\psi$                     Function
         $\theta_{\underline{\psi}}$         Classification result for grounded predicate $\underline{\psi}$      Scalar
                   $\Psi$                                  Complete predicate set for a domain                     Set
             $\Psi_\mathrm{sta}$                            Static predicate set for a domain                      Set
             $\Psi_\mathrm{dyn}$                           Dynamic predicate set for a domain                      Set
              $\Psi_\mathrm{G}$                              Goal predicate set for a domain                       Set
                $\theta_\Psi$                            Classifier set for predicate set $\Psi$                   Set
                    $\pi$                                             Refined plan                                 List
                 $\bar{\pi}$                                          Plan skeleton                                List
                $\mathcal{D}$                                   The dataset for learning                           Set
                     $B$                                      The number of task-plan pairs                       Scalar
          $\mathtt{Op}^\mathtt{C}$                          Operator for action $\mathtt{C}$                       Set
               $\mathtt{Var}$                                         Variable set                                 List
               $\mathtt{Pre}$                                       Pre-condition set                              Set
              $\mathtt{Eff}^+$                                       Add effect set                                Set
              $\mathtt{Eff}^-$                                      Delete effect set                              Set
              $\eta^\mathtt{C}$                              Sampler for action $\mathtt{C}$                     Function
          $\hat{\Psi}_\mathrm{dyn}$                              Candidate predicate set                           Set
                 $J(\cdot)$                             Score function based on planning outcome                 Function
             $\Psi^\mathtt{Var}$                  Set of predicates with typed variables $\mathtt{Var}$            Set
                $\Delta^\psi$                              Effect vector for predicate $\psi$                     Vector
               $\delta^\psi_i$                 Effect value for predicate $\psi$ in action $\mathtt{C}_i$         Scalar
   $\bm{t}^{\psi, \underline{\mathtt{C}}}$                Predicted ground predicate transition                   Vector
        $\Delta^{\Psi^\mathtt{Var}}$             Effect vector set for predicate set $\Psi^\mathtt{Var}$           Set
               $\mathbf{L}_t$                             Loss information at $t$-th iteration                    Vector
                   $r^n_t$                       Value for the $n$-th effect vector at $t$-th iteration           Scalar
               $\mathbf{R}_t$                            Global value vector at $t$-th iteration                  Vector

  : List of the important notations in this work.
:::

[]{#tab:notation label="tab:notation"}

## Ground Predicates with Action Variables {#app:same_type}

In general, for a transition with ground action $\underline{\mathtt{C}}$, multiple ground predicates could be "grounded on\" the object set $\mathcal{O}_{\underline{\mathtt{C}}}$. For example, in the Blocks domain, we could have actions like $\mathtt{Stack(?r,?b_0,?b_1)}$, where there are two same typed variables $\mathtt{?b_0,?b_1}$ (two objects in the blocks type). In this case, consider the object set $\{\mathtt{r_1,b_1,b_2}\}$, if we have ground action $\mathtt{Stack(r_1,b_1,b_2)}$, then the two ground predicates $\mathtt{P1(b_1,b_2)}$ and $\mathtt{P1(b_2,b_1)}$ should be both considered as "grounded on\" the object set $\mathcal{O}_{\underline{\mathtt{C}}}$. In such cases, the two ground predicates will have the same transition following Definition [4](#def:ground_effect_vec){reference-type="ref" reference="def:ground_effect_vec"}. However, this is usually not true, for example, if $\mathtt{P1(?b,?b)}=\mathtt{On(?b,?b)}$, then the transition of $\mathtt{On(b_1,b_2)}$ and $\mathtt{On(b_2,b_1)}$ should **not** be the same. To solve this problem, when we define the predicate sets $\Psi^\mathtt{Var}$ with the same typed variables $\mathtt{Var}$, we additionally annotate that the predicate variables $\mathtt{Var}$ have a fixed correspondence with the action variables $\mathtt{Var}_\mathtt{c}$. More specifically, when we ground the predicates, all possible object compositions are considered. But when we use the ground predicates to form effects (during predicate function training) and pre-conditions (during operator learning), we only use the ground predicates whose object sets have the specified correspondence with the action variables. For example, consider the predicate $\mathtt{P1(?b,?b)}$, we may further annotate it with a list $[0,1]$, meaning that the first predicate variables should be matched with the first variable in the actions that is typed as a block and the second predicate variables should be matched with the second block variable in the actions. In this case, we will only consider $\mathtt{P1(b_1,b_2)}$ for transitions with action $\mathtt{Stack(r_1,b_1,b_2)}$ (and $\mathtt{P1(b_2,b_1)}$ with action $\mathtt{Stack(r_1,b_2,b_1)}$). In practice, the predicate sets with the same typed variables but different correspondence annotation are considered as different groups in the bilevel learning. For more details, please refer to our source code.

## Improving Efficiency during Expansion {#app:pruning}

To make the tree expansion (symbolic learning) more efficient without sacrificing too much completeness, we have tried to prune an effect vector $\Delta^{\psi_n}$ (setting its value $r^n$ as $-\infty$) via the following strategy:

- If the input object-centric states to the predicate function $\theta_{\psi_n}$ never change for any ground actions $\underline{\mathtt{C}}$ belonging to an action $\mathtt{C}$, then the nodes $\Delta^{\psi_n}$ with non-zero entry $\Delta^{\psi_n}_\mathtt{C}$ will be pruned. This strategy is implemented as a "pre-check\", which happens before the tree expansion starts.

- Assume the loss vector $\mathbf{L}_t$ is from the evaluated effector vector $\Delta^\psi_t$ in the $t$-th iteration. Let $\mathbb{I}(\Delta^{\psi}_t \neq 0)$ and $\mathbb{I}(\Delta^{\psi_n} \neq 0)$ be the mask indicating whether the entries in $\Delta^\psi_t$ and $\Delta^{\psi_n}$ are non-zero, respectively. We prune $\Delta^{\psi_n}$ if $\sum \mathbf{L}_t\odot\mathbb{I}(\Delta^{\psi}_t \neq 0)\odot\mathbb{I}(\Delta^{\psi_n} \neq 0) > \tau$.

The second strategy prunes a vector if the sum of the loss from its non-zero indices is larger than the threshold. This strategy might make the tree expansion not fully complete. The intuition behind it is that: Since the children have the same non-zero parts as their parents, if the parents' non-zero part has already contributed high validation loss, then we assume the children's non-zero part will also contribute high loss. There is a small chance that the children turn out to have low loss due to the additional non-zero entry. We have empirically shown that this strategy works in practice, probably due to the fact that a child node can come from different parents.

:::: {#fig:app_failure .figure latex-placement="!t"}
![](Li2025Bilevel_figs/app_failure.png){width="2\\columnwidth"}

::: caption
Typical failure cases in the real robot tests of the Climb-Transport domain. The most common failure is that the target is dropped outside of the container, which is due to the localization error. Other failures include failing to generate the grasping motion plan on the platform and falling of the platform while trying to climb onto it.
:::
::::

## Implementation Details for Each Domain {#app:domain_details}

Here, we provide more details for each domain:

**Satellites:**

- *Types*: The satellites ($\mathtt{s}$) and the targets ($\mathtt{t}$).

- *Actions*: $\mathtt{Calibrate(?s,?t)}$, $\mathtt{MoveTo(?s,?t)}$, $\mathtt{MoveAway(?s,?t)}$, $\mathtt{ShootX(?s,?t)}$, $\mathtt{ShootY(?s,?t)}$, $\mathtt{TakeCam(?s,?t)}$, $\mathtt{TakeInfrared(?s,?t)}$, and $\mathtt{TakeGeiger(?s,?t)}$.

- *Static Predicates*: $\mathtt{CalibrationTgt(?s,?t)}$, $\mathtt{ShootsX(?s)}$, $\mathtt{ShootsY(?s)}$.

- *Goal Predicates*: $\mathtt{CamTaken(?s,?t)}$, $\mathtt{InfraredTaken(?s,?t)}$, $\mathtt{GeigerTaken(?s,?t)}$.

- *Task Description*: There are some number of satellites, each carrying an instrument. The possible instruments are: (1) a camera, (2) an infrared sensor, (3) a Geiger counter. Additionally, each satellite may be able to shoot Chemical X and/or Chemical Y. The satellites have a viewing cone within which they can see everything that is not occluded. The goal is for specific satellites to take readings of specific objects with calibrated instruments.

- *Predicate invention hardware*: A single A100 GPU.

**Blocks:**

- *Types*: The robot ($\mathtt{r}$) and the blocks ($\mathtt{b}$).

- *Actions*: $\mathtt{PickFromTable(?r,?b)}$, $\mathtt{Unstack(?r,?b,?b)}$, $\mathtt{Stack(?r,?b,?b)}$, $\mathtt{PutOnTable(?r,?b)}$, $\mathtt{Pack(?b,?b)}$.

- *Static Predicates*: None.

- *Goal Predicates*: $\mathtt{Packed(?b,?b)}$.

- *Task Description*: The robot needs to manipulate a set of blocks (which were initialized as random towers) and pack them into required pairs. In order to pack two blocks, one block needs to be on the top of another with the bottom block on the table and the top block clear.

- *Predicate invention hardware*: A single A100 GPU.

**Measure-Mul:**

- *Types*: The robot ($\mathtt{r}$) and the targets ($\mathtt{t}$).

- *Actions*: $\mathtt{Calibrate(?r,?t)}$, $\mathtt{MoveTo(?r,?t)}$, $\mathtt{MoveAway(?r,?t)}$, $\mathtt{Gaze(?r,?t)}$, and $\mathtt{Measure(?r,?t)}$.

- *Static Predicates*: $\mathtt{CalibrationTgt(?s,?t)}$.

- *Goal Predicates*: $\mathtt{Measured(?t)}$.

- *Task Description*: The Spot robot needs to use a thermal camera under its hand to measure the body temperature of multiple human targets. To do this, it needs to first calibrate the camera with respect to a calibrator by gazing at it, which poses some constraints on the relative poses between the hand and the target. Then, before measuring each target, it also needs to gaze at them.

- *Predicate invention hardware*: A single A100 GPU.

**Climb-Measure:**

- *Types*: The robot ($\mathtt{r}$), the targets ($\mathtt{t}$), and the platform ($\mathtt{p}$).

- *Actions*: $\mathtt{Calibrate(?r,?t)}$, $\mathtt{MoveToGaze(?r,?t)}$, $\mathtt{MoveToReach(?r,?p)}$, $\mathtt{MoveToPlace(?r,?p,?t)}$, $\mathtt{MoveAwayOff(?r,?t)}$, $\mathtt{MoveAwayOn(?r,?p,?t)}$, $\mathtt{WalkOn(?r,?p,?t)}$, $\mathtt{Pick(?r,?p)}$, $\mathtt{Place(?r,?p,?t)}$, $\mathtt{Gaze(?r,?t)}$, and $\mathtt{Measure(?r,?t)}$.

- *Static Predicates*: $\mathtt{CalibrationTgt(?s,?t)}$, $\mathtt{DirectViewable(?t)}$, $\mathtt{AppliedTo(?p,?t)}$.

- *Goal Predicates*: $\mathtt{Measured(?t)}$.

- *Task Description*: Similar to Measure-Mul, the Spot robot needs to use a thermal camera under its hand to measure the body temperature of a human target. Differently, the calibrator and human target could be at a high location where the Spot can directly gaze at them. To achieve the goal, the Spot will need to arrange some platforms.

- *Predicate invention hardware*: Parallelly on four A100 GPUs.

**Climb-Transport:**

- *Types*: The robot ($\mathtt{r}$), the targets ($\mathtt{t}$), and the platform ($\mathtt{p}$).

- *Actions*: $\mathtt{Grasp(?r,?t)}$, $\mathtt{MoveToGaze(?r,?t)}$, $\mathtt{MoveToReach(?r,?p)}$, $\mathtt{MoveToPlace(?r,?p,?t)}$, $\mathtt{MoveAwayOff(?r,?p)}$, $\mathtt{MoveAwayOn(?r,?p,?t)}$, $\mathtt{WalkOn(?r,?p,?t)}$, $\mathtt{Pick(?r,?p)}$, $\mathtt{Gaze(?r,?t)}$, and $\mathtt{Drop(?r,?t,?t)}$.

- *Static Predicates*: $\mathtt{GraspingTgt(?t)}$, $\mathtt{InitHigh(?t)}$.

- *Goal Predicates*: $\mathtt{In(?t,?t)}$.

- *Task Description*: The Spot robot needs to grasp a target and drop it into another target container. Similar to Climb-Measure, to achieve the goal, the Spot will need to arrange some platforms.

- *Predicate invention hardware*: Parallelly on four A100 GPUs.

**Engrave:**

- *Types*: The robot ($\mathtt{r}$) and the blocks ($\mathtt{b}$).

- *Actions*: $\mathtt{PickFromTable(?r,?b)}$, $\mathtt{Unstack(?r,?b,?b)}$, $\mathtt{Stack(?r,?b,?b)}$, $\mathtt{PutOnTable(?r,?b)}$, $\mathtt{Engrave(?r, ?b,?b)}$, $\mathtt{Rotate(?r,?b)}$, $\mathtt{Pack(?b,?b)}$.

- *Static Predicates*: $\mathtt{NotEq(?b,?b)}$

- *Goal Predicates*: $\mathtt{Packed(?b,?b)}$.

- *Task Description*: Similar to Blocks, the robot needs to manipulate a set of blocks (which were initialized as random towers) and pack them into required pairs. However, blocks start with one irregular Gaussian surface that must be "engraved\" to create a matching fit. Once engraved, blocks need to be further rotated and placed for final assembly and packing. We generate the Block meshes and point clouds using Pytorch3D [@ravi2020pytorch3d]. For fairness, all methods use the same PointNet [@qi2017pointnet] as the state encoder.

- *Predicate invention hardware*: Parallelly on six A100 GPUs.

For more details about these domains, please refer to our source code.

## More Details about Baselines {#app:baseline_details}

We introduce more details for the relational neural policy baselines here:

- **GNN**: The nodes are defined the object-centric features and the edges are defined as the grounded binary predicates (provided static and goal predicates). During training, the GNN learns to predict the action class and the selected objects. During test, the GNN tries to shoot multiple tries until planning budget run out.

- **Transformer**: The tokens are defined the object-centric features as well as the grounded predicates (provided static and goal predicates). The training objective and test setup are similar to GNN. However, different from the message passing strategy in GNN, we used the multi-head attention mechanism for the information fusing among tokens

- **FOSAE**: The baseline is loosely inspired by the state autoencoder (SAE) proposed in LatPlan [@asai2019latplan_fol]. We first use the official attention mechanism to pre-train the SAE module by reconstructing the original state. Then, since the action spaces in this work is relational (instead of nullary), we encode the augmented binary states from SAE as the global feature of a graph neural network. Finally, the graph neural network is trained and evaluated similar to the GNN-shooting baseline.

For fairness, we have used the same action samplers learned using our framework for the three baseline above. For more details, please refer to our source code.

## Failures in Real Robot Experiments {#app:failures}

As shown in Figure [7](#fig:app_failure){reference-type="ref" reference="fig:app_failure"}, we present the typical failure cases in the real-robot tests for the Climb-Transport domain. The most frequent failure is that the robot finally drops the target outside of the container (but very close). The reason is that the map of our experiments was recorded before the tables (used to place targets) were placed, which could result in the small drift of the localization system on Spot during the plan execution. These drifts finally accumulate and result in the final hand pose error. A worse problem is that due to the lack of a motion capture system, the container itself might not be accurately placed. One potential way to address this is by integrating some more advanced SLAM system that is robust to partial map changes. Another failure case (much less common) is that the Spot grasping skill could fail when it is on a platform. Here, we have used the manipulation toolkit from the official Boston Dynamics Python SDK, which might fail to find a grasping motion plan in certain states. Finally, since the platform is narrow, we have also observed that the Spot could fall off the platform when walking onto the platform.

## Invented Predicates and Operators {#app:complete_op}

We present the invented predicates together with the operators for the Satellites domain below. The invented predicates are named as $\mathtt{P1},\mathtt{P2},\cdots$, while the provided predicates have the names introduced in Appendix [7.5](#app:domain_details){reference-type="ref" reference="app:domain_details"}. For other domains, the learned operators are more sophisticated; please refer to our source code and meta results for details.

**Satellites:**

``` {frame="single" resetmargins="true"}
Calibrate(?x0:s, ?x1:t)
  :Pre (and 
      (CalibrationTgt(?x0, ?x1))
      (not P3_0(?x0, ?x1))) 
  :Eff+ (P1_0(?x0))
  :Eff- set()
MoveAway(?x0:s, ?x1:t)
  :Pre (not P3_0(?x0, ?x1))
  :Eff+ (ForAll:?t P3_0(?x0, ?t))
  :Eff- (not P3_0(?x0, ?x1))
MoveTo(?x0:s, ?x1:t)
  :Pre (ForAll:?t P3_0(?x0, ?t))
  :Eff+ (not P3_0(?x0, ?x1))
  :Eff- (ForAll:?t P3_0(?x0, ?t))
ShootChemX(?x0:s, ?x1:t)
  :Pre (and
    (not P3_0(?x0, ?x1))
    ShootsChemX(?x0))
  :Eff+ (P2_0(?x1))
  :Eff- set()
ShootChemY(?x0:s, ?x1:t)
  :Pre (and
    (not P3_0(?x0, ?x1))
    ShootsChemY(?x0))
  :Eff+ (P2_1(?x1))
  :Eff- set()
UseCamera(?x0:s, ?x1:t)
  :Pre (and
    (not P3_0(?x0, ?x1))
    (P1_0(?x0))
    (P2_0(?x1))
    HasCam(?x0))
  :Eff+ (CameraReadingTaken(?x0, ?x1))
  :Eff- set()
UseGeiger(?x0:s, ?x1:t)
  :Pre (and
    (not P3_0(?x0, ?x1))
    (P1_0(?x0))
    HasGeiger(?x0))
  :Eff+ (GeigerReadingTaken(?x0, ?x1))
  :Eff- set()
UseInfraRed(?x0:s, ?x1:t)
  :Pre (and
    (not P3_0(?x0, ?x1))
    (P1_0(?x0))
    (P2_1(?x1))
    HasInfrared(?x0))
  :Eff+ (InfraredReadingTaken(?x0, ?x1))
  :Eff- set()
```

:::: {#fig:vis_sample .figure latex-placement="!t"}
![](Li2025Bilevel_figs/app_sampler.png){width="1\\columnwidth"}

::: caption
Visualization of the classification results on sampled poses for `MoveToReach` action using our invented predicate $\mathtt{P3(?r,?p)}$. TP is for true positive, TN is for true negatives, and FP is for false positive. We only visualize part of the samples which are converted to SE2 for simplicity, best viewed in color.
:::
::::

## Neural Predicates as Guidance for the Samplers {#app:sampler_vis}

As shown in Figure [8](#fig:vis_sample){reference-type="ref" reference="fig:vis_sample"}, we visualize classification results for sampled continuous parameters of the `MoveToReach` action across $4$ tasks. Since training demonstrations involve solving inverse kinematics (IK) for `MoveToReach`, accurate sampler learning is challenging. Our invented predicate $\mathtt{P3(?r,?p)}$, an add effect of `MoveToReach` and a precondition for `Pick`, effectively filters out most true negatives (TNs), ensuring successful plans.

:::: {#fig:ana_objective .figure latex-placement="!t"}
![](Li2025Bilevel_figs/app_obj.png){width="1\\columnwidth"}

::: caption
Score optimization process during the predicate selection stage. Compared with grammar based predicate pool [@silver2023predicateinvent], our IVNTR is capable of constructing a much stronger neural predicate pool, which is able to effectively optimize the planning objective with a few hill-climbing steps. Yet, the grammar-based approach has failed.
:::
::::

## Objective Minimization {#app:objective}

We display the objective minimization process during the predicate selection stage in Figure [9](#fig:ana_objective){reference-type="ref" reference="fig:ana_objective"}. Compared with the grammar-based predicate pool [@silver2023predicateinvent], IVNTR is capable of generating much stronger neural functions as predicate candidates. These neural predicates have made the objective minimization possible for more complicated states, where previous approaches have failed [@silver2023predicateinvent].

## Operator and Sampler Learning {#app:op_sam_learning}

We primarily follow existing work for sampler and operator learning [@silver2023predicateinvent]. For each predicate in the final set $\psi\in\Psi$, we obtain its lifted effect vector $\Delta^\psi$ by running the classifier on training dataset. For the $m-$th operator $\mathtt{Op}^\mathtt{C}$, its effects are computed by checking the $m-$th entry of the effect vectors from all predicates. The preconditions for each operator are determined by finding the intersection among all ground atoms that are true in previous states of ground transitions, known as intersection [@silver2023predicateinvent]. For sampler learning, we leverage supervised learning to train a Gaussian regressor as generator and an MLP as classifier.

## Applying IVNTR to Domains with Image States {#app:blocks_img}

:::: {#fig:blocks_img .figure latex-placement="!t"}
![](Li2025Bilevel_figs/app_blocks_img.png){width="1\\columnwidth"}

::: caption
An example demonstration with $3$ blocks, where the states are represented in RGB images. In each step, we have used an object detection algorithm to obtain object centric images as the input states to our IVNTR algorithm.
:::
::::

::: {#tab:app_search}
   Method/Predicate   P1   P2   P3    P4    P5   Avg.
  ------------------ ---- ---- ----- ----- ---- ------
   **IVNTR (Ours)**   6    55    6    51    2     24
        Greedy        77   34   139   20    12   56.4
         BFS          15   30   55    218   14   66.4
         DFS          4    39   188   91    18    68
        Random        80   80   242   242   26   134

  : Comparison between our neural guided tree expansion and other alternative tree expansion algorithms in the Climb-Transport domain. Our IVNTR has demonstrated the best average efficiency in finding the five predicates.
:::

We have further implemented a Blocks stacking domain with RGB images as states, see Figure [10](#fig:blocks_img){reference-type="ref" reference="fig:blocks_img"} for visualizations. Methods are required to generalize from $3-4$ blocks to $5$ blocks. IVNTR was built upon ResNet18 [@he2016res], which has successfully invented visual predicates like `Holding(?b)`. The average success rate on generalized tasks of *IVNTR*/GNN/No_invention are *92.0%*/14.7%/0.0%.

## Search Efficiency Comparison {#app:more_search}

We further present the search ablations on the Climb-Transport domain in Table [5](#tab:app_search){reference-type="ref" reference="tab:app_search"}, where the average search iterations using *IVNTR*/Greedy/BFS/DFS/Random are *24*/56.4/66.4/68/134.

[^1]: $^\dagger$Work was partly done during internship at Centaur AI Institute. Correspondence to {bowenli2,basti}@andrew.cmu.edu.

[^2]: Unlike previous work [@silver2023predicateinvent], we do not assume that features are scalars; high-dimensional images and point clouds are also allowed.

[^3]: Each predicate here can appear at most once in the effect sets, but this doesn't affect the representation capability of the final predicate set.

[^4]: Following previous work [@silver2023predicateinvent], we can also add quantifiers and negations as prefix for each of the invented neural predicates.
