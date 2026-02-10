#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2024.2.4),
    on July 25, 2025, at 10:22
If you publish work using this script the most relevant publication is:

    Peirce J, Gray JR, Simpson S, MacAskill M, Höchenberger R, Sogo H, Kastman E, Lindeløv JK. (2019) 
        PsychoPy2: Experiments in behavior made easy Behav Res 51: 195. 
        https://doi.org/10.3758/s13428-018-01193-y

"""

import psychopy
psychopy.useVersion('2024.2')


# --- Import packages ---
from psychopy import locale_setup
from psychopy import prefs
from psychopy import plugins
plugins.activatePlugins()
prefs.hardware['audioLib'] = 'pygame'
prefs.hardware['audioLatencyMode'] = '3'
from psychopy import sound, gui, visual, core, data, event, logging, clock, colors, layout, hardware
from psychopy.tools import environmenttools
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER, priority)

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle, choice as randchoice
import os  # handy system and path functions
import sys  # to get file system encoding

import psychopy.iohub as io
from psychopy.hardware import keyboard

# --- Setup global variables (available in all functions) ---
# create a device manager to handle hardware (keyboards, mice, mirophones, speakers, etc.)
deviceManager = hardware.DeviceManager()
# ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
# store info about the experiment session
psychopyVersion = '2024.2.4'
expName = 'test'  # from the Builder filename that created this script
# information about this experiment
expInfo = {
    'participant': f"{randint(0, 999999):06.0f}",
    'session': '001',
    'date|hid': data.getDateStr(),
    'expName|hid': expName,
    'psychopyVersion|hid': psychopyVersion,
}

# --- Define some variables which will change depending on pilot mode ---
'''
To run in pilot mode, either use the run/pilot toggle in Builder, Coder and Runner, 
or run the experiment with `--pilot` as an argument. To change what pilot 
#mode does, check out the 'Pilot mode' tab in preferences.
'''
# work out from system args whether we are running in pilot mode
PILOTING = core.setPilotModeFromArgs()
# start off with values from experiment settings
_fullScr = True
_winSize = [1920, 1080]
# if in pilot mode, apply overrides according to preferences
if PILOTING:
    # force windowed mode
    if prefs.piloting['forceWindowed']:
        _fullScr = False
        # set window size
        _winSize = prefs.piloting['forcedWindowSize']

def showExpInfoDlg(expInfo):
    """
    Show participant info dialog.
    Parameters
    ==========
    expInfo : dict
        Information about this experiment.
    
    Returns
    ==========
    dict
        Information about this experiment.
    """
    # show participant info dialog
    dlg = gui.DlgFromDict(
        dictionary=expInfo, sortKeys=False, title=expName, alwaysOnTop=True
    )
    if dlg.OK == False:
        core.quit()  # user pressed cancel
    # return expInfo
    return expInfo


def setupData(expInfo, dataDir=None):
    """
    Make an ExperimentHandler to handle trials and saving.
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    dataDir : Path, str or None
        Folder to save the data to, leave as None to create a folder in the current directory.    
    Returns
    ==========
    psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    """
    # remove dialog-specific syntax from expInfo
    for key, val in expInfo.copy().items():
        newKey, _ = data.utils.parsePipeSyntax(key)
        expInfo[newKey] = expInfo.pop(key)
    
    # data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
    if dataDir is None:
        dataDir = _thisDir
    filename = u'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])
    # make sure filename is relative to dataDir
    if os.path.isabs(filename):
        dataDir = os.path.commonprefix([dataDir, filename])
        filename = os.path.relpath(filename, dataDir)
    
    # an ExperimentHandler isn't essential but helps with data saving
    thisExp = data.ExperimentHandler(
        name=expName, version='',
        extraInfo=expInfo, runtimeInfo=None,
        originPath='C:\\Users\\KIST\\Desktop\\Tutorial\\tutorial_lastrun.py',
        savePickle=True, saveWideText=True,
        dataFileName=dataDir + os.sep + filename, sortColumns='time'
    )
    thisExp.setPriority('thisRow.t', priority.CRITICAL)
    thisExp.setPriority('expName', priority.LOW)
    # return experiment handler
    return thisExp


def setupLogging(filename):
    """
    Setup a log file and tell it what level to log at.
    
    Parameters
    ==========
    filename : str or pathlib.Path
        Filename to save log file and data files as, doesn't need an extension.
    
    Returns
    ==========
    psychopy.logging.LogFile
        Text stream to receive inputs from the logging system.
    """
    # set how much information should be printed to the console / app
    if PILOTING:
        logging.console.setLevel(
            prefs.piloting['pilotConsoleLoggingLevel']
        )
    else:
        logging.console.setLevel('warning')
    # save a log file for detail verbose info
    logFile = logging.LogFile(filename+'.log')
    if PILOTING:
        logFile.setLevel(
            prefs.piloting['pilotLoggingLevel']
        )
    else:
        logFile.setLevel(
            logging.getLevel('info')
        )
    
    return logFile


def setupWindow(expInfo=None, win=None):
    """
    Setup the Window
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    win : psychopy.visual.Window
        Window to setup - leave as None to create a new window.
    
    Returns
    ==========
    psychopy.visual.Window
        Window in which to run this experiment.
    """
    if PILOTING:
        logging.debug('Fullscreen settings ignored as running in pilot mode.')
    
    if win is None:
        # if not given a window to setup, make one
        win = visual.Window(
            size=_winSize, fullscr=_fullScr, screen=1,
            winType='pyglet', allowGUI=False, allowStencil=False,
            monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
            backgroundImage='', backgroundFit='none',
            blendMode='avg', useFBO=True,
            units='height',
            checkTiming=False  # we're going to do this ourselves in a moment
        )
    else:
        # if we have a window, just set the attributes which are safe to set
        win.color = [0,0,0]
        win.colorSpace = 'rgb'
        win.backgroundImage = ''
        win.backgroundFit = 'none'
        win.units = 'height'
    if expInfo is not None:
        # get/measure frame rate if not already in expInfo
        if win._monitorFrameRate is None:
            win._monitorFrameRate = win.getActualFrameRate(infoMsg='Attempting to measure frame rate of screen, please wait...')
        expInfo['frameRate'] = win._monitorFrameRate
    win.hideMessage()
    # show a visual indicator if we're in piloting mode
    if PILOTING and prefs.piloting['showPilotingIndicator']:
        win.showPilotingIndicator()
    
    return win


def setupDevices(expInfo, thisExp, win):
    """
    Setup whatever devices are available (mouse, keyboard, speaker, eyetracker, etc.) and add them to 
    the device manager (deviceManager)
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    win : psychopy.visual.Window
        Window in which to run this experiment.
    Returns
    ==========
    bool
        True if completed successfully.
    """
    # --- Setup input devices ---
    ioConfig = {}
    
    # Setup iohub keyboard
    ioConfig['Keyboard'] = dict(use_keymap='psychopy')
    
    # Setup iohub experiment
    ioConfig['Experiment'] = dict(filename=thisExp.dataFileName)
    
    # Start ioHub server
    ioServer = io.launchHubServer(window=win, **ioConfig)
    
    # store ioServer object in the device manager
    deviceManager.ioServer = ioServer
    
    # create a default keyboard (e.g. to check for escape)
    if deviceManager.getDevice('defaultKeyboard') is None:
        deviceManager.addDevice(
            deviceClass='keyboard', deviceName='defaultKeyboard', backend='iohub'
        )
    if deviceManager.getDevice('key_resp') is None:
        # initialise key_resp
        key_resp = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='key_resp',
        )
    if deviceManager.getDevice('gelling_key') is None:
        # initialise gelling_key
        gelling_key = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='gelling_key',
        )
    if deviceManager.getDevice('erp_start_key') is None:
        # initialise erp_start_key
        erp_start_key = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='erp_start_key',
        )
    # create speaker 'erp_stimuli'
    deviceManager.addDevice(
        deviceName='erp_stimuli',
        deviceClass='psychopy.hardware.speaker.SpeakerDevice',
        index=16.0
    )
    if deviceManager.getDevice('erp_end_key') is None:
        # initialise erp_end_key
        erp_end_key = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='erp_end_key',
        )
    if deviceManager.getDevice('main_start_key') is None:
        # initialise main_start_key
        main_start_key = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='main_start_key',
        )
    # create speaker 'main_stimuli'
    deviceManager.addDevice(
        deviceName='main_stimuli',
        deviceClass='psychopy.hardware.speaker.SpeakerDevice',
        index=16.0
    )
    if deviceManager.getDevice('quiz_key') is None:
        # initialise quiz_key
        quiz_key = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='quiz_key',
        )
    if deviceManager.getDevice('rest_key') is None:
        # initialise rest_key
        rest_key = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='rest_key',
        )
    if deviceManager.getDevice('main_end_key') is None:
        # initialise main_end_key
        main_end_key = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='main_end_key',
        )
    if deviceManager.getDevice('finish_key') is None:
        # initialise finish_key
        finish_key = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='finish_key',
        )
    # return True if completed successfully
    return True

def pauseExperiment(thisExp, win=None, timers=[], playbackComponents=[]):
    """
    Pause this experiment, preventing the flow from advancing to the next routine until resumed.
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    win : psychopy.visual.Window
        Window for this experiment.
    timers : list, tuple
        List of timers to reset once pausing is finished.
    playbackComponents : list, tuple
        List of any components with a `pause` method which need to be paused.
    """
    # if we are not paused, do nothing
    if thisExp.status != PAUSED:
        return
    
    # start a timer to figure out how long we're paused for
    pauseTimer = core.Clock()
    # pause any playback components
    for comp in playbackComponents:
        comp.pause()
    # make sure we have a keyboard
    defaultKeyboard = deviceManager.getDevice('defaultKeyboard')
    if defaultKeyboard is None:
        defaultKeyboard = deviceManager.addKeyboard(
            deviceClass='keyboard',
            deviceName='defaultKeyboard',
            backend='ioHub',
        )
    # run a while loop while we wait to unpause
    while thisExp.status == PAUSED:
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=['escape']):
            endExperiment(thisExp, win=win)
        # sleep 1ms so other threads can execute
        clock.time.sleep(0.001)
    # if stop was requested while paused, quit
    if thisExp.status == FINISHED:
        endExperiment(thisExp, win=win)
    # resume any playback components
    for comp in playbackComponents:
        comp.play()
    # reset any timers
    for timer in timers:
        timer.addTime(-pauseTimer.getTime())


def run(expInfo, thisExp, win, globalClock=None, thisSession=None):
    """
    Run the experiment flow.
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    psychopy.visual.Window
        Window in which to run this experiment.
    globalClock : psychopy.core.clock.Clock or None
        Clock to get global time from - supply None to make a new one.
    thisSession : psychopy.session.Session or None
        Handle of the Session object this experiment is being run from, if any.
    """
    # mark experiment as started
    thisExp.status = STARTED
    # make sure window is set to foreground to prevent losing focus
    win.winHandle.activate()
    # make sure variables created by exec are available globally
    exec = environmenttools.setExecEnvironment(globals())
    # get device handles from dict of input devices
    ioServer = deviceManager.ioServer
    # get/create a default keyboard (e.g. to check for escape)
    defaultKeyboard = deviceManager.getDevice('defaultKeyboard')
    if defaultKeyboard is None:
        deviceManager.addDevice(
            deviceClass='keyboard', deviceName='defaultKeyboard', backend='ioHub'
        )
    eyetracker = deviceManager.getDevice('eyetracker')
    # make sure we're running in the directory for this experiment
    os.chdir(_thisDir)
    # get filename from ExperimentHandler for convenience
    filename = thisExp.dataFileName
    frameTolerance = 0.001  # how close to onset before 'same' frame
    endExpNow = False  # flag for 'escape' or other condition => quit the exp
    # get frame duration from frame rate in expInfo
    if 'frameRate' in expInfo and expInfo['frameRate'] is not None:
        frameDur = 1.0 / round(expInfo['frameRate'])
    else:
        frameDur = 1.0 / 60.0  # could not measure, so guess
    
    # Start Code - component code to be run after the window creation
    
    # --- Initialize components for Routine "Start" ---
    # Run 'Begin Experiment' code from start_code
    # Import TDT library and establish connection
    import tdt
    from datetime import datetime
    import time
    
    print("=========== Setting Configuration ===========") 
    # Attempt TDT Synapse connection
    try:
        syn = tdt.SynapseAPI()
        print("1. TDT Synapse connection successful")
        tdt_connected = True
    except Exception as e:
        print(f"TDT Synapse connection failed: {e}")
        # Abort experiment if TDT connection fails
        core.quit()
    
    # Initialize global variables
    experiment_start_time = None
    tank_dir = None
    block_dir = None
    start_text = visual.TextStim(win=win, name='start_text',
        text='',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    key_resp = keyboard.Keyboard(deviceName='key_resp')
    
    # --- Initialize components for Routine "Geling" ---
    gelling_text = visual.TextStim(win=win, name='gelling_text',
        text="(If gelling is finished and you are willing to proceed, please press '9'.)",
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    gelling_key = keyboard.Keyboard(deviceName='gelling_key')
    
    # --- Initialize components for Routine "Gelling_end" ---
    gelling_end_text = visual.TextStim(win=win, name='gelling_end_text',
        text='It takes about 20 seconds to stabilize EEG signals from impedance checking.',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    
    # --- Initialize components for Routine "ERP_start" ---
    erp_start_text = visual.TextStim(win=win, name='erp_start_text',
        text="ERP session starts.\n\n(If you are willing to proceed, please press '0'.)",
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    erp_start_key = keyboard.Keyboard(deviceName='erp_start_key')
    
    # --- Initialize components for Routine "ERP" ---
    # Run 'Begin Experiment' code from erp_code
    # Define trigger_id
    trigger_id = None
    erp_stimuli = sound.Sound(
        'A', 
        secs=-1, 
        stereo=True, 
        hamming=True, 
        speaker='erp_stimuli',    name='erp_stimuli'
    )
    erp_stimuli.setVolume(1.0)
    erp_text_rest = visual.TextStim(win=win, name='erp_text_rest',
        text='.',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-2.0);
    erp_text_isi = visual.TextStim(win=win, name='erp_text_isi',
        text='.',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-3.0);
    
    # --- Initialize components for Routine "ERP_end" ---
    erp_end_text = visual.TextStim(win=win, name='erp_end_text',
        text="ERP session is finished.\n\n(If you are willing to proceed, please press '0'.)",
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    erp_end_key = keyboard.Keyboard(deviceName='erp_end_key')
    
    # --- Initialize components for Routine "Main_start" ---
    main_start_text = visual.TextStim(win=win, name='main_start_text',
        text="Main session starts.\n\n(If you are willing to proceed, please press '0'.)",
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    main_start_key = keyboard.Keyboard(deviceName='main_start_key')
    
    # --- Initialize components for Routine "Main" ---
    # Run 'Begin Experiment' code from main_code
    # Define fixed isi
    main_fixed_isi = 3
    main_stimuli = sound.Sound(
        'A', 
        secs=-1, 
        stereo=True, 
        hamming=True, 
        speaker='main_stimuli',    name='main_stimuli'
    )
    main_stimuli.setVolume(1.0)
    main_text_rest = visual.TextStim(win=win, name='main_text_rest',
        text='.',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-2.0);
    main_text_isi = visual.TextStim(win=win, name='main_text_isi',
        text='.',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-3.0);
    
    # --- Initialize components for Routine "quiz" ---
    # Run 'Begin Experiment' code from quiz_code
    quiz_correct = 2001
    quiz_wrong = 2002
    quiz_text = visual.TextStim(win=win, name='quiz_text',
        text='',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    quiz_key = keyboard.Keyboard(deviceName='quiz_key')
    
    # --- Initialize components for Routine "rest" ---
    rest_text = visual.TextStim(win=win, name='rest_text',
        text="You can stretch and take a rest for a while.\n\n(If you are willing to proceed, please press '0')",
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    rest_key = keyboard.Keyboard(deviceName='rest_key')
    
    # --- Initialize components for Routine "Main_end" ---
    main_end_text = visual.TextStim(win=win, name='main_end_text',
        text="Main sesssion finished.\n\n(If you are willing to proceed, please press '0'.)",
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    main_end_key = keyboard.Keyboard(deviceName='main_end_key')
    
    # --- Initialize components for Routine "Finish" ---
    finish_text_1 = visual.TextStim(win=win, name='finish_text_1',
        text='Please wait...\n\nIt takes about 10 seconds for wrapping up the experiment.',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    finish_text_2 = visual.TextStim(win=win, name='finish_text_2',
        text="All the experiment completed successfully.\n\nSaving data and stopping recording.\n\n(If you are willing to finish, please press '0'.)",
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-2.0);
    finish_key = keyboard.Keyboard(deviceName='finish_key')
    
    # create some handy timers
    
    # global clock to track the time since experiment started
    if globalClock is None:
        # create a clock if not given one
        globalClock = core.Clock()
    if isinstance(globalClock, str):
        # if given a string, make a clock accoridng to it
        if globalClock == 'float':
            # get timestamps as a simple value
            globalClock = core.Clock(format='float')
        elif globalClock == 'iso':
            # get timestamps in ISO format
            globalClock = core.Clock(format='%Y-%m-%d_%H:%M:%S.%f%z')
        else:
            # get timestamps in a custom format
            globalClock = core.Clock(format=globalClock)
    if ioServer is not None:
        ioServer.syncClock(globalClock)
    logging.setDefaultClock(globalClock)
    # routine timer to track time remaining of each (possibly non-slip) routine
    routineTimer = core.Clock()
    win.flip()  # flip window to reset last flip timer
    # store the exact time the global clock started
    expInfo['expStart'] = data.getDateStr(
        format='%Y-%m-%d %Hh%M.%S.%f %z', fractionalSecondDigits=6
    )
    
    # --- Prepare to start Routine "Start" ---
    # create an object to store info about Routine Start
    Start = data.Routine(
        name='Start',
        components=[start_text, key_resp],
    )
    Start.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # Run 'Begin Routine' code from start_code
    # Record experiment start time
    experiment_start_time = core.getTime()
    
    # Experiment strftime 
    clean_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Define User and Experiment names
    user = "Tutorial"
    experiment = "Tutorial"
    
    # Define Block names
    block_name = f"{expInfo['participant']}_{clean_datetime}"  # participant_date format
    
    # Configure TDT Tank and Block
    try:
        # First switch Synapse to Idle mode
        if not syn.getMode() == 0:
            syn.setMode(0)  # Idle mode
        
        # Set User & Experiment (setting name)
        syn.setCurrentUser(user)
        print(f"2. Setting user ({user}) done")
        syn.setCurrentExperiment(experiment)
        print(f"3. Setting experiment ({experiment}) done")
    
        # Tank Check (experiment name)
        current_tank = syn.getCurrentTank()
        print(f"4. Tank setup ({current_tank}) done")
        
        # Set Subject (participant name)
        syn.createSubject(expInfo['participant'], f'datetime_{clean_datetime}', 'mouse')
        syn.setCurrentSubject(expInfo['participant'])
        current_subject = syn.getCurrentSubject()
        print(f"5. Subject setup ({current_subject}) done")
        
        # Set Block name (participant_date)
        syn.setCurrentBlock(block_name)
        print(f"6. Block setup ({block_name}) done")
        
        # Synapse Recording mode
        syn.setMode(3)  
        print("7. TDT Recording mode started")
    
        # Block dir (where actual data will be saved)
        block_dir = f"{current_tank}\\{block_name}"
        
        # PsychoPy CSV save path (in Block directory)
        filename = f"{block_dir}\\psychopy_{expInfo['participant']}_{expInfo['date']}"
        
        print(f"8. PsychoPy data savepath setup ({filename}) done")
        print("=========== Setting Configuration Done ===========")
    except Exception as e:
        print(f"Tank/Block setup failed: {e}")
        core.quit()
        
    start_text.setText("Tutorial start.\n\n- Setting up experiment successful.\n- Connecting TDT and configuring settings successful.\n\n(If you are willing to proceed, please press '0'.)\n\n(If you press '0', psychopy window will be minimized and impedance checker would appear.)")
    # create starting attributes for key_resp
    key_resp.keys = []
    key_resp.rt = []
    _key_resp_allKeys = []
    # store start times for Start
    Start.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    Start.tStart = globalClock.getTime(format='float')
    Start.status = STARTED
    thisExp.addData('Start.started', Start.tStart)
    Start.maxDuration = None
    # keep track of which components have finished
    StartComponents = Start.components
    for thisComponent in Start.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "Start" ---
    Start.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *start_text* updates
        
        # if start_text is starting this frame...
        if start_text.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
            # keep track of start time/frame for later
            start_text.frameNStart = frameN  # exact frame index
            start_text.tStart = t  # local t and not account for scr refresh
            start_text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(start_text, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'start_text.started')
            # update status
            start_text.status = STARTED
            start_text.setAutoDraw(True)
        
        # if start_text is active this frame...
        if start_text.status == STARTED:
            # update params
            pass
        
        # *key_resp* updates
        waitOnFlip = False
        
        # if key_resp is starting this frame...
        if key_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            key_resp.frameNStart = frameN  # exact frame index
            key_resp.tStart = t  # local t and not account for scr refresh
            key_resp.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(key_resp, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'key_resp.started')
            # update status
            key_resp.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(key_resp.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(key_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if key_resp.status == STARTED and not waitOnFlip:
            theseKeys = key_resp.getKeys(keyList=['0'], ignoreKeys=["escape"], waitRelease=False)
            _key_resp_allKeys.extend(theseKeys)
            if len(_key_resp_allKeys):
                key_resp.keys = _key_resp_allKeys[-1].name  # just the last key pressed
                key_resp.rt = _key_resp_allKeys[-1].rt
                key_resp.duration = _key_resp_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[]
            )
            # skip the frame we paused on
            continue
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            Start.forceEnded = routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in Start.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "Start" ---
    for thisComponent in Start.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for Start
    Start.tStop = globalClock.getTime(format='float')
    Start.tStopRefresh = tThisFlipGlobal
    thisExp.addData('Start.stopped', Start.tStop)
    # Run 'End Routine' code from start_code
    try:
        # Check system status
        status = syn.getSystemStatus()
        print(f"System status: {status}")
        
        # Record initial trigger to mark experiment start
        EXP_START = 9999
        syn.setParameterValue('TTL2Int1', 'IntegerValue', EXP_START)
        syn.setParameterValue('TTL2Int1', 'ManualTrigger', 1)
        core.wait(0.01)
        syn.setParameterValue('TTL2Int1', 'ManualTrigger', 0)
        print("=============================================") 
        print(f"Experiment start trigger {EXP_START} sent")
        print("=============================================") 
        
        core.wait(1)
    except Exception as e:
        print(f"Failed to switch to Record mode: {e}")
        core.quit()
    # check responses
    if key_resp.keys in ['', [], None]:  # No response was made
        key_resp.keys = None
    thisExp.addData('key_resp.keys',key_resp.keys)
    if key_resp.keys != None:  # we had a response
        thisExp.addData('key_resp.rt', key_resp.rt)
        thisExp.addData('key_resp.duration', key_resp.duration)
    thisExp.nextEntry()
    # the Routine "Start" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "Geling" ---
    # create an object to store info about Routine Geling
    Geling = data.Routine(
        name='Geling',
        components=[gelling_text, gelling_key],
    )
    Geling.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # Run 'Begin Routine' code from gelling_code
    # Gelling trigger settings
    GELLING_START = 9000
    GELLING_END = 9001
    
    # Send Gelling start trigger
    syn.setParameterValue('TTL2Int1', 'IntegerValue', GELLING_START)
    syn.setParameterValue('TTL2Int1', 'ManualTrigger', 1)
    core.wait(0.01)
    syn.setParameterValue('TTL2Int1', 'ManualTrigger', 0)
    print("=============================================") 
    print(f"Gelling started - Trigger {GELLING_START} sent")
    print("=============================================") 
    
    # Launch impedance checker
    import subprocess
    win.winHandle.minimize()
    print("PsychoPy window minimized")
    
    imp_check_file = "C:/Users/KIST/Desktop/임피던스체커 패키지/check_realtime_imp.exe"
    if os.path.exists(imp_check_file):
        impedance_process = subprocess.Popen([imp_check_file])
        print("Impedance checker launched")
    else:
        raise Exception("Warning: Impedance checker file not found")
    # create starting attributes for gelling_key
    gelling_key.keys = []
    gelling_key.rt = []
    _gelling_key_allKeys = []
    # store start times for Geling
    Geling.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    Geling.tStart = globalClock.getTime(format='float')
    Geling.status = STARTED
    thisExp.addData('Geling.started', Geling.tStart)
    Geling.maxDuration = None
    # keep track of which components have finished
    GelingComponents = Geling.components
    for thisComponent in Geling.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "Geling" ---
    Geling.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *gelling_text* updates
        
        # if gelling_text is starting this frame...
        if gelling_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            gelling_text.frameNStart = frameN  # exact frame index
            gelling_text.tStart = t  # local t and not account for scr refresh
            gelling_text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(gelling_text, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'gelling_text.started')
            # update status
            gelling_text.status = STARTED
            gelling_text.setAutoDraw(True)
        
        # if gelling_text is active this frame...
        if gelling_text.status == STARTED:
            # update params
            pass
        
        # *gelling_key* updates
        waitOnFlip = False
        
        # if gelling_key is starting this frame...
        if gelling_key.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            gelling_key.frameNStart = frameN  # exact frame index
            gelling_key.tStart = t  # local t and not account for scr refresh
            gelling_key.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(gelling_key, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'gelling_key.started')
            # update status
            gelling_key.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(gelling_key.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(gelling_key.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if gelling_key.status == STARTED and not waitOnFlip:
            theseKeys = gelling_key.getKeys(keyList=['9'], ignoreKeys=["escape"], waitRelease=False)
            _gelling_key_allKeys.extend(theseKeys)
            if len(_gelling_key_allKeys):
                gelling_key.keys = _gelling_key_allKeys[-1].name  # just the last key pressed
                gelling_key.rt = _gelling_key_allKeys[-1].rt
                gelling_key.duration = _gelling_key_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[]
            )
            # skip the frame we paused on
            continue
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            Geling.forceEnded = routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in Geling.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "Geling" ---
    for thisComponent in Geling.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for Geling
    Geling.tStop = globalClock.getTime(format='float')
    Geling.tStopRefresh = tThisFlipGlobal
    thisExp.addData('Geling.stopped', Geling.tStop)
    # Run 'End Routine' code from gelling_code
    win.winHandle.activate()
    print("PsychoPy window activated")
    
    # Send Gelling end trigger
    syn.setParameterValue('TTL2Int1', 'IntegerValue', int(GELLING_END))
    syn.setParameterValue('TTL2Int1', 'ManualTrigger', 1)
    core.wait(0.01)
    syn.setParameterValue('TTL2Int1', 'ManualTrigger', 0)
    print("=============================================") 
    print(f"Gelling ended - Trigger {GELLING_END} sent")
    print("=============================================") 
    
    # Ensure impedance checker is fully closed
    try:
        os.system("taskkill /F /IM check_realtime_imp.exe")
        print("Impedance checker killed by process name")
    except Exception as e:
        print(f"Error: {e}")
    # check responses
    if gelling_key.keys in ['', [], None]:  # No response was made
        gelling_key.keys = None
    thisExp.addData('gelling_key.keys',gelling_key.keys)
    if gelling_key.keys != None:  # we had a response
        thisExp.addData('gelling_key.rt', gelling_key.rt)
        thisExp.addData('gelling_key.duration', gelling_key.duration)
    thisExp.nextEntry()
    # the Routine "Geling" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "Gelling_end" ---
    # create an object to store info about Routine Gelling_end
    Gelling_end = data.Routine(
        name='Gelling_end',
        components=[gelling_end_text],
    )
    Gelling_end.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # store start times for Gelling_end
    Gelling_end.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    Gelling_end.tStart = globalClock.getTime(format='float')
    Gelling_end.status = STARTED
    thisExp.addData('Gelling_end.started', Gelling_end.tStart)
    Gelling_end.maxDuration = None
    # keep track of which components have finished
    Gelling_endComponents = Gelling_end.components
    for thisComponent in Gelling_end.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "Gelling_end" ---
    Gelling_end.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine and routineTimer.getTime() < 20.0:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *gelling_end_text* updates
        
        # if gelling_end_text is starting this frame...
        if gelling_end_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            gelling_end_text.frameNStart = frameN  # exact frame index
            gelling_end_text.tStart = t  # local t and not account for scr refresh
            gelling_end_text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(gelling_end_text, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'gelling_end_text.started')
            # update status
            gelling_end_text.status = STARTED
            gelling_end_text.setAutoDraw(True)
        
        # if gelling_end_text is active this frame...
        if gelling_end_text.status == STARTED:
            # update params
            pass
        
        # if gelling_end_text is stopping this frame...
        if gelling_end_text.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > gelling_end_text.tStartRefresh + 20-frameTolerance:
                # keep track of stop time/frame for later
                gelling_end_text.tStop = t  # not accounting for scr refresh
                gelling_end_text.tStopRefresh = tThisFlipGlobal  # on global time
                gelling_end_text.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'gelling_end_text.stopped')
                # update status
                gelling_end_text.status = FINISHED
                gelling_end_text.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[]
            )
            # skip the frame we paused on
            continue
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            Gelling_end.forceEnded = routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in Gelling_end.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "Gelling_end" ---
    for thisComponent in Gelling_end.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for Gelling_end
    Gelling_end.tStop = globalClock.getTime(format='float')
    Gelling_end.tStopRefresh = tThisFlipGlobal
    thisExp.addData('Gelling_end.stopped', Gelling_end.tStop)
    # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
    if Gelling_end.maxDurationReached:
        routineTimer.addTime(-Gelling_end.maxDuration)
    elif Gelling_end.forceEnded:
        routineTimer.reset()
    else:
        routineTimer.addTime(-20.000000)
    thisExp.nextEntry()
    
    # --- Prepare to start Routine "ERP_start" ---
    # create an object to store info about Routine ERP_start
    ERP_start = data.Routine(
        name='ERP_start',
        components=[erp_start_text, erp_start_key],
    )
    ERP_start.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # Run 'Begin Routine' code from erp_start_code
    # Send ERP block start trigger
    ERP_START = 8000
    syn.setParameterValue('TTL2Int1', 'IntegerValue', int(ERP_START))
    syn.setParameterValue('TTL2Int1', 'ManualTrigger', 1)
    core.wait(0.01)
    syn.setParameterValue('TTL2Int1', 'ManualTrigger', 0)
    print("=============================================") 
    print(f"ERP Block started - Trigger {ERP_START} sent")
    print("=============================================")
    # create starting attributes for erp_start_key
    erp_start_key.keys = []
    erp_start_key.rt = []
    _erp_start_key_allKeys = []
    # store start times for ERP_start
    ERP_start.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    ERP_start.tStart = globalClock.getTime(format='float')
    ERP_start.status = STARTED
    thisExp.addData('ERP_start.started', ERP_start.tStart)
    ERP_start.maxDuration = None
    # keep track of which components have finished
    ERP_startComponents = ERP_start.components
    for thisComponent in ERP_start.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "ERP_start" ---
    ERP_start.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *erp_start_text* updates
        
        # if erp_start_text is starting this frame...
        if erp_start_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            erp_start_text.frameNStart = frameN  # exact frame index
            erp_start_text.tStart = t  # local t and not account for scr refresh
            erp_start_text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(erp_start_text, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'erp_start_text.started')
            # update status
            erp_start_text.status = STARTED
            erp_start_text.setAutoDraw(True)
        
        # if erp_start_text is active this frame...
        if erp_start_text.status == STARTED:
            # update params
            pass
        
        # *erp_start_key* updates
        waitOnFlip = False
        
        # if erp_start_key is starting this frame...
        if erp_start_key.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            erp_start_key.frameNStart = frameN  # exact frame index
            erp_start_key.tStart = t  # local t and not account for scr refresh
            erp_start_key.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(erp_start_key, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'erp_start_key.started')
            # update status
            erp_start_key.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(erp_start_key.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(erp_start_key.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if erp_start_key.status == STARTED and not waitOnFlip:
            theseKeys = erp_start_key.getKeys(keyList=['0'], ignoreKeys=["escape"], waitRelease=False)
            _erp_start_key_allKeys.extend(theseKeys)
            if len(_erp_start_key_allKeys):
                erp_start_key.keys = _erp_start_key_allKeys[-1].name  # just the last key pressed
                erp_start_key.rt = _erp_start_key_allKeys[-1].rt
                erp_start_key.duration = _erp_start_key_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[]
            )
            # skip the frame we paused on
            continue
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            ERP_start.forceEnded = routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in ERP_start.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "ERP_start" ---
    for thisComponent in ERP_start.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for ERP_start
    ERP_start.tStop = globalClock.getTime(format='float')
    ERP_start.tStopRefresh = tThisFlipGlobal
    thisExp.addData('ERP_start.stopped', ERP_start.tStop)
    # check responses
    if erp_start_key.keys in ['', [], None]:  # No response was made
        erp_start_key.keys = None
    thisExp.addData('erp_start_key.keys',erp_start_key.keys)
    if erp_start_key.keys != None:  # we had a response
        thisExp.addData('erp_start_key.rt', erp_start_key.rt)
        thisExp.addData('erp_start_key.duration', erp_start_key.duration)
    thisExp.nextEntry()
    # the Routine "ERP_start" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # set up handler to look after randomisation of conditions etc
    erp_trials = data.TrialHandler2(
        name='erp_trials',
        nReps=1.0, 
        method='sequential', 
        extraInfo=expInfo, 
        originPath=-1, 
        trialList=data.importConditions('erp_stimuli/erp_stimuli.csv'), 
        seed=None, 
    )
    thisExp.addLoop(erp_trials)  # add the loop to the experiment
    thisErp_trial = erp_trials.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisErp_trial.rgb)
    if thisErp_trial != None:
        for paramName in thisErp_trial:
            globals()[paramName] = thisErp_trial[paramName]
    if thisSession is not None:
        # if running in a Session with a Liaison client, send data up to now
        thisSession.sendExperimentData()
    
    for thisErp_trial in erp_trials:
        currentLoop = erp_trials
        thisExp.timestampOnFlip(win, 'thisRow.t', format=globalClock.format)
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
        # abbreviate parameter names if possible (e.g. rgb = thisErp_trial.rgb)
        if thisErp_trial != None:
            for paramName in thisErp_trial:
                globals()[paramName] = thisErp_trial[paramName]
        
        # --- Prepare to start Routine "ERP" ---
        # create an object to store info about Routine ERP
        ERP = data.Routine(
            name='ERP',
            components=[erp_stimuli, erp_text_rest, erp_text_isi],
        )
        ERP.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        # Run 'Begin Routine' code from erp_code
        # Get trigger ID from CSV
        trigger_id = int(erp_trials.thisTrial['trigger_id'])  # from CSV trigger_id column
        
        # Send trigger at stimulus onset (sync with sound start)
        syn.setParameterValue('TTL2Int1', 'IntegerValue', trigger_id)
        syn.setParameterValue('TTL2Int1', 'ManualTrigger', 1)
        core.wait(0.01)
        syn.setParameterValue('TTL2Int1', 'ManualTrigger', 0)
        print("=============================================")
        print(f"ERP Trial {index}: Trigger {trigger_id} sent, ISI = {isi:.3f}s")
        print("=============================================")
        erp_stimuli.setSound(fname, hamming=True)
        erp_stimuli.setVolume(1.0, log=False)
        erp_stimuli.seek(0)
        # store start times for ERP
        ERP.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        ERP.tStart = globalClock.getTime(format='float')
        ERP.status = STARTED
        thisExp.addData('ERP.started', ERP.tStart)
        ERP.maxDuration = None
        # keep track of which components have finished
        ERPComponents = ERP.components
        for thisComponent in ERP.components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "ERP" ---
        # if trial has changed, end Routine now
        if isinstance(erp_trials, data.TrialHandler2) and thisErp_trial.thisN != erp_trials.thisTrial.thisN:
            continueRoutine = False
        ERP.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *erp_stimuli* updates
            
            # if erp_stimuli is starting this frame...
            if erp_stimuli.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                erp_stimuli.frameNStart = frameN  # exact frame index
                erp_stimuli.tStart = t  # local t and not account for scr refresh
                erp_stimuli.tStartRefresh = tThisFlipGlobal  # on global time
                # add timestamp to datafile
                thisExp.addData('erp_stimuli.started', tThisFlipGlobal)
                # update status
                erp_stimuli.status = STARTED
                erp_stimuli.play(when=win)  # sync with win flip
            
            # if erp_stimuli is stopping this frame...
            if erp_stimuli.status == STARTED:
                if bool(False) or erp_stimuli.isFinished:
                    # keep track of stop time/frame for later
                    erp_stimuli.tStop = t  # not accounting for scr refresh
                    erp_stimuli.tStopRefresh = tThisFlipGlobal  # on global time
                    erp_stimuli.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'erp_stimuli.stopped')
                    # update status
                    erp_stimuli.status = FINISHED
                    erp_stimuli.stop()
            
            # *erp_text_rest* updates
            
            # if erp_text_rest is starting this frame...
            if erp_text_rest.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                erp_text_rest.frameNStart = frameN  # exact frame index
                erp_text_rest.tStart = t  # local t and not account for scr refresh
                erp_text_rest.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(erp_text_rest, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'erp_text_rest.started')
                # update status
                erp_text_rest.status = STARTED
                erp_text_rest.setAutoDraw(True)
            
            # if erp_text_rest is active this frame...
            if erp_text_rest.status == STARTED:
                # update params
                pass
            
            # if erp_text_rest is stopping this frame...
            if erp_text_rest.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > erp_text_rest.tStartRefresh + 1.0-frameTolerance:
                    # keep track of stop time/frame for later
                    erp_text_rest.tStop = t  # not accounting for scr refresh
                    erp_text_rest.tStopRefresh = tThisFlipGlobal  # on global time
                    erp_text_rest.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'erp_text_rest.stopped')
                    # update status
                    erp_text_rest.status = FINISHED
                    erp_text_rest.setAutoDraw(False)
            
            # *erp_text_isi* updates
            
            # if erp_text_isi is starting this frame...
            if erp_text_isi.status == NOT_STARTED and tThisFlip >= 1.0-frameTolerance:
                # keep track of start time/frame for later
                erp_text_isi.frameNStart = frameN  # exact frame index
                erp_text_isi.tStart = t  # local t and not account for scr refresh
                erp_text_isi.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(erp_text_isi, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'erp_text_isi.started')
                # update status
                erp_text_isi.status = STARTED
                erp_text_isi.setAutoDraw(True)
            
            # if erp_text_isi is active this frame...
            if erp_text_isi.status == STARTED:
                # update params
                pass
            
            # if erp_text_isi is stopping this frame...
            if erp_text_isi.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > erp_text_isi.tStartRefresh + isi-frameTolerance:
                    # keep track of stop time/frame for later
                    erp_text_isi.tStop = t  # not accounting for scr refresh
                    erp_text_isi.tStopRefresh = tThisFlipGlobal  # on global time
                    erp_text_isi.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'erp_text_isi.stopped')
                    # update status
                    erp_text_isi.status = FINISHED
                    erp_text_isi.setAutoDraw(False)
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer], 
                    playbackComponents=[erp_stimuli]
                )
                # skip the frame we paused on
                continue
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                ERP.forceEnded = routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in ERP.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "ERP" ---
        for thisComponent in ERP.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for ERP
        ERP.tStop = globalClock.getTime(format='float')
        ERP.tStopRefresh = tThisFlipGlobal
        thisExp.addData('ERP.stopped', ERP.tStop)
        # Run 'End Routine' code from erp_code
        # Backup save after ERP block
        backup_filename = filename + '_ERP_backup.csv'
        if os.path.exists(backup_filename):
            os.remove(backup_filename)
        thisExp.saveAsWideText(backup_filename)
        print(f"ERP backup data saved: {backup_filename}")
        erp_stimuli.pause()  # ensure sound has stopped at end of Routine
        # the Routine "ERP" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        thisExp.nextEntry()
        
    # completed 1.0 repeats of 'erp_trials'
    
    if thisSession is not None:
        # if running in a Session with a Liaison client, send data up to now
        thisSession.sendExperimentData()
    
    # --- Prepare to start Routine "ERP_end" ---
    # create an object to store info about Routine ERP_end
    ERP_end = data.Routine(
        name='ERP_end',
        components=[erp_end_text, erp_end_key],
    )
    ERP_end.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # create starting attributes for erp_end_key
    erp_end_key.keys = []
    erp_end_key.rt = []
    _erp_end_key_allKeys = []
    # store start times for ERP_end
    ERP_end.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    ERP_end.tStart = globalClock.getTime(format='float')
    ERP_end.status = STARTED
    thisExp.addData('ERP_end.started', ERP_end.tStart)
    ERP_end.maxDuration = None
    # keep track of which components have finished
    ERP_endComponents = ERP_end.components
    for thisComponent in ERP_end.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "ERP_end" ---
    ERP_end.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *erp_end_text* updates
        
        # if erp_end_text is starting this frame...
        if erp_end_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            erp_end_text.frameNStart = frameN  # exact frame index
            erp_end_text.tStart = t  # local t and not account for scr refresh
            erp_end_text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(erp_end_text, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'erp_end_text.started')
            # update status
            erp_end_text.status = STARTED
            erp_end_text.setAutoDraw(True)
        
        # if erp_end_text is active this frame...
        if erp_end_text.status == STARTED:
            # update params
            pass
        
        # *erp_end_key* updates
        waitOnFlip = False
        
        # if erp_end_key is starting this frame...
        if erp_end_key.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            erp_end_key.frameNStart = frameN  # exact frame index
            erp_end_key.tStart = t  # local t and not account for scr refresh
            erp_end_key.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(erp_end_key, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'erp_end_key.started')
            # update status
            erp_end_key.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(erp_end_key.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(erp_end_key.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if erp_end_key.status == STARTED and not waitOnFlip:
            theseKeys = erp_end_key.getKeys(keyList=['0'], ignoreKeys=["escape"], waitRelease=False)
            _erp_end_key_allKeys.extend(theseKeys)
            if len(_erp_end_key_allKeys):
                erp_end_key.keys = _erp_end_key_allKeys[-1].name  # just the last key pressed
                erp_end_key.rt = _erp_end_key_allKeys[-1].rt
                erp_end_key.duration = _erp_end_key_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[]
            )
            # skip the frame we paused on
            continue
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            ERP_end.forceEnded = routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in ERP_end.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "ERP_end" ---
    for thisComponent in ERP_end.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for ERP_end
    ERP_end.tStop = globalClock.getTime(format='float')
    ERP_end.tStopRefresh = tThisFlipGlobal
    thisExp.addData('ERP_end.stopped', ERP_end.tStop)
    # Run 'End Routine' code from erp_end_code
    # Send ERP block end trigger
    ERP_END = 8999
    syn.setParameterValue('TTL2Int1', 'IntegerValue', ERP_END)
    syn.setParameterValue('TTL2Int1', 'ManualTrigger', 1)
    core.wait(0.01)
    syn.setParameterValue('TTL2Int1', 'ManualTrigger', 0)
    print("=============================================") 
    print(f"ERP Block ended - Trigger {ERP_END} sent")
    print("=============================================") 
    
            
    core.wait(2)
    # check responses
    if erp_end_key.keys in ['', [], None]:  # No response was made
        erp_end_key.keys = None
    thisExp.addData('erp_end_key.keys',erp_end_key.keys)
    if erp_end_key.keys != None:  # we had a response
        thisExp.addData('erp_end_key.rt', erp_end_key.rt)
        thisExp.addData('erp_end_key.duration', erp_end_key.duration)
    thisExp.nextEntry()
    # the Routine "ERP_end" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "Main_start" ---
    # create an object to store info about Routine Main_start
    Main_start = data.Routine(
        name='Main_start',
        components=[main_start_text, main_start_key],
    )
    Main_start.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # Run 'Begin Routine' code from main_start_code
    # Send Main block start trigger
    MAIN_START = 0
    syn.setParameterValue('TTL2Int1', 'IntegerValue', MAIN_START)
    syn.setParameterValue('TTL2Int1', 'ManualTrigger', 1)
    core.wait(0.01)
    syn.setParameterValue('TTL2Int1', 'ManualTrigger', 0)
    print("=============================================")
    print(f"Main Block started - Trigger {MAIN_START} sent")
    print("=============================================")
    
    # create starting attributes for main_start_key
    main_start_key.keys = []
    main_start_key.rt = []
    _main_start_key_allKeys = []
    # store start times for Main_start
    Main_start.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    Main_start.tStart = globalClock.getTime(format='float')
    Main_start.status = STARTED
    thisExp.addData('Main_start.started', Main_start.tStart)
    Main_start.maxDuration = None
    # keep track of which components have finished
    Main_startComponents = Main_start.components
    for thisComponent in Main_start.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "Main_start" ---
    Main_start.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *main_start_text* updates
        
        # if main_start_text is starting this frame...
        if main_start_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            main_start_text.frameNStart = frameN  # exact frame index
            main_start_text.tStart = t  # local t and not account for scr refresh
            main_start_text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(main_start_text, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'main_start_text.started')
            # update status
            main_start_text.status = STARTED
            main_start_text.setAutoDraw(True)
        
        # if main_start_text is active this frame...
        if main_start_text.status == STARTED:
            # update params
            pass
        
        # *main_start_key* updates
        waitOnFlip = False
        
        # if main_start_key is starting this frame...
        if main_start_key.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            main_start_key.frameNStart = frameN  # exact frame index
            main_start_key.tStart = t  # local t and not account for scr refresh
            main_start_key.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(main_start_key, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'main_start_key.started')
            # update status
            main_start_key.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(main_start_key.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(main_start_key.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if main_start_key.status == STARTED and not waitOnFlip:
            theseKeys = main_start_key.getKeys(keyList=['0'], ignoreKeys=["escape"], waitRelease=False)
            _main_start_key_allKeys.extend(theseKeys)
            if len(_main_start_key_allKeys):
                main_start_key.keys = _main_start_key_allKeys[-1].name  # just the last key pressed
                main_start_key.rt = _main_start_key_allKeys[-1].rt
                main_start_key.duration = _main_start_key_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[]
            )
            # skip the frame we paused on
            continue
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            Main_start.forceEnded = routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in Main_start.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "Main_start" ---
    for thisComponent in Main_start.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for Main_start
    Main_start.tStop = globalClock.getTime(format='float')
    Main_start.tStopRefresh = tThisFlipGlobal
    thisExp.addData('Main_start.stopped', Main_start.tStop)
    # check responses
    if main_start_key.keys in ['', [], None]:  # No response was made
        main_start_key.keys = None
    thisExp.addData('main_start_key.keys',main_start_key.keys)
    if main_start_key.keys != None:  # we had a response
        thisExp.addData('main_start_key.rt', main_start_key.rt)
        thisExp.addData('main_start_key.duration', main_start_key.duration)
    thisExp.nextEntry()
    # the Routine "Main_start" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # set up handler to look after randomisation of conditions etc
    main_trials = data.TrialHandler2(
        name='main_trials',
        nReps=1.0, 
        method='sequential', 
        extraInfo=expInfo, 
        originPath=-1, 
        trialList=data.importConditions('main_stimuli/main_stimuli.csv'), 
        seed=None, 
    )
    thisExp.addLoop(main_trials)  # add the loop to the experiment
    thisMain_trial = main_trials.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisMain_trial.rgb)
    if thisMain_trial != None:
        for paramName in thisMain_trial:
            globals()[paramName] = thisMain_trial[paramName]
    if thisSession is not None:
        # if running in a Session with a Liaison client, send data up to now
        thisSession.sendExperimentData()
    
    for thisMain_trial in main_trials:
        currentLoop = main_trials
        thisExp.timestampOnFlip(win, 'thisRow.t', format=globalClock.format)
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
        # abbreviate parameter names if possible (e.g. rgb = thisMain_trial.rgb)
        if thisMain_trial != None:
            for paramName in thisMain_trial:
                globals()[paramName] = thisMain_trial[paramName]
        
        # --- Prepare to start Routine "Main" ---
        # create an object to store info about Routine Main
        Main = data.Routine(
            name='Main',
            components=[main_stimuli, main_text_rest, main_text_isi],
        )
        Main.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        # Run 'Begin Routine' code from main_code
        # Get trigger ID from CSV
        trigger_id = int(main_trials.thisTrial['trigger_id'])  # from CSV trigger_id column
        syn.setParameterValue('TTL2Int1', 'IntegerValue', trigger_id)
        syn.setParameterValue('TTL2Int1', 'ManualTrigger', 1)
        core.wait(0.01)
        syn.setParameterValue('TTL2Int1', 'ManualTrigger', 0)
        print("=============================================")
        print(f"Main Trial {index}: {fname}, Trigger {trigger_id} sent")
        print("=============================================")
        main_stimuli.setSound(fname, hamming=True)
        main_stimuli.setVolume(1.0, log=False)
        main_stimuli.seek(0)
        # store start times for Main
        Main.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        Main.tStart = globalClock.getTime(format='float')
        Main.status = STARTED
        thisExp.addData('Main.started', Main.tStart)
        Main.maxDuration = None
        # keep track of which components have finished
        MainComponents = Main.components
        for thisComponent in Main.components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "Main" ---
        # if trial has changed, end Routine now
        if isinstance(main_trials, data.TrialHandler2) and thisMain_trial.thisN != main_trials.thisTrial.thisN:
            continueRoutine = False
        Main.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *main_stimuli* updates
            
            # if main_stimuli is starting this frame...
            if main_stimuli.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                main_stimuli.frameNStart = frameN  # exact frame index
                main_stimuli.tStart = t  # local t and not account for scr refresh
                main_stimuli.tStartRefresh = tThisFlipGlobal  # on global time
                # add timestamp to datafile
                thisExp.addData('main_stimuli.started', tThisFlipGlobal)
                # update status
                main_stimuli.status = STARTED
                main_stimuli.play(when=win)  # sync with win flip
            
            # if main_stimuli is stopping this frame...
            if main_stimuli.status == STARTED:
                if bool(False) or main_stimuli.isFinished:
                    # keep track of stop time/frame for later
                    main_stimuli.tStop = t  # not accounting for scr refresh
                    main_stimuli.tStopRefresh = tThisFlipGlobal  # on global time
                    main_stimuli.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'main_stimuli.stopped')
                    # update status
                    main_stimuli.status = FINISHED
                    main_stimuli.stop()
            
            # *main_text_rest* updates
            
            # if main_text_rest is starting this frame...
            if main_text_rest.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                main_text_rest.frameNStart = frameN  # exact frame index
                main_text_rest.tStart = t  # local t and not account for scr refresh
                main_text_rest.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(main_text_rest, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'main_text_rest.started')
                # update status
                main_text_rest.status = STARTED
                main_text_rest.setAutoDraw(True)
            
            # if main_text_rest is active this frame...
            if main_text_rest.status == STARTED:
                # update params
                pass
            
            # if main_text_rest is stopping this frame...
            if main_text_rest.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > main_text_rest.tStartRefresh + 1.0-frameTolerance:
                    # keep track of stop time/frame for later
                    main_text_rest.tStop = t  # not accounting for scr refresh
                    main_text_rest.tStopRefresh = tThisFlipGlobal  # on global time
                    main_text_rest.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'main_text_rest.stopped')
                    # update status
                    main_text_rest.status = FINISHED
                    main_text_rest.setAutoDraw(False)
            
            # *main_text_isi* updates
            
            # if main_text_isi is starting this frame...
            if main_text_isi.status == NOT_STARTED and tThisFlip >= 1.0-frameTolerance:
                # keep track of start time/frame for later
                main_text_isi.frameNStart = frameN  # exact frame index
                main_text_isi.tStart = t  # local t and not account for scr refresh
                main_text_isi.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(main_text_isi, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'main_text_isi.started')
                # update status
                main_text_isi.status = STARTED
                main_text_isi.setAutoDraw(True)
            
            # if main_text_isi is active this frame...
            if main_text_isi.status == STARTED:
                # update params
                pass
            
            # if main_text_isi is stopping this frame...
            if main_text_isi.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > main_text_isi.tStartRefresh + main_fixed_isi-frameTolerance:
                    # keep track of stop time/frame for later
                    main_text_isi.tStop = t  # not accounting for scr refresh
                    main_text_isi.tStopRefresh = tThisFlipGlobal  # on global time
                    main_text_isi.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'main_text_isi.stopped')
                    # update status
                    main_text_isi.status = FINISHED
                    main_text_isi.setAutoDraw(False)
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer], 
                    playbackComponents=[main_stimuli]
                )
                # skip the frame we paused on
                continue
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                Main.forceEnded = routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in Main.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "Main" ---
        for thisComponent in Main.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for Main
        Main.tStop = globalClock.getTime(format='float')
        Main.tStopRefresh = tThisFlipGlobal
        thisExp.addData('Main.stopped', Main.tStop)
        main_stimuli.pause()  # ensure sound has stopped at end of Routine
        # the Routine "Main" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # --- Prepare to start Routine "quiz" ---
        # create an object to store info about Routine quiz
        quiz = data.Routine(
            name='quiz',
            components=[quiz_text, quiz_key],
        )
        quiz.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        # Run 'Begin Routine' code from quiz_code
        quiz_trigger = trigger_id + 1000
        syn.setParameterValue('TTL2Int1', 'IntegerValue', quiz_trigger)
        syn.setParameterValue('TTL2Int1', 'ManualTrigger', 1)
        core.wait(0.01)
        syn.setParameterValue('TTL2Int1', 'ManualTrigger', 0)
        print("=============================================")
        print(f"Main Trial {index}: {fname}, Quiz Trigger {quiz_trigger} sent")
        print("=============================================")
        quiz_text.setText(quiz_content)
        # create starting attributes for quiz_key
        quiz_key.keys = []
        quiz_key.rt = []
        _quiz_key_allKeys = []
        # store start times for quiz
        quiz.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        quiz.tStart = globalClock.getTime(format='float')
        quiz.status = STARTED
        thisExp.addData('quiz.started', quiz.tStart)
        quiz.maxDuration = None
        # keep track of which components have finished
        quizComponents = quiz.components
        for thisComponent in quiz.components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "quiz" ---
        # if trial has changed, end Routine now
        if isinstance(main_trials, data.TrialHandler2) and thisMain_trial.thisN != main_trials.thisTrial.thisN:
            continueRoutine = False
        quiz.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *quiz_text* updates
            
            # if quiz_text is starting this frame...
            if quiz_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                quiz_text.frameNStart = frameN  # exact frame index
                quiz_text.tStart = t  # local t and not account for scr refresh
                quiz_text.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(quiz_text, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'quiz_text.started')
                # update status
                quiz_text.status = STARTED
                quiz_text.setAutoDraw(True)
            
            # if quiz_text is active this frame...
            if quiz_text.status == STARTED:
                # update params
                pass
            
            # *quiz_key* updates
            waitOnFlip = False
            
            # if quiz_key is starting this frame...
            if quiz_key.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                quiz_key.frameNStart = frameN  # exact frame index
                quiz_key.tStart = t  # local t and not account for scr refresh
                quiz_key.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(quiz_key, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'quiz_key.started')
                # update status
                quiz_key.status = STARTED
                # keyboard checking is just starting
                waitOnFlip = True
                win.callOnFlip(quiz_key.clock.reset)  # t=0 on next screen flip
                win.callOnFlip(quiz_key.clearEvents, eventType='keyboard')  # clear events on next screen flip
            if quiz_key.status == STARTED and not waitOnFlip:
                theseKeys = quiz_key.getKeys(keyList=['1','2','3','4', 'num_1', 'num_2', 'num_3', 'num_4'], ignoreKeys=["escape"], waitRelease=False)
                _quiz_key_allKeys.extend(theseKeys)
                if len(_quiz_key_allKeys):
                    quiz_key.keys = _quiz_key_allKeys[-1].name  # just the last key pressed
                    quiz_key.rt = _quiz_key_allKeys[-1].rt
                    quiz_key.duration = _quiz_key_allKeys[-1].duration
                    # was this correct?
                    if (quiz_key.keys == str(ans)) or (quiz_key.keys == ans):
                        quiz_key.corr = 1
                    else:
                        quiz_key.corr = 0
                    # a response ends the routine
                    continueRoutine = False
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer], 
                    playbackComponents=[]
                )
                # skip the frame we paused on
                continue
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                quiz.forceEnded = routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in quiz.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "quiz" ---
        for thisComponent in quiz.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for quiz
        quiz.tStop = globalClock.getTime(format='float')
        quiz.tStopRefresh = tThisFlipGlobal
        thisExp.addData('quiz.stopped', quiz.tStop)
        # Run 'End Routine' code from quiz_code
        # Send trigger once there is an input on keyboard
        if quiz_key.keys:
            if quiz_key.corr:
                syn.setParameterValue('TTL2Int1', 'IntegerValue', quiz_correct)
                syn.setParameterValue('TTL2Int1', 'ManualTrigger', 1)
                core.wait(0.01)
                syn.setParameterValue('TTL2Int1', 'ManualTrigger', 0)
                print("=============================================")
                print(f"Quiz correct : Trigger {quiz_correct} sent")
                print("=============================================")
            else:
                syn.setParameterValue('TTL2Int1', 'IntegerValue', quiz_wrong)
                syn.setParameterValue('TTL2Int1', 'ManualTrigger', 1)
                core.wait(0.01)
                syn.setParameterValue('TTL2Int1', 'ManualTrigger', 0)
                print("=============================================")
                print(f"Quiz wrong : Trigger {quiz_wrong} sent")
                print("=============================================")
        
        # check responses
        if quiz_key.keys in ['', [], None]:  # No response was made
            quiz_key.keys = None
            # was no response the correct answer?!
            if str(ans).lower() == 'none':
               quiz_key.corr = 1;  # correct non-response
            else:
               quiz_key.corr = 0;  # failed to respond (incorrectly)
        # store data for main_trials (TrialHandler)
        main_trials.addData('quiz_key.keys',quiz_key.keys)
        main_trials.addData('quiz_key.corr', quiz_key.corr)
        if quiz_key.keys != None:  # we had a response
            main_trials.addData('quiz_key.rt', quiz_key.rt)
            main_trials.addData('quiz_key.duration', quiz_key.duration)
        # the Routine "quiz" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # --- Prepare to start Routine "rest" ---
        # create an object to store info about Routine rest
        rest = data.Routine(
            name='rest',
            components=[rest_text, rest_key],
        )
        rest.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        # create starting attributes for rest_key
        rest_key.keys = []
        rest_key.rt = []
        _rest_key_allKeys = []
        # store start times for rest
        rest.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        rest.tStart = globalClock.getTime(format='float')
        rest.status = STARTED
        thisExp.addData('rest.started', rest.tStart)
        rest.maxDuration = None
        # keep track of which components have finished
        restComponents = rest.components
        for thisComponent in rest.components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "rest" ---
        # if trial has changed, end Routine now
        if isinstance(main_trials, data.TrialHandler2) and thisMain_trial.thisN != main_trials.thisTrial.thisN:
            continueRoutine = False
        rest.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *rest_text* updates
            
            # if rest_text is starting this frame...
            if rest_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                rest_text.frameNStart = frameN  # exact frame index
                rest_text.tStart = t  # local t and not account for scr refresh
                rest_text.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(rest_text, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'rest_text.started')
                # update status
                rest_text.status = STARTED
                rest_text.setAutoDraw(True)
            
            # if rest_text is active this frame...
            if rest_text.status == STARTED:
                # update params
                pass
            
            # *rest_key* updates
            waitOnFlip = False
            
            # if rest_key is starting this frame...
            if rest_key.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                rest_key.frameNStart = frameN  # exact frame index
                rest_key.tStart = t  # local t and not account for scr refresh
                rest_key.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(rest_key, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'rest_key.started')
                # update status
                rest_key.status = STARTED
                # keyboard checking is just starting
                waitOnFlip = True
                win.callOnFlip(rest_key.clock.reset)  # t=0 on next screen flip
                win.callOnFlip(rest_key.clearEvents, eventType='keyboard')  # clear events on next screen flip
            if rest_key.status == STARTED and not waitOnFlip:
                theseKeys = rest_key.getKeys(keyList=['0'], ignoreKeys=["escape"], waitRelease=False)
                _rest_key_allKeys.extend(theseKeys)
                if len(_rest_key_allKeys):
                    rest_key.keys = _rest_key_allKeys[-1].name  # just the last key pressed
                    rest_key.rt = _rest_key_allKeys[-1].rt
                    rest_key.duration = _rest_key_allKeys[-1].duration
                    # a response ends the routine
                    continueRoutine = False
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer], 
                    playbackComponents=[]
                )
                # skip the frame we paused on
                continue
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                rest.forceEnded = routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in rest.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "rest" ---
        for thisComponent in rest.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for rest
        rest.tStop = globalClock.getTime(format='float')
        rest.tStopRefresh = tThisFlipGlobal
        thisExp.addData('rest.stopped', rest.tStop)
        # Run 'End Routine' code from rest_code
        # Backup save after MAIN block
        backup_filename = filename + '_MAIN_backup.csv'
        if os.path.exists(backup_filename):
            os.remove(backup_filename)
        thisExp.saveAsWideText(backup_filename)
        print(f"ERP backup data saved: {backup_filename}")
        # check responses
        if rest_key.keys in ['', [], None]:  # No response was made
            rest_key.keys = None
        main_trials.addData('rest_key.keys',rest_key.keys)
        if rest_key.keys != None:  # we had a response
            main_trials.addData('rest_key.rt', rest_key.rt)
            main_trials.addData('rest_key.duration', rest_key.duration)
        # the Routine "rest" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        thisExp.nextEntry()
        
    # completed 1.0 repeats of 'main_trials'
    
    if thisSession is not None:
        # if running in a Session with a Liaison client, send data up to now
        thisSession.sendExperimentData()
    
    # --- Prepare to start Routine "Main_end" ---
    # create an object to store info about Routine Main_end
    Main_end = data.Routine(
        name='Main_end',
        components=[main_end_text, main_end_key],
    )
    Main_end.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # create starting attributes for main_end_key
    main_end_key.keys = []
    main_end_key.rt = []
    _main_end_key_allKeys = []
    # store start times for Main_end
    Main_end.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    Main_end.tStart = globalClock.getTime(format='float')
    Main_end.status = STARTED
    thisExp.addData('Main_end.started', Main_end.tStart)
    Main_end.maxDuration = None
    # keep track of which components have finished
    Main_endComponents = Main_end.components
    for thisComponent in Main_end.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "Main_end" ---
    Main_end.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *main_end_text* updates
        
        # if main_end_text is starting this frame...
        if main_end_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            main_end_text.frameNStart = frameN  # exact frame index
            main_end_text.tStart = t  # local t and not account for scr refresh
            main_end_text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(main_end_text, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'main_end_text.started')
            # update status
            main_end_text.status = STARTED
            main_end_text.setAutoDraw(True)
        
        # if main_end_text is active this frame...
        if main_end_text.status == STARTED:
            # update params
            pass
        
        # *main_end_key* updates
        waitOnFlip = False
        
        # if main_end_key is starting this frame...
        if main_end_key.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            main_end_key.frameNStart = frameN  # exact frame index
            main_end_key.tStart = t  # local t and not account for scr refresh
            main_end_key.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(main_end_key, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'main_end_key.started')
            # update status
            main_end_key.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(main_end_key.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(main_end_key.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if main_end_key.status == STARTED and not waitOnFlip:
            theseKeys = main_end_key.getKeys(keyList=['0'], ignoreKeys=["escape"], waitRelease=False)
            _main_end_key_allKeys.extend(theseKeys)
            if len(_main_end_key_allKeys):
                main_end_key.keys = _main_end_key_allKeys[-1].name  # just the last key pressed
                main_end_key.rt = _main_end_key_allKeys[-1].rt
                main_end_key.duration = _main_end_key_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[]
            )
            # skip the frame we paused on
            continue
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            Main_end.forceEnded = routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in Main_end.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "Main_end" ---
    for thisComponent in Main_end.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for Main_end
    Main_end.tStop = globalClock.getTime(format='float')
    Main_end.tStopRefresh = tThisFlipGlobal
    thisExp.addData('Main_end.stopped', Main_end.tStop)
    # Run 'End Routine' code from main_end_code
    # Send Main block end trigger
    MAIN_END = 1999
    syn.setParameterValue('TTL2Int1', 'IntegerValue', MAIN_END)
    syn.setParameterValue('TTL2Int1', 'ManualTrigger', 1)
    core.wait(0.01)
    syn.setParameterValue('TTL2Int1', 'ManualTrigger', 0)
    print("=============================================")
    print(f"Main Block ended - Trigger {MAIN_END} sent")
    print("=============================================")
    
    # Final backup save after MAIN block
    backup_filename = filename + '_MAIN_backup.csv'
    if os.path.exists(backup_filename):
        os.remove(backup_filename)
    thisExp.saveAsWideText(backup_filename)
    print(f"ERP backup data saved: {backup_filename}")
    
    core.wait(2)
    # check responses
    if main_end_key.keys in ['', [], None]:  # No response was made
        main_end_key.keys = None
    thisExp.addData('main_end_key.keys',main_end_key.keys)
    if main_end_key.keys != None:  # we had a response
        thisExp.addData('main_end_key.rt', main_end_key.rt)
        thisExp.addData('main_end_key.duration', main_end_key.duration)
    thisExp.nextEntry()
    # the Routine "Main_end" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "Finish" ---
    # create an object to store info about Routine Finish
    Finish = data.Routine(
        name='Finish',
        components=[finish_text_1, finish_text_2, finish_key],
    )
    Finish.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # Run 'Begin Routine' code from finish_code
    # Send experiment end trigger
    EXP_END = 9998
    syn.setParameterValue('TTL2Int1', 'IntegerValue', EXP_END)
    syn.setParameterValue('TTL2Int1', 'ManualTrigger', 1)
    core.wait(0.01)
    syn.setParameterValue('TTL2Int1', 'ManualTrigger', 0)
    print("=============================================")
    print(f"Experiment end trigger {EXP_END} sent")
    print("=============================================")
    
    syn.setParameterValue('PZ5(1)', 'CheckSubAmp', 1)
    
    # Display completion message
    print("Experiment completed successfully")
    print(f"Total experiment duration: {core.getTime() - experiment_start_time:.1f} seconds")
    # create starting attributes for finish_key
    finish_key.keys = []
    finish_key.rt = []
    _finish_key_allKeys = []
    # store start times for Finish
    Finish.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    Finish.tStart = globalClock.getTime(format='float')
    Finish.status = STARTED
    thisExp.addData('Finish.started', Finish.tStart)
    Finish.maxDuration = None
    # keep track of which components have finished
    FinishComponents = Finish.components
    for thisComponent in Finish.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "Finish" ---
    Finish.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *finish_text_1* updates
        
        # if finish_text_1 is starting this frame...
        if finish_text_1.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            finish_text_1.frameNStart = frameN  # exact frame index
            finish_text_1.tStart = t  # local t and not account for scr refresh
            finish_text_1.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(finish_text_1, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'finish_text_1.started')
            # update status
            finish_text_1.status = STARTED
            finish_text_1.setAutoDraw(True)
        
        # if finish_text_1 is active this frame...
        if finish_text_1.status == STARTED:
            # update params
            pass
        
        # if finish_text_1 is stopping this frame...
        if finish_text_1.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > finish_text_1.tStartRefresh + 10-frameTolerance:
                # keep track of stop time/frame for later
                finish_text_1.tStop = t  # not accounting for scr refresh
                finish_text_1.tStopRefresh = tThisFlipGlobal  # on global time
                finish_text_1.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'finish_text_1.stopped')
                # update status
                finish_text_1.status = FINISHED
                finish_text_1.setAutoDraw(False)
        
        # *finish_text_2* updates
        
        # if finish_text_2 is starting this frame...
        if finish_text_2.status == NOT_STARTED and tThisFlip >= 10-frameTolerance:
            # keep track of start time/frame for later
            finish_text_2.frameNStart = frameN  # exact frame index
            finish_text_2.tStart = t  # local t and not account for scr refresh
            finish_text_2.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(finish_text_2, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'finish_text_2.started')
            # update status
            finish_text_2.status = STARTED
            finish_text_2.setAutoDraw(True)
        
        # if finish_text_2 is active this frame...
        if finish_text_2.status == STARTED:
            # update params
            pass
        
        # *finish_key* updates
        waitOnFlip = False
        
        # if finish_key is starting this frame...
        if finish_key.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            finish_key.frameNStart = frameN  # exact frame index
            finish_key.tStart = t  # local t and not account for scr refresh
            finish_key.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(finish_key, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'finish_key.started')
            # update status
            finish_key.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(finish_key.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(finish_key.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if finish_key.status == STARTED and not waitOnFlip:
            theseKeys = finish_key.getKeys(keyList=['0'], ignoreKeys=["escape"], waitRelease=False)
            _finish_key_allKeys.extend(theseKeys)
            if len(_finish_key_allKeys):
                finish_key.keys = _finish_key_allKeys[-1].name  # just the last key pressed
                finish_key.rt = _finish_key_allKeys[-1].rt
                finish_key.duration = _finish_key_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[]
            )
            # skip the frame we paused on
            continue
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            Finish.forceEnded = routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in Finish.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "Finish" ---
    for thisComponent in Finish.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for Finish
    Finish.tStop = globalClock.getTime(format='float')
    Finish.tStopRefresh = tThisFlipGlobal
    thisExp.addData('Finish.stopped', Finish.tStop)
    # Run 'End Routine' code from finish_code
    # Save final PsychoPy data to the block directory
    if 'filename' in locals() and filename:
        try:
            # Final complete save
            thisExp.saveAsWideText(filename + '_final.csv')
            print(f"Final PsychoPy data saved: {filename}_final.csv")
            
        except Exception as e:
            print(f"Error saving final data: {e}")
    
    # Stop TDT recording and switch to Idle mode
    try:
        syn.setMode(0)  # Switch to Idle mode
        print("TDT switched to Idle mode - Recording stopped")
        
        # Get final system status
        final_status = syn.getSystemStatus()
        print(f"Final TDT status: {final_status}")
        
    except Exception as e:
        print(f"Error stopping TDT recording: {e}")
    
    # Display experiment summary
    print("\n" + "="*50)
    print("EXPERIMENT SUMMARY")
    print("="*50)
    if 'tank_path' in locals():
        print(f"Data saved to: {tank_path}")
    if 'current_tank' in locals():
        print(f"TDT Tank: {current_tank}")
    if 'current_block' in locals():
        print(f"TDT Block: {current_block}")
    print(f"Participant: {expInfo['participant']}")
    print(f"Session: {expInfo['session']}")
    print(f"Date: {expInfo['date']}")
    print("="*50)
    # check responses
    if finish_key.keys in ['', [], None]:  # No response was made
        finish_key.keys = None
    thisExp.addData('finish_key.keys',finish_key.keys)
    if finish_key.keys != None:  # we had a response
        thisExp.addData('finish_key.rt', finish_key.rt)
        thisExp.addData('finish_key.duration', finish_key.duration)
    thisExp.nextEntry()
    # the Routine "Finish" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    # Run 'End Experiment' code from finish_code
    # Final cleanup and shutdown
    try:
        # Close TDT connection safely
        if 'syn' in locals():
            print("Closing TDT connection...")
            # Note: SynapseAPI doesn't have explicit close method
            # Connection will be closed when Python exits
        
        # Final message
        print("All systems shut down successfully")
        print("Thank you for using the EEG experiment framework!")
        
    except Exception as e:
        print(f"Error during final cleanup: {e}")
    
    # Close PsychoPy window and quit
    win.close()
    core.quit()
    
    # mark experiment as finished
    endExperiment(thisExp, win=win)


def saveData(thisExp):
    """
    Save data from this experiment
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    """
    filename = thisExp.dataFileName
    # these shouldn't be strictly necessary (should auto-save)
    thisExp.saveAsWideText(filename + '.csv', delim='auto')
    thisExp.saveAsPickle(filename)


def endExperiment(thisExp, win=None):
    """
    End this experiment, performing final shut down operations.
    
    This function does NOT close the window or end the Python process - use `quit` for this.
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    win : psychopy.visual.Window
        Window for this experiment.
    """
    if win is not None:
        # remove autodraw from all current components
        win.clearAutoDraw()
        # Flip one final time so any remaining win.callOnFlip() 
        # and win.timeOnFlip() tasks get executed
        win.flip()
    # return console logger level to WARNING
    logging.console.setLevel(logging.WARNING)
    # mark experiment handler as finished
    thisExp.status = FINISHED
    logging.flush()


def quit(thisExp, win=None, thisSession=None):
    """
    Fully quit, closing the window and ending the Python process.
    
    Parameters
    ==========
    win : psychopy.visual.Window
        Window to close.
    thisSession : psychopy.session.Session or None
        Handle of the Session object this experiment is being run from, if any.
    """
    thisExp.abort()  # or data files will save again on exit
    # make sure everything is closed down
    if win is not None:
        # Flip one final time so any remaining win.callOnFlip() 
        # and win.timeOnFlip() tasks get executed before quitting
        win.flip()
        win.close()
    logging.flush()
    if thisSession is not None:
        thisSession.stop()
    # terminate Python process
    core.quit()


# if running this experiment as a script...
if __name__ == '__main__':
    # call all functions in order
    expInfo = showExpInfoDlg(expInfo=expInfo)
    thisExp = setupData(expInfo=expInfo)
    logFile = setupLogging(filename=thisExp.dataFileName)
    win = setupWindow(expInfo=expInfo)
    setupDevices(expInfo=expInfo, thisExp=thisExp, win=win)
    run(
        expInfo=expInfo, 
        thisExp=thisExp, 
        win=win,
        globalClock='float'
    )
    saveData(thisExp=thisExp)
    quit(thisExp=thisExp, win=win)
