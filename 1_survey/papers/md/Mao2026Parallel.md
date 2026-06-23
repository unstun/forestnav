---
citation_key: Mao2026Parallel
arxiv_id: 2603.22508
arxiv_url: "https://arxiv.org/abs/2603.22508"
title: "Parallel OctoMapping: A Scalable Framework for Enhanced Path Planning in Autonomous Navigation"
authors_short: "Yihui Mao et al."
year: 2026
direction_tag: H_hierarchical_planning
source: pymupdf4llm
converted_at: 2026-06-23T17:52:43Z
origin: ai+web
reviewed: false
---

1 

## Parallel OctoMapping: A Scalable Framework for Enhanced Path Planning in Autonomous Navigation 

Yihui Mao, Tian Tan, Xuehui Shen, Warren E. Dixon, and Rushikesh Kamalapurkar 

_**Abstract**_ **—Mapping is essential in robotics and autonomous systems because it provides the spatial foundation for path planning. Efficient mapping enables planning algorithms to generate reliable paths while ensuring safety and adapting in real time to complex environments. Fixed-resolution mapping methods often produce overly conservative obstacle representations, which can lead to suboptimal paths or planning failures in cluttered scenes. To address this issue, we introduce Parallel OctoMapping (POMP), an efficient OctoMap-based mapping technique that preserves more navigable free space and supports multi-threaded computation. To the best of our knowledge, POMP is the first method that refines the representation of free space at a fixed occupancy-grid resolution without changing the underlying grid structure, while preserving compatibility with existing searchbased planners. It can therefore be integrated into existing planning pipelines, yielding higher pathfinding success rates and shorter path lengths, especially in cluttered environments, while substantially improving computational efficiency. An interactive web-based demonstration illustrating the mapping and planning behavior of POMP is available on the project webpage.**[1] 

_**Index Terms**_ **—OctoMap, occupancy mapping, autonomous navigation, path planning, search-based planning, parallel computing.** 

## I. INTRODUCTION 

Understanding the environment is fundamental to autonomy in mobile robotics. A well-designed mapping method that enforces spatial consistency across observations, produces an accurate and memory-efficient representation of the environment, and supports fast, informative spatial queries is thus a critical component of modern autonomy systems. Therefore, good map representations improve the reliability of downstream planning and collision-avoidance modules, enabling safer, higher-quality trajectories and ultimately more robust autonomous navigation [1]–[5]. 

In online navigation, mapping accuracy alone is insufficient. The mapping module must also meet time and computation constraints, supporting fast construction and frequent updates without sacrificing fidelity (runtime efficiency), while keeping 

This research is supported, in part, by the Air Force Research Laboratory under Grant No. FA8651-24-1-0019, the Air Force Office of Scientific Research under Grant No. FA9550-19-1-0169, and the U.S. Army Research Laboratory under Grant No. W911NF-25-2-0045. Any opinions, findings, and conclusions or recommendations expressed in this material are those of the author(s) and do not necessarily reflect the views of the sponsoring agencies. Yihui Mao, Xuehui Shen, Warren E. Dixon, and Rushikesh Kamalapurkar are with the Department of Mechanical and Aerospace Engineering, University of Florida, Gainesville, FL 32611 USA (e-mail: _{_ yihui.mao, xuehuishen, wdixon, rkamalapurkar _}_ @ufl.edu). 

Tian Tan is with the Department of Electrical and Systems Engineering, University of Pennsylvania, Philadelphia, PA 19104 USA (e-mail: tiantan@alumni.upenn.edu). 

1https://maoyihui53.github.io/pomp-demo/ 

memory usage bounded through sparse representations (memory efficiency). During execution, the map should provide online querying capability, allowing the planner to obtain the spatial information it needs, so that mapping and planning can work together within a unified navigation pipeline (continuous usability). OctoMap is a widely adopted representation for 3D occupancy mapping because its sparse octree structure enables memory-efficient storage, multi-resolution queries, and incremental updates [1]. However, in large environments with dense point clouds and high update rates, a standard OctoMap pipeline can become compute-bound and may struggle to sustain real-time throughput. 

Search-based methods are widely used for planning because they integrate naturally with grid and voxel maps and can provide completeness and optimality guarantees under standard assumptions [6]–[9]. The performance of search-based planning, however, is strongly influenced by map resolution and the choice of representation. With fixed resolution cells, typical occupancy grids may mark an entire cell as occupied when a relatively small portion of an obstacle falls within it. The conservative labeling rule can unnecessarily mark traversable space as non-traversable, resulting in broken connectivity in narrow passages, increased search effort, degraded path quality, and in some cases planning failures in cluttered scenes [10]. A straightforward remedy is to increase the grid resolution, but this substantially increases mapping computation and memory consumption, enlarges the search graph, and ultimately lengthens planning time. Motivated by these limitations, we seek map representations that better exploit within-cell free space to preserve narrow passages without globally refining the resolution, while remaining efficient for online planning. 

To address the limitations of fixed-resolution mapping for path planning, we propose an efficient mapping technique based on OctoMap that accelerates map construction through multi-threaded parallel computation and maximizes the utilization of cell space at fixed resolution. While conventional methods conservatively label an entire cell as occupied whenever it contains even a small portion of an obstacle, Parallel OctoMapping (POMP) performs a finer-grained analysis of the internal clustered spatial distribution of the point cloud to safely reclaim significant navigable space that would otherwise be inaccessible under traditional methods. In summary, our contributions are as follows: 

- A novel OctoMap-based mapping technique (POMP) is developed that improves grid/voxel space utilization in 2D and 3D by subdividing each fixed-resolution grid/cell into distinct sub-regions. By introducing clear, safe, 

2 

and unsafe states based on the clustered spatial distribution of the point cloud, this method unlocks significant navigable space overlooked by conservative Occupancy Grid Map (OGM) methods. 

- POMP performs parallel, multi-threaded computation, significantly reducing map construction time in large environments with dense point clouds and frequent updates. 

- POMP improves pathfinding success rate and path quality of search-based path planning while reducing mapping time compared with conventional fixed-resolution occupancy grid methods. 

## II. RELATED WORK 

## _A. Mapping Representations and Frameworks_ 

Point clouds, commonly captured in robotic tasks like mapping and planning, often contain excessive points and sensor noise, making them less suitable for efficiently representing large-scale environments. One simple alternative is the grid/voxel map, which partitions space into uniform squares/cubes to represent the scene; however, many of these remain unexplored in each sensor measurement, leading to a substantial memory overhead. 

Tree-based representations have been studied to overcome these issues. The OctoMap [1] is a well-established representation that uses an Octree, which divides 3D space into eight subspaces that have the same volume. OctoMaps compactly and probabilistically represent an environment with occupancy states, including unknown, occupied, or free. 

In recent years, a variety of mapping frameworks [1], [11]–[17] have been proposed to improve map representation and computational efficiency. In addition, some of these frameworks [18]–[20] facilitate navigation by providing map representations that are more suitable for path planning. Truncated Signed Distance Fields (TSDFs) [2], [21], originally used in computer graphics, represent geometry implicitly by storing truncated signed distance to the observed surface. In practice, TSDF values are updated using distances projected along the sensor ray, and they are maintained only within a narrow truncation band around the surface. Voxblox [18] builds upon TSDF by incrementally constructing Euclidean Signed Distance Fields (ESDFs) from the TSDF map, allowing efficient queries of the Euclidean distance from each voxel to the nearest obstacle to support path planning. FIESTA [19] is another well-known fast incremental ESDF mapping framework for online motion planning of aerial robots. It computes the ESDF directly from an occupancy grid map and builds a growing global map, and has been reported to achieve higher accuracy and computational performance compared to Voxblox in its experiments. 

## _B. Planning on Structured Maps_ 

Discrete volumetric occupancy maps are typically implemented using one of three commonly used structures: uniform voxels [22]–[24], Octrees (e.g., OctoMap [1]), and hashed voxel/block structures [18], [25]. 

Occupancy grid mapping, where uniform voxel cells discretize the space, is easy to implement and aligns well with 

data from LiDAR and RGB-D cameras; however, dense implementations allocate memory uniformly across the bounded map volume, which leads to rapidly increasing memory usage as the resolution becomes finer. Octree–based representations such as OctoMap provide hierarchical, memory–efficient storage and naturally support multi–resolution updates, but their pointer–based hierarchy incurs _O_ (log _n_ ) access time and makes neighborhood queries across different depths cumbersome. Hashed voxel/block structures can achieve sparse access in expected near _O_ (1) access time and scale well to large environments, but suffer from potential hash collisions and require careful memory management. 

To combine the strengths of these approaches while avoiding their weaknesses, we use the octree solely as a parallel point cloud reader and storage backend, streaming its leaf states to a fixed-resolution occupancy grid in real time. Atomic updates propagate each leaf change to the corresponding grid cell without race conditions, so the planner operates on a grid array with per-voxel access time of _O_ (1) and constantstride neighbor checks, without traversing the tree during planning, while the map remains sparsely represented in the tree. This decoupled design preserves the octree’s efficient incremental construction and provides the planner with a contiguous grid array for fixed-stride access, enabling fast search-based planning. 

## III. PRELIMINARIES 

## _A. OctoMap and Occupancy Grid Mapping Overview_ 

OctoMap [1] is a 3D occupancy mapping framework that uses an Octree-based data structure to efficiently store, update, and query volumetric information. An Octree is a hierarchical structure that recursively subdivides 3D space into cubic volumes, or voxels, starting from a root node and continuing until a predefined resolution is reached. 

The occupancy grid map for pathfinding is generated from the Octree built in the mapping process. The OctoMap and the occupancy grid map are configured as follows. 

**Octree Configuration.** The first step is to align the OctoMap with the workspace of interest. We set the root center **c** root of the Octree to coincide with the geometric center **c** map of the environment bounds along each coordinate axis. Let _Lx, Ly, Lz_ denote the side lengths of the workspace along the _x_ , _y_ , and _z_ axes. We then define _L_ max = max _{Lx, Ly, Lz}_ as the maximum extent of the environment. The depth _n_ of the Octree is determined by the smallest resolution _r_ (i.e., the edge length of a leaf cube). Since each additional tree level subdivides a cube into 8 smaller ones, the minimum depth required to achieve a leaf size _r_ is computed as 


![](1_survey/papers/md/Mao2026Parallel_figs/Mao2026Parallel.pdf-0002-19.png)


The depth guarantees that the root node has a side length _S_ 0 = 2 _[n] r_ which is large enough to cover the maximum workspace dimension _L_ max in all directions. Intuitively, this step defines the “outer box” of the Octree and ensures that the leaf nodes match the desired map resolution. 

3 

**Grid Configuration.** _Nx_ , _Ny_ , and _Nz_ denote the numbers of leaf nodes along the _x_ , _y_ , and _z_ axes after discretizing the half of the workspace with leaf size _r_ : 


![](1_survey/papers/md/Mao2026Parallel_figs/Mao2026Parallel.pdf-0003-02.png)


where _Lx_ , _Ly_ , and _Lz_ are the workspace extents along the _x_ , _y_ , and _z_ axes, respectively. 

The origin of the occupancy grid, **o** grid, is placed at the vertex with the smallest coordinates in all three dimensions: 


