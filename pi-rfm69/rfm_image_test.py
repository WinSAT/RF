#!/usr/bin/env python

''' Test script for downlinking single image from satellite using Adafruit RFM69 tranceivers '''

import board
import busio
import digitalio
from io import BytesIO
from PIL import Image

import adafruit_rfm69

# Define radio parameters.
RADIO_FREQ_MHZ = 915.0  # Frequency of the radio in Mhz. Must match your
# module! Can be a value like 915.0, 433.0, etc.

# Define pins connected to the chip, use these if wiring up the breakout according to the guide:
CS = digitalio.DigitalInOut(board.D7)
RESET = digitalio.DigitalInOut(board.D25)

# Define the onboard LED - optional
LED = digitalio.DigitalInOut(board.D26)
LED.direction = digitalio.Direction.OUTPUT

# Initialize SPI bus.
spi = busio.SPI(board.D11, MOSI=board.D10, MISO=board.D9)

# Initialze RFM radio
rfm69 = adafruit_rfm69.RFM69(spi, CS, RESET, RADIO_FREQ_MHZ)

# Optionally set an encryption key (16 byte AES key). MUST match both
# on the transmitter and receiver (or be set to None to disable/the default).
rfm69.encryption_key = (
    b"\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08"
)

# Print out some chip state:
print("Temperature: {0}C".format(rfm69.temperature))
print("Frequency: {0}mhz".format(rfm69.frequency_mhz))
print("Bit rate: {0}kbit/s".format(rfm69.bitrate / 1000))
print("Frequency deviation: {0}hz".format(rfm69.frequency_deviation))

print("Waiting for packets...")

image = bytearray()

def downlink_image():

    while True:
        packet = rfm69.receive()
        # Optionally change the receive timeout from its default of 0.5 seconds:
        # packet = rfm69.receive(timeout=5.0)
        # If no packet was received during the timeout then None is returned.
        if packet is None:
            # Packet has not been received
            LED.value = False
            print("Received nothing! Listening again...")
        else:
            break

    while True:
        # Received a packet!
        LED.value = True
        print("Received (raw bytes): {0}".format(packet))

        # add packet to image
        image.extend(packet)
    
        packet = rfm69.receive()
        while packet is None:
            packet = rfm69.receive()

        # end bytes - meaning end of image
        if packet == bytearray(b'\x00\x01'):
            break

    # save image when done downlinking all packets
    #print(image)
    image1 = Image.open(BytesIO(image))
    image1.save("./image.jpg")
    #image1.show()

downlink_image()



