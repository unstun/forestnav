---
citation_key: GonzlezCalvin2025Efficient
arxiv_id: 2512.13183
arxiv_url: https://arxiv.org/abs/2512.13183
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-23T18:56:25Z
origin: ai+web
reviewed: false
---

# Introduction {#sec: intro}

In robotics and control, motion execution is often decomposed into a hierarchy of interrelated problems. Path planning determines a feasible route through the robot's configuration space---typically as a sparse sequence of waypoints---using methods ranging from graph-search algorithms like A\* to sampling-based approaches such as RRT [@lavalle2006planning]. Path generation then transforms this abstract plan into a smooth, continuous geometric path or time-parameterized trajectory, often using Spline-based methods, including cubic B-splines [@lau2009kinodynamic; @berglund2010planning] and Bézier curves [@yang2010analytical]. These methods ensure $C^2$ continuity and bounded curvature but may produce high curvature and cumbersome paths when the spacing of waypoints is irregular [@meek1992]. Gaussian process regression [@rasmussen2006] and kernel smoothing [@hastie2009] generate $C^\infty$-smooth approximations, trading exact waypoint passage for improved smoothness at the cost of $O(n^3)$ computational complexity and potential numerical instability. Optimization-based approaches [@mellinger2011; @ratliff2009chomp] incorporate explicit curvature bounds through convex formulations, enabling real-time computation but requiring careful parameter tuning [@heiden2018grips].

However, critically, path generation does not operate in isolation: its output must meet the requirements imposed by the downstream control layer, which typically takes one of two forms. In *path following*, the generated path must be geometrically smooth and continuously differentiable, so that a well-defined tangent and curvature exist at every point for spatial error computation [@weijiaarticlegvf]. In *trajectory tracking*, the demands are more stringent: the time parameterization must additionally be consistent with the robot's dynamic capabilities, as a reference trajectory that demands accelerations or velocities beyond the system's limits cannot be reliably tracked regardless of the controller's design [@siciliano2009robotics]. In both cases, path generation must internalize the robot's kinematic and dynamic constraints, effectively acting as the bridge that makes a planned route physically executable and controllable.

In this paper, we propose an inexpensive path generation method based on *mollifying* non-differentiable paths, e.g., piecewise functions, using mollifier functions. Mollifiers are smooth functions that, via convolution, approximate non-smooth functions arbitrarily close. They have been extensively used in partial differential equations [@Evans2022-PDE] and in studying the non-vanishing of generalized Riemann zeta functions [@cech2025optimalitymollifiers]. From an engineering perspective, mollifiers are used in signal and image processing to estimate the original probability distribution of variables under measurement error [@hohage2024mollifier]. However, to the best of the authors' knowledge, mollifiers have not been applied to path generation problems, despite their natural fit for robotics applications.

Mollification offers a principled approach to path generation. For example, given a finite collection of ordered waypoints, it produces a smooth curve that approximates the piecewise-linear route to an arbitrary degree of Euclidean closeness. For this specific generated path, our method is well-suited for unicycle-like robots that travel at constant speed with heading-rate constraints; i.e., we can guarantee a maximum curvature for the generated path at the mild cost of slightly deviating from these connecting segments---an unavoidable trade-off, since the union of segments produces a non-differentiable path. Our approach is particularly appealing because it is computationally inexpensive as it can be run on small microcontrollers, and the resulting path, in its parametric representation, can be followed using path-following techniques based on modern guiding vector fields [@weijiaarticlegvf]. We also show how our method can generate 3D paths and guarantee several properties for generic sets of input points, including convexity preservation, enclosure of the generated path, and bounded maximum length when the input is also closed.

