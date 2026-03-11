"""
Unit tests for descriptive statistics service.
Test against known values.
"""
import pytest
import numpy as np
import pandas as pd
from app.domain.services.descriptives import (
    compute_frequencies, compute_descriptives, compute_crosstabs,
    compute_explore, spss_boxplot_stats
)


@pytest.fixture
def sample_df():
    """Sample DataFrame with known values."""
    return pd.DataFrame({
        "age": [22, 25, 21, 28, 23, 30, 24, 26, 22, 29, 21, 27],
        "score": [78.5, 82.3, 65.4, 90.1, 71.2, 88.7, 79.8, 84.5, 68.3, 92.1, 75.6, 81.4],
        "gender": [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2],
        "group": [1, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1],
    })


class TestFrequencies:
    def test_basic_frequencies(self, sample_df):
        result = compute_frequencies(sample_df, "gender")
        assert result["n_valid"] == 12
        assert result["n_missing"] == 0
        assert len(result["rows"]) == 2
        # Check counts
        counts = {str(r["value"]): r["count"] for r in result["rows"]}
        assert counts["1"] == 6
        assert counts["2"] == 6

    def test_percentages_sum_to_100(self, sample_df):
        result = compute_frequencies(sample_df, "gender")
        valid_rows = [r for r in result["rows"] if r["value"] != "Missing"]
        total_valid_pct = sum(r["valid_percent"] for r in valid_rows)
        assert abs(total_valid_pct - 100.0) < 0.5

    def test_cumulative_percent_ends_at_100(self, sample_df):
        result = compute_frequencies(sample_df, "group")
        valid_rows = [r for r in result["rows"] if r["value"] != "Missing"]
        assert abs(valid_rows[-1]["cumulative_percent"] - 100.0) < 0.5

    def test_with_missing_values(self):
        df = pd.DataFrame({"x": [1, 2, None, 1, 2, None, 1]})
        result = compute_frequencies(df, "x")
        assert result["n_missing"] == 2
        assert result["n_valid"] == 5


class TestDescriptives:
    def test_known_values(self, sample_df):
        result = compute_descriptives(sample_df, ["score"])
        row = result["rows"][0]
        assert row["variable"] == "score"
        assert row["n"] == 12
        assert abs(row["mean"] - 79.825) < 0.1
        assert row["minimum"] == 65.4
        assert row["maximum"] == 92.1

    def test_standard_error(self, sample_df):
        result = compute_descriptives(sample_df, ["score"])
        row = result["rows"][0]
        # SE = std / sqrt(n)
        expected_se = row["std_dev"] / np.sqrt(row["n"])
        assert abs(row["se_mean"] - expected_se) < 0.001

    def test_multiple_variables(self, sample_df):
        result = compute_descriptives(sample_df, ["age", "score"])
        assert len(result["rows"]) == 2
        vars_ = [r["variable"] for r in result["rows"]]
        assert "age" in vars_ and "score" in vars_

    def test_range_is_max_minus_min(self, sample_df):
        result = compute_descriptives(sample_df, ["age"])
        row = result["rows"][0]
        assert abs(row["range"] - (row["maximum"] - row["minimum"])) < 0.001


class TestCrosstabs:
    def test_basic_crosstab(self, sample_df):
        result = compute_crosstabs(sample_df, "gender", "group")
        assert result["n"] > 0
        assert result["chi2"] is not None

    def test_chi2_not_negative(self, sample_df):
        result = compute_crosstabs(sample_df, "gender", "group")
        assert result["chi2"] >= 0

    def test_p_value_in_range(self, sample_df):
        result = compute_crosstabs(sample_df, "gender", "group")
        assert 0.0 <= result["p_value"] <= 1.0

    def test_2x2_has_fishers(self, sample_df):
        result = compute_crosstabs(sample_df, "gender", "group")
        # 2×2 should have Fisher's exact
        assert result["fisher_exact_p"] is not None


class TestBoxPlotStats:
    def test_whiskers_are_actual_data_points(self):
        """SPSS-exact whiskers: actual data points, not fence values."""
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        result = spss_boxplot_stats(data)
        assert result["whisker_low"] in data
        assert result["whisker_high"] in data

    def test_no_outliers_for_normal_data(self):
        """Normal-ish data should have no outliers."""
        data = list(range(1, 21))
        result = spss_boxplot_stats(data)
        assert len(result["mild_outliers"]) == 0
        assert len(result["extreme_outliers"]) == 0

    def test_outliers_detected(self):
        """Extreme value should be flagged as outlier."""
        data = [1, 2, 3, 4, 5, 6, 7, 8, 100]  # 100 is outlier
        result = spss_boxplot_stats(data)
        assert 100 in result["mild_outliers"] or 100 in result["extreme_outliers"]

    def test_median_correct(self):
        data = [1, 2, 3, 4, 5]
        result = spss_boxplot_stats(data)
        assert result["median"] == 3.0
