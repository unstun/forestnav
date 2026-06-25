---
citation_key: Shrestha2020HighLevel
arxiv_id: 2001.02330
arxiv_url: "https://arxiv.org/abs/2001.02330"
title: "High-Level Plan for Behavioral Robot Navigation with Natural Language Directions and R-NET"
authors_short: "Amar Shrestha et al."
year: 2020
direction_tag: G_subgoal_optimization
source: mineru-vlm
converter: mineru-open-api
model: vlm
converted_at: 2026-06-25T09:43:49Z
origin: ai+web
reviewed: false
---

# High-Level Plan for Behavioral Robot Navigation with Natural Language Directions and R-NET

Amar Shrestha<sup>\*</sup>, Krittaphat Pugdeethosapol<sup>\*</sup>, Haowen Fang, Qinru Qiu

Department of Electrical Engineering & Computer Science, Syracuse University, USA {amshrest, kpugdeet, hfang02, qiqiu}@syr.edu

## Abstract

When the navigational environment is known, it can be represented as a graph where landmarks are nodes, the robot behaviors that move from node to node are edges, and the route is a set of behavioral instructions. The route path from source to destination can be viewed as a class of combinatorial optimization problems where the path is a sequential subset from a set of discrete items. The pointer network is an attention-based recurrent network that is suitable for such a task. In this paper, we utilize a modified R-NET with gated attention and self-matching attention translating natural language instructions to a high-level plan for behavioral robot navigation by developing an understanding of the behavioral navigational graph to enable the pointer network to produce a sequence of behaviors representing the path. Tests on the navigation graph dataset show that our model outperforms the state-of-the-art approach for both known and unknown environments.

## Introduction

In a complex but known environment, an automated robot needs to follow a route to reach the destination from a starting point. When the environment is described in terms of a graph (Sepulveda et al. 2018) where landmarks are nodes and the robot behaviors that moves it from one node to its adjacent nodes are edges, the route is a set of behavioral instructions (go left, go right, go forward, etc.). The route path from source to destination can be viewed as a class of combinatorial optimization problems where the path is a sequential subset from a set of discrete items.

Thus, this robot navigation application should take the environment or behavioral graph and the sourcedestination pair along with natural language directions as input and produce a sequence of behavioral instructions to reach the destination from the source. In terms of Neural Program Learning, this can be taken as an example-driven induction (Devlin et al. 2017).

Sequence- to-sequence paradigm of recurrent neural networks (RNNs) have been a staple of neural network architectures for learning functions over sequences (encoder) from examples and producing sequences of outputs (decoder). The content-based attentional mechanism has also been used to provide contextual information from the encoded input to the decoder. But these methods require a fixed-sized output dictionary which is not suitable for combinatorial problems where the size of the output dictionary depends on the length of the input sentence. This problem can be resolved by utilizing Pointer Networks (Vinyals et al. 2015) which augment the attention mechanism to create pointers to the input elements. The augmentation is simple: instead of blending the hidden encoder units using attention to provide context at each decoder step, utilize the attention as a pointer to select a member of the input sequence as the output.

In this work, we utilize the behavioral graph dataset from (Zang et al. 2018). Given the complexity of the problem, we move from the straight-forward sequence-tosequence architecture in the original pointer network in (Vinyals et al. 2015) to a modification of R-Net (Wang et al. 2017) with gated-attention and self-matching attention mechanisms to:

1. Incorporate an understanding of the behavioral graph with the source-destination pair and natural language directions.

2. Aggregate evidence from the entire graph to infer the route from source to destination based on natural language directions.

## Related work

In order for an automated robot to follow a route based on navigation commands to reach the destination, the robot needs to be able to process and understand the natural language direction, as well as translating into plans or commands to execute. The most common approaches can be divided into three categories, manually parsing commands, constraining language descriptions, and statistical machine translation methods (Zang et al. 2018).

![](Shrestha2020HighLevel_figs/aa086379320c826f19e570dd580db777403cceb667ff9b892641b002555df8be.jpg)  
Figure 1. (a) Map of an environment. (b) Its behavioral navigation graph and desired behavioral sequence. (c) Problem setting. The red part of (b) corresponds to the representation of the route highlighted in red in (a). The codes “oo-left”, “cf”, “cf”, and “io-left”, correspond to the behaviors “Exit the room, turn left”, “follow the corridor”, “follow the corridor”, “turn left and enter the room” respectively.

