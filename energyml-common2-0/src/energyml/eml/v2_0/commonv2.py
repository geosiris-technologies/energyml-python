from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
from xsdata.models.datatype import XmlDateTime
from generated.eml.v2_0.mod_3 import (
    ProjectedCrstype,
    VerticalCrstype,
)

__NAMESPACE__ = "http://www.energistics.org/energyml/data/commonv2"


class ApigammaRayUom(Enum):
    """
    :cvar G_API: API gamma ray unit
    """

    G_API = "gAPI"


class ApigravityUom(Enum):
    """
    :cvar D_API: API gravity unit
    """

    D_API = "dAPI"


class ApineutronUom(Enum):
    """
    :cvar N_API: API neutron unit
    """

    N_API = "nAPI"


class AbsorbedDoseUom(Enum):
    """
    :cvar C_GY: centigray
    :cvar CRD: hundredth of rad
    :cvar D_GY: decigray
    :cvar DRD: tenth of rad
    :cvar EGY: exagray
    :cvar ERD: million million million rad
    :cvar F_GY: femtogray
    :cvar FRD: femtorad
    :cvar GGY: gigagray
    :cvar GRD: thousand million rad
    :cvar GY: gray
    :cvar K_GY: kilogray
    :cvar KRD: thousand rad
    :cvar M_GY: milligray
    :cvar MGY_1: megagray
    :cvar MRD: million rad
    :cvar MRD_1: thousandth of rad
    :cvar N_GY: nanogray
    :cvar NRD: nanorad
    :cvar P_GY: picogray
    :cvar PRD: picorad
    :cvar RD: rad
    :cvar TGY: teragray
    :cvar TRD: million million rad
    :cvar U_GY: microgray
    :cvar URD: millionth of rad
    """

    C_GY = "cGy"
    CRD = "crd"
    D_GY = "dGy"
    DRD = "drd"
    EGY = "EGy"
    ERD = "Erd"
    F_GY = "fGy"
    FRD = "frd"
    GGY = "GGy"
    GRD = "Grd"
    GY = "Gy"
    K_GY = "kGy"
    KRD = "krd"
    M_GY = "mGy"
    MGY_1 = "MGy"
    MRD = "Mrd"
    MRD_1 = "mrd"
    N_GY = "nGy"
    NRD = "nrd"
    P_GY = "pGy"
    PRD = "prd"
    RD = "rd"
    TGY = "TGy"
    TRD = "Trd"
    U_GY = "uGy"
    URD = "urd"


@dataclass
class AbstractProjectedCrs:
    pass


@dataclass
class AbstractVerticalCrs:
    pass


class ActivityOfRadioactivityUom(Enum):
    """
    :cvar BQ: becquerel
    :cvar CI: curie
    :cvar GBQ: gigabecquerel
    :cvar MBQ: megabecquerel
    :cvar M_CI: thousandth of curie
    :cvar N_CI: nanocurie
    :cvar P_CI: picocurie
    :cvar TBQ: terabecquerel
    :cvar U_CI: millionth of curie
    """

    BQ = "Bq"
    CI = "Ci"
    GBQ = "GBq"
    MBQ = "MBq"
    M_CI = "mCi"
    N_CI = "nCi"
    P_CI = "pCi"
    TBQ = "TBq"
    U_CI = "uCi"


class AmountOfSubstancePerAmountOfSubstanceUom(Enum):
    """
    :cvar VALUE: percent
    :cvar MOLAR: percent [molar basis]
    :cvar EUC: euclid
    :cvar MOL_MOL: mole per mole
    :cvar N_EUC: nanoeuclid
    :cvar PPK: part per thousand
    :cvar PPM: part per million
    """

    VALUE = "%"
    MOLAR = "%[molar]"
    EUC = "Euc"
    MOL_MOL = "mol/mol"
    N_EUC = "nEuc"
    PPK = "ppk"
    PPM = "ppm"


class AmountOfSubstancePerAreaUom(Enum):
    """
    :cvar MOL_M2: gram-mole per square metre
    """

    MOL_M2 = "mol/m2"


class AmountOfSubstancePerTimePerAreaUom(Enum):
    """
    :cvar LBMOL_H_FT2: pound-mass-mole per hour square foot
    :cvar LBMOL_S_FT2: pound-mass-mole per second square foot
    :cvar MOL_S_M2: gram-mole per second square metre
    """

    LBMOL_H_FT2 = "lbmol/(h.ft2)"
    LBMOL_S_FT2 = "lbmol/(s.ft2)"
    MOL_S_M2 = "mol/(s.m2)"


class AmountOfSubstancePerTimeUom(Enum):
    """
    :cvar KMOL_H: kilogram-mole per hour
    :cvar KMOL_S: kilogram-mole per second
    :cvar LBMOL_H: pound-mass-mole per hour
    :cvar LBMOL_S: pound-mass-mole per second
    :cvar MOL_S: gram-mole per second
    """

    KMOL_H = "kmol/h"
    KMOL_S = "kmol/s"
    LBMOL_H = "lbmol/h"
    LBMOL_S = "lbmol/s"
    MOL_S = "mol/s"


class AmountOfSubstancePerVolumeUom(Enum):
    """
    :cvar KMOL_M3: kilogram-mole per cubic metre
    :cvar LBMOL_FT3: pound-mass-mole per cubic foot
    :cvar LBMOL_GAL_UK: pound-mass-mole per UK gallon
    :cvar LBMOL_GAL_US: pound-mass-mole per US gallon
    :cvar MOL_M3: gram-mole per cubic metre
    """

    KMOL_M3 = "kmol/m3"
    LBMOL_FT3 = "lbmol/ft3"
    LBMOL_GAL_UK = "lbmol/gal[UK]"
    LBMOL_GAL_US = "lbmol/gal[US]"
    MOL_M3 = "mol/m3"


class AmountOfSubstanceUom(Enum):
    """
    :cvar KMOL: kilogram-mole
    :cvar LBMOL: pound-mass-mole
    :cvar MMOL: milligram-mole
    :cvar MOL: gram-mole
    :cvar UMOL: microgram-mole
    """

    KMOL = "kmol"
    LBMOL = "lbmol"
    MMOL = "mmol"
    MOL = "mol"
    UMOL = "umol"


class AnglePerLengthUom(Enum):
    """
    :cvar VALUE_0_01_DEGA_FT: angular degree per hundred foot
    :cvar VALUE_1_30_DEGA_FT: angular degree per thirty foot
    :cvar VALUE_1_30_DEGA_M: angular degree per thirty metre
    :cvar DEGA_FT: angular degree per foot
    :cvar DEGA_M: angular degree per metre
    :cvar RAD_FT: radian per foot
    :cvar RAD_M: radian per metre
    :cvar REV_FT: revolution per foot
    :cvar REV_M: revolution per metre
    """

    VALUE_0_01_DEGA_FT = "0.01 dega/ft"
    VALUE_1_30_DEGA_FT = "1/30 dega/ft"
    VALUE_1_30_DEGA_M = "1/30 dega/m"
    DEGA_FT = "dega/ft"
    DEGA_M = "dega/m"
    RAD_FT = "rad/ft"
    RAD_M = "rad/m"
    REV_FT = "rev/ft"
    REV_M = "rev/m"


class AnglePerVolumeUom(Enum):
    """
    :cvar RAD_FT3: radian per cubic foot
    :cvar RAD_M3: radian per cubic metre
    """

    RAD_FT3 = "rad/ft3"
    RAD_M3 = "rad/m3"


class AngularAccelerationUom(Enum):
    """
    :cvar RAD_S2: radian per second squared
    :cvar RPM_S: (revolution per minute) per second
    """

    RAD_S2 = "rad/s2"
    RPM_S = "rpm/s"


class AngularVelocityUom(Enum):
    """
    :cvar DEGA_H: angular degree per hour
    :cvar DEGA_MIN: angular degree per minute
    :cvar DEGA_S: angular degree per second
    :cvar RAD_S: radian per second
    :cvar REV_S: revolution per second
    :cvar RPM: revolution per minute
    """

    DEGA_H = "dega/h"
    DEGA_MIN = "dega/min"
    DEGA_S = "dega/s"
    RAD_S = "rad/s"
    REV_S = "rev/s"
    RPM = "rpm"


class AreaPerAmountOfSubstanceUom(Enum):
    """
    :cvar M2_MOL: square metre per gram-mole
    """

    M2_MOL = "m2/mol"


class AreaPerAreaUom(Enum):
    """
    :cvar VALUE: percent
    :cvar AREA: percent [area basis]
    :cvar C_EUC: centieuclid
    :cvar EUC: euclid
    :cvar IN2_FT2: square inch per square foot
    :cvar IN2_IN2: square inch per square inch
    :cvar M2_M2: square metre per square metre
    :cvar MM2_MM2: square millimetre per square millimetre
    """

    VALUE = "%"
    AREA = "%[area]"
    C_EUC = "cEuc"
    EUC = "Euc"
    IN2_FT2 = "in2/ft2"
    IN2_IN2 = "in2/in2"
    M2_M2 = "m2/m2"
    MM2_MM2 = "mm2/mm2"


class AreaPerMassUom(Enum):
    """
    :cvar CM2_G: square centimetre per gram
    :cvar FT2_LBM: square foot per pound-mass
    :cvar M2_G: square metre per gram
    :cvar M2_KG: square metre per kilogram
    """

    CM2_G = "cm2/g"
    FT2_LBM = "ft2/lbm"
    M2_G = "m2/g"
    M2_KG = "m2/kg"


class AreaPerTimeUom(Enum):
    """
    :cvar CM2_S: square centimetre per second
    :cvar FT2_H: square foot per hour
    :cvar FT2_S: square foot per second
    :cvar IN2_S: square inch per second
    :cvar M2_D: square metre per day
    :cvar M2_H: square metre per hour
    :cvar M2_S: square metre per second
    :cvar MM2_S: square millimetre per second
    """

    CM2_S = "cm2/s"
    FT2_H = "ft2/h"
    FT2_S = "ft2/s"
    IN2_S = "in2/s"
    M2_D = "m2/d"
    M2_H = "m2/h"
    M2_S = "m2/s"
    MM2_S = "mm2/s"


class AreaPerVolumeUom(Enum):
    """
    :cvar VALUE_1_M: per metre
    :cvar B_CM3: barn per cubic centimetre
    :cvar CU: capture unit
    :cvar FT2_IN3: square foot per cubic inch
    :cvar M2_CM3: square metre per cubic centimetre
    :cvar M2_M3: square metre per cubic metre
    """

    VALUE_1_M = "1/m"
    B_CM3 = "b/cm3"
    CU = "cu"
    FT2_IN3 = "ft2/in3"
    M2_CM3 = "m2/cm3"
    M2_M3 = "m2/m3"


class AreaUom(Enum):
    """
    :cvar ACRE: acre
    :cvar B: barn
    :cvar CM2: square centimetre
    :cvar FT2: square foot
    :cvar HA: hectare
    :cvar IN2: square inch
    :cvar KM2: square kilometre
    :cvar M2: square metre
    :cvar MI_US_2: square US survey mile
    :cvar MI2: square mile
    :cvar MM2: square millimetre
    :cvar SECTION: section
    :cvar UM2: square micrometre
    :cvar YD2: square yard
    """

    ACRE = "acre"
    B = "b"
    CM2 = "cm2"
    FT2 = "ft2"
    HA = "ha"
    IN2 = "in2"
    KM2 = "km2"
    M2 = "m2"
    MI_US_2 = "mi[US]2"
    MI2 = "mi2"
    MM2 = "mm2"
    SECTION = "section"
    UM2 = "um2"
    YD2 = "yd2"


class AttenuationPerFrequencyIntervalUom(Enum):
    """
    :cvar B_O: bel per octave
    :cvar D_B_O: decibel per octave
    """

    B_O = "B/O"
    D_B_O = "dB/O"


class AxisOrder2D(Enum):
    """
    Defines the cordinate system axis order of the global CRS using the axis names
    (from EPSG database).

    :cvar EASTING_NORTHING: The first axis is easting and the second
        axis is northing.
    :cvar NORTHING_EASTING: The first axis is northing and the second
        asis is easting.
    :cvar WESTING_SOUTHING: The first axis is westing and the second
        axis is southing.
    :cvar SOUTHING_WESTING: The first axis is southing and the second
        axis is westing.
    :cvar NORTHING_WESTING: the first axis is northing and the second
        axis is westing.
    :cvar WESTING_NORTHING: the first axis is westing and the second
        axis is northing.
    """

    EASTING_NORTHING = "easting northing"
    NORTHING_EASTING = "northing easting"
    WESTING_SOUTHING = "westing southing"
    SOUTHING_WESTING = "southing westing"
    NORTHING_WESTING = "northing westing"
    WESTING_NORTHING = "westing northing"


class CapacitanceUom(Enum):
    """
    :cvar C_F: centifarad
    :cvar D_F: decifarad
    :cvar EF: exafarad
    :cvar F: farad
    :cvar F_F: femtofarad
    :cvar GF: gigafarad
    :cvar K_F: kilofarad
    :cvar M_F: millifarad
    :cvar MF_1: megafarad
    :cvar N_F: nanofarad
    :cvar P_F: picofarad
    :cvar TF: terafarad
    :cvar U_F: microfarad
    """

    C_F = "cF"
    D_F = "dF"
    EF = "EF"
    F = "F"
    F_F = "fF"
    GF = "GF"
    K_F = "kF"
    M_F = "mF"
    MF_1 = "MF"
    N_F = "nF"
    P_F = "pF"
    TF = "TF"
    U_F = "uF"


@dataclass
class Citation:
    """
    An ISO 19115 EIP-derived set of metadata attached to all specializations of
    AbstractObject to ensure the traceability of each individual independent (top
    level) element.

    :ivar title: One line description/name of the RESQML object. This is
        the equivalent in ISO 19115 of CI_Citation.title Legacy DCGroup
        - title
    :ivar originator: Name (or other human-readable identifier) of the
        person who initially originated the object or RESQML document in
        the source application. If that information is not available,
        the user who created the RESQML format file. The originator
        remains the same as the object is subsequently edited. This is
        the equivalent in ISO 19115 to the CI_Individual.name or the
        CI_Organization.name of the citedResponsibleParty whose role is
        "originator". Legacy DCGroup - author
    :ivar creation: Date and time the document was created in the source
        application or, if that information is not available, when it
        was saved to the RESQML format file. This is the equivalent of
        the ISO 19115 CI_Date where the CI_DateTypeCode = "creation" The
        type is the Energistics timestamp datatype which is the W3C
        xs:dateTime with the optional timezone offset from UTC made
        mandatory. Format: YYYY-MM-DDThh:mm:ssZ[+/-]hh:mm Legacy DCGroup
        - created
    :ivar format: Software or service that was used to originate the
        object and the file format created. Must be human and machine
        readable and unambiguously identify the software by including
        the company name, software name and software version. This is
        the equivalent in ISO 19115 to the distributionFormat.MD_Format.
        The ISO format for this is
        [vendor:applicationName]/fileExtension where the application
        name includes the version number of the application. SIG
        Implementation Notes 1. RESQML - Legacy DCGroup from v1.1 -
        publisher - fileExtension is not relevant and will be ignored if
        present. - vendor and applicationName are mandatory.
    :ivar editor: Name (or other human-readable identifier) of the last
        person who updated the object. This is the equivalent in ISO
        19115 to the CI_Individual.name or the CI_Organization.name of
        the citedResponsibleParty whose role is "editor". Legacy DCGroup
        - contributor
    :ivar last_update: Date and time the document was last modified in
        the source application or, if that information is not available,
        when it was last saved to the RESQML format file. This is the
        equivalent of the ISO 19115 CI_Date where the CI_DateTypeCode =
        "lastUpdate" The type is the Energistics timestamp datatype
        which is the W3C xs:dateTime with the optional timezone offset
        from UTC made mandatory. Format: YYYY-MM-DDThh:mm:ssZ[+/-]hh:mm
        Legacy DCGroup - modified
    :ivar version_string:
    :ivar description: User descriptive comments about the object.
        Intended for end-user use (human readable); not necessarily
        meant to be used by software. This is the equivalent of the ISO
        19115 abstract.CharacterString Legacy DCGroup - description
    :ivar descriptive_keywords: Key words to describe the activity, for
        example, history match or volumetric calculations, relevant to
        this object. Intended to be used in a search function by
        software. This is the equivalent in ISO 19115 of
        descriptiveKeywords.MD_Keywords Legacy DCGroup - subject
    """

    title: Optional[str] = field(
        default=None,
        metadata={
            "name": "Title",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/commonv2",
            "required": True,
            "min_length": 1,
            "max_length": 256,
            "white_space": "collapse",
        },
    )
    originator: Optional[str] = field(
        default=None,
        metadata={
            "name": "Originator",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/commonv2",
            "required": True,
            "min_length": 1,
            "max_length": 64,
            "white_space": "collapse",
        },
    )
    creation: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "Creation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/commonv2",
            "required": True,
        },
    )
    format: Optional[str] = field(
        default=None,
        metadata={
            "name": "Format",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/commonv2",
            "required": True,
            "min_length": 1,
            "max_length": 256,
            "white_space": "collapse",
        },
    )
    editor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Editor",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/commonv2",
            "min_length": 1,
            "max_length": 64,
            "white_space": "collapse",
        },
    )
    last_update: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "LastUpdate",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/commonv2",
        },
    )
    version_string: Optional[str] = field(
        default=None,
        metadata={
            "name": "VersionString",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/commonv2",
        },
    )
    description: Optional[str] = field(
        default=None,
        metadata={
            "name": "Description",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/commonv2",
            "min_length": 1,
            "max_length": 4000,
            "white_space": "collapse",
        },
    )
    descriptive_keywords: Optional[str] = field(
        default=None,
        metadata={
            "name": "DescriptiveKeywords",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/commonv2",
            "min_length": 1,
            "max_length": 4000,
            "white_space": "collapse",
        },
    )


@dataclass
class CustomData:
    """WITSML - Custom or User Defined Element and Attributes Component Schema.
    Specify custom element, attributes, and types in the custom data area.

    :ivar any_element: Any element or attribute in any namespace. It is
        strongly recommended that all custom data definitions be added
        to a unique namespace.
    """

    any_element: List[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
        },
    )


@dataclass
class DataObjectReference:
    """
    It only applies for Energistics data object.

    :ivar content_type: The content type of the referenced element.
    :ivar title:
    :ivar uuid: Reference to an object using its global UID.
    :ivar uuid_authority: The authority that issued and maintains the
        uuid of the referenced object. Used mainly in alias context.
    :ivar version_string: Indicates the version of the object which is
        referenced.
    """

    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "ContentType",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/commonv2",
            "required": True,
        },
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "name": "Title",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/commonv2",
            "required": True,
            "min_length": 1,
            "max_length": 256,
            "white_space": "collapse",
        },
    )
    uuid: Optional[str] = field(
        default=None,
        metadata={
            "name": "UUID",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/commonv2",
            "required": True,
            "pattern": r"[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}",
        },
    )
    uuid_authority: Optional[str] = field(
        default=None,
        metadata={
            "name": "UuidAuthority",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/commonv2",
        },
    )
    version_string: Optional[str] = field(
        default=None,
        metadata={
            "name": "VersionString",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/commonv2",
            "min_length": 1,
            "max_length": 64,
            "white_space": "collapse",
        },
    )


class DataTransferSpeedUom(Enum):
    """
    :cvar BIT_S: bit per second
    :cvar BYTE_S: byte per second
    """

    BIT_S = "bit/s"
    BYTE_S = "byte/s"


class DiffusionCoefficientUom(Enum):
    """
    :cvar M2_S: square metre per second
    """

    M2_S = "m2/s"


class DigitalStorageUom(Enum):
    """
    :cvar BIT: bit
    :cvar BYTE: byte
    :cvar KIBYTE: kibibyte
    :cvar MIBYTE: mebibyte
    """

    BIT = "bit"
    BYTE = "byte"
    KIBYTE = "Kibyte"
    MIBYTE = "Mibyte"


class DimensionlessUom(Enum):
    """
    :cvar VALUE: percent
    :cvar C_EUC: centieuclid
    :cvar D_EUC: decieuclid
    :cvar EEUC: exaeuclid
    :cvar EUC: euclid
    :cvar F_EUC: femtoeuclid
    :cvar GEUC: gigaeuclid
    :cvar K_EUC: kiloeuclid
    :cvar MEUC: megaeuclid
    :cvar M_EUC_1: millieuclid
    :cvar N_EUC: nanoeuclid
    :cvar P_EUC: picoeuclid
    :cvar PPK: part per thousand
    :cvar PPM: part per million
    :cvar TEUC: teraeuclid
    :cvar U_EUC: microeuclid
    """

    VALUE = "%"
    C_EUC = "cEuc"
    D_EUC = "dEuc"
    EEUC = "EEuc"
    EUC = "Euc"
    F_EUC = "fEuc"
    GEUC = "GEuc"
    K_EUC = "kEuc"
    MEUC = "MEuc"
    M_EUC_1 = "mEuc"
    N_EUC = "nEuc"
    P_EUC = "pEuc"
    PPK = "ppk"
    PPM = "ppm"
    TEUC = "TEuc"
    U_EUC = "uEuc"


class DipoleMomentUom(Enum):
    """
    :cvar C_M: coulomb metre
    """

    C_M = "C.m"


class DoseEquivalentUom(Enum):
    """
    :cvar MREM: thousandth of rem
    :cvar M_SV: millisievert
    :cvar REM: rem
    :cvar SV: sievert
    """

    MREM = "mrem"
    M_SV = "mSv"
    REM = "rem"
    SV = "Sv"


