---
citation_key: Mao2026Parallel
arxiv_id: 2603.22508
arxiv_url: "https://arxiv.org/abs/2603.22508"
title: "Parallel OctoMapping: A Scalable Framework for Enhanced Path Planning in Autonomous Navigation"
authors_short: "Yihui Mao et al."
year: 2026
direction_tag: H_hierarchical_planning
source: mineru-vlm
converter: mineru-open-api
model: vlm
converted_at: 2026-06-25T08:07:20Z
origin: ai+web
reviewed: false
---

# Parallel OctoMapping: A Scalable Framework for Enhanced Path Planning in Autonomous Navigation

Yihui Mao, Tian Tan, Xuehui Shen, Warren E. Dixon, and Rushikesh Kamalapurkar

Abstract—Mapping is essential in robotics and autonomous systems because it provides the spatial foundation for path planning. Efficient mapping enables planning algorithms to generate reliable paths while ensuring safety and adapting in real time to complex environments. Fixed-resolution mapping methods often produce overly conservative obstacle representations, which can lead to suboptimal paths or planning failures in cluttered scenes. To address this issue, we introduce Parallel OctoMapping (POMP), an efficient OctoMap-based mapping technique that preserves more navigable free space and supports multi-threaded computation. To the best of our knowledge, POMP is the first method that refines the representation of free space at a fixed occupancy-grid resolution without changing the underlying grid structure, while preserving compatibility with existing searchbased planners. It can therefore be integrated into existing planning pipelines, yielding higher pathfinding success rates and shorter path lengths, especially in cluttered environments, while substantially improving computational efficiency. An interactive web-based demonstration illustrating the mapping and planning behavior of POMP is available on the project webpage.

Index Terms—OctoMap, occupancy mapping, autonomous navigation, path planning, search-based planning, parallel computing.

## I. INTRODUCTION

Understanding the environment is fundamental to autonomy in mobile robotics. A well-designed mapping method that enforces spatial consistency across observations, produces an accurate and memory-efficient representation of the environment, and supports fast, informative spatial queries is thus a critical component of modern autonomy systems. Therefore, good map representations improve the reliability of downstream planning and collision-avoidance modules, enabling safer, higher-quality trajectories and ultimately more robust autonomous navigation [1]–[5].

In online navigation, mapping accuracy alone is insufficient. The mapping module must also meet time and computation constraints, supporting fast construction and frequent updates without sacrificing fidelity (runtime efficiency), while keeping memory usage bounded through sparse representations (memory efficiency). During execution, the map should provide online querying capability, allowing the planner to obtain the spatial information it needs, so that mapping and planning can work together within a unified navigation pipeline (continuous usability). OctoMap is a widely adopted representation for 3D occupancy mapping because its sparse octree structure enables memory-efficient storage, multi-resolution queries, and incremental updates [1]. However, in large environments with dense point clouds and high update rates, a standard OctoMap pipeline can become compute-bound and may struggle to sustain real-time throughput.

Search-based methods are widely used for planning because they integrate naturally with grid and voxel maps and can provide completeness and optimality guarantees under standard assumptions [6]–[9]. The performance of search-based planning, however, is strongly influenced by map resolution and the choice of representation. With fixed resolution cells, typical occupancy grids may mark an entire cell as occupied when a relatively small portion of an obstacle falls within it. The conservative labeling rule can unnecessarily mark traversable space as non-traversable, resulting in broken connectivity in narrow passages, increased search effort, degraded path quality, and in some cases planning failures in cluttered scenes [10]. A straightforward remedy is to increase the grid resolution, but this substantially increases mapping computation and memory consumption, enlarges the search graph, and ultimately lengthens planning time. Motivated by these limitations, we seek map representations that better exploit within-cell free space to preserve narrow passages without globally refining the resolution, while remaining efficient for online planning.

To address the limitations of fixed-resolution mapping for path planning, we propose an efficient mapping technique based on OctoMap that accelerates map construction through multi-threaded parallel computation and maximizes the utilization of cell space at fixed resolution. While conventional methods conservatively label an entire cell as occupied whenever it contains even a small portion of an obstacle, Parallel OctoMapping (POMP) performs a finer-grained analysis of the internal clustered spatial distribution of the point cloud to safely reclaim significant navigable space that would otherwise be inaccessible under traditional methods. In summary, our contributions are as follows:

• A novel OctoMap-based mapping technique (POMP) is developed that improves grid/voxel space utilization in 2D and 3D by subdividing each fixed-resolution grid/cell into distinct sub-regions. By introducing clear, safe, and unsafe states based on the clustered spatial distribution of the point cloud, this method unlocks significant navigable space overlooked by conservative Occupancy Grid Map (OGM) methods.

• POMP performs parallel, multi-threaded computation, significantly reducing map construction time in large environments with dense point clouds and frequent updates.

• POMP improves pathfinding success rate and path quality of search-based path planning while reducing mapping time compared with conventional fixed-resolution occupancy grid methods.

## II. RELATED WORK

## A. Mapping Representations and Frameworks

Point clouds, commonly captured in robotic tasks like mapping and planning, often contain excessive points and sensor noise, making them less suitable for efficiently representing large-scale environments. One simple alternative is the grid/voxel map, which partitions space into uniform squares/cubes to represent the scene; however, many of these remain unexplored in each sensor measurement, leading to a substantial memory overhead.

Tree-based representations have been studied to overcome these issues. The OctoMap [1] is a well-established representation that uses an Octree, which divides 3D space into eight subspaces that have the same volume. OctoMaps compactly and probabilistically represent an environment with occupancy states, including unknown, occupied, or free.

In recent years, a variety of mapping frameworks [1], [11]–[17] have been proposed to improve map representation and computational efficiency. In addition, some of these frameworks [18]–[20] facilitate navigation by providing map representations that are more suitable for path planning. Truncated Signed Distance Fields (TSDFs) [2], [21], originally used in computer graphics, represent geometry implicitly by storing truncated signed distance to the observed surface. In practice, TSDF values are updated using distances projected along the sensor ray, and they are maintained only within a narrow truncation band around the surface. Voxblox [18] builds upon TSDF by incrementally constructing Euclidean Signed Distance Fields (ESDFs) from the TSDF map, allowing efficient queries of the Euclidean distance from each voxel to the nearest obstacle to support path planning. FIESTA [19] is another well-known fast incremental ESDF mapping framework for online motion planning of aerial robots. It computes the ESDF directly from an occupancy grid map and builds a growing global map, and has been reported to achieve higher accuracy and computational performance compared to Voxblox in its experiments.

## B. Planning on Structured Maps

Discrete volumetric occupancy maps are typically implemented using one of three commonly used structures: uniform voxels [22]–[24], Octrees (e.g., OctoMap [1]), and hashed voxel/block structures [18], [25].

Occupancy grid mapping, where uniform voxel cells discretize the space, is easy to implement and aligns well with data from LiDAR and RGB-D cameras; however, dense implementations allocate memory uniformly across the bounded map volume, which leads to rapidly increasing memory usage as the resolution becomes finer. Octree–based representations such as OctoMap provide hierarchical, memory–efficient storage and naturally support multi–resolution updates, but their pointer–based hierarchy incurs O(log n) access time and makes neighborhood queries across different depths cumbersome. Hashed voxel/block structures can achieve sparse access in expected near O(1) access time and scale well to large environments, but suffer from potential hash collisions and require careful memory management.

To combine the strengths of these approaches while avoiding their weaknesses, we use the octree solely as a parallel point cloud reader and storage backend, streaming its leaf states to a fixed-resolution occupancy grid in real time. Atomic updates propagate each leaf change to the corresponding grid cell without race conditions, so the planner operates on a grid array with per-voxel access time of $O ( 1 )$ and constantstride neighbor checks, without traversing the tree during planning, while the map remains sparsely represented in the tree. This decoupled design preserves the octree’s efficient incremental construction and provides the planner with a contiguous grid array for fixed-stride access, enabling fast search-based planning.

## III. PRELIMINARIES

## A. OctoMap and Occupancy Grid Mapping Overview

OctoMap [1] is a 3D occupancy mapping framework that uses an Octree-based data structure to efficiently store, update, and query volumetric information. An Octree is a hierarchical structure that recursively subdivides 3D space into cubic volumes, or voxels, starting from a root node and continuing until a predefined resolution is reached.

The occupancy grid map for pathfinding is generated from the Octree built in the mapping process. The OctoMap and the occupancy grid map are configured as follows.

Octree Configuration. The first step is to align the OctoMap with the workspace of interest. We set the root center $\scriptstyle \mathbf { c } _ { \mathrm { r o o t } }$ of the Octree to coincide with the geometric center $\mathbf { c } _ { \mathrm { m a p } }$ of the environment bounds along each coordinate axis. Let $L _ { x } , L _ { y } , L _ { z }$ denote the side lengths of the workspace along the x, y, and z axes. We then define $L _ { \mathrm { m a x } } =$ max $\{ L _ { x } , L _ { y } , L _ { z } \}$ as the maximum extent of the environment. The depth n of the Octree is determined by the smallest resolution $r \ ( \mathrm { i . e . }$ , the edge length of a leaf cube). Since each additional tree level subdivides a cube into 8 smaller ones, the minimum depth required to achieve a leaf size r is computed as

$$
n = \left\lceil \log_ {2} \left(\frac {L _ {\mathrm{max}}}{r}\right)\right\rceil .
$$

The depth guarantees that the root node has a side length $S _ { 0 } =$ $2 ^ { n _ { r } }$ which is large enough to cover the maximum workspace dimension $L _ { \mathrm { m a x } }$ in all directions. Intuitively, this step defines the “outer box” of the Octree and ensures that the leaf nodes match the desired map resolution.

Grid Configuration. $N _ { x } , \ N _ { y }$ , and $N _ { z }$ denote the numbers of leaf nodes along the $x , y ,$ and z axes after discretizing the half of the workspace with leaf size r:

$$
N _ {x} = \left\lceil \frac {L _ {x}}{2 r} \right\rceil , N _ {y} = \left\lceil \frac {L _ {y}}{2 r} \right\rceil , N _ {z} = \left\lceil \frac {L _ {z}}{2 r} \right\rceil ,
$$

where $L _ { x } , L _ { y } ,$ and $L _ { z }$ are the workspace extents along the $x ,$ $y ,$ and z axes, respectively.

The origin of the occupancy grid, $\mathbf { o } _ { \mathrm { g r i d } } .$ , is placed at the vertex with the smallest coordinates in all three dimensions:

$$
\mathbf {o} _ {\text {grid}} = \left[ \begin{array}{c} \mathbf {c} _ {\text {map} _ {x}} - N _ {x} r - \frac {r}{2} \\ \mathbf {c} _ {\text {map} _ {y}} - N _ {y} r - \frac {r}{2} \\ \mathbf {c} _ {\text {map} _ {z}} - N _ {z} r - \frac {r}{2} \end{array} \right].
$$

Finally, the grid dimensions are defined as:

$$
\dim_ {x} = 2 N _ {x} + 1, \quad \dim_ {y} = 2 N _ {y} + 1, \quad \dim_ {z} = 2 N _ {z} + 1,
$$

The grid configuration guarantees that the occupancy grid is symmetrically aligned with the octree root, spans the full environment, and extends by half a cell $\left( r / 2 \right)$ beyond the outermost octree leaf nodes.

## B. Parallelization of octree construction

A dense point cloud input can make OctoMap construction a computational bottleneck, given that the commonly used implementation is often used in a single-threaded or effectively sequential manner in practice. Sequential processing limits throughput and responsiveness in real time mapping tasks, especially when handling large-scale or high-frequency sensor data. In addition, the hierarchical nature of the octree makes fine-grained parallelization difficult, because both updates and queries require root-to-leaf traversal, and concurrent operations may contend for shared nodes, necessitating synchronization to avoid race conditions.

Existing efforts to accelerate OctoMap can be broadly divided into hardware-assisted and software-based approaches. Hardware solutions, such as OMU [26], improve performance but reduce portability across the heterogeneous computing platforms used in robotic systems. Other hardware-assisted methods, including NanoMap [27], OctoMap-RT [16], OctoMap build based on Super Rays [15] and GPU-accelerated OctoMap [28], mainly accelerate ray tracing, yet octree updates can still remain the dominant cost. Software approaches are more limited. VoxelCache [29] reduces voxel-access latency through on-chip caching of recently used voxel-block pointers, but it does not parallelize OctoMap tree construction. SkiMap [30] improves efficiency by replacing the octree with a Tree of SkipLists and is thus better regarded as an alternative mapping structure than a direct optimization of OctoMap. Among software methods that preserve the OctoMap octree, OctoCache [14] is the closest, although its gains mainly arise from caching and workflow-level concurrency rather than true parallel updates within a single Octree.

We parallelize OctoMap construction with Intel oneAPI Threading Building Blocks (oneTBB), a task-based C++ library whose work-stealing scheduler balances the irregular, fine-grained tasks in voxel updates [31]. Compared with GPU approaches [16], [28], CPU parallelism can avoid host–device transfer costs when data reside on the CPU and often better matches the branching and sparse access patterns of Octree updates. Among CPU options, both OpenMP and oneTBB support dynamic scheduling and task parallelism. We choose oneTBB for its composable task-graph API and work-stealing runtime, which can better accommodate many small, irregular tasks than a simple thread-pool design.

To ensure correctness during concurrent updates, we employ the compare-and-swap (CAS) instruction, an atomic primitive supported by most modern multiprocessor architectures. CAS atomically compares the value at a memory location with an expected value and, only if they match, updates it to a new value. During parallel octree construction, when multiple threads concurrently attempt to create the same child node, each thread allocates a candidate node and uses CAS to atomically update the corresponding child pointer from null to that node. If the CAS fails, the thread discards the candidate node and proceeds with the child that has already been created by another thread. Each successful CAS thus ensures that only one thread initializes a given child pointer, preventing duplicate node creation under contention. Compared with the mutex-based locking used in OctoMap, this CAS-based design enables fine-grained child-node creation, reducing lock contention, thread blocking, and context-switch overhead, thereby improving the parallel throughput and scalability of hierarchical octree updates.

![](Mao2026Parallel_figs/e3532451e4e3e47a8f2098075016a456e62b98d44f6326f848bd200a1ee935fb.jpg)  
Fig. 1. System overview of our proposed mapping framework

## IV. OVERVIEW

Fig. 1 provides an overview of the proposed POMP framework. The framework consists of two tightly coupled components: (i) an OctoMap backend for real-time map construction, and (ii) a planner-facing fixed-resolution occupancy grid map (OGM) to support efficient search-based planning. Specifically, the OctoMap is continuously updated online, and the leaf-level region states are projected onto the OGM to determine the navigability of each corresponding grid cell for planning.

Because the OctoMap and the OGM are tightly coupled, their spatial relationship is explicitly defined (see Section III-A). In particular, the OctoMap leaf-node size is set equal to the OGM cell size. The number of OGM cells is selected to be larger by one along each axis than the number of OctoMap leaf nodes, and it is shifted by a half-cell offset so that the two discretizations are staggered by half of the cell size. This arrangement yields a consistent, overlap-based correspondence between OctoMap leaf nodes and OGM cells, enabling reliable projection of leaf-level region states onto the grid for planning. Due to half-cell offset, the leaf-node boundaries at the chosen depth often pass through the centers of OGM cells, effectively slicing the original grid and introducing additional split lines; because these boundaries are uniformly spaced, any narrow passage of sufficient width (larger than the chosen OGM cell resolution) must be intersected by at least one boundary (pigeonhole principle) and therefore cannot be “skipped” by discretization. We then apply occupancy thresholding with a safety margin to preserve the required clearance even when an obstacle occupies only a small fraction of an OGM cell (See the Region block in Fig. 2 and the left panel of Fig. 3). POMP starts by acquiring a stream of point clouds, either directly from range sensors (e.g., LiDAR) or from an existing point cloud map. An OctoMap is then constructed with a predefined leaf resolution, where incoming measurements are integrated through leaf-node point storage and/or occupancy updates (see Section V-B). Based on the resulting leaf-level statistics, we assign each leaf-node region a navigability label (unsafe / safe / clear) based on occupancy thresholding, and use this label to evaluate the traversability of the corresponding OGM cell, as discussed in Sections V-C and V-D.

TABLE I TERMINOLOGY AND NOTATION.

<table><tr><td>Category</td><td>Term</td><td>Definition</td><td>Sym.</td></tr><tr><td rowspan="5">OctoMap</td><td>node</td><td>A hierarchical spatial unit in the Octree corresponding to a cubic region of space.</td><td>----</td></tr><tr><td>leaf size</td><td>The edge length of a leaf node.</td><td>r</td></tr><tr><td>threshold</td><td>A user-defined range to classify points as unsafe, safe or clear for navigation.</td><td>thr</td></tr><tr><td>occupied state</td><td>A state in which the OctoMap node contains point cloud.</td><td>■</td></tr><tr><td>unoccupied state</td><td>A state where no point cloud is marked in an OctoMap node.</td><td>■</td></tr><tr><td rowspan="4">Region</td><td>region</td><td>A leaf node equally separated into 4 regions in 2D and 8 regions in 3D.</td><td>——</td></tr><tr><td>unsafe state</td><td>A region state in a leaf node with points outside the range set by the threshold.</td><td>■</td></tr><tr><td>safe state</td><td>A region whose points remain within the threshold bound and are treated as axis-aligned traversable.</td><td>■</td></tr><tr><td>clear state</td><td>A region state in a leaf node without a point cloud.</td><td>■</td></tr><tr><td rowspan="3">Occupancy Grid Map</td><td>grid</td><td>A discrete unit of the 2D occupancy grid map.</td><td>----</td></tr><tr><td>voxel</td><td>A discrete unit of the 3D occupancy grid map.</td><td>----</td></tr><tr><td>resolution</td><td>The grid/voxel edge length, same as the leaf size in our method.</td><td>res</td></tr></table>

The developed method fundamentally overcomes a key limitation of existing mapping techniques. The conventional methods [32], [33] employ overconservative occupancy labeling, marking a grid cell as fully occupied regardless of whether it is densely filled or contains only a few sparse points. Our approach, described in Algorithm 1 and Algorithm 2, performs a targeted subdivision at the leaf node to unlock navigable free space in OGM for motion planning. This process retains a significant portion of the free space that would otherwise be deemed untraversable. The resulting OGM thus provides a substantially larger configuration space for path planners, directly enhancing both the probability of finding a valid path and the quality of the solution in complex environments.

## V. POMP DESIGN AND IMPLEMENTATION

In this section, we present the implementation of the data structures and algorithms. The terminology and notation used in this paper are summarized in Table I.

![](Mao2026Parallel_figs/2998c9d977265d2f713b4d2284d248b6bb48e604108c45a4a6a03d0e959e501d.jpg)  
Fig. 2. Parallel insertion of point clouds into the Octree with concurrent node construction. Each leaf node is subdivided into 4 regions in 2D or 8 regions in 3D. In the figure, “ ” represents occupied, “ ” represents unoccupied, and ” denotes the threshold bounding box. The bounding box is centered on a leaf node and used to determine the region state; by default, the edge length of the bounding box is set to half the leaf size. The regions are classified as clear “ ” (no points), safe “ ”, or unsafe “ ” (see Fig.3).

## A. Data Structure

In Data Structure 1, Lines 2 and 3 define common attributes of a standard Octree node: the node’s size and pointers to its child nodes. The atomic type is used to enable concurrent (thread-safe) modifications to the child pointers without requiring a mutex, allowing safe node creation and point insertion in parallel. Line 3 stores atomic child pointers, which enable concurrent child creation during parallel insertion. In 2D, each node has four children, whereas in 3D it has eight. In line 4, we optionally store point coordinates in each leaf node using a concurrent vector. A concurrent vector is a thread-safe data structure that allows multiple threads to insert or access elements simultaneously without explicit locking, thus preventing race conditions during tree construction. Line 5 defines safe\_state: an atomic bitmask records the occupancy and safety of regions within a leaf node (8 bits in 2D and 16 bits in 3D). Using an atomic type ensures thread-safe updates during concurrent point insertions.

Data Structure 2 includes the pointer to the top-level node of the Octree, serving as the root for accessing and traversing the entire tree in Line 2. The map in Line 4 is for pathfinding, which is formally introduced in Data Structure

```txt
Data Structure 2: Octree
1 Structure:
2 OctreeNode* root;
3 double leafsize;
4 OccupancyGridMap* map;
```

```c
Data Structure 1: OctreeNode
1 Structure:
2 double node_size;
3 array<atomic<OctreeNode*>,8> children;
4 concurrent_vector<PointType> points;
5 atomic<uint16_t> safe_state{0};
```

3. The leafsize is a given value that represents the leaf node size, and is the same as the resolution of the map in Data Structure 3.

Data Structure 3 is the OccupancyGridMap, where Line 3 references an array of unsigned char (1 byte) occupancy state for thread-safe parallel updates. It plays the same role as occupancy grid cells but is designed to minimize conservative full-occupancy labels, improving spatial efficiency. The resolution (Line 2) represents the size of each voxel in the map.

![](Mao2026Parallel_figs/7d2eab2bc624cc862365beac8742c67b21b33fa569189fb11be8c740444be1a3.jpg)  
Fig. 3. Illustration of the threshold setup and region classification: clear , safe, and unsafe. The left panel depicts the boundary of the area, where h denotes half the edge length of an OctoMap leaf node (equal to the map resolution r), and the threshold distance is thr = h · ratio, with ratio specified at initialization. Red points lie outside the thresholded boundary, while blue points lie inside; these points determine the region safe state label (unsafe / safe / clear).

