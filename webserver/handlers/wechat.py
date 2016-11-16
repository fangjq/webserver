import json
import tornado.web

import hashlib
import logging
from handlers.base import BaseHandler

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
            return echostr

