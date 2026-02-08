import pandas
import re


def add_virtual_column(df: pandas.DataFrame, role: str, new_column: str) -> pandas.DataFrame:
    pattern = r'^[a-zA-Z_]+$'

    if not re.match(pattern, new_column):
        return pandas.DataFrame([])

    for col in df.columns:
        if not re.match(pattern, col):
            return pandas.DataFrame([])

    allowed_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_+-* ")
    if not all(c in allowed_chars for c in role):
        return pandas.DataFrame([])

    tokens = re.split(r'([+\-*])', role)
    clean_tokens = [t.strip() for t in tokens if t.strip()]

    for token in clean_tokens:
        if token not in ['+', '-', '*']:
            if token not in df.columns:
                return pandas.DataFrame([])

    try:
        df_new = df.copy()

        expr = role
        for col in df.columns:
            if col in expr:
                expr = re.sub(rf'\b{col}\b', f'df["{col}"]', expr)

        df_new[new_column] = eval(expr, {"df": df, "pandas": pandas}, {})
        return df_new
    except:
        return pandas.DataFrame([])