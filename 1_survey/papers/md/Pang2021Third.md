---
citation_key: Pang2021Third
arxiv_id: 2107.01834
arxiv_url: "https://arxiv.org/abs/2107.01834"
title: "Third Party Risk Modelling and Assessment for Safe UAV Path Planning in Metropolitan Environments"
authors_short: "Bizhao Pang et al."
year: 2021
direction_tag: F_hybrid_astar
source: pymupdf4llm
converted_at: 2026-06-24T16:36:12Z
origin: ai+web
reviewed: false
---

## **Third Party Risk Modelling and Assessment for Safe UAV Path Planning in Metropolitan Environments** 

## Bizhao Pang[a] , Xinting Hu[b] , Wei Dai[a, c] , Kin Huat Low[a,][*] 

> a _School of Mechanical and Aerospace Engineering, Nanyang Technological University, Singapore 639798, Singapore_ 

> b _School of Air Traffic Management, Civil Aviation University of China, Tianjin 300300, China_ 

> c _Air Traffic Management Research Institute, Nanyang Technological University, Singapore 639460, Singapore_ 

**Abstract** : Various applications of advanced air mobility (AAM) in urban environments facilitate our daily life and public services. As one of the key issues of realizing these applications autonomously, path planning problem has been studied with main objectives on minimizing travel distance, flight time and energy cost. However, AAM operations in metropolitan areas bring safety and society issues. Because most of AAM aircraft are unmanned aerial vehicles (UAVs) and they may fail to operate resulting in fatality risk, property damage risk and societal impacts (noise and privacy) to the public. To quantitatively assess these risks and mitigate them in planning phase, this paper proposes an integrated risk assessment model and develops a hybrid algorithm to solve the risk-based 3D path planning problem. The integrated risk assessment method considers probability and severity models of UAV impact ground people and vehicle. By introducing gravity model, the population density and traffic density are estimated in a finer scale, which enables more accurate risk assessment. The 3D risk-based path planning problem is first formulated as a special minimum cost flow problem. Then, a hybrid estimation of distribution algorithm (EDA) and risk-based A* (named as EDA-RA*) algorithm is proposed to solve the problem. To improve computational efficiency, k-means clustering method is incorporated into EDA-RA* to provide both global and local search heuristic information, which formed the EDA and fast risk-based A* algorithm we call EDA-FRA*. Case study results show that the risk assessment model can capture high risk areas and the generated risk map enables safe UAV path planning in urban complex environments. The statistical analysis is also conducted to test the transformational impact of risk assessment model and risk-based path planning method. Obtained results show that the proposed risk assessment model and riskbased method are effective for all types of urban patterns. 

**Keywords** : Unmanned aircraft system, third party risk modelling, risk-based path planning, hybrid algorithm, reliability validation 

## **1. Introduction** 

Applications of advanced air mobility (NASA 2020) have been extensively seeing in urban areas for various cases such as traffic monitoring, aerial photography, delivery, etc. Projection also shows that drone operation in metropolitan areas will continue to rise (Narkus-Kramer 2017). To handle the large-scale UAV operations with different tasks, autonomous flying capability is crucial. As one of the key enabler of autonomous flying, path planning problems have been widely investigated with purposes of minimizing flight distance and operational cost (Ha et al. 2018), energy consumption (Wai and Prasetia 2019), or maximizing coverage rate for surveillance mission (Wu, Wu, and Hu 2020). However, third party risk issues are essential for UAV operating in metropolitan areas, as UAV may fail and fall due to loss of control or navigation (Pang, Ng, and Low 2020). Falling UAV may cause fatalities to people (Koh et al. 2018) and damages to properties (Dalamagkidis, Valavanis, and Piegl 2008). UAV operating in low-altitude airspace also brings societal issues like noise impact and privacy concerns to the public (Lin Tan et al. 2021). These issues are considered as psychological risk cost of UAV operation to the public, which needs to be mitigated in path planning phase. In this paper, we investigate and answer the question of how to quantitively assess various UAV operational risks, and how to effectively mitigate these risks by using risk-aware airspace modelling and risk-based path planning method. 

There are existing studies investigated the risk assessment problems of UAV operation, and they focused on impact probability and severity models to people and vehicle on the ground. The authors (Mitici and Blom 2019) presented main mathematic models for conflict and collision probability estimation, which provide insights for collision risk assessment of AAM.  Pioneer works studied the probability of fatalities and the fatality rates associated with a ground impact to pedestrians, and analysis results showed that the risk of fatality to human is low in condition of light UAV operates in areas with low population density (Dalamagkidis, Valavanis, and Piegl 2008). The probability model of UAV to road traffic was also established. The authors (Bertrand, Raballand, and Viguier 2018) defined the possible ground impact area of falling UAV and developed the collision probability model, which helps for identification of 

* Corresponding author: K.H. Low (mkhlow@ntu.edu.sg) 

main risky areas of road network. Follow up works studied the impact severity of UAV to people and they subsequently proposed the weight threshold of falling UAV impact ground people based on the injury scale and criterion (Koh et al. 2018; Clothier, Williams, and Hayhurst 2018). Based on the UAV impact probability and severity studies, researcher proposed a risk-based approach for small UAV operations (Breunig et al. 2019), and generated the probabilistic map using Monte Carlo simulation for more accurate ground impact risk analysis (Levasseur et al. 2019). 

Recent studies paid attention to third-party risk modelling and analysis. The third-party risk was defined as risks pertaining to human life and property damage which are not onboard the UAV (Melnyk et al. 2014; Clothier, Williams, and Hayhurst 2018; Jiang, Blom, and Sharpanskykh 2020). In subsequent studies, a third-party risk framework was proposed to analyze the UAV ground impact risk (Melnyk et al. 2014), and third-party risk indicators and their utilization in safety regulations were proposed (Jiang, Blom, and Sharpanskykh 2020). By using these proposed frameworks, some practical studies have been conducted to model the third-party risk in urban environments (S. H. Kim 2020; Ren and Cheng 2020), and the level of risk for UAV system was also proposed to identify critical areas and actions (Gonçalves, Sobral, and Ferreira 2017). The analysis and modelling of these risks facilitate the generation of risk aware map, which can be used for risk-based path planning with aims of achieving safer UAV operation in metropolitan environments. 

UAV path planning problems have also been extensively studied with different models and optimization objectives. Exact methods like Dijkstra algorithm (Dijkstra 1959), heuristic algorithms like A* (Bell 2009), and swarm-based heuristic methods (Wu 2021; Wu et al. 2021). These methods have various optimization objectives like minimizing travel distance and cost, maximizing flight duration. These methods always consider obstacle avoidance but ignore risks underneath the UAV flying path. Extended from conventional distance or cost based path planning problems, the risk-based one is relied on a risk map used for path planning (De Filippis, Guglieri, and Quagliotti 2011; Hu et al. 2020). Various methods and algorithms were developed to generate the risk map and to cope with the risk-based path planning problems. The A*-based algorithms, for instance, was developed together with Dubins Curves for risk-based path planning and smoothing (De Filippis, Guglieri, and Quagliotti 2011). In the follow up study, the authors (Primatesta, Guglieri, and Rizzo 2019) developed a RiskA* algorithm to minimize the risk of the produced path. Genetic algorithm and Dijkstra methods are also popular in addressing this problem and been chosen as benchmarks to compare with A*-based path planning algorithm (Da Silva Arantes et al. 2017; Votion and Cao 2019). Other methods like Markov decision process was used with hierarchical method to maximize efficiency and minimize risks (Feyzabadi and Carpin 2014). A rapidly exploring random tree (RRT) was proposed to minimize the third-party risk of UAV takeoff trajectories (Rudnick-Cohen, Azarm, and Herrmann 2019). And Tabu search algorithm was employed to optimize the UAV route in order to minimize the cost of damaged cargos (Zhu et al. 2020). What is more, authors (Chung et al. 2019) also developed a risk-aware graph search algorithm to select paths which have high probability to yield low risk. On the other hand, the UAV operational environments have also been covered from factory-like area (Feyzabadi and Carpin 2014) to inhabited areas (Rudnick-Cohen, Herrmann, and Azarm 2016) and to urban environments (N. Kim and Yoon 2019). In different areas, the risk types are various. For instance, in factory area the main risk sources are critical infrastructure and property damages. While in inhabited area and urban areas, population and vehicle density, high-rise buildings are more sensitive for risk-based path planning. 

In overall, existing studies have investigated the probability and severity models of ground impact on human life and property. However, these models rarely considered the mobility of population density in metropolitan areas, which fails to accurately capture the population density distribution a major contributor in risk modelling. Various risk types (fatality, property, etc.) have been investigated individually in different environments. However, an integrated risk assessment model is still lacking to cope with various risks in complex metropolitan environments. Lastly, existing path planning methods rarely incorporated risk cost into fitness function, and with even less studies investigated the risk-based heuristic function to improve optimality and efficiency of the risk-based path planning method. 

In this paper, we propose an integrated risk assessment model with 3D risk aware airspace modelling, and we also develop a robust and effective algorithm to address the risk-based path planning problems with the goal of minimizing operational risk. We summarize the main contributions of this article as follows. 

- (1) We establish an integrated risk assessment model with a gravity model to better estimate the population density distribution and to capture high risk areas in a finer scale. The model considers three main risk categories in urban environments, which includes fatality risk (human life), property damage risk (infrastructure), and societal impact risk (noise and privacy). The introduced societal impact risk enables public perception of drone operation been considered in safe and sustainable airspace management and UAV operation planning. 

- (2) We formulate the risk-based 3D path planning problem as a special case of minimum cost flow problem. The objective is to find a minimum cost flow starting from origin to destination (OD) among the graph, with constrains of motion step size, flight consistency and obstacle clearance. 

- (3) We develop a hybrid algorithm integrating estimation of distribution algorithm, k-means method and improved A* algorithm (named as EDA-FRA*) to solve large scale 3D risk-based path planning problems. The outer loop of the EDA-FRA* algorithm is a 0-1 optimization problem, which aims for selecting and optimizing the low risk-cost path points based on OD information. The k-means clustering algorithm is introduced to extract heuristic information from selected low-risk path points for A* path searching algorithm to produce a riskcost-effective path with high robustness and efficiency. 

The rest of the paper is structured as follows. Section 2 analyzes the risk types in urban environments and illustrates the concept of risk aware airspace and path planning. The integrated risk assessment model is established in Section 3. The mathematic problem formulation and the hybrid 3D path planning algorithms are developed in Section 4. Followed by simulation validations and case studies in Section 5. Section 6 concludes the main findings of this article. 

## **2. Problem background** 

