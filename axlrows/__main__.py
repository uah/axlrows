from axlrows import CiscoUCM
from ptpython import repl

print("Making ucm object")
ucm = CiscoUCM()

print("Starting repl")
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
