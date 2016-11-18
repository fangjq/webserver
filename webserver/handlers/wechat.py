import json
import tornado.web

import hashlib
import logging
from handlers.base import BaseHandler
import xml.etree.ElementTree
import time
from urllib import urlencode
from urllib import unquote

import traceback
try:
    # from parser.main import get_crawled_result
    # from parser import config
    from parser.main import *
except:
    traceback.print_exc()

logger = logging.getLogger(__name__)

class WeChatTokenHandler(BaseHandler):

    def get(self):
        signature = self.get_argument("signature", default=None, strip=True)
        timestamp = self.get_argument("timestamp", default=None, strip=True)

        nonce = self.get_argument("nonce", default=None, strip=True)
        echostr = self.get_argument("echostr", default=None, strip=True)

        token = "creditease"
        l = [token, timestamp, nonce]
        l.sort()
        sha1 = hashlib.sha1()
        map(sha1.update, l)
        hashcode = sha1.hexdigest()

        logger.info("nonce: " + nonce)
        logger.info("timestamp: " + timestamp)
        logger.info("hashcode: " + hashcode)
        logger.info("signature: " + signature)
        logger.info("echostr: " + echostr)

        if hashcode == signature:
            self.write(echostr)
            self.flush()

    def post(self):
        try:
            request_data = self.request.body

            xml_obj = xml.etree.ElementTree.fromstring(request_data)

            content = xml_obj.find("Content").text
            msg_type = xml_obj.find("MsgType").text
            from_user = xml_obj.find("FromUserName").text
            to_user = xml_obj.find("ToUserName").text

            url_params = urlencode({
                "link": content
            })

            self.render("reply_url.xml", from_user=to_user, to_user=from_user,
                    title="Test", description="test", picurl="http://",
                    url="http://10.106.161.146:8000/h5?" + url_params)
            # self.render("reply_text.xml", from_user=from_user, to_user=to_user,
                    # content=content)

        except Exception as e:
            logger.error(repr(e))

class WeChatH5Handler(BaseHandler):

    def get(self):
        link = unquote(self.get_argument("link"))
        logger.info("received link:" + link)
        self.render("index.html")
