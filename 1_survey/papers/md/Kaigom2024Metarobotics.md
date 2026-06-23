---
citation_key: Kaigom2024Metarobotics
arxiv_id: 2404.00797
arxiv_url: "https://arxiv.org/abs/2404.00797"
title: "Metarobotics for Industry and Society: Vision, Technologies, and Opportunities"
authors_short: "Eric Guiffo Kaigom"
year: 2024
direction_tag: R_surveys
source: pymupdf4llm
converted_at: 2026-06-23T19:04:01Z
origin: ai+web
reviewed: false
---

1 

## Metarobotics for Industry and Society: Vision, Technologies, and Opportunities 

Eric Guiffo Kaigom 

_**Abstract**_ **—Metarobotics aims to combine next generation wireless communication, multi-sense immersion, and collective intelligence to provide a pervasive, itinerant, and non-invasive access and interaction with distant robotized applications. Industry and society are expected to benefit from these functionalities. For instance, robot programmers will no longer travel worldwide to plan and test robot motions, even collaboratively. Instead, they will have a personalized access to robots and their environments from anywhere, thus spending more time with family and friends. Students enrolled in robotics courses will be taught under authentic industrial conditions in real-time. This paper describes objectives of Metarobotics in society, industry, and in-between. It identifies and surveys technologies likely to enable their completion and provides an architecture to put forward the interplay of key components of Metarobotics. Potentials for self-determination, self-efficacy, and work-life-flexibility in robotics-related applications in Society 5.0, Industry 4.0, and Industry 5.0 are outlined.** 


![](1_survey/papers/md/Kaigom2024Metarobotics_figs/Kaigom2024Metarobotics.pdf-0001-05.png)


Fig. 1: Pervasive and itinerant HRC in a mobile workspace. 

_**Index Terms**_ **—Robotics, Digital Twins, Metaverse, Collective Intelligence, 6G, Holoportation, Industry 4.0** _/_ **5.0, Society 5.0** 

## I. INTRODUCTION 

Enhancing operational efficiency in personalized production through smart decentralized robotized automation that quickly adapts to varying market conditions is a key objective of the industry. Efforts toward this end have culminated in the _Industry 4.0_ vision [1], [2]. By contrast, improving the well-being and experience of workers on top of Machine-to-Machine (M2M) communication is at the heart of _Industry 5.0_ [3]. It instills a human-centered, intellectual, social, and ethical acumen into the industrial worklife that reaches out to a digital transformation- and service-driven comfort, resilience, and self-fulfillment of citizens as core pillars of _Society 5.0_ [4]. 

However, there is a widening gap between physical humanrobot-collaboration (HRC) restricted to factories or home settings and personal as well as professional expectations of citizens. The generation Z of workers born after 1997 is an example. New work practices preferred by this generation are driven by digitalization, smart and boundless mobility, along with interconnected decisions. Forbes mentions that _"...generation Z are spending more time in Metaverse-related scenarios and have a closer relationship with their online_ 

Eric Guiffo Kaigom is with the Faculty of Computer Science and Engineering, Frankfurt University of Applied Sciences, Nibelungenplatz 1, 60318 Frankfurt/Main, Germany. Contact: kaigom@fb2.fra-uas.de 

© 2024 IEEE. Personal use of this material is permitted. Permission from IEEE must be obtained for all other uses, in any current or future media, including reprinting/republishing this material for advertising or promotional purposes, creating new collective works, for resale or redistribution to servers or lists, or reuse of any copyrighted component of this work in other works. 

Published on IEEE Transactions on Industrial Informatics, Volume 20, Issue 4, April 2024, DOI: https://doi.org/10.1109/TII.2023.3337380 

_selves than any generation prior."_ [5]. Since such features and functionalities are barely integrated in HRC, societal ramifications and implications of the gap become apparent. 

An approach to fill in this gap is to take advantage of the increasing adoption of immersive interfaces, including virtual _/_ augmented reality (VR _/_ AR) glasses, by citizens. This can be supplemented with wireless data transfer beyond Ultra Reliable Low Latency Communication (b-URLLC), such as 6G, and collective intelligence based upon jointly reasoning cognitive Digital Twins (cogDTs) to constantly ensured HRC [6]. The seamless appearance, disappearance, and multi-modal interaction with cogDTs of physical robots and their environments spatially teleported (i.e., holoported) into physical locations, even in motion, enables a contextualized access and operation of robots available on demand anytime and anywhere (see figure 1). Citizens can leave usual living- and workspaces while collaboratively carrying out robotized applications from _wherever_ , as shown in the smart mobility layer of figure 2. 

This novel form of pervasive and itinerant HRC termed as pi-HRC or _π_ -HRC enables flexible, mobile, and sustainable workspaces, while strengthening inclusion and resilience. Besides the reduction of the carbon footprint, and thus the ecological impact of workers free to work from any location, social distancing is self-regulated while maintaining interactions with distant robots and collaborators. In-house and outsourced employees work with customers on distant robotized applications as if they were all physically, technically, and socially copresent in the same remote place, even during pandemics. 

Since collaborators have their own six dimensional (6D) views of shared cogDTs with depth, color, and light perception, limitations of a fixed 2D video-streaming are overcome 

2 

|b-URLLC-driven<br>**Smart Mobility**<br>Layer<br>**Collaboration**<br>**Metaverse**<br>Layer<br>**Perception**<br>Layer<br>MEC-enabledCollective<br>andGenerative<br>IntelligenceDriven by<br>Privacy-aware and<br>Interoperating cogDTs<br>Indoor<br>Drones<br>Robots<br>Shared Robot States<br>HorizontalHeterogenous<br>Robotics-relatedPhysical<br>Ecosystems<br>CitizenImmersionand<br>Presencein Remote<br>Virtualized Workspaces<br>& Robotized Applications<br>Shop Floors<br>Households<br>Classrooms<br>Pervasive and Itinerant Robot Usage<br>Citizens<br>…<br>…<br>Holoported Robot on Track<br>Holop. Robot in City<br>(Humotics)<br>(Cotrusting)<br>**Multi‐Access Edge Computing (MEC)**<br>UAV<br>SLAM<br>Skillful Motions<br>Commands<br>Ergonomics<br>On-Board<br>AI/ML<br>Mesh-based<br>6D Streaming<br>Battery Status<br>Citizen Intentions<br>Comfort<br>Home<br>Workcell<br>Fig. 2: A three layer view on _Metarobotics_.|**KPI**|**5G**|**6G**|**Enabling Technologies**|
|---|---|---|---|---|
||Capacity|10MBps<br>_/m_2|103_×_<br>_/m_3|Visible light and Terahertz spectrum,<br>Satialmultilexinetc|
||Downlink|20GBps|50_×_|p pg, .<br>Non-Orthogonal Multiple Access (NOMA)<br>multiple-input multiple-output (MIMO), etc.|
||Uplink|10GBps|100_×_|Non-Orthogonal Multiple Access (NOMA)<br>multiple-input multiple-output (MIMO), etc.|
||Latency|1 ms|0_._1_×_|Multi-access Edge Computing (MEC), Caching,<br>Semantics-based individualization of communication,<br>Reinforcement Learning (RL) _/_ Deep Learning (DL)-based<br>allocation of resources, intelligent coding/decoding, etc.|
||Reliability|10_−_5|10_−_4_×_|Multi-hop, Intelligent Reconfgurable Surfaces (IRSs),<br>Edge AI, RL-based robustifcation|
||User<br>experience|50MBps<br>(2D)|200_×_<br>(3D)|MEC, Terahertz spectrum, NOMA, context awareness,<br>Semantics-based personalization of communication,<br>IRSs, Ambient Backscatter Communication (ABC), etc.|
||Mobility|500km/ h|2_×_|Space-Air-Underwater-Terrestrial Integrated Networks|
||Sensing<br>Localization|10 cm<br>(2D)|0_._1_×_<br>(3D)|Terahertz and mmWave spectrum,<br>SiGe BiCMOS, Bulk and PD-SOI CMOS, etc.|
|robotized applications. For instance, workers can remotely<br>alk around the same holoported workpiece to teach target<br>bot poses and therebyjointly specifygoalsThis accelerates|Energy/bit<br>Effciency|-|1 pJ/bit|Edge Computing, IRS, ABC, Energy Harvesting,<br>Simultaneous Wireless Information & Power Transfer,<br>Wireless Power Transfer (WPT), Network Functions<br>Virtualization (NFV), Software-Defned Networking (SDN),<br>Deep Reinforcement Learning-based effcient sleep/wakeup<br>dynamics, Optical Wireless Communication (OWC), etc.|



in robotized applications. For instance, workers can remotely walk around the same holoported workpiece to teach target robot poses and thereby jointly specify goals. This accelerates co-programming and facilitates socialization among workers despite distance. Also, the potential for decent and upskilling work conditions, especially under hazards, such as heat or smoke exposition in glass factories [7], are incentives for citizen scientists and professional researchers to contribute to a shared and evolving knowledge base that informs decisions empowering citizens in _π_ -HRC. The _"human touch"_ for robotized _"mass personalization"_ advocated in [8] becomes actionable _beyond_ industrial borders to reach out to humancentered society at large. This _**Metarobotics**_ can be realized in a way that is location-agnostic, globally knowledge-driven, trustworthy, uplifting for workers, and noble for citizens. 

TABLE I: 5G _/_ 6G comparison. Numerical KPIs from [9]. 

## III. RELATED WORK 