The parallel Octree construction follows the standard octree insertion procedure, which is illustrated in Fig. 2, but inserts points concurrently using multiple threads (see Algorithm 1). We parallelize point insertion by distributing the input points across threads; each thread traverses the tree from the root to the corresponding leaf for every point it inserts. Using parallel threads to access the same node can lead to race conditions; therefore, whenever constructing a new child under a parent node, we first check whether the pointer is nullptr. An atomic compare-and-swap (CAS) is used to safely construct child nodes during parallel point insertion. A new node is constructed only if the child pointer remains nullptr at the time of the operation. A successful CAS atomically sets the corresponding child pointer to the newly allocated node, whereas failure indicates that another thread has already constructed the child, in which case the newly allocated node is discarded. This process is repeated recursively until reaching a leaf node, whose size corresponds to the predefined resolution.

```txt
Algorithm 1: Parallel Octree Build

Input: Points P
1 Function TreeBuild(P):
2    foreach p ∈ P in parallel do
3    ParallelInsertPoints(p, root)

Input: Points p, OctreeNode node
1 Function ParallelInsertPoints(p, node):
2    if node is leaf then
3    push p into node.points
4    set_safe_state(p, node)
5    return
6    else
7    idx ← node.get_child_idx(p)
8    childPtr ← node.children[idx]
9    child ← AtomicLoad(childPtr)
10    if child is nullptr then
11    newNode ← new OctreeNode
12    old ← nullptr
13    ok ← CAS(childPtr, old, newNode)
14    if ok then
15    child ← newNode
16    else
17    destroy(newNode)
18    child ← AtomicLoad(childPtr)
19    ParallelInsertPoints(p, child)

Input: Points p, OctreeNode node
1 Function set_safe_state(p, node):
2    c ← node.center;
3    h ← node.size * 0.5;
4    idx ← node.get_child_idx(p)
5    offset ← number_of_regions
6    mask ← 1u << (idx+offset)
7    if ||p - c||∞ ≥ h · ratio then
8    mask ← mask | 1u << (idx)
9    AtomicOr(node.safe_state, mask)
```

Each OctoMap leaf node is subdivided into four regions in 2D or eight regions in 3D. During the point insertion (see the set\_safe\_state function), each point is checked against the leaf node center c. A region is marked unsafe if it contains any point whose perpendicular distance to any axisaligned splitting line/plane (used to partition the leaf cube) exceeds the threshold $t h r = h \cdot r a t i o ,$ , where h is half of the leafcube edge length. Equivalently, max<sub>i</sub> $| p _ { i } - c _ { i } | \ge t h r .$ , where p<sub>i</sub> and $c _ { i }$ are the i-th coordinate components of the point p and the leaf center c, respectively, and the splitting planes pass through c.

![](Mao2026Parallel_figs/073c7a1fbb90810c2690d3f7c62d4b9fe9d63b193f5d21420bff2691be1f1fa7.jpg)  
Fig. 4. Illustration of the mapping configuration from Octree leaf nodes (left) to leaf regions and their projection onto the OGM (right). The occupancy grid is shown with a dash–dot outline, OctoMap nodes with a long-dashed outline, and region partitions with solid lines.

This threshold provides a margin so that points too close to the boundary are conservatively treated as obstacles. If all points in the region lie within this margin, the region is marked safe. If the region contains no points, it is marked clear. All settings are illustrated in Fig. 3. For compact storage, these states are encoded in a single safe\_state variable. In 2D, for each region i, bit i + 4 records whether the region is non-clear, i.e., whether it contains at least one point, and bit i records whether the region is unsafe. Thus, a region is clear if neither bit is set, safe if only the nonclear bit is set, and unsafe if both the non-clear bit and the unsafe bit are set. The 3D case uses the same encoding with eight regions, where bits 8–15 record non-clear states and bits 0–7 record unsafe states. Note that unsafe, safe, and clear are the three region states we use to evaluate safety for navigability. A region is non-clear if it has been visited by points, which includes both the unsafe and safe cases. This atomic encoding allows multiple threads to update the safe state of different regions in parallel without requiring locks. The state of each region determines the navigability of its corresponding occupancy grid/voxel.

## C. Mapping Implementation

The OctoMap and the OGM are tightly coupled: the OctoMap is continuously updated online, as described in Section V-B, and the OGM used for pathfinding is derived from the OctoMap. The region safe states in the leaf level, as shown in Fig. 3, are used to infer the navigability of the corresponding OGM cells, and the inferred navigability is then used to assign the occupancy of each cell. Fig. 4 illustrates the spatial correspondence between the OctoMap and the OGM over the entire map.

In Algorithm 2, the constructed OctoMap is traversed from the root to the leaves using the function traverse(node). At each leaf node, we call project\_onto\_OGM(node) to mark the occupancy of the corresponding OGM cell. This function applies diagonal examination (see Fig. 5) to determine the navigability of the OGM cell containing the region, as well as the navigability of the OGM cell containing its diagonal region, and accordingly assigns the occupancy of that cell using set\_cell\_Occupied(idx). Here, from\_idx and to\_idx follow the arrow direction illustrated in Fig. 5.

![](Mao2026Parallel_figs/f7c3aebf5aae7245ef70bd50d876622bbb751e9a85a613bc882bcbeb21c08d4e.jpg)  
Fig. 5. Illustration of the diagonal examination pairs and rules for determining grid navigability. is the unsafe region in the leaf node, is the safe region in the leaf node, and is the clear region in the leaf node. The arrow represents the direction of examination. The floating square with a black border indicates that the corresponding cell of OGM should be marked as occupied after the examination.

## D. Diagonal Examination

In a standard occupancy grid map, a free cell has up to 8 neighbors in 2D and up to 26 neighbors in 3D. Accordingly, motion primitives can be categorized into two types: axisaligned and diagonal moves.

Under our alignment configuration, the OGM is shifted by a half-cell offset so that the two discretizations are staggered by half of the cell size. Consequently, each OGM cell overlaps multiple OctoMap leaf regions: four in 2D and eight in 3D. A clear region contains no obstacles and is navigable in all directions; a safe region is assumed to be navigable only in axis-aligned directions; and an unsafe region is not navigable in any direction. We leverage this decomposition and let the regions jointly determine whether an OGM cell should be marked as occupied (see Fig. 6).

![](Mao2026Parallel_figs/931826a9a1edb94414bf0daf1519f63ade7971d83128e010a290346a38908663.jpg)

Fig. 6. Illustration of the OGM produced by our method. This panel shows the bottom-right corner of the map in Fig. 4. For clarity, the OGM cell boundaries are drawn with a black dash-dotted outline, and the leaf-node boundary is shown as a gold long-dashed box. The nine OGM cells are labeled 1–9, and nine representative points are shown, colored by whether they lie inside or outside the threshold bound. The occupancy of diagonal pairs of OGM cells is 2<sub>determined</sub> <sub>by</sub> <sub>using</sub> <sub>Fig.</sub> <sub>5.</sub> <sub>The</sub> <sub>arrows</sub> <sub>indicate</sub> <sub>the</sub> <sub>feasible</sub> <sub>navigations</sub> <sub>between</sub> <sub>grid</sub> <sub>cells,</sub> <sub>and</sub> <sub>the</sub> <sub>colors</sub> <sub>encode</sub> <sub>each</sub> <sub>cell’s</sub> <sub>feasible</sub> <sub>navigations.</sub> <sub>Colored</sub> crosses mark the point cloud blocked during the Diagonal Examination for the corresponding colored cells.  
```txt
Algorithm 2: Occupancy Grid Mapping

Input: OctreeNode node
1 Function project onto_OGM(node):
2    if region[from_idx] is clear then
3    if region[to_idx] is not clear then
4    set_cell_Occupied(to_idx)
5    else
6    if region[from_idx] is safe then
7    if region[to_idx] is not clear then
8    set_cell_Occupied(to_idx)
9    else
10    set_cell_Occupied(from_idx)
11    else
12    if region[to_idx] is unsafe then
13    set_cell_Occupied(to_idx)
14    set_cell_Occupied(from_idx)

Input: OctreeNode node
1 Function traverse(node):
2    if node is Leaf then
3    projectonto_OGM(node)
4    else
5    foreach child ∈ node in parallel do
6    traverse(child)
```

By design, any cell that does not contain an unsafe region is navigable in axis-aligned directions. Thus, we only need to design occupancy rules using diagonal navigability. For example, all cells except for cells 1 and 4 in Fig. 6 are axisaligned navigable. Cells 6, 7, and 9 are nevertheless marked as occupied due to diagonal navigability considerations.

Using the presence of points in leaf-node regions to directly determine diagonal navigability is overly conservative. For example, in Fig. 6, although all cells except 2 and 3 appear to be diagonally non-navigable due to the presence of the points marked in blue, cells 5 and 8 can be safely marked unoccupied, which preserves axis-aligned navigation through cells 2, 5, and 8, and diagonal navigation between cells 3 and 5.

Navigability of diagonal pairs of OGM cells is determined using the corresponding diagonal regions of the leaf node that overlaps them. In the 2D case, the four regions of a leaf node yield two diagonal pairs, labeled [1, 4], [2, 3] in Fig. 2. In the 3D case, the eight regions of a leaf node yield four diagonal pairs, labeled [1, 8], [2, 7], [3, 6], [4, 5] in Fig. 2. As shown in Fig. 5, the navigability of diagonal regions is orderindependent. Accordingly, in 2D only two diagonal pairs need to be examined, whereas in 3D only four diagonal examination directions are required.

## E. Navigability State Determination

The rules for determining navigability of diagonal pairs of OGM cells are shown in Table II. All cells in the OGM are initialized as unoccupied. Cells containing one or more unsafe regions are marked occupied. Cells containing only clear regions are marked unoccupied. Since safe regions are navigable in axis-aligned directions but not along diagonal directions, marking either the cell containing the safe region or its diagonally adjacent cell as occupied is sufficient to block diagonal navigation between the two cells (e.g., cells 1 and 5, cells 5 and 7, and cells 5 and 9 in Fig. 6).

Based on the above discussion, the rules for occupancy assignment can be summarized as follows (see Fig. 5):

TABLE II  
NAVIGABILITY STATE DETERMINATION TABLE BASED ON THE DIAGONAL EXAMINATION

