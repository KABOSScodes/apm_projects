import pandas as pd
from scipy.stats import skew
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, leaves_list


def check_transform_suitability(df, save_csv=False, skew_bias=True, csv_path='transform_suitability.csv'):
    """
    Parameters:
    - df: pandas DataFrame
    - save_csv: bool, whether to save the summary dataframe to a csv file (default False)
    - skew_bias: bool, whether to apply bias correction in skewness calculation (default True)
    - csv_path: str, path to save the csv file if save_csv=True
    
    Returns:
    - summary_df: DataFrame with columns ['Column', 'Data Type', 'Box-Cox Applicable', 'Yeo-Johnson Applicable', 'Has NaNs', 'NaN Count', 'NaN %']
    - boxcox_cols: list of columns suitable for Box-Cox
    - yeojohnson_cols: list of columns suitable for Yeo-Johnson
    """
    
    summary_list = []
    
    for col in df.columns:
        dtype = df[col].dtype
        
        # Initializations
        skew_value = None
        boxcox_applicable = False
        yeojohnson_applicable = False
        
        if pd.api.types.is_numeric_dtype(dtype):
            col_data = df[col].dropna() # 
            skew_value = skew(col_data, bias=skew_bias)  # Calculate skewness
            # Box-Cox requires all values > 0
            if (col_data > 0).all():
                boxcox_applicable = True
            # Yeo-Johnson works for all numeric (including 0 and negatives)
            yeojohnson_applicable = True

        # Missing values info
        nan_count = df[col].isna().sum()
        has_nans = "Yes" if nan_count > 0 else "No"
        nan_percent = (nan_count / len(df)) * 100
        
        summary_list.append({
            'Column': col,
            'Data Type': str(dtype),
            'Skewness': skew_value,
            'Apply Transformation': (abs(skew_value) > 0.5) if skew_value is not None else False,
            'Box-Cox Applicable': boxcox_applicable,
            'Yeo-Johnson Applicable': yeojohnson_applicable,
            'NaN Count': nan_count,
            'NaN %': f"{nan_percent:.2f}%"
        })
    
    summary_df = pd.DataFrame(summary_list)
    
    # Purely nice-to-have for later analysis
    boxcox_cols = summary_df[summary_df['Box-Cox Applicable']]['Column'].tolist()
    yeojohnson_cols = summary_df[summary_df['Yeo-Johnson Applicable']]['Column'].tolist()
    
    if save_csv:
        summary_df.to_csv(csv_path, index=False)
        print(f"Summary saved to {csv_path}")
    
    return summary_df, boxcox_cols, yeojohnson_cols


def selective_transform(df, summary_df):
    """
    Transform columns in df if 'Apply Transformation' in summary_df is True.
    Use Box-Cox if applicable, otherwise Yeo-Johnson. Only numeric columns are transformed.
    """
    from sklearn.preprocessing import PowerTransformer

    transformed_df = df.copy()
    for _, row in summary_df.iterrows():
        col = row['Column']
        apply = row['Apply Transformation']
        boxcox_ok = row['Box-Cox Applicable']
        yeojohnson_ok = row['Yeo-Johnson Applicable']
        dtype = df[col].dtype

        # Only transform if flagged, applicable, and numeric
        if pd.api.types.is_numeric_dtype(dtype):
            data = df[col].values.reshape(-1, 1)
            if boxcox_ok and apply:
                pt = PowerTransformer(method='box-cox')
                transformed_df[col] = pt.fit_transform(data)
            elif yeojohnson_ok and apply:
                pt = PowerTransformer(method='yeo-johnson')
                transformed_df[col] = pt.fit_transform(data)
            else:
                # Center and scale for the remaining columns
                transformed_df[col] = (data - np.mean(data)) / np.std(data)
            # If neither applicable, skip

    return transformed_df


