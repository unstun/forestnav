---
citation_key: Farajtabar2024path
arxiv_id: 2407.02664
arxiv_url: "https://arxiv.org/abs/2407.02664"
title: "The path towards contact-based physical human-robot interaction"
authors_short: "Mohammad Farajtabar et al."
year: 2024
direction_tag: R_surveys
source: pymupdf4llm
converted_at: 2026-06-23T19:14:36Z
origin: ai+web
reviewed: false
---

## - - THE PATH TOWARDS CONTACT BASED PHYSICAL HUMAN ROBOT INTERACTION 

## **Mohammad Farajtabar** 

Department of Mechanical and Manufacturing Engineering University of Calgary `mohammad.farajtabar@ucalgary.ca` 

## **Marie Charbonneau** 

Department of Mechanical and Manufacturing Engineering University of Calgary `marie.charbonneau@ucalgary.ca` 

## **ABSTRACT** 

With the advancements in human-robot interaction (HRI), robots are now capable of operating in close proximity and engaging in physical interactions with humans (pHRI). Likewise, contact-based pHRI is becoming increasingly common as robots are equipped with a range of sensors to perceive human motions. Despite the presence of surveys exploring various aspects of HRI and pHRI, there is presently a gap in comprehensive studies that collect, organize and relate developments across all aspects of contact-based pHRI. It has become challenging to gain a comprehensive understanding of the current state of the field, thoroughly analyze the aspects that have been covered, and identify areas needing further attention. Hence, the present survey. While it includes key developments in pHRI, a particular focus is placed on contact-based interaction, which has numerous applications in industrial, rehabilitation and medical robotics. Across the literature, a common denominator is the importance to establish a safe, compliant and human intention-oriented interaction. This endeavour encompasses aspects of perception, planning and control, and how they work together to enhance safety and reliability. Notably, the survey highlights the application of data-driven techniques: backed by a growing body of literature demonstrating their effectiveness, approaches like reinforcement learning and learning from demonstration have become key to improving robot perception and decision-making within complex and uncertain pHRI scenarios. This survey also stresses how little attention has yet been dedicated to ethical considerations surrounding pHRI, including the development of contact-based pHRI systems that are appropriate for people and society. As the field is yet in its early stage, these observations may help guide future developments and steer research towards the responsible integration of physically interactive robots into workplaces, public spaces, and elements of private life. 

**Keywords** Physical human-robot interaction, Robot safety, Robot sensing systems, Robot learning, Motion planning, Compliant control, Robot Ethics 

## **1 Introduction** 

- While the integration of robots into human personal and social life is not universal yet, there is a noticeable trend towards expanding their role and presence. Considering the world’s aging populations and increasingly personalized lifestyles, alongside growing computational capacity, plus the emergence of artificial intelligence and machine learning ( **AI/ML** ), it becomes more and more probable that not only industrial, but also service and domestic robots will significantly impact our lives. Robotic technology is making its way into individuals’ social lives in different ways, such as social robots intended for companionship or interactive robots in public settings. Domestic robots performing household tasks, personal assistant robots, and wearable robotic devices designed to enhance daily activities are reshaping the way people approach their daily routines [1, 2]. 

From an industrial perspective, for example in the manufacturing, logistics and warehouse industries, the introduction of robotics has 

altered industrial paradigms, while contributing to the creation and restructuring of numerous jobs. Robots can bring efficiency, quality, consistency and safety to production lines by reorganizing processes and lowering costs [3, 4]. Similar impacts are soon expected in the agriculture, transportation, service, medical and retail industries, which are now experiencing a growing emergence of robotic technologies [5]. While simple, repetitive tasks that pose safety and health risks to people may be taken over by robots, humans still have significant roles to play. Nonetheless, over time, human involvement will require different sets of skills and responsibilities [6, 7]. 

When robots are programmed to perform hazardous tasks, they contribute to making work generally safer for humans [3]. With the use of robots in a common environment with humans becoming more widespread, new challenges are introduced in the escalatingly more complex field of human-robot interaction ( **HRI** ). HRI can be classified as ‘social’ ( **sHRI** ), for example when it consists of distanced visual or auditory and vocal interaction, it can be classified as ‘physical’ ( **pHRI** ) when a robot physically interacts with humans, or it 

The path towards contact-based physical human-robot interaction (Preprint) 

can be at once both social and physical [8]. Whether a robot is made socially or physically closer to humans, ensuring safety becomes critical. Currently, the most prominent ways to address physical safety directly involve robot perception, planning and control, while psychological safety has yet to be addressed through ethical and psychosocial frameworks. Each of these fields (perception, planning, control, ethics) are also central to the development of robots that can effectively perform their intended task while harmoniously physically interacting with humans. 

pHRI, and in particular _**contact-based**_ **pHRI** involving active, deliberate contact between humans and robots, is still in the early stages of development. There is however a growing, scattered body of literature on the topic. The contribution of this paper is therefore to provide a comprehensive and interconnected perspective on pHRI, encompassing technical, safety, and ethical challenges and considerations. The paper aims to provide a holistic understanding of the current research in contact-based pHRI, including background knowledge for new researchers in the field, while calling attention to challenges that have yet to be tackled. 

Numerous aspects come together to make robots that can directly physically interact with humans. This review will kick off by defining pHRI within the context of HRI in Section 2. Section 3 will then delve into the topic of safety, which we consider as the foremost challenge in pHRI, to explore how it has so far been addressed through strategies involving perception, planning and control, and leveraging the power of AI/ML. The paper then surveys the different ways in which robots that can effectively physically interact with humans have been developed. In Section 4, an extensive discussion of perception, including sensor development and human intent detection is presented. Planning approaches that have been proposed to carry out pHRI applications are explored in Section 5, and Section 6 covers robot motion control for contact-based pHRI, with special attention to the realization of variable compliance control schemes, stability, and AI/ML approaches. Section 7 discusses computational considerations, covering aspects related to both software and hardware perspectives. We additionally examine the ethical considerations that must be taken into account when designing and deploying robots that closely interact with humans in Section 8. Finally, Section 9 summarizes the current state of research in contactbased pHRI, leading to our identifying future trends and challenges that have yet to be addressed. 


![](1_survey/papers/md/Farajtabar2024path_figs/Farajtabar2024path.pdf-0002-04.png)



![](1_survey/papers/md/Farajtabar2024path_figs/Farajtabar2024path.pdf-0002-05.png)


**----- Start of picture text -----**<br>
(a) Classification by the degree of independence<br>(b) Classification by the degree of engagement<br>**----- End of picture text -----**<br>


Figure 1: Classifying HRI based on two factors. a) the degree of independence between human and robot actions, including coexistence: humans and robots occupy separate workspaces without any interference, co-operation: humans and robots share a workspace while working on their respective tasks, and collaboration: humans and robots share a workspace and simultaneously work together on a common task. b) the degree of physical and psychological engagement in the interaction. The four quadrants mark the division between social, physical, social-physical HRI and teleoperation. Each quadrant encompasses various forms of interaction along the co-existence-co-operation-collaboration spectrum. 

## **2.1 HRI categorized by degree of independence** 

## **2 Definitions of human-robot interaction** 

HRI can be defined as the study of how people interact with robots. It includes the design, development, and evaluation of systems that allow people to interact with robots in a natural and intuitive way. HRI research covers a wide range of topics, including humanrobot communication, user interface design, robot perception, robot autonomy, safety and ethics. The goal of HRI is to develop robots that can work alongside humans in a variety of settings, such as homes, workplaces, and public spaces. In general, HRI can be categorized from two perspectives: (A) the degree of independence between human and robot actions, or (B) the degree of engagement between a human and a robot. The next two subsections detail these two classification themes, and Fig. 1a provides a graphical representation. 

As shown in Fig. 1a, HRI can be divided among three broad categories of interaction: co-existence, collaboration, and co-operation, as explicitly introduced in [9], and further used in [3, 10, 11, 12] **Co-existence** refers to humans and robots operating in the same environment without mutual interference, emphasizing individual independence. An example of co-existence might be robots transporting goods in a warehouse where humans are doing the packing. **Co-operation** refers to coordinated teamwork with clearly defined roles and responsibilities for a human and a robot working within a shared workspace, but who do not engage in simultaneous work on the same item. An instance of this can be observed in a production line scenario where both partners sequentially manipulate an object. **Collaboration** involves humans and robots actively working together: sharing information, resources and decision making processes to achieve a shared goal, thus entailing a symbiotic de- 

2 

The path towards contact-based physical human-robot interaction (Preprint) 

pendence. An example of this could be a robot assisting a human by handing over objects or jointly carrying goods. 

## **2.2 HRI categorized by degree of engagement** 

HRI can be categorized into remote interaction and proximate interaction, as suggested in [13]: 

- Remote interaction: human and robot are separated spatially or temporally 

- Proximate interaction: human and robot are in the same location or environment 

As distance can be interpreted in either physical or psychological terms, Fig. 1b illustrates a division of HRI into four general quadrants relating to the degree to which interactions involve psychological and physical connections. 

**Social HRI (sHRI)** refers to the ability of a robot to engage with humans socially, which includes engaging in conversations and responding to emotional cues. There currently are two prevalent forms of social interaction: speech-based interaction, which involves using speech recognition and natural language processing for vocal communication, and visual-based interaction, which encompasses the recognition of gestures, body language, and the use of lights or displays for communication [14, 15, 16, 17]. For example, socially skilled robots can offer companionship to healthcare patients. A study conducted in [18] used a humanoid robot to assist children with autism in improving their body awareness and social interactions, demonstrating the potential effectiveness of robots as a tool to educate children with autism. In entertainment venues like theme parks and museums, robots have also been employed to engage visitors and enrich their overall entertainment experience [19, 20]. 

**Physical HRI (pHRI)** , in the opposite corner, involves robots and humans interacting with each other through different types of contact [3, 10, 11, 21], within a large range of applications and industrial settings [8]. pHRI is central to assistive technology, where it can be used to assist individuals with disabilities or older adults in achieving mobility or in carrying out daily tasks [22, 23, 24]. In healthcare, robots can play a crucial role through pHRI in medical procedures, surgeries, and physical rehabilitation [25, 26, 27, 28]. In manufacturing and industrial settings, pHRI can be leveraged to enhance productivity and safety by having robots perform dull, repetitive and dangerous tasks when working alongside humans [29, 30, 31, 32]. 

Within pHRI, distinct types of interaction can be identified, as shown in Fig. 2. These include: 

- Direct (contact-based) physical interaction: involves direct contact between human and robot, such as through touch or grasping, for example shaking hands [33], dancing [34], kinesthetic teaching [35], assisting humans in industrial tasks [32], in rehabilitation [24, 36], or in surgery[27]. 

- Indirect physical interaction: involves humans and robots interacting through the intermediary of objects, for instance when collaborating to achieve a common goal such as manipulating or moving objects together [37, 38], assembling a product [39], or handing objects over [40]. 


![](1_survey/papers/md/Farajtabar2024path_figs/Farajtabar2024path.pdf-0003-12.png)



![](1_survey/papers/md/Farajtabar2024path_figs/Farajtabar2024path.pdf-0003-13.png)



![](1_survey/papers/md/Farajtabar2024path_figs/Farajtabar2024path.pdf-0003-14.png)


**----- Start of picture text -----**<br>
(a) Direct interaction (b) Handover<br>(c) Co-manipulation<br>**----- End of picture text -----**<br>


Figure 2: Three different scenarios in pHRI: a) Dancing, leveraging direct physical contact, b) Handover task, where the robot transfers an object to the human, c) Co-manipulation, where the human and robot collaborate to accomplish a task through direct contact. Picture reproduced from [32] with permission. 

- Proximity interaction: involves the robot and the human working in close proximity to each other, but not necessarily in direct or indirect physical contact. For example, accomplishing complementary roles to collaboratively accomplish a task [41], or human-aware robot navigation in common environments such as warehouse and manufacturing [42, 43]. 

**Social-physical HRI** ( **spHRI** ) involves the integration of social and physical cues to establish human-like, engaging interactions between humans and robots. This form of interaction goes beyond verbal or visual communication by incorporating physical gestures, touch, and movement. 

In the service and hospitality industries, spHRI can lead to robots interacting and engaging with customers, taking and delivering orders and enhancing the overall customer experience [12, 19, 20, 44, 45]. In education, spHRI can facilitate teaching and learning of various topics. For instance, in [34], a robot is programmed to teach dancing skills, providing learners with social and physical feedback. Experiments conducted in [46] and [47] explored the use of robots in educational settings for children. The findings suggest that the presence of a robot acting as a teacher or tutor assistant, and which 

3 

The path towards contact-based physical human-robot interaction (Preprint) 

interacts socially or physically with children, can positively affect their interest in learning. 

Integrating the social and physical aspects of HRI can lead to increased safety and efficiency of robots that operate alongside humans, as suggested in [48]. This paper introduces a spHRI framework, by combining visual perception of humans, a robot controller that safely reacts before and after contact with humans, and data from people and objects perceived in the environment. 

**Teleoperation** consists of a more distanced type of HRI, where humans interact with robots remotely, e.g., remotely performing inspections through a telepresence robot, as described for example in [3, 10, 21]. Teleoperation can be merged into pHRI when augmented with haptics, or into sHRI when used to communicate with people through the intermediary of the teleoperated robot. 

One of the main challenges currently limiting the development of applications involving physical HRI is safety. When humans and robots engage in any of the interaction types described above, ensuring human safety indeed becomes a major challenge and a significant aspect of HRI [12]. The next section delves deeper into that topic. 

## **3 Safety** 

Prevention of accidents and injuries, whether physical or psychological, has long been and still is a key challenge in HRI. Traditionally, ensuring physical safety has required preventing any unintentional or unwanted physical contact between humans and robots, for example by establishing safety zones that isolate robots from humans. When physical contact is unavoidable or required for a specific task, as in some pHRI scenarios, the typical approach is to keep forces applied by the robot within a safe range. By ensuring psychological safety, one aims to create stress-free and comfortable HRI, for instance through the robot’s appearance, embodiment, gaze, speech, posture, and adherence to social conventions [3, 12, 22, 49]. 

Recent advancements in human physical and psychological factors, materials, sensing technology, motion planning and control, as well as the integration of AI/ML, have the potential to expand robot capabilities toward physically safe HRI [50, 51]. 

Researchers so far have formalized levels of damages and accidents that can occur through HRI [49, 52], along with suggested strategies for accident prevention and safety enhancement. After surveying literature on pHRI, one may categorize the array of proposed approaches into four main types of safety strategies, each addressed in the next four subsections: (3.1) robot design, (3.2) human prediction, (3.3) motion planning, and (3.4) control. 

## **3.1 Robot design** 

Robot design encompasses the physical design of a robot, its components, and the environment in which it operates [53, 54, 55]. Designing for safety can then be addressed from multiple angles, as detailed in the following subsubsections. One can enhance safety from the perspective of (3.1.1) ergonomics, as well as (3.1.2) social and psychological factors. In addition, one can minimize the risk of injury caused by collisions by designing (3.1.3) softer, lighter, and 

compliant robots, or minimize the risk of collisions through (3.1.4) sensing systems. 

## **3.1.1 Ergonomics and physical human factors** 

When it comes to robotics, ergonomics is typically focused on optimizing human well-being and robot performance through the analysis of interactions between humans and robots, often targeting to minimize the risk of work-related musculoskeletal disorders. To do so, an ergonomic assessment of the robot-human system throughout the design process will be crucial. To that effect, [56] introduced a method for detailed ergonomic assessments of collaborative robots, identified influential parameters to improve ergonomics and defined a robot design optimization algorithm based on their analysis. A different methodology optimizing robot hardware parameters with the objective of ergonomically minimizing energy expenditure, was developed and applied to a collaborative payload lifting task in [57]. 

To design ergonomic social and service robots, and make the environment in which they operate also ergonomic, a cross-disciplinary approach, bringing together roboticists, architects, and designers, was taken in [58], integrating a variety of factors such as human size, aesthetics, appropriateness and simplicity. Physical ergonomics is crucial for improving pHRI in repetitive tasks, such as industrial assembly. Guidelines are proposed in [59] for the design of safe and efficient human-centered collaborative assembly workstations, based on international standards, research, and real-world cases. In particular, the guidelines seek to mitigate 1) upper-body load during repetitive tasks, 2) whole-body load when lifting or lowering objects,and 3) whole-body strain when maintaining working postures. As pHRI is developed further, ergonomic close physical interactions will remain essential for physical safety, just as much as psychological safety will need attention. 

## **3.1.2 Social and psychological human factors** 

Social and psychological factors may often be overlooked in robot design. However, they play crucial roles in ensuring **perceived safety** , encompassing the feeling of safety and security conveyed to humans during pHRI [60]. It arises from factors such as comfort, predictability, transparency, sense of control, and trust [61]. Approaches aimed at enhancing psychological safety in pHRI typically focus on fulfilling these factors [22, 62]. Findings from [63, 64] suggest that individuals from diverse cultures may place varying levels of trust in robots. According to these studies a multitude of cultural aspects, including communication, attitudes, values, beliefs, expectations, technology levels must be considered to enhance trust and psychological safety in pHRI. The review in [65] investigated workers’ mental stress and safety awareness in human-robot collaboration, finding that it is affected by robot size, speed, trajectories and contacts with the robot. The impact of different robot behaviours on human discomfort, perceived safety, sense of control and distrust was explored in [61], with results indicating that perceived safety is also influenced by individual human characteristics (e.g., personality and gender), and that physiological signal data can be effective in measuring perceived safety. 

Thus, robot design, in terms of physical characteristics and interactive behaviours, significantly impacts perceived safety. One way to 

4 

The path towards contact-based physical human-robot interaction (Preprint) 

effectively increase how intrinsically safe a robot is to be around, is through robot structural design. 

## **3.1.3 Structural design and material selection** 

Enhancing safety involves prioritizing the development of robot hardware that is both user-friendly and inherently safer. In instances of collision, employing a compliant robot structure proves beneficial in minimizing potential harm to humans. Within the realm of robot hardware production, three key design elements are commonly emphasized to mitigate collision energy, whether interactions are deliberate or accidental: mechanical compliance in the robot’s links and actuators (referred to as passive compliance), the utilization of soft and energy-absorbing robot skin, and the adoption of lightweight manufacturing techniques for robots [66]. 