![](1_survey/papers/md/Mao2026Parallel_figs/Mao2026Parallel.pdf-0003-05.png)


Finally, the grid dimensions are defined as: 

dim _x_ = 2 _Nx_ + 1 _,_ dim _y_ = 2 _Ny_ + 1 _,_ dim _z_ = 2 _Nz_ + 1 _,_ 

The grid configuration guarantees that the occupancy grid is symmetrically aligned with the octree root, spans the full environment, and extends by half a cell ( _r/_ 2) beyond the outermost octree leaf nodes. 

## _B. Parallelization of octree construction_ 

A dense point cloud input can make OctoMap construction a computational bottleneck, given that the commonly used implementation is often used in a single-threaded or effectively sequential manner in practice. Sequential processing limits throughput and responsiveness in real time mapping tasks, especially when handling large-scale or high-frequency sensor data. In addition, the hierarchical nature of the octree makes fine-grained parallelization difficult, because both updates and queries require root-to-leaf traversal, and concurrent operations may contend for shared nodes, necessitating synchronization to avoid race conditions. 

Existing efforts to accelerate OctoMap can be broadly divided into hardware-assisted and software-based approaches. Hardware solutions, such as OMU [26], improve performance but reduce portability across the heterogeneous computing platforms used in robotic systems. Other hardware-assisted methods, including NanoMap [27], OctoMap-RT [16], OctoMap build based on Super Rays [15] and GPU-accelerated OctoMap [28], mainly accelerate ray tracing, yet octree updates can still remain the dominant cost. Software approaches are more limited. VoxelCache [29] reduces voxel-access latency through on-chip caching of recently used voxel-block pointers, but it does not parallelize OctoMap tree construction. SkiMap [30] improves efficiency by replacing the octree with a Tree of SkipLists and is thus better regarded as an alternative mapping structure than a direct optimization of OctoMap. Among software methods that preserve the OctoMap octree, OctoCache [14] is the closest, although its gains mainly arise from caching and workflow-level concurrency rather than true parallel updates within a single Octree. 

We parallelize OctoMap construction with Intel oneAPI Threading Building Blocks (oneTBB), a task-based C++ library whose work-stealing scheduler balances the irregular, fine-grained tasks in voxel updates [31]. Compared with GPU approaches [16], [28], CPU parallelism can avoid host–device 

transfer costs when data reside on the CPU and often better matches the branching and sparse access patterns of Octree updates. Among CPU options, both OpenMP and oneTBB support dynamic scheduling and task parallelism. We choose oneTBB for its composable task-graph API and work-stealing runtime, which can better accommodate many small, irregular tasks than a simple thread-pool design. 

To ensure correctness during concurrent updates, we employ the compare-and-swap (CAS) instruction, an atomic primitive supported by most modern multiprocessor architectures. CAS atomically compares the value at a memory location with an expected value and, only if they match, updates it to a new value. During parallel octree construction, when multiple threads concurrently attempt to create the same child node, each thread allocates a candidate node and uses CAS to atomically update the corresponding child pointer from null to that node. If the CAS fails, the thread discards the candidate node and proceeds with the child that has already been created by another thread. Each successful CAS thus ensures that only one thread initializes a given child pointer, preventing duplicate node creation under contention. Compared with the mutex-based locking used in OctoMap, this CAS-based design enables fine-grained child-node creation, reducing lock contention, thread blocking, and context-switch overhead, thereby improving the parallel throughput and scalability of hierarchical octree updates. 


![](1_survey/papers/md/Mao2026Parallel_figs/Mao2026Parallel.pdf-0003-15.png)


**----- Start of picture text -----**<br>
Map Structure Mapping Strategy<br>Leaf<br>Point Clouds Octree OccupancyUpdate OR Point CloudStorage<br>Construction<br>(Section V-B) Region State Determination<br>Configuration<br>Cell<br>Alignment Occupancy Diagonal Examination<br>(Section III-A) Grid Map<br>Navigability State<br>Mapping Determination<br>(Section V-C) (Section V-D & E)<br>Planning Search-Based Pathfinding<br>**----- End of picture text -----**<br>


Fig. 1. System overview of our proposed mapping framework 

## IV. OVERVIEW 

Fig. 1 provides an overview of the proposed POMP framework. The framework consists of two tightly coupled components: (i) an OctoMap backend for real-time map construction, and (ii) a planner-facing fixed-resolution occupancy grid map (OGM) to support efficient search-based planning. Specifically, the OctoMap is continuously updated online, and the leaf-level region states are projected onto the OGM to determine the navigability of each corresponding grid cell for planning. 

Because the OctoMap and the OGM are tightly coupled, their spatial relationship is explicitly defined (see Section IIIA). In particular, the OctoMap leaf-node size is set equal to the OGM cell size. The number of OGM cells is selected to 

4 

TABLE I 

TERMINOLOGY AND NOTATION. 

|**Category**|**Term**|**Defnition**|**Sym.**|
|---|---|---|---|
|OctoMap|node|A hierarchical spatial unit in the Octree<br>corresponding to a cubic region of space.||
||leaf size|The edge length of a leaf node.|_r_|
||threshold|A user-defned range to classify points as<br>unsafe, safe or clear for navigation.|thr|
||occupied<br>state|A state in which the OctoMap node contains<br>point cloud.||
||unoccupied<br>state|A state where no point cloud is marked in an<br>OctoMap node.||
|Region|region|A leaf node equally separated into 4 regions in<br>2D and 8 regions in 3D.||
||unsafe state|A region state in a leaf node with points<br>outside the range set by the threshold.||
||safe state|A region whose points remain within the<br>threshold bound and are treated as axis-aligned<br>traversable.||
||clear state|A region state in a leaf node without a point<br>cloud.||
|Occupancy<br>Grid Map|grid|A discrete unit of the 2D occupancy grid map.||
||voxel|A discrete unit of the 3D occupancy grid map.||
||resolution|The grid/voxel edge length, same as the leaf<br>size in our method.|res|



be larger by one along each axis than the number of OctoMap leaf nodes, and it is shifted by a half-cell offset so that the two discretizations are staggered by half of the cell size. This arrangement yields a consistent, overlap-based correspondence between OctoMap leaf nodes and OGM cells, enabling reliable projection of leaf-level region states onto the grid for planning. Due to half-cell offset, the leaf-node boundaries at the chosen depth often pass through the centers of OGM cells, effectively slicing the original grid and introducing additional split lines; because these boundaries are uniformly spaced, any narrow passage of sufficient width (larger than the chosen OGM cell resolution) must be intersected by at least one boundary (pigeonhole principle) and therefore cannot be “skipped” by discretization. We then apply occupancy thresholding with a safety margin to preserve the required clearance even when an obstacle occupies only a small fraction of an OGM cell (See the Region block in Fig. 2 and the left panel of Fig. 3). POMP starts by acquiring a stream of point clouds, either directly from range sensors (e.g., LiDAR) or from an existing point cloud map. An OctoMap is then constructed with a predefined leaf resolution, where incoming measurements are integrated through leaf-node point storage and/or occupancy updates (see Section V-B). Based on the resulting leaf-level statistics, we assign each leaf-node region a navigability label (unsafe / safe / clear) based on occupancy thresholding, and use this label to evaluate the traversability of the corresponding OGM cell, as discussed in Sections V-C and V-D. 

The developed method fundamentally overcomes a key limitation of existing mapping techniques. The conventional methods [32], [33] employ overconservative occupancy labeling, marking a grid cell as fully occupied regardless of whether it is densely filled or contains only a few sparse points. Our approach, described in Algorithm 1 and Algorithm 2, performs a targeted subdivision at the leaf node to unlock navigable free space in OGM for motion planning. This process retains a significant portion of the free space that would otherwise 

be deemed untraversable. The resulting OGM thus provides a substantially larger configuration space for path planners, directly enhancing both the probability of finding a valid path and the quality of the solution in complex environments. 

## V. POMP DESIGN AND IMPLEMENTATION 

In this section, we present the implementation of the data structures and algorithms. The terminology and notation used in this paper are summarized in Table I. 


![](1_survey/papers/md/Mao2026Parallel_figs/Mao2026Parallel.pdf-0004-09.png)


**----- Start of picture text -----**<br>
3 4 2<br>7 8 6 1 2 3 4 5 6 7 8<br>1<br>**----- End of picture text -----**<br>


Fig. 2. Parallel insertion of point clouds into the Octree with concurrent node construction. Each leaf node is subdivided into 4 regions in 2D or 8 regions in 3D. In the figure, “ ” represents occupied, “ ” represents unoccupied, and “ ” denotes the threshold bounding box. The bounding box is centered on a leaf node and used to determine the region state; by default, the edge length of the bounding box is set to half the leaf size. The regions are classified as clear “ ” (no points), safe “ ”, or unsafe “ ” (see Fig.3). 

## _A. Data Structure_ 

In **Data Structure 1** , Lines 2 and 3 define common attributes of a standard Octree node: the node’s size and pointers to its child nodes. The atomic type is used to enable concurrent (thread-safe) modifications to the child pointers without requiring a mutex, allowing safe node creation and point insertion in parallel. Line 3 stores atomic child pointers, which enable concurrent child creation during parallel insertion. In 2D, each node has four children, whereas in 3D it has eight. In line 4, we optionally store point coordinates in each leaf node using a concurrent vector. A concurrent vector is a thread-safe data structure that allows multiple threads to insert or access elements simultaneously without explicit locking, thus preventing race conditions during tree construction. Line 5 defines safe_state: an atomic bitmask records the occupancy and safety of regions within a leaf node (8 bits in 2D and 16 bits in 3D). Using an atomic type ensures thread-safe updates during concurrent point insertions. 

**Data Structure 2** includes the pointer to the top-level node of the Octree, serving as the root for accessing and traversing the entire tree in Line 2. The map in Line 4 is for pathfinding, which is formally introduced in **Data Structure** 

5 

## **Data Structure 1:** OctreeNode 

## **1 Structure:** 

**2** double node_size; **3** array _<_ atomic _<_ OctreeNode* _>_ ,8 _>_ children; **4** concurrent vector _<_ PointType _>_ points; **5** atomic _<_ uint16 t _>_ safe_state _{_ 0 _}_ ; 

**3** . The leafsize is a given value that represents the leaf node size, and is the same as the resolution of the map in **Data Structure 3** . 

## **Data Structure 2:** Octree 

## **1 Structure:** 

- **2** OctreeNode* root; **3** double leafsize; **4** OccupancyGridMap* map; 

**Data Structure 3** is the OccupancyGridMap, where Line 3 references an array of unsigned char (1 byte) occupancy state for thread-safe parallel updates. It plays the same role as occupancy grid cells but is designed to minimize conservative full-occupancy labels, improving spatial efficiency. The resolution (Line 2) represents the size of each voxel in the map. 

## **Data Structure 3:** OccupancyGridMap 

## **Algorithm 1:** Parallel Octree Build 

**Input:** Points _P_ **1 Function** TreeBuild( _P_ ) **: 2 foreach** _p ∈P_ _**in parallel**_ **do 3** ParallelInsertPoints( _p, root_ ) 

