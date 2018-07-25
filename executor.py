# -*- coding: utf8 -*-
# created by  Jin(jinzhencheng@auto-smart.com) at 2017/09/18.

from validator import Validator
from logger import Logger
from db_helper import DBOperator
import time
import Queue
import config


logger = Logger(__name__, "proxy-validator.log").get_logger()


class Executor(object):

    def __init__(self):
        self.queue = Queue.Queue()
        self.db_helper = DBOperator()

    def __init_queue(self):
        proxy_list = self.db_helper.query()
        for proxy in proxy_list:
            self.queue.put(proxy)

    def execute(self):
        for i in range(0, config.DEFAULT_VALIDATE_THREAD):
            print i
            validator = Validator("validator_%d" % i)
            if self.queue.empty():
                self.__init_queue()
            logger.info("=== validator:%s has started, current queue size is: %d ===" % (i, self.queue.qsize()))
            validator.queue = self.queue
            validator.start()
            time.sleep(config.DEFAULT_VALIDE_SLEEP)
        logger.info("==== All thread have been executed. ===")


if __name__ == "__main__":
    exe = Executor()
    exe.execute()

