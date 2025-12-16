# Chapter Notes
The attempt with this file is to abbreviate the learnings and procedures from the chapters as further assistance in future endeavors. 

This file will be gradually developed in parallel with the assignments from Chapter 4 onwards, while notes from Chapters 1, 2, and 3 will be added at a later stage.

## Chapter 4: Over-Fitting and Model Tuning
### 4.1 Data Splitting

Data splitting defines how to create independent subsets for model development and evaluation.  
Choice of splitting method depends on the characteristics of the dataset (e.g., classification vs regression and/or independence of samples).

> "With all splitting, it is crucial to set the seed number to ensure reproducibility."

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

When assessing the strengths and weaknesses of a model, a mix of performance metrics and plots (particularly residual plots) can/should be used to evaluate if the model truly is a good fit for its intended purpose.

### Metrics

---

#### Mean squared error - MSE

The mean squared error is calculated as the sum of the squared residuals (observed values minus predicted values): 

$$
\text{MSE} = \frac{1}{n} \sum_{i=1}^n (y_i - \hat{y}_i)^2
$$

---

#### Root mean squared error - RMSE

When the outcome is a number, the most common metric for evaluation of the model's predictive capabilities is the root mean squared error (RMSE), which is a function of the residuals. 

$$
\text{RMSE} = \sqrt{MSE} = \sqrt{\frac{1}{n} \sum_{i=1}^n (y_i - \hat{y}_i)^2}
$$

---

#### Coefficient of determination - R2

The coefficient of determination is another metric that is widely used (and often misused). It can be interpreted as:

> "the proportion of the information in the data that is explained by the model"

It is important to note, that R2 is a measure of the correlation - not accuracy. A common phenomenon with some tree-based methods is overprediction of low values and underprediction of high values. In such cases R2 needs to be used with caution, but such a systematic bias in the predictions may be acceptable if the model otherwise works.

Likewise, it should be noted that R2 is dependent on the outcome variation as seen below. Thus, two models can have the exact same RMSE, but differences in the variance of the outcome values may result in one model performing better than the other according to R2.

There are many formulas for calculating R2. It can be expressed in terms of MSE and the variance: 

$$
R^2 = 1 - \frac{MSE}{Var(y)}
$$

The simplest version simply squares the correlation coefficient:

$$
R^2 = r^2
$$

The correlation coefficient can be calculated from Pearson's formula.

**Pearson's correlation coefficient - Conceptual Formula**
* Numerator = covariance
* Denominator = product of standard deviations
* Slow computation

$$
r = \frac{\sum_{i=1}^n (x_i - \bar{x})(y_i - \bar{y})}{\sqrt{\sum_{i=1}^n (x_i - \bar{x})^2}\,\sqrt{\sum_{i=1}^n (y_i - \bar{y})^2}}
$$

**Pearson's correlation coefficient - Computational shortcut**

$$
\[
r = \frac{n \sum x y - (\sum x)(\sum y)}
{\sqrt{\left[ n \sum x^2 - (\sum x)^2 \right] \left[ n \sum y^2 - (\sum y)^2 \right]}}\]
$$

**Spearman's rank correlation**

In some cases, such as with biological activity of drugs, it may be sufficient, or even better, for a model to simply rank new samples. Spearman's rank correlation can be used in for this purpose.

> "The rank correlation takes the ranks of the observed outcome values (as opposed to their actual numbers) and evaluates how close these are to ranks of the model predictions. To calculate this value, the ranks of the observed and predicted outcomes are obtained and the correlation coefficient between these ranks is calculated."

---

### Variance-Bias Trade-off

Under the assumption that data points are statistically independent with a theoretical mean of zero and a constant variance of $\sigma^2$, the following applies:

$$
E[MSE] = \sigma^2 + (Model Bias)^2 + Model Variance
$$

- E: The expected value
- $\sigma^2$: Irreducible noise. Cannot be eliminated through modeling
- $(Model Bias)^2$: How close the model can get to the true relationship between predictors and outcome.
- $Model Variance$: Vulnerability towards small pertubations in the data. 

