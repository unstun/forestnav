---
citation_key: Rana2023SayPlan
arxiv_id: 2307.06135
arxiv_url: "https://arxiv.org/abs/2307.06135"
title: "SayPlan: Grounding Large Language Models using 3D Scene Graphs for Scalable Robot Task Planning"
authors_short: "Krishan Rana et al."
year: 2023
direction_tag: A_path_smoothing
source: mineru-vlm
converter: mineru-open-api
model: vlm
converted_at: 2026-06-25T09:32:02Z
origin: ai+web
reviewed: false
---

# SayPlan: Grounding Large Language Models using 3D Scene Graphs for Scalable Robot Task Planning

Krishan Rana<sup>†1</sup>, Jesse Haviland<sup>∗1,2</sup>, Sourav Garg<sup>∗3</sup>, Jad Abou-Chakra<sup>∗1</sup>, Ian Reid<sup>3</sup>, Niko Sunderhauf¨ <sup>1</sup>

<sup>1</sup>QUT Centre for Robotics, Queensland University of Technology

<sup>2</sup>CSIRO Data61 Robotics and Autonomous Systems Group

<sup>3</sup>University of Adelaide

<sup>∗</sup>Equal Contribution

<sup>†</sup>ranak@qut.edu.au

## Abstract:

Large language models (LLMs) have demonstrated impressive results in developing generalist planning agents for diverse tasks. However, grounding these plans in expansive, multi-floor, and multi-room environments presents a significant challenge for robotics. We introduce SayPlan, a scalable approach to LLM-based, large-scale task planning for robotics using 3D scene graph (3DSG) representations. To ensure the scalability of our approach, we: (1) exploit the hierarchical nature of 3DSGs to allow LLMs to conduct a semantic search for task-relevant subgraphs from a smaller, collapsed representation of the full graph; (2) reduce the planning horizon for the LLM by integrating a classical path planner and (3) introduce an iterative replanning pipeline that refines the initial plan using feedback from a scene graph simulator, correcting infeasible actions and avoiding planning failures. We evaluate our approach on two large-scale environments spanning up to 3 floors and 36 rooms with 140 assets and objects and show that our approach is capable of grounding large-scale, long-horizon task plans from abstract, and natural language instruction for a mobile manipulator robot to execute. We provide real robot video demonstrations on our project page sayplan.github.io.

## 1 Introduction

“Make me a coffee and place it on my desk” – The successful execution of such a seemingly straightforward command remains a daunting task for today’s robots. The associated challenges permeate every aspect of robotics, encompassing navigation, perception, manipulation as well as high-level task planning. Recent advances in Large Language Models (LLMs) [1, 2, 3] have led to significant progress in incorporating common sense knowledge for robotics [4, 5, 6]. This enables robots to plan complex strategies for a diverse range of tasks that require a substantial amount of background knowledge and semantic comprehension.

For LLMs to be effective planners in robotics, they must be grounded in reality, that is, they must adhere to the constraints presented by the physical environment in which the robot operates, including the available affordances, relevant predicates, and the impact of actions on the current state. Furthermore, in expansive environments, the robot must additionally understand where it is, locate items of interest, as well comprehend the topological arrangement of the environment in order to plan across the necessary regions. To address this, recent works have explored the utilization of vision-based value functions [4], object detectors [7, 8], or Planning Domain Definition Language (PDDL) descriptions of a scene [9, 10] to ground the output of the LLM-based planner. However, these efforts are primarily confined to small-scale environments, typically single rooms with pre-encoded information on all the existing assets and objects present. The challenge lies in scaling these models. As the environment’s complexity and dimensions expand, and as more rooms and entities enter the scene, pre-encoding all the necessary information within the LLM’s context becomes increasingly infeasible.

![](Rana2023SayPlan_figs/2681bae62cdf701701505eededf3a67b6b87dbaf662454d33ca889f42f05e54a.jpg)  
Figure 1: SayPlan Overview (top). SayPlan operates across two stages to ensure scalability: (left) Given a collapsed 3D scene graph and a task instruction, semantic search is conducted by the LLM to identify a suitable subgraph that contains the required items to solve the task; (right) The explored subgraph is then used by the LLM to generate a high-level task plan, where a classical path planner completes the navigational component of the plan; finally, the plan goes through an iterative replanning process with feedback from a scene graph simulator until an executable plan is identified. Numbers on the top-left corners represent the flow of operations.

To this end, we present a scalable approach to ground LLM-based task planners across environments spanning multiple rooms and floors. We achieve this by exploiting the growing body of 3D scene graph (3DSG) research [11, 12, 13, 14, 15, 16]. 3DSGs capture a rich topological and hierarchicallyorganised semantic graph representation of an environment with the versatility to encode the necessary information required for task planning including object state, predicates, affordances and attributes using natural language – suitable for parsing by an LLM. We can leverage a JSON representation of this graph as input to a pre-trained LLM, however, to ensure the scalability of the plans to expansive scenes, we present three key innovations.

Firstly, we present a mechanism that enables the LLM to conduct a semantic search for a taskrelevant subgraph G<sup>0</sup> by manipulating the nodes of a ‘collapsed’ 3DSG, which exposes only the top level of the full graph G, via expand and contract API function calls – thus making it feasible to plan over increasingly large-scale environments. In doing so, the LLM maintains focus on a relatively small, informative subgraph, G<sup>0</sup> during planning, without exceeding its token limit. Secondly, as the horizon of the task plans across such environments tends to grow with the complexity and range of the given task instructions, there is an increasing tendency for the LLM to hallucinate or produce infeasible action sequences [17, 18, 7]. We counter this by firstly relaxing the need for the LLM to generate the navigational component of the plan, and instead leverage an existing optimal path planner such as Dijkstra [19] to connect high-level nodes generated by the LLM. Finally, to ensure the feasibility of the proposed plan, we introduce an iterative replanning pipeline that verifies and refines the initial plan using feedback from a scene graph simulator in order to correct for any unexecutable actions, e.g., missing to open the fridge before putting something into it – thus avoiding planning failures due to inconsistencies, hallucinations, or violations of the physical constraints and predicates imposed by the environment.

Our approach SayPlan ensures feasible and grounded plan generation for a mobile manipulator robot operating in large-scale environments spanning multiple floors and rooms. We evaluate our framework across a range of 90 tasks organised into four levels of difficulty. These include semantic search tasks such as (“Find me something non-vegetarian.”) to interactive, long-horizon tasks with ambiguous multi-room objectives that require a significant level of common-sense reasoning (“Let’s play a prank on Niko”). These tasks are assessed in two expansive environments, including a large office floor spanning 37 rooms and 150 interactable assets and objects, and a three-storey house with 28 rooms and 112 objects. Our experiments validate SayPlan’s ability to scale task planning to large-scale environments while conserving a low token footprint. By introducing a semantic search pipeline, we can reduce full large-scale scene representations by up to 82.1% for LLM parsing and our iterative replanning pipeline allows for near-perfect executability rates, suitable for execution on a real mobile manipulator robot.<sup>1</sup>

## 2 Related Work

Task planning in robotics aims to generate a sequence of high-level actions to achieve a goal within an environment. Conventional methods employ domain-specific languages such as PDDL [20, 21, 22] and ASP [23] together with semantic parsing [24, 25], search techniques [26, 27] and complex heuristics [28] to arrive at a solution. These methods, however, lack both the scalability to large environments as well as the task generality required when operating in the real world. Hierarchical and reinforcement learning-based alternatives [29, 30], [31] face challenges with data demands and scalability. Our work leverages the in-context learning capabilities of LLMs to generate task plans across 3D scene graphs. Tasks, in this case, can be naturally expressed using language, with the internet scale training of LLMs providing the desired knowledge for task generality, while 3D scene graphs provide the grounding necessary for large-scale environment operation. This allows for a general and scalable framework when compared to traditional non-LLM-based alternatives.

Task planning with LLMs, that is, translating natural language prompts into task plans for robotics, is an emergent trend in the field. Earlier studies have effectively leveraged pre-trained LLMs’ incontext learning abilities to generate actionable plans for embodied agents [4, 10, 9, 8, 32, 7, 33]. A key challenge for robotics is grounding these plans within the operational environment of the robot. Prior works have explored the use of object detectors [8, 7], PDDL environment representations [10, 9, 34] or value functions [4] to achieve this grounding, however, they are predominantly constrained to single-room environments, and scale poorly with the number of objects in a scene which limits their ability to plan over multi-room or multi-floor environments. In this work, we explore the use of 3D scene graphs and the ability of LLMs to generate plans over large-scale scenes by exploiting the inherent hierarchical and semantic nature of these representations.

Integrating external knowledge in LLMs has been a growing line of research combining language models with external tools to improve the reliability of their outputs. In such cases, external modules are used to provide feedback or extra information to the LLM to guide its output generation. This is achieved either through API calls to external tools [35, 36] or as textual feedback from the operating environment [37, 8]. More closely related to our work, CLAIRIFY [38] iteratively leverage compiler error feedback to re-prompt an LLM to generate syntactically valid code. Building on these ideas, we propose an iterative plan verification process with feedback from a scene graph-based simulator to ensure all generated plans adhere to the constraints and predicates captured by the preconstructed scene graph. This ensures the direct executability of the plan on a mobile manipulator robot, operating in the corresponding real-world environment.

## 3 SayPlan

## 3.1 Problem Formulation

We aim to address the challenge of long-range task planning for an autonomous agent, such as a mobile manipulator robot, in a large-scale environment based on natural language instructions. This requires the robot to comprehend abstract and ambiguous instructions, understand the scene and generate task plans involving both navigation and manipulation of a mobile robot within an environment. Existing approaches lack the ability to reason over scenes spanning multiple floors and rooms. Our focus is on integrating large-scale scenes into planning agents based on Language Models (LLMs) and solving the scalability challenge. We aim to tackle two key problems: 1) representing large-scale scenes within LLM token limitations, and 2) mitigating LLM hallucinations and erroneous outputs when generating long-horizon plans in large-scale environments.

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 1: SayPlan

Given: scene graph simulator $\psi$, classical path planner $\phi$, large language model $LLM$

Inputs: prompt $\mathcal{P}$, scene graph $\mathcal{G}$, instruction $\mathcal{I}$

1: $\mathcal{G}' \leftarrow \text{collapse}_{\psi}(\mathcal{G})$ ▷ collapse scene graph
Stage 1: Semantic Search ▷ search scene graph for all relevant items

2: while command != “terminate” do

