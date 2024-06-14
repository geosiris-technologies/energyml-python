# Copyright (c) 2023-2024 Geosiris.
# SPDX-License-Identifier: Apache-2.0

from src.energyml.utils.uri import Uri, parse_uri


def test_uri_constructor():
    assert (
        str(
            Uri(
                dataspace="/folder-name/project-name",
                domain="resqml",
                domain_version="20",
                object_type="obj_HorizonInterpretation",
                uuid="421a7a05-033a-450d-bcef-051352023578",
                version="2.0",
                collection_domain=None,
                collection_domain_version=None,
                collection_domain_type=None,
                query="query",
            )
        )
        == "eml:///dataspace('/folder-name/project-name')/resqml20.obj_HorizonInterpretation(uuid=421a7a05-033a-450d-bcef-051352023578,version='2.0')?query"
    )


def test_uri_error():
    assert parse_uri("eml//") is None
    assert parse_uri("a random text") is None


def test_uri_default_dataspace():
    uri = "eml:///"
    assert uri == str(parse_uri(uri))
    assert uri == str(Uri())


def test_uri_empty_dataspace():
    uri = "eml:///dataspace('')"
    assert "eml:///" == str(parse_uri(uri))


def test_uri_dataspace():
    uri = "eml:///dataspace('rdms-db')"
    assert uri == str(parse_uri(uri))


def test_uri_dataspace_bis():
    uri = "eml:///dataspace('/folder-name/project-name')"
    assert uri == str(parse_uri(uri))


def test_uri_dataspace_query():
    uri = "eml:///dataspace('rdms-db')?$filter=Name eq 'mydb'"
    assert uri == str(parse_uri(uri))


def test_uri_collection():
    uri = "eml:///witsml20.Well/witsml20.Wellbore"
    assert uri == str(parse_uri(uri))


def test_uri_data_object_resqml():
    uri = "eml:///resqml20.obj_HorizonInterpretation(421a7a05-033a-450d-bcef-051352023578)"
    assert uri == str(parse_uri(uri))


def test_uri_data_object_witsml():
    uri = "eml:///witsml21.Well(uuid=ec8c3f16-1454-4f36-ae10-27d2a2680cf2)"
    assert uri == str(parse_uri(uri))


def test_uri_dataspace_data_object():
    uri = "eml:///dataspace('/folder-name/project-name')/resqml20.obj_HorizonInterpretation?query"
    assert uri == str(parse_uri(uri))


def test_uri_dataspace_data_object_query():
    uri = "eml:///dataspace('/folder-name/project-name')/resqml20.obj_HorizonInterpretation(uuid=421a7a05-033a-450d-bcef-051352023578,version='2.0')?query"
    assert uri == str(parse_uri(uri))


def test_uri_dataspace_data_object_collection_query():
    uri = "eml:///dataspace('test')/witsml20.Well(ec8c3f16-1454-4f36-ae10-27d2a2680cf2)/witsml20.Wellbore?query"
    assert uri == str(parse_uri(uri))


def test_uri_full():
    uri = "eml:///witsml20.Well(uuid=ec8c3f16-1454-4f36-ae10-27d2a2680cf2,version='1.0')/witsml20.Wellbore?query"
    assert uri == str(parse_uri(uri))
