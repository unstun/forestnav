---
citation_key: Ismayilov2025Decentralized
arxiv_id: 2510.23824
arxiv_url: "https://arxiv.org/abs/2510.23824"
title: "Decentralized Multi-Agent Goal Assignment for Path Planning using Large Language Models"
authors_short: "Murad Ismayilov et al."
year: 2025
direction_tag: H_hierarchical_planning
source: mineru-vlm
converter: mineru-open-api
model: vlm
converted_at: 2026-06-25T09:20:24Z
origin: ai+web
reviewed: false
---

# Decentralized Multi-Agent Goal Assignment for Path Planning using Large Language Models

Murad Ismayilov

Center for Intelligent Machines (CIM) Laboratory

McGill University

Montreal, Canada

Murad.Ismayilov@mail.mcgill.ca

Shuo Wen

Center for Intelligent Machines (CIM) Laboratory

McGill University

Montreal, Canada

Shuo.Wen@mail.mcgill.ca

Edwin Meriaux

Center for Intelligent Machines (CIM) Laboratory

McGill University

Montreal, Canada

Edwin.Meriaux@mail.mcgill.ca

Gregory Dudek

Center for Intelligent Machines (CIM) Laboratory

McGill University

Montreal, Canada

Gregory.Dudek@mcgill.ca

Abstract—Coordinating multiple autonomous agents in shared environments under decentralized conditions is a long-standing challenge in robotics and artificial intelligence. This work addresses the problem of decentralized goal assignment for multiagent path planning, where agents independently generate ranked preferences over goals based on structured representations of the environment, including grid visualizations and scenario data. After this reasoning phase, agents exchange their goal rankings, and assignments are determined by a fixed, deterministic conflictresolution rule (e.g., agent index ordering), without negotiation or iterative coordination. We systematically compare greedy heuristics, optimal assignment, and large language model (LLM)- based agents in fully observable grid-world settings. Our results show that LLM-based agents, when provided with well-designed prompts and relevant quantitative information, can achieve near-optimal makespans and consistently outperform traditional heuristics. These findings underscore the potential of language models for decentralized goal assignment in multi-agent path planning and highlight the importance of information structure in such systems.

Index Terms—multi-agent systems, path planning, goal assignment, large language models, decentralized coordination, gridworld, artificial intelligence

## I. INTRODUCTION

Coordinating the actions of multiple autonomous agents is a fundamental challenge in robotics, logistics, and artificial intelligence, with increasing relevance as multi-agent systems are deployed in real-world applications such as warehouse automation, urban delivery, and disaster response [1]–[4]. In these settings, each agent must select a unique goal or target, plan its movements, and avoid both static obstacles and conflicts with other agents operating in the same environment. Effective assignment and coordination are essential for maximizing system efficiency and avoiding deadlocks or congestion [2].

Centralized approaches to goal assignment and scheduling can, in principle, produce optimal solutions given full knowledge of the environment and control over all agents. However, such methods quickly become computationally infeasible as the number of agents grows or as the system becomes more dynamic and unpredictable [1], [5].

Decentralization has emerged as a practical and scalable alternative in multi-agent systems, allowing each agent to act independently or semi-independently, often with only partial or local information about the environment and the actions of others [3], [5]. Examples include fleets of warehouse robots that must self-assign to pick locations and delivery points, or mobile robots in search-and-rescue operations, where coordination is required under uncertain and dynamic conditions [1], [2].

This work investigates the problem of decentralized goal assignment in fully observable grid-world environments. Each agent is provided with a structured representation of the world, including the grid layout, the positions of all agents, obstacles, goals, and, in some experimental conditions, explicit agent-goal distance tables. Agents independently generate a ranking of goals they prefer to pursue, based on the available information. These rankings are then collected and used to resolve assignment conflicts centrally, ensuring that each goal is assigned to exactly one agent without duplication. Notably, before assignments are finalized, agents also receive information about the provisional choices of other agents, enabling them to reason about potential conflicts and adapt their rankings accordingly.

