import pandas as pd

from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer


NUMERIC_FEATURES = [
    "Study_Hours",
    "Attendance",
    "Previous_Score",
    "Assignment_Score",
    "Internal_Assessment",
    "Quiz_Score",
    "Sleep_Hours",
    "Previous_GPA",
    "Backlogs",
    "Internet_Usage",
    "Participation"
]

CATEGORICAL_FEATURES = [
    "Extracurricular"
]


def get_preprocessing_pipeline(
    numeric_features=None,
    categorical_features=None
):

    if numeric_features is None:
        numeric_features = NUMERIC_FEATURES

    if categorical_features is None:
        categorical_features = CATEGORICAL_FEATURES

    numeric_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler())
        ]
    )

    categorical_transformer = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(
                    strategy="most_frequent"
                )
            ),
            (
                "onehot",
                OneHotEncoder(
                    handle_unknown="ignore",
                    sparse_output=False
                )
            )
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "numeric",
                numeric_transformer,
                numeric_features
            ),
            (
                "categorical",
                categorical_transformer,
                categorical_features
            )
        ]
    )

    return preprocessor


def clean_data(df):

    if not isinstance(df, pd.DataFrame):
        raise TypeError(
            "Input must be a pandas DataFrame."
        )

    df = df.copy()

    # Clean column names
    df.columns = (
        df.columns
        .str.strip()
        .str.replace(" ", "_")
    )

    # Remove completely empty rows
    df = df.dropna(how="all")

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Numeric columns
    numeric_columns = NUMERIC_FEATURES + ["Final_Score"]

    for col in numeric_columns:

        if col in df.columns:

            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

    # Keep score-related values in valid ranges
    score_columns = [
        "Attendance",
        "Previous_Score",
        "Assignment_Score",
        "Internal_Assessment",
        "Quiz_Score",
        "Final_Score"
    ]

    for col in score_columns:

        if col in df.columns:
            df[col] = df[col].clip(0, 100)

    # GPA should normally be between 0 and 10
    if "Previous_GPA" in df.columns:
        df["Previous_GPA"] = df["Previous_GPA"].clip(0, 10)

    # Backlogs cannot be negative
    if "Backlogs" in df.columns:
        df["Backlogs"] = df["Backlogs"].clip(lower=0)

    return df


def validate_data(df):

    required_columns = (
        NUMERIC_FEATURES
        + CATEGORICAL_FEATURES
        + ["Final_Score"]
    )

    missing_columns = [
        col
        for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:

        raise ValueError(
            "Missing columns: "
            + ", ".join(missing_columns)
        )

    return True