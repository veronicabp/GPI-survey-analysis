import os
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from respondents_treatments import question_description, results, treatment_description
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
            stat, pval = stats.ttest_ind(
                results[t][question_index], results[control_treatment][question_index])

            if pval < .1:

                print("-"*100)
                print("Two-sided t-test:")
                print(
                    f"{t}: {treatment_description[t]} -- Mean: {round(np.mean(results[t][question_index]),2)}")
                print(
                    f"{control_treatment}: {treatment_description[control_treatment]} -- Mean: {round(np.mean(results[control_treatment][question_index]),2)}")
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

    ax.bar(x_pos, means, yerr=error, align='center',
           alpha=0.5, ecolor='black', capsize=10)
    ax.set_ylabel('Mean response')
    ax.set_xticks(x_pos)
    ax.set_xticklabels(labels)
    ax.set_title(f'Responses to {question} by treatment')
    ax.yaxis.grid(True)

    plt.tight_layout()
    plt.savefig(os.path.join('..', 'graphics', f'{question}.png'))
    # plt.show()