3:    command, node_name ← $LLM(\mathcal{P}, \mathcal{G}', \mathcal{I})$

4:    if command == “expand” then

5:    $\mathcal{G}' \leftarrow \text{expand}_{\psi}(\text{node\_name})$ ▷ expand node to reveal objects and assets

6:    else if command == “contract” then

7:    $\mathcal{G}' \leftarrow \text{contract}_{\psi}(\text{node\_name})$ ▷ contract node if nothing relevant found
Stage 2: Causal Planning ▷ generate a feasible plan

8: feedback = “”
9: while feedback != “success” do

10:    plan ← $LLM(\mathcal{P}, \mathcal{G}', I, \text{feedback})$ ▷ high level plan
11:    full_plan ← $\phi(\text{plan}, \mathcal{G}')$ ▷ compute optimal navigational path between nodes
12:    feedback ← verify_plan$_{\psi}$(full_plan) ▷ forward simulate the full plan
13: return full_plan ▷ executable plan
</div>

## 3.2 Preliminaries

Here, we describe the 3D scene graph representation of an environment and the scene graph simulator API which we leverage throughout our approach.

Scene Representation: 3D Scene Graphs (3DSG) [11, 12, 14] have recently emerged as an actionable world representation for robots [13, 15, 16, 39, 40, 41], which hierarchically abstract the environment at multiple levels through spatial semantics and object relationships while capturing relevant states, affordances and predicates of the entities present in the environment. Formally, a 3DSG is a hierarchical multigraph $\mathcal { G } = ( V , E )$ in which the set of vertices $\check { V }$ comprises $V _ { 1 } \cup { \dot { V } } _ { 2 } \cup . . . \cup V _ { K }$ , with

![](Rana2023SayPlan_figs/4578041451a1253675f5eb03732b27129b6074b6a836592bc3bf101950e3dee6.jpg)  
Figure 2: Hierarchical Structure of a 3D Scene Graph. This graph consists of 4 levels. Notes that the room nodes are connected to one another via sequences of pose nodes which capture the topological arrangement of a scene.

each $V _ { k }$ signifying the set of vertices at a particular level of the hierarchy $k .$ Edges stemming from a vertex $v \in V _ { k }$ may only terminate in $V _ { k - 1 } \cup V _ { k } \cup V _ { k + 1 }$ , i.e. edges connect nodes within the same level, or one level higher or lower.

We assume a pre-constructed 3DSG representation of a large-scale environment generated using existing techniques [15, 13, 11]. The entire 3DSG can be represented as a NetworkX Graph object [42] and text-serialised into a JSON data format that can be parsed directly by a pretrained LLM. An example of a single asset node from the 3DSG is represented as: {name: coffee\_machine, type: asset, location: kitchen, affordances: [turn\_on, turn\_off, release], state: off, attributes: [red, automatic], position: [2.34, 0.45, 2.23]} with edges between nodes captured as {kitchen↔coffee machine}. The 3DSG is organized in a hierarchical manner with four primary levels: floors, rooms, assets, and objects as shown in Figure 2. The top level contains floors, each of which branches out to several rooms. These rooms are interconnected through pose nodes to represent the environment’s topological structure. Within each room, we find assets (immovable entities) and objects (movable entities). Both asset and object nodes encode particulars including state, affordances, additional attributes such as colour or weight, and 3D pose. The graph also incorporates a dynamic agent node, denoting a robot’s location within the scene. Note that this hierarchy is scalable and node levels can be adapted to capture even larger environments e.g. campuses and buildings

Scene Graph Simulator ψ refers to a set of API calls for manipulating and operating over JSON formatted 3DSGs, using the following functions: 1) collapse(G): Given a full 3DSG, this function returns an updated scene graph that exposes only the highest level within the 3DSG hierarchy e.g. floor nodes. 2) expand(node name): Returns an updated 3DSG that reveals all the nodes connected to node name in the level below. 3) contract(node name): Returns an updated 3DSG that hides all the nodes connected to node name in the level below. 4) verify\_plan(plan): Forward simulates the generated plan at the abstract graph level captured by the 3DSG to check if each action adheres to the environment’s predicates, states and affordances. Returns textual feedback e.g. “cannot pick up banana” if the fridge containing the banana is closed.

## 3.3 Approach

We present a scalable framework for grounding the generalist task planning capabilities of pretrained LLMs in large-scale environments spanning multiple floors and rooms using 3DSG representations. Given a 3DSG G and a task instruction I defined in natural language, we can view our framework SayPlan as a high-level task planner π(a|I, G), capable of generating long-horizon plans a grounded in the environment within which a mobile manipulator robot operates. This plan is then fed to a low-level visually grounded motion planner for real-world execution. To ensure the scalability of SayPlan, two stages are introduced: Semantic Search and Iterative Replanning which we detail below. An overview of the SayPlan pipeline is illustrated in Figure 1 with the corresponding pseudo-code given in Algorithm 1.

Semantic Search: When planning over 3DSGs using LLMs we take note of two key observations: 1) A 3DSG of a large-scale environment can grow infinitely with the number of rooms, assets and objects it contains, making it impractical to pass as input to an LLM due to token limits and 2) only a subset of the full 3DSG G is required to solve any given task $\mathrm { e . g . }$ we don’t need to know about the toothpaste in the bathroom when making a cup of coffee. To this end, the Semantic Search stage seeks to identify this smaller, task-specific subgraph $\mathcal { G } ^ { \prime }$ from the full 3DSG which only contains the entities in the environment required to solve the given task instruction. To identify $\overline { { { g } ^ { \prime } } }$ from a full 3DSG, we exploit the semantic hierarchy of these representations and the reasoning capabilities of LLMs. We firstly collapse $\mathcal { G }$ to expose only its top level e.g. the floor nodes, reducing the 3DSG initial token representation by ≈ 80%. The LLM manipulates this collapsed graph via expand and contract API calls in order to identify the desired subgraph for the task based on the given instruction I. This is achieved using in-context learning over a set of input-out examples (see Appendix ${ \mathrm { J } } ) ,$ and utilising chain-of-thought prompting to guide the LLM in identifying which nodes to manipulate. The chosen API call and node are executed within the scene graph simulator, and the updated 3DSG is passed back to the LLM for further exploration. If an expanded node is found to contain irrelevant entities for the task, the LLM contracts it to manage token limitations and maintain a task-specific subgraph (see Figure 3). To avoid expanding already-contracted nodes, we maintain a list of previously expanded nodes, passed as an additional Memory input to the LLM, facilitating a Markovian decision-making process and allowing SayPlan to scale to extensive search sequences without the overhead of maintaining the full interaction history [5]. The LLM autonomously proceeds to the planning phase once all necessary assets and objects are identified in the current subgraph $\mathcal { G } ^ { \prime }$ . An example of the LLM-scene graph interaction during Semantic Search is provided in Appendix K.

Iterative Replanning: Given the identified subgraph $\mathcal { G } ^ { \prime }$ and the same task instruction I from above, the LLM enters the planning stage of the pipeline. Here the LLM is tasked with generating a sequence of node-level navigational (goto(pose2)) and manipulation (pickup(coffee\_mug)) actions that satisfy the given task instruction. LLMs, however, are not perfect planning agents and tend to hallucinate or produce erroneous outputs [43, 9]. This is further exacerbated when planning over large-scale environments or long-horizon tasks. We facilitate the generation of task plans by the LLM via two mechanisms. First, we shorten the LLM’s planning horizon by delegating pose-level path planning to an optimal path planner, such as Dijkstra. For example, a typical plan output such as [goto(meeting\_room), goto(pose13), goto(pose14), goto(pose8), ..., goto(kitchen), access(fridge), open(fridge)] is simplified to [goto(meeting\_room), goto(kitchen), access(fridge), open(fridge)]. The path planner handles finding the optimal route between high-level locations, allowing the LLM to focus on essential manipulation components of the task. Secondly, we build on the self-reflection capabilities of LLMs [17] to iteratively correct their generated plans using textual, task-agnostic feedback from a scene graph simulator which evaluates if the generated plan complies with the scene graph’s predicates, state, and affordances. For instance, a pick(banana) action might fail if the robot is already holding something, if it is not in the correct location or if the fridge was not opened beforehand. Such failures are transformed into textual feedback (e.g., ”cannot pick banana”), appended to the LLM’s input, and used to generate an updated, executable plan. This iterative process, involving planning, validation, and feedback integration, continues until a feasible plan is obtained. The validated plan is then passed to a low-level motion planner for robotic execution. An example of the LLM-scene graph interaction during iterative replanning is provided in Appendix L. Specific implementation details are provided in Appendix A.

## 4 Experimental Setup

We design our experiments to evaluate the 3D scene graph reasoning capabilities of LLMs with a particular focus on high-level task planning pertaining to a mobile manipulator robot. The plans adhere to a particular embodiment consisting of a 7-degree-of-freedom robot arm with a two-fingered gripper attached to a mobile base. We use two large-scale environments, shown in Figure 4, which exhibit multiple rooms and multiple floors which the LLM agent has to plan across. To better ablate and showcase the capabilities of SayPlan, we decouple its semantic search ability from the overall causal planning capabilities using the following two evaluation settings as shown in Appendix C:

Semantic Search: Here, we focus on queries which test the semantic search capabilities of an LLM provided with a collapsed 3D scene graph. This requires the LLM to reason over the room and floor node names and their corresponding attributes in order to aid its search for the relevant assets and objects required to solve the given task instruction. We evaluate against a human baseline to understand how the semantic search capabilities of an LLM compare to a human’s thought process. Furthermore, to gain a better understanding of the impact different LLM models have on this graphbased reasoning, we additionally compare against a variant of SayPlan using GPT-3.5.

Causal Planning: In this experiment, we evaluate the ability of SayPlan to generate feasible plans to solve a given natural language instruction. The evaluation metrics are divided into two components: 1) Correctness, which primarily validates the overall goal of the plan and its alignment to what a human would do to solve the task and 2) Executability, which evaluates the alignment of the plan to the constraints of the scene graph environment and its ability to be executed by a mobile manipulator robot. We note here that for a plan to be executable, it does not necessarily have to be correct and vice versa. We evaluate SayPlan against two baseline methods that integrate an LLM for task planning:

LLM-As-Planner, which generates a full plan sequence in an open-loop manner; the plan includes the full sequence of both navigation and manipulation actions that the robot must execute to complete a task, and LLM+P, an ablated variant of SayPlan, which only incorporates the path planner to allow for shorter horizon plan sequences, without any iterative replanning.

## 5 Results

## 5.1 Semantic Search

We summarise the results for the semantic search evaluation in Table 1. SayPlan (GPT-3.5) consistently failed to reason over the input graph representation, hallucinating nodes to

<table><tr><td></td><td colspan="3">Office</td><td colspan="3">Home</td></tr><tr><td>Subtask</td><td>Human</td><td>SayPlan (GPT-3.5)</td><td>SayPlan (GPT-4)</td><td>Human</td><td>SayPlan (GPT-3.5)</td><td>SayPlan (GPT-4)</td></tr><tr><td>Simple Search</td><td>100%</td><td>6.6%</td><td>86.7%</td><td>100%</td><td>0.0%</td><td>86.7%</td></tr><tr><td>Complex Search</td><td>100%</td><td>0.0%</td><td>73.3%</td><td>100%</td><td>0.0%</td><td>73.3%</td></tr></table>

Table 1: Evaluating the semantic search capabilities of GPT-4. The table shows the semantic search success rate in finding a suitable subgraph for planning.

explore or stagnating at exploring the same node multiple times. SayPlan (GPT-4) in contrast achieved 86.7% and 73.3% success in identifying the desired subgraph across both the simple and complex search tasks respectively, demonstrating significantly better graph-based reasoning than GPT-3.5.