We compare four categories of agents: a greedy baseline using nearest-goal heuristics, a centralized optimal solver and agents powered by LLMs such as GPT-4.1 and LLaVA [6]. LLM-based agents use structured prompts to process world information and produce their goal preferences.

By systematically evaluating these decentralized goal assignment strategies, this study aims to provide new insight into the relative strengths and limitations of algorithmic and language-based decision-making in multi-agent coordination. The findings inform the design of scalable decentralized systems, highlighting the importance of input structure, conflict resolution, and agent reasoning in collaborative environments.

## II. BACKGROUND

Classical approaches to multi-agent goal assignment have often relied on centralized planning, where a single entity with access to global information computes assignments for all agents. For example, Faigl et al. [7] benchmark several assignment strategies, including greedy assignment to the nearest available goal (implemented centrally to ensure unique assignment), iterative improvement, and the optimal Hungarian method, within the domain of multi-robot exploration. Their results show that methods which account for global path costs typically outperform simpler heuristics, but centralized approaches may face computational and robustness limitations in large or dynamic environments.

To address these challenges, a variety of decentralized and distributed protocols have been proposed. In decentralized settings, agents make assignment decisions using only partial knowledge or local communication, which improves robustness and scalability. Examples include auction-based algorithms, consensus-driven protocols, and hybrid metaheuristics such as the consensus-based decentralized discrete particle swarm optimization method of Tong et al. [8]. These strategies have demonstrated empirical success in reducing makespan and balancing workloads among agents, especially when global knowledge is unavailable or costly to maintain.

In addition to purely algorithmic methods, recent research has explored the use of LLMs as decentralized decisionmakers for multi-robot systems. For instance, Chen et al. [9] evaluate LLM-based planning frameworks in both centralized and decentralized multi-robot collaboration, and report that hybrid approaches leveraging real-time feedback can outperform purely centralized or decentralized strategies.

Recent advances in prompt engineering have had a notable impact on the capabilities of large language models in multiagent coordination and planning. Prompt engineering—the process of carefully designing and refining input queries and instructions for LLMs—has been shown to significantly influence both the reliability and reasoning depth of model outputs, especially for complex decision-making and collaborative tasks. A particularly important development is chainof-thought (CoT) prompting [10], where LLMs are guided to articulate intermediate reasoning steps before arriving at a final answer. CoT techniques have demonstrated substantial improvements in multi-step planning, team-based decisionmaking, and overall LLM performance for both individual and collaborative scenarios [11].

Empirical studies have further established that wellstructured prompts—including scenario descriptions, explicit instructions, reasoning checklists, and clear conflict-resolution rules—are essential for eliciting team-level reasoning and globally efficient assignments [10], [12]. These prompt design elements facilitate transparency, make agent intentions machine-interpretable, and are now considered a core component in LLM-driven multi-agent systems.

This motivates the present study, which seeks to provide a controlled evaluation of decentralized goal assignment protocols, including classical algorithms and LLM-based agents, within a unified grid-world framework.

## III. PROBLEM FORMULATION

The central problem studied in this work is decentralized goal assignment for multiple agents in a fully observable, synchronous grid-world. The objective is to assign each agent to a unique goal location so that the makespan—the number of timesteps required for all agents to reach their assigned goals—is minimized:

$$
\text { Makespan } = \min _ {\pi} \max _ {i = 1, \dots , k} C _ {i} (\pi)\tag{1}
$$

where $C _ { i } ( \pi )$ is the arrival time of agent $a _ { i }$ at its assigned goal under assignment π and a valid set of paths.

In this problem, the algorithms only compute the assignment of agents to goals; that is, each agent is assigned to exactly one goal. Once assignments are determined, each agent takes the shortest path (by number of steps) from its initial position to its assigned goal, computed using a deterministic shortestpath algorithm such as breadth-first search (BFS) [13]. No path optimization or multi-agent path planning is required beyond this assignment step.

Problems that seek to minimize makespan are instances of collaborative optimization, where agents must consider not only their own travel times but also the overall team objective. Optimal assignments often require agents to avoid purely greedy choices and instead select goals that lead to the smallest maximum arrival time across the group.

