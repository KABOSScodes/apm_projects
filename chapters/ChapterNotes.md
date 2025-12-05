# Chapter Notes
The attempt with this file is to abbreviate the learnings and procedures from the chapters as further assistance in future endeavors. 

This file will be gradually developed in parallel with the assignments from Chapter 4 onwards, while notes from Chapters 1, 2, and 3 will be added at a later stage.

## Chapter 4: Over-Fitting and Model Tuning
### 4.1 Data Splitting

Data splitting defines how to create independent subsets for model development and evaluation.  
Choice of splitting method depends on the characteristics of the dataset (e.g., classification vs regression and/or independence of samples).

> With all splitting, it is crucial to set the seed number to ensure reproducibility.

---

#### Data Splitting Recommendations

Obtained from book section 4.7:

There is a strong technical case to be made against using a single, independent test set:

- A test set is a single evaluation of the model and has limited ability to characterize the uncertainty in the results.  
- Proportionally large test sets divide the data in a way that increases bias in the performance estimates (due to less available data for training).  
- With small sample sizes:
  - The model may need every possible data point to adequately determine model values.  
  - The uncertainty of the test set can be considerably large to the point where different test sets may produce very different results.  
- Resampling methods can produce reasonable predictions of how well the model will perform on future samples.

---

#### Identify Data Characteristics
When deciding how to split or resample, check:

- Is the target class of categorical type and are classes equally prominent (classification)?
- Is the **target distribution** imbalanced?
- Are samples **independent**, or grouped/repeated?
- Is there **temporal order** (not introduced in this chapter)?

Grouped or "repeated" samples mean multiple observations that belong together logically — e.g.:

- Several measurements from the same patient (grouped)
- Multiple tests on the same experimental batch (grouped)
- Replicate experiments (repeated)

If you split such data randomly, you could end up training on some repeats and testing on others -> data leakage.

---

#### Train/test Split Strategy Selection (Initial split)

| Data Characteristics | Recommended Split | R (`caret`) | Python (`scikit-learn`) | Notes |
|----------------------|------------------|--------------|--------------------------|-------|
| Independent samples, non-categorical target | Simple random split | `sample` | `train_test_split()` | Default case. See additional notes below. |
| Independent samples, categorical target | Stratified split | `createDataPartition` | `train_test_split(..., stratify=y)` | Preserves class ratios. See additional notes below. |
| Grouped or repeated samples | Grouped split | `group_vfold_cv()` (via `rsample`) or custom | `GroupShuffleSplit` | Keep related samples together |
| Grouped samples + imbalanced classes | Stratified grouped split | Custom implementation in R | `StratifiedGroupKFold()` | Preserve group integrity and class proportions in train/test split. |
| Time-ordered data | Time-series split | `createTimeSlices` | `TimeSeriesSplit()` | Avoid future leakage |
| Want diverse test set covering edge cases|Max dissimilarity sampling | `maxdissim()` | No equivalent in python | Selects most dissimilar samples from training set based on predictors |


> If classes are evenly prevalent and samples are independent, a random split can technically be used instead of a stratified split.

> Stratified splits can also be used for numerical targets by binning the continuous target variable into quantiles or intervals and then stratifying based on those bins. However, stratification is most relevant with categorical targets.

---

#### Resampling Methods (Overview)

| Method | Description | Recommended Use / Key Considerations |
|--------|-------------|------------------------------------|
| **Monte Carlo / Repeated Random Splits** | Perform repeated random train/test splits with a fixed proportion (e.g., 80/20). | Flexible split ratio; fewer model fits than repeated k-fold CV; quick exploratory validation but higher variance and uneven sample coverage. |
| **Repeated Stratified Split** | Same as Monte Carlo CV but preserves class proportions in target variable. | Same as Monte Carlo CV but preserves class proportions in target variable. |
| **Bootstrap** | Random sampling *with replacement* to create resamples the same size as the original dataset. | Good for **model comparison** when variance should be low |
| **k-Fold Cross-Validation** | Split data into *k* folds; train on *k−1*, validate on the remaining fold. | Standard choice for model evaluation and tuning; use **10-fold** for small to medium datasets. |
| **Repeated k-Fold CV** | Repeat k-fold CV multiple times with different random partitions. | Recommended for **small sample sizes** to reduce variance; balances bias and variance. |
| **Leave-One-Out CV (LOOCV)** | Special case of k-fold where *k = n*. | Very small datasets; high computational cost; maximizes training data. |