def near_zero_var(df, freq_cut=95/5, unique_cut=10):
    """
    Identifies near-zero variance features in a DataFrame. This function is only 
    meaningful for discrete/categorical or rounded numeric data, not continuous features.

    This function replicates the behavior of the `caret::nearZeroVar()` function in R.
    It flags columns (features) that have both:
        - A high imbalance in the frequency of values (i.e., one value dominates), and
        - A low number of unique values relative to the number of samples.

    Parameters:
    ----------
    df : pandas.DataFrame
        The input DataFrame containing features to evaluate.
    freq_cut : float, optional (default = 19)
        The frequency ratio cutoff. Columns where the ratio of the most common to the
        second most common value exceeds this threshold are considered imbalanced.
    unique_cut : float, optional (default = 10)
        The percentage cutoff for the number of unique values. Columns with fewer than
        this percentage of unique values (relative to the number of rows) are flagged.

    Returns:
    -------
    nzv : list of str
        List of column names in `df` that are considered near-zero variance predictors.
    """
    nzv = []
    for col in df.columns:
        counts = df[col].value_counts()
        if len(counts) == 0:
            continue
        freq_ratio = counts.iloc[0] / counts.iloc[1] if len(counts) > 1 else float('inf')
        percent_unique = 100.0 * len(counts) / len(df)
        
        if freq_ratio > freq_cut and percent_unique < unique_cut:
            nzv.append(col)
    return nzv


def find_correlation(df, cutoff=0.75, exact=True):
    """
    Parameters:
    df : pandas.DataFrame
        The input DataFrame for which to find highly correlated features.
    cutoff : float, optional (default=0.75)
        The correlation threshold above which features are considered highly correlated.
    exact : boolean, optional (deafult=True)
        If True, use the exact (but slower) algorithm for finding correlated features.
        If False, use a faster, approximate method. The exact method is more precise,
        but may be slower for large datasets.
    
    Returns:
    list : 
        A list of column names that are highly correlated with at least one other column
    """


    def _find_correlation_fast(corr, cutoff):
        # Compute mean correlations
        avg = corr.mean() 
            
        # Find all pairs above the cutoff (lower triangle only)
        high_corr_pairs = corr.where(np.tril(np.ones(corr.shape), k=-1).astype(bool) & (corr > cutoff)).stack().index

        # Split into rows and columns
        rows_to_check = high_corr_pairs.get_level_values(0)
        cols_to_check = high_corr_pairs.get_level_values(1)

        # Create mask
        msk = avg[cols_to_check] > avg[rows_to_check].values # Comparison of mean correlations

        # Use mask to only return features that had greatest average mean correlation.
        cols_to_delete = pd.unique(np.r_[cols_to_check[msk], rows_to_check[~msk]]).tolist()

        return cols_to_delete

    def _find_correlation_exact(corr, cutoff):
        # TODO: Implement exact correlation removal logic
        pass

    corr_matrix = df.corr().abs()
    cols_to_delete = _find_correlation_fast(corr_matrix, cutoff)

    return cols_to_delete


def plot_corr(df, figsize=(10, 8)):
    """
    Visualizes the correlation matrix of the DataFrame using seaborn heatmap.
    Clusters the heatmap to group similar features together.
    
    Parameters:
    df : pandas.DataFrame
        The input DataFrame for which to visualize the correlation matrix.
    figsize : tuple, optional (default=(10, 8))
        The size of the figure for the heatmap.
    
    Returns:
    correlation_matrix : pandas.DataFrame
        The reordered correlation matrix after clustering.
    """

    # Calculate the correlation matrix
    correlation_matrix = df.corr()

    # Compute linkage on the correlation matrix (use ward linkage, like hclust in R)
    linkage_matrix = linkage(correlation_matrix, method='ward')

    # Reorder rows/columns according to clustering
    reordered_indices = leaves_list(linkage_matrix)
    correlation_matrix = correlation_matrix.iloc[reordered_indices, reordered_indices]

    plt.figure(figsize=figsize)
    sns.heatmap(correlation_matrix, cmap='coolwarm', center=0, square=True, linewidths=0.5)
    plt.title("Correlation Matrix with Clustering")
    plt.tight_layout()
    plt.show()

    return correlation_matrix