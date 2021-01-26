# Senator Vote Prediction 
### Using Bills and Vote History to Predict Allegiance

The app created to explore this model can be found at https://senator-prediction.jeremytraberowens.com. 

For cost-effectiveness, 
the Sagemaker backend may not always be running, but the comparison of the model against older bills can always be
explored. Should you like to explore how the model behaves for proposed, as yet unseen bills, please email 
jeremytraberowens [at] gmail [dot] com to turn the service on.

## Introduction

The goal of this project was multi-fold. From a curiosity standpoint, I'm most interested in politics and civic tech, 
and I wanted to know if ML could help people predict how the votes on a given bill would swing in Congress, as those 
laws have vast repercussions throughout our entire country (the USA in my case).

From a technical standpoint, while I was confident in my abilities as it comes to data exploration, analysis, and 
building predictive models, I specifically wanted to learn more about natural language processing (NLP) in the world of 
data science, and how to implement it in machine learning algorithms. I also wanted to grow my skills in creating apps 
that people can use to explore and utilize my model, as well as how to use containers (Docker) and hosting services 
(AWS) to make sure the application is seamless across all environments.

While this app that I developed is fun for citizens and policymakers to use, seeing how various bills they devise could 
fare on the floor of the Senate, this is a product most geared towards the majority and minority whip of the Senate. This
app could certainly be expanded to work in both houses of Congress, but I decided to focus on the Senate for this 
venture. One, the data would be more manageable for an MVP (only 100 senators compared to 435 house seats, which
multiplied across all the bills that hit the floor is a significant difference). Two, senators serve a longer term 
(6 years vs. 2 years), so the model would likely pick up on trends for a particular senator across bills easier than 
house congresspeople, who (potentially) rotate out every 2 years.

## 01 - Data Acquisition

This project focuses on the last 8 years of senatorial bodies. Starting in 2012, we have the 113th Congress (through 2014), 
and we end with the 116th Congress, which existed from 2018 to 2020. This was done party out of necessity, partly by 
design. For one, the OpenSecrets API does not have any contribution data prior to the 2012 cycle. While the Open Secrets
data is not a part of the MVP model presented here, it is planned for future versions, and thus training on years
prior to 2012 would make later OpenSecrets integration very cumbersome. From an industry knowledge standpoint as well, 
2012 is an inflection point in the extreme divisiveness of the political parties today. We were past the tumult of the 
2008 financial crisis that was the star of that election cycle, and we existed in a divided government (with the president
of one political party and at least one house of congress of the other political party). In 2014, the Senate flips to 
the Republican party, so we have at least 2 years of a Democratic majority in the Senate before a long Republican
majority in the following 6 years, which bakes in a little noise that's useful for the model to parse out.

One of the most prominent sources of data for this project is [Voteview](https://voteview.com/) which houses a
historical record of all the votes and members of each house of congress, all the way back to the very first congress in
the United States. There are a few .csv files for each senate (113-116) that are most pertinent to this study, those of
the members of each congress, the overall votes for bills on the floor (aka rollcalls), and the individual votes cast by
each member in each congress.

I also utilized the OpenSecrets API to pull down contribution information for every senator that served in the range of 
congresses I was analyzing. While the MVP version of this model did not end up using contribution data, the combination
of voteview data and open secrets data allowed me to create a table that I could not find anywhere else on the internet,
one that acts as a reference table for any senator's CID (ID for open secrets), BioguideID (used by congress.gov), 
icpsr (an ID used by Voteview and other political science resources), and their FEC Candidate ID (how they are
referenced in FEC databases).

![Senator Reference Table](images/senator_ref_df_head.png)

There are a few profiles for Senators that are missing from the OpenSecrets search, but those ids, as I discovered
through some research, are for senators who were appointed due to an elected senator's death, 
or left shortly after winning due to scandal.

For election voting history (so I can calculate how safe a certain senator's district is, which could certainly
influence voting patterns), I went to the MIT Election Lab, where they have a downloadable .tsv file of all election
results back to 1976. That file can be found 
[here](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/PEJ5QU).

The other major data source used is via the ProPublica API, which allowed me to gather the summaries, subjects, and
amendments for all the bills that wanted to train and validate the model on. I ignored treaty documents in this case, as
they were not relevant to this project. I also opted to ignore the National Defense Authorization Act yearly fiscal 
bills, as they were mostly pro forma votes and would just be extra noise for the model.

## 02 - DF construction and Feature Engineering

While it's such a major component to any model development, very few people care about the dataframe construction and
feature engineering process, so I'll just say after joining all the above data together, and doing some transformations
and feature engineering, I end up with the following, most pertinent features to send to the baseline model:

Senator info:
- DW Nominate dimension 1
- DW Nominate dimension 2
- What percent of the vote they had in their most recent campaign
- Boolean for if the vote is being cast in an election year
- Their tenure in the Senate (how long since they were first voted in)
- Their age
- Boolean for if they are the sponsor of the bill being voted on
- Boolean for if the sponsor of the bill is from their same party
- Dummy variables for what their party affiliation is
- How many cosponsors of the bill are of the same party as the senator (standard and exponentiated)

Bill/Congress info:
- Boolean for if the sponsor party of the bill is the lead party in the Senate
- The percentage of the total cosponsors that are Democrat or Republican
- Of those percentages, which is of the lead party
- Dummy variable for if the sponsor party is Democrat, Republican, or Independent
- Total cosponsors of the bill, and how many there are of each party (standard and exponentiated) 
- If the lead party in the Senate is Democrat or Republican

I drop any bills that lack sponsor information, or where there are cast codes that are present or absent (aka, not a
true yea or nay vote).

I then pickle that combined DataFrame for baseline modeling and eventually more advanced ML modeling with XGBoost.

## 03 - Baseline Model

For developing this model, I chose to drop all rollcalls except for the last for each bill (to make sure hard fought 
bills that had multiple voting rounds weren't oversampled in the dataset)

I used a Train-Test-Split of 70-30, ran all the non-text data through a standard scalar, and utilized SMOTE to balance
out the otherwise imbalanced dataset (in the base dataset there are far more nay votes than yea votes).

I ran a recursive feature engineering ranking on the dataset, assuming a logistic regression model, and aimed for 
around 15 features before taking the modified dataset and fitting it to the logistic regression model. The prediction
results can be found below:

![Logit Prelim Confusion Matrix](images/logit1_base_confusion_report.png)
![Logit Prelim ROC Graph](images/logit1_base_roc.png)

I also wanted to see how a Random Forest algorithm would perform, as it's consistently one of the easiest to implement
and represents close to the best we can do without incorporating vectorized text data. Using the same Train-Test-Split, 
scalar, and SMOTE, and using all the available features, instead of just those from the recursive feature engineering
done for the logistic regression model, we end up with the following metrics on the prediction set:

![Random Forest Confusion Matrix](images/rf_base_confusion_report.png)
![Random Forest ROC Graph](images/rf_base_roc.png)

There's definite improvement here over the logistic regression model, both in our F1 and our ROC score, but I wanted to 
make sure it's an apples to apples comparison for the two baseline models. I pulled out the feature importance for all 
the features used in the Random Forest model and plotted them to see if there were any major drop off points.

![Random Forest Feature Importance](images/rf_base_feature_import_graph.png)

It's a fairly even slope, though there is a noticeable drop around party_R, the 18th feature.

To be sure, I iterated through an increasing number of features (in order of importance from the above graph), and ran
a fit/predict (using all the same methods as before) on a logistic regression, and below you can see the F1 score for 
every iteration.

![Logit Feature Test](images/logit_feature_iteration.png)

I chose to stick with 18 features, as at the 18th feature we hit an F1 score of .792 (rounded), and it was the lowest
number of features I could use to achieve that F1 score, which did not meaningfully increase even by the 27th iteration. 

I re-ran the logistic regression with those 18 features, using the same methods as before and here were the results
for that new baseline.

![Logit Base Confusion Matrix](images/logit2_base_confusion_report.png)
![Logit Base ROC Graph](images/logit2_base_roc.png)

Alas, there was no real change from the previous iteration of the logistic regression model, but I pickled the 18 chosen 
features for use in more advanced XGBoost model.


## 04 - XGBoost Model

XGBoost is a machine learning algorithm that has taken the world by storm, and is especially well suited to 
vectorized text, so I decided to see if I could improve the predictive accuracy (or in this case, F1 and ROC) using 
said algorithm.

As before, I drop all rollcalls except the last for each bill, and use the top 18 features I pickled from the baseline
model.

I originally randomly split all data in my train-test-split, but later determined that randomly separating out 
individual bills was a more scientific approach, and would ensure no information from my training environment leaked 
into my test environment.

Just to see where I stood before adding in vectorized text, I ran the XGBoost model using only the 18 pickled features,
and below you can see the results:

![XGB No NLP Confusion Matrix](images/xgb_no_nlp_confusion_report.png)
![XGB No NLP ROC](images/xgb_no_nlp_roc.png)

There is a slight improvement, but no major change from logistic regression baseline model.
The XGBoost model has better performance in classifying false values (comparatively), but worse performance in 
predicting true values, though there is an overall improved ROC score (7% improvement).

Let's see what I can do with some NLP mixed in instead!

### XGB with NLP

Since pre-trained text vectorizers are far easier to implement and have been trained on far more text data than I have 
in my own project, I decided to utilize the Universal Sentence Encoder from google to vectorize the bill summaries I had
available. While the MVP just focuses on summaries, later interations will include the entire bill text and/or 
amendments made throughout the voting process.

I extract the bill summaries, send then through the USE, take those embeddings and turn them into thier own dataframe, 
join that dataframe back with the list of original bill summaries, join that back to main dataframe, oversample 
the training set with SMOTE (as we still want to make sure our training set is balanced), and run that through an
XGBoost algorithm. Below are the results!

![XGB NLP Confusion Matrix](images/xgb_nlp_confusion_report.png)

![XGB NLP ROC](images/xgb_nlp_roc.png)

The incorporation of text appears to improve the F1 score, but slightly decreases the ROC score. This suggests that 
while the model improves at the rounded binary classification of a yea or nea vote, those votes it predicts incorrectly 
it predicts more confidently in the opposite direction.

### Hyperparameter Tuning

The final thing I did with the XGBoost model is some hyperparameter tuning, to see what additional shifts I could make in 
eeking out the last of that F1 score and ROC curve. I performed a nested iteration through 'n_estimators', 'max_depth', 
'learning_rate', 'subsample', 'colsample_bytree', and 'gamma', seen below:

```python
n_estimators = [100, 500, 1000]
max_depth = [3, 4, 5, 6]
learning_rate = [.1, .01]
subsample = [.8, .9, 1]
colsample_bytree = [.3, .6, .9]
gamma = [0, 1, 5]
```

```python
for a in n_estimators:
    for b in max_depth:
        for c in learning_rate:
            for d in subsample:
                for e in colsample_bytree:
                    for f in gamma:
                        try:
                            clf_xgb = xgb.sklearn.XGBClassifier(nthread=-1, seed=1234, 
                                                                learning_rate=c,
                                                                n_estimators=a,
                                                                max_depth=b,
                                                                min_child_weight=1,
                                                                gamma=f,
                                                                subsample=d,
                                                                colsample_bytree=e,
                                                                objective= 'binary:logistic',
                                                                scale_pos_weight=1)

                            clf_xgb.fit(X_over_vec[model_cols], y_over)
```

Believe me, I hated writing that nested loop as much as you hate reading it.

I then plotted the f1 score against the roc score and from all those iterations. I visually chose the hyperparameter 
sets with the highest F1 score, the one with the highest ROC score, and one that was a balance between the two.

I then tested each of those hyperparameter sets using the same oversampled, nlp-included train and test sets as before, 
and chose the one with the highest F1 score, as the ROC was basically the same between all 3 models,as you can see
below.

```python
{'n_estimators': 1000, 
 'max_depth': 6, 
 'learning_rate': 0.1, 
 'subsample': 1, 
 'colsample_bytree': 0.9, 
 'gamma': 0, ...}
F1:  0.8685
ROC: 0.853

{'n_estimators': 500, 
 'max_depth': 6, 
 'learning_rate': 0.1, 
 'subsample': 1, 
 'colsample_bytree': 0.9, 
 'gamma': 0, ...}
F1:  0.8655
ROC: 0.8542

{'n_estimators': 1000, 
 'max_depth': 5, 
 'learning_rate': 0.1, 
 'subsample': 0.9, 
 'colsample_bytree': 0.3, 
 'gamma': 1, ...}
F1:  0.8584
ROC: 0.8567
```

I ran with threshold of .6 (instead of .5) for a vote going yea instead of nay, and our f1 score gets up to random 
forest levels, but with a significant improvement in our ROC over the Random Forest model.

![XGB Hyper Confusion Matrix - Low Threshold](images/xgb_best_hyper_6_thresh_confusion_report.png)

![XGB Hyper ROC](images/xgb_best_hyper_roc.png)

We can see how imbalanced the confusion matrix is though, and in practice, a majority or minority whip who was using 
this product would assume the votes were there too often, when they actually weren't. So I raised the threshold for a 
yea vote to .9, and the matrix shifts as such:

![XGB Hyper Confusion Matrix - High Threshold](images/xgb_best_hyper_9_thresh_confusion_report.png)

While it lowers our F1 score slightly, the more balanced classes are better served in the eventual product, though we
keep the same ROC score as before.

## 05 - Creating artifacts for the web application

I then run the entire dataframe through the model and append the predictions from the model onto the main dataframe 
for faster retrieval of information in the web app. I save that dataframe as an artifact. I also save the features, 
scalar, and model as .sav files, which will eventually be hosted on AWS for retrieval when creating a sagemaker docker 
container for predictions.

## 06 - Building a web app front end (and containerizing)

There are two main containers that I built to present this model to the world. One is the front end web application 
(what's in the web_app folder) that is built using streamlit and allows a user to either: 
1. See how the model compares against how the actual vote went for that bill or
2. Create a new proposed bill (adding in summary information as well as how many cosponsors of each party are on the bill)

The main.py file initializes the sidebar and creates a session state (the class also defined in the main.py file) 
based on the user's choice of which part of the application they want to view (new bills or old bill comparison). This
session state allows the sidebar to persist with the same entry fields throughout the building process for a new proposed
bill. Once the new or old bill direction is chosen, the main file calls the new_bill_search or old_bill_search function
(respectively) that exist in their own python files.

If working with an old bill, it starts by initializing a DataframeHandler object, which is the backend workhorse for 
parsing which congresses are available to view, and what bill numbers exist in that congress to view votes for.
The user chooses which congress they want to view (anything from the 113th to the 116th
congress) and which bill from that congress they want to view a comparison for. Once the "Bill Look Up" button is
pressed, the DataframeHandler object pulls out the information for that specific bill, displays the top line metrics for
how the model compares against reality, and plots the predicted likelihood of a vote against each senator's DW 
nominate score (which is roughly a score on how liberal or conservative a congressperson is, more info here: 
https://en.wikipedia.org/wiki/NOMINATE_(scaling_method)). 

![Top Line Metrics](images/app_vote_metrics.png)

![Voting Graph](images/app_vote_graph.png)

If working with a new proposed bill, we still initialize a DataframeHandler object so that we know which senators from
which Congress we want predictions for. The user is asked to enter pertinent information (a summary of the proposed
bill, and the number of cosponsors from each party, as well as independents) before the information is compiled and
sent to a Sagemaker endpoint on AWS. That endpoint (expanded on below) creates the calculated fields it needs from the
user passed data, and returns a json object, which is parsed into a dataframe and output into human language voting
metrics and graphed for a visualization of where each senator lands on their predicted vote probability.

All of the code for this front end app exists in a Docker image that lives on AWS ECR, which is then pulled into an AWS
EC2 instance. Once I SSH'd into the instance and pulled down the docker image from ECR, I ran a container, passing in the
needed AWS credentials as environmental variables (so they weren't hardcoded anywhere) so that the front end could
appropriatly call the sagmaker endpoint for predictions of new bills.

## 07 - Building a sagemaker backend on AWS

The Docker container that's eventually run on Sagemaker is a Flask app that listens for any data sent to the
ip-address/invocations. When data is POSTed to /invocations, it uses the ModelHandler object (in model_api.py) to
transform the data (including vectorizing the bill summary with the Universal Sentence Encoder) into a dataframe that the
trained model can make a vote prediction on. The ModelHandler returns a dataframe consisting of the name of the senator,
their party, their DW Nominate score, the probability of a yea vote, and the predicted actual cast of their vote
(currently using a .9 probability threshold for a guaranteed yes vote).

That dataframe is then passed back to the Flask app as a json file, the Flask app send that json back to the front end,
and the front end web app decodes the json back to a pandas dataframe for showing vote metrics and probability graphs.

## 08 - Getting the app hosted and running on AWS Servers

While it's wonderful that the two Docker containers exist on AWS and can talk to each other, what matters more is can
this be a useful product for whips, or at the very least, a fun app for citizens to play around with. To wrap this up, 
I transferred my domain from GoDaddy to Route 53 (quite the process involving nameserver changes and super secret 
authorizations) and requested an SSL certificate so people could securely access the subdomain of my personal domain
that this app exists on. I set up an Elastic IP address for the EC2 container as well, so at least I always had a set
of numbers to fall back on when testing the app online.

I then set up an Application Load Balancer as a reverse proxy to route the http traffic to the more secure https site
(props to [Ahmed Besbes on Medium](https://medium.com/swlh/end-to-end-machine-learning-from-data-collection-to-deployment-ce74f51ca203) 
for the inspiration). After creating all the target and security groups necessary, 
and making sure the http redirect was set up, I then could view the app through my load-balancer-dns-name-amazonaws.com!

For the finishing polish, I created a record set for my chosen subdomain in my Route 53 hosted zone, with the Alias 
set to my Application Load Balancer. 30 minutes later, post DNS propogation, my app was ready for the world to see at 
https://senator-prediction.jeremytraberowens.com!
