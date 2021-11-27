import os
from tabulate import tabulate
import numpy as np
import pickle
from respondents_treatments import SurveyRespondent

input_file = os.path.join("..", "data", "respondent_objects")
with open(input_file, "rb") as f:
    respondents = pickle.load(f)

# Convert data into array
headers = ["id"] + [f"T{i+1}" for i in range(8)] + ["age", "income", "education", "ethnicity", "party", "involvement", "knowledge"] + [f"Q{i+1}" for i in range(12)]
data = []

for i, respondent in enumerate(respondents):

	treatment = [0 for _ in range(8)]
	treatment[int(respondent.treatment[-1])-1] = 1

	responses = []
	for question in respondent.responses:
		responses.append(respondent.responses[question])

	if respondent.political_involvement == "Not involved at all":
		involvement = -2  
	if respondent.political_involvement == "Not very involved":
		involvement = -1
	if respondent.political_involvement == "Neutral":
		involvement = 0
	if respondent.political_involvement == "Moderately involved":
		involvement = 1
	if respondent.political_involvement == "Highly involved":
		involvement = 2

	row = [i] + treatment + [respondent.age, respondent.income, respondent.education, respondent.ethnicity, respondent.party, involvement, respondent.political_knowledge()] + responses
	data.append(row)

data = np.array(data)

print(tabulate(data, headers=headers))