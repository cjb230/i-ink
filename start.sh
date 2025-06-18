#!/bin/bash
rm /home/cjb/i-ink.log
exec >> /home/cjb/i-ink.log 2>&1
set -x
cd /home/cjb/repos/i-ink
git -C /home/cjb/repos/i-ink pull --ff-only || true
source /home/cjb/repos/i-ink/myenv/bin/activate
export GPIOZERO_PIN_FACTORY=pigpio
exec python run.py
