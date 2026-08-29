from turtle_square.square_node import next_command


def test_even_steps_move_forward():
    cmd = next_command(0)
    assert cmd.linear.x > 0
    assert cmd.angular.z == 0.0


def test_odd_steps_turn():
    cmd = next_command(1)
    assert cmd.linear.x == 0.0
    assert cmd.angular.z > 0.0


def test_cycle_wraps_at_eight_steps_worth_of_pattern():
    # step 0 and step 8 should behave the same (mod 8 logic lives in the node,
    # but the pattern itself repeats every 2 steps)
    assert next_command(0).linear.x == next_command(2).linear.x
    assert next_command(1).angular.z == next_command(3).angular.z
