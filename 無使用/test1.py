from pyp2p.net import *
import time

me=Net(passive_bind="192.168.1.41",passive_port=4444, interface="eth0:2",node_type="passive",debug=1)
me.start()
me.bootstrap()
me.advertise()

while True:
	for con in me:
		for reply in con:
			print(reply)
	time.sleep(1)