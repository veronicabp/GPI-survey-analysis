# Import data set 
data <- read_csv("FALL 2021/GPI Initiative/cleaned_data.csv")

#install.packages("dplyr") 

# remove row with participant over 75 and less than high school because there is only one 
data = data[data$age != "75 - 84", ]
data = data[data$education != "Less than high school", ]

#Print summary statistics 
summary(data)


#Create a frequency table 
library(dplyr)
library(tidyr)
gather(data, key, val) 
count(key, val) 
spread(key, n)


#Create bar plots demonstrating response frequency
barplot(table(data$age), main = "Age Representation", xlab = "Age Ranges", ylab = "Frequency", col = "#ff9d5c")
barplot(table(data$income), main = "Spread of Income", xlab = "Income", ylab = "Frequency", col = "#000080")


#Create 3D piechart for political party representation 
table(data$party)
x <- c(388, 175, 55, 2)
categories <- c("Democrat", "Republican", "Independent", "Other")
pie3D(x, labels = categories, explode = 0.03, main = "Party Representation")


# creating donut plots 
install.packages("labeling")
install.packages("farver")
library(ggplot2)
donut_data <- data.frame(category=c("2 year degree", "4 year degree", "Doctorate", "High school graduate", "Professional degree", "Some college"), count = c(31, 387, 5, 29, 116, 52))
donut_data$fraction <- donut_data$count / sum(donut_data$count)  # Compute percentages
donut_data$ymax <- cumsum(donut_data$fraction)  
donut_data$ymin <- c(0, head(donut_data$ymax, n=-1)) 
donut_data$labelPosition <- (donut_data$ymax + donut_data$ymin) / 2   # Compute label position
donut_data$label <- paste0(donut_data$category, "\n value: ", donut_data$count)

ggplot(donut_data, aes(ymax=ymax, ymin=ymin, xmax=4, xmin=3, fill=category)) + geom_rect() +
geom_label( x=3.5, aes(y=labelPosition, label=label), size=2.2) 
+     scale_fill_brewer(palette=4) 
+     coord_polar(theta="y") + xlim(c(2, 4)) 
+     theme_void() 
+     theme(legend.position = "none")


#Create boxplots to compare questions 
boxplot(data$Q1, data$Q5, data$Q9, col = "#FFFFC2", main = "Range of Responses for Human Rights Focused Questions", names = c("Human Rights", "Economic Growth", "Military/Tech"), ylab = "Responses in Numeric Form")

#Grouped barplots to look at political invovlement 
df <- data.frame(Level = c(1, 1, 2, 2,3, 3, 4, 4,5, 5), Category = c("Involvement", "Knowledge", "Involvement", "Knowledge","Involvement", "Knowledge","Involvement", "Knowledge","Involvement", "Knowledge"), Frequency = c(9,169,36, 99, 173, 144, 255, 143, 149, 67))
ggplot(df, aes(fill= Category, y= Frequency, x= Level)) + 
    geom_bar(position='dodge', stat='identity') + labs(title='Political Involvement & Knowledge') + theme(plot.title = element_text(hjust=0.5, size=20, face='bold')) 

# Compare percent of a specific question before and after removing a specific treatment 
install.packages('epiDisplay')
library(epiDisplay)
install.packages(tweenr)
library(ggplot2)
library(gganimate)

removed_T3 <- data[!(data$T3== 1), ]
tab1(data$Q1, sort.group = "decreasing", cum.percent = TRUE)
table1 = tab1(data$Q12, sort.group = "decreasing", cum.percent = TRUE)
table2 = tab1(removed_T3$Q12, sort.group = "decreasing", cum.percent = TRUE)
set1 <- data.frame(Responses = c("-2", "-1", "0", "1", "2"), Percent = c(10, 12.9, 18, 26.4, 32.8), frame=rep('a',5))
set2 <- data.frame(Responses = c("-2", "-1", "0", "1", "2"), Percent = c(9.6, 11.5, 16.9, 28, 34.1),frame=rep('b',5))
binded_data <- rbind(set1,set2)

ggplot(binded_data, aes(x= Responses, y= Percent, fill= Responses)) + 
  geom_bar(stat='identity') +
  theme_bw() +
  # gganimate specific bits:
  transition_states(
    frame,
    transition_length = 2,
    state_length = 1
  ) +
  ease_aes('sine-in-out') + labs(title='The Effect of T3 on Q12') + theme(plot.title = element_text(hjust=0.5, size=20, face='bold'))
anim_save("animated-barplot-transition.gif")

# Make responses ordinal 
first_set <- c("T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8", "age", "income", "education", "ethnicity", "party", "involvement", "knowledge")
first_set_data <- data[first_set]
second_set <- c("Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7", "Q8", "Q9", "Q10", "Q11", "Q12")
second_set_data <- data[second_set]
second_set_data[second_set_data == 2] <- 5
second_set_data[second_set_data == 1] <- 4
second_set_data[second_set_data == 0] <- 3
second_set_data[second_set_data == -1] <- 2
second_set_data[second_set_data == -2] <- 1
new_data <- cbind(first_set_data, second_set_data)

#Split into train and test 
samplesize = .7*nrow(new_data)
set.seed(100)
index = sample(seq_len(nrow(new_data)), size = samplesize)
train = new_data[index,]
test = new_data[-index,]

#library(dplyr)
# library(MASS) 
model <- polr(as.factor(Q1) ~ T1 + T2 + T3 + T4 + T5 + T6 + T7 + T8 + age + ethnicity + party + involvement + knowledge, data = train, Hess = TRUE)
# model <- polr(Humanitarian_Q1 ~ Age + Income + Education + Ethnicity + Political_Party + Political_Involvement, Treatment_1, Treatment_2, Treatment_3, Treatment_4, Treatment_5, Treatment_6, Treatment_7, data = train, Hess = TRUE)
summary(model)

