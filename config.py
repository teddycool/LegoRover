__author__ = 'teddycool'

#Handling all configuration for legorover
roverconfig = { "Streamer": {"StreamerImage": "/tmp/stream/pic.jpg", "StreamerLib": "/tmp/stream"},
               "Compass":{"OffsetX": -36, "OffsetY": -104, "Scale":0.92},
               "RefreshRates": {"DriverLoop": 10, "Streamer": 2, "Sensors": 10}, #times per second
               "Vision": {"WriteRawImageToFile": False, "WriteCvImageToFile": False},
                "Logger": {"LogFile": "/home/pi/LegoRover/Logger/log.txt"}
                }

