import time
import cv2
import logging
import os

from src.globals.consts.logger_messages import LoggerMessages
from src.infrastructure.factories.logger_factory import LoggerFactory
from src.globals.consts.consts_strings import ConstsStrings

logger = LoggerFactory.get_logger_manager()
logger.log(ConstsStrings.LOG_NAME_INFO,
                             LoggerMessages.CURRENT_DIRECTORY_INFO.format(os.getcwd()), level=logging.INFO) 

video_path = "/home/admin-admin/Downloads/video3.mp4"
cap = cv2.VideoCapture(video_path)
for i in range(10):
    if cap.isOpened():
        logger.log(ConstsStrings.LOG_NAME_INFO,
                             LoggerMessages.CAPTURE_OPEN_SUCCESSFULLY, level=logging.INFO) 
        break
    logger.log(ConstsStrings.LOG_NAME_WARNING,
                             LoggerMessages.ATTEMPT_NOT_OPEN_YET.format(i+1), level=logging.WARNING) 
    time.sleep(0.5)
else:
    logger.log(ConstsStrings.LOG_NAME_ERROR,
                             LoggerMessages.FAIL_TO_OPEN_CAPTURE_AFTER_5_SECONDS, level=logging.ERROR) 