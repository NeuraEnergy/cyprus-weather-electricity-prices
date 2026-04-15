"""Minimal loader example — zero dependencies beyond pandas.

Usage
-----
    python load_dataset.py

Loads the joined weather + prices CSV and prints a quick summary. Intended
as a starting point you can copy into your own scripts or notebooks.
"""

from pathlib import Path
import pandas as pd


def load(data_dir: Path | str = None) -> pd.DataFrame:
    """Load the joined weather + prices dataset.

    Parameters
    ----------
    data_dir : Path or str, optional
        Path to the `data/` directory. Defaults to `../data/` relative
        to this file so the example works in-place after cloning.
    """
    if data_dir is None:
        data_dir = Path(__file__).resolve().parent.parent / "data"
    data_dir = Path(data_dir)
    df = pd.read_csv(
        data_dir / "weather_prices_joined.csv",
        parse_dates=["timestamp", "price_period_start", "price_period_end"],
    )
    return df


def summary(df: pd.DataFrame) -> None:
    print(f"Rows:            {len(df):,}")
    print(f"Columns:         {len(df.columns)}")
    print(f"Time span:       {df['timestamp'].min()}  ->  {df['timestamp'].max()}")
    print(f"Avg temp:        {df['temp_c'].mean():.1f} C")
    print(f"Temp range:      {df['temp_c'].min():.1f} - {df['temp_c'].max():.1f} C")
    print(f"Avg price:       EUR {df['price_eur_per_mwh'].mean():.1f} / MWh")
    print(f"Price range:     EUR {df['price_eur_per_mwh'].min():.1f} - "
          f"{df['price_eur_per_mwh'].max():.1f} / MWh")


if __name__ == "__main__":
    df = load()
    summary(df)
