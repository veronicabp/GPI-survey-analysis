# Import data set 
data <- read_csv("FALL 2021/GPI Initiative /survey_data.csv")

#install.packages("dplyr") 

#remove the first 25 and last 4 columns and first 2 rows
data = data[-1,]
data = data[-1,]
for (i in 1:17){ data = dplyr::select(data, -1)}
for (i in 1:4){ data = dplyr::select(data, -ncol(data))}

#make data ordinal
data$Q10_1 = factor(data$Q10_1, levels = c("Strongly disagree", "Somewhat disagree", "Neither agree nor disagree", "Somewhat agree", "Strongly Agree"), ordered = TRUE)
data$Q10_2 = factor(data$Q10_2, levels = c("Strongly disagree", "Somewhat disagree", "Neither agree nor disagree", "Somewhat agree", "Strongly Agree"), ordered = TRUE)
data$Q10_3 = factor(data$Q10_3, levels = c("Strongly disagree", "Somewhat disagree", "Neither agree nor disagree", "Somewhat agree", "Strongly Agree"), ordered = TRUE)
data$Q10_4 = factor(data$Q10_4, levels = c("Strongly disagree", "Somewhat disagree", "Neither agree nor disagree", "Somewhat agree", "Strongly Agree"), ordered = TRUE)
data$Q26_1 = factor(data$Q26_1, levels = c("Strongly disagree", "Somewhat disagree", "Neither agree nor disagree", "Somewhat agree", "Strongly Agree"), ordered = TRUE)
data$Q26_2 = factor(data$Q26_2, levels = c("Strongly disagree", "Somewhat disagree", "Neither agree nor disagree", "Somewhat agree", "Strongly Agree"), ordered = TRUE)
data$Q26_3 = factor(data$Q26_3, levels = c("Strongly disagree", "Somewhat disagree", "Neither agree nor disagree", "Somewhat agree", "Strongly Agree"), ordered = TRUE)
data$Q26_4 = factor(data$Q26_4, levels = c("Strongly disagree", "Somewhat disagree", "Neither agree nor disagree", "Somewhat agree", "Strongly Agree"), ordered = TRUE)
data$Q27_1 = factor(data$Q27_1, levels = c("Strongly disagree", "Somewhat disagree", "Neither agree nor disagree", "Somewhat agree", "Strongly Agree"), ordered = TRUE)
data$Q27_2 = factor(data$Q27_2, levels = c("Strongly disagree", "Somewhat disagree", "Neither agree nor disagree", "Somewhat agree", "Strongly Agree"), ordered = TRUE)
data$Q27_3 = factor(data$Q27_3, levels = c("Strongly disagree", "Somewhat disagree", "Neither agree nor disagree", "Somewhat agree", "Strongly Agree"), ordered = TRUE)
data$Q27_4 = factor(data$Q27_4, levels = c("Strongly disagree", "Somewhat disagree", "Neither agree nor disagree", "Somewhat agree", "Strongly Agree"), ordered = TRUE)

#rename data 
names(data)[names(data) == "Q10_1"] <- "Humanitarian_Q1"
names(data)[names(data) == "Q10_2"] <- "Humanitarian_Q2"
names(data)[names(data) == "Q10_3"] <- "Humanitarian_Q3"
names(data)[names(data) == "Q10_4"] <- "Humanitarian_Q4"
names(data)[names(data) == "Q26_1"] <- "Economy_Q1"
names(data)[names(data) == "Q26_2"] <- "Economy_Q2"
names(data)[names(data) == "Q26_3"] <- "IR_Q1"
names(data)[names(data) == "Q26_4"] <- "IR_Q2"
names(data)[names(data) == "Q27_1"] <- "IR_Q3"
names(data)[names(data) == "Q27_2"] <- "Military_Q1"
names(data)[names(data) == "Q27_3"] <- "Military_Q2"
names(data)[names(data) == "Q27_4"] <- "Military_Q3"
names(data)[names(data) == "Q2"] <- "Age"
names(data)[names(data) == "Q3"] <- "Income"
names(data)[names(data) == "Q4"] <- "Education"
names(data)[names(data) == "Q5"] <- "Ethnicity"
names(data)[names(data) == "Q6"] <- "Political_Party"
names(data)[names(data) == "Q15"] <- "Political_Involvement"
# names(data)[names(data) == "Q7"] <- "Treatment_1"
# names(data)[names(data) == "Q28"] <- "Treatment_2"
# names(data)[names(data) == "Q12"] <- "Treament_3"
# names(data)[names(data) == "Q13"] <- "Treatment_4"
# names(data)[names(data) == "Q9"] <- "Treatment_5"
# names(data)[names(data) == "Q14"] <- "Treatment_6"
# names(data)[names(data) == "Q29"] <- "Treatment 7"


# remove row with participant over 75 and less than high school because there is only one 
data = data[data$Age != "75 - 84", ]
data = data[data$Education != "Less than high school", ]


#Print summary statistics 
summary(data)

#Print table with count, questions of choice 
table(data$Political_Party, data$Humanitarian_Q1)

#Split into train and test 
samplesize = .7*nrow(data)
set.seed(100)
index = sample(seq_len(nrow(data)), size = samplesize)
train = data[index,]
test = data[-index,]

#library(dplyr)
# library(MASS) 
model <- polr(Humanitarian_Q1 ~ Age + Income + Education + Ethnicity + Political_Party + Political_Involvement, data = train, Hess = TRUE)
# model <- polr(Humanitarian_Q1 ~ Age + Income + Education + Ethnicity + Political_Party + Political_Involvement, Treatment_1, Treatment_2, Treatment_3, Treatment_4, Treatment_5, Treatment_6, Treatment_7, data = train, Hess = TRUE)
summary(model)

#Confusion Matrix 
prediction = predict(model, test)
table(test$Humanitarian_Q1, prediction)

#library("effects") 
plot(Effect(focal.predictors = "Political_Party", model))

#Creating histograms from the responses 
x <- data$Humanitarian_Q1
> barplot(prop.table(table(x)))