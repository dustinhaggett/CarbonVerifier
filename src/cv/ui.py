"""UI helpers — pure HTML-string builders for the Orbital Forensic Interface.

Each function returns a single-line HTML string suitable for
``st.markdown(html, unsafe_allow_html=True)``. Multi-line f-strings break
Streamlit's markdown parser; everything here is one logical string per call."""

from __future__ import annotations

from pathlib import Path

ASSETS = Path(__file__).resolve().parents[2] / "assets"
CSS_PATH = ASSETS / "forensic.css"


# ── Risk-rating mapping ─────────────────────────────────────────────────────
RISK_PILLS = {
    "CRITICAL": "pill-critical",
    "HIGH": "pill-high",
    "MODERATE": "pill-moderate",
    "LOW": "pill-low",
    "VERIFIED": "pill-verified",
    "PENDING": "pill-pending",
    "MONITORING": "pill-monitoring",
}


def load_css() -> str:
    """Return a <style>…</style> block with the design-system CSS embedded."""
    css = CSS_PATH.read_text() if CSS_PATH.exists() else ""
    return f"<style>{css}</style>"


# ── Plain-English glossary for the dashboard ─────────────────────────────────
# Each entry: short term  → one-paragraph explanation aimed at someone who has
# never opened a Verra registry page or a satellite-data tool. Used by the
# tip() helper to wrap inline terms with hover-tooltips, and by the Glossary
# expander in the sidebar as a catch-all reference.
GLOSSARY: dict[str, str] = {
    "VCS": "Verified Carbon Standard — the world's largest voluntary carbon-credit registry, run by Verra. Every project here has a VCS ID like VCS832.",
    "REDD+": "Reducing Emissions from Deforestation and forest Degradation — a category of carbon project where you sell credits for protecting forest that you claim would otherwise be cleared.",
    "Hectare": "10,000 m² — about the size of a soccer pitch. The standard unit for forest area.",
    "Forest 2000": "How much tree-cover (≥30% canopy) the project area had in the year 2000. Year 2000 is the global baseline used by the Hansen forest dataset; all later loss is measured against it.",
    "Post-start loss": "Hectares of forest cleared inside the project boundary AFTER the project officially started selling credits. This is what the credits were sold to prevent.",
    "Additionality": "Did the project actually save forest that would have been lost otherwise? It's the central integrity question for any carbon credit. We test it by comparing the project's loss rate to nearby unprotected land of similar size and biome.",
    "Additionality verdict": "STRONG = project lost much less forest than nearby unprotected land. WEAK = small but positive difference. NONE = no detectable difference. NEGATIVE = project lost MORE forest than controls — credits arguably represent no real climate benefit.",
    "NDVI": "Normalized Difference Vegetation Index — a 0-to-1 satellite measure of how much chlorophyll plants are producing. Healthy Amazon rainforest reads ~0.85; bare ground reads <0.2.",
    "Hansen GFC": "Hansen Global Forest Change — the gold-standard global deforestation dataset, run by University of Maryland. 30-meter resolution, annual since 2001. Free, no auth.",
    "Sentinel-2": "European Space Agency satellite pair providing free 10-meter optical imagery every 5 days. The imagery you see on the map is Sentinel-2.",
    "MGRS tile": "Military Grid Reference System — Sentinel-2 imagery is delivered in fixed 100km×100km tiles. Each tile gets an ID like 22MGB; we pick the same tile each year so the time series is comparable.",
    "Cloud cover": "Percentage of a satellite scene blocked by clouds. We pick the least-cloudy scene per year. <5% is excellent, >20% gets rejected.",
    "Boundary (KML / WDPA)": "The exact polygon defining the project's registered area. KML is the format Verra hosts. WDPA is for protected areas like national parks. Without a real polygon, we fall back to a bounding-box approximation centered on the published coordinates — less accurate.",
    "Carbon credit": "A tradable certificate representing 1 tonne of CO₂ supposedly avoided or removed. Companies buy them to claim 'net zero' or 'carbon neutral' status. The voluntary carbon market is ~$2B/year.",
    "Verra registry": "The publicly searchable database where every VCS-certified project lives. Each project has its own page with documents, issuance history, and (sometimes) a downloadable boundary KML.",
    "Risk pill": "Color-coded summary of the project's credit integrity. CRITICAL (red) / HIGH (red) / MODERATE (orange) / LOW (green) / VERIFIED (green). Derived from the additionality verdict.",
    "Anomaly": "An unusual event the system flagged from the satellite record — typically the worst-loss year inside the project boundary, or a sharp NDVI drop.",
    "LOSS_ID": "Internal label for a detection event — the worst single-year forest loss inside the project boundary, with the area in hectares and a confidence score.",
    "Biomass density": "Approximation of how much living plant matter is in the project area, from satellite vegetation indices. Used here as a 7-year mini-bar-chart of Hansen forest loss; tall red bars mark high-loss years.",
    "EXPORT_DATA": "Click to download a ZIP bundle with this project's full data package: dataset JSON, NDVI timeseries, additionality test, all three Claude reports, time-lapse GIF, and the Folium boundary preview.",
    "NEW_QUERY": "Clear all caches and re-run the analysis from disk. Use after editing projects.json or pulling a fresh KML.",
    "Three voices / Briefs": "Same satellite evidence, three Claude-authored audit reports — Executive (for a sustainability buyer), Investigative (for a journalist), Regulator (for a Verra compliance auditor). Each cites the specific numbers from the Hansen + Sentinel-2 record.",
}


