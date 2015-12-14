# -*- coding: utf-8 -*-


def test_api_exports_match_all():
    """Make sure publicly exposed classes / functions / etc. match what we export."""
    import artificium.api
    members = set([item for item in dir(artificium.api) if not item.startswith("_")])
    exported = set(artificium.api.__all__)
    assert members == exported