class DynamicViscosityUom(Enum):
    """
    :cvar C_P: centipoise
    :cvar D_P: decipoise
    :cvar DYNE_S_CM2: dyne second per square centimetre
    :cvar EP: exapoise
    :cvar F_P: femtopoise
    :cvar GP: gigapoise
    :cvar KGF_S_M2: thousand gram-force second per square metre
    :cvar K_P: kilopoise
    :cvar LBF_S_FT2: pound-force second per square foot
    :cvar LBF_S_IN2: pound-force second per square inch
    :cvar M_P: millipoise
    :cvar MP_1: megapoise
    :cvar M_PA_S: millipascal second
    :cvar N_S_M2: newton second per square metre
    :cvar N_P: nanopoise
    :cvar P: poise
    :cvar PA_S: pascal second
    :cvar P_P: picopoise
    :cvar PSI_S: psi second
    :cvar TP: terapoise
    :cvar U_P: micropoise
    """

    C_P = "cP"
    D_P = "dP"
    DYNE_S_CM2 = "dyne.s/cm2"
    EP = "EP"
    F_P = "fP"
    GP = "GP"
    KGF_S_M2 = "kgf.s/m2"
    K_P = "kP"
    LBF_S_FT2 = "lbf.s/ft2"
    LBF_S_IN2 = "lbf.s/in2"
    M_P = "mP"
    MP_1 = "MP"
    M_PA_S = "mPa.s"
    N_S_M2 = "N.s/m2"
    N_P = "nP"
    P = "P"
    PA_S = "Pa.s"
    P_P = "pP"
    PSI_S = "psi.s"
    TP = "TP"
    U_P = "uP"


class ElectricChargePerAreaUom(Enum):
    """
    :cvar C_CM2: coulomb per square centimetre
    :cvar C_M2: coulomb per square metre
    :cvar C_MM2: coulomb per square millimetre
    :cvar M_C_M2: millicoulomb per square metre
    """

    C_CM2 = "C/cm2"
    C_M2 = "C/m2"
    C_MM2 = "C/mm2"
    M_C_M2 = "mC/m2"


class ElectricChargePerMassUom(Enum):
    """
    :cvar A_S_KG: ampere second per kilogram
    :cvar C_G: coulomb per gram
    :cvar C_KG: coulomb per kilogram
    """

    A_S_KG = "A.s/kg"
    C_G = "C/g"
    C_KG = "C/kg"


class ElectricChargePerVolumeUom(Enum):
    """
    :cvar A_S_M3: ampere second per cubic metre
    :cvar C_CM3: coulomb per cubic centimetre
    :cvar C_M3: coulomb per cubic metre
    :cvar C_MM3: coulomb per cubic millimetre
    """

    A_S_M3 = "A.s/m3"
    C_CM3 = "C/cm3"
    C_M3 = "C/m3"
    C_MM3 = "C/mm3"


class ElectricChargeUom(Enum):
    """
    :cvar A_H: ampere hour
    :cvar A_S: ampere second
    :cvar C: coulomb
    :cvar C_C: centicoulomb
    :cvar D_C: decicoulomb
    :cvar EC: exacoulomb
    :cvar F_C: femtocoulomb
    :cvar GC: gigacoulomb
    :cvar K_C: kilocoulomb
    :cvar MC: megacoulomb
    :cvar M_C_1: millicoulomb
    :cvar N_C: nanocoulomb
    :cvar P_C: picocoulomb
    :cvar TC: teracoulomb
    :cvar U_C: microcoulomb
    """

    A_H = "A.h"
    A_S = "A.s"
    C = "C"
    C_C = "cC"
    D_C = "dC"
    EC = "EC"
    F_C = "fC"
    GC = "GC"
    K_C = "kC"
    MC = "MC"
    M_C_1 = "mC"
    N_C = "nC"
    P_C = "pC"
    TC = "TC"
    U_C = "uC"


class ElectricConductanceUom(Enum):
    """
    :cvar C_S: centisiemens
    :cvar D_S: decisiemens
    :cvar ES: exasiemens
    :cvar F_S: femtosiemens
    :cvar GS: gigasiemens
    :cvar K_S: kilosiemens
    :cvar M_S: millisiemens
    :cvar MS_1: megasiemens
    :cvar N_S: nanosiemens
    :cvar P_S: picosiemens
    :cvar S: siemens
    :cvar TS: terasiemens
    :cvar U_S: microsiemens
    """

    C_S = "cS"
    D_S = "dS"
    ES = "ES"
    F_S = "fS"
    GS = "GS"
    K_S = "kS"
    M_S = "mS"
    MS_1 = "MS"
    N_S = "nS"
    P_S = "pS"
    S = "S"
    TS = "TS"
    U_S = "uS"


class ElectricConductivityUom(Enum):
    """
    :cvar K_S_M: kilosiemens per metre
    :cvar M_S_CM: millisiemens per centimetre
    :cvar M_S_M: millisiemens per metre
    :cvar S_M: siemens per metre
    """

    K_S_M = "kS/m"
    M_S_CM = "mS/cm"
    M_S_M = "mS/m"
    S_M = "S/m"


class ElectricCurrentDensityUom(Enum):
    """
    :cvar A_CM2: ampere per square centimetre
    :cvar A_FT2: ampere per square foot
    :cvar A_M2: ampere per square metre
    :cvar A_MM2: ampere per square millimetre
    :cvar M_A_CM2: milliampere per square centimetre
    :cvar M_A_FT2: milliampere per square foot
    :cvar U_A_CM2: microampere per square centimetre
    :cvar U_A_IN2: microampere per square inch
    """

    A_CM2 = "A/cm2"
    A_FT2 = "A/ft2"
    A_M2 = "A/m2"
    A_MM2 = "A/mm2"
    M_A_CM2 = "mA/cm2"
    M_A_FT2 = "mA/ft2"
    U_A_CM2 = "uA/cm2"
    U_A_IN2 = "uA/in2"


class ElectricCurrentUom(Enum):
    """
    :cvar A: ampere
    :cvar C_A: centiampere
    :cvar D_A: deciampere
    :cvar EA: exaampere
    :cvar F_A: femtoampere
    :cvar GA: gigaampere
    :cvar K_A: kiloampere
    :cvar M_A: milliampere
    :cvar MA_1: megaampere
    :cvar N_A: nanoampere
    :cvar P_A: picoampere
    :cvar TA: teraampere
    :cvar U_A: microampere
    """

    A = "A"
    C_A = "cA"
    D_A = "dA"
    EA = "EA"
    F_A = "fA"
    GA = "GA"
    K_A = "kA"
    M_A = "mA"
    MA_1 = "MA"
    N_A = "nA"
    P_A = "pA"
    TA = "TA"
    U_A = "uA"


class ElectricFieldStrengthUom(Enum):
    """
    :cvar M_V_FT: millivolt per foot
    :cvar M_V_M: millivolt per metre
    :cvar U_V_FT: microvolt per foot
    :cvar U_V_M: microvolt per metre
    :cvar V_M: volt per metre
    """

    M_V_FT = "mV/ft"
    M_V_M = "mV/m"
    U_V_FT = "uV/ft"
    U_V_M = "uV/m"
    V_M = "V/m"


class ElectricPotentialDifferenceUom(Enum):
    """
    :cvar C_V: centivolt
    :cvar D_V: decivolt
    :cvar F_V: femtovolt
    :cvar GV: gigavolt
    :cvar K_V: kilovolt
    :cvar M_V: millivolt
    :cvar MV_1: megavolt
    :cvar N_V: nanovolt
    :cvar P_V: picovolt
    :cvar TV: teravolt
    :cvar U_V: microvolt
    :cvar V: volt
    """

    C_V = "cV"
    D_V = "dV"
    F_V = "fV"
    GV = "GV"
    K_V = "kV"
    M_V = "mV"
    MV_1 = "MV"
    N_V = "nV"
    P_V = "pV"
    TV = "TV"
    U_V = "uV"
    V = "V"


class ElectricResistancePerLengthUom(Enum):
    """
    :cvar OHM_M: ohm per metre
    :cvar UOHM_FT: microhm per foot
    :cvar UOHM_M: microhm per metre
    """

    OHM_M = "ohm/m"
    UOHM_FT = "uohm/ft"
    UOHM_M = "uohm/m"


class ElectricResistanceUom(Enum):
    """
    :cvar COHM: centiohm
    :cvar DOHM: deciohm
    :cvar EOHM: exaohm
    :cvar FOHM: femtoohm
    :cvar GOHM: gigaohm
    :cvar KOHM: kilohm
    :cvar MOHM: megohm
    :cvar MOHM_1: milliohm
    :cvar NOHM: nanoohm
    :cvar OHM: ohm
    :cvar POHM: picoohm
    :cvar TOHM: teraohm
    :cvar UOHM: microohm
    """

    COHM = "cohm"
    DOHM = "dohm"
    EOHM = "Eohm"
    FOHM = "fohm"
    GOHM = "Gohm"
    KOHM = "kohm"
    MOHM = "Mohm"
    MOHM_1 = "mohm"
    NOHM = "nohm"
    OHM = "ohm"
    POHM = "pohm"
    TOHM = "Tohm"
    UOHM = "uohm"


class ElectricalResistivityUom(Enum):
    """
    :cvar KOHM_M: kiloohm metre
    :cvar NOHM_MIL2_FT: nanoohm square mil per foot
    :cvar NOHM_MM2_M: nanoohm square milimetre per metre
    :cvar OHM_CM: ohm centimetre
    :cvar OHM_M: ohm metre
    :cvar OHM_M2_M: ohm square metre per metre
    """

    KOHM_M = "kohm.m"
    NOHM_MIL2_FT = "nohm.mil2/ft"
    NOHM_MM2_M = "nohm.mm2/m"
    OHM_CM = "ohm.cm"
    OHM_M = "ohm.m"
    OHM_M2_M = "ohm.m2/m"


class ElectromagneticMomentUom(Enum):
    """
    :cvar A_M2: ampere square metre
    """

    A_M2 = "A.m2"


class EnergyLengthPerAreaUom(Enum):
    """
    :cvar J_M_M2: joule metre per square metre
    :cvar KCAL_TH_M_CM2: thousand calorie metre per square centimetre
    """

    J_M_M2 = "J.m/m2"
    KCAL_TH_M_CM2 = "kcal[th].m/cm2"


class EnergyLengthPerTimeAreaTemperatureUom(Enum):
    """
    :cvar BTU_IT_IN_H_FT2_DELTA_F: BTU per (hour square foot delta
        Fahrenheit per inch)
    :cvar J_M_S_M2_DELTA_K: joule metre per second square metre delta
        kelvin
    :cvar K_J_M_H_M2_DELTA_K: kilojoule metre per hour square metre
        delta kelvin
    :cvar W_M_DELTA_K: watt per metre delta kelvin
    """

    BTU_IT_IN_H_FT2_DELTA_F = "Btu[IT].in/(h.ft2.deltaF)"
    J_M_S_M2_DELTA_K = "J.m/(s.m2.deltaK)"
    K_J_M_H_M2_DELTA_K = "kJ.m/(h.m2.deltaK)"
    W_M_DELTA_K = "W/(m.deltaK)"


class EnergyPerAreaUom(Enum):
    """
    :cvar ERG_CM2: erg per square centimetre
    :cvar J_CM2: joule per square centimetre
    :cvar J_M2: joule per square metre
    :cvar KGF_M_CM2: thousand gram-force metre per square centimetre
    :cvar LBF_FT_IN2: foot pound-force per square inch
    :cvar M_J_CM2: millijoule per square centimetre
    :cvar M_J_M2: millijoule per square metre
    :cvar N_M: newton per metre
    """

    ERG_CM2 = "erg/cm2"
    J_CM2 = "J/cm2"
    J_M2 = "J/m2"
    KGF_M_CM2 = "kgf.m/cm2"
    LBF_FT_IN2 = "lbf.ft/in2"
    M_J_CM2 = "mJ/cm2"
    M_J_M2 = "mJ/m2"
    N_M = "N/m"


class EnergyPerLengthUom(Enum):
    """
    :cvar J_M: joule per metre
    :cvar MJ_M: megajoule per metre
    """

    J_M = "J/m"
    MJ_M = "MJ/m"


class EnergyPerMassPerTimeUom(Enum):
    """
    :cvar MREM_H: thousandth of irem per hour
    :cvar M_SV_H: millisievert per hour
    :cvar REM_H: rem per hour
    :cvar SV_H: sievert per hour
    :cvar SV_S: sievert per second
    """

    MREM_H = "mrem/h"
    M_SV_H = "mSv/h"
    REM_H = "rem/h"
    SV_H = "Sv/h"
    SV_S = "Sv/s"


class EnergyPerMassUom(Enum):
    """
    :cvar BTU_IT_LBM: BTU per pound-mass
    :cvar CAL_TH_G: calorie per gram
    :cvar CAL_TH_KG: calorie per kilogram
    :cvar CAL_TH_LBM: calorie per pound-mass
    :cvar ERG_G: erg per gram
    :cvar ERG_KG: erg per kilogram
    :cvar HP_H_LBM: horsepower hour per pound-mass
    :cvar J_G: joule per gram
    :cvar J_KG: joule per kilogram
    :cvar KCAL_TH_G: thousand calorie per gram
    :cvar KCAL_TH_KG: thousand calorie per kilogram
    :cvar K_J_KG: kilojoule per kilogram
    :cvar K_W_H_KG: kilowatt hour per kilogram
    :cvar LBF_FT_LBM: foot pound-force per pound-mass
    :cvar MJ_KG: megajoule per kilogram
    :cvar MW_H_KG: megawatt hour per kilogram
    """

    BTU_IT_LBM = "Btu[IT]/lbm"
    CAL_TH_G = "cal[th]/g"
    CAL_TH_KG = "cal[th]/kg"
    CAL_TH_LBM = "cal[th]/lbm"
    ERG_G = "erg/g"
    ERG_KG = "erg/kg"
    HP_H_LBM = "hp.h/lbm"
    J_G = "J/g"
    J_KG = "J/kg"
    KCAL_TH_G = "kcal[th]/g"
    KCAL_TH_KG = "kcal[th]/kg"
    K_J_KG = "kJ/kg"
    K_W_H_KG = "kW.h/kg"
    LBF_FT_LBM = "lbf.ft/lbm"
    MJ_KG = "MJ/kg"
    MW_H_KG = "MW.h/kg"


class EnergyPerVolumeUom(Enum):
    """
    :cvar BTU_IT_BBL: BTU per barrel
    :cvar BTU_IT_FT3: BTU per cubic foot
    :cvar BTU_IT_GAL_UK: BTU per UK gallon
    :cvar BTU_IT_GAL_US: BTU per US gallon
    :cvar CAL_TH_CM3: calorie per cubic centimetre
    :cvar CAL_TH_M_L: calorie per millilitre
    :cvar CAL_TH_MM3: calorie per cubic millimetre
    :cvar ERG_CM3: erg per cubic centimetre
    :cvar ERG_M3: erg per cubic metre
    :cvar HP_H_BBL: horsepower hour per barrel
    :cvar J_DM3: joule per cubic decimetre
    :cvar J_M3: joule per cubic metre
    :cvar KCAL_TH_CM3: thousand calorie per cubic centimetre
    :cvar KCAL_TH_M3: thousand calorie per cubic metre
    :cvar K_J_DM3: kilojoule per cubic decimetre
    :cvar K_J_M3: kilojoule per cubic metre
    :cvar K_W_H_DM3: kilowatt hour per cubic decimetre
    :cvar K_W_H_M3: kilowatt hour per cubic metre
    :cvar LBF_FT_BBL: foot pound-force per barrel
    :cvar LBF_FT_GAL_US: foot pound-force per US gallon
    :cvar MJ_M3: megajoule per cubic metre
    :cvar MW_H_M3: megawatt hour per cubic metre
    :cvar TONF_US_MI_BBL: US ton-force mile per barrel
    """

    BTU_IT_BBL = "Btu[IT]/bbl"
    BTU_IT_FT3 = "Btu[IT]/ft3"
    BTU_IT_GAL_UK = "Btu[IT]/gal[UK]"
    BTU_IT_GAL_US = "Btu[IT]/gal[US]"
    CAL_TH_CM3 = "cal[th]/cm3"
    CAL_TH_M_L = "cal[th]/mL"
    CAL_TH_MM3 = "cal[th]/mm3"
    ERG_CM3 = "erg/cm3"
    ERG_M3 = "erg/m3"
    HP_H_BBL = "hp.h/bbl"
    J_DM3 = "J/dm3"
    J_M3 = "J/m3"
    KCAL_TH_CM3 = "kcal[th]/cm3"
    KCAL_TH_M3 = "kcal[th]/m3"
    K_J_DM3 = "kJ/dm3"
    K_J_M3 = "kJ/m3"
    K_W_H_DM3 = "kW.h/dm3"
    K_W_H_M3 = "kW.h/m3"
    LBF_FT_BBL = "lbf.ft/bbl"
    LBF_FT_GAL_US = "lbf.ft/gal[US]"
    MJ_M3 = "MJ/m3"
    MW_H_M3 = "MW.h/m3"
    TONF_US_MI_BBL = "tonf[US].mi/bbl"


class EnergyUom(Enum):
    """
    :cvar VALUE_1_E6_BTU_IT: million BTU
    :cvar A_J: attojoule
    :cvar BTU_IT: British thermal unit
    :cvar BTU_TH: thermochemical British thermal unit
    :cvar BTU_UK: United Kingdom British thermal unit
    :cvar CAL_IT: calorie [International Table]
    :cvar CAL_TH: calorie
    :cvar CCAL_TH: hundredth of calorie
    :cvar CE_V: centielectronvolt
    :cvar C_J: centijoule
    :cvar DCAL_TH: tenth of calorie
    :cvar DE_V: decielectronvolt
    :cvar D_J: decijoule
    :cvar ECAL_TH: million million million calorie
    :cvar EE_V: exaelectronvolt
    :cvar EJ: exajoule
    :cvar ERG: erg
    :cvar E_V: electronvolt
    :cvar FCAL_TH: femtocalorie
    :cvar FE_V: femtoelectronvolt
    :cvar F_J: femtojoule
    :cvar GCAL_TH: thousand million calorie
    :cvar GE_V: gigaelectronvolt
    :cvar GJ: gigajoule
    :cvar GW_H: gigawatt hour
    :cvar HP_H: horsepower hour
    :cvar HP_METRIC_H: metric-horsepower hour
    :cvar J: joule
    :cvar KCAL_TH: thousand calorie
    :cvar KE_V: kiloelectronvolt
    :cvar K_J: kilojoule
    :cvar K_W_H: kilowatt hour
    :cvar MCAL_TH: million calorie
    :cvar MCAL_TH_1: thousandth of calorie
    :cvar ME_V: millielectronvolt
    :cvar ME_V_1: megaelectronvolt
    :cvar MJ: megajoule
    :cvar M_J_1: millijoule
    :cvar MW_H: megawatt hour
    :cvar NCAL_TH: nanocalorie
    :cvar NE_V: nanoelectronvolt
    :cvar N_J: nanojoule
    :cvar PCAL_TH: picocalorie
    :cvar PE_V: picoelectronvolt
    :cvar P_J: picojoule
    :cvar QUAD: quad
    :cvar TCAL_TH: million million calorie
    :cvar TE_V: teraelectronvolt
    :cvar THERM_EC: European Community therm
    :cvar THERM_UK: United Kingdom therm
    :cvar THERM_US: United States therm
    :cvar TJ: terajoule
    :cvar TW_H: terrawatt hour
    :cvar UCAL_TH: millionth of calorie
    :cvar UE_V: microelectronvolt
    :cvar U_J: microjoule
    """

    VALUE_1_E6_BTU_IT = "1E6 Btu[IT]"
    A_J = "aJ"
    BTU_IT = "Btu[IT]"
    BTU_TH = "Btu[th]"
    BTU_UK = "Btu[UK]"
    CAL_IT = "cal[IT]"
    CAL_TH = "cal[th]"
    CCAL_TH = "ccal[th]"
    CE_V = "ceV"
    C_J = "cJ"
    DCAL_TH = "dcal[th]"
    DE_V = "deV"
    D_J = "dJ"
    ECAL_TH = "Ecal[th]"
    EE_V = "EeV"
    EJ = "EJ"
    ERG = "erg"
    E_V = "eV"
    FCAL_TH = "fcal[th]"
    FE_V = "feV"
    F_J = "fJ"
    GCAL_TH = "Gcal[th]"
    GE_V = "GeV"
    GJ = "GJ"
    GW_H = "GW.h"
    HP_H = "hp.h"
    HP_METRIC_H = "hp[metric].h"
    J = "J"
    KCAL_TH = "kcal[th]"
    KE_V = "keV"
    K_J = "kJ"
    K_W_H = "kW.h"
    MCAL_TH = "Mcal[th]"
    MCAL_TH_1 = "mcal[th]"
    ME_V = "meV"
    ME_V_1 = "MeV"
    MJ = "MJ"
    M_J_1 = "mJ"
    MW_H = "MW.h"
    NCAL_TH = "ncal[th]"
    NE_V = "neV"
    N_J = "nJ"
    PCAL_TH = "pcal[th]"
    PE_V = "peV"
    P_J = "pJ"
    QUAD = "quad"
    TCAL_TH = "Tcal[th]"
    TE_V = "TeV"
    THERM_EC = "therm[EC]"
    THERM_UK = "therm[UK]"
    THERM_US = "therm[US]"
    TJ = "TJ"
    TW_H = "TW.h"
    UCAL_TH = "ucal[th]"
    UE_V = "ueV"
    U_J = "uJ"


