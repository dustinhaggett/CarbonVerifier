import json
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path

from shapely.geometry.base import BaseGeometry
from shapely.geometry import MultiPolygon, box

from .geometry import load_geometry
from .paths import PROJECTS_JSON, ROOT


@dataclass
class Project:
    id: str
    name: str
    country: str
    hectares: int
    project_start: str
    first_credit_issuance: str
    centroid_lat: float
    centroid_lon: float
    bbox: tuple[float, float, float, float]
    buyers_known: list[str]
    scandal_notes: str
    registry_url: str
    boundary_source: str
    preferred_mgrs_tile: str | None = None
    kml_path: str | None = None
    sentinel_require_contains_bbox: bool = True

    @cached_property
    def geometry(self) -> BaseGeometry:
        """Real polygon if a boundary file is registered, otherwise a bbox rectangle."""
        if self.kml_path:
            p = Path(self.kml_path)
            if not p.is_absolute():
                p = ROOT / p
            return load_geometry(p)
        return MultiPolygon([box(*self.bbox)])

    @property
    def effective_bbox(self) -> tuple[float, float, float, float]:
        """Bbox derived from the actual geometry (KML or registered bbox)."""
        minx, miny, maxx, maxy = self.geometry.bounds
        return (minx, miny, maxx, maxy)


def load_projects() -> list[Project]:
    raw = json.loads(PROJECTS_JSON.read_text())
    out: list[Project] = []
    for p in raw["projects"]:
        out.append(
            Project(
                id=p["id"],
                name=p["name"],
                country=p["country"],
                hectares=p["hectares"],
                project_start=p["project_start"],
                first_credit_issuance=p["first_credit_issuance"],
                centroid_lat=p["centroid_lat"],
                centroid_lon=p["centroid_lon"],
                bbox=tuple(p["bbox"]),
                buyers_known=p["buyers_known"],
                scandal_notes=p["scandal_notes"],
                registry_url=p["registry_url"],
                boundary_source=p["boundary_source"],
                preferred_mgrs_tile=p.get("preferred_mgrs_tile"),
                kml_path=p.get("kml_path"),
                sentinel_require_contains_bbox=p.get("sentinel_require_contains_bbox", True),
            )
        )
    return out


def get_project(project_id: str) -> Project:
    for p in load_projects():
        if p.id == project_id:
            return p
    raise KeyError(f"Unknown project: {project_id}")
