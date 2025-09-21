import logging

class Logger:
    def __init__(self, name="AutoIrriga"):
        self._logger = logging.getLogger(name)
        self._logger.setLevel(logging.INFO)

        if not self._logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s', '%Y-%m-%d %H:%M:%S')
            handler.setFormatter(formatter)
            self._logger.addHandler(handler)

    def info(self, msg):
        self._logger.info(msg)

    def warn(self, msg):
        self._logger.warning(msg)

    def error(self, msg):
        self._logger.error(msg)