# Whole Room Screen Timer

Features:

- 3-stage screen timer sound every 25mins:
  - t-10s: An alert buzzer
  - t-0s: "Look away from your screen for 20 seconds"
  - t+23s: "Get back to work"
- Runs on a computer attached to your home router (python script)
  - ... so that you can have speakers attached which can be heard through your whole living space, regardless of muting, headphones, etc. on whatever you're doing currently.
- Website with time left before next sound and some controls

![Screenshot of control website](docs/Screenshot%202023-11-24%20at%2023-05-07%20ScreenTimer.png)

## Install

Copy these files onto a Linux computer with Python 3.9+ & ALSA (cli tool: `aplay`) installed:

> In examples below, we assume script was copied to `/opt/whole-room-screen-timer/`, so that this should exist: `/opt/whole-room-screen-timer/app.py`.

Add to startup as a systemd task: 

```
sudo cp whole-room-screen-timer.service /etc/systemd/system/whole-room-screen-timer.service
```

Then enable the service:

```bash
sudo systemctl enable whole-room-screen-timer.service
```

You can check the status of the service with:

```bash
sudo systemctl status whole-room-screen-timer.service
```

And start it!

```bash
sudo systemctl start whole-room-screen-timer.service
```