<table><tr><td>Region pair</td><td colspan="2">Axis-dir. navigability</td><td colspan="2">Diag-dir. navigability</td><td>Marking in cell</td><td>Notes</td></tr><tr><td>[unsafe unsafe]</td><td>unsafe: ✗</td><td>unsafe: ✗</td><td>unsafe: ✗</td><td>unsafe: ✗</td><td>Marking both diagonal cells as occupied</td><td>Axis-aligned:  $\|p - c\|_{\infty} \ge h \cdot ratio \Rightarrow ✗$ Diagonal: both regions contain points ⇒ ✗</td></tr><tr><td>[safe safe]</td><td>safe: √</td><td>safe: √</td><td>safe: ✗</td><td>safe: ✗</td><td>Mark one as occupied to block diagonal access while preserving axis-aligned navigation in the other region</td><td>Axis-aligned:  $\|p - c\|_{\infty} < h \cdot ratio \Rightarrow √$ Diagonal: both regions contain points ⇒ ✗</td></tr><tr><td>[clear clear]</td><td>clear: √</td><td>clear: √</td><td>clear: √</td><td>clear: √</td><td>Keep unoccupied in both diagonal cells</td><td>Both regions do not contain points ⇒ √</td></tr><tr><td>[unsafe safe]</td><td>unsafe: ✗</td><td>safe: √</td><td>unsafe: ✗</td><td>safe: ✗</td><td>Mark the unsafe cell as occupied.Allow axis-aligned navigation in the safe region.</td><td>Axis-aligned:  $\|p - c\|_{\infty} \ge h \cdot ratio \Rightarrow ✗$  $\|p - c\|_{\infty} < h \cdot ratio \Rightarrow √$ Diagonal: both regions contain points ⇒ ✗</td></tr><tr><td>[unsafe clear]</td><td>unsafe: ✗</td><td>clear: √</td><td>unsafe: ✗</td><td>clear: √</td><td>Mark the unsafe cell as occupied.Allow axis-aligned and diagonal navigation in the clear region.</td><td>Axis-aligned:  $\|p - c\|_{\infty} \ge h \cdot ratio \Rightarrow ✗$ Diagonal: unsafe region is non-empty ⇒ ✗The clear region contains no points ⇒ √</td></tr><tr><td>[safe clear]</td><td>safe: √</td><td>clear: √</td><td>safe: ✗</td><td>clear: √</td><td>Mark the safe cell as occupied. Allow axis-aligned and diagonal navigation in the clear region.</td><td>Axis-aligned:  $\|p - c\|_{\infty} < h \cdot ratio \Rightarrow √$ Diagonal: safe region is non-empty ⇒ ✗The clear region contains no points ⇒ √</td></tr></table>

Note: <sup>✓</sup>/<sup>✗</sup> denote navigable/non-navigable in the indicated direction; color denotes the region state. Notes summarize the navigability criteria for each region pair, and the Marking in cell column describes the POMP cell-marking strategy for preserving navigability.

![](Mao2026Parallel_figs/4809bd82bc0832ed966ac82847313c739f2614e1dfae0e365d9eb6e5cef9ece8.jpg)  
Fig. 7. Top row (POMP): Using the obstacle setup in Fig. 4 and the mapping rule in Fig. 5, POMP assigns each region an unsafe/safe/clear label (top left), updates the corresponding occupancy grid cells and their valid navigations between cells (top middle), and produces the final occupancy map (top right). Compared to direct OGM, POMP preserves more valid navigations (blue). Bottom row (direct OGM): For the same point cloud map, a standard occupancy grid voxelizes space (bottom left), marks a cell as occupied if it contains any points and marks the valid navigations between cells (bottom middle), and yields the final occupancy map (bottom right).

1) Safety hierarchy: regions are prioritized in the order of their safety levels as clear, safe, and unsafe.

2) Mixed pair: when two diagonally paired regions have different safety levels, the cell containing the safer region is designated as unoccupied, while the cell containing the less safe region is occupied.

## 3) Equal pair:

• if both regions are unsafe, both cells are designated as occupied;

• if both regions are safe, designate either cell as

occupied and the other as unoccupied;

• if both regions are clear, then both cells are designated as unoccupied;

Note that each OGM cell overlaps multiple pairs of diagonal leaf-node regions (4 in 2D and 8 in 3D). If any of the diagonal pairs of leaf-node region results in an occupied designation, the cell is marked as occupied. Otherwise, it remains unoccupied (see Fig. 7). To prevent race conditions caused by cells participating in multiple examinations, we use atomic operations for both the region safe state update and the cell-level occupancy update. In addition, octree construction and projection onto the OGM are executed sequentially rather than asynchronously.

![](Mao2026Parallel_figs/a6e12cb357db41ca8e733652d9cee9ba06970f328dacbe2859d1f066a4714d40.jpg)  
Fig. 8. Paths planned using POMP (red) and direct (traditional) OGM (blue) superimposed on the point cloud (a) and on the occupancy grid (b). The orange box (enlarged on the right) highlights the region responsible for the shorter path. Differences between our POMP and direct OGM are highlighted in (c) by cell (1)-(5). These cells are classified as unoccupied by POMP but occupied by the direct OGM. In particular, keeping cells (2) and (3) free in our method explains the shorter path found, as it preserves a traversable narrow passage (see middle figure).

The comparison between POMP and direct OGM, using an identical point cloud, is shown in Fig. 7 and Fig. 8. In Fig. 7, the cells that contain points, but are marked by POMP as unoccupied, are highlighted in blue. These cells result in a feasible path connecting the start and the goal, whereas the direct OGM admits no such path. Fig. 8 shows another case where POMP produces a shorter (red) path by preserving more navigable space.

## VI. EXPERIMENTS

In this section, we present randomized experiments to illustrate specific characteristics of the POMP algorithm, followed by offline experiments on real-world datasets and ROS bag simulations to demonstrate POMP’s performance. Except for Experiment B-1(a), all experiments are implemented in ROS 2 and conducted on an Intel Core Ultra 9 285 (2.50 GHz) system with 24 cores and 24 threads.

In the following, five experiments on randomized datasets are presented to illustrate the performance of POMP for tree construction, OGM construction, navigability, and planning.

## A. Randomized Point Clouds

![](Mao2026Parallel_figs/6d84029fb125b2b1d2e2037c77abde893ce6f00e46607b5a4a926dc4d349181a.jpg)  
Fig. 9. Two maps utilized in the randomized point-cloud experiments.

1) Tree Construction: In this experiment, we focus exclusively on evaluation of the computational efficiency of the Octree construction module of POMP. POMP is compared against three state-of-the-art incremental tree construction methods: i-Octree, ikd-Tree, and PCL Octree, for spatial representation across different leaf sizes. For evaluation, datasets containing 500,000, 1,000,000, and 2,000,000 points are randomly generated within a $1 0 \mathrm { m } \times 1 0 \mathrm { m } \times 1 0 \mathrm { m }$ workspace, and tree construction was repeated 200 times for each dataset using varying leaf sizes (0.01 m, 0.02 m, 0.03 m, 0.04 m, 0.05 m, 0.06 m and 0.07 m).

![](Mao2026Parallel_figs/c517c025d828cada1117e26c797ccc1190616536910446cf9a55da32b9fba6bd.jpg)

Construction Time vs. Leaf Size (1M Points)  
![](Mao2026Parallel_figs/7f6e077aa7c9c33ea5dd0216bf9f7915207cc8f29749d37d371f1a9e0b74ceb1.jpg)

Construction Time vs. Leaf Size (2M Points)  
![](Mao2026Parallel_figs/7ee39f42f2b3fbeea3f193b82c91a048587a1f9963ec91714ed5c6f5b34f2ed5.jpg)  
Fig. 10. Experiment A-1: Runtime comparison with point clouds, showing from top to bottom: 500,000, 1,000,000, and 2,000,000 points.

As shown in Fig. 10, across three datasets, POMP is at least 2 × faster than i-Octree [34], 7–10 × faster than ikd-Tree [35], and about 9 × faster than PCL Octree [36], while maintaining similarly low standard deviations across resolutions. These results demonstrate that, from a data-structure perspective, POMP achieves consistently higher tree construction throughput than state-of-the-art tree construction techniques.

2) OctoMap Construction & Occupancy Mapping: The second experiment evaluates the total runtime of OctoMap construction and the subsequent projection of region safe states from leaf nodes onto OGM cell occupancy, and compares it with three baselines: a direct OGM method, a mutexprotected parallel OctoMap (OctoMap-MTX), and the original OctoMap. In direct OGM method, the environment is discretized into grid cells, and each point in the point cloud directly updates the occupancy state of its corresponding cell. The OctoMap-MTX is a mutex-protected shared octree for parallel octree construction. To establish a strong lock-based baseline, we go beyond a naive shared-octree design with per-node mutexes. OctoMap-MTX still inserts all points into a single shared tree, but first partitions large point clouds by upper-level octree buckets and schedules the resulting disjoint subtrees to different workers. This retains the synchronization overhead of a shared-tree implementation while avoiding excessive fine-grained lock contention during bulk insertion. The original OctoMap baseline directly uses the official OctoMap implementation [1], where each input point updates the occupancy state of its corresponding octree node.

This experiment utilizes static uniform random cylinder environments. Cylinders are randomly distributed within the workspace defined by $x ~ \in ~ [ - 1 0 , 1 0 ] , ~ y ~ \in ~ [ - 1 0 , 1 0 ]$ , and $z \in [ - 5 , 5 ]$ (meters). A total of 50 million, 5 million, and 500 thousand points are sampled, with the cylinder radius uniformly drawn from [0.8, 1.0] m. To ensure robustness, 500 independent trial maps are generated under this configuration.

The results are shown in Fig. 11. To highlight the efficiency of our method, we compare our method with direct OGM. Across varying resolutions, our method is approximately 4–6× faster than the direct OGM method for 50M points, 2–3× faster for 5M points, and slightly faster for 500K points. Notably, this runtime includes both OctoMap construction and the subsequent projection onto an OGM, but it still outperforms the direct method. These results indicate that POMP better supports real-time updates and continuous map availability, especially for dense point clouds, which is critical for online planning in large-scale, high-rate sensing scenarios.

3) Navigability: In the third experiment, we evaluate the navigability performance of POMP on randomized 3D worlds of size $5 0 \mathrm { m } \times 5 0 \mathrm { m } \times 5 0 \mathrm { m }$ uniformly populated with three geometric shapes, including spheres, right circular cones, and axis-aligned boxes. The metric used to assess navigability is navigable space ratio (NSR), defined as the ratio of navigable cells to total cells. To assess performance across spatial resolutions, we vary the resolution from 0.5 to 5.0 m in 0.5 m increments and generate 200 independent worlds for each resolution. Each world contains 100 spheres, 100 cones, and 100 boxes (300 obstacles in total), with their surfaces uniformly sampled into generated point clouds containing 600,000 points.

Mapping Performance (50M Points)  
![](Mao2026Parallel_figs/022518637b46c0bd70884717b7a3508e66e4d05c3c0af12755af1ac3c4a75166.jpg)

Mapping Performance (5M Points)  
![](Mao2026Parallel_figs/e131f1b57a567209e513503ce190713cd70b55e34f09c551726c909eb1eb7ae1.jpg)

Mapping Performance (500K Points)  
![](Mao2026Parallel_figs/9c3ea5f7aa25badf41cc7dc97a30b8b37b4084d486a56f63f864ce06801079fc.jpg)  
Fig. 11. Experiment A-2: Comparison of the total runtime of OctoMap construction and the subsequent projection of region safe states from leaf nodes onto OGM cell occupancy, against three baseline map representations (direct OGM, OctoMap-MTX and the original OctoMap). The y-axis is shown in log scale.

