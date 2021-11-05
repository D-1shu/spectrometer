sudo lsusb
sudo modprobe usbserial
sudo sh -c 'echo "067b 23c3" > /sys/bus/usb-serial/drivers/generic/new_id'
sudo sh -c 'echo "KERNEL==\"ttyUSB*\", ATTRS{idVendor}==\"067b\", ATTRS{idProduct}==\"23c3\", GROUP=\"uucp\", MODE=\"0666\"" > /etc/udev/rules.d/60-usb-serial-devices.rules'
cat /etc/udev/rules.d/60-usb-serial-devices.rules
cu --parity=none --nostop --line /dev/ttyUSB0 --speed 9600 dir

