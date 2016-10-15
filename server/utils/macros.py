##
## File:    macros.py
##
## Author:  Schuyler Martin <sam8050@rit.edu>
##
## Description: Python file that contains C-like macros for the project
##

#### GLOBALS    ####

# Enables extended debug printing
DEBUG_MACRO = True

# Host name of the server
SERVER_HOST = "localhost"
# Name of the default queue
SERVER_QUEUE = "Default Queue"

# Various semi-official tutor titles
TUTOR_TA  = "TA"
TUTOR_SLI = "SLI"
TUTOR_TUT = "Tutor"

# TODO Message commands/interface with the app
# Tutor enters/leaves the Mentoring Center
MSG_TUT_ENTER       = ""
MSG_TUT_LEAVE       = ""
# Tutor is assigned a question/finishes with a student
MSG_STU_HELP        = ""
MSG_STU_DONE        = ""
# Student proposes question/gets question answered
MSG_STU_QUEST       = ""
MSG_STU_ANS         = ""