## _Mechanical compliance in robot links and actuators_ 

Safety in pHRI can be enhanced with the introduction of tunable stiffness robot links, as proposed in [67], where servo motors are used to adjust the stiffness of actuated four-bar linkages. Impact tests on this approach have revealed a significant reduction in acceleration and head injury criteria, indicating improved safety for operators during collisions. 

A compliant actuator can be defined as an actuator designed with a mechanically low impedance (for example through a spring), which therefore permits deviations from its equilibrium position, with minimal force or torque in response to external forces. In contrast, a stiff actuator would be designed with a high mechanical impedance, allowing it to remain fixed once it reaches a specific position, regardless of external forces (within the limits of the forces and torques it can widthstand) [68]. A notable example of compliant actuation is the use of series elastic actuators ( **SEAs** ), which has been proposed in collaborative robots to absorb collision energy and make interactions safer. Broadly speaking, SEAs are composed of a spring connected in series with a stiff actuator. The compliance of SEAs is fixed and determined by the spring constant, which cannot be adjusted during operation. In particular, this setup facilitates force control [69, 70]. Another example of compliant actuators is the variable stiffness actuator ( **VSA** ), designed with adjustable stiffness, rendering them suitable for safe pHRI. Their energy-efficient nature and adaptability to various tasks, environments, or conditions make them a promising option for robot actuation. This type of actuators generally comprise three pulleys, with two of them independently controlled by motors, linked to the joint via a timing belt [71, 72]. 

Passive compliance can also be attained through backdrivable transmissions, where external forces exerted between human and the robot is reflected in motor currents. This setup facilitates robust torque control, since the motor functions as a torque sensor. By colocating the sensor and actuator, it notably alleviates dynamic stability issues encountered in force control. Direct-drive ( **DD** ) and quasi direct-drive ( **QDD** ) actuators are two examples of backdrivable transmissions proposed in [73, 74]. 

## _Energy-absorbing robot skin_ 

Various implementations of energy-absorbing robot skins have been introduced over time, such as employing viscoelastic coverings [49, 75, 76], to reduce the potential impacts of collisions, while at the same time offering a tactile experience reminiscent of human skin. In [77], authors devised a soft skin incorporating pressurized airbags 

connected to a pressure sensor to identify the force exerted on the robot arm covered by the skin. Another instance of a soft skin equipped with tactile sensors to detect touch is introduced in [78]. The robot’s soft, hypoallergenic fur-covered skin ensures the safety of pHRI. Utilizing inherently soft skins without soft sensing components offers an alternative for swift and safe interaction, as there is no delay associated with force sensing. A soft inflatable robotic arm, such as the one introduced in [79], may be made inherently safe without requiring external force sensors, resulting in reduced delay in the control system. 

## _Lightweight robot manufacturing techniques_ 

Lastly, the design of lightweight structures, such as introduced in [80, 81], is another safety-oriented consideration aimed at minimizing injuries in the event of collisions with humans. Decreasing robot mass results in decreased momentum, thus reducing impact forces when accidental contact or collision occurs in pHRI [82]. As a result, using lightweight robots contributes to safety in pHRI by presenting a lower risk of injury in comparison to heavier, more traditional, robots. 

From there, to evaluate the extent to which a robotic system is safe, psychologically and physically, and to generate safe robot behaviours, sensors will be the crucial pieces of equipment to consider. 

## **3.1.4 Sensors** 

Sensors are critical in ensuring safe pHRI. A range of human physiological sensors may be used to evaluate perceived safety during pHRI [60]. Robot sensors, for their part, enable environment awareness and detection of human presence. Tactile, pressure, 6-axis force/torque ( **F/T** ) and joint torque sensors, as well as cameras, are commonly employed in this sense. Tactile sensors allow perception of human touch, while pressure sensors measure a force applied over a given area. An F/T sensor measures the resulting 3D forces and torques from wrenches applied to robot body parts situated distally from the sensor, while a joint torque sensor measures the 1D torque applied at a robot joint as a result of wrenches applied distally. Cameras, systems composed of stereo and/or range cameras as in [83], or RGB-D sensors, can be used to capture 3D information about a robot’s surroundings. These systems, when installed on a robot or in the environment, capture 2D images alongside depth information, allowing to map the distance between the sensor and objects in the environment, ultimately aiding in estimating human pose. 

Artifical skin sensors can also be developed to measure interaction forces on robot body regions, such as the pressure-sensitive skin introduced in [84]. Integrating a pressure sensitive layer with an energy absorbing layer, it can conform to complex shapes and reduce the risk of injury while measuring contact pressure during pHRI. In [85], an artificial robot skin is introduced, comprising an array of tactile sensor cells capable of detecting 3D acceleration, force, proximity, and temperature. Alternatively, [86] introduced flexible tactile sensors inspired by techniques from the clothing industry. 

The information provided by sensors can therefore be used for the implementation of safety measures that prevent potential harm to humans [32, 52, 87, 88], for instance through prediction of human movements, robot motion planning and control, as covered in the next subsections. 

5 

The path towards contact-based physical human-robot interaction (Preprint) 

## **3.2 Human detection and motion prediction** 

To ensure safety during pHRI, planning and control strategies often rely on an explicit evaluation of potential danger to humans, for example based on factors that influence collision impact forces such as relative distance and velocity between the robot and human and robot inertia [89]. From there, the ability to perceive human presence and behaviours around the robot can be another essential aspect to improving safety. 

Computer vision and learning approaches have been used to build a human model that estimates human pose and intention [90, 83]. In [91], a methodology is proposed to integrate vision and physiological sensor-based data on the user’s position and physiological responses into medium and short-term safety strategies. Another framework to generate safe robot motions is introduced in [92], based on early human motion recognition using a Gaussian Mixture Model ( **GMM** ), and human motion prediction using Gaussian Mixture Regression ( **GMR** ). In [93], the authors proposed a method for predicting human arm motion for safe interaction using a red marker attached to the arm of a human tracked by cameras. Using data from experiments, a topological map is created, and arm velocities are estimated through a hidden Markov model ( **HMM** ). Likewise, [94] introduces a framework for predicting human arm motion during a reaching task. It integrates partial trajectory classification and human motion regression, enabling action recognition and trajectory prediction before completion of the movement. Combining computer vision with deep learning can also help handle the complex nature of human models. [95] presents a mixed reality system for safe human-robot collaboration using deep learning and digital twin technology. It measures real-time safe distances, provides task assistance, and integrates mixture regression with safety monitoring using RGB-D cameras. 

In particular, detecting human intention and predicting motion through gaze plays a crucial role in fostering successful and safer interactions. Gaze offers nuanced cues that facilitate smoother communication between individuals. By integrating predictions based on human gaze, it becomes possible to gauge the level of engagement during human-robot interactions, enabling the robot to anticipate the intentions or objectives of the human participant [96, 97]. In collaborative interactions between humans and robots, the utilization of gaze tracking and eye monitoring can contribute to anticipating the human operator’s workload and performance levels throughout the task [98, 99]. 

Along the same line, [32] integrates vision and tactile sensors information and identifies touch location, human pose, and gaze direction, and uses that information to train a machine learning algorithm which classifies intentional and unintentional touch. Alternatively, in [100], signals from F/T sensors are combined with motor currents to differentiate accidental collisions from intentional ones. This information has been shown in both [32, 100] to be instrumental in appropriately adapting robot behaviour for safe pHRI, for instance through motion planning and control. 

Collision-based detection, i.e., identifying when a robot comes into contact with humans in its workspace, can also be crucial for safety. For instance, the authors in [101], developed and evaluated two distinct collision detection approaches: a disturbance observer, and a robot torque observer. Broadly speaking, collision detection meth- 

ods based on observers, like those mentioned above or a momentum observer, offer utility as they remove the need to solve the inverse dynamics problem [102]. Once a collision has been detected, the actions of the robot must then be adjusted for safety, making use of appropriate motion planning and control approaches. From there, human state information is vital for the introduction of a safety strategy, typically relying on planning. 

## **3.3 Motion planning** 

Going beyond collision prevention at the control level, real-time human-aware motion planning has been shown to improve physical and psychological safety in HRI [22, 103, 104]. For instance, [105] introduces a human-aware planner for robot handover tasks, which determines handover location based on factors including human kinematics, field of vision and personal preferences, thus reducing human cognitive load and increasing comfort and efficiency. To enhance safety and robot predictability, a motion planning cost function is proposed in [106], taking into account avoidance of previously occupied workspace by human, and robot motion consistency. Instead, a human model is integrated into robot path planning in [107], with the objective of minimizing path execution time while slowing down and stopping when humans are in proximity. This is achieved by defining speed limits as configuration-space cost functions based on observed and predicted human states. 

Although most planning approaches focus primarily on pre-collision strategies, such as in [108, 109], when contact is expected or unavoidable, motion planning must adeptly manage contacts to ensure safety. Traditionally, this has been viewed primarily as a control problem, but integrating contact handling into trajectory planning can lead to more sophisticated and human-friendly interactions [110]. The idea introduced in [101] for post-collision robot reaction involves retaining the original motion path, while also incorporating compliant behaviour through adjustments in the timing of the intended trajectory, in response to a collision. 

In [111], a reactive planner is proposed, in addition to pre-collision planning. This reactive planner determines the course of action during a collision: end-effector motion is stopped and, a new internal model is created based on the time evolution of contact forces, and then the new destination for retraction is obtained. 

A model-based trajectory planning algorithm is introduced in [112] for rehabilitation and physical therapy robotics, alongside a framework incorporating a human musculoskeletal model to evaluate patient conditions and perform physical therapy movements safely with a wide range of robot motions. An example of safe real-time motion planning allowing legged humanoid robots to safely engage in physical interaction with humans is furthermore introduced in [113], focusing on the dynamical planning of bipedal walking trajectories and adapting steps for successful push recovery. 

Nonetheless, safe and human-aware robot motion planning may not be sufficient to guarantee safe pHRI: motion control also needs to be considered. 

## **3.4 Control** 

Several control strategies can be adopted for safety during pHRI, including acting (3.4.1) before and (3.4.2) after a collision occurs, 

6 

The path towards contact-based physical human-robot interaction (Preprint) 

or (3.4.3) ensuring robot compliance at all times, and (3.4.4) stabilization of unstable robots. 

## **3.4.1 Pre-collision strategies** 

These techniques involve monitoring either the human, the robot, or both, and adjusting robot control parameters before a collision or contact occurs. The objective is to proactively modify the robot’s behaviour to prevent potential accidents and ensure a safe HRI environment [12]. For example, [91] designed a motion planning and control approach which relies on an explicit estimate of the danger level during the interaction, taking into account measured human heart rate, skin conductance and contraction of facial muscles. 

Adopting a different approach, [89] proposes a controller which maintains robot velocity within dynamic bounds, determined based on robot dynamics and configuration, as well as an estimate of injuries that may be incurred in the context. Seeking instead to balance safety and productivity while leveraging robot redundancy, [114] proposes a controller in which robot velocity is scaled within a safety region defined based on its current velocity and braking distance. 

Extensive efforts to prevent collisions and minimize the associated risks may not entirely eliminate the occurrence of collisions. Consequently, post-collision strategies are just as essential to reduce the severity of injuries. 

## **3.4.2 Post-collision strategies** 

Post-collision safety strategies may include designing robots with compliant and soft materials that can absorb impact forces and reduce the risk of injury upon collision with a human, as discussed in 3.1.3. Another approach may be to design robots with sensor systems that can detect collisions or contacts in real-time. Upon detection, the robot can stop moving or dynamically adjust its behavior to minimize any harm or damage [49]. 

A common approach to mitigate collisions is to adjust control parameters based on joint torque and encoder signals, as presented in [115, 116, 117]. One can also leverage signals from an F/T sensor mounted at the robot end-effector: for instance, [100] uses measured F/T signals in combination with motor currents, to differentiate accidental collisions from intentional contacts. Robot response is then adapted in consequence to ensure safety, e.g., by interrupting any motion after accidental collision, or by ensuring robot compliance to intentional contact as described next. 

## **3.4.3 Compliant control** 

In articulated collaborative robots, signals from F/T sensors, joint encoders and torque sensors as mentioned above, or even artificial skins [118, 119], may be instrumental in developing robot motion controllers that are compliant to physical interactions and safe for pHRI (i.e., active compliance). 

Passivity, or maintaining the energy stored within system elements (comprising kinetic and potential energy) lower than the input energy, is crucial for ensuring stability, and consequently, safety [120]. Within this context, passivity-based approaches designed to guarantee compliant controller stability during physical interactions are highly useful for safety. However, passivity alone may not directly address the need to maintain safe robot configurations, velocities, 

power and interaction forces. This is for example addressed in [121], where a robot controller is designed to maintain motion within safe position and velocity regions, while ensuring passivity during pHRI. Alternatively, in [122] and [123], a variable admittance control approach is introduced based on principles of passivity, allowing to adjust admittance parameters (damping, inertia, and stiffness) in such a way as to limit interaction forces, thus enhancing safety during pHRI. 

Compliant control is currently the most common control approach in pHRI, being employed beyond the single purpose of ensuring safety. For this reason, Section 6 will delve deeper into the subject. 

## **3.4.4 Stabilization** 

While the strategies outlined in subsections 3.1.3, 3.1.4, 3.2, 3.3, and 3.4 of the current section on Safety contribute to the safety of both the human and robot, another strategy consists in primarily enhancing the safety of the robot itself. Such a strategy is especially relevant for locomoting robots that are not passively stable, such as humanoids and ballbots. Introducing compliance (either passive or controlled) in such robots is likely to compromise their balance, along with their ability to prevent falls or tipping over, especially when subjected to external forces. Therefore, incorporating stabilizing control algorithms (e.g., stabilizers such as introduced in [124]) into the control framework is essential to ensure safety during pHRI, preventing the robot from collapsing and either breaking itself or injuring a human through its fall. Exploring this issue, [125] presented a control strategy, adapted for a human-assisted robot sit-to-stand scenario, which takes into account interaction forces applied to a compliantly torque-controlled humanoid robot, when computing control inputs that track a desired center of mass trajectory. Contrastingly, [126] introduced an impedance control framework allowing a ballbot to maintain balance in a robot-assisted human sit-to-stand scenario. Another framework was proposed in [127] for indoor service ballbots, offering physical aid and dynamic guidance to individuals navigating congested and tight spaces. To maintain balance, the robot employs a balancing PID controller to mitigate disturbances and uphold the desired roll and pitch angles of the body. 

In [128], an approach to close multi-contact physical interaction between human and humanoid robots was introduced. The proposed controller, based on the divergent component of motion [129], maintains balance while stepping by considering pHRI forces as disturbances. 

As control makes heavy use of perception data, the topic of perception will first be covered in Section 4. 

## **4 Perception** 

In HRI, awareness can be defined as the human’s perception and understanding of a robot’s location, activities, status, and surroundings and vice versa [130]. The robot relies on information about the human’s commands or instructions to guide its actions within specific conditions and limitations. Insufficient awareness significantly hampers the level of interaction, resulting in a notable decrease in overall task performance, when human-robot collaboration is re- 

7 

The path towards contact-based physical human-robot interaction (Preprint) 

quired [130]. To organize our analysis, we divide the robot perception and control chain in pHRI into four main modules [131, 132]: 

- A. Sensor development: gather information from the environment through various sensors 

- B. Sensory data integration: build a representation of the environment, users, and interaction forces 

- C. System modelling: develop models to analyze the integrated data and predict future states of the system 

- D. Planning and control: implement robot decision policies based on optimization, and command robot motion to achieve a given task 

The following subsections address modules A, B, and C to provide a comprehensive exploration of perception in pHRI, while module D will be the topic of Sections 5 and 6. 

## **4.1 Sensors for pHRI** 

This subsection covers the development and use of the main sensors used for contact-based pHRI. A handful of sensors count as the most commonly used to measure physical interactions: joint torque, F/T, tactile, cameras and depth sensors, but other types of sensors have also shown to be useful. 

Figure 3 shows sensor configurations for pHRI on different robots. 

Data from **joint torque sensors** relates directly to the forces exchanged in pHRI, e.g., as leveraged in [25]. When a robot is equipped with joint torque sensors, it is common practice to use the measured torques as feedback in compliant joint torque control laws adapted for pHRI, as surveyed in [133], and implemented in [134, 36]. 

**F/T sensors** mounted on robot end-effectors are widely employed to measure contacts during pHRI and to implement compliant control algorithms [135, 136, 137, 138]. 

A variety of **tactile sensors** have been developed and employed specifically for pHRI. On/off tactile sensors have been used to detect human touch or proximity, for example in [139], where they allow humans to communicate desired whole-body motions of a humanoid robot through direct pHRI. A Hall effect-based sensing module has been developed to measure forces along 3 axes in [140] and was shown to measure interaction forces when installed on robot fingertips. The sensor module was later modified to allow force sensitivity adjustments during operation, and augmented with capacitive sensing for proximity measurements [141], thus also allowing to detect an approaching object before contact occurs. In [142], an artificial skin composed of an array of pressure sensors was used to recognize human hand touch by projecting the 3D pressure distribution onto a 2D image, and classifying hand shapes through machine learning. A sensor array composed of large flexible 1-D capacitive tactile sensors was developed in [143] to cover the base of a mobile robot, allowing to measure interaction forces while safely engaging in pHRI with the robot base. Thousands of conformable capacitive sensors disposed in arrays are also used to cover large areas of humanoid robots [86]. For the same purpose, a multi-modal modular artificial skin was introduced in [144], for which each unit includes proximity, normal force, acceleration and temperature sensing. It has shown multiple times to facilitate pHRI, e.g., in [144, 145]. 


![](1_survey/papers/md/Farajtabar2024path_figs/Farajtabar2024path.pdf-0008-13.png)



![](1_survey/papers/md/Farajtabar2024path_figs/Farajtabar2024path.pdf-0008-14.png)



![](1_survey/papers/md/Farajtabar2024path_figs/Farajtabar2024path.pdf-0008-15.png)



![](1_survey/papers/md/Farajtabar2024path_figs/Farajtabar2024path.pdf-0008-16.png)


**----- Start of picture text -----**<br>
(a) F/T sensor (b) RGB-D sensor (c) Laser range sensors<br>**----- End of picture text -----**<br>



