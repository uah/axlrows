from suds.client import Client
import json

print("Loading configuration")
with open('config.json', 'r') as file:
    config = json.loads(file.read())

print("Bringing up client")
client = Client(config['wsdl'],location=config['location'], username=config['username'], password=config['password'])

print("Querying")
phone = client.service.getPhone(uuid=client.service.listPhone({'name':'SEP6C416A3693DE'})[0][0][0]._uuid)[0][0]

lines = phone.lines[0]
print(lines)

dns = [line.dirn.pattern for line in lines]
print("DNs on this phone: ")
print(dns)

for dn in dns:
    line = client.service.getLine(uuid=client.service.listLine({'pattern':dn})[0][0][0]._uuid)[0][0]
    print("DN " + dn + " appears on:")
    print(line.associatedDevices[0])

print("Shutting down")