<table><tr><td rowspan="2"></td><td colspan="2">Simple</td><td colspan="2">Long Horizon</td><td colspan="5">Types of Errors</td></tr><tr><td>Corr</td><td>Exec</td><td>Corr</td><td>Exec</td><td>Missing Action</td><td>Missing Pose</td><td>Wrong Action</td><td>Incomplete Search</td><td>Hallucinated Nodes</td></tr><tr><td>LLM+P</td><td>93.3%</td><td>13.3%</td><td>33.3%</td><td>0.0%</td><td>26.7%</td><td>0.0%</td><td>10.0%</td><td>3.33%</td><td>10.0%</td></tr><tr><td>LLM-As-Planner</td><td>93.3%</td><td>80.0%</td><td>66.7%</td><td>13.3%</td><td>20.0%</td><td>60.0%</td><td>0.17%</td><td>0.03%</td><td>10.0%</td></tr><tr><td>SayPlan</td><td>93.3%</td><td>100.0%</td><td>73.3%</td><td>86.6%</td><td>0.0%</td><td>0.0%</td><td>0.0%</td><td>0.0%</td><td>6.67%</td></tr></table>

Table 3: Causal Planning Results. Left: Correctness and Executability on Simple and Long Horizon planning tasks and Right: Types of execution errors encountered when planning using LLMs. Note that SayPlan corrects the majority of the errors faced by LLM-based planners.

While as expected the human baseline achieved 100% on all sets of instructions, we are more interested in the qualitative assessment of the common-sense reasoning used during semantic search. More specifically we would like to identify the similarity in the semantic search heuristics utilised by humans and that used by the underlying LLM based on the given task instruction.

We present the full sequence of explored nodes for both SayPlan (GPT-4) and the human baseline in Appendix F. As shown in the tables, Say-Plan (GPT-4) demonstrates remarkably similar performance to a human’s semantic and common sense reasoning for most tasks, exploring a similar sequence of nodes given a particular instruction. For example, when asked to “find a ripe banana”, the LLM first explores the kitchen followed by the next most likely location, the cafeteria. In the case where no semantics are present in the instruction such as “find me object K31X”, we note that the LLM agent is capable of conducting a breadthfirst-like search across all the unexplored nodes. This highlights the importance of meaningful node names and attributes that capture the relevant environment semantics that the LLM can leverage to relate the query instruction for efficient search.

![](Rana2023SayPlan_figs/48cf5b717d2bdc9ba7cef832f3a35ebb117a13d863850b102c59e7b2752df5a6.jpg)  
Figure 3: Scene Graph Token Progression During Semantic Search. This graph illustrates the scalability of our approach to large-scale 3D scene graphs. Note the importance of node contraction in maintaining a near constant token representation of the 3DSG input.

<table><tr><td></td><td>Full Graph (Token Count)</td><td>Collapsed Graph (Token Count)</td><td>Compression Ratio</td></tr><tr><td>Office</td><td>6731</td><td>878</td><td>86.9%</td></tr><tr><td>Home</td><td>6598</td><td>1817</td><td>72.5%</td></tr></table>

Table 2: 3D Scene Graph Token Count Number of tokens required for the full graph vs. collapsed graph.

An odd failure case in the simple search instructions involved negation, where the agent consistently failed when presented with questions such as “Find me an office that does not have a cabinet” or “Find me a bathroom with no toilet”. Other failure cases noted across the complex search instructions included the LLM’s failure to conduct simple distance-based and count-based reasoning over graph nodes. While trivial to a human, this does require the LLM agent to reason over multiple nodes simultaneously, where it tends to hallucinate or miscount connected nodes.

Scalability Analysis: We additionally analyse the scalability of SayPlan during semantic search. Table 2 illustrates the impact of exploiting the hierarchical nature of 3D scene graphs and allowing the LLM to explore the graph from a collapsed initial state. This allows for a reduction of 82.1% in the initial input tokens required to represent the Office environment and a 60.4% reduction for the Home environment. In Figure 3, we illustrate how endowing the LLM with the ability to contract explored nodes which it deems unsuitable for solving the task allows it to maintain near-constant input memory from a token perspective across the entire semantic search process. Note that the initial number of tokens already present represents the input prompt tokens as given in Appendix J. Further ablation studies on the scalability of SayPlan to even larger 3DSGs are provided in Appendix H.

## 5.2 Causal Planning

The results for causal planning across simple and long-horizon instructions are summarised in Table 3 (left). We compared SayPlan’s performance against two baselines: LLM-As-Planner and LLM+P. All three methods displayed consistent correctness in simple planning tasks at 93%, given that this metric is more a function of the underlying LLMs reasoning capabilities. However, it is interesting to note that in the long-horizon tasks, both the path planner and iterative replanning play an important role in improving this correctness metric by reducing the planning horizon and allowing the LLM to reflect on its previous output.

The results illustrate that the key to ensuring the task plan’s executability was iterative replanning. Both LLM-As-Planner and LLM+P exhibited poor executability, whereas SayPlan achieved nearperfect executability as a result of iterative replanning, which ensured that the generated plans were grounded to adhere to the constraints and predicated imposed by the environment. Detailed task plans and errors encountered are provided in Appendix G. We summarise these errors in Table 3 (right) which shows that plans generated with LLM+P and LLM-As-Planner entailed various types of errors limiting their executability. LLM+P mitigated navigational path planning errors as a result of the classical path planner however still suffered from errors pertaining to the manipulation of the environment - missing actions or incorrect actions which violate environment predicates. SayPlan mitigated these errors via iterative replanning, however in 6.67% of tasks, it failed to correct for some hallucinated nodes. While we believe these errors could be eventually corrected via iterative replanning, we limited the number of replanning steps to 5 throughout all experiments. We provide an illustration of the real-world execution of a generated plan using SayPlan on a mobile manipulator robot coupled with a vision-guided motion controller [44, 45] in Appendix I.

## 6 Limitations

SayPlan is notably constrained by the limitations inherent in current large language models (LLMs), including biases and inaccuracies, affecting the validity of its generated plans. More specifically, SayPlan is limited by the graph-based reasoning capabilities of the underlying LLM which fails at simple distance-based reasoning, node count-based reasoning and node negation. Future work could explore fine-tuning these models for these specific tasks or alternatively incorporate existing and more complex graph reasoning tools [46] to facilitate decision-making. Secondly, SayPlan’s current framework is constrained by the need for a pre-built 3D scene graph and assumes that objects remain static post-map generation, significantly restricting its adaptability to dynamic realworld environments. Future work could explore how online scene graph SLAM systems [15] could be integrated within the SayPlan framework to account for this. Additionally, the incorporation of open-vocabulary representations within the scene graph could yield a general scene representation as opposed to solely textual node descriptions. Lastly, a potential limitation of the current system lies in the scene graph simulator and its ability to capture the various planning failures within the environment. While this works well in the cases presented in this paper, for more complex tasks involving a diverse set of predicates and affordances, the incorporation of relevant feedback messages for each instance may become infeasible and forms an important avenue for future work in this area.

## 7 Conclusion

SayPlan is a natural language-driven planning framework for robotics that integrates hierarchical 3D scene graphs and LLMs to plan across large-scale environments spanning multiple floors and rooms. We ensure the scalability of our approach by exploiting the hierarchical nature of 3D scene graphs and the semantic reasoning capabilities of LLMs to enable the agent to explore the scene graph from the highest level within the hierarchy, resulting in a significant reduction in the initial tokens required to capture larger environments. Once explored, the LLM generates task plans for a mobile manipulator robot, and a scene graph simulator ensures that the plan is feasible and grounded to the environment via iterative replanning. The framework surpasses existing techniques in producing correct, executable plans, which a robot can then follow. Finally, we successfully translate validated plans to a real-world mobile manipulator agent which operates across multiple rooms, assets and objects in a large office environment. SayPlan represents a step forward for general-purpose service robotics that can operate in our homes, hospitals and workplaces, laying the groundwork for future research in this field.

## Acknowledgments

The authors would like to thank Ben Burgess-Limerick for assistance with the robot hardware setup, Nishant Rana for creating the illustrations and Norman Di Palo and Michael Milford for insightful discussions and feedback towards this manuscript. The authors also acknowledge the ongoing support from the QUT Centre for Robotics. This work was partially supported by the Australian Government through the Australian Research Council’s Discovery Projects funding scheme (Project DP220102398) and by an Amazon Research Award to Niko Sunderhauf.¨

## References

[1] L. Ouyang, J. Wu, X. Jiang, D. Almeida, C. L. Wainwright, P. Mishkin, C. Zhang, S. Agarwal, K. Slama, A. Ray, J. Schulman, J. Hilton, F. Kelton, L. E. Miller, M. Simens, A. Askell, P. Welinder, P. F. Christiano, J. Leike, and R. J. Lowe. Training language models to follow instructions with human feedback. ArXiv, abs/2203.02155, 2022.

[2] T. Brown, B. Mann, N. Ryder, M. Subbiah, J. D. Kaplan, P. Dhariwal, A. Neelakantan, P. Shyam, G. Sastry, A. Askell, S. Agarwal, A. Herbert-Voss, G. Krueger, T. Henighan, R. Child, A. Ramesh, D. Ziegler, J. Wu, C. Winter, C. Hesse, M. Chen, E. Sigler, M. Litwin, S. Gray, B. Chess, J. Clark, C. Berner, S. McCandlish, A. Radford, I. Sutskever, and D. Amodei. Language models are few-shot learners. In H. Larochelle, M. Ranzato, R. Hadsell, M. Balcan, and H. Lin, editors, Advances in Neural Information Processing Systems, volume 33, pages 1877–1901. Curran Associates, Inc., 2020.

[3] OpenAI. Gpt-4 technical report. ArXiv, abs/2303.08774, 2023.

[4] A. Brohan, Y. Chebotar, C. Finn, K. Hausman, A. Herzog, D. Ho, J. Ibarz, A. Irpan, E. Jang, R. Julian, et al. Do As I Can, Not As I Say: Grounding language in robotic affordances. In Conference on Robot Learning, pages 287–318. PMLR, 2023.

[5] N. Wake, A. Kanehira, K. Sasabuchi, J. Takamatsu, and K. Ikeuchi. Chatgpt empowered longstep robot control in various environments: A case application, 2023.

[6] D. Driess, F. Xia, M. S. M. Sajjadi, C. Lynch, A. Chowdhery, B. Ichter, A. Wahid, J. Tompson, Q. Vuong, T. Yu, W. Huang, Y. Chebotar, P. Sermanet, D. Duckworth, S. Levine, V. Vanhoucke, K. Hausman, M. Toussaint, K. Greff, A. Zeng, I. Mordatch, and P. Florence. Palm-E: An embodied multimodal language model, 2023.

[7] C. H. Song, J. Wu, C. Washington, B. M. Sadler, W.-L. Chao, and Y. Su. LLM-Planner: Few-shot grounded planning for embodied agents with large language models. arXiv preprint arXiv:2212.04088, 2022.

[8] W. Huang, F. Xia, T. Xiao, H. Chan, J. Liang, P. Florence, A. Zeng, J. Tompson, I. Mordatch, Y. Chebotar, et al. Inner monologue: Embodied reasoning through planning with language models. arXiv preprint arXiv:2207.05608, 2022.

[9] B. Liu, Y. Jiang, X. Zhang, Q. Liu, S. Zhang, J. Biswas, and P. Stone. LLM+P: Empowering large language models with optimal planning proficiency. arXiv preprint arXiv:2304.11477, 2023.