![](1_survey/papers/md/Farajtabar2024path_figs/Farajtabar2024path.pdf-0008-17.png)



![](1_survey/papers/md/Farajtabar2024path_figs/Farajtabar2024path.pdf-0008-18.png)



![](1_survey/papers/md/Farajtabar2024path_figs/Farajtabar2024path.pdf-0008-19.png)



![](1_survey/papers/md/Farajtabar2024path_figs/Farajtabar2024path.pdf-0008-20.png)


**----- Start of picture text -----**<br>
(d) Tactile sensors (e) Pressure sensors (f) RGB-D sensor<br>**----- End of picture text -----**<br>


Figure 3: Sensors commonly employed for pHRI: a) F/T sensor mounted on the wrist of the REEEM-C robot, b) RGB-D sensor mounted on the REEM-C head, c) Laser range sensor embedded in each foot of the REEM-C, d) Tactile sensors on the NAO robot: capacitive sensors at the head and hands; on/off bumpers on each foot, e) Flexible resistive pressure sensors mounted on a glove, f) RGB-D sensor mounted on the MOVO robot. 

Instead of using an array of sensor modules to sense simultaneous contacts in different locations, [146] introduced a flexible sensor sheet embedded into flexible polyurethane that can do just that, while absorbing collisions. Along the same line, the artificial skin introduced in [147] uses projected mutual capacitance to measure forces applied by multiple contacts, while reproducing the mechanical properties of human skin (Fig. 3d). With the emergence of wearable sensing, continuous advancements in the development of electronic skin can be expected over the coming years [148]. 

The combination of **cameras and depth sensors** can produce detailed 3D representations of a robot’s surroundings [149], and can also be used to detect human touch. Approaches to estimate contact forces without the use of torque or force sensing have also been developed, such as the one introduced in [150]. In this paper, contact forces are estimated given (i) joint torques due to contacts estimated based on the robot’s dynamic model and given joint positions measured by encoders, as well as the control torques, and (ii) contact locations estimated from images captured by an external depth sensor pointed toward the robot. This approach relies on the concept of the generalized momentum observer [151], calculating change in robot momentum following external disturbances such as contacts with humans. 

As **vision-based tactile sensors** have been materializing for robot manipulation, the concept was extended to a vision-based artificial skin in [152]: in this design, a camera is used to capture the de- 

8 

The path towards contact-based physical human-robot interaction (Preprint) 

formation of a flexible skin covered with a dot grid pattern, thus allowing for 3D force sensing. 

Less ubiquitous, **proximity sensors** , e.g., LIDAR, detect the presence of nearby entities. However, proximity sensors may not provide detailed enough data to identify what object or human body part is detected, or to predict their motion. 

**Biometric sensors** are sometimes used in pHRI. For example, electromyography ( **EMG** ) sensors capture muscle activity: their signals have been used to estimate interaction forces during pHRI [153], and to modulate compliant controller parameters [154]. Electroencephalography ( **EEG** ) sensors capture brain activity in braincomputer interfaces. They have been used to predict motion intentions in assistive robotics, including wearable robotic limbs [155]. 

**Inertial Measurement Unit** ( **IMU** ) sensors typically combine accelerometers, gyroscopes and sometimes magnetometers. They may be installed on a robot to track its motion, or, more often in pHRI applications, they are found in wearable sensors to measure the motion of the human body parts they are placed on. They are therefore commonly used for human motion tracking during pHRI, such as in [156, 157]. 

As another option, **audio sensors** such as microphones capture sound waves and convert them into electrical signals that can be processed by robots. Taking advantage of AI/ML techniques, data captured by audio sensors can be used to detect and localize sound sources, parse speech and spoken commands [158], or even detect emotions or intents from human voice signals. [149] further details the different uses of audio sensors in HRI. Audio sensing can therefore enable humans to communicate with robots through speech or sounds. Audio and visual signals can also be combined for richer human-robot communication, as in [159]. 

## **4.2 Sensory data integration** 

Within the context of HRI, sensor integration, or fusion, refers to the process of combining data from different types of sensors to generate a more comprehensive perception of the environment than would be obtained with a single type of sensor. The sensory data integration process in pHRI can be divided into two main components, as suggested in [149]: (1) spatial perception of the environment, task objects and humans, for example fusing visual and depth sensor data, and (2) contact-based perception of the workspace, task objects and humans, for instance fusing F/T, joint torque and tactile sensor data. These two components can then be used separately, or further integrated together. In either case, three levels of data fusion can be defined, following [160]: 

- Data-level fusion: raw data from multiple complementary sensors is combined. E.g., combining tactile sensor data and visual data from a camera to differentiate human from non-human contacts. 

- Feature-level fusion: features from sensor data are extracted separately, before being combined. E.g., combining human poses and facial expressions extracted from visual data from a camera, with wrenches obtained from F/T sensor readings, to infer human intentions. 

- Decision-level fusion: raw sensor data is processed to extract features that separately result in different outputs of 

the robot decision process, which are then combined. E.g., combining a target end-effector configuration determined given the pose of an object obtained from camera data, together with desired end-effector displacements determined from wrenches measured by F/T sensors, to generate appropriate robot motions. 

The reader is referred to [160], Table 5, for a schematic representation of each level of data fusion. 

In multiple pHRI applications, data integration can be accomplished without explicitly leveraging data fusion for motion control. For instance, human posture estimated from camera data, contact forces by F/T sensors and contact locations by tactile sensors can be directly used to define a variable impedance/admittance controller [32, 161, 162], a controller combining visual servoing and impedance control [163], or simply to recognize human activity [29]. For an example from the rehabilitation robotics field, EMG data is used in [164, 165] to predict human joint torques and adjust parameters of an admittance controller for a gait rehabilitation exoskeleton. 

## **4.3 System modelling** 

System modelling for pHRI is often centered on interpreting human motions and interaction forces. As exposed in [166], strategies to do so can fall into one or a combination of the following three main categories. 

1. Model-based strategies: rely on precise mathematical models of the robot and the task, 

2. Human-based strategies: reproduce communication patterns observed in human-human interactions, 

3. Learning-based strategies: leverage AI/ML algorithms to generate models based on data. 

In particular, AI/ML approaches have been shown to contribute toward making pHRI safer and more effective, by enabling human motion identification and prediction [167]. For instance, multiple algorithms and frameworks are now available to accurately estimate 2D or 3D human pose in real-time [168, 169, 170, 171]. Among those frameworks, one of the most widely used is OpenPose [172], an open-source system which can detect the pose of bodies, feet, hands and facial keypoints from multiple people, given 2D visual data; further developments now allow for 3D pose estimation. For example, [173] compared the effectiveness of different 2D human pose detection methods and their extension to 3D for close pHRI, with a specific interest in hand detection for pHRI. Fig. 4, illustrates an instance of human body keypoint (e.g., head, eyes, arms, hands) detection and 3D pose estimation. 

In [92], human motion is modelled using a Gaussian mixture model, and then predicted through Gaussian mixture regression. This information is in turned used to predict areas of the robot workspace that will be occupied by a human. In [32], a supervised ML model is trained to classify intentional and unintentional human touch based on touch location, human posture and gaze direction. For example, in [174], a robotic arm holding a rigid endoscope was developed to be controlled by a surgeon’s eye movements, eliminating the need for a camera assistant. Gaze gestures, detected through eye movements, signal the surgeon’s intention for camera control. In [175], 

9 

The path towards contact-based physical human-robot interaction (Preprint) 


![](1_survey/papers/md/Farajtabar2024path_figs/Farajtabar2024path.pdf-0010-01.png)


Figure 4: Human body keypoint detection using RGB and depth sensors. Reproduced with permission from [173]. 

human intention is deduced from gaze direction and physical cues provided through direct manual interaction with the robot. 

Relying on human pose detection, real-time human gesture recognition has then been made possible. For example, [176] trained a convolutional neural network ( **CNN** ) from hand localization data to detect hand gestures used to communicate actions to the robot. This work was further extended in [177] to reduce the influence of image background. 

Alternatively to vision systems, wearable systems based on IMU can also be leveraged for human posture and gesture recognition. For instance, [178] introduces a framework for this purpose, which is further experimentally compared with visual measurements in [156]. Wearable IMU-based sensors have been used in [179] to estimate human internal accelerations and torques when assisting a robot in a direct pHRI scenario. In a scenario where the robot is leading pHRI, [180] models the human based on a digital human model, and training Gaussian processes to predict human postures, given the planned trajectory of the robot and the current human posture measured by a wearable system. 

Another common approach to predict interaction forces in pHRI is to use surface EMG signals, such as in [153], where a deep CNN model is trained to output predicted interaction forces, given EMG signals. 

Physical interaction data can also be beneficial to human motion and gesture recognition in pHRI. For instance, [181] introduces an approach where a multi-class classifier is trained on human-human interaction data to identify human intention to start, accelerate or stop walking based on motion and interaction force data. A radial basis function neural network is trained in [182] to predict the velocity of a human in contact with the robot at a single point, given the normal contact force, position and velocity of the contact point. 

In the absence of tactile sensors, AI/ML approaches have been used to estimate contact forces, such as the radial basis neural network proposed in [183]. Authors in [25] and [26], used time series CNN algorithms to detect the forces applied by a surgical tool, based on visual data showing soft-tissue deformation and the deformation of the surgical tool. 

## **5 Planning** 

To ensure safe, efficient pHRI, robot motion planning must include human presence and physical interaction awareness. More specifically, pHRI can be considered as a multi-agent sequential decision problem. Two agents (the human and the robot) select actions based 

on their given policies, working in coordination with each other to accomplish a shared objective [184]. While subsection 3.3 introduced planning specifically for safety in pHRI, the present section will focus on motion planning approaches for effectively carrying out pHRI. 

As discussed above, human awareness can be achieved using different types of sensors, and human motions can be predicted through various approaches leveraging the captured data. Robot motions can then be adapted, given these predictions. Typical conventional robot motion planning approaches aim to find feasible paths between initial and final configurations, and avoid obstacles in a known environment. However, to address path planning in complex and dynamic human environments, optimization-based, probabilistic and data driven approaches are more commonly used. For example, flexibility in planning can be achieved through feedback motion planning, i.e., continuously updating a desired path towards a goal configuration [185]. One approach to do so is through a model predictive control ( **MPC** ) framework as proposed in [186, 187], which enables navigating around dynamic obstacles during the execution of a pHRI task. 

Within the context of HRI, one approach to generating robot trajectories may be to mimic human-human interactions. This is for example explored in [188], where human negotiation gestures are reproduced in robot trajectories, in a scenario where human and robot need to settle who grabs an object both are reaching for. However, pHRI may often require planning complex motions. When coupled with complex robot dynamics, **model-based planning** approaches as described above may require extensive computational resources, compromising the real-time responsiveness of the system. As an alternative, **learning-based planning** approaches have become more prominent over time. 

When it comes to motion planning, learning from demonstration ( **LfD** ) often involves pHRI, as synthesized in [189]. In particular, kinesthetic teaching allows LfD by moving a robot through direct pHRI. A spatiotemporal LfD frameowrk, in which direct pHRI is modeled based on Bayesian interaction primitive, is developed in [157]: it predicts appropriate robot joint trajectories and contact forces, given the current human pose and forces applied to the robot during social-physical interaction. The concept has been applied to rehabilitation therapy in [28]: a model of the assistive forces applied by the therapist throughout a task is obtained, given interaction force and motion data from kinesthetic teaching demonstrations. LfD is also used to adapt robot motions to different human partners and new interactions, e.g. as in [40], where human and robot movements during interactions are correlated by modeling HRI patterns from unlabeled demonstrations, using Gaussian mixture models of interaction primitives. 

Movement primitives, as introduced in [190], are commonly used alongside LfD to represent robot movements or generalize trajectories from demonstrations. The concept is extended in [191] to pHRI primitives, which estimate user intent from interaction forces. Additionally, LfD approaches commonly involve decomposing a complex task into multiple relatively easy sub-tasks, e.g., in [192], unstructured demonstrations are segmented into sub-skills, based on dynamic movement primitives and HMMs. In a similar way, [193] extracted a set of action primitives from a demonstrated sequential task, resulting in a probabilistic representation of the sequence of ac- 

10 

The path towards contact-based physical human-robot interaction (Preprint) 

tions required to complete the task. The authors in [194] employed the concept of dynamic movement primitives to characterize the interaction and learn the robot’s trajectories in real-time through contact-based pHRI. 

Inverse reinforcement learning ( **IRL** ), or intention learning, is a subset of LfD approaches in which the robot, instead of learning demonstrated motions, learns a reward function. In particular, [42] leverages this concept for the kinesthetic teaching of a mobile robot: given direct pHRI forces, IRL is used to adapt parameters of a navigation cost function, ultimately correcting robot trajectories. Similarly, collaborative arm trajectories are adapted online through IRL in [195], where appropriate corrections to the objective function are learned, given interaction forces. 

## **6 Control** 

The choice of appropriate control approaches is a key factor in the safety and effectiveness of pHRI applications. When a human and a robot are closely working together, task execution and control is likely to be shared between them (e.g. the human may be controlling end-effector position, while a robot controller maintains its orientation), leading to the concept of **shared control** . An overview of the topic oriented towards pHRI can be found in [196], where central themes include the division of control and communication between human and robot. Integrating latest AI/ML techniques allows for greater flexibility in shared control of pHRI, as suggested in a recent survey [197]. These advancements have paved the way towards the concept of **shared autonomy** , where robots can be programmed to dynamically adapt their autonomy level in function of context. For example, a robot can have a lower level of autonomy when performing tasks that require human input, and higher autonomy for repetitive tasks. 

Controlling robot motions to be compliant to physical interactions is also a common approach in pHRI, as documented in [198]. While control techniques for safety have been discussed in 3.4, this section discusses recent advancements in control adapted to direct pHRI, with a focus on compliant control for collaborative robotic arms. Inherent instability in robots like humanoids and ballbots necessitates additional attention to stability when engaging in contact-based pHRI, a topic that will also be addressed in this section. 

Compliance in a robot can typically be achieved through: **Passive compliance:** 1) leveraging inherent flexibility in the mechanical structure of the robot and 2) employing compliant actuators, e.g. series-elastics or pneumatic actuators. 

**Active compliance:** defining control laws modulating the resistance of the robot to external forces or torques, such as admittance and impedance control laws. 

Utilizing compliant control (active compliance) allows robot actions to be adjusted in response to external forces, thus promoting safety and mitigating the potential for injury [199, 198]. With its versatility, this software-driven method can be implemented across diverse applications, bolstering safety measures and facilitating effective interaction in scenarios involving pHRI. 

The mechanical impedance of a structure (such as the body of a robot) relates the force acting on it to its displacement (or velocity), 

indicating how the structure resists external forces [200]. Put simply, it is the ratio of the displacement at the specific point on the robot where the force is applied by the magnitude of the applied force. Conversely, admittance, the inverse of impedance, is the ratio of applied force to displacement at that point. Admittance takes force as input and provides displacement (or velocity) [201]. It is noteworthy that these concepts can be described in either Cartesian space or joint space. 

The parameters of mechanical impedance/admittance (inertia, stiffness, and damping) serve as metrics to measure a robotic system’s resistance to motion when subjected to force by a human, such as at its end-effector. In other words, in compliant control, the robot’s force/motion in response to external motion/force is controlled by representing the robot as an impedance/admittance element and fine-tuning its parameters. In recent years, these types of controllers have risen as notably efficient techniques in the pHRI realm. 

For example, admittance control is used in [202] to generate safe robot motion control during pHRI, while robot trajectories are obtained with a model predictive control approach that considers the progression of a predefined task. Instead, impedance control is used in [203] to ensure compliance to external interaction, while reinforcement learning is used to identify if a human is leading or following in the completion of a task requiring pHRI. Authors in [204] proposed an adaptive tracking controller that relies on the modified function approximation technique to estimate the uncertain dynamics of an exoskeleton robot and reach a compliant control in a contact-based pHRI. 

One of the main research directions in compliant control for pHRI is in modulating the stiffness, damping and inertia of the robot during operation, i.e., **variable impedance (VI) and variable admittance (VA) control** schemes. In particular, [205] provides a comprehensive discussion of admittance control for pHRI and its distinction from impedance control. Since the concept was introduced in [206], strategies have been developed based on various control inputs and feedback as reported in [207], and further synthesized in Table 1. 

|**Approach**|**Control commands generated based on**|
|---|---|
|Velocity-<br>based<br>Force-based<br>EMG-based<br>Stability-<br>based|joint, end-effector, or base velocity<br>wrenches at the end-effector or other inter-<br>action forces on the body of the robot<br>EMG signals from human operator muscles<br>stability margins of the controller, given in-<br>teraction dynamics|



Table 1: Strategies for admittance or impedance variation 

Various methods for adjusting VI and VA control parameters, such as adaptive control and other conventional control strategies, as well as stabilization approaches, are addressed in subsection 6.1. 

Often, robots interacting with humans require more intelligent behavior than passively following interaction forces. AI/ML algorithms make it possible to handle a range of pHRI scenarios by programming complex robot behaviours, given data from sensors measuring pHRI [51]. The next subsections will cover how AI/ML 

11 

The path towards contact-based physical human-robot interaction (Preprint) 

algorithms have been applied to VA and VI control in pHRI applications. We focus in particular on more artificial neural networks in 6.2, deep learning in 6.3, reinforcement learning in 6.4, and learning from demonstration in 6.5. 

## **6.1 Traditional control** 

A VA control approach is introduced in [199], combining a force sensor and a force observer to safely allow a human to physically guide a robot making contact with objects of unknown stiffness. Several VA control laws for direct pHRI were explored in [122], relying on interaction forces and velocity for control parameter modulation. The control laws also ensure passivity through power envelope regulation, which bounds within a safe range the power injected into the system by interaction forces. 

In [208], the argument is made that when a robot is controlled with an admittance control law, a force feedback is generated during direct pHRI by a combination of the robot motion and the human hand impedance, which distorts the measured interaction forces. The paper therefore introduces a variable hand impedance compensation scheme. Instead, [209] argues that since admittance controllers rely on the inverse kinematics or the Jacobian, they require a highly accurate model of the robot for precision. As an alternative, the paper introduces admittance control methods based on end-effector orientations. 