Highly correlated predictors can lead to collinearity issues. Bias of a model can be increased to reduce variance as a way to mitigate this issue. This is the variance-bias trade-off.

---

## Chapter 6: Linear Regression and Its Cousins

Linear regression and its cousins concerns models all of which can directly or indirectly be written in the form

$$
y_i = b_0 + b_{1}x_{i1} + b_{2}x_{i2} + ... + b_{P}x_{iP} + e_i
$$

where

- $y_i$: Numeric response for the ith sample
- $b_j$: Estimated coefficient for the jth predictor
- $x_{ij}$: Value of the jth predictor for the ith sample
- $e_i$: Random error that cannot be explained by the model

This makes them highly interpretable, but they are mainly useful when the relationship between the predictors and the response falls along a hyperplane. Linear regression models can be augmented in case the relation between predictors is curvilinear (quadratic, cubic, interactions between predictors), 
If the relation between predictors and response is curvelinear (quadratic, cubic, interactions between predictors), one can attempt to augment the linear models by adding predictors that are functions of original predictors, but such augmentations may not always be enough to capture non-linear relationships.

A model in the above form is said to be linear in its parameters. Models linear in their parameters include:

- Ordinary linear regression
- Partial Least Squares (PLS)
- Penalized models:
   - Ridge regression
   - The lasso
   - The elastic net

These models attempt to find the set of parameters the minimizes the sum of the squared errors or a function thereof. 

---

### Case Study: Quantitative Structure-Activity Relationship modeling

> "We will demonstrate various regression modeling techniques by predicting solubility using chemical structures."

> "Tetko et al. (2001) and Huuskonen (2000) investigated a set of compounds with corresponding experimental solubility values using complex sets of descriptors. They used linear regression and neural network models to estimate the relationship between chemical structure and solubility. For our analyses, we will use 1,267 compounds and a set of more understandable descriptors that fall into one of three groups:
> * Twohundredandeight binary “fingerprints” that indicate the presence or absence of a particular chemical substructure.
> * Sixteen count descriptors, such as the number of bonds or the number of bromine atoms.
> * Four continuous descriptors, such as molecular weight or surface area."

> "On average, the descriptors are uncorrelated. However, there are many pairs that show strong positive correlations; 47 pairs have correlations greater than 0.90. In some cases, we should expect correlations between descriptors. In the solubility data, for example, the surface area of a compound is calculated for regions associated with certain atoms (e.g., nitrogen or oxygen). One descriptor in these data measures the surface area associated with two specific elements while another uses the same elements plus two more. Given their definitions, we would expect that the two surface area predictors would be correlated. In fact, the descriptors are identical for 87 % of the compounds. The small differences between surface area predictors may contain some important information for prediction, but the modeler should realize that there are implications of redundancy on the model. Another relevant quality of the solubility predictors is that the count-based descriptors show a significant right skewness, which may have an impact on some models."

**Data splitting**

> "The data were split using random sampling into a training set (n = 951) and test set (n = 316). The training set will be used to tune and estimate models, as well as to determine initial estimates of performance using repeated 10-fold cross-validation. The test set will be used for a final characterization of the models of interest."

**Pre-processing**

Fingerprint descriptors:

> "Recall that 208 of the predictors are binary fingerprints. Since there are only two values of these variables, there is very little that pre-processing will accomplish."

Skewness of continuous descriptors:

> "The average skewness statistic was 1.6 (with a minimum of 0.7 and a maximum of 3.8), indicating that these predictors have a propensity to be right skewed. To correct for this skewness, a Box–Cox transformation was applied to all predictors (i.e., the transformation parameter was not estimated to be near one for any of the continuous predictors)."

**Linearity**