[10] T. Silver, V. Hariprasad, R. S. Shuttleworth, N. Kumar, T. Lozano-Perez, and L. P. Kaelbling.´ PDDL planning with pretrained large language models. In NeurIPS 2022 Foundation Models for Decision Making Workshop.

[11] I. Armeni, Z.-Y. He, J. Gwak, A. R. Zamir, M. Fischer, J. Malik, and S. Savarese. 3D scene graph: A structure for unified semantics, 3D space, and camera. In Proceedings of the IEEE/CVF international conference on computer vision, pages 5664–5673, 2019.

[12] U.-H. Kim, J.-M. Park, T.-J. Song, and J.-H. Kim. 3-D scene graph: A sparse and semantic representation of physical environments for intelligent agents. IEEE transactions on cybernetics, 50(12):4921–4933, 2019.

[13] A. Rosinol, A. Violette, M. Abate, N. Hughes, Y. Chang, J. Shi, A. Gupta, and L. Carlone. Kimera: From slam to spatial perception with 3D dynamic scene graphs. The International Journal of Robotics Research, 40(12-14):1510–1546, 2021.

[14] P. Gay, J. Stuart, and A. Del Bue. Visual graphs from motion (vgfm): Scene understanding with object geometry reasoning. In Computer Vision–ACCV 2018: 14th Asian Conference on Computer Vision, Perth, Australia, December 2–6, 2018, Revised Selected Papers, Part III 14, pages 330–346. Springer, 2019.

[15] N. Hughes, Y. Chang, and L. Carlone. Hydra: A real-time spatial perception engine for 3D scene graph construction and optimization. Robotics: Science and Systems XIV, 2022.

[16] C. Agia, K. M. Jatavallabhula, M. Khodeir, O. Miksik, V. Vineet, M. Mukadam, L. Paull, and F. Shkurti. Taskography: Evaluating robot task planning over large 3D scene graphs. In Conference on Robot Learning, pages 46–58. PMLR, 2022.

[17] N. Shinn, F. Cassano, B. Labash, A. Gopinath, K. Narasimhan, and S. Yao. Reflexion: Language agents with verbal reinforcement learning, 2023.

[18] J. Wei, X. Wang, D. Schuurmans, M. Bosma, E. Chi, Q. Le, and D. Zhou. Chain of thought prompting elicits reasoning in large language models. arXiv preprint arXiv:2201.11903, 2022.

[19] E. W. Dijkstra. A note on two problems in connexion with graphs. In Edsger Wybe Dijkstra: His Life, Work, and Legacy, pages 287–290. 2022.

[20] D. McDermott, M. Ghallab, A. Howe, C. Knoblock, A. Ram, M. Veloso, D. Weld, and D. Wilkins. PDDL-the planning domain definition language. 1998.

[21] M. Fox and D. Long. PDDL2. 1: An extension to PDDL for expressing temporal planning domains. Journal of artificial intelligence research, 20:61–124, 2003.

[22] P. Haslum, N. Lipovetzky, D. Magazzeni, and C. Muise. An introduction to the planning domain definition language. Synthesis Lectures on Artificial Intelligence and Machine Learning, 13(2):1–187, 2019.

[23] M. Gelfond and Y. Kahl. Knowledge representation, reasoning, and the design of intelligent agents: The answer-set programming approach. Cambridge University Press, 2014.

[24] S. Tellex, T. Kollar, S. Dickerson, M. R. Walter, A. G. Banerjee, S. J. Teller, and N. Roy. Understanding natural language commands for robotic navigation and mobile manipulation. Proceedings of the AAAI Conference on Artificial Intelligence, 2011.

[25] J. Thomason, A. Padmakumar, J. Sinapov, N. Walker, Y. Jiang, H. Yedidsion, J. W. Hart, P. Stone, and R. J. Mooney. Jointly improving parsing and perception for natural language commands through human-robot dialog. J. Artif. Intell. Res., 67:327–374, 2020.

[26] H. Kautz and B. Selman. Pushing the envelope: Planning, propositional logic, and stochastic search. In Proceedings of the national conference on artificial intelligence, pages 1194–1201, 1996.

[27] B. Bonet and H. Geffner. Planning as heuristic search. Artificial Intelligence, 129(1-2):5–33, 2001.

[28] M. Vallati, L. Chrpa, M. Grzes, T. L. McCluskey, M. Roberts, S. Sanner, et al. The 2014´ international planning competition: Progress and trends. AI Magazine, 36(3):90–98, 2015.

[29] R. Chitnis, T. Silver, B. Kim, L. Kaelbling, and T. Lozano-Perez. CAMPs: Learning Context-Specific Abstractions for Efficient Planning in Factored MDPs. In Conference on Robot Learning, pages 64–79. PMLR, 2021.

[30] T. Silver, R. Chitnis, A. Curtis, J. B. Tenenbaum, T. Lozano-Perez, and L. P. Kaelbling. Plan- ´ ning with learned object importance in large problem instances using graph neural networks. In Proceedings of the AAAI conference on artificial intelligence, volume 35, pages 11962–11971, 2021.

[31] F. Ceola, E. Tosello, L. Tagliapietra, G. Nicola, and S. Ghidoni. Robot task planning via deep reinforcement learning: a tabletop object sorting application. In 2019 IEEE International Conference on Systems, Man and Cybernetics (SMC), pages 486–492, 2019. doi:10.1109/ SMC.2019.8914278.

[32] S. Yao, J. Zhao, D. Yu, N. Du, I. Shafran, K. Narasimhan, and Y. Cao. React: Synergizing reasoning and acting in language models. arXiv preprint arXiv:2210.03629, 2022.

[33] A. Zeng, A. Wong, S. Welker, K. Choromanski, F. Tombari, A. Purohit, M. Ryoo, V. Sindhwani, J. Lee, V. Vanhoucke, et al. Socratic models: Composing zero-shot multimodal reasoning with language. arXiv preprint arXiv:2204.00598, 2022.

[34] Y. Xie, C. Yu, T. Zhu, J. Bai, Z. Gong, and H. Soh. Translating natural language to planning goals with large-language models. arXiv preprint arXiv:2302.05128, 2023.

[35] B. Peng, M. Galley, P. He, H. Cheng, Y. Xie, Y. Hu, Q. Huang, L. Liden, Z. Yu, W. Chen, et al. Check your facts and try again: Improving large language models with external knowledge and automated feedback. arXiv preprint arXiv:2302.12813, 2023.

