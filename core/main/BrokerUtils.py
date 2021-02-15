import json
import SysConfigUtils


class BrokerUtils:
    def __init__(self):
        pass

    def getPort(self, name: str) -> str:
        config = SysConfigUtils.getConfig()
        return config["PORTS"][name]

    # Encode to Json
    def mogrify(self, topic, msg):
        # prepend topic and encode Json
        return str(topic) + ' ' + json.dumps(msg)

    # Convert Json to readable msg
    def demogrify(self, topicmsg):
        json0 = topicmsg.find('{')
        topic = topicmsg[0:json0].strip()
        msg = json.loads(topicmsg[json0:])
        return topic, msg