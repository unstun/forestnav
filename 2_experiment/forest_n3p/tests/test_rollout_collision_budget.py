from forest_n3p.scripts.run_rollout_collision_budget import sample_policy_like_rollout, steering_fraction_sequence
from forest_n3p.third_party.pathplan import AckermannParams, AckermannState


def test_steering_fraction_sequence_is_deterministic_and_repeats():
    assert steering_fraction_sequence(10) == (-0.65, -0.25, 0.0, 0.35, 0.70, 0.25, -0.35, 0.0, -0.65, -0.25)


def test_policy_like_rollout_sample_count_matches_collision_step():
    samples, final_state = sample_policy_like_rollout(
        start=AckermannState(1.0, 1.0, 0.0),
        params=AckermannParams(wheelbase=0.6, min_turn_radius=1.1284),
        rollout_step_count=8,
        action_step_m=0.3,
        collision_sample_step_m=0.1,
    )

    assert len(samples) == 25
    assert final_state.x > 1.0
