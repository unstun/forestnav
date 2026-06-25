---
citation_key: Daniel2014Theta
arxiv_id: 1401.3843
arxiv_url: "https://arxiv.org/abs/1401.3843"
title: "Theta*: Any-Angle Path Planning on Grids"
authors_short: "Kenny Daniel et al."
year: 2014
direction_tag: M_multi_objective_planning
source: mineru-vlm
converter: mineru-open-api
model: vlm
converted_at: 2026-06-25T09:58:32Z
origin: ai+web
reviewed: false
---

# Theta\*: Any-Angle Path Planning on Grids

Kenny Daniel KFDANIEL@USC.EDU Alex Nash ANASH@USC.EDU Sven Koenig SKOENIG@USC.EDU Computer Science Department University of Southern California Los Angeles, California 90089-0781, USA

Ariel Felner Department of Information Systems Engineering Ben-Gurion University of the Negev Beer-Sheva, 85104, Israel

FELNER@BGU.AC.IL

## Abstract

Grids with blocked and unblocked cells are often used to represent terrain in robotics and video games. However, paths formed by grid edges can be longer than true shortest paths in the terrain since their headings are artificially constrained. We present two new correct and complete anyangle path-planning algorithms that avoid this shortcoming. Basic Theta\* and Angle-Propagation Theta\* are both variants of A\* that propagate information along grid edges without constraining paths to grid edges. Basic Theta\* is simple to understand and implement, fast and finds short paths. However, it is not guaranteed to find true shortest paths. Angle-Propagation Theta\* achieves a better worst-case complexity per vertex expansion than Basic Theta\* by propagating angle ranges when it expands vertices, but is more complex, not as fast and finds slightly longer paths. We refer to Basic Theta\* and Angle-Propagation Theta\* collectively as Theta\*. Theta\* has unique properties, which we analyze in detail. We show experimentally that it finds shorter paths than both A\* with post-smoothed paths and Field D\* (the only other version of A\* we know of that propagates information along grid edges without constraining paths to grid edges) with a runtime comparable to that of $\mathbf { A } ^ { * }$ on grids. Finally, we extend Theta\* to grids that contain unblocked cells with non-uniform traversal costs and introduce variants of Theta\* which provide different tradeoffs between path length and runtime.

## 1. Introduction

In this article, we study path planning for robotics and video games (Choset, Lynch, Hutchinson, Kantor, Burgard, Kavraki, & Thrun, 2005; Deloura, 2000; Patel, 2000; Murphy, 2000; Rabin, 2002), where a two-dimensional continuous terrain is discretized into a grid with blocked and unblocked cells. Our objective is to find a short unblocked path from a given start vertex to a given goal vertex (both at the corners of cells). A\* finds grid paths (that is, paths constrained to grid edges) quickly, but grid paths are often not true shortest paths (that is, shortest paths in the terrain) since their potential headings are artificially constrained to multiples of 45 degrees, as shown in Figure 1(a) (Yap, 2002). This shortcoming led to the introduction of what we call any-angle path planning (Nash, Daniel, Koenig, & Felner, 2007; Ferguson & Stentz, 2006). Any-angle path-planning algorithms find paths without constraining the headings of the paths, as shown in Figure 1(b). We present two new correct and complete any-angle path-planning algorithms. Basic Theta\* and Angle-Propagation Theta\* are both variants of $\mathbf { A } ^ { * }$ that propagate information along grid edges (to achieve a short runtime) without constraining paths to grid edges (to find any-angle paths). Unlike $\mathbf { A } ^ { * }$ on visibility graphs, they are not guaranteed to find true shortest paths. The asterisk in their names thus does not denote their optimality but rather their similarity to $\mathbf { A } ^ { * }$ . Basic Theta\* is simple to understand and implement, fast and finds short paths. Angle-Propagation Theta\* achieves a worst-case complexity per vertex expansion that is constant rather than linear in the number of cells (like that of Basic Theta\*) by propagating angle ranges when it expands vertices, but is more complex, is not as fast and finds slightly longer paths. We refer to Basic Theta\* and Angle-Propagation Theta\* collectively as Theta\*. Theta\* has unique properties, which we analyze in detail. We show experimentally that it finds shorter paths than both $\mathbf { A } ^ { * }$ with post-smoothed paths and Field $\mathbf { D } ^ { * }$ (the only other version of $\mathbf { A } ^ { * }$ we know of that propagates information along grid edges without constraining paths to grid edges) with a runtime comparable to that of $\mathbf { A } ^ { * }$ on grids. Finally, we extend Theta\* to grids that contain unblocked cells with non-uniform traversal costs and introduce variants of Theta\* which provide different tradeoffs between path length and runtime.

![](Daniel2014Theta_figs/73196bcb4bb5c53286df03202187578e6c848b79db26dd0ae3ccfcb8b92d0bd7.jpg)  
(a) Grid path

![](Daniel2014Theta_figs/3381bb0a89bf683f308ad19276a22613f6e1abb0fe476a09a62dfb7baba72db7.jpg)  
(b) True shortest path  
Figure 1: Grid path versus true shortest path

## 2. Path-Planning Problem and Notation

In this section, we describe the path-planning problem that we study in this article, namely path planning on eight-neighbor grids with blocked and unblocked cells of uniform size. Cells are labeled as either blocked (grey) or unblocked (white). We use the corners of cells (rather than their centers) as vertices. $S$ is the set of all vertices. The path-planning problem is to find an unblocked path from a given start vertex $s _ { s t a r t }$ to a given goal vertex $s _ { g o a l } .$

A path is unblocked iff each vertex on the path has line-of-sight to its successor on the path. Vertex s has line-of-sight to vertex $s ^ { \prime } { \mathrm { . } }$ , written as ${ \cal L i n e O f S i g h t } ( s , s ^ { \prime } )$ , iff the straight line from vertex s to vertex $s ^ { \prime }$ neither passes through the interior of blocked cells nor passes between blocked cells that share an edge. Pseudocode for implementing the line-of-sight function is given in Appendix A. For simplicity, we allow a straight line to pass between diagonally touching blocked cells.

$c ( s , s ^ { \prime } )$ is the length of the straight line from vertex s to vertex $s ^ { \prime } . n g h b r s _ { v i s } ( s )$ is the set of visible neighbors of vertex s in the eight compass directions, that is those neighbors of vertex s that have line-of-sight to vertex s. Figure 1 shows an example where the visible neighbors of vertex B4 are vertices A3, A4, A5, B3, B5, C3 and C4.

## 3. Existing Terrain Discretizations

Continuous terrain needs to be discretized for path planning. In this section, we compare grids to other existing terrain discretizations. We use grids to discretize terrain since they are widely used in robotics and video games (Deloura, 2000; Murphy, 2000; Rabin, 2004) and have several desirable properties:

Grids are simple data structures and allow for simple path-planning algorithms.

<sub>•</sub> Terrain can easily be discretized into a grid by laying the grid over the terrain and labeling all cells that are partially or completely obstructed as blocked.

Grids provide a comprehensive picture of all the traversable surfaces in the continuous terrain. This is essential when the path planning algorithm is used in a dynamic environment and must interact with a navigation planner. For example if a robot or video game character encounters a temporary blockage to its path, it can easily determine whether it is best to divert left (unblocked) or right (blocked) (Tozour, 2004).

Cells can store information in addition to their traversability, such as the amount of gold hidden in the region of the terrain that corresponds to the cell or a rendering of the region when displaying the terrain.

The information stored in cells can be accessed quickly since grids are random access data structures.

The precision of path and navigation planning can be improved by simply increasing the grid resolution.

We now list some alternative terrain discretizations, assuming for simplicity that the obstacles in the terrain are polygonal.

Voronoi graphs (Aurenhammer, 1991) discretize the terrain by biasing paths away from blocked polygons. The resulting paths can thus be much longer than true shortest paths.

The discretization in the work of Mitchell and Papadimitriou (1991) partitions the terrain into regions with linear and hyperbolic edges, which allows one to find true shortest paths with time and space complexity $O ( m ^ { 5 / 3 } )$ , where m is the number of corners of blocked polygons. Thus, the runtime of path planning can grow superlinearly in the number of corners of blocked polygons.

