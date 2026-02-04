"""Tests for ContentSection dataclass."""

from extractors.base import ContentSection


def test_anchor_id_uses_explicit_anchor():
    section = ContentSection(id="some-id", title="Title", html_content="", anchor="custom-anchor")
    assert section.anchor_id == "custom-anchor"


def test_anchor_id_generated_from_id():
    section = ContentSection(id="meta/principles", title="Principles", html_content="")
    assert section.anchor_id == "meta-principles"


def test_anchor_id_replaces_dots():
    section = ContentSection(id="file.name", title="T", html_content="")
    assert section.anchor_id == "file-name"


def test_anchor_id_lowercased():
    section = ContentSection(id="Blog/Post", title="T", html_content="")
    assert section.anchor_id == "blog-post"


def test_default_level_is_1():
    section = ContentSection(id="x", title="T", html_content="")
    assert section.level == 1


def test_children_default_empty():
    section = ContentSection(id="x", title="T", html_content="")
    assert section.children == []