Enabling technologies behind _Humotics_ and _Cotrusting_ , including b-URLLC, Holoportation, cogDTs, and Multi-Access Edge Computing (MEC), have been surveyed so far either independently from each other or in a generic way [10]. By contrast, this work surveys these technologies while emphasizing on their combination shown in figures 2, 3, 5 and 6 to meet the goals of _Metarobotics_ introduced in section II. In _Humotics_ , for instance, b-URLLC is expected to achieve an unnoticeable transmission of holoported assets in terms of latency, throughput, and reliability from the edge to any remote location to propel actionable cogDTs, as pointed out in the MEC-layer of figures 5 and 6. Semantics, goal orientation, and online learning behind 6G are thus leveraged by _Metarobotics_ - based _π_ -HRC for less transmitted data, reduced energy consumption, and more bandwidth [9]. This contrasts with [11] that exploits 5G for HRC. In fact, limitations of 5G (see table I) might impede _π_ -HRC. Similarly, _Cotrusting_ harnesses MEC-enabled blockchained transactions to preserve privacy. 

## II. CONTRIBUTIONS 

_Metarobotics_ is introduced as a concept for the pervasive and itinerant interaction with distant robotized applications and their enrichment with collective intelligence. Emerging technologies toward this end are identified and a survey thereof is provided. Discussed functionalities align with goals pursued by Industry 4 _._ 0, Industry 5 _._ 0, and Society 5 _._ 0 by fostering 

- a human-centered mobility of robotics beyond industry and society, called _Humotics_ , in the top layer of figure 2. It transcends distance, perpetuates a flexible proximity between robots and citizens, and facilitates inclusion. Mobile workspaces and operational efficiency are likely to benefit from this agility to anticipate and adapt course of actions and enhance comfort in robotized applications. 

A few surveys focusing on Holoportation have pointed out the importance of multi-modal feedback to raise the Quality of Experience (QoE) of citizens. The sense of touch is mentioned in e.g. [12] and ISO/IEC 18039:2019. However, advantages of 6G networks for ultra-massive personal-level support are not considered. Further modalities, such as a thermal sensation and visual deformation feedback, were omitted in surveys. Yet, these sensations are crucial for robotized tasks and predictive maintenance (e.g., situation awareness related to heating in the glass industry), as well as social interactions (e.g., touching a coffee cup, handshaking), and thus included in this paper. 

- a collective trusted intelligence termed as _Cotrusting_ in the middle layer of figure 2. It goes beyond individual capabilities of citizens and robots. Their networked and interoperating cogDTs fed with industrial and societal data (see bottom layer in figure 2) seamlessly augment citizens with otherwise hidden information and knowledge that they transform into competitive advantages to sustainably achieve robotized tasks while preserving privacy. 

A challenge around multi-modal feedback in Holoportation is the synchronization of independent information channels. In this paper, a survey of recent advances in synchronization techniques for multi-modal transmissions is provided. Achieving multi-modal feedback also offers opportunities to technically and socially engage, for example, the generation Z in professional and personal robotized applications, following thereby core objectives of Industry 4.0 and Industry 5.0. 

The paper is structured as follows. Section III describes how Metarobotics extends related work. Core objectives of Metarobotics are introduced in section IV. Section V surveys technologies leveraged by Metarobotics and combined in its architecture to meet these objectives. Use cases populate the paper to exemplify the practicability of these technologies. Finally, section VI concludes the paper with further challenges. 

3 


![](1_survey/papers/md/Kaigom2024Metarobotics_figs/Kaigom2024Metarobotics.pdf-0003-01.png)


**----- Start of picture text -----**<br>
Metaverse Beyond<br>URLLC Personalized experience Shared knowledge<br>MEC<br>DT Volumetric and Multi-  Flexibility, Self-Efficacy Use Cases<br>Immersion In-Motionmodal Presence and Presence and Human-ImmersionVolumetric Location-Agnostic ImmersionVolumetric   Diversity, InclusionSymbiosis, Sustainability<br>Robot-Interaction<br> NeXt generation URLLC-based Holoportation  Society 5.0, Industry 5.0 ,<br> Semantics & Goal-Driven CommunicationFederated Perpetual Learning Interoperability Transfer Learning ,<br> Pervasiveness<br>LM Pre-trained FederatedFoundation Models Collective & Generative ImmersionVolumetric ImmersionVolumetric Intelligence  ItinerancyNon-Invasiveness<br>LM FFM LM Industry 4.0<br>Cross-Domain  Metaverse<br>Multimodal Data<br>Enablers Functionalities KPI and Values Applications<br>**----- End of picture text -----**<br>


Fig. 3: Enablers, Functionalities, Key Performance Indexes (KPI), and envisioned examples of use cases of _Metarobotics_ . 

A state-of-the-art review of human-centered HRC has been recently proposed in [13]. Beyond human interpretations in HRC and striving for human satisfaction in Society 5.0, the survey in this paper emphasizes on robot centricity. This contributes to symbiosis and shared autonomy [14] in _π_ -HRC. 

This paper conceptualizes the usage of b-URLLC-based and multi-sense Holoportation for _π_ -HRC that benefits citizens in industry, society, and in-between. It summarizes how _Metarobotics_ capitalizes on surveyed technologies in an architecture (see figure 5) for that. To the best of our knowledge, we are not aware of any previous work that provides such a recent integration of emerging technologies toward this end. 

## IV. METAROBOTICS 

## _A. Motivation_ 

_Metarobotics_ arises from the need to develop a technologymediated and human-centered framework that fosters selfdetermination, efficacy, and comfort in robotics-related applications. Self-determination conceptualizes motivation around three pillars which are competence, autonomy, and inclusion [15]. Hence, citizens can perceive and understand challenges through multiple modalities, define personal and professional goals, and freely design solutions under a transparent but holistic assistance of interconnected cogDTs. This assistance is provided in a uniform transition between society and industry that considers current contexts and elevates capabilities of citizens as well as incorporates global constraints and shared intelligence. Finally, efforts of empowered citizens materialize themselves in the completion of robotized tasks in remote areas. 

These objectives can be achieved in the top layer of figure 2 regardless of smart mobility modes of citizens. They are given access to virtualized applications and empowered with facts inferred in the middle layer using structured information on remote physical siblings of applications run in the bottom layer. Conversely, IoT devices and citizens return information on the mobile workspace (e.g., ambient lighting, battery status) and appreciations of the trustworthiness of inferred facts to enhance the believability of knowledge from the middle layer of the collaboration Metaverse. Here, the notion of collaboration is disentangled from usual restrictions to real humans. Collaboration agents encompass embodied avatars and cogDTs. They semantically interoperate and reason in the Metaverse with a 

depth and breadth of information gained across domains in the bottom layer in figure 2, along with privacy-preserving learning and attention skills that outperform the capabilities of single humans they augment in terms of e.g. uncertainty handling and informed decision support. CogDTs are loosely coupled with their physical surrogates (e.g., a robot) that they mirror, monitor, and control to achieve goals in the bottom layer. 

## _B. Definition_ 

_Metarobotics_ is a software-defined framework (SDF) that strives to enable a location-independent and continuous proximity as well as assisted interaction with robotized applications beyond traditional scopes and boundaries of society and industry (hence, the prefix "Meta-"). The softwarization enables a reconfigurable availability of applications across heterogeneous platforms, domains, and devices. Standardized interfaces and information models, together with a granular control of atomic (micro)services adapted on-demand [16], facilitate the development of scalable, differentiated, and multidisciplinary solutions. Remote robotized applications can be holoported into collaboration spaces of the Metaverse using e.g. mesh- or point cloud-based reconstructions and virtually projected onto existing or prospective environments without affecting the milieu. Hence, _Metarobotics_ will be non-invasive. In fact, cross-domain projections are digital and do not modify augmented physical environments (see figure 1). Each projection ubiquitously enriches the smart mobility of citizens with spatial contexts and global cogDT-supported information about robotized applications. Additionally, the projection functionality engages citizens because virtualized applications (including human partners, assets, and collaboration processes) can be _spatially_ (i.e., in 6D) up- or downscaled to comfortably and purposefully fit in various environments like a confined cabin of an electric train in motion. Finally, each projection is sustainable by design through b-URLLC driven development, as mentioned in figures 2 and 3 and emphasized in table I. 

Using b-URLLC to combine these three dimensions (i.e., human-centric collective creation, sharing, and consumption of robotics-related knowledge, smart mobility, remote and spatial access to robotized applications) in the layers of figure 2 distinguishes _Humotics_ from approaches that only support single means of transport and 2D interfaces (e.g., tablets). Since 

4 

_Metarobotics_ is comparatively characterized by an ultra-dense and heterogeneous mobility of citizens with an on-demand and reliable proximity to remote robotized applications, as pursued by _Humotics_ , it needs to accommodate requirements set to network capacity and energy budget (see table I). One approach to achieve this goal is to leverage non-orthogonal multiple access (NOMA), millimeter Wave (mmWave), and Terahertz (THz) channels propelled by a base station caching and an application-dependent selection of channels [17]. Channels for signal transmission of the downlink mentioned in table I are assumed to be adaptively selected as a function of e.g. the transmission rate requirement of the application (e.g., 1 Tbps for Holoportation is associated with a Terahertz channel) in _Metarobotics_ to enhance the spectral efficiency, still following [17]. Ultra-low latency, high data rates, and reliability of 6G mentioned in table I align with the Quality of Service (QoS) required by _Metarobotics_ to control the motion and force-sensitiveness of most robots in closed feedback loops. Previously mentioned QoS properties also contribute to a high-fidelity multi-modal sensory (e.g., tactile) feedback for e.g. kinesthetic guidance tasks in robotized applications. Furthermore, the QoE of citizens in terms of presence and immersion will benefit from the QoS in _Metarobotics_ . Presence encompasses engaging multi-modal interactions with virtualized environments in which applications take place while immersion reflects a sensation of being completely located inside holoported environments [18]. Localization in the Terahertz channel with multipath resolvability [19] is an essential feature of _Metarobotics_ for e.g. logistics use cases (see r.h.s of figure 3). Intelligent Reconfigurable Surfaces (IRSs) with known poses act as passive and adjustable base stations with low energy consumption [20] that are used for solid and compatible multipaths to localize assets like mobile robots in even harsh environments (e.g., blockages of line-of-sight) [21]. 

