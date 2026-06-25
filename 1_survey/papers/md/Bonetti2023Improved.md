---
citation_key: Bonetti2023Improved
arxiv_id: 2304.14043
arxiv_url: "https://arxiv.org/abs/2304.14043"
title: "Improved path planning algorithms for non-holonomic autonomous vehicles in industrial environments with narrow corridors: Roadmap Hybrid A* and Waypoints Hybrid B*. Roadmap hybrid A* and Waypoints hybrid A* Pseudocodes"
authors_short: "Alessandro Bonetti et al."
year: 2023
direction_tag: F_hybrid_astar
source: mineru-vlm
converter: mineru-open-api
model: vlm
converted_at: 2026-06-25T08:29:21Z
origin: ai+web
reviewed: false
---

# IMPROVED PATH PLANNING ALGORITHMS FOR NON-HOLONOMIC AUTONOMOUS VEHICLES IN INDUSTRIAL ENVIRONMENTS WITH NARROW CORRIDORS: ROADMAP HYBRID A\* AND WAYPOINTS HYBRID A\*

# Roadmap Hybrid A\* and Waypoints Hybrid A\* Pseudocodes

Alessandro Bonetti
University of Modena and Reggio Emilia,
Via Amendola 2, Pad. Morselli - 42122 Reggio Emilia, Italy
alessandro.bonetti@unimore.it

Simone Guidetti

Gruppo TecnoFerrari S.p.a. con socio unico,

Via Ghiarola Nuova, 105, 41042 Fiorano Modenese (MO), Italy

simone\_guidetti@tecnoferrari.it

Lorenzo Sabattini

University of Modena and Reggio Emilia,

Via Amendola 2, Pad. Morselli - 42122 Reggio Emilia, Italy
lorenzo.sabattini@unimore.it

## Contents

1 Proposed solutions 3  
1.1 Roadmap Hybrid A\* 4  
1.2 Waypoint Hybrid A\* 6

## 1 Proposed solutions

In order to overcome the issues that have arisen from the standard version of Hybrid A\* in the industrial environment described in Section 2, two new global path planners are presented: Roadmap Hybrid A\* and Waypoint Hybrid A\*. For the development of both algorithms, some preliminary steps were required. To begin, the map was divided manually into rectangular zones. This division aimed to provide a topological representation of the environment, composed of machine servicing areas and corridors. The former are represented by green rectangles, while the corridors are depicted by pink rectangles, as shown in Fig. 1. A topological graph of the plant was then set up using the NetworkX [1] python library by imposing the connections between these rectangular zones.

![](Bonetti2023Improved_figs/ca8e6e7a64ab2bb8b8acbaa5fb845937c302ea30ada5ad8fff035ae4ebc151b5.jpg)  
Figure 1: The image shows the topological map of the plant, highlighting areas with green borders containing machines and narrow corridors marked in pink. The map features Bezier curve segments, with the red curves driven forward by the vehicle and the blue ones in reverse. Furthermore, the legend identifies the different types of segments used in corridors and entry and exit maneuvers. The numbers in the image uniquely identify the endpoints of each segment Bezier curve, enabling to define connections between them. Two segments are connected if they share the same endpoint.

To complete the preliminary steps required for implementing the algorithms, we manually designed the corridor segments and the machine entrance and exit segments for the AMR using Bezier curves. The corridor curves were drawn in the center to maximize the distance between the AMR and the walls, while machinery entry and exit curves were designed in order to minimize the vehicle footprint while maneuvering and ensuring safety. To accomplish this, we carefully selected the control points of each Bezier curve so as to obtain a collision-free and feasible path for the vehicle. The former condition is achieved by applying a collision checking algorithm that compares the bounding box of the vehicle with the grid map cells on the poses traversed by the vehicle. The latter condition is achieved by checking the maximum curvature of each curve segment and ensuring that consecutive segments have matching tangents to guarantee smoothness.

Then we collected the connectivity relationships between all the curves into a graph, on which a graph search algorithm is applied to extract the fixed path parts needed to form the final path of the proposed algorithms.

In Fig. 1, the red segments represent the forward fixed sections of the path traveled by the vehicle, while the blue segments represent the reverse ones. The blue segments are only used for the entrance to the machines, as the uploading and downloading tools are located at the back of the vehicle.

In conclusion, the topological map graph and the Bezier curve segment graph are obtained in order to implement the Roadmap Hybrid A\* and Waypoint Hybrid A\* algorithms, as detailed in the following subsections.

## 1.1 Roadmap Hybrid A\*

In this subsection, we propose Roadmap Hybrid A\*, a novel path planning technique for autonomous mobile vehicles subject to non-holonomic constraints. The technique combines two different methods: a graph search algorithm applied to fixed segments and the Hybrid A\* algorithm. The former is used in obstacle-free zones and for maneuvering in and out of machines to guarantee a robust and predictable path. The latter provides flexibility and the ability to navigate around obstacles in more dynamic areas.

