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
        self.__client.service.updateLine(uuid=phone._uuid, **kwargs)

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
    
    #Health checks
    def get_users_without_extensions(self):
        all_users = self.get_users(department='')
        bad_users = []
        for user in all_users:
            if user.primaryExtension == '' and user.associatedDevices == '' and user.associatedRemoteDestinationProfiles == '':
                bad_users.append(user)
        return bad_users

    def get_lines_in_holding_with_devices(self):
        holding_lines = self.get_lines(routePartitionName='Sys-Holding-PT')
        with_devices = []
        for line in holding_lines:
            if int(line.pattern[0]) in list(range(1, 7+1)) and line.associatedDevices != "":
                with_devices.append(line)
        return with_devices

    def run_health_check(self):
        print("Running VoIP Health Check at", datetime.now())

    #Cleanups
    def cleanup_lines_in_holding_with_devices(self):
        for line in self.get_lines_in_holding_with_devices():
            print("Moving", line.pattern, "to system extensions")
            self.update_line(line, newRoutePartitionName='Sys-Ext-PT')

    def cleanup_users_without_extensions(self):
        for user in self.get_users_without_extensions():
            print("Converting", user.userid, "to local")
            self.update_user(user, ldapDirectoryName="", userIdentity="")
            print("Removing", user.userid)
            self.remove_user(user)


