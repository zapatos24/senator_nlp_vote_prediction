# Senator Vote Prediction 
### Using Bills and Vote History to Predict Allegiance

The goal of this project was multi-fold. From a curiosity standpoint, I'm most interested in politics and civic tech, 
and I wanted to know if ML could help people predict how the votes on a given bill would swing in Congress, as those 
laws have vast repercussions throughout our entire country (the USA in my case).

From a technical standpoint, while I was confident in my abilities as it comes to data exploration, analysis, and 
building predictive models, I specifically wanted to learn more about natural language processing (NLP) in the world of 
data science, and how to implement it in machine learning algorithms. I also know that if a data science project is 
created and no one can play with it, did it really happen? As such, I wanted to grow my skills in creating apps that 
people can use to explore and utilize my model, as well as how to use containers (Docker) and hosting services (AWS) to 
make sure the application is seamless across all environments.

While this app that I developed is fun for citizens and policymakers to use, seeing how various bills they devise could 
fare on the floor of Congress, this is a product most geared towards the majority and minority whip of the Senate. This
app could certainly be expanded to work in both houses of Congress, but I decided to focus on the Senate for this 
venture. One, the data would be more manageable for an MVP (only 100 senators compared to 435 house seats, which
multiplied across all the bills that hit the floor is a significant difference). Two, senators serve a longer term 
(6 years vs. 2 years), so the model would likely pick up on trends for a particular senator across bills easier than 
house congresspeople, who (potentially) rotate out every 2 years.

## 01 - Data Acquisition

congress 113-116

voteview votes
voteview members
voteview rollcalls

open secrets - future use for bringing in campaign donation info into votes
was able to create a table of CID, FecCandID, BioguideID, Name CSV for senators that did not yet exist on internet

[fancy_table_df_head.png]

pull all open secrets data, but Remaining ids are for senators who were appointed due to an elected senator's death, 
or left shortly after winning due to scandal.

propublica api - gather bill summaries, subjects list, and amendments from initial bill (ignore treaty documents, not
relevant to this project)

remaining missing bills are those that are the National Defense Authorization Act yearly fiscal bills

## 02 - DF construction and Feature Engineering

making all dataframes from gathered data

join all votes from congress 113 - 116 (dropping those of the vice president, adds unnecessary noise to model)

join all senators from congress 113-116
    drop pres/vice-pres
    change the party code to a readable letter
    separate out name parts for easier joining of dataframes later

join with votes df and add column for the lead party for each congress

join all the rollcalls from each congress together

join to votes/members dataframe

pull out nomination and treaty votes (to reduce model noise)

using fancy table, added cid info to each row in the df (though not currently in use)

created df of major industries that contributed to each senator, but did not incorporate into final model

parse resultant df for all bill numbers, search pro-pub summaries and subjects
parse bill info (summary and cosponsors) into dict from 'summary' pro-pub json
parse party cosponsor count into dict
parse all subjects (if any) into string of all subjects
    #add the subjects string to the dictionary
add the full dictionary to a list of all bills

add all bill info to the votes, members, rollcalls, ids df

add industry info for each senator to the main df
    we create feature for what campaign year relates to congress number, since they are not aligned

make df for election data back to 1976
reduce election df to just those who won each election
fix Lisa Murkowski's nan value for the 2010 election
clean up party affiliations
parse out first and last names
calc how close the race was
make a df for each time someone one their first election by dropping duplicates, keeping their first win
merge the first year elected back onto election df

make the main dataframe by merging election data with all other info (votes, members, ids, etc.)

create feature for if it's an election year
senator's tenure in office (since they first joined)
senator's age
if they're a sponsor of a given bill
whether or not the sponsor of the bill is the lead party in the senate
percentage of cosponsors from a given party on a bill
what is the percentage of cosponsors from the lead party
is the sponsor the same party as the given senator
make interaction of party with cosponsors of that party
exponentiate cosponsor values

