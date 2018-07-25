# -*- coding: utf-8 -*-
# created by jinzc at 2017/02/08

import logging


class Logger(object):

    def __init__(self, name, filename):
        """
        Initlializing logger for logging
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        handler = logging.FileHandler(filename)
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    pass

    def get_logger(self):
        return self.logger


