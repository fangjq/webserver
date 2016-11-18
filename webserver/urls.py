from handlers.health import HealthHandler
from handlers.wechat import WeChatTokenHandler
from handlers.wechat import WeChatH5Handler
from handlers.wechat import WeChatEvalResultHandler
url_patterns = [
    (r"/health", HealthHandler),
    (r"/sync", WeChatTokenHandler),
    (r"/h5", WeChatH5Handler),
    (r"/eval-result", WeChatEvalResultHandler),
]