As for impedance control, a velocity-based VI controller, with proven stability and convergence given uncertain contact impedance characteristics, is proposed in [210]. The problem of model uncertainty is addressed in [200], with the introduction of four different model reference adaptive impedance controllers. 

When addressing the control of inherently unstable robots in pHRI, the control challenge is broadened by accounting for the human’s present state, predicting their future state, and preserving stability through concurrent motion and contact control. Predicting the human’s future state entails estimating their motion intentions. Essentially, the issue in pHRI with unstable robots lies in determining how to anticipate the human’s intentions to develop robot controllers that are responsive to the human’s movements (human’s transition to future states) while attempting to maintain stability amid interactions influenced by both human forces and the dynamics of the robot itself [211]. 

This multitask optimization challenge is often addressed using Quadratic Programming ( **QP** ), which minimizes the disparity between actual and reference task values. QP formulation allows for adaptable control solutions, covering inverse kinematics, inverse dynamics, and momentum-based challenges in either position or torque-controlled robots [184]. QP serves as a method for defining a constrained, at times hierachical, optimization problem, often formulated to find the control inputs that minimize the tracking error on one or multiple tasks. The constraints are critical to ensure safe robot behavior, such as joint position, velocity, and torque limits, as well as limits on allowable contact wrenches to maintain balance by keeping the ZMP within the support polygon, and in somple implementations, also imposing center of mass ( **CoM** ) trajectories [212, 213]. 

The interaction forces exerted between human and humanoid robot can be reflected in the QP constraints as part of a dynamic robot model subjected to external forces. For example, [212] implemented a QP controller for human-humanoid physical collaboration with the addition of constraints for contacts and collision-avoidance. To achieve compliance during the interaction, a stack of tasks can be defined in a hierarchical QP controller. These tasks can for example include position regulation based on human ergonomics, interaction force tracking, or motion tracking [214, 215]. The interaction dynamics between humans and humanoid robots (the forces exchanged between them) can be incorporated into QP constraints, modeling the robot’s dynamic response to external forces. 

Beyond a traditional QP, inherently unstable robots can greatly benefit from a stabilizer to maintain balance during physical interaction tasks, as introduced in subsection 3.4.4. Within this context, a few comprehensive approaches to whole-body compliant control have been introduced. In [216], a controller is proposed, comprising a compliant stabilizer based on the zero moment point ( **ZMP** ), measured via force/torque sensors located at the robot’s ankles, to complement a whole-body inverse kinematics engine. In [85] instead, the robot is equipped with a tactile sensor skin to capture interaction forces and employs a PID controller for balancing through ZMP tracking. 

In [217], a wheeled humanoid robot is made to guide physical interactions during dance training by controlling the height of its COM. In this approach, the robot engages in a dance with its human partner by adhering to a predefined trajectory while compliantly responding to the partner’s movements. This is facilitated through impedance control, which determines the robot’s joint accelerations according to the forces exchanged between the robot and the human partner. The robot is also programmed to convey its direction of motion with CoM height variations. 

## **6.2 Artificial neural network** 

Different solutions based on artificial neural networks ( **ANN** ) have been proposed for variable impedance and admittance control. In [218], an ANN is trained to output the force admittance of a robotic arm, in function of interaction forces measured by tactile sensors installed on the arm. An admittance control approach is proposed in [219], where an ANN is set up to feedback linearize the robot dynamics during pHRI, and Lyapunov stability analysis is leveraged to obtain ANN weight tuning laws. To enhance cooperation during pHRI, [220] introduced an admittance controller based on a combination of hedge algebras and ANN, which are used as an alternative to dynamic admittance model identification. 

Controlling compliant robots, whether through active compliance or tracking control, in the presence of joint flexibility poses challenges due to uncertainties in dynamics. Employing ANNs can effectively address these challenges by handling the complexities of flexibility dynamics. 

In [221], an adaptive impedance controller is introduced for humanrobot co-transportation tasks. This controller, incorporating an admittance-based radial basis function NN, error constraints, and input constraints, enables the tracking of human hand position and interaction force through vision and force sensing. In [222], the precise tracking of flexible robot joints in uncertain environments 

12 

The path towards contact-based physical human-robot interaction (Preprint) 

is addressed using a Lyapunov-stable adaptive neural network controller. The controller comprises two loops: a force-based outer loop and a position-based inner loop. The outer loop generates the reference trajectory using interaction force error and estimated environment stiffness, while the inner loop focuses on accurate position tracking with neural network compensation for uncertainties. 

## **6.3 Deep learning** 

Deep learning can be instrumental in advancing the field of pHRI by empowering robots to perceive, plan and respond to human intentions with greater accuracy and adaptability. Through deep neural networks ( **DNN** s) such as deep ANNs, CNNs or recurrent neural networks ( **RNN** s), complex mappings can be achieved between sensory inputs, such as visual, tactile, joint encoder, and F/T sensor feedback, and appropriate motor responses. Given the intricate nature of pHRI dynamics, neural networks require significant complexity, with a high number of layers, abundant data, and appropriate regularization. This is where deep learning methods prove to be highly advantageous. 

DNNs find multiple applications across a perception-planningcontrol system. Literature in which DNN techniques are used for perception and planning, such as [25, 26, 195] have been previously discussed in the Perception section (4), under its system modelling subsection (4.4.3) and planning section ( 5). DNNs have been used to interpret subtle human cues, anticipate movements, and adjust robot behaviour accordingly, towards fostering more natural and intuitive human-robot interactions [223, 153]. Moreover, deep learning has been applied to facilitating the development of control strategies involving learning from human demonstrations, adapting to dynamic environments, and optimizing robot actions to ensure safety and efficiency. This will be covered in the following two subsections, which will include the application of deep learning to RL and LfD. 

## **6.4 Reinforcement learning** 

Reinforcement learning ( **RL** ) can be employed to model complex task dynamics, which in turn can be used to optimize VI or VA control parameters as proposed in [224]. In this paper, the control parameters of a VI controller are optimized online through MPC, given the objective to minimize human effort during interaction and a model of HRI dynamics generated using ANNs. RL is used in [225] to automatically infer VI parameters of a robotic knee prosthesis by mimicking the motion of the intact knee. Instead, RL in [226] is employed to learn the damping coefficients of a VA controller that minimize jerk in point-to-point movements during co-manipulation tasks. 

Combining the deep deterministic policy gradient algorithm ( **DDPG** ) [227] and reward function optimization is proposed by [228] for safe human-robot collaboration in the manufacturing context: in this paper, a reward function is optimized to effectively learn collision avoidance policies. Instead, within the context of rehabilitation robotics, [229] introduced a controller for a robotic orthosis employing a two-stage deep RL strategy. Firstly, optimal human gaits are learned using deep RL-based imitation learning of a healthy human model. Then, models of weakened soleus muscles 

are developed and used to train a robotic orthosis policy for walking assistance. 

## **6.5 Learning from demonstration** 

Being based on human demonstrations, LfD is potentially more suitable than the typical RL approach of trial-and-error exploration, in the case of pHRI applications in which random exploration could be unsafe [230]. For instance, in [231], a teaching interface based on learning from demonstration is used to decrease the stiffness of an impedance-controlled robot in the Cartesian space, given displacements of the end-effector generated by direct pHRI. This work was later extended in [232] with an interface to increase stiffness based on measured interaction forces, and a mechanism to modulate stiffness either in the Cartesian or the joint space. 

Adopting a different strategy, [233] combines IRL and RL to tune impedance control parameters in an optimization framework where cost functions for pHRI performance are obtained from IRL, and then used to determine impedance parameters through RL. Another LfD approached introduced in [33], a deep RL algorithm is used to train control policies through a customizable multi-objective reward function derived from motion capture data of human-human handshakes and hand claps. 

The diversity of human behaviours drives the complexity of pHRI. The development of _intention-oriented_ control systems is required, in order to generate appropriate robot motions, given human intentions inferred from a combination of sensors. Further data-driven control approaches have yet to be extensively researched to make this a reality. 

## **7 Computational Enhancement** 

Contact-based pHRI demands rapid response and real-time performance from robots. When AI/ML is involved, the dynamic nature of the problem, coupled with changing interaction forces and human states, often necessitates resource-intensive deep learning methods. Consequently, computational constraints pose significant bottlenecks in the system, particularly with algorithms like fully connected neural networks, CNNs and RNNs [234, 235]. 

In this context, this section addresses computational challenges from both a hardware and a software perspective. The following section focuses on hardware technologies aimed at accelerating computation with a focus on processing units, while the subsequent subsection discusses control architectures and paradigms for achieving realtime and fast perception-planning-control systems. 

## **7.1 Hardware architecture** 

To address computational challenges, hardware and software system modification represent one approach to reducing computation time. For instance, various processor units and specialized electronic boards have been proposed to expedite computations. Incorporating graphics processing units ( **GPUs** ) [236], tensor processing units ( **TPUs** ) [237], and field-programmable gate arrays ( **FPGAs** ) [238] in conjunction with conventional central processing units ( **CPUs** ) has rendered deep learning algorithms viable for high-performance computing. 

13 

The path towards contact-based physical human-robot interaction (Preprint) 

GPUs excel in parallel processing, making them advantageous for training complex neural networks and analyzing sensor data quickly for real-time decisions in robotics. TPUs, on the other hand, are specialized hardware accelerators designed for machine learning tasks, particularly deep neural networks. They excel in matrix calculations and are preferred for both training and inference processes in robotics, especially for rapid data throughput and minimal latency. For their part, FPGAs offer adaptability and are useful for instant processing of sensor data, swift implementation of control algorithms with minimal delay, and accelerating machine learning computations within robotic frameworks. 

A study in [239] evaluated the performance of CPUs, GPUs, and FPGAs in solving the forward dynamics of articulated robotic arms. This task involves spatial algebra and the derivative of the Recursive Newton-Euler Algorithm. The study underscored the importance of this comparison, given that computing the gradient of rigid body dynamics typically consumes 30% to 90% of total computational time in nonlinear MPC implementations. The results revealed that the GPU and FPGA implementations completed the forward dynamics solution three times faster than their CPU counterpart, thanks to more efficient utilization of parallelism and customization. 

To accelerate deep learning models, parallelizing computations is key. This involves dividing data or models into smaller chunks and processing them concurrently across multiple devices. By harnessing the power of parallel processing, such as utilizing GPUs alongside FPGAs or leveraging multiple CPU cores, processing time is significantly reduced. For instance, in [240], a power-efficient implementation of DNN was suggested for both FPGAs and GPUs to accelerate the DNN computations, comprising both a CNN block and a fully connected NN block. By allocating the CNN part to the GPU and utilizing the FPGA for the fully connected layers, both could be processed in parallel. Through model breakdown and distributed processing, swifter computation could be achieved, along with a significant reduction of power consumption. 

## **7.2 Software architecture** 

Delving into robotic system architecture, the complexities inherent in designing systems capable of interacting with dynamic real-world environments, including humans, call to be explored. At its core, a robotic system is a complex communication network between sensors and actuators, geared towards accomplishing a defined set of tasks. However, the variability and uncertainty of pHRI scenarios, coupled with the diverse array of sensors and actuators, pose a level of intricacy that demands meticulous design and practical implementation strategies. Optimal architecture for rapid performance is also crucial for human safety, i.e., real-time and fast sensing, planning, and acting is important to ensure safety in a pHRI scenario. 

A robotic system architecture can be described with two key aspects: structure and style. The structure concerns the way in which the system is broken down into manageable interconnected subsystems, whereas the style involves the computational framework that defines communication among components within the architecture [241]. While there may not be a one-size-fits-all architecture for robotic systems, certain paradigms have emerged as valuable design frameworks. Below are listed several prominent architectural structures: 

**Deliberative architecture (Sense-Plan-Act):** This architecture, which was among the first proposed architectures, comprises three core subsystems: sensing, planning, and execution, arranged sequentially in a hierarchy. Sensor data is relayed to the planner, which then communicates with the controller to issue actuator commands. Deliberative architectures are flexible, scalable, and intelligent due to their ability to process sensory information in the planning module and to make decisions on actions. However, they come with a number of drawbacks: the planning stage often slows down the controller due to computational limitations, and the controller’s lack of direct sensor access hampers system reactivity [242]. The nested hierarchical controller [243] and the US National Institute of Standards and Technology (NIST) real-time control system [244] are two examples of this structure. 

**Reactive architecture (Sense-Act):** Reactive architectures operate under the premise that a robotic system can react to sensor inputs without requiring internal representation of sensory data (information) or planning. Such architectures comprise basic rules or behaviours that prompt actions in response to stimuli. While reactive architectures offer speed, robustness, and straightforward implementation, they often sacrifice flexibility, scalability, and intelligence. Since there is no planning module to process perceived sensory data and make decisions for actions, the sensory data and actions are confined to those that are hard-coded [242]. They are suitable for straightforward robotic systems operating in consistent, foreseeable conditions. And example of a suitable scenario could be basic obstacle avoidance, where a mobile robot is programmed to move along a straight path, and to simply shift to the left or right upon sensing an obstacle. 

**Hybrid architecture:** The principle behind hybrid architectures in robotics is to combine reactive and deliberative elements, in order to leverage their respective strengths into different levels of control. For instance, low-level (behavioural) actions may be handled reactively, while high-level planning may be handled deliberatively [245, 246]. In this context, low-level control is primarily concerned with executing localized, short-term behaviours at the sensor and actuator level (such as commanding the robot to turn left or right to avoid an obstacle). An executive, intermediate level oversees the translation of high-level plans into actionable low-level behaviours and manages exceptions (such as navigating to a destination). High-level planning then involves deliberate decision-making and long-term strategizing to optimize robot behaviour (such as planning to reach a destination and perform a given task). Although hybrid architectures provide a blend of the advantages found in both reactive and deliberative architectures, such as adaptability, modularity, and robustness, they may present challenges in terms of their design, implementation, and debugging processes due to the complexity of this architecture. 

**Subsumption architecture:** As proposed by [247], the subsumption architecture presents a real-time control option, as an alternative to the sense-plan-act paradigm. In this architecture, higher-level behaviours exert control over lower-level ones, facilitating the delegation of minor tasks to lower levels. Hence, it is designated as a **behaviour-based** structure. Each behaviour, such as map-building, exploration, wandering, and obstacle avoidance, is realized as a layer of finite state machines interconnected with sensors and actuators. This architecture is designed to allow multiple behaviours 

14 

The path towards contact-based physical human-robot interaction (Preprint) 

to be evaluated simultaneously and activated sequentially, through an arbitration mechanism determining the prioritized hierarchy of behaviours in real-time. 

The subsumption architecture has proven to be highly effective through numerous implementations, such as presented in [248, 249] The robots programmed under this architecture have been shown to exhibit real-time performance and responsiveness, due to their ability to continuously perceive and respond to changes in their surroundings, thus indicating the subsumption architecture to be well-suited for dynamic or human environments. Consequently, it is a promising option for scenarios involving pHRI, where real-time sense-plan-action capabilities are crucial, and where traditional AI may fail to provide sufficient response speed. 

Traditional AI approaches divide tasks into intricate subsystems such as perception, modeling, planning, execution, and control, which are carried out sequentially. Each of these subsystems may entail complexity and consume significant time. In contrast, the subsumption approach simplifies control by organizing tasks into parallel layers, each representing a specific behaviour. Each layer can independently control the robot in a basic manner, thus operating more swiftly compared to traditional AI methods [250]. However, while this architecture is highly reactive, it currently lacks effective long-term planning or behaviour optimization capabilities, thus posing challenges when it comes to achieving long-term objectives [241]. 

Aside from determining the architecture of a robotic system, selecting its style can be just as crucial. The style influences how the different components of a system, such as the planner, controller, and sensors, interact with each other. This communication is typically facilitated by middleware, which can for example take the format of client-server or that of publisher-subscriber. Client-server middleware, such as remote procedure call (RPC) [251] involves clients sending requests to a server, risking deadlocks (which may for example occur due to server crash). In contrast, publishersubscriber middleware broadcasts messages asynchronously, such that the control flow isn’t tied to any specific order, thus reducing the impact of missing or out-of-order messages. [252]. Robot Operating System (ROS) is a popular robotics middleware, which has drawn significant attention from research and industrial communities since its initial release in 2007 [253]. It is primarily built on the publishersubscriber style of communication, although it also incorporates support for the client-server style. 

In the past sections, the focus has been mostly on the technical functionality and performance of robotic systems that directly physically interact with people. In contrast, the next section will delve into the human experience of pHRI. 

While solutions have yet to be implemented, tested and evaluated in the context of pHRI, and many questions have yet to be answered, e.g., what safety measures ensure psychological safety during pHRI? How does one make robot programming transparent? How do biases show in pHRI? Who will be directly and indirectly affected by pHRI applications? How will major technology companies or governments engage on future employment concerns? 

As part of the solution, a code of HRI ethics proposed in [255] includes physically assistive robots. Ethical issues that influence the intention of people to use interactive robots have been investigated in [266], leading to recommendations for robot design. Additionally, the integration of established usability and user experience design principles into social HRI and collaborative robots is investigated in [268], towards ensuring human comfort and well-being. 

As research on the ethics of HRI is gradually emerging, we can look forward to further developments in the ethics of pHRI. However, the currently limited literature documenting problems and solutions relevant to contact-based pHRI indicates a need for researchers to dedicate resources to this problem, before robots become more integrated into everyday life. One significant challenge that was not explicitly mentioned yet but requires pressing attention, is that of comprehending how working in close proximity to robots impacts humans. Both on the short or on the long term, gaining a deeper understanding of robots’ influence and their implications on society is critical to ensuring the well-being of future populations across the globe (and beyond). 

## **9 Conclusion** 

The future of pHRI holds promising opportunities, with the potential to revolutionize industry and everyday life. However, significant challenges have yet to be tackled: the analysis above leads us to conclude that robotics, and pHRI in particular, is still in its infancy. 

In this survey, we have covered diverse categories of pHRI with a specific emphasis on contact-based interactions and explored various interconnected aspects of making the interaction safe and effective. To leave the reader with a sense of the interconnection between each of the aspects covered above, Fig. 5 provides a schematic representation of the collaboration and communication between ethics to design, planning and control. We propose to end with an outline of the challenges we have identified as most urgently requiring further investigation and attention: 

## **9.1 Design** 

## **8 Ethics** 

