import json


class Serializer:
    def __init__(self):
        pass

    # Encode to Json
    def json_mogrify(self, topic, data):
        # prepend topic and encode Json
        return str(topic) + ' ' + json.dumps(data)

    # Convert Json to readable message
    def json_demogrify(self, msg):
        json0 = msg.find('{')
        topic = msg[0:json0].strip()
        data = json.loads(msg[json0:])
        return topic, data