import json
import SysConfigUtils


class ClientUtils:
    def __init__(self):
        pass

    def getPort(self, name: str) -> str:
        config = SysConfigUtils.getConfig()
        return config["PORTS"][name]
    
    def getBrokerHost(self) -> str:
        config = SysConfigUtils.getConfig()
        return config["BROKER"]["host"]
    
    def increaseClientSize(self):
        SysConfigUtils.increaseSize("CLIENT")

    def decreaseClientSize(self):
        SysConfigUtils.decreaseSize("CLIENT")
    
    def tryReset(self):
        config = SysConfigUtils.getConfig()
        # Reset config file on certain condition
        if config["CLIENT"]["size"] == "0" and config["BROKER"]["size"] == "0":
            SysConfigUtils.reset()

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