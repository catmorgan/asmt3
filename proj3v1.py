#--------------------------------------------------------------------
#
# BIOL / CMPU 353
# Spring 2014
# 3/25/2014S
#
# Algorithm by: Jodi Schwarz and Marc Smith
# Written by: Catherine Morgan (and Yefri Baez)
#
# Assignment 3 
#
# Description: Extract matches from results of BLAST search 
#              that begin with ATG.
#
#--------------------------------------------------------------------

import re

#----------------------------------------------------------------
# FSM: Finite State Machine (has states and transitions)
# - states: each state represents the line being searched for in 
#           the BLAST search results file. 
# - transitions: describe how the FSM changes from one state to 
#                another.
#
# There will be four possible states in our FSM, upon completion
# of this project: S1-S4 
# Note: this initial version uses only one state
#
# Here is what each state represents: 
#
# S1: looking for "Query="
# S2: looking for "(nnn letters)"
# S3: looking for "Query:" or "No hits found"
# S4: looking for "Sbjct: nnn"
#
# Here is a table representation of the state transition function 
# with initial state S1. (this is equivalent to drawing a state
# transition diagram, which is hard to do in a text file)
#
# From-State  To-State  if Line match =
# ----------  --------  ---------------
#     S1         S2     "Query="
#     S2         S3     "(nnn letters)"
#     S3         S1     "No hits found"
#     S3         S4     "Query: 
#     S4         S1     "Sbjct:"
#----------------------------------------------------------------

# initialize states S1 - S4, and start state
S1 = 1
S2 = 2
S3 = 3
S4 = 4
State = S1
count = 0

# Print header line for three (3) tab-separated columns
print "EST\tEST Length\tQuery Start Position"

FileName = "/home/joschwarz/public/AipTransc_v_SwissProt.blastx"
BlastFile = open(FileName, 'r')

for Line in BlastFile:
    # if we're looking for the new Query= line...
    if State == S1:
        match = re.search(r'^Query=\s+([\w\.]+)', Line)
        #if there is a match
        if match:
            #get the locus name
            CurrentEST = match.group(1)
            #move to state 2
            State = S2  
    elif State == S2:
        #save the num of letters for length of query
        EST = re.search(r'\s*(\w*)\s+letters', Line)
        #if there is a match
        if EST:
            #set the length
            ESTLength = EST.group(1)
            #move to state 3
            State = S3
    elif State == S3:
        #if no hits were found 
        match = re.search(r'\s*\.*\s+No\s+hits\s+found\s+\.*\s*', Line)
        if match:
            #move to state 1 
            State = S1
        #else you come across a "query:" (so hits)
        else:
            #capture query number and first letter 
            query = re.search(r'^Query:\s+(\w*)\s+(\w)', Line)
            if query:
                #set query number
                queryNum = query.group(1)
                #set the first letter
                firstLetter = query.group(2)
                #move to state 4
                State = S4
    elif State == S4:
        #find the subject line and save the subject num and first letter
        subject = re.search(r'^Sbjct:\s+(\w*)\s+(\w)', Line)
        #if subject line found
        if subject:
            #set subject num
            subjectNum = subject.group(1)
            #set first letter of subject line
            subjectLetter = subject.group(2)
            #if first letter and sbjct letter is M and sbject number is 1
            if firstLetter == 'M' and subjectLetter == 'M' and subjectNum == '1':
                #print the first 20 results
                if count < 20:
                    print CurrentEST,"\t", ESTLength,"\t", queryNum
                #add one to hit count
                count = count + 1
            #move to state 1
            State = S1 
    else:
        print "===> Error processing BLAST output: this line shouldn't print"

#prints total number of hits
print "Hits: ", count

BlastFile.close()
