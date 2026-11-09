from math import asin, cos, radians, sin, sqrt
from pathlib import Path
from csv import DictReader
from urllib.request import urlopen
from html import escape

def load_locations():
    path = Path(__file__).with_name("locations.csv")
    with path.open(encoding="utf-8-sig", newline="") as source:
        rows = list(DictReader(source))
    return [(float(row["lat"]), float(row["lon"])) for row in rows], [row["name"] for row in rows]


def distance(first, second):
    lat_a, lon_a = map(radians, first)
    lat_b, lon_b = map(radians, second)
    haversine = sin((lat_b - lat_a) / 2) ** 2
    haversine += cos(lat_a) * cos(lat_b) * sin((lon_b - lon_a) / 2) ** 2
    return 12742 * asin(sqrt(min(1, haversine)))


def length(route):
    return sum(distance(POINTS[a], POINTS[b]) for a, b in zip(route, route[1:]))


def nearest_neighbor():
    route = [0]
    remaining = set(range(1, len(POINTS)))
    while remaining:
        stop = min(remaining, key=lambda index: (distance(POINTS[route[-1]], POINTS[index]), index))
        route.append(stop)
        remaining.remove(stop)
    return route + [0]


def improve(route):
    while True:
        best = route
        best_length = length(route)
        for start in range(1, len(route) - 2):
            for end in range(start + 1, len(route) - 1):
                candidate = route[:start] + route[start:end + 1][::-1] + route[end + 1:]
                candidate_length = length(candidate)
                if candidate_length < best_length - 1e-9:
                    best, best_length = candidate, candidate_length
        if best == route:
            return route
        route = best


def draw_routes(original, improved):
    latitudes, longitudes = zip(*POINTS)
    scale = min(270 / (max(longitudes) - min(longitudes)), 215 / (max(latitudes) - min(latitudes)))
    coordinates = [(30 + (lon - min(longitudes)) * scale,
                    25 + (max(latitudes) - lat) * scale) for lat, lon in POINTS]
    svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="680" height="300">']
    svg.append('<rect width="100%" height="100%" fill="white"/>')
    for route, offset, color, label in [
        (original, 0, "#a13c21", "Plus proche voisin"),
        (improved, 340, "#006b61", "Après 2-opt"),
    ]:
        path = " ".join(f"{coordinates[i][0] + offset:.1f},{coordinates[i][1]:.1f}" for i in route)
        svg.append(f'<polyline points="{path}" stroke="{color}" stroke-width="2" fill="none"/>')
        for index, (x, y) in enumerate(coordinates):
            svg.append(f'<circle cx="{x + offset}" cy="{y}" r="4" fill="{color}"><title>{escape(NAMES[index])}</title></circle>')
            svg.append(f'<text x="{x + offset + 6}" y="{y - 5}" font-size="11">{index}</text>')
        svg.append(f'<text x="{30 + offset}" y="282">{label} · {length(route):.1f} km</text>')
    Path("tours.svg").write_text("\n".join(svg + ["</svg>"]), encoding="utf-8")


if __name__ == "__main__":
    POINTS, NAMES = load_locations()
    original = nearest_neighbor()
    improved = improve(original)
    assert original[0] == improved[0] == original[-1] == improved[-1] == 0
    assert sorted(improved[1:-1]) == list(range(1, len(POINTS)))
    assert length(improved) <= length(original)
    draw_routes(original, improved)
    print(f"Plus proche voisin : {length(original):.2f} km")
    print(f"Après 2-opt : {length(improved):.2f} km")



