---
citation_key: Gaebert2023Paramater
arxiv_id: 2302.14422
arxiv_url: "https://arxiv.org/abs/2302.14422"
title: "Paramater Optimization for Manipulator Motion Planning using a Novel Benchmark Set"
authors_short: "Carl Gaebert et al."
year: 2023
direction_tag: O_dense_forest_narrow_passage
source: mineru-vlm
converter: mineru-open-api
model: vlm
converted_at: 2026-06-25T08:28:41Z
origin: ai+web
reviewed: false
---

# PARAMETER OPTIMIZATION FOR MANIPULATOR MOTION PLANNING USING A NOVEL BENCHMARK SET

Carl Gaebert, Sascha Kaden, Benjamin Fischer and Ulrike Thomas<sup>∗</sup>

## ABSTRACT

Sampling-based motion planning algorithms have been continuously developed for more than two decades. Apart from mobile robots, they are also widely used in manipulator motion planning. Hence, these methods play a key role in collaborative and shared workspaces. Despite numerous improvements, their performance can highly vary depending on the chosen parameter setting. The optimal parameters depend on numerous factors such as the start state, the goal state and the complexity of the environment. Practitioners usually choose these values using their experience and tedious trial and error experiments. To address this problem, recent works combine hyperparameter optimization methods with motion planning. They show that tuning the planner’s parameters can lead to shorter planning times and lower costs. It is not clear, however, how well such approaches generalize to a diverse set of planning problems that include narrow passages as well as barely cluttered environments. In this work, we analyze optimized planner settings for a large set of diverse planning problems. We then provide insights into the connection between the characteristics of the planning problem and the optimal parameters. As a result, we provide a list of recommended parameters for various use-cases. Our experiments are based on a novel motion planning benchmark for manipulators which we provide at https://mytuc.org/rybj.

## 1 Introduction

For more than two decades, robot motion planning has been an active field of research. One prominent group of approaches are sampling-based motion planning (SBMP) algorithms. They are well-suited to address the problem of high-dimensionality which is a main challenge in many robotics applications. Instead of searching the complete configuration space, these algorithms use random sampling to find a feasible solution. Approaches such as RRT\* [1] and RRT\*-Connect [2] sample the robot’s configuration space to grow a collision-free tree connecting start and goal. While doing so, they also optimize the existing tree to minimize a given cost function. In contrast to static scenarios, human-robot interaction (HRI) calls for optimized solutions within a very short planning time. To this end, many approaches have been presented which increase the performance of sampling-based planners. They address the problem of narrow passages [3, 4], use adaptive sampling strategies [5] or even learning-based methods [6, 7, 8]. Despite all these improvements, the performance of the planner is still heavily influenced by its most basic parameter settings, namely the step size s and the goal bias $b _ { g o a l }$ . Moreover, the settings recorded in the original works are often related to mobile robot applications. In industry, practitioners are thus often faced with fine-tuning basic parameter settings by hand for manipulators. A recent line of research therefore aims at automatizing this process through optimization. In recent years, several approaches have addressed the problem of automatic hyperparameter tuning in SBMP for manipulators. In [9], the authors utilize a random forest model to tune parameters of several algorithms provided in the Open Motion Planning Library (OMPL) [10]. The authors achieved reduced planning times and costs in a few pre-defined pick-and-place scenarios. Cano et al. investigated several optimization methods while considering the BKPIECE [11] and RRT-Connect [12] algorithms implemented in OMPL. The authors show that planning time can be reduced by a factor of 4.5. In addition, randomized planning problems are used to show that the tuned parameters generalize well across various setups from the same problem distribution. Moll et al. use Bayesian Optimization and Hyperband (BOHB) [13] to find optimal settings in an extensive search space that includes several planning algorithms and their parameters. Hence, the authors manage to find the best performing approach together with its tuned parameters. For evaluating their approach, the authors use several classes of planning problems such as reaching into a shelf or into a box. The considered optimization criteria are planning and execution speed. In the same work, the authors also demonstrate that optimizing on a small set of problem classes can lead to good performance in all of them. However, it was not shown to which number of classes and to which variety in complexity this holds. For example, a planner optimized on a trivial problem such as in Fig. 1a may still work well when introducing a few more obstacles to the scene. However, it is likely to fail in very complex environments like the one shown in Fig. 1b. Furthermore, none of the mentioned works utilize a parallelized planner. It is thus not clear to which extent parameter optimization can improve the results in such a setup. To this end, our work provides the following contributions:

![](Gaebert2023Paramater_figs/a7710a58da1b21f054e60484bc66a5b170dd983ae565b155e161f4e40e69e726.jpg)  
(a) Trivial environment

![](Gaebert2023Paramater_figs/5e27629e1a3f892b32e97ad37924bb64f0e5d44cc68e37688cea6579543e869e.jpg)  
(b) Complex environment  
Figure 1: A seven DoF manipulator operating in two different environments. (a): Almost no obstacles are present which allows for a higher step size and goal bias during sampling. (b): Complex environment with many narrow passages. A smaller goal bias and step size is thus recommended.

• We provide a benchmark dataset for manipulator motion planning consisting of 20 environments and over 200 planning problems of different complexity.

• We utilize this dataset to investigate how well optimized parameters generalize across a very diverse set of planning problems.

• We analyze the distribution of optimized parameters and connect them to the characteristics of the planning problems. In consequence, we can provide a list of recommendations to practitioners for setting up their planner in a specific scenario.

In the remainder of the paper, we first provide a brief summary of the optimization algorithm. Since we use results from stochastic planners, we also review a method for extracting clusters from noisy datasets. Next, we introduce the optimization function used throughout this work. In a subsequent step, we present details of the motion planning benchmark for manipulators in 4. Next, we point out the challenges of finding suitable parameters for diverse planning problems. Finally, we experimentally derive a list of recommendations for optimal planning parameters depending on the problem.

## 2 Background

## 2.1 Bayesian Optimization and Hyperband

In SBMP, costs and planning time heavily depend on the planner’s parameters. A very low goal bias, for example, can lead to a bad performance even in simple environments. Such sensitivity towards hyperparameter choices is also commonly observed in areas of Deep Learning. Therefore, automatic hyperparameter tuning is an active field of research beyond robotics. Formally, the performance of a motion planning algorithm can be defined as a function $f : \mathcal { X } \to \bar { \mathbb { R } }$ of its parameters x. The goal of the optimization procedure is to find the parameters $x ^ { * }$ for which f is minimized. Typically, the function f is expensive to validate. However, it can be approximated by sampling from the parameter space X . A recent work by Falkner et al. [13] in this direction combines the strengths of Bayesian Optimization with a Hyperband scheduler [14]. In line with the work of Moll et al. [15], we utilize this approach to tune the parameters of our motion planning algorithm. In BOHB the Hyperband scheduler is used to identify the best out of $n _ { t r i a l s }$ randomly initialized planner configurations. It does so by using Successive Halving [16] (as cited in [13]) and assigning resources to the most promising trials. Instead of relying on random samples, BOHB uses kernel density estimators to generate new promising trials based on previous results. The resulting increase in efficiency is crucial for our experiments since they require solving hundreds of challenging motion planning problems.

## 2.2 Clustering Large and Noisy Datasets

SBMP algorithms rely on stochastic processes and thus deliver non-deterministic solutions. This has to be taken into account while analyzing results from such sources. When clustering such datasets, one thus has to cope with outliers that do not necessarily belong to a cluster. One established algorithm for such use-cases is Density Based Spatial Clustering of Applications with Noise (DBSCAN) [17]. The advantage of using this algorithm over K-Means, for example, is that clusters do not have to be of convex shape. Instead, they are viewed as regions with high density which are separated by areas of low density. The method is based on the concept of core samples. A sample is considered a core sample when a number of min samples are within a distance of $\varepsilon \ { \mathrm { t o } }$ it. Besides core samples, a cluster can also contain samples which are within ε to one of the core samples. Therefore, the algorithms does not require a number of clusters to look for but a distance metric and the number of core samples. It thus allows for marking too distant samples as outliers.

## 3 Methodology

In HRI one is typically interested in optimizing for two objectives simultaneously: planning time and costs. The latter can vary depending on the application and may involve state as well as distant costs. In contrast to works like [15], we rely on the optimizing planner $\mathrm { R R T ^ { * } } { _ - }$ Connect [2] only. For this, we use a custom and highly-parallelized implementation. This allows us to combine these two objectives into a single objective function which would not be possible using non-optimizing planners such as RRT.

For a single planning problem p from a start configuration $\theta _ { s t a r t }$ to a goal configuration $\theta _ { g o a l }$ , we define the combined costs $c ( p )$ as follows:

$$
c (p) = w _ {t} * t + \frac {c _ {C}}{| | \theta_ {s t a r t} - \theta_ {g o a l} | | _ {2}}\tag{1}
$$

