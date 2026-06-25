---
citation_key: Faroni2024Online
arxiv_id: 2403.07638
arxiv_url: https://arxiv.org/abs/2403.07638
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-24T15:36:20Z
origin: ai+web
reviewed: false
---

# Associate Editor {#associate-editor .unnumbered}

There is agreement that this paper is technically sound, and makes a novel and well-motivated contribution that advances the state of the art. However, the reviewers have also noted several ways in which the paper can be strengthened, including better-justifying key design decisions. Please review their comments carefully.

The video provides helpful visualizations of the proposed framework and is a useful addition to the submission.

# Reviewer 1 {#reviewer-1 .unnumbered}

This paper considers the problem of robot manipulation in the case of inaccurate models, given an estimate of model errors. The paper provides a heuristic method to correct for inaccuracies with the MDE function found during execution, by adapting the cost function and sampling distribution of a sampling-based motion planning algorithm. A manipulation-specific context-based transition similarity measure is proposed as part of this adaptive cost function. The adapted cost function is used during replanning to correct the planning strategy towards trajectories that avoid unrealiable motions. Results on a few case studies show that the proposed approach improves success rate and has lower number of replannings compared to baseline algorithms.

The paper poses an important problem where the planning dynamics is different from the true dynamics, but only an estimate of the deviation is given. The paper proposes an interesting solution, where the cost function and sampling is skewed away from \"unreliable\" transitions. Overall, the paper is well written and proposes a good solution.

The experiments are well formulated, with ablation studies on the two main aspects of the proposed algorithm. Results are very promising for the case studies considered. However, I have questions about the generality of the proposed approach to non-manipulation domains, and justifications for aspects of the proposed approach is unclear.

Major Questions/Comments:

1\. It is not clear why minimizing the MDE function for the initial solution is the best method. One would think a solution that is robust to model deviation would be more optimal. For example, consider two paths; one path has low MDE but is very close to obstacles, whereas another path has higher MDE but is far away from obstacles. Then, replanning with the updated cost function as discussed in the paper might produce a better overall execution behavior. A stronger justification for this step would make the approach more convincing.

\- how would a robust policy perform in the experiments?

[Robust policy can avoid areas with uncertain MDE values, but it would not be able to update the MDE estimate online. The main advantage of our approach is that it updates the cost function online according to the observed error and context. ]{style="color: verde"}\
2. What are the theoretical properties of the proposed algorthm? The algorithm uses MAB-RRT \[18\]. From \[18\], MAB-RRT is not proven to be asymptotically optimal, even though empirical results does suggest that. Since the proposed method uses an adaptive cost function during replanning, there is an implicit assumption that the replanning algorithm is able to optimize for lower cost paths. This is difficult to say in general for MAB-RRT.

[ I don't think asymptotic optimality is key considering that the cost function is inaccurate and the system will probably require re-planning. Perhaps it is more interesting to understand if the cost function converges to the true error, but we did not investigate it. ]{style="color: verde"}\
3. As it stands, the algorithm makes sense but it is difficult to tell if this is the best way to solve the problem considered, since there is not enough justification (or discussion) for each design decision. This is especially evident in the context-based transition similarity which may only work for well for the considered cases in the paper. This is already mentioned in the conclusion section, but is a limitation of the paper.

[I agree the definition of context similarity is quite case-dependent.]{style="color: verde"}\
4. Why would the simpler solution of updating the MDE function not work better than the proposed solution of updating the adaptive cost function?

[I don't see how I can update the MDE function online. If it is a neural network, I should re-train it, if it is analytical, I should update the parameters (not straightforward).]{style="color: verde"}\
5. The paper title is misleading. I believe the paper is specifically for the case of robotic manipulation and similar domains (e.g. the assumption that there is a safety stop, collisions are not catastrophic, the context-based transition similarity is defined for manipulation domains).

Current title: Online Adaptation of Sampling-Based Motion Planning with Inaccurate Models

[Comments?]{style="color: verde"}\
Comments on the Video Attachment:

The video shows the general approach and some case studies. A narration would be helpful.

[I can do it.]{style="color: verde"}\

# Reviewer 2 {#reviewer-2 .unnumbered}

The motivation behind this work is really nice. Offline models only match real-world so well, and there needs to be a way to compensate that. Moreover, the function describing this compensation realistically varies based on context. Adapting components in the cost function whenever its error reaches a threshold and using that to re-plan is a very intuitive idea and this work presents a simple framework for doing so.

That being said, the example demonstrations could be more compelling even though this is just an initial work. In your examples, it doesn't seem as if the contexts and the model mismatch are well-coupled. For example, in Fig. 2 it is shown that there are more anomalies in the prediction model when it is near an obstacle. However, the obstacle itself isn't the cause of the actual drift that is causing the error. Rather, the error comes from the fact that the robot stops at an obstacle when it should ideally be following the path. If the obstacle is taken away, there are still two areas with different amounts of drift that would be mapped to the same context in this method. The same issue is present in scenario B, where obstacles exist in all sections of drifts. This only allows you to demonstrate that the planner will become more conservative with obstacles and doesn't really show any adaptation with respect to the drift zones.

[The result in the specific case is that the planner becomes more conservative with obstacles, but the approach is more general as long as it is provided with a context-similarity metric and the execution has "drift".]{style="color: verde"}\
One way to address this could maybe be to keep the problem simple and incorporate location into the context as well. Then you could show that the planner avoids certain regions of the map since its model is not as accurate in those regions.

[Makes sense, but in our examples it did not help much.]{style="color: verde"}\
Comments on the Video Attachment:

Adding audio would be nice, especially during the segments where you show video demos. The text slides were too fast paced.
