import json

def encode(o: object):
    return json.dumps(o.__dict__)

def decode(json_str: str, cls: object):
    return decoder(json.loads(json_str), cls)

def decoder(json, cls: object):
    obj = object.__new__(cls)
    obj.__init__()

    for k in obj.__dict__:
        if k in json:
            obj.__dict__[k] = json[k]
    
    return obj