The cost consists of the planning time t in seconds and the path length in configuration space $c _ { C }$ . The latter is given in radian and normalized using the shortest path length possible. In addition, we weight the influence of the planning time throughout this paper with $w _ { t } = 3$

Since we are interested in an approximation of our planner’s performance in various workspaces, we consider a whole set $\mathcal { P }$ of n problems. The final objective function f is then defined as

$$
\begin{array}{c} f (\mathcal {P}) = \mathcal {Q} _ {0. 7} \{s _ {1},..., s _ {m} \} \\ \text { with } s _ {j} = \sum_ {n} c (p _ {n}). \end{array}\tag{2}
$$

This can be interpreted as follows: We solve all planning problems in $\mathcal { P }$ and sum up the costs calculated using (1). The process is repeated m times which results in a distribution of estimates costs for this trial. In line with [15], we then take the 0.7-quanttile $\mathcal { Q } _ { 0 . 7 }$ of this distribution as our estimate. This is done to account for the highly stochastic nature and the high variance of solutions obtained by SBMP algorithms. Due to the complexity of the environments, certain parameter configurations might perform very poorly. It is thus necessary to restrict the maximum planning time to $t _ { m a x }$ . In cases where no solution was found within $t _ { m a x } ,$ , we use a cost value of $c ( p ) = 3 * t _ { m a x } + \bar { 1 0 0 }$ . Moreover, the possible ranges for the goal bias $b _ { g o a l }$ and step size s are significantly different. Using the Euclidean distance for clustering the optimal settings would thus favor clusters with a wide range of goal bias parameters. For this reason, we introduce a distance metric that scales the distance in the goal bias dimension using the ratio of the parameter ranges. The distance between parameter settings a and b are then calculated using the step sizes $s _ { a }$ and $s _ { b }$ as well as the goal bias settings $b _ { g o a l , a }$ and $b _ { g o a l , b }$ as shown below.

$$
d (a, b) = | | s _ {a} - s _ {b} | | _ {2} + 2. 9 \times | | b _ {\text { goal }, a} - b _ {\text { goal }, b} | | _ {2}.\tag{3}
$$

## 4 Motion Planning Benchmark for Manipulators

Related works utilize a wide range of planning problems and applications for evaluation. However, they are often not made publically available which hinders comparing results to previous works. Moreover, they are usually based on randomized environments or tailored towards a specific problem class. Our contribution is thus to provide a manipulator motion planning benchmark (see Fig. 2). It consists of 20 environments with several robot configurations per environment. Each environment e can be used to construct a set of possible planning problems $\mathcal { P } _ { e } .$ For now, only configurations for the Kuka iiwa manipulator are provided. However, we provide Blender and Coppelia files for each environment which allows for including other manipulators. Furthermore, the benchmark is independent of any planning software. Hence, it can also be used with well-established tools such as the OMPL benchmark pipeline [18]. In total, the benchmark contains 214 possible planning problems that can be generated by combining the provided configurations. As it can be seen in Fig. 2, the provided planning problems contain several narrow passages and thus yield a challenge for most state-of-the-art algorithms. The whole dataset can be downloaded from https://mytuc.org/rybj.

![](Gaebert2023Paramater_figs/770df0b34c73e98b0a365f549fdcc552ae7aceb7ab9ff0cd67bc5b8fe5ea38c1.jpg)  
(a) $\mathcal { P } _ { 2 }$

![](Gaebert2023Paramater_figs/46d9a9d90161afe6b6eeb1da425fee848a19228f6ae03592773d3bb926078dd3.jpg)  
(b) $\mathcal { P } _ { 3 }$

![](Gaebert2023Paramater_figs/eaff56e0a535c13056f98afa27db7fd0ba6aa624ae0b5207e87eec634c808097.jpg)  
(c) ${ \mathcal { P } } _ { 5 }$

![](Gaebert2023Paramater_figs/abec093989119354091213ed3abb9ff656f9c344a6b1d90263dac2d6832d6d3c.jpg)  
(d) $\mathcal { P } _ { 7 }$

![](Gaebert2023Paramater_figs/4718114bf0952f13efdb77e5c431eeadfceec264ed86d72b8367bf23770f636a.jpg)  
(e) $\mathcal { P } _ { 8 }$

![](Gaebert2023Paramater_figs/b1a1b4e6fee11026d438d65d59da825dc484790c34c18aa234144a9c6f750c1b.jpg)  
(f) $\mathcal { P } _ { 1 6 }$

![](Gaebert2023Paramater_figs/ac06c1d761201ca7010d2ecaca125915dfe5655ba844c203b4b5b8c9a12e4c4b.jpg)  
(g) $\mathcal { P } _ { 1 7 }$

