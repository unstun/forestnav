---
citation_key: Gaebert2023Paramater
arxiv_id: 2302.14422
arxiv_url: "https://arxiv.org/abs/2302.14422"
title: "Paramater Optimization for Manipulator Motion Planning using a Novel Benchmark Set"
authors_short: "Carl Gaebert et al."
year: 2023
direction_tag: O_dense_forest_narrow_passage
source: pymupdf4llm
converted_at: 2026-06-23T19:38:15Z
origin: ai+web
reviewed: false
---

# PARAMETER OPTIMIZATION FOR MANIPULATOR MOTION PLANNING USING A NOVEL BENCHMARK SET 

**Carl Gaebert, Sascha Kaden, Benjamin Fischer and Ulrike Thomas** _[∗]_ 

## **ABSTRACT** 

Sampling-based motion planning algorithms have been continuously developed for more than two decades. Apart from mobile robots, they are also widely used in manipulator motion planning. Hence, these methods play a key role in collaborative and shared workspaces. Despite numerous improvements, their performance can highly vary depending on the chosen parameter setting. The optimal parameters depend on numerous factors such as the start state, the goal state and the complexity of the environment. Practitioners usually choose these values using their experience and tedious trial and error experiments. To address this problem, recent works combine hyperparameter optimization methods with motion planning. They show that tuning the planner’s parameters can lead to shorter planning times and lower costs. It is not clear, however, how well such approaches generalize to a diverse set of planning problems that include narrow passages as well as barely cluttered environments. In this work, we analyze optimized planner settings for a large set of diverse planning problems. We then provide insights into the connection between the characteristics of the planning problem and the optimal parameters. As a result, we provide a list of recommended parameters for various use-cases. Our experiments are based on a novel motion planning benchmark for manipulators which we provide at https://mytuc.org/rybj. 

## **1 Introduction** 

For more than two decades, robot motion planning has been an active field of research. One prominent group of approaches are sampling-based motion planning (SBMP) algorithms. They are well-suited to address the problem of high-dimensionality which is a main challenge in many robotics applications. Instead of searching the complete configuration space, these algorithms use random sampling to find a feasible solution. Approaches such as RRT* [1] and RRT*-Connect [2] sample the robot’s configuration space to grow a collision-free tree connecting start and goal. While doing so, they also optimize the existing tree to minimize a given cost function. In contrast to static scenarios, human-robot interaction (HRI) calls for optimized solutions within a very short planning time. To this end, many approaches have been presented which increase the performance of sampling-based planners. They address the problem of narrow passages [3, 4], use adaptive sampling strategies [5] or even learning-based methods [6, 7, 8]. Despite all these improvements, the performance of the planner is still heavily influenced by its most basic parameter settings, namely the step size _s_ and the goal bias _bgoal_ . Moreover, the settings recorded in the original works are often related to mobile robot applications. In industry, practitioners are thus often faced with fine-tuning basic parameter settings by hand for manipulators. A recent line of research therefore aims at automatizing this process through optimization. In recent years, several approaches have addressed the problem of automatic hyperparameter tuning in SBMP for manipulators. In [9], the authors utilize a random forest model to tune parameters of several algorithms provided in the Open Motion Planning Library (OMPL) [10]. The authors achieved reduced planning times and costs in a few pre-defined pick-and-place scenarios. Cano et al. investigated several optimization methods while considering the BKPIECE [11] and RRT-Connect [12] algorithms implemented in OMPL. The authors show that planning time can be reduced by a factor of 4.5. In addition, randomized planning problems are used to show that the tuned parameters generalize well across various setups from the same problem distribution. Moll et al. use Bayesian Optimization and Hyperband (BOHB) [13] to find optimal settings in an extensive search space that includes several planning algorithms and their parameters. Hence, the authors manage to find the best performing approach together with its tuned parameters. For evaluating their approach, the authors use several classes of planning problems such as reaching 

> _∗_ All authors are with the Robotics and Human-Machine Interaction Lab, Chemnitz University of Technology, Germany _{_ `carl.gaebert, sascha.kaden, ulrike.thomas` _}_ `@etit.tu-chemnitz.de` 

©2023 IEEE. Personal use of this material is permitted. Permission from IEEE must be obtained for all other uses, in any current or future media, including reprinting/republishing this material for advertising or promotional purposes, creating new collective works, for resale or redistribution to servers or lists, or reuse of any copyrighted component of this work in other works. 

