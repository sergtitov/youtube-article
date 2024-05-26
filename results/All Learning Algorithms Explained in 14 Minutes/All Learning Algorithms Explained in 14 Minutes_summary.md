# Intro

Imagine a world where machines can predict your next move, recommend the perfect song, or even diagnose diseases with uncanny accuracy. This isn't the plot of a sci-fi movie; it's the reality of machine learning. The video "Every single machine learning algorithm explained" dives into the heart of this fascinating field, breaking down complex algorithms into digestible pieces. From the simplicity of linear regression to the intricacies of gradient-boosted decision trees, the video aims to demystify the algorithms that power our modern world.

# ELI5

Think of machine learning algorithms as different types of chefs in a kitchen. Each chef has a unique way of preparing a dish, but they all aim to create something delicious. Some chefs follow a strict recipe (like linear regression), while others experiment with different ingredients to find the best flavor (like random forests). The video explains how these "chefs" work, making it easier for us to understand the magic behind the scenes.

# Terminologies

- **Algorithm**: A set of instructions for solving a problem or performing a task.
- **Linear Regression**: A method to model the relationship between a dependent variable and one or more independent variables by fitting a linear equation.
- **Support Vector Machine (SVM)**: A classification algorithm that finds the best boundary to separate different classes.
- **Naive Bayes**: A classification algorithm based on Bayes' theorem, assuming that features are independent.
- **Logistic Regression**: A classification algorithm used for binary outcomes, based on the logistic function.
- **K-Nearest Neighbors (KNN)**: A classification and regression algorithm that assigns values based on the closest data points.
- **Decision Trees**: A model that makes decisions by splitting data into branches based on feature values.
- **Random Forest**: An ensemble method that uses multiple decision trees to improve accuracy.
- **Gradient Boosted Decision Trees (GBDT)**: An ensemble method that builds trees sequentially, each one correcting errors from the previous tree.
- **K-Means Clustering**: An unsupervised learning method that groups data points into clusters based on similarity.
- **DBSCAN**: A clustering algorithm that finds clusters based on the density of data points.
- **Principal Components Analysis (PCA)**: A dimensionality reduction technique that transforms features into a set of principal components.

# Summary

## The Simplicity of Linear Regression

Linear regression is the bread and butter of machine learning algorithms. It's like a chef who follows a straightforward recipe to make a dish. The algorithm tries to fit a straight line through a set of data points, minimizing the distance between the points and the line. This method is particularly useful for predicting continuous outcomes, like house prices or stock values.

## The Precision of Support Vector Machines

Support Vector Machines (SVM) are like chefs who meticulously separate ingredients to create a perfect dish. SVMs are primarily used for classification tasks, drawing a decision boundary that best separates different classes. The algorithm plots data points in a multi-dimensional space and finds the hyperplane that maximizes the margin between classes. This makes SVMs highly effective for complex classification problems.

## The Speed of Naive Bayes

Naive Bayes is the fast-food chef of machine learning. It makes a "naive" assumption that all features are independent, which speeds up the computation. Despite its simplicity, Naive Bayes is surprisingly effective for many classification tasks, especially when speed is more critical than accuracy.

## The Versatility of Logistic Regression

Logistic regression is a versatile chef who can handle a variety of dishes. It's primarily used for binary classification problems, like predicting whether an email is spam or not. The algorithm uses the logistic function to map any real-valued number to a value between 0 and 1, making it ideal for probability-based predictions.

## The Neighborhood Watch of K-Nearest Neighbors

K-Nearest Neighbors (KNN) is like a neighborhood watch group that makes decisions based on the majority vote. The algorithm assigns a value to a data point based on the values of its nearest neighbors. This makes KNN simple and easy to interpret but also sensitive to the choice of the parameter 'K' and the presence of outliers.

## The Decision-Making of Decision Trees

Decision trees are like chefs who ask a series of questions to decide the best way to prepare a dish. The algorithm splits data into branches based on feature values, aiming to increase the purity of nodes. However, decision trees are prone to overfitting and often need to be combined with other trees to generalize well.

## The Ensemble Power of Random Forests

