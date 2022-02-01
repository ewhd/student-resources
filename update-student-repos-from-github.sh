#!/bin/bash

# Script Name:  update-student-repos-from-github.sh
# Author Name:  Ethan
# Last revised: 1/31/2022
# Purpose:      Pull the main branch from all student repos I have organized in the current directory


# https://stackoverflow.com/questions/1443210/updating-a-local-repository-with-changes-from-a-github-repository
# https://linuxize.com/post/bash-printf-command/
# 

# I want to automate the running of `git pull origin main` in each local student repo.
# I've organized student repos as follows:
# .../[course-name]/[StudentName]/[arbitrary-repo-name]
# Running this script in the course folder should run `git pull origin main` in each student's arbitrarily named repo.

# This line creates a var to store our output in, and starts it with a new line for aesthetics
printf -v messagevar "\n"

# This bit silently loops over all the subfolders of all the folders in the current directory.
# Within each loop tries to run `git pull origin main`.
# If it succeeds/fails, it adds a message to our messagevar, then continues 
for d in */*/ ; do
    if (cd $d;(git pull origin main))
    then
        printf -v messagevar "${messagevar}%-40s Updated\n" $d
        continue
    else
        printf -v messagevar "${messagevar}%-40s Failed to update\n" $d
        continue
    fi &> /dev/null
    done

# Prints the accumulated contents of our messagevar
printf "$messagevar\n"
