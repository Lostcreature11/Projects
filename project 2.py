
import pandas as pd

def load_dataset():
    path = input("Enter the path of your CSV file: ").strip()
    try:
        df = pd.read_csv(path)
        print("\nDataset loaded successfully.")
        print("Shape:", df.shape)
        print("\nColumn Information:")
        print(df.info())
        return df
    except Exception as e:
        print("Error loading file:", e)
        return None


def remove_duplicates(df):
    before = df.shape[0]
    df = df.drop_duplicates()
    after = df.shape[0]
    print(f"Removed {before - after} duplicate rows.")
    return df


def drop_columns(df):
    print("\nAvailable columns:")
    print(df.columns.tolist())
    cols = input("Enter column names to drop (comma separated): ").strip()
    columns_to_drop = [c.strip() for c in cols.split(",") if c.strip() in df.columns]
    df = df.drop(columns=columns_to_drop)
    print("Dropped columns:", columns_to_drop)
    return df


def handle_missing(df):
    print("\nHandling missing values...")
    strategy = input("Choose strategy (mean / median / mode / drop): ").strip().lower()

    for col in df.columns:
        if df[col].isna().sum() > 0:
            if strategy == "mean" and df[col].dtype != "object":
                df[col].fillna(df[col].mean(), inplace=True)
            elif strategy == "median" and df[col].dtype != "object":
                df[col].fillna(df[col].median(), inplace=True)
            elif strategy == "mode":
                df[col].fillna(df[col].mode()[0], inplace=True)
            elif strategy == "drop":
                df = df.dropna()
                break

    print("Missing value handling completed.")
    return df


def convert_dates(df):
    print("\nAvailable columns:")
    print(df.columns.tolist())
    col = input("Enter column name to convert to datetime (or press Enter to skip): ").strip()
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], errors="coerce")
        print(f"Converted {col} to datetime format.")
    return df


def clean_text(df):
    choice = input("Do you want to standardize text columns? (yes/no): ").strip().lower()
    if choice == "yes":
        for col in df.select_dtypes(include="object").columns:
            df[col] = df[col].str.strip().str.lower()
        print("Text columns standardized.")
    return df


def save_dataset(df):
    filename = input("Enter name for cleaned output file (without .csv): ").strip()
    df.to_csv(f"{filename}.csv", index=False)
    print(f"Cleaned dataset saved as {filename}.csv")


if __name__ == "__main__":
    print("==== Interactive Data Cleaning Tool ====\n")

    dataframe = load_dataset()

    if dataframe is not None:

        if input("Remove duplicate rows? (yes/no): ").strip().lower() == "yes":
            dataframe = remove_duplicates(dataframe)

        if input("Drop unwanted columns? (yes/no): ").strip().lower() == "yes":
            dataframe = drop_columns(dataframe)

        if input("Handle missing values? (yes/no): ").strip().lower() == "yes":
            dataframe = handle_missing(dataframe)

        if input("Convert any column to datetime? (yes/no): ").strip().lower() == "yes":
            dataframe = convert_dates(dataframe)

        dataframe = clean_text(dataframe)

        save_dataset(dataframe)

        print("\nData cleaning process completed successfully.")