Random forests are like a team of chefs working together to create a masterpiece. This ensemble method uses multiple decision trees to improve accuracy and reduce overfitting. Each tree is built on a random subset of data and features, making the final model robust and reliable.

## The Sequential Learning of Gradient Boosted Decision Trees

Gradient Boosted Decision Trees (GBDT) are like chefs who learn from their mistakes to perfect a dish. This ensemble method builds trees sequentially, with each tree correcting the errors of the previous one. GBDT is highly accurate but requires careful tuning to avoid overfitting.

## The Clustering of K-Means

K-Means clustering is like a chef who groups similar ingredients together. This unsupervised learning method partitions data into clusters based on similarity. The algorithm iteratively adjusts the cluster centers until the data points converge, making it fast and easy to interpret.

## The Density-Based Clustering of DBSCAN

DBSCAN is like a chef who identifies clusters based on the density of ingredients. This algorithm is effective for finding arbitrary-shaped clusters and detecting outliers. It doesn't require the number of clusters to be specified beforehand, making it flexible and robust.

## The Dimensionality Reduction of PCA

Principal Components Analysis (PCA) is like a chef who simplifies a complex recipe without losing its essence. This dimensionality reduction technique transforms features into a set of principal components, retaining as much information as possible. PCA is widely used as a preprocessing step for other algorithms, making it a valuable tool in the machine learning toolkit.

# Takeaways

- **Understand the Basics**: Familiarize yourself with the fundamental concepts of each algorithm.
- **Choose the Right Tool**: Select the algorithm that best fits your problem's requirements.
- **Balance Speed and Accuracy**: Consider the trade-offs between computational speed and accuracy.
- **Avoid Overfitting**: Use techniques like cross-validation and ensemble methods to prevent overfitting.
- **Tune Hyperparameters**: Carefully tune the hyperparameters to optimize model performance.
- **Preprocess Data**: Use techniques like PCA for dimensionality reduction and data preprocessing.
- **Stay Updated**: Keep abreast of the latest developments in machine learning to continually improve your models.

# Full transcript

## Introduction to Algorithms

Every single machine learning algorithm explained. In case you don't know, an algorithm is a set of commands that must be followed for a computer to perform calculations or other problem-solving operations. According to its formal definition, an algorithm is a finite set of instructions carried out in a specific order to perform a particular task. It's not an entire program or code; it is simple logic to a problem.

## Linear Regression

Linear regression is a supervised learning algorithm and tries to model the relationship between a continuous target variable and one or more independent variables by fitting a linear equation to the data. Take this chart of dots, for example. A linear regression model tries to fit a regression line to the data points that best represents their relations or correlations. With this method, the best regression line is found by minimizing the sum of squares of the distance between the data points and the regression line. So for these data points, the regression line looks like this.

## Support Vector Machine (SVM)

Support Vector Machine or SVM for short is a supervised learning algorithm and is mostly used for classification tasks but is also suitable for regression tasks. SVM distinguishes classes by drawing a decision boundary. How to draw or determine the decision boundary is the most critical part in SVM algorithms. Before creating the decision boundary, each observation or data point is plotted in n-dimensional space, with n being the number of features used. For example, if we use length and width to classify different cells, observations are plotted in a 2-dimensional space and decision boundary is a line. If we use 3 features, decision boundary is a plane in 3-dimensional space. If we use more than 3 features, decision boundary becomes a hyperplane, which is really hard to visualize. Decision boundary is drawn in a way that the distance to support vectors are maximized. If the decision boundary is too close to a support vector, it'll be highly sensitive to noises and not generalize well. Even very small changes to independent variables may cause a misclassification. SVM is especially effective in cases where the number of dimensions is more than the number of samples. When finding the decision boundary, SVM uses a subset of training points rather than all points, which makes it memory efficient. On the other hand, training time increases for large datasets, which negatively affects the performance.

## Naive Bayes

