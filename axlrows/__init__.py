from suds.client import Client
import json
from datetime import datetime

__all__ = ['CiscoUCM']

class CiscoUCM:
    def __init__(self):
        with open('config.json', 'r') as file:
            config = json.loads(file.read())
            self.__client = Client(config['wsdl'], location=config['location'], username=config['username'], password=config['password'])

    def get_phones(self, **kwargs):
        try:
            uuids = [x._uuid for x in self.__client.service.listPhone(kwargs)[0][0]]
            return (self.__client.service.getPhone(uuid=uuid)[0][0] for uuid in uuids)
        except IndexError:
            return iter(()) #empty generator
    
    def update_phone(self, phone, **kwargs):
        self.__client.service.updatePhone(uuid=phone._uuid, **kwargs)

    def apply_phone(self, phone):
        self.__client.service.applyPhone(uuid=phone._uuid)

    def get_lines(self, **kwargs):
        try:
            uuids = [x._uuid for x in self.__client.service.listLine(kwargs)[0][0]]
            return (self.__client.service.getLine(uuid=uuid)[0][0] for uuid in uuids)
        except IndexError:
            return iter(())

    def update_line(self, line, **kwargs):
        self.__client.service.updateLine(uuid=line._uuid, **kwargs)

    def get_users(self, **kwargs):
        try:
            uuids = [x._uuid for x in self.__client.service.listUser(kwargs)[0][0]]
            return (self.__client.service.getUser(uuid=uuid)[0][0] for uuid in uuids)
        except IndexError:
            return iter(()) #empty generator

    def update_user(self, user, **kwargs):
        self.__client.service.updateUser(uuid=user._uuid, **kwargs)

    def remove_user(self, user):
        self.__client.service.removeUser(uuid=user._uuid)


    def execute_sql_update(self, **kwargs):
        self.__client.service.executeSQLUpdate(**kwargs)

    