dummy variable party and sponsor_party columns
dummy variable lead party designation
drop anywhere df lacks sponsor info
drop any cast codes that are present or absent, and change cast code 6 ('nay') to 0

pickle for baseline and advanced ML modeling

## 03 - Baseline Model

Drop all rollcalls except last for each bill (to make sure hard fought bills aren't oversampled in dataset)
** check with Christophe on this

TTS .3
run non-text data through standard scalar
SMOTE imbalanced dataset (far more nays than yeas)

run recursive feature engineering on dataset (assuming logit reg model)

fit/predict logit model
[logit1_base_confusion_report.png]
roc-auc score
[logit1_base_roc.png]

Random Forest
TTS .3, scale, smote

fit/predict logit model
[rf_base_confusion_report.png]
roc-auc score
[rf_base_roc.png]

improvement, but want to make sure it's apples to apples comparison for two baselines

[rf_base_feature_import_graph.png]

iterated through logit using more and more features (in order of rf importance)

[logit_feature_iteration.png]

chose 18 features for reasons, re-ran logit with same TTS .3, scale, smote

[logit2_base_confusion_report.png]
roc-auc score
[logit2_base_roc.png]

No real change, but saved 18 chosen features for use in more advanced model


## 04 - XGBoost Model

drop all rollcalls except last, and use top 18 features from logit/RF

originally just randomly sampled all data, but later determined that randomly separating out individual bills would
ensure no information from my training environment leaked into my test environment

[xgb_no_nlp_confusion_report.png]

[code for roc score on xgb no nlp]

slight improvement, but no major change from logit model
better performance in classifying false values, worse in predicting true values, though an overall improved ROC
score (7%)

### XGB with NLP

Utilize the Universal Sentence Encoder from google to vectorize bills summaries

Turn the embeddings into df, join back with original bill summaries, join back to main_df, oversample training set

[xgb_nlp_confusion_report.png]

[code for roc score on xgb no nlp]

Incorporation of text appears to improve the F1 score, but slightly decrease the ROC score. Suggests that while the
model improves at the rounded binary classification of a yea or nea vote, those votes it corrects incorrectly it
predicts more confidently in the opposite direction.

### Hyperparameter Tuning

The final thing I did with the XGBoost model is some hyperparameter tuning, see what additional shifts we can make 
to eek out the last of that F1 score. I performed a nested iteration through 'n_estimators', 'max_depth', 'learning_rate', 
'subsample', 'colsample_bytree', and 'gamma'. 

[code for versions of each hyper iterated through]

I then plotted the f1 score against the roc score and from all those iterations, I visually chose the hyperparameter 
sets with the highest F1 score, the one with the highest ROC score, and one that was a balance between the two. 

[code block of choosing best hyper parameters]

I then tested each of those hyperparameter sets using the same oversampled, nlp-included train and test sets as before, 
and chose the one with the highest F1 score, as the ROC was basically the same between all 3 models.

[code for best hyperparameters]

ran with threshold of .6 (instead of .5) for a vote going yea instead of nay, f1 score gets up to random forest levels, 
with ROC a significant improvement over RF

[xgb_best_hyper_confusion_report.png]

We can see how imbalanced the confusion matrix is though, and in practice, a whip who was using this product would
assume the votes were there too often, when they actually weren't. So I raised the threshold for a yea vote to .9, and
the matrix shifts as such

[xgb_best_hyper_9_thres_confusion_report.png]

while it lowers our F1 score slightly, the more balanced classes are better served in the eventual product, though we
keep the same ROC score as before

## Creating artifacts for the web application

I then run the entire dataframe through the model, and append the predictions from the model onto the main dataframe, 
for faster retrieval of information in the web app, and save that df as an artifact. I also save the features, scalar, 
and model as .sav files, which will eventually be hosted on AWS for retrieval when creating a sagemaker docker container 
for predictions.

