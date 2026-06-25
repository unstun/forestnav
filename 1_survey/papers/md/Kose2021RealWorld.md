---
citation_key: Kose2021RealWorld
arxiv_id: 2109.00890
arxiv_url: https://arxiv.org/abs/2109.00890
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-24T16:38:45Z
origin: ai+web
reviewed: false
---

# Testing and Results

Real life experimentation of trajectory planning algorithms on MIT RACECAR requires additional work. Until this part, MIT RACECAR platform is inspected by its hardware and software. Also, numerous helper package of ROS is expressed and how trajectory planning algorithms can be applied. For the real time testing of different trajectory planning algorithms, there should be a measurement for determining how well the algorithm works. For that purpose, an environment was set up in Artificial Intelligence and Intelligent Systems(AI2S) laboratory. As the scenery, a double lane curvy road with obstacles in different locations was chosen. MIT RACECAR was expected to stay in lane and when it encounters to an obstacle, to pass the obstacle by changing the lane.

As a result of the chosen scenery, it is needed to detect lanes on the road. For achieving this, ZED Camera was used for image processing. Image processing in this project is achieved by OpenCV library. An image processing algorithm that detects lanes and returns goal points was designed with Python. Goal points are generated from detected lanes with respect to the look ahead distance that is determined by velocity of the vehicle dynamically.

Another aspect of the project is obstacle detection. Obstacle detection is done with the help of RPLidar A2 2D lidar. RPLidar provides users a ROS package that handles communication between computer and lidar and publishes obstacle information as a ROS topic. Lastly, all of these outputs are given to the path planning algorithm as target points and obstacles.

## Test Environment

In order to create the required environment, a double lane curvy road was draw on the floor of AI2S Laboratory by electrical tapes. While making the road for MIT RACECAR, constraints like width of the vehicle, minimum turning radius of the vehicle are considered. Also, it is tried to avoid environmental effects like flare on the floor because of the lights. Since, the reference is being obtained from image processing, the flare is changing the quality of the reference signal in a bad manner and causes the vehicle to go out of the lane.

Also, the turning radius is an important constraint in such small environments, especially when obstacle avoidance is required. Thus, the curvature of the road was tried to be kept small enough to turn but also, big enough to see the limits of the algorithm.

Double lane structure of the road was chosen for lane changing when encountered by an obstacle. This structure also provides a good use case like lane changing and overtaking problems as future works. Besides, the middle lane of the road was chosen red in order to provide easier recognition of the lane. Since red color is easy to recognize with color filters like HSV, this provides a good starting point for the lane detection and leaves more time to focus on trajectory planning algorithms. The most painful part of the generated scenario for this study was that the changeable light conditions in the environment had a serious effect on the lane recognition algorithm's performance.