> "Figure 6.3 shows scatter plots of the predictors against the outcome along with a regression line from a flexible “smoother” model called loess (Cleveland 1979). The smoothed regression lines indicate that there are some linear relationships between the predictors and the outcome (e.g., molecular weight) and some nonlinear relationships (e.g., the number of origins or chlorines). Because of this, we might consider augmenting the predictor set with quadratic terms for some variables."

**Between-predictor correlations**

> "principal component analysis (PCA) was used on the full set of trans- formed predictors, and the percent of variance accounted for by each component is determined. Figure 6.4 is commonly known as a scree plot and displays a profile of the variability accounted for by each component. Notice that the amount of variability summarized by component drops sharply, with no one component accounting for more than 13 % of the variance. This profile indicates that the structure of the data is contained in a much smaller number of dimensions than the number of dimensions of the original space; this is often due to a large number of collinearities among the predictors."

> "Figure 6.5 shows the correlation structure of the transformed continuous predictors; there are many strong positive correlations (indicated by the large, dark blue circles). As previously discussed, this could create problems in developing some models (such as linear regression), and appropriate pre-processing steps will need to be taken to account for this problem."

---

#### Linear Regression

\uline{Model definition}

Ordinary linear regression attempts to find the plane that minimizes the sum of squared errors (SSE):

$$
SSE = \sum_{i=1}^n (y_i - \hat{y}_i)^2
$$

where

- $y_i$: Outcome for the ith sample
- $\hat{y}_i$: Predicted outcome for the ith sample

The mathematically optimal plane can be shown to be:

$$
(\mathbf{X}^\top \mathbf{X})^{-1} \mathbf{X}^\top y
$$

- $\mathbf{X}$: Descriptor matrix, Design matrix
- y: Response vector

Making minimal assumptions about the distribution of the residuals, the parameter estimates that minimize SSE are the ones that minimize the bias of the bias-variance trade-off.

---

\uline{Model need-to-know}

$(\mathbf{X}^\top \mathbf{X})^{-1}$ is proportional to the covariance matrix of the predictors. A unique invers ONLY exists when:

1. No predictor can be determined from a combination of one or more of the other predictors
2. The number of samples is greater than the number of predictors

If the data falls under condition 1, a unique set of predicted values can still be obtained by

- replacing $(\mathbf{X}^\top \mathbf{X})^{-1}$ with a conditional inverse (Graybill 1976)
- removing predictors that are collinear

But, since the regression coefficients are not unique, it is not possible to meaningfully interpret them.

If the data falls under condition 2, there are still several options:

- Remove pairwise correlated predictors, which will reduce the number of overall predictors
- Diagnose multicollinearity (predictors may be functions of two or more of the other predictors) using the variance inflation factor (Myers 1994)
- PCA 
- PLS
- Employ methods that shrink parameter estimates such as ridge regression, the lasso, or the elastic net

---

Another drawback of multiple linear regression is that the solution is a flat hyperplane. The Predicted-vs-residual plot of Fig. 5.3 is a great way of visually investigating if the relationships are non-linear. Curvature in the plot strongly indicates that the underlying relationship is not linear. Quadratic, cubic, or predictor interactions can be accomodated by adding quadratic, cubic, or interaction predictors (feature engineering), but this is not always a practical solution.

If it is not possible to determine the non-linear predictor-response relationships, or the relationships are simply too non-linear, more complex methods may be required.

---

Linear regression models are prone to chase outliers. 

> "Recall that linear regression seeks to find the parameter estimates that minimize SSE; hence, observations that are far from the trend of the majority of the data will have exponentially large residuals."

Such observation are called influential. One way to address this issue is to exchange the SSE metric for one less sensitive to large outliers. SSE alternatives:

- Sum of the absolute errors is more resistant to outliers
- The Huber function uses the squared errors when they are below a certain threshold and the absolute errors when above it

---

When collinearity exists in the data set, the regression model may become instable (see example p. 110-111). For pairwise collinearity, one of the offending predictors may be removed. However, if the number of predictors is large, this may be difficult, and if the collinearity involves multiple predictors, the interactions may be too complex, in which case a different model should be considered.

---

