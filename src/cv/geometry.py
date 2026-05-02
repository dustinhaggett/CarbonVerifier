"""Geometry utilities — load project boundaries from KML or GeoJSON into a
shapely MultiPolygon.

We deliberately use stdlib XML + shapely rather than fiona/geopandas, since
driver support varies and we only need the outer-ring polygons here."""

from __future__ import annotations

import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

from shapely.geometry import MultiPolygon, Polygon, shape
from shapely.ops import unary_union

KML_NS = {"k": "http://www.opengis.net/kml/2.2"}


def _parse_coord_block(text: str) -> list[tuple[float, float]]:
    """Pull (lon, lat) pairs out of a KML <coordinates> string. Altitude (3rd
    component) is dropped; we only care about the 2D footprint."""
    out: list[tuple[float, float]] = []
    for match in re.finditer(r"(-?\d+(?:\.\d+)?),(-?\d+(?:\.\d+)?)", text):
        out.append((float(match.group(1)), float(match.group(2))))
    return out


def _localname(tag: str) -> str:
    """Strip the {namespace} prefix from an etree tag, returning the local name."""
    return tag.rsplit("}", 1)[-1] if "}" in tag else tag


def _load_kml_via_regex(text: str) -> list[Polygon]:
    """Last-resort parser for KMLs with malformed XML namespaces (e.g. files
    that reference ``xsi:`` without declaring it)."""
    polys: list[Polygon] = []
    # Match <Polygon>... up to the first matching </Polygon> (greedy outer boundary)
    for poly_match in re.finditer(r"<Polygon\b[^>]*>(.*?)</Polygon>", text, re.DOTALL | re.IGNORECASE):
        body = poly_match.group(1)
        # Inside, find <outerBoundaryIs>...<coordinates>...</coordinates></LinearRing>
        outer = re.search(
            r"<outerBoundaryIs\b[^>]*>.*?<coordinates\b[^>]*>(.*?)</coordinates>",
            body,
            re.DOTALL | re.IGNORECASE,
        )
        if not outer:
            continue
        coords = _parse_coord_block(outer.group(1))
        if len(coords) < 4:
            continue
        polys.append(Polygon(coords))
    return polys


def load_kml_polygons(path: Path) -> MultiPolygon:
    """Return all <Polygon><outerBoundaryIs> rings as a single (Multi)Polygon.

    Namespace-agnostic — Verra's exports use ``kml/2.2`` (current),
    ``earth.google.com/kml/2.0`` (legacy Google Earth used by older PDDs),
    and occasionally ship malformed namespace declarations (e.g. ``xsi:``
    without an attribute declaration). Falls back to a regex parser if
    strict XML parsing rejects the file.
    Inner rings (holes) are dropped — the demo projects don't use them.
    ``buffer(0)`` repairs any minor self-intersection from coarse coords."""
    polygons: list[Polygon] = []
    try:
        tree = ET.parse(path)
        root = tree.getroot()
        for el in root.iter():
            if _localname(el.tag) != "Polygon":
                continue
            ring_text: str | None = None
            for sub in el.iter():
                if _localname(sub.tag) == "coordinates" and sub.text:
                    ring_text = sub.text
                    break
            if not ring_text:
                continue
            coords = _parse_coord_block(ring_text)
            if len(coords) < 4:
                continue
            polygons.append(Polygon(coords))
    except ET.ParseError:
        polygons = _load_kml_via_regex(path.read_text(errors="ignore"))

    if not polygons:
        raise ValueError(f"No polygons found in KML: {path}")

    union = unary_union(polygons)
    if isinstance(union, Polygon):
        return MultiPolygon([union])
    if isinstance(union, MultiPolygon):
        return union
    # Geometry collection — pull polygons out
    return MultiPolygon([g.buffer(0) for g in union.geoms if g.geom_type in ("Polygon", "MultiPolygon")])


def load_geojson_polygons(path: Path) -> MultiPolygon:
    """Read polygons from a GeoJSON FeatureCollection (or single Feature/geometry).
    Handles MultiPolygon by exploding into the union of its parts."""
    raw = json.loads(path.read_text())

    if raw.get("type") == "FeatureCollection":
        geoms = [shape(f["geometry"]) for f in raw["features"] if f.get("geometry")]
    elif raw.get("type") == "Feature":
        geoms = [shape(raw["geometry"])]
    else:
        geoms = [shape(raw)]

    polys: list[Polygon] = []
    for g in geoms:
        if g.geom_type == "Polygon":
            polys.append(g)
        elif g.geom_type == "MultiPolygon":
            polys.extend(list(g.geoms))

    if not polys:
        raise ValueError(f"No polygons in GeoJSON: {path}")

    union = unary_union(polys)
    if isinstance(union, Polygon):
        return MultiPolygon([union])
    if isinstance(union, MultiPolygon):
        return union
    return MultiPolygon([g.buffer(0) for g in union.geoms if g.geom_type in ("Polygon", "MultiPolygon")])


def load_geometry(path: Path) -> MultiPolygon:
    """Dispatch on extension. Returns a MultiPolygon."""
    ext = path.suffix.lower()
    if ext in (".kml",):
        return load_kml_polygons(path)
    if ext in (".geojson", ".json"):
        return load_geojson_polygons(path)
    raise ValueError(f"Unsupported boundary file extension: {ext}")
