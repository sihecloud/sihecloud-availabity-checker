import logging
from logging.handlers import TimedRotatingFileHandler
import sys
import os

os.makedirs("data", exist_ok=True)

LOG_FILEANME = "./data/checker.log"
my_logger = logging.getLogger('checker')
my_logger.setLevel(logging.INFO)
my_handler = TimedRotatingFileHandler(LOG_FILEANME, when='midnight', interval=1, backupCount=7)
my_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
my_handler.setFormatter(my_formatter)
my_logger.propagate = False
my_logger.addHandler(my_handler)

# 创建控制台处理器
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
my_logger.addHandler(console_handler)
