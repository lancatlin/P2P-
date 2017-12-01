from pyp2p.net import *
import time

#Setup Alice's p2p node.
alice = Net(passive_bind="192.168.1.41", passive_port=4, interface="eth0:2", node_type="passive", debug=1)
alice.start()
alice.bootstrap()
alice.advertise()

#Event loop.
while 1:
    for con in alice:
        for reply in con:
            print(reply)

    time.sleep(1)