class ForceAreaUom(Enum):
    """
    :cvar DYNE_CM2: dyne square centimetre
    :cvar KGF_M2: thousand gram-force square metre
    :cvar K_N_M2: kilonewton square metre
    :cvar LBF_IN2: pound-force square inch
    :cvar M_N_M2: millinewton square metre
    :cvar N_M2: newton square metre
    :cvar PDL_CM2: poundal square centimetre
    :cvar TONF_UK_FT2: UK ton-force square foot
    :cvar TONF_US_FT2: US ton-force square foot
    """

    DYNE_CM2 = "dyne.cm2"
    KGF_M2 = "kgf.m2"
    K_N_M2 = "kN.m2"
    LBF_IN2 = "lbf.in2"
    M_N_M2 = "mN.m2"
    N_M2 = "N.m2"
    PDL_CM2 = "pdl.cm2"
    TONF_UK_FT2 = "tonf[UK].ft2"
    TONF_US_FT2 = "tonf[US].ft2"


class ForceLengthPerLengthUom(Enum):
    """
    :cvar KGF_M_M: thousand gram-force metre per metre
    :cvar LBF_FT_IN: foot pound-force per inch
    :cvar LBF_IN_IN: pound-force inch per inch
    :cvar N_M_M: newton metre per metre
    :cvar TONF_US_MI_FT: US ton-force mile per foot
    """

    KGF_M_M = "kgf.m/m"
    LBF_FT_IN = "lbf.ft/in"
    LBF_IN_IN = "lbf.in/in"
    N_M_M = "N.m/m"
    TONF_US_MI_FT = "tonf[US].mi/ft"


class ForcePerForceUom(Enum):
    """
    :cvar VALUE: percent
    :cvar EUC: euclid
    :cvar KGF_KGF: thousand gram-force per kilogram-force
    :cvar LBF_LBF: pound-force per pound-force
    :cvar N_N: newton per newton
    """

    VALUE = "%"
    EUC = "Euc"
    KGF_KGF = "kgf/kgf"
    LBF_LBF = "lbf/lbf"
    N_N = "N/N"


class ForcePerLengthUom(Enum):
    """
    :cvar VALUE_0_01_LBF_FT: pound-force per hundred foot
    :cvar VALUE_1_30_LBF_M: pound-force per thirty metre
    :cvar VALUE_1_30_N_M: newton per thirty metre
    :cvar DYNE_CM: dyne per centimetre
    :cvar KGF_CM: thousand gram-force per centimetre
    :cvar K_N_M: kilonewton per metre
    :cvar LBF_FT: pound-force per foot
    :cvar LBF_IN: pound-force per inch
    :cvar M_N_KM: millinewton per kilometre
    :cvar M_N_M: millinewton per metre
    :cvar N_M: newton per metre
    :cvar PDL_CM: poundal per centimetre
    :cvar TONF_UK_FT: UK ton-force per foot
    :cvar TONF_US_FT: US ton-force per foot
    """

    VALUE_0_01_LBF_FT = "0.01 lbf/ft"
    VALUE_1_30_LBF_M = "1/30 lbf/m"
    VALUE_1_30_N_M = "1/30 N/m"
    DYNE_CM = "dyne/cm"
    KGF_CM = "kgf/cm"
    K_N_M = "kN/m"
    LBF_FT = "lbf/ft"
    LBF_IN = "lbf/in"
    M_N_KM = "mN/km"
    M_N_M = "mN/m"
    N_M = "N/m"
    PDL_CM = "pdl/cm"
    TONF_UK_FT = "tonf[UK]/ft"
    TONF_US_FT = "tonf[US]/ft"


class ForcePerVolumeUom(Enum):
    """
    :cvar VALUE_0_001_PSI_FT: psi per thousand foot
    :cvar VALUE_0_01_PSI_FT: psi per hundred foot
    :cvar ATM_FT: standard atmosphere per foot
    :cvar ATM_HM: standard atmosphere per hundred metre
    :cvar ATM_M: standard atmosphere per metre
    :cvar BAR_KM: bar per kilometre
    :cvar BAR_M: bar per metre
    :cvar GPA_CM: gigapascal per centimetre
    :cvar K_PA_HM: kilopascal per hectometre
    :cvar K_PA_M: kilopascal per metre
    :cvar LBF_FT3: pound-force per cubic foot
    :cvar LBF_GAL_US: pound-force per US gallon
    :cvar MPA_M: megapascal per metre
    :cvar N_M3: newton per cubic metre
    :cvar PA_M: pascal per metre
    :cvar PSI_FT: psi per foot
    :cvar PSI_M: psi per metre
    """

    VALUE_0_001_PSI_FT = "0.001 psi/ft"
    VALUE_0_01_PSI_FT = "0.01 psi/ft"
    ATM_FT = "atm/ft"
    ATM_HM = "atm/hm"
    ATM_M = "atm/m"
    BAR_KM = "bar/km"
    BAR_M = "bar/m"
    GPA_CM = "GPa/cm"
    K_PA_HM = "kPa/hm"
    K_PA_M = "kPa/m"
    LBF_FT3 = "lbf/ft3"
    LBF_GAL_US = "lbf/gal[US]"
    MPA_M = "MPa/m"
    N_M3 = "N/m3"
    PA_M = "Pa/m"
    PSI_FT = "psi/ft"
    PSI_M = "psi/m"


class ForceUom(Enum):
    """
    :cvar VALUE_10_K_N: ten kilonewton
    :cvar C_N: centinewton
    :cvar DA_N: dekanewton
    :cvar D_N: decinewton
    :cvar DYNE: dyne
    :cvar EN: exanewton
    :cvar F_N: femtonewton
    :cvar GF: gram-force
    :cvar GN: giganewton
    :cvar H_N: hectonewton
    :cvar KDYNE: kilodyne
    :cvar KGF: thousand gram-force
    :cvar KLBF: thousand pound-force
    :cvar K_N: kilonewton
    :cvar LBF: pound-force
    :cvar MGF: million gram-force
    :cvar M_N: millinewton
    :cvar MN_1: meganewton
    :cvar N: newton
    :cvar N_N: nanonewton
    :cvar OZF: ounce-force
    :cvar PDL: poundal
    :cvar P_N: piconewton
    :cvar TN: teranewton
    :cvar TONF_UK: UK ton-force
    :cvar TONF_US: US ton-force
    :cvar U_N: micronewton
    """

    VALUE_10_K_N = "10 kN"
    C_N = "cN"
    DA_N = "daN"
    D_N = "dN"
    DYNE = "dyne"
    EN = "EN"
    F_N = "fN"
    GF = "gf"
    GN = "GN"
    H_N = "hN"
    KDYNE = "kdyne"
    KGF = "kgf"
    KLBF = "klbf"
    K_N = "kN"
    LBF = "lbf"
    MGF = "Mgf"
    M_N = "mN"
    MN_1 = "MN"
    N = "N"
    N_N = "nN"
    OZF = "ozf"
    PDL = "pdl"
    P_N = "pN"
    TN = "TN"
    TONF_UK = "tonf[UK]"
    TONF_US = "tonf[US]"
    U_N = "uN"


class FrequencyIntervalUom(Enum):
    """
    :cvar O: octave
    """

    O = "O"


class FrequencyUom(Enum):
    """
    :cvar C_HZ: centihertz
    :cvar D_HZ: decihertz
    :cvar EHZ: exahertz
    :cvar F_HZ: femtohertz
    :cvar GHZ: gigahertz
    :cvar HZ: hertz
    :cvar K_HZ: kilohertz
    :cvar M_HZ: millihertz
    :cvar MHZ_1: megahertz
    :cvar N_HZ: nanohertz
    :cvar P_HZ: picohertz
    :cvar THZ: terahertz
    :cvar U_HZ: microhertz
    """

    C_HZ = "cHz"
    D_HZ = "dHz"
    EHZ = "EHz"
    F_HZ = "fHz"
    GHZ = "GHz"
    HZ = "Hz"
    K_HZ = "kHz"
    M_HZ = "mHz"
    MHZ_1 = "MHz"
    N_HZ = "nHz"
    P_HZ = "pHz"
    THZ = "THz"
    U_HZ = "uHz"


class HeatCapacityUom(Enum):
    """
    :cvar J_DELTA_K: joule per delta kelvin
    """

    J_DELTA_K = "J/deltaK"


class HeatFlowRateUom(Enum):
    """
    :cvar VALUE_1_E6_BTU_IT_H: million BTU per hour
    :cvar BTU_IT_H: BTU per hour
    :cvar BTU_IT_MIN: BTU per minute
    :cvar BTU_IT_S: BTU per second
    :cvar CAL_TH_H: calorie per hour
    :cvar EJ_A: exajoule per julian-year
    :cvar ERG_A: erg per julian-year
    :cvar GW: gigawatt
    :cvar J_S: joule per second
    :cvar KCAL_TH_H: thousand calorie per hour
    :cvar K_W: kilowatt
    :cvar LBF_FT_MIN: foot pound-force per minute
    :cvar LBF_FT_S: foot pound-force per second
    :cvar MJ_A: megajoule per julian-year
    :cvar MW: megawatt
    :cvar M_W_1: milliwatt
    :cvar N_W: nanowatt
    :cvar QUAD_A: quad per julian-year
    :cvar TJ_A: terajoule per julian-year
    :cvar TW: terawatt
    :cvar UCAL_TH_S: millionth of calorie per second
    :cvar U_W: microwatt
    :cvar W: watt
    """

    VALUE_1_E6_BTU_IT_H = "1E6 Btu[IT]/h"
    BTU_IT_H = "Btu[IT]/h"
    BTU_IT_MIN = "Btu[IT]/min"
    BTU_IT_S = "Btu[IT]/s"
    CAL_TH_H = "cal[th]/h"
    EJ_A = "EJ/a"
    ERG_A = "erg/a"
    GW = "GW"
    J_S = "J/s"
    KCAL_TH_H = "kcal[th]/h"
    K_W = "kW"
    LBF_FT_MIN = "lbf.ft/min"
    LBF_FT_S = "lbf.ft/s"
    MJ_A = "MJ/a"
    MW = "MW"
    M_W_1 = "mW"
    N_W = "nW"
    QUAD_A = "quad/a"
    TJ_A = "TJ/a"
    TW = "TW"
    UCAL_TH_S = "ucal[th]/s"
    U_W = "uW"
    W = "W"


class HeatTransferCoefficientUom(Enum):
    """
    :cvar BTU_IT_H_FT2_DELTA_F: BTU per hour square foot delta
        Fahrenheit
    :cvar BTU_IT_H_FT2_DELTA_R: BTU per hour square foot delta Rankine
    :cvar BTU_IT_H_M2_DELTA_C: BTU per hour square metre delta Celsius
    :cvar BTU_IT_S_FT2_DELTA_F: (BTU per second) per square foot delta
        Fahrenheit
    :cvar CAL_TH_H_CM2_DELTA_C: calorie per hour square centimetre delta
        Celsius
    :cvar CAL_TH_S_CM2_DELTA_C: calorie per second square centimetre
        delta Celsius
    :cvar J_S_M2_DELTA_C: joule per second square metre delta Celsius
    :cvar KCAL_TH_H_M2_DELTA_C: thousand calorie per hour square metre
        delta Celsius
    :cvar K_J_H_M2_DELTA_K: kilojoule per hour square metre delta kelvin
    :cvar K_W_M2_DELTA_K: kilowatt per square metre delta kelvin
    :cvar W_M2_DELTA_K: watt per square metre delta kelvin
    """

    BTU_IT_H_FT2_DELTA_F = "Btu[IT]/(h.ft2.deltaF)"
    BTU_IT_H_FT2_DELTA_R = "Btu[IT]/(h.ft2.deltaR)"
    BTU_IT_H_M2_DELTA_C = "Btu[IT]/(h.m2.deltaC)"
    BTU_IT_S_FT2_DELTA_F = "Btu[IT]/(s.ft2.deltaF)"
    CAL_TH_H_CM2_DELTA_C = "cal[th]/(h.cm2.deltaC)"
    CAL_TH_S_CM2_DELTA_C = "cal[th]/(s.cm2.deltaC)"
    J_S_M2_DELTA_C = "J/(s.m2.deltaC)"
    KCAL_TH_H_M2_DELTA_C = "kcal[th]/(h.m2.deltaC)"
    K_J_H_M2_DELTA_K = "kJ/(h.m2.deltaK)"
    K_W_M2_DELTA_K = "kW/(m2.deltaK)"
    W_M2_DELTA_K = "W/(m2.deltaK)"


class IlluminanceUom(Enum):
    """
    :cvar FOOTCANDLE: footcandle
    :cvar KLX: kilolux
    :cvar LM_M2: lumen per square metre
    :cvar LX: lux
    """

    FOOTCANDLE = "footcandle"
    KLX = "klx"
    LM_M2 = "lm/m2"
    LX = "lx"


class InductanceUom(Enum):
    """
    :cvar C_H: centihenry
    :cvar D_H: decihenry
    :cvar EH: exahenry
    :cvar F_H: femtohenry
    :cvar GH: gigahenry
    :cvar H: henry
    :cvar K_H: kilohenry
    :cvar MH: megahenry
    :cvar M_H_1: millihenry
    :cvar N_H: nanohenry
    :cvar TH: terahenry
    :cvar U_H: microhenry
    """

    C_H = "cH"
    D_H = "dH"
    EH = "EH"
    F_H = "fH"
    GH = "GH"
    H = "H"
    K_H = "kH"
    MH = "MH"
    M_H_1 = "mH"
    N_H = "nH"
    TH = "TH"
    U_H = "uH"


class IsothermalCompressibilityUom(Enum):
    """
    :cvar DM3_K_W_H: cubic decimetre per kilowatt hour
    :cvar DM3_MJ: cubic decimetre per megajoule
    :cvar M3_K_W_H: cubic metre per kilowatt hour
    :cvar M3_J: cubic metre per joule
    :cvar MM3_J: cubic millimetre per joule
    :cvar PT_UK_HP_H: UK pint per horsepower hour
    """

    DM3_K_W_H = "dm3/(kW.h)"
    DM3_MJ = "dm3/MJ"
    M3_K_W_H = "m3/(kW.h)"
    M3_J = "m3/J"
    MM3_J = "mm3/J"
    PT_UK_HP_H = "pt[UK]/(hp.h)"


class KinematicViscosityUom(Enum):
    """
    :cvar CM2_S: square centimetre per second
    :cvar C_ST: centistokes
    :cvar FT2_H: square foot per hour
    :cvar FT2_S: square foot per second
    :cvar IN2_S: square inch per second
    :cvar M2_H: square metre per hour
    :cvar M2_S: square metre per second
    :cvar MM2_S: square millimetre per second
    :cvar PA_S_M3_KG: pascal second square metre per kilogram
    :cvar ST: stokes
    """

    CM2_S = "cm2/s"
    C_ST = "cSt"
    FT2_H = "ft2/h"
    FT2_S = "ft2/s"
    IN2_S = "in2/s"
    M2_H = "m2/h"
    M2_S = "m2/s"
    MM2_S = "mm2/s"
    PA_S_M3_KG = "Pa.s.m3/kg"
    ST = "St"


class LengthPerLengthUom(Enum):
    """
    :cvar VALUE: percent
    :cvar VALUE_0_01_FT_FT: foot per hundred foot
    :cvar VALUE_1_30_M_M: metre per thirty metre
    :cvar EUC: euclid
    :cvar FT_FT: foot per foot
    :cvar FT_IN: foot per inch
    :cvar FT_M: foot per metre
    :cvar FT_MI: foot per mile
    :cvar KM_CM: kilometre per centimetre
    :cvar M_CM: metre per centimetre
    :cvar M_KM: metre per kilometre
    :cvar M_M: metre per metre
    :cvar MI_IN: mile per inch
    """

    VALUE = "%"
    VALUE_0_01_FT_FT = "0.01 ft/ft"
    VALUE_1_30_M_M = "1/30 m/m"
    EUC = "Euc"
    FT_FT = "ft/ft"
    FT_IN = "ft/in"
    FT_M = "ft/m"
    FT_MI = "ft/mi"
    KM_CM = "km/cm"
    M_CM = "m/cm"
    M_KM = "m/km"
    M_M = "m/m"
    MI_IN = "mi/in"


class LengthPerMassUom(Enum):
    """
    :cvar FT_LBM: foot per pound-mass
    :cvar M_KG: metre per kilogram
    """

    FT_LBM = "ft/lbm"
    M_KG = "m/kg"


class LengthPerPressureUom(Enum):
    """
    :cvar FT_PSI: foot per psi
    :cvar M_K_PA: metre per kilopascal
    :cvar M_PA: metre per Pascal
    """

    FT_PSI = "ft/psi"
    M_K_PA = "m/kPa"
    M_PA = "m/Pa"


class LengthPerTemperatureUom(Enum):
    """
    :cvar FT_DELTA_F: foot per delta Fahrenheit
    :cvar M_DELTA_K: metre per delta kelvin
    """

    FT_DELTA_F = "ft/deltaF"
    M_DELTA_K = "m/deltaK"


class LengthPerTimeUom(Enum):
    """
    :cvar VALUE_1000_FT_H: thousand foot per hour
    :cvar VALUE_1000_FT_S: thousand foot per second
    :cvar CM_A: centimetre per julian-year
    :cvar CM_S: centimetre per second
    :cvar DM_S: decimetre per second
    :cvar FT_D: foot per day
    :cvar FT_H: foot per hour
    :cvar FT_MIN: foot per minute
    :cvar FT_MS: foot per millisecond
    :cvar FT_S: foot per second
    :cvar FT_US: foot per microsecond
    :cvar IN_A: inch per julian-year
    :cvar IN_MIN: inch per minute
    :cvar IN_S: inch per second
    :cvar KM_H: kilometre per hour
    :cvar KM_S: kilometre per second
    :cvar KNOT: knot
    :cvar M_D: metre per day
    :cvar M_H: metre per hour
    :cvar M_MIN: metre per minute
    :cvar M_MS: metre per millisecond
    :cvar M_S: metre per second
    :cvar MI_H: mile per hour
    :cvar MIL_A: mil per julian-year
    :cvar MM_A: millimetre per julian-year
    :cvar MM_S_1: millimetre per second
    :cvar NM_S: nanometre per second
    :cvar UM_S: micrometre per second
    """

    VALUE_1000_FT_H = "1000 ft/h"
    VALUE_1000_FT_S = "1000 ft/s"
    CM_A = "cm/a"
    CM_S = "cm/s"
    DM_S = "dm/s"
    FT_D = "ft/d"
    FT_H = "ft/h"
    FT_MIN = "ft/min"
    FT_MS = "ft/ms"
    FT_S = "ft/s"
    FT_US = "ft/us"
    IN_A = "in/a"
    IN_MIN = "in/min"
    IN_S = "in/s"
    KM_H = "km/h"
    KM_S = "km/s"
    KNOT = "knot"
    M_D = "m/d"
    M_H = "m/h"
    M_MIN = "m/min"
    M_MS = "m/ms"
    M_S = "m/s"
    MI_H = "mi/h"
    MIL_A = "mil/a"
    MM_A = "mm/a"
    MM_S_1 = "mm/s"
    NM_S = "nm/s"
    UM_S = "um/s"


class LengthPerVolumeUom(Enum):
    """
    :cvar FT_BBL: foot per barrel
    :cvar FT_FT3: foot per cubic foot
    :cvar FT_GAL_US: foot per US gallon
    :cvar KM_DM3: kilometre per cubic decimetre
    :cvar KM_L: kilometre per litre
    :cvar M_M3: metre per cubic metre
    :cvar MI_GAL_UK: mile per UK gallon
    :cvar MI_GAL_US: mile per US gallon
    """

    FT_BBL = "ft/bbl"
    FT_FT3 = "ft/ft3"
    FT_GAL_US = "ft/gal[US]"
    KM_DM3 = "km/dm3"
    KM_L = "km/L"
    M_M3 = "m/m3"
    MI_GAL_UK = "mi/gal[UK]"
    MI_GAL_US = "mi/gal[US]"


