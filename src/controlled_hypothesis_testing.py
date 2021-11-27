from respondents_treatments import respondents, treatment_description, question_description
from hypothesis_testing import ptest, graph_bar

import numpy as np
import os
import matplotlib.pyplot as plt

def graph_multiple_bar(data, output_path):
	for question_index, question in enumerate(question_description):

		categories = list(data.keys())
		colors = ["r","b","g","c","m","orange","pink"]

		first_key = categories[0]
		if len(data[first_key]["T1"])==0:
			continue

		fig, ax = plt.subplots()

		width = 0.25
		current_pos = 0
		for i, category in enumerate(data):
			labels = [treatment_label for treatment_label in treatment_description]

			means = []
			for treatment in data[category]:
				means.append(np.mean(data[category][treatment][question_index]))

			error = []
			for treatment in data[category]:
				error.append(np.std(data[category][treatment][question_index]))

			x_pos = np.arange(len(treatment_description))

			# ax.bar(x_pos + current_pos, means, width=width, yerr=error, align='center',
			# 	   alpha=0.5, ecolor='black', capsize=10, label = category, color = colors[i])
			ax.bar(x_pos + current_pos, means, width=width, alpha=0.5, label = category, color = colors[i])

			current_pos += width

		ax.set_ylabel('Mean response')
		ax.set_xticks(x_pos + width/2)
		ax.set_xticklabels(labels)
		ax.set_title(f'Responses to {question} by treatment')
		ax.yaxis.grid(True)
		ax.legend()

		plt.tight_layout()
		plt.savefig(os.path.join(output_path, f'{question}.png'))
		# plt.show()

# Control for political party

parties = ["Republican", "Democrat"]
party_data = dict()

for party in parties:
	print(f"Party: {party}")
	num = 0
	results = {}
	for treatment in treatment_description:
		lst = []
		for respondent in respondents:
			if respondent.treatment == treatment and respondent.party == party:
				lst.append([respondent.responses[question] for question in respondent.responses])

		arr = np.transpose(np.array(lst))
		results[treatment] = arr
		num += len(lst)
	ptest(results) 
	# graph_bar(results, os.path.join('..','graphics','controlled_tests','party', party))

	party_data[party] = results
graph_multiple_bar(party_data, os.path.join('..','graphics','controlled_tests','party'))

# # Control for age

# ages = ["Under 18", "18 - 24", "25 - 34", "35 - 44", "45 - 54", "55 - 64", "65 - 74", "75 - 84", "85 or older"]
# age_dict = {
# 	"young": ["Under 18", "18 - 24", "25 - 34"],
# 	"middle_age": [ "35 - 44", "45 - 54", "55 - 64"],
# 	"old": [ "65 - 74", "75 - 84", "85 or older"]
# }

# for age in age_dict:
# 	print(f"Age: {age}")
# 	results = {}
# 	for treatment in treatment_description:
# 		lst = []
# 		for respondent in respondents:
# 			if respondent.treatment == treatment and respondent.age in age_dict[age]:
# 				lst.append([respondent.responses[question] for question in respondent.responses])

# 		arr = np.transpose(np.array(lst))
# 		results[treatment] = arr

# 	ptest(results)

# 	try:	
# 		os.mkdir( os.path.join('..','graphics','controlled_tests','age', age))
# 	except:
# 		print("folder already exists")

# 	try:
# 		graph_bar(results, os.path.join('..','graphics','controlled_tests','age', age))
# 	except:
# 		print()

# # Control for income

# # Control for political involvement

# # involvement = ["Highly involved", "Moderately involved", "Neutral", "Not very involved", "Not involved at all"]

# for inv in involvement:
# 	print(f"Political Involvement: {inv}")
# 	results = {}
# 	for treatment in treatment_description:
# 		lst = []
# 		for respondent in respondents:
# 			if respondent.treatment == treatment and respondent.political_involvement == inv:
# 				lst.append([respondent.responses[question] for question in respondent.responses])

# 		arr = np.transpose(np.array(lst))
# 		results[treatment] = arr

# 	ptest(results)

# 	path = os.path.join('..','graphics','controlled_tests','involvement', inv)

# 	try:	
# 		os.mkdir(path)
# 	except:
# 		print("folder already exists")

# 	try:
# 		graph_bar(results, path)
# 	except:
# 		print()

# # Control for education

# education = ["Less than high school", "High school graduate", "Some college", "2 year degree", "4 year degree", "Professional degree", "Doctorate"]

# for edu in education:
# 	print(f"Education level: {edu}")
# 	results = {}
# 	for treatment in treatment_description:
# 		lst = []
# 		for respondent in respondents:
# 			if respondent.treatment == treatment and respondent.education == edu:
# 				lst.append([respondent.responses[question] for question in respondent.responses])

# 		arr = np.transpose(np.array(lst))
# 		results[treatment] = arr

# 	ptest(results)

# 	path = os.path.join('..','graphics','controlled_tests','education', edu)

# 	try:	
# 		os.mkdir(path)
# 	except:
# 		print("folder already exists")

# 	try:
# 		graph_bar(results, path)
# 	except:
# 		print()

# # Control for race

# races = ["White", "Black or African American", "American Indian or Alaska Native", "Asian", "Native Hawaiian or Pacific Islander", "Other"]

# for race in races:
# 	print(f"Race: {race}")
# 	results = {}
# 	for treatment in treatment_description:
# 		lst = []
# 		for respondent in respondents:
# 			if respondent.treatment == treatment and respondent.ethnicity == race:
# 				lst.append([respondent.responses[question] for question in respondent.responses])

# 		arr = np.transpose(np.array(lst))
# 		results[treatment] = arr

# 	ptest(results)

# 	path = os.path.join('..','graphics','controlled_tests','race', race)

# 	try:	
# 		os.mkdir(path)
# 	except:
# 		print("folder already exists")

# 	try:
# 		graph_bar(results, path)
# 	except:
# 		print()

# # Control for political knowledge