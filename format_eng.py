import json
import os
import sys
import re
import csv

f = open("eng_data.csv", "rU")

wf = open("eng_formatted.json", "w")

force_data = {"nodes": [],
			"links": [],
			"plan" : []
			}
"""['Term Code', 'Course', 'Subject Code', 'Catalog Number', 'Class Section Code',
 'First Name', 'Last Name', 'UC ID', 'Username', 'Campus eMail', 'Academic Plan',
  'Primary Academic Subplan']"""

test = dict()
d = csv.reader(f)
d.next()
count = 0
studentDict = dict()
classDict = dict()
majorDict = dict()
for row  in d:
	if row[1] in classDict:
		classDict[row[1]]["count"] += 1

	else:
		classDict[row[1]] = {
		"count" : 1,
		"code" : row[3]
		}
	if row[8] in studentDict:
		studentDict[row[8]]["count"] +=1

	else:
		studentDict[row[8]] = {
		"count" : 1,
		"planA" : row[10],
		"planB" : row[11]

		}
	if row[10] in majorDict:
		majorDict[row[10]] += 1
	else:
		majorDict[row[10]] = 1
	force_data["links"].append({
			"source" : row[8],
			"target" : row[1],
			"value" : 1
			})


print classDict
for key in classDict:
	force_data["nodes"].append({
		"id" : key,
		"student" : -1,
		"info" : classDict[key]
		})
for key in studentDict:
	force_data["nodes"].append({
		"id" : key,
		"student" : 1,
		"info" : studentDict[key]
		})
for key in majorDict:
	force_data["plan"].append({
		"name" : key,
		"count" : majorDict[key]
		})



print len(force_data["nodes"])
json.dump(force_data, wf, indent=4)