As a SDF, _Metarobotics_ further targets a QoE that reflects how a configurable level of autonomy and efficacy individualy culminates in satisfaction and comfort. For instance, the information overload on graphical user interfaces can be dynamically adapted to an inferred level of expertise using visual cues. In this respect, cogDTs can recommend actions to steer the course of interactions with virtualized applications toward successful task completions in the remote real environment. By contrast, conventional robotic hardware with generic interfaces (e.g., control panels) can hardly be modified at this level of reconfiguration and responsiveness. In _Metarobotics_ , emerging technologies are leveraged at consumer levels to provide a pervasive and itinerant interaction with remote robotized applications in society, industry, and in-between. Citizens are empowered with the capability to continuously customize the level of control authority _α ∈_ [0 _,_ 1] to shape the function 


![](1_survey/papers/md/Kaigom2024Metarobotics_figs/Kaigom2024Metarobotics.pdf-0004-03.png)


where _h_ arbitrates the autonomy level of the physical distant robot using the citizen input _uh_ and autonomous control _ua_ , as introduced in [14]. In _Metarobotics_ , however, _ua_ = _uDT_ , which is a cogDT-driven autonomous control. It is worth noting that this choice injects a holistic awareness of society 


![](1_survey/papers/md/Kaigom2024Metarobotics_figs/Kaigom2024Metarobotics.pdf-0004-05.png)


**----- Start of picture text -----**<br>
Combina-tion ofPolicies DistributedTraining<br>Reinforcement<br>MixtureExpertsof Bagging Learning AveragingModel<br>Domain#n+2 Stacking Ensemble Learning Collective Learning Federated Learning Voting<br>Domain#n+1 Weighting Boosting Selectionof<br>Snapshot cogDTs<br>Domain#n<br>Itinerancy<br>Pervasiveness<br>**----- End of picture text -----**<br>


Fig. 4: **L.h.s:** Intinerancy and pervasiveness in _Metarobotics_ . **R.h.s:** Three pillars of collective learning in _Metarobotics_ . 

and industry inferred by interoperating cogDTs in the behavior of the remote local robot. Such an arbitration is likely to lead to a Quality of Value (QoV) that transforms society and industry in terms of self-determination, self-efficacy, and comfort. 

## _C. Fostering Personal Self-Determination in Society_ 

An itinerant access to virtualized applications allows citizens to spatially self-project from anywhere (see l.h.s. of figure 4) to achieve personal objectives without being physically present where the robot carries out domestic tasks in reality. Senior citizens, for instance, can thereby be physically [22] and socially [23] assisted at home, in supermarkets, or airports. This can be done by tuning _α_ in equation (1) to compensate for a potential disability and preserve autonomy. For _α →_ 1, a remote family member, as an example, and the local senior fully influence the robot behavior. A key advantage is that the member can be located anywhere. The immersion is volumetric, i.e., gaze directions, gesture dimensions, and the emotions of the senior together with undesired collisions like accidentally knocking over a bottle (see r.h.s of figure 3) are better perceived than in 2D. A suitable arbitration of the autonomy of the prolonged member’ arm (i.e., physical robot) can also foster self-determination of the senior. Assisting cogDTs in the Metaverse layer in figure 2 act on top of the perception layer to automatically adapt the robot behavior to e.g. gaze-related [24] or speech-based [23] inferences of needs and intentions of the senior who thereby cogDT-driven ( _α →_ 0) indirectly commands the robot. Since robotic emotional intelligence for social assistance incorporates monitoring, expressing, and understanding emotions [23], which are in turn considerably impacted by cultural factors [25], [26], considering diversity for rich discriminative inferences using deployed AI _/_ ML models is important [27], [28]. To this end, Foundation Models broadly and globally pre-trained in the collaboration Metaverse can be specialized to downstream emotion detection tasks through transfer learning [29] (see figure 3). Local AI _/_ ML models (LMs) are trained on-premise using sensitive data of citizens and open IoT data to update public foundation models (FMs) without disclosing raw data via Federated Learning (FL). Scenarios Engineering is a methodology to develop FMs in the Metaverse [30]. Resulting Federated Foundation Models (FFM) [31] with relay mechanisms to support energy-limited devices [32] take advantage of edge AI for an intelligent (e.g., context- and resource-aware) and continuous access to applications from society to industry with human-centered values. 

5 

## _D. Supporting Professional Self-Efficacy in Industry_ 

Orthogonally, pervasiveness describes the capability of _Metarobotics_ to help robotized applications penetrate and aggregate different domains of society and industry (see l.h.s. of figure 4) as well as forge a collective and shared generative intelligence that accelerates value creation and uplifts workers (see l.h.s. of figure 3). For example, customers and their environments (e.g., a parcel) can be spatially virtualized using the drone technology and projected into industrial settings for robotized individualized construction, and conversely. In this regard, the collaboration Metaverse and mobile Holoportation in figure 2 are combined to connect geographically distributed stakeholders (e.g., customers, architects, mechanical engineers, project managers, etc.) from different disciplines around the joint employment of robots to realize an individual house. Embodied avatars and cogDTs are drivers of this undertaking. 

In volumetrically accessible [33] collaboration spaces of _Metarobotics_ , cogDTs are aggregated to support two of its core functionalities (see figure 3) namely itinerancy and pervasiveness (see l.h.s. of figure 4). CogDTs transparently infer contexts, states, and intentions of stakeholders by e.g. using parallelizable attention mechanisms of vision transformers [34] or learning context relations among domains for robust recognition tasks (e.g., classification, segmentation, detection) despite domain gaps [35]. Inference results are then used to adapt the type and scope of created spatial common sense knowledge to enhance the efficacy of workers to safely and comfortably execute tasks [36] during _itinerancy_ . Intersectoral knowledge is employed on the other side to support _pervasiveness_ . Outcomes of common sense reasoning of interconnected cogDTs finally help stakeholders make efficient decisions. 

In collaboration spaces for robotized construction, for example, geometric forms specified by designers are translated into Cartesian motions of the robot end-effector by engineers. A global network of interoperating cogDTs acts in the background as a parallel intelligence engine (PIE) to quickly optimize time scaling factors with which joint trajectories are executed with a minimized energy consumption and anticipate bottlenecks. Outcomes of the PIE augment stakeholders from anywhere to validate or reject how remote robotized processes semi-autonomously ( _α →_ 0 _._ 5) evolve and make informed supervisory decisions for task completion with substantially less resource usage, which increases the professional satisfaction. 

## _E. Work-Life-Flexibility between Industry and Society_ 

Giving workers more choice over locations in which they work as a strategy to engage them is a key objective of worklife-flexibility [37]. In Metarobotics, the smart mobility of citizens goes together with their remote multi-modal presence when it comes to e.g. manually guiding a distant robot in realtime via its cogDT and skillfully supervising or automating inmotion. Resulting advantages are professional and personal. Indeed, _Metarobotics_ invites to redefine and individualize the notion of workplace in robotized applications. It shifts workspaces from restrictive and location-discrete " _office or/ and home_ "-rules to flexible and location-continuous " _from anywhere if desired_ "-opportunities in Society 5.0. Commuters, 

such as robot technicians, exposed to project-related traveling, and outsourced employees can benefit from this shift. They can work from _anywhere_ , which impacts their work-life-balance. _Metarobotics_ leverages digital technologies to meet key values like inclusion and co-innovation worldwide. It is thus likely to not only engage and bind but also offer opportunities to the post generation Z to capitalize on curiosity and creativity. 

## _F. Targeted Design and Engineering Functionalities_ 

_1) Collective and Generative Knowledge for Citizens and Robots: Metarobotics_ makes use of sensing with on-board preprocessing and reasoning based upon off-loaded AI _/_ ML at the edge (see figures 2 and 5). On-device storage and computation limitations as well as latency and congestions issues are mitigated. Sensitive data are securely collected and analyzed through a trusted decentralized AI _/_ ML-pipeline. It employs loosely-coupled microservices to create new knowledge (see figure 5). Service discovery and composition, load balancing, circuit breaker function for reliability and fault tolerance, as well as rate limiting against excessive usages need to be implemented. Resilience, adaptation at run-time, and scalability are resulting advantages. FL is run on top of variants of Ensemble Learning (see figure 4) to address accuracy issues due to significantly heterogeneous class biases among local data [38] while creating FFMs [31]. _Metarobotics_ benefits from FFMs when AI _/_ ML models are intended to achieve similar tasks (e.g., picking and placing a rotor in an assembly line and grasping bottles in home settings) using new and legacy robots with limited data access. Once a FFM is built and shared in the Metaverse, parameter efficient transfer learning (e.g., Adapter, Prompt, Diff-Pruning, BifFit) accelerates the specialization of the collective intelligence condensed in pre-trained parameters to downstream tasks. While most parameters are frozen, only a few are fine-tuned, which prevents building the entire large model from scratch and substantially saves time and energy. 

A challenge in _Metarobotics_ resides in the transferability of trained models from the Metarverse to reality in terms of performance. Even though the Metaverse is fed with live measured data, the cogDT might be model-based and data can be noisy, leading to model uncertainties (e.g., truncation, undesired frequencies). As e.g. reinforcement learning (RL) is involved in applications, _Metarobotics_ can leverage knowledge distillation and reuse [39], among others, to address this challenge. In distillation, the policy in reality is a model that minimizes action divergences between Metaverse and reality [39]. In the reuse case, the real policy is a weighted combination of policies developed in Metaverse while considering the performance expected from the targeted robot in reality [39]. 

