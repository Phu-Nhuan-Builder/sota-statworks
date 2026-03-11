"""
Unit tests for SPSS I/O service.
Test box plot whiskers, Q-Q Blom formula, session management.
"""
import pytest
import os
import numpy as np
import pandas as pd
from app.domain.services.spss_io import (
    SESSION_STORE, create_session, get_session, update_session,
    delete_session, df_to_json_safe, resolve_encoding
)
from app.domain.services.descriptives import spss_boxplot_stats
from app.domain.services.regression import spss_qq_data
from app.core.exceptions import SessionNotFoundError


@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "id": range(1, 11),
        "age": [22, 25, 21, 28, 23, 30, 24, 26, 22, 29],
        "score": [78.5, 82.3, 65.4, 90.1, 71.2, 88.7, 79.8, 84.5, 68.3, 92.1],
        "name": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
    })


@pytest.fixture
def sample_meta():
    from app.domain.models.dataset import DatasetMeta, VariableMeta, VariableType, VariableMeasure, VariableRole
    return DatasetMeta(
        file_name="test.csv",
        n_cases=10,
        n_vars=4,
        variables=[
            VariableMeta(name="id", label="ID", var_type=VariableType.numeric),
            VariableMeta(name="age", label="Age", var_type=VariableType.numeric),
            VariableMeta(name="score", label="Score", var_type=VariableType.numeric),
            VariableMeta(name="name", label="Name", var_type=VariableType.string),
        ],
        encoding="utf-8",
    )


class TestSessionStore:
    def test_create_session_returns_uuid(self, sample_df, sample_meta):
        session_id = create_session(sample_df, sample_meta)
        assert len(session_id) == 36  # UUID format
        delete_session(session_id)

    def test_get_session_returns_df_and_meta(self, sample_df, sample_meta):
        session_id = create_session(sample_df, sample_meta)
        df, meta = get_session(session_id)
        assert len(df) == 10
        assert meta.file_name == "test.csv"
        delete_session(session_id)

    def test_get_nonexistent_session_raises(self):
        with pytest.raises(SessionNotFoundError):
            get_session("nonexistent-session-id")

    def test_delete_session(self, sample_df, sample_meta):
        session_id = create_session(sample_df, sample_meta)
        delete_session(session_id)
        with pytest.raises(SessionNotFoundError):
            get_session(session_id)

    def test_update_session(self, sample_df, sample_meta):
        session_id = create_session(sample_df, sample_meta)
        new_df = sample_df.copy()
        new_df["new_col"] = 1
        update_session(session_id, new_df, sample_meta)
        df, _ = get_session(session_id)
        assert "new_col" in df.columns
        delete_session(session_id)


class TestDfToJsonSafe:
    def test_nan_becomes_none(self):
        df = pd.DataFrame({"x": [1.0, float("nan"), 3.0]})
        result = df_to_json_safe(df)
        assert result[1]["x"] is None

    def test_numpy_int_serializable(self):
        df = pd.DataFrame({"x": np.array([1, 2, 3], dtype=np.int64)})
        result = df_to_json_safe(df)
        assert isinstance(result[0]["x"], int)

    def test_timestamp_is_isoformat(self):
        df = pd.DataFrame({"dt": pd.to_datetime(["2024-01-01", "2024-01-02"])})
        result = df_to_json_safe(df)
        assert isinstance(result[0]["dt"], str)
        assert "2024" in result[0]["dt"]


class TestCSVReading:
    def test_read_sample_csv(self):
        fixture_path = os.path.join(
            os.path.dirname(__file__), "..", "fixtures", "sample.csv"
        )
        if not os.path.exists(fixture_path):
            pytest.skip("sample.csv fixture not found")
        from app.domain.services.spss_io import read_csv
        df, meta = read_csv(fixture_path)
        assert len(df) == 50
        assert meta.n_cases == 50
        assert meta.n_vars >= 5


class TestBoxPlotWhiskers:
    def test_whiskers_are_actual_data_points_not_fences(self):
        """Critical SPSS requirement: whiskers must be actual data values."""
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        result = spss_boxplot_stats(data)
        assert result["whisker_low"] in data
        assert result["whisker_high"] in data

    def test_iqr_method_correct(self):
        data = [2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7]
        result = spss_boxplot_stats(data)
        q1 = np.percentile(data, 25)
        q3 = np.percentile(data, 75)
        iqr = q3 - q1
        # Whiskers should be within 1.5*IQR from Q1/Q3
        assert result["whisker_low"] >= q1 - 1.5 * iqr
        assert result["whisker_high"] <= q3 + 1.5 * iqr


class TestQQBlomFormula:
    def test_blom_vs_scipy_default(self):
        """Verify Blom formula differs from scipy default (Filliben)."""
        from scipy import stats as scipy_stats
        data = list(range(1, 11))
        result = spss_qq_data(data)
        # Blom: (i - 3/8) / (n + 1/4)
        # Scipy default: (i - 0.5) / n
        n = 10
        blom_p1 = (1 - 3/8) / (n + 1/4)
        scipy_p1 = 0.5 / n  # (1 - 0.5) / n = 0.5/10
        assert abs(blom_p1 - scipy_p1) > 0.01  # They should differ
        expected_blom_t1 = scipy_stats.norm.ppf(blom_p1)
        assert abs(result["theoretical"][0] - expected_blom_t1) < 0.001
