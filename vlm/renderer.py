"""Render Plotly JSON to base64 PNG."""

import base64
import json
from typing import Union


def render_plot_to_base64(
    plotly_json: Union[str, dict],
    width: int = 640,
    height: int = 480,
    scale: float = 1.0,
) -> str:
    """Convert Plotly JSON to base64-encoded PNG.

    Args:
        plotly_json: Plotly figure as JSON string or dict
        width: Image width in pixels
        height: Image height in pixels
        scale: Resolution multiplier (1.0 = native resolution)

    Returns:
        Base64-encoded PNG string

    Raises:
        RuntimeError: If kaleido or plotly not installed
        ValueError: If invalid Plotly JSON
    """
    try:
        import plotly.io as pio
    except ImportError as e:
        raise RuntimeError(
            "plotly is required for rendering. Install with: pip install plotly"
        ) from e

    # Parse JSON if string
    if isinstance(plotly_json, str):
        try:
            plotly_json = json.loads(plotly_json)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON string: {e}") from e

    if not isinstance(plotly_json, dict):
        raise ValueError(
            f"Expected dict or JSON string, got {type(plotly_json).__name__}"
        )

    # Create figure from JSON
    try:
        fig = pio.from_json(json.dumps(plotly_json))
    except Exception as e:
        raise ValueError(f"Invalid Plotly JSON structure: {e}") from e

    # Export to PNG bytes using kaleido
    try:
        img_bytes = fig.to_image(
            format="png",
            width=width,
            height=height,
            scale=scale,
        )
    except ValueError as e:
        if "kaleido" in str(e).lower():
            raise RuntimeError(
                "kaleido is required for plot rendering. Install with: pip install kaleido"
            ) from e
        raise

    return base64.b64encode(img_bytes).decode("utf-8")
