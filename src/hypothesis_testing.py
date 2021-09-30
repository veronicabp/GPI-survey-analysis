import csv
import os
import numpy as np
from scipy import stats
from tabulate import tabulate
import matplotlib.pyplot as plt

treatment_description = {
	"T1": "China is an economic threat to the US",
	"T2": "China is a threat to human rights",
	"T3": "China is a military threat to the US",
	"T4": "China is not an economic threat",
	"T5": "China is not a threat to human rights",
	"T6": "China is not a military threat to the US",
	"T7": "US-China cooperation is important to fight climate change",
	"T8": "Control"
}

question_description = {
	"Q1": "Human rights abuses in China concern me.",
	"Q2": "I am confident that China will be able to\nhandle allegations of human rights abuses against them\nwithout US or international intervention.",
	"Q3": "The widely reported internment of Muslim Uyghurs\nand other ethnic minorities in China, which has been termed\na genocide by human rights groups, has led to the emergence of\na boycott of the 2022 Beijing Olympics.\nChina reported that they will punish countries that boycott\nthe Games with political sanctions and commercial retaliation,\ntherefore impacting international trade.\n\nAmerican companies should boycott the Beijing Olympics.",
	"Q4": "I believe the US should invest money and\nresources in promoting human rights in China.",
	"Q5": "China's economic growth concerns me.",
	"Q6": "U.S. sanctions on China affect both countries.\nAs a result of recent sanctions, Americans lost an estimate 0.3\npercent of real GDP, equivalent to nearly 300,000 jobs.\nThese sanctions were estimated to negatively impact China's economy\nby hundreds of billions of dollars.\n\nI believe that the benefits of placing sanctions on China outweigh the costs.",
	"Q7": "I am willing to spend more on an item\nthat was not made in China.",
	"Q8": "If forced to pick between the two, I think\nthat it is more important for the U.S. to develop a\ngood relationship with China than for the U.S.\nto prioritize staying ahead of China.",
	"Q9": "China's military and technological advances concern me.",
	"Q10": "The U.S. should invest resources into developing\ninternational cybersecurity regulations to limit\ncyber threats from foreign nations.",
	"Q11": "Currently, the U.S. has more than one hundred thousand\ntroops in the Asia-Pacific region and several military\nbases in Korea, Japan and Guam. China has expressed\nopposition to extensive U.S. military presence in the region, taking retaliatory\neconomic action against the U.S. and its allies.\n\nThe U.S. should reduce its military presence near China,\nin order to try to improve relations with China.",
	"Q12": "I believe that the U.S. should invest less resources\ninto military and defense."
}

political_knowledge_questions = [
	"Which party currently controls the House of Representatives?",
	"How long is a senator's term?",
	"Name three presidents of foreign countries.",
	"What does TPP stand for?"
]

def convert_response_to_number(response):
	if response == "Strongly Agree":
		return 2
	elif response == "Somewhat agree":
		return 1
	elif response == "Neither agree nor disagree":
		return 0
	elif response == "Somewhat disagree":
		return -1
	elif response == "Strongly disagree":
		return -2	

def convert_number_to_response(number):
	if number == 2:
		return "Strongly agree"
	elif number == 1:
		return "Somewhat agree"
	elif number == 0:
		return "Neither agree nor disagree"
	elif number == -1:
		return "Somewhat disagree"
	elif number == -2:
		return "Strongly disagree"	

class SurveyRespondent:
	def __init__(self, treatment, responses, age, income, education, ethnicity, party, political_involvement, political_knowledge):
		self.treatment = treatment
		self.responses = responses
		self.age = age
		self.income = income
		self.education = education
		self.ethnicity = ethnicity
		self.party = party
		self.political_involvement = political_involvement
		self.political_knowledge = political_knowledge

	def __str__(self):
		output = "===============================================\n"
		output += f"Treatment: {treatment_description[self.treatment]}\n\n"

		output += "Responses:\n"
		response_table = []
		for question_label in self.responses:
			response_table.append([question_description[question_label] + "\n\n\n", convert_number_to_response(responses[question_label])])
		output += tabulate(response_table, headers = ["Question", "Response"], tablefmt='fancy_grid')

		output += "\n\nDemographics:\n"
		output += tabulate([["Age Group", self.age], ["Income Group", self.income], ["Education Level", self.education], ["Ethnicity", self.ethnicity], ["Political Party", self.party], ["Political Involvement", self.political_involvement]], headers = ["Question", "Response"], tablefmt='fancy_grid')

		output += "\n\nPolitical Knowledge:\n"
		political_knowledge_table = [[political_knowledge_questions[i], self.political_knowledge[i]] for i in range(4)]
		output += tabulate(political_knowledge_table, headers = ["Question", "Response"], tablefmt='fancy_grid')

		output += "\n===============================================\n\n"
		return output