def tip(label: str, key: str | None = None, custom: str | None = None, below: bool = False) -> str:
    """Wrap a label in a hover-tooltip. ``key`` looks up GLOSSARY; ``custom``
    overrides with a one-off explanation. ``below`` flips the tooltip to
    appear under the label (for elements at the top of the screen)."""
    text = custom or GLOSSARY.get(key or label, "")
    if not text:
        return label
    safe = text.replace('"', "&quot;").replace("\n", " ")
    cls = "cv-tip below" if below else "cv-tip"
    return f'<span class="{cls}" data-tip="{safe}">{label}</span>'


def glossary_expander() -> str:
    """Catch-all definitions panel for the sidebar bottom."""
    items = []
    for term, definition in GLOSSARY.items():
        items.append(f'<dt>{term}</dt><dd>{definition}</dd>')
    return (
        '<details>'
        '<summary>GLOSSARY · plain-english</summary>'
        f'<dl>{"".join(items)}</dl>'
        '</details>'
    )


def pill(text: str, kind: str = "pending") -> str:
    """Render an inline status pill. ``kind`` ∈ critical / high / moderate / low /
    verified / pending / monitoring."""
    cls = RISK_PILLS.get(text.upper(), f"pill-{kind.lower()}")
    return f'<span class="pill {cls}">{text}</span>'


def top_bar(
    title: str = "CARBON_VERIFY // SATELLITE_CORE",
    meta: str = "",
    export_href: str | None = None,
    export_filename: str | None = None,
) -> str:
    """Top app bar — brand on left, action cluster (EXPORT_DATA + icons) on right.

    If ``export_href`` is supplied (e.g. a ``data:application/zip;base64,...``
    URL), the EXPORT_DATA pill becomes a real ``<a download>`` link."""
    button_style = (
        "display:inline-flex;align-items:center;padding:4px 10px;"
        "border:1px solid var(--border);background:var(--surface-low);"
        "font-family:var(--font-mono);font-size:10px;font-weight:700;letter-spacing:0.1em;"
        "color:var(--text);text-transform:uppercase;text-decoration:none;cursor:pointer"
    )
    if export_href:
        download_attr = f' download="{export_filename}"' if export_filename else ' download'
        export_el = (
            f'<a href="{export_href}"{download_attr} style="{button_style}" '
            f'title="Download project ZIP bundle">EXPORT_DATA</a>'
        )
    else:
        export_el = f'<span style="{button_style}">EXPORT_DATA</span>'

    icons = (
        '<div style="display:flex;align-items:center;gap:14px">'
        f'{export_el}'
        '<span class="material-symbols-outlined" style="color:var(--text-faint);font-size:18px">settings</span>'
        '<span class="material-symbols-outlined" style="color:var(--text-faint);font-size:18px">notifications</span>'
        '<span class="material-symbols-outlined" style="color:var(--text-faint);font-size:18px">account_circle</span>'
        '</div>'
    )
    meta_html = f'<span class="meta" style="margin-right:14px">{meta}</span>' if meta else ''
    return (
        '<div class="top-bar">'
        f'<span class="brand">{title}</span>'
        f'<div style="display:flex;align-items:center">{meta_html}{icons}</div>'
        '</div>'
    )