![](Gaebert2023Paramater_figs/0103a9c3dca874a68a27307b0b4c095a6ab525087352a5525f738e30e52ed676.jpg)  
(h) $\mathcal { P } _ { 1 8 }$

![](Gaebert2023Paramater_figs/612c7fd87a1f3686388aa3f9ca260c0be3891da1e57a586a222d5b744edb1b58.jpg)  
(i) $\mathcal { P } _ { 1 9 }$

![](Gaebert2023Paramater_figs/de7e169f0879148627d8dab9bf25aa08af8d2807f51843bdb2e2d11ce011d99e.jpg)  
(j) $\mathcal { P } _ { 2 0 }$  
Figure 2: Ten example environments included in the presented benchmark. Some of them contain narrow passages. Others do not include many obstacles and are thus easier to solve.

## 5 Experiments

In the following, we conduct two experiments using the previously presented benchmark of planning problems. For all our experiments we use our own $\mathrm { \bar { R } R T ^ { * } } { _ { - } }$ Connect implementation. In contrast to most implementations in OMPL, the algorithm is highly parallelized. We restrict number of threads per trial to eight. Throughout our experiments, we optimize the parameters goal bias $b _ { g o a l } \in ( 0 . 0 5 , 0 . 7 5 )$ and step size $s \in ( 1 5 ^ { \circ } , 1 3 5 ^ { \circ } )$ . We use the BOHB implementation provided by Tune [19]. For each problem within a trial, the planning time is restricted to $t _ { m a x } = 2 0 \mathrm { s } .$ . All experiments are executed on a workstation with two Intel Xeon E5-2670 v3 CPUs, each with 12 processor cores and 64 GB of Ram.

In the following, we first demonstrate the challenge of finding an optimized planner configuration for multiple environments. In a second experiment, we extend the set of considered problems to obtain a distribution of optimal parameters. This allows for extracting a set of suggested parameters depending on the setup.

## 5.1 Optimizing on a Single Environment

In the first experiment we investigate weather a planner tuned on one environment can generalize across environments with other characteristics. For this, we used the BOHB algorithm on the planning problem sets $\mathcal { P } _ { 2 } , \mathcal { P } _ { 3 }$ and ${ \mathcal { P } } _ { 5 }$ (see Fig. 2(a)-(c)). As it can be seen, the three environments differ in the number of obstacles and narrow passages. Moreover, some planning problems within an environment are more challenging than others. In ${ \mathcal { P } } _ { 3 } ,$ for example, finding a path to the other side of the arch is more challenging than finding one to a configuration on the same side. Hence, our first goal is to test the generalization capabilities of an optimized planner. For this, we run BOHB with 100 trials on all problems of an environment and test the results on all three. For obtaining a stable loss estimate per environment, we sum up the costs for all problems. The process was repeated five times for each environment e and the 0.7-quantile was used as a loss $L _ { e }$ . We also optimize the parameters using the combined set $\mathcal { P } _ { 2 , 3 , 5 }$ . In addition, we include the settings suggested by OMPL for the Kuka iiwa manipulator as a baseline. The results can be seen in Table 1. The first column describes from which source the optimized parameters s and $b _ { g o a l }$ were taken. Their values can be seen in column three and four. The remaining columns show the mean loss and the 0.7-quantile for all environments. The last column shows the average loss over all environments $\mathcal { P } _ { 2 } , \mathcal { P } _ { 3 }$ and ${ \mathcal { P } } _ { 5 }$

Looking at the optimized parameters, it can be seen that the step size in $\mathcal { P } _ { 2 }$ has the smallest value which most-likely results from the robot reaching inside the walls. Environment five, on the other hand, is characterized by a very high step size and goal bias because not many obstacles are present within the scene. In consequence, the loss values for the hold-out environments are much higher. Therefore, the optimized parameters are not applicable across all environments. Taking the optimal parameters for $\mathcal { P } _ { 5 } , \mathcal { P } _ { 2 }$ is solved with more than double the loss compared to using its optimal parameters. Optimizing for all three environments, as shown in the last column, leads to a trade-off. This inter-class generalization was also reported in [15]. However, this trade-off is highly biased towards $\mathcal { P } _ { 3 }$ . The reason for this is that $\mathcal { P } _ { 3 }$ is more prone to returning higher planning times and costs. In consequence, the costs and optimized parameters are close to the results for optimizing on $\mathcal { P } _ { 3 }$ . At the same time, it leads to considerably higher costs for $\mathcal { P } _ { 2 }$ The same can be observed for the OMPL baseline settings. In the latter case, the parameters work very well on $\mathcal { P } _ { 3 }$ but deliver poor results on $\mathcal { P } _ { 2 }$ . The combined loss, however is also low.

