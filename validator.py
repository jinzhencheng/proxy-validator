# -*- coding: utf-8 -*-
# created by jinzc at 2017/02/07

from db_helper import DBOperator
from logger import Logger
import time
import requests
import config
import threading
import Queue

logger = Logger(__name__, "proxy-validator.log").get_logger()


class Validator(threading.Thread):

    def __init__(self, name):
        threading.Thread.__init__(self)
        self.validator_name = name
        self.valid_proxies = []
        self.invalid_proxies = []
        self.db_helper = DBOperator()
        self.__queue = None

    @property
    def queue(self):
        return self.__queue

    @queue.setter
    def queue(self, value):
        if isinstance(value, Queue.Queue):
            self.__queue = value

    def run(self):
        self.validate_proxy(self.queue)

    def validate_proxy(self, queue):
        """
        Fetch proxy list from database,then update or delete
        """
        self.__check_ip(queue)
        self.__flush_to_db()
    pass

    def __flush_to_db(self):
        if len(self.valid_proxies) % 10 == 0 or self.queue.qsize() == 0:
            print " valid proxy (%d - %d) " % ((len(self.valid_proxies)), self.queue.qsize())
            self.db_helper.update(self.valid_proxies)
            self.valid_proxies = []
        if len(self.invalid_proxies) % 10 == 0 or self.queue.qsize() == 0:
            print " invalid proxy (%d - %d) " % ((len(self.valid_proxies)), self.queue.qsize())
            self.db_helper.delete(self.invalid_proxies)
            self.invalid_proxies = []

    def __check_ip(self, queue):
        """
        Checking ip is valid or not while testing the speed.
        :return: Proxy list which is contains a list of valid ip and speed.
        """
        while queue.qsize() != 0:
            print "( %s ) queue size is: %d" % (self.name, queue.qsize())
            proxy = queue.get()
            proxies = {"http": "http://%s:%s" % (proxy.ip, proxy.port)}
            start_time = time.time()
            try:
                resp = requests.get(url=config.REQUEST_SITE_URL,
                                    headers=config.HEADER,
                                    timeout=config.REQUEST_TIME_OUT,
                                    proxies=proxies)
                logger.info("response code:%s" % resp.status_code)
                print resp.content
                if resp.ok and resp.content:
                    print "%s:%s" % (proxy.ip, proxy.port)
                    end_time = time.time()
                    delay = (end_time - start_time) * 1000
                    proxy.delay = round(delay, 3)
                    proxy.update_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time))
                    self.valid_proxies.append(proxy)
                else:
                    self.invalid_proxies.append(proxy)
            except Exception, e:
                logger.info("Exception occured during checking ip, details:\n %s" % str(e))
                self.invalid_proxies.append(proxy)
            finally:
                self.__flush_to_db()
    pass

