---
name: MoodLens AI
colors:
  surface: '#0f131d'
  surface-dim: '#0f131d'
  surface-bright: '#353944'
  surface-container-lowest: '#0a0e18'
  surface-container-low: '#171b26'
  surface-container: '#1c1f2a'
  surface-container-high: '#262a35'
  surface-container-highest: '#313540'
  on-surface: '#dfe2f1'
  on-surface-variant: '#cac4d4'
  inverse-surface: '#dfe2f1'
  inverse-on-surface: '#2c303b'
  outline: '#948e9d'
  outline-variant: '#494552'
  surface-tint: '#cebdff'
  primary: '#cebdff'
  on-primary: '#381385'
  primary-container: '#a78bfa'
  on-primary-container: '#3c1989'
  inverse-primary: '#674bb5'
  secondary: '#c0c1ff'
  on-secondary: '#1000a9'
  secondary-container: '#3131c0'
  on-secondary-container: '#b0b2ff'
  tertiary: '#ccbeff'
  on-tertiary: '#332664'
  tertiary-container: '#a193d9'
  on-tertiary-container: '#372a68'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#e8ddff'
  primary-fixed-dim: '#cebdff'
  on-primary-fixed: '#21005e'
  on-primary-fixed-variant: '#4f319c'
  secondary-fixed: '#e1e0ff'
  secondary-fixed-dim: '#c0c1ff'
  on-secondary-fixed: '#07006c'
  on-secondary-fixed-variant: '#2f2ebe'
  tertiary-fixed: '#e7deff'
  tertiary-fixed-dim: '#ccbeff'
  on-tertiary-fixed: '#1e0e4e'
  on-tertiary-fixed-variant: '#4a3d7c'
  background: '#0f131d'
  on-background: '#dfe2f1'
  surface-variant: '#313540'
typography:
  headline-xl:
    fontFamily: Plus Jakarta Sans
    fontSize: 40px
    fontWeight: '700'
    lineHeight: 48px
    letterSpacing: -0.02em
  headline-xl-mobile:
    fontFamily: Plus Jakarta Sans
    fontSize: 30px
    fontWeight: '700'
    lineHeight: 38px
    letterSpacing: -0.015em
  headline-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
    letterSpacing: -0.015em
  headline-lg-mobile:
    fontFamily: Plus Jakarta Sans
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
    letterSpacing: -0.01em
  headline-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 18px
    fontWeight: '600'
    lineHeight: 26px
    letterSpacing: -0.005em
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
    letterSpacing: 0em
  body-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
    letterSpacing: 0.005em
  body-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 16px
    letterSpacing: 0.01em
  label-lg:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 20px
    letterSpacing: 0.01em
  label-md:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.02em
  label-sm:
    fontFamily: Inter
    fontSize: 11px
    fontWeight: '600'
    lineHeight: 14px
    letterSpacing: 0.04em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  gutter: 1.5rem
  gutter-mobile: 1rem
  margin: 2rem
  margin-mobile: 1rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2.5rem
---

## Brand & Style

The design system establishes a high-precision, contemplative, and scientific interface for natural language emotion intelligence. It bridges deep computational NLP analysis with human emotional resonance. The atmosphere is clinical yet luminous: dark obsidian backdrops, precise micro-geometry, and targeted emotional chroma. 

The aesthetic is **Dark Modern Glass & Metric Precision**. It avoids decorative clutter in favor of low-key structural discipline, restrained indigo-violet luminescence, and distinct categorical data cues. Interactions feel immediate, calm, and weighted with mathematical clarity.

## Colors

The palette relies on a deep triple-tier slate foundation overlaid with focused chromatic channels for emotion taxonomy and diagnostic feedback.

### Foundation & Luminescence
- **Base Canvas (`#0B0F19`):** Ground-level viewport void.
- **Surface Elevation 1 (`#111827`):** Primary panel and view containers.
- **Surface Elevation 2 (`#1E293B`):** Interactive inputs, nested cards, and table headers.
- **Subtle Borders (`rgba(255, 255, 255, 0.08)`):** Hairline segmentation across dark layers.
- **Accents:** Soft lavender (`#C4B5FD`) and violet (`#A78BFA`) drive active states, selection outlines, and primary system metrics. Secondary indigo (`#6366F1`) powers underlying radial ambient glows.

### Semantic Emotion Spectrum
The taxonomy strictly adheres to dedicated functional hues across confidence meters, token highlights, and breakdown charts:
- **Joy:** Warm Golden Amber (`#F59E0B`)
- **Sadness:** Serene Sky Blue (`#3B82F6`)
- **Anger:** Crimson Coral (`#EF4444`)
- **Love:** Rose Magenta (`#EC4899`)
- **Fear:** Deep Amethyst Purple (`#8B5CF6`)
- **Surprise:** Vibrant Emerald Teal (`#10B981`)

## Typography

Typography prioritizes high optical contrast, structural hierarchy, and legibility during analytical parsing.

- **Headlines:** Set in `Plus Jakarta Sans` with tight negative tracking, offering crisp structural authority for model telemetry, card groups, and metric callouts.
- **Body & Metrics:** Set in `Inter` with neutral metrics for sustained analytical reading, inline token sentiment inspection, and dense payload listings.
- **Labels & Badges:** Upper-micro labels (`label-sm`) feature elevated letter spacing for model versioning, pipeline states, and confidence value indicators.