Table 1: results for experiment 1

<table><tr><td></td><td>s</td><td> $b_{goal}$ </td><td> $L_2$ (mean)</td><td> $L_2$  $(Q_{0.7})$ </td><td> $L_3$ (mean)</td><td> $L_3$  $(Q_{0.7})$ </td><td> $L_5$ (mean)</td><td> $L_5$  $(Q_{0.7})$ </td><td> $L_{2,3,5}$ (mean)</td></tr><tr><td> $\mathcal{P}_2$ </td><td>0.68</td><td>0.47</td><td>89.73</td><td>99.91</td><td>371.45</td><td>428.68</td><td>17.52</td><td>18.90</td><td>159.57</td></tr><tr><td> $\mathcal{P}_3$ </td><td>2.01</td><td>0.18</td><td>129.25</td><td>138.72</td><td>90.76</td><td>95.82</td><td>12.79</td><td>13.19</td><td>77.60</td></tr><tr><td> $\mathcal{P}_5$ </td><td>2.26</td><td>0.59</td><td>227.66</td><td>301.23</td><td>109.20</td><td>111.36</td><td>11.68</td><td>12.31</td><td>116.16</td></tr><tr><td> $\mathcal{P}_{2,3,5}$ </td><td>1.87</td><td>0.08</td><td>146.93</td><td>135.78</td><td>93.43</td><td>99.88</td><td>12.28</td><td>12.73</td><td>84.21</td></tr><tr><td>OMPL</td><td>2.74</td><td>0.05</td><td>177.01</td><td>254.75</td><td>79.44</td><td>83.34</td><td>12.65</td><td>12.64</td><td>89.70</td></tr></table>

It can be seen that inter-class optimization of hyperparameters can be challenging due to an optimization bias towards harder problems. When extending the optimization set to even more environments, it is expected that this issue increases. It is thus necessary to identify the modes of the parameter distribution instead of relying on a single setting for all problems.

## 5.2 Cluster Analysis

In the next step, we provide insights in the distribution of optimal parameters for a large set of planning problems. The goal is to define regions of optimal parameters and connect them to the characteristics of the planning problem. For this, we use the three environments from 5.1 as a test set. The remaining 17 environments and their 196 planning problems define the data basis for our analysis. We run BOHB with 100 trials for each of the problems and record the best step size and goal bias. For a more stable estimate, we solve each problem five times and use the loss function from (2). In a subsequent step, we run a cluster analysis on the resulting 196 data points. For this, we use the scikitlearn [20] implementation of the DBSCAN algorithm [17]. Using the metric defined in $( 3 ) ,$ , we set the algorithm’s parameters $\mathbf { t o } \ \varepsilon = 0 . 1 5$ and min samples = 3. These settings were chosen with the goal of not obtaining too many outliers or only a single cluster. The resulting clusters can be seen in Fig. 3. The final number of outliers is 25 and the number of samples per cluster is given in Table 2. In addition, we provide a list of planning problems per cluster in the attachment.

It can be seen that the obtained parameters are relatively widely spread across most of the parameter range. This stems from the fact that the data is based on a stochastic motion planning procedure. We also use a limited set of trials during optimization. It is thus necessary to consider the resulting data points as noisy and use appropriate clustering algorithms such as DBSCAN. Furthermore, a distribution of the individual planning problems per cluster and environment is given in Fig. 4. It can be seen that settings from $c _ { 1 }$ are most dominant in all environments. This results from the fact that most environments also contain planning problems which are less complex. In $\mathcal { P } _ { 1 7 }$ for instance, a significant amount of problems involves moving the manipulator over the small box and away from the narrow passage (see Fig. 2g). Considering the individual problems, however, one can see some similarities. A limited set of examples is provided in Fig. 5 and a complete list can be found with the benchmark files. The cluster c<sub>1</sub> contains most data points and its center thus represents a good general setting for medium complexity. This means it is well-suited for situations where the robot does not have to reach far inside a narrow passage. In contrast, cluster $c _ { 2 }$ is characterized by a larger step size and suited for less cluttered environments. When operating in mostly free spaces and not reaching into narrow passages, $c _ { 4 }$ is recommended. In contrast, the problems in cluster $c _ { 5 }$ are characterized by narrow passages and hard-to-reach goal configurations. Comparing $\mathrm { F i g }$ . 5d and Fig. 5e, one can see that reaching a bit further inside the shelf already requires adapting the parameters from $c _ { 4 }$ to $c _ { 5 }$ . The remaining setting in $c _ { 3 }$ and $c _ { 6 }$ can be seen as an extension of $c _ { 1 }$ since they are close and not supported by many data points. We thus recommend considering them for problems of medium complexity as well.

