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
# RIT email extension
RIT_EMAIL_EXT = "@rit.edu"

# Various semi-official tutor titles
TUTOR_TA  = "TA"
TUTOR_SLI = "SLI"
TUTOR_TUT = "Tutor"

# TODO Message commands/interface with the app
# User enters/leaves the Mentoring Center
MSG_STU_ENTER       = "stu_enters"
MSG_TUT_ENTER       = "tut_enters"
MSG_USER_ENTER      = "user_enters"
MSG_USER_LEAVE      = "user_leaves"
# Generic "User is getting helped or giving help"
MSG_USER_HELPED     = ""
# Student proposes question/gets question answered
MSG_STU_QUEST       = ""
MSG_STU_ANS         = ""
# Tutor is assigned a question/finishes with a student
MSG_TUT_HELP        = ""
MSG_TUT_DONE        = ""
# Error messages
MSG_ERR_USER_LOGIN  = "err_user_login"

# TODO Message JSON parameters
MSG_PARAM_METHOD        = "get_method"
MSG_PARAM_USER_NAME     = "user_name"
MSG_PARAM_USER_PASSWD   = "user_passwd"
MSG_PARAM_USER_F_NAME   = "user_f_name"
MSG_PARAM_USER_L_NAME   = "user_l_name"
MSG_PARAM_USER_TITLE    = "user_title"
# identify users in messaging
MSG_PARAM_USER_UID      = "user_uid"
MSG_PARAM_STU_UID       = "student_uid"
MSG_PARAM_TUT_UID       = "tutor_uid"

# SQLite database file naming
SQL_DB_PATH       = "./"
SQL_DB_FILE       = "mmcga.db"
SQL_DB            = SQL_DB_PATH + SQL_DB_FILE
# debug version of the database for testing purposes
SQL_DB_FILE_DEBUG = "debug_test_mmcga.db"
SQL_DB_DEBUG      = SQL_DB_PATH + SQL_DB_FILE_DEBUG

# TODO Database tables
DB_USER_TBL       = "Users"

# alternative indices in the table ("secondary keys")
DB_UNAME_IDX      = "user_name_idx"

# fields for DB tables
DB_FIELD_UID      = "uid"
DB_FIELD_UNAME    = "user_name"
DB_FIELD_JSON     = "json_str"

# field types for DB tables
DB_F_TYPE_INT     = "INTEGER"
DB_F_TYPE_TXT     = "TEXT"