def section_header(
    title: str,
    lat: float | None = None,
    lon: float | None = None,
    anomaly: str | None = None,
) -> str:
    """Section header above the KPI strip.
    Optional anomaly line below the title rendered in error red with a pulsing dot."""
    lat_lon = ""
    if lat is not None and lon is not None:
        lat_lon = f'<span class="lat-lon">LAT: {lat:.4f} / LON: {lon:.4f}</span>'
    anomaly_html = f'<div class="anomaly">{anomaly}</div>' if anomaly else ""
    return (
        '<div class="section-header">'
        '<div class="row">'
        f'<h1>{title}</h1>'
        f'{lat_lon}'
        '</div>'
        f'{anomaly_html}'
        '</div>'
    )


def kpi_strip(cells: list[dict]) -> str:
    """Render a 4-cell KPI strip. Each cell is a dict with at least
    {label, value} and optionally {unit, kind: "default"|"error"|"secondary",
    sparkline: list[float] (0..1) | pill_text+pill_kind, tip: str}.
    ``tip`` (or ``tip_key``) wraps the label in a hover-tooltip."""
    parts = []
    for c in cells:
        raw_label = c.get("label", "")
        if c.get("tip"):
            label = tip(raw_label, custom=c["tip"], below=True)
        elif c.get("tip_key"):
            label = tip(raw_label, key=c["tip_key"], below=True)
        else:
            label = raw_label
        value = c.get("value", "")
        unit = f' <span class="unit">{c["unit"]}</span>' if c.get("unit") else ""
        kind = c.get("kind", "default")
        value_cls = {"error": " error", "secondary": " secondary"}.get(kind, "")

        # Render either a plain value, or a pill, or value+sparkline
        if c.get("pill_text"):
            inner = f'<div class="pill {RISK_PILLS.get(c["pill_text"].upper(), "pill-pending")}">{c["pill_text"]}</div>'
        elif c.get("sparkline"):
            bars = "".join(
                f'<div class="spark-bar" style="height:{int(max(8, min(100, h*100)))}%"></div>'
                for h in c["sparkline"]
            )
            inner = (
                f'<div style="display:flex;align-items:flex-end;justify-content:space-between;gap:12px">'
                f'<span class="value{value_cls}">{value}{unit}</span>'
                f'<div class="spark-row" style="width:96px">{bars}</div>'
                f'</div>'
            )
        else:
            inner = f'<span class="value{value_cls}">{value}{unit}</span>'
        parts.append(f'<div class="kpi-cell"><span class="label">{label}</span>{inner}</div>')
    return f'<div class="kpi-strip">{"".join(parts)}</div>'


def panel_open(title: str) -> str:
    return f'<div class="panel"><div class="panel-header">// {title}</div>'


def panel_close() -> str:
    return '</div>'


def anomaly_log(entries: list[dict]) -> str:
    """ANOMALY_LOG side panel.
    Each entry: {head: str, head_kind: "error"|"warn"|"ok", lines: list[str],
    tip: str (optional)}. The panel header itself carries a tooltip explaining
    what an "anomaly" is in this context."""
    panel_label = tip("ANOMALY_LOG", key="Anomaly")
    panel_html = f'<div class="panel"><div class="panel-header">// {panel_label}</div>'

    if not entries:
        return f'{panel_html}<div class="anomaly-entry"><div class="line">No anomalies logged.</div></div></div>'
    parts = []
    for e in entries:
        head_kind = e.get("head_kind", "ok")
        head_label = e.get("head", "")
        if e.get("tip"):
            head_label = tip(head_label, custom=e["tip"])
        lines = "".join(f'<div class="line">{ln}</div>' for ln in e.get("lines", []))
        parts.append(
            f'<div class="anomaly-entry">'
            f'<div class="head {head_kind}">{head_label}</div>'
            f'{lines}'
            f'</div>'
        )
    return f'{panel_html}{"".join(parts)}</div>'