Parameter Optimization for Manipulator Motion Planning using a Novel Benchmark Set 


![](1_survey/papers/md/Gaebert2023Paramater_figs/Gaebert2023Paramater.pdf-0002-01.png)



![](1_survey/papers/md/Gaebert2023Paramater_figs/Gaebert2023Paramater.pdf-0002-02.png)



![](1_survey/papers/md/Gaebert2023Paramater_figs/Gaebert2023Paramater.pdf-0002-03.png)


**----- Start of picture text -----**<br>
(a) Trivial environment (b) Complex environment<br>**----- End of picture text -----**<br>


Figure 1: A seven DoF manipulator operating in two different environments. (a): Almost no obstacles are present which allows for a higher step size and goal bias during sampling. (b): Complex environment with many narrow passages. A smaller goal bias and step size is thus recommended. 

into a shelf or into a box. The considered optimization criteria are planning and execution speed. In the same work, the authors also demonstrate that optimizing on a small set of problem classes can lead to good performance in all of them. However, it was not shown to which number of classes and to which variety in complexity this holds. For example, a planner optimized on a trivial problem such as in Fig. 1a may still work well when introducing a few more obstacles to the scene. However, it is likely to fail in very complex environments like the one shown in Fig. 1b. Furthermore, none of the mentioned works utilize a parallelized planner. It is thus not clear to which extent parameter optimization can improve the results in such a setup. To this end, our work provides the following contributions: 

- We provide a benchmark dataset for manipulator motion planning consisting of 20 environments and over 200 planning problems of different complexity. 

- We utilize this dataset to investigate how well optimized parameters generalize across a very diverse set of planning problems. 

- We analyze the distribution of optimized parameters and connect them to the characteristics of the planning problems. In consequence, we can provide a list of recommendations to practitioners for setting up their planner in a specific scenario. 

In the remainder of the paper, we first provide a brief summary of the optimization algorithm. Since we use results from stochastic planners, we also review a method for extracting clusters from noisy datasets. Next, we introduce the optimization function used throughout this work. In a subsequent step, we present details of the motion planning benchmark for manipulators in 4. Next, we point out the challenges of finding suitable parameters for diverse planning problems. Finally, we experimentally derive a list of recommendations for optimal planning parameters depending on the problem. 

## **2 Background** 

## **2.1 Bayesian Optimization and Hyperband** 

In SBMP, costs and planning time heavily depend on the planner’s parameters. A very low goal bias, for example, can lead to a bad performance even in simple environments. Such sensitivity towards hyperparameter choices is also commonly observed in areas of Deep Learning. Therefore, automatic hyperparameter tuning is an active field of research beyond robotics. Formally, the performance of a motion planning algorithm can be defined as a function _f_ : _X →_ R of its parameters _x_ . The goal of the optimization procedure is to find the parameters _x[∗]_ for which _f_ is minimized. Typically, the function _f_ is expensive to validate. However, it can be approximated by sampling from the parameter space _X_ . A recent work by Falkner et al. [13] in this direction combines the strengths of Bayesian Optimization with a Hyperband scheduler [14]. In line with the work of Moll et al. [15], we utilize this approach to tune the parameters of our motion planning algorithm. In BOHB the Hyperband scheduler is used to identify the best out of _ntrials_ randomly initialized planner configurations. It does so by using Successive Halving [16] (as cited in 

2 

Parameter Optimization for Manipulator Motion Planning using a Novel Benchmark Set 

[13]) and assigning resources to the most promising trials. Instead of relying on random samples, BOHB uses kernel density estimators to generate new promising trials based on previous results. The resulting increase in efficiency is crucial for our experiments since they require solving hundreds of challenging motion planning problems. 

## **2.2 Clustering Large and Noisy Datasets** 

SBMP algorithms rely on stochastic processes and thus deliver non-deterministic solutions. This has to be taken into account while analyzing results from such sources. When clustering such datasets, one thus has to cope with outliers that do not necessarily belong to a cluster. One established algorithm for such use-cases is Density Based Spatial Clustering of Applications with Noise (DBSCAN) [17]. The advantage of using this algorithm over K-Means, for example, is that clusters do not have to be of convex shape. Instead, they are viewed as regions with high density which are separated by areas of low density. The method is based on the concept of core samples. A sample is considered a core sample when a number of _min_ ~~_s_~~ _amples_ are within a distance of _ε_ to it. Besides core samples, a cluster can also contain samples which are within _ε_ to one of the core samples. Therefore, the algorithms does not require a number of clusters to look for but a distance metric and the number of core samples. It thus allows for marking too distant samples as outliers. 

