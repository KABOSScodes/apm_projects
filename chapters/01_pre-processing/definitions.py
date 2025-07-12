def check_transform_suitability(df, save_csv=False, skew_bias=True, csv_path='transform_suitability.csv'):
    """
    UPDATE DESCRIPTION:
    Check suitability of each column for Box-Cox and Yeo-Johnson transformations,
    and report missing value stats.
    
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
    CONSIDER ADDING CENTERING AND FOR CONSITENCY'S SAKE
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
