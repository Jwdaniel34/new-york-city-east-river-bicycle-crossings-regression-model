# 🚲 NYC East River Bicycle Crossings: Count Modeling

This project uses **Poisson Regression** and **Negative Binomial Regression** to model and analyze bicycle traffic across New York City’s East River crossings. The dataset includes daily total bike counts, weather data (temperature, precipitation), and time-based features like day of the week and month.

---

## 📂 Dataset

- **Source**: [Kaggle - NYC East River Bicycle Crossings](https://www.kaggle.com/datasets/new-york-city/nyc-east-river-bicycle-crossings)
- **File used**: `east_river_counts.csv`
- **Rows**: 210 days  
- **Columns**: Date, Total (bike count), Bridge-level counts, Weather features

---

## 🧹 Data Cleaning & Preprocessing

### ✅ Steps Taken:

1. **Datetime parsing**:
   - Converted `Date` column to `datetime` format
   - Extracted `day_of_week` and `month`

2. **Temperature engineering**:
   - Created `temp_avg` = (HighTemp + LowTemp) / 2

3. **Precipitation processing**:
   - Original `Precip` column had mixed types (e.g., "0.47 (S)")
   - Extracted precipitation values numerically
   - Created binary indicator:
     - `precip_bin = 1` if precipitation > 0 (rain or snow)
     - `precip_bin = 0` otherwise

4. **Final variables used**:
   - `Count` (total bike count) — renamed from `Total`
   - `temp_avg`
   - `precip_bin`
   - `day_of_week` (categorical)
   - `month` (categorical)

---

## 📊 Exploratory Data Analysis (EDA)

- Scatter plot of `temp_avg` vs `Count` showed a positive trend
- Rainy/snowy days visibly reduced total bike counts

---

## 📈 Modeling Approaches

### 🟠 Poisson Regression

```python
formula = "Count ~ temp_avg + precip_bin + C(day_of_week)"
poisson_mod = smf.glm(formula=formula, data=df, family=sm.families.Poisson()).fit()
nb_mod = smf.glm(formula=formula, data=df_raw, family=sm.families.NegativeBinomial()).fit()
```

Model Summary

| **Metric**                    | **Value**     | **Explanation**                                      |
|------------------------------|---------------|------------------------------------------------------|
| **Dependent Variable**       | `Count`       | Daily total bicycle count                            |
| **Observations**             | 210           | Number of days in dataset                            |
| **Model Family**             | Negative Binomial | Accounts for overdispersion in count data        |
| **Link Function**            | Log           | Predicts the log of expected counts                  |
| **Degrees of Freedom (Residual)** | 201     | Used in deviance and chi-squared calculations        |
| **Log-Likelihood**           | -2206.9       | Higher (less negative) indicates a better fit        |
| **Deviance**                 | 8.57          | Low deviance means predictions fit observed counts   |
| **Pearson Chi²**             | 8.13          | Close to degrees of freedom → good model fit         |
| **Pseudo R² (Cragg & Uhler)**| 0.1401        | Model explains ~14% of variability in counts         |
| **Iterations to Converge**   | 8             | Model fitting converged in 8 steps                   |


<br>

Because it had Over-dispersion I decided to go with Negative Binomial Poisson and + C(month) there was only one month being shown throughout
the dates so it will calculate for the month of April