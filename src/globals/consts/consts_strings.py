class ConstsStrings:
    #? paths
    optimzied_model_path = "resnet18_baseline_att_224x224_A_epoch_249_trt.pth"
    topology_pose_path = "assets/configs/human_pose_draw.json"
    topology_depth_path = "assets/configs/human_pose_draw.json"
    model_weights = "assets/weights_and_engines/resnet18_baseline_att_224x224_A_epoch_249.pth"

    #? keys:
    keypoints_key = "keypoints"
    skeleton_key = "skeleton"
    counts_key = "counts"
    objects_key = "objects"
    peaks_key = "peaks"
    frame_key = "frame"
    model_results_key = "model_results"
    state_key = "state"
    cameras_key = "cameras"
    key_key = "key"

    open_to_read = "r"
    host_root_path = "/host_root"
    encoder = 'utf-8'

    #? Kafka settings
    auto_offset_reset='earliest'
    group_id='my-group'
    configuration_path = "config/configuration.xml"
    bootstrap_servers_root = 'bootstrap_servers'
    kafka_root_configuration_name = "kafka_configuration"
    distance_trigger_topic_name = "distance_trigger_topic"
    distance_trigger_msg = "distance_trigger"

    #? ZMQ server connection
    base_tcp_connection_strings = "tcp://"

    # ? ZMQ request format identifiers
    resource_identifier = "resource"
    operation_identifier = "operation"
    data_identifier = "data"

    # ? ZMQ response format indentifiers
    status_identifier = "status"
    data_identifier = "data"

    # ? ZMQ resources
    config_resource = "config"

    # ? ZMQ operations
    get_data_operation = "get_data"

    # ? errors
    file_path_must_be_provided = "File path must be provided"
    error_parsing_XML = "Error parsing XML file"
    invalid_JSON_format = "Invalid JSON format"
    invalid_status_value_in_JSON = "Invalid status value in JSON:"
    error_message = "error"

    # ? env_keys
    zmq_server_host = "ZMQ_SERVER_HOST"
    zmq_server_port = "ZMQ_SERVER_PORT"
    camera_username_key = "CAMERA_USERNAME_KEY"
    camera_password_key = "CAMERA_PASSWORD_KEY"