## **3 Methodology** 

In HRI one is typically interested in optimizing for two objectives simultaneously: planning time and costs. The latter can vary depending on the application and may involve state as well as distant costs. In contrast to works like [15], we rely on the optimizing planner RRT*-Connect [2] only. For this, we use a custom and highly-parallelized implementation. This allows us to combine these two objectives into a single objective function which would not be possible using non-optimizing planners such as RRT. 

For a single planning problem _p_ from a start configuration _θstart_ to a goal configuration _θgoal_ , we define the combined costs _c_ ( _p_ ) as follows: 


![](1_survey/papers/md/Gaebert2023Paramater_figs/Gaebert2023Paramater.pdf-0003-07.png)


The cost consists of the planning time _t_ in seconds and the path length in configuration space _cC_ . The latter is given in radian and normalized using the shortest path length possible. In addition, we weight the influence of the planning time throughout this paper with _wt_ = 3. 

Since we are interested in an approximation of our planner’s performance in various workspaces, we consider a whole set _P_ of _n_ problems. The final objective function _f_ is then defined as 


![](1_survey/papers/md/Gaebert2023Paramater_figs/Gaebert2023Paramater.pdf-0003-10.png)


This can be interpreted as follows: We solve all planning problems in _P_ and sum up the costs calculated using (1). The process is repeated _m_ times which results in a distribution of estimates costs for this trial. In line with [15], we then take the 0.7-quanttile _Q_ 0 _._ 7 of this distribution as our estimate. This is done to account for the highly stochastic nature and the high variance of solutions obtained by SBMP algorithms. Due to the complexity of the environments, certain parameter configurations might perform very poorly. It is thus necessary to restrict the maximum planning time to _tmax_ . In cases where no solution was found within _tmax_ , we use a cost value of _c_ ( _p_ ) = 3 _∗ tmax_ + 100. Moreover, the possible ranges for the goal bias _bgoal_ and step size _s_ are significantly different. Using the Euclidean distance for clustering the optimal settings would thus favor clusters with a wide range of goal bias parameters. For this reason, we introduce a distance metric that scales the distance in the goal bias dimension using the ratio of the parameter ranges. The distance between parameter settings _a_ and _b_ are then calculated using the step sizes _sa_ and _sb_ as well as the goal bias settings _bgoal,a_ and _bgoal,b_ as shown below. 


![](1_survey/papers/md/Gaebert2023Paramater_figs/Gaebert2023Paramater.pdf-0003-12.png)


## **4 Motion Planning Benchmark for Manipulators** 

Related works utilize a wide range of planning problems and applications for evaluation. However, they are often not made publically available which hinders comparing results to previous works. Moreover, they are usually based on 

3 

Parameter Optimization for Manipulator Motion Planning using a Novel Benchmark Set 

randomized environments or tailored towards a specific problem class. Our contribution is thus to provide a manipulator motion planning benchmark (see Fig. 2). It consists of 20 environments with several robot configurations per environment. Each environment _e_ can be used to construct a set of possible planning problems _Pe_ . For now, only configurations for the Kuka iiwa manipulator are provided. However, we provide Blender and Coppelia files for each environment which allows for including other manipulators. Furthermore, the benchmark is independent of any planning software. Hence, it can also be used with well-established tools such as the OMPL benchmark pipeline [18]. In total, the benchmark contains 214 possible planning problems that can be generated by combining the provided configurations. As it can be seen in Fig. 2, the provided planning problems contain several narrow passages and thus yield a challenge for most state-of-the-art algorithms. The whole dataset can be downloaded from https://mytuc.org/rybj. 


![](1_survey/papers/md/Gaebert2023Paramater_figs/Gaebert2023Paramater.pdf-0004-02.png)



![](1_survey/papers/md/Gaebert2023Paramater_figs/Gaebert2023Paramater.pdf-0004-03.png)



![](1_survey/papers/md/Gaebert2023Paramater_figs/Gaebert2023Paramater.pdf-0004-04.png)