class LengthUom(Enum):
    """
    :cvar VALUE_0_1_FT: tenth of foot
    :cvar VALUE_0_1_FT_US: tenth of US survey foot
    :cvar VALUE_0_1_IN: tenth of inch
    :cvar VALUE_0_1_YD: tenth of yard
    :cvar VALUE_1_16_IN: sixteenth of inch
    :cvar VALUE_1_2_FT: half of Foot
    :cvar VALUE_1_32_IN: thirty-second of inch
    :cvar VALUE_1_64_IN: sixty-fourth of inch
    :cvar VALUE_10_FT: ten foot
    :cvar VALUE_10_IN: ten inch
    :cvar VALUE_10_KM: 10 kilometre
    :cvar VALUE_100_FT: hundred foot
    :cvar VALUE_100_KM: 100 kilometre
    :cvar VALUE_1000_FT: thousand foot
    :cvar VALUE_30_FT: thirty foot
    :cvar VALUE_30_M: thirty metres
    :cvar ANGSTROM: angstrom
    :cvar CHAIN: chain
    :cvar CHAIN_BN_A: British chain [Benoit 1895 A]
    :cvar CHAIN_BN_B: British chain [Benoit 1895 B]
    :cvar CHAIN_CLA: Clarke chain
    :cvar CHAIN_IND37: Indian Chain [1937]
    :cvar CHAIN_SE: British chain [Sears 1922]
    :cvar CHAIN_SE_T: British chain [Sears 1922 truncated]
    :cvar CHAIN_US: US survey chain
    :cvar CM: centimetre
    :cvar DAM: dekametre
    :cvar DM: decimetre
    :cvar EM: exametre
    :cvar FATHOM: international fathom
    :cvar FM: femtometre
    :cvar FT: foot
    :cvar FT_BN_A: British foot [Benoit 1895 A]
    :cvar FT_BN_B: British foot [Benoit 1895 B]
    :cvar FT_BR36: British foot [1936]
    :cvar FT_BR65: British foot [1865]
    :cvar FT_CLA: Clarke foot
    :cvar FT_GC: Gold Coast foot
    :cvar FT_IND: indian foot
    :cvar FT_IND37: indian foot [1937]
    :cvar FT_IND62: indian foot ]1962]
    :cvar FT_IND75: indian foot [1975]
    :cvar FT_SE: British foot [Sears 1922]
    :cvar FT_SE_T: British foot [Sears 1922 truncated]
    :cvar FT_US: US survey foot
    :cvar FUR_US: furlong US survey
    :cvar GM: gigametre
    :cvar HM: hectometre
    :cvar IN: inch
    :cvar IN_US: US survey inch
    :cvar KM: kilometre
    :cvar LINK: link
    :cvar LINK_BN_A: British link [Benoit 1895 A]
    :cvar LINK_BN_B: British link [Benoit 1895 B]
    :cvar LINK_CLA: Clarke link
    :cvar LINK_SE: British link [Sears 1922]
    :cvar LINK_SE_T: British link [Sears 1922 truncated]
    :cvar LINK_US: US survey link
    :cvar M: metre
    :cvar M_GER: German legal metre
    :cvar MI: mile
    :cvar MI_NAUT: international nautical mile
    :cvar MI_NAUT_UK: United Kingdom nautical mile
    :cvar MI_US: US survey mile
    :cvar MIL: mil
    :cvar MM: megametre
    :cvar MM_1: millimetre
    :cvar NM: nanometre
    :cvar PM: picometre
    :cvar ROD_US: rod US Survey
    :cvar TM: terametre
    :cvar UM: micrometre
    :cvar YD: yard
    :cvar YD_BN_A: British yard [Benoit 1895 A]
    :cvar YD_BN_B: British yard [Benoit 1895 B]
    :cvar YD_CLA: Clarke yard
    :cvar YD_IND: Indian yard
    :cvar YD_IND37: Indian yard [1937]
    :cvar YD_IND62: Indian yard [1962]
    :cvar YD_IND75: Indian yard [1975]
    :cvar YD_SE: British yard [Sears 1922]
    :cvar YD_SE_T: British yard [Sears 1922 truncated]
    :cvar YD_US: US survey yard
    """

    VALUE_0_1_FT = "0.1 ft"
    VALUE_0_1_FT_US = "0.1 ft[US]"
    VALUE_0_1_IN = "0.1 in"
    VALUE_0_1_YD = "0.1 yd"
    VALUE_1_16_IN = "1/16 in"
    VALUE_1_2_FT = "1/2 ft"
    VALUE_1_32_IN = "1/32 in"
    VALUE_1_64_IN = "1/64 in"
    VALUE_10_FT = "10 ft"
    VALUE_10_IN = "10 in"
    VALUE_10_KM = "10 km"
    VALUE_100_FT = "100 ft"
    VALUE_100_KM = "100 km"
    VALUE_1000_FT = "1000 ft"
    VALUE_30_FT = "30 ft"
    VALUE_30_M = "30 m"
    ANGSTROM = "angstrom"
    CHAIN = "chain"
    CHAIN_BN_A = "chain[BnA]"
    CHAIN_BN_B = "chain[BnB]"
    CHAIN_CLA = "chain[Cla]"
    CHAIN_IND37 = "chain[Ind37]"
    CHAIN_SE = "chain[Se]"
    CHAIN_SE_T = "chain[SeT]"
    CHAIN_US = "chain[US]"
    CM = "cm"
    DAM = "dam"
    DM = "dm"
    EM = "Em"
    FATHOM = "fathom"
    FM = "fm"
    FT = "ft"
    FT_BN_A = "ft[BnA]"
    FT_BN_B = "ft[BnB]"
    FT_BR36 = "ft[Br36]"
    FT_BR65 = "ft[Br65]"
    FT_CLA = "ft[Cla]"
    FT_GC = "ft[GC]"
    FT_IND = "ft[Ind]"
    FT_IND37 = "ft[Ind37]"
    FT_IND62 = "ft[Ind62]"
    FT_IND75 = "ft[Ind75]"
    FT_SE = "ft[Se]"
    FT_SE_T = "ft[SeT]"
    FT_US = "ft[US]"
    FUR_US = "fur[US]"
    GM = "Gm"
    HM = "hm"
    IN = "in"
    IN_US = "in[US]"
    KM = "km"
    LINK = "link"
    LINK_BN_A = "link[BnA]"
    LINK_BN_B = "link[BnB]"
    LINK_CLA = "link[Cla]"
    LINK_SE = "link[Se]"
    LINK_SE_T = "link[SeT]"
    LINK_US = "link[US]"
    M = "m"
    M_GER = "m[Ger]"
    MI = "mi"
    MI_NAUT = "mi[naut]"
    MI_NAUT_UK = "mi[nautUK]"
    MI_US = "mi[US]"
    MIL = "mil"
    MM = "Mm"
    MM_1 = "mm"
    NM = "nm"
    PM = "pm"
    ROD_US = "rod[US]"
    TM = "Tm"
    UM = "um"
    YD = "yd"
    YD_BN_A = "yd[BnA]"
    YD_BN_B = "yd[BnB]"
    YD_CLA = "yd[Cla]"
    YD_IND = "yd[Ind]"
    YD_IND37 = "yd[Ind37]"
    YD_IND62 = "yd[Ind62]"
    YD_IND75 = "yd[Ind75]"
    YD_SE = "yd[Se]"
    YD_SE_T = "yd[SeT]"
    YD_US = "yd[US]"


class LightExposureUom(Enum):
    """
    :cvar FOOTCANDLE_S: footcandle second
    :cvar LX_S: lux second
    """

    FOOTCANDLE_S = "footcandle.s"
    LX_S = "lx.s"


class LinearAccelerationUom(Enum):
    """
    :cvar CM_S2: centimetre per square second
    :cvar FT_S2: foot per second squared
    :cvar GAL: galileo
    :cvar GN: gravity
    :cvar IN_S2: inch per second squared
    :cvar M_S2: metre per second squared
    :cvar M_GAL: milligalileo
    :cvar MGN: thousandth of gravity
    """

    CM_S2 = "cm/s2"
    FT_S2 = "ft/s2"
    GAL = "Gal"
    GN = "gn"
    IN_S2 = "in/s2"
    M_S2 = "m/s2"
    M_GAL = "mGal"
    MGN = "mgn"


class LinearThermalExpansionUom(Enum):
    """
    :cvar VALUE_1_DELTA_K: per delta kelvin
    :cvar IN_IN_DELTA_F: inch per inch delta Fahrenheit
    :cvar M_M_DELTA_K: metre per metre delta kelvin
    :cvar MM_MM_DELTA_K: millimetre per millimetre delta kelvin
    """

    VALUE_1_DELTA_K = "1/deltaK"
    IN_IN_DELTA_F = "in/(in.deltaF)"
    M_M_DELTA_K = "m/(m.deltaK)"
    MM_MM_DELTA_K = "mm/(mm.deltaK)"


class LogarithmicPowerRatioPerLengthUom(Enum):
    """
    :cvar B_M: bel per metre
    :cvar D_B_FT: decibel per foot
    :cvar D_B_KM: decibel per kilometre
    :cvar D_B_M: decibel per metre
    """

    B_M = "B/m"
    D_B_FT = "dB/ft"
    D_B_KM = "dB/km"
    D_B_M = "dB/m"


class LogarithmicPowerRatioUom(Enum):
    """
    :cvar B: bel
    :cvar D_B: decibel
    """

    B = "B"
    D_B = "dB"


class LuminanceUom(Enum):
    """
    :cvar CD_M2: candela per square metre
    """

    CD_M2 = "cd/m2"


class LuminousEfficacyUom(Enum):
    """
    :cvar LM_W: lumen per watt
    """

    LM_W = "lm/W"


class LuminousFluxUom(Enum):
    """
    :cvar LM: lumen
    """

    LM = "lm"


class LuminousIntensityUom(Enum):
    """
    :cvar CD: candela
    :cvar KCD: kilocandela
    """

    CD = "cd"
    KCD = "kcd"


class MagneticDipoleMomentUom(Enum):
    """
    :cvar WB_M: weber metre
    """

    WB_M = "Wb.m"


class MagneticFieldStrengthUom(Enum):
    """
    :cvar A_M: ampere per metre
    :cvar A_MM: ampere per millimetre
    :cvar OE: oersted
    """

    A_M = "A/m"
    A_MM = "A/mm"
    OE = "Oe"


class MagneticFluxDensityPerLengthUom(Enum):
    """
    :cvar GAUSS_CM: gauss per centimetre
    :cvar M_T_DM: millitesla per decimetre
    :cvar T_M: tesla per metre
    """

    GAUSS_CM = "gauss/cm"
    M_T_DM = "mT/dm"
    T_M = "T/m"


class MagneticFluxDensityUom(Enum):
    """
    :cvar CGAUSS: centigauss
    :cvar C_T: centitesla
    :cvar DGAUSS: decigauss
    :cvar D_T: decitesla
    :cvar EGAUSS: exagauss
    :cvar ET: exatesla
    :cvar FGAUSS: femtogauss
    :cvar F_T: femtotesla
    :cvar GAUSS: gauss
    :cvar GGAUSS: gigagauss
    :cvar GT: gigatesla
    :cvar KGAUSS: kilogauss
    :cvar K_T: kilotesla
    :cvar MGAUSS: milligauss
    :cvar MGAUSS_1: megagauss
    :cvar M_T: millitesla
    :cvar NGAUSS: nanogauss
    :cvar N_T: nanotesla
    :cvar PGAUSS: picogauss
    :cvar P_T: picotesla
    :cvar T: tesla
    :cvar TGAUSS: teragauss
    :cvar TT: teratesla
    :cvar UGAUSS: microgauss
    :cvar U_T: microtesla
    """

    CGAUSS = "cgauss"
    C_T = "cT"
    DGAUSS = "dgauss"
    D_T = "dT"
    EGAUSS = "Egauss"
    ET = "ET"
    FGAUSS = "fgauss"
    F_T = "fT"
    GAUSS = "gauss"
    GGAUSS = "Ggauss"
    GT = "GT"
    KGAUSS = "kgauss"
    K_T = "kT"
    MGAUSS = "mgauss"
    MGAUSS_1 = "Mgauss"
    M_T = "mT"
    NGAUSS = "ngauss"
    N_T = "nT"
    PGAUSS = "pgauss"
    P_T = "pT"
    T = "T"
    TGAUSS = "Tgauss"
    TT = "TT"
    UGAUSS = "ugauss"
    U_T = "uT"


class MagneticFluxUom(Enum):
    """
    :cvar C_WB: centiweber
    :cvar D_WB: deciweber
    :cvar EWB: exaweber
    :cvar F_WB: femtoweber
    :cvar GWB: gigaweber
    :cvar K_WB: kiloweber
    :cvar MWB: megaweber
    :cvar M_WB_1: milliweber
    :cvar N_WB: nanoweber
    :cvar P_WB: picoweber
    :cvar TWB: teraweber
    :cvar U_WB: microweber
    :cvar WB: weber
    """

    C_WB = "cWb"
    D_WB = "dWb"
    EWB = "EWb"
    F_WB = "fWb"
    GWB = "GWb"
    K_WB = "kWb"
    MWB = "MWb"
    M_WB_1 = "mWb"
    N_WB = "nWb"
    P_WB = "pWb"
    TWB = "TWb"
    U_WB = "uWb"
    WB = "Wb"


class MagneticPermeabilityUom(Enum):
    """
    :cvar H_M: henry per metre
    :cvar U_H_M: microhenry per metre
    """

    H_M = "H/m"
    U_H_M = "uH/m"


class MagneticVectorPotentialUom(Enum):
    """
    :cvar WB_M: weber per metre
    :cvar WB_MM: weber per millimetre
    """

    WB_M = "Wb/m"
    WB_MM = "Wb/mm"


class MassLengthUom(Enum):
    """
    :cvar KG_M: kilogram metre
    :cvar LBM_FT: pound-mass foot
    """

    KG_M = "kg.m"
    LBM_FT = "lbm.ft"


class MassPerAreaUom(Enum):
    """
    :cvar VALUE_0_01_LBM_FT2: pound-mass per hundred square foot
    :cvar KG_M2: kilogram per square metre
    :cvar LBM_FT2: pound-mass per square foot
    :cvar MG_M2: megagram per square metre
    :cvar TON_US_FT2: US ton-mass per square foot
    """

    VALUE_0_01_LBM_FT2 = "0.01 lbm/ft2"
    KG_M2 = "kg/m2"
    LBM_FT2 = "lbm/ft2"
    MG_M2 = "Mg/m2"
    TON_US_FT2 = "ton[US]/ft2"


class MassPerEnergyUom(Enum):
    """
    :cvar KG_K_W_H: kilogram per kilowatt hour
    :cvar KG_J: kilogram per joule
    :cvar KG_MJ: kilogram per megajoule
    :cvar LBM_HP_H: pound-mass per horsepower hour
    :cvar MG_J: milligram per joule
    """

    KG_K_W_H = "kg/(kW.h)"
    KG_J = "kg/J"
    KG_MJ = "kg/MJ"
    LBM_HP_H = "lbm/(hp.h)"
    MG_J = "mg/J"


class MassPerLengthUom(Enum):
    """
    :cvar KG_M_CM2: kilogram metre per square centimetre
    :cvar KG_M: kilogram per metre
    :cvar KLBM_IN: thousand pound-mass per inch
    :cvar LBM_FT: pound-mass per foot
    :cvar MG_IN: megagram per inch
    """

    KG_M_CM2 = "kg.m/cm2"
    KG_M = "kg/m"
    KLBM_IN = "klbm/in"
    LBM_FT = "lbm/ft"
    MG_IN = "Mg/in"


class MassPerMassUom(Enum):
    """
    :cvar VALUE: percent
    :cvar MASS: percent [mass basis]
    :cvar EUC: euclid
    :cvar G_KG: gram per kilogram
    :cvar G_T: gram per tonne
    :cvar KG_KG: kilogram per kilogram
    :cvar KG_SACK_94LBM: kilogram per 94-pound-sack
    :cvar KG_T: kilogram per tonne
    :cvar MG_G: milligram per gram
    :cvar MG_KG: milligram per kilogram
    :cvar NG_G: nanogram per gram
    :cvar NG_MG: nanogram per milligram
    :cvar PPK: part per thousand
    :cvar PPM: part per million
    :cvar PPM_MASS: part per million [mass basis]
    :cvar UG_G: microgram per gram
    :cvar UG_MG: microgram per milligram
    """

    VALUE = "%"
    MASS = "%[mass]"
    EUC = "Euc"
    G_KG = "g/kg"
    G_T = "g/t"
    KG_KG = "kg/kg"
    KG_SACK_94LBM = "kg/sack[94lbm]"
    KG_T = "kg/t"
    MG_G = "mg/g"
    MG_KG = "mg/kg"
    NG_G = "ng/g"
    NG_MG = "ng/mg"
    PPK = "ppk"
    PPM = "ppm"
    PPM_MASS = "ppm[mass]"
    UG_G = "ug/g"
    UG_MG = "ug/mg"


class MassPerTimePerAreaUom(Enum):
    """
    :cvar G_FT_CM3_S: gram foot per cubic centimetre second
    :cvar G_M_CM3_S: gram metre per cubic centimetre second
    :cvar KG_M2_S: kilogram per square metre second
    :cvar K_PA_S_M: kilopascal second per metre
    :cvar LBM_FT2_H: pound-mass per square foot hour
    :cvar LBM_FT2_S: pound-mass per square foot second
    :cvar MPA_S_M: megapascal second per metre
    """

    G_FT_CM3_S = "g.ft/(cm3.s)"
    G_M_CM3_S = "g.m/(cm3.s)"
    KG_M2_S = "kg/(m2.s)"
    K_PA_S_M = "kPa.s/m"
    LBM_FT2_H = "lbm/(ft2.h)"
    LBM_FT2_S = "lbm/(ft2.s)"
    MPA_S_M = "MPa.s/m"


class MassPerTimePerLengthUom(Enum):
    """
    :cvar KG_M_S: kilogram per metre second
    :cvar LBM_FT_H: pound-mass per hour foot
    :cvar LBM_FT_S: pound-mass per second foot
    :cvar PA_S: pascal second
    """

    KG_M_S = "kg/(m.s)"
    LBM_FT_H = "lbm/(ft.h)"
    LBM_FT_S = "lbm/(ft.s)"
    PA_S = "Pa.s"


class MassPerTimeUom(Enum):
    """
    :cvar VALUE_1_E6_LBM_A: million pound-mass per julian-year
    :cvar G_S: gram per second
    :cvar KG_D: kilogram per day
    :cvar KG_H: kilogram per hour
    :cvar KG_MIN: kilogram per min
    :cvar KG_S: kilogram per second
    :cvar LBM_D: pound-mass per day
    :cvar LBM_H: pound-mass per hour
    :cvar LBM_MIN: pound-mass per minute
    :cvar LBM_S: pound-mass per second
    :cvar MG_A: megagram per julian-year
    :cvar MG_D: megagram per day
    :cvar MG_H: megagram per hour
    :cvar MG_MIN: megagram per minute
    :cvar T_A: tonne per julian-year
    :cvar T_D: tonne per day
    :cvar T_H: tonne per hour
    :cvar T_MIN: tonne per minute
    :cvar TON_UK_A: UK ton-mass per julian-year
    :cvar TON_UK_D: UK ton-mass per day
    :cvar TON_UK_H: UK ton-mass per hour
    :cvar TON_UK_MIN: UK ton-mass per minute
    :cvar TON_US_A: US ton-mass per julian-year
    :cvar TON_US_D: US ton-mass per day
    :cvar TON_US_H: US ton-mass per hour
    :cvar TON_US_MIN: US ton-mass per minute
    """

    VALUE_1_E6_LBM_A = "1E6 lbm/a"
    G_S = "g/s"
    KG_D = "kg/d"
    KG_H = "kg/h"
    KG_MIN = "kg/min"
    KG_S = "kg/s"
    LBM_D = "lbm/d"
    LBM_H = "lbm/h"
    LBM_MIN = "lbm/min"
    LBM_S = "lbm/s"
    MG_A = "Mg/a"
    MG_D = "Mg/d"
    MG_H = "Mg/h"
    MG_MIN = "Mg/min"
    T_A = "t/a"
    T_D = "t/d"
    T_H = "t/h"
    T_MIN = "t/min"
    TON_UK_A = "ton[UK]/a"
    TON_UK_D = "ton[UK]/d"
    TON_UK_H = "ton[UK]/h"
    TON_UK_MIN = "ton[UK]/min"
    TON_US_A = "ton[US]/a"
    TON_US_D = "ton[US]/d"
    TON_US_H = "ton[US]/h"
    TON_US_MIN = "ton[US]/min"


class MassPerVolumePerLengthUom(Enum):
    """
    :cvar G_CM4: gram per centimetre to the fourth power
    :cvar KG_DM4: kilogram per decimetre to the fourth power
    :cvar KG_M4: kilogram per metre to the fourth power
    :cvar LBM_GAL_UK_FT: pound-mass per UK gallon foot
    :cvar LBM_GAL_US_FT: pound-mass per US gallon foot
    :cvar LBM_FT4: pound-mass per foot to the fourth power
    :cvar PA_S2_M3: pascal second squared per cubic metre
    """

    G_CM4 = "g/cm4"
    KG_DM4 = "kg/dm4"
    KG_M4 = "kg/m4"
    LBM_GAL_UK_FT = "lbm/(gal[UK].ft)"
    LBM_GAL_US_FT = "lbm/(gal[US].ft)"
    LBM_FT4 = "lbm/ft4"
    PA_S2_M3 = "Pa.s2/m3"


