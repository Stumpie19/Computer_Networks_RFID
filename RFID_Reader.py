#!/usr/bin/env python

import RPi.GPIO as GPIO
import spidev
import signal
import time
import logging

class RFID_READER: