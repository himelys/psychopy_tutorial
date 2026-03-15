#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reference snippets for integrating PsychoPy with TDT Synapse.

This file is intentionally a helper/reference module, not a runnable script.
It keeps the original setup notes in valid Python form so the `experiments`
folder remains importable and compile-checkable.
"""


TDT_INITIALIZATION_EXAMPLE = """
# Import TDT library and establish connection
import tdt
from datetime import datetime
import time

print("=========== Setting Configuration ===========")
try:
    syn = tdt.SynapseAPI()
    print("1. TDT Synapse connection successful")
    tdt_connected = True
except Exception as e:
    print(f"TDT Synapse connection failed: {e}")
    core.quit()
"""


TRIGGER_EXAMPLE = """
EXP_START = 9999
syn.setParameterValue('TTL2Int1', 'IntegerValue', EXP_START)
syn.setParameterValue('TTL2Int1', 'ManualTrigger', 1)
core.wait(0.01)
syn.setParameterValue('TTL2Int1', 'ManualTrigger', 0)
print(f"Experiment start trigger {EXP_START} sent")
"""


TANK_AND_BLOCK_EXAMPLE = """
if syn.getMode() != 0:
    syn.setMode(0)

syn.setCurrentUser(user)
syn.setCurrentExperiment(experiment)
current_tank = syn.getCurrentTank()
syn.createSubject(expInfo['participant'], f'datetime_{clean_datetime}', 'mouse')
syn.setCurrentSubject(expInfo['participant'])
syn.setCurrentBlock(block_name)
syn.setMode(3)
block_dir = f"{current_tank}\\\\{block_name}"
filename = f"{block_dir}\\\\psychopy_{expInfo['participant']}_{expInfo['date']}"
"""


SHUTDOWN_EXAMPLE = """
try:
    syn.setMode(0)
    print("TDT switched to Idle mode - Recording stopped")
    final_status = syn.getSystemStatus()
    print(f"Final TDT status: {final_status}")
except Exception as e:
    print(f"Error stopping TDT recording: {e}")

win.close()
core.quit()
"""


def print_reference_sections():
    """Print the saved TDT reference snippets."""
    sections = {
        "initialization": TDT_INITIALIZATION_EXAMPLE,
        "trigger": TRIGGER_EXAMPLE,
        "tank_and_block": TANK_AND_BLOCK_EXAMPLE,
        "shutdown": SHUTDOWN_EXAMPLE,
    }
    for name, text in sections.items():
        print(f"[{name}]")
        print(text.strip())
        print()


if __name__ == "__main__":
    print_reference_sections()