![](Gaebert2023Paramater_figs/70520478f36ab52440098b7005a098f7e61e7b121d6c8510388511cdaf75d061.jpg)  
Figure 3: Results of the clustering analysis defining a set of six parameter settings. Samples labeled as outliers are displayed as black dots.

![](Gaebert2023Paramater_figs/6e29417f578f43c09c8f1d464d6eb5c2b02ea732c82114725e73e89b841fa815.jpg)  
Figure 4: Number of clustered problems per class. It can be seen that the optimized parameters vary even within the same problem class. However, settings from $c _ { 1 }$ are applicable for most of the problems.

![](Gaebert2023Paramater_figs/951d9ec5864e1801839e62547dac4600c07710e52d02127f61fb6d2da4570257.jpg)

![](Gaebert2023Paramater_figs/dd9c26040693c92bdc57024f62ffa6b1af98f617c8e82e99ca79955e0a439b6c.jpg)  
(a) Example for $c _ { 1 }$

![](Gaebert2023Paramater_figs/8fc83600437cde43e05d6ec57aa02e30e1d3e3a1a692822d7e5718e143829129.jpg)  
(b) Example for $c _ { 2 }$

![](Gaebert2023Paramater_figs/e26954b01c7b825b3255c871894661351101e39a890ce679dd118d65c0a49679.jpg)  
(d) Example for $c _ { 4 }$

(c) Example for c<sub>3</sub>  
![](Gaebert2023Paramater_figs/6ed83d412f11444f0e8065295c1860b8a8e238249f5a32e38208c0b16775fbb4.jpg)  
(e) Example for $c _ { 5 }$

![](Gaebert2023Paramater_figs/591beb84f8e3cb7732e7154ec5429705d8b50a1c2966ab6dba6dc47a6d874e73.jpg)  
(f) Example for $c _ { 6 }$  
Figure 5: Example planning problems per cluster. Start configurations are shown in orange and goals in blue.

Finally, we use the test problems $\mathcal { P } _ { 2 } , \mathcal { P } _ { 3 }$ and ${ \mathcal { P } } _ { 5 }$ to validate the feasibility of the obtained parameters. The values for the cluster centers as well as the number of samples per cluster are shown in Table 2. In the second part of the table the results of using these parameters are shown. For this, we used the same test setup as in 5.1. It can be seen that the challenging set $\mathcal { P } _ { 2 }$ can be solved most efficiently with the parameter settings from $c _ { 5 }$ whereas $c _ { 2 }$ performs poorly. In contrast, $c _ { 2 }$ is well-suited for ${ \mathcal { P } } _ { 5 }$ since the little amount of obstacles allow for larger step sizes and goal biases. In environments with trivial as well as harder problems, such as $\mathcal { P } _ { 3 }$ , a reduced goal bias and increased step size such as in $c _ { 4 }$ works best on average. On the other hand, using the center of $c _ { 3 }$ is not recommended because small values for $b _ { g o a l }$ and s lead to longer planning times when solving the easier problems at one side of the arch.

## 6 Discussion

In this work, we have presented a novel benchmark for manipulator motion planning. The dataset contains a set of 20 planning environments and 214 planning problems in total. The main contribution of this work, however, is optimizing the parameters of the RRT\*-Connect algorithm. First, we investigated weather a planner optimized on one environment can be employed in other setups. In contrast to previous works, we chose environments with inherently different characteristics and complexity. Such settings are closer to dynamic environments such as shared workspaces. We show that this is not always possible. Moreover, the planner’s performance can even drop when optimized on a different setup. In some cases even below the baseline. When jointly optimizing the planner on all three environments, we achieved slightly better results than with the baseline setting. However, they do not outperform the individually optimized planners. Moreover, the optimization was tailored towards $\mathcal { P } _ { 3 }$ which is most prone to deliver high loss values. The optimization procedure thus leads to a reasonable performance in general but gives up on the advantages in some setups. Depending on the chosen optimization set, such a general parameter setting could even lead to very poor performance in certain cases which should be avoided in HRI applications.

Table 2: Cluster center and their performance on the test set

