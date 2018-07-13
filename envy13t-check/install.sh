#!/bin/bash

cp check.py /usr/bin/envy13t-check
cp check.service /etc/systemd/user/envy13t-check.service
systemctl --user --global enable envy13t-check