Each environment consists of:

• A square $N \times N$ grid.

• k agents, each starting from a unique cell.

• k goals, each located in a unique cell.

• A set of obstacles, which are impassable cells that block agent movement.

The grid is represented as a labeled image, with obstacles shown as black squares, goals as labeled red squares (A, B, $\mathrm { C } , \ldots \mathrm { ) }$ , agents as labeled blue circles $( 1 , 2 , 3 , \ldots )$ , and empty cells as uniquely indexed references. Borders and diagonal blockers are also depicted to aid orientation and prevent illegal moves around obstacle corners.

Agents are assumed to have full knowledge of the environment, including the grid layout, the locations of all agents and goals, and the positions of obstacles. The problem constraints are as follows:

• Each goal is assigned to exactly one agent, and vice versa.

• Agents cannot move through obstacles, off the grid, or occupy the same cell at the same time.

• Agents may swap places if they simultaneously attempt to move into each other’s cells.

This formulation provides a unified basis for comparing different decentralized goal assignment strategies under controlled and interpretable conditions.

## A. Illustrative Examples

![](Ismayilov2025Decentralized_figs/c0122692458a53fef151e0e6e6816238f8f50f4c81d422e4478c97511c287aa1.jpg)  
(a) Initial world

![](Ismayilov2025Decentralized_figs/8cca9d7344142b7303668b15dc711072aa3d4c300c2d9027c69c7ddb0121220c.jpg)  
(b) Optimal solution  
Fig. 1: Example 1 (Small World): A 5 × 5 grid with 3 agents, 3 goals (red color), and 2 obstacles (black color).

In Example 1, the initial world configuration (left) shows three agents and three goals in a 5 × 5 grid with 2 obstacles. In this scenario, the greedy strategy (where each agent selects its nearest goal) yields the optimal assignment, as all agents can reach their respective goals along the shortest available routes without conflict. The optimal assignment, shown in the right panel, pairs Agent 1 to Goal B, Agent 2 to Goal A, and Agent 3 to Goal C. Each agent follows its shortest path to its assigned goal. The makespan in this solution—corresponding to Equation 1—is 3 steps, set by Agent 2’s route to Goal A.

![](Ismayilov2025Decentralized_figs/4151dfed1c611aba5aede7357c14c0e9c9b8e919d48b74d3ebc3eee7eecf643a.jpg)  
(a) Initial world

![](Ismayilov2025Decentralized_figs/65d65ebc8f272d5c6a185f2b8910cbf0813cb2d468b4f724cf7a5b92a7e2b253.jpg)  
(b) Optimal solution  
Fig. 2: Example 2 (Difficult World): A 20 × 20 grid with 3 agents, 3 goals, and multiple obstacles.

For Example 2, the environment contains numerous obstacles that block direct paths between agents and goals. Here, the optimal assignment may require assigning agents to non-nearest goals in order to minimize congestion and avoid bottlenecks. The increased complexity and obstacle density make it difficult to identify the optimal solution by inspection, illustrating the challenges faced by decentralized assignment strategies in large, cluttered environments.

## IV. PROPOSED SOLUTION

We propose a decentralized goal assignment protocol for multi-agent systems operating in grid-based environments, leveraging large language models (LLMs) for assignment decision-making. In each scenario, agents receive a structured representation of the environment, consisting of a labeled grid image, the positions of all agents, goals, and obstacles, as well as, in some experiments, an explicit table of agentgoal distances. Based on this input, each agent independently generates a ranked list of goals according to its preferences.

Agents then simultaneously announce their ranked preferences to one another. At this point, all agents have made their decisions in a decentralized manner: no agent communicates during the decision-making process, and they only receive the goal rankings from other agents. Assignment conflicts are resolved according to a predefined agent index order. At initialization, each of the n agents is assigned a unique index in the range 1 to n. In the event of a conflict, the agent with the lowest index receives priority.

## A. Prompt Engineering

