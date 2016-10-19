#!/bin/bash
#
# run_tests.sh
#
# Schuyler Martin <sam8050@rit.edu>
#
# Simple shell script that runs one or all of the class tests.
# Providing no arguments or 0 will run through all tests. Providing a test
# number will run a specific test
#

USAGE="Usage: ./run_tests.sh [test_#]"

# usage checks
if [ "$#" -gt 1 ]; then
    echo "${USAGE}"
    exit 1
fi

test_id="$1"
# by default, run all tests
if [ "${test_id}" = "" ]; then
    test_id=0
fi

echo "###################### START TESTS ######################"
# conditionally run tests
if [ "${test_id}" -eq 0 ] || [ "${test_id}" -eq 1 ]; then
    echo "###################### TEST 1: Student Queue ######################"
    python3 -m users.queue_stu
fi

if [ "${test_id}" -eq 0 ] || [ "${test_id}" -eq 2 ]; then
    echo "###################### TEST 2: Tutor Queue ######################"
    python3 -m users.queue_tut
fi

if [ "${test_id}" -eq 0 ] || [ "${test_id}" -eq 3 ]; then
    echo "###################### TEST 3: Bunny Class ######################"
    python3 -m utils.bunny
fi
echo "######################  END TESTS  ######################"