class MassPerVolumeUom(Enum):
    """
    :cvar VALUE_0_001_LBM_BBL: pound-mass per thousand barrel
    :cvar VALUE_0_001_LBM_GAL_UK: pound-mass per thousand UK gallon
    :cvar VALUE_0_001_LBM_GAL_US: pound-mass per thousand US gallon
    :cvar VALUE_0_01_GRAIN_FT3: grain per hundred cubic foot
    :cvar VALUE_0_1_LBM_BBL: pound-mass per ten barrel
    :cvar VALUE_10_MG_M3: ten thousand kilogram per cubic metre
    :cvar G_CM3: gram per cubic centimetre
    :cvar G_DM3: gram per cubic decimetre
    :cvar G_GAL_UK: gram per UK gallon
    :cvar G_GAL_US: gram per US gallon
    :cvar G_L: gram per litre
    :cvar G_M3: gram per cubic metre
    :cvar GRAIN_FT3: grain per cubic foot
    :cvar GRAIN_GAL_US: grain per US gallon
    :cvar KG_DM3: kilogram per cubic decimetre
    :cvar KG_L: kilogram per litre
    :cvar KG_M3: kilogram per cubic metre
    :cvar LBM_BBL: pound-mass per barrel
    :cvar LBM_FT3: pound-mass per cubic foot
    :cvar LBM_GAL_UK: pound-mass per UK gallon
    :cvar LBM_GAL_US: pound-mass per US gallon
    :cvar LBM_IN3: pound-mass per cubic inch
    :cvar MG_DM3: milligram per cubic decimetre
    :cvar MG_GAL_US: milligram per US gallon
    :cvar MG_L: milligram per litre
    :cvar MG_M3: milligram per cubic metre
    :cvar MG_M3_1: megagram per cubic metre
    :cvar T_M3: tonne per cubic metre
    :cvar UG_CM3: microgram per cubic centimetre
    """

    VALUE_0_001_LBM_BBL = "0.001 lbm/bbl"
    VALUE_0_001_LBM_GAL_UK = "0.001 lbm/gal[UK]"
    VALUE_0_001_LBM_GAL_US = "0.001 lbm/gal[US]"
    VALUE_0_01_GRAIN_FT3 = "0.01 grain/ft3"
    VALUE_0_1_LBM_BBL = "0.1 lbm/bbl"
    VALUE_10_MG_M3 = "10 Mg/m3"
    G_CM3 = "g/cm3"
    G_DM3 = "g/dm3"
    G_GAL_UK = "g/gal[UK]"
    G_GAL_US = "g/gal[US]"
    G_L = "g/L"
    G_M3 = "g/m3"
    GRAIN_FT3 = "grain/ft3"
    GRAIN_GAL_US = "grain/gal[US]"
    KG_DM3 = "kg/dm3"
    KG_L = "kg/L"
    KG_M3 = "kg/m3"
    LBM_BBL = "lbm/bbl"
    LBM_FT3 = "lbm/ft3"
    LBM_GAL_UK = "lbm/gal[UK]"
    LBM_GAL_US = "lbm/gal[US]"
    LBM_IN3 = "lbm/in3"
    MG_DM3 = "mg/dm3"
    MG_GAL_US = "mg/gal[US]"
    MG_L = "mg/L"
    MG_M3 = "mg/m3"
    MG_M3_1 = "Mg/m3"
    T_M3 = "t/m3"
    UG_CM3 = "ug/cm3"


class MassUom(Enum):
    """
    :cvar AG: attogram
    :cvar CG: centigram
    :cvar CT: carat
    :cvar CWT_UK: UK hundredweight
    :cvar CWT_US: US hundredweight
    :cvar EG: exagram
    :cvar FG: femtogram
    :cvar G: gram
    :cvar GG: gigagram
    :cvar GRAIN: grain
    :cvar HG: hectogram
    :cvar KG: kilogram
    :cvar KLBM: thousand pound-mass
    :cvar LBM: pound-mass
    :cvar MG: milligram
    :cvar MG_1: megagram
    :cvar NG: nanogram
    :cvar OZM: ounce-mass
    :cvar OZM_TROY: troy ounce-mass
    :cvar PG: picogram
    :cvar SACK_94LBM: 94 pound-mass sack
    :cvar T: tonne
    :cvar TG: teragram
    :cvar TON_UK: UK ton-mass
    :cvar TON_US: US ton-mass
    :cvar UG: microgram
    """

    AG = "ag"
    CG = "cg"
    CT = "ct"
    CWT_UK = "cwt[UK]"
    CWT_US = "cwt[US]"
    EG = "Eg"
    FG = "fg"
    G = "g"
    GG = "Gg"
    GRAIN = "grain"
    HG = "hg"
    KG = "kg"
    KLBM = "klbm"
    LBM = "lbm"
    MG = "mg"
    MG_1 = "Mg"
    NG = "ng"
    OZM = "ozm"
    OZM_TROY = "ozm[troy]"
    PG = "pg"
    SACK_94LBM = "sack[94lbm]"
    T = "t"
    TG = "Tg"
    TON_UK = "ton[UK]"
    TON_US = "ton[US]"
    UG = "ug"


class MobilityUom(Enum):
    """
    :cvar D_PA_S: darcy per pascal second
    :cvar D_C_P: darcy per centipoise
    :cvar M_D_FT2_LBF_S: millidarcy square foot per pound-force second
    :cvar M_D_IN2_LBF_S: millidarcy square inch per pound-force second
    :cvar M_D_PA_S: millidarcy per pascal second
    :cvar M_D_C_P: millidarcy per centipoise
    :cvar TD_API_PA_S: teradarcy-API per pascal second
    """

    D_PA_S = "D/(Pa.s)"
    D_C_P = "D/cP"
    M_D_FT2_LBF_S = "mD.ft2/(lbf.s)"
    M_D_IN2_LBF_S = "mD.in2/(lbf.s)"
    M_D_PA_S = "mD/(Pa.s)"
    M_D_C_P = "mD/cP"
    TD_API_PA_S = "TD[API]/(Pa.s)"


class MolarEnergyUom(Enum):
    """
    :cvar BTU_IT_LBMOL: BTU per pound-mass-mole
    :cvar J_MOL: joule per gram-mole
    :cvar KCAL_TH_MOL: thousand calorie per gram-mole
    :cvar K_J_KMOL: kilojoule per kilogram-mole
    :cvar MJ_KMOL: megajoule per kilogram-mole
    """

    BTU_IT_LBMOL = "Btu[IT]/lbmol"
    J_MOL = "J/mol"
    KCAL_TH_MOL = "kcal[th]/mol"
    K_J_KMOL = "kJ/kmol"
    MJ_KMOL = "MJ/kmol"


class MolarHeatCapacityUom(Enum):
    """
    :cvar BTU_IT_LBMOL_DELTA_F: BTU per pound-mass-mole delta Fahrenheit
    :cvar CAL_TH_MOL_DELTA_C: calorie per gram-mole delta Celsius
    :cvar J_MOL_DELTA_K: joule per gram-mole delta kelvin
    :cvar K_J_KMOL_DELTA_K: kilojoule per kilogram-mole delta kelvin
    """

    BTU_IT_LBMOL_DELTA_F = "Btu[IT]/(lbmol.deltaF)"
    CAL_TH_MOL_DELTA_C = "cal[th]/(mol.deltaC)"
    J_MOL_DELTA_K = "J/(mol.deltaK)"
    K_J_KMOL_DELTA_K = "kJ/(kmol.deltaK)"


class MolarVolumeUom(Enum):
    """
    :cvar DM3_KMOL: cubic decimetre per kilogram-mole
    :cvar FT3_LBMOL: cubic foot per pound-mass-mole
    :cvar L_KMOL: litre per kilogram-mole
    :cvar L_MOL: litre per gram-mole
    :cvar M3_KMOL: cubic metre per kilogram-mole
    :cvar M3_MOL: cubic metre per gram-mole
    """

    DM3_KMOL = "dm3/kmol"
    FT3_LBMOL = "ft3/lbmol"
    L_KMOL = "L/kmol"
    L_MOL = "L/mol"
    M3_KMOL = "m3/kmol"
    M3_MOL = "m3/mol"


class MolecularWeightUom(Enum):
    """
    :cvar G_MOL: gram per mole
    :cvar KG_MOL: kilogram per mole
    :cvar LBM_LBMOL: pound-mass per pound-mole
    """

    G_MOL = "g/mol"
    KG_MOL = "kg/mol"
    LBM_LBMOL = "lbm/lbmol"


class MomentOfForceUom(Enum):
    """
    :cvar VALUE_1000_LBF_FT: thousand foot pound-force
    :cvar DA_N_M: dekanewton metre
    :cvar D_N_M: decinewton metre
    :cvar J: joule
    :cvar KGF_M: thousand gram-force metre
    :cvar K_N_M: kilonewton metre
    :cvar LBF_FT: foot pound-force
    :cvar LBF_IN: inch pound-force
    :cvar LBM_FT2_S2: pound-mass square foot per second squared
    :cvar N_M: newton metre
    :cvar PDL_FT: foot poundal
    :cvar TONF_US_FT: US ton-force foot
    :cvar TONF_US_MI: US ton-force mile
    """

    VALUE_1000_LBF_FT = "1000 lbf.ft"
    DA_N_M = "daN.m"
    D_N_M = "dN.m"
    J = "J"
    KGF_M = "kgf.m"
    K_N_M = "kN.m"
    LBF_FT = "lbf.ft"
    LBF_IN = "lbf.in"
    LBM_FT2_S2 = "lbm.ft2/s2"
    N_M = "N.m"
    PDL_FT = "pdl.ft"
    TONF_US_FT = "tonf[US].ft"
    TONF_US_MI = "tonf[US].mi"


class MomentOfInertiaUom(Enum):
    """
    :cvar KG_M2: kilogram square metre
    :cvar LBM_FT2: pound-mass square foot
    """

    KG_M2 = "kg.m2"
    LBM_FT2 = "lbm.ft2"


class MomentumUom(Enum):
    """
    :cvar KG_M_S: kilogram metre per second
    :cvar LBM_FT_S: foot pound-mass per second
    """

    KG_M_S = "kg.m/s"
    LBM_FT_S = "lbm.ft/s"


class NormalizedPowerUom(Enum):
    """
    :cvar B_W: bel watt
    :cvar D_B_MW: decibel megawatt
    :cvar D_B_M_W_1: decibel milliwatt
    :cvar D_B_W: decibel watt
    """

    B_W = "B.W"
    D_B_MW = "dB.MW"
    D_B_M_W_1 = "dB.mW"
    D_B_W = "dB.W"


@dataclass
class ObjectAlias:
    identifier: Optional[str] = field(
        default=None,
        metadata={
            "name": "Identifier",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/commonv2",
            "required": True,
        },
    )
    description: Optional[str] = field(
        default=None,
        metadata={
            "name": "Description",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/commonv2",
            "min_length": 1,
            "max_length": 256,
            "white_space": "collapse",
        },
    )
    authority: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "min_length": 1,
            "max_length": 64,
            "white_space": "collapse",
        },
    )


class PermeabilityLengthUom(Enum):
    """
    :cvar D_FT: darcy foot
    :cvar D_M: darcy metre
    :cvar M_D_FT: millidarcy foot
    :cvar M_D_M: millidarcy metre
    :cvar TD_API_M: teradarcy-API metre
    """

    D_FT = "D.ft"
    D_M = "D.m"
    M_D_FT = "mD.ft"
    M_D_M = "mD.m"
    TD_API_M = "TD[API].m"


class PermeabilityRockUom(Enum):
    """
    :cvar D: darcy
    :cvar D_API: darcy-API
    :cvar M_D: millidarcy
    :cvar TD_API: teradarcy-API
    """

    D = "D"
    D_API = "D[API]"
    M_D = "mD"
    TD_API = "TD[API]"


class PermittivityUom(Enum):
    """
    :cvar F_M: farad per metre
    :cvar U_F_M: microfarad per metre
    """

    F_M = "F/m"
    U_F_M = "uF/m"


class PlaneAngleUom(Enum):
    """
    :cvar VALUE_0_001_SECA: angular millisecond
    :cvar CCGR: centesimal-second
    :cvar CGR: centesimal-minute
    :cvar DEGA: angular degree
    :cvar GON: gon
    :cvar KRAD: kiloradian
    :cvar MILA: angular mil
    :cvar MINA: angular minute
    :cvar MRAD: megaradian
    :cvar MRAD_1: milliradian
    :cvar RAD: radian
    :cvar REV: revolution
    :cvar SECA: angular second
    :cvar URAD: microradian
    """

    VALUE_0_001_SECA = "0.001 seca"
    CCGR = "ccgr"
    CGR = "cgr"
    DEGA = "dega"
    GON = "gon"
    KRAD = "krad"
    MILA = "mila"
    MINA = "mina"
    MRAD = "Mrad"
    MRAD_1 = "mrad"
    RAD = "rad"
    REV = "rev"
    SECA = "seca"
    URAD = "urad"


class PotentialDifferencePerPowerDropUom(Enum):
    """
    :cvar V_B: volt per bel
    :cvar V_D_B: volt per decibel
    """

    V_B = "V/B"
    V_D_B = "V/dB"


class PowerPerAreaUom(Enum):
    """
    :cvar BTU_IT_H_FT2: (BTU per hour) per square foot
    :cvar BTU_IT_S_FT2: BTU per second square foot
    :cvar CAL_TH_H_CM2: calorie per hour square centimetre
    :cvar HP_IN2: horsepower per square inch
    :cvar HP_HYD_IN2: hydraulic-horsepower per square inch
    :cvar K_W_CM2: kilowatt per square centimetre
    :cvar K_W_M2: kilowatt per square metre
    :cvar M_W_M2: milliwatt per square metre
    :cvar UCAL_TH_S_CM2: millionth of calorie per second square
        centimetre
    :cvar W_CM2: watt per square centimetre
    :cvar W_M2: watt per square metre
    :cvar W_MM2: watt per square millimetre
    """

    BTU_IT_H_FT2 = "Btu[IT]/(h.ft2)"
    BTU_IT_S_FT2 = "Btu[IT]/(s.ft2)"
    CAL_TH_H_CM2 = "cal[th]/(h.cm2)"
    HP_IN2 = "hp/in2"
    HP_HYD_IN2 = "hp[hyd]/in2"
    K_W_CM2 = "kW/cm2"
    K_W_M2 = "kW/m2"
    M_W_M2 = "mW/m2"
    UCAL_TH_S_CM2 = "ucal[th]/(s.cm2)"
    W_CM2 = "W/cm2"
    W_M2 = "W/m2"
    W_MM2 = "W/mm2"


class PowerPerPowerUom(Enum):
    """
    :cvar VALUE: percent
    :cvar BTU_IT_HP_H: BTU per horsepower hour
    :cvar EUC: euclid
    :cvar W_K_W: watt per kilowatt
    :cvar W_W: watt per watt
    """

    VALUE = "%"
    BTU_IT_HP_H = "Btu[IT]/(hp.h)"
    EUC = "Euc"
    W_K_W = "W/kW"
    W_W = "W/W"


class PowerPerVolumeUom(Enum):
    """
    :cvar BTU_IT_H_FT3: BTU per hour cubic foot
    :cvar BTU_IT_S_FT3: (BTU per second) per cubic foot
    :cvar CAL_TH_H_CM3: calorie per hour cubic centimetre
    :cvar CAL_TH_S_CM3: calorie per second cubic centimetre
    :cvar HP_FT3: horsepower per cubic foot
    :cvar K_W_M3: kilowatt per cubic metre
    :cvar U_W_M3: microwatt per cubic metre
    :cvar W_M3: watt per cubic metre
    """

    BTU_IT_H_FT3 = "Btu[IT]/(h.ft3)"
    BTU_IT_S_FT3 = "Btu[IT]/(s.ft3)"
    CAL_TH_H_CM3 = "cal[th]/(h.cm3)"
    CAL_TH_S_CM3 = "cal[th]/(s.cm3)"
    HP_FT3 = "hp/ft3"
    K_W_M3 = "kW/m3"
    U_W_M3 = "uW/m3"
    W_M3 = "W/m3"


class PowerUom(Enum):
    """
    :cvar C_W: centiwatt
    :cvar D_W: deciwatt
    :cvar EW: exawatt
    :cvar F_W: femtowatt
    :cvar GW: gigawatt
    :cvar HP: horsepower
    :cvar HP_ELEC: electric-horsepower
    :cvar HP_HYD: hydraulic-horsepower
    :cvar HP_METRIC: metric-horsepower
    :cvar K_W: kilowatt
    :cvar MW: megawatt
    :cvar M_W_1: milliwatt
    :cvar N_W: nanowatt
    :cvar P_W: picowatt
    :cvar TON_REFRIG: ton-refrigeration
    :cvar TW: terawatt
    :cvar U_W: microwatt
    :cvar W: watt
    """

    C_W = "cW"
    D_W = "dW"
    EW = "EW"
    F_W = "fW"
    GW = "GW"
    HP = "hp"
    HP_ELEC = "hp[elec]"
    HP_HYD = "hp[hyd]"
    HP_METRIC = "hp[metric]"
    K_W = "kW"
    MW = "MW"
    M_W_1 = "mW"
    N_W = "nW"
    P_W = "pW"
    TON_REFRIG = "tonRefrig"
    TW = "TW"
    U_W = "uW"
    W = "W"


class PressurePerTimeUom(Enum):
    """
    :cvar ATM_H: standard atmosphere per hour
    :cvar BAR_H: bar per hour
    :cvar K_PA_H: kilopascal per hour
    :cvar K_PA_MIN: kilopascal per min
    :cvar MPA_H: megapascal per hour
    :cvar PA_H: pascal per hour
    :cvar PA_S: pascal per second
    :cvar PSI_H: psi per hour
    :cvar PSI_MIN: psi per minute
    """

    ATM_H = "atm/h"
    BAR_H = "bar/h"
    K_PA_H = "kPa/h"
    K_PA_MIN = "kPa/min"
    MPA_H = "MPa/h"
    PA_H = "Pa/h"
    PA_S = "Pa/s"
    PSI_H = "psi/h"
    PSI_MIN = "psi/min"


class PressurePerVolumeUom(Enum):
    """
    :cvar PA_M3: pascal per cubic metre
    :cvar PSI2_D_C_P_FT3: psi squared day per centipoise cubic foot
    """

    PA_M3 = "Pa/m3"
    PSI2_D_C_P_FT3 = "psi2.d/(cP.ft3)"


class PressureSquaredPerForceTimePerAreaUom(Enum):
    """
    :cvar VALUE_0_001_K_PA2_C_P: kilopascal squared per thousand
        centipoise
    :cvar BAR2_C_P: bar squared per centipoise
    :cvar K_PA2_C_P: kilopascal squared per centipoise
    :cvar PA2_PA_S: pascal squared per pascal second
    :cvar PSI2_C_P: psi squared per centipoise
    """

    VALUE_0_001_K_PA2_C_P = "0.001 kPa2/cP"
    BAR2_C_P = "bar2/cP"
    K_PA2_C_P = "kPa2/cP"
    PA2_PA_S = "Pa2/(Pa.s)"
    PSI2_C_P = "psi2/cP"


class PressureSquaredUom(Enum):
    """
    :cvar BAR2: bar squared
    :cvar GPA2: gigapascal squared
    :cvar K_PA2: kilopascal squared
    :cvar KPSI2: (thousand psi) squared
    :cvar PA2: pascal squared
    :cvar PSI2: psi squared
    """

    BAR2 = "bar2"
    GPA2 = "GPa2"
    K_PA2 = "kPa2"
    KPSI2 = "kpsi2"
    PA2 = "Pa2"
    PSI2 = "psi2"


class PressureTimePerVolumeUom(Enum):
    """
    :cvar PA_S_M3: pascal second per cubic metre
    :cvar PSI_D_BBL: psi day per barrel
    """

    PA_S_M3 = "Pa.s/m3"
    PSI_D_BBL = "psi.d/bbl"


class PressureUom(Enum):
    """
    :cvar VALUE_0_01_LBF_FT2: pound-force per hundred square foot
    :cvar AT: technical atmosphere
    :cvar ATM: standard atmosphere
    :cvar BAR: bar
    :cvar CM_H2_O_4DEG_C: centimetre of water at 4 degree Celsius
    :cvar C_PA: centipascal
    :cvar D_PA: decipascal
    :cvar DYNE_CM2: dyne per square centimetre
    :cvar EPA: exapascal
    :cvar F_PA: femtopascal
    :cvar GPA: gigapascal
    :cvar HBAR: hundred bar
    :cvar IN_H2_O_39DEG_F: inch of water at 39.2 degree Fahrenheit
    :cvar IN_H2_O_60DEG_F: inch of water at 60 degree Fahrenheit
    :cvar IN_HG_32DEG_F: inch of mercury at 32 degree Fahrenheit
    :cvar IN_HG_60DEG_F: inch of mercury at 60 degree Fahrenheit
    :cvar KGF_CM2: thousand gram-force per square centimetre
    :cvar KGF_M2: thousand gram-force per square metre
    :cvar KGF_MM2: thousand gram-force per square millimetre
    :cvar K_N_M2: kilonewton per square metre
    :cvar K_PA: kilopascal
    :cvar KPSI: thousand psi
    :cvar LBF_FT2: pound-force per square foot
    :cvar MBAR: thousandth of bar
    :cvar MM_HG_0DEG_C: millimetres of Mercury at 0 deg C
    :cvar M_PA: millipascal
    :cvar MPA_1: megapascal
    :cvar MPSI: million psi
    :cvar N_M2: newton per square metre
    :cvar N_MM2: newton per square millimetre
    :cvar N_PA: nanopascal
    :cvar PA: pascal
    :cvar P_PA: picopascal
    :cvar PSI: pound-force per square inch
    :cvar TONF_UK_FT2: UK ton-force per square foot
    :cvar TONF_US_FT2: US ton-force per square foot
    :cvar TONF_US_IN2: US ton-force per square inch
    :cvar TORR: torr
    :cvar TPA: terapascal
    :cvar UBAR: millionth of bar
    :cvar UM_HG_0DEG_C: micrometre of mercury at 0 degree Celsius
    :cvar U_PA: micropascal
    :cvar UPSI: millionth of psi
    """

    VALUE_0_01_LBF_FT2 = "0.01 lbf/ft2"
    AT = "at"
    ATM = "atm"
    BAR = "bar"
    CM_H2_O_4DEG_C = "cmH2O[4degC]"
    C_PA = "cPa"
    D_PA = "dPa"
    DYNE_CM2 = "dyne/cm2"
    EPA = "EPa"
    F_PA = "fPa"
    GPA = "GPa"
    HBAR = "hbar"
    IN_H2_O_39DEG_F = "inH2O[39degF]"
    IN_H2_O_60DEG_F = "inH2O[60degF]"
    IN_HG_32DEG_F = "inHg[32degF]"
    IN_HG_60DEG_F = "inHg[60degF]"
    KGF_CM2 = "kgf/cm2"
    KGF_M2 = "kgf/m2"
    KGF_MM2 = "kgf/mm2"
    K_N_M2 = "kN/m2"
    K_PA = "kPa"
    KPSI = "kpsi"
    LBF_FT2 = "lbf/ft2"
    MBAR = "mbar"
    MM_HG_0DEG_C = "mmHg[0degC]"
    M_PA = "mPa"
    MPA_1 = "MPa"
    MPSI = "Mpsi"
    N_M2 = "N/m2"
    N_MM2 = "N/mm2"
    N_PA = "nPa"
    PA = "Pa"
    P_PA = "pPa"
    PSI = "psi"
    TONF_UK_FT2 = "tonf[UK]/ft2"
    TONF_US_FT2 = "tonf[US]/ft2"
    TONF_US_IN2 = "tonf[US]/in2"
    TORR = "torr"
    TPA = "TPa"
    UBAR = "ubar"
    UM_HG_0DEG_C = "umHg[0degC]"
    U_PA = "uPa"
    UPSI = "upsi"


