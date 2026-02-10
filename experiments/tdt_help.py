# TDT initialization

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


# Trigger example

 # Record initial trigger to mark experiment start
        EXP_START = 9999
        syn.setParameterValue('TTL2Int1', 'IntegerValue', EXP_START)
        syn.setParameterValue('TTL2Int1', 'ManualTrigger', 1)
        core.wait(0.01)
        syn.setParameterValue('TTL2Int1', 'ManualTrigger', 0)
        print("=============================================") 
        print(f"Experiment start trigger {EXP_START} sent")
        print("=============================================") 
        
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

# Stop TDT recording and switch to Idle mode
    try:
        syn.setMode(0)  # Switch to Idle mode
        print("TDT switched to Idle mode - Recording stopped")
        
        # Get final system status
        final_status = syn.getSystemStatus()
        print(f"Final TDT status: {final_status}")
        
    except Exception as e:
        print(f"Error stopping TDT recording: {e}")

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


