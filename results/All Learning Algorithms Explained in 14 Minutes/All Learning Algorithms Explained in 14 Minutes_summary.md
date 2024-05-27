## Summary

Machine learning algorithms, each with unique strengths and weaknesses, are designed to solve specific types of problems, ranging from regression and classification to clustering and dimensionality reduction.

## Key takeaways

1. **Linear Regression**: Models the relationship between a continuous target variable and one or more independent variables by fitting a linear equation to the data, minimizing the sum of squares of the distance between data points and the regression line.

2. **Support Vector Machine (SVM)**: Primarily used for classification tasks, SVM draws a decision boundary in n-dimensional space to distinguish classes, maximizing the distance to support vectors to avoid sensitivity to noise.

3. **Naive Bayes**: Assumes features are independent and uses Bayes theorem to calculate the probability of a class given a set of feature values. It is very fast but less accurate due to its naive assumption of feature independence.

4. **Logistic Regression**: Used for binary classification problems, logistic regression maps any real value number to a value between zero and one using the logistic function, making it effective for tasks like spam detection and customer churn prediction.

5. **K-Nearest Neighbors (KNN)**: Determines the class of a data point based on the majority class of its nearest neighbors. It is simple and non-parametric but becomes slow and memory-inefficient with large datasets.

6. **Decision Trees**: Partition data by iteratively asking questions to increase node purity. They are easy to visualize and interpret but prone to overfitting, requiring ensemble methods like random forests to generalize well.

7. **Random Forest**: An ensemble of decision trees using bagging, which reduces overfitting and increases accuracy. It runs trees in parallel and uses bootstrapping and feature randomness to ensure uncorrelated trees.

8. **Gradient Boosted Decision Trees (GBDT)**: Combines decision trees in series to minimize errors from previous trees, making it highly efficient and accurate. It requires careful tuning of hyperparameters to prevent overfitting.

9. **K-Means Clustering**: Partitions data into K clusters by iteratively assigning data points to the nearest centroid and recalculating centroids. It is fast and easy to interpret but requires the number of clusters to be predetermined.

10. **DBSCAN Clustering**: A density-based method that can find arbitrary-shaped clusters and detect outliers. It classifies points as core, border, or outliers based on neighborhood distance (EPS) and minimum points (minPTS).