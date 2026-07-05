# Module2 Formal Gate Missing Artifacts Audit

This file inventories missing formal-gate evidence. It does not execute commands or write paper results.

- status: `formal_gate_missing_artifacts_open`
- all_required_evidence_present: `False`
- audit_issue_count: `0`
- local_training_allowed: `False`
- formal_claim_allowed: `False`

## Current Gate Summary

- f02_6_decision_record_status: `approved`
- f02_6_decision_gate_status: `f02_6_decision_gate_audit_passed`
- f02_6_transition_gate_status: `f02_6_transition_gate_audit_passed`
- f02_6_transition_gate_audit_issue_count: `0`
- post_f02_6_plan_status: `ready_for_remote_training_packet_execution`
- post_plan_training_allowed_now: `True`
- post_plan_remote_preflight_allowed_now: `True`
- source_freshness_status: `source_freshness_clean_current`
- source_freshness_regeneration_required: `False`
- source_freshness_blocking_regeneration_required: `False`
- remote_packet_status: `ready_for_gpu3070ti_remote_training`
- ready_to_run_remote_training: `True`
- remote_packet_safety_audit_status: `remote_packet_safety_audit_passed`
- h01_manifest_status: `ready_for_formal_run`
- h01_blockers: `[]`
- h02_acceptance_status: `blocked_formal_output_acceptance`
- h02_blockers: `['h02_verdict_not_formal', 'gate3_formal_audit_not_passed', 'h02_scale_below_h01_manifest', 'missing_ppo_result_rows']`

## Formal Gate Handoff Index

- status: `formal_gate_requirements_open`
- open_requirement_count: `1`
- local_training_allowed_now: `False`
- remote_training_allowed_now: `True`
- formal_result_material_allowed_now: `False`
- next_action: `resolve_h01_h02_formal_evaluation_acceptance` (requires_dr_sun=`False`, allowed_for_agent_now=`False`)
- next_action_description: Resolve h01_h02_formal_evaluation_acceptance with acceptable evidence; invalid substitutes remain disallowed.
- claim_boundary: This handoff index is a gate-navigation aid; it is not a training command, evaluation command, result table, or paper-result source.

### Authority Artifacts

- decision_record: `0_trials/module2_f02_6_decision_record/f02_6_decision_record.json`
- transition_gate_audit: `0_trials/module2_f02_6_transition_gate_audit/f02_6_transition_gate_audit.json`
- post_f02_6_regeneration_plan: `0_trials/module2_post_f02_6_regeneration_plan/post_f02_6_regeneration_plan.json`
- remote_formal_execution_packet: `0_trials/module2_remote_formal_execution_packet/remote_formal_execution_packet.json`
- formal_missing_artifacts_inventory: `0_trials/module2_formal_gate_missing_artifacts/formal_gate_missing_artifacts.json`
- h01_manifest: `0_trials/module2_v1_evaluation_manifest/module2_v1_evaluation_manifest.json`
- h02_formal_acceptance: `0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json`

### Handoff Requirements

- `f02_6_human_decision` (decision): status=`satisfied`, missing_count=`0`, execution_allowed_now=`False`
  - source_artifacts: `0_trials/module2_f02_6_decision_record/f02_6_decision_record.json; 0_trials/module2_f02_6_transition_gate_audit/f02_6_transition_gate_audit.json`
  - downstream_consumers: `0_trials/module2_post_f02_6_regeneration_plan/post_f02_6_regeneration_plan.json; 0_trials/module2_remote_formal_execution_packet/remote_formal_execution_packet.json; 0_trials/module2_v1_evaluation_manifest/module2_v1_evaluation_manifest.json; 0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json`
