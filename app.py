import sched
import subprocess
from threading import Thread
import time

import bottle
from bottle import route, get, post, static_file, request

SCREEN_TIMER_DELAY_SECONDS = 25*60
SCREEN_TIMER_SOUND_FILENAME = 'media/screenTimerSequence-01.wav'
HOST_PORT=23238
HOST_IP='0.0.0.0'

class ScreenTimerStatus:
    lastScheduledSoundJob: sched.Event
    lastScheduledSoundTime: float
    autoTurnOffTime: str
    autoTurnOffEnabled: bool = False

    def isTimerRunning(self):
        return self.lastScheduledSoundJob != None

status = ScreenTimerStatus() 
scheduler = sched.scheduler(timefunc=time.monotonic) # default: monotonic clock

def playSound(filename: str):
    Thread(target=lambda: subprocess.run(['aplay', filename]), daemon=True).start()
playSound('media/screenTimerOn.wav')

def scheduleAnotherScreenTimerSound():
    status.lastScheduledSoundTime = time.monotonic() + SCREEN_TIMER_DELAY_SECONDS
    status.lastScheduledSoundJob = scheduler.enter(SCREEN_TIMER_DELAY_SECONDS, priority=1, action=playScreenTimerSoundAndRequeue)

def playScreenTimerSoundAndRequeue():
    scheduleAnotherScreenTimerSound()
    playSound(SCREEN_TIMER_SOUND_FILENAME)

@get('/screen-timer/status')
def retrieveScreenTimerStatus():
    return {
        "secondsUntilNextAlert": status.lastScheduledSoundTime - time.monotonic() if status.isTimerRunning() else None,
        "timerRunning": status.isTimerRunning(),
        "autoTurnOffTime": None,
        "autoTurnOffEnabled": False,
    }

@post('/screen-timer/stop')
def stopScreenTimer():
    # Cancel previous screen timer
    if status.isTimerRunning():
        scheduler.cancel(status.lastScheduledSoundJob)
        status.lastScheduledSoundJob = None
        status.lastScheduledSoundTime = None
    return retrieveScreenTimerStatus()

@post('/screen-timer/restart')
def restartScreenTimer():
    # Cancel previous screen timer
    stopScreenTimer()
    # Start screen timer
    scheduleAnotherScreenTimerSound()

    return retrieveScreenTimerStatus()

@post('/screen-timer/auto-turn-off-time')
def setAutoTurnOffTime():
    status.autoTurnOffTime = request.query.time

@post('/screen-timer/auto-turn-off-time/enabled')
def enableDisableAutoTurnOff():
    status.autoTurnOffEnabled = request.query.enabled

@route('/<filepath:path>')
def staticWebsite(filepath):
    return static_file(filepath, root='www')

def runScheduler():
    # Don't let it stop running even if it doesn't have any events at any given time
    while True:
        scheduler.run(blocking=True)
        time.sleep(2)

scheduleAnotherScreenTimerSound()
Thread(target=runScheduler, daemon=True).start()

bottle.run(host=HOST_IP, port=HOST_PORT)