:::: {#fig:testing_env .figure latex-placement="h!"}
![](Kose2021RealWorld_figs/4_environment.png){width="\\linewidth"}

::: caption
Testing environment
:::
::::

## Lane Detection Algorithm

Lane detection algorithm, which is a crucial part of the scenery that is chosen for the project, will be explained in this section. Lane detection algorithm consists of OpenCV functions that will not be explained since it is out of the scope of the project. The algorithm is designed to have two main parts for its being modular and easy to understand.

:::: {.figure latex-placement="h!"}
![](Kose2021RealWorld_figs/main_flow.png){width="\\linewidth"}

::: caption
Main structure of the lane detection algorithm
:::
::::

The first part of the algorithm, the pre-processing part, is responsible for extracting lane information from camera input by eliminating everything except lanes itself from the image. The first idea for the algorithm was based on the idea to extract black lanes and red lane individually. For this purpose, a complex image processing algorithm that can be seen in Figure [1.2](#fig:pre_1){reference-type="ref" reference="fig:pre_1"} was proposed. However, the computational cost of this proposed method was not affordable for Jetson TX2. As a result of this problem, feedback loop of the system is updated only on 5-8 times average in one second and this situation was resulting in a hard control problem and slow response system.

:::: {#fig:pre_1 .figure latex-placement="h!"}
![](Kose2021RealWorld_figs/pre_1.png){width="\\linewidth"}

::: caption
Flow of the first proposed image pre-processing algorithm
:::
::::

In order to overcome these problems, a new, more plain algorithm that can be seen in Figure [1.4](#fig:pre_2){reference-type="ref" reference="fig:pre_2"} was proposed. The idea of the new algorithm is that it is not needed to find all the lanes individually, it is only needed to find red lane which is easier to find respectively. As a result, the new proposed method is less accurate but more effective and faster, and this loss of accuracy is a neglectable amount.

:::: {#fig:pre_2 .figure latex-placement="h!"}
![](Kose2021RealWorld_figs/pre_2.png){width="\\linewidth"}

::: caption
Flow of the final image pre-processing algorithm
:::
::::

The pre-processing part of the algorithm uses mainly HSV masking, morphological operations and filtering contours based on sizes and area. The flow of the algorithm with an example input image can be inspected in Figure [1.4](#fig:pre_2){reference-type="ref" reference="fig:pre_2"}.

:::: {#fig:pre_2 .figure latex-placement="h!"}
![](Kose2021RealWorld_figs/pre_example.png){width="\\linewidth"}

::: caption
Example output of pre-processing image with stages
:::
::::

The second part of the algorithm takes the binary image that is the output of the pre-processing part as input. This part of the algorithm firstly takes the perspective transformation of the lane image to the Bird-Eye view. After taking transformation, the contour information of the image is extracted and applied some filtering again. After all of these processes, a basic second degree polynomial is fit for the lane. This is required because in some cases, only a small part of the lane is visible and the coordinates of the target point at the look ahead distance is required for path planning. Additionally, some coordinate transformations is applied to the target point and the point is passed as output of the lane detection algorithm. The flow of the entire algorithm can be seen in Figure [1.5](#fig:entire_flow){reference-type="ref" reference="fig:entire_flow"} and an example output of the lane detection algorithm is also can be seen in Figure [1.6](#fig:detect_out){reference-type="ref" reference="fig:detect_out"}.

::: landscape
:::: {#fig:entire_flow .figure latex-placement="h!"}
![](Kose2021RealWorld_figs/entire_flow.png){width="\\linewidth"}

::: caption
The flow of the entire lane detection algorithm
:::
::::
:::

:::: {#fig:detect_out .figure latex-placement="h!"}
![](Kose2021RealWorld_figs/detect_out.png){width="\\linewidth"}

::: caption
An example output of the lane detection algorithm
:::
::::

## Testing and Results

In this chapter, an overall qualitative assessment of the trajectory planning algorithms is given. This assessment relies on how successfully the vehicle followed the lanes, how many obstacles the vehicle pass through without collision and some special comments on the algorithm behavior. Since there is no global position data source in AI2S laboratory environment, an overall numeric error can not be calculated.

While testing the algorithms, it is tried to keep the environment same for all the algorithms. Nevertheless, some environmental circumstances like lighting condition can be changed. During the testing a Rviz is used which can be seen in Figure [1.7](#fig:rviz){reference-type="ref" reference="fig:rviz"} for visualizing the vehicle condition from the vehicle's perspective, global plan and local plan that is manipulated by trajectory algorithm.

:::: {#fig:rviz .figure latex-placement="h!"}
![](Kose2021RealWorld_figs/global_local.png){width="\\linewidth"}

::: caption
An example Rviz view with global plan (red) and local plan (purple)
:::
::::

In addition, how the trajectory planning manipulates the target points which are determined by lane detection can be seen in Figure [1.8](#fig:manipulator){reference-type="ref" reference="fig:manipulator"}. At the top side of the figure, how the vehicle sees the environment can be seen and below the image from camera and lane detection algorithm can be seen. While the red arrow is the output of the lane detection algorithm, the purple arrows indicates the planned trajectory that will avoid the obstacle without leaving the road.

:::: {#fig:manipulator .figure latex-placement="h!"}
![](Kose2021RealWorld_figs/manipulator.png){width="\\linewidth" height="23cm"}

::: caption
An example view that trajectory planning is running (red arrow is the output of the lane detection, the purple arrows are the planned trajectory)
:::
::::

The final assessment about the trajectory planning algorithms can be inspected in Table [1.7](#tab:assessment){reference-type="ref" reference="tab:assessment"}. But as a matter of fact, it should be said that this assessment is only according to the chosen scenery, it is not about which trajectory planning algorithm is better than the others. Besides, determining which algorithm is superior to others depends on the application scenery. As a conclusion, artificial potential field algorithm has better results according to the project requests and it is chosen to continue to the project with APF algorithm from now on. Since it provides reasonable performance with low cost, when considered possible future development of the project, the APF method is chosen.

::: {#tab:assessment}
+-------------------------------------------------------------------------------+-----------------------+-------------------------------------------------------------------------------+
|                                                                               | **Obstacles Avoided** | **Comments**                                                                  |
+:=============================================================================:+:=====================:+:=============================================================================:+
| ::: {#tab:assessment}                                                         | 5 out of 7            | ::: {#tab:assessment}                                                         |
|   ----------------                                                            |                       |   -----------------------------------------------                             |
|    Dynamic Window                                                             |                       |     DWA planner is easy to implement and tune.                                |
|       Approach                                                                |                       |     Its performance was acceptable and stable.                                |
|   ----------------                                                            |                       |           Also, while avoiding obstacles,                                     |
|                                                                               |                       |     it could stay in the course, but sometimes,                               |
|   : The assessment of the experiments of the trajectory generation algorithms |                       |    its effort was not enough to avoid obstacles.                              |
| :::                                                                           |                       |      Also, it gets stuck in complex situations                                |
|                                                                               |                       |                like narrow pass ways                                          |
|                                                                               |                       |   -----------------------------------------------                             |
|                                                                               |                       |                                                                               |
|                                                                               |                       |   : The assessment of the experiments of the trajectory generation algorithms |
|                                                                               |                       | :::                                                                           |
+-------------------------------------------------------------------------------+-----------------------+-------------------------------------------------------------------------------+
| ::: {#tab:assessment}                                                         | 7 out of 7            | ::: {#tab:assessment}                                                         |
|   -------------------                                                         |                       |   ---------------------------------------------                               |
|    Time-Elastic Band                                                          |                       |    TEB planner is very successful to model the                                |
|         Planner                                                               |                       |      vehicle, and it is suitable for complex                                  |
|   -------------------                                                         |                       |    environments. But, it is very hard to tune                                 |
|                                                                               |                       |     effectively and sometimes having so many                                  |
|   : The assessment of the experiments of the trajectory generation algorithms |                       |        parameters to tune is turning into                                     |
| :::                                                                           |                       |      a disadvantage instead of an advantage.                                  |
|                                                                               |                       |         Also, since it heavily relies on                                      |
|                                                                               |                       |      an optimization problem, computational                                   |
|                                                                               |                       |          cost gets very high, especially                                      |
|                                                                               |                       |             in complex environments.                                          |
|                                                                               |                       |   ---------------------------------------------                               |
|                                                                               |                       |                                                                               |
|                                                                               |                       |   : The assessment of the experiments of the trajectory generation algorithms |
|                                                                               |                       | :::                                                                           |
+-------------------------------------------------------------------------------+-----------------------+-------------------------------------------------------------------------------+
| ::: {#tab:assessment}                                                         | 5 out of 7            | ::: {#tab:assessment}                                                         |
|   ----------------------                                                      |                       |   ----------------------------------------------                              |
|    Artificial Potential                                                       |                       |      APF is the easiest to implement and tune                                 |
|           Field                                                               |                       |      by far. Thanks to its basic logic based                                  |
|   ----------------------                                                      |                       |     on simple math, it provides an acceptable                                 |
|                                                                               |                       |          result with low cost. And also,                                      |
|   : The assessment of the experiments of the trajectory generation algorithms |                       |    in line with the application scenery that is                               |
| :::                                                                           |                       |        selected for this project, it is not                                   |
|                                                                               |                       |    too much deviates the vehicle from the road.                               |
|                                                                               |                       |   ----------------------------------------------                              |
|                                                                               |                       |                                                                               |
|                                                                               |                       |   : The assessment of the experiments of the trajectory generation algorithms |
|                                                                               |                       | :::                                                                           |
+-------------------------------------------------------------------------------+-----------------------+-------------------------------------------------------------------------------+

: The assessment of the experiments of the trajectory generation algorithms
:::
