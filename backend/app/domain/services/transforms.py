"""
Data Transform Service
Recode, Compute, Filter (Select Cases), Sort, Rank
"""
import logging
import re
from typing import Any, Dict, List, Optional, Union

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

# Safe functions available in compute expressions
SAFE_MATH = {
    "abs": abs, "round": round, "int": int, "float": float,
    "min": min, "max": max, "sum": sum,
    "sqrt": np.sqrt, "log": np.log, "log10": np.log10, "log2": np.log2,
    "exp": np.exp, "sin": np.sin, "cos": np.cos, "tan": np.tan,
    "floor": np.floor, "ceil": np.ceil,
    "nan": float("nan"), "inf": float("inf"),
}


def recode_variable(
    df: pd.DataFrame,
    source_var: str,
    target_var: str,
    mapping_rules: List[Dict[str, Any]],
    else_value: Optional[Any] = None,
) -> pd.DataFrame:
    """
    Recode variable values using a mapping table.
    Supports: into same variable (source_var == target_var) or different variable.
    mapping_rules: list of {"from_value": val, "to_value": new_val}
    else_value: value for unmatched cases (None = keep original)
    """
    df = df.copy()
    source = df[source_var].copy()

    # Build value mapping dict
    value_map = {}
    for rule in mapping_rules:
        from_val = rule.get("from_value")
        to_val = rule.get("to_value")
        if from_val is not None:
            value_map[from_val] = to_val

    # Apply mapping
    if else_value is not None:
        # Map with default for unmatched
        df[target_var] = source.map(value_map).fillna(
            source.map(lambda x: else_value if x not in value_map else value_map[x])
        )
        # Simpler approach: map then fill with else_value for unmapped
        mapped = source.map(value_map)
        mask = source.isin(value_map.keys())
        result = source.copy().astype(object)
        result[mask] = mapped[mask]
        result[~mask] = else_value
        df[target_var] = result
    else:
        # Keep original for unmatched
        result = source.copy().astype(object)
        for from_val, to_val in value_map.items():
            result[source == from_val] = to_val
        df[target_var] = result

    return df


def compute_variable(
    df: pd.DataFrame,
    target_var: str,
    expression: str,
    label: Optional[str] = None,
) -> pd.DataFrame:
    """
    Compute a new variable from a formula expression.
    Uses pd.eval() with a safe namespace including numpy math functions.
    Example: "age * 2 + income / 1000"
    """
    df = df.copy()

    # Sanitize expression — block dangerous builtins
    dangerous = ["__", "import", "exec", "eval", "open", "file", "os", "sys", "subprocess"]
    for d in dangerous:
        if d in expression:
            raise ValueError(f"Expression contains forbidden term: '{d}'")

    try:
        # Try pd.eval first (fast path for simple arithmetic)
        result = df.eval(expression)
        df[target_var] = result
    except Exception as e1:
        # Fallback: numpy eval with safe namespace
        try:
            local_ns = {col: df[col].to_numpy() for col in df.columns}
            local_ns.update(SAFE_MATH)
            result = eval(expression, {"__builtins__": {}}, local_ns)
            df[target_var] = result
        except Exception as e2:
            raise ValueError(f"Invalid expression: {str(e2)}")

    return df


def select_cases(
    df: pd.DataFrame,
    condition: str,
    filter_type: str = "include",
) -> pd.DataFrame:
    """
    Filter rows based on a condition expression.
    Uses df.query() for safe evaluation.
    filter_type: "include" (keep matching) or "exclude" (remove matching)
    """
    # Sanitize condition
    dangerous = ["__", "import", "exec", "eval", "open", "os", "sys"]
    for d in dangerous:
        if d in condition:
            raise ValueError(f"Condition contains forbidden term: '{d}'")

    try:
        matching = df.query(condition)
        if filter_type == "exclude":
            return df.drop(matching.index).reset_index(drop=True)
        else:
            return matching.reset_index(drop=True)
    except Exception as e:
        raise ValueError(f"Invalid filter condition: {str(e)}")


def sort_cases(df: pd.DataFrame, sort_keys: List[Dict[str, str]]) -> pd.DataFrame:
    """
    Sort DataFrame by multiple keys.
    sort_keys: [{"variable": "age", "order": "asc"}, {"variable": "name", "order": "desc"}]
    """
    if not sort_keys:
        return df

    columns = []
    ascending = []
    for key in sort_keys:
        var = key.get("variable")
        order = key.get("order", "asc").lower()
        if var and var in df.columns:
            columns.append(var)
            ascending.append(order != "desc")

    if not columns:
        return df

    return df.sort_values(by=columns, ascending=ascending).reset_index(drop=True)


def rank_cases(
    df: pd.DataFrame,
    variables: List[str],
    method: str = "average",
    ascending: bool = True,
) -> pd.DataFrame:
    """
    Rank variable values. Creates new rank columns prefixed with 'RANK_'.
    method: "average", "min", "max", "first", "dense"
    """
    df = df.copy()
    for var in variables:
        if var not in df.columns:
            continue
        rank_col = f"RANK_{var}"
        df[rank_col] = df[var].rank(method=method, ascending=ascending, na_option="keep")
    return df