**Input:** Points p, OctreeNode node **1 Function** ParallelInsertPoints( _p, node_ ) **: 2 if** _node is leaf_ **then 3** push _p_ into node.points **4** set_safe_state( _p_ , node) **5 return 6 else 7** _idx ←_ node.get_child_idx( _p_ ) **8** childPtr _←_ node.children[ _idx_ ] **9** child _←_ AtomicLoad(childPtr) **10 if** _child is nullptr_ **then 11** newNode _←_ new OctreeNode **12** old _←_ nullptr **13** ok _←_ CAS(childPtr _,_ old _,_ newNode) **14 if** _ok_ **then 15** child _←_ newNode **16 else 17** destroy(newNode) **18** child _←_ AtomicLoad(childPtr) **19** ParallelInsertPoints( _p_ , child) 

## **1 Structure:** 

**2** double resolution; **3** atomic _<_ unsigned char _>_ * voxels; 

## _B. Parallel Octree Construction_ 


![](1_survey/papers/md/Mao2026Parallel_figs/Mao2026Parallel.pdf-0005-16.png)


**----- Start of picture text -----**<br>
c<br>thr<br>h<br>**----- End of picture text -----**<br>


Fig. 3. Illustration of the threshold setup and region classification: clear , safe, and unsafe. The left panel depicts the boundary of the area, where _h_ denotes half the edge length of an OctoMap leaf node (equal to the map resolution r), and the threshold distance is thr = _h ·_ ratio, with ratio specified at initialization. Red points lie outside the thresholded boundary, while blue points lie inside; these points determine the region safe state label (unsafe / safe / clear). 

The parallel Octree construction follows the standard octree insertion procedure, which is illustrated in Fig. 2, but inserts points concurrently using multiple threads (see **Algorithm 1** ). We parallelize point insertion by distributing the input points across threads; each thread traverses the tree from the root to the corresponding leaf for every point it inserts. Using parallel threads to access the same node can lead to 

## **Input:** Points p, OctreeNode node 

**1 Function** set_safe_state( _p, node_ ) **: 2** _c ←_ node.center; **3** _h ←_ node.size * 0.5; **4** idx _←_ node.get_child_idx( _p_ ) **5** offset _←_ number of regions **6** mask _←_ 1u<<(idx+offset) **7 if** _∥p − c∥∞ ≥ h · ratio_ **then 8** mask _←_ mask|1u<<(idx) **9** AtomicOr(node.safe_state,mask) 

race conditions; therefore, whenever constructing a new child under a parent node, we first check whether the pointer is nullptr. An atomic compare-and-swap (CAS) is used to safely construct child nodes during parallel point insertion. A new node is constructed only if the child pointer remains nullptr at the time of the operation. A successful CAS atomically sets the corresponding child pointer to the newly allocated node, whereas failure indicates that another thread has already constructed the child, in which case the newly allocated node is discarded. This process is repeated recursively until reaching a leaf node, whose size corresponds to the predefined resolution. 

Each OctoMap leaf node is subdivided into four regions in 2D or eight regions in 3D. During the point insertion (see the set_safe_state function), each point is checked against 

6 


![](1_survey/papers/md/Mao2026Parallel_figs/Mao2026Parallel.pdf-0006-01.png)


Fig. 4. Illustration of the mapping configuration from Octree leaf nodes (left) to leaf regions and their projection onto the OGM (right). The occupancy grid is shown with a dash–dot outline, OctoMap nodes with a long-dashed outline, and region partitions with solid lines. 

the leaf node center _c_ . A region is marked unsafe if it contains any point whose perpendicular distance to _any_ axisaligned splitting line/plane (used to partition the leaf cube) exceeds the threshold _thr_ = _h·ratio_ , where _h_ is half of the leafcube edge length. Equivalently, max _i |pi − ci| ≥ thr_ , where _pi_ and _ci_ are the _i_ -th coordinate components of the point _p_ and the leaf center _c_ , respectively, and the splitting planes pass through _c_ . 

This threshold provides a margin so that points too close to the boundary ~~are conservatively treated as obsta~~ cles. If all points in the region lie within this margin, the region is marked safe. If the region contains no points, it is marked clear. All settings are illustrated in Fig. 3. For compact storage, these states are encoded in a single safe_state variable. In 2D, for each region _i_ , bit _i_ + 4 records whether the region is non-clear, i.e., whether it contains at least one point, and bit _i_ records whether the region is unsafe. Thus, a region is clear if neither bit is set, safe if only the nonclear bit is set, and unsafe if both the non-clear bit and the unsafe bit are set. The 3D case uses the same encoding with eight regions, where bits 8–15 record non-clear states and bits 0–7 record unsafe states. Note that unsafe, safe, and clear are the three region states we use to evaluate safety for navigability. A region is non-clear if it has been visited by points, which includes both the unsafe and safe cases. This atomic encoding allows multiple threads to update the safe state of different regions in parallel without requiring locks. The state of each region determines the navigability of its corresponding occupancy grid/voxel. 

## _C. Mapping Implementation_ 

The OctoMap and the OGM are tightly coupled: the OctoMap is continuously updated online, as described in Section V-B, and the OGM used for pathfinding is derived from the OctoMap. The region safe states in the leaf level, as shown in Fig. 3, are used to infer the navigability of the corresponding OGM cells, and the inferred navigability is then used to assign the occupancy of each cell. Fig. 4 illustrates the spatial correspondence between the OctoMap and the OGM over the entire map. 

In Algorithm 2, the constructed OctoMap is traversed from the root to the leaves using the function traverse(node). At each leaf node, we call project_onto_OGM(node) to mark the occupancy of the corresponding OGM cell. This 


![](1_survey/papers/md/Mao2026Parallel_figs/Mao2026Parallel.pdf-0006-08.png)


Fig. 5. Illustration of the diagonal examination pairs and rules for determining grid navigability. is the unsafe region in the leaf node, is the safe region in the leaf node, and is the clear region in the leaf node. The arrow represents the direction of examination. The floating square with a black border indicates that the corresponding cell of OGM should be marked as occupied after the examination. 

function applies diagonal examination (see Fig. 5) to determine the navigability of the OGM cell containing the region, as well as the navigability of the OGM cell containing its diagonal region, and accordingly assigns the occupancy of that cell using set_cell_Occupied(idx). Here, from_idx and to_idx follow the arrow direction illustrated in Fig. 5. 

## _D. Diagonal Examination_ 

In a standard occupancy grid map, a free cell has up to 8 neighbors in 2D and up to 26 neighbors in 3D. Accordingly, motion primitives can be categorized into two types: axisaligned and diagonal moves. 

Under our alignment configuration, the OGM is shifted by a half-cell offset so that the two discretizations are staggered by half of the cell size. Consequently, each OGM cell overlaps multiple OctoMap leaf regions: four in 2D and eight in 3D. A clear region contains no obstacles and is navigable in all directions; a safe region is assumed to be navigable only in axis-aligned directions; and an unsafe region is not 

7 


![](1_survey/papers/md/Mao2026Parallel_figs/Mao2026Parallel.pdf-0007-01.png)


**----- Start of picture text -----**<br>
1 2 3 2 3<br>1<br>2<br>4 5 6 5<br>3<br>8<br>4 7<br>5 6 9<br>7 8 9 8<br>**----- End of picture text -----**<br>


Fig. 6. Illustration of the OGM produced by our method. This panel shows the bottom-right corner of the map in Fig. 4. For clarity, the OGM cell boundaries are drawn with a black dash-dotted outline, and the leaf-node boundary is shown as a gold long-dashed box. The nine OGM cells are labeled 1–9, and nine representative points are shown, colored by whether they lie inside or outside the threshold bound. The occupancy of diagonal pairs of OGM cells is determined by using Fig. 5. The arrows indicate the feasible navigations between grid cells, and the colors encode each cell’s feasible navigations. Colored crosses mark the point cloud blocked during the Diagonal Examination for the corresponding colored cells. 


![](1_survey/papers/md/Mao2026Parallel_figs/Mao2026Parallel.pdf-0007-03.png)


**----- Start of picture text -----**<br>
Algorithm 2: Occupancy Grid Mapping<br>Input: OctreeNode node<br>1 Function project_onto_OGM( node ) :<br>2 if region[from idx] is clear then<br>3 if region[to idx] is not clear then<br>4 set_cell_Occupied(to_idx)<br>5 else<br>6 if region[from idx] is safe then<br>7 if region[to idx] is not clear then<br>8 set_cell_Occupied(to_idx)<br>9 else<br>10 set_cell_Occupied(from_idx)<br>11 else<br>12 if region[to idx] is unsafe then<br>13 set_cell_Occupied(to_idx)<br>14 set_cell_Occupied(from_idx)<br>**----- End of picture text -----**<br>


**Input:** OctreeNode node **1 Function** traverse( _node_ ) **: 2 if** _node is Leaf_ **then 3** project_onto_OGM( _node_ ) **4 else 5 foreach** _child ∈ node_ _**in parallel**_ **do 6** traverse(child) 

navigable in any direction. We leverage this decomposition and let the regions jointly determine whether an OGM cell should be marked as occupied (see Fig. 6). 

By design, any cell that does not contain an unsafe region 

is navigable in axis-aligned directions. Thus, we only need to design occupancy rules using diagonal navigability. For example, all cells except for cells 1 and 4 in Fig. 6 are axisaligned navigable. Cells 6, 7, and 9 are nevertheless marked as occupied due to diagonal navigability considerations. 

Using the presence of points in leaf-node regions to directly determine diagonal navigability is overly conservative. For example, in Fig. 6, although all cells except 2 and 3 appear to be diagonally non-navigable due to the presence of the points marked in blue, cells 5 and 8 can be safely marked unoccupied, which preserves axis-aligned navigation through cells 2, 5, and 8, and diagonal navigation between cells 3 and 5. 

Navigability of diagonal pairs of OGM cells is determined using the corresponding diagonal regions of the leaf node that overlaps them. In the 2D case, the four regions of a leaf node yield two diagonal pairs, labeled [1 _,_ 4] _,_ [2 _,_ 3] in Fig. 2. In the 3D case, the eight regions of a leaf node yield four diagonal pairs, labeled [1 _,_ 8] _,_ [2 _,_ 7] _,_ [3 _,_ 6] _,_ [4 _,_ 5] in Fig. 2. As shown in Fig. 5, the navigability of diagonal regions is orderindependent. Accordingly, in 2D only two diagonal pairs need to be examined, whereas in 3D only four diagonal examination directions are required. 

## _E. Navigability State Determination_ 

The rules for determining navigability of diagonal pairs of OGM cells are shown in Table II. All cells in the OGM are initialized as unoccupied. Cells containing one or more unsafe regions are marked occupied. Cells containing only clear regions are marked unoccupied. Since safe regions are navigable in axis-aligned directions but not along diagonal directions, marking either the cell containing the safe region or its diagonally adjacent cell as occupied is sufficient to block diagonal navigation between the two cells (e.g., cells 1 and 5, cells 5 and 7, and cells 5 and 9 in Fig. 6). 

Based on the above discussion, the rules for occupancy assignment can be summarized as follows (see Fig. 5): 

8 

TABLE II 

NAVIGABILITY STATE DETERMINATION TABLE BASED ON THE DIAGONAL EXAMINATION 

