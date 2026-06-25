---
citation_key: Tedrake2019Computing
arxiv_id: 1901.03922
arxiv_url: "https://arxiv.org/abs/1901.03922"
title: "Computing Large Convex Regions of Obstacle-Free Space via Semidefinite Programming"
authors_short: "Deits and Tedrake"
year: 2019
direction_tag: I_corridor_planning
source: mineru-vlm
converter: mineru-open-api
model: vlm
converted_at: 2026-06-25T09:49:30Z
origin: ai+web
reviewed: false
---

# Nonlinear Waves in an Experimentally Motivated Ring-shaped Bose-Einstein Condensate Setup

M. Haberichter,<sup>1,</sup> <sup>∗</sup> P. G. Kevrekidis,<sup>1</sup> R. Carretero-Gonz´alez,<sup>2</sup> and M. Edwards<sup>3,</sup> <sup>4</sup> <sup>,</sup> <sup>†</sup>

<sup>1</sup>Department of Mathematics and Statistics, University of Massachusetts, Amherst, Massachusetts 01003-4515, USA <sup>2</sup>Nonlinear Dynamical Systems Group,<sup>‡</sup> Computational Sciences Research Center, and Department of Mathematics and Statistics, San Diego State University, San Diego, California 92182-7720, USA <sup>3</sup> Department of Physics, Georgia Southern University, Statesboro, Georgia 30460-8031, USA <sup>4</sup> Joint Quantum Institute, National Institute of Standards and Technology and the University of Maryland, Gaithersburg, Maryland 20899, USA (Dated: January 15, 2019)

We systematically construct stationary soliton states in a one-component, two-dimensional, repulsive, Gross-Pitaevskii equation with a ring-shaped target-like trap similar to the potential used to confine a Bose-Einstein condensate in a recent experiment [Eckel, et al. Nature 506, 200 (2014)]. In addition to the ground state configuration, we identify a wide variety of excited states involving phase jumps (and associated dark solitons) inside the ring. These configurations are obtained from a systematic bifurcation analysis starting from the linear, small atom density, limit. We study the stability, and when unstable, the dynamics of the most basic configurations. Often these lead to vortical dynamics inside the ring persisting over long time scales in our numerical experiments. To illustrate the relevance of the identified states, we showcase how such dark-soliton configurations (even the unstable ones) can be created in laboratory condensates by using phase-imprinting techniques.

PACS numbers:

## I. INTRODUCTION

Atomic Bose-Einstein condensates (BECs) [1–4] ofer an ideal testing ground for confronting theoretical models of nonlinear matter waves with experimental data. Since their experimental realization, there have been tremendous advances [4–8] in trapping, guiding, manipulating and controlling BECs. For instance, recent advances in all-optical trapping [9–11] have produced confined atomic clouds with temperatures at the nanokelvin scale. Alloptical trapping, in turn, has enabled the strength of the atom-atom interactions in atomic gas BECs to be tuned to any desired value over many orders of magnitude [12] by adjusting an external magnetic field through the phenomenon of the Feshbach resonance [13]. This enables a wide range of experiments to be conducted because the properties of BECs —as well as the nature of their efective nonlinearity— crucially depend on the strength and sign of these interactions.

These advances have led to more stable, easier to use experimental settings and high-precision measurements of coherent structures in BECs. In a plethora of experiments, matter-wave dark [14] and bright [15–19] solitons have been realized in single- and multi-component BECs with repulsive or attractive interatomic interactions, respectively. For example, bright solitons have been formed in ultracold <sup>7</sup>Li gas [17, 18] as well as during the collapse of <sup>85</sup>Rb condensates [19]. Dark solitons have been studied in <sup>87</sup>Rb condensates [20–23] and in sodium BECs [24, 25]. Furthermore, coupled dark-bright solitons have been engineered in <sup>87</sup>Rb condensates using phaseimprinting methods [22] or generated during superfluidsuperfluid counterflow [26, 27]. Finally, matter wave gap solitons [28, 29] have been produced in BECs trapped in light-induced periodic potentials.

At the theoretical level, and for suficiently low temperatures, static and dynamical properties of BECs have been quite successfully modeled by an efective meanfield equation known as the Gross-Pitaevskii equation (GPE) [1, 2, 30]. The GPE is tantamount to a (cubic) nonlinear Schr¨odinger (NLS) equation with the addition of the external potential that confines the BEC. The (2 + 1)-dimensional version of the fully 3D equation reads, in terms of physical units, as

$$
i \hbar \partial_ {t} \Phi = \Big [ - \frac {\hbar^ {2}}{2 m} \nabla^ {2} + g _ {\mathrm{2D}} | \Phi | ^ {2} + V (\pmb {r}) \Big ] \Phi ,\tag{1}
$$

where $\Phi ( \boldsymbol { r } , t )$ is the macroscopic BEC wavefunction, <sup>2</sup> is the Laplacian in $\boldsymbol { r } = ( x , y )$ , m is the atomic mass and g<sub>2D</sub> describes the efective 2D strength of the atom-atom interaction. The efective 2D coupling constant g<sub>2D</sub> is given by $g _ { \mathrm { 2 D } } = g / ( \sqrt { 2 \pi } a _ { z } ) = 2 \sqrt { 2 \pi } \hbar a _ { z } \omega _ { z } a$ , where $\omega _ { z }$ is the harmonic trapping strength in the transverse direction, with a<sub>z</sub> being its corresponding harmonic oscillator length. The 3D coupling constant is $g = 4 \pi \hbar ^ { 2 } a / m$ , where a is the s-wave scattering length.

In the following, we set $g _ { \mathrm { 2 D } } > 0$ , that is the nonlinearity in the GPE is chosen to be defocusing [30–32] which models a repulsive interatomic interaction, as is the case, e.g., in <sup>87</sup>Rb. Multiple stationary dark-soliton states can emerge when the repulsion between dark solitons is counterbalanced by the inclusion of a trapping potential $V ( r )$ in Eq. (1). The existence and formation of nonlinear patterns in BECs crucially depend on the chosen form for the applied trapping potential $V ( r )$ . The traditionally used magnetic traps can be adequately modeled by an harmonic external potential of the form [6, 33]

$$
V = \frac {1}{2} m \left(\omega_ {x} ^ {2} x ^ {2} + \omega_ {y} ^ {2} y ^ {2}\right),\tag{2}
$$

where, for generality, the trap frequencies $\omega _ { x }$ and $\omega _ { y }$ along the x- and y-direction can be chosen to be diferent. Static and dynamical properties of matter-wave dark solitons have been investigated in great detail in model (1) with the parabolic confining potential (2) and higherdimensional analogues thereof. For example, dark soliton stripes and multivortex states such as vortex dipoles, tripoles, and quadrupoles have been found [34, 35] and their existence, stability and dynamics have been discussed in detail in the literature [36, 37].

However, in recent years there has been increasing research activity in exploring diferent choices (specifically non-parabolic ones) for the external trapping potential in Eq. (1). Examples of trapping configurations recently used in BEC experiments include: double [38–44], and more-well (such as four-well [45]) potentials, box potentials [2], optical lattice potentials [2, 46, 47], or magnetic quadrupole trap combined with an optical dipole trap [48], among many others.

In this article, we wish to explore the existence and stability of localized states in the two-dimensional (2D) GPE (1) with a ring-shaped trapping potential and repulsive interatomic interactions. A key feature of our work is the identification of a wide variety of nonlinear states in this system including ones bearing diferent numbers of phase jumps and associated dark solitons. The bifurcation analysis of such stationary solutions is complemented by the corresponding stability analysis, and the dynamical evolution of potentially unstable configurations. Equally importantly, phase imprinting protocols are utilized in suitably crafted numerical experiments in order to illustrate the potential of such states towards being realized in recently considered experimental setups.

