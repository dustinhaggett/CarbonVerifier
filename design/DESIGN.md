---
name: Orbital Forensic Interface
colors:
  surface: '#131314'
  surface-dim: '#131314'
  surface-bright: '#3a393a'
  surface-container-lowest: '#0e0e0f'
  surface-container-low: '#1c1b1c'
  surface-container: '#201f20'
  surface-container-high: '#2a2a2b'
  surface-container-highest: '#353435'
  on-surface: '#e5e2e2'
  on-surface-variant: '#c6c6cc'
  inverse-surface: '#e5e2e2'
  inverse-on-surface: '#313031'
  outline: '#909096'
  outline-variant: '#46464c'
  surface-tint: '#c3c6d4'
  primary: '#c3c6d4'
  on-primary: '#2c303b'
  primary-container: '#0b0f19'
  on-primary-container: '#787b88'
  inverse-primary: '#5a5e6a'
  secondary: '#4de082'
  on-secondary: '#003919'
  secondary-container: '#00b55d'
  on-secondary-container: '#003e1c'
  tertiary: '#ffb783'
  on-tertiary: '#4f2500'
  tertiary-container: '#1e0a00'
  on-tertiary-container: '#bf6308'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#dfe2f1'
  primary-fixed-dim: '#c3c6d4'
  on-primary-fixed: '#171b26'
  on-primary-fixed-variant: '#434652'
  secondary-fixed: '#6dfe9c'
  secondary-fixed-dim: '#4de082'
  on-secondary-fixed: '#00210c'
  on-secondary-fixed-variant: '#005227'
  tertiary-fixed: '#ffdcc5'
  tertiary-fixed-dim: '#ffb783'
  on-tertiary-fixed: '#301400'
  on-tertiary-fixed-variant: '#713700'
  background: '#131314'
  on-background: '#e5e2e2'
  surface-variant: '#353435'
typography:
  headline-xl:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '700'
    lineHeight: 32px
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '600'
    lineHeight: 24px
    letterSpacing: -0.01em
  body-base:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  data-mono:
    fontFamily: Space Grotesk
    fontSize: 13px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.05em
  label-caps:
    fontFamily: Space Grotesk
    fontSize: 11px
    fontWeight: '700'
    lineHeight: 12px
    letterSpacing: 0.1em
spacing:
  unit: 4px
  gutter: 16px
  margin: 24px
  panel-padding: 12px
  density-ratio: tight
---

## Brand & Style

This design system is engineered for high-stakes environmental verification and satellite telemetry analysis. The brand personality is authoritative, precise, and forensic. It evokes the "mission critical" urgency of a NASA control room blended with the information density and speed of a Bloomberg Terminal.

The aesthetic follows a **Technical Minimalism** approach with **Cyber-Forensic** accents. It prioritizes utility over decoration, utilizing sharp geometric lines, high-density data visualization, and subtle glow effects to simulate an active glowing console. The emotional response is one of total situational awareness—providing the user with a "god-view" of planetary data that feels scientific, verified, and indisputable.

## Colors

The palette is anchored in a deep navy void, designed for long-duration monitoring with minimal eye strain. 

- **Base:** The primary background (#0B0F19) provides a cinematic depth.
- **Vegetation/Growth:** Muted green (#4ADE80) is reserved for healthy biomes and positive delta verification.
- **Risk/Caution:** Alarm orange (#FB923C) identifies anomalies, infrastructure changes, or drought indices.
- **Critical:** Alert red (#F87171) is used strictly for deforestation events, illegal mining, or sensor failure.
- **UI Accents:** Brighter cyan and slate tints are used for grid lines and non-semantic technical data.

Use "glow" variants of these colors (15% opacity fills with 4px blurs) to highlight active tracking targets or live data streams.

## Typography

This design system utilizes a dual-font strategy to balance readability with technical aesthetics. 

**Inter** handles all primary interface elements, body text, and structural labels, providing a clean, neutral foundation. 
**Space Grotesk** (serving as the monospace surrogate) is used for all dynamic data values, coordinates, timestamps, and "readout" text. 

Maintain high density by favoring smaller font sizes (13-14px) for body content. All numerical data must be monospaced to prevent "jumping" during live telemetry updates.

## Layout & Spacing

The layout follows a **Fixed-Modular Grid** system. The screen is divided into functional quadrants or "tiles" that do not overlap, maximizing the use of screen real estate.

- **Grid:** Use a 12-column underlying structure, but group columns into 3 or 4 main dashboard panels.
- **Rhythm:** A 4px base unit ensures tight alignment. Gutters between panels are kept at a lean 16px to maintain the "Terminal" feel.
- **Density:** High information density is a requirement. Padding inside data tables and lists should be minimal (8px vertical) to ensure maximum data visibility without scrolling.

## Elevation & Depth

In this design system, depth is conveyed through **Tonal Layering and Sharp Borders** rather than traditional shadows.

- **Surface Tiers:** Background is Level 0 (#0B0F19). Panels are Level 1 (#161B22). Tooltips or Modals are Level 2 (#1E293B).
- **Borders:** Every container must have a 1px solid border. Use `#334155` for inactive panels and the semantic colors (green/orange/red) for active or alerted panels.
- **Subtle Glow:** Apply a `drop-shadow(0 0 4px color)` only to active status indicators and critical data points to simulate the luminescence of a high-end CRT or LCD console.
- **Scanlines:** A very low opacity (2%) horizontal linear-gradient can be overlaid on map modules to enhance the forensic satellite aesthetic.

## Shapes

The shape language is strictly **Geometric and Sharp**. 

All UI elements—including buttons, cards, input fields, and panels—use 0px border radii. This reinforces the scientific and industrial nature of the dashboard. Circular elements are permitted only for status pips, radio buttons, and compass/azimuth dials. Hexagonal or chamfered corners may be used for highly specialized "Verification Badges" to distinguish them from standard UI boxes.

## Components

- **Buttons:** Rectangular with 1px borders. Primary buttons use a ghost style (transparent fill, colored border) that fills solid on hover. Use Space Grotesk for button labels in all-caps.
- **Data Cells:** High-density rows with hairline dividers. Values should be right-aligned in monospace; labels left-aligned in Inter.
- **Telemetry Chips:** Small, rectangular tags used for metadata (e.g., "SATELLITE: SENTINEL-2"). Background matches the surface; border indicates status.
- **Input Fields:** Flat bottom-border only or full 1px border. Focus state is indicated by a subtle outer glow in the primary accent color.
- **Status Indicators:** Small 8px squares (not circles) that pulse when data is "Live."
- **Dashboard Tiles:** Each tile must have a header bar with a "breadcrumb" or "coordinate" string in the top-left corner to denote the data's origin.
- **Additional Components:**
    - **Histogram/Sparklines:** Integrated directly into data rows to show 24h trends.
    - **Coordinate Crosshairs:** A persistent overlay on map modules for precise targeting.
    - **Breadcrumb HUD:** A top-level bar showing "Orbit > Sector > Plot" pathing.