In metropolitan environments, there are dense populations, high-rise buildings, critical infrastructure, etc. UAV operates in such low altitude airspace will encounter various risk issues (Ghasri and Maghrebi 2021). In this paper, the scope of operation altitude is below 400 feet (Federal Aviation Administration 2020) above the ground. Recent studies investigated various risks in urban environments, and most of their attentions are on the risks of  the impact on ground people and road network (Bertrand, Raballand, and Viguier 2018; Clothier, Williams, and Hayhurst 2018), midair collision with small UAS and manned aircraft (Zou et al. 2021; Wang, Tan, and Low 2019), impact of noise and privacy issues (Vascik and Hansman 2018; Lin Tan et al. 2021), as well as UAV operational cost and efficiency (Ha et al. 2018). We conclude the primary risk sources as three categories as follows, illustrated in Fig. 1. 

- (1) Fatality risk. UAV impact pedestrians and vehicles on the ground, causing injuries or fatalities on people. 

- (2) Property damage risk. Falling UAV hits critical infrastructures or collides with high-rise buildings, causing property loss. 

- (3) Societal impact risk. Noise and privacy impact to the public is a big concern for the acceptance of UAV operation in urban environments. These impacts are modelled as societal impact risk, which will be assessed and mitigated. 

Other risk factor like midair collision of UAV and manned aircraft in integrated urban airspace (Vascik and Hansman 2019) is not considered in this work, because airport performs segregated operation with UAV and the Aerodrome Control Zone is treated as restricted area where the UAV is strictly not allowed to enter. Risks of UAV intruding military-related bases and facilities are also out of scope of this article. 


![](1_survey/papers/md/Pang2021Third_figs/Pang2021Third.pdf-0003-08.png)


**----- Start of picture text -----**<br>
Fatality risk of<br>impacting people and<br>vehicle on the ground<br>Property<br>h v damage risk<br>to buildings<br>h p<br>l obs. Noise and<br>privacy impact<br>h s<br>on people<br>**----- End of picture text -----**<br>


**Fig. 1.** Illustration of three primary risk types in metropolitan environments. 

The identified risk sources of population density, vehicle density and buildings are discretely distributed in metropolitan environments. Subdivision of airspace into smaller manageable unit enable more flexible managing (Cho and Yoon 2019). To quantitatively assess these risks, urban low-altitude airspace is divided into discrete 3D air block unit (Pang, et al. 2020) and the centroid of the unit is denoted as 𝑣!"# (Fig. 2(a)). UAV operates from one air block to another with 26 possible points to choose for the next move.  Risk assessment of each airspace unit is conducted based on its pertaining environments such as population density and vehicle density underneath. UAV operates following the centroid point to maintain safe separation with other UAVs in adjacent air blocks. The risk is represented as colored 

air blocks (Fig. 2(b)), and the 3D risk map is illustrated as Fig. 2(c). UAV operates in complex 3D risk map to avoid high risk areas (presented as red color) and to minimize total operational risk. 


![](1_survey/papers/md/Pang2021Third_figs/Pang2021Third.pdf-0004-01.png)


**----- Start of picture text -----**<br>
Risk cost z<br>Low High<br>Origin<br>y<br>Destination<br>x<br>(a) 26 choices from current position  (b) Risk-aware airspace and flight path<br>(c) 3D view<br>to next position demonstration<br>**----- End of picture text -----**<br>


**Fig. 2.** Risk aware airspace modelling and risk representation. 

The core of the risk aware airspace model and path planning is the accurate and quantitative risk value of each airspace unit. To achieve this, an integrated risk assessment model is proposed to compute the risk value. 

## **3. Risk modelling and assessment** 

The integrated risk assessment model includes three main parts: fatality risk cost model, property damage risk cost model, and societal impact risk cost model. 

## _3.1.  Fatality risk cost model_ 

## _3.1.1.  Risk of UAV impacts people on the ground_ 

As it is possible that UAV might be loss of control or power when operating, falling UAV may impact people on the ground (see Fig. 1). There are three processes (Bertrand et al. 2017; Hu et al. 2020) a crash incident will cause injury or fatality to pedestrians: (a) failure of UAV; (b) falling UAV impacts people on ground; and (c) fatality damage caused to the people. 

That falling UAV hits people on the ground causing fatalities is a chain action, which corresponds with the three processes mentioned above. The risk cost of UAV impacting ground people is defined as the number of fatalities per hour, denoted as 


![](1_survey/papers/md/Pang2021Third_figs/Pang2021Third.pdf-0004-10.png)


where 𝐶$_& is the risk cost associated to the fatality of people, and 𝑃'$()* is the probability of UAV failure. Note that 𝑁*+,& is the number of pedestrians hit by falling UAV (proportional to the population density of people), and 𝑅-& is the fatality rate associated to the function of kinetic energy. 

The 𝑃'$()* is primarily determined by the capability of UAV itself, including hardware and software capabilities and reliability. The 𝑅-& is strongly correlated with the weight and falling height of the UAV. The most uncertain variable in Eq. (1) is the 𝑁*+,& , which associates with the population density, defined as 


![](1_survey/papers/md/Pang2021Third_figs/Pang2021Third.pdf-0004-13.png)


where 𝑆*+, is the explored area of UAV impacts the ground, and 𝜎& is the population density in the administrative unit 𝑢. 

The fatality rate 𝑅-& associates with two main factors: impact kinetic energy and sheltering effects. The kinetic energy 𝐸+.& of falling UAV primarily determines the severity of impact, while the sheltering coefficient 𝑆/ affects the degree of impact on the people and vehicle, as the buffering effects of buildings, trees, etc. will soften the ground impact on them. Inspired by (Primatesta, Rizzo, and la Cour-Harbo 2020), the sheltering coefficient 𝑆/ is introduced as the absolute real number 𝑆/ = (0,1], and the fatality rate is presented as 


![](1_survey/papers/md/Pang2021Third_figs/Pang2021Third.pdf-0005-00.png)


where 𝛼 is the impact energy that might cause 50% fatality with 𝑆/ = 0.5, while 𝛽 is the impact energy threshold required to cause fatality as 𝑆/ approaching zero (see Fig. 2 in (Dalamagkidis, Valavanis, and Piegl 2008)). Based on that, we take 𝛼 =10[6] J and 𝛽 =100 J. 

The impact kinetic energy 𝐸+.& of the falling UAV is known as 


![](1_survey/papers/md/Pang2021Third_figs/Pang2021Third.pdf-0005-03.png)


where 𝑚 (kg) is the mass of the falling UAV, and 𝑣 is the velocity when UAV hitting the ground stuff. To compute 𝑣, we have the followings. 

The vertical drag force 𝐹6 of falling UAV is related to its size and materials, as well as the density of air, etc., denoted by (Koh et al. 2018) 


![](1_survey/papers/md/Pang2021Third_figs/Pang2021Third.pdf-0005-06.png)


where 𝑅7 is the drag coefficient related to the UAV type, 𝜌8 is the density of air (1.225 kg/m[3 ] at sea level), and 𝑣9:; is the true air speed of falling UAV. 

Then the acceleration of UAV is 


![](1_survey/papers/md/Pang2021Third_figs/Pang2021Third.pdf-0005-09.png)


where 𝐹C is the gravitational force, 𝐹C = 𝑚𝑔. (g=9.8m/s[2] ) 

Thus, the 𝑣 at moment 𝑡 which UAV hits ground can be obtained as 


![](1_survey/papers/md/Pang2021Third_figs/Pang2021Third.pdf-0005-12.png)


where ℎ is the start falling height of UAV above the ground surface. 

## _3.1.2.  Risk of UAV impacts vehicle on the ground_ 

Similar to the risk model of people impact, there are also three components of a crash incident on road network (Bertrand, Raballand, and Viguier 2018): (a) UAV failure; (b) falling UAV hits a ground vehicle; (c) the crash incident causes a traffic accident which subsequently cause injuries or fatalities to people. 

The expected fatality of UAV impacting a ground vehicle can be defined as the number of fatalities per hour caused by falling UAVs, denoted as 


![](1_survey/papers/md/Pang2021Third_figs/Pang2021Third.pdf-0005-17.png)


where 𝐶$_F is the risk cost associated to vehicle. Note that 𝑁*+,F is the number of vehicles hit by falling UAV (proportional to the traffic density), and 𝑅-F is the average fatality rate associated to vehicle accident. 

The average number of ground vehicles which may hit by falling UAV can be defined as the ratio of total area of all vehicles projected and the total road area, denoted as 


![](1_survey/papers/md/Pang2021Third_figs/Pang2021Third.pdf-0005-20.png)


in which 𝜎F is the traffic density in the administrative unit 𝑢. 

## _3.1.3.  Estimation of population density and traffic density using gravity model_ 

The population density and traffic density distributions in metropolitan environments are the essential variables which will directly influence the UAV operational risk costs as discussed in Eq. (1), (2) and Eq. (8), (9). Based on the previous studies, these density distributions are strongly correlated with the consumption amenities (Rappaport 2008), which attracts people and vehicle. To quantitively assess this correlation between consumption amenity and population density, the gravity model was used to calculate the population density (Yao et al. 2017). Inspired by the gravity model (Pang et al. 2021) and population mapping method (Deville et al. 2014), we have the following formulas to compute the population density in urban environments. 

The population density of given unit 𝑢 is given as 