When talking about deploying pHRI in the real world, it is critical to address questions of ethics encompassing physical and psychological safety, transparency, privacy and work environment concerns [265, 266, 267]. Some of the questions needing most urgent consideration for the responsible and beneficial integration of robotic technology in society are included in Table 2. 

The design and testing of robots for pHRI require substantial engineering efforts and time investment due to constraints including use of materials, battery power, sensor and actuator availability, as well as robot functionality, locomotion abilities, and user-friendliness. Currently, robot utilization remains limited to specific scenarios and targeted tasks, primarily within industrial, rehabilitation and medical robotics. The development of versatile robots capable of seamlessly integrating into various aspects of human life remains an ongoing challenge. 

15 

The path towards contact-based physical human-robot interaction (Preprint) 

|**Ethical issues**|**Potential strategies**|
|---|---|
|Preventing harm to those who interact with robots, including|Safety guidelines for robot design [254], protocols for robots|
|physical, social and emotional impact of robots|touching humans, consider human emotional needs and the|
||formation of emotional bonds in design [255]|
|Ensuring users understand robot capabilities and intentions|Transparency [256] and explainability measures [257]|
|Protecting user privacy|Cybersecurity approaches [258], defne and follow privacy|
||laws and regulations [255]|
|Develop appropriate levels of trust in users|Predictability and communicativity [259]|
|Ensure user comfort, well-being and autonomy|Predictability [260], interaction design and transparency [261]|
|Eliminate biases and discrimination|Community engagement, transparency and explainability mea-|
||sures [262], avoid explicit computational evaluation of identity|
||characteristics [263], alternative robot morphologies [255]|
|Maintain human dignity and ensure fair labor practices|Support worker training and participation, transparency [264]|



Table 2: Imminent questions that need to be addressed regarding pHRI, along with potential solutions to explore 


![](1_survey/papers/md/Farajtabar2024path_figs/Farajtabar2024path.pdf-0016-03.png)


Figure 5: Schematic illustration of a typical pHRI framework, demonstrating the interconnections between various modules. Emphasizing safety as a critical aspect, the figure highlights the overarching need to address safety at each step, as well as to consider ethics from the start. 

## **9.2 Perception** 

It is crucial for robots to accurately perceive the dynamically changing environment and humans around them. To achieve comprehensive perception and develop socially aware robots, employing multi-modal sensory systems becomes inevitable, for example combining vision, touch, and audio signals. With advancements in AI/ML algorithms and their integration into robotics, e.g., the latest trend to integrate a generative pre-trained transformer into robot communication systems, there is great potential to achieve natural and intuitive interactions. 

## **9.3 Adaptability** 

Developing robots that can adapt to diverse human partners, environments, and tasks still needs significant effort. With currently trending approaches, this would require large AI/ML models and datasets, long learning periods and substantial computational re- 

sources, while still having to deal with limitations in the design of robots. 

## **9.4 Safety and compliance** 

Prioritizing human safety, for instance by ensuring robot compliance to interactions and adequate response to human actions, requires a tight integration of sensors, planning and control systems. Additionally, to properly ensure psychological and social safety in pHRI scenarios, further research on the impacts of robots on humans within pHRI contexts is acutely called for. Developing robots that exhibit intelligent behaviour and ensuring that people place an appropriate amount of trust in robots remains a persistent challenge. 

16 

The path towards contact-based physical human-robot interaction (Preprint) 

## **9.5 Ethics** 

It is becoming essential for engineers, researchers, industries and governments to prioritize ethical concerns regarding HRI and pHRI. Open conversations and extensive research needs to be conducted to explore effective ways of addressing the ethical challenges identified in the previous section, and the new challenges that have yet to be uncovered. Ultimately, this will hopefully lead to developing robots that work in the interests of people, and to increasing the interest of people in employing robots that work alongside them. In-depth ethical studies are prompted to ensure safety in pHRI, address the concerns related to robots replacing humans, to appropriately consider cultural and social differences in HRI, among all the significant ethical challenges that remain open. 

Our hope is that by engaging with these challenges on all fronts, robotic technology will be developed to realize the promises it holds, while enabling future society to thrive. 

## **References** 

- [1] Reza Rawassizadeh, Taylan Sen, Sunny Jung Kim, Christian Meurisch, Hamidreza Keshavarz, Max Mühlhäuser, and Michael Pazzani. Manifestation of virtual assistants and robots into daily life: Vision and challenges. CCF Transactions on Pervasive Computing and Interaction, 1:163–174, 2019. 

- [2] Anna Henschel, Guy Laban, and Emily S Cross. What makes a robot social? a review of social robots from science fiction to a home or hospital near you. Current Robotics Reports, 2:9–19, 2021. 

- [3] Agostino De Santis, Bruno Siciliano, Alessandro De Luca, and Antonio Bicchi. An atlas of physical human–robot interaction. Mechanism and Machine Theory, 43(3):253–270, 2008. 

- [4] Afonso Castro, Filipe Silva, and Vitor Santos. Trends of human-robot collaboration in industry contexts: Handover, learning, and metrics. Sensors, 21(12):4113, 2021. 

- [5] Mordechai Ben-Ari, Francesco Mondada, Mordechai BenAri, and Francesco Mondada. Robots and their applications. Elements of robotics, pages 1–20, 2018. 

- [6] Linn D Evjemo, Tone Gjerstad, Esten I Grøtli, and Gabor Sziebig. Trends in smart manufacturing: Role of humans and industrial robots in smart factories. Current Robotics Reports, 1:35–41, 2020. 

- [7] Khalid Hasan Tantawi, Alexandr Sokolov, and Omar Tantawi. Advances in industrial robotics: From industry 3.0 automation to industry 4.0 collaboration. In 2019 4th Technology Innovation Management and Engineering Science International Conference (TIMES-iCON), pages 1– 4, 2019. 

- [8] Steffen Walther and Tim Guhl. Classification of physical human-robot interaction scenarios to identify relevant requirements. In ISR/Robotik 2014; 41st International Symposium on Robotics, pages 1–8. VDE, 2014. 

- [9] Sarah L Müller, Sebastian Stiehm, Sabina Jeschke, and Anja Richert. Subjective stress in hybrid collaboration. In 

Social Robotics: 9th International Conference, ICSR 2017, Tsukuba, Japan, November 22-24, 2017, Proceedings 9, pages 597–606. Springer, 2017. 

- [10] Uchenna Emeoha Ogenyi, Jinguo Liu, Chenguang Yang, Zhaojie Ju, and Honghai Liu. Physical human–robot collaboration: Robotic systems, learning methods, collaborative strategies, sensors, and actuators. IEEE Transactions on Cybernetics, 51(4):1888–1901, 2021. 

- [11] Panagiota Tsarouchi, Sotiris Makris, and George Chryssolouris. Human–robot interaction review and challenges on task planning and programming. International Journal of Computer Integrated Manufacturing, 29(8):916–931, 2016. 

- [12] Angeliki Zacharaki, Ioannis Kostavelis, Antonios Gasteratos, and Ioannis Dokas. Safety bounds in human robot interaction: A survey. Safety science, 127:104667, 2020. 

- [13] Michael A Goodrich, Alan C Schultz, et al. Human– robot interaction: a survey. Foundations and Trends® in Human–Computer Interaction, 1(3):203–275, 2008. 

- [14] Haibin Yan, Marcelo H Ang, and Aun Neow Poo. A survey on perception methods for human–robot interaction in social robots. International Journal of Social Robotics, 6:85–119, 2014. 

- [15] Guang-Zhong Yang, Paolo Dario, and Danica Kragic. Social robotics—trust, learning, and social interaction, 2018. 

- [16] Judith Bütepage and Danica Kragic. Human-robot collaboration: from psychology to social robotics. arXiv preprint arXiv:1705.10146, 2017. 

- [17] Neziha Akalin and Amy Loutfi. Reinforcement learning approaches in social robotics. Sensors, 21(4):1292, 2021. 

- [18] Sandra Costa, Hagen Lehmann, Kerstin Dautenhahn, Ben Robins, and Filomena Soares. Using a humanoid robot to elicit body awareness and appropriate physical interaction in children with autism. International journal of social robotics, 7:265–278, 2015. 

- [19] K. Kosuge and Y. Hirata. Human-robot interaction. In 2004 IEEE International Conference on Robotics and Biomimetics, pages 8–11, 2004. 

- [20] Kathrin Pollmann, Wulf Loh, Nora Fronemann, and Daniel Ziegler. Entertainment vs. manipulation: Personalized human-robot interaction between user experience and ethical design. Technological Forecasting and Social Change, 189:122376, 2023. 

- [21] Steffen Walther and Tim Guhl. Classification of physical human-robot interaction scenarios to identify relevant requirements. In ISR/Robotik 2014; 41st International Symposium on Robotics, pages 1–8, 2014. 

- [22] Przemyslaw A Lasota, Terrence Fong, Julie A Shah, et al. A survey of methods for safe human-robot interaction. Foundations and Trends® in Robotics, 5(4):261–349, 2017. 

- [23] Hamed N Rahimi, Ian Howard, and Lei Cui. Neural impedance adaption for assistive human–robot interaction. Neurocomputing, 290:50–59, 2018. 

- [24] Yali Han, Songqing Zhu, Yiming Zhou, and Haitao Gao. An admittance controller based on assistive torque estimation for 

17 

The path towards contact-based physical human-robot interaction (Preprint) 

a rehabilitation leg exoskeleton. Intelligent Service Robotics, conference on Human-Robot Interaction, pages 391–398, 12(4):381–391, 2019. 2012. 

- [25] Arturo Marban, Vignesh Srinivasan, Wojciech Samek, Josep Fernández, and Alicia Casals. A recurrent convolutional neural network approach for sensorless force estimation in robotic surgery. Biomedical Signal Processing and Control, 50:134–150, 2019. 

- [26] Jiuyun Xia and Kazuo Kiguchi. Sensorless real-time force estimation in microsurgery robots using a time series convolutional neural network. IEEE Access, 9:149447–149455, 2021. 

- [27] Yeoun Jae Kim, Jong Hyun Seo, Hong Rae Kim, and Kwang Gi Kim. Impedance and admittance control for respiratory-motion compensation during robotic needle insertion–a preliminary test. The International Journal of Medical Robotics and Computer Assisted Surgery, 13(4):e1795, 2017. 

- [28] Jason Fong and Mahdi Tavakoli. Kinesthetic teaching of a therapist’s behavior to a rehabilitation robot. In 2018 International Symposium on Medical Robotics (ISMR), pages 1–6, 2018. 

- [29] Fatemeh Mohammadi Amin, Maryam Rezayati, Hans Wernher van de Venn, and Hossein Karimpour. A mixedperception approach for safe human–robot collaboration in industrial automation. Sensors, 20(21):6347, 2020. 

- [30] Harsh Maithani, Juan Antonio Corrales Ramon, Laurent Lequievre, Youcef Mezouar, and Matthieu Alric. Exoscarne: Assistive strategies for an industrial meat cutting system based on physical human-robot interaction. Applied Sciences, 11(9), 2021. 

- [31] Bitao Yao, Zude Zhou, Lihui Wang, Wenjun Xu, Quan Liu, and Aiming Liu. Sensorless and adaptive admittance control of industrial robot in physical human- robot interaction. Robotics and Computer-Integrated Manufacturing, 51:158– 168, 2018. 

- [32] Christopher Yee Wong, Lucas Vergez, and Wael Suleiman. Vision-and tactile-based continuous multimodal intention and attention recognition for safer physical human–robot interaction. IEEE Transactions on Automation Science and Engineering, pages 1–11, 2023. 

- [33] Sammy Christen, Stefan Stevši´c, and Otmar Hilliges. Demonstration-guided deep reinforcement learning of control policies for dexterous human-robot interaction. In 2019 International Conference on Robotics and Automation (ICRA), pages 2161–2167, 2019. 

- [34] Diego Felipe Paez Granados, Breno A. Yamamoto, Hiroko Kamide, Jun Kinugawa, and Kazuhiro Kosuge. Dance teaching by a robot: Combining cognitive and physical human–robot interaction for supporting the skill learning process. IEEE Robotics and Automation Letters, 2(3):1452– 1459, 2017. 

- [35] Baris Akgun, Maya Cakmak, Jae Wook Yoo, and Andrea Lockerd Thomaz. Trajectories and keyframes for kinesthetic teaching: A human-robot interaction perspective. In Proceedings of the seventh annual ACM/IEEE international 

- [36] Alberto Topini, William Sansom, Nicola Secciani, Lorenzo Bartalucci, Alessandro Ridolfi, and Benedetto Allotta. Variable admittance control of a hand exoskeleton for virtual reality-based rehabilitation tasks. Frontiers in neurorobotics, 15:188, 2022. 

- [37] Ali Ghadirzadeh, Judith Bütepage, Atsuto Maki, Danica Kragic, and Mårten Björkman. A sensorimotor reinforcement learning framework for physical human-robot interaction. In 2016 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), pages 2682–2688, 2016. 

- [38] Mahdi Khoramshahi and Aude Billard. A dynamical system approach to task-adaptation in physical human–robot interaction. Autonomous Robots, 43:927–946, 2019. 

- [39] David Vogt, Simon Stepputtis, Steve Grehl, Bernhard Jung, and Heni Ben Amor. A system for learning continuous human-robot interactions from human-human demonstrations. In 2017 IEEE International Conference on Robotics and Automation (ICRA), pages 2882–2889, 2017. 

- [40] Marco Ewerton, Gerhard Neumann, Rudolf Lioutikov, Heni Ben Amor, Jan Peters, and Guilherme Maeda. Learning multiple collaborative tasks with a mixture of interaction primitives. In 2015 IEEE International Conference on Robotics and Automation (ICRA), pages 1535–1542, 2015. 

- [41] Konstantinos Tsiakas, Michalis Papakostas, Michail Theofanidis, Morris Bell, Rada Mihalcea, Shouyi Wang, Mihai Burzo, and Fillia Makedon. An interactive multisensing framework for personalized human robot collaboration and assistive training using reinforcement learning. In Proceedings of the 10th International Conference on PErvasive Technologies Related to Assistive Environments, pages 423–427, 2017. 

- [42] Marina Kollmitz, Torsten Koller, Joschka Boedecker, and Wolfram Burgard. Learning human-aware robot navigation from physical interaction via inverse reinforcement learning. In 2020 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), pages 11025–11031, 2020. 

- [43] Mattia Leonori, Juan M. Gandarias, and Arash Ajoudani. Moca-s: A sensitive mobile collaborative robotic assistant exploiting low-cost capacitive tactile cover and whole-body control. IEEE Robotics and Automation Letters, 7(3):7920– 7927, 2022. 

- [44] Leonel Rozo, Joao Silverio, Sylvain Calinon, and Darwin G Caldwell. Learning controllers for reactive and proactive behaviors in human–robot collaboration. Frontiers in Robotics and AI, 3:30, 2016. 

- [45] Wei He, Chengqian Xue, Xinbo Yu, Zhijun Li, and Chenguang Yang. Admittance-based controller design for physical human–robot interaction in the constrained task space. IEEE Transactions on Automation Science and Engineering, 17(4):1937–1949, 2020. 

- [46] Maria Blancas, Vasiliki Vouloutsi, Klaudia Grechuta, and Paul FMJ Verschure. Effects of the robot’s role on humanrobot interaction in an educational scenario. In Biomimetic 

18 

The path towards contact-based physical human-robot interaction (Preprint) 

and Biohybrid Systems: 4th International Conference, Living Machines 2015, Barcelona, Spain, July 28-31, 2015, Proceedings 4, pages 391–402. Springer, 2015. 

- [47] Olivier A Blanson Henkemans, Bert PB Bierman, Joris Janssen, Mark A Neerincx, Rosemarijn Looije, Hanneke van der Bosch, and Jeanine AM van der Giessen. Using a robot to personalise health education for children with diabetes type 1: A pilot study. Patient education and counseling, 92(2):174–181, 2013. 

- [48] Phuong D.H. Nguyen, Fabrizio Bottarel, Ugo Pattacini, Matej Hoffmann, Lorenzo Natale, and Giorgio Metta. Merging physical and social interaction for effective humanrobot collaboration. In 2018 IEEE-RAS 18th International Conference on Humanoid Robots (Humanoids), pages 1–9, 2018. 

- [49] S. Robla-Gómez, Victor M. Becerra, J. R. Llata, E. GonzálezSarabia, C. Torre-Ferrero, and J. Pérez-Oria. Working together: A review on safe human-robot collaboration in industrial environments. IEEE Access, 5:26754–26773, 2017. 

- [50] Edirlei Soares de Lima and Bruno Feijó. Artificial intelligence in human-robot interaction. In Emotional Design in Human-Robot Interaction, pages 187–199. Springer, 2019. 

- [51] Francesco Semeraro, Alexander Griffiths, and Angelo Cangelosi. Human–robot collaboration and machine learning: A systematic review of recent research. Robotics and - 

- Computer Integrated Manufacturing, 79:102432, 2023. 

- [52] Milos Vasic and Aude Billard. Safety issues in humanrobot interactions. In 2013 ieee international conference on robotics and automation, pages 197–204. IEEE, 2013. 

- [53] Alessandra Papetti, Marianna Ciccarelli, Cecilia Scoccia, Giacomo Palmieri, and Michele Germani. A human-oriented design process for collaborative robotics. International Journal of Computer Integrated Manufacturing, pages 1–23, 2022. 

- [54] Giovanni Boschetti, Maurizio Faccio, and Irene Granata. Human-centered design for productivity and safety in collaborative robots cells: A new methodological approach. Electronics, 12(1):167, 2022. 

- [55] Luca Gualtieri, Erwin Rauch, and Renato Vidoni. Development and validation of guidelines for safety in human-robot collaborative assembly systems. Computers & Industrial Engineering, 163:107801, 2022. 

- [56] Pauline Maurice, Vincent Padois, Yvan Measson, and Philippe Bidaud. Human-oriented design of collaborative robots. International Journal of Industrial Ergonomics, 57:88–102, 2017. 

- [57] Carlotta Sartore, Lorenzo Rapetti, and Daniele Pucci. Optimization of humanoid robot designs for humanrobot ergonomic payload lifting. In 2022 IEEE-RAS 21st International Conference on Humanoid Robots (Humanoids), pages 722–729, 2022. 