Another challenge in the Metaverse is the design of modular robots that can complete a task in reality. Being capable to assess the feasibility of this objective to make decision contributes to self-efficacy introduced in section IV-D. Given task objectives, a robot configuration can be searched to complete the task with the highest performance. Generative Adversarial Networks (GANs) are used to learn to map one task to a distribution of configurations [40]. Motivated by the graph-like kinematics of robots, a global control policy of modular robots 

6 


![](1_survey/papers/md/Kaigom2024Metarobotics_figs/Kaigom2024Metarobotics.pdf-0006-01.png)


**----- Start of picture text -----**<br>
4<br>Heterogenous  Cloudlet & Client Apps (e.g., Analytics, Diagnosis, Maintenance, Decision Support,<br>Composable  Control, Global Co-Innovation,…, Privacy, and Safety as a Service)<br>Services Scalable and trustworthy collaboration spaces to accelerate value creation at the global stage Space Applications:<br>Metaverse (Robotized On-Orbit-<br>Servicing/Exploration)<br>3 Standards & Protocols for Volumetric Streams (Transmission: Dynamic Adaptive Streaming over HTTP (DASH),  Real-<br>Time Streaming Protocol (RTSP), Web Real-Time Communication (WebRTC), etc., 3D Dyn. Graphics: WebGL, Web3D, etc.)<br>Beyond URLLC, such as 6G: Radio Access, Core Terrestrial & Non-Terrestrial (e.g. Optical Wireless Communication) Networks<br>2 Decentralized Data Collaborative Ensemble in Federated & Transformer-based<br>Spaces & Management Caching Reinforcement Learning natural robot control<br>Caching Caching Caching<br>Multi-Access  Multi-Access<br>Infrastructure Edge Infrastructure Edge Infrastructure<br>Virtualization Computing Virtualization Computing Virtualization<br>Server Server<br>Edge AI | 3D Simulation  Microservices|Orchestrat. Rendering | Storage<br>Multimodal Sem. Encoding Multimodal Sem. Encoding Multimodal Sem. Decoding<br>Access Network Access Network Real<br>1<br>On-Device Inference On-Device Analytics<br>… … Virtual<br>5<br>Local Physical Industrial Robots Class Room & Home Settings Mixed Holoported Robotized Applications<br>Commu- nication<br>)(Holoportation Mining  )(Blockchain Zero Knowl.  Proof ()Privacy Situational & Context Awareness<br>: High-Performance   Volumetric Fusion  Experiantial Network In- telligence|ZeroTouch Mngt   Pre-trained & fine-tuned federa. foundation models<br>MEC<br>Intell. Computing and Storage<br>QoS-aware  Computation  Offloading QoE-Aware  Computation  Offloading<br>Intelligent  Perception<br>**----- End of picture text -----**<br>


Fig. 5: A high-level architecture of _Metarobotics_ with five key layers being highlighted (see numbering). 

can be learned using Graph Neural Networks (GNNs) in which knowledge is shared among different configurations [41]. 

Complementary knowledge about entities, such as physical, contextual, functional, cultural, and ethical insights, is targeted in _Metarobotics_ . The reason is at least twofold. First, a decentralized semantic storage based upon ontologies for fast and robust queries. Second, the inference of semantic properties of entities under heterogeneous sensory perceptions and task objectives. This is because symbiotic and thus mutualistic interactions between robots and citizens are envisioned. In this case, inferred knowledge needs to overcome the often handcrafted perspective of citizens [42], [43]. Knowledge is therefore also interpreted from the conceptual perspective of individual robots depending upon, for instance, their operational contexts. Unsupervised clustering [42] or transformerbased neural networks [43] can be utilized to this end. In combination with human perception and cognition, these skills strengthen reasoning capabilities of decentralized cogDTs. Autonomous inference and substitution of missed information in remote applications _"from household to industrial robotics"_ [42] even in deep space applications by combining terrestrial and non-terresrial networks are targeted outcomes of _Metarobotics_ , as depicted in figure 5). 

_2) CogDT-Based Multi-Agent Optimization:_ Swarms of distributed cogDTs are assumed to operate as systems of decentralized optimization agents in _Metarobotics_ . Each agent individually explores a solution space and shares its experience to collectively contribute to the optimization of a cost function to complete robotized tasks. Semantics-driven M2Mcommunication standards, such as OPC UA FX, can support this collaboration. Related information models enable a common and global understanding of exchanged data, helping out each cogDT to self-adapt to cumulative broadcasts of findings sent by other cogDTs. Similarly to the particle Swarm Optimization (PSO), the approach is gradient-free. It is not under- 

mined by discontinuous cost functions. However, in contrast to the PSO, advantages of CogDT Swarm Optimization (CSO) include the heterogeneous abstraction (e.g., modular robots with distinct configurations designed as in section IV-F1) and reasoning capability of each cogDT. Instead of uniformly enforcing predefined behavior patterns for each swarm member as in the PSO, each cogDT independently exploits attentionbased rewards to contextually and situatively reasons and decides how to sustainably contribute to swarm objectives. 

_3) Green Ultra-Massively Adopted π-HRC:_ Surroundingsand application-awareness for b-URLLC-based mobile Holoportation (see section V-C) can be used in _Metarobotics_ to democratize the sustainable access to remotely conducted robotized applications. Mobile Holoportation has been initiated by Microsoft in the automotive field and remains an active research field [44]. In the robotics context of _Metarobotics_ , the adoption of mobile Holoportation by an ultra-massive number of geographically distributed stakeholders is driven by two incentives in the Society 5.0 context. First, an individualized QoE of citizens that also aligns with objectives of Industry 4.0. Needs and intentions of workers and robots are inferred to enhance process efficiency through anticipation. High resolution sensing allowed by the Teraherz and mmWave spectrum [20], [21] and collective localization of physical siblings are enablers. To this end, AI _/_ ML, such as RL, can scrutinize emitted and acknowledged sensing data to capture a channel model for motion inference and thus localization [20], [21] of physical siblings of collaborating decentralized cogDTs. 6G-based centimeter-level 3D localization (see table I) helps understand root causes (e.g., obstacles) and prevent collisions of mobile robots in holoported spaces in real-time. Second, the QoV like work-life-flexibility stemming from decent work conditions and multi-stage characteristics of the underlying sustainability as advocated by Industry 5.0. In _Metarobotics_ , the inherent energy efficiency of smart mobility is combined with mini- 

7 

mized energy consumption of 6G (see table I) together with an active reduction of energy expenditures of robots. Remote time scaling of joint trajectories or posture optimization in the Jacobian null-space while productively meeting goals with the decoupled end-effector can be done to this end. 

_4) Holoportation with Sensation Feedback:_ Holoportation with sense of touch is expected to be pivotal in _Metarobotics_ . It complements visual immersion and enhances the QoE and QoV. For instance, being aware and feeling the exchange of mechanical energy with remote entities meet various goals. In the former case, force feedback indicates physical interactions with other entities. In the latter case, tactile sensations come into play. A high resolution of measuring how pressure is distributed over contact areas is enabled. Tactile sensations thus provide a more accurate perception of distant and occluded objects in even cluttered areas. Touch-sensitive applications, such as tactile manual guidance in _π_ -HRC and remote lightsout manufacturing, benefit from this perception of entity properties. These include stiffness and softness (e.g., elasticity, plasticity), roughness, geometry, and contact force localization. 

Motivated by ISO/IEC TS 23884:2021(E), at least three approaches can help realize the sense of touch in AR _/_ VR-based interactions in _Metarobotics_ . The first one, used in advanced multi-body simulation, exploits parameters for constraint force mixing and error reduction to mimic customizable spring and damping behavior of entity materials during contact dynamics. The second approach is a real-time simulation of an elastic tactile sensor as proposed in [45]. In this case, the tactile sensor is voxelized to yield particles as voxel centers. Their displacements under pressure help render deformation processes by using the (Moving Least Squares) Material Point Method [45]. The deformed mesh is then reconstructed on the basis of the particle location [45]. An advantage of this second method for _Metarobotics_ is the dynamic-visual and tactile information perceived by citizens. This enriches their immersion in _Metarobotics_ especially when soft materials are considered. 

Since human skin and grasped objects, including a robot, might have varying temperatures, as in glass factories [7], thermo-tactile feedback is considered in the third approach [46]. A triboelectric and pyroelectric ring-sensor worn by a citizen and connected to the holoported environment via 6G reflects the thermo-tactil feedback. A nanogenerator tracks how muscles swell when fingers bend to estimate pressure by integrating voltage [46]. A heated nichrome metal wire provides thermo feedback in the ring [46]. Thermo-tactile feedback fosters values of Industry 5.0 and Society 5.0 in _Metarobotics_ , such as socialization, resilience, and diversity. Indeed, geographically distributed collaborators can showcase and familiarize with specific cultural rules of People-to-People (P2P) communication and etiquette, including remote hugs and handshakes in meetings [46], without e.g. contamination hazards. 

## _G. Parallel Intelligence for Human-Centered Robotics_ 

Embedding visual and tactile features in a latent space can help cogDTs predict tactile forces from images [47]. Learned multi-modal correlations between images and tactile features allow it to adapt robots and inform citizens about various environment properties like roughness [47]. Cross-modal reasoning 

