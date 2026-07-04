# Module2 Reviewer Evidence Cards

- status: `reviewer_evidence_cards_ready`
- local training allowed: `False`
- remote training resource: `gpu3070ti-relay`
- evidence map status: `module2_manuscript_evidence_mapped`
- formal performance claim allowed: `False`

## Blocking Reasons

- none

## Cards

### method_is_ha_star_analytic_operator
- reviewer verdict: `claim_traceable_with_scope_limit`
- claim status: `allowed_method_structure`
- evidence state: `mapped`
- writing instruction: Can be used only with the listed scope/qualifier and cited against the primary evidence artifacts.
- manuscript anchors:
  - `learned analytic-expansion operator inside` -> `3_paper/module2_section_seed/module2_paper_section_seed.tex:8` raw=`True` stripped=`True`
  - `not a standalone global planner` -> `3_paper/module2_section_seed/module2_paper_section_seed.tex:8` raw=`True` stripped=`True`
  - `terminal RS` -> `3_paper/module2_section_seed/module2_paper_section_seed.tex:11` raw=`True` stripped=`True`
- primary evidence:
  - `0_trials/module2_claim_safety/module2_claim_safety.json` status=`blocked_formal_performance_claims`
  - `0_trials/module2_method_algorithms/module2_method_algorithms.json` status=`code_anchored`
  - `0_trials/module2_system_diagram/module2_system_diagram.json` status=`code_anchored_drawio`
  - `0_trials/module2_paper_readiness/module2_paper_readiness.json` status=`ready_to_write`
  - `3_paper/module2_section_seed/module2_paper_section_seed.json` status=`draft_ready`
- code anchors:
  - `2_experiment/forest_n3p/third_party/pathplan/hybrid_a_star/planner.py:129` `HybridAStarPlanner.__init__`
  - `2_experiment/forest_n3p/third_party/pathplan/hybrid_a_star/planner.py:175` `HybridAStarPlanner.__init__`
  - `2_experiment/forest_n3p/main_evaluation.py:70` `main_evaluation.RL_RS_OPERATOR_METHODS`
  - `2_experiment/forest_n3p/third_party/pathplan/hybrid_a_star/planner.py:296` `HybridAStarPlanner._try_analytic_expansion`
  - `2_experiment/forest_n3p/third_party/pathplan/hybrid_a_star/planner.py:301` `HybridAStarPlanner._try_custom_analytic_expansion`
  - `2_experiment/forest_n3p/rl_rs/checkpoint_operator.py:55` `load_rl_rs_funnel_operator_from_checkpoint`
  - `2_experiment/forest_n3p/rl_rs/checkpoint_operator.py:77` `load_rl_rs_funnel_operator_from_checkpoint`
  - `2_experiment/forest_n3p/rl_rs/checkpoint_operator.py:85` `load_rl_rs_funnel_operator_from_checkpoint`

### no_warm_gate3_formal_failure
- reviewer verdict: `claim_traceable_with_scope_limit`
- claim status: `allowed_with_no_warm_scope_limit`
- evidence state: `mapped`
- writing instruction: Can be used only with the listed scope/qualifier and cited against the primary evidence artifacts.
- manuscript anchors:
  - `No-warm PPO Gate` -> `3_paper/module2_section_seed/module2_paper_section_seed.tex:14` raw=`True` stripped=`True`
  - `0.453125` -> `3_paper/module2_section_seed/module2_paper_section_seed.tex:14` raw=`True` stripped=`True`
  - `does not evaluate obstacle-summary warm-start` -> `3_paper/module2_section_seed/module2_paper_section_seed.tex:14` raw=`True` stripped=`True`
  - `Formal performance claims remain blocked` -> `3_paper/module2_section_seed/module2_paper_section_seed.tex:14` raw=`True` stripped=`True`
- primary evidence:
  - `0_trials/module2_claim_safety/module2_claim_safety.json` status=`blocked_formal_performance_claims`
  - `0_trials/module2_gate3_formal/gate3_no_warm_formal_v1/gate3_formal_audit.json` status=`fail`
  - `0_trials/module2_paper_readiness/module2_paper_readiness.json` status=`ready_with_scope_limit`
  - `3_paper/module2_section_seed/module2_paper_section_seed.json` status=`draft_ready_with_scope_limit`
