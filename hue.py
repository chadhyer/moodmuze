import re
import requests
import json

def check_response(data):
    if bool(re.match('\[{"error":{', data)):
        json_error = json.loads(data)
        print(str(json_error))
        exit('An error has occurred')
    else:
        return True


class Light:

    def __init__(self, id, data):
        self.id = id
        self.conf = json.loads(json.dumps(data))


class Group:

    def __init__(self, id, data):
        self.id = id
        self.conf = json.loads(json.dumps(data))


class Bridge:

    def __init__(self, ip, auth_key, proxy):
        self.auth_token = 'http://' + ip + '/api/' + auth_key + '/'
        try:
            self.proxy = proxy
        except:
            self.proxy = None
        self.encoding = 'utf-8'
        self.lights = []
        self.groups = []

    def get_config(self):
        url = self.auth_token + 'config'
        response = requests.get(url, proxies=self.proxy)
        data = str(response.content, self.encoding)
        
        check_response(data)
        
        self.conf = json.loads(data)

    def get_item_list(self, kind):
        if kind != 'lights' and kind != 'groups':
            exit('Kind must be lights or groups!')
        url = self.auth_token + kind
        response = requests.get(url, proxies=self.proxy)
        data = str(response.content, self.encoding)
        
        check_response(data)

        json_data = json.loads(data)
        for obj in json_data:
            if kind == 'lights':
                self.lights.append(Light(obj, json_data[obj]))
            elif kind == 'groups':
                self.groups.append(Group(obj, json_data[obj]))

    def get_object_info(self, obj, kind):
        url = self.auth_token + kind + '/' + obj.id
        response = requests.get(url, proxies=self.proxy)
        data = str(response.content, self.encoding)
        
        check_response(data)

        obj.conf = json.loads(data)
        #json_data = json.loads(data)
        #obj.load_state(json_data["state"])
        #if kind == 'groups':
        #    obj.load_action(json_data["action"])

    def update_object(self, obj, kind, body, state_action):
        url = self.auth_token + kind + '/' + obj.id + state_action
        response = requests.put(url, body, proxies=self.proxy)
        data = str(response.content, self.encoding)

        check_response(data)
        
        self.get_object_info(obj, kind)

