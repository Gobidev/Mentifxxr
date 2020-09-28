#!/bin/bash

while :
do
  screen -Amd torify python3 spam_thread.py
  sleep 1
done

# To stop, run "killall screen"