![](Mao2026Parallel_figs/fb37ed421e7df535911d454437692a2684377d0bed3635ad7251814e35183d0b.jpg)  
Fig. 12. Experiment A-3: Comparison of the navigable space ratio (NSR) across OGM cell resolutions.

As shown in Fig. 12, across varying resolutions POMP outperforms the direct occupancy grid construction, achieving up to about 10% higher NSR at coarse resolutions. These results demonstrate that, at a fixed occupancy grid resolution, POMP refines the free space representation by reducing overly conservative occupancy labeling, thereby enlarging the feasible planning space for search-based planners.

4) Planning Performance: The fourth experiment evaluates planning performance using the same randomized datasets as in the second experiment. The start and goal positions are fixed at $( - 9 , - 9 , - 2 )$ and (9, 9, 2), respectively. A total of

![](Mao2026Parallel_figs/b2aa7f72d08fd65e5ebeae9d81e32da5fd506d64f0cb41d42c24b8f9658a006c.jpg)

![](Mao2026Parallel_figs/d4d75b8114059b797094f9f199bc6c63b7337dc48b5de6efcc6e435b1544edbe.jpg)

![](Mao2026Parallel_figs/0c594730897b3839177ed7b32c5826fef55fee81a4017d008d9e9c8c7dfa99a5.jpg)

![](Mao2026Parallel_figs/5dafa9625d11d127adabdf354dd5665207f3cd0526dab871655b72d84e831bd7.jpg)  
Fig. 13. Experiment A-4: Planning runtime and path length are reported only when both approaches successfully found a path. Note that at a resolution of 2.0 m, across all 500 trial maps, no path was found in the direct OGM, but paths were still found in the POMP maps.

500 independent trial maps are generated, and we evaluate the runtime of planning with two search-based pathfinding algorithms, $\mathbf { A } ^ { * }$ and Jump Point Search (JPS). The evaluation metrics include planning runtime, pathfinding success rate, and path length, under both direct occupancy grid construction and POMP in varying resolutions. For a fair comparison, all cells outside the environment boundary are marked as occupied in all trials. When comparing path lengths, comparisons are made only when both approaches are able to find a path.

The results in Fig. 13 indicate that, for search-based planners $( \mathbf { A } ^ { * }$ and JPS), POMP incurs essentially no additional planning-time overhead compared with direct OGM. However, across varying map resolutions, POMP substantially improves the pathfinding success rate and consistently reduces the resulting path length.

5) Performance Comparison Across Threshold Ratio: The fifth experiment evaluates the effect of the threshold ratio on planning performance. In contrast to the fourth experiment, we consider a continuous-motion scenario with a single environment populated by uniformly random cubes. Cubes are initially distributed within the workspace $x \in [ - 2 5 , 2 5 ] , y \in [ - 2 5 , 2 5 ]$ and $z ~ \in ~ [ - 2 5 , 2 5 ]$ . A total of 800 cubes are placed in the workspace, resulting in a point cloud of approximately 70,000 points. The cube side lengths are uniformly distributed over [1.0, 2.0] m. Each cube independently selects a fixed random direction and then moves for 500 frames, translating 1 to 2 m per frame. When a cube contacts the workspace boundary, its motion follows a specular reflection rule, with the angle of incidence equal to the angle of reflection.

Threshold ratios of $r a t i o \in \{ 0 . 9 5 , 0 . 7 5 , 0 . 5 0 , 0 . 2 5 \}$ are evaluated and compared against a direct OGM baseline. For path planning, the start and the goal are fixed at $( - 2 0 , - 2 0 , - 2 0 )$ and (20, 20, 20), respectively.

As reported in Table III, decreasing the threshold ratio makes the safety margin more conservative, which reduces the effective navigable space and leads to a gradual decrease in planning success rate. However, for every evaluated resolution and ratio, POMP still outperforms the direct OGM baseline in pathfinding rate, demonstrating that the free-space refinement feature of POMP enlarges the feasible planning space while allowing the conservativeness to be tuned via ratio.

TABLE III  
EXPERIMENT A-5: PATHFINDING RATE ACROSS 500 FRAMES WITH VARYING THRESHOLD RATIO

<table><tr><td rowspan="2"></td><td colspan="7">Resolution (m)</td></tr><tr><td>1.0</td><td>1.5</td><td>2.0</td><td>2.5</td><td>3.0</td><td>3.5</td><td>4.0</td></tr><tr><td>POMP 0.95</td><td>82.2%</td><td>68.8%</td><td>58.8%</td><td>50.0%</td><td>38.4%</td><td>23.0%</td><td>15.4%</td></tr><tr><td>POMP 0.75</td><td>82.2%</td><td>67.4%</td><td>57.7%</td><td>46.4%</td><td>37.6%</td><td>21.8%</td><td>14.4%</td></tr><tr><td>POMP 0.50</td><td>81.4%</td><td>66.8%</td><td>56.3%</td><td>43.0%</td><td>35.0%</td><td>19.6%</td><td>13.0%</td></tr><tr><td>POMP 0.25</td><td>81.4%</td><td>66.4%</td><td>55.8%</td><td>42.4%</td><td>34.0%</td><td>19.0%</td><td>12.4%</td></tr><tr><td>OGM</td><td>81.4%</td><td>66.4%</td><td>55.6%</td><td>42.0%</td><td>32.2%</td><td>16.2%</td><td>9.6%</td></tr></table>

## B. Offline experiments on Real-world Datasets

![](Mao2026Parallel_figs/42fbc94b8858bef4fe064cf801c37b50eb5ccec5dab0d17ad3ab6d89893ba8b6.jpg)  
Fig. 14. Benchmark maps used in the application experiments include Cambridge 15, Cambridge 16, Cloud 7, Apartment 0, Apartment 1, and Apartment 2.

TABLE IV  
DETAILS OF MAPS IN DATASETS FOR BENCHMARK EXPERIMENT

<table><tr><td>Dataset</td><td>Map dimensions ( $m^{3}$ )</td><td>Point number</td></tr><tr><td>Cambridge_15</td><td> $400 \times 400 \times 60$ </td><td>119684095</td></tr><tr><td>Cambridge_16</td><td> $400 \times 400 \times 35$ </td><td>113159239</td></tr><tr><td>Cloud_7</td><td> $45 \times 104 \times 12$ </td><td>12915992</td></tr><tr><td>Apartment_0</td><td> $9.4 \times 14.8 \times 5.3$ </td><td>4564613</td></tr><tr><td>Apartment_1</td><td> $10.7 \times 7.9 \times 2.9$ </td><td>1909995</td></tr><tr><td>Apartment_2</td><td> $9.4 \times 10.2 \times 2.8$ </td><td>2136963</td></tr></table>

We evaluate POMP in real-world scenarios using three public datasets: SensatUrban [37], Replica [38] and Treescope [39]. SensatUrban is an urban-scale photogrammetric point cloud dataset with nearly three billion points from three UK cities; Replica provides high quality reconstructions of diverse indoor environments. Treescope is the first robotics dataset in precision agriculture and forestry designed specifically for counting and mapping trees in forest and orchard environments. The datasets Cambridge\_15 and Cambridge\_16 from SensatUrban, Apartment\_0, Apartment\_1, and Apartment\_2 from Replica, and Cloud\_7 from WSF-19 in Treescope are used for evaluation (See Fig. 14). Dataset details are provided in Table IV.

TABLE V  
EXPERIMENT B-1(A): CONSTRUCTION RUNTIME (MS) OF OCTOMAP, OCCUPANCY GRID MAP, AND OURS UNDER VARYING RESOLUTIONS ON FIVE MAPS (20-THREAD CPU)

<table><tr><td>Dataset</td><td colspan="3">Cambridge_15</td><td colspan="3">Cambridge_16</td><td colspan="3">Apartment_0</td><td colspan="3">Apartment_1</td><td colspan="3">Apartment_2</td></tr><tr><td>Resolution (m)</td><td>1.0</td><td>3.0</td><td>5.0</td><td>1.0</td><td>3.0</td><td>5.0</td><td>0.05</td><td>0.10</td><td>0.50</td><td>0.05</td><td>0.10</td><td>0.50</td><td>0.05</td><td>0.10</td><td>0.50</td></tr><tr><td>OctoMap</td><td>5089.00</td><td>4893.54</td><td>4878.26</td><td>4825.89</td><td>4626.40</td><td>4613.28</td><td>364.46</td><td>236.26</td><td>190.91</td><td>152.30</td><td>97.51</td><td>79.40</td><td>168.87</td><td>109.26</td><td>89.23</td></tr><tr><td>OctoMap-MTX</td><td>2695.07</td><td>2650.77</td><td>2511.81</td><td>2528.09</td><td>2446.34</td><td>2346.05</td><td>112.45</td><td>102.49</td><td>86.37</td><td>40.87</td><td>36.98</td><td>33.38</td><td>45.62</td><td>41.39</td><td>37.37</td></tr><tr><td>OGM</td><td>454.99</td><td>450.45</td><td>447.62</td><td>430.51</td><td>425.16</td><td>421.18</td><td>17.11</td><td>17.68</td><td>16.94</td><td>7.16</td><td>7.01</td><td>7.02</td><td>8.35</td><td>7.99</td><td>7.26</td></tr><tr><td>Ours</td><td>314.25</td><td>244.38</td><td>220.13</td><td>296.04</td><td>233.06</td><td>214.62</td><td>19.71</td><td>13.04</td><td>8.07</td><td>7.22</td><td>4.57</td><td>4.04</td><td>8.40</td><td>5.40</td><td>4.11</td></tr></table>

TABLE VI

EXPERIMENT B-1(B): CONSTRUCTION RUNTIME (MS) OF OCTOMAP, OCCUPANCY GRID MAP, AND OURS UNDER VARYING RESOLUTIONS ON FIVE MAPS (24-THREAD CPU)

<table><tr><td>Dataset</td><td colspan="3">Cambridge_15</td><td colspan="3">Cambridge_16</td><td colspan="3">Apartment_0</td><td colspan="3">Apartment_1</td><td colspan="3">Apartment_2</td></tr><tr><td>Resolution (m)</td><td>1.0</td><td>3.0</td><td>5.0</td><td>1.0</td><td>3.0</td><td>5.0</td><td>0.05</td><td>0.10</td><td>0.50</td><td>0.05</td><td>0.10</td><td>0.50</td><td>0.05</td><td>0.10</td><td>0.50</td></tr><tr><td>OctoMap</td><td>3336.56</td><td>3222.84</td><td>3209.94</td><td>3167.78</td><td>3047.52</td><td>3039.78</td><td>220.76</td><td>144.46</td><td>121.60</td><td>88.18</td><td>59.50</td><td>51.10</td><td>99.44</td><td>67.50</td><td>57.98</td></tr><tr><td>OctoMap-MTX</td><td>1873.78</td><td>1826.14</td><td>1721.92</td><td>1724.86</td><td>1677.24</td><td>1613.94</td><td>63.84</td><td>57.66</td><td>48.41</td><td>16.7</td><td>15.44</td><td>14.16</td><td>18.92</td><td>17.06</td><td>15.82</td></tr><tr><td>OGM</td><td>437.32</td><td>433.98</td><td>427.26</td><td>417.36</td><td>407.78</td><td>403.34</td><td>17.46</td><td>16.82</td><td>16.12</td><td>7.24</td><td>6.90</td><td>6.92</td><td>8.08</td><td>8.02</td><td>8.10</td></tr><tr><td>Ours</td><td>213.78</td><td>158.74</td><td>135.08</td><td>205.08</td><td>151.14</td><td>128.54</td><td>17.20</td><td>11.78</td><td>6.58</td><td>8.02</td><td>5.88</td><td>3.16</td><td>8.68</td><td>6.84</td><td>3.64</td></tr></table>

