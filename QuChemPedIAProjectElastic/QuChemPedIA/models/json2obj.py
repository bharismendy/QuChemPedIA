import json
from collections import namedtuple


def json2obj(data):
    try:
        data = json.dumps(data)
        data = data.replace('_', '')
        loaded_json = json.loads(data)
        try:
            inchi = loaded_json['molecule']['inchi'].strip()
            print(inchi)
        except Exception as error:
            print("error for getting the InChi : ")
            print(error)


    except Exception as error:
        print(error)
    return None