- [58] Ricardo Sosa, Miguel Montiel, Eduardo B Sandoval, Rajesh E Mohan, et al. Robot ergonomics: Towards humancentred and robot-inclusive design. In DS 92: Proceedings of the DESIGN 2018 15th International Design Conference, pages 2323–2334, 2018. 

- [59] Luca Gualtieri, Erwin Rauch, Renato Vidoni, and Dominik T Matt. Safety, ergonomics and efficiency in human-robot collaborative assembly: design guidelines and requirements. Procedia CIRP, 91:367–372, 2020. 

- [60] Matteo Rubagotti, Inara Tusseyeva, Sara Baltabayeva, Danna Summers, and Anara Sandygulova. Perceived safety in physical human–robot interaction—a survey. Robotics and Autonomous Systems, 151:104047, 2022. 

- [61] Neziha Akalin, Annica Kristoffersson, and Amy Loutfi. Do you feel safe with your robot? factors influencing perceived safety in human-robot interaction based on subjective and objective measures. International journal of human-computer studies, 158:102744, 2022. 

- [62] Olesya Ogorodnikova. Methodology of safety for a human robot interaction designing stage. In 2008 Conference on Human System Interactions, pages 452–457, 2008. 

- [63] Velvetina Lim, Maki Rooksby, and Emily S Cross. Social robots on a global stage: establishing a role for culture during human–robot interaction. International Journal of Social Robotics, 13(6):1307–1333, 2021. 

- [64] Abdullah Alzahrani, Simon Robinson, and Muneeb Ahmad. Exploring factors affecting user trust across different humanrobot interaction settings and cultures. In Proceedings of the 10th International Conference on Human-Agent Interaction, pages 123–131, 2022. 

- [65] Lu Lu, Ziyang Xie, Hanwen Wang, Li Li, and Xu Xu. Mental stress and safety awareness during human-robot collaboration-review. Applied Ergonomics, 105:103832, 2022. 

- [66] Aslam Pervez and Jeha Ryu. Safe physical human robot interaction-past, present and future. Journal of Mechanical Science and Technology, 22:469–483, 2008. 

- [67] Yu She, Hai-Jun Su, Cheng Lai, and Deshan Meng. Design and prototype of a tunable stiffness arm for safe human-robot interaction. In International design engineering technical conferences and computers and information in engineering conference, volume 50169, page V05BT07A063. American Society of Mechanical Engineers, 2016. 

- [68] Ronald Van Ham, Thomas G Sugar, Bram Vanderborght, Kevin W Hollander, and Dirk Lefeber. Compliant actuator designs. IEEE Robotics & Automation Magazine, 16(3):81– 94, 2009. 

- [69] Michael Zinn, Oussama Khatib, Bernard Roth, and J Kenneth Salisbury. Playing it safe [human-friendly robots]. IEEE Robotics & Automation Magazine, 11(2):12–21, 2004. 

- [70] Gill A Pratt and Matthew M Williamson. Series elastic actuators. In Proceedings 1995 IEEE/RSJ International Conference on Intelligent Robots and Systems. Human Robot Interaction and Cooperative Robots, volume 1, pages 399–406. IEEE, 1995. 

- [71] G. Tonietti, R. Schiavi, and A. Bicchi. Design and control of a variable stiffness actuator for safe and fast physical human/robot interaction. In Proceedings of the 2005 IEEE International Conference on Robotics and Automation, pages 526–531, 2005. 

19 

The path towards contact-based physical human-robot interaction (Preprint) 

- [72] Antonio Bicchi, Giovanni Tonietti, Michele Bavaro, and Marco Piccigallo. Variable stiffness actuators for fast and safe motion control. In Robotics Research. The Eleventh International Symposium: With 303 Figures, pages 527–536. Springer, 2005. 

- [73] David V. Gealy, Stephen McKinley, Brent Yi, Philipp Wu, Phillip R. Downey, Greg Balke, Allan Zhao, Menglong Guo, Rachel Thomasson, Anthony Sinclair, Peter Cuellar, Zoe McCarthy, and Pieter Abbeel. Quasi-direct drive for lowcost compliant robotic manipulation. In 2019 International Conference on Robotics and Automation (ICRA), pages 437– 443, 2019. 

- [74] Gavin Kenneally, Avik De, and D. E. Koditschek. Design principles for a family of direct-drive legged robots. IEEE Robotics and Automation Letters, 1(2):900–907, 2016. 

- [75] K. Suita, Y. Yamada, N. Tsuchida, K. Imai, H. Ikeda, and N. Sugimoto. A failure-to-safety "kyozon" system with simple contact detection and stop capabilities for safe humanautonomous robot coexistence. In Proceedings of 1995 IEEE International Conference on Robotics and Automation, volume 3, pages 3089–3096 vol.3, 1995. 

- [76] Hun-Ok Lim and Kazuo Tanie. Collision-tolerant control of human-friendly robot with viscoelastic trunk. IEEE/ASME transactions on mechatronics, 4(4):417–427, 1999. 

- [77] Joohyung Kim, Alexander Alspach, and Katsu Yamane. 3d printed soft skin for safe human-robot interaction. In 2015 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), pages 2419–2425, 2015. 

- [78] Wan-Ling Chang and Selma Šabanovi´c. Interaction expands function: Social shaping of the therapeutic robot paro in a nursing home. In Proceedings of the Tenth Annual ACM/IEEE International Conference on Human-Robot Interaction, pages 343–350, 2015. 

- [79] Ronghuai Qi, Tin Lun Lam, and Yangsheng Xu. Mechanical design and implementation of a soft inflatable robot arm for safe human-robot interaction. In 2014 IEEE International Conference on Robotics and Automation (ICRA), pages 3490–3495, 2014. 

- [80] Antonio Bicchi and Giovanni Tonietti. Fast and" soft-arm" tactics [robot arm design]. IEEE Robotics & Automation Magazine, 11(2):22–33, 2004. 

- [81] Rainer Bischoff, Johannes Kurth, Guenter Schreiber, Ralf Koeppe, Alin Albu-Schaeffer, Alexander Beyer, Oliver Eiberger, Sami Haddadin, Andreas Stemmer, Gerhard Grunwald, and Gerhard Hirzinger. The kuka-dlr lightweight robot arm - a new reference platform for robotics research and manufacturing. In ISR 2010 (41st International Symposium on Robotics) and ROBOTIK 2010 (6th German Conference on Robotics), pages 1–8, 2010. 

- [82] Alessandro De Luca, Alin Albu-Schaffer, Sami Haddadin, and Gerd Hirzinger. Collision detection and safe reaction with the dlr-iii lightweight manipulator arm. In 2006 IEEE/RSJ International Conference on Intelligent Robots and Systems, pages 1623–1630. IEEE, 2006. 

- [83] Paul Rybski, Peter Anderson-Sprecher, Daniel Huber, Chris Niessl, and Reid Simmons. Sensor fusion for human safety in industrial workcells. In 2012 IEEE/RSJ International Conference on Intelligent Robots and Systems, pages 3612– 3619. IEEE, 2012. 

- [84] Markus Fritzsche, Norbert Elkmann, and Erik Schulenburg. Tactile sensing: A key technology for safe physical human robot interaction. In Proceedings of the 6th International Conference on Human-robot Interaction, pages 139–140, 2011. 

- [85] Emmanuel Dean-Leon, J. Rogelio Guadarrama-Olvera, Florian Bergner, and Gordon Cheng. Whole-body active compliance control for humanoid robots with robot skin. In 2019 International Conference on Robotics and Automation (ICRA), pages 5404–5410, 2019. 

- [86] Perla Maiolino, Marco Maggiali, Giorgio Cannata, Giorgio Metta, and Lorenzo Natale. A flexible and robust large scale capacitive tactile system for robots. IEEE Sensors Journal, 13(10):3910–3917, 2013. 

- [87] Isabella Huang and Ruzena Bajcsy. High resolution soft tactile interface for physical human-robot interaction. In 2020 IEEE International Conference on Robotics and Automation (ICRA), pages 1705–1711, 2020. 

- [88] A. Cirillo, F. Ficuciello, C. Natale, S. Pirozzi, and L. Villani. A conformable force/tactile skin for physical human–robot interaction. IEEE Robotics and Automation Letters, 1(1):41– 48, 2016. 

- [89] Sami Haddadin, Simon Haddadin, Augusto Khoury, Tim Rokahr, Sven Parusel, Rainer Burgkart, Antonio Bicchi, and Alin Albu-Schäffer. On making robots understand safety: Embedding injury knowledge into control. The International Journal of Robotics Research, 31(13):1578–1602, 2012. 

- [90] Carlos Morato, Krishnanand Kaipa, Boxuan Zhao, and Satyandra K Gupta. Safe human robot interaction by using exteroceptive sensing based human modeling. In International Design Engineering Technical Conferences and Computers and Information in Engineering Conference, volume 55850, page V02AT02A073. American Society of Mechanical Engineers, 2013. 

- [91] Dana Kuli´c and Elizabeth Croft. Pre-collision safety strategies for human-robot interaction. Autonomous Robots, 22:149–164, 2007. 

- [92] Jim Mainprice and Dmitry Berenson. Human-robot collaborative manipulation planning using early prediction of human motion. In 2013 IEEE/RSJ International Conference on Intelligent Robots and Systems, pages 299–306. IEEE, 2013. 

- [93] Hao Ding, Gunther Reißig, Kurniawan Wijaya, Dino Bortot, Klaus Bengler, and Olaf Stursberg. Human arm motion modeling and long-term prediction for safe and efficient humanrobot-interaction. In 2011 IEEE International Conference on Robotics and Automation, pages 5875–5880, 2011. 

- [94] Qinghua Li, Zhao Zhang, Yue You, Yaqi Mu, and Chao Feng. Data driven models for human motion prediction in humanrobot collaboration. IEEE Access, 8:227690–227702, 2020. 

20 

The path towards contact-based physical human-robot interaction (Preprint) 

- [95] Sung Ho Choi, Kyeong-Beom Park, Dong Hyeon Roh, Jae Yeol Lee, Mustafa Mohammed, Yalda Ghasemi, and Heejin Jeong. An integrated mixed reality system for safetyaware human-robot collaboration using deep learning and digital twin generation. Robotics and Computer-Integrated Manufacturing, 73:102258, 2022. 

- [96] Henny Admoni and Brian Scassellati. Social eye gaze in human-robot interaction: a review. Journal of Human-Robot Interaction, 6(1):25–63, 2017. 

- [97] Akanksha Saran, Srinjoy Majumdar, Elaine Schaertl Short, Andrea Thomaz, and Scott Niekum. Human gaze following for human-robot interaction. In 2018 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), pages 8615–8621, 2018. 

- [98] Satyajit Upasani, Divya Srinivasan, Qi Zhu, Jing Du, and Alexander Leonessa. Eye-tracking in physical human–robot interaction: Mental workload and performance prediction. Human factors, page 00187208231204704, 2023. 

- [99] Alireza Haji Fathaliyan, Xiaoyu Wang, and Veronica J Santos. Exploiting three-dimensional gaze tracking for action recognition during bimanual manipulation to enhance human– robot collaboration. Frontiers in Robotics and AI, 5:25, 2018. 

- [100] Eleonora Mariotti, Emanuele Magrini, and Alessandro De Luca. Admittance control for human-robot interaction using an industrial robot equipped with a f/t sensor. In 2019 International Conference on Robotics and Automation (ICRA), pages 6130–6136, 2019. 

- [101] Sami Haddadin, Alin Albu-Schaffer, Alessandro De Luca, and Gerd Hirzinger. Collision detection and reaction: A contribution to safe physical human-robot interaction. In 2008 IEEE/RSJ International Conference on Intelligent Robots and Systems, pages 3356–3363, 2008. 

- [102] Yi Li, Yanhui Li, Mingchao Zhu, Zhenbang Xu, and Deqiang Mu. A nonlinear momentum observer for sensorless robot collision detection under model uncertainties. Mechatronics, 78:102603, 2021. 

- [103] Przemyslaw A. Lasota, Gregory F. Rossano, and Julie A. Shah. Toward safe close-proximity human-robot interaction with standard industrial robots. In 2014 IEEE International Conference on Automation Science and Engineering (CASE), pages 339–344, 2014. 

- [104] Przemyslaw A Lasota and Julie A Shah. Analyzing the effects of human-aware motion planning on close-proximity human–robot collaboration. Human factors, 57(1):21–33, 2015. 

- [105] Emrah Akin Sisbot and Rachid Alami. A human-aware manipulation planner. IEEE Transactions on Robotics, 28(5):1045–1057, 2012. 

- [106] Rafi Hayne, Ruikun Luo, and Dmitry Berenson. Considering avoidance and consistency in motion planning for human-robot manipulation in a shared workspace. In 2016 IEEE International Conference on Robotics and Automation (ICRA), pages 3948–3954, 2016. 

- [107] Marco Faroni, Manuel Beschi, and Nicola Pedrocchi. Safetyaware time-optimal motion planning with uncertain human state estimation. IEEE Robotics and Automation Letters, 7(4):12219–12226, 2022. 

- [108] Agostino De Santis, Bruno Siciliano, et al. Reactive collision avoidance for safer human–robot interaction. In 5th IARP/IEEE RAS/EURON workshop on technical challenges for dependable robots in human environments, volume 1. Citeseer, 2007. 

- [109] Yiwei Wang, Yixuan Sheng, Ji Wang, and Wenlong Zhang. Optimal collision-free robot trajectory generation based on time series prediction of human motion. IEEE Robotics and Automation Letters, 3(1):226–233, 2018. 

- [110] Sami Haddadin, Sven Parusel, Rico Belder, and Alin Albu-Schäffer. It is (almost) all about human safety: A novel paradigm for robot design, control, and planning. In Computer Safety, Reliability, and Security: 32nd International Conference, SAFECOMP 2013, Toulouse, France, September 24-27, 2013. Proceedings 32, pages 202– 215. Springer, 2013. 

- [111] Sami Haddadin, Rico Belder, and Alin Albu-Schäffer. Dynamic motion planning for robots in partially unknown environments. IFAC Proceedings Volumes, 44(1):6842–6850, 2011. 

- [112] J. Micah Prendergast, Stephan Balvert, Tom Driessen, Ajay Seth, and Luka Peternel. Biomechanics aware collaborative robot system for delivery of safe physical therapy in shoulder rehabilitation. IEEE Robotics and Automation Letters, 6(4):7177–7184, 2021. 

- [113] Milad Shafiee, Giulio Romualdi, Stefano Dafarra, Francisco Javier Andrade Chavez, and Daniele Pucci. Online dcm trajectory generation for push recovery of torque-controlled humanoid robots. In 2019 IEEE-RAS 19th International Conference on Humanoid Robots (Humanoids), pages 671– 678, 2019. 

- [114] Andrea Maria Zanchettin, Nicola Maria Ceriani, Paolo Rocco, Hao Ding, and Björn Matthias. Safety in humanrobot collaborative manufacturing environments: Metrics and control. IEEE Transactions on Automation Science and Engineering, 13(2):882–893, 2016. 

- [115] Artemiy Oleinikov, Sanzhar Kusdavletov, Almas Shintemirov, and Matteo Rubagotti. Safety-aware nonlinear model predictive control for physical human-robot interaction. IEEE Robotics and Automation Letters, 6(3):5665– 5672, 2021. 

- [116] Axel Vick, Dragoljub Surdilovic, and Jörg Krüger. Safe physical human-robot interaction with industrial dual-arm robots. In 9th International Workshop on Robot Motion and Control, pages 264–269. IEEE, 2013. 

- [117] Feifei Bian, Danmei Ren, Ruifeng Li, and Peidong Liang. Improving stability in physical human–robot interaction by estimating human hand stiffness and a vibration index. Industrial Robot: the international journal of robotics research and application, 2018. 

- [118] David Silvera-Tawil, David Rye, and Mari Velonaki. Artificial skin and tactile sensing for socially interactive robots: 

21 

The path towards contact-based physical human-robot interaction (Preprint) 

A review. Robotics and Autonomous Systems, 63:230–243, 2015. 

- [119] Guozhen Li, Shiqiang Liu, Qian Mao, and Rong Zhu. Multifunctional electronic skins enable robots to safely and dexterously interact with human. Advanced Science, 9(11):2104969, 2022. 

- [120] Federica Ferraguti, Cristian Secchi, and Cesare Fantuzzi. A tank-based approach to impedance control with variable stiffness. In 2013 IEEE International Conference on Robotics and Automation, pages 4948–4953, 2013. 

- [121] Wenceslao Shaw Cortez, Christos K Verginis, and Dimos V Dimarogonas. Safe, passive control for mechanical systems with application to physical human-robot interactions. In 2021 IEEE International Conference on Robotics and Automation (ICRA), pages 3836–3842. IEEE, 2021. 

- [122] Jingdong Chen and Paul I Ro. Human intention-oriented variable admittance control with power envelope regulation in physical human-robot interaction. Mechatronics, 84:102802, 2022. 

- [123] Gitae Kang, Hyun Seok Oh, Joon Kyue Seo, Uikyum Kim, and Hyouk Ryeol Choi. Variable admittance control of robot manipulators based on human intention. IEEE/ASME Transactions on Mechatronics, 24(3):1023–1032, 2019. 

- [124] Chengxu Zhou, Zhibin Li, Juan Castano, Houman Dallali, Nikos G. Tsagarakis, and Darwin G. Caldwell. A passivity based compliance stabilizer for humanoid robots. In 2014 IEEE International Conference on Robotics and Automation (ICRA), pages 1487–1492, 2014. 

- [125] Yeshasvi Tirupachuri, Gabriele Nava, Claudia Latella, Diego Ferigo, Lorenzo Rapetti, Luca Tagliapietra, Francesco Nori, and Daniele Pucci. Towards partner-aware humanoid robot control under physical interactions. In Intelligent Systems and Applications: Proceedings of the 2019 Intelligent Systems Conference (IntelliSys) Volume 2, pages 1073– 1092. Springer, 2020. 

- [126] Michael Shomin, Jodi Forlizzi, and Ralph Hollis. Sit-tostand assistance with a balancing mobile robot. In 2015 IEEE International Conference on Robotics and Automation (ICRA), pages 3795–3800, 2015. 

- [127] Zhongyu Li and Ralph Hollis. Toward a ballbot for physically leading people: A human-centered approach. In 2019 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), pages 4827–4833, 2019. 

