import time

time.sleep(2)

newCode = None
with open('updateMain.py', 'r') as myfile:
    newCode = myfile.read()

with open('trigger.py', 'w') as myfile:
    myfile.write(newCode)

time.sleep(1)

#Make into system restart
exec(open("trigger.py").read())