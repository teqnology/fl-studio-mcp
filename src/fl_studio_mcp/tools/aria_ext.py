"""AR/IA extension tools: mixer routing, patterns, playlist tracks, markers, audits.

Requires the matching `handle_ext` block in fl_controller/device_FLStudioMCP.py
(branch aria-ext). Re-copy the controller script into FL Studio's
Settings/Hardware/FLStudioMCP folder after updating it.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fastmcp import FastMCP


def _hex_to_rgb(color: str) -> dict:
    c = color.lstrip("#")
    return {"r": int(c[0:2], 16), "g": int(c[2:4], 16), "b": int(c[4:6], 16)}


def register_aria_ext_tools(mcp: FastMCP) -> None:
    from fl_studio_mcp.utils.connection import get_connection

    def _send(action: str, params: dict | None = None) -> dict:
        return get_connection().send_command(action, params or {})

    @mcp.tool()
    def fl_mixer_audit() -> dict:
        """Full mixer audit: every named / plugin-loaded insert with colour, routes and plugins per slot."""
        return _send("ext.mixerAudit")

    @mcp.tool()
    def fl_channel_audit() -> dict:
        """Full channel rack audit: name, colour, target mixer insert, type, generator plugin, mute."""
        return _send("ext.channelAudit")

    @mcp.tool()
    def fl_get_mixer_routes(track: int) -> dict:
        """List the mixer inserts that `track` currently sends to (0 = Master)."""
        return _send("ext.getRoutes", {"track": track})

    @mcp.tool()
    def fl_set_mixer_route(src: int, dest: int, enabled: bool = True, exclusive: bool = False) -> dict:
        """Create or remove an insert-to-insert route (e.g. drums -> drum bus).

        Args:
            src: source mixer insert
            dest: destination insert (0 = Master)
            enabled: True to create the send, False to remove it
            exclusive: True removes every other send from `src` (incl. Master) so it only feeds `dest`
        """
        return _send("ext.setRoute", {"src": src, "dest": dest, "enabled": enabled, "exclusive": exclusive})

    @mcp.tool()
    def fl_get_patterns() -> dict:
        """List all patterns (1-based index) with name, colour and length in beats."""
        return _send("ext.getPatterns")

    @mcp.tool()
    def fl_set_pattern_name(index: int, name: str) -> dict:
        """Rename pattern `index` (1-based)."""
        return _send("ext.setPatternName", {"index": index, "name": name})

    @mcp.tool()
    def fl_set_pattern_color(index: int, color: str) -> dict:
        """Set pattern colour. color = '#RRGGBB'."""
        return _send("ext.setPatternColor", {"index": index, **_hex_to_rgb(color)})

    @mcp.tool()
    def fl_select_pattern(index: int) -> dict:
        """Make pattern `index` (1-based) the current pattern (piano-roll / step tools write into it)."""
        return _send("ext.selectPattern", {"index": index})

    @mcp.tool()
    def fl_get_playlist_tracks(include_empty: bool = False) -> dict:
        """List playlist tracks (renamed ones only unless include_empty)."""
        return _send("ext.getPlaylistTracks", {"include_empty": include_empty})

    @mcp.tool()
    def fl_set_playlist_track_name(index: int, name: str) -> dict:
        """Rename playlist track `index`."""
        return _send("ext.setPlaylistTrackName", {"index": index, "name": name})

    @mcp.tool()
    def fl_set_playlist_track_color(index: int, color: str) -> dict:
        """Set playlist track colour. color = '#RRGGBB'."""
        return _send("ext.setPlaylistTrackColor", {"index": index, **_hex_to_rgb(color)})

    @mcp.tool()
    def fl_add_time_marker(bar: int, name: str) -> dict:
        """Add a playlist time marker at the start of `bar` (1-based, 4/4)."""
        return _send("ext.addTimeMarker", {"bar": bar, "name": name})