𝜎& = 𝑒[(0=G][4][)] 𝜎&.(FI (10) 

where 𝜎&.(FI  is the average population density in the given area. Note that 𝑟 is the radius of the gravity influence area induced by the amenity, which is given as 1 km in this work. As shown in Fig. 3, the population density decreases in an inverted exponential pattern with increase of the radius 𝑟. In first 0.3 km, the index remains high, capturing the high population density distribution in the very vicinity of amenities. While in range of 0.3 km to 1.0 km, the index drops linearly, demonstrating the even decrease of population density. 


![](1_survey/papers/md/Pang2021Third_figs/Pang2021Third.pdf-0006-02.png)


**Fig. 3** .  Illustration of population density index changes with influence radius _r._ 

Similarly, the road traffic density distribution can be denoted as 


![](1_survey/papers/md/Pang2021Third_figs/Pang2021Third.pdf-0006-05.png)


where 𝜎F.(FI is the average traffic density in the given area. 

The UAV operational risks to people and vehicle can be considered as fatality risk cost 𝐶$_J, presented as: 


![](1_survey/papers/md/Pang2021Third_figs/Pang2021Third.pdf-0006-08.png)


## _3.2.  Property damage risk cost model_ 

Dense high-rise buildings in urban environments is another challenge to perform UAV operations. Potential collisions with buildings pose property damage risks, and densely distributed high-rise buildings also limit the speed of traffic flow, resulting in the inefficiency of UAS system (Ang and Hansen 2019). Thus, the property damage risk cost model also integrates the operational efficiency cost, which are accounted for planning and optimization of airspace and traffic flow. 

The flight altitude is a primary variable of the property damage risk model. As Fig. 4(a) depicted, in low altitude layer (Layer 1 for instance), the density of building is high. UAV operating in Layer-1-type airspace needs to frequently perform deconflictions to avoid obstacles, thus increasing risks and efficiency loss. In high altitude layer (i.e. Layer 4), in contrast, there are few buildings to affect UAV operation, so that the operational safety and efficiency can be significantly improved. 

The building height distribution is not fit with standard normal distribution but log-normal distribution (Kirtner and Anderson 2008; Usui 2019), as building height is the nonnegative value and its distribution is not symmetry. Based on the height distribution relationship, the correlation between building height and property damage risk cost can be established as 


![](1_survey/papers/md/Pang2021Third_figs/Pang2021Third.pdf-0006-13.png)


where 𝜇 and 𝜎 are the mean and standard deviation of the logarithmic variable (building height ℎ). Note that 𝐶$_&.O is the risk cost of property damage upon drone operation. For buildings with height smaller than the threshold of 𝑒[P] , the risk cost equals to the one which the height 𝑒[P] has (as Eq. (14) defines). Which is because below that height (ℎ= 𝑒[P] ), buildings are dense and the risks are high. The biggest risk cost value is therefore being given, and which is taken at 

height ℎ= 𝑒[P] . In this case, 𝜇= 3.0467 as computed above. While for buildings with height greater than 𝑒[P] , the operational risk cost is computed as the log-normal distribution presents in Eq. (13). Meaning that with the increase of building height (ℎ> 𝑒[P] ), the property damage risk cost decreases, as in higher layers there are few building obstacles to influence the safety of UAV operations. Note that the property damage risk factor is to facilitate the determination of optimal flight layer in particular areas. UAV should not collide with buildings in any flight layer with any building density. 


![](1_survey/papers/md/Pang2021Third_figs/Pang2021Third.pdf-0007-01.png)



![](1_survey/papers/md/Pang2021Third_figs/Pang2021Third.pdf-0007-02.png)


(a) Illustration of building height distribution                             (b) Log-normal distribution of building height 

**Fig. 4.** Building obstacles impact on UAV operation in urban area. In (a), the building height data is selected from a particular city area in Singapore, where 100 building clusters have been selected to illustrate the building height distribution. In (b), the statistical features of building height distribution are analyzed using log-normal distribution. Here, the height frequency presents the number of buildings at such height. 

## _3.3.  Societal impact risk cost model_ 

Noise and privacy impacts are important societal issues and need to be considered when UAV operates in low altitude urban environments (Lin Tan et al. 2021), as low-flying UAV may upset people and make them feel annoying. That will be therefore considered as risk cost when conducting planning. The impacts of noise and privacy issues to the public are the same because their impacts are in effective when UAV operating close to people especially at nighttime. While with the increase of flying altitude, the impacts will decrease to the threshold which will not have effects on ground people. As the privacy risk cost is hard to be captured while it has the same nature of impact with noise issue, the societal risk model is therefore presented by noise impact risk model. The correlation of noise induced risk cost and its flying height is illustrated as Fig. 5. Based on the analysis, we know that the key factor of noise impact to people is UAV flying height. 

A good first approximation of sound propagation is the spherical spreading, denoted as 


![](1_survey/papers/md/Pang2021Third_figs/Pang2021Third.pdf-0007-08.png)


where 𝐼(𝑠𝑖) is the sound intensity at height ℎ and distance _d_ from the point directly under the drone. Here _d_ is taken as 30 feet (Alexander and Whelchel 2019). 


![](1_survey/papers/md/Pang2021Third_figs/Pang2021Third.pdf-0007-10.png)


in which 𝐿(𝑠𝑙) is the sound level (dB); 𝜛 is the convert coefficient from sound intensity to sound level; LK is the reference noise produced by drone, taken as LK = 60dB (Bulusu et al. 2017). 


![](1_survey/papers/md/Pang2021Third_figs/Pang2021Third.pdf-0007-12.png)


where 𝐶$_Q is the risk cost of noise upon drone operation in the given airspace unit. Noise impact will not be considered as risk cost for UAV operation if flying height exceeding the threshold. Based on previous studies (Bauer 2019; Torija, Li, and Self 2020), we take the height threshold as the one corresponded to the noise level of 40dB, illustrated as Fig. 5(b). 


![](1_survey/papers/md/Pang2021Third_figs/Pang2021Third.pdf-0008-00.png)


**----- Start of picture text -----**<br>
h<br>d<br>**----- End of picture text -----**<br>



![](1_survey/papers/md/Pang2021Third_figs/Pang2021Third.pdf-0008-01.png)



![](1_survey/papers/md/Pang2021Third_figs/Pang2021Third.pdf-0008-02.png)


(a) Illustration of noise impact on people                           (b) Correlation of noise level and flying height **Fig. 5.** UAV noise impact on people. 

## _3.4.  Integrated risk cost model_ 

The three risk cost models are discussed and developed above. To integrated them together as a comprehensive model, normalization is made for each type of risk. Obtained risk cost in each airspace unit 𝑢 will be divided by the maximum risk value of their own categories. All risk cost values of each type will be therefore ranged in (0,1]. The generalization factors are the reciprocal of the maximum risk cost for the corresponding type, denoted as: 


![](1_survey/papers/md/Pang2021Third_figs/Pang2021Third.pdf-0008-06.png)


Note that 𝜔$_J _,_ 𝜔$_&.O and 𝜔$_Q are the generalization factors, which are used to keep the same order of magnitude for the three risk types. 

The total operational risk cost in the given airspace unit integrates fatality cost, property damage risk cost and societal risk cost together. As the weight of these three types of cost might be different due to their significance or user’s preferences (Liu et al. 2020), the contribution of each type of cost will also be various. For instance, aviation regulators may take safety as top priority, requiring a very low fatality risk cost of UAV operation. In this regard, the weight of fatality cost will be much greater than the other two factors. Thus, areas with dense population and vehicle will be identified as high-risk areas by proposed model, and the path planning will subsequently avoid these areas. To quantify the significance and preferences of UAS stakeholders on different risk types, the weight factors are introduced, and the total operational risk cost is computed as 


![](1_survey/papers/md/Pang2021Third_figs/Pang2021Third.pdf-0008-09.png)


where 𝛼] is weight factor, 𝜔] is generalization factor and 𝐶] is risk cost. Here 𝑖= 1, 2, 3 corresponds to fatality risk, property damage risk and noise impact risk, respectively. Note that {𝛼0, 𝛼5, 𝛼^}∈[0,1], while 𝛼0 + 𝛼5 + 𝛼^ = 100%. 

## **4. Modelling of risk-based 3D path planning** 

In defined discrete airspace environment, the risk-based path planning problem is formulated, based on graph theory, as minimum cost flow problem in an undirected graph. To solve this problem, a hybrid algorithm has been proposed incorporating EDA and A* algorithms. The outer loop of the EDA-RA* algorithm is a 0-1 optimization problem, which aims for selecting and optimizing the path points as feasible search region. The optimized feasible region will be feed into the inner loop, where A* algorithm is employed, to generate the cost-effective path. To better improve the computational efficiency of the hybrid algorithm, the k-means clustering algorithm is introduced and incorporated to provide heuristic information for A* path searching algorithm, which is named as EDA-FRA*. Detailed problem formulation and algorithms development are presented in followings. 

## _4.1.  Problem formulation of risk-based path planning_ 

