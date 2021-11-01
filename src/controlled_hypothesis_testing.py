from respondents_treatments import respondents, treatment_description
from hypothesis_testing import ptest, graph_bar

import numpy as np
import os

# Control for political party

parties = ["Republican", "Democrat", "Independent"]

for party in parties:
	print(f"Party: {party}")
	results = {}
	for treatment in treatment_description:
		lst = []
		for respondent in respondents:
			if respondent.treatment == treatment and respondent.party == party:
				lst.append([respondent.responses[question] for question in respondent.responses])

		arr = np.transpose(np.array(lst))
		results[treatment] = arr
	ptest(results)
	graph_bar(results, os.path.join('..','graphics','controlled_tests','party', party))

# Control for age

ages = ["Under 18", "18 - 24", "25 - 34", "35 - 44", "45 - 54", "55 - 64", "65 - 74", "75 - 84", "85 or older"]
age_dict = {
	"young": ["Under 18", "18 - 24", "25 - 34"],
	"middle_age": [ "35 - 44", "45 - 54", "55 - 64"],
	"old": [ "65 - 74", "75 - 84", "85 or older"]
}

for age in age_dict:
	print(f"Age: {age}")
	results = {}
	for treatment in treatment_description:
		lst = []
		for respondent in respondents:
			if respondent.treatment == treatment and respondent.age in age_dict[age]:
				lst.append([respondent.responses[question] for question in respondent.responses])

		arr = np.transpose(np.array(lst))
		results[treatment] = arr

	ptest(results)

	try:	
		os.mkdir( os.path.join('..','graphics','controlled_tests','age', age))
	except:
		print("folder already exists")

	try:
		graph_bar(results, os.path.join('..','graphics','controlled_tests','age', age))
	except:
		print()

# Control for income

# Control for political involvement

# involvement = ["Highly involved", "Moderately involved", "Neutral", "Not very involved", "Not involved at all"]

for inv in involvement:
	print(f"Political Involvement: {inv}")
	results = {}
	for treatment in treatment_description:
		lst = []
		for respondent in respondents:
			if respondent.treatment == treatment and respondent.political_involvement == inv:
				lst.append([respondent.responses[question] for question in respondent.responses])

		arr = np.transpose(np.array(lst))
		results[treatment] = arr

	ptest(results)

	path = os.path.join('..','graphics','controlled_tests','involvement', inv)

	try:	
		os.mkdir(path)
	except:
		print("folder already exists")

	try:
		graph_bar(results, path)
	except:
		print()

# Control for education

education = ["Less than high school", "High school graduate", "Some college", "2 year degree", "4 year degree", "Professional degree", "Doctorate"]

for edu in education:
	print(f"Education level: {edu}")
	results = {}
	for treatment in treatment_description:
		lst = []
		for respondent in respondents:
			if respondent.treatment == treatment and respondent.education == edu:
				lst.append([respondent.responses[question] for question in respondent.responses])

		arr = np.transpose(np.array(lst))
		results[treatment] = arr

	ptest(results)

	path = os.path.join('..','graphics','controlled_tests','education', edu)

	try:	
		os.mkdir(path)
	except:
		print("folder already exists")

	try:
		graph_bar(results, path)
	except:
		print()

# Control for race

races = ["White", "Black or African American", "American Indian or Alaska Native", "Asian", "Native Hawaiian or Pacific Islander", "Other"]

for race in races:
	print(f"Race: {race}")
	results = {}
	for treatment in treatment_description:
		lst = []
		for respondent in respondents:
			if respondent.treatment == treatment and respondent.ethnicity == race:
				lst.append([respondent.responses[question] for question in respondent.responses])

		arr = np.transpose(np.array(lst))
		results[treatment] = arr

	ptest(results)

	path = os.path.join('..','graphics','controlled_tests','race', race)

	try:	
		os.mkdir(path)
	except:
		print("folder already exists")

	try:
		graph_bar(results, path)
	except:
		print()

# Control for political knowledge