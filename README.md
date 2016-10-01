# Generic Decision Tree

This is the implementation for a generic decision tree using greedy method where the most important attribute is checked first for arriving to a decision. The importance of an attribute is decided on the basis of the 'information gain' heuristic and uses entropy to find it.

The algorithm uses the n-fold cross validation technique to train and test the data sets. Two sample datasets are included.

Input data file is in the csv format, where the first row is the name of attributes and the last column of each row is the decision made.
Accuracy for each of the folds and average accuracy over n-folds is displayed.