TABLE VII  
EXPERIMENT B-2 AND B-3: PATHFINDING METRICS ACROSS RESOLUTIONS.

<table><tr><td rowspan="2">Resolution (m)</td><td colspan="4">Cambridge_15</td><td colspan="4">Cambridge_16</td><td colspan="5">Cloud 7</td></tr><tr><td>2</td><td>6</td><td>10</td><td>14</td><td>2</td><td>6</td><td>10</td><td>14</td><td>0.5</td><td>1.0</td><td>1.5</td><td>2.0</td><td>2.5</td></tr><tr><td>OGM Pathfinding (%)</td><td>84.1</td><td>46.7</td><td>36.7</td><td>20.2</td><td>81.4</td><td>24.6</td><td>7.0</td><td>0.4</td><td>82.8</td><td>45.2</td><td>25.0</td><td>5.4</td><td>0.7</td></tr><tr><td>POMP Pathfinding (%)</td><td>91.5</td><td>68.8</td><td>50.2</td><td>45.1</td><td>82.7</td><td>29.6</td><td>7.5</td><td>6.3</td><td>92.1</td><td>68.4</td><td>44.9</td><td>33.6</td><td>16.4</td></tr><tr><td>OGM Path Length (m)</td><td>225.46</td><td>218.34</td><td>233.43</td><td>211.10</td><td>222.58</td><td>241.99</td><td>177.16</td><td>-</td><td>45.90</td><td>48.08</td><td>52.62</td><td>33.23</td><td>-</td></tr><tr><td>POMP Path Length (m)</td><td>225.42</td><td>218.30</td><td>233.40</td><td>210.90</td><td>222.42</td><td>237.70</td><td>176.64</td><td>-</td><td>45.84</td><td>47.70</td><td>50.94</td><td>31.22</td><td>-</td></tr><tr><td>A* on OGM (ms)</td><td>217.113</td><td>5.148</td><td>0.853</td><td>0.03</td><td>130.048</td><td>3.045</td><td>0.071</td><td>-</td><td>86.984</td><td>8.314</td><td>1.928</td><td>0.074</td><td>-</td></tr><tr><td>A* on POMP (ms)</td><td>215.331</td><td>5.497</td><td>0.995</td><td>0.084</td><td>122.764</td><td>2.72</td><td>0.029</td><td>-</td><td>91.589</td><td>10.246</td><td>2.692</td><td>0.167</td><td>-</td></tr><tr><td>JPS on OGM (ms)</td><td>114.408</td><td>1.518</td><td>0.204</td><td>0.001</td><td>67.955</td><td>1.289</td><td>0.014</td><td>-</td><td>43.827</td><td>4.454</td><td>1.104</td><td>0.019</td><td>-</td></tr><tr><td>JPS on POMP (ms)</td><td>123.703</td><td>1.715</td><td>0.188</td><td>0.001</td><td>67.514</td><td>1.13</td><td>0.001</td><td>-</td><td>48.234</td><td>5.239</td><td>1.524</td><td>0.074</td><td>-</td></tr></table>

Note: “-” indicates that insufficient common successful trials were available for the comparison of path length and pathfinding time.

1) Map Construction Performance: Map construction runtime of POMP is evaluated against three baselines: direct OGM and OctoMap-MTX with the same settings as in the randomized data experiment, and the original OctoMap, which updates occupancy via point cloud insertion. For OctoMap, we used the official open-source implementation available on GitHub [1].

Since the performance of POMP scales with thread count, we evaluated it on two machines: (i) an Intel Core i9- 13900H system with 14 cores and 20 threads, and (ii) an Intel Core Ultra 9 285 (2.50 GHz) system with 24 cores and 24 threads. As shown in Tables V and VI, the reported time covers the entire pre-planning pipeline, including Octree construction and its projection onto an OGM. Compared with the direct OGM baseline, which loops over all points and directly updates the occupancy state of their corresponding cells, our method achieves lower runtime, supports real-time updates and online path planning, and, like OctoMap, yields a sparse representation of large scenes.

2) Planning Performance in Sparse Environments: In this experiment, we compared our method in terms of pathfinding success rate, path length, and A\* and JPS planning time on two large-scale but relatively sparse point cloud scenes, Cambridge\_15 and Cambridge\_16, across varying resolutions. To ensure fairness, this experiment followed the same configuration as the randomized data experiments.

As shown in Table VII, real-world results are consistent with the randomized data results. POMP shows a clear advantage in the success rate of pathfinding. Compared with the baseline direct OGM, it produces paths of comparable or shorter length, though with slightly longer planning time in some cases.

3) Planning Performance in Cluttered Environments: To study performance in clustered environments, we use the Cloud\_7 (WSF-19, Treescope) dataset, shown in Fig. 15, and measure pathfinding rate, resulting path length, and A\* and JPS planning time over a range of resolutions.

As shown in Table VII, POMP shows a clear advantage in the success rate. Compared with the baseline direct OGM, it produces paths of comparable or shorter length, though with slightly longer planning time. Since POMP provides the planners with more free cells than the baseline, a slight increase in planning time is expected.

![](Mao2026Parallel_figs/343f09e7a8c5b6dbb79ffbb0475d7b7ce9d1b337f2ab0be6a34a30c91d12bc44.jpg)  
Fig. 15. Cloud\_7 from WSF-19 in the Treescope dataset. The upper-left panel shows the raw point cloud map, the lower-left panel shows the octree constructed from the point cloud, and the right panel shows the planning result. The blue path is generated by POMP, while the purple path is obtained using the direct OGM.

## C. Real-world experiments

To evaluate the performance of POMP in a real-world setting using sensor data, we use the processed rosbags released with Treescope. Since the Treescope dataset is composed of sensor data recorded in an uncontrolled outdoor environment, it is a better evaluation tool than in-lab hardware experimentation. The bags include LiDAR-inertial odometry and velocity-corrected point cloud sweeps produced by Faster-LIO [40]. The point clouds from the UAV Laser Scanning (ULS) sequences are captured with an Ouster OS1-64 LiDAR; specifically, we use two VAT-0723U rosbags: VAT-0723U-03, a 9.2 GiB bag spanning 380.4 seconds, and VAT-0723U-04, a 16.2 GiB bag spanning 654.4 seconds. Each LiDAR sweep contains approximately 65,536 points (64 × 1024).

To better emulate on-robot operation, we replay each rosbag at real-time speed with timestamps governed by the same ROS time mechanism used at runtime and run the same on-robot processing stack. Each LiDAR sweep is processed as it arrives and matched to the closest odometry and pose transform within a small time tolerance, using a fixed synchronization timeout. When the processing rate briefly falls behind the sensor rate, we prevent unbounded latency growth by using bounded queues and retaining only the most recent sweeps; any sweep that cannot be time-synchronized is dropped. The synchronized frames are then forwarded directly to the mapping backend under the same timing and latency constraints as live operation.

1) Octree Construction: The per-sweep Octree construction time of POMP is evaluated against that of OctoMap-MTX and the original OctoMap across different leaf-node sizes (i.e., map resolutions). For original OctoMap, we used the official opensource implementation available on GitHub [1]. To align with the default setting in the OctoMap source code, we use the same 16-level tree with leaf resolution r. This configuration yields a maximum spatial extent of $r \cdot 2 ^ { 1 5 }$ . Although our method can adapt the tree depth based on the estimated scene size, we keep the depth fixed here for a fair comparison.

TABLE VIII  
EXPERIMENT C-1: PER-SWEEP OCTREE CONSTRUCTION TIME (MS).  
VAT-0723U-03

<table><tr><td>Res. (m)</td><td>POMP</td><td>OctoMap-MTX</td><td>OctoMap</td></tr><tr><td>0.2</td><td>1.536±0.008</td><td>5.817±0.096</td><td>6.513±0.098</td></tr><tr><td>0.5</td><td>1.333±0.009</td><td>4.592±0.062</td><td>3.433±0.051</td></tr><tr><td>1.0</td><td>1.289±0.007</td><td>4.158±0.048</td><td>2.601±0.043</td></tr><tr><td>1.5</td><td>1.264±0.008</td><td>3.995±0.031</td><td>2.428±0.030</td></tr><tr><td>2.0</td><td>1.255±0.011</td><td>3.890±0.053</td><td>2.291±0.046</td></tr><tr><td>2.5</td><td>1.233±0.006</td><td>3.845±0.024</td><td>2.194±0.050</td></tr></table>

VAT-0723U-04

<table><tr><td>Res. (m)</td><td>POMP</td><td>OctoMap-MTX</td><td>OctoMap</td></tr><tr><td>0.2</td><td>1.521±0.021</td><td>6.233±0.075</td><td>6.526±0.078</td></tr><tr><td>0.5</td><td>1.350±0.012</td><td>4.852±0.048</td><td>3.559±0.064</td></tr><tr><td>1.0</td><td>1.305±0.016</td><td>4.393±0.040</td><td>2.941±0.063</td></tr><tr><td>1.5</td><td>1.261±0.012</td><td>4.156±0.045</td><td>2.657±0.059</td></tr><tr><td>2.0</td><td>1.240±0.011</td><td>3.997±0.056</td><td>2.643±0.040</td></tr><tr><td>2.5</td><td>1.239±0.008</td><td>3.941±0.028</td><td>2.597±0.056</td></tr></table>

As shown in Table VIII, we replay each rosbag at its nominal rate and measure per-sweep construction time over the full playback. Each configuration is repeated 10 times, and we report the mean and standard deviation. Overall, POMP achieves lower runtime with reduced variability, and is typically 2-3xfaster than OctoMap and OctoMap-MTX, meeting the real-time requirements of a lightweight online mapping pipeline.

2) Occupancy Grid Construction from Octree: The time taken to construct occupancy grids from the POMP octree and the original OctoMap octree is compared. For each setting, we run the conversion 500 times on the constructed Octree. As the mean and standard deviation in Table IX indicate, POMP achieves lower average conversion time and lower variability.

TABLE IX  
EXPERIMENT C-2: PER-SWEEP MAPPING TIME (MS).

