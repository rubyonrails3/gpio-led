# gpio-led
Snap to control GPIO pin 2 to turn on and off depending on sunset and sunrise and can be controlled remotely

# How to test

## Build the snap

`snapcraft` or `snapcraft --use-lxd` 

## Install snap on device with GPIO pins 

`sudo snap install light_0.0.1_arm64.snap --dangerous` 

## Connect GPIO PIN-2 to the snap

`sudo snap connect lights:gpio pi:bcm-gpio-2` 

## Start the daemon

`sudo light.control` 


# Control light remotely

`wick --url ws://ec2-3-133-149-135.us-east-2.compute.amazonaws.com:8080/ws call com.lights.change_state on` 

`wick --url ws://ec2-3-133-149-135.us-east-2.compute.amazonaws.com:8080/ws call com.lights.current_state on`

# Subscribe to be notified 

`wick --url ws://ec2-3-133-149-135.us-east-2.compute.amazonaws.com:8080/ws subscribe com.lights.update` 
