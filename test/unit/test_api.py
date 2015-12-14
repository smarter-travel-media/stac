# -*- coding: utf-8 -*-


def test_api_exports_match_all():
    """Make sure publicly exposed classes / functions / etc. match what we export."""
    import stac.api
    members = set([item for item in dir(stac.api) if not item.startswith("_")])
    exported = set(stac.api.__all__)
    assert members == exported
