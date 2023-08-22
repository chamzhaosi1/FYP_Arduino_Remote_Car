### Refer: https://www.highvoltagecode.com/post/webrtc-on-raspberry-pi-live-hd-video-and-audio-streaming

# raspi-config # GUI
# # Interfacing Options > Camera.


# #Installing and testing the UV4L streaming server
# cd ~
# curl http://www.linux-projects.org/listing/uv4l_repo/lpkey.asc 
# apt-key add lpkey.asc
# echo "deb https://www.linux-projects.org/listing/uv4l_repo/raspbian/stretch stretch main" | sudo tee /etc/apt/sources.list.d/uv4l.list
# sudo apt-get update && sudo apt-get upgrade

# sudo apt-get install uv4l-webrtc
# sudo apt-get install uv4l-webrtc-armv6
# uv4l --external-driver --device-name=video0

# http://192.168.0.84:8080/stream/webrtc


###############################################################################
## Option 2
## https://github.com/kclyu/rpi-webrtc-streamer/blob/master/README_building.md




###############################################################################
## Option 3
## https://github.com/kclyu/rpi-webrtc-streamer/blob/master/README_rws_setup.md


###############################################################################
## Option 4
## https://pramod-atre.medium.com/live-streaming-video-audio-on-raspberry-pi-using-usb-camera-and-microphone-d19ece13eff0