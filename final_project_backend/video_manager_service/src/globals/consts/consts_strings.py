class ConstsStrings:
    VERSION = "0.1.0"
    # ? paths
    MODEL_NET = "yolov8s_pose.hef"

    # ? keys:
    KEYPOINTS_KEY = "keypoints"
    FRAME_KEY = "frame"
    DETECTION_STATE_KEY = "state"
    CAMERAS_KEY = "cameras"
    KEY_KEY = "key"
    CONFIDENCE_KEY = "confidence"
    X_POINT_KEY = "x"
    Y_POINT_KEY = "y"
    JOINT_SCORES_KEY = "joint_scores"
    SCORES_KEY = "scores"
    CAMERA_NAME_KEY = "camera_name"
    EXIT_KEY_IMSHOW = "q"
    CAMERA_ID_KEY = "camera_id"
    CAMERA_PORT_KEY = "camera_port"
    CAMERA_IP_KEY = "camera_ip"
    CAMERA_PASSWORD_KEY = "camera_password"
    CAMERA_USERNAME_KEY = "camera_username"
    CAMERA_PROTOCOL_KEY = "camera_protocol"
    PROCESS_VIDEO_KEY = "process_video"

    # ? general
    ENCODER = "utf-8"
    ALL_FILES_PATTERN = "*"
    RGB_FORMAT = "RGB"
    FORMAT_FLOAT = "FLOAT32"
    IMSHOW_HEADLINE = "Processed Frames"
    IMSHOW_WINDOW_NAME = "Main View"
    CSV_FILE_NAME = "debug_output_{}.csv"

    # ? Kafka settings
    AUTO_OFFSET_RESET = "earliest"
    GROUP_ID = "my-group"
    CONFIGURATION_PATH = "config/configuration.xml"
    BOOTSTRAP_SERVERS_ROOT = "bootstrap_servers"
    KAFKA_ROOT_CONFIGURATION_NAME = "kafka_configuration"
    DISTANCE_TRIGGER_TOPIC_NAME = "distance_trigger_topic"
    DISTANCE_TRIGGER_MSG = "distance_trigger"

    # ? ZMQ server connection
    BASE_TCP_CONNECTION_STRINGS = "tcp://"

    # ? ZMQ request/response format identifiers
    RESOURCE_IDENTIFIER = "resource"
    OPERATION_IDENTIFIER = "operation"
    DATA_IDENTIFIER = "data"
    STATUS_IDENTIFIER = "status"

    # ? ZMQ resources
    CONFIG_RESOURCE = "config"

    # ? ZMQ operations
    GET_DATA_OPERATION = "get_data"

    # ? errors
    ERROR_PARSING_XML = "Error parsing XML file"
    INVALID_JSON_FORMAT = "Invalid JSON format"
    INVALID_STATUS_VALUE_IN_JSON = "Invalid status value in JSON:"
    ERROR_MESSAGE = "error"

    # ? env_keys
    ZMQ_SERVER_HOST = "ZMQ_SERVER_HOST"
    ZMQ_SERVER_PORT = "ZMQ_SERVER_PORT"
    ACTIVE_CHILD_DISTANCE = "ALGORITHM_GET_CHILD_DISTANCE"
    TEST_MODE_ENV = "ALGORITHM_TEST_MODE"
    FRAME_WIDTH_KEY = "FRAME_WIDTH"
    FRAME_HEIGHT_KEY = "FRAME_HEIGHT"
    FRAME_RATE_KEY = "FRAME_RATE"

    # ? video
    ONVIF_PATH = "h264"
    AXIS_PATH = "axis-media/media.amp?adjustablelivestream=1"
    SHARED_MEMORY_CAM_PATH = "/dev/shm/cam{camera_id}"
    SHARED_MEMORY_PATH = "/dev/shm/"
    VIDEO_PIPELINE_RTSP = (
        "rtspsrc location=rtsp://{camera_username}:{camera_password}@{camera_ip}:{camera_port}/{protocol_path} "
        "latency=10 ! "
        "rtph264depay ! "
        "h264parse ! "
        "avdec_h264 ! "
        "videoscale ! "
        "video/x-raw, width={frame_width}, height={frame_height} ! "
        "videoconvert ! "
        "appsink drop=true sync=false"
    )
    SHARED_MEMORY_PIPELINE = (
        "appsrc is-live=true do-timestamp=true ! "
        "video/x-raw,format=BGR,width={frame_width},height={frame_height},framerate={frame_rate}/1 ! "
        "videoconvert ! videoscale ! "
        "video/x-raw,format=I420,width={scaled_width},height={scaled_height} ! "
        "shmsink socket-path={shared_memory_path} sync=false wait-for-connection=false shm-size=200000000"
    )
    DATE_AND_TIME_FORMAT = "%Y-%m-%d_%H-%M-%S"

    # ? Log
    LOG_NAME_DEBUG = "debug"
    LOG_NAME_ERROR = "error"
    LOG_NAME_INFO = "info"
    LOG_NAME_WARNING = "warning"
    LOG_NAME_CRITICAL = "critical"
    LOG_ENV = "LOG_FILE_PATH"
    LOG_FILEPATH = "./logs/{}_{}.log"
    LOG_MODE = "a"
    LOG_FORMATTER = "%(asctime)s - %(levelname)s - %(message)s"
    DATE_TIME_FORMAT = '%Y_%m_%d-%H_%M_%S'

    # Custom log level names
    ALGORITHM_MANAGER_CRITICAL_LOG_LEVEL_NAME = "ALGORITHM Manager Critical"
    ALGORITHM_MANAGER_ERROR_LOG_LEVEL_NAME    = "ALGORITHM Manager Error"
    ALGORITHM_MANAGER_WARNING_LOG_LEVEL_NAME  = "ALGORITHM Manager Warning"
    ALGORITHM_MANAGER_INFO_LOG_LEVEL_NAME     = "ALGORITHM Manager Info"
    ALGORITHM_MANAGER_DEBUG_LOG_LEVEL_NAME    = "ALGORITHM Manager Debug"
    
    # ? shared memory prefixes
    SHARED_MEMORY_FILES_PREFIXES = ["cam", "shmpipe"]