![](1_survey/papers/md/Gaebert2023Paramater_figs/Gaebert2023Paramater.pdf-0004-05.png)



![](1_survey/papers/md/Gaebert2023Paramater_figs/Gaebert2023Paramater.pdf-0004-06.png)



![](1_survey/papers/md/Gaebert2023Paramater_figs/Gaebert2023Paramater.pdf-0004-07.png)


**----- Start of picture text -----**<br>
(a)  P 2 (b)  P 3 (c)  P 5 (d)  P 7 (e)  P 8<br>(f)  P 16 (g)  P 17 (h)  P 18 (i)  P 19 (j)  P 20<br>**----- End of picture text -----**<br>


Figure 2: Ten example environments included in the presented benchmark. Some of them contain narrow passages. Others do not include many obstacles and are thus easier to solve. 

## **5 Experiments** 

In the following, we conduct two experiments using the previously presented benchmark of planning problems. For all our experiments we use our own RRT*-Connect implementation. In contrast to most implementations in OMPL, the algorithm is highly parallelized. We restrict number of threads per trial to eight. Throughout our experiments, we ° ° optimize the parameters goal bias _bgoal ∈_ (0 _._ 05 _,_ 0 _._ 75) and step size _s ∈_ (15 _,_ 135 ). We use the BOHB implementation provided by Tune [19]. For each problem within a trial, the planning time is restricted to _tmax_ = 20 s. All experiments are executed on a workstation with two Intel Xeon E5-2670 v3 CPUs, each with 12 processor cores and 64 GB of Ram. 

In the following, we first demonstrate the challenge of finding an optimized planner configuration for multiple environments. In a second experiment, we extend the set of considered problems to obtain a distribution of optimal parameters. This allows for extracting a set of suggested parameters depending on the setup. 

## **5.1 Optimizing on a Single Environment** 

In the first experiment we investigate weather a planner tuned on one environment can generalize across environments with other characteristics. For this, we used the BOHB algorithm on the planning problem sets _P_ 2, _P_ 3 and _P_ 5 (see Fig. 2(a)-(c)). As it can be seen, the three environments differ in the number of obstacles and narrow passages. Moreover, some planning problems within an environment are more challenging than others. In _P_ 3, for example, finding a path to the other side of the arch is more challenging than finding one to a configuration on the same side. Hence, our first goal is to test the generalization capabilities of an optimized planner. For this, we run BOHB with 100 trials on all problems of an environment and test the results on all three. For obtaining a stable loss estimate per environment, we sum up the costs for all problems. The process was repeated five times for each environment _e_ and the 0.7-quantile was used as a loss _Le_ . We also optimize the parameters using the combined set _P_ 2 _,_ 3 _,_ 5. In addition, we include the settings suggested by OMPL for the Kuka iiwa manipulator as a baseline. The results can be seen in Table 1. The first column describes from which source the optimized parameters _s_ and _bgoal_ were taken. Their values can be seen in column three and four. The remaining columns show the mean loss and the 0.7-quantile for all environments. The last column shows the average loss over all environments _P_ 2, _P_ 3 and _P_ 5. 

Looking at the optimized parameters, it can be seen that the step size in _P_ 2 has the smallest value which most-likely results from the robot reaching inside the walls. Environment five, on the other hand, is characterized by a very high 

4 

Parameter Optimization for Manipulator Motion Planning using a Novel Benchmark Set 

Table 1: results for experiment 1 

||_s_|_bgoal_|_L_2<br>(mean)|_L_2<br>(_Q_0_._7)|_L_3<br>(mean)|_L_3<br>(_Q_0_._7)|_L_5<br>(mean)|_L_5<br>(_Q_0_._7)|_L_2_,_3_,_5<br>(mean)|
|---|---|---|---|---|---|---|---|---|---|
|_P_2|0.68|0.47|89.73|99.91|371.45|428.68|17.52|18.90|159.57|
|_P_3|2.01|0.18|129.25|138.72|90.76|95.82|12.79|13.19|77.60|
|_P_5|2.26|0.59|227.66|301.23|109.20|111.36|11.68|12.31|116.16|
|_P_2_,_3_,_5|1.87|0.08|146.93|135.78|93.43|99.88|12.28|12.73|84.21|
|OMPL|2.74|0.05|177.01|254.75|79.44|83.34|12.65|12.64|89.70|



