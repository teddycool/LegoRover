# legorover
Autonomous legorover...
Using sensors and openCV for image analyze and obstacle detection. The openCV stream is sent to a mjpeg streamer that can be viewed in a webbrowser (firefox) on the same network.


Using LCM for sensordata
Each sensortype has its own messagetype and publish this as fast as possible from a separate thread started in MainLoopLcm
Msg-channels are used for different type of values, ie US sensormessages is the same but channel is different for front and rear values



Implementation:
This branch is dedicated to using lcm for sensordata etc and I'll clean out things not used... 




LCM:
Build:      https://lcm-proj.github.io/build_instructions.html
DataType:   https://lcm-proj.github.io/tut_lcmgen.html
Generate:   lcm-gen -p usdistance.lcm



