# legorover
Autonomous legorover...
Using sensors and openCV for image analyze and obstacle detection. The openCV stream is sent to a mjpeg streamer that can be viewed in a webbrowser (firefox) on the same network.


Using LCM for sensordata
Each sensortype has its own messagetype and publish this as fast as possible from a separate thread started in MainLcm
Msg-channels are used for different type of values, ie US sensormessages is the same but channel is different for front and rear values



Implementation:
The implementation is using a simple game-development 'pattern' or strategy with a MainLoop. This loop around the different objects (Sensors, Vison, Driver) and all object have the methods initialize, update and draw.
Each object, like the sensors may have more parts that are looped within this object. Sensors has a number of US distance sensors and a compass. The Driver has a base-class for 'state' with a couple of different implementations for different states.
Vision is using classes for obstable-, face- and line-recognition wich data is tranfered to the driver-class.




LCM:
Build:      https://lcm-proj.github.io/build_instructions.html
DataType:   https://lcm-proj.github.io/tut_lcmgen.html
Generate:   lcm-gen -p usdistance.lcm



