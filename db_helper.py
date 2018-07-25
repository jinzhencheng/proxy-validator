# -*- coding: utf-8 -*-
# created by jinzc (jinzc@yiche.com) at 2017/02/07 (last update time)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func

import config
from proxy_info import ProxyInfo


class DBOperator(object):
    """
    Database operation class
    """
    session = None

    def __init__(self):
        self.mysql_uri = config.MYSQL_URI

    def query_count(self):
        """
        Query total count
        :return:
        """
        if not self.session:
            self.__open_driver()
        count = self.session.query(func.count(ProxyInfo.id)).scalar()
        self.__close_driver()
        return count

    def query(self):
        """
        Query 1000 items
        :return: proxy list contains many proxy items.
        """
        if not self.session:
            self.__open_driver()
        proxy_list = self.session.query(ProxyInfo).order_by(ProxyInfo.id.desc()).all()
        for proxy in proxy_list:
            self.session.expunge(proxy)
        return proxy_list

    def update(self, proxy_list):
        """
        Update when porxy is valid
        :param proxy_list: proxy list
        """
        if not self.session:
            self.__open_driver()
        for proxy in proxy_list:
            self.session.query(ProxyInfo).filter(ProxyInfo.id == proxy.id).update({"delay": proxy.delay,
                                                                                   "update_time": proxy.update_time})
        self.session.commit()
        self.__close_driver()
    pass

    def delete(self, proxy_list):
        """
        Batch update
        :param proxy_list: Invalid proxy list
        :return:None
        """
        if not self.session:
            self.__open_driver()
        for proxy in proxy_list:
            self.session.delete(proxy)
        self.session.commit()
        self.__close_driver()

    def __open_driver(self):
        """
        Connection establishment
        :return:None
        """
        self.engine = create_engine(self.mysql_uri)
        self.DBSession = sessionmaker(bind=self.engine)
        self.session = self.DBSession()
    
    def __close_driver(self):
        """
        Connection be closed
        :return:None
        """
        self.session.close()
    pass