#############################################################################
# Create list of SurveyRespondent objects
#############################################################################

respondents = []
data_file = os.path.join('..','data','survey_results.csv')
with open(data_file, 'r') as f:
	reader = csv.reader(f)
	next(reader)
	next(reader)
	next(reader)

	for row in reader:

		# Remove respondents who did not finish survey
		if row[6] == "FALSE":
			continue
		 
		 # Determine treatment of individual
		if row[17] == "Yes":
		 	treatment = "T1"
		elif row[18] == "Yes":
		 	treatment = "T2"
		elif row[19] == "Yes":
		 	treatment = "T8"
		elif row[20] == "Yes":
		 	treatment = "T4"
		elif row[21] == "Yes":
		 	treatment = "T5"
		elif row[22] == "Yes":
		 	treatment = "T3"
		elif row[23] == "Yes":
		 	treatment = "T6"
		elif row[24] == "Yes":
		 	treatment = "T7"

		responses = {
		 	"Q1" : convert_response_to_number(row[25]),
		 	"Q2" : convert_response_to_number(row[26]),
		 	"Q3" : convert_response_to_number(row[27]),
		 	"Q4" : convert_response_to_number(row[28]),
		 	"Q5" : convert_response_to_number(row[29]),
		 	"Q6" : convert_response_to_number(row[30]),
		 	"Q7" : convert_response_to_number(row[31]),
		 	"Q8" : convert_response_to_number(row[32]),
		 	"Q9" : convert_response_to_number(row[33]),
		 	"Q10" : convert_response_to_number(row[34]),
		 	"Q11" : convert_response_to_number(row[35]),
		 	"Q12" : convert_response_to_number(row[36])
		 }

		age = row[37]
		income = row[38]
		education = row[39]
		ethnicity = row[40]
		party = row[41]
		political_involvement = row[42]
		political_knowledge = [row[43], row[44], row[45], row[46]]

		respondents.append(SurveyRespondent(treatment, responses, age, income, education, ethnicity, party, political_involvement, political_knowledge))

# for respondent in respondents:
# 	print(respondent)

#############################################################################
# Store data as numpy arrays
#############################################################################

results = {}
for treatment in treatment_description:
	lst = []
	for respondent in respondents:
		if respondent.treatment == treatment:
			lst.append([respondent.responses[question] for question in respondent.responses])

	arr = np.transpose(np.array(lst))
	results[treatment] = arr

#############################################################################
# Hypothesis Testing
#############################################################################

control_treatment = "T8"

for question_index, question in enumerate(question_description):
	print("="*100)
	print(f"{question}: {question_description[question]}")
	print("="*100)
	print("\n")
	for t in results:
		if treatment_description[t] != "Control":
			stat, pval = stats.ttest_ind(results[t][question_index], results[control_treatment][question_index])

			if pval < .1:

				print("-"*100)
				print("Two-sided t-test:")
				print(f"{t}: {treatment_description[t]} -- Mean: {round(np.mean(results[t][question_index]),2)}")
				print(f"{control_treatment}: {treatment_description[control_treatment]} -- Mean: {round(np.mean(results[control_treatment][question_index]),2)}")
				print(f'P-Val: {round(pval,2)}')
	print("\n\n\n")

#############################################################################
# Graphing
#############################################################################

for question_index, question in enumerate(question_description):

	fig, ax = plt.subplots()

	labels = [treatment_label for treatment_label in treatment_description]

	means = []
	for treatment in results:
		means.append(np.mean(results[treatment][question_index]))

	error = []
	for treatment in results:
		error.append(np.std(results[treatment][question_index]))

	x_pos = np.arange(len(treatment_description))

	ax.bar(x_pos, means, yerr=error, align='center', alpha=0.5, ecolor='black', capsize=10)
	ax.set_ylabel('Mean response')
	ax.set_xticks(x_pos)
	ax.set_xticklabels(labels)
	ax.set_title(f'Responses to {question} by treatment')
	ax.yaxis.grid(True)

	plt.tight_layout()
	plt.savefig(os.path.join('..','graphics',f'{question}.png'))
	# plt.show()