Roadmap Hybrid A\*, as described in pseudo-code in Algorithm 1, uses the start and goal nodes of the vehicle, the Bezier segment graph, the topological graph, and the grid map as input to initiate the planning process. The first step is to identify the entry and exit paths, as well as the corresponding attachment and detachment nodes. The exit path is the fixed segment curve that allows the vehicle to safely exit the starting machine and whose end points are the start and detachment nodes. Following the same principle, the entry path is the fixed curve that the AMR must travel to enter the destination station and whose end points are the goal and detachment nodes. The attachment and detachment nodes serve as transition points between the free motion of the vehicle provided by Hybrid A\* and the fixed path during the entry or exit processes.

The next step involves determining the start and goal areas using the Even-Odd rule $[2]$ , which is a technique used in computational geometry to determine if a point lies inside or outside a closed polygonal curve in a two-dimensional plane. The rule consists in drawing a straight line from that point in any direction and counting the number of intersections of the line with the shape. If this number is odd, the point is inside; if even, the point is outside. The Even-Odd rule works for any simple or complex polygon, and it was applied to the rectangular areas and the positions of the start and goal machine nodes, as shown from line 3 to 10 of the pseudo-code. If the start and goal areas are different, Roadmap Hybrid A\* uses Dijkstra's algorithm to determine the sequence of areas that the vehicle must traverse. The sequence of corridors, the Bezier curve paths within them and the corresponding ordered endpoint list are also found at this stage. As shown from lines 17 to 28 of Algorithm 1, the fixed-path segment endpoints, as well as the attachment and detachment nodes, are then connected using standard Hybrid A\*. The detachment pose is linked to the first endpoint, and the even-indexed endpoints are linked to the odd-indexed ones. Finally, the last endpoint is connected to the attachment node. As shown in line 30 of Algorithm 1, if the initial area matches the target area instead, the detachment pose is directly connected with the attachment pose using Hybrid A\*.

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 1 RoadMap Hybrid A*

Input: $q_{start}, q_{goal}, \text{TopologicalGraph}, \text{SegmentGraph}, \text{GridMap}$

Output: FinalPath

1: ExitPath, DetachmentPose ← FindExitPath($q_{start}, SegmentGraph$)
2: EntryPath, AttachPose ← FindEntryPath($q_{goal}, SegmentGraph$)
3: for each area ∈ TopologicalGraph do
4:    if EvenOddRule($q_{start}, area$) then
5:    StartArea = area
6:    end if
7:    if EvenOddRule($q_{goal}, area$) then
8:    GoalArea = area
9:    end if
10: end for
11: if StartArea ≠ GoalArea then
12:    AreasSequence ← DijkstraAlgorithm(TopologicalGraph, StartArea, GoalArea)
13:    CorridorsSequence ← FindCorridorsSequence(AreasSequence)
14:    CorridorPath, EndPoints ← FindCorridorsPath(CorridorsSequence, SegmentGraph)
15:    HybridAstarPaths ← ∅
16:    numEndPoints ← number of EndPoints
17:    for i = 1 to numEndPoints do
18:    if i = 1 then
19:    HybridAstarPathi ← HybridAstar(DetachmentPose, EndPoints[i], GridMap)
20:    else if i = numEndPoints then
21:    HybridAstarPathi ← HybridAstar(Endpoints[i], AttachPose, GridMap)
22:    else if i is even then
23:    HybridAstarPathi ← HybridAstar(Endpoints[i], EndPoints[i+1], GridMap)
24:    else
25:    continue to next iteration
26:    end if
27:    HybridAstarPaths ← HybridAstarPaths ∪ HybridAstarPathi
28:    end for
29: else
30:    HybridAstarPaths ← HybridAstar(DetachmentPose, AttachPose, GridMap)
31: end if
32: FinalPath ← ExitPath ∪ CorridorPath ∪ HybridAstarPaths ∪ EntryPath
33: return FinalPath
</div>

Finally, the exit path, corridor path, Hybrid A\* paths, and entry path are concatenated to produce the final output of the algorithm. An example of RoadMap Hybrid A\* is shown in Fig. 2.

![](Bonetti2023Improved_figs/84f1ad45778301c3ac6bc857c1c71cee0a3515430822beedd7a53f4a1da73bb4.jpg)  
Figure 2: Roadmap Hybrid A\* path planned from node 13 to 19. The legend identifies the exit path, Hybrid A\* path, corridor path and entry path parts.

## 1.2 Waypoint Hybrid A\*

In this subsection, the Waypoint Hybrid A\* path planner is presented. The implementation of this algorithm aimed to evaluate the cost-effectiveness of using waypoints in narrow corridors compared to the static roadmap employed in Roadmap Hybrid A\*.

