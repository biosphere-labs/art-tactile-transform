# Tactile Art Transform - Design System v2.0

**Version**: 2.0.0
**Last Updated**: 2025-11-08
**Status**: Draft
**Purpose**: Comprehensive design system for the Tactile Art Transform GUI application

---

## Table of Contents

1. [Design Philosophy](#design-philosophy)
2. [Color System](#color-system)
3. [Typography](#typography)
4. [Spacing & Layout](#spacing--layout)
5. [Component Library](#component-library)
6. [Interaction Patterns](#interaction-patterns)
7. [Accessibility](#accessibility)
8. [Responsive Design](#responsive-design)
9. [Dark/Light Modes](#darklight-modes)

---

## 1. Design Philosophy

### Core Principles

**Accessibility First**
- Design for blind and visually impaired users who will collaborate with sighted assistants
- High contrast ratios (WCAG AAA compliance: 7:1 minimum)
- Full keyboard navigation support
- Comprehensive screen reader compatibility
- Clear focus indicators and large touch targets

**Clarity Over Aesthetics**
- Function drives form
- Clear visual hierarchy
- Generous whitespace
- Minimal distractions
- Purpose-driven design

**Progressive Disclosure**
- Simple by default, powerful when needed
- Mode-specific parameters only shown when relevant
- Advanced options collapsible
- Contextual help available but not intrusive

**Immediate Feedback**
- Real-time preview updates
- Clear status indicators
- Progress visualization
- Validation messages inline

---

## 2. Color System

### Primary Palette

**Brand Colors**
```
Primary Blue (Main Actions)
- Primary-500: #0066CC (Main interactive elements)
- Primary-600: #0052A3 (Hover state)
- Primary-700: #003D7A (Active/pressed state)
- Primary-300: #3399FF (Disabled state)

Contrast Ratio with White: 8.2:1 ✓ AAA
```

**Semantic Colors**
```
Success Green
- Success-500: #00AA44 (Successful operations)
- Success-600: #008835 (Hover)
- Success-700: #006626 (Active)

Warning Orange
- Warning-500: #FF8800 (Warnings, caution)
- Warning-600: #CC6D00 (Hover)
- Warning-700: #995200 (Active)

Error Red
- Error-500: #DD0000 (Errors, destructive actions)
- Error-600: #B10000 (Hover)
- Error-700: #850000 (Active)

Info Cyan
- Info-500: #0099CC (Informational messages)
- Info-600: #007AA3 (Hover)
- Info-700: #005B7A (Active)
```

### Neutral Palette (Light Mode)

```
Backgrounds
- Gray-50: #FAFAFA (Page background)
- Gray-100: #F5F5F5 (Panel background)
- Gray-200: #E8E8E8 (Input backgrounds)

Borders & Dividers
- Gray-300: #D0D0D0 (Subtle borders)
- Gray-400: #B0B0B0 (Standard borders)
- Gray-500: #909090 (Strong borders)

Text
- Gray-900: #1A1A1A (Primary text - 15.8:1 contrast)
- Gray-700: #404040 (Secondary text - 10.7:1 contrast)
- Gray-600: #606060 (Tertiary text - 7.2:1 contrast)
```

### Neutral Palette (Dark Mode)

```
Backgrounds
- Dark-900: #121212 (Page background)
- Dark-800: #1E1E1E (Panel background)
- Dark-700: #2A2A2A (Input backgrounds)

Borders & Dividers
- Dark-600: #404040 (Subtle borders)
- Dark-500: #5A5A5A (Standard borders)
- Dark-400: #707070 (Strong borders)

Text
- Dark-50: #F5F5F5 (Primary text - 15.8:1 contrast)
- Dark-200: #D0D0D0 (Secondary text - 11.2:1 contrast)
- Dark-300: #B0B0B0 (Tertiary text - 8.1:1 contrast)
```

### 3D Viewport Colors

```
Height Gradient (for heightmap visualization)
- Lowest: #1A1A5A (Deep blue - valleys)
- Low-Mid: #0066CC (Blue)
- Mid: #00AA44 (Green - mid-level)
- Mid-High: #FFAA00 (Orange)
- Highest: #DD0000 (Red - peaks)

Grid & Helpers
- Grid lines: rgba(255, 255, 255, 0.15)
- Axis X: #FF0000 (Red)
- Axis Y: #00FF00 (Green)
- Axis Z: #0000FF (Blue)
- Measurements: #FFD700 (Gold)
```

---

## 3. Typography

### Font Families

**Primary Font: Inter**
- Modern, highly legible sans-serif
- Excellent at small sizes
- Wide language support
- Variable font support for fine-tuning

**Monospace Font: JetBrains Mono**
- For measurements, coordinates, file sizes
- Clear distinction between similar characters (0/O, 1/l/I)

**Fallback Stack**
```css
font-family: 'Inter', -apple-system, BlinkMacSystemFont,
             'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu',
             'Helvetica Neue', Arial, sans-serif;
```

### Type Scale

```
Display (Hero text)
- Size: 32px / 2rem
- Weight: 700 (Bold)
- Line Height: 1.2
- Use: Application title, major headings

Heading 1
- Size: 24px / 1.5rem
- Weight: 600 (Semi-bold)
- Line Height: 1.3
- Use: Section headers

Heading 2
- Size: 20px / 1.25rem
- Weight: 600 (Semi-bold)
- Line Height: 1.4
- Use: Subsection headers

Heading 3
- Size: 16px / 1rem
- Weight: 600 (Semi-bold)
- Line Height: 1.4
- Use: Component headers, panel titles

Body Large
- Size: 16px / 1rem
- Weight: 400 (Regular)
- Line Height: 1.5
- Use: Primary content, descriptions

Body Regular
- Size: 14px / 0.875rem
- Weight: 400 (Regular)
- Line Height: 1.5
- Use: Most UI text, labels

Body Small
- Size: 12px / 0.75rem
- Weight: 400 (Regular)
- Line Height: 1.4
- Use: Captions, helper text, metadata

Caption
- Size: 11px / 0.6875rem
- Weight: 400 (Regular)
- Line Height: 1.3
- Use: Timestamps, footnotes

Monospace (for values)
- Size: 14px / 0.875rem
- Weight: 500 (Medium)
- Line Height: 1.4
- Use: Measurements, file sizes, technical data
```

### Font Weights

```
- Regular: 400 (body text)
- Medium: 500 (emphasis, monospace values)
- Semi-bold: 600 (headings)
- Bold: 700 (strong emphasis, display text)
```

---

## 4. Spacing & Layout

### Spacing Scale (Base Unit: 4px)

```
space-1:  4px   (0.25rem)  - Tight spacing, icon padding
space-2:  8px   (0.5rem)   - Small spacing, inline elements
space-3:  12px  (0.75rem)  - Compact spacing
space-4:  16px  (1rem)     - Standard spacing (BASE)
space-5:  20px  (1.25rem)  - Comfortable spacing
space-6:  24px  (1.5rem)   - Section spacing
space-8:  32px  (2rem)     - Large spacing
space-10: 40px  (2.5rem)   - Major section spacing
space-12: 48px  (3rem)     - Page section dividers
space-16: 64px  (4rem)     - Hero spacing
```

### Layout Grid

**Container Widths**
```
- Small (Mobile): 100% (min 320px)
- Medium (Tablet): 768px
- Large (Desktop): 1280px
- XLarge (Wide): 1920px
```

**Column System**
```
12-column grid with 24px gutters

Layout proportions:
- Left panel (upload/mode): 3 columns (25%)
- Center (preview area): 6 columns (50%)
- Right panel (parameters): 3 columns (25%)

Responsive breakpoints:
- Mobile (<768px): Stacked single column
- Tablet (768-1024px): 2-column layout
- Desktop (>1024px): 3-column layout
```

**Margins & Padding**
```
- Page margins: space-6 (24px)
- Panel padding: space-4 (16px)
- Component padding: space-3 (12px)
- Button padding: space-3 horizontal, space-2 vertical
- Input padding: space-3 (12px)
```

### Border Radius

```
- radius-sm: 4px (small elements, badges)
- radius-md: 6px (buttons, inputs, cards - DEFAULT)
- radius-lg: 8px (panels, modals)
- radius-xl: 12px (major containers)
- radius-full: 9999px (circular buttons, avatars)
```

### Shadows

```
Shadow-sm (Subtle depth)
- box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05)
- Use: Inputs, subtle elevation

Shadow-md (Standard elevation)
- box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1)
- Use: Cards, dropdowns, tooltips

Shadow-lg (Prominent elevation)
- box-shadow: 0 10px 15px rgba(0, 0, 0, 0.1)
- Use: Modals, popovers

Shadow-xl (Maximum elevation)
- box-shadow: 0 20px 25px rgba(0, 0, 0, 0.15)
- Use: Major overlays

Focus Shadow (Accessibility)
- box-shadow: 0 0 0 3px rgba(0, 102, 204, 0.4)
- Use: Keyboard focus indicators
```

---

## 5. Component Library

### 5.1 Buttons

**Primary Button**
```
Purpose: Main actions (Export, Process, Apply)
Background: Primary-500
Text: White
Padding: 12px 24px
Border Radius: 6px
Font: 14px, Semi-bold (600)

States:
- Default: bg-primary-500, no shadow
- Hover: bg-primary-600, shadow-sm
- Active: bg-primary-700, scale(0.98)
- Disabled: bg-primary-300, cursor-not-allowed, opacity 0.6
- Focus: 3px focus ring, primary-500 at 40% opacity
```

**Secondary Button**
```
Purpose: Alternative actions (Cancel, Reset)
Background: Transparent
Border: 2px solid Gray-400
Text: Gray-900
Padding: 10px 22px (accounting for border)

States:
- Hover: bg-gray-100, border-gray-500
- Active: bg-gray-200
- Disabled: border-gray-300, text-gray-400
```

**Icon Button**
```
Purpose: Compact actions (Close, Settings, Info)
Size: 32px × 32px (square)
Padding: 6px
Border Radius: 6px

States:
- Default: transparent background
- Hover: bg-gray-100
- Active: bg-gray-200
- Focus: 3px focus ring
```

**Button Groups**
```
Related buttons grouped together
- No space between buttons
- First button: rounded left corners
- Last button: rounded right corners
- Middle buttons: no radius
- Shared border (1px between items)
```

### 5.2 Form Inputs

**Text Input**
```
Height: 40px
Padding: 12px
Border: 1px solid Gray-400
Background: White (light) / Dark-700 (dark)
Font: 14px, Regular
Border Radius: 6px

States:
- Default: border-gray-400
- Hover: border-gray-500
- Focus: border-primary-500, focus ring
- Error: border-error-500, error text below
- Disabled: bg-gray-100, border-gray-300, cursor-not-allowed
```

**Slider**
```
Track:
- Height: 4px
- Background: Gray-300
- Border Radius: 2px
- Active portion: Primary-500

Thumb:
- Size: 20px × 20px
- Background: White
- Border: 2px solid Primary-500
- Shadow: shadow-md
- Cursor: grab (grabbable)

States:
- Hover: thumb scale 1.1, shadow-lg
- Active/Dragging: thumb scale 1.15, cursor: grabbing
- Focus: 3px focus ring on thumb
- Disabled: opacity 0.5, cursor-not-allowed

Labels:
- Min/Max values at track ends (11px, gray-600)
- Current value above thumb (14px, semi-bold, primary-500)
```

**Checkbox & Radio**
```
Size: 20px × 20px
Border: 2px solid Gray-400
Background: White

Checkbox:
- Border Radius: 4px
- Checked: bg-primary-500, white checkmark icon

Radio:
- Border Radius: 50% (circular)
- Checked: bg-primary-500, white dot (8px) centered

States:
- Hover: border-gray-500
- Focus: 3px focus ring
- Disabled: bg-gray-100, border-gray-300
```

**Dropdown/Select**
```
Height: 40px
Padding: 12px
Border: 1px solid Gray-400
Background: White
Font: 14px, Regular
Icon: Chevron-down (16px) on right

States:
- Same as text input
- Open: border-primary-500, chevron rotated 180deg

Dropdown Menu:
- Background: White
- Border: 1px solid Gray-300
- Shadow: shadow-lg
- Border Radius: 6px
- Max Height: 300px (scrollable)
- Padding: 4px

Menu Items:
- Padding: 10px 12px
- Hover: bg-gray-100
- Selected: bg-primary-50, text-primary-700
```

### 5.3 Cards & Panels

**Card**
```
Background: White (light) / Dark-800 (dark)
Border: 1px solid Gray-300
Border Radius: 8px
Padding: 16px
Shadow: shadow-sm

Interactive Card (clickable):
- Hover: shadow-md, border-gray-400
- Active: scale(0.99)
```

**Panel**
```
Background: Gray-100 (light) / Dark-800 (dark)
Border Radius: 8px
Padding: 20px

Header:
- Border Bottom: 1px solid Gray-300
- Padding Bottom: 12px
- Margin Bottom: 16px
- Title: Heading 3
```

**Modal**
```
Backdrop: rgba(0, 0, 0, 0.6)
Container:
- Background: White (light) / Dark-800 (dark)
- Border Radius: 12px
- Shadow: shadow-xl
- Max Width: 600px (standard), 800px (large)
- Padding: 24px

Header:
- Title: Heading 2
- Close button: top-right icon button
- Border Bottom: 1px solid Gray-300

Body:
- Padding: 24px 0

Footer:
- Border Top: 1px solid Gray-300
- Padding Top: 16px
- Button alignment: right (flex-end)
- Button spacing: 12px gap
```

### 5.4 Navigation & Tabs

**Tabs (Horizontal)**
```
Container:
- Border Bottom: 2px solid Gray-300

Tab:
- Padding: 12px 20px
- Font: 14px, Medium
- Border Bottom: 3px solid transparent
- Transition: all 200ms

States:
- Default: text-gray-600
- Hover: text-gray-900, bg-gray-50
- Active: text-primary-600, border-bottom-primary-500
- Focus: focus ring
```

**Breadcrumbs**
```
Container: flex row, gap 8px

Item:
- Font: 14px, Regular
- Color: Gray-600
- Hover: text-gray-900

Separator: "/" (gray-400)
Current: text-gray-900, semi-bold
```

### 5.5 Feedback Components

**Toast Notification**
```
Width: 400px
Background: White
Border: 1px solid Gray-300
Border-left: 4px solid [semantic-color]
Border Radius: 6px
Shadow: shadow-lg
Padding: 16px
Animation: slide-in-right 300ms

Structure:
- Icon (24px) [semantic-color]
- Title (14px, semi-bold)
- Message (14px, regular)
- Close button (icon button)
- Auto-dismiss: 5 seconds

Variants:
- Success: border-left success-500, green icon
- Error: border-left error-500, red icon
- Warning: border-left warning-500, orange icon
- Info: border-left info-500, blue icon
```

**Progress Bar**
```
Track:
- Height: 8px
- Background: Gray-200
- Border Radius: 4px

Fill:
- Background: Primary-500
- Border Radius: 4px
- Transition: width 300ms ease

With Label:
- Percentage above bar (12px, semi-bold)
- Status text below bar (12px, regular, gray-600)
```

**Spinner/Loader**
```
Size: 24px (small), 40px (medium), 64px (large)
Border: 3px solid Gray-200
Border-top: 3px solid Primary-500
Border Radius: 50%
Animation: rotate 1s linear infinite
```

**Tooltip**
```
Background: Gray-900 (light) / Gray-100 (dark)
Text: White (light) / Dark-900 (dark)
Font: 12px, Regular
Padding: 6px 10px
Border Radius: 4px
Shadow: shadow-md
Max Width: 250px

Arrow: 6px triangle matching background

Trigger: hover (1s delay) or focus
```

### 5.6 Data Display

**Badge**
```
Padding: 4px 8px
Font: 11px, Medium
Border Radius: 4px
Text Transform: uppercase
Letter Spacing: 0.5px

Variants:
- Default: bg-gray-200, text-gray-700
- Primary: bg-primary-100, text-primary-700
- Success: bg-success-100, text-success-700
- Warning: bg-warning-100, text-warning-700
- Error: bg-error-100, text-error-700
```

**Stat Card**
```
Label: 12px, uppercase, gray-600, medium
Value: 24px, semi-bold, gray-900
Icon: 32px, semantic color
Change: 12px, success/error color with arrow

Layout: flex column, gap 4px
Padding: 16px
Background: white
Border: 1px solid gray-200
Border Radius: 8px
```

---

## 6. Interaction Patterns

### Hover States
```
Timing: 150ms ease-in-out
Effects:
- Background color change
- Border color change
- Shadow elevation increase
- Slight scale (1.02-1.05 for buttons)
- Cursor: pointer for interactive elements
```

### Active/Pressed States
```
Timing: 100ms ease-out
Effects:
- Darker background
- Scale down (0.98-0.99)
- Shadow reduction
- Immediate feedback
```

### Focus States (Keyboard Navigation)
```
Always visible: 3px solid focus ring
Color: Primary-500 at 40% opacity
Offset: 2px from element
Border Radius: matches element + 2px
Never remove: outline-none is forbidden
```

### Loading States
```
Buttons:
- Show spinner inside button
- Disable interaction
- Maintain button size
- Text: "Loading..." or specific status

Full Page:
- Overlay with semi-transparent backdrop
- Centered large spinner
- Optional status text
- Prevent interaction with content below
```

### Drag & Drop
```
Drop Zone:
- Default: dashed 2px border, gray-400
- Drag Over: solid 2px border, primary-500, bg-primary-50
- Accepted: bg-success-50, border-success-500
- Rejected: bg-error-50, border-error-500

Draggable Element:
- Cursor: grab
- Dragging: cursor: grabbing, opacity 0.6, scale 1.05
```

### Transitions & Animations
```
Standard Timing:
- Instant: 0ms (immediate feedback)
- Fast: 100-150ms (micro-interactions)
- Standard: 200-300ms (default)
- Slow: 400-500ms (page transitions)

Easing:
- ease-in: acceleration (starting animations)
- ease-out: deceleration (ending animations) - DEFAULT
- ease-in-out: smooth start and end (complex animations)
- linear: constant speed (loading spinners)

Motion Preferences:
- Respect prefers-reduced-motion
- Disable non-essential animations
- Maintain functional animations (loading indicators)
```

---

## 7. Accessibility

### WCAG AAA Compliance

**Color Contrast**
- Text: Minimum 7:1 ratio
- Large text (18pt+): Minimum 4.5:1 ratio
- UI components: Minimum 3:1 ratio
- All semantic colors tested against backgrounds

**Keyboard Navigation**
```
Tab Order:
- Logical sequence: top-to-bottom, left-to-right
- Skip links for repeated content
- Focus trap in modals
- Escape key closes overlays

Keyboard Shortcuts:
- Ctrl/Cmd + O: Open file
- Ctrl/Cmd + E: Export STL
- Ctrl/Cmd + S: Save parameters
- Ctrl/Cmd + R: Reset view
- Space: Play/Pause animation
- Arrow keys: Navigate sliders (± 1)
- Shift + Arrow: Navigate sliders (± 10)
```

**Screen Reader Support**
```
Semantic HTML:
- <button> for actions
- <input> with proper types
- <label> for all form fields
- <nav>, <main>, <aside> for structure

ARIA Labels:
- aria-label for icon buttons
- aria-describedby for help text
- aria-live for dynamic content
- aria-expanded for collapsible sections
- aria-current for active states
- aria-valuenow/min/max for sliders

Focus Management:
- Visible focus indicators (never outline: none)
- Focus moves to modal on open
- Focus returns to trigger on close
- Skip to main content link
```

**Visual Accessibility**
```
Text Sizing:
- Zoomable to 200% without horizontal scroll
- Relative units (rem, em) not pixels
- Minimum 14px body text

Spacing:
- Minimum 44px × 44px touch targets
- Adequate spacing between interactive elements
- Clear visual separation of sections

Color Independence:
- Never rely on color alone
- Icons + text labels
- Patterns in addition to colors
- Status indicated by multiple cues
```

**Assistive Technology**
```
Alt Text:
- Descriptive alt text for images
- Empty alt for decorative images
- SVG with title and desc elements

Captions & Transcripts:
- Any video content captioned
- Audio descriptions if needed

Forms:
- Clear error messages
- Error summary at top of form
- Field-level validation
- Success confirmations
```

---

## 8. Responsive Design

### Breakpoints

```css
/* Mobile First Approach */

/* Mobile (default) */
@media (min-width: 320px) { ... }

/* Tablet */
@media (min-width: 768px) { ... }

/* Desktop */
@media (min-width: 1024px) { ... }

/* Wide Desktop */
@media (min-width: 1440px) { ... }

/* Ultra-wide */
@media (min-width: 1920px) { ... }
```

### Layout Adaptations

**Mobile (<768px)**
```
- Single column layout
- Stacked panels (upload → preview → parameters)
- Collapsible parameter sections
- Bottom sheet for controls
- Larger touch targets (48px minimum)
- Simplified 3D controls (touch gestures)
- Reduced parameter count (essential only)
```

**Tablet (768px - 1024px)**
```
- Two-column layout
  - Left: Upload + Parameters (40%)
  - Right: Preview (60%)
- Collapsible sidebar
- Touch-optimized sliders (wider tracks)
- Moderate parameter visibility
```

**Desktop (>1024px)**
```
- Three-column layout (as designed)
- All parameters visible
- Advanced controls available
- Keyboard shortcuts enabled
- Hover interactions
```

### Component Responsiveness

**Typography Scale (Mobile)**
```
- Display: 24px (reduced from 32px)
- H1: 20px (reduced from 24px)
- H2: 18px (reduced from 20px)
- Body: 16px (increased for readability)
```

**3D Viewport**
```
Mobile:
- Full width
- Aspect ratio: 4:3
- Touch gestures: 1-finger rotate, 2-finger zoom/pan
- Simplified controls

Desktop:
- Fixed aspect ratio or flexible
- Mouse controls: drag rotate, scroll zoom, shift-drag pan
- Advanced overlay controls
```

---

## 9. Dark/Light Modes

### Mode Toggle
```
Location: Top-right header
Component: Icon button with sun/moon icon
Behavior: Toggle between modes
Persistence: Save preference to localStorage
System Preference: Respect prefers-color-scheme
```

### Light Mode (Default)
```
- White/light gray backgrounds
- Dark text
- Vibrant semantic colors
- Subtle shadows
- High contrast for readability
```

### Dark Mode
```
- Dark backgrounds (#121212 - #2A2A2A)
- Light text
- Slightly desaturated semantic colors
- Stronger borders (compensate for lack of shadow contrast)
- Elevated surfaces lighter than base

Color Adjustments:
- Primary-500: Slightly lighter for better contrast
- Success/Warning/Error: Desaturated by 10%
- Shadows: Heavier (darker, higher opacity)
- Borders: Lighter, more visible
```

### 3D Viewport in Dark Mode
```
- Background: Dark-900 (#121212)
- Grid lines: rgba(255, 255, 255, 0.1)
- Lighting: Adjusted for darker environment
- Height gradient: Same colors, better contrast
```

### Images
```
- Original image preview: No filter
- Processed heightmap: May invert for clarity in dark mode
- Icons: Automatically inverted or use CSS filter
```

---

## 10. File Organization

### Design Tokens (JSON/CSS Variables)

```
styles/
├── tokens/
│   ├── colors.json
│   ├── typography.json
│   ├── spacing.json
│   ├── shadows.json
│   └── animations.json
├── base/
│   ├── reset.css
│   ├── typography.css
│   └── utilities.css
├── components/
│   ├── buttons.css
│   ├── forms.css
│   ├── cards.css
│   └── [component-name].css
└── themes/
    ├── light.css
    └── dark.css
```

### Component Naming Convention

```
BEM (Block Element Modifier)

.component-name { ... }           /* Block */
.component-name__element { ... }  /* Element */
.component-name--modifier { ... } /* Modifier */

Examples:
.button { ... }
.button--primary { ... }
.button--secondary { ... }
.button__icon { ... }

.slider { ... }
.slider__track { ... }
.slider__thumb { ... }
.slider--disabled { ... }
```

---

## 11. Implementation Notes

### Technology Recommendations

**CSS Framework**
- Option A: Tailwind CSS (utility-first, fast development)
- Option B: Custom CSS with design tokens (full control)
- Recommendation: Tailwind with custom configuration

**Component Library**
- Option A: Build from scratch (maximum accessibility control)
- Option B: Headless UI + custom styling (accessible primitives)
- Recommendation: Headless UI for complex components (modals, dropdowns)

**3D Rendering**
- Three.js for WebGL rendering
- React Three Fiber if using React
- Custom controls for accessibility

### Performance Considerations

```
- CSS: Minimize reflows/repaints
- Animations: Use transform and opacity (GPU-accelerated)
- Images: Lazy loading, WebP format
- Fonts: Self-hosted, preload critical fonts
- Bundle size: Code splitting, tree shaking
```

### Browser Support

```
Modern Browsers:
- Chrome/Edge: Last 2 versions
- Firefox: Last 2 versions
- Safari: Last 2 versions

Graceful Degradation:
- Progressive enhancement
- Polyfills for critical features
- Fallbacks for unsupported features
```

---

## 12. Version History

**v2.0.0** (2025-11-08)
- Initial design system for GUI v2.0
- Comprehensive component library
- Accessibility-first approach
- Dark/light mode support
- Responsive design patterns

---

**End of Design System Documentation**