step size and goal bias because not many obstacles are present within the scene. In consequence, the loss values for the hold-out environments are much higher. Therefore, the optimized parameters are not applicable across all environments. Taking the optimal parameters for _P_ 5, _P_ 2 is solved with more than double the loss compared to using its optimal parameters. Optimizing for all three environments, as shown in the last column, leads to a trade-off. This inter-class generalization was also reported in [15]. However, this trade-off is highly biased towards _P_ 3. The reason for this is that _P_ 3 is more prone to returning higher planning times and costs. In consequence, the costs and optimized parameters are close to the results for optimizing on _P_ 3. At the same time, it leads to considerably higher costs for _P_ 2. The same can be observed for the OMPL baseline settings. In the latter case, the parameters work very well on _P_ 3 but deliver poor results on _P_ 2. The combined loss, however is also low. 

It can be seen that inter-class optimization of hyperparameters can be challenging due to an optimization bias towards harder problems. When extending the optimization set to even more environments, it is expected that this issue increases. It is thus necessary to identify the modes of the parameter distribution instead of relying on a single setting for all problems. 

## **5.2 Cluster Analysis** 

In the next step, we provide insights in the distribution of optimal parameters for a large set of planning problems. The goal is to define regions of optimal parameters and connect them to the characteristics of the planning problem. For this, we use the three environments from 5.1 as a test set. The remaining 17 environments and their 196 planning problems define the data basis for our analysis. We run BOHB with 100 trials for each of the problems and record the best step size and goal bias. For a more stable estimate, we solve each problem five times and use the loss function from (2). In a subsequent step, we run a cluster analysis on the resulting 196 data points. For this, we use the scikitlearn [20] implementation of the DBSCAN algorithm [17]. Using the metric defined in (3), we set the algorithm’s parameters to _ε_ = 0 _._ 15 and _min_ ~~_s_~~ _amples_ = 3. These settings were chosen with the goal of not obtaining too many outliers or only a single cluster. The resulting clusters can be seen in Fig. 3. The final number of outliers is 25 and the number of samples per cluster is given in Table 2. In addition, we provide a list of planning problems per cluster in the attachment. 

It can be seen that the obtained parameters are relatively widely spread across most of the parameter range. This stems from the fact that the data is based on a stochastic motion planning procedure. We also use a limited set of trials during optimization. It is thus necessary to consider the resulting data points as noisy and use appropriate clustering algorithms such as DBSCAN. Furthermore, a distribution of the individual planning problems per cluster and environment is given in Fig. 4. It can be seen that settings from _c_ 1 are most dominant in all environments. This results from the fact that most environments also contain planning problems which are less complex. In _P_ 17, for instance, a significant amount of problems involves moving the manipulator over the small box and away from the narrow passage (see Fig. 2g). Considering the individual problems, however, one can see some similarities. A limited set of examples is provided in Fig. 5 and a complete list can be found with the benchmark files. The cluster _c_ 1 contains most data points and its center thus represents a good general setting for medium complexity. This means it is well-suited for situations where the robot does not have to reach far inside a narrow passage. In contrast, cluster _c_ 2 is characterized by a larger step size and suited for less cluttered environments. When operating in mostly free spaces and not reaching into narrow passages, _c_ 4 is recommended. In contrast, the problems in cluster _c_ 5 are characterized by narrow passages and hard-to-reach goal configurations. Comparing Fig. 5d and Fig. 5e, one can see that reaching a bit further inside the shelf already requires adapting the parameters from _c_ 4 to _c_ 5. The remaining setting in _c_ 3 and _c_ 6 can be seen as an extension of _c_ 1 since they are close and not supported by many data points. We thus recommend considering them for problems of medium complexity as well. 

5 

Parameter Optimization for Manipulator Motion Planning using a Novel Benchmark Set 


![](1_survey/papers/md/Gaebert2023Paramater_figs/Gaebert2023Paramater.pdf-0006-01.png)


**----- Start of picture text -----**<br>
cout c2 c4 c6<br>c1 c3 c5<br>0.6<br>0.4<br>0.2<br>0.8 1.0 1.2 1.4 1.6 1.8 2.0<br>s<br>goal<br>b<br>**----- End of picture text -----**<br>


Figure 3: Results of the clustering analysis defining a set of six parameter settings. Samples labeled as outliers are displayed as black dots. 


![](1_survey/papers/md/Gaebert2023Paramater_figs/Gaebert2023Paramater.pdf-0006-03.png)