Waypoint Hybrid A\* takes inspiration from the planner described in [3], where waypoints were generated by applying a visibility graph and then connected by means of Hybrid A\*. In [3], it has been found that using waypoints to guide the Hybrid A\* to its destination results in a 40% faster run-time. In this research we propose to adapt the waypoints principle in a slightly different way in order to speed up computational time but also trying to avoid oscillating paths produced by Hybrid A\*.

Waypoint Hybrid A\*, as presented in the pseudo-code in Algorithm 2, uses the start and goal nodes of the vehicle, the Bezier segment graph, the topology graph, and the grid map of the environment as input. To begin the planning process, as explained with Roadmap Hybrid A\* in Subsection 1.1, the algorithm finds the entry and exit paths as well as the attachment and detachment nodes. After that, from lines 3 to 10, the initial and target areas are determined by applying the Even-Odd rule to the rectangular shape zones and the start and goal node positions. If the starting and target areas are different, the algorithm employs Dijkstra's algorithm to determine the sequence of areas through which the vehicle must pass. The ordered sequence of waypoints is then defined as the midpoint of the free space connection width between consecutive zones.

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 2 Waypoint Hybrid A*

Input: $q_{start}, q_{goal}, \text{TopologicalGraph}, \text{SegmentGraph}, \text{GridMap}$

Output: FinalPath

1: ExitPath, DetachmentPose ← FindExitPath($q_{start}, \text{SegmentGraph}$)
2: EntryPath, AttachPose ← FindEntryPath($q_{goal}, \text{SegmentGraph}$)
3: for each area ∈ TopologicalGraph do
4:    if EvenOddRule($q_{start}, \text{area}$) then
5:    StartArea = area
6:    end if
7:    if EvenOddRule($q_{goal}, \text{area}$) then
8:    GoalArea = area
9:    end if
10: end for
11: if StartArea ≠ GoalArea then
12: AreasSequence ← DijkstraAlgorithm(TopologicalGraph, StartArea, GoalArea)
13: Waypoints ← FindWaypointsSequence(AreasSequence)
14: HybridAstarPaths ← ∅
15: numWaypoints ← number of Waypoints
16: for i = 1 to numWaypoints do
17:    if i = 1 then
18:    HybridAstarPath₀ ← HybridAstar(DetachmentPose, Waypoints[i], GridMap)
19:    HybridAstarPaths ← HybridAstarPaths ∪ HybridAstarPath₀
20:    HybridAstarPathᵢ ← HybridAstar(Waypoints[i], Waypoints[i+1], GridMap)
21: else if i = numWaypoints then
22:    HybridAstarPathᵢ ← HybridAstar(Waypoints[i], AttachPose, GridMap)
23:    else
24:    HybridAstarPathᵢ ← HybridAstar(Waypoints[i], Waypoints[i+1], GridMap)
25:    end if
26:    HybridAstarPaths ← HybridAstarPaths ∪ HybridAstarPathᵢ
27:    end for
28: else
29:    HybridAstarPaths ← HybridAstar(DetachmentPose, AttachPose, GridMap)
30: end if
31: FinalPath ← ExitPath ∪ HybridAstarPaths ∪ EntryPath
32: return FinalPath
</div>

From line 16 to 27 of Algorithm 2, the waypoints, the attachment node and detachment node are connected using standard Hybrid A\*. The detachment pose is connected to the first waypoint, then each waypoint is connected with its successor except for the last one, which is connected with the last endpoint. As shown in line 29 of Algorithm 2, if the initial area matches the target area, the detachment pose is directly connected with the attachment pose using Hybrid A\*. It is worth noting that, if this condition is verified, the output of Roadmap Hybrid A\* and Waypoint Hybrid A\* are exactly the same. Finally, the exit path, Hybrid A\* paths, and entry path are concatenated to produce the final path of the algorithm, as show in Fig. 3.

![](Bonetti2023Improved_figs/9af2faa82406bbf0c925ede9411a112b958c69cc6ef41154e50ae25e7df1144c.jpg)  
Figure 3: Waypoint Hybrid A star path planned from node 13 to 19. The legend identifies the exit path, Hybrid A\* path and entry path parts.

## References

[1] A. A. Hagberg, D. A. Schult, and P. J. Swart, “Exploring network structure, dynamics, and function using networkx,” in Proceedings of the 7th Python in Science Conference, G. Varoquaux, T. Vaught, and J. Millman, Eds., Pasadena, CA USA, 2008, pp. 11 – 15.

[2] J. D. Foley, A. van Dam, S. Feiner, and J. Hughes, Computer Graphics: Principles and Practice. Reading, MA: Addison-Wesley, 1990.

[3] S. Sedighi, D.-V. Nguyen, and K.-D. Kuhnert, “Guided hybrid a-star path planning algorithm for valet parking applications,” in 2019 5th International Conference on Control, Automation and Robotics (ICCAR), 2019, pp. 570–575.