Manually parsing commands is a straight forward method to translate natural language into command, but it is inapplicable in a real-world situation. For example, (Levit and Roy 2007) proposed a method to translate the spatial language to a map navigational task by manually parsing natural language instructions into navigation information units (positions, orientations, moves, turns, and location references) sequence for navigation.

In constraining language descriptions, the space of input descriptions is limited to aid the translation into execution commands. (Schulz et al. 2015) proposed a symbolic navigation system that utilizes symbolic information extracted from door label and map environments to navigate robot from source to destination.

The statistical machine translation is the most recent approach translating the natural language to robot navigation instructions by utilizing translation rules created from a corpus of data. For example, (Matuszek et al. 2010) parse natural language instructions into a grammar liked language sequence by using the word alignment-based semantic parser (Wong and Mooney 2007).

In this work, we mainly focus on end-to-end learning to translate free-from natural language instruction to a highlevel plan for behavioral robot navigation by utilizing a sequence to sequence neural network for natural language processing.

## Experimental Task

## Behavioral Graph

The navigation environment in the dataset (Zang et al. 2018) consists of 7 types of semantic locations, 12 types of behaviors shown in Table 1., and 20 different types of landmarks. A location in the environment can be a room, a lab, an office, a kitchen, a hall, a corridor, or a bathroom. As we require unique sets of elements in the graph and as the behaviors are not unique to its location, we encode the environment into a behavioral graph ? into unique triplets $T _ { l } = < p _ { i } ; b _ { l } ; p _ { j } > _  $ , where $p _ { i }$ and $p _ { j }$ are adjacent nodes in the graph, and the edge $b _ { l }$ is an executable behavior to navigate from $p _ { i }$ to $p _ { j } .$ . In this work, as opposed to (Zang et al. 2018), we remove the landmarks as they do not provide any more information and increases the dimensionality of the behavioral graph.

<table><tr><td>Behavior</td><td>Description</td></tr><tr><td>oo</td><td>Go out of the current place and turn</td></tr><tr><td>io</td><td>Turnand enter the place straight ahead</td></tr><tr><td>oio</td><td>Exit current place and enter straight ahead</td></tr><tr><td>t</td><td>Turnat the intersection</td></tr><tr><td>cf</td><td>Follow (or go straight down) the corridor</td></tr><tr><td>sp</td><td>Go straight at a T intersection</td></tr><tr><td>st</td><td>Go straight through the corridor</td></tr><tr><td>ch</td><td>Cross the hall and turn</td></tr></table>

Table 1: Behaviors (edges) of the navigation graphs considered in this work. The direction <d> can be left or right (Zang et al. 2018).

An example from the dataset and problem sets are shown in Figure 1. (a) shows the environment with the source and destination represented by red and green symbol respectively, and the red line showing the desired path between them which correspond to natural language direction. (b) shows the result behavioral navigation graph and the desired behavior sequence. (c) shows the problem setting where the inputs of the model are a behavioral graph, source-destination pair, and natural language instruction for the target path such as “Exit the room, turn left, follow the corridor, turn left and enter the room”. The dataset consists of 8066 pairs of navigation plans and sourcedestination for training. This training data was collected from 88 unique simulated environments, totaling 6064 distinct navigation plans. The dataset consists of two test sets

![](Shrestha2020HighLevel_figs/5e6cb196a1fd0a4edd71dfbfb2af3eca68950206f4227e55c768a14305387f3d.jpg)  
Figure 2. Modified R-NET Structure with natural language direction.

(1) Test-repeated: This test set contains 1012 pairs of navigation plans and source-destination pair. These routes are not part of the training set; however, they are collected using environments that are part of the training set.

(2) Test-new: This test set contains 946 samples collected using environments that are not part of the training set. In the training set, the largest set of triplets is 500 and the smallest set is 200. Thus, we limit the training set to 300 maximum triplets. The graph with fewer triplets is padded and the graph with more than 300 triplets is cut but ensuring that the target sequence of triplets is included in the 300.

## Problem Formulation

