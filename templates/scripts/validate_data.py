"""Data Testing : vérification du format et de la représentativité d'un jeu de données.

Usage :
    python scripts/validate_data.py --data-path data/processed/test_data.csv \
        [--reference-path data/processed/train_data.csv]

Adapter SCHEMA au projet. Le script sort en code 1 si un contrôle échoue,
ce qui fait échouer l'étape correspondante de la CI.
"""
import argparse
import sys

import pandas as pd
from scipy.stats import ks_2samp

# Colonne -> (type attendu, min, max). None = pas de borne.
SCHEMA = {
    "Age": ("number", 0, 120),
    "Sex": ("object", None, None),
    "BP": ("object", None, None),
    "Cholesterol": ("object", None, None),
    "Na_to_K": ("number", 0, None),
}
MAX_MISSING_RATIO = 0.0
DRIFT_P_VALUE = 0.05


def check_format(df):
    errors = []
    missing_cols = set(SCHEMA) - set(df.columns)
    if missing_cols:
        errors.append(f"Colonnes manquantes : {sorted(missing_cols)}")
    for col, (kind, low, high) in SCHEMA.items():
        if col not in df.columns:
            continue
        series = df[col]
        if kind == "number" and not pd.api.types.is_numeric_dtype(series):
            errors.append(f"{col} : type numérique attendu, obtenu {series.dtype}")
            continue
        ratio = series.isna().mean()
        if ratio > MAX_MISSING_RATIO:
            errors.append(f"{col} : {ratio:.1%} de valeurs manquantes")
        if low is not None and (series < low).any():
            errors.append(f"{col} : valeurs < {low}")
        if high is not None and (series > high).any():
            errors.append(f"{col} : valeurs > {high}")
    return errors


def check_representativeness(df, ref):
    errors = []
    for col, (kind, _, _) in SCHEMA.items():
        if col not in df.columns or col not in ref.columns:
            continue
        if kind == "number":
            p_value = ks_2samp(df[col].dropna(), ref[col].dropna()).pvalue
            if p_value < DRIFT_P_VALUE:
                errors.append(f"{col} : dérive détectée (KS p={p_value:.3f})")
        else:
            unseen = set(df[col].dropna()) - set(ref[col].dropna())
            if unseen:
                errors.append(f"{col} : catégories inconnues {sorted(unseen)}")
    return errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-path", required=True)
    parser.add_argument("--reference-path")
    args = parser.parse_args()

    df = pd.read_csv(args.data_path)
    errors = check_format(df)
    if args.reference_path:
        errors += check_representativeness(df, pd.read_csv(args.reference_path))

    if errors:
        print("❌ Validation des données échouée :")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)
    print(f"✅ Données valides ({len(df)} lignes)")


if __name__ == "__main__":
    main()
