import os
import sys
import re
import csv
import json

f = open("eng_data.csv", "rU")

wf = open("eng_formatted_grouped.json", "w")

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
#studentDict = dict()
majorNodeDict = dict()
classDict = dict()
majorDict = dict()

majorDict["Music"] = 0
majorNodeDict["Music"] = {
	"count" : 0
}
musicMajors = ["Violin", "Piano", "Oboe", "Trombone", "Commercial Music Production", "Tuba", "Bassoon", "Violoncello", "Viola", "Clarinet", "Percussion", "Music Education and Performance", "Double Bass", "French Horn", "Voice", "Jazz Studies"]
others = "Pre-Special Education,Classics,French,Judaic Studies,Classical Guitar,Pre-Secondary Education - AX,Business Management Technology,Pre-Respiratory Care,Geology - BA,Pre-Secondary Education - AS,Horticulture,Health Information Systems,German Studies,Geography - BA,Eng & Applied Science Entrance,Geography - BS,Early Childhood Education - B5,Pre-Health Professions,Pre-Health Education,Didactic Program in Dietetics,Psychology,Archaeology - BA,Pre-Pharmacy,Neuroscience - BX,Music Education & Performance,Pre-Engineering,Pre-Middle Childhood Education,Physics - BA,Aviation Technology,Paralegal Studies,Criminal Justice Technology,Africana Studies,Respiratory Therapy,Film & Media Studies,Pre-Nursing,Pre-Early Childhood Education,Insurance and Risk Management,International Exchange Student,Food and Nutrition,Pre-Allied Health,Classical Civilization,Media Criticism & Journalism,Business Analytics,Pre-Comm Sci and Disorders,Digital Media Collaboration,Accounting Option,Physical Therapist Assistant,Pre-Organizational Leadership,Interdisciplinary - Neurosci"
otherlist = others.split(",")
print otherlist
def checkMajor(name):
	returnstr = name
	for m in musicMajors:
		if name == m:
			returnstr = "Music"
	for m in otherlist:
		if name == m:
			returnstr = "MISC"
	return returnstr
for row  in d:
	if row[1] in classDict:
		classDict[row[1]]["count"] += 1

	else:
		classDict[row[1]] = {
		"count" : 1,
		"code" : row[3]
		}
	if checkMajor(row[10]) in majorNodeDict:
		#print checkMajor(row[10])
		majorNodeDict[checkMajor(row[10])]["count"] +=1

	else:
		majorNodeDict[checkMajor(row[10])] = {
		"count" : 1
		#"planA" : row[10],
		#"planB" : row[11]

		}
	if checkMajor(row[10]) in majorDict:
		majorDict[checkMajor(row[10])] += 1
	else:
		majorDict[checkMajor(row[10])] = 1
	found = False
	for link in force_data['links']:
		if link['source'] == checkMajor(row[10]) and link['target'] == row[1]:
			link['value'] = link['value'] + 1
			found = True
	if not found:
		force_data["links"].append({
				"source" : checkMajor(row[10]),
				"target" : row[1],
				"value" : 1
				})



for key in classDict:
	force_data["nodes"].append({
		"id" : key,
		"student" : -1,
		"info" : classDict[key]
		})
for key in majorNodeDict:
	force_data["nodes"].append({
		"id" : key,
		"student" : 1,
		"info" : majorNodeDict[key]
		})
for key in majorDict:
	force_data["plan"].append({
		"name" : key,
		"count" : majorDict[key]
		})




json.dump(force_data, wf, indent=4)

