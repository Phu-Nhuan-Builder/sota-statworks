"""
Unit tests for regression service.
Test against statsmodels reference values.
"""
import pytest
import numpy as np
import pandas as pd
import statsmodels.api as sm
from app.domain.services.regression import (
    ols_regression, binary_logistic, pearson_spearman_correlation, spss_qq_data
)


@pytest.fixture
def regression_df():
    """DataFrame for regression tests."""
    np.random.seed(123)
    n = 50
    x1 = np.random.normal(5, 2, n)
    x2 = np.random.normal(3, 1, n)
    y = 2.0 + 1.5 * x1 - 0.8 * x2 + np.random.normal(0, 1, n)
    return pd.DataFrame({"y": y, "x1": x1, "x2": x2})


@pytest.fixture
def logistic_df():
    """DataFrame for logistic regression tests."""
    np.random.seed(42)
    n = 100
    x1 = np.random.normal(0, 1, n)
    x2 = np.random.normal(0, 1, n)
    logit = 0.5 + 1.2 * x1 - 0.8 * x2
    prob = 1 / (1 + np.exp(-logit))
    y = (np.random.random(n) < prob).astype(int)
    return pd.DataFrame({"y": y, "x1": x1, "x2": x2})


class TestOLSRegression:
    def test_r2_matches_statsmodels(self, regression_df):
        result = ols_regression(regression_df, "y", ["x1", "x2"])
        # Reference using statsmodels
        X = sm.add_constant(regression_df[["x1", "x2"]])
        ref_model = sm.OLS(regression_df["y"], X).fit()
        assert abs(result["r2"] - ref_model.rsquared) < 0.001

    def test_adj_r2_matches_statsmodels(self, regression_df):
        result = ols_regression(regression_df, "y", ["x1", "x2"])
        X = sm.add_constant(regression_df[["x1", "x2"]])
        ref_model = sm.OLS(regression_df["y"], X).fit()
        assert abs(result["adj_r2"] - ref_model.rsquared_adj) < 0.001

    def test_coefficients_match_statsmodels(self, regression_df):
        result = ols_regression(regression_df, "y", ["x1", "x2"])
        X = sm.add_constant(regression_df[["x1", "x2"]])
        ref_model = sm.OLS(regression_df["y"], X).fit()
        # Intercept
        assert abs(result["coefficients"][0]["B"] - float(ref_model.params[0])) < 0.01
        # x1
        assert abs(result["coefficients"][1]["B"] - float(ref_model.params[1])) < 0.01

    def test_f_statistic_positive(self, regression_df):
        result = ols_regression(regression_df, "y", ["x1", "x2"])
        assert result["f_stat"] > 0

    def test_vif_present(self, regression_df):
        result = ols_regression(regression_df, "y", ["x1", "x2"])
        for coef in result["coefficients"][1:]:  # skip intercept
            assert coef["vif"] is not None

    def test_durbin_watson_in_range(self, regression_df):
        result = ols_regression(regression_df, "y", ["x1", "x2"])
        assert 0.0 <= result["durbin_watson"] <= 4.0


class TestBinaryLogistic:
    def test_result_structure(self, logistic_df):
        result = binary_logistic(logistic_df, "y", ["x1", "x2"])
        assert "neg_2LL" in result
        assert "cox_snell_r2" in result
        assert "nagelkerke_r2" in result
        assert len(result["coefficients"]) == 3  # intercept + 2 vars

    def test_exp_B_positive(self, logistic_df):
        result = binary_logistic(logistic_df, "y", ["x1", "x2"])
        for coef in result["coefficients"]:
            assert coef["exp_B"] > 0

    def test_pseudo_r2_in_range(self, logistic_df):
        result = binary_logistic(logistic_df, "y", ["x1", "x2"])
        assert 0.0 <= result["cox_snell_r2"] <= 1.0
        assert 0.0 <= result["nagelkerke_r2"] <= 1.0


class TestCorrelation:
    def test_pearson_diagonal_is_1(self, regression_df):
        result = pearson_spearman_correlation(regression_df, ["y", "x1", "x2"])
        for i in range(3):
            assert result["r_matrix"][i][i] == 1.0

    def test_symmetry(self, regression_df):
        result = pearson_spearman_correlation(regression_df, ["y", "x1"])
        assert abs(result["r_matrix"][0][1] - result["r_matrix"][1][0]) < 0.001


class TestQQData:
    def test_blom_formula(self):
        """SPSS uses Blom (1958): p_i = (i - 3/8) / (n + 1/4)"""
        data = list(range(1, 11))  # 10 values
        result = spss_qq_data(data)
        assert len(result["theoretical"]) == 10
        assert len(result["observed"]) == 10
        # First theoretical quantile: (1 - 3/8) / (10 + 1/4) = 0.625/10.25
        from scipy import stats as scipy_stats
        expected_p1 = (1 - 3/8) / (10 + 1/4)
        expected_t1 = scipy_stats.norm.ppf(expected_p1)
        assert abs(result["theoretical"][0] - expected_t1) < 0.001
