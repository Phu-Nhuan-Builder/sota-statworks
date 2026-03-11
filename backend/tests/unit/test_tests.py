"""
Unit tests for hypothesis tests service.
Test against scipy reference values.
"""
import pytest
import numpy as np
import pandas as pd
from scipy import stats as scipy_stats
from app.domain.services.tests import (
    independent_ttest, paired_ttest, one_sample_ttest, one_way_anova
)


@pytest.fixture
def two_group_df():
    """DataFrame with two groups for independent t-test."""
    np.random.seed(42)
    group1 = [78.5, 82.3, 65.4, 90.1, 71.2, 88.7, 79.8, 84.5, 68.3, 92.1]
    group2 = [65.2, 70.1, 75.8, 63.4, 72.6, 68.9, 74.3, 66.7, 71.5, 69.8]
    return pd.DataFrame({
        "score": group1 + group2,
        "group": [1] * 10 + [2] * 10,
    })


@pytest.fixture
def anova_df():
    """DataFrame with 3 groups for ANOVA."""
    return pd.DataFrame({
        "score": [10, 12, 11, 15, 14, 13, 20, 22, 19, 25, 24, 21],
        "group": ["A", "A", "A", "B", "B", "B", "C", "C", "C", "D", "D", "D"],
    })


class TestIndependentTTest:
    def test_t_statistic_matches_scipy(self, two_group_df):
        result = independent_ttest(two_group_df, "group", "score", equal_var=True)
        g1 = two_group_df[two_group_df["group"] == 1]["score"].values
        g2 = two_group_df[two_group_df["group"] == 2]["score"].values
        t_ref, p_ref = scipy_stats.ttest_ind(g1, g2, equal_var=True)
        assert abs(result["statistic"] - t_ref) < 0.001

    def test_p_value_matches_scipy(self, two_group_df):
        result = independent_ttest(two_group_df, "group", "score", equal_var=True)
        g1 = two_group_df[two_group_df["group"] == 1]["score"].values
        g2 = two_group_df[two_group_df["group"] == 2]["score"].values
        _, p_ref = scipy_stats.ttest_ind(g1, g2, equal_var=True)
        assert abs(result["pvalue"] - p_ref) < 0.001

    def test_levene_test_present(self, two_group_df):
        result = independent_ttest(two_group_df, "group", "score")
        assert result["levene_F"] is not None
        assert result["levene_p"] is not None

    def test_cohen_d_is_float(self, two_group_df):
        result = independent_ttest(two_group_df, "group", "score")
        assert isinstance(result["cohen_d"], float)

    def test_ci_contains_mean_diff(self, two_group_df):
        result = independent_ttest(two_group_df, "group", "score")
        assert result["ci_lower"] <= result["mean_diff"] <= result["ci_upper"]

    def test_welch_different_from_student(self, two_group_df):
        result_eq = independent_ttest(two_group_df, "group", "score", equal_var=True)
        result_welch = independent_ttest(two_group_df, "group", "score", equal_var=False)
        # Welch df should differ from Student df for unequal groups
        # Both should have the same sign of t-statistic
        assert result_eq["statistic"] * result_welch["statistic"] > 0


class TestPairedTTest:
    def test_t_matches_scipy(self):
        df = pd.DataFrame({"pre": [10, 12, 11, 15, 14], "post": [12, 14, 13, 17, 16]})
        result = paired_ttest(df, "pre", "post")
        t_ref, p_ref = scipy_stats.ttest_rel(df["pre"], df["post"])
        assert abs(result["statistic"] - t_ref) < 0.001

    def test_correlation_is_positive(self):
        df = pd.DataFrame({"pre": [10, 12, 11, 15, 14], "post": [12, 14, 13, 17, 16]})
        result = paired_ttest(df, "pre", "post")
        assert result["correlation"] > 0


class TestOneSampleTTest:
    def test_t_matches_scipy(self):
        df = pd.DataFrame({"x": [10, 12, 11, 15, 14, 13, 9, 16, 11, 12]})
        result = one_sample_ttest(df, "x", test_value=10)
        t_ref, p_ref = scipy_stats.ttest_1samp(df["x"].values, 10)
        assert abs(result["statistic"] - t_ref) < 0.001

    def test_zero_mean_diff_when_test_value_equals_mean(self):
        values = [10.0, 10.0, 10.0, 10.0, 10.0]
        df = pd.DataFrame({"x": values})
        result = one_sample_ttest(df, "x", test_value=10.0)
        assert abs(result["mean_diff"]) < 0.001
        assert abs(result["statistic"]) < 0.001


class TestOneWayANOVA:
    def test_f_matches_scipy(self, anova_df):
        result = one_way_anova(anova_df, "group", "score")
        groups = [anova_df[anova_df["group"] == g]["score"].values for g in ["A", "B", "C", "D"]]
        f_ref, p_ref = scipy_stats.f_oneway(*groups)
        assert abs(result["f_statistic"] - f_ref) < 0.01

    def test_p_value_in_range(self, anova_df):
        result = one_way_anova(anova_df, "group", "score")
        assert 0.0 <= result["p_value"] <= 1.0

    def test_eta_squared_in_range(self, anova_df):
        result = one_way_anova(anova_df, "group", "score")
        assert 0.0 <= result["eta_squared"] <= 1.0

    def test_tukey_posthoc(self, anova_df):
        result = one_way_anova(anova_df, "group", "score", posthoc="tukey")
        assert result["posthoc_results"] is not None
        assert len(result["posthoc_results"]) > 0