<table><tr><td rowspan="2">Res. (m)</td><td colspan="2">VAT-0723U-03</td><td colspan="2">VAT-0723U-04</td></tr><tr><td>POMP</td><td>OctoMap</td><td>POMP</td><td>OctoMap</td></tr><tr><td>0.2</td><td>11.803±0.448</td><td>52.364±1.643</td><td>13.245±0.426</td><td>59.363±1.530</td></tr><tr><td>0.5</td><td>2.735±0.229</td><td>9.136±0.366</td><td>2.929±0.284</td><td>9.569±0.482</td></tr><tr><td>1.0</td><td>0.429±0.071</td><td>1.573±0.157</td><td>0.465±0.288</td><td>1.650±0.191</td></tr><tr><td>1.5</td><td>0.192±0.069</td><td>0.468±0.082</td><td>0.189±0.076</td><td>0.475±0.079</td></tr><tr><td>2.0</td><td>0.127±0.066</td><td>0.238±0.059</td><td>0.136±0.062</td><td>0.236±0.058</td></tr><tr><td>2.5</td><td>0.098±0.050</td><td>0.140±0.037</td><td>0.102±0.058</td><td>0.139±0.040</td></tr></table>

3) Navigability and Planning: We also repeat Experiments A-3 and A-4 for these data. Specifically, we compare (i) the navigability of the occupancy grids converted from the POMP Octree (Table XI) and (ii) the planning performance on these occupancy grids (Table X) against occupancy grids obtained from original OctoMap. Planning performance is evaluated using both $\mathbf { A } ^ { * }$ and JPS, including pathfinding success rate, path length, and planning time. Since JPS is a pruned, accelerated variant of $\mathbf { A } ^ { * } ,$ it returns the same shortest-path length as $\mathbf { A } ^ { * }$ on the same grid (when using the same connectivity and edge costs). Therefore, $\mathbf { A } ^ { * }$ and JPS have identical path lengths in our experiments, and we do not report them separately.

![](Mao2026Parallel_figs/ba4fc75986f0556c5593e0e1a2b5af0c4826382bc3520b4c1d3bdfe51ece1461.jpg)  
Fig. 16. Visualization of the input point cloud VAT-0723U-03 and the resulting POMP Octree, from left to right with leaf sizes $r = 0 . 5 \mathrm { m }$ , 1.0m, and 2.0m.

TABLE X  
EXPERIMENT C-3: PLANNING METRICS ACROSS RESOLUTIONS.

<table><tr><td rowspan="3">Res. (m)</td><td colspan="8">VAT-0723U-03</td><td colspan="8">VAT-0723U-04</td></tr><tr><td colspan="2">Succ. (%) ↑</td><td colspan="2">A* time (ms) ↓</td><td colspan="2">JPS time (ms) ↓</td><td colspan="2">Length (m) ↓</td><td colspan="2">Succ. (%) ↑</td><td colspan="2">A* time (ms) ↓</td><td colspan="2">JPS time (ms) ↓</td><td colspan="2">Length (m) ↓</td></tr><tr><td>POMP</td><td>OGM</td><td>POMP</td><td>OGM</td><td>POMP</td><td>OGM</td><td>POMP</td><td>OGM</td><td>POMP</td><td>OGM</td><td>POMP</td><td>OGM</td><td>POMP</td><td>OGM</td><td>POMP</td><td>OGM</td></tr><tr><td>0.2</td><td>90.60%</td><td>88.80%</td><td>52.833</td><td>52.200</td><td>43.766</td><td>42.787</td><td>15.466</td><td>15.469</td><td>88.20%</td><td>86.00%</td><td>51.005</td><td>50.810</td><td>41.391</td><td>41.391</td><td>15.015</td><td>15.019</td></tr><tr><td>0.5</td><td>69.00%</td><td>65.00%</td><td>1.100</td><td>1.405</td><td>0.571</td><td>0.585</td><td>15.491</td><td>15.507</td><td>73.60%</td><td>69.60%</td><td>1.053</td><td>1.355</td><td>0.579</td><td>0.591</td><td>14.594</td><td>14.637</td></tr><tr><td>1.0</td><td>44.00%</td><td>38.40%</td><td>0.113</td><td>0.153</td><td>0.069</td><td>0.068</td><td>14.303</td><td>14.389</td><td>42.80%</td><td>37.00%</td><td>0.124</td><td>0.161</td><td>0.074</td><td>0.076</td><td>15.207</td><td>15.262</td></tr><tr><td>1.5</td><td>27.80%</td><td>24.20%</td><td>0.050</td><td>0.067</td><td>0.033</td><td>0.034</td><td>16.427</td><td>16.740</td><td>26.60%</td><td>20.20%</td><td>0.048</td><td>0.053</td><td>0.032</td><td>0.033</td><td>16.024</td><td>16.247</td></tr><tr><td>2.0</td><td>12.80%</td><td>8.60%</td><td>0.041</td><td>0.029</td><td>0.018</td><td>0.018</td><td>16.950</td><td>18.161</td><td>11.40%</td><td>7.60%</td><td>0.037</td><td>0.024</td><td>0.015</td><td>0.015</td><td>13.689</td><td>14.182</td></tr><tr><td>2.5</td><td>3.40%</td><td>1.40%</td><td>0.016</td><td>0.019</td><td>0.012</td><td>0.009</td><td>21.576</td><td>23.684</td><td>2.60%</td><td>1.80%</td><td>0.011</td><td>0.014</td><td>0.009</td><td>0.007</td><td>13.604</td><td>13.780</td></tr></table>

Note: Bold indicates the better value between POMP and OGM for each bag and resolution. Success rate denotes the pathfinding rate, and length denotes the path length.

TABLE XI  
EXPERIMENT C-4: PER-SWEEP NAVIGABLE SPACE RATIO (%).

<table><tr><td rowspan="2">Res. (m)</td><td colspan="2">VAT-0723U-03</td><td colspan="2">VAT-0723U-04</td></tr><tr><td>POMP</td><td>OGM</td><td>POMP</td><td>OGM</td></tr><tr><td>0.2</td><td>94.17%</td><td>93.44%</td><td>94.11%</td><td>93.41%</td></tr><tr><td>0.5</td><td>84.20%</td><td>82.08%</td><td>84.02%</td><td>81.92%</td></tr><tr><td>1.0</td><td>66.38%</td><td>62.35%</td><td>65.23%</td><td>61.41%</td></tr><tr><td>1.5</td><td>50.42%</td><td>45.18%</td><td>49.13%</td><td>43.40%</td></tr><tr><td>2.0</td><td>35.01%</td><td>27.71%</td><td>32.94%</td><td>26.53%</td></tr><tr><td>2.5</td><td>23.50%</td><td>15.25%</td><td>24.00%</td><td>18.25%</td></tr></table>

As shown in Table XI, our maps preserve more navigable free space than the direct OGM method across resolutions; consequently, as reported in Table X, POMP achieves a higher pathfinding success rate. The improvement holds at fine resolutions (where finding a path is usually easier) and at coarse resolutions (where planning often fails). At the resolutions that best match the scene and the planner, the improvement becomes greater, which is consistent with what our method is designed to do.

## VII. DISCUSSION

In our mapping to planning pipeline, we re-partition a fixedresolution occupancy grid map using OctoMap leaf boundaries at depth $n ,$ then apply occupancy thresholding with a conservative safety margin and assign each cell’s navigability via Diagonal Examination (Fig. 6). The key intuition is that uniform partitioning improves coverage, making gaps near the grid resolution less likely to be missed. Given the scene scale, we can further choose an appropriate OctoMap tree depth to ensure sufficient spatial coverage while controlling memory and computation.

In implementation, map building is integrated into the planning pipeline, allowing mapping to be performed during planning. The Octree insertion and update operations, including the safety-state updates, are parallelized. The subsequent octree to OGM projection is also parallelized. With dense point clouds, POMP is typically faster than a naive pointwise serial loop that writes directly into an OGM, meeting the requirements of synchronous online operation. Compared with the serial Octree-to-OGM conversion in the original method, POMP’s octree to OGM conversion incurs little additional computational cost; the proposed region safety state update does not introduce excessive cost. In the serial baseline, each leaf node typically maps to a single OGM cell update; in POMP, each leaf node is split into four regions in 2D and eight in 3D, and navigability is written to the OGM via one-way diagonal pair updates (a diagonal pair of cells is updated together), requiring two pairs in 2D and four pairs in 3D. This procedure can be further accelerated via parallel execution, while atomic operations prevent race conditions under concurrent updates. Moreover, given a desired OGM configuration (resolution, origin, and spatial bounds) based on the expected scene size, the corresponding octree placement (origin and extent) can be determined so that the octree is instantiated with the appropriate size, location, and depth to match the target OGM layout.

We validate POMP through extensive benchmarks on diverse real-world datasets, including LiDAR and reconstruction maps spanning outdoor urban scenes, indoor rooms, and forested environments. Additional tests use randomized scene configurations with diverse geometric combinations. Experiments cover point clouds of varying scales and densities, from sparse to dense, and include realistic rosbag replays that emulate online operation.

Evaluation considers a broad set of metrics. Across the above scenes, multiple point cloud sizes, and multiple resolutions, we measure OctoMap build time, octree to OGM projection time, and navigability differences relative to a standard OGM baseline. Planning performance is also reported across resolutions and scenarios, including pathfinding success rate, search time, and path length under multiple search-based planning methods, with an additional experiment evaluating the impact of the threshold on success rate.

To verify consistency with the standard serial implementation, we examine the proposed POMP construction procedure from both analytical and empirical perspectives. In particular, we compare the resulting data structures and validate point cloud assignments at the node level to confirm equivalence. To demonstrate construction efficiency, we further benchmark against state-of-the-art tree based structure building methods, where our approach consistently achieves faster build time.

## VIII. CONCLUSIONS

This article presents a framework for fixed-resolution freespace refinement and efficient octree-based occupancy-grid mapping. By accelerating dense point-cloud insertion and occupancy-grid-map updates without altering the underlying data structure or introducing additional computational overhead, the framework provides an efficient basis for searchbased planning. The framework builds on three core techniques.

First, octree construction is accelerated through parallel multithreaded computation. Because concurrent updates in a hierarchical tree are nontrivial, compare-and-swap with atomic pointers ensures safe node creation and updates, while atomic operations propagate leaf states and point-cloud updates to a planner-facing occupancy grid without race conditions. This combination achieves mapping time comparable to a pointwise OGM insertion baseline and outperforms that baseline as point clouds become denser.

Second, discretization accuracy is improved without further subdividing the tree. Region-level safety states are stored in a compact byte-level representation, avoiding the memory overhead of deeper trees while inducing a cell-level safety margin. This region-level encoding refines free-space representation at a fixed resolution and improves search-based planning efficiency.

Third, a hybrid map couples mapping and planning. An Octree-backed representation is maintained alongside a planner-facing occupancy grid, enabling synchronous operation and achieving higher pathfinding success rates and comparable or shorter paths than conventional fixed-resolution OGM pipelines.