|**Region pair**|**Axis-dir. **|**navigability**|**Diag-dir. **|**navigability**|**Marking in cell**|**Notes**|
|---|---|---|---|---|---|---|
|**[unsafe unsafe]**|unsafe: **✗✗✗**|unsafe: **✗✗✗**|unsafe: **✗✗✗**|unsafe: **✗✗✗**|Marking both diagonal cells as|Axis-aligned: _∥p −c∥∞≥h · ratio ⇒_**✗✗✗**|
||||||occupied|Diagonal: both regions contain points _⇒_**✗✗✗**|
|**[safe safe]**|safe: **✓✓**<br>**✓**|safe: **✓✓**<br>**✓**|safe: **✗✗✗**|safe: **✗✗✗**|Mark one as occupied to block|Axis-aligned: _∥p −c∥∞< h · ratio ⇒_**✓✓**<br>**✓**|
||||||diagonal access while preserving|Diagonal: both regions contain points _⇒_**✗✗✗**|
||||||axis-aligned navigation in the other region||
|**[clear clear]**|clear: **✓✓**<br>**✓**|clear: **✓✓**<br>**✓**|clear: **✓✓**<br>**✓**|clear: **✓✓**<br>**✓**|Keep unoccupied in both diagonal|Both regions do not contain points _⇒_**✓✓**<br>**✓**|
||||||cells||
|**[unsafe safe]**|unsafe: **✗✗✗**|safe: **✓✓**<br>**✓**|unsafe: **✗✗✗**|safe: **✗✗✗**|Mark the unsafe cell as occupied.|Axis-aligned: _∥p −c∥∞≥h · ratio ⇒_**✗✗✗**|
||||||Allow axis-aligned navigation in the safe|_∥p −c∥∞< h · ratio ⇒_**✓✓**<br>**✓**|
||||||region.|Diagonal: both regions contain points _⇒_**✗✗✗**|
|**[unsafe clear]**|unsafe: **✗✗✗**|clear: **✓✓**<br>**✓**|unsafe: **✗✗✗**|clear: **✓✓**<br>**✓**|Mark the unsafe cell as occupied.|Axis-aligned: _∥p −c∥∞≥h · ratio ⇒_**✗✗✗**|
||||||Allow axis-aligned and diagonal|Diagonal: unsafe region is non-empty _⇒_**✗✗✗**|
||||||navigation in the clear region.|The clear region contains no points _⇒_**✓✓**<br>**✓**|
|**[safe clear]**|safe: **✓✓**<br>**✓**|clear: **✓✓**<br>**✓**|safe: **✗✗✗**|clear: **✓✓**<br>**✓**|Mark the safe cell as occupied. Allow|Axis-aligned: _∥p −c∥∞< h · ratio⇒_**✓✓**<br>**✓**|
||||||axis-aligned and diagonal navigation in|Diagonal: safe region is non-empty _⇒_**✗✗✗**|
||||||the clear region.|The clear region contains no points _⇒_**✓✓**<br>**✓**|



_Note:_ **✓✓✓** / **✗✗[✗]** denote navigable/non-navigable in the indicated direction; color denotes the region state. Notes summarize the navigability criteria for each region pair, and the Marking in cell column describes the POMP cell-marking strategy for preserving navigability. 


![](1_survey/papers/md/Mao2026Parallel_figs/Mao2026Parallel.pdf-0008-05.png)


Fig. 7. Top row (POMP): Using the obstacle setup in Fig. 4 and the mapping rule in Fig. 5, POMP assigns each region an unsafe/safe/clear label (top left), updates the corresponding occupancy grid cells and their valid navigations between cells (top middle), and produces the final occupancy map (top right). Compared to direct OGM, POMP preserves more valid navigations (blue). Bottom row (direct OGM): For the same point cloud map, a standard occupancy grid voxelizes space (bottom left), marks a cell as occupied if it contains any points and ma ~~rks the valid navigations between cells (bott~~ om middle), and yields the final occupancy map (bottom right). 

- 1) **Safety hierarchy:** regions are prioritized in the order of their safety levels as clear, safe, and unsafe. 

- 2) **Mixed pair:** when two diagonally paired regions have different safety levels, the cell containing the safer region is designated as unoccupied, while the cell containing the less safe region is occupied. 

- 3) **Equal pair:** 

   - if both regions are unsafe, both cells are designated as occupied; 

   - if both regions are safe, designate either cell as 

## occupied and the other as unoccupied; 

- if both regions are clear, then both cells are designated as unoccupied; 

Note that each OGM cell overlaps multiple pairs of diagonal leaf-node regions (4 in 2D and 8 in 3D). If any of the diagonal pairs of leaf-node region results in an occupied designation, the cell is marked as occupied. Otherwise, it remains unoccupied (see Fig. 7). To prevent race conditions caused by cells participating in multiple examinations, we use atomic operations for both the region safe state update and the 

9 


![](1_survey/papers/md/Mao2026Parallel_figs/Mao2026Parallel.pdf-0009-01.png)


**----- Start of picture text -----**<br>
start<br>end<br>**----- End of picture text -----**<br>



![](1_survey/papers/md/Mao2026Parallel_figs/Mao2026Parallel.pdf-0009-02.png)



![](1_survey/papers/md/Mao2026Parallel_figs/Mao2026Parallel.pdf-0009-03.png)


Fig. 8. Paths planned using POMP (red) and direct (traditional) OGM (blue) superimposed on the point cloud (a) and on the occupancy grid (b). The orange box (enlarged on the right) highlights the region responsible for the shorter path. Differences between our POMP and direct OGM are highlighted in (c) by cell (1)-(5). These cells are classified as unoccupied by POMP but occupied by the direct OGM. In particular, keeping cells (2) and (3) free in our method explains the shorter path found, as it preserves a traversable narrow passage (see middle figure). 

cell-level occupancy update. In addition, octree construction and projection onto the OGM are executed sequentially rather than asynchronously. 

The comparison between POMP and direct OGM, using an identical point cloud, is shown in Fig. 7 and Fig. 8. In Fig. 7, the cells that contain points, but are marked by POMP as unoccupied, are highlighted in blue. These cells result in a feasible path connecting the start and the goal, whereas the direct OGM admits no such path. Fig. 8 shows another case where POMP produces a shorter (red) path by preserving more navigable space. 

## VI. EXPERIMENTS 

In this section, we present randomized experiments to illustrate specific characteristics of the POMP algorithm, followed by offline experiments on real-world datasets and ROS bag simulations to demonstrate POMP’s performance. Except for Experiment B-1(a), all experiments are implemented in ROS 2 and conducted on an Intel Core Ultra 9 285 (2.50 GHz) system with 24 cores and 24 threads. 

In the following, five experiments on randomized datasets are presented to illustrate the performance of POMP for tree construction, OGM construction, navigability, and planning. 

## _A. Randomized Point Clouds_ 


![](1_survey/papers/md/Mao2026Parallel_figs/Mao2026Parallel.pdf-0009-11.png)


Fig. 9. Two maps utilized in the randomized point-cloud experiments. 

_1) Tree Construction:_ In this experiment, we focus exclusively on evaluation of the computational efficiency of the Octree construction module of POMP. POMP is compared against three state-of-the-art incremental tree construction methods: i- Octree, ikd-Tree, and PCL Octree, for spatial representation across different leaf sizes. For evaluation, datasets contain- 


![](1_survey/papers/md/Mao2026Parallel_figs/Mao2026Parallel.pdf-0009-14.png)


**----- Start of picture text -----**<br>
Construction Time vs. Leaf Size  (500K Points)<br>120 POMP octree i-Octree ikd-Tree PCL octree<br>100<br>80<br>15.0<br>60 12.5<br>0.01 0.02<br>40<br>20<br>0.01 0.02 0.03 0.04 0.05 0.06 0.07<br>Leaf Size (m)<br>Construction Time vs. Leaf Size  (1M Points)<br>POMP octree i-Octree ikd-Tree PCL octree<br>250<br>200<br>150 30<br>25<br>100 0.01 0.02<br>50<br>0.01 0.02 0.03 0.04 0.05 0.06 0.07<br>Leaf Size (m)<br>Construction Time vs. Leaf Size  (2M Points)<br>600 POMP octree i-Octree ikd-Tree PCL octree<br>400 60<br>55<br>0.01 0.02<br>200<br>0.01 0.02 0.03 0.04 0.05 0.06 0.07<br>Leaf Size (m)<br>Run Time (ms)<br>Run Time (ms)<br>Run Time (ms)<br>**----- End of picture text -----**<br>


Fig. 10. _Experiment A-1:_ Runtime comparison with point clouds, showing from top to bottom: 500 _,_ 000, 1 _,_ 000 _,_ 000, and 2 _,_ 000 _,_ 000 points. 

10 

ing 500 _,_ 000, 1 _,_ 000 _,_ 000, and 2 _,_ 000 _,_ 000 points are randomly generated within a 10 m _×_ 10 m _×_ 10 m workspace, and tree construction was repeated 200 times for each dataset using varying leaf sizes (0.01 m, 0.02 m, 0.03 m, 0.04 m, 0.05 m, 0.06 m and 0.07 m). 

As shown in Fig. 10, across three datasets, POMP is at least 2 _×_ faster than i-Octree [34], 7–10 _×_ faster than ikd-Tree [35], and about 9 _×_ faster than PCL Octree [36], while maintaining similarly low standard deviations across resolutions. These results demonstrate that, from a data-structure perspective, POMP achieves consistently higher tree construction throughput than state-of-the-art tree construction techniques. 

_2) OctoMap Construction & Occupancy Mapping:_ The second experiment evaluates the total runtime of OctoMap construction and the subsequent projection of region safe states from leaf nodes onto OGM cell occupancy, and compares it with three baselines: a direct OGM method, a mutexprotected parallel OctoMap (OctoMap-MTX), and the original OctoMap. In direct OGM method, the environment is discretized into grid cells, and each point in the point cloud directly updates the occupancy state of its corresponding cell. The OctoMap-MTX is a mutex-protected shared octree for parallel octree construction. To establish a strong lock-based baseline, we go beyond a naive shared-octree design with per-node mutexes. OctoMap-MTX still inserts all points into a single shared tree, but first partitions large point clouds by upper-level octree buckets and schedules the resulting disjoint subtrees to different workers. This retains the synchronization overhead of a shared-tree implementation while avoiding excessive fine-grained lock contention during bulk insertion. The original OctoMap baseline directly uses the official OctoMap implementation [1], where each input point updates the occupancy state of its corresponding octree node. 

This experiment utilizes static uniform random cylinder environments. Cylinders are randomly distributed within the workspace defined by _x ∈_ [ _−_ 10 _,_ 10], _y ∈_ [ _−_ 10 _,_ 10], and _z ∈_ [ _−_ 5 _,_ 5] (meters). A total of 50 million, 5 million, and 500 thousand points are sampled, with the cylinder radius uniformly drawn from [0 _._ 8 _,_ 1 _._ 0] m. To ensure robustness, 500 independent trial maps are generated under this configuration. 