To facilitate the risk cost assessment, the airspace is divided as uniform unit 𝑢 in three-dimensional space. The centroid of the airspace unit 𝑢] is presented as vertex 𝑣](𝑥], 𝑦], 𝑧]), and the UAV operational risk cost in that unit is denoted as 𝐶$_]. The problem of finding a path from origin to destination with minimum cost is a special case of the minimum cost flow problem, which can be modelled as follows. Let 𝐺= (𝑉, 𝐸) be an undirected, connected and weighted graph such that all edge weights are nonnegative, with weight function 𝐶: 𝐸→ℝ1E and let 𝑠 and 𝑡 be distinct vertices of 𝐺. A path 𝑃 from 𝑠 to 𝑡 in 𝐺 is called the most risk-cost-effective path if 𝐶(𝑃) = ∑`∈b 𝐶(𝑒) is minimum among all paths from 𝑠 to 𝑡 in 𝐺. Here the weight function is equivalent to the risk cost function of Eq. (19). 

## _A. Objective_ 

The objective of this work is to minimize the total risk cost of planned path for UAV operation. The total risk cost consists of human fatality risk, property damage risk and societal impact risk. 


![](1_survey/papers/md/Pang2021Third_figs/Pang2021Third.pdf-0009-04.png)


where 𝐶(𝑃) is the total risk cost of the path 𝑃, and 𝐶m𝑒cn is the risk cost of edge 𝑒c. Note that P is the set of all edges included in the path. 

Based on the risk assessment model, minimizing the total risk cost is to optimize several key variables, which are positions and flight altitude of UAV. In the model, they are presented as the 3D coordinate (𝑥], 𝑦], 𝑧]),  for each path point. 

## _B. Constrains_ 

As Fig. 2(a) shows, there are 26 available vertices can be chosen as the next point to move. Specifically, there are 6 vertices which are straightly connected with the current vertex 𝑣], while 12 vertices connected as planar diagonal and 8 vertices connected as cubical diagonal. Let 𝑙 be the length of the unit 𝑢. The motions and constrains of UAV in the discrete airspace can be expressed as follows. 


![](1_survey/papers/md/Pang2021Third_figs/Pang2021Third.pdf-0009-09.png)


where (𝑥]10, 𝑦]10, 𝑧]10) is the next path point 𝑣]10 we are choosing to move, and  (𝑥], 𝑦], 𝑧]) is the current position 𝑣]. Note that 𝜉!] , 𝜉"] , 𝜉#] are the unit lengths of each move corresponding to x-axis, y-axis and z-axis, respectively. Here the 𝑋>d!, 𝑌>d! and 𝑍>d! are the boundaries of defined airspace in each axis. 

As the step size in each axis is 𝑙, the first constrain is the unit moving length, which can only be chosen from alternative values of {- 𝑙 ,0, 𝑙 }, presented in Eq. (21). Assuming hovering is not allowed, the second constrain is that UAV must then take a move in whatever axis, which is denoted as the sum of the unit length must not equal to zero. 

The third constrain related to obstacle avoidance. UAV should not collide with buildings in any situation, meaning that UAV should not enter the airspace unit, which is occupied by buildings. Therefore, we give the infinite risk cost to points which belong to building-occupied airspace, presented as 


![](1_survey/papers/md/Pang2021Third_figs/Pang2021Third.pdf-0009-13.png)


in which 𝐶$_e is the cost of these path points which are included in the occupied airspace. Note that Ufg) is the airspace unit set containing all building-occupied units 𝑢e. 

## _4.2.  A hybrid EDA-RA* algorithm for risk-based path planning_ 

To solve the developed minimum cost flow problem, there are several types of algorithms we can choose. Exact methods, like Dijkstra algorithm, is one of the classic and effective graph-based path-searching methods, which has been extensively used for path planning problems. However, Dijkstra is a computational inefficiency method, especially in dealing with large-scale problems like the one this paper studied. Heuristic methods, like A* algorithm, has better performance in solving path planning problem in terms of computational time without reducing the quality of solutions, provided the accurate heuristic information can be offered. 

For the standard A* algorithm, the heuristic distance can be surely determined either as Manhattan distance or Euclidean distance (Fig. 6(a)) to estimate the distance from current position to destination. However, in the risk-based 

environment, the cost of each grid is different and unevenly distributed, making it hard to determine the heuristic distance (Fig. 6(b)). What is more, as the scale of the problem getting large, it is difficult for the heuristic methods which initiated with only one solution to search for the outstanding solutions from the feasible ones.  In this regard, conventional A* algorithm is not suitable for the problem. 


![](1_survey/papers/md/Pang2021Third_figs/Pang2021Third.pdf-0010-01.png)


**----- Start of picture text -----**<br>
Manhattan<br>distance ( x end,  y end) ( x end,  y end) ( x end,  y end)<br>Cluster<br>centriod<br>Heuristic<br>Euclidean  distance<br>distance (global)<br>( xi ,  yi )<br>( xi ,  yi ) Heuristic<br>Risk-based  ( xi , yi ) direction<br>heuristic  (local)<br>information<br>( x start,  y start) ( x start,  y start) ( x start,  y start)<br>(a) (b) (c)<br>**----- End of picture text -----**<br>


**Fig. 6.** Analysis of heuristic distance between classic A* algorithm and risk-based A*. Note that (a) shows that the classic A* algorithm normally has two options of its heuristic distance, Manhattan distance and Euclidean distance. For (b), the heuristic distance is chosen as risk-based distance, as the risk cost distribution from current node (𝑥#, 𝑦#) to target node (𝑥$%&, 𝑦$%&) is unknown and unpredictable. For (c), the heuristic distance path is directly from current node to destination (global heuristic information). While the heuristic direction path is generated by connecting the cluster centroids to provide local heuristic information. 

Swarm-based heuristic methods, on the other hand, initiate with a number of solutions and are suitable to solve the outer loop of our proposed problem. EDA is one of the typical swarm-based algorithms for solving both the continuous and discrete optimization problem. In this paper, the optimization variables of the problem are the 3D coordinate of path points, and the number of them are not fixed. EDA method is well aligned with these requirements, as it has no limitation for the number of variables, and it performs well in terms of global searching. In this work, the EDA method will be used to solve the outer loop 0-1 optimization problem, and it is incorporated with improved A* algorithm to generate the cost-effective path. 

EDA algorithm is a stochastic method. The core of it is to generate and sample explicit probabilistic models of the promising solutions to guide the search for the optimum. The optimization process can be seen as a series incremental update of the probabilistic model to achieve the global optimal solution. That characteristic is good for globally optimizing the feasible region for the A* searching algorithm, which is the inner loop of the hybrid method to generate the path point by point. The general outline of the hybrid EDA-RA* algorithm for min-cost path planning is presented as **Algorithm 1** . 

The EDA-RA* algorithm operates on a 3D operational risk-based airspace map, and the cost value is computed by the proposed risk cost assessment model. The output of this algorithm is the optimized path and total risk cost of the path. The main loop of the algorithm is from Line 6 to Line 23, which is concerned with the EDA method to optimize the feasible region, and A* algorithm for path generation. 

The essential part of EDA-RA* algorithm is the probability update function (Line 22). By selecting the dominant populations from the species, the function is updated towards that the individuals, which belongs to dominant populations, will have increasing probabilities to be selected as optimal points in the graph. The update function is denoted as: 


![](1_survey/papers/md/Pang2021Third_figs/Pang2021Third.pdf-0010-07.png)


where the 𝒑 is the array that stores the probability of being selected for each individual, and  𝑙$(,h is the learning rate, which is the evolving factor to accelerate the optimization process with the accumulation of dominant species data. Note that 𝑫𝑺 is the array of dominant species, and DN is the total number of the species. 

The selection of dominant populations is based on the fitness value. Here, the fitness value is the sum of risk cost value for vertices belong to the selected path, presented as 


![](1_survey/papers/md/Pang2021Third_figs/Pang2021Third.pdf-0010-10.png)


As EDA is a stochastic method based on probabilistic model, during the iteration, some populations might be stuck by obstacles and may not be able to find path from origin to destination. The total risk cost for these populations will be replaced by the maximum risk cost among the whole species (Line 18). In subsequent iterations, these populations will be eliminated, and the selected dominant population will not have problem to find a feasible path. 

**Algorithm 1** : Hybrid EDA-RA* algorithm for minimum risk-cost 3D path planning 

- **1:**[Result: ] _[path]_[ , ] _[TotalCost]_ 

**2:** load CostDataset **3:** _[path]_[ =] _[null]_[;] **4:** _[TotalCost]_[ =0;] **5:** initialize the probability matrix for EDA **6: for** _i_ =1:iterations %EDA outer loop **7: while** _j_ <=populationSize **8:** r=rand(size(CostDataset)); **9:**[            species{] _[j]_[,1} = 1.*(r<probability);] **10:** _[ j]_[=] _[j]_[+1;] **11: end 12:** save species **13: for** k=1:populationSize % A* inner loop **14:** path=A*(species, obstacle); **15:** TotalCost=FitnessValue(path); **16:** TC=[TC;TotalCost]; **17: end 18:** TC(replaceNP, :)=max(TC); **19:** FitnessValue=TC; **20:** [Fitness, index] = sort(FitnessValue); **21:**[dominantSpecies{:, 1} = species{index(:), 1}; ][%][select dominant population] **22:** probability = (1- _l r_ ate)*probability+ _l_ rate*dominantSpecies/dominantNum; 

**23: end** 

**24: Return** ( _path_ , _TotalCost_ ) 

## _4.3.  An improvement of EDA-RA* with fast computation: EDA-FRA*_ 

The EDA-RA* algorithm incorporates A* as inner loop, and it is conducted for every population of the species at every iteration. Although the A* conducts very fast, this algorithm will cost considerable computational time as the problem scale getting larger. To cope with this problem, we further improve the EDA-RA* algorithm by introducing k-means method to provide both global and local heuristic information for path searching (see Fig. 6(c)). The improved hybrid algorithm is named as EDA-FRA*. Besides, the A* algorithm will also be improved to cater for the unique needs of risk-based 3D path planning problem. 

The hybrid EDA-FRA* algorithm has three main functions. First function is EDA algorithm, which is used to globally optimize the feasible region that has low risk cost among all searching space. The second is the k-means algorithm. Based on the optimized feasible region, k-means clusters the feasible vertices to identify the heuristic directions (main tracks) and heuristic distance factor. The identified heuristic information will be ingested into the improved risk-based A* algorithm (named as RiskA* for easy reference) to generate the risk-cost-effective path. As the improved RiskA* algorithm is only called once, the speed of EDA-FRA* is much faster than that of the EDARA*. The pseudocode of the hybrid EDA-FRA* algorithm for fast minimum risk-cost path planning is shown in **Algorithm 2** . 

The EDA algorithm independently process the cost data and output the best population of the feasible region (Line 5). The obtained best population is further processed to get the position of open points (Line 6-Line 9). The k-means method is then employed to obtain the centroid position of clusters, and to generate the heuristic distance factor and heuristic direction for RiskA*. The heuristic distance of RiskA* is improved from Euclidean distance to estimate the total risk cost from current node to destination, presented as 

ℎk+), = 𝑓K`no]pD‹(𝑥o −𝑥])[5] + (𝑦o −𝑦])[5] + (𝑧o −𝑧])[5] (25) 


![](1_survey/papers/md/Pang2021Third_figs/Pang2021Third.pdf-0012-00.png)


in which ℎk+), is the improved heuristic distance for RiskA*, and (𝑥], 𝑦], 𝑧]) is the coordination of current point and (𝑥o, 𝑦o, 𝑧o) is the destination point, which are used to compute the Euclidean distance. Note that 𝑓K`no]pD is the heuristic distance factor, which takes the minimum value among the mean risk cost of all open points V[&hQ and the mean risk cost of cluster centroid points Vr,$). Taking the minimum value is because smaller heuristic value leads to better quality of solution for RiskA* algorithm. The solution will reach optimum when heuristic value down to zero, and the RiskA* is then equivalent to Dijkstra. The determination of the heuristic value for the algorithm is to make a trade-off between the quality of solution and computational efficiency. 

**Algorithm 2** : EDA-FRA* algorithm for fast minimum risk-cost 3D path planning 

- **1:**[Result: ] _[path]_[ , ] _[TotalCost]_ 

**2:** load CostDataset 

**3:** _[path]_[ =] _[null]_ 

**4:** _[TotalCost]_[ =0;] 

**5:**[BestPop=EDA(CostDataset); ][% ][obtain the best population] 

**6: if** sum(BestPop( _i_ , _j_ , _k_ ))==1  % obtain open points for path searching 

**7:**[     IndivPosn=[] _[i]_[, ] _[j]_[, ] _[k]_[];  ][% ][get the index of the open points] 

**8:** Posn=[Posn; IndivPosn]; 

**9: end** 

**10:**[[Ctrs, heuDist] _[f]_[, heuDrctn]=k-means(Posn); % obtain heuristic information] 

**11:**[[] _[path]_[ , ] _[TotalCost]_[ ]=RiskA*(CostDataset, heuDist] _[f]_[, heuDrctn);] 

- **12: Return** ( _path_ , _TotalCost_ ) 

The total risk cost function from origin to destination can be then described as 


![](1_survey/papers/md/Pang2021Third_figs/Pang2021Third.pdf-0012-16.png)


where 𝑔(C) is the integral of the risk cost from origin 𝑣s to current point 𝑣], and ℎk+),(C) is obtained by Eq. (25). Note that 𝐶(𝑣) is the risk cost of path point 𝑣. 

The heuristic direction is represented by a set of segments, which starts from origin connecting cluster centroids to the destination (Fig. 6(c)). The heuristic distance provides global information by selecting the node with the smallest distance 𝑓(C) to destination. While the heuristic direction assists with local searching by evaluating the distance cost from current node to the local cluster centroid. The key part of RiskA* framework is given as **Algorithm 3** . 

**Algorithm 3:** Improved RiskA* algorithm for minimum risk-cost path planning **1:**[Result: ] _[path]_ **2:**[load CostDataset, heuDist] _[f]_[, heuDrctn] **3: for** _i_ = 1:26 % possible choices of next position **4:**[      next = [] _[x]_[(] _[i]_[), ] _[y]_[(] _[i]_[), ] _[z]_[(] _[i]_[), CostDataset(] _[x]_[(] _[i]_[), ] _[y]_[(] _[i]_[), ] _[z]_[(] _[i]_[))]; ][%][ next position and its cost value] **5:** Motion=[Motion; next]; **6: end 7:**[MotionMode{} = Motion; ][% ][record the moving cost matrix for every open points] **8:** _[g]_[(c)=] _[f]_[(MotionMode{c});] **9:**[hDistDest(c)=] _[f]_[(heuDist] _[f]_[, ] _[v]_[(c)); ][%][ heuristic distance to destination] **10:**[hDistCtrs(c)=] _[f]_[(heuDrctn, ] _[v]_[(c)); ][%][ heuristic distance along the cluster centriods to destination] **11: if** hDistCtrs(c)-hDistDest(c)<ԑ % degree of deviation from main track, ԑ>=0 **12:**[    hDist(c)=hDistDest(c); ][%][ Dev is acceptable, put currrent point a small estimated cost] **13: else 14:**[    hDist(c)=hDistCtrs(c); ][%][ unacceptable, put currrent point a high estimated cost, it will be then discarded] **15: end 16:** _[f]_[(c)=] _[g]_[(c)+hDist(c); ][%][ distance funtion] **17: if** _f_ (c) < open( _f_ (:)) % distance from current point to destination less than that of the points in openlist **18:** Putting current point as father point, and it will be included in the path **19: end 20: Return** ( _path_ ) 

The motion mode function is to obtain the risk cost value of the adjacent 26 possible positions. The cost matrix of all feasible points is computed and stored in the MotionMode array, which is employed to compute the total risk cost 𝑔(C) from origin point to current point. For the second part, the heuristic distance ℎk+), is computed to estimate the distance from current point to destination. The ℎk+),o`pD (Line 9) is computed by Eq. (25). While ℎk+),tDGp (Line 10) the heuristic distance along the cluster centroids to destination is the sum of segment distance products the heuristic factor 𝑓K`no]pD. As Fig. 6(c) depicted, the heuristic distance path is directly from current node to destination, while the heuristic direction path is generated by connecting the cluster centroids. The ℎk+),o`pD globally inspires the path searching process, and the ℎk+),tDGp assists with local searching by evaluating the deviation between heuristic direction and actual path searching one (Line 11 to Line 14). If the deviation exceeds the threshold 𝜀, that node will be given an infinite cost and it will be removed in the next iteration. Here the 𝜀 is taken as 0.2, which presents the deviation between main track and current track. 

