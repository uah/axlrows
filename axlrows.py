from suds.client import Client
import json
from ptpython import repl

class CiscoUCM:
    def __init__(self):
        print("Loading configuration")
        with open('config.json', 'r') as file:
            config = json.loads(file.read())
            print("Bringing up client")
            self.__client = Client(config['wsdl'], location=config['location'], username=config['username'], password=config['password'])

    def get_phones(self, **kwargs):
        try:
            uuids = [x._uuid for x in self.__client.service.listPhone(kwargs)[0][0]]
            return (self.__client.service.getPhone(uuid=uuid)[0][0] for uuid in uuids)
        except IndexError:
            return iter(()) #empty generator

    def get_phone(self, **kwargs):
        try:
            phones = self.__client.service.listPhone(kwargs)[0][0]
            uuid = phones[0]._uuid
            return self.__client.service.getPhone(uuid=uuid)[0][0]
        except IndexError:
            return None
    
    def update_phone(self, phone, **kwargs):
        self.__client.service.updatePhone(uuid=phone._uuid, **kwargs)

    def apply_phone(self, phone):
        self.__client.service.applyPhone(uuid=phone._uuid)

    def get_lines(self, dn):
        try:
            lines = uuid=self.__client.service.listLine({'pattern':dn})[0][0]
        except IndexError:
            return None
        uuids = [line._uuid for line in lines]
        return [self.__client.service.getLine(uuid=x)[0][0] for x in uuids]
        #return self.__client.service.getLine(uuid=uuid)[0][0]


if __name__ == "__main__":
    print("Making ucm object")
    ucm = CiscoUCM()

    print("Starting repl")
    #repl.embed(globals(), locals())
    method_names = [m for m in dir(ucm) if '__' not in m]
    repl.embed(dict(zip(method_names, [getattr(ucm, mn) for mn in method_names])), locals())

    quit()

    print("Querying")
    phone = ucm.get_phone(name='SEPBC671C30B2F7')

    lines = phone.lines[0]
    print(lines)

    dns = [line.dirn.pattern for line in lines]
    print("DNs on this phone: ")
    print(dns)

    for dn in dns:
        line = ucm.get_line(dn)
        print("DN " + dn + " appears on:")
        print(line.associatedDevices[0])


