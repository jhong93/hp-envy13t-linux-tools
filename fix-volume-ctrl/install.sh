#!/bin/bash

cp fix-volume-ctrl.py /usr/bin/fix-volume-ctrl
cp fix-volume-ctrl.service /etc/systemd/system/
systemctl enable fix-volume-ctrl
systemctl restart fix-volume-ctrl
