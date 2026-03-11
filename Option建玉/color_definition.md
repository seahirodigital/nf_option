# JPX Options Dashboard Color Definition (Rebranded)

This document defines the color palette used in the rebranded JPX Options Dashboard, inspired by modern design principles.

## 1. Primary Palette (Tailwind Configuration)
These colors are defined in the `tailwind.config` section of the dashboard.

| Key | Hex Code | Purpose |
| :--- | :--- | :--- |
| `primary` | `#7C4DFF` | Accent color, Brand purple, Buttons, Positive bars |
| `secondary` | `#651FFF` | Button hover state, Darker accent |
| `bgLight` | `#f8fafc` | Global body background (Slate light) |
| `textPrimary` | `#334155` | Primary headings, Strong text |
| `textSecondary`| `#64748b` | Sub-text, Labels, Chart tick colors |
| `borderLight` | `#e2e8f0` | Panel borders, Grid lines |

---

## 2. Dashboard UI Elements
Specific styling rules for components.

### Header (HP Style)
- **Background**: `white`
- **Bottom Border**: `1px solid #e2e8f0`
- **Text (Title)**: `#7C4DFF` (Bold)
- **Status Text**: `#94a3b8` (Slate 400)
- **Font Size**: All elements set to `text-xs` (approx. 12px) for a minimal look.

### Buttons & Controls
- **Primary Button**: Background `#7C4DFF`, Text `white`
- **Primary Button Hover**: Background `#651FFF`
- **Inputs/Selects**: White background, `#e2e8f0` border, `#7C4DFF` on focus.

### Content Panels
- **Container**: White background, `#e2e8f0` 1px border.
- **Shadow**: `shadow-sm` (subtle shadow for elevation).

---

## 3. Visualization Colors (Charts)
Standardized colors for data representation in Chart.js.

| Data Type | Hex Code | Description |
| :--- | :--- | :--- |
| **Positive / Growth / Call** | `#7C4DFF` | Primary Purple (Rebranded from Emerald Green) |
| **Negative / Decrease / Put** | `#f43f5e` | Rose Red |
| **Trend Line** | `#7C4DFF` | Purple line with gradient fill |
| **Chart Grid Lines** | `#e2e8f0` | Subtle grey |
| **Chart Labels/Ticks** | `#64748b` | Medium grey for readability |
| **Highlighted Strike Price** | `#334155` | Dark grey (weighted semi-bold) for major prices (e.g., 10k intervals) |

---

## 4. Log Area
- **Background**: `#f8fafc`
- **Text**: `#64748b`
- **Success Message**: `#7C4DFF`
- **Error Message**: `#f43f5e`
