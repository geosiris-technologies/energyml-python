from src.energyml.utils.constants import content_type_to_qualified_type, qualified_type_to_content_type


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