- [128] Taisuke Kobayashi, Emmanuel Dean-Leon, Julio Rogelio Guadarrama-Olvera, Florian Bergner, and Gordon Cheng. Whole-body multicontact haptic human–humanoid interaction based on leader–follower switching: A robot dance of the “box step”. Advanced Intelligent Systems, 4(2):2100038, 2022. 

- [129] Johannes Englsberger, Christian Ott, and Alin Albu-Schäffer. Three-dimensional bipedal walking control based on divergent component of motion. IEEE Transactions on Robotics, 31(2):355–368, 2015. 

- [130] J.L. Drury, J. Scholtz, and H.A. Yanco. Awareness in humanrobot interactions. In SMC’03 Conference Proceedings. 

   - 2003 IEEE International Conference on Systems, Man and Cybernetics. Conference Theme - System Security and Assurance (Cat. No.03CH37483), volume 1, pages 912–918 vol.1, 2003. 

- [131] S. Russell and P. Norvig. Artifcial Intelligence: A Modern Approach. Always learning. Pearson, 2016. 

- [132] Hugh F Durrant-Whyte. Integration, coordination and control of multi-sensor robot systems, volume 36. Springer Science & Business Media, 2012. 

- [133] Sami Haddadin and Elizabeth Croft. Physical Human–Robot Interaction, pages 1835–1874. Springer International Publishing, Cham, 2016. 

- [134] G. Grunwald, G. Schreiber, A. Albu-Schaffer, and G. Hirzinger. Programming by touch: the different way of human-robot interaction. IEEE Transactions on Industrial Electronics, 50(4):659–666, 2003. 

- [135] Vincent Duchaine and Clement Gosselin. Safe, stable and intuitive control for physical human-robot interaction. In 2009 IEEE International Conference on Robotics and Automation, pages 3383–3388, 2009. 

- [136] Zhijun Li, Bo Huang, Zhifeng Ye, Mingdi Deng, and Chenguang Yang. Physical human–robot interaction of a robotic exoskeleton by admittance control. IEEE Transactions on Industrial Electronics, 65(12):9614–9624, 2018. 

- [137] Chiara Talignani Landi, Federica Ferraguti, Lorenzo Sabattini, Cristian Secchi, and Cesare Fantuzzi. Admittance control parameter adaptation for physical human-robot interaction. In 2017 IEEE International Conference on Robotics and Automation (ICRA), pages 2911–2916, 2017. 

- [138] Hsieh-Yu Li, Ishara Paranawithana, Liangjing Yang, Terence Sey Kiat Lim, Shaohui Foong, Foo Cheong Ng, and U-Xuan Tan. Stable and compliant motion of physical human–robot interaction coupled with a moving environment using variable admittance and adaptive control. IEEE Robotics and Automation Letters, 3(3):2493–2500, 2018. 

- [139] Christopher Yee Wong, Saeid Samadi, Wael Suleiman, Abderrahmane Kheddar, and Christopher Yee Wong. Touch semantics for intuitive physical manipulation of humanoids. IEEE transactions on human-machine systems., 52(6), 202212. 

- [140] Alexis C. Holgado, Nicola Piga, Tito Pradhono Tomo, Giulia Vezzani, Alexander Schmitz, Lorenzo Natale, and Shigeki Sugano. Magnetic 3-axis soft and sensitive fingertip sensors integration for the icub humanoid robot. In 2019 IEEE-RAS 19th International Conference on Humanoid Robots (Humanoids), pages 1–8, 2019. 

- [141] Alexis Carlos Holgado, Tito Pradhono Tomo, Sophon Somlor, and Shigeki Sugano. A multimodal, adjustable sensitivity, digital 3-axis skin sensor module. Sensors, 20(11), 2020. 

- [142] Alessandro Albini and Giorgio Cannata. Pressure distribution classification and segmentation of human hands in contact with the robot body. The International Journal of Robotics Research, 39(6):668–687, 2020. 

- [143] Mattia Leonori, Juan M. Gandarias, and Arash Ajoudani. Moca-s: A sensitive mobile collaborative robotic assistant 

22 

The path towards contact-based physical human-robot interaction (Preprint) 

exploiting low-cost capacitive tactile cover and whole-body control. IEEE Robotics and Automation Letters, 7(3):7920– 7927, 2022. 

- [144] P. Mittendorfer, E. Yoshida, and G. Cheng. Realizing wholebody tactile interactions with a self-organizing, multi-modal artificial skin on a humanoid robot. Advanced Robotics, 29(1):51–67, 2015. 

- [145] Simon Armleder, Emmanuel Dean-Leon, Florian Bergner, and Gordon Cheng. Interactive force control based on multimodal robot skin for physical human- robot collaboration. Advanced Intelligent Systems, 4(2):2100047, 2022. 

- [146] Vincent Duchaine, Nicolas Lauzier, Mathieu Baril, MarcAntoine Lacasse, and Clement Gosselin. A flexible robot skin for safe physical human robot interaction. In 2009 IEEE International Conference on Robotics and Automation, pages 3676–3681, 2009. 

- [147] Marc Teyssier, Brice Parilusyan, Anne Roudaut, and Jürgen Steimle. Human-like artificial skin sensor for physical humanrobot interaction. In 2021 IEEE International Conference on Robotics and Automation (ICRA), pages 3626–3633, 2021. 

- [148] Shan Wei, Yijian Liu, Lina Yang, Haicheng Wang, Haoran Niu, Chao Zhou, Yanyan Wang, Qiuquan Guo, and Da Chen. Flexible large e-skin array based on patterned laser-induced graphene for tactile perception. Sensors and Actuators A: Physical, 334:113308, 2022. 

- [149] Teng Xue, Weiming Wang, Jin Ma, Wenhai Liu, Zhenyu Pan, and Mingshuo Han. Progress and prospects of multimodal fusion methods in physical human–robot interaction: A review. IEEE Sensors Journal, 20(18):10355–10370, 2020. 

- [150] Emanuele Magrini, Fabrizio Flacco, and Alessandro De Luca. Estimation of contact forces using a virtual force sensor. In 2014 IEEE/RSJ International Conference on Intelligent Robots and Systems, pages 2126–2133, 2014. 

- [151] Arne Wahrburg, Björn Matthias, and Hao Ding. Cartesian contact force estimation for robotic manipulators-a fault isolation perspective. IFAC-PapersOnLine, 48(21):1232–1237, 2015. 

- [152] Yazhan Zhang, Guanlan Zhang, Yipai Du, and Michael Yu Wang. Vtacarm. a vision-based tactile sensing augmented robotic arm with application to human-robot interaction. In 2020 IEEE 16th International Conference on Automation Science and Engineering (CASE), pages 35–42, 2020. 

- [153] Hang Su, Wen Qi, Zhijun Li, Ziyang Chen, Giancarlo Ferrigno, and Elena De Momi. Deep neural network approach in emg-based force estimation for human–robot interaction. IEEE Transactions on Artifcial Intelligence, 2(5):404–412, 2021. 

- [154] Stavros Grafakos, Fotios Dimeas, and Nikos Aspragathos. Variable admittance control in phri using emg-based arm muscles co-activation. In 2016 IEEE International Conference on Systems, Man, and Cybernetics (SMC), pages 001900– 001905, 2016. 

- [155] DSV Bandara, Jumpei Arata, and Kazuo Kiguchi. A noninvasive brain–computer interface approach for predicting motion intention of activities of daily living tasks for an upper-limb 

wearable robot. International Journal of Advanced Robotic Systems, 15(2):1729881418767310, 2018. 

- [156] Luis Roda-Sanchez, Celia Garrido-Hidalgo, Arturo S García, Teresa Olivares, and Antonio Fernández-Caballero. Comparison of rgb-d and imu-based gesture recognition for humanrobot interaction in remanufacturing. The International Journal of Advanced Manufacturing Technology, pages 1– 13, 2021. 

- [157] Joseph Campbell and Katsu Yamane. Learning whole-body human-robot haptic interaction in social contexts. In 2020 IEEE International Conference on Robotics and Automation (ICRA), pages 10177–10183. IEEE, 2020. 

- [158] Mustafa Can Bingol and Omur Aydogmus. Performing predefined tasks using the human–robot interaction on speech recognition for an industrial robot. Engineering Applications of Artifcial Intelligence, 95:103903, 2020. 

- [159] K Ashok, Mohd Ashraf, J Thimmia Raja, Md Zair Hussain, Dinesh Kumar Singh, and Anandakumar Haldorai. Collaborative analysis of audio-visual speech synthesis with sensor measurements for regulating human–robot interaction. International Journal of System Assurance Engineering and Management, pages 1–8, 2022. 

- [160] Shuo Gao, Yanning Dai, and Arokia Nathan. Tactile and vision perception for intelligent humanoids. Advanced Intelligent Systems, 4(2):2100074, 2022. 

- [161] Emanuele Magrini, Fabrizio Flacco, and Alessandro De Luca. Control of generalized contact motion and force in physical human-robot interaction. In 2015 IEEE International Conference on Robotics and Automation (ICRA), pages 2298–2304, 2015. 

- [162] Don Joven Agravante, Andrea Cherubini, Antoine Bussy, Pierre Gergondet, and Abderrahmane Kheddar. Collaborative human-humanoid carrying using vision and haptic sensing. In 2014 IEEE international conference on robotics and automation (ICRA), pages 607–612. IEEE, 2014. 

- [163] Don Joven Agravante, Andrea Cherubini, Antoine Bussy, Pierre Gergondet, and Abderrahmane Kheddar. Collaborative human-humanoid carrying using vision and haptic sensing. In 2014 IEEE International Conference on Robotics and Automation (ICRA), pages 607–612, 2014. 

- [164] H. Kawamoto, Suwoong Lee, S. Kanbe, and Y. Sankai. Power assist method for hal-3 using emg-based feedback controller. In SMC’03 Conference Proceedings. 2003 IEEE International Conference on Systems, Man and Cybernetics. Conference Theme - System Security and Assurance (Cat. No.03CH37483), volume 2, pages 1648–1653 vol.2, 2003. 

- [165] Kai Gui, Honghai Liu, and Dingguo Zhang. Toward multimodal human–robot interaction to enhance active participation of users in gait rehabilitation. IEEE Transactions on Neural Systems and Rehabilitation Engineering, 25(11):2054–2066, 2017. 

- [166] Ali Al-Yacoub, YC Zhao, William Eaton, Yee Mey Goh, and Niels Lohse. Improving human robot collaboration through force/torque based learning for object manipulation. Robotics and Computer-Integrated Manufacturing, 69:102111, 2021. 

23 

The path towards contact-based physical human-robot interaction (Preprint) 

- [167] Lourdes Martínez-Villaseñor and Hiram Ponce. A concise review on sensor signal acquisition and transformation applied to human activity recognition and human–robot interaction. International Journal of Distributed Sensor Networks, 15(6):1550147719853987, 2019. 

- [168] Zhe Cao, Tomas Simon, Shih-En Wei, and Yaser Sheikh. Realtime multi-person 2d pose estimation using part affinity fields. In Proceedings of the IEEE conference on computer vision and pattern recognition, pages 7291–7299, 2017. 

- [169] Yu Cheng, Bo Yang, Bo Wang, and Robby T Tan. 3d human pose estimation using spatio-temporal networks with explicit occlusion training. In Proceedings of the AAAI Conference on Artifcial Intelligence, volume 34, pages 10631–10638, 2020. 

- [170] Kyoungoh Lee, Inwoong Lee, and Sanghoon Lee. Propagating lstm: 3d pose estimation based on joint interdependency. In Proceedings of the European conference on computer vision (ECCV), pages 119–135, 2018. 

- [171] Ching-Hang Chen, Ambrish Tyagi, Amit Agrawal, Dylan Drover, Rohith Mv, Stefan Stojanov, and James M Rehg. Unsupervised 3d pose estimation with geometric selfsupervision. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, pages 5714– 5724, 2019. 

- [172] Z. Cao, G. Hidalgo, T. Simon, S. Wei, and Y. Sheikh. Openpose: Realtime multi-person 2d pose estimation using part affinity fields. IEEE Transactions on Pattern Analysis & Machine Intelligence, 43(01):172–186, jan 2021. 

- [173] Jan Docekal, Jakub Rozlivek, Jiri Matas, and Matej Hoffmann. Human keypoint detection for close proximity humanrobot interaction. In 2022 IEEE-RAS 21st International Conference on Humanoid Robots (Humanoids), pages 450– 457, 2022. 

- [174] Kenko Fujii, Gauthier Gras, Antonino Salerno, and GuangZhong Yang. Gaze gesture based human robot interaction for laparoscopic surgery. Medical image analysis, 44:196–214, 2018. 

- [175] Oriane Dermy, François Charpillet, and Serena Ivaldi. Multimodal intention prediction with probabilistic movement primitives. In Human Friendly Robotics: 10th International Workshop, pages 181–196. Springer, 2019. 

- [176] Osama Mazhar, Sofiane Ramdani, Benjamin Navarro, Robin Passama, and Andrea Cherubini. Towards real-time physical human-robot interaction using skeleton information and hand gestures. In 2018 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), pages 1–6, 2018. 

- [177] Osama Mazhar, Benjamin Navarro, Sofiane Ramdani, Robin Passama, and Andrea Cherubini. A real-time human-robot interaction framework with robust background invariant hand gesture detection. Robotics and Computer-Integrated Manufacturing, 60:34–48, 2019. 

- [178] Luis Roda-Sanchez, Teresa Olivares, Celia Garrido-Hidalgo, José Luis de la Vara, and Antonio Fernandez-Caballero. Human-robot interaction in industry 4.0 based on an internet of things real-time gesture control system. Integrated Computer-Aided Engineering, 28(2):159–175, 2021. 

- [179] Francesco Romano, Gabriele Nava, Morteza Azad, Jernej ˇCamernik, Stefano Dafarra, Oriane Dermy, Claudia Latella, Maria Lazzaroni, Ryan Lober, Marta Lorenzini, Daniele Pucci, Olivier Sigaud, Silvio Traversaro, Jan Babiˇc, Serena Ivaldi, Michael Mistry, Vincent Padois, and Francesco Nori. The codyco project achievements and beyond: Toward human aware whole-body controllers for physical human robot interaction. IEEE Robotics and Automation Letters, 3(1):516–523, 2018. 

- [180] Lorenzo Vianello, Jean-Baptiste Mouret, Eloise Dalin, Alexis Aubry, and Serena Ivaldi. Human posture prediction during physical human-robot interaction. IEEE Robotics and Automation Letters, 6(3):6046–6053, 2021. 

- [181] Jessica Lanini, Hamed Razavi, Julen Urain, and Auke Ijspeert. Human intention detection as a multiclass classification problem: Application in physical human–robot interaction while walking. IEEE Robotics and Automation Letters, 3(4):4171–4178, 2018. 

- [182] Zhiguang Liu and Jianhong Hao. Intention recognition in physical human-robot interaction based on radial basis function neural network. Journal of Robotics, 2019, 2019. 

- [183] Guangzhu Peng, Chenguang Yang, Wei He, and C. L. Philip Chen. Force sensorless admittance control with neural learning for robots with actuator saturation. IEEE Transactions on Industrial Electronics, 67(4):3138–3148, 2020. 

- [184] Lorenzo Vianello, Luigi Penco, Waldez Gomes, Yang You, Salvatore Maria Anzalone, Pauline Maurice, Vincent Thomas, and Serena Ivaldi. Human-humanoid interaction and cooperation: a review. Current Robotics Reports, 2(4):441– 454, 2021. 

- [185] Martin Lawitzky, José Ramón Medina, Dongheui Lee, and Sandra Hirche. Feedback motion planning and learning from demonstration in physical robotic assistance: differences and synergies. In 2012 IEEE/RSJ International Conference on Intelligent Robots and Systems, pages 3646–3652, 2012. 

- [186] Shiqi Li, Ke Han, Xiao Li, Shuai Zhang, Youjun Xiong, and Zheng Xie. Hybrid trajectory replanning-based dynamic obstacle avoidance for physical human-robot interaction. Journal of Intelligent & Robotic Systems, 103:1–14, 2021. 

- [187] Marco Faroni, Manuel Beschi, and Nicola Pedrocchi. An mpc framework for online motion planning in human-robot collaborative tasks. In 2019 24th IEEE International Conference on Emerging Technologies and Factory Automation (ETFA), pages 1555–1558, 2019. 

- [188] Ajung Moon, Maneezhay Hashmi, HF Machiel Van Der Loos, Elizabeth A Croft, and Aude Billard. Design of hesitation gestures for nonverbal human-robot negotiation of conflicts. ACM Transactions on Human-Robot Interaction (THRI), 10(3):1–25, 2021. 

- [189] Sonia Chernova and Andrea L Thomaz. Robot learning from human teachers. Synthesis lectures on artifcial intelligence and machine learning, 8(3):1–121, 2014. 

- [190] Heni Ben Amor, Gerhard Neumann, Sanket Kamthe, Oliver Kroemer, and Jan Peters. Interaction primitives for humanrobot cooperation tasks. In 2014 IEEE International 

24 

The path towards contact-based physical human-robot interaction (Preprint) 

Conference on Robotics and Automation (ICRA), pages 2831–2837, 2014. 

- [191] Yujun Lai, Gavin Paul, Yunduan Cui, and Takamitsu Matsubara. User intent estimation during robot learning using physical human robot interaction primitives. Autonomous Robots, 46(2):421–436, 2022. 

- [192] Scott Niekum, Sarah Osentoski, George Konidaris, and Andrew G Barto. Learning and generalization of complex tasks from unstructured demonstrations. In 2012 IEEE/RSJ International Conference on Intelligent Robots and Systems, pages 5239–5246. IEEE, 2012. 

- [193] Nadia Figueroa, Ana Lucia Pais Ureche, and Aude Billard. Learning complex sequential tasks from demonstration: A pizza dough rolling case study. In 2016 11th ACM/IEEE International Conference on Human-Robot Interaction (HRI), pages 611–612, 2016. 

- [194] Rui Huang, Hong Cheng, Jing Qiu, and Jianwei Zhang. Learning physical human–robot interaction with coupled cooperative primitives for a lower exoskeleton. IEEE Transactions on Automation Science and Engineering, 16(4):1566–1574, 2019. 