The results are shown in Fig. 11. To highlight the efficiency of our method, we compare our method with direct OGM. Across varying resolutions, our method is approximately 4–6 _×_ faster than the direct OGM method for 50M points, 2–3 _×_ faster for 5M points, and slightly faster for 500K points. Notably, this runtime includes both OctoMap construction and the subsequent projection onto an OGM, but it still outperforms the direct method. These results indicate that POMP better supports real-time updates and continuous map availability, especially for dense point clouds, which is critical for online planning in large-scale, high-rate sensing scenarios. 

_3) Navigability:_ In the third experiment, we evaluate the navigability performance of POMP on randomized 3D worlds of size 50 m _×_ 50 m _×_ 50 m uniformly populated with three geometric shapes, including spheres, right circular cones, and axis-aligned boxes. The metric used to assess navigability is navigable space ratio (NSR), defined as the ratio of navigable cells to total cells. To assess performance across spatial 


![](1_survey/papers/md/Mao2026Parallel_figs/Mao2026Parallel.pdf-0010-07.png)


**----- Start of picture text -----**<br>
Mapping Performance (50M Points)<br>POMP Direct OGM OctoMap-MTX Original OctoMap<br>1000 1402 1388 1383 1389 1373 1375<br>500 608.2 621.8 631.7 613.5 612.0 625.2<br>100 182.7 183.4 182.9 183.7 182.5 183.0<br>50 40.91 33.24 28.51 29.50 26.62 28.62<br>0.5 1.0 1.5 2.0 2.5 3.0<br>Resolution (m)<br>Mapping Performance (5M Points)<br>POMP Direct OGM OctoMap-MTX Original OctoMap<br>100 138.1 134.9 134.7 134.1 132.4 132.9<br>57.56 53.19 51.99 52.06 51.53 50.68<br>50<br>16.96 16.97 17.08 16.99 16.91 16.89<br>10 6.480 5.881 5.517 5.587 5.969 6.361<br>5<br>0.5 1.0 1.5 2.0 2.5 3.0<br>Resolution (m)<br>Mapping Performance (500K Points)<br>POMP Direct OGM OctoMap-MTX Original OctoMap<br>10 14.14 13.90 13.77 13.62 13.65 13.56<br>5 5.013 4.242 3.665 3.750 3.539 3.517<br>1.761 1.801 1.827 1.863 1.853 1.894<br>1 1.262 1.268 1.330 1.653 1.7 6 8 1.8 9 3<br>0.5 1.0 1.5 2.0 2.5 3.0<br>Resolution (m)<br>Run Time (ms)<br>Run Time (ms)<br>Run Time (ms)<br>**----- End of picture text -----**<br>


Fig. 11. Experiment A-2: Comparison of the total runtime of OctoMap construction and the subsequent projection of region safe states from leaf nodes onto OGM cell occupancy, against three baseline map representations (direct OGM, OctoMap-MTX and the original OctoMap). The y-axis is shown in log scale. 

resolutions, we vary the resolution from 0 _._ 5 to 5 _._ 0 m in 0 _._ 5 m increments and generate 200 independent worlds for each resolution. Each world contains 100 spheres, 100 cones, and 100 boxes (300 obstacles in total), with their surfaces uniformly sampled into generated point clouds containing 600 _,_ 000 points. 


![](1_survey/papers/md/Mao2026Parallel_figs/Mao2026Parallel.pdf-0010-10.png)


**----- Start of picture text -----**<br>
Navigability Performance<br>100% POMP OGM<br>80%<br>60%<br>40%<br>20%<br>0%<br>0.0 0.5 1.0 1.5 2.0 2.5 3.0 3.5 4.0 4.5 5.0 5.5<br>Resolution (m)<br>NSR<br>**----- End of picture text -----**<br>


Fig. 12. Experiment A-3: Comparison of the navigable space ratio (NSR) across OGM cell resolutions. 

As shown in Fig. 12, across varying resolutions POMP outperforms the direct occupancy grid construction, achieving up to about 10% higher NSR at coarse resolutions. These results demonstrate that, at a fixed occupancy grid resolution, POMP refines the free space representation by reducing overly conservative occupancy labeling, thereby enlarging the feasible planning space for search-based planners. 

_4) Planning Performance:_ The fourth experiment evaluates planning performance using the same randomized datasets as in the second experiment. The start and goal positions are fixed at ( _−_ 9 _, −_ 9 _, −_ 2) and (9 _,_ 9 _,_ 2), respectively. A total of 

11 


![](1_survey/papers/md/Mao2026Parallel_figs/Mao2026Parallel.pdf-0011-01.png)


**----- Start of picture text -----**<br>
Planning  A* Planning JPS<br>5 A* on POMP 5 JPS on POMP<br>A* on OGM JPS on OGM<br>4 4<br>3 3<br>2 2<br>1 1<br>0 0<br>0.75 1.00 1.25 1.50 1.75 2.00 0.75 1.00 1.25 1.50 1.75 2.00<br>Pathfinding Rate Pathfinding Distance<br>100 POMP  48 POMP<br>80 OGM  44 OGM<br> 40<br>60<br> 36<br>40<br> 32<br>20<br> 28<br>0  24<br>0.75 1.00 1.25 1.50 1.75 2.00 0.75 1.00 1.25 1.50 1.75 2.00<br>Resolution (m) Resolution (m)<br>Planning Time (ms) Planning Time (ms)<br>Path Length (m)<br>Pathfinding Rate (%)<br>**----- End of picture text -----**<br>


Fig. 13. Experiment A-4: Planning runtime and path length are reported only when both approaches successfully found a path. Note that at a resolution of 2.0 m, across all 500 trial maps, no path was found in the direct OGM, but paths were still found in the POMP maps. 

500 independent trial maps are generated, and we evaluate the runtime of planning with two search-based pathfinding algorithms, A* and Jump Point Search (JPS). The evaluation metrics include planning runtime, pathfinding success rate, and path length, under both direct occupancy grid construction and POMP in varying resolutions. For a fair comparison, all cells outside the environment boundary are marked as occupied in all trials. When comparing path lengths, comparisons are made only when both approaches are able to find a path. 

The results in Fig. 13 indicate that, for search-based planners (A* and JPS), POMP incurs essentially no additional planning-time overhead compared with direct OGM. However, across varying map resolutions, POMP substantially improves the pathfinding success rate and consistently reduces the resulting path length. 

_5) Performance Comparison Across Threshold Ratio:_ The fifth experiment evaluates the effect of the threshold ratio on planning performance. In contrast to the fourth experiment, we consider a continuous-motion scenario with a single environment populated by uniformly random cubes. Cubes are initially distributed within the workspace _x ∈_ [ _−_ 25 _,_ 25], _y ∈_ [ _−_ 25 _,_ 25], and _z ∈_ [ _−_ 25 _,_ 25]. A total of 800 cubes are placed in the workspace, resulting in a point cloud of approximately 70,000 points. The cube side lengths are uniformly distributed over [1 _._ 0 _,_ 2 _._ 0] m. Each cube independently selects a fixed random direction and then moves for 500 frames, translating 1 to 2 m per frame. When a cube contacts the workspace boundary, its motion follows a specular reflection rule, with the angle of incidence equal to the angle of reflection. 

Threshold ratios of _ratio ∈{_ 0 _._ 95 _,_ 0 _._ 75 _,_ 0 _._ 50 _,_ 0 _._ 25 _}_ are evaluated and compared against a direct OGM baseline. For path planning, the start and the goal are fixed at ( _−_ 20 _, −_ 20 _, −_ 20) and (20 _,_ 20 _,_ 20), respectively. 

As reported in Table III, decreasing the threshold ratio makes the safety margin more conservative, which reduces the effective navigable space and leads to a gradual decrease in planning success rate. However, for every evaluated resolution 

TABLE III 

EXPERIMENT A-5: PATHFINDING RATE ACROSS 500 FRAMES WITH VARYING THRESHOLD RATIO 

||**Resolution (m)**<br>**1.0**<br>**1.5**<br>**2.0**<br>**2.5**<br>**3.0**<br>**3.5**<br>**4.0**|
|---|---|
|**POMP 0.95**<br>**POMP 0.75**<br>**POMP 0.50**<br>**POMP 0.25**<br>**OGM**|82.2%<br>68.8%<br>58.8%<br>50.0%<br>38.4%<br>23.0%<br>15.4%<br>82.2%<br>67.4%<br>57.7%<br>46.4%<br>37.6%<br>21.8%<br>14.4%<br>81.4%<br>66.8%<br>56.3%<br>43.0%<br>35.0%<br>19.6%<br>13.0%<br>81.4%<br>66.4%<br>55.8%<br>42.4%<br>34.0%<br>19.0%<br>12.4%<br>81.4%<br>66.4%<br>55.6%<br>42.0%<br>32.2%<br>16.2%<br>9.6%|



and ratio, POMP still outperforms the direct OGM baseline in pathfinding rate, demonstrating that the free-space refinement feature of POMP enlarges the feasible planning space while allowing the conservativeness to be tuned via _ratio_ . 

## _B. Offline experiments on Real-world Datasets_ 


![](1_survey/papers/md/Mao2026Parallel_figs/Mao2026Parallel.pdf-0011-13.png)


Fig. 14. Benchmark maps used in the application experiments include Cambridge 15, Cambridge 16, Cloud 7, Apartment 0, Apartment 1, and Apartment 2. 

TABLE IV 

DETAILS OF MAPS IN DATASETS FOR BENCHMARK EXPERIMENT 

||**Dataset**||**Map dimensions (m**3**)**|**Point number**|
|---|---|---|---|---|
||Cambridge<br>Cambridge<br>Cloud<br>7|15<br>16|400 _×_ 400 _×_ 60<br>400 _×_ 400 _×_ 35<br>45 _×_ 104 _×_ 12|119684095<br>113159239<br>12915992|
||Apartment|0|9.4 _×_ 14.8 _×_ 5.3|4564613|
||Apartment|1|10.7 _×_ 7.9 _×_ 2.9|1909995|
||Apartment|2|9.4 _×_ 10.2 _×_ 2.8|2136963|



We evaluate POMP in real-world scenarios using three public datasets: SensatUrban [37], Replica [38] and Treescope [39]. SensatUrban is an urban-scale photogrammetric point cloud dataset with nearly three billion points from three UK cities; Replica provides high quality reconstructions of diverse indoor environments. Treescope is the first robotics dataset in precision agriculture and forestry designed specifically for counting and mapping trees in forest 

12 

TABLE V 

EXPERIMENT B-1(A): CONSTRUCTION RUNTIME (MS) OF OCTOMAP, OCCUPANCY GRID MAP, AND OURS UNDER VARYING RESOLUTIONS ON FIVE MAPS (20-THREAD CPU) 