[36] T. Schick, J. Dwivedi-Yu, R. Dess\`ı, R. Raileanu, M. Lomeli, L. Zettlemoyer, N. Cancedda, and T. Scialom. Toolformer: Language models can teach themselves to use tools. arXiv preprint arXiv:2302.04761, 2023.

[37] R. Liu, J. Wei, S. S. Gu, T.-Y. Wu, S. Vosoughi, C. Cui, D. Zhou, and A. M. Dai. Mind’s eye: Grounded language model reasoning through simulation. arXiv preprint arXiv:2210.05359, 2022.

[38] M. Skreta, N. Yoshikawa, S. Arellano-Rubach, Z. Ji, L. B. Kristensen, K. Darvish, A. Aspuru-Guzik, F. Shkurti, and A. Garg. Errors are useful prompts: Instruction guided task programming with verifier-assisted iterative prompting. arXiv preprint arXiv:2303.14100, 2023.

[39] Z. Ravichandran, L. Peng, N. Hughes, J. D. Griffith, and L. Carlone. Hierarchical representations and explicit memory: Learning effective navigation policies on 3D scene graphs using graph neural networks. In 2022 International Conference on Robotics and Automation (ICRA), pages 9272–9279. IEEE, 2022.

[40] A. Kurenkov, R. Mart´ın-Mart´ın, J. Ichnowski, K. Goldberg, and S. Savarese. Semantic and geometric modeling with neural message passing in 3D scene graphs for hierarchical mechanical search. In 2021 IEEE International Conference on Robotics and Automation (ICRA), pages 11227–11233. IEEE, 2021.

[41] S. Garg, N. Sunderhauf, F. Dayoub, D. Morrison, A. Cosgun, G. Carneiro, Q. Wu, T.-J. Chin,¨ I. Reid, S. Gould, et al. Semantics for robotic mapping, perception and interaction: A survey. Foundations and Trends® in Robotics, 8(1–2):1–224, 2020.

[42] A. A. Hagberg, D. A. Schult, and P. J. Swart. Exploring network structure, dynamics, and function using networkx. In G. Varoquaux, T. Vaught, and J. Millman, editors, Proceedings of the 7th Python in Science Conference, pages 11 – 15, Pasadena, CA USA, 2008.

[43] M. Skreta, N. Yoshikawa, S. Arellano-Rubach, Z. Ji, L. B. Kristensen, K. Darvish, A. Aspuru-Guzik, F. Shkurti, and A. Garg. Errors are useful prompts: Instruction guided task programming with verifier-assisted iterative prompting. ArXiv, abs/2303.14100, 2023. URL https://api.semanticscholar.org/CorpusID:257757298.

[44] J. Haviland, N. Sunderhauf, and P. Corke. A holistic approach to reactive mobile manipulation.¨ IEEE Robotics and Automation Letters, 7(2):3122–3129, 2022.

[45] P. Corke and J. Haviland. Not your grandmother’s toolbox–the robotics toolbox reinvented for python. In 2021 IEEE international conference on robotics and automation (ICRA), pages 11357–11363. IEEE, 2021.

[46] J. Zhang. Graph-toolformer: To empower LLMs with graph reasoning ability via prompt augmented by chatgpt. arXiv preprint arXiv:2304.11116, 2023.

[47] S. Haddadin, S. Parusel, L. Johannsmeier, S. Golz, S. Gabl, F. Walch, M. Sabaghian, C. Jahne,¨ L. Hausperger, and S. Haddadin. The franka emika robot: A reference platform for robotics research and education. IEEE Robotics and Automation Magazine, 29(2):46–64, 2022. doi: 10.1109/MRA.2021.3138382.

[48] Omron. Omron LD / HD Series. URL https://www.ia.omron.com/products/ family/3664/dimension.html.

[49] C. Chi, S. Feng, Y. Du, Z. Xu, E. Cousineau, B. Burchfiel, and S. Song. Diffusion policy: Visuomotor policy learning via action diffusion. In Proceedings of Robotics: Science and Systems (RSS), 2023.

[50] K. Rana, A. Melnik, and N. Sunderhauf. Contrastive language, action, and state pre-training¨ for robot learning, 2023.

[51] Q-transformer: Scalable offline reinforcement learning via autoregressive q-functions. In 7th Annual Conference on Robot Learning, 2023.

[52] K. Rana, M. Xu, B. Tidd, M. Milford, and N. Suenderhauf. Residual skill policies: Learning an adaptable skill-based action space for reinforcement learning for robotics. In 6th Annual Conference on Robot Learning, 2022. URL https://openreview.net/forum?id= 0nb97NQypbK.

## A Implementation Details

We utilise GPT-4 [3] as the underlying LLM agent unless otherwise stated. We follow a similar prompting structure to Wake et al. [5] as shown in Appendix J. We define the agent’s role, details pertaining to the scene graph environment, the desired output structure and a set of input-output examples which together form the static prompt used for in-context learning. This static prompt is both task- and environment-agnostic and takes up ≈3900 tokens of the LLM’s input. During semantic search, both the 3D Scene Graph and Memory components of the input prompt get updated at each step, while during iterative replanning only the Feedback component gets updated with information from the scene graph simulator. In all cases, the LLM is prompted to output a JSON object containing arguments to call the provided API functions.

## B Environments

![](Rana2023SayPlan_figs/e69c524edfaaa32f66d6b10e380768446b0a551fc2cd69877eefb216627a3dc4.jpg)  
Figure 4: Large-scale environments used to evaluate SayPlan. The environments span multiple rooms and floors including a vast range of

We evaluate SayPlan across a set of two large-scale environments spanning multiple rooms and floors as shown in Figure 4. We provide details of each of these environments below, including a breakdown of the number of entities and tokens required to represent them in the 3DSG:

Office: A large-scale office floor, spanning 37 rooms and 151 assets and objects which the agent can interact with. A full and collapsed 3D scene graph representation of this environment are provided in Appendix D and E respectively. This scene graph represents a real-world office floor within which a mobile manipulator robot is present. This allows us to embody the plans generated using SayPlan and evaluate their feasibility in the corresponding environment. Real-world video demonstrations of a mobile manipulator robot executing the generated plan in this office environment are provided on our project site<sup>2</sup>.

Home: An existing 3D scene graph from the Stanford 3D Scene Graph dataset [11] which consists of a family home environment (Klickitat) spanning 28 rooms across 3 floors and contains 112 assets and objects that the agent can interact with. A 3D visual of this environment can be viewed at the 3D Scene Graph project website<sup>3</sup>.

## B.1 Real World Environment Plan Execution

To enable real-world execution of the task plans generated over a 3DSG, we require a corresponding 2D metric map within which we can align the posed nodes captured by the 3DSG. At each room node we assume the real robot can visually locate the appropriate assets and objects that are visible to it within the 3DSG. The mobile manipulator robot used for the demonstration consisted of a Franka Panda 7-DoF robot manipulator [47] attached to an LD-60 Omron mobile base [48]. The robot is equipped with a LiDAR scanner to localise the robot both within the real world and the corresponding 3DSG. All the skills or affordances including pick, place, open and close were developed using the motion controller from [44] coupled with a RGB-D vision module for grasp detection, and a behaviour tree to manage the execution of each component including failure recovery. Future work could incorporate a range of pre-trained skills (whisking, flipping, spreading etc.) using imitation learning [49, 50] or reinforcement learning [51, 52] to increase the diversity of tasks that SayPlan is able to achieve.

<table><tr><td>Entity Type</td><td>Number of Entities</td><td>Total Number of Tokens</td><td>Average Number of Tokens</td></tr><tr><td>Room Node</td><td>37</td><td>340</td><td>9.19</td></tr><tr><td>Asset Node</td><td>73</td><td>1994</td><td>27.3</td></tr><tr><td>Object Node</td><td>78</td><td>2539</td><td>32.6</td></tr><tr><td>Agent Node</td><td>1</td><td>15</td><td>15.0</td></tr><tr><td>Node Edges</td><td>218</td><td>1843</td><td>8.45</td></tr><tr><td>Full Graph</td><td>407</td><td>6731</td><td>16.5</td></tr><tr><td>Collapsed Graph</td><td>105</td><td>878</td><td>8.36</td></tr></table>

Table 4: Detailed 3DSG breakdown for the Office Environment. The table summarises the number of different entities present in the 3DSG, the total LLM tokens required to represent each entity group and the average number of tokens required to represent a single type of entity.

<table><tr><td>Entity Type</td><td>Number of Entities</td><td>Total Number of Tokens</td><td>Average Number of Tokens</td></tr><tr><td>Room Node</td><td>28</td><td>231</td><td>8.25</td></tr><tr><td>Asset Node</td><td>52</td><td>1887</td><td>36.3</td></tr><tr><td>Object Node</td><td>60</td><td>1881</td><td>31.35</td></tr><tr><td>Agent Node</td><td>1</td><td>15</td><td>15</td></tr><tr><td>Node Edges</td><td>323</td><td>2584</td><td>8</td></tr><tr><td>Full Graph</td><td>464</td><td>6598</td><td>14.2</td></tr><tr><td>Collapsed Graph</td><td>240</td><td>1817</td><td>7.57</td></tr></table>

Table 5: Detailed 3DSG breakdown for the Home Environment. The table summarises the number of different entities present in the 3DSG, the total LLM tokens required to represent each entity group and the average number of tokens required to represent a single type of entity.

## C Tasks

<table><tr><td>Instruction Family</td><td>Num</td><td>Explanation</td><td>Example Instruction</td></tr><tr><td colspan="4">Semantic Search</td></tr><tr><td>Simple Search</td><td>30</td><td>Queries focussed on evaluating the basic semantic search capabilities of SayPlan</td><td>Find me a ripe banana.</td></tr><tr><td>Complex Search</td><td>30</td><td>Abstract semantic search queries which require complex reasoning</td><td>Find the room where people are playing board games.</td></tr><tr><td colspan="4">Causal Planning</td></tr><tr><td>Simple Planning</td><td>15</td><td>Queries which require the agent to perform search, causal reasoning and environment interaction in order to solve a task.</td><td>Refrigerate the orange left on the kitchen bench.</td></tr><tr><td>Long-Horizon Planning</td><td>15</td><td>Long Horizon planning queries requiring multiple interactive steps</td><td>Tobi spilt soda on his desk. Help him clean up.</td></tr></table>

Table 6: List of evaluation task instructions. We evaluate SayPlan on 90 instructions, grouped to test various aspects of the planning capabilities across large-scale scene graphs. The full instruction set is given in Appendix C.

We evaluate SayPlan across 4 instruction sets which are classified to evaluate different aspects of its 3D scene graph reasoning and planning capabilities as shown in Table 6:

Simple Search: Focused on evaluating the semantic search capabilities of the LLM based on queries which directly reference information in the scene graph as well as the basic graph-based reasoning capabilities of the LMM.

Complex Search: Abstract semantic search queries which require complex reasoning. The information required to solve these search tasks is not readily available in the graph and has to be inferred by the underlying LLM.

Simple Planning: Task planning queries which require the agent to perform graph search, causal reasoning and environment interaction in order to solve the task. Typically requires shorter horizon plans over single rooms.

Long Horizon Planning: Long Horizon planning queries require multiple interactive steps. These queries evaluate SayPlan’s ability to reason over temporally extended instructions to investigate how well it scales to such regimes. Typically requires long horizon plans spanning multiple rooms.

The full list of instructions used and the corresponding aspect the query evaluates are given in the following tables:

## C.1 Simple Search

## C.1.1 Office Environment

<table><tr><td colspan="2">Instruction</td></tr><tr><td>Find me object K31X.</td><td>▷ unguided search with no semantic cue</td></tr><tr><td>Find me a carrot.</td><td>▷ semantic search based on node name</td></tr><tr><td>Find me anything purple in the postdoc bays.</td><td>▷ semantic search with termination conditioned on attribute</td></tr><tr><td>Find me a ripe banana.</td><td>▷ semantic search with termination conditioned on attribute</td></tr><tr><td>Find me something that has a screwdriver in it.</td><td>▷ unguided search with termination conditioned on children</td></tr><tr><td>One of the offices has a poster of the Terminator. Which one is it?</td><td>▷ semantic search with termination conditioned on children</td></tr><tr><td>I printed a document but I don’t know which printer has it. Find the document.</td><td>▷ semantic search based on parent</td></tr><tr><td>I left my headphones in one of the meeting rooms. Locate them.</td><td>▷ semantic search based on parent</td></tr><tr><td>Find the PhD bay that has a drone in it.</td><td>▷ semantic search with termination conditioned on children</td></tr><tr><td>Find the kale that is not in the kitchen.</td><td>▷ semantic search with termination conditioned on a negation predicate on parent</td></tr><tr><td>Find me an office that does not have a cabinet.</td><td>▷ semantic search with termination conditioned on a negation predicate on children</td></tr><tr><td>Find me an office that contains a cabinet, a desk, and a chair.</td><td>▷ semantic search with termination conditioned on a conjunctive query on children</td></tr><tr><td>Find a book that was left next to a robotic gripper.</td><td>▷ semantic search with termination conditioned on a sibling</td></tr><tr><td>Luis gave one of his neighbours a stapler. Find the stapler.</td><td>▷ semantic search with termination conditioned on a sibling</td></tr><tr><td>There is a meeting room with a chair but no table. Locate it.</td><td>▷ semantic search with termination conditioned on a conjunctive query with negation</td></tr></table>

Table 7: Simple Search Instructions. Evaluated in Office Environment.

C.1.2 Home Environment

<table><tr><td colspan="2">Instruction</td></tr><tr><td>Find me a FooBar.</td><td>▷ unguided search with no semantic cue</td></tr><tr><td>Find me a bottle of wine.</td><td>▷ semantic search based on node name</td></tr><tr><td>Find me a plant with thorns.</td><td>▷ semantic search with termination conditioned on attribute</td></tr><tr><td>Find me a plant that needs watering.</td><td>▷ semantic search with termination conditioned on attribute</td></tr><tr><td>Find me a bathroom with no toilet.</td><td>▷ semantic search with termination conditioned on a negation predicate</td></tr><tr><td>The baby dropped their rattle in one of the rooms. Locate it.</td><td>▷ semantic search based on node name</td></tr><tr><td>I left my suitcase either in the bedroom or the living room. Which room is it in.</td><td>▷ semantic search based on node name</td></tr><tr><td>Find the room with a ball in it.</td><td>▷ semantic search based on node name</td></tr><tr><td>I forgot my book on a bed. Locate it.</td><td>▷ semantic search based on node name</td></tr><tr><td>Find an empty vase that was left next to sink.</td><td>▷ semantic search with termination conditioned on sibling</td></tr><tr><td>Locate the dining room which has a table, chair and a baby monitor.</td><td>▷ semantic search with termination conditioned on conjuctive query</td></tr><tr><td>Locate a chair that is not in any dining room.</td><td>▷ semantic search with termination conditioned on negation predicate</td></tr><tr><td>I need to shave. Which room has both a razor and shaving cream.</td><td>▷ semantic search with termination conditioned on children</td></tr><tr><td>Find me 2 bedrooms with pillows in them.</td><td>▷ semantic search with multiple returns</td></tr><tr><td>Find me 2 bedrooms without pillows in them.</td><td>▷ semantic search with multiple returns based on negation predicate</td></tr></table>

Table 8: Simple Search Instructions. Evaluated in Home Environment.

## C.2 Complex Search

## C.2.1 Office Environment

<table><tr><td colspan="2">Instruction</td></tr><tr><td>Find object J64M. J64M should be kept at below 0 degrees Celsius.</td><td>▷ semantic search guided by implicit world knowledge (knowledge not directly encoded in graph)</td></tr><tr><td>Find me something non vegetarian.</td><td>▷ semantic search with termination conditioned on implicit world knowledge</td></tr><tr><td>Locate something sharp.</td><td>▷ unguided search with termination conditioned on implicit world knowledge</td></tr><tr><td>Find the room where people are playing board games.</td><td>▷ semantic search with termination conditioned on ability to deduce context from node children using world knowledge (“board game” is not part of any node name or attribute in this graph)</td></tr><tr><td>Find an office of someone who is clearly a fan of Arnold Schwarzenegger.</td><td>▷ semantic search with termination conditioned on ability to deduce context from node children using world knowledge</td></tr><tr><td>There is a postdoc that has a pet Husky. Find the desk that’s most likely theirs.</td><td>▷ semantic search with termination conditioned on ability to deduce context from node children using world knowledge</td></tr><tr><td>One of the PhD students was given more than one complimentary T-shirts. Find his desk.</td><td>▷ semantic search with termination conditioned on the number of children</td></tr><tr><td>Find me the office where a paper attachment device is inside an asset that is open.</td><td>▷ semantic search with termination conditioned on node descendants and their attributes</td></tr><tr><td>There is an office which has a cabinet containing exactly 3 items in it. Locate the office.</td><td>▷ semantic search with termination conditioned on the number of children</td></tr><tr><td>There is an office which has a cabinet containing a rotten apple. The cabinet name contains an even number. Locate the office.</td><td>▷ semantic search guided by numerical properties</td></tr><tr><td>Look for a carrot. The carrot is likely to be in a meeting room but I’m not sure.</td><td>▷ semantic search guided by user provided bias</td></tr><tr><td>Find me a meeting room with a RealSense camera.</td><td>▷ semantic search that has no result (no meeting room has a realsense camera in the graph)</td></tr><tr><td>Find the closest fire extinguisher to the manipulation lab.</td><td>▷ search guided by node distance</td></tr><tr><td>Find me the closest meeting room to the kitchen.</td><td>▷ search guided by node distance</td></tr><tr><td>Either Filipe or Tobi has my headphones. Locate it.</td><td>▷ evaluating constrained search, early termination once the two office are explored</td></tr></table>

Table 9: Complex Search Instructions. Evaluated in Office Environment.

C.2.2 Home Environment

<table><tr><td colspan="2">Instruction</td></tr><tr><td>I need something to access ChatGPT. Where should I go?</td><td>▷ semantic search guided by implicit world knowledge</td></tr><tr><td>Find the livingroom that contains the most electronic devices.</td><td>▷ semantic search with termination conditioned on children with indirect information</td></tr><tr><td>Find me something to eat with a lot of potassium.</td><td>▷ semantic search with termination conditioned on implicit world knowledge</td></tr><tr><td>I left a sock in a bedroom and one in the living room. Locate them. They should match.</td><td>▷ semantic search with multiple returns</td></tr><tr><td>Find me a potted plant that is most likely a cactus.</td><td>▷ semantic search with termination implicitly conditioned on attribute</td></tr><tr><td>Find the dining room with exactly 5 chairs.</td><td>▷ semantic search with termination implicitly conditioned on quantity of children</td></tr><tr><td>Find me the bedroom closest to the home office.</td><td>▷ semantic search with termination implicitly conditioned on node distance</td></tr><tr><td>Find me a bedroom with an unusual amount of bowls.</td><td>▷ semantic search with termination implicitly conditioned on quantity of children</td></tr><tr><td>Which bedroom is empty.</td><td>▷ semantic search with termination implicitly conditioned on quantity of children</td></tr><tr><td>Which bathroom has the most potted plants.</td><td>▷ semantic search with termination implicitly conditioned on quantity of children</td></tr><tr><td>The kitchen is flooded. Find somewhere I can heat up my food.</td><td>▷ semantic search guided by negation</td></tr><tr><td>Find me the room which most likely belongs to a child</td><td>▷ semantic search with termination conditioned on ability to deduce context from node children using world knowledge</td></tr><tr><td>15 guests are arriving. Locate enough chairs to seat them.</td><td>▷ semantic search with termination implicitly conditioned on the quantity of specified node</td></tr><tr><td>A vegetarian dinner was prepared in one of the dining rooms. Locate it.</td><td>▷ semantic search with selection criteria based on world knowledge</td></tr><tr><td>My tie is in one of the closets. Locate it.</td><td>▷ evaluating constrained search that has no result, termination after exploring closets</td></tr></table>

Table 10: Complex Search Instructions. Evaluated in Home Environment.

## C.3 Simple Planning

<table><tr><td>Instruction</td></tr><tr><td>Close Jason&#x27;s cabinet.</td></tr><tr><td>Refrigerate the orange left on the kitchen bench.</td></tr><tr><td>Take care of the dirty plate in the lunchroom.</td></tr><tr><td>Place the printed document on Will&#x27;s desk.</td></tr><tr><td>Peter is working hard at his desk. Get him a healthy snack.</td></tr><tr><td>Hide one of Peter&#x27;s valuable belongings.</td></tr><tr><td>Wipe the dusty admin shelf.</td></tr><tr><td>There is coffee dripping on the floor. Stop it.</td></tr><tr><td>Place Will&#x27;s drone on his desk.</td></tr><tr><td>Move the monitor from Jason&#x27;s office to Filipe&#x27;s.</td></tr><tr><td>My parcel just got delivered! Locate it and place it in the appropriate lab.</td></tr><tr><td>Check if the coffee machine is working.</td></tr><tr><td>Heat up the chicken kebab.</td></tr><tr><td>Something is smelling in the kitchen. Dispose of it.</td></tr><tr><td>Throw what the agent is holding in the bin.</td></tr></table>

Table 11: Simple Planning Instructions. Evaluated in Office Environment.

## C.4 Long Horizon Planning

<table><tr><td>Instruction</td></tr><tr><td>Heat up the noodles in the fridge, and place it somewhere where I can enjoy it.</td></tr><tr><td>Throw the rotting fruit in Dimity&#x27;s office in the correct bin.</td></tr><tr><td>Wash all the dishes on the lunch table. Once finished, place all the clean cutlery in the drawer.</td></tr><tr><td>Safely file away the freshly printed document in Will&#x27;s office then place the undergraduate thesis on his desk.</td></tr><tr><td>Make Niko a coffee and place the mug on his desk.</td></tr><tr><td>Someone has thrown items in the wrong bins. Correct this.</td></tr><tr><td>Tobi spilt soda on his desk. Throw away the can and take him something to clean with.</td></tr><tr><td>I want to make a sandwich. Place all the ingredients on the lunch table.</td></tr><tr><td>A delegation of project partners is arriving soon. We want to serve them snacks and non-alcoholic drinks. Prepare everything in the largest meeting room. Use items found in the supplies room only.</td></tr><tr><td>Serve bottled water to the attendees who are seated in meeting room 1. Each attendee can only receive a single bottle of water.</td></tr><tr><td>Empty the dishwasher. Place all items in their correct locations</td></tr><tr><td>Locate all 6 complimentary t-shirts given to the PhD students and place them on the shelf in admin.</td></tr><tr><td>I&#x27;m hungry. Bring me an apple from Peter and a pepsi from Tobi. I&#x27;m at the lunch table.</td></tr><tr><td>Let&#x27;s play a prank on Niko. Dimity might have something.</td></tr><tr><td>There is an office which has a cabinet containing a rotten apple. The cabinet name contains an even number. Locate the office, throw away the fruit and get them a fresh apple.</td></tr></table>

Table 12: Long-Horizon Planning Instructions. Evaluated in Office Environment.

## D Full 3D Scene Graph: Office Environment

![](Rana2023SayPlan_figs/ebb1197905178c7b799dfc145cbd28197dca8d28e3d867970b4b3887c24c2170.jpg)  
Figure 5: 3D Scene Graph - Fully Expanded Office Environment. Full 3D scene graph exposing all the rooms, assets and objects available in the scene. Note that the LLM agent never sees all this information unless it chooses to expand every possible node without contraction.

![](Rana2023SayPlan_figs/fef25bd05f12d75e2b03c126040a7b0f00626d6341af0ea6569db1e5cfed196b.jpg)  
Figure 6: 3D Scene Graph - Contracted Office Environment. Contracted 3D scene graph exposing only the highest level within the hierarchy - room nodes. This results in an 82.1% reduction in the number of tokens required to represent the scene before the semantic search phase.

## F Semantic Search Evaluation Results

\- Full listings of the generated semantic search sequences for the evaluation instruction sets are provided on the following pages -

Find me object K31X.

Find me anything purple in the postdoc bays.

One of the offices has a poster of the Terminator. Which one is it?

I printed a document, but I dont know which printer has it. Find the document.

![](Rana2023SayPlan_figs/35c435ed9a7523fce004eae5babe3e47004435bc07656a023c2cc743e385bb22.jpg)

I left my headphones in one of the meeting rooms. Locate them.

Find the PhD bay that has a drone in it.

Find the kale that is not in the kitchen.

Find me an office that does not have a cabinet.

![](Rana2023SayPlan_figs/273947ea20012176217682fe5ce46b6ab8562ced6ea875838305ad0e73ed7a12.jpg)  
Table 13: Simple Search Office Environment Evaluation. Sequence of Explored Nodes for Simple Search Office Environment Instructions.

Find object J64M. J64M should be kept at below 0 degrees Celsius.

Find me something non vegetarian.

Find the office of someone who is clearly a fan of Arnold Schwarzenegger.

There is postdoc that has a pet Husky. Find the desk that’s most likely theirs.

One of the PhD students was given more than one complimentary T-shirt. Find his desk.

Find me the office where a paper attachment device is inside an asset that is open.

![](Rana2023SayPlan_figs/75d5c966155c36d5ff319d71612d362ec4947e0a4d97a53619a9b1b85e626971.jpg)

There is an office which has a cabinet containing exactly 3 items in it. Locate the office.

There is an office containing a rotten apple. The cabinet name contains an even number. Locate the office.

![](Rana2023SayPlan_figs/a4c0fe1cccb3f6e5cd0415dfd9def509c91b45d536e3030496006cb6e6c01d93.jpg)  
Table 14: Complex Search Office Environment Evaluation. Sequence of Explored Nodes for Complex Search Office Environment Instructions.

![](Rana2023SayPlan_figs/1dbd73076111be9e5fead145a294f49b0ced612902f121090f2a8e8e82cb90a2.jpg)

I forgot my book on a bed. Locate it.

![](Rana2023SayPlan_figs/d164c63db68b433f19ce512a0ff6475064ab01f8d54be45bb76dd9b3bac9ea6b.jpg)  
Table 15: Simple Search Home Environment Evaluation. Sequence of Explored Nodes for Simple Search Home Environment Instructions.

<table><tr><td>kitchen0</td><td>&gt;</td><td>kitchen1</td></tr><tr><td>kitchen0</td><td>&gt;</td><td>kitchen1</td></tr></table>

I need something to access ChatGPT. Where should I go?.

Find the livingroom that contains the most electronic devices.

<table><tr><td>living_room0</td><td>living_room1</td><td>living_room2</td></tr><tr><td>living_room0</td><td>living_room1</td><td>living_room2</td></tr></table>

Find me something to eat with alot of potassium.

I left a sock in a bedrooom and in one of the livingrooms. Locate them. They should match.

![](Rana2023SayPlan_figs/74321c654f3f3972eb006e145cd1078cd950b9b8f6d8b0bf4df08181bceecca6.jpg)

Find the potted plant that is most likely a cactus.

Find the dining room with exactly 5 chairs.

Find me the bedroom closest to the home office.

Find me the bedroom with an unusual amount of bowls.

<table><tr><td>bedroom0</td><td>bedroom1</td><td>bedroom2</td></tr><tr><td>bedroom0</td><td>bedroom1</td><td>bedroom2</td></tr></table>

Which bedroom is empty.

![](Rana2023SayPlan_figs/2606b4dacbf577bc726d8700caa64e76ca500c6e1c4759c7f441342f96a12b19.jpg)

Which bathroom has the most potted plants.

The kitchen is flooded. Find somewhere I can heat up my food.

<table><tr><td>kitchen0</td><td>kitchen1</td><td>dining_room0</td></tr><tr><td>dining_room0</td><td></td><td></td></tr></table>

![](Rana2023SayPlan_figs/466eb97c0643091de0dfab6e3ce35a2bec628490bd3333a4100461851917ac53.jpg)  
Table 16: Complex Search Home Environment Evaluation. Sequence of Explored Nodes for Complex Search Home Environment Instructions.

## G Causal Planning Evaluation Results

In this section, we provide a detailed breakdown of the causal planning performance of SayPlan across the two sets of evaluation instructions. Tables 17 and 18 detail the correctness, executability and the number of iterative replanning steps it took to obtain an executable plan.

<table><tr><td>Instruction</td><td>Corr.</td><td>Exec.</td><td>No. of Replanning Iterations</td></tr><tr><td>Close Jason's cabinet.</td><td>✓</td><td>✓</td><td>0</td></tr><tr><td>Refrigerate the orange left on the kitchen bench.</td><td>✓</td><td>✓</td><td>0</td></tr><tr><td>Take care of the dirty plate in the lunchroom.</td><td>✓</td><td>✓</td><td>0</td></tr><tr><td>Place the printed document on Will's desk.</td><td>✓</td><td>✓</td><td>0</td></tr><tr><td>Peter is working hard at his desk. Get him a healthy snack.</td><td>✗</td><td>✓</td><td>5</td></tr><tr><td>Hide one of Peter's valuable belongings.</td><td>✓</td><td>✓</td><td>0</td></tr><tr><td>Wipe the dusty admin shelf.</td><td>✓</td><td>✓</td><td>0</td></tr><tr><td>There is coffee dripping on the floor. Stop it.</td><td>✓</td><td>✓</td><td>0</td></tr><tr><td>Place Will's drone on his desk.</td><td>✓</td><td>✓</td><td>0</td></tr><tr><td>Move the monitor from Jason's office to Filipe's.</td><td>✓</td><td>✓</td><td>0</td></tr><tr><td>My parcel just got delivered! Locate it and place it in the appropriate lab.</td><td>✓</td><td>✓</td><td>0</td></tr><tr><td>Check if the coffee machine is working.</td><td>✓</td><td>✓</td><td>0</td></tr><tr><td>Heat up the chicken kebab.</td><td>✓</td><td>✓</td><td>1</td></tr><tr><td>Something is smelling in the kitchen. Dispose of it.</td><td>✓</td><td>✓</td><td>0</td></tr><tr><td>Throw what the agent is holding in the bin.</td><td>✓</td><td>✓</td><td>1</td></tr><tr><td>Heat up the noodles in the fridge, and place it somewhere where I can enjoy it.</td><td>√</td><td>√</td><td>2</td></tr><tr><td>Throw the rotting fruit in Dimity's office in the correct bin.</td><td>√</td><td>√</td><td>1</td></tr><tr><td>Wash all the dishes on the lunch table. Once finished, place all the clean cutlery in the drawer.</td><td>✕</td><td>√</td><td>2</td></tr><tr><td>Safely file away the freshly printed document in Will's office then place the undergraduate thesis on his desk.</td><td>√</td><td>√</td><td>2</td></tr><tr><td>Make Niko a coffee and place the mug on his desk.</td><td>√</td><td>√</td><td>0</td></tr><tr><td>Someone has thrown items in the wrong bins. Correct this.</td><td>✕</td><td>√</td><td>0</td></tr><tr><td>Tobi spilt soda on his desk. Throw away the can and take him something to clean with.</td><td>√</td><td>√</td><td>3</td></tr><tr><td>I want to make a sandwich. Place all the ingredients on the lunch table.</td><td>√</td><td>√</td><td>3</td></tr><tr><td>A delegation of project partners is arriving soon. We want to serve them snacks and non-alcoholic drinks. Prepare everything in the largest meeting room. Use items found in the supplies room only.</td><td>√</td><td>√</td><td>2</td></tr><tr><td>Serve bottled water to the attendees who are seated in meeting room 1. Each attendee can only receive a single bottle of water.</td><td>√</td><td>√</td><td>2</td></tr><tr><td>Empty the dishwasher. Place all items in their correct locations.</td><td>√</td><td>√</td><td>2</td></tr><tr><td>Locate all 6 complimentary t-shirts given to the PhD students and place them on the shelf in admin.</td><td>√</td><td>√</td><td>1</td></tr><tr><td>I'm hungry. Bring me an apple from Peter and a Pepsi from Tobi. I'm at the lunch table.</td><td>✕</td><td>✕</td><td>5</td></tr><tr><td>Let's play a prank on Niko. Dimity might have something.</td><td>√</td><td>√</td><td>1</td></tr><tr><td>There is an office which has a cabinet containing a rotten apple. The cabinet name contains an even number. Locate the office, throw away the fruit and get them a fresh apple.</td><td>✕</td><td>✕</td><td>5</td></tr></table>

Table 17: Correctness, Executability and Number of Replanning Iterations for Simple Planning Instructions. Evaluating the performance of SayPlan on each simple planning instruction. Values indicated in red indicate that no executable plan was identified up to that number of iterative replanning steps. In this case, 5 was the maximum number of replanning steps.

Table 18: Correctness, Executability and Number of Replanning Iterations for Long-Horizon Planning Instructions. Evaluating the performance of SayPlan on each long-horizon planning instruction. Values indicated in red indicate that no executable plan was identified up to that number of iterative replanning steps. In this case, 5 was the maximum number of replanning steps.

The full plan sequences generated by SayPlan and all the baseline methods for each of the above instructions are detailed in Table 19. Note the regions highlighted in red indicating the precise action where a plan failed.

\- Full listings of the generated plan sequences for the simple and long-horizon instruction sets are provided on the following pages -

![](Rana2023SayPlan_figs/65c1061a17740643ba1de56941a9c8c18964d48d6ea84492bafa014349ede336.jpg)

![](Rana2023SayPlan_figs/54bfd07515d89d0b82e88a21cee87da89e27a82c11fe0df1cb5b5189074d7893.jpg)

![](Rana2023SayPlan_figs/8f3210264722ac4c486288219eca2346629b135482d143e0aab7165565ffaf63.jpg)

Place Will's drone on his desk.  
![](Rana2023SayPlan_figs/3d6f53113e9fddafef51a4aab99caa8b51d35186054b353f1f2441cf2cd3e3fc.jpg)

Move the monitor from Jason's office to Filipe's.  
![](Rana2023SayPlan_figs/97c258143510832bf2839a8dca0202a92a6f036a4020b9bba303c987d375f5ad.jpg)

My parcel just got delivered! Locate it and place it in the appropriate lab.  
![](Rana2023SayPlan_figs/04185613223e1bf6470207e948acd6c256c949f0b39e41a8f1a7273a41edc0a4.jpg)

Check if the coffee machine is working.  
![](Rana2023SayPlan_figs/550aef08de7b5701ce12b3a743c2b4e1f1c05946d88e1ece641153af52f6247e.jpg)

![](Rana2023SayPlan_figs/a2efedabd88d8b9262e8b504f62ae64975de5e24b244c9903ee918517f176da1.jpg)

Heat up the chicken kebab.  
![](Rana2023SayPlan_figs/dba20f01f748676a25ca9d68642b89e3b8bd486051320229077fcbd7cf12945c.jpg)

Something is smelling in the kitchen. Dispose of it.  
![](Rana2023SayPlan_figs/912bf3c5fb7b24909cabaf9f4498203b73d427788be490d6aa2812cd1cf347d6.jpg)

Throw what the agent is holding in the bin.  
![](Rana2023SayPlan_figs/1cd7f98295db422f2e15ba82b51a25410e0e43277b516d9473c705f68f5e7b22.jpg)

Heat up the noodles in the fridge, and place it somewhere where I can enjoy it.  
![](Rana2023SayPlan_figs/62d0c3a783a869f1d2a5af5e923e83f747ec1dca8ab8cf64df97516fdfa42d55.jpg)

Throw the rotting fruit in Dimity's office in the correct bin.  
![](Rana2023SayPlan_figs/cb92193ee54953a4b59518d146b873e18a1aa47813a0d0ce2ba832e76e893089.jpg)

Wash all the dishes on the lunch table. Once finished, place all the clean cutlery in the drawer.  
![](Rana2023SayPlan_figs/f97616d5adbd333c31dc4eb1d0cdf99602799815ff16f1c5948cb69103a8bc5f.jpg)

Safely file away the freshly printed document in Will's office then place the undergraduate thesis on his desk.  
![](Rana2023SayPlan_figs/736e5f80bdead8255ab4b307c3e63e292eecac2f134b2bbbaf68dfd3cf169d77.jpg)

![](Rana2023SayPlan_figs/54a7289df17254c31e85601ce560ca1e6866e09251daae52e1a6132326065623.jpg)  
Make Niko a coffee and place the mug on his desk.

Tobi spilt soda on his desk. Throw away the can and take him something to clean with.  
![](Rana2023SayPlan_figs/cd08cab14df0efd59d7edf05f32ba3d0295259e78d881ea42942d9b51ef09027.jpg)

I want to make a sandwich. Place all the ingredients on the lunch table.  
![](Rana2023SayPlan_figs/df2de9656cdcf363be9d4117579d08a5663f7b71ce06559d8a974a0f8ac2bcd2.jpg)

Empty the dishwasher. Place all items in their correct locations  
![](Rana2023SayPlan_figs/04b6696617e84e962b4de928989da212cbe60c4366fc88e229b06e0a74ea29bb.jpg)

A delegation of project partners is arriving soon. We want to serve them snacks and non-alcoholic drinks. Prepare everything in the largest meeting room. Use items found in the supplies room only.  
![](Rana2023SayPlan_figs/cc4288615847aad742175a661d2bf565b3e0f1dacde18a8993940a1a2ecad2cb.jpg)

Serve bottled water to the attendees who are seated in meeting room 1. Each attendee can only receive a single bottle of water.  
![](Rana2023SayPlan_figs/e4b18af207f158f0545321e8321c93da965f602bf3fbd042f383393bb863a764.jpg)

Locate all 6 complimentary t-shirts given to the PhD students and place them on the shelf in admin.  
![](Rana2023SayPlan_figs/fac48bf8ea1e27981fcf79c7ce408818340f0af3856586df1877839e148d63a7.jpg)

I'm hungry. Bring me an apple from Peter and a pepsi from Tobi. I'm at the lunch table  
![](Rana2023SayPlan_figs/b12681fff78c8e2b6e5190ac38419f75aa60a59d485f0384bcb2c5a46a13b2dc.jpg)  
Table 19: Causal Planning Evaluation. Task planning action sequences generated for a mobile manipulator robot to follow for both the simple and long-horizon planning instruction sets.

## H Scalability Ablation Study

In this study, we evaluate the ability of SayPlan and the underlying LLM to reason over larger-scale scene graphs. More specifically, as SayPlan’s initial input is a collapsed 3DSG, we explore how increasing the number of nodes in this base environment impacts the ability of the LLM to attend to the relevant parts of the scene graph for both semantic search and iterative replanning.

![](Rana2023SayPlan_figs/b610b4227765053faed798aae6babb22eaa837653b2d5750a9a19c6442f448af.jpg)  
Figure 7: Evaluating the performance of the underlying LLMs semantic search capabilities as the scale of the environment increases. For the office environment used in this study, we are primarily interested in the number of room nodes present in the collapsed form of the 3DSG.

![](Rana2023SayPlan_figs/a05d76abdaece26d92f27a259ef3693280bf77bccb2c557e88f5be680ea19724.jpg)  
Figure 8: Evaluating the performance of SayPlan’s causal planning capabilities as the scale of the environment increases. For the office environment used in this study, we are primarily interested in the number of room nodes present in the collapsed form of the 3DSG.

We note here that all the failures that occurred across both semantic search and iterative replanning were a result of the LLM’s input exceeding the maximum token limits – in the case of GPT-4 this corresponded to 8192 tokens. With regard to the scalability to larger environments, this is an important observation as it indicates that the LLM’s reasoning capabilities or ability to attend to the relevant parts of the 3DSG is not significantly impacted by the presence of ”noisy” or increasing number of nodes. One potential downside to larger environments however is the increased number of steps required before semantic search converges. As more semantically relevant floor or room nodes enter the scene, each one of these may be considered by the LLM for exploration.

![](Rana2023SayPlan_figs/740d22b272199fbbde4026fff11396cadd4540e7dbdeb79426c6103b519a6995.jpg)  
Figure 9: Real World Execution of a Generated Long Horizon Plan. Execution of a generated and validated task plan on a real-world mobile manipulator robot.

## J Input Prompt Structure

Input prompt passed to the LLM for SayPlan. Note that the components highlighted in violet represent static components of the prompt that remain fixed throughout both the semantic search and iterative replanning phases of SayPlan.

```txt
Agent Role: You are an excellent graph planning agent. Given a graph representation of an environment, you can explore the graph by expanding nodes to find the items of interest. You can then use this graph to generate a step-by-step task plan that the agent can follow to solve a given instruction.
Environment Functions:
goto(<pose>): Move the agent to any room node or pose node.
access(<asset>): Provide access to the set of affordances associated with an asset node and its connected objects.
pickup(<object>): Pick up an accessible object from the accessed node.
release(<object>): Release grasped object at an asset node.
turn_on/off(<object>): Toggle object at agent's node, if accessible and has affordance.
open/close(<asset>): Open/close asset at agent's node, affecting object accessibility.
done(): Call when the task is completed.
Environment State:
ontop_of(<asset>): Object is located on <asset>
inside_of(<asset>): Object is located inside <asset>
inside_hand: Object is currently being grasped by the robot/agent closed: Asset can be opened
open: Asset can be closed or kept open
on: Asset is currently on
off: Asset is currently off
accessible: The object is not accessible if it is inside an asset and the asset state is "closed".
Environment API:
expand_node(<node>): Reveal assets/objects connected to a room/floor node.
contract_node(<node>): Hide assets/objects, reducing graph size for memory constraints.
verify_plan(): Verify generated plan in the scene graph environment.
Output Response Format:
{chain_of_thought: break your problem down into a series of intermediate reasoning steps to help you determine your next command,
reasoning: justify why the next action is important
mode: "exploring" OR "planning"
command: {``command_name": Environment API call
    "node_name": node to perform an operation on
    "plan": task plan if in planning mode}}
