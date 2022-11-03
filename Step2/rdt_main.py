
import time

from rdt_layer import *

################# Main ####################
################# Main ####################

dataToSend = "The quick brown fox jumped over the lazy dog"

dataToSend = "\r\n\r\n...We choose to go to the moon. We choose to go to the moon in this "\
"decade and do the other things, not because they are easy, but because they are hard, "\
"because that goal will serve to organize and measure the best of our energies and skills, "\
"because that challenge is one that we are willing to accept, one we are unwilling to "\
"postpone, and one which we intend to win, and the others, too."\
"\r\n\r\n"\
"...we shall send to the moon, 240,000 miles away from the control station in Houston, a giant "\
"rocket more than 300 feet tall, the length of this football field, made of new metal alloys, "\
"some of which have not yet been invented, capable of standing heat and stresses several times "\
"more than have ever been experienced, fitted together with a precision better than the finest "\
"watch, carrying all the equipment needed for propulsion, guidance, control, communications, food "\
"and survival, on an untried mission, to an unknown celestial body, and then return it safely to "\
"earth, re-entering the atmosphere at speeds of over 25,000 miles per hour, causing heat about half "\
"that of the temperature of the sun--almost as hot as it is here today--and do all this, and do it "\
"right, and do it first before this decade is out.\r\n\r\n"\
"JFK - September 12, 1962\r\n"

client = RDTLayer()
server = RDTLayer()

# Start with a reliable channel (all flags false)
outOfOrder = False    # <--- Change this to True in Step 3
dropPackets = False   # <--- Change this to True in Step 4
delayPackets = False  # <--- Change this to True in Step 4
dataErrors = False    # <--- Change this to True in Step 5

clientToServerChannel = UnreliableChannel(outOfOrder,dropPackets,delayPackets,dataErrors)
serverToClientChannel = UnreliableChannel(outOfOrder,dropPackets,delayPackets,dataErrors)

client.setSendChannel(clientToServerChannel)
client.setReceiveChannel(serverToClientChannel)

server.setSendChannel(serverToClientChannel)
server.setReceiveChannel(clientToServerChannel)

client.setDataToSend(dataToSend)

loopIter = 1
while True:
    print("loop: {0}".format(loopIter))
    print('')
    
    # Call the manage methods to make stuff happen
    print("***** client.manage *****")
    client.manage()
    print('')
    print("***** clientToServerChannel.manage *****")
    clientToServerChannel.manage()
    print('')
    print("***** server.manage *****")
    server.manage()
    print('')
    print("***** serverToClientChannel.manage *****")
    serverToClientChannel.manage()

    # show the data received so far
    dataReceived = server.deliver_data()
    print("dataReceived: {0}".format(dataReceived))

    if dataReceived == dataToSend:
        print('$$$$$$$$ ALL DATA RECEIVED $$$$$$$$')
        break

    loopIter += 1

    #time.sleep(0.1)
    #input("Press any key to continue...")

    if loopIter >= 1000:
        break

print("countTotalDataPackets: {0}".format(clientToServerChannel.countTotalDataPackets))
print("countSentPackets: {0}".format(clientToServerChannel.countSentPackets + serverToClientChannel.countSentPackets))
print("countChecksumErrorPackets: {0}".format(clientToServerChannel.countChecksumErrorPackets))
print("countOutOfOrderPackets: {0}".format(clientToServerChannel.countOutOfOrderPackets))
print("countDelayedPackets: {0}".format(clientToServerChannel.countDelayedPackets + serverToClientChannel.countDelayedPackets))
print("countDroppedDataPackets: {0}".format(clientToServerChannel.countDroppedPackets))
print("countAckPackets: {0}".format(serverToClientChannel.countAckPackets))
print("countDroppedAckPackets: {0}".format(serverToClientChannel.countDroppedPackets))

print("# segment timeouts: {0}".format(client.countSegmentTimeouts))

print("TOTAL ITERATIONS: {0}".format(loopIter))

print('')
print('...exactus...')
print('')