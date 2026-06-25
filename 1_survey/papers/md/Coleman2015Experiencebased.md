---
citation_key: Coleman2015Experiencebased
arxiv_id: 1510.08636
arxiv_url: "https://arxiv.org/abs/1510.08636"
title: "Experience-based Planning with Sparse Roadmap Spanners"
authors_short: "Coleman et al."
year: 2015
direction_tag: N_path_repair
source: mineru-vlm
converter: mineru-open-api
model: vlm
converted_at: 2026-06-25T09:57:39Z
origin: ai+web
reviewed: false
---

# <sup>Z Z</sup> [<sup>u</sup>]-additive codes<sup>∗</sup>

Zhenliang Lu, Shixin Zhu

Department of Mathematics, Hefei University of Technology, Hefei 230009, Anhui, P.R.China

Abstract: In this paper, we study <sup>Z Z</sup> [u]-additive codes, where $p$ is prime and ${ u ^ { 2 } = 0 }$ . In particular, we determine a Gray map from $\mathbb { Z } _ { p } \mathbb { Z } _ { p } [ u ]$ to $\mathbb { Z } _ { p } ^ { \alpha + 2 \beta }$ and study generator and parity check matrices for these codes. We prove that a Gray map Φ is a distance preserving map from $( \mathbb { Z } _ { p } \mathbb { Z } _ { p } [ u ]$ ,Gray distance) to $( \mathbb { Z } _ { p } ^ { \alpha + 2 \beta }$ ,Hamming distance), it is a weight preserving map as well. Furthermore we study the structure of $\mathbb { Z } _ { p } \mathbb { Z } _ { p } [ u ]$ -additive cyclic codes.

Keywords:additive codes; $\mathbb { Z } _ { p } \mathbb { Z } _ { p } [ u ]$ -additive codes; $\mathbb { Z } _ { p } \mathbb { Z } _ { p } [ u ]$ -additive cyclic codes; Gray map.

## 1 Introduction

Additive codes with the remarkable paper by Delsarte in 1973[1], he defines additive codes as subgroups of the underlying abelian group in a translation association scheme. In 2006, Borges J. et al. define an extension of the usual Gray map, the new Gray map is an isometry which transforms Lee distance in $Z _ { 2 } ^ { \alpha } \times Z _ { 4 } ^ { \beta }$ to Hamming distance in $Z _ { 2 } ^ { \dot { \alpha } + 2 \beta } [ 6 ]$ . Then, many properties of additive codes are studied. Two kinds of maximum distance separable codes over $Z _ { 2 } Z _ { 4 }$ are studied $[ 7 ]$ , all MDS $Z _ { 2 } Z _ { 4 } .$ -additive codes are zero or one error-correcting codes with the exception of the trivial repetition codes containing two codewords. Cyclic additive codes are also studied[8][15]. Recently, $Z _ { 2 } Z _ { 4 }$ -additive codes were generalized to $Z _ { 2 } Z _ { 2 ^ { s } }$ -additive codes by Aydogdu and Siap[9]. And next $Z _ { p ^ { r } } Z _ { p ^ { s } }$ -additive codes are studied by Aydogdu and Siap[4]. In [4], the paper given the standard generator matrices and dual matrices of the form over $Z _ { p ^ { r } } Z _ { p ^ { s } }$ -additive codes.

Later, in [3], a generalization towards another direction that have a good algebraic structure and provide good binary codes is presented, a new class of additive codes which is referred to as $Z _ { 2 } Z _ { 2 } [ u ]$ ]-additive codes is introduced. About the application of additive codes to steganography is proposed[10] and lt’s also helped to study quantum code. Now, quantum additive code is a new research direction. Many articles and research has been done on quantum additive codes. In this paper, we extend the $Z _ { 2 } Z _ { 2 } [ u ]$ -additive codes to codes over $\mathbb { Z } _ { p } \mathbb { Z } _ { p } [ u ]$ ,where $p$ is prime and $u ^ { 2 } = 0$ . Corresponding, we given a more simplify standard generator matrices and dual matrices of the form. At the same time, we define a Gray map Φ. We prove that a Gray map Φ is a distance preserving map from $( \mathbb { Z } _ { p } \mathbb { Z } _ { p } [ u ]$ ,Gray distance) to $( \mathbb { Z } _ { p } ^ { \alpha + 2 \beta }$ ,Hamming distance), it is a weight preserving map as well. At the end of the paper, we study the structure of $\mathbb { Z } _ { p } \mathbb { Z } _ { p } [ u ] .$ additive cyclic codes.

## 2 Preliminaries

Let $\mathbb { Z } _ { p }$ be a finite filed with p elements, where p is an odd prime. Let R be the commutative ring $\mathbb { Z } _ { p } + u \mathbb { Z } _ { p } = \{ a + u b \mid a , b \in \mathbb { Z } _ { p } \}$ where ${ u ^ { 2 } } = 0$ . A linear code $C$ over R containing some nonzero codewords is permutation equivalent to a code with a generator matrix of the form

$$
G = \left( \begin{array}{c c c} I _ {k _ {0}} & A & B \\ 0 & u I _ {k _ {1}} & u D \end{array} \right),
$$

where $A , D$ are $p { \mathrm { - a r y } }$ matrices, B is $\mathbb { Z } _ { p } + u \mathbb { Z } _ { p }$ -matrices, $I _ { k _ { 0 } }$ and $I _ { k _ { 1 } }$ denote the $k _ { 0 } \times k _ { 0 }$ and $k _ { 1 } \times k _ { 1 }$ identity matrices, and $C$ contains $p ^ { 2 k _ { 0 } + k _ { 1 } }$ codewords[2].