In summary, POMP shows that significant gains in planning performance can be achieved not by globally refining map resolution, but by more effectively exploiting free space within each fixed-resolution cell. Through parallel octree construction, compact region-level encoding, and a planner-facing hybrid map, POMP brings coarse-resolution planning closer to fine-resolution performance while retaining the efficiency advantages of coarse maps. As a result, it provides a practical path toward faster, more memory-efficient, and more reliable planning in dense and cluttered environments, and can be readily integrated into existing search-based autonomy pipelines.

## REFERENCES

[1] A. Hornung, K. M. Wurm, M. Bennewitz, C. Stachniss, and W. Burgard, “Octomap: An efficient probabilistic 3D mapping framework based on octrees,” Auton. Robots, vol. 34, pp. 189–206, 2013.

[2] R. A. Newcombe, S. Izadi, O. Hilliges, D. Molyneaux, D. Kim, A. J. Davison, P. Kohi, J. Shotton, S. Hodges, and A. Fitzgibbon, “Kinectfusion: Real-time dense surface mapping and tracking,” in Proc. IEEE Int. Symp. Mixed Augmented Reality, 2011, pp. 127–136.

[3] M. Keller, D. Lefloch, M. Lambers, S. Izadi, T. Weyrich, and A. Kolb, “Real-time 3D reconstruction in dynamic scenes using point-based fusion,” in Proc. Int. Conf. 3D Vision (3DV), 2013, pp. 1–8.

[4] M. Qureshi, T. E. Ogri, Z. I. Bell, and R. Kamalapurkar, “Scalar field mapping with adaptive high-intensity region avoidance,” in Proc. IEEE Conf. Control Technol. Appl., Newcastle upon Tyne, UK, Aug. 2024, pp. 388–393. [Online]. Available: https: //ieeexplore.ieee.org/document/10666509

[5] S. Thrun, “Probabilistic robotics,” Communications of the ACM, vol. 45, no. 3, pp. 52–57, 2002.

[6] E. W. Dijkstra, “A note on two problems in connexion with graphs,” in Edsger Wybe Dijkstra: his life, work, and legacy, 2022, pp. 287–290.

[7] P. E. Hart, N. J. Nilsson, and B. Raphael, “A formal basis for the heuristic determination of minimum cost paths,” IEEE Trans. Syst. Sci. Cybern., vol. 4, no. 2, pp. 100–107, 1968.

[8] A. Stentz, “Optimal and efficient path planning for partially-known environments,” in Proc. IEEE Int. Conf. Robot. Autom., 1994, pp. 3310– 3317.

[9] D. Harabor and A. Grastien, “Online graph pruning for pathfinding on grid maps,” in Proc. AAAI Conf. Artif. Intell., vol. 25, no. 1, 2011, pp. 1114–1119.

[10] J.-C. Latombe, Robot Motion Planning. Boston, MA: Kluwer Academic Publishers, 1991.

[11] Z. Liu, P. van Oosterom, J. Balado, A. Swart, and B. Beers, “Data frame aware optimized octomap-based dynamic object detection and removal in mobile laser scanning data,” Alexandria Engineering Journal, vol. 74, pp. 327–344, 2023.

[12] D. Duberg and P. Jensfelt, “UFOMap: An efficient probabilistic 3D mapping framework that embraces the unknown,” IEEE Robot. Autom. Lett., vol. 5, no. 4, pp. 6411–6418, 2020.

[13] L. Sun, Z. Yan, A. Zaganidis, C. Zhao, and T. Duckett, “Recurrent-OctoMap: Learning state-based map refinement for long-term semantic mapping with 3-d lidar data,” IEEE Robot. Autom. Lett., vol. 3, pp. 3749–3756, 2018.

[14] P. Chen, M. Li, Z. Wan, Y.-S. Hsiao, M. Yu, V. J. Reddi, and Z. Liu, “OctoCache: Caching voxels for accelerating 3D occupancy mapping in autonomous systems,” in Proc. ACM Int. Conf. Archit. Support Program. Lang. Oper. Syst. ACM, 2025, pp. 704–718. [Online]. Available: https://doi.org/10.1145/3676641.3716263

[15] Y. Kwon, D. Kim, I. An, and S.-e. Yoon, “Super rays and culling region for real-time updates on grid-based occupancy maps,” IEEE Trans. Robot., vol. 35, no. 2, pp. 482–497, 2019.

[16] H. Min, K. M. Han, and Y. J. Kim, “OctoMap-RT: Fast probabilistic volumetric mapping using ray-tracing GPUs,” IEEE Robot. Autom. Lett., vol. 8, no. 9, pp. 5696–5703, 2023.

[17] Y. Cai, F. Kong, Y. Ren, F. Zhu, J. Lin, and F. Zhang, “Occupancy grid mapping without ray-casting for high-resolution LiDAR sensors,” IEEE Trans. Robot., vol. 40, pp. 172–192, 2024.

[39] D. Cheng, F. C. Ojeda, A. Prabhu, X. Liu, A. Zhu, P. C. Green, R. Ehsani, P. Chaudhari, and V. Kumar, “Treescope: An agricultural robotics dataset for lidar-based mapping of trees in forests and orchards,” arXiv:2310.02162, 2023.

[18] H. Oleynikova, Z. Taylor, M. Fehr, R. Siegwart, and J. Nieto, “Voxblox: Incremental 3D euclidean signed distance fields for on-board mav planning,” in Proc. IEEE/RSJ Int. Conf. Intell. Robots Syst. (IROS), 2017, pp. 1366–1373.

[40] C. Bai, T. Xiao, Y. Chen, H. Wang, F. Zhang, and X. Gao, “Faster-LIO: Lightweight tightly coupled lidar-inertial odometry using parallel sparse incremental voxels,” IEEE Robot. Autom. Lett., vol. 7, no. 2, pp. 4861–4868, 2022.

[19] L. Han, F. Gao, B. Zhou, and S. Shen, “FIESTA: Fast incremental euclidean distance fields for online motion planning of aerial robots,” in Proc. IEEE/RSJ Int. Conf. Intell. Robots Syst., 2019, pp. 4423–4430. [Online]. Available: https://ieeexplore.ieee.org/document/8968199

[20] Y. Pan, Y. Kompis, L. Bartolomei, R. Mascaro, C. Stachniss, and M. Chli, “Voxfield: Non-projective signed distance fields for online planning and 3D reconstruction,” in Proc. IEEE/RSJ Int. Conf. Intell. Robots Syst. IEEE, 2022, pp. 5331–5338. [Online]. Available: https://ieeexplore.ieee.org/document/9981318

[21] B. Curless and M. Levoy, “A volumetric method for building complex models from range images,” in Proc. ACM SIGGRAPH, 1996, pp. 303– 312.

[22] S. Liu, M. Watterson, K. Mohta, K. Sun, S. Bhattacharya, C. J. Taylor, and V. Kumar, “Planning dynamically feasible trajectories for quadrotors using safe flight corridors in 3-D complex environments,” IEEE Robot. Autom. Lett., vol. 2, no. 3, pp. 1688–1695, 2017.

[23] X. Zhou, Z. Wang, H. Ye, C. Xu, and F. Gao, “Ego-planner: An ESDFfree gradient-based local planner for quadrotors,” IEEE Robot. Autom. Lett., vol. 6, no. 2, pp. 478–485, 2020.

[24] S. Liu, Y. Mao, and C. A. Belta, “Safety-critical planning and control for dynamic obstacle avoidance using control barrier functions,” in Proc. Am. Control Conf. (ACC), Denver, CO, USA, 2025, pp. 348–354.

[25] M. Nießner, M. Zollhofer, S. Izadi, and M. Stamminger, “Real-time¨ 3D reconstruction at scale using voxel hashing,” ACM Transactions on Graphics, vol. 32, no. 6, pp. 1–11, 2013.

[26] T. Jia, E.-Y. Yang, Y.-S. Hsiao, J. Cruz, D. Brooks, G.-Y. Wei, and V. J. Reddi, “OMU: A probabilistic 3D occupancy mapping accelerator for real-time OctoMap at the edge,” arXiv:2205.03325, 2022.

[27] P. R. Florence, J. Carter, J. Ware, and R. Tedrake, “NanoMap: Fast, uncertainty-aware proximity queries with lazy search over local 3D data,” in Proc. IEEE Int. Conf. Robot. Autom. IEEE, 2018, pp. 7631– 7638.

[28] H. Min, K. M. Han, and Y. J. Kim, “Accelerating probabilistic volumetric mapping using ray-tracing graphics hardware,” in Proc. IEEE Int. Conf. Robot. Autom. IEEE, 2021, pp. 5440–5445.

[29] S. Durvasula, R. Kiguru, S. Mathur, J. Xu, J. Lin, and N. Vijaykumar, “VoxelCache: Accelerating online mapping in robotics and 3D reconstruction tasks,” in Proc. Int. Conf. Parallel Archit. Compilation Tech. ACM, 2023, pp. 239–251.

[30] D. De Gregorio and L. Di Stefano, “SkiMap: An efficient mapping framework for robot navigation,” in Proc. IEEE Int. Conf. Robot. Autom. IEEE, 2017, pp. 2569–2576.

[31] J. Reinders, Intel threading building blocks: outfitting C++ for multicore processor parallelism. O’Reilly Media, Inc., 2007.

[32] A. Elfes, “Using occupancy grids for mobile robot perception and navigation,” Computer, vol. 22, no. 6, pp. 46–57, 1989.

[33] H. Moravec and A. Elfes, “High resolution maps from wide angle sonar,” in Proc. IEEE Int. Conf. Robot. Autom., vol. 2, 1985, pp. 116–121.

[34] J. Zhu, H. Li, Z. Wang, S. Wang, and T. Zhang, “i-Octree: A fast, lightweight, and dynamic octree for proximity search,” in Proc. IEEE Int. Conf. Robot. Autom., 2024, pp. 12 290–12 296.

[35] Y. Cai, W. Xu, and F. Zhang, “ikd-Tree: An incremental K-D tree for robotic applications,” arXiv:2102.10808, 2021.

[36] R. B. Rusu and S. Cousins, “3D is here: Point cloud library (PCL),” in Proc. IEEE Int. Conf. Robot. Autom., 2011, pp. 1–4.

[37] Q. Hu, B. Yang, S. Khalid, W. Xiao, N. Trigoni, and A. Markham, “SensatUrban: Learning semantics from urban-scale photogrammetric point clouds,” Int. J. Comput. Vis., vol. 130, no. 2, pp. 316–343, 2022.

[38] J. Straub, T. Whelan, L. Ma, Y. Chen, E. Wijmans, S. Green, J. J. Engel, R. Mur-Artal, C. Ren, S. Verma, A. Clarkson, M. Yan, B. Budge, Y. Yan, X. Pan, J. Yon, Y. Zou, K. Leon, N. Carter, J. Briales, T. Gillingham, E. Mueggler, L. Pesqueira, M. Savva, D. Batra, H. M. Strasdat, R. De Nardi, M. Goesele, S. Lovegrove, and R. Newcombe, “The Replica dataset: A digital replica of indoor spaces,” arXiv preprint arXiv:1906.05797, 2019.