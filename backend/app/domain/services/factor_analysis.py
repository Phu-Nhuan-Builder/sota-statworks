"""
Factor Analysis & Reliability Service
EFA, KMO, Bartlett's test, Cronbach's alpha
"""
import logging
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

# ── Monkey-patch: scikit-learn 1.6+ removed force_all_finite param ─────────
# factor_analyzer passes force_all_finite to sklearn.utils.validation.check_array
# which was renamed to ensure_all_finite in sklearn 1.6+.
# CRITICAL: factor_analyzer binds check_array at import time via
#   `from sklearn.utils.validation import check_array`
# So we must patch BOTH sklearn's module AND factor_analyzer's own reference.
try:
    from sklearn.utils.validation import check_array as _original_check_array
    import sklearn.utils.validation as _skval

    def _patched_check_array(*args, **kwargs):
        kwargs.pop("force_all_finite", None)
        return _original_check_array(*args, **kwargs)

    # Only patch if needed (test if force_all_finite is actually unsupported)
    try:
        _original_check_array([[1.0]], force_all_finite=True)
    except TypeError:
        # Patch sklearn module
        _skval.check_array = _patched_check_array
        # Patch factor_analyzer's own bound reference
        try:
            import factor_analyzer.factor_analyzer as _fa_mod
            _fa_mod.check_array = _patched_check_array
        except (ImportError, AttributeError):
            pass
        try:
            import factor_analyzer.utils as _fa_utils
            if hasattr(_fa_utils, 'check_array'):
                _fa_utils.check_array = _patched_check_array
        except (ImportError, AttributeError):
            pass
        logger.info("Patched check_array for force_all_finite compat (sklearn + factor_analyzer)")
except ImportError:
    pass


def calculate_kmo(X_array: np.ndarray) -> Tuple[float, np.ndarray]:
    """
    Kaiser-Meyer-Olkin (KMO) measure of sampling adequacy.
    Manual numpy implementation for full control.
    Returns (overall_kmo, per_variable_kmo_array)
    """
    from scipy import stats
    n, p = X_array.shape
    # Correlation matrix
    R = np.corrcoef(X_array, rowvar=False)
    try:
        R_inv = np.linalg.inv(R)
    except np.linalg.LinAlgError:
        R_inv = np.linalg.pinv(R)

    # Partial correlation matrix
    D = np.diag(1.0 / np.sqrt(np.diag(R_inv)))
    partial_corr = -D @ R_inv @ D
    np.fill_diagonal(partial_corr, 1.0)

    # KMO for each variable
    r2 = R ** 2
    pc2 = partial_corr ** 2
    np.fill_diagonal(r2, 0)
    np.fill_diagonal(pc2, 0)

    kmo_per_var = np.sum(r2, axis=0) / (np.sum(r2, axis=0) + np.sum(pc2, axis=0) + 1e-10)
    kmo_overall = np.sum(r2) / (np.sum(r2) + np.sum(pc2) + 1e-10)

    return float(kmo_overall), kmo_per_var