> **Choosing a Resampling Method (Kuhn & Johnson)**  
> - No method is uniformly best; consider sample size, purpose, and computation.  
> - **Small datasets:** repeated 10-fold CV — good bias–variance balance, manageable cost.  
> - **Model comparison:** bootstrap — low variance in performance estimates.  
> - **Large datasets:** differences between methods are minor; 10-fold CV is efficient and generally sufficient.

---

### 4.2 Splitting/Resampling implementations
#### Stratified Splits
**Language: R**

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

**Language: Python**
```python
X_train, X_test, y_train, y_test = train_test_split(
    X, y, 
    train_size=0.8, 
    random_state=1,   # same as set.seed(1)
    stratify=y        # ensures class proportions are preserved
)
```

#### Resampling
The caret package has various functions for data splitting. For example, to use repeated training/test splits, the function createDataPartition could be used again.

```r
> set.seed(1)
> repeatedSplits <- createDataPartition(trainClasses, p = .80, times = 3)

> str(repeatedSplits)
  List of 3
   $ Resample1: int [1:135] 1 2 3 4 5 6 7 9 11 12 ...
   $ Resample2: int [1:135] 4 6 7 8 9 10 11 12 13 14 ... 
   $ Resample3: int [1:135] 2 3 4 6 7 8 9 10 11 12 ...
```

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

# To get the first 90 % of the data (the first fold):
> cvPredictors1 <- trainPredictors[fold1,]
> cvClasses1 <- trainClasses[fold1]
> nrow(trainPredictors)
[1] 167
> nrow(cvPredictors1)
[1] 151
```

**Sampling Summary**
| Function in R (`caret`) | Python Equivalent (`scikit-learn`) | Purpose / Description |
|--------------------------|------------------------------------|------------------------|
| `sample` | `train_test_split()` | Creates simple random training/test splits without stratification. |
| `createDataPartition` | `train_test_split(..., stratify=y)` | Creates **stratified** training/test splits to preserve class proportions. The `times` argument for the R function allows generation of repeated random splits (Monte Carlo cross-validation). |
| `createResamples` | `sklearn.utils.resample()` | Generates **bootstrap resamples** (sampling with replacement) to estimate model variability or confidence intervals. Each resample is the same size as the original data. |
| `createFolds` | `KFold()` / `StratifiedKFold()` | Creates indices for **k-fold cross-validation**. Data are split into *k* parts, training occurs on *k−1* folds, and validation on the remaining one. Stratified variants preserve class balance. |
| `createMultiFolds` | `RepeatedKFold()` / `RepeatedStratifiedKFold()` | Creates indices for **repeated k-fold cross-validation**, repeating the k-fold process multiple times with different random partitions for more stable performance estimates. |

There is also LOOCV which fits as many models as there are samples in the training set. This should only be considered when number of samples is very small. 

### Choosing Tuning Parameters
**Book: Section 4.6**
> "The “one-standard error” method for choosing simpler models finds the numerically optimal value and its corresponding standard error and then seeks the simplest model whose performance is within a single standard error of the numerically best value. This procedure originated with classification and regression trees (Breiman et al. (1984) and Sects. 8.1 and 14.1). In Fig. 4.10, the standard error of the accuracy values when the cost is 8 is about 0.7 %. This technique would find the simplest tuning parameter settings associated with accuracy no less than 74.3 % (75 %–0.7 %). This procedure would choose a value of 2 for the cost parameter."

> "Another approach is to choose a simpler model that is within a certain tolerance of the numerically best value. The percent decrease in performance could be quantified by (X − O)/O where X is the performance value and O is the numerically optimal value. For example, in Fig. 4.9, the best accuracy value across the profile was 75 %. If a 4 % loss in accuracy was acceptable as a trade-off for a simpler model, accuracy values greater than 71.2% would be acceptable. For the profile in Fig.4.9, a cost value of 1 would be chosen using this approach."

### Choosing Between Models
**Book: Section 4.8**
> 1. Start with several models that are the least interpretable and most flexible, such as boosted trees or support vector machines. Across many problem domains, these models have a high likelihood of producing the empirically optimum results (i.e., most accurate).
> 2. Investigate simpler models that are less opaque (e.g., not complete black boxes), such as multivariate adaptive regression splines (MARS), partial least squares, generalized additive models, or na ̈ıve Bayes models.
> 3. Consider using the simplest model that reasonably approximates the per- formance of the more complex methods.

## Chapter 5: Measuring Performance in Regression Models
### 4.1 Data Splitting
To understand the strengths and weaknesses of a particular model, relying solely on a sin- gle metric is problematic. Visualizations of the model fit, particularly residual plots, are critical to understanding whether the model is fit for purpose.