With the development above, the framework and relationship of EDA-RA* and EDA-FRA* are presented in Fig. 7. There are two similarities of the two hybrid algorithms. They use same risk cost data as input and they employ EDA to generate initial solution of feasible regions. The difference between the two algorithm is prominent. For EDA-RA*, the A* algorithm is called for each single iteration to produce path for all species. By giving dominant path points high probability of been selected into feasible region, the final optimized path will effectively search all space and obtain a good quality of solution. While for EDA-FRA*, the main loop is to optimize the feasible region. It calls RiskA* only once after obtaining the optimized feasible region. That significantly saves computational time whereas the optimized feasible region may not be as good as the EDA-RA* has. 

The EDA-RA* can achieve better feasible region and solution quality, but it costs more time to compute. In comparison, the EDA-FRA* is much faster as it calls RiskA* only once while the solution quality may not compete with EDA-RA*. Simulation and case studies are conducted in next section to validate the proposed hybrid algorithms in term of computational efficiency and quality of solutions. 


![](1_survey/papers/md/Pang2021Third_figs/Pang2021Third.pdf-0013-03.png)


**----- Start of picture text -----**<br>
Initial parameters<br>i =1,  j =1<br>Input: Risk<br>cost dataset<br>EDA-RA* begins with  i th iteration EDA-FRA* begins with  j th iteration<br>Generate solution of feasible region via EDA<br>j = j +1<br>i = i +1<br>Conduct risk-based path planning for  Select the dominant path points with<br>each species using RiskA* low risk cost and increase the<br>probability of being chosen for them<br>Select the dominant paths with low<br>risk cost and increase the probability  No<br>of being chosen for these path points  j> Nmax (No. of iteration)<br>Yes<br>No<br>i> Nmax (No. of iteration) Output: Optimal feasible region, k-<br>means produced heuristic information<br>Yes<br>Output: the optimized risk  Conduct risk-based path planning<br>cost-effective path based on the optimal feasible region<br>Final solutions are obtained<br>**----- End of picture text -----**<br>


**Fig. 7** .  Framework of EDA-RA* and EDA-FRA* algorithms. 

## **5. Simulation studies** 

To validate the proposed risk cost assessment model and the developed hybrid risk-based 3D path planning algorithms, we perform simulations and case studies in the context of a representative metropolitan area. Firstly, the risk assessment model is implemented in a real-world environment to generate 3D risk-aware airspace map. We then apply the proposed hybrid algorithms to the generated 3D airspace to produce the risk-cost-effective path. Lastly, we conduct simulations and statistical analysis to test how well the proposed risk assessment model and algorithms can be generalized to other urban patterns. 

## _5.1.  Case study of risk cost assessment model_ 

A typical metropolitan area (6km×6km) in Singapore is selected for the modelling of risk aware airspace, and the allowable altitude in this study is chosen as 120 meters (400 feet) above the ground. The size of each air block is 100m×100m×30m. The selected metropolitan area has dense high-rise buildings, shopping centers, city squares, residential areas with dense population, parks, etc., which are representative for modern mega cities. The selected environment has two administrative districts, and the average population densities are 8.358×10[3] and 7.219×10[3] (people/km[2] ) (WorldoMeter 2021). The average traffic density in the given area is obtained as 7.12×10[3] (vehicle/km[2] ) (SG Land Transport Authority 2021). Based on the average population and vehicle densities, we can estimate the fine population density distribution using Eq. (10) and traffic density distribution using Eq. (11). Obtained population and traffic distribution results are demonstrated in Fig. 8. 


![](1_survey/papers/md/Pang2021Third_figs/Pang2021Third.pdf-0014-04.png)



![](1_survey/papers/md/Pang2021Third_figs/Pang2021Third.pdf-0014-05.png)



![](1_survey/papers/md/Pang2021Third_figs/Pang2021Third.pdf-0014-06.png)


**----- Start of picture text -----**<br>
(a) Population density distribution                                        (b) Traffic density distribution<br>**----- End of picture text -----**<br>


**Fig. 8.** Distribution of population density and traffic density in selected urban environments. 

In this case study, the UAV is selected as one of the most commonly used drones (DJI Phantom 4). The weight is 1.38kg, and the crash probability 𝑃'$()* is 6.04×10[-5] per flight hour (Shaokun 2018). The explored area of UAV impacts the ground is 𝑆*+, = 0.0188 m[2] and the drag coefficient is 𝑅7 = 0.3 (Koh et al. 2018). The number of casualties caused by average traffic accident is 𝑅-F= 0.27 (Budget Direct Insurance 2021). For the integrated risk cost model, the weight factors of fatality risk, property damage and societal impact are given as 𝛼0 = 0.5, 𝛼5 = 0.25 and 𝛼^ = 0.25, respectively (see Eq. (19)). The fatality risk cost is given a high weight with 50% of the total weight, while the property damage cost and societal impact cost are given the same weight with 25% each in this study. Based on the obtained data, the total integrated risk cost of each flight layer is computed and demonstrated in Fig. 9. 


![](1_survey/papers/md/Pang2021Third_figs/Pang2021Third.pdf-0014-09.png)



![](1_survey/papers/md/Pang2021Third_figs/Pang2021Third.pdf-0014-10.png)



![](1_survey/papers/md/Pang2021Third_figs/Pang2021Third.pdf-0014-11.png)



![](1_survey/papers/md/Pang2021Third_figs/Pang2021Third.pdf-0014-12.png)


(a)  Layer 1: h=30 m                (b)  Layer 2: h=60 m                  (c)  Layer 3: h=90 m               (d)  Layer 4: h=120 m **Fig. 9.** Risk cost mapping for different flight altitude. 

In Fig. 9(a), the altitude of the flight layer is 30 meters and the average risk cost of whole area is high.  The areas with high fatality risks are well identified in the map. For instance, the location (20, 55) on the map has the highest risk cost, as there are shopping streets, highway intersections, and dense population in real-world environments. Thus, the fatality risk and property damage risk in there are high, making the total risk cost high. In Layer 2 (Fig. 9(b)), with the increase of flight altitude, risk costs are significantly reduced for property damage and noise impact as denoted in Eq. (14) and Eq. (17), whereas the fatality risk cost increases 7.7% compared with the one in the Layer 1. 

In the third and fourth flight layers as demonstrated in Fig. 9(c) and Fig. 9(d), the flight altitude increases to 90 and 120 meters. The high-risk areas in these two layers are still clearly identified while the total risk cost has not changed much from Layer 3 to Layer 4 because of two reasons. For one thing, the fatality risk only slightly increases (4.09% from Layer 2 to Layer 3 and 2.66% from Layer 3 to Layer 4) after the altitude passing 60 meters, as the impact damage over such height is mostly the same, which is causing fatalities. For another, the influence of the societal impact exceeds the height threshold (40 meters in Eq. (17) and Fig. 5(b)) and contributes nothing to the risk cost, while the property damage cost is significantly small. The risk cost in Layer 3 and Layer 4 are therefore significantly small while with high risk areas being clearly identified. 

## _5.2.  Risk-based path planning analysis_ 

With the risk-aware 3D airspace map, the risk-based path planning is conducted using EDA-RA* and EDA-FRA* algorithms. For comparison, Dijkstra and ACO algorithms are employed in the same environments. What is more, we investigate the impact of different risk types on the risk-based path planning and safe UAV operation. 

## _A. 3D risk-based path planning in real-world environment_ 

In general, the produced 3D risk-cost-effective paths are able to avoid obstacles and high-risk areas identified by our proposed risk assessment model. The results of 3D view with risk map, without risk map and top view are presented in Fig. 10(a), Fig. 10(b) and Fig. 10(c).  Observed from 3D view, the drone flight height for most of the time is 120 meters, which is the top layer of the modelled environments. Flying at such height significantly reduced the property damage risk and noise impact cost, and the fatality cost can also be reduced by avoiding high population density and vehicle density areas such as locations (10, 12), (40, 40) and (42, 39) shown in the top view. 


![](1_survey/papers/md/Pang2021Third_figs/Pang2021Third.pdf-0015-06.png)



![](1_survey/papers/md/Pang2021Third_figs/Pang2021Third.pdf-0015-07.png)



![](1_survey/papers/md/Pang2021Third_figs/Pang2021Third.pdf-0015-08.png)


(a)  3D view                                          (b)  3D view without risk map                               (c)  Top view 


![](1_survey/papers/md/Pang2021Third_figs/Pang2021Third.pdf-0015-10.png)


**----- Start of picture text -----**<br>
Fig. 10.   Results of 3D risk-based path planning in real-world environments.<br>**----- End of picture text -----**<br>


