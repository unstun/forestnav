---
origin: ai+web+doi
reviewed: false
date: 2026-06-23
task: T21
status: pass
scope: reference audit for 3_paper/main.tex and 3_paper/references.bib
---

# T21 Reference Audit

## Summary

All 7 citation keys used by `3_paper/main.tex` are defined in `3_paper/references.bib`.
All 7 references were checked against an opened official paper page, DOI/arXiv metadata, and DOI-fetched BibTeX.
No `[CITATION NEEDED]` marker remains.

One claim-level correction was made during the audit: the Wang2021 citation now supports the existence and breadth of learning-based robot motion-planning work, while the conservative F-N3P design choice is stated as this paper's own design boundary rather than as a claim attributed to that survey.

An independent literature-scout cross-check returned no fake-citation or hard metadata failures. Its two warnings were addressed in the final files: the Wang2021 local claim was softened, and the Bonetti2023 BibTeX title was expanded to match the arXiv/DataCite title string.

## Audit Method

1. Extracted citation keys from `3_paper/main.tex` and compared them with `3_paper/references.bib`.
2. Opened official or primary pages for every reference: arXiv pages for arXiv works, SAGE for Dolgov2010, MSP/Pacific Journal of Mathematics for Reeds-Shepp, IEEE/Crossref for Kavraki1996, IET/Crossref for Wang2021.
3. Fetched raw BibTeX with `curl -H "Accept: application/x-bibtex" https://doi.org/<DOI>` and saved the raw records under `raw_bibtex/`.
4. Checked whether each citation supports the sentence or paragraph where it is used in `main.tex`.

The bundled `inno-reference-audit` verification script was tried as a first-pass machine check, but it is not used as final evidence because its optional dependencies were missing and it crashed on Crossref's list-valued title field. The final audit therefore uses direct opened sources and saved DOI/arXiv metadata.

## Source Artifacts

| Artifact | Purpose |
|---|---|
| `raw_bibtex/*.bib` | DOI-fetched BibTeX records for all 7 references |
| `source_snippets/*_arxiv.xml` | arXiv API metadata for Xue2026N3P, Bonetti2023Roadmap, Sormoli2024HybridSurvey |
| `source_snippets/*_crossref.json` | Crossref metadata for Dolgov2010HybridAstar, ReedsShepp1990, Kavraki1996PRM, Wang2021LearningMotionPlanning |

## Per-Reference Verdict

| Key | Primary source | BibTeX source | Claim check | Verdict |
|---|---|---|---|---|
| `Xue2026N3P` | https://arxiv.org/abs/2605.22722 | `raw_bibtex/Xue2026N3P.bib` | Supports N3P as a learning-based three-stage automated parking method using an intermediate preparatory pose and Hybrid A* integration. The paper uses it only as inspiration for F-N3P's subgoal-decomposition design. | PASS |
| `Dolgov2010HybridAstar` | https://journals.sagepub.com/doi/10.1177/0278364909359210 | `raw_bibtex/Dolgov2010HybridAstar.bib` | Supports autonomous-vehicle planning in semi/unstructured environments, A* over a 3D kinematic vehicle state space, kinematically feasible trajectories, and topological guidance for faster search. | PASS |
| `ReedsShepp1990` | https://msp.org/pjm/1990/145-2/p06.xhtml | `raw_bibtex/ReedsShepp1990.bib` | Supports shortest bounded-curvature car paths with forward/reverse motion and cusps/reversals, matching the Reeds-Shepp connector role in the paper. | PASS |
| `Bonetti2023Roadmap` | https://arxiv.org/abs/2304.14043 | `raw_bibtex/Bonetti2023Roadmap.bib` | Supports Roadmap Hybrid A* and waypoint-guided Hybrid A* for non-holonomic vehicles in narrow industrial environments, including a static roadmap and waypoint guidance. The BibTeX title in `references.bib` keeps the official arXiv/DataCite title string, including its duplicated pseudocode suffix. | PASS |
| `Kavraki1996PRM` | https://ieeexplore.ieee.org/document/508439/ | `raw_bibtex/Kavraki1996PRM.bib` | Supports PRM as a roadmap-based planning method with learning and query phases in high-dimensional configuration spaces. | PASS |
| `Wang2021LearningMotionPlanning` | https://digital-library.theiet.org/doi/full/10.1049/csy2.12020 and Crossref DOI metadata | `raw_bibtex/Wang2021LearningMotionPlanning.bib` | Supports the statement that learning-based robot motion planning covers multiple learning settings. The earlier stronger wording about weakening feasibility was softened in `main.tex`. | PASS |
| `Sormoli2024HybridSurvey` | https://arxiv.org/abs/2406.05575 | `raw_bibtex/Sormoli2024HybridSurvey.bib` | Supports hybrid motion planning as combinations of data-driven/learning-based and logic-driven/analytic components for automated-driving motion planning. | PASS |

## Text Change Made

`3_paper/main.tex` now says learning-based motion planning has been studied across supervised, unsupervised, and reinforcement-learning settings before introducing F-N3P's deliberately narrower design. This avoids over-claiming that Wang2021 directly proves the safety or feasibility weakness of learned planners.

## Remaining Boundary

The audit verifies that the current references exist and support their local citation contexts. It does not make the experimental claims stronger. T14 remains the only formal main-evaluation evidence; T15 and T16 remain framework-scale, and T16 RealMap transfer remains unresolved.