- `training_remote_ppo_checkpoint` (training): status=`satisfied`, missing_count=`0`, execution_allowed_now=`True`
  - source_artifacts: `0_trials/module2_remote_formal_execution_packet/remote_formal_execution_packet.json; 0_trials/module2_remote_packet_safety_audit/remote_packet_safety_audit.json`
  - downstream_consumers: `0_trials/module2_v1_evaluation_manifest/module2_v1_evaluation_manifest.json; 0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json`
  - responsible_stage: `gate3_remote_training` (status=`ready`, allowed_now=`True`)
- `evaluation_gate3_episode_outputs` (evaluation): status=`satisfied`, missing_count=`0`, execution_allowed_now=`True`
  - source_artifacts: `0_trials/module2_remote_formal_execution_packet/remote_formal_execution_packet.json; 0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json`
  - downstream_consumers: `0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json`
  - responsible_stage: `gate3_remote_audit_pullback` (status=`blocked`, allowed_now=`False`)
- `acceptance_remote_pullback_and_audit` (acceptance): status=`satisfied`, missing_count=`0`, execution_allowed_now=`True`
  - source_artifacts: `0_trials/module2_remote_formal_execution_packet/remote_formal_execution_packet.json; 0_trials/module2_remote_packet_safety_audit/remote_packet_safety_audit.json; 0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json`
  - downstream_consumers: `0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json`
  - responsible_stage: `gate3_remote_audit_pullback` (status=`blocked`, allowed_now=`False`)
- `h01_h02_formal_evaluation_acceptance` (evaluation_acceptance): status=`blocked_missing_outputs`, missing_count=`1`, execution_allowed_now=`False`
  - missing_artifact_ids: `h02_formal_output_acceptance`
  - source_artifacts: `0_trials/module2_v1_evaluation_manifest/module2_v1_evaluation_manifest.json; 0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json`
  - downstream_consumers: `0_trials/module2_claim_safety/module2_claim_safety.json; 0_trials/module2_paper_readiness/module2_paper_readiness.json`
  - responsible_stage: `regenerate_h01_h02_formal_artifacts` (status=`blocked`, allowed_now=`False`)

## Missing Counts

- acceptance: `0`
- claim_gate: `1`
- decision: `0`
- decision_gate: `0`
- evaluation: `0`
- evaluation_acceptance: `1`
- gate_sequence: `4`
- regeneration: `0`
- training: `0`

## Formal Gate Requirements

- `training_remote_ppo_checkpoint` (training): status=`satisfied`, execution_allowed_now=`True`
  - responsible_stage: `gate3_remote_training` (status=`ready`, allowed_now=`True`)
  - acceptable_evidence: `remote-produced train/final_model.zip pulled back to the local formal Gate3 trial directory; train/summary.json with PPO run metadata and terminal-RS training signals; train/training_manifest.json with protocol label, source head, host, seed, and command provenance`
  - invalid_substitutes: `local training output; available-subset smoke model; no-warm Gate3 failed checkpoint; stdout without pulled-back checkpoint and manifest`
- `evaluation_gate3_episode_outputs` (evaluation): status=`satisfied`, execution_allowed_now=`True`
  - responsible_stage: `gate3_remote_audit_pullback` (status=`blocked`, allowed_now=`False`)
  - responsible_stage_blocked_by: `remote_training_not_completed`
  - acceptable_evidence: `eval/gate3_eval_episodes.csv from the approved formal remote run; eval/gate3_summary.json with formal terminal-RS success, collision, truncation, and timing fields`
  - invalid_substitutes: `H02 available-subset smoke CSV; paper table preview; no-warm formal failure eval reused as warm-start evidence`
- `acceptance_remote_pullback_and_audit` (acceptance): status=`satisfied`, execution_allowed_now=`True`
  - responsible_stage: `gate3_remote_audit_pullback` (status=`blocked`, allowed_now=`False`)
  - responsible_stage_blocked_by: `remote_training_not_completed`
  - acceptable_evidence: `gate3_trial_manifest.json copied back from the formal remote run; gate3_formal_audit.json marking the run formal, scoped, and non-smoke; checkpoint SHA-256 record for the pulled-back final_model.zip`
  - invalid_substitutes: `remote command success without local pullback; checkpoint file without hash record; audit marked candidate, smoke, preview, or not_formal`
- `h01_h02_formal_evaluation_acceptance` (evaluation_acceptance): status=`blocked_missing_outputs`, execution_allowed_now=`False`
  - missing_artifact_ids: `h02_formal_output_acceptance`
  - blocked_by: `h02_formal_output_acceptance`
  - responsible_stage: `regenerate_h01_h02_formal_artifacts` (status=`blocked`, allowed_now=`False`)
  - responsible_stage_blocked_by: `missing_remote_audit_pullback`
  - acceptable_evidence: `H01 manifest status ready_for_formal_run or ready_for_formal_evaluation after F02.6 is closed; H02 acceptance with formal_output_accepted=true and paper_result_input_allowed=true; formal PPO rows present and accepted against the H01 required output schema`
  - invalid_substitutes: `blocked H01 manifest; blocked H02 acceptance audit; formal-looking tables generated from smoke or missing PPO rows`

## Evidence Groups

- `f02_6_decision_record` (decision): complete=`True`, blocked_by=``
- `f02_6_transition_gate_audit` (decision_gate): complete=`True`, blocked_by=``
- `source_fresh_regeneration_targets` (regeneration): complete=`True`, blocked_by=``
- `post_f02_6_ordered_stages` (gate_sequence): complete=`False`, blocked_by=`f02_6_decision_record, gate3_remote_audit_pullback, regenerate_h01_h02_formal_artifacts, regenerate_claim_gate_artifacts`
  - missing `f02_6_decision_record`: `0_trials/module2_f02_6_decision_record/f02_6_decision_record.json` (current_decision_status_approved)
  - missing `gate3_remote_audit_pullback`: `0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/final_model.zip; 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/summary.json; 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/train/training_manifest.json; 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/eval/gate3_eval_episodes.csv; 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/eval/gate3_summary.json; 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/gate3_trial_manifest.json; 0_trials/module2_gate3_formal/gate3_obstacle_summary_warm_approved_v1/gate3_formal_audit.json` (remote_training_not_completed)
  - missing `regenerate_h01_h02_formal_artifacts`: `0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json` (missing_remote_audit_pullback)
  - missing `regenerate_claim_gate_artifacts`: `` (h02_formal_acceptance_not_ready)
- `remote_training_outputs` (training): complete=`True`, blocked_by=``
- `gate3_evaluation_outputs` (evaluation): complete=`True`, blocked_by=``
- `gate3_acceptance_pullback` (acceptance): complete=`True`, blocked_by=``
- `h01_h02_formal_evaluation_acceptance` (evaluation_acceptance): complete=`False`, blocked_by=`h02_formal_output_acceptance`
  - missing `h02_formal_output_acceptance`: `0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json` (h02_verdict_not_formal, gate3_formal_audit_not_passed, h02_scale_below_h01_manifest, missing_ppo_result_rows)
- `claim_gate_regeneration` (claim_gate): complete=`False`, blocked_by=`h02_formal_acceptance_before_claim_gate`
  - missing `h02_formal_acceptance_before_claim_gate`: `0_trials/module2_h02_formal_acceptance/h02_formal_acceptance.json` (claim gate cannot be regenerated from blocked H02 outputs)

## Audit Issues

- none

## Claim Boundaries

- This audit lists missing formal-gate evidence; it does not run training, preflight, sync, audit, pullback, or evaluation.
- A complete file list is still not a paper claim unless Gate3 audit passes, hashes are recorded, H01 is ready, and H02 accepts formal outputs.
- F02.6 approval by Dr Sun is required before obstacle-summary warm-start formal training.
- PPO formal training remains gpu3070ti-relay-only; local training remains prohibited.
- This artifact is a gate inventory, not result-table or appendix material.