In real-world environment, these identified high risk locations are shopping street, hospital, school or highway conjunctions, where the population density and vehicle density are significantly higher than the rest of the areas. Being able to quantitively identify high risk areas using our proposed model facilitates the risk management of low altitude urban airspace and risk-based path planning. Which subsequently enables safe UAV operations in metropolitan environments. 

The path planning results of four algorithms are obtained and presented in Fig. 11 and 

Table **1** . Compared with Dijkstra algorithm, EDA-FRA* produced path has 2.06% shorter distance while using a mere of 3.05% computational time, whereas the risk cost of the path is 4.58% greater than the Dijkstra one. Followed by the path produced by ACO with 1.51% more cost and 1.22% longer distance. Its computational time is, however, dramatically greater than all of other three algorithms, with 785.98% greater than Dijkstra method. For EDA-RA* algorithm, its performance makes a good trade-off between risk cost, path distance and computational time. 


![](1_survey/papers/md/Pang2021Third_figs/Pang2021Third.pdf-0016-00.png)



![](1_survey/papers/md/Pang2021Third_figs/Pang2021Third.pdf-0016-01.png)



![](1_survey/papers/md/Pang2021Third_figs/Pang2021Third.pdf-0016-02.png)


**Fig. 11.** Comparison results of four path planning algorithms. 

**Table 1** 

Detailed performance results of the four path planning algorithms. 

|**Performance\**<br>**Indicators**|**Computational results**<br>**Performance ratio compared with**<br>**Dijkstra method**|
|---|---|
||Dijkstra<br>ACO<br>EDA-RA*<br>EDA-FRA*<br>ACO<br>EDA-RA*<br>EDA-FRA*|
|Risk cost index<br>Distance (km)<br>Computation time (s)|1102.60<br>1119.32<br>1126.26<br>1153.07<br>101.51%<br>102.14%<br>104.58%<br>9.73<br>9.85<br>10.11<br>9.53<br>101.22%<br>103.94%<br>97.94%<br>3806.21<br>29916.15<br>984.87<br>116.22<br>785.98%<br>25.88%<br>3.05%|



## _B. Impact of different risk types on risk-based path planning_ 

In order to demonstrate the impact of different risk types on safe UAV operations, we conduct four groups of path planning simulation with risk-related variables controlled and all constrains applied (see Section 4.1). Four simulations are planned as: (1) Path1: without consider any risk; (2) Path2: only consider fatality risk; (3) Path3: consider fatality risk and property damage risk; (4) Path4: consider all three risks. The environment of the four simulations is the same, which is generated in Section 5.1. The EDA-FRA* algorithm performs well among the benchmark methods in terms of computational efficiency and effectiveness and is therefore applied for each of the four simulations. Obtained results are shown in Fig. 12 and Table 2. 

The Path1 goes from origin (1, 1, 1) to destination (60, 60, 4) with almost a straight line. This path avoids obstacles in positions like (30, 32) and (40, 40) shown in Fig. 12. However, it does not avoid high population density and vehicle density areas where the risk costs are high, resulting in the total risk cost of Path1 is the highest among all paths, with risk cost index of 1698.25 (see Table 2). Whereas the distance of the path is the shortest as it goes almost straightly. For Path2 the fatality risk is taken into account. This path successfully avoids the high population density areas (10, 12), (40, 45), (42, 15) shown in Fig. 8(a) and high vehicle density areas (8, 20), (45, 10) and (55, 40) shown in Fig. 8(b). As the fatality risk cost has a high proportion in the total risk cost model, avoiding high fatality risk areas makes a significant reduction (23.68%) of risk cost for Path2, compared with Path1. While the distance of Path2 is the greatest among the four paths, as more distance is travelled to avoid high risk areas. For Path3 the fatality risk and property damage risk are both considered. The produced path3 not only averts the high fatality risk areas, but avoid dense highrise building areas like (20, 20) and (30, 30) shown in Fig. 4(a), which Path1 and Path2 fail to do so (see Fig. 12). By adding property damage risk into the model, the Path3 is able to additionally avoid dense building areas, thus the risk cost of its path further drops by 5.94% compared with Path2. For Path4, it takes all three risk types into consideration. However, the most part of the path is at flight level 120 meters where the property damage and noise impact have tiny contributions to the risk cost. So, the risk cost of Path4 has no remarkable reduction (a mere of 2.48%) compared with Path3. 


![](1_survey/papers/md/Pang2021Third_figs/Pang2021Third.pdf-0017-00.png)


**Fig. 12.** Top view of produced paths for considering four different risk types. 

Overall, the fatality risk is identified as the primary factor in the risk assessment model and in the subsequent costeffective path planning, followed by property damage risk and noise impact cost. With more risk types getting considered, the more accurate risk aware 3D airspace map will be generated to produce lower risk cost path for safe UAV operations. While the distance of the produced path will be greater as the UAV needs more movements to avoid obstacles and high-risk areas. 

**Table 2** 

Results of the four produced paths considering different risk types. 

|**Performance\**<br>**Indicators**<br>Risk cost index<br>Travel Distance (km)|**Computational results**<br>**Performance ratio compared with Path1**|
|---|---|
||Path1<br>Path2<br>Path3<br>Path4<br>Path1<br>Path2<br>Path3<br>Path4|
||1698.25<br>1296.02<br>1195.18<br>1153.10<br>100.00%<br>76.32%<br>70.38%<br>67.90%<br>8.35<br>10.22<br>10.01<br>9.53<br>100.00%<br>122.32%<br>119.88%<br>114.08%|



## _5.3.  External validity of the risk assessment model_ 

To validate how well the proposed risk assessment model can be generalized to other urban patterns in mitigating third-party risk, we conduct external validity and randomly generate the parameters of 100 different urban patterns. We take population density from the integer range of [5, 25] ×10[3 ] (people/km[2] ), which covers the most densely populated cities worldwide (Wikipedia 2021). The average traffic density is given as same as above in Section 5.1 _5.1_ . The building height distribution of all generated patterns follows log-normal distribution. The scope of the validation environment is 6km×6km×120m with size of each unit is 100m×100m×30m. Using the risk assessment model in Section 3 with the generated parameters, we obtain the risk cost value in each airspace unit for 100 independent simulation environments. 

Each simulation has been independently conducted standard Dijkstra and risk-based Dijkstra via MATLAB software on a desktop equipped with an InteI E5-2680 @2.4Ghz CPU. The standard Dijkstra algorithm is performed in a normal map without considering third-party risk, while risk-based Dijkstra is conducted based on the risk map generated by our assessment model. Comparison is made between these two ways to see how much percentage of risk being mitigated by using risk-based method. The simulation starts from origin (1, 1, 1) to destination (60, 60, 4) to produce the risk-cost-effective path. Total risk cost for each simulation is obtained and presented in Fig. 13. 

In the 100 generated samples (urban patterns), the mitigated risk of flight path in each individual urban pattern is greatly less than the unmitigated one produced by standard Dijkstra. To test how effective the risk can be mitigated for the population (all types of urban patterns), we conduct statistical analysis to find a 95% confidence interval for the percentage of the risk being mitigated by. 


![](1_survey/papers/md/Pang2021Third_figs/Pang2021Third.pdf-0018-00.png)


**Fig. 13.** Risk being mitigated by using risk-based method. 

In this case, we have two sample groups and they are mitigated risk group (Group 1) and unmitigated risk group (Group 2). Each group has 100 samples (total risk cost index). As the sample sizes are large (𝑛0>30 and 𝑛5>>30), we use normal distribution the compute the confidence interval. The sample means (𝑥̅0 and 𝑥̅5) and sample variances 5 5 (𝑠0 and 𝑠5 ) of the two groups are computed and presented in Table 3. The population means of Group 1 and Group 2 are presented as 𝜇0 and  𝜇5. The confidence interval of risk mitigation effect can be then described as (𝜇5 −𝜇0)/𝑥̅5, where the interval of 𝜇5 −𝜇0 can be computed as (𝑥̅5 −𝑥̅0) ± 𝑍u/5‹𝑠05/𝑛0 + 𝑠55/𝑛5. The obtained result shows that a 95% confidence interval for risk mitigation effect is (𝜇5 −𝜇0)/𝑥̅5 ∈ [0.4264, 0.4415]. Which means that our proposed risk assessment model is effective for all types of urban patterns, and the average total risk can be mitigated by [42.64%, 44.15%] at 95% confidence level. 

**Table 3** 

Statistical analysis parameters of risk mitigation effect. 

|Groups|Mitigated risk(Group1)|Unmitigated risk(Group2)|
|---|---|---|
|Sample size|𝑛!=100|𝑛'=100|
|Sample mean|𝑥!=18584|𝑥'=32831|
|Sample variance|𝑠!<br>'=1594657|𝑠'<br>'=4859067|



## _5.4.  Reliability validation of the proposed algorithms_ 

Above we validated that the proposed risk assessment model is effective to capture risk features and mitigate total risks in all types of urban patterns. To test the reliability of proposed risk-based algorithms in solving path planning problems with different urban patterns and risk maps, we perform the simulations based on the urban patterns and risk cost value generated in the Section 5.3. the comparison involves three algorithms of risk-based Dijkstra, EDA-RA* and EDA-FRA*. Total risk cost and total distance of the produced path, as well as computational time are obtained and presented in Fig. 14 and Table 4. 

In the overall 100 simulations, the Dijkstra algorithm performs the best in terms of the total risk cost of the produced path, followed by EDA-RA* and EDA-FRA* with average performance rate of 102.76% and 105.47%, respectively. It means that the average total risk cost of the path produced by EDA-RA* and EDA-FRA* algorithms are 2.76% and 5.47% greater than that of the Dijkstra method. In contrast, the EDA-FRA* algorithm provides the best performance in terms of average total distance and average computational time, with 0.4% shorter in total distance and a mere of 2.07% in computational time. Followed by EDA-RA* algorithm, it saves 0.17% travel distance while spends 24.12% computational time compared with Dijkstra method. Another interesting trend can be observed is that total risk cost (Fig. 14 (a)) and total travel distance (Fig. 14 (b)) are two variables with opposite trend. One variable increases resulting in decrease of the other (e.g. the 7[th] , 13[th ] and 37[th] simulations). Which implies that to achieve a low risk cost path in risk-based environment, UAV always has to travel more distance to avoid high risk areas. 

Deviation analysis of the 100 simulations with randomly generated risk environments shows that the proposed EDA-RA* and EDA-FRA* algorithms has good robustness, with a mere of 1.29% and 2.54% standard deviation in computing total risk cost, while 2.18% and 4.29% for total distance (Table 4). The results present that the proposed algorithms are reliable to solve complex risk-based 3D path planning problems for different environments. 


![](1_survey/papers/md/Pang2021Third_figs/Pang2021Third.pdf-0019-00.png)


**Fig. 14.** Reliability testing results for proposed algorithms in terms of total risk cost and total flight distance. 

