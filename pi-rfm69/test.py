#!/usr/bin/env python3

from RFM69 import Radio, FREQ_433MHZ
import datetime
import time

this_node_id = 1
network_id = 100
recipient_id = 2

with Radio(FREQ_433MHZ, this_node_id) as radio:
    print("Starting loop...")

    rx_counter = 0
    tx_counter = 0

    while True:

        # every 10 seconds, get packets
        if rx_counter > 10:
            rx_counter = 0
            for packet in radio.get_packets():
                print(packet)

        # every 5 seconds, send a message
        if tx_counter > 5:
            tx_counter = 0
            print("Sending...")
            if radio.send(2, "TEST", attempts=3, waitTime=100):
                print("Acknowledgement received")
            else:
                print("No acknowledgement")

        print("Listening...", len(radio.packets), radio.mode_name)
        delay = 0.5
        rx_counter += delay
        tx_counter += delay

        time.sleep(delay)