The task in the work is to build a model to extrapolate the path from the source to the destination with natural language direction in a behavioral navigational graph for an indoor environment. We provide the model, sourcedestination triplet pair $( s , d )$ , natural language direction $I ,$ and behavioral navigational graph ?. Formally, we construct a model to predict the correct sequence of triplets to provide the correct sequence of behaviors $( b _ { 1 } , b _ { 2 } , \ldots )$ based on the previously unseen input of $( m , s , d , I )$ . From a supervised learning perspective, the goal is then to estimate:

$$
\underset {T _ {1}, \ldots , T _ {t}} {\text {argmax}} P (T _ {1}, \ldots T _ {t} | m, s, d, I)\tag{1}
$$

From the dataset, the input-output pair is $\left\{ x _ { i } , y _ { i } \right) \mid 0 \leq i \leq$ $N \}$ where $x _ { i } = ( m , s , d , I ) _ { i }$ and $y _ { i } = ( b _ { 1 } , \ldots , b _ { t } ) _ { i } \in$ $( T _ { 1 } , \dots , T _ { t } ) _ { i }$

## Proposed Work

Figure 2. shows the overview of the modified R-NET architecture (Wang et al. 2017) that we utilize in this work. First, the behavioral navigational graph m is processed by a bidirectional recurrent network (BiRNN) (Schuster and Paliwal 1997) to get $u ^ { P }$ . The source-destination triplet pair $( s , d )$ is separately processed by a multilayer perceptron (MLP) with ReLU activation. The natural language direction I is separated into words and embedded using GLOVE embedded vectors (Pennington et al. 2014), then processed by BiRNN to get $e ^ { Q }$ . Second, we concatenate the processed source-destination triple pair with processed natural language direction to get $u ^ { Q }$

$$
u ^ {Q} = c o n c a t \bigl (M L P _ {Q} (s, d), e ^ {Q} \bigr)\tag{2}
$$

Third, we pass $u ^ { P }$ and $u ^ { Q }$ into a gated attention-based recurrent network to incorporate natural language direction and source-destination information into a behavioral navigational graph representation. Then, we refine the graph representation by aggregating the evidence from the whole navigational graph utilizing self-matching attention. This is then fed into the decoder layer with a pointer network containing Gated Recurrent Units (GRU) to produce predictions over the input triplets in the behavioral navigational graph.

The main differences from the original R-NET architecture are in the encoder where we use MLP and BiRNN to produce the new representation $u ^ { Q }$ and the pointer network in the decoder where the initial hidden state $( r ^ { Q } )$ of the BiRNN for the pointer network is determined from the encoding of the encode $u ^ { Q }$ :

$$
r ^ {Q} = M L P (u ^ {Q})\tag{3}
$$

The other parts remaining the same as the original R-NET paper and we use the same notations to ensure that the differences are visible.

## Evaluation

## Training Details

The training procedure used in this is straight-forward. We utilize the entire training set containing 8066 samples for training and the entire test-repeated set containing 1012 samples for validation. The summary of the dataset is shown in Table 2.

<table><tr><td>Dataset</td><td># Single</td><td>#Double</td><td>Total</td></tr><tr><td>Training</td><td>4062</td><td>2002</td><td>8066</td></tr><tr><td>Test-Repeated</td><td>944</td><td>34</td><td>1012</td></tr><tr><td>Test-New</td><td>962</td><td>0</td><td>962</td></tr></table>

Table 2: Statistic of behavioral navigation dataset (Zang et al. 2018). “# Single” indicate the plans with single instruction. “# Double” indicate the plans with double instructions.

We utilize backpropagation with the ADAM optimizer to optimize the network. We also utilize a variational dropout as used in the original R-NET architecture. The evaluations were performed in both test-repeated and test-new set. The model is trained for 45 epochs. The number of units in BiRNN is set to 100 and there are 3 GRU layers in the BiRNN.

## Evaluation metrics

We utilize four metrics to evaluate the model as in (Zang et al. 2018):

Exact Match (EM): If the predicted plan exactly matches the ground truth, the value is 1 and it is 0 otherwise.

F1 score (F1): The harmonic mean of precision and recall.

Edit Distance (ED): The minimum number of changes need to be made in order to transform a predicted sequence to ground truth sequence.

Goal Match (GM): If a predicted sequence reaches the ground truth destination, the value is 1 even it has a different sequence and it is 0 otherwise.

## Results

As shown in Table 3, our model outperforms the original work (Zang et al. 2018) in both test-repeated and test-new set. This is because of modified R-NET, gated-attention and self-matching attention that produce a better understanding of the navigational graph, and pointer network to produce the output behavior sequence by producing a probability over the input graph instead of producing probabilities over the list of behaviors.

We can also see that our model performance does not drop when applying to test-new set compare to (Zang et al. 2018) in which EM and GM significantly drop.

<table><tr><td rowspan="2">Model</td><td colspan="4">Test-Repeated Set</td></tr><tr><td>EM ↑</td><td>F1 ↑</td><td>ED ↓</td><td>GM ↑</td></tr><tr><td>Zang et al.</td><td>61.71</td><td>93.54</td><td>0.75</td><td>61.36</td></tr><tr><td>Our</td><td>72.65</td><td>95.56</td><td>0.31</td><td>85.15</td></tr></table>

<table><tr><td rowspan="2">Model</td><td colspan="4">Test-New Set</td></tr><tr><td>EM ↑</td><td>F1 ↑</td><td>ED ↓</td><td>GM ↑</td></tr><tr><td>Zang et al.</td><td>41.71</td><td>90.22</td><td>1.22</td><td>41.81</td></tr><tr><td>Our</td><td>75.00</td><td>94.61</td><td>0.42</td><td>89.06</td></tr></table>

Table 3: Performance of our models compare to in (Zang et al. 2018) on the test datasets. EM and GM report percentages, and ED corresponds to average edit distance. The symbol ↑ indicates that higher results are better in the corresponding column; ↓ indicates that lower is better.

## Conclusion

In this paper, we utilize the behavioral graph dataset from (Zang et al. 2018) and given the complexity of the problem, we move from the straight-forward sequence-tosequence architecture in the original pointer network to a modification of R-Net with gated attention and selfmatching attention mechanisms. We utilize the graph, natural language direction, and the source-destination triplet pair as inputs to produce a sequence of behaviors.

## References

Devlin, J., Bunel, R.R., Singh, R., Hausknecht, M. and Kohli, P., 2017. Neural program meta-induction. In Advances in Neural Information Processing Systems (pp. 2080-2088).

Levit, M. and Roy, D., 2007. Interpretation of spatial language in a map navigation task. IEEE Transactions on Systems, Man, and Cybernetics, Part B (Cybernetics), 37(3), pp.667-679.

Matuszek, C., Fox, D. and Koscher, K., 2010, March. Following directions using statistical machine translation. In 2010 5th ACM/IEEE International Conference on Human-Robot Interaction (HRI) (pp. 251-258). IEEE.

Pennington, J., Socher, R. and Manning, C., 2014, October. Glove: Global vectors for word representation. In Proceedings of the 2014 conference on empirical methods in natural language processing (EMNLP) (pp. 1532-1543).

Schulz, R., Talbot, B., Lam, O., Dayoub, F., Corke, P., Upcroft, B. and Wyeth, G., 2015, May. Robot navigation using human cues: A robot navigation system for symbolic goal-directed exploration. In 2015 IEEE International Conference on Robotics and Automation (ICRA) (pp. 1100-1105). IEEE.

Schuster, M. and Paliwal, K.K., 1997. Bidirectional recurrent neural networks. IEEE Transactions on Signal Processing, 45(11), pp.2673-2681.

Sepulveda, G., Niebles, J.C. and Soto, A., 2018, May. A deep learning based behavioral approach to indoor autonomous navigation. In 2018 IEEE International Conference on Robotics and Automation (ICRA) (pp. 4646-4653). IEEE.

Vinyals, O., Fortunato, M. and Jaitly, N., 2015. Pointer networks. In Advances in Neural Information Processing Systems (pp. 2692-2700).

Wang, W., Yang, N., Wei, F., Chang, B. and Zhou, M., 2017, July. Gated self-matching networks for reading comprehension and question answering. In Proceedings of the 55th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers) (pp. 189-198).

Wong, Y.W. and Mooney, R.J., 2006, June. Learning for semantic parsing with statistical machine translation. In Proceedings of the main conference on Human Language Technology Conference of the North American Chapter of the Association of Computational Linguistics (pp. 439-446). Association for Computational Linguistics.

Zang, X., Pokle, A., Vázquez, M., Chen, K., Niebles, J.C., Soto, A. and Savarese, S., 2018. Translating Navigation Instructions in Natural Language to a High-Level Plan for Behavioral Robot Navigation. arXiv preprint arXiv:1810.00663.