The performance of LLM-based agents in decentralized goal assignment relies heavily on the design and structure of their prompts. In our approach, each agent receives a carefully constructed prompt that includes a labeled grid image, a scenario description, the explicit positions of all agents, goals, and obstacles, and, in some experiments, a table of agent-to-goal distances. Each prompt instructs the agent to generate a complete ranking of all goals, with explicit consideration of both team objectives and potential assignment conflicts. Guidelines for deterministic conflict resolution, such as tiebreaking by agent index, are provided to ensure agents can independently compute a consistent and feasible assignment.

A key element of our design is the use of chain-ofthought (CoT) prompting [10], where agents are encouraged to articulate intermediate reasoning steps before producing their final ranking. We employ explicit step-by-step checklists and structured reasoning sections in the prompt to elicit more consistent and globally informed choices from LLM agents [11].

Team-level Reasoning Checklist (excerpt):

1) List every remaining goal and estimate which agent is fastest to reach each one.

2) Draft a full assignment (agents → goals, no duplicates).

3) Compute the assignment’s longest path length.

4) Try at least one alternative assignment; select the one with the smallest maximum path.

5) Try to resolve conflicts in case of ties.

The complete prompt, including the full environment specification, explicit conflict resolution logic, and formatting, is available in our project code<sup>1</sup>.

We systematically evaluate two main prompt variants: one providing the agent-goal distance table, and one omitting this information to assess the LLM’s ability to infer costs based solely on spatial reasoning.

Additionally, our prompt protocols encode provisional assignments (“pseudo-policies”) of other agents at each step, supporting a limited form of indirect, pre-assignment communication—a design inspired by recent advances in collaborative multi-agent LLM prompting [14], [15]. These elements are intended to improve both single-agent accuracy and teamlevel coordination by making agent preferences and intentions explicit and machine-interpretable.

Our empirical results demonstrate how these prompt content and structure choices impact the effectiveness of decentralized LLM agents for multi-agent goal assignment.

## V. METHODOLOGY

Experiments are conducted over 100 randomly generated grid-world scenarios, each consisting of a 20 × 20 grid with 2 to 6 agents and goals. Obstacles are placed uniformly at random, numbering between 15 and 30 per scenario, with care taken to avoid overlap with agents or goals.

To benchmark the LLM-based approach, we include several baseline strategies:

• Greedy Assignment: Agents are assigned to their nearest available goal by BFS distance, with assignment order determined by agent index; assignments are final and nonnegotiated.

• Random Assignment: Agents are matched to goals uniformly at random, subject to unique assignment constraints; navigation proceeds via BFS as in other methods.

In addition, for each scenario, we compute the optimal assignment via brute-force centralized search, yielding the assignment that minimizes the makespan. This provides a ground-truth lower bound for comparison, and all methods are evaluated by their absolute makespan and their performance gap relative to this optimum.

Performance is evaluated using the makespan (see Problem Formulation) and the performance gap, defined as the difference between the makespan of a given method and the optimal assignment.

## VI. RESULTS

Table I reports the mean makespan achieved by each method over all scenarios. The optimal solver provides a lower bound with an average makespan of 13.93. Among LLM-based approaches, GPT-4.1 agents that re-rank goals at each step and receive explicit agent-goal distances achieve the best results, with a mean makespan of 15.12. This is closely followed by the same LLM when ranking only once at the start (15.50). When explicit distance information is removed from the prompt, GPT-4.1 performance declines to 17.67, comparable to the greedy baseline (17.93). Random assignment performs substantially worse (20.54), and the LLaVA-based LLM agent demonstrates the largest gap, with a mean makespan of 27.98.

To analyze how performance scales with team size, Figure 3 plots the mean number of steps above the optimal makespan as a function of the number of agents (the lower the better). In all methods, the performance gap increases with group size, but the rate of increase varies significantly. The best LLM-based agents (GPT-4.1 with distance tables and either once or everystep ranking) remain consistently close to optimal across all scales, while LLMs deprived of distance information, greedy, and random assignment strategies show a more pronounced gap as the number of agents increases. The greedy and “no distance” LLM approaches are nearly indistinguishable for larger agent teams (except for the case with 5-agent worlds), both lagging the best LLM agents by several steps. The random assignment baseline deteriorates most rapidly as agent count grows. We can also see that ranking once strategy seems to scale worse than every-step ranking once based on the results.