def biomass_density(values: list[dict]) -> str:
    """Mini bar chart for the right rail.
    Each value: {label: str, height: float (0..1), kind: "ok"|"alert"}."""
    bars = []
    for v in values:
        h = max(8, min(100, int(v.get("height", 0) * 100)))
        color_cls = "spark-bar"
        if v.get("kind") == "alert":
            color_cls += ""
            style = f"height:{h}%; background: var(--error); border-top: 1px solid var(--error);"
        else:
            style = f"height:{h}%;"
        bars.append(f'<div class="{color_cls}" style="{style}"></div>')
    labels = "".join(
        f'<span style="color:{"var(--error)" if v.get("kind")=="alert" else "var(--text-faint)"}">{v.get("label","")}</span>'
        for v in values
    )
    return (
        f'{panel_open("BIOMASS_DENSITY")}'
        f'<div style="display:flex;align-items:flex-end;gap:3px;height:80px">{"".join(bars)}</div>'
        f'<div style="display:flex;justify-content:space-between;margin-top:6px;font-family:var(--font-mono);font-size:10px;letter-spacing:0.05em">{labels}</div>'
        f'{panel_close()}'
    )


def status_footer(
    items: dict | None = None,
    live_text: str = "VERIFYING PROJECT COMPLIANCE",
) -> str:
    """Bottom terminal-style status bar."""
    items = items or {"SYSTEM": "READY", "DB_CONNECTION": "SECURE", "SENTINEL_SYNC": "0.02ms"}
    left = "".join(f'<span>{k}: {v}</span>' for k, v in items.items())
    return (
        f'<div class="status-footer">'
        f'<div class="group">{left}</div>'
        f'<div class="group"><span class="live">{live_text}</span><span class="cursor">_</span></div>'
        f'</div>'
    )


def map_hud_header(layer: str, coord: str) -> str:
    """Header bar that sits inside the map module top-left, showing layer & coords."""
    return (
        f'<div style="display:flex;justify-content:space-between;align-items:center;'
        f'padding:6px 10px;background:rgba(15,23,42,0.85);border-bottom:1px solid var(--border);'
        f'font-family:var(--font-mono);font-size:10px;letter-spacing:0.1em">'
        f'<div style="display:flex;gap:10px;color:var(--text-dim)">'
        f'<span>LAYER: {layer}</span>'
        f'<span style="color:var(--text-mute)">|</span>'
        f'<span>COORD: {coord}</span>'
        f'</div>'
        f'</div>'
    )


def sector_nav(label: str = "SECTOR_NAV", sub: str = "ORBIT_SNTL_2") -> str:
    """Header at the top of the sidebar."""
    return (
        f'<div class="sector-nav">'
        f'<div class="icon-box"><span class="material-symbols-outlined" style="color:var(--accent-bright);font-size:18px">radar</span></div>'
        f'<div class="label-stack">'
        f'<div class="title">{label}</div>'
        f'<div class="sub">{sub}</div>'
        f'</div>'
        f'</div>'
    )


_STATUS_ICON = {
    "critical": "warning",
    "high": "warning",
    "moderate": "radar",
    "low": "verified",
    "verified": "verified",
    "pending": "schedule",
    "monitoring": "analytics",
}


def project_row(label: str, status: str, status_kind: str, active: bool = False) -> str:
    """Sidebar project row with a trailing status pill + Material Symbols icon."""
    border = "border-left: 2px solid var(--accent-bright);" if active else "border-left: 2px solid transparent;"
    bg = "background: rgba(15,23,42,0.6);" if active else ""
    color = "color: var(--accent-bright);" if active else "color: var(--text-faint);"
    icon = _STATUS_ICON.get(status_kind.lower(), "flag")
    return (
        f'<div style="{border} {bg} {color} padding: 9px 14px; '
        f'display:flex; justify-content:space-between; align-items:center; gap:8px; '
        f'font-family:var(--font-mono); font-size:10px; letter-spacing:0.1em; '
        f'text-transform:uppercase; font-weight:700;">'
        f'<span style="display:flex;align-items:center;gap:8px;flex:1;min-width:0">'
        f'<span class="material-symbols-outlined" style="font-size:16px">{icon}</span>'
        f'<span style="overflow:hidden;text-overflow:ellipsis;white-space:nowrap">{label}</span>'
        f'</span>'
        f'{pill(status, status_kind)}'
        f'</div>'
    )