In summary, the EDA-FRA* is the fastest algorithm in terms of computation and it is much faster than the other two algorithms. While it also has a good performance in obtaining the quality of solution. Its performance is made possible by the heuristic information scheme and the algorithm’s structure (see Algorithm 3) without need to call A* function in every loop. The EDA-FRA* algorithm can be therefore used for more time-sensitive risk-based path planning missions. The EDA-RA* algorithm performs well in both quality of solution and computational efficiency, so it can be applied to the trade-off case. As an exact method, Dijkstra can be employed to produce the minimum risk cost path if computational time is not sensitive. 

**Table 4** 

Reliability testing results of the proposed algorithms with 100 independent simulations. 

|Performance\<br>Algorithms|Averagetotal riskcost<br>Averagetotaldistance (km)<br>Average<br>computational time<br>(s)<br>Average<br>percentage of<br>the time<br>Indicator ratio<br>Standard<br>Deviation<br>Indicator ratio<br>Standard<br>Deviation|
|---|---|
|Dijkstra<br>EDA-RA*<br>EDA-FRA*|100.00%<br>0.00%<br>100.00%<br>0.00%<br>4120.35<br>100.00%<br>102.76%<br>1.29%<br>99.83%<br>2.18%<br>993.68<br>24.12%<br>105.47%<br>2.54%<br>99.60%<br>4.29%<br>85.24<br>2.07%|



## **6. Conclusions** 

In this article, we investigated the third party risk assessment model and risk-based path planning problems for safe UAV operations in metropolitan environments. Main findings are concluded as follows. 

- (1) The proposed integrated risk assessment model is able to capture comprehensive risk types in urban environments including fatality risk, property damage risk and societal impact risk. The statistical analysis results show that the proposed model is effective for all types of urban patterns. The model enables quantitative risk assessment for urban airspace, which facilitates the risk aware airspace modelling and riskbased path planning. 

- (2) The introduced gravity model for population density and vehicle density estimation can identify high population density areas in a finer scale. Which means that the population density in one district will not be averagely treated but being identified with actual high-density areas while releasing low density areas for UAV operations. 

- (3) The developed hybrid 3D risk-based path planning algorithms outperform the existing methods in terms of solution quality and computational efficiency. The proposed hybrid EDA-FRA* algorithm performs best in computational time while it can still reach an average of 94% optimality of solution quality. Besides, the proposed EDA-RA* algorithm has better performance in making trade-off between solution quality and computational time. 

- (4) With more risk sources been considered, the total risk cost of produced path deceases. That is because the risk-based path planning algorithm will avoid areas with high risks, provided the risk types are considered 

and assessed. That further justifies the significancy of our proposed integrated risk assessment model, which is able to incorporate more risks with different types. 

The work of this article can be further improved from several aspects. For instance, a more accurate estimation model for population density could be developed if multisource data is available (Deville et al. 2014). Besides, collision risk between UAV and manned aircraft can also be incorporated into the integrated model for these environments where manned and unmanned aircraft are allowed to co-exist. 

## **Acknowledgement** 

The authors would like to thank Dr. Yu Wu and Dr. C.H. John Wang for their insightful suggestions on risk modelling and algorithm design. This research is supported by the Civil Aviation Authority of Singapore and the Nanyang Technological University, Singapore under their collaboration in the Air Traffic Management Research Institute. Any opinions, findings and conclusions or recommendations expressed in this material are those of the authors and do not reflect the views of the Civil Aviation Authority of Singapore. 

## **References** 

Alexander, W. Nathan, and Jeremiah Whelchel. 2019. “Flyover Noise of Multi-Rotor SUAS.” In _INTER-NOISE 2019 MADRID - 48th International Congress and Exhibition on Noise Control Engineering_ . 

Ang, Li, and Mark Hansen. 2019. “Clustering Based Approach to Single Drone Path Planning in Complex Urban Airspace.” https://cpb-use1.wpmucdn.com/blog.umd.edu/dist/9/604/files/2019/02/UAV_YEAR1_REPORT-23hozv7.pdf. Bauer, Michael W. 2019. “First Assessment of Community Noise for a Simulated Scenario of New Urban Air Traffic.” In _Proceedings of the 26th International Congress on Sound and Vibration, ICSV 2019_ , 1–8. 

Bell, Michael G.H. 2009. “Hyperstar: A Multi-Path Astar Algorithm for Risk Averse Vehicle Navigation.” _Transportation Research Part B: Methodological_ 43 (1): 97–107. https://doi.org/10.1016/j.trb.2008.05.010. 

Bertrand, S., N. Raballand, and F. Viguier. 2018. “Evaluating Ground Risk for Road Networks Induced by UAV Operations.” In _2018 International Conference on Unmanned Aircraft Systems, ICUAS 2018_ , 168–76. IEEE. https://doi.org/10.1109/ICUAS.2018.8453441. Bertrand, S., N. Raballand, F. Viguier, and F. Muller. 2017. “Ground Risk Assessment for Long-Range Inspection Missions of Railways by UAVs.” In _2017 International Conference on Unmanned Aircraft Systems, ICUAS 2017_ , 1343–51. https://doi.org/10.1109/ICUAS.2017.7991331. 

Breunig, Jeff, Joyce Forman, Shereef Sayed, Laurence Audenaerd, Art Branch, and Michael Hadjimichael. 2019. “Modeling Risk-Based Approach for Small Unmanned Aircraft Systems.” In _AUVSI XPONENTIAL 2019: All Things Unmanned_ , 1–23. Budget Direct Insurance. 2021. “Road Accident Statistics Singapore 2021.” Land Transport Authority. 2021. 

https://www.budgetdirect.com.sg/car-insurance/research/road-accident-statistics-in-singapore#:~:text=road fatality rate.-,Singapore’s road fatality rate of 2.73 per 100%2C000 citizens is,100%2C000 cars is far lower. Bulusu, Vishwanath, Valentin Polishchuk, Raja Sengupta, and Leonid Sedov. 2017. “Capacity Estimation for Low Altitude Airspace.” In _17th AIAA Aviation Technology, Integration, and Operations Conference_ . https://doi.org/10.2514/6.2017-4266. 

Cho, Jungwoo, and Yoonjin Yoon. 2019. “Extraction and Interpretation of Geometrical and Topological Properties of Urban Airspace for UAS Operations.” In _13th USA/Europe Air Traffic Management Research and Development Seminar 2019_ . Chung, Jen Jen, Andrew J. Smith, Ryan Skeele, and Geoffrey A. Hollinger. 2019. “Risk-Aware Graph Search with Dynamic Edge Cost Discovery.” _International Journal of Robotics Research_ 38 (2–3): 182–95. https://doi.org/10.1177/0278364918781009. Clothier, Reece A., Brendan P. Williams, and Kelly J. Hayhurst. 2018. “Modelling the Risks Remotely Piloted Aircraft Pose to People on the Ground.” _Safety Science_ 101 (December 2016): 33–47. https://doi.org/10.1016/j.ssci.2017.08.008. Dalamagkidis, Konstantinos, Kimon P. Valavanis, and Les A. Piegl. 2008. “Evaluating the Risk of Unmanned Aircraft Ground Impacts.” In _16th Mediterranean Conference on Control and Automation_ , 709–16. https://doi.org/10.1109/MED.2008.4602249. Deville, Pierre, Catherine Linard, Samuel Martin, Marius Gilbert, Forrest R. Stevens, Andrea E. Gaughan, Vincent D. Blondel, and Andrew J. Tatem. 2014. “Dynamic Population Mapping Using Mobile Phone Data.” In _Proceedings of the National Academy of Sciences of the United States of America_ , 111:15888–93. https://doi.org/10.1073/pnas.1408439111. Dijkstra, Edsger W. 1959. “A Note on Two Problems in Connexion with Graphs.” _Numerische Mathematik_ 1 (1): 269–71. http://www.bioinfo.org.cn/~dbu/AlgorithmCourses/Lectures/Dijkstra1959.pdf. Federal Aviation Administration. 2020. “Fact Sheet – Small Unmanned Aircraft Systems (UAS) Regulations (Part 107).” U.S Department of Transportation. 2020. https://www.faa.gov/news/fact_sheets/news_story.cfm?newsId=22615. Feyzabadi, Seyedshams, and Stefano Carpin. 2014. “Risk-Aware Path Planning Using Hirerachical Constrained Markov Decision Processes.” In _IEEE International Conference on Automation Science and Engineering_ , 2014-Janua:297–303. IEEE. https://doi.org/10.1109/CoASE.2014.6899341. Filippis, Luca De, Giorgio Guglieri, and Fulvia Quagliotti. 2011. “A Minimum Risk Approach for Path Planning of UAVs.” _Journal of Intelligent and Robotic Systems: Theory and Applications_ 61 (1–4): 203–19. https://doi.org/10.1007/s10846-010-9493-9. Ghasri, Milad, and Mojtaba Maghrebi. 2021. “Factors Affecting Unmanned Aerial Vehicles’ Safety: A Post-Occurrence Exploratory Data Analysis of Drones’ Accidents and Incidents in Australia.” _Safety Science_ 139: 105273. https://doi.org/10.1016/j.ssci.2021.105273. Gonçalves, P., J. Sobral, and L. A. Ferreira. 2017. “Unmanned Aerial Vehicle Safety Assessment Modelling through Petri Nets.” _Reliability Engineering and System Safety_ 167 (June): 383–93. https://doi.org/10.1016/j.ress.2017.06.021. Ha, Quang Minh, Yves Deville, Quang Dung Pham, and Minh Hoàng Hà. 2018. “On the Min-Cost Traveling Salesman Problem with Drone.” _Transportation Research Part C: Emerging Technologies_ 86 (November 2017): 597–621. https://doi.org/10.1016/j.trc.2017.11.015. Hu, Xinting, Bizhao Pang, Fuqing Dai, and Kin Huat Low. 2020. “Risk Assessment Model for UAV Cost-Effective Path Planning in Urban Environments.” _IEEE Access_ 8: 150162–73. https://doi.org/10.1109/ACCESS.2020.3016118. Jiang, Chengpeng, Henk A. Blom, and Alexei Sharpanskykh. 2020. “Third Party Risk Indicators and Their Use in Safety Regulations for UAS Operations.” In _AIAA AVIATION 2020 FORUM, 2020_ , 1–15. AIAA. https://doi.org/10.2514/6.2020-2901. Kim, Namwoo, and Yoonjin Yoon. 2019. “Cooperative SUAV Collision Avoidance Based on Satisficing Theory.” _International Journal of_ 

_Aeronautical and Space Sciences_ 20 (4): 978–86. https://doi.org/10.1007/s42405-019-00183-4. 