#### Partial Least Squares

As previously stated, there are two common pitfalls with linear regression:

1. Correlation between predictors results in the ordinary least squares solution for multiple linear regression becoming unstable due to high variability
2. Number of predictors greater than number of observations means that ordinary least squared will be unable to find a unique solution in its usual form that minimizes SSE.

Using PCA for pre-processing ensures resulting predictors or combinations thereof are uncorrelated. The downside is that resulting predictors are linear combinations of the originals, meaning the interpretability becomes less obvious. 

Performing regression on components from PCA is known as principal component regression, **PCR**. While this is a solid approach to regression, it is not without potential pitfalls, as the components don't necessarily explain the response.

> "Because of this inherent problem with PCR, we recommend using PLS when there are correlated predictors and a linear regression-type solution is desired."

---

$\uline{Model definition}$

While PCA components are made to maximally summarize the predictor space variability, PLS components are made to maximally summarize covariance with the response.

> PLS finds linear combinations of the predictors. These linear combinations are commonly called components or latent variables. While the PCA linear combinations are chosen to maximally summarize predictor space variability, the PLS linear combinations of predictors are chosen to maximally summarize covariance with the response.

In practice, PCR performs similar to PLS, but based on the experiences of the authors:

> "the number of components retained via cross-validation using PCR is always equal to or greater than the number of components retained by PLS. This is due to the fact that dimensions retained by PLS have been chosen to be optimally related to the response, while those chosen with PCR are not."

Through Variable Importance in the Projection calculations, the importance of predictors wrt predicting the response can be determined. This calculation was developed by Wold et al. (1993). They go further and suggest that "predictors with small PLS regression coefficients and small VIP values are likely not important and should be considered as candidates for removal from the model."

---

$\uline{Model need-to-know}$

Prior to performing PLS, the predictors should be centered and scaled, especially if the predictors are on scales of differing magnitude. In spite of the constraint of correlation with the response, predictors with large variation may skew the regression.

PLS may be prone to inefficiency when n > 2500 and P > 30.

---

$\uline{Algorithmic Variations of PLS}$

Lindgren et al. (1993) developed an alternative computation approach to address the inefficiency in computing. They leveraged:

1. A "kernel" matrix, P × P
2. The covariance matrix of the predictors, P × P
3. The covariance matrix of the predictors and response, P × 1

This was especially effective when n >> P.

Likewise, de Jong (1993) improved the algorithm's inefficiency issues by viewing the underlying task as "finding latent orthogonal variables in the predictor space that maximize the covariance with the response". This meant focusing on deflating the covariance matrix between predictors and response rather than deflating the predictor matrix AND the response. This approach was termed SIMPLS, as it was a "simple modification of the PLS algorithm".

When there is only one response variable, SIMPLS latent variables were shown to be identical to those of the NIPALS algorithm on which PLS is based.

Dayal and MacGregor (1997) developed two modifications to the NIPALS algorithm, which especially performed when n >> P. As with SIMPLS, their modifications only require the deflated covariance matrix. Alin (2009) compared algorithmic modifications to NIPALS with varying number of samples (500–10,000), predictors (10–30), and responses (1–15). The second kernel algorithm of Dayal and MacGregor was more computationally efficient than all other approaches in nearly all scenarios and provided superior performance when n > 2, 500 and P > 30. When their second algorithm was not the most efficient, their first was. 

Rännar et al. (1994) adressed the case where P > n by constructing a n x n dimensional matrix based on the predictor and response matrices. A usual PLS analysis can then be performed on the n x n matrix. 

Modifications have been developed to capture curvilinear and non-linear relationships:

- Berglund and Wold (1997): Added squared and cubic (if necessary) predictors
- Berglund et al. (2001): Binned predictors according to the GIFI approach

Due to the considerable amount of effort in constructing the new predictor sets, Kuhn & Johnson do not recommend relying PLS to capture intricate predictor-response structures.

---

#### Penalized Models



---

$\underline{Model definition}$