**----- Start of picture text -----**<br>
cout c2 c4 c6<br>c1 c3 c5<br>40<br>30<br>20<br>10<br>0<br>i<br>number of problems<br>1 4 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20<br>**----- End of picture text -----**<br>


Figure 4: Number of clustered problems per class. It can be seen that the optimized parameters vary even within the same problem class. However, settings from _c_ 1 are applicable for most of the problems. 

6 

Parameter Optimization for Manipulator Motion Planning using a Novel Benchmark Set 


![](1_survey/papers/md/Gaebert2023Paramater_figs/Gaebert2023Paramater.pdf-0007-01.png)



![](1_survey/papers/md/Gaebert2023Paramater_figs/Gaebert2023Paramater.pdf-0007-02.png)



![](1_survey/papers/md/Gaebert2023Paramater_figs/Gaebert2023Paramater.pdf-0007-03.png)


**----- Start of picture text -----**<br>
(a) Example for  c 1 (b) Example for  c 2<br>**----- End of picture text -----**<br>



![](1_survey/papers/md/Gaebert2023Paramater_figs/Gaebert2023Paramater.pdf-0007-04.png)



![](1_survey/papers/md/Gaebert2023Paramater_figs/Gaebert2023Paramater.pdf-0007-05.png)



![](1_survey/papers/md/Gaebert2023Paramater_figs/Gaebert2023Paramater.pdf-0007-06.png)


**----- Start of picture text -----**<br>
(c) Example for  c 3 (d) Example for  c 4<br>**----- End of picture text -----**<br>



![](1_survey/papers/md/Gaebert2023Paramater_figs/Gaebert2023Paramater.pdf-0007-07.png)



![](1_survey/papers/md/Gaebert2023Paramater_figs/Gaebert2023Paramater.pdf-0007-08.png)



![](1_survey/papers/md/Gaebert2023Paramater_figs/Gaebert2023Paramater.pdf-0007-09.png)


**----- Start of picture text -----**<br>
(e) Example for  c 5 (f) Example for  c 6<br>**----- End of picture text -----**<br>


Figure 5: Example planning problems per cluster. Start configurations are shown in orange and goals in blue. 

Finally, we use the test problems _P_ 2 _, P_ 3 and _P_ 5 to validate the feasibility of the obtained parameters. The values for the cluster centers as well as the number of samples per cluster are shown in Table 2. In the second part of the table the results of using these parameters are shown. For this, we used the same test setup as in 5.1. It can be seen that the challenging set _P_ 2 can be solved most efficiently with the parameter settings from _c_ 5 whereas _c_ 2 performs poorly. In contrast, _c_ 2 is well-suited for _P_ 5 since the little amount of obstacles allow for larger step sizes and goal biases. In environments with trivial as well as harder problems, such as _P_ 3, a reduced goal bias and increased step size such as in _c_ 4 works best on average. On the other hand, using the center of _c_ 3 is not recommended because small values for _bgoal_ and _s_ lead to longer planning times when solving the easier problems at one side of the arch. 

## **6 Discussion** 

In this work, we have presented a novel benchmark for manipulator motion planning. The dataset contains a set of 20 planning environments and 214 planning problems in total. The main contribution of this work, however, is 

7 

Parameter Optimization for Manipulator Motion Planning using a Novel Benchmark Set 

Table 2: Cluster center and their performance on the test set 

|cluster|_s∗_|_b∗_<br>_goal_|_|ci|_|_L_2<br>(_Q_0_._7)|_L_3<br>(_Q_0_._7)|_L_5<br>(_Q_0_._7)|
|---|---|---|---|---|---|---|
|_c_1|1.23|0.59|142|263.25|129.37|16.90|
|_c_2|1.74|0.66|14|469.36|109.47|**11.88**|
|_c_3|0.89|0.30|3|131.47|192.46|19.31|
|_c_4|2.02|0.55|5|152.27|**93.56**|12.00|
|_c_5|1.33|0.16|4|**82.16**|113.34|14.40|
|_c_6|1.26|0.36|3|116.20|120.05|17.89|