can be achieved using interconnected multi-modal knowledge graphs (MMKG) [30], [48] that evolve from structured crowd sourcing, IoT, and synthetic data. This leads to a swarm of cogDTs (as MMKG-nodes) with maturing intelligence in terms of the depth and diversity of knowledge integration, as well as edge and cloudlet processing rates (see figure 5). The swarm acts as a PIE alongside and beyond human capabilities. Experience is captured by e.g. grounding representation symbols to their semantics in the real word structured in the MMKG [48] to empower industry and society. In _Metarobotics_ , the symbol robot can be grounded to contextual and situational multi-modal data like joint state, ML-models, videos, and CAD files to enlarge the breadth of experience. 

## _H. Global, Trustworthy, and Cross-Domain Robotics_ 

_Metarobotics_ aims to capitalize on several opportunities delivered by the Metaverse to lower entry barriers and revamp the collaborative realization of distant robotized applications. Its location-agnostic accessibility can yield an engaging proximity, visibility, democratization, experimentation, and familiarization with robotics. In the Metaverse, which is also viewed as an interconnection of decentralized virtual collaboration spaces loosely coupled with digital and physical assets, as shown in figure 6, robotics-related contents in terms of knowledge, service, and products are globally created and exposed as well as instantly discovered, purchased, and combined. Contents are consumed by cogDTs of assets, processes, and citizens worldwide using Blockchain-based Non-Fungible Tokens (NFTs) for e.g. authenticity, authorization, and ownership check. _Metarobotics_ aims to enable a sovereign data sharing to preserve privacy. Following the connector idea of the International Data Space Association and project GAIA-X [49], _Cotrusting_ can manage who is granted access to raw data by initially exposing only meta-data instead of raw data. Upon agreement, encrypted raw data are sent to authorized cogDTs. Raw data are jointly processed with trust by design (see section V-D2). Virtualized robotized resources and services are combined through standardized interfaces for enhanced performances. They are then deployed in collaboration spaces to quickly and cost-effectively assess and shape benefits of robotics in untapped markets. Resources are parts of a global society and circular economy (based upon interoperable NFTs) in the Metaverse. While constraints and shocks can be virtually customized, interactions with physical distant assets use measured data, raising the applicability of assessment results. 

## _I. Streamlining Education Worldwide_ 

Learners can expect elevated experience in robotized applications under authentic industrial or societal conditions close up with _Metarobotics_ (see figure 6). These include learning best practices even in the early innovation phases. _Humotics_ allows teachers to extend excursions often restricted to local factories, for e.g. logistic reasons, to concerns abroad at negligible complexity and costs. Since an intrinsically safe, volumetric, and multi-modal proximity to distant physical robots will be ensured in _Metarobotics_ by exposing learners to cogDTs, tremendous intrinsically safe possibilities for course design 

8 

arise. Immersive learning is customized to the individual skills and background of learners and teachers using certificates. Learners discuss ideas with on-site experts in real-time to validate theoretical results. Industrial and societal open data are provided to laboratories. Students thereby learn with authentic data how to transform industrial resources into competitive advantages using AI _/_ ML-based analytics. Developed prototypes, such as filters and pre-trained models, are re-injected in the Metaverse to cross-fertilize industry, society, and academia. 

## V. ARCHITECTURE AND ENABLING TECHNOLOGIES 

An architecture of _Metarobotics_ is given in figure 5. Enabler technologies therein provide together functionalities to fulfill goals stipulated in section IV. Data are collected in the first perception layer. Encrypted relevant results of on-device preprocessing are offloaded to the second microservice-enabled MEC-layer for further processing. The third communication layer is b-URLLC-driven. Delay- [50] and Energy-efficient [51] cloudlets can be deployed in the fourth layer to benefit from edge proximity and resources elasticity. This streamlines the execution of _π_ -HRC applications in the final fifth layer. 

## _A. Communication Driven by b-URLLC_ 

_1) Tactile Internet:_ Interactions between citizens and remote robotized applications involve tactile sensors with spatial resolutions resp. sampling rates below 0 _._ 5 mm resp. above 10 KHz. 6G-based tactile internet is expected to meet global network connectivity needs for a massive number of industrial and consumer-level applications. Ultra-reliable data transmission rates in multiple TBps with a stringent sub-millisecond latency (see table I), i.e., below the time of reaction of citizens ( _≈_ 0.2s), and substantially reduced latency jitters and packet losses will improve the QoS and QoE in _Metarobotics_ . Indeed, delays raise the sensation of heavier objects and jitters induce not only instabilities, but also the misleading sensation of a varying mass of objects [52]. An accurate perception of the Cartesian effective mass of robots in given directions is however safety-relevant in robotized applications, such as physical _π_ -HRC. Since packet losses distort the power of the perceived force [52], _Metarobotics_ will benefit from the enhanced reliability of 6G wireless communication and beyond, as quantified in table I. Nevertheless, data synchronization in volumetric fusion and coordinating different signals such as visual, audio, thermal, and haptic data streams with distinct latency values require more attention to further enhance the QoE and QoS. 

_2) Haptic Feedback Support:_ In [53], the transmission of a haptic-visual signal that does not depend upon timestamp synchronization has been proposed. The synchronization is instead based upon the combination of key samples of haptic and key frames of visual signals by taking advantage of the sequential correlation observed in the transmission and playback [53]. Context-aware haptic feedback is addressed in [54] by adopting a two stage approach. First, a supervised learning that relies upon Artificial Neural Network (ANN) is applied to control data from a VR glove and predict whether haptic feedback is necessary or not with an accuracy of 99%. Then, RL is used to predict samples of 

haptic feedback with an accuracy of 92% for four different materials [54]. Characteristics of People to Machine (P2M) traffic in haptic teleoperation, such as the packet interarrival time and the correlation between human control and haptic feedback during a time window equivalent to a polling cycle, are estimated in [55]. Whereas the generalized Pareto arrival model provides the smallest fitting error when compared with three other statistical distributions (t-location, Logistic, and Exponential), a considerable cross-correlation between 0.6 and 0.8 is observed between control (master to slave) and feedback (slave to master) traces. Therefore, an ANN estimates bandwidth requirements for P2M traffics. The bandwidth is then predictively allocated to the control traffic and, at the same time, interactively granted (by harnessing the correlation) to the feedback traffic to reduce latency and accelerate haptic feedback [55]. In the multi-modal case (e.g., visual, haptic, and audio signals), haptics-related control traffic is allocated additional bandwidth unlike content requests. Furthermore, haptic feedback packages are assigned a higher priority during the transmission for a lower latency [55]. 

_3) High Mobility Support:_ Intelligent 6G networks are expected to learn and predict properties and communication requirements of applications to adapt their operational configurations and enable multi-modal tactile communication capabilities under high mobility [56]. Predictions can result from historical observations when it comes to e.g. train beams for the use of mmWave and THz bands to support increased mobility [57]. Online AI _/_ ML, such as RL, operates at the network edge to optimize the usage of resources via efficient anticipations of upcoming demands that leverage e.g. Open Source Multi-access Edge Computing (OS-MEC) [58] to fulfill constraints on transmission delay [9]. OS-MEC ensures disaggregation, i.e., a separation and adaptation of MEC functions and resources, for a flexibly tailored edge performance by taking advantage of Network Function Virtualization (NFV) [58]. End-to-end delays include not only the elapsed time for caching, computing, and transmission [9], but also the overhead to train the beam to estimate channel states [57]. A GNN that generalizes over network structure, routing approach, and traffic intensity and predicts the average delay and jitter is combined with RL to optimize routing strategy and congestion control via Software Defined Networking (SDN) in [57], [59]. Furthermore, a mobility management that foresees the cell in which a citizen in motion is likely to enter and be allocated radio before handover is proposed by [57]. This prediction helps reduce the overhead of signaling [57] along with related latency and power consumed to this end. It also achieves a continuous coverage during mobility [57] and thus enhance QoS and QoE in _Metarobotics_ . In addition to a low power consumption of 1 pJ/bit for a sustainable wireless communication, as mentioned in table I, mobility support at a speed of up to 1000 Km/h is a prominent advantage for sustainable pervasiveness and itinerancy goals pursued by _Metarobotics_ . 

## _B. Cognitive Digital Twin_ 

_1) Cognition:_ Industrial and personal applications are subject to uncertainties. Noisy data, truncated models, faults, 

9 

anomalies, and undesired contact forces are a few causes. For the sake of adaptable and robust interactions between citizens, cogDTs, and physical assets, the standard DT is equipped in _Metarobotics_ with cognitive skills. These encompass _"perception"_ , _"attention"_ , and _"reasoning"_ [60]. Perception aims to a meaningful representation of sensed and accessible data about entities [60]. Attention supports the selective concentration on relevant information [60]. To create knowledge and anticipate uncertainties, knowledge engines of cogDTs learn on data structured in a knowledge graph (KG). These engines usually combine sub-symbolic (e.g., Multi-Layer Perceptron (MLP), Neural Tensor Network (NTN), Deep Learning) with symbolic (e.g., ontologies-, rules-, and expert systems-based) AI _/_ ML, to predict properties and missing relations (i.e., edges) between entities (i.e., nodes) of a KG as well as their clustering and constraints. In _Metarobotics_ , MLP and NTN, for instance, can be used to capture correlations between nodes and edges by learning latent features when properties cannot be directly observed [61], [62]. Since ontologies like OWL meaningfully formalize relations, rules, and constraints between nodes, they are interpretable by cogDTs, robots, and citizens. This in turn supports M2M, P2M, P2P, as well as cogDT to cogDT, Machine to cogDT, and Citizens to cogDT communication in _Metarobotics_ . Further types of functional constraints along with incompatibilities can be learned by observing sets of nodes and edges [62]. Hence, a skillful, fast-growing, and evolving ecosystem with an actively harnessed latent _"body of knowledge"_ [63] and _"body of experience_ [63] arises, in which cogDTs find inputs about what they reason. The goal of the cogDT-based PIE is to predict and anticipate events, while defining and scheduling the next actions to be recommended to citizens and robots in _Metarobotics_ , as highlighted in figure 6. 