Framed Quadtrees (Yahja, Stentz, Singh, & Brumitt, 1998) recursively subdivide terrain into four equally sized cells until all cells are completely obstructed, completely unobstructed or of sufficiently small size. The resulting paths can have unnecessary heading changes (that is, heading changes that occur in free space rather than the corners of blocked polygons).

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
1 Main()
2 g(s$_{start}$) := 0;
3 parent(s$_{start}$) := s$_{start}$;
4 open := ∅;
5 open.Insert(s$_{start}$, g(s$_{start}$) + h(s$_{start}$));
6 closed := ∅;
7 while open ≠ ∅ do
8    s := open.Pop();
9    if s = s$_{goal}$ then
10    return “path found”;
11    closed := closed ∪ {s};
12    /* The following line is executed only by AP Theta*. */;
13    [UpdateBounds(s)];
14    foreach s' ∈ nghbrs$_{vis}$(s) do
15    if s'∉ closed then
16    if s'∉ open then
17    g(s') := ∞;
18    parent(s') := NULL;
19    UpdateVertex(s, s');
20    return “no path found”;
21 end
22 UpdateVertex(s,s')
23    if g(s) + c(s, s') &lt; g(s') then
24    g(s') := g(s) + c(s, s');
25    parent(s') := s;
26    if s' ∈ open then
27    open.Remove(s');
28    open.Insert(s', g(s') + h(s'));
29 end
</div>

Algorithm 1: A\*

Probabilistic roadmaps (Kavraki, Svestka, Latombe, & Overmars, 1996) or rapidly-exploring random trees (LaValle & Kuffner, 2001) place vertices randomly (in addition to the start and goal vertex). Two vertices are connected via a straight line iff they have line-of-sight. The random placement of vertices needs to be tuned carefully since it influences the runtime of path planning, the likelihood of finding a path and the length of the path.

Visibility graphs (Lee, 1978; Lozano-P´erez & Wesley, 1979) use the corners of each blocked polygon as vertices (in addition to the start and goal vertex). Two vertices are connected via a straight line iff they have line-of-sight, which allows one to find true shortest paths. The runtime of path planning can grow superlinearly in the number of vertices since the number of edges can grow quadratically in the number of vertices.

## 4. Existing Path-Planning Algorithms

In this section, we describe some existing path-planning algorithms, all of which are variants of A\* (Hart, Nilsson, & Raphael, 1968). A\* is a popular path-planning algorithm in robotics and video games. Algorithm 1 shows the pseudocode of A\*. Line 13 is to be ignored. A\* maintains three values for every vertex s:

The g-value $g ( s )$ is the length of the shortest path from the start vertex to vertex s found so far and thus is an estimate of the start distance of vertex s.

The user-provided h-value $h ( s )$ is an estimate of the goal distance of vertex s. $\mathbf { A } ^ { * }$ uses the h-value to calculate an f-value to focus the $\mathbf { A } ^ { * }$ search. The f-value $f ( s ) = g ( s ) + h ( s )$ is an estimate of the length of a shortest path from the start vertex via vertex s to the goal vertex.

<sub>•</sub> The parent parent(s) is used to extract a path from the start vertex to the goal vertex after $\mathbf { A } ^ { * }$ terminates.

## $\mathbf { A } ^ { * }$ also maintains two global data structures:

The open list is a priority queue that contains the vertices that $\mathbf { A } ^ { * }$ considers for expansion. In the pseudocode, open.Insert $( s , x )$ inserts vertex s with key x into the priority queue open, open.Remove(s) removes vertex s from the priority queue open, and open.Pop() removes a vertex with the smallest key from the priority queue open and returns it.

The closed list is a set that contains the vertices that $\mathbf { A } ^ { * }$ has already expanded. It ensures that $\mathbf { A } ^ { * }$ expands every vertex at most once.

$\mathbf { A } ^ { * }$ sets the g-value of every vertex to infinity and the parent of every vertex to NULL when it encounters the vertex for the first time [Lines 17-18]. It sets the g-value of the start vertex to zero and the parent of the start vertex to the start vertex itself [Lines 2-3]. It sets the open and closed lists to the empty list and then inserts the start vertex into the open list with the f-value as its key [4-6]. $\mathbf { A } ^ { * }$ then repeatedly executes the following procedure: If the open list is empty, then it reports that there is no path [Line 20]. Otherwise, it identifies a vertex s with the smallest f-value in the open list [Line 8]. If this vertex is the goal vertex, then $\mathbf { A } ^ { * }$ reports that it has found a path [Line 10]. Path extraction [not shown in the pseudocode] follows the parents from the goal vertex to the start vertex to retrieve a path from the start vertex to the goal vertex in reverse. Otherwise, $\mathbf { A } ^ { * }$ removes the vertex from the open list [Line 8] and expands it by inserting the vertex into the closed list [Line 11] and then generating each of its unexpanded visible neighbors, as follows: $\mathbf { A } ^ { * }$ checks whether the g-value of vertex s plus the length of the straight line from vertex s to vertex $s ^ { \prime }$ is smaller than the g-value of vertex $s ^ { \prime }$ [Line 23]. If so, then it sets the g-value of vertex $s ^ { \prime }$ to the g-value of vertex s plus the length of the straight line from vertex s to vertex $s ^ { \prime } { \mathrm { . } }$ , sets the parent of vertex $s ^ { \prime }$ to vertex s and finally inserts vertex $s ^ { \prime }$ into the open list with the f-value as its key or, if it was already in the open list, sets its key to the f-value [Lines 24-28]. It then repeats this procedure.

To summarize, when $\mathbf { A } ^ { * }$ updates the g-value and parent of an unexpanded visible neighbor $s ^ { \prime }$ of vertex s in procedure UpdateVertex, it considers the path from the start vertex to vertex $s [ = g ( s ) ]$ ] and from vertex s to vertex $s ^ { \prime }$ in a straight line $[ = c ( s , s ^ { \prime } ) ]$ , resulting in a length of $g ( s ) + c ( s , s ^ { \prime } )$ [Line 23]. $\mathbf { A } ^ { * }$ updates the g-value and parent of vertex $s ^ { \prime }$ if the considered path is shorter than the shortest path from the start vertex to vertex $s ^ { \prime }$ found so far $[ = g ( s ^ { \prime } ) ]$ ].

We now describe several existing path-planning algorithms that are versions of $\mathbf { A } ^ { * }$ and how they trade off between two conflicting criteria, namely runtime and path length, as shown in Figure 2. We introduce them in order of decreasing path lengths.

![](Daniel2014Theta_figs/53ccff46a121a150f4c44040bd66db6b2d356f4e33802956cd4cc2e4231bfed7.jpg)  
Figure 2: Runtime versus path length (relative to the length of true shortest path) on random $1 0 0 \times$ 100 grids with 20 percent blocked cells

```matlab
30 PostSmoothPath([s0, . . . , sn])
31    k := 0;
32    tk := s0;
33    foreach i := 1 ... n - 1 do
34    if NOT LineOfSight(tk, si+1) then
35    k := k + 1;
36    tk := si;
37    k := k + 1;
38    tk := sn;
39    return [t0, . . . , tk];
40 end
```  
Algorithm 2: Post-smoothing

## 4.1 A\* on Grids

One can run $\mathbf { A } ^ { * }$ on grids, that is, on the graphs given by the grid vertices and edges. The resulting paths are artificially constrained to be formed by the edges of the grid, which can be seen in Figure 1(a). As a result the paths found by $\mathbf { A } ^ { * }$ on grids are not equivalent to the true shortest paths and are unrealistic looking since they either deviate substantially from the true shortest paths or have many more heading changes, which provides the motivation for smoothing them. We use the octile distances, which can be computed using Algorithm 5, as h-values in the experiments.

![](Daniel2014Theta_figs/fadaab21f210f75720a24ad4d09678eeee9b838991fb5a44d49ef1757aa4325a.jpg)  
Figure 3: $\mathbf { A } ^ { * }$ PS path versus true shortest path

## 4.2 A\* with Post-Smoothed Paths (A\* PS)

One can run $\mathbf { A } ^ { * }$ with post-smoothed paths $( \mathbf { A } ^ { * } \mathbf { P } \mathbf { S } )$ (Thorpe, 1984). $\mathbf { A } ^ { * }$ PS runs $\mathbf { A } ^ { * }$ on grids and then smoothes the resulting path in a post-processing step, which often shortens it at an increase in runtime. Algorithm 2 shows the pseudocode of the simple smoothing algorithm that $\mathbf { A } ^ { * } \mathbf { P S }$ uses in our experiments (Botea, M¨uller, & Schaeffer, 2004), which provides a good tradeoff between runtime and path length. Assume that $\mathbf { A } ^ { * }$ on grids finds the path $[ s _ { 0 } , s _ { 1 } , \ldots , s _ { n } ]$ with $s _ { 0 } = s _ { s t a r t }$ and $s _ { n } = s _ { g o a l } . ~ \mathbf { A } ^ { * }$ PS uses the first vertex on the path as the current vertex. It then checks whether the current vertex $s _ { 0 }$ has line-of-sight to the successor $s _ { 2 }$ of its successor on the path. If so, $\mathbf { A } ^ { * }$ PS removes the intermediate vertex $s _ { 1 }$ from the path, thus shortening it. $\mathbf { A } ^ { * }$ PS then repeats this procedure by checking again whether the current vertex $s _ { 0 }$ has line-of-sight to the successor $s _ { 3 }$ of its successor on the path, and so on. As soon as the current vertex does not have line-of-sight to the successor of its successor on the path, $\mathbf { A } ^ { * }$ PS advances the current vertex and repeats this procedure until it reaches the end of the path. We use the straight-line distances $h ( s ) = c ( s , s _ { g o a l } )$ as h-values in the experiments.

$\mathbf { A } ^ { * }$ PS typically finds shorter paths than $\mathbf { A } ^ { * }$ on grids, but is not guaranteed to find true shortest paths. Figure 3 shows an example. Assume that $\mathbf { A } ^ { * }$ PS finds the dotted blue path, which is one of many shortest grid paths. It then smoothes this path to the solid blue path, which is not a true shortest path. The dashed red path, which moves above (rather than below) blocked cell B2-B3-C3-C2 is a true shortest path. $\mathbf { A } ^ { * } \mathbf { P S }$ is not guaranteed to find true shortest paths because it only considers grid paths during the $\mathbf { A } ^ { * }$ search and thus cannot make informed decisions regarding other paths during the $\mathbf { A } ^ { * }$ search, which motivates interleaving searching and smoothing. In fact, Theta\* is similar to $\mathbf { A } ^ { * }$ PS except that it interleaves searching and smoothing.

## 4.3 Field D\* (FD\*)

One can run Field $\mathbf { D } ^ { * }$ (Ferguson & Stentz, 2006) (FD\*). $\mathrm { F D ^ { * } }$ propagates information along grid edges without constraining the paths to grid edges. FD\* was designed to use $\mathbf { D } ^ { * }$ Lite (Koenig & Likhachev, 2002) for fast replanning (by reusing information from the previous $\mathbf { A } ^ { * }$ search to speed up the next one) and searches from the goal vertex to the start vertex. Our version of $\mathrm { F D ^ { * } }$ uses $\mathbf { A } ^ { * }$ and searches from the start vertex to the goal vertex, like all other path-planning algorithms in this article, which allows us to compare them fairly, except for their replanning abilities. (Theta\* is currently in the process of being extended for fast replanning in Nash, Koenig, & Likhachev, 2009.)

![](Daniel2014Theta_figs/9fdfdfacd4e40d0c1e6fc4376bd28245f413a9f220df4d9ab07518de9c8b51b9.jpg)

Figure 4: FD\* path  
![](Daniel2014Theta_figs/74ba979f38842906181f6a2c2386f58b0d4ccdcc49a2a841c0862a10de1c028a.jpg)  
Figure 5: Screenshot of $\mathrm { F D ^ { * } }$ path versus true shortest path

When FD\* updates the g-value and parent of an unexpanded visible neighbor $s ^ { \prime }$ of vertex s, it considers all paths from the start vertex to any point X (not necessarily a vertex) on the perimeter of vertex $s ^ { \prime } \left[ = g ( X ) \right]$ that has line-of-sight to vertex $s ^ { \prime } ,$ , where the perimeter is formed by connecting all the neighbors of vertex $s ^ { \prime } ,$ and from point X to vertex $s ^ { \prime }$ in a straight line $[ = c ( X , s ^ { \prime } ) ]$ , resulting in a length of $g ( X ) + c ( X , s ^ { \prime } )$ . FD\* updates the g-value and parent of vertex $s ^ { \prime }$ if the considered path is shorter than the shortest path from the start vertex to vertex $s ^ { \prime }$ found so far $[ = g ( s ^ { \prime } ) ]$ ]. We use the straight-line distances $h ( s ) = c ( s , s _ { g o a l } )$ as h-values in the experiments.

Figure 4 shows an example. The perimeter of vertex $s ^ { \prime } = B 4$ is formed by connecting all of the neighbors of vertex B4, as shown in bold. Consider point X on the perimeter. $\mathrm { F D ^ { * } }$ does not know the g-value of point X since it only stores g-values for vertices. It calculates the g-value using linear interpolation between the g-values of the two vertices on the perimeter that are adjacent to the point X. Thus, it linearly interpolates between $g ( B 3 ) = 2 . 4 1$ and $g ( C 3 ) = 2 . 0 0$ , resulting in $g ( X ) = 0 . 5 5 \times 2 . 4 1 + 0 . 4 5 \times 2 . 0 0 = 2 . 2 3$ since 0.55 and 0.45 are the distances from point X to vertices B3 and C3, respectively. The calculated g-value of point X is different from its true start distance $[ = 2 . 5 5 ]$ even though the g-values of vertices B3 and C3 are both equal to their true start distances. The reason for this mistake is simple. There exist true shortest paths from the start vertex through either vertex C3 or vertex B3 to the goal vertex. Thus, the linear interpolation assumption predicts that there must also exist a short path from the start vertex through any point along the edge that connects vertices B3 and C3 to the goal vertex. However, this is not the case since these paths need to circumnavigate blocked cell B2-B3-C3-C2, which makes them longer than expected. As a result of miscalculating the g-value of point X, FD\* sets the parent of vertex B4 to point X, resulting in a path that has an unnecessary heading change at point X and is longer than even a shortest grid path.

![](Daniel2014Theta_figs/e0492bfe8527c8d017c6620305813456308ad42e0907f973faabf4888d6fc9d4.jpg)  
(a) Simple visibility graph

![](Daniel2014Theta_figs/b5dcfe91f40d7d8e54271d461c8ceda51c9d6e50d8ede828c5f0583ce2c5d01f.jpg)  
(b) Terrain resulting in a more complex visibility graph  
Figure 6: Visibility graphs

The authors of $\mathrm { F D ^ { * } }$ recognize that the paths found by $\mathrm { F D ^ { * } }$ frequently have unnecessary heading changes and suggest to use a one-step look-ahead algorithm during path extraction (Ferguson & Stentz, 2006), which $\mathrm { F D ^ { * } }$ uses in our experiments. This one-step look-ahead algorithm allows $\mathrm { F D ^ { * } }$ to avoid some of the unnecessary heading changes, like the one in Figure 4, but does not eliminate all of them. Figure 5 shows an example of an $\mathrm { F D ^ { * } }$ path in red and the corresponding true shortest path in blue. The $\mathrm { F D ^ { * } }$ path still has many unnecessary heading changes.

## 4.4 A\* on Visibility Graphs

One can run $\mathbf { A } ^ { * }$ on visibility graphs. The visibility graph of a grid with blocked and unblocked cells contains the start vertex, the goal vertex and the corners of all blocked cells (Lozano-P´erez & Wesley, 1979). We use the straight-line distances $h ( s ) = c ( s , s _ { g o a l } )$ as h-values in the experiments. $\mathbf { A } ^ { * }$ on visibility graphs finds true shortest paths, as shown in Figure 6(a). True shortest paths have heading changes only at the corners of blocked cells, while the paths found by $\mathbf { A } ^ { * }$ on grids, $\mathbf { A } ^ { * }$ PS and $\mathrm { F D ^ { * } }$ can have unnecessary heading changes. On the other hand, $\mathbf { A } ^ { * }$ on visibility graphs can be slow. It propagates information along visibility graph edges, whose number can grow quadratically in the number of cells, while $\mathbf { A } ^ { * }$ on grids, $\mathbf { A } ^ { * }$ PS and $\mathrm { F D ^ { * } }$ propagate information along grid edges, whose number grows only linearly in the number of cells. If one constructed the visibility graphs before the $\mathbf { A } ^ { * }$ search, one would need to perform a line-of-sight check for every pair of corners of blocked cells to determine whether or not there should be a visibility graph edge between them, which requires at least 2,556 line-of-sight checks for the room in Figure 6(b) (Tozour, 2004). The number of line-of-sight checks performed by $\mathbf { A } ^ { * }$ on visibility graphs can be reduced by constructing the visibility graphs during the $\mathbf { A } ^ { * }$ search. When it expands a vertex, it performs line-of-sight checks between the expanded vertex and the corners of all blocked cells (and the goal vertex). While this can significantly reduce the number of line-of-sight checks performed in some environments, such as simple outdoor terrain, it fails to do so in others, such as cluttered indoor terrain. More complex optimizations, such as reduced visibility graphs can further reduce the number of line-ofsight checks, but do not sufficiently speed up $\mathbf { A } ^ { * }$ on visibility graphs (Liu & Arimoto, 1992).

```matlab
41 UpdateVertex(s,s')
42 if LineOfSight(parent(s), s') then
43 /* Path 2 */
44 if g(parent(s)) + c(parent(s), s') < g(s') then
45    g(s') := g(parent(s)) + c(parent(s), s');
46    parent(s') := parent(s);
47    if s' ∈ open then
48    open.Remove(s');
49    open.Insert(s', g(s') + h(s'));
50 else
51 /* Path 1 */
52 if g(s) + c(s, s') < g(s') then
53    g(s') := g(s) + c(s, s');
54    parent(s') := s;
55    if s' ∈ open then
56    open.Remove(s');
57    open.Insert(s', g(s') + h(s'));
58 end
```  
Algorithm 3: Basic Theta\*

## 5. Basic Theta\*

In this section, we introduce Theta\* (Nash et al., 2007), our version of $\mathbf { A } ^ { * }$ for any-angle path planning that propagates information along grid edges without constraining the paths to grid edges. It combines the ideas behind $\mathbf { A } ^ { * }$ on visibility graphs (where heading changes occur only at the corners of blocked cells) and $\mathbf { A } ^ { * }$ on grids (where the number of edges grows only linearly in the number of cells). Its paths are only slightly longer than true shortest paths (as found by $\mathbf { A } ^ { * }$ on visibility graphs), yet is only slightly slower than $\mathbf { A } ^ { * }$ on grids, as shown in Figure 2. The key difference between Theta\* and $\mathbf { A } ^ { * }$ on grids is that the parent of a vertex can be any vertex when using Theta\*, while the parent of a vertex has to be a neighbor of the vertex when using $\mathbf { A } ^ { * } .$ . We first introduce Basic Theta\*, a simple version of Theta\*.

Algorithm 3 shows the pseudocode of Basic Theta\*. Procedure Main is identical to that of $\mathbf { A } ^ { * }$ in Algorithm 1 and thus is not shown. Line 13 is to be ignored. We use the straight-line distances $h ( s ) = c ( s , s _ { g o a l } )$ as h-values in the experiments.

## 5.1 Operation of Basic Theta\*

Basic Theta\* is simple. It is identical to $\mathbf { A } ^ { * }$ except that, when it updates the g-value and parent of an unexpanded visible neighbor $s ^ { \prime }$ of vertex s in procedure UpdateVertex, it considers two paths instead of only the one path considered by $\mathbf { A } ^ { * }$ . Figure 7(a) shows an example. Basic Theta\* is expanding vertex B3 with parent A4 and needs to update the g-value and parent of unexpanded visible neighbor C3. Basic Theta\* considers two paths:

![](Daniel2014Theta_figs/f56e8d380ab14c296b4e81d9bc689bdc5cea8b29e4f4172caf044110987ae411.jpg)  
(a) Path 2 is unblocked

![](Daniel2014Theta_figs/9b0cff652ccc0815c9b12f389e46799cf36f284d799bb972f7a4d82dcbcec0b3.jpg)  
(b) Path 2 is blocked  
Figure 7: Paths 1 and 2 considered by Basic Theta\*

Path 1: Basic Theta\* considers the path from the start vertex to vertex $s [ = g ( s ) ]$ and from vertex s to vertex $s ^ { \prime }$ in a straight line $[ = c ( s , s ^ { \prime } ) ]$ , resulting in a length of $g ( s ) + c ( s , s ^ { \prime } )$ [Line 52]. Path 1 is the path considered by $\mathbf { A } ^ { * }$ . It corresponds to the dashed red path [A4, B3, C3] in Figure 7(a)).

Path 2: Basic Theta\* also considers the path from the start vertex to the parent of vertex $s [ =$ g(parent(s))] and from the parent of vertex s to vertex $s ^ { \prime }$ in a straight line $[ = c ( p a r e n t ( s ) , s ^ { \prime } ) ]$ resulting in a length of $g ( p a r e n t ( s ) ) + c ( p a r e n t ( s ) , s ^ { \prime } )$ [Line 44]. Path 2 is not considered by $\mathbf { A } ^ { * }$ and allows Basic Theta\* to construct any-angle paths. It corresponds to the solid blue path [A4, C3] in Figure 7(a).

Path 2 is no longer than Path 1 due to the triangle inequality. The triangle inequality states that the length of any side of a triangle is no longer than the sum of the lengths of the other two sides. It applies here since Path 1 consists of the path from the start vertex to the parent of vertex s, the straight line from the parent of vertex s to vertex $s$ (Line A) and the straight line from vertex s to vertex $s ^ { \prime }$ (Line B), Path 2 consists of the same path from the start vertex to the parent of vertex s and the straight line from the parent of vertex s to vertex $s ^ { \prime }$ (Line C) and Lines A, B and C form a triangle. Path 1 is guaranteed to be unblocked but Path 2 is not. Thus, Basic Theta\* chooses Path 2 over Path 1 if vertex $s ^ { \prime }$ has line-of-sight to the parent of vertex s and Path 2 is thus unblocked. Figure $\mathrm { 7 ( a ) }$ shows an example. Otherwise, Basic Theta\* chooses Path 1 over Path 2. Figure 7(b) shows an example. Basic Theta\* updates the g-value and parent of vertex $s ^ { \prime }$ if the chosen path is shorter than the shortest path from the start vertex to vertex $s ^ { \prime }$ found so far $[ = g ( s ^ { \prime } ) ]$ . We use the straight-line distances $h ( s ) = c ( s , s _ { g o a l } )$ as h-values in the experiments.

![](Daniel2014Theta_figs/5a046a2d39828d3de213f30fb8df01cac9448eb4a65e5a430dceee8f9c8a1f8f.jpg)  
(a)

![](Daniel2014Theta_figs/dc393f3fc0f0a276a020cd313c5d85ee2e25cb7e6eff8e20786a0a5b8797cc68.jpg)  
(b)

![](Daniel2014Theta_figs/ecf5bd4193fd6824fb89bd2ac05bbde8ad2ca82e21ad5a3755a78676833284e2.jpg)  
(c)

![](Daniel2014Theta_figs/2ccfdae5183b1a9d4b969feac5e04dc209cf331690f1eda9523d26f6c88cc7e3.jpg)  
(d)  
Figure 8: Example trace of Basic Theta\*

## 5.2 Example Trace of Basic Theta\*

Figure 8 shows an example trace of Basic Theta\*. The vertices are labeled with their g-values and parents. The arrows point to their parents. Red circles indicate vertices that are being expanded, and blue arrows indicate vertices that are generated during the current expansion. First, Basic Theta\* expands start vertex A4 with parent A4, as shown in Figure 8(a). It sets the parent of the unexpanded visible neighbors of vertex A4 to vertex A4, just like A\* would do. Second, Basic Theta\* expands vertex B3 with parent A4, as shown in Figure 8(b). Vertex B2 is an unexpanded visible neighbor of vertex B3 that does not have line-of-sight to vertex A4. Basic Theta\* thus updates it according to Path 1 and sets its parent to vertex B3. On the other hand, vertices C2, C3 and C4 are unexpanded visible neighbors of vertex B3 that have line-of-sight to vertex A4. Basic Theta\* thus updates them according to Path 2 and sets their parents to vertex A4. (The g-values and parents of the other unexpanded visible neighbors of vertex B3 are not updated.) Third, Basic Theta\* expands vertex B2 with parent B3, as shown in Figure 8(c). Vertices A1 and A2 are unexpanded visible neighbors of vertex B2 that do not have line-of-sight to vertex B3. Basic Theta\* thus updates them according to Path 1 and sets their parents to vertex B2. On the other hand, vertices B1 and C1 are unexpanded visible neighbors of vertex B2 that do have line-of-sight to vertex B3. Basic Theta\* thus updates them according to Path 2 and sets their parents to vertex B3. Fourth, Basic Theta\* expands goa vertex C1 with parent B3 and terminates, as shown in Figure 8(d). Path extraction then follows the parents from goal vertex C1 to start vertex A4 to retrieve the true shortest path [A4, B3, C1] from the start vertex to the goal vertex in reverse.

## 5.3 Properties of Basic Theta\*

We now discuss the properties of Basic Theta\*.

## 5.3.1 CORRECTNESS AND COMPLETENESS

Basic Theta\* is correct (that is, finds only unblocked paths from the start vertex to the goal vertex) and complete (that is, finds a path from the start vertex to the goal vertex if one exists). We use the following lemmata in the proof.

Lemma 1. If there exists an unblocked path between two vertices then there also exists an unblocked grid path between the same two vertices.

Proof. An unblocked path between two vertices exists iff an unblocked any-angle path $[ s _ { 0 } , \ldots , s _ { n } ]$ exists between the same two vertices. Consider any path segment $\overline { { s _ { k } s _ { k + 1 } } }$ of this any-angle path. If the path segment is horizontal or vertical, then consider the unblocked grid path from vertex $s _ { k }$ to vertex $s _ { k + 1 }$ that coincides with the path segment. Otherwise, consider the sequence $\left( b _ { 0 } , \ldots , b _ { m } \right)$ of unblocked cells whose interior the path segment passes through. Any two consecutive cells $b _ { j }$ and $b _ { j + 1 }$ share at least one vertex $s _ { j + 1 } ^ { \prime }$ since the cells either share an edge or are diagonally touching. (If they share more than one vertex, pick one arbitrarily.) Consider the grid path $[ s _ { 0 } ^ { \prime } = $ $s _ { k } , s _ { 1 } ^ { \prime } , \ldots , s _ { m } ^ { \prime } , s _ { m + 1 } ^ { \prime } = s _ { k + 1 } ]$ . This grid path from vertex $s _ { k }$ to vertex $s _ { k + 1 }$ is unblocked since any two consecutive vertices on it are corners of the same unblocked cell and are thus visible neighbors. Repeat this procedure for every path segment of the any-angle path and concatenate the resulting grid paths to an unblocked grid path from vertex $s _ { 0 }$ to vertex $s _ { n }$ . (If several consecutive vertices on the grid path are identical, then all of them but one can be removed.) □

Lemma 2. At any point during the execution of Basic Theta\*, following the parents from any vertex in the open or closed lists to the start vertex retrieves an unblocked path from the start vertex to this vertex in reverse.

Proof. We prove by induction that the lemma holds and that the parent of any vertex in the union of the open or closed lists itself is in the union of the open or closed lists. This statement holds initially because the start vertex is the only vertex in the union of the open or closed lists and it is its own parent. We now show that the statement continues to hold whenever a vertex changes either its parent or its membership in the union of the open or closed lists. Once a vertex is a member of the union of the open or closed lists, it continues to be a member. A vertex can become a member in the union of the open or closed lists only when Basic Theta\* expands some vertex s and updates the g-value and parent of an unexpanded visible neighbor $s ^ { \prime }$ of vertex s in procedure UpdateVertex. Vertex s is thus in the closed list, and its parent is in the union of the open or closed lists according to the induction assumption. Thus, following the parents from vertex s (or its parent) to the start vertex retrieves an unblocked path from the start vertex to vertex $s$ (or its parent, respectively) in reverse according to the induction assumption. If Basic Theta\* updates vertex $s ^ { \prime }$ according to Path 1, then the statement continues to hold since vertices $s$ and $s ^ { \prime }$ are visible neighbors and the path segment from vertex s to vertex $s ^ { \prime }$ is thus unblocked. If Basic Theta\* updates vertex $s ^ { \prime }$ according to Path 2, then the statement continues to hold since Basic Theta\* explicitly checks that the path segment from the parent of vertex s to vertex $s ^ { \prime }$ is unblocked. There are no other ways in which the parent of a vertex can change. □

Theorem 1. Basic Theta\* terminates and path extraction retrieves an unblocked path from the start vertex to the goal vertex if such a path exists. Otherwise, Basic Theta\* terminates and reports that no unblocked path exists.

Proof. The following properties together prove the theorem. Their proofs utilize the fact that Basic Theta\* terminates iff the open is empty or it expands the goal vertex. The start vertex is initially in the open list. Any other vertex is initially neither in the open nor closed lists. A vertex neither in the open nor closed lists can be inserted into the open list. A vertex in the open list can be removed from the open list and be inserted into the closed list. A vertex in the closed list remains in the closed list.

Property 1: Basic Theta\* terminates. It expands one vertex in the open list during each iteration. In the process, it removes the vertex from the open list and can then never insert it into the open list again. Since the number of vertices is finite, the open list eventually becomes empty and Basic Theta\* has to terminate if it has not terminated earlier already.

Property 2: If Basic Theta\* terminates because its open list is empty, then there does not exist an unblocked path from the start vertex to the goal vertex. We prove the contrapositive. Assume that there exists an unblocked path from the start vertex to the goal vertex. We prove by contradiction that Basic Theta\* then does not terminate because its open list is empty. Thus, assume also that Basic Theta\* terminates because its open list is empty. Then, there exists an unblocked grid path $[ s _ { 0 } = s _ { s t a r t } , \ldots , s _ { n } = s _ { g o a l } ]$ from the start vertex to the goal vertex according to Lemma 1. Choose vertex $s _ { i }$ to be the first vertex on the grid path that is not in the closed list when Basic Theta\* terminates. The goal vertex is not in the closed list when Basic Theta\* terminates since Basic Theta\* would otherwise have terminated when it expanded the goal vertex. Thus, vertex $s _ { i }$ exists. Vertex $s _ { i }$ is not the start vertex since the start vertex would otherwise be in the open list and Basic Theta\* could not have terminated because its open list is empty. Thus, vertex $s _ { i }$ has a predecessor on the grid path. This predecessor is in the closed list when Basic Theta\* terminates since vertex $s _ { i }$ is the first vertex on the grid path that is not in the closed list when Basic Theta\* terminates. When Basic Theta\* expanded the predecessor, it added vertex $s _ { i }$ to the open list. Thus, vertex $s _ { i }$ is still in the open list when Basic Theta\* terminates. But then Basic Theta\* could not have terminated because its open list is empty, which is a contradiction.

Property 3: If Basic Theta\* terminates because it expands the goal vertex, then path extraction retrieves an unblocked path from the start vertex to the goal vertex because following the parents from the goal vertex to the start vertex retrieves an unblocked path from the start vertex to the goal vertex in reverse according to Lemma 2.

![](Daniel2014Theta_figs/9f2ec7121cba215b1b00b24b6c921d5fec857ac20d1f4796829f5d1dc99236b0.jpg)  
(a)

![](Daniel2014Theta_figs/be0649309248cca14e550916d86f8984fe08a524b363fe248d65729872f33c9f.jpg)  
Figure 9: Basic Theta\* paths versus true shortest paths

## 5.3.2 OPTIMALITY

Basic Theta\* is not optimal (that is, it is not guaranteed to find true shortest paths) because the parent of a vertex has to be either a visible neighbor of the vertex or the parent of a visible neighbor, which is not always the case for true shortest paths. Figure 9(a) shows an example where the dashed red path [E1, B9] is a true shortest path from start vertex E1 to vertex B9 since vertex E1 has lineof-sight to vertex B9. However, vertex E1 is neither a visible neighbor nor the parent of a visible neighbor of vertex B9 since vertex E1 does not have line-of-sight to these vertices (highlighted in red). Thus, Basic Theta\* cannot set the parent of vertex B9 to vertex E1 and does not find a true shortest path from vertex E1 to vertex B9. Similarly, Figure 9(b) shows an example where the dashed red path [E1, D8, C10] is a true shortest path from vertex E1 to vertex C10. However, vertex D8 is neither a visible neighbor nor the parent of a visible neighbor of vertex C10 since start vertex E1 either has line-of-sight to them or Basic Theta\* found paths from vertex E1 to them that do not contain vertex D8. In fact, the truly shortest paths from vertex E1 to all visible neighbors of vertex C10 that vertex E1 does not have line-of-sight to move above (rather than below) blocked cell C7- C8-D8-D7. Thus, Basic Theta\* cannot set the parent of vertex C10 to vertex D8 and thus does not find a true shortest path from vertex E1 to vertex C10. The solid blue path from vertex E1 to vertex B9 in Figure 9(a) and the solid blue path from vertex E1 to vertex C10 in Figure 9(b) are less than a factor of 1.002 longer than the true shortest paths.

![](Daniel2014Theta_figs/c7ff479dc401848140104dfdfe736528876bb381ed436c17e3b62c4a67b36d84.jpg)  
Figure 10: Heading changes of Basic Theta\*

## 5.3.3 HEADING CHANGES

Basic Theta\* takes advantage of the fact that true shortest paths have heading changes only at the corners of blocked cells. However, the paths found by Basic Theta\* can occasionally have unnecessary heading changes. Figure 10 shows an example where Basic Theta\* finds the solid blue path [A1, D5, D6] from vertex A1 to vertex D6. The reason for this mistake is simple. Assume that the open list contains both vertices C5 and D5. The f-value of vertex C5 is $f ( C 5 ) = g ( C 5 ) +$ $h ( C 5 ) = 4 . 6 1 + 1 . 4 1 = 6 . 0 2$ and its parent is vertex C4. The f-value of vertex D5 is $f ( D 5 ) =$ $5 . 0 0 + 1 . 0 0 = 6 . 0 0$ and its parent is vertex A1. Thus Basic Theta\* expands vertex D5 before vertex C5 (since its f-value is smaller). When Basic Theta\* expands vertex D5 with parent A1, it generates vertex D6. Vertex D6 is an unexpanded visible neighbor of vertex D5 that does not have line-of-sight to vertex A1. Basic Theta\* thus updates it according to Path 1, sets its f-value to $f ( D 6 ) = 6 . 0 0 + 0 . 0 0 = 6 . 0 0$ , sets its parent to vertex D5 and inserts it into the open list. Thus Basic Theta\* expands goal vertex D6 before vertex C5 (since its f-value is smaller) and terminates. Path extraction then follows the parents from goal vertex D6 to start vertex A1 to retrieve the solid blue path [A1, D5, D6]. Thus, Basic Theta\* never expands vertex C5, which would have resulted in it setting the parent of vertex D6 to vertex C4 according to Path 2 and path extraction retrieving the dashed red path [A1, C4, D6] which is the true shortest path. The solid blue path from vertex A1 to vertex D6 in Figure 10 is less than a factor of 1.027 longer than true shortest path.

```txt
59 UpdateVertex(s,s')
60 if s ≠ s_start AND lb(s) ≤ Θ(s, parent(s), s') ≤ ub(s) then
61 /* Path 2 */
62 if g(parent(s)) + c(parent(s), s') < g(s') then
63    g(s') := g(parent(s)) + c(parent(s), s');
64    parent(s') := parent(s);
65    if s' ∈ open then
66    open.Remove(s');
67    open.Insert(s', g(s') + h(s'));
68 else
69 /* Path 1 */
70 if g(s) + c(s, s') < g(s') then
71    g(s') := g(s) + c(s, s');
72    parent(s') := s;
73    if s' ∈ open then
74    open.Remove(s');
75    open.Insert(s', g(s') + h(s'));
76 end
77 UpdateBounds(s)
78 lb(s) := -∞; ub(s) := ∞;
79 if s ≠ s_start then
80 foreach blocked cell b adjacent to s do
81    if ∀s' ∈ corners(b) : parent(s) = s' OR Θ(s, parent(s), s') < 0 OR
82    (Θ(s, parent(s), s') = 0 AND c(parent(s), s') ≤ c(parent(s), s)) then
83    lb(s) = 0;
84    if ∀s' ∈ corners(b) : parent(s) = s' OR Θ(s, parent(s), s') > 0 OR
85    (Θ(s, parent(s), s') = 0 AND c(parent(s), s') ≤ c(parent(s), s)) then
86    ub(s) = 0;
87 foreach s' ∈ nghbrs_vis(s) do
88    if s' ∈ closed AND parent(s) = parent(s') AND s' ≠ s_start then
89    if lb(s') + Θ(s, parent(s), s') ≤ 0 then
90    lb(s) := max(lb(s), lb(s') + Θ(s, parent(s), s'));
91    if ub(s') + Θ(s, parent(s), s') ≥ 0 then
92    ub(s) := min(ub(s), ub(s') + Θ(s, parent(s), s'));
93    if c(parent(s), s') < c(parent(s), s) AND parent(s) ≠ s' AND (s'∉ closed OR parent(s) ≠ parent(s'))
94    then
95    if Θ(s, parent(s), s') < 0 then
96    lb(s) := max(lb(s), Θ(s, parent(s), s'));
97    if Θ(s, parent(s), s') > 0 then
98 end
```  
Algorithm 4: AP Theta\*

## 6. Angle-Propagation Theta\* (AP Theta\*)

The runtime of Basic Theta\* per vertex expansion (that is, the runtime consumed during the generation of the unexpanded visible neighbors when expanding a vertex) can be linear in the number of cells since the runtime of each line-of-sight check can be linear in the number of cells. In this section, we introduce Angle-Propagation Theta\* (AP Theta\*), which reduces the runtime of Basic

![](Daniel2014Theta_figs/91fcbbdab2ac38d565d0a0254b1c76544341d39cba02f0c36a662c7da029db4d.jpg)  
Figure 11: Region of points with line-of-sight to vertex s

Theta\* per vertex expansion from linear to constant.<sup>1</sup> The key difference between AP Theta\* and Basic Theta\* is that AP Theta\* propagates angle ranges and uses them to determine whether or not two vertices have line-of-sight.

If there is a light source at a vertex and light cannot pass through blocked cells, then cells in the shadows do not have line-of-sight to the vertex while all other cells have line-of-sight to the vertex. Each contiguous region of points that have line-of-sight to the vertex can be characterized by two rays emanating from the vertex and thus by an angle range defined by two angle bounds. Figure 11 shows an example where all points within the red angle range defined by the two angle bounds $\theta _ { 1 }$ and $\theta _ { 2 }$ have line-of-sight to vertex s. AP Theta\* calculates the angle range of a vertex when it expands the vertex and then propagates it along grid edges, resulting in a constant runtime per vertex expansion since the angle ranges can be propagated in constant time and the line-of-sight checks can be performed in constant time as well.

Algorithm 4 shows the pseudocode of AP Theta\*. Procedure Main is identical to that of A\* in Algorithm 1 and thus is not shown. Line 13 is to be executed. We use the straight-line distances $h ( s ) = c ( s , s _ { g o a l } )$ as h-values in the experiments.

## 6.1 Definition of Angle Ranges

We now discuss the key concept of an angle range. AP Theta\* maintains two additional values for every vertex s, namely a lower angle bound lb(s) of vertex s and an upper angle bound $u b ( s )$ of vertex s, that together form the angle range $[ l b ( s ) , u b ( s ) ]$ of vertex s. The angle bounds correspond to headings of rays (measured in degrees) that originate at the parent of vertex s. The heading of the ray from the parent of vertex s to vertex s is zero degrees. A visible neighbor of vertex s is guaranteed to have line-of-sight to the parent of vertex s if (but not necessarily only if) the heading of the ray from the parent of vertex s to the visible neighbor of vertex s is contained in the angle range of vertex s. Figure 12 shows an example where vertex C3 with parent A4 has angle range [ 18, 27]. Thus, all visible neighbors of vertex C3 in the red region are guaranteed to have line-ofsight to the parent of vertex C3. For example, vertex C4 is guaranteed to have line-of-sight to the parent of vertex C3 but vertex B2 is not. AP Theta\* therefore assumes that vertex B2 does not have line-of-sight to the parent of vertex C3.

![](Daniel2014Theta_figs/603a5d335879a28828e70fe489d84914e7ecf284756f3ed2065ae8c441eba0f3.jpg)  
Figure 12: Angle range of AP Theta\*

We now define the concept of an angle range more formally. $\Theta ( s , p , s ^ { \prime } ) \in [ - 9 0 , 9 0 ]$ , which gives AP Theta\* its name, is the angle (measured in degrees) between the ray from vertex p to vertex s and the ray from vertex $p$ to vertex $s ^ { \prime } .$ . It is positive if the ray from vertex $p$ to vertex s is clockwise from the ray from vertex $p$ to vertex $s ^ { \prime } ,$ , zero if the ray from vertex $p$ to vertex s has the same heading as the ray from vertex $p$ to vertex $s ^ { \prime } ,$ , and negative if the ray from vertex $p$ to vertex s is counterclockwise from the ray from vertex $p$ to vertex $s ^ { \prime } .$ Figure 12 shows an example where $\Theta ( C 3 , A 4 , C 4 ) = 2 7$ and $\Theta ( C 3 , A 4 , B 3 ) = - 1 8 .$ A visible neighbor $s ^ { \prime }$ of vertex s is guaranteed to have line-of-sight to the parent of vertex $s$ if (but not necessarily only if) $l b ( s ) \leq \Theta ( s , p a r e n t ( s ) , s ^ { \prime } ) \leq u b ( s )$ (Visibility Property).

## 6.2 Update of Angle Ranges

We now discuss how AP Theta\* calculates the angle range of a vertex when it expands the vertex. This calculation is complicated by the fact that AP Theta\* is not guaranteed to have sufficient information to determine the angle range exactly since the order of vertex expansions depends on a variety of factors, such as the h-values. In this case, AP Theta\* can constrain the angle range more than necessary to guarantee that the Visibility Property holds and that it finds unblocked paths.

When AP Theta\* expands vertex s, it sets the angle range of vertex s initially to $[ - \infty , \infty ]$ , meaning that all visible neighbors of the vertex are guaranteed to have line-of-sight to the parent of the vertex. It then constrains the angle range more and more if vertex s is not the start vertex.

AP Theta\* constrains the angle range of vertex s based on each blocked cell b that is adjacent to vertex s (that is, that vertex s is a corner of $b ,$ written as $s \in c o r n e r s ( b ) )$ provided that at least one of two conditions is satisfied:

Case 1: If every corner $s ^ { \prime }$ of blocked cell b satisfies at least one of the following conditions:

$$
- p a r e n t (s) = s ^ {\prime} \text {   or   }
$$

$$
\begin{array}{l} - \Theta (s, p a r e n t (s), s ^ {\prime}) <   0 \text {or} \\ - \Theta (s, p a r e n t (s), s ^ {\prime}) = 0 \text {and} c (p a r e n t (s), s ^ {\prime}) \leq c (p a r e n t (s), s), \end{array}
$$

then AP Theta\* assumes that a vertex $s ^ { \prime \prime }$ does not have line-of-sight to the parent of vertex s if the ray from the parent of vertex s to vertex s is counterclockwise from the ray from the parent of vertex s to vertex $s ^ { \prime \prime } .$ , that is, if $\Theta ( s , p a r e n t ( s ) , s ^ { \prime \prime } ) < 0$ . AP Theta\* therefore sets the lower angle bound of vertex s to $\Theta ( s , p a r e n t ( s ) , s ) = 0 [ \mathrm { L i n e } 8 3 ]$

Case 2: If every corner $s ^ { \prime }$ of blocked cell b satisfies at least one of the following conditions:

$$
\begin{array}{l} - p a r e n t (s) = s ^ {\prime} \text {or} \\ - \Theta (s, p a r e n t (s), s ^ {\prime}) > 0 \text {or} \\ - \Theta (s, p a r e n t (s), s ^ {\prime}) = 0 \text {and} c (p a r e n t (s), s ^ {\prime}) \leq c (p a r e n t (s), s), \end{array}
$$

then AP Theta\* assumes that a vertex $s ^ { \prime \prime }$ does not have line-of-sight to the parent of vertex s if the ray from the parent of vertex s to vertex s is clockwise from the ray from the parent of vertex s to vertex $s ^ { \prime \prime } .$ , that is, if $\Theta ( s , p a r e n t ( s ) , s ^ { \prime \prime } ) > 0$ . AP Theta\* therefore sets the upper angle bound of vertex s to $\Theta ( s , p a r e n t ( s ) , s ) = 0 [ \mathrm { L i n e } 8 6 ]$

AP Theta\* also constrains the angle range of vertex s based on each visible neighbor $s ^ { \prime }$ of vertex s provided that at least one of two conditions is satisfied:

Case 3: If vertex $s ^ { \prime }$ satisfies all of the following conditions:

$$
\begin{array}{l} - s ^ {\prime} \in c l o s e d \text { and } \\ - p a r e n t (s) = p a r e n t (s ^ {\prime}) \text { and } \\ - s ^ {\prime} \neq s _ {s t a r t}, \end{array}
$$

then AP Theta\* constrains the angle range of vertex s by intersecting it with the angle range of vertex $s ^ { \prime }$ [Lines 90 and 92]. To do that, it first shifts the angle range of vertex $s ^ { \prime }$ by $\Theta ( s , p a r e n t ( s ) , s ^ { \prime } )$ degrees to take into account that the angle range of vertex $s ^ { \prime }$ is calibrated so that the heading of the ray from the joint parent of vertices s and $s ^ { \prime }$ to vertex $s ^ { \prime }$ is zero degrees, while the angle range of vertex s is calibrated so that the heading of the ray from the joint parent of vertices s and $s ^ { \prime }$ to vertex s is zero degrees. Lines 89 and 91 ensure that the lower angle bound always remains non-positive and the upper angle bound always remains non-negative, respectively. The fact that lower angle bounds should be non-positive (and upper angle bounds non-negative) is intuitive in that if a vertex s is assigned parent vertex $p$ then the angle of the ray from vertex p to vertex s should be included in the angle range of vertex s.

Case 4: If vertex $s ^ { \prime }$ satisfies all of the following conditions:

$- \ p a r e n t ( s ) \neq s ^ { \prime }$ and

– s′  closed or parent(s) = parent(s′),

then AP Theta\* has insufficient information about vertex s′. AP Theta\* therefore cannot determine the angle range of vertex s exactly and makes the conservative assumption that vertex $s ^ { \prime }$ barely has line-of-sight to the parent of vertex s [Lines 95 and 97].

The Visibility Property holds after AP Theta\* has updated the angle range of vertex s in procedure UpdateBounds. Thus, when AP Theta\* checks whether or not a visible neighbor s′ of vertex s has line-of-sight to the parent of vertex s, it now checks whether or not $l b ( s ) \leq \Theta ( s , p a r e n t ( s ) , s ^ { \prime } ) \leq$ ub(s) [Line 60] is true instead of whether or not LineOfSight(parent(s), s′) [Line 42] is true . These are the only differences between AP Theta\* and Basic Theta\*.

Figure 13(a) shows an example where AP Theta\* calculates the angle range of vertex A4. It sets the angle range to [ , ]. Figure 13(b) shows an example where AP Theta\* calculates the angle range of vertex B3. It sets the angle range initially to $[ - \infty , \infty ]$ . It then sets the lower angle bound to 0 degrees according to Case 1 based on the blocked cell A2-A3-B3-B2 [Line 83]. It sets the upper angle bound to 45 degrees according to Case 4 based on vertex B4, which is unexpanded and thus not in the closed list [Line 97]. Figure 13(c) shows an example where AP Theta\* calculates the angle range of vertex B2. It sets the angle range initially $\mathrm { t o } \ [ - \infty , \infty ]$ . It then sets the lower angle bound to 0 degrees according to Case 1 based on the blocked cell A2-A3-B3-B2 [Line 83]. Assume that vertex C1 is not the goal vertex. Figure 13(d) then shows an example where AP Theta\* calculates the angle range of vertex C1. It sets the angle range initially to $[ - \infty , \infty ]$ . It then sets the lower angle bound to -27 degrees according to Case 3 based on vertex B2 [Line 90] and the upper angle bound to 18 degrees according to Case 4 based on vertex C2, which is unexpanded and thus not in the closed list [Line 97].

## 6.3 Example Trace of AP Theta\*

Figure 13 shows an example trace of AP Theta\* using the path-planning problem from Figure 8. The labels of the vertices now include the angle ranges.

## 6.4 Properties of AP Theta\*

We now discuss the properties of AP Theta\*. AP Theta\* operates in the same way as Basic Theta\* and thus has similar properties as Basic Theta\*. For example, AP Theta\* is correct and complete. It is not guaranteed to find true shortest paths, and its paths can occasionally have unnecessary heading changes.

AP Theta\* sometimes constrains the angle ranges more than necessary to guarantee that it finds unblocked paths, which means that its line-of-sight checks sometimes fail incorrectly in which case it has to update vertices according to Path 1 rather than Path 2. AP Theta\* is still complete since it finds an unblocked grid path if all line-of-sight checks fail, and there always exists an unblocked grid path if there exists an unblocked any-angle path. However, the paths found by AP Theta\* can be longer than those found by Basic Theta\*. Figure 14 shows an example. When AP Theta\* expands vertex C4 with parent B1 and calculates the angle range of vertex C4, vertex C3 is unexpanded and thus not in the closed list. This means that AP Theta\* has insufficient information about vertex

![](Daniel2014Theta_figs/caa18c3836109f77f1a5a74b0a5684e78a7b7bd790a0288e9343a8cf52c5ead1.jpg)  
(a)

![](Daniel2014Theta_figs/138586f8a4e42a0c04cd70c6877159bd2015b8e044fdb48c4fbbce705e097b6e.jpg)  
(b)

![](Daniel2014Theta_figs/a4389a817c3f38588ff5bf5384b1ff70967ecf0da5c34026ec053c5a040fcd0b.jpg)  
(c)

![](Daniel2014Theta_figs/c145515f3450bca58a4a1310e63d8b9de002e975fe281a5edcbcec73e680d09f.jpg)  
(d)

Figure 13: Example trace of AP Theta\*  
![](Daniel2014Theta_figs/8314de4ec5ddf309f9ba809392383e0433a43eccad265e118a7fee2198002d24.jpg)  
Figure 14: Basic Theta\* path versus AP Theta\* path

C3 because, for example, it does not know whether or not cell C2-C3-D3-D2 is unblocked. AP Theta\* therefore cannot determine the angle range of vertex C4 exactly and makes the conservative assumption that vertex C3 barely has line-of-sight to vertex B1 and sets the lower angle bound of vertex C4 according to Case 4 based on vertex C3. It then uses the resulting angle range to determine that the unexpanded visible neighbor D4 of vertex C4 is not guaranteed to have line-ofsight to vertex B1. However, vertex D4 does have line-of-sight to vertex B1 if cell C2-C3-D3-D2 is unblocked. AP Theta\* eventually finds the solid blue path [B1, C3, D4] from start vertex B1 to vertex D4, while Basic Theta\* finds the dashed red path [B1, D4], which is the true shortest path.

![](Daniel2014Theta_figs/b2ca028a5a37c4078b95f901b90db0eadbada18b02759229a61e6acbc98fb363.jpg)  
Figure 15: Map of Baldur’s Gate II

The correctness and completeness proof of Basic Theta\* needs to get changed slightly for AP Theta\* since AP Theta\* performs its line-of-sight checks differently.

Theorem 2. AP Theta\* terminates and path extraction retrieves an unblocked path from the start vertex to the goal vertex if such a path exists. Otherwise, AP Theta\* terminates and reports that no unblocked path exists.

Proof. The proof is similar to the proof of Theorem 1 since AP Theta\* uses the angle ranges only to determine whether or not Path 2 is blocked but not to determine whether or not Path 1 is blocked. The only property that needs to be proved differently is that two vertices indeed have line-of-sight if (but not necessarily only if) the line-of-sight check of AP Theta\* succeeds, see Appendix B.

## 7. Experimental Results

In this section, we compare Basic Theta\* and AP Theta\* to $\mathbf { A } ^ { * }$ on grids, A\* PS, FD\* and $\mathbf { A } ^ { * }$ on visibility graphs with respect to their path length, number of vertex expansions, runtime (measured in seconds) and number of heading changes.

We compare these path-planning algorithms on 100  100 and 500  500 grids with different percentages of randomly blocked cells (random grids) and scaled maps from the real-time strategy game Baldur’s Gate II (game maps). Figure 15 (Bulitko, Sturtevant, & Kazakevich, 2005) shows an example of a game map. The start and goal vertices are the south-west corners of cells. For random grids, the start vertex is in the south-west cell. The goal vertex is in a cell randomly chosen from the column of cells furthest east. Cells are blocked randomly but a one-unit border of unblocked cells guarantees that there is path from the start vertex to the goal vertex. For game maps, the start and goal vertices are randomly chosen from the corners of unblocked cells. We average over 500 random 100 100 grids, 500 random 500 500 grids and 118 game maps.

<table><tr><td></td><td></td><td>FD*</td><td>Basic Theta*</td><td>AP Theta*</td><td>A* on Visibility Graphs (true shortest path)</td><td>A* on Grids</td><td>A* PS</td></tr><tr><td rowspan="6">100×100</td><td>Game Maps</td><td>40.04</td><td>39.98</td><td>40.05</td><td>39.96</td><td>41.77</td><td>40.02</td></tr><tr><td>Random Grids 0%</td><td>114.49</td><td>114.33</td><td>114.33</td><td>114.33</td><td>120.31</td><td>114.33</td></tr><tr><td>Random Grids 5%</td><td>114.15</td><td>113.94</td><td>113.94</td><td>113.83</td><td>119.76</td><td>114.71</td></tr><tr><td>Random Grids 10%</td><td>114.74</td><td>114.51</td><td>114.51</td><td>114.32</td><td>119.99</td><td>115.46</td></tr><tr><td>Random Grids 20%</td><td>115.20</td><td>114.93</td><td>114.95</td><td>114.69</td><td>120.31</td><td>116.16</td></tr><tr><td>Random Grids 30%</td><td>115.45</td><td>115.22</td><td>115.25</td><td>114.96</td><td>120.41</td><td>116.69</td></tr><tr><td rowspan="6">500×500</td><td>Game Maps</td><td>223.64</td><td>223.30</td><td>224.40</td><td>N/A</td><td>233.66</td><td>223.70</td></tr><tr><td>Random Grids 0%</td><td>576.19</td><td>575.41</td><td>575.41</td><td>N/A</td><td>604.80</td><td>575.41</td></tr><tr><td>Random Grids 5%</td><td>568.63</td><td>567.30</td><td>567.34</td><td>N/A</td><td>596.45</td><td>573.46</td></tr><tr><td>Random Grids 10%</td><td>576.23</td><td>574.57</td><td>574.63</td><td>N/A</td><td>603.51</td><td>581.03</td></tr><tr><td>Random Grids 20%</td><td>580.19</td><td>578.41</td><td>578.51</td><td>N/A</td><td>604.93</td><td>585.62</td></tr><tr><td>Random Grids 30%</td><td>581.73</td><td>580.18</td><td>580.35</td><td>N/A</td><td>606.38</td><td>588.98</td></tr></table>

Table 1: Path length

<table><tr><td></td><td></td><td>FD*</td><td>Basic Theta*</td><td>AP Theta*</td><td>A* on Visibility Graphs (true shortest path)</td><td>A* on Grids</td><td>A* PS</td></tr><tr><td rowspan="6">100×100</td><td>Game Maps</td><td>0.0111</td><td>0.0060</td><td>0.0084</td><td>0.4792</td><td>0.0048</td><td>0.0052</td></tr><tr><td>Random Grids 0%</td><td>0.0229</td><td>0.0073</td><td>0.0068</td><td>0.0061</td><td>0.0053</td><td>0.0208</td></tr><tr><td>Random Grids 5%</td><td>0.0275</td><td>0.0090</td><td>0.0111</td><td>0.0766</td><td>0.0040</td><td>0.0206</td></tr><tr><td>Random Grids 10%</td><td>0.0305</td><td>0.0111</td><td>0.0145</td><td>0.3427</td><td>0.0048</td><td>0.0204</td></tr><tr><td>Random Grids 20%</td><td>0.0367</td><td>0.0150</td><td>0.0208</td><td>1.7136</td><td>0.0084</td><td>0.0222</td></tr><tr><td>Random Grids 30%</td><td>0.0429</td><td>0.0183</td><td>0.0263</td><td>3.7622</td><td>0.0119</td><td>0.0240</td></tr><tr><td rowspan="6">500×500</td><td>Game Maps</td><td>0.1925</td><td>0.1166</td><td>0.1628</td><td>N/A</td><td>0.0767</td><td>0.1252</td></tr><tr><td>Random Grids 0%</td><td>0.3628</td><td>0.1000</td><td>0.0234</td><td>N/A</td><td>0.0122</td><td>0.6270</td></tr><tr><td>Random Grids 5%</td><td>0.4514</td><td>0.1680</td><td>0.1962</td><td>N/A</td><td>0.0176</td><td>0.6394</td></tr><tr><td>Random Grids 10%</td><td>0.5608</td><td>0.2669</td><td>0.3334</td><td>N/A</td><td>0.0573</td><td>0.6717</td></tr><tr><td>Random Grids 20%</td><td>0.6992</td><td>0.3724</td><td>0.5350</td><td>N/A</td><td>0.1543</td><td>0.6852</td></tr><tr><td>Random Grids 30%</td><td>0.8562</td><td>0.5079</td><td>0.7291</td><td>N/A</td><td>0.3238</td><td>0.7355</td></tr></table>

Table 2: Runtime

<table><tr><td></td><td></td><td>FD*</td><td>Basic Theta*</td><td>AP Theta*</td><td>A* on Visibility Graphs (true shortest path)</td><td>A* on Grids</td><td>A* PS</td></tr><tr><td rowspan="6">100×100</td><td>Game Maps</td><td>247.07</td><td>228.45</td><td>226.42</td><td>68.23</td><td>197.19</td><td>315.08</td></tr><tr><td>Random Grids 0%</td><td>592.74</td><td>240.42</td><td>139.53</td><td>1.00</td><td>99.00</td><td>1997.29</td></tr><tr><td>Random Grids 5%</td><td>760.17</td><td>430.06</td><td>361.17</td><td>35.35</td><td>111.96</td><td>1974.27</td></tr><tr><td>Random Grids 10%</td><td>880.21</td><td>591.31</td><td>520.91</td><td>106.23</td><td>169.98</td><td>1936.56</td></tr><tr><td>Random Grids 20%</td><td>1175.42</td><td>851.79</td><td>813.14</td><td>357.33</td><td>386.41</td><td>2040.10</td></tr><tr><td>Random Grids 30%</td><td>1443.44</td><td>1113.40</td><td>1089.96</td><td>659.36</td><td>620.18</td><td>2153.28</td></tr><tr><td rowspan="6">500×500</td><td>Game Maps</td><td>6846.62</td><td>6176.37</td><td>6220.58</td><td>N/A</td><td>5580.32</td><td>9673.88</td></tr><tr><td>Random Grids 0%</td><td>11468.11</td><td>2603.40</td><td>663.34</td><td>N/A</td><td>499.00</td><td>49686.47</td></tr><tr><td>Random Grids 5%</td><td>15804.81</td><td>7450.85</td><td>5917.25</td><td>N/A</td><td>755.66</td><td>49355.41</td></tr><tr><td>Random Grids 10%</td><td>19874.62</td><td>11886.95</td><td>10405.34</td><td>N/A</td><td>2203.83</td><td>50924.01</td></tr><tr><td>Random Grids 20%</td><td>26640.83</td><td>18621.61</td><td>17698.75</td><td>N/A</td><td>6777.15</td><td>50358.66</td></tr><tr><td>Random Grids 30%</td><td>34313.28</td><td>25744.57</td><td>25224.92</td><td>N/A</td><td>14641.36</td><td>53732.82</td></tr></table>

Table 3: Number of vertex expansions

All path-planning algorithms are implemented in C# and executed on a 3.7 GHz Core 2 Duo with 2 GByte of RAM. Our implementations are not optimized and can possibly be improved.

<table><tr><td></td><td></td><td>FD*</td><td>Basic Theta*</td><td>AP Theta*</td><td>A* on Visibility Graphs (true shortest paths)</td><td>A* on Grids</td><td>A* PS</td></tr><tr><td rowspan="6">100×100</td><td>Game Maps</td><td>34.25</td><td>3.08</td><td>3.64</td><td>2.92</td><td>5.21</td><td>2.83</td></tr><tr><td>Random Grids 0%</td><td>123.40</td><td>0.00</td><td>0.00</td><td>0.00</td><td>0.99</td><td>0.00</td></tr><tr><td>Random Grids 5%</td><td>113.14</td><td>5.14</td><td>6.03</td><td>5.06</td><td>6.00</td><td>4.53</td></tr><tr><td>Random Grids 10%</td><td>106.66</td><td>8.96</td><td>9.87</td><td>8.84</td><td>10.85</td><td>8.48</td></tr><tr><td>Random Grids 20%</td><td>98.76</td><td>15.21</td><td>15.96</td><td>14.74</td><td>19.42</td><td>14.45</td></tr><tr><td>Random Grids 30%</td><td>96.27</td><td>19.96</td><td>20.62</td><td>19.44</td><td>26.06</td><td>18.35</td></tr><tr><td rowspan="6">500×500</td><td>Game Maps</td><td>219.70</td><td>4.18</td><td>7.58</td><td>N/A</td><td>10.19</td><td>3.84</td></tr><tr><td>Random Grids 0%</td><td>667.00</td><td>0.00</td><td>0.00</td><td>N/A</td><td>1.00</td><td>0.00</td></tr><tr><td>Random Grids 5%</td><td>592.65</td><td>21.91</td><td>27.99</td><td>N/A</td><td>24.68</td><td>22.27</td></tr><tr><td>Random Grids 10%</td><td>559.69</td><td>41.60</td><td>47.40</td><td>N/A</td><td>49.73</td><td>43.16</td></tr><tr><td>Random Grids 20%</td><td>506.10</td><td>72.49</td><td>76.79</td><td>N/A</td><td>91.40</td><td>69.44</td></tr><tr><td>Random Grids 30%</td><td>481.16</td><td>97.21</td><td>100.31</td><td>N/A</td><td>123.81</td><td>89.43</td></tr></table>

Table 4: Number of heading changes

![](Daniel2014Theta_figs/6d3a33430aeb1af85c376be4add6ecbb033e0137ac13871c7053cbb9d82fc395.jpg)  
(a) Path length

![](Daniel2014Theta_figs/9edb6a3c75337373fd0e65230f3726aeedf73ef069acc395b57079028da826e8.jpg)  
(b) Runtime

![](Daniel2014Theta_figs/64bf0d9ec24a9774bbe5763e86e7b34751473c08a1eb5528d86f1413c9052e68.jpg)  
(c) Number of vertex expansions

![](Daniel2014Theta_figs/5d84d396f2622c98df21efdcb3fed5f77f6da0ac8d3946bfb30927d7b1e363e5.jpg)  
(d) Number of heading changes  
Figure 16: Random 500  500 grids

<table><tr><td colspan="2">99 h(s)</td></tr><tr><td>100</td><td> $\Delta_x := |s.x - (s_{goal}).x|;$ </td></tr><tr><td>101</td><td> $\Delta_y := |s.y - (s_{goal}).y|;$ </td></tr><tr><td>102</td><td> $largest := max(\Delta_x, \Delta_y);$ </td></tr><tr><td>103</td><td> $smallest := min(\Delta_x, \Delta_y);$ </td></tr><tr><td>104</td><td> $return \sqrt{2} \cdot smallest + (largest - smallest);$ </td></tr><tr><td colspan="2">105 end</td></tr></table>

Algorithm 5: Calculation of octile distances

$\mathbf { A } ^ { * }$ on grids, $\mathrm { A ^ { * } P S , F D ^ { * } }$ and $\mathbf { A } ^ { * }$ on visibility graphs break ties among vertices with the same fvalue in the open list in favor of vertices with larger g-values (when they decide which vertex to expand next) since this tie-breaking scheme typically results in fewer vertex expansions and thus shorter runtimes for $\mathbf { A } ^ { * }$ . Care must thus be taken when calculating the g-values, h-values and fvalues precisely. The numerical precision of these floating point numbers can be improved for $\mathbf { A } ^ { * }$ on grids by representing them in the form $m + { \sqrt { 2 } } n$ for integers m and n. Basic Theta\* and $\mathbf { A P }$ Theta\* break ties in favor of vertices with smaller g-values for the reasons explained in Section 9.

We use all path-planning algorithms with consistent h-values since consistent h-values result in short paths for $\mathbf { A } ^ { * } .$ . Consistent h-values satisfy the triangle inequality, that is, the h-value of the goal vertex is zero and the h-value of any potential non-goal parent of any vertex is no greater than the distance from the potential non-goal parent of the vertex to the vertex plus the h-value of the vertex (Hart et al., 1968; Pearl, 1984). Consistent h-values are lower bounds on the corresponding goal distances of vertices. Increasing consistent h-values typically decreases the number of vertex expansions for $\mathbf { A } ^ { * }$ and thus also the runtime of $\mathbf { A } ^ { * }$ . We thus use all path-planning algorithms with the largest consistent h-values that are easy to calculate. For Basic Theta\*, AP Theta\*, $\mathrm { F D ^ { * } }$ and $\mathbf { A } ^ { * }$ on visibility graphs, the goal distances of vertices can be equal to the true goal distances, that is, the goal distances on grids if the paths are not constrained to grid edges. We therefore use these path planning algorithms with the straight-line distances $h ( s ) = c ( s , s _ { g o a l } )$ as h-values in our experiments. The straight-line distances are the goal distances on grids without blocked cells if the paths are not constrained to grid edges. For $\mathbf { A } ^ { * }$ on grids and $\mathbf { A } ^ { * } \mathbf { P S }$ , the goal distances of vertices are equal to the goal distances on grids if the paths are constrained to grid edges. We could therefore use them with the larger octile distances as h-values in our experiments. The octile distances are the goal distances on grids without blocked cells if the paths are constrained to grid edges. Algorithm 5 shows how to calculate the octile distance of a given vertex s, where s.x and s.y are the x and y coordinates of vertex s, respectively. We indeed use $\mathbf { A } ^ { * }$ on grids with the octile distances but $\mathbf { A } ^ { * }$ PS with the straight-line distances since smoothing is then typically able to shorten the resulting paths much more at an increase in the number of vertex expansions and thus runtime. Grids without blocked cells provide an example. With the octile distances as h-values, $\mathbf { A } ^ { * }$ on grids finds paths in which all diagonal movements (whose lengths are $\sqrt { 2 } )$ precede all horizontal or vertical movements (whose lengths are 1) because the paths with the largest number of diagonal movements are the longest ones among all paths with the same number of movements due to the tie-breaking scheme used. On the other hand, with the straight-line distances as h-values, $\mathbf { A } ^ { * }$ on grids finds paths that interleave the diagonal movements with the horizontal and vertical movements (which means tha it is likely that there are lots of opportunities to smooth the paths even for grids with some blocked cells) and that are closer to the straight line between the start and goal vertices (which means tha it is likely that the paths are closer to true shortest paths even for grids with some blocked cells), because the h-values of vertices closer to the straight line are typically smaller than the h-values of vertices farther away from the straight line.

![](Daniel2014Theta_figs/eacc2373a802e091b948b5a6a39576756af0f764e041553748530af3ab20cbb2.jpg)  
Figure 17: True shortest paths found by $\mathrm { F D ^ { * } }$ (left), A\* PS (middle) and Basic Theta\* (right)

Tables 1-4 report our experimental results. The runtime of $\mathbf { A } ^ { * }$ on visibility graphs (which finds true shortest paths) is too long on $5 0 0 \times 5 0 0$ grids and thus is omitted. Figure 16 visualizes the experimental results on random 500 500 grids. The path length of $\mathbf { A } ^ { * }$ on grids is much larger than the path lengths of the other path-planning algorithms and thus is omitted.

We make the following observations about the path lengths:

The path-planning algorithms in order of increasing path lengths tend to be: $\mathbf { A } ^ { * }$ on visibility graphs (which finds true shortest paths), Basic Theta\*, AP Theta\*, FD\*, $\mathbf { A } ^ { * }$ PS and $\mathbf { A } ^ { * }$ on grids. On random 500 <sub>×</sub> 500 grids with 20 percent blocked cells, Basic Theta\* finds shorter paths than AP Theta\* 70 percent of the time, shorter paths than FD\* 97 percent of the time, shorter paths than $\mathbf { A } ^ { * }$ PS 94 percent of the time and shorter paths than $\mathbf { A } ^ { * }$ on grids 99 percent of the time.

The paths found by Basic Theta\* and AP Theta\* are almost as short as true shortest paths even though AP Theta\* sometimes constrains the angle ranges more than necessary. For example, they are on average less than a factor of 1.003 longer than true shortest paths on $1 0 0 \times 1 0 0$ grids.

Basic Theta\* finds true shortest paths more often than $\mathrm { F D ^ { * } }$ and A\* PS. Figure 17 shows an example where the light green vertex in the center is the start vertex and the red, green and blue vertices represent goal vertices to which FD\*, A\* PS and Basic Theta\* find true shortest paths, respectively.

We make the following observations about the runtimes. The path-planning algorithms in order of increasing runtimes tend to be: $\mathbf { A } ^ { * }$ on grids, Basic Theta\*, AP Theta\*, A\* PS, FD\* and $\mathbf { A } ^ { * }$ on visibility graphs.

We make the following observations about the numbers of vertex expansions. The path-planning algorithms in order of increasing numbers of vertex expansions tend to be: $\mathbf { A } ^ { * }$ on visibility graphs, $\mathbf { A } ^ { * }$ on grids, AP Theta\*, Basic Theta\*, FD\* and $\mathbf { A } ^ { * }$ PS. (The number of vertex expansions of $\mathbf { A } ^ { * }$ on grids and A\* PS are different because we use them with different h-values.)

<table><tr><td></td><td>FD*</td><td>Basic Theta*</td><td>AP Theta*</td><td>A* PS</td></tr><tr><td>Runtime</td><td>5.21</td><td>3.65</td><td>5.70</td><td>3.06</td></tr><tr><td>Runtime per Vertex Expansion</td><td>0.000021</td><td>0.000015</td><td>0.000023</td><td>0.000012</td></tr></table>

Table 5: Path-planning algorithms without post-processing steps on random 500  500 grids with 20 percent blocked cells

Finally, we make the following observations about the number of heading changes. The pathplanning algorithms in order of increasing numbers of heading changes tend to be: A\* PS, $\mathbf { A } ^ { * }$ on visibility graphs, Basic Theta\*, AP Theta\*, A\* on grids and FD\*.

There are some exceptions to the trends reported above. We therefore perform paired t-tests. They show with confidence level α = 0.01 that Basic Theta\* indeed finds shorter paths than AP Theta\*, A\* PS and $\mathrm { F D ^ { * } }$ and that Basic Theta\* indeed has a shorter runtime than AP Theta\*, A\* PS and FD\*.

To summarize, A\* on visibility graphs finds true shortest paths but is slow. On the other hand, A\* on grids finds long paths but is fast. Any-angle path planning lies between these two extremes. Basic Theta\* dominates AP Theta\*, A\* PS and FD\* in terms of the tradeoff between runtime and path length. It finds paths that are almost as short as true shortest paths and is almost as fast as $\mathbf { A } ^ { * }$ on grids. It is also simpler to implement than AP Theta\*. Therefore, we build on Basic Theta\* for the remainder of this article, although we report some experimental results for AP Theta\* as well. However, AP Theta\* reduces the runtime of Basic Theta\* per vertex expansion from linear to constant. It is currently unknown whether or not constant time line-of-sight checks can be devised that make AP Theta\* faster than Basic Theta\*. This is an interesting area of future research since AP Theta\* is potentially a first step toward significantly reducing the runtime of any-angle path planning via more sophisticated line-of-sight checks.

## 8. Extensions of Theta\*

In this section, we extend Basic Theta\* to find paths from a given start vertex to all other vertices and to find paths on grids that contain unblocked cells with non-uniform traversal costs.

## 8.1 Single Source Paths

So far, Basic Theta\* has found paths from a given start vertex to a given goal vertex. We now discuss a version of Basic Theta\* that finds single source paths (that is, paths from a given start vertex to all other vertices) by terminating only when the open list is empty instead of when either the open list is empty or it expands the goal vertex.

Finding single source paths requires all path-planning algorithms to expand the same number of vertices, which minimizes the influence of the h-values on the runtime and thus results in a clean comparison since the h-values sometimes are chosen to trade off between runtime and path length.

The runtimes of A\* PS and FD\* are effected more than those of Basic Theta\* and AP Theta\* when finding single source paths since they require post-smoothing or path-extraction steps for each path, and thus need to post-process many paths. Table 5 reports the runtimes of the path-planning algorithms without these post-processing steps. The runtime of Basic Theta\* per vertex expansion is similar to that of A\* PS and shorter than that of either AP Theta\* and FD\* because the later two algorithms require more floating point operations.

![](Daniel2014Theta_figs/b047cce79a3d7be8a06a30868d5b922d6312c55bd03e7ba1d9aa48d66f30445a.jpg)  
Figure 18: Basic Theta\* on grids that contain unblocked cells with non-uniform traversal costs

(a) Small contiguous regions of uniform traversal costs (b) Large contiguous regions of uniform traversal costs

<table><tr><td></td><td>A* on Grids</td><td>FD*</td><td>Basic Theta*</td><td></td><td>A* on Grids</td><td>FD*</td><td>Basic Theta*</td></tr><tr><td>Path Cost</td><td>4773.59</td><td>4719.26</td><td>4730.96</td><td>Path Cost</td><td>1251.88</td><td>1208.89</td><td>1207.06</td></tr><tr><td>Runtime</td><td>11.28</td><td>14.98</td><td>19.02</td><td>Runtime</td><td>3.42</td><td>5.31</td><td>5.90</td></tr></table>

Table 6: Path-planning algorithms on random 1000 1000 grids with non-uniform traversal costs

## 8.2 Non-Uniform Traversal Costs

So far, Basic Theta\* has found paths on grids that contain unblocked cells with uniform traversal costs. In this case, true shortest paths have heading changes only at the corners of blocked cells and the triangle inequality holds, which means that Path 2 is no longer than Path 1. We now discuss a version of Basic Theta\* that finds paths on grids that contain unblocked cells with non-uniform traversal costs by computing and comparing path lengths (which are now path costs) appropriately. In this case, true shortest paths can also have heading changes at the boundaries between unblocked cells with different traversal costs and the triangle inequality is no longer guaranteed to hold, which means that Path 2 can be more costly than Path 1. Thus, Basic Theta\* no longer unconditionally chooses Path 2 over Path 1 if Path 2 is unblocked [Line 42] but chooses the path with the smaller cost. It uses the standard Cohen-Sutherland clipping algorithm from computer graphics (Foley, van Dam, Feiner, & Hughes, 1992) to calculate the cost of Path 2 during the line-of-sight check. Figure 18 shows an example for the path segment C1A6 from vertex C1 to vertex A6. This straight line is split into line segments at the points where it intersects with cell boundaries. The cost of the path segment is the sum of the costs of its line segments $\overline { { I _ { i } I _ { i + 1 } } }$ , and the cost of each line segment is the product of its length and the traversal cost of the corresponding unblocked cell.

We found that changing the test on Line 52 in Algorithm 3 from “strictly less than” to “less than or equal to” slightly reduces the runtime of Basic Theta\*. This is a result of the fact that it is faster to compute the cost of a path segment that corresponds to Path 1 than Path 2 since it tends to consist of fewer line segments.

![](Daniel2014Theta_figs/b40e5cda39ff673b95489146e102ad4769fb5dda92adefca735c0dd56e4878b2.jpg)

![](Daniel2014Theta_figs/a65a1b8ebb419468c84eda52f6b199840a0cec8d98bcf2744a890038fcf8b16f.jpg)  
Figure 19: Non-monotonicity of f-values of Basic Theta\*

We compare Basic $\mathrm { T h e t a ^ { * } }$ to $\mathbf { A } ^ { * }$ on grids and $\mathrm { F D ^ { * } }$ with respect to their path cost and runtime (measured in seconds) since $\mathbf { A } ^ { * }$ can easily be adapted to grids that contain unblocked cells with non-uniform traversal costs and $\mathrm { F D ^ { * } }$ was designed for this case. We compare these path-planning algorithms on $1 0 0 0 \times 1 0 0 0 \mathrm { g r i d s } ,$ where each cell is assigned an integer traversal cost from 1 to 15 (corresponding to an unblocked cell) and infinity (corresponding to a blocked cell), similar to the technique used in the work of Ferguson and Stentz (2006) . If a path lies on the boundary between two cells with different traversal costs, then we use the smaller traversal cost of the two cells. The start and goal vertices are the south-west corners of cells. The start vertex is in the south-west cell. The goal vertex is in a cell randomly chosen from the column of cells furthest east. We average over 100 random grids. Table 6 (a) reports our results if every traversal cost is chosen with uniform probability, resulting in small contiguous regions of uniform traversal costs. The path cost and runtime of $\mathrm { F D ^ { * } }$ are both smaller than those of Basic Theta\*. The path cost of $\mathbf { A } ^ { * }$ on grids is only about 1 percent larger than that of $\mathrm { F D ^ { * } }$ although its runtime is much smaller than that of $\mathrm { F D ^ { * } }$ . Thus, any-angle planning does not have a large advantage over $\mathbf { A } ^ { * }$ on grids. Table $6 ( \mathsf { b } )$ reports our results if traversal cost one is chosen with probability 50 percent and all other traversal costs are chosen with uniform probability, resulting in large contiguous regions of uniform traversal costs. The path cost of Basic $\mathrm { T h e t a ^ { * } }$ is now smaller than that of $\mathrm { F D ^ { * } }$ and its runtime is about the same as that of $\mathrm { F D ^ { * } }$ . The paths found by $\mathrm { F D ^ { * } }$ tend to have many more unnecessary heading changes in regions with the same traversal costs than those of Basic Theta\*, which outweighs the paths found by Basic Theta\* not having necessary heading changes on the boundary between two cells with different traversal costs. The path cost of $\mathbf { A } ^ { * }$ on grids is more than 3 percent larger than that of Basic Theta\*. Thus, any-angle planning now has a larger advantage over $\mathbf { A } ^ { * }$ on grids.

## 9. Trading Off Runtime and Path Length: Exploiting h-Values

There are strategies for trading off runtime and path length that $\mathbf { A } ^ { * }$ on grids and Basic Theta\* share. However, their behavior can be very different even though the two algorithms have very similar pseudocode. In this section, we develop versions of Basic Theta\* that might be able to find shorter paths at an increase in runtime, including versions that use weighted h-values with weights less than one, that break ties among vertices with the same f-value in the open list in favor of vertices with smaller g-values (when they decide which vertex to expand next) and that re-expand vertices whose f-values have decreased.

We use all path-planning algorithms with consistent h-values. $\mathbf { A } ^ { * }$ on grids then has the following properties (Pearl, 1984): The f-value of any expanded vertex is no larger than the f-value of any of its unexpanded visible neighbors after updating them according to Path 1, which implies that the f-value of any vertex that is expanded before some other vertex is no larger than the f-value of this other vertex. Consequently, at any point in time during a search once a vertex has been expanded, following the parents from the expanded vertex to the start vertex retrieves a shortest path from the start vertex to the expanded vertex in reverse, which implies that $\mathbf { A } ^ { * }$ cannot find shorter paths by expanding vertices more than once. Basic $\mathrm { T h e t a ^ { * } }$ has different properties: The f-value of an expanded vertex can be larger than the f-value of one or more of its unexpanded visible neighbors after updating them according to Path 2, which implies that the f-value of a vertex that is expanded before some other vertex can be larger than the f-value of this other vertex. Consequently, at any point in time during a search once a vertex has been expanded, following the parents from the expanded vertex to the start vertex is not guaranteed to retrieve a shortest path from the start vertex to the vertex in reverse, which implies that Basic $\mathrm { T h e t a ^ { * } }$ might find shorter paths by expanding vertices more than once. Figure 19 shows an example. When Basic $\mathrm { T h e t a ^ { * } }$ expands start vertex C1 with parent C1, it generates vertex B2. Vertex B2 is an unexpanded visible neighbor of vertex C1 that has line-of-sight to vertex C1. Basic Theta\* thus updates it according to Path 2 (which is the same as Path 1 in this case), sets its f-value to $f ( B 2 ) = 1 . 4 1 + 3 . 1 6 = 4 . 5 7$ , sets its parent to vertex C1 and inserts it into the open list (Figure 19(a)). When Basic $\mathrm { T h e t a ^ { * } }$ later expands vertex B2 with parent C1, it generates vertex B3. Vertex B3 is an unexpanded visible neighbor of vertex B2 that has line-of-sight to vertex C1. Basic $\mathrm { T h e t a ^ { * } }$ thus updates it according to Path 2, sets its f-value to $f ( B 3 ) = 2 . 2 4 + 2 . 2 4 = 4 . 4 8$ , sets its parent to vertex C1 and inserts it into the open list (Figure 19(b)). Thus, the f-value of expanded vertex B2 is indeed larger than the f-value of its unexpanded visible neighbor B3 after updating it according to Path 2 because the increase in g-value from vertex B2 to vertex $\mathbf { B } ^ { 3 } \left[ = 0 . 8 3 \right]$ is less than the decrease in h-value from vertex B2 to vertex $\mathbf { B } ^ { 3 } \left[ = 0 . 9 2 \right]$ When Basic $\mathrm { T h e t a ^ { * } }$ later expands vertex B3, the f-value of vertex $\mathbf { B } 2 \ [ = 4 . 5 7 ]$ that is expanded before vertex B3 is indeed larger than the f-value of vertex $\mathrm { B } 3 [ = 4 . 4 8 ]$

These properties suggest that Basic Theta\* might be able to find shorter paths at an increase in runtime by re-expanding vertices or expanding additional vertices (for example by using weighted h-values with weights less than one) while $\mathbf { A } ^ { * }$ cannot. At the same time, standard optimizations of $\mathbf { A } ^ { * }$ that decrease its runtime might also be able to decrease the runtime of Basic Theta\* (such as breaking ties among vertices with the same f-value in the open list in favor of vertices with larger g-values). In this section we investigate these tradeoffs.

## 9.1 Weighted h-Values

So far, Basic Theta\* has used consistent h-values $h ( s ) . \mathrm { A } ^ { * }$ with consistent h-values finds paths of the same length no matter how small or large the h-values are. Decreasing consistent h-values typically increases the number of vertex expansions for $\mathbf { A } ^ { * }$ . We therefore now discuss a version of Basic $\mathrm { T h e t a ^ { * } }$ that might be able to find shorter paths at an increase in runtime by using weighted h-values with weights less than one. This version of Basic Theta\* uses the h-values $h ( s ) = w \times c ( s , s _ { g o a l } )$ for a given weight $0 \leq w < 1$ and thus is similar to Weighted $\mathbf { A } ^ { * }$ (Pohl, 1973), except that Weighted $\mathbf { A } ^ { * }$ typically uses weights greater than one. Figure 20(a) shows an example of the resulting effect on the number of vertex expansions and path length. The green vertex in the north-east is the start vertex, and the red vertex in the south-west is the goal vertex. Basic Theta\* with weight 1.00 (as used so far) expands the orange vertices and finds the red path. Basic Theta\* with weight 0.75 expands the blue vertices and finds the blue path. Thus, Basic Theta\* expands more vertices with weight 0.75 than with weight 1.00 and the resulting path is shorter since it passes through vertices that are expanded with weight 0.75 but not with weight 1.00.

![](Daniel2014Theta_figs/11c9d0c6eadeac30523f1bc912fbb1ff60f5cf5da688ae7f8e6da87c78b362cb.jpg)  
(a) Expanded vertices by Basic Theta\* with different weights

![](Daniel2014Theta_figs/bedead7daa77acfd2a023ac605d9e6cfa5abf6d5341981eb0661052b95358c38.jpg)  
(b) Random <sup>500 × 500</sup> grids with 20 percent blocked cells  
Figure 20: Weighted h-values

<table><tr><td rowspan="2"></td><td colspan="2">Smaller g-Values</td><td colspan="2">Larger g-Values</td></tr><tr><td>Basic Theta*</td><td>AP Theta*</td><td>Basic Theta*</td><td>AP Theta*</td></tr><tr><td>Path Length</td><td>578.41</td><td>578.51</td><td>578.44</td><td>578.55</td></tr><tr><td>Number of Vertex Expansions</td><td>18621.61</td><td>17698.75</td><td>18668.03</td><td>17744.94</td></tr><tr><td>Runtime</td><td>0.3724</td><td>0.5350</td><td>0.3829</td><td>0.5389</td></tr></table>

Table 7: Random 500 500 grids with 20 percent blocked cells

Figure 20(b) reports the effect of different weights on the path length and number of vertex expansions of Basic Theta\* and AP Theta\* on random 500 500 grids with 20 percent blocked cells. (The graphs of the number of vertex expansions of Basic Theta\* and AP Theta\* nearly coincide.) Decreasing the weight decreases the path length at an increase in the number of vertex expansions and thus the runtime. The path length decreases more for AP Theta\* than Basic Theta\* since AP Theta\* can constrain the angle ranges more than necessary and thus benefits in two ways from expanding more vertices. However, neither Basic Theta\* nor AP Theta\* are guaranteed to find true shortest paths even if their weights are zero.

## 9.2 Tie Breaking

So far, Basic Theta\* has broken ties among vertices in the open list with the same f-value in favor of vertices with larger g-values (when it decides which vertex to expand next). A\* with consistent h-values finds paths of the same length no matter which tie-breaking scheme it uses. Breaking ties in favor of vertices with smaller g-values typically increases the number of vertex expansions and thus the runtime. We therefore discuss a version of Basic Theta\* that might be able to find shorter paths at an increase in runtime by breaking ties in favor of vertices with smaller g-values. Figure 21 shows an example of the resulting effect on path length. Vertices C4 and B4 have the same f-value but vertex B4 has a larger g-value since f(C4) = 3.83+1.41 = 5.24 and f(B4) = 4.24+1 = 5.24. If Basic Theta\* breaks ties in favor of vertices with larger g-values, then it expands vertex B4 with parent E1 before vertex C4 with parent C3 and eventually expands the goal vertex with parent B4 and terminates. Path extraction then follows the parents from goal vertex B5 to start vertex E1 to retrieve the dashed red path [E1, B4, B5]. However, if Basic Theta\* breaks ties in favor of vertices with smaller g-values, then it expands vertex C4 with parent C3 before vertex B4 with parent E1 and eventually expands the goal vertex with parent C3 and terminates. Path extraction then follows the parents from goal vertex B5 to start vertex E1 to retrieve the shorter solid blue path [E1, C3, B5].

Table 7 reports the effect of the tie-breaking scheme on the path length, number of vertex expansions and runtime of Basic Theta\* and AP Theta\* on random 500 500 grids with 20 percent blocked cells. Breaking ties in favor of vertices with smaller g-values neither changes the path length, number of vertex expansions nor runtime significantly. The effect of the tie-breaking scheme is small since fewer vertices have the same f-value for Basic Theta\* and AP Theta\* than for A\* on grids because the number of possible g-values and h-values is larger for any-angle path planning.

![](Daniel2014Theta_figs/1095add1219f4caab03f5497abc094d1db7f581eadeaa9c6fbda8d654dec29c2.jpg)  
Figure 21: Basic Theta\* paths for different tie-breaking schemes

<table><tr><td></td><td>Basic Theta* without Vertex Re-Expansions</td><td>Basic Theta* with Vertex Re-Expansions</td></tr><tr><td>Path Length</td><td>578.41</td><td>577.60</td></tr><tr><td>Number of Vertex Expansions</td><td>18621.61</td><td>22836.37</td></tr><tr><td>Runtime</td><td>0.3724</td><td>0.5519</td></tr></table>

Table 8: Random 500 500 grids with 20 percent blocked cells

There is also a second method in which breaking ties can effect path length. So far, Basic Theta\* has chosen Path 2 over Path 1 if an unexpanded visible neighbor of a vertex has line-of-sight to the parent of the vertex. However, it can choose Path 1 over Path 2 if both paths are equally long, which increases the runtime due to the additional comparison. Figure 21 shows an example of the resulting effect on path length. Assume that Basic Theta\* expands vertex B4 before vertex C4. If Basic Theta\* chooses Path 2 over Path 1 then it expands vertex B4 with parent E1 and eventually expands the goal vertex B5 with parent B4 and terminates. Path extraction then follows the parents from goal vertex B5 to start vertex E1 to retrieve the dashed red path [E1, B4, B5]. However, if Basic Theta\* chooses Path 1 over Path 2 then it expands vertex B4 with parent C3 and eventually expands goal vertex B5 with parent C3 and terminates. Path extraction then follows the parents from goal vertex B5 to start vertex E1 to retrieve the shorter solid blue path [E1, C3, B5].

## 9.3 Re-Expanding Vertices

So far, Basic Theta\* has used a closed list to ensure that it expands each vertex at most once. A\* with consistent h-values does not re-expand vertices whether or not it uses a closed list since it cannot find a shorter path from the start vertex to a vertex after expanding that vertex. On the other hand, Basic Theta\* can re-expand vertices if it does not use a closed list since it can find a shorter path from the start vertex to a vertex after expanding the vertex. It then re-inserts the vertex into the open list and eventually re-expands it.<sup>2</sup> Figure 22 shows an example of the effect of vertex re-expansions on path length. Basic Theta\* without vertex re-expansions eventually expands vertex C8 with parent D4. Vertex C9 is an unexpanded visible neighbor of vertex C8 that has line-of-sigh to vertex D4. Basic Theta\* without vertex re-expansions thus updates it according to Path 2 and sets its parent to vertex D4. After termination, path extraction follows the parents from goal vertex B9 to start vertex E1 to retrieve the dashed red path [E1, D4, C9, B9]. However, Basic Theta\* with vertex re-expansions eventually expands vertex C8 with parent D4 and later re-expands vertex C8 with parent E1. Vertex C9 is a visible neighbor of vertex C8 that has line-of-sight to vertex E1. Basic Theta\* with vertex re-expansions thus updates it according to Path 2 and sets its parent to vertex E1. After termination, path extraction follows the parents from goal vertex B9 to start vertex E1 to retrieve the shorter solid blue path [E1, C9, B9].

![](Daniel2014Theta_figs/f63818f14a3ab6e2894048e4dac64604c44e14e4a00b5e569e0478d69636e846.jpg)  
Figure 22: Basic Theta\* paths with and without vertex re-expansions

Theorem 3. Basic Theta\* with vertex re-expansions terminates and path extraction returns an unblocked path from the start vertex to the goal vertex if such a path exists. Otherwise, Basic Theta\* with vertex re-expansions terminates and reports that no unblocked path exists.

Proof. The proof is similar to the proof of Theorem 1. The only property that needs to be proved differently is that Basic Theta\* with vertex re-expansions terminates since it is no longer true that it can never insert a vertex into the open list again once it has removed the vertex from the open list. However, since the number of vertices is finite, there are only a finite number of acyclic paths from the start vertex to each vertex. Therefore, the number of possible g-values is finite. Therefore, Basic Theta\* with vertex re-expansions can reduce the g-value of each vertex only a finite number of times and thus inserts each vertex into the open list a finite number of times. Thus, the open list eventually becomes empty and Basic Theta\* has to terminate if it has not terminated earlier already. □

Table 8 reports the effect of vertex re-expansions on the path length, number of vertex expansions and runtime of Basic Theta\* on random $5 0 0 \times 5 0 0$ grids with 20 percent blocked cells. Vertex re-expansions decrease the path length slightly at an increase in the number of vertex expansions and thus the runtime.

## 10. Trading Off Runtime and Path Length: Other Approaches

There are additional strategies for trading off runtime and path length that are specific to Basic Theta\*. In this section, we develop versions of Basic Theta\* that might be able to find shorter paths at an increase in runtime by examining more paths, including versions that check for line-ofsight to the parent of a parent, that use key vertices to identify promising parents and that increase the number of visible neighbors and thus the number of potential parents when updating vertices according to Path 1.

## 10.1 Three Paths

So far, Basic Theta\* has considered two paths (namely Paths 1 and 2) when it updates the gvalue and parent of an unexpanded visible neighbor $s ^ { \prime }$ of vertex s. We now discuss a version of Basic Theta\* that considers a third path, namely the path from the start vertex to the parent of the parent of vertex $s ~ [ = ~ g ( p a r e n t ( p a r e n t ( s ) ) ) ]$ and from it to vertex $s ^ { \prime }$ in a straight line [= $c ( p a r e n t ( p a r e n t ( s ) ) , s ^ { \prime } ) ]$ , resulting in a length of $g ( p a r e n t ( p a r e n t ( s ) ) ) + c ( p a r e n t ( p a r e n t ( s ) ) , s ^ { \prime } )$ This version of Basic Theta\* might be able to find shorter paths at an increase in runtime since the third path is no longer than Path 2 due to the triangle inequality. However, our experimental results (not reported here) show that the third path does not decrease the path length significantly because the original version of Basic Theta\* already determines that the parent of the parent of vertex s does not have line-of-sight to some vertex that shares its parent with vertex s. Thus, it is very unlikely that the parent of the parent of vertex s has line-of-sight to vertex $s ^ { \prime }$ and thus that the third path is unblocked.

## 10.2 Key Vertices

So far, Basic Theta\* has considered two paths (namely Paths 1 and 2) when it updates the g-value and parent of an unexpanded visible neighbor $s ^ { \prime }$ of vertex s. The parent of a vertex then is either a visible neighbor of the vertex or the parent of a visible neighbor, which is not always the case for true shortest paths. We now discuss a version of Basic Theta\* that considers additional paths, namely the paths from the start vertex to cached key vertices and from them to vertex $s ^ { \prime }$ in a straight line. This version of Basic Theta\* might be able to find shorter paths at an increase in runtime due to the fact that the parent of a vertex can now also be one of the key vertices. However, our experimental results (not reported here) show that key vertices decrease the path length only slightly at a larger increase in runtime due to the overhead of having to select key vertices, maintain them and consider a larger number of paths.

![](Daniel2014Theta_figs/11b94ce6fb45012249609c05d61fa47d9afc82a08ef647d6f815065ed1db6c92.jpg)  
(a) Branching factor 4

![](Daniel2014Theta_figs/b04f4772d3d82c0cba458ebbf527d91a086f0328585652db7f8dbec8475fc5f7.jpg)  
(b) Branching factor 8

![](Daniel2014Theta_figs/69ae09525b0ce900be90923931a8155b9a12317e705b5ae97b5a47fcf4d21c1d.jpg)  
(c) Branching factor 16  
Figure 23: Grids with different branching factors

![](Daniel2014Theta_figs/397a455bc1a37ab07cb900ad6f163e51618d1927218e9c79a33da233dcfbfead.jpg)  
Figure 24: Basic Theta\* on random 500 500 grids with 20 percent blocked cells

## 10.3 Larger Branching Factors

So far, Basic Theta\* has operated on eight-neighbor grids. We now discuss a version of Basic Theta\* that operates on grids with different numbers of neighbors and thus different branching factors. Figure 23 shows the neighbors of the center vertex for branching factors 4, 8 and 16 respectively. This version of Basic Theta\* might be able to find shorter paths at an increase in runtime since larger branching factors increase the number of visible neighbors of vertices and thus their number of potential parents when updating them according to Path 1. Figure 24 reports the effect of larger branching factors on the path length and runtime of Basic Theta\* on random 500 500 grids with 20 percent blocked cells. Larger branching factors indeed decrease the path length at an increase in runtime.

## 11. Conclusions

Any-angle path-planning algorithms find paths without artificially constraining the headings of the paths. We presented two new correct and complete any-angle path-planning algorithms. Basic Theta\* and Angle-Propagation Theta\* (AP Theta\*) are both variants of $\mathbf { A } ^ { * }$ that propagate information along grid edges (to achieve a short runtime) without constraining paths to grid edges (to find any-angle paths). Basic Theta\* is simple to understand and implement, fast and finds short paths. However, it is not guaranteed to find true shortest paths. AP Theta\* achieves a worst-case complexity per vertex expansion that is constant (like that of $\mathbf { A } ^ { * }$ on grids) rather than linear in the number of cells (like that of Basic Theta\*) by propagating angle ranges when it expands vertices. However, AP Theta\* is more complex than Basic Theta\*, is not as fast and finds slightly longer paths.

We proved the correctness and completeness of Basic Theta\* and AP Theta\* and then compared them against three existing any-angle path-planning algorithms, namely $\mathbf { A } ^ { * }$ with post-smoothed paths (A\* PS), $\mathbf { A } ^ { * }$ on visibility graphs and Field $\mathbf { D } ^ { * }$ (FD\*), the only other version of $\mathbf { A } ^ { * }$ we know of that propagates information along grid edges without constraining the paths to grid edges. Basic Theta\* and AP Theta\* (unlike A\* PS) consider paths not constrained to grid edges during their search and thus can make informed decisions regarding these paths during the search. Basic Theta\* and AP Theta\* (unlike FD\*) take advantage of the fact that true shortest paths have heading changes only at the corners of blocked cells.

$\mathbf { A } ^ { * }$ on visibility graphs finds true shortest paths but is slow. On the other hand, $\mathbf { A } ^ { * }$ on grids finds long paths but is fast. Any-angle path planning lies between these two extremes. Basic Theta\* dominates $\mathbf { A P }$ Theta\*, A\* PS and FD\* in terms of their tradeoffs between runtime and path length. It finds paths that are almost as short as true shortest paths and is almost as fast as $\mathbf { A } ^ { * }$ on grids.

We extended Basic Theta\* to find paths from a given start vertex to all other vertices and to find paths on grids that contain cells with non-uniform traversal costs. The f-value of an expanded vertex of Basic Theta\* (unlike $\mathbf { A } ^ { * }$ on grids) with consistent h-values can be larger than the f-value of one or more of its unexpanded visible neighbors, which means that Basic Theta\* might be able to find shorter paths at an increase in runtime by re-expanding vertices or expanding additional vertices. We thus developed versions of Basic Theta\* that use weighted h-values with weights less than one, that break ties among vertices with the same f-value in the open list in favor of vertices with smaller g-values (when they decide which vertex to expand next), that re-expand vertices whose f-values have decreased, that check for line-of-sight to the parent of a parent, that use key vertices to identify promising parents and that increase the number of visible neighbors.

In the future, we intend to develop a worst-case bound on the path lengths of Basic Theta\* and AP Theta\*, to better understand their properties and to investigate faster versions of AP Theta\* that perform line-of-sight checks in constant time.

## Appendix A. Checking Line-of-Sight

In this appendix, we explain how to perform line-of-sight checks fast. For simplicity, we allow straight lines to pass between diagonally touching blocked cells. Performing a line-of-sight check is similar to determining which points to plot on a raster display when drawing a straight line be tween two points. The plotted points correspond to the cells that the straight line passes through.

```txt
106 LineOfSight(s, s')
107    x₀ := s.x;
108    y₀ := s.y;
109    x₁ := s′.x;
110    y₁ := s′.y;
111    dᵧ := y₁ - y₀;
112    dₓ := x₁ - x₀;
113    f := 0;
114    if dᵧ < 0 then
115    dᵧ := -dᵧ;
116    sᵧ := -1;
117    else
118    sᵧ := 1;
119    if dₓ < 0 then
120    dₓ := -dₓ;
121    sₓ := -1;
122    else
123    sₓ := 1;
124    if dₓ ≥ dᵧ then
125    while x₀ ≠ x₁ do
126    f := f + dᵧ;
127    if f ≥ dₓ then
128    if grid(x₀ + ((sₓ - 1)/2), y₀ + ((sᵧ - 1)/2)) then
129    return false;
130    y₀ := y₀ + sᵧ;
131    f := f - dₓ;
132    if f ≠ 0 AND grid(x₀ + ((sₓ - 1)/2), y₀ + ((sᵧ - 1)/2)) then
133    return false;
134    if dᵧ = 0 AND grid(x₀ + ((sₓ - 1)/2), y₀) AND grid(x₀ + ((sₓ - 1)/2), y₀ - 1) then
135    return false;
136    x₀ := x₀ + sₓ;
137    else
138    while y₀ ≠ y₁ do
139    f := f + dₓ;
140    if f ≥ dᵧ then
141    if grid(x₀ + ((sₓ - 1)/2), y₀ + ((sᵧ - 1)/2)) then
142    return false;
143    x₀ := x₀ + sₓ;
144    f := f - dᵧ;
145    if f ≠ 0 AND grid(x₀ + ((sₓ - 1)/2), y₀ + ((sᵧ - 1)/2)) then
146    return false;
147    if dₓ = 0 AND grid(x₀, y₀ + ((sᵧ - 1)/2)) AND grid(x₀ - 1, y₀ + ((sᵧ - 1)/2)) then
148    return false;
149    y₀ := y₀ + sᵧ;
150    return true;
151 end
```  
Algorithm 6: Line-of-sight algorithm

Thus, two vertices have line-of-sight iff none of the plotted points correspond to blocked cells. This allows Basic Theta\* to perform its line-of-sight checks with the standard Bresenham line-drawing algorithm from computer graphics (Bresenham, 1965), that uses only fast logical and integer operations rather than floating-point operations. Algorithm 6 shows the resulting line-of-sight algorithm, where s.x and s.y are the x and y coordinates of vertex s, respectively, grid represents the grid and $g r i d ( x , y )$ is true iff the corresponding cell is blocked.

![](Daniel2014Theta_figs/1997f8677b9f0382f07ee6a78e787dc29039174d9e9ec5b8e05abb8938abc69b.jpg)  
Figure 25: Parent, blocked cell and boundary vertices

## Appendix B. AP Theta\* Returns Unblocked Paths

In this appendix, we prove that AP Theta\* never returns a blocked path.

Theorem 4. AP Theta\* never returns a blocked path.

Proof. We define a path to be blocked iff at least one vertex on the path does not have line-of-sight to its successor on the path. Thus, a path is blocked iff at least one of its path segments passes through the interior of a blocked cell or passes between two blocked cells that share an edge.

We first prove that AP Theta\* never returns a path with a path segment that passes through the interior of a blocked cell. We prove by contradiction that AP Theta\* cannot assign some parent p to some vertex s such that the path segment from parent p to vertex s passes through the interior of some blocked cell b. Assume otherwise. To simplify the proof, we translate and rotate the grid such that blocked cell b is immediately south-west of the origin $b _ { 0 }$ of the grid and parent p is in quadrant II, as shown in Figure 25. We define the quadrant of a vertex s as follows, where s.x and s.y are the x and y coordinates of vertex s, respectively:

Quadrant I is the north-east quadrant (excluding the x-axis) given by $s . x \geq 0$ and $s . y > 0$

Quadrant II is the north-west quadrant (excluding the y-axis) given by $s . x < 0$ and $s . y \geq 0$

Quadrant III is the south-west quadrant (excluding the x-axis) given by $s . x \leq 0$ and $s . y < 0$

![](Daniel2014Theta_figs/790254445d7305144db28cb684bbf122c02df27d69e89f51573e638172997190.jpg)  
Figure 26: Neighbors of vertex s

Quadrant IV is the south-east quadrant (excluding the y-axis but including the origin $b _ { 0 } )$ given by $s . x > 0$ and $s . y \leq 0$ or s.x = 0 and $s . y = 0$

We refer to the neighbors of vertex s as east(s), northeast(s), north(s), northwest(s), west(s), southwest(s), south(s), southeast(s), as shown in Figure 26.

Assume that there is a light source at vertex p and that light cannot pass through blocked cell $b ,$ which creates a shadow. A vertex s is in the shadow iff the straight line from parent p to vertex s passes through the interior of blocked cell b. We distinguish two parts of the perimeter of this shadow, namely the upper and lower boundary, as shown in Figure 25. We define a boundary vertex to be any vertex not in the shadow that has at least one neighbor (although not necessarily a visible neighbor) in the shadow. The origin $b _ { 0 }$ is not in the shadow but its neighbor $s o u t h ( b _ { 0 } )$ is in the shadow. Thus, the origin $b _ { 0 }$ is a boundary vertex. We consider only the upper boundary without loss of generality. Then, a boundary vertex (to be precise: an upper boundary vertex) is any vertex s with $\Theta ( s , p , b _ { 0 } ) \le 0$ (that is, on or above the upper boundary and thus outside of the shadow) that has at least one neighbor $s ^ { \prime }$ with $\Theta ( s ^ { \prime } , p , b _ { 0 } ) > 0$ (that is, below the upper boundary and thus inside of the shadow). It is easy to see that all boundary vertices are in quadrant IV and form an infinite boundary path $[ b _ { 0 } , b _ { 1 } , \ldots ]$ that starts at the origin $b _ { 0 }$ and repeatedly moves either south or east, that is, $b _ { i + 1 } = s o u t h ( b _ { i } )$ or $b _ { i + 1 } = e a s t ( b _ { i } )$ .

We define a vertex s to be sufficiently constrained iff $\Theta ( s , p , b _ { 0 } ) \le l b ( s )$ for its parent $p .$ Once vertex s is sufficiently constrained, it remains sufficiently constrained since no operation of AP Theta\* can decrease its lower angle bound $l b ( s )$ . We prove in the following that every boundary vertex is sufficiently constrained at the time it is expanded if it is expanded with parent $p .$ Consider any vertex s below the upper boundary (that is, $\Theta ( s , p , b _ { 0 } ) > 0$ and thus $\Theta ( b _ { 0 } , p , s ) < 0 )$ that is a visible neighbor of some boundary vertex $b _ { i }$ . Vertex s cannot have been updated according to Path 1 and been assigned parent p at the time its parent p was expanded since the straight line from parent p to vertex s passes through the interior of a blocked cell and they are therefore not visible neighbors. It cannot have been updated according to Path 2 and been assigned parent $p$ at the time boundary vertex $b _ { i }$ was expanded with parent $p$ because boundary vertex $b _ { i }$ is sufficiently constrained at that time and thus $\Theta ( b _ { i } , p , b _ { 0 } ) \le l b ( b _ { i } )$ , which implies that $\Theta ( b _ { i } , p , s ) = \Theta ( b _ { i } , p , b _ { 0 } ) + \Theta ( b _ { 0 } , p , s ) <$ $\Theta ( b _ { i } , p , b _ { 0 } ) \le l b ( b _ { i } )$ and the condition on Line 60 remains unsatisfied. Consequently, no vertex in the shadow can have parent $p .$

We now prove by induction on the order of the vertex expansions that every boundary vertex is sufficiently constrained at the time it is expanded if it is expanded with parent $p .$ Assume that boundary vertex $b _ { 0 }$ is expanded with parent $p .$ . Then, the condition on Line 81 is satisfied and

Line 83 is executed for blocked cell b at the time boundary vertex $b _ { 0 }$ is expanded with parent $p .$ Boundary vertex $b _ { 0 }$ is sufficiently constrained afterwards since its lower angle bound is set to zero. Now assume that boundary vertex $b _ { i }$ with $i > 0$ is expanded with parent $p .$ . Then, boundary vertex $b _ { i }$ cannot be identical to parent $p$ (since they are in different quadrants) nor to the start vertex (since the start vertex does not have parent $p )$ . Boundary vertex $b _ { i }$ cannot have been updated according to Path 1 and been assigned parent $p$ at the time its parent $p$ was expanded since $p . x < 0$ and $( b _ { i } ) . x > 0$ and they are thus not neighbors. Consequently, boundary vertex $b _ { i }$ must have been updated according to Path 2 and been assigned parent $p$ at the time one of its visible neighbors x was expanded with parent $p .$ . Vertex x must be on or above the upper boundary (that is, $\Theta ( x , p , b _ { 0 } ) \le 0 )$ and cannot be identical to parent $p$ (since they are in different quadrants). We distinguish two cases:

Assume that vertex x is a boundary vertex. It is sufficiently constrained at the time it is expanded with parent $p$ according to the induction assumption (that is, $\Theta ( x , p , b _ { 0 } ) \le l b ( x ) )$ since it is expanded before boundary vertex $b _ { i }$ . Boundary vertex $b _ { i }$ was updated according to Path 2 at the time vertex x was expanded with parent $p .$ . Thus, the condition on Line 60 is satisfied at that time (that is, $l b ( x ) \ \leq \ \Theta ( x , p , b _ { i } ) )$ and thus $l b ( x ) + \Theta ( b _ { i } , p , x ) =$ $l b ( x ) \mathrm { ~ - ~ } \Theta ( x , p , b _ { i } ) \mathrm { ~ \le ~ } 0 .$ Then, the conditions on Lines 88 and 89 are satisfied and Line 90 is executed with $s ^ { \prime } = x$ at the time boundary vertex $b _ { i }$ is expanded with parent $p .$ Boundary vertex $b _ { i }$ is sufficiently constrained afterwards since its lower angle bound is set to max $( l b ( b _ { i } ) , l b ( x ) + \Theta ( b _ { i } , p , x ) )$ and $\Theta ( b _ { i } , p , b _ { 0 } ) \ = \ \Theta ( b _ { i } , p , x ) + \Theta ( x , p , b _ { 0 } ) \ \leq$ $l b ( x ) + \Theta ( b _ { i } , p , x ) \le \operatorname* { m a x } ( l b ( b _ { i } ) , l b ( x ) + \Theta ( b _ { i } , p , x ) )$ .

Assume that vertex x is not a boundary vertex.

Lemma 3. Assume that a vertex s and a boundary vertex $b _ { i }$ are visible neighbors, $c ( p , b _ { i } ) <$ $c ( p , s )$ and $\Theta ( s , p , b _ { i } ) < 0$ . Assume that boundary vertex $b _ { i }$ is sufficiently constrained at the time vertex s is expanded with parent p if boundary vertex $b _ { i }$ has been expanded with parent p at that time. Then, vertex s is sufficiently constrained at the time it is expanded if it is expanded with parent $p .$

Proof. Assume that vertex s is expanded with parent p. Then, $\Theta ( s , p , b _ { 0 } ) = \Theta ( s , p , b _ { i } ) \ +$ $\Theta ( b _ { i } , p , b _ { 0 } ) < 0$ since $\Theta ( s , p , b _ { i } ) < 0$ and $\Theta ( b _ { i } , p , b _ { 0 } ) \le 0$ . We distinguish two cases:

– Assume that boundary vertex $b _ { i }$ is not expanded before vertex s or is expanded with a parent other than parent $p .$ . Then, the conditions on Lines 93 and 94 are satisfied and Line 95 is executed with $s ^ { \prime } = b _ { i }$ at the time vertex s is expanded with parent $p .$ . Vertex s is sufficiently constrained afterwards since its lower angle bound is set to max $( l b ( s ) , \Theta ( s , p , b _ { i } ) )$ and $\Theta ( s , p , b _ { 0 } ) = \Theta ( s , p , b _ { i } ) + \Theta ( b _ { i } , p , b _ { 0 } ) \leq \Theta ( s , p , b _ { i } ) \leq$ max $( l b ( s ) , \Theta ( s , p , b _ { i } ) )$ .

– Assume that boundary vertex $b _ { i }$ is expanded with parent $p$ before vertex s is expanded with parent $p .$ . Boundary vertex $b _ { i }$ is sufficiently constrained at the time vertex s is expanded with parent p according to the premise (that is, $\Theta ( b _ { i } , p , b _ { 0 } ) \le l b ( b _ { i } ) )$ . Furthermore, $l b ( b _ { i } ) \leq 0$ (since no operation of AP Theta\* can make the lower angle bound positive) and thus $l b ( b _ { i } ) + \Theta ( s , p , b _ { i } ) \le 0$ . Then, the conditions on Lines 88 and 89 are satisfied and Line 90 is executed with $s ^ { \prime } = b _ { i }$ at the time vertex s is expanded with parent $p .$ . Vertex s is sufficiently constrained afterwards since its lower angle bound is

$$
\begin{array}{l} \text { set   to } \max (l b (s), l b (b _ {i}) + \Theta (s, p, b _ {i})) \text { and } \Theta (s, p, b _ {0}) = \Theta (s, p, b _ {i}) + \Theta (b _ {i}, p, b _ {0}) \leq \\ l b (b _ {i}) + \Theta (s, p, b _ {i}) \leq \max (l b (s), l b (b _ {i}) + \Theta (s, p, b _ {i})). \end{array}
$$

Boundary vertex $b _ { i }$ is either immediately south or east of boundary vertex $b _ { i - 1 }$ since the boundary path moves only south or east. We distinguish three subcases:

– Assume that parent p is on the x-axis in quadrant II. Then, the boundary path is along the x-axis. Vertices wes $t ( b _ { i } )$ and $e a s t ( b _ { i } )$ are boundary vertices, and vertices southwest $\left( b _ { i } \right)$ , south $\mathbf { \nabla } _ { \cdot } ( b _ { i } )$ , and $s o u t h e a s t ( b _ { i } )$ are below the upper boundary. Thus, vertex x is identical to one of vertices northwes $t ( b _ { i } )$ , north(b<sub>i</sub>) or $n o r t h e a s t ( b _ { i } )$ . In all cases, there is a boundary vertex $b _ { j }$ immediately south of vertex x. If vertices $x$ and $b _ { j }$ were not visible neighbors, then there would be blocked cells immediately southwest and south-east of vertex x and vertices x and $b _ { i }$ could thus not be visible neighbors. Thus, vertices $x$ and $b _ { j }$ are visible neighbors. Furthermore, boundary vertex $b _ { j }$ is immediately south of vertex x and thus $c ( p , b _ { j } ) < c ( p , x )$ and $\Theta ( x , p , b _ { j } ) < 0$ . Finally, boundary vertex $b _ { j }$ is sufficiently constrained according to the induction assumption at the time boundary vertex $b _ { i }$ is expanded with parent $p$ if boundary vertex $b _ { j }$ has been expanded with parent $p$ at that time. Thus, vertex x is sufficiently constrained at the time it is expanded with parent p according to Lemma 3 (that is, $\Theta ( x , p , b _ { 0 } ) \le l b ( x ) )$ . Consequently, the conditions on Lines 88 and 89 are satisfied (for the reason given before) and Line 90 is executed with $s ^ { \prime } = x$ at the time boundary vertex $b _ { i }$ is expanded with parent $p .$ . Boundary vertex $b _ { i }$ is sufficiently constrained afterwards since its lower angle bound is set to max $( l b ( b _ { i } ) , l b ( x ) + \Theta ( b _ { i } , p , x ) )$ and $\Theta ( b _ { i } , p , b _ { 0 } ) = \Theta ( b _ { i } , p , x ) + \Theta ( x , p , b _ { 0 } ) \leq$ $l b ( x ) + \Theta ( b _ { i } , p , x ) \le \operatorname* { m a x } ( l b ( b _ { i } ) , l b ( x ) + \Theta ( b _ { i } , p , x ) )$

– Assume that parent $p$ is not on the x-axis in quadrant II and that boundary vertex $b _ { i }$ is immediately east of boundary vertex $b _ { i - 1 }$ and thus $c ( p , b _ { i - 1 } ) ~ < ~ c ( p , b _ { i } )$ and $\Theta ( b _ { i } , p , b _ { i - 1 } ) < 0$ . Furthermore, boundary vertex $b _ { i - 1 }$ is sufficiently constrained according to the induction assumption at the time boundary vertex $b _ { i }$ is expanded with parent $p$ if boundary vertex $b _ { i - 1 }$ has been expanded with parent $p$ at that time. If boundary vertices $b _ { i - 1 }$ and $b _ { i }$ are visible neighbors, then boundary vertex $b _ { i }$ is sufficiently constrained at the time it is expanded with parent $p$ according to Lemma 3. If boundary vertices $b _ { i - 1 }$ and $b _ { i }$ are not visible neighbors, then there must be blocked cells immediately north-west and south-west of boundary vertex $b _ { i }$ . Then, Line 81 is satisfied and Line 83 is executed for the blocked cell immediately south-west of boundary vertex $b _ { i }$ at the time boundary vertex $b _ { i }$ is expanded with parent $p .$ Boundary vertex $b _ { i }$ is sufficiently constrained afterwards since its lower angle bound is set to zero.

– Assume that parent $p$ is not on the x-axis in quadrant II and that boundary vertex $b _ { i }$ is immediately south of boundary vertex $b _ { i - 1 }$

Lemma 4. Assume that a vertex s in quadrant IV is on or above the upper boundary. Then, vertex s is a boundary vertex iff the vertex immediately south-west of vertex s is below the upper boundary.

Proof. If the vertex $s ^ { \prime }$ immediately south-west of vertex s is below the upper boundary, then vertex s is a boundary vertex by definition. On the other hand, if vertex $s ^ { \prime }$ is on or above the upper boundary (that is, $\Theta ( s ^ { \prime } , p , b _ { 0 } ) \le 0 )$ , then vertex s is not a boundary vertex because every neighbor of it is on or above the upper boundary. The neighbors of vertex s are

$$
\begin{array}{c} e a s t (s), n o r t h e a s t (s), n o r t h (s), n o r t h w e s t (s), \\ w e s t (s), s o u t h w e s t (s), s o u t h (s) \text {and} s o u t h e a s t (s). \end{array}
$$

or, equivalently,

$$
\begin{array}{c} e a s t (e a s t (n o r t h (s ^ {\prime}))), e a s t (e a s t (n o r t h (n o r t h (s ^ {\prime})))), e a s t (n o r t h (n o r t h (s ^ {\prime}))), \\ n o r t h (n o r t h (s ^ {\prime})), n o r t h (s ^ {\prime}), s ^ {\prime}, e a s t (s ^ {\prime}) \text {and} e a s t (e a s t (s ^ {\prime})). \end{array}
$$

Thus, every neighbor $s ^ { \prime \prime }$ of vertex s can be reached from vertex $s ^ { \prime }$ by repeatedly moving either north or east and thus $\Theta ( s ^ { \prime \prime } , p , s ^ { \prime } ) ~ \le ~ 0$ . Consequently, $\Theta ( s ^ { \prime \prime } , p , b _ { 0 } ) \ =$ $\Theta ( s ^ { \prime \prime } , p , s ^ { \prime } ) + \Theta ( s ^ { \prime } , p , b _ { 0 } ) \le 0$ and thus every neighbor $s ^ { \prime \prime }$ of vertex s is on or above the upper boundary. □

We distinguish two subcases:

Assume that boundary vertex $b _ { i + 1 }$ is immediately east of boundary vertex $b _ { i }$ . Vertices $n o r t h ( b _ { i } )$ and $e a s t ( b _ { i } )$ are boundary vertices. Vertices $w e s t ( b _ { i } )$ southwest $( b _ { i } )$ and $s o u t h ( b _ { i } )$ are south-west of boundary vertices $b _ { i - 1 } , b _ { i }$ and $b _ { i + 1 }$ respectively, and thus below the upper boundary according to Lemma 4. Vertices northwes $\div ( b _ { i } )$ and $s o u t h e a s t ( b _ { i } )$ are either boundary vertices or south-west of boundary vertices $b _ { i - 2 }$ and $b _ { i + 2 }$ , respectively, and then below the upper boundary according to Lemma 4. Thus, vertex x is identical to vertex northwest $\cdot ( b _ { i } )$

Assume that boundary vertex $b _ { i + 1 }$ is immediately south of boundary vertex $b _ { i }$ Vertices nor $t h ( b _ { i } )$ and $s o u t h ( b _ { i } )$ are boundary vertices. Vertices west $\cdot ( b _ { i } )$ and southwest $( b _ { i } )$ are south-west of boundary vertices $b _ { i - 1 }$ and $b _ { i }$ , respectively, and thus below the upper boundary according to Lemma 4. Vertex $n o r t h w e s t ( b _ { i } )$ is either a boundary vertex or south-west of boundary vertex $b _ { i - 2 }$ and then below the upper boundary according to Lemma 4. Thus, vertex x is identical to one of vertices northeast $\cdot ( b _ { i } )$ , ea $s t ( b _ { i } )$ or southeast(b ).

In all cases, vertex x is immediately east of some boundary vertex $b _ { j }$ and thus $c ( p , b _ { j } ) <$ $c ( p , x )$ and $\Theta ( x , p , b _ { j } ) < 0$ . If vertices x and $b _ { j }$ were not visible neighbors, then there would be blocked cells immediately north-west and south-west of vertex x and vertices x and $b _ { i }$ could not be visible neighbors. Thus, vertices x and $b _ { j }$ are visible neighbors. Furthermore, boundary vertex $b _ { j }$ is sufficiently constrained according to the induction assumption at the time boundary vertex $b _ { i }$ is expanded with parent $p$ if boundary vertex $b _ { j }$ has been expanded with parent $p$ at that time. Thus, vertex x is sufficiently constrained at the time it is expanded with parent $p$ according to Lemma 3 (that ${ \mathrm { i s } } ,$ $\Theta ( x , p , b _ { 0 } ) \le l b ( x ) \rangle$ ). Consequently, the conditions on Lines 88 and 89 are satisfied (for the reason given before) and Line 90 is executed with $s ^ { \prime } = x$ at the time boundary vertex $b _ { i }$ is expanded with parent $p .$ Boundary vertex $b _ { i }$ is sufficiently constrained afterwards since its lower angle bound is set to max $( l b ( b _ { i } ) , l b ( x ) + \Theta ( b _ { i } , p , x ) )$ and $\Theta ( b _ { i } , p , b _ { 0 } ) =$ $\Theta ( b _ { i } , p , x ) + \Theta ( x , p , b _ { 0 } ) \leq l b ( x ) + \Theta ( b _ { i } , p , x ) \leq \operatorname* { m a x } ( l b ( b _ { i } ) , l b ( x ) + \Theta ( b _ { i } , p , x ) )$

This concludes the proof that every boundary vertex is sufficiently constrained at the time it is expanded if it is expanded with parent $p$ and thus also the proof that AP Theta\* never returns a path with a path segment that passes through the interior of a blocked cell.

We now prove that AP Theta\* never returns a path with a path segment that passes between two blocked cells that share an edge. We prove by contradiction that AP Theta\* cannot assign some parent p to some vertex s such that the path segment from parent $p$ to vertex s passes between two blocked cells that share an edge. Assume otherwise and consider the first time AP Theta\* assigns some parent $p$ to some vertex s such that the path segment from parent $p$ to vertex s passes between two blocked cells that share an edge. The path segment must be either horizontal or vertical. Vertex s cannot have been updated according to Path 1 and been assigned parent $p$ at the time its parent $p$ was expanded since then the straight line from parent $p$ to vertex s passes through the interior of a blocked cell and they are therefore not visible neighbors. It cannot have been updated according to Path 2 and been assigned parent $p$ at the time some visible neighbor $s ^ { \prime }$ was expanded with parent $p$ since then either a) neighbor $s ^ { \prime }$ would not be colinear with vertices $p$ and s and the straight line from parent $p$ to vertex $s ^ { \prime }$ would thus pass through the interior of a blocked cell or b) neighbor $s ^ { \prime }$ would be colinear with vertices $p$ and s and the straight line from parent $p$ to vertex $s ^ { \prime }$ would pass between two blocked cells that share an edge, which is a contradiction of the assumption. This concludes the proof that $\mathbf { A P }$ Theta\* never returns a path with a path segment that passes between two blocked cells that share an edge.

Thus, $\mathbf { A P }$ Theta\* never returns a blocked path.

## Appendix C. Acknowledgments

This article is an extension of an earlier publication (Nash et al., 2007) and contains additional expositions, examples and proofs. We thank Vadim Bulitko from the University of Alberta for making maps from the real-time game Baldur’s Gate II available to us. Our research was done while Ariel Felner spent his sabbatical at the University of Southern California, visiting Sven Koenig. This research has been partly supported by a U.S. Army Research Laboratory (ARL) and U.S. Army Research Office (ARO) award to Sven Koenig under grant W911NF-08-1-0468, by a Office of Naval Research (ONR) award to Sven Koenig under grant N00014-09-1-1031, by a National Science Foundation (NSF) award to Sven Koenig under grant 0413196 and by an Israeli Science Foundation (ISF) award to Ariel Felner under grants 728/06 and 305/09. Alex Nash was funded by the Northrop Grumman Corporation. The views and conclusions contained in this document are those of the authors and should not be interpreted as representing the official policies, either expressed or implied, of the sponsoring organizations, agencies, companies or the U.S. government.

## References

Aurenhammer, F. (1991). Voronoi diagrams—a survey of a fundamental geometric data structure. ACM Computing Surveys, 23(3), 345–405.

Botea, A., M¨uller, M., & Schaeffer, J. (2004). Near optimal hierarchical path-finding. Journal of Game Development, 1(1), 1–22.

Bresenham, J. (1965). Algorithm for computer control of a digital plotter. IBM Systems Journal, 4(1), 25–30.

Bulitko, V., Sturtevant, N., & Kazakevich, M. (2005). Speeding up learning in real-time search via automatic state abstraction. In Proceedings of the AAAI Conference on Artificial Intelligence, pp. 1349–1354.

Choset, H., Lynch, K., Hutchinson, S., Kantor, G., Burgard, W., Kavraki, L., & Thrun, S. (2005). Principles of Robot Motion: Theory, Algorithms, and Implementations. MIT Press.

Deloura, M. (2000). Game Programming Gems. Charles River Media.

Ferguson, D., & Stentz, A. (2006). Using interpolation to improve path planning: The Field D\* algorithm. Journal of Field Robotics, 23(2), 79–101.

Foley, J., van Dam, A., Feiner, S., & Hughes, J. (1992). Computer Graphics: Principles and Practice. Addison-Wesley.

Hart, P., Nilsson, N., & Raphael, B. (1968). A formal basis for the heuristic determination of minimum cost paths. IEEE Transactions on Systems Science and Cybernetics, SCC-4(2), 100–107.

Kavraki, L., Svestka, P., Latombe, J., & Overmars, M. (1996). Probabilistic roadmaps for path planning in high-dimensional configuration spaces. IEEE Transactions on Robotics and Automation, 12(4), 566–580.

Koenig, S., & Likhachev, M. (2002). D\* Lite. In Proceedings of the AAAI Conference on Artificial Intelligence, pp. 476–483.

LaValle, S., & Kuffner, J. (2001). Rapidly-exploring random trees: Progress and prospects. In Donald, B., Lynch, K., & Rus, D. (Eds.), Algorithmic and Computational Robotics: New Directions, pp. 293–308. A K Peters.

Lee, D.-T. (1978). Proximity and reachability in the plane. Ph.D. thesis, University of Illinois at Urbana-Champaign.

Liu, Y.-H., & Arimoto, S. (1992). Path planning using a tangent graph for mobile robots among polygonal and curved obstacles. International Journal Robotics Research, 11(4), 376–382.

Lozano-P´erez, T., & Wesley, M. (1979). An algorithm for planning collision-free paths among polyhedral obstacles. Communication of the ACM, 22, 560–570.

Mitchell, J., & Papadimitriou, C. (1991). The weighted region problem: Finding shortest paths through a weighted planar subdivision. Journal of the ACM, 38(1), 18–73.

Murphy, R. (2000). Introduction to AI Robotics. MIT Press.

Nash, A., Daniel, K., Koenig, S., & Felner, A. (2007). Theta\*: Any-angle path planning on grids. In Proceedings of the AAAI Conference on Artificial Intelligence, pp. 1177–1183.

Nash, A., Koenig, S., & Likhachev, M. (2009). Incremental Phi\*: Incremental any-angle path planning on grids. In Proceedings of the International Joint Conference on Aritificial Intelligence, pp. 1824–1830.

Patel, A. (2000). Amit’s Game Programming Information. available online at http://theory.stanford.edu/ amitp/GameProgramming/MapRepresentations.html.

Pearl, J. (1984). Heuristics: Intelligent Search Strategies for Computer Problem Solving. Addison-Wesley.

Pohl, I. (1973). The avoidance of (relative) catastrophe, heuristic competence, genuine dynamic weighting and computational issues in heuristic problem solving. In Proceedings of the International Joint Conference on Artificial Intelligence, pp. 12–17.

Rabin, S. (2002). AI Game Programming Wisdom. Charles River Media.

Rabin, S. (2004). AI Game Programming Wisdom 2. Charles River Media.

Thorpe, C. (1984). Path relaxation: Path planning for a mobile robot. In Proceedings of the AAAI Conference on Artificial Intelligence, pp. 318–321.

Tozour, P. (2004). Search space representations. In Rabin, S. (Ed.), AI Game Programming Wisdom 2, pp. 85–102. Charles River Media.

Yahja, A., Stentz, A., Singh, S., & Brumitt, B. (1998). Framed-quadtree path planning for mobile robots operating in sparse environments. In Proceedings of the International Conference on Robotics and Automation, pp. 650–655.

Yap, P. (2002). Grid-based path-finding. In Proceedings of the Canadian Conference on Artificial Intelligence, pp. 44–55.