- [195] Dylan P Losey, Andrea Bajcsy, Marcia K O’Malley, and Anca D Dragan. Physical interaction as communication: Learning robot objectives online from human corrections. The International Journal of Robotics Research, 41(1):20– 44, 2022. 

- [196] Dylan P Losey, Craig G McDonald, Edoardo Battaglia, and Marcia K O’Malley. A review of intent detection, arbitration, and communication aspects of shared control for physical human–robot interaction. Applied Mechanics Reviews, 70(1), 2018. 

- [197] Mario Selvaggio, Marco Cognetti, Stefanos Nikolaidis, Serena Ivaldi, and Bruno Siciliano. Autonomy in physical human-robot interaction: A brief survey. IEEE Robotics and Automation Letters, 6(4):7989–7996, 2021. 

- [198] Said G Khan, Guido Herrmann, Mubarak Al Grafi, Tony Pipe, and Chris Melhuish. Compliance control and human– robot interaction: Part 1—survey. International journal of humanoid robotics, 11(03):1430001, 2014. 

- [199] Hsieh-Yu Li, Audelia G Dharmawan, Ishara Paranawithana, Liangjing Yang, and U-Xuan Tan. A control scheme for physical human-robot interaction coupled with an environment of unknown stiffness. Journal of Intelligent & Robotic Systems, 100:165–182, 2020. 

- [200] Mojtaba Sharifi, Saeed Behzadipour, and Gholamreza Vossoughi. Nonlinear model reference adaptive impedance control for human–robot interactions. Control Engineering Practice, 32:9–27, 2014. 

- [201] Issac Rhee, Gitae Kang, Seung Jae Moon, Yun Seok Choi, and Hyouk Ryeol Choi. Hybrid impedance and admittance control of robot manipulator with unknown environment. Intelligent Service Robotics, 16(1):49–60, 2023. 

- [202] Kevin Haninger, Christian Hegeler, and Luka Peternel. Model predictive control with gaussian processes for flexible multi-modal physical human robot interaction. In 

2022 International Conference on Robotics and Automation (ICRA), pages 6948–6955. IEEE, 2022. 

- [203] Bryan Whitsell and Panagiotis Artemiadis. Physical human–robot interaction (phri) in 6 dof with asymmetric cooperation. IEEE Access, 5:10834–10845, 2017. 

- [204] Brahim Brahmi, Mohamed Hamza Laraki, Maarouf Saad, Cristobal Ochoa-Luna, and Abdelkrim Brahmi. Compliant adaptive control of human upper-limb exoskeleton robot with unknown dynamics based on a modified function approximation technique (mfat). Robotics and Autonomous Systems, 117:92–102, 2019. 

- [205] Arvid QL Keemink, Herman van der Kooij, and Arno HA Stienen. Admittance control for physical human–robot interaction. The International Journal of Robotics Research, 37(11):1421–1444, 2018. 

- [206] H-P Huang and S-S Chen. Compliant motion control of robots by using variable impedance. The International Journal of Advanced Manufacturing Technology, 7(6):322– 332, 1992. 

- [207] Mojtaba Sharifi, Amir Zakerimanesh, Javad K. Mehr, Ali Torabi, Vivian K. Mushahwar, and Mahdi Tavakoli. Impedance variation and learning strategies in human–robot interaction. IEEE Transactions on Cybernetics, 52(7):6462– 6475, 2022. 

- [208] Kyeong Ha Lee, Seung Guk Baek, Hyuk Jin Lee, Seung Ho Lee, and Ja Choon Koo. Real-time adaptive impedance compensator using simultaneous perturbation stochastic approximation for enhanced physical human–robot interaction transparency. Robotics and Autonomous Systems, 147:103916, 2022. 

- [209] Wen Yu and Adolfo Perrusquía. Simplified stable admittance control using end-effector orientations. International Journal of Social Robotics, 12(5):1061–1073, 2020. 

- [210] Jianwei Dong, Jianming Xu, Qiaoqian Zhou, and Songda Hu. Physical human–robot interaction force control method based on adaptive variable impedance. Journal of the Franklin Institute, 357(12):7864–7878, 2020. 

- [211] Francesco Romano, Gabriele Nava, Morteza Azad, Jernej ˇCamernik, Stefano Dafarra, Oriane Dermy, Claudia Latella, Maria Lazzaroni, Ryan Lober, Marta Lorenzini, Daniele Pucci, Olivier Sigaud, Silvio Traversaro, Jan Babiˇc, Serena Ivaldi, Michael Mistry, Vincent Padois, and Francesco Nori. The codyco project achievements and beyond: Toward human aware whole-body controllers for physical human robot interaction. IEEE Robotics and Automation Letters, 3(1):516–523, 2018. 

- [212] Kazuya Otani, Karim Bouyarmane, and Serena Ivaldi. Generating assistive humanoid motions for co-manipulation tasks with a multi-robot quadratic program controller. In 2018 IEEE International Conference on Robotics and Automation (ICRA), pages 3107–3113, 2018. 

- [213] Marie Charbonneau, Valerio Modugno, Francesco Nori, Giuseppe Oriolo, Daniele Pucci, and Serena Ivaldi. Learning robust task priorities of qp-based whole-body torque-controllers. In 2018 IEEE-RAS 18th International 

25 

The path towards contact-based physical human-robot interaction (Preprint) 

Conference on Humanoid Robots (Humanoids), pages 1–9, motion. IEEE Robotics and Automation Letters, 7(3):7014– 2018. 7020, 2022. 

- [214] Francesco Tassi, Elena De Momi, and Arash Ajoudani. An adaptive compliance hierarchical quadratic programming controller for ergonomic human–robot collaboration. Robotics and Computer-Integrated Manufacturing, 78:102381, 2022. 

- [215] Francesco Tassi and Arash Ajoudani. Multi-modal and adaptive control of human-robot interaction through hierarchical quadratic programming. 2023. 

- [216] Enrico Mingo Hoffman, Brice Clement, Chengxu Zhou, Nikos G Tsagarakis, Jean-Baptiste Mouret, and Serena Ivaldi. Whole-body compliant control of icub: first results with opensot. In IEEE/RAS ICRA Workshop on Dynamic Legged Locomotion in Realistic Terrains, 2018. 

- [217] Diego Felipe Paez Granados, Jun Kinugawa, Yasuhisa Hirata, and Kazuhiro Kosuge. Guiding human motions in physical human-robot interaction through com motion control of a dance teaching robot. In 2016 IEEE-RAS 16th International Conference on Humanoid Robots (Humanoids), pages 279– 285, 2016. 

- [218] Ganna Pugach, Artem Melnyk, Olga Tolochko, Alexandre Pitti, and Philippe Gaussier. Touch-based admittance control of a robotic arm using neural learning of an artificial skin. In 2016 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), pages 3374–3380. IEEE, 2016. 

- [219] Sven Cremer, Sumit Kumar Das, Indika B. Wijayasinghe, Dan O. Popa, and Frank L. Lewis. Model-free online neuroadaptive controller with intent estimation for physical human–robot interaction. IEEE Transactions on Robotics, 36(1):240–253, 2020. 

- [220] Nguyen-Van Toan, Phan-Bui Khoi, and Soo-Yeong Yi. A mlp-hedge-algebras admittance controller for physical human–robot interaction. Applied Sciences, 11(12), 2021. 

- [221] Xinbo Yu, Bin Li, Wei He, Yanghe Feng, Long Cheng, and Carlos Silvestre. Adaptive-constrained impedance control for human–robot co-transportation. IEEE Transactions on Cybernetics, 52(12):13237–13249, 2022. 

- [222] Xinbo Yu, Sisi Liu, Shuang Zhang, Wei He, and Haifeng Huang. Adaptive neural network force tracking control of flexible joint robot with an uncertain environment. IEEE Transactions on Industrial Electronics, 71(6):5941–5949, 2024. 

- [223] Dong Wei, Lipeng Chen, Longfei Zhao, Hua Zhou, and Bidan Huang. A vision-based measure of environmental effects on inferring human intention during human robot interaction. IEEE Sensors Journal, 22(5):4246–4256, 2022. 

- [224] Loris Roveda, Jeyhoon Maskani, Paolo Franceschi, Arash Abdi, Francesco Braghin, Lorenzo Molinari Tosatti, and Nicola Pedrocchi. Model-based reinforcement learning variable impedance control for human-robot collaboration. Journal of Intelligent & Robotic Systems, 100(2):417–433, 2020. 

- [225] Ruofan Wu, Minhan Li, Zhikai Yao, Wentao Liu, Jennie Si, and He Huang. Reinforcement learning impedance control of a robotic prosthesis to coordinate with human intact knee 

- [226] Fotios Dimeas and Nikos Aspragathos. Reinforcement learning of variable admittance control for human-robot comanipulation. In 2015 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), pages 1011– 1016, 2015. 

- [227] Timothy P Lillicrap, Jonathan J Hunt, Alexander Pritzel, Nicolas Heess, Tom Erez, Yuval Tassa, David Silver, and Daan Wierstra. Continuous control with deep reinforcement learning. arXiv preprint arXiv:1509.02971, 2015. 

- [228] Quan Liu, Zhihao Liu, Bo Xiong, Wenjun Xu, and Yang Liu. Deep reinforcement learning-based safe interaction for industrial human-robot collaboration using intrinsic reward function. Advanced Engineering Informatics, 49:101360, 2021. 

- [229] Jong In Han, Jeong-Hoon Lee, Ho Seon Choi, Jung-Hoon Kim, and Jongeun Choi. Policy design for an ankle-foot orthosis using simulated physical human–robot interaction via deep reinforcement learning. IEEE Transactions on Neural Systems and Rehabilitation Engineering, 30:2186– 2197, 2022. 

- [230] Mojtaba Sharifi, Vahid Azimi, Vivian K. Mushahwar, and Mahdi Tavakoli. Impedance learning-based adaptive control for human–robot interaction. IEEE Transactions on Control Systems Technology, 30(4):1345–1358, 2022. 

- [231] Klas Kronander and Aude Billard. Online learning of varying stiffness through physical human-robot interaction. In 2012 IEEE International Conference on Robotics and Automation, pages 1842–1849, 2012. 

- [232] Klas Kronander and Aude Billard. Learning compliant manipulation through kinesthetic and tactile human-robot interaction. IEEE transactions on haptics, 7(3):367–380, 2013. 

- [233] Wentao Liu, Ruofan Wu, Jennie Si, and He Huang. A new robotic knee impedance control parameter optimization method facilitated by inverse reinforcement learning. IEEE Robotics and Automation Letters, 7(4):10882–10889, 2022. 

- [234] Neil C Thompson, Kristjan Greenewald, Keeheon Lee, and Gabriel F Manso. The computational limits of deep learning. arXiv preprint arXiv:2007.05558, 2020. 

- [235] Dmitry Baskakov and Dmitry Arseniev. On the computational complexity of deep learning algorithms. In Proceedings of International Scientifc Conference on Telecommunications, Computing and Control: TELECCON 2019, pages 343–356. Springer, 2021. 

- [236] William J Dally, Stephen W Keckler, and David B Kirk. Evolution of the graphics processing unit (gpu). IEEE Micro, 41(6):42–51, 2021. 

- [237] Rubens Luiz Rech and Paolo Rech. Reliability of google’s tensor processing units for embedded applications. In 2022 Design, Automation & Test in Europe Conference & Exhibition (DATE), pages 376–381, 2022. 

- [238] P.H.W. Leong and K.H. Tsoi. Field programmable gate array technology for robotics applications. In 2005 IEEE 

26 

The path towards contact-based physical human-robot interaction (Preprint) 

International Conference on Robotics and Biomimetics - workshop on open source software, volume 3, page 5. Kobe, ROBIO, pages 295–298, 2005. Japan, 2009. 

- [239] Brian Plancher, Sabrina M. Neuman, Thomas Bourgeat, Scott Kuindersma, Srinivas Devadas, and Vijay Janapa Reddi. Accelerating robot dynamics gradients on a cpu, gpu, and fpga. IEEE Robotics and Automation Letters, 6(2):2335–2342, 2021. 

- [240] Yuexuan Tu, Saad Sadiq, Yudong Tao, Mei-Ling Shyu, and Shu-Ching Chen. A power efficient neural network implementation on heterogeneous fpga and gpu devices. In 2019 IEEE 20th international conference on information reuse and integration for data science (IRI), pages 193–199. IEEE, 2019. 

- [241] David Kortenkamp, Reid Simmons, and Davide Brugali. Robotic systems architectures and programming. Springer handbook of robotics, pages 283–306, 2016. 

- [242] Félix Ingrand and Malik Ghallab. Deliberation for autonomous robots: A survey. Artifcial Intelligence, 247:10– 44, 2017. 

- [243] A. Meystel. Planning in a hierarchical nested controller for autonomous robots. In 1986 25th IEEE Conference on Decision and Control, pages 1237–1249, 1986. 

- [244] James S Albus et al. The nist real-time control system (rcs): An application survey. In Proc. of the AAAI 1995 Spring Symposium Series, Stanford University, Menlo Park, CA, 1995. 

- [245] Ronald C Arkin. Behavior-based robotics. MIT press, 1998. 

- [246] Faisal Qureshi, Demetri Terzopoulos, and Ross Gillett. The cognitive controller: a hybrid, deliberative/reactive control architecture for autonomous robots. In International Conference on Industrial, Engineering and Other Applications of Applied Intelligent Systems, pages 1102–1111. Springer, 2004. 

- [247] R. Brooks. A robust layered control system for a mobile robot. IEEE Journal on Robotics and Automation, 2(1):14– 23, 1986. 

- [248] Ian Horswill. Polly: A vision-based artificial agent. 

- [249] Maja J Matari´c. Integration of representation into goal-driven behavior-based robots. In The artifcial life route to artifcial intelligence, pages 165–186. Routledge, 2018. 

- [250] Daniel Toal, Colin Flanagan, Caimin Jones, and Bob Strunz. Subsumption architecture for the control of robots. IMC-13, Limerick, 1996. 

- [251] Michele Amoretti and Monica Reggiani. Architectural paradigms for robotics applications. Advanced Engineering Informatics, 24(1):4–13, 2010. 

- [252] PU Chavan, M Murugan, and PP Chavan. A review on software architecture styles with layered robotic software architecture. In 2015 International Conference on Computing Communication Control and Automation, pages 827–831. IEEE, 2015. 

- [253] Morgan Quigley, Ken Conley, Brian Gerkey, Josh Faust, Tully Foote, Jeremy Leibs, Rob Wheeler, Andrew Y Ng, et al. Ros: an open-source robot operating system. In ICRA 

- [254] Alberto Martinetti, Peter K Chemweno, Kostas Nizamis, and Eduard Fosch-Villaronga. Redefining safety in light of human-robot interaction: A critical review of current standards and regulations. Frontiers in chemical engineering, 3:32, 2021. 

- [255] Laurel Riek and Don Howard. A code of ethics for the humanrobot interaction profession. Proceedings of we robot, 2014. 

- [256] Yusuf Aydin, Ozan Tokatli, Volkan Patoglu, and Cagatay Basdogan. A computational multicriteria optimization approach to controller design for physical human-robot interaction. IEEE Transactions on Robotics, 36(6):1791–1804, 2020. 

- [257] Rossitza Setchi, Maryam Banitalebi Dehkordi, and Juwairiya Siraj Khan. Explainable robotics in human-robot interactions. Procedia Computer Science, 176:3057–3066, 2020. 

- [258] Francisco J Rodríguez Lera, Camino Fernández Llamas, Ángel Manuel Guerrero, and Vicente Matellán Olivera. Cybersecurity of robotics and autonomous systems: Privacy and safety. Robotics-legal, ethical and socioeconomic impacts, 2017. 

- [259] Adriana Hamacher, Nadia Bianchi-Berthouze, Anthony G. Pipe, and Kerstin Eder. Believing in bert: Using expressive communication to enhance trust and counteract operational error in physical human-robot interaction. In 2016 25th IEEE International Symposium on Robot and Human Interactive Communication (RO-MAN), pages 493–500, 2016. 

- [260] Yue Hu, Naoko Abe, Mehdi Benallegue, Natsuki Yamanobe, Gentiane Venture, and Eiichi Yoshida. Toward active physical human–robot interaction: Quantifying the human state during interactions. IEEE Transactions on Human-Machine Systems, 52(3):367–378, 2022. 

- [261] Nora Fronemann, Kathrin Pollmann, and Wulf Loh. Should my robot know what’s best for me? human–robot interaction between user experience and ethical design. AI & SOCIETY, 37(2):517–533, 2022. 

- [262] Ayanna Howard and Jason Borenstein. The ugly truth about ourselves and our robot creations: the problem of bias and social inequity. Science and engineering ethics, 24:1521– 1536, 2018. 

- [263] Tom Williams. The eye of the robot beholder: Ethical risks of representation, recognition, and reasoning over identity characteristics in human-robot interaction. In Companion of the 2023 ACM/IEEE International Conference on Human-Robot Interaction, HRI ’23, page 1–10, New York, NY, USA, 2023. Association for Computing Machinery. 

- [264] Antonia Meissner, Angelika Trübswetter, Antonia S ContiKufner, and Jonas Schmidtler. Friend or foe? understanding assembly workers’ acceptance of human-robot collaboration. ACM Transactions on Human-Robot Interaction (THRI), 10(1):1–30, 2020. 

- [265] Aimee van Wynsberghe, Madelaine Ley, and Sabine Roeser. Ethical aspects of human–robot collaboration in industrial 

27 

The path towards contact-based physical human-robot interaction (Preprint) 

work settings. The 21st Century Industrial Robot: When Tools Become Collaborators, pages 255–266, 2022. 

- [266] Reza Etemad-Sajadi, Antonin Soussan, and Théo Schöpfer. How ethical issues raised by human–robot interaction can impact the intention to use the robot? International journal of social robotics, 14(4):1103–1115, 2022. 

- [267] AJung Moon, Shalaleh Rismani, and HF Machiel Van der Loos. Ethics of corporeal, co-present robots as agents of influence: a review. Current Robotics Reports, 2:223–229, 2021. 

- [268] Nora Fronemann, Kathrin Pollmann, and Wulf Loh. Should my robot know what’s best for me? human–robot interaction between user experience and ethical design. AI & SOCIETY, 37(2):517–533, 2022. 

28 

