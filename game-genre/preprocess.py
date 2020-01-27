from fastai.vision import (
    ImageList,
    get_transforms,
    imagenet_stats,
    get_transforms,
    DataBunch,
)
import pandas as pd

# TODO Put all parameters in one file for consistency
CSV_LOCATION = "image-labels.csv"
GENRE_NAMES = [
    "Action",
    "Adventure",
    "Arcade",
    "Board Games",
    "Card",
    "Casual",
    "Educational",
    "Family",
    "Fighting",
    "Indie",
    "Massively Multiplayer",
    "Platformer",
    "Puzzle",
    "RPG",
    "Racing",
    "Shooter",
    "Simulation",
    "Sports",
    "Strategy",
]
ROOT_FOLDER = "D:\\Anton\\IgnoredDocuments\\projects\\game-genre\\images\\"


def load_df(location: str = CSV_LOCATION):
    with open(CSV_LOCATION, "r", encoding="utf-16") as csv_file:
        df = pd.read_csv(csv_file)
    return df


def clean_df(df: pd.DataFrame) -> pd.DataFrame:
    df = df.drop_duplicates("id")
    df["image_location"] = df["image_location"].replace("None", None)
    df = df.dropna()
    return df.sample(1000)


def extract_genres(df: pd.DataFrame, genre_column: str = "genres") -> pd.DataFrame:
    other_columns = df.loc[:, df.columns != genre_column]
    new_df = pd.concat(
        [other_columns, df[genre_column].str.get_dummies(sep="-")], axis="columns"
    )
    return new_df


def create_databunch(df, validation_fraction: float = 0.2) -> DataBunch:
    tfms = get_transforms(max_warp=0.0, max_zoom=1)
    data_bunch = (
        ImageList.from_df(df, path=ROOT_FOLDER, cols="image_location")
        .split_by_rand_pct(0.2)
        .label_from_df(cols=GENRE_NAMES)
        # .datasets()
        .transform(tfms, size=224)
        .databunch()
        .normalize(imagenet_stats)
    )
    return data_bunch


def preprocess_csv(location: str = CSV_LOCATION):
    df = load_df()
    df = clean_df(df)
    df = extract_genres(df)
    data = create_databunch(df)
    return data


if __name__ == "__main__":
    preprocess_csv()
