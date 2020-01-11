from fastai.vision import ImageDataBunch
import pandas as pd

#TODO Put all parameters in one file for consistency
CSV_LOCATION = "image-labels.csv"
GENRE_NAMES = ['Action', 'Adventure', 'Arcade', 'Board Games', 'Card', 'Casual',
       'Educational', 'Family', 'Fighting', 'Indie', 'Massively Multiplayer',
       'Platformer', 'Puzzle', 'RPG', 'Racing', 'Shooter', 'Simulation',
       'Sports', 'Strategy']


def load_df(location: str = CSV_LOCATION):
    with open(CSV_LOCATION, "r", encoding="utf-16") as csv_file:
        df = pd.read_csv(csv_file)
    return df

def clean_df(df: pd.DataFrame) -> pd.DataFrame:
    df = df.drop_duplicates("id")
    df["image_location"] = df["image_location"].replace("None", None)
    df = df.dropna()
    return df

def extract_genres(df: pd.DataFrame, genre_column: str = "genres" ) -> pd.DataFrame:
    other_columns = df.loc[:, df.columns != genre_column]
    new_df = pd.concat([
        other_columns, 
        df[genre_column].str.get_dummies(sep="-")
    ], axis="columns")
    return new_df

def create_databunch(df, validation_fraction: float = 0.2) -> ImageDataBunch:
    return ImageDataBunch.from_df("D:\\", df, valid_pct=validation_fraction, fn_col="image_location", label_col=GENRE_NAMES, size=224)

def preprocess_csv(location: str = CSV_LOCATION):
    df = load_df()
    df = clean_df(df)
    df = extract_genres(df)
    data = create_databunch(df)
    return data

if __name__ == "__main__":
    preprocess_csv()