Example: <see Appendix K and L>
Instruction: Natural language description of the task
3D Scene Graph: Text-serialised JSON description of a 3D scene graph
Memory: History of previously expanded nodes
Feedback: External textual feedback from scene graph simulator
Ensure the response can be parsed by Python json.loads.
```

# K Example Input-Output Interaction Between LLM and Scene Graph Simulator During Semantic Search

```txt
Instruction: make a coffee for Tom and place it in his room
3D Scene Graph: {nodes: {room: {{id: bobs_room}, {id: toms_room}, {id: jacks_room}, {id: kitchen}, {id: livingroom}], pose: {{id: pose1}, {id: pose2}, {id: pose3}, {id: pose4}, {id: pose5}], agent: {{location: bobs_room, id: agent}}}, links: [bobs_room↔pose1, bobs_room↔agent, toms_room↔pose1, toms_room↔pose2, toms_room↔pose5, jacks_room↔pose2, jacks_room↔pose3, kitchen↔pose3, kitchen↔pose4, kitchen↔pose5, livingroom↔pose4]}
Memory: []
SayPlan [Mode->Search]: chain-of-thought: explore graph for coffee mug, coffee machine and somewhere to place the coffee -> perform common sense exploration first -> explore toms room -> explore kitchen -> if items not found then explore other nodes reasoning: i will expand toms room command: expand(toms_room)
Scene Graph Simulator: <Updated 3D scene graph>
Memory: [toms_room]
SayPlan [Mode->Search]: chain-of-thought: i have found a wardrobe in tom's room -> leave this node expanded -> the coffee mug is not in his room -> still have not found the coffee machine -> kitchen might have coffee machine and coffee mug -> explore this node next reasoning: i will expand the kitchen next command: expand(kitchen)
Scene Graph Simulator: <Updated 3D scene graph>
Memory: [toms_room, kitchen]
SayPlan [Mode->Search]: chain-of-thought: i've found the coffee machine in the kitchen -> the coffee mug however is not in the kitchen -> i will explore other unexpanded nodes now for the coffee mug -> jacks room, bobs room and the living room are unexplored yet -> i will try jack"s room next reasoning: i will expand jacks room next command: expand(jacks_room)
Scene Graph Simulator: <Updated 3D scene graph>
Memory: [toms_room, kitchen, jacks_room]
SayPlan [Mode->Search]: chain-of-thought: jacks room does not have anything relevant towards solving this task -> I should contract this node to save token memory -> i will explore other unexplored nodes after doing this reasoning: contract jack's room to save memory command: contract(jacks_room)
Scene Graph Simulator: <Updated 3D scene graph>
Memory: [toms_room, kitchen, jacks_room]
SayPlan [Mode->Search]: chain-of-thought: i have found a wardrobe in tom's room and coffee machine in the kitchen -> the coffee mug is still required for the task -> explore a new room next reasoning: i will expand bob's room as it is unexplored command: expand(bobs_room)
Scene Graph Simulator: <Updated 3D scene graph>
Memory: [toms_room, kitchen, jacks_room, bobs_room]
SayPlan [Mode->Search]: chain-of-thought: i have found the coffee mug, the coffee machine and tom's wardrobe on the graph -> search complete -> I will switch to planning mode-> collect coffee mug -> generate plan for making coffee -> place coffee mug on Tom's wardrobe reasoning: I will generate a task plan using the identified subgraph
```

## L Example Input-Output Interaction Between LLM and Scene Graph Environment During Iterative Replanning

```txt
Instruction: make a coffee for Tom and place it in his room
3D Scene Graph: {nodes: {room: {{id: bobs_room}, {id: toms_room}, {id: jacks_room}, {id: kitchen}, {id: livingroom}], pose: {{id: pose1}, {id: pose2}, {id: pose3}, {id: pose4}, {id: pose5}], agent: {{location: bobs_room, id: agent}], asset: {{room: toms_room, state: free, affordances: [release], id: bed2}, {room: toms_room, state: closed, affordances: [open, close, release], id: wardrobe2}, {room: kitchen, state: closed, affordances: [open, close, release], id: fridge}, {room: kitchen, affordances: [turn_on, turn_off], state: off, id: coffee_machine}, {room: bobs_room, state: free, affordances: [release], id: bed1}, {room: bobs_room, state: closed, affordances: [open, close, release], id: wardrobe1}], object: {{affordances: [pickup], state: inside_of(wardrobel), attributes: "blue", id: coffee_mug}}}, links: [bobs_room↔pose1, bobs_room↔agent, bobs_room↔bed1, bobs_room↔wardrobel, toms_room↔pose1, toms_room↔pose2, toms_room↔pose5, toms_room↔bed2, toms_room↔wardrobe2, jacks_room↔pose2, jacks_room↔pose3, kitchen↔pose3, kitchen↔pose4, kitchen↔pose5, kitchen↔fridge, kitchen↔coffee_machine, livingroom↔pose4, wardrobe1↔coffee_mug}}
Memory: [toms_room, kitchen, jacks_room, bobs_room]
SayPlan [Mode->Planning]: chain-of-thought: "i have found the coffee mug, the coffee machine and tom's wardrobe on the graph -> search complete -> I will switch to planning mode-> collect coffee mug -> generate plan for making coffee -> place coffee mug on Tom's wardrobe"
reasoning: I will generate a task plan using the identified subgraph plan: [goto(bobs_room) > access(wardrobel) > pickup(coffee_mug) > goto(kitchen) > access(coffee_machine) > release(coffee_mug) > turn_on(coffee_machine) > turn_off(coffee_machine) > pickup(coffee_mug) > goto(toms_room) > access(wardrobe2) > release(coffee_mug) > done]
Path Planner:plan: [goto(pose3) > goto(pose4) > goto(pose1) > goto(bobs_room) > access(wardrobel) > pickup(coffee_mug) > goto(pose2) > goto(pose5) > goto(kitchen) > access(coffee_machine) > release(coffee_mug) > turn_on(coffee_machine) > turn_off(coffee_machine) > pickup(coffee_mug) > goto(pose5) > goto(pose2) > goto(toms_room) > access(wardrobe2) > release(coffee_mug) > done]
Scene Graph Simulator (Feedback): "coffee mug is not accessible"
Memory: [toms_room, kitchen, jacks_room, bobs_room]
SayPlan [Mode->Planning]: chain-of-thought: "the coffee mug was not accessible -> the wardrobe it is in is currently closed -> I update the plan to open the wardrobe first -> generate plan for making coffee -> place coffee mug on Tom's wardrobe"
reasoning: I will generate a task plan using the identified subgraph and the feedback from the simulator
plan: [goto(bobs_room) > access(wardrobel) > open(wardrobel) >
pickup(coffee_mug) > goto(kitchen) > access(coffee_machine) >
release(coffee_mug) > turn_on(coffee_machine) > turn_off(coffee_machine) >
pickup(coffee_mug) > goto(toms_room) > access(wardrobe2) >
release(coffee_mug) > done]
Path Planner:plan: [goto(pose3) > goto(pose4) > goto(pose1) >
goto(bobs_room) > access(wardrobel) > open(wardrobel) > pickup(coffee_mug) >
goto(pose2) > goto(pose5) > goto(kitchen) > access(coffee_machine) >
release(coffee_mug) > turn_on(coffee_machine) > turn_off(coffee_machine) >
pickup(coffee_mug) > goto(pose5) > goto(pose2) > goto(toms_room) >
access(wardrobe2) > release(coffee_mug) > done]
Scene Graph Simulator: Plan Verified
```