|**Dataset**<br>**Resolution (m)**|**Cambridge**<br>**15**<br>1.0<br>3.0<br>5.0|**Cambridge**<br>**16**<br>1.0<br>3.0<br>5.0|**Apartment**<br>**0**<br>0.05<br>0.10<br>0.50|**Apartment**<br>**1**<br>0.05<br>0.10<br>0.50|**Apartment**<br>**2**<br>0.05<br>0.10<br>0.50|
|---|---|---|---|---|---|
|**OctoMap**<br>**OctoMap-MTX** <br>**OGM**<br>**Ours**|5089.00 4893.54 4878.26 <br> 2695.07 2650.77 2511.81 <br>454.99<br>450.45<br>447.62<br>**314.25**<br>**244.38**<br>**220.13**|4825.89 4626.40 4613.28 <br>2528.09 2446.34 2346.05 <br>430.51<br>425.16<br>421.18<br>**296.04**<br>**233.06**<br>**214.62**|364.46 236.26 190.91 <br> 112.45 102.49<br>86.37<br>**17.11**<br>17.68<br>16.94<br>19.71<br>**13.04**<br>**8.07**|152.30 97.51 79.40 <br>40.87<br>36.98 33.38<br>**7.16**<br>7.01<br>7.02<br>7.22<br>**4.57**<br>**4.04**|168.87 109.26 89.23<br>45.62<br>41.39<br>37.37<br>8.35<br>7.99<br>7.26<br>**8.40**<br>**5.40**<br>**4.11**|



TABLE VI 

EXPERIMENT B-1(B): CONSTRUCTION RUNTIME (MS) OF OCTOMAP, OCCUPANCY GRID MAP, AND OURS UNDER VARYING RESOLUTIONS ON FIVE MAPS (24-THREAD CPU) 

|**Dataset**<br>**Resolution (m)**|**Cambridge**<br>**15**<br>1.0<br>3.0<br>5.0|**Cambridge**<br>**16**<br>1.0<br>3.0<br>5.0|**Apartment**<br>**0**<br>0.05<br>0.10<br>0.50|**Apartment**<br>**1**<br>0.05<br>0.10<br>0.50|**Apartment**<br>**2**<br>0.05<br>0.10<br>0.50|
|---|---|---|---|---|---|
|**OctoMap**<br>**OctoMap-MTX**<br>**OGM**<br>**Ours**|3336.56<br>3222.84<br>3209.94<br>1873.78<br>1826.14<br>1721.92<br>437.32<br>433.98<br>427.26<br>**213.78**<br>**158.74**<br>**135.08**|3167.78<br>3047.52<br>3039.78<br>1724.86<br>1677.24<br>1613.94<br>417.36<br>407.78<br>403.34<br>**205.08**<br>**151.14**<br>**128.54**|220.76<br>144.46<br>121.60<br>63.84<br>57.66<br>48.41<br>17.46<br>16.82<br>16.12<br>**17.20**<br>**11.78**<br>**6.58**|88.18<br>59.50<br>51.10<br>16.7<br>15.44<br>14.16<br>**7.24**<br>6.90<br>6.92<br>8.02<br>**5.88**<br>**3.16**|99.44<br>67.50<br>57.98<br>18.92<br>17.06<br>15.82<br>**8.08**<br>8.02<br>8.10<br>8.68<br>**6.84**<br>**3.64**|



## TABLE VII 

EXPERIMENT B-2 AND B-3: PATHFINDING METRICS ACROSS RESOLUTIONS. 

|**Resolution (m)**|**Cambridge**<br>**15**<br>2<br>6<br>10<br>14|**Cambridge**<br>**16**<br>2<br>6<br>10<br>14|**Cloud 7**<br>0.5<br>1.0<br>1.5<br>2.0<br>2.5|
|---|---|---|---|
|**OGM Pathfnding (%)**<br>**POMP Pathfnding (%)**|84.1<br>46.7<br>36.7<br>20.2<br>**91.5**<br>**68.8**<br>**50.2**<br>**45.1**|81.4<br>24.6<br>7.0<br>0.4<br>**82.7**<br>**29.6**<br>**7.5**<br>**6.3**|82.8<br>45.2<br>25.0<br>5.4<br>0.7<br>**92.1**<br>**68.4**<br>**44.9**<br>**33.6**<br>**16.4**|
|**OGM Path Length (m)**<br>**POMP Path Length (m)**|225.46<br>218.34<br>233.43<br>211.10<br>**225.42**<br>**218.30**<br>**233.40**<br>**210.90**|222.58<br>241.99<br>177.16<br>-<br>**222.42**<br>**237.70**<br>**176.64**<br>-|45.90<br>48.08<br>52.62<br>33.23<br>-<br>**45.84**<br>**47.70**<br>**50.94**<br>**31.22**<br>-|
|**A* on OGM (ms)**<br>**A* on POMP (ms)**|217.113<br>**5.148**<br>**0.853**<br>**0.03**<br>**215.331**<br>5.497<br>0.995<br>0.084|130.048<br>3.045<br>0.071<br>-<br>**122.764**<br>**2.72**<br>**0.029**<br>-|**86.984**<br>**8.314**<br>**1.928**<br>**0.074**<br>-<br>91.589<br>10.246<br>2.692<br>0.167<br>-|
|**JPS on OGM (ms)**<br>**JPS on POMP (ms)**|**114.408**<br>**1.518**<br>0.204<br>**0.001**<br>123.703<br>1.715<br>**0.188**<br>0.001|67.955<br>1.289<br>0.014<br>-<br>**67.514**<br>**1.13**<br>**0.001**<br>-|**43.827**<br>**4.454**<br>**1.104**<br>**0.019**<br>-<br>48.234<br>5.239<br>1.524<br>0.074<br>-|



_Note:_ “-” indicates that insufficient common successful trials were available for the comparison of path length and pathfinding time. 

and orchard environments. The datasets Cambridge_15 and Cambridge_16 from SensatUrban, Apartment_0, Apartment_1, and Apartment_2 from Replica, and Cloud_7 from WSF-19 in Treescope are used for evaluation (See Fig. 14). Dataset details are provided in Table IV. 

_1) Map Construction Performance:_ Map construction runtime of POMP is evaluated against three baselines: direct OGM and OctoMap-MTX with the same settings as in the randomized data experiment, and the original OctoMap, which updates occupancy via point cloud insertion. For OctoMap, we used the official open-source implementation available on GitHub [1]. 

Since the performance of POMP scales with thread count, we evaluated it on two machines: (i) an Intel Core i913900H system with 14 cores and 20 threads, and (ii) an Intel Core Ultra 9 285 (2.50 GHz) system with 24 cores and 24 threads. As shown in Tables V and VI, the reported time covers the entire pre-planning pipeline, including Octree construction and its projection onto an OGM. Compared with the direct OGM baseline, which loops over all points and directly updates the occupancy state of their corresponding 

cells, our method achieves lower runtime, supports real-time updates and online path planning, and, like OctoMap, yields a sparse representation of large scenes. 

_2) Planning Performance in Sparse Environments:_ In this experiment, we compared our method in terms of pathfinding success rate, path length, and A* and JPS planning time on two large-scale but relatively sparse point cloud scenes, Cambridge_15 and Cambridge_16, across varying resolutions. To ensure fairness, this experiment followed the same configuration as the randomized data experiments. 

As shown in Table VII, real-world results are consistent with the randomized data results. POMP shows a clear advantage in the success rate of pathfinding. Compared with the baseline direct OGM, it produces paths of comparable or shorter length, though with slightly longer planning time in some cases. 

_3) Planning Performance in Cluttered Environments:_ To study performance in clustered environments, we use the Cloud_7 (WSF-19, Treescope) dataset, shown in Fig. 15, and measure pathfinding rate, resulting path length, and A* and JPS planning time over a range of resolutions. 

As shown in Table VII, POMP shows a clear advantage in 

13 


![](1_survey/papers/md/Mao2026Parallel_figs/Mao2026Parallel.pdf-0013-01.png)


Fig. 15. Cloud_7 from WSF-19 in the Treescope dataset. The upper-left panel shows the raw point cloud map, the lower-left panel shows the octree constructed from the point cloud, and the right panel shows the planning result. The blue path is generated by POMP, while the purple path is obtained using the direct OGM. 

the success rate. Compared with the baseline direct OGM, it produces paths of comparable or shorter length, though with slightly longer planning time. Since POMP provides the planners with more free cells than the baseline, a slight increase in planning time is expected. 

## _C. Real-world experiments_ 

To evaluate the performance of POMP in a real-world setting using sensor data, we use the processed rosbags released with Treescope. Since the Treescope dataset is composed of sensor data recorded in an uncontrolled outdoor environment, it is a better evaluation tool than in-lab hardware experimentation. The bags include LiDAR-inertial odometry and velocity-corrected point cloud sweeps produced by FasterLIO [40]. The point clouds from the UAV Laser Scanning (ULS) sequences are captured with an Ouster OS1-64 LiDAR; specifically, we use two VAT-0723U rosbags: VAT-0723U-03, a 9.2 GiB bag spanning 380.4 seconds, and VAT-0723U-04, a 16.2 GiB bag spanning 654.4 seconds. Each LiDAR sweep contains approximately 65,536 points (64 × 1024). 

To better emulate on-robot operation, we replay each rosbag at real-time speed with timestamps governed by the same ROS time mechanism used at runtime and run the same on-robot processing stack. Each LiDAR sweep is processed as it arrives and matched to the closest odometry and pose transform within a small time tolerance, using a fixed synchronization timeout. When the processing rate briefly falls behind the sensor rate, we prevent unbounded latency growth by using bounded queues and retaining only the most recent sweeps; any sweep that cannot be time-synchronized is dropped. The synchronized frames are then forwarded directly to the mapping backend under the same timing and latency constraints as live operation. 

_1) Octree Construction:_ The per-sweep Octree construction time of POMP is evaluated against that of OctoMap-MTX and the original OctoMap across different leaf-node sizes (i.e., map resolutions). For original OctoMap, we used the official opensource implementation available on GitHub [1]. To align with the default setting in the OctoMap source code, we use the 

## TABLE VIII 

EXPERIMENT C-1: PER-SWEEP OCTREE CONSTRUCTION TIME (MS). 

||||VAT-0723U-03|VAT-0723U-03||
|---|---|---|---|---|---|
||Res.|(m)|POMP|OctoMap-MTX|OctoMap|
||0.2||**1.536**_±_**0.008**|5_._817_±_0_._096|6_._513_±_0_._098|
||0.5||**1.333**_±_**0.009**|4_._592_±_0_._062|3_._433_±_0_._051|
||1.0||**1.289**_±_**0.007**|4_._158_±_0_._048|2_._601_±_0_._043|
||1.5||**1.264**_±_**0.008**|3_._995_±_0_._031|2_._428_±_0_._030|
||2.0||**1.255**_±_**0.011**|3_._890_±_0_._053|2_._291_±_0_._046|
||2.5||**1.233**_±_**0.006**|3_._845_±_0_._024|2_._194_±_0_._050|
||||VAT-0723U-04|||
||Res.|(m)|POMP|OctoMap-MTX|OctoMap|
||0.2<br>0.5<br>1.0<br>1.5<br>2.0||**1.521**_±_**0.021**<br>**1.350**_±_**0.012**<br>**1.305**_±_**0.016**<br>**1.261**_±_**0.012**<br>**1.240**_±_**0.011**|6_._233_±_0_._075<br>4_._852_±_0_._048<br>4_._393_±_0_._040<br>4_._156_±_0_._045<br>3_._997_±_0_._056|6_._526_±_0_._078<br>3_._559_±_0_._064<br>2_._941_±_0_._063<br>2_._657_±_0_._059<br>2_._643_±_0_._040|
||2.5||**1.239**_±_**0.008**|3_._941_±_0_._028|2_._597_±_0_._056|