optimizing the parameters of the RRT*-Connect algorithm. First, we investigated weather a planner optimized on one environment can be employed in other setups. In contrast to previous works, we chose environments with inherently different characteristics and complexity. Such settings are closer to dynamic environments such as shared workspaces. We show that this is not always possible. Moreover, the planner’s performance can even drop when optimized on a different setup. In some cases even below the baseline. When jointly optimizing the planner on all three environments, we achieved slightly better results than with the baseline setting. However, they do not outperform the individually optimized planners. Moreover, the optimization was tailored towards _P_ 3 which is most prone to deliver high loss values. The optimization procedure thus leads to a reasonable performance in general but gives up on the advantages in some setups. Depending on the chosen optimization set, such a general parameter setting could even lead to very poor performance in certain cases which should be avoided in HRI applications. 

For this reason, we analyzed the distribution of optimal parameter settings for 196 problems across 17 environments. The resulting data, however, does not show a very clear cluster structure due to the stochastic planning process and the limited number of optimization trials. Due to these noisy data points, we used the established DBSCAN algorithm together with an adapted distance metric to identify six clusters. This number, however, is influenced by the parameter settings of the algorithm and can vary. When choosing a setting for a concrete use-case, we recommend _c_ 1 _, c_ 3 and _c_ 6 for environments with medium clutter. The robot should also not have to reach far inside narrow passages. For less-densely cluttered workspaces, _c_ 2 can be considered. The settings for _c_ 5 are recommended for complex problems with narrow passages and _c_ 4 for trivial problems. We utilized the hold-out test set from our first analysis to evaluate the suggested parameters. The results are equally good to optimizing the planner directly on the test environments. The presented set of parameters can thus help practitioners setting up their planner given the category of planning problems. 

However, our approach is limited in some ways. First, we use a highly parallelized custom version of the RRT*Connect algorithm. Hence, our method explores the search space much more rapidly than single-threaded planners. It is thus not clear yet how well the suggested settings transfer to other implementations or even algorithms. In addition, it is possible to cluster the obtained data differently. This would lead to a different number of outliers and clusters. Moreover, this work only provides informed guidelines for setting parameters optimally. It is not possible yet to directly extract them from the concrete planning problem. For future work, we are interested in extracting relevant characteristics from the environment by learning a latent representation and assigning parameters automatically. 

## **ACKNOWLEDGMENT** 

Funded by the Deutsche Forschungsgemeinschaft (DFG, German Research Foundation) – Project-ID 416228727 – SFB 1410 

## **References** 

- [1] S. Karaman and E. Frazzoli, “Sampling-based algorithms for optimal motion planning,” _The International Journal of Robotics Research_ , vol. 30, no. 7, pp. 846–894, Jun 2011. 

8 

Parameter Optimization for Manipulator Motion Planning using a Novel Benchmark Set 

- [2] S. Klemm, J. Oberl¨ander, A. Hermann, A. Roennau, T. Schamm, J. M. Zollner, and R. Dillmann, “RRT*Connect: Faster, asymptotically optimal motion planning,” in _2015 IEEE International Conference on Robotics and Biomimetics (ROBIO)_ . IEEE, 2015, pp. 1670–1677. 

- [3] D. Hsu, T. Jiang, J. Reif, and Z. Sun, “The Bridge Test for Sampling Narrow Passages with Probabilistic Roadmap Planners,” _Proceedings - IEEE International Conference on Robotics and Automation_ , vol. 3, pp. 4420–4426, 2003. 

- [4] N. M. Amato, O. B. Bayazit, L. K. Dale, C. Jones, and D. Vallejo, “OBPRM: An Obstacle-Based PRM for 3D Workspaces,” in _Proceedings of the Third Workshop on the Algorithmic Foundations of Robotics_ , ser. WAFR ’98. USA: A. K. Peters, Ltd., 1998, pp. 155–168. 

- [5] S. Rodriguez, S. Thomas, R. Pearce, and N. M. Amato, “RESAMPL: A Region-Sensitive Adaptive Motion Planner,” in _Algorithmic Foundation of Robotics VII_ . Berlin, Heidelberg: Springer, 2008, pp. 285–300. 

- [6] B. Ichter, J. Harrison, and M. Pavone, “Learning Sampling Distributions for Robot Motion Planning,” in _2018 IEEE International Conference on Robotics and Automation (ICRA)_ , 2018, pp. 7087–7094. 

- [7] A. H. Qureshi, A. Simeonov, M. J. Bency, and M. C. Yip, “Motion Planning Networks,” in _2019 International Conference on Robotics and Automation (ICRA)_ , 2019, pp. 2118–2124. 