We define a Gray map ψ from R to $Z _ { p } ^ { 2 }$ in the following way.

$$
\begin{array}{c} \psi : R \to Z _ {p} ^ {2} \\ (a + u b) \to (b, a + b). \end{array}
$$

The set $\mathbb { Z } _ { p } \mathbb { Z } _ { p } [ u ]$ is defined by

$$
\mathbb {Z} _ {p} \mathbb {Z} _ {p} [ u ] = \{(a, b) | a \in \mathbb {Z} _ {p} a n d b \in R \}
$$

The set not well defined with respect to the usual multiplication, therefore, to make it well defined and get some good results, we introduce a new scalar multiplication in the following way:

$$
(1) \forall c _ {1} = (a _ {0}, a _ {1}, \dots , a _ {\alpha - 1}, b _ {0}, b _ {1}, \dots , b _ {\beta - 1}), c _ {2} = (a _ {0} ^ {\prime}, a _ {1} ^ {\prime}, \dots , a _ {\alpha - 1} ^ {\prime}, b _ {0} ^ {\prime}, b _ {1} ^ {\prime}, \dots , b _ {\beta - 1} ^ {\prime}) \in \mathbb {Z} _ {p} \mathbb {Z} _ {p} [ u ]
$$

$$
c _ {1} c _ {2} = (a _ {0} a _ {0} ^ {\prime}, a _ {1} a _ {1} ^ {\prime}, \dots , a _ {\alpha - 1} a _ {\alpha - 1} ^ {\prime}, b _ {0} b _ {0} ^ {\prime}, b _ {1} b _ {1} ^ {\prime}, \dots , b _ {\beta - 1} b _ {\beta - 1} ^ {\prime})
$$

$$
(2) \forall c _ {1} = (a _ {0}, a _ {1}, \dots , a _ {\alpha - 1}, b _ {0}, b _ {1}, \dots , b _ {\beta - 1}) \in \mathbb {Z} _ {p} \mathbb {Z} _ {p} [ u ], c = r + q u \in R.
$$

$$
c c _ {1} = (r a _ {0}, r a _ {1}, \dots , r a _ {\alpha - 1}, c b _ {0}, c b _ {1}, \dots , c b _ {\beta - 1})
$$

$$
(3) \forall c _ {1} = (a _ {0}, a _ {1}, \dots , a _ {\alpha - 1}, b _ {0}, b _ {1}, \dots , b _ {\beta - 1}) \in \mathbb {Z} _ {p} \mathbb {Z} _ {p} [ u ], c \in \mathbb {Z} _ {p}.
$$

$$
c c _ {1} = \left(c a _ {0}, c a _ {1}, \dots , c a _ {\alpha - 1}, c b _ {0}, c b _ {1}, \dots , c b _ {\beta - 1}\right)
$$

## 3 $\mathbb { Z } _ { p } \mathbb { Z } _ { p } [ u ] .$ -additive codes

In this section, we introduced the definition of the additive codes and the additive dual codes, determine the structure of the generator matrix and dual generator matrix in the standard form of the code.

Definition 3.1.A linear code C is called a $\mathbb { Z } _ { p } \mathbb { Z } _ { p } [ u ]$ additive code if it is a $\mathbb { Z } _ { p } + \mathbb { Z } _ { p } [ u ]$ submodule of $\mathbb { Z } _ { p } ^ { \alpha } \times \mathbb { Z } _ { p } [ u ] ^ { \beta }$ with respect to the scalar multiplication defined in $( 1 ) , ( 2 ) , ( 3 )$ . Then the p-ary image $\boldsymbol { \Phi } ( \boldsymbol { \bar { C } } ) = \mathbf { C }$ is called $\mathbb { Z } _ { p } \mathbb { Z } _ { p } [ u ]$ linear code of length $n = \alpha + 2 \beta$ where Φ is a map from $\mathbb { Z } _ { p } ^ { \alpha } \times \mathbb { Z } _ { p } [ u ] ^ { \beta }$ to $\mathbb { Z } _ { p } ^ { n }$ defined as

$$
\Phi (a, b) = \left(a _ {0}, a _ {1}, \dots , a _ {\alpha - 1}, \psi \left(b _ {0}\right), \psi \left(b _ {1}\right), \dots , \psi \left(b _ {\beta - 1}\right)\right)
$$

for all a = (a<sub>0</sub>, a<sub>1</sub>, · · · , a<sub>α</sub>−<sub>1</sub>) ∈ <sup>Zα</sup><sub>p</sub> , b = (b<sub>0</sub>, b<sub>1</sub>, · · · , b<sub>β</sub>−<sub>1</sub>) ∈ <sup>Z</sup><sub>p</sub>[u]<sup>β</sup>.

Theorem 3.2. Let C be a $\mathbb { Z } _ { p } \mathbb { Z } _ { p } [ u ]$ ]-additive code of type $\left( p ; \alpha , \beta ; k _ { 0 } , k _ { 1 } \right)$ . Then $C$ is permutation equivalent to a $\mathbb { Z } _ { p } \mathbb { Z } _ { p } [ u ]$ additive code with the standard form matrix

$$
G = \left( \begin{array}{c c c} I _ {k _ {0}} & A & B \\ 0 & u I _ {k _ {1}} & u D \end{array} \right),\tag{1}
$$

where $A , B , D$ are R-matrices, $J _ { k _ { 0 } }$ and $I _ { k _ { 1 } }$ denote the $k _ { 0 } \times k _ { 0 }$ and $k _ { 1 } \times k _ { 1 }$ identity matrices.