<table><tr><td>cluster</td><td> $s^*$ </td><td> $b^{*}_{goal}$ </td><td> $|c_i|$ </td><td> $L_2$  $(Q_{0.7})$ </td><td> $L_3$  $(Q_{0.7})$ </td><td> $L_5$  $(Q_{0.7})$ </td></tr><tr><td> $c_1$ </td><td>1.23</td><td>0.59</td><td>142</td><td>263.25</td><td>129.37</td><td>16.90</td></tr><tr><td> $c_2$ </td><td>1.74</td><td>0.66</td><td>14</td><td>469.36</td><td>109.47</td><td>11.88</td></tr><tr><td> $c_3$ </td><td>0.89</td><td>0.30</td><td>3</td><td>131.47</td><td>192.46</td><td>19.31</td></tr><tr><td> $c_4$ </td><td>2.02</td><td>0.55</td><td>5</td><td>152.27</td><td>93.56</td><td>12.00</td></tr><tr><td> $c_5$ </td><td>1.33</td><td>0.16</td><td>4</td><td>82.16</td><td>113.34</td><td>14.40</td></tr><tr><td> $c_6$ </td><td>1.26</td><td>0.36</td><td>3</td><td>116.20</td><td>120.05</td><td>17.89</td></tr></table>

For this reason, we analyzed the distribution of optimal parameter settings for 196 problems across 17 environments. The resulting data, however, does not show a very clear cluster structure due to the stochastic planning process and the limited number of optimization trials. Due to these noisy data points, we used the established DBSCAN algorithm together with an adapted distance metric to identify six clusters. This number, however, is influenced by the parameter settings of the algorithm and can vary. When choosing a setting for a concrete use-case, we recommend $c _ { 1 } , c _ { 3 }$ and $c _ { 6 }$ for environments with medium clutter. The robot should also not have to reach far inside narrow passages. For less-densely cluttered workspaces, $c _ { 2 }$ can be considered. The settings for $c _ { 5 }$ are recommended for complex problems with narrow passages and $c _ { 4 }$ for trivial problems. We utilized the hold-out test set from our first analysis to evaluate the suggested parameters. The results are equally good to optimizing the planner directly on the test environments. The presented set of parameters can thus help practitioners setting up their planner given the category of planning problems.

However, our approach is limited in some ways. First, we use a highly parallelized custom version of the RRT\*- Connect algorithm. Hence, our method explores the search space much more rapidly than single-threaded planners. It is thus not clear yet how well the suggested settings transfer to other implementations or even algorithms. In addition, it is possible to cluster the obtained data differently. This would lead to a different number of outliers and clusters. Moreover, this work only provides informed guidelines for setting parameters optimally. It is not possible yet to directly extract them from the concrete planning problem. For future work, we are interested in extracting relevant characteristics from the environment by learning a latent representation and assigning parameters automatically.

## ACKNOWLEDGMENT

Funded by the Deutsche Forschungsgemeinschaft (DFG, German Research Foundation) – Project-ID 416228727 – SFB 1410

## References

[1] S. Karaman and E. Frazzoli, “Sampling-based algorithms for optimal motion planning,” The International Journal of Robotics Research, vol. 30, no. 7, pp. 846–894, Jun 2011.

[2] S. Klemm, J. Oberlander, A. Hermann, A. Roennau, T. Schamm, J. M. Zollner, and R. Dillmann, “RRT\*-¨ Connect: Faster, asymptotically optimal motion planning,” in 2015 IEEE International Conference on Robotics and Biomimetics (ROBIO). IEEE, 2015, pp. 1670–1677.

[3] D. Hsu, T. Jiang, J. Reif, and Z. Sun, “The Bridge Test for Sampling Narrow Passages with Probabilistic Roadmap Planners,” Proceedings - IEEE International Conference on Robotics and Automation, vol. 3, pp. 4420–4426, 2003.

[4] N. M. Amato, O. B. Bayazit, L. K. Dale, C. Jones, and D. Vallejo, “OBPRM: An Obstacle-Based PRM for 3D Workspaces,” in Proceedings of the Third Workshop on the Algorithmic Foundations of Robotics, ser. WAFR ’98. USA: A. K. Peters, Ltd., 1998, pp. 155–168.

[5] S. Rodriguez, S. Thomas, R. Pearce, and N. M. Amato, “RESAMPL: A Region-Sensitive Adaptive Motion Planner,” in Algorithmic Foundation of Robotics VII. Berlin, Heidelberg: Springer, 2008, pp. 285–300.

