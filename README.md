# PianoPythonTuner
## Equipment
* Raspberry Pi Model 3
* USB Soundcard 3D sound
* 3.5mm Microphone
* 16gb SD card
* LED in series with 100 ohm resistor
* 5V 2A Micro-USB Power Supply

## Getting Started

### Setting up Raspbian
The RPi OS used is *Raspbian Jessie*. The latest is *Raspbian Stretch*, however was skipped due to the lack of online support in comparison to *Jessie*

*Raspbian Jessie* is available [here](http://downloads.raspberrypi.org/raspbian_lite/images/). Folder: "raspbian-2017-07-05"

Extract the **.img** file and flash using any disk imager to an sd for Rpi, for example [Win32 Disk Imager](https://sourceforge.net/projects/win32diskimager/).

### Configuring the RPi
A large basis of this configuration uses [this wiki](https://wiki.linuxaudio.org/wiki/raspberrypi) as a guideline. Feel free to visit the link for additional procedures and explanations.

#### Internet
1. Log into the RPi, with **Username:**`pi` **Password:**`raspberry`

2. Connect to the wifi using:

`sudo nano /etc/wpa_supplicant/wpa_supplicant.conf`

3. Inside the editor, your wifi access details will have to be entered in the following manner:

``` 
network={  
    ssid="NETWORK_ID"  
    psk="PASSWORD"   
    key_mgmt=WPA-PSK   
} 
```

*with WPA-PSK or WPA-EAP depending on the router setup

1. Reconfigure with:

`wpa_cli -i wlan0 reconfigure`

2. And check if connection is running with:

`ifconfig wlan0`

#### Headless setup
Headless allows another system to remotely access RPi through SSH. This is will significantly improve processor performance by detaching our GUI.

1. Enable SSH access on RPi:

`sudo raspi-config`

2. Navigate to **Interfacing Options -> SSH -> Enable**

Lastly we will want to set up a static ip adress.
This ins under the assumption that the address used (192.168.0.200) will conflict with any other addresses, otherwise, simply change the '200' to another value.

3. Edit the dhcpcd.conf file:

`sudo nano /etc/dhcpcd.conf`

4. Adding to the bottom:
```
interface wlan0   
static ip_address=192.168.0.200/24       
static routers=192.168.0.1     
static domain_name_servers=192.168.0.1
```
5. Reboot with new static ip:

`sudo reboot`

6. Access your RPi remotely using any means, such as PuTTY or terminal entering:

`ssh -X pi@192.168.0.200`

Note: in most cases, X-forwarding is required in order to prevent issues involving JACKD

The last step is to get all the necessary updates:

`sudo apt-get update`

`sudo apt-get upgrade`

### Enabling USB Soundcard

Our list of connected soundcards and their respective label can be checked with:

`arecord -l`

and:

`aplay -l`

Card 0 indicates the internal soundcard and card 1 should appear, indicating a connected external soundcard.

We will change the default soundcard through the alsa.conf file.

1. Open alsa.conf:

`sudo nano /usr/share/alsa/alsa.conf`

2. Navigate to the line of code containing:
```
defaults.ctl.card 0  
defaults.pcm.card 0
```

4. Edit this to specify the external soundcard:

```
defaults.ctl.card 1  
defauts.pcm.card 1
```

4. Exit and save with **CTRL+X** then **Y** then **ENTER**

5. Adjust gain levels:

`alsamixer`

### The Python Code

#### ALSA

In the alsa.conf file, there are more changes needed in order for the soundcard to work through python. Running PyAudio as is will return messages such as:

```
ALSA lib pcm.c:2239:(snd_pcm_open_noupdate) Unknown PCM cards.pcm.rear  
ALSA lib pcm.c:2239:(snd_pcm_open_noupdate) Unknown PCM cards.pcm.center_lfe  
ALSA lib pcm.c:2239:(snd_pcm_open_noupdate) Unknown PCM cards.pcm.side  
ALSA lib pcm.c:2239:(snd_pcm_open_noupdate) Unknown PCM cards.pcm.hdmi  
ALSA lib pcm.c:2239:(snd_pcm_open_noupdate) Unknown PCM cards.pcm.modem  
ALSA lib pcm.c:2239:(snd_pcm_open_noupdate) Unknown PCM cards.pcm.phoneline
```

We will need to change a few name items.

1. Open alsa.conf again:

`sudo nano /usr/share/alsa/alsa.conf`
 
2. Locate the line containing:

`pcm.front cards.pcm.front`

3. The tail label for each item needs to be changed to **.default** like so:

`pcm.front cards.pcm.default`

This will point actions to the default device which we specified earlier as the USB soundcard.

4. Do this for every **cards.pcm.""** item

5. Save and exit

#### Python

The version pre-installed is Python2.7. But we will still need certain libraries in order for the code to work.

1. Get pip for easy module installation:

`sudo apt-get install python-pip`

2. Update *pip, wheels, setuptools*:

`sudo python -m pip install --upgrade pip setuptools wheel`

3. Install library dependencies:

` sudo apt-get install libasound2-dev portaudio19-dev libportaudio2 libportaudiocpp0 libav-tools python-all-dev`

4. Install *pyaudio*:

` sudo pip install pyaudio`

#### Github

1. Install *Github*:

`sudo apt-get install git`

2. Clone Repository:

`git clone https://github.com/realtimshady1/PianoPythonTuner.git`

#### Jackd

We will need *Jack 1 & 2* in order to route to alsa in our Python code. Be sure to install Jackd last, I discovered that the other packages will remove a preinstalled Jackd.

1. Jackd 1:

`sudo apt-get install jackd1`

Ensure to allow realtime access priority

2. Jackd 2:

`sudo apt-get install jackd2`

## Running the Script

Before running any instance of *Jackd*, we have to export the following environment variable. I am not exactly sure what this is but without this, *Jackd* refuses to work.

1. Export the following:

`export DBUS_SESSION_BUS_ADDRESS=unix:path=/run/dbus/system_bus_socket`

2. Run an instance of *Jackd* to *alsa* in the background:

`jackd -d alsa &`

3. Navigate to PianoPythonTuner

`cd ~/PianoPythonTuner/`

4. Run the Script

`./RMS_Duty_Converter.py`

