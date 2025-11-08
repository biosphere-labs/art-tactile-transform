"""GUI application for art-tactile-transform (placeholder for future implementation)."""

import sys

try:
    import gradio as gr
except ImportError:
    gr = None


def main() -> None:
    """GUI entry point.

    This is a placeholder for the future Gradio-based GUI application.
    The full implementation will be added in Phase 1 of the PRD.
    """
    if gr is None:
        print("Error: Gradio is not installed.", file=sys.stderr)
        print("Install GUI dependencies with: pip install art-tactile-transform[gui]")
        sys.exit(1)

    print("GUI interface coming soon!")
    print("This will provide:")
    print("  - Interactive parameter adjustment")
    print("  - Real-time 3D preview")
    print("  - Multiple processing modes (Portrait, Landscape, Text, Diagram)")
    print("  - Preset management")
    print("")
    print("For now, please use the CLI interface: art-tactile-cli")
    print("See the PRD at docs/prd/tactile-art-gui-v2.md for planned features")


if __name__ == "__main__":
    main()
