import logging
import os
from logging.handlers import TimedRotatingFileHandler
import datetime

# 기본 로그 디렉토리 설정
def make_default_log_dir():
    global LOG_DIRECTORY
    log_directory = os.path.join(os.getcwd(), 'logs')
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)
    return log_directory

def create_daily_log_file_name(directory):
    """
    날짜(년-월-일)만을 포함하는 로그 파일 이름을 생성하는 함수.
    이 함수는 전역 로그 파일의 이름을 생성하는 데 사용됩니다.
    생성된 파일 이름은 전역 로그를 위해 하루에 한 번씩만 변경되며,
    로그 데이터가 날짜별로 구분되어 저장됩니다.

    Args:
        directory (str): 로그 파일을 저장할 디렉토리 경로.

    Returns:
        str: 생성된 로그 파일의 전체 경로. 예: 'logs/app_2023-11-21.log'
    """
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    return os.path.join(directory, f'app_{current_date}.log')


def create_detailed_log_file_name(directory):
    """
    날짜와 시간(년-월-일_시-분-초)을 모두 포함하는 로그 파일 이름을 생성하는 함수.
    이 함수는 특정 모듈 또는 함수별 세부 로그 파일의 이름을 생성하는 데 사용됩니다.
    생성된 파일 이름은 각 로그 이벤트가 발생한 정확한 시점을 반영하며,
    이를 통해 더 세부적인 로그 관리가 가능합니다.

    Args:
        directory (str): 로그 파일을 저장할 디렉토리 경로.

    Returns:
        str: 생성된 로그 파일의 전체 경로. 예: 'logs/app_2023-11-21_15-45-30.log'
    """
    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return os.path.join(directory, f'app_{current_datetime}.log')


# 로그 핸들러 설정
def set_log_handler(log_file, log_level, log_format):
    log_handler = TimedRotatingFileHandler(log_file, when='midnight', backupCount=30)
    log_handler.setFormatter(logging.Formatter(log_format))
    return log_handler

# 로거 기본 설정
def setup_default_logger():
    logger = logging.getLogger()
    logger.setLevel(LOG_LEVEL)
    logger.handlers = [default_log_handler]

# 추가 로그 디렉토리 활성화
def enable_additional_logging(directory, logger_name):
    log_file = create_detailed_log_file_name(directory)
    log_handler = set_log_handler(log_file, LOG_LEVEL, LOG_FORMAT)
    logger = logging.getLogger(logger_name)
    logger.addHandler(log_handler)

# 추가 로그 디렉토리 비활성화
def disable_additional_logging(logger_name):
    logger = logging.getLogger(logger_name)
    for handler in logger.handlers[:]:
        if isinstance(handler, TimedRotatingFileHandler):
            logger.removeHandler(handler)


# 기본 로그 설정
LOG_LEVEL = logging.DEBUG
LOG_FORMAT = "%(asctime)s — %(levelname)s — %(message)s — in %(pathname)s:%(lineno)d"
LOG_DIRECTORY = default_log_dir = make_default_log_dir()
default_log_file = create_daily_log_file_name(default_log_dir)
default_log_handler = set_log_handler(default_log_file, LOG_LEVEL, LOG_FORMAT)

# 기본 로거 설정 적용
setup_default_logger()