Naive Bayes is a supervised learning algorithm used for classification tasks. Hence, it is also called Naive Bayes classifier. Naive Bayes assumes that features are independent of each other and there is no correlation between features. However, this is not the case in real life. This naive assumption of features being uncorrelated is the reason why this algorithm is called Naive. The intuition behind Naive Bayes algorithm is the Bayes theorem. PAB is the probability of event A given event B has already occurred. PBA is the probability of event B given event A has already occurred. PA is the probability of event A and PB is the probability of event B. Naive Bayes classifier calculates the probability of a class given a set of feature values. The assumption that all features are independent makes Naive Bayes algorithm very fast when compared to complicated algorithms. In some cases, speed is preferred over higher accuracy. But on the other hand, the same assumption makes Naive Bayes algorithm less accurate than complicated algorithms.

## Logistic Regression

Logistic regression is a supervised learning algorithm which is mostly used for binary classification problems. Logistic regression is a simple yet very effective classification algorithm so it is commonly used for many binary classification tasks. Things like customer churn, spam email, website, or ad click predictions are some examples of the areas where logistic regression offers a powerful solution. The basis of logistic regression is the logistic function also called the sigmoid function which takes any real value number and maps it to a value between 0 and 1. Let's consider we have the following linear equation to solve. Logistic regression model takes a linear equation as input and uses logistic function and log odds to perform a binary classification task. Then we will get the famous shaped graph of logistic regression. We can use the calculated probability as is. For example, the output can be the probability that this email is spam is 95% or the probability that the customer will click on the ad is 70%. However, in most cases, probabilities are used to classify data points. For example, if the probability is greater than 50%, the prediction is positive class or 1. Otherwise, the prediction is negative class or 0.

## K-Nearest Neighbors (KNN)

K-Nearest Neighbors or KNN for short is a supervised learning algorithm that can be used to solve both classification and regression tasks. The main idea behind KNN is that the value of a class or of a data point is determined by the data points around it. KNN classifier determines the class of a data point by majority voting principle. For instance, if K is set to 5, the classes of 5 closest points are checked. Prediction is done according to the majority class. Similarly, KNN regression takes the mean value of 5 closest points. Let's go over an example. Consider the following data points that belong to 4 different classes. And let's see how the predicted classes change according to the K value. It is very important to determine an optimal K value. If K is too low, the model is too specific and not generalized well. It also tends to be too sensitive to noise. The model accomplishes a high accuracy on train set, but will be a poor predictor on new, previously unseen data points. Therefore, we are likely to end up with an overfit model. On the other hand, if K is too large, the model is too generalized and is not a good predictor on both train and test sets. This situation is known as underfitting. KNN is simple and easy to interpret. It does not make any assumptions, so it can be implemented in non-linear tasks. KNN does become very slow as the number of data points increases because the model needs to store all data points. Thus, it is not memory efficient. Another downside of KNN is that it is sensitive to outliers.

## Decision Trees

Decision trees work by iteratively asking questions to partition data. It is easier to conceptualize the partitioning data with a visual representation of a decision tree. This represents a decision tree to predict customer churn. First split is based on monthly charges amount, then the algorithm keeps asking questions to separate class labels. The questions get more specific as the tree gets deeper. The aim is to increase the predictiveness as much as possible at each partitioning so that the model keeps gaining information about the dataset. Randomly splitting the feature does not usually give us the valuable insight into the dataset. It's the splits that increase the purity of nodes that are most informative. The purity of a node is inversely proportional to the distribution of different classes in that node. The questions to ask are chosen in a way that increases purity or decreases impurity. But how many questions do we ask? When do we stop? When is our tree sufficient to solve our classification problem? The answer to all of these questions leads us to one of the most important concepts in machine learning, overfitting. The model can keep asking questions until all nodes are pure. However, this would be a too specific model and would not generalize well. It achieves high accuracy with the training set, but performs poorly on new, previously unseen data points which indicates overfitting. Decision tree algorithm usually does not require to normalize or scale features. It is also suitable to work on a mixture of feature data types. On the negative side, it is prone to overfitting and needs to be ensembled in order to generalize well.

## Random Forest