The article is organized as follows, Section [3](#sec: problem){reference-type="ref" reference="sec: problem"} introduces the mollifier functions and the requirements for the path generation problem. Section [4](#sec: res){reference-type="ref" reference="sec: res"} explores which geometrical and analytical aspects of the original function are affected by mollification. Convexity, concavity and quasiconvexity are treated, as well as the length of the path and the curvature. Section [6](#sec: exp){reference-type="ref" reference="sec: exp"} validates the theoretical findings numerically and experimentally. We end the article with some conclusions in Section [7](#sec: con){reference-type="ref" reference="sec: con"}.

# Notation {#sec: not}

In this paper we use Lebesgue integration rather than Riemann integration to overcome some limitations with sets of measure zero and interchanging integral and limits. Therefore, we denote the Lebesgue measure in one dimension as $\lambda$, i.e., $\lambda := \lambda_1$, and as $\lambda_n$ the $n$'th dimensional Lebesgue measure, and we consider that it is equipped with the Borel sigma algebra. Consequently, all integrals in this paper must be thought as the Lebesgue integral with respect to the Lebesgue measure, even if the notation $\lambda$ is sometimes omitted in the integral. For $p \in [1,\infty)$, we say that a measurable function $f$ is locally $p$-integrable, denoted $f \in L^p_{\mathrm{loc}}(X)$, if it is $p$-integrable in each compact subset of $X$. We denote by $\mathop{\mathrm{id}}: X \to X$ the identity function defined as $\mathop{\mathrm{id}}(x) = x$. Then, the indicator function of a set $A$ is defined as $$\begin{equation*}
    \mathop{\mathrm{ind}}_{A}(x) = \begin{cases}
        1 & x \in A, \\
        0 & x \notin A
    \end{cases}.
\end{equation*}$$ For any two sets $X,Y$ we denote $C(X,Y)$ as the set of continuous functions from $X$ to $Y$ and for $n \in \mathbb N\cup \{\infty\}$ we denote as $C^n(X,Y)$ the set of $n$-times continuously differentiable functions from $X$ to $Y$. For a set $A$ we denote its closure as $\overline{A}$ and the support of a real-valued function is defined as $\mathop{\mathrm{supp}}f := \overline{\{x \in \mathop{\mathrm{dom}}f \mid
f(x) \neq 0\}}$, where $\mathop{\mathrm{dom}}f$ is the domain of $f$. Finally, a (parametric) path in $\mathbb R^n$ is a measurable function $f : X \subset \mathbb R\to \mathbb R^n$. Writing $f = (f_1,\dots,f_n)$, we call $f_i$ the $i$'th component of the path for $i \in \{1,\dots,n\}$.

# Path generation by mollification {#sec: problem}

## Path generation requirements

This paper seeks an alternative approach to interpolation and optimization methods for the generation of paths from high-level inputs---such as waypoint sequences---that is computationally efficient, conceptually simple, and has a transparent physical interpretation. Furthermore, the generated paths must be feasible for mobile robots such as unicycles, avoiding unnecessarily complex trajectories. Technically, we consider the transformation of an arbitrary parametric path $f : \mathbb R\to \mathbb R^n$ into another parametric path that satisfies the following requirements casted as a formal problem.

::: {#prob:RegularizationProblem .problem}
**Problem 1** (Path generation problem). *Let $f : \mathbb R\to \mathbb R^n$ be a parametric path and $\{\varepsilon_i\}_{i=1}^n$ be a collection of positive real numbers. Find a new path $T_{\varepsilon}(f) : \mathbb R\to \mathbb R^n$ where $T_{\varepsilon}(f) =: \{T_{\varepsilon_i}(f_i)\}_{i=1}^{n}$ and $T_{\varepsilon_i}$ is a functional that acts on each component of $f$ such that:*

1.  *Each component of the parametric path can be made arbitrary close to the original path, that is, $T_{\varepsilon_i}(f_i) \to f_i$ as $\varepsilon_i \to 0$ in some sense of convergence.*

2.  *It provides enough smoothness, that is, for $p \in \mathbb N$ with $p \geq 2$, $T_{\varepsilon_i}(f_i) \in C^p(\mathbb R,\mathbb R)$ for $i \in \{1,\dots,n\}$.*

3.  *$T_{\varepsilon_i}(f_i)$ is computationally simple. $\square$*
:::

The first requirement ensures that the generated path approximates $f$ arbitrarily well through a single independent tuning parameter per dimension, allowing a sequence of functions to be made arbitrarily close to the---potentially non-differentiable everywhere---original path. The second requirement guarantees feasibility for mobile robots like unicycles with speed constraints; we demonstrate how to bound the curvature when the input path consists of concatenated line segments when $n=2$. Finally, the third requirement enables real-time path generation with low-cost hardware.

## Mollifiers for the path generation {#subsec: Molli}

The solution to Problem [1](#prob:RegularizationProblem){reference-type="ref" reference="prob:RegularizationProblem"} can be obtained by taking a weighted average of the points along the parametric path $f$ through convolution with a certain type of function known as a *mollifier* [@Evans2022-PDE]. Let us recall the convolution operation.

::: {#def:ConvolutionDefinition .definition}
**Definition 1** (Convolution). *Let $f,g \in L^1(\mathbb R^n)$. The convolution $f*g : \mathbb R^n \to \mathbb R$ is defined as $$\begin{equation}
        (f*g)(x) := \int_{\mathbb R^n}f(y)g(x-y) \, \mathrm{d}\lambda_n(y). \nonumber
\end{equation}$$ $\square$*
:::

We recall that the convolution is associative, bilinear and commutative. Let us now introduce the mollifier function.

::: {#def:MollifiersDefinition .definition}
**Definition 2** (Mollifier). *Let $\varphi \in C^{\infty}(\mathbb R^n,\mathbb R)$ and for $\varepsilon>0$ define $\varphi_{\varepsilon} := \frac{1}{\varepsilon^n}\varphi \circ
    \frac{\mathop{\mathrm{id}}}{\varepsilon}$. We call $\varphi$ a mollifier if it satisfies:*

1.  *$\mathop{\mathrm{supp}}\varphi$ is compact.*

2.  *$\int_{\mathbb R^n}\varphi \, \mathrm{d}\lambda_n = 1$.*

3.  *For any bounded $f \in C(\mathbb R^n,\mathbb R)$, $\lim_{\varepsilon\to 0}
            \int_{\mathbb R^n}f(x)\varphi_{\varepsilon}(x) \, \mathrm{d}\lambda_n(x) = f(0)$. $\square$*
:::

Let us present one of the most popular mollifiers since it will be used extensively in this paper.

::: {#example:OurMollifier .example}
**Example 1**. *Let $\varphi : \mathbb R\to [0,\infty)$ be the function $$\begin{equation}
\label{eq:OurMollifier}
        \varphi(x) = \begin{cases}
            c_1\exp\left(\frac{-1}{1-x^2}\right), & |x| < 1, \\
            0, &|x| \geq 1
        \end{cases},
\end{equation}$$ where $c_1 > 0$ is a normalization constant that ensures $\int_{\mathbb R}\varphi \, \mathrm{d}\lambda = 1$. Clearly $\mathop{\mathrm{supp}}\varphi = \overline{(-1,1)} = [-1,1]$ and $\mathop{\mathrm{supp}}\varphi_{\varepsilon} = [-\varepsilon,\varepsilon]$. Moreover, with a change of variables it can be seen that $\int_{\mathbb R}\varphi_{\varepsilon} \, \mathrm{d}\lambda = 1$, and it can also be shown using the Lebesgue Dominated Convergence Theorem that as $\varepsilon\to 0$ the third property in Definition [2](#def:MollifiersDefinition){reference-type="ref" reference="def:MollifiersDefinition"} holds. Figure [1](#fig:OurMollifier){reference-type="ref" reference="fig:OurMollifier"} represents the function $\varphi_{\varepsilon}$ for different values of $\varepsilon> 0$. $\square$*
:::

For several results in this paper, we will require the following assumption.

::: {#ass: mol .assumption}
**Assumption 1**. *The mollifier $\varphi$ is nonnegative and its support is the symmetric set around the origin $[-1,1]$.*
:::

Note that this assumption is made for the sake of convenience. If the set is not symmetric around the origin, many of the presented results will be *displaced* but still apply. Also note that if the support of $\varphi$ is $[-a,a]$, with $0 < a \neq 1$, we can always rescale it to be $[-1,1]$ via the parameter $\varepsilon$ as in Definition [2](#def:MollifiersDefinition){reference-type="ref" reference="def:MollifiersDefinition"}.

![Representation of $\varphi_{\varepsilon}$ for different values of $\varepsilon> 0$ where the mollifier $\varphi$ is defined in Example [1](#example:OurMollifier){reference-type="ref" reference="example:OurMollifier"}.](Images/MollifierPlots.eps){#fig:OurMollifier width="\\linewidth"}

Now, let us consider a set of mollifiers $\{\varphi_{\varepsilon_i} : \mathbb R\to \mathbb R\}_{i=1}^{n}$, and define the generated path $F = (F_1,\dots,F_n)$ with $F_i := f_i * \varphi_{\varepsilon_i}$ for all $i \in \{1,\dots,n\}$, and let us denote by $\varphi_{\varepsilon}^{(n)}$ the $n$-th derivative of the function $\varphi_{\varepsilon}$.

::: {#thm:PropertiesOfMollifying .theorem}
**Theorem 1** ([@Evans2022-PDE Appendix C, Theorem 7]). *Let $\varepsilon> 0$, $f \in L_{loc}^p(\mathbb R)$ with $p \in [1,\infty]$, and $\varphi$ be a mollifier; then the following three statements hold:*

1.  *$F_{\varepsilon} \in C^{\infty}(\mathbb R,\mathbb R)$ and for any $n \in \mathbb N$ we have that $F_{\varepsilon}^{(n)} = (\varphi_{\varepsilon} * f)^{(n)} = (\varphi_{\varepsilon})^{(n)} * f$.*

2.  *$\varphi_{\varepsilon} * f \to f$ pointwise almost everywhere as $\varepsilon\to 0$.*

3.  *If $p < \infty$ then $\lim_{\varepsilon\to0}||\varphi_{\varepsilon} * f - f||_{p} = 0$. $\square$*
:::

While it may seem otherwise, Theorem [1](#thm:PropertiesOfMollifying){reference-type="ref" reference="thm:PropertiesOfMollifying"} does not solve Problem [1](#prob:RegularizationProblem){reference-type="ref" reference="prob:RegularizationProblem"} *entirely*. Indeed, the second requirement is satisfied straightforwardly. Regarding the computational efficiency from the third requirement, the computation of $F$ is also straightforward. Indeed, because of the compact and symmetric support of the mollifier due to Assumption [1](#ass: mol){reference-type="ref" reference="ass: mol"}, we have that $F_{\varepsilon}(x) = \int_{[-\varepsilon,\varepsilon]}f(x-t)\varphi_{\varepsilon}(t) \, \mathrm{d}\lambda(t)$ is an inexpensive numerical operation, and note the compact integration interval. Furthermore, note that $F_i^{(n)} := (f_i * \varphi_{\varepsilon_i})^{(n)} = f_i * \varphi_{\varepsilon_i}^{(n)}$, and also note that computing $F_i^{(n)}(x)$ does not require the existence of $f_i^{(n)}(x)$.

However, regarding the first requirement of Problem [1](#prob:RegularizationProblem){reference-type="ref" reference="prob:RegularizationProblem"}, Theorem [1](#thm:PropertiesOfMollifying){reference-type="ref" reference="thm:PropertiesOfMollifying"} only gives us pointwise convergence and $L^p$ convergence. For path following or trajectory tracking algorithms we want to have a stronger notion of convergence for Problem [1](#prob:RegularizationProblem){reference-type="ref" reference="prob:RegularizationProblem"}, i.e., if $f \in L^p_{loc}(\mathbb R)$ then for any mollifier $\varphi$, we want $\varphi_{\varepsilon} * f \to f$ as $\varepsilon\to 0$ uniformly. This is true if we require $f$ to be uniformly continuous; nonetheless, if $f$ is just continuous we have uniform convergence on compact subsets of $\mathbb R$. Let us finish by showing why mollifying a uniformly continuous $f$ solves the Path Generation Problem [1](#prob:RegularizationProblem){reference-type="ref" reference="prob:RegularizationProblem"} with a stronger notion of convergence.

::: {#thm:UniformConvergence .theorem}
**Theorem 2** (Uniform convergence). *Let $f \in L^p_{loc}(\mathbb R)$ and let $\varphi : \mathbb R\to \mathbb R$ be a non negative mollifier. The following statements hold:*

1.  *If $f$ is uniformly continuous then $F_{\varepsilon} \to f$ as $\varepsilon
            \to 0$ uniformly.*

2.  *If $f$ is Lipschitz continuous then $F_{\varepsilon} \to f$ as $\varepsilon\to 0$ uniformly and $F_{\varepsilon}$ is Lipschitz continuous for any $\varepsilon> 0$.*

3.  *If $f$ is continuous then $F_{\varepsilon} \to f$ as $\varepsilon\to 0$ uniformly on compact subsets of $\mathbb R$.*
:::

::: proof
*Proof.* For the first statement, suppose $f$ is uniformly continuous. Fix $x \in \mathbb R$ and $\eta > 0$. We know there exists a $\delta = \delta(\eta) > 0$ such that $|f(a)-f(b)| < \eta$ whenever $|a-b| < \delta$. Choose $\varepsilon\in (0,\delta)$. Recall that $\int_{\mathbb R} \varphi = 1$, thus $f(x) = \int_{\mathbb R}f(x)\varphi(t) \, \mathrm{d}\lambda(t)$. Therefore $$\begin{align*}
|F_{\varepsilon}(x) -f(x)| &= \left|\int_{(-\varepsilon,\varepsilon)}(f(x-t)-f(x))\varphi_{\varepsilon}(t) \, \mathrm{d}\lambda(t)\right| \\
&\leq \int_{(-\varepsilon,\varepsilon)}|f(x-t)-f(x)|\varphi_{\varepsilon}(t) \, \mathrm{d}\lambda(t) < \eta,
\end{align*}$$ because $|x-t-x| = |t| \leq \varepsilon< \delta$. Since $x$ was arbitrary the statement follows.

For the second statement, since every Lipschitz continuous functions is uniformly continuous, the uniform convergence claim follows from the previous paragraph. Moreover, take $x, y \in \mathbb R$, $\varepsilon\in (0,\infty)$ and suppose that $f$ is Lipschitz with Lipschitz constant $K > 0$. $$\begin{align*}
|F_{\varepsilon}(x) - F_{\varepsilon}(y)| &\leq \int_{\mathbb R}|f(x-t)-f(y-t)|\varphi_{\varepsilon}(t)\, \mathrm{d}\lambda(t) \\
&\leq K|x-y|\int_{\mathbb R}\varphi_{\varepsilon}(t) \, \mathrm{d}\lambda(t) = K|x-y|,
\end{align*}$$ which proves that $F_{\varepsilon}$ is Lipschitz.

Finally, for the third statement, suppose now $f$ is continuous and take any compact set $K \subset \mathbb R$. Then $f$ is uniformly continuous on $K$. Thus, the same arguments as above can be followed noting that in this case $\delta$ depends on the compact set $K$. ◻
:::

# Key properties of the generated path {#sec: res}

While Theorems [1](#thm:PropertiesOfMollifying){reference-type="ref" reference="thm:PropertiesOfMollifying"} and [2](#thm:UniformConvergence){reference-type="ref" reference="thm:UniformConvergence"} solve Problem [1](#prob:RegularizationProblem){reference-type="ref" reference="prob:RegularizationProblem"}, they do not provide further details about the properties of the resulting path. In this section, we characterize key properties of the generated path based on the input path. Specifically, we address questions such as: under what conditions does the output path preserve (local/quasi) convexity of the input? Does the output maintain monotonicity or other qualitative properties of the input, such as for step functions? How is the output path positioned relative to the input? How is the output path enclosed, and what is its length when the input is a closed path? We defer the analysis of the output path's curvature to Section [5](#sec: curvature){reference-type="ref" reference="sec: curvature"}, where we provide a detailed curvature analysis for the case when the input is a sequence of 2D or 3D waypoints. This curvature analysis serves as a systematic methodology that can be applied to other types of input paths.

For conciseness, we restrict our attention to mollifiers defined on the real line, since our analysis is carried out component-wise along trajectories. Nevertheless, most results can be generalized to functions from $\mathbb R^n$ to $\mathbb R$, which may be useful when the desired path in $\mathbb R^n$ is encoded as the intersection of $n-1$ hypersurfaces parametrized by functions from $\mathbb R^n$ to $\mathbb R$. In such higher-dimensional cases, one would consider the standard Euclidean norm in $\mathbb R^n$, the topology whose basis consists of open balls $B(x,\varepsilon) = \{y \in \mathbb R^n \mid ||y-x|| <\varepsilon\}$, and a mollifier whose support is the closed ball $\overline{B}(0,1) = \{x \in \mathbb R^n \mid ||x|| \leq 1\}$. Indeed, this is precisely the case for the extension to $\mathbb R^n$ of the mollifier presented in Example [1](#example:OurMollifier){reference-type="ref" reference="example:OurMollifier"}.

## Convexity properties

Convexity and local convexity are properties of great interest in the study of trajectory shapes. For example, if a vehicle attempts to follow a continuous but non-differentiable trajectory that resembles an inverted tent, such as the function $x \in \mathbb R\mapsto |x|$, will the mollified trajectory preserve this inverted tent shape? What if the property holds only locally? Intuitively, since mollification is a weighted average of the original function, the answer to the first question is affirmative. However, the answer to the second question depends on the parameter value $\varepsilon$. If the parameter is sufficiently large, the "average" of the function over the locally convex region may become negligible. We now present several propositions and counterexamples addressing these questions.

::: {#prop:ConvexityIsPreserved .proposition}
**Proposition 1** (Convexity and mollification). *Let $f \in L^1_{loc}(\mathbb R)$ be convex and $\varphi$ a nonnegative mollifier as in Definition [2](#def:MollifiersDefinition){reference-type="ref" reference="def:MollifiersDefinition"}; then $F_{\varepsilon} :=
    \varphi_{\varepsilon} * f$ is convex for any $\varepsilon> 0$.*
:::

::: proof
*Proof.* Let $x,y \in \mathbb R$ and $\gamma \in [0,1]$. Since $\varphi_{\varepsilon} \geq 0$ we have that $$\begin{align*}
        F_{\varepsilon}(\gamma x + &(1-\gamma)y) = \int_{\mathbb R}f(\gamma x +
        (1-\gamma)y - t)\varphi_{\varepsilon}(t) \, \mathrm{d}t \\
        &= \int_{\mathbb R}f(\gamma(x-t) + (1-\gamma)(y-t))\varphi_{\varepsilon}(t) \, \mathrm{d}t \\
        &\leq \int_{\mathbb R}\left[\gamma f(x-t) +
        (1-\gamma)f(y-t)\right]\varphi_{\varepsilon}(t) \, \mathrm{d}t \\
        &=\gamma F_{\varepsilon}(x) + (1-\gamma)F_{\varepsilon}(y).
\end{align*}$$ ◻
:::

This property allows us to predict the shape of the mollified trajectory in advance. For example, if the trajectory to be followed resembles an inverted tent, the mollified trajectory $F_{\varepsilon}$ will also resemble an inverted tent for any $\varepsilon>0$. The question is whether local convexity is always preserved. This is false; local convexity is preserved only for sufficiently small $\varepsilon>0$, where the bound on $\varepsilon$ depends on the neighborhood in which the function is convex. We now present a proposition and a counterexample.

::: {#prop:LocalConvexity .proposition}
**Proposition 2** (Local convexity and mollification). *Let $f \in L^{1}_{loc}(\mathbb R)$ be a function that is convex in some set $(a,b)
    \subseteq \mathbb R$ with $-\infty \leq a < b \leq \infty$. Let $\varphi$ satisfy Assumption [1](#ass: mol){reference-type="ref" reference="ass: mol"}. Then, for each $x,y \in (a,b)$ with $x < y$ there exists a $\delta = \delta(x,y)> 0$ such that for all $\varepsilon
    \in(0,\delta)$ the function $F_{\varepsilon} := f * \varphi_{\varepsilon}$ is convex in the set $(x,y)$.*
:::

::: proof
*Proof.* Let $x,y \in (a,b)$. Since $(a,b)$ is open there exists a real number $\delta > 0$ such that $(x-\delta,y+\delta) \subset (a,b)$. The sets $V = (x-\delta,y+\delta)\subset (a,b)$ and $(x,y)\subset(a,b)$ are clearly open and convex. Choose $\xi,\zeta \in (x,y)$ and $\gamma \in
    [0,1]$. Then we have that $\gamma \xi + (1-\gamma)\zeta \in (x,y)$. Let $\varepsilon\in (0,\delta)$, and we know that $$\begin{align*}
        F_{\varepsilon}(\gamma &\xi + (1-\gamma)\zeta) = \int_{\mathbb R}f(\gamma \xi +
        (1-\gamma)\zeta -t)\varphi_{\varepsilon}(t) \, \mathrm{d}\lambda(t).
\end{align*}$$ Note that by the selection of $\varepsilon$ and $\delta$ we have that $t \in
    (-\varepsilon,\varepsilon) \subset (-\delta, \delta)$. Thus, for any $t \in
    (-\varepsilon,\varepsilon)$, $\xi-t \in
    V$ and $\zeta-t \in V$. Since $V$ is convex we have that $\gamma (\xi-t) + (1-\gamma)(\zeta-t) \in V$ for all $t \in (-\varepsilon,\varepsilon)$ and $\gamma \in [0,1]$. Given that $f$ is convex in $(a,b)$ it is also convex in $V\subset (a,b)$, and noting $\varphi_{\varepsilon} \geq 0$ we can follow the steps of the proof of proposition [1](#prop:ConvexityIsPreserved){reference-type="ref" reference="prop:ConvexityIsPreserved"} to reach $$\begin{align*}
        F_{\varepsilon}(\gamma \xi + (1-\gamma)\zeta)
        % &\leq \gamma
        % \int_{(-\ep,\ep)}f(\xi-t)\varphi_{\ep}(t)\mathrm{d}\lambda(t) +
        % (1-\gamma)\int_{(-\ep,\ep)}f(\zeta-t)\varphi_{\ep}(t)\mathrm{d}\lambda(t)
        % \\
        &\leq\gamma F_{\varepsilon}(\xi) + (1-\gamma)F_{\varepsilon}(\zeta).
\end{align*}$$ Because $\xi,\zeta \in V$ and $\gamma \in [0,1]$ were arbitrary the proposition follows. ◻
:::

::: {#example: LocalConvexityNotPreserved .example}
**Example 2**. *It is natural to ask whether Proposition [2](#prop:LocalConvexity){reference-type="ref" reference="prop:LocalConvexity"} holds for any $\varepsilon> 0$. That is, if $f$ is convex on an open set, is $F_{\varepsilon}$ also convex on that open set independently of $\varepsilon$ and the choice of non-negative mollifier? This is generally false, as demonstrated by the following counterexample. Consider the continuous function $$\begin{equation}
f(x) = \begin{cases}
        0, & x < 0 \\
        x, & 0 \leq x \leq \frac{1}{2} \\
        1-x, & x > \frac{1}{2}
    \end{cases},
    \label{ex: 2}
\end{equation}$$ and the mollifier of Example [1](#example:OurMollifier){reference-type="ref" reference="example:OurMollifier"}. The function [\[ex: 2\]](#ex: 2){reference-type="eqref" reference="ex: 2"} is convex on the open set $(-0.5, 0.5)$. However, for $\varepsilon= 3.2$, the mollified function is not convex and even lies below $f$ at every point in that open set, rather than above, as shown in Figure [2](#fig:CounterExampleLocalConvexity){reference-type="ref" reference="fig:CounterExampleLocalConvexity"}.*

:::: {#fig:CounterExampleLocalConvexity .figure latex-placement="!htb"}
![](GonzlezCalvin2025Efficient_figs/CounterExampleLocalConvexityBelow.png){width="\\linewidth"}

::: caption
*If $f$ is convex in an open neighbourhood there can exist a mollifier $\varphi$ as in example [1](#example:OurMollifier){reference-type="ref" reference="example:OurMollifier"} and an $\varepsilon> 0$ such that $F_{\varepsilon} := f
            * \varphi$ is below $f$ in that neighbourhood. Blue line represents $f$, while the red one shows $F_{3.2}$ and the black one $F_{0.45}$.*
:::
::::

*Nevertheless, for $\varepsilon= 0.45$, we have that $F_{\varepsilon}$ is convex on a neighborhood contained in $(-0.5,0.5)$. Thus, we can set $\delta = 0.45$ in Proposition [2](#prop:LocalConvexity){reference-type="ref" reference="prop:LocalConvexity"}, and for any $\varepsilon< \delta$, $F_{\varepsilon}$ is convex in $(-0.5,0.5)$.*
:::

::: remark
**Remark 1**. *Note that Propositions [1](#prop:ConvexityIsPreserved){reference-type="ref" reference="prop:ConvexityIsPreserved"} and [2](#prop:LocalConvexity){reference-type="ref" reference="prop:LocalConvexity"} also hold when $f$ is concave instead of convex, with concavity replacing convexity throughout.*
:::

Before the following result, we need to prove that affine maps are invariant under mollification.

::: {#prop:MollifyIdentityIsIdentity .proposition}
**Proposition 3** (Affine functions and mollification). *Let $\varphi_{\varepsilon}$ with $\varepsilon> 0$ be a mollifier with symmetric support around the origin, and let $a,b \in \mathbb R$; then $\varphi_{\varepsilon} * (a\mathop{\mathrm{id}}+b) =
    a\mathop{\mathrm{id}}+ b$.*
:::

::: proof
*Proof.* Let $x \in \mathbb R$ and $\varepsilon> 0$. Then $$\begin{align*}
        (\varphi_{\varepsilon} * (a\mathop{\mathrm{id}}+b))(x)  &=
        \int_{\mathbb R}(a(x-y)+b)\varphi_{\varepsilon}(y) \mathrm{d} \lambda(y)  \\
        &= ax\int_{\mathbb R}\varphi_{\varepsilon}(y) \, \mathrm{d}\lambda(y) -
        a\int_{\mathbb R}y\varphi_{\varepsilon}(y) \, \mathrm{d}\lambda(y) \\
        & +
        b\int_{\mathbb R}\varphi_{\varepsilon}(y)\, \mathrm{d}\lambda(y) \\
        &=ax + b - a\int_{(-\varepsilon,\varepsilon)}y\varphi_{\varepsilon}(y)\, \mathrm{d}\lambda(y).
\end{align*}$$ The result follows noting that $y\in\mathbb R\mapsto y \varphi_{\varepsilon}(y)$ is an odd function that is integrated over a symmetric interval. ◻
:::

We also need the Jensen's inequality.

::: {#thm:Jensen .theorem}
**Theorem 3** (Jensen's inequality). *[@durrett2019probability Theorem 1.6.2] Let $\varphi$ be a non-negative measurable function such that $\int_{\mathbb R}\varphi \mathrm{d}\lambda = 1$, $g$ be any measurable function and $f$ be a convex function such that $\mathop{\mathrm{dom}}f \supset \mathop{\mathrm{img}}g$; then $$\begin{equation*}
        f\left(\int_{\mathbb R}g(x)\varphi(x)\mathrm{d}\lambda(x)\right) \leq \int_{\mathbb R} (f \circ
        g)(x)\varphi(x)\mathrm{d}\lambda(x).
\end{equation*}$$ $\square$*
:::

![Mollification of the function $f = |\mathop{\mathrm{id}}|$ with the mollifier $\varphi_{\varepsilon}$ as in Example [1](#example:OurMollifier){reference-type="ref" reference="example:OurMollifier"} for different values of $\varepsilon$. Note that the function $f$ is convex, implying $F_{\varepsilon}$ is convex as demonstrated in proposition [1](#prop:ConvexityIsPreserved){reference-type="ref" reference="prop:ConvexityIsPreserved"} and it is above the graph as shown in Proposition [4](#prop:ConvexityThenMolliAbove){reference-type="ref" reference="prop:ConvexityThenMolliAbove"}. ](Images/MolliAbsFunction.eps){#fig:MollifOfAbs width="\\linewidth"}

Now, we are ready to show that if $f$ is convex and $\varphi_{\varepsilon}$ is a non-negative even mollifier, then $\varphi_{\varepsilon} * f \geq f$ pointwise. For example, combined with Proposition [3](#prop:MollifyIdentityIsIdentity){reference-type="ref" reference="prop:MollifyIdentityIsIdentity"}, the following result implies that if our trajectory resembles an inverted tent, then the mollified function will also resemble a smoothed inverted tent but with the mollified function lying *above* the original path; see Figure [3](#fig:MollifOfAbs){reference-type="ref" reference="fig:MollifOfAbs"} for the illustration.

::: {#prop:ConvexityThenMolliAbove .proposition}
**Proposition 4** (If $f$ is convex then $F_{\varepsilon}$ is above $f$). *Let $\varphi_{\varepsilon}$ with $\varepsilon> 0$ satisfying Assumption [1](#ass: mol){reference-type="ref" reference="ass: mol"}, $f$ be a convex function and define $F_{\varepsilon} := \varphi_{\varepsilon} * f$. Then $F_{\varepsilon} \geq f$.*
:::

::: proof
*Proof.* Note that $\varphi_{\varepsilon}$ satisfies the conditions in Jensen's inequality and that $f$ is convex. Let $x \in \mathbb R$, and note that the function $y \in \mathbb R\mapsto x-y$ is continuous, and therefore measurable. Applying Jensen's inequality $$\begin{align*}
        F_{\varepsilon}(x) = (\varphi_{\varepsilon} * f)(x) &=
        \int_{\mathbb R}f(x-y)\varphi_{\varepsilon}(y)\mathrm{d}\lambda(y) \\
        &\geq f\left(\int_{\mathbb R}(x-y)\varphi_{\varepsilon}(y)\mathrm{d}\lambda(y)\right) \\
        &= f( (\varphi_{\varepsilon} * \mathop{\mathrm{id}})(x)).
\end{align*}$$ The result now follows from Proposition [3](#prop:MollifyIdentityIsIdentity){reference-type="ref" reference="prop:MollifyIdentityIsIdentity"} since $x$ is arbitrary. ◻
:::

::: remark
**Remark 2**. *Note that a similar result also holds if $f$ is concave, where clearly $F_{\varepsilon}$ would be below $f$ in that case.*
:::

The following result resembles Proposition [2](#prop:LocalConvexity){reference-type="ref" reference="prop:LocalConvexity"}.

::: {#prop:MolliAboveFConvexityLocally .proposition}
**Proposition 5** (Local convexity and $F_{\varepsilon}\geq f$). *Let $\varphi$ be even and satisfying Assumption [1](#ass: mol){reference-type="ref" reference="ass: mol"}, and $f : \mathbb R\to \mathbb R$ be a function that is convex in $(a,b)$. Then, for each $x,y \in (a,b)$ with $x < y$ there exists a $\delta  =  \delta(x,y)> 0$ such that for all $\varepsilon\in (0,\delta)$ we have that $F_{\varepsilon} = \varphi_{\varepsilon} * f \geq f$ on $(x,y)$.*
:::

::: proof
*Proof.* Let $x,y \in (a,b)$. There exists a $\delta>0$ such that $(x-\delta,y+\delta) \subset (a,b)$. Choose $\varepsilon\in (0,\delta)$ and take $\xi \in (x,y) \subset (a,b)$. Then $(\xi-\varepsilon,\xi+\varepsilon) \subset (x-\varepsilon,y+\varepsilon) \subset
    (x-\delta,y+\delta)\subset (a,b)$. Since $f$ is convex in $(\xi-\varepsilon,\xi+\varepsilon)$ we can apply Jensen's inequality leading to $$\begin{align*}
        F_{\varepsilon}(\xi) &= (\varphi_{\varepsilon} * f)(\xi) 
        =
        \int_{(-\varepsilon,\varepsilon)}f(\xi-t)\varphi_{\varepsilon}(t)\mathrm{d}\lambda(t) \\
        &\geq
        f\left(\int_{(-\varepsilon,\varepsilon)}(\xi-t)\varphi_{\varepsilon}(t)\mathrm{d}\lambda(t)\right) \\
        &= f( (\varphi_{\varepsilon} * \mathop{\mathrm{id}})(\xi))
        = f(\xi),
\end{align*}$$ where the last equality comes from Proposition [3](#prop:MollifyIdentityIsIdentity){reference-type="ref" reference="prop:MollifyIdentityIsIdentity"}. Since $\xi \in (x,y)$ was arbitrary the result follows. ◻
:::

::: remark
**Remark 3**. *Note that as it can be seen in Example [2](#example: LocalConvexityNotPreserved){reference-type="ref" reference="example: LocalConvexityNotPreserved"}, Proposition [5](#prop:MolliAboveFConvexityLocally){reference-type="ref" reference="prop:MolliAboveFConvexityLocally"} does not hold for any $\varepsilon> 0$. Indeed, also note that if the function is locally concave then we reach a similar result where the original function will be above the mollified function.*
:::

## Quasiconvexity under mollification

Any convex function is quasiconvex, but the converse does not hold in general. Therefore, quasiconvexity is a weaker condition than convexity, and it is important to study how it is preserved under mollification. From an engineering standpoint, this is particularly useful for estimating the shape of the mollified curve.

::: {#def:Quasiconvex .definition}
**Definition 3** (Quasiconvex function). *Let $S$ be a non empty convex set and $f : S \to \mathbb R$ be a real-valued function. We say that $f$ is quasiconvex if for all $\alpha \in \mathbb R$ the set $$\begin{equation*}
        S_{\alpha} := \{x \in S \mid f(x) \leq \alpha\}
\end{equation*}$$ is convex. An equivalent definition is that $f$ is quasiconvex if for all $x,y\in S$ and all $\gamma \in [0,1]$ we have $$\begin{equation*}
        f(\gamma x + (1-\gamma)y) \leq \max \{f(x),f(y)\}. \; \square
\end{equation*}$$*
:::

We need the following lemma before proving that quasiconvexity is preserved under mollification.

::: {#lemma:QuasiconvexFunctionMeasurable .lemma}
**Lemma 4**. *Let $f : \mathbb R\to \mathbb R$ be a quasiconvex function, $a,b \in \mathbb R$, and define $g := a \mathop{\mathrm{id}}+ b$; then, the following statements hold:*

1.  *$f$ is measurable, and*

2.  *$f \circ g$ is quasiconvex.*
:::

::: proof
*Proof.* First we prove that $f$ is measurable. Note that for any $\alpha \in \mathbb R$ the set $S_{\alpha} = \{x \in \mathbb R\mid f(x) \leq \alpha\}$ is a convex set, therefore path connected, hence connected. Since a set in $\mathbb R$ is connected if and only if it is an interval, then $S_{\alpha}$ is an interval. Thus, it is measurable because any interval is a Borel set.

We now prove that $f \circ g$ is quasiconvex. Let $\alpha \in \mathbb R$ and define the set $$\begin{equation*}
        S_{\alpha} := \{x \in \mathbb R\mid (f \circ g)(x) \leq \alpha\} = \{x \in \mathbb R
        \mid f(ax  + b) \leq \alpha\}.
\end{equation*}$$ If $S_{\alpha}$ is empty then it is convex by definition, and if $S_{\alpha}$ is a singleton is also convex. Therefore, suppose that $S_{\alpha}$ consists of at least two elements. Choose $x,y \in S_{\alpha}$ and $\gamma \in [0,1]$. Then $$\begin{align*}
        f(a(\gamma x + (1-\gamma)y) + b) &= f(\gamma(ax+b) + (1-\gamma)(ay+b)) \\
        &\leq \max \{f(ax+b), f(ay+b)\} \\
        &\leq \max \{\alpha,\alpha\} \\
        &= \alpha.
\end{align*}$$ That is, $\gamma  x + (1-\gamma)y \in S_{\alpha}$. Therefore $S_{\alpha}$ is a convex set, proving $f \circ g$ is quasiconvex. ◻
:::

Having presented the main properties of quasiconvex functions, let us consider a representative quasiconvex case, the monotonic function. Interesting enough, the mollified function of a monotonic path, e.g., a staircase-like sequence of steps, will also be monotonic.

::: {#prop:Monotonicity .proposition}
**Proposition 6** (Monotonicity and mollification). *Let $f \in L^1_{loc}(\mathbb R)$ be monotone increasing (resp. decreasing); then for any nonnegative mollifier $\varphi$ and $\varepsilon> 0$ the function $F_{\varepsilon} := (\varphi_{\varepsilon} * f)$ is monotone increasing (resp. decreasing).*
:::

::: proof
*Proof.* Suppose $f$ is monotone increasing. Let $x,y \in \mathbb R$ with $x > y$. Then for any $t \in \mathbb R$ we have $x-t > y-t$, thus $f(x-t) \geq f(y-t)$. $$\begin{align*}
        F_{\varepsilon}(x)-F_{\varepsilon}(y) &=
        \int_{\mathbb R}[f(x-t)-f(y-t)]\varphi_{\varepsilon}(t)\mathrm{d}\lambda(t) \geq 0,
\end{align*}$$ since $\varphi_{\varepsilon}$ is positive. The proof is identical for monotone decreasing functions. ◻
:::

:::: {#fig:MollificationOfStepStairFunction .figure latex-placement="ht"}
![](GonzlezCalvin2025Efficient_figs/MollificationDiscontinuousFunction.png){width="\\linewidth"}

::: caption
Mollification of stair-step function created using shifted Heaviside step functions. The blue solid line represents the (discontinuous) stair-step function $f$, while the red solid line represents its mollification using the mollifier [\[eq:OurMollifier\]](#eq:OurMollifier){reference-type="eqref" reference="eq:OurMollifier"} and $\varepsilon= 0.5$. Due to Proposition [6](#prop:Monotonicity){reference-type="ref" reference="prop:Monotonicity"}, $F_{\varepsilon}$ cannot present overshoots or oscillations.
:::
::::

Suppose the desired trajectory is the Heaviside step function $h :\mathbb R\to \mathbb R$ defined by $h(t) = \mathop{\mathrm{ind}}_{(0,\infty)}(t)$. By this result, its mollification is also monotonically increasing, so the mollified trajectory cannot exhibit overshoots or oscillations, see Figure [4](#fig:MollificationOfStepStairFunction){reference-type="ref" reference="fig:MollificationOfStepStairFunction"}; this contrasts with the Gibbs phenomenon. We finally show that quasiconvexity is preserved under mollification with a nonnegative mollifier.

::: {#thm:QuasiconvexityIsPreserved .theorem}
**Theorem 5**. *Suppose $f : \mathbb R\to \mathbb R$ is a quasiconvex function and let $\varphi$ be a mollifier satisfying Assumption [1](#ass: mol){reference-type="ref" reference="ass: mol"}; then, for all $\varepsilon>
    0$ the function $F_{\varepsilon} := f * \varphi_{\varepsilon}$ is quasiconvex.*
:::

::: proof
*Proof.* We are going to proceed by contradiction. Let $f$ be quasiconvex, and suppose that there exists an $\varepsilon> 0$ such that $F_{\varepsilon}$ is not quasiconvex. This implies there exist $x,y \in \mathbb R$ and $\gamma \in [0,1]$ such that $$\begin{equation*}
        F(\gamma x + (1-\gamma)y) > \max\{F(x),F(y)\}.
\end{equation*}$$ In particular $$\begin{align*}
        &F_{\varepsilon}(\gamma x + (1-\gamma)y) - F_{\varepsilon}(x) \\
        &=
        \int_{(-\varepsilon,\varepsilon)}\left[f(\gamma x +
        (1-\gamma)y-t)-f(x-t)\right]\varphi_{\varepsilon}(t)\mathrm{d}\lambda(t) > 0.
\end{align*}$$ First, we claim that the set $V_1 := \{t \in (-\varepsilon,\varepsilon) \mid f(\gamma x +
    (1-\gamma)y-t)-f(x-t) > 0\}$ is measurable and it has positive measure. By Lemma [4](#lemma:QuasiconvexFunctionMeasurable){reference-type="ref" reference="lemma:QuasiconvexFunctionMeasurable"} we know that the composition of a quasiconvex function with an affine mapping is quasiconvex, hence measurable. Since the linear combination of two measurable function results in a measurable function, the set $V_1$ is measurable. Thus, if $\lambda(V_1)$ were zero, then it would be negligible in integration, which would imply that $$\begin{align*}
        0&< \int_{(-\varepsilon,\varepsilon)}\left[f(\gamma x +
        (1-\gamma)y-t)-f(x-t)\right]\varphi_{\varepsilon}(t)\mathrm{d}\lambda(t) \\
        &=\int_{\left[(-\varepsilon,\varepsilon)\setminus V_1\right] \cup V_1}\left[f(\gamma x +
        (1-\gamma)y-t)-f(x-t)\right]\varphi_{\varepsilon}(t)\mathrm{d}\lambda(t)  \\
        &=\int_{(-\varepsilon,\varepsilon)\setminus V_1}\left[f(\gamma x +
        (1-\gamma)y-t)-f(x-t)\right]\varphi_{\varepsilon}(t)\mathrm{d}\lambda(t),
\end{align*}$$ but $(-\varepsilon,\varepsilon)\setminus V_1 = \{t \in (-\varepsilon,\varepsilon) \mid t \notin V_1\} = \{t
    \in (-\varepsilon,\varepsilon) \mid f(\gamma x + (1-\gamma)y-t)-f(x-t) \leq 0\}$ and $\varphi$ is nonnegative, thus $$\begin{equation*}
        \int_{(-\varepsilon,\varepsilon)\setminus V_1}\left[f(\gamma x +
        (1-\gamma)y-t)-f(x-t)\right]\varphi_{\varepsilon}(t)\mathrm{d}\lambda(t) \leq 0,
\end{equation*}$$ which leads to the first contradiction. Therefore $\lambda(V_1) > 0 \Longrightarrow V_1
    \neq \emptyset$. Moreover, since $f$ is quasiconvex we have that for any $t
    \in V_1$ $$\begin{align*}
        f(x-t) &< f(\gamma x + (1-\gamma)y -t)  \\
        &=
        f(\gamma(x-t)+(1-\gamma)(y-t)) \\
        &\leq \max\{f(x-t),f(y-t)\}.
\end{align*}$$ Now let us consider that $$\begin{equation}
\label{eq:ConjectureProofEq1}
        f(y-t) > f(x-t), \quad \forall t \in V_1.
\end{equation}$$ because if not, we would reach a contradiction; therefore, proving that our assumption about $F_{\varepsilon}$ is false, thus proving the theorem.

The same procedure can be done considering the other point, $y$, and $F_{\varepsilon}(\gamma x + (1-\gamma)y) - F_{\varepsilon}(y) > 0$, i.e., there exists a set of positive measure $V_2 \subset (-\varepsilon,\varepsilon)$ such that $$\begin{equation*}
        f(\gamma x + (1-\gamma)y -t) - f(y-t) > 0, \quad \forall t \in V_2,
\end{equation*}$$ and since $f$ is quasiconvex, with the same arguments as above $$\begin{equation}
\label{eq:ConjectureProofEq2}
        f(x-t) > f(y-t), \quad \forall t \in V_2.
\end{equation}$$ Suppose $V_1 \cap V_2 \neq \emptyset$. This implies that there exists a $t
    \in V_1\cap V_2$ such that $f(y-t) < f(x-t) < f(y-t)$ which is again a contradiction, thus proving the theorem. So we just need to prove that we reach a contradiction in the case $V_1 \cap V_2 = \emptyset$. Take $t_1 \in
    V_1$ and $t_2 \in V_2$ and any $\beta \in [0,1]$, then $$\begin{align*}
        f(y-\beta t_1 - (1-\beta)t_2) &= f(\beta(y-t_1)+(1-\beta)(y-t_2)) \\
        &\leq
        \max \{f(y-t_1), f(y-t_2)\}
\end{align*}$$ However, $f(y-t_2) < f(x-t_2)$ because of [\[eq:ConjectureProofEq2\]](#eq:ConjectureProofEq2){reference-type="eqref" reference="eq:ConjectureProofEq2"}, thus $$\begin{align*}
        f(y-\beta t_1 - (1-\beta)t_2)< \max\{f(y-t_1), f(x-t_2)\}, \\ 
        \quad \forall
        \beta \in [0,1].
\end{align*}$$ Using the same approach and considering [\[eq:ConjectureProofEq1\]](#eq:ConjectureProofEq1){reference-type="eqref" reference="eq:ConjectureProofEq1"} we have that $$\begin{align*}
        f(x-\beta t_1 - (1-\beta)t_2) < \max\{f(y-t_1), f(x-t_2)\}, \\ \quad
        \forall \beta \in [0,1].
\end{align*}$$ Since this is independent of the value of $\beta$, and in particular for $\beta = 1$ and $\beta = 0$ we have that $$\begin{align*}
        f(y-t_1) < \max\{f(y-t_1),f(x-t_2)\} \\
        f(x-t_2) < \max\{f(y-t_1),f(x-t_2)\},
\end{align*}$$ but this leads to a contradiction. Therefore, the assumption that there exists an $\varepsilon> 0$ for which $F_{\varepsilon}$ is not quasiconvex is false. That is, $F_{\varepsilon}$ is quasiconvex for any $\varepsilon> 0$. ◻
:::

::: {#rem: Q .remark}
**Remark 4**. *The converse is not in general true. That is, having $F_{\varepsilon}$ quasiconvex for some $\varepsilon> 0$ does not imply that $f$ is quasiconvex. For example, consider the following measurable function that is not quasiconvex $$\begin{equation*}
       f(x) = \begin{cases}
            1, & x\in \mathbb R\setminus \mathbb Q\\
            2, & x \in \mathbb Q
        \end{cases},
\end{equation*}$$ because the set $S_{1.5} = \{x \in \mathbb R\mid
    f(x) \leq 1.5\} = \mathbb R\setminus \mathbb Q$ is disconnected, hence it is not convex. However, since $\lambda(\mathbb Q)= 0$, we have that for any $x \in \mathbb R$ $$\begin{align*}
        F_{\varepsilon}(x) &= \int_{\mathbb R}\varphi(x-t)f(t)\mathrm{d}\lambda(t) 
        = \int_{\mathbb R\setminus
            \mathbb Q}\varphi(x-t)\mathrm{d}\lambda(t) \\
            &=
        \int_{(\mathbb R\setminus \mathbb Q) \cup \mathbb Q} \varphi(x-t) \mathrm{d}\lambda(t) = \int_{\mathbb R}
        \varphi \mathrm{d}\lambda = 1,
\end{align*}$$ which is convex; thus quasiconvex too. Moreover, it is clear that if $F_{\varepsilon}$ is quasiconvex for all $\varepsilon> 0$ then $f$ is quasiconvex since the pointwise limit of a family of quasiconvex functions can be shown to be quasiconvex function as well.*
:::

## Enclosure and length of paths

So far, we have worked with real-valued functions because we represent desired paths or trajectories as parametric functions, i.e., functions $f : \mathbb R\to \mathbb R^n$. Nonetheless, we still want to characterize (in advance) how mollification affects the complete function $f$, that is, treat it as a whole. We now address the following question: given the original trajectory, does there exist a subset $U$ of $\mathbb R^n$ such that the mollified trajectory is contained in $U$ for any value of its parameter? The answer is affirmative, with $U$ being the convex hull of $f(\mathbb R)$.

::: definition
**Definition 4**. *Let $A \subset \mathbb R^n$ be a set. Its convex hull, denoted as $\mathop{\mathrm{co}}(A)$ is defined as the smallest convex set that contains $A$, that is, $A \subset \mathop{\mathrm{co}}(A)$. $\square$*
:::

We first present a result when $\mathop{\mathrm{dom}}f = \mathbb R$.

::: {#thm:ConvexHull .theorem}
**Theorem 6**. *Let $f : \mathbb R\to \mathbb R^n$ be a measurable function and $\varphi$ be a nonnegative mollifier. Define for $t \in \mathbb R$ and $\varepsilon> 0$ $$\begin{equation*}
        F_{\varepsilon}(t) := (f * \varphi_{\varepsilon})(t) = \left((f_1 * \varphi_{\varepsilon})(t),
        \dots, (f_{n}*\varphi_{\varepsilon})(t)\right).
\end{equation*}$$ Then, given $\varepsilon> 0$, we have that $$\begin{equation*}
        \left\{F_{\varepsilon}(t) \mid t \in \mathbb R\right\} \subset \mathop{\mathrm{co}}\left\{f(t) \mid t \in \mathbb R\right\}.
\end{equation*}$$*
:::

::: proof
*Proof.* Let $U = \mathop{\mathrm{co}}\{f(t) \mid t \in \mathbb R\}$. Define the extended real valued function $I_{U} : \mathbb R^n \to \mathbb R\cup \{-\infty,\infty\}$ as $$\begin{equation*}
        I_{U}(x) = \begin{cases}
            +\infty, & x \notin U  \\
            0, & x \in U
        \end{cases}.
\end{equation*}$$ The function $I_{U}$ is clearly convex. Fix $t \in \mathop{\mathrm{dom}}f$. Noting that $\int_{\mathbb R}\varphi_{\varepsilon}\mathrm{d}\lambda = 1$ and $\varphi_{\varepsilon} \geq 0$, we can apply Jensens' Inequality in higher dimensions to get $$\begin{align*}
        0 \leq I_U(F_{\varepsilon}(t)) &=
        I_{U}\left(\int_{\mathop{\mathrm{supp}}
        \varphi_{\varepsilon}}f(t-s)\varphi_{\varepsilon}(s)\mathrm{d}\lambda(s)\right) \\
        &\leq
        \int_{\mathop{\mathrm{supp}}\varphi_{\varepsilon}}I_{U}(f(t-s))\varphi_{\varepsilon}(s)\mathrm{d}\lambda(s).
\end{align*}$$ However, note that $I_{U}(f(t-s)) = 0$ for any $t-s\in \mathop{\mathrm{dom}}f$, and since $\mathop{\mathrm{dom}}f = \mathbb R$ then $$\begin{equation*}
        0 \leq I_U(F_{\varepsilon}(t)) \leq 
        \int_{\mathop{\mathrm{supp}}\varphi_{\varepsilon}}I_{U}(f(t-s))\varphi_{\varepsilon}(s)\mathrm{d}\lambda(s) = 0,
\end{equation*}$$ i.e., $I_U(F_{\varepsilon}(t)) = 0$ so $F_{\varepsilon}(t) \in U$. Since $t$ and $\varepsilon$ are arbitrary, the claim follows. ◻
:::

::: {#rmk:ContinuousExtension .remark}
**Remark 5**. *It is common that the path is a continuous function defined in a compact subset of $\mathbb R$, i.e., $f : [a,b] \to \mathbb R^n$ with $-\infty < a < b < \infty$. In such a case, we can extend the function $f$ to $\mathbb R$ as follows to get a new continuous function $$\begin{equation*}
    \bar f(t) = \begin{cases}
        f(a), & -\infty < t \leq a \\
        f(x), & a \leq t \leq  b \\
        f(b), & b \leq t < \infty
    \end{cases}.
\end{equation*}$$ Note that $\bar f([a,b]) = f([a,b])$ and $\bar f((-\infty,a]\cup[b,\infty))
= \{f(a),f(b)\}$, so $\bar{f}(\mathbb R) = f([a,b])$ and then $\mathop{\mathrm{co}}\bar{f}(\mathbb R) =
\mathop{\mathrm{co}}f([a,b])$. Then we can use as our path $\bar{f}$ instead of $f$, obtaining the result of the previous theorem, and later restricting the domain of the mollified function to $[a,b]$ again, i.e., we let $\bar F_{\varepsilon} = \bar{f} * \varphi_{\varepsilon}$ and use the mollified curve $F_{\varepsilon} = \bar{F}_{\varepsilon}|_{[a,b]}$, thus $$\begin{equation*}
    F_{\varepsilon}([a,b]) \subset \bar{F}(\mathbb R) \subset \mathop{\mathrm{co}}\bar f(\mathbb R) = \mathop{\mathrm{co}}
    f([a,b]).
\end{equation*}$$ Clearly for $t \in [a+\varepsilon,b-\varepsilon]$, $F_{\varepsilon}$ coincides with the mollification of $f$, and in $[a,a+\varepsilon)$ and $(b-\varepsilon,b]$ it belongs to the convex hull of $f([a,b])$.*
:::

Having characterized the space in which the mollified path is enclosed, we now consider the relationship between the length of the original path and its mollification. First, we introduce the definition of path length for paths that do not need to be differentiable.

::: definition
**Definition 5** (Length of $f$). *Let $f : [a,b] \to \mathbb R^n$ be a continuous function, and $||\cdot|| : \mathbb R^n \to [0,\infty)$ be any norm in $\mathbb R^n$. Let a finite set $P = \{x_0,x_1,\dots,x_N\}$, where $a = x_0 < x_1 < \dots < x_N = b$ be a partition of $[a,b]$. Then, the length of $f$ is $$\begin{equation*}
        L(f) := \sup_{P \text{ partition of } [a,b]}\sum_{i=1}^{N}||f(x_i)-f(x_{i-1})||. \, \square
\end{equation*}$$*
:::

Note that when working with trajectories with compact domain, we must extend them as done in Remark [5](#rmk:ContinuousExtension){reference-type="ref" reference="rmk:ContinuousExtension"}.

::: {#lem:LengthOfPaths .lemma}
**Lemma 7**. *Let $f : [a,b] \to \mathbb R^n$ be a continuous function and fix $\varepsilon> 0$. Let $\bar f : 
    [a-\varepsilon,b+\varepsilon]$ be its continuous extension as done in Remark [5](#rmk:ContinuousExtension){reference-type="ref" reference="rmk:ContinuousExtension"}. The following two statements are true:*

1.  *$L(\bar f) = L(f)$.*

2.  *If $|t| \leq \varepsilon$ and $g(s) = \bar f(s-t)$ for all $s \in [a,b]$, then $L(g) \leq L(\bar f) = L(f)$.*
:::

::: proof
*Proof.* We prove each statement separately.

1.  Take a partition $P$ of $[a-\varepsilon,b+\varepsilon]$ with $N$ elements, such that there exists $0 < J < K < N$ such that $x_j = a$ and $x_k =
            b$. Then $$\begin{align*}
                &\sum_P||\bar f(x_i)-\bar f(x_{i-1})|| \\
                &=
                \sum_{i=1}^{J-1}||f(x_i)-f(x_{i-1})|| +
                \sum_{i=J}^{K}||f(x_i)-f(x_{i-1})|| \\
                &+ \sum_{i={K+1}}^{N}||f(x_i)-f(x_{i-1})|| \\
                &= \sum_{i=J}^K||f(x_i)-f(x_{i-1})|| \leq L(f),
    \end{align*}$$ where the last inequality comes from the fact that $\{x_J, \dots, x_K\}$ is a partition of $[a,b]$. Therefore, by definition of the supremum $L(\bar f) \leq L(f)$. The inequality $L(f) \leq L(\bar f)$ holds trivially by noting that a partition of $[a,b]$ can be extended to create a partition of $[a-\varepsilon,a+\varepsilon]$ and we are summing positive terms. Therefore $L(f) = L(\bar f)$.

2.  Let $|t| \leq \varepsilon$ and consider a partition $P = \{x_0,\dots,x_N\}$ of $[a,b]$. Clearly $P- \{t\} = \{x_0-t,\dots,x_n-t\}$ could be considered as a subset of a partition of $[a-\varepsilon,a+\varepsilon]$. Therefore by constructing $P' = (P-\{t\})\cup\{a-\varepsilon,b+\varepsilon\}$ then $$\begin{align*}
                &\sum_P||g(x_i)-g(x_{i-1})|| \\
                &= \sum_P||\bar f(x_i-t)-\bar
                f(x_{i-1}-t)|| \\
                &= \sum_{P-\{t\}}||\bar f(y_i)-\bar f(y_{i-1})|| \\
                &\leq
                \sum_{(P-\{t\})\cup\{a-\varepsilon,b+\varepsilon\}}||f(y_i)-f(y_{i-1})|| \\
                &\leq
                \sup_{P \text{ partition of }[a-\varepsilon,b+\varepsilon]}\sum_P||f(y_i)-f(y_{i-1})||
                =L(\bar f).
    \end{align*}$$ Since the supremum is the least upper bound, it follows that $L(g) \leq L(\bar f) = L(f)$.

 ◻
:::

Now we are ready for the main result regarding the length of the generated mollified path being shorter or equal than the original.

::: {#thm:Length .theorem}
**Theorem 8**. *Let $f : [a,b] \to \mathbb R^n$ be a continuous function and let $\varphi$ be a nonnegative mollifier. Fixed $\varepsilon> 0$ let $\bar f :[a-\varepsilon,b+\varepsilon] \to \mathbb R^n$ be the continuous extension as in remark [5](#rmk:ContinuousExtension){reference-type="ref" reference="rmk:ContinuousExtension"}. Define $F : [a,b] \to \mathbb R^n$ as $F = \bar f * \varphi_{\varepsilon}$; then $L(F) \leq L(f)$.*
:::

::: proof
*Proof.* Take a partition $P$ of $[a,b]$, then $$\begin{align*}
        &\sum_P||F(x_i)-F(x_{i-1})|| \\
        &\underset{||\cdot||\text{ Jens. ineq}}{\leq}
        \sum_P\int_{[-\varepsilon,\varepsilon]}||\bar f(x_i-t)-\bar f(x_{i-1}-t)||\varphi_{\varepsilon}(t)\mathrm{d}t \\
        &\underset{\text{linearity of integral}}{\leq}\int_{[-\varepsilon,\varepsilon]}\sum_P||\bar
        f(x_i-t)-\bar f(x_{i-1}-t)||\varphi_{\varepsilon}(t)\mathrm{d}t \\
        &\leq \int_{[-\varepsilon,\varepsilon]}\sup_{P' \text{ part. of } [a,b]}\sum_{P'}||\bar
        f(x_i-t)-\bar f(x_{i-1}-t)||\varphi_{\varepsilon}(t)\mathrm{d}t \\
        &\underset{\text{Lemma
        \ref{lem:LengthOfPaths}}}{\leq}\int_{[-\varepsilon,\varepsilon]}L(\bar
        f)\varphi_{\varepsilon}(t)\mathrm{d}t =L(\bar f) = L(f),
\end{align*}$$ thus, by definition of the supremum, $L(F) \leq L(f)$. ◻
:::

::: {#rmk:EndingAndInitialPoints .remark}
**Remark 6**. *Note that this does not imply that if $f$ is a geodesic between $f(a)$ and $f(b)$, then $F$ is also a geodesic between these points. This is because $F(a)
\neq f(a)$ or $F(b) \neq f(b)$ may occur. While Theorem [6](#thm:ConvexHull){reference-type="ref" reference="thm:ConvexHull"} and Remark [5](#rmk:ContinuousExtension){reference-type="ref" reference="rmk:ContinuousExtension"} guarantee that $F([a,b]) = (\bar
f*\varphi_{\varepsilon})([a,b]) \subset \mathop{\mathrm{co}}f([a,b])$, we cannot ensure that $F$ has the same starting and ending points as $f$. What Theorem [8](#thm:Length){reference-type="ref" reference="thm:Length"} establishes is that by considering the actual starting and ending points of $F$, we can ensure that $L(F) \leq L(f)$. An example of this property is shown in Figure [5](#fig:MolliDifferentPointsAndLengths){reference-type="ref" reference="fig:MolliDifferentPointsAndLengths"}. The original function, which is a linear interpolation of three points in $\mathbb R^2$ and whose domain is $[a,b]=[0,2]$, is extended to the domain $[-\varepsilon,2+\varepsilon]$ with $\varepsilon= 0.5$ using the extension presented in remark [5](#rmk:ContinuousExtension){reference-type="ref" reference="rmk:ContinuousExtension"}. As it can be seen from each of its components, $F_{\varepsilon}(a) \neq f(a)$ and $F_{\varepsilon}(b) \neq f(b)$, and clearly $L(F_{\varepsilon}) \leq L(f)$ as Theorem [8](#thm:Length){reference-type="ref" reference="thm:Length"} states. Finally note that, while $f_2$ can be considered a geodesic between the points $(0,0)$ and $(2,2)$ in $\mathbb R^2$ using the Euclidean norm, $(f_2 * \varphi_{\varepsilon})$ is not a geodesic between those two points.*
:::

:::: {#fig:MolliDifferentPointsAndLengths .figure latex-placement="t"}
![](GonzlezCalvin2025Efficient_figs/MollificationDifferentPoints.png){width="\\linewidth"}

::: caption
Visual representation of remark [6](#rmk:EndingAndInitialPoints){reference-type="ref" reference="rmk:EndingAndInitialPoints"}. The left picture represents the original path $f$ as a blue solid line, and as a red solid line its mollification $F_{\varepsilon} = (f_1 *
    \varphi_{\varepsilon}, f_2 * \varphi_{\varepsilon})$ where $\varphi$ is as in [\[eq:OurMollifier\]](#eq:OurMollifier){reference-type="eqref" reference="eq:OurMollifier"} and $\varepsilon= 0.5$. The middle picture represents the same information but for the first component of the function and its mollification, while the right picture represents the same information but for the second component.
:::
::::

## The effect of reparametrization and mollification

Suppose the desired path is encoded using a continuous function $f :
[a,b] \to \mathbb R^n$ and for a given $\varepsilon> 0$ we consider its mollification with parameter $\varepsilon$. As we have seen, we first need to extend the function $f$ to $\bar{f} : [a-\varepsilon,b+\varepsilon]$ as is done in Remark [5](#rmk:ContinuousExtension){reference-type="ref" reference="rmk:ContinuousExtension"} or in Theorem [8](#thm:Length){reference-type="ref" reference="thm:Length"}. It may be of interest to reparametrize the curve so it is normalized, i.e., to find a function $g : [-\varepsilon,1+\varepsilon] \to [a-\varepsilon,b+\varepsilon]$, and consider $\bar{f} \circ g * \varphi_{\varepsilon} : [0,1] \to \mathbb R^n$, as the desired mollified path. How does the parameter of the mollification change under these conditions? That is, does there exist a $\eta = \eta(\varepsilon) > 0$ such that $$\begin{equation*}
    (\bar f \circ g * \varphi_{\varepsilon}) ([0,1]) = (\bar f * \varphi_{\eta})([a,b])?
\end{equation*}$$

What we require is a continuous function $g:[-\varepsilon,1+\varepsilon] \to [a-\varepsilon,b+\varepsilon]$ that is strictly increasing and satisfies $g([0,1]) = [a,b]$. However, it is easy to see that such a function must be nonlinear. In the best-case scenario where such a function exists it is invertible, if it happens to be differentiable, we arrive at the following conclusions. Suppose $g : [-\varepsilon,1+\varepsilon] \to [a-\varepsilon,b+\varepsilon]$ is a continuously differentiable, increasing function that is nonlinear but satisfies $g([0,1]) = [a,b]$---as previously required. In this case, let $s \in [0,1]$ and applying the change of variables $v(t) = g(s-t)$, we get $$\begin{align*}
        &(f*\varphi_{\varepsilon})(s)=\int_{[-\varepsilon,\varepsilon]}f(g(s-t))\varphi_{\varepsilon}(t)\mathrm{d}t \\
        %&\underset{u=t/\ep}{=} \int_{[-1,1]}f(g(s-\ep u))\varphi(u)\mathrm{d}u \\
        &=
        \int_{[g(s-\varepsilon),g(s+\varepsilon)]}f(v)\varphi\left(\frac{s-g^{-1}(v)}{\varepsilon}\right)\frac{1}{\varepsilon
        g'(g^{-1}(v))}\mathrm{d}v \\
        &= \int_{[g(s-\varepsilon), g(s+\varepsilon)]}f(v)\varphi_{\varepsilon}(s-g^{-1}(v))\frac{1}{g'(g^{-1}(v))}\mathrm{d}v.
\end{align*}$$ Since $g$ is nonlinear, there is no straightforward way to solve for $v$ and obtain a convolution-like expression with a single parameter in terms of $\varepsilon$. The effect to the reparametrization on $\varepsilon$ may seem like an artificial question to be posed. Nevertheless, note that for a planar $f$ that is parametrized in arc length, its curvature can be simply computed as $\kappa(s) = ||f''(s)||_2$, with $s \in [0,L(f)]$. Nevertheless, the arc-length parametrization is, in general, non-linear. Therefore we have shown that we cannot find an upper bound for the curvature that depends on the parameter $\varepsilon$ for the mollified curve using arc-length parametrization. Moreover, we add that it can be shown, but it is not included in this work due to its cumbersome formulas, that if the mapping $g : [-\varepsilon,1+\varepsilon] \to
[a-\varepsilon,b+\varepsilon]$ is affine, continuous and increasing, then it is *unique*, and there is an expression relating $\eta$ and $\varepsilon$, which can be easily found by rudimentary computations. Nevertheless, it happens that $(\bar{f} \circ g * \varphi_{\varepsilon})([0,1]) \subset (\bar{f} *
\varphi_{\eta})([a,b])$, which implies that we do not generate the complete mollified path after the reparametrization. Thus, even in the affine reparametrization situation, the mollification does not behave well under the reparametrization of curves.

# Curvature guarantees from a sequence of waypoints {#sec: curvature}

In this section, we show how to systematically analyze the curvature of the generated path. In particular, we provide a formula to upper bound the curvature of the mollification of a sequence of 2D or 3D waypoints connected by straight line segments, i.e., via linear interpolation. First, we restrict ourselves to the simpler case of two segments. From now on, $\mathbb R^n$ denotes either $\mathbb R^2$ or $\mathbb R^3$.

## The case of three points forming two segments

Suppose the desired path can be encoded using a parametric function of the following form.

::: {#def:TwoLinesSegment .definition}
**Definition 6** (Two line segments function). *Let $P_0,P_1,P_2 \in \mathbb R^n$, and let $f : [0,2] \to \mathbb R^n$ be $$\begin{equation}
\label{eq:TwoLineSegments}
    f(t) = \begin{cases}
        P_0 + (P_1-P_0)t, & t \in [0,1], \\
        P_1 + (P_2-P_1)(t-1), & t \in [1,2]
    \end{cases}.
\end{equation}$$ We call $f$ the two-line segments function. And we call $$\begin{equation}
\label{eq:TwoLinesSegmentsExtended}
    \bar{f}(t) = \begin{cases}
        P_0 + (P_1-P_0)t, & t \in (-\infty,1], \\
        P_1 + (P_2-P_1)(t-1), & t \in [1,\infty)
    \end{cases},
\end{equation}$$ the two-lines segment extended function. Note that $\bar{f}\mid_{[0,2]} = f$. $\square$*
:::

We know by Proposition [3](#prop:MollifyIdentityIsIdentity){reference-type="ref" reference="prop:MollifyIdentityIsIdentity"} that affine functions are invariant under mollification when Assumption [1](#ass: mol){reference-type="ref" reference="ass: mol"} is met and the mollifier is an even function, such as in Example [1](#example:OurMollifier){reference-type="ref" reference="example:OurMollifier"}. From Figure [3](#fig:MollifOfAbs){reference-type="ref" reference="fig:MollifOfAbs"} and Proposition [4](#prop:ConvexityThenMolliAbove){reference-type="ref" reference="prop:ConvexityThenMolliAbove"} it is clear that for the curve defined in Definition [6](#def:TwoLinesSegment){reference-type="ref" reference="def:TwoLinesSegment"} it happens that $f(1) \neq F_{\varepsilon}(1)$ for all $\varepsilon> 0$. However, it of special interesting to compute the intervals in which the original and the mollified curve coincide, because in those intervals there is no approximation, there is an equality between the original and mollified curve. This is easily answered in the next proposition, in which we show that the initial and ending points of the original and mollified curve also coincide.

::: {#prop:EqualityInSets .proposition}
**Proposition 7**. *Let $\bar{f}$ be as in [\[eq:TwoLinesSegmentsExtended\]](#eq:TwoLinesSegmentsExtended){reference-type="eqref" reference="eq:TwoLinesSegmentsExtended"}. Suppose $\varepsilon\in (0,\frac{1}{2})$, define for $r \in \{1,2\}$, $V_r := [r-1+\varepsilon,r-\varepsilon]$ and let $F_{\varepsilon} := \bar{f} * \varphi_{\varepsilon}$ with $\varphi$ even. Then $F_{\varepsilon}|_{V}=\bar{f}|_V = f_V$, $F_{\varepsilon}(0) = f(0)$, and $F_{\varepsilon}(2) =
    f(2)$.*
:::

::: proof
*Proof.* Let $t \in V_r$, and note that for any $s \in [-\varepsilon,\varepsilon]$ it holds that $r-1 \leq t-\varepsilon< t-s < t+\varepsilon\leq r$. Thus, if $r = 1$ the function to be mollified is the line $P_0 + (P_1-P_0)t$ for any $t \in V_r$ and if $r = 2$ the function to be mollified is the line $P_1 + (P_2-P_1)(t-1)$ for any $t \in V_r$. Thus, by Proposition [3](#prop:MollifyIdentityIsIdentity){reference-type="ref" reference="prop:MollifyIdentityIsIdentity"} we get the desired result. The proof that the initial and ending points are the same it is carried in a similar fashion. ◻
:::

It is straightforward to note that $f$ is differentiable in $(0,2) \setminus \{1\}$ and $\bar{f}$ in $\mathbb R\setminus\{1\}$. Note that in both cases, the set of points on which the functions are not differentiable form a set of measure zero, and the expressions of their derivatives are constant functions. Let $t \in \mathbb R\setminus\{1\}$, then $$\begin{equation*}
    \bar{f}'(t) = \begin{cases}
        P_1-P_0, & t \in (-\infty,1) \\
        P_2-P_1, & t \in (1,\infty)
    \end{cases}.
\end{equation*}$$ For $r \in \mathbb N$ we define $\tilde{P}_r := P_{r} - P_{r-1}$. Note that both $f$ and $\bar{f}$ are continuous functions, hence locally integrable, and from Theorem [1](#thm:PropertiesOfMollifying){reference-type="ref" reference="thm:PropertiesOfMollifying"} we have that if $F_{\varepsilon} := \bar{f} *
\varphi_{\varepsilon}$ where $\varphi$ is any mollifier and $\varepsilon> 0$ then $F_{\varepsilon}' =
\bar{f} * \varphi_{\varepsilon}'$. It is not difficult to prove that in this case, $F_{\varepsilon}' = \bar{f} * \varphi_{\varepsilon}' = \bar{f}' * \varphi_{\varepsilon}$ for any $\varepsilon>
0$.

We can now exploit these results to obtain a formula for the curvature, as well as an upper bound.

### Computing the exact curvature

We know by the discussion above that $F_{\varepsilon}' =
(\bar{f}*\varphi'_{\varepsilon}) = (\bar{f}' * \varphi_{\varepsilon})$ everywhere. Consider a mollifier $\varphi$ and let $\varepsilon> 0$. Given $t \in \mathbb R\setminus \{1\}$, note that $$\begin{equation*}
    \bar{f}'(t) = \tilde{P}_1 \mathop{\mathrm{ind}}_{(-\infty,1)}(t) + \tilde{P}_2\mathop{\mathrm{ind}}_{(1,\infty)}(t),
\end{equation*}$$ hence for $t \in \mathbb R$ $$\begin{align*}
    F_{\varepsilon}'(t) &= \int_{\mathbb R}\varphi_{\varepsilon}(t-s)\bar{f}'(s)\mathrm{d}s \\
    &= 
    \int_{(-\infty,1]}\varphi_{\varepsilon}(t-s)\tilde{P}_1\mathrm{d}s + \int_{[1,\infty)}\varphi_{\varepsilon}(t-s)\tilde{P}_2\mathrm{d}s \\
    &= \tilde{P}_1 \int_{(-\infty,1]}\varphi_{\varepsilon}(t-s)\mathrm{d}s + \tilde{P}_2
    \int_{[1,\infty)}\varphi_{\varepsilon}(t-s)\mathrm{d}s.
\end{align*}$$ Note that if $\Phi_{\varepsilon} : \mathbb R\to \mathbb R$ is such that $\Phi_{\varepsilon}' = \varphi_{\varepsilon}$, then $$\begin{align*}
    \frac{d}{dt}\int_{[a,b]}\varphi_{\varepsilon}(t-s)\mathrm{d}s &=
    \frac{d}{dt}\int_{[t-b,t-a]}\varphi_{\varepsilon}(u)\mathrm{d}u \\
    &= \frac{d}{dt}(\Phi_{\varepsilon}(t-b)-\Phi_{\varepsilon}(t-a)) \\
    &=\varphi_{\varepsilon}(t-b)-\varphi_{\varepsilon}(t-a),
\end{align*}$$ thus $$\begin{equation*}
    F_{\varepsilon}''(t) = \varphi_{\varepsilon}(t-1)(\tilde{P}_1-\tilde{P}_2).
\end{equation*}$$

Now define $$\begin{align*}
    A_1(t) &:= \int_{(-\infty,1]}\varphi_{\varepsilon}(t-s)\mathrm{d}s \\
    A_2(t) &:= \int_{[1,\infty)}\varphi_{\varepsilon}(t-s)\mathrm{d}s,
\end{align*}$$ therefore, if $\kappa : \mathbb R\to \mathbb R$ is the curvature,

$$\begin{align*}
    \kappa(t) &= \frac{|| F_{\varepsilon}''(t) \wedge F_{\varepsilon}'(t)||_2}{||F_{\varepsilon}'(t)||_2^3}
    \\ &= \frac{||\varphi_{\varepsilon}(t-1)(\tilde{P}_1-\tilde{P}_2) \wedge
    (\tilde{P}_1 A_1(t) + \tilde{P}_2 A_2(t))||_2}{||F_{\varepsilon}'(t)||_2^3} \\
    &=
    \varphi_{\varepsilon}(t-1)|A_2(t)+A_1(t)|\frac{
    ||\tilde{P}_2\wedge \tilde{P}_1||_2}{||\tilde{P}_1A_1(t)+\tilde{P}_2A_2(t)||_2^3},
\end{align*}$$

and noting that, due to the properties of the mollifier, $A_1(t)+A_2(t) = 1$ and $A_1(t),A_2(t) \geq 0$ for all $t \in \mathbb R$, we have that $$\begin{equation}
\label{eq:CurvatureClosedFormula}
    \kappa(t) = \varphi_{\varepsilon}(t-1)\frac{
    ||\tilde{P}_2\wedge \tilde{P}_1||_2}{||\tilde{P}_1A_1(t)+\tilde{P}_2A_2(t)||_2^3}.
\end{equation}$$ Equation [\[eq:CurvatureClosedFormula\]](#eq:CurvatureClosedFormula){reference-type="eqref" reference="eq:CurvatureClosedFormula"} is an exact formula for the curvature at each $t \in \mathbb R$.

### Upper bounding the curvature

Note that $\varphi_{\varepsilon}(t-1) \leq \frac{1}{\varepsilon}||\varphi||_{\infty}$ for all $t \in \mathbb R$. Moreover, it is clear that $F_{\varepsilon}'(t)$ is the convex combination of $\tilde{P}_1$ and $\tilde{P}_2$. Therefore $$\begin{equation*}
    ||F_{\varepsilon}'(t)||_2^2 \geq \min_{s\in[0,1]}||s\tilde{P}_1 + (1-s)\tilde{P}_2||_2^2 =: \min_{s\in[0,1]}g(s).
\end{equation*}$$ Note that $g$ is a differentiable convex function, so its minimum exists in the compact set $[0,1]$ and by the KKT conditions it is necessary and sufficient to find an $\bar{s} \in [0,1]$ such that $g'(\bar{s}) = 0$. In this case $$\begin{equation*}
    g'(\bar{s}) =0 \Longleftrightarrow \bar{s} = \frac{\left\langle \tilde{P}_2-\tilde{P}_1, \tilde{P}_2 \right\rangle}{||\tilde{P}_2-\tilde{P}_1||_2^2}.
\end{equation*}$$ Since $g$ is positive $||F_{\varepsilon}||_2 \geq \sqrt{g(\bar{s})}$. Also note that when differentiating, and making it equal to $0$ we are not constraining the values of $\bar{s}$. It may happen that $\bar{s} < 0$ or $\bar{s} > 0$. Nevertheless, since the function $g$ is convex---in fact, strictly convex as long as $\tilde{P}_1 \neq \tilde{P}_2$---we know that if the minimum of the unconstrained problem is not in the feasible set, i.e., $[0,1]$, then it is at the boundaries of the feasible set. For this reason if it happens that that $\bar{s} < 0$ then $g(0) = ||\tilde{P}_1||_2$ is the minimum value because $\bar{s} < 0$ is where the minimum occurs and the function is convex, while if $\bar{s}
> 1$ then $g(1) = ||\tilde{P}_2||_2$ is the minimum value. Therefore, $$\begin{align*}
\min_{s\in [0,1]}&||\tilde{P}_1s - \tilde{P}_2(1-s)||_2
 \\
&=\begin{cases}
        \left|\left|\tilde{P}_1
    \bar{s} +
    \left(1-\bar{s}\right)\tilde{P}_2\right|\right|_2,
    & 0 \leq \bar{s} \leq 1 \\
    \min\{||\tilde{P}_1||_2, ||\tilde{P}_2||_2\}, & \text{ otherwise }
    \end{cases}
\end{align*}$$ From which it follows that if $$\begin{align*}
    M(\tilde{P}_1,\tilde{P}_2)
    := \begin{cases}
        \frac{1}{\left|\left|\tilde{P}_1
    \bar{s} +
    \left(1-\bar{s}\right)\tilde{P}_2\right|\right|_2^3},
    & 0 \leq \bar{s} \leq 1 \\
    \max\left\{\frac{1}{||\tilde{P}_1||_2^3}, \frac{1}{||\tilde{P}_2||_2^3}\right\}, & \text{ otherwise }
    \end{cases},
\end{align*}$$ then $\frac{1}{||F_{\varepsilon}'(t)||_2^3} \leq M(\tilde{P}_1,\tilde{P}_2)$, and using [\[eq:CurvatureClosedFormula\]](#eq:CurvatureClosedFormula){reference-type="eqref" reference="eq:CurvatureClosedFormula"} we arrive at $$\begin{equation}
\label{eq:UpperBoundCurvature}
    \kappa(t) \leq \frac{1}{\varepsilon}||\varphi||_{\infty}||\tilde{P}_1\wedge\tilde{P}_2||_2M(\tilde{P}_1,\tilde{P}_2), \quad \forall t \in \mathbb R.
\end{equation}$$ That is, we have found an upper bound on the curvature for two segments that is independent of $t$. Figures [6](#fig:FirstUpperBoundCurvature){reference-type="ref" reference="fig:FirstUpperBoundCurvature"} and [7](#fig:SecondUpperBoundCurvature){reference-type="ref" reference="fig:SecondUpperBoundCurvature"} illustrate this upper bound for two different curves. Note that when the segments have similar lengths, the upper bound equals the maximum curvature---making it the tightest possible bound. However, when one segment is significantly longer than the other, the zone of maximum curvature shifts from $t = 1$ due to the mollification process. In any case, we can confidently assert that this upper bound is a good approximation of the maximum curvature, and in many cases optimal.

![Left plot represents of a three-point-two-segment function and its mollification. Right plot represents the curvature of the function and its upper bound $U_{\kappa}$ which is the right hand side of [\[eq:UpperBoundCurvature\]](#eq:UpperBoundCurvature){reference-type="eqref" reference="eq:UpperBoundCurvature"}. In this case the zone of maximum curvature corresponds to a point really close (or equal) to $t= 1$. We have used the mollifier presented in Example [1](#example:OurMollifier){reference-type="ref" reference="example:OurMollifier"}.](Images/FirstBoundOnCurvature.eps){#fig:FirstUpperBoundCurvature width="\\linewidth"}

![Left plot represents of a three-point-two-segment function and its mollification. Right plot represents the curvature of the function and its upper bound $U_{\kappa}$ which is the right hand side of [\[eq:UpperBoundCurvature\]](#eq:UpperBoundCurvature){reference-type="eqref" reference="eq:UpperBoundCurvature"}. In this case the zone of maximum curvature does not correspond to the join of the two segments. We have used the mollifier presented in Example [1](#example:OurMollifier){reference-type="ref" reference="example:OurMollifier"}.](Images/SecondBoundOnCurvature.eps){#fig:SecondUpperBoundCurvature width="\\linewidth"}

## The general case

We are going to present how, the natural generalization of the previous computations to a $p >2$ segments curve, gives, in general, a worse result than considering the curvature of each pair of segments locally, and then choosing the most restrictive $\varepsilon_{max} > 0$ so that all curvatures are constraint under this $\varepsilon_{max} >
0$. Nevertheless, due to the cumbersome and rudimentary computations, we just present the result. The natural lower bound we arrive to the upper bound of the function $\kappa$ for the $p$ segments curve can be found to be $$\begin{align*}
    \kappa \leq
    \frac{2}{\varepsilon}\frac{||\varphi||_{\infty}}{||\mathop{\mathrm{proj}}_{\mathop{\mathrm{co}}(S)}(0)||_2^3}\sum_{j=1}^{p}\sum_{i=j+1}^{p+1}&||\tilde{P}_i \wedge \tilde{P}_j||_2, \\ &\text{ as long as}
    \quad 0 \notin \mathop{\mathrm{co}}(S).
\end{align*}$$ where $S := \{\tilde{P}_i\}_{i=1}^{p}$, $\tilde{P}_i := P_i-P_{i-1}$, $i \in \{1,\dots,p+1\}$ and $\mathop{\mathrm{proj}}_{\mathop{\mathrm{co}}(S)}(0)$ is the unique element $s \in \mathbb R^n$ such that $d(0,S) = ||s||_2$, that is, the projection of $0$ onto $\mathop{\mathrm{co}}(S)$. Nevertheless, from this equation one can see that if several points are collinear, then $0 \in \mathop{\mathrm{co}}(S)$, increasing the upper bound, which is contradictory to the fact that the curvature shall decrease. Thus, we conclude that, the natural generalization of the three point two segment approach cannot be used for the $p+1$ points $p$ segments approach.

We propose the following methodology. Suppose we have $p \in \mathbb N$ segments with $p \geq 2$. Using [\[eq:UpperBoundCurvature\]](#eq:UpperBoundCurvature){reference-type="eqref" reference="eq:UpperBoundCurvature"} and given a maximum curvature $\kappa_{\max} > 0$, we can compute for each pair of consecutive segments its respective[^2] $\varepsilon_{i} > 0$ such that, under the three-point-two-segment approximation, their curvatures are upper bounded. If $\varepsilon_{i} < \frac{1}{2}$ for all $i$, then [\[eq:UpperBoundCurvature\]](#eq:UpperBoundCurvature){reference-type="eqref" reference="eq:UpperBoundCurvature"} is exact, because only the two segments used for computing $\varepsilon_i$ contribute to the mollification at the junction point. In this case, take $\varepsilon= \max_{i}\varepsilon_i$, which is valid because the only dependence on $\varepsilon_i$ in the right-hand side of [\[eq:UpperBoundCurvature\]](#eq:UpperBoundCurvature){reference-type="eqref" reference="eq:UpperBoundCurvature"} is through $\frac{1}{\varepsilon_i}$; hence, $\varepsilon$ satisfies the bound for each pair of segments. If $\varepsilon_{i} > \frac{1}{2}$ for some $i$, then [\[eq:UpperBoundCurvature\]](#eq:UpperBoundCurvature){reference-type="eqref" reference="eq:UpperBoundCurvature"} becomes an approximation. In this case, one can either accept an admissible error or use $\varepsilon= \max_{i}\varepsilon_i$ as an initial condition for an optimization algorithm that seeks the minimum $\varepsilon> 0$ that upper bounds the curvature. In either case, [\[eq:UpperBoundCurvature\]](#eq:UpperBoundCurvature){reference-type="eqref" reference="eq:UpperBoundCurvature"} is a powerful, computationally inexpensive tool that can be used to either compute an exact upper bound for the complete trajectory or reduce computation time in an optimization algorithm.

# Numerical validations and real experiments {#sec: exp}

To demonstrate the effectiveness of our path generation approach, we first show a comparison between the path generated by different spline methods and the one by mollification. We also present both numerical and experimental results for path following of a mollified path by a unicycle vehicle. Specifically, we employ the Singularity-Free Guiding Vector Fields (SF-GVF) path following algorithm [@WeijiaGVF; @weijiaarticlegvf]. In brief, SF-GVF takes a parametric path $f\in C^2(\mathbb R,\mathbb R^n)$ as input and constructs a vector field $\chi \in C^2(\mathbb R^n,\mathbb R^n)$ whose flow traces the mollified path.

## Comparison with traditional interpolation methods

We recall that mollification can generate paths from more general inputs than those for which interpolation is possible, such as the input that considers only $x\in\mathbb{Q}$ in Remark [4](#rem: Q){reference-type="ref" reference="rem: Q"}. Nonetheless, to compare traditional interpolation methods with our path generation via mollification, consider a collection of points in $\mathbb{R}^2$ that are linearly interpolated, and their $C^2$ cubic splines, B-splines and quintic Hermite interpolation splines, i.e, polynomial splines that are twice continuously differentiable and which are computed to specifically pass through the pre-defined collection of points. We compare the generated paths between the spline approaches and the proposed mollification in Figure [8](#fig:ComparisonWithSplines){reference-type="ref" reference="fig:ComparisonWithSplines"}.

![Comparison of different approach for path generation. The blue line represents the path generated from the linearly interpolated sequence of points shown in black. The mollifier used is the one presented in Example [1](#example:OurMollifier){reference-type="ref" reference="example:OurMollifier"} with $\varepsilon= 0.4$.](Images/ComparisonsWithSplines.eps){#fig:ComparisonWithSplines width="\\linewidth"}

As it can be seen, the mollification approach is the method that resembles the original function the most. Moreover, due to Proposition [7](#prop:EqualityInSets){reference-type="ref" reference="prop:EqualityInSets"} we know *exactly* in which intervals the original function and the mollified one coincide. Clearly, this is at the cost of not intersecting the collection of points, except the initial and ending ones. Nevertheless, note that numerically speaking, the mollification method is by far the simplest one. Indeed, for $C^2$ continuity there are several conditions that the coefficients of the spline polynomials must met, and which are extremely sensible to changes in the path. That is, a small change in the original path, i.e., a small change in a point of the collection, can generate a big change in the generated path. This is not something that happens in mollification, since by Proposition [7](#prop:EqualityInSets){reference-type="ref" reference="prop:EqualityInSets"} and the results of Section [4](#sec: res){reference-type="ref" reference="sec: res"} we know exactly in which sets the original path and its mollification coincide, where is the mollified curve enclosed, as well as the geometric properties preserved. Finally, we want to remark an important fact. The polynomials spline here presented are *at most* $C^2$ continuous at the collection of points, and its maximum curvature is not easy to compute between two segments nor the complete spline. For this purpose an optimization approach is often carried as mentioned in the introduction. In the mollified case, with just a single operation, $C^{\infty}$ continuity is obtained, and its derivatives are easy to compute thanks to Theorem [1](#thm:PropertiesOfMollifying){reference-type="ref" reference="thm:PropertiesOfMollifying"}. We have also provided, for this specific example, an analytical and simple to compute curvature upper bound in ([\[eq:UpperBoundCurvature\]](#eq:UpperBoundCurvature){reference-type="ref" reference="eq:UpperBoundCurvature"}). This implies that mollified path can be computed or changed online in low-cost platforms.

## Usage with a path following algorithm

For the path-following part, we are going to consider the so called "heart" function as our input path. Define the function $$\begin{equation*}
        t\in[0,2\pi) \to r(t) = 2 - 2\sin(t) + \sin(t)
        \frac{\sqrt{|\cos(t)|}}{\sin(t)+1.4}.
\end{equation*}$$ For $t \in [0,2\pi)$ let $f_1(t) = r(t)\cos(t)$ and $f_2(t) = r(t)\sin(t)$, and we call $f := (f_1,f_2)$ the "heart" path. Note that the "heart" path is continuous but not differentiable; therefore, it cannot be used for the path following algorithm SF-GVF. We solve this issue by approximating the function using mollifiers. Let $\varphi$ the mollifier presented in Example [1](#example:OurMollifier){reference-type="ref" reference="example:OurMollifier"} and let $\varepsilon_1,\varepsilon_2 > 0$ be real numbers. We then mollify the "heart" path $F$ is defined as follows $$\begin{equation*}
    F = (F_1, F_2) := (f_1 * \varphi_{\varepsilon_1},
    f_2*\varphi_{\varepsilon_2}).
\end{equation*}$$

![Representation of the numerical simulation. In both pictures the original path $f$, is shown as a blue dotted line, while as a red dotted line the mollified trajectory $F$ for $\varepsilon_1=\varepsilon_2=0.4$ in the left picture, and for $\varepsilon_1 = 0.2$ and $\varepsilon_2 = 0.8$ in the right picture. The black solid line represents the (now smooth) flow generated by the guiding vector field according to [@weijiaarticlegvf] starting from an arbitrary initial condition (IC).](Images/HeartFunctionSimulations.eps){#fig:GVFHeartMolliComplete width="\\linewidth"}

A numerical simulation of the vehicle under SF-GVF using $\varepsilon_1 = \varepsilon_2 = 0.4$ for the "heart" path is shown in the left plot of Figure [9](#fig:GVFHeartMolliComplete){reference-type="ref" reference="fig:GVFHeartMolliComplete"}. The vehicle's trajectory indicates convergence to the desired mollified path. Moreover, as $\varepsilon\to 0$, the trajectory approaches the original path more closely. Note that the mollified path lies inside the original path, as predicted by Theorem [6](#thm:ConvexHull){reference-type="ref" reference="thm:ConvexHull"}. In practical terms, this means that the "heart" function can now be used with SF-GVF, extending the applicability of this path following algorithm. Clearly, to improve convergence to the original path, we can reduce both $\varepsilon_1$ and $\varepsilon_2$, since by Theorem [1](#thm:PropertiesOfMollifying){reference-type="ref" reference="thm:PropertiesOfMollifying"} we have uniform convergence on compact sets as $\varepsilon_1,\varepsilon_2 \to 0$. However, to demonstrate the flexibility of the approach, we also consider the case $\varepsilon_1 = 0.2$ and $\varepsilon_2 = 0.8$, whose simulation is presented in the right plot of Figure [9](#fig:GVFHeartMolliComplete){reference-type="ref" reference="fig:GVFHeartMolliComplete"}. Note that in the first component, the mollified curve is better adjusted to the original curve, while in the second component, the opposite occurs. This results from $\varepsilon_2$ being four times larger than $\varepsilon_1$. Indeed, the values of $\varepsilon_1$ and $\varepsilon_2$ can be constrained by the vehicle's dynamics. This is a key advantage of the method: by simply adjusting these parameters, we can ensure that the vehicle follows the curve within its dynamic limits, thereby avoiding issues related to reconverging to the path. Moreover, numerical computations show that the length of the original path with respect to the $\ell_1$ norm is (in arbitrary units) $25.58$, while the mollified curve has length $23.16$ in the left case and $21.74$ in the right case of Figure [9](#fig:GVFHeartMolliComplete){reference-type="ref" reference="fig:GVFHeartMolliComplete"}, as predicted by Theorem [8](#thm:Length){reference-type="ref" reference="thm:Length"}. The same conclusions from Theorem [8](#thm:Length){reference-type="ref" reference="thm:Length"} can be verified with respect to any other arbitrary $\ell_p$ norm.

![Representation of the three dimensional numerical simulation. The original path $f$ is represented as a solid blue line, while the mollified trajectory $F = (F_k)_{k=1}^3 = (f_k *
    \varphi_{\varepsilon_k})_{k=1}^3$ is shown as a dashed red line, with $\varphi$ as in example [1](#example:OurMollifier){reference-type="ref" reference="example:OurMollifier"} and $\varepsilon_k = 1$ for $k \in \{1,2,3\}$. The black solid line represents the (now smooth) flow generated by the guiding vector field according to [@weijiaarticlegvf] starting from an arbitrary initial condition (IC).](Images/3DMollification_v2.pdf){#fig:3DMollification width="\\linewidth"}

## Three dimensional path mollification

Finally, for completeness, a numerical simulation of a 3D mollified path is presented in Figure [10](#fig:3DMollification){reference-type="ref" reference="fig:3DMollification"}. The notation used is identical to that in the previous numerical simulations. The original path $f$ is constructed via linear interpolation between a sequence of vertices/waypoints of a three-dimensional cube. As can be seen, $f$ is non-differentiable at these vertices. In contrast, the mollified function $F$ provides a smooth approximation that can be effectively employed in SF-GVF, as illustrated in Figure [10](#fig:3DMollification){reference-type="ref" reference="fig:3DMollification"}. Indeed, the flow of the guiding vector field converges to the mollified trajectory. Moreover, Theorem [8](#thm:Length){reference-type="ref" reference="thm:Length"} can also be validated numerically. In this case, the length of the original path in the $\ell_2$ norm is (in arbitrary units) $7.38$, while the length of the mollified path is $5.48$. An important feature of this approach is its scalability: any trajectory of the form $g : \mathbb R\to \mathbb R^n$ can be mollified component-wise, producing a sufficiently smooth curve that can be further adapted to satisfy a variety of constraints.

## Experimental results

Before presenting the experimental results, we introduce the software and hardware platforms used in the experiments. We also provide the necessary links to the developed software so that any interested reader can replicate these experiments.

### Experimental and Software Platform

Our experimental platform, shown in Figure [11](#fig:Rover-Hardware){reference-type="ref" reference="fig:Rover-Hardware"}, is a rover modeled as a unicycle, built around a Matek F765-Wing autopilot with an STM32 microcontroller, integrated IMUs, and support for GNSS, compass, and radio receivers---specifically a Matek M10Q-5883, a Futaba 7008SB receiver, and a Zigbee Xbee telemetry radio. The entire system runs on the open-source Paparazzi UAV framework [@paparazzo], which handles autonomous operation, telemetry, and real-time communication with the Ground Control Station (GCS). Through the GCS, the user can issue high-level commands and adjust waypoints on the fly, while the onboard microcontroller recomputes the mollified path in real time whenever a point or parameter is modified, as illustrated in Figure [12](#fig:GCSScreenShot){reference-type="ref" reference="fig:GCSScreenShot"}.

![Rover vehicle and hardware used during the experiments.](GonzlezCalvin2025Efficient_figs/hardware_2.jpg){#fig:Rover-Hardware width="\\linewidth"}

![Capture of an experiment using Paparazzi GCS. The original trajectory $f$ is shown in green created by linearly interpolating the points $L_i \in \mathbb R^2$, $i \in \{0,\dots,7\}$. The yellow curve represents the mollification of the original trajectory $F=(f_1 * \varphi_{\varepsilon}, f_2 *
    \varphi_{\varepsilon})$ where $\varphi$ is as in Example [1](#example:OurMollifier){reference-type="ref" reference="example:OurMollifier"} and $\varepsilon= 0.5$. The orange line represents the trajectory described by the vehicle.](Images/PaparazziGCSScreenShotV2.png){#fig:GCSScreenShot width="\\linewidth"}

### Experimental data

We show our logs in Figure [13](#fig:Experiments){reference-type="ref" reference="fig:Experiments"}. We created a continuous but non-differentiable path by linearly interpolating points in $\mathbb R^2$ as it is done in Section [5](#sec: curvature){reference-type="ref" reference="sec: curvature"}. As noted above, any Paparazzi user can create such trajectories by simply moving points in the ground control station before or during the experiment in real time. The experiment uses a curve similar to that in Figure [12](#fig:GCSScreenShot){reference-type="ref" reference="fig:GCSScreenShot"}.

![Real experiment of path following of a mollified non-differentiable path with a rover vehicle. The original non-differentiable path $f$ is in black, the mollified family trajectories $\{F_{\varepsilon_i}\}_{i=1}^{6}$ to be followed at each *stage* are in solid red, its initial point $r_0$ is denoted as the blue cross, the position of the vehicle for its corresponding $\varepsilon_i>0$ at times $t \in [t_{i-1},t_{i}]$ in a thick solid blue line. Finally, the complete trajectory of the vehicle $r(t;r_0)$ throughout all the stages is the dashed blue line.](Images/ExperimentPlotsMollifierChanging_v2.eps){#fig:Experiments width="1\\columnwidth"}

The experimental objective is as follows: Given a desired non-differentiable path $f$, mollify it with parameter $\varepsilon> 0$ to obtain $F_{\varepsilon} = (f * \varphi_{\varepsilon})$, where $\varepsilon$ is a function of vehicle speed limited by maximum allowed curvature. To demonstrate potential applications, we use a linear relationship between maximum allowed curvature and speed. For speed $v > 0$, with $R_{min}$, $R_{max}$, and $v_{max}$ denoting minimum radius, maximum radius, and maximum speed respectively, the allowed radius of curvature is $R(v) := R_{min} + \frac{v}{v_{max}}(R_{max}-R_{min})$. Note this is merely illustrative; curvature and speed need not be linearly related in practice. We are going to consider a curve consisting on seven two dimensional points which are linearly interpolated, as shown in Figure [13](#fig:Experiments){reference-type="ref" reference="fig:Experiments"}.

The adaptation of the curve to vehicle dynamics operates as follows: at initial time $t_0$, we set $\varepsilon_1 = 0.5$ to generate the first mollified curve $F_{\varepsilon_1}=f * \varphi_{\varepsilon_1}$, where $f$ is the original curve and $\varphi$ is as in Example [1](#example:OurMollifier){reference-type="ref" reference="example:OurMollifier"}. As the vehicle advances and reaches each segment midpoint at times $\{t_i\}_{i=1}^{6}$, the speed is measured and used to compute the maximum allowed curvature, from which the minimum permissible $\varepsilon_{i+1}$ is determined via [\[eq:UpperBoundCurvature\]](#eq:UpperBoundCurvature){reference-type="eqref" reference="eq:UpperBoundCurvature"}. This generates a family of six parameters $\{\varepsilon_i\}_{i=1}^{6}$ and corresponding mollified curves $\{F_{\varepsilon_i}\}_{i=1}^{6}$ that dynamically adapt to vehicle constraints. As shown in Figure [13](#fig:Experiments){reference-type="ref" reference="fig:Experiments"}, the resulting paths remain close to the original trajectory where curvature permits, e.g., segments four and five, while strongly constraining the curve when necessary, e.g., the last two segments. All theoretical guarantees hold: the mollified curves lie within the convex hull of the original path (Theorem [6](#thm:ConvexHull){reference-type="ref" reference="thm:ConvexHull"}), and parameters are sufficiently small that Propositions [2](#prop:LocalConvexity){reference-type="ref" reference="prop:LocalConvexity"} and [5](#prop:MolliAboveFConvexityLocally){reference-type="ref" reference="prop:MolliAboveFConvexityLocally"} apply. These experiments validate both the theoretical solution of Problem [1](#prob:RegularizationProblem){reference-type="ref" reference="prob:RegularizationProblem"} and the practical viability of our approach on real, affordable hardware.

# Conclusions {#sec: con}

In this work, we addressed the problem of efficient path generation to make non-suitable curves, such as linear interpolations from waypoint collections, suitable for path following and trajectory tracking algorithms via mollification. The mollification can be adjusted so that the mollified trajectory approximates the original trajectory arbitrarily closely on compact sets while being completely smooth. Additionally, properties such as convexity, concavity, monotonicity, and quasiconvexity are preserved under mollification, with local versions also preserved for sufficiently small mollification parameters.

We validated the approach through numerical simulations using Singularity-Free Guiding Vector Fields as a path following algorithm, applying mollification to the "heart" path and a 3D trajectory while examining the effects of different parameter values. Finally, experiments on rovers demonstrated the viability of the approach and the ability to tune mollified paths to match vehicle dynamics. While the original trajectory may not be physically realizable, the mollified trajectory with appropriate parameters can be successfully followed. This confirms that our results have both theoretical significance and practical value for autonomous vehicles, industrial robotics, and any engineering application requiring fast and rigorous function approximation.

::: IEEEbiography
Alfredo González-Calvin earned his Electrical Engineering degree from the Complutense University of Madrid in 2023. He earned his two Master's degrees from UNED University: one in Control and Systems Engineering in 2024 and another in Mathematics in 2025. Currently, he is pursuing a Ph.D. in Physics, focusing on path planning and mathematical applications in robotics and engineering.
:::

::: IEEEbiography
Juan Jimenez graduated in Physics from the Universidad Autónoma de Madrid (Spain) in 1986 and earned his Ph.D. in Systems Control in 1999 from the Universidad Nacional de Educación a Distancia (Spain). Since 2015, he has been an Associate Professor in the Department of Computer Architecture, Systems Engineering, and Automation at the Universidad Complutense de Madrid. His research interests include distributed control and cooperative control in multi-agent systems, with a particular focus on applications to autonomous vehicles.
:::

::: IEEEbiography
Hector Garcia de Marina (Member IEEE) received the Ph.D. degree in systems and control from the University of Groningen, The Netherlands, in 2016. He was a Postdoctoral Research Associate with the Ecole Nationale de l'viation Civile, Toulouse, France, and an Assistant Professor with the Unmanned Aerial Systems Center, University of Southern Denmark, Odense, Denmark. Since 2022, he has been a Ramón y Cajal Researcher with the Department of Computer Engineering, Automation and Robotics, and with CITIC, Universidad de Granada, Spain. He is the recipient of an ERC Starting Grant and was Associate Editor for IEEE Transactions on Robotics for four years. His current research interests include multiagent systems and the design of guidance navigation and control systems for autonomous vehicles.
:::

[^1]: Alfredo and Juan are with the Department of Computer Architecture and Automation, Faculty of Physics, Complutense University of Madrid, Madrid, Spain. Hector is with the Department of Computer Engineering, Automation, and Robotics (ICAR) & Institute of Mathematics (IMAG), University of Granada, Spain. This work is specially supported by the FPU program of the Ministry of science, innovation and universities of Spain and it is supported by iRoboCity2030-CM, Ref TEC-2024/TEC-62, financed by Comunidad Autónoma de Madrid (Spain) and by the ERC Starting Grant iSwarm 101076091 and the RYC2020-030090-I grant from the Spanish Ministry of Science. Corresponding author `alfredgo@ucm.es`.

[^2]: The index $i$ ranges from the first pair to the last pair of consecutive segments.
