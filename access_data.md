# Load dataset
Tutorial on how to access data used in Applied Predictive Modeling. This is accessed in R and then downloaded as a Parquet file for import in python.

Example is based on the specific dataset segmentationOriginal from the AppliedPredictiveModeling package. In all cases, this should be replaced with the dataset and package of interest.

## In R
Install and load dataset:
- `install.packages('AppliedPredictiveModeling')` Follow instructions if any for installation.
- `library(AppliedPredictiveModeling)`
- `data(segmentationOriginal)`

Use the following to inspect the loaded dataset:
- `str(segmentationOriginal)`
- `head(segmentationOriginal)`
- `summary(segmentationOriginal)`

If not installed, install arrow to export data as parquet file:
- `install.packages("arrow")`

Load arrow and save the dataset:
- `library(arrow)`
- `write_parquet(segmentationOriginal, "segmentation.parquet")`
Or
- `write_parquet(segmentationOriginal, "~/Desktop/apm_projects/data/segmentation.parquet", compression = "snappy")`

### Note on the BloodBrain Dataset
For the BloodBrain dataset (from the caret package), the outcome (logBBB) is stored as a separate vector from the predictors (bbbDescr). To save it as a single data frame, we combine them after loading:
- `data(BloodBrain)`
- `bbb_data <- cbind(logBBB = logBBB, bbbDescr)`

## In python
Load dataset:
- `import pandas as pd`
- `df = pd.read_parquet("../../data/segmentation.parquet")`
