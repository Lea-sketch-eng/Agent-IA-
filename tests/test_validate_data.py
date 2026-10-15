import pandas as pd
from validate_data import check_format, check_representativeness


def make_df(**overrides):
    data = {
        "Age": [23, 47, 61],
        "Sex": ["F", "M", "F"],
        "BP": ["HIGH", "LOW", "NORMAL"],
        "Cholesterol": ["HIGH", "HIGH", "NORMAL"],
        "Na_to_K": [25.3, 13.0, 18.0],
    }
    data.update(overrides)
    return pd.DataFrame(data)


def test_valid_data_passes():
    assert check_format(make_df()) == []


def test_missing_column_is_reported():
    errors = check_format(make_df().drop(columns="BP"))
    assert any("Colonnes manquantes" in e for e in errors)


def test_out_of_range_and_missing_values_are_reported():
    errors = check_format(make_df(Age=[-3, 47, 200], Na_to_K=[None, 13.0, 18.0]))
    assert any("Age : valeurs < 0" in e for e in errors)
    assert any("Age : valeurs > 120" in e for e in errors)
    assert any("Na_to_K" in e and "manquantes" in e for e in errors)


def test_wrong_type_is_reported():
    errors = check_format(make_df(Age=["vingt", "trente", "quarante"]))
    assert any("type numérique attendu" in e for e in errors)


def test_unseen_category_is_reported():
    errors = check_representativeness(make_df(Sex=["F", "X", "M"]), make_df())
    assert errors == ["Sex : catégories inconnues ['X']"]


def test_numeric_drift_is_detected():
    ref = make_df(
        Age=list(range(20, 50)), Sex=["F"] * 30, BP=["LOW"] * 30,
        Cholesterol=["HIGH"] * 30, Na_to_K=[15.0] * 30,
    )
    new = ref.assign(Age=list(range(80, 110)))
    assert any("Age : dérive détectée" in e for e in check_representativeness(new, ref))
