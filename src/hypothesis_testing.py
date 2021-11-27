import os
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import pickle
from respondents_treatments import question_description, treatment_description, SurveyRespondent
#############################################################################
# Hypothesis Testing
#############################################################################

def ptest(data):

    control_treatment = "T8"

    for question_index, question in enumerate(question_description):
        print("="*100)
        print(f"{question}: {question_description[question]}")
        print("="*100)
        print("\n")
        for t in data:
            if treatment_description[t] != "Control" and len(data[t])>0 and len(data[control_treatment])>0:
                stat, pval = stats.ttest_ind(
                    data[t][question_index], data[control_treatment][question_index])
                if pval < 0.1:

                    print("-"*100)
                    print("Two-sided t-test:")
                    print(
                        f"{t}: {treatment_description[t]} -- Mean: {round(np.mean(data[t][question_index]),2)}")
                    print(
                        f"{control_treatment}: {treatment_description[control_treatment]} -- Mean: {round(np.mean(data[control_treatment][question_index]),2)}")
                    print(f'P-Val: {round(pval,2)}')
        print("\n\n\n")

#############################################################################
# Graphing
#############################################################################

def graph_bar(data, output_path):
    for question_index, question in enumerate(question_description):

        if len(data["T1"])==0:
            continue

        fig, ax = plt.subplots()

        labels = [treatment_label for treatment_label in treatment_description]

        means = []
        for treatment in data:
            means.append(np.mean(data[treatment][question_index]))

        error = []
        for treatment in data:
            error.append(np.std(data[treatment][question_index]))

        x_pos = np.arange(len(treatment_description))

        ax.bar(x_pos, means, yerr=error, align='center',
               alpha=0.5, ecolor='black', capsize=10)
        ax.set_ylabel('Mean response')
        ax.set_xticks(x_pos)
        ax.set_xticklabels(labels)
        ax.set_title(f'Responses to {question} by treatment')
        ax.yaxis.grid(True)

        plt.tight_layout()
        plt.savefig(os.path.join(output_path, f'{question}.png'))
        # plt.show()

#############################################################################
# Run Tests
#############################################################################

if __name__ == "__main__":


    input_file = os.path.join("..", "data", "respondent_objects")
    with open(input_file, "rb") as f:
        respondents = pickle.load(f)


    input_file = os.path.join("..", "data", "data")
    with open(input_file, "rb") as f:
        data = pickle.load(f)

    data = {}
    for treatment in treatment_description:
        row = []
        for respondent in respondents:
            if respondent.treatment == treatment:
                row.append([respondent.responses[question] for question in respondent.responses])
        row = np.transpose(np.array(row))
        data[treatment] = row

    # print(data)
    ptest(data) 