TABLE I: Mean makespan (timesteps until all agents reach goals) for each strategy.

<table><tr><td>Agent Type</td><td>Average Makespan</td></tr><tr><td>Optimal</td><td>13.93</td></tr><tr><td>LLM (rank every step, distances shown, GPT-4.1)</td><td>15.12</td></tr><tr><td>LLM (rank once, distances shown, GPT-4.1)</td><td>15.50</td></tr><tr><td>LLM (rank every step, no distances, GPT-4.1)</td><td>17.67</td></tr><tr><td>Greedy</td><td>17.93</td></tr><tr><td>Random Assignment</td><td>20.54</td></tr><tr><td>LLM (rank every step, LLaVA)</td><td>27.98</td></tr></table>

![](Ismayilov2025Decentralized_figs/0aa31a0196710b1aecd55703612890a1931347df2fb68024d15927b06377d4d3.jpg)  
Fig. 3: Performance gap (mean steps above optimal) by number of agents for each method.

These results indicate that the combination of structured world information and explicit agent-goal distances allows LLM-based agents to approximate optimal decentralized assignment even as problem complexity increases. In contrast, heuristic and unstructured methods become less effective in larger, more congested environments.

## VII. DISCUSSION

The results of this study provide several important insights into decentralized goal assignment using LLM-based agents in grid-based environments. As expected, the optimal assignment algorithm establishes the lower bound for makespan, with all other strategies measured against this benchmark.

Among decentralized methods, LLM agents powered by GPT-4.1, given access to explicit agent-goal distance tables and updated rankings at each step, consistently achieved makespans within two steps of the optimal solution across a wide range of scenarios and team sizes. This was, on average, the best performing algorithm. It outperformed the Greedy and Random Assignment baselines, primarily because the LLM agents are able to reason about global team objectives and consider the effects of different assignments on the makespan, rather than simply selecting locally optimal or random matches. In particular, by systematically ranking assignments based on overall team cost and re-evaluating choices at each step, the LLM-based approach avoids common pitfalls of greedy assignment, such as bottlenecking a single agent or forcing suboptimal assignments due to local decisions. This solution maintained robust performance as the number of agents increased, highlighting the ability to scale to more complex coordination tasks. The single-shot ranking strategy with distance information performed only marginally worse, while depriving agents of distance tables led to a marked decline in performance—nearly matching the heuristic greedy baseline. This emphasizes that explicit, quantitative information is critical for effective decentralized assignment when using LLMs.

An analysis by group size further reinforces these findings: only the GPT-4.1 agents with distance information, along with the optimal solver, showed relatively flat scaling as agent count increased. Heuristic, random, and “no-distance” LLM strategies exhibited significantly steeper degradation, suggesting that complex environments amplify the benefits of structured input and repeated reasoning for LLMs.

In contrast, the LLaVA-based agent performed substantially worse than all other methods, with makespans often exceeding even the random assignment baseline as team size grew. This unusually poor result appears to be due in part to LLaVA’s tendency to change its assignment strategy from step to step, leading to frequent shifts in goal selection and a lack of stable, globally consistent plans. On the other hand, GPT-4.1 produced more stable and coherent rankings over time, which contributed to its strong performance.

There are several limitations to the present study. All experiments were conducted in static, fully observable environments with a maximum of six agents and assumed perfect knowledge for assignment conflict resolution. Real-world scenarios may introduce dynamic obstacles, communication constraints, or partial observability that require further adaptation of these protocols. Additionally, LLM agents in this work were restricted to single-stage or per-step assignment and did not participate in navigation or ongoing negotiation.

Despite these constraints, the results demonstrate that, with well-designed prompts and access to quantitative world information, modern language models can serve as competitive decentralized agents for goal assignment.

## VIII. CONCLUSION

