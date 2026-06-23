---
citation_key: Hu2025MapWorld
arxiv_id: 2511.20156
arxiv_url: https://arxiv.org/abs/2511.20156
source: arxiv-e-print
converter: pandoc-3.9 markdown+tex_math_dollars-raw_html-raw_tex
converted_at: 2026-06-23T18:55:26Z
origin: ai+web
reviewed: false
---

# Introduction {#sec:intro}

End-to-end autonomous driving maps raw multi-sensor inputs to future ego trajectories or low-level controls within a single network [@chitta2022transfuser; @li2024law; @hu2023_uniad], building on recent advances in 3D perception, motion forecasting, and online mapping [@polar; @huang2022bevdet; @wang2021detr3d; @li2022bevformer; @shi2023motiontransformer; @liao2023maptr]. This paradigm reduces hand-crafted interfaces and has reached strong performance on several open- and closed-loop benchmarks. Yet a central difficulty remains: in realistic traffic, there are many plausible futures for both the ego vehicle and surrounding agents, and the planner must represent this multi-modality without sacrificing temporal consistency or real-time efficiency.

:::: {#fig:fig1 .figure latex-placement="!"}
![](Hu2025MapWorld_figs/anchor2.png){width="\\linewidth"}

::: caption
Anchor-based selection versus MAP-World. (a) DiffusionDrive generates multi-modal trajectories tied to an anchor set and then selects one as the final plan. (b) MAP-World predicts trajectories directly via masked action planning, without anchors, allowing a broader family of motion modes that better aligns with the ground truth.
:::
::::

Most current systems handle multi-modality through a fixed set of trajectory anchors. The network learns to refine or select from this library [@diffusiondrive; @li2025wote; @zheng2025world4driveendtoendautonomousdriving; @li2024hydra], which stabilizes training and avoids trivial mode collapse. However, anchors discretize the solution space. Important behaviours that depend on subtle interactions or road geometry may fall between anchors, leading to plans that are feasible but misaligned with natural driving and sometimes inconsistent with the observed history. The matching and selection stages also add latency and implementation complexity, and even reduced-anchor designs such as DiffusionDrive [@diffusiondrive] remain constrained by the expressiveness of the anchor set (Fig. [1](#fig:fig1){reference-type="ref" reference="fig:fig1"}).

World-model-based planners aim to improve foresight by predicting how the scene will evolve. Some methods first roll out future BEV states and then regress trajectories from these predictions [@li2024law; @yang2025resim; @zheng2023occworld]; others generate candidates and rely on a learned world model to score or filter them, often with a reinforcement-learning selector [@li2025wote; @zheng2025world4driveendtoendautonomousdriving]. Both families enrich the planner with counterfactual rollouts, but they largely follow a "generate then pick one'' pattern. Only the selected trajectory influences control and supervision, so most of the multi-modal structure is discarded, and selector training introduces additional complexity.

This work asks whether the planner and world model can be coupled in a different way: can we generate multi-modal futures without anchors, keep them consistent with history and intent, and train the world model on the full distribution of plausible paths rather than on a single choice?

We answer this with **MAP-World**, a prior-free multi-modal planning framework that combines masked action planning with path-weighted world-model training. Future ego motion is treated as a masked sequence to be completed: past waypoints are visible tokens, future waypoints are mask tokens, and a driving-intent trajectory provides a coarse scaffold. From this sequence and the BEV scene representation, MAP-World constructs a compact latent planning state. Injecting noise into this state yields multiple trajectory queries that share the same history and intent but diverge in their futures, so multi-modality arises from a learned latent space rather than from an anchor library. A lightweight world model predicts future BEV semantics conditioned on each trajectory, and a trajectory probability head defines a distribution over modes. Training minimizes a semantic loss that is an expectation over trajectories, weighted by their probabilities, so the planner learns from an ensemble of plausible paths while remaining fully differentiable and free of reinforcement learning.

In summary, our contributions are:

- We propose a prior-free multi-modal trajectory generator that formulates planning as masked sequence completion (visible past, masked future, intent scaffold), producing diverse and history-consistent trajectories without anchors or teacher policies.

- We develop a path-weighted world-model objective that supervises an expectation over candidate trajectories using their predicted probabilities as importance weights, enabling end-to-end differentiable training without reinforcement learning or post-hoc selection.

- Extensive experiments show that MAP-World achieves state-of-the-art closed-loop results on NAVSIM and competitive open-loop accuracy on nuScenes, while keeping inference latency compatible with real-time deployment.

# Related Works {#sec:Related}

## End-to-End Autonomous Driving

End-to-end driving maps raw sensor inputs to waypoints or controls within a single model [@centaur; @hu2023_uniad; @li2024law; @yuan2024drama; @sun2024sparsedriveendtoendautonomousdriving]. UniAD [@hu2023_uniad] unifies perception to strengthen planning. VAD [@jiang2023vad] vectorizes agents and HD maps into a compact scene representation, improving planning efficiency. VAD-V2 [@chen2024vadv2] introduces vectorized scene representations and large-vocabulary probabilistic planning for multi-modal trajectories, but offers limited guarantees of diversity and quality. HydraMDP [@li2024hydra] combines imitation and reinforcement learning with a teacher planner, increasing dependence on prior design and training complexity. DiffusionDrive [@diffusiondrive] uses diffusion with anchor trajectories and truncated denoising for real-time inference. MomAD [@song2025momad] injects historical information as trajectory and perceptual momentum into current decisions, mitigating jitter and myopia from weak temporal modeling. Despite these advances [@chen2024vadv2; @diffusiondrive; @li2025wote; @song2025momad; @zheng2025world4driveendtoendautonomousdriving; @liu2025gaussianfusion; @xing2025goalflow; @chai2025anchdrive; @yao2025drivesuprim; @zhang2025perceptionplan], many methods still rely on predefined priors and auxiliary selection modules, which constrain diversity, tie quality to prior design, and increase system overhead.

## World Model in Autonomous Driving

LAW [@li2024law] divides driving world models into image-based approaches [@wang2023drivingwm; @yang2025resim; @hu2023gaia1; @hu2022urban] that generate future images and then plan, and occupancy-based approaches [@zheng2023occworld; @min2024driveworld] that forecast future occupancy and then plan. The former is computation-heavy, and the latter requires high-quality occupancy labels. Both adopt a predict-then-plan pipeline with high latency. LAW instead plans first, then predicts future states conditioned on the plan and supervises them, improving trajectory quality. Building on this idea, WoTE [@li2025wote] pairs BEV features with trajectory anchors and uses RL to select plausible futures, and World4Drive [@zheng2025world4driveendtoendautonomousdriving] extends LAW to multi-modal trajectories via pretrained intent cues,yet both still rely on predefined anchors for multi-modality.

## Masked AutoEncoder in Autonomous Driving

Occupancy-MAE [@min2023occmae] adapts MAE [@MaskedAutoencoders2021] to voxelized LiDAR by masking and reconstructing occupancy, reducing label requirements and improving downstream performance. Traj-MAE [@chen2023trajmae] reconstructs masked histories and HD-map elements to learn interaction-aware features. M-BEV [@chen2023mbev] applies MAE to camera-to-BEV perception via view-occlusion reconstruction. UniM$^{2}$AE [@zou2023unimae] unifies images and LiDAR in a shared 3D volume. And NOMAE [@abdelsamad2025nomae] restricts masking to neighborhoods of occupied voxels for more efficient self-supervised learning. However, these MAE variants primarily reconstruct observed data rather than forecast future states; to our knowledge, this is the first MAE-based extension to a latent world model for autonomous driving.

# Method {#sec:Method}

:::: {#fig:main .figure latex-placement="t!"}
![](Hu2025MapWorld_figs/pipeline.png){width="100%"}

::: caption
Overview of MAP-World. (a) Multi-view images and LiDAR are encoded to obtain the current BEV features. The encoded ego state is fused with the BEV features to form the current state representation. (b) Masked Action Planning generates multi-modal trajectories by applying a Transformer decoder to the current state representation. (c) The BEV world model conditions on the multi-modal trajectories and current BEV features to synthesize future BEV features, which are trained via losses against the BEV semantic map and evaluated under a path-integral formulation.
:::
::::

## Preliminary

**Task formulation.** End-to-end autonomous driving maps raw sensor inputs to a scene representation and, conditioned on this representation, predicts the ego vehicle's future trajectory. The trajectory is represented as a sequence of waypoints$\mathbf{T}_t = \{\mathbf{\tau}_t^1, \mathbf{\tau}_t^2, \ldots, \mathbf{\tau}_t^L\}$, where each waypoint $\mathbf{\tau}_t^i = (x_t^i, y_t^i)$ denotes the predicted BEV position of the ego vehicle at time $t + i$. The horizon $L$ specifies the number of future positions to be predicted.

**World model.** A world model predicts the world features or state at time $t+i$ from those at time $t$. In autonomous driving, such models either condition on current images or BEV features and forecast future visual or BEV representations to guide trajectory planning, or condition on current BEV features together with a predicted trajectory and jointly forecast future BEV features to further improve planning performance.

**Masked autoencoder.** It [@MaskedAutoencoders2021] employs a high masking ratio and reconstructs the masked patches with an asymmetric architecture to learn globally coherent representations. This reconstruction-based pretraining substantially reduces computational cost and improves scalability and transferability.

**Feynman path-integral.** Feynman's path integral formulates quantum evolution as a sum over all spacetime paths satisfying endpoint constraints, with each path contributing to the transition amplitude via a phase weight. Thus "all histories interfere." A compact expression in terms of a path measure and phase weight is: $$\begin{equation}
\begin{aligned}
Z \;&=\; \int \mathcal D\tau \;\exp\!\big(\mathcal A[\tau]\big) \\[4pt]
\mathcal A[\tau] \;&=\; \int \ell\!\big(\tau(s),\tau'(s),t\big)\,dt
\end{aligned}
\label{eq:feynman}
\end{equation}$$ $D\tau$ denotes the path-integral measure, i.e., integration over all admissible paths. $A[\tau]$ denotes the action functional, integrating the Lagrangian over time yields the action. $\tau(s)$ represents a path, and $\tau'(s)$ its derivative with respect to $t$, which can be interpreted as a velocity or rate of change.

## Masked Action Planning

In this section, we plan future trajectories using the historical trajectory and the current BEV state. We first derive an intent trajectory from the current BEV features. Following the MAE paradigm, the historical trajectory is encoded as unmasked latent tokens, while the future trajectory is represented by masked tokens. A conditional generative decoder then reconstructs multi-modal future trajectories from these tokens.

**Driving intention trajectory.** We define a driving-intention trajectory as an initial hypothesis of the ego vehicle's future intent inferred from the current state, serving as a coarse proxy for the downstream route and path geometry. Concretely, we adopt TransFuser[@chitta2022transfuser] as the perception--fusion backbone to integrate camera images and LiDAR into a BEV feature map $F_{bev}$. Following the prior work [@diffusiondrive; @li2025wote; @li2024law], we concatenate these BEV tokens with an ego status embedding $Emb_{ego}$ produced by a dedicated linear layer to obtain current BEV state $F^{cur}_{state}$, and apply learnable queries $Q_{bev}$ with cross-attention over the BEV representation to disentangle ego intention $F_{ego}$ and agent intention $F_{Agent}$ features. Finally, an MLP projects the $F_{ego}$ to a driving-intent trajectory parameterized in the current ego- centric coordinate system. Given the multi-view image $I$ and LiDAR feature $Li$,we can obtain: $$\begin{equation}
\begin{aligned}[c]
F_{bev} &= TransFuser(I,Li) \\
F^{cur}_{state} &= concat(F_{bev}, Emb_{ego}) \\
F_{ego}, F_{Agent} &= CrossAttention(Q_{bev},F^{cur}_{state}) \\
T_{intent} &= MLP(F_{ego})
\end{aligned}
\label{eq:coarse}
\end{equation}$$ We then employ a lightweight BEV semantic decoder to map BEV features into a BEV semantic map used for supervision. In parallel, a separate MLP projects agent representations to agent states $\mathcal{S}_{Agent}$ and computes a loss $\mathcal{L}_{Agent}$ against the agent ground-truth. $$\begin{equation}
\begin{aligned}[c]
\mathcal{B}_{semantic} &= BEVdecoder(F_{bev}) \\
\mathcal{S}_{Agent} &= MLP(F_{Agent})
\end{aligned}
\label{eq:coarse}
\end{equation}$$

**Trajectory decoder.**Given a history of length $T_h$ waypoints $\{\tau_t\}_{t=1}^{T_h},\tau_t \in \mathbb{R}^2$, the module constructs a MAE- style decoder that reconstructs multi-modal future trajectories conditioned on BEV context and auxiliary cues.

The history is augmented with first-order motion cues by concatenating displacements $\Delta\mathbf{\tau}_t=\mathbf{\tau}_t-\mathbf{\tau}_{t-1}$, yielding $[\mathbf{\tau}_t,\Delta\mathbf{\tau}_t]\in\mathbb{R}^4$. An MLP projects each step to a d-dimensional token, and a Transformer encoder produces temporally contextualized history embeddings: $$\begin{equation}
\begin{aligned}[c]
F_{hist} &= \mathrm{MLP}\big([\mathbf{\tau}_1,\Delta\mathbf{\tau}_1],\dots,[\mathbf{\tau}_{T_h},\Delta\mathbf{\tau}_{T_h}]\big)\in\mathbb{R}^{T_h\times d} \\
\mathbf{H}&=\mathrm{Encoder(F_{hist})}
\end{aligned}
\label{eq:hist}
\end{equation}$$ Future steps $T_f$ are represented by learnable mask tokens. The decoder input is formed by concatenating the encoded history tokens with these future mask tokens: $$\begin{equation}
\begin{aligned}[c]
\mathbf{Q_{traj}} = [\mathbf{H}, \mathbf{Mask}] \in \mathbb{R}^{(T_h + T_f)\times d}
\end{aligned}
\label{eq:hist}
\end{equation}$$ To realize multi-modal futures, the sequence $\mathbf{Q_{traj}}$ is compressed across time to $\tilde{q}\in \mathbb{R}^d$ by a fusion MLP and replicated to $K$ mode query $\{\tilde{q}^{(k)}\}_{k=1}^{K}$. Furthermore, per-mode latent noise is mapped and added to induce diverse hypotheses: $$\begin{equation}
\begin{aligned}[c]
\mathbf{q}^{(k)}=\tilde{\mathbf{q}}+\psi(\mathbf{z}^{(k)}),
\mathbf{z}^{(k)}\sim\mathcal{N}(\mathbf{0},\mathbf{I})
\end{aligned}
\label{eq:hist}
\end{equation}$$ The full coordinate sequence $\mathbf{P}\in\mathbb{R}^{(T_h+T_f)\times 2}$ is formed by concatenating history waypoints $\{\tau_t\}_{t=1}^{T_h}$ with a driving intent trajectory $T_{intent}$. For each mode k, the decoder receives the context feature $F_{context} = \{\mathbf{q}^{(k)},\mathbf{P},  F_{bev}, F_{Agent}\}$. Within the trajectory decoder, these conditions are fused via cross-attention.$F_{bev}$ supplies spatial context, $\mathbf{P}$ imposes geometric constraints, and auxiliary signals provide semantic and dynamical priors. The decoder predicts each mode's trajectory as a residual relative to the driving-intent trajectory, thereby refining mode-specific representations and producing the final candidate set $T_{Tf}$ together with the corresponding path probabilities or confidence score $T_{cls}$: $$\begin{equation}
\begin{aligned}[c]
F_{scene}&=TrajDecoder(F_{context}) \\ 
T_{res}, T_{cls} &= RefineModule(F_{scene}) \\
T_{Tf} &= T_{res} + \mathbf{P}
\end{aligned}
\label{eq:hist}
\end{equation}$$ Follow the prior work[@diffusiondrive],the trajectory decoder first interacts with BEV features via deformable spatial cross-attention. The resulting trajectory features then perform cross-attention with the agent feature $F_{Agent}$, followed by a feed-forward network(FFN). A final MLP refinement head estimates the confidence of each trajectory and its offset with respect to the reference path $\mathbf{P}$. The predicted confidence is interpreted as the path weight in the Feynman path--integral formulation and is also used for trajectory selection. We take the trajectory with the highest confidence as the final prediction.

Masked Action Planning encodes the observed history and treats the future as masked targets. A conditional Transformer decoder, conditioned on BEV context, agent tokens, and a coarse intent path, reconstructs the future trajectory. Multi-modality arises from mode queries with latent perturbations, jointly optimizing geometric fidelity and inter-mode separation. The history supplies dynamics priors and boundary conditions, while the masked-sequence formulation enforces temporal consistency and reduces drift. Predicting residuals with respect to the intent trajectory further improves synthesis quality. We use $\ell_1$ loss for trajectories, focal loss for trajectory classification, cross-entropy loss for BEV semantics, and a combination of cross-entropy and $\ell_1$ for agent boxes and labels, aggregated as:

$$\begin{equation}
\begin{aligned}[c]
\mathcal{L}_{e2e} &= \lambda_{traj}\mathcal{L}_{traj}(T_{Tf}, T_{gt})\\ &+\lambda_{agent}\mathcal{L}_{Agent} + \lambda_{semantic}\mathcal{L}_{semantic} \\
&+\lambda_{cls}\mathcal{L}_{cls}
\end{aligned}
\label{eq:losse2e}
\end{equation}$$

## Feynman Path Integral World Model

**Latent world model.** Following prior work [@li2024law; @li2025wote],the latent world model takes as input the current BEV features and a candidate future trajectory, and predicts future BEV features. We also attach an MAE-style masked reconstruction head: learnable mask tokens with positional embeddings are concatenated with the current BEV tokens and decoded into future BEV latents. This decouples current and future representations and biases the model toward generating future semantics rather than copying the present. Compared with directly regressing future BEV features from current BEV and trajectory embeddings, this design yields a clearer optimization objective and reduces interference between geometric reconstruction and temporal extrapolation.

**Path-integral view.** We consider discrete time indices $t=1,\dots,T$ with a history horizon $T_h$ and a prediction horizon $T_f$ so that $T=T_h+T_f$. We condition on the observed history, a driving intention path, and the current BEV state, the conditioning set: $$\mathcal{C}
\;\triangleq\;
\Big\{
\boldsymbol{\tau}_{1:T_h},\;
\mathrm{T_{intent}},\;
F^{\mathrm{cur}}_{\mathrm{state}},\;
F_{\mathrm{Agent}}
\Big\},$$ Integrate only over the *future* degrees of freedom and future trajectory-field representation follows as: $$\Phi
\;\triangleq\;
\Big\{
\boldsymbol{\tau}_{T_h+1:T_h+T_f},\;
\mathcal{B}_{\mathrm{semantic}}^{(T_h+1:T_h+T_f)}
\Big\},$$ The conditional law over future configurations given $\mathcal{C}$ is written as $$\begin{equation}
\begin{aligned}[c]
\mathcal{Z}[\mathcal{C}]
\;&=\;
\int \mathcal{D}\Phi\;
\exp\!\big(-\mathcal{A}[\Phi;\mathcal{C}]\big) \\
\mathcal{D}\Phi
\;&\triangleq\;
\prod_{t=T_h+1}^{T_h+T_f}
\mathrm{d}\boldsymbol{\tau}_{t}\;\mathrm{d}\mathcal{B}_{\mathrm{semantic}}^{(t)}.\\
&\iff T_{cls}
\end{aligned}
\label{eq:conditionlaw}
\end{equation}$$ with the discrete-time action decomposed as $$\begin{equation}
\label{eq:S-discrete-mine-en}
\begin{aligned}[c]
\mathcal{A}[\Phi;\mathcal{C}]
&=
\sum_{t=T_h+1}^{T_h+T_f}
\Big(
\lambda_{\mathrm{bev}}\,
\ell_{\mathrm{bev}}\!\big(\mathcal{B}_{\mathrm{semantic}}^{(t)}\;\big|\;F^{\mathrm{cur}}_{\mathrm{state}}\big)\Big) \\
&+\mathcal{B}[\mathcal{C}], \\
&\iff \mathcal{L}_{wm}(WorldModel(T_{Tf}, F_{bev}))
\end{aligned}
\end{equation}$$ where $\mathcal{B}[\mathcal{C}]$ is a boundary term that enforces the endpoint constraints: $$\begin{equation}
\label{eq:boundary}
\begin{aligned}[c]
\mathcal{B}[\mathcal{C}] = &-\log \delta\!\big(\boldsymbol{\tau}_{1:T_h}-\boldsymbol{\tau}^{\,\mathrm{obs}}_{1:T_h}\big) \;\\&
-\log \delta\!\big(F^{\mathrm{cur}}_{\mathrm{state}}-\mathrm{concat}(F_{bev},Emb_{ego})\big).
\end{aligned}
\end{equation}$$ The boundary term encodes hard endpoint constraints via Dirac deltas, $\delta(\boldsymbol{\tau}_{1:T_h}-\boldsymbol{\tau}^{\mathrm{obs}}_{1:T_h})$ clamps the historical trajectory to observations, and $\delta(F^{\mathrm{cur}}_{\mathrm{state}}-\mathrm{concat}(F_{bev},Emb_{ego}))$ anchors the current BEV state. Expressed as $-\log\delta(\cdot)$, the penalty is zero when satisfied and $+\infty$ otherwise, implying these variables are fixed conditioning rather than optimized degrees of freedom. Note that this term merely indicates that these components do not belong to the future degrees of freedom to be integrated, and it is unrelated to our actual training loss.

In Masked Action Planning, the historical segment is observed, and the$T_f$future steps are represented by learnable mask tokens. In a path-integral view, this specifies boundary conditions (fixed past, integrable future),the mask tokens act as placeholders for future degrees of freedom, whose posteriors are reconstructed by the decoder under the conditioning. The corresponding path weight is the selection probability of each trajectory among the generated multi-modal candidates.Therefore, finally, we can express the Feynman path integral in the world model as follows: $$\begin{equation}
\label{eq:overall-fpi}
\begin{aligned}[c]
\mathcal{Z}[\mathcal{C}]
\;&=\;
\int \mathcal{D}\Phi\;
\exp\!\big(-\mathcal{A}[\Phi;\mathcal{C}]\big) \\
&\iff\sum_{k=1}^KT_{cls}^{k} \mathcal{L}_{wm}(\hat{\mathcal{B}}_{semantic}^{(Tf)}\
,\mathcal{B}_{semantic}^{(Tf)})
\end{aligned}
\end{equation}$$ where $\hat{\mathcal{B}}_{semantic}^{(Tf)}=\textit{WorldModel} (T_{Tf}, F_{bev})$, $\mathcal{B}_{semantic}^{(T_f)}$ means ground-truth semantic map at future time *Tf*. CE loss is also used here for the semantic map. Therefore, the total loss:

$$\begin{equation}
\label{eq:totalloss}
\begin{aligned}[c]
\mathcal{L}_{total} = \mathcal{L}_{e2e} + \lambda_{wm}
\sum_{k=1}^KT_{cls}^{k} \mathcal{L}_{wm}(\hat{\mathcal{B}}_{semantic}^{(Tf)}\
,\mathcal{B}_{semantic}^{(Tf)})
\end{aligned}
\end{equation}$$

# Experiments {#sec:Experiments}

:::: {#fig:main .figure latex-placement="t!"}
![](Hu2025MapWorld_figs/woteVSours.png){width="100%"}

::: caption
Visualization results comparing our method with WoTE. Because our model is not constrained by trajectory anchors and learns from the full set of future features, it trains efficiently and outperforms WoTE across both simple and complex scenes, including challenging edge cases.
:::
::::

:::: table*
::: center
:::
::::

:::: table*
::: center
:::
::::

::: table*
+:-------------------------------------------------+:------------------:+:------------------:+:------------------:+:------------------:+:------------------:+:------------------:+:------------------:+:------------------:+
| Method                                           | **L2** ($m$) $\downarrow$                                                         | **Col. Rate** (%) $\downarrow$                                                    |
|                                                  +--------------------+--------------------+--------------------+--------------------+--------------------+--------------------+--------------------+--------------------+
|                                                  | 1$s$               | 2$s$               | 3$s$               | Avg.               | 1$s$               | 2$s$               | 3$s$               | Avg.               |
+--------------------------------------------------+--------------------+--------------------+--------------------+--------------------+--------------------+--------------------+--------------------+--------------------+
| ST-P3 [@hu2022stp3endtoendvisionbasedautonomous] | 1.33               | 2.11               | 2.90               | 2.11               | 0.23               | 0.62               | 1.27               | 0.71               |
+--------------------------------------------------+--------------------+--------------------+--------------------+--------------------+--------------------+--------------------+--------------------+--------------------+
| BEV-Planner [@li2024bevplanner]                  | 0.28               | **0.42**           | **0.68**           | **0.46**           | 0.04               | 0.37               | 1.07               | 0.49               |
+--------------------------------------------------+--------------------+--------------------+--------------------+--------------------+--------------------+--------------------+--------------------+--------------------+
| LAW [@li2024law]                                 | 0.26               | 0.57               | 1.01               | 0.61               | 0.14               | 0.21               | 0.54               | 0.30               |
+--------------------------------------------------+--------------------+--------------------+--------------------+--------------------+--------------------+--------------------+--------------------+--------------------+
| PARA-Drive [@weng2024paradrive]                  | [0.25]{.underline} | [0.46]{.underline} | [0.74]{.underline} | [0.48]{.underline} | 0.14               | 0.23               | 0.39               | 0.25               |
+--------------------------------------------------+--------------------+--------------------+--------------------+--------------------+--------------------+--------------------+--------------------+--------------------+
| VAD-Base [@jiang2023vad]                         | 0.41               | 0.70               | 1.05               | 0.72               | 0.07               | 0.17               | 0.41               | 0.22               |
+--------------------------------------------------+--------------------+--------------------+--------------------+--------------------+--------------------+--------------------+--------------------+--------------------+
| GenAD [@zheng2024genad]                          | 0.28               | 0.49               | 0.78               | 0.52               | 0.08               | 0.14               | 0.34               | 0.19               |
+--------------------------------------------------+--------------------+--------------------+--------------------+--------------------+--------------------+--------------------+--------------------+--------------------+
| UniAD [@hu2023_uniad]                            | 0.44               | 0.67               | 0.96               | 0.69               | 0.04               | 0.08               | 0.23               | 0.12               |
+--------------------------------------------------+--------------------+--------------------+--------------------+--------------------+--------------------+--------------------+--------------------+--------------------+
| BridgeAD [@zhang2025bridgad]                     | 0.29               | 0.57               | 0.92               | 0.59               | [0.01]{.underline} | [0.05]{.underline} | 0.22               | 0.09               |
+--------------------------------------------------+--------------------+--------------------+--------------------+--------------------+--------------------+--------------------+--------------------+--------------------+
| MomAD [@song2025momad]                           | 0.31               | 0.57               | 0.91               | 0.60               | [0.01]{.underline} | [0.05]{.underline} | 0.22               | 0.09               |
+--------------------------------------------------+--------------------+--------------------+--------------------+--------------------+--------------------+--------------------+--------------------+--------------------+
| DiffusionDrive [@diffusiondrive]                 | 0.27               | 0.54               | 0.90               | 0.57               | 0.03               | [0.05]{.underline} | **0.16**           | [0.08]{.underline} |
+--------------------------------------------------+--------------------+--------------------+--------------------+--------------------+--------------------+--------------------+--------------------+--------------------+
| Map-World (Ours)                                 | **0.22**           | 0.47               | 0.81               | 0.50               | **0.00**           | **0.03**           | [0.18]{.underline} | **0.07**           |
+--------------------------------------------------+--------------------+--------------------+--------------------+--------------------+--------------------+--------------------+--------------------+--------------------+
:::

## Dataset

**NAVSIM.**The Navsim dataset [@Dauner2024navsim] is a planning-oriented benchmark built on OpenScene, a 2 Hz, 120-hour condensation of nuPlan, and is resampled to emphasize challenging, non-trivial scenarios, making ego-status--only fitting insufficient. It provides 360° coverage from eight cameras plus a fused Lidar, with 2 Hz annotations including HD maps and 3D boxes. The dataset is split into Navtrain and Navtest with 1192 train/val and 136 test scenarios.

**NAVSIM metric.** The NAVSIM has two versions of metrics, one is the predictive driver model score (PDMS) [@Dauner2024navsim], a weighted combination of no-accidents at-fault (NC), drivable-area compliance (DAC), time-to-collision (TTC), comfort (Comf.) and ego progress (EP). Another is extended PDMS(EPDMS) [@Cao2025navsimv2], which augments the PDMS score with four additional components: Driving Direction Compliance (DDC), Traffic Light Compliance (TLC), Lane Keeping (LK), and Extended Comfort (EC).

**nuScenes.** The nuScenes [@caesar2020nuscenes] dataset comprises 1000 urban driving scenes, each a 20-second synchronized multi-sensor sequence.This dataset is widely used in autonomous driving. Following the prior work [@jiang2023vad; @sun2024sparsedriveendtoendautonomousdriving; @diffusiondrive], we report the L2 displacement Error and Collision Rate on nuScenes dataset.

## Implementation Details

Following TransFuser and DiffusionDrive, we adopt a ResNet-34 backbone as Visual encoder. Camera inputs are $1024\times256$ pixels. Lidar point clouds cover a $64\text{m}\times 64\text{m}$ area around ego vehicles. We use the TransFuser backbone to produce BEV features, and the world model comprises two Transformer decoder layers. Within the world model, two BEV feature scales from the backbone are used to capture global semantics and local details. Training on Navtrain uses 2×A100-80GB GPUs with a total batch size of 256.We train for 100 epochs with a learning rate of $6e^{-4}$. AdamW [@AdamW] is used as the optimizer for both datasets.

## Comparison with state of the art

**NAVSIM.** On NAVSIM, MAP-World achieves a PDMS of 88.8 on the test set (Table [\[tab:sota_navsim\]](#tab:sota_navsim){reference-type="ref" reference="tab:sota_navsim"}), surpassing all prior systems that rely on trajectory anchors or anchor vocabularies. Compared to world-model-based planners such as World4Drive and WoTE, MAP-World reaches higher PDMS without reinforcement-learning selectors or vision-language models, and improves the EPDMS score to 85.0 (Table [\[tab:navsimv2\]](#tab:navsimv2){reference-type="ref" reference="tab:navsimv2"}). Together with the lower inference latency in Table [\[tab:latency\]](#tab:latency){reference-type="ref" reference="tab:latency"}, this demonstrates that our prior-free multi-modal planning and path-weighted world model yield both better safety metrics and more efficient deployment.

**nuScenes.** On nuScenes, MAP-World also attains strong open-loop planning accuracy (Table [\[tab:nuscenes\]](#tab:nuscenes){reference-type="ref" reference="tab:nuscenes"}). Despite the benchmark's relative simplicity and metrics that are less sensitive to deviations from expert trajectories, our method achieves lower L2 displacement error and collision rate than most prior methods, including DiffusionDrive, while using a smaller number of modes and avoiding anchor designs.

::: table*
   Mask Token   Path Integral   Traj-World     NC $\uparrow$        DAC $\uparrow$       TTC$\uparrow$      Comf.$\uparrow$     EP $\uparrow$       PDMS $\uparrow$
  ------------ --------------- ------------ -------------------- -------------------- -------------------- ----------------- -------------------- --------------------
                                    1        [98.1]{.underline}   [96.7]{.underline}          94.3             **99.9**       [82.8]{.underline}          88.4
                                    1             **98.3**        [96.7]{.underline}   [94.7]{.underline}      **99.9**              82.6                 88.5
                                    4             **98.3**        [96.7]{.underline}        **94.8**           **99.9**              82.3                 88.4
                                    4             **98.3**               96.6                 94.4             **99.9**              82.7                 88.5
                                    8             **98.3**             **96.9**        [94.7]{.underline}      **99.9**              82.6          [88.6]{.underline}
                                    10            **98.3**             **96.9**               94.5             **99.9**            **83.1**             **88.7**
:::

::: table*
           Method           Anchor   #Traj     NC $\uparrow$        DAC $\uparrow$       TTC$\uparrow$      Comf. $\uparrow$     EP $\uparrow$       PDMS $\uparrow$
  ------------------------ -------- ------- -------------------- -------------------- -------------------- ------------------ -------------------- --------------------
         TransFuser                    1            97.7                 92.8                 92.8              **100**               79.2                 84.0
   DiffusionDrive (Extra)              1            97.3                 94.0                 92.6              **100**               79.6                 84.7
       DiffusionDrive                 20     [98.2]{.underline}   [96.2]{.underline}        **94.7**            **100**        [82.2]{.underline}   [88.1]{.underline}
      MAP Only (Ours)                  4          **98.3**             **96.6**        [94.4]{.underline}       **100**             **82.7**             **88.3**
:::

## Ablation study.

**Effect of masked action planning.** Masked action planning is pivotal,removing it causes mode collapse and unrealistic futures. To assess its effect, we drop the path-integral world model and compare with DiffusionDrive [@diffusiondrive] under identical settings and loss weights. As shown in Tab. [\[tab:mode\]](#tab:mode){reference-type="ref" reference="tab:mode"}, DiffusionDrive (Extra) generates a single mode and yields only marginal gains over TransFuser [@chitta2022transfuser], highlighting its reliance on anchors. Our module, by contrast, produces genuine multi-modal trajectories without anchors and surpasses DiffusionDrive even with anchors, confirming its effectiveness.

**Feynman Path Integral world model.** To assess the effectiveness of our Feynman path--integral world model, we conduct an ablation that isolates the entire world-model component. As shown in Tab [\[tab:masktoken\]](#tab:masktoken){reference-type="ref" reference="tab:masktoken"}, when conditioning on a single best trajectory to generate future states, omitting the MAE-style mask tokens yields slightly better results; however, when extending to multi-modal futures, concatenating learnable mask tokens with the current BEV features as queries produces superior performance. Moreover, under the path--integral formulation, performance improves gradually with the number of generated trajectories.

We also observe that mask tokens stabilize training as the number of modes increases, whereas removing them can lead to gradient issues. We cap the number of trajectories at 10, since beyond this point we begin to observe mode collapse in certain cases; this can be mitigated by increasing the noise perturbation in masked action planning (details in the Appendix).

**Different trajectory decoder layers.** As shown in Tab [\[tab:decoder\]](#tab:decoder){reference-type="ref" reference="tab:decoder"}, we varied the depth of the trajectory decoder and found that a 3-layer variant outperforms a 2-layer design. To balance accuracy and real-time latency, we adopt three layers for the trajectory decoder in the final model.

::: center
:::

::: center
:::

# Conclusion {#sec:Con}

This paper presented MAP-World, a prior-free multi-modal planning framework that couples masked action planning with a path-weighted world model for autonomous driving. By viewing planning as masked sequence completion, MAP-World generates diverse, history-consistent trajectories without handcrafted anchors or reinforcement-learning-based selectors. The path-weighted world model then supervises an expectation over candidate futures, so training benefits from the full trajectory distribution instead of a single chosen mode. Experiments on NAVSIM and nuScenes show that MAP-World improves both safety-critical driving metrics and planning accuracy, while keeping inference latency compatible with real-time deployment. A current limitation is the fixed number of trajectory modes and the sensitivity of training to probability weighting; future work will explore scene-adaptive mode allocation and more robust weighting schemes.These will all be the focus of our future work, and further research will be conducted.

**Acknowledgements.** This work was supported by the Science and Technology Development Fund of Macau \[0122/2024/RIB2, 0215/2024/AGJ, 001/2024/SKL\], the Research Services and Knowledge Transfer Office, University of Macau \[SRG2023-00037-IOTSC, MYRG-GRG2024-00284-IOTSC\], the Shenzhen-Hong Kong-Macau Science and Technology Program Category C \[SGDX20230821095159012\], the Science and Technology Planning Project of Guangdong \[2025A0505010016\], National Natural Science Foundation of China \[52572354\], the State Key Lab of Intelligent Transportation System \[2024-B001\], and the Jiangsu Provincial Science and Technology Program \[BZ2024055\].

# Further Ablation study

We conducted further ablation study on the number of BEV states predicted by our world model to investigate how the granularity of prediction time steps affects final performance. This experiment was conducted using two GeForce RTX 3090 GPU with a learning rate of $2 \times 10^{-4}$. As shown in Tab [\[tab:ts\]](#tab:ts){reference-type="ref" reference="tab:ts"}, employing finer, denser time steps to predict future states increased model complexity yet resulted in a marginal decline in overall performance. Specifically, the configuration predicting only the fourth-second BEV achieved higher scores than simultaneously predicting both the 2s and 4s BEVs.

::: center
:::

# Various noise perturbation factors

When the number of generated trajectories reaches ten, the resulting modes become visually entangled and difficult to distinguish. Amplifying the noise perturbation used in masked action planning by different scaling factors can make the multi-modal trajectories more separable in visualization, as shown in Figure [4](#fig:noise){reference-type="ref" reference="fig:noise"}, but it also degrades planning quality, as shown in Tab [\[tab:noise\]](#tab:noise){reference-type="ref" reference="tab:noise"}. This indicates that, although the proposed paradigm is effective, additional research is needed to improve robustness under stronger noise perturbations.Therefore,we do not recommend training with excessively large noise perturbations.

::: center
:::

:::: {#fig:noise .figure latex-placement="t!"}
![](Hu2025MapWorld_figs/noise_perturbations.png){width="100%"}

::: caption
Visualization of trajectories with noise perturbations of different factors.
:::
::::

# Further Model Training Detail

In this section, we compare the data requirements of our approach with those of prior methods. As shown in the Tab [\[tab:sota_qualitative\]](#tab:sota_qualitative){reference-type="ref" reference="tab:sota_qualitative"}, within purely end-to-end planning frameworks, anchor-based methods significantly outperform anchor-free approaches on the NAVSIM test dataset. For world-model--based methods, using additional data beyond standard end-to-end planning inputs is common. For example, WoTE not only utilizes the anchor trajectory but also relies on extra annotations by inserting an ego box into the future BEV semantic map that does not appear in the original dataset to force alignment between the predicted future trajectory and the annotated ego box. This provides a stronger supervisory signal for the BEV world model and enhances its understanding of physical context. In contrast, our method does not use any such additional annotations, with only simple historical trajectory inputs, it surpasses WoTE, further demonstrating the effectiveness of our approach.

:::: table*
::: center
:::
::::

# Further Qualitative Comparison

In this section, we further present qualitative comparisons between our method and WoTE on challenging scenarios from the NAVSIM test dataset.

**Turning right.** The Figure [5](#fig:right){reference-type="ref" reference="fig:right"} shows that, compared with WoTE, MAP-World closely follows the ground-truth trajectory in complex right-turn scenarios while maintaining a high throughput, completing the maneuver more quickly. In contrast, WoTE tends to exhibit pronounced hesitation or produces trajectories with larger turning radii that deviate from typical human expert driving behavior.

**Going straight.** The Figure [6](#fig:straight){reference-type="ref" reference="fig:straight"} shows that, in contrast, MAP-World maintains stable forward motion and robust lane-keeping even on narrow roads and in tight-radius curves, whereas WoTE is more prone to lane departures and shows reduced longitudinal stability in such scenarios.

**Turning left and overtaking.** The Figure [7](#fig:left){reference-type="ref" reference="fig:left"} shows that, in some scenarios, WoTE tends to misinterpret turning intent, for example classifying a left turn as a right turn, which leads to planned trajectories that deviate markedly from the desired route. In overtaking scenarios, when a large vehicle (e.g., a bus) occludes the field of view, WoTE often adopts an overly conservative strategy and fails to initiate an overtake. This behavior is likely due to the scarcity of such cases in the training data, so that the corresponding trajectory patterns are not well represented in the anchor set, making it difficult for the model to learn appropriate decisions for these situations.

:::: {#fig:right .figure latex-placement="t!"}
![](Hu2025MapWorld_figs/right.png){width="100%"}

::: caption
Qualitative comparison of WoTE and Map-World on turning right scenarios of NAVSIM navtest split.
:::
::::

:::: {#fig:straight .figure latex-placement="t!"}
![](Hu2025MapWorld_figs/straight.png){width="100%"}

::: caption
Qualitative comparison of WoTE and Map-World on going straight scenarios of NAVSIM navtest split.
:::
::::

:::: {#fig:left .figure latex-placement="t!"}
![](Hu2025MapWorld_figs/left.png){width="100%"}

::: caption
Qualitative comparison of WoTE and Map-World on turning left and overtaking scenarios of NAVSIM navtest split.
:::
::::
