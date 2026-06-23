---
citation_key: Chen2026Computing
arxiv_id: 2606.14794
arxiv_url: https://arxiv.org/abs/2606.14794
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-23T17:56:30Z
origin: ai+web
reviewed: false
---

**Keywords:** Minimal paths, curvature bounds, Hamilton-Jacob-Bellman equation, curvilinear structure tracking, path planning, hamiltonian fast marching method, curvature regularization

# Introduction {#sec_intro}

In recent years, the theoretical foundations and numerical methods for computing minimal paths in a connected domain have become the core to a wide range of scientific problems posed in applied mathematics, engineering and science [@peyre2010geodesic], due to their strong ability in accommodating mixed geometric, perceptual and physical priors. The computation of minimal paths bridges several research areas, including artificial intelligence, image understanding and PDE numerical analysis, thus exhibiting its fundamental and important role in computational sciences.

Early approaches focus on the computation of minimal paths whose weighted curve length is dependent on the local path position and tangent, which are categorized as first-order geometric features [@cohen1997global; @benmansour2011tubular; @chen2024region]. Despite successful applications in many research areas, these first-order minimal path models have difficulties in taking into account the path curvature and the associated geometric shape priors [@chen2023geodesic; @duits2018optimal; @mirebeau2018fast; @mashtakov2023time; @chen2023computing]. Recent efforts are devoted to minimizing bending energy functionals featuring different second-order curvature penalizations. Using path curvature as regularization leads to strong flexibility in embedding various geometry priors into the computation of minimal paths, and has succeeded in a variety of practical applications such as image analysis [@mashtakov2017tracking; @bekkers2015pde; @deng2019new; @liu2021color] and robotics motion planning [@kimmel1998multivalued; @mirebeau2017automatic; @kimmel2001optimal].

The connection between the minimization of a path energy, defined by an appropriate metric, and the geometric control theory paves the way for computing globally optimal paths between prescribed endpoints [@mirebeau2018fast]. The foundation of this research line is established over the framework of the first-order static HJB PDE, whose viscosity solution corresponds to the minimum of the path energy and can be numerically approximated via the seminal approach named Fast-Marching method [@sethian1996fast; @sethian1999fast] and its elegant Finslerian variants featuring asymmetry property [@mirebeau2018fast; @mirebeau2019hamiltonian; @mirebeau2014anisotropic; @mirebeau2023massively; @sethian2003ordered; @sethian2001ordered]. The classical Euler-Mumford Elastica problem, first investigated in physics to describe the deformation of an elastic thin rod, is a typical instance for computing second-order curvature-penalized minimal paths, whose bending energy involves an integral of squared path curvature. Following the pioneering approach in [@mumford1994elastica], the Euler-Mumford Elastica model has been developed as an efficient mathematical tool in the fields of computer vision and medical imaging [@chen2017global; @tai2011fast; @ben2014tangent]. In its basic formulation, the Euler-Mumford Elastica model usually favors smooth minimal paths with homogeneously slow-varying tangents, which, unfortunately, is not always suitable in the realistic applications. Indeed, in the application domain of interest, minimal paths are expected to simultaneously maintain the rigid property of curves, and to fit the centerlines of curvilinear structures featuring segments whose curvature is strong and varies quickly. For that purpose, the curvature prior Elastica model [@chen2023computing] was introduced as a generalization of the classical approach [@chen2017global; @mirebeau2018fast] to penalize a curvature drift term that measures the deviation of the path curvature from a prescribed feature map, providing an avenue to take advantage of the bending features of curvilinear structures. However, in its basic formulation, the curvature drift term in essence imposes a soft constraint on the associated minimal paths, whose path curvature may not always agree with the prescribed values, especially when the geometric objects to process have challenging appearance. This is also the case for the variant of the Reeds-Shepp forward model [@van2024geodesic], even though the two models [@chen2023computing; @van2024geodesic] are distinct from each other in the use of curvature priors and also in the definition of bending energy functionals.

