__author__ = 'teddycool'

#Handling all configuration for legorover
config = {"Streamer": {"StreamerImage": "/tmp/stream/pic.jpg", "StreamerLib": "/tmp/stream"},
                "Compass":{"OffsetX": -36, "OffsetY": -104, "Scale":0.92},
                "RefreshRates": {"DriverLoop": 10, "Streamer": 2, "Sensors": 10},  #times per second
                "Vision": {"WriteRawImageToFile": False, "WriteCvImageToFile": False},
                "Logger": {"LogFile": "/home/pi/LegoRover/Logger/log.txt"},
                "Driver": {"TooClose": 10, "TooFarAway": 50, "TooTurn": 30},
                "PushButton": {"Pressed": 0.1, "LongPressed": 1.5},
                "LedIndicator": {"ActivationTime": 2},
          }