- [8] R. Cheng, K. Shankar, and J. W. Burdick, “Learning an Optimal Sampling Distribution for Efficient Motion Planning,” in _IEEE International Conference on Intelligent Robots and Systems_ . IEEE, Oct 2020, pp. 7485– 7492. 

- [9] R. Burger, M. Bharatheesha, M. van Eert, and R. Babuˇska, “Automated tuning and configuration of path planning algorithms,” in _2017 IEEE International Conference on Robotics and Automation (ICRA)_ , 2017, pp. 4371–4376. 

- [10] I. A. S¸ucan, M. Moll, and L. E. Kavraki, “The Open Motion Planning Library,” _IEEE Robotics & Automation Magazine_ , vol. 19, no. 4, pp. 72–82, Dec 2012, https://ompl.kavrakilab.org. 

- [11] I. A. S¸ucan and L. E. Kavraki, “Kinodynamic Motion Planning by Interior-Exterior Cell Exploration,” in _Algorithmic Foundation of Robotics VIII_ . Springer, 2009, pp. 449–464. 

- [12] J. Kuffner and S. LaValle, “RRT-connect: An efficient approach to single-query path planning,” in _Proceedings 2000 ICRA. Millennium Conference. IEEE International Conference on Robotics and Automation. Symposia Proceedings (Cat. No.00CH37065)_ , vol. 2, 2000, pp. 995–1001. 

- [13] S. Falkner, A. Klein, and F. Hutter, “BOHB: Robust and Efficient Hyperparameter Optimization at Scale,” in _Proceedings of the 35th International Conference on Machine Learning_ , ser. Proceedings of Machine Learning Research, J. Dy and A. Krause, Eds., vol. 80. PMLR, 10–15 Jul 2018, pp. 1437–1446. [Online]. Available: https://proceedings.mlr.press/v80/falkner18a.html 

- [14] L. Li, K. Jamieson, G. DeSalvo, A. Rostamizadeh, and A. Talwalkar, “Hyperband: A Novel Bandit-Based Approach to Hyperparameter Optimization,” _The Journal of Machine Learning Research_ , vol. 18, no. 1, pp. 6765– 6816, 2017. 

- [15] M. Moll, C. Chamzas, Z. Kingston, and L. E. Kavraki, “HyperPlan: A Framework for Motion Planning Algorithm Selection and Parameter Optimization,” in _2021 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_ , 2021, pp. 2511–2518. 

- [16] K. Jamieson and A. Talwalkar, “Non-stochastic Best Arm Identification and Hyperparameter Optimization,” in _Proceedings of the 19th International Conference on Artificial Intelligence and Statistics_ , ser. Proceedings of Machine Learning Research, A. Gretton and C. C. Robert, Eds., vol. 51. Cadiz, Spain: PMLR, 09–11 May 2016, pp. 240–248. [Online]. Available: https://proceedings.mlr.press/v51/jamieson16.html 

- [17] M. Ester, H.-P. Kriegel, J. Sander, X. Xu _et al._ , “A Density-Based Algorithm for Discovering Clusters in Large Spatial Databases with Noise,” in _Proceedings of the 2nd International Conference on Knowledge Discovery and Data Mining_ , vol. 96, no. 34. AAAI, 1996, pp. 226–231. 

- [18] M. Moll, I. A. Sucan, and L. E. Kavraki, “Benchmarking Motion Planning Algorithms: An Extensible Infrastructure for Analysis and Visualization,” _IEEE Robotics & Automation Magazine_ , vol. 22, no. 3, pp. 96–102, 2015. 

- [19] R. Liaw, E. Liang, R. Nishihara, P. Moritz, J. E. Gonzalez, and I. Stoica, “Tune: A research platform for distributed model selection and training,” _arXiv preprint arXiv:1807.05118_ , 2018. 

- [20] F. Pedregosa, G. Varoquaux, A. Gramfort, V. Michel, B. Thirion, O. Grisel, M. Blondel, P. Prettenhofer, R. Weiss, V. Dubourg, J. Vanderplas, A. Passos, D. Cournapeau, M. Brucher, M. Perrot, and E. Duchesnay, “Scikit-learn: Machine Learning in Python,” _Journal of Machine Learning Research_ , vol. 12, pp. 2825–2830, 2011. 

9 

