import os
import streamlit.components.v1 as components

_RELEASE = True

if not _RELEASE:
    _weighing_scale = components.declare_component(
        "weighing_scale",
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    # Assuming index.html is in this directory
    _weighing_scale = components.declare_component(
        "weighing_scale", path=parent_dir
    )

def weighing_scale(key=None):
    """
    Shows an interactive weighing scale and returns the final mass.
    """
    component_value = _weighing_scale(key=key, default=None)
    return component_value
