#!/usr/bin/env python

import sys
import time
import random

import config as config

from iothub_client import IoTHubClient, IoTHubMessage, IoTHubClientError, IoTHubTransportProvider
from iothub_client import IoTHubMessageDispositionResult, IoTHubError

from light_sensor import LightSensor

if len(sys.argv) < 2:
    print ( "IoT Hub connection string and device ID must be provided as input" )
    sys.exit(0)

PROTOCOL = IoTHubTransportProvider.MQTT
CONNECTION_STRING = sys.argv[1]
# TODO: Get device ID from connection string?
DEVICE_ID = 'pi-001'

# Messages will time out after ten seconds
MESSAGE_TIMEOUT = 10000

# TODO: What are these for?
RECEIVE_CONTEXT = 0
TWIN_CONTEXT = 0
METHOD_CONTEXT = 0

SEND_CALLBACKS = 0
RECEIVE_CALLBACKS = 0
METHOD_CALLBACKS = 0
DO_SEND_MESSAGES = True

MESSAGE_COUNT = 0

MESSAGE_FORMAT_LIGHT = "{ 'deviceId': '%s', 'lux': %f, 'timestamp': '%s' }"

def print_message_details(message, counter):
    buffer = message.get_bytearray()
    size = len(buffer)
    print ( 'Received message %d:' % counter )
    print ( '    Size: %d, Data: %s', size, buffer[:size].decode('utf-8') )
    properties = message.properties()
    pairs = properties.get_internals()
    print ( '    Properties: %s' % pairs )

def receive_message_callback(message, counter):
    global RECEIVE_CALLBACKS
    RECEIVE_CALLBACKS += 1
    counter += 1
    print_message_details(message, counter)
    return IoTHubMessageDispositionResult.ACCEPTED

def device_method_callback(method_name, payload, user_context):
    global METHOD_CALLBACKS, DO_SEND_MESSAGES
    print ( "\nMethod callback called with:\nmethodName = %s\npayload = %s\ncontext = %s" % (method_name, payload, user_context) )
    METHOD_CALLBACKS += 1
    print ( "Total calls confirmed: %d\n" % METHOD_CALLBACKS )
    return_value = DeviceMethodReturnValue()
    return_value.response = "{ \"Response\": \"Failed to interpret message\" }"
    return_value.status = 200
    if method_name == "start":
        DO_SEND_MESSAGES = True
        print ( "Start sending messages\n" )
        return_value.response = "{ \"Response\": \"Successfully started\" }"
        return return_value
    if method_name == "stop":
        DO_SEND_MESSAGES = False
        print ( "Stop sending messages\n" )
        return_value.response = "{ \"Response\": \"Successfully stopped\" }"
        return return_value
    return return_value

def send_confirmation_callback(message, result, user_context):
    global SEND_CALLBACKS
    SEND_CALLBACKS += 1
    print ( '%d messages sent' % SEND_CALLBACKS )

def iothub_connect():
    client = IoTHubClient(CONNECTION_STRING, PROTOCOL)
    client.set_option('product_info', 'Adaran-Pi-Py')
    # If we're using HTTP, we should set timeout (distinct from messageTimeout) and minimum polling time here
    client.set_option('messageTimeout', MESSAGE_TIMEOUT)
    client.set_option('logtrace', 1)
    client.set_message_callback(receive_message_callback, RECEIVE_CONTEXT)
    client.set_device_method_callback(device_method_callback, METHOD_CONTEXT)
    return client

def read_and_send_light(client):
    light_sensor = LightSensor()
    lux = light_sensor.get_lux()
    now = time.time()
    msg = MESSAGE_FORMAT_LIGHT % ( DEVICE_ID, lux, now )
    print (msg)
    message = IoTHubMessage(msg)
    # optional: assign ids
    message.message_id = "message_%d" % MESSAGE_COUNT
    message.correlation_id = "correlation_%d" % MESSAGE_COUNT

    client.send_event_async(message, send_confirmation_callback, MESSAGE_COUNT)

def run():
    try:
        client = iothub_connect()

        while True:
            global MESSAGE_COUNT, DO_SEND_MESSAGES
            if DO_SEND_MESSAGES:
                if config.TSL_2591:
                    read_and_send_light(client)
            time.sleep(config.MESSAGE_TIMESPAN / 1000.0)

    except IoTHubError as iothub_error:
        print ( 'Error: %s' % iothub_error )
        return

    except KeyboardInterrupt:
        print ( 'Stopped' )
        return

if __name__ == '__main__':
    print ( '\nPython %s' % sys.version )
    print ( 'Heliconia IoT Message Generator' )

    run()
