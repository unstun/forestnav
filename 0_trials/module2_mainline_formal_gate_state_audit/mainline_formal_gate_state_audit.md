# Module2 Mainline Formal Gate State Audit

This file checks that the long-term Module2 mainline task book mirrors the current formal-gate state. It is not a training run, remote preflight, formal evaluation, or paper result.

- status: `mainline_formal_gate_state_audit_failed`
- audit_issue_count: `3`
- expected_next_action_id: `record_f02_6_decision`
- expected_next_action_mentioned: `True`
- total_missing_deliverables: `10`
- mainline_missing_deliverable_mention_count: `0`
- proof_summary_chain_status: `formal_gate_proof_summary_chain_audit_failed`
- proof_summary_handoff_single_next_action_consistency: `{'row_count': 3, 'consistent_row_count': 1}`
- executes_commands: `False`
- runs_training: `False`
- runs_remote_preflight: `False`
- formal_claim_allowed: `False`

## Audit Issues

- `mainline_missing_proof_chain_status`: Mainline task book must mention the current proof-summary chain status.
- `proof_summary_chain_has_audit_issues`: Mainline task-book state should only mirror a clean proof-summary chain.
- `proof_summary_chain_handoff_single_next_action_inconsistent`: Proof-summary chain must agree on the handoff single-next-action index before mainline mirrors it.

## Missing Formal Deliverables

- `training:train_final_model_zip`: artifact_id=`train_final_model_zip`, mentioned=`True`, mentioned_in_current_section=`True`
- `training:train_summary_json`: artifact_id=`train_summary_json`, mentioned=`True`, mentioned_in_current_section=`True`
- `training:train_training_manifest_json`: artifact_id=`train_training_manifest_json`, mentioned=`True`, mentioned_in_current_section=`True`
- `evaluation:eval_gate3_eval_episodes_csv`: artifact_id=`eval_gate3_eval_episodes_csv`, mentioned=`True`, mentioned_in_current_section=`True`
- `evaluation:eval_gate3_summary_json`: artifact_id=`eval_gate3_summary_json`, mentioned=`True`, mentioned_in_current_section=`True`
- `acceptance:gate3_trial_manifest_json`: artifact_id=`gate3_trial_manifest_json`, mentioned=`True`, mentioned_in_current_section=`True`
- `acceptance:gate3_formal_audit_json`: artifact_id=`gate3_formal_audit_json`, mentioned=`True`, mentioned_in_current_section=`True`
- `acceptance:pulled_back_checkpoint_hash_record`: artifact_id=`pulled_back_checkpoint_hash_record`, mentioned=`True`, mentioned_in_current_section=`True`
- `formal_acceptance:h01_ready_for_formal_run`: artifact_id=`h01_ready_for_formal_run`, mentioned=`True`, mentioned_in_current_section=`True`
- `formal_acceptance:h02_formal_output_acceptance`: artifact_id=`h02_formal_output_acceptance`, mentioned=`True`, mentioned_in_current_section=`True`

## Current Boundary Tokens

- `local training`: mentioned=`True`
- `remote preflight`: mentioned=`True`
- `remote training`: mentioned=`True`
- `formal claim`: mentioned=`True`
- `paper-result material`: mentioned=`True`
- `gpu3070ti-relay`: mentioned=`True`

## Claim Boundaries

- This audit only checks that the long-term mainline task book mirrors the current formal-gate state.
- It does not execute commands, run local training, run remote preflight, run remote PPO training, evaluate PPO, pull back artifacts, or write paper results.
- A consistent blocked audit does not prove PPO has replaced RS in formal evaluation.
- Formal PPO-vs-RS performance claims still require the missing training, evaluation, acceptance, and H01/H02 artifacts to be produced and audited.