#Confusion Matrix 
prediction = predict(model, test)
table(test$Q1, prediction)

#library("effects") 
plot(Effect(focal.predictors = "party", model))
plot(Effect(focal.predictors = "age", model))
plot(Effect(focal.predictors = "ethnicity", model))
plot(Effect(focal.predictors = "involvement", model))
plot(Effect(focal.predictors = "knowledge", model))

#effects of treatments on model 
plot(Effect(focal.predictors = "T1", model))
plot(Effect(focal.predictors = "T2", model))
plot(Effect(focal.predictors = "T3", model))
plot(Effect(focal.predictors = "T4", model))
plot(Effect(focal.predictors = "T5", model))
plot(Effect(focal.predictors = "T6", model))
plot(Effect(focal.predictors = "T7", model))
plot(Effect(focal.predictors = "T8", model))


#Creating histograms from the responses 
x <- data$Q1
barplot(prop.table(table(x)))
x <- data$Q2
barplot(prop.table(table(x)))
x <- data$Q3
barplot(prop.table(table(x)))
x <- data$Q4
barplot(prop.table(table(x)))
x <- data$Q5
barplot(prop.table(table(x)))
x <- data$Q6
barplot(prop.table(table(x)))
x <- data$Q7
barplot(prop.table(table(x)))
x <- data$Q8
barplot(prop.table(table(x)))
x <- data$Q9
barplot(prop.table(table(x)))
x <- data$Q10
barplot(prop.table(table(x)))
x <- data$Q11
barplot(prop.table(table(x)))
x <- data$Q12
barplot(prop.table(table(x)))

#Running a Logistic for Each Question (have to run each one by one)
model <- polr(as.factor(Q1) ~ age + ethnicity + education + party + involvement + knowledge, Hess = TRUE)
model(summary)
model <- polr(as.factor(Q2) ~ age + ethnicity + education + party + involvement + knowledge, Hess = TRUE)
model(summary)
model <- polr(as.factor(Q3) ~ age + ethnicity + education + party + involvement + knowledge, Hess = TRUE)
model(summary)
model <- polr(as.factor(Q4) ~ age + ethnicity + education + party + involvement + knowledge, Hess = TRUE)
model(summary)
model <- polr(as.factor(Q5) ~ age + ethnicity + education + party + involvement + knowledge, Hess = TRUE)
model(summary)
model <- polr(as.factor(Q6) ~ age + ethnicity + education + party + involvement + knowledge, Hess = TRUE)
model(summary)
model <- polr(as.factor(Q7) ~ age + ethnicity + education + party + involvement + knowledge, Hess = TRUE)
model(summary)
model <- polr(as.factor(Q8) ~ age + ethnicity + education + party + involvement + knowledge, Hess = TRUE)
model(summary)
model <- polr(as.factor(Q9) ~ age + ethnicity + education + party + involvement + knowledge, Hess = TRUE)
model(summary)
model <- polr(as.factor(Q10) ~ age + ethnicity + education + party + involvement + knowledge, Hess = TRUE)
model(summary)
model <- polr(as.factor(Q11) ~ age + ethnicity + education + party + involvement + knowledge, Hess = TRUE)
model(summary)
model <- polr(as.factor(Q12) ~ age + ethnicity + education + party + involvement + knowledge, Hess = TRUE)
model(summary)

#Running a Logistic for Each Question by treatment (have to run each one by one)
model <- polr(as.factor(Q1) ~ T1 + T2 + T3 + T4 + T5 + T6 + T7 + T8, data = train, Hess = TRUE)
model(summary)
model <- polr(as.factor(Q2) ~ T1 + T2 + T3 + T4 + T5 + T6 + T7 + T8, data = train, Hess = TRUE)
model(summary)
model <- polr(as.factor(Q3) ~ T1 + T2 + T3 + T4 + T5 + T6 + T7 + T8, data = train, Hess = TRUE)
model(summary)
model <- polr(as.factor(Q4) ~ T1 + T2 + T3 + T4 + T5 + T6 + T7 + T8, data = train, Hess = TRUE)
model(summary)
model <- polr(as.factor(Q5) ~ T1 + T2 + T3 + T4 + T5 + T6 + T7 + T8, data = train, Hess = TRUE)
model(summary)
model <- polr(as.factor(Q6) ~ T1 + T2 + T3 + T4 + T5 + T6 + T7 + T8, data = train, Hess = TRUE)
model(summary)
model <- polr(as.factor(Q7) ~ T1 + T2 + T3 + T4 + T5 + T6 + T7 + T8, data = train, Hess = TRUE)
model(summary)
model <- polr(as.factor(Q8) ~ T1 + T2 + T3 + T4 + T5 + T6 + T7 + T8, data = train, Hess = TRUE)
model(summary)
model <- polr(as.factor(Q9) ~ T1 + T2 + T3 + T4 + T5 + T6 + T7 + T8, data = train, Hess = TRUE)
model(summary)
model <- polr(as.factor(Q10) ~ T1 + T2 + T3 + T4 + T5 + T6 + T7 + T8, data = train, Hess = TRUE)
model(summary)
model <- polr(as.factor(Q11) ~ T1 + T2 + T3 + T4 + T5 + T6 + T7 + T8, data = train, Hess = TRUE)
model(summary)
model <- polr(as.factor(Q12) ~ T1 + T2 + T3 + T4 + T5 + T6 + T7 + T8, data = train, Hess = TRUE)
model(summary)