same 16-level tree with leaf resolution _r_ . This configuration yields a maximum spatial extent of _r ·_ 2[15] . Although our method can adapt the tree depth based on the estimated scene size, we keep the depth fixed here for a fair comparison. 

As shown in Table VIII, we replay each rosbag at its nominal rate and measure per-sweep construction time over the full playback. Each configuration is repeated 10 times, and we report the mean and standard deviation. Overall, POMP achieves lower runtime with reduced variability, and is typically 2-3xfaster than OctoMap and OctoMap-MTX, meeting the real-time requirements of a lightweight online mapping pipeline. 

_2) Occupancy Grid Construction from Octree:_ The time taken to construct occupancy grids from the POMP octree and the original OctoMap octree is compared. For each setting, we run the conversion 500 times on the constructed Octree. As the mean and standard deviation in Table IX indicate, POMP achieves lower average conversion time and lower variability. 

TABLE IX 

EXPERIMENT C-2: PER-SWEEP MAPPING TIME (MS). 

|VAT-0723U-03<br>VAT-0723U-04<br>Res. (m)<br>POMP<br>OctoMap<br>POMP<br>OctoMap<br>0.2<br>**11.803**_±_**0.448** 52_._364_±_1_._643 **13.245**_±_**0.426** 59_._363_±_1_._530<br>0.5<br>**2.735**_±_**0.229**<br>9_._136_±_0_._366<br>**2.929**_±_**0.284**<br>9_._569_±_0_._482<br>1.0<br>**0.429**_±_**0.071**<br>1_._573_±_0_._157<br>**0.465**_±_0_._288<br>1_._650_±_**0.191**<br>1.5<br>**0.192**_±_**0.069**<br>0_._468_±_0_._082<br>**0.189**_±_**0.076**<br>0_._475_±_0_._079<br>2.0<br>**0.127**_±_0_._066<br>0_._238_±_**0.059**<br>**0.136**_±_0_._062<br>0_._236_±_**0.058**<br>2.5<br>**0.098**_±_0_._050<br>0_._140_±_**0.037**<br>**0.102**_±_0_._058<br>0_._139_±_**0.040**|VAT-0723U-03<br>POMP<br>OctoMap|VAT-0723U-04<br>POMP<br>OctoMap|
|---|---|---|



_3) Navigability and Planning:_ We also repeat Experiments A-3 and A-4 for these data. Specifically, we compare (i) the navigability of the occupancy grids converted from the POMP Octree (Table XI) and (ii) the planning performance on these occupancy grids (Table X) against occupancy grids obtained from original OctoMap. Planning performance is evaluated using both A* and JPS, including pathfinding success rate, path length, and planning time. Since JPS is a pruned, accelerated 

14 


![](1_survey/papers/md/Mao2026Parallel_figs/Mao2026Parallel.pdf-0014-01.png)


Fig. 16. Visualization of the input point cloud VAT-0723U-03 and the resulting POMP Octree, from left to right with leaf sizes _r_ = 0 _._ 5m, 1 _._ 0m, and 2 _._ 0m. 

TABLE X 

EXPERIMENT C-3: PLANNING METRICS ACROSS RESOLUTIONS. 

|Res. (m)|||VAT-0723U-03|VAT-0723U-03|VAT-0723U-03|VAT-0723U-03|VAT-0723U-03|||VAT-0723U-04|VAT-0723U-04|VAT-0723U-04|VAT-0723U-04|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||Succ. (%) _↑_<br>POMP<br>OGM|||||||Succ. (%) _↑_<br>POMP<br>OGM||||||
|||||||||||||||
|0.2<br>**90.60**% 88_._80%<br>0.5<br>**69.00**% 65_._00%<br>1.0<br>**44.00**% 38_._40%<br>1.5<br>**27.80**% 24_._20%<br>2.0<br>**12.80**%<br>8_._60%<br>2.5<br>**3.40**%<br>1_._40%||52_._833 **52.200**<br>**1.100**<br>1_._405<br>**0.113**<br>0_._153<br>**0.050**<br>0_._067<br>0_._041<br>**0.029**<br>**0.016**<br>0_._019||43_._766 **42.787**<br>**0.571**<br>0_._585<br>0_._069<br>**0.068**<br>**0.033**<br>0_._034<br>0_._018<br>0_._018<br>0_._012<br>**0.009**||**15.466** 15_._469<br>**15.491** 15_._507<br>**14.303** 14_._389<br>**16.427** 16_._740<br>**16.950** 18_._161<br>**21.576** 23_._684|**88.20**% 86_._00%<br>**73.60**% 69_._60%<br>**42.80**% 37_._00%<br>**26.60**% 20_._20%<br>**11.40**%<br>7_._60%<br>**2.60**%<br>1_._80%||51_._005 **50.810**<br>**1.053**<br>1_._355<br>**0.124**<br>0_._161<br>**0.048**<br>0_._053<br>0_._037<br>**0.024**<br>**0.011**<br>0_._014||41_._391 41_._391<br>**0.579**<br>0_._591<br>**0.074**<br>0_._076<br>**0.032**<br>0_._033<br>0_._015<br>0_._015<br>0_._009<br>**0.007**||**15.015** 15_._019<br>**14.594** 14_._637<br>**15.207** 15_._262<br>**16.024** 16_._247<br>**13.689** 14_._182<br>**13.604** 13_._780|



_Note:_ Bold indicates the better value between POMP and OGM for each bag and resolution. Success rate denotes the pathfinding rate, and length denotes the path length. 

variant of A*, it returns the same shortest-path length as A* on the same grid (when using the same connectivity and edge costs). Therefore, A* and JPS have identical path lengths in our experiments, and we do not report them separately. 

TABLE XI 

EXPERIMENT C-4: PER-SWEEP NAVIGABLE SPACE RATIO (%). 

|Res. (m)|VAT-0723U-03<br>POMP<br>OGM|VAT-0723U-04<br>POMP<br>OGM|
|---|---|---|
|0.2<br>0.5<br>1.0<br>1.5<br>2.0<br>2.5|**94.17**%<br>93_._44%<br>**84.20**%<br>82_._08%<br>**66.38**%<br>62_._35%<br>**50.42**%<br>45_._18%<br>**35.01**%<br>27_._71%<br>**23.50**%<br>15_._25%|**94.11**%<br>93_._41%<br>**84.02**%<br>81_._92%<br>**65.23**%<br>61_._41%<br>**49.13**%<br>43_._40%<br>**32.94**%<br>26_._53%<br>**24.00**%<br>18_._25%|



As shown in Table XI, our maps preserve more navigable free space than the direct OGM method across resolutions; consequently, as reported in Table X, POMP achieves a higher pathfinding success rate. The improvement holds at fine resolutions (where finding a path is usually easier) and at coarse resolutions (where planning often fails). At the resolutions that best match the scene and the planner, the improvement becomes greater, which is consistent with what our method is designed to do. 

## VII. DISCUSSION 

In our mapping to planning pipeline, we re-partition a fixedresolution occupancy grid map using OctoMap leaf boundaries at depth _n_ , then apply occupancy thresholding with a conservative safety margin and assign each cell’s navigability via Diagonal Examination (Fig. 6). The key intuition is that uniform partitioning improves coverage, making gaps near the grid resolution less likely to be missed. Given the scene scale, we can further choose an appropriate OctoMap tree depth to ensure sufficient spatial coverage while controlling memory and computation. 

In implementation, map building is integrated into the planning pipeline, allowing mapping to be performed during planning. The Octree insertion and update operations, including the safety-state updates, are parallelized. The subsequent octree to OGM projection is also parallelized. With dense point clouds, POMP is typically faster than a naive pointwise serial loop that writes directly into an OGM, meeting the requirements of synchronous online operation. Compared with the serial Octree-to-OGM conversion in the original method, POMP’s octree to OGM conversion incurs little additional computational cost; the proposed region safety state update does not introduce excessive cost. In the serial baseline, each leaf node typically maps to a single OGM cell update; in POMP, each leaf node is split into four regions in 2D and eight in 3D, and navigability is written to the OGM via one-way diagonal pair updates (a diagonal pair of cells is updated together), requiring two pairs in 2D and four pairs 

15 

in 3D. This procedure can be further accelerated via parallel execution, while atomic operations prevent race conditions under concurrent updates. Moreover, given a desired OGM configuration (resolution, origin, and spatial bounds) based on the expected scene size, the corresponding octree placement (origin and extent) can be determined so that the octree is instantiated with the appropriate size, location, and depth to match the target OGM layout. 

We validate POMP through extensive benchmarks on diverse real-world datasets, including LiDAR and reconstruction maps spanning outdoor urban scenes, indoor rooms, and forested environments. Additional tests use randomized scene configurations with diverse geometric combinations. Experiments cover point clouds of varying scales and densities, from sparse to dense, and include realistic rosbag replays that emulate online operation. 

Evaluation considers a broad set of metrics. Across the above scenes, multiple point cloud sizes, and multiple resolutions, we measure OctoMap build time, octree to OGM projection time, and navigability differences relative to a standard OGM baseline. Planning performance is also reported across resolutions and scenarios, including pathfinding success rate, search time, and path length under multiple search-based planning methods, with an additional experiment evaluating the impact of the threshold on success rate. 

To verify consistency with the standard serial implementation, we examine the proposed POMP construction procedure from both analytical and empirical perspectives. In particular, we compare the resulting data structures and validate point cloud assignments at the node level to confirm equivalence. To demonstrate construction efficiency, we further benchmark against state-of-the-art tree based structure building methods, where our approach consistently achieves faster build time. 

## VIII. CONCLUSIONS 

This article presents a framework for fixed-resolution freespace refinement and efficient octree-based occupancy-grid mapping. By accelerating dense point-cloud insertion and occupancy-grid-map updates without altering the underlying data structure or introducing additional computational overhead, the framework provides an efficient basis for searchbased planning. The framework builds on three core techniques. 

First, octree construction is accelerated through parallel multithreaded computation. Because concurrent updates in a hierarchical tree are nontrivial, compare-and-swap with atomic pointers ensures safe node creation and updates, while atomic operations propagate leaf states and point-cloud updates to a planner-facing occupancy grid without race conditions. This combination achieves mapping time comparable to a pointwise OGM insertion baseline and outperforms that baseline as point clouds become denser. 

Second, discretization accuracy is improved without further subdividing the tree. Region-level safety states are stored in a compact byte-level representation, avoiding the memory overhead of deeper trees while inducing a cell-level safety margin. This region-level encoding refines free-space represen- 

tation at a fixed resolution and improves search-based planning efficiency. 

Third, a hybrid map couples mapping and planning. An Octree-backed representation is maintained alongside a planner-facing occupancy grid, enabling synchronous operation and achieving higher pathfinding success rates and comparable or shorter paths than conventional fixed-resolution OGM pipelines. 

In summary, POMP shows that significant gains in planning performance can be achieved not by globally refining map resolution, but by more effectively exploiting free space within each fixed-resolution cell. Through parallel octree construction, compact region-level encoding, and a planner-facing hybrid map, POMP brings coarse-resolution planning closer to fine-resolution performance while retaining the efficiency advantages of coarse maps. As a result, it provides a practical path toward faster, more memory-efficient, and more reliable planning in dense and cluttered environments, and can be readily integrated into existing search-based autonomy pipelines. 

