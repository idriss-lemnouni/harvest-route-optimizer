from csv import DictReader, DictWriter
from io import TextIOWrapper
from pathlib import Path
from urllib.request import urlopen

SOURCE = "https://raw.githubusercontent.com/plotly/datasets/master/2014_us_cities.csv"
NAMES = ("Los Angeles", "San Diego", "San Jose", "San Francisco", "Fresno",
         "Sacramento", "Long Beach", "Oakland", "Bakersfield", "Riverside", "Stockton")


def extract(stream, output):
    cities = {}
    for row in DictReader(stream):
        name = row["name"].strip()
        if name in NAMES:
            cities.setdefault(name, {"name": name, "lat": row["lat"], "lon": row["lon"]})
    selected = [cities[name] for name in NAMES]
    writer = DictWriter(output, fieldnames=("name", "lat", "lon"))
    writer.writeheader()
    writer.writerows(selected)


if __name__ == "__main__":
    from io import StringIO
    result = StringIO()
    with urlopen(SOURCE, timeout=30) as response:
        extract(TextIOWrapper(response, encoding="utf-8-sig"), result)
    Path(__file__).with_name("locations.csv").write_text(result.getvalue(), encoding="utf-8", newline="")
