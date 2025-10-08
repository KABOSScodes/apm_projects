# Chapter Notes
The attempt with this file is to abbreviate the learnings and procedures from the chapters as further assistance in future endeavors. 

This file will be gradually developed in parallel with the assignments from Chapter 3 onwards, while notes from Chapters 1 and 2 will be added at a later stage.

## Chapter 3: Over-Fitting and Model Tuning
### Data splitting
The base R function **sample** can create simple random splits of the data. To create stratified random splits of the data (based on the classes), the **createDataPartition** function in the **caret** package can be used. The percent of data that will be allocated to the training set should be specified.

When creating stratified splits, the seed should be set to ensure results are reproducible. 

To generate a test set using **maximum dissimilarity sampling**, the caret function **maxdissim** can be used to sequentially sample the data.

| Sampling              | Notes |
|------------------------|-------|
| Random splits                | Each sample is chosen by chance, giving all data points an equal probability of selection. |
| Stratified random splits            | Data is divided into groups (strata), and samples are taken from each group to preserve proportional representation. |
| Maximum Dissimilarity  | Samples are chosen to be as different from each other as possible, ensuring wide coverage of the data space. |

**In R**

classes: Outcome vector

predictors: Matrix with 2 columns. 1 for each predictor of the class.

```r
> set.seed(1)
> trainingRows <- createDataPartition(classes, p = .80, list = FALSE)
# p = .80 sets percent allocated to training set.
# list = FALSE: a matrix of row numbers is generated. These samples are allocated to the training set.

> head(trainingRows)
       Resample1
[1,]          99
[2,]         100
[3,]         101
[4,]         102
[5,]         103
[6,]         104

# Subset the data into objects for training using integer sub-setting.
> trainPredictors <- predictors[trainingRows, ]
> trainClasses <- classes[trainingRows]
# Do the same for the test set using negative integers.
> testPredictors <- predictors[-trainingRows, ]
> testClasses <- classes[-trainingRows]

> str(trainPredictors)
   'data.frame': 167 obs. of 2 variables:
   $ PredictorA: num 0.226 0.262 0.52 0.577 0.426 ... 
   $ PredictorB: num 0.291 0.225 0.547 0.553 0.321 ...

> str(testPredictors)
   'data.frame': 41 obs. of 2 variables:
   $ PredictorA: num 0.0658 0.1056 0.2909 0.4129 0.0472 ... 
   $ PredictorB: num 0.1786 0.0801 0.3021 0.2869 0.0414 ...
```

**In Python**
```python
X_train, X_test, y_train, y_test = train_test_split(
    X, y, 
    train_size=0.8, 
    random_state=1,   # same as set.seed(1)
    stratify=y        # ensures class proportions are preserved
)
```

### Resampling
The caret package has various functions for data splitting. For example, to use repeated training/test splits, the function createDataPartition could be used again.

```r
> set.seed(1)
> repeatedSplits <- createDataPartition(trainClasses, p = .80, times = 3)

> str(repeatedSplits)
List of 3
$ Resample1: int [1:135] 1 2 3 4 5 6 7 9 11 12 ...
$ Resample2: int [1:135] 4 6 7 8 9 10 11 12 13 14 ... $ Resample3: int [1:135] 2 3 4 6 7 8 9 10 11 12 ...
```

| Function             | Purpose / Description |
|----------------------|---------------------|
| `createDataPartition` | Creates training/test splits. Can generate repeated splits using the `times` argument. |
| `createResamples`     | Generates bootstrap resamples of the dataset. |
| `createFolds`         | Creates indices for k-fold cross-validation. |
| `createMultiFolds`    | Creates indices for repeated k-fold cross-validation. |

**Example**
```r
> set.seed(1)
> cvSplits <- createFolds(trainClasses, k = 10, returnTrain = TRUE)
> str(cvSplits)
  List of 10
   $ Fold01: int [1:151] 1 2 3 4 5 6 7 8 9 11 ...
   $ Fold02: int [1:150] 1 2 3 4 5 6 8 9 10 12 ...
   $ Fold03: int [1:150] 1 2 3 4 6 7 8 10 11 13 ...
   $ Fold04: int [1:151] 1 2 3 4 5 6 7 8 9 10 ...
   $ Fold05: int [1:150] 1 2 3 4 5 7 8 9 10 11 ...
   $ Fold06: int [1:150] 2 4 5 6 7 8 9 10 11 12 ...
   $ Fold07: int [1:150] 1 2 3 4 5 6 7 8 9 10 ...
   $ Fold08: int [1:151] 1 2 3 4 5 6 7 8 9 10 ...
   $ Fold09: int [1:150] 1 3 4 5 6 7 9 10 11 12 ...
   $ Fold10: int [1:150] 1 2 3 5 6 7 8 9 10 11 ...
# Get the first set of row numbers from the list.
> fold1 <- cvSplits[[1]]