## REFERENCES 

- [1] A. Hornung, K. M. Wurm, M. Bennewitz, C. Stachniss, and W. Burgard, “Octomap: An efficient probabilistic 3D mapping framework based on octrees,” _Auton. Robots_ , vol. 34, pp. 189–206, 2013. 

- [2] R. A. Newcombe, S. Izadi, O. Hilliges, D. Molyneaux, D. Kim, A. J. Davison, P. Kohi, J. Shotton, S. Hodges, and A. Fitzgibbon, “Kinectfusion: Real-time dense surface mapping and tracking,” in _Proc. IEEE Int. Symp. Mixed Augmented Reality_ , 2011, pp. 127–136. 

- [3] M. Keller, D. Lefloch, M. Lambers, S. Izadi, T. Weyrich, and A. Kolb, “Real-time 3D reconstruction in dynamic scenes using point-based fusion,” in _Proc. Int. Conf. 3D Vision (3DV)_ , 2013, pp. 1–8. 

- [4] M. Qureshi, T. E. Ogri, Z. I. Bell, and R. Kamalapurkar, “Scalar field mapping with adaptive high-intensity region avoidance,” in _Proc. IEEE Conf. Control Technol. Appl._ , Newcastle upon Tyne, UK, Aug. 2024, pp. 388–393. [Online]. Available: https: //ieeexplore.ieee.org/document/10666509 

- [5] S. Thrun, “Probabilistic robotics,” _Communications of the ACM_ , vol. 45, no. 3, pp. 52–57, 2002. 

- [6] E. W. Dijkstra, “A note on two problems in connexion with graphs,” in _Edsger Wybe Dijkstra: his life, work, and legacy_ , 2022, pp. 287–290. 

- [7] P. E. Hart, N. J. Nilsson, and B. Raphael, “A formal basis for the heuristic determination of minimum cost paths,” _IEEE Trans. Syst. Sci. Cybern._ , vol. 4, no. 2, pp. 100–107, 1968. 

- [8] A. Stentz, “Optimal and efficient path planning for partially-known environments,” in _Proc. IEEE Int. Conf. Robot. Autom._ , 1994, pp. 3310– 3317. 

- [9] D. Harabor and A. Grastien, “Online graph pruning for pathfinding on grid maps,” in _Proc. AAAI Conf. Artif. Intell._ , vol. 25, no. 1, 2011, pp. 1114–1119. 

- [10] J.-C. Latombe, _Robot Motion Planning_ . Boston, MA: Kluwer Academic Publishers, 1991. 

- [11] Z. Liu, P. van Oosterom, J. Balado, A. Swart, and B. Beers, “Data frame aware optimized octomap-based dynamic object detection and removal in mobile laser scanning data,” _Alexandria Engineering Journal_ , vol. 74, pp. 327–344, 2023. 

- [12] D. Duberg and P. Jensfelt, “UFOMap: An efficient probabilistic 3D mapping framework that embraces the unknown,” _IEEE Robot. Autom. Lett._ , vol. 5, no. 4, pp. 6411–6418, 2020. 

- [13] L. Sun, Z. Yan, A. Zaganidis, C. Zhao, and T. Duckett, “RecurrentOctoMap: Learning state-based map refinement for long-term semantic mapping with 3-d lidar data,” _IEEE Robot. Autom. Lett._ , vol. 3, pp. 3749–3756, 2018. 

- [14] P. Chen, M. Li, Z. Wan, Y.-S. Hsiao, M. Yu, V. J. Reddi, and Z. Liu, “OctoCache: Caching voxels for accelerating 3D occupancy mapping in autonomous systems,” in _Proc. ACM Int. Conf. Archit. Support Program. Lang. Oper. Syst._ ACM, 2025, pp. 704–718. [Online]. Available: https://doi.org/10.1145/3676641.3716263 

- [15] Y. Kwon, D. Kim, I. An, and S.-e. Yoon, “Super rays and culling region for real-time updates on grid-based occupancy maps,” _IEEE Trans. Robot._ , vol. 35, no. 2, pp. 482–497, 2019. 

16 

- [16] H. Min, K. M. Han, and Y. J. Kim, “OctoMap-RT: Fast probabilistic volumetric mapping using ray-tracing GPUs,” _IEEE Robot. Autom. Lett._ , vol. 8, no. 9, pp. 5696–5703, 2023. 

- [17] Y. Cai, F. Kong, Y. Ren, F. Zhu, J. Lin, and F. Zhang, “Occupancy grid mapping without ray-casting for high-resolution LiDAR sensors,” _IEEE Trans. Robot._ , vol. 40, pp. 172–192, 2024. 

- [18] H. Oleynikova, Z. Taylor, M. Fehr, R. Siegwart, and J. Nieto, “Voxblox: Incremental 3D euclidean signed distance fields for on-board mav planning,” in _Proc. IEEE/RSJ Int. Conf. Intell. Robots Syst. (IROS)_ , 2017, pp. 1366–1373. 

   - [39] D. Cheng, F. C. Ojeda, A. Prabhu, X. Liu, A. Zhu, P. C. Green, R. Ehsani, P. Chaudhari, and V. Kumar, “Treescope: An agricultural robotics dataset for lidar-based mapping of trees in forests and orchards,” arXiv:2310.02162, 2023. 

   - [40] C. Bai, T. Xiao, Y. Chen, H. Wang, F. Zhang, and X. Gao, “FasterLIO: Lightweight tightly coupled lidar-inertial odometry using parallel sparse incremental voxels,” _IEEE Robot. Autom. Lett._ , vol. 7, no. 2, pp. 4861–4868, 2022. 

- [19] L. Han, F. Gao, B. Zhou, and S. Shen, “FIESTA: Fast incremental euclidean distance fields for online motion planning of aerial robots,” in _Proc. IEEE/RSJ Int. Conf. Intell. Robots Syst._ , 2019, pp. 4423–4430. [Online]. Available: https://ieeexplore.ieee.org/document/8968199 

- [20] Y. Pan, Y. Kompis, L. Bartolomei, R. Mascaro, C. Stachniss, and M. Chli, “Voxfield: Non-projective signed distance fields for online planning and 3D reconstruction,” in _Proc. IEEE/RSJ Int. Conf. Intell. Robots Syst._ IEEE, 2022, pp. 5331–5338. [Online]. Available: https://ieeexplore.ieee.org/document/9981318 

- [21] B. Curless and M. Levoy, “A volumetric method for building complex models from range images,” in _Proc. ACM SIGGRAPH_ , 1996, pp. 303– 312. 

- [22] S. Liu, M. Watterson, K. Mohta, K. Sun, S. Bhattacharya, C. J. Taylor, and V. Kumar, “Planning dynamically feasible trajectories for quadrotors using safe flight corridors in 3-D complex environments,” _IEEE Robot. Autom. Lett._ , vol. 2, no. 3, pp. 1688–1695, 2017. 

- [23] X. Zhou, Z. Wang, H. Ye, C. Xu, and F. Gao, “Ego-planner: An ESDFfree gradient-based local planner for quadrotors,” _IEEE Robot. Autom. Lett._ , vol. 6, no. 2, pp. 478–485, 2020. 

- [24] S. Liu, Y. Mao, and C. A. Belta, “Safety-critical planning and control for dynamic obstacle avoidance using control barrier functions,” in _Proc. Am. Control Conf. (ACC)_ , Denver, CO, USA, 2025, pp. 348–354. 

- [25] M. Nießner, M. Zollh¨ofer, S. Izadi, and M. Stamminger, “Real-time 3D reconstruction at scale using voxel hashing,” _ACM Transactions on Graphics_ , vol. 32, no. 6, pp. 1–11, 2013. 

- [26] T. Jia, E.-Y. Yang, Y.-S. Hsiao, J. Cruz, D. Brooks, G.-Y. Wei, and V. J. Reddi, “OMU: A probabilistic 3D occupancy mapping accelerator for real-time OctoMap at the edge,” arXiv:2205.03325, 2022. 

- [27] P. R. Florence, J. Carter, J. Ware, and R. Tedrake, “NanoMap: Fast, uncertainty-aware proximity queries with lazy search over local 3D data,” in _Proc. IEEE Int. Conf. Robot. Autom._ IEEE, 2018, pp. 7631– 7638. 

- [28] H. Min, K. M. Han, and Y. J. Kim, “Accelerating probabilistic volumetric mapping using ray-tracing graphics hardware,” in _Proc. IEEE Int. Conf. Robot. Autom._ IEEE, 2021, pp. 5440–5445. 

- [29] S. Durvasula, R. Kiguru, S. Mathur, J. Xu, J. Lin, and N. Vijaykumar, “VoxelCache: Accelerating online mapping in robotics and 3D reconstruction tasks,” in _Proc. Int. Conf. Parallel Archit. Compilation Tech._ ACM, 2023, pp. 239–251. 

- [30] D. De Gregorio and L. Di Stefano, “SkiMap: An efficient mapping framework for robot navigation,” in _Proc. IEEE Int. Conf. Robot. Autom._ IEEE, 2017, pp. 2569–2576. 

- [31] J. Reinders, _Intel threading building blocks: outfitting C++ for multicore processor parallelism_ . O’Reilly Media, Inc., 2007. 

- [32] A. Elfes, “Using occupancy grids for mobile robot perception and navigation,” _Computer_ , vol. 22, no. 6, pp. 46–57, 1989. 

- [33] H. Moravec and A. Elfes, “High resolution maps from wide angle sonar,” in _Proc. IEEE Int. Conf. Robot. Autom._ , vol. 2, 1985, pp. 116–121. 

- [34] J. Zhu, H. Li, Z. Wang, S. Wang, and T. Zhang, “i-Octree: A fast, lightweight, and dynamic octree for proximity search,” in _Proc. IEEE Int. Conf. Robot. Autom._ , 2024, pp. 12 290–12 296. 

- [35] Y. Cai, W. Xu, and F. Zhang, “ikd-Tree: An incremental K-D tree for robotic applications,” arXiv:2102.10808, 2021. 

- [36] R. B. Rusu and S. Cousins, “3D is here: Point cloud library (PCL),” in _Proc. IEEE Int. Conf. Robot. Autom._ , 2011, pp. 1–4. 

- [37] Q. Hu, B. Yang, S. Khalid, W. Xiao, N. Trigoni, and A. Markham, “SensatUrban: Learning semantics from urban-scale photogrammetric point clouds,” _Int. J. Comput. Vis._ , vol. 130, no. 2, pp. 316–343, 2022. 

- [38] J. Straub, T. Whelan, L. Ma, Y. Chen, E. Wijmans, S. Green, J. J. Engel, R. Mur-Artal, C. Ren, S. Verma, A. Clarkson, M. Yan, B. Budge, Y. Yan, X. Pan, J. Yon, Y. Zou, K. Leon, N. Carter, J. Briales, T. Gillingham, E. Mueggler, L. Pesqueira, M. Savva, D. Batra, H. M. Strasdat, R. De Nardi, M. Goesele, S. Lovegrove, and R. Newcombe, “The Replica dataset: A digital replica of indoor spaces,” _arXiv preprint arXiv:1906.05797_ , 2019. 