_2) Uncertain Knowledge Graph:_ Uncertainty accommodation will be essential to handle unfamiliar and unforeseen operational conditions in remote workspace in _Metarobotics_ . CogDTs generalize knowledge from known facts to infer course of action and adapt. For instance, a cogDT can contextualize and characterize an initially unknown object as a grasp target of the robot (see r.h.s of figure 3). The trustworthiness of relations between a payload and similar workpieces previously manipulated are used to this end. Therefore, relations between pairs of KG nodes are assigned confidence scores that reflect the level of belief in the relation to take uncertainties into consideration [64]. This contrasts with deterministic KG in Robobrain [61], where the belief is maximal. The capability cogDTs to transfer knowledge can be based upon the classification of nodes and prediction of links between them [62]. A knowledge engine can thereby discover and recommend facts in addition to efficiently answering queries for even unseen facts [64]. Nodes and relations of such an uncertain KG are embedded into a low-dimensional continuous (latent) space [64]. Efficiency refers to insightful abstractions of non-Euclidean and multi-modal data as well as the richness and expressiveness of representations learned using e.g. GNN [60]. Probabilistic soft logic and probabilistic box can be used to predict confidence scores of unseen facts by transferring confidence scores related to available knowledge to unseen relations [64]. 


![](1_survey/papers/md/Kaigom2024Metarobotics_figs/Kaigom2024Metarobotics.pdf-0009-03.png)


**----- Start of picture text -----**<br>
Metarobotics<br>Beyond URLLC (e.g., 6G) Network Created Values<br>Industry<br>Knowledge | Holop.| Planning as a Service<br>AI/ML | Privacy | Automation as a Service Mobility<br>Sensing| Monitoring| Control as a Service<br>Society<br>FFM-based Intelligence<br>Fixed / Mobile and  Multi‐Access Edge Computing‐based Metaverse with Virtualized & In‐Motion<br>Physical Application Pervasive & Itinerant Robotics as a Service Swarm of cogDTs Application,  𝝅 ‐Workspace<br>**----- End of picture text -----**<br>


Fig. 6: Metaverse is service _/_ content provider for _Metarobotics_ . 

## _C. Holoportation_ 

The pipeline for Holoportation includes scene capture, volumetric fusion, transmission, and rendering phase [65], [66]. 

_1) Capture:_ Surrounding RGB-D cameras like Kinect can be used to capture scene from which point clouds (PCs) [66], [67] or time-varying 3D mesh (TVM) [65], [67] are generated. 

_2) Fusion:_ For PCs, a synchronized merging of RGBD frames can be conducted for reconstruction [68]. In the TVM case, a deformation model of the nonrigid motion field between frames can be used for a temporal volumetric fusion from which a 3D polygonal model is obtained [65]. 

_3) Encoding and Transmission:_ The compression aims to balance real-time capability, low-latency, and quality, which aligns with a high QoS and QoE. In the PCs case, octree occupancy can be used to represent geometry [66]. Vertex deduplication, the reduction of position and normal data, and the assignment of a constant color to non-foreground from segmentation help reduce the frame size in the TVM case [65]. Dynamic Adaptive Streaming over HTTP (DASH) currently support both mesh- and point cloud-based Holoportation [67]. 

_4) Latency and Throughput Challenges:_ Holoportation throughputs are in the Gbps range and already supported by 5G networks with a 4K spatial light modulator for displaying [69]. However, in VR, the experienced computation and communication latency of more than 140 ms is at least 9 _×_ the maximally allowed latency (< 15 ms) [70]. Also, ultra-high definition in 8K with e.g. 48 Gbps is better supported by 6G (see table I). Computation resp. communication latencies can be reduced using MEC [70]. In _Metarobotics_ , robot abstractions can help further reduce latency if e.g. the environment of the remote robot does not change. Without high dynamic modes, the robot posture is retrieved from its forward kinematics and rendered on the receiver side. Only current joint positions (i.e., a vector of scalars) are therefore transmitted without expensive point cloud processing. As dynamics are more involved, kinematic and dynamic models can be learned by using GANs [71] and retrieved once joint positions and velocities of the remote robot are received. Conversely, the velocity of external joint torques induced by manual guidance can reveal citizen intentions to manually accelerate or decelerate robots. 

## _D. Metaverse_ 

Another key enabler of _Metarobotics_ is the Metaverse, as shown in figure 6. It is a digital ecosystem fed with hybrid (e.g., sensed, synthesized) data and populated by cogDTs that mirror real and prospective applications. Usually, this occurs in decentralized and interconnected virtual collaboration spaces. _Metarobotics_ projects these spaces onto further digital and 

10 

physical environments (e.g. shop floor, home settings, trains) on-demand and re-injects experience, knowledge, and wisdom gained from completing robotized applications back into the Metaverse for efficient cross-fertilization and prosperity. This bidirectional communication is depicted in figure 6. 

The _Omniverse_ platform [72], recently released by Nvidia, is increasingly in use at e.g. BMW [73] and Ericsson [74] to develop such places in the manufacturing and telecommunication realm. In _Metarobotics_ , however, citizens are empowered with tools to influence the course of action of robotized applications in society and industry as well, adhering to the concept of metasocieties that extends real society with skillful and farreaching forecasts and suggestions [75]. _Metarobotics_ targets a global, standardized, and trusted robotics-related approach that leverages AI _/_ ML-based emerging technologies, such as FFMs, to accelerate familiarization, adaptation, and self-fulfillment. 

_1) Interoperability:_ A mutual understanding of formats for scene modeling, processes, and services is pivotal to use cogDTs and enhance QoE across collaboration spaces involving heterogeneous tools. ISO/IEC 23005 standardizes interoperability between collaboration spaces as well as physical and collaboration spaces [76]. It provides an architecture and information models for data traffics and specifies data formats for e.g. robotic devices, such as sensors, actuators, and virtual assets [76]. ISO/IEC 23005 considers the use of virtual decisions to command physical assets, as pursued by _Metarobotics_ . 

_2) Self-Organization, Privacy, and trust:_ Blockchains offer a tamper-proof collective storage and synchronization for self-organization in _Metarobotics_ . Traceable and encrypted transactions can be automatically triggered and executed as blockchained smart contracts in decentralized networks of cogDTs using a bi-level coordination for resilience and autonomy [77]. The authenticity of data and services provided by cogDTs can be verified using Self-Sovereign Identity with Zero Knowledge Proofs (at MEC in _Metarobotics_ , see figure 5) without data traffics over internet or server storage [78]. This implies that, for _Metarobotics_ , citizens and cogDTs can share the same authentication for distinct collaboration spaces [78]. As trustworthiness with chemical signature (e.g., in 3D printing) is needed, makerchains help against counterfeiting [79]. 

## VI. CONCLUSION 

_Metarobotics_ targets a collectively informed usage of remote robots operating in different environments from anywhere. It leverages emerging technologies for a trustworthy, pervasive, and itinerant access to and interaction with remote robotized applications. This paper has surveyed relevant technologies toward this end, such as cogDTs, 6G, Holoportation, and Blockchain. It has also highlighted their integration based on microservices, dynamic interplay, and usefulness to meet goals of _Metarobotics_ . How the QoE and QoV in professional and personal activities can be elevated, has been introduced. 

Challenges remain to be addressed. Assessing the performance of mesh- and point cloud-based Holoportation in contact and non-contact robotized applications deserves further investigations. Standardizing a dedicated and ressource-adaptive protocol for Holoportation is likely to strengthen interoperability and consumer-level adoption. In this regard, _Metarobotics_ 

will benefit from developing transmitter and receiver chipsets for 6G beyond the 100 GhZ [80] and their massive societal and industrial penetration. A realistic embodiment of avatars for acceptance and QoE purposes requires contextually inferred appearances. An approach to realize this objective could be the image-based representation from ISO/IEC 23488:2022(E). Furthermore, multi-modal feedback, locomotion, and gestures need to be synchronized with subjective gaze-related emotions. Although _Metarobotics_ targets robotics, it is transferable to other domains. Pervasive and itinerant Product Lifecycle Management ( _π_ -PLM), regardless of the product, is an example. 

## REFERENCES 

- [1] V. Sunder M., A. Prashar, G. L. Tortorella, and V. R. Sreedharan, “Role of organizational learning on industry 4.0 awareness and adoption for business performance improvement,” _IEEE Transactions on Engineering Management_ , pp. 1–14, 2023. 

- [2] D. Mourtzis, _Design and operation of production networks for mass personalization in the era of cloud technology_ . Elsevier, 2021. 

- [3] W. Xian, K. Yu, F. Han, L. Fang, D. He, and Q.-L. Han, “Advanced manufacturing in industry 5.0: A survey of key enabling technologies and future trends,” _IEEE Transactions on Industrial Informatics_ , pp. 1– 15, 2023. 

- [4] E. G. Carayannis, R. Canestrino, and P. Magliocca, “From the dark side of industry 4.0 to society 5.0: Looking “beyond the box” to developing human-centric innovation ecosystems,” _IEEE Transactions on Engineering Management_ , pp. 1–17, 2023. 

- [5] J. Wilson, “Generation z’s adoption of new technology spells a new era for entertainment,” https://www.forbes.com/sites/joshwilson/2022/05/26/ generation-zs-adoption-of-new-technology-spells-a-new-era-for-entertainment/ ?sh=7ac824a56c0a, Forbes, May 2022, last accessed: 07.12.2023. 

