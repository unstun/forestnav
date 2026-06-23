---
citation_key: Rao2024Trajectory
arxiv_id: 2410.04129
arxiv_url: https://arxiv.org/abs/2410.04129
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-23T19:17:17Z
origin: ai+web
reviewed: false
---

:::: frontmatter
[^1]

,

::: keyword
Dubins Shortest Path, curvature bounded trajectories, elongation strategies, trajectory planning
:::
::::

# Introduction

The problem of planning trajectories between two given points for an autonomous vehicle moving at a constant speed has been explored extensively in literature of guidance and control. It finds its applications in a variety of fields such as parking problems[@b29], warehouse automation[@b30], missile guidance[@b27], *etc.* The feasibility of such problems towards real world applications leads to additional requirements such as curvature-boundedness, desired lengths of the trajectories, directions of motion at initial and final points[@b12], and optimal energy consumption [@b28].

The shortest trajectory between any two oriented points in $\mathbb{R}^2$ is either of the form Circle-Circle-Circle $(CCC)$ or Circle-Straight Line-Circle $(CSC)$ ([@dubins],[@b14]). This trajectory is called Dubins Shortest Path. A relaxed problem is to find trajectories of desired lengths between an oriented point and a fixed point in $\mathbb{R}^2$. The shortest path in such a scenario is of the form Circle-Circle $(CC)$ or Circle-Straight Line $(CS)$ as shown in [@bui1994accessibility]. Elongation of certain subsections of such a minimum length trajectory is done to get trajectories of desired lengths. Without fixing the tangent vector at the final point, the authors in [@b12] and [@b13] present multiple such elongation strategies. However, it is shown in [@b19] that between some initial oriented points and final points, there exist no curvature-bounded paths for a certain range of lengths. This classification of the set of reachable lengths is elaborated in [@b19] and elongation strategies are presented for all the cases.

The authors in [@b15] discuss elongation strategies achieved by increasing the radii of curvature of the terminal circles when the Dubins Shortest Path is of the form $CSC$. Alternatively, the authors in [@b22] propose replacing the straight-line segment with an elongated path. The use of clothoid arcs of arbitrary lengths is proposed in [@b1] for trajectory elongation while also ensuring a continuity in the curvature profile. The authors in [@chen_elongation] provide a comprehensive analysis of the set of reachable lengths given any two oriented points and propose elongation strategies for all pairs of oriented points. They also highlight the cases when certain lengths are not reachable for some pairs of oriented points. In [@b25], the Dubins Shortest Path is extended to three-dimensional space, followed by the introduction of trajectory elongation methods to attain any desired length. The authors in [@patsko2022three] analyse the set of reachable oriented points from any initial oriented point at time $t_f$ for a Dubins vehicle with symmetric bounds on the control input. Further, in the case of asymmetric bounds on the control input, the set of reachable oriented points is derived in [@patsko2023threeasym]. Note that, in general, the use of elongation based strategies increases the number of changeover points. The strategies presented in [@b15; @b22; @b1; @chen_elongation] increase the number of changeover points by as large as six. To address this problem, in one of our earlier works [@RAO], we propose to construct trajectories of desired lengths using exactly two circles of varying radius minimising the changeover points to exactly one always.

Geometrical curves other than circles and straight lines are also used in the literature to construct trajectories of desired lengths. The use of elliptical curves and Bezier curves is proposed in [@b8] and [@b26], respectively, to achieve trajectories of desired lengths. However, the use of geometrical curves, other than the circles and straight lines, limits the set of reachable lengths. Alternate methods have also been explored to achieve a trajectory of desired length between any two oriented points. The authors in [@xu1999curve] construct the trajectory as a polynomial expression and find its parameters that satisfy various constraints. Optimal control theory is employed in [@b23] and [@b24] to develop closed-form Impact Time Control Guidance (ITCG) laws, allowing a vehicle to manoeuvre between two oriented points with a fixed time of flight. In contrast, [@b2] introduces a structure-homotopy-based planner that generates trajectories by focusing on endpoint conditions rather than relying on elongation strategies.

In this work, we focus on planning trajectories of desired lengths between any two given oriented points while minimising the number of changeover points and ensuring the maximum coverage of the set of reachable lengths. The major contributions of this work are as follows:

- *Design of paths of desired lengths:* We propose to construct a feasible trajectory by concatenating three circles. We show that there always exist infinitely many such curvature-bounded trajectories of varying lengths between any two oriented points and present analytical results for the same.

- *Internally tangent trajectories:* The Circle-Circle-Circle Dubins paths are of form $\{RLR,LRL\}$ in literature. The proposed solution expands the Dubins path of form Circle-Circle-Circle $(CCC)$ to eight forms, namely $\{LLL,LLR,LRR,LRL,RRL,RLL,RLR,RRR\}$, by considering circles that are internally tangent. We also show that the Circle-Circle trajectories of form $\{LL,LR,RR,RL\}$ presented in [@RAO] emerge naturally as a subset of the proposed solution.

- *Set of reachable lengths:* We find the set of reachable lengths for these trajectories and show that it is equal to the maximum set of reachable lengths. Given a reachable length, we show that there exist multiple curvature-bounded trajectories of a desired length.

- *Reduction in the number of points of curvature discontinuity:* The proposed trajectory always has a maximum of two changeover points for any two arbitrarily orientated points and a given desired length. This minimisation is achieved without any reduction in the maximum set of reachable lengths.

