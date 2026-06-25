---
citation_key: Lumelsky2018Classification
arxiv_id: 1804.07537
arxiv_url: https://arxiv.org/abs/1804.07537
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-24T16:59:15Z
origin: ai+web
reviewed: false
---

# Introduction {#sec:intro}

Following the era of detection that started with @Mayor1995, the characterization of exoplanets is one of the great scientific adventures of the early 21st century. Transiting planets are particularly interesting because their radius can be determined from the transit depth. On top of this, transmission spectroscopy can provide insights on their gas layers, if any. The satellites *CoRoT* [@Baglin2003] and *Kepler* [@Borucki2010] have been dedicated to the study of stellar light curves and the search for exoplanetary transits, with remarkable success. The light curves are so fine that the transit depth can be determined with amazing precision (less than 2% in 125 cases referenced on `exoplanets.org`). Follow-up with spectrographs such as HARPS [@Mayor-etal-2003] then provides the amplitude of the radial velocity signal, from which the planet-to-star mass ratio can be deduced. Despite an inherent degeneracy, the ability to characterize the interiors of exoplanets improves with higher precision on mass and radius. To date, 2379 objects have both a mass and a radius in the `exoplanets.org` database (which includes unconfirmed candidates), but only 100 with a precision better than $5\%$ for both quantities. High-precision data are the challenge of the next decade. In many cases, the uncertainty on planetary parameters is dominated by the uncertainties in mass and radius (which are generally of several percent) of the host star. We will never know a planet better than its host star. This is why the new missions dedicated to the search for transiting planets -- CHEOPS [@Broeg2013], TESS [@Ricker2014], and PLATO [@Rauer-etal-2014] -- now focus on bright stars, whose properties can be more easily determined by ground-based instruments. In particular, one of the most important parameters needed to characterize exoplanets is the stellar radius [see e.g. @Creevey2007]. If the star is brighter than $\sim 8$ mag, it can be obtained by interferometry [see @Mourard-etal-2009; @Ligi2014; @Ligi-etal-2015] with better than $2\%$ precision [e.g. @Kervella2004; @Boyajian2012a; @Boyajian2012b; @Ligi-etal-2012; @Ligi-etal-2016].

One of the few bright stars hosting transiting planets known today is 55 Cnc (a.k.a. HIP 43587, HD 75732, $\rho$`<!-- -->`{=html}1 Cnc A). This star is the main component of a wide binary system, and hosts a system of five planets, detected with the radial velocity technique [@Fischer-etal-2008 and references therein]. One of them (55 Cnc e, the closest to the star) is transiting and has been detected independently by @Winn-etal-2011 and @Demory2011. As one of the first transiting super-Earths, it has received a lot of attention, and many studies have already attempted to determine its composition. Previous studies employed infrared and optical observations of transits, occultations, and phase curves [@Demory-etal-2012; @Demory-etal-2016; @Angleo-Hu-2017]. The planet is highly irradiated with an equilibrium temperature of about $2000$ K. The phase curve analysis revealed a large day--night-side temperature contrast ($\sim$ $1300$ K) and a shift of the hottest spot to the east of the substellar point [@Demory-etal-2016; @Angleo-Hu-2017]. The implication for a possible gas layer is an optically thick layer with inefficient heat redistribution. The presence of a hydrogen-rich layer is unlikely, since it would not sustain stellar evaporation and in fact no extended hydrogen atmosphere has been detected ([@Ehrenreich-etal-2012]; but see [@Tsiaras-etal-2016]). If a gas layer is present, it would be of secondary (enriched) nature [@Dorn-Heng-2017]. Furthermore, the study of 55 Cnc e's thermal evolution and atmospheric evaporation by @Lopez-2017 suggests either a bare rocky planet or a water-rich interior. But a bare rocky planet is disfavored by @Angleo-Hu-2017 and @Dorn-etal-2017b. The composition of 55 Cnc e is a matter of debate and a consistent explanation of all observations is yet to come.

The most recent interferometric study of 55 Cnc was performed by @Ligi-etal-2016, who provide a determination of the stellar angular diameter with $1.64\%$ precision, independent of any stellar evolution model (although a limb darkening model was used). Their work is consistent within $1\%$ with a previous angular diameter estimate by @vanBraun2011. Since 55 Cnc hosts a transiting exoplanet, the density of the star was determined using the transit light curve by @Maxted-etal-2015_mass-age, and thus, @Ligi-etal-2016 derived the stellar mass directly with $7\%$ uncertainty. It is therefore timely to use these new data to constrain the internal structure of the transiting planet.

