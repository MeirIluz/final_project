class Maps:
    body_part_lengths_statistically = {
        "right_upper_hand": 37.2618,
        "left_upper_hand": 37.2618,
        "right_lower_hand": 27.9,
        "left_lower_hand": 27.9,
        "right_upper_leg": 41.61,
        "left_upper_leg": 41.61,
        "right_lower_leg": 37.8,
        "left_lower_leg": 37.8,
    }

    body_part_connections = {
        (5, 7): "left_upper_hand",
        (6, 8): "right_upper_hand",
        (7, 9): "left_lower_hand",
        (8, 10): "right_lower_hand",
        (15, 13): "left_lower_leg",
        (14, 12): "right_upper_leg",
        (16, 14): "right_lower_leg",
        (13, 11): "left_upper_leg",
    }

    data_field_to_internal_variable = {
        "counts": "_counts",
        "objects": "_objects",
        "peaks": "_peaks",
        "frame": "_frame"
    }
