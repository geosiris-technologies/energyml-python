from src.energyml.utils.constants import content_type_to_qualified_type, qualified_type_to_content_type, sanitize_file_name


def test_content_type_to_qualified_type():
    assert (
        content_type_to_qualified_type("application/x-resqml+xml;version=2.0;type=obj_FaultInterpretation")
        == "resqml20.obj_FaultInterpretation"
    )


def test_qualified_type_to_content_type():
    assert (
        qualified_type_to_content_type("resqml20.obj_FaultInterpretation")
        == "application/x-resqml+xml;version=2.0;type=obj_FaultInterpretation"
    )


# ---------------------------------------------------------------------------
# sanitize_file_name
# ---------------------------------------------------------------------------


def test_sanitize_file_name_replaces_the_colon():
    """The bug this exists for.

    A citation title such as "AUB-PRO-SP05512: Trajectory" goes into the export file name. On
    Windows ``open("well: Traj.geojson", "w")`` does not fail: ``:`` opens an NTFS alternate
    data stream, so the content lands in a hidden stream and an empty, extension-less file
    called ``well`` is left on disk.
    """
    assert ":" not in sanitize_file_name("AUB-PRO-SP05512: Trajectory")
    assert sanitize_file_name("AUB-PRO-SP05512: Trajectory") == "AUB-PRO-SP05512_ Trajectory"


def test_sanitize_file_name_replaces_every_forbidden_char():
    for char in r'<>:"/\|?*':
        assert char not in sanitize_file_name(f"a{char}b"), char
    assert sanitize_file_name("a\x00b\x1fc") == "a_b_c"


def test_sanitize_file_name_collapses_replacement_runs():
    # "a: b" -> one for the colon, one for the space: a single separator is enough.
    assert sanitize_file_name("a:/b") == "a_b"


def test_sanitize_file_name_strips_trailing_dots_and_spaces():
    # Windows drops them silently, so "x." and "x" would collide.
    assert sanitize_file_name("name.  ") == "name"
    assert sanitize_file_name("  name  ") == "name"


def test_sanitize_file_name_escapes_reserved_device_names():
    assert sanitize_file_name("CON") != "CON"
    assert sanitize_file_name("con.geojson").startswith("con_")
    assert sanitize_file_name("COM1") != "COM1"
    # A name that merely starts with a reserved word is fine.
    assert sanitize_file_name("CONTOUR") == "CONTOUR"


def test_sanitize_file_name_truncates():
    assert len(sanitize_file_name("x" * 400)) == 150
    assert len(sanitize_file_name("x" * 400, max_length=20)) == 20


def test_sanitize_file_name_never_returns_empty():
    assert sanitize_file_name("") == "unnamed"
    assert sanitize_file_name("///") == "unnamed"
    assert sanitize_file_name("...") == "unnamed"


def test_sanitize_file_name_keeps_a_normal_title_untouched():
    assert sanitize_file_name("Bartonien Bottom") == "Bartonien Bottom"
    assert sanitize_file_name("Generated Triangulation 2") == "Generated Triangulation 2"