[6] B. Ichter, J. Harrison, and M. Pavone, “Learning Sampling Distributions for Robot Motion Planning,” in 2018 IEEE International Conference on Robotics and Automation (ICRA), 2018, pp. 7087–7094.

[7] A. H. Qureshi, A. Simeonov, M. J. Bency, and M. C. Yip, “Motion Planning Networks,” in 2019 International Conference on Robotics and Automation (ICRA), 2019, pp. 2118–2124.

[8] R. Cheng, K. Shankar, and J. W. Burdick, “Learning an Optimal Sampling Distribution for Efficient Motion Planning,” in IEEE International Conference on Intelligent Robots and Systems. IEEE, Oct 2020, pp. 7485– 7492.

[9] R. Burger, M. Bharatheesha, M. van Eert, and R. Babuska, “Automated tuning and configuration of path planningˇ algorithms,” in 2017 IEEE International Conference on Robotics and Automation (ICRA), 2017, pp. 4371–4376.

[10] I. A. S¸ ucan, M. Moll, and L. E. Kavraki, “The Open Motion Planning Library,” IEEE Robotics & Automation Magazine, vol. 19, no. 4, pp. 72–82, Dec 2012, https://ompl.kavrakilab.org.

[11] I. A. S¸ ucan and L. E. Kavraki, “Kinodynamic Motion Planning by Interior-Exterior Cell Exploration,” in Algorithmic Foundation of Robotics VIII. Springer, 2009, pp. 449–464.

[12] J. Kuffner and S. LaValle, “RRT-connect: An efficient approach to single-query path planning,” in Proceedings 2000 ICRA. Millennium Conference. IEEE International Conference on Robotics and Automation. Symposia Proceedings (Cat. No.00CH37065), vol. 2, 2000, pp. 995–1001.

[13] S. Falkner, A. Klein, and F. Hutter, “BOHB: Robust and Efficient Hyperparameter Optimization at Scale,” in Proceedings of the 35th International Conference on Machine Learning, ser. Proceedings of Machine Learning Research, J. Dy and A. Krause, Eds., vol. 80. PMLR, 10–15 Jul 2018, pp. 1437–1446. [Online]. Available: https://proceedings.mlr.press/v80/falkner18a.html

[14] L. Li, K. Jamieson, G. DeSalvo, A. Rostamizadeh, and A. Talwalkar, “Hyperband: A Novel Bandit-Based Approach to Hyperparameter Optimization,” The Journal of Machine Learning Research, vol. 18, no. 1, pp. 6765– 6816, 2017.

[15] M. Moll, C. Chamzas, Z. Kingston, and L. E. Kavraki, “HyperPlan: A Framework for Motion Planning Algorithm Selection and Parameter Optimization,” in 2021 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), 2021, pp. 2511–2518.

[16] K. Jamieson and A. Talwalkar, “Non-stochastic Best Arm Identification and Hyperparameter Optimization,” in Proceedings of the 19th International Conference on Artificial Intelligence and Statistics, ser. Proceedings of Machine Learning Research, A. Gretton and C. C. Robert, Eds., vol. 51. Cadiz, Spain: PMLR, 09–11 May 2016, pp. 240–248. [Online]. Available: https://proceedings.mlr.press/v51/jamieson16.html

[17] M. Ester, H.-P. Kriegel, J. Sander, X. Xu et al., “A Density-Based Algorithm for Discovering Clusters in Large Spatial Databases with Noise,” in Proceedings of the 2nd International Conference on Knowledge Discovery and Data Mining, vol. 96, no. 34. AAAI, 1996, pp. 226–231.

[18] M. Moll, I. A. Sucan, and L. E. Kavraki, “Benchmarking Motion Planning Algorithms: An Extensible Infrastructure for Analysis and Visualization,” IEEE Robotics & Automation Magazine, vol. 22, no. 3, pp. 96–102, 2015.

[19] R. Liaw, E. Liang, R. Nishihara, P. Moritz, J. E. Gonzalez, and I. Stoica, “Tune: A research platform for distributed model selection and training,” arXiv preprint arXiv:1807.05118, 2018.

[20] F. Pedregosa, G. Varoquaux, A. Gramfort, V. Michel, B. Thirion, O. Grisel, M. Blondel, P. Prettenhofer, R. Weiss, V. Dubourg, J. Vanderplas, A. Passos, D. Cournapeau, M. Brucher, M. Perrot, and E. Duchesnay, “Scikit-learn: Machine Learning in Python,” Journal of Machine Learning Research, vol. 12, pp. 2825–2830, 2011.