def run_efa(
    df: pd.DataFrame,
    variables: List[str],
    n_factors: int = 3,
    extraction: str = "principal",
    rotation: str = "varimax",
) -> dict:
    """
    Exploratory Factor Analysis using factor_analyzer.
    Supports: principal, minres, ml extraction; varimax, oblimin, quartimax, promax, none rotation.
    Returns: loadings, communalities, eigenvalues, % variance, scree data, KMO, Bartlett.
    """
    from factor_analyzer import FactorAnalyzer
    from factor_analyzer.factor_analyzer import calculate_bartlett_sphericity
    from scipy import stats

    subset = df[variables].dropna()
    X = subset.to_numpy(dtype=float)
    n, p = X.shape

    if n < 3:
        raise ValueError(f"Need at least 3 cases for factor analysis, got {n}")

    if p < 2:
        raise ValueError(f"Need at least 2 variables for factor analysis, got {p}")

    if n < p:
        logger.warning(f"EFA: n ({n}) < p ({p}), results may be unstable")

    if n_factors > p:
        n_factors = p
        logger.warning(f"EFA: n_factors capped at {p} (number of variables)")

    # Clean NaN/Inf values that slip through
    if not np.isfinite(X).all():
        X = np.nan_to_num(X, nan=0.0, posinf=0.0, neginf=0.0)
        logger.warning("EFA: Replaced non-finite values with 0")

    # KMO
    kmo_overall, kmo_per_var = calculate_kmo(X)

    # Bartlett's test
    bartlett_chi2 = None
    bartlett_df = None
    bartlett_p = None
    try:
        chi2, p_val = calculate_bartlett_sphericity(X)
        bartlett_chi2 = round(float(chi2), 4)
        bartlett_df = int(p * (p - 1) / 2)
        bartlett_p = round(float(p_val), 4)
    except Exception as e:
        logger.warning(f"Bartlett's test failed: {e}")

    # Map extraction method to factor_analyzer naming
    method_map = {"principal": "principal", "minres": "minres", "ml": "ml"}
    fa_method = method_map.get(extraction, "principal")
    rotation_val = None if rotation == "none" else rotation

    # Fit factor analyzer (sklearn compat patched at module level)
    fa = FactorAnalyzer(n_factors=n_factors, method=fa_method, rotation=rotation_val)
    fa.fit(X)

    # Loadings (n_vars × n_factors)
    loadings = fa.loadings_.tolist()

    # Communalities
    communalities = fa.get_communalities().tolist()

    # Eigenvalues (from unrotated solution for scree plot)
    ev, v = fa.get_eigenvalues()
    eigenvalues = ev.tolist()

    # Explained variance
    var_explained = fa.get_factor_variance()
    # Returns (SS_loadings, proportion_var, cumulative_var)
    explained_variance = var_explained[1].tolist()  # proportion
    cumulative_variance = var_explained[2].tolist()  # cumulative proportion

    # Convert to percentage
    explained_variance_pct = [round(v * 100, 2) for v in explained_variance]
    cumulative_variance_pct = [round(v * 100, 2) for v in cumulative_variance]

    # Factor names
    factor_names = [f"Factor {i+1}" for i in range(n_factors)]

    # Build loadings table
    headers = ["Variable"] + factor_names + ["Communality"]
    rows = []
    for i, var in enumerate(variables):
        row = [var] + [round(float(loadings[i][j]), 4) for j in range(n_factors)] + [round(float(communalities[i]), 4)]
        rows.append(row)

    return {
        "variables": variables,
        "n_factors": n_factors,
        "n_cases": n,
        "extraction": extraction,
        "rotation": rotation,
        "loadings": loadings,
        "communalities": communalities,
        "eigenvalues": eigenvalues,
        "explained_variance": explained_variance_pct,
        "cumulative_variance": cumulative_variance_pct,
        "kmo": round(kmo_overall, 4),
        "kmo_per_var": kmo_per_var.tolist(),
        "bartlett_chi2": bartlett_chi2,
        "bartlett_df": bartlett_df,
        "bartlett_p": bartlett_p,
        "scree_data": [round(float(e), 4) for e in eigenvalues],
        "headers": headers,
        "rows": rows,
    }


def run_reliability(df: pd.DataFrame, variables: List[str]) -> dict:
    """
    Reliability Analysis — Cronbach's alpha + item statistics.
    Uses pingouin.cronbach_alpha() which matches SPSS exactly (ddof=1).
    """
    import pingouin as pg

    subset = df[variables].dropna()
    n_cases = len(subset)
    n_items = len(variables)

    if n_cases < 2 or n_items < 2:
        raise ValueError("Need at least 2 cases and 2 items for reliability analysis")

    # Overall Cronbach's alpha
    alpha_result = pg.cronbach_alpha(data=subset)
    alpha = round(float(alpha_result[0]), 4)
    ci = alpha_result[1]  # 95% CI tuple
    alpha_ci_lower = round(float(ci[0]), 4)
    alpha_ci_upper = round(float(ci[1]), 4)

    # Item statistics
    item_stats = []
    for var in variables:
        # Item-total correlation (corrected: correlate item with sum of OTHER items)
        other_vars = [v for v in variables if v != var]
        other_sum = subset[other_vars].sum(axis=1)
        r, _ = __import__("scipy.stats", fromlist=["pearsonr"]).pearsonr(subset[var].to_numpy(), other_sum.to_numpy())

        # Alpha if item deleted
        alpha_if_deleted = None
        try:
            remaining = [v for v in variables if v != var]
            if len(remaining) >= 2:
                aid_result = pg.cronbach_alpha(data=subset[remaining])
                alpha_if_deleted = round(float(aid_result[0]), 4)
        except Exception:
            pass

        item_stats.append({
            "variable": var,
            "mean": round(float(subset[var].mean()), 4),
            "std": round(float(subset[var].std(ddof=1)), 4),
            "item_total_corr": round(float(r), 4),
            "alpha_if_deleted": alpha_if_deleted,
        })

    return {
        "variables": variables,
        "n_items": n_items,
        "n_cases": n_cases,
        "cronbach_alpha": alpha,
        "cronbach_alpha_ci_lower": alpha_ci_lower,
        "cronbach_alpha_ci_upper": alpha_ci_upper,
        "item_stats": item_stats,
        "headers": ["Item", "Mean", "Std Dev", "Item-Total Corr.", "Alpha if Deleted"],
        "rows": [[s["variable"], s["mean"], s["std"], s["item_total_corr"], s["alpha_if_deleted"]] for s in item_stats],
    }