- [6] D. Mourtzis, J. Angelopoulos, and N. Panopoulos, “Closed-loop robotic arm manipulation based on mixed reality,” _Applied Sciences_ , vol. 12, no. 6, p. 2972, 2022. 

- [7] N. Barker and C. Jewitt, “Collaborative robots and tangled passages of tactile-affects,” _J. Hum.-Robot Interact._ , vol. 12, no. 2, mar 2023. [Online]. Available: https://doi.org/10.1145/3534090 

- [8] E. H. Østergaard, “Welcome to industry 5.0,the “human touch” revolution is now under way,” _Universal Robots_ , vol. 5, p. 2020, 2019. 

- [9] E. C. Strinati and S. Barbarossa, “6g networks: Beyond shannon towards semantic and goal-oriented communications,” _Computer Networks_ , vol. 190, p. 107930, 2021. 

- [10] H. Tataria, M. Shafi, A. F. Molisch, M. Dohler, H. Sjöland, and F. Tufvesson, “6g wireless systems: Vision, requirements, challenges, insights, and opportunities,” _Proceedings of the IEEE_ , vol. 109, no. 7, pp. 1166–1199, 2021. 

- [11] Y. Shi, W. Shen, L. Wang, F. Longo, L. Nicoletti, and A. Padovano, “A cognitive digital twins framework for human-robot collaboration,” _Procedia Computer Science_ , vol. 200, pp. 1867–1874, 2022. 

- [12] R. Petkova, V. Poulkov, A. Manolova, and K. Tonchev, “Challenges in implementing low-latency holographic-type communication systems,” _Sensors_ , vol. 22, no. 24, p. 9617, 2022. 

- [13] F. Semeraro, A. Griffiths, and A. Cangelosi, “Human–robot collaboration and machine learning: A systematic review of recent research,” _Robotics and Computer-Integrated Manufacturing_ , vol. 79, p. 102432, 2023. 

- [14] M. Selvaggio, M. Cognetti, S. Nikolaidis, S. Ivaldi, and B. Siciliano, “Autonomy in physical human-robot interaction: A brief survey,” _IEEE Robotics and Automation Letters_ , vol. 6, no. 4, pp. 7989–7996, 2021. 

- [15] M. Gagné, S. K. Parker, M. A. Griffin, P. D. Dunlop, C. Knight, F. E. Klonek, and X. Parent-Rocheleau, “Understanding and shaping the future of work with self-determination theory,” _Nature Reviews Psychology_ , vol. 1, no. 7, pp. 378–392, 2022. 

- [16] C. K. Rath, A. K. Mandal, and A. Sarkar, “Microservice based scalable iot architecture for device interoperability,” _Computer Standards & Interfaces_ , vol. 84, p. 103697, 2023. 

- [17] P. Jain, A. Gupta, N. Kumar, and M. Guizani, “Dynamic and efficient spectrum utilization for 6g with thz, mmwave, and rf band,” _IEEE Transactions on Vehicular Technology_ , vol. 72, no. 3, pp. –, 2023. 

- [18] M. Mahmoud, S. Rizou, A. S. Panayides, N. V. Kantartzis, G. K. Karagiannidis, P. I. Lazaridis, and Z. D. Zaharis, “A survey on optimizing mobile delivery of 360° videos: Edge caching and multicasting,” _IEEE Access_ , 2023. 

- [19] I. F. Akyildiz, C. Han, Z. Hu, S. Nie, and J. M. Jornet, “Terahertz band communication: An old problem revisited and research directions for the next decade,” _IEEE Transactions on Communications_ , 2022. 

11 

- [20] H. Chen, H. Sarieddeen, T. Ballal, H. Wymeersch, M.-S. Alouini, and T. Y. Al-Naffouri, “A tutorial on terahertz-band localization for 6g communication systems,” _IEEE Communications Surveys & Tutorials_ , vol. 24, no. 3, pp. 1780–1815, 2022. 

- [21] H. Wymeersch, J. He, B. Denis, A. Clemente, and M. Juntti, “Radio localization and mapping with reconfigurable intelligent surfaces: Challenges, opportunities, and research directions,” _IEEE Vehicular Technology Magazine_ , vol. 15, no. 4, pp. 52–61, 2020. 

- [22] C. Keroglou, I. Kansizoglou, P. Michailidis, K. M. Oikonomou, I. T. Papapetros, P. Dragkola, I. T. Michailidis, A. Gasteratos, E. B. Kosmatopoulos, and G. C. Sirakoulis, “A survey on technical challenges of assistive robotics for elder people in domestic environments: The aspida concept,” _IEEE Transactions on Medical Robotics and Bionics_ , 2023. 

- [23] H. Abdollahi, M. Mahoor, R. Zandie, J. Sewierski, and S. Qualls, “Artificial emotional intelligence in socially assistive robots for older adults: a pilot study,” _IEEE Transactions on Affective Computing_ , 2022. 

- [24] B. Yang, J. Huang, X. Chen, X. Li, and Y. Hasegawa, “Natural grasp intention recognition based on gaze in human–robot interaction,” _IEEE Journal of Biomedical and Health Informatics_ , pp. –, 2023. 

- [25] S. Marcos-Pablos and F. J. García-Peñalvo, “Emotional intelligence in robotics: a scoping review,” in _New Trends in Disruptive Technologies, Tech Ethics and Artificial Intelligence: The DITTET Collection 1_ . Springer, 2022, pp. 66–75. 

- [26] O. Korn, N. Akalin, and R. Gouveia, “Understanding cultural preferences for social robots: a study in german and arab communities,” _ACM Transactions on Human-Robot Interaction (THRI)_ , 2021. 

- [27] S. Fazelpour and M. De-Arteaga, “Diversity in sociotechnical machine learning systems,” _Big Data & Society_ , 2022. 

- [28] Z. Gong, P. Zhong, and W. Hu, “Diversity in machine learning,” _Ieee Access_ , vol. 7, pp. 64 323–64 350, 2019. 

- [29] Z.-Y. Huang, C.-C. Chiang, J.-H. Chen, Y.-C. Chen, H.-L. Chung, Y.-P. Cai, and H.-C. Hsu, “A study on computer vision for facial emotion recognition,” _Scientific Reports_ , vol. 13, no. 1, p. 8425, 2023. 

- [30] X. Li, Y. Tian, P. Ye, H. Duan, and F.-Y. Wang, “A novel scenarios engineering methodology for foundation models in metaverse,” _IEEE Transactions on Systems, Man, and Cybern.: Systems_ , 2022. 

- [31] S. Yu, J. P. Muñoz, and A. Jannesari, “Federated foundation models: Privacy-preserving and collaborative learning for large models,” _ArXiv_ , vol. abs/2305.11414, 2023. [Online]. Available: https://api.semanticscholar.org/CorpusID:258823148 

- [32] Y. Li, W. Liang, J. Li, X. Cheng, D. Yu, A. Y. Zomaya, and S. Guo, “Energy-aware, device-to-device assisted federated learning in edge computing,” _IEEE Transactions on Par. and Distributed Systems_ , 2023. 

- [33] N. Sharma, B. Meglicki, and C. Liu, “Intuitive virtual reality humanrobot interface with volumetric tele-presence, visual haptics and audio,” _2nd Workshop toward robot avatars, IEEE international conference on robotics and automation, ICRA, UK, London_ , pp. 1–3, 2023. 

- [34] A. Abdelraouf, M. Abdel-Aty, and Y. Wu, “Using vision transformers for spatial-context-aware rain and road surface condition detection on freeways,” _IEEE Transactions on Intelligent Transportation Systems_ , vol. 23, no. 10, pp. 18 546–18 556, 2022. 

- [35] L. Hoyer, D. Dai, H. Wang, and L. Van Gool, “Mic: Masked image consistency for context-enhanced domain adaptation,” in _Proceedings of the IEEE/CVF Conference on Comp. Vision and Pat. Recogn._ , 2023. 

- [36] C. J. Conti, A. S. Varde, and W. Wang, “Human-robot collaboration with commonsense reasoning in smart manufacturing contexts,” _IEEE Transactions on Automation Science and Engineering_ , 2022. 

- [37] E. E. Kossek, M. B. Perrigino, and B. A. Lautsch, “Work-life flexibility policies from a boundary control and implementation perspective: a review and research framework,” _Journal of Management_ , 2023. 

- [38] S. Zeng, Z. Li, H. Yu, Z. Zhang, L. Luo, B. Li, and D. Niyato, “Hfedms: Heterogeneous federated learning with memorable data semantics in industrial metaverse,” _IEEE Transactions on Cloud Computing_ , 2023. 

- [39] Z. Zhu, K. Lin, A. K. Jain, and J. Zhou, “Transfer learning in deep reinforcement learning: A survey,” _IEEE Transactions on Pattern Analysis and Machine Intelligence_ , 2023. 

- [40] J. Hu, J. Whitman, M. Travers, and H. Choset, “Modular robot design optimization with generative adversarial networks,” in _2022 International Conference on Robotics and Automation (ICRA)_ . IEEE, 2022. 

- [41] J. Whitman, M. Travers, and H. Choset, “Learning modular robot control policies,” _IEEE Transactions on Robotics_ , 2023. 

- [42] M. Thosar, C. A. Mueller, G. Jäger, J. Schleiss, N. Pulugu, R. Mallikarjun Chennaboina, S. V. Rao Jeevangekar, A. Birk, M. Pfingsthorn, and S. Zug, “From multi-modal property dataset to robot-centric conceptual knowledge about household objects,” _Frontiers in Rob. and AI_ , 2021. 

- [43] W. Liu, D. Bansal, A. A. Daruna, and S. Chernova, “Learning instancelevel n-ary semantic knowledge at scale for robots operating in everyday environments.” in _Robotics: Science and Systems_ , 2021. 

