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
UID_BOOTSTRAP_QUEUE = "UID Queue"

# UID prefixes that identifies what kind of user we have
UID_PREFIX_STU = "stu_"
UID_PREFIX_TUT = "tut_"

# Various semi-official tutor titles
TUTOR_TA  = "TA"
TUTOR_SLI = "SLI"
TUTOR_TUT = "Tutor"

# TODO Message commands/interface with the app
# User enters/leaves the Mentoring Center
MSG_USER_ENTER       = ""
MSG_USER_LEAVE       = ""
# Tutor is assigned a question/finishes with a student
MSG_TUT_HELP        = ""
MSG_TUT_DONE        = ""
# Student proposes question/gets question answered
MSG_STU_QUEST       = ""
MSG_STU_ANS         = ""

# TODO Message JSON parameters
MSG_PARAM_METHOD        = "get_method"
MSG_PARAM_USER_NAME     = "user_name"
MSG_PARAM_USER_TITLE    = "user_title"
MSG_PARAM_USER_UID      = "user_uid"
