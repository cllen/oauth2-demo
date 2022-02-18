import sys
import logging
from .logstash_formatter import LogstashFormatterV1


def get_logstash_logger(py_file_path=__name__,level=logging.INFO):

	logger = logging.getLogger(py_file_path)
	handler = logging.StreamHandler(stream=sys.stdout)
	handler.setFormatter(LogstashFormatterV1())

	logger = logging.getLogger(py_file_path)
	logger.handlers = [handler]
	logger.propagate = False
	#logger.addHandler(handler)
	logger.setLevel(level)

	return logger