class QuantityOfLightUom(Enum):
    """
    :cvar LM_S: lumen second
    """

    LM_S = "lm.s"


class RadianceUom(Enum):
    """
    :cvar W_M2_SR: watt per square metre steradian
    """

    W_M2_SR = "W/(m2.sr)"


class RadiantIntensityUom(Enum):
    """
    :cvar W_SR: watt per steradian
    """

    W_SR = "W/sr"


class ReciprocalAreaUom(Enum):
    """
    :cvar VALUE_1_FT2: per square foot
    :cvar VALUE_1_KM2: per square kilometre
    :cvar VALUE_1_M2: per square metre
    :cvar VALUE_1_MI2: per square mile
    """

    VALUE_1_FT2 = "1/ft2"
    VALUE_1_KM2 = "1/km2"
    VALUE_1_M2 = "1/m2"
    VALUE_1_MI2 = "1/mi2"


class ReciprocalElectricPotentialDifferenceUom(Enum):
    """
    :cvar VALUE_1_U_V: per microvolt
    :cvar VALUE_1_V: per volt
    """

    VALUE_1_U_V = "1/uV"
    VALUE_1_V = "1/V"


class ReciprocalForceUom(Enum):
    """
    :cvar VALUE_1_LBF: per pound-force
    :cvar VALUE_1_N: per Newton
    """

    VALUE_1_LBF = "1/lbf"
    VALUE_1_N = "1/N"


class ReciprocalLengthUom(Enum):
    """
    :cvar VALUE_1_ANGSTROM: per angstrom
    :cvar VALUE_1_CM: per centimetre
    :cvar VALUE_1_FT: per foot
    :cvar VALUE_1_IN: per inch
    :cvar VALUE_1_M: per metre
    :cvar VALUE_1_MI: per mile
    :cvar VALUE_1_MM: per millimetre
    :cvar VALUE_1_NM: per nanometre
    :cvar VALUE_1_YD: per yard
    :cvar VALUE_1_E_9_1_FT: per thousand million foot
    """

    VALUE_1_ANGSTROM = "1/angstrom"
    VALUE_1_CM = "1/cm"
    VALUE_1_FT = "1/ft"
    VALUE_1_IN = "1/in"
    VALUE_1_M = "1/m"
    VALUE_1_MI = "1/mi"
    VALUE_1_MM = "1/mm"
    VALUE_1_NM = "1/nm"
    VALUE_1_YD = "1/yd"
    VALUE_1_E_9_1_FT = "1E-9 1/ft"


class ReciprocalMassTimeUom(Enum):
    """
    :cvar VALUE_1_KG_S: per (kilogram per second)
    :cvar BQ_KG: becquerel per kilogram
    :cvar P_CI_G: picocurie per gram
    """

    VALUE_1_KG_S = "1/(kg.s)"
    BQ_KG = "Bq/kg"
    P_CI_G = "pCi/g"


class ReciprocalMassUom(Enum):
    """
    :cvar VALUE_1_G: per gram
    :cvar VALUE_1_KG: per kilogram
    :cvar VALUE_1_LBM: per pound
    """

    VALUE_1_G = "1/g"
    VALUE_1_KG = "1/kg"
    VALUE_1_LBM = "1/lbm"


class ReciprocalPressureUom(Enum):
    """
    :cvar VALUE_1_BAR: per bar
    :cvar VALUE_1_K_PA: per kilopascal
    :cvar VALUE_1_PA: per pascal
    :cvar VALUE_1_P_PA: per picopascal
    :cvar VALUE_1_PSI: per psi
    :cvar VALUE_1_UPSI: per millionth of psi
    """

    VALUE_1_BAR = "1/bar"
    VALUE_1_K_PA = "1/kPa"
    VALUE_1_PA = "1/Pa"
    VALUE_1_P_PA = "1/pPa"
    VALUE_1_PSI = "1/psi"
    VALUE_1_UPSI = "1/upsi"


class ReciprocalTimeUom(Enum):
    """
    :cvar VALUE_1_A: per julian-year
    :cvar VALUE_1_D: per day
    :cvar VALUE_1_H: per hour
    :cvar VALUE_1_MIN: per minute
    :cvar VALUE_1_MS: per millisecond
    :cvar VALUE_1_S: per second
    :cvar VALUE_1_US: per microsecond
    :cvar VALUE_1_WK: per week
    """

    VALUE_1_A = "1/a"
    VALUE_1_D = "1/d"
    VALUE_1_H = "1/h"
    VALUE_1_MIN = "1/min"
    VALUE_1_MS = "1/ms"
    VALUE_1_S = "1/s"
    VALUE_1_US = "1/us"
    VALUE_1_WK = "1/wk"


class ReciprocalVolumeUom(Enum):
    """
    :cvar VALUE_1_BBL: per barrel
    :cvar VALUE_1_FT3: per cubic foot
    :cvar VALUE_1_GAL_UK: per UK gallon
    :cvar VALUE_1_GAL_US: per US gallon
    :cvar VALUE_1_L: per litre
    :cvar VALUE_1_M3: per cubic metre
    """

    VALUE_1_BBL = "1/bbl"
    VALUE_1_FT3 = "1/ft3"
    VALUE_1_GAL_UK = "1/gal[UK]"
    VALUE_1_GAL_US = "1/gal[US]"
    VALUE_1_L = "1/L"
    VALUE_1_M3 = "1/m3"


class ReluctanceUom(Enum):
    """
    :cvar VALUE_1_H: per henry
    """

    VALUE_1_H = "1/H"


class SecondMomentOfAreaUom(Enum):
    """
    :cvar CM4: centimetre to the fourth power
    :cvar IN4: inch to the fourth power
    :cvar M4: metre to the fourth power
    """

    CM4 = "cm4"
    IN4 = "in4"
    M4 = "m4"


class SignalingEventPerTimeUom(Enum):
    """
    :cvar BD: baud
    """

    BD = "Bd"


class SolidAngleUom(Enum):
    """
    :cvar SR: steradian
    """

    SR = "sr"


class SpecificHeatCapacityUom(Enum):
    """
    :cvar BTU_IT_LBM_DELTA_F: BTU per pound-mass delta Fahrenheit
    :cvar BTU_IT_LBM_DELTA_R: BTU per pound-mass delta Rankine
    :cvar CAL_TH_G_DELTA_K: calorie per gram delta kelvin
    :cvar J_G_DELTA_K: joule per gram delta kelvin
    :cvar J_KG_DELTA_K: joule per kilogram delta kelvin
    :cvar KCAL_TH_KG_DELTA_C: thousand calorie per kilogram delta
        Celsius
    :cvar K_J_KG_DELTA_K: kilojoule per kilogram delta kelvin
    :cvar K_W_H_KG_DELTA_C: kilowatt hour per kilogram delta Celsius
    """

    BTU_IT_LBM_DELTA_F = "Btu[IT]/(lbm.deltaF)"
    BTU_IT_LBM_DELTA_R = "Btu[IT]/(lbm.deltaR)"
    CAL_TH_G_DELTA_K = "cal[th]/(g.deltaK)"
    J_G_DELTA_K = "J/(g.deltaK)"
    J_KG_DELTA_K = "J/(kg.deltaK)"
    KCAL_TH_KG_DELTA_C = "kcal[th]/(kg.deltaC)"
    K_J_KG_DELTA_K = "kJ/(kg.deltaK)"
    K_W_H_KG_DELTA_C = "kW.h/(kg.deltaC)"


class TemperatureIntervalPerLengthUom(Enum):
    """
    :cvar VALUE_0_01_DELTA_F_FT: delta Fahrenheit per hundred foot
    :cvar DELTA_C_FT: delta Celsius per foot
    :cvar DELTA_C_HM: delta Celsius per hectometre
    :cvar DELTA_C_KM: delta Celsius per kilometre
    :cvar DELTA_C_M: delta Celsius per metre
    :cvar DELTA_F_FT: delta Fahrenheit per foot
    :cvar DELTA_F_M: delta Fahrenheit per metre
    :cvar DELTA_K_KM: delta kelvin per kilometre
    :cvar DELTA_K_M: delta kelvin per metre
    """

    VALUE_0_01_DELTA_F_FT = "0.01 deltaF/ft"
    DELTA_C_FT = "deltaC/ft"
    DELTA_C_HM = "deltaC/hm"
    DELTA_C_KM = "deltaC/km"
    DELTA_C_M = "deltaC/m"
    DELTA_F_FT = "deltaF/ft"
    DELTA_F_M = "deltaF/m"
    DELTA_K_KM = "deltaK/km"
    DELTA_K_M = "deltaK/m"


class TemperatureIntervalPerPressureUom(Enum):
    """
    :cvar DELTA_C_K_PA: delta Celsius per kilopascal
    :cvar DELTA_F_PSI: delta Fahrenheit per psi
    :cvar DELTA_K_PA: delta kelvin per Pascal
    """

    DELTA_C_K_PA = "deltaC/kPa"
    DELTA_F_PSI = "deltaF/psi"
    DELTA_K_PA = "deltaK/Pa"


class TemperatureIntervalPerTimeUom(Enum):
    """
    :cvar DELTA_C_H: delta Celsius per hour
    :cvar DELTA_C_MIN: delta Celsius per minute
    :cvar DELTA_C_S: delta Celsius per second
    :cvar DELTA_F_H: delta Fahrenheit per hour
    :cvar DELTA_F_MIN: delta Fahrenheit per minute
    :cvar DELTA_F_S: delta Fahrenheit per second
    :cvar DELTA_K_S: delta kelvin per second
    """

    DELTA_C_H = "deltaC/h"
    DELTA_C_MIN = "deltaC/min"
    DELTA_C_S = "deltaC/s"
    DELTA_F_H = "deltaF/h"
    DELTA_F_MIN = "deltaF/min"
    DELTA_F_S = "deltaF/s"
    DELTA_K_S = "deltaK/s"


class TemperatureIntervalUom(Enum):
    """
    :cvar DELTA_C: delta Celsius
    :cvar DELTA_F: delta Fahrenheit
    :cvar DELTA_K: delta kelvin
    :cvar DELTA_R: delta Rankine
    """

    DELTA_C = "deltaC"
    DELTA_F = "deltaF"
    DELTA_K = "deltaK"
    DELTA_R = "deltaR"


class ThermalConductanceUom(Enum):
    """
    :cvar W_DELTA_K: watt per delta kelvin
    """

    W_DELTA_K = "W/deltaK"


class ThermalConductivityUom(Enum):
    """
    :cvar BTU_IT_H_FT_DELTA_F: BTU per hour foot delta Fahrenheit
    :cvar CAL_TH_H_CM_DELTA_C: calorie per hour centimetre delta Celsius
    :cvar CAL_TH_S_CM_DELTA_C: calorie per second centimetre delta
        Celsius
    :cvar KCAL_TH_H_M_DELTA_C: thousand calorie per hour metre delta
        Celsius
    :cvar W_M_DELTA_K: watt per metre delta kelvin
    """

    BTU_IT_H_FT_DELTA_F = "Btu[IT]/(h.ft.deltaF)"
    CAL_TH_H_CM_DELTA_C = "cal[th]/(h.cm.deltaC)"
    CAL_TH_S_CM_DELTA_C = "cal[th]/(s.cm.deltaC)"
    KCAL_TH_H_M_DELTA_C = "kcal[th]/(h.m.deltaC)"
    W_M_DELTA_K = "W/(m.deltaK)"


class ThermalDiffusivityUom(Enum):
    """
    :cvar CM2_S: square centimetre per second
    :cvar FT2_H: square foot per hour
    :cvar FT2_S: square foot per second
    :cvar IN2_S: square inch per second
    :cvar M2_H: square metre per hour
    :cvar M2_S: square metre per second
    :cvar MM2_S: square millimetre per second
    """

    CM2_S = "cm2/s"
    FT2_H = "ft2/h"
    FT2_S = "ft2/s"
    IN2_S = "in2/s"
    M2_H = "m2/h"
    M2_S = "m2/s"
    MM2_S = "mm2/s"


class ThermalInsulanceUom(Enum):
    """
    :cvar DELTA_C_M2_H_KCAL_TH: delta Celsius square metre hour per
        thousand calory
    :cvar DELTA_F_FT2_H_BTU_IT: delta Fahrenheit square foot hour per
        BTU
    :cvar DELTA_K_M2_K_W: delta kelvin square metre per kilowatt
    :cvar DELTA_K_M2_W: delta kelvin square metre per watt
    """

    DELTA_C_M2_H_KCAL_TH = "deltaC.m2.h/kcal[th]"
    DELTA_F_FT2_H_BTU_IT = "deltaF.ft2.h/Btu[IT]"
    DELTA_K_M2_K_W = "deltaK.m2/kW"
    DELTA_K_M2_W = "deltaK.m2/W"


class ThermalResistanceUom(Enum):
    """
    :cvar DELTA_K_W: delta kelvin per watt
    """

    DELTA_K_W = "deltaK/W"


class ThermodynamicTemperatureUom(Enum):
    """
    :cvar DEG_C: degree Celsius
    :cvar DEG_F: degree Fahrenheit
    :cvar DEG_R: degree Rankine
    :cvar K: degree kelvin
    """

    DEG_C = "degC"
    DEG_F = "degF"
    DEG_R = "degR"
    K = "K"


class TimePerLengthUom(Enum):
    """
    :cvar VALUE_0_001_H_FT: hour per thousand foot
    :cvar H_KM: hour per kilometre
    :cvar MIN_FT: minute per foot
    :cvar MIN_M: minute per metre
    :cvar MS_CM: millisecond per centimetre
    :cvar MS_FT: millisecond per foot
    :cvar MS_IN: millisecond per inch
    :cvar MS_M: millisecond per metre
    :cvar NS_FT: nanosecond per foot
    :cvar NS_M: nanosecond per metre
    :cvar S_CM: second per centimetre
    :cvar S_FT: second per foot
    :cvar S_IN: second per inch
    :cvar S_M: second per metre
    :cvar US_FT: microsecond per foot
    :cvar US_IN: microsecond per inch
    :cvar US_M: microsecond per metre
    """

    VALUE_0_001_H_FT = "0.001 h/ft"
    H_KM = "h/km"
    MIN_FT = "min/ft"
    MIN_M = "min/m"
    MS_CM = "ms/cm"
    MS_FT = "ms/ft"
    MS_IN = "ms/in"
    MS_M = "ms/m"
    NS_FT = "ns/ft"
    NS_M = "ns/m"
    S_CM = "s/cm"
    S_FT = "s/ft"
    S_IN = "s/in"
    S_M = "s/m"
    US_FT = "us/ft"
    US_IN = "us/in"
    US_M = "us/m"


class TimePerMassUom(Enum):
    """
    :cvar S_KG: second per kilogram
    """

    S_KG = "s/kg"


class TimePerTimeUom(Enum):
    """
    :cvar VALUE: percent
    :cvar EUC: euclid
    :cvar MS_S: millisecond per second
    :cvar S_S: second per second
    """

    VALUE = "%"
    EUC = "Euc"
    MS_S = "ms/s"
    S_S = "s/s"


class TimePerVolumeUom(Enum):
    """
    :cvar VALUE_0_001_D_FT3: day per thousand cubic foot
    :cvar D_BBL: day per barrel
    :cvar D_FT3: day per cubic foot
    :cvar D_M3: day per cubic metre
    :cvar H_FT3: hour per cubic foot
    :cvar H_M3: hour per cubic metre
    :cvar S_FT3: second per cubic foot
    :cvar S_L: second per litre
    :cvar S_M3: second per cubic metre
    :cvar S_QT_UK: second per UK quart
    :cvar S_QT_US: second per US quart
    """

    VALUE_0_001_D_FT3 = "0.001 d/ft3"
    D_BBL = "d/bbl"
    D_FT3 = "d/ft3"
    D_M3 = "d/m3"
    H_FT3 = "h/ft3"
    H_M3 = "h/m3"
    S_FT3 = "s/ft3"
    S_L = "s/L"
    S_M3 = "s/m3"
    S_QT_UK = "s/qt[UK]"
    S_QT_US = "s/qt[US]"


class TimeUom(Enum):
    """
    :cvar VALUE_1_2_MS: half of millisecond
    :cvar VALUE_100_KA_T: hundred thousand tropical-year
    :cvar A: julian-year
    :cvar A_T: tropical-year
    :cvar CA: hundredth of julian-year
    :cvar CS: centisecond
    :cvar D: day
    :cvar DS: decisecond
    :cvar EA_T: million million million tropical-year
    :cvar FA: femtojulian-year
    :cvar GA_T: thousand million tropical-year
    :cvar H: hour
    :cvar HS: hectosecond
    :cvar KA_T: thousand tropical-year
    :cvar MA_T: million tropical-year
    :cvar MIN: minute
    :cvar MS: millisecond
    :cvar NA: nanojulian-year
    :cvar NS: nanosecond
    :cvar PS: picosecond
    :cvar S: second
    :cvar TA_T: million million tropical-year
    :cvar US: microsecond
    :cvar WK: week
    """

    VALUE_1_2_MS = "1/2 ms"
    VALUE_100_KA_T = "100 ka[t]"
    A = "a"
    A_T = "a[t]"
    CA = "ca"
    CS = "cs"
    D = "d"
    DS = "ds"
    EA_T = "Ea[t]"
    FA = "fa"
    GA_T = "Ga[t]"
    H = "h"
    HS = "hs"
    KA_T = "ka[t]"
    MA_T = "Ma[t]"
    MIN = "min"
    MS = "ms"
    NA = "na"
    NS = "ns"
    PS = "ps"
    S = "s"
    TA_T = "Ta[t]"
    US = "us"
    WK = "wk"


class VerticalDirection(Enum):
    """
    :cvar UP: Values are positive when moving away from the center of
        the Earth.
    :cvar DOWN: Values are positive when moving toward the center of the
        Earth.
    """

    UP = "up"
    DOWN = "down"


class VolumeFlowRatePerVolumeFlowRateUom(Enum):
    """
    :cvar VALUE: percent
    :cvar BBL_D_BBL_D: (barrel per day) per (barrel per day)
    :cvar M3_D_M3_D: (cubic metre per day) per (cubic metre per day)
    :cvar M3_S_M3_S: (cubic metre per second) per (cubic metre per
        second)
    :cvar VALUE_1_E6_FT3_D_BBL_D: (million cubic foot per day) per
        (barrel per day)
    :cvar EUC: euclid
    """

    VALUE = "%"
    BBL_D_BBL_D = "(bbl/d)/(bbl/d)"
    M3_D_M3_D = "(m3/d)/(m3/d)"
    M3_S_M3_S = "(m3/s)/(m3/s)"
    VALUE_1_E6_FT3_D_BBL_D = "1E6 (ft3/d)/(bbl/d)"
    EUC = "Euc"


class VolumePerAreaUom(Enum):
    """
    :cvar VALUE_1_E6_BBL_ACRE: million barrel per acre
    :cvar BBL_ACRE: barrel per acre
    :cvar FT3_FT2: cubic foot per square foot
    :cvar M3_M2: cubic metre per square metre
    """

    VALUE_1_E6_BBL_ACRE = "1E6 bbl/acre"
    BBL_ACRE = "bbl/acre"
    FT3_FT2 = "ft3/ft2"
    M3_M2 = "m3/m2"


class VolumePerLengthUom(Enum):
    """
    :cvar VALUE_0_01_DM3_KM: cubic decimetre per hundred kilometre
    :cvar VALUE_0_01_L_KM: litre per hundred kilometre
    :cvar BBL_FT: barrel per foot
    :cvar BBL_IN: barrel per inch
    :cvar BBL_MI: barrel per mile
    :cvar DM3_M: cubic decimetre per metre
    :cvar FT3_FT: cubic foot per foot
    :cvar GAL_UK_MI: UK gallon per mile
    :cvar GAL_US_FT: US gallon per foot
    :cvar GAL_US_MI: US gallon per mile
    :cvar IN3_FT: cubic inch per foot
    :cvar L_M: litre per metre
    :cvar M3_KM: cubic metre per kilometre
    :cvar M3_M: cubic metre per metre
    """

    VALUE_0_01_DM3_KM = "0.01 dm3/km"
    VALUE_0_01_L_KM = "0.01 L/km"
    BBL_FT = "bbl/ft"
    BBL_IN = "bbl/in"
    BBL_MI = "bbl/mi"
    DM3_M = "dm3/m"
    FT3_FT = "ft3/ft"
    GAL_UK_MI = "gal[UK]/mi"
    GAL_US_FT = "gal[US]/ft"
    GAL_US_MI = "gal[US]/mi"
    IN3_FT = "in3/ft"
    L_M = "L/m"
    M3_KM = "m3/km"
    M3_M = "m3/m"


