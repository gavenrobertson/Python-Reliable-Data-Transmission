
from unreliable import *

class RDTLayer(object):
    # The length of the string data that will be sent per packet...
    # ########################################################################
    # Step 1: Change the DATA_LENGTH so it can send multiple chars in one packets 
    # ########################################################################
    # YOUR CODE HERE:
    
    DATA_LENGTH = 1 # characters

    # Receive window size for flow-control
    # max num of packet sent in 1 iteration: FLOW_CONTROL_WIN_SIZE / DATA_LENGTH

    # ########################################################################
    # Step 1: Change the FLOW_CONTROL_WIN_SIZE so it matches DATA_LENGTH 
    # ########################################################################
    # YOUR CODE HERE:
    
    FLOW_CONTROL_WIN_SIZE = 1 # characters

    # ########################################################################
    # Step 2: Change the FLOW_CONTROL_WIN_SIZE so it can send multiple packets a time
    # ########################################################################
    # YOUR CODE HERE:
    

    # ########################################################################
    # Step 4: declare and initialize a variable, MAX_ITERATIONS_SEGMENT_TIMEOUT, 
    #         which shows maximum iterations allowed before it is considered timeout
    # i.e., suppose a segment was sent in iteration 5, it is timout if not received/ACKed at the end of iteration 7, 
    #       then set MAX_ITERATIONS_SEGMENT_TIMEOUT to 2 (7-5)
    # ########################################################################
    # YOUR CODE HERE:
    

    # Add class members as needed...

    
    def __init__(self):
        self.sendChannel = None
        self.receiveChannel = None

        self.sendWinStart = 0
        self.dataToSend = ''
        self.dataReceived = [] # <--- Use this list to deliver data 
        self.dictSent = {} # <--- Use this dictionary to keep track of sent segments
        self.dictReceived = {} # <--- Use this dictionary to keep track of received segments in Step 3
        self.currentIteration = 0 # <--- Use this for segment 'timeouts' in Step 4
        self.countSegmentTimeouts = 0 # <--- Use this for segment 'timeouts' in Step 4
        self.countChecksumErrors = 0 # <--- Use this to count segments have checksum error in Step 5  

    # Called by main to set the unreliable sending lower-layer channel
    def setSendChannel(self, channel):
        self.sendChannel = channel

    # Called by main to set the unreliable receiving lower-layer channel
    def setReceiveChannel(self, channel):
        self.receiveChannel = channel

    # Called by main to set the string data to send
    def setDataToSend(self,data):
        self.dataToSend = data

    # Called by main to get the currently received and buffered string data, in order
    def deliver_data(self):
        # ########################################################################
        # Step 3: use dictReceived, deliver data in the correct order
        # hints: 
        # 1. use sorted()
        # 2. make sure dataReceived is empty before appending 
        # ########################################################################
        # YOUR CODE HERE:

         
        return ''.join(self.dataReceived)


    # ########################################################################
    # Step 3: Implement the following function so that it returns the cumulative ack in dictReceived
    # i.e., assuming DATA_LENGTH = 4, 
    #       if the values of key are [0, 4, 8], then return value is 12 
    #       if the values of key are [0, 4, 12, 16], then return value is 8, since seg of seqnum 8 is missing
    # ########################################################################
    def getCumAck(self):
        # YOUR CODE HERE:
        print ("getCumAck")
       


    # "timeslice". Called by main once per iteration
    def manage(self):
        self.currentIteration += 1

        # check if any sent packets timeout
        self.manageSegmentTimeouts()
        
        # both client and server would call rdt_send() and rdt_recv()
        # but we will handle cases like nothing to send/recv inside those functions 
        self.rdt_send()
        self.rdt_recv()


    # Manage Sent Segment timeouts...
    # ########################################################################
    # Step 4: implement the following function 
    # hint: compare currentIteration - seg's start iteration with RDTLayer.MAX_ITERATIONS_SEGMENT_TIMEOUT
    # note: you cannot change dictionary during iteration
    # ########################################################################
    def manageSegmentTimeouts(self):
        # YOUR CODE HERE:
        print ("manage timeouts")


    # ########################################################################
    # EXTRA CREDIT Step: Remove all keys up to and including the provided one
    # ########################################################################
    def removeSentSegmentsToAndIncluding(self,maxkey):
        # YOUR CODE HERE:
        print ("extra credit function")


    # Manage Segment sending tasks...
    def rdt_send(self):
        print('rdt_send')

        # You should pipeline segments to fit the flow-control window
        # The flow-control window is the constant RDTLayer.FLOW_CONTROL_WIN_SIZE
        # The maximum data that you can send in a segment is RDTLayer.DATA_LENGTH
        # These constants are given in # characters

        # The data is just part of the entire string that you are trying to send.
        # The seqnum is the sequence number for the segment (in character number, not bytes)

        
        #if there is nothing to send (dataToSend is empty), return
        if not self.dataToSend:
            return

        # the sequence number is the first byte of the sending window
        seqnum = self.sendWinStart

        # ########################################################################
        # Step 2: pipelining: implement a loop to send multiple packets a time
        # ########################################################################
        # YOUR CODE HERE:

        # if the seqnum already in the sent list, then 
        # don't send the packet again, since we are waiting for its ack or timeout
        # ########################################################################
        # Step 2: modify the following if statement so it wouldn't return immediately
        # ########################################################################
        if seqnum in self.dictSent:
            # YOUR CODE HERE:
            
            return

        # ##############################################################################################
        # Step 2: add another condition, what if the current segment to be sent exceeds the window size?
        # ##############################################################################################
        # YOUR CODE HERE:

        
        # Get data from the dataToSend
        # ###################################################################################
        # Step 1: modify the following line so that it can send multiple chars in one packet
        # ###################################################################################
        # YOUR CODE HERE:
        
        data = self.dataToSend[seqnum]

        # create a data segment  
        seg = Segment()

        # set seqnum and data 
        seg.setData(seqnum,data)

        # display segment, for debugging purposes
        print("sending segment: ")
        seg.dump()

        # ###################################################################################
        # Step 4: set seg's start iteration 
        # ###################################################################################
        # YOUR CODE HERE:


        # Use the unreliable sendChannel to send the segment
        self.sendChannel.udt_send(seg)

        # Once the segment is sent, add the segment into sent dictionary
        # since now we are waiting for its ack or timeouts
        self.dictSent[seqnum] = seg




    # Manage Segment receive tasks...
    def rdt_recv(self):
        # This call returns a list of incoming segments (see UnreliableChannel class)...
        listIncoming = self.receiveChannel.receive()
        print('rdt_recv')

        # return if nothing received....
        if len(listIncoming) == 0:
            return

        # use a boolean flag, dataPacketsReceived to tell data segments apart from ack segemnts
        # assume they are not data packets
        dataPacketsReceived = False

        # create a variable to store acknowledge number 
        acknum = -1

        # loop through each segments in the incoming list
        for seg in listIncoming: 
            # if the seqnum is >=0, meaning it is a data segment
            if seg.seqnum >= 0:

                # ###########################################################################################
                # Step 5: handle dataErrors by checking checksum
                # hint: checkChecksum() in Segment class returns False if detects a checksum error, True otherwise
                # ###########################################################################################
                # YOUR CODE HERE:
                

                # append the data from segment to the list of data received
                # ###########################################################################################
                # Step 3: use dictReceived dictionary instead of dataReceived list to store the received segments 
                # ###########################################################################################
                # YOUR CODE HERE:

                self.dataReceived.append(seg.payload)

                # assign value to acknum, so it shows the next expected byte
                # ###########################################################################################
                # Step 1: modify the acknum so it correctly reflects the next expected byte 
                #         when a segment contains multiple chars
                # ###########################################################################################
                # YOUR CODE HERE:
                

                # ###########################################################################################
                # Step 3: modify the acknum so it gets the cumulative ack
                # hint: call getCumAck()
                # ###########################################################################################
                # YOUR CODE HERE:

                acknum = seg.seqnum + 1
                

                # change the dataPacketsReceived to True, indicating this is indeed a data packet
                dataPacketsReceived = True

                # display segment, for debugging purposes
                print("received data seg:")
                seg.dump()

            # if the acknum is >= 0, meaning it is a ack segment
            elif seg.acknum >= 0:
                # once received an ack, shift the starting point of the sending window 
                self.sendWinStart = seg.acknum

                # display segment, for debugging purposes
                print("received ack:")
                seg.dump()

                # ########################################################################
                # EXTRA Credit Step: # remove the segment from sent dictionary
                # hint: cumulative ack? Call removeSentSegmentsToAndIncluding()
                # ########################################################################
                # YOUR CODE HERE:
                
        
        # if data packet is received, send ack immediately
        if dataPacketsReceived: 
            # create an ack packet 
            ack = Segment()

            # set the ack num
            ack.setAck(acknum)

            # display packet, for debugging purpose 
            print("sending ack:")
            ack.dump()

            # Use the unreliable sendChannel to send the ack packet
            self.sendChannel.udt_send(ack)