## Layout & Spacing

The layout is built on a responsive 12-column fluid grid system paired with strict 8px horizontal and vertical spacing intervals.

### Grid Framework
- **Desktop (1200px+):** 12 columns, `gutter` of 1.5rem (`24px`), `margin` of 2rem (`32px`), max content width of 1440px centered.
- **Tablet (768px – 1199px):** 8 columns, `gutter` of 1.5rem (`24px`), `margin` of 1.5rem (`24px`).
- **Mobile (< 768px):** 4 columns, `gutter-mobile` of 1rem (`16px`), `margin-mobile` of 1rem (`16px`). Two-column analysis sidebars collapse below primary token inputs.

### Layout Philosophy
Components respect an internal structural rhythm: micro details (badge spacing, token padding) use `space-xs` and `space-sm`, while analytical card gutters and pipeline panels scale from `space-md` to `space-xl`.

## Elevation & Depth

Visual depth is achieved through layered dark tonal planes, restrained luminous backdrops, and precision hairline boundaries. Drop shadows are quiet and tinted.

### Surface Tiers
- **Tier 0 (Canvas):** Pure `#0B0F19` backdrop.
- **Tier 1 (Panels & Feed Cards):** `#111827` bound by a `1px` border of `rgba(255, 255, 255, 0.08)`.
- **Tier 2 (Interactive Floating Inputs & Modals):** `#1E293B` bound by `1px` border of `rgba(255, 255, 255, 0.12)`.

### Shadow & Glow Language
- **Restrained Ambient Shadow:** `0 8px 32px -4px rgba(0, 0, 0, 0.5)`.
- **Subtle Ambient Indigo Glow:** Used strictly behind primary active modules or focal metrics: `0 0 48px -12px rgba(99, 102, 241, 0.18)`.
- **Selected Element Outline:** Avoids excessive blur; applies a crisp `1px solid rgba(196, 181, 253, 0.4)` border with an optional inner ring of `rgba(167, 139, 250, 0.1)`.

## Shapes

The design system adopts **Rounded** geometry (`roundedness: 2`). Base corners sit at `0.5rem` (`8px`), outer analytic containers and cards at `1rem` (`16px`), and high-level overlays or modals at `1.5rem` (`24px`). 

Badges, emotion tags, and pipeline micro-chips use full-pill styling to juxtapose structural container grids.

## Components

### Buttons
- **Primary:** Background in `#A78BFA` with `#0B0F19` text, `font-weight: 600`, `border-radius: 0.5rem`, padding `0.625rem 1.25rem`. Hover state transitions to `#C4B5FD` with a soft box shadow `0 0 16px rgba(167, 139, 250, 0.35)`.
- **Secondary / Ghost:** Background `rgba(30, 41, 59, 0.6)`, border `1px solid rgba(255, 255, 255, 0.08)`, text `#F3F4F6`. Hover increases surface opacity to `rgba(30, 41, 59, 1)` and border to `rgba(255, 255, 255, 0.2)`.

### Emotion Confidence Bars
- **Track:** Height of `6px` or `8px`, background `rgba(255, 255, 255, 0.06)`, `border-radius: 9999px`.
- **Fill:** Direct mapping to emotion tokens (e.g., Joy `#F59E0B`, Sadness `#3B82F6`). Bar edges are rounded with a subtle trailing `0.5px` inner glow.

### NLP Pipeline Badges & Chips
- **Pipeline Badges:** Pill shape (`border-radius: 9999px`), padding `0.25rem 0.625rem`. Background `rgba(30, 41, 59, 0.8)`, border `1px solid rgba(255, 255, 255, 0.1)`. Typography set to `label-sm` in monospace-like tracking. Features a 6px status dot (e.g., `#10B981` for active inference).
- **Emotion Category Chips:** Tinted backgrounds using semantic color at `12%` opacity with matching colored text and `1px` border at `24%` opacity.

### Segmented Tabs
- **Container:** Background `#0B0F19`, `1px solid rgba(255, 255, 255, 0.06)`, padding `4px`, `border-radius: 0.625rem`.
- **Tab Item:** Text `#9CA3AF`, padding `0.375rem 0.875rem`, `border-radius: 0.375rem`. Active state utilizes `#1E293B` background, `#FFFFFF` text, and hairline top highlight.

### Text Analysis Input Fields
- **Container:** Background `#111827`, border `1px solid rgba(255, 255, 255, 0.08)`, `border-radius: 0.75rem`.
- **Focus State:** Border shifts to `#A78BFA`, accompanied by a `0 0 0 3px rgba(167, 139, 250, 0.15)` focus ring.
- **Inline Analyzed Tokens:** Highlighted text fragments wrapped in soft rounded tags with emotion-coded backgrounds at `15%` opacity and an underline border matching the emotion index.

### Cards & Panels
- **Structure:** Surface `#111827`, border `1px solid rgba(255, 255, 255, 0.08)`, `border-radius: 1rem`, padding `1.5rem`.
- **Header:** Distinct split layout with `headline-sm` title paired with token count, model inference latency badges, or probability density summaries.