class VolumePerMassUom(Enum):
    """
    :cvar VALUE_0_01_L_KG: litre per hundred kilogram
    :cvar BBL_TON_UK: barrel per UK ton-mass
    :cvar BBL_TON_US: barrel per US ton-mass
    :cvar CM3_G: cubic centimetre per gram
    :cvar DM3_KG: cubic decimetre per kilogram
    :cvar DM3_T: cubic decimetre per ton
    :cvar FT3_KG: cubic foot per kilogram
    :cvar FT3_LBM: cubic foot per pound-mass
    :cvar FT3_SACK_94LBM: cubic foot per 94-pound-sack
    :cvar GAL_UK_LBM: UK gallon per pound-mass
    :cvar GAL_US_LBM: US gallon per pound-mass
    :cvar GAL_US_SACK_94LBM: US gallon per 94-pound-sack
    :cvar GAL_US_TON_UK: US gallon per UK ton-mass
    :cvar GAL_US_TON_US: US gallon per US ton-mass
    :cvar L_KG: litre per kilogram
    :cvar L_T: litre per tonne
    :cvar L_TON_UK: litre per UK ton-mass
    :cvar M3_G: cubic metre per gram
    :cvar M3_KG: cubic metre per kilogram
    :cvar M3_T: cubic metre per tonne
    :cvar M3_TON_UK: cubic metre per UK ton-mass
    :cvar M3_TON_US: cubic metre per US ton-mass
    """

    VALUE_0_01_L_KG = "0.01 L/kg"
    BBL_TON_UK = "bbl/ton[UK]"
    BBL_TON_US = "bbl/ton[US]"
    CM3_G = "cm3/g"
    DM3_KG = "dm3/kg"
    DM3_T = "dm3/t"
    FT3_KG = "ft3/kg"
    FT3_LBM = "ft3/lbm"
    FT3_SACK_94LBM = "ft3/sack[94lbm]"
    GAL_UK_LBM = "gal[UK]/lbm"
    GAL_US_LBM = "gal[US]/lbm"
    GAL_US_SACK_94LBM = "gal[US]/sack[94lbm]"
    GAL_US_TON_UK = "gal[US]/ton[UK]"
    GAL_US_TON_US = "gal[US]/ton[US]"
    L_KG = "L/kg"
    L_T = "L/t"
    L_TON_UK = "L/ton[UK]"
    M3_G = "m3/g"
    M3_KG = "m3/kg"
    M3_T = "m3/t"
    M3_TON_UK = "m3/ton[UK]"
    M3_TON_US = "m3/ton[US]"


class VolumePerPressureUom(Enum):
    """
    :cvar BBL_PSI: barrel per psi
    :cvar M3_K_PA: cubic metre per kilopascal
    :cvar M3_PA: cubic metre per Pascal
    """

    BBL_PSI = "bbl/psi"
    M3_K_PA = "m3/kPa"
    M3_PA = "m3/Pa"


class VolumePerRotationUom(Enum):
    """
    :cvar FT3_RAD: cubic foot per radian
    :cvar M3_RAD: cubic metre per radian
    :cvar M3_REV: cubic metre per revolution
    """

    FT3_RAD = "ft3/rad"
    M3_RAD = "m3/rad"
    M3_REV = "m3/rev"


class VolumePerTimeLengthUom(Enum):
    """
    :cvar VALUE_1000_BBL_FT_D: thousand barrel foot per day
    :cvar VALUE_1000_M4_D: thousand (cubic metre per day) metre
    :cvar M4_S: metre to the fourth power per second
    """

    VALUE_1000_BBL_FT_D = "1000 bbl.ft/d"
    VALUE_1000_M4_D = "1000 m4/d"
    M4_S = "m4/s"


class VolumePerTimePerAreaUom(Enum):
    """
    :cvar FT3_MIN_FT2: cubic foot per minute square foot
    :cvar FT3_S_FT2: cubic foot per second square foot
    :cvar GAL_UK_H_FT2: UK gallon per hour square foot
    :cvar GAL_UK_H_IN2: UK gallon per hour square inch
    :cvar GAL_UK_MIN_FT2: UK gallon per minute square foot
    :cvar GAL_US_H_FT2: US gallon per hour square foot
    :cvar GAL_US_H_IN2: US gallon per hour square inch
    :cvar GAL_US_MIN_FT2: US gallon per minute square foot
    :cvar M3_S_M2: cubic metre per second square metre
    """

    FT3_MIN_FT2 = "ft3/(min.ft2)"
    FT3_S_FT2 = "ft3/(s.ft2)"
    GAL_UK_H_FT2 = "gal[UK]/(h.ft2)"
    GAL_UK_H_IN2 = "gal[UK]/(h.in2)"
    GAL_UK_MIN_FT2 = "gal[UK]/(min.ft2)"
    GAL_US_H_FT2 = "gal[US]/(h.ft2)"
    GAL_US_H_IN2 = "gal[US]/(h.in2)"
    GAL_US_MIN_FT2 = "gal[US]/(min.ft2)"
    M3_S_M2 = "m3/(s.m2)"


class VolumePerTimePerLengthUom(Enum):
    """
    :cvar VALUE_1000_FT3_D_FT: (thousand cubic foot per day) per foot
    :cvar VALUE_1000_M3_D_M: (thousand cubic metre per day) per metre
    :cvar VALUE_1000_M3_H_M: (thousand cubic metre per hour) per metre
    :cvar BBL_D_FT: barrel per day foot
    :cvar FT3_D_FT: (cubic foot per day) per foot
    :cvar GAL_UK_H_FT: UK gallon per hour foot
    :cvar GAL_UK_H_IN: UK gallon per hour inch
    :cvar GAL_UK_MIN_FT: UK gallon per minute foot
    :cvar GAL_US_H_FT: US gallon per hour foot
    :cvar GAL_US_H_IN: US gallon per hour inch
    :cvar GAL_US_MIN_FT: US gallon per minute foot
    :cvar M3_D_M: (cubic metre per day) per metre
    :cvar M3_H_M: (cubic metre per hour) per metre
    :cvar M3_S_FT: (cubic metre per second) per foot
    :cvar M3_S_M: cubic metre per second metre
    """

    VALUE_1000_FT3_D_FT = "1000 ft3/(d.ft)"
    VALUE_1000_M3_D_M = "1000 m3/(d.m)"
    VALUE_1000_M3_H_M = "1000 m3/(h.m)"
    BBL_D_FT = "bbl/(d.ft)"
    FT3_D_FT = "ft3/(d.ft)"
    GAL_UK_H_FT = "gal[UK]/(h.ft)"
    GAL_UK_H_IN = "gal[UK]/(h.in)"
    GAL_UK_MIN_FT = "gal[UK]/(min.ft)"
    GAL_US_H_FT = "gal[US]/(h.ft)"
    GAL_US_H_IN = "gal[US]/(h.in)"
    GAL_US_MIN_FT = "gal[US]/(min.ft)"
    M3_D_M = "m3/(d.m)"
    M3_H_M = "m3/(h.m)"
    M3_S_FT = "m3/(s.ft)"
    M3_S_M = "m3/(s.m)"


class VolumePerTimePerPressureLengthUom(Enum):
    """
    :cvar BBL_FT_PSI_D: barrel per day foot psi
    :cvar FT3_FT_PSI_D: cubic foot per day foot psi
    :cvar M2_K_PA_D: square metre per kilopascal day
    :cvar M2_PA_S: square metre per pascal second
    """

    BBL_FT_PSI_D = "bbl/(ft.psi.d)"
    FT3_FT_PSI_D = "ft3/(ft.psi.d)"
    M2_K_PA_D = "m2/(kPa.d)"
    M2_PA_S = "m2/(Pa.s)"


class VolumePerTimePerPressureUom(Enum):
    """
    :cvar VALUE_1000_FT3_PSI_D: (thousand cubic foot per day) per psi
    :cvar BBL_K_PA_D: (barrel per day) per kilopascal
    :cvar BBL_PSI_D: (barrel per day) per psi
    :cvar L_BAR_MIN: (litre per minute) per bar
    :cvar M3_BAR_D: (cubic metre per day) per bar
    :cvar M3_BAR_H: (cubic metre per hour) per bar
    :cvar M3_BAR_MIN: (cubic metre per minute) per bar
    :cvar M3_K_PA_D: (cubic metre per day) per kilopascal
    :cvar M3_K_PA_H: (cubic metre per hour) per kilopascal
    :cvar M3_PA_S: cubic metre per pascal second
    :cvar M3_PSI_D: (cubic metre per day) per psi
    """

    VALUE_1000_FT3_PSI_D = "1000 ft3/(psi.d)"
    BBL_K_PA_D = "bbl/(kPa.d)"
    BBL_PSI_D = "bbl/(psi.d)"
    L_BAR_MIN = "L/(bar.min)"
    M3_BAR_D = "m3/(bar.d)"
    M3_BAR_H = "m3/(bar.h)"
    M3_BAR_MIN = "m3/(bar.min)"
    M3_K_PA_D = "m3/(kPa.d)"
    M3_K_PA_H = "m3/(kPa.h)"
    M3_PA_S = "m3/(Pa.s)"
    M3_PSI_D = "m3/(psi.d)"


class VolumePerTimePerTimeUom(Enum):
    """
    :cvar BBL_D2: (barrel per day) per day
    :cvar BBL_H2: (barrel per hour) per hour
    :cvar DM3_S2: (cubic decimetre per second) per second
    :cvar FT3_D2: (cubic foot per day) per day
    :cvar FT3_H2: (cubic foot per hour) per hour
    :cvar FT3_MIN2: (cubic foot per minute) per minute
    :cvar FT3_S2: (cubic foot per second) per second
    :cvar GAL_UK_H2: (UK gallon per hour) per hour
    :cvar GAL_UK_MIN2: (UK gallon per minute) per minute
    :cvar GAL_US_H2: (US gallon per hour) per hour
    :cvar GAL_US_MIN2: (US gallon per minute) per minute
    :cvar L_S2: (litre per second) per second
    :cvar M3_D2: (cubic metre per day) per day
    :cvar M3_S2: cubic metre per second squared
    """

    BBL_D2 = "bbl/d2"
    BBL_H2 = "bbl/h2"
    DM3_S2 = "dm3/s2"
    FT3_D2 = "ft3/d2"
    FT3_H2 = "ft3/h2"
    FT3_MIN2 = "ft3/min2"
    FT3_S2 = "ft3/s2"
    GAL_UK_H2 = "gal[UK]/h2"
    GAL_UK_MIN2 = "gal[UK]/min2"
    GAL_US_H2 = "gal[US]/h2"
    GAL_US_MIN2 = "gal[US]/min2"
    L_S2 = "L/s2"
    M3_D2 = "m3/d2"
    M3_S2 = "m3/s2"


class VolumePerTimePerVolumeUom(Enum):
    """
    :cvar BBL_D_ACRE_FT: barrel per day acre foot
    :cvar M3_S_M3: cubic metre per time cubic metre
    """

    BBL_D_ACRE_FT = "bbl/(d.acre.ft)"
    M3_S_M3 = "m3/(s.m3)"


class VolumePerTimeUom(Enum):
    """
    :cvar VALUE_1_30_CM3_MIN: cubic centimetre per thirty minute
    :cvar VALUE_1000_BBL_D: thousand barrel per day
    :cvar VALUE_1000_FT3_D: thousand cubic foot per day
    :cvar VALUE_1000_M3_D: thousand cubic metre per day
    :cvar VALUE_1000_M3_H: thousand cubic metre per hour
    :cvar VALUE_1_E6_BBL_D: million barrel per day
    :cvar VALUE_1_E6_FT3_D: million cubic foot per day
    :cvar VALUE_1_E6_M3_D: million cubic metre per day
    :cvar BBL_D: barrel per day
    :cvar BBL_H: barrel per hour
    :cvar BBL_MIN: barrel per minute
    :cvar CM3_H: cubic centimetre per hour
    :cvar CM3_MIN: cubic centimetre per minute
    :cvar CM3_S: cubic centimetre per second
    :cvar DM3_S: cubic decimetre per second
    :cvar FT3_D: cubic foot per day
    :cvar FT3_H: cubic foot per hour
    :cvar FT3_MIN: cubic foot per minute
    :cvar FT3_S: cubic foot per second
    :cvar GAL_UK_D: UK gallon per day
    :cvar GAL_UK_H: UK gallon per hour
    :cvar GAL_UK_MIN: UK gallon per minute
    :cvar GAL_US_D: US gallon per day
    :cvar GAL_US_H: US gallon per hour
    :cvar GAL_US_MIN: US gallon per minute
    :cvar L_H: litre per hour
    :cvar L_MIN: litre per minute
    :cvar L_S: litre per second
    :cvar M3_D: cubic metre per day
    :cvar M3_H: cubic metre per hour
    :cvar M3_MIN: cubic metre per minute
    :cvar M3_S: cubic metre per second
    """

    VALUE_1_30_CM3_MIN = "1/30 cm3/min"
    VALUE_1000_BBL_D = "1000 bbl/d"
    VALUE_1000_FT3_D = "1000 ft3/d"
    VALUE_1000_M3_D = "1000 m3/d"
    VALUE_1000_M3_H = "1000 m3/h"
    VALUE_1_E6_BBL_D = "1E6 bbl/d"
    VALUE_1_E6_FT3_D = "1E6 ft3/d"
    VALUE_1_E6_M3_D = "1E6 m3/d"
    BBL_D = "bbl/d"
    BBL_H = "bbl/h"
    BBL_MIN = "bbl/min"
    CM3_H = "cm3/h"
    CM3_MIN = "cm3/min"
    CM3_S = "cm3/s"
    DM3_S = "dm3/s"
    FT3_D = "ft3/d"
    FT3_H = "ft3/h"
    FT3_MIN = "ft3/min"
    FT3_S = "ft3/s"
    GAL_UK_D = "gal[UK]/d"
    GAL_UK_H = "gal[UK]/h"
    GAL_UK_MIN = "gal[UK]/min"
    GAL_US_D = "gal[US]/d"
    GAL_US_H = "gal[US]/h"
    GAL_US_MIN = "gal[US]/min"
    L_H = "L/h"
    L_MIN = "L/min"
    L_S = "L/s"
    M3_D = "m3/d"
    M3_H = "m3/h"
    M3_MIN = "m3/min"
    M3_S = "m3/s"


class VolumePerVolumeUom(Enum):
    """
    :cvar VALUE: percent
    :cvar VOL: percent [volume basis]
    :cvar VALUE_0_001_BBL_FT3: barrel per thousand cubic foot
    :cvar VALUE_0_001_BBL_M3: barrel per thousand cubic metre
    :cvar VALUE_0_001_GAL_UK_BBL: UK gallon per thousand barrel
    :cvar VALUE_0_001_GAL_UK_GAL_UK: UK gallon per thousand UK gallon
    :cvar VALUE_0_001_GAL_US_BBL: US gallon per thousand barrel
    :cvar VALUE_0_001_GAL_US_FT3: US gallon per thousand cubic foot
    :cvar VALUE_0_001_GAL_US_GAL_US: US gallon per thousand US gallon
    :cvar VALUE_0_001_PT_UK_BBL: UK pint per thousand barrel
    :cvar VALUE_0_01_BBL_BBL: barrel per hundred barrel
    :cvar VALUE_0_1_GAL_US_BBL: US gallon per ten barrel
    :cvar VALUE_0_1_L_BBL: litre per ten barrel
    :cvar VALUE_0_1_PT_US_BBL: US pint per ten barrel
    :cvar VALUE_1000_FT3_BBL: thousand cubic foot per barrel
    :cvar VALUE_1000_M3_M3: thousand cubic metre per cubic metre
    :cvar VALUE_1_E_6_ACRE_FT_BBL: acre foot per million barrel
    :cvar VALUE_1_E_6_BBL_FT3: barrel per million cubic foot
    :cvar VALUE_1_E_6_BBL_M3: barrel per million cubic metre
    :cvar VALUE_1_E6_BBL_ACRE_FT: million barrel per acre foot
    :cvar VALUE_1_E6_FT3_ACRE_FT: million cubic foot per acre foot
    :cvar VALUE_1_E6_FT3_BBL: million cubic foot per barrel
    :cvar BBL_ACRE_FT: barrel per acre foot
    :cvar BBL_BBL: barrel per barrel
    :cvar BBL_FT3: barrel per cubic foot
    :cvar BBL_M3: barrel per cubic metre
    :cvar C_EUC: centieuclid
    :cvar CM3_CM3: cubic centimetre per cubic centimetre
    :cvar CM3_L: cubic centimetre per litre
    :cvar CM3_M3: cubic centimetre per cubic metre
    :cvar DM3_M3: cubic decimetre per cubic metre
    :cvar EUC: euclid
    :cvar FT3_BBL: cubic foot per barrel
    :cvar FT3_FT3: cubic foot per cubic foot
    :cvar GAL_UK_FT3: UK gallon per cubic foot
    :cvar GAL_US_BBL: US gallon per barrel
    :cvar GAL_US_FT3: US gallon per cubic foot
    :cvar L_M3: litre per cubic metre
    :cvar M3_HA_M: cubic metre per hectare metre
    :cvar M3_BBL: cubic metre per barrel
    :cvar M3_M3: cubic metre per cubic metre
    :cvar M_L_GAL_UK: millilitre per UK gallon
    :cvar M_L_GAL_US: millilitre per US gallon
    :cvar M_L_M_L: millilitre per millilitre
    :cvar PPK: part per thousand
    :cvar PPM: part per million
    :cvar PPM_VOL: part per million [volume basis]
    """

    VALUE = "%"
    VOL = "%[vol]"
    VALUE_0_001_BBL_FT3 = "0.001 bbl/ft3"
    VALUE_0_001_BBL_M3 = "0.001 bbl/m3"
    VALUE_0_001_GAL_UK_BBL = "0.001 gal[UK]/bbl"
    VALUE_0_001_GAL_UK_GAL_UK = "0.001 gal[UK]/gal[UK]"
    VALUE_0_001_GAL_US_BBL = "0.001 gal[US]/bbl"
    VALUE_0_001_GAL_US_FT3 = "0.001 gal[US]/ft3"
    VALUE_0_001_GAL_US_GAL_US = "0.001 gal[US]/gal[US]"
    VALUE_0_001_PT_UK_BBL = "0.001 pt[UK]/bbl"
    VALUE_0_01_BBL_BBL = "0.01 bbl/bbl"
    VALUE_0_1_GAL_US_BBL = "0.1 gal[US]/bbl"
    VALUE_0_1_L_BBL = "0.1 L/bbl"
    VALUE_0_1_PT_US_BBL = "0.1 pt[US]/bbl"
    VALUE_1000_FT3_BBL = "1000 ft3/bbl"
    VALUE_1000_M3_M3 = "1000 m3/m3"
    VALUE_1_E_6_ACRE_FT_BBL = "1E-6 acre.ft/bbl"
    VALUE_1_E_6_BBL_FT3 = "1E-6 bbl/ft3"
    VALUE_1_E_6_BBL_M3 = "1E-6 bbl/m3"
    VALUE_1_E6_BBL_ACRE_FT = "1E6 bbl/(acre.ft)"
    VALUE_1_E6_FT3_ACRE_FT = "1E6 ft3/(acre.ft)"
    VALUE_1_E6_FT3_BBL = "1E6 ft3/bbl"
    BBL_ACRE_FT = "bbl/(acre.ft)"
    BBL_BBL = "bbl/bbl"
    BBL_FT3 = "bbl/ft3"
    BBL_M3 = "bbl/m3"
    C_EUC = "cEuc"
    CM3_CM3 = "cm3/cm3"
    CM3_L = "cm3/L"
    CM3_M3 = "cm3/m3"
    DM3_M3 = "dm3/m3"
    EUC = "Euc"
    FT3_BBL = "ft3/bbl"
    FT3_FT3 = "ft3/ft3"
    GAL_UK_FT3 = "gal[UK]/ft3"
    GAL_US_BBL = "gal[US]/bbl"
    GAL_US_FT3 = "gal[US]/ft3"
    L_M3 = "L/m3"
    M3_HA_M = "m3/(ha.m)"
    M3_BBL = "m3/bbl"
    M3_M3 = "m3/m3"
    M_L_GAL_UK = "mL/gal[UK]"
    M_L_GAL_US = "mL/gal[US]"
    M_L_M_L = "mL/mL"
    PPK = "ppk"
    PPM = "ppm"
    PPM_VOL = "ppm[vol]"


class VolumeUom(Enum):
    """
    :cvar VALUE_1000_BBL: thousand barrel
    :cvar VALUE_1000_FT3: thousand cubic foot
    :cvar VALUE_1000_GAL_UK: thousand UK gallon
    :cvar VALUE_1000_GAL_US: thousand US gallon
    :cvar VALUE_1000_M3: thousand cubic metre
    :cvar VALUE_1_E_6_GAL_US: millionth of US gallon
    :cvar VALUE_1_E12_FT3: million million cubic foot
    :cvar VALUE_1_E6_BBL: million barrel
    :cvar VALUE_1_E6_FT3: million cubic foot
    :cvar VALUE_1_E6_M3: million cubic metre
    :cvar VALUE_1_E9_BBL: thousand million barrel
    :cvar VALUE_1_E9_FT3: thousand million cubic foot
    :cvar ACRE_FT: acre foot
    :cvar BBL: barrel
    :cvar CM3: cubic centimetre
    :cvar DM3: cubic decimetre
    :cvar FLOZ_UK: UK fluid-ounce
    :cvar FLOZ_US: US fluid-ounce
    :cvar FT3: cubic foot
    :cvar GAL_UK: UK gallon
    :cvar GAL_US: US gallon
    :cvar HA_M: hectare metre
    :cvar H_L: hectolitre
    :cvar IN3: cubic inch
    :cvar KM3: cubic kilometre
    :cvar L: litre
    :cvar M3: cubic metre
    :cvar MI3: cubic mile
    :cvar M_L: millilitre
    :cvar MM3: cubic millimetre
    :cvar PT_UK: UK pint
    :cvar PT_US: US pint
    :cvar QT_UK: UK quart
    :cvar QT_US: US quart
    :cvar UM2_M: square micrometre metre
    :cvar YD3: cubic yard
    """

    VALUE_1000_BBL = "1000 bbl"
    VALUE_1000_FT3 = "1000 ft3"
    VALUE_1000_GAL_UK = "1000 gal[UK]"
    VALUE_1000_GAL_US = "1000 gal[US]"
    VALUE_1000_M3 = "1000 m3"
    VALUE_1_E_6_GAL_US = "1E-6 gal[US]"
    VALUE_1_E12_FT3 = "1E12 ft3"
    VALUE_1_E6_BBL = "1E6 bbl"
    VALUE_1_E6_FT3 = "1E6 ft3"
    VALUE_1_E6_M3 = "1E6 m3"
    VALUE_1_E9_BBL = "1E9 bbl"
    VALUE_1_E9_FT3 = "1E9 ft3"
    ACRE_FT = "acre.ft"
    BBL = "bbl"
    CM3 = "cm3"
    DM3 = "dm3"
    FLOZ_UK = "floz[UK]"
    FLOZ_US = "floz[US]"
    FT3 = "ft3"
    GAL_UK = "gal[UK]"
    GAL_US = "gal[US]"
    HA_M = "ha.m"
    H_L = "hL"
    IN3 = "in3"
    KM3 = "km3"
    L = "L"
    M3 = "m3"
    MI3 = "mi3"
    M_L = "mL"
    MM3 = "mm3"
    PT_UK = "pt[UK]"
    PT_US = "pt[US]"
    QT_UK = "qt[UK]"
    QT_US = "qt[US]"
    UM2_M = "um2.m"
    YD3 = "yd3"


class VolumetricHeatTransferCoefficientUom(Enum):
    """
    :cvar BTU_IT_H_FT3_DELTA_F: BTU per hour cubic foot delta Fahrenheit
    :cvar BTU_IT_S_FT3_DELTA_F: (BTU per second) per cubic foot delta
        Fahrenheit
    :cvar K_W_M3_DELTA_K: killowatt per cubic metre delta kelvin
    :cvar W_M3_DELTA_K: watt per cubic metre delta kelvin
    """

    BTU_IT_H_FT3_DELTA_F = "Btu[IT]/(h.ft3.deltaF)"
    BTU_IT_S_FT3_DELTA_F = "Btu[IT]/(s.ft3.deltaF)"
    K_W_M3_DELTA_K = "kW/(m3.deltaK)"
    W_M3_DELTA_K = "W/(m3.deltaK)"


class VolumetricThermalExpansionUom(Enum):
    """
    :cvar VALUE_1_DELTA_C: per delta Celsius
    :cvar VALUE_1_DELTA_F: per delta Fahrenheit
    :cvar VALUE_1_DELTA_K: per delta kelvin
    :cvar VALUE_1_DELTA_R: per delta Rankine
    :cvar VALUE_1_E_6_M3_M3_DELTA_C: (cubic metre per million cubic
        metre) per delta Celsius
    :cvar VALUE_1_E_6_M3_M3_DELTA_F: (cubic metre per million cubic
        metre) per delta Fahrenheit
    :cvar M3_M3_DELTA_K: cubic metre per cubic metre delta kelvin
    :cvar PPM_VOL_DELTA_C: (part per million [volume basis]) per delta
        Celsius
    :cvar PPM_VOL_DELTA_F: (part per million [volume basis)] per delta
        Fahrenheit
    """

    VALUE_1_DELTA_C = "1/deltaC"
    VALUE_1_DELTA_F = "1/deltaF"
    VALUE_1_DELTA_K = "1/deltaK"
    VALUE_1_DELTA_R = "1/deltaR"
    VALUE_1_E_6_M3_M3_DELTA_C = "1E-6 m3/(m3.deltaC)"
    VALUE_1_E_6_M3_M3_DELTA_F = "1E-6 m3/(m3.deltaF)"
    M3_M3_DELTA_K = "m3/(m3.deltaK)"
    PPM_VOL_DELTA_C = "ppm[vol]/deltaC"
    PPM_VOL_DELTA_F = "ppm[vol]/deltaF"


@dataclass
class ApigammaRayMeasure:
    class Meta:
        name = "APIGammaRayMeasure"

    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[ApigammaRayUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class ApigravityMeasure:
    class Meta:
        name = "APIGravityMeasure"

    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[ApigravityUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class ApineutronMeasure:
    class Meta:
        name = "APINeutronMeasure"

    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[ApineutronUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class AbsorbedDoseMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[AbsorbedDoseUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class AbstractObject:
    """The intended abstract supertype of all schema roots that may be a member of
    a substitution group (whether contextual or data).

    The type of root global elements should be extended from this type
    and the root global element should be declared to be a member of one
    of the above substitution groups.

    :ivar citation:
    :ivar aliases:
    :ivar custom_data:
    :ivar schema_version: The specific version of a schema from which
        this object is derived. This string should be exactly equivalent
        to the version attribute of the root element of the associated
        XSD schema file. In the UML model is the same as the version
        tagged value of the &lt;&lt;XSDschema&gt;&gt; package.
    :ivar uuid:
    :ivar object_version:
    """

    citation: Optional[Citation] = field(
        default=None,
        metadata={
            "name": "Citation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/commonv2",
        },
    )
    aliases: List[ObjectAlias] = field(
        default_factory=list,
        metadata={
            "name": "Aliases",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/commonv2",
        },
    )
    custom_data: Optional[CustomData] = field(
        default=None,
        metadata={
            "name": "CustomData",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/commonv2",
        },
    )
    schema_version: Optional[str] = field(
        default=None,
        metadata={
            "name": "schemaVersion",
            "type": "Attribute",
            "required": True,
        },
    )
    uuid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
            "pattern": r"[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}",
        },
    )
    object_version: Optional[str] = field(
        default=None,
        metadata={
            "name": "objectVersion",
            "type": "Attribute",
            "min_length": 1,
            "max_length": 64,
            "white_space": "collapse",
        },
    )


@dataclass
class ActivityOfRadioactivityMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[ActivityOfRadioactivityUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class AmountOfSubstanceMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[AmountOfSubstanceUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class AmountOfSubstancePerAmountOfSubstanceMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[AmountOfSubstancePerAmountOfSubstanceUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class AmountOfSubstancePerAreaMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[AmountOfSubstancePerAreaUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class AmountOfSubstancePerTimeMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[AmountOfSubstancePerTimeUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class AmountOfSubstancePerTimePerAreaMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[AmountOfSubstancePerTimePerAreaUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class AmountOfSubstancePerVolumeMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[AmountOfSubstancePerVolumeUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class AnglePerLengthMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[AnglePerLengthUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class AnglePerVolumeMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[AnglePerVolumeUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class AngularAccelerationMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[AngularAccelerationUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class AngularVelocityMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[AngularVelocityUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class AreaMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[AreaUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class AreaPerAmountOfSubstanceMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[AreaPerAmountOfSubstanceUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class AreaPerAreaMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[AreaPerAreaUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class AreaPerMassMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[AreaPerMassUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class AreaPerTimeMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[AreaPerTimeUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class AreaPerVolumeMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[AreaPerVolumeUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class AttenuationPerFrequencyIntervalMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[AttenuationPerFrequencyIntervalUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class CapacitanceMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[CapacitanceUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class DataTransferSpeedMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[DataTransferSpeedUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class DiffusionCoefficientMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[DiffusionCoefficientUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class DigitalStorageMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[DigitalStorageUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class DimensionlessMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[DimensionlessUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class DipoleMomentMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[DipoleMomentUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class DoseEquivalentMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[DoseEquivalentUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class DynamicViscosityMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[DynamicViscosityUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class ElectricChargeMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[ElectricChargeUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class ElectricChargePerAreaMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[ElectricChargePerAreaUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class ElectricChargePerMassMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[ElectricChargePerMassUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class ElectricChargePerVolumeMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[ElectricChargePerVolumeUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class ElectricConductanceMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[ElectricConductanceUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class ElectricConductivityMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[ElectricConductivityUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class ElectricCurrentDensityMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[ElectricCurrentDensityUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class ElectricCurrentMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[ElectricCurrentUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class ElectricFieldStrengthMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[ElectricFieldStrengthUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class ElectricPotentialDifferenceMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[ElectricPotentialDifferenceUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class ElectricResistanceMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[ElectricResistanceUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class ElectricResistancePerLengthMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[ElectricResistancePerLengthUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class ElectricalResistivityMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[ElectricalResistivityUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class ElectromagneticMomentMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[ElectromagneticMomentUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class EnergyLengthPerAreaMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[EnergyLengthPerAreaUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class EnergyLengthPerTimeAreaTemperatureMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[EnergyLengthPerTimeAreaTemperatureUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class EnergyMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[EnergyUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class EnergyPerAreaMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[EnergyPerAreaUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class EnergyPerLengthMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[EnergyPerLengthUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class EnergyPerMassMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[EnergyPerMassUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class EnergyPerMassPerTimeMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[EnergyPerMassPerTimeUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class EnergyPerVolumeMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[EnergyPerVolumeUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class ForceAreaMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[ForceAreaUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class ForceLengthPerLengthMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[ForceLengthPerLengthUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class ForceMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[ForceUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class ForcePerForceMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[ForcePerForceUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class ForcePerLengthMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[ForcePerLengthUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class ForcePerVolumeMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[ForcePerVolumeUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class FrequencyIntervalMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[FrequencyIntervalUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class FrequencyMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[FrequencyUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class GmlProjectedCrsDefinition(AbstractProjectedCrs):
    """
    This is the Energistics encapsulation of the ProjectedCrs type from GML.
    """

    gml_projected_crs_definition: Optional[ProjectedCrstype] = field(
        default=None,
        metadata={
            "name": "GmlProjectedCrsDefinition",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/commonv2",
            "required": True,
        },
    )


@dataclass
class GmlVerticalCrsDefinition(AbstractVerticalCrs):
    """
    This is the Energistics encapsulation of the ProjectedCrs type from GML.
    """

    gml_vertical_crs_definition: Optional[VerticalCrstype] = field(
        default=None,
        metadata={
            "name": "GmlVerticalCrsDefinition",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/commonv2",
            "required": True,
        },
    )


@dataclass
class Hdf5Dataset:
    """
    :ivar path_in_hdf_file: The path of the referenced dataset in the
        HDF file. The separator between groups and final dataset is a
        slash '/'
    :ivar hdf_proxy:
    """

    path_in_hdf_file: Optional[str] = field(
        default=None,
        metadata={
            "name": "PathInHdfFile",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/commonv2",
            "required": True,
        },
    )
    hdf_proxy: Optional[DataObjectReference] = field(
        default=None,
        metadata={
            "name": "HdfProxy",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/commonv2",
            "required": True,
        },
    )


@dataclass
class HeatCapacityMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[HeatCapacityUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class HeatFlowRateMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[HeatFlowRateUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class HeatTransferCoefficientMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[HeatTransferCoefficientUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class IlluminanceMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[IlluminanceUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class InductanceMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[InductanceUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class IsothermalCompressibilityMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[IsothermalCompressibilityUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class KinematicViscosityMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[KinematicViscosityUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class LengthMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[LengthUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class LengthPerLengthMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[LengthPerLengthUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class LengthPerMassMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[LengthPerMassUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class LengthPerPressureMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[LengthPerPressureUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class LengthPerTemperatureMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[LengthPerTemperatureUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class LengthPerTimeMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[LengthPerTimeUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class LengthPerVolumeMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[LengthPerVolumeUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class LightExposureMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[LightExposureUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class LinearAccelerationMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[LinearAccelerationUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class LinearThermalExpansionMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[LinearThermalExpansionUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class LogarithmicPowerRatioMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[LogarithmicPowerRatioUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class LogarithmicPowerRatioPerLengthMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[LogarithmicPowerRatioPerLengthUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class LuminanceMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[LuminanceUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class LuminousEfficacyMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[LuminousEfficacyUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class LuminousFluxMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[LuminousFluxUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class LuminousIntensityMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[LuminousIntensityUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class MagneticDipoleMomentMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[MagneticDipoleMomentUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class MagneticFieldStrengthMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[MagneticFieldStrengthUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class MagneticFluxDensityMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[MagneticFluxDensityUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class MagneticFluxDensityPerLengthMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[MagneticFluxDensityPerLengthUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class MagneticFluxMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[MagneticFluxUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class MagneticPermeabilityMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[MagneticPermeabilityUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class MagneticVectorPotentialMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[MagneticVectorPotentialUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class MassLengthMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[MassLengthUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class MassMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[MassUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class MassPerAreaMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[MassPerAreaUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class MassPerEnergyMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[MassPerEnergyUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class MassPerLengthMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[MassPerLengthUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class MassPerMassMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[MassPerMassUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class MassPerTimeMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[MassPerTimeUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class MassPerTimePerAreaMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[MassPerTimePerAreaUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class MassPerTimePerLengthMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[MassPerTimePerLengthUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class MassPerVolumeMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[MassPerVolumeUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class MassPerVolumePerLengthMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[MassPerVolumePerLengthUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class MobilityMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[MobilityUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class MolarEnergyMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[MolarEnergyUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class MolarHeatCapacityMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[MolarHeatCapacityUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class MolarVolumeMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[MolarVolumeUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class MolecularWeightMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[MolecularWeightUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class MomentOfForceMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[MomentOfForceUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class MomentOfInertiaMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[MomentOfInertiaUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class MomentumMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[MomentumUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class NormalizedPowerMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[NormalizedPowerUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class PermeabilityLengthMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[PermeabilityLengthUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class PermeabilityRockMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[PermeabilityRockUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class PermittivityMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[PermittivityUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class PlaneAngleMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[PlaneAngleUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class PotentialDifferencePerPowerDropMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[PotentialDifferencePerPowerDropUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class PowerMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[PowerUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class PowerPerAreaMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[PowerPerAreaUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class PowerPerPowerMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[PowerPerPowerUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class PowerPerVolumeMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[PowerPerVolumeUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class PressureMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[PressureUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class PressurePerTimeMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[PressurePerTimeUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class PressurePerVolumeMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[PressurePerVolumeUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class PressureSquaredMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[PressureSquaredUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class PressureSquaredPerForceTimePerAreaMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[PressureSquaredPerForceTimePerAreaUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class PressureTimePerVolumeMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[PressureTimePerVolumeUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class ProjectedCrsEpsgCode(AbstractProjectedCrs):
    """
    This is the Energistics encapsulation of the ProjectedCrs type from GML.
    """

    epsg_code: Optional[int] = field(
        default=None,
        metadata={
            "name": "EpsgCode",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/commonv2",
            "required": True,
        },
    )


@dataclass
class ProjectedUnknownCrs(AbstractProjectedCrs):
    """
    This is the Energistics encapsulation of the ProjectedCrs type from GML.
    """

    unknown: Optional[str] = field(
        default=None,
        metadata={
            "name": "Unknown",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/commonv2",
            "required": True,
            "min_length": 1,
            "max_length": 256,
            "white_space": "collapse",
        },
    )


@dataclass
class QuantityOfLightMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[QuantityOfLightUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class RadianceMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[RadianceUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class RadiantIntensityMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[RadiantIntensityUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class ReciprocalAreaMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[ReciprocalAreaUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class ReciprocalElectricPotentialDifferenceMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[ReciprocalElectricPotentialDifferenceUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class ReciprocalForceMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[ReciprocalForceUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class ReciprocalLengthMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[ReciprocalLengthUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class ReciprocalMassMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[ReciprocalMassUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class ReciprocalMassTimeMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[ReciprocalMassTimeUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class ReciprocalPressureMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[ReciprocalPressureUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class ReciprocalTimeMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[ReciprocalTimeUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class ReciprocalVolumeMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[ReciprocalVolumeUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class ReluctanceMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[ReluctanceUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class SecondMomentOfAreaMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[SecondMomentOfAreaUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class SignalingEventPerTimeMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[SignalingEventPerTimeUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class SolidAngleMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[SolidAngleUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class SpecificHeatCapacityMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[SpecificHeatCapacityUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class TemperatureIntervalMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[TemperatureIntervalUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class TemperatureIntervalPerLengthMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[TemperatureIntervalPerLengthUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class TemperatureIntervalPerPressureMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[TemperatureIntervalPerPressureUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class TemperatureIntervalPerTimeMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[TemperatureIntervalPerTimeUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class ThermalConductanceMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[ThermalConductanceUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class ThermalConductivityMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[ThermalConductivityUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class ThermalDiffusivityMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[ThermalDiffusivityUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class ThermalInsulanceMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[ThermalInsulanceUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class ThermalResistanceMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[ThermalResistanceUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class ThermodynamicTemperatureMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[ThermodynamicTemperatureUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class TimeMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[TimeUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class TimePerLengthMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[TimePerLengthUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class TimePerMassMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[TimePerMassUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class TimePerTimeMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[TimePerTimeUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class TimePerVolumeMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[TimePerVolumeUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class VerticalCrsEpsgCode(AbstractVerticalCrs):
    """
    This is the Energistics encapsulation of the ProjectedCrs type from GML.
    """

    epsg_code: Optional[int] = field(
        default=None,
        metadata={
            "name": "EpsgCode",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/commonv2",
            "required": True,
        },
    )


@dataclass
class VerticalUnknownCrs(AbstractVerticalCrs):
    """
    This is the Energistics encapsulation of the ProjectedCrs type from GML.
    """

    unknown: Optional[str] = field(
        default=None,
        metadata={
            "name": "Unknown",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/commonv2",
            "required": True,
            "min_length": 1,
            "max_length": 256,
            "white_space": "collapse",
        },
    )


@dataclass
class VolumeFlowRatePerVolumeFlowRateMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[VolumeFlowRatePerVolumeFlowRateUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class VolumeMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[VolumeUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class VolumePerAreaMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[VolumePerAreaUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class VolumePerLengthMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[VolumePerLengthUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class VolumePerMassMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[VolumePerMassUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class VolumePerPressureMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[VolumePerPressureUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class VolumePerRotationMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[VolumePerRotationUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class VolumePerTimeLengthMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[VolumePerTimeLengthUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class VolumePerTimeMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[VolumePerTimeUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class VolumePerTimePerAreaMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[VolumePerTimePerAreaUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class VolumePerTimePerLengthMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[VolumePerTimePerLengthUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class VolumePerTimePerPressureLengthMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[VolumePerTimePerPressureLengthUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class VolumePerTimePerPressureMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[VolumePerTimePerPressureUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class VolumePerTimePerTimeMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[VolumePerTimePerTimeUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class VolumePerTimePerVolumeMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[VolumePerTimePerVolumeUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class VolumePerVolumeMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[VolumePerVolumeUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class VolumetricHeatTransferCoefficientMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[VolumetricHeatTransferCoefficientUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class VolumetricThermalExpansionMeasure:
    value: Optional[float] = field(
        default=None,
        metadata={
            "required": True,
        },
    )
    uom: Optional[VolumetricThermalExpansionUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class AbstractCitedDataObject(AbstractObject):
    """The Mother Class for all Top Level Elements in RESQML.

    Inherits from the commonv2 AbstractDataObject. The purpose of this
    derivation is simply to make the Citation element mandatory.
    Appropriate to use as a base class in any ML where this is desired.
    """

    citation: Optional[Citation] = field(
        default=None,
        metadata={
            "name": "Citation",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/commonv2",
            "required": True,
        },
    )


@dataclass
class AbstractContextualObject(AbstractObject):
    """
    Substitution group for contextual objects.
    """

    class Meta:
        namespace = "http://www.energistics.org/energyml/data/commonv2"


@dataclass
class AbstractDataObject(AbstractObject):
    """
    Substitution group for normative data objects.
    """

    class Meta:
        namespace = "http://www.energistics.org/energyml/data/commonv2"


@dataclass
class ProjectedCrs(AbstractCitedDataObject):
    """
    This is the Energistics encapsulation of the ProjectedCrs type from GML.
    """

    axis_order: Optional[AxisOrder2D] = field(
        default=None,
        metadata={
            "name": "AxisOrder",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/commonv2",
            "required": True,
        },
    )
    abstract_projected_crs: Optional[AbstractProjectedCrs] = field(
        default=None,
        metadata={
            "name": "AbstractProjectedCrs",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/commonv2",
            "required": True,
        },
    )
    uom: Optional[LengthUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class VerticalCrs(AbstractCitedDataObject):
    direction: Optional[VerticalDirection] = field(
        default=None,
        metadata={
            "name": "Direction",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/commonv2",
            "required": True,
        },
    )
    abstract_vertical_crs: Optional[AbstractVerticalCrs] = field(
        default=None,
        metadata={
            "name": "AbstractVerticalCrs",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/commonv2",
            "required": True,
        },
    )
    uom: Optional[LengthUom] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class ObjEpcExternalPartReference(AbstractCitedDataObject):
    """It defines a proxy for external part of the EPC package.

    It must be used at least for external HDF parts.

    :ivar mime_type: IAMF registered, if one exists, or a free text
        field. Needs documentation on seismic especially. MIME type for
        HDF proxy is : application/x-hdf5 (by RESQML convention).
    """

    class Meta:
        name = "obj_EpcExternalPartReference"

    mime_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "MimeType",
            "type": "Element",
            "namespace": "http://www.energistics.org/energyml/data/commonv2",
            "required": True,
        },
    )


@dataclass
class EpcExternalPartReference(ObjEpcExternalPartReference):
    class Meta:
        namespace = "http://www.energistics.org/energyml/data/commonv2"
