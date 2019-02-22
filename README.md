Online coding platforms have gained wide popularity through the recent
years. Our recommendation system aims to improve user experience
when the user interacts with the online coding platform. Everytime the user
visits the platform user data is collected based on user activity. The
engine recommends next problem to the user based on the user profile
and user’s history.

There are 4 different parts of this recommendation system as described below:
1.  Recommender system through collaborative filtering: For
    each user, recommender system will recommend the next problem based on how
    similar users solved the problem. For each user, user activity data is
    collected when the user visits the platform and based on the user
    activity data of similar users the next problem will be recommended.
    
    K-means algorithm used to overcome cold start problem
    
2.  Recommender system through content based filtering: For each user,
    recommender system will recommend the next problem based on the user profile
    and the user’s history. The next problem will be recommended based
    on the user profile which contains preference (type of the problem or
    complexity of the problem the user pefers to solve) and the user
    history based on the previous activity of the user.
    
3.  Prediction of level type of new problem: Built machine learning models
    to predict the level type of newly introduced problem with an accuracy of 48.417%
    The new problem entering the platform will contain only the tags making it
    difficult to recommend the problem. The models will predict the level type of the 
    problem which will be used to recommend the new problem to the users.
    
4.  Predicting the number of attempts taken by the user to solve the
    problem.
