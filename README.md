# Toyota Prius CAN Bus

### Install

Panda 及相關依賴套件案裝：

```shell
pip install pandacan
pip install cffi
```

Pygame install

```shell
sudo apt-get install python-pygame
# testing
python -m pygame.examples.aliens
```



---

### Run panda without root scripts

Linux udev rules :

```shell
sudo -i
echo 'SUBSYSTEMS=="usb", ATTR{idVendor}=="bbaa", ATTR{idProduct}=="ddcc", MODE:="0666"' > /etc/udev/rules.d/11-panda.rules
exit
```