P roof Since the $\mathbb { Z } _ { p } \mathbb { Z } _ { p } [ u ]$ additive codes front part is $\mathbb { Z } _ { p } ^ { \alpha }$ ,so the $\mathbb { Z } _ { p } \mathbb { Z } _ { p } [ u ]$ additive codes can be generated by a matrix as follow:

$$
\left( \begin{array}{c c} I _ {k _ {0}} & S _ {1} \end{array} \right),
$$

where S are $Z _ { P } \mathrm { - m a t r i x }$

Likewise, the $\mathbb { Z } _ { p } \mathbb { Z } _ { p } [ u ]$ additive codes after part is $\mathbb { Z } _ { p } + u \mathbb { Z } _ { p } ,$ , so the $\mathbb { Z } _ { p } \mathbb { Z } _ { p } [ u ]$ additive codes can be generated by a matrix as follow:

$$
\left( \begin{array}{c c c c} S _ {2} & I _ {k _ {1}} & A _ {1} & A _ {2} \\ S _ {3} & 0 & u I _ {k _ {2}} & u A _ {3} \end{array} \right),
$$

where $S _ { 2 } , S _ { 3 } , A _ { 1 } , A _ { 2 } , A _ { 3 }$ are Z<sub>P</sub> -matrices. $I _ { k _ { 1 } } , I _ { k _ { 2 } }$ is identity matrices.

According to generator matrices theorem,we know the matrices

$$
\left( \begin{array}{c c c c} I _ {k _ {0}} & S _ {1 1} & S _ {1 2} & S _ {1 3} \\ S _ {2} & I _ {k _ {1}} & A _ {1} & A _ {2} \\ S _ {3} & 0 & u I _ {k _ {2}} & u A _ {3} \end{array} \right),
$$

is also generate the additive codes,where $S _ { 1 } { = } S _ { 1 1 } + S _ { 1 2 } + S _ { 1 3 }$

Next by applying necessary row and column oprations to the above matrix,we obtain

$$
\left( \begin{array}{c c c c} I _ {k _ {0}} & 0 & S _ {1 2} ^ {\prime} & S _ {1 3} ^ {\prime} \\ 0 & I _ {k _ {1 1}} & A _ {1} ^ {\prime} & A _ {2} ^ {\prime} \\ 0 & 0 & u I _ {k _ {2 2}} & u A _ {3} ^ {\prime} \end{array} \right),
$$