Kim, Sang Hyun. 2020. “Third-Party Risk Analysis of Small Unmanned Aircraft Systems Operations.” _Journal of Aerospace Information Systems_ 17 (1): 24–35. https://doi.org/10.2514/1.I010763. Kirtner, Jody, and Harry Anderson. 2008. “The Application of Land Use / Land Cover (Clutter) Data to Wireless Communication System Design.” _Technology White Paper_ . https://proceedings.esri.com/library/userconf/proc98/PROCEED/TO550/PAP525/P525.HTM. Koh, Choon Hian, K. H. Low, Lei Li, Yi Zhao, Chao Deng, Shi Kun Tan, Yuliang Chen, Bing Cheng Yeap, and Xin Li. 2018. “Weight Threshold Estimation of Falling UAVs (Unmanned Aerial Vehicles) Based on Impact Energy.” _Transportation Research Part C: Emerging Technologies_ 93 (April): 228–55. https://doi.org/10.1016/j.trc.2018.04.021. 

Levasseur, Baptiste, Sylvain Bertrand, Nicolas Raballand, Flavien Viguier, and Gregoire Goussu. 2019. “Accurate Ground Impact Footprints and Probabilistic Maps for Risk Analysis of UAV Missions.” In _IEEE Aerospace Conference Proceedings_ , 2019-March:1–10. https://doi.org/10.1109/AERO.2019.8741718. 

Lin Tan, Lynn Kai, Beng Chong Lim, Guihyun Park, Kin Huat Low, and Victor Chuan Seng Yeo. 2021. “Public Acceptance of Drone Applications in a Highly Urbanized Environment.” _Technology in Society_ 64 (November 2020): 101462. https://doi.org/10.1016/j.techsoc.2020.101462. 

Liu, Chang, Shiwu Yang, Yong Cui, and Yixuan Yang. 2020. “An Improved Risk Assessment Method Based on a Comprehensive Weighting Algorithm in Railway Signaling Safety Analysis.” _Safety Science_ 128 (February): 104768. https://doi.org/10.1016/j.ssci.2020.104768. Melnyk, Richard, Daniel Schrage, Vitali Volovoi, and Hernando Jimenez. 2014. “A Third-Party Casualty Risk Model for Unmanned Aircraft System Operations.” _Reliability Engineering and System Safety_ 124: 105–16. https://doi.org/10.1016/j.ress.2013.11.016. Mitici, Mihaela, and Henk A.P. Blom. 2019. “Mathematical Models for Air Traffic Conflict and Collision Probability Estimation.” _IEEE Transactions on Intelligent Transportation Systems_ 20 (3): 1052–68. https://doi.org/10.1109/TITS.2018.2839344. Narkus-Kramer, Marc. 2017. “Future Demand and Benefits for Small - Autonomous Unmanned Aerial Systems Package Delivery.” In _AIAA AVIATION Forum_ , 1–7. Denver, Colorado: AIAA. https://doi.org/10.2514/6.2017-4103. NASA. 2020. “ADVANCED AIR MOBILITY: WHAT IS AAM?” https://doi.org/https://www.nasa.gov/sites/default/files/atoms/files/what-isaam-student-guide_0.pdf. Pang, Bizhao, Wei Dai, Xinting Hu, Fuqing Dai, and Kin Huat Low. 2021. “Multiple Air Route Crossing Waypoints Optimization via Artificial Potential Field Method.” _Chinese Journal of Aeronautics_ 34 (4). https://doi.org/10.1016/j.cja.2020.10.008. Pang, Bizhao, Ee Meng Ng, and Kin Huat Low. 2020. “UAV Trajectory Estimation and Deviation Analysis for Contingency Management in Urban Environments.” In _AIAA AVIATION 2020 FORUM_ , 1–10. AIAA. https://doi.org/10.2514/6.2020-2919. Pang, Bizhao, Qingyu Tan, Thu Ra, and Kin Huat Low. 2020. “A Risk-Based UAS Traffic Network Model for Adaptive Urban Airspace Management.” In _AIAA AVIATION 2020 FORUM_ , 1–9. AIAA. https://doi.org/10.2514/6.2020-2900. Primatesta, Stefano, Giorgio Guglieri, and Alessandro Rizzo. 2019. “A Risk-Aware Path Planning Strategy for UAVs in Urban Environments.” _Journal of Intelligent and Robotic Systems: Theory and Applications_ 95 (2): 629–43. https://doi.org/10.1007/s10846-018-0924-3. Primatesta, Stefano, Alessandro Rizzo, and Anders la Cour-Harbo. 2020. “Ground Risk Map for Unmanned Aircraft in Urban Environments.” _Journal of Intelligent and Robotic Systems: Theory and Applications_ 97 (3–4): 489–509. https://doi.org/10.1007/s10846-019-01015-z. Rappaport, Jordan. 2008. “Consumption Amenities and City Population Density.” _Regional Science and Urban Economics_ 38 (6): 533–52. https://doi.org/10.1016/j.regsciurbeco.2008.02.001. Ren, Xinhui, and Caixia Cheng. 2020. “Model of Third-Party Risk Index for Unmanned Aerial Vehicle Delivery in Urban Environment.” _Sustainability_ 12 (20): 8318. https://doi.org/10.3390/su12208318. Rudnick-Cohen, Eliot, Shapour Azarm, and Jeffrey W. Herrmann. 2019. “Planning Unmanned Aerial System (UAS) Takeoff Trajectories to Minimize Third-Party Risk.” In _2019 International Conference on Unmanned Aircraft Systems, ICUAS 2019_ , 1306–15. IEEE. https://doi.org/10.1109/ICUAS.2019.8798149. Rudnick-Cohen, Eliot, Jeffrey W. Herrmann, and Shapour Azarm. 2016. “Risk-Based Path Planning Optimization Methods for Unmanned Aerial Vehicles over Inhabited Areas.” _Journal of Computing and Information Science in Engineering_ 16 (2): 1–7. https://doi.org/10.1115/1.4033235. SG Land Transport Authority. 2021. “Singapore Road Traffic Conditions during Peak Hours.” Singapore Open Data Licence. 2021. https://data.gov.sg/dataset/road-traffic-conditions?view_id=c4da8178-f136-4496-9b55-6426854d829e&resource_id=f2451c6c-14694d8b-8c4f-a4aab9de40e3. 

Shaokun, Yan. 2018. “UAV Operational Risk Assessment Model,” 38. 

Silva Arantes, Jesimar Da, Márcio Da Silva Arantes, Claudio Fabiano Motta Toledo, Onofre Trindade Júnior, and Brian Charles Williams. 2017. “Heuristic and Genetic Algorithm Approaches for UAV Path Planning under Critical Situation.” _International Journal on Artificial Intelligence Tools_ 26 (1): 1–30. https://doi.org/10.1142/S0218213017600089. 

Torija, Antonio J., Zhengguang Li, and Rod H. Self. 2020. “Effects of a Hovering Unmanned Aerial Vehicle on Urban Soundscapes Perception.” _Transportation Research Part D: Transport and Environment_ 78: 102195. https://doi.org/10.1016/j.trd.2019.11.024. Usui, Hiroyuki. 2019. “Statistical Distribution of Building Lot Depth: Theoretical and Empirical Investigation of Downtown Districts in Tokyo.” _Environment and Planning B: Urban Analytics and City Science_ 46 (8): 1499–1516. https://doi.org/10.1177/2399808319840366. Vascik, Parker D., and R. John Hansman. 2018. “Scaling Constraints for Urban Air Mobility Operations: Air Traffic Control, Ground Infrastructure, and Noise.” In _2018 Aviation Technology, Integration, and Operations Conference_ , 1–25. https://doi.org/10.2514/6.20183849. 

Vascik, Parker D., and R John Hansman. 2019. “Assessing Integration Between Emerging and Conventional Operations in Urban Airspace.” In _AIAA AVIATION Forum_ , 1–24. https://doi.org/10.2514/6.2019-3125. Votion, Johnathan, and Yongcan Cao. 2019. “Diversity-Based Cooperative Multivehicle Path Planning for Risk Management in Costmap Environments.” _IEEE Transactions on Industrial Electronics_ 66 (8): 6117–27. https://doi.org/10.1109/TIE.2018.2874587. Wai, Rong Jong, and Alex S. Prasetia. 2019. “Adaptive Neural Network Control and Optimal Path Planning of UAV Surveillance System with Energy Consumption Prediction.” _IEEE Access_ 7: 126137–53. https://doi.org/10.1109/ACCESS.2019.2938273. Wang, C. H.John, Shi Kun Tan, and Kin Huat Low. 2019. “Collision Risk Management for Non-Cooperative UAS Traffic in Airport-Restricted Airspace with Alert Zones Based on Probabilistic Conflict Map.” _Transportation Research Part C: Emerging Technologies_ 109 (July): 19–39. https://doi.org/10.1016/j.trc.2019.09.017. 

Wikipedia. 2021. “List of Cities Proper by Population Density.” 2021. 

https://en.wikipedia.org/wiki/List_of_cities_proper_by_population_density. 

WorldoMeter. 2021. “The Population Density in Singapore.” Www.Worldometers.Info. 2021. https://www.worldometers.info/world- 

population/singapore-population/#:~:text=Singapore ranks number 114 in,21%2C646 people per mi2).&text=The median age in Singapore is 42.2 years. 

- Wu, Yu. 2021. “A Survey on Population-Based Meta-Heuristic Algorithms for Motion Planning of Aircraft.” _Swarm and Evolutionary Computation_ 62 (March 2020): 100844. https://doi.org/10.1016/j.swevo.2021.100844. 

- Wu, Yu, Kin Huat Low, Bizhao Pang, and Qingyu Tan. 2021. “Swarm-Based 4D Path Planning for Drone Operations in Urban Environments.” _IEEE Transactions on Vehicular Technology_ 9545 (c). https://doi.org/10.1109/TVT.2021.3093318. 

- Wu, Yu, Shaobo Wu, and Xinting Hu. 2020. “Cooperative Path Planning of UAVs & UGVs for a Persistent Surveillance Task in Urban Environments.” _IEEE Internet of Things Journal_ , no. c: 1–1. https://doi.org/10.1109/JIOT.2020.3030240. 

- Yao, Yao, Xiaoping Liu, Xia Li, Jinbao Zhang, Zhaotang Liang, Ke Mai, and Yatao Zhang. 2017. “Mapping Fine-Scale Population Distributions at the Building Level by Integrating Multisource Geospatial Big Data.” _International Journal of Geographical Information Science_ 31 (6): 1220–44. https://doi.org/10.1080/13658816.2017.1290252. 

- Zhu, Xiaoning, Rui Yan, Rui Peng, and Zhongxin Zhang. 2020. “Optimal Routing, Loading and Aborting of UAVs Executing Both Visiting Tasks and Transportation Tasks.” _Reliability Engineering and System Safety_ 204 (March): 107132. https://doi.org/10.1016/j.ress.2020.107132. 

- Zou, Yiyuan, Honghai Zhang, Gang Zhong, Hao Liu, and Dikun Feng. 2021. “Collision Probability Estimation for Small Unmanned Aircraft Systems.” _Reliability Engineering and System Safety_ 213 (July 2020): 107619. https://doi.org/10.1016/j.ress.2021.107619. 