More specifically, our considerations are tailored the recent experimental setup of atomtronic systems [49, 50], that are confined, neutral, ultracold atomic gases which exhibit behavior analogous to semiconductor electronic devices and circuits. In atomtronics, ring BECs are used [51–53] to realize atomic-gas analogs of superconducting quantum interference devices (SQUIDs). In Ref. [51], a closed-loop atom circuit was implemented for the first time in a ring-shaped confining potential. Rf SQUIDs [54] have been created [52] in ring BECs by rotating a weak link (a localized region of reduced superfluid density) around the ring-shaped condensate. A rotating weak link was used to drive phase slips which changed the circulation around the ring and simulations, based on the GPE, showed how the circulation of the ring BEC can be probed by measuring the distribution of hole areas in time-of-flight images [53]. We also note in passing that ring-shaped BECs have been recently argued [55] as an interesting laboratory testbed for cosmological physics.

The article is structured as follows. In Sec. II we briefly review some of the properties of the GPE in (2 + 1) dimensions and introduce the chosen ring-shaped trapping potential. For a detailed discussion of the existence and stability analysis of steady-state solutions in the 2D GPE with repulsive interactions we refer the interested reader to the reviews and textbooks [3, 30, 31]. Our numerical results are reported in Sec. III. Finally, in Sec. IV, we summarize our conclusions and discuss possible directions for further work.

## II. MODEL AND METHODOLOGY

To simplify our numerical calculations, we rewrite Eq. (1) in its well-known dimensionless form [3, 30]

$$
i \partial_ {t} \Phi = - \frac {1}{2} \nabla^ {2} \Phi + | \Phi | ^ {2} \Phi + V (\pmb {r}) \Phi ,\tag{3}
$$

where $\Phi = \Phi ( x , y )$ is the 2D wavefunction and $\nabla ^ { 2 }$ is the Laplacian in $\boldsymbol { r } = ( x , y )$ . Equation (3) is obtained from Eq. (1) by averaging (integrating) along the z-direction and rescaling space coordinates by the the transverse oscillator length $a _ { z }$ and time by $\omega _ { z } ^ { - 1 }$ . Then, the density $| \Phi | ^ { 2 }$ , length, time and energy are respectively measured in units of $( 2 \sqrt { 2 \pi } a a _ { z } ) ^ { - 1 }$ , the harmonic oscillator length $a _ { z } = \sqrt { \hbar / ( m \omega _ { z } ) }$ , the inverse trap frequency $\omega _ { z } ^ { - 1 }$ and energy $\hbar \omega _ { z }$

![](Tedrake2019Computing_figs/e4350609cec4db49de6cca2c750ee29c30ba18e5cf83d1f608742a2fdb7ee25b.jpg)  
FIG. 1: (Color online) Ring-shaped trapping potential V , given in Eq. (4), corresponding to an experiment performed at NIST [56]. In this figure, and all subsequent ones, space $( x , y )$ is displayed using physical units (in microns).

We choose an external trapping potential as experimentally obtained from a fit provided by NIST experimentalists corresponding to a ring-shaped channel of mean radius $r _ { \mathrm { r i n g } }$ together with a central well of radius $r _ { \mathrm { d i s k } } .$ . Stationary ground-state condensates filling this potential (see Fig. 1) consist of a central disk surrounded by a ring thus motivating the names $r _ { \mathrm { d i s k } }$ and $r _ { \mathrm { r i n g } } \ [ 5 6 , 5 7 ]$ This potential has the flexibility to be either a ring-plusdisk or just a ring. In the case where a ring is present, the disk can be used as a phase reference to detect phase variations in the ring caused by, e.g., stirring. Specifically, the fitted potential from the experiments takes the radial form:

$$
V (r) = \left\{ \begin{array}{l l} 1 - A e ^ {- \frac {(r - r _ {\text {ring}}) ^ {2}}{s _ {\text {ring}} ^ {2}}} - e ^ {- \frac {(r - r _ {\text {disk}}) ^ {2}}{s _ {\text {disk}} ^ {2}}} & r \geq r _ {\text {disk}} \\ - A e ^ {- \frac {(r - r _ {\text {ring}}) ^ {2}}{s _ {\text {ring}} ^ {2}}} & r <   r _ {\text {disk}}, \end{array} \right.\tag{4}
$$

where $r _ { \mathrm { r i n g } } ,$ A and $s _ { \mathrm { r i n g } }$ represent, respectively, the radius, the amplitude and the width of this ring-shaped potential. The experimentally fitted potential parameters correspond to: $r _ { \mathrm { r i n g } } = 2 2 . 2 7 ~ \mu \mathrm { m } , \ : r _ { \mathrm { d i s k } } = 2 . 5 9 7$ µm, $s _ { \mathrm { r i n g } } = 3 . 9 1 3 ~ \mu \mathrm { m } , s _ { \mathrm { d i s k } } = 4 . 7 1 7 ~ \mu \mathrm { m }$ , and $A = 0 . 8 2 0 6$ . Expressed in terms of the dimensionless units of Eq. (3), based on a transverse trap frequency $\omega _ { z } / 2 \pi ~ = ~ 5 0 0$ $\mathrm { H z } ,$ these quantities correspond to: $r _ { \mathrm { r i n g } } = 2 5 . 3 0 4 7 3 8$ 2 $r _ { \mathrm { d i s k } } = 2 . 9 5 0 8 9 , s _ { \mathrm { r i n g } } = 4 . 4 4 6 2 2 6 , s _ { \mathrm { d i s k } } = 5 . 3 5 9 7 8 6 7$ , and $A = 0 . 8 2 0 6 .$ . A plot of the resulting ring-shaped potential is displayed in Fig. 1. Note that for ease of interpretation, we opt to display in this figure, and all subsequent ones, the spatial dimensions in the original variables, namely in microns.

Let us now construct stationary solutions of $\operatorname { E q } .$ (3) by separating space and time according to

$$
\Phi (\pmb {r}, t) = \phi (\pmb {r}) e ^ {- i \mu t},\tag{5}
$$

where $\mu$ is the (dimensionless) chemical potential. Substituting ansatz (5) into the 2D GPE (3) yields the steady-state equation

$$
- \frac {1}{2} \nabla^ {2} \phi + | \phi | ^ {2} \phi + [ V (x, y) - \mu ] \phi = 0.\tag{6}
$$

Steady-state solutions for Eq. (6) correspond to monoparametric branches parametrized by the chemical potential $\mu$ which, in turn, fixes the number of BEC atoms in the condensate. This relationship is obtained through the conserved quantity of the GPE corresponding to the (squared) $L ^ { 2 }$ norm of the solution:

$$
N = \iint_ {- \infty} ^ {+ \infty} | \phi (x, y) | ^ {2} d x d y.\tag{7}
$$

Thus, after bringing back the dimensions into Eq. (7), N can be identified with the mass or total number of atoms in the BEC. In what follows we find suitable starting points on a given solution branch and then vary $\mu$ using continuation methods to follow the entire branch possibly leading to bifurcations (when two solution branches collide or when new branches emanate from existing ones) as the chemical potential $\mu$ is varied [37, 58]. For given chemical potential $\mu ,$ we find stationary nonlinear solutions to Eq. (6) by using two diferent implementations of

Newton algorithms. Details on these numerical methods are found in Sec. III.

After having numerically computed solutions, for each chosen value of $\mu ,$ we proceed to study their instability modes by performing the well-known Bogoliubovde Gennes (BdG) stability analysis [1–3]. We perturb around a stationary solution $\phi _ { 0 }$ using the perturbation ansatz

$$
\phi (\boldsymbol {r}) = \phi_ {0} (\boldsymbol {r}) + \left[ a (\boldsymbol {r}) e ^ {i \omega t} + b ^ {\star} (\boldsymbol {r}) e ^ {- i \omega^ {\star} t} \right],\tag{8}
$$

where $( \cdot ) ^ { \star }$ denotes complex conjugation and ω is a complex eigenfrequency. Linearization of the GPE (3) around the stationary solution $\phi _ { 0 }$ via the ansatz (8) yields the following BdG eigenvalue problem

$$
- \omega \binom{a}{b} = \left( \begin{array}{c c} A _ {1 1} & A _ {1 2} \\ - A _ {1 2} ^ {\star} & - A _ {1 1} \end{array} \right) \binom{a}{b},\tag{9}
$$

where the matrix elements are explicitly given by

$$
A _ {1 1} = - \frac {1}{2} \nabla^ {2} + 2 | \phi_ {0} | ^ {2} + V (x, y) - \mu .\tag{10a}
$$

$$
A _ {1 2} = (\phi_ {0}) ^ {2}.\tag{10b}
$$

We compute the eigenfunctions $\{ a ( x , y ) , b ( x , y ) \}$ and eigenfrequencies $\omega$ of the BdG eigenvalue problem (9) for a steady-state solution φ<sub>0</sub> and for a given value $\mu$ using the eigs MATLAB routine [59, 60] and our results are further checked with the Scalable Library for Eigenvalue Problem Computations (SLEPc) [61–63]. The BdG stability results are then depicted in terms of the corresponding spectra by plotting the real and imaginary parts of the eigenfrequencies as a function of $\mu .$ Recall that for a linearly (neutrally) stable soliton configuration, all eigenfrequencies must be real, that is Im $( \omega ) = 0$

## III. NUMERICAL SIMULATIONS

Our numerical results are based on discretizing the ensuing nonlinear equations —for the dynamics Eq. (3), for the steady states Eq. (6), and for the BdG spectra eigenvalue problem Eq. (9)— on the rectangular, uniform, 2D grid $( x , y ) \in [ - 5 0 , 5 0 ]$ and with grid spacing $\Delta x = 0 . 2$ The steady-state equation (6) is solved using a Newton-Krylov algorithm [64] and then, the obtained states are checked using Newton iterations implemented in the SNES libraries of PETSc [65–67].

In order to pick a suitable initial guess for convergence towards the steady state we use the first few solutions close to the linear limit. The linear limit, corresponding to weak nonlinearities in Eq. (9), may be formally identified with $N  0$ . Then, stationary states for larger values of $\mu$ are obtained via numerical continuation by taking as initial guess the configuration calculated at nearby chemical potential values. The numerical results presented below were carried out with the chemical potential $\mu$ varying over the interval [0, 1] with steps of $\Delta \mu = 0 . 0 0 2$ . If not otherwise stated, all configurations depicted here correspond to the chemical potential $\mu = 0 . 9$

![](Tedrake2019Computing_figs/752ee9f8f3aa8a2209b9def963fefaaf5aa091e814a144081a1ae9681a4bb45b.jpg)  
FIG. 2: (Color online) Ground state and n-dark soliton solutions for $\mu = 0 . 9$ . The real part and density of the solutions are depicted, respectively, in the top and bottom rows of panels. (a) Ground state (that populates the central well of the external potential). (b) Basic ring state without any dark solitons. $\mathrm { ( c ) - ( e ) }$ First 3 excited states along the ring containing, respectively, two, four, and six dark solitons. All these stationary solutions are purely real.

Further insights into the dynamical properties and stability of the found steady states can be obtained by perturbing these solutions with the eigenvectors, computed in the BdG linearization analysis (9), and studying their temporal evolution. To simulate the time evolution based on Eq. (3), we employ a fourth order Runge-Kutta integrator in time with a second-order finite diferences used for the discretization of the spatial derivatives.

## A. States bifurcating from the linear limit

The most basic steady state is given by the ground state. For our system with the potential given in Eq. (4), the ground state emerging from the linear limit simply corresponds to a localized “hump” of atoms that populate the central well of the potential (see panels (a) in Fig. 2). The corresponding particle number (or mass) for the ground state branch as a function of the chemical potential is depicted in Fig. 3 (see line denoted by GS). It is interesting to note that the ground state does not populate the ring of the external potential. In fact the ring does not get populated until $\mu$ reaches $\mu \simeq \mu _ { \mathrm { c r i t } } ^ { ( 0 ) } = 0 . 3 1 3$ For $\mu \geq \mu _ { \mathrm { c r i t } } ^ { ( 0 ) }$ a new state emerges from the linear, $N \simeq 0$ , limit that starts filling the ring with atoms (see panels (b) in Fig. 2). This ring-shaped solution would correspond to the ground state if the central well was absent. The mass for this ring state is depicted in Fig. 3 (see line denoted by 0S). Since this ring state could be considered as a quasi-1D periodic line of density, it is possible to think about the configurations stemming from its excited states.

For instance, in an infinite 1D line density, in the absence of external potential, the repulsive GPE admits a dark soliton solution [3, 30] corresponding to the first excited state. In the case of the ring line density, the wavefunction necessarily has to be periodic along the ring.

![](Tedrake2019Computing_figs/d4f75b8779fd629f217846b5ff01b8c17c71ab873a07a321cd8daeb191e719a5.jpg)  
FIG. 3: (Color online) Particle number N as a function of $\mu$ for the ground state (GS) and the n-soliton (nS) stationary steady states. These steady states are obtained by continuation from the $N \simeq 0$ limit where the solutions are calculated by taking an initial guess in our fixed point iterations corresponding to the first few eigenfunctions (excited states) in the linear limit. The critical chemical potential values µ<sub>crit</sub> at which the diferent states are found to emerge correspond to $\mu _ { \mathrm { c r i t } } ^ { ( 0 ) } = 0 . 3 1 3$ for 0S, $\mu _ { \mathrm { c r i t } } ^ { ( 2 ) } = 0 . 3 1 4$ for 2S, $\mu _ { \mathrm { c r i t } } ^ { ( 4 ) } = 0 . 3 1 6$ for 4S, $\mu _ { \mathrm { c r i t } } ^ { ( 6 ) } = 0 . 3 2 0$ for 6S, and $\mu _ { \mathrm { c r i t } } ^ { ( 8 ) } = 0 . 3 2 6$ for 8S. The corresponding profiles for these solutions for $\mu = 0 . 9$ are depicted in Fig. 2.

This topological constraint restricts the number of dark solitons that can be excited along the ring to be an even number. With an even number of dark solitons along the ring, periodic boundaries are automatically satisfied.

We show these n-soliton steady-state solutions in Fig. 2 for $n = 0$ (the ring state without any solitons), $n = 2$ (a pair of dark solitons), $n = 4$ (two dark soliton pairs), and $n = 6$ (three dark soliton pairs). Note that, due to symmetry, in the steady state all the dark solitons must be equidistant from each other along the periodic ring. The particle numbers corresponding to these n-soliton solutions are depicted in Fig. 3. Note that the n-dark soliton solutions, populating the ring, bifurcate from the linear limit $( N \simeq 0 )$ and are independent of the ground state that populates the central well.

## B. States bifurcating from the ground state

We also explored states bifurcating from the ground state. In particular, at $\mu \approx 0 . 5 6 0 \mathrm { ~ a ~ }$ double-ring solution bifurcates away from the ground state. This doublering (see panels (a) in Fig. 4) contains the ground state populating the central well coupled to two out-of-phase rings, that populate the ring portion of the external potential, as can be seen in the top panel of Fig. 4(a) — depicting the real part of the solution— where the phase diference between the inner and outer rings is evident. Namely, this state efectively contains a ring dark soliton [14, 30, 68] inside the outside ring channel. Figure 6 depicts the BdG spectra for the ground state and the double-ring state as a function of $\mu .$ . As expected, the ground state is always (neutrally) stable. However, as it is clear from the figure, the double ring is unstable since its inception. It is relevant to note that this has been recently demonstrated to be generically the case due to their azimuthal undulations in the presence of an external radial potential with the quadrupolar undulations representing the first among such spatial modes that becomes unstable [69].

![](Tedrake2019Computing_figs/4aa914fe74ab95341044faf7e75b689cbfabd7fc50e86ffa3a43d01ab4045724.jpg)  
FIG. 4: (Color online) Double-ring solution and some of its bifurcating states for $\mu = 0 . 7 .$ . (a) Double ring solution (that bifurcated from the ground state) consisting of two concentric out-of-phase rings. (b)–(d) Successive states bifurcating away from the double-ring solution. The corresponding particle numbers for these solutions as a function of $\mu$ are depicted in Fig. 5. Same layout as in Fig. 2.

![](Tedrake2019Computing_figs/fb1607f237f1a5adcb3f4eb29070be68c63f1680afb6f790ffeddf6ed3558dfd.jpg)  
FIG. 5: (Color online) Particle number $N$ as a function of $\mu$ for ground state (GS), the double-ring (a) and its first three bifurcating branches (b)–(d). The corresponding profiles for $\mu = 0 . 7$ are depicted in Fig. 4. These double-ring bifurcates from the ground state at $\mu \simeq 0 . 5 6 0$ , while the subsequent states bifurcate in turn from the double-ring solution for (b) $\mu = 0 . 5 8 6$ , (c) 0.618, and (d) 0.708.

Interestingly, there exist further states bifurcating in turn from the double-ring solution. These states, depicted in panels (b)–(d) in Fig. 4, correspond to the double-ring with out-of-phase “petals” along the azimuthal direction. The bifurcation progression of the double-ring from the ground state and, subsequently, the states bifurcating from the double-ring is more evidently portrayed in Fig. 5 that depicts the particle numbers for these solutions as a function of $\mu .$ It is relevant to note that, apparently, configurations with higher number of petals bifurcate first from the double-ring. This bifurcation cascade continues beyond what is shown in Fig. 4 (where only the first couple of bifurcating branches are depicted).

![](Tedrake2019Computing_figs/d1293ca24edcc8f42c4bc46bc202b4db0a4711eb9a94c14883114021cbe82fdc.jpg)

![](Tedrake2019Computing_figs/45cbf5439d7cc82215794086819e38196f4c72e8527eb5b2bb86aa98c6eb5e7d.jpg)

![](Tedrake2019Computing_figs/89f27ee6698de7c1c66c7822827ff55626073773954c1bb13ec3e9f521edb21e.jpg)

![](Tedrake2019Computing_figs/43fcdb2841037b5e991a22df746c3079f4063c910ebe78c2e05403e97a82f109.jpg)  
FIG. 6: (Color online) Stability BdG spectra for the ground state (top row of panels) and the double-ring state (bottom row of panels) as a function of the chemical potential $\mu .$ The corresponding profiles are depicted in the first row of panels of, respectively, Fig. 2 and Fig. 4. The left and right panel depict, respectively, the real and imaginary parts of the spectra. Recall that (neutral) stability is only achieved when ${ \mathrm { I m } } ( \omega ) = 0$ . The ground state is always (neutrally) stable while the double-ring state is, since its inception, always unstable.

As concerns the stability of the bifurcating states, it is important to stress that the double-ring solution is unstable since its emergence from the ground state around $\mu \simeq 0 . 5 6 0$ and, therefore, all the subsequent bifurcating states from the double-ring inherit the instability from their double ring “ancestor” and are thus always unstable as well. Furthermore, it is interesting to note that the the first few instabilities seen in the BdG spectrum of the double ring (bottom-right panel in Fig. 6) coincide with the critical mass values corresponding to the emergence of the diferent bifurcating states from the double-ring configuration. Another way to state this in the language of dynamical systems is that these multi-petal states are emerging via supercritical pitchfork (symmetry breaking) bifurcations, leading to the further destabilization of the radially symmetric state via the emergence of a wide variety of azimuthally modulated ones.

![](Tedrake2019Computing_figs/3221fd022cde5a0707729b1fb21d0588ca59ad1a633483fbff9eb4259838ca64.jpg)  
FIG. 7: (Color online) Evolution of the double-ring configuration (see panels (a) in Fig. 4) heavily perturbed (30 times the normalized eigenvector) with an eigenvector picked from the third instability in the BdG spectra (see bottom panels in Fig. 6). More precisely, we perturb the double-ring state solution with the eigenvector of the ring state calculated for $\mu = 0 . 6 3$ . The top, middle, and bottom rows of panels display, respectively, the real part, the density, and phase of the profiles at the times indicated. In this figure, as is the case in all the figures in this work, the indicated times are measured in non-dimensional units as per the adimensionalization discussed below Eq. (3).

Finally, in order to monitor the evolution of instabilities for the double-ring, we depict in Fig. 7 the dynamical destabilization of the double-ring. In this case, we perturb the double-ring profile with an eigenvector picked from the third instability in the BdG spectra (see bottom-right panel in Fig. 6). The wave form involving the relevant wavenumber is clearly dynamically amplified and eventually destroys the ring like structure in favor of one that bears the periodicity of the imposed perturbation.

![](Tedrake2019Computing_figs/6c4f25b7ffec2c9420ee263a3e3b4655f1b0ca0370732bd47985b601214bb191.jpg)  
FIG. 8: (Color online) 2-dark soliton profile and its bifurcating states for $\mu = 0 . 7$ . Same layout as in previous figures. The corresponding particle numbers as a function of $\mu$ are depicted in Fig. 9.

![](Tedrake2019Computing_figs/bf74a82fd30e51a6bc9a390506cd55ebbd043249f6f1b3f3880a89cfc9e47917.jpg)  
FIG. 9: (Color online) Top: Particle number N as a function of µ for the stationary states bifurcating from the 2-soliton solution (a). Bottom: Particle number diference ∆N between the states bifurcating from the 2-soliton configuration and the 2-soliton configuration itself. The corresponding profiles are depicted in Fig. 8. The first three bifurcating states from the 2-soliton solution (a) bifurcate at: (b) $\mu \simeq 0 . 3 2 1$ , (c) $\mu \simeq 0 . 4 6 6$ , and (d) $\mu \simeq 0 . 6 1 4$

![](Tedrake2019Computing_figs/664398e8df19a4fb892297074dfdeb6907ba0bf68afccc8369551b7d6371c991.jpg)  
FIG. 10: (Color online) Same as Fig. 8, but showing (from left to right) the first state bifurcating from the 4-, 6-, and 8-soliton profiles.

## C. States bifurcating from the n-dark soliton configurations

In a similar manner as we identified bifurcating states from the ground state and subsequently from the doublering in the previous section, we now follow the bifurcating states from the n-dark soliton solutions and their associated phenomenology. For instance, Fig. 8 depicts, alongside the 2-soliton solution, its first three bifurcating states. In this case the bifurcating states pertain to excitations of the central well of the external potential. These central well excitations correspond to azimuthal, out-ofphase, “multi-petal” configurations. Figure 9 depicts the particle numbers for these configurations. In particular, the bottom panel displays the particle number diference $\Delta N$ between the central excited states and the original 2- soliton solution. When this diagnostic departs from zero, it signals the emergence of a bifurcation of a new branch from a previously existing one (with $\Delta N = 0 )$ . As shown in Fig. 10, similarly to the bifurcating states from the 2- soliton configuration, we were able to identify bifurcating states from the 4-, 6-, and 8-soliton configurations.

![](Tedrake2019Computing_figs/03fe279d99bc69d3d0ff124c1667578354d49d9b7034ab8afa2c6c9d763f317f.jpg)

![](Tedrake2019Computing_figs/6ec9e042a40b9c45738ff1c793ef538edd0f7b2012ccf2dd19b20a992c89fc36.jpg)

![](Tedrake2019Computing_figs/53e692a46b379f19d0e4a81cc20c84dc815e8bfab4e2c20c916c34bbcd09b32a.jpg)

![](Tedrake2019Computing_figs/41740c16b206e7a5dbf622ec2c00ef7e0542a3ece48f19f1a96f11d1a1b7e358.jpg)  
FIG. 11: (Color online) Stability BdG spectra for the 2-soliton configuration and its first bifurcating state as a function of $\mu .$ Same layout as in Fig. 6. The corresponding profiles for $\mu = 0 . 7$ are depicted, respectively, in the first two columns of Fig. 8.

Now that we have identified the 2-soliton solution and its bifurcating states, let us briefly discuss the ensuing stability as a function of $\mu .$ In Fig. 11 we depict the BdG spectra of the 2-soliton state (top row) together with the spectra of its first bifurcating states (bottom row) —profiles for these configurations for $\mu = 0 . 7$ are depicted in the first two columns of Fig. 8. The BdG spectrum for the 2-soliton configuration indicates that this profile is (neutrally) stable for $\mu < 0 . 7 0 2$ . For larger values of the chemical potential (not shown here) other instabilities arise, however we do not consider them here given their much weaker growth rates.

For instance, Fig. 12 shows the long time evolution of the 2-soliton ground state heavily perturbed with an eigenvector picked from the second instability in the BdG spectrum. We observe that, when perturbed, the 2- soliton configuration develops two pairs of vortices which travel inside the ring. The vortex nature of these traveling localized solutions becomes apparent in the phase plots (see bottom row of panels) and the corresponding $2 \pi$ winding at the vortex locations. To guide the reader we have included (red) arrows that indicate the direction of motion for the vortices. As time progresses one of the vortices in each vortex pair gets “absorbed” by the edge of the ring $( t \approx 5 0 )$ leaving only two vortices of opposite charge to run along the ring. The two vortices travel towards each other, then reverse direction, move again towards each other, bounce of again etc. The vortices are found to move back and forth for a prolonged time before they annihilate for longer times (not shown here) and the configuration settles down to a slightly perturbed ring without any apparent vortices in the bulk of the ring.

Here, we omit the time evolution of instabilities corresponding to the higher excited states of the 2-soliton configuration since they do not provide any new insights into the dynamical properties. In all cases, vortices are found to travel back and forth inside the ring. For the excited states of the 2-soliton configuration, we also observe that vortices are created in the central portion of the cloud. However, those might be less relevant for experiments as the density is low there and the vortices are more tightly packed.

For completeness, we depict in Fig. 13 the BdG stability spectra for the 4-, 6- and 8-soliton solutions. As it was the case for the 2-soliton configuration, the n-soliton configurations are also stable for $\mu < 0 . 7 0 2$ and the spectra are quite similar. This is straightforward to understand as the corresponding dark solitons are placed relatively far away from each other along the ring and, therefore, their mutual interaction is (exponentially) weak and thus not very noticeable when dealing with a handful of solitons. Nonetheless, higher-order excited states including a large number of dark solitons will correspond to relatively shorter mutual separations leading to stronger interactions and modifications of the stability spectra. We defer the study of such cases to future publications.

Finally, we depict in ${ \mathrm { F i g . } }$ . 14 the corresponding dynamical evolution for the n-soliton profiles for $n = 4$ , 6, and $^ { 8 , }$ when perturbed with eigenvectors picked from the first instability in their BdG spectra. Note that in all cases the dynamics tends to lead to the disintegration of the dark solitons (through collisions and/or splitting into vortex pairs that in turn get “absorbed” by the periphery of the ring). Eventually, and potentially after long transient stages, the evolution settles into a perturbed ring structure without dark solitons or vortices in its bulk.

## D. Phase imprinting of n-dark soliton states

We now explore the especially important —in terms of a practical implementation— possibility of seeding in the experiment some of the excited state configurations that we described above. In particular, we are interested in the experimental possibility of initializing configurations that bear n-dark solitons and let them evolve to study their interactions and collisional dynamics. For that purpose, we start with the ring steady state depicted in Fig. 2(b). As mentioned above, this solution exists for $\mu \geq 0 . 3 1 3$ and it is stable for $\mu < 0 . 7 0 2$ and therefore it is a good candidate to be attainable in a physical experiment. Then, by using a phase imprinting technique, $\mathrm { e . g . }$ , by shining laser light on one half of the condensate for a short period of time [20, 24, 70, 71], whereby half of the ring’s phase is shifted by π with respect to the other half, it is possible to generate an initial condition that has the correct phase profile of a 2-dark soliton state. Such scenarios with multiple phase jumps have been previously used in quasi-1d settings in order to examine the efectively 1d interaction of dark solitary waves [72].

![](Tedrake2019Computing_figs/402c117bd6272a0b167a5f7f4c53255ef1c6cbfd171f2916c7756256d9a003ab.jpg)  
FIG. 12: (Color online) Density (top row of panels) and phase (bottom row of panels) plots showing the time evolution of the 2-soliton ground state heavily perturbed (30 times the normalized eigenvector) with an eigenvector picked from the second instability in the BdG spectra (see Fig. 11). Specifically, we perturb a 2-soliton configuration obtained for $\mu = 0 . 9 0 4$ with the second eigenvector of the 2-soliton state calculated for $\mu = 0 . 9 3$ . We confirmed the same type of dynamics when adding smaller perturbations.

![](Tedrake2019Computing_figs/e41d27df0f7a68b7d854d1750fba7d9f22f71cf48d966a417f0d43b57b71c05d.jpg)

![](Tedrake2019Computing_figs/38d91060487633098c8c3c8b51dfb436ec20e08676b9cb5c6ace3cf5dd6dff3d.jpg)

![](Tedrake2019Computing_figs/bc5c395ac549bd9df35b6f2103c69b122bc254de0c0fb74020dde916c99e3787.jpg)

![](Tedrake2019Computing_figs/2f2a728add5d1a15f5f88bd79694b393307e28947d298dfddfb7e0f824313376.jpg)

![](Tedrake2019Computing_figs/e4cad55d9784c678b5a0aae9eca06f3abf67e7151fda51d99eda112fdd5c9662.jpg)

![](Tedrake2019Computing_figs/e14fdc86bcc0a3b09931472b85f12c296ca8e363fd3181a94da12365c2e0655c.jpg)  
FIG. 13: (Color online) Stability BdG spectra for the 4-, 6- and 8-soliton states (from top to bottom). Same layout as in Fig. 6. The corresponding profiles are depicted in the panels (c)–(e) of Fig. 2.

We have tested that this technique is successful at seeding n-dark solution solutions for chemical potentials below the instability threshold around $\mu \approx 0 . 7$ (results not shown here). However, as we are interested not only in seeding steady states in the experiments, but also in observing the potentially unstable dynamics of these n-dark soliton solutions. In that light, we focus our attention here on phase imprinting n-dark soliton solutions past their stability threshold $( \mathrm { i . e . , ~ } \mu$ a bit larger than 0.7). This is precisely what is depicted in Fig. 15 where the initial condition (first column of panels) corresponds the ring steady state with a phase imprinting such that the phase of the left half is +π while the phase of the right half is 0. As can be observed from the figure, after an initial period of adjustment $( t ~ < ~ 3 0 0 )$ , where the imprinted phase forces the dark soliton nucleation, a pair of dark solitons on opposite sides of the ring is formed. This configuration corresponds to a slightly perturbed 2-dark soliton state. This state, being unstable for the chosen value of $\mu$ as per the discussion in the previous sections, evolves in a manner akin to the one depicted in Fig. 12. Namely, the dark solitons start moving and colliding along the ring.

This phase-imprinting technique can be straightforwardly generalized to higher number of dark solitons by imprinting the appropriate phase. For instance, by imprinting a phase diference across the horizontal axis and then doing the same across the vertical axis, one is left with the appropriate phase to nucleate the 4-dark soliton state. This case is depicted in Fig. 16 whose dynamical evolution in now similar to the one depicted in the first row of panels in Fig. 14. It is relevant to mention that the dynamics of the unstable n-dark soliton eventually leads to a perturbed ground state as the dark solitons destabilize towards the formation of vortex pairs, which in turn scatter and ultimately get absorbed by the periphery of the ring. It is natural to expect that as the ring gets thinner and more quasi-one-dimensional the relevant states will be progressively stabilized against such transverse undulations and the associated breakup towards vortex dipoles [73].

![](Tedrake2019Computing_figs/fbc1546c081c5658bfc606bbb101131efb45b1aea267ee3b69878345fd09e309.jpg)  
FIG. 14: (Color online) Evolution dynamics for the 4-soliton (top row), 6-soliton (middle row), and 8-soliton (bottom row) configurations heavily perturbed (30 times the normalized eigenvector) with an eigenvector picked from the first instability of the corresponding BdG spectra. In all cases we perturb the n-soliton state obtained for $\mu = 0 . 7$ with the eigenvector of the n-soliton state calculated for $\mu = 0 . 7 1$

![](Tedrake2019Computing_figs/fbeab38d6e11972d0fd64015eaf2250d07c9040816c23fa3f0b4b8a9000eb753.jpg)  
FIG. 15: (Color online) Dynamics ensuing from the phase imprinting the 2-soliton configuration for $\mu = 0 . 9 .$

![](Tedrake2019Computing_figs/2a9c569475a107a1cc7a9fa84729028dc88f225022c405730a1458971102a2e8.jpg)  
FIG. 16: (Color online) Same as in Fig. 15 but for the 4-soliton configuration.

## E. A Zoo of More Exotic States

In addition to the states we constructed from the linear limit, there also exist states which bifurcate from the

![](Tedrake2019Computing_figs/6192a43e19aa606619f02b879b1a7802db824177c8b52d8558018b5da82cfc7f.jpg)  
FIG. 17: (Color online) Real states bifurcating from the ground state for µ = 0.9 [except µ = 0.96 for panel (k)].

![](Tedrake2019Computing_figs/7ec5796225ac346bc6f43e7de2d2447bac16f9d41d3689e0e20a10a9ed1759ee.jpg)  
FIG. 18: (Color online) Real states calculated from the dipole state for $\mu = 0 . 9$

![](Tedrake2019Computing_figs/4ababbb5bd0bbbc74ecb5174a0311f1e1d76c74ee88a04eab505a785b9edfc59.jpg)

![](Tedrake2019Computing_figs/90d851632942935e0baf32c5b1a0d2ffc90d3ad2a49dede0e99bb14cc3e7aaf2.jpg)

![](Tedrake2019Computing_figs/7cec079e8b0be6f36b2ac0bbb837fd3cb93b20fd6725ca1d21c14de9e00263be.jpg)  
FIG. 19: (Color online) (a)–(d) Complex states calculated from the ground state. These profiles correspond to an n-dark soliton state coupled to a the ground state. (e)–(h) Complex states calculated from the dipole state. These profiles correspond to an n-dark soliton state coupled to a dipole state at the center of the cloud. (i)–(k) Vortex like states calculated from the ground state. These states a similar to the ones depicted in panels (a)–(d) by replacing the n-dark soliton state by a ring of n vortices. $\mu = 0 . 9$ in all cases.

ground and dipole states and their excitations. Appropriate initial guesses for these states have been constructed by using the well-known ground and dipole ans¨atze for solutions of Eq. (6) in the presence of a harmonic external potential. For instance, as depicted in Fig. 17, there is a plethora of states bifurcating from the ground state. All of the states presented in this figure are real and pertain the combination of an n-dark soliton solution (populating the ring) coupled to a phase-less hump of mass localized in the central well (namely, the remnant of the ground state of the system). We have checked that all of these states are actually unstable (results not shown here). Similarly, as depicted in Fig. 18, it is possible to find more families of purely real solutions corresponding to the combination of, again, an n-dark soliton solution (populating the ring) but now coupled to the first excited state of the ground state (namely, the dipole consisting of a plus-minus hump at the center of the cloud). We have also checked that all of these states are actually unstable (results not shown here). This process can be extended for higher excited states of the ground state coupled to the n-dark soliton configuration on the ring.

Furthermore, it is also possible to find rich families of genuinely complex solutions. For instance, as seen in panels (a)–(d) of Fig. 19, it is possible to couple the n-dark soliton state with the ground state with a nontrivial phase diference between these two states. In the same vein, as is shown in panels (e)–(h) in Fig. 19, it is possible to couple with a non-trivial relative phase the n-dark soliton state with the dipole state at the center of the cloud. We have also checked that all of these states are always unstable (results not shown here).

Finally, it is relevant to mention that non-trivial phase configurations can be constructed by replacing the n-dark soliton solutions on the ring by a necklace of n-vortex solutions. These more exotic profiles are depicted in panels (i)–(k) in Fig. 19 for the case of 2, 4, and 8 vortices, respectively.

## IV. CONCLUSIONS AND FUTURE CHALLENGES

We have studied the stationary and dynamical properties of BEC profiles supported by a ring-shaped potential with a target-like profile that has been used in a number of recent experiments conducted at NIST [56, 57]. By following steady states and their bifurcations from the linear (low atom number) limit, we have obtained a wide range of solution branches (not all of which were shown here) and studied the corresponding stability properties as the chemical potential $\mu$ (cf. atom number) is varied. Importantly, numerous among these states were found to be potentially stable, including states carrying multiple (2-, 4-, 6-, 8-) solitons between the starting point of the respective branches and up to a suitable critical value of the chemical potential. Past this critical µ value, we studied the ensuing dynamics of the dark solitons around the ring. We typically observed that the dark solitons bounce back-and-forth in the ring until they disappear in a process involving each dark soliton splitting into a vortex pair and then the vortices getting eventually absorbed by the periphery of the ring. This process eventually led to a weakly perturbed (i.e, almost homogeneous) ring void of any dark solitons or vortices that persisted for long times.

In the case of n-dark soliton solutions, taking advantage of their spectral stability, we illustrated their potential for experimental realization by using phaseimprinting techniques to seed them in the condensate. We were not only able to seed stable n-dark soliton solutions but, equally interestingly, to seed unstable solutions whereby the ensuing dark soliton instability dynamics can be studied.

Additionally, a plethora of states was identified involving a combination of (ground or excited) states supported by the central well of the target-like potential coupled with states supported by the ring channel. The states supported by the central well corresponded to the trivialphase ground state and its excitations in the form of

[1] C. J. Pethick and H. Smith, Bose-Einstein Condensation in Dilute Gases (Cambridge University Press, 2008), 2nd ed.

[2] L. Pitaevskii and S. Stringari, Bose-Einstein Condensation (Oxford University Press, Oxford, 2003).

[3] P. G. Kevrekidis, D. J. Frantzeskakis, and R. Carretero-Gonz´alez, Emergent Nonlinear Phenomena in Bose-Einstein Condensates (2008).

[4] V. S. Bagnato, D. J. Frantzeskakis, P. G. Kevrekidis,

dipole, quadrupole, etc. states. On the other hand, the ring channel accepts n-dark (equidistant) soliton solutions where n is even as the periodicity of the ring enforces an even number of dark solitons. We also followed states that, instead of bifurcating from the linear limit, bifurcate from the ground state of the system (a phase-less hump populating the central well). These states correspond to double-ring, out-of-phase, solutions and “petal”-like patterns around the ring.

It would be interesting to implement the phaseimprinting methodology in the actual experiment as it would naturally allow for the study of dark soliton dynamics and interactions especially so in such an annular setup. The potential control of the spatial width of the annulus and the associated control of the snaking stability of the solitonic structures could play a significant role in the explored dynamics. From the modeling perspective it would be interesting to study the stability and dynamics of steady states bearing a large number of dark solitons. For instance, it is known that a chain of dark solitons can be approximated by a Toda lattice on the solitons’ positions and thus one can create (Toda) solitons riding on a backbone of dark solitons (see Ref. [74] and references therein). Furthermore, a systematic extension of the present studies considering the vortex patterns in the present setting would naturally complement the present solitonic considerations. Lastly, considering extensions of this type of set up also in higher dimensions and suitable (e.g. toroidal-poloidal) geometries may be particularly interesting and relevant in its own right, as well as an appreciation of which (potentially vortical) patterns may be dynamically stable.

## Acknowledgements

Some of the work of M.H. was undertaken as a visiting research scholar at the Department of Mathematics and Statistics, University of Massachusetts, employed by the University of Oldenburg and financially supported by FP7, Marie Curie Actions, People, International Research Staf Exchange Scheme (IRSES-605096). P.G.K. and R.C.G. and M.A.E. gratefully acknowledge the support from the National Science Foundation, under grants PHY-1602994, PHY-1603058, and PHY-1707776.

B. A. Malomed, and D. Mihalache (2015), rom. Rep. Phys. 67, 5.

[5] E. A. Cornell and C. E. Wieman, Rev. Mod. Phys. 74, 875 (2002).

[6] F. Dalfovo, S. Giorgini, L. P. Pitaevskii, and S. Stringari, Rev. Mod. Phys. 71, 463 (1999).

[7] W. Ketterle, Rev. Mod. Phys. 74, 1131 (2002).

[8] A. E. Leanhardt, A. P. Chikkatur, D. Kielpinski, Y. Shin, T. L. Gustavson, W. Ketterle, and D. E. Pritchard, Phys.

Rev. Lett. 89, 040401 (2002).

[9] K. Henderson, C. Ryu, C. MacCormick, and M. G. Boshier, New Journal of Physics 11, 043030 (2009).

[10] A. L. Gaunt and Z. Hadzibabic, Scientific Reports 2, 721 (2012).

[11] M. Pasienski and B. DeMarco, Opt. Express 16, 2176 (2008).

[12] S. E. Pollack, D. Dries, M. Junker, Y. P. Chen, T. A. Corcovilos, and R. G. Hulet, Phys. Rev. Lett. 102, 090402 (2009).

[13] S. Inouye, M. R. Andrews, J. Stenger, H. J. Miesner, D. M. Stamper-Kurn, and W. Ketterle, Nature 392, 151 (1998).

[14] D. J. Frantzeskakis, Journal of Physics A Mathematical General 43, 213001 (2010).

[15] K. E. Strecker, G. B. Partridge, A. G. Truscott, and R. G. Hulet, New Journal of Physics 5, 73 (2003).

[16] F. Kh. Abdullaev, A. Gammal, A. Kamchatnov, and L. Tomio, International Journal of Modern Physics B 19, 3415 (2005).

[17] L. Khaykovich, F. Schreck, G. Ferrari, T. Bourdel, J. Cubizolles, L. D. Carr, Y. Castin, and C. Salomon, Science 296, 1290 (2002).

[18] K. Strecker, G. Partridge, A. G. Truscott, and R. H. Hullet, Nature 417, 150 (2002).

[19] S. L. Cornish, S. T. Thompson, and C. E. Wieman, Phys. Rev. Lett. 96, 170401 (2006).

[20] S. Burger, K. Bongs, S. Dettmer, W. Ertmer, K. Sengstock, A. Sanpera, G. V. Shlyapnikov, and M. Lewenstein, Phys. Rev. Lett. 83, 5198 (1999).

[21] B. P. Anderson, P. C. Haljan, C. A. Regal, D. L. Feder, L. A. Collins, C. W. Clark, and E. A. Cornell, Phys. Rev. Lett. 86, 2926 (2001).

[22] C. Becker, S. Stellmer, P. Soltan-Panahi, S. D¨orscher, M. Baumert, E.-M. Richter, J. Kronj¨ager, K. Bongs, and K. Sengstock, Nature Physics 4, 496 (2008).

[23] A. Weller, J. P. Ronzheimer, C. Gross, J. Esteve, M. K. Oberthaler, D. J. Frantzeskakis, G. Theocharis, and P. G. Kevrekidis, Phys. Rev. Lett. 101, 130401 (2008).

[24] J. Denschlag, J. E. Simsarian, D. L. Feder, C. W. Clark, L. A. Collins, J. Cubizolles, L. Deng, E. W. Hagley, K. Helmerson, W. P. Reinhardt, et al., Science 287, 97 (2000).

[25] Z. Dutton, M. Budde, C. Slowe, and L. V. Hau, Science 293, 663 (2001).

[26] C. Hamner, J. J. Chang, P. Engels, and M. A. Hoefer, Phys. Rev. Lett. 106, 065302 (2011).

[27] S. Middelkamp, J. Chang, C. Hamner, R. Carretero-Gonz´alez, P. Kevrekidis, V. Achilleos, D. Frantzeskakis, P. Schmelcher, and P. Engels, Physics Letters A 375, 642 (2011).

[28] B. Eiermann, T. Anker, M. Albiez, M. Taglieber, P. Treutlein, K.-P. Marzlin, and M. K. Oberthaler, Phys. Rev. Lett. 92, 230401 (2004).

[29] O. Morsch and M. Oberthaler, Rev. Mod. Phys. 78, 179 (2006).

[30] P. Kevrekidis, D. Frantzeskakis, and R. Carretero-Gonz´alez, The Defocusing Nonlinear Schr¨odinger Equation (Society for Industrial and Applied Mathematics, Philadelphia, PA, 2015).

[31] M. J. Ablowitz, B. Prinari, and A. D. Trubatch, Discrete and Continuous Nonlinear Schr¨odinger Systems (2004).

[32] C. Sulem and P. Sulem, The Nonlinear Schr¨odinger Equation: Self-Focusing and Wave Collapse, Applied

Mathematical Sciences (Springer New York, 2007).

[33] P. G. Kevrekidis and D. J. Frantzeskakis, Modern Physics Letters B 18, 173 (2004).

[34] M. M¨ott¨onen, S. M. M. Virtanen, T. Isoshima, and M. M. Salomaa, Phys. Rev. A 71, 033626 (2005).

[35] V. Pietil¨a, M. M¨ott¨onen, T. Isoshima, J. A. M. Huhtam¨aki, and S. M. M. Virtanen, Phys. Rev. A 74, 023603 (2006).

[36] S. Middelkamp, P. G. Kevrekidis, D. J. Frantzeskakis, R. Carretero-Gonz´alez, and P. Schmelcher, Phys. Rev. A 82, 013646 (2010).

[37] S. Middelkamp, P. Kevrekidis, D. Frantzeskakis, R. Carretero-Gonz´alez, and P. Schmelcher, Physica D: Nonlinear Phenomena 240, 1449 (2011).

[38] G. J. Milburn, J. Corney, E. M. Wright, and D. F. Walls, Phys. Rev. A 55, 4318 (1997).

[39] P. Capuzzi and E. S. Hern´andez, Phys. Rev. A 59, 1488 (1999).

[40] M. Holthaus, Phys. Rev. A 64, 011601 (2001).

[41] Y. Shin, C. Sanner, G.-B. Jo, T. A. Pasquini, M. Saba, W. Ketterle, D. E. Pritchard, M. Vengalattore, and M. Prentiss, Phys. Rev. A 72, 021604 (2005).

[42] Y.-J. Wang, D. Z. Anderson, V. M. Bright, E. A. Cornell, Q. Diot, T. Kishimoto, M. Prentiss, R. A. Saravanan, S. R. Segal, and S. Wu, Phys. Rev. Lett. 94, 090405 (2005).

[43] M. Albiez, R. Gati, J. F¨olling, S. Hunsmann, M. Cristiani, and M. K. Oberthaler, Phys. Rev. Lett. 95, 010402 (2005).

[44] T. Zibold, E. Nicklas, C. Gross, and M. K. Oberthaler, Phys. Rev. Lett. 105, 204101 (2010).

[45] C. Wang, G. Theocharis, P. G. Kevrekidis, N. Whitaker, K. J. H. Law, D. J. Frantzeskakis, and B. A. Malomed, Phys. Rev. E 80, 046611 (2009), arXiv:0904.0255.

[46] S. K. Adhikari and P. Muruganandam, Physics Letters A 310, 229 (2003), ISSN 0375-9601.

[47] D.-I. Choi and Q. Niu, Phys. Rev. Lett. 82, 2022 (1999).

[48] Y.-J. Lin, A. R. Perry, R. L. Compton, I. B. Spielman, and J. V. Porto, Phys. Rev. A 79, 063631 (2009).

[49] R. A. Pepino, J. Cooper, D. Z. Anderson, and M. J. Holland, Phys. Rev. Lett. 103, 140405 (2009).

[50] B. T. Seaman, M. Kr¨amer, D. Z. Anderson, and M. J. Holland, Phys. Rev. A 75, 023615 (2007).

[51] A. Ramanathan, K. C. Wright, S. R. Muniz, M. Zelan, W. T. Hill, C. J. Lobb, K. Helmerson, W. D. Phillips, and G. K. Campbell, Phys. Rev. Lett. 106, 130401 (2011).

[52] K. C. Wright, R. B. Blakestad, C. J. Lobb, W. D. Phillips, and G. K. Campbell, Phys. Rev. Lett. 110, 025302 (2013).

[53] N. Murray, M. Krygier, M. Edwards, K. C. Wright, G. K. Campbell, and C. W. Clark, Phys. Rev. A 88, 053615 (2013).

[54] J. Clarke and A. I. Braginski, The SQUID Handbook: Fundamentals and Technology of SQUIDs and SQUID Systems (Wiley-VCH, 2004), 1st ed., ISBN 3527402292.

[55] S. Eckel, A. Kumar, T. Jacobson, I. B. Spielman, and G. K. Campbell (2017), arXiv:1710.05800.

[56] R. Mathew, A. Kumar, S. Eckel, F. Jendrzejewski, G. K. Campbell, M. Edwards, and E. Tiesinga, Phys. Rev. A 92, 033602 (2015).

[57] S. Eckel, J. Lobb, M. Edwards, W. Phillips, J. Lee, F. Jendrzejewski, N. Murray, and G. Campbell, Nature 506, 200 (2014).

[58] E. Charalampidis, P. Kevrekidis, and P. Farrell, Commu-

nications in Nonlinear Science and Numerical Simulation 54, 482 (2018).

[59] G. W. Stewart, SIAM Journal on Matrix Analysis and Applications 23, 601 (2002).

[60] R. Lehoucq, D. Sorensen, and C. Yang, ARPACK Users’ Guide (Society for Industrial and Applied Mathematics, 1998).

[61] V. Hernandez, J. E. Roman, and V. Vidal, ACM Trans. Math. Software 31, 351 (2005).

[62] V. Hernandez, J. E. Roman, and V. Vidal, Lect. Notes Comput. Sci. 2565, 377 (2003).

[63] J. E. Roman, C. Campos, E. Romero, and A. Tomas, Tech. Rep. DSIC-II/24/02 - Revision 3.8, D. Sistemes Inform\`atics i Computaci´o, Universitat Polit\`ecnica de Val\`encia (2017).

[64] C. Kelley, Solving Nonlinear Equations with Newton’s Method (Society for Industrial and Applied Mathematics, 2003).

[65] S. Balay, S. Abhyankar, M. F. Adams, J. Brown, P. Brune, K. Buschelman, L. Dalcin, V. Eijkhout, W. D. Gropp, D. Kaushik, et al., PETSc Web page, (2017), URL http://www.mcs.anl.gov/petsc.

[66] S. Balay, S. Abhyankar, M. F. Adams, J. Brown, P. Brune, K. Buschelman, L. Dalcin, V. Eijkhout, W. D.

Gropp, D. Kaushik, et al., Tech. Rep. ANL-95/11 - Revision 3.8, Argonne National Laboratory (2017), URL http://www.mcs.anl.gov/petsc.

[67] S. Balay, W. D. Gropp, L. C. McInnes, and B. F. Smith, in Modern Software Tools in Scientific Computing, edited by E. Arge, A. M. Bruaset, and H. P. Langtangen (Birkh¨auser Press, 1997), pp. 163–202.

[68] G. Theocharis, D. J. Frantzeskakis, P. G. Kevrekidis, B. A. Malomed, and Y. S. Kivshar, Phys. Rev. Lett. 90, 120403 (2003).

[69] P. G. Kevrekidis, W. Wang, R. Carretero-Gonz´alez, and D. J. Frantzeskakis, Phys. Rev. Lett. 118, 244101 (2017).

[70] S. Burger, L. D. Carr, P. Ohberg, K. Sengstock, and<sup>¨</sup> A. Sanpera, Phys. Rev. A 65, 043611 (2002).

[71] T. Schulte, L. Santos, A. Sanpera, and M. Lewenstein, Phys. Rev. A 66, 033602 (2002).

[72] S. Stellmer, C. Becker, P. Soltan-Panahi, E.-M. Richter, S. D¨orscher, M. Baumert, J. Kronj¨ager, K. Bongs, and K. Sengstock, Phys. Rev. Lett. 101, 120406 (2008).

[73] J. Brand and W. P. Reinhardt, Phys. Rev. A 65, 043612 (2002).

[74] M. Ma, R. Navarro, and R. Carretero-Gonz´alez, Phys. Rev. E 93, 022202 (2016).