In this paper, we present in sections [2](#sec:star){reference-type="ref" reference="sec:star"} and [3.1](#subsec:MRp){reference-type="ref" reference="subsec:MRp"} a general method to rigorously make use of all available interferometric observations, reducing the uncertainty and using the correlations between the various stellar parameters. As much as possible, we use analytical derivations of the probability density functions (PDFs) of the parameters of interest from those of the observed quantities. We apply these numerically to the case of 55 Cnc and its transiting planet, and show that we can reduce the uncertainty on the planetary density. In section [3.2](#subsec:IC){reference-type="ref" reference="subsec:IC"}, these new estimates of the planetary mass and radius and their correlation are used to determine the internal composition of 55 Cnc e, using the model of @Dorn-etal-2017a. Compared to previous applications of the model [@Dorn-etal-2017b], we have a slightly different estimate for the mass and radius of the planet, and we account for the correlation between them as well as for asymmetric uncertainties. The results are then compared to a scenario where the mass-radius correlation is neglected, and to a scenario where constraints on refractory element abundances are used. Thereby, we can quantify the information content of the different data inputs on the planetary interior. Eventually, we provide the most precise interior estimates while rigorously accounting for data uncertainties. Section [4](#sec:conclu){reference-type="ref" reference="sec:conclu"} is devoted to a summary and conclusion.

# Stellar parameters : A joint PDF {#sec:star}

In this section, we focus on the parameters of the host star, 55 Cnc. The observational quantities are the transit lightcurve, the angular diameter $\theta$, the spectral energy distribution from which we derive the bolometric flux $F_{\rm bol}$, and the parallax $p_\star$. We combine them to retrieve the parameters of interest (luminosity $L_\star$, effective temperature $T_{\rm eff}$, mass $M_\star$, radius $R_\star$). More specifically, we provide analytically the joint PDF of these parameters from that of the observable quantities. A joint PDF shows the correlations ; from the way the parameters are derived, correlations are strong and inevitable, and provide valuable information, as will be illustrated in this paper. Also, multiplying by a prior may lead to non-Gaussian final distributions.

## PDF of the stellar mass and radius from observations only : A Bayesian approach

Before determining mass and radius of 55 Cnc, we first evaluate prior knowledge on stellar parameters that will help to improve the interpretation of observational data. More specifically, we look for possibilities of excluding sets of parameters that would correspond to the less populated regions of the Hertzsprung--Russell (hereafter H-R) diagram. We take a Bayesian approach in order to estimate $L_\star$ and $T_{\rm eff}$. In essence, this approach accounts for both the probability distribution of $L_\star$ and $T_{\rm eff}$ for the star 55 Cnc as deduced from observations of the star, and the prior distribution of $L_\star$ and $T_{\rm eff}$ for stars in general as derived from the H-R diagram. In the following, we discuss the approach in more detail and explain how it can affect the estimate of the stellar radius.

### Probability density function of the stellar radius

The stellar radius $R_\star$ is the product of the angular radius ($\theta/2$, in radian) with the distance $d$, which is proportional to the inverse of the parallax $p_\star$ : $$\begin{equation}
R_\star=\frac{\theta d}{2} = R_0\theta/p_\star
\end{equation}$$ where $R_0$ is a length. If $\theta$ is given in milliarcseconds (mas) and $p_\star$ in arcseconds (as), $R_0=\frac{1 \rm pc}{2\,m_r} = 0.1075\,R_\odot$ (where $m_r$ is the number of mas in one radian).

Therefore, the PDF of $R_\star$, $f_{R_\star}$, can be expressed as a function of those of $\theta$ and $p_\star$ (respectively denoted $f_\theta$ and $f_{p_\star}$) as (see Appendix A): $$\begin{eqnarray}
\label{eq:fR_p}
f_{R_\star}(R) & = &
\frac{1}{R_0}\int_0^\infty p\, f_{p_\star}(p)f_\theta\left(\frac{p\,R}{R_0}\right)\ {\rm d}p\\
 & = &
\frac{R_0}{R^2}\int_0^\infty t\, f_{p_\star}\left(\frac{R_0\,t}{R}\right)f_\theta(t)\ {\rm d}t \ .
\label{eq:fR_t}
\end{eqnarray}$$ Note that if $f_{p_\star}$ and $f_\theta$ are Gaussian functions, then $f_{R_\star}$ is also a Gaussian of mean $R_0\theta_0/{p_\star}_{0}$ and variance the sum of the variances of $\theta$ and $p_\star$, but this expression is more general. It gives directly the PDF of $R_\star$ as a function of the observables.

The stellar radius is also linked to the stellar luminosity and effective temperature by $$\begin{equation}
R_\star = \sqrt{\frac{L_\star}{4\pi\sigma_{\scriptscriptstyle\!\rm SB}}}T_{\rm eff}^2
\end{equation}$$ where $\sigma_{\scriptscriptstyle\!\rm SB}$ is the Stefan--Boltzmann constant. From this, the PDF of $R_\star$ can also be expressed as a function of $f_{\rm HR}$, the joint PDF of $L_\star$ and $T_{\rm eff}$ (see Appendix A): $$\begin{eqnarray}
\label{eq:fR_T}
\hspace{-1cm}f_{R_\star}(R)
 & = & \frac{2}{R}\int_{t=0}^\infty L_{(R,t)}\, f_{\rm HR}(L_{(R,t)},t)\ {\rm d}t\\
 & = & \frac{1}{2R}\int_{l=0}^\infty T_{(R,l)}\, f_{\rm HR}(l,T_{(R,l)})\ {\rm d}l
\label{eq:fR_L}
\end{eqnarray}$$ where $L_{(R,t)} = 4\pi R^2\sigma_{\scriptscriptstyle\!\rm SB}t^4$ and $T_{(R,l)} =
\left(\frac{l}{4\pi R^2\sigma_{\scriptscriptstyle\!\rm SB}}\right)^{1/4}$. With these expressions, we can make use of a prior in the $L_\star$--$T_{\rm eff}$ plane to infer the PDF of $R_\star$.

### Likelihood and prior in the H-R diagram

#### Likelihood

The formulas linking $F_{\rm bol}$, $\theta$ and $p_\star$ to $L_\star$ and $T_{\rm eff}$ are specified in @Ligi-etal-2016, where the distributions of these two parameters were computed separately using a standard propagation of errors. Here, we derive analytically the joint likelihood of any pair $(L_\star,T_{\rm eff})$ in the H-R plane, given the observational data $f_{F_{\rm bol}}$, $f_{p_\star}$, $f_\theta$ (see Appendix B) : $$\begin{equation}
\mathcal{L}_{\rm HR}(L_\star,T_{\rm eff}) = \frac{{4\,\rm pc}\,\sqrt{\pi}m_r}{T_{\rm eff}^{\,3}\sqrt{\sigma_{\scriptscriptstyle\!\rm SB}L_\star^{\,3}}}\times\int_0^{+\infty}{\rm d}t
\label{eq:Ld_LT}
\end{equation}$$ $$\times t\times f_{F_{\rm bol}}(t)\times f_{p_\star}\left(\sqrt{\frac{4\pi t}{L_\star}}\right)\times f_\theta\left(\sqrt{\frac{4\,t}{\sigma_{\scriptscriptstyle\!\rm SB}\,T_{\rm eff}^{\,4}}}\right)\ .$$ Taking $f_{F_{\rm bol}}$, $f_{p_\star}$ and $f_\theta$ as Gaussian distributions of means and standard deviations as given in @Ligi-etal-2016, we integrate numerically the expression above and obtain for 55 Cnc the contour lines shown in Fig. [1](#fig:LT){reference-type="ref" reference="fig:LT"}. They are spread along a diagonal direction (along $L_\star\propto T_{\rm eff}^4$, that is equal radius lines) because both are increasing functions of $F_{\rm bol}$ [see also the Appendix of @Ligi-etal-2016]. From Eq. ([\[eq:Ld_LT\]](#eq:Ld_LT){reference-type="ref" reference="eq:Ld_LT"}), one can see that if the parallax and the angular diameter were perfectly known (that is, if $f_{p_\star}$ and $f_\theta$ were Dirac functions), $\mathcal{L}_{\rm HR}(L_\star,T_{\rm eff})$ would be non zero only on the parametric curve $L_\star(t)=4\pi t/p_\star^2$, $T_{\rm eff}(t) =
(4t/\sigma_{\scriptscriptstyle\!\rm SB}\theta^2)^{1/4}$. In this case, the correlation would be $1$. This curve corresponds to varying $F_{\rm bol}$ while keeping the stellar radius and distance fixed. The uncertainty on the stellar radius and distance smears the PDF around this curve. Hence, the better $p_\star$ and $\theta$ are constrained compared to $F_{\rm bol}$, the more $L_\star$ and $T_{\rm eff}$ are correlated. Here, the coefficient of correlation of $L_\star$ and $T_{\rm eff}$ is $0.23$ .

#### Prior

55 Cnc is part of the *Hipparcos* catalog, in which the density of stars in the $(L_\star-T_{\rm eff})$ plane is not uniform. Hence, one can estimate *a priori* regions in the H-R diagram where 55 Cnc has more chances to be found, and regions where it should not. This is a *prior* PDF in the $(L_\star-T_{\rm eff})$ plane. To build this prior, we have downloaded the *Hipparcos* catalog `hip2.dat`[^1], and computed $L_\star$ and $T_{\rm eff}$ for each star within $68.5$ pc from the Sun as explained in detail in Appendix C.

In Fig. [1](#fig:LT){reference-type="ref" reference="fig:LT"}, the background grayscale maps $f_{\rm Hip}^0$, the number density of stars in the *Hipparcos* catalog (light for low density, dark for high density, linear arbitrary scale). The main sequence goes down steeply from the top left corner. Inside the largest ellipse shown, the ratio of the maximum to minimum is $1.7$ ; and within half the maximum of the likelihood, it is $1.33$ . The star 55 Cnc appears to be in the vicinity of the main sequence.

![**Contour lines :** likelihood $\mathcal{L}_{\rm HR}$ of the luminosity and effective temperature of 55 Cnc as given by Eq. ([\[eq:Ld_LT\]](#eq:Ld_LT){reference-type="ref" reference="eq:Ld_LT"}) based on observations by @Ligi-etal-2016 ; nine contours separate 10 equal-sized intervals between 0 and the maximum of the likelihood. **Background grayscale :** density of stars in the *Hipparcos* catalog in this region ; in this box, the minimum and maximum of $f_{\rm Hip}^0$ are respectively 23 (light gray) and 488 (dark).](./figure1_large-eps-converted-to.pdf){#fig:LT width="\\linewidth"}

Eventually, the joint PDF of $L_\star$ and $T_{\rm eff}$ is $$\begin{equation}
f_{\rm HR}(L_\star,T_{\rm eff}) = \mathcal{L}_{\rm HR}(L_\star,T_{\rm eff}) \times f_{\rm Hip}^0(L_\star,T_{\rm eff})
\label{eq:fHR}
\end{equation}$$ It should be noted that $L_\star$ is so well constrained by the observations that the multiplication by the prior has almost no effect on the PDF of $L_\star$ : we estimate $0.591\pm 0.013\,L_\odot$ from $\mathcal{L}_{\rm HR}$ and from $f_{\rm HR}$ as well. As for the temperature, while the expected value of $T_{\rm eff}$ from $\mathcal{L}_{\rm HR}$ is $5169\,K$ with a standard deviation of $46\,K$, the $T_{\rm eff}$ found from $f_{\rm HR}$ is : $5174 \pm 46\,K$.

The Kullback--Leibler divergence $$\mathcal{D}=\iint
f_{\rm HR}\ \ln\left(\frac{f_{\rm HR}}{f_{\rm Hip}^{\,0}}\right)\ {\rm d}
L_\star\,{\rm d}T_{\rm eff}$$ is positive ($\sim 2.1$ when $L_\star$ and $T_{\rm eff}$ are integrated over a range of plus or minus $6\sigma$ around the mean), and only $3\%$ smaller than using a uniform prior. The data are very informative, and we are not dominated by the prior.

### Final Joint PDF of the Mass and Radius Using the Density {#subsec:MR}

Using Equations ([\[eq:fR_p\]](#eq:fR_p){reference-type="ref" reference="eq:fR_p"}) and ([\[eq:fR_t\]](#eq:fR_t){reference-type="ref" reference="eq:fR_t"}) gives $R_{\rm 55\,Cnc} = 0.960 \pm
0.0181\, R_\odot = (668.3 \pm 12.6)10^6$ m, $f_{R_\star}$ being a Gaussian, as in @Ligi-etal-2016.

In Appendix A.3, we show that using Equations ([\[eq:fR_T\]](#eq:fR_T){reference-type="ref" reference="eq:fR_T"}) and ([\[eq:fR_L\]](#eq:fR_L){reference-type="ref" reference="eq:fR_L"}) with $f_{\rm HR}$ given by Eq. ([\[eq:Ld_LT\]](#eq:Ld_LT){reference-type="ref" reference="eq:Ld_LT"}) is exactly equivalent to directly using Equations ([\[eq:fR_p\]](#eq:fR_p){reference-type="ref" reference="eq:fR_p"}) and ([\[eq:fR_t\]](#eq:fR_t){reference-type="ref" reference="eq:fR_t"}). No information is lost, and no uncertainty is added by moving to the H-R plane. Hence, using Equations ([\[eq:fR_T\]](#eq:fR_T){reference-type="ref" reference="eq:fR_T"}) and ([\[eq:fR_L\]](#eq:fR_L){reference-type="ref" reference="eq:fR_L"}) with $f_{\rm HR}$ given by Equation ([\[eq:fHR\]](#eq:fHR){reference-type="ref" reference="eq:fHR"}) shows only the effect of the prior. Integrating this numerically, we find $R_{\rm 55\,Cnc} = 0.958\pm 0.0178\,R_\odot$. These two PDFs of $R_\star$ are shown in the bottom left panel of Fig. [2](#fig:MRstar){reference-type="ref" reference="fig:MRstar"}.

@Maxted-etal-2015_mass-age provide the density of 55 Cnc : $\rho_\star = 1.084 \pm 0.038\ \rho_\odot$. Indeed, a careful analysis of the light curve, combining the transit period and the transit duration directly yields the stellar density $\rho_\star$ [@Seager-MallenOrnelas-2003]. Then, the joint likelihood of $M_\star$ and $R_\star$ can be expressed analytically : $$\begin{equation}
\mathcal{L}_{MR\star} (M,R) = 
\frac{3}{4\pi R^3}\times f_{R_\star}(R)\times f_{\rho_\star}\left(\frac{3M}{4\pi R^3}\right)
\label{eq:MRstar_anal}
\end{equation}$$ (see Appendix D). Using $f_{R_\star}$ given by Eqs. ([\[eq:fR_p\]](#eq:fR_p){reference-type="ref" reference="eq:fR_p"}-[\[eq:fR_t\]](#eq:fR_t){reference-type="ref" reference="eq:fR_t"}), the result is $M_{\rm 55\,Cnc} =
0.961 \pm 0.064\ M_\odot$, with a correlation coefficient with $R_{\rm
  55\,Cnc}$ of $0.85$. The level curves of this distribution are shown in Fig. [2](#fig:MRstar){reference-type="ref" reference="fig:MRstar"} as the tilted solid ellipses. Using the prior in the H-R diagram, one gets $M_{\rm 55\,Cnc} = 0.954 \pm 0.063\ M_\odot$, with a correlation coefficient with $R_{\rm 55\,Cnc}$ of $0.85$.

Our results are summarized and compared to the ones of @Ligi-etal-2016 in Table [1](#tab:params){reference-type="ref" reference="tab:params"}. We find that the prior from the *Hipparcos* catalog does not change significantly the joint PDF of ($M_{\rm 55\,Cnc}$, $R_{\rm 55\,Cnc}$). The interferometric observations are precise enough to constrain the stellar parameters. In what follows, we thus use the analytical expressions Equations. ([\[eq:fR_p\]](#eq:fR_p){reference-type="ref" reference="eq:fR_p"}), ([\[eq:fR_t\]](#eq:fR_t){reference-type="ref" reference="eq:fR_t"}), and ([\[eq:MRstar_anal\]](#eq:MRstar_anal){reference-type="ref" reference="eq:MRstar_anal"}).

If correlation is neglected and $M_\star$ and $R_\star$ are directly taken with their uncertainties as independent variables, their joint PDF becomes a 2D Gaussian distribution represented by the dashed ellipses with horizontal and vertical axes in Fig. [2](#fig:MRstar){reference-type="ref" reference="fig:MRstar"}. In doing so, one would have correct marginal distributions (they are close to Gaussian). But one would mistakenly consider likely combinations of $M_\star$ and $R_\star$ that can actually be excluded by the constraint on $\rho_\star$. Obviously, taking the correlation into account reduces the area to explore in the mass-radius parameter plane, and should help constrain the structure and composition of the transiting planet, as we will see in the next section.

:::: {#fig:MRstar .figure}
![image](Lumelsky2018Classification_figs/MR_star_contour-eps-converted-to.png){width="\\linewidth"} ![image](Lumelsky2018Classification_figs/R_star-eps-converted-to.png){width="49%"} ![image](Lumelsky2018Classification_figs/M_star-eps-converted-to.png){width="49%"}

::: caption
**Top :** joint probability density function of the mass and radius of the star 55 Cnc. The nine plain thick contour lines separate 10 equal-sized intervals between 0 and the maximum of Eq. ([\[eq:MRstar_anal\]](#eq:MRstar_anal){reference-type="ref" reference="eq:MRstar_anal"}). The dashed blue contour lines show the same for the case where one mistakenly considers $M_\star$ and $R_\star$ as independent. **Bottom :** marginal PDFs of $R_\star$ and $M_\star$ (plain lines); the dashed blue line is the Gaussian obtained without the use of the prior in the case of $R_\star$, and is a Gaussian curve of the same mean and standard deviation, for comparison, in the case of $M_\star$.
:::
::::

## About stellar models

$L_\star$ and $T_{\rm eff}$ of 55 Cnc being known, one could fit them with stellar evolution models to infer the corresponding mass, age, and other parameters like the radius. Stellar models are a precious tool to estimate stellar parameters that are not measurable, provided observational constraints are tight enough. Nonetheless, this method should be used with care, for the following reasons.

1.  Degeneracy : low-mass stars gather on the main sequence where they slowly increase their luminosity and temperature for billions of years, inducing a huge mass--age degeneracy. In the case of 55 Cnc, which is close to the main sequence, the degeneracy is between a pre- and a post-main sequence phase [coined "young" and "old" solutions in @Ligi-etal-2016] ; the detection of lithium in its atmosphere [@Hinkel-etal-2014; @Ramirez-etal-2014] advocates for the young solution.

2.  Internal source of error : models are more or less sensitive to many parameters that are not always well constrained, such as the metallicity (with very different values provided in the literature for 55 Cnc), the initial helium abundance, the rotation rate, and the choice of input physics. Assuming a default value of these parameters may lead to inaccuracy in the final result (see below).

3.  External source of error : different models available in the literature can give different results, in part because of the two difficulties mentioned above [see @Lebreton2012].

In fact, using the CES2MO pipeline[^2] and our value for $L_\star$ and $T_{\rm eff}$, we find, for the young solution of 55 Cnc, masses ranging from $0.950\pm 0.015$ to $0.989\pm 0.020\,M_\odot$, depending on the choice on the internal parameters (mostly the stellar metallicity). This highlights the difficulty of using stellar models to derive accurately the mass and radius of an individual star with reliable uncertainties. Of course, accuracy is difficult to assess ; however, the variability of estimates yields a proxy for it. Here, the different values from stellar models are only in rough agreement with one another, so it would be inappropriate to just pick one, neglecting the uncertainty on the parameters of the model.

Note that the mass range we find using the Bayesian approach above encompasses the various stellar models mentioned here for the young solution [see also @Ligi-etal-2016]. Although the interferometric radius disagrees with the radius found by asteroseismology for some stars (which opens the question of possible bias for one of these methods), it overcomes assumptions that are otherwise introduced by the use of stellar models. Hence, reassured by the agreement with stellar models, in the following we adopt the estimate of the mass and radius for 55 Cnc given in sect. [2.1.3](#subsec:MR){reference-type="ref" reference="subsec:MR"}. We stress that our error bar is larger than the brutal use of a single stellar model could provide, but we think it is the best possibility so far for 55 Cnc.

::: {#tab:params}
+--------------------------------------------------------------------------------------------------+
| Coordinates                                                                                      |
+:=================================+==========================:+==================:+:=============:+
| R.A. (J2000)                                                 | 08h 52min 35.81093s               |
+--------------------------------------------------------------+-----------------------------------+
| Decl. (J2000)                                                | +28$^{\circ}$ 19' 50.9511"        |
+--------------------------------------------------------------+-----------------------------------+
| Parallax \[mas\]                                             | 81.03 $\pm$ 0.75                  |
+--------------------------------------------------------------+-----------------------------------+
| Distance \[pc\]                                              | 12.34 $\pm$ 0.11                  |
+--------------------------------------------------------------+-----------------------------------+
| Stellar parameters                                                                               |
+----------------------------------+---------------------------+-------------------+---------------+
|                                  | Ligi+(2016)               | This work         | (corr.)       |
+----------------------------------+---------------------------+-------------------+---------------+
| $M_\star$ \[$M_\odot$\]          | 0.960 $\pm$ 0.067         | 0.954 $\pm$ 0.063 | $0.85$        |
+----------------------------------+---------------------------+-------------------+               |
| $R_\star$ \[$R_\odot$\]          | 0.96 $\pm$ 0.02           | 0.958 $\pm$ 0.018 |               |
+----------------------------------+---------------------------+-------------------+---------------+
| $\rho_\star$ \[$\rho_\odot$\]    | 1.084 $\pm$ 0.038                             |               |
+----------------------------------+---------------------------+-------------------+---------------+
| $L_\star$ \[$L_\odot$\]          | 0.589 $\pm$ 0.014         | 0.591$\pm$ 0.013  | $0.23$        |
+----------------------------------+---------------------------+-------------------+               |
| $T_{\rm eff}$ \[K\]              | 5165 $\pm$ 46             | 5174 $\pm$ 46     |               |
+----------------------------------+---------------------------+-------------------+---------------+
| Planetary parameters                                                                             |
+----------------------------------+---------------------------+-------------------+---------------+
|                                  | Ligi+(2016)               | This work         | (corr.)       |
+----------------------------------+---------------------------+-------------------+---------------+
| $M_{\rm p}$ \[$M_\oplus$\]       | 8.631 $\pm$ 0.495         | 8.703 $\pm$ 0.482 | $0.30$        |
+----------------------------------+---------------------------+-------------------+               |
| $R_{\rm p}$ \[$R_\oplus$\]       | 2.031$^{+0.091}_{-0.088}$ | 2.023 $\pm$ 0.088 |               |
+----------------------------------+---------------------------+-------------------+---------------+
| $\rho_{\rm p}$ \[$\rho_\oplus$\] | $1.03\pm 0.14$            | $1.06\pm 0.13$    |               |
+----------------------------------+---------------------------+-------------------+---------------+

: Properties of the star 55 Cnc and of its transiting exoplanet 55 Cnc e.
:::

# Planetary parameters and composition {#sec:planet}

In this section, we apply the previous results on the host star to the transiting planet 55 Cnc e. This planet has attracted a lot of attention already, being one of the first discovered transiting super-Earth, as explained in Section [1](#sec:intro){reference-type="ref" reference="sec:intro"}. It is therefore an excellent case to test the power of our method.

## Likelihood and joint PDF {#subsec:MRp}

From the PDF of the mass and radius of the star, we deduce that of the planet analytically. For any $M_p$, $M_\star$, one can define the associated semi-amplitude of the radial velocity signal $K$, following a classical formula resulting from Kepler's law: $K(M_p,M_\star)=\frac{M_p}{M_\star^{2/3}}\left(\frac{2\pi
  G}{P}\right)^{1/3}$ (where $P$ is the orbital period, and we have assumed that the eccentricity is zero[^3]). Similarly, for a pair $R_p$, $R_\star$, the corresponding transit depth is $TD(R_p,R_\star)=(R_p/R_\star)^2$. Therefore, the PDF associated to any fixed planetary mass and radius is $$\begin{eqnarray*}
f_p(M_p,R_p) & \propto & \iint \exp\left(-\frac12\left(\frac{K(M_p,M_\star)-K_e}{\sigma_K}\right)^2\right) \\
 & & \ \times \exp\left(-\frac12\left(\frac{TD(M_p,M_\star)-TD_e}{\sigma_{TD}}\right)^2\right)\\
 & & \ \times \mathcal{L}_{MR\star}(M_\star,R_\star)\  {\rm d}M_\star\,{\rm d}R_\star
\label{eq:PDF_MR_planet}
\end{eqnarray*}$$ where the observed transit depth associated to 55 Cnc e is $TD_e\pm\sigma_{TD}=(3.72\pm 0.30) 10^{-4}$ [@Dragomir-etal-2014], and the amplitude of the signal in radial velocity is $K_e\pm\sigma_K=6.30\pm 0.21$ m s$^{-1}$ [@Endl-etal-2012].

![Mass and radius data samples for `O`, `OC`, and the `OH` that mostly differ in terms of the correlation between mass and radius. In comparison, two idealized mass-radius relationships for pure MgSiO$_3$ and Earth-like interiors are plotted. MgSiO$_3$ represents the least dense end-member of purely rocky interiors. Therefore, purely rocky interiors cannot be exluded in cases of `O` and `OC`, whereas in the case of the hypothetical high correlation (`OH`), the interior must be rich in volatiles. See the text for details.](Lumelsky2018Classification_figs/FigureNEWer_55CncE.png){#fig:MRSAMP width="\\linewidth"}

This expression has been integrated numerically ; we find : $$\begin{eqnarray}
\label{eq:Mp}
M_p & = & 8.703 \pm 0.482\ M_\oplus\\
\label{eq:Rp}
R_p & = & 2.023 \pm 0.088\ R_\oplus
\end{eqnarray}$$ with a correlation of $c=0.30$.\
The cloud of red dots labeled `OC` in Fig. [3](#fig:MRSAMP){reference-type="ref" reference="fig:MRSAMP"} shows a Monte Carlo realization of this PDF. The correlation is visible, as the cloud is elongated in a direction parallel to isodensity lines. An Earth-like composition is almost excluded, while a pure rocky interior appears possible. The blue dots in Fig. [3](#fig:MRSAMP){reference-type="ref" reference="fig:MRSAMP"} correspond to the case where $\mathcal{L}_{MR\star}(M_\star,R_\star)$ would be replaced in the expression of $f_p(M_p,R_p)$ by a PDF of $M_\star,R_\star$ that would neglect their correlation (shown as short dashed lines in Fig. [2](#fig:MRstar){reference-type="ref" reference="fig:MRstar"}). In this case, an Earth-like composition could be excluded with less confidence.

It is particularly interesting to consider the correlation in order to estimate the density of the planet. From our joint PDF, we find $\rho_p = 5846\pm 740$ kg m$^{-3} = 1.06\pm
\,0.13\rho_\oplus$ [^4]. A standard propagation of errors assuming $M_p$ and $R_p$ indepenent would give $\rho_p = 5797 \pm 819$ kg.m$^{-3}$. We get a $10\%$ smaller uncertainty on the density of 55 Cnc e taking the correlation into account. The limiting factor here is the uncertainty on $TD_e$, which is mainly responsible for the correlation between mass and radius to be much smaller for the planet ($0.30$) than for the host star ($0.86$). Indeed, the $8\%$ uncertainty on $TD_e$ translates into $4\%$ in the radius ratio, while the stellar radius is determined to within $2\%$. More precise observations of the transit would be very useful in this particular case and would allow us to increase significantly the gain on the density precision. On the other hand, the $3\%$ uncertainty on $K_e$ is smaller than that on $M_\star$ (and even on $M_\star^{2/3}$) so, to gain precision in the planetary mass, one should aim at gaining precision on the stellar mass. In the particular case of 55 Cnc, the best way to do so would be to better constrain its density by obtaining a finer light curve[^5].

In the next subsection, we use this joint PDF to characterize the interior of 55 Cnc e, including a test scenario where $TD_e$ and $K_e$ would be known with negligible uncertainty, which is shown in Fig. [3](#fig:MRSAMP){reference-type="ref" reference="fig:MRSAMP"} as the pale dots labeled `OH` ; in this case, one recovers the $0.85$ correlation associated with the distribution of the stellar mass and radius.

## Structure and Composition {#subsec:IC}

### Method

The estimates of planetary mass and radius are subsequently used to characterize the interior of 55 Cnc e. To do so, we use the generalized Bayesian inference analysis of @Dorn-etal-2017a that employs a Markov chain Monte Carlo (MCMC) method. This method allows us to rigorously quantify the degeneracy of the following interior parameters for a general planet interior:

1.  core: core size ($r_{\rm core}$),

2.  mantle: mantle composition (mass ratios ${\rm Fe}/{\rm Si}_{\rm mantle}$, ${\rm Mg}/{\rm Si}_{\rm mantle}$) and size of rocky interior ($r_{\rm core+mantle}$),

3.  gas: intrinsic luminosity ($L_{\rm int}$), gas mass ($m_{\rm gas}$), and metallicity ($Z_{\rm gas}$).

In this study, the planetary interior is assumed to be composed of a pure iron core, a silicate mantle comprising the oxides Na$_2$O--CaO--FeO--MgO--Al$_2$O$_3$--SiO$_2$, and a gas layer of H, He, C, and O. Unlike @Dorn-etal-2017b, we have assumed no additional water layer. For the highly irradiated planet 55 Cnc e, any water layer would be in a vapour or super-critical state.

The prior distributions of the interior parameters are listed in Table [2](#tableprior){reference-type="ref" reference="tableprior"}. The priors are chosen conservatively. The cubic uniform priors on $r_{\rm core}$ and $r_{\rm core+mantle}$ reflect equal weighing of masses for both core and mantle. Prior bounds on ${\rm Fe}/{\rm Si}_{\rm mantle}$ and ${\rm Mg}/{\rm Si}_{\rm mantle}$ are determined by the host star's photospheric abundance proxies, whenever abundance constraints are considered. Otherwise, ${\rm Fe}/{\rm Si}_{\rm mantle}$ and ${\rm Mg}/{\rm Si}_{\rm mantle}$ are chosen such that the iron oxide can range from $0\%$ to $70\%$ in weight while the magnesium and silicate oxides can range from $0\%$ to $100\%$ (all oxides summing up to $100\%$ of course). Since iron is distributed between core and mantle, ${\rm Fe}/{\rm Si}_{\rm bulk}$ only sets an upper bound on ${\rm Fe}/{\rm Si}_{\rm mantle}$. A log-uniform prior is set for $m_{\rm gas}$ and $L_{\rm int}$.

In general, the data that we consider as input to the interior characterization are:

1.  Original data (`O`), that comprises the planetary mass and radius given by Eqs. ([\[eq:Mp\]](#eq:Mp){reference-type="ref" reference="eq:Mp"}) and ([\[eq:Rp\]](#eq:Rp){reference-type="ref" reference="eq:Rp"}), the orbital radius, and the stellar irradiation (namely, stellar effective temperature $T_{\rm eff} = 5174 K$ and stellar radius $R_\star = 0.961 R_{\odot}$).

2.  Correlation (`C`) between mass and radius: $c$ =0.30,

3.  Abundances (`A`), that comprise bulk abundance constraints on ${\rm Fe}/{\rm Si}_{\rm bulk}$ and ${\rm Mg}/{\rm Si}_{\rm bulk}$, and minor elements Na, Ca, Al. From the stellar ratios that can be measured in the stellar photosphere, one gets: ${\rm Fe}/{\rm Si}_{\rm bulk}$ = 1.86 $\pm$ 1.49, ${\rm Mg}/{\rm Si}_{\rm bulk}$ = 0.93 $\pm$ 0.77, m$_{\rm CaO}$ = 0.013 wt%, m$_{\rm Al_2O_3}$ = 0.062 wt%, m$_{\rm Na_2O}$ = 0.024 wt% [@Dorn-etal-2017b].

We consider different scenarios labeled `O`, `OC`, `OA`, and `OCA` where the letters correspond to the set of data taken into account. For example, for the data scenario `O`, we consider planetary mass and radius as well as other data, but we neglect mass-radius correlation and abundance constraints.

The structural model for the interior uses self-consistent thermodynamics for core, mantle, and to some extent also the gas layer. For the core density profile, we use the equation of state (EoS) fit of iron in the hexagonal close-packed structure provided by @bouchet on *ab initio* molecular dynamics simulations. For the silicate mantle, we compute equilibrium mineralogy and density as a function of pressure, temperature, and bulk composition by minimizing the Gibbs free energy [@connolly09]. We assume an adiabatic temperature profile within core and mantle.

For the gas layer, we solve the equations of hydrostatic equilibrium, mass conservation, and energy transport. For the EoS of elemental compositions of H, He, C, and O, we employ the Chemical Equilibrium with Applications package [@CEA], which performs chemical equilibrium calculations for an arbitrary gaseous mixture, including dissociation and ionization and assuming ideal gas behavior. The metallicity $Z_{\rm gas}$ is the mass fraction of C and O in the gas layer, which can range from 0 to 1. For the gas layer, we assume an irradiated layer on top of a convection-dominated layer, for which we assume a semi-gray, analytic, global temperature averaged profile [@Guillot-2010; @Heng2014]. The boundary between the irradiated layer and the underlying layer is defined where the optical depth in visible wavelength is $100 / \sqrt{3}$ [@JIN2014]. Within the convection-dominated layer, the usual Schwarzschild criterion is used to determine where in the layer convection or radiation is more efficient. The planet radius is defined where the chord optical depth becomes 0.56 [@Lecavelier08]. We refer the reader to model I in @Dorn-etal-2017a for more details on both the inference analysis and the structural model.

::: {#tableprior}
  ---------------------------------- ------------------------------------- ------------------------------------
  Parameter                          Prior Range                           Distribution
  $r_{\rm core}$                     (0.01 -- 1) $r_{\rm core+mantle}$     uniform in $r_{\rm core}^3$
  ${\rm Fe}/{\rm Si}_{\rm mantle}$   0 -- ${\rm Fe}/{\rm Si}_{\rm star}$   uniform
  ${\rm Mg}/{\rm Si}_{\rm mantle}$   ${\rm Mg}/{\rm Si}_{\rm star}$        Gaussian
  $r_{\rm core+mantle}$              (0.01 -- 1) $R$                       uniform in $r_{\rm core+mantle}^3$
  $m_{\rm gas}$                      0 -- $m_{\rm env, max}$               uniform in log-scale
  $L_{\rm int}$                      $10^{18} - 10^{23}$ erg s$^{-1}$      uniform in log-scale
  $Z_{\rm gas}$                      0 -- 1                                uniform
  ---------------------------------- ------------------------------------- ------------------------------------

  : Prior Ranges.
:::

:::: table*
::: center
  -------------------------------------- ------------------------- ------------------------- ------------------------- ------------------------- -------------------------
  Interior Parameter                                         `O`                      `OC`                 **`OCA`**                      `OA`                      `OH`  
  log$_{10}$($m_{\rm gas}$/M$_p$)          $-4.75_{-1.74}^{+2.03}$   $-4.86_{-1.71}^{+2.03}$   $-5.07_{-1.61}^{+2.14}$   $-5.32_{-1.87}^{+2.14}$   $-4.49_{-1.49}^{+1.97}$
  $Z_{\rm gas}$                             $0.55_{-0.29}^{+0.23}$    $0.55_{-0.29}^{+0.23}$    $0.58_{-0.30}^{+0.22}$    $0.57_{-0.30}^{+0.23}$    $0.55_{-0.30}^{+0.21}$
  log$_{10}$($L_{\rm int}$)                $21.46_{-2.11}^{+2.12}$   $21.51_{-2.11}^{+2.08}$   $21.49_{-2.14}^{+2.13}$   $21.48_{-2.14}^{+2.14}$   $21.48_{-2.15}^{+2.13}$
  $r_{\rm gas}$                             $0.09_{-0.05}^{+0.06}$    $0.09_{-0.05}^{+0.05}$    $0.08_{-0.05}^{+0.05}$    $0.08_{-0.06}^{+0.05}$    $0.10_{-0.03}^{+0.05}$
  $r_{\rm core+mantle}$/R$_p$               $0.91_{-0.06}^{+0.05}$    $0.91_{-0.05}^{+0.05}$    $0.92_{-0.05}^{+0.05}$    $0.92_{-0.05}^{+0.06}$    $0.90_{-0.05}^{+0.03}$
  $r_{\rm core}$/$r_{\rm core+mantle}$      $0.41_{-0.14}^{+0.13}$    $0.40_{-0.13}^{+0.13}$    $0.36_{-0.12}^{+0.10}$    $0.35_{-0.11}^{+0.10}$    $0.39_{-0.12}^{+0.13}$
  ${\rm Fe}/{\rm Si}_{\rm mantle}$          $6.47_{-4.36}^{+7.25}$    $6.69_{-4.54}^{+7.83}$    $1.31_{-0.85}^{+1.19}$    $1.37_{-0.88}^{+1.19}$    $6.84_{-4.68}^{+8.52}$
  ${\rm Mg}/{\rm Si}_{\rm mantle}$          $6.83_{-4.16}^{+5.80}$    $6.97_{-4.15}^{+5.74}$    $1.03_{-0.57}^{+0.66}$    $1.04_{-0.58}^{+0.66}$    $7.14_{-4.20}^{+5.83}$
  -------------------------------------- ------------------------- ------------------------- ------------------------- ------------------------- -------------------------

Note. Uncertainties of 1-$\sigma$ are listed.\
We use the `OCA` scenario (in bold) for the final interpretation of possible interiors of 55Cnc e.
:::
::::

### Results

We investigate the information content of the different data scenarios labeled `O`, `OC`, `OA`, and `OCA`. For each scenario, we have used the generalized MCMC method to calculate a large number of sampled models ($\sim 10^6$) that represent the posterior distribution of possible interior models. The resulting posterior distributions are shown in Fig. [4](#fig:IC1){reference-type="ref" reference="fig:IC1"}, which displays cumulative distribution functions (cdf). The thin black line is the initial (prior) distribution. The colored lines correspond to the different data scenarios. They indicate how the ability to estimate interiors changes by considering different data. A summary of interior parameter estimates is stated in Table [\[tableresults\]](#tableresults){reference-type="ref" reference="tableresults"}.

In the first scenario (`O`), the uncorrelated planetary mass and radius given in Table [1](#tab:params){reference-type="ref" reference="tab:params"} are considered, as well as the orbital radius and stellar luminosity. These data help to constrain the mass and radius fraction of the gas layer, the size of the rocky interior and the core, while intrinsic luminosity, gas metallicity, and mantle composition are poorly constrained. In the second scenario (`OC`), we add the correlation coefficient of $M_p$ and $R_p$. Since this correlation is low ($c = 0.3$, see also Fig. [3](#fig:MRSAMP){reference-type="ref" reference="fig:MRSAMP"}), differences in our ability to constrain the interior are marginal : uncertainty ranges for $r_{\rm core+mantle}$, $r_{\rm
  core}$, $m_{\rm gas}$, and $r_{\rm gas}$ reduce by $\sim
1\%$.

In the `OA` scenario, we add constraints on refractory element ratios compared to the scenario `O` with uncorrelated mass and radius. The abundance constraints significantly improve estimates on the mantle composition (by $\sim$ 85%) and the core size (by $\sim$ 20%). Thereby the density of the rocky interior is better constrained which also affects the estimates of $r_{\rm core+mantle}$, $m_{\rm gas}$, and $r_{\rm gas}$ by a few percent. The information value of abundance constraints is discussed by @Dorn-etal-2015 in detail.

If abundance constraints are considered, the effect of adding the mass-radius correlation is more pronounced. This can be seen by comparing scenario `OA` with `OCA`, in which the latter scenario accounts for both the correlation and the abundance constraints. The additional correlation mostly improves $r_{\rm core+mantle}$, $m_{\rm gas}$, and $r_{\rm gas}$. The 10th percentiles (and 90th percentiles) of the gas radius fraction (and the rocky radius fraction) change by 2% compared to the planet radius.

To study the importance of the mass-radius correlation, we add a hypothetical scenario (`OH`), in which the uncertainty on the transit depth $TD_e$ and radial velocity signal $K_e$ are assumed negligible, such that the correlation between the planetary mass and radius is equal to that between the stellar mass and radius with $c =
0.869$. Note that neglecting the uncertainty on the planet-to-star radius and mass ratios also leads to reducing significantly the uncertainties on $M_p$ and more importantly $R_p$ : we get $R_p=2.025
\pm 0.042\ R_\oplus$ (where the slight but negligible difference in the expected value with the previous case is due to the non-use of the *Hipparcos* prior here). For `OH`, we generally find that interior estimates significantly improve compared to `OCA`. This is true for $r_{\rm core+mantle}$, $m_{\rm gas}$, and $r_{\rm gas}$. In this scenario, we can exclude the possibility of a purely rocky interior and find gas layers with radius fractions larger than 0.05 and mass fractions larger than $10^{-7}$. This (hypothetical) case illustrates the high value in both a high radius precision and mass-radius-correlation for interior characterization.

The `OCA` scenario represents our most complete dataset given the considered interferometric data. Figure [5](#fig:IC2){reference-type="ref" reference="fig:IC2"} shows the posterior distribution of the `OCA` scenario in more detail. The one-dimensional posterior functions illustrate that only some interior parameters can be constrained by data, since prior and posterior distributions significantly differ: gas mass fraction $m_{\rm gas}$, $r_{\rm core+mantle}$, $r_{\rm core}$, and ${\rm Fe}/{\rm Si}_{\rm mantle}$. The gas layer properties of metallicity and intrinsic luminosity are very degenerate and the data considered here do not allow to constrain them. We find that the gas layer has a radius fraction of $r_{\rm gas} = 0.08\pm 0.05\ R_p$ and a mass fraction about 10 times larger than for Earth, although with large uncertainty (see Table [\[tableresults\]](#tableresults){reference-type="ref" reference="tableresults"}). The gas metallicity is weakly constrained; however, low metallicities are less likely i.e., there is an 80% chance that the metallicity is larger than 0.3 (while assuming a uniform prior on $Z_{\rm gas}$). The size of the rocky interior is estimated to be $r_{\rm core+mantle}$= $0.92 \pm 0.05\ R_p$ with a core of size $r_{\rm core} = 0.36^{+0.10}_{-0.12}$ $r_{\rm core+mantle}$.

Between the scenarios `O`, `OC`, `OH` on one hand and `OCA`, `OA` on the other, there is a large difference in the predicted range of mantle compositions. For the former, the ratios of ${\rm Fe}/{\rm Si}_{\rm mantle}$ and ${\rm Mg}/{\rm Si}_{\rm mantle}$ are large, albeit with huge uncertainties, while for the latter these ratios are significantly better constrained, due to the used abundance constraints (${\rm Fe}/{\rm Si}_{\rm bulk}$ and ${\rm Mg}/{\rm Si}_{\rm bulk}$). Note that a larger ${\rm Fe}/{\rm Si}_{\rm mantle}$ induces a denser mantle, hence a thicker gas layer. These differences illustrate the high information value of abundance constraints for which the stellar composition may be used as a proxy [@Dorn-etal-2015] in order to reduce the otherwise high degeneracy. Only mass and radius (`O`, `OC`, `OH`) allow for a large range of possibly unrealistic mantle compositions that are very different from Earth-like mantle compositions (Mg/Si$\sim 1$ and Fe/Si $< 1$).

![Sampled one-dimensional marginal posterior for interior parameters: (a) gas mass fraction $m_{\rm gas}$, (b) gas metallicity $Z_{\rm gas}$, (c) intrinsic luminosity $L_{\rm int}$, (d) gas radius fraction, (e) size of rocky interior $r_{\rm core+mantle}$/$R_{\rm p}$, (f) relative core size $r_{\rm
    core}$/$r_{\rm core+mantle}$, (g), (h) mantle composition in terms of mass ratios ${\rm Fe}/{\rm Si}_{\rm mantle}$ and ${\rm Mg}/{\rm Si}_{\rm mantle}$. The prior distributions are shown in black. For (g), (h) the priors vary between the data scenarios (`O`, `OC`, `OH` versus `OCA`, `OA`) and are not shown.](./Figure_55CncE_cdf_O.pdf){#fig:IC1 width="\\textwidth"}

![Sampled two and one-dimensional marginal posterior for all interior parameters and the `OCA` data scenario. Grey shaded 2-D areas represent 1-$\sigma$ and 2-$\sigma$ distributions of marginalized posteriors. Prior distributions are shown in dashed blue for the one-dimensional marginal posteriors. ](Lumelsky2018Classification_figs/Figure_2Dpdf_55CncE.png){#fig:IC2 width="\\textwidth"}

### Discussion

An alternative interior scenario could include C-rich compositions. Such interiors are indeed possible, and have been proposed in the past [e.g. @Madhusudhan-etal-2012]. This was motivated by a high C/O ratio estimate for the star [$1.12\pm0.19$, @DelgadoMena-etal-2010], but this ratio has been later corrected down to $0.78\pm0.08$ [@Teske-etal-2013], making C-rich interior models less timely for 55 Cnc e. Although @Moriatry-etal-2014 argue that a sequential condensation during the whole life of an evolving proto-planetary disk can favor the formation of C-rich planetesimals, they find that the planetesimals expected to form around 55 Cnc should have C/O$<$`<!-- -->`{=html}1, even assuming C/O=1 for this system (their figure 1). In addition, C-rich interiors are poorly understood. Some exotic models exist that account SiC, C, and Fe layers, but neglect major rock-forming elements (e.g. Mg, O) [@Kuchner-Seager2005; @Bond-etal-2010]. In order to make meaningful predictions on C-rich interior structures, a better understanding of carbon-bearing compounds, their phase diagrams, phase equilibria, and EoSs are required [e.g., Miozzi et al. (in review) @Nisr-et-al-2017; @Wilson-and-Militzer-2014].

For reference, assuming a C-rich interior for the planet could lead to a larger $r_{\rm core+mantle}$ because SiC can be less dense than silicates (in its zinc-blende (B3) form), hence to a thinner gas layer ; but again these models suffer from large uncertainties. In particular, @Daviau-Lee-2017b show that B3 SiC decomposes into Si and C (diamond) above roughly 2000 K, which is likely to apply to 55 Cnc e's mantle. Also, @Daviau-Lee-2017a find that B3 SiC transitions to a rocksalt (B1) form at high pressures, which has a density very close to that of MgSiO$_3$. This would make an SiC planet undistinguishable from a silicate one from the mass radius relation only. It would also conveniently make our conclusions on the size of the mantle independent of whether it is made of silicates or of B1 SiC.

# Conclusions {#sec:conclu}

In this paper, we have characterized the possible interiors of 55 Cnc e starting with a rigorous investigation of the observations of its host star. Compared to previous work, we have adopted a more analytical approach, which allows us to use a prior in the H-R diagram and to obtain semi-analytically the joint PDF of the mass and radius of the star, then of the planet. We have estimated the uncertainties on these parameters carefully, taking inherent correlations into account. Besides the particular case of 55 Cnc e, our analysis helps to demonstrate the information value of different data types besides mass and radius: mass-radius-correlation and refractory element abundances.

We provide an analytical expression for the joint likelihood of the stellar luminosity and temperature directly from the observables. This formula allows us to skip a Monte Carlo analysis. In the case of 55 Cnc, we find that the stellar parameters are well enough constrained by interferometry with respect to our prior based on the *Hipparcos* catalog, which does not bring much significant information. The distribution of the stellar mass and radius is also derived analytically; they are very strongly correlated, thanks to the constraint on the stellar density. Compared to stellar evolution models, our stellar parameters are in good agreement, with an uncertainty encompassing the various outcomes of different models. We conclude that stellar evolution models are good in general, but should be used with great care for the case of individual stars: they provide appealing small uncertainty, but their accuracy is very sensitive to many parameters. The method we developed here seems to be a more reliable way of estimating stellar and thus planetary mass and radius, because it is based on direct measurements, and in particular that of the stellar radius (unfortunately not always available). Of course, if the age of the planet is needed (e.g., in the case of gas giant planets that contract as they evolve), stellar models would be a necessary step to infer it, via the dating of the host star.

Using the planetary mass and radius that we derived, we inferred the internal structure of the planet 55 Cnc e, using the model developed by @Dorn-etal-2017a. Our results show that the data on mass and radius, taken independently, allow to estimate the internal structure of the planet to some degree. Improved estimates can be obtained by accounting for (1) possible correlation of mass and radius or (2) abundance constraints that were discussed in previous studies. In the case of 55 Cnc e, the $0.3$ correlation is too small to have significant influence on interior estimates. In any case, there is a well-known inherent degeneracy such that a large number of interiors can fit even infinitely precise mass and radius. Assuming that the planet's ${\rm Fe}/{\rm Si}_{\rm mantle}$ and ${\rm Mg}/{\rm Si}_{\rm mantle}$ are similar to the star's helps contrain the internal structure of the planet much better, in particular the size of the core and the mantle composition, which is only poorly constrained by the mass-radius correlation.

We find that there is a low chance, of 5%, that the interior is purely rocky. The gas layer thickness is estimated to be 8% ($\pm$ 5%) of the total radius. We stress that a more precise estimate of the transit depth would allow us to increase significantly the mass-radius correlation of the planet, and thus to reduce significantly the uncertainty on the thickness and mass of the gaseous layer and the rocky interior, as well as on the core size[^6].

We warmly thank Diana Valencia for interesting discussions on the internal composition of planets, Florentin Millour for explanations concerning the *Hipparcos* catalog, Georges Kordopatis, Orlagh Creevey and Mathias Schultheis for insights on stellar models and populations.\
R.L. is funded by the European Union's Horizon 2020 research and innovation programme under the Marie Skłodowska-Curie grant agreement n. 664931.\
C.D. is funded by the Swiss National Science Foundation under the Ambizione grant PZ00P2_174028.

# Probability Density Function of $R_\star$

Let us deote $f_X$ as the PDF of $X$ and $F_X$ as its cumulative distribution function.

## From the observations of the angular diameter and the parallax {#subsec:Rfromthetapx}

The stellar radius $R_\star$ is the product of the angular radius ($\theta/2$) with the distance $d$, and the distance is proportional to the inverse of the parallax $p_\star$. Thus, one can write $$\begin{equation}
R_\star=\frac{\theta d}{2} = R_0\theta/p_\star
\end{equation}$$ where $R_0$ is a length, equal to $\frac{1 \rm pc}{2\,m_r} =
0.1075\,R_\odot$ if $\theta$ is in milliarcseconds (mas) and $p_\star$ in arcseconds (as).

As a consequence, $R_\star$ is lower than $R$ if and only if $\theta$ is lower than $p_\star(\frac{R}{R_0})$, whatever the value of $p_\star$. Thus, the probability that $R_\star<R$ reads: $$\begin{equation}
F_{R_\star}(R) = \int_0^\infty f_{p_\star}(p)\left[\int_0^{\frac{pR}{R_0}}f_\theta(t)\,{\rm d}t\right]\ {\rm d}p
\end{equation}$$ From this, one deduces the PDF of $R_\star$ as follows : $$\begin{eqnarray*}
f_{R_\star}(R) & = & F_{R_\star}'(R)\\
 & = & \int_0^\infty f_{p_\star}(p)\frac{\partial}{\partial R}\left[\int_0^{\frac{pR}{R_0}}f_\theta(t)\,{\rm d}t\right]\ {\rm d}p\\
 & = & \int_0^\infty f_{p_\star}(p)\left(\frac{p}{R_0}\right)f_\theta\left(\frac{p\,R}{R_0}\right)\ {\rm d}p\\
 & = & \frac{1}{R_0}\int_0^\infty p\, f_{p_\star}(p)f_\theta\left(\frac{p\,R}{R_0}\right)\ {\rm d}p
\end{eqnarray*}$$

A change of variable ($t=p\,R/R_0$) gives the equivalent expression used in the main text: $$\begin{equation}
f_{R_\star}(R)  =  \frac{R_0}{R^2}\int_0^\infty t\, f_{p_\star}\left(\frac{R_0\,t}{R}\right)f_\theta(t)\ {\rm d}t\ .
\label{eq:fR_thetapx}
\end{equation}$$

## From the joint PDF of ($L_\star,T_{\rm eff}$) {#RfromLT}

The stellar luminosity and effective temperature are connected through the stellar radius as: $L_\star=4\pi R_\star^2\sigma_{\scriptscriptstyle\!\rm SB}T_{\rm eff}^4$. Therefore, $R_\star<R$ is equivalent to $L_\star<4\pi R^2\sigma_{\scriptscriptstyle\!\rm SB}T_{\rm eff}^4$. Hence, with $f_{\rm HR}$ the joint PDF of $L_\star$ and $T_{\rm eff}$: $$\begin{eqnarray*}
F_{R_\star}(R) & = & \iint_{\{l<4\pi R^2\sigma_{\scriptscriptstyle\!\rm SB}t^4\}} f_{\rm HR}(l,t)\ {\rm d}l\ {\rm d}t\\
 & = & \int_{t=0}^\infty \left[\int_0^{4\pi R^2\sigma_{\scriptscriptstyle\!\rm SB}t^4} f_{\rm HR}(l,t)\ {\rm d}l\right]\, {\rm d}t
\end{eqnarray*}$$ Again, derivation with resect to $R$ gives the PDF of $R_\star$:

$$\begin{eqnarray}
\hspace{-1cm}f_{R_\star}(R) & = & \int_{t=0}^\infty (8\pi R\sigma_{\scriptscriptstyle\!\rm SB}t^4)\,f_{\rm HR}(4\pi R^2\sigma_{\scriptscriptstyle\!\rm SB}t^4,t)\ {\rm d}t\\
 & = & \frac{2}{R}\int_{t=0}^\infty L_{(R,t)}\, f_{\rm HR}(L_{(R,t)},t)\ {\rm d}t
\end{eqnarray}$$ where $L_{(R,t)} = 4\pi R^2\sigma_{\scriptscriptstyle\!\rm SB}t^4$.\
Noting $T_{(R,l)} = \left(\frac{l}{4\pi R^2\sigma_{\scriptscriptstyle\!\rm SB}}\right)^{1/4}$, and making the change of variable $l=L_{(R,t)}$ leads to the equivalent expression: $$\begin{equation}
f_{R_\star}(R) =  \frac{1}{2R}\int_{l=0}^\infty T_{(R,l)}\, f_{\rm HR}(l,T_{(R,l)})\ {\rm d}l
\label{eq:fR_LT}
\end{equation}$$

## Equivalence of the two methods

Below, we show that Eq. ([\[eq:fR_LT\]](#eq:fR_LT){reference-type="ref" reference="eq:fR_LT"}) is exactly equivalent to Eq. ([\[eq:fR_thetapx\]](#eq:fR_thetapx){reference-type="ref" reference="eq:fR_thetapx"}) if $f_{\rm HR}$ is taken as $\mathcal{L}_{\rm HR}$ derived from $f_{F_{\rm bol}}$, $f_{p_\star}$, and $f_\theta$ in Appendix [6](#app:PDF_LT){reference-type="ref" reference="app:PDF_LT"} (see Eq. ([\[eq:Ld_LT\]](#eq:Ld_LT){reference-type="ref" reference="eq:Ld_LT"}) ). This means that using Eq. ([\[eq:fR_LT\]](#eq:fR_LT){reference-type="ref" reference="eq:fR_LT"}), one does not lose any information compared to directly using $f_\theta$ and $f_{p_\star}$ with Eq. ([\[eq:fR_thetapx\]](#eq:fR_thetapx){reference-type="ref" reference="eq:fR_thetapx"}) :

$$\begin{eqnarray*}
f(R) & = & \frac{2}{R}\int_{t=0}^\infty L_{(R,t)} \mathcal{L}_{\rm HR}(L_{(R,t)},t)\, {\rm d}t\\
 & = & \frac{2}{R}\int_{t=0}^\infty L_{(R,t)} \frac{{4 \rm pc}\sqrt{\pi/\sigma_{\scriptscriptstyle\!\rm SB}}m_r}{L_{(R,t)}^{3/2}\,t^3}%\\
% & & \hspace{-1.5cm}
\times\left[\int_{\tau=0}^\infty \tau\, f_{F_{\rm bol}}(\tau)f_\theta\left(m_r\sqrt{\frac{4\tau}{\sigma_{\scriptscriptstyle\!\rm SB}t^4}}\right)f_{p_\star\!}\left(\sqrt{\frac{4\pi \tau}{L_{(R,t)}}}{1\rm pc}\right) {\rm d}\tau \right]\, {\rm d}t\\
 & = & \frac{4\,{\rm pc}\ m_r}{R^2}\int_{t=0}^\infty\frac{{\rm d}t}{\sigma_{\scriptscriptstyle\!\rm SB}\,t^5} \left[\int_{u=0}^\infty \frac{\sigma_{\scriptscriptstyle\!\rm SB}t^4}{4\,m_r^2}u^2%\right.\\
% & & \hspace{-1.5cm}\times \left.
f_{F_{\rm bol}}\left(\frac{\sigma_{\scriptscriptstyle\!\rm SB}t^4 u^2}{4\,m_r^2}\right) f_\theta(u) f_{p_\star\!}\left(\sqrt{\frac{\sigma_{\scriptscriptstyle\!\rm SB}\,t^4}{L_{(R,t)}}}\frac{u({1\rm pc})}{m_r}\right) \frac{\sigma_{\scriptscriptstyle\!\rm SB}t^4 u\,{\rm d}u}{2\,m_r^2}\right]\\
 & = & \frac{{1\,\rm pc}}{2R^2m_r}\iint{\rm d}u\ {\rm d}t\ \sigma_{\scriptscriptstyle\!\rm SB}\,t^3\,u^3 %\\
% & & \ \ \ \ \ \ \ \ \ \ \times
f_{F_{\rm bol}}\left(\frac{\sigma_{\scriptscriptstyle\!\rm SB}t^4 u^2}{4}\right) f_\theta(u) f_{p_\star\!}\left(\frac{u({1\rm pc})}{2Rm_r}\right)\\
 & = & \frac{R_0}{R^2}\int_{u=0}^\infty {\rm d}u\ f_\theta(u) f_{p_\star\!}\left(\frac{uR_0}{R}\right) \, u%\\
% & & \ \ \ \ \ \ \ \ \ \ \times
\int_{t=0}^\infty \sigma_{\scriptscriptstyle\!\rm SB}t^3 u^2 f_{F_{\rm bol}}\left(\frac{\sigma_{\scriptscriptstyle\!\rm SB}t^4 u^2}{4}\right)  {\rm d}t\\
 & = & \frac{R_0}{2R^2}\int_{u=0}^\infty {\rm d}u\ f_\theta(u) f_{p_\star\!}\left(\frac{uR_0}{R}\right) \, u\,\underbrace{\int_{\phi=0}^\infty f_{F_{\rm bol}}\left(\phi\right)  {\rm d}\phi}_{1}
%\frac{\dd u}{\sqrt{L_{(R,t)}}\,t^3}\times\\
% & & t^4u^3 f_{F_{\rm bol}}\left(\frac{\ssb t^4 u^2}{4}\right)
\end{eqnarray*}$$

Hence, one can apply the prior $f_{\rm Hip}^0$ to the PDF of $R_\star$ by simply calculating $$\begin{equation}
f_{R_\star}(R) =  \frac{1}{2R} \int_0^\infty L_{(R,t)}
   \mathcal{L}_{\rm HR}(L_{(R,t)},t)f_{\rm Hip}^0(L_{(R,t)},t)\, {\rm d}t\ .
\label{eq:fR_prior}
\end{equation}$$

# Likelihood of $L_\star$ and $T_{\rm eff}$, Given Obseravtions {#app:PDF_LT}

Here, we want to derive analytically the likelihood of a pair of luminosity and effective temperature against the observations of the angular diameter, parallax, and bolometric flux. The PDFs of the observables are denoted respectively $f_\theta$, $f_{p_\star}$ and $f_{F_{\rm bol}}$. The likelihood in the H-R plane is denoted $\mathcal{L}_{\rm HR}$.

Be $H=\{L<a;T<b\}$ a subset of the universe $\Omega=\{L\in\mathbb{R}+;T\in\mathbb{R}+\}$. The probability of $H$ is naturally $$\mathbb{P}(H)\equiv P(a,b)=\int_{u=0}^{u=a}\int_{v=0}^{v=b} \mathcal{L}_{\rm HR}(u,v)\,{\rm d}v\,{\rm d}u\ .$$ Hence $$\begin{equation}
\mathcal{L}_{\rm HR}(a,b)=\frac{\partial^2P(a,b)}{\partial a\  \partial b}\ .
\label{eq:fLTderiv}
\end{equation}$$

$L_\star$ and $T_{\rm eff}$ are given as functions of the observable quantities by : $$\begin{eqnarray}
\label{eq:L}
L & = & 4\pi\,F_{\rm bol}\,\left(\frac{1\,\rm pc}{p_\star\,\rm[as]}\right)^2\\
\label{eq:T}
T_{\rm eff} & = & \left(\frac{4}{\sigma_{\scriptscriptstyle\!\rm SB}}\right)^{\!1/4}F_{\rm bol}^{\ 1/4}\,(\theta\,{\rm [rad]})^{-1/2}\ ,
\end{eqnarray}$$ where $\sigma_{\scriptscriptstyle\!\rm SB}$ is the Stefan--Boltzmann constant. Thus, $H$ can also be defined as: $$\left\{F_{\rm bol}=t\in\mathbb{R}\,; \ p_\star{\rm [as]}>{1\,\rm
  pc}\sqrt{\frac{4\pi t}{a}}\,; \ \theta{\rm [mas]} >
m_r\sqrt{\frac{4\,t}{\sigma_{\scriptscriptstyle\!\rm SB}\,b^4}}\right\}$$ (where $m_r=2.06\cdot 10^8$ is the number of mas in 1 rad). From now on, $\theta$ is implicitely given in mas, and $p_\star$ in as. The probability of the event $H$ is given by $$\begin{equation}
\mathbb{P}(H) = \int_0^{+\infty} f_{F_{\rm bol}}(t)\times \left[1-F_{p_\star}\left(\sqrt{\frac{4\pi t}{a}}{1\,\rm pc}\right)\right]\times\left[1-F_\theta\left(m_r\sqrt{\frac{4\,t}{\sigma_{\scriptscriptstyle\!\rm SB}\,b^4}}\right)\right]\ {\rm d}t
\label{eq:PdeH}
\end{equation}$$ Using Eqs. ([\[eq:fLTderiv\]](#eq:fLTderiv){reference-type="ref" reference="eq:fLTderiv"}) and ([\[eq:PdeH\]](#eq:PdeH){reference-type="ref" reference="eq:PdeH"}), one obtains $$\begin{eqnarray*}
\mathcal{L}_{\rm HR}(a,b) & = & \frac{\partial^2}{\partial a\  \partial b}P(a,b)\\
 & = & \frac{\partial}{\partial a}\Bigg\{ \int_0^{+\infty} f_{F_{\rm bol}}(t)\times \left[1-F_{p_\star}\left(\sqrt{\frac{4\pi t}{a}}{1\,\rm pc}\right)\right]%\\
% & & \ \ \ \ \ \ \ 
\times \frac{\partial}{\partial b}\left(\left[1-F_\theta\left(m_r\sqrt{\frac{4\,t}{\sigma_{\scriptscriptstyle\!\rm SB}\,b^4}}\right)\right]\right)\ {\rm d}t\Bigg\}\\
 & = & \frac{\partial}{\partial a}\Bigg\{ \int_0^{+\infty} f_{F_{\rm bol}}(t)\times \left[1-F_{p_\star}\left(\sqrt{\frac{4\pi t}{a}}{1\,\rm pc}\right)\right]%\\
% & & \ \ \ \ \ \ \ 
\times \left[-\frac{-2m_r}{b^3}\sqrt{\frac{4t}{\sigma_{\scriptscriptstyle\!\rm SB}}}f_\theta\left(m_r\sqrt{\frac{4\,t}{\sigma_{\scriptscriptstyle\!\rm SB}\,b^4}}\right)\right]\ {\rm d}t\Bigg\}\\
% & & \ \vspace{30pt}\\
 & = & \int_0^{+\infty} f_{F_{\rm bol}}(t)\times\frac{\partial}{\partial a}\left\{\left[1-F_{p_\star}\left(\sqrt{\frac{4\pi t}{a}}{1\,\rm pc}\right)\right]\right\}%\\
% & & \ \ \ \ \ \ \ 
\times \left[\frac{4m_r}{b^3}\sqrt{\frac{t}{\sigma_{\scriptscriptstyle\!\rm SB}}}f_\theta\left(m_r\sqrt{\frac{4\,t}{\sigma_{\scriptscriptstyle\!\rm SB}\,b^4}}\right)\right]\ {\rm d}t\\
% & & \ \vspace{30pt} \\
 & = & \int_0^{+\infty} f_{F_{\rm bol}}(t)\times\left\{\frac{1\,\rm pc}{2}\sqrt{\frac{4\pi t}{a^3}}f_{p_\star}\left(\sqrt{\frac{4\pi t}{a}}{1\,\rm pc}\right)\right\}%\\
% & & \ \ \ \ \ \ \ 
\times \left[\frac{4m_r}{b^3}\sqrt{\frac{t}{\sigma_{\scriptscriptstyle\!\rm SB}}}f_\theta\left(m_r\sqrt{\frac{4\,t}{\sigma_{\scriptscriptstyle\!\rm SB}\,b^4}}\right)\right]\ {\rm d}t%\\
%\Ld_{\rm HR}(a,b)  & = & \frac{4\sqrt{\pi}}{b^3\sqrt{\ssb a^3}}\ \int_0^{+\infty} f_{F_{\rm bol}}(t)\,f_{\px}\left(\sqrt{\frac{4\pi t}{a}}\right)f_\theta\left(\sqrt{\frac{4\,t}{\ssb\,b^4}}\right)\ t\ \dd t
\end{eqnarray*}$$ $$\begin{equation}
\mathcal{L}_{\rm HR}(a,b) = \frac{{4\,\rm pc}\sqrt{\pi}m_r}{b^3\sqrt{\sigma_{\scriptscriptstyle\!\rm SB}a^3}}\times \int_0^{+\infty} f_{F_{\rm bol}}(t)\,f_{p_\star}\left(\sqrt{\frac{4\pi t}{a}}\right)f_\theta\left(\sqrt{\frac{4\,t}{\sigma_{\scriptscriptstyle\!\rm SB}\,b^4}}\right)\ t\,{\rm d}t
\end{equation}$$

# Density of stars in the H-R plane in the solar neighborhood from the *Hipparcos* catalog

From the *Hipparcos* catalog, we compute the effective temperature and luminosity of each star as follows.

- The effective temperature is a function of the $B-V$ color index (provided in the catalog) given by @Flower-1996 and @Torres-2010 [Table 2].

- The luminosity $L_\star$ is given by : $$\begin{equation}
  2.5\,\log(L/L_\odot) = 4.74 - \underbrace{H_p+BC-5\,\log(1/p_\star\ [{\rm as}])}_{M_{\rm bol}}\ ,
  \label{eq:Lum_Hip}
  \end{equation}$$ where $M_{\rm bol}$ is the absolute bolometric magnitude ($4.74$ being the solar absolute bolometric magnitude adopted here), with $H_p$ the *Hipparcos* magnitude, $BC$ the bolometric correction, and $p_\star$ the parallax. $H_p$ and $p_\star$ are in the catalog. For $BC$, we fit linearly @Cayrel-etal-1997 in the region of interest for us ($5000\,K<T_{\rm eff}<5500\,K$) as : $BC = -2.44 + 0.0004\,T_{\rm eff}\,.$ We have checked that a more elaborate functional form of $BC$ has no significant impact on the density of stars near 55 Cnc.

Then, the density of stars next to the point $(L_0,T_0)$ is defined as $$\begin{equation}
f_{\rm Hip}^0(L_0,T_0) = \sum_{{p_\star}_{,i}>14.6\,\rm mas} \exp \left\{ - \frac12
\left(\frac{\log(L_0)-\log(L_i)}{0.08}\right)^2 -
\frac12\left(\frac{T_0-T_i}{100\,K}\right)^2 \right\}
\label{eq:rho_Hip}
\end{equation}$$ where the widths of the Gaussian kernels in $L_\star$ and $T$ have been chosen to obtain a smooth density function in the region next to 55 Cnc without losing information. The sum goes through all the stars of the catalog with a parallax larger than $14.6$ mas (while that of 55 Cnc is $81$ mas). Indeed, brighter stars can be seen from larger distances, and hence would be overrepresented in the catalog without a distance limit. The *Hipparcos* catalog is complete up to a magnitude $H_p = 8.5$, and we want our sample to be complete up to $\log(L/L_\odot)=0.1$ to cover well the 55 Cnc region of the HR diagram. The limit parallax then results from Eq. ([\[eq:Lum_Hip\]](#eq:Lum_Hip){reference-type="ref" reference="eq:Lum_Hip"}).

# Calculation of the joint PDF of $M_\star$ and $R_\star$ from the PDFs of $R_\star$ and $\rho_\star$

The subset $K=\{M_\star<a;R_\star<b\}$ of the $M_\star-R_\star$ space is identical to $\{\rho_\star < \frac{3 a}{4\pi
  R_\star^{\,3}};R_\star<b\}$. Hence, $\mathbb{P}(K)=\displaystyle\int_{R_\star=0}^{\ b}\int_{\rho_\star=0}^{\frac{3 a}{4\pi
    R_\star^{\,3}}}f_{R_\star}(R_\star)f_{\rho_\star}(\rho_\star)\ {\rm d}\rho_\star\,{\rm d}
R_\star$ .

$$\begin{eqnarray*}
\mathcal{L}_{MR_\star}(a,b) & = & \frac{\partial^2 \mathbb{P}(K)}{\partial a\ \partial b}\\
 & = & \frac\partial{\partial b}\int_{R_\star=0}^b
       f_{R_\star}(R_\star)\,\frac\partial{\partial a}
       \int_{\rho_\star=0}^{\frac{3 a}{4\pi R_\star^{\,3}}}f_{\rho_\star}(\rho_\star)\ 
       {\rm d}\rho_\star\,{\rm d}R_\star\\
 & = & \frac\partial{\partial b}\int_{R_\star=0}^b
       f_{R_\star}(R_\star)\,\frac{3}{4\pi R_\star^{\,3}}\,f_{\rho_\star}
       \left(\frac{3a}{4\pi R_\star^{\,3}}\right)\ {\rm d}R_\star\\
 & = & f_{R_\star}(b)\,\frac{3}{4\pi b^{\,3}}\,f_{\rho_\star}
       \left(\frac{3a}{4\pi b^{\,3}}\right)\\
\mathcal{L}_{MR_\star}(a,b) & = & \frac{3}{4\pi b^{\,3}}\,f_{\rho_\star}
       \left(\frac{3a}{4\pi b^{\,3}}\right)\,f_{R_\star}(b)
\end{eqnarray*}$$

[^1]: ` ftp://cdsarc.u-strasbg.fr/pub/cats/I/239/hip_main.dat.gz`

[^2]: The CES2MO tool is a stellar model optimization pipeline. It has been described in @Lebreton-Goupil-2014 and is based on the Cesam2k stellar evolution code [@Morel-Lebreton-2008].

[^3]: The eccentricity of 55 Cnc e is $0.028$ in `exoplanet.eu`, which makes the assumption $e\approx 0$ reasonable.

[^4]: A careful reader may notice that $8.703/2.023^3=1.051$, not $1.06$. Because $<R_p^{\,3}>\neq<R_p>^3$, the expected value of $\rho_p$ is not given by $<M_p>/<R_p>^3$.

[^5]: Note added after publication : this has been done just a few weeks after the publication of this article by @Bourrier+18. See @Crida+2018b for an update of this paper. For reference, we eventually find $M_p = 8.59 \pm 0.43\ M_\oplus$, $R_p = 1.947 \pm
      0.038\ R_\oplus$, with a correlation of $c=0.54$.

[^6]: The reader is referred to @Crida+2018b for an update of this work using new, better data.