The paper is organised as follows: Section [2](#section: prelim){reference-type="ref" reference="section: prelim"} presents some preliminary technical results that are used subsequently in the paper. Section [3](#sec: problem){reference-type="ref" reference="sec: problem"} presents the problem statement and describes the proposed method of trajectory design with the motivation behind it. Section [4](#section: existence){reference-type="ref" reference="section: existence"} provides a mathematical description of the proposed Circle-Circle-Circle trajectory and the conditions necessary for its existence. Building on these results, Section [\[section: traj of desired length\]](#section: traj of desired length){reference-type="ref" reference="section: traj of desired length"} explores elongation strategies and their impact on the attributes of the proposed trajectories. Section [6](#sec: reachability set){reference-type="ref" reference="sec: reachability set"} discusses the set of reachable lengths for various pairs of oriented points. Section [7](#sec: simulation){reference-type="ref" reference="sec: simulation"} presents numerical simulations to illustrate the theoretical findings. Finally, Section [8](#sec: conclusion){reference-type="ref" reference="sec: conclusion"} concludes the paper and suggests potential directions for future research.

# Preliminaries and Notations {#section: prelim}

Trajectories constructed using circles have been utilised frequently in path planning problems. They provide simplicity in design and require constant lateral acceleration in physical implementation. We define a curvature-bounded trajectory as a function $\Lambda$ and the minimum turn radius allowed for any such trajectory as $r_{\min}$.

::: {#def:lambda .definition}
****Definition** 1**. *Given two oriented points ${A}=(\mathbf{a},\alpha)$ and ${B}=(\mathbf{b},\beta)$, $\Lambda:[0,s]\longrightarrow\mathbb{R}^2$ denotes a feasible curvature-bounded trajectory connecting the oriented points such that*

- *$\Lambda(t)$ is parameterized by arc length and is $C^1$ and piece-wise $C^2$.*

- *$|{\Lambda^{'}(t)}| = 1 \forall
  t\in[0, s]$*

- *$\Lambda(0)=\mathbf{a},\Lambda(s)=\mathbf{b},\Lambda'(0)=(\cos\alpha,\sin\alpha),\Lambda'(s)=(\cos\beta,\sin\beta)$*

- *$||\Lambda^{''}(t)||\leq1/r_{\min}$, $t\in[0,s]$ when defined,*

*where $r_{\min}>0$. The length of the trajectory is denoted by $l(\Lambda)$.*
:::

We define $\mathcal{C}^r_P$ and $\mathcal{C}^l_P$ as two tangential circles of radius $r_{\min}$ at an oriented point $P$ with their centres at $\mathbf{c}^r_P$ and $\mathbf{c}^l_P$, respectively, as shown in Fig. [1](#fig: left right circles){reference-type="ref" reference="fig: left right circles"}. These circles correspond to a right turn (denoted by $R$) and a left turn (denoted by $L$) on a circular arc of radius $r_{\min}$. Further, we define the function $d:\mathbb{R}^2\times\mathbb{R}^2\longrightarrow\mathbb{R}$ that gives the Euclidean distance between any two points in $\mathbb{R}^2$ plane.

:::: {#fig: left right circles .figure latex-placement="h"}
![](Rao2024Trajectory_figs/left_right.png)

::: caption
Two circles $\mathcal{C}^r_P$ and $\mathcal{C}^l_P$ at oriented points $P$
:::
::::

The radius of a circle is generally a positive real number. However, we denote the radius of a circle as $r\in\mathbb{R}$ within the context of this paper with the following attributes.

::: {#lem:neg_radius .definition}
****Definition** 2**. *For any value of the radius $r\in\mathbb{R}$, the magnitude of curvature is given by $1/|r|$, and the orientation of motion on the trajectory $\Lambda$ is counter-clockwise for $r>0$ and is clockwise for $r<0$.*
:::

We now present some useful results from [@RAO] on the tangency of circles and the motion over trajectories formed by such tangential circles. The statements of these results have been appropriately re-phrased for the context of this paper.

::: {#lem:tangency centre disctance .lemma}
****Lemma** 1**. *Any two tangential circles must satisfy the condition, $$\begin{equation}
    d(\mathbf{o_a},\mathbf{o_b})=|r_a-r_b|
    \label{eq:centre disctance}
\end{equation}$$ where $\mathbf{o_a}$ and $\mathbf{o_b}$ are the coordinates of centres of the circles and $r_a$ and $r_b$ are the radii, respectively.*
:::

The relation in [\[eq:centre disctance\]](#eq:centre disctance){reference-type="eqref" reference="eq:centre disctance"} for the distance between the centres of any two (internally or externally) tangential circles is within the context of the radius given in Definition [2](#lem:neg_radius){reference-type="ref" reference="lem:neg_radius"}.

::: {#lem:tangency relation circles .lemma}
****Lemma** 2**. *If two circles $\mathcal{C}_a$ and $\mathcal{C}_b$ are externally tangent, their radii, $r_a$ and $r_b$, respectively, have opposite signs, otherwise they have the same signs.*
:::

::: {#lem: orientation change .lemma}
****Lemma** 3**. *If any two circular arcs are externally tangent, then, the orientation of the motion switches from clockwise to anti-clockwise or vice-versa along the trajectory at the point of tangency. On the contrary, if the circles are internally tangent, the orientation of the motion remains the same. (Fig. [4](#fig:typesoftangency){reference-type="ref" reference="fig:typesoftangency"})*
:::

:::: {#fig:typesoftangency .figure latex-placement="h"}
![Internally Tangent Arcs](Rao2024Trajectory_figs/FIG12.png){#fig:external orient width="75%"}

![Externally Tangent Arcs](Rao2024Trajectory_figs/FIG17.png){#fig:internal orient width="\\textwidth"}

::: caption
Change of orientation in Internally and Externally Tangent Arcs
:::
::::

We know from [@dubins] that the shortest curvature-bounded trajectory between any two oriented points $A$ and $B$ is either of the form Circle-Straight Line-Circle ($CSC$) or Circle-Circle-Circle ($CCC$), where C denotes a circular arc of radius $r_{\min}$ and S denotes a straight-line segment. We denote this shortest trajectory by $\Lambda_m$ and its length by $l_m$. There exist two types of $CCC$ paths, namely $\{LRL,RLR\}$; and four types of $CSC$ paths, namely $\{LSR,LSL,RSL,RSR\}$.

# Problem Statement {#sec: problem}

Consider two points $\mathbf{a}$ and $\mathbf{b}$ in $\mathbb{R}^2$ space. Without loss of generality, we assume that the final point $\mathbf{b}$ lies at the origin. Let $\alpha$ and $\beta$ be the angles that the velocity vectors make at $\mathbf{a}$ and $\mathbf{b}$ with respect to the positive X-axis, respectively, such that $\alpha,\beta \in [0,2\pi)$. Using them, we define the tuples ${A}(\mathbf{a},\alpha)$ and ${B}(\mathbf{b},\beta)$ to be two oriented points. *The objective of the paper is to construct a trajectory of any arbitrary length $l_o$ between any two given oriented points $A$ and $B$.* Further, additional constraints of curvature-boundedness and minimum curvature discontinuities are imposed on the trajectory to facilitate practical implementation.

:::: {#fig:oriented points .figure latex-placement="h"}
![](Rao2024Trajectory_figs/fig1.png)

::: caption
Oriented points $A(\mathbf{a},\alpha)$ and $B(\mathbf{b},\beta)$ for trajectory design
:::
::::

Any feasible trajectory between $A$ and $B$ has five attributes to satisfy: the initial heading angle ($\alpha$), the final heading angle ($\beta$), the length of the trajectory ($l_o$) and the relative location of points $\mathbf{a}$ and $\mathbf{b}$ in $\mathbb{R}^2$ space. *To impose all of the above conditions, we design a trajectory formed by concatenating three circular arcs with exactly two pairs of circular arcs tangent to each other.* We refer to such trajectories as Circle-Circle-Circle trajectories. The circles are denoted by $\mathcal{C}_1$, $\mathcal{C}_2$ and $\mathcal{C}_3$ and their respective radii by $r_1$, $r_2$ and $r_3$. In any proposed feasible trajectory,

1.  the trajectory begins at the point $\mathbf{a}$ on $\mathcal{C}_1$,

2.  the circles $\mathcal{C}_1$ and $\mathcal{C}_2$ are tangent at a point $\mathbf{c_1}$ and the circles $\mathcal{C}_2$ and $\mathcal{C}_3$ are tangent at a point $\mathbf{c_2}$. These points are called the *changeover points*.

3.  the trajectory ends at point the $\mathbf{b}$ on $\mathcal{C}_3$, and,

4.  the overall trajectory is composed of the union of three circular arcs given by $\widearc{\mathbf{ac_1}} \cup \widearc{\mathbf{c_1c_2}}\cup\widearc{\mathbf{c_2b}}$.

:::: {#fig:traj_cc .figure latex-placement="h"}
![](Rao2024Trajectory_figs/traj_ccc.png)

::: caption
Parameters of Circle-Circle-Circle Trajectory
:::
::::

Fig. [6](#fig:traj_cc){reference-type="ref" reference="fig:traj_cc"} illustrates a Circle-Circle-Circle trajectory. We denote such trajectories by $\mathbf{C}^{r_1}\mathbf{C}^{r_2}\mathbf{C}^{r_3}$ where $r_1,r_2\text{ and }r_3$ correspond to the radius of the three circles, respectively. This is a generalisation of the commonly used notation $CCC$ which represents a Dubins Paths comprising of three circles of curvature $1/r_{\min}$. We now highlight the motivation for using such trajectories:

- In one of our previous works [@RAO], Circle-Circle trajectories are proposed as feasible trajectories in the given framework. The degrees of freedom of such a trajectory are exactly equal to the attributes of the desired trajectory. However, the set of reachable lengths is a subset of the maximum set of reachable lengths given by Theorem [3](#thm: maximal reachable lengths){reference-type="ref" reference="thm: maximal reachable lengths"}. We show eventually that the proposed Circle-Circle-Circle trajectories overcome this limitation.

- Three circles of varying radii lead to nine degrees of freedom in the overall trajectory. With two tangency constraints, we get seven degrees of freedom in a Circle-Circle-Circle trajectory. The extra degrees of freedom are advantageous as they lead to the existence of multiple trajectories between $A$ and $B$.

The following section deals with the mathematical formulation to design $\mathbf{C}^{r_1}\mathbf{C}^{r_2}\mathbf{C}^{r_3}$ trajectories between any two oriented points.

# Existence of Circle-Circle-Circle trajectory {#section: existence}

In this section, we explore the existence of a general $\mathbf{C}^{r_1}\mathbf{C}^{r_2}\mathbf{C}^{r_3}$ trajectory while relaxing the constraint of a desired length. Then, given the oriented points $A(\mathbf{a},\alpha)$ and $B(\mathbf{b},\beta)$, consider the circles $\mathcal{C}_1$ and $\mathcal{C}_3$. Their centres must lie on the lines normal to their respective heading vectors at the terminal points $\mathbf{a}=(a_x,a_y)$ and $\mathbf{b}=(0,0)$. Then, $$\begin{align}
    \mathbf{o_1}&=(a_x-r_1\sin\alpha,a_y+r_1\cos\alpha)\\
    \mathbf{o_3}&=(-r_3\sin\beta,r_3\cos\beta)
\end{align}
\label{eq:centres o1 and o3}$$ As mentioned in Definition [2](#lem:neg_radius){reference-type="ref" reference="lem:neg_radius"}, we interpret $r_1$ and $r_3$ (and later $r_2$) as not just the radii of the respective circles but also the orientations of motion on them. Eqn. [\[eq:centres o1 and o3\]](#eq:centres o1 and o3){reference-type="eqref" reference="eq:centres o1 and o3"} can be viewed as the locus of the centres $\mathbf{o_1}$ and $\mathbf{o_3}$ parameterised by $r_1\in\mathbb{R}$ and $r_3\in\mathbb{R}$. Note that eqn. [\[eq:centres o1 and o3\]](#eq:centres o1 and o3){reference-type="eqref" reference="eq:centres o1 and o3"} holds irrespective of the choice of the intermediate curve. This implies that any curve which satisfies the the five required degrees of freedom can be used here. We choose to use a circular path so that the Dubins Shortest Path is achievable by the resulting trajectory. Depending upon the curve used, different existence conditions emerge. It is not always guaranteed that such a path will exist. Next, we proceed to find the conditions for the existence of the proposed $\mathbf{C}^{r_1}\mathbf{C}^{r_2}\mathbf{C}^{r_3}$ trajectories.

## Locus of the centre of circle $\mathcal{C}_2$ {#subs: locus of centre}

In order to determine the conditions to check the existence of $\mathbf{C}^{r_1}\mathbf{C}^{r_2}\mathbf{C}^{r_3}$ trajectories, we focus on $\mathcal{C}_2$ while keeping $\mathcal{C}_1$ and $\mathcal{C}_3$ fixed. In other words, we assume that $r_1$ and $r_3$ take some finite values in $\mathbb{R}$.

::: {#thm: hyperbola of centre .theorem}
****Theorem** 1**. *For any given circles $\mathcal{C}_1$ and $\mathcal{C}_3$, the locus of the centre of $\mathcal{C}_2$, denoted by $\mathbf{o_2}$, is a hyperbola $\mathcal{H}$ defined by, $$\begin{equation}
        \mathcal{H}=\{\mathbf{o_2}\in\mathbb{R}^2 \mid ~~|d(\mathbf{o_2},\mathbf{o_1})-d(\mathbf{o_2},\mathbf{o_3})|=|r_1-r_3|\}
        \label{eq: hyperbolic relation of centres}
\end{equation}$$ where $\mathbf{o_1}$ and $\mathbf{o_3}$ are centres of $\mathcal{C}_1$ and $\mathcal{C}_3$, respectively, in the feasible $\mathbf{C}^{r_1}\mathbf{C}^{r_2}\mathbf{C}^{r_3}$ trajectory and $r_1$ and $r_3$ are the corresponding radii.*
:::

Let us denote the radius of $\mathcal{C}_2$ as $r_2\in\mathbb{R}$. We proceed with the proof by considering two cases:

- $r_1r_3>0$: Consider $r_1>0$ and $r_3>0$. Thus, there is a left turn on both $\mathcal{C}_1$ and $\mathcal{C}_3$. For this to happen, $\mathcal{C}_2$ must be chosen such that the orientation of motion changes at both $\mathbf{c_1}$ and $\mathbf{c_2}$ or at neither of them. Thus, $\mathcal{C}_2$ must be either externally or internally tangent to both $\mathcal{C}_1$ and $\mathcal{C}_3$ from Lemma [3](#lem: orientation change){reference-type="ref" reference="lem: orientation change"}. For internal tangency, $r_2>0$ from Lemma [2](#lem:tangency relation circles){reference-type="ref" reference="lem:tangency relation circles"}. Consequently, $d(\mathbf{o_2},\mathbf{o_1})=r_2-r_1$ and $d(\mathbf{o_2},\mathbf{o_3})=r_2-r_3$ which implies $d(\mathbf{o_2},\mathbf{o_1})-d(\mathbf{o_2},\mathbf{o_3})=r_3-r_1$. For external tangency, $r_2<0$ from Lemma [2](#lem:tangency relation circles){reference-type="ref" reference="lem:tangency relation circles"}. Hence, $d(\mathbf{o_2},\mathbf{o_1})=r_1-r_2$ and $d(\mathbf{o_2},\mathbf{o_3})=r_3-r_2$ which implies $d(\mathbf{o_2},\mathbf{o_1})-d(\mathbf{o_2},\mathbf{o_3})=r_1-r_3$. Combining them, we get $\left|d(\mathbf{o_2},\mathbf{o_1})-d(\mathbf{o_2},\mathbf{o_3})\right|=|r_1-r_3|$. We get a similar relation for the case $r_1<0$ and $r_3<0$.

- $r_1r_3<0$: Consider $r_1>0$ and $r_3<0$. Thus, there is a left turn on $\mathcal{C}_1$ and a right turn on $\mathcal{C}_3$. For this to happen, $\mathcal{C}_2$ must be chosen such that the orientation changes at exactly one point amongst $\mathbf{c_1}$ and $\mathbf{c_2}$. From Lemma [3](#lem: orientation change){reference-type="ref" reference="lem: orientation change"}, $\mathcal{C}_2$ must be externally tangent to one circle and internally tangent to the other. Thus, for internal tangency at $\mathcal{C}_1$ and external tangency at $\mathcal{C}_3$, $r_2>0$ from Lemma [2](#lem:tangency relation circles){reference-type="ref" reference="lem:tangency relation circles"}. Hence, $d(\mathbf{o_2},\mathbf{o_1})=r_2-r_1$ and $d(\mathbf{o_2},\mathbf{o_3})=r_2-r_3$ which implies $d(\mathbf{o_2},\mathbf{o_1})-d(\mathbf{o_2},\mathbf{o_3})=r_3-r_1$. For the other case where internal tangency occurs with $\mathcal{C}_3$ and external tangency with $\mathcal{C}_1$, $r_2<0$ from Lemma [2](#lem:tangency relation circles){reference-type="ref" reference="lem:tangency relation circles"}. Consequently, $d(\mathbf{o_2},\mathbf{o_1})=r_1-r_2$ and $d(\mathbf{o_2},\mathbf{o_3})=r_3-r_2$ which implies $d(\mathbf{o_2},\mathbf{o_1})-d(\mathbf{o_2},\mathbf{o_3})=r_1-r_3$. Combining them, we get $\left|d(\mathbf{o_2},\mathbf{o_1})-d(\mathbf{o_2},\mathbf{o_3})\right|=|r_1-r_3|$. We get similar relation for the case $r_1<0$ and $r_3>0$.

The relation $\left|d(\mathbf{o_2},\mathbf{o_1})-d(\mathbf{o_2},\mathbf{o_3})\right|=|r_1-r_3|$ represents the hyperbola $\mathcal{H}$ defined in eqn. [\[eq: hyperbolic relation of centres\]](#eq: hyperbolic relation of centres){reference-type="ref" reference="eq: hyperbolic relation of centres"} whose foci are at $\mathbf{o_1}$ and $\mathbf{o_3}$. It is depicted in Fig. [7](#fig: hyperbola locus){reference-type="ref" reference="fig: hyperbola locus"}. Hence, proved. $\square$

The hyperbola $\mathcal{H}$ is important for the analysis of the existence of $\mathbf{C}^{r_1}\mathbf{C}^{r_2}\mathbf{C}^{r_3}$ trajectories. For every point on $\mathcal{H}$, a unique $\mathbf{C}^{r_1}\mathbf{C}^{r_2}\mathbf{C}^{r_3}$ trajectory exists between given $A$ and $B$. We highlight some more attributes of $\mathcal{H}$ in the following subsection.

:::: {#fig: hyperbola locus .figure latex-placement="h"}
![](Rao2024Trajectory_figs/HYPERBOLA_LOCUS.png)

::: caption
Locus of $\mathbf{o_2}$
:::
::::

## Properties of the hyperbola $\mathcal{H}$ {#subs: math of H}

The analytical expression for $\mathcal{H}$ is significant from theoretical as well as computational perspectives. We start the analysis with a discussion of some useful properties of $\mathcal{H}$.

- The focal length and the length of the semi-major and the semi-minor axes are given by $\Bar{c}=\frac{d(\mathbf{o_3},\mathbf{o_1})}{2}$, $\Bar{a}=\frac{|r_3-r_1|}{2}$ and $\Bar{b}=\sqrt{\Bar{c}^2-\Bar{a}^2}$, respectively.

- We denote the coordinate frame of reference along the semi-major and semi-minor axes as $X'-Y'$. Thereafter, we define $\hat{n}=[n_x,n_y]^T=\frac{\mathbf{o_3-o_1}}{d(\mathbf{o_3},\mathbf{o_1})}$ as a unit vector along the major axis. Then, $R=\begin{bmatrix}
      n_x & -n_y\\
      n_y & n_x
  \end{bmatrix}$ is the rotation matrix between the frames $X-Y$ and $X'-Y'$ (see Fig. [7](#fig: hyperbola locus){reference-type="ref" reference="fig: hyperbola locus"}).

- The parametric expression of $\mathcal{H}$ in $X'-Y'$ axis is $\mathbf{o_2}=[a\sec k,b\tan k]^T$ where $k\in[-\pi/2,3\pi/2)$. Through a sequence of rotation and translation the parametric coordinates of $\mathbf{o_2}$ in $X-Y$ coordinates are given by $$\begin{equation}
      \mathbf{o_2}=R\begin{bmatrix}
          a\sec k\\
          b\tan k
      \end{bmatrix} + \frac{\mathbf{o_1+o_3}}{2}
      \label{eq: o2 centre of c2}
  \end{equation}$$

- Thus, all the points on $\mathcal{H}$ can be parameterised by $k\in[-\pi/2,3\pi/2)$. The range of $k$ is chosen such that a continuous parameterization is achieved for each branch. The right branch is parameterised by $k\in[-\pi/2,\pi/2)$ and the left branch by $k\in[\pi/2,3\pi/2)$.

The existence of the hyperbola is inherently related to $\{A,B\}$ and the values of $\{r_1,r_3\}$. The same is highlighted in the next result.

::: {#corr: existence of H .theorem}
****Theorem** 2**. *Given two oriented points $A$ and $B$, the hyperbola $\mathcal{H}$ exists for any $r_1$ and $r_3$ if $$\begin{equation}
        d(\mathbf{o_3},\mathbf{o_1})>|r_3-r_1|.
        \label{eq: existence of Hyperbola}
\end{equation}$$ where $\mathbf{o_1}$ and $\mathbf{o_3}$ are given by [\[eq:centres o1 and o3\]](#eq:centres o1 and o3){reference-type="eqref" reference="eq:centres o1 and o3"}.*
:::

From the definition of $\mathcal{H}$, we know that the length of the semi-minor axis $\Bar{b}$ is a positive real number. It then follows that $\Bar{c}>\Bar{a}$. This implies that $d(\mathbf{o_3},\mathbf{o_1})>|r_3-r_1|$. Hence, proved. $\square$

Based on the proof of Theorem [2](#corr: existence of H){reference-type="ref" reference="corr: existence of H"}, two interesting cases arise for $\mathcal{H}$:

- In the limiting case of $\Bar{b}=0$, $d(\mathbf{o_3},\mathbf{o_1})=|r_3-r_1|$. This is the condition for the existence of a Circle-Circle trajectory and results in the hyperbolic relation presented in [@RAO]. Equivalently, by using appropriate values of $r_1$ and $r_3$, a Circle-Circle trajectory can be designed within the given framework.

- If $r_1=r_3$, then eqn. [\[eq: hyperbolic relation of centres\]](#eq: hyperbolic relation of centres){reference-type="eqref" reference="eq: hyperbolic relation of centres"} reduces to two super-imposed straight lines. This line is the perpendicular bisector of the line segment joining $\mathbf{o_1}$ and $\mathbf{o_3}$.

To summarise, given two oriented points $A$ and $B$, consider the ordered pair $(r_1,r_3)\in\mathbb{R}^2$. The equation $d(\mathbf{o_3},\mathbf{o_1})=|r_3-r_1|$ gives a hyperbolic relation in $r_1$ and $r_3$ which partitions the $\mathbb{R}^2$ space into two regions as shown in Fig. [8](#fig: partition r1 r3){reference-type="ref" reference="fig: partition r1 r3"}. Note that $(r_1,r_3)=(0,0)$ always satisfies [\[eq: existence of Hyperbola\]](#eq: existence of Hyperbola){reference-type="eqref" reference="eq: existence of Hyperbola"}. Thus, the region highlighted in green in Fig. [8](#fig: partition r1 r3){reference-type="ref" reference="fig: partition r1 r3"} denotes the allowed values of $r_1$ and $r_3$ to construct a feasible $\mathbf{C}^{r_1}\mathbf{C}^{r_2}\mathbf{C}^{r_3}$ trajectory. The boundary results in a Circle-Circle trajectory.

:::: {#fig: partition r1 r3 .figure latex-placement="h"}
![](Rao2024Trajectory_figs/partition_r1_r3.png)

::: caption
Allowed values of $(r_1,r_3)$ for the existence of $\mathbf{C}^{r_1}\mathbf{C}^{r_2}\mathbf{C}^{r_3}$ trajectory (in green)
:::
::::

The design of $\mathbf{C}^{r_1}\mathbf{C}^{r_2}\mathbf{C}^{r_3}$ trajectories can be effectively visualized through the variation of the three parameters $\{r_1,r_3,k\}$. Theorem [2](#corr: existence of H){reference-type="ref" reference="corr: existence of H"} gives the sufficient condition for the existence of such a trajectory. Since each circle can either be a left or right turn, it follows naturally that eight permutations are possible for a $\mathbf{C}^{r_1}\mathbf{C}^{r_2}\mathbf{C}^{r_3}$ trajectory. Next, we proceed to classify these trajectories based on the parameters $\{r_1,r_3,k\}$.

## Classification of trajectories and radius of circle $\mathcal{C}_2$ {#subs: classification of CCC}

Any $\mathbf{C}^{r_1}\mathbf{C}^{r_2}\mathbf{C}^{r_3}$ trajectory can be classified into eight types: $\{LLL,RRR,LLR,RRL,LRR,RLL,LRL,RLR\}$ based upon the orientation of motion on each circular arc. The kind of tangency between any two consecutive circles, which is in turn dependent on the parameters $\{r_1,r_3,k\}$, determines the type of overall trajectory. The following results illustrate the nature and significance of the tangency between the circles in a given $\mathbf{C}^{r_1}\mathbf{C}^{r_2}\mathbf{C}^{r_3}$ trajectory.

::: {#lem: classification 1 .lemma}
****Lemma** 4**. *For any given $r_1$ and $r_3$ such that $r_1r_3<0$,*

1.  *if $k\in(-\pi/2,\pi/2),~\mathcal{C}_2$ is externally tangent to $\mathcal{C}_1$ and internally tangent to $\mathcal{C}_3$, and*

2.  *if $k\in(\pi/2,3\pi/2),~\mathcal{C}_2$ is internally tangent to $\mathcal{C}_1$ and externally tangent to $\mathcal{C}_3$.*
:::

Consider $r_1>0$ and $r_3<0$. We have shown in proof of Theorem [1](#thm: hyperbola of centre){reference-type="ref" reference="thm: hyperbola of centre"} that for the case of internal tangency at $\mathcal{C}_1$ and external tangency at $\mathcal{C}_3$, $d(\mathbf{o_2},\mathbf{o_1})-d(\mathbf{o_2},\mathbf{o_3})=r_3-r_1<0$. Clearly, $\mathbf{o_2}$ belongs to the left branch as it is farther from $\mathbf{o_3}$ than $\mathbf{o_1}$. For the alternate case, $d(\mathbf{o_2},\mathbf{o_1})-d(\mathbf{o_2},\mathbf{o_3})=r_1-r_3>0$. This corresponds to $\mathbf{o_2}$ belonging to the right branch as it is farther from $\mathbf{o_1}$ than $\mathbf{o_3}$. Thus, each branch of the hyperbola results in one particular kind of tangency for any $\mathbf{o_2}$ on that branch. The range of $k$ follows automatically. We can similarly prove the case with $r_1<0$ and $r_3>0$. Hence, proved. $\square$

::: {#lem: classification 2 .lemma}
****Lemma** 5**. *For any given $r_1$ and $r_3$ such that $r_1r_3>0$ and $|r_1|>|r_3|$,*

1.  *if $k\in(-\pi/2,\pi/2),~\mathcal{C}_2$ is externally tangent to both $\mathcal{C}_1$ and $\mathcal{C}_3$, else*

2.  *if $k\in(\pi/2,3\pi/2),~\mathcal{C}_2$ is internally tangent to both $\mathcal{C}_3$ and $\mathcal{C}_1$.*

*For $|r_1|<|r_3|$, the branches switch.*
:::

Consider the case $r_1>0$ and $r_3>0$. We have shown in proof of Theorem [1](#thm: hyperbola of centre){reference-type="ref" reference="thm: hyperbola of centre"} that for internal tangency to both $\mathcal{C}_1$ and $\mathcal{C}_3$, $d(\mathbf{o_2},\mathbf{o_1})-d(\mathbf{o_2},\mathbf{o_3})=r_3-r_1<0$ since $|r_1|>|r_3|$. Clearly, $\mathbf{o_2}$ belongs to the left branch as it is farther from $\mathbf{o_3}$ than $\mathbf{o_1}$. For the case of external tangency, $d(\mathbf{o_2},\mathbf{o_1})-d(\mathbf{o_2},\mathbf{o_3})=r_1-r_3>0$ since $|r_1|>|r_3|$. This corresponds to $\mathbf{o_2}$ belongs to the right branch as it is farther from $\mathbf{o_1}$ than $\mathbf{o_3}$. If $|r_1|<|r_3|$, the branches switch. The range of $k$ follows automatically. We can similarly prove for the case with $r_1<0$ and $r_3<0$ $\square$

Using Lemma [4](#lem: classification 1){reference-type="ref" reference="lem: classification 1"} and Lemma [5](#lem: classification 2){reference-type="ref" reference="lem: classification 2"}, the classification of $\mathbf{C}^{r_1}\mathbf{C}^{r_2}\mathbf{C}^{r_3}$ trajectories for various values of $\{r_1,r_3,k\}$ can done as shown in Table [1](#table: tangency value){reference-type="ref" reference="table: tangency value"}.

:::: center
[]{#table: tangency value label="table: tangency value"}

::: {#table: tangency value}
+------------------+----------------------------------+----------------------------------+
|                  | $k\in[-\pi/2,\pi/2)$             | $k\in[\pi/2,3\pi/2)$             |
+:=================+:=================+:==============+:=================+:==============+
| 2-5              | $|r_1|\geq|r_3|$ | $|r_1|<|r_3|$ | $|r_1|\geq|r_3|$ | $|r_1|<|r_3|$ |
+------------------+------------------+---------------+------------------+---------------+
| $r_1>0$, $r_3>0$ | $LRL$            | $LLL$         | $LLL$            | $LRL$         |
+------------------+------------------+---------------+------------------+---------------+
| $r_1<0$, $r_3<0$ | $RLR$            | $RRR$         | $RRR$            | $RLR$         |
+------------------+------------------+---------------+------------------+---------------+
| $r_1>0$, $r_3<0$ | $LRR$                            | $LLR$                            |
+------------------+----------------------------------+----------------------------------+
| $r_1<0$, $r_3>0$ | $RLL$                            | $RRL$                            |
+------------------+----------------------------------+----------------------------------+

: Classification of $\mathbf{C}^{r_1}\mathbf{C}^{r_2}\mathbf{C}^{r_3}$ trajectories
:::
::::

::: {#remark: eight types for fixed magnitude .remark}
****Remark** 1**. *Consider the case where, for any given $A$ and $B$, only the radii of $\mathcal{C}_1$ and $\mathcal{C}_2$ are specified. In other words, we only have the magnitudes of $r_1$ and $r_3$. In such a scenario, it follows from Table [1](#table: tangency value){reference-type="ref" reference="table: tangency value"} that all eight types of the trajectories ($LLL,RRR,LLR,RRL,LRR,RLL,LRL,RLR$) can be constructed simply by choosing suitable signs of $r_1$ and $r_3$.*
:::

Remark [1](#remark: eight types for fixed magnitude){reference-type="ref" reference="remark: eight types for fixed magnitude"} highlights the existence of a trajectory of each type. The corresponding value of $r_2\in\mathbb{R}$ for each type can be easily computed. Given any $r_1$ and $r_2$, eqn. [\[eq: o2 centre of c2\]](#eq: o2 centre of c2){reference-type="eqref" reference="eq: o2 centre of c2"} gives the coordinates of the center of $\mathcal{C}_2$ and Table [1](#table: tangency value){reference-type="ref" reference="table: tangency value"} states the kind of tangency between $\mathcal{C}_1$ and $\mathcal{C}_2$ for each $k$. Using eqns. [\[eq:centres o1 and o3\]](#eq:centres o1 and o3){reference-type="eqref" reference="eq:centres o1 and o3"} and [\[eq:centre disctance\]](#eq:centre disctance){reference-type="eqref" reference="eq:centre disctance"}, we get the value of $r_2$ with appropriate signs. We derive its expression in a case-wise manner and summarise it in Table [2](#table: r_2 value){reference-type="ref" reference="table: r_2 value"}. Note that we define $s=d(\mathbf{o_2},\mathbf{o_1})$.

:::: center
[]{#table: r_2 value label="table: r_2 value"}

::: {#table: r_2 value}
+------------------+----------------------------------+----------------------------------+
|                  | $k\in[-\pi/2,\pi/2)$             | $k\in[\pi/2,3\pi/2)$             |
+:=================+:=================+:==============+:=================+:==============+
| 2-5              | $|r_1|\geq|r_3|$ | $|r_1|<|r_3|$ | $|r_1|\geq|r_3|$ | $|r_1|<|r_3|$ |
+------------------+------------------+---------------+------------------+---------------+
| $r_1>0$, $r_3>0$ | $-s+r_1$         | $s+r_1$       | $s+r_1$          | $-s+r_1$      |
+------------------+------------------+---------------+------------------+---------------+
| $r_1<0$, $r_3<0$ | $s+r_1$          | $-s+r_1$      | $-s+r_1$         | $s+r_1$       |
+------------------+------------------+---------------+------------------+---------------+
| $r_1>0$, $r_3<0$ | $-s+r_1$                         | $s+r_1$                          |
+------------------+----------------------------------+----------------------------------+
| $r_1<0$, $r_3>0$ | $s+r_1$                          | $-s+r_1$                         |
+------------------+----------------------------------+----------------------------------+

: Analytical expressions of $r_2$
:::
::::

The above table can be alternatively expressed compactly in the following form. $$\begin{align}
    r_2=\begin{dcases}
        \text{sign}(r_1(|r_1|-|r_3|)(k-\frac{\pi}{2}))s+r_1&, r_1r_2>0\\
        \text{sign}(r_1(k-\frac{\pi}{2}))s+r_1&, r_1r_2<0
    \end{dcases}
\end{align}$$ where $$\begin{equation*}
    \text{sign}(x)=\begin{dcases}
        ~~1, &x\geq0\\
        -1, &x<0
    \end{dcases}
\end{equation*}$$ With the radius of the $\mathcal{C}_2$ appropriately defined, the analytical expression for the two changeover points $\{\mathbf{c_1,c_2}\}$ can be written as $$\begin{align}
        \mathbf{c_1}&=\frac{r_2\mathbf{o_1}-r_1\mathbf{o_2}}{r_2-r_1}\\
        \mathbf{c_2}&=\frac{r_2\mathbf{o_3}-r_3\mathbf{o_2}}{r_2-r_3}
        \label{eq: changeover points c_1 c_2}
    \end{align}$$ Finally, we put forth an interesting observation on $\mathcal{C}_2$.

::: {#corr: r_2 infinity .corollary}
****Corollary** 1**. *For $k=\pm\frac{\pi}{2}$, $\mathcal{C}_2$ limits to a straight line (a circle with infinite radius) tangent to both $\mathcal{C}_1$ and $\mathcal{C}_3$.*
:::

For $k$ tending to $\pm\pi/2$, it follows from Table [2](#table: r_2 value){reference-type="ref" reference="table: r_2 value"} that $s$ and, equivalently, $|r_2|$ tend to $\infty$. Additionally, we know from Theorem [1](#thm: hyperbola of centre){reference-type="ref" reference="thm: hyperbola of centre"}, $\mathcal{C}_2$ is always tangent to the other two circles. Thus, $\mathcal{C}_2$ limits to a straight line tangent to $\mathcal{C}_1$ and $\mathcal{C}_3$. Hence, proved. $\square$

Note that Corollary [1](#corr: r_2 infinity){reference-type="ref" reference="corr: r_2 infinity"} states that as $k$ tends $\pm\pi/2$, the $\mathbf{C}^{r_1}\mathbf{C}^{r_2}\mathbf{C}^{r_3}$ trajectory limits to a CSC trajectory ($C^{r_1}C^{\pm\infty}C^{r_3}$ trajectory). Thus, the proposed trajectory design encapsulates all of the forms of the Dubins Shortest Paths for appropriate variation of the three circles.

The analysis of $\mathbf{C}^{r_1}\mathbf{C}^{r_2}\mathbf{C}^{r_3}$ trajectories presented in this section is without any explicit constraints of a desired length of the trajectory or curvature boundedness. In the following sections, we proceed to analyse the variation of the length of the trajectory with parameters $\{r_1,r_3,k\}$ and derive the set of reachable lengths using the proposed trajectory between any pair of oriented points.

# Variation of $k$ for Circle-Circle-Circle trajectories

Every attribute of a Circle-Circle-Circle trajectory (like $\mathbf{c_1,c_2},r_2$, *etc.*) can written as a function of the parameter $k$ for fixed values of $r_1$ and $r_3$. We define a function $l:[-\pi/2,3\pi/2)\longrightarrow\mathbb{R}^+$ as the length of trajectory for fixed values of $r_1$ and $r_3$. The parameter $k$ varies in the range $[-\pi/2,3\pi/2)$. This variation of $k$ can be further divided into two parts: $k\in[-\pi/2,\pi/2)$ and $k\in[\pi/2,3\pi/2)$, i.e., over each branch of $\mathcal{H}$. The following interesting results then arise:

- Such a variation of $k$ results in distinct types of $\mathbf{C}^{r_1}\mathbf{C}^{r_2}\mathbf{C}^{r_3}$ trajectories for each branch of $\mathcal{H}$ (which is discussed elaborately in Sec. [4.3](#subs: classification of CCC){reference-type="ref" reference="subs: classification of CCC"}).

- An infinite elongation of the trajectory can be achieved within each branch of $\mathcal{H}$.

We analyze the impact of these variations on the changeover points and the length of trajectory in a case-wise manner. []{#section: traj of desired length label="section: traj of desired length"}

**Case 1:** $r_1r_3>0$

We know that for both $k=\pi/2$ and $k=-\pi/2$, $\mathcal{C}_2$ becomes a common tangent line to $\mathcal{C}_1$ and $\mathcal{C}_3$. These tangents, as shown in Fig. [9](#fig: partition of circle 1){reference-type="ref" reference="fig: partition of circle 1"}, divide the boundary of each circle into two parts. We label them as $\mathcal{B}_1$ and $\mathcal{B}_2$ as shown in Fig. [9](#fig: partition of circle 1){reference-type="ref" reference="fig: partition of circle 1"}. One of the variations in $k$ results in $\mathcal{C}_2$ being externally tangent to both $\mathcal{C}_1$ and $\mathcal{C}_3$. Under such a variation, the changeover points lie in $\mathcal{B}_2$ for both $\mathcal{C}_1$ and $\mathcal{C}_3$ as shown in Fig. [10](#fig: case 1 ext){reference-type="ref" reference="fig: case 1 ext"}.

:::: {#fig: partition of circle 1 .figure latex-placement="h"}
![](Rao2024Trajectory_figs/partition_of_circle_2.png)

::: caption
Common tangents for $\mathcal{C}_1$ and $\mathcal{C}_3$ for $r_Ar_B>0$
:::
::::

The other variation results in $\mathcal{C}_2$ being internally tangent to both $\mathcal{C}_1$ and $\mathcal{C}_3$. The changeover points lie in $\mathcal{B}_1$ for both $\mathcal{C}_1$ and $\mathcal{C}_3$ in such a case as shown in Fig. [11](#fig: case 1 int){reference-type="ref" reference="fig: case 1 int"}. For both of the variations, the lengths of the $\mathbf{C}^{r_1}\mathbf{C}^{r_2}\mathbf{C}^{r_3}$ trajectories tend to infinity at one end of each branch of $\mathcal{H}$.

:::: {#fig:three graphs .figure latex-placement="htbp"}
![$\mathcal{C}_2$ externally tangent to both $\mathcal{C}_1$ and $\mathcal{C}_3$](Rao2024Trajectory_figs/ELONGATION_1.png){#fig: case 1 ext width="\\textwidth"}

![$\mathcal{C}_2$ internally tangent to both $\mathcal{C}_1$ and $\mathcal{C}_3$](Rao2024Trajectory_figs/ELONGATION_2.png){#fig: case 1 int width="85%"}

![$\mathcal{C}_2$ externally tangent to $\mathcal{C}_1$ and internally tangent to $\mathcal{C}_3$](Rao2024Trajectory_figs/ELONGATION_2_1.png){#fig: case 2_1 width="\\textwidth"}

![$\mathcal{C}_2$ internally tangent to $\mathcal{C}_1$ and externally tangent to $\mathcal{C}_3$](Rao2024Trajectory_figs/ELONGATION_2_2.png){#fig: case 2_2 width="\\textwidth"}

::: caption
Variation of $\mathcal{C}_2$ in a $\mathbf{C}^{r_1}\mathbf{C}^{r_2}\mathbf{C}^{r_3}$ trajectory
:::
::::

**Case 2:** $r_1r_3<0$

In contrast to the previous case, the tangents, arising out $k=\pi/2$ and $k=-\pi/2$, take the form shown in Fig. [15](#fig: partition of circle 2){reference-type="ref" reference="fig: partition of circle 2"}. As before, they divide the boundary of each circle into two parts: $\mathcal{B}_1$ and $\mathcal{B}_2$. The variation of $k$ in $[-\pi/2,\pi/2)$ results in $\mathcal{C}_2$ being externally tangent to $\mathcal{C}_1$ and internally tangent to $\mathcal{C}_3$. Unlike the previous case, the changeover points lie in $\mathcal{B}_2$ for $\mathcal{C}_1$ and in $\mathcal{B}_2$ for $\mathcal{C}_3$ under such a variation as shown in Fig. [12](#fig: case 2_1){reference-type="ref" reference="fig: case 2_1"}. The other variation results in $\mathcal{C}_2$ being internally tangent to $\mathcal{C}_1$ and externally tangent to $\mathcal{C}_3$ as shown in Fig. [13](#fig: case 2_2){reference-type="ref" reference="fig: case 2_2"}. For both of the variations, the lengths of the $\mathbf{C}^{r_1}\mathbf{C}^{r_2}\mathbf{C}^{r_3}$ trajectories tend to infinity at one end of each branch of $\mathcal{H}$.

:::: {#fig: partition of circle 2 .figure latex-placement="H"}
![](Rao2024Trajectory_figs/partition_of_circle.png)

::: caption
Common tangents for $\mathcal{C}_1$ and $\mathcal{C}_3$ for $r_Ar_B<0$
:::
::::

Note that while $l(k)$ goes to infinity for each variation of $k$, $l(k)$ is not always continuous. This is illustrated through the following result.

::: {#lem: jump discontinuity .lemma}
****Lemma** 6**. *Consider two oriented points $A$ and $B$. For fixed values of $r_1,r_3\in\mathbb{R}$, $l(\cdot)$ has at most two discontinuities. The points of discontinuity, if they exist, are at $k_a$ and $k_b$ where $\mathbf{c_1}(k_a)=\mathbf{a}$ and $\mathbf{c_2}(k_b)=\mathbf{b}$. Moreover, these discontinuities are jump discontinuities of magnitude $2\pi |r_1|$ at $k=k_a$ and $2\pi |r_3|$ at $k=k_b$.*
:::

For each of the variations of $k$, we discussed in the preceding paragraphs how $\mathbf{c_1}$ and $\mathbf{c_2}$, i.e., the changeover points, vary continuously in either $\mathcal{B}_1$ or $\mathcal{B}_2$. Let $k_a$ and $k_b$ be values such that $\mathbf{c_1}(k_a)=\mathbf{a}$ and $\mathbf{c_2}(k_b)=\mathbf{b}$. Consider an infinitesimal variation of $k$ around the point $k=k_a$ and the resulting trajectories as shown in Fig. [16](#fig: discontinuity of l){reference-type="ref" reference="fig: discontinuity of l"}.

:::: {#fig: discontinuity of l .figure latex-placement="H"}
![](Rao2024Trajectory_figs/proof_disc_l.png)

::: caption
Jump discontinuity in $l(\cdot)$
:::
::::

It is easy to see in Fig. [6](#fig:traj_cc){reference-type="ref" reference="fig:traj_cc"} that the arc length of $\widearc{\mathbf{c_1c_2}}$ and $\widearc{\mathbf{c_2b}}$ is continuous along this infinitesimal variation around $k_a$. However, the arc length of $\widearc{\mathbf{ac_1}}$ tends to $0$ as $k_a^+$ tends to $k_a$ and $\widearc{\mathbf{ac}_1}$ tends to $2\pi |r_1|$ as $k_a^-$ tends to $k_a$. Thus, $l(\cdot)$ is discontinuous at $k=k_a$. Note that in the above case, $l(k)$ jumps down by $2\pi |r_1|$ at $k=k_a$. If the location of $\mathbf{c_1}(k_a^+)$ and $\mathbf{c_1}(k_a^-)$ were switched, $l(k)$ would have jumped up by $2\pi|r_1|$. A similar discontinuity exists at $k=k_b$. Hence, proved. $\square$

It is important to note that the discontinuities at $k_a$ and $k_b$ need not occur simultaneously. Further, if $\mathbf{c_1}(k)$ is not equal to $\mathbf{a}$ and $\mathbf{c_b}(k)$ is not equal to $\mathbf{b}$ for any $k$ varying over one branch of the hyperbola, we get a continuous elongation of $l(k)$ to infinity. This is true only if no curvature constraints are imposed on the trajectory. *Through these results, we observe that the variation of $k$ results in interesting properties pertaining to the length of the trajectory.* We use these results along with the imposition of curvature constraint to determine the set reachable lengths between any two oriented points in the following section.

# Curvature-bounded Circle-Circle-Circle trajectory of desired length {#sec: reachability set}

With important observations arising out of the variation of parameter $k$ as discussed in the previous section, we are now able to state the set of reachable lengths. We begin the analysis with a reference to [@chen_elongation] for a characterisation of pairs of oriented points $(A,B)$ based upon the kind of Dubins Shortest Path ($\Lambda_m$) between them: $$\label{eq: classification of O}
\begin{align}
        \mathcal{O}_1&=\{(A,B) | \Lambda_m\in C_{\eta}S_dC_{\zeta}\text{ with } \eta\geq\pi\}\\
        \mathcal{O}_2&=\{(A,B) | \Lambda_m\in C_{\eta}S_dC_{\zeta}\text{ with } \zeta\geq\pi\}\\
        \mathcal{O}_3&=\{(A,B) | \Lambda_m\in C_{\eta}S_dC_{\zeta}\text{ with } d\geq4r_{\min}\}\\
        \mathcal{O}_4&=\{(A,B) | \Lambda_m\in C_{\eta}S_dC_{\zeta}\text{ with } \newline d(\mathbf{c}^r_A,\mathbf{c}^r_B)\geq4r_{\min}\}\\
        \mathcal{O}_5&=\{(A,B) | \Lambda_m\in C_{\eta}S_dC_{\zeta}\text{ with } \newline d(\mathbf{c}^l_A,\mathbf{c}^l_B)\geq4r_{\min}\}
\end{align}$$ where $\eta$ and $\zeta$ are the arc lengths of the first and third circles, respectively, and $d$ is the length of the straight line path. Let $\mathcal{O}:=\mathcal{O}_1\cup\mathcal{O}_2\cup\mathcal{O}_3\cup\mathcal{O}_4\cup\mathcal{O}_5$ and $\mathcal{O}^c$ be the its complementary set $$\begin{equation*}
    \mathcal{O}^c=\{(A,B) | \Lambda_m\in CSC, (A,B)\notin \mathcal{O}\}.
\end{equation*}$$

Based upon the above characterisation, the authors in [@chen_elongation] classify the set of reachable lengths for any two oriented points as:

::: {#thm: maximal reachable lengths .theorem}
****Theorem** 3** ([@chen_elongation] ). *Given any two oriented points $A$ and $B$ so that $A\neq B$, the following statements hold:*

- *If $(A,B)\notin\mathcal{O}\cup\mathcal{O}^c$, for every $l_o\geq l_m$ there exists a trajectory $\Lambda$ so that $l(\Lambda)=l_o$.*

- *If $(A,B)\in\mathcal{O}$, for every $l_o\geq l_m$ there exists a trajectory $\Lambda$ so that $l(\Lambda)=l_o$.*

- *If $(A,B)\in\mathcal{O}^c$, we have that (a) for every $l_o\in[l_m,l_1]\cup[l_2,\infty)$ there exists a trajectory $\Lambda$ so that $l(\Lambda)=l_o$; and (b) for any trajectory $\Lambda$ we have $l(\Lambda)\notin(l_1,l_2)$.*
:::

where $l_o$ is the length of the desired trajectory and $$\label{eq: l1 l2 definition}
\begin{align}
    l_1&:=\max\{l^s_{LRL},l^s_{RLR}\}\\
    l_2&:=\min\{l_m+2\pi r_{\min},l^l_{LRL},l^l_{RLR},\{l_{RSR},l_{LSL},l_{RSL},l_{LSR}\}\setminus\{l_m\}\}
\end{align}$$

:::: {#fig: lrl rlr 2 .figure latex-placement="h"}
![](Rao2024Trajectory_figs/lrl_rlr_2.png){width="50%"}

::: caption
Two $LRL$ trajectories (in red) and $RLR$ trajectories (in blue) between $A$ and $B$
:::
::::

The various lengths of trajectory mentioned in [\[eq: l1 l2 definition\]](#eq: l1 l2 definition){reference-type="eqref" reference="eq: l1 l2 definition"} have been elaborated in [@chen_elongation]. For $(A,B)\in\mathcal{O}^c$, there exist two $LRL$ and $RLR$ trajectories with the magnitude of curvature being $1/|r_{\min}|$ throughout as shown in Fig. [17](#fig: lrl rlr 2){reference-type="ref" reference="fig: lrl rlr 2"} in red and blue, respectively. Note that there exists a continuous elongation between the two $LRL$ (or $RLR$) trajectories if there were no curvature constraints. We denote the length of the longer $LRL$ trajectory as $l_{LRL}^l$ and the shorter one as $l_{LRL}^s$. The lengths $l_{RLR}^l$ and $l_{RLR}^s$ are defined similarly. These lengths are used to determine $l_1$ and $l_2$ in eqn. [\[eq: l1 l2 definition\]](#eq: l1 l2 definition){reference-type="eqref" reference="eq: l1 l2 definition"}. Further, the following result holds for the remaining of the trajectories in eqn. [\[eq: l1 l2 definition\]](#eq: l1 l2 definition){reference-type="eqref" reference="eq: l1 l2 definition"} as shown in [@chen_elongation].

::: {#lem: anti parallel tangent .lemma}
****Lemma** 7** ([@chen_elongation]). *If $(A,B)\in\mathcal{O}^c$, each CSC-path, with its length in $\{l_{RSR},l_{LSL},l_{RSL},l_{LSR}\}\setminus\{l_m\}$, has anti-parallel tangents.*
:::

Lemma [7](#lem: anti parallel tangent){reference-type="ref" reference="lem: anti parallel tangent"} highlights that for each CSC-path, with its length in $\{l_{RSR},l_{LSL},l_{RSL},l_{LSR}\}\setminus\{l_m\}$, has either $\eta\geq\pi$ or $\zeta\geq\pi$. With these observations, we present the elongation strategies for the Dubins Shortest Path to achieve a $\mathbf{C}^{r_1}\mathbf{C}^{r_2}\mathbf{C}^{r_3}$ trajectory of a desired length between any two oriented points.

## Elongation of a trajectory for $(A,B)\notin\mathcal{O}\cup\mathcal{O}^c$

The set of ordered pairs $(A,B)\notin\mathcal{O}\cup\mathcal{O}^c$ corresponds to the cases where the Dubins Shortest Path is a CCC trajectory. The following theorem illustrates the elongation strategy for such cases.

::: {#lem: CCC ELONGATION .theorem}
****Theorem** 4**. *Given oriented points $A$ and $B$ such that $(A,B)\notin\mathcal{O}\cup\mathcal{O}^c$, there always exists a $\mathbf{C}^{r_1}\mathbf{C}^{r_2}\mathbf{C}^{r_3}$ trajectory of any desired length $l_o\in[l_m,\infty)$.*
:::

:::: {#fig:ccc elongation .figure latex-placement="h"}
![](Rao2024Trajectory_figs/CCC_DUBINS.png)

::: caption
Elongation of CCC Dubins Shortest Path
:::
::::

It is shown in [@dubins] that if the Dubins Shortest Path is of the form CCC, the arc length of the middle circle is greater than or equal to $\pi r_{\min}$. Thus, the minimum length trajectory is shown in red in Fig. [18](#fig:ccc elongation){reference-type="ref" reference="fig:ccc elongation"} (for $LRL$). If we increase the magnitude of $r_2$, we get a continuous elongation till infinity. We can elongate the Dubins Shortest Path of form $RLR$ similarly. Hence, proved. $\square$

## Elongation of a trajectory for $(A,B)\in\mathcal{O}$

The set $\mathcal{O}$ is formed by the union of five different sets given by eqn. [\[eq: classification of O\]](#eq: classification of O){reference-type="eqref" reference="eq: classification of O"}. We first present an important observation on this set.

::: {#lem: not in o3 .lemma}
****Lemma** 8**. *For all $(A,B)\in\mathcal{O}_3$, $(A,B)\in\mathcal{O}_1\cup\mathcal{O}_2\cup\mathcal{O}_4\cup\mathcal{O}_5$.*
:::

Consider the the Dubins Shortest Path between any $(A,B)\in\mathcal{O}_3$ as a $C_{\eta}S_dC_{\zeta}$ trajectory. Clearly, if $\eta\geq\pi$ or $\zeta\geq\pi$, $(A,B)\in\mathcal{O}_1\cup\mathcal{O}_2$. We now focus on the case of $\eta<\pi$ and $\zeta<\pi$. If the trajectory is of form $RSR$, $d(\mathbf{c}^r_A,\mathbf{c}^r_B)=d\geq4r_{\min}$ implying $(A,B)\in\mathcal{O}_4$. Similarly, $(A,B)\in\mathcal{O}_5$ if the trajectory is of the form $LSL$.

If the trajectory is of the form $RSL$, the same has been shown in Fig. [19](#fig: rsl o3 not){reference-type="ref" reference="fig: rsl o3 not"}. Construct the normal lines at the endpoints of the straight line segment (labelled as $n_1$ and $n_2$) and circle $\mathcal{C}_A^l$. As $\eta<\pi$, the point $\mathbf{c}^l_A$ lies to the left of or on the normal line $n_1$. Clearly, $d(\mathbf{c}^l_A,\mathbf{c}^l_B)\geq d\geq4r_{\min}$. Thus, $(A,B)\in\mathcal{O}_5$. Note that we can similarly show that $d(\mathbf{c}^r_A,\mathbf{c}^r_B)\geq d\geq4r_{\min}$ and $(A,B)\in\mathcal{O}_4$ for this case. Further, the case of $LSR$ path can be proven similarly. Hence, proved.

:::: {#fig: rsl o3 not .figure latex-placement="h"}
![](Rao2024Trajectory_figs/fig_rsl_o3.png)

::: caption
For a Dubins Shortest Path of form $RSL$ $d(\mathbf{c}^l_A,\mathbf{c}^l_B)\geq4r_{\min}$
:::
::::

$\square$

The sets given in eqn. [\[eq: classification of O\]](#eq: classification of O){reference-type="eqref" reference="eq: classification of O"} are not mutually disjoint. There exist certain pairs of $(A,B)$ that belong to a unique set and certain pairs that belong to multiple sets. Fig. [20](#fig: belong all){reference-type="ref" reference="fig: belong all"} illustrates a pair of oriented point that belongs to $\mathcal{O}_1\cap\mathcal{O}_4\cap\mathcal{O}_5$. However, Lemma [8](#lem: not in o3){reference-type="ref" reference="lem: not in o3"} illustrates that $\mathcal{O}_3$ does not have any unique elements. Thus, it is sufficient to construct elongation strategies for the remaining four sets to explore a continuous elongation in $\mathcal{O}$. We analyse each of these sets separately. We begin by presenting the following result which discusses elongation strategies for set $\mathcal{O}_1\cup\mathcal{O}_2$.

:::: {#fig: belong all .figure latex-placement="h"}
![](Rao2024Trajectory_figs/belong_all.png)

::: caption
CSC Dubins Shortest Path for some $(A,B)\in\mathcal{O}_1\cap\mathcal{O}_4\cap\mathcal{O}_5$
:::
::::

::: {#lem: CSC great pi ELONGATION .lemma}
****Lemma** 9**. *Given oriented points $A$ and $B$ such that $(A,B)\in\mathcal{O}_1\cup\mathcal{O}_2$, there always exists $\mathbf{C}^{r_1}\mathbf{C}^{r_2}\mathbf{C}^{r_3}$ trajectory of any desired length $l_o\in[l_m,\infty)$.*
:::

We begin the proof by considering the set $\mathcal{O}_1$. Thus, $\eta\geq\pi$. We divide the proof into two cases.

**Case 1**: Let the $CSC$ trajectory be of form $RSR$. Clearly, $\mathbf{a}\in\mathcal{B}_2$. We continuously deform $\mathcal{C}_2$ as shown in Fig. [11](#fig: case 1 int){reference-type="ref" reference="fig: case 1 int"}. If $\mathbf{b}\in\mathcal{B}_2$, this elongation will be continuous till infinity.

On the contrary, if $\mathbf{b}\in\mathcal{B}_1$, there exists a $k_b$ such that $\mathbf{c_2}(k_b)=\mathbf{b}$. Construct circle $\mathcal{C}^l_B$ and a transverse tangent between $\mathcal{C}_1$ and $\mathcal{C}^l_B$. This construction is shown in Fig. [21](#fig: rsr 1){reference-type="ref" reference="fig: rsr 1"}. The point $\mathbf{x}$ divides $\mathcal{B}_2$ into two arcs denoted by $\mathcal{B}_2^I$ and $\mathcal{B}_2^{II}$. If $\mathbf{a}\in\mathcal{B}_2^I$, we deform $\mathcal{C}_2$ and get a series $RRR$ trajectories until point $k_b$ is reached as shown by a green curve in Fig. [21](#fig: rsr 1){reference-type="ref" reference="fig: rsr 1"}. This is an $RR$ trajectory. If we continue further, we will have a jump of $2\pi|r_3|$ as discussed in Lemma [6](#lem: jump discontinuity){reference-type="ref" reference="lem: jump discontinuity"}. To ascertain a continuous elongation of the length of the trajectory, we proceed to deform $\mathcal{C}_2$ such that it is internally tangent to $\mathcal{C}_1$ and externally to $\mathcal{C}_B^l$ as shown in blue in Fig. [21](#fig: rsr 1){reference-type="ref" reference="fig: rsr 1"} resulting in a $RRL$ trajectory. Since $\mathbf{a}\in\mathcal{B}_2^{I}$, we will have a continuous elongation until $|r_2|$ goes to infinity as shown in Fig. [21](#fig: rsr 1){reference-type="ref" reference="fig: rsr 1"}.

:::: {#fig: rsr .figure latex-placement="h"}
![$\mathbf{a}\in\mathcal{B}_2^{I}$ and $\mathbf{b}\in\mathcal{B}_1$](Rao2024Trajectory_figs/fig_lsl.png){#fig: rsr 1 width="\\textwidth"}

![$\mathbf{a}\in\mathcal{B}_2^{II}$ and $\mathbf{b}\in\mathcal{B}_1$](Rao2024Trajectory_figs/fig_lsl_2.png){#fig: rsr 2 width="\\textwidth"}

::: caption
Elongation of $C_{\eta}S_dC_{\zeta}$ trajectory with $\eta\geq\pi$
:::
::::

If $\mathbf{a}\in\mathcal{B}_2^{II}$, construct $\mathcal{C}^l_A$. We deform $\mathcal{C}_2$ similarly as in the previous case until the point $k_a$ is reached such that $\mathbf{c_1}(k_a)=a$ before the length of trajectory goes to infinity. This is an $RL$ trajectory as shown by the yellow curve in Fig. [22](#fig: rsr 2){reference-type="ref" reference="fig: rsr 2"}. If we proceed similarly, we get a jump discontinuity of $2\pi|r_1|$. Instead, we now deform $\mathcal{C}_2$ such that it is externally tangent to both $\mathcal{C}^l_A$ and $\mathcal{C}^l_B$ resulting in $LRL$ trajectories and a continuous deformation after $k=k_a$ until the length reaches infinity. Note that in all the cases, $|r_2|\geq r_{\min}$. Thus, the curvature constraint on the trajectory is not violated. We can similarly achieve a continuous elongation of an $LSL$ path with $\eta\geq\pi$.

**Case 2**: Let the $CSC$ trajectory be of form $RSL$. For $\eta\geq\pi$, $\mathbf{a}$ can lie in either $\mathcal{B}_1$ or $\mathcal{B}_2$. If $\mathbf{a}\in\mathcal{B}_2$, we deform $\mathcal{C}_2$ as shown in Fig. [13](#fig: case 2_2){reference-type="ref" reference="fig: case 2_2"} such that $\mathbf{c_1}\neq\mathbf{a}$ always. Further, if $\mathbf{b}\in\mathcal{B}_1$, we get a continuous elongation as $\mathbf{c_2}\in\mathcal{B}_2$ and no jump discontinuity is encountered. If $\mathbf{b}\in\mathcal{B}_2$, there exist a $k_b$ such that $\mathbf{c_2}(k_b)=\mathbf{b}$. However, there is a jump down discontinuity and the set of reachable lengths is given by $l\in[l_m,l_b+2\pi|r_3|)\cup[l_b,\infty)=[l_m,\infty)$ where $l(k_b)=l_b$. Thus, a continuous elongation of the trajectory exists until its length goes to infinity.

:::: {#fig: lsr elong .figure latex-placement="h"}
![](Rao2024Trajectory_figs/fig_lsr.png)

::: caption
Elongation of $RSL$ trajectory with $\eta\geq\pi$ where $\mathbf{a}\in\mathcal{B}_1$ and $\mathbf{b}\in\mathcal{B}_1$
:::
::::

If $\mathbf{a}\in\mathcal{B}_1$, we again proceed in a case-wise manner. If $\mathbf{b}\in\mathcal{B}_2$, we deform $\mathcal{C}_2$ as shown in Fig. [12](#fig: case 2_1){reference-type="ref" reference="fig: case 2_1"}. For such a variation, $\mathbf{c_1}\in\mathcal{B}_2$ and $\mathbf{c_2}\in\mathcal{B}_1$ resulting in no jump discontinuities and we get a continuous elongation of the trajectory till infinity. If $\mathbf{b}\in\mathcal{B}_2$, we proceed in a similar manner as the case of $\mathbf{a}\in\mathcal{B}_2^{II}$ in Case 1. The same has been highlighted in Fig. [24](#fig: lsr elong){reference-type="ref" reference="fig: lsr elong"}. We can similarly achieve a continuous elongation for an $LSR$ path.

The elongation strategies mentioned here can be similarly applied to the cases where $\zeta\geq\pi$, i.e., $(A,B)\in\mathcal{O}_2$. Thus, a continuous elongation of trajectory exist using $\mathbf{C}^{r_1}\mathbf{C}^{r_2}\mathbf{C}^{r_3}$ trajectory for all $(A,B)\in\mathcal{O}_1\cup\mathcal{O}_2$. Hence, proved. $\square$

An important idea emerges from the proof of Lemma [9](#lem: CSC great pi ELONGATION){reference-type="ref" reference="lem: CSC great pi ELONGATION"}. The deformation of $\mathcal{C}_2$ is realised by the variation of the parameter $k$. If the point $k_a$ (or $k_b$), defined in Lemma [6](#lem: jump discontinuity){reference-type="ref" reference="lem: jump discontinuity"}, is reached in this deformation, one should switch $\mathcal{C}_1$ (or $\mathcal{C}_3$) from $\mathcal{C}^l_A$ to $\mathcal{C}^r_A$ or vice-versa (or $\mathcal{C}^l_B$ to $\mathcal{C}^r_B$ or vice-versa) for further deformation of $\mathcal{C}_2$ instead of proceeding on the same circle. The arc length of $\widearc{\mathbf{ac_1}}$ (or $\widearc{\mathbf{c_2b}}$) goes to zero as $k_a$ (or $k_b$) is approached and starts increasing after the switch, preserving its continuity and, in turn, the continuity of the overall length of trajectory (see Fig. [25](#fig: cont elong){reference-type="ref" reference="fig: cont elong"}). The switching of the terminal circles can be alternatively viewed as changing $r_1$ (or $r_3$) from $r_{\min}$ to $-r_{\min}$ or vice versa.

:::: {#fig: cont elong .figure latex-placement="h"}
![](Rao2024Trajectory_figs/cont_elong.png)

::: caption
Continuous elongation of $\mathbf{C}^{r_1}\mathbf{C}^{r_2}\mathbf{C}^{r_3}$ trajectory
:::
::::

We now discuss the set $\mathcal{O}_4\cup\mathcal{O}_5$. Clearly, any pair $(A,B)\in\mathcal{O}_4\cup\mathcal{O}_5$ such that $\eta\geq\pi$ or $\zeta\geq\pi$ can be elongated continuously to infinitely large lengths from Lemma [9](#lem: CSC great pi ELONGATION){reference-type="ref" reference="lem: CSC great pi ELONGATION"}. We analyse the remaining cases in the following result.

::: {#lem: CSC great d(o) ELONGATION .lemma}
****Lemma** 10**. *Given oriented points $A$ and $B$ such that $(A,B)\in\mathcal{O}_4\cup\mathcal{O}_5$ with $\eta<\pi$ and $\zeta<\pi$, there always exists a $\mathbf{C}^{r_1}\mathbf{C}^{r_2}\mathbf{C}^{r_3}$ trajectory of any desired length $l_o\in[l_m,\infty)$.*
:::

:::: {#fig: O4 O5 .figure latex-placement="h"}
![$\Lambda_m$ is of the form $RSR$](Rao2024Trajectory_figs/fig_lsl_o4.png){width="\\textwidth"}

![$\Lambda_m$ is of the form $RSL$](Rao2024Trajectory_figs/fig_rsl_great_4r.png){width="\\textwidth"}

::: caption
Elongation of $C_{\eta}S_dC_{\zeta}$ trajectory with $d(\mathbf{c}^l_A,\mathbf{c}^l_B)\geq4r_{\min}$
:::
::::

The proof is similar to that of Lemma [9](#lem: CSC great pi ELONGATION){reference-type="ref" reference="lem: CSC great pi ELONGATION"}. It can be illustrated for different cases of $RSR$ and $RSL$ trajectories through Fig. [26](#fig: O4 O5){reference-type="ref" reference="fig: O4 O5"}. $\square$

The following theorem follows from Lemma [9](#lem: CSC great pi ELONGATION){reference-type="ref" reference="lem: CSC great pi ELONGATION"} and [10](#lem: CSC great d(o) ELONGATION){reference-type="ref" reference="lem: CSC great d(o) ELONGATION"}.

::: {#lem: set O ELONGATION .theorem}
****Theorem** 5**. *Given oriented points $A$ and $B$ such that $(A,B)\in\mathcal{O}$, there exists $\mathbf{C}^{r_1}\mathbf{C}^{r_2}\mathbf{C}^{r_3}$ trajectory for all lengths $l_o\in[l_m,\infty)$.*
:::

## Elongation of trajectory for $(A,B)\in\mathcal{O}^{c}$

For all $(A,B)\in\mathcal{O}^c$, there exist trajectories of lengths $l_{LRL}^s$ and $l_{RLR}^s$ as shown in Fig. [17](#fig: lrl rlr 2){reference-type="ref" reference="fig: lrl rlr 2"}. Using the definitions of $l_1$ and $l_2$ from [\[eq: l1 l2 definition\]](#eq: l1 l2 definition){reference-type="eqref" reference="eq: l1 l2 definition"}, the following result illustrates the elongation strategy for such cases.

::: {#lem: set OC elongation .theorem}
****Theorem** 6**. *Given oriented points $A$ and $B$ such that $(A,B)\in\mathcal{O}^c$, there always exists a $\mathbf{C}^{r_1}\mathbf{C}^{r_2}\mathbf{C}^{r_3}$ trajectory of any desired length $l_o\in[l_m,l_1]\cup[l_2,\infty)$ where $l_1$ and $l_2$ are given by eqn. [\[eq: l1 l2 definition\]](#eq: l1 l2 definition){reference-type="eqref" reference="eq: l1 l2 definition"}.*
:::

Consider the trajectories whose lengths are mentioned in [\[eq: l1 l2 definition\]](#eq: l1 l2 definition){reference-type="eqref" reference="eq: l1 l2 definition"}. Without loss of generality, let $l_1=l_{RLR}^s$. Fig. [27](#fig: lsl_oc){reference-type="ref" reference="fig: lsl_oc"} shows the elongation strategy for an $LSL$ minimum path. We deform $\mathcal{C}_2$ resulting in a series of $LLL$ trajectories until point $k_a$ is reached. This trajectory is of the type $LL$. To preserve the continuity of elongation, we construct $\mathcal{C}_2$ between $\mathcal{C}^r_A$ and $\mathcal{C}_3$ resulting in a series of $RLL$ trajectories until a point $k_b$ is reached. Henceforth, $\mathcal{C}_2$ is constructed such that it is externally tangent to $\mathcal{C}^r_A$ and $\mathcal{C}^r_B$ forming a series of $RLR$ trajectories. This $\mathcal{C}_2$ is deformed until we get a trajectory whose length is $l_{RLR}^s$. Thus, a $\mathbf{C}^{r_1}\mathbf{C}^{r_2}\mathbf{C}^{r_3}$ trajectory exists for every $l_o\in[l_m,l_1]$. Note that it might happen that $k_b$ is reached earlier than $k_a$. In such a case, $\mathcal{C}_3$ is switched first. The proof follows similarly.

:::: {#fig: lsl_oc .figure latex-placement="h"}
![](Rao2024Trajectory_figs/lsl_oc.png){width="65%"}

::: caption
Elongation of trajectory from $l_m$ to $l_1$ when $(A,B)\in\mathcal{C}^c$
:::
::::

Clearly, trajectories of length $\{l_{RLR}^l,l_{LRL}^l\}$ have arc lengths of $\mathcal{C}_2$ greater than $\pi r_{\min}$ as shown in Fig. [17](#fig: lrl rlr 2){reference-type="ref" reference="fig: lrl rlr 2"}. These can be continuously elongated till infinity using strategies in Theorem [4](#lem: CCC ELONGATION){reference-type="ref" reference="lem: CCC ELONGATION"}. Further, we know from Lemma [7](#lem: anti parallel tangent){reference-type="ref" reference="lem: anti parallel tangent"} that the trajectories of lengths $\{l_{RSR},l_{LSL},l_{RSL},l_{LSR}\}\setminus\{l_m\}$ have either $\eta\geq\pi$ or $\zeta\geq\pi$. Thus, they can also be elongated continuously using Lemma [9](#lem: CSC great pi ELONGATION){reference-type="ref" reference="lem: CSC great pi ELONGATION"}. Lastly, the trajectory of length $l_m+2\pi r_{\min}$ can also be continuously elongated till infinity using Lemma [9](#lem: CSC great pi ELONGATION){reference-type="ref" reference="lem: CSC great pi ELONGATION"}. Consequently, there exists a $\mathbf{C}^{r_1}\mathbf{C}^{r_2}\mathbf{C}^{r_3}$ trajectory for all $l_o\in[l_2,\infty)$. Hence proved. $\square$

Theorems [4](#lem: CCC ELONGATION){reference-type="ref" reference="lem: CCC ELONGATION"} - [6](#lem: set OC elongation){reference-type="ref" reference="lem: set OC elongation"} show that the proposed $\mathbf{C}^{r_1}\mathbf{C}^{r_2}\mathbf{C}^{r_3}$ trajectories can form curvature-bounded trajectories of any desired lengths. The corresponding set of reachable lengths is exactly the same as the maximum reachability set mentioned in Theorem [3](#thm: maximal reachable lengths){reference-type="ref" reference="thm: maximal reachable lengths"} for all pairs of oriented points $(A,B)$. Further, the proposed strategies guarantee a maximum of two changeover points in the entire trajectory between $A$ and $B$ for any desired length.

The analysis of the set of reachable lengths till now is done with the values of $r_1$ and $r_3$ fixed. They took the value of $\pm r_{\min}$ depending upon the kind of Dubins Shortest Path between $(A,B)$ and the subsequent elongation strategy. We have established that the maximum reachability set is completely covered with just these values of $r_1$ and $r_3$ for the $\mathbf{C}^{r_1}\mathbf{C}^{r_2}\mathbf{C}^{r_3}$ trajectory. Next, we proceed to discuss the variation of $r_1$ and $r_3$ values and its implication on the lengths of the $\mathbf{C}^{r_1}\mathbf{C}^{r_2}\mathbf{C}^{r_3}$ trajectories.

## Variation of $r_1$ and $r_3$ for Circle-Circle-Circle trajectories

The design of a Circle-Circle-Circle trajectory is accomplished by a suitable variation of $\{r_1,r_3,k\}$. All the reachable lengths are achieved by varying $k$ in $[-\pi/2,3\pi/2)$ and $r_1$ and $r_3$ in $\{-r_{\min},r_{\min}\}$. In this section, we explore the effect of a continuous variation of $r_1$ and $r_3$ in $\mathbb{R}\setminus(-r_{\min},r_{\min})$. Given a desired length $l_o$, we show that this results in the existence of multiple trajectories between the oriented points $A$ and $B$. We begin the analysis with the following definition of a trajectory $\Tilde{\Lambda}$.

::: definition
****Definition** 3**. *Given two oriented points $A$ and $B$, consider that the radii $r_1$ and $r_3$ take some fixed values in $\mathbb{R}$ such that eqn. [\[eq: existence of Hyperbola\]](#eq: existence of Hyperbola){reference-type="eqref" reference="eq: existence of Hyperbola"} holds. Let $$\begin{equation*}
        \Tilde{l}=\underset{k\in[-\pi/2,3\pi/2)}\min l(k)
\end{equation*}$$ be the length of the shortest trajectory in this framework. We denote this trajectory by $\Tilde{\Lambda}$.*
:::

The trajectory $\Tilde{\Lambda}$ can be found numerically by iterating over $k\in[-\pi/2,3\pi/2)$. Note that it can be a $CSC$ trajectory which is a $\mathbf{C}^{r_1}\mathbf{C}^{r_2}\mathbf{C}^{r_3}$ trajectory with $|r_2|$ tending to ininity. We should highlight that for appropriate values of $(A,B,r_1,r_3)$ with $r_1,r_3\in\{\pm r_{\min}\}$, $\Tilde{\Lambda}={\Lambda_m}$. We define the following sets based upon the trajectory $\Tilde{\Lambda}$. $$\begin{align*}
        \mathcal{P}_0=\{(A,B,r_1,r_3)|&\Tilde{\Lambda}\in C_{\eta}^{r_1}C_{\mu}^{r_2}C_{\zeta}^{r_3}\text{ with } \mu\geq\pi|r_2|\}\\
        \mathcal{P}_1=\{(A,B,r_1,r_3)|&\Tilde{\Lambda}\in C_{\eta}^{r_1}C_{\mu}^{r_2}C_{\zeta}^{r_3}\text{ with } \eta\geq\pi|r_1|\}\\
        \mathcal{P}_2=\{(A,B,r_1,r_3)|&\Tilde{\Lambda}\in C_{\eta}^{r_1}C_{\mu}^{r_2}C_{\zeta}^{r_3}\text{ with } \zeta\geq\pi|r_3|\}\\
        \mathcal{P}_3=\{(A,B,r_1,r_3) | &\Tilde{\Lambda}\in C_{\eta}^{r_1}C_{\mu}^{r_2}C_{\zeta}^{r_3}\text{ with }\\ &d(\mathbf{c}^r_A,\mathbf{c}^r_B)\geq|r_1|+|r_3|+2r_{\min}\}\\
        \mathcal{P}_4=\{(A,B,r_1,r_3) |&\Tilde{\Lambda}\in C_{\eta}^{r_1}C_{\mu}^{r_2}C_{\zeta}^{r_3}\text{ with }\\ &d(\mathbf{c}^l_A,\mathbf{c}^l_B)\geq|r_1|+|r_3|+2r_{\min}\}
\end{align*}$$ where $\eta$, $\mu$ and $\zeta$ are arc lengths of the three circles, respectively. The points $\mathbf{c}^r_A$ and $\mathbf{c}^l_A$ are the centres of the circles of radius $|r_1|$ at $A$ corresponding to right and left turns, respectively. The points $\mathbf{c}^r_B$ and $\mathbf{c}^l_B$ are the centres of the circles of radius $|r_3|$ at $B$ corresponding to right and left turns, respectively. We define the set $\mathcal{P}:=\mathcal{P}_1\cup\mathcal{P}_2\cup\mathcal{P}_3\cup\mathcal{P}_4$. The set $\mathcal{P}$ is a generalisation of the set $\mathcal{O}$ for different values of $r_1$ and $r_3$. The following theorem states the set of reachable lengths for these sets.

::: {#thm: variable r1 and r3 .theorem}
****Theorem** 7**. *Given two oriented points $A$ and $B$, consider that the radii $r_1$ and $r_3$ take some fixed values in $\mathbb{R}$ such that eqn. [\[eq: existence of Hyperbola\]](#eq: existence of Hyperbola){reference-type="eqref" reference="eq: existence of Hyperbola"} holds. If $(A,B,r_1,r_3)\in\mathcal{P}_0\cup\mathcal{P}$, then there exists a $\mathbf{C}^{r_1}\mathbf{C}^{r_2}\mathbf{C}^{r_3}$ trajectory for all desired lengths $l_o\in[\Tilde{l},\infty)$.*
:::

The proof for the sets $\mathcal{P}_0$ and $\mathcal{P}$ is similar to that of Theorems [4](#lem: CCC ELONGATION){reference-type="ref" reference="lem: CCC ELONGATION"} and [5](#lem: set O ELONGATION){reference-type="ref" reference="lem: set O ELONGATION"}, respectively. $\square$

This concludes our discussion on the set of reachable lengths for curvature-bounded trajectories of desired lengths. Theorem [7](#thm: variable r1 and r3){reference-type="ref" reference="thm: variable r1 and r3"} provides set of reachable lengths for any given values of $r_1$ and $r_3$ in $\mathbb{R}$ through the construction of sets $\mathcal{P}_0$ and $\mathcal{P}$.

::: remark
****Remark** 2**. *It should be noted that the reachability set in Theorem [7](#thm: variable r1 and r3){reference-type="ref" reference="thm: variable r1 and r3"} is always a subset of the maximum set of reachable lengths. Thus, it illustrates the existence of multiple trajectories for the same desired length. Note that this is in contrast to the results presented in Theorems [4](#lem: CCC ELONGATION){reference-type="ref" reference="lem: CCC ELONGATION"} - [6](#lem: set OC elongation){reference-type="ref" reference="lem: set OC elongation"} which prove the existence of at least one $\mathbf{C}^{r_1}\mathbf{C}^{r_2}\mathbf{C}^{r_3}$ trajectory of a reachable desired length. Further, all of the proposed elongation strategies result in curvature-bounded trajectories with at most two curvature discontinuities.*
:::

# Numerical simulations {#sec: simulation}

In this section, we illustrate the results presented in this paper through the following numerical simulations.

**Example 1:** Consider $A=(-3m,1m,0.785rad)$ and $B=(0m,0m,0rad)$. The Dubins Shortest Path between $A$ and $B$ for $r_{\min}=1m$ is an $RSL$ path of length $l_m=3.484m$. The given $(A,B)\in\mathcal{O}^c$ with $l_1=4.144m$ and $l_2=6.856m$ from eqn. [\[eq: l1 l2 definition\]](#eq: l1 l2 definition){reference-type="eqref" reference="eq: l1 l2 definition"}. Consequently, the set of reachable lengths can be defined. We seek to construct trajectories of lengths $l_o\in\{3.60m,4.05m,7.00m,11.15m,12.45m,14.90m\}$. Table [3](#tab: simulation 1){reference-type="ref" reference="tab: simulation 1"} shows the computed values of $r_2$. Fig. [28](#fig: simulation 1){reference-type="ref" reference="fig: simulation 1"} shows the various feasible trajectories. The Dubins Shortest Path has been highlighted in red.

::: {#tab: simulation 1}
   $l_o(m)$   $r_1(m)$   $r_2(m)$     $k$     $r_3(m)$   Label
  ---------- ---------- ---------- --------- ---------- -------
    3.484      -1.00     $\infty$   $\pi$/2     1.00    
     3.60      -1.00      -1.37      2.634      1.00    
     4.05       1.00      -1.031    -0.379      1.00    
     7.00       1.00      -1.015     0.360      1.00    
    11.15       1.00      -1.57      0.748      1.00    
    12.45      -1.00       1.49     -0.634      1.00    
    14.90      -1.00       1.87     -0.876      1.00    

  :  Computed values of $r_2$ for trajectories between $A$ and $B$ of various lengths
:::

[]{#tab: simulation 1 label="tab: simulation 1"}

:::: {#fig: simulation 1 .figure latex-placement="h"}
![](Rao2024Trajectory_figs/simulation_2.png)

::: caption
Trajectories between $A=(-3m,1m,0.785rad)$ and $B=(0m,0m,0rad)$ of various lengths with changeover points labeled ($\bullet$)
:::
::::

**Example 2:** Consider $A=(-30m,10m,0.714rad)$ and $B=(0m,0m,0rad)$. The Dubins Shortest Path for $r_{\min}=1m$ is an $RSL$ path of length $l_m=31.809m$. The given $(A,B)\in\mathcal{O}_3$. Thus, a $\mathbf{C}^{r_1}\mathbf{C}^{r_2}\mathbf{C}^{r_3}$ trajectory exists for all $l_o\in[l_m,\infty)$. We seek to construct trajectories of length $l=44.5m>l_m$. There exists infinitely many such trajectories between $A$ and $B$. We arbitrarily choose $r_1$ and $r_3$ values and check if $(A,B,r_1,r_3)\in\mathcal{P}_0\cup\mathcal{P}$. If $l_o\geq\Tilde{l}$, then we proceed to compute the values of $r_2$. Table [4](#tab:r1 r2 r3 simulation){reference-type="ref" reference="tab:r1 r2 r3 simulation"} shows the computed values of $\Tilde{l}$ and $r_2$. Fig. [29](#fig:trajectpry ccc){reference-type="ref" reference="fig:trajectpry ccc"} shows the simulated trajectories in the $\mathbb{R}^2$ plane. Note that for the trajectory in green, $r_1$ and $r_3$ values are appropriately chosen such that we don't require three circular arcs resulting in a $LL$ trajectory.

::: {#tab:r1 r2 r3 simulation}
   $r_1(m)$   $r_3(m)$   $\Tilde{l}(m)$   $r_2(m)$    $k$     Label
  ---------- ---------- ---------------- ---------- -------- -------
    -2.500     1.500         32.099        20.683    0.805   
    -5.500     -3.580        33.467        9.601     0.167   
    -1.000     -1.010        32.389        14.798    3.328   
    13.790     10.010        35.998        -9.145    -0.242  
    1.940      12.010        35.673        -27.42    2.029   
    2.040      59.314         N/A           N/A       N/A    

  :  Computed values of $r_2$ and $k$ for trajectories between $A$ and $B$ of length $l_o=44.5m$
:::

:::: {#fig:trajectpry ccc .figure latex-placement="ht"}
![](Rao2024Trajectory_figs/trajectory_1.png)

::: caption
Trajectories between $A$ and $B$ of length $l_o=44.5m$ with changeover points labeled ($\bullet$)
:::
::::

# Conclusion {#sec: conclusion}

In this paper, our objective is to construct curvature-bounded trajectories of any desired length between any two given oriented points. To do so, we propose to design the trajectory utilising three circular arcs of varying radii for the same, referred to as a Circle-Circle-Circle ($\mathbf{C}^{r_1}\mathbf{C}^{r_2}\mathbf{C}^{r_3}$) trajectory. The feasible trajectory is constructed by first fixing the terminal circles. Then, we show that the locus of the centre of $\mathcal{C}_2$ is a hyperbola $\mathcal{H}$ parameterised by the argument $k$. The overall trajectory is then defined using the three parameters: the radii of the terminal circles $\{r_1,r_3\}$ and an argument $k$. In the absence of any constraints on the length of the trajectory, we derive the necessary conditions for the existence of $\mathbf{C}^{r_1}\mathbf{C}^{r_2}\mathbf{C}^{r_3}$ trajectories. Now, such trajectories can be of eight types: $\{LLL,LLR,LRR,LRL,RRL,RLL,RLR,RRR\}$. We also present a complete classification of the trajectories into these forms based upon the values of $\{r_1,r_3,k\}$.

In the presence of curvature boundedness, we propose to elongate the circular arcs $C^{r_i}$, $\in\{1,2,3\}$ to achieve trajectories of desired lengths. In this regard, we show that the argument $k$ is critical as its variation, divided over the two branches of the hyperbola, results in an infinite (not necessarily continuous) elongation of the trajectory. However, this variation leads to jump discontinuities in the length of the trajectory for some configurations of $(A,B)$. To resolve this issue, we propose elongation strategies which guarantee the existence of curvature-bounded trajectories of any desired length for any configuration $(A,B)$. Further, we show that the set of reachable lengths is exactly equal to that proposed in [@chen_elongation] guaranteeing maximum coverage of the reachability set. In addition to this, the proposed elongation strategies also lead to the existence of multiple trajectories of desired lengths simply through the variation of $r_1$ and $r_3$.

The paper concludes with numerical solutions illustrating and validating various results discussed in the paper. Future works in this direction may extend this approach to trajectory planning in the presence of obstacles. Further, additional constraints like minimum control effort maybe imposed as the trajectory is under-constrained for the problem addressed in this paper.

[^1]: This work was not supported by any organisation.