This study demonstrates that large language models, when provided with structured prompts and explicit quantitative information, can serve as highly effective decentralized agents for goal assignment in multi-agent grid environments. GPT-4.1-based agents, in particular, achieved makespans close to the optimal solver without centralized planning and consistently outperformed both greedy and random assignment strategies, especially as problem complexity increased.

These results highlight the crucial role of prompt design and input structure in enhancing reasoning capabilities of LLMs for collaborative tasks. Our work provides new benchmarks for language-model-driven coordination and points to promising directions for further integrating LLM-based agents into scalable, decentralized multi-agent systems. Future work should explore larger team sizes, dynamic settings, richer agent communication protocols, and the integration of LLM reasoning into more aspects of multi-agent decision-making.

## REFERENCES

[1] L. Sun, Y. Yang, Q. Duan, Y. Shi, C. Lyu, Y.-C. Chang, C.-T. Lin, and Y. Shen, “Multi-agent coordination across diverse applications: A survey,” arXiv preprint arXiv:2502.14743, 2025.

[2] A. Dahiya, A. M. Aroyo, K. Dautenhahn, and S. L. Smith, “A survey of multi-agent human–robot interaction systems,” Robotics and Autonomous Systems, vol. 161, p. 104335, 2023.

[3] C. A. Groenewald, G. Saha, G. Mann, B. Bhushan, E. Howard, and E. Groenewald, “Multi-agent systems in robotics: coordination and communication using machine learning,” Naturalista Campano, vol. 28, pp. 882–897, 2024.

[4] J. Lundberg and A. Hakansson, “Framework for dynamic life critical˚ situations using agents,” in German Conference on Multiagent System Technologies. Springer, 2009, pp. 214–219.

[5] S. Sudhakara, “Symmetric policy design for multi-agent dispatch coordination in supply chains,” arXiv preprint arXiv:2504.19397, 2025.

[6] H. Liu, C. Li, Q. Wu, and Y. J. Lee, “Visual instruction tuning,” Advances in neural information processing systems, vol. 36, pp. 34 892– 34 916, 2023.

[7] J. Faigl, M. Kulich, and L. Pˇreucil, “Goal assignment using distance costˇ in multi-robot exploration,” in 2012 IEEE/RSJ International Conference on Intelligent Robots and Systems, 2012, pp. 3741–3746.

[8] B. Tong, Q. Liu, and C. Dai, “A decentralized hybrid method for goal assignment in multi-robot exploration,” in 2020 IEEE International Conference on Information Technology,Big Data and Artificial Intelligence (ICIBA), vol. 1, 2020, pp. 238–253.

[9] Y. Chen, J. Arkin, Y. Zhang, N. Roy, and C. Fan, “Scalable multi-robot collaboration with large language models: Centralized or decentralized systems?” in 2024 IEEE International Conference on Robotics and Automation (ICRA), 2024, pp. 4311–4317.

[10] J. Wei, X. Wang, D. Schuurmans, M. Bosma, F. Xia, E. Chi, Q. V. Le, D. Zhou et al., “Chain-of-thought prompting elicits reasoning in large language models,” Advances in neural information processing systems, vol. 35, pp. 24 824–24 837, 2022.

[11] B. Chen, Z. Zhang, N. Langrene, and S. Zhu, “Unleashing the potential´ of prompt engineering for large language models,” Patterns, 2025.

[12] S. M. Bsharat, A. Myrzakhan, and Z. Shen, “Principled instructions are all you need for questioning llama-1/2,” GPT-3.5/4, Tech. Rep., 2024.

[13] A. Bundy and L. Wallen, “Breadth-first search,” in Catalogue of artificial intelligence tools. Springer, 1984, pp. 13–13.

[14] Y. Luo, Y. Tang, C. Shen, Z. Zhou, and B. Dong, “Prompt engineering through the lens of optimal control,” arXiv preprint arXiv:2310.14201, 2023.

[15] S. Agashe, Y. Fan, A. Reyna, and X. E. Wang, “Llm-coordination: evaluating and analyzing multi-agent coordination abilities in large language models,” arXiv preprint arXiv:2310.03903, 2023.