Random forest is an ensemble of many decision trees. Random forests are built using a method called bagging in which decision trees are used as parallel estimators. If used for a classification problem, the result is based on the majority vote of the results received from each decision tree. For regression, the prediction of a leaf node is the mean value of the target values in that leaf. Random forest regression takes mean values of results from decision trees. Random forests reduce the risk of overfitting and accuracy is much higher than a single decision tree. Furthermore, decision trees in a random forest run in parallel so that the time does not become a bottleneck. The success of a random forest highly depends on using uncorrelated decision trees. If we use the same or very similar trees, the overall result will not be much different than the result of a single decision tree. Random forests achieve to have uncorrelated decision trees by bootstrapping and feature randomness. Bootstrapping is randomly selecting samples from training data with replacement. They are called bootstrap samples. Feature randomness is achieved by selecting features randomly for each decision tree in a random forest. The number of features used for each tree in a random forest can be controlled with max underscore features parameter. Random forest is a highly accurate model on many different problems and does not require normalization or scaling. However, it is not a good choice for high dimensional data sets compared to fast linear models.

## Gradient Boosted Decision Trees (GBDT)

Gradient Boosted Decision Trees or GBDT for short is an ensemble algorithm which uses boosting methods to combine individual decision trees. Boosting means combining a learning algorithm in series to achieve a strong learner from many sequentially connected weak learners. In the case of GBDT, the weak learners are the decision trees. Each tree attempts to minimize the errors of the previous tree. Trees in boosting are weak learners, but adding many trees in series and each focusing on the errors from the previous one make boosting a highly efficient and accurate model. Unlike bagging, boosting does not involve bootstrap sampling. Every time a new tree is added, it fits on a modified version of the initial data set. Since trees are added sequentially, boosting algorithms learn slowly. In statistical learning, models that learn slowly perform better. GBDT is very efficient on both classification and regression tasks and provides more accurate predictions compared to random forests. It can handle mixed type of features and no preprocessing is needed. GBDT does require careful tuning of hyperparameters in order to prevent the model from overfitting.

## K-Means Clustering

K means clustering. Clustering is a way to group a set of data points in a way that similar data points are grouped together. Therefore, clustering algorithms look for similarities or dissimilarities among data points. Clustering is an unsupervised learning method, so there is no label associated with data points. Clustering algorithms try to find the underlying structure of the data. Observations or data points in a classification task have labels. Each observation is classified according to some measurements. Classification algorithms try to model the relationship between measurements on observations and their assigned class. Then the model predicts the class of new observations. K means clustering aims to partition data into k clusters in a way that data points in the same cluster are similar and data points in different clusters are further apart. Thus, it is a partition-based clustering technique. Similarity of two points is determined by the distance between them. Consider the following 2D visualization of a dataset. It can be partitioned into four different clusters. Now, real-life datasets are much more complex in which clusters are not clearly separated. However, the algorithm works in the same way. K means is an iterative process. It is built on expectation maximization algorithm. After the number of clusters are determined, it works by executing the following steps. Number one, it randomly selects the centroids or the center of cluster for each cluster. Then it calculates the distance of all data points to the centroids. It assigns the data points to the closest cluster. It finds the new centroids of each cluster by taking the mean of all data points in the cluster. And it repeats steps two, three, and four until all points converge and cluster centers stop moving. K means clustering is relatively fast and easy to interpret. It is also able to choose the positions of initial centroids in a smart way that speeds up the convergence. The one challenge with K-means is that the number of clusters must be predetermined. K-means algorithm is not able to guess how many clusters exist in the data. If there is a non-linear structure separating groups in the data, K-means will not be a good choice.

## DBSCAN Clustering

DBSCAN clustering. Partition-based and hierarchical clustering techniques are highly efficient with normal-shaped clusters. However, when it comes to arbitrary-shaped clusters or detecting outliers, density-based techniques are more efficient. DBSCAN stands for density-based spatial clustering of applications with noise. It is able to find arbitrary-shaped clusters and clusters with noise. The main idea behind DBSCAN is that a point belongs to a cluster if it is close to many points from that cluster. There are two key parameters of DBSCAN. EPS, which is the distance that specifies the neighborhoods. Two points are considered to be neighbors if the distance between them are less than or equal to EPS. And minPTS, which is the minimum number of data points to define a cluster. Based on these two