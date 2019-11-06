#! /usr/bin/python2.7

# check_boinc_pid script to check BOINC project status and provide the output to Nagios
# This only returns critical if the project is enabled and the processes are not running
# This script has been written by Andy Bowery (Oxford University, 2019)

import os,sys,argparse,subprocess
from subprocess import Popen, PIPE
from xml.dom import minidom

def is_pid_running(pid):
  try:
    os.kill(pid,0)
    return True
  except OSError:
    return False

if __name__ == "__main__":

  project_dir = PATH_TO_BOINC_PROJECT_DIRECTORY
  project_pid_dir = PATH_TO_BOINC_PROJECT_PID_DIRECTORY

  # Parse the run_state xml file
  is_enabled = 0
  xmldoc = minidom.parse(project_dir+'run_state_SERVER_NAME.xml')
  state_file = xmldoc.getElementsByTagName('boinc')
  for tag in state_file:
    is_enabled = str(tag.getElementsByTagName('enabled')[0].childNodes[0].nodeValue)

  if is_enabled==1:
    with open(project_pid_dir+'feeder.pid','r') as feeder_pid_file:
      for value in feeder_pid_file:
        feeder_pid = int(value)
        #print "feeder_pid: "+str(feeder_pid)
        if not is_pid_running(feeder_pid):
          print "CRITICAL - feeder not running"
          sys.exit(2)

    with open(project_pid_dir+'transitioner.pid','r') as transitioner_pid_file:
      for value in transitioner_pid_file:
        transitioner_pid = int(value)
        #print "transitioner_pid: "+str(transitioner_pid)
        if not is_pid_running(transitioner_pid):
          print "CRITICAL - transitioner not running"
          sys.exit(2)

    with open(project_pid_dir+'trickle.pid','r') as trickle_pid_file:
      for value in trickle_pid_file:
        cpdn_trickle_pid = int(value)
        #print "trickle_pid: "+str(trickle_pid)
        if not is_pid_running(trickle_pid):
          print "CRITICAL - trickle not running"
          sys.exit(2)

  print "OK - either all process running or project disabled"
  sys.exit(0)

  # Note: for a warning the message would be:
  #print "WARNING - warning message"
