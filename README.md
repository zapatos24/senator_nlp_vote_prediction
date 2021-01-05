# Senator Vote Prediction 
### Using Bills and Vote History to Predict Allegiance

The goal of this project was multi-fold. From a curiosity standpoint, I'm most interested in politics and civic tech, and I wanted to know if ML could help 
people predict how the votes on a given bill would swing in Congress, as those laws have vast repercussions throughout
our entire country (the USA in my case).

From a technical standpoint, while I was confident in my abilities as it comes to data exploration, analysis, and building predictive models, I
specifically wanted to learn more about natural language processing (NLP) in the world of data science, and how to 
implement it in machine learning algorithms. I also know that if a data science project is created and no one can play
with it, did it really happen? As such, I wanted to grow my skills in creating apps that people can use to explore and
utilize my model, as well as how to use containers (Docker) and hosting services (AWS) to make sure the application is
seamless across all environments.

While this app that I developed is fun for citizens and policymakers to use, seeing how various bills they devise could 
fare on the floor of Congress, this is a product most geared towards the majority and minority whip of the Senate. This
app could certainly be expanded to work in both houses of Congress, but I decided to focus on the Senate for this 
venture. One, the data would be more manageable for an MVP (only 100 senators compared to 435 house seats, which
multiplied across all the bills that hit the floor is a significant difference). Two, senators serve a longer term 
(6 years vs. 2 years), so the model would likely pick up on trends for a particular senator across bills easier than 
house congresspeople, who (potentially) rotate out every 2 years.

congress 113-116

voteview votes
voteview members
voteview rollcalls

open secrets - future use for bringing in campaign donation info into votes
was able to create table of CID, FecCandID, BioguideID, Name CSV for senators that did not yet exist on internet

pull all open secrets data, but Remaining ids are for senators who were appointed due to an elected senator's death, 
or left shortly after winning due to scandal.