:::: {#fig_CompXRay .figure latex-placement="!htbp"}
![](Chen2026Computing_figs/fig1.png){width="\\linewidth"}

::: caption
Illustration for the advantages of the proposed curvature-bounded geodesic model comparing to state-of-the-art second-order curvature-penalized models. (**a**) The initialization information over an x-ray heart image, which contains a self-crossing pattern. The blue and red dots represent the source point and the end point with arrows indicating the path tangents at those points. (**b**)-(**d**) The lines indicate the physical projection curves of the minimal paths which are respectively derived from the classical Euler-Mumford Elastica model, the Dubins car model and the introduced curvature-constrained Elastica model. The varying color of the lines represent the euclidean curve length of those paths.
:::
::::

The Dubins model [@mirebeau2018fast] is designed for computing minimal paths with strong curvature penalization, where the magnitude of path curvature is constrained [@boissonnat1994shortest]. However, unlike the Euler-Mumford Elastica model, a key limitation of the Dubins model is its lack of smoothness property in the yielded minimal paths---an essential property in many practical applications. In this article, we propose a variant of the classical Euler-Mumford Elastica model [@chen2017global], referred to as the *curvature-bounded model*, which is able impose *arbitrary* lower and upper bounds to directly control the path curvature of the planar component of the computed minimal paths. For that purpose, we define a new Hamiltonian, we study the corresponding control sets, which implicitly embed the limitation of path curvature, and we design numerical schemes for solving the corresponding HJB PDE using the geometric optimization tool of Voronoi's first reduction [@mirebeau2018fast; @mirebeau2019riemannian]. This allows us to interpret our curvature-bounded model as a minimum arrival time problem or a minimal action problem by means of the optimal control theory, and also yields an efficient way to find globally optimal curves of bounded curvature between two endpoints with given tangent directions at both points. In particular, the model we propose here provides a hard constraint to limit the path curvature, thus serving as an alternative way to efficiently implement the curvature prior enhancement for finding satisfactory minimal paths. This gives our model a clear advantage over existing minimal path methods, particularly in challenging scenarios, highlighting that the introduction of the curvature-bounded model is both significant and nontrivial. In Fig. [1](#fig_CompXRay){reference-type="ref" reference="fig_CompXRay"}, we illustrate the qualitative comparison results of the Euler-Mumford Elastica model [@chen2017global], the Dubins car model [@mirebeau2018fast] and the introduced bounded elastica model. Those numerical experiments demonstrated in Fig. [1](#fig_CompXRay){reference-type="ref" reference="fig_CompXRay"} are conducted over an X-ray heart image. The objective is to compute a minimal path such that its physical projection curve can accurately depict the centerline of a blood vessel featuring a self-crossing structure. The initialization for the tested models is illustrated in Fig. [1](#fig_CompXRay){reference-type="ref" reference="fig_CompXRay"}a, where the blue and red dots respectively denote the source point and the target point with arrows pointing the tangent directions at those points. From this experiment, one can see that both of the Euler-Mumford elastica model and the Dubins car model, whose minimal paths are respectively shown in Figs. [1](#fig_CompXRay){reference-type="ref" reference="fig_CompXRay"}b and [1](#fig_CompXRay){reference-type="ref" reference="fig_CompXRay"}c, fail to track the centerlines of the self-crossing structures. In contrast, the introduced bounded Elastica model blends the benefits of the smoothness property and the enhancement from the arbitrary curvature bounds, thus is able to successfully extract the self-crossing structure, as illustrated in Fig. [1](#fig_CompXRay){reference-type="ref" reference="fig_CompXRay"}d.

The remainder of this manuscript is organized as follows. We first summarize the introduced bounded Elastica model and the mathematical tools used. Following that we present the main contribution of this work:

- The theoretical results involving the expression of the Hamiltonian of the bounded Elastica model and the corresponding control sets.

- The practical applications involving the curvilinear structure tracking and robot motion planning. Eventually, the numerical scheme for tracking accurate minimal paths from a Cartesian grid is presented in the Method section.

# Results {#sec_res}

:::: {#fig_ControlsJMM .figure latex-placement="!htbp"}
![](Chen2026Computing_figs/fig2.png){width="80%"}

::: caption
(**a**) Tissot indicatrix of the proposed bounded Elastica model, i.e. illustration of the control set $\mathcal B(\mathbf p)$ of admissible velocities at a collection of points $\mathbf p= (x,y,\theta) \in \mathbb M:= \Omega \times \mathbb S^1$ of the domain. (**b**) Comparison of the control sets of the proposed bounded Elastica model, with the Euler-Mumford Elastica (with adjusted parameters) and Dubins models. (**c**) Comparison of the curvature penalties. The proposed bounded Elastica model has a smooth and convex curvature penalty, with vertical asymptotes as $\kappa \to 1^-$ and $\kappa \to -1^+$. The curvature penalty of the Euler-Mumford Elastica model has the form $a+b\kappa^2$, for user-defined parameters $a,b>0$. The curvature penalty of the Dubins model is constant if $|\kappa|<1$, and $+\infty$ otherwise.
:::
::::

## Model Overview {#model-overview .unnumbered}

The bounded Elastica model introduced in this paper is designed in such way that the optimal curves are smooth and that their curvature is constrained within arbitrary upper and lower bounds. Similarly to other state-of-the-art curvature-penalized minimal path models [@chen2017global; @mirebeau2018fast; @duits2018optimal; @chen2023computing] based on the HJB PDE framework, the state space underlying the curvature-bounded model is a three-dimensional orientation lifted space, defined as the product $\mathbb M:=\Omega\times\mathbb S^1$ of a two dimensional open-bounded *physical* domain $\Omega\subset\mathbb R^2$, with the *angular* domain $\mathbb S^1:=\mathbb R/2\pi\mathbb Z$ (equivalently, $\mathbb S^1 = [0,2\pi[$ with periodic boundary conditions). An arbitrary point $\mathbf p=(\mathfrak p,\theta)\in\mathbb M$ thus involves two components: $\mathfrak p\in\Omega$ the physical position, and $\theta\in\mathbb S^1$ the angular coordinate. Consider a parametrized curve $\gamma:[0,1]\to\Omega$ in the physical domain $\Omega$, which is twice continuously differentiable and *regular* in the sense that its velocity is non-vanishing. This curve can be lifted to $\wp=(\gamma,\eta):[0,1]\to\mathbb M$ where the function $\eta:[0,1]\to\mathbb S^1$ characterizes the turning angles of the *physical projection curve* $\gamma$, namely $\gamma^\prime(t)=\|\gamma^\prime(t)\|\mathbf{n}(\eta(t)),\,\forall t\in[0,1]$, where $\mathbf{n}(\theta)=(\cos\theta,\sin\theta)$ is the unit vector associated to an angle $\theta\in\mathbb S^1$. The curvature $\kappa:[0,1]\to\mathbb R$ of the physical projection curve $\gamma$ equals the ratio $$\begin{equation*}
%\label{eq:kappa}
\kappa=\eta^\prime/\|\gamma^\prime\|.
\end{equation*}$$ The curvature $\kappa$ of the physical projection curve $\gamma$ is thus expressed in terms of the tangent vector $\wp^\prime = (\gamma^\prime,\eta^\prime)$ to the *orientation-lifted path*.

The proposed curvature-bounded geodesic model can be formulated as a minimum arrival time optimal control problem in the configuration space $\mathbb M$, in which the velocity of an orientation-lifted path is constrained within suitable control sets $\mathcal B$. Each control set $\mathcal B(\mathbf p)$ at a point $\mathbf p\in\mathbb M$ is a *convex* and *compact* subset of the tangent space $\mathbb E:=\mathbb R^2\times\mathbb R$ containing the origin $\mathbf{0}=(0,0,0)$, and depending continuously on $\mathbf p$ w.r.t. the Haussdorff distance; the control sets corresponding to our specific model are illustrated in Fig. [2](#fig_ControlsJMM){reference-type="ref" reference="fig_ControlsJMM"} and will be explicitly constructed in the next section. The minimum arrival time problem from a source point $\mathbf s\in\mathbb M$ to a target point $\mathbf p\in\mathbb M$ is defined as $$\begin{align}
\label{eq_MinimalTime}
\mathcal T_\mathcal B(\mathbf s,\mathbf p):=\inf\Bigl\{T>0\,|\,&\exists\wp\in\mathop{\mathrm{Lip}}([0,1],\mathbb M),\nonumber\\
&\wp(0)=\mathbf s,\,\wp(1)=\mathbf p,\nonumber\\
&T^{-1}\wp^\prime(t)\in\mathcal B(\wp(t)),\,\forall t\in[0,1]\Bigr\}
\end{align}$$ where $\mathop{\mathrm{Lip}}([0,1],\mathbb M)$ denotes the collection of all Lipschitz continuous curves $\wp:[0,1]\to\mathbb M$. In [\[eq_MinimalTime\]](#eq_MinimalTime){reference-type="ref+label" reference="eq_MinimalTime"}, the condition $T^{-1}\wp^\prime\in\mathcal B(\wp)$ defines the $T\mathcal B$-admissibility of a curve $\wp\in\mathop{\mathrm{Lip}}([0,1],\mathbb M)$. If the infimum $T:=\mathcal T_{\mathcal B}(\mathbf s,\mathbf p)$ is finite, then it is attained, i.e. there exists a $T\mathcal B$-admissible path $\mathcal G_{\mathbf s,\mathbf p}$ from $\mathbf s$ to $\mathbf p$ referred to as an optimal curve or minimal path, see the literature [@bardi1997Optimal] or [@chen2017global Appendix B] on optimal control.

The tangents $T^{-1} \mathcal G_{\mathbf s,\mathbf p}^\prime\in\mathcal B(\mathcal G_{\mathbf s,\mathbf p})$ to the minimal path $\mathcal G_{\mathbf s,\mathbf p}=(\tilde{\gamma}_{\mathbf s,\mathbf p},\tilde{\eta}_{\mathbf s,\mathbf p})$ contain all the information for computing the path curvature $\tilde{\kappa}$ of its physical projection curve $\tilde{\gamma}_{\mathbf s,\mathbf p}$. By designing proper control sets $\mathcal B$, in the following, we are able to constrain the curvature $\tilde{\kappa}$: $$\begin{equation}
\label{eq_curvatureBounds}
\Im_{\rm min}\bigl(\tilde{\gamma}_{\mathbf s,\mathbf p}(t),\tilde{\eta}_{\mathbf s,\mathbf p}(t)\bigr)\leq \tilde{\kappa}(t)\leq \Im_{\rm max}\bigl(\tilde{\gamma}_{\mathbf s,\mathbf p}(t),\tilde{\eta}_{\mathbf s,\mathbf p}(t)\bigr)
\end{equation}$$ for any $t\in[0,1]$, where $\Im_{\rm min}$, $\Im_{\rm max}:\mathbb M\to\mathbb R$ are two user-defined scalar-valued continuous functions setting the lower and upper curvature bounds.

We discuss below some of the qualitative properties of the control sets of the proposed curvature-bounded model, anticipating on their precise mathematical definition which is given in the next section, and which involves four parameters here arbitrarily fixed to $$\begin{equation}
\label{eq_default_params}
    \mathcal C=\xi=1 
    \quad \text{and} \quad 
    \psi_{\max} = -\psi_{\min} = \pi/4.
\end{equation}$$ The *Tissot indicatrix* of the curvature-bounded model, illustrated in [2](#fig_ControlsJMM){reference-type="ref+label" reference="fig_ControlsJMM"}a, shows the control sets $\mathcal B(x,y,\theta)$ attached to a collection of regularly spaced points, i.e. the physical position $\mathfrak p= (x,y)\in \Omega$ and the angular coordinate $\theta\in \mathbb S^1$ lie on a grid. Each of these control sets is a flat convex shape contained in a two-dimensional half plane $\mathbb E_\theta$ of the tangent space $\mathbb E:= \mathbb R^2 \times \mathbb R$: $$\begin{equation}
\label{eq_HalfPlane}
    \mathbb E_\theta := \{ (\dot \nu \mathbf{n}(\theta), \dot \theta) \mid \dot \nu \geq 0,\ \dot \theta \in \mathbb R\},
\end{equation}$$ where we recall that $\mathbf{n}(\theta) := (\cos\theta,\sin\theta)$. Our minimal path model thus describes a non-holonomic vehicle whose physical velocity $\dot{\nu}\mathbf{n}(\theta)$ is always positively collinear with the heading direction $\mathbf{n}(\theta)$, and is thus never directed backwards or sideways. Since $\mathcal B(\mathbf p) \subset \mathbb E_\theta$, there is no loss of information in considering the following sliced control sets $$\begin{equation}
\label{eq_BECS2D}
\tilde\mathcal B(\mathbf p)=\left\{(\dot\nu,\dot\theta)\in\mathbb R^2~|~\dot\nu\geq0,(\dot\nu\mathbf{n}(\theta),\dot\theta)\in\mathcal B(\mathbf p)\right\},
\end{equation}$$ as shown in [2](#fig_ControlsJMM){reference-type="ref+label" reference="fig_ControlsJMM"}b, which is independent of $\mathbf p$ under the assumption in [\[eq_default_params\]](#eq_default_params){reference-type="ref+label" reference="eq_default_params"}. Similarly to the Euler-Mumford Elastica model, the control sets of the proposed curvature-bounded model have a smooth (except at the origin) and strictly convex boundary, leading to smooth minimal paths; in contrast, the triangle-shaped control set of the Dubins model leads to piecewise smooth paths, which are known to be concatenations of straight segments and circular arcs. Similarly to the Dubins model, the boundary of the control sets of the curvature-bounded model has an angle at the origin, leading to upper and lower bounds on the admissible path curvature, see [1](#prop_BoundedCurvature){reference-type="ref+label" reference="prop_BoundedCurvature"} for a detailed argument; in contrast, the Euler-Mumford Elastica model admits a vertical tangent at the origin, indicating that the curvature is not bounded a priori.

Minimal paths for the proposed curvature-bounded model, the Euler-Mumford Elastica model and the Dubins model, can be investigated in the curvature penalization framework established in [@mirebeau2018fast]. A path $\wp$ from $\mathbf p= (\mathfrak p,\theta)$ to $\mathbf q= (\mathfrak q,\phi)$ is optimal iff the physical projection curve $\gamma : [0,L] \to \mathbb R^2$, parametrized at unit Euclidean speed and whose curvature is denoted $\kappa : [0,L] \to \mathbb R$, minimizes the second-order energy functional $$\begin{equation*}
\int_0^L  \mathfrak{C}(\kappa(l)) dl,\ \text{subject to}\
\begin{cases}
\gamma(0) = \mathbf p,\ \gamma^\prime(0) = \mathbf{n}(\theta),\\
\gamma(L)=\mathbf q,\ \gamma^\prime(L)=\mathbf{n}(\phi).
\end{cases}
\end{equation*}$$ The curvature dependent cost function $\mathfrak{C}: \mathbb R\to ]0,\infty]$ is related to the control sets via the equality $$\begin{equation}
\label{eq_CurvCost}
\mathfrak{C}(\dot \theta/\dot \nu) = 1/\dot\nu \quad \text{for each~} (\dot \nu, \dot \theta) \in \partial \tilde \mathcal B(\mathbf p),
\end{equation}$$ with $\dot\nu>0$. The curvature cost function $\mathfrak{C}$ associated to the Euler-Mumford Elastica model is a parabola, whereas for the Dubins model it equals $1$ on the interval $[-1,1]$ and $+\infty$ elsewhere. Unfortunately, the curvature cost function $\mathfrak{C}$ associated with the curvature-bounded model does not have a closed form algebraic expression to our knowledge, but we can nevertheless compute it numerically using [\[eq_CurvCost\]](#eq_CurvCost){reference-type="ref+label" reference="eq_CurvCost"}, see [2](#fig_ControlsJMM){reference-type="ref+label" reference="fig_ControlsJMM"}c. Similarly to the Euler-Mumford Elastica model, it is smooth and approximately parabolic close to the origin; similarly to the Dubins model it equals $+\infty$ outside the interval $[-1,1]$.

Finally, let us mention that a much wider range of control set shapes and minimal path behaviors can be achieved by lifting the constraint of [\[eq_curvatureBounds\]](#eq_curvatureBounds){reference-type="ref+label" reference="eq_curvatureBounds"}, and letting the parameters $\mathcal C$, $\xi$, $\psi_{\max}$, $\psi_{\min}$ depend on the current point $\mathbf p$. One may for instance favor paths in going through some regions by decreasing the cost $\mathcal C$ there, one may impose specific upper or lower curvature bounds via $\psi_{\max}$ and $\psi_{\min}$, and one may alter the curvature cost function through $\xi$.

## Hamiltonian and control sets of the proposed curvature-bounded model {#hamiltonian-and-control-sets-of-the-proposed-curvature-bounded-model .unnumbered}

The control sets $\mathcal B$ can be equivalently described in terms of a Hamiltonian $\mathcal H:\mathbb M\times\mathbb E^*\to[0,\infty[$, where the co-tangent space $\mathbb E^*$ is the dual to the tangent vector space $\mathbb E= \mathbb R^2 \times \mathbb R$. On the one hand, one can define $$\begin{equation}
\label{eq_HamAsSup}
    \sqrt{2\mathcal H(\mathbf p,\hat{\mathbf{p}})} = \max\big\{ \langle\hat \mathbf p,\dot{\mathbf{p}}\rangle \mid \dot \mathbf p\in \mathcal B(\mathbf p)\big\},
\end{equation}$$ where $\langle\dot{\mathbf{p}},\hat{\mathbf{p}}\rangle$ denotes the standard Euclidean scalar product of $\dot{\mathbf{p}}$ and $\hat{\mathbf{p}}$. The Hamiltonian $\mathcal H(\mathbf p,\hat{\mathbf{p}})$ is a continuous function of point $\mathbf p\in \mathbb M$ and co-vector $\hat \mathbf p\in \mathbb E^*$, convex and positively two-homogeneous w.r.t. the second variable $\hat \mathbf p$. Conversely, the control sets can be recovered as follows from a Hamiltonian obeying those properties: $$\begin{equation}
\label{eq_BEControlSet}
\mathcal B(\mathbf p):=\overline{\mathrm{co}}\left\{\frac{\partial}{\partial\hat{\mathbf{p}}}\sqrt{2\mathcal H(\mathbf p,\hat{\mathbf{p}})}\in\mathbb E,\,\forall \hat{\mathbf{p}}\in\mathbb E^*\backslash\{\mathbf{0}\} \right\},
\end{equation}$$ where $\overline{\mathrm{co}}(A)$ denotes the closed convex envelope of a set $A \subset \mathbb E$, and the points $\hat \mathbf p$ where $\sqrt{2 \mathcal H(\mathbf p,\cdot)}$ is not differentiable are implicitly omitted from Eq. [\[eq_BEControlSet\]](#eq_BEControlSet){reference-type="ref+label" reference="eq_BEControlSet"}. Therefore, instead of giving the explicit expression of the control sets $\mathcal B$, we alternatively focus on the design of a Hamiltonian $\mathcal H$ that enforces the desired curvature constraints, whose construction constitutes the main theoretical originality of this work.

Let $\mathcal C: \mathbb M\to ]0,\infty[$ be a positive cost function characterizing the geometric features of the target curvilinear structures and let us define by $\Re(\theta,\psi)\in\mathbb E$ a control vector with respect to a pair of angles $(\theta,\,\psi)$, reading as $$\begin{equation}
\label{eq_ControlVector}
\Re(\theta,\psi)=\left(\cos(\psi)\mathbf{n}(\theta),\xi^{-1}\sin(\psi)\right),
\end{equation}$$ where $\xi>0$ is a constant. For any point $\mathbf p=(\mathfrak p,\theta)\in\mathbb M$ and any co-vector $\hat{\mathbf{p}}=(\hat{\mathfrak{p}},\hat\theta)\in\mathbb E^*$, we define the Hamiltonian $\mathcal H$ of the proposed curvature-bounded model as follows $$\begin{equation}
\label{eq_BEHamiltonian}
\mathcal H(\mathbf p,\hat{\mathbf{p}}):=\frac{3}{8}\mathcal C(\mathbf p)^{-2}\,\int_{\psi_{\rm min}(\mathbf p)}^{\psi_{\rm max}(\mathbf p)}\,\langle\hat{\mathbf{p}}, \Re(\theta,\psi)\rangle_+^2\,w_\mathbf p(\psi)\,d\psi
\end{equation}$$ where $\langle\hat{\mathbf{p}},\dot{\mathbf{p}}\rangle_+:=\max\{0,\langle\hat{\mathbf{p}},\dot{\mathbf{p}}\rangle\}$ is the positive part of the standard Euclidean scalar product, and $\psi_{\rm min},\,\psi_{\rm max}:\mathbb M\to[-\pi/2,\pi/2]$ are scalar-valued functions computed from the curvature bounds $\Im_{\rm min} < \Im_{\rm max}$ in such way that $$\begin{align*}
&\psi_{\rm min}(\mathbf p):=\arctan\bigl(\xi\Im_{\rm min}(\mathbf p)\bigr),\\
&\psi_{\rm max}(\mathbf p):=\arctan\bigl(\xi\Im_{\rm max}(\mathbf p)\bigr).
\end{align*}$$ In addition, the non-negative weight $w_\mathbf p(\psi)\geq 0$ in the integral is defined for each angle $\psi \in [\psi_{\min}(\mathbf p),\psi_{\max}(\mathbf p)]$ as $$\begin{equation}
\label{eq_VarFejWeights}
w_\mathbf p(\psi):=\frac{1}{\lambda_\mathbf p}\cos\left(\frac{\psi-\Psi_\mathbf p}{\lambda_\mathbf p}\right)
\end{equation}$$ where the functions $\Psi_\mathbf p$ and $\lambda_\mathbf p$ are respectively defined as $$\begin{align*}
&\Psi_\mathbf p:=\frac{1}{2}\bigl(\psi_{\rm max}(\mathbf p)+\psi_{\rm min}(\mathbf p)\bigr), \\
&\lambda_\mathbf p:=\frac{1}{\pi}\bigl(\psi_{\rm max}(\mathbf p)-\psi_{\rm min}(\mathbf p)\bigr).
\end{align*}$$ By those definitions we note that $\Psi_\mathbf p$ is the average of the values $\psi_{\rm max}(\mathbf p)$ and $\psi_{\rm min}(\mathbf p)$, and $\lambda_\mathbf p$ is a scaling factor.

The definition of the Hamiltonian in [\[eq_BEHamiltonian\]](#eq_BEHamiltonian){reference-type="ref+label" reference="eq_BEHamiltonian"} via an integral is not very common in applications [@bardi1997Optimal; @mirebeau2018fast]. Typically, one either provides an explicit algebraic expression or employs a supremum form analogous to that in [\[eq_HamAsSup\]](#eq_HamAsSup){reference-type="ref+label" reference="eq_HamAsSup"}. The integral form [\[eq_BEHamiltonian\]](#eq_BEHamiltonian){reference-type="ref+label" reference="eq_BEHamiltonian"} here is motivated by (i) its simple and accurate numerical implementation using Fejer quadrature as described in the Methods section, and (ii) its connection to the Euler-Mumford Elastica model (see [\[eq_ElasticaHam\]](#eq_ElasticaHam){reference-type="ref+label" reference="eq_ElasticaHam"} below).

:::: {#fig_ControlSets_Xi .figure latex-placement="!htbp"}
![](Chen2026Computing_figs/fig3.png){width="90%"}

::: caption
Illustration for the plots of the boundaries $\partial\tilde{\mathcal B}(\mathbf p)$ of the proposed curvature-bounded model and the corresponding minimal paths. (**a**)-(**c**): visualization for the boundaries $\partial\tilde{\mathcal B}(\mathbf p)$ with respect to different values of the parameter $\xi$. The values of the curvature bounds $\Im_{\rm min}$ and $\Im_{\rm max}$ are shown at the top of each column. The red dots indicate the origin $(0,0)$ of the set $\tilde{\mathcal B}(\mathbf p)$. (**d**): the lines represent the physical projections of orientation-lifted minimal paths with bounded curvature. The blue and red dots are respectively the source point and endpoint with arrows indicating the tangent directions assigned to the these points.
:::
::::

Differentiating the Hamiltonian expressed in [\[eq_BEHamiltonian\]](#eq_BEHamiltonian){reference-type="ref+label" reference="eq_BEHamiltonian"} w.r.t. the co-vector $\hat \mathbf p\in \mathbb E^*$, we obtain at any point $\mathbf p= (\mathfrak p,\theta) \in \mathbb M$ $$\begin{equation*}
    \frac{\partial\mathcal H}{\partial \hat \mathbf p}(\mathbf p,\hat \mathbf p) = \frac 3 {4\mathcal C(\mathbf p)^2} 
    \int_{\psi_{\rm min}(\mathbf p)}^{\psi_{\rm max}(\mathbf p)}\langle\hat{\mathbf{p}}, \Re(\theta,\psi)\rangle_+ \Re(\theta,\psi) w_\mathbf p(\psi)d\psi.
\end{equation*}$$ By construction, the control vectors $\Re(\theta,\psi)$ defined in [\[eq_ControlVector\]](#eq_ControlVector){reference-type="ref+label" reference="eq_ControlVector"} lie in the half plane $\mathbb E_\theta$ defined by [\[eq_HalfPlane\]](#eq_HalfPlane){reference-type="ref+label" reference="eq_HalfPlane"}. Therefore $\frac{\partial\mathcal H}{\partial \hat \mathbf p}(\mathbf p,\hat \mathbf p) \in \mathbb E_\theta$, and thus $\mathcal B(\mathbf p) \subset \mathbb E_\theta$ in view of [\[eq_BEControlSet\]](#eq_BEControlSet){reference-type="ref+label" reference="eq_BEControlSet"}, which fits with the discussion of the previous section and makes [\[eq_BECS2D\]](#eq_BECS2D){reference-type="ref+label" reference="eq_BECS2D"} well defined. This observation holds for arbitrary parameters $\mathcal C(\mathbf p)>0$, $\xi(\mathbf p)>0$, $-\pi/2 < \psi_{\min}(\mathbf p) < \psi_{\max}(\mathbf p)<\pi/2$.

Eventually, we present the following result on the path curvature of any $T\mathcal B$-admissible curve.

::: {#prop_BoundedCurvature .proposition}
**Proposition 1**. *\[Boundedness of Path Curvature\] Consider a $T \mathcal B$-admissible curve $\wp=(\gamma,\eta)\in\mathop{\mathrm{Lip}}([0,1],\mathbb M)$, w.r.t. the control sets $\mathcal B$ defined in [\[eq_BEControlSet\]](#eq_BEControlSet){reference-type="ref+label" reference="eq_BEControlSet"}. Then the path curvature $\kappa$ of the physical projection curve $\gamma$ satisfies $$\begin{equation*}
\Im_{\rm min}(\wp(t))\leq\kappa(t)\leq \Im_{\rm max}(\wp(t)),\quad\forall t\in[0,1].
\end{equation*}$$*
:::

::: proof
*Proof.* Define for each point $\mathbf p= (\mathfrak p,\theta) \in \mathbb M$ the following subset $\mathbb E_\mathbf p\subset \mathbb E$ of the tangent space: $$\begin{equation*}
    \mathbb E_\mathbf p:= \{ \lambda \Re(\theta,\psi)\mid \lambda \geq 0,\ \psi_{\min}(\mathbf p) \leq \psi \leq \psi_{\max}(\mathbf p)\}.
\end{equation*}$$ It is not hard to see that $\mathbb E_\mathbf p$ is a closed and convex two-dimensional cone, generated by two extremal vectors: $$\begin{equation*}
\mathbb E_\mathbf p:= \{ \alpha \Re(\theta,\psi_{\min}(\mathbf p)) + \beta \Re(\theta,\psi_{\max}(\mathbf p)) \mid \alpha,\beta \geq 0\}.
\end{equation*}$$ One has $\frac{\partial\mathcal H}{\partial \hat \mathbf p}(\mathbf p,\hat \mathbf p)\in \mathbb E_\mathbf p$, in view of the integral expression of this gradient and by convexity of $\mathbb E_\mathbf p$, and therefore $\mathcal B(\mathbf p) \subset \mathbb E_\mathbf p$ in view of [\[eq_BEControlSet\]](#eq_BEControlSet){reference-type="ref+label" reference="eq_BEControlSet"}. As a result, for any $T\mathcal B$-admissible curve $\wp=(\gamma,\eta) : [0,1] \to \mathbb M$ and for a.e. $t \in [0,1]$ one has $$\begin{equation*}
\wp^\prime(t)\propto \Re\bigl(\eta(t),\varphi(t)\bigr),
\end{equation*}$$ for some angle $\varphi(t)$ such that $\psi_{\min}(\wp(t)) \leq \varphi(t) \leq \psi_{\max}(\wp(t))$. The curvature $\kappa$ of the path $\gamma$ is thus formulated as $$\begin{equation*}
\kappa(t)=\frac{\eta^\prime(t)}{\|\gamma^\prime(t)\|}=\xi^{-1}\tan(\varphi(t))\in\bigl[\Im_{\rm min}(\wp(t)),\Im_{\rm max}(\wp(t))\bigr]
\end{equation*}$$ which concludes the proof. ◻
:::

:::: {#fig_AdvContrCurvature .figure latex-placement="!htbp"}
![](Chen2026Computing_figs/fig4.png){width="\\linewidth"}

::: caption
Illustration of different curvature-penalized models on controlling the path curvature. **Column 1**: Visualization for physical projection curves of the minimal paths associated to different models. The blue and red dots respectively indicate the source point and the target point, and the arrows indicate the path tangent directions assigned to these points. **Columns 2-3**: The line plots of the turning angles and path curvature of the physical projection curves as functions of Euclidean curve length.
:::
::::

## curvature-bounded Model is a Generalization of the Euler-Mumford Elastica Model {#curvature-bounded-model-is-a-generalization-of-the-euler-mumford-elastica-model .unnumbered}

In this section, we reveal the tight relationship between the proposed curvature-bounded model and the Euler-Mumford Elastica model [@chen2017global; @mirebeau2018fast], by comparing their respective Hamiltonians. For that purpose, let us first reformulate the Hamiltonian $\mathcal H$ of the curvature-bounded model, using the linear change of variables $\varphi = (\psi-\Psi_\mathbf p)/\lambda_\mathbf p$ in the defining integral of [\[eq_BEHamiltonian\]](#eq_BEHamiltonian){reference-type="ref+label" reference="eq_BEHamiltonian"}: $$\begin{equation}
\label{eq_EquivBEHamiltonian}
\mathcal H(\mathbf p,\hat{\mathbf{p}})=\frac{3}{8}\mathcal C(\mathbf p)^{-2}\int_{-\pi/2}^{\pi/2}\langle\hat{\mathbf{p}}, \Re(\theta,\lambda_\mathbf p\varphi+\Psi_\mathbf p)\rangle_+^2\cos(\varphi)d\varphi
\end{equation}$$ for any point $\mathbf p=(\mathfrak p,\theta)\in\mathbb M$ and any co-vector $\hat{\mathbf{p}}=(\hat{\mathfrak{p}},\hat\theta)\in\mathbb E^*$. Note that the weight $w_\mathbf p$ in [\[eq_VarFejWeights\]](#eq_VarFejWeights){reference-type="ref+label" reference="eq_VarFejWeights"} simplifies here to $\cos\varphi$. The control vectors in [\[eq_EquivBEHamiltonian\]](#eq_EquivBEHamiltonian){reference-type="ref+label" reference="eq_EquivBEHamiltonian"} read $$\begin{equation*}
%\label{eq_BEControlNew}
\Re(\theta,\lambda_\mathbf p\varphi+\Psi_\mathbf p)=(\mathbf{n}(\theta)\cos(\lambda_\mathbf p\varphi+\Psi_\mathbf p),\xi^{-1}\sin(\lambda_\mathbf p\varphi+\Psi_\mathbf p))
\end{equation*}$$ and therefore depend on the terms $\Psi_\mathbf p$ and $\lambda_\mathbf p$ related to the curvature bounds. On the other hand, the Hamiltonian $\mathfrak H$ associated with the Euler-Mumford Elastica model can be formulated as follows [@mirebeau2018fast] $$\begin{equation}
\label{eq_ElasticaHam}
\mathfrak H(\mathbf p,\hat{\mathbf{p}})=\frac{3}{8}\mathcal C(\mathbf p)^{-2}\int_{-\pi/2}^{\pi/2} \left\langle\hat{\mathbf{p}},\Re(\theta,\varphi) \right\rangle_+^2\cos\varphi\, d\varphi.
\end{equation}$$

The difference between the Hamiltonian $\mathcal H$ of the proposed curvature-bounded model, and the original one $\mathfrak H$, thus solely lies in the translation and scaling $\lambda_\mathbf p\varphi + \Psi_\mathbf p$ of the angular parameter of the control vectors, introduced in this work to enforce curvature bounds. In the special case where the angles $\psi_{\rm min},\,\psi_{\rm max}$ in the Hamiltonian $\mathcal H$ are respectively set as $\psi_{\rm min}\equiv -\pi/2$ and $\psi_{\rm max}\equiv\pi/2$, the lower and upper curvature bounds become infinite $\Im_{\rm min}\equiv-\infty,\,\Im_{\rm max}\equiv\infty$, and the angular parameters of the control vectors remain untouched $\lambda_\mathbf p=1,\,\Psi_\mathbf p=0,\,\forall\mathbf p\in\mathbb M$. Under these circumstances, our model thus coincides with the standard Euler-Mumford Elastica model.

Let $\mathfrak B(\mathbf p)$ be the control set of the Euler-Mumford Elastica model at a point $\mathbf p= (\mathfrak p,\theta) \in \mathbb M$. By a reasoning similar to the proposed curvature-bounded model, one has $\mathfrak B(\mathbf p) \subset \mathbb E_\theta$, and one may therefore define the sliced control sets $$\begin{equation*}
\tilde\mathfrak B(\mathbf p)=\left\{(\dot\nu,\dot\theta)\in\mathbb R^2~|~\dot\nu\geq0,(\dot\nu\mathbf{n}(\theta),\dot\theta)\in\mathfrak B(\mathbf p)\right\}.
\end{equation*}$$ It is known [@chen2017global; @mirebeau2018fast] that $\tilde\mathfrak B(\mathbf p)$ is an *ellipse* (and more precisely a *disk* in the special case where $\xi=1$), whose center lies on the $\dot \nu$ axis, and whose boundary is tangent to the origin.

## On the parameter $\xi$ in the Curvature-bounded Model {#on-the-parameter-xi-in-the-curvature-bounded-model .unnumbered}

As defined in [\[eq_ControlVector\]](#eq_ControlVector){reference-type="ref+label" reference="eq_ControlVector"} and [\[eq_BEHamiltonian\]](#eq_BEHamiltonian){reference-type="ref+label" reference="eq_BEHamiltonian"}, the curvature-bounded model involves a parameter $\xi>0$ that modulates both the shape of the control sets and the relative importance of the curvature of the corresponding minimal paths. In Fig. [3](#fig_ControlSets_Xi){reference-type="ref" reference="fig_ControlSets_Xi"}, the boundaries of the sliced control sets $\tilde\mathcal B(\mathbf p)$ associated with the curvature-bounded model are illustrated, under varying values of parameter $\xi$ and of curvature bounds $\Im_{\rm min},\,\Im_{\rm max}$. Fig. [3](#fig_ControlSets_Xi){reference-type="ref" reference="fig_ControlSets_Xi"}d depicts a qualitative comparison of minimal paths computed using the curvature-bounded model. Both minimal paths are generated using the sliced control sets shown in Fig. [3](#fig_ControlSets_Xi){reference-type="ref" reference="fig_ControlSets_Xi"}a, corresponding to curvature bounds $\Im_{\rm min}\equiv-1$ and $\Im_{\rm max}\equiv1$. More precisely, the red line is computed using the curvature-bounded model with $\xi=1$, and the black line with $\xi=2$. Similar to the its effect in the Euler-Mumford Elastica model [@chen2017global; @mirebeau2018fast], the parameter $\xi$ in the curvature-bounded model controls the smoothness of paths: high values of $\xi$ are expected to produce minimal paths whose physical projection curves have low maximum curvature. Note that the increased curvature penalty associated with high values of $\xi$ is independent of curvature bounds. Similarly, in Fig. [3](#fig_ControlSets_Xi){reference-type="ref" reference="fig_ControlSets_Xi"}d, the red line exhibits a lower minimum turning radius (i.e. higher maximum path curvature) compared to the black line.

## Significance in Controlling the Boundedness of the Path Curvature {#significance-in-controlling-the-boundedness-of-the-path-curvature .unnumbered}

Given two endpoints as well as the angles that corresponds to the path tangents at these points, a major advantage of our curvature-bounded model, over existing curvature-penalized models, lies at its strong ability in controlling the path curvature of the computed minimal paths, since it imposes a hard constraint on the curvature via arbitrary lower and upper bounds, as formulated in [\[eq_curvatureBounds\]](#eq_curvatureBounds){reference-type="ref+label" reference="eq_curvatureBounds"}. In contrast, the classical Euler-Mumford Elastica model [@chen2017global; @mirebeau2018fast] takes into account a squared curvature penalty as the model regularization, whereas the Dubins car model [@mirebeau2018fast] is designed to search for minimal paths, where the *absolute curvature* of the physical projection curves is bounded by a positively-defined scalar-valued function. This explicitly implies that neither the Euler-Mumford Elastica model nor the Dubins car model can limit the path curvature of the corresponding minimal paths to satisfy mandatory *arbitrary bounds*. Moreover, the minimal paths of the Dubins model are non-smooth and frequently saturate the curvature bounds.

In Fig. [4](#fig_AdvContrCurvature){reference-type="ref" reference="fig_AdvContrCurvature"}, we conduct numerical experiments to exhibit the advantages of the curvature-bounded model in manipulating the curvature (of the physical projection curves) of the minimal paths, when comparing to the Euler-Mumford Elastica model and to the Dubins model. In this experiment, each test is set up with a single source point $\mathbf s\in\mathbb M$ and two target points $\mathbf x_j$ for $j\in\{1,2\}$, which yields two minimal paths $\mathcal G_{\mathbf s,\mathbf x_j}=(\tilde{\gamma}_{\mathbf s,\mathbf x_j},\tilde{\eta}_{\mathbf s,\mathbf x_j})$ sharing the same source point $\mathbf s$. We choose a point $\mathbf x^*$ corresponding to lower minimum arrival time $\mathcal T_{\mathcal B}$, see [\[eq_MinimalTime\]](#eq_MinimalTime){reference-type="ref+label" reference="eq_MinimalTime"}, i.e $$\begin{equation}
\mathcal T_{\mathcal B}(\mathbf s,\mathbf x^*)=\min\{\mathcal T_{\mathcal B}(\mathbf s,\mathbf x_1),\mathcal T_{\mathcal B}(\mathbf s,\mathbf x_2)\}.
\end{equation}$$ For the sake of simplicity, we denote by $\mathcal G_*=(\tilde{\gamma}_*,\tilde{\eta}_*)$ the chosen minimal path, where the physical projection curve, the turning angles and path curvature of the physical projection curve are respectively denoted by $\tilde{\gamma}_*$, $\tilde{\eta}_*$ and $\tilde\kappa_*$. Furthermore, the cost $\mathcal C$, as formulated in [\[eq_BEHamiltonian\]](#eq_BEHamiltonian){reference-type="ref+label" reference="eq_BEHamiltonian"} and [\[eq_ElasticaHam\]](#eq_ElasticaHam){reference-type="ref+label" reference="eq_ElasticaHam"}, for the curvature-penalized models considered are fixed as $\mathcal C\equiv1$.

The left column of Fig. [4](#fig_AdvContrCurvature){reference-type="ref" reference="fig_AdvContrCurvature"} illustrates the physical projection curves $\tilde{\gamma}_*$ derived from curvature-penalized models with respect to different parameters which affect the path curvature, the middle column draws the respective turning angles $\tilde{\eta}_*$ which is regarded as a function of the Euclidean curve length, and the right column illustrates the line plots of the path curvature of the physical projection $\tilde{\gamma}_*$. More specifically, Fig. [4](#fig_AdvContrCurvature){reference-type="ref" reference="fig_AdvContrCurvature"}a illustrates the physical projection curves of the Euler-Mumford Elastica minimal paths, whose turning angles feature a slowly-varying property, as demonstrated in Fig. [4](#fig_AdvContrCurvature){reference-type="ref" reference="fig_AdvContrCurvature"}b. It follows that the Euler-Mumford Elastica model encourages the minimal paths to be smooth. Analogous to the Euler-Mumford Elastica model, the characteristics of the smoothness property can also be observed in Figs. [4](#fig_AdvContrCurvature){reference-type="ref" reference="fig_AdvContrCurvature"}g and [4](#fig_AdvContrCurvature){reference-type="ref" reference="fig_AdvContrCurvature"}h, where the physical projection curves and their turning angles are produced through the proposed curvature-bounded model.

:::: {#fig_SynComp .figure latex-placement="!htbp"}
![](Chen2026Computing_figs/fig5.jpg){width="99%"}

::: caption
Qualitative comparisons on synthetic images containing curvilinear structures of varying shapes. In column $1$, the red and blue dots respectively mark the physical positions of the source and target points for initializing the minimal path models, with arrows indicating their assigned tangent vectors. Columns $2$ to $5$ show the physical projection curves of minimal paths computed from the Euler-Mumford Elastica model, the Dubins model, the curvature prior Elastica model and the proposed curvature-bounded geodesic model, respectively .
:::
::::

## Curvilinear Structure Tracking {#subsec_VesselTracking .unnumbered}

Finding curvilinear structure centerlines from images of various modalities is a challenging problem, due to the presence of complex geometry appearance such as branched structures and rapidly-varying background content. Those centerlines can be naturally modeled as minimal paths which are solutions to a global optimization problem integrating data-driven cost with curve regularization [@liao2022progressive; @liao2023segmentation; @chen2019minimal; @pechaud2009extraction; @li2007vessels]. In particular, the proposed curvature-bounded model takes both curvature penalization and curvature bounds as regularization, and is suitable for tracking curvilinear structure centerlines, since the curvature bounds can be efficiently estimated from the image data and can be naturally used as strong geometric priors to enhance the results. In particular, this application works in conjunction with the estimation of curvature bounds from image data.

In this article we focus on the extraction of curvilinear structure centerline, providing that its two endpoints and their respective tangent directions are given. The solution to such a task typically involves two major ingredients that should be estimated from the image data. Specifically, the first ingredient is the cost function $\mathcal C$ as utilized in [\[eq_EquivBEHamiltonian\]](#eq_EquivBEHamiltonian){reference-type="ref+label" reference="eq_EquivBEHamiltonian"}. It characterizes the appearance of the curvilinear structures and can be computed as a decreasing function of the orientation scores [@chen2017global; @chen2023computing]. In principle, the value of the cost $\mathcal C(\mathbf p)$ is supposed to be low at a given point $\mathbf p=(\mathfrak p,\theta)\in\mathbb M$, provided that the physical position $\mathfrak p$ is inside a curvilinear structure and simultaneously the direction $(\cos\theta,\sin\theta)$ is nearly collinear to the centerline tangent at a position close to $\mathfrak p$. The second ingredient lies at the construction of the curvature bounds $\Im_{\rm min}$ and $\Im_{\rm max}$ using the image data. As introduced in [@chen2023computing], one can estimate the path curvature, which are referred to as curvature priors, of computed curvilinear centerline segments as prescribed geometric features. The curvature priors are encoded in a scalar-valued function $\varpi:\mathbb M\to\mathbb R$, by which the curvature bounds $\Im_{\rm min}$ and $\Im_{\rm max}$ can be naturally constructed as follows: $$\begin{equation}
\label{eq_CurvatureBounds}
\Im_{\rm max}(\mathbf p):=\varpi(\mathbf p)+\varsigma/2\quad\text{and}\quad\Im_{\rm min}(\mathbf p):=\varpi(\mathbf p)-\varsigma/2,
\end{equation}$$ where $\varsigma>0$ is a constant.

:::: {#fig_MedDataComp .figure latex-placement="!htbp"}
![](Chen2026Computing_figs/fig6.jpg){width="99%"}

::: caption
Qualitative comparison on tracking curvilinear structure centerlines from medical images. **Column 1** The dots and the arrows indicate the source and target points for initializing the minimal path models. **Columns 2-5** The physical projections of minimal paths derived from different curvature-penalized models are demonstrated.
:::
::::

Note that the curvature priors $\varpi$ characterize the prescribed curvature values of curvilinear structure centerlines. We exploit the same procedure as the curvature prior Elastica model [@chen2023computing] to compute $\varpi$ over the orientation-lifted space $\mathbb M$, where a key step for this tracking method is to compute a set of disjoint piecewise smooth curves which fit to the discrete centerline segments. For this purpose, we develop an efficient segmentation-free algorithm for detecting those discrete centerline segments, allowing to fully benefit from the strongly oriented features of the elongated structures. The details can be seen in the Supplemental Information.

We demonstrate in Fig. [5](#fig_SynComp){reference-type="ref" reference="fig_SynComp"} and Fig. [6](#fig_MedDataComp){reference-type="ref" reference="fig_MedDataComp"} the qualitative comparison results between the proposed curvature-bounded model and state-of-the-art curvature-penalized models, involving the classical Euler-Mumford Elastica model [@chen2017global; @mirebeau2018fast], the Dubins model [@mirebeau2018fast] and the curvature prior Elastica model [@chen2023computing] in tracking curvilinear structure centerlines. In each test, the compared models are given two source points and two targets for initialization. As in the literature [@chen2017global; @chen2023computing], such an initialization manner allows to generate four minimal paths, among which the one with minimum arrival time is chosen as the output of the model.

In Fig. [5](#fig_SynComp){reference-type="ref" reference="fig_SynComp"}, the synthetic curvilinear structures are deliberately designed to facilitate the evaluation of the smoothness, rigidity and elasticity properties exhibited by different minimal path models. Columns $2$ to $5$ present the physical projection curves of minimal paths computed using the Euler-Mumford Elastica model, the Dubins model and the curvature-bounded model, respectively. The first row of Fig. [5](#fig_SynComp){reference-type="ref" reference="fig_SynComp"} shows a spiral-like curvilinear structure. As observed in columns in columns $2$ to $4$ of the first row, the resulting minimal paths unfortunately suffer from shortcut artifacts, failing to follow the desired structures. In the second row, the image depicts an elongated shape of letter "$6$\", where the red dots indicate the physical endpoints of minimal paths placed around the junction pattern. The physical projection curves of the minimal paths are expected to traverse regions near the red dots in order to accurately delineate the entire structure. The optimal paths shown in columns $2$ and $3$ fail to accurately capture the circular structures. In the third row, the synthetic image presents a more complex curvilinear pattern composed of three self-intersecting loops. In this test, the models shown in columns $2$ to $4$ fail to accurately extract the circular structures due to insufficient constraint over the path curvature. In contrast, the curvature-bounded model as demonstrated in column $5$ of Fig. [5](#fig_SynComp){reference-type="ref" reference="fig_SynComp"}, successfully produces minimal paths that capture these circular structures, due to the blended benefits from the curvature penalization and the mandatory curvature bounds.

The synthetic curvilinear patterns illustrated in Fig. [5](#fig_SynComp){reference-type="ref" reference="fig_SynComp"} faithfully represent the characteristic geometries of blood vessels, nerve fibers, and roads in medical and aerial images, as exemplified in Fig. [6](#fig_MedDataComp){reference-type="ref" reference="fig_MedDataComp"}. Consistent with experiments conducted in Fig. [5](#fig_SynComp){reference-type="ref" reference="fig_SynComp"}, compared curvature-penalized models exhibit obvious shortcut artifacts and fail to follow the desired curvilinear trajectories, as evident in columns $2$--$4$ of Fig. [6](#fig_MedDataComp){reference-type="ref" reference="fig_MedDataComp"}. In contrast, the proposed curvature-bounded model robustly recovers the underlying structures, even in the presence of complex backgrounds or circular patterns, see column $5$.

# Methods

We describe in this section the numerical method for computing minimal paths of the proposed curvature-bounded model. We introduce a static first-order HJB PDE associated with the optimal control problem of interest, a backtracking ordinary differential equation (ODE) for recovering optimal paths from its viscosity solution the minimal action map, and suitable finite difference discretizations of the PDE and ODE.

## Upwind Discretization Scheme {#upwind-discretization-scheme .unnumbered}

We apply the scheme introduced in [@mirebeau2018fast; @mirebeau2019riemannian] for the discretization of the HJB PDE. Let $U$ be the numerical approximation, defined on the Cartesian grid $\mathbb M_h=\mathbb M\cap (h\mathbb Z^2\times h\mathbb Z/2\pi\mathbb Z)$ of scale $h>0$, of the viscosity solution $\mathcal U_\mathbf s$ by solving in a single pass a well chosen wide stencil finite differences discretization of the HJB PDE [\[eq_BEHJB\]](#eq_BEHJB){reference-type="ref+label" reference="eq_BEHJB"}. In the numerical experiments, we set the grid scale to $h=2\pi/N_{\rm angles}$, where $N_{\rm angles}\in\mathbb{N}$ is the number of discrete angles along the third dimension of $\mathbb M$.

Let us recall that the control vector in the proposed curvature-bounded model is formulated as $\Re(\theta,\psi)=(\cos(\psi)\mathbf{n}(\theta),\xi^{-1}\sin(\psi))$. The integral defining the corresponding Hamiltonian $\mathcal H$, see [\[eq_EquivBEHamiltonian\]](#eq_EquivBEHamiltonian){reference-type="ref+label" reference="eq_EquivBEHamiltonian"}, is first approximated using the Fejer quadrature rule: following [@mirebeau2018fast] $$\begin{align}
\mathcal C(\mathbf p)^{2}\mathcal H(\mathbf p,\hat{\mathbf{p}})&=\frac{3}{8}\int_{-\pi/2}^{\pi/2}\langle\hat{\mathbf{p}}, \Re(\theta,\lambda_\mathbf p\varphi+\Psi_\mathbf p)\rangle_+^2\,\cos\varphi\,d\varphi\nonumber\\
\label{eq_HamiltonianDecom}
&=\frac{3}{16}\sum_{1\leq\ell\leq L}f_\ell\langle\hat{\mathbf{p}},\Re(\theta,\tilde\varphi_\ell) \rangle_+^2+\mathcal O(L^{-2})
\end{align}$$ for any point $\mathbf p=(\mathfrak p,\theta)$. The number of $L$ nodes of the Fejer quadrature rule is fixed to $9$ in all the numerical experiments in this work. The Fejer weights $f_\ell \geq 0$, $1 \leq \ell \leq L$ are tabulated in the literature, and the angular nodes are defined as $\varphi_l := (2\ell- L - 1)\pi /(2L)$. For convenience we denoted $\tilde \varphi_\ell := \lambda_\mathbf p\varphi_\ell+\Psi_\mathbf p$.

In the spirit of the wroks [@mirebeau2019riemannian; @mirebeau2018fast], each quadratic term $\langle\hat{\mathbf{p}},\Re(\theta,\tilde\varphi_\ell) \rangle_+^2$ in [\[eq_HamiltonianDecom\]](#eq_HamiltonianDecom){reference-type="ref+label" reference="eq_HamiltonianDecom"} is approximated via a family of positive weights $\rho_{j\ell}^\theta:=\rho_j^\epsilon(\Re(\theta,\tilde\varphi_\ell))>0$ and offsets $\dot{\mathbf e}^\theta_{j\ell}:=\dot{\mathbf e}_j^\epsilon(\Re(\theta,\tilde\varphi_\ell))\in\mathbb Z^3$ whose coordinates are integers, where $1\leq j \leq J:= 6$ are indices and where $\epsilon>0$ is a relaxation parameter, as follows: for any angular node $\tilde\varphi_\ell$ $$\begin{equation}
\label{eq_QuadraAppro}
\langle\hat{\mathbf{p}},\Re(\theta,\tilde\varphi_\ell)\rangle_+^2=\sum_{1\leq j \leq J}\rho_{j\ell}^\theta\langle\hat{\mathbf{p}},\dot{\mathbf e}_{j\ell}^\theta \rangle _+^2+\|\hat{\mathbf{p}}\|^2\mathcal O(\epsilon^2).
\end{equation}$$ The weights $\rho_{j\ell}^\theta$ and offsets $\dot{\mathbf e}^\theta_{j\ell}$ are computed relying on the theorem of Selling's decomposition of positive quadratic forms [@mirebeau2018fast]. Combining [\[eq_HamiltonianDecom\]](#eq_HamiltonianDecom){reference-type="ref+label" reference="eq_HamiltonianDecom"} and [\[eq_QuadraAppro\]](#eq_QuadraAppro){reference-type="ref+label" reference="eq_QuadraAppro"}, we approximate the HJB PDE operator value $\mathcal H(\mathbf p,d\mathcal U_\mathbf s(\mathbf p))$ as $$\begin{align}
\label{eq_HamiltonQuadraDecom}
\mathcal H(\mathbf p,d\mathcal U_\mathbf s(\mathbf p))\approx
\frac{3}{16}\mathcal C(\mathbf p)^{-2}\sum_{1\leq \ell \leq L}f_{\ell}\sum_{1\leq j \leq J}\rho^\theta_{j\ell}\langle d\mathcal U_\mathbf s(\mathbf p),\dot{\mathbf e}^\theta_{j\ell} \rangle_+^2.
\end{align}$$ Finally, we approximate the directional gradient $\langle d\mathcal U_\mathbf s(\mathbf p),\dot{\mathbf e}^\theta_{j\ell}\rangle_+$ of the minimal action map with the upwind finite difference $h^{-1}(U(\mathbf p)-U(\mathbf p-h\dot{\mathbf e}_{j\ell}^\theta))_+$ of the unknown $U:\mathbb M_h\to[0,\infty[$ of our discretization. The HJB PDE is thus discretized by the system of equations $$\begin{equation*}
\frac{3}{8}\sum_{1\leq \ell\leq L}f_{\ell} \sum_{1\leq j\leq J}\rho_{j\ell}^\theta\left(\frac{U(\mathbf p)-U(\mathbf p-h\dot{\mathbf e}_{j\ell}^\theta)}{h}\right)_+^2=\mathcal C(\mathbf p)^2,
\end{equation*}$$ for all $\mathbf p\in \mathbb M_h \setminus\{\mathbf s\}$, together with the source constraint $U(\mathbf s) = 0$ and outflow boundary conditions on $\partial \mathbb M$.

Using both of [\[eq_geodesicFlows\]](#eq_geodesicFlows){reference-type="ref+label" reference="eq_geodesicFlows"} and [\[eq_HamiltonQuadraDecom\]](#eq_HamiltonQuadraDecom){reference-type="ref+label" reference="eq_HamiltonQuadraDecom"}, the geodesic flows $\mathbf V$ can be approximated through the positive weights and offsets of integer coordinates as follows $$\begin{equation}
\label{eq_GVApprox}
\mathbf V(\mathbf p)\approx\frac{-3}{8\mathcal C(\mathbf p)^2}\sum_{1\leq \ell \leq L}f_\ell\sum_{1\leq j \leq J}\rho_{j\ell}^\theta \,\langle d\mathcal U_\mathbf s(\mathbf p),\dot{\mathbf e}_{j\ell}^\theta \rangle_+\,\dot{\mathbf e}^\theta_{j\ell}.
\end{equation}$$ Then the finite difference scheme for numerically approximating the geodesic flow $\mathbf V$ of the form formulated in [\[eq_GVApprox\]](#eq_GVApprox){reference-type="ref+label" reference="eq_GVApprox"} is expressed as $$\begin{equation*}
\mathbf V(\mathbf p)\approx\frac{-3}{8\mathcal C(\mathbf p)^2}\!\!   \sum_{1\leq \ell \leq L}f_\ell\sum_{1\leq j \leq J}\rho_{j\ell}^\theta\,\left(\frac{U(\mathbf p)-U(\mathbf p-h\dot{\mathbf e}^\theta_{j\ell})} h\right)_+\dot{\mathbf e}^\theta_{j\ell}.
\end{equation*}$$

# Conclusion {#sec_conclusion}

In this paper, we propose a curvature-bounded geodesic model formulated within the HJB PDE framework that computes globally optimal curves with second-order regularization under arbitrary curvature bounds constraint. The primary theoretical contribution is the implicit embedding of mandatory curvature range constraints into the Hamiltonian, which forms the foundation of the associated HJB PDE. Furthermore, we develop an upwind discretization scheme for the Hamiltonian of the curvature-bounded model, yielding a discretized HJB system that seamlessly integrates with the state-of-the-art Hamiltonian Fast Marching method, enabling efficient approximation of minimal action maps.

The proposed curvature-bounded model effectively tracks curvilinear structures in complex scenarios, where the construction of the curvature bounds, defining the admissible curvature varying ranges, is a critical step for practical applications.In our formulation, the curvature bound at each point is defined by a prior term combined with a scalar offset term that adapts to local features of elongated shapes. These curvature priors are obtained by fitting smooth curves to disjoint segments of predefined curvilinear centerlines. However, their accuracy may be degraded by fragmentation in the precomputed curvilinear centerlines. An alternative and promising direction is to design a path voting scheme, in which curvature priors and offset terms are efficiently estimated from a dense set of minimal paths distributed across all plausible curvilinear patterns.

Moreover, the proposed curvature-bounded geodesic model is a powerful tool for extracting curvilinear structures, providing that their endpoints and the tangent directions at those points are given. Future work will focus on integrating this model with a path classifier [@gupta2023topology; @turetken2016reconstructing] to enable the automatic reconstruction and tracking of entire curvilinear networks.

# Appendices {#appendices .unnumbered}

# Computing the Minimal Action Map Through the Static First-order HJB PDE Framework

For clarity, we start with a reformulation of the optimal control problem of [\[eq_MinimalTime\]](#eq_MinimalTime){reference-type="ref+label" reference="eq_MinimalTime"}, involving the control sets $\mathcal B$, as the computation of a path length distance [@mirebeau2019riemannian; @bardi1997Optimal], from a source point $\mathbf s\in\mathbb M$ to a target point $\mathbf p\in\mathbb M$. Indeed, the data of the control sets $\mathcal B$ is equivalent to the data of a (sub-Finslerian) geodesic metric $\mathcal F:\mathbb M\times\mathbb E\to[0,\infty]$ defined as $$\begin{equation}
\mathcal F(\mathbf p,\dot{\mathbf{p}}):=\inf\,\bigl\{\lambda>0~|~(\dot{\mathbf{p}}/\lambda)\in\mathcal B(\mathbf p)\bigr\}    .
\end{equation}$$ The corresponding path length reads $$\begin{equation}
\label{eq_Length}
\mathop{\mathrm{Length}}_\mathcal F(\wp):=\int_0^1\mathcal F(\wp(t),\wp^\prime(t))dt,
\end{equation}$$ and its minimization leads to an equivalent expression of the minimal traveltime from $\mathbf s$ to $\mathbf p$ w.r.t. $\mathcal B$, see [\[eq_MinimalTime\]](#eq_MinimalTime){reference-type="ref+label" reference="eq_MinimalTime"} $$\begin{align}
\label{eq_MinimalLength}
\mathcal T_{\mathcal B}(\mathbf s,\mathbf p):=\inf\bigl\{\mathop{\mathrm{Length}}_\mathcal F(\wp)~|~&\wp\in\mathop{\mathrm{Lip}}([0,1],\mathbb M),\nonumber\\
&\wp(0)=\mathbf s,\wp(1)=\mathbf p\bigr\}.
\end{align}$$

Fixing the source point $\mathbf s$, the minimal action map $\mathcal U_\mathbf s:\mathbb M\to [0,\infty]$ assigns to each possible endpoint $\mathbf p$ the corresponding minimum arrival time: $$\begin{equation}
\label{eq_MAP}
\mathcal U_\mathbf s(\mathbf p)=\mathcal T_\mathcal B(\mathbf s,\mathbf p).
\end{equation}$$ The static first-order HJB PDE framework [@cohen1997global; @bardi1997Optimal] characterizes $\mathcal U_\mathbf s$ as the unique viscosity solution to a boundary value problem: $$\begin{equation}
\label{eq_BEHJB}
\begin{cases}
\mathcal H(\mathbf p,d\mathcal U_\mathbf s(\mathbf p))=\frac{1}{2},&\forall \mathbf x\in\mathbb M\backslash\{\mathbf s\}\\
\mathcal U_\mathbf s(\mathbf s)=0,&\text{(boundary condition)},
\end{cases}
\end{equation}$$ where $d\mathcal U_\mathbf s$ denotes the first-order differential of the minimal action map $\mathcal U_\mathbf s$.

The geodesic flow towards the seed $\mathbf s$ is represented by a vector field $\mathbf V$ defined in terms of the minimal action map $\mathcal U_\mathbf s$: $$\begin{equation}
\label{eq_geodesicFlows}
\mathbf V(\mathbf p)=-\partial_2 \mathcal H(\mathbf p,d\mathcal U_\mathbf s(\mathbf p))
\end{equation}$$ where $\partial_2\mathcal H(\mathbf p,\hat{\mathbf{p}}):=\partial\mathcal H(\mathbf p,\hat{\mathbf{p}})/\partial\hat{\mathbf{p}}$. The vector $\mathbf V(\mathbf p)$ is the negative gradient of the minimal action map $\mathcal U_\mathbf s$ at $\mathbf p$ and w.r.t. the local metric $\mathcal F(\mathbf p,\cdot)$, and its characterizes the tangent direction of the shortest path towards $\mathbf s$. More precisely, consider an arbitrary point $\mathbf p\in \mathbb M$, and the path $\mathcal G: [0,T] \to \mathbb M$ obeying the ordinary differential equation $$\begin{equation*}
\label{eq_Backtracking}
\mathcal G^\prime(t)=\mathbf V(\mathcal G(t)),~\forall t\in]0,T[.
\end{equation*}$$ with initial value $\mathcal G(0)=\mathbf p$ and total time $T = \mathcal U_\mathbf s(\mathbf p)$. This *backtracked* path $\mathcal G$ travels by construction from the target point $\mathbf p$ to the source point $\mathbf s$. By re-parametrization one obtains a minimal path $\mathcal G_{\mathbf s,\mathbf p}(t):=\mathcal G(T(1-t))$ from the source $\mathcal G_{\mathbf s,\mathbf p}(0)=\mathbf s$ to the target $\mathcal G_{\mathbf s,\mathbf p}(1)=\mathbf p$.

# Computing Geometric Features from Curvilinear Structures

## Orientation Scores {#orientation-scores .unnumbered}

In practice, the tool of the orientation scores is designed to characterize the appearance of curvilinear structures in an anisotropy manner, so as to alleviate the negative influence from the mixed complicated data distribution and structures of crossing morphology. Recall that $\mathbb M=\Omega\times\mathbb S^1$ represents the orientation-lifted space, where $\Omega\subset\mathbb R^2$ is the image domain and $\mathbb S^1=[0,2\pi[$ is an interval of periodic boundary condition. The orientation score map, denoted by a scalar-valued map $\tilde\alpha:\mathbb M\to[0,\infty[$, can be extracted from a gray level image $f:\Omega\to\mathbb R$ via an orientation-dependent filter bank $\hbar$: $$\begin{equation*}
\tilde\alpha(\mathfrak p,\theta)=(\hbar_\theta\ast f)(\mathfrak p)
\end{equation*}$$ for any physical position $\mathfrak p\in\Omega$ and for any an angular coordinate $\theta\in\mathbb S^1$, where $\ast$ is a convolution operator. In practice, the orientation score map $\tilde\alpha$ is usually normalized to the range $[0,1]$: $$\begin{equation}
\label{eq_NLOS}
\alpha(\mathfrak p,\theta)=\tilde\alpha(\mathfrak p,\theta)/\|\tilde\alpha\|_\infty.
\end{equation}$$ Many curvilinear structure filters can be applied to compute the orientation score map $\alpha$, where typical examples may involve the steerable filters [@law2008three; @jacob2004design], the filter depending on the cake wavelets [@franken2009crossing] and filter consisting of multiple Gaussian kernels [@moriconi2018inference]. The value of the orientation score $\alpha(\mathfrak p,\theta)$ characterizes the probability that the physical position $\mathfrak p$ is inside the curvilinear structures and simultaneously the direction $\mathrm{n}(\theta)=(\cos\theta,\sin\theta)$ is collinear to the orientation that a curvilinear structure should have at the physical position $\mathfrak p$. In Fig. [7](#fig_OS){reference-type="ref" reference="fig_OS"}, we illustrate an example for the orientation scores computed from an image involving two curvilinear structures which cross one another.

## Detection of the Centerlines of Curvilinear Structures {#detection-of-the-centerlines-of-curvilinear-structures .unnumbered}

We introduce a method for extracting the centerlines of curvilinear structures using the geometric descriptor of orientation scores. The basic idea is to regard the centerlines of curvilinear structures as a collection of optimal points of orientation score map $\alpha$. In addition, these optimal points should also pass several tests, which are detailed in the following paragraphs.

Firstly, we establish a binary-valued function in the orientation-lifted space, denoted by $\Phi:\mathbb M\to\{0,1\}$, such that fixing a position $\mathfrak p$ the value $\Phi(\mathfrak p,\theta)=1$ implies that the orientation score $\alpha(\mathfrak p,\theta)$ is a local maximum of $\alpha(\mathfrak p,\cdot)$ along the angular dimension, i.e. given a proper value $\epsilon>0$, for any angle that $\phi\in[\theta-\epsilon,\theta+\epsilon]\text{~and~}\phi\neq\theta$, one has $\alpha(\mathfrak p,\theta)>\alpha(\mathfrak p,\phi)$. In other words, $\Phi(\mathfrak p,\cdot)$ characterizes the optimal angles at the physical position $\mathfrak p$ in the sense of the orientation scores. In case the position $\mathfrak p$ is located at a curvilinear structure centerline and $\Phi(\mathfrak p,\theta_*)=1$ at some angle $\theta_*$, then the direction $\mathrm{n}(\theta_*)=(\cos\theta_*,\sin\theta_*)$ should be collinear to the tangent of the centerline at $\mathfrak p$.

Secondly, for each orientation-lifted point $\mathbf p=(\mathfrak p,\theta)\in\mathbb M$ such that $\Phi(\mathfrak p,\theta)=1$, we detect two points $(\mathfrak p_1,\theta_1)$ and $(\mathfrak p_2,\theta_2)$ which are close to $\mathbf p$. In our work this is implemented in a two-step procedure. Specifically, the first step is to produce the physical positions $\mathfrak p_1$ and $\mathfrak p_2$, respectively by moving the physical position $\mathfrak p$ along the directions $\varphi(\theta)=(-\sin\theta,\cos\theta)$ and $-\varphi(\theta)=(\sin\theta,-\cos\theta)$, reading as $$\begin{align*}
&\mathfrak p_1=\mathfrak p+\iota\varphi(\theta)\\
&\mathfrak p_2=\mathfrak p-\iota\varphi(\theta),
\end{align*}$$ where $\iota>0$ is an offset parameter. The angles $\theta_1$ (resp. $\theta_2$) corresponds to the local maximum of the orientation scores $\alpha(\mathfrak p_1,\cdot)$ (resp. $\alpha(\mathfrak p_2,\cdot)$) in the angular dimension within the range $[\theta-\zeta,\theta+\zeta]$ of a periodic boundary condition, where $\zeta>0$ is a positive constant. In other words, the objective angles $\theta_1$ and $\theta_2$ are detected as $$\begin{align*}
&\theta_1=\underset{\phi\in[\theta-\zeta,\theta+\zeta]}{\arg\max}~\alpha(\mathfrak p_1,\phi)\\
&\theta_2=\underset{\phi\in[\theta-\zeta,\theta+\zeta]}{\arg\max}~\alpha(\mathfrak p_2,\phi).
\end{align*}$$ Then we obtain a new function $\Phi_1:\mathbb M\to\{0,1\}$ which is defined as $$\begin{equation*}
\Phi_1(\mathfrak p,\theta)=
\begin{cases}
1,&\text{if~}\alpha(\mathfrak p,\theta)>\max\{\alpha(\mathfrak p_1,\theta_1),\alpha(\mathfrak p_2,\theta_2)\}~\text{and}~\Phi(\mathfrak p,\theta)=1 \\
0,&\text{otherwise}.
\end{cases}
\end{equation*}$$ Actually, the function $\Phi_1(\mathfrak p,\theta)=1$ means that the physical position $\mathfrak p$ is a candidate point of the centerline of a curvilinear structure, since it is a locally optimal point, in terms of the orientation score map $\alpha$, along the normal direction of the centerline at $\mathfrak p$. In order to reduce the negative influence from image noise and also to further refine the detected locally optimal points, we also invoke the test considered in the literature [@wang2013interactive] related to the image gradients $\vartheta:\Omega\to\mathbb R^2$ of a gray level image $f$, i.e. $$\begin{equation*}
\vartheta(\mathfrak p)=(\nabla G_\sigma\ast f)(\mathfrak p)
\end{equation*}$$ where $G_\sigma$ is a Gaussian kernel whose standard deviation is $\sigma$ and where $\nabla G_\sigma$ denotes its standard Euclidean gradient in the space $\mathbb R^2$. As implemented in the literature [@wang2013interactive], each physical position $\mathfrak p$ is assigned to an optimal angle $\theta^*$ $$\begin{equation*}
\theta^*:=\underset{\phi\in[0,2\pi[}{\arg\max}~\alpha(\mathfrak p,\phi),
\end{equation*}$$ which characterizes the orientation of the curvilinear structure at the physical position $\mathfrak p$. The original test presented in [@wang2013interactive] says that a point $\mathfrak p$ is a centerline point if there exists a radius $r$ such that the pair $(\mathfrak p,\theta^*)$ passes the test $$\begin{equation}
\label{eq_NotUsedTest}
\vartheta\bigl(\mathfrak p+r\varphi(\theta^*)\bigr)=-\vartheta\bigl(\mathfrak p-r\varphi(\theta^*)\bigr).
\end{equation}$$ In this work, we consider a new test, slightly different to the one in [\[eq_NotUsedTest\]](#eq_NotUsedTest){reference-type="eqref" reference="eq_NotUsedTest"}, which utilizes all the orientation-lifted points $(\mathfrak p,\theta)$ such that $\Phi_1(\mathfrak p,\theta)=1$. In particular, we evaluate the following formulation $$\begin{equation}
\label{eq_GradTest}
\mathop{\mathrm{sign}}\left(\langle\varphi(\theta),\vartheta(\mathfrak p+r\varphi(\theta))\rangle\right)=-\mathop{\mathrm{sign}}\left(\langle\varphi(\theta),\vartheta(\mathfrak p-r\varphi(\theta))\rangle\right).
\end{equation}$$ We define the target indicator $\Phi_2:\mathbb M\to\{0,1\}$ of the centerlines of curvilinear structures, where $\Phi_2(\mathfrak p,\theta)=1$ if $\Phi_1(\mathfrak p,\theta)=1$ and if the point $(\mathfrak p,\theta)$ passes the test in [\[eq_GradTest\]](#eq_GradTest){reference-type="eqref" reference="eq_GradTest"}. Finally, we obtain a map $\zeta:\Omega\to\{0,1\}$ that involves all the admissible centerline points $$\begin{equation}
\label{eq_SkeleMap}
\zeta(\mathbf p)=
\begin{cases}
1,&\text{if~}\int_0^{2\pi}\Phi_2(\mathfrak p,\theta)d\theta>0\\
0,&\text{otherwise}.
\end{cases}
\end{equation}$$ The binary-valued map $\zeta$ characterizes the curvilinear structure centerlines involved in the image data. It will be further processed to generate a family of disjoint centerline segments, as presented in next section.

# Computing the Curvature Prior Map $\varpi$ from Curvilinear Structure Centerlines

In the application of tracking curvilinear structure centerlines using the introduced bounded Elastica model, a crucial ingredient is the construction of the curvature prior map $\varpi$ using the path curvature which is the intrinsic geometric properties of the curvilinear structure centerline candidates, so as to compute the curvature bounds $\Im_{\rm min}$ and $\Im_{\rm max}$. In our work, we follow the efficient method proposed in the literature [@chen2023computing] to compute the curvature prior map $\varpi$, where the first step is to fit piecewise smooth curvature-penalized optimal paths to the disjoint discrete centerline segments using the map $\zeta$, as introduced in the following section.

## Fitting Smooth Curvature-penalized Minimal Paths to Disjoint Centerline Segments of Curvilinear Structures {#fitting-smooth-curvature-penalized-minimal-paths-to-disjoint-centerline-segments-of-curvilinear-structures .unnumbered}

Let $\Omega_h:=\Omega\cap \mathbb Z^2$ be a Cartesian grid, where $h$ is the grid scale. Without loss of generality, we set the scale $h=1$. In this discrete setting, a discrete centerline segment is defined as a family of ordered grid points of eight-connection and a junction point is regarded as a particular grid point which has more than two eight-connected neighbouring points.

The centerline indicator map $\zeta$ formulated in [\[eq_SkeleMap\]](#eq_SkeleMap){reference-type="eqref" reference="eq_SkeleMap"} involves the information of the potential discrete centerline segments. In order to guarantee that the width of each individual centerline segment equals exactly one grid point, we apply the morphological filter to the set $\{\mathfrak p\in\Omega_h~|~\zeta(\mathfrak p)>0\}$ and then remove all the junction points to generate $N$ disjoint centerline segments $\Gamma_j$ indexed by $1 \leq j \leq N$. Fig. [8](#fig_CurvaturePrior){reference-type="ref" reference="fig_CurvaturePrior"}a illustrates those discrete centerline segments using different colors. From them one can also construct $N$ disjoint tubular neighbourhood regions $\mathcal T_j\subset\Omega$ for $1\leq j \leq N$ in terms of Euclidean distances. This is to say $$\begin{equation}
\mathcal T_j=\{\mathfrak p\in \Omega~|~d(\mathfrak p,\Gamma_j)<d(\mathfrak p,\Gamma_i),\,\forall i\neq j\},
\end{equation}$$ where $d(\mathfrak p,\Gamma_j)$ denotes the Euclidean distance between a physical position $\mathfrak p$ and the discrete centerline segment $\Gamma_j$. In this way, one can point out that for any $i \neq j$, the neighbourhoods $\mathcal T_i$ and $\mathcal T_j$ are disjoint, i.e., $\mathcal T_i\cap  \mathcal T_j=\emptyset$. In Fig. [8](#fig_CurvaturePrior){reference-type="ref" reference="fig_CurvaturePrior"}b, we illustrate an example of these disjoint neighbourhood regions.

In the open bounded and connected domain $\mathcal T_j$, each individual discrete centerline segment $\Gamma_j$ can provide two endpoints $\mathfrak p_j,\,\mathfrak q_j\in\Omega$, i.e. an endpoint only has a single neighbouring point. With these definitions in hands, we attempt to minimize the following path energy in order to track the path $\mathcal G_j$ $$\begin{equation}
\label{eq_CurvatureEnergy}
\int_0^1\mathcal C(\gamma(t),\eta(t))\mathfrak{C}(\xi\kappa(t))dt,\quad\text{subject to}~
\begin{cases}
\gamma(0)=\mathfrak p_j,&\\
\gamma(1)=\mathfrak q_j,&\\
\gamma(t)\in \mathcal T_j,&~\forall t\in[0,1]. 
\end{cases}
\end{equation}$$ where $\mathcal C$ is the image data-driven cost function, $\mathfrak{C}$ is a cost of the path curvature $\kappa$ and $\xi>0$ is a weighting parameter on the curvature. More specifically, we define the data-driven cost function $\mathcal C$ as follows: $$\begin{equation*}
\mathcal C(\mathfrak p,\theta)=\exp\left(-\beta\alpha(\mathfrak p,\theta)\right),
\end{equation*}$$ for any physical position $\mathfrak p\in\Omega$ and any angular coordinate $\theta\in\mathbb S^1$. One can point out that the cost $\mathcal C$ is a decreasing function of the orientation scores $\alpha$. It is also used as the data-drive cost function of the proposed bounded Elastica model. Moreover, the curvature cost function $\mathfrak{C}$ is dependent to the curvature-penalized minimal path model considered. For instances, the cost $\mathfrak{C}(a)=1+a^2$ for any $a\in\mathbb R$ corresponds to the Euler-Mumford elastica model [@chen2017global; @mirebeau2018fast] and $\mathfrak{C}(a)=\sqrt{1+a^2}$ corresponds to the Reeds-Shepp optimal curve model [@duits2018optimal].

The minimization of the weighted curve length defined in [\[eq_CurvatureEnergy\]](#eq_CurvatureEnergy){reference-type="eqref" reference="eq_CurvatureEnergy"} can be implemented via the HJB PDE framework. Specifically,one can estimate the minimal action map $\mathcal U_j$ by addressing the HJB PDE by the Hamiltonian Fast-Marching method [@mirebeau2018fast] or by the GPU-implemented way [@mirebeau2023massively]. Then a gradient descent procedure is performed on the minimal action map $\mathcal U_j$ to track the minimal path $\mathcal G_j=(\gamma_j,\eta_j)$ lying inside the corresponding tubular neighbourhood $\mathcal T_j$. Note that during the estimation of the minimal action map $\mathcal U_j$, the set $\partial\mathcal T_j\times\mathbb S^1$ of the tubular neighbourhood is used as a wall to limit the distance propagation within the domain $\mathcal T_j \times \mathbb S^1$. In Fig. [8](#fig_CurvaturePrior){reference-type="ref" reference="fig_CurvaturePrior"}, we illustrate this procedure using the image data shown in Fig. [7](#fig_OS){reference-type="ref" reference="fig_OS"}a.

## The Computation of the Curvature Prior Map $\varpi$ {#the-computation-of-the-curvature-prior-map-varpi .unnumbered}

Once all the minimal paths $\mathcal G_j=(\gamma_j,\eta_j)$ are generated, we can estimate their curvature $\kappa_j$ of each physical projection curve $\gamma_j$ as follows: $$\begin{equation*}
\kappa_j(u)=\frac{\eta_j^\prime(u)}{\|\gamma_j^\prime(u)\|},
\end{equation*}$$ for any parameter $u\in[0,1]$.

Eventually, we follow the method introduced in the literature [@chen2023computing] to compute the curvature prior map $\varpi:\mathbb M\to\mathbb R$ using the computed physical projection curves $\{\gamma_j\}_j$ and their curvature $\{\kappa_j\}_j$, as shown in Fig. [8](#fig_CurvaturePrior){reference-type="ref" reference="fig_CurvaturePrior"}d. In this figure, the values of $\kappa_j$ are visualized by different colors, where the red arrows indicate the parameterization of the respective planar components $\gamma_j$ of the minimal paths $\mathcal G_j$. Following [@chen2023computing], we define by $0\leq\Lambda\leq \min_j\{\|\kappa_j\|^{-1}_\infty\}$ a bounding parameter and let $\mathcal N_j$ be the unit normal to the curve $\gamma_j$. Then one can construct the curvature prior map $\varpi$ by $$\begin{equation*}
\varpi(\mathfrak p,\theta)=
\begin{cases}
\kappa(u)\mathop{\mathrm{sign}}\left(\langle\mathrm{n}(\theta),\mathrm{n}(\eta_j(u)) \rangle\right),&\text{if~}\mathfrak p\in\mathcal T_j~\text{and}~\mathfrak p=\gamma_j(u)+\lambda\mathcal N_j(u),\,\forall\lambda\in[-\Lambda,\Lambda]\\
0,&\text{otherwise}.
\end{cases}
\end{equation*}$$ or by $$\begin{equation*}
\varpi(\mathfrak p,\theta)=
\begin{cases}
\kappa(u)\langle\mathrm{n}(\theta),\mathrm{n}(\eta_j(u)) \rangle,&\text{if~}\mathfrak p\in\mathcal T_j~\text{and}~\mathfrak p=\gamma_j(u)+\lambda\mathcal N_j(u),\,\forall\lambda\in[-\Lambda,\Lambda]\\
0,&\text{otherwise}.
\end{cases}
\end{equation*}$$ Note that $\gamma_j+\lambda\mathcal N_j$ represent an offset curve of $\gamma_j$. We refer to the literature [@chen2023computing] for more detail on the computation of the curvature prior map $\varpi$.

# The Dubins Model with Extended Curvature Bounds

In contrast to the introduced bounded Elastica model which takes into account arbitrary curvature bounds as a geometric prior, the Dubins model [@mirebeau2018fast] alternatively invokes a boundedness limitation to the absolute path curvature. As introduced in the work [@mirebeau2018fast], the Hamiltonian $\mathfrak H^{\rm D}$ of the original Dubins model is formulated as $$\begin{align}
\label{eq_DubinsHamiltonian}    
\mathfrak H^{\rm D}(\mathbf p,\hat{\mathbf{p}})&=\frac{1}{2}\max\left\{0,\,\left\langle\hat{\mathbf{p}},\left(\mathrm{n}(\theta),\xi^{-1}\right) \right\rangle,\left\langle\hat{\mathbf{p}},\left(\mathrm{n}(\theta),-\xi^{-1}\right)\right\rangle\right\}^2\nonumber\\
&=\frac{1}{2}\max\left\{\left\langle\hat{\mathbf{p}},\left(\mathrm{n}(\theta),\xi^{-1}\right) \right\rangle_+,\left\langle\hat{\mathbf{p}},\left(\mathrm{n}(\theta),-\xi^{-1}\right)\right\rangle_+\right\}^2
\end{align}$$ for any point $\mathbf p=(\mathfrak p,\theta)\in\mathbb M$ and for any co-vector $\hat{\mathbf{p}}=(\hat{\mathfrak{p}},\hat\theta)\in\mathbb R^2\times\mathbb R$.

The control set $\mathfrak B^{\rm D}$ of the Dubins model can be formulated as follows [@mirebeau2018fast] $$\begin{align*}
\mathfrak B^{\rm D}(\mathbf p)=&\left\{(\dot{\mathfrak p},\dot\theta);\xi|\dot\theta|\leq\|\dot\mathfrak p\| \leq 1,\dot\mathfrak p=\|\dot\mathfrak p\|\mathrm{n}(\theta)\right\}\\
=&\left\{a\mathrm{n}(\theta),b\xi^{-1});0\leq |b|\leq a \leq 1\right\}.
\end{align*}$$ As discussed in [@mirebeau2018fast], the control set $\mathfrak B^{\rm D}(\mathbf p)$ is a triangle whose vertices are $\mathbf{0}$, $(\mathrm{n}(\theta),1/\xi)$ and $(\mathrm{n}(\theta),-1/\xi)$. For any minimal path $\mathcal G=(\tilde\gamma,\tilde\eta):[0,1]\to\mathbb M$, the curvature $\tilde\kappa=\tilde\eta^\prime/\|\tilde\gamma^\prime\|$ satisfies $$\begin{equation*}
\tilde\kappa(u)\in\left[-\xi^{-1},\xi^{-1}\right],\quad \forall u\in[0,1]
\end{equation*}$$ Furthermore, for the purpose of visualization, we consider the following sliced control sets $$\begin{equation*}
\tilde{\mathfrak B}^{\rm D}(\mathbf p)=\{(\dot\nu,\dot\theta)\in\mathbb R^2;\dot\nu>0,(\dot\nu\mathrm{n}(\theta),\dot\theta)\in\mathfrak B^{\rm D}(\mathbf p)\},
\end{equation*}$$ where we recall that $\mathrm{n}(\theta)$ is defined as $\mathrm{n}(\theta)=(\cos\theta,\sin\theta)$. In Fig. [9](#fig_DubinsControlSet){reference-type="ref" reference="fig_DubinsControlSet"}, we illustrate the sliced control set $\mathfrak B^{\rm D}(\mathbf p)$ at a point $\mathbf p$, constructed with parameters $\xi=1$, $\xi=2$ and $\xi=3$.

In this original Dubins model, the constraint imposed to the absolute path curvature is implemented via the constant parameter $\xi$. However, such a setting may lose the information from the image data. As pointed out in the literature [@mirebeau2019hamiltonian], the constant parameter $\xi$ can be extended as a pointwise function regarded as the absolute curvature bounds of the Dubins car model. For this purpose, we consider a scalar-valued positively-defined function $\mathcal K:\mathbb M\to\mathbb R^+$, defined by $$\begin{equation}
\label{eq_DubinsBounds}
\mathcal K(\mathbf p)=\max\bigl\{|\Im_{\rm min}(\mathbf p)|,\,|\Im_{\rm max}(\mathbf p)|\bigr\},
\end{equation}$$ where $\Im_{\rm min},\Im_{\rm max}:\mathbb M\to\mathbb R$ are the curvature bounds used in the introduced bounded Elastica model.

:::: {#fig_OS .figure latex-placement="htbp"}
![](Chen2026Computing_figs/fig7.png){width="90%"}

::: caption
Visualization for the orientation scores of curvilinear structures. (**a**) The raw image for estimating the orientations score map by the optimally oriented flux filter as introduced in the literature [@law2008three]. The red and blue dots represent two sampled points, which are respectively located at the curvilinear structure and at the background. (**b**) Visualization of orientation scores $\alpha(x,\theta)$ at three slices with respect to three sampled angles $\theta=\pi/6,\,\pi/2$ and $\pi$. (**c**) Plots of the normalized orientation score values $\alpha$ at two sampled points, where the red and blue lines represent the values of $\alpha$ at the red and blue dots in figure (a), respectively.
:::
::::

:::: {#fig_CurvaturePrior .figure latex-placement="htbp"}
![](Chen2026Computing_figs/fig8.png){width="95%"}

::: caption
Illustration for the computation of the curvature prior map $\varpi$. (**a**) Visualization of the piecewise disjoint discrete centerline segments $\Gamma_j$ via different colors. **b** Visualization for the disjoint tubular neighbourhood regions $\mathcal T_j$. Note that for better visualization we slightly enlarge the width of each tubular neighbourhood region. **c** Visualization for the planar components $\gamma_j$ of the smooth paths $\mathcal G_j$, each of which fits to the discrete centerline segments. **c** The computed curvature of each fitting path. The red arrows indicate the respective parameterization directions of the physical projection curves $\gamma_j$ of the fitting minimal paths.
:::
::::

:::: {#fig_DubinsControlSet .figure latex-placement="htbp"}
![](Chen2026Computing_figs/fig9.png){width="90%"}

::: caption
Illustration for the sliced control sets $\tilde{\mathfrak B}^{\rm D}(\mathbf p)$ of the Dubins model with different values of the parameter $\xi$. The red dots are the origins $(0,0)$ of the sliced control sets. (**a**) - (**c**) The sliced control sets with respect to $\xi=1$, $\xi=2$ and $\xi=3$, respectively.
:::
::::