- metric values: `terminal_rs_success_rate=0.453125, episodes=64, success_threshold=0.8`

### formal_results_blocked
- reviewer verdict: `blocked_placeholder_traceable`
- claim status: `blocked_placeholder_not_a_result_claim`
- evidence state: `blocked_as_expected`
- writing instruction: Do not write this as a result claim; keep it as a blocked placeholder until the listed blockers close.
- manuscript anchors:
  - `Formal performance claims remain blocked` -> `3_paper/module2_section_seed/module2_paper_section_seed.tex:14` raw=`True` stripped=`True`
  - `% BLOCKED: formal_results` -> `3_paper/module2_section_seed/module2_paper_section_seed.tex:16` raw=`True` stripped=`False`
- primary evidence:
  - `3_paper/module2_claim_audit/module2_manuscript_claim_audit.json` status=`maintex_module2_claim_audit_passed`
  - `0_trials/module2_claim_safety/module2_claim_safety.json` status=`blocked_formal_performance_claims`
  - `0_trials/module2_paper_readiness/module2_paper_readiness.json` status=`blocked`
  - `3_paper/module2_section_seed/module2_paper_section_seed.json` status=`blocked`
- paper blockers: `paper_tables_not_formal`, `h02_verdict_not_formal`, `h02_formal_acceptance_not_accepted`, `h01_manifest_not_ready`, `f02_6_warm_start_decision_pending`, `missing_module2_rl_rs_checkpoint`, `remote_execution_packet_not_ready`, `requires_dr_sun_approval`, `missing_gate3_formal_audit`, `h02_scale_below_h01_manifest`, `missing_ppo_result_rows`, `missing_remote_pullback_artifacts`, `f02_6_formal_chain_pending`, `claim_safety_blocks_formal_performance`, `f02_6_pending`

### warm_start_effect_blocked
- reviewer verdict: `blocked_placeholder_traceable`
- claim status: `blocked_placeholder_pending_f02_6`
- evidence state: `blocked_as_expected`
- writing instruction: Do not write this as a result claim; keep it as a blocked placeholder until the listed blockers close.
- manuscript anchors:
  - `% BLOCKED: warm_start_effect` -> `3_paper/module2_section_seed/module2_paper_section_seed.tex:17` raw=`True` stripped=`False`
  - `does not evaluate obstacle-summary warm-start` -> `3_paper/module2_section_seed/module2_paper_section_seed.tex:14` raw=`True` stripped=`True`
- primary evidence:
  - `0_trials/module2_paper_readiness/module2_paper_readiness.json` status=`blocked`
  - `3_paper/module2_section_seed/module2_paper_section_seed.json` status=`blocked`
  - `0_trials/module2_f02_6_decision_record/f02_6_decision_record.json` status=`pending_human_decision`
  - `0_trials/module2_remote_formal_execution_packet/remote_formal_execution_packet.json` status=`blocked_until_f02_6_decision`
- paper blockers: `f02_6_not_approved`, `requires_dr_sun_approval`, `f02_6_warm_start_decision_pending`, `missing_module2_rl_rs_checkpoint`

## Verification Commands

- `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_manuscript_evidence_map`
- `PYTHONPATH=2_experiment python -m forest_n3p.scripts.build_module2_reviewer_evidence_cards`
- `PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests/test_module2_manuscript_evidence_map.py 2_experiment/forest_n3p/tests/test_module2_reviewer_evidence_cards.py`
- `pdflatex wrapper input for 3_paper/module2_reviewer_evidence_cards/module2_reviewer_evidence_cards.tex`
- `KMP_DUPLICATE_LIB_OK=TRUE PYTHONPATH=2_experiment pytest -q 2_experiment/forest_n3p/tests`
- `cd 3_paper && pdflatex -interaction=nonstopmode -halt-on-error -draftmode -output-directory=/tmp/forestnav_module2_texcheck main.tex`

## Review Boundaries

- These cards are for reviewer-facing traceability, not formal performance evidence.
- Cards with claim_status beginning with blocked_ are placeholders only and must not be rewritten as result claims.
- No local training is allowed; formal PPO checkpoint production remains gated on F02.6 and gpu3070ti-relay.