Let $k _ { 0 } ^ { ' } { = } k _ { 1 } { + } k _ { 1 1 }$ ,we can obtain the matrices

$$
G = \left( \begin{array}{c c c} I _ {k _ {0} ^ {\prime}} & A & B \\ 0 & u I _ {k _ {1}} & u D \end{array} \right),
$$

Finally,Let $k _ { 0 } ^ { ' } = k _ { 0 }$ ,we reach to the claimed form.

□

The inner product for the vectors v, w $\in \mathbb { Z } _ { p } \mathbb { Z } _ { p } [ u ]$ is defined by

$$
v \cdot w = u (\sum_ {i = 1} ^ {\alpha} v _ {i} w _ {i}) + \sum_ {j = \alpha + 1} ^ {\alpha + \beta} v _ {j} w _ {j} \in Z _ {p} + u Z _ {p}
$$

Definition 3.3.Let C be a $\mathbb { Z } _ { p } \mathbb { Z } _ { p } [ u ]$ -additive code,The additive dual code of C,denote by $C ^ { \perp }$ and

$$
C ^ {\perp} = \{w \in \mathbb {Z} _ {p} ^ {\alpha} \times \mathbb {Z} _ {p} [ u ] ^ {\beta} \mid v \cdot w = 0 f o r a l l v \in C \}.
$$

Theorem 3.4.Let $C$ be a $\mathbb { Z } _ { p } \mathbb { Z } _ { p }$ [u] additive code of type $( p ; \alpha , \beta ; k _ { 0 } , k _ { 1 } )$ with the standard form matrix defined in Equation (1),Then the generator matrix for the additive dual code $C ^ { \perp }$ is given by

$$
H = \left( \begin{array}{c c c} - B ^ {t} + D ^ {t} A ^ {t} & - D ^ {t} & I _ {n - k _ {0} - k _ {1}} \\ u A ^ {t} & - u I _ {k _ {1}} & 0 \end{array} \right),\tag{2}
$$

P roof Denote the code with generator matrix (2) by $C ^ { ' }$ . Since $H G ^ { ' } = 0$ , clearly $C ^ { ' } \in C ^ { \perp }$ Let $c = ( c _ { 1 } , c _ { 2 } , \cdot \cdot \cdot , c _ { n } ) \in C ^ { \bot }$ . After adding a linear combination of the first $n - k _ { 0 } - k _ { 1 }$ row of (2) to $\mathrm { c } ,$ we obtain a codeword is of the form

$$
c ^ {\prime} = \left(c _ {1}, c _ {2}, \dots , c _ {k _ {0}}, c _ {k _ {0} + 1}, \dots , c _ {k _ {0} + k _ {1}}, 0, \dots , 0\right) \in C ^ {\perp}
$$

Since $c ^ { ' }$ is orthogonal to the last $k _ { 1 }$ rows of $( 1 ) , \mathrm { { s o } }$ we can adding a certain linear combination of the last $k _ { 1 }$ row of (2) to $c ^ { ' }$ . Similar, we obtain a codeword is of the form

$$
c ^ {\prime \prime} = (c _ {1}, c _ {2}, \dots , c _ {k _ {0}}, 0, \dots , 0) \in C ^ {\perp}
$$

Since $c ^ { ^ { \prime \prime } }$ is orthogonal to the first $k _ { 0 }$ rows of (1), so we can obtain $c _ { 1 } = c _ { 2 } = \cdot \cdot \cdot = c _ { k } = 0$ . so $c \in C ^ { ' } , C ^ { \perp } \in C ^ { ' }$ . Therefore H is the generator matrix of the additive dual code $C ^ { \perp }$ 口

Example 3.5. Let $C$ be a $\mathbb { Z } _ { p } \mathbb { Z } _ { p } [ u ]$ ]-additive code of type (3; 1, 4; 2, 2) with the standard form generator matrix:

$$
G = \left( \begin{array}{c c c c c} 1 & 0 & 0 & 1 & 1 \\ 0 & 1 & 0 & 2 & 0 \\ 0 & 0 & u & 0 & 2 u \\ 0 & 0 & 0 & u & 0 \end{array} \right)\tag{3}
$$

Then,the parity-check matrix of $C$ as given:

$$
H = \left( \begin{array}{c c c c c} 2 & 0 & 1 & 0 & 1 \\ 0 & 0 & 2 u & 0 & 0 \\ u & 2 u & 0 & 2 u & 0 \end{array} \right)\tag{4}
$$

And it’s clear that $C ^ { \perp }$ is of type (3; 1.4; 1, 2).

Notice that the number of codewords cannot given by the additive code of type.

## 4 The gray map

In this part of the paper, we study the MacWilliams identity for $\mathbb { Z } _ { p } \mathbb { Z } _ { p } [ u ] \mathrm { - a d d i t i v e }$ code, the results is similar to $p = 2 \ [ 3 ]$ , and a Gray map $\Phi$ is given, we found the Gray map $\Phi$ is a distance preserving map from $( \mathbb { Z } _ { p } \mathbb { Z } _ { p } [ u ]$ ,Gray distance) to $( \mathbb { Z } _ { p } ^ { \alpha + 2 \beta }$ ,Hamming distance), and it is also a weight preserving map.

In the Preliminaries, we also define a Gray map $\psi$ from R to $Z _ { p } ^ { 2 }$ in the following way.

$$
\begin{array}{c} \psi : R \to Z _ {p} ^ {2} \\ (a + u b) \to (b, a + b). \end{array}
$$

At the same time, in definition 3.1., we given a map Φ, it is from $\mathbb { Z } _ { p } ^ { \alpha } \times \mathbb { Z } _ { p } [ u ] ^ { \beta }$ to $\mathbb { Z } _ { p } ^ { n }$ defined as

$$
\Phi (a, b) = \left(a _ {0}, a _ {1}, \dots , a _ {\alpha - 1}, \psi \left(b _ {0}\right), \psi \left(b _ {1}\right), \dots , \psi \left(b _ {\beta - 1}\right)\right)
$$

for all $a = ( a _ { 0 } , a _ { 1 } , \cdots , a _ { \alpha - 1 } ) \in \mathbb { Z } _ { p } ^ { \alpha } , b = ( b _ { 0 } , b _ { 1 } , \cdots , b _ { \beta - 1 } ) \in \mathbb { Z } _ { p } [ u ] ^ { \beta } .$

Let C be an additive code and assume $n = \alpha + 2 \beta$ , the weight enumerator of an additive code C is defined by

$$
W (x, y) = \sum_ {c \in C} x ^ {n - w (c)} y ^ {w (c)}.
$$

Theorem 4.1. Let C be a $\mathbb { Z } _ { p } \mathbb { Z } _ { p } [ u ]$ -additive code, and $C ^ { \perp }$ be its dual code, then their weight enumerators $W _ { G } ( x , y )$ and $W _ { G ^ { \perp } } ( x , y )$ are connected by the MacWilliams identity:

$$
W _ {G ^ {\perp}} (x, y) = \frac {1}{| c |} W _ {G} (X + (q - 1) Y, X - Y)
$$

P roof Similar to the proof of [3,theorem 3.3].

Let $F _ { p } ^ { * }$ is a multiplication group with nonzero elements, where $p$ is an odd prime. Next we definition a Gray weight $W _ { G } ( c )$ for $c = ( c _ { 1 } , c _ { 2 } , \cdot \cdot \cdot , c _ { n } )$ in the following way:

$$
W _ {G} (c) = \sum_ {i = 0} ^ {n - 1} W _ {G} (c _ {i})
$$

where

$$
W _ {G} (c _ {i}) = \left\{ \begin{array}{l l} 0, & \text { if } c _ {i} = 0, \\ 2, & \text { if } c _ {i} = a + u (p - b), a, b \in F _ {p} ^ {*} \text { and } a \neq b, \\ 1, & \text { others }. \end{array} \right.
$$

This gray weight function defines also a gray distance function

$$
d _ {G} (x, y) = W _ {G} (x - y)
$$

The Hamming weight of a weight of n-tuples is the number of its nonzero entries. The Hamming distance between two n-tuples is defined as the Hamming weight of their diference. Denote the Hamming weight of a weight of a p-ary vector x by $W _ { H } ( x )$ and the Hamming distance between two p-ary vectors x and y of the same length by $d _ { H } ( x , y )$ , and we have $W _ { H } ( x - y ) = d _ { H } ( x , y )$

Since $\forall c = ( c _ { 1 } , c _ { 2 } , \cdot \cdot \cdot , c _ { n } ) \in \mathbb { Z } _ { p } \mathbb { Z } _ { p } [ u ]$ . We have

$$
W _ {H} (\Phi (c _ {i})) = \left\{ \begin{array}{l l} 0, & \text { if } c _ {i} = 0, \\ 2, & \text { if } c _ {i} = a + u (p - b), a, b \in F _ {p} ^ {*} a n d a \neq b, \\ 1, & o t h e r s. \end{array} \right.
$$

$$
\text { Clearly }, W _ {G} (c _ {i}) = W _ {H} (\Phi (c _ {i})) \forall c _ {i} \in \mathbb {Z} _ {p}, i \in (1, 2, \dots , n).
$$

Theorem 4.2. The Gray map Φ is a weight preserving map from

$$
\left(\mathbb {Z} _ {p} ^ {\alpha} \mathbb {Z} _ {p} [ u ] ^ {\beta}, G r a y w e i g h t\right) \quad t o \quad \left(\mathbb {Z} _ {p} ^ {\alpha + 2 \beta}, H a m m i n g w e i g h t\right)
$$

i.e.

$$
W _ {G} (c) = W _ {H} (\Phi (c) \quad f o r \forall c \in \mathbb {Z} _ {p} \mathbb {Z} _ {p} [ u ].\tag{5}
$$

and Φ is a distance preserving map from

$$
(\mathbb {Z} _ {p} ^ {\alpha} \mathbb {Z} _ {p} [ u ] ^ {\beta}, G r a y d i s t a n c e) \quad t o \quad (\mathbb {Z} _ {p} ^ {\alpha + 2 \beta}, H a m m i n g d i s t a n c e)
$$

i.e.

$$
d _ {G} (x, y) = d _ {H} (\Phi (x), \Phi (y)) \quad f o r \forall x, y \in \mathbb {Z} _ {p} \mathbb {Z} _ {p} [ u ].\tag{6}
$$

P roof Let $\forall c = ( c _ { 1 } , c _ { 2 } , \cdot \cdot \cdot , c _ { \alpha } , c _ { \alpha + 1 } , \cdot \cdot \cdot , c _ { \alpha + \beta } ) \in \mathbb { Z } _ { p } ^ { \alpha } \mathbb { Z } _ { p } [ u ] ^ { \beta }$ , where $c _ { i } \in \mathbb { Z } _ { p } ^ { \alpha } , i = 1 , 2 , \cdot \cdot \cdot , \alpha$ $c _ { \alpha + i } = r _ { i } + u q _ { i } \in \mathbb { Z } _ { p } [ u ] ^ { \beta } , i = 1 , 2 , \cdot \cdot \cdot , \beta .$ . by the grap map Φ we obtain:

$$
\begin{array}{c} \Phi (c) = (c _ {1}, c _ {2}, \dots , \psi (c _ {\alpha}), \psi (c _ {\alpha + 1}), \dots , \psi (c _ {\alpha + \beta})) \\ = (c _ {1}, c _ {2}, \dots , c _ {\alpha}, q _ {1}, q _ {2}, \dots , q _ {\beta}, q _ {1} + r _ {1}, q _ {2} + r _ {2}, \dots , q _ {\beta} + r _ {\beta}) \end{array}
$$

$$
\begin{array}{l} W _ {H} (\Phi (c)) = W _ {H} (c _ {1}, c _ {2}, \dots , c _ {\alpha}, q _ {1}, q _ {2}, \dots , q _ {\beta}, q _ {1} + r _ {1}, q _ {2} + r _ {2}, \dots , q _ {\beta} + r _ {\beta}) \\ \qquad = \sum_ {i = 1} ^ {\alpha} W _ {H} (c _ {i}) + \sum_ {i = 1} ^ {\beta} W _ {H} (q _ {i}, q _ {i} + r _ {i}) \\ \qquad = \sum_ {i = 1} ^ {\alpha} W _ {H} (c _ {i}) + \sum_ {i = 1} ^ {\beta} W _ {H} (\psi (c _ {\alpha + i})) \\ \qquad = \sum_ {i = 1} ^ {\alpha} W _ {G} (c _ {i}) + \sum_ {i = 1} ^ {\beta} W _ {G} (c _ {\alpha + i}) \\ \qquad = \sum_ {i = 1} ^ {\alpha + \beta} W _ {G} (c _ {i}) = W _ {G} (c) \end{array}
$$

Therefore we have (5). Similarly,we also can deduce (6),the proof is omitted.

## 5 The structure of $\mathbb { Z } _ { p } \mathbb { Z } _ { p } [ u ]$ -additive cyclic code

In this part of the paper, we introduce the definition of a additive cyclic code and some algebraic structure. A code C is cyclic if and only if its polynomial representation is an ideal. Let $\begin{array} { r } { R _ { \alpha , \beta } [ x ] = \frac { Z _ { p } [ x ] } { < x ^ { \alpha } - 1 > } \times \frac { R [ x ] } { < x ^ { \beta } - 1 > } } \end{array}$

Definition 5.1.A additive code C is called a $\mathbb { Z } _ { p } \mathbb { Z } _ { p } [ u ]$ -additive cyclic code if any cyclic shift of a codeword is also a code. i.e.,

$$
\left(a _ {0}, a _ {1}, \dots , a _ {\alpha - 1}, b _ {0}, b _ {1}, \dots , b _ {\beta - 1}\right) \in C \Rightarrow \left(a _ {\alpha - 1}, a _ {0}, \dots , a _ {\alpha - 2}, b _ {\beta - 1}, b _ {0}, \dots , b _ {\beta - 2}\right) \in C.
$$

Theorem 5.2. If C be any $\mathbb { Z } _ { p } \mathbb { Z } _ { p } [ u ]$ -additive cyclic code, then $C ^ { \perp }$ is also cyclic. P roof Let C be any $\mathbb { Z } _ { p } ^ { \alpha } \mathbb { Z } _ { p } [ u ] ^ { \beta }$ -additive cyclic code. Suppose $v = \left( a _ { 0 } , a _ { 1 } , \cdot \cdot \cdot , a _ { \alpha - 1 } , b _ { 0 } , b _ { 1 } , \cdot \cdot \cdot , b _ { \beta - 1 } \right) \in$ $C ^ { \perp }$ , for any codeword $w = ( d _ { 0 } , d _ { 1 } , \cdot \cdot \cdot , d _ { \alpha - 1 } , e _ { 0 } , e _ { 1 } , \cdot \cdot \cdot , e _ { \beta - 1 } ) \in C$ we have

$$
v \cdot w = u (\sum_ {i = 0} ^ {\alpha - 1} a _ {i} d _ {i}) + \sum_ {j = 0} ^ {\beta - 1} b _ {j} e _ {j} = 0
$$

Let S is a cyclic shift, and $j = l c m ( \alpha , \beta )$ . Then we have $S ( v ) = ( a _ { \alpha - 1 } , a _ { 0 } , \cdot \cdot \cdot , a _ { \alpha - 2 } , b _ { \beta - 1 } , b _ { 0 } , \cdot \cdot \cdot , b _ { \beta - 2 } )$ and $S ^ { j } ( w ) = w$ for any $w \in C$ . Since C be any $\mathbb { Z } _ { p } ^ { \alpha } \mathbb { Z } _ { p } [ u ] ^ { \tilde { \beta } }$ -additive cyclic code, So we have

$$
S ^ {j - 1} (w) = \left(d _ {1}, d _ {2}, \dots , d _ {\alpha - 1}, d _ {0}, e _ {1}, e _ {2}, \dots , e _ {\beta - 1}, e _ {0}\right) \in C
$$

Hence

$$
\begin{array}{r l} 0 = v \cdot S ^ {j - 1} (w) & = u (a _ {0} d _ {1} + a _ {1} d _ {2} + \dots + a _ {\alpha - 2} d _ {\alpha - 1} + a _ {\alpha - 1} d _ {0}) \\ & \quad + (b _ {0} e _ {1} + b _ {1} e _ {2} + \dots + b _ {\beta - 2} e _ {\beta - 1} + b _ {\beta - 1} e _ {0}) \\ & = u (a _ {\alpha - 1} d _ {0} + a _ {0} d _ {1} + \dots + a _ {\alpha - 2} d _ {\alpha - 1}) \\ & \quad + (b _ {\beta - 1} e _ {0} + b _ {1} e _ {2} + \dots + b _ {\beta - 2} e _ {\beta - 2}) \\ & = S (v) \cdot w \end{array}
$$

Therefore,we have $S ( v ) \in C ^ { \bot } , \mathrm { s o } \ C ^ { \bot }$ is a cyclic code.

Let C be a $\mathbb { Z } _ { p } \mathbb { Z } _ { p } [ u ]$ -additive cyclic code, for any codeword $c = ( a _ { 0 } , a _ { 1 } , \cdot \cdot \cdot , a _ { \alpha - 1 } , b _ { 0 } , b _ { 1 } , \cdot \cdot \cdot , b _ { \beta - 1 } ) \in$ C can be representation with a polynomial,i.e.,

$$
c (x) = (a _ {0} + a _ {1} x + \dots + a _ {\alpha - 1} x ^ {\alpha - 1}, b _ {0} + b _ {1} x + \dots + b _ {\beta - 1} x ^ {\beta - 1}) = (a (x), b (x)) \in R _ {\alpha , \beta} [ x ].
$$

Similarly. In preliminaries, we introduce a new scalar multiplication. Now, we have the following multiplication:

$$
(1) \forall c _ {1} (x) = (a _ {1} (x), b _ {1} (x)), c _ {2} (x) = (a _ {2} (x), b _ {2} (x)) \in R _ {\alpha , \beta} [ x ],
$$

$$
c _ {1} (x) c _ {2} (x) = (a _ {1} (x) a _ {2} (x), b _ {1} (x) b _ {2} (x))
$$

$$
(2) \forall c _ {1} (x) = (a _ {1} (x), b _ {1} (x)) \in R _ {\alpha , \beta} [ x ], c _ {2} (x) = r (x) + u q (x) \in R [ x ], \text {where} r (x), q (x) \in Z _ {p} [ x ],
$$

$$
c _ {1} (x) c _ {2} (x) = (a _ {1} (x) r (x), b _ {1} (x) c _ {2} (x))
$$

$$
(3) \forall c _ {1} (x) = (a _ {1} (x), b _ {1} (x)) \in R _ {\alpha , \beta} [ x ], c _ {2} (x) \in Z _ {p} [ x ],
$$

$$
c _ {1} (x) c _ {2} (x) = \left(a _ {1} (x) c _ {2} (x), b _ {1} (x) c _ {2} (x)\right)
$$

Clearly, definition 5.1 is equivalent to

$$
\begin{array}{c} c (x) = (a _ {0} + a _ {1} x + \dots + a _ {\alpha - 1} x ^ {\alpha - 1}, b _ {0} + b _ {1} x + \dots + b _ {\beta - 1} x ^ {\beta - 1}) \in R _ {\alpha , \beta} [ x ]. \\ \Longrightarrow x c (x) = (a _ {\alpha - 1} + a _ {0} x + \dots + a _ {\alpha - 2} x ^ {\alpha - 1}, b _ {\beta - 1} + b _ {0} x + \dots + b _ {\beta - 2} x ^ {\beta - 1}) \in R _ {\alpha , \beta} [ x ]. \end{array}
$$

Now, we define the homomorphism mapping:

$$
\begin{array}{l} \Psi : R _ {\alpha , \beta} [ x ] \longrightarrow R [ x ] \\ \Psi (c (x)) = \Psi (a (x), b (x)) = b (x) \end{array}
$$

It is clear that $I m a g e ( \Psi )$ is an ideal in the ring $\frac { R [ x ] } { < x ^ { \beta } - 1 > }$ and ker(Ψ) is also an ideal over $Z _ { p } [ x ]$ And note that

$$
\operatorname{Image} (\Psi) = \left\{b (x) \in R [ x ]: (a (x), b (x)) \in R _ {\alpha , \beta} [ x ] \right\}
$$

$$
k e r (\Psi) = \{(a (x), 0) \in R _ {\alpha , \beta} [ x ]: a (x) \in \frac {Z _ {p} [ x ]}{x ^ {\alpha} - 1}) \}
$$

By using the characterization in [14], we have

$$
\operatorname{Image} (\Psi) = <   g (x) + u p (x), u q (x) >
$$

where $\begin{array} { r } { g ( x ) , p ( x ) , q ( x ) \in \frac { R [ x ] } { < x ^ { \beta } - 1 > } , q ( x ) \mid g ( x ) \mid ( x ^ { \beta } - 1 ) \mathrm { ~ a n d ~ } q ( x ) \mid p ( x ) \frac { x ^ { \beta } - 1 } { g ( x ) } . } \end{array}$ Similarly,

$$
k e r (\Psi) = <   (f (x), 0) >
$$

where $\begin{array} { r } { f ( x ) \in \frac { Z _ { p } [ x ] } { x ^ { \alpha } - 1 } } \end{array}$ and $f ( x ) \mid ( x ^ { \alpha } - 1 )$ ).

According to the homomorphism map theorem we have:

$$
C / k e r (\Psi) \cong <   g (x) + u p (x), u q (x) >.
$$

Hence, we have

$$
(h (x), (g (x) + u p (x), u q (x)) \in C
$$

$$
\text { where } \Psi (h (x), (g (x) + u p (x), u q (x))) = (g (x) + u p (x), u q (x)).
$$

By these discussion, it is easy to see that any $\mathbb { Z } _ { p } \mathbb { Z } _ { p } [ u ]$ ]-additive cyclic code can be generated by two elements of the form $( h ( x ) , ( g ( x ) + u p ( x ) , u q ( x ) ) )$ and $( f ( x ) , 0 )$

Corollary 5.3.Let C be a $\mathbb { Z } _ { p } \mathbb { Z } _ { p } [ u ]$ -additive cyclic code. Then C is an ideal in $R _ { \alpha , \beta } [ x ]$ which can be generated by

$$
C = ((f (x), 0), (h (x), (g (x) + u p (x), u q (x)))).
$$

where $q ( x ) \mid g ( x ) \mid ( x ^ { \beta } - 1 ) , q ( x ) \mid p ( x ) { \frac { x ^ { \beta } - 1 } { g ( x ) } }$

Corollary 5.4. Let $C = ( ( f ( x ) , 0 ) , ( h ( x ) , ( g ( x ) + u p ( x ) , u q ( x ) ) ) )$ is a $\mathbb { Z } _ { p } \mathbb { Z } _ { p } [ u ]$ -additive cyclic code, then we may assume that $\textstyle f ( x ) \mid h ( x ) { \frac { x ^ { \beta } - 1 } { l ( x ) } }$ .where $l ( x ) = l c m ( p ( x ) , q ( x ) )$

$$
\begin{array}{r l r} & & {\text {Proof (1)Since \Psi(\frac {x^{\beta} - 1}{l(x)} (h(x),(g(x)+up(x),uq(x)))) = \Psi((\frac {x^{\beta} - 1}{l(x)} *h(x),0)) = 0.}} \\ & & {\mathrm{Hence (\frac {x^{\beta} - 1}{l(x)} * h(x),0)\in ker(\Psi)\subseteq C \text {and} f(x)\mid h(x)\frac {x^{\beta} - 1}{l(x)}.}} \end{array}
$$

As a consequence to this corollary, we classify the structure of the additive cyclic code into three categories by the following theorem.

Theorem 5.5. Let C be a $\mathbb { Z } _ { p } \mathbb { Z } _ { p } [ u ]$ -additive cyclic code.Then C can be identified as following: $( 1 ) C = ( ( f ( x ) , 0 )$ , where $\begin{array} { r } { f ( x ) \in \frac { Z _ { p } [ x ] } { x ^ { \alpha } - 1 } } \end{array}$

$( 2 ) C = ( h ( x ) , ( g ( x ) + u p ( x ) , u q ( x ) ) )$ , where $q ( x ) \mid g ( x ) \mid ( x ^ { \beta } - 1 )$ and $( x ^ { r } - 1 ) \mid p ( x ) { \textstyle \frac { x ^ { \beta } - 1 } { g ( x ) } }$ $( 3 ) C = ( ( f ( x ) , 0 ) , ( h ( x ) , ( g ( x ) + u p ( x ) , u q ( x ) ) ) )$ ,where $q ( x ) \mid g ( x ) \mid ( x ^ { \beta } - 1 ) , q ( x ) \mid p ( x ) { \frac { x ^ { \beta } - 1 } { g ( x ) } }$ 2$\textstyle f ( x ) \mid h ( x ) { \frac { x ^ { \beta } - 1 } { l ( x ) } }$ and $l ( x ) = l c m ( p ( x ) , q ( x ) )$ 口

Corollary 5.6.Let C be any $\mathbb { Z } _ { p } \mathbb { Z } _ { p } [ u ]$ -additive cyclic code. Then $\Phi ( C )$ is an cyclic code of length $\alpha + 2 \beta$ over $Z _ { p }$

P roof Let $S$ is a cyclic shift. Since $C$ be any $\mathbb { Z } _ { p } \mathbb { Z } _ { p } [ u ]$ -additive cyclic code. For any codeword

$$
c = (a _ {0}, a _ {1}, \dots , a _ {\alpha - 1}, b _ {0}, b _ {1}, \dots , b _ {\beta - 1}) \in C
$$

where $b _ { i } = r _ { i } + u q _ { i } , i \in \{ 0 , 1 , 2 , \cdots , \beta - 1 \} , a _ { i } , r _ { i } , q _ { i } \in Z _ { p } .$

We have

$$
S (c) = \left(a _ {\alpha - 1}, a _ {0}, \dots , a _ {\alpha - 2}, b _ {\beta - 1}, b _ {0}, \dots , b _ {\beta - 2}\right) \in C
$$

Then

$$
\begin{array}{c} \Phi (S (c)) = (a _ {\alpha - 1}, a _ {0}, \dots , a _ {\alpha - 2}, q _ {\beta - 1}, q _ {0}, \dots , \\ q _ {\beta - 2}, q _ {\beta - 1} + r _ {\beta - 1}, q _ {0} + r _ {0}, \dots , q _ {\beta - 2} + r _ {\beta - 2}) \in \Phi (C) \end{array}
$$

Then by the Gray map we have:

$$
\Phi (c) = \left(a _ {0}, a _ {1}, \dots , a _ {\alpha - 1}, q _ {0}, q _ {1}, \dots , q _ {\beta - 1}, q _ {0} + r _ {0}, q _ {1} + r _ {1}, \dots , q _ {\beta - 1} + r _ {\beta - 1}\right) \in \Phi (C).
$$

Hence

$$
\begin{array}{c} S (\Phi (c)) = (a _ {\alpha - 1}, a _ {0}, \dots , a _ {\alpha - 2}, q _ {\beta - 1}, q _ {0}, \dots , q _ {\beta - 2}, \\ q _ {\beta - 1} + r _ {\beta - 1}, q _ {0} + r _ {0}, \dots , q _ {\beta - 2} + r _ {\beta - 2}) = \Phi (S (c)) \in \Phi (C). \end{array}
$$

This proves that $\Phi ( C )$ is an cyclic code of length $\alpha + 2 \beta$ over $Z _ { p }$

## 6 Conclusion

In this paper, we studied $\mathbb { Z } _ { p } \mathbb { Z } _ { p } [ u ] \mathrm { - a d d i t i v e }$ codes some property, including generator and parity check matrices for the codes. We fund the Gray map Φ is a distance preserving map and weight preserving map as well. At the end of the paper,we introduce the structure of $\mathbb { Z } _ { p } \mathbb { Z } _ { p } [ u ] .$ additive cyclic code. The studies makes this family of codes become widespread. we hope this family of codes haven more studies, such as constacyclic codes, depth distribution and other place. Due to this family of codes is newly introduced, some similar problems are still open here.

## References

[1] P.Delsarte, An algebraic approach to the association schemes of coding theory[R]. philips Research Rep Suppl,1973.

[2] G.H. Norton, A.S., On the Hamming Distance of Linear Codes Over a Finite Chain Ring. IEEE Trans. Inform. Theory,VOL.46,NO.3,MAY 2000.

[3] I.Aydogdu,T.Abualrub ,I.Siap, On <sup>Z</sup><sub>2</sub><sup>Z</sup><sub>2</sub>[u] additive codes,Int.J.Comput.Math.2014.doi: 10.1080/00207160.2013.859854

[4] I.Aydogdu , I.Siap , On $Z _ { p ^ { r } } Z _ { p ^ { \smash { \prime } } }$ s -additive codes,Linear and Multilinear Algebra,2015.Vol.63. No.10.2089-2102.

[5] RC.Singleton, Maximum distance q-ary codes.IEEE Trans.Inform.Theory.1964;10:116-118.

[6] J.Borges,C.Fern´andez,J.Pujol,M.Villanueva, Z<sub>2</sub>Z<sub>4</sub>-linear codes and duality.VJMDA, pp.171-177, Ciencias,23.Secr.Publ.intercamb.Ed.,Valladolid(2006).

[7] M.Bilal, J.Borges, S.T.Dougherty, C.Fern´andez, Maximum distance separable codes over $Z _ { 4 }$ and $Z _ { 2 } \times Z _ { 4 }$ . Des.codes cryptogr.(2011)61:31-40.

[8] B.J¨urgen, Cyclic additive codes. Journal of Algebra 372(2012)661-672.

[9] I.Aydogdu and I.Siap, The structure of $Z _ { 2 } Z _ { 2 } .$ s -additive code:Bounds on the minimum distance, Appl.Math.Inform.Sci.7(6)(2013),pp.2271-2278.

[10] H.Rifa, J.Rifa, and L.Ronquillo, Perfect $Z _ { 2 } Z _ { 4 }$ -linear codes in steganography, Comput.Res. Reposit.,Vol.abs/1002.0(2010).

[11] J.Rifa, L.Ronquillo, Product Perfect $Z _ { 2 } Z _ { 4 }$ -linear codes in steganography.ISITA,Taichung, Taiwan,October 2010,pp.696-701.

[12] F.J.MacWilliams, N.J.A. Solane, The Theory of Error-Correcting Codes, North-Holland, Amsterdam, 1997.

[13] Z.X.Wan, Quaternary Codes, World Scientific, Singapore, 1997.

[14] X.S.Liu, H.L.Liu, Cyclic Code over $F _ { 2 } + u F _ { 2 } + v F _ { 2 }$ , Chin.Quart.J.of Math.2014,29(2):189- 194.

[15] T.Abualrub, I.Siap, N.Aydin, $Z _ { 2 } Z _ { 4 } – \mathrm { A d d i t i v e }$ Cyclic Codes ,IEEE Trans.Inform.Theory. VOL.60.NO.3.MARCH 2014.