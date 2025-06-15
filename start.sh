#!/bin/bash
cd /home/cjb/repos/i-ink
git pull
source /home/cjb/repos/i-ink/myenv/bin/activate
export GPIOZERO_PIN_FACTORY=pigpio
exec python run.py
