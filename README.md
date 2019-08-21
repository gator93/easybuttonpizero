# easybuttonpizero

Adds a RaspberryPi Zero W to a Staples Easy Button for a push-to-SMS project.

The idea for this project was to create a simple way for my mom, who suffers from dementia, to request help from my dad. She can't operate a phone or two-way radio anymore so pushing a button is ideal.

The button is attached to a GPIO pin and monitored by a script. Pressing the button triggers an email to be sent to the email-to-SMS service provided by the phone carrier.

[EasyButtonPiZero](https://www.thingiverse.com/thing:3815784)


Hardware
1 - Staples Easy Button
1 - RaspberryPi Zero W, microSD card, and power supply
1 - 6x6x4.3 tactile button
2 - 3/8" x 1/10" rare earth magnets (and matching magnet washers) to attach base
https://www.rockler.com/rare-earth-magnets-magnets?gclid=CjwKCAjw7uPqBRBlEiwAYDsr113YIHM8D4hktJRxECwKZXEZRNt4ctl47OzL8jG72H5bVa0vkqjzuxoC0qcQAvD_BwE

Version 2:
1 red LED
1 330 ohm resistor
1 6x6x8 tactile button

E6000 adhesive (for magnets and attaching the button wedge)

Setup

1) Configure NTP 
[Enable NTP client](http://raspberrypi.tomasgreno.cz/ntp-client-and-server.html)
```
sudo apt-get install ntp
```

Add servers to /etc/ntp.conf
```
sudo nano /etc/ntp.conf
server 0.north-america.pool.ntp.org
server 1.north-america.pool.ntp.org
server 2.north-america.pool.ntp.org
server 3.north-america.pool.ntp.org

sudo systemctl stop systemd-timesyncd
sudo systemctl disable systemd-timesyncd
sudo /etc/init.d/ntp stop
sudo /etc/init.d/ntp start
```

2) Enable UART for status LED (optional)
Add line to /boot/config.txt
```
sudo nano /boot/config.txt
enable_uart=1
```
3) Install git
```
sudo apt-get install git
```

4) Prepare easybutton directories
```
mkdir /home/pi/easy
mkdir /home/pi/dev
cd /home/pi/dev/
git clone https://github.com/gator93/easybuttonpizero
```

5) Add email and phone credentials to easy.py
```
cp /home/pi/dev/easybuttonpizero/easy.py /home/pi/easy
cd /home/pi/easy
sudo chmod +x easy.py
nano easy.py
```

6) Make scripts start on boot
[Add Power Button](https://howchoo.com/g/mwnlytk3zmm/how-to-add-a-power-button-to-your-raspberry-pi)
[Run Program at boot](https://www.dexterindustries.com/howto/run-a-program-on-your-raspberry-pi-at-startup/)
```
cd /home/pi/dev/easybuttonpizero
sudo cp listen-for-shutdown.py /usr/local/bin/
sudo chmod +x /usr/local/bin/listen-for-shutdown.py
sudo cp listen-for-shutdown.sh /etc/init.d
sudo chmod +x /etc/init.d/listen-for-shutdown.sh
sudo update-rc.d listen-for-shutdown.sh defaults
sudo /etc/init.d/listen-for-shutdown.sh start
```

7) Reboot
```
sudo reboot now
```
