class Maps:
    BODY_PART_LENGTHS_STATISTICALLY = {
        "right_upper_hand": 37.2618,
        "left_upper_hand": 37.2618,
        "right_lower_hand": 27.9,
        "left_lower_hand": 27.9,
        "right_upper_leg": 41.61,
        "left_upper_leg": 41.61,
        "right_lower_leg": 37.8,
        "left_lower_leg": 37.8,
        "shoulders": 40,
        "hips": 31,
    }

    BODY_PART_NAME_TO_INDEXES = {
        "shoulders": (5, 6),
        "hips": (11, 12),
        "right_upper_hand": (5, 7),
        "left_upper_hand": (6, 8),
        "right_lower_hand": (7, 9),
        "left_lower_hand": (8, 10),
        "left_upper_leg": (11, 13),
        "right_upper_leg": (12, 14),
        "left_lower_leg": (13, 15),
        "right_lower_leg": (14, 16)
    }

    KEYPOINT_INDEX_TO_NAME = {
        0: "nose",
        1: "left_eye",
        2: "right_eye",
        3: "left_ear",
        4: "right_ear",
        5: "left_shoulder",
        6: "right_shoulder",
        7: "left_elbow",
        8: "right_elbow",
        9: "left_wrist",
        10: "right_wrist",
        11: "left_hip",
        12: "right_hip",
        13: "left_knee",
        14: "right_knee",
        15: "left_ankle",
        16: "right_ankle"
    }