- [44] C. Ben, F. Spencer, S. Mike, V. S. Thiago, and A. B. M. Lima, “What is holoportation?” https://www.microsoft.com/en-us/research/ 

   - project/holoportation-3/, Microsoft, May 2023, last accessed: 07-122023. 

- [45] Y. Wang, W. Huang, B. Fang, F. Sun, and C. Li, “Elastic tactile simulation towards tactile-visual perception,” in _Proceedings of the 29th ACM International Conference on Multimedia_ , 2021, pp. 2690–2698. 

- [46] Z. Sun, M. Zhu, X. Shan, and C. Lee, “Augmented tactile-perception and haptic-feedback rings as human-machine interfaces aiming for immersive interactions,” _Nature communications_ , vol. 13, no. 1, 2022. 

- [47] K. Takahashi and J. Tan, “Deep visuo-tactile learning: Estimation of tactile properties from images,” in _2019 International Conference on Robotics and Automation (ICRA)_ . IEEE, 2019. 

- [48] X. Zhu, Z. Li, X. Wang, X. Jiang, P. Sun, X. Wang, Y. Xiao, and N. J. Yuan, “Multi-modal knowledge graph construction and application: A survey,” _IEEE Transactions on Knowledge and Data Engineering_ , pp. 1–20, 2022. 

- [49] B. Otto and A. Burmann, “Europäische dateninfrastrukturen: Ansätze und werkzeuge zur nutzung von daten zum wohl von individuum und gemeinschaft,” _Informatik Spektrum_ , vol. 44, pp. 283–291, 2021. 

- [50] T. K. Rodrigues, K. Suto, and N. Kato, “Edge cloud server deployment with transmission power control through machine learning for 6g internet of things,” _IEEE Transactions on Emerging Topics in Computing_ , 2019. 

- [51] C. Dou, N. Huang, Y. Wu, and T. Q. Quek, “Energy-efficient hybrid noma-fdma assisted distributed two-tier edge-cloudlet multi-access computation offloading,” _IEEE Trans. on Green Comm. and Netw._ , 2023. 

- [52] A. Marshall, K. M. Yap, W. Yu _et al._ , “Providing qos for networked peers in distributed haptic virtual environments,” _Advances in Multimedia_ , vol. 2008, 2008. 

- [53] Y. Xu, L. Huang, T. Zhao, Y. Fang, and L. Lin, “A timestampindependent haptic–visual synchronization method for haptic-based interaction system,” _Sensors_ , vol. 22, no. 15, p. 5502, 2022. 

- [54] S. Mondal, L. Ruan, M. Maier, D. Larrabeiti, G. Das, and E. Wong, “Enabling remote human-to-machine applications with ai-enhanced servers over access networks,” _IEEE Open Journal of the Communications Society_ , vol. 2, pp. 889–899, July 2020. 

- [55] L. Ruan, M. P. I. Dias, and E. Wong, “Achieving low-latency humanto-machine (h2m) applications: An understanding of h2m traffic for aifacilitated bandwidth allocation,” _IEEE Internet of things journal_ , 2021. 

- [56] G. P. Fettweis and H. Boche, “6g: the personal tactile internet—and open questions for information theory,” _IEEE BITS the Information Theory Magazine_ , vol. 1, no. 1, pp. 71–82, 2021. 

- [57] Z. Hou, C. She, Y. Li, D. Niyato, M. Dohler, and B. Vucetic, “Intelligent communications for tactile internet in 6g: Requirements, technologies, and challenges,” _IEEE Com. Magazine_ , vol. 59, no. 12, pp. 82–88, 2021. 

- [58] L. Zhao, G. Zhou, G. Zheng, I. Chih-Lin, X. You, and L. Hanzo, “Opensource-defined multi-access edge computing for 6g: Opportunities and challenges,” _IEEE Access_ , 2021. 

- [59] K. Rusek, J. Suárez-Varela, P. Almasan, P. Barlet-Ros, and A. CabellosAparicio, “Routenet: Leveraging graph neural networks for network modeling and optimization in sdn,” _IEEE Journal on Selected Areas in Communications_ , vol. 38, no. 10, pp. 2260–2270, 2020. 

- [60] T. Mortlock, D. Muthirayan, S.-Y. Yu, P. P. Khargonekar, and M. Abdullah Al Faruque, “Graph learning for cognitive digital twins in manufacturing systems,” _IEEE Transactions on Emerging Topics in Computing_ , vol. 10, no. 1, pp. 34–45, 2022. 

- [61] A. Saxena, A. Jain, O. Sener, A. Jami, D. K. Misra, and H. S. Koppula, “Robobrain: Large-scale knowledge engine for robots,” _CoRR_ , vol. abs/1412.0691, 2014. 

- [62] M. Nickel, K. Murphy, V. Tresp, and E. Gabrilovich, “A review of relational machine learning for knowledge graphs,” _Proceedings of the IEEE_ , vol. 104, no. 1, pp. 11–33, 2015. 

- [63] W. Kinsner, “Digital twins for personalized education and lifelong learning,” in _IEEE Canadian Conf. on Elect. and Comp. Eng._ , 2021. 

- [64] X. Chen, M. Chen, W. Shi, Y. Sun, and C. Zaniolo, “Embedding uncertain knowledge graphs,” in _Proceedings of the AAAI Conference on Artificial Intelligence_ , vol. 33, no. 01, 2019, pp. 3363–3370. 

- [65] S. Orts-Escolano, C. Rhemann, S. Fanello, W. Chang, A. Kowdle, Y. Degtyarev, D. Kim, P. L. Davidson, S. Khamis, M. Dou _et al._ , “Holoportation: Virtual 3d teleportation in real-time,” in _Proc. of 29th sympos. on user interface software and technology_ , 2016, pp. 741–754. 

- [66] S. F. Langa, M. Montagud, G. Cernigliaro, and D. R. Rivera, “Multiparty holomeetings: Toward a new era of low-cost volumetric holographic meetings in virtual reality,” _Ieee Access_ , 2022. 

- [67] I. Viola and P. Cesar, “Chapter 15 - volumetric video streaming: Current approaches and implementations,” pp. 425–443, 2023. [Online]. Available: https://www.sciencedirect.com/science/article/pii/ B9780323917551000213 

- [68] M. Montagud, J. Li, G. Cernigliaro, A. El Ali, S. Fernández, and P. Cesar, “Towards socialvr: evaluating a novel technology for watching videos together,” _Virtual Reality_ , 2022. 

- [69] L. He, K. Liu, Z. He, and L. Cao, “Three-dimensional holographic communication system for the metaverse,” _Optics Communicat._ , 2023. 

12 

- [70] M. S. Elbamby, C. Perfecto, M. Bennis, and K. Doppler, “Toward lowlatency and ultra-reliable virtual reality,” _IEEE Network_ , 2018. 

- [71] H. Ren and P. Ben-Tzvi, “Learning inverse kinematics and dynamics of a robotic manipulator using generative adversarial networks,” _Robotics and Autonomous Systems_ , vol. 124, p. 103386, 2020. 

- [72] NVIDIA, “Nvidia omniverse - the platform for connecting and developing openusd applications.” https://www.nvidia.com/en-us/omniverse/, NVIDIA, Aug. 2023, last accessed: 07-12-2023. 

- [73] NVIDIA and BMW, “Omniverse at bmw - youtube video,” https://www. youtube.com/watch?v=6-DaWgg4zF8, NVIDIA, 2023, last accessed: 07-12-2023. 

- [74] M. L. Dag Lindbo, German Ceballos, “Next-generation simulation technology to accelerate the 5g journey,” https://www.ericsson.com/ en/blog/2021/4/5g-simulation-omniverse-platform, Ericsson, Apr. 2021, last accessed: 07-12-2023. 

- [75] F.-Y. Wang, R. Qin, X. Wang, and B. Hu, “Metasocieties in metaverse: Metaeconomics and metamanagement for metaenterprises and metacities,” _IEEE Transactions on Computational Social Systems_ , 2022. 

- [76] I. Technical Committee and J. S. . I. . 35.040.40, “Iso/iec 230051:2020 information technology media context and control part 1: 

Architecture,” https://www.iso.org/standard/73581.html, ISO Technical Committee ISO/IEC JTC 1/SC 29 ICS : 35.040.40, 2020, last accessed: 07-12-2023. 

- [77] J. Leng, X. Zhu, Z. Huang, K. Xu, Z. Liu, Q. Liu, and X. Chen, “Manuchain ii: Blockchained smart contract system as the digital twin of decentralized autonomous manufacturing toward resilience in industry 

   - 5.0,” _IEEE Transactions on Systems, Man, and Cybernetics_ , 2023. 

- [78] S. Ghirmai, D. Mebrahtom, M. Aloqaily, M. Guizani, and M. Debbah, “Self-sovereign identity for trust and interoperability in the metaverse,” in _2022 IEEE Smartworld, Ubiquitous Intelligence & Computing, Scalable Computing_ . IEEE, 2022, pp. 2468–2475. 

- [79] G. Xiong, T. S. Tamir, Z. Shen, X. Shang, H. Wu, and F.-Y. Wang, “A survey on social manufacturing: A paradigm shift for smart prosumers,” _IEEE Transactions on Computational Social Systems_ , 2022. 

- [80] U. Gustavsson, P. Frenger, C. Fager, T. Eriksson, H. Zirath, F. Dielacher, C. Studer, A. Pärssinen, R. Correia, J. N. Matos _et al._ , “Implementation challenges and opportunities in beyond-5g and 6g communication,” _IEEE Journal of Microwaves_ , vol. 1